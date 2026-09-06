# Resultados parciales — Equipo Remoto 48 GB

**Fecha del corte:** 2026-09-06 09:32 (actualización; ver historial abajo)
**Equipo:** Remoto 48 GB RAM (Claude Code)
**Encargo:** `PROMPT-EQUIPO-REMOTO-48GB.md` / artefacto de ejecución (4 tareas)
**Rama:** `sesion/revision-final-20260905`
**Entregables:** `remote_48g/results/`

> Reporte de **progreso parcial** solicitado por el equipo de desarrollo principal. Las corridas siguen en
> ejecución al momento del corte; este documento se actualizará al cierre de cada tarea.

---

## Verificaciones previas (todas OK)

| Comprobación | Obtenido | Esperado |
|:---|:--:|:--:|
| `kleptotrace.json` | 15 | 15 ✓ |
| `benchmark_balanced_120.json` | 120 | 120 ✓ |
| `persons.json` | 3605 | 3605 ✓ |
| `organizations.json` | 1848 | 1848 ✓ |
| `augmented_persons.json` | 12000 | 12000 ✓ |

Diccionarios **no regenerados** (snapshot 27-jul respetado). Anti-suspensión `caffeinate -dimsu` activo — sin
suspensiones. Todos los modelos ya locales (cero `pull`).

---

## Estado por tarea

| Tarea | Estado | Filas | Tasa de fallo |
|:---|:---|:--:|:--:|
| **P1** `gemma4:31b` N=15 | ✅ COMPLETADA | 30/30 | **0** |
| **P2** `sonct988/gemma4-26b…` N=120 | ✅ COMPLETADA | 240/240 | **0** |
| **P2** `gpt-oss:20b` N=120 | ⏳ encolado (fix aplicado) | 0 | — |
| **P3** principal N=120 (7 modelos) | ▶️ EN CURSO | 1137/1680 (~68%) | 0 hasta ahora |
| **P4** ablación de prompts | ⏳ en cola | 0 | — |
| **Re-corrida afectados** `gemma4:12b-mlx` + `qwen3:8b` | ⏳ encolada (fix thinking) | 0 | — |

---

## Cifras validadas

### P1 — `gemma4:31b` sobre N=15 (`--rag-mode entities`)
Desbloquea la fila de la Tabla 2 que citaba **F1 = 67,83 %** sin dato crudo.

| Condición | F1 | Precisión | Recall | Alucinación |
|:---|:--:|:--:|:--:|:--:|
| baseline | 0.6912 | 0.5883 | 0.8680 | 0.16 % |
| rag_enhanced | 0.6391 | 0.6080 | 0.8119 | 0 % |

- **VRAM:** 18,8 GB → el modelo de 19 GB **cupo** (imposible en 16 GB).
- **Tasa de fallo:** 0/30 (`parse_method`: 29 `direct_json` + 1 `fallback`; ningún `failed`).

### P2 — `sonct988/gemma4-26b-a4b-it-q4km-256k` sobre N=120 (`--rag-mode kb_combined`)
Recupera 1 de los 2 modelos excluidos por RAM → estudio de **12 a 13 modelos**.

| Condición | F1 | Precisión | Recall |
|:---|:--:|:--:|:--:|
| baseline | 0.5627 | 0.5233 | 0.7171 |
| kb_rag | 0.5964 | 0.5297 | 0.7608 |

- **Tasa de fallo:** 0/240.

---

## Incidencia resuelta — enrutado de `gpt-oss:20b`

`gpt-oss:20b` (segundo modelo excluido) **falló entero** por un **bug de enrutado**, no por RAM:
`src/providers/factory.py:46` mandaba todo `gpt-*` a `OpenAIProvider`, pero `gpt-oss:20b` es Ollama local.

```
Error: OpenAIProvider.extract_entities() got an unexpected keyword argument 'rag_context'
```

**Fix aplicado (aprobado por el autor):** la regla `gpt-*` ahora excluye nombres con tag Ollama (`:`), de
modo que `gpt-oss:20b` rutea a `OllamaProvider` y `gpt-4o`/`gpt-4` siguen en OpenAI. Backup:
`factory.py.bak_gptoss_routing_20260906`. Re-corrida de `gpt-oss:20b` **encolada tras P3/P4** (serialidad de
modelos locales) con `--resume` sobre el mismo `results/excluidos_n120_REMOTO/`. Al completarse, el estudio
llegaría a **14 modelos**.

> Nota para el equipo principal: AGENTS.md §8.2 clasifica `gpt-oss:20b` como «Local/Active», lo que
> contradecía la fila `gpt-*→OpenAI` de esa misma tabla. Conviene reflejar el fix en AGENTS.md.

---

## Progreso de P3 (detalle)

Al corte 09:28: **1137/1680 (~68%)**, tasa de fallo 0.
- ✅ Completos válidos (240/240): `mistral-nemo`, `nuextract`, `qwen3:8b`* (ver aviso), `gemma4:12b-mlx`* (inválido).
- ▶️ `llama3.1:8b`: baseline 87/120.
- ⏳ Faltan: `llama3.1:8b` kb_rag, `nemotron-mini:4b`, `deepseek-r1:1.5b`.

- **Ritmo:** ~150 filas/h en 48 GB (vs ~2 filas/h en la máquina de 16 GB; proyección local ~518 h ≈ 21 días).
- **ETA P3:** ≈ 4 h; luego P4, re-corrida de `gpt-oss` y re-corrida de afectados.

## 🔴 Aviso: bug thinking en esta corrida P3 (ALERTA-EQUIPO-REMOTO-20260906)

Recibida vuestra alerta. **Confirmado en los datos de P3** (corrida con código previo al fix):

