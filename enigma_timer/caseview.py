"""Geometry of algorithm-case pictures (independent of Qt).

`shapes(state, view, alg)` returns a list of drawing primitives in a unit
square [0, 1] x [0, 1]:
    ("poly", [(x, y), ...], "#rrggbb")
    ("arrow", (x1, y1), (x2, y2))

Views:
    "oll"  - top view; last-layer stickers yellow when facing up, grey otherwise
    "eo"   - like "oll" but only edges (2-look OLL edge step)
    "pll"  - top view with side colours and arrows showing where pieces go
    "f2l"  - 3D view of U, F, R; last-layer pieces grey
    "full" - 3D view with all colours
In pictures the last layer is yellow and the cross white (standard CFOP
colours), so the simulator's U/D colours are swapped for display.
"""

from .fast3 import LOCS, LOC_INDEX, COLOR

DISPLAY = {
    "U": "#ffd500",   # yellow on top
    "D": "#ffffff",   # white cross on the bottom
    "F": "#00b050",
    "B": "#1e5cff",
    "R": "#e8231e",
    "L": "#ff8a00",
}
GREY = "#3b3a3a"
PLASTIC = "#0b0b0b"


def _loc(face, r, c):
    return LOC_INDEX[(face, r, c)]


def _home_is_top(sticker_id):
    face, r, c = LOCS[sticker_id]
    return face == "U" or (face in "FRBL" and r == 0)


# ---------------------------------------------------------------------------
# Top (last layer) view
# ---------------------------------------------------------------------------

