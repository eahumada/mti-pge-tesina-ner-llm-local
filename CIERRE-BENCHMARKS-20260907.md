# 🔒 CIERRE DE BENCHMARKS — 2026-09-07

**Decisión del autor:** se conservan los **13 modelos actuales** y **se cierra la fase de ejecución**.
No se lanzan más corridas. Todo lo que queda es documental.

---

## 1. Alcance definitivo del estudio N=120 (KB RAG)

**13 modelos × 2 modos = 26 grupos · 3 120 filas · N=120 por grupo.**
Análisis conjunto: `results/ANALISIS_CONJUNTO_20260907/` — **F = 36.3666 · p = 1.2236e-152**.

| # | Modelo | baseline | kb_rag | ΔRAG |
|--:|:---|--:|--:|--:|
| 1 | `gemma4:31b-cloud` | 0.6238 | 0.6185 | −0.005 |
| 2 | `gemma4:31b-mlx` | 0.5925 | 0.5907 | −0.002 |
| 3 | `gemma4:12b-mlx` | 0.5618 | 0.5846 | +0.023 |
| 4 | `gemma4:latest` | 0.5591 | 0.5474 | −0.012 |
| 5 | `qwen2.5:14b` | 0.5022 | 0.5484 | +0.046 |
| 6 | `llama3.1:8b` | 0.4876 | 0.5075 | +0.020 |
| 7 | `qwen3:8b` *(think=false)* | 0.4821 | 0.5146 | +0.032 |
| 8 | `gemma:latest` | 0.4400 | 0.5136 | +0.074 |
| 9 | `gpt-oss:20b` *(think ON, congelado)* | 0.4384 | 0.3419 | −0.097 |
| 10 | `mistral-nemo:latest` | 0.4338 | 0.4576 | +0.024 |
| 11 | `llama3.2:latest` | 0.3611 | 0.4693 | **+0.108** |
| 12 | `deepseek-r1:1.5b` | 0.2483 | 0.2394 | −0.009 |
| 13 | `nemotron-mini:4b` | 0.2259 | 0.3712 | **+0.145** |

**Hallazgo central:** el RAG contextual aporta tanto más cuanto más débil es el modelo (+0.145, +0.108,
+0.074 en la cola) y es neutro o negativo en los grandes (−0.005 y −0.002 en los dos 31B).

**Fuera del estudio por decisión del autor:** `nuextract`, `minimax-m3`, `gemini`, `gliner`, `phi3.5`,
`gemma4-12b-mlx-q8-64k` (nombre retirado) y **`sonct988/gemma4-26b`** (cuantización *custom* de un usuario:
ni citable ni reproducible; eliminado del árbol de trabajo el 2026-09-07, commit `33fbe7d`).

## 2. Estado de integridad al cierre

| Comprobación | Resultado |
|:---|:---|
| Convención de puntuación | **Única en todo el estudio** (bug `F1=1.0` en extracción vacía corregido y re-puntuado sin re-inferir) |
| Violaciones de `F1 ≤ (P+R)/2` | **0** |
| Filas degeneradas (`P=R=0` con `F1=1`) | **0** |
| `parse_method='failed'` | **0** en todas las corridas |
| `summary` vs `CSV` | Coinciden en todas las corridas |
| Fuente válida de P/R/F1 | `benchmark_results.csv` (ver `results/AVISO-SUMMARIES-OBSOLETOS.md`) |

**Dos salvedades que deben declararse en el informe:**

1. **`gemma4:31b-cloud` — la latencia no mide inferencia.** Está cuantizada por el `--request-delay` que se
   añadió para resolver el *rate limit*: 114 filas en exactamente 1,02 s. **Su F1 es válido; su latencia y
   sus tok/s no pueden usarse en ninguna comparación de eficiencia.**
