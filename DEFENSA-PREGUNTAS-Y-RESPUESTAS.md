# Preguntas probables de la mesa, y dónde está la respuesta calculada

**2026-09-08.** No es un guion de defensa ni sustituye al criterio del autor. Es un índice: para cada objeción
que un tribunal puede plantear con fundamento, dice **si la respuesta ya está calculada y dónde**, de modo
que no haya que improvisarla ni recalcularla en el momento.

Se ha escrito porque el trabajo de revisión de hoy produjo respuestas a varias objeciones que nadie ha
planteado todavía, y esas respuestas se pierden si quedan repartidas entre hallazgos.

---

## Lo primero: la tesis central cambió con el corpus corregido

**Esta sección es posterior a las demás y las condiciona.** El 2026-09-09 terminó la re-corrida completa sobre
el corpus con las tres categorías anotadas, y el hallazgo central del trabajo no sobrevive en la forma en que
está escrito. Conviene leerlo antes que nada, porque varias respuestas de más abajo se apoyan en las cifras
antiguas.

**«Su tesis es que el beneficio del RAG decrece con la capacidad del modelo. ¿Lo sostienen los datos?»**
**Sobre el corpus corregido, no en esa forma.** La correlación entre capacidad base y mejora pasa de Spearman
−0,5165 a **−0,0879 (p = 0,7752)**: el coeficiente de rangos se va a cero. El de Pearson queda en −0,5266
(p = 0,0645), pero **descansa en un solo punto**: retirando `nemotron-mini:4b` cae a +0,0120 con p = 0,971,
mientras que retirar cualquier otro modelo lo deja entre −0,52 y −0,67.

**Lo que sí sostienen los datos, y hay que decirlo así:** **tres** modelos mejoran de forma significativa
tras el post-hoc pareado sobre el corpus corregido —`nemotron-mini:4b` con +14,23 pp, `llama3.2:latest` con
+6,73 y `gemma4:12b-mlx` con +2,29—, el resto apenas se mueve, y **ningún modelo grande empeora**. Los dos
primeros son de los más pequeños del estudio. Es más modesto que «inversamente proporcional» y es
verdadero. Y es exactamente lo que justifica la arquitectura en dos niveles del capítulo 6, de modo que **el
argumento práctico del trabajo no depende de la forma funcional que se cae**.
→ `FINDINGS §F86` · `INVENTARIO-AFECTADO-POR-F86-20260909.md`

**«El informe dice que el efecto es nulo o adverso en los modelos mayores.»**
Eso **era cierto sobre el corpus defectuoso y no lo es sobre el corregido**. Los cinco modelos de mayor
capacidad tienen todos mejora positiva: +0,81, +0,97, +2,29, +1,67 y +2,53. La afirmación está en el resumen,
en el abstract, en §5.3.1 y explicada en §6, y hay que rectificarla en los cuatro sitios.

**«¿Y por qué cambia tanto?»**
Porque el corpus anterior **no anotaba localizaciones** mientras el prompt las pedía, de modo que toda
localización extraída contaba como falso positivo: el 66 % de todos los falsos positivos del estudio. Los
modelos que más localizaciones emitían salían más castigados, y eso no era una propiedad suya sino del
corpus. Corregida la anotación, el efecto se recoloca.
→ `FINDINGS §F53`

**«¿Su mayor resultado, el +14,5 de `nemotron-mini`, es fiable?»**
**No del todo, y lo sabemos.** En la re-corrida su línea base incluye **diecisiete registros que puntúan cero
por un `TypeError` del arnés** —`llm_runner.py:167`, que asume que el modelo devuelve un objeto JSON y falla
si devuelve un array—, y **todos caen en la línea base, ninguno en el brazo con RAG**, porque el ejemplar del
prompt de recuperación guía al modelo al formato correcto. Descontándolos, su Δ pasa de +14,23 a **+9,58 pp**.