def _ll(state, view, alg=None):
    out = []
    m = 0.13            # margin for side strips
    cell = (1 - 2 * m) / 3.0
    gap = cell * 0.07
    strip = m * 0.62

    out.append(("poly", [(m - gap, m - gap), (1 - m + gap, m - gap),
                         (1 - m + gap, 1 - m + gap), (m - gap, 1 - m + gap)], PLASTIC))

    def colour_of(face, r, c):
        col = state.color(_loc(face, r, c))
        corner = (face == "U" and r != 1 and c != 1) or (face != "U" and c != 1)
        if view == "cmll" and not corner and not (face == "U" and r == 1 and c == 1):
            return GREY  # Roux CMLL: only the corners matter
        if view in ("oll", "eo"):
            if view == "eo" and corner and not (face == "U" and r == 1 and c == 1):
                return GREY
            return DISPLAY["U"] if col == "U" else GREY
        return DISPLAY[col]

    # top face
    for r in range(3):
        for c in range(3):
            x0 = m + c * cell + gap
            y0 = m + r * cell + gap
            x1, y1 = x0 + cell - 2 * gap, y0 + cell - 2 * gap
            col = colour_of("U", r, c)
            if r == 1 and c == 1:
                col = DISPLAY["U"]
            out.append(("poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col))

    # side strips: position i runs left->right (or top->bottom)
    def strip_rect(side, i):
        a = m + i * cell + gap
        b = a + cell - 2 * gap
        if side == "F":
            return [(a, 1 - m + gap * 2), (b, 1 - m + gap * 2), (b, 1 - m + strip), (a, 1 - m + strip)]
        if side == "B":
            return [(a, m - strip), (b, m - strip), (b, m - gap * 2), (a, m - gap * 2)]
        if side == "L":
            return [(m - strip, a), (m - gap * 2, a), (m - gap * 2, b), (m - strip, b)]
        return [(1 - m + gap * 2, a), (1 - m + strip, a), (1 - m + strip, b), (1 - m + gap * 2, b)]

    for i in range(3):
        out.append(("poly", strip_rect("F", i), colour_of("F", 0, i)))
        out.append(("poly", strip_rect("B", i), colour_of("B", 0, 2 - i)))
        out.append(("poly", strip_rect("L", i), colour_of("L", 0, i)))
        out.append(("poly", strip_rect("R", i), colour_of("R", 0, 2 - i)))

    if view == "pll" and alg:
        out.extend(_pll_arrows(state, alg, m, cell))
    return out


def _piece_moves(state, alg):
    """{(r, c): (r2, c2)} for top pieces the algorithm moves, ignoring a final AUF."""
    best = None
    for post in ("", "U", "U2", "U'"):
        after = state.copy().apply(alg + " " + post).normalize()
        where = {}
        for r in range(3):
            for c in range(3):
                where[after.arr[_loc("U", r, c)]] = (r, c)
        moves = {}
        for r in range(3):
            for c in range(3):
                if r == 1 and c == 1:
                    continue
                dest = where.get(state.arr[_loc("U", r, c)])
                if dest and dest != (r, c):
                    moves[(r, c)] = dest
        if best is None or len(moves) < len(best):
            best = moves
    return best


def best_pre_auf(state, alg):
    """Pre-AUF that shows a PLL case with the fewest moving pieces."""
    best, best_n = "", 99
    for pre in ("", "U", "U2", "U'"):
        st = state.copy().apply(pre)
        n = len(_piece_moves(st, _inverse_auf(pre) + " " + alg))
        if n < best_n:
            best, best_n = pre, n
    return best


def _pll_arrows(state, alg, m, cell):
    """Arrows from where each top piece is now to where the algorithm puts it."""
    moves = _piece_moves(state, alg)

    def pt(rc):
        return (m + (rc[1] + 0.5) * cell, m + (rc[0] + 0.5) * cell)

    arrows = []
    done = set()
    for src, dst in moves.items():
        if (src, dst) in done:
            continue
        if moves.get(dst) == src:          # a swap: one double-headed arrow
            arrows.append(("arrow2", pt(src), pt(dst)))
            done.add((dst, src))
        else:
            arrows.append(("arrow", pt(src), pt(dst)))
        done.add((src, dst))
    return arrows


# ---------------------------------------------------------------------------
# 3D view of U, F, R
# ---------------------------------------------------------------------------

_C30 = 0.8660254
_S30 = 0.5


def _iso(state, view):
    # cube spans [-1.5, 1.5]^3; isometric projection, then fitted to the unit square
    def P(x, y, z):
        return ((x - z) * _C30, (x + z) * _S30 - y)

    quads = []

    def add(face, r, c, corners):
        col = state.color(_loc(face, r, c))
        sid = state.arr[_loc(face, r, c)]
        if view == "f2l" and _home_is_top(sid):
            colour = GREY
        else:
            colour = DISPLAY[col]
        # shrink sticker a little towards its centre
        cx = sum(p[0] for p in corners) / 4.0
        cy = sum(p[1] for p in corners) / 4.0
        pts = [(cx + (p[0] - cx) * 0.86, cy + (p[1] - cy) * 0.86) for p in corners]
        quads.append((pts, colour))

    h = 1.5
    for r in range(3):
        for c in range(3):
            # U: row r -> z from back to front, col c -> x left to right
            x0, z0 = -h + c, -h + r
            add("U", r, c, [P(x0, h, z0), P(x0 + 1, h, z0), P(x0 + 1, h, z0 + 1), P(x0, h, z0 + 1)])
            # F: row r -> y from top, col c -> x left to right
            y0, x0 = h - r, -h + c
            add("F", r, c, [P(x0, y0, h), P(x0 + 1, y0, h), P(x0 + 1, y0 - 1, h), P(x0, y0 - 1, h)])
            # R: row r -> y from top, col c -> z from front to back
            y0, z0 = h - r, h - c
            add("R", r, c, [P(h, y0, z0), P(h, y0, z0 - 1), P(h, y0 - 1, z0 - 1), P(h, y0 - 1, z0)])

    outline = [P(-h, h, -h), P(h, h, -h), P(h, h, h), P(h, -h, h), P(-h, -h, h), P(-h, h, h)]
    xs = [p[0] for p in outline]
    ys = [p[1] for p in outline]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    span = max(x1 - x0, y1 - y0) * 1.04
    ox = (span - (x1 - x0)) / 2.0
    oy = (span - (y1 - y0)) / 2.0

    def fit(p):
        return ((p[0] - x0 + ox) / span, (p[1] - y0 + oy) / span)

    out = [("poly", [fit(p) for p in outline], PLASTIC)]
    for pts, colour in quads:
        out.append(("poly", [fit(p) for p in pts], colour))
    return out


def iso_grid(g, n, grey_top=False):
    """3D view (U, F, R) of any n x n cube from its facelets."""
    def P(x, y, z):
        return ((x - z) * _C30, (x + z) * _S30 - y)

    h = n / 2.0
    quads = []

    def add(face, r, c, corners):
        colour = DISPLAY[g[face][r][c]]
        cx = sum(p[0] for p in corners) / 4.0
        cy = sum(p[1] for p in corners) / 4.0
        pts = [(cx + (p[0] - cx) * 0.86, cy + (p[1] - cy) * 0.86) for p in corners]
        quads.append(("poly", pts, colour))

    for r in range(n):
        for c in range(n):
            x0, z0 = -h + c, -h + r
            add("U", r, c, [P(x0, h, z0), P(x0 + 1, h, z0), P(x0 + 1, h, z0 + 1), P(x0, h, z0 + 1)])
            y0, x0 = h - r, -h + c
            add("F", r, c, [P(x0, y0, h), P(x0 + 1, y0, h), P(x0 + 1, y0 - 1, h), P(x0, y0 - 1, h)])
            y0, z0 = h - r, h - c
            add("R", r, c, [P(h, y0, z0), P(h, y0, z0 - 1), P(h, y0 - 1, z0 - 1), P(h, y0 - 1, z0)])
    outline = [P(-h, h, -h), P(h, h, -h), P(h, h, h), P(h, -h, h), P(-h, -h, h), P(-h, h, h)]
    return _fit([("poly", outline, PLASTIC)] + quads, 0.02)


def shapes(state, view, alg=None):
    if view in ("oll", "eo", "pll", "cmll"):
        return _ll(state, view, alg)
    return _iso(state, view)


_PRE = {}


def _fit(shapes, margin=0.03):
    """Scale primitives so they fill the unit square (keeping proportions)."""
    pts = [q for sh in shapes for q in (sh[1] if sh[0] == "poly" else (sh[1], sh[2]))]
    if not pts:
        return shapes
    x0 = min(p[0] for p in pts)
    x1 = max(p[0] for p in pts)
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    span = max(x1 - x0, y1 - y0) or 1.0
    k = (1 - 2 * margin) / span
    ox = margin + ((1 - 2 * margin) - (x1 - x0) * k) / 2.0
    oy = margin + ((1 - 2 * margin) - (y1 - y0) * k) / 2.0

    def T(p):
        return (ox + (p[0] - x0) * k, oy + (p[1] - y0) * k)

    out = []
    for sh in shapes:
        if sh[0] == "poly":
            out.append(("poly", [T(p) for p in sh[1]], sh[2]))
        else:
            out.append((sh[0], T(sh[1]), T(sh[2])))
    return out


def ll_grid(g, n, mask):
    """Top view of the U face of an n x n cube with side strips.

    g: facelets dict {face: rows of colour letters}; mask: True for the
    "yellow or grey" orientation view, False for full colours."""
    out = []
    m = 0.13
    cell = (1 - 2 * m) / float(n)
    gap = cell * 0.07
    strip = m * 0.62
    out.append(("poly", [(m - gap, m - gap), (1 - m + gap, m - gap),
                         (1 - m + gap, 1 - m + gap), (m - gap, 1 - m + gap)], PLASTIC))

    def col(c):
        if mask:
            return DISPLAY["U"] if c == "U" else GREY
        return DISPLAY[c]

    for r in range(n):
        for c in range(n):
            x0 = m + c * cell + gap
            y0 = m + r * cell + gap
            x1, y1 = x0 + cell - 2 * gap, y0 + cell - 2 * gap
            out.append(("poly", [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col(g["U"][r][c])))
    for i in range(n):
        a = m + i * cell + gap
        b = a + cell - 2 * gap
        out.append(("poly", [(a, 1 - m + gap * 2), (b, 1 - m + gap * 2), (b, 1 - m + strip),
                             (a, 1 - m + strip)], col(g["F"][0][i])))
        out.append(("poly", [(a, m - strip), (b, m - strip), (b, m - gap * 2), (a, m - gap * 2)],
                    col(g["B"][0][n - 1 - i])))
        out.append(("poly", [(m - strip, a), (m - gap * 2, a), (m - gap * 2, b), (m - strip, b)],
                    col(g["L"][0][i])))
        out.append(("poly", [(1 - m + gap * 2, a), (1 - m + strip, a), (1 - m + strip, b),
                             (1 - m + gap * 2, b)], col(g["R"][0][n - 1 - i])))
    return out


def _pentagon():
    import math
    pts = [(0.5 + 0.42 * math.cos(math.radians(-90 + 72 * i)),
            0.53 + 0.42 * math.sin(math.radians(-90 + 72 * i))) for i in range(5)]
    inner = [(0.5 + 0.2 * math.cos(math.radians(90 + 72 * i)),
              0.53 + 0.2 * math.sin(math.radians(90 + 72 * i))) for i in range(5)]
    return [("poly", pts, "#2a2828"), ("poly", inner, DISPLAY["U"])]


def other_shapes(case):
    """Pictures for events other than the 3x3."""
    st = case.state()
    view = case.view
    if view in ("ll2", "cll2", "ll4"):
        n = st.n
        return ll_grid(st.facelets(), n, mask=(view == "ll2"))
    if view == "pbl":
        top = ll_grid(st.facelets(), 2, mask=False)
        bottom = ll_grid(st.copy().apply("x2").facelets(), 2, mask=False)
        out = []
        for shapes, ox in ((top, 0.0), (bottom, 0.52)):
            for sh in shapes:
                out.append(("poly", [(ox + x * 0.48, 0.26 + y * 0.48) for x, y in sh[1]], sh[2]))
        return out
    if view in ("pyra", "skewb"):
        return _fit([("poly", pts, colour) for pts, colour in st.polygons()])
    if view == "sq1":
        from .puzzles import sq1_polygons, sq1_slice_lines
        shapes = [("poly", pts, colour) for pts, colour in sq1_polygons(st)]
        shapes += [("line", a, b) for a, b in sq1_slice_lines()]
        return _fit(shapes)
    return _pentagon()


def case_shapes(case, auf=None, arrows=True):
    """Primitives for an algs.Case.

    auf: pre-AUF to apply to the case (None = the clearest one for PLL).
    arrows: draw PLL arrows (hidden in the trainer, they give the answer away).
    """
    if case.puzzle not in ("333", "333oh", "333bf") or case.view == "none":
        return other_shapes(case)
    view = case.view
    if case.id.startswith("oll2-"):
        view = "eo"
    state = case.state()
    if auf is None:
        auf = ""
        if view == "pll":
            if case.id not in _PRE:
                _PRE[case.id] = best_pre_auf(state, case.alg)
            auf = _PRE[case.id]
    if auf:
        # turning the last layer before solving = applying the AUF to the case
        state = state.copy().apply(auf)
    alg = (_inverse_auf(auf) + " " + case.alg) if (arrows and view == "pll") else None
    return shapes(state, view, alg)


def _inverse_auf(auf):
    return {"": "", "U": "U'", "U'": "U", "U2": "U2"}[auf]


__all__ = ["shapes", "case_shapes", "DISPLAY", "GREY", "COLOR"]
