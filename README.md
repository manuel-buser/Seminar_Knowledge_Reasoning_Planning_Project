# Spider PDDL: Axioms vs No-Axioms

Project for the *Knowledge Representation* seminar HS25 at the University of Basel
(supervisor: Florian Pommerening).

## Overview

The IPC-2018 *Spider* PDDL domain models a variant of Spider
Solitaire. Movement and collection actions depend on cascading properties,
whether a card is movable, which tableau a card belongs to, that an
encoding could express as derived predicates. But because the IPC-2018 track
did it without axioms, the published domain instead simulates them with auxiliary
fluents (`currently-updating-*`, `make-movable`, `make-part-of-tableau`, …) and
a chain of zero-cost propagation actions that walks over the affected pile
after every real move.

This project rewrites the domain using PDDL axioms (`(:derived ...)`) and
evaluates both encodings on Fast Downward across the IPC-2018 instance set.
The two encodings should be plan-cost equivalent; the experimental questions
are what the axiom rewrite costs and saves in grounding size, search effort,
and wall-clock time, and which configurations of Fast Downward benefit most.

## Repository layout

```
.
├── Spider_NoAxioms/        published IPC-2018 encoding
│   ├── domain.pddl         conditional-effect machinery + propagation actions
│   ├── p01.pddl            quick check instance before letting the planner run on a bigger instance
│   └── instances/          opt_p01..p15 (8 instances) + sat_p01..p09 (5)
├── Spider_Axioms/          axiom-based rewrite
│   ├── domain.pddl         two derived predicates, no propagation actions
│   ├── i01.pddl            also quick check instance before letting the planner run on a bigger instance
│   └── instances/          mirrors of the no-axioms instances
├── scripts/
│   ├── run_matrix.sh       drives Fast Downward across the experimental matrix
│   ├── extract_stats.py    parses translator + search statistics from FD logs
│   ├── build_report.py     aggregates statistics into results/report.md
│   ├── lama_trajectory.py  extracts anytime LAMA solution trajectories
│   ├── ipc_to_axioms.py    converts IPC instance files to the axiom format
│   └── spider_viz.py       renders plan playbacks
├── runs/                   Fast Downward .log + .plan output, one pair per cell
├── results/
│   └── report.md           auto-built comparison report
```

## The two encodings

`Spider_NoAxioms/domain.pddl` is identical to the IPC-2018 release.[^1]
Each real action (`move-to-card`, `deal-card`, `start-collecting-deck`, …) sets
a `currently-updating-*` flag and plants a `make-*` marker on one card; a chain
of cost-0 actions then propagates the update along the affected pile while
every other action is blocked. This serialises the propagation and inflates
plan length, but can handle the domain without axioms.

`Spider_Axioms/domain.pddl` introduces two derived predicates and removes the
propagation machinery:

Both axioms are positively recursive in a single stratum (no negation in the
body, no cross-stratum dependency). Eight propagation actions, the
corresponding marker fluents, and `:conditional-effects` from the
`:requirements` line are dropped. The direct effects of the move, deal, and
collect actions are unchanged, which is what makes the two encodings
plan-cost equivalent on matched instances.

## Running the experiments

The experiments require Fast Downward.[^2] In this project the binary lives at
`/home/buser/planopt/planopt-hs25/demo/fast-downward.py`. A single cell:

```bash
./fast-downward.py \
    --plan-file runs/axioms_opt_p01_blind.plan \
    Spider_Axioms/domain.pddl Spider_Axioms/instances/opt_p01.pddl \
    --search "astar(blind())" \
    | tee runs/axioms_opt_p01_blind.log
```

The full matrix and the comparison report:

```bash
bash scripts/run_matrix.sh
python3 scripts/build_report.py > results/report.md
```

The matrix runs `{noaxioms, axioms} × {blind, informative-admissible}` on the
optimal track and `--alias lama` on the satisficing track, with a 5-minute,
4-GB budget per cell. Because Fast Downward's `lmcut` does not reliably handle
axioms in this build, the informative-admissible comparison uses `lmcut` on
the no-axioms encoding and `hmax` on the axiom encoding.

## Results in summary

Full numbers and per-instance breakdowns in [`results/report.md`](results/report.md).

- **Grounding size.** The axiom encoding produces 0.42–0.56× the grounded
  operators and 0.36–0.47× the task size of the no-axioms encoding,
  consistently across all 13 instances.
- **Optimal search, informative-admissible head-to-head.** On every solved
  instance (`p01`, `p03`, `p07`, `p09`, `p15`), `astar(hmax())` on the axiom
  encoding is 4–9× faster wall-clock than `astar(lmcut())` on the no-axioms
  encoding, and reports the same optimal plan cost.
- **Satisficing.** LAMA solves 5 of 5 satisficing instances on the axiom
  encoding versus 3 of 5 on the no-axioms encoding, and reaches the first
  solution faster on every instance solved by both.
- **Open coverage gap.** `p05`, `p11`, and `p13` time out in every optimal
  cell on both encodings.


[^1]: <https://github.com/aibasel/downward-benchmarks/blob/master/spider-opt18-strips/domain.pddl>
[^2]: <https://www.fast-downward.org/>
