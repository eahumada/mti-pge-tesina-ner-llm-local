#!/bin/bash
set -u
cd "$(dirname "$0")"
PY=./venv/bin/python
DRIVER_PID="${1:-}"
log(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
if [ -n "$DRIVER_PID" ]; then
  log "gpt-oss: esperando fin del driver (PID $DRIVER_PID, P3->P4)..."
  while kill -0 "$DRIVER_PID" 2>/dev/null; do sleep 30; done
  log "driver finalizado."
fi
log "=== gpt-oss:20b (P2 completar) INICIO ==="
$PY src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/excluidos_n120_REMOTO \
  --models gpt-oss:20b \
  --batch-size 3 --num-workers 6 --resume \
  >> results/excluidos_n120_REMOTO/run_console.log 2>&1
log "=== gpt-oss:20b FIN (rc=$?) ==="
