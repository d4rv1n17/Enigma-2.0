# -*- coding: utf-8 -*-
"""Facts about an algorithm case, computed with the simulators.

Nothing here is typed by hand: move counts, which pieces an algorithm moves
and how a case looks are all worked out from the algorithm itself, so the
text can never disagree with the picture.
"""

from .cube import tokens

_ROTATIONS = set("xyz")


def move_count(alg):
    """Moves without whole-cube rotations (slices count as one move)."""
    return sum(1 for t in tokens(alg) if t[0] not in _ROTATIONS)


def _plural_ru(n, one, few, many):
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def _cycles(moves):
    """Cycle lengths of a {position: destination} mapping."""
    seen, out = set(), []
    for start in moves:
        if start in seen:
            continue
        n, p = 0, start
        while p not in seen and p in moves:
            seen.add(p)
            p = moves[p]
            n += 1
        out.append(n)
    return out


def _pieces_text(kind, cycles):
    """('swaps two corners', ...) for corner or edge cycles."""
    en_word = {"c": ("corner", "corners"), "e": ("edge", "edges")}[kind]
    ru_word = {"c": ("угол", "угла", "углов"), "e": ("ребро", "ребра", "рёбер")}[kind]
    parts_en, parts_ru = [], []
    swaps = sum(1 for n in cycles if n == 2)
    if swaps == 2:
        parts_en.append("swaps two pairs of %s" % en_word[1])
        parts_ru.append("меняет местами две пары %s" % ru_word[2])
    elif swaps == 1:
        parts_en.append("swaps two %s" % en_word[1])
        parts_ru.append("меняет местами два %s" % ru_word[1])
    for n in sorted(cycles, reverse=True):
        if n >= 3:
            parts_en.append("cycles %d %s" % (n, en_word[1]))
            parts_ru.append("переставляет по кругу %d %s" % (n, _plural_ru(n, *ru_word)))
    return parts_en, parts_ru


def _pll_facts(case):
    from .caseview import _PRE, _piece_moves, best_pre_auf
    state = case.state()
    pre = _PRE.get(case.id)
    if pre is None:
        pre = _PRE[case.id] = best_pre_auf(state, case.alg)
    inv = {"": "", "U": "U'", "U'": "U", "U2": "U2"}[pre]
    st = state.copy().apply(pre) if pre else state
    moves = _piece_moves(st, inv + " " + case.alg)
    corners = {k: v for k, v in moves.items() if k[0] != 1 and k[1] != 1}
    edges = {k: v for k, v in moves.items() if k not in corners}
    ce, cr = _pieces_text("c", _cycles(corners))
    ee, er = _pieces_text("e", _cycles(edges))
    en = ce + ee
    ru = cr + er
    if not corners:
        en.append("corners stay in place")
        ru.append("углы остаются на месте")
    if not edges:
        en.append("edges stay in place")
        ru.append("рёбра остаются на месте")
    return [("What it does: " + ", ".join(en) + ".",
             "Что делает: " + ", ".join(ru) + ".")]


def _oll_facts(case, edges_only=False):
    g = case.state().copy().normalize().facelets()
    e = sum(1 for r, c in [(0, 1), (1, 0), (1, 2), (2, 1)] if g["U"][r][c] == "U")
    c = sum(1 for r, cc in [(0, 0), (0, 2), (2, 0), (2, 2)] if g["U"][r][cc] == "U")
    if edges_only:
        return [("Before: %d of 4 top edges already face up." % e,
                 "До алгоритма: вверх смотрят %d из 4 рёбер." % e)]
    return [("Before: %d of 4 edges and %d of 4 corners already face up." % (e, c),
             "До алгоритма: вверх смотрят %d из 4 рёбер и %d из 4 углов." % (e, c))]


def _f2l_facts(case):
    from .fast3 import LOCS
    st = case.state().copy().normalize()
    # the white-green-red corner and green-red edge of the front-right slot
    corner_home = {("D", 0, 2), ("F", 2, 2), ("R", 2, 0)}
    edge_home = {("F", 1, 2), ("R", 1, 0)}
    corner_at, edge_at, white_up = [], [], False
    for i, (f, r, c) in enumerate(LOCS):
        home = LOCS[st.arr[i]]
        if home in corner_home:
            corner_at.append((f, r))
            if home == ("D", 0, 2) and f == "U":
                white_up = True
        if home in edge_home:
            edge_at.append((f, r))
    corner_top = any(f == "U" or r == 0 for f, r in corner_at)
    edge_top = any(f == "U" or r == 0 for f, r in edge_at)
    where_en = "Corner %s, edge %s." % ("on top" if corner_top else "in the slot",
                                        "on top" if edge_top else "in the slot")
    where_ru = "Угол %s, ребро %s." % ("сверху" if corner_top else "в слоте",
                                       "сверху" if edge_top else "в слоте")
    out = [(where_en, where_ru)]
    if corner_top:
        out.append(("White sticker of the corner faces %s." % ("up" if white_up else "sideways"),
                    "Белая наклейка угла смотрит %s." % ("вверх" if white_up else "вбок")))
    return out


def facts(case):
    """List of (en, ru) sentences describing the case."""
    out = []
    n = move_count(case.alg)
    out.append(("Length: %d moves." % n,
                "Длина: %d %s." % (n, _plural_ru(n, "ход", "хода", "ходов"))))
    try:
        if case.puzzle in ("333", "333oh", "333bf") and case.view == "pll":
            out += _pll_facts(case)
        elif case.puzzle in ("333", "333oh") and case.view == "oll":
            out += _oll_facts(case, edges_only=case.id.startswith("oll2-"))
        elif case.puzzle == "333" and case.view == "f2l" and case.set_id == "f2l":
            out += _f2l_facts(case)
    except Exception:  # noqa: BLE001 - facts are a bonus, never break the UI
        pass
    if case.alts:
        k = len(case.alts)
        out.append(("%d more option%s below." % (k, "s" if k > 1 else ""),
                    "Ниже ещё %d %s." % (k, _plural_ru(k, "вариант", "варианта", "вариантов"))))
    return out
