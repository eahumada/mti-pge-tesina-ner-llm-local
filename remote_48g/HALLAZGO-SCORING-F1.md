# 🔴 Hallazgo — bug de scoring que infla F1 (extracción vacía → 1.0)

**Fecha:** 2026-09-06 · **De:** Equipo Remoto 48 GB · **Severidad:** alta (afecta cifras del estudio)
**Decisión del autor:** documentar y avisar; **no** modificar el scorer (cambiaría todas las cifras históricas).

---

## Qué pasa

`src/evaluator.py:126-134`, en el cálculo de métricas *overall* por registro:

```python
overall_precision = tp/(tp+fp) if (tp+fp) > 0 else 1.0
overall_recall    = tp/(tp+fn) if (tp+fn) > 0 else 1.0
overall_f1        = 2*P*R/(P+R) if (P+R) > 0 else 1.0
if overall_tp == 0 and overall_fp == 0 and overall_fn == 0:
    overall_precision = overall_recall = overall_f1 = 1.0
```

Cuando el modelo **no extrae nada** en un artículo (respuesta vacía, o parse `fallback` que devuelve vacío),
no hay predicciones → `tp+fp = 0` → la precisión cae al **default 1.0**, y por la combinación de defaults el
registro termina puntuando **F1 = 1.0** en vez de penalizar las entidades gold no recuperadas.

**Ejemplo:** `real_mixed_64` tiene gold `Organizations: ['EFE']`. `nuextract:latest_kb_rag` extrajo vacío →
registrado **F1=1.0, P=0, R=0**. Debería ser ~0 (perdió EFE).

## Qué NO es

Distinto de los **4 artículos gold-vacío legítimos** (`real_mixed_22/76/102/103`): ahí F1=1.0 es correcto
(no hay nada que extraer y el modelo acierta al no inventar). Esos 4 se mantienen.

## Impacto cuantificado (N=120)

F1 ajustado = restando los falsos 1.0 (registros con F1=1.0 que NO son gold-vacío):

| Modelo | F1 registrado | F1 ajustado | Δ inflado | # registros |
|:---|--:|--:|--:|--:|
| `nuextract` kb_rag | 0.4323 | 0.2240 | **+0.208** | 25 |
| `nemotron-mini:4b` baseline | 0.3630 | 0.2130 | **+0.150** | 18 |
| `deepseek-r1:1.5b` kb_rag | 0.3394 | 0.2394 | +0.100 | 12 |
| `deepseek-r1:1.5b` baseline | 0.3400 | 0.2483 | +0.092 | 11 |
| `nemotron-mini:4b` kb_rag | 0.4399 | 0.3733 | +0.067 | 8 |
| `llama3.1:8b` kb_rag | 0.5491 | 0.5075 | +0.042 | 5 |
| `mistral-nemo` kb_rag | 0.4826 | 0.4576 | +0.025 | 3 |
| `qwen3:8b` kb_rag (P3, inválido) | 0.4425 | 0.4259 | +0.017 | 2 |
| `mistral-nemo` baseline | 0.4505 | 0.4338 | +0.017 | 2 |
| `nuextract` baseline | 0.4455 | 0.4288 | +0.017 | 2 |
| `gemma4:31b-cloud` kb_rag | 0.6268 | 0.6185 | +0.008 | 1 |
| `llama3.1:8b` baseline | 0.4959 | 0.4876 | +0.008 | 1 |

*(Ajuste conservador: coincide con la métrica micro del propio evaluator, F1=0 para extracción vacía.)*

## Por qué importa

- **No es uniforme.** Los modelos propensos a devolver vacío (parse `fallback`) se inflan mucho (+0.15 a +0.21);
  los fuertes, casi nada. **Sesga la comparación y comprime el ranking.**
- **Alcance:** afecta a **todas** las corridas con el mismo evaluator, incluida la de referencia 2026-09-01 y
  las cifras históricas del informe.

## Recomendación

Al recalcular el ANOVA definitivo, decidir explícitamente la convención para extracción vacía sobre gold
no-vacío (F1=0 es lo correcto). Si se corrige el scorer, **recomputar todas las corridas** y re-fusionar.
Mientras tanto, estas cifras registradas están **infladas para los modelos débiles** y no deben citarse como
absolutas sin esta nota.

---

## ✅ CORREGIDO (2026-09-06) — sin re-inferir

`evaluator.py:126-134` arreglado (default 0.0; F1=1.0 solo si `tp+fp+fn==0`). Los datos guardados se
**re-puntuaron desde los `tp/fp/fn` persistidos** (`detailed_results.json`) con `tools/rescore_saved.py`
— **no hizo falta re-ejecutar ningún modelo**. CSVs corregidos (backup `.bak_prescore`).

### F1 corregido definitivo (N=120, kb_combined salvo Tabla 2)

| Modelo | baseline | kb_rag | Fuente |
|:---|--:|--:|:---|
| `gemma4:31b-cloud` | 0.6238 | 0.6185 | cloud |
| `gemma4:12b-mlx` | 0.5618 | 0.5846 | afectados |
| `qwen3:8b` (think=false) | 0.4821 | 0.5146 | qwen3_nothink |
| `llama3.1:8b` | 0.4876 | 0.5075 | P3 |
| `mistral-nemo` | 0.4338 | 0.4576 | P3 |
| `nuextract` | 0.4288 | 0.2240 | P3 |
| `nemotron-mini:4b` | 0.2150 | 0.3712 | rerun (excluir 7 failed) |
| `deepseek-r1:1.5b` | 0.2483 | 0.2394 | P3 |
| `gpt-oss:20b` | 0.4384 | 0.3419 | excluidos |
| **Tabla 2 `gemma4:31b` N=15** | 0.6912 | 0.6391 | P1 |
| **Variación prompts** (gemma4:latest) | — | fs-es 0.7444 / zs-es 0.6843 / zs-en 0.6405 / fs-en 0.6332 | P4 |

Cambios mayores por la corrección: nuextract kb_rag 0.4323→0.2240, nemotron baseline 0.3630→0.2130,
deepseek 0.34→0.24. Modelos con parsing limpio casi no cambian.
