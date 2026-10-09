#!/usr/bin/env python3
"""Enigma Cube - a speedcubing timer.

Run:  python main.py
"""

import os
import sys

from PyQt5.QtCore import QLocale, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enigma_timer import i18n, theme  # noqa: E402
from enigma_timer.storage import Store  # noqa: E402
from enigma_timer.window import MainWindow  # noqa: E402


def safe_exit_setup():
    """Don't run C++ destructors at interpreter exit (PyQt's recommended fix for
    crashes on exit when Qt objects outlive the QApplication)."""
    try:
        from PyQt5 import sip
    except ImportError:  # very old PyQt5
        try:
            import sip
        except ImportError:
            return
    sip.setdestroyonexit(False)


def main():
    safe_exit_setup()
    if "--selftest" in sys.argv:
        from enigma_timer import selftest
        i = sys.argv.index("--selftest")
        folder = sys.argv[i + 1] if i + 1 < len(sys.argv) else "selftest"
        sys.exit(selftest.run(folder))
    if "--uninstall" in sys.argv:
        # Settings -> Apps -> Enigma Cube -> Uninstall runs "EnigmaCube.exe --uninstall"
        from installer import setup_app
        sys.exit(setup_app.main())
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setApplicationName("Enigma Cube")
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
    icon = os.path.join(base, "assets", "app_icon.png")
    if os.path.exists(icon):
        app.setWindowIcon(QIcon(icon))
    app.setStyle("Fusion")
    app.setStyleSheet(theme.stylesheet())

    store = Store()
    lang = store.settings.get("language")
    if not lang:  # auto: Russian for ru/uk/be systems, otherwise English
        sys_lang = QLocale.system().name().split("_")[0]
        lang = "ru" if sys_lang in ("ru", "uk", "be") else "en"
    i18n.set_language(lang)
    win = MainWindow(store)
    win.show()
    code = app.exec_()
    # Free cached pixmaps while Qt is still alive; see safe_exit_setup().
    from enigma_timer import training
    training.clear_caches()
    sys.exit(code)


if __name__ == "__main__":
    main()
