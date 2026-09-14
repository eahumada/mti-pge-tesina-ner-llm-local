# Encargo de re-corridas — Equipo 48 GB
**Creado:** 2026-09-14 · **Por:** Antigravity (coordinación) · **Basado en:** hallazgos del autor

> **Leer CURRENT-TASKS.md antes de empezar.** Escribir entrada en §3.bis al iniciar cada tarea,
> actualizarla al terminar. Trabajar en `main`. Commitear y pushear al terminar cada corrida.

---

## Contexto: hallazgos que motivan este encargo

### §F175 — corregido (criterio de exclusión f1==0 erróneo)
El criterio `f1==0 OR fallback` mezclaba tres cosas distintas. Con el criterio estricto
(`tp+fp==0 AND fallback`) el efecto del RAG pasa de +13,71 a **+13,04**, y nueve modelos no
cambian nada. De los 20 ceros de `nemotron-mini`, 18 son fallos del modelo (extrajo entidades y
erró todas), **no averías**. La conclusión 1 se sostiene. §F174 (+10,40) se sostiene íntegro.

### R2 — hallazgo nuevo: variabilidad no declarada
Dos corridas con modelo, corpus, semilla 42, temperatura 0,1, max_tokens y prompt **idénticos**
dieron **64,05 y 66,76 de F1** en la misma celda. El estudio entero es de una sola pasada:
ninguna cifra publicada tiene barra de error conocida. **Es lo primero que pregunta un tribunal.**

---

## Tabla de re-corridas

| ID | Qué | Coste estimado | Arregla |
|---|---|---|---|
| **R1** | Variantes 2×2 × 5 semillas, N=15 y N=120 | 45 min (N=15) + 6-7 h (N=120) | §5.2, Tabla 5, §6.1, conclusión 2 |
| **R2** | Barra de error del titular (13 modelos × 5 semillas × N=120) | 8-10 h, nocturno | Tabla 7 |
| **R3** | Instrumentación: respuesta cruda íntegra, 2 columnas, reintento declarado | Solo código | Auditabilidad futura |
| **R4** | Corpus N=30 en inglés | 2-3 h | No recomendado (a 16 días de defensa) |

---

## R1 — Variantes 2×2 con 5 semillas (PRIORITARIA)

### Objetivo
Medir el efecto real del idioma del prompt (español vs inglés) y del few-shot (ZS vs FS),
con intervalo de confianza. El experimento actual es N=15 todo en inglés — nunca fue el
experimento correcto para medir el efecto del idioma.

### Comandos

**Fase 1 — N=15 (validación rápida, ~45 min):**
```bash
cd repos/ner-llm-entity-benchmark
source venv/bin/activate

for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models gemma4:latest \
    --ablation \
    --data-file data/kleptotrace_balanced_15.json \
    --seed $SEED \
    --num-workers 4 \
    --results-dir results/variantes_5semillas_n15_REMOTO/seed_${SEED}
done
```

**Fase 2 — N=120 (resultado principal, ~6-7 h):**
```bash
for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models gemma4:latest \
    --ablation \
    --data-file data/benchmark_balanced_120.json \
    --seed $SEED \
    --num-workers 4 \
    --results-dir results/variantes_5semillas_n120_REMOTO/seed_${SEED}
done
```

### Verificación tras cada semilla
```bash
python3 tools/verificar_corrida.py results/variantes_5semillas_n15_REMOTO/seed_42
# failed == 0 obligatorio; ablation = True en run_config.json
```

### Entregables
- `results/variantes_5semillas_n15_REMOTO/seed_{42,123,456,789,1024}/`
- `results/variantes_5semillas_n120_REMOTO/seed_{42,123,456,789,1024}/`
- Cada directorio: `benchmark_results.csv`, `detailed_results.json`, `run_config.json`, `benchmark.log`

---

## R2 — Barra de error del titular (NOCTURNA)

### Objetivo
Cuantificar la variabilidad del F1 por modelo en N=120 con 5 semillas distintas.
Permite reportar el F1 como `μ ± σ` en la Tabla 7.

### Comandos
```bash
MODELS="gemma4:31b-cloud gemma4:31b-mlx gemma4:12b-mlx gemma4:latest \
        qwen3:8b gpt-oss:20b mistral-nemo:latest llama3.2:latest \
        llama3.1:8b nemotron-mini:4b deepseek-r1:1.5b"

for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models $MODELS \
    --rag-study \
    --rag-mode kb_combined \
    --data-file data/benchmark_balanced_120.json \
    --seed $SEED \
    --num-workers 4 \
    --max-tokens 4096 \
    --results-dir results/barras_error_n120_REMOTO/seed_${SEED}
done
```

> ⚠️ **Lanzar por la noche.** ETA ~8-10 h. Usar `caffeinate -dimsu` para evitar suspensiones.
> Usar `--resume` si se interrumpe.

### Entregables
- `results/barras_error_n120_REMOTO/seed_{42,123,456,789,1024}/`
- Incluir `detailed_results.json` en cada directorio (ya no está en `.gitignore`)

---

## R3 — Instrumentación (solo código, no requiere GPU)

### Objetivo
Que cada corrida futura guarde la **respuesta cruda íntegra** del modelo y el número real
de reintentos, en dos columnas adicionales del CSV.

### Cambios en `src/evaluator.py` o `src/worker.py`
Añadir al CSV de salida:
- `raw_response` — respuesta cruda completa del modelo (antes de parsear)
- `retry_count` — número de reintentos efectivos (0 = éxito en el primer intento)

Estos datos permiten:
1. Auditar casos de `parse_method='fallback'` sin re-inferir
2. Diagnosticar variabilidad (R2) a nivel de respuesta individual
3. Reproducir métricas futuras sin repetir la inferencia

### Sin re-corridas
Este cambio solo aplica a corridas futuras. Las corridas existentes no se rehacen.

---

## R4 — Corpus N=30 en inglés (NO RECOMENDADO)

**Recomendación del autor: no correr.** A 16 días de la defensa oral, el coste (2-3 h) no
justifica el beneficio, y el resultado podría abrir preguntas que el tiempo no permite responder.

Si el autor autoriza explícitamente, usar:
```bash
python3 src/main.py \
  --models gemma4:31b gemma4:31b-mlx \
  --rag-study \
  --rag-mode kb_combined \
  --data-file data/kleptotrace_augmented_30_en.json \
  --seed 42 \
  --results-dir results/n30_english_REMOTO
```

---

## Protocolo de entrega

1. `git pull` antes de empezar
2. Escribir entrada en `CURRENT-TASKS.md §3.bis.20` (R1) y `§3.bis.21` (R2)
3. Al terminar cada corrida: `python3 tools/verificar_corrida.py <directorio>`
4. `failed == 0` obligatorio. Si hay fallos, documentarlos antes de continuar
5. `git add results/<dir>/ && git commit -m "feat(remoto): R1/R2 semilla N"`
6. `git push`
7. Actualizar entrada en `CURRENT-TASKS.md` con F1 obtenido y estado final

---

## Orden de ejecución recomendado

1. **Hoy:** R1 Fase 1 (N=15, 45 min) — validar que el pipeline produce resultados coherentes
2. **Esta noche:** R1 Fase 2 (N=120, 6-7 h) en paralelo con R3 (código)
3. **Noche siguiente:** R2 (barra de error, 8-10 h)
4. R4: solo si el autor lo autoriza explícitamente
