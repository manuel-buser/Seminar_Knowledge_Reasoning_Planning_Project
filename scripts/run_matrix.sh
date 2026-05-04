#!/usr/bin/env bash
# Run the experimental matrix on a list of IPC instances.
#
# Usage:
#   ./run_matrix.sh opt p01 p03 p05 p07 p09 p11 p13 p15
#   ./run_matrix.sh sat p01 p03 p05 p07 p09
#
# - opt: runs {noaxioms,axioms} x {astar(blind()), astar(lmcut()/hmax())}
# - sat: runs --alias lama on both encodings
#
# Per-run budget: 5min wall + 4GB. Logs/plans land in KRP_Project/runs/.
set -o pipefail

TRACK="$1"; shift
INSTANCES=("$@")

KRP=/home/buser/KRP_Project
FD_DIR=/home/buser/planopt/planopt-hs25/demo
IPC_DIR="$FD_DIR/ipc/spider-${TRACK}18-strips"
PREP="$KRP/scripts/ipc_to_axioms.py"

NOAX_DOM="$KRP/Spider_NoAxioms/domain.pddl"
AX_DOM="$KRP/Spider_Axioms/domain.pddl"
NOAX_INST_DIR="$KRP/Spider_NoAxioms/instances"
AX_INST_DIR="$KRP/Spider_Axioms/instances"
RUNS="$KRP/runs"

mkdir -p "$NOAX_INST_DIR" "$AX_INST_DIR" "$RUNS"

# FD time/memory limits (per run)
LIMITS=(--overall-time-limit 300 --overall-memory-limit 4096)

if [[ "$TRACK" == "opt" ]]; then
    # 4 cells: noaxioms-blind, noaxioms-lmcut, axioms-blind, axioms-hmax
    CONFIGS=(
        "noaxioms:blind:astar(blind())"
        "noaxioms:lmcut:astar(lmcut())"
        "axioms:blind:astar(blind())"
        "axioms:hmax:astar(hmax())"
    )
elif [[ "$TRACK" == "sat" ]]; then
    CONFIGS=(
        "noaxioms:lama:--alias-lama"
        "axioms:lama:--alias-lama"
    )
else
    echo "first arg must be 'opt' or 'sat'" >&2
    exit 1
fi

cd "$FD_DIR"

for inst in "${INSTANCES[@]}"; do
    src="$IPC_DIR/${inst}.pddl"
    if [[ ! -f "$src" ]]; then
        echo "MISSING: $src" >&2
        continue
    fi
    # Prepare instances (idempotent)
    cp -f "$src" "$NOAX_INST_DIR/${TRACK}_${inst}.pddl"
    python3 "$PREP" "$src" -o "$AX_INST_DIR/${TRACK}_${inst}.pddl"

    for cfg in "${CONFIGS[@]}"; do
        IFS=':' read -r enc heur search <<<"$cfg"
        if [[ "$enc" == "noaxioms" ]]; then
            domain="$NOAX_DOM"; inst_path="$NOAX_INST_DIR/${TRACK}_${inst}.pddl"
        else
            domain="$AX_DOM";   inst_path="$AX_INST_DIR/${TRACK}_${inst}.pddl"
        fi
        log="$RUNS/${enc}_${TRACK}_${inst}_${heur}.log"
        plan="$RUNS/${enc}_${TRACK}_${inst}_${heur}.plan"
        echo "== $enc $TRACK $inst $heur =="
        if [[ "$search" == "--alias-lama" ]]; then
            ./fast-downward.py "${LIMITS[@]}" --alias lama \
                --plan-file "$plan" "$domain" "$inst_path" 2>&1 | tee "$log" \
                | grep -E "^(Plan cost|Plan length|Expanded|Generated|Search time|Total time|Translator|search exit)" || true
        else
            ./fast-downward.py "${LIMITS[@]}" \
                --plan-file "$plan" "$domain" "$inst_path" \
                --search "$search" 2>&1 | tee "$log" \
                | grep -E "^(Plan cost|Plan length|Expanded|Generated|Search time|Total time|Translator|search exit)" || true
        fi
        echo
    done
done
