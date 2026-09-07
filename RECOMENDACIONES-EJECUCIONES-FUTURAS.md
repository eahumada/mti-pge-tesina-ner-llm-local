# Recomendaciones para ejecuciones futuras — política de modo *thinking*

**Fecha:** 2026-09-07 · **Estado:** HALLAZGO FINAL, cerrado · **Destinatarios:** equipo remoto 48 GB,
equipo principal y cualquier sesión (Claude Code, Claude Desktop, Antigravity) que reanude el benchmark.

> Este documento **no describe trabajo pendiente**: fija las reglas con las que se ejecutarán los benchmarks
> de aquí en adelante. Nace de dos episodios reales de este estudio — el falso hallazgo de `qwen3` y el
> experimento de 5 modelos — y de su verificación contra los datos crudos.
> Fuentes: `FINDINGS.md §F44` y **§F45**, `remote_48g/EXPERIMENTO-THINKING-5MODELOS.md`,
> `CORRECCION-QWEN3-THINKING-20260906.md`.

---

## 1. Régimen de *thinking* por modelo (vigente)

| Modelo | Régimen | Fundamento |
|:---|:---|:---|
| `gpt-oss:20b` | **ON — CONGELADO** | Sin razonamiento **deja de producir**: `recall=0` en 7/15 (baseline) y 10/15 (kb_rag). ΔF1 −0.12. Su corrida oficial `results/excluidos_n120_REMOTO` **no se re-ejecuta ni se toca** |
| `qwen3:8b` | **OFF** | Único efecto grande y consistente medido sobre **N=120**: F1 +4,2 pp, `recall=0` de 15 → 1, ~10× más rápido |
| `gemma4:12b-mlx`, `gemma4:31b-mlx`, `gemma4-12b-mlx` | **OFF** | El razonamiento agotaba `num_predict` y vaciaba `content` |
| `qwen3:14b`, `qwen3:32b`, `qwen3:latest` | ON — **sin medir** | Pendiente de evaluación si entran en algún estudio |

## 2. Reglas operativas

**R1 — No generalizar entre modelos.** El efecto del *thinking* es **específico de cada modelo**. Que
apagarlo ayude en uno no dice nada sobre otro.

**R2 — `think` es parámetro de primer nivel.** Va como kwarg de `Client.chat()`, **nunca dentro de
`options`**. Ollama **descarta en silencio** las claves de `options` que no conoce, y entonces el modelo corre
con su **valor por defecto — que en un modelo con capacidad `thinking` es ON**, no OFF. Este error hizo creer
durante meses que `qwen3` corría sin razonamiento cuando corría con él.

**R3 — Antes de cambiar el régimen, medir con el pipeline real**, con `thinking` como única variable y el
scorer corregido. Nunca decidir sobre una estimación.

**R4 — Umbral de decisión.** Aceptar el cambio solo si el ΔF1 es **≥ 0 en todas las condiciones medidas** y el
**signo es estable**. Un modelo cuyo delta cambia de signo entre sus propias condiciones (p. ej.
`gemma4:latest`: +0.066 en `fs-en` y −0.051 en `fs-es`) está mostrando **ruido, no efecto**. Con N=15,
descartar cualquier |ΔF1| < 0.05.

**R5 — Exigir mecanismo, no solo media.** Un efecto real se ve en el **conteo de `recall=0`** y en la
latencia, no únicamente en el F1 medio. `gpt-oss` es el ejemplo: lo decisivo no fue el −0.12 sino que dejara
de responder en la mitad de los artículos.

**R6 — La latencia debe corroborar la hipótesis.** El razonamiento genera tokens: **no puede acelerar**. Si la
condición «OFF» sale más lenta, **hay que detenerse y explicarlo antes de concluir nada**. Caso vivido: en el
falso hallazgo de `qwen3` la condición «OFF» aparecía más lenta que «ON», y esa inversión era precisamente la
señal de que las etiquetas estaban cambiadas.

**R7 — Documentar el régimen en el `run_config.json` de cada corrida** y **no mezclar regímenes en silencio**.
Si el estudio combina modelos con y sin *thinking*, debe declararse como excepción justificada — igual que se
hizo con la convención de puntuación.

**R8 — Comparar solo lo comparable.** Antes de contrastar dos corridas, verificar que difieren **de verdad**
en la variable de interés. Si dos corridas dan métricas idénticas fila a fila, no han comparado nada: tenían
la misma configuración.

## 3. Verificaciones obligatorias antes de aceptar cualquier cifra

1. **Tasa de fallo por modelo:** `parse_method='failed'` y número de `recall=0`.
2. **Protocolo:** `run_config.json` con el `--rag-mode` correcto (`kb_combined` en N=120, `entities` en N=15)
   y los 9 parámetros de la corrida de referencia.
3. **Consistencia aritmética:** ninguna fila puede tener `F1 > (P+R)/2`.
4. **Al promediar desde JSON**, usar `if x.get('k') is not None` — **nunca** `if x.get('k')`: `0.0` es falsy y
   descartaría las filas en cero, inflando la media.
5. **Distinguir causas:** latencia 0 y 0 tokens = rechazo de infraestructura; latencia alta con `content`
   vacío = el arnés perdió la respuesta. Cruzar `parse_method` con `recall` para ver si el *fallback* rescata
   contenido o encubre un fallo.
6. **Fuente válida:** `benchmark_results.csv`. Ver `results/AVISO-SUMMARIES-OBSOLETOS.md`.

## 4. Para el equipo remoto — qué hacer la próxima vez

- **No re-ejecutar** los 4 modelos con `think=OFF` (decisión cerrada, §F45): sus deltas son ruido de N=15 y
  hacerlo introduciría un **segundo eje de inconsistencia** en el estudio (unos modelos con razonamiento y
  otros sin él), del mismo tipo que las dos convenciones de puntuación que ya costó cerrar.
- **Si en el futuro se amplía el estudio**, medir el régimen de *thinking* **a N=120**, no a N=15, y aplicar
  R4–R6 antes de tocar el código.
- **Sigue pendiente** de `CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`: evaluar `qwen3:14b/32b/latest` y
  **enumerar todos los modelos del estudio con capacidad `thinking`**.
