# -*- coding: utf-8 -*-
"""Learning path, lessons and spaced-repetition progress for the Training section.

Every case has a Leitner "box" (0..5). Rating a case in the trainer moves it
between boxes and schedules the next review:

    box:       0      1      2      3      4       5
    review:    now    1 day  3 days 7 days 16 days 35 days

A case counts as *learned* from box 3. New cases are introduced in order,
a few at a time, so the learner is never flooded.
"""

import random
import time

from .algs import CASES, SET_BY_ID

DAY = 86400.0
INTERVALS = [0, 1 * DAY, 3 * DAY, 7 * DAY, 16 * DAY, 35 * DAY]
LEARNED_BOX = 3
MAX_BOX = len(INTERVALS) - 1

NEW, LEARNING, LEARNED = 0, 1, 2

AGAIN, HARD, GOOD = 0, 1, 2


# ---------------------------------------------------------------------------
# Learning path
# ---------------------------------------------------------------------------

BEGINNER, INTERMEDIATE, ADVANCED = "beginner", "intermediate", "advanced"
TIER_NAMES = {
    BEGINNER: ("Beginner", "Новичок"),
    INTERMEDIATE: ("Intermediate", "Продвинутый"),
    ADVANCED: ("Pro", "Профи"),
}


class Level(object):
    def __init__(self, lid, name, subtitle, set_id=None, lesson=None, tier=BEGINNER):
        self.id = lid
        self.name = name            # (en, ru)
        self.subtitle = subtitle    # (en, ru)
        self.set_id = set_id
        self.lesson = lesson        # lesson id or None
        self.tier = tier

    @property
    def cases(self):
        return SET_BY_ID[self.set_id].cases if self.set_id else []


def _lv(*args, **kw):
    lv = Level(*args, **kw)
    LEVEL_BY_ID[lv.id] = lv
    return lv


LEVEL_BY_ID = {}

