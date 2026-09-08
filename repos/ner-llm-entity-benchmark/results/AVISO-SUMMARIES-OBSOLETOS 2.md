# ⚠️ AVISO — `benchmark_summary.json` y `statistical_report.md` están OBSOLETOS

**Fecha:** 2026-09-07

El **bug de scoring** (`evaluator.py`: una extracción vacía sobre gold no-vacío recibía `F1 = 1.0`) se
corrigió el 2026-09-06 y todas las corridas se **re-puntuaron sin re-inferir** con
`tools/rescore_saved.py`, que recalcula P/R/F1 desde los `tp/fp/fn` guardados.

**Esa herramienta reescribe únicamente `benchmark_results.csv`.**

Por tanto, en **todos** los directorios de `results/`:

| Artefacto | Estado |
|:---|:---|
| `benchmark_results.csv` | ✅ **Única fuente válida** de precision / recall / F1 |
| `benchmark_summary.json` | ❌ Obsoleto — cifras **pre-fix, infladas** |
| `statistical_report.md` | ❌ Obsoleto — mismo motivo |
| `confusion_matrix.json`, `acceptance_status.json` | ❌ Obsoletos |
| `detailed_results.json` | ⚠️ **Mixto**: `metrics.overall.tp/fp/fn` correctos, campo `f1` por fila **obsoleto** |

## Consecuencias prácticas

- **No citar** ninguna cifra de F1 tomada de un `summary` o de un `statistical_report.md` por corrida.
- Al promediar desde `detailed_results.json`, **recalcular desde `tp/fp/fn`**; nunca promediar el campo `f1`.
- El análisis conjunto vigente es **`results/ANALISIS_CONJUNTO_20260907/`** (14 modelos × 2 modos,
  F = 36.3696, p = 1.4321e-164), generado con `src/merge_and_analyze.py`, que **lee los CSV**.

Un incidente real por ignorar esto: la auditoría B1 del equipo remoto (`494dacf`) tomó 0.4959/0.5491 del
summary como «fuente primaria» de `llama3.1:8b` cuando el valor correcto es **0.4876/0.5075**. Ver
`CORRECCION-B1-SUMMARIES-20260907.md`.
