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


def main():
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
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
