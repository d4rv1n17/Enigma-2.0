# -*- coding: utf-8 -*-
"""Algorithm database for the Training section (3x3, Fridrich / CFOP).

Sources:
  OLL 1-57, PLL 21  - speedcubedb.com (main algorithm of each case)
  F2L 1-41          - cubingcheatsheet.com
  Beginner method   - ruwix.com
  2-look OLL/PLL    - the standard beginner subsets of the above

Every algorithm is checked by tests/test_algs.py with the cube simulator:
it must keep the already-solved part of the cube intact, and all cases of a
set must be different. Case pictures are generated from the algorithm itself,
so a picture always matches its algorithm.
"""

from .cube import invert
from .fast3 import case_state, net_rotation

# ---------------------------------------------------------------------------
# Raw data
# ---------------------------------------------------------------------------

OLL = [
    # number, group (en, ru), algorithm
    (1, "dot", "R U2 R2 F R F' U2 R' F R F'"),
    (2, "dot", "y' R U' R2 D' r U r' D R2 U R'"),
    (3, "dot", "y' f R U R' U' f' U' F R U R' U' F'"),
    (4, "dot", "y' R' F2 R2 U2 R' F' R U2 R2 F2 R"),
    (5, "square", "r' U2 R U R' U r"),
    (6, "square", "r U2 R' U' R U' r'"),
    (7, "lightning", "r U R' U R U2 r'"),
    (8, "lightning", "y2 r' U' R U' R' U2 r"),
    (9, "fish", "y R U R' U' R' F R2 U R' U' F'"),
    (10, "fish", "R U R' U R' F R F' R U2 R'"),
    (11, "lightning", "r' R2 U R' U R U2 R' U M'"),
    (12, "lightning", "y' M' R' U' R U' R' U2 R U' M"),
    (13, "knight", "F U R U2 R' U' R U R' F'"),
    (14, "knight", "R' F R U R' F' R F U' F'"),
    (15, "knight", "r' U' r R' U' R U r' U r"),
    (16, "knight", "r U r' R U R' U' r U' r'"),
    (17, "dot", "R U R' U R' F R F' U2 R' F R F'"),
    (18, "dot", "y R U2 R2 F R F' U2 M' U R U' r'"),
    (19, "dot", "y S' R U R' S U' R' F R F'"),
    (20, "dot", "r U R' U' M2 U R U' R' U' M'"),
    (21, "ocll", "R U R' U R U' R' U R U2 R'"),
    (22, "ocll", "R U2 R2 U' R2 U' R2 U2 R"),
    (23, "ocll", "R2 D R' U2 R D' R' U2 R'"),
    (24, "ocll", "r U R' U' r' F R F'"),
    (25, "ocll", "R U2 R D R' U2 R D' R2"),
    (26, "ocll", "y R U2 R' U' R U' R'"),
    (27, "ocll", "R U R' U R U2 R'"),
    (28, "corners", "r U R' U' M U R U' R'"),
    (29, "awkward", "r2 D' r U r' D r2 U' r' U' r"),
    (30, "awkward", "y2 F U R U2 R' U' R U2 R' U' F'"),
    (31, "p", "R' U' F U R U' R' F' R"),
    (32, "p", "S R U R' U' R' F R f'"),
    (33, "t", "R U R' U' R' F R F'"),
    (34, "c", "y f R f' U' r' U' R U M'"),
    (35, "fish", "R U2 R2 F R F' R U2 R'"),
    (36, "w", "y R U R2 F' U' F U R2 U2 R'"),
    (37, "fish", "F R' F' R U R U' R'"),
    (38, "w", "R U R' U R U' R' U' R' F R F'"),
    (39, "lightning", "y' f' r U r' U' r' F r S"),
    (40, "lightning", "y R' F R U R' U' F' U R"),
    (41, "awkward", "y2 R U R' U R U2 R' F R U R' U' F'"),
    (42, "awkward", "R' U' R U' R' U2 R F R U R' U' F'"),
    (43, "p", "y R' U' F' U F R"),
    (44, "p", "f R U R' U' f'"),
    (45, "t", "F R U R' U' F'"),
    (46, "c", "R' U' R' F R F' U R"),
    (47, "l", "y' F R' F' R U2 R U' R' U R U2 R'"),
    (48, "l", "F R U R' U' R U R' U' F'"),
    (49, "l", "y2 r U' r2 U r2 U r2 U' r"),
    (50, "l", "r' U r2 U' r2 U' r2 U r'"),
    (51, "line", "y2 F U R U' R' U R U' R' F'"),
    (52, "line", "y2 R' F' U' F U' R U R' U R"),
    (53, "l", "r' U' R U' R' U R U' R' U2 r"),
    (54, "l", "r U R' U R U' R' U R U2 r'"),
    (55, "line", "y R' F U R U' R2 F' R2 U R' U' R"),
    (56, "line", "r U r' U R U' R' U R U' R' r U' r'"),
    (57, "corners", "R U R' U' M' U R U' r'"),
]

