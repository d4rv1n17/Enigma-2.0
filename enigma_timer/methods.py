# -*- coding: utf-8 -*-
"""Algorithm sets for every event other than the 3x3 CFOP sets in algs.py.

Sources (main algorithm of each case):
  2x2 Ortega OLL / PBL, 2x2 CLL, Pyraminx L4E, Megaminx EO/CO/EP/CP,
  4x4 parity                                     - speedcubedb.com
  Square-1 beginner                              - ruwix.com
  Skewb layer method                             - computed and verified with
                                                   the built-in Skewb simulator
                                                   (WCA notation, optimal length)
Every set except Megaminx (no simulator) is checked in tests/test_methods.py.
"""

# ---------------------------------------------------------------------------
# 2x2
# ---------------------------------------------------------------------------

BEGINNER_222 = [
    ("222-corner", ("First layer corner", "Угол первого слоя"), "R U R' U'",
     ("Corner above its spot at front-right: repeat until it is in place.",
      "Угол над своим местом спереди справа: повторяй, пока он не встанет.")),
    ("222-sune", ("Sune: turn top corners", "Суне: поворот верхних углов"), "R U R' U R U2 R'",
     ("Repeat (turning U between) until all yellow stickers face up.",
      "Повторяй (поворачивая U между повторами), пока весь жёлтый не будет сверху.")),
    ("222-t", ("T perm: swap two corners", "T: обмен двух соседних углов"),
     "R U R' U' R' F R2 U' R' U' R U R' F'",
     ("Two matching corners (headlights) at the back, swap the front-right pair.",
      "Два совпадающих угла («фары») сзади — меняет правую пару.")),
    ("222-y", ("Y perm: swap diagonal corners", "Y: обмен по диагонали"),
     "F R U' R' U' R U R' F' R U R' U' R' F R F'",
     ("No headlights anywhere: swaps two diagonal corners.",
      "«Фар» нет нигде: меняет два угла по диагонали.")),
]

ORTEGA_OLL = [
    ("Sune", "R U R' U R U2 R'"),
    ("Anti Sune", "R U2 R' U' R U' R'"),
    ("Pi", "F R U R' U' R U R' U' F'"),
    ("P", "F R U R' U' F'"),
    ("L", "y F' R U R' U' R' F R"),
    ("T", "R U R' U' R' F R F'"),
    ("H", "R2 U2 R' U2 R2"),
]

ORTEGA_PBL = [
    ("Adj", "y R U R' F' R U R' U' R' F R2 U' R'"),
    ("Opp", "R U' R' U' F2 U' R U R' U F2"),
    ("Opp Opp", "R2 F2 R2"),
    ("Adj Adj", "R2 U' B2 U2 R2 U' R2"),
    ("Adj Opp", "R U' R F2 R' U R'"),
    ("Opp Adj", "y R2 U R2 U' R2 U R2 U' R2"),
]

