# -*- coding: utf-8 -*-
"""Reference (notation for every puzzle) and Achievements pages."""

import time

from PyQt5.QtCore import QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (QAbstractItemView, QFrame, QHBoxLayout, QLabel, QListView,
                             QListWidget, QListWidgetItem, QStyle, QStyledItemDelegate,
                             QVBoxLayout, QWidget)

from . import achievements as ach
from . import reference, theme
from .i18n import lang, pick, tr
from .training import LessonBrowser

ROLE = Qt.UserRole + 7


class ReferencePage(QWidget):
    """Notation reference: list of puzzles on the left, notation on the right."""

    def __init__(self, hub, parent=None):
        QWidget.__init__(self, parent)
        self.hub = hub
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(20)
        side = QFrame()
        side.setObjectName("panel")
        side.setFixedWidth(250)
        sv = QVBoxLayout(side)
        sv.setContentsMargins(10, 14, 10, 10)
        t = QLabel(tr("reference").upper())
        t.setObjectName("sectionTitle")
        sv.addWidget(t)
        self.list = QListWidget()
        self.list.setObjectName("plainlist")
        self.list.setFocusPolicy(Qt.NoFocus)
        for pid, name in reference.PUZZLES:
            it = QListWidgetItem(pick(name))
            it.setData(ROLE, pid)
            it.setSizeHint(QSize(200, 40))
            self.list.addItem(it)
        self.list.currentRowChanged.connect(self._show)
        sv.addWidget(self.list, 1)
        root.addWidget(side)
        self.text = LessonBrowser()
        root.addWidget(self.text, 1)
        self.list.setCurrentRow(0)
        if not self.text.toPlainText():
            self._show(0)

    def _show(self, row):
        it = self.list.item(row)
        if it is None:
            return
        self.text.setHtml(reference.html(it.data(ROLE), lang()))

    def show_puzzle(self, pid):
        for row in range(self.list.count()):
            if self.list.item(row).data(ROLE) == pid:
                self.list.setCurrentRow(row)
                return


class BadgeDelegate(QStyledItemDelegate):
    W, H = 236, 112

    def __init__(self, page, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.page = page

    def sizeHint(self, option, index):
        return QSize(self.W, self.H)

    def paint(self, p, option, index):
        a = ach.BY_ID.get(index.data(ROLE))
        if a is None:
            return
        unlocked = self.page.unlocked.get(a["id"])
        value, target = self.page.status.get(a["id"], (0, 1))
        r = QRectF(option.rect).adjusted(5, 5, -5, -5)
        p.save()
        p.setRenderHint(QPainter.Antialiasing)
        hover = bool(option.state & QStyle.State_MouseOver)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor("#1f1e1e" if hover else theme.PANEL))
        p.drawRoundedRect(r, 12, 12)
        # badge
        b = QRectF(r.left() + 14, r.top() + 16, 52, 52)
        if unlocked:
            p.setBrush(QColor(theme.ACCENT))
            p.drawEllipse(b)
            p.setPen(QColor("#111111"))
        else:
            p.setPen(QPen(QColor("#3a3737"), 2))
            p.setBrush(Qt.NoBrush)
            p.drawEllipse(b.adjusted(1, 1, -1, -1))
            p.setPen(QColor(theme.FAINT))
        f = QFont(theme.ui_font())
        f.setPixelSize(15 if len(a["badge"]) <= 3 else 12)
        f.setBold(True)
        p.setFont(f)
        p.drawText(b, Qt.AlignCenter, a["badge"])
        # texts
        tx = b.right() + 14
        f.setPixelSize(14)
        f.setBold(False)
        f.setWeight(QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(theme.TEXT if unlocked else theme.MUTED))
        p.drawText(QRectF(tx, r.top() + 12, r.right() - tx - 10, 20),
                   Qt.AlignLeft | Qt.AlignVCenter, pick(a["name"]))
        f.setPixelSize(11)
        f.setWeight(QFont.Normal)
        p.setFont(f)
        p.setPen(QColor(theme.MUTED))
        p.drawText(QRectF(tx, r.top() + 34, r.right() - tx - 10, 34),
                   Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, pick(a["desc"]))
        if unlocked:
            p.setPen(QColor(theme.ACCENT))
            p.drawText(QRectF(tx, r.bottom() - 22, r.right() - tx - 10, 16),
                       Qt.AlignLeft | Qt.AlignVCenter,
                       time.strftime("%d.%m.%Y", time.localtime(unlocked)))
        elif target > 1:
            label = "%d/%d" % (value, target)
            lw = p.fontMetrics().boundingRect(label).width() + 10
            bar = QRectF(tx, r.bottom() - 16, max(20.0, r.right() - tx - 14 - lw), 4)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor("#2a2828"))
            p.drawRoundedRect(bar, 2, 2)
            p.setBrush(QColor(theme.ACCENT))
            p.drawRoundedRect(QRectF(bar.left(), bar.top(),
                                     bar.width() * min(1.0, value / float(target)), 4), 2, 2)
            p.setPen(QColor(theme.FAINT))
            p.drawText(QRectF(bar.right() + 4, r.bottom() - 24, r.right() - bar.right() - 12, 20),
                       Qt.AlignRight | Qt.AlignVCenter, label)
        p.restore()


class AchievementsPage(QWidget):
    def __init__(self, store, parent=None):
        QWidget.__init__(self, parent)
        self.store = store
        self.unlocked = {}
        self.status = {}
        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 0, 0)
        lay.setSpacing(8)
        self.title = QLabel(tr("achievements"))
        self.title.setStyleSheet("font-size: 26px; font-weight: 700;")
        lay.addWidget(self.title)
        self.summary = QLabel()
        self.summary.setObjectName("muted")
        lay.addWidget(self.summary)
        self.grid = QListWidget()
        self.grid.setObjectName("grid")
        self.grid.setViewMode(QListView.IconMode)
        self.grid.setResizeMode(QListView.Adjust)
        self.grid.setMovement(QListView.Static)
        self.grid.setUniformItemSizes(True)
        self.grid.setSelectionMode(QAbstractItemView.NoSelection)
        self.grid.setFocusPolicy(Qt.NoFocus)
        self.grid.setMouseTracking(True)
        self.grid.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.grid.setItemDelegate(BadgeDelegate(self, self.grid))
        lay.addWidget(self.grid, 1)
        self.refresh()

    def refresh(self):
        _new, self.status = ach.check(self.store)
        self.unlocked = self.store.training.get("ach", {})
        self.grid.clear()
        order = sorted(ach.A, key=lambda a: (a["id"] not in self.unlocked,
                                             a["cat"] != ach.SOLVING))
        for a in order:
            it = QListWidgetItem()
            it.setData(ROLE, a["id"])
            it.setSizeHint(QSize(BadgeDelegate.W, BadgeDelegate.H))
            self.grid.addItem(it)
        self.summary.setText(tr("ach_summary") % (len(self.unlocked), len(ach.A)))
