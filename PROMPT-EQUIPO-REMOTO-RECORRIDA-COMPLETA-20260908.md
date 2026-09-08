# Encargo al equipo remoto de 48 GB — re-ejecución completa del estudio

**Fecha:** 2026-09-08. **Solicitado por:** el autor. **Verdad de referencia:** el informe entregado al
profesor guía, en `doc/versions/enviados/`. Todo lo que este encargo dice se subordina a ese documento.

**Antes de cualquier cosa: la historia del repositorio se reescribió.** Se purgó una credencial con
`git filter-repo` y se forzó el empuje, de modo que **vuestro clon es incompatible con el remoto**. Un `pull`
os fallará. Clonad de nuevo antes de empezar, y tened en cuenta que `.setenv.sh` no está en git: hay que
reponerlo a mano.

---

## 1. Por qué se pide repetir el estudio

Una segunda pasada de revisión, con seis auditores independientes y un orquestador, encontró **172 hallazgos,
61 de ellos graves**. La aritmética del trabajo resistió —cinco auditores recalcularon el ANOVA por separado y
coincide hasta la centésima con lo publicado—, pero apareció un defecto de medición que afecta a **todas** las
cifras y que no se puede corregir editando el texto. Está documentado en `FINDINGS.md §F53`.

**El defecto.** Los cuatro *prompts* del sistema ordenan extraer tres categorías de entidad —personas,
organizaciones y localizaciones— y **ningún corpus anota localizaciones**: el campo está vacío en los ciento
veinte registros. Como el evaluador puntúa las tres, toda localización que el modelo devuelve se contabiliza
como falso positivo sin que exista forma de acertar en ella. **20 946 de los 32 201 falsos positivos del
estudio, el 65 %, venían de ahí.**

La corrección publicada en paralelo (Anexo I del informe) reagrega desde los desgloses ya almacenados y sube
el F1 entre 0,5 y 15 puntos según el modelo. Pero es una corrección de escritorio: **lo limpio es alinear lo
que el prompt pide con lo que el corpus anota y volver a medir**, y eso exige repetir la inferencia.

---

## 2. Lo que hay que arreglar antes de lanzar nada

### 2.1 Alinear prompts y anotación (bloqueante)

Dos caminos, y el autor prefiere el primero:

1. **Retirar `Locations` de los cuatro prompts del sistema** —`SYSTEM_PROMPT.md`, `SYSTEM_PROMPT_ES.md`,
   `SYSTEM_PROMPT_EN_FEWSHOT.md` y `SYSTEM_PROMPT_ES_FEWSHOT.md`— y de los ejemplos *few-shot* que la
   incluyen, dejando el esquema de salida en dos categorías. Es lo que mide el corpus.
2. Anotar las localizaciones de los tres corpus. Es metodológicamente superior y exige anotación experta que
   no está disponible.

Si se toma el camino 1, comprobar que `src/evaluator.py` deja de puntuar la categoría: hoy la incluye en
`types` en las líneas 45 y 211.

**Comprobación obligatoria antes de aceptar cualquier corrida nueva:** para cada categoría puntuada, el `fn`
agregado debe ser mayor que cero. Si vale cero mientras `fp` crece, esa categoría está puntuando contra el
vacío y la corrida no sirve.

### 2.2 Normalizar la codificación en ambos lados (bloqueante)

`FINDINGS.md §F53`, `§F56` y `§F57`. El corpus N=120 almacena los nombres con *mojibake* —`JosÃ© Bono` donde
el nombre real es **José Bono**—, y el defecto está a la vez en la referencia (20,1 % de las entidades) y en
el texto de entrada (87 % de los artículos).

Lo importante es que **el sentido del sesgo depende de dónde esté la corrupción**, y eso está medido:

| Criterio | Efecto |
|:---|:---|
| Referencia corrupta | **19 de 24 grupos puntúan mejor**: el cotejo premia copiar los bytes y castiga escribir bien el nombre |
| Texto de entrada corrupto | **19 de 24 puntúan peor**: dificulta la extracción para todos |

Los dos efectos se contraponen y se cancelan, y de ahí sale una consecuencia que hay que verificar en la
re-corrida: **la ventaja del prompt en español desaparece precisamente sobre el corpus con más entidades
hispanas**, porque allí la competencia lingüística se vuelve desventaja frente a una referencia corrompida.

La tarea es **reparar la codificación de los tres corpus, en la referencia y en el texto**, dejando los
nombres en UTF-8 correcto, y volver a medir. El script `tools/analisis_mojibake.py` reproduce la medición
actual y sirve de referencia para comprobar que después de la reparación el efecto desaparece.

