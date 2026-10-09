# -*- coding: utf-8 -*-
"""Training section: learning path, algorithm browser, lessons and trainer.

The same TrainingWidget is used inside the main window and in any number of
separate windows (see windows.py); they share one TrainingHub, so progress
changed in one window appears in all of them immediately.
"""

import math
import random
from urllib.parse import unquote

from PyQt5.QtCore import QObject, QPointF, QRectF, QSize, Qt, pyqtSignal
from PyQt5.QtGui import (QColor, QFont, QImage, QPainter, QPen, QPixmap,
                         QPolygonF, QTextDocument)
from PyQt5.QtWidgets import (QAbstractItemView, QButtonGroup, QComboBox, QFrame, QGridLayout, QHBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QProgressBar, QPushButton, QScrollArea, QSizePolicy, QStackedWidget, QStyle, QStyledItemDelegate, QTextBrowser, QVBoxLayout, QWidget)

from . import algs, caseview, insights, learn, theme
from .fast3 import State
from .i18n import lang, pick, tr
from .lessons import lesson_html

ROLE_ID = Qt.UserRole + 1


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def paint_shapes(p, rect, shapes):
    """Draw caseview primitives into a QRectF."""
    x0, y0, w, h = rect.x(), rect.y(), rect.width(), rect.height()

    def T(pt):
        return QPointF(x0 + pt[0] * w, y0 + pt[1] * h)

    p.setRenderHint(QPainter.Antialiasing)
    for sh in shapes:
        if sh[0] == "poly":
            col = QColor(sh[2])
            p.setPen(QPen(col, 0.6))
            p.setBrush(col)
            p.drawPolygon(QPolygonF([T(q) for q in sh[1]]))
    lw = max(1.5, w * 0.022)
    for sh in shapes:
        if sh[0] == "line":
            p.setPen(QPen(QColor(theme.ACCENT), max(1.2, w * 0.012), Qt.DashLine))
            p.drawLine(T(sh[1]), T(sh[2]))
    for sh in shapes:
        if sh[0] not in ("arrow", "arrow2"):
            continue
        a, b = T(sh[1]), T(sh[2])
        heads = [(a, b)] + ([(b, a)] if sh[0] == "arrow2" else [])
        p.setPen(QPen(QColor("#111111"), lw, Qt.SolidLine, Qt.RoundCap))
        dx, dy = b.x() - a.x(), b.y() - a.y()
        length = math.hypot(dx, dy) or 1.0
        shrink = w * 0.05
        ux, uy = dx / length, dy / length
        a2 = QPointF(a.x() + ux * shrink, a.y() + uy * shrink)
        b2 = QPointF(b.x() - ux * shrink, b.y() - uy * shrink)
        p.drawLine(a2, b2)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#111111"))
        hl = w * 0.07
        for (s, e) in heads:
            ang = math.atan2(e.y() - s.y(), e.x() - s.x())
            tip = QPointF(e.x() - math.cos(ang) * shrink, e.y() - math.sin(ang) * shrink)
            l1 = QPointF(tip.x() - hl * math.cos(ang - 0.45), tip.y() - hl * math.sin(ang - 0.45))
            l2 = QPointF(tip.x() - hl * math.cos(ang + 0.45), tip.y() - hl * math.sin(ang + 0.45))
            p.drawPolygon(QPolygonF([tip, l1, l2]))


_PIX_CACHE = {}


def clear_caches():
    """Free cached pixmaps while Qt is still alive (avoids crashes on exit)."""
    _PIX_CACHE.clear()


def case_pixmap(case, size, auf=None, arrows=True):
    key = (case.id, size, auf, arrows)
    pm = _PIX_CACHE.get(key)
    if pm is None:
        dpr = 2.0
        img = QImage(int(size * dpr), int(size * dpr), QImage.Format_ARGB32_Premultiplied)
        img.fill(Qt.transparent)
        p = QPainter(img)
        paint_shapes(p, QRectF(0, 0, size * dpr, size * dpr),
                     caseview.case_shapes(case, auf, arrows))
        p.end()
        pm = QPixmap.fromImage(img)
        pm.setDevicePixelRatio(dpr)
        _PIX_CACHE[key] = pm
    return pm


def move_image(puzzle, moves, size):
    """Picture of a puzzle after `moves` (for lessons and the reference)."""
    from .puzzles import Pyraminx, Skewb, sq1_polygons, sq1_slice_lines
    from .fastn import NState
    if puzzle in ("333", "333oh", "333bf", "333fm"):
        shapes = caseview.shapes(State().apply(moves), "full")
    elif puzzle in ("222", "444", "555", "666", "777"):
        n = int(puzzle[0])
        shapes = caseview.iso_grid(NState(n).apply(moves).facelets(), n)
    elif puzzle == "pyram":
        shapes = caseview._fit([("poly", a, b) for a, b in Pyraminx().apply(moves).polygons()])
    elif puzzle == "skewb":
        shapes = caseview._fit([("poly", a, b) for a, b in Skewb().apply(moves).polygons()])
    elif puzzle == "sq1":
        shapes = caseview._fit([("poly", a, b) for a, b in sq1_polygons(moves)] +
                               [("line", a, b) for a, b in sq1_slice_lines()])
    else:
        shapes = caseview._pentagon()
    img = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    p = QPainter(img)
    paint_shapes(p, QRectF(0, 0, size, size), shapes)
    p.end()
    return img


def state_image(state, view, size):
    img = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
    img.fill(Qt.transparent)
    p = QPainter(img)
    paint_shapes(p, QRectF(0, 0, size, size), caseview.shapes(state, view))
    p.end()
    return img


# ---------------------------------------------------------------------------
# Shared state
# ---------------------------------------------------------------------------

