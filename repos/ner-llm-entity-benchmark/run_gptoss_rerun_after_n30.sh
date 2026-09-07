#!/bin/bash
set -u; cd "$(dirname "$0")"; set -a; source .setenv.sh 2>/dev/null; set +a
PY=./venv/bin/python; WAIT_PID="${1:-}"
log(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPTOSS-RERUN: $*"; }
if [ -n "$WAIT_PID" ]; then
  log "esperando fin de N30 (PID $WAIT_PID)..."
  while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 30; done
  log "N30 finalizado."
fi
TS=$(date "+%Y%m%d_%H%M%S"); DIR=results/gptoss_rerun_REMOTO; mkdir -p "$DIR"; LOG="$DIR/run_${TS}.log"
{ echo "=== gpt-oss:20b re-run completo — INICIO $(date '+%Y-%m-%d %H:%M:%S %Z') ==="
  echo "N=120 kb_combined · thinking ON · num_predict 4096 (evita truncacion) · batch3 workers6"
  echo "motivo: recall=0 oficial = artefacto de truncacion (ver DIAGNOSTICO-GPTOSS-20260907.md)"; } > "$LOG"
$PY src/main.py --data-file data/benchmark_balanced_120.json --rag-study --rag-mode kb_combined \
  --results-dir "$DIR" --models gpt-oss:20b --batch-size 3 --num-workers 6 --max-tokens 4096 \
  >> "$LOG" 2>&1
log "=== gpt-oss re-run FIN (rc=$?) ==="
