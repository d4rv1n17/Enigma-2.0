"""Sticker-level simulators used to draw scramble previews for non-cube
puzzles (Pyraminx, Skewb, Square-1).

Pyraminx and Skewb are simulated geometrically: every sticker has a 3D
centroid; a move rotates every sticker on one side of a cutting plane by
-120 degrees about the axis (= clockwise when looking at that vertex), and the
rotated centroid tells which slot the colour lands in. The resulting slot
permutation is cached per move, so applying a scramble is cheap.

Each preview returns a list of (polygon_2d, colour_hex) for drawing.
"""

import math
import re

from .scramble import _SQ1_START, _sq1_slash, _sq1_twist


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a):
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


def _rotate(v, axis, angle):
    """Rodrigues rotation of v about unit axis by angle (radians)."""
    c, s = math.cos(angle), math.sin(angle)
    ax, ay, az = axis
    cx = ay * v[2] - az * v[1]
    cy = az * v[0] - ax * v[2]
    cz = ax * v[1] - ay * v[0]
    d = _dot(axis, v) * (1 - c)
    return (v[0] * c + cx * s + ax * d,
            v[1] * c + cy * s + ay * d,
            v[2] * c + cz * s + az * d)


def _centroid(pts):
    n = float(len(pts))
    return tuple(sum(p[i] for p in pts) / n for i in range(len(pts[0])))


class _GeoPuzzle(object):
    """Generic sticker puzzle. Subclasses fill slots and define moves."""

    MOVES = {}  # name -> (axis_vector, threshold)

    def __init__(self):
        self.slots = []      # (centroid3d, polygon2d, solved_colour)
        self._build()
        self.colors = [s[2] for s in self.slots]
        self._perm_cache = {}

    def _build(self):
        raise NotImplementedError

    def _perm(self, name):
        if name in self._perm_cache:
            return self._perm_cache[name]
        axis, threshold = self.MOVES[name]
        axis = _norm(axis)
        cents = [s[0] for s in self.slots]
        perm = list(range(len(cents)))  # perm[src] = dst
        for i, c in enumerate(cents):
            if _dot(c, axis) > threshold:
                r = _rotate(c, axis, -2 * math.pi / 3)
                best, best_d = i, 1e9
                for j, c2 in enumerate(cents):
                    d = sum((r[k] - c2[k]) ** 2 for k in range(3))
                    if d < best_d:
                        best, best_d = j, d
                perm[i] = best
        self._perm_cache[name] = perm
        return perm

    def turn(self, name, times=1):
        perm = self._perm(name)
        for _ in range(times % 3):
            new = list(self.colors)
            for src, dst in enumerate(perm):
                new[dst] = self.colors[src]
            self.colors = new

    def apply(self, alg):
        for tok in alg.split():
            m = re.match(r"^([A-Za-z])('?)$", tok)
            if not m or m.group(1) not in self.MOVES:
                continue
            self.turn(m.group(1), 2 if m.group(2) else 1)
        return self

    def polygons(self):
        return [(s[1], c) for s, c in zip(self.slots, self.colors)]

    def is_solved(self):
        return self.colors == [s[2] for s in self.slots]


# ---------------------------------------------------------------------------
# Pyraminx
# ---------------------------------------------------------------------------

_R8 = math.sqrt(8.0) / 3.0
_PV = {
    "U": (0.0, 1.0, 0.0),
    "L": (-_R8 * math.sin(math.pi / 3), -1.0 / 3, _R8 * 0.5),
    "R": (_R8 * math.sin(math.pi / 3), -1.0 / 3, _R8 * 0.5),
    "B": (0.0, -1.0 / 3, -_R8),
}
_H = math.sqrt(3) / 2.0


