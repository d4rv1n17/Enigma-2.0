"""Colours and the application style sheet."""

import os
import sys

from PyQt5.QtGui import QFontDatabase

_ROOT = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHEVRON = "" if "chev" in os.environ.get("ET_SKIP", "") else os.path.join(_ROOT, "assets", "chevron.png").replace("\\", "/")

# Colours sampled from the Enigma Cube logo
BG = "#121111"          # logo background
PANEL = "#181717"       # cards: barely lighter than the background, no borders
PANEL2 = "#211f1f"      # hover / inputs
BORDER = "#2a2828"
TEXT = "#f0efed"
MUTED = "#7d7976"
FAINT = "#4a4644"       # very quiet UI (inactive icons, separators)
SCRAMBLE = "#d6d2cd"
ACCENT = "#f4cc0c"      # Enigma Cube yellow
ACCENT_DARK = "#2e2706"
READY = "#2ee07a"
HOLD = "#ff5a5f"
INSPECT = "#ffb020"
BLUE = "#5aa9ff"
DNF_RED = "#ff5a5f"

_PREFERRED = ["Segoe UI", "SF Pro Display", "Helvetica Neue", "Inter",
              "Roboto", "Ubuntu", "Noto Sans", "Arial"]
_MONO = ["Cascadia Mono", "Consolas", "SF Mono", "Menlo", "JetBrains Mono",
         "DejaVu Sans Mono", "Courier New"]

_cache = {}


def _pick(candidates, key):
    if key not in _cache:
        families = set(QFontDatabase().families())
        _cache[key] = next((f for f in candidates if f in families), "")
    return _cache[key]


def ui_font():
    return _pick(_PREFERRED, "ui")


def mono_font():
    return _pick(_MONO, "mono")


