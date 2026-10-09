# -*- coding: utf-8 -*-
"""GUI self-test: python main.py --selftest <folder>

Builds every screen of the app with real Qt, saves screenshots into <folder>
and exits with code 0 (or 1 and a traceback in <folder>/error.txt). Used by
the CI workflow on Windows, where the real app can be checked.
"""

import json
import os
import random
import sys
import tempfile
import time
import traceback
import zipfile


def _pump(app, ms=150):
    end = time.time() + ms / 1000.0
    while time.time() < end:
        app.processEvents()
        time.sleep(0.01)


_LOG = []


def _step(folder, text):
    _LOG.append(text)
    with open(os.path.join(folder, "steps.txt"), "a", encoding="utf-8") as f:
        f.write(text + "\n")


def _grab(app, widget, folder, name):
    _pump(app)
    widget.grab().save(os.path.join(folder, name + ".png"))
    _step(folder, "saved " + name)


_KEEP = []   # keeps Qt objects alive until the process exits


def run(folder):
    os.makedirs(folder, exist_ok=True)
    import faulthandler
    fault = open(os.path.join(folder, "fault.txt"), "w")
    faulthandler.enable(fault)
    code = 0
    try:
        _run(folder)
        _step(folder, "all screens done")
        with open(os.path.join(folder, "ok.txt"), "w") as f:
            f.write("ok")
    except Exception:  # noqa: BLE001 - report everything
        with open(os.path.join(folder, "error.txt"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        traceback.print_exc()
        code = 1
    from . import training
    training.clear_caches()
    _step(folder, "exit %d" % code)
    fault.flush()
    return code


def _run(folder):
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication

    from . import i18n, theme
    from .stats import Solve, PLUS2, DNF
    from .storage import Store
    from .window import MainWindow

    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication.instance() or QApplication(sys.argv[:1])
    _KEEP.append(app)
    app.setStyle("Fusion")
    app.setStyleSheet(theme.stylesheet())

    for lang in ("ru", "en"):
        i18n.set_language(lang)
        tmp = tempfile.mkdtemp()
        store = Store(os.path.join(tmp, "data.json"))
        win = MainWindow(store)
        _KEEP.append(win)
        win.resize(1440, 880)
        win.show()
        _grab(app, win, folder, "%s_01_timer_empty" % lang)

        random.seed(7)
        base = time.time() - 3600
        for i in range(60):
            ms = int(random.gauss(14500, 1600))
            pen = DNF if i == 17 else (PLUS2 if i == 33 else 0)
            win.store.current.solves.append(Solve(ms, pen, win.scramble, base + i * 40))
        win.refresh()
        _grab(app, win, folder, "%s_02_timer_stats" % lang)
        win.chart_tabs.button(1).click()
        _grab(app, win, folder, "%s_03_distribution" % lang)

        for pid in ("pyram", "sq1", "777"):
            win.select_puzzle(pid)
        _grab(app, win, folder, "%s_04_timer_7x7" % lang)
        win.select_puzzle("333")

        win.set_page(1)
        tw = win.training
        _grab(app, win, folder, "%s_05_training_notation" % lang)
        tw.levels.setCurrentRow(1)
        _grab(app, win, folder, "%s_06_training_beginner" % lang)
        tw.levels.setCurrentRow(5)          # full OLL
        tw.content.setCurrentIndex(1)
        tw.grid.setCurrentRow(26)           # OLL 27 (Sune)
        _grab(app, win, folder, "%s_07_training_oll" % lang)
        tw.levels.setCurrentRow(6)          # PLL
        tw.content.setCurrentIndex(1)
        tw.grid.setCurrentRow(15)
        _grab(app, win, folder, "%s_08_training_pll" % lang)
        tw.levels.setCurrentRow(4)          # F2L
        tw.content.setCurrentIndex(1)
        tw.grid.setCurrentRow(0)
        _grab(app, win, folder, "%s_09_training_f2l" % lang)
        tw.levels.setCurrentRow(6)
        tw.train_level()
        _grab(app, win, folder, "%s_10_trainer" % lang)
        tw.trainer.reveal()
        _grab(app, win, folder, "%s_11_trainer_revealed" % lang)
        tw.trainer.rate(2)
        tw.trainer.stop()

        win.open_training_window()
        extra = win.extra_windows[-1]
        _grab(app, extra, folder, "%s_12_training_window" % lang)
        extra.close()
        win.set_page(0)
        win.close()
        _pump(app)

        _setup_screens(app, folder, lang)


def _setup_screens(app, folder, lang):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root)
    from installer import setup_app, setup_core

    tmp = tempfile.mkdtemp()
    payload = os.path.join(tmp, "payload.zip")
    with zipfile.ZipFile(payload, "w") as z:
        z.writestr("EnigmaCube.exe", b"0" * (58 * 1024 * 1024))
        z.writestr("payload.json", json.dumps({"version": "3.0"}))
    original = setup_core.resource
    setup_core.resource = lambda name: payload if name == "payload.zip" else original(name)
    check = setup_app._check_icon(os.path.join(tmp, "check.png"))
    app.setStyleSheet(setup_app.stylesheet(check))
    try:
        w = setup_app.SetupWindow("install", os.path.join(tmp, "Enigma Cube"))
        _KEEP.append(w)
        w.set_lang(lang)
        w.show()
        _grab(app, w, folder, "%s_20_setup" % lang)
        w.stage = "working"
        w.pages.setCurrentIndex(1)
        w.bar.setValue(64)
        w.status.setText("_internal\\PyQt5\\Qt5\\bin\\Qt5Widgets.dll")
        w.retranslate()
        _grab(app, w, folder, "%s_21_setup_progress" % lang)
        w._done("")
        _grab(app, w, folder, "%s_22_setup_done" % lang)
        w.close()
        u = setup_app.SetupWindow("uninstall", os.path.join(tmp, "Enigma Cube"))
        _KEEP.append(u)
        u.set_lang(lang)
        u.show()
        _grab(app, u, folder, "%s_23_uninstall" % lang)
        u.close()
    finally:
        setup_core.resource = original
        from . import theme
        app.setStyleSheet(theme.stylesheet())
