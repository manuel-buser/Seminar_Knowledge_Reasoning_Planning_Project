#!/usr/bin/env python3
"""Build a Markdown comparison report from the FD run logs.

Reads /home/buser/KRP_Project/runs/, extracts stats, emits Markdown to stdout
or to -o path.

Sections:
  1. Translator-stats compactness (per instance, both encodings side-by-side)
  2. Optimal-search results (4-cell matrix per opt-track instance)
  3. Satisficing LAMA trajectories (per sat-track instance)
"""
import argparse
import csv
import io
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_stats import LOG_NAME_RE, parse_log
from lama_trajectory import trajectory


def collect_rows():
    rows = []
    for fn in sorted(p.name for p in RUNS.iterdir()):
        m = LOG_NAME_RE.match(fn)
        if not m:
            continue
        rows.append({**m.groupdict(), **parse_log(RUNS / fn)})
    return rows


def fmt(x, default="—"):
    return default if x is None or x == "" else str(x)


def render_translator_table(rows):
    out = io.StringIO()
    out.write("## Translator stats (encoding compactness)\n\n")
    out.write("Per IPC instance, comparing the no-axioms baseline against the axioms ")
    out.write("reformulation. These numbers come from FD's translator and are ")
    out.write("recorded even when search times out. The ratio columns show ")
    out.write("axioms / no-axioms.\n\n")
    out.write("| track | inst | "
              "vars (n / a / ratio) | "
              "operators (n / a / ratio) | "
              "task size (n / a / ratio) | "
              "derived vars (a) | axioms (a) |\n")
    out.write("|---|---|---|---|---|---:|---:|\n")
    by_inst = defaultdict(dict)
    for r in rows:
        by_inst[(r["track"], r["instance"])][r["encoding"]] = r
    for (track, inst), pair in sorted(by_inst.items()):
        n = pair.get("noaxioms", {})
        a = pair.get("axioms", {})

        def cell(field):
            nv, av = n.get(field), a.get(field)
            ratio = f"{av/nv:.2f}" if nv and av else "—"
            return f"{fmt(nv)} / {fmt(av)} / {ratio}"

        out.write(
            f"| {track} | {inst} | {cell('trans_variables')} | "
            f"{cell('trans_operators')} | {cell('trans_task_size')} | "
            f"{fmt(a.get('trans_derived_vars'))} | "
            f"{fmt(a.get('trans_axioms'))} |\n"
        )
    return out.getvalue() + "\n"


def render_coverage(rows):
    out = io.StringIO()
    out.write("## Coverage (instances solved per cell, 5 min / 4 GB budget)\n\n")
    out.write("| track | encoding × heuristic | solved / total |\n")
    out.write("|---|---|---:|\n")
    cells = (
        ("opt", "noaxioms", "blind"),
        ("opt", "noaxioms", "lmcut"),
        ("opt", "axioms",   "blind"),
        ("opt", "axioms",   "hmax"),
        ("sat", "noaxioms", "lama"),
        ("sat", "axioms",   "lama"),
    )
    for tr, enc, heur in cells:
        match = [r for r in rows if (r["track"], r["encoding"], r["heur"]) == (tr, enc, heur)]
        # For sat: "solved" means LAMA found at least one plan.
        if tr == "sat":
            solved = sum(1 for r in match if r.get("plan_cost") is not None)
        else:
            solved = sum(1 for r in match if r.get("status") == "solved")
        total = len(match)
        out.write(f"| {tr} | {enc} + {heur} | {solved} / {total} |\n")
    return out.getvalue() + "\n"


