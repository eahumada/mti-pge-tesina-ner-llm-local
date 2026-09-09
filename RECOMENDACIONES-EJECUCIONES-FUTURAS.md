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

## 2.bis Codificación del corpus

**R9 — Verificar la codificación del corpus antes de usarlo, en la entrada y en la referencia.** El corpus
N=120 de este estudio almacena *mojibake*: guarda `JosÃ© Bono` donde el nombre real es **José Bono** (bytes
UTF-8 reinterpretados como Latin-1). Comprobación: `s.encode('latin-1').decode('utf-8') != s`.

**R10 — Un defecto de codificación coherente NO produce un sesgo uniforme.** Si el defecto está en el gold
*y* en el texto de entrada —como aquí: 20,1 % de las entidades y 87 % de los artículos—, el corpus es
internamente consistente: **premia al modelo que transcribe literalmente y penaliza al que normaliza la
ortografía**. Medido, el efecto varía entre **−0.070 y +0.091** de F1 según el modelo. Ver `FINDINGS.md §F48`
y `LEARNING.md §L39`.

**R11 — Al repararlo, normalizar los DOS lados de la comparación.** Arreglar solo la referencia invierte la
injusticia en vez de eliminarla. La reparación debe aplicarse al gold **y** a la entidad extraída antes del
cotejo difuso —`rapidfuzz.fuzz.ratio` con `fuzzy_threshold=85` (`src/evaluator.py`), que mide similitud de
**caracteres**, no de tokens—, de modo que el resultado no dependa de la representación de bytes.

**R12 — Una re-corrida aislada usa el mismo corpus y el mismo evaluador que las demás.** Corregir el corpus
para un solo modelo lo mide con otra vara — el mismo error que mezclar convenciones de puntuación o regímenes
de *thinking*.

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
7. **Población de la métrica:** leer `total_records` del `benchmark_summary.json` y comprobar que coincide con
   las filas que se están promediando. En N=15 y N=30 coinciden; en N=120 **no**, porque se descuentan los
   siete artículos contaminados y la métrica publicada va sobre **113**. Promediar el CSV entero da un número
   que no es el del estudio (`FINDINGS §F65`).
8. **La latencia no caracteriza al modelo.** Incluye la espera en cola bajo concurrencia, de modo que no
   compara entre corridas ni dentro de una misma. Se comprueba multiplicándola por `tokens_per_sec`: si el
   producto supera el tope de salida configurado, la latencia no mide generación. En las corridas publicadas
   lo supera en **20 de 26 grupos** (`FINDINGS §F71.ter`). Lo que sí compara es `tokens_per_sec`, estable
   entre corridas.

## 3.bis Qué registrar la próxima vez, y que hoy falta

- **El recuento de tokens generados por registro.** Es el dato que determina cuánto tarda una corrida, y no
  está en ninguna parte: el CSV guarda `tokens_per_sec` pero no los tokens. Sin él **la duración de un
  barrido no es estimable**, y este proyecto lo intentó dos veces por caminos distintos, fallando las dos
  (`FINDINGS §F79`). Añadir una columna cuesta nada y evita tener que juzgar por el silencio si una ejecución
  sigue viva.
- **Un tiempo de inferencia separado de la espera.** Si además del reloj de pared se registrara el tiempo que
  el modelo pasa generando, la tabla de eficiencia podría publicar segundos por artículo comparables, cosa
  que hoy no puede.
- **El manifiesto de artículos excluidos junto a cada corrida.** Hoy vive en `data/knowledge_base/` y una
  corrida aislada no lleva constancia de sobre qué población se calculó su métrica.

## 3.ter Cómo se escriben las comprobaciones, y cómo se prueban

Ocho defectos de esta revisión estaban en las propias comprobaciones, no en los datos. Las cuatro reglas que
los habrían evitado, todas comprobadas contra un caso real:

