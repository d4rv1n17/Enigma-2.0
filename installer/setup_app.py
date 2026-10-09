# -*- coding: utf-8 -*-
"""Enigma Cube Setup - a small custom installer window (PyQt5).

    EnigmaCube-Setup.exe               install or update
    uninstall.exe --uninstall          remove (Settings -> Apps calls this)
    ... --quiet                        no window (used by Windows for quiet removal)
"""

import os
import shutil
import subprocess
import sys
import tempfile

from PyQt5.QtCore import QLocale, QPoint, QRectF, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QFileDialog, QFrame,
                             QHBoxLayout, QLabel, QLineEdit, QProgressBar, QPushButton,
                             QStackedWidget, QVBoxLayout, QWidget)

try:  # imported from the app (EnigmaCube.exe --uninstall)
    from . import setup_core as core
except ImportError:  # run as the setup script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import setup_core as core  # noqa: E402

ACCENT = "#f4cc0c"

T = {
    "setup": ("Setup", "Установка"),
    "window": ("Enigma Cube Setup", "Установка Enigma Cube"),
    "install_title": ("Install Enigma Cube %s", "Установить Enigma Cube %s"),
    "update_title": ("Update Enigma Cube to %s", "Обновить Enigma Cube до %s"),
    "reinstall_title": ("Reinstall Enigma Cube %s", "Переустановить Enigma Cube %s"),
    "tagline": ("Speedcubing timer with WCA scrambles, statistics and algorithm training.",
                "Таймер для спидкубинга: скрамблы WCA, статистика и тренировка алгоритмов."),
    "location": ("Install location", "Папка установки"),
    "change": ("Change…", "Изменить…"),
    "desktop": ("Desktop shortcut", "Ярлык на рабочем столе"),
    "launch": ("Launch after setup", "Запустить после установки"),
    "needs": ("Needs about %d MB. No administrator rights required: it installs just for you.",
              "Нужно около %d МБ. Права администратора не нужны: программа ставится только для вас."),
    "keeps": ("Your solves and settings are kept.", "Ваши сборки и настройки сохранятся."),
    "cancel": ("Cancel", "Отмена"),
    "install": ("Install", "Установить"),
    "update": ("Update", "Обновить"),
    "installing": ("Installing Enigma Cube…", "Устанавливаем Enigma Cube…"),
    "updating": ("Updating Enigma Cube…", "Обновляем Enigma Cube…"),
    "preparing": ("Preparing…", "Подготовка…"),
    "done_title": ("Enigma Cube is ready", "Enigma Cube установлен"),
    "done_sub": ("Find it in the Start menu%s.", "Ищите его в меню «Пуск»%s."),
    "done_desktop": (" and on your desktop", " и на рабочем столе"),
    "finish": ("Finish", "Готово"),
    "error_title": ("Something went wrong", "Что-то пошло не так"),
    "retry": ("Try again", "Повторить"),
    "close": ("Close", "Закрыть"),
    "remove_title": ("Remove Enigma Cube", "Удалить Enigma Cube"),
    "remove_sub": ("The program will be removed from this computer.",
                   "Программа будет удалена с этого компьютера."),
    "delete_data": ("Also delete my solves and settings", "Удалить также мои сборки и настройки"),
    "data_kept": ("Your solves stay on this computer unless you tick the box.",
                  "Ваши сборки останутся на компьютере, если не отметить галочку."),
    "remove": ("Remove", "Удалить"),
    "removing": ("Removing Enigma Cube…", "Удаляем Enigma Cube…"),
    "removed": ("Enigma Cube was removed", "Enigma Cube удалён"),
    "removed_sub": ("Thanks for using it!", "Спасибо, что пользовались!"),
    "pick_folder": ("Choose install folder", "Выберите папку установки"),
    "min": ("Minimise", "Свернуть"),
}


def tr(key, lang):
    pair = T.get(key, (key, key))
    return pair[1] if lang == "ru" else pair[0]


def _font_family():
    fams = set(QFontDatabase().families())
    for f in ("Segoe UI Variable Display", "Segoe UI", "Inter", "Helvetica Neue", "Arial"):
        if f in fams:
            return f
    return ""