OLL_GROUPS = {
    "dot": ("Dot", "Точка"),
    "square": ("Square", "Квадрат"),
    "lightning": ("Lightning", "Молния"),
    "fish": ("Fish", "Рыба"),
    "knight": ("Knight move", "Ход конём"),
    "ocll": ("Cross (OCLL)", "Крест (OCLL)"),
    "corners": ("Corners oriented", "Углы на месте"),
    "awkward": ("Awkward", "Неудобные"),
    "p": ("P shape", "Буква P"),
    "t": ("T shape", "Буква T"),
    "c": ("C shape", "Буква C"),
    "w": ("W shape", "Буква W"),
    "l": ("Small L", "Малая L"),
    "line": ("Line", "Линия"),
}

# common nicknames for the 7 corner cases (OCLL)
OCLL_NAMES = {
    21: ("H", "H"), 22: ("Pi", "Пи"), 23: ("Headlights", "Фары"),
    24: ("Chameleon", "Хамелеон"), 25: ("Bowtie", "Бабочка"),
    26: ("Antisune", "Антисуне"), 27: ("Sune", "Суне"),
}

PLL = [
    ("Aa", "corners", "x R' U R' D2 R U' R' D2 R2 x'"),
    ("Ab", "corners", "x R2 D2 R U R' D2 R U' R x'"),
    ("E", "corners", "y x' R U' R' D R U R' D' R U R' D R U' R' D' x"),
    ("F", "adjacent", "y R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R"),
    ("Ga", "g", "R2 U R' U R' U' R U' R2 D U' R' U R D'"),
    ("Gb", "g", "D R' U' R U D' R2 U R' U R U' R U' R2"),
    ("Gc", "g", "R2 U' R U' R U R' U R2 D' U R U' R' D"),
    ("Gd", "g", "R U R' U' D R2 U' R U' R' U R' U R2 D'"),
    ("H", "edges", "M2 U M2 U2 M2 U M2"),
    ("Ja", "adjacent", "y2 x R2 F R F' R U2 r' U r U2 x'"),
    ("Jb", "adjacent", "R U R' F' R U R' U' R' F R2 U' R'"),
    ("Na", "diagonal", "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'"),
    ("Nb", "diagonal", "R' U R U' R' F' U' F R U R' F R' F' R U' R"),
    ("Ra", "adjacent", "y R U' R' U' R U R D R' U' R D' R' U2 R'"),
    ("Rb", "adjacent", "R' U2 R U2 R' F R U R' U' R' F' R2"),
    ("T", "adjacent", "R U R' U' R' F R2 U' R' U' R U R' F'"),
    ("Ua", "edges", "y2 M2 U M U2 M' U M2"),
    ("Ub", "edges", "y2 M2 U' M U2 M' U' M2"),
    ("V", "diagonal", "R' U R' U' R D' R' D R' U D' R2 U' R2 D R2"),
    ("Y", "diagonal", "F R U' R' U' R U R' F' R U R' U' R' F R F'"),
    ("Z", "edges", "M' U' M2 U' M2 U' M' U2 M2"),
]