L333 = [
    _lv("notation", ("Notation", "Нотация"),
        ("How to read algorithms", "Как читать алгоритмы"), lesson="notation"),
    _lv("beginner", ("Beginner method", "Метод для начинающих"),
        ("Solve the cube for the first time", "Собери куб в первый раз"),
        set_id="beginner", lesson="beginner"),
    _lv("oll2", ("2-look OLL", "OLL в 2 этапа"),
        ("10 algorithms for a yellow top", "10 алгоритмов для жёлтого верха"),
        set_id="oll2", lesson="cfop", tier=INTERMEDIATE),
    _lv("pll2", ("2-look PLL", "PLL в 2 этапа"),
        ("6 algorithms to finish the cube", "6 алгоритмов, чтобы закончить куб"),
        set_id="pll2", tier=INTERMEDIATE),
    _lv("f2l", ("F2L", "F2L"),
        ("41 cases, two layers at once", "41 случай: два слоя сразу"),
        set_id="f2l", lesson="f2l", tier=INTERMEDIATE),
    _lv("oll", ("Full OLL", "Полный OLL"),
        ("57 cases, last layer orientation in one look",
         "57 случаев: ориентация за один взгляд"), set_id="oll", tier=ADVANCED),
    _lv("pll", ("Full PLL", "Полный PLL"),
        ("21 cases, last layer in one look", "21 случай: последний слой за один взгляд"),
        set_id="pll", tier=ADVANCED),
    _lv("roux-cmll", ("Roux: CMLL", "Roux: CMLL"),
        ("Another top method: blocks, CMLL, LSE", "Другой топ-метод: блоки, CMLL, LSE"),
        set_id="333-cmll", lesson="roux", tier=ADVANCED),
]
L222 = [
    _lv("222-notation", ("Notation", "Нотация"), ("Same as the 3x3", "Как на 3x3"),
        lesson="ref:222"),
    _lv("222-beginner", ("Beginner method", "Метод для начинающих"),
        ("Layer by layer, 4 algorithms", "Послойно, 4 алгоритма"),
        set_id="222-beginner", lesson="222-beginner"),
    _lv("222-ortega-oll", ("Ortega: OLL", "Ортега: OLL"), ("7 algorithms", "7 алгоритмов"),
        set_id="222-ortega-oll", lesson="222-ortega", tier=INTERMEDIATE),
    _lv("222-ortega-pbl", ("Ortega: PBL", "Ортега: PBL"), ("6 algorithms", "6 алгоритмов"),
        set_id="222-ortega-pbl", tier=INTERMEDIATE),
    _lv("222-cll", ("CLL", "CLL"), ("40 cases, last layer in one look",
                                     "40 случаев: последний слой за один взгляд"),
        set_id="222-cll", tier=ADVANCED),
]
LBIG = [
    _lv("big-notation", ("Notation", "Нотация"), ("Wide moves and slices", "Широкие ходы и слайсы"),
        lesson="ref:444"),
    _lv("444-reduction", ("Reduction method", "Метод редукции"),
        ("Centres, edges, then 3x3", "Центры, рёбра, затем 3x3"), lesson="444-reduction"),
    _lv("444-parity", ("4x4 parity", "Паритеты 4x4"), ("3 algorithms", "3 алгоритма"),
        set_id="444-parity", tier=INTERMEDIATE),
    _lv("555-edges", ("5x5 and bigger", "5x5 и больше"),
        ("Edge pairing", "Сборка рёбер"), set_id="555-edges", lesson="555-edges",
        tier=INTERMEDIATE),
]
LPYRA = [
    _lv("pyra-notation", ("Notation", "Нотация"), ("Corners and tips", "Вершины и кончики"),
        lesson="ref:pyram"),
    _lv("pyra-beginner", ("Beginner method", "Метод для начинающих"),
        ("Tips, centres, edges", "Вершинки, центры, рёбра"),
        set_id="pyra-beginner", lesson="pyra-beginner"),
    _lv("pyra-l4e", ("L4E", "L4E"), ("36 cases", "36 случаев"), set_id="pyra-l4e",
        lesson="pyra-l4e", tier=ADVANCED),
]
LSKEWB = [
    _lv("skewb-notation", ("Notation", "Нотация"), ("WCA corner moves", "Ходы углами по WCA"),
        lesson="ref:skewb"),
    _lv("skewb-layer", ("Layer method", "Послойный метод"),
        ("2 corner + 16 centre cases", "2 случая углов + 16 центров"),
        set_id="skewb-layer", lesson="skewb-layer", tier=INTERMEDIATE),
]
LMINX = [
    _lv("minx-notation", ("Notation", "Нотация"), ("Faces and Pochmann scrambles",
                                                   "Грани и скрамблы Похмана"), lesson="ref:minx"),
    _lv("minx-beginner", ("Beginner method", "Метод для начинающих"),
        ("Like a 3x3, layer by layer", "Как 3x3, послойно"), lesson="minx-beginner"),
    _lv("minx-ll", ("4-look last layer", "Последний слой в 4 этапа"), ("39 algorithms", "39 алгоритмов"),
        set_id="minx-ll", tier=INTERMEDIATE),
]
LSQ1 = [
    _lv("sq1-notation", ("Notation", "Нотация"), ("(x, y) and the slice", "(x, y) и слайс"),
        lesson="ref:sq1"),
    _lv("sq1-beginner", ("Beginner method", "Метод для начинающих"),
        ("7 algorithms", "7 алгоритмов"), set_id="sq1-beginner", lesson="sq1-beginner"),
]
LCLOCK = [
    _lv("clock-notation", ("Notation", "Нотация"), ("Pins and dials", "Штырьки и колёса"),
        lesson="ref:clock"),
    _lv("clock-beginner", ("Beginner method", "Метод для начинающих"),
        ("Cross, back, corners", "Крест, обратная сторона, углы"), lesson="clock-beginner"),
]
LBLD = [L333[0], _lv("bld-op", ("Old Pochmann", "Old Pochmann"),
                     ("Blindfolded, one piece at a time", "Вслепую, по одной детали"),
                     set_id="bld-op", lesson="bld-op", tier=INTERMEDIATE)]
LOH = [_lv("oh", ("One-handed tips", "Советы для одной руки"), ("Grips and algorithms",
                                                                 "Хваты и алгоритмы"),
           lesson="oh"), L333[2], L333[3], L333[4]]
LFMC = [L333[0], _lv("fmc", ("FMC basics", "Основы FMC"), ("Blocks, skeletons, NISS",
                                                            "Блоки, скелеты, NISS"), lesson="fmc")]

PATHS = {
    "333": L333, "222": L222, "444": LBIG, "555": LBIG, "666": LBIG, "777": LBIG,
    "pyram": LPYRA, "skewb": LSKEWB, "minx": LMINX, "sq1": LSQ1, "clock": LCLOCK,
    "333bf": LBLD, "333oh": LOH, "333fm": LFMC,
}
# order of the puzzles in the Training selector
PATH_ORDER = ["333", "222", "444", "pyram", "skewb", "minx", "sq1", "clock",
              "333bf", "333oh", "333fm"]
