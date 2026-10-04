"""Tiny NxN cube simulator used to draw the scramble preview offline.

Every sticker is stored with an integer 3D position and an outward normal.
Cubie centres use odd coordinates in [-(n-1), n-1]; a sticker sits one unit
outside its cubie along the normal, so face stickers have |coord| == n.
Axes: x -> R, y -> U, z -> F.
"""

import re

# WCA colour scheme
FACE_COLORS = {
    "U": "#ffffff",
    "D": "#ffd500",
    "F": "#00b050",
    "B": "#1e5cff",
    "R": "#e8231e",
    "L": "#ff8a00",
}

_NORMALS = {
    "R": (1, 0, 0), "L": (-1, 0, 0),
    "U": (0, 1, 0), "D": (0, -1, 0),
    "F": (0, 0, 1), "B": (0, 0, -1),
}

_MOVE_RE = re.compile(r"^(\d*)([URFDLB])(w?)(['2]?)$")


def _rot_cw(v, a):
    """Rotate vector v by 90 degrees clockwise when looking at the face whose
    outward normal is a (i.e. -90 degrees about a): v' = -(a x v) + a(a.v)."""
    cx = a[1] * v[2] - a[2] * v[1]
    cy = a[2] * v[0] - a[0] * v[2]
    cz = a[0] * v[1] - a[1] * v[0]
    d = a[0] * v[0] + a[1] * v[1] + a[2] * v[2]
    return (-cx + a[0] * d, -cy + a[1] * d, -cz + a[2] * d)


class Cube(object):
    def __init__(self, n):
        self.n = n
        self.stickers = []  # [pos, normal, color_face]
        coords = range(-(n - 1), n, 2)
        for face, nv in _NORMALS.items():
            for u in coords:
                for w in coords:
                    pos = [0, 0, 0]
                    axis = [i for i in range(3) if nv[i] != 0][0]
                    others = [i for i in range(3) if i != axis]
                    pos[axis] = nv[axis] * n
                    pos[others[0]] = u
                    pos[others[1]] = w
                    self.stickers.append([tuple(pos), nv, face])

    # ------------------------------------------------------------------
    def turn(self, face, width=1, times=1):
        a = _NORMALS[face]
        n = self.n
        threshold = n - 2 * width  # stickers with signed coord > threshold move
        times %= 4
        if times == 0:
            return
        for st in self.stickers:
            pos = st[0]
            signed = a[0] * pos[0] + a[1] * pos[1] + a[2] * pos[2]
            if signed > threshold:
                p, nv = pos, st[1]
                for _ in range(times):
                    p = _rot_cw(p, a)
                    nv = _rot_cw(nv, a)
                st[0] = p
                st[1] = nv

    def apply(self, alg):
        for tok in alg.split():
            m = _MOVE_RE.match(tok)
            if not m:
                continue  # ignore unknown tokens (rotations etc.)
            prefix, face, wide, suf = m.groups()
            if prefix:
                width = int(prefix)
            elif wide:
                width = 2
            else:
                width = 1
            width = max(1, min(width, self.n))
            times = {"": 1, "'": 3, "2": 2}[suf]
            self.turn(face, width, times)
        return self

    # ------------------------------------------------------------------
    def facelets(self):
        """Return {face: n x n list of colour-face letters} in net order.

        Orientation matches the usual unfolded net:
                U
              L F R B
                D
        """
        n = self.n
        grid = {f: [[None] * n for _ in range(n)] for f in _NORMALS}

        def inc(c):
            return (c + (n - 1)) // 2

        def dec(c):
            return ((n - 1) - c) // 2

        for pos, nv, color in self.stickers:
            x, y, z = pos
            if nv == (0, 1, 0):
                face, r, c = "U", inc(z), inc(x)
            elif nv == (0, -1, 0):
                face, r, c = "D", dec(z), inc(x)
            elif nv == (0, 0, 1):
                face, r, c = "F", dec(y), inc(x)
            elif nv == (0, 0, -1):
                face, r, c = "B", dec(y), dec(x)
            elif nv == (1, 0, 0):
                face, r, c = "R", dec(y), dec(z)
            else:
                face, r, c = "L", dec(y), inc(z)
            grid[face][r][c] = color
        return grid

    def is_solved(self):
        g = self.facelets()
        return all(len(set(c for row in g[f] for c in row)) == 1 for f in g)
