#!/usr/bin/env python3
"""Animate a Spider plan: read instance + sas_plan, render the state at each step.

Usage:
  spider_viz.py <instance.pddl> <plan-file>          # ASCII frames to stdout
  spider_viz.py <instance.pddl> <plan-file> --html OUT.html

Card naming convention (IPC encoding): card-d{deck}-s{suit}-v{value}.
We render value as a number (0 = ace, max = king) and use distinct unicode
glyphs for the four suits.
"""
import argparse
import re
import sys
from pathlib import Path

SUIT_GLYPH = ["S", "H", "D", "C"]   # spades, hearts, diamonds, clubs (s0..s3)


def parse_card(name: str):
    m = re.match(r"card-d(\d+)-s(\d+)-v(\d+)", name)
    return None if not m else (int(m[1]), int(m[2]), int(m[3]))


def card_label(name: str) -> str:
    parsed = parse_card(name)
    if parsed is None:
        return name
    _, suit, value = parsed
    glyph = SUIT_GLYPH[suit] if suit < len(SUIT_GLYPH) else f"S{suit}"
    return f"{value:>2}{glyph}"


def _slice_block(text: str, marker: str) -> str:
    """Return the body of the (marker ...) s-expression — paren-balanced."""
    start = text.find(marker)
    if start == -1:
        return ""
    i = start + len(marker)
    depth = 1
    while i < len(text) and depth > 0:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    return text[start + len(marker) : i - 1]


def parse_instance(path: Path):
    text = path.read_text()
    init_block = _slice_block(text, "(:init")
    cards, piles, deals = set(), [], []
    for m in re.finditer(r"(card-d\d+-s\d+-v\d+)\s*-\s*card", text):
        cards.add(m.group(1))
    for m in re.finditer(r"(pile-\d+)\s*-\s*tableau", text):
        piles.append(m.group(1))
    for m in re.finditer(r"(deal-\d+)\s*-\s*deal", text):
        deals.append(m.group(1))
    piles.sort(key=lambda s: int(s.split("-")[1]))
    deals.sort(key=lambda s: int(s.split("-")[1]))
    init_on = dict(re.findall(r"\(on\s+(\S+)\s+(\S+)\)", init_block))
    in_play = set(re.findall(r"\(in-play\s+(\S+)\)", init_block))
    return {
        "cards":   cards,
        "piles":   piles,
        "deals":   deals,
        "on":      init_on,
        "in_play": in_play,
        "discard": [],
        "phase":   "idle",
    }


def stack_at(state, base):
    """Return list of card names stacked on `base`, bottom-up. `base` itself excluded."""
    on_inv = {}
    for c, b in state["on"].items():
        on_inv.setdefault(b, []).append(c)
    out, cur = [], base
    while cur in on_inv:
        nxt = on_inv[cur]
        if not nxt:
            break
        cur = nxt[0]
        out.append(cur)
    return out


def render(state, step_idx, action) -> str:
    rows = [f"step {step_idx:>3}: {action}"]
    rows.append(f"phase: {state['phase']}")
    rows.append("")
    for pile in state["piles"]:
        labels = [card_label(c) for c in stack_at(state, pile)]
        rows.append(f"  {pile:<8}: " + " ".join(labels) if labels else f"  {pile:<8}: (empty)")
    rows.append("")
    for deal in state["deals"]:
        labels = [card_label(c) for c in stack_at(state, deal)]
        rows.append(f"  {deal:<8}: " + " ".join(labels) if labels else f"  {deal:<8}: (empty)")
    rows.append("")
    discarded = sum(1 for c in state["cards"] if state["on"].get(c) == "discard")
    rows.append(f"  discard : {discarded} / {len(state['cards'])}")
    return "\n".join(rows)


def apply_action(state, action: str):
    tokens = re.findall(r"[\w-]+", action)
    if not tokens:
        return
    op, *args = tokens
    if op == "start-dealing":
        state["phase"] = "dealing"
    elif op == "finish-dealing":
        state["phase"] = "idle"
    elif op == "deal-card":
        c, _from, _fromdeal, to, _tableau = args
        state["on"][c] = to
        state["in_play"].add(c)
    elif op in ("move-to-card", "move-to-tableau"):
        c, _from, to = args[0], args[1], args[2]
        state["on"][c] = to
    elif op == "start-collecting-deck":
        state["phase"] = "collecting"
    elif op in ("collect-card", "finish-collecting-deck"):
        c = args[0]
        state["on"][c] = "discard"
        state["in_play"].discard(c)
        if op == "finish-collecting-deck":
            state["phase"] = "idle"


def parse_plan(path: Path):
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("instance")
    ap.add_argument("plan")
    ap.add_argument("--html", help="write HTML slideshow")
    args = ap.parse_args()

    state = parse_instance(Path(args.instance))
    actions = parse_plan(Path(args.plan))

    frames = [render(state, 0, "(initial state)")]
    for i, a in enumerate(actions, start=1):
        apply_action(state, a)
        frames.append(render(state, i, a))

    if args.html:
        css = ("body{font-family:monospace;background:#222;color:#eee;}"
               "pre{background:#111;padding:1em;border-radius:6px;}"
               ".frame{display:none;} .frame.active{display:block;}"
               "button{font-size:1em;padding:.3em .8em;margin:.2em;}")
        js = ("let i=0,n=document.querySelectorAll('.frame').length;"
              "function show(k){document.querySelectorAll('.frame').forEach((f,j)=>"
              "f.classList.toggle('active',j===k));"
              "document.getElementById('idx').textContent=k+'/'+(n-1);}"
              "function step(d){i=Math.max(0,Math.min(n-1,i+d));show(i);}"
              "document.addEventListener('keydown',e=>{"
              "if(e.key==='ArrowRight'||e.key==='j')step(1);"
              "if(e.key==='ArrowLeft'||e.key==='k')step(-1);});"
              "show(0);")
        body = "\n".join(
            f"<div class='frame{' active' if k == 0 else ''}'><pre>{f}</pre></div>"
            for k, f in enumerate(frames)
        )
        html = (f"<!doctype html><html><head><meta charset='utf-8'>"
                f"<title>Spider plan</title><style>{css}</style></head><body>"
                f"<h2>Spider plan: {args.plan}</h2>"
                f"<button onclick='step(-1)'>&laquo; prev</button>"
                f"<button onclick='step(1)'>next &raquo;</button>"
                f"<span id='idx'></span><br>{body}<script>{js}</script></body></html>")
        Path(args.html).write_text(html)
        print(f"wrote {args.html} ({len(frames)} frames)", file=sys.stderr)
    else:
        for f in frames:
            print(f)
            print("-" * 40)


if __name__ == "__main__":
    main()