class Pyraminx(_GeoPuzzle):
    # Vertex axis; the face opposite a vertex lies at -1/3, the vertex at 1.
    # Two-layer turns cut at 1/9, tips at 5/9.
    MOVES = {}
    for _k, _v in _PV.items():
        MOVES[_k] = (_v, 1.0 / 9)
        MOVES[_k.lower()] = (_v, 5.0 / 9)
    del _k, _v

    def _build(self):
        net = {
            # face colour, 3D corners, 2D corners (screen coords, y down)
            "F": ("#00b050", ("U", "L", "R"), ((0, 0), (-0.5, _H), (0.5, _H))),
            "L": ("#e8231e", ("U", "L", "B"), ((0, 0), (-0.5, _H), (-1.0, 0))),
            "R": ("#1e5cff", ("U", "R", "B"), ((0, 0), (0.5, _H), (1.0, 0))),
            "D": ("#ffd500", ("L", "R", "B"), ((-0.5, _H), (0.5, _H), (0, 2 * _H))),
        }
        for _face, (col, names, p2) in net.items():
            a3, b3, c3 = [_PV[n] for n in names]
            a2, b2, c2 = p2

            def P3(i, j):
                return tuple(a3[k] + (b3[k] - a3[k]) * i / 3.0 + (c3[k] - a3[k]) * j / 3.0
                             for k in range(3))

            def P2(i, j):
                return tuple(a2[k] + (b2[k] - a2[k]) * i / 3.0 + (c2[k] - a2[k]) * j / 3.0
                             for k in range(2))

            tris = []
            for i in range(3):
                for j in range(3 - i):
                    tris.append(((i, j), (i + 1, j), (i, j + 1)))
                    if i + j <= 1:
                        tris.append(((i + 1, j), (i + 1, j + 1), (i, j + 1)))
            for t in tris:
                pts3 = [P3(*ij) for ij in t]
                pts2 = [P2(*ij) for ij in t]
                self.slots.append((_centroid(pts3), pts2, col))


# ---------------------------------------------------------------------------
# Skewb
# ---------------------------------------------------------------------------

_SKEWB_FACES = {
    "U": ("#ffffff", 1, 1), "D": ("#ffd500", 1, -1),
    "R": ("#e8231e", 0, 1), "L": ("#ff8a00", 0, -1),
    "F": ("#00b050", 2, 1), "B": ("#1e5cff", 2, -1),
}
# same unfolded-net orientation as the NxN preview
_NET_POS = {"U": (1, 0), "L": (0, 1), "F": (1, 1), "R": (2, 1), "B": (3, 1), "D": (1, 2)}


def _face_uv(face, p):
    """Map a 3D point on a cube face ([-1,1]^3) to (u, v) in [0,1] on the net."""
    x, y, z = p
    inc = lambda c: (c + 1) / 2.0  # noqa: E731
    dec = lambda c: (1 - c) / 2.0  # noqa: E731
    if face == "U":
        return inc(x), inc(z)
    if face == "D":
        return inc(x), dec(z)
    if face == "F":
        return inc(x), dec(y)
    if face == "B":
        return dec(x), dec(y)
    if face == "R":
        return dec(z), dec(y)
    return inc(z), dec(y)  # L


class Skewb(_GeoPuzzle):
    # WCA: R = DBR, U = UBL, L = DFL, B = DBL (clockwise looking at the corner)
    MOVES = {
        "R": ((1, -1, -1), 0.0),
        "U": ((-1, 1, -1), 0.0),
        "L": ((-1, -1, 1), 0.0),
        "B": ((-1, -1, -1), 0.0),
    }

    def _build(self):
        gap = 0.08
        for face, (col, axis, sign) in _SKEWB_FACES.items():
            others = [i for i in range(3) if i != axis]

            def pt(a, b):
                p = [0.0, 0.0, 0.0]
                p[axis] = float(sign)
                p[others[0]] = a
                p[others[1]] = b
                return tuple(p)

            corners = [pt(-1, -1), pt(1, -1), pt(1, 1), pt(-1, 1)]
            mids = [pt(0, -1), pt(1, 0), pt(0, 1), pt(-1, 0)]
            ox, oy = _NET_POS[face]

            def to2(p):
                u, v = _face_uv(face, p)
                return (ox * (1 + gap) + u, oy * (1 + gap) + v)

            # centre diamond
            self.slots.append((_centroid(mids), [to2(m) for m in mids], col))
            # four corner triangles
            for k in range(4):
                tri = [corners[k], mids[k], mids[k - 1]]
                self.slots.append((_centroid(tri), [to2(q) for q in tri], col))


