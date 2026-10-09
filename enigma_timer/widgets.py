"""Custom painted widgets: big timer, scramble preview, progress chart."""

from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPolygonF
from PyQt5.QtWidgets import QLabel, QToolTip, QWidget

from . import theme
from .cube import Cube, FACE_COLORS
from .i18n import tr
from .puzzles import Pyraminx, Skewb, sq1_polygons, sq1_slice_lines
from .scramble import CUBE_SIZE
from .stats import INF, fmt_ms, fmt_avg


class TimerDisplay(QWidget):
    """Huge auto-scaling time readout. Mouse press/release act like Space."""

    pressed = pyqtSignal()
    released = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._text = "0.00"
        self._sub = ""
        self._color = QColor(theme.TEXT)
        self.setMinimumHeight(140)
        self.setCursor(Qt.PointingHandCursor)

    def set_display(self, text, color=None, sub=""):
        color = QColor(color or theme.TEXT)
        if text != self._text or sub != self._sub or color != self._color:
            self._text, self._sub, self._color = text, sub, color
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        r = self.rect()
        sub_h = int(r.height() * 0.16) if self._sub else 0
        main = r.adjusted(0, 0, 0, -sub_h)
        size = min(main.height() * 0.72, r.width() * 1.55 / max(4, len(self._text)))
        f = QFont(theme.ui_font())
        f.setPixelSize(max(14, int(size)))
        f.setWeight(QFont.Medium)
        f.setLetterSpacing(QFont.PercentageSpacing, 98)
        p.setFont(f)
        p.setPen(self._color)
        p.drawText(main, Qt.AlignCenter, self._text)
        if self._sub:
            f2 = QFont(theme.ui_font())
            px = int(min(sub_h * 0.5, r.width() * 1.7 / max(10, len(self._sub))))
            f2.setPixelSize(max(11, px))
            p.setFont(f2)
            p.setPen(QColor(theme.MUTED))
            p.drawText(r.adjusted(0, r.height() - sub_h - 4, 0, 0),
                       Qt.AlignHCenter | Qt.AlignTop, self._sub)
        p.end()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.pressed.emit()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.released.emit()


class ScramblePreview(QWidget):
    """Draws the scrambled state: cube nets, Pyraminx, Skewb and Square-1."""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._grid = None
        self._n = 0
        self._polys = None
        self._lines = []
        self.setMinimumSize(200, 150)

    def set_scramble(self, puzzle, scramble):
        self._grid, self._n, self._polys, self._lines = None, 0, None, []
        try:
            n = CUBE_SIZE.get(puzzle)
            if n:
                self._n = n
                self._grid = Cube(n).apply(scramble).facelets()
            elif puzzle == "pyram":
                self._polys = Pyraminx().apply(scramble).polygons()
            elif puzzle == "skewb":
                self._polys = Skewb().apply(scramble).polygons()
            elif puzzle == "sq1":
                self._polys = sq1_polygons(scramble)
                self._lines = sq1_slice_lines()
        except Exception:  # noqa: BLE001 - a preview must never break the timer
            self._grid, self._polys = None, None
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(8, 8, -8, -8)
        if self._grid:
            self._paint_cube(p, r)
        elif self._polys:
            self._paint_polys(p, r)
        else:
            p.setPen(QColor(theme.MUTED))
            p.drawText(r, Qt.AlignCenter | Qt.TextWordWrap, tr("preview_na"))
        p.end()

    def _paint_polys(self, p, r):
        xs = [pt[0] for poly, _ in self._polys for pt in poly]
        ys = [pt[1] for poly, _ in self._polys for pt in poly]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        scale = min(r.width() / max(1e-6, x1 - x0), r.height() / max(1e-6, y1 - y0))
        ox = r.x() + (r.width() - (x1 - x0) * scale) / 2.0
        oy = r.y() + (r.height() - (y1 - y0) * scale) / 2.0

        def T(pt):
            return QPointF(ox + (pt[0] - x0) * scale, oy + (pt[1] - y0) * scale)

        pen = QPen(QColor("#000000"), max(1.0, scale * 0.03))
        pen.setJoinStyle(Qt.RoundJoin)
        p.setPen(pen)
        cache = {}
        for poly, col in self._polys:
            if col not in cache:
                cache[col] = QColor(col)
            p.setBrush(cache[col])
            p.drawPolygon(QPolygonF([T(pt) for pt in poly]))
        if self._lines:
            p.setPen(QPen(QColor(theme.ACCENT), max(1.5, scale * 0.035), Qt.DashLine))
            for a, b in self._lines:
                p.drawLine(T(a), T(b))

    def _paint_cube(self, p, r):
        n = self._n
        gap = 6.0
        s = min((r.width() - 3 * gap) / (4.0 * n), (r.height() - 2 * gap) / (3.0 * n))
        s = max(2.0, s)
        face = s * n
        total_w = 4 * face + 3 * gap
        total_h = 3 * face + 2 * gap
        ox = r.x() + (r.width() - total_w) / 2.0
        oy = r.y() + (r.height() - total_h) / 2.0
        layout = {"U": (1, 0), "L": (0, 1), "F": (1, 1), "R": (2, 1), "B": (3, 1), "D": (1, 2)}
        inset = max(0.6, s * 0.07)
        radius = s * 0.18
        colors = dict((k, QColor(v)) for k, v in FACE_COLORS.items())
        for fname, (cx, cy) in layout.items():
            fx = ox + cx * (face + gap)
            fy = oy + cy * (face + gap)
            p.setPen(Qt.NoPen)
            p.setBrush(QColor("#000000"))
            p.drawRoundedRect(QRectF(fx - 2, fy - 2, face + 4, face + 4), radius + 2, radius + 2)
            g = self._grid[fname]
            for row in range(n):
                for col in range(n):
                    p.setBrush(colors[g[row][col]])
                    p.drawRoundedRect(QRectF(fx + col * s + inset, fy + row * s + inset,
                                             s - 2 * inset, s - 2 * inset), radius, radius)


