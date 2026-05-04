#!/usr/bin/env python3
"""Extract LAMA's anytime cost trajectory from a Fast Downward log.

LAMA emits multiple "Plan length: N step(s)." / "Plan cost: C" pairs, one per
improving solution. We pair them in order of appearance and emit (idx, cost,
length, time_s) tuples.

Usage: ./lama_trajectory.py <log file>...
"""
import re
import sys

PLAN_RE = re.compile(
    r"\[t=(?P<t>[\d.]+)s.*?\]\s+Plan length:\s+(?P<length>\d+).*?\n"
    r"\[t=[\d.]+s.*?\]\s+Plan cost:\s+(?P<cost>\d+)",
    re.MULTILINE,
)


def trajectory(text: str):
    return [
        {
            "idx":     i,
            "time_s":  float(m.group("t")),
            "length":  int(m.group("length")),
            "cost":    int(m.group("cost")),
        }
        for i, m in enumerate(PLAN_RE.finditer(text))
    ]


def main():
    for path in sys.argv[1:]:
        text = open(path).read()
        traj = trajectory(text)
        print(f"# {path}")
        print("idx\ttime_s\tlength\tcost")
        for r in traj:
            print(f"{r['idx']}\t{r['time_s']}\t{r['length']}\t{r['cost']}")
        print()


if __name__ == "__main__":
    main()