Sigue siendo el mayor efecto del estudio y sigue siendo significativo en ambos escenarios. Está pedido
re-ejecutar ese brazo antes de fijar cifras. **Ningún otro modelo está afectado**: es el único error de las
treinta y nueve corridas, y los datos publicados tienen cero fallos.
→ `FINDINGS §F85` · `remote_48g/ALERTA-NEMOTRON-BASELINE-20260909.md`

## Sobre la estadística

**«¿Por qué un ANOVA de una vía sobre observaciones que no son independientes?»**
Es la objeción más probable, y el informe la declara él mismo como limitación. La respuesta añadida: se
repitió con el contraste que corresponde al diseño, **Friedman**, y el rechazo se sostiene con
χ² = 1 169,23 (p = 6,25 × 10⁻²³¹) frente al p = 3,45 × 10⁻¹⁶⁰ del ANOVA. **La conclusión no depende de la
elección.** Los dos estadísticos no son comparables entre sí, de modo que no procede decir que uno tenga más
potencia; lo que se afirma es que ambos rechazan.
→ `FINDINGS §F75` · `results/ROBUSTEZ_ESTADISTICA_20260908/friedman.json`

**«Esa correlación de −0,52 entre capacidad y beneficio, ¿no es un artefacto? El Δ contiene la línea base.»**
Buena objeción, y comprobada. Simulada la nula correcta —efecto del RAG independiente de la capacidad, cinco
mil repeticiones—, la ρ tiene mediana −0,005 e intervalo [−0,484, +0,462]. El valor observado cae fuera:
solo el **3,72 %** de las simulaciones llega a ser tan negativo. **No es artefacto.**
→ `FINDINGS §F74.bis` · `results/CORRELACION_CAPACIDAD_20260908/correlacion.json`

**«¿Por qué citan Spearman y no Pearson?»**
Porque discrepan y el informe **lo declara**: Spearman da −0,5165 (p = 0,0707, no significativo) y Pearson
−0,6004 (p = 0,0300, significativo). Citar solo uno sería seleccionar el resultado. La causa de la
discrepancia es el tamaño de muestra: con trece modelos el contraste está al límite.
→ `FINDINGS §F74`

**«Con trece modelos, ¿tienen potencia para afirmar eso?»**
Para la correlación principal, al límite: haría falta n ≥ 15 para que Spearman alcanzara p < 0,05. El informe
lo presenta por ello como **tendencia y no como efecto demostrado**. Para el contraste de las dos
compilaciones de 31B sobre N=30 la potencia es del **8 %** ante el efecto observado, y el texto lo declara.
→ `FINDINGS §F73`, `§F77` · `results/ROBUSTEZ_ESTADISTICA_20260908/potencia_contrastes.json`

**«El post-hoc dice que solo dos modelos mejoran. ¿No es demasiado conservador?»**
Sí, y está medido. El Tukey publicado corrige por las **325** comparaciones entre los veintiséis grupos
cuando las de interés son **trece**. Con el contraste pareado y corrección de Holm sobre esas trece,
**mejoran ocho de trece** sobre los datos publicados, y los cinco que no lo hacen son exactamente los de
efecto nulo o negativo. **Decisión del autor pendiente** sobre si el informe lo adopta.

**Aviso, porque estas dos cifras conviven y se confunden:** ese «ocho de trece» es sobre el **corpus
antiguo**. Sobre el **corregido** el mismo contraste da **tres de trece** —`nemotron-mini:4b`,
`llama3.2:latest` y `gemma4:12b-mlx`—. No es que el post-hoc sea más o menos conservador: es que el efecto
del RAG es mucho menor cuando el corpus anota las localizaciones que el prompt pide.
→ `FINDINGS §F76` · `results/ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json`

---

## Sobre los datos y la medición

**«¿Cómo puede el 66 % de sus falsos positivos venir de una categoría que el corpus no anota?»**
Es un defecto real del estudio, medido y declarado: 12 852 de 19 464. El informe lo explica en §3.3, acompaña
cada resultado de una medición restringida a las categorías anotadas, y el defecto **está corregido en el
corpus** desde el 2026-09-08, con la re-corrida en marcha.
→ `FINDINGS §F53`, `§F58`, `§F69` · `results/COMPOSICION_FP_20260908/`