class TimeChart(QWidget):
    """Line chart of singles with ao5 / ao12 overlays and hover tooltips."""

    MAX_POINTS = 400

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMouseTracking(True)
        self.setMinimumHeight(140)
        self._singles = []
        self._ao5 = []
        self._ao12 = []
        self._offset = 0
        self._decimals = 2
        self._geom = None

    def set_data(self, singles, ao5, ao12, decimals=2):
        n = len(singles)
        start = max(0, n - self.MAX_POINTS)
        self._offset = start
        self._singles = singles[start:]
        self._ao5 = ao5[start:]
        self._ao12 = ao12[start:]
        self._decimals = decimals
        self.update()

    def _finite(self):
        vals = [v for v in self._singles if v is not None and v != INF]
        vals += [v for v in self._ao5 if v is not None and v != INF]
        return vals

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        vals = self._finite()
        r = self.rect()
        if len(self._singles) < 2 or len(vals) < 2:
            p.setPen(QColor(theme.MUTED))
            p.drawText(r, Qt.AlignCenter, tr("not_enough_data"))
            self._geom = None
            p.end()
            return
        left, right, top, bottom = 52, 12, 26, 20
        plot = QRectF(left, top, max(10, r.width() - left - right),
                      max(10, r.height() - top - bottom))
        lo, hi = min(vals), max(vals)
        if hi - lo < 100:
            hi += 50
            lo -= 50
        pad = (hi - lo) * 0.08
        lo, hi = max(0, lo - pad), hi + pad
        n = len(self._singles)

        def X(i):
            return plot.left() + (plot.width() * i / float(max(1, n - 1)))

        def Y(v):
            return plot.bottom() - (v - lo) / (hi - lo) * plot.height()

        self._geom = (plot, n, X)
        # grid
        f = QFont(theme.ui_font())
        f.setPixelSize(11)
        p.setFont(f)
        for k in range(5):
            v = lo + (hi - lo) * k / 4.0
            y = Y(v)
            p.setPen(QPen(QColor("#211f1f"), 1))
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            p.setPen(QColor(theme.MUTED))
            p.drawText(QRectF(0, y - 8, left - 6, 16), Qt.AlignRight | Qt.AlignVCenter,
                       fmt_ms(v, 1))

        def draw_series(seq, color, width, dots=False):
            path = QPainterPath()
            started = False
            for i, v in enumerate(seq):
                if v is None or v == INF:
                    started = False
                    continue
                pt = QPointF(X(i), Y(v))
                if started:
                    path.lineTo(pt)
                else:
                    path.moveTo(pt)
                    started = True
            p.setPen(QPen(QColor(color), width))
            p.setBrush(Qt.NoBrush)
            p.drawPath(path)
            if dots and n <= 120:
                p.setPen(Qt.NoPen)
                p.setBrush(QColor(color))
                for i, v in enumerate(seq):
                    if v is not None and v != INF:
                        p.drawEllipse(QPointF(X(i), Y(v)), 2.2, 2.2)

        draw_series(self._singles, "#5a5653", 1.2, dots=True)
        draw_series(self._ao12, theme.BLUE, 2.0)
        draw_series(self._ao5, theme.ACCENT, 2.2)
        # DNF marks
        p.setPen(QPen(QColor(theme.DNF_RED), 1.6))
        for i, v in enumerate(self._singles):
            if v == INF:
                x, y = X(i), plot.top() + 4
                p.drawLine(QPointF(x - 3, y - 3), QPointF(x + 3, y + 3))
                p.drawLine(QPointF(x - 3, y + 3), QPointF(x + 3, y - 3))
        # legend
        lx = plot.right()
        for label, color in (("ao12", theme.BLUE), ("ao5", theme.ACCENT),
                             (tr("chart_single"), "#7d7976")):
            fm = p.fontMetrics()
            w = fm.horizontalAdvance(label) if hasattr(fm, "horizontalAdvance") else fm.width(label)
            lx -= w + 22
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(color))
            p.drawRoundedRect(QRectF(lx, 8, 10, 4), 2, 2)
            p.setPen(QColor(theme.MUTED))
            p.drawText(QPointF(lx + 14, 14), label)
        p.end()

    def mouseMoveEvent(self, e):
        if not self._geom:
            return
        plot, n, X = self._geom
        if not plot.contains(QPointF(e.pos())):
            QToolTip.hideText()
            return
        rel = (e.pos().x() - plot.left()) / max(1.0, plot.width())
        i = int(round(rel * (n - 1)))
        i = max(0, min(n - 1, i))
        d = self._decimals
        lines = ["#%d   %s" % (i + 1 + self._offset, fmt_ms(self._singles[i], d))]
        if self._ao5[i] is not None:
            lines.append("ao5   %s" % fmt_avg(self._ao5[i], d))
        if self._ao12[i] is not None:
            lines.append("ao12  %s" % fmt_avg(self._ao12[i], d))
        QToolTip.showText(e.globalPos(), "\n".join(lines), self)

    def leaveEvent(self, e):
        QToolTip.hideText()