PLL_GROUPS = {
    "edges": ("Edges only", "Только рёбра"),
    "corners": ("Corners only", "Только углы"),
    "adjacent": ("Adjacent corner swap", "Соседние углы"),
    "diagonal": ("Diagonal corner swap", "Диагональные углы"),
    "g": ("G perms", "G-перестановки"),
}

F2L = [
    (1, "U R U' R'"),
    (2, "U' F' U F"),
    (3, "F' U' F"),
    (4, "R U R'"),
    (5, "U' R U R' U' R U2 R'"),
    (6, "U F' U' F U F' U2 F"),
    (7, "U' R U2 R' U' R U2 R'"),
    (8, "U F' U2 F U F' U2 F"),
    (9, "U F' U' F U' F' U' F"),
    (10, "U' R U R' U R U R'"),
    (11, "U' R U2 R' d R' U' R"),
    (12, "d R' U2 R d' R U R'"),
    (13, "U F' U F U' F' U' F"),
    (14, "U' R U' R' U R U R'"),
    (15, "F' U F U' d' F U F'"),
    (16, "R U' R' U d R' U' R"),
    (17, "R U2 R' U' R U R'"),
    (18, "F' U2 F U F' U' F"),
    (19, "U R U2 R' U R U' R'"),
    (20, "U' F' U2 F U' F' U F"),
    (21, "U2 R U R' U R U' R'"),
    (22, "U2 F' U' F U' F' U F"),
    (23, "R U R' U' U' R U R' U' R U R'"),
    (24, "y' R' U' R U U R' U' R U R' U' R"),
    (25, "U' F' U F U R U' R'"),
    (26, "U R U' R' U' F' U F"),
    (27, "R U' R' U R U' R'"),
    (28, "F' U F U' F' U F"),
    (29, "F' U' F U F' U' F"),
    (30, "R U R' U' R U R'"),
    (31, "R U' R' d R' U R"),
    (32, "R U R' U' R U R' U' R U R'"),
    (33, "U' R U' R' U' R U2 R'"),
    (34, "U F' U F U F' U2 F"),
    (35, "U' R U R' d R' U' R"),
    (36, "U F' U' F d' F U F'"),
    (37, "R U' R' d R' U2 R U R' U2 R"),
    (38, "R U' R' U' R U R' U' R U2 R'"),
    (39, "R U' R' U R U2 R' U R U' R'"),
    (40, "R U' R' d R' U' R U' R' U' R"),
    (41, "R U R' U' R U' R' U d R' U' R"),
]
# cubingcheatsheet numbers the 42 positions including "solved"; we keep its
# order but skip the solved one, which gives the usual 41 cases.

BEGINNER = [
    # id, (name en, name ru), algorithm, (hint en, hint ru)
    ("b-corner", ("First layer corner", "Угол первого слоя"), "R U R' U'",
     ("Corner above its slot (front-right): repeat until it is in place.",
      "Угол над своим местом (спереди справа): повторяй, пока он не встанет.")),
    ("b-edge-r", ("Second layer: edge to the right", "Второй слой: ребро вправо"),
     "U R U' R' U' F' U F",
     ("Edge on top matches the front centre and goes to the right.",
      "Ребро сверху совпадает с передним центром и идёт вправо.")),
    ("b-edge-l", ("Second layer: edge to the left", "Второй слой: ребро влево"),
     "U' L' U L U F U' F'",
     ("Mirror of the previous one: the edge goes to the left.",
      "Зеркальный случай: ребро идёт влево.")),
    ("b-cross", ("Yellow cross", "Жёлтый крест"), "F R U R' U' F'",
     ("Dot: 3 times. L shape (at back-left): twice. Line (horizontal): once.",
      "Точка: 3 раза. Уголок (сзади слева): 2 раза. Линия (горизонтально): 1 раз.")),
    ("b-edges", ("Yellow edges", "Жёлтые рёбра"), "R U R' U R U2 R' U",
     ("Swaps the front and left yellow edges.",
      "Меняет местами переднее и левое жёлтые рёбра.")),
    ("b-corners", ("Place yellow corners", "Расставить жёлтые углы"), "U R U' L' U R' U' L",
     ("Keep a correctly placed corner at front-right and cycle the other three.",
      "Держи правильно стоящий угол спереди справа — остальные три сменятся по кругу.")),
    ("b-twist", ("Turn yellow corners", "Повернуть жёлтые углы"), "R' D' R D",
     ("Corner at front-right: repeat 2 or 4 times, then turn only U.",
      "Угол спереди справа: повтори 2 или 4 раза, потом крути только U.")),
]

