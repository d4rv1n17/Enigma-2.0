# -*- coding: utf-8 -*-
"""Achievements: computed from the solves and the training progress.

Each achievement has a badge text (short, drawn inside a circle), a name, a
description and a function returning (value, target). It is unlocked when
value >= target; unlocked ones are stored with their date in
store.training["ach"] so they stay unlocked.
"""

import datetime
import time

from .algs import SET_BY_ID
from .learn import LEARNED, Progress
from .scramble import PUZZLE_IDS
from .stats import DNF, INF, average

SOLVING, TRAINING = "solving", "training"


class Ctx(object):
    """Facts about the user, computed once per check."""

    def __init__(self, store):
        self.store = store
        self.progress = Progress(store.training)
        self.solves = []                    # (puzzle, solve)
        self.events = set()
        self.max_session = 0
        best = {}
        for sess in store.sessions:
            self.max_session = max(self.max_session, len(sess.solves))
            for s in sess.solves:
                self.solves.append((sess.puzzle, s))
                if s.penalty != DNF:
                    self.events.add(sess.puzzle)
        for puzzle, s in self.solves:
            v = s.value
            if v != INF and v < best.get(puzzle, INF):
                best[puzzle] = v
        self.best = best
        self.best_avg = {}
        for sess in store.sessions:
            if sess.puzzle != "333":
                continue
            vals = [s.value for s in sess.solves]
            for k in (5, 12):
                for i in range(k, len(vals) + 1):
                    a = average(vals[i - k:i])
                    key = (sess.puzzle, k)
                    if a is not None and a != INF and a < self.best_avg.get(key, INF):
                        self.best_avg[key] = a
        days = set(store.training.get("days", []))
        for _, s in self.solves:
            days.add(time.strftime("%Y-%m-%d", time.localtime(s.date)))
        self.days = days
        per_day = {}
        for _, s in self.solves:
            d = time.strftime("%Y-%m-%d", time.localtime(s.date))
            per_day[d] = per_day.get(d, 0) + 1
        self.max_per_day = max(per_day.values()) if per_day else 0
        self.reviews = sum(r.get("seen", 0) for r in store.training.get("cases", {}).values())
        self.flags = store.training.setdefault("flags", {})

    def streak(self):
        best = run = 0
        prev = None
        for d in sorted(self.days):
            day = datetime.date(*[int(x) for x in d.split("-")])
            run = run + 1 if prev and (day - prev).days == 1 else 1
            best = max(best, run)
            prev = day
        return best

    def learned(self, set_ids):
        cases = {}
        for sid in set_ids:
            for c in SET_BY_ID[sid].cases:
                cases[c.id] = c
        done = sum(1 for cid in cases if self.progress.status(cid) == LEARNED)
        return done, len(cases)


def _sub(puzzle, seconds):
    def f(ctx):
        b = ctx.best.get(puzzle, INF)
        return (1 if b < seconds * 1000 else 0), 1
    return f


def _avg(puzzle, k, seconds):
    def f(ctx):
        b = ctx.best_avg.get((puzzle, k), INF)
        return (1 if b < seconds * 1000 else 0), 1
    return f


def _count(n):
    return lambda ctx: (min(len(ctx.solves), n), n)


def _sets(*ids):
    return lambda ctx: ctx.learned(ids)


def _lesson(lid):
    return lambda ctx: (1 if ctx.progress.lesson_done(lid) else 0), 1


def _flag(name):
    return lambda ctx: (1 if ctx.flags.get(name) else 0), 1


A = []


def _a(aid, cat, badge, name, desc, fn):
    A.append({"id": aid, "cat": cat, "badge": badge, "name": name, "desc": desc, "fn": fn})


# --- solving -----------------------------------------------------------------
_a("first", SOLVING, "1", ("First solve", "Первая сборка"),
   ("Time your first solve.", "Засеки первую сборку."), _count(1))