2. **`nemotron-mini:4b` — 7 filas con telemetría en cero.** Re-extraídas fuera del arnés durante el parcheo:
   P/R/F1 reales, `latency=0` y `tok/s=0`. Coinciden con la firma de *rechazo de infraestructura*, así que
   toda auditoría futura las marcará si no se documenta. Es además el único modelo con reintentos (16).

**Advertencia transversal:** las latencias **no son comparables entre modelos** — las corridas usaron
`num_workers` distinto (6 vs 9) y máquinas distintas (16 GB y 48 GB).

## 3. ⚠️ Dos conjuntos distintos, no confundirlos

| | Tabla 2 del informe (§5.1) | Estudio N=120 (ANOVA) |
|:---|:---|:---|
| **Corpus** | N=15 | N=120 |
| **Modo RAG** | `entities` | `kb_combined` |
| **Alcance** | 12 modelos / 13 configuraciones | **13 modelos** |
| **Estado** | Contiene modelos **fuera del estudio** (`gemini-3.1-flash-lite`, `nuextract:latest`) y la sustitución A1 pendiente | Cerrado y verificado |

Los «12 modelos» que declara el informe (§1.4, §3.2, §5.1) se refieren a la **Tabla 2**, no al estudio N=120.
Conviene decirlo explícitamente en el texto: un revisor que vea «12» y luego un ANOVA de 13 pensará que falta
un modelo.

## 4. Lo que queda — todo documental, ninguna ejecución

- **Sustituciones A1-A3** (`remote_48g/DECISIONES-PENDIENTES-AUTOR.md`): aprobar el reemplazo por dato limpio.
- **Tabla 2:** retirar/marcar `gemini-3.1-flash-lite` y `nuextract:latest`, aplicar A1 (`gemma4:31b` → 0.6912)
  y resolver las dos filas con cifras idénticas (`gemma4:31b` y `gemma4:31b-mlx`, ambas 67.83 %).
- **Renombrado terminológico global** a «Variación / Variantes de Prompts» — la condición de disparo
  (datos completos) **ya se cumple**.
- **Cierre de formato del `.docx`** (Claude Desktop §2.1-2.5), ahora **desbloqueado**: verificar el límite de
  **25 páginas** tras las correcciones B1-B4, que añadieron texto.
- **Declarar las dos salvedades** del §2 de este documento.

## 5. Para el equipo remoto

**La fase de ejecución está cerrada. No lanzar más corridas.** Quedan dos encargos documentales de
`CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`, útiles solo si el estudio se amplía en el futuro:
evaluar `qwen3:14b/32b/latest` y **enumerar los modelos con capacidad `thinking`**. Las reglas para cualquier
ejecución posterior están en `RECOMENDACIONES-EJECUCIONES-FUTURAS.md`.

---

## 6. Enmienda (2026-09-07) — una excepción al cierre

**Decisión del autor:** se reabre la ejecución **para una sola corrida**, la de **N=30**.

Motivo: el F1 titular de ese corpus (`gemma4:31b` 79.03 %) es **la única cifra del estudio todavía calculada
con el *scorer* defectuoso**, y no admite re-puntaje porque su dato por registro se perdió por sobrescritura
(solo sobrevive el agregado de `benchmark_augmented_30.log`). Sostiene §5.3.1–5.3.4 y la verificación de la
hipótesis en §6.1, así que necesita respaldo verificable.

Encargos: [`ENCARGO-REMOTO-N30-20260907.md`](./ENCARGO-REMOTO-N30-20260907.md) (§3.bis.12) y
[`ENCARGO-REMOTO-GPTOSS-20260907.md`](./ENCARGO-REMOTO-GPTOSS-20260907.md) (§3.bis.13, diagnóstico de
`gpt-oss:20b` — **10 registros, no una corrida completa** — y búsqueda de los datos perdidos de N=30). **El resto del cierre sigue plenamente vigente:** ninguna otra corrida se
reabre, y el estudio N=120 de 13 modelos queda como está.