class TrainingHub(QObject):
    """Owns the progress data; every Training view listens to `changed`."""

    changed = pyqtSignal()

    def __init__(self, store, parent=None):
        QObject.__init__(self, parent)
        self.store = store
        self.progress = learn.Progress(store.training)
        self.path = store.settings.get("train_path") or "333"

    def save(self):
        self.store.settings["train_path"] = self.path
        try:
            self.store.save()
        except (IOError, OSError):
            pass
        self.changed.emit()


STATUS_COLORS = {learn.NEW: "#4a4644", learn.LEARNING: theme.ACCENT, learn.LEARNED: "#3ddc84"}


# ---------------------------------------------------------------------------
# Delegates
# ---------------------------------------------------------------------------

class LevelDelegate(QStyledItemDelegate):
    def __init__(self, hub, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.hub = hub

    def sizeHint(self, option, index):
        if str(index.data(ROLE_ID)).startswith("tier:"):
            return QSize(220, 30)
        return QSize(220, 62)

    def paint(self, p, option, index):
        lid = str(index.data(ROLE_ID))
        if lid.startswith("tier:"):
            p.save()
            f = QFont(theme.ui_font())
            f.setPixelSize(11)
            f.setBold(True)
            p.setFont(f)
            p.setPen(QColor(theme.FAINT))
            r = QRectF(option.rect).adjusted(12, 8, -8, 0)
            p.drawText(r, Qt.AlignLeft | Qt.AlignVCenter,
                       pick(learn.TIER_NAMES[lid[5:]]).upper())
            p.restore()
            return
        if lid == "overview":
            self._paint_overview(p, option)
            return
        lv = learn.LEVEL_BY_ID.get(lid)
        if lv is None:
            return
        prog = self.hub.progress
        path = learn.PATHS.get(self.hub.path, learn.L333)
        r = QRectF(option.rect).adjusted(4, 3, -4, -3)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        selected = bool(option.state & QStyle.State_Selected)
        hover = bool(option.state & QStyle.State_MouseOver)
        if selected or hover:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(theme.PANEL2 if selected else "#1d1c1c"))
            p.drawRoundedRect(r, 10, 10)
        done, total = prog.level_counts(lv)
        nxt = prog.next_level(self.hub.path)
        is_next = nxt is not None and nxt.id == lv.id
        # step marker
        mr = QRectF(r.left() + 10, r.top() + 12, 22, 22)
        p.setPen(Qt.NoPen)
        if done >= total:
            p.setBrush(QColor("#3ddc84"))
        elif is_next:
            p.setBrush(QColor(theme.ACCENT))
        else:
            p.setBrush(QColor("#2e2c2c"))
        p.drawEllipse(mr)
        f = QFont(theme.ui_font())
        f.setPixelSize(11)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor("#111111") if (done >= total or is_next) else QColor(theme.MUTED))
        num = (path.index(lv) + 1) if lv in path else 0
        p.drawText(mr, Qt.AlignCenter, "✓" if done >= total else str(num))
        # texts
        tx = mr.right() + 10
        f.setPixelSize(14)
        f.setBold(False)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(theme.TEXT))
        p.drawText(QRectF(tx, r.top() + 6, r.right() - tx - 8, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, pick(lv.name))
        f.setPixelSize(11)
        f.setWeight(QFont.Normal)
        p.setFont(f)
        p.setPen(QColor(theme.MUTED))
        sub = "%d / %d" % (done, total) if lv.set_id else pick(lv.subtitle)
        p.drawText(QRectF(tx, r.top() + 26, r.right() - tx - 8, 16),
                   Qt.AlignLeft | Qt.AlignVCenter, sub)
        # progress bar
        if lv.set_id:
            bar = QRectF(tx, r.bottom() - 10, r.right() - tx - 12, 3)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor("#2a2828"))
            p.drawRoundedRect(bar, 1.5, 1.5)
            if total:
                fill = QRectF(bar.left(), bar.top(), bar.width() * done / float(total), bar.height())
                p.setBrush(QColor("#3ddc84" if done >= total else theme.ACCENT))
                p.drawRoundedRect(fill, 1.5, 1.5)
        p.restore()