EO_2LOOK = [
    ("oll2-line", ("Line", "Линия"), "F R U R' U' F'"),
    ("oll2-l", ("L shape", "Уголок"), "f R U R' U' f'"),
    ("oll2-dot", ("Dot", "Точка"), "F R U R' U' F' f R U R' U' f'"),
]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def invert_minx(alg):
    """Inverse of a megaminx algorithm (U2 = 144 degrees, so U2 -> U2')."""
    out = []
    for tok in reversed(alg.split()):
        base = tok.rstrip("'2")
        suffix = tok[len(base):]
        out.append(base + {"": "'", "'": "", "2": "2'", "2'": "2", "'2": "2"}.get(suffix, "'"))
    return " ".join(out)


# Alternative algorithms (second / third choice on speedcubedb.com). Every one
# is checked in tests/test_algs.py to solve exactly the same case as the main one.
ALTS = {
    "oll-1": ["y R U' R2 D' r U' r' D R2 U R'"],
    "oll-2": ["F R U R' U' S R U R' U' f'"],
    "oll-3": ["y R' F2 R2 U2 R' F R U2 R2 F2 R"],
    "oll-4": ["y' f R U R' U' f' U F R U R' U' F'"],
    "oll-5": ["y2 l' U2 L U L' U l"],
    "oll-6": ["F U' R2 D R' U' R D' R2 U F'"],
    "oll-7": ["S' R U R' U R U2 R' U S"],
    "oll-8": ["l' U' L U' L' U2 l"],
    "oll-9": ["R U2 R' U' S' R U' R' S"],
    "oll-10": ["y F U F' R' F R U' R' F' R"],
    "oll-11": ["y2 r U R' U R' F R F' R U2 r'"],
    "oll-12": ["F R U R' U' F' U F R U R' U' F'"],
    "oll-13": ["F U R U' R2 F' R U R U' R'"],
    "oll-14": ["r U R' U' r' F R2 U R' U' F'"],
    "oll-15": ["y2 l' U' l L' U' L U l' U l"],
    "oll-16": ["r U M U R' U' r U' r'"],
    "oll-17": ["y2 F R' F' R U S' R U' R' S"],
    "oll-18": ["r U R' U R U2 r2 U' R U' R' U2 r"],
    "oll-19": ["M U R U R' U' M' R' F R F'"],
    "oll-20": ["M' U2 M U2 M' U M U2 M' U2 M"],
    "oll-21": ["y R U2 R' U' R U R' U' R U' R'"],
    "oll-22": ["R' U2 R2 U R2 U R2 U2 R'"],
    "oll-23": ["y2 R2 D' R U2 R' D R U2 R"],
    "oll-24": ["y2 R' F' r U R U' r' F"],
    "oll-25": ["y F' r U R' U' r' F R"],
    "oll-26": ["R' U' R U' R' U2 R"],
    "oll-27": ["y' R' U2 R U R' U R"],
    "oll-28": ["R' F R S R' F' R S'"],
    "oll-29": ["y R U R' U' R U' R' F' U' F R U R'"],
    "oll-30": ["y' r' D' r U' r' D r2 U' r' U r U r'"],
    "oll-31": ["y2 S' L' U' L U L F' L' f"],
    "oll-32": ["y2 L U F' U' L' U L F L'"],
    "oll-33": ["y2 L' U' L U L F' L' F"],
    "oll-34": ["y2 R U R2 U' R' F R U R U' F'"],
    "oll-35": ["f R U R' U' f' R U R' U R U2 R'"],
    "oll-36": ["y2 L' U' L U' L' U L U L F' L' F"],
    "oll-37": ["F R U' R' U' R U R' F'"],
    "oll-38": ["y F R U' R' S U' R U R' f'"],
    "oll-39": ["y' R U R' F' U' F U R U2 R'"],
    "oll-40": ["y' f R' F' R U R U' R' S'"],
    "oll-41": ["y2 F U R2 D R' U' R D' R2 F'"],
    "oll-42": ["y F S' R U R' U' F' U S"],
    "oll-43": ["y2 F' U' L' U L F"],
    "oll-44": ["y2 F U R U' R' F'"],
    "oll-45": ["y R' F' U' F U R"],
    "oll-46": ["R' F' U' F R U' R' U2 R"],
    "oll-47": ["F' L' U' L U L' U' L U F"],
    "oll-48": ["y2 f U R U' R' U R U' R' f'"],
    "oll-49": ["l U' l2 U l2 U l2 U' l"],
    "oll-50": ["y2 R' F R2 B' R2 F' R2 B R'"],
    "oll-51": ["f R U R' U' R U R' U' f'"],
    "oll-52": ["R U R' U R U' B U' B' R'"],
    "oll-53": ["y2 l' U' L U' L' U L U' L' U2 l"],
    "oll-54": ["y' r U2 R' U' R U R' U' R U' r'"],
    "oll-55": ["y R' F R U R U' R2 F' R2 U' R' U R U R'"],
    "oll-56": ["r U r' U R U' R' M' U R U2 r'"],
    "oll-57": ["y R U' R' S' R U R' S"],
    "pll-Aa": ["y' x L2 D2 L' U' L D2 L' U L'", "l' U R' D2 R U' R' D2 R2 x'"],
    "pll-Ab": ["y' x L U' L D2 L' U L D2 L2", "y x' R U' R D2 R' U R D2 R2 x"],
    "pll-E": ["R' U' R' D' R U' R' D R U R' D' R U R' D R2", "R2 U F' R' U R U' R' U R U' R' U R U' F U' R2"],
    "pll-F": ["y R' F R f' R' F R2 U R' U' R' F' R2 U R' S", "R' U R U' R2 F' U' F U R F R' F' R2"],
    "pll-Ga": ["R2 u R' U R' U' R u' R2 F' U F", "y R U R' F' R U R' U' R' F R U' R' F R2 U' R' U' R U R' F'"],
    "pll-Gb": ["R' U' R U D' R2 U R' U R U' R U' R2 D", "y F' U' F R2 u R' U R U' R u' R2"],
    "pll-Gc": ["y2 R2 F2 R U2 R U2 R' F R U R' U' R' F R2", "D R2 U' R U' R U R' U R2 D' U R U' R'"],
    "pll-Gd": ["D' R U R' U' D R2 U' R U' R' U R' U R2", "R U R' y' R2 u' R U' R' U R' u R2"],
    "pll-H": ["M2 U' M2 U2 M2 U' M2", "R2 S2 R2 U' R2 S2 R2"],
    "pll-Ja": ["y R' U L' U2 R U' R' U2 R L", "L' U' L F L' U' L U L F' L2 U L"],
    "pll-Jb": ["R U2 R' U' R U2 L' U R' U' L", "r' F R F' r U2 R' U R U2 R'"],
    "pll-Na": ["F' R U R' U' R' F R2 F U' R' U' R U F' R'", "R F U' R' U R U F' R2 F' R U R U' R' F"],
    "pll-Nb": ["r' D' F r U' r' F' D r2 U r' U' r' F r F'", "R' U L' U2 R U' L R' U L' U2 R U' L"],
    "pll-Ra": ["y R U R' F' R U2 R' U2 R' F R U R U2 R'", "L U2 L' U2 L F' L' U' L U L F L2"],
    "pll-Rb": ["y R2 F R U R U' R' F' R U2 R' U2 R", "R' U2 R' D' R U' R' D R U R U' R' U' R"],
    "pll-T": ["R U R' U' R' F R2 U' R' U F' L' U L"],
    "pll-Ua": ["R U R' U R' U' R2 U' R' U R' U R", "y R2 U' S' U2 S U' R2"],
    "pll-Ub": ["R' U R' U' R' U' R' U R U R2"],
    "pll-V": ["R' U R U' R' f' U' R U2 R' U' R U' R' f R", "R' U R' U' y R' F' R2 U' R' U R' F R F"],
    "pll-Y": ["F R' F R2 U' R' U' R U R' F' R U R' U' F'", "R2 U' R2 U' R2 U F U F' R2 F U' F'"],
    "pll-Z": ["M2 U M2 U M' U2 M2 U2 M'", "y M2 U' M2 U' M' U2 M2 U2 M'"],
}


