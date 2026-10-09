"""Main window and the timer state machine."""

import os
import sys
import time

from PyQt5.QtCore import QByteArray, QEvent, QObject, Qt, QTimer
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QAction, QApplication,
                             QButtonGroup, QComboBox, QDialog, QFileDialog, QFrame, QHBoxLayout,
                             QHeaderView, QInputDialog, QLabel, QLineEdit, QMainWindow,
                             QMenu, QMessageBox, QPlainTextEdit, QPushButton, QShortcut,
                             QSizePolicy, QStackedWidget, QTableWidget, QTableWidgetItem, QTextEdit,
                             QToolButton, QVBoxLayout, QWidget)

from . import scramble as scr
from . import storage, theme
from .dialogs import AboutDialog, SettingsDialog, SolveDialog, TextDialog
from .i18n import tr
from .stats import (DNF, INF, OK, PLUS2, STAT_ROWS, SessionStats, Solve, fmt_avg,
                    fmt_ms, fmt_solve, parse_time, trimmed_indices)
from .stats import average as stats_average
from .stats import mean as stats_mean
from .training import TrainingHub, TrainingWidget, TrainingWindow
from .widgets import ScramblePreview, TimeChart, TimeHistogram, TimerDisplay, Toast

# PyInstaller unpacks bundled files to sys._MEIPASS
_BASE = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(_BASE, "assets")

# timer states
IDLE, INSPECTING, HOLDING, READY, RUNNING, STOPPED = range(6)

INSPECTION_S = 15.0


def _panel():
    f = QFrame()
    f.setObjectName("panel")
    return f


def _section(text):
    lb = QLabel(text.upper())
    lb.setObjectName("sectionTitle")
    return lb


def _dark_title_bar(widget):
    """Ask Windows 10/11 to draw a dark title bar (no-op elsewhere)."""
    if not sys.platform.startswith("win"):
        return
    try:
        import ctypes
        hwnd = ctypes.c_void_p(int(widget.winId()))
        value = ctypes.c_int(1)
        for attr in (20, 19):  # DWMWA_USE_IMMERSIVE_DARK_MODE (new / old builds)
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, attr, ctypes.byref(value), ctypes.sizeof(value)) == 0:
                break
    except Exception:  # noqa: BLE001 - purely cosmetic
        pass


class _KeyFilter(QObject):
    """Application-wide filter so Space works no matter which widget has focus."""

    def __init__(self, win):
        QObject.__init__(self, win)
        self.win = win

    def eventFilter(self, obj, ev):
        t = ev.type()
        if t == QEvent.Show and isinstance(obj, QDialog):
            _dark_title_bar(obj)  # message boxes, input dialogs, settings…
            return False
        if t not in (QEvent.KeyPress, QEvent.KeyRelease, QEvent.ShortcutOverride,
                     QEvent.MouseButtonPress):
            return False
        w = self.win
        if getattr(w, "page", 0) != 0:
            return False
        if QApplication.activeModalWidget() is not None or \
                QApplication.activePopupWidget() is not None or \
                QApplication.activeWindow() is not w:
            return False
        if t == QEvent.MouseButtonPress:
            if w.state == RUNNING:
                w.stop_solve()
                return True
            return False
        fw = QApplication.focusWidget()
        if isinstance(fw, (QLineEdit, QTextEdit, QPlainTextEdit, QAbstractSpinBox)) \
                and w.state == IDLE:
            return False
        if t == QEvent.ShortcutOverride:
            # while the timer is busy, keys must reach us instead of shortcuts
            if w.state != IDLE or ev.key() == Qt.Key_Space:
                ev.accept()
                return True
            return False
        if t == QEvent.KeyPress:
            return w.on_key_press(ev.key(), ev.isAutoRepeat())
        return w.on_key_release(ev.key(), ev.isAutoRepeat())