def render_optimal_summary(rows):
    """Side-by-side speedup table: noaxioms-lmcut vs axioms-hmax on solved instances."""
    out = io.StringIO()
    out.write("## Optimal search — informative-admissible head-to-head\n\n")
    out.write("`noaxioms+lmcut` is the best informative-admissible cell on the no-axioms ")
    out.write("encoding; `axioms+hmax` is the equivalent on the axioms encoding. Same ")
    out.write("optimal cost on every instance — cells differ on expansions and time.\n\n")
    out.write("| inst | cost | "
              "expanded (n / a / ratio) | "
              "total time s (n / a / ratio) |\n")
    out.write("|---|---:|---|---|\n")
    by_inst = defaultdict(dict)
    for r in rows:
        if r["track"] != "opt":
            continue
        if (r["encoding"], r["heur"]) in (("noaxioms", "lmcut"), ("axioms", "hmax")):
            by_inst[r["instance"]][(r["encoding"], r["heur"])] = r
    for inst, pair in sorted(by_inst.items()):
        n = pair.get(("noaxioms", "lmcut"), {})
        a = pair.get(("axioms", "hmax"), {})
        if n.get("status") != "solved" or a.get("status") != "solved":
            continue

        def cell(field, fmt_fn=str):
            nv, av = n.get(field), a.get(field)
            ratio = f"{av/nv:.2f}" if nv and av else "—"
            return f"{fmt_fn(nv)} / {fmt_fn(av)} / {ratio}"

        cost = a.get("plan_cost") or n.get("plan_cost")
        out.write(
            f"| {inst} | {fmt(cost)} | {cell('expanded')} | "
            f"{cell('total_time_s')} |\n"
        )
    return out.getvalue() + "\n"


def render_optimal_table(rows):
    out = io.StringIO()
    out.write("## Optimal search results\n\n")
    out.write("4-cell matrix: {no-axioms, axioms} × {blind, informative-admissible}. ")
    out.write("Wall-clock budget 5 min, memory 4 GB. `lmcut` runs on the no-axioms ")
    out.write("encoding; `hmax` runs on the axioms encoding (lmcut does not reliably ")
    out.write("support axioms in this FD build).\n\n")
    out.write("| inst | encoding | heur | status | cost | length | expanded | "
              "search time (s) | total time (s) |\n")
    out.write("|---|---|---|---|---:|---:|---:|---:|---:|\n")
    opt = sorted([r for r in rows if r["track"] == "opt"],
                 key=lambda r: (r["instance"], r["encoding"], r["heur"]))
    for r in opt:
        status = r.get("status", "unknown")
        out.write(
            f"| {r['instance']} | {r['encoding']} | {r['heur']} | {status} | "
            f"{fmt(r.get('plan_cost'))} | {fmt(r.get('plan_length'))} | "
            f"{fmt(r.get('expanded'))} | {fmt(r.get('search_time_s'))} | "
            f"{fmt(r.get('total_time_s'))} |\n"
        )
    return out.getvalue() + "\n"


def render_sat_table(rows):
    out = io.StringIO()
    out.write("## Satisficing — LAMA anytime trajectories\n\n")
    out.write("Both encodings under `--alias lama`. Trajectory is the sequence of ")
    out.write("improving solutions LAMA finds before the time budget runs out.\n\n")
    sat = [r for r in rows if r["track"] == "sat"]
    if not sat:
        out.write("_(no satisficing runs yet)_\n\n")
        return out.getvalue()
    by_inst = defaultdict(dict)
    for r in sat:
        by_inst[r["instance"]][r["encoding"]] = r
    for inst in sorted(by_inst):
        out.write(f"### {inst}\n\n")
        out.write("| encoding | t (s) | length | cost |\n|---|---:|---:|---:|\n")
        for enc in ("noaxioms", "axioms"):
            r = by_inst[inst].get(enc)
            if not r:
                continue
            log = RUNS / f"{enc}_sat_{inst}_lama.log"
            traj = trajectory(log.read_text()) if log.exists() else []
            if not traj:
                out.write(f"| {enc} | (no solution) | | |\n")
                continue
            for step in traj:
                out.write(f"| {enc} | {step['time_s']} | {step['length']} | {step['cost']} |\n")
        out.write("\n")
    return out.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="-")
    args = ap.parse_args()
    rows = collect_rows()
    body = (
        "# Spider — axioms vs no-axioms: experimental results\n\n"
        f"Generated from {len(rows)} run logs.\n\n"
        + render_coverage(rows)
        + render_translator_table(rows)
        + render_optimal_summary(rows)
        + render_optimal_table(rows)
        + render_sat_table(rows)
    )
    if args.output == "-":
        sys.stdout.write(body)
    else:
        Path(args.output).write_text(body)
        print(f"wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
