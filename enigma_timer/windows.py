# -*- coding: utf-8 -*-
"""Multi-window mode: any section of the app in its own window.

* PageWindow shows Training, Reference or Achievements on its own.
* MiniTimerWindow is a compact timer that saves into the current session
  of the main window, so it can sit next to the algorithms.

Every window shares the main window's store and TrainingHub, so progress and
solves made in one window appear in all of them immediately.
"""

import sys
import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QPushButton, QSizePolicy,
                             QVBoxLayout, QWidget)

from . import scramble as scr
from . import theme
from .i18n import tr
from .stats import OK, Solve, fmt_ms
from .widgets import TimerDisplay

IDLE, HOLDING, READY, RUNNING, STOPPED = range(5)


def _dark(widget):
    if sys.platform.startswith("win"):
        from .window import _dark_title_bar
        _dark_title_bar(widget)


class _BaseWindow(QMainWindow):
    """Dark window with a slim header: title on the left, pin on the right."""

    def __init__(self, main, title, parent=None):
        QMainWindow.__init__(self, parent)
        self.main = main
        self.setWindowTitle("Enigma Cube — " + title)
        self.setWindowIcon(main.windowIcon())
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        self.body = QVBoxLayout(central)
        self.body.setSpacing(12)
        head = QHBoxLayout()
        head.setSpacing(8)
        self.title = QLabel(title)
        self.title.setStyleSheet("font-size: 15px; font-weight: 700; color: %s;" % theme.MUTED)
        head.addWidget(self.title)
        head.addStretch(1)
        self.pin = QPushButton(tr("pin"))
        self.pin.setObjectName("pin")
        self.pin.setCheckable(True)
        self.pin.setFocusPolicy(Qt.NoFocus)
        self.pin.setToolTip(tr("pin_window"))
        self.pin.toggled.connect(self.set_pinned)
        head.addWidget(self.pin)
        self.body.addLayout(head)

    def set_pinned(self, on):
        geo = self.geometry()
        self.setWindowFlag(Qt.WindowStaysOnTopHint, bool(on))
        self.setGeometry(geo)
        self.show()

    def sync(self):
        """Called by the main window whenever solves or progress change."""

    def showEvent(self, e):
        QMainWindow.showEvent(self, e)
        self.setFocus()
        if not getattr(self, "_dark_done", False):
            self._dark_done = True
            _dark(self)


class PageWindow(_BaseWindow):
    """Training, Reference or Achievements in a separate window."""

    TITLES = {"training": "win_training", "reference": "win_reference",
              "achievements": "win_achievements"}

    def __init__(self, main, kind, parent=None):
        _BaseWindow.__init__(self, main, tr(self.TITLES[kind]), parent)
        self.kind = kind
        self.body.setContentsMargins(18, 10, 18, 18)
        from .pages import AchievementsPage, ReferencePage
        from .training import TrainingWidget
        if kind == "training":
            self.page = TrainingWidget(main.hub)
            self.resize(1180, 780)
        elif kind == "reference":
            self.page = ReferencePage(main.hub)
            self.page.show_puzzle(main.reference_puzzle())
            self.resize(1100, 760)
        else:
            self.page = AchievementsPage(main.store)
            self.page.refresh()
            self.resize(900, 720)
        self.body.addWidget(self.page, 1)

    def sync(self):
        if self.kind == "achievements":
            self.page.refresh()