PATH_NAMES = {
    "333": ("3x3 · Fridrich (CFOP)", "3x3 · Фридрих (CFOP)"),
    "222": ("2x2 · Ortega, CLL", "2x2 · Ортега, CLL"),
    "444": ("4x4–7x7 · Reduction", "4x4–7x7 · Редукция"),
    "pyram": ("Pyraminx", "Пирамидка"),
    "skewb": ("Skewb", "Скьюб"),
    "minx": ("Megaminx", "Мегаминкс"),
    "sq1": ("Square-1", "Square-1"),
    "clock": ("Clock", "Clock"),
    "333bf": ("3x3 blindfolded", "3x3 вслепую"),
    "333oh": ("3x3 one-handed", "3x3 одной рукой"),
    "333fm": ("3x3 fewest moves", "3x3 FMC"),
}
LEVELS = L333   # kept for older code


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------

class Progress(object):
    """Wraps the `training` dict stored in data.json."""

    def __init__(self, data):
        self.data = data
        data.setdefault("cases", {})
        data.setdefault("lessons", {})

    # --- per case ------------------------------------------------------
    def _rec(self, cid):
        return self.data["cases"].get(cid)

    def box(self, cid):
        r = self._rec(cid)
        return r["box"] if r else -1

    def status(self, cid):
        r = self._rec(cid)
        if not r:
            return NEW
        return LEARNED if r["box"] >= LEARNED_BOX else LEARNING

    def set_status(self, cid, status, now=None):
        now = now or time.time()
        if status == NEW:
            self.data["cases"].pop(cid, None)
            return
        r = self.data["cases"].setdefault(cid, {"box": 0, "due": now, "seen": 0, "ok": 0})
        if status == LEARNED:
            r["box"] = max(r["box"], LEARNED_BOX)
            r["due"] = now + INTERVALS[r["box"]]
        else:
            r["box"] = min(r["box"], LEARNED_BOX - 1)
            r["due"] = now

    def rate(self, cid, rating, now=None):
        now = now or time.time()
        r = self.data["cases"].setdefault(cid, {"box": 0, "due": now, "seen": 0, "ok": 0})
        r["seen"] += 1
        if rating == AGAIN:
            r["box"] = 0
            r["due"] = now
        elif rating == HARD:
            r["box"] = max(1, r["box"])
            r["due"] = now + INTERVALS[r["box"]] / 2.0
            r["ok"] += 1
        else:
            r["box"] = min(MAX_BOX, r["box"] + 1)
            r["due"] = now + INTERVALS[r["box"]]
            r["ok"] += 1

    def is_due(self, cid, now=None):
        r = self._rec(cid)
        return bool(r) and r["due"] <= (now or time.time())

    # --- lessons -------------------------------------------------------
    def lesson_done(self, lid):
        return bool(self.data["lessons"].get(lid))

    def set_lesson_done(self, lid, done=True):
        self.data["lessons"][lid] = bool(done)

    # --- levels --------------------------------------------------------
    def level_counts(self, level):
        """(learned, total) for a level; a lesson-only level counts as 1 item."""
        if not level.set_id:
            return (1 if self.lesson_done(level.lesson) else 0), 1
        cases = level.cases
        return sum(1 for c in cases if self.status(c.id) == LEARNED), len(cases)

    def level_done(self, level):
        a, b = self.level_counts(level)
        return a >= b

    def next_level(self, path="333"):
        for lv in PATHS.get(path, L333):
            if not self.level_done(lv):
                return lv
        return None

    def due_count(self, cases, now=None):
        now = now or time.time()
        return sum(1 for c in cases if self.is_due(c.id, now))


class Trainer(object):
    """Chooses the next case to practise from a list of cases."""

    NEW_PER_SESSION = 4

    def __init__(self, progress, cases, include_learned=True):
        self.progress = progress
        self.cases = list(cases)
        self.include_learned = include_learned
        self.last = None
        self.new_introduced = 0
        self.reviewed = 0

    def next_case(self, now=None):
        now = now or time.time()
        p = self.progress
        pool = [c for c in self.cases if c.id != self.last] or self.cases
        due = [c for c in pool if p.status(c.id) == LEARNING and p.is_due(c.id, now)]
        if due:
            due.sort(key=lambda c: p.data["cases"][c.id]["due"])
            choice = due[0]
        else:
            fresh = [c for c in pool if p.status(c.id) == NEW]
            if fresh and self.new_introduced < self.NEW_PER_SESSION:
                choice = fresh[0]
                self.new_introduced += 1
            else:
                learning = [c for c in pool if p.status(c.id) == LEARNING]
                if learning:
                    choice = min(learning, key=lambda c: (p.box(c.id), random.random()))
                elif fresh:
                    choice = fresh[0]
                else:
                    choice = min(pool, key=lambda c: (p.box(c.id), random.random()))
        self.last = choice.id
        return choice

    def rate(self, case, rating, now=None):
        self.progress.rate(case.id, rating, now)
        self.reviewed += 1


def random_auf():
    return random.choice(["", "U", "U2", "U'"])


def all_case_ids():
    return list(CASES.keys())