### 2.3 El defecto de doble emparejamiento

`FINDINGS.md §F49` y `§F50`. En `src/evaluator.py:84-94`, los aciertos se cuentan **por entidad extraída**
mientras las omisiones se cuentan **por entidad de referencia**, de modo que dos extracciones que casen con un
mismo elemento del gold suman dos aciertos e **inflan la exhaustividad**. Se detecta buscando registros con
`recall > 1.0`, pero ese indicador **subestima la incidencia entre tres y diez veces**, porque solo captura
los casos que rompen el techo de la métrica. La incidencia real llega al 33 % de los registros en algunas
corridas.

Corregir contando los aciertos contra el conjunto de entidades de referencia ya emparejadas, no contra la
lista de extracciones.

### 2.4 El umbral de alucinación que se descarta en silencio

`FINDINGS.md §F50`. `evaluate_single_record` llama a `calculate_hallucination_rate(extracted, source_text)`
sin propagar el umbral configurado (`evaluator.py:302`), de modo que el 85 de `BenchmarkConfig` se ignora y se
usa el 70 por omisión. Propagarlo o documentar explícitamente que la tasa de alucinación usa un umbral
distinto del cotejo.

### 2.5 Los parámetros que el proveedor descarta sin avisar

`FINDINGS.md §F45`. El argumento `think` es de primer nivel en `Client.chat()` y **no** una clave de
`options`: dentro de `options` Ollama lo descarta en silencio y el modelo corre con su valor por omisión, que
en los modelos con razonamiento está activado. Y `num_predict` corto produce contenido vacío que dispara el
respaldo y acaba en extracción vacía, lo que parece un fallo del modelo y es del arnés: con 2048 `gpt-oss`
daba 67 respaldos, con 4096 bajó a 2.

Antes de la re-corrida, **volcar la configuración efectiva que recibe el proveedor** y comprobarla contra
`run_config.json`, no fiarse de lo que el código pretende enviar.

---

## 3. La investigación que el autor pide expresamente

### 3.1 El corpus N=30 y el idioma

`FINDINGS.md §F54`. Los dos corpus del dominio están **íntegramente en inglés**: `kleptotrace.json` da cero de
quince artículos en español y `kleptotrace_augmented_30.json` cero de treinta. El único corpus con material
español es el N=120, con 105 de sus 120 artículos.

Pero el **Anexo F del informe transcribe un prompt generador redactado en español** cuya salida versionada
está en inglés. O el prompt transcrito no es el que se ejecutó, o el corpus versionado no es el que ese prompt
generó. **Hay que determinar cuál de las dos cosas ocurrió**, buscando en los registros de ejecución de julio
la invocación real del generador, y documentarlo. Es la única forma de saber si el corpus N=30 responde al
diseño declarado.

Si el generador se lanzó en inglés por error, **regenerar el corpus N=30 en español** es la tarea derivada, y
cambia el sentido de todo el experimento del dominio.

### 3.2 Las entidades ibéricas y la mejora del prompt en español

`FINDINGS.md §F56`. Este es el hallazgo más interesante y el que menos comprobado está. Medido:

| Corpus | Personas | De aspecto ibérico | Organizaciones | De aspecto ibérico |
|:---|---:|---:|---:|---:|
| N=15 | 84 | **12 (14 %)** | 128 | 3 (2 %) |
| N=30 | 36 | 1 (3 %) | 69 | 0 |
| N=120 | 594 | **263 (44 %)** | 812 | 198 (24 %) |

El corpus de quince artículos está en inglés y sin embargo el *prompt* en español mejoraba el resultado. La
hipótesis que los datos soportan es que la instrucción en español **no ayuda a leer el texto sino a delimitar
la minoría de nombres ibéricos**, casi todos portugueses y procedentes de un caso de corrupción angoleño
—`Isabel dos Santos`, `Hélder Pitta Grós`, `Mario Leite da Silva`—, con partículas y acentos donde un
tokenizador anglocéntrico parte la entidad en dos.

**Lo que hay que hacer para confirmarlo o descartarlo:** medir el efecto del idioma del prompt **por separado
sobre las entidades ibéricas y sobre las anglosajonas**, dentro del mismo corpus. Si la hipótesis es correcta,
la ventaja debe concentrarse en el subconjunto ibérico y desaparecer en el anglosajón. Es un contraste
limpio, no exige corpus nuevo y resolvería de una vez un hallazgo que hoy se sostiene sobre una correlación.

### 3.3 El efecto del prompt en español no replica