class TimeHistogram(QWidget):
    """Distribution of single times as horizontal bars (like csTimer).

    Each row is a time bucket ("12+" = 12.00-12.99 for a 1 s step); the bar
    length is the number of solves in it. DNFs are excluded.
    """

    MIN_SOLVES = 5
    ROW_MAX = 26
    ROW_MIN = 16

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumHeight(140)
        self._values = []

    def set_data(self, singles):
        self._values = [v for v in singles if v is not None and v != INF]
        self.update()

    @staticmethod
    def _nice_step(span_ms, max_rows):
        for step in (100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 15000,
                     30000, 60000, 120000, 300000, 600000):
            if span_ms / float(step) < max_rows:
                return step
        return 600000

    @staticmethod
    def _label(ms, step):
        if step >= 1000:
            secs = ms // 1000
            m, sec = divmod(secs, 60)
            return ("%d:%02d+" % (m, sec)) if m else ("%d+" % sec)
        return fmt_ms(ms, 1) + "+"

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(6, 8, -8, -6)
        vals = self._values
        if len(vals) < self.MIN_SOLVES:
            p.setPen(QColor(theme.MUTED))
            p.drawText(r, Qt.AlignCenter | Qt.TextWordWrap,
                       tr("dist_need") % (self.MIN_SOLVES - len(vals)))
            p.end()
            return
        max_rows = max(3, min(20, int(r.height() // self.ROW_MIN)))
        lo, hi = min(vals), max(vals)
        step = self._nice_step(max(1, hi - lo + 1), max_rows)
        start = int(lo // step) * step
        nb = int((hi - start) // step) + 1
        counts = [0] * nb
        for v in vals:
            counts[min(nb - 1, int((v - start) // step))] += 1
        cmax = max(counts)
        row_h = max(self.ROW_MIN, min(self.ROW_MAX, r.height() / float(nb)))
        f = QFont(theme.ui_font())
        f.setPixelSize(int(min(13, row_h * 0.6)))
        p.setFont(f)
        fm = p.fontMetrics()
        adv = fm.horizontalAdvance if hasattr(fm, "horizontalAdvance") else fm.width
        label_w = max(adv(self._label(start + i * step, step)) for i in range(nb)) + 10
        count_w = adv(str(cmax)) + 10
        bar_x = r.left() + label_w
        bar_max = max(10.0, r.right() - bar_x - count_w)
        best_bucket = counts.index(cmax)
        for i, c in enumerate(counts):
            y = r.top() + i * row_h
            p.setPen(QColor(theme.MUTED))
            p.drawText(QRectF(r.left(), y, label_w - 8, row_h),
                       Qt.AlignRight | Qt.AlignVCenter, self._label(start + i * step, step))
            if c:
                w = bar_max * c / float(cmax)
                p.setPen(Qt.NoPen)
                col = QColor(theme.ACCENT)
                if i != best_bucket:
                    col.setAlpha(170)
                p.setBrush(col)
                p.drawRoundedRect(QRectF(bar_x, y + row_h * 0.18, w, row_h * 0.64), 3, 3)
                p.setPen(QColor(theme.TEXT))
                p.drawText(QRectF(bar_x + w + 6, y, count_w, row_h),
                           Qt.AlignLeft | Qt.AlignVCenter, str(c))
        p.end()


class Toast(QLabel):
    """Small pop-up message shown over the timer."""

    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setObjectName("toast")
        self.setAlignment(Qt.AlignCenter)
        self.hide()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_message(self, text, ms=3000):
        self.setText(text)
        self.adjustSize()
        par = self.parentWidget()
        if par is not None:
            self.move(int((par.width() - self.width()) / 2), 14)
        self.raise_()
        self.show()
        self._timer.start(ms)