def _check_icon(path):
    """Black check mark used inside yellow checkboxes."""
    pm = QPixmap(36, 36)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(QColor("#111111"), 4.2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    p.drawPolyline(QPoint(9, 19), QPoint(15, 25), QPoint(27, 11))
    p.end()
    pm.save(path)
    return path


def stylesheet(check_path):
    fam = _font_family()
    return """
* { font-family: "%(fam)s"; }
QWidget { color: #f0efed; font-size: 14px; }
QFrame#shell { background: #141414; border: 1px solid #262626; border-radius: 14px; }
QLabel#muted { color: #8f8b88; }
QLabel#small { color: #8f8b88; font-size: 12px; }
QLabel#title { font-size: 27px; font-weight: 700; }
QLabel#appname { font-size: 18px; font-weight: 700; }
QLabel#wintitle { color: #8f8b88; font-size: 13px; }
QFrame#card { background: #1c1c1c; border-radius: 12px; }
QLineEdit { background: #242424; border: none; border-radius: 8px; padding: 9px 12px;
            selection-background-color: %(acc)s; selection-color: #111; }
QPushButton { background: #262626; border: none; border-radius: 8px; padding: 9px 16px; }
QPushButton:hover { background: #2f2f2f; }
QPushButton#primary { background: %(acc)s; color: #111; font-weight: 600; min-width: 92px; }
QPushButton#primary:hover { background: #ffd92e; }
QPushButton#seg { background: transparent; color: #8f8b88; padding: 6px 12px; border-radius: 7px;
                  font-size: 13px; }
QPushButton#seg:checked { background: #2c2c2c; color: #f0efed; }
QFrame#segbox { background: #1c1c1c; border: 1px solid #2a2a2a; border-radius: 9px; }
QCheckBox { spacing: 10px; }
QCheckBox::indicator { width: 18px; height: 18px; border-radius: 5px; background: #2a2a2a; }
QCheckBox::indicator:checked { background: %(acc)s; image: url("%(check)s"); }
QProgressBar { background: #242424; border: none; border-radius: 3px; max-height: 6px; }
QProgressBar::chunk { background: %(acc)s; border-radius: 3px; }
""" % {"fam": fam, "acc": ACCENT, "check": check_path.replace("\\", "/")}


class Dot(QPushButton):
    """Small round window button (minimise / close)."""

    def __init__(self, colour, parent=None):
        QPushButton.__init__(self, parent)
        self.colour = QColor(colour)
        self.setFixedSize(16, 16)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("background: transparent; padding: 0;")

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        c = QColor(self.colour)
        if self.underMouse():
            c = c.lighter(118)
        p.setPen(Qt.NoPen)
        p.setBrush(c)
        p.drawEllipse(QRectF(2, 2, 12, 12))
        p.end()


class Worker(QThread):
    progress = pyqtSignal(int, str)
    finished_ok = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, fn, parent=None):
        QThread.__init__(self, parent)
        self.fn = fn

    def run(self):
        try:
            result = self.fn(lambda i, n, name: self.progress.emit(int(100 * i / max(1, n)), name))
            self.finished_ok.emit(str(result or ""))
        except Exception as e:  # noqa: BLE001 - shown to the user
            self.failed.emit(str(e))