CLL = [
    ("AS 1", "y R U2 R' U' R U' R'"),
    ("AS 2", "R U2 R' F R' F' R U' R U' R'"),
    ("AS 3", "y2 F' L F L' U2 L' U2 L"),
    ("AS 4", "y2 R' F R F' R U R'"),
    ("AS 5", "y2 R U2 R' U2 R' F R F'"),
    ("AS 6", "y' R U2 R' U' R U' R' F R' F' R U R U' R' U'"),
    ("H 1", "F R2 U' R2 U' R2 U R2 F'"),
    ("H 2", "R U R' U R U R' F R' F' R"),
    ("H 3", "y F R U R' U' R U R' U' R U R' U' F'"),
    ("H 4", "y R2 U2 R' U2 R2"),
    ("L 1", "y R U2 R' F' R U2 R' U R' F2 R"),
    ("L 2", "y2 R U2 R2 F2 R U R' F2 R F'"),
    ("L 3", "y2 R' U R' U2 R U' R' U R U' R2"),
    ("L 4", "y R U2 R2 F R F' R U2 R'"),
    ("L 5", "y F R' F' R U R U' R'"),
    ("L 6", "y2 F' R U R' U' R' F R"),
    ("Pi 1", "y F R' F' R U2 R U' R' U R U2 R'"),
    ("Pi 2", "R U2 R' U' R U R' U2 R' F R F'"),
    ("Pi 3", "y F R2 U' R2 U R2 U R2 F'"),
    ("Pi 4", "y2 R' F R F' R U' R' U' R U' R'"),
    ("Pi 5", "y' R' U' R' F R F' R U' R' U2 R"),
    ("Pi 6", "F R U R' U' R U R' U' F'"),
    ("Sune 1", "L' U2 L U2 L F' L' F"),
    ("Sune 2", "R U R' U' R' F R F' R U R' U R U2 R'"),
    ("Sune 3", "R U' R' F R' F' R"),
    ("Sune 4", "F R' F' R U2 R U2 R'"),
    ("Sune 5", "y2 R U R' U R' F R F' R U2 R'"),
    ("Sune 6", "R U R' U R U2 R'"),
    ("T 1", "y' R U R' U' R' F R F'"),
    ("T 2", "y L' U' L U L F' L' F"),
    ("T 3", "F U' R U2 R' U' F2 R U R'"),
    ("T 4", "R' U R U2 R2 F' R U' R' F2 R2"),
    ("T 5", "y2 F R U R' U' R U' R' U' R U R' F'"),
    ("T 6", "R' U R U2 R2 F R F' R"),
    ("U 1", "y' F R U R' U' F'"),
    ("U 2", "R' U' R2 U R' U2 R U2 R' U R'"),
    ("U 3", "y2 F R U R' U2 F' R U' R' F"),
    ("U 4", "y' F R' F' R U' R U' R' U2 R U' R'"),
    ("U 5", "R U' R2 F R F' R U R' U' R U R'"),
    ("U 6", "R' U R' F R F' R U2 R' U R"),
]

# ---------------------------------------------------------------------------
# Big cubes
# ---------------------------------------------------------------------------

PARITY_444 = [
    ("444-oll", ("OLL parity", "OLL-паритет"),
     "2R' U2 2L F2 2L' F2 2R2 U2 2R U2 2R' U2 F2 2R2 F2",
     ("One edge pair on top is flipped: hold it at the front. This 'pure' version "
      "changes nothing else.",
      "Одна пара рёбер наверху перевёрнута: держи её спереди. Эта «чистая» версия "
      "больше ничего не меняет.")),
    ("444-pll-opp", ("PLL parity: opposite edges", "PLL-паритет: противоположные рёбра"),
     "2R2 U2 2R2 Uw2 2R2 Uw2",
     ("Two opposite edges are swapped (front and back).",
      "Два противоположных ребра поменяны местами (спереди и сзади).")),
    ("444-pll-adj", ("PLL parity: adjacent edges", "PLL-паритет: соседние рёбра"),
     "R' U R U' 2R2 U2' 2R2 Uw2' 2R2 Uw2' U' R' U' R",
     ("Two adjacent edges are swapped.", "Два соседних ребра поменяны местами.")),
]

EDGES_555 = [
    ("555-l2e", ("Flip the last edge", "Перевернуть последнее ребро"), "Dw R F' U R' F Dw'",
     ("Edge pairing: fixes a flipped edge on the right while keeping the centres.",
      "Сборка рёбер: исправляет перевёрнутое ребро справа, не трогая центры.")),
]

# ---------------------------------------------------------------------------
# Pyraminx (WCA notation; L4E ends with a U adjustment when needed)
# ---------------------------------------------------------------------------