_a("s100", SOLVING, "100", ("Hundred", "Сотня"), ("100 solves.", "100 сборок."), _count(100))
_a("s1000", SOLVING, "1K", ("Thousand", "Тысяча"), ("1000 solves.", "1000 сборок."), _count(1000))
_a("s10000", SOLVING, "10K", ("Ten thousand", "Десять тысяч"), ("10 000 solves.", "10 000 сборок."),
   _count(10000))
for sec in (60, 30, 20, 15, 10):
    _a("sub%d" % sec, SOLVING, str(sec), ("Sub-%d" % sec, "Быстрее %d" % sec),
       ("3x3 single under %d seconds." % sec, "Сингл 3x3 быстрее %d секунд." % sec),
       _sub("333", sec))
_a("ao5sub30", SOLVING, "ao5", ("Consistent", "Стабильность"),
   ("3x3 average of 5 under 30 seconds.", "Среднее из 5 на 3x3 быстрее 30 секунд."),
   _avg("333", 5, 30))
_a("ao12sub20", SOLVING, "ao12", ("Speedcuber", "Спидкубер"),
   ("3x3 average of 12 under 20 seconds.", "Среднее из 12 на 3x3 быстрее 20 секунд."),
   _avg("333", 12, 20))
_a("ao100", SOLVING, "100×", ("Marathon session", "Марафон"),
   ("100 solves in one session.", "100 сборок в одной сессии."),
   lambda ctx: (min(ctx.max_session, 100), 100))
_a("day50", SOLVING, "50/d", ("Practice day", "День тренировки"),
   ("50 solves in one day.", "50 сборок за один день."),
   lambda ctx: (min(ctx.max_per_day, 50), 50))
_a("events5", SOLVING, "5ev", ("Explorer", "Исследователь"),
   ("Solve 5 different events.", "Собери 5 разных дисциплин."),
   lambda ctx: (min(len(ctx.events), 5), 5))
_a("eventsall", SOLVING, "14", ("All-rounder", "Универсал"),
   ("Solve all 14 events.", "Собери все 14 дисциплин."),
   lambda ctx: (len(ctx.events & set(PUZZLE_IDS)), len(PUZZLE_IDS)))
_a("big", SOLVING, "7×7", ("Big cube", "Большой куб"), ("Solve a 7x7.", "Собери 7x7."),
   lambda ctx: (1 if "777" in ctx.events else 0, 1))
_a("bld", SOLVING, "BLD", ("Blindfolded", "Вслепую"),
   ("A successful 3x3 blindfolded solve.", "Успешная сборка 3x3 вслепую."),
   lambda ctx: (1 if "333bf" in ctx.events else 0, 1))
for n in (3, 7, 30):
    _a("streak%d" % n, SOLVING, "%dd" % n, ("%d-day streak" % n, "%d дней подряд" % n),
       ("Practise %d days in a row." % n, "Тренируйся %d дней подряд." % n),
       (lambda k: lambda ctx: (min(ctx.streak(), k), k))(n))

# --- training ----------------------------------------------------------------
_a("notation", TRAINING, "R'", ("Fluent", "Знаю нотацию"),
   ("Finish the notation lesson.", "Пройди урок нотации."), _lesson("notation"))
_a("firstalg", TRAINING, "✓", ("First algorithm", "Первый алгоритм"),
   ("Learn any algorithm.", "Выучи любой алгоритм."),
   lambda ctx: (1 if any(ctx.progress.status(c) == LEARNED
                         for c in ctx.store.training.get("cases", {})) else 0, 1))
_a("beginner", TRAINING, "LBL", ("First solve by yourself", "Сам собрал"),
   ("Learn the 3x3 beginner method.", "Выучи метод для начинающих на 3x3."), _sets("beginner"))
_a("twolook", TRAINING, "2L", ("Two looks", "Два взгляда"),
   ("Learn 2-look OLL and PLL.", "Выучи OLL и PLL в 2 этапа."), _sets("oll2", "pll2"))
_a("f2l", TRAINING, "F2L", ("F2L master", "Мастер F2L"), ("Learn all 41 F2L cases.",
                                                         "Выучи все 41 случай F2L."), _sets("f2l"))
_a("oll", TRAINING, "OLL", ("Full OLL", "Полный OLL"), ("Learn all 57 OLLs.", "Выучи все 57 OLL."),
   _sets("oll"))