def stylesheet():
    family = ui_font()
    fam = ('font-family: "%s";' % family) if family else ""
    return """
* { %(fam)s }
QMainWindow, QWidget#central { background: %(BG)s; }
QWidget { color: %(TEXT)s; font-size: 14px; }
QToolTip { background: %(PANEL2)s; color: %(TEXT)s; border: none; padding: 6px 8px;
           border-radius: 6px; }

/* cards: no outlines, just a slightly lighter surface */
QFrame#panel { background: %(PANEL)s; border: none; border-radius: 18px; }
QLabel#muted { color: %(MUTED)s; }
QLabel#sectionTitle { color: %(MUTED)s; font-size: 11px; font-weight: 600; }
QLabel#toast { background: %(PANEL2)s; color: %(ACCENT)s; border-radius: 16px;
               padding: 8px 20px; font-weight: 600; font-size: 14px; }

/* buttons are quiet text by default */
QPushButton { background: transparent; border: none; border-radius: 8px;
              padding: 6px 10px; color: %(MUTED)s; }
QPushButton:hover { color: %(TEXT)s; background: %(PANEL2)s; }
QPushButton:pressed { color: %(ACCENT)s; }
QPushButton:disabled { color: %(FAINT)s; }
QPushButton:checked { color: %(ACCENT)s; }

QPushButton#puzzle { padding: 6px 7px 5px 7px; font-weight: 600; font-size: 13px;
                     border-radius: 0; border-bottom: 2px solid transparent; min-width: 30px; }
QPushButton#puzzle:hover { background: transparent; color: %(TEXT)s; }
QPushButton#puzzle:checked { color: %(TEXT)s; border-bottom: 2px solid %(ACCENT)s; }
QPushButton#pen { min-width: 40px; font-weight: 600; font-size: 13px; }
QPushButton#icon { padding: 5px 9px; font-size: 16px; color: %(FAINT)s; }
QPushButton#icon:hover { color: %(TEXT)s; }
QPushButton#icon:checked { color: %(ACCENT)s; }
QPushButton#tab { padding: 4px 8px; font-size: 11px; font-weight: 600; }
QPushButton#tab:hover { background: transparent; }
QPushButton#tab:checked { color: %(TEXT)s; }

QPushButton#event { font-size: 14px; font-weight: 600; padding: 7px 12px; color: %(TEXT)s;
                    background: %(PANEL2)s; border-radius: 9px; }
QPushButton#event:hover { background: #2b2929; }
QPushButton#event::menu-indicator { image: none; width: 0; }
QPushButton#windows { font-size: 14px; font-weight: 600; padding: 7px 12px; color: %(MUTED)s;
                      background: transparent; border-radius: 9px; }
QPushButton#windows:hover { background: %(PANEL2)s; color: %(TEXT)s; }
QPushButton#windows::menu-indicator { image: none; width: 0; }
QLabel#keycap { background: %(PANEL2)s; color: %(TEXT)s; border-radius: 6px; padding: 2px 8px;
                font-size: 12px; font-weight: 600; }
QLabel#empty { color: %(MUTED)s; font-size: 13px; }
QPushButton#pin { padding: 4px 10px; font-size: 12px; color: %(MUTED)s; border-radius: 8px; }
QPushButton#pin:hover { color: %(TEXT)s; background: %(PANEL2)s; }
QPushButton#pin:checked { color: #111; background: %(ACCENT)s; }
QFrame#steprow { background: %(PANEL)s; border-radius: 12px; }
QFrame#steprow:hover { background: %(PANEL2)s; }
QProgressBar { background: %(BORDER)s; border: none; border-radius: 3px; }
QProgressBar::chunk { background: %(ACCENT)s; border-radius: 3px; }
QPushButton#nav { font-size: 15px; font-weight: 600; padding: 6px 12px; color: %(MUTED)s; }
QPushButton#nav:hover { background: transparent; color: %(TEXT)s; }
QPushButton#nav:checked { color: %(TEXT)s; background: %(PANEL2)s; }
QPushButton#primary { background: %(ACCENT)s; color: #111; font-weight: 700; padding: 8px 18px;
                      border-radius: 10px; }
QPushButton#primary:hover { background: #ffd92e; color: #111; }
QPushButton#seg { background: %(PANEL2)s; color: %(MUTED)s; padding: 7px 12px; }
QPushButton#seg:checked { background: %(ACCENT_DARK)s; color: %(ACCENT)s; }
QPushButton#rate { background: %(PANEL2)s; color: %(TEXT)s; padding: 10px 16px; font-weight: 600;
                   border-radius: 10px; }
QPushButton#rate:hover { background: #2e2c2c; }

QListWidget#levels, QListWidget#grid { background: transparent; border: none; outline: 0; }
QListWidget#plainlist { background: transparent; border: none; outline: 0; font-size: 14px; }
QListWidget#plainlist::item { padding: 4px 10px; border-radius: 8px; color: %(MUTED)s; }
QListWidget#plainlist::item:hover { background: #1d1c1c; color: %(TEXT)s; }
QListWidget#plainlist::item:selected { background: %(PANEL2)s; color: %(TEXT)s; }
QListWidget#levels::item, QListWidget#grid::item { background: transparent; border: none; }
QTextBrowser { background: transparent; border: none; color: %(SCRAMBLE)s; font-size: 15px;
               selection-background-color: %(ACCENT)s; selection-color: #111; }

/* real buttons inside dialogs */
QDialog QPushButton { background: %(PANEL2)s; color: %(TEXT)s; padding: 7px 16px; }
QDialog QPushButton:hover { background: #2b2929; }
QDialog QPushButton:default { background: %(ACCENT)s; color: #111; font-weight: 600; }
QDialog QPushButton#pen:checked { background: %(ACCENT_DARK)s; color: %(ACCENT)s; }

QToolButton { background: transparent; border: none; border-radius: 8px;
              padding: 5px 9px; color: %(FAINT)s; font-size: 16px; }
QToolButton:hover { color: %(TEXT)s; background: %(PANEL2)s; }
QToolButton::menu-indicator { image: none; }

QComboBox { background: transparent; border: none; border-radius: 8px;
            padding: 5px 8px; font-weight: 600; font-size: 15px; }
QComboBox:hover { background: %(PANEL2)s; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox::down-arrow { image: url(%(CHEVRON)s); width: 10px; height: 6px; }
QComboBox QAbstractItemView { background: %(PANEL2)s; border: none; padding: 4px;
            selection-background-color: %(ACCENT)s; selection-color: #111; outline: 0; }
QDialog QComboBox { background: %(BG)s; font-size: 14px; font-weight: 400; }

QMenu { background: %(PANEL2)s; border: none; padding: 6px; border-radius: 10px; }
QMenu::item { padding: 7px 22px; border-radius: 6px; }
QMenu::item:selected { background: #2e2c2c; color: %(TEXT)s; }
QMenu::separator { height: 1px; background: %(BORDER)s; margin: 5px 10px; }

QTableWidget { background: transparent; border: none; gridline-color: transparent;
               selection-background-color: transparent; outline: 0; }
QTableWidget::item { padding: 2px 6px; border: none; }
QTableWidget::item:hover { background: %(PANEL2)s; }
QHeaderView { background: transparent; border: none; }
QHeaderView::section { background: transparent; color: %(FAINT)s; border: none;
                       padding: 2px 6px 6px 6px; font-size: 11px; font-weight: 600; }
QTableCornerButton::section { background: transparent; border: none; }

QScrollBar:vertical { background: transparent; width: 6px; margin: 2px; }
QScrollBar::handle:vertical { background: #2a2828; border-radius: 3px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: #3a3737; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; width: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }

QDialog { background: %(PANEL)s; }
QLineEdit, QPlainTextEdit, QSpinBox { background: %(BG)s; border: 1px solid %(BORDER)s;
            border-radius: 8px; padding: 7px; selection-background-color: %(ACCENT)s;
            selection-color: #111; }
QLineEdit:focus, QPlainTextEdit:focus { border-color: #4a4430; }
QCheckBox { spacing: 10px; }
QCheckBox::indicator { width: 16px; height: 16px; border-radius: 5px; background: %(BORDER)s; }
QCheckBox::indicator:checked { background: %(ACCENT)s; }
QSlider::groove:horizontal { height: 4px; background: %(BORDER)s; border-radius: 2px; }
QSlider::handle:horizontal { background: %(TEXT)s; width: 14px; margin: -5px 0;
                             border-radius: 7px; }
QSlider::sub-page:horizontal { background: %(ACCENT)s; border-radius: 2px; }
""" % dict(fam=fam, BG=BG, PANEL=PANEL, PANEL2=PANEL2, BORDER=BORDER, TEXT=TEXT,
           MUTED=MUTED, FAINT=FAINT, ACCENT=ACCENT, ACCENT_DARK=ACCENT_DARK,
           SCRAMBLE=SCRAMBLE, CHEVRON=CHEVRON)
