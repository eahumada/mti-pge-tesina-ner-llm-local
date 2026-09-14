# Encargo al equipo de 48 GB — re-corridas para cerrar el informe

**Fecha:** 2026-09-14. **Entrega de la tesina:** 30 de septiembre de 2026, quedan dieciséis días.
**Origen:** `FINDINGS §F174`, `§F175` y su corrección, `LEARNING §L81` y `§L82`.

Este encargo sustituye a cualquier petición anterior sobre los mismos experimentos.

> **Ampliación del mismo día, por instrucción del autor: «no permitir fisuras en la tesis, correr lo que sea
> necesario; los costes son locales y la máquina de 48 GB está destinada solo a esto».** Con ella:
>
> - **todas las peticiones pasan a imprescindibles**, y R2 se extiende a los trece modelos;
> - **el cómputo deja de ser la restricción.** Todo corre en Ollama local, en esa máquina dedicada, sin
>   coste por llamada y sin límite de peticiones. La única restricción real es el **calendario**: quedan
>   dieciséis días y el informe hay que reescribirlo con los resultados, de modo que lo que llegue tarde no
>   entra aunque esté bien medido.
> - Por eso el encargo se ordena por **cuándo desbloquea trabajo del informe**, no por coste, y por eso
>   incluye una lista de ampliaciones que antes se habrían descartado por caras.

---

## Por qué se pide esto

El informe publicaba «+10,40 puntos de F1 por redactar el prompt en español». La cifra reproduce
exactamente desde su CSV y aun así era engañosa: de los quince artículos del corpus, **uno** puntuó 0,00 en
las dos configuraciones inglesas porque el modelo no devolvió salida parseable (`tp=0`, `fp=0`, `fn=18`,
`parse_method='fallback'`). Ese artículo aporta 6,21 de los 10,40 puntos; sin él, el efecto del idioma puro
cambia de signo. La corrida procede del 6 de septiembre, con `max_tokens=2048` y el parser anterior al
arreglo `§F85`.

**La re-corrida del 8 de septiembre no cubre ese experimento.** Sus 39 corridas miden solo `baseline` y
`kb_rag`, con `SYSTEM_PROMPT.md` (zero-shot inglés) y `max_tokens=4096`. De modo que hoy no existe
medición vigente del efecto del idioma del prompt, y el informe cita una que no se sostiene.

Buscando el mismo defecto en la corrida vigente apareció un segundo asunto, este de fondo: **dos corridas
con configuración idéntica dan resultados distintos**. Comprobado en los `run_config.json`: mismo modelo
(`gemma4:latest`), mismo corpus (`data/kleptotrace.json`), **semilla 42**, temperatura 0,1,
`max_tokens=2048`, mismo `SYSTEM_PROMPT.md`, mismo umbral difuso de 85. Resultados:

| Corrida | zs-en | fs-es |
|:---|---:|---:|
| `ablacion_n15_REMOTO` | 64,05 % | 74,44 % |
| `kleptotrace_20260727_110454` | 66,76 % | 69,87 % |

Casi cinco puntos de diferencia en la misma celda. **Todo el estudio es de una sola pasada por modelo, de
modo que ninguna de sus cifras tiene barra de error conocida.** Es la primera pregunta que hará un tribunal.

---

## R1 — Variantes de prompt, con réplicas (IMPRESCINDIBLE)

**Qué se corre.** El diseño factorial 2×2 de siempre: `zs-en`, `zs-es`, `fs-en`, `fs-es`, con la rama
`--ablation` de `src/main.py`, que solo intercambia el fichero de prompt y no activa recuperación.

**Sobre qué.**

| Corpus | Modelo | Condiciones | Semillas | Llamadas | Reloj estimado |
|:---|:---|---:|---:|---:|---:|
| N=15 (`data/kleptotrace.json`) | `gemma4:latest` | 4 | 5 | 300 | ~45 min |
| N=120 (`data/benchmark_balanced_120.json`) | `gemma4:latest` | 4 | 5 | 2 260 | ~6 a 7 h |

**Primero el N=15**, que es el que sustituye directamente a la Tabla 5 del informe y da resultado en menos
de una hora. **El N=120 es el que de verdad responde a la pregunta de la tesina**, porque 105 de sus 120
artículos están en español y la hipótesis del trabajo habla de despliegues en mercados hispanohablantes: el
N=15 está íntegramente en inglés, de modo que un efecto del idioma medido solo ahí nunca fue el experimento
correcto.

