"""Checks the algorithm sets for 2x2, 4x4, Pyraminx, Skewb, Square-1 and BLD."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from enigma_timer import achievements, algs, caseview, learn, methods  # noqa: E402
from enigma_timer.cube import invert  # noqa: E402
from enigma_timer.fastn import NState, bottom_key, net_rotation  # noqa: E402
from enigma_timer.puzzles import Pyraminx, Skewb, sq1_parse  # noqa: E402
from enigma_timer.scramble import _SQ1_START, _sq1_can_slash, _sq1_slash, _sq1_twist  # noqa: E402

ROT = [(a + " " + b).strip() for a in ("", "x", "x2", "x'", "z", "z'") for b in ("", "y", "y2", "y'")]


def solved_up_to_rotation(state):
    return any(state.copy().apply(r).is_solved() for r in ROT)


class TwoByTwoTest(unittest.TestCase):
    def test_cll_and_ortega_oll_keep_first_layer(self):
        for name, alg in methods.CLL + methods.ORTEGA_OLL:
            rot = net_rotation(2, alg)
            after = NState(2).apply(alg)
            self.assertEqual(bottom_key(after), bottom_key(NState(2).apply(rot)), name)
            self.assertFalse(NState(2).apply(rot).apply(invert(alg)).is_solved(), name)

    def test_pbl_keeps_both_faces(self):
        for name, alg in methods.ORTEGA_PBL:
            g = NState(2).apply(alg).facelets()
            for f in "UD":
                self.assertEqual(len(set(sum(g[f], []))), 1, name)

    def test_beginner_algs_keep_first_layer(self):
        for cid, _n, alg, _h in methods.BEGINNER_222[1:]:
            self.assertEqual(bottom_key(NState(2).apply(alg)), bottom_key(NState(2)), cid)

    def test_cll_cases_distinct(self):
        auf = ["", "U", "U2", "U'"]
        ys = [("", ""), ("y", "y'"), ("y2", "y2"), ("y'", "y")]

        def norm(st):
            k = bottom_key(NState(2))
            for r in ROT:
                c = st.copy().apply(r)
                if bottom_key(c) == k:
                    return c
            return st

        fams = []
        for _, alg in methods.CLL:
            base = net_rotation(2, alg) + " " + invert(alg)
            fams.append(set(norm(NState(2).apply(" ".join([y, a, base, b, yi]))).key()
                            for a in auf for b in auf for y, yi in ys))
        for i in range(len(fams)):
            for j in range(i + 1, len(fams)):
                self.assertFalse(fams[i] & fams[j], (methods.CLL[i][0], methods.CLL[j][0]))


class RouxTest(unittest.TestCase):
    def test_cmll_keeps_both_blocks(self):
        from enigma_timer.fast3 import State
        for name, alg in methods.CMLL:
            g = State().apply(alg).facelets()
            for f in "LR":
                self.assertTrue(all(x == f for x in g[f][1] + g[f][2]), name)
            self.assertTrue(all(g["D"][r][c] == "D" for r in range(3) for c in (0, 2)), name)
            for f in "FB":
                self.assertTrue(all(g[f][r][c] == f for r in (1, 2) for c in (0, 2)), name)

    def test_cmll_cases_distinct(self):
        from enigma_timer.fast3 import State, net_rotation as nr3
        auf = ["", "U", "U2", "U'"]

        def key(st):
            g = st.facelets()
            return tuple([g["U"][r][c] for r in (0, 2) for c in (0, 2)] +
                         [g[f][0][c] for f in "FRBL" for c in (0, 2)])

        fams = []
        for _, alg in methods.CMLL:
            base = nr3(alg) + " " + invert(alg)
            fams.append(set(key(State().apply(a + " " + base + " " + b)) for a in auf for b in auf))
        self.assertEqual(len(fams), 42)
        for i in range(len(fams)):
            self.assertNotIn(key(State()), fams[i])
            for j in range(i + 1, len(fams)):
                self.assertFalse(fams[i] & fams[j], (methods.CMLL[i][0], methods.CMLL[j][0]))


class BigCubeTest(unittest.TestCase):
    def test_444_parity_algorithms(self):
        for cid, _n, alg, _h in methods.PARITY_444:
            g = NState(4).apply(alg).facelets()
            self.assertTrue(all(x == "D" for row in g["D"] for x in row), cid)
            for f in "FRBL":
                for r in (1, 2, 3):
                    self.assertTrue(all(x == f for x in g[f][r]), cid)
        # the OLL parity flips exactly one edge pair (4 stickers)
        g = NState(4).apply(methods.PARITY_444[0][2]).facelets()
        moved = sum(1 for f in g for r in range(4) for c in range(4) if g[f][r][c] != f)
        self.assertEqual(moved, 4)

    def test_555_edge_alg_keeps_centres(self):
        g = NState(5).apply(methods.EDGES_555[0][2]).facelets()
        self.assertTrue(all(g[f][r][c] == f for f in g for r in (1, 2, 3) for c in (1, 2, 3)))


class PyraminxTest(unittest.TestCase):
    KINDS = None

    @classmethod
    def setUpClass(cls):
        kinds = []
        for i in range(3):
            for j in range(3 - i):
                kinds.append("tip" if (i, j) in [(0, 0), (2, 0), (0, 2)] else "edge")
                if i + j <= 1:
                    kinds.append("centre")
        cls.KINDS = kinds * 4
        cls.BASE = [s[2] for s in Pyraminx().slots]

    def test_l4e_moves_only_edges(self):
        algs_ = [a for _, a in methods.PYRA_L4E] + [a for _, _, a, _ in methods.PYRA_BEGINNER]
        for alg in algs_:
            ok = False
            for post in ("", "U", "U'"):
                q = Pyraminx().apply(alg + " " + post)
                changed = set(self.KINDS[i] for i, (a, b) in enumerate(zip(self.BASE, q.colors))
                              if a != b)
                if changed <= {"edge"}:
                    ok = True
                    break
            self.assertTrue(ok, alg)


class SkewbTest(unittest.TestCase):
    def test_layer_method(self):
        base = [s[2] for s in Skewb().slots]
        faces = ["U", "D", "R", "L", "F", "B"]
        d_slots = [i for i in range(30) if faces[i // 5] == "D"]
        for name, alg in methods.SKEWB_CORNERS + methods.SKEWB_CENTRES:
            case = Skewb().apply(invert(alg))
            self.assertFalse(case.is_solved(), name)
            # the case has the first layer (D centre + D corners) solved
            self.assertTrue(all(case.colors[i] == base[i] for i in d_slots), name)
            self.assertTrue(case.apply(alg).is_solved(), name)
        for name, alg in methods.SKEWB_CENTRES:
            case = Skewb().apply(invert(alg))
            corners_ok = all(case.colors[i] == base[i] for i in range(30) if i % 5)
            self.assertTrue(corners_ok, name)


class Square1Test(unittest.TestCase):
    def test_algorithms_are_legal_from_cube_shape(self):
        piece = list(_SQ1_START)
        for cid, _n, alg, _h in methods.SQ1_BEGINNER:
            st = list(range(24))
            for mv in sq1_parse(alg):
                if mv == "/":
                    self.assertTrue(_sq1_can_slash([piece[u] for u in st]), cid)
                    st = _sq1_slash(st)
                else:
                    st = _sq1_twist(st, mv[0], mv[1])


class RegistryTest(unittest.TestCase):
    def test_every_case_has_a_picture_and_setup(self):
        for c in algs.CASES.values():
            self.assertTrue(caseview.case_shapes(c), c.id)
            self.assertTrue(c.setup() or c.puzzle == "minx", c.id)

    def test_every_path_level_exists(self):
        for pid, levels in learn.PATHS.items():
            self.assertTrue(levels, pid)
            for lv in levels:
                if lv.set_id:
                    self.assertIn(lv.set_id, algs.SET_BY_ID, lv.id)

    def test_achievements_evaluate(self):
        import tempfile
        from enigma_timer.stats import Solve
        from enigma_timer.storage import Store
        st = Store(os.path.join(tempfile.mkdtemp(), "d.json"))
        new, status = achievements.check(st)
        self.assertEqual(new, [])
        st.current.solves.append(Solve(9000))
        new, status = achievements.check(st)
        ids = set(a["id"] for a in new)
        self.assertTrue({"first", "sub10", "sub60"} <= ids)
        self.assertEqual(achievements.check(st)[0], [])   # not unlocked twice


if __name__ == "__main__":
    unittest.main()