class MiniTimerWindow(_BaseWindow):
    """A small always-handy timer that saves into the main session."""

    def __init__(self, main, parent=None):
        _BaseWindow.__init__(self, main, tr("win_mini_timer"), parent)
        self.state = IDLE
        self.t_start = 0.0
        self.hold_start = 0.0
        self.body.setContentsMargins(16, 10, 16, 14)
        self.body.setSpacing(6)

        self.scramble = QLabel()
        self.scramble.setWordWrap(True)
        self.scramble.setAlignment(Qt.AlignCenter)
        self.scramble.setTextFormat(Qt.PlainText)
        self.scramble.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.scramble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.scramble.setStyleSheet("font-size: 15px; color: %s;" % theme.SCRAMBLE)
        self.body.addWidget(self.scramble)

        self.display = TimerDisplay()
        self.display.setMinimumHeight(110)
        self.display.pressed.connect(lambda: self._press(Qt.Key_Space, False))
        self.display.released.connect(lambda: self._release(Qt.Key_Space, False))
        self.body.addWidget(self.display, 1)

        self.hint = QLabel(tr("mini_hint"))
        self.hint.setObjectName("muted")
        self.hint.setAlignment(Qt.AlignCenter)
        self.hint.setStyleSheet("font-size: 12px;")
        self.body.addWidget(self.hint)

        self.tick = QTimer(self)
        self.tick.setTimerType(Qt.PreciseTimer)
        self.tick.timeout.connect(self._on_tick)

        self.setFocusPolicy(Qt.StrongFocus)
        self.resize(460, 330)
        self.setMinimumSize(340, 260)
        self.sync()

    # ------------------------------------------------------------------
    def _decimals(self):
        return int(self.main.settings.get("decimals", 2))

    def sync(self):
        m = self.main
        self.title.setText("%s · %s" % (tr("win_mini_timer"),
                                        scr.PUZZLE_NAME.get(m.session.puzzle, m.session.puzzle)))
        self.scramble.setText(m.scramble)
        if self.state == IDLE:
            self._render()

    def _render(self):
        d = self._decimals()
        st = self.state
        if st == RUNNING:
            ms = int((time.perf_counter() - self.t_start) * 1000)
            self.display.set_display(fmt_ms(ms, d), theme.TEXT)
        elif st == HOLDING:
            self.display.set_display(self.main._last_text(d), theme.HOLD)
        elif st == READY:
            self.display.set_display(fmt_ms(0, d), theme.READY)
        else:
            self.display.set_display(self.main._last_text(d), theme.TEXT, self.main._last_sub())
        busy = st in (HOLDING, READY, RUNNING)
        self.scramble.setVisible(not busy or st == HOLDING)
        if self.main.state != 0:
            self.hint.setText(tr("mini_busy"))
        else:
            self.hint.setText(tr("mini_hint"))

    def _on_tick(self):
        if self.state == HOLDING:
            hold = int(self.main.settings.get("hold_ms", 300))
            if (time.perf_counter() - self.hold_start) * 1000 >= hold:
                self.state = READY
        self._render()

    # ------------------------------------------------------------------
    def _press(self, key, auto_repeat):
        if self.state == RUNNING:
            if not auto_repeat:
                self._stop()
            return True
        if self.state == STOPPED:
            return True
        if key == Qt.Key_Escape and self.state in (HOLDING, READY):
            self.state = IDLE
            self.tick.stop()
            self._render()
            return True
        if key != Qt.Key_Space or auto_repeat:
            return key == Qt.Key_Space
        if self.state == IDLE and self.main.state == 0:
            self.hold_start = time.perf_counter()
            self.state = HOLDING
            if int(self.main.settings.get("hold_ms", 300)) <= 0:
                self.state = READY
            self.tick.start(15)
            self._render()
        return True

    def _release(self, key, auto_repeat):
        if auto_repeat:
            return True
        if self.state == STOPPED:
            self.state = IDLE
            self._render()
            return True
        if key != Qt.Key_Space:
            return False
        if self.state == HOLDING:
            self.state = IDLE
            self.tick.stop()
            self._render()
        elif self.state == READY:
            self.t_start = time.perf_counter()
            self.state = RUNNING
            self._render()
        return True

    def _stop(self):
        ms = int((time.perf_counter() - self.t_start) * 1000)
        self.tick.stop()
        self.state = STOPPED
        m = self.main
        m._add_solve(Solve(ms, OK, m.scramble))
        m.new_scramble(force=True)
        self.sync()
        self._render()

    def keyPressEvent(self, e):
        if not self._press(e.key(), e.isAutoRepeat()):
            _BaseWindow.keyPressEvent(self, e)

    def keyReleaseEvent(self, e):
        if not self._release(e.key(), e.isAutoRepeat()):
            _BaseWindow.keyReleaseEvent(self, e)

    def mousePressEvent(self, e):
        if self.state == RUNNING:
            self._stop()
        else:
            _BaseWindow.mousePressEvent(self, e)

    def closeEvent(self, e):
        if self.state == RUNNING:
            self._stop()
        self.tick.stop()
        _BaseWindow.closeEvent(self, e)


__all__ = ["PageWindow", "MiniTimerWindow"]