_a("pll", TRAINING, "PLL", ("Full PLL", "Полный PLL"), ("Learn all 21 PLLs.", "Выучи все 21 PLL."),
   _sets("pll"))
_a("cfop", TRAINING, "CFOP", ("Fridrich master", "Мастер Фридриха"),
   ("Learn F2L, OLL and PLL.", "Выучи F2L, OLL и PLL."), _sets("f2l", "oll", "pll"))
_a("ortega", TRAINING, "ORT", ("Ortega", "Ортега"), ("Learn the Ortega method (2x2).",
                                                     "Выучи метод Ортега (2x2)."),
   _sets("222-ortega-oll", "222-ortega-pbl"))
_a("cll", TRAINING, "CLL", ("CLL", "CLL"), ("Learn all 40 CLL cases (2x2).",
                                             "Выучи все 40 случаев CLL (2x2)."), _sets("222-cll"))
_a("parity", TRAINING, "4×4", ("Parity", "Паритет"), ("Learn the 4x4 parities.",
                                                      "Выучи паритеты 4x4."), _sets("444-parity"))
_a("l4e", TRAINING, "L4E", ("Pyramid pro", "Профи Пирамидки"), ("Learn all 36 L4E cases.",
                                                                "Выучи все 36 случаев L4E."),
   _sets("pyra-l4e"))
_a("skewb", TRAINING, "SKB", ("Skewb", "Скьюб"), ("Learn the Skewb layer method.",
                                                  "Выучи послойный метод Скьюба."),
   _sets("skewb-layer"))
_a("minx", TRAINING, "MGX", ("Megaminx", "Мегаминкс"), ("Learn the megaminx last layer.",
                                                       "Выучи последний слой мегаминкса."),
   _sets("minx-ll"))
_a("sq1", TRAINING, "SQ1", ("Square-1", "Square-1"), ("Learn the Square-1 beginner method.",
                                                      "Выучи метод новичка для Square-1."),
   _sets("sq1-beginner"))
_a("op", TRAINING, "OP", ("Old Pochmann", "Old Pochmann"), ("Learn the blindfolded algorithms.",
                                                           "Выучи алгоритмы для вслепую."),
   _sets("bld-op"))
_a("r100", TRAINING, "×100", ("Diligent", "Усердие"), ("100 reviews in the trainer.",
                                                       "100 повторений в тренажёре."),
   lambda ctx: (min(ctx.reviews, 100), 100))
_a("r1000", TRAINING, "×1K", ("Muscle memory", "Мышечная память"),
   ("1000 reviews in the trainer.", "1000 повторений в тренажёре."),
   lambda ctx: (min(ctx.reviews, 1000), 1000))
_a("windows", TRAINING, "⧉", ("Multitasker", "Многозадачность"),
   ("Open Training in a separate window.", "Открой тренировку в отдельном окне."),
   _flag("training_window"))
_a("reference", TRAINING, "?", ("Curious", "Любопытство"),
   ("Open the notation reference.", "Открой справочник нотации."), _flag("reference"))

BY_ID = dict((a["id"], a) for a in A)


def check(store, now=None):
    """Evaluate all achievements; return a list of newly unlocked ones and a
    dict id -> (value, target) for progress bars."""
    ctx = Ctx(store)
    unlocked = store.training.setdefault("ach", {})
    new = []
    status = {}
    for a in A:
        try:
            value, target = a["fn"](ctx)
        except Exception:  # noqa: BLE001 - an achievement must never break the app
            value, target = 0, 1
        status[a["id"]] = (value, target)
        if value >= target and a["id"] not in unlocked:
            unlocked[a["id"]] = now or time.time()
            new.append(a)
    return new, status


def mark_day(store, when=None):
    """Remember that the user practised today (for streaks)."""
    days = store.training.setdefault("days", [])
    d = time.strftime("%Y-%m-%d", time.localtime(when or time.time()))
    if d not in days:
        days.append(d)


def set_flag(store, name):
    store.training.setdefault("flags", {})[name] = True