`FINDINGS.md §F55`. Hay **tres corridas** del mismo experimento y el informe citaba solo la más favorable:

| Corrida | Corpus | zs-en | fs-es | Diferencia |
|:---|:---|---:|---:|---:|
| `ablacion_n15_REMOTO` | N=15 | 67,52 % | 77,92 % | **+10,40 pp** |
| `kleptotrace_20260727_110454` | N=15 | 66,76 % | 69,87 % | +3,11 pp |
| `benchmark_balanced_120_20260825_071207` | N=120 | 54,46 % | 54,02 % | **−0,43 pp** (p = 0,9328) |

Las dos primeras usan el mismo modelo, el mismo corpus, semilla 42 y temperatura 0,1, y difieren en siete
puntos. **Repetir la ablación con réplicas, al menos cinco por celda, con semillas declaradas**, sobre los dos
corpus, y reportar la media y la dispersión. Sin réplicas no se puede decidir si el efecto existe.

---

## 4. Modelos: lista cerrada

**No incluir en ninguna corrida** `nuextract:latest`, `minimax-m3:cloud`, `gemini-3.1-flash-lite`,
`gemini-3.5-flash`, `phi3.5`, `gliner:medium`, `sonct988/gemma4-26b` ni la etiqueta `gemma4-12b-mlx-q8-64k`,
que medía `gemma4:12b-mlx` con un sufijo de cuantización falso. Ver `CLAUDE.md`, sección «Modelos excluidos
del estudio: lista cerrada». Sus filas ya se retiraron de los datos y del informe, y **no deben reaparecer**.

Los modelos del estudio son los que declara el informe entregado. Cualquier duda se resuelve contra ese PDF.

---

## 5. Protocolo de la re-corrida

Sobre el corpus N=120 con la codificación reparada, en los dos modos —extracción directa y `kb_combined`—,
con `temperature=0.1`, `seed=42`, `fuzzy_threshold=85` y `num_predict` suficiente para que ningún modelo
agote el presupuesto. Un modelo por turno, que es la condición que garantiza telemetría limpia en una GPU de
memoria unificada.

**Entregar por corrida:** `benchmark_results.csv`, `detailed_results.json` con el desglose por tipo,
`run_config.json` con la configuración efectiva, `benchmark_summary.json`, el informe estadístico y **el
`benchmark.log` completo**. Los registros de ejecución **no se recortan ni se filtran por ningún motivo**: son
la prueba de qué se ejecutó, y este proyecto ya los ha necesitado para diagnosticar fallos. Ver `CLAUDE.md`,
sección «Los registros de ejecución se conservan».

**Verificaciones que hay que pasar antes de declarar una corrida válida**, y reportarlas explícitamente:

1. `fn` agregado mayor que cero en **cada** categoría puntuada.
2. Cero registros con `recall > 1.0`.
3. Ninguna fila con F1 mayor que la media de precisión y exhaustividad.
4. Recuento de `parse_method='failed'` y de `recall=0` por modelo, con su causa: latencia cero y cero tokens
   es rechazo de infraestructura; latencia alta con contenido vacío es que el arnés pierde la respuesta.
5. Los nueve parámetros de `run_config.json` coincidiendo con la corrida de referencia.
6. Al promediar desde JSON, usar `if x.get('k') is not None` y **nunca** `if x.get('k')`: un `0.0` es falsy y
   descartaría las filas en cero, inflando la media.

---

## 6. Qué esperar del resultado

Con el defecto de `Locations` corregido, el mejor local sobre el corpus español debería situarse **en torno al
77 %** de F1, frente al 62,67 % publicado, y superar el umbral del 70 % que fija la hipótesis. La variante en
la nube debería seguir por delante, alrededor del 81 %, de modo que **la conclusión de que la soberanía cuesta
unos cinco puntos se mantiene**. Si la re-corrida arroja cifras muy distintas de estas, es señal de que algo
más cambió, y hay que averiguar qué antes de dar los números por buenos.

Con la codificación reparada, el efecto diferencial del *mojibake* debe **desaparecer**: si sigue apareciendo,
la reparación fue incompleta.

---

## 7. Documentación de vuelta

Actualizar `remote_48g/REPORTE-FINAL.md` con lo hecho, declarar la tarea en `CURRENT-TASKS.md §3.bis` antes de
empezar y al terminar, y anotar en `research/rag/WORKLOG.md`. Si algo del encargo resulta imposible o
contradictorio, **decirlo antes de ejecutar** en lugar de resolverlo por criterio propio: varias de las
inconsistencias que este encargo repara nacieron de decisiones razonables tomadas sin consultar.
