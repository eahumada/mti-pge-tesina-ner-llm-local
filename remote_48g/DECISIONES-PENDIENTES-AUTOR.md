# Decisiones de redacción pendientes del autor

**Fecha:** 2026-09-06 · **Equipo Remoto 48 GB** · Fuente: `TODO-INFORME-FINAL.md §10-§12`

La **ejecución está 100 % completa** (0 fallos en todo el estudio, scoring corregido). Lo que queda **no es
ejecutable**: requiere tu criterio o una fuente externa. Ninguna bloquea el merge+ANOVA; sí bloquean la
defensa si no se resuelven.

---

## A. Sustituciones directas — ya hay dato limpio, solo falta aprobar

| # | Qué | Valor actual (sin respaldo) | Valor nuevo (medido) | Acción |
|--:|:---|:---|:---|:---|
| A1 | Tabla 2 `gemma4:31b` (N=15) | F1 **67,83 %** | **0.6912** / rag 0.6391 | sustituir |
| A2 | Análisis de Variantes de Prompts | 0.7169 / 0.6640 / 0.6482 / 0.5874 | **fs-es 0.7444 · zs-es 0.6843 · zs-en 0.6405 · fs-en 0.6332** | sustituir |
| A3 | `gemma4:31b-cloud` N=120 | tabla 0.6754 (subconjunto) vs crudo contaminado | **0.6238 / 0.6185** (0 fallo, rate-limit) | sustituir |

**Decisión requerida:** ¿apruebas reemplazar A1-A3 por las mediciones limpias del equipo remoto?

---

## B. Requieren tu criterio o una fuente externa (no hay dato)

| # | Problema | Ubicación | Opciones |
|--:|:---|:---|:---|
| B1 | **F1 aritméticamente imposibles** en tabla legacy: `llama3.2_rag` 0.8783 (> cota 0.7646) y `llama3.1:8b_baseline` 0.7667 (> 0.7333). **Ningún valor existe en dato alguno.** | `BENCHMARKS.md` RAG Integration Study | (a) retirar filas · (b) marcar «prototipo temprano, no verificable». *Nota:* ya hay `llama3.1:8b` real N=120 (0.4876/0.5075) si se quiere reemplazar. |
| B2 | **Cita inventada** `[referencia KPMG 2024]` junto a cifras de mercado (USD 12.300 y 87.200 M) | Informe §1.1 | (a) aportar la fuente real · (b) eliminar las cifras. Fabricar la cita = falsificación. |
| B3 | **Contradicción de hardware**: se declara correr modelos de ~24,7 GB de VRAM sobre 16 GB | Informe §2.4 / §3.6 | reformular. *Insumo:* el equipo remoto confirmó que esos modelos requieren >16 GB (por eso se delegaron a 48 GB). Redacción honesta disponible. |
| B4 | **Tabla de eficiencia no reproducible**: VRAM/Tok-s de §5.5 no salen de ningún CSV (24.607 MB / 22.80 vs 24.751 / 27.56 de la tabla) | Informe §5.5 | reconciliar con el CSV o marcar la fuente. |

---

## C. Ya decididas por el autor (no requieren acción — registro)

- **qwen3 thinking:** `think=false` (no mejora F1, ~10× más lento). Aplicado.
- **Bug de scoring** (F1=1.0 en extracción vacía): corregido y re-puntuado sin re-inferir.
- **Modelos cloud legacy:** se conservan como comparación histórica.
- **gliner / gemini / phi3.5:** fuera del estudio; no citar como resultados.
- **F1 titular N=30 (79,03 % de julio):** el nuevo resultado es el oficial; el de julio queda en WORKLOG.

---

## Recomendación de orden

1. Aprobar **A1-A3** (sustituciones mecánicas con dato limpio) → cierra 3 bloqueantes al instante.
2. Resolver **B1** (retirar/ marcar las 2 filas imposibles) → elimina el riesgo aritmético que un revisor
   detecta a simple vista.
3. **B2** (KPMG) y **B3/B4** (redacción) → cierre documental.

Tras A+B, el informe queda consistente y trazable para la defensa.