**«Han medido dos veces varios modelos. ¿Por qué publican unas cifras y no otras?»**
El Anexo I lo declara con su motivo y su evidencia. De ocho grupos con más de una corrida, seis son
mediciones **inválidas** —el modelo no llegó a responder— y sus cifras no se publican; dos son repeticiones
válidas y se dan ambas. En una de ellas la publicada da **menos** que la sustituida, lo que acredita que el
criterio fue la validez y no el resultado.
→ `FINDINGS §F61`, `§F62`

**«¿El corpus está en español, como dice la hipótesis?»**
Parcialmente, y el informe lo declara: 105 de los 120 artículos proceden de CoNLL-2002 en español y los otros
quince de un conjunto europeo en inglés. La afirmación se ancla al corpus N=120.
→ `FINDINGS §F54`

**«¿Y el mojibake? ¿No invalida las cifras?»**
Afecta a 283 de 1 406 entidades de referencia, y el corpus es **internamente coherente**: el texto de entrada
lleva la misma corrupción, de modo que un modelo que transcribe literalmente coincide. El efecto medido
oscila entre −0,070 y +0,025 de F1 según el modelo, y los corpus N=15 y N=30 están limpios.
→ Anexo H del informe · `FINDINGS §F46`

---

## Sobre las cifras económicas

**«¿De dónde sale el 99,4 % de reducción de coste? ¿Lo han medido?»**
No, y el informe lo dice con todas las letras: **son estimaciones, no mediciones**. Los 0,052 dólares por
artículo reparten la amortización del equipo a un año (0,050) más el consumo eléctrico (0,002), de modo que
**no miden cómputo** y por eso son idénticos en las tres filas de la tabla. Los 8,75 dólares de la revisión
manual resultan de valorar el tiempo de un analista en 35 dólares por hora y estimar quince minutos por
noticia, **ambos de observación interna del proceso vigente en Austranet y no de una fuente publicada**. Las
dos cosas están declaradas en §5.5 y en la conclusión 4. Presentarlas como medición sería lo indefendible;
presentarlas como estimación con sus parámetros a la vista es lo correcto.

**«El objetivo dice 60–80 % y el resultado 99,4 %. ¿En qué quedamos?»**
Son dos magnitudes distintas y el informe las separa: **99,4 % es la reducción del coste unitario directo**
—0,052 frente a 8,75— y el **60–80 % se refiere al coste operativo total, que incluye la supervisión
humana**. La distinción se introdujo tras la auditoría del 2026-09-03 (hallazgo M9), y por eso la afirmación
se retiró del resumen.

**Y aquí hay que ser honesto, porque es el flanco real:** el informe **no deriva** ese 60–80 %. Es el rango
que fijaron los objetivos al principio del trabajo, no un resultado calculado a partir de los datos. La
respuesta defendible es esa misma: el estudio estima el coste unitario con sus parámetros declarados, y
advierte de que el ahorro total **depende de cuánto reduzca el sistema el volumen que llega a revisión
humana**, algo que este trabajo **no midió** porque exigiría un despliegue en producción con analistas. Quien
pregunte por el 60–80 % está señalando una limitación declarada, no un error.

**Lo que no conviene hacer** es defender el 60–80 % como si tuviera respaldo empírico. No lo tiene, y sostenerlo
convierte una limitación honesta en una cifra atacable.

## Sobre defectos de la medición que el propio trabajo encontró

**«He mirado sus datos crudos y hay registros con exhaustividad mayor que 1. ¿Cómo lo explica?»**
Es correcto, hay **197**, y el máximo es **2,444**. La causa está localizada en el código: el emparejamiento
incrementa los aciertos **por cada entidad extraída que casa**, mientras cuenta los fallos sobre las
referencias **distintas** casadas. Cuando dos extracciones casan con la misma referencia —«John Smith» y
«Smith, John», iguales para el emparejamiento difuso al 85 %— el acierto se cuenta dos veces. La precisión no
está afectada, porque cada entidad extraída contribuye como mucho una vez.