class Case(object):
    __slots__ = ("id", "name", "alg", "set_id", "view", "group", "hint", "puzzle", "_state")

    @property
    def alts(self):
        """Verified alternative algorithms for this case (may be empty)."""
        return ALTS.get(self.id, [])

    def __init__(self, cid, name, alg, set_id, view, group=None, hint=None, puzzle="333"):
        self.id = cid
        self.name = name          # (en, ru)
        self.alg = alg
        self.set_id = set_id
        self.view = view          # oll, pll, f2l, full, eo, ll2, pll2, pbl, ll4, pll4,
        #                           pyra, skewb, sq1, none
        self.group = group        # (en, ru) or None
        self.hint = hint          # (en, ru) or None
        self.puzzle = puzzle      # event id the case belongs to
        self._state = None

    def state(self):
        """Puzzle state showing this case (cached; None if there is no simulator)."""
        if self._state is None:
            self._state = _puzzle_case_state(self.puzzle, self.alg)
        return self._state

    def setup(self):
        """Moves that create the case on a solved puzzle."""
        return _puzzle_setup(self.puzzle, self.alg)


def _puzzle_case_state(puzzle, alg):
    if puzzle in ("333", "333bf", "333oh"):
        return case_state(alg)
    if puzzle in ("222", "444", "555"):
        from .fastn import NState, net_rotation as nrot, centre_rotation
        n = int(puzzle[0])
        rot = nrot(n, alg) if n == 2 else centre_rotation(n, alg)
        return NState(n).apply(rot).apply(invert(alg))
    if puzzle == "pyram":
        from .puzzles import Pyraminx
        return Pyraminx().apply(invert(alg))
    if puzzle == "skewb":
        from .puzzles import Skewb
        return Skewb().apply(invert(alg))
    if puzzle == "sq1":
        from .puzzles import sq1_invert
        return sq1_invert(alg)          # drawn from this move sequence
    return None


