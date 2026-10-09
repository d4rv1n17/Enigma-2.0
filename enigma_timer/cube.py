"""Tiny NxN cube simulator used to draw scramble previews and algorithm cases.

Every sticker is stored with an integer 3D position and an outward normal.
Cubie centres use odd coordinates in [-(n-1), n-1]; a sticker sits one unit
outside its cubie along the normal, so face stickers have |coord| == n.
Axes: x -> R, y -> U, z -> F.

Supported notation: face turns (R, U2, F'), wide turns (Rw, 3Rw, r),
slices (M, E, S), whole-cube rotations (x, y, z) and brackets.
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

_MOVE_RE = re.compile(r"^(\d*)([URFDLBurfdlbMESxyz])(w?)(2?'?|'?2?)$")

# slice -> (face whose direction it follows)
_SLICE = {"M": "L", "E": "D", "S": "F"}
_ROTATION = {"x": "R", "y": "U", "z": "F"}


def _rot_cw(v, a):
    """Rotate vector v by 90 degrees clockwise when looking at the face whose
    outward normal is a (i.e. -90 degrees about a): v' = -(a x v) + a(a.v)."""
    cx = a[1] * v[2] - a[2] * v[1]
    cy = a[2] * v[0] - a[0] * v[2]
    cz = a[0] * v[1] - a[1] * v[0]
    d = a[0] * v[0] + a[1] * v[1] + a[2] * v[2]
    return (-cx + a[0] * d, -cy + a[1] * d, -cz + a[2] * d)


def tokens(alg):
    """Split an algorithm into move tokens, dropping brackets and commas."""
    alg = alg.replace("’", "'").replace("`", "'")
    alg = re.sub(r"[()\[\],]", " ", alg)
    return alg.split()


def invert(alg):
    """Inverse of an algorithm (works for any supported notation)."""
    out = []
    for tok in reversed(tokens(alg)):
        if tok.endswith("2'") or tok.endswith("'2"):
            out.append(tok.rstrip("2'") + "2")
        elif tok.endswith("2"):
            out.append(tok)
        elif tok.endswith("'"):
            out.append(tok[:-1])
        else:
            out.append(tok + "'")
    return " ".join(out)


class Cube(object):
    def __init__(self, n):
        self.n = n
        self.stickers = []  # [pos, normal, color_face, sticker_id]
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
                    self.stickers.append([tuple(pos), nv, face, len(self.stickers)])

    def copy(self):
        c = Cube.__new__(Cube)
        c.n = self.n
        c.stickers = [list(s) for s in self.stickers]
        return c

    # ------------------------------------------------------------------
    def turn(self, face, width=1, times=1, skip=0):
        """Turn `width` layers of `face` clockwise; the outer `skip` layers stay."""
        a = _NORMALS[face]
        n = self.n
        lo = n - 2 * width - 1       # layers 1..width have signed coord > lo
        hi = n - 2 * skip + 1        # the outer `skip` layers have signed coord >= hi
        times %= 4
        if times == 0:
            return
        for st in self.stickers:
            pos = st[0]
            signed = a[0] * pos[0] + a[1] * pos[1] + a[2] * pos[2]
            if signed > lo and (skip == 0 or signed < hi):
                p, nv = pos, st[1]
                for _ in range(times):
                    p = _rot_cw(p, a)
                    nv = _rot_cw(nv, a)
                st[0] = p
                st[1] = nv

    def apply(self, alg):
        n = self.n
        for tok in tokens(alg):
            m = _MOVE_RE.match(tok)
            if not m:
                continue  # ignore unknown tokens
            prefix, face, wide, suf = m.groups()
            times = 1
            if "2" in suf:
                times = 2
            elif "'" in suf:
                times = 3
            if "2" in suf and "'" in suf:
                times = 2
            if face in _ROTATION:
                self.turn(_ROTATION[face], n, times)
            elif face in _SLICE:
                # middle layer(s) only: everything except the two outer layers
                self.turn(_SLICE[face], n - 1, times, skip=1)
            else:
                if face.islower():
                    face = face.upper()
                    width = int(prefix) if prefix else 2
                elif prefix:
                    width = int(prefix)
                elif wide:
                    width = 2
                else:
                    width = 1
                width = max(1, min(width, n))
                self.turn(face, width, times)
        return self

    # ------------------------------------------------------------------
    def centre(self, face):
        """Colour of the centre sticker of `face` (odd cubes)."""
        nv = _NORMALS[face]
        target = tuple(c * self.n for c in nv)
        for pos, normal, color, _ in self.stickers:
            if pos == target:
                return color
        return None

    def normalize(self):
        """Rotate the whole cube so the centres sit in the standard orientation
        (only meaningful for odd cubes). Returns self."""
        if self.n % 2 == 0 or (self.centre("U") == "U" and self.centre("F") == "F"):
            return self
        for first in ("", "x", "x2", "x'", "z", "z'"):
            for second in ("", "y", "y2", "y'"):
                c = self.copy().apply(first + " " + second)
                if c.centre("U") == "U" and c.centre("F") == "F":
                    self.stickers = c.stickers
                    return self
        return self

    def facelets(self):
        """Return {face: n x n list of colour-face letters} in net order.

        Orientation matches the usual unfolded net:
                U
              L F R B
                D
        """
        n = self.n
        grid = {f: [[None] * n for _ in range(n)] for f in _NORMALS}
        for pos, nv, color, _ in self.stickers:
            face, r, c = self.locate(pos, nv)
            grid[face][r][c] = color
        return grid

    def ids(self):
        """Like facelets() but with sticker ids instead of colours."""
        n = self.n
        grid = {f: [[None] * n for _ in range(n)] for f in _NORMALS}
        for pos, nv, color, sid in self.stickers:
            face, r, c = self.locate(pos, nv)
            grid[face][r][c] = sid
        return grid

    def locate(self, pos, nv):
        n = self.n

        def inc(c):
            return (c + (n - 1)) // 2

        def dec(c):
            return ((n - 1) - c) // 2

        x, y, z = pos
        if nv == (0, 1, 0):
            return "U", inc(z), inc(x)
        if nv == (0, -1, 0):
            return "D", dec(z), inc(x)
        if nv == (0, 0, 1):
            return "F", dec(y), inc(x)
        if nv == (0, 0, -1):
            return "B", dec(y), dec(x)
        if nv == (1, 0, 0):
            return "R", dec(y), dec(z)
        return "L", dec(y), inc(z)

    def is_solved(self):
        g = self.facelets()
        return all(len(set(c for row in g[f] for c in row)) == 1 for f in g)