def _paint_overview_row(self, p, option):
    r = QRectF(option.rect).adjusted(4, 3, -4, -3)
    p.save()
    p.setRenderHint(QPainter.Antialiasing)
    selected = bool(option.state & QStyle.State_Selected)
    hover = bool(option.state & QStyle.State_MouseOver)
    if selected or hover:
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(theme.PANEL2 if selected else "#1d1c1c"))
        p.drawRoundedRect(r, 10, 10)
    done, total = self.hub.progress.course_counts(self.hub.path)
    mr = QRectF(r.left() + 10, r.top() + 12, 22, 22)
    p.setPen(QPen(QColor(theme.ACCENT), 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(mr.adjusted(1, 1, -1, -1))
    if total:
        p.setPen(QPen(QColor(theme.ACCENT), 2.2))
    f = QFont(theme.ui_font())
    f.setPixelSize(14)
    f.setWeight(QFont.DemiBold)
    p.setFont(f)
    p.setPen(QColor(theme.TEXT))
    tx = mr.right() + 10
    p.drawText(QRectF(tx, r.top() + 6, r.right() - tx - 8, 20), Qt.AlignLeft | Qt.AlignVCenter,
               tr("overview"))
    f.setPixelSize(11)
    f.setWeight(QFont.Normal)
    p.setFont(f)
    p.setPen(QColor(theme.MUTED))
    pct = int(round(100.0 * done / total)) if total else 0
    p.drawText(QRectF(tx, r.top() + 26, r.right() - tx - 8, 16), Qt.AlignLeft | Qt.AlignVCenter,
               tr("course_pct") % pct)
    p.restore()


LevelDelegate._paint_overview = _paint_overview_row


class OverviewView(QWidget):
    """Course home: overall progress, what to do next, all steps."""

    open_level = pyqtSignal(str)
    review_due = pyqtSignal()

    def __init__(self, hub, parent=None):
        QWidget.__init__(self, parent)
        self.hub = hub
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
        outer.addWidget(scroll)
        self.body = QWidget()
        scroll.setWidget(self.body)
        self.lay = QVBoxLayout(self.body)
        self.lay.setContentsMargins(0, 4, 8, 8)
        self.lay.setSpacing(10)

    def rebuild(self):
        lay = self.lay
        while lay.count():
            item = lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        prog = self.hub.progress
        pid = self.hub.path
        path = learn.PATHS[pid]

        # summary card
        card = QFrame()
        card.setObjectName("panel")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 16, 20, 18)
        cl.setSpacing(8)
        done, total = prog.course_counts(pid)
        steps_done = sum(1 for lv in path if prog.level_done(lv))
        head = QLabel(tr("course_steps") % (steps_done, len(path)))
        head.setStyleSheet("font-size: 18px; font-weight: 700;")
        cl.addWidget(head)
        bar = QProgressBar()
        bar.setRange(0, max(1, total))
        bar.setValue(done)
        bar.setTextVisible(False)
        bar.setFixedHeight(6)
        cl.addWidget(bar)
        cases_total = sum(len(lv.cases) for lv in path if lv.set_id)
        learned = sum(1 for lv in path if lv.set_id for c in lv.cases
                      if prog.status(c.id) == learn.LEARNED)
        due_cases = [c for lv in path if lv.set_id for c in lv.cases if prog.is_due(c.id)]
        info = QLabel(tr("course_info") % (learned, cases_total, len(due_cases)))
        info.setObjectName("muted")
        cl.addWidget(info)
        btns = QHBoxLayout()
        btns.setSpacing(8)
        nxt = prog.next_level(pid)
        if nxt is not None:
            b = _button("▶  " + tr("continue_with") % pick(nxt.name), "primary")
            b.clicked.connect(lambda _=False, lid=nxt.id: self.open_level.emit(lid))
            btns.addWidget(b)
        else:
            done_lbl = QLabel(tr("course_done"))
            done_lbl.setStyleSheet("color: #3ddc84; font-weight: 600;")
            btns.addWidget(done_lbl)
        if due_cases:
            b = _button(tr("review_now") % len(due_cases), "seg")
            b.clicked.connect(self.review_due.emit)
            btns.addWidget(b)
        btns.addStretch(1)
        cl.addLayout(btns)
        lay.addWidget(card)

        # steps
        tier = None
        for i, lv in enumerate(path):
            if lv.tier != tier:
                tier = lv.tier
                t = QLabel(pick(learn.TIER_NAMES[tier]).upper())
                t.setObjectName("sectionTitle")
                t.setContentsMargins(4, 8, 0, 0)
                lay.addWidget(t)
            row = QPushButton()
            row.setObjectName("steprow")
            row.setCursor(Qt.PointingHandCursor)
            row.setFocusPolicy(Qt.NoFocus)
            row.clicked.connect(lambda _=False, lid=lv.id: self.open_level.emit(lid))
            rl = QHBoxLayout(row)
            rl.setContentsMargins(14, 10, 14, 10)
            rl.setSpacing(12)
            a, b2 = prog.level_counts(lv)
            mark = QLabel("✓" if a >= b2 else str(i + 1))
            mark.setFixedSize(26, 26)
            mark.setAlignment(Qt.AlignCenter)
            colour = "#3ddc84" if a >= b2 else (theme.ACCENT if nxt is lv else "#2e2c2c")
            mark.setStyleSheet("background: %s; color: %s; border-radius: 13px; font-weight: 700;"
                               % (colour, "#111" if (a >= b2 or nxt is lv) else theme.MUTED))
            rl.addWidget(mark)
            texts = QVBoxLayout()
            texts.setSpacing(1)
            name = QLabel(pick(lv.name))
            name.setStyleSheet("font-size: 15px; font-weight: 600;")
            sub = QLabel(pick(lv.subtitle))
            sub.setObjectName("muted")
            texts.addWidget(name)
            texts.addWidget(sub)
            rl.addLayout(texts, 1)
            what = []
            if lv.lesson:
                what.append(tr("has_lesson"))
            if lv.set_id:
                what.append(tr("has_algs") % len(lv.cases))
            kind = QLabel("  ·  ".join(what))
            kind.setObjectName("muted")
            rl.addWidget(kind)
            cnt = QLabel("%d / %d" % (a, b2) if lv.set_id else (tr("done") if a else ""))
            cnt.setMinimumWidth(56)
            cnt.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            cnt.setStyleSheet("color: %s; font-weight: 600;" % ("#3ddc84" if a >= b2 else theme.MUTED))
            rl.addWidget(cnt)
            for w in (mark, name, sub, kind, cnt):
                w.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            lay.addWidget(row)
        lay.addStretch(1)


class CaseDelegate(QStyledItemDelegate):
    W, H = 150, 196

    def __init__(self, hub, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.hub = hub

    def sizeHint(self, option, index):
        return QSize(self.W, self.H)

    def paint(self, p, option, index):
        case = algs.CASES.get(index.data(ROLE_ID))
        if case is None:
            return
        r = QRectF(option.rect).adjusted(5, 5, -5, -5)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        selected = bool(option.state & QStyle.State_Selected)
        hover = bool(option.state & QStyle.State_MouseOver)
        p.setPen(QPen(QColor(theme.ACCENT), 1.5) if selected else Qt.NoPen)
        p.setBrush(QColor("#1f1e1e" if (hover or selected) else theme.PANEL))
        p.drawRoundedRect(r, 12, 12)
        img = 96
        pm = case_pixmap(case, img)
        p.drawPixmap(int(r.center().x() - img / 2), int(r.top() + 10), pm)
        # status dot
        st = self.hub.progress.status(case.id)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(STATUS_COLORS[st]))
        p.drawEllipse(QRectF(r.right() - 16, r.top() + 10, 7, 7))
        f = QFont(theme.ui_font())
        f.setPixelSize(13)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(theme.TEXT))
        ty = r.top() + 12 + img
        name = p.fontMetrics().elidedText(pick(case.name), Qt.ElideRight, int(r.width() - 16))
        p.drawText(QRectF(r.left() + 8, ty, r.width() - 16, 18),
                   Qt.AlignHCenter | Qt.AlignVCenter, name)
        f.setPixelSize(11)
        f.setWeight(QFont.Normal)
        p.setFont(f)
        p.setPen(QColor(theme.MUTED))
        p.drawText(QRectF(r.left() + 8, ty + 20, r.width() - 16, r.bottom() - ty - 24),
                   Qt.AlignHCenter | Qt.AlignTop | Qt.TextWordWrap, case.alg)
        p.restore()


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def _button(text, name=None, checkable=False):
    b = QPushButton(text)
    b.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    if name:
        b.setObjectName(name)
    b.setCheckable(checkable)
    b.setFocusPolicy(Qt.NoFocus)
    b.setCursor(Qt.PointingHandCursor)
    return b


