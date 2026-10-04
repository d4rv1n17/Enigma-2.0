"""Dialogs: settings, solve details, average details."""

import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
                             QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPlainTextEdit, QPushButton, QSlider, QVBoxLayout)

from . import VERSION, theme
from .i18n import tr
from .stats import OK, PLUS2, DNF, fmt_solve


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(tr("settings"))
        self.setMinimumWidth(460)
        self.settings = dict(settings)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 20, 22, 18)
        lay.setSpacing(12)

        self.cb_insp = QCheckBox(tr("s_inspection"))
        self.cb_insp.setChecked(bool(settings.get("inspection")))
        self.cb_alerts = QCheckBox(tr("s_alerts"))
        self.cb_alerts.setChecked(bool(settings.get("inspection_alerts")))
        self.cb_focus = QCheckBox(tr("s_focus"))
        self.cb_focus.setChecked(bool(settings.get("focus_mode")))
        self.cb_preview = QCheckBox(tr("s_preview"))
        self.cb_preview.setChecked(bool(settings.get("show_preview")))
        self.cb_chart = QCheckBox(tr("s_chart"))
        self.cb_chart.setChecked(bool(settings.get("show_chart")))
        for w in (self.cb_insp, self.cb_alerts, self.cb_focus, self.cb_preview, self.cb_chart):
            lay.addWidget(w)
        self.cb_insp.toggled.connect(self.cb_alerts.setEnabled)
        self.cb_alerts.setEnabled(self.cb_insp.isChecked())

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        hold_row = QHBoxLayout()
        self.sl_hold = QSlider(Qt.Horizontal)
        self.sl_hold.setRange(0, 10)  # x100 ms
        self.sl_hold.setValue(int(settings.get("hold_ms", 300)) // 100)
        self.lb_hold = QLabel()
        self.lb_hold.setMinimumWidth(56)
        self.sl_hold.valueChanged.connect(self._hold_changed)
        self._hold_changed(self.sl_hold.value())
        hold_row.addWidget(self.sl_hold, 1)
        hold_row.addWidget(self.lb_hold)
        form.addRow(tr("s_hold"), hold_row)

        self.cmb_update = QComboBox()
        for key in ("full", "tenths", "seconds", "hidden"):
            self.cmb_update.addItem(tr("u_" + key), key)
        self._select(self.cmb_update, settings.get("update_mode", "full"))
        form.addRow(tr("s_update"), self.cmb_update)

        self.cmb_dec = QComboBox()
        for d in (2, 3):
            self.cmb_dec.addItem(str(d), d)
        self._select(self.cmb_dec, int(settings.get("decimals", 2)))
        form.addRow(tr("s_decimals"), self.cmb_dec)

        self.cmb_lang = QComboBox()
        self.cmb_lang.addItem(tr("lang_auto"), "")
        self.cmb_lang.addItem("English", "en")
        self.cmb_lang.addItem("Русский", "ru")
        self._select(self.cmb_lang, settings.get("language") or "")
        form.addRow(tr("s_language"), self.cmb_lang)
        lay.addLayout(form)

        title = QLabel(tr("shortcuts").upper())
        title.setObjectName("sectionTitle")
        lay.addSpacing(6)
        lay.addWidget(title)
        sc = QLabel(tr("shortcuts_text"))
        sc.setObjectName("muted")
        sc.setWordWrap(True)
        lay.addWidget(sc)

        btns = QHBoxLayout()
        btns.addStretch(1)
        cancel = QPushButton(tr("close"))
        ok = QPushButton("OK")
        ok.setDefault(True)
        cancel.clicked.connect(self.reject)
        ok.clicked.connect(self._accept)
        btns.addWidget(cancel)
        btns.addWidget(ok)
        lay.addLayout(btns)

    @staticmethod
    def _select(combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return

    def _hold_changed(self, v):
        self.lb_hold.setText("%.1f s" % (v / 10.0))

    def _accept(self):
        s = self.settings
        s["inspection"] = self.cb_insp.isChecked()
        s["inspection_alerts"] = self.cb_alerts.isChecked()
        s["focus_mode"] = self.cb_focus.isChecked()
        s["show_preview"] = self.cb_preview.isChecked()
        s["show_chart"] = self.cb_chart.isChecked()
        s["hold_ms"] = self.sl_hold.value() * 100
        s["update_mode"] = self.cmb_update.currentData()
        s["decimals"] = self.cmb_dec.currentData()
        s["language"] = self.cmb_lang.currentData() or None
        self.accept()


class SolveDialog(QDialog):
    """Shows one solve; lets the user change penalty, comment or delete it."""

    def __init__(self, solve, number, decimals, parent=None):
        QDialog.__init__(self, parent)
        self.solve = solve
        self.deleted = False
        self.decimals = decimals
        self.setWindowTitle(tr("solve_n") % number)
        self.setMinimumWidth(520)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 20, 22, 18)
        lay.setSpacing(10)

        self.lb_time = QLabel()
        self.lb_time.setStyleSheet("font-size: 40px; font-weight: 700; color: %s;" % theme.ACCENT)
        lay.addWidget(self.lb_time)
        date = QLabel(time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(solve.date)))
        date.setObjectName("muted")
        lay.addWidget(date)

        pen_row = QHBoxLayout()
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)
        # button ids must be >= 0 (Qt treats -1 as "assign automatically")
        self._pen_values = [OK, PLUS2, DNF]
        for idx, (label, val) in enumerate(((tr("ok"), OK), (tr("plus2"), PLUS2),
                                            (tr("dnf"), DNF))):
            b = QPushButton(label)
            b.setObjectName("pen")
            b.setCheckable(True)
            b.setChecked(solve.penalty == val)
            self.group.addButton(b, idx)
            pen_row.addWidget(b)
        pen_row.addStretch(1)
        self.group.buttonClicked[int].connect(self._set_penalty)
        lay.addLayout(pen_row)

        t = QLabel(tr("scramble").upper())
        t.setObjectName("sectionTitle")
        lay.addWidget(t)
        scr = QLabel(solve.scramble or "-")
        scr.setWordWrap(True)
        scr.setTextInteractionFlags(Qt.TextSelectableByMouse)
        scr.setStyleSheet("font-size: 16px;")
        lay.addWidget(scr)

        t2 = QLabel(tr("comment").upper())
        t2.setObjectName("sectionTitle")
        lay.addWidget(t2)
        self.ed_comment = QLineEdit(solve.comment)
        lay.addWidget(self.ed_comment)

        btns = QHBoxLayout()
        delete = QPushButton(tr("delete"))
        delete.setStyleSheet("color: %s;" % theme.DNF_RED)
        delete.clicked.connect(self._delete)
        copy = QPushButton(tr("copy"))
        copy.clicked.connect(self._copy)
        close = QPushButton(tr("close"))
        close.setDefault(True)
        close.clicked.connect(self.accept)
        btns.addWidget(delete)
        btns.addStretch(1)
        btns.addWidget(copy)
        btns.addWidget(close)
        lay.addLayout(btns)
        self._refresh()

    def _refresh(self):
        self.lb_time.setText(fmt_solve(self.solve, self.decimals))

    def _set_penalty(self, idx):
        self.solve.penalty = self._pen_values[idx]
        self._refresh()

    def _copy(self):
        QApplication.clipboard().setText("%s   %s" % (fmt_solve(self.solve, self.decimals),
                                                      self.solve.scramble))

    def _delete(self):
        self.deleted = True
        self.accept()

    def accept(self):
        self.solve.comment = self.ed_comment.text().strip()
        QDialog.accept(self)


