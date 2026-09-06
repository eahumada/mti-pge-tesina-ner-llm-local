# Reporte completo — Equipo Remoto 48 GB

**Fecha:** 2026-09-06 16:46 · **Rama:** `sesion/revision-final-20260905` · **Entregables:** `remote_48g/results/`

Consolidación de todas las corridas del encargo (`PROMPT-EQUIPO-REMOTO-48GB.md` + `ADENDA-EQUIPO-REMOTO-20260906.md`).

---

## 1. Estado de las tareas

| # | Tarea | Estado | Fallo |
|--:|:---|:---|:--|
| P1 | `gemma4:31b` N=15 (`entities`) | ✅ | 0/30 |
| P2a | `sonct988/gemma4-26b` N=120 | ✅ | 0/240 |
| P2b | `gpt-oss:20b` N=120 (fix routing) | ✅ | 0/240 |
| P3 | principal N=120, 7 modelos | ✅ | 8/1680 (nemotron baseline) |
| P4 | ablación de prompts | ✅ | 0/60 |
| Nueva | `gemma4:31b-cloud` N=120 (rate limit) | ✅ | 0/240 |
| Fix | `gemma4:12b-mlx` re-run (thinking) | ✅ | 0/240 |
| Fix | `nemotron-mini:4b` re-run | ✅ | 7/240 (vacíos esporádicos inherentes) |
| Fix | `qwen3:8b` re-corrida limpia | ▶️ EN CURSO | — |

---

## 2. Resultados N=120 (F1 baseline / kb_rag) — fuente de verdad por modelo

| Modelo | baseline | kb_rag | Fuente | Nota |
|:---|--:|--:|:---|:---|
| `sonct988/gemma4-26b` | 0.5627 | **0.5964** | excluidos | recuperado por RAM; **lidera** |
| `gemma4:31b-cloud` | 0.6238 | 0.6268 | cloud | 10º modelo; rate limit |
| `gemma4:12b-mlx` | 0.5618 | 0.5929 | **afectados** | ✅ con fix thinking (P3 inválido: 0.27/0.11) |
| `gpt-oss:20b` | 0.4467 | 0.3419 | excluidos | fix routing |
| `llama3.1:8b` | 0.4959 | 0.5491 | P3 | RAG mejora |
| `mistral-nemo` | 0.4505 | 0.4826 | P3 | kb_rag sube fallback (RAG altera formato, benigno) |
| `nuextract` | 0.4455 | 0.4323 | P3 | |
| `nemotron-mini:4b` | 0.3650 | 0.4378 | **nemotron re-run** | excluir 7 `failed` (vacíos esporádicos del 4B) |
| `deepseek-r1:1.5b` | 0.3400 | 0.3394 | P3 | |
| `qwen3:8b` | *(pendiente)* | *(pendiente)* | **qwen3 limpio** | re-corrida en curso; NO usar la de afectados (cobertura 99/114) |

> **P3 `gemma4:12b-mlx` y `qwen3:8b` son INVÁLIDOS** (bug thinking previo al fix `743054d`). Usar las re-corridas.

---

## 3. Tabla 2 — `gemma4:31b` N=15 (`--rag-mode entities`)

| Condición | F1 | P | R | Alucinación |
|:---|--:|--:|--:|--:|
| baseline | 0.6912 | 0.5883 | 0.8680 | 0.16 % |
| rag_enhanced | 0.6391 | 0.6080 | 0.8119 | 0 % |

Desbloquea la fila que citaba F1=67,83 % sin dato crudo.

---

## 4. Ablación de prompts (P4, `gemma4:latest`, N=15)

| Config | F1 |
|:---|--:|
| **fs-es** (few-shot español) | **0.7444** |
| zs-es | 0.6843 |
| zs-en | 0.6405 |
| fs-en | 0.6332 |

Confirma: el español mejora; few-shot español es el óptimo. Regenera las 4 cifras que no existían en datos
(citadas 0.7169/0.6640/0.6482/0.5874).

---

## 5. Incidencias y correcciones

1. **Routing `gpt-oss:20b`** (`factory.py`): `gpt-*` iba a OpenAIProvider; ahora los nombres con `:` (tag Ollama)
   rutean a Ollama. `gpt-4o`/`gpt-4` intactos. Backup guardado.
2. **Bug thinking** (`ollama_provider.py`, fix `743054d` del equipo principal): `gemma4:12b-mlx`→`think=False`,
   `qwen3:8b`→`think=True` como kwarg de primer nivel. Verificado end-to-end.
3. **Rate limit cloud** (`main.py`): flags `--max-workers` + `--request-delay` (gate global). Con 1 worker + 3s:
   0× HTTP 429 (antes 79 % fallo). `gemma4:31b-cloud` recuperado.
4. **nemotron 7-8 `failed`:** vacíos esporádicos del 4B (no por longitud, no thinking). Inherente → excluir esas filas.
5. **qwen3 corrupción por reinicios:** reiniciar para "optimizar" concurrencia dejó cobertura incompleta
   (baseline 99/120). Corregido con re-corrida limpia en dir fresco, sin reinicios. **Aprendizaje:** no reiniciar
   corridas con checkpoint.

---

## 6. Protocolo cumplido

`--results-dir` explícito · `--rag-mode kb_combined` en N=120 / `entities` en N=15 · verificación de tasa de
fallo por corrida (trampa 04) · diccionarios NO regenerados · pre-checks (corpus 15/120, dicts 3605/1848/12000) ·
`caffeinate` sin suspensiones · coordinación en `CURRENT-TASKS.md §3.bis`.

## 7. Pendiente único

`qwen3:8b` re-corrida limpia (~1.5-2 h). Al cerrar: verificación §4.3 y set completo listo para merge + ANOVA.