class LessonBrowser(QTextBrowser):
    """QTextBrowser that renders move:/case: images itself."""

    def loadResource(self, rtype, url):
        if rtype == QTextDocument.ImageResource:
            s = unquote(url.toString())
            if s.startswith("move:"):
                rest = s[5:]
                puzzle, moves = (rest.split(":", 1) if ":" in rest else ("333", rest))
                return move_image(puzzle, moves, 200)
            if s.startswith("case:") and s[5:] in algs.CASES:
                c = algs.CASES[s[5:]]
                return case_pixmap(c, 120).toImage()
        return QTextBrowser.loadResource(self, rtype, url)


class CaseDetail(QFrame):
    train_requested = pyqtSignal(str)

    def __init__(self, hub, parent=None):
        QFrame.__init__(self, parent)
        self.setObjectName("panel")
        self.hub = hub
        self.case = None
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
        outer.addWidget(scroll)
        body = QWidget()
        scroll.setWidget(body)
        lay = QVBoxLayout(body)
        lay.setContentsMargins(18, 18, 18, 18)
        lay.setSpacing(8)
        self.img = QLabel()
        self.img.setAlignment(Qt.AlignCenter)
        self.img.setMinimumHeight(200)
        lay.addWidget(self.img)
        self.name = QLabel()
        self.name.setStyleSheet("font-size: 20px; font-weight: 700;")
        lay.addWidget(self.name)
        self.group = QLabel()
        self.group.setObjectName("muted")
        lay.addWidget(self.group)
        self.alg = QLabel()
        self.alg.setWordWrap(True)
        self.alg.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.alg.setStyleSheet("font-size: 18px; font-weight: 600; color: %s; padding: 8px 0;"
                               % theme.ACCENT)
        lay.addWidget(self.alg)
        self.hint = QLabel()
        self.hint.setWordWrap(True)
        self.hint.setStyleSheet("color: %s;" % theme.SCRAMBLE)
        lay.addWidget(self.hint)
        self.facts = QLabel()
        self.facts.setWordWrap(True)
        self.facts.setTextFormat(Qt.RichText)
        self.facts.setStyleSheet("color: %s; font-size: 13px;" % theme.SCRAMBLE)
        lay.addWidget(self.facts)
        self.alts_title = QLabel(tr("alternatives").upper())
        self.alts_title.setObjectName("sectionTitle")
        lay.addWidget(self.alts_title)
        self.alts = QLabel()
        self.alts.setWordWrap(True)
        self.alts.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.alts.setStyleSheet("font-size: 14px; font-weight: 600; color: %s;" % theme.TEXT)
        lay.addWidget(self.alts)
        self.setup = QLabel()
        self.setup.setWordWrap(True)
        self.setup.setObjectName("muted")
        self.setup.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lay.addWidget(self.setup)
        lay.addSpacing(6)
        st_row = QHBoxLayout()
        st_row.setSpacing(4)
        self.st_group = QButtonGroup(self)
        self.st_group.setExclusive(True)
        for i, key in enumerate(("st_new", "st_learning", "st_learned")):
            b = _button(tr(key), "seg", True)
            self.st_group.addButton(b, i)
            st_row.addWidget(b)
        self.st_group.buttonClicked[int].connect(self._set_status)
        lay.addLayout(st_row)
        self.train_btn = _button(tr("train_case"), "primary")
        self.train_btn.clicked.connect(lambda: self.case and self.train_requested.emit(self.case.id))
        lay.addWidget(self.train_btn)
        lay.addStretch(1)
        self.empty = QLabel(tr("select_case"))
        self.empty.setObjectName("muted")
        self.empty.setWordWrap(True)
        self.empty.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.empty)
        self.show_case(None)

    def show_case(self, case):
        self.case = case
        widgets = (self.img, self.name, self.group, self.alg, self.hint, self.setup,
                   self.train_btn, self.facts, self.alts, self.alts_title)
        for w in widgets:
            w.setVisible(case is not None)
        for b in self.st_group.buttons():
            b.setVisible(case is not None)
        self.empty.setVisible(case is None)
        if case is None:
            return
        self.img.setPixmap(case_pixmap(case, 200))
        self.name.setText(pick(case.name))
        self.group.setText(pick(case.group) if case.group else "")
        self.group.setVisible(bool(case.group))
        self.alg.setText(case.alg)
        self.hint.setText(pick(case.hint) if case.hint else "")
        self.hint.setVisible(bool(case.hint))
        self.setup.setText(tr("setup_hint") % case.setup())
        facts = insights.facts(case)
        self.facts.setText("<br>".join("• " + pick(f) for f in facts))
        self.alts.setText("\n\n".join(case.alts))
        self.alts.setVisible(bool(case.alts))
        self.alts_title.setVisible(bool(case.alts))
        self.refresh()

    def refresh(self):
        if self.case is None:
            return
        st = self.hub.progress.status(self.case.id)
        b = self.st_group.button(st)
        if b:
            b.setChecked(True)

    def _set_status(self, idx):
        if self.case is not None:
            self.hub.progress.set_status(self.case.id, idx)
            self.hub.save()