PYRA_BEGINNER = [
    ("pyra-righty", ("Insert an edge to the right", "Вставить ребро вправо"), "R U' R'", None),
    ("pyra-lefty", ("Insert an edge to the left", "Вставить ребро влево"), "L' U L", None),
    ("pyra-sune", ("Cycle 3 top edges (Sune)", "Цикл трёх рёбер (Суне)"), "R U R' U R U R'",
     ("Three edges move around the top; repeat once more for the other direction.",
      "Три верхних ребра меняются по кругу; повтори, чтобы в другую сторону.")),
    ("pyra-antisune", ("Cycle 3 top edges back", "Обратный цикл трёх рёбер"), "R U' R' U' R U' R'", None),
    ("pyra-flip", ("Flip two edges", "Перевернуть два ребра"), "R' L R L' U L' U' L", None),
]

PYRA_L4E = [
    ("Sune", "R U R' U R U R'"), ("AntiSune", "R U' R' U' R U' R'"),
    ("Lefty Bars", "R' U' L' U L R"), ("Righty Bars", "L U R U' R' L'"),
    ("Sledge", "R' L R L'"), ("Hedge", "L R' L' R"),
    ("Clockwise", "L R' L' R' U' R'"), ("Counterclockwise", "R' L R L U L"),
    ("Righty", "R U' R'"), ("Lefty", "L' U L"),
    ("Sexy", "U' R U R'"), ("Left Sexy", "U L' U' L"),
    ("2 Flip", "R' L R L' U L' U' L"), ("DR Flip", "L' U L U' R U' R'"),
    ("DL Flip", "R' L R L' R U' R'"), ("DB Flip", "R U R' U L' U' L"),
    ("4 Flip", "L' U L R U' R' L' U L R U' R'"),
    ("Right Polish Flip", "R U' R' L' U' L"), ("Left Polish Flip", "L' U L R U R'"),
    ("SUS", "R' L R L' U' R' L R L'"), ("Anti SUS", "L R' L' R U L R' L' R"),
    ("Good Niky", "R U' R' L' U L"), ("Good Sochi", "L' U L R U' R'"),
    ("Super Sledge", "R U' R L R L'"), ("Super Hedge", "L' U L' R' L' R"),
    ("Bad Niky", "R U' R' U' L' U L"), ("Bad Sochi", "L' U L U R U' R'"),
    ("Right Spam", "R U R' U R' L R L'"), ("Left Spam", "L' U' L U' L R' L' R"),
    ("Bad Sledge", "L R' L' R U' R U' R'"), ("Bad Hedge", "R' L R L' U L' U L"),
    ("Bad Sexy", "L' U' L U' R U' R'"), ("Bad Ugly", "R U R' U L' U L"),
    ("Bad Righty", "L' U L U' R U R'"), ("Bad Lefty", "R U' R' U L' U' L"),
    ("Double Sexy", "U' R U' R' U R U R'"), ("Double Ugly", "L' U L U L' U' L"),
]
# speedcubedb writes R2' / L2' (= one clockwise turn on a 3-sided axis); they
# are written here as plain R / L so the notation stays WCA-legal.

# ---------------------------------------------------------------------------
# Skewb layer method (computed, WCA notation: R=DBR, U=UBL, L=DFL, B=DBL)
# ---------------------------------------------------------------------------

SKEWB_CORNERS = [
    ("Corners A", "B' L' U B R' L' R'"),
    ("Corners B", "U R L' U' R L R"),
]