class SetupWindow(QWidget):
    def __init__(self, mode="install", install_dir=None):
        QWidget.__init__(self)
        self.mode = mode
        self.lang = "ru" if QLocale.system().name().split("_")[0] in ("ru", "uk", "be") else "en"
        self.worker = None
        self._drag = None
        self.existing = core.existing_install() if mode == "install" else None
        self.version, self.size = ("", 0)
        if mode == "install":
            self.version, self.size = core.payload_info()
        self.install_dir = install_dir or (self.existing or {}).get("dir") or core.default_install_dir()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(640, 530)
        icon = QIcon(core.resource("icon.png"))
        self.setWindowIcon(icon)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(6, 6, 6, 6)
        shell = QFrame()
        shell.setObjectName("shell")
        outer.addWidget(shell)
        lay = QVBoxLayout(shell)
        lay.setContentsMargins(26, 14, 26, 24)
        lay.setSpacing(0)

        # title bar
        self.titlebar = QWidget()
        tb = QHBoxLayout(self.titlebar)
        tb.setContentsMargins(0, 0, 0, 0)
        small = QLabel()
        small.setPixmap(icon.pixmap(16, 16))
        tb.addWidget(small)
        self.wintitle = QLabel()
        self.wintitle.setObjectName("wintitle")
        tb.addWidget(self.wintitle)
        tb.addStretch(1)
        self.d_min = Dot("#2fc25b")
        self.d_min.clicked.connect(self.showMinimized)
        self.d_mid = Dot("#5a5a5a")
        self.d_close = Dot("#ff5f57")
        self.d_close.clicked.connect(self.close)
        for d in (self.d_min, self.d_mid, self.d_close):
            tb.addSpacing(6)
            tb.addWidget(d)
        lay.addWidget(self.titlebar)
        lay.addSpacing(22)

        # header: icon, name, language switch
        head = QHBoxLayout()
        tile = QLabel()
        tile.setFixedSize(46, 46)
        tile.setAlignment(Qt.AlignCenter)
        tile.setStyleSheet("background: #1f1f1f; border-radius: 12px;")
        tile.setPixmap(icon.pixmap(34, 34))
        head.addWidget(tile)
        head.addSpacing(10)
        names = QVBoxLayout()
        names.setSpacing(0)
        appname = QLabel(core.APP_NAME)
        appname.setObjectName("appname")
        self.sub = QLabel()
        self.sub.setObjectName("small")
        names.addWidget(appname)
        names.addWidget(self.sub)
        head.addLayout(names)
        head.addStretch(1)
        segbox = QFrame()
        segbox.setObjectName("segbox")
        sl = QHBoxLayout(segbox)
        sl.setContentsMargins(3, 3, 3, 3)
        sl.setSpacing(2)
        self.lang_group = QButtonGroup(self)
        for i, code in enumerate(("ru", "en")):
            b = QPushButton(code.upper())
            b.setObjectName("seg")
            b.setCheckable(True)
            b.setChecked(code == self.lang)
            b.setFocusPolicy(Qt.NoFocus)
            b.setCursor(Qt.PointingHandCursor)
            self.lang_group.addButton(b, i)
            sl.addWidget(b)
        self.lang_group.buttonClicked[int].connect(lambda i: self.set_lang(("ru", "en")[i]))
        head.addWidget(segbox, 0, Qt.AlignTop)
        lay.addLayout(head)
        lay.addSpacing(24)

        self.title = QLabel()
        self.title.setObjectName("title")
        lay.addWidget(self.title)
        lay.addSpacing(6)
        self.subtitle = QLabel()
        self.subtitle.setObjectName("muted")
        self.subtitle.setWordWrap(True)
        lay.addWidget(self.subtitle)
        lay.addSpacing(20)

        self.pages = QStackedWidget()
        lay.addWidget(self.pages, 1)

        # page 0: options
        opts = QWidget()
        ov = QVBoxLayout(opts)
        ov.setContentsMargins(0, 0, 0, 0)
        ov.setSpacing(14)
        card = QFrame()
        card.setObjectName("card")
        cv = QVBoxLayout(card)
        cv.setContentsMargins(18, 16, 18, 16)
        cv.setSpacing(10)
        self.loc_label = QLabel()
        self.loc_label.setObjectName("small")
        cv.addWidget(self.loc_label)
        row = QHBoxLayout()
        row.setSpacing(10)
        self.path = QLineEdit(self.install_dir)
        row.addWidget(self.path, 1)
        self.change = QPushButton()
        self.change.setCursor(Qt.PointingHandCursor)
        self.change.clicked.connect(self.pick_dir)
        row.addWidget(self.change)
        self.loc_row = QWidget()
        self.loc_row.setLayout(row)
        row.setContentsMargins(0, 0, 0, 0)
        cv.addWidget(self.loc_row)
        cv.addSpacing(2)
        self.cb_desktop = QCheckBox()
        self.cb_desktop.setChecked(True)
        self.cb_launch = QCheckBox()
        self.cb_launch.setChecked(True)
        self.cb_data = QCheckBox()
        self.cb_data.setChecked(False)
        for cb in (self.cb_desktop, self.cb_launch, self.cb_data):
            cb.setCursor(Qt.PointingHandCursor)
            cv.addWidget(cb)
        ov.addWidget(card)
        self.note = QLabel()
        self.note.setObjectName("small")
        self.note.setWordWrap(True)
        ov.addWidget(self.note)
        ov.addStretch(1)
        self.pages.addWidget(opts)

        # page 1: progress
        prog = QWidget()
        pv = QVBoxLayout(prog)
        pv.setContentsMargins(0, 30, 0, 0)
        pv.setSpacing(12)
        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        pv.addWidget(self.bar)
        self.status = QLabel()
        self.status.setObjectName("small")
        pv.addWidget(self.status)
        pv.addStretch(1)
        self.pages.addWidget(prog)

        # page 2: empty (done / error use the title + subtitle)
        self.pages.addWidget(QWidget())

        # buttons
        btns = QHBoxLayout()
        btns.addStretch(1)
        self.b_cancel = QPushButton()
        self.b_cancel.setCursor(Qt.PointingHandCursor)
        self.b_cancel.clicked.connect(self.close)
        self.b_main = QPushButton()
        self.b_main.setObjectName("primary")
        self.b_main.setCursor(Qt.PointingHandCursor)
        self.b_main.setDefault(True)
        self.b_main.clicked.connect(self.main_action)
        btns.addWidget(self.b_cancel)
        btns.addSpacing(8)
        btns.addWidget(self.b_main)
        lay.addLayout(btns)

        self.stage = "options"
        self.error = ""
        self.retranslate()

    # ------------------------------------------------------------------
    def t(self, key):
        return tr(key, self.lang)

    def set_lang(self, lang):
        self.lang = lang
        b = self.lang_group.button(0 if lang == "ru" else 1)
        if b is not None and not b.isChecked():
            b.setChecked(True)
        self.retranslate()

    def retranslate(self):
        t = self.t
        self.wintitle.setText(t("window"))
        self.setWindowTitle(t("window"))
        self.sub.setText(t("setup"))
        self.d_min.setToolTip(t("min"))
        self.d_close.setToolTip(t("close"))
        self.loc_label.setText(t("location"))
        self.change.setText(t("change"))
        self.cb_desktop.setText(t("desktop"))
        self.cb_launch.setText(t("launch"))
        self.cb_data.setText(t("delete_data"))
        self.b_cancel.setText(t("cancel"))
        uninstall = self.mode == "uninstall"
        self.loc_label.setVisible(not uninstall)
        self.loc_row.setVisible(not uninstall)
        self.cb_desktop.setVisible(not uninstall)
        self.cb_launch.setVisible(not uninstall)
        self.cb_data.setVisible(uninstall)
        updating = bool(self.existing)
        st = self.stage
        if st == "options":
            if uninstall:
                self.title.setText(t("remove_title"))
                self.subtitle.setText(t("remove_sub"))
                self.note.setText(t("data_kept"))
                self.b_main.setText(t("remove"))
            else:
                if updating and self.existing.get("version") == self.version:
                    self.title.setText(t("reinstall_title") % self.version)
                elif updating:
                    self.title.setText(t("update_title") % self.version)
                else:
                    self.title.setText(t("install_title") % self.version)
                self.subtitle.setText(t("tagline"))
                note = t("needs") % max(1, round(self.size / 1048576.0))
                if updating:
                    note += " " + t("keeps")
                self.note.setText(note)
                self.b_main.setText(t("update") if updating else t("install"))
            self.b_cancel.setVisible(True)
        elif st == "working":
            self.b_cancel.setVisible(False)
            self.b_main.setVisible(False)
            if uninstall:
                self.title.setText(t("removing"))
            else:
                self.title.setText(t("updating") if updating else t("installing"))
            self.subtitle.setText("")
        elif st == "done":
            if uninstall:
                self.title.setText(t("removed"))
                self.subtitle.setText(t("removed_sub"))
            else:
                self.title.setText(t("done_title"))
                extra = t("done_desktop") if self.cb_desktop.isChecked() else ""
                self.subtitle.setText(t("done_sub") % extra)
            self.b_main.setText(t("finish"))
            self.b_main.setVisible(True)
            self.b_cancel.setVisible(False)
        elif st == "error":
            self.title.setText(t("error_title"))
            self.subtitle.setText(self.error)
            self.b_main.setText(t("retry"))
            self.b_main.setVisible(True)
            self.b_cancel.setText(t("close"))
            self.b_cancel.setVisible(True)

    # ------------------------------------------------------------------
    def pick_dir(self):
        d = QFileDialog.getExistingDirectory(self, self.t("pick_folder"), self.path.text())
        if d:
            self.path.setText(core.normalise_dir(d))

    def main_action(self):
        if self.stage == "done":
            if self.mode == "install" and self.cb_launch.isChecked():
                core.launch_app(self.install_dir)
            self.close()
            return
        if self.stage in ("options", "error"):
            self.start()

    def start(self):
        self.stage = "working"
        self.pages.setCurrentIndex(1)
        self.b_main.setEnabled(False)
        self.b_cancel.setVisible(False)
        self.bar.setValue(0)
        self.status.setText(self.t("preparing"))
        self.retranslate()
        if self.mode == "install":
            self.install_dir = core.normalise_dir(self.path.text())
            payload = core.resource("payload.zip")
            desktop = self.cb_desktop.isChecked()
            existing = self.existing
            target = self.install_dir

            def job(progress):
                return core.install(payload, target, desktop, progress, existing)
        else:
            target = self.install_dir
            delete_data = self.cb_data.isChecked()

            def job(progress):
                core.uninstall(target, delete_data, progress)

        self.worker = Worker(job, self)
        self.worker.progress.connect(self._progress)
        self.worker.finished_ok.connect(self._done)
        self.worker.failed.connect(self._failed)
        self.worker.start()

    def _progress(self, pct, name):
        self.bar.setValue(pct)
        self.status.setText(name)

    def _done(self, _result):
        self.stage = "done"
        self.pages.setCurrentIndex(2)
        self.b_main.setEnabled(True)
        self.retranslate()
        if self.mode == "uninstall":
            _schedule_self_delete()

    def _failed(self, msg):
        self.error = msg
        self.stage = "error"
        self.pages.setCurrentIndex(2)
        self.b_main.setEnabled(True)
        self.retranslate()

    # ------------------------------------------------------------------
    def closeEvent(self, e):
        if self.worker is not None and self.worker.isRunning():
            e.ignore()
            return
        QWidget.closeEvent(self, e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and e.pos().y() < 70:
            self._drag = e.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag is not None and e.buttons() & Qt.LeftButton:
            self.move(e.globalPos() - self._drag)

    def mouseReleaseEvent(self, e):
        self._drag = None

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and self.stage != "working":
            self.close()
        elif e.key() in (Qt.Key_Return, Qt.Key_Enter) and self.b_main.isEnabled():
            self.main_action()
        else:
            QWidget.keyPressEvent(self, e)


TEMP_PREFIX = "EnigmaCube-uninstall-"


def _schedule_self_delete():
    """The temporary copy used for uninstalling removes itself after it exits."""
    if not core.IS_WIN or not getattr(sys, "frozen", False):
        return
    folder = os.path.dirname(sys.executable)
    if not os.path.basename(folder).startswith(TEMP_PREFIX):
        return
    subprocess.Popen('cmd /c ping 127.0.0.1 -n 4 > nul & rmdir /s /q "%s"' % folder,
                     shell=True, creationflags=core.NO_WINDOW)


def _relaunch_from_temp(install_dir, quiet):
    """The program cannot delete its own files while running, so the removal
    runs from a temporary copy of the program folder."""
    tmp = os.path.join(tempfile.gettempdir(), TEMP_PREFIX + str(os.getpid()))
    shutil.copytree(install_dir, tmp)
    exe = os.path.join(tmp, os.path.basename(sys.executable))
    args = [exe, "--uninstall", "--dir", install_dir] + (["--quiet"] if quiet else [])
    subprocess.Popen(args, cwd=tmp, close_fds=True)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:  # avoid crashes on exit (see main.py)
        from PyQt5 import sip
        sip.setdestroyonexit(False)
    except ImportError:
        pass
    uninstall = "--uninstall" in argv
    quiet = "--quiet" in argv
    install_dir = None
    if "--dir" in argv and argv.index("--dir") + 1 < len(argv):
        install_dir = argv[argv.index("--dir") + 1]

    if uninstall:
        here = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else None
        if install_dir is None:
            install_dir = here or core.default_install_dir()
            if here and core.IS_WIN:
                _relaunch_from_temp(install_dir, quiet)
                return 0
        if quiet:
            core.uninstall(install_dir)
            _schedule_self_delete()
            return 0

    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    check = _check_icon(os.path.join(tempfile.gettempdir(), "enigma_setup_check.png"))
    app.setStyleSheet(stylesheet(check))
    win = SetupWindow("uninstall" if uninstall else "install", install_dir)
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