def _puzzle_setup(puzzle, alg):
    if puzzle in ("333", "333bf", "333oh"):
        return setup_moves(alg)
    if puzzle in ("222", "444", "555"):
        from .fastn import net_rotation as nrot, centre_rotation
        n = int(puzzle[0])
        rot = nrot(n, alg) if n == 2 else centre_rotation(n, alg)
        return (rot + " " + invert(alg)).strip()
    if puzzle == "sq1":
        from .puzzles import sq1_invert
        return sq1_invert(alg)
    if puzzle == "minx":
        return invert_minx(alg)
    return invert(alg)


class AlgSet(object):
    def __init__(self, sid, name, cases, description=("", "")):
        self.id = sid
        self.name = name
        self.cases = cases
        self.description = description


def setup_moves(alg):
    """Moves that create the case on a solved cube (held in the usual way)."""
    return (net_rotation(alg) + " " + invert(alg)).strip()


def _build():
    sets = []
    views = {"b-corner": "f2l", "b-edge-r": "f2l", "b-edge-l": "f2l", "b-cross": "oll",
             "b-edges": "full", "b-corners": "full", "b-twist": "full"}
    beginner = [Case(cid, name, alg, "beginner", views[cid], hint=hint)
                for cid, name, alg, hint in BEGINNER]
    sets.append(AlgSet("beginner", ("Beginner method", "Метод для начинающих"), beginner,
                       ("7 simple steps, 7 short algorithms.",
                        "7 простых шагов и 7 коротких алгоритмов.")))

    oll_cases = {}
    for num, group, alg in OLL:
        name = ("OLL %d" % num, "OLL %d" % num)
        if num in OCLL_NAMES:
            en, ru = OCLL_NAMES[num]
            name = ("OLL %d · %s" % (num, en), "OLL %d · %s" % (num, ru))
        oll_cases[num] = Case("oll-%d" % num, name, alg, "oll", "oll", OLL_GROUPS[group])
    pll_cases = {}
    for pname, group, alg in PLL:
        pll_cases[pname] = Case("pll-%s" % pname, ("%s perm" % pname, "%s-перестановка" % pname),
                                alg, "pll", "pll", PLL_GROUPS[group])

    eo = [Case(cid, name, alg, "oll2", "oll", ("Edges", "Рёбра")) for cid, name, alg in EO_2LOOK]
    co = [oll_cases[n] for n in (27, 26, 23, 24, 25, 21, 22)]
    sets.append(AlgSet("oll2", ("2-look OLL", "OLL в 2 этапа"), eo + co,
                       ("Orient the last layer in two steps: 3 edge + 7 corner algorithms.",
                        "Ориентация последнего слоя за 2 шага: 3 алгоритма для рёбер и 7 для углов.")))
    cp = [pll_cases[n] for n in ("T", "Y")]
    ep = [pll_cases[n] for n in ("Ua", "Ub", "H", "Z")]
    sets.append(AlgSet("pll2", ("2-look PLL", "PLL в 2 этапа"), cp + ep,
                       ("Permute the last layer in two steps: corners, then edges.",
                        "Расстановка последнего слоя за 2 шага: сначала углы, потом рёбра.")))
    f2l = [Case("f2l-%d" % num, ("F2L %d" % num, "F2L %d" % num), alg, "f2l", "f2l")
           for num, alg in F2L]
    sets.append(AlgSet("f2l", ("F2L", "F2L"), f2l,
                       ("First two layers: pair a corner with its edge and insert them together.",
                        "Первые два слоя: собираешь угол с ребром в пару и вставляешь вместе.")))
    sets.append(AlgSet("oll", ("OLL", "OLL"), [oll_cases[n] for n, _, _ in OLL],
                       ("All 57 cases: orient the last layer in one step.",
                        "Все 57 случаев: ориентация последнего слоя за один шаг.")))
    sets.append(AlgSet("pll", ("PLL", "PLL"), [pll_cases[n] for n, _, _ in PLL],
                       ("All 21 cases: permute the last layer in one step.",
                        "Все 21 случай: расстановка последнего слоя за один шаг.")))
    sets.extend(_build_other_events())
    return sets


