#!/bin/bash
# Driver secuencial equipo remoto 48 GB — P2, P3, P4 tras P1 (trampa 06: un modelo local a la vez)
set -u
cd "$(dirname "$0")"
PY=./venv/bin/python
P1_PID="${1:-}"
log(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# Esperar a que P1 (gemma4:31b N=15) termine
if [ -n "$P1_PID" ]; then
  log "Esperando fin de P1 (PID $P1_PID)..."
  while kill -0 "$P1_PID" 2>/dev/null; do sleep 30; done
  log "P1 finalizado."
fi

# --- P2: excluidos N=120 (kb_combined) ---
log "=== P2 INICIO ==="
mkdir -p results/excluidos_n120_REMOTO
$PY src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/excluidos_n120_REMOTO \
  --models gpt-oss:20b \
  --batch-size 3 --num-workers 6 \
  > results/excluidos_n120_REMOTO/run_console.log 2>&1
log "=== P2 FIN (rc=$?) ==="

# --- P3: benchmark principal N=120, 7 modelos (kb_combined) ---
log "=== P3 INICIO ==="
mkdir -p results/benchmark_n120_REMOTO
$PY src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/benchmark_n120_REMOTO \
  --models gemma4:12b-mlx qwen3:8b mistral-nemo:latest nuextract:latest \
           llama3.1:8b nemotron-mini:4b deepseek-r1:1.5b \
  --batch-size 3 --num-workers 8 \
  > results/benchmark_n120_REMOTO/run_console.log 2>&1
log "=== P3 FIN (rc=$?) ==="

# --- P4: ablacion prompts gemma4:latest ---
log "=== P4 INICIO ==="
mkdir -p results/ablacion_n15_REMOTO
$PY src/main.py \
  --data-file data/kleptotrace.json \
  --ablation \
  --results-dir results/ablacion_n15_REMOTO \
  --models gemma4:latest \
  --batch-size 3 --num-workers 4 \
  > results/ablacion_n15_REMOTO/run_console.log 2>&1
log "=== P4 FIN (rc=$?) ==="
log "=== CADENA COMPLETA ==="