Si tras el N=120 sobra tiempo, repetid el N=120 con `gemma4:31b-mlx`, que es el mejor modelo local vigente.
No es imprescindible.

**Con qué configuración.** La vigente, sin excepciones: `max_tokens=4096`, parser posterior al arreglo
`§F85`, `per_entity` persistido, corrector de puntuación aplicado, y el manifiesto de los siete artículos
contaminados excluido en el N=120. Semillas **42, 43, 44, 45, 46**, declaradas en el `run_config.json` de
cada corrida.

**Qué hay que entregar.** Media y desviación típica de F1 por condición y semilla, el contraste pareado por
artículo entre `fs-es` y `zs-en` (en cuántos mejora, en cuántos empeora, en cuántos empata), y el recuento
de registros con extracción vacía por condición. **No calculéis vosotros el veredicto**: entregad los datos.

**Qué arregla.** §5.2 y la Tabla 5, el primer factor de §6.1, la conclusión 2, el punto 10 de §7.2 y las
frases del resumen y del abstract.

---

## R2 — Barra de error de TODA la Tabla 7 (IMPRESCINDIBLE)

**El problema.** El estudio completo es una sola pasada por modelo. La comparación de arriba demuestra que
repetirla no da lo mismo. Sin repeticiones no se puede decir cuánta de la diferencia entre dos modelos es
real y cuánta es ruido de ejecución, y la Tabla 7 ordena trece modelos por décimas.

**Qué se corre.** `baseline` y `kb_rag` sobre N=120, **para los trece modelos**, tres veces:

- **2 repeticiones adicionales con semilla 42**, que miden el **no determinismo del sistema**: si con semilla
  fija ya varía, el ruido está en la ejecución (concurrencia, orden de la cola, estado del servidor) y no en
  el muestreo del modelo.
- **1 repetición con semilla 43**, que mide la **variabilidad de muestreo**.

Son dos fuentes distintas y el informe necesita separarlas. La corrida del 8 de septiembre cuenta como la
primera repetición con semilla 42, de modo que basta con añadir tres barridos completos.

**Coste medido, no estimado.** El barrido del 8 de septiembre tardó **8 h 24 min** de reloj para sus 39
corridas; la parte de N=120 suma **416 min**, es decir **unas 7 h** por barrido completo de los trece
modelos. Tres barridos: **unas 21 h**, repartibles en tres noches.

| Modelo | N=120, minutos por barrido |
|:---|---:|
| `gpt-oss:20b` | 126,6 |
| `gemma4:latest` | 74,4 |
| `gemma4:31b-mlx` | 45,3 |
| `qwen2.5:14b` | 27,5 |
| `deepseek-r1:1.5b` | 23,0 |
| `qwen3:8b` · `gemma4:12b-mlx` · `mistral-nemo:latest` | 18,4 · 18,2 · 18,2 |
| `gemma:latest` · `llama3.1:8b` | 17,3 · 17,0 |
| `nemotron-mini:4b` · `gemma4:31b-cloud` · `llama3.2:latest` | 11,0 · 10,9 · 8,7 |

**Qué hay que entregar.** Los tres barridos completos, cada uno en su directorio, con su `run_config.json`.
**No consolidéis vosotros**: el consolidado y la desviación entre repeticiones los calcula el equipo
principal, para que el informe tenga una sola cadena de cálculo.

**Si algo tuviera que recortarse**, y solo entonces: conservad siempre las dos repeticiones con semilla fija
de los trece modelos, y sacrificad la de semilla 43. Con la semilla fija ya se puede publicar una barra de
error honesta de toda la tabla, que es el mínimo defendible.

## R3 — Instrumentación: que el fallo de parseo deje prueba (IMPRESCINDIBLE, y es código, no cómputo)

Sin esto, R1 y R2 vuelven a producir datos que no se pueden auditar.

1. **`src/llm_runner.py` línea 146** registra la respuesta cruda **cortada a 200 caracteres** cuando el
   parseo falla. Es exactamente lo que impidió clasificar el artículo 4 de `§F174`. **Guardad la respuesta
   íntegra**, en un fichero aparte por registro fallido (`raw_failures/<config>_<record_id>.txt`), no en el
   `benchmark.log`, para no engordarlo.
2. **Añadid dos columnas al CSV**, calculadas por el evaluador y no por un análisis posterior:
   `extraccion_vacia` (verdadero cuando `tp + fp == 0`) y `rescate_regex` (verdadero cuando el parseo fue
   `fallback` pero se recuperaron entidades). Las dos distinguen la avería del instrumento del fallo del
   modelo, que es la confusión que hizo declarar un defecto inexistente en `§F175`.
