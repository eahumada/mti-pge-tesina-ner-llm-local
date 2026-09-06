# Resultados parciales — Equipo Remoto 48 GB

**Fecha del corte:** 2026-09-06 08:58 (actualización; corte previo 04:33)
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
| **P3** principal N=120 (7 modelos) | ▶️ EN CURSO | 870/1680 (~52%) | 0 hasta ahora |
| **P4** ablación de prompts | ⏳ en cola | 0 | — |

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

Al corte 08:58: **870/1680 (~52%)**.
- ✅ Completos (240/240): `gemma4:12b-mlx`, `mistral-nemo`, `qwen3:8b`.
- ▶️ `nuextract`: baseline 120 ✅, kb_rag 30/120.
- ⏳ Faltan: `llama3.1:8b`, `nemotron-mini:4b`, `deepseek-r1:1.5b`.

- **Ritmo:** ~154 filas/h en 48 GB (vs ~2 filas/h en la máquina de 16 GB; proyección local ~518 h ≈ 21 días).
- **ETA P3:** ≈ 5 h desde el corte; luego P4 y la re-corrida de `gpt-oss`.

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