**Una comprobación declara cuántos elementos examinó, y un recuento que baja es un síntoma.** `§L47` lo fijó
para el caso de cero, pero el peor no es cero: es que baje de trece a nueve, porque **parece un estado
normal**. Ocurrió con la comprobación del índice de defensa cuando un artefacto desaparecía, y con las tablas
del informe cuando una fila dejaba de ser legible: bajaban de 52 a 48 y seguían diciendo «ok»
(`FINDINGS §F82`, `LEARNING §L60`).

**Lo robusto no es publicar el recuento, sino exigir que todo candidato se procese.** Contar lo que se
intentó, no solo lo que salió bien. Una fila con formato inesperado tiene que aparecer **como fallo, no como
ausencia**.

**Un recuento no se comprueba por presencia de la palabra.** Una cifra decimal distintiva —«0,0879»— sí,
porque no aparece por casualidad; «tres» no, porque aparece en cualquier documento en español por otros
motivos. Los recuentos exigen anclaje: el número **en la misma oración** que el sustantivo que cuenta
(`§L59`).

**Una autoprueba de cobertura debe atribuir.** No basta con preguntar «¿falló algo?»: hay que exigir que
falle **la comprobación que usa ese artefacto**. Varios ficheros los leen dos o tres comprobaciones distintas,
y basta con que una se entere para que la autoprueba dé el visto bueno mientras las otras siguen ciegas
(`§L60`).

**Y sobre las pruebas de mutación**, que son las que destaparon todo lo anterior: una mutación debe alcanzar
**todas** las apariciones de lo que altera. Dos falsos negativos de esta revisión fueron mutaciones mal
construidas —una cambió una de dos apariciones de la misma cifra— y en ambos casos la conclusión precipitada
habría sido «la comprobación no funciona».

## 3.quater Órdenes cuyo «no hizo nada» se confunde con «lo hizo bien»

Tres incidentes con la misma forma, y la misma solución:

| Orden | El valor engañoso | El control que lo destapa |
|:---|:---|:---|
| Comprobar una purga de GitHub | **404** significa «purgado» o «URL mal escrita» | Pedir en la misma orden la raíz del repositorio y un commit vigente: deben dar 200 (`§L57`) |
| `git branch -f <rama> main` | No mueve la rama **activa** y el rechazo va a `/dev/null` si se silencia | `git rev-list --count origin/<rama>..<rama>` por cada rama, comparado con cero (`§L58`) |
| Extraer texto de un PDF | **Cero apariciones** significa «no lo dice» o «el extractor no lee» | Buscar además palabras que **tienen** que estar (`§L57` aplicado) |

**La regla:** toda comprobación cuyo valor bueno sea «algo ya no está» lleva adjunto el control de algo que
**sí debe seguir estando**. Si el control también falla, el resultado no es un hallazgo: es una avería.

Y su corolario: **un resultado que mejora sin causa conocida se verifica antes de celebrarse**. Se aplicó dos
veces con signos opuestos —un 404 que parecía éxito y era avería, y una cuenta de acreditaciones que bajó de
cuatro a tres y era una mejora, porque Zenodo había vuelto a responder—.

## 4. Para el equipo remoto — qué hacer la próxima vez

- **No re-ejecutar** los 4 modelos con `think=OFF` (decisión cerrada, §F45): sus deltas son ruido de N=15 y
  hacerlo introduciría un **segundo eje de inconsistencia** en el estudio (unos modelos con razonamiento y
  otros sin él), del mismo tipo que las dos convenciones de puntuación que ya costó cerrar.
- **Si en el futuro se amplía el estudio**, medir el régimen de *thinking* **a N=120**, no a N=15, y aplicar
  R4–R6 antes de tocar el código.
- **Sigue pendiente** de `CORRECCION-QWEN3-THINKING-20260906.md §4.6-4.7`: evaluar `qwen3:14b/32b/latest` y
  **enumerar todos los modelos del estudio con capacidad `thinking`**.
