"""Fast NxN simulator (any size) built on sticker permutations, plus helpers
shared by the 2x2 / 4x4 / 5x5 algorithm sets."""

from .cube import Cube, tokens

FACES = "URFDLB"


class _Tables(object):
    def __init__(self, n):
        self.n = n
        self.locs = [(f, r, c) for f in FACES for r in range(n) for c in range(n)]
        self.index = dict((loc, i) for i, loc in enumerate(self.locs))
        base = Cube(n)
        self.home = {}
        self.color = {}
        for pos, nv, col, sid in base.stickers:
            loc = self.index[base.locate(pos, nv)]
            self.home[sid] = loc
            self.color[loc] = col
        self.perms = {}

    def perm(self, tok):
        p = self.perms.get(tok)
        if p is None:
            c = Cube(self.n).apply(tok)
            p = [0] * len(self.locs)
            for pos, nv, col, sid in c.stickers:
                p[self.home[sid]] = self.index[c.locate(pos, nv)]
            self.perms[tok] = p
        return p


_TABLES = {}


def tables(n):
    t = _TABLES.get(n)
    if t is None:
        t = _TABLES[n] = _Tables(n)
    return t


ROTATIONS = [(a + " " + b).strip() for a in ("", "x", "x2", "x'", "z", "z'")
             for b in ("", "y", "y2", "y'")]


class NState(object):
    __slots__ = ("n", "arr")

    def __init__(self, n, arr=None):
        self.n = n
        self.arr = list(arr) if arr is not None else list(range(6 * n * n))

    def copy(self):
        return NState(self.n, self.arr)

    def apply(self, alg):
        t = tables(self.n)
        arr = self.arr
        size = len(arr)
        for tok in tokens(alg):
            p = t.perm(tok)
            new = [0] * size
            for src in range(size):
                new[p[src]] = arr[src]
            arr = new
        self.arr = arr
        return self

    def facelets(self):
        t = tables(self.n)
        n = self.n
        g = dict((f, [[None] * n for _ in range(n)]) for f in FACES)
        for i, (f, r, c) in enumerate(t.locs):
            g[f][r][c] = t.color[self.arr[i]]
        return g

    def key(self):
        t = tables(self.n)
        return tuple(t.color[x] for x in self.arr)

    def is_solved(self):
        g = self.facelets()
        return all(len(set(c for row in g[f] for c in row)) == 1 for f in g)


def bottom_key(state):
    """D face and the bottom row of the side faces (the solved first layer)."""
    g = state.facelets()
    n = state.n
    return (tuple(map(tuple, g["D"])),) + tuple(tuple(g[f][n - 1]) for f in "FRBL")


def net_rotation(n, alg):
    """Whole-cube rotation `alg` leaves behind, judged by the bottom layer
    (works for cubes without fixed centres, as long as `alg` keeps the first
    layer intact)."""
    k = bottom_key(NState(n).apply(alg))
    for rot in ROTATIONS:
        if bottom_key(NState(n).apply(rot)) == k:
            return rot
    return ""


def centre_rotation(n, alg):
    """Rotation judged by the centre colours (odd cubes and 4x4 centres)."""
    after = NState(n).apply(alg).facelets()
    m = n // 2
    for rot in ROTATIONS:
        g = NState(n).apply(rot).facelets()
        if all(g[f][m][m] == after[f][m][m] for f in "UF"):
            return rot
    return ""
