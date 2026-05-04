#!/usr/bin/env python3
"""Extract translator + search stats from Fast Downward log files.

Walks KRP_Project/runs/, parses each *.log file matching
<encoding>_<track>_<instance>_<heur>.log, and emits CSV.

Usage: ./extract_stats.py [runs_dir] [-o out.csv]
"""
import argparse
import csv
import os
import re
import sys
from pathlib import Path

LOG_NAME_RE = re.compile(
    r"^(?P<encoding>noaxioms|axioms)_(?P<track>opt|sat)_(?P<instance>p\d+)_(?P<heur>\w+)\.log$"
)

# (csv_field, regex, cast)
PATTERNS = [
    ("trans_variables",        r"^Translator variables:\s+(\d+)",          int),
    ("trans_derived_vars",     r"^Translator derived variables:\s+(\d+)",  int),
    ("trans_facts",            r"^Translator facts:\s+(\d+)",              int),
    ("trans_operators",        r"^Translator operators:\s+(\d+)",          int),
    ("trans_axioms",           r"^Translator axioms:\s+(\d+)",             int),
    ("trans_task_size",        r"^Translator task size:\s+(\d+)",          int),
    ("trans_peak_kb",          r"^Translator peak memory:\s+(\d+)\s+KB",   int),
    ("plan_cost",              r"^\[t=.*?\] Plan cost:\s+(\d+)",           int),
    ("plan_length",            r"^\[t=.*?\] Plan length:\s+(\d+)",         int),
    ("expanded",               r"^\[t=.*?\] Expanded\s+(\d+)\s+state",     int),
    ("generated",              r"^\[t=.*?\] Generated\s+(\d+)\s+state",    int),
    ("dead_ends",              r"^\[t=.*?\] Dead ends:\s+(\d+)\s+state",   int),
    ("search_time_s",          r"^\[t=.*?\] Search time:\s+([\d.]+)s",     float),
    ("total_time_s",           r"^\[t=.*?\] Total time:\s+([\d.]+)s",      float),
    ("peak_kb",                r"^Peak memory:\s+(\d+)\s+KB",              int),
    ("search_exit",            r"^search exit code:\s+(\d+)",              int),
]

STATUS_PATTERNS = [
    ("solved",  r"^Solution found"),
    ("timeout", r"[Tt]ime limit has been reached|reached the time limit"),
    ("memout",  r"[Mm]emory limit has been reached|reached the memory limit|MemoryError"),
]


def parse_log(path: Path) -> dict:
    row = {}
    text = path.read_text(errors="replace")
    for field, pat, cast in PATTERNS:
        m = re.search(pat, text, re.MULTILINE)
        if m:
            try:
                row[field] = cast(m.group(1))
            except ValueError:
                pass
    status = "unknown"
    for label, pat in STATUS_PATTERNS:
        if re.search(pat, text, re.MULTILINE | re.IGNORECASE):
            status = label
            break
    row["status"] = status
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs_dir", nargs="?", default="/home/buser/KRP_Project/runs")
    ap.add_argument("-o", "--output", default="-")
    args = ap.parse_args()

    rows = []
    for fn in sorted(os.listdir(args.runs_dir)):
        m = LOG_NAME_RE.match(fn)
        if not m:
            continue
        meta = m.groupdict()
        stats = parse_log(Path(args.runs_dir) / fn)
        rows.append({**meta, **stats})

    fields = ["encoding", "track", "instance", "heur", "status",
              "plan_cost", "plan_length", "expanded", "generated",
              "search_time_s", "total_time_s", "peak_kb",
              "trans_variables", "trans_derived_vars", "trans_facts",
              "trans_operators", "trans_axioms", "trans_task_size",
              "trans_peak_kb", "dead_ends", "search_exit"]
    out = sys.stdout if args.output == "-" else open(args.output, "w")
    w = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)


if __name__ == "__main__":
    main()