SKEWB_CENTRES = [
    ("3 centres · 1", "L' R' U B L' B' L R"),
    ("3 centres · 2", "R L' B L B' U' R L R"),
    ("3 centres · 3", "R U B' U' B L R' U'"),
    ("3 centres · 4", "R U R' U' L B R' B'"),
    ("3 centres · 5", "R' L R' L' B L B' U' R'"),
    ("4 centres · 1", "R B R U' L' B' L' U"),
    ("4 centres · 2", "R L R L B R' B' L' R"),
    ("4 centres · 3", "R L' B R' U' B U' B"),
    ("4 centres · 4", "R L' B' R' L' B L U"),
    ("4 centres · 5", "R U L' R L' U' R L'"),
    ("5 centres · 1", "R B' U' R' B R' B L R B'"),
    ("5 centres · 2", "R L R' B L U' R' U L' B'"),
    ("5 centres · 3", "R L' B L R U' R L' B' L'"),
    ("5 centres · 4", "R L' B R' U' L' R B' L U"),
    ("5 centres · 5", "R L' R' B L U' R U L' B'"),
    ("5 centres · 6", "R U B R' B R' L' B' R B'"),
]

# ---------------------------------------------------------------------------
# Megaminx (4-look last layer; no picture, the algorithms use R/U/F like 3x3)
# ---------------------------------------------------------------------------

MINX_EO = [("EO 1", "F R U R' U' F'"), ("EO 2", "F U R U' R' F'"),
           ("EO 3", "F R U2 R2' F R F' U2' F'")]
MINX_CO = [
    ("CO 1", "R U R' U R U R' U2' R U' R'"), ("CO 2", "F R U2 R' U' R U' R' F'"),
    ("CO 3", "R U2 R' U R U2 R'"), ("CO 4", "R U R' U' R' F R U R U' R' F'"),
    ("CO 5", "R U R' U R U2' R'"), ("CO 6", "R' U' R U' R' U2 R"),
    ("CO 7", "R U2 R' U' R U' R'"), ("CO 8", "R U R' U2 R U2 R'"),
    ("CO 9", "R U2 R' U' R U R' U' R U' R'"), ("CO 10", "R U R' U R U' R' U R U2' R'"),
    ("CO 11", "R U R' U R U R' U' R U2' R'"), ("CO 12", "R U2 R' U' R U' R2' U' R U' R' U2 R"),
    ("CO 13", "R U2 R2' U' R2 U' R2' U2 R"), ("CO 14", "R' U2' R2 U R2' U R2 U2' R'"),
    ("CO 15", "R U R' U2 R U2' R' U R U2' R'"), ("CO 16", "R U2 R' U' R U2 R' U2' R U' R'"),
]
MINX_EP = [
    ("EP 1", "R2 U2' R2' U' R2 U2' R2'"), ("EP 2", "R2 U2 R2' U R2 U2 R2'"),
    ("EP 3", "R U R' F' R U R' U' R' F R2 U' R'"),
    ("EP 4", "R U R' U R' U' R2 U' R' U R' U R U2'"),
    ("EP 5", "L R U2 L' U R' L U' R U2 L' U2 R'"),
]
MINX_CP = [
    ("CP 1", "R' BR' R BR R' F' R BR' R' BR F R"), ("CP 2", "R' F' BR' R BR R' F R BR' R' BR R"),
    ("CP 3", "BR' R' U L U' R' U L' U' R2 BR"), ("CP 4", "BR' R2' U L U' R U L' U' R BR"),
    ("CP 5", "L' R U2 R' U' R U R' U' R U R' U' R U' R' L"),
    ("CP 6", "R U R' U R' U' R F' R U R' U' R' F R2 U' R2' U R U'"),
    ("CP 7", "R2 U R' U' y R U R' U' R U R' U' R U R' y' R U' R2'"),
    ("CP 8", "F R U2 R' U' R U' R' F' R' y' R' U' R U' R' U2 R BR U'"),
    ("CP 9", "R U R' U R' U' R2 U' R' U R' U R U R U R' U R' U' R2 U' R' U R' U R U"),
    ("CP 10", "R2 U2 R2' U' R2 U' R2' y' R2' U' R2 U' R2' U2 R2"),
    ("CP 11", "R2' U2' R2 U R2' U R2 y R2 U R2' U R2 U2' R2'"),
    ("CP 12", "R2 U2' R2' U' R2 U2' R' U R' U' R' F R2 U' R' U' R U R' F'"),
    ("CP 13", "R' U2 R U' R' U2 R U2' R' U' R U2' R' U R U2' R' U R"),
    ("CP 14", "R2 U2' R2' U' R2 U R2' U' R2 U R2' U' R2 U2' R2'"),
    ("CP 15", "R2 U2 R2' U R2 U' R2' U R2 U' R2' U R2 U2 R2'"),
]