class TrainerView(QWidget):
    """Spaced-repetition trainer: recognise, solve, reveal, rate."""

    closed = pyqtSignal()

    def __init__(self, hub, parent=None):
        QWidget.__init__(self, parent)
        self.hub = hub
        self.trainer = None
        self.case = None
        self.auf = ""
        self.revealed = False
        self.title_text = ""
        self.setFocusPolicy(Qt.StrongFocus)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 4, 8, 8)
        lay.setSpacing(10)
        top = QHBoxLayout()
        back = _button("←  " + tr("back"))
        back.clicked.connect(self.stop)
        top.addWidget(back)
        top.addStretch(1)
        lay.addLayout(top)
        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: 700;")
        lay.addWidget(self.title)
        self.stats = QLabel()
        self.stats.setAlignment(Qt.AlignCenter)
        self.stats.setObjectName("muted")
        lay.addWidget(self.stats)
        lay.addStretch(1)

        self.img = QLabel()
        self.img.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.img)
        self.setup = QLabel()
        self.setup.setAlignment(Qt.AlignCenter)
        self.setup.setWordWrap(True)
        self.setup.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setup.setStyleSheet("color: %s; font-size: 15px;" % theme.MUTED)
        lay.addWidget(self.setup)
        lay.addSpacing(10)
        self.answer = QLabel()
        self.answer.setAlignment(Qt.AlignCenter)
        self.answer.setWordWrap(True)
        self.answer.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.answer.setMinimumHeight(60)
        lay.addWidget(self.answer)

        self.reveal_btn = _button(tr("reveal") + "  ␣", "primary")
        self.reveal_btn.clicked.connect(self.reveal)
        row0 = QHBoxLayout()
        row0.addStretch(1)
        row0.addWidget(self.reveal_btn)
        row0.addStretch(1)
        lay.addLayout(row0)
        self.rate_row = QWidget()
        rr = QHBoxLayout(self.rate_row)
        rr.setContentsMargins(0, 0, 0, 0)
        rr.addStretch(1)
        for key, val in (("r_again", learn.AGAIN), ("r_hard", learn.HARD), ("r_good", learn.GOOD)):
            b = _button(tr(key), "rate")
            b.setMinimumWidth(130)
            b.clicked.connect(lambda _=False, v=val: self.rate(v))
            rr.addWidget(b)
        rr.addStretch(1)
        lay.addWidget(self.rate_row)

        # recognition quiz: four names to choose from
        self.quiz_row = QWidget()
        qr = QGridLayout(self.quiz_row)
        qr.setContentsMargins(0, 0, 0, 0)
        qr.setHorizontalSpacing(8)
        qr.setVerticalSpacing(8)
        self.quiz_btns = []
        for i in range(4):
            b = _button("", "rate")
            b.setMinimumWidth(230)
            b.clicked.connect(lambda _=False, k=i: self.answer_quiz(k))
            qr.addWidget(b, i // 2, i % 2)
            self.quiz_btns.append(b)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.quiz_row)
        row.addStretch(1)
        lay.addLayout(row)
        self.next_btn = _button(tr("next") + "  ␣", "primary")
        self.next_btn.clicked.connect(self.next)
        row2 = QHBoxLayout()
        row2.addStretch(1)
        row2.addWidget(self.next_btn)
        row2.addStretch(1)
        lay.addLayout(row2)
        lay.addStretch(2)
        self.mode = "review"
        self.options = []
        self.answered = False
        self.quiz_right = 0
        self.quiz_total = 0

    def start(self, title, cases, mode="review"):
        self.title_text = title
        self.mode = mode if len(cases) >= 4 else "review"
        self.trainer = learn.Trainer(self.hub.progress, cases)
        self.quiz_right = self.quiz_total = 0
        key = "quiz_title" if self.mode == "quiz" else "trainer_title"
        self.title.setText(tr(key) % title)
        self.next()
        self.setFocus()

    def stop(self):
        self.trainer = None
        self.closed.emit()

    def next(self):
        if not self.trainer:
            return
        if self.mode == "quiz":
            self._next_quiz()
            return
        self.quiz_row.setVisible(False)
        self.next_btn.setVisible(False)
        self.setup.setVisible(True)
        self.case = self.trainer.next_case()
        self.auf = learn.random_auf() if self.case.view in ("oll", "pll") else ""
        self.revealed = False
        self.img.setPixmap(case_pixmap(self.case, 260, self.auf, arrows=False))
        self.setup.setText(tr("setup_hint") % (self.case.setup() + (" " + self.auf if self.auf else "")))
        self.answer.setText(tr("reveal_hint"))
        self.answer.setStyleSheet("color: %s; font-size: 14px;" % theme.FAINT)
        self.reveal_btn.setVisible(True)
        self.rate_row.setVisible(False)
        self._stats()

    def _next_quiz(self):
        cases = self.trainer.cases
        self.case = random.choice([c for c in cases if c is not self.case] or cases)
        same = [c for c in cases if c is not self.case and c.group == self.case.group]
        other = [c for c in cases if c is not self.case and c not in same]
        random.shuffle(same)
        random.shuffle(other)
        self.options = (same + other)[:3] + [self.case]
        random.shuffle(self.options)
        self.answered = False
        self.auf = learn.random_auf() if self.case.view in ("oll", "pll", "cmll") else ""
        self.img.setPixmap(case_pixmap(self.case, 260, self.auf, arrows=False))
        self.setup.setVisible(False)
        self.reveal_btn.setVisible(False)
        self.rate_row.setVisible(False)
        self.quiz_row.setVisible(True)
        self.next_btn.setVisible(False)
        for i, (b, c) in enumerate(zip(self.quiz_btns, self.options)):
            b.setText("%d   %s" % (i + 1, pick(c.name)))
            b.setStyleSheet("")
            b.setEnabled(True)
        self.answer.setText(tr("quiz_hint"))
        self.answer.setStyleSheet("color: %s; font-size: 14px;" % theme.FAINT)
        self._stats()

    def answer_quiz(self, k):
        if self.mode != "quiz" or self.answered or k >= len(self.options):
            return
        self.answered = True
        right = self.options[k] is self.case
        self.quiz_total += 1
        self.quiz_right += int(right)
        q = self.hub.progress.data.setdefault("quiz", {"right": 0, "total": 0})
        q["total"] += 1
        q["right"] += int(right)
        for b, c in zip(self.quiz_btns, self.options):
            b.setEnabled(False)
            if c is self.case:
                b.setStyleSheet("background: #1f4d33; color: #3ddc84;")
        if not right:
            self.quiz_btns[k].setStyleSheet("background: #4d1f22; color: #ff6b6f;")
        verdict = tr("quiz_right") if right else tr("quiz_wrong")
        self.answer.setText("%s\n%s" % (verdict, self.case.alg))
        self.answer.setStyleSheet("color: %s; font-size: 20px; font-weight: 600;"
                                  % ("#3ddc84" if right else theme.ACCENT))
        self.next_btn.setVisible(True)
        self.hub.save()
        self._stats()

    def reveal(self):
        if not self.case or self.revealed:
            return
        self.revealed = True
        pre = {"": "", "U": "U'", "U'": "U", "U2": "U2"}[self.auf]
        self.answer.setText("%s\n%s" % (pick(self.case.name), ((pre + " ") if pre else "") + self.case.alg))
        self.answer.setStyleSheet("color: %s; font-size: 22px; font-weight: 600;" % theme.ACCENT)
        self.reveal_btn.setVisible(False)
        self.rate_row.setVisible(True)

    def rate(self, rating):
        if not self.case or not self.revealed or not self.trainer:
            return
        self.trainer.rate(self.case, rating)
        self.hub.save()
        self.next()

    def _stats(self):
        if self.trainer and self.mode == "quiz":
            self.stats.setText(tr("quiz_stats") % (self.quiz_right, self.quiz_total))
        elif self.trainer:
            due = self.hub.progress.due_count(self.trainer.cases)
            self.stats.setText(tr("session_stats") % (self.trainer.reviewed, due))

    def keyPressEvent(self, e):
        k = e.key()
        if self.mode == "quiz":
            if k in (Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4):
                self.answer_quiz(k - Qt.Key_1)
            elif k in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter) and self.answered:
                self.next()
            elif k == Qt.Key_Escape:
                self.stop()
            return
        if k == Qt.Key_Space:
            self.reveal()
        elif k in (Qt.Key_1, Qt.Key_2, Qt.Key_3):
            self.rate({Qt.Key_1: learn.AGAIN, Qt.Key_2: learn.HARD, Qt.Key_3: learn.GOOD}[k])
        elif k == Qt.Key_Escape:
            self.stop()
        else:
            QWidget.keyPressEvent(self, e)


