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

class Level(object):
    def __init__(self, lid, name, subtitle, set_id=None, lesson=None):
        self.id = lid
        self.name = name            # (en, ru)
        self.subtitle = subtitle    # (en, ru)
        self.set_id = set_id
        self.lesson = lesson        # lesson id or None

    @property
    def cases(self):
        return SET_BY_ID[self.set_id].cases if self.set_id else []


LEVELS = [
    Level("notation", ("Notation", "Нотация"),
          ("How to read algorithms", "Как читать алгоритмы"), lesson="notation"),
    Level("beginner", ("Beginner method", "Метод для начинающих"),
          ("Solve the cube for the first time", "Собери куб в первый раз"),
          set_id="beginner", lesson="beginner"),
    Level("oll2", ("2-look OLL", "OLL в 2 этапа"),
          ("10 algorithms for a yellow top", "10 алгоритмов для жёлтого верха"),
          set_id="oll2", lesson="cfop"),
    Level("pll2", ("2-look PLL", "PLL в 2 этапа"),
          ("6 algorithms to finish the cube", "6 алгоритмов, чтобы закончить куб"),
          set_id="pll2"),
    Level("f2l", ("F2L", "F2L"),
          ("41 cases, two layers at once", "41 случай: два слоя сразу"),
          set_id="f2l", lesson="f2l"),
    Level("oll", ("Full OLL", "Полный OLL"),
          ("57 cases, last layer orientation in one look",
           "57 случаев: ориентация за один взгляд"), set_id="oll"),
    Level("pll", ("Full PLL", "Полный PLL"),
          ("21 cases, last layer in one look", "21 случай: последний слой за один взгляд"),
          set_id="pll"),
]
LEVEL_BY_ID = dict((lv.id, lv) for lv in LEVELS)


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

    def next_level(self):
        for lv in LEVELS:
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
