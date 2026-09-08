# Encargo al equipo remoto de 48 GB — re-ejecución completa del estudio

**Fecha:** 2026-09-08. **Solicitado por:** el autor. **Verdad de referencia:** el informe entregado al
profesor guía, en `doc/versions/enviados/`. Todo lo que este encargo dice se subordina a ese documento.

**Antes de cualquier cosa: la historia del repositorio se reescribió.** Se purgó una credencial con
`git filter-repo` y se forzó el empuje, de modo que **vuestro clon es incompatible con el remoto**. Un `pull`
os fallará. Clonad de nuevo antes de empezar, y tened en cuenta que `.setenv.sh` no está en git: hay que
reponerlo a mano.

---

## 0. Disparador de ejecución

**TURK_182_GOGO**

Esta palabra es la orden de ejecución. Su presencia en este documento significa que **las revisiones globales
del informe han terminado** y que el equipo de 48 GB debe **volver a correr todos los benchmarks** con las
correcciones que este encargo detalla.

El autor fijó el protocolo así a propósito: la palabra no se escribió mientras las revisiones estaban en
curso, precisamente para que su aparición no pueda confundirse con un aviso preparatorio. Si estáis leyendo
esto, la condición se cumplió.

**Antes de lanzar, leed las secciones 2 y 4.** La sección 2 enumera cinco defectos de código que hay que
reparar primero, y lanzar sin repararlos produciría otra vez cifras que habría que descartar. La sección 4
fija la lista cerrada de modelos: ocho nombres que no deben aparecer en ninguna corrida.

---

**Condición cumplida.** Las tres rondas de revisión global del informe han terminado. La última cerró con
199 hallazgos y 75 graves, y su veredicto íntegro está en
[`VEREDICTO-REVISION-GLOBAL-20260908.md`](./VEREDICTO-REVISION-GLOBAL-20260908.md). Cuatro de esos hallazgos
son defectos de código que **invalidarían esta re-corrida si no se reparan antes de lanzarla**, y están en la
sección 2.bis, que se añadió después de redactar el resto de este encargo. **Leedla antes que nada.**

Conviene que sepáis el estado del informe, porque explica el encargo: el veredicto es **no listo para
entregar**, y una de sus razones es que la métrica actual no es defendible. La re-corrida no es un refinamiento
opcional: es lo que permite publicar cifras que resistan una defensa.

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

## 2.bis Defectos descubiertos en la tercera revisión global (2026-09-08, posteriores a la redacción de este encargo)

Cuatro hallazgos nuevos, todos verificados de forma independiente por el orquestador de la revisión. **Los
cuatro invalidarían la re-corrida si no se reparan antes de lanzarla**, igual que invalidaron la anterior.

### 2.bis.1 Contaminación del conjunto de prueba en la base de conocimientos (BLOQUEANTE)

Los siete ejemplares de `data/knowledge_base/few_shot_exemplars.json` llevan en su campo `source` la cadena
`benchmark_balanced_120.json#real_mixed_N`: **son artículos del corpus que se evalúa**, con su anotación de
oro como salida esperada. Afecta a los modos `kb_fewshot` y `kb_combined`, que son los del estudio principal.

El efecto está medido: el Δ del KB RAG sobre esos siete artículos es **+10,01 pp frente a +2,19 pp en los 113
restantes**, y el patrón se repite en las siete corridas sin excepción, de +5,29 en la variante alojada a
+31,41 en `nemotron-mini`. Las dos significancias de Tukey sobreviven al descuento, pero **la magnitud
publicada está inflada**.

Hay un segundo efecto: los ejemplares llevan `Locations` pobladas (`Bilbao`, `Iran`, `WASHINGTON`,
`Liberia`), de modo que la base de conocimientos **enseña al modelo a emitir justo la categoría que el cotejo
penaliza** como falso positivo.

**Tarea:** reconstruir los ejemplares con material **ajeno al corpus de evaluación** y retirar de ellos las
localizaciones. Si se prefiere conservarlos, hay que excluir esos siete artículos de la métrica y declararlo.

### 2.bis.2 CoNLL-2002 sí anota localizaciones: el defecto está en la conversión (BLOQUEANTE)

Corrige lo que la sección 2.1 de este encargo daba por supuesto. CoNLL-2002 anota cuatro tipos —PER, ORG,
LOC y MISC— y aporta 105 de los 120 artículos del corpus principal. **Las localizaciones existen**; lo que
las pierde es el conversor:

- `download_conll2002.py` conserva solo `name_entities` y `organizations`.
- `src/data_loader.py:117-120` escribe `"Locations": []` como **constante**.

De modo que para 105 de los 120 artículos **basta con no descartarlas al convertir**, y no hace falta
anotación experta. Eso cambia la tarea: en lugar de retirar `Locations` de los prompts, la vía limpia es
**recuperar las localizaciones de CoNLL-2002 en la conversión** y medir las tres categorías. Los quince
artículos de Kleptotrace seguirían sin anotarlas, y ese subconjunto sí habría que anotar a mano o excluir de
la métrica de esa categoría.

### 2.bis.3 `gpt-oss:20b` corrió con otro presupuesto de generación (BLOQUEANTE)

Entró en la Tabla 7 y en el ANOVA con **`max_tokens=4096`** mientras los otros doce modelos corrieron con
**2048**. Existe una corrida previa del mismo modelo y corpus con 2048 en `results/excluidos_n120_REMOTO`,
donde el Δ del RAG es **−9,65 pp (43,84 → 34,19)** frente al **+3,28 pp** publicado: **el signo del efecto se
invierte con el presupuesto**. Ni el parámetro ni la corrida descartada se declaran en el informe.

**Tarea:** correr los trece modelos con el **mismo** presupuesto, elegido de modo que ninguno lo agote, y
dejar constancia del valor en `run_config.json`. Comprobar tras la corrida que ningún modelo termina por
límite de tokens.

### 2.bis.4 La repuntuación de la extracción vacía no llegó a los JSON

La convención corregida —F1 = 0 y no 1 ante extracción vacía— se aplicó a los `benchmark_results.csv` pero
**no a los `detailed_results.json`**, que son precisamente los ficheros de los que se calculan los anexos.
Quedan **251 registros con F1 = 1,0** por extracción vacía en nueve corridas.

**Tarea:** aplicar la convención a los dos formatos y comprobar que ningún registro con extracción vacía
tiene F1 distinto de cero.

### 2.bis.5 Dos defectos de datos menores, para arreglar de paso

- Las **siete filas re-extraídas de `nemotron-mini`** tienen `latencia = 0`, `0 tokens/s` y, lo importante,
  **su `per_type` no cuadra con su `overall`**: faltan 26 falsos positivos. De ahí nacen dos denominadores
  distintos para el mismo recuento.
- El **análisis de sensibilidad por longitud atípica es vacío por construcción**: `src/statistics.py:189`
  fija el umbral en `avg_len + 500` y el corpus N=30 tiene media 202 y máximo 293 caracteres, de modo que el
  criterio de 702 no podía marcar nada. Sustituirlo por un criterio estadístico real, como el rango
  intercuartílico.

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
