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

class Case(object):
    __slots__ = ("id", "name", "alg", "set_id", "view", "group", "hint", "_state")

    def __init__(self, cid, name, alg, set_id, view, group=None, hint=None):
        self.id = cid
        self.name = name          # (en, ru)
        self.alg = alg
        self.set_id = set_id
        self.view = view          # "oll", "pll", "f2l", "full"
        self.group = group        # (en, ru) or None
        self.hint = hint          # (en, ru) or None
        self._state = None

    def state(self):
        """Cube showing this case (cached)."""
        if self._state is None:
            self._state = case_state(self.alg)
        return self._state

    def setup(self):
        """Scramble that creates the case from a solved cube."""
        return setup_moves(self.alg)


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
    return sets


SETS = _build()
SET_BY_ID = dict((s.id, s) for s in SETS)
CASES = {}
for _s in SETS:
    for _c in _s.cases:
        CASES[_c.id] = _c
