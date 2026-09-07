#!/bin/bash
# Prueba think=OFF en 15 registros para los 5 modelos que corrieron thinking ON.
# Serial (un modelo local a la vez). Compara luego contra su think-ON existente.
set -u
cd "$(dirname "$0")"
set -a; source .setenv.sh 2>/dev/null; set +a
PY=./venv/bin/python
log(){ echo "[$(date '+%H:%M:%S')] TEST: $*"; }
mkdir -p results/test_nothink

# --- 3 modelos N=120 (subset 15, kb_combined) ---
for M in deepseek-r1:1.5b gpt-oss:20b ; do
  SAFE=$(echo "$M" | tr '/:' '__')
  log "=== $M INICIO ==="
  $PY src/main.py --data-file data/test15_balanced.json --rag-study --rag-mode kb_combined \
    --results-dir "results/test_nothink/$SAFE" --models "$M" --batch-size 3 --num-workers 4 \
    > "results/test_nothink/$SAFE.log" 2>&1
  log "=== $M FIN (rc=$?) ==="
done

# --- gemma4:31b (kleptotrace 15, entities, como P1) ---
log "=== gemma4:31b INICIO ==="
$PY src/main.py --data-file data/kleptotrace.json --rag-study --rag-mode entities \
  --results-dir results/test_nothink/gemma4_31b --models gemma4:31b --batch-size 3 --num-workers 4 \
  > results/test_nothink/gemma4_31b.log 2>&1
log "=== gemma4:31b FIN (rc=$?) ==="

# --- gemma4:latest (kleptotrace 15, ablation, como P4) ---
log "=== gemma4:latest INICIO ==="
$PY src/main.py --data-file data/kleptotrace.json --ablation \
  --results-dir results/test_nothink/gemma4_latest --models gemma4:latest --batch-size 3 --num-workers 4 \
  > results/test_nothink/gemma4_latest.log 2>&1
log "=== gemma4:latest FIN (rc=$?) ==="
log "=== TEST COMPLETO ==="