# ---------------------------------------------------------------------------
# Square-1 beginner (ruwix.com)
# ---------------------------------------------------------------------------

SQ1_BEGINNER = [
    ("sq1-middle", ("Fix the middle layer", "Выровнять средний слой"),
     "(0,-1) / (6,0) / (6,0) / (0,1)",
     ("Cube shape reached but the middle is not square.",
      "Форма куба есть, но средний слой не квадратный.")),
    ("sq1-cswap", ("Corner between layers", "Угол между слоями"), "(0,-4) / (0,3) / (0,1)",
     ("Swaps a corner between the top and bottom layers.",
      "Меняет угол между верхним и нижним слоем.")),
    ("sq1-ctop", ("Place top corners", "Расставить верхние углы"),
     "(1,0) / (0,-3) / (0,3) / (0,-3) / (0,-3) / (0,6) / (-1,0)", None),
    ("sq1-eswap", ("Edge between layers", "Ребро между слоями"),
     "(1,0) / (0,-3) / (0,-3) / (-1,-1) / (1,4) / (0,3) / (-1,0)",
     ("Edges at top-right and bottom-right swap layers.",
      "Рёбра справа сверху и справа снизу меняются слоями.")),
    ("sq1-cbottom", ("Swap bottom corners", "Обмен нижних углов"),
     "/ (3,-3) / (0,3) / (-3,0) / (3,0) / (-3,0) /",
     ("Swaps the two front bottom corners.", "Меняет два передних нижних угла.")),
    ("sq1-edges", ("Permute edges", "Расставить рёбра"), "(0,2) / (0,-3) / (1,1) / (-1,2) / (0,-2)",
     ("Swaps two top edges and two bottom edges.",
      "Меняет два верхних и два нижних ребра.")),
    ("sq1-parity", ("Parity", "Паритет"),
     "/ (3,3) / (1,0) / (-2,-2) / (2,0) / (2,2) / (-1,0) / (-3,-3) / (-2,0) / (3,3) / (3,0) "
     "/ (-1,-1) / (-3,0) / (1,1) / (-4,-3)",
     ("Only two edges are left unsolved: swaps two top edges.",
      "Остались два несобранных ребра: меняет два верхних ребра.")),
]

# ---------------------------------------------------------------------------
# 3x3 blindfolded (Old Pochmann)
# ---------------------------------------------------------------------------

BLD_OP = [
    ("bld-t", ("Edges: T perm", "Рёбра: T-перестановка"), "R U R' U' R' F R2 U' R' U' R U R' F'",
     ("Swaps the buffer edge UR with UL (and two corners, fixed later).",
      "Меняет буферное ребро UR с UL (и два угла — это исправится позже).")),
    ("bld-ja", ("Edges: Ja perm", "Рёбра: Ja"), "x R2 F R F' R U2 r' U r U2 x'",
     ("Swaps the buffer edge UR with UB (and the same two corners as T).",
      "Меняет буферное ребро UR с UB (и те же два угла, что и T).")),
    ("bld-jb", ("Edges: Jb perm", "Рёбра: Jb"), "R U R' F' R U R' U' R' F R2 U' R' U'",
     ("Swaps the buffer edge UR with UF (and the same two corners as T).",
      "Меняет буферное ребро UR с UF (и те же два угла, что и T).")),
    ("bld-y", ("Corners: modified Y perm", "Углы: модифицированная Y"),
     "R U' R' U' R U R' F' R U R' U' R' F R",
     ("Swaps the buffer corner ULB with the corner at RDF (and the UL/UB edges).",
      "Меняет буферный угол ULB с углом на месте RDF (и рёбра UL/UB).")),
]


