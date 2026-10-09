"""Checks every algorithm in the Training database with the cube simulator."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from enigma_timer import algs, caseview, learn  # noqa: E402
from enigma_timer.cube import Cube, invert  # noqa: E402
from enigma_timer.fast3 import State, net_rotation  # noqa: E402

AUF = ["", "U", "U2", "U'"]
Y = [("", ""), ("y", "y'"), ("y2", "y2"), ("y'", "y")]


def f2l_solved(st):
    g = st.facelets()
    if any(x != "D" for row in g["D"] for x in row):
        return False
    return all(x == f for f in "FRBL" for x in g[f][1] + g[f][2])


def others_solved(st):
    """Cross and the three slots other than front-right are solved."""
    g = st.facelets()
    for r, c in [(0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (2, 0), (2, 2)]:
        if g["D"][r][c] != "D":
            return False
    for f in "FRBL":
        if g[f][2][1] != f or g[f][1][1] != f:
            return False
    cells = [("F", [(1, 0), (2, 0)]), ("L", [(1, 0), (2, 0), (1, 2), (2, 2)]),
             ("B", [(1, 0), (2, 0), (1, 2), (2, 2)]), ("R", [(1, 2), (2, 2)])]
    return all(g[f][r][c] == f for f, rc in cells for r, c in rc)


def oll_mask(st):
    g = st.facelets()
    stickers = sum(g["U"], []) + g["F"][0] + g["R"][0] + g["B"][0] + g["L"][0]
    return tuple(x == "U" for x in stickers)


def family(alg, key, post=True, conj=True):
    base = net_rotation(alg) + " " + invert(alg)
    out = set()
    for a in AUF:
        for b in (AUF if post else [""]):
            for yc, yi in (Y if conj else [("", "")]):
                st = State().apply(" ".join([yc, a, base, b, yi])).normalize()
                out.add(key(st))
    return out


class FastSimTest(unittest.TestCase):
    def test_matches_slow_simulator(self):
        for alg in ["R U R' U'", "x y' z2 M E S", "r u f l d b", "R2 D' x' M2 U"]:
            self.assertEqual(State().apply(alg).facelets(), Cube(3).apply(alg).facelets(), alg)

    def test_notation_identities(self):
        same = lambda a, b: State().apply(a).facelets() == State().apply(b).facelets()  # noqa
        self.assertTrue(same("M", "x' R L'"))
        self.assertTrue(same("r", "R M'"))
        self.assertTrue(same("E", "y' U D'"))
        self.assertTrue(same("S", "z F' B"))


class AlgorithmTest(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(algs.SET_BY_ID["oll"].cases), 57)
        self.assertEqual(len(algs.SET_BY_ID["pll"].cases), 21)
        self.assertEqual(len(algs.SET_BY_ID["f2l"].cases), 41)
        self.assertEqual(len(algs.SET_BY_ID["oll2"].cases), 10)
        self.assertEqual(len(algs.SET_BY_ID["pll2"].cases), 6)

    def test_ll_algorithms_keep_f2l(self):
        for sid in ("oll", "pll", "oll2", "pll2"):
            for c in algs.SET_BY_ID[sid].cases:
                after = State().apply(c.alg).normalize()
                self.assertTrue(f2l_solved(after), c.id)
                if c.view == "pll":
                    g = after.facelets()
                    self.assertTrue(all(x == "U" for row in g["U"] for x in row), c.id)

    def test_f2l_cases_touch_only_one_slot(self):
        for c in algs.SET_BY_ID["f2l"].cases:
            st = c.state().copy().normalize()
            self.assertTrue(others_solved(st), c.id)
            self.assertFalse(f2l_solved(st), c.id)

    def _distinct(self, sid, key, post, conj):
        cases = algs.SET_BY_ID[sid].cases
        fams = [family(c.alg, key, post, conj) for c in cases]
        for i in range(len(cases)):
            for j in range(i + 1, len(cases)):
                self.assertFalse(fams[i] & fams[j], (cases[i].id, cases[j].id))

    def test_oll_cases_distinct(self):
        self._distinct("oll", oll_mask, True, True)

    def test_pll_cases_distinct(self):
        self._distinct("pll", lambda s: s.key(), True, True)

    def test_f2l_cases_distinct(self):
        self._distinct("f2l", lambda s: s.key(), False, False)

    def test_oll_groups_match_shapes(self):
        for c in algs.SET_BY_ID["oll"].cases:
            n = int(c.id.split("-")[1])
            g = c.state().copy().normalize().facelets()
            edges = sum(1 for r, cc in [(0, 1), (1, 0), (1, 2), (2, 1)] if g["U"][r][cc] == "U")
            corners = sum(1 for r, cc in [(0, 0), (0, 2), (2, 0), (2, 2)] if g["U"][r][cc] == "U")
            if n in (1, 2, 3, 4, 17, 18, 19, 20):
                self.assertEqual(edges, 0, c.id)
            if 21 <= n <= 27:
                self.assertEqual(edges, 4, c.id)
            if n in (28, 57):
                self.assertEqual(corners, 4, c.id)

    def test_pictures_render(self):
        for c in algs.CASES.values():
            shapes = caseview.case_shapes(c)
            self.assertTrue(any(s[0] == "poly" for s in shapes))
        arrows = [s for s in caseview.case_shapes(algs.CASES["pll-H"]) if s[0] != "poly"]
        self.assertEqual(len(arrows), 2)  # two edge swaps


class AlternativesTest(unittest.TestCase):
    def test_alternatives_solve_the_same_case(self):
        for cid, alts in algs.ALTS.items():
            case = algs.CASES[cid]
            key = oll_mask if case.view == "oll" else (lambda s: s.key())
            main = family(case.alg, key)
            for alt in alts:
                self.assertTrue(f2l_solved(State().apply(alt).normalize()), (cid, alt))
                self.assertTrue(family(alt, key) & main, (cid, alt))

    def test_facts(self):
        from enigma_timer import insights
        facts = insights.facts(algs.CASES["pll-Ua"])
        self.assertIn("3", facts[1][0])
        self.assertTrue(all(len(f) == 2 for c in algs.CASES.values() for f in insights.facts(c)))


class LearnTest(unittest.TestCase):
    def test_leitner(self):
        p = learn.Progress({})
        cid = "oll-27"
        self.assertEqual(p.status(cid), learn.NEW)
        for _ in range(3):
            p.rate(cid, learn.GOOD, now=0)
        self.assertEqual(p.status(cid), learn.LEARNED)
        p.rate(cid, learn.AGAIN, now=0)
        self.assertEqual(p.status(cid), learn.LEARNING)
        self.assertTrue(p.is_due(cid, now=0))

    def test_trainer_introduces_new_cases_gradually(self):
        p = learn.Progress({})
        cases = algs.SET_BY_ID["pll"].cases
        t = learn.Trainer(p, cases)
        seen = set()
        for _ in range(20):
            c = t.next_case(now=0)
            seen.add(c.id)
            t.rate(c, learn.HARD, now=0)
        self.assertLessEqual(len(seen), learn.Trainer.NEW_PER_SESSION)

    def test_level_progress(self):
        p = learn.Progress({})
        self.assertEqual(p.next_level().id, "notation")
        p.set_lesson_done("notation")
        self.assertEqual(p.next_level().id, "beginner")
        for c in learn.LEVEL_BY_ID["beginner"].cases:
            p.set_status(c.id, learn.LEARNED)
        self.assertEqual(p.next_level().id, "cross")


if __name__ == "__main__":
    unittest.main()
