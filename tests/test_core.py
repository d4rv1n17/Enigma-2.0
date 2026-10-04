import json
import os
import random
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from enigma_timer import scramble, stats, storage  # noqa: E402
from enigma_timer.cube import Cube  # noqa: E402
from enigma_timer.stats import Solve, INF, OK, PLUS2, DNF  # noqa: E402


def invert(alg):
    out = []
    for tok in reversed(alg.split()):
        if tok.endswith("'"):
            out.append(tok[:-1])
        elif tok.endswith("2"):
            out.append(tok)
        else:
            out.append(tok + "'")
    return " ".join(out)


class CubeTest(unittest.TestCase):
    def test_sexy_move_order_6(self):
        c = Cube(3)
        for _ in range(6):
            c.apply("R U R' U'")
        self.assertTrue(c.is_solved())

    def test_R_moves_front_to_up(self):
        g = Cube(3).apply("R").facelets()
        self.assertEqual([g["U"][r][2] for r in range(3)], ["F"] * 3)
        self.assertEqual([g["F"][r][2] for r in range(3)], ["D"] * 3)
        self.assertEqual([g["B"][r][0] for r in range(3)], ["U"] * 3)

    def test_U_moves_front_to_left(self):
        g = Cube(3).apply("U").facelets()
        self.assertEqual(g["L"][0], ["F"] * 3)
        self.assertEqual(g["F"][0], ["R"] * 3)

    def test_F_moves_up_to_right(self):
        g = Cube(3).apply("F").facelets()
        self.assertEqual([g["R"][r][0] for r in range(3)], ["U"] * 3)
        self.assertEqual(g["U"][2], ["L"] * 3)

    def test_inverse_restores_all_sizes(self):
        for pid, n in scramble.CUBE_SIZE.items():
            for _ in range(5):
                s = scramble.generate(pid)
                c = Cube(n).apply(s)
                self.assertFalse(c.is_solved(), pid)
                c.apply(invert(s))
                self.assertTrue(c.is_solved(), pid)

    def test_wide_equals_slice_plus_face(self):
        a = Cube(4).apply("Rw").facelets()
        b = Cube(4).apply("R").facelets()
        self.assertNotEqual(a, b)
        a5 = Cube(5).apply("3Rw").facelets()
        b5 = Cube(5).apply("Rw").facelets()
        self.assertNotEqual(a5, b5)

    def test_superflip_centers_fixed_3x3(self):
        g = Cube(3).apply("R L U2 F U' D F2 R2 B2 L U2 F' B' U R2 D F2 U R2 U").facelets()
        for f in "URFDLB":
            self.assertEqual(g[f][1][1], f)


class ScrambleTest(unittest.TestCase):
    def test_all_generate(self):
        random.seed(1)
        for pid in scramble.PUZZLE_IDS:
            for _ in range(50):
                s = scramble.generate(pid)
                self.assertTrue(s.strip())

    def test_no_redundant_axis_moves(self):
        random.seed(2)
        for pid in ["333", "444", "777"]:
            for _ in range(200):
                toks = scramble.generate(pid).split()
                run = []
                for t in toks:
                    base = t.rstrip("'2")
                    face = [ch for ch in base if ch in "URFDLB"][0]
                    axis = {"U": 0, "D": 0, "R": 1, "L": 1, "F": 2, "B": 2}[face]
                    if run and run[-1][0] == axis:
                        self.assertNotIn(base, [b for _, b in run], toks)
                        run.append((axis, base))
                    else:
                        run = [(axis, base)]

    def test_lengths(self):
        self.assertEqual(len(scramble.generate("333").split()), 25)
        self.assertEqual(len(scramble.generate("222").split()), 11)
        self.assertEqual(len(scramble.generate("minx").split("\n")), 7)
        self.assertEqual(scramble.generate("sq1").count("/"), 12)

    def test_sq1_shape_stays_legal(self):
        random.seed(3)
        for _ in range(200):
            st = list(scramble._SQ1_START)
            for tok in scramble.generate("sq1").split():
                a, b = tok.strip("()/").split(",")
                st = scramble._sq1_twist(st, int(a), int(b))
                self.assertTrue(scramble._sq1_can_slash(st))
                st = scramble._sq1_slash(st)
            # every piece still occupies 1 (edge) or 2 adjacent (corner) units
            for layer in (st[:12], st[12:]):
                for pid in set(layer):
                    idx = [i for i, v in enumerate(layer) if v == pid]
                    self.assertIn(len(idx), (1, 2))