# ---------------------------------------------------------------------------
# 3x3 Roux: CMLL (speedcubedb.com, main algorithm of each case)
# ---------------------------------------------------------------------------

CMLL = [
    ("O Adjacent", "R U R' F' R U R' U' R' F R2 U' R'"),
    ("O Diagonal", "F R U' R' U' R U R' F' R U R' U' R' F R F'"),
    ("H Columns", "U R U R' U R U' R' U R U2 R'"),
    ("H Rows", "F R U R' U' R U R' U' R U R' U' F'"),
    ("H Column", "R' F2 D R2 U R2 D' F2 R"),
    ("H Row", "U2 r U' r2 D' r U' r' D r2 U r'"),
    ("Pi Right Bar", "F R U R' U' R U R' U' F'"),
    ("Pi Down Slash", "U F R' F' R U2 R U' R' U R U2 R'"),
    ("Pi X", "R' F2 D R2 U' R2 D' F2 R"),
    ("Pi Up Slash", "R U2 R' U' R U R' U2 R' F R F'"),
    ("Pi Columns", "U' r U' r2 D' r U r' D r2 U r'"),
    ("Pi Left Bar", "U' R' U' R' F R F' R U' R' U2 R"),
    ("U Up Slash", "U2 R2 D R' U2 R D' R' U2 R'"),
    ("U Down Slash", "R2 D' R U2 R' D R U2 R"),
    ("U Bottom Row", "R' U' R U' R' U2 R2 U R' U R U2 R'"),
    ("U Rows", "U' F R2 D R' U R D' R2 U' F'"),
    ("U X", "U2 r U' r' U r' D' r U' r' D r"),
    ("U Upper Row", "U' F R U R' U' F'"),
    ("T Left Bar", "U' R U R' U' R' F R F'"),
    ("T Right Bar", "U L' U' L U L F' L' F"),
    ("T Rows", "R U2 R' U' R U' R2 U2 R U R' U R"),
    ("T Bottom Row", "r' U r U2 R2 F R F' R"),
    ("T Top Row", "r' D' r U r' D r U' r U r'"),
    ("T Columns", "U2 r U' r2 D' r U2 r' D r2 U r'"),
    ("Sune Left Bar", "U R U R' U R U2 R'"),
    ("Sune X", "U L' U2 L U2 r U' r' F"),
    ("Sune Up Slash", "U F R' F' R U2 R U2 R'"),
    ("Sune Columns", "U R U R' U' R' F R F' R U R' U R U2 R'"),
    ("Sune Right Bar", "U' R U R' U R' F R F' R U2 R'"),
    ("Sune Down Slash", "U r U' r' F R' F' R"),
    ("Anti Sune Right Bar", "U R' U' R U' R' U2 R"),
    ("Anti Sune Columns", "U2 R U R2 F' r F R U' r2 F r"),
    ("Anti Sune Down Slash", "U' F' L F L' U2 L' U2 L"),
    ("Anti Sune X", "U' R U2 R' U2 R' F R F'"),
    ("Anti Sune Up Slash", "U' R' F R F' r U r'"),
    ("Anti Sune Left Bar", "U R U2 R' F R' F' R U' R U' R'"),
    ("L Best", "U' F' r U r' U' r' F r"),
    ("L Good", "U2 F R' F' R U R U' R'"),
    ("L Pure", "R U R' U R U' R' U R U' R' U R U2 R'"),
    ("L Front Commutator", "U2 R U2 R D R' U2 R D' R2"),
    ("L Diagonal", "U2 R U2 R2 F R F' R U2 R'"),
    ("L Back Commutator", "U R' U2 R' D' R U2 R' D R2"),
]