**Y está cuantificado.** Recalculado contando cada referencia una sola vez, sin reejecutar inferencia: el F1
está inflado **+0,160 pp de media** y **+1,287 pp** como máximo, siempre al alza; **ninguna** de las trece
mejoras cambia de signo, y **los dos únicos Δ significativos crecen** —`llama3.2` de +10,82 a +10,91 y
`nemotron-mini` de +14,52 a +15,75—. Queda muy por debajo del umbral de 0,02 en F1 que el proyecto declara
tolerable. La tabla completa está calculada.
→ `FINDINGS §F81`, `§F81.bis` · `results/EMPAREJAMIENTO_DUPLICADO_20260908/tabla7_recalculada.md`

**«¿Por qué no lo corrigieron y volvieron a medir?»**
Porque el barrido de sustitución estaba en marcha con ese mismo evaluador. Corregirlo a mitad habría dejado
los modelos ya terminados medidos con un criterio y los restantes con otro, y **la homogeneidad del barrido
vale más que la corrección de la métrica, porque la corrección se puede aplicar después y la homogeneidad no
se recupera**. La corrección no necesita reejecutar inferencia: se despeja del propio dato.

**«La Tabla 4 y el resto del capítulo, ¿están medidas igual?»**
No, y la glosa de la tabla lo declara: la Tabla 4 se midió sobre N=15 en modo `entities`, mientras el estudio
principal usa `kb_combined` sobre N=120. Son dos conjuntos de evaluación distintos y el §5.1 lo advierte
expresamente al presentarlos.

**«Excluyen siete artículos por contaminación, pero solo contaminaban el modo con recuperación. ¿Por qué los
quitan también de la línea base?»**
Buena pregunta, y la respuesta es deliberada. Los siete son los ejemplares *few-shot* del propio corpus, de
modo que solo contaminan `kb_fewshot` y `kb_combined` —el manifiesto lo declara así, en su campo
`excluded_from_metric_modes`—. Se excluyen igualmente de la línea base **para que ambos brazos se midan sobre
los mismos 113 artículos**. Si no se hiciera, la comparación base contra RAG sería entre poblaciones distintas
y el emparejamiento por registro, que es lo que sostiene el contraste de Wilcoxon y el ANOVA de medidas
repetidas, dejaría de ser posible. Quitar siete artículos a ambos lados cuesta poco; compararlos sobre
conjuntos distintos invalidaría el contraste.

**«¿Cómo sé que las cifras del seguimiento salen de los datos y no de un resumen que quedó viejo?»**
Porque se ha comprobado. Los **66 grupos** de los once modelos rehechos —tres corpus cada uno— se
recalcularon desde los `benchmark_results.csv` crudos, excluyendo los siete contaminados, y **coinciden con
sus `benchmark_summary.json` sin una sola discrepancia**, tanto en la media de F1 como en el recuento de
registros.

## Sobre la reproducibilidad

**«¿Puedo reproducir sus cifras?»**
Sí, y hay herramienta para cada tabla: `tools/verificar_informe.py` ejecuta veintidós comprobaciones que atan
cada tabla y cada figura del informe a los datos de los que salen, incluidas las URL de la bibliografía.
→ `doc/prompts/00-revision-completa.md`

**«¿Por qué el repositorio que citan no responde?»**
Porque a esta fecha es privado. Es un **pendiente declarado** y bloqueante para la entrega.
→ `TODO-INFORME-FINAL.md`, sección del bloqueante [37]

---

## Sobre la tasa de alucinación y el objetivo 5

