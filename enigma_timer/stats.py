"""Solve model and WCA-style statistics."""

import math
import time

OK = 0
PLUS2 = 2
DNF = -1

INF = float("inf")


class Solve(object):
    __slots__ = ("ms", "penalty", "scramble", "date", "comment")

    def __init__(self, ms, penalty=OK, scramble="", date=None, comment=""):
        self.ms = int(ms)
        self.penalty = penalty
        self.scramble = scramble
        self.date = date if date is not None else time.time()
        self.comment = comment

    @property
    def value(self):
        """Effective time in ms (inf for DNF)."""
        if self.penalty == DNF:
            return INF
        if self.penalty == PLUS2:
            return self.ms + 2000
        return self.ms

    def to_dict(self):
        return {"ms": self.ms, "p": self.penalty, "s": self.scramble,
                "d": self.date, "c": self.comment}

    @classmethod
    def from_dict(cls, d):
        return cls(d.get("ms", 0), d.get("p", OK), d.get("s", ""),
                   d.get("d"), d.get("c", ""))


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def fmt_ms(ms, decimals=2):
    """Format milliseconds as 12.34 / 1:02.34 / 1:02:03.45.

    Singles are truncated (WCA style), not rounded.
    """
    if ms is None:
        return "-"
    if ms == INF:
        return "DNF"
    ms = int(ms)
    if decimals == 3:
        frac = "%03d" % (ms % 1000)
    elif decimals == 1:
        frac = "%d" % ((ms % 1000) // 100)
    else:
        frac = "%02d" % ((ms % 1000) // 10)
    total_s = ms // 1000
    h, rem = divmod(total_s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return "%d:%02d:%02d.%s" % (h, m, s, frac)
    if m:
        return "%d:%02d.%s" % (m, s, frac)
    return "%d.%s" % (s, frac)


def fmt_avg(v, decimals=2):
    """Averages are rounded to the displayed precision (WCA style)."""
    if v is None:
        return "-"
    if v == INF:
        return "DNF"
    step = {1: 100, 2: 10, 3: 1}.get(decimals, 10)
    return fmt_ms(int(math.floor(v / step + 0.5)) * step, decimals)


def fmt_solve(s, decimals=2):
    if s.penalty == DNF:
        return "DNF(%s)" % fmt_ms(s.ms, decimals)
    if s.penalty == PLUS2:
        return fmt_ms(s.ms + 2000, decimals) + "+"
    return fmt_ms(s.ms, decimals)


def parse_time(text):
    """Parse manual entry: '12.34', '1:02.5', '1234' (=12.34), 'DNF'."""
    t = text.strip().upper().replace(",", ".")
    if not t:
        raise ValueError("empty")
    penalty = OK
    if t.startswith("DNF"):
        penalty = DNF
        t = t[3:].strip("() ")
        if not t:
            return 0, DNF
    if t.endswith("+"):
        penalty = PLUS2 if penalty == OK else penalty
        t = t[:-1].strip()
    if ":" in t or "." in t:
        parts = t.split(":")
        secs = float(parts[-1])
        mins = int(parts[-2]) if len(parts) >= 2 else 0
        hours = int(parts[-3]) if len(parts) >= 3 else 0
        ms = int(round((hours * 3600 + mins * 60 + secs) * 1000))
    else:
        # digits only, stackmat-style: 1234 -> 12.34, 10234 -> 1:02.34
        digits = int(t)
        cs = digits % 100
        rest = digits // 100
        s = rest % 100
        m = rest // 100
        ms = (m * 60 + s) * 1000 + cs * 10
    if ms <= 0 and penalty != DNF:
        raise ValueError("zero")
    if penalty == PLUS2:
        ms -= 2000  # stored raw; "+" means the entered time already includes +2
        if ms <= 0:
            raise ValueError("zero")
    return ms, penalty


# ---------------------------------------------------------------------------
# Averages
# ---------------------------------------------------------------------------

def trim_count(n):
    """Number of solves removed from each side (WCA: 5% rounded up)."""
    if n < 5:
        return 0
    return int(math.ceil(n * 0.05))


def average(values):
    """WCA trimmed average of a list of effective values (inf = DNF)."""
    n = len(values)
    if n == 0:
        return None
    t = trim_count(n)
    dnfs = sum(1 for v in values if v == INF)
    if dnfs > t:
        return INF
    s = sorted(values)
    kept = s[t:n - t] if t else s
    return sum(kept) / float(len(kept))


def mean(values):
    if not values:
        return None
    if any(v == INF for v in values):
        return INF
    return sum(values) / float(len(values))


def trimmed_indices(values):
    """Indices (within values) of the solves excluded from the average."""
    n = len(values)
    t = trim_count(n)
    if not t:
        return set()
    order = sorted(range(n), key=lambda i: (values[i], i))
    return set(order[:t]) | set(order[n - t:])


def rolling(values, k, kind="avg"):
    """List where item i is the ao/mo of solves (i-k+1 .. i), or None."""
    fn = average if kind == "avg" else mean
    out = []
    for i in range(len(values)):
        if i + 1 < k:
            out.append(None)
        else:
            out.append(fn(values[i + 1 - k:i + 1]))
    return out


def best_of(seq):
    best = None
    best_i = None
    for i, v in enumerate(seq):
        if v is None:
            continue
        if best is None or v < best:
            best, best_i = v, i
    return best, best_i


# (label, size, kind) rows shown in the statistics panel
STAT_ROWS = [
    ("single", 1, "single"),
    ("mo3", 3, "mean"),
    ("ao5", 5, "avg"),
    ("ao12", 12, "avg"),
    ("ao50", 50, "avg"),
    ("ao100", 100, "avg"),
]


class SessionStats(object):
    """Pre-computed statistics for a list of solves."""

    def __init__(self, solves):
        self.solves = solves
        self.values = [s.value for s in solves]
        self.rows = {}
        self.series = {}
        for label, k, kind in STAT_ROWS:
            if kind == "single":
                seq = list(self.values)
            else:
                seq = rolling(self.values, k, "avg" if kind == "avg" else "mean")
            self.series[label] = seq
            cur = seq[-1] if seq else None
            best, best_i = best_of(seq)
            if best == INF:
                best, best_i = None, None
            self.rows[label] = {"current": cur, "best": best, "best_index": best_i,
                                "size": k}
        finite = [v for v in self.values if v != INF]
        self.count = len(self.values)
        self.dnf_count = self.count - len(finite)
        self.session_mean = (sum(finite) / len(finite)) if finite else None
        if len(finite) > 1:
            m = self.session_mean
            self.std_dev = math.sqrt(sum((v - m) ** 2 for v in finite) / (len(finite) - 1))
        else:
            self.std_dev = None
        self.worst = max(finite) if finite else None

    def ao(self, label, index):
        seq = self.series.get(label)
        if not seq or index < 0 or index >= len(seq):
            return None
        return seq[index]
