# Respuesta a CORRECCION-B1-SUMMARIES-20260907

**De:** Equipo Remoto 48 GB · **Fecha:** 2026-09-07 · Recibido y aplicado. Gracias por el catch.

## 1. B1 — corregido (aditivo)
Sin reconciliación pendiente: el valor oficial de `llama3.1:8b` es **baseline 0.4876 / kb_rag 0.5075** (CSV
re-puntuado). El 0.4959/0.5491 venía del `summary.json` pre-fix (obsoleto). Actualizado en
`remote_48g/INVESTIGACION-B1-B4.md`. Ya lo habíamos aplicado así al `.md` canónico (commit `38b20da`).

## 2. `rescore_saved.py` extendido
Ahora, además del CSV, reescribe:
- **`detailed_results.json`**: `f1/precision/recall` de cada fila desde `metrics.overall` (elimina la
  inconsistencia interna que os hizo tropezar en B1).
- **`benchmark_summary.json`**: regenera `f1/precision/recall` por modelo como media del CSV corregido.

Re-ejecutado sobre las **8 corridas** del equipo remoto. Backups `.bak_prescore` en cada artefacto.

## 3. Aviso — interacción con el patch de nemotron
Detectamos (y corregimos) que el re-score **revertía el patch de `nemotron-mini:4b`**: el patch de los 7
registros (fallo de contexto batch) sólo tocaba el CSV, no `detailed_results.json`, así que el rescore los
volvía a leer como vacíos. **`patch_nemotron_failed.py` ahora actualiza también `detailed_results.json`**
(matchea por `record_id`, idempotente). nemotron queda estable en **baseline 0.2259, 0 failed** en CSV,
detailed y summary. Lección: cualquier corrección puntual debe tocar CSV **y** detailed, o el rescore la pisa.

## 4. §4.7 — Modelos del estudio con capacidad `thinking` (`ollama show`)

| Modelo | ¿capacidad thinking? | Estado en el estudio |
|:---|:--:|:---|
| gemma4:31b | ✅ | corrió thinking ON (P1, N=15) |
| gemma4:31b-mlx | ✅ | `think=False` (en `_THINKING_DISABLED_MODELS`) |
| gemma4:12b-mlx | ✅ | `think=False` (fix + re-run) |
| gemma4:latest | ✅ | corrió thinking ON (P4 ablación) |
| qwen3:8b | ✅ | `think=False` (fix + re-run limpio) |
| deepseek-r1:1.5b | ✅ | corrió thinking ON (P3) |
| gpt-oss:20b | ✅ | corrió thinking ON (P2) |
| llama3.1:8b, mistral-nemo, nuextract, nemotron-mini:4b | ❌ | sin thinking (no afectados) |

**qwen3:14b/32b/latest:** siguen en `_QWEN3_THINKING_MODELS` pero **NO participan en el estudio** (cero filas en
cualquier CSV) → sin impacto.

**Implicación (para decisión del equipo/autor):** 5 modelos capaces corrieron con thinking ON y **no** fueron
re-evaluados con thinking OFF: `gemma4:31b`, `gemma4:latest`, `deepseek-r1:1.5b`, `gpt-oss:20b`
(+`gemma4:31b-cloud`, cloud). Por la lección de qwen3 (thinking OFF ~+4pp y menos vacíos en NER), sus cifras
podrían estar subestimadas. Enumerados aquí; la decisión de re-correrlos con `think=False` excede el alcance
cerrado y queda a criterio del autor.

## 5. Confirmado de vuestro lado
ANOVA conjunto (14 modelos, F=36.3696, p=1.4321e-164) y re-score de las 3 legacy: recibido. Nuestros CSV ahora
comparten la misma convención; los summary/detailed regenerados ya no contradicen al CSV.
