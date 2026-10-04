"""Offline scramble generators for WCA puzzles.

All generators are random-move scramblers that follow the usual notation
and the standard "no redundant moves" rules:

* the same face is never turned twice in a row;
* on a single axis (e.g. R and L) each layer is turned at most once
  before a move on another axis appears, so sequences such as
  ``R L R`` or ``Rw R Rw`` are never produced.
"""

import random

# ---------------------------------------------------------------------------
# Puzzle catalogue
# ---------------------------------------------------------------------------

PUZZLES = [
    # id,        short label, full name
    ("222", "2x2", "2x2x2 Cube"),
    ("333", "3x3", "3x3x3 Cube"),
    ("444", "4x4", "4x4x4 Cube"),
    ("555", "5x5", "5x5x5 Cube"),
    ("666", "6x6", "6x6x6 Cube"),
    ("777", "7x7", "7x7x7 Cube"),
    ("pyram", "Pyra", "Pyraminx"),
    ("skewb", "Skewb", "Skewb"),
    ("minx", "Mega", "Megaminx"),
    ("clock", "Clock", "Clock"),
    ("sq1", "SQ-1", "Square-1"),
    ("333oh", "OH", "3x3x3 One-Handed"),
    ("333bf", "3BLD", "3x3x3 Blindfolded"),
    ("333fm", "FMC", "3x3x3 Fewest Moves"),
]

PUZZLE_IDS = [p[0] for p in PUZZLES]
PUZZLE_LABEL = {p[0]: p[1] for p in PUZZLES}
PUZZLE_NAME = {p[0]: p[2] for p in PUZZLES}

# Cube size for NxN puzzles (used by the preview renderer)
CUBE_SIZE = {"222": 2, "333": 3, "444": 4, "555": 5, "666": 6, "777": 7,
             "333oh": 3, "333bf": 3, "333fm": 3}

_AXIS = {"U": 0, "D": 0, "R": 1, "L": 1, "F": 2, "B": 2}
_SUFFIX = ["", "'", "2"]


