"""Persistent storage of sessions and settings (a single JSON file)."""

import csv
import io
import json
import os
import sys
import time
import uuid

from .stats import Solve, OK, PLUS2, DNF, fmt_ms

DEFAULT_SETTINGS = {
    "inspection": False,        # 15 s WCA inspection
    "inspection_alerts": True,  # beep at 8 s / 12 s
    "hold_ms": 300,             # how long Space must be held before start
    "update_mode": "full",      # full | tenths | seconds | hidden
    "decimals": 2,
    "focus_mode": True,         # hide everything while solving
    "show_preview": True,
    "show_chart": True,
    "minimal": False,           # hide side panels
    "language": None,           # None = follow the Windows language
}


def data_dir():
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        path = os.path.join(base, "EnigmaTimer")
    elif sys.platform == "darwin":
        path = os.path.expanduser("~/Library/Application Support/EnigmaTimer")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
        path = os.path.join(base, "EnigmaTimer")
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


class Session(object):
    def __init__(self, name, puzzle, solves=None, sid=None):
        self.id = sid or uuid.uuid4().hex[:12]
        self.name = name
        self.puzzle = puzzle
        self.solves = solves or []

    def to_dict(self):
        return {"id": self.id, "name": self.name, "puzzle": self.puzzle,
                "solves": [s.to_dict() for s in self.solves]}

    @classmethod
    def from_dict(cls, d):
        return cls(d.get("name", "Session"), d.get("puzzle", "333"),
                   [Solve.from_dict(x) for x in d.get("solves", [])], d.get("id"))


class Store(object):
    VERSION = 2

    def __init__(self, path=None):
        self.path = path or os.path.join(data_dir(), "data.json")
        self.settings = dict(DEFAULT_SETTINGS)
        self.training = {}
        self.sessions = []
        self.current_id = None
        self.load()

    # ------------------------------------------------------------------
    def load(self):
        data = None
        if os.path.exists(self.path):
            try:
                with io.open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (ValueError, IOError, OSError):
                # keep a copy of the broken file instead of silently losing it
                try:
                    os.replace(self.path, self.path + ".broken-%d" % int(time.time()))
                except OSError:
                    pass
                data = None
        if data:
            self.settings.update(data.get("settings", {}))
            self.sessions = [Session.from_dict(s) for s in data.get("sessions", [])]
            self.current_id = data.get("current")
            self.training = data.get("training", {}) or {}
        if not self.sessions:
            self.sessions = [Session("3x3", "333")]
        if self.current is None:
            self.current_id = self.sessions[0].id

    def save(self):
        data = {"version": self.VERSION, "settings": self.settings,
                "training": self.training,
                "current": self.current_id,
                "sessions": [s.to_dict() for s in self.sessions]}
        text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        tmp = self.path + ".tmp"
        with io.open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, self.path)

    # ------------------------------------------------------------------
    @property
    def current(self):
        for s in self.sessions:
            if s.id == self.current_id:
                return s
        return None

    def sessions_for(self, puzzle):
        return [s for s in self.sessions if s.puzzle == puzzle]

    def new_session(self, name, puzzle):
        s = Session(name, puzzle)
        self.sessions.append(s)
        self.current_id = s.id
        return s

    def delete_session(self, sid):
        self.sessions = [s for s in self.sessions if s.id != sid]
        if not self.sessions:
            self.sessions = [Session("3x3", "333")]
        if self.current is None:
            self.current_id = self.sessions[0].id


# ---------------------------------------------------------------------------
# Import / export
# ---------------------------------------------------------------------------

def export_csv(session, path, decimals=2):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["No", "Time", "Penalty", "Raw ms", "Scramble", "Date", "Comment"])
        for i, s in enumerate(session.solves, 1):
            pen = {OK: "", PLUS2: "+2", DNF: "DNF"}.get(s.penalty, "")
            shown = "DNF" if s.penalty == DNF else fmt_ms(s.value, decimals)
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s.date))
            w.writerow([i, shown, pen, s.ms, s.scramble.replace("\n", " "), date, s.comment])


_CSTIMER_TYPES = [
    ("333oh", "333oh"), ("333ni", "333bf"), ("333bf", "333bf"), ("333fm", "333fm"),
    ("222", "222"), ("333", "333"), ("444", "444"), ("555", "555"),
    ("666", "666"), ("777", "777"), ("pyr", "pyram"), ("skb", "skewb"),
    ("mgm", "minx"), ("minx", "minx"), ("clk", "clock"), ("sq1", "sq1"),
]


def _cstimer_puzzle(scr_type):
    scr_type = (scr_type or "").lower()
    for prefix, pid in _CSTIMER_TYPES:
        if scr_type.startswith(prefix):
            return pid
    return "333"


def import_cstimer(path):
    """Read a csTimer export file and return a list of Session objects."""
    with io.open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = {}
    props = data.get("properties", {})
    sd = props.get("sessionData")
    if isinstance(sd, str):
        try:
            sd = json.loads(sd)
        except ValueError:
            sd = {}
    if isinstance(sd, dict):
        meta = sd
    result = []
    keys = sorted((k for k in data if k.startswith("session") and k[7:].isdigit()),
                  key=lambda k: int(k[7:]))
    for key in keys:
        raw = data[key]
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except ValueError:
                continue
        if not raw:
            continue
        num = key[7:]
        info = meta.get(num, {}) if isinstance(meta, dict) else {}
        name = info.get("name", num)
        opt = info.get("opt", {}) or {}
        puzzle = _cstimer_puzzle(opt.get("scrType", "333"))
        solves = []
        for entry in raw:
            try:
                pen, ms = entry[0][0], entry[0][1]
                scramble = entry[1] if len(entry) > 1 else ""
                comment = entry[2] if len(entry) > 2 else ""
                date = entry[3] if len(entry) > 3 else None
            except (IndexError, TypeError):
                continue
            if pen == -1:
                p = DNF
            elif pen == 2000:
                p = PLUS2
            else:
                p = OK
            solves.append(Solve(ms, p, scramble or "", date, comment or ""))
        result.append(Session("csTimer %s" % name, puzzle, solves))
    return result
