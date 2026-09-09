# Preguntas probables de la mesa, y dónde está la respuesta calculada

**2026-09-08.** No es un guion de defensa ni sustituye al criterio del autor. Es un índice: para cada objeción
que un tribunal puede plantear con fundamento, dice **si la respuesta ya está calculada y dónde**, de modo
que no haya que improvisarla ni recalcularla en el momento.

Se ha escrito porque el trabajo de revisión de hoy produjo respuestas a varias objeciones que nadie ha
planteado todavía, y esas respuestas se pierden si quedan repartidas entre hallazgos.

---

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
**mejoran ocho de trece**, y los cinco que no lo hacen son exactamente los de efecto nulo o negativo.
**Decisión del autor pendiente** sobre si el informe lo adopta.
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

## Sobre la reproducibilidad

**«¿Puedo reproducir sus cifras?»**
Sí, y hay herramienta para cada tabla: `tools/verificar_informe.py` ejecuta veintidós comprobaciones que atan
cada tabla y cada figura del informe a los datos de los que salen, incluidas las URL de la bibliografía.
→ `doc/prompts/00-revision-completa.md`

**«¿Por qué el repositorio que citan no responde?»**
Porque a esta fecha es privado. Es un **pendiente declarado** y bloqueante para la entrega.
→ `TODO-INFORME-FINAL.md`, sección del bloqueante [37]

---

## Lo que no tiene respuesta calculada, y conviene saberlo

- **Por qué las latencias de la re-corrida difieren tanto de las publicadas.** Ocho de diez pares bajan,
  algunos hasta ×0,02, en la misma máquina. Descartadas la máquina y el modo de razonamiento; sin explicación
  cerrada. Si se pregunta por eficiencia, conviene ceñirse al índice Tok/s/B y declarar la salvedad.
  → `FINDINGS §F71`
- **Si el efecto del RAG converge o no** con el corpus corregido. Ocho de trece modelos rehechos; los dos de
  mayor efecto siguen pendientes. Hasta que lleguen, cualquier afirmación sobre el patrón es prematura.
  → `FINDINGS §F68.ter`
