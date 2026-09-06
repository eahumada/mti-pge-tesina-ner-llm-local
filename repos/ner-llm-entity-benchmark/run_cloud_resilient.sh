#!/bin/bash
# gemma4:31b-cloud N=120 resiliente: corre hasta completar o barrera de plan (402).
# En 429 (cuota temporal) espera y reintenta con --resume. Criterio de parada: fallo >10%.
set -u
cd "$(dirname "$0")"
set -a; source .setenv.sh 2>/dev/null; set +a
PY=./venv/bin/python
DIR=results/gemma4_31b_cloud_n120_REMOTO
LOG=$DIR/run_console.log
CSV=$DIR/benchmark_results.csv
mkdir -p "$DIR"
log(){ echo "[$(date '+%Y-%m-%d %H:%M:%S')] CLOUD: $*"; }
MAX_TRIES=48   # ~ hasta 48 reintentos
for i in $(seq 1 $MAX_TRIES); do
  log "intento $i/$MAX_TRIES (--resume)"
  $PY src/main.py \
    --data-file data/benchmark_balanced_120.json \
    --rag-study --rag-mode kb_combined \
    --results-dir "$DIR" \
    --models gemma4:31b-cloud \
    --batch-size 3 --num-workers 1 --max-workers 1 --request-delay 3.0 --resume \
    >> "$LOG" 2>&1
  rc=$?
  log "main.py rc=$rc"
  # 402 barrera de plan -> parar y avisar
  if grep -qiE "402|payment required|plan" "$LOG"; then
    log "🔴 HTTP 402 detectado — barrera de plan. PARANDO. Requiere intervención."
    break
  fi
  # completado? 240 filas esperadas (120 x 2 condiciones)
  if [ -f "$CSV" ]; then
    rows=$(($(wc -l < "$CSV") - 1))
    log "filas en CSV: $rows/240"
    if [ "$rows" -ge 240 ]; then log "✅ COMPLETADO ($rows filas)"; break; fi
  fi
  # 429 cuota temporal -> esperar y reintentar
  if grep -qiE "429|rate limit|quota|too many requests" "$LOG"; then
    log "⏳ HTTP 429 (cuota temporal) — esperando 15 min antes de reanudar"
    sleep 900
  else
    log "salida sin 402/429 y sin completar — esperando 3 min y reintentando"
    sleep 180
  fi
done
log "=== CLOUD FIN ==="