3. **Reintentad una vez** la llamada cuando el parseo falle por completo, y **registrad que hubo reintento**
   en su propia columna. Un reintento no declarado es peor que no reintentar.

**No toquéis nada más del evaluador.** A dieciséis días de la entrega, un cambio en el emparejamiento o en
las métricas obligaría a repetir el estudio entero. Estas tres son adiciones, no modificaciones del cálculo.

---

## R4 — El corpus del dominio en español (IMPRESCINDIBLE tras la instrucción del autor)

**La fisura.** `FINDINGS §F54` dejó abierto que el **Anexo F** del informe transcribe un prompt generador
redactado en español cuya salida versionada, el corpus N=30, **está en inglés**. O el prompt transcrito no es
el que se ejecutó, o el corpus versionado no es el que ese prompt generó. Mientras tanto, el informe declara
validación en el dominio y la cifra que la acredita (90,16 %) se midió sobre texto inglés.

**Cómo se cierra, y por qué así.** **No se regenera: se traduce.** El corpus N=30 se traduce al español
**conservando su anotación de referencia**, y se ejecutan los trece modelos sobre la versión española.

Regenerar desde cero exigiría anotación experta nueva, que es el activo caro de ese corpus y lo que le da
valor; producirla con prisa a dieciséis días de la entrega abriría una fisura mayor que la que cierra.
Traducir, en cambio, deja un **par emparejado**: el mismo contenido, las mismas entidades, dos idiomas. Eso
no solo cierra el hueco del Anexo F, sino que da el contraste de idioma más limpio de todo el trabajo, mucho
mejor que el del N=15, porque elimina la diferencia de contenido entre las dos condiciones.

**Cómo traducir sin romper la anotación.**

1. Los **nombres propios de personas y organizaciones no se traducen**: la anotación de referencia se
   conserva tal cual para esas dos categorías.
2. Las **localizaciones sí cambian de forma** (`United States` pasa a `Estados Unidos`). Hay que actualizar
   la anotación de esa categoría **y entregar la correspondencia**, entrada por entrada, para que se pueda
   auditar.
3. **Verificad que cada entidad de referencia aparece literalmente en el texto traducido.** Una entidad
   anotada que no está en el texto convierte cada acierto del modelo en un error, que es exactamente el
   defecto de `Locations` que costó dos meses detectar.
4. Entregad las dos versiones, `kleptotrace_augmented_30.json` (inglés, intacto, **no se toca**) y
   `kleptotrace_augmented_30_es.json` (nuevo).

**Qué se corre.** Los trece modelos, `baseline` y `kb_rag`, sobre la versión española: 780 llamadas,
**del orden de 2 h** de reloj a la velocidad medida.

**Y una reserva que hay que declarar en el informe, no esconder:** un corpus traducido no es un corpus
nativo. La traducción introduce su propia regularidad sintáctica, y eso debe decirse al presentar la
comparación. Es una limitación conocida y declarada; callarla sí sería una fisura.

## R5 — Variantes de prompt sobre el par emparejado del dominio (IMPRESCINDIBLE)

Una vez exista el N=30 en español, el diseño 2×2 de R1 se ejecuta **sobre las dos versiones del mismo
corpus**, con `gemma4:latest` y cinco semillas: 4 condiciones × 30 artículos × 5 semillas × 2 idiomas de
corpus = **1 200 llamadas, unas 6,6 h**.

Esto es lo que convierte la pregunta del idioma en un experimento con respuesta. Hoy el informe compara
prompt inglés contra prompt español **sobre un corpus inglés**, que es el experimento equivocado. Con el par
emparejado se puede responder a las dos preguntas que importan y que hasta ahora estaban confundidas:

- ¿el idioma del *prompt* importa cuando coincide con el del texto?
- ¿importa cuando no coincide?

## R6 — Contestad la pregunta pendiente del método (`§3.bis.17`)

Sigue sin respuesta desde el 2026-09-08 y no requiere cómputo. Vuestro manifiesto declara que el KB RAG
aporta **+10,01 pp** sobre los siete artículos contaminados y **+2,19 pp** sobre los ciento trece restantes;
recalculado aquí desde los `detailed_results.json`, promediando el delta de cada modelo y luego entre los
trece, salen **+11,89** y **+3,16**. La conclusión no cambia con ninguna de las dos, y las nuestras son
peores para el trabajo, de modo que no hay incentivo en preferirlas.