**«Su objetivo 5 fija una tasa de alucinaciones inferior al 5 %. ¿Lo cumplieron?»**
**Parcialmente, y el informe da los datos para verlo aunque no lo formule como un sí o un no.** §5.4 declara
el rango completo: de **cero** en las variantes alojadas de `gemma4:31b` al **21,59 %** de `deepseek-r1:1.5b`
con recuperación por diccionario, con **28 de 61 grupos por debajo del 1 %**. El umbral se cumple en la gran
mayoría de configuraciones y **se incumple en los dos modelos más pequeños**, que es donde el informe sitúa
expresamente el problema.

**La respuesta honesta** es que el objetivo se alcanza para las configuraciones que el capítulo 6 propone
desplegar, y no para los modelos más pequeños, que el propio trabajo descarta para uso en producción por su
F1. Presentarlo como un cumplimiento global sería falso y es innecesario: la conclusión práctica no depende de
ello.

**Cifras de la re-corrida sobre el corpus corregido**, con doce de los trece modelos y por tanto provisionales:
el máximo baja a **15,61 %** (`deepseek-r1:1.5b` con KB RAG) y **21 de 24 grupos quedan por debajo del 5 %**,
quince de ellos por debajo del 1 %. Los tres que lo superan son las dos configuraciones de `deepseek-r1:1.5b`
y `gemma:latest` con KB RAG, esta última en 5,14 %. **El cuadro cualitativo no cambia**: el problema sigue
concentrado en los modelos pequeños.

## Sobre la bibliografía

**«¿De dónde salen el 88,43 % y el 82,1 % del §2?»**
De [7] y [15], y **ambas están verificadas contra las tablas de los propios artículos** (2026-09-09):

- **88,43 %** es el F1 de **BETO *cased*** en NER sobre **CoNLL-2002 en español**, en la **Tabla 1** de [7].
  El artículo lo marca con asterisco como **nuevo estado del arte** en ese *benchmark*, por delante del mejor
  mBERT (87,38) y de la variante *uncased* (82,67). El informe dice «con un codificador monolingüe», que es
  exactamente lo que BETO es.
- **82,1 %** es el **micro-F1 de `sec-bert-shape` sobre el conjunto de prueba de FiNER-139**, en la **Tabla 4**
  de [15]; su macro-F1 es 80,1. El artículo describe su tarea como «*word-level tagging of financial numeric
  expressions with XBRL entity types*», que confirma literalmente la salvedad del informe: **etiquetar
  magnitudes según la taxonomía XBRL y no identificar personas y organizaciones**.

Si preguntan por el modelo concreto detrás del 82,1 —el informe no lo nombra— la respuesta es `sec-bert-shape`.

**Contexto que obliga a ser especialmente cuidadoso aquí.** La verificación del 2026-09-08 encontró que
**cuatro referencias no correspondían a ninguna obra existente** —[7], [9], [10] y [15]—, y dos de ellas
sostenían precisamente una afirmación del estado del arte. Las cuatro se sustituyeron por obras reales y el
texto se reescribió con precisión: [15] declara ahora que la tarea de FiNER es etiquetar magnitudes según la
taxonomía XBRL «y no identificar personas y organizaciones», que es la corrección exacta que el hallazgo
pedía. **El problema está resuelto**, y por eso mismo las cifras que quedan merecen comprobarse hasta el
final.
→ `FINDINGS §F51` · comprobación de que las URL responden: `python3 tools/verificar_informe.py --red`

## Lo que no tiene respuesta calculada, y conviene saberlo

- **Por qué las latencias de la re-corrida difieren tanto de las publicadas.** Ocho de diez pares bajan,
  algunos hasta ×0,02, en la misma máquina. Descartadas la máquina y el modo de razonamiento; sin explicación
  cerrada. Si se pregunta por eficiencia, conviene ceñirse al índice Tok/s/B y declarar la salvedad.
  → `FINDINGS §F71`
- **Si el efecto del RAG converge o no** con el corpus corregido. Ocho de trece modelos rehechos; los dos de
  mayor efecto siguen pendientes. Hasta que lleguen, cualquier afirmación sobre el patrón es prematura.
  → `FINDINGS §F68.ter`