def _nxn(n, length, first_axis_not=None, last_axis_not=None):
    """Random-move scramble for an n x n x n cube using WCA notation.

    Allowed layers: outer face turns, plus wide turns up to n//2 layers
    (``Rw`` = 2 layers, ``3Rw`` = 3 layers). For 2x2 only R, U, F are used,
    like the official WCA scrambles.
    """
    if n == 2:
        faces = ["R", "U", "F"]
    else:
        faces = ["R", "L", "U", "D", "F", "B"]
    max_width = max(1, n // 2)
    moves = []
    cur_axis = None
    used_on_axis = set()  # (face, width) already used in the current axis run
    while len(moves) < length:
        face = random.choice(faces)
        width = random.randint(1, max_width)
        # For even cubes, an n/2-wide turn on the opposite face is the same
        # as a slice of the other face plus rotation; keep only R/U/F for the
        # widest even layer to avoid redundant pairs.
        if n % 2 == 0 and n > 2 and width == n // 2 and face in ("L", "D", "B"):
            continue
        axis = _AXIS[face]
        if not moves and first_axis_not is not None and axis == first_axis_not:
            continue
        if len(moves) == length - 1 and last_axis_not is not None and axis == last_axis_not:
            continue
        if axis == cur_axis:
            if (face, width) in used_on_axis:
                continue
        else:
            cur_axis = axis
            used_on_axis = set()
        used_on_axis.add((face, width))
        moves.append(_fmt_wide(face, width) + random.choice(_SUFFIX))
    return " ".join(moves)


def _fmt_wide(face, width):
    if width == 1:
        return face
    if width == 2:
        return face + "w"
    return "%d%sw" % (width, face)


def _pyraminx(length=11):
    faces = ["U", "L", "R", "B"]
    moves = []
    last = None
    while len(moves) < length:
        f = random.choice(faces)
        if f == last:
            continue
        last = f
        moves.append(f + random.choice(["", "'"]))
    tips = []
    for t in ["u", "l", "r", "b"]:
        d = random.randint(0, 2)
        if d == 1:
            tips.append(t)
        elif d == 2:
            tips.append(t + "'")
    return " ".join(moves + tips)


def _skewb(length=11):
    faces = ["R", "U", "L", "B"]
    moves = []
    last = None
    while len(moves) < length:
        f = random.choice(faces)
        if f == last:
            continue
        last = f
        moves.append(f + random.choice(["", "'"]))
    return " ".join(moves)


def _megaminx(lines=7):
    """Pochmann-style megaminx scramble (WCA format), one line per row."""
    out = []
    for _ in range(lines):
        row = []
        for i in range(10):
            letter = "R" if i % 2 == 0 else "D"
            row.append(letter + random.choice(["++", "--"]))
        row.append(random.choice(["U", "U'"]))
        out.append(" ".join(row))
    return "\n".join(out)


def _clock():
    def m():
        v = random.randint(-5, 6)
        return "%d%s" % (abs(v), "+" if v >= 0 else "-")

    parts = []
    for pin in ["UR", "DR", "DL", "UL", "U", "R", "D", "L", "ALL"]:
        parts.append(pin + m())
    parts.append("y2")
    for pin in ["U", "R", "D", "L", "ALL"]:
        parts.append(pin + m())
    return " ".join(parts)


# --- Square-1 --------------------------------------------------------------
# Each layer is 12 units of 30 degrees; a corner occupies two consecutive
# units with the same piece id, an edge occupies one unit. Both layers are
# indexed by the same angle seen from the top (counter-clockwise), starting
# at the slice cut, so in the solved state the bottom pieces sit exactly
# under the top pieces (edge, corner, edge, corner ... from the cut).
# The slash swaps the "right half" (units 0..5) of the top layer with units
# 5..0 of the bottom layer (a 180-degree turn of the right half).
# Check: from solved, (1,0)/ and (0,-1)/ are legal, (-1,0)/ and (0,1)/ are not.

_SQ1_START = [0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7,
              8, 9, 9, 10, 11, 11, 12, 13, 13, 14, 15, 15]


def _sq1_twist(state, top, bottom):
    t = state[:12]
    b = state[12:]
    # top clockwise (seen from top) by `top` units, bottom clockwise (seen
    # from bottom) by `bottom` units
    t = [t[(i + top) % 12] for i in range(12)]
    b = [b[(i - bottom) % 12] for i in range(12)]
    return t + b


def _sq1_can_slash(state):
    t = state[:12]
    b = state[12:]
    return t[11] != t[0] and t[5] != t[6] and b[11] != b[0] and b[5] != b[6]


def _sq1_slash(state):
    s = list(state)
    for i in range(6):
        s[i], s[12 + 5 - i] = state[12 + 5 - i], state[i]
    return s


def _sq1(slashes=12):
    state = list(_SQ1_START)
    out = []
    while len(out) < slashes:
        top = random.randint(-5, 6)
        bottom = random.randint(-5, 6)
        if top == 0 and bottom == 0 and out:
            continue
        cand = _sq1_twist(state, top, bottom)
        if not _sq1_can_slash(cand):
            continue
        state = _sq1_slash(cand)
        out.append("(%d,%d)/" % (top, bottom))
    return " ".join(out)


def _bld():
    """3BLD: random-move scramble plus a random cube orientation (WCA style)."""
    base = _nxn(3, 25)
    last_axis = _AXIS[base.split()[-1][0]]
    tail = []
    first = random.choice(["", "Rw", "Rw2", "Rw'", "Fw", "Fw'"])
    if first and _AXIS[first[0]] == last_axis:
        first = ""
    if first:
        tail.append(first)
    second = random.choice(["", "Uw", "Uw2", "Uw'"])
    if second and not tail and last_axis == _AXIS["U"]:
        second = ""
    if second:
        tail.append(second)
    return " ".join([base] + tail)


def _fmc():
    """FMC: R' U' F + scramble + R' U' F, as in official WCA scrambles."""
    # middle must not start on the F/B axis or end on the R/L axis
    mid = _nxn(3, 21, first_axis_not=_AXIS["F"], last_axis_not=_AXIS["R"])
    return "R' U' F " + mid + " R' U' F"


# ---------------------------------------------------------------------------

_LENGTH = {"222": 11, "333": 25, "444": 40, "555": 60, "666": 80, "777": 100}


def generate(puzzle):
    """Return a new scramble string for the given puzzle id."""
    if puzzle == "333oh":
        return _nxn(3, 25)
    if puzzle == "333bf":
        return _bld()
    if puzzle == "333fm":
        return _fmc()
    if puzzle in CUBE_SIZE:
        return _nxn(CUBE_SIZE[puzzle], _LENGTH[puzzle])
    if puzzle == "pyram":
        return _pyraminx()
    if puzzle == "skewb":
        return _skewb()
    if puzzle == "minx":
        return _megaminx()
    if puzzle == "clock":
        return _clock()
    if puzzle == "sq1":
        return _sq1()
    raise ValueError("Unknown puzzle: %r" % (puzzle,))