**Solo hace falta el método:** ¿promediasteis los registros de los siete y de los ciento trece por separado y
restasteis, o promediasteis por modelo y luego entre modelos? ¿Sobre qué corridas? Con eso se elige una
cifra y se declara. Publicar dos sin saber cuál mide qué es una fisura, y es de las baratas de cerrar.

## Coste total y orden de ejecución

| Orden | Petición | Llamadas | Reloj | Por qué este orden |
|---:|:---|---:|---:|:---|
| 1 | **R3** instrumentación | — | código | sin ella, todo lo demás vuelve a producir datos no auditables |
| 2 | **R1** variantes, N=15 | 300 | ~1,7 h | sustituye la Tabla 5 y da resultado el primer día |
| 3 | **R4** N=30 en español | 780 | ~2 h | desbloquea R5 |
| 4 | **R6** método | — | — | no requiere cómputo |
| 5 | **R5** variantes sobre el par del dominio | 1 200 | ~6,6 h | el experimento de idioma bien planteado |
| 6 | **R1** variantes, N=120 | 2 260 | ~12,4 h | el corpus donde vive la hipótesis |
| 7 | **R2** barra de error, trece modelos × 3 | 8 814 | ~21 h | el más caro, y repartible en noches |
| | **Total** | **13 354** | **~43 h** | menos de 3 h diarias en dieciséis días |

Las estimaciones de reloj salen de la velocidad **medida** en el barrido del 8 de septiembre: 226 llamadas
en 74,4 min para `gemma4:latest` sobre N=120, con la concurrencia de entonces. Si vuestra concurrencia
efectiva cambia, avisad con el primer dato real en lugar de esperar al final.

**El cómputo no es la restricción; el calendario sí.** Con la máquina dedicada, las 43 h caben de sobra en
dieciséis días. Lo que no cabe es esperar a tenerlo todo para empezar a escribir: **entregad cada petición en
cuanto termine, no al final**, porque cada una desbloquea una parte distinta del informe y esas partes se
reescriben en paralelo a vuestras corridas.

**Ampliaciones, ahora que el coste no manda.** Ejecutadlas en este orden, después de las siete anteriores, y
sin que ninguna retrase una entrega de las de arriba:

| | Ampliación | Llamadas | Reloj | Qué añade |
|:---|:---|---:|---:|:---|
| A1 | **R2 con cinco repeticiones** en lugar de tres (2 más con semilla 42, 1 más con semilla 44) | +5 876 | ~14 h | una desviación calculada sobre cinco puntos en vez de tres, que es lo mínimo para citarla sin reservas |
| A2 | **R1 sobre N=120 también con `gemma4:31b-mlx`** | +2 260 | ~5 h | comprueba si el efecto del idioma depende del tamaño del modelo, hoy medido en uno solo |
| A3 | **R5 con un segundo modelo** (`gemma4:31b-mlx`) sobre el par emparejado | +1 200 | ~2,5 h | lo mismo, sobre el contraste limpio |
| A4 | **N=15 y N=30 en el barrido de R2** | +2 100 | ~3 h | barra de error también para las Tablas 4 y 6, que hoy tampoco la tienen |

Con las ampliaciones el total ronda las **67 h**, unas cuatro horas diarias de máquina dedicada.

**Lo único que no se sacrifica en ningún escenario es R3**, porque es lo que garantiza que todo lo demás
pueda auditarse después. Si algo llega tarde, se declara en el informe que no se midió; lo que no se puede
es publicar una cifra que nadie puede reconstruir.

## Reglas que siguen vigentes

- **Los registros de ejecución no se editan ni se borran**, nunca, ni una línea. Son la prueba de qué se
  ejecutó, y este proyecto ya los ha necesitado para diagnosticar.
- **Ninguna cifra de una medición inválida se publica.** Si una corrida se estropea (cuota del servicio,
  reinicio, cobertura incompleta), se declara el motivo y se repite; no se publica su métrica.
- **No se reinician corridas con punto de control** para «optimizar» la concurrencia: ya dejó una cobertura
  incompleta que hubo que rehacer en un directorio limpio.
- **Los modelos excluidos del estudio no vuelven**, ni en los datos ni en una glosa que los declare fuera.
- Entregad los datos crudos y los `run_config.json`. **El veredicto lo redacta el equipo principal**, para
  que quede una sola voz en el informe.