class TextDialog(QDialog):
    """Read-only text (average breakdown) with a copy button."""

    def __init__(self, title, text, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.resize(620, 420)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 14)
        ed = QPlainTextEdit(text)
        ed.setReadOnly(True)
        mono = theme.mono_font()
        if mono:
            ed.setStyleSheet('font-family: "%s"; font-size: 14px;' % mono)
        lay.addWidget(ed)
        row = QHBoxLayout()
        row.addStretch(1)
        copy = QPushButton(tr("copy"))
        copy.clicked.connect(lambda: QApplication.clipboard().setText(text))
        close = QPushButton(tr("close"))
        close.setDefault(True)
        close.clicked.connect(self.accept)
        row.addWidget(copy)
        row.addWidget(close)
        lay.addLayout(row)


class AboutDialog(QDialog):
    def __init__(self, logo_path, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(tr("about"))
        self.setFixedWidth(420)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 20)
        lay.setSpacing(10)
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        pm = QPixmap(logo_path)
        if not pm.isNull():
            logo.setPixmap(pm.scaledToWidth(260, Qt.SmoothTransformation))
        logo.setStyleSheet("background: %s; border-radius: 16px;" % theme.BG)
        lay.addWidget(logo)
        ver = QLabel("Enigma Cube Timer %s" % VERSION)
        ver.setAlignment(Qt.AlignCenter)
        ver.setStyleSheet("font-size: 16px; font-weight: 700;")
        lay.addWidget(ver)
        txt = QLabel(tr("about_text"))
        txt.setObjectName("muted")
        txt.setWordWrap(True)
        txt.setAlignment(Qt.AlignCenter)
        lay.addWidget(txt)
        close = QPushButton(tr("close"))
        close.setDefault(True)
        close.clicked.connect(self.accept)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(close)
        row.addStretch(1)
        lay.addLayout(row)