def _named(prefix, set_id, view, puzzle, items, group=None):
    out = []
    for name, alg in items:
        cid = "%s-%s" % (prefix, name.lower().replace(" ", "-").replace("·", "").replace("--", "-"))
        out.append(Case(cid, (name, name), alg, set_id, view, group, puzzle=puzzle))
    return out


def _described(set_id, view, puzzle, items):
    return [Case(cid, name, alg, set_id, view, hint=hint, puzzle=puzzle)
            for cid, name, alg, hint in items]


def _build_other_events():
    from . import methods as M
    sets = []

    def add(sid, name, cases, desc):
        sets.append(AlgSet(sid, name, cases, desc))

    # 2x2
    add("222-beginner", ("Beginner method", "Метод для начинающих"),
        _described("222-beginner", "cll2", "222", M.BEGINNER_222),
        ("Layer by layer with 4 algorithms.", "Послойно, всего 4 алгоритма."))
    add("222-ortega-oll", ("Ortega: OLL", "Ортега: OLL"),
        _named("ortega-oll", "222-ortega-oll", "ll2", "222", M.ORTEGA_OLL),
        ("Orient the last layer (bottom face only needs one colour).",
         "Ориентация верхнего слоя (снизу нужен только один цвет)."))
    add("222-ortega-pbl", ("Ortega: PBL", "Ортега: PBL"),
        _named("ortega-pbl", "222-ortega-pbl", "pbl", "222", M.ORTEGA_PBL),
        ("Permute both layers at once.", "Расстановка обоих слоёв сразу."))
    add("222-cll", ("CLL", "CLL"),
        _named("cll", "222-cll", "cll2", "222", M.CLL),
        ("Solve the whole last layer in one algorithm after the first layer.",
         "Весь последний слой одним алгоритмом после первого слоя."))
    # big cubes
    add("444-parity", ("4x4 parity", "Паритеты 4x4"),
        _described("444-parity", "ll4", "444", M.PARITY_444),
        ("Cases that cannot happen on a 3x3.", "Случаи, которых не бывает на 3x3."))
    add("555-edges", ("5x5 edge pairing", "Сборка рёбер 5x5"),
        _described("555-edges", "none", "555", M.EDGES_555),
        ("Pair the last edges without breaking the centres.",
         "Собрать последние рёбра, не ломая центры."))
    # pyraminx
    add("pyra-beginner", ("Beginner method", "Метод для начинающих"),
        _described("pyra-beginner", "pyra", "pyram", M.PYRA_BEGINNER),
        ("Tips, centres, then edges with 5 short algorithms.",
         "Вершины, центры, затем рёбра — 5 коротких алгоритмов."))
    add("pyra-l4e", ("L4E", "L4E"),
        _named("l4e", "pyra-l4e", "pyra", "pyram", M.PYRA_L4E),
        ("Last four edges: 36 cases used by fast solvers.",
         "Последние четыре ребра: 36 случаев, которыми пользуются быстрые сборщики."))
    # skewb
    add("skewb-layer", ("Layer method", "Послойный метод"),
        _named("skewb-c", "skewb-layer", "skewb", "skewb", M.SKEWB_CORNERS,
               ("Top corners", "Верхние углы")) +
        _named("skewb-z", "skewb-layer", "skewb", "skewb", M.SKEWB_CENTRES,
               ("Last centres", "Последние центры")),
        ("First layer by intuition, then 2 corner and 16 centre algorithms "
         "(optimal, computed by the app).",
         "Первый слой интуитивно, затем 2 алгоритма для углов и 16 для центров "
         "(оптимальные, вычислены программой)."))
    # megaminx
    # 3x3 Roux
    cmll = []
    for name, alg in M.CMLL:
        group = name.rsplit(" ", 2)[0] if name.startswith("Anti Sune") else name.split(" ")[0]
        cid = "cmll-" + name.lower().replace(" ", "-")
        cmll.append(Case(cid, ("CMLL · " + name, "CMLL · " + name), alg, "333-cmll", "cmll",
                         (group, group), puzzle="333"))
    add("333-cmll", ("Roux: CMLL", "Roux: CMLL"), cmll,
        ("Corners of the last layer in one look, keeping both Roux blocks.",
         "Углы последнего слоя за один взгляд, не ломая блоки Roux."))
    add("minx-ll", ("4-look last layer", "Последний слой в 4 этапа"),
        _named("minx-eo", "minx-ll", "none", "minx", M.MINX_EO, ("Edge orientation", "Ориентация рёбер")) +
        _named("minx-co", "minx-ll", "none", "minx", M.MINX_CO, ("Corner orientation", "Ориентация углов")) +
        _named("minx-ep", "minx-ll", "none", "minx", M.MINX_EP, ("Edge permutation", "Перестановка рёбер")) +
        _named("minx-cp", "minx-ll", "none", "minx", M.MINX_CP, ("Corner permutation", "Перестановка углов")),
        ("EO, CO, EP, CP — 39 algorithms.", "EO, CO, EP, CP — 39 алгоритмов."))
    # square-1
    add("sq1-beginner", ("Beginner method", "Метод для начинающих"),
        _described("sq1-beginner", "sq1", "sq1", M.SQ1_BEGINNER),
        ("Cube shape, corners, edges and parity.", "Форма куба, углы, рёбра и паритет."))
    # blindfolded
    add("bld-op", ("Old Pochmann", "Old Pochmann"),
        _described("bld-op", "full", "333bf", M.BLD_OP),
        ("Solve one piece at a time with swap algorithms.",
         "Собираешь по одной детали алгоритмами обмена."))
    return sets


SETS = _build()
SET_BY_ID = dict((s.id, s) for s in SETS)
CASES = {}
for _s in SETS:
    for _c in _s.cases:
        CASES[_c.id] = _c