# ---------------------------------------------------------------------------
# Square-1
# ---------------------------------------------------------------------------

_SQ1_TOP = "#ffffff"
_SQ1_BOTTOM = "#ffd500"
_SQ1_SIDE = [(270, "#00b050"), (0, "#e8231e"), (90, "#1e5cff"), (180, "#ff8a00")]
_UNIT0 = 255.0  # math angle (degrees, CCW seen from the top) where unit 0 starts


def _side_colour(angle):
    angle %= 360.0
    best = min(_SQ1_SIDE, key=lambda s: min(abs(angle - s[0]), 360 - abs(angle - s[0])))
    return best[1]


def sq1_state(scramble):
    """Return (units, piece_of): 24 unit ids after the scramble."""
    units = list(range(24))
    piece_of = list(_SQ1_START)
    for tok in scramble.split():
        m = re.match(r"^\(?(-?\d+),(-?\d+)\)?(/?)$", tok.replace(" ", ""))
        if m:
            units = _sq1_twist(units, int(m.group(1)), int(m.group(2)))
            if m.group(3):
                units = _sq1_slash(units)
        elif tok == "/":
            units = _sq1_slash(units)
    return units, piece_of


def sq1_polygons(scramble):
    """Polygons for the top layer (left) and bottom layer (right).

    Top is seen from above (front at the bottom); bottom is seen from below
    after flipping the puzzle forward (front at the top).
    """
    units, piece_of = sq1_state(scramble)
    h = 1.0
    r1 = h / math.cos(math.radians(15))
    r2 = h * math.sqrt(2)
    out = []
    for layer in (0, 1):
        cx = 0.0 if layer == 0 else 2.0 * r2 + 0.35
        lay = units[layer * 12:(layer + 1) * 12]

        def P(angle_deg, r):
            a = math.radians(angle_deg)
            y = math.sin(a) * r
            return (cx + math.cos(a) * r, (-y if layer == 0 else y))

        for i, u in enumerate(lay):
            a0 = _UNIT0 + 30 * i
            pid = piece_of[u]
            nxt = piece_of[lay[(i + 1) % 12]]
            prv = piece_of[lay[(i - 1) % 12]]
            is_corner = pid in (nxt, prv) and _is_corner_piece(pid)
            if not is_corner:
                outer = [P(a0, r1), P(a0 + 30, r1)]
            elif pid == nxt:
                outer = [P(a0, r1), P(a0 + 30, r2)]
            else:
                outer = [P(a0, r2), P(a0 + 30, r1)]
            centre = (cx, 0.0)
            # original solved position of this unit -> its colours
            home = u % 12
            home_layer = u // 12
            top_col = _SQ1_TOP if home_layer == 0 else _SQ1_BOTTOM
            side = _side_colour(_UNIT0 + 30 * home + 15)
            out.append(([centre] + outer, side))
            inner = [centre] + [(cx + (q[0] - cx) * 0.78, q[1] * 0.78) for q in outer]
            out.append((inner, top_col))
    return out


def _is_corner_piece(pid):
    return _SQ1_START.count(pid) == 2


def sq1_slice_lines():
    """Dashed line showing where the slice cuts each layer."""
    h = 1.0
    r2 = h * math.sqrt(2)
    lines = []
    for layer in (0, 1):
        cx = 0.0 if layer == 0 else 2.0 * r2 + 0.35
        pts = []
        for ang in (_UNIT0, _UNIT0 + 180):
            a = math.radians(ang)
            y = math.sin(a) * r2 * 1.02
            pts.append((cx + math.cos(a) * r2 * 1.02, -y if layer == 0 else y))
        lines.append((pts[0], pts[1]))
    return lines
