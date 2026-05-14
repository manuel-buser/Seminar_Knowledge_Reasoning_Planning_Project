# Representative reconstructed prompts

Exact prompts were not preserved during the sessions. The reconstructions
below are representative, not verbatim, they reflect what I asked for at the
granularity I typically use, inferred from the resulting code. Referenced
from [AI_USAGE.md](AI_USAGE.md).

## 1. For [scripts/extract_stats.py](scripts/extract_stats.py), FD log parser

> *"I have Fast Downward log files in `runs/` named*
> *`<encoding>_<track>_<instance>_<heuristic>.log` (e.g.*
> *`noaxioms_opt_p01_lmcut.log`). Write me a Python script that parses one or*
> *more such logs and extracts: translator stats (variables, derived variables,*
> *operators, axioms, task size, mutex groups), search status (solved /*
> *timeout / out-of-memory), plan cost, plan length, expanded states, search*
> *time, peak memory. Output as CSV with one row per log. Filename should be*
> *parseable into encoding / track / instance / heuristic columns."*

## 2. For [scripts/build_report.py](scripts/build_report.py), report generator

> *"Take the CSV from `extract_stats.py` and build a markdown comparison*
> *report. I want: a coverage table per (encoding, heuristic), a*
> *translator-stats table showing the axioms-vs-no-axioms ratios, an*
> *optimal-search head-to-head table (same instance, same cost, two*
> *heuristics, speedup column), and a LAMA satisficing table with*
> *first-solution time and best cost found. Auto-regenerable: re-running the*
> *script on updated logs should overwrite the report cleanly."*

## 3. For [scripts/spider_viz.py](scripts/spider_viz.py), plan visualiser

> *"I have a PDDL Spider instance and a plan file from Fast Downward. Write a*
> *Python script that reads both, simulates the plan action by action (moves*
> *between piles, dealing, collecting completed runs), and renders the*
> *gameplay. Two output modes: standalone HTML with step-through controls, and*
> *a PNG frame grid. Card faces should show suit + rank."*

## 4. For [scripts/ipc_to_axioms.py](scripts/ipc_to_axioms.py), instance converter

> *"I have the IPC Spider instances written for the no-axioms domain. The*
> *axioms version uses the same instance format but doesn't need the `make-*`*
> */ `currently-updating-*` initial facts and references a different domain*
> *name. Write me a small idempotent script that converts an IPC instance*
> *file to the axioms format."*

## 5. PDDL debugging, typical interaction shape

A *class* of prompts rather than a single one; I used variants of it many
times while getting the axiomatic domain past the Fast Downward translator:

> *"Here is `Spider_Axioms/domain.pddl` and the Fast Downward translator*
> *output (pasted). It rejects the file with `<error message>`. What is the*
> *syntactic problem? Do not change the semantics of my axioms, only the*
> *PDDL syntax needed to make the translator accept the file."*

Every proposed patch was reviewed before being applied, and the translator
was re-run to confirm the fix.