class MainWindow(QMainWindow):
    def __init__(self, store):
        QMainWindow.__init__(self)
        self.store = store
        self.settings = store.settings
        self.state = IDLE
        self.t_start = 0.0
        self.hold_start = 0.0
        self.insp_start = None
        self.insp_alerts_done = set()
        self.insp_penalty = OK
        self.arm_inspection = False
        self.scramble = ""
        self.stats = None
        self._loading = False
        self.page = 0
        self.training = None
        self.extra_windows = []
        self.hub = TrainingHub(store, self)

        self.setWindowTitle(tr("app_title"))
        icon_path = os.path.join(ASSETS, "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(1100, 680)
        self._build_ui()
        self._build_shortcuts()

        self.tick = QTimer(self)
        self.tick.setTimerType(Qt.PreciseTimer)
        self.tick.timeout.connect(self._on_tick)
        self.tick.start(15)

        self.key_filter = _KeyFilter(self)
        QApplication.instance().installEventFilter(self.key_filter)

        geo = self.settings.get("geometry")
        if geo:
            try:
                self.restoreGeometry(QByteArray.fromBase64(geo.encode("ascii")))
            except Exception:  # noqa: BLE001 - geometry is cosmetic
                pass
        else:
            self.resize(1280, 800)

        self.switch_session(self.store.current_id)

    # ==================================================================
    # UI construction
    # ==================================================================
    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 16, 24, 20)
        root.setSpacing(18)

        # ---- top bar -------------------------------------------------
        self.top_bar = QWidget()
        top = QHBoxLayout(self.top_bar)
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(2)
        logo = QLabel()
        pm = QPixmap(os.path.join(ASSETS, "header.png"))
        if not pm.isNull():
            pm.setDevicePixelRatio(2.0)   # header.png is drawn at 2x for sharp HiDPI
            logo.setPixmap(pm)
        logo.setCursor(Qt.PointingHandCursor)
        logo.setToolTip(tr("about"))
        logo.mousePressEvent = lambda e: self.show_about()
        top.addWidget(logo)
        top.addSpacing(16)
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        for i, key in enumerate(("nav_timer", "nav_training")):
            b = QPushButton(tr(key))
            b.setObjectName("nav")
            b.setCheckable(True)
            b.setChecked(i == 0)
            b.setFocusPolicy(Qt.NoFocus)
            self.nav_group.addButton(b, i)
            top.addWidget(b)
        self.nav_group.buttonClicked[int].connect(self.set_page)
        top.addStretch(1)
        self.puzzle_bar = QWidget()
        top_puzzles = QHBoxLayout(self.puzzle_bar)
        top_puzzles.setContentsMargins(0, 0, 0, 0)
        top_puzzles.setSpacing(2)
        top.addWidget(self.puzzle_bar)
        top_main = top
        top = top_puzzles

        self.puzzle_group = QButtonGroup(self)
        self.puzzle_group.setExclusive(True)
        self.puzzle_buttons = {}
        for i, (pid, label, name) in enumerate(scr.PUZZLES):
            if pid == "333oh":
                sep = QFrame()
                sep.setFixedSize(1, 22)
                sep.setStyleSheet("background: %s;" % theme.BORDER)
                top.addSpacing(4)
                top.addWidget(sep)
                top.addSpacing(4)
            b = QPushButton(label)
            b.setObjectName("puzzle")
            b.setCheckable(True)
            b.setToolTip(name)
            b.setFocusPolicy(Qt.NoFocus)
            self.puzzle_group.addButton(b, i)
            self.puzzle_buttons[pid] = b
            top.addWidget(b)
        self.puzzle_group.buttonClicked[int].connect(
            lambda i: self.select_puzzle(scr.PUZZLES[i][0]))
        top = top_main
        top.addSpacing(10)

        self.window_btn = QPushButton("⧉")
        self.window_btn.setObjectName("icon")
        self.window_btn.setToolTip(tr("new_window"))
        self.window_btn.setFocusPolicy(Qt.NoFocus)
        self.window_btn.clicked.connect(self.open_training_window)
        top.addWidget(self.window_btn)

        self.minimal_btn = QPushButton("◧")
        self.minimal_btn.setObjectName("icon")
        self.minimal_btn.setCheckable(True)
        self.minimal_btn.setChecked(bool(self.settings.get("minimal")))
        self.minimal_btn.setToolTip(tr("minimal_mode") + " (M)")
        self.minimal_btn.setFocusPolicy(Qt.NoFocus)
        self.minimal_btn.clicked.connect(self.toggle_minimal)
        top.addWidget(self.minimal_btn)

        gear = QPushButton("⚙")
        gear.setObjectName("icon")
        gear.setToolTip(tr("settings") + " (Ctrl+,)")
        gear.setFocusPolicy(Qt.NoFocus)
        gear.clicked.connect(self.open_settings)
        top.addWidget(gear)
        root.addWidget(self.top_bar)

        # ---- body ----------------------------------------------------
        self.pages = QStackedWidget()
        self.timer_page = QWidget()
        body = QHBoxLayout(self.timer_page)
        body.setContentsMargins(0, 0, 0, 0)
        self.pages.addWidget(self.timer_page)
        body.setSpacing(28)
        root.addWidget(self.pages, 1)

        # left: statistics + list of times
        self.left_panel = _panel()
        self.left_panel.setFixedWidth(300)
        lv = QVBoxLayout(self.left_panel)
        lv.setContentsMargins(16, 14, 12, 10)
        lv.setSpacing(8)
        sess_row = QHBoxLayout()
        sess_row.setSpacing(6)
        self.session_combo = QComboBox()
        self.session_combo.setFocusPolicy(Qt.NoFocus)
        self.session_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.session_combo.currentIndexChanged.connect(self._on_session_combo)
        sess_row.addWidget(self.session_combo, 1)
        menu_btn = QToolButton()
        menu_btn.setText("☰")
        menu_btn.setToolTip(tr("session"))
        menu_btn.setFocusPolicy(Qt.NoFocus)
        menu_btn.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu(menu_btn)
        menu.addAction(tr("new_session"), self.new_session)
        menu.addAction(tr("rename_session"), self.rename_session)
        menu.addAction(tr("delete_session"), self.delete_session)
        menu.addAction(tr("clear_session"), self.clear_session)
        menu.addSeparator()
        menu.addAction(tr("manual_entry") + "   Ctrl+E", self.manual_entry)
        menu.addSeparator()
        menu.addAction(tr("import_cstimer"), self.import_cstimer)
        menu.addAction(tr("export_csv"), self.export_csv)
        menu.addSeparator()
        menu.addAction(tr("settings"), self.open_settings)
        menu.addAction(tr("about"), self.show_about)
        menu_btn.setMenu(menu)
        sess_row.addWidget(menu_btn)
        lv.addLayout(sess_row)
        lv.addSpacing(4)
        self.stats_table = QTableWidget(len(STAT_ROWS), 3)
        self.stats_table.setHorizontalHeaderLabels(["", tr("current").upper(), tr("best").upper()])
        self._setup_table(self.stats_table)
        self.stats_table.verticalHeader().setDefaultSectionSize(28)
        self.stats_table.setFixedHeight(28 * len(STAT_ROWS) + 30)
        self.stats_table.cellClicked.connect(self._on_stat_clicked)
        for r, (label, _, _) in enumerate(STAT_ROWS):
            it = QTableWidgetItem(tr("single") if label == "single" else label)
            it.setForeground(self._qcolor(theme.MUTED))
            self.stats_table.setItem(r, 0, it)
        lv.addWidget(self.stats_table)
        self.summary = QLabel()
        self.summary.setObjectName("muted")
        lv.addWidget(self.summary)

        self.times_table = QTableWidget(0, 4)
        self.times_table.setHorizontalHeaderLabels(["#", tr("time").upper(), "AO5", "AO12"])
        self.times_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self._setup_table(self.times_table)
        self.times_table.verticalHeader().setDefaultSectionSize(26)
        self.times_table.cellClicked.connect(self._on_time_clicked)
        self.times_table.cellDoubleClicked.connect(self._on_time_double_clicked)
        self.times_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.times_table.customContextMenuRequested.connect(self._times_menu)
        lv.addWidget(self.times_table, 1)
        body.addWidget(self.left_panel)

        # centre: scramble, timer, penalty bar
        center = QVBoxLayout()
        center.setSpacing(10)
        body.addLayout(center, 1)

        self.scramble_panel = QWidget()
        sv = QHBoxLayout(self.scramble_panel)
        sv.setContentsMargins(40, 18, 0, 0)
        sv.setSpacing(8)
        self.scramble_label = QLabel()
        self.scramble_label.setObjectName("scramble")
        self.scramble_label.setWordWrap(True)
        self.scramble_label.setTextFormat(Qt.PlainText)
        self.scramble_label.setAlignment(Qt.AlignCenter)
        self.scramble_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.scramble_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sv.addWidget(self.scramble_label, 1)
        sbtns = QVBoxLayout()
        nb = QPushButton("↻")
        nb.setObjectName("icon")
        nb.setToolTip(tr("next_scramble"))
        nb.setFocusPolicy(Qt.NoFocus)
        nb.clicked.connect(self.new_scramble)
        cb = QPushButton("❐")
        cb.setObjectName("icon")
        cb.setToolTip(tr("copy_scramble"))
        cb.setFocusPolicy(Qt.NoFocus)
        cb.clicked.connect(self.copy_scramble)
        sbtns.addWidget(nb)
        sbtns.addWidget(cb)
        sbtns.addStretch(1)
        sv.addLayout(sbtns)
        center.addWidget(self.scramble_panel)

        self.timer_area = QWidget()
        ta = QVBoxLayout(self.timer_area)
        ta.setContentsMargins(0, 0, 0, 0)
        self.timer_display = TimerDisplay()
        self.timer_display.pressed.connect(lambda: self.on_key_press(Qt.Key_Space, False))
        self.timer_display.released.connect(lambda: self.on_key_release(Qt.Key_Space, False))
        ta.addWidget(self.timer_display, 1)
        center.addWidget(self.timer_area, 1)
        self.toast = Toast(self.timer_area)

        self.pen_bar = QWidget()
        pb = QHBoxLayout(self.pen_bar)
        pb.setContentsMargins(0, 0, 0, 0)
        pb.addStretch(1)
        self.pen_buttons = {}
        for label, val in ((tr("ok"), OK), (tr("plus2"), PLUS2), (tr("dnf"), DNF)):
            b = QPushButton(label)
            b.setObjectName("pen")
            b.setCheckable(True)
            b.setFocusPolicy(Qt.NoFocus)
            b.clicked.connect(lambda _=False, v=val: self.set_last_penalty(v))
            self.pen_buttons[val] = b
            pb.addWidget(b)
        cbtn = QPushButton("✎")
        cbtn.setObjectName("icon")
        cbtn.setToolTip(tr("comment"))
        cbtn.setFocusPolicy(Qt.NoFocus)
        cbtn.clicked.connect(self.comment_last)
        dbtn = QPushButton("✕")
        dbtn.setObjectName("icon")
        dbtn.setToolTip(tr("delete") + " (Ctrl+Z)")
        dbtn.setFocusPolicy(Qt.NoFocus)
        dbtn.clicked.connect(self.delete_last)
        pb.addWidget(cbtn)
        pb.addWidget(dbtn)
        pb.addStretch(1)
        center.addWidget(self.pen_bar)

        self.hint = QLabel()
        self.hint.setObjectName("muted")
        self.hint.setAlignment(Qt.AlignCenter)
        center.addWidget(self.hint)

        # right: preview + chart
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(340)
        rv = QVBoxLayout(self.right_panel)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(0)
        right_card = _panel()
        rc = QVBoxLayout(right_card)
        rc.setContentsMargins(0, 0, 0, 0)
        rc.setSpacing(0)
        rv.addWidget(right_card, 1)
        self.preview_panel = QWidget()
        pv = QVBoxLayout(self.preview_panel)
        pv.setContentsMargins(14, 14, 14, 6)
        self.preview = ScramblePreview()
        self.preview.setMinimumHeight(220)
        pv.addWidget(self.preview)
        rc.addWidget(self.preview_panel)
        self.chart_panel = QWidget()
        cv = QVBoxLayout(self.chart_panel)
        cv.setContentsMargins(8, 4, 10, 10)
        cv.setSpacing(0)
        tabs = QHBoxLayout()
        tabs.setSpacing(2)
        self.chart_tabs = QButtonGroup(self)
        self.chart_tabs.setExclusive(True)
        for idx, key in enumerate(("tab_progress", "tab_distribution")):
            b = QPushButton(tr(key).upper())
            b.setObjectName("tab")
            b.setCheckable(True)
            b.setFocusPolicy(Qt.NoFocus)
            b.setChecked(idx == 0)
            self.chart_tabs.addButton(b, idx)
            tabs.addWidget(b)
        tabs.addStretch(1)
        cv.addLayout(tabs)
        self.chart_stack = QStackedWidget()
        self.chart = TimeChart()
        self.histogram = TimeHistogram()
        self.chart_stack.addWidget(self.chart)
        self.chart_stack.addWidget(self.histogram)
        self.chart_tabs.buttonClicked[int].connect(self.chart_stack.setCurrentIndex)
        cv.addWidget(self.chart_stack, 1)
        rc.addWidget(self.chart_panel, 1)
        body.addWidget(self.right_panel)
        self._apply_visibility()

    def _setup_table(self, t):
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setSelectionMode(QAbstractItemView.NoSelection)
        t.setFocusPolicy(Qt.NoFocus)
        t.verticalHeader().setVisible(False)
        t.setShowGrid(False)
        t.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        h = t.horizontalHeader()
        h.setSectionResizeMode(QHeaderView.Stretch)
        h.setHighlightSections(False)
        t.setCursor(Qt.PointingHandCursor)

    @staticmethod
    def _qcolor(c):
        return QColor(c)

    def _build_shortcuts(self):
        def sc(seq, fn):
            s = QShortcut(QKeySequence(seq), self)
            s.setContext(Qt.WindowShortcut)
            s.activated.connect(fn)
            return s

        sc("Ctrl+1", lambda: self.set_last_penalty(OK))
        sc("Ctrl+2", lambda: self.set_last_penalty(PLUS2))
        sc("Ctrl+3", lambda: self.set_last_penalty(DNF))
        sc("Ctrl+Z", self.delete_last)
        sc("N", self.new_scramble)
        sc("Ctrl+E", self.manual_entry)
        sc("Ctrl+,", self.open_settings)
        sc("M", self.toggle_minimal)

    def _apply_visibility(self):
        st = self.state
        busy = st in (INSPECTING, HOLDING, READY, RUNNING)
        # Holding Space without inspection keeps the UI visible (red/green
        # colour feedback); once the timer is armed or running, focus mode
        # hides everything but the time.
        focus_state = st in (INSPECTING, READY, RUNNING) or \
            (st == HOLDING and self.insp_start is not None)
        show = not (self.settings.get("focus_mode") and focus_state)
        self.top_bar.setVisible(show)
        minimal = bool(self.settings.get("minimal"))
        self.left_panel.setVisible(show and not minimal)
        self.scramble_panel.setVisible(show)
        self.pen_bar.setVisible(show and not busy and self._current_solves_count() > 0)
        self.hint.setVisible(show and not busy and self._current_solves_count() == 0)
        want_preview = bool(self.settings.get("show_preview"))
        want_chart = bool(self.settings.get("show_chart"))
        self.right_panel.setVisible(show and not minimal and (want_preview or want_chart))
        self.preview_panel.setVisible(want_preview)
        self.chart_panel.setVisible(want_chart)

    def _current_solves_count(self):
        s = self.store.current
        return len(s.solves) if s else 0

    # ==================================================================
    # Sessions & puzzles
    # ==================================================================
    @property
    def session(self):
        return self.store.current

    def select_puzzle(self, pid):
        if self.session and self.session.puzzle == pid:
            return
        existing = self.store.sessions_for(pid)
        if existing:
            target = existing[-1]
        else:
            target = self.store.new_session(scr.PUZZLE_LABEL[pid], pid)
        self.switch_session(target.id)

    def switch_session(self, sid):
        self.store.current_id = sid
        sess = self.session
        if sess is None:
            return
        self._loading = True
        btn = self.puzzle_buttons.get(sess.puzzle)
        if btn:
            btn.setChecked(True)
        self.session_combo.clear()
        for s in self.store.sessions_for(sess.puzzle):
            self.session_combo.addItem(s.name, s.id)
        idx = self.session_combo.findData(sid)
        self.session_combo.setCurrentIndex(max(0, idx))
        self._loading = False
        self.cancel_timer()
        self.new_scramble()
        self.refresh()
        self.save()

    def _on_session_combo(self, idx):
        if self._loading or idx < 0:
            return
        sid = self.session_combo.itemData(idx)
        if sid and sid != self.store.current_id:
            self.switch_session(sid)

    def new_session(self):
        pid = self.session.puzzle if self.session else "333"
        default = "%s #%d" % (scr.PUZZLE_LABEL[pid], len(self.store.sessions_for(pid)) + 1)
        name, ok = QInputDialog.getText(self, tr("new_session"), tr("session_name"),
                                        QLineEdit.Normal, default)
        if ok and name.strip():
            s = self.store.new_session(name.strip(), pid)
            self.switch_session(s.id)

    def rename_session(self):
        s = self.session
        name, ok = QInputDialog.getText(self, tr("rename_session"), tr("session_name"),
                                        QLineEdit.Normal, s.name)
        if ok and name.strip():
            s.name = name.strip()
            self.switch_session(s.id)

    def delete_session(self):
        s = self.session
        if QMessageBox.question(self, tr("delete_session"),
                                tr("confirm_delete_session") % (s.name, len(s.solves))) \
                != QMessageBox.Yes:
            return
        pid = s.puzzle
        self.store.delete_session(s.id)
        rest = self.store.sessions_for(pid)
        self.switch_session(rest[-1].id if rest else self.store.current_id)

    def clear_session(self):
        s = self.session
        if not s.solves:
            return
        if QMessageBox.question(self, tr("clear_session"),
                                tr("confirm_clear") % len(s.solves)) != QMessageBox.Yes:
            return
        s.solves = []
        self.refresh()
        self.save()

    # ==================================================================
    # Scrambles
    # ==================================================================
    def new_scramble(self, force=False):
        if getattr(self, "page", 0) != 0 and force is not True and self.scramble:
            return
        if self.state != IDLE and force is not True:
            return
        puzzle = self.session.puzzle
        self.scramble = scr.generate(puzzle)
        self.scramble_label.setText(self.scramble)
        size = {"444": 19, "555": 17, "666": 15, "777": 14, "minx": 15,
                "333fm": 20}.get(puzzle, 23)
        self.scramble_label.setStyleSheet(
            "font-size: %dpx; font-weight: 500; color: %s;" % (size, theme.SCRAMBLE))
        self.preview.set_scramble(puzzle, self.scramble)

    def copy_scramble(self):
        QApplication.clipboard().setText(self.scramble)
        self.toast.show_message(tr("copied"), 1200)

    # ==================================================================
    # Timer state machine
    # ==================================================================
    def on_key_press(self, key, auto_repeat):
        if self.state == RUNNING:
            if not auto_repeat:
                self.stop_solve()
            return True
        if self.state == STOPPED:
            if auto_repeat:
                return True
            self.state = IDLE  # the release of the stopping key was lost
        if key == Qt.Key_Escape and self.state in (INSPECTING, HOLDING, READY):
            self.cancel_timer()
            return True
        if key != Qt.Key_Space:
            return False
        if auto_repeat:
            return True
        if self.state == IDLE:
            if self.settings.get("inspection"):
                self.arm_inspection = True
            else:
                self._begin_hold()
        elif self.state == INSPECTING:
            self._begin_hold()
        return True

    def on_key_release(self, key, auto_repeat):
        if auto_repeat:
            return key == Qt.Key_Space or self.state != IDLE
        if self.state == STOPPED:
            self.state = IDLE
            self._apply_visibility()
            self._render()
            return True
        if key != Qt.Key_Space:
            return self.state != IDLE
        if self.state == IDLE and self.arm_inspection:
            self.arm_inspection = False
            self._start_inspection()
        elif self.state == HOLDING:
            self.state = INSPECTING if self.insp_start is not None else IDLE
            self._apply_visibility()
            self._render()
        elif self.state == READY:
            self.start_solve()
        return True

    def _begin_hold(self):
        self.hold_start = time.perf_counter()
        self.state = HOLDING
        if int(self.settings.get("hold_ms", 300)) <= 0:
            self.state = READY
        self._apply_visibility()
        self._render()

    def _start_inspection(self):
        self.insp_start = time.perf_counter()
        self.insp_alerts_done = set()
        self.state = INSPECTING
        self._apply_visibility()
        self._render()

    def start_solve(self):
        self.insp_penalty = OK
        if self.insp_start is not None:
            used = time.perf_counter() - self.insp_start
            if used > INSPECTION_S + 2:
                self.insp_penalty = DNF
            elif used > INSPECTION_S:
                self.insp_penalty = PLUS2
        self.insp_start = None
        self.t_start = time.perf_counter()
        self.state = RUNNING
        self._apply_visibility()
        self._render()

    def stop_solve(self):
        elapsed_ms = int((time.perf_counter() - self.t_start) * 1000)
        self.state = STOPPED
        solve = Solve(elapsed_ms, self.insp_penalty, self.scramble)
        self.insp_penalty = OK
        self._add_solve(solve)
        self.new_scramble(force=True)
        self._apply_visibility()

    def cancel_timer(self):
        self.state = IDLE
        self.insp_start = None
        self.arm_inspection = False
        self.insp_penalty = OK
        self._apply_visibility()
        self._render()

    def _on_tick(self):
        if self.state == HOLDING:
            if (time.perf_counter() - self.hold_start) * 1000 >= int(self.settings.get("hold_ms", 300)):
                self.state = READY
        if self.insp_start is not None and self.state in (INSPECTING, HOLDING, READY):
            used = time.perf_counter() - self.insp_start
            if self.settings.get("inspection_alerts"):
                for mark in (8, 12):
                    if used >= mark and mark not in self.insp_alerts_done:
                        self.insp_alerts_done.add(mark)
                        QApplication.beep()
        if self.state != IDLE:
            self._render()

    def _render(self):
        d = int(self.settings.get("decimals", 2))
        st = self.state
        if st == RUNNING:
            ms = int((time.perf_counter() - self.t_start) * 1000)
            mode = self.settings.get("update_mode", "full")
            if mode == "hidden":
                text = tr("solving")
            elif mode == "seconds":
                text = fmt_ms(ms, 2).split(".")[0]
            elif mode == "tenths":
                text = fmt_ms(ms, 1)
            else:
                text = fmt_ms(ms, d)
            self.timer_display.set_display(text, theme.TEXT)
            return
        if self.insp_start is not None and st in (INSPECTING, HOLDING, READY):
            used = time.perf_counter() - self.insp_start
            left = INSPECTION_S - used
            if left > 0:
                text = str(int(left) + 1)
            elif left > -2:
                text = "+2"
            else:
                text = "DNF"
            color = {HOLDING: theme.HOLD, READY: theme.READY}.get(st, theme.INSPECT)
            self.timer_display.set_display(text, color, tr("inspection"))
            return
        if st == HOLDING:
            self.timer_display.set_display(self._last_text(d), theme.HOLD)
            return
        if st == READY:
            self.timer_display.set_display(fmt_ms(0, d), theme.READY)
            return
        self.timer_display.set_display(self._last_text(d), theme.TEXT, self._last_sub())
        self.hint.setText(tr("inspect_hint") if self.settings.get("inspection") else tr("ready_hint"))

    def _last_text(self, d):
        s = self.session
        if s and s.solves:
            return fmt_solve(s.solves[-1], d)
        return fmt_ms(0, d)

    def _last_sub(self):
        if not self.stats or self.stats.count == 0:
            return ""
        parts = []
        for label in ("ao5", "ao12"):
            v = self.stats.rows[label]["current"]
            if v is not None:
                parts.append("%s  %s" % (label, fmt_avg(v, int(self.settings.get("decimals", 2)))))
        return "     ".join(parts)

    # ==================================================================
    # Solves
    # ==================================================================
    def _add_solve(self, solve):
        sess = self.session
        old = self.stats
        sess.solves.append(solve)
        self.refresh()
        self.save()
        self._check_pb(old)

    def _check_pb(self, old):
        if old is None or self.stats is None:
            return
        d = int(self.settings.get("decimals", 2))
        for label in ("ao100", "ao50", "ao12", "ao5", "single"):
            new_row = self.stats.rows[label]
            old_best = old.rows[label]["best"]
            cur = new_row["current"]
            if cur is None or cur == INF or old_best is None:
                continue
            if cur < old_best:
                name = tr("single") if label == "single" else label
                val = fmt_ms(cur, d) if label == "single" else fmt_avg(cur, d)
                self.toast.show_message(tr("new_pb") % (name, val), 3500)
                return

    def set_last_penalty(self, pen):
        if self.state != IDLE or not self.session.solves:
            return
        self.session.solves[-1].penalty = pen
        self.refresh()
        self.save()

    def delete_last(self):
        if self.state != IDLE or not self.session.solves:
            return
        s = self.session.solves[-1]
        if QMessageBox.question(self, tr("delete"),
                                tr("confirm_delete_solve") % fmt_solve(s)) != QMessageBox.Yes:
            return
        self.session.solves.pop()
        self.refresh()
        self.save()

    def comment_last(self):
        if not self.session.solves:
            return
        s = self.session.solves[-1]
        text, ok = QInputDialog.getText(self, tr("comment"), tr("comment_prompt"),
                                        QLineEdit.Normal, s.comment)
        if ok:
            s.comment = text.strip()
            self.refresh()
            self.save()

    def manual_entry(self):
        if self.state != IDLE:
            return
        text, ok = QInputDialog.getText(self, tr("manual_entry"), tr("enter_time"))
        if not ok or not text.strip():
            return
        try:
            ms, pen = parse_time(text)
        except ValueError:
            QMessageBox.warning(self, tr("manual_entry"), tr("bad_time"))
            return
        self._add_solve(Solve(ms, pen, self.scramble))
        self.new_scramble()

    def open_solve(self, index):
        solves = self.session.solves
        if not (0 <= index < len(solves)):
            return
        dlg = SolveDialog(solves[index], index + 1, int(self.settings.get("decimals", 2)), self)
        dlg.exec_()
        if dlg.deleted:
            del solves[index]
        self.refresh()
        self.save()

    # ==================================================================
    # Tables
    # ==================================================================
    def refresh(self):
        sess = self.session
        self.stats = SessionStats(sess.solves)
        st = self.stats
        d = int(self.settings.get("decimals", 2))

        # stats panel
        for r, (label, _size, kind) in enumerate(STAT_ROWS):
            row = st.rows[label]
            fmt = (lambda v: fmt_ms(v, d)) if kind == "single" else (lambda v: fmt_avg(v, d))
            cur = QTableWidgetItem(fmt(row["current"]) if row["current"] is not None else "-")
            best = QTableWidgetItem(fmt(row["best"]) if row["best"] is not None else "-")
            best.setForeground(self._qcolor(theme.ACCENT))
            self.stats_table.setItem(r, 1, cur)
            self.stats_table.setItem(r, 2, best)
        mean = fmt_avg(st.session_mean, d) if st.session_mean is not None else "-"
        sd = fmt_avg(st.std_dev, d) if st.std_dev is not None else "-"
        self.summary.setText("%s: %d%s     %s: %s     %s: %s" % (
            tr("solves"), st.count - st.dnf_count,
            ("/%d" % st.count) if st.dnf_count else "", tr("mean"), mean, tr("sd"), sd))

        # times list (newest first)
        n = len(sess.solves)
        t = self.times_table
        t.setUpdatesEnabled(False)
        t.setRowCount(n)
        best_i = st.rows["single"]["best_index"]
        ao5 = st.series["ao5"]
        ao12 = st.series["ao12"]
        for row in range(n):
            i = n - 1 - row
            s = sess.solves[i]
            cells = [str(i + 1), fmt_solve(s, d),
                     fmt_avg(ao5[i], d) if ao5[i] is not None else "",
                     fmt_avg(ao12[i], d) if ao12[i] is not None else ""]
            for c, txt in enumerate(cells):
                it = QTableWidgetItem(txt)
                it.setData(Qt.UserRole, i)
                if c == 0:
                    it.setForeground(self._qcolor(theme.MUTED))
                elif c == 1:
                    if i == best_i:
                        it.setForeground(self._qcolor(theme.ACCENT))
                    elif s.penalty == DNF:
                        it.setForeground(self._qcolor(theme.DNF_RED))
                    if s.comment:
                        it.setToolTip(s.comment)
                        it.setText(txt + "  •")
                t.setItem(row, c, it)
        t.setUpdatesEnabled(True)

        # chart
        self.chart.set_data(st.values, ao5, ao12, d)
        self.histogram.set_data(st.values)

        # penalty bar
        last = sess.solves[-1] if sess.solves else None
        for val, b in self.pen_buttons.items():
            b.setChecked(bool(last) and last.penalty == val)
        self._apply_visibility()
        self._render()

    def _row_index(self, row):
        it = self.times_table.item(row, 0)
        return it.data(Qt.UserRole) if it is not None else None

    def _on_time_clicked(self, row, col):
        i = self._row_index(row)
        if i is None:
            return
        if col == 2 and self.stats.series["ao5"][i] is not None:
            self.show_average(5, i)
        elif col == 3 and self.stats.series["ao12"][i] is not None:
            self.show_average(12, i)

    def _on_time_double_clicked(self, row, col):
        if col in (0, 1):
            i = self._row_index(row)
            if i is not None:
                self.open_solve(i)

    def _times_menu(self, pos):
        row = self.times_table.rowAt(pos.y())
        if row < 0:
            return
        i = self._row_index(row)
        s = self.session.solves[i]
        m = QMenu(self)
        for label, val in ((tr("ok"), OK), (tr("plus2"), PLUS2), (tr("dnf"), DNF)):
            a = QAction(label, m)
            a.setCheckable(True)
            a.setChecked(s.penalty == val)
            a.triggered.connect(lambda _=False, v=val: self._set_penalty(i, v))
            m.addAction(a)
        m.addSeparator()
        m.addAction(tr("comment") + "…", lambda: self.open_solve(i))
        m.addAction(tr("copy_scramble_menu"),
                    lambda: QApplication.clipboard().setText(s.scramble))
        m.addSeparator()
        m.addAction(tr("delete"), lambda: self._delete_index(i))
        m.exec_(self.times_table.viewport().mapToGlobal(pos))

    def _set_penalty(self, i, pen):
        self.session.solves[i].penalty = pen
        self.refresh()
        self.save()

    def _delete_index(self, i):
        s = self.session.solves[i]
        if QMessageBox.question(self, tr("delete"),
                                tr("confirm_delete_solve") % fmt_solve(s)) == QMessageBox.Yes:
            del self.session.solves[i]
            self.refresh()
            self.save()

    def _on_stat_clicked(self, row, col):
        if col not in (1, 2) or not self.stats:
            return
        label, size, kind = STAT_ROWS[row]
        info = self.stats.rows[label]
        if col == 1:
            end = self.stats.count - 1 if info["current"] is not None else None
        else:
            end = info["best_index"]
        if end is None:
            return
        if kind == "single":
            self.open_solve(end)
        else:
            self.show_average(size, end, mean=(kind == "mean"))

    def show_average(self, size, end, mean=False):
        """Show the breakdown of the average of `size` solves ending at `end`."""
        d = int(self.settings.get("decimals", 2))
        solves = self.session.solves[end - size + 1:end + 1]
        if len(solves) < size:
            return
        values = [s.value for s in solves]
        label = ("mo%d" if mean else "ao%d") % size
        avg = stats_mean(values) if mean else stats_average(values)
        trimmed = set() if mean else trimmed_indices(values)
        lines = ["%s: %s" % (label, fmt_avg(avg, d)), ""]
        for k, s in enumerate(solves):
            t = fmt_solve(s, d)
            if k in trimmed:
                t = "(%s)" % t
            line = "%d. %-12s %s" % (end - size + 2 + k, t, s.scramble.replace("\n", " "))
            if s.comment:
                line += "   // " + s.comment
            lines.append(line)
        TextDialog(label, "\n".join(lines), self).exec_()

    # ==================================================================
    # Import / export / settings
    # ==================================================================
    def import_cstimer(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("import_cstimer"), "",
                                              "csTimer export (*.txt *.json);;All files (*)")
        if not path:
            return
        try:
            sessions = storage.import_cstimer(path)
        except Exception as e:  # noqa: BLE001 - show any parse error to the user
            QMessageBox.warning(self, tr("import_cstimer"), tr("import_failed") % e)
            return
        total = 0
        for s in sessions:
            self.store.sessions.append(s)
            total += len(s.solves)
        if sessions:
            self.switch_session(sessions[0].id)
        QMessageBox.information(self, tr("import_cstimer"),
                                tr("imported") % (len(sessions), total))

    def export_csv(self):
        s = self.session
        default = os.path.join(os.path.expanduser("~"), "%s.csv" % s.name.replace(" ", "_"))
        path, _ = QFileDialog.getSaveFileName(self, tr("export_csv"), default, "CSV (*.csv)")
        if not path:
            return
        storage.export_csv(s, path, int(self.settings.get("decimals", 2)))
        self.toast.show_message(tr("exported") % os.path.basename(path), 2500)

    def set_page(self, idx):
        if self.state != IDLE:
            self.nav_group.button(self.page).setChecked(True)
            return
        if idx == 1 and self.training is None:
            self.training = TrainingWidget(self.hub)
            self.pages.addWidget(self.training)
        self.page = idx
        self.pages.setCurrentIndex(idx)
        self.puzzle_bar.setVisible(idx == 0)
        self.minimal_btn.setVisible(idx == 0)
        b = self.nav_group.button(idx)
        if b and not b.isChecked():
            b.setChecked(True)

    def open_training_window(self):
        win = TrainingWindow(self.hub, self.windowIcon())
        self.extra_windows.append(win)
        win.destroyed.connect(lambda *_: self.extra_windows.remove(win)
                              if win in self.extra_windows else None)
        geo = self.geometry()
        win.move(geo.x() + 60, geo.y() + 40)
        win.show()

    def toggle_minimal(self):
        if self.state != IDLE or self.page != 0:
            return
        self.settings["minimal"] = not self.settings.get("minimal")
        self.minimal_btn.setChecked(bool(self.settings["minimal"]))
        self._apply_visibility()
        self.save()

    def showEvent(self, e):
        QMainWindow.showEvent(self, e)
        if not getattr(self, "_dark_title", False):
            self._dark_title = True
            _dark_title_bar(self)

    def show_about(self):
        if self.state == IDLE:
            AboutDialog(os.path.join(ASSETS, "logo_full.png"), self).exec_()

    def open_settings(self):
        if self.state != IDLE:
            return
        old_lang = self.settings.get("language")
        dlg = SettingsDialog(self.settings, self)
        if dlg.exec_():
            self.settings.update(dlg.settings)
            self.save()
            if self.settings.get("language") != old_lang:
                QMessageBox.information(self, tr("settings"), tr("restart_needed"))
            self.cancel_timer()
            self.refresh()

    # ==================================================================
    def save(self):
        try:
            self.store.save()
        except (IOError, OSError) as e:
            self.toast.show_message("Save error: %s" % e, 5000)

    def resizeEvent(self, e):
        QMainWindow.resizeEvent(self, e)
        if self.toast.isVisible():
            self.toast.move(int((self.timer_area.width() - self.toast.width()) / 2), 14)

    def closeEvent(self, e):
        for w in list(self.extra_windows):
            w.close()
        self.settings["geometry"] = self.saveGeometry().toBase64().data().decode("ascii")
        self.save()
        QMainWindow.closeEvent(self, e)
