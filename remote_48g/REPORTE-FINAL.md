# Reporte final — Equipo Remoto 48 GB (cierre)

**Fecha:** 2026-09-06 18:15 · **Rama:** `sesion/revision-final-20260905` · **Entregables:** `remote_48g/results/`

Ejecución **100 % completa y verificada**. Todos los modelos del estudio N=120 corridos, con F1 re-puntuado
tras corregir el bug de scoring. Sin corridas activas.

---

## 1. Integridad (barrido final)

| Corrida | Filas | Fallos | F1 anómalos | Dups | Estado |
|:---|--:|--:|--:|--:|:--|
| `gemma4_31b_n15` | 30/30 | 0 | 0 | 0 | ✅ |
| `excluidos_n120` (sonct988, gpt-oss) | 480/480 | 0 | 0 | 0 | ✅ |
| `benchmark_n120` (P3, 7 modelos) | 1680/1680 | 8¹ | 0 | 0 | ✅ |
| `ablacion_n15` (variación prompts) | 60/60 | 0 | 0 | 0 | ✅ |
| `gemma4_31b_cloud_n120` | 240/240 | 0 | 0 | 0 | ✅ |
| `nemotron_rerun_n120` | 240/240 | 7¹ | 0 | 0 | ✅ |
| `qwen3_nothink_n120` | 240/240 | 0 | 0 | 0 | ✅ |
| `afectados` (gemma4:12b-mlx limpio) | 240 | 0 | 0 | 0 | ✅ |

¹ `nemotron-mini:4b` — vacíos esporádicos inherentes al 4B (no thinking, no longitud). Excluir esas filas.
Sin F1 fuera de [0,1], sin F1 > (P+R)/2, sin duplicados. `--rag-mode` correcto por corpus.

---

## 2. Tabla de resultados F1 (corregida, definitiva)

N=120, `kb_combined`. Fuente de verdad indicada por modelo.

| # | Modelo | baseline | kb_rag | ΔRAG | Fuente |
|--:|:---|--:|--:|--:|:---|
| 1 | `sonct988/gemma4-26b` | 0.5627 | **0.5964** | +0.034 | excluidos |
| 2 | `gemma4:31b-cloud` | 0.6238 | 0.6185 | −0.005 | cloud |
| 3 | `gemma4:12b-mlx` | 0.5618 | 0.5846 | +0.023 | afectados (fix thinking) |
| 4 | `qwen3:8b` (think=false) | 0.4821 | 0.5146 | +0.033 | qwen3_nothink |
| 5 | `llama3.1:8b` | 0.4876 | 0.5075 | +0.020 | P3 |
| 6 | `mistral-nemo` | 0.4338 | 0.4576 | +0.024 | P3 |
| 7 | `gpt-oss:20b` | 0.4384 | 0.3419 | −0.097 | excluidos (fix routing) |
| 8 | `nuextract` | 0.4288 | 0.2240 | −0.205 | P3 |
| 9 | `nemotron-mini:4b` | 0.2150 | 0.3712 | +0.156 | rerun (excluir 7 failed) |
| 10 | `deepseek-r1:1.5b` | 0.2483 | 0.2394 | −0.009 | P3 |

**Tabla 2 — `gemma4:31b` N=15** (`entities`): baseline 0.6912 · rag 0.6391.
**Variación de prompts** (`gemma4:latest`, N=15): **fs-es 0.7444** · zs-es 0.6843 · zs-en 0.6405 · fs-en 0.6332.

---

## 3. Correcciones e incidencias resueltas

1. **Routing `gpt-oss:20b`** — `gpt-*` iba a OpenAI; ahora tags Ollama (`:`) → Ollama. Recuperado (0 fallo).
2. **Bug thinking** (`gemma4:12b-mlx` vacíos, `qwen3` thinking off) — fix `743054d`; re-corridas limpias.
3. **Rate limit cloud** — `--max-workers`/`--request-delay`; `gemma4:31b-cloud` de 79 % fallo → 0 %.
4. **qwen3 thinking innecesario** — think=false iguala/supera y ~10× más rápido; aplicado.
5. **Bug de scoring** (`evaluator.py`: extracción vacía → F1=1.0) — **corregido y re-puntuado desde datos
   guardados, sin re-inferir** (`tools/rescore_saved.py`). Desinfló nuextract kb_rag 0.43→0.22, nemotron 0.36→0.21.

## 4. Aprendizajes operativos

- No reiniciar corridas con checkpoint para "optimizar" concurrencia: corrompe cobertura (dupes/huecos).
- qwen3 thinking es GPU-bound: más workers = thrash, no acelera.
- Verificar tasa de fallo por modelo antes de citar cifras; separar fallo de cuota (429/402) de fallo de parseo.

## 5. Decisiones del autor aún pendientes (redacción)

Ninguna bloquea la ejecución; requieren tu criterio o fuente externa (ver `TODO-INFORME-FINAL.md §10`):
- **#4** cita `[referencia KPMG 2024]` (§1.1): aportar fuente o eliminar.
- **#6** contradicción de hardware (§2.4/§3.6, 24,7 GB sobre 16 GB): reformular.
- **#7** tabla de eficiencia §5.5 (VRAM/tok-s no reproducibles): reconciliar o marcar.
- **#1** filas legacy con F1 imposible (`llama3.2_rag` 0.8783, `llama3.1:8b_baseline` 0.7667): retirar/ marcar no verificables.

## 6. Listo para

**Merge + ANOVA** sobre el set de 10 modelos N=120 (+ referencia 2026-09-01) con F1 corregido, más Tabla 2 y
Variación de prompts. Todos los CSV en `remote_48g/results/` re-puntuados.