class PuzzleSimTest(unittest.TestCase):
    def test_orders(self):
        from enigma_timer.puzzles import Pyraminx, Skewb
        for cls, moves in ((Pyraminx, "ULRBulrb"), (Skewb, "RULB")):
            for m in moves:
                p = cls()
                p.apply(" ".join([m] * 3))
                self.assertTrue(p.is_solved(), (cls.__name__, m))
                p = cls().apply(m)
                self.assertFalse(p.is_solved())
                p.apply(m + "'")
                self.assertTrue(p.is_solved())

    def test_scramble_inverse(self):
        from enigma_timer.puzzles import Pyraminx, Skewb
        for cls, pid in ((Pyraminx, "pyram"), (Skewb, "skewb")):
            for _ in range(20):
                s = scramble.generate(pid)
                p = cls().apply(s)
                inv = " ".join(t[:-1] if t.endswith("'") else t + "'" for t in reversed(s.split()))
                p.apply(inv)
                self.assertTrue(p.is_solved())

    def test_skewb_r_cycles_centres(self):
        from enigma_timer.puzzles import Skewb
        p = Skewb().apply("R")
        # centre slots are the first slot of each face block (5 slots per face)
        faces = ["U", "D", "R", "L", "F", "B"]
        centres = dict((f, p.colors[i * 5]) for i, f in enumerate(faces))
        self.assertEqual(centres["R"], "#ffd500")  # D -> R
        self.assertEqual(centres["U"], "#ffffff")

    def test_sq1_first_moves(self):
        st = scramble._SQ1_START
        legal = lambda x, y: scramble._sq1_can_slash(scramble._sq1_twist(st, x, y))  # noqa: E731
        self.assertTrue(legal(1, 0))
        self.assertTrue(legal(0, -1))
        self.assertFalse(legal(-1, 0))
        self.assertFalse(legal(0, 1))

    def test_sq1_polygons(self):
        from enigma_timer.puzzles import sq1_polygons
        for _ in range(20):
            self.assertEqual(len(sq1_polygons(scramble.generate("sq1"))), 48)

    def test_extra_events(self):
        for pid in ("333oh", "333bf", "333fm"):
            s = scramble.generate(pid)
            Cube(3).apply(s)
        fm = scramble.generate("333fm").split()
        self.assertEqual(fm[:3], ["R'", "U'", "F"])
        self.assertEqual(fm[-3:], ["R'", "U'", "F"])


class StatsTest(unittest.TestCase):
    def test_ao5(self):
        v = [10000, 12000, 11000, 9000, 20000]
        self.assertAlmostEqual(stats.average(v), 11000)

    def test_ao5_one_dnf(self):
        v = [10000, INF, 11000, 9000, 12000]
        self.assertAlmostEqual(stats.average(v), 11000)

    def test_ao5_two_dnf(self):
        self.assertEqual(stats.average([1, INF, INF, 3, 4]), INF)

    def test_ao12_trim(self):
        self.assertEqual(stats.trim_count(12), 1)
        self.assertEqual(stats.trim_count(50), 3)
        self.assertEqual(stats.trim_count(100), 5)

    def test_mo3_dnf(self):
        self.assertEqual(stats.mean([1, 2, INF]), INF)

    def test_format(self):
        self.assertEqual(stats.fmt_ms(12345), "12.34")
        self.assertEqual(stats.fmt_ms(62345), "1:02.34")
        self.assertEqual(stats.fmt_ms(12345, 3), "12.345")
        self.assertEqual(stats.fmt_avg(12345.0), "12.35")
        self.assertEqual(stats.fmt_ms(INF), "DNF")

    def test_parse(self):
        self.assertEqual(stats.parse_time("12.34"), (12340, OK))
        self.assertEqual(stats.parse_time("1234"), (12340, OK))
        self.assertEqual(stats.parse_time("10234"), (62340, OK))
        self.assertEqual(stats.parse_time("1:02.5"), (62500, OK))
        self.assertEqual(stats.parse_time("14.34+"), (12340, PLUS2))
        self.assertEqual(stats.parse_time("dnf"), (0, DNF))
        self.assertEqual(stats.parse_time("DNF(12.00)"), (12000, DNF))

    def test_session_stats(self):
        solves = [Solve(10000 + i * 100) for i in range(12)]
        solves[3].penalty = DNF
        st = stats.SessionStats(solves)
        self.assertEqual(st.rows["single"]["best"], 10000)
        self.assertIsNotNone(st.rows["ao12"]["current"])
        self.assertIsNone(st.rows["ao50"]["current"])
        self.assertEqual(st.dnf_count, 1)


class StorageTest(unittest.TestCase):
    def test_roundtrip(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "data.json")
        s = storage.Store(p)
        s.current.solves.append(Solve(12345, PLUS2, "R U", 1.0, "hi"))
        s.new_session("Big", "777")
        s.save()
        s2 = storage.Store(p)
        self.assertEqual(len(s2.sessions), 2)
        self.assertEqual(s2.current.puzzle, "777")
        self.assertEqual(s2.sessions[0].solves[0].value, 14345)
        storage.export_csv(s2.sessions[0], os.path.join(d, "x.csv"))

    def test_cstimer_import(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "cs.txt")
        data = {
            "session1": [[[0, 12340], "R U", "", 1600000000],
                         [[2000, 11000], "F", "c", 1600000001],
                         [[-1, 9000], "B", "", 1600000002]],
            "session2": [],
            "properties": {"sessionData": json.dumps(
                {"1": {"name": "main", "opt": {"scrType": "444wca"}}})},
        }
        with open(p, "w") as f:
            json.dump(data, f)
        res = storage.import_cstimer(p)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].puzzle, "444")
        self.assertEqual([x.penalty for x in res[0].solves], [OK, PLUS2, DNF])


if __name__ == "__main__":
    unittest.main()
