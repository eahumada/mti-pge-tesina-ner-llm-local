#!/bin/bash
# Re-corrida de modelos afectados por el bug thinking (gemma4:12b-mlx, qwen3:8b) con el fix ya aplicado.
# Espera a que termine el waiter de gpt-oss (que a su vez espera P3->P4). Serialidad: un modelo local a la vez.
set -u
cd "$(dirname "$0")"
PY=./venv/bin/python
WAIT_PID="${1:-}"
log(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
if [ -n "$WAIT_PID" ]; then
  log "afectados: esperando fin del waiter gpt-oss (PID $WAIT_PID)..."
  while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 30; done
  log "waiter gpt-oss finalizado."
fi
log "=== RE-CORRIDA afectados (gemma4:12b-mlx, qwen3:8b) INICIO ==="
mkdir -p results/afectados_thinking_n120_REMOTO
$PY src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/afectados_thinking_n120_REMOTO \
  --models gemma4:12b-mlx qwen3:8b \
  --batch-size 3 --num-workers 8 --resume \
  >> results/afectados_thinking_n120_REMOTO/run_console.log 2>&1
log "=== RE-CORRIDA afectados FIN (rc=$?) ==="