class TrainingWidget(QWidget):
    """Sidebar with the learning path + level page + case details + trainer."""

    def __init__(self, hub, standalone=False, parent=None):
        QWidget.__init__(self, parent)
        self.hub = hub
        self.level = None
        self.filter = "all"
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(20)

        # --- sidebar -------------------------------------------------------
        side = QFrame()
        side.setObjectName("panel")
        side.setFixedWidth(250)
        sv = QVBoxLayout(side)
        sv.setContentsMargins(10, 14, 10, 10)
        sv.setSpacing(6)
        course = QLabel(tr("path").upper())
        course.setObjectName("sectionTitle")
        course.setContentsMargins(8, 0, 0, 0)
        sv.addWidget(course)
        head = QHBoxLayout()
        self.path_combo = QComboBox()
        self.path_combo.setFocusPolicy(Qt.NoFocus)
        for pid in learn.PATH_ORDER:
            self.path_combo.addItem(pick(learn.PATH_NAMES[pid]), pid)
        self.path_combo.currentIndexChanged.connect(self._path_changed)
        head.addWidget(self.path_combo, 1)
        sv.addLayout(head)
        self.levels = QListWidget()
        self.levels.setObjectName("levels")
        self.levels.setItemDelegate(LevelDelegate(hub, self.levels))
        self.levels.setMouseTracking(True)
        self.levels.setFocusPolicy(Qt.NoFocus)
        self.levels.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.levels.currentRowChanged.connect(self._level_changed)
        sv.addWidget(self.levels, 1)
        root.addWidget(side)

        # --- centre ----------------------------------------------------------
        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        page = QWidget()
        pv = QVBoxLayout(page)
        pv.setContentsMargins(4, 4, 0, 0)
        pv.setSpacing(10)
        self.title = QLabel()
        self.title.setStyleSheet("font-size: 26px; font-weight: 700;")
        pv.addWidget(self.title)
        self.subtitle = QLabel()
        self.subtitle.setObjectName("muted")
        self.subtitle.setWordWrap(True)
        pv.addWidget(self.subtitle)
        bar = QHBoxLayout()
        bar.setSpacing(4)
        self.train_btn = _button("▶  " + tr("train"), "primary")
        self.train_btn.clicked.connect(self.train_level)
        bar.addWidget(self.train_btn)
        self.quiz_btn = _button("?  " + tr("quiz"), "seg")
        self.quiz_btn.setToolTip(tr("quiz_tip"))
        self.quiz_btn.clicked.connect(lambda: self.train_level("quiz"))
        bar.addWidget(self.quiz_btn)
        self.lesson_btn = _button(tr("mark_lesson"), "seg", True)
        self.lesson_btn.clicked.connect(self._toggle_lesson)
        bar.addWidget(self.lesson_btn)
        bar.addSpacing(14)
        self.progress_lbl = QLabel()
        self.progress_lbl.setObjectName("muted")
        bar.addWidget(self.progress_lbl)
        bar.addStretch(1)
        pv.addLayout(bar)
        bar = QHBoxLayout()
        bar.setSpacing(4)
        self.view_group = QButtonGroup(self)
        self.view_group.setExclusive(True)
        self.view_btns = {}
        for i, key in enumerate(("lesson", "algorithms")):
            b = _button(tr(key), "tab", True)
            self.view_group.addButton(b, i)
            self.view_btns[key] = b
            bar.addWidget(b)
        self.view_group.buttonClicked[int].connect(self._view_changed)
        bar.addStretch(1)
        self.filter_group = QButtonGroup(self)
        self.filter_group.setExclusive(True)
        self.filter_btns = []
        for i, key in enumerate(("f_all", "f_new", "f_learning", "f_learned")):
            b = _button(tr(key), "tab", True)
            b.setChecked(i == 0)
            self.filter_group.addButton(b, i)
            self.filter_btns.append(b)
            bar.addWidget(b)
        self.filter_group.buttonClicked[int].connect(self._filter_changed)
        pv.addLayout(bar)

        self.content = QStackedWidget()
        self.lesson = LessonBrowser()
        self.lesson.setOpenExternalLinks(True)
        self.content.addWidget(self.lesson)
        self.grid = QListWidget()
        self.grid.setObjectName("grid")
        self.grid.setViewMode(QListView.IconMode)
        self.grid.setResizeMode(QListView.Adjust)
        self.grid.setMovement(QListView.Static)
        self.grid.setUniformItemSizes(True)
        self.grid.setSpacing(4)
        self.grid.setMouseTracking(True)
        self.grid.setFocusPolicy(Qt.NoFocus)
        self.grid.setSelectionMode(QAbstractItemView.SingleSelection)
        self.grid.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grid.setItemDelegate(CaseDelegate(hub, self.grid))
        self.grid.currentItemChanged.connect(self._case_changed)
        self.content.addWidget(self.grid)
        self.empty = QLabel(tr("empty_filter"))
        self.empty.setObjectName("muted")
        self.empty.setAlignment(Qt.AlignCenter)
        self.content.addWidget(self.empty)
        self.overview = OverviewView(hub)
        self.overview.open_level.connect(self.select_level)
        self.overview.review_due.connect(self._review_due)
        self.content.addWidget(self.overview)
        self._on_overview = False
        pv.addWidget(self.content, 1)
        self.stack.addWidget(page)

        self.trainer = TrainerView(hub)
        self.trainer.closed.connect(self._trainer_closed)
        self.stack.addWidget(self.trainer)

        # --- details ---------------------------------------------------------
        self.detail = CaseDetail(hub)
        self.detail.setFixedWidth(300)
        self.detail.train_requested.connect(self.train_case)
        root.addWidget(self.detail)

        hub.changed.connect(self.refresh)
        idx = self.path_combo.findData(hub.path)
        self.path_combo.setCurrentIndex(max(0, idx))
        if self.levels.count() == 0:
            self._path_changed(max(0, idx))

    # ------------------------------------------------------------------
    def _path_changed(self, idx):
        pid = self.path_combo.itemData(idx) or "333"
        self.hub.path = pid
        self.level = None
        self.levels.blockSignals(True)
        self.levels.clear()
        ov = QListWidgetItem()
        ov.setData(ROLE_ID, "overview")
        self.levels.addItem(ov)
        tier = None
        for lv in learn.PATHS[pid]:
            if lv.tier != tier:
                tier = lv.tier
                head = QListWidgetItem()
                head.setData(ROLE_ID, "tier:" + tier)
                head.setFlags(Qt.NoItemFlags)
                self.levels.addItem(head)
            it = QListWidgetItem()
            it.setData(ROLE_ID, lv.id)
            self.levels.addItem(it)
        self.levels.blockSignals(False)
        self.select_level("overview")

    def select_level(self, level_id):
        for row in range(self.levels.count()):
            if self.levels.item(row).data(ROLE_ID) == level_id:
                self.levels.setCurrentRow(row)
                if self.level is None or self.level.id != level_id:
                    self._level_changed(row)
                return

    def _show_overview(self):
        self.level = None
        self.stack.setCurrentIndex(0)
        self.title.setText(pick(learn.PATH_NAMES[self.hub.path]))
        self.subtitle.setText(pick(learn.PATH_DESCRIPTIONS.get(self.hub.path, ("", ""))))
        for w in (self.train_btn, self.quiz_btn, self.lesson_btn, self.progress_lbl):
            w.setVisible(False)
        for b in list(self.view_btns.values()) + self.filter_btns:
            b.setVisible(False)
        self.overview.rebuild()
        self.content.setCurrentWidget(self.overview)
        self.detail.setVisible(False)
        self._on_overview = True

    def _review_due(self):
        path = learn.PATHS[self.hub.path]
        due = [c for lv in path if lv.set_id for c in lv.cases if self.hub.progress.is_due(c.id)]
        if due:
            self.stack.setCurrentIndex(1)
            self._update_detail_visibility()
            self.trainer.start(tr("due_title"), due)

    def _level_changed(self, row):
        if row < 0 or self.levels.item(row) is None:
            return
        if self.levels.item(row).data(ROLE_ID) == "overview":
            self._show_overview()
            return
        self._on_overview = False
        self.progress_lbl.setVisible(True)
        lv = learn.LEVEL_BY_ID.get(self.levels.item(row).data(ROLE_ID))
        if lv is None:
            return
        self.level = lv
        self.stack.setCurrentIndex(0)
        self.title.setText(pick(lv.name))
        desc = pick(algs.SET_BY_ID[lv.set_id].description) if lv.set_id else pick(lv.subtitle)
        self.subtitle.setText(desc)
        has_lesson = bool(lv.lesson)
        has_cases = bool(lv.set_id)
        if has_lesson:
            self.lesson.setHtml(lesson_html(lv.lesson, lang()))
        self.view_btns["lesson"].setVisible(has_lesson and has_cases)
        self.view_btns["algorithms"].setVisible(has_lesson and has_cases)
        for b in self.filter_btns:
            b.setVisible(has_cases)
        self.train_btn.setVisible(has_cases)
        pictures = has_cases and lv.cases[0].view != "none"
        self.quiz_btn.setVisible(pictures and len(lv.cases) >= 4)
        self.lesson_btn.setVisible(has_lesson)
        start_on_lesson = has_lesson and (not has_cases or not self.hub.progress.lesson_done(lv.lesson))
        idx = 0 if start_on_lesson else 1
        self.content.setCurrentIndex(idx)
        self.stack.setCurrentIndex(0)
        b = self.view_group.button(idx)
        if b:
            b.setChecked(True)
        self._fill_grid()
        self.detail.show_case(None)
        self._update_detail_visibility()
        self.refresh()

    def _view_changed(self, idx):
        self.content.setCurrentIndex(idx if (idx == 0 or self.grid.count()) else 2)
        self._update_detail_visibility()

    def _update_detail_visibility(self):
        """The case panel only makes sense next to the grid of cases."""
        on_grid = (self.stack.currentIndex() == 0 and self.content.currentIndex() in (1, 2)
                   and not getattr(self, "_on_overview", False))
        self.detail.setVisible(on_grid)
        for b in self.filter_btns:
            b.setVisible(on_grid)

    def _trainer_closed(self):
        self.stack.setCurrentIndex(0)
        if getattr(self, "_on_overview", False):
            self.overview.rebuild()
        self._update_detail_visibility()

    def _filter_changed(self, idx):
        self.filter = ("all", "new", "learning", "learned")[idx]
        self._fill_grid()
        if self.content.currentIndex() == 0 and self.level and self.level.lesson:
            return
        self.content.setCurrentIndex(1 if self.grid.count() else 2)
        self._update_detail_visibility()

    def _visible_cases(self):
        if not self.level or not self.level.set_id:
            return []
        want = {"all": None, "new": learn.NEW, "learning": learn.LEARNING,
                "learned": learn.LEARNED}[self.filter]
        prog = self.hub.progress
        return [c for c in self.level.cases if want is None or prog.status(c.id) == want]

    def _fill_grid(self):
        self.grid.clear()
        for c in self._visible_cases():
            it = QListWidgetItem()
            it.setData(ROLE_ID, c.id)
            it.setSizeHint(QSize(CaseDelegate.W, CaseDelegate.H))
            it.setToolTip(c.alg)
            self.grid.addItem(it)

    def _case_changed(self, cur, prev):
        self.detail.show_case(algs.CASES.get(cur.data(ROLE_ID)) if cur else None)

    def _toggle_lesson(self):
        if self.level and self.level.lesson:
            prog = self.hub.progress
            prog.set_lesson_done(self.level.lesson, not prog.lesson_done(self.level.lesson))
            self.hub.save()

    def refresh(self):
        self.levels.viewport().update()
        self.grid.viewport().update()
        self.detail.refresh()
        if getattr(self, "_on_overview", False) and self.stack.currentIndex() == 0:
            self.overview.rebuild()
        lv = self.level
        if lv is None:
            return
        prog = self.hub.progress
        if lv.set_id:
            done, total = prog.level_counts(lv)
            due = prog.due_count(lv.cases)
            txt = tr("learned_of") % (done, total)
            if due:
                txt += "  ·  " + tr("due_now") % due
            self.progress_lbl.setText(txt)
        else:
            self.progress_lbl.setText("")
        if lv.lesson:
            d = prog.lesson_done(lv.lesson)
            self.lesson_btn.setChecked(d)
            self.lesson_btn.setText(tr("lesson_done") if d else tr("mark_lesson"))

    def train_level(self, mode="review"):
        if self.level and self.level.set_id:
            self.stack.setCurrentIndex(1)
            self._update_detail_visibility()
            self.trainer.start(pick(self.level.name), self.level.cases,
                               mode if isinstance(mode, str) else "review")

    def train_case(self, cid):
        case = algs.CASES.get(cid)
        if case:
            self.stack.setCurrentIndex(1)
            self._update_detail_visibility()
            self.trainer.start(pick(case.name), [case])


__all__ = ["TrainingHub", "TrainingWidget"]
