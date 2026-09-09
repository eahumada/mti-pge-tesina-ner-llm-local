# Qué pasajes del informe desmienten los datos de la re-corrida

**2026-09-09.** `FINDINGS §F86` establece que la proporcionalidad inversa entre capacidad del modelo y
beneficio del RAG **no se sostiene sobre el corpus corregido**. Esa afirmación no vive en un solo sitio: se
enuncia en el resumen, se demuestra en el capítulo de resultados, se explica en el de discusión y se recoge en
las conclusiones. Este documento localiza cada pasaje, para que la reescritura sea un trabajo acotado y no una
relectura completa.

**Nada de esto se ha modificado.** Reescribir conclusiones es del autor, y además hay que esperar a que se
resuelva `§F85` —los diecisiete ceros del `TypeError` en la línea base de `nemotron-mini`— porque afectan
justamente al punto que más pesa en el análisis.

## Lo que los datos dicen ahora

| | Publicado | Re-corrida (13 modelos) |
|:---|---:|---:|
| Spearman ρ (capacidad vs Δ) | −0,5165 (p = 0,0707) | **−0,0879 (p = 0,7752)** |
| Pearson r | −0,6004 (p = 0,0300) | −0,5266 (p = 0,0645) |
| Pearson r sin `nemotron-mini` | — | **+0,0120 (p = 0,971)** |
| Δ de los cinco modelos mayores | negativos o nulos | **todos positivos**: +0,81 · +0,97 · +2,29 · +1,67 · +2,53 |

## Los pasajes afectados, por orden de gravedad

### 1. Resumen y abstract, primera página

Ambos dicen que el efecto del RAG «**es nulo o adverso en los mayores**» / «**is null or adverse in the larger
ones**». **Falso** sobre el corpus corregido: los cinco mayores mejoran. Y las dos cifras que citan, «+14,5 y
+10,8 puntos», pasan a **+14,2 y +6,7** en el consolidado nuevo, o a **+9,6 y +6,7** si se descuenta el
artefacto de `§F85`.

Recordatorio de norma: resumen y abstract se corrigen **en el mismo commit** y deben decir exactamente lo
mismo. Cada uno tiene un tope de 200 palabras, de modo que la sustitución ha de ser neutra en extensión.

### 2. §5.3.1 — el hallazgo central

La frase «el beneficio del KB RAG es **inversamente proporcional** a la capacidad del modelo» es la tesis del
apartado, y es la que el coeficiente de rangos deja de sostener. También la coletilla «se anula o revierte en
los de mayor capacidad».

**No se arregla cambiando cifras.** Lo que los datos permiten afirmar es más modesto y sigue siendo útil: dos
modelos pequeños se benefician de forma clara y **son los dos únicos significativos** tras el post-hoc
pareado; el resto apenas se mueve; y **ningún modelo grande empeora**.

### 3. §6 — la explicación del efecto

El párrafo de la «**redundancia de conocimiento**» —que los modelos de mayor capacidad ya han internalizado en
el preentrenamiento las reglas que la base de conocimiento aporta— es una explicación de un fenómeno que los
datos corregidos no muestran. Si el efecto no decrece con la capacidad, no hay nada que explicar por esa vía.
Puede conservarse como hipótesis sobre por qué los pequeños ganan más, que es lo que sí se observa, pero no
como explicación de un gradiente que no existe.

### 4. Conclusión 6 del §7

«El RAG contextual supera al RAG por diccionario» **no está afectada**: es una comparación entre dos
estrategias de recuperación, no entre capacidades. Se comprueba aquí para que no se reescriba por arrastre.

## Lo que NO está afectado, y conviene tenerlo claro

- **La conclusión 1, de viabilidad.** El umbral del 70 % se supera con más holgura en el corpus corregido, no
  con menos.
- **Las conclusiones 2, 3, 4, 5 y 7.** Localización lingüística, soberanía, costes, controlador AIMD y
  *mojibake* son independientes de la relación capacidad-beneficio.
- **La Tabla 8 y el capítulo 6 en lo que toca a eficiencia.** El índice Tok/s/B se mueve poco y la afirmación
  de los dos órdenes de magnitud aguanta (decisión 10).
- **El hecho de que el RAG ayude.** Sigue habiendo mejora significativa en dos modelos y ninguna degradación
  en los grandes. Lo que cae es la **forma funcional** de la relación, no su existencia en los pequeños.

## Dónde está ya publicado, y esto cambia el asunto

Las cuatro afirmaciones no están solo en el Markdown. Comprobado el 2026-09-09:

| Artefacto | «nulo o adverso» | «inversamente proporcional» | «se anula o revierte» | «redundancia de conocimiento» |
|:---|:---:|:---:|:---:|:---:|
| `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | sí | sí | sí | sí |
| `Informe_Final_Tesina_NER.docx` | sí | sí | sí | sí |
| **PDF entregado al profesor guía** (`doc/versions/enviados/`, 31 páginas) | **sí** | **sí** | **sí** | **sí** |

**El profesor ya tiene un documento que afirma algo que los datos corregidos desmienten.** No era un error
cuando se entregó —era lo que decían los datos de entonces— pero significa que la corrección **no se agota
editando el informe**: hay que comunicarla, y es mejor hacerlo por iniciativa propia que verse preguntado en
la defensa. Cómo y cuándo es del autor; lo que aquí se hace es dejarlo dicho.

### Qué cifras concretas tiene el profesor

Extraídas del PDF entregado: **las trece filas de línea base de la Tabla 7** están todas —62.38, 59.25,
56.18, 55.91, 52.39, 50.22, 48.76, 48.21, 44.00, 43.38, 36.11, 24.83 y 22.59— y el **ANOVA F = 38,2222**
también.

**Los coeficientes de correlación, en cambio, no aparecen**: ni 0,5165 ni 0,6004 ni sus valores *p*. Es
coherente con `FINDINGS §F74`, que descubrió el 2026-09-08 por la tarde —después de la entrega, que fue a las
05:07— que la ρ que sostiene el hallazgo central **vivía únicamente dentro de la imagen de la Figura 2**, sin
mencionarse en el texto. Se añadieron al informe entonces.

De modo que el documento que tiene el profesor **enuncia la proporcionalidad inversa sin las cifras que la
sostienen**. Para la corrección esto es más fácil, no más difícil: lo que hay que rectificar allí es una
afirmación cualitativa y trece valores de tabla, no un aparato estadístico.

**Nota de método.** Esta comprobación estuvo a punto de dar un falso negativo. Un primer extractor de PDF
casero devolvió **cero** apariciones de las cuatro frases, lo que se habría leído como «el PDF no lo dice». El
control de `LEARNING §L57` —buscar además palabras que **tienen** que estar— lo destapó: «Kleptotrace»,
«gemma» y «Ahumada» también daban cero, de modo que el extractor no leía nada. Con `pypdf` el control pasa
(11, 91 y 2 apariciones) y las cuatro frases aparecen.

## Orden recomendado

1. Esperar a que el equipo resuelva `§F85` y rehaga el consolidado.
2. Recalcular con `tools/robustez_estadistica.py` y la correlación, y fijar las cifras definitivas.
3. Reescribir §5.3.1 con lo que digan, y **en el mismo commit** el resumen y el abstract.
4. Revisar §6 a la luz de lo anterior.
5. Pasar `tools/verificar_informe.py` y comprobar el tope de 200 palabras y el de 25 páginas.
