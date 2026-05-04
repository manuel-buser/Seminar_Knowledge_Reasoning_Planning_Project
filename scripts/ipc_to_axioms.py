#!/usr/bin/env python3
"""Rewrite an IPC-2018 Spider instance for use with Spider_Axioms/domain.pddl.

Three transformations:
  1. (:domain spider) -> (:domain spider-axioms)
  2. Strip every (part-of-tableau ...) line from :init   [derived predicate]
  3. Strip every (movable ...) line from :init           [derived predicate]

Idempotent. Reads stdin or path arg, writes stdout or to -o path.
"""
import argparse
import re
import sys

DROP_PREDS = ("part-of-tableau", "movable")
DOMAIN_RE = re.compile(r"\(:domain\s+spider\s*\)")


def rewrite(text: str) -> str:
    out_lines = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        # Drop derived-predicate :init facts. Match "(<pred> " or "(<pred>)".
        if any(stripped.startswith(f"({p} ") or stripped.startswith(f"({p})")
               for p in DROP_PREDS):
            continue
        out_lines.append(line)
    rewritten = "".join(out_lines)
    rewritten = DOMAIN_RE.sub("(:domain spider-axioms)", rewritten)
    return rewritten


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="input PDDL (default stdin)")
    ap.add_argument("-o", "--output", help="output path (default stdout)")
    args = ap.parse_args()

    src = open(args.input).read() if args.input else sys.stdin.read()
    dst = rewrite(src)
    if args.output:
        with open(args.output, "w") as f:
            f.write(dst)
    else:
        sys.stdout.write(dst)


if __name__ == "__main__":
    main()