| Modelo (P3) | recall=0 | F1 medio | Veredicto |
|:---|:--:|:--:|:---|
| `gemma4:12b-mlx` baseline | 66/120 | 0.27 | ❌ inválido (respuestas vacías) |
| `gemma4:12b-mlx` kb_rag | 94/120 | 0.11 | ❌ inválido |
| `qwen3:8b` baseline | 15/120 | 0.45 | ⚠️ thinking off (bug 2) |
| `qwen3:8b` kb_rag | 27/120 | 0.44 | ⚠️ thinking off |
| `mistral-nemo` baseline (control) | 3/120 | 0.45 | ✅ sano |

El fix (`ollama_provider.py`, commit `743054d`) ya está en el árbol, pero **P3 corre con el código viejo
cargado en memoria** → esos 2 modelos no se salvan en esta corrida. Los otros 5 no usan *thinking*: válidos.

**Acción tomada (opción §4.2 del alerta, aprobada por el autor):** dejar P3 terminar y **re-correr solo
`gemma4:12b-mlx` + `qwen3:8b`** con el fix en `results/afectados_thinking_n120_REMOTO/` (encolado tras
gpt-oss). Verificado en código: `gemma4:12b-mlx`→`think=False`, `qwen3:8b`→`think=True`, `think` como kwarg
de primer nivel. Aplicaremos vuestra verificación §4.3 (recall=0 residual) antes de entregar.

---

## Protocolo respetado

- `--results-dir` explícito en todas las corridas (evita reinicio silencioso, trampa 01).
- `--rag-mode kb_combined` en N=120, `entities` en N=15 (comparabilidad, trampa 02).
- Un modelo local a la vez (serialidad, trampa 06); cloud no aplica (todos locales).
- Verificación de tasa de fallo tras cada corrida antes de dar cifras por buenas (trampa 04).
- Coordinación en `CURRENT-TASKS.md §3.bis` mantenida al día.

---

## Entregables incluidos en este push

- `remote_48g/results/gemma4_31b_n15_REMOTO/` — P1 completa (CSV, JSON, statistical_report.md, log, config).
- `remote_48g/results/excluidos_n120_REMOTO/` — P2 sonct988 completa.
- `remote_48g/results/benchmark_n120_REMOTO/` — P3 **snapshot parcial** (checkpoint, config, log). Se
  completará al cierre.

---

## Actualización 2026-09-06 10:04 — cloud en marcha + P3 casi completo

### `gemma4:31b-cloud` N=120 (tarea nueva §3.bis.6) — EN CURSO, en paralelo
- **Progreso:** 153/240 · **tasa de fallo 0/153 (0.0%)** · 0× HTTP 429 · 0× 402.
- `baseline` completo (120/120, todo `direct_json`); `kb_rag` 33/120.
- **Rate limit aplicado desde el inicio:** `--num-workers 1 --max-workers 1 --request-delay 3.0`.
  La corrida previa de este modelo fallaba al 79% por cuota; con el límite va a **0%**.
- Corre **en paralelo** con la cadena local, sin consumir RAM local. Sumará el **10º modelo** al ANOVA.

### P3 principal N=120 — 1632/1680 (~97%)
- Solo falta `deepseek-r1:1.5b` kb_rag (45 filas).
- **Fallos:** 8, todos en `nemotron-mini:4b_baseline` (6,7% de ese grupo; sin *thinking*, residual). Resto 0.
- Recordatorio: `gemma4:12b-mlx` y `qwen3:8b` de P3 son **inválidos** (bug thinking) — se re-corren aparte con el fix.

### Cola restante
Local (serial): P3 (termina ya) → P4 → gpt-oss → afectados (`gemma4:12b-mlx`, `qwen3:8b`).
Cloud (paralelo): `gemma4:31b-cloud` (~1 h para 240).

---

## Actualización 2026-09-06 12:43 — gpt-oss cerrado, afectados y nemotron en marcha

### `gpt-oss:20b` N=120 — ✅ COMPLETADO (fix de routing)
- 240/240 · **fallo 0** (166 `direct_json` + 74 `fallback`, recuperación blanda). F1 baseline 0.4467 / kb_rag 0.3419.
- Confirmado end-to-end el fix de enrutado (`gpt-*` con `:` → Ollama). Recupera el modelo que antes fallaba entero.

### Re-corrida de afectados (bug thinking) — ▶️ EN CURSO
- `gemma4:12b-mlx` + `qwen3:8b` con el fix `743054d`, en `results/afectados_thinking_n120_REMOTO/`.
- Avance rápido (gemma4:12b-mlx ~111/120 con `think=False`). Reemplazará los datos inválidos de P3.

### Re-corrida `nemotron-mini:4b` — ▶️ EN CURSO (en paralelo)
- **Motivo:** en P3, `nemotron-mini:4b_baseline` tuvo **8 respuestas vacías** (`failed`), esporádicas
  (no correlacionan con longitud: fallidos mediana 1471 chars vs OK 1856; procesó bien uno de 8813).
  No es thinking (el modelo no lo tiene). Se re-corre para limpiar esos 8 antes del ANOVA.
- Dir: `results/nemotron_rerun_n120_REMOTO/`.

### Observación mistral-nemo (sin acción)
- `kb_rag` sube a 69 `fallback` (vs 9 baseline) pero recall=0 sigue en 4: el RAG le altera el formato de
  salida, el parser de respaldo lo rescata. Benigno; se documenta.

### Estado de modelos para el ANOVA
Válidos y completos: sonct988, gpt-oss:20b, gemma4:31b-cloud, + 5 de P3 (llama3.1, mistral-nemo, nuextract,
deepseek-r1, nemotron*). Pendientes de re-corrida (en curso): gemma4:12b-mlx, qwen3:8b, nemotron-mini*.
