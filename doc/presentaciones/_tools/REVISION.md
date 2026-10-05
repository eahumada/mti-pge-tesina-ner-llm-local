# Plan de revisión iterativa — Tesina_MTI_IA_Aplicada.pptx
Cadencia: cada 10 minutos, 10 pasadas. Idioma de trabajo: español.
Fuente de verdad: doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md
Entrega: ~/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local/doc/presentaciones/

| # | Pasada | Estado |
|---|--------|--------|
| 1 | Estructura, solapamientos de cajas y rótulos de los gráficos nativos | HECHA |
| 2 | Revisión lámina a lámina 1–10: ortografía, acentos, coherencia de términos | HECHA |
| 3 | Revisión lámina a lámina 11–20 | HECHA |
| 4 | Revisión lámina a lámina 21–30 | HECHA |
| 5 | Contraste de cifras contra el informe, tabla por tabla | HECHA |
| 6 | Calidad de las cuatro imágenes reutilizadas: recorte, nitidez y texto | HECHA |
| 7 | Coherencia con el resumen y el abstract finales de la tesina | HECHA |
| 8 | Notas del orador y ajuste al formato de 10 a 15 minutos | HECHA |
| 9 | Contraste de color, tamaños mínimos y nombres de objetos | HECHA |
| 10 | Revalidación, exportación final, entrega y registro en CURRENT-TASKS.md | HECHA |

## Hallazgos corregidos
- Pasada 1: vinetas de la lámina 25 invadían la columna derecha (marco ancho); se creó `bullets2`.
- Pasada 1: la lámina 6 repetía en tarjetas las dos cifras que ya traía el gráfico; se sustituyeron.
- Pasada 1: «5 familias» en la lámina 11 se confundía con las cuatro familias de técnicas del título.
- Pasada 1: rótulos `llama3.2:3b` y `mistral-nemo:12b` en los gráficos; se usaron las etiquetas reales.
- Pasada 1: el rótulo de la barra negativa pisaba el nombre de categoría; se amplió el mínimo del eje.
- Pasada 1: el título y el pie de la caja A3 afirmaban que el RAG evita las alucinaciones; se recortaron y se reemplazaron por texto nativo.
- Pasada 2: la lámina 2 prometía «veinte láminas de recorrido y diez de respaldo», reparto que no se sostiene al contarlas.
- Pasada 2: la cuarta viñeta de la lámina 6 repetía casi textualmente el pie del gráfico; se diferenciaron.
- Pasada 2: la tarjeta «Cientos/día» usaba una barra en lugar de texto; se reescribió.
- Pasada 2: «3 vías» en la lámina 7 chocaba con la viñeta que presenta una cuarta vía; ahora dice «3 vías clásicas».
- Pasada 2: ortografía, acentuación y tildes diacríticas revisadas en las láminas 1 a 10, sin otros hallazgos.
- Pasada 3: la raya de cierre de la lámina 14 quedaba huérfana al inicio de línea; se reescribió sin aposición.
- Pasada 3: «footprint» en la lámina 17 se sustituyó por «tamaño en memoria».
- Pasada 3: la observación de la fila Gemma en la lámina 19 no valía para gemma:latest (7B), que queda en 59,55 %.
- Pasada 3: «veintiséis grupos —cada uno con y sin recuperación—» hacía concordar «cada uno» con «grupos» en vez de con «modelos».
- Pasada 3: verificado que los rótulos corregidos en la pasada 1 (llama3.2:latest, mistral-nemo) y la separación del rótulo negativo se renderizan bien.
- Pasada 4: los rótulos de los tres gráficos salían con punto decimal («63.25%») junto al texto con coma; se apagó el rótulo automático y la cifra pasó a la etiqueta de categoría, que sí es texto bajo control.
- Pasada 4: las barras horizontales se dibujan de abajo hacia arriba, así que el mejor modelo quedaba al pie; se invirtieron los dos arreglos para que encabece.
- Pasada 4: la lámina 22 unía el 63,25 % (N=120) con el índice 26,44 (corrida de hardware) como si fueran la misma medición.
- Pasada 4: la tarjeta «0 %» de la lámina 25 atribuía el cero al modelo recomendado; el cero exacto es de las variantes alojadas y el recomendado va de 0,00 % a 0,16 %.
- Pasada 4: la fase 2 de la hoja de ruta no decía sobre qué corpus se miden los 4,43 puntos que faltan para la meta interna.
- Pasada 5: se verificaron contra el informe las 37 cifras del mazo (Tablas 4, 5, 6, 7 y 8, §5.4, §5.6, §6.1 y conclusiones). Todas aparecen en la fuente con el mismo valor.
- Pasada 5: «13 configuraciones en el estudio principal» confundía los dos conjuntos: las trece configuraciones son del benchmark exploratorio y el estudio principal tiene trece modelos en veintiséis grupos.
- Pasada 5: «0 bytes enviados a terceros» en la lámina 2 podía leerse como una propiedad del estudio, que sí usó una variante en la nube para comparar; ahora habla de la operación local.
- Pasada 6: las imágenes se insertaban forzadas a 6,00 x 4,46 sin respetar su proporción. A2 (919x633) salía estirada un 8 % en vertical. Se añadió `pngSize`/`encajar`, que lee la cabecera del PNG y centra la imagen en el marco sin deformarla.
- Pasada 6: las cuatro cajas flotaban sobre el blanco mientras los ocho gráficos nativos van enmarcados; se les dio el mismo marco para que el mazo se lea como un solo sistema.
- Pasada 6: resolución efectiva verificada, entre 144 y 153 ppp sobre el marco de 6 pulgadas; el texto de las cuatro cajas se lee sin esfuerzo en el render a 100 ppp.
- Pasada 7: las nueve afirmaciones centrales del resumen y del abstract están todas en el mazo y ninguna lo contradice. El mazo es más preciso que el resumen en un punto, el 90,16 %, porque añade que la cifra está restringida a las categorías que el corpus anota, como hacen §6.1 y el Anexo I.
- Pasada 7: el mazo no decía que el corpus N=30 se validó solo con los dos modelos de mayor capacidad, dato que el resumen sí destaca; se añadió al panel de corpus.
- Pasada 7: la lámina de cierre omitía el 90,16 % del corpus del dominio, una de las dos cifras que el resumen pone en su última frase; ahora cita ambas.
- Pasada 8: las treinta láminas ya tenían nota, pero ninguna decía cuánto dura ni cuál se puede saltar. Cada nota lleva ahora su franja horaria o la marca RESPALDO con la pregunta que la justifica.
- Pasada 8: la nota de la lámina 1 recoge el plan completo: veintidós láminas de recorrido en unos catorce minutos, las ocho de respaldo, el orden de recorte si la sesión baja a diez minutos y qué añadir si sobra tiempo.
- Pasada 9: se midieron las 23 combinaciones de color del mazo con la fórmula de luminancia relativa. Siete quedaban por debajo del 4,5 a 1 que pide el nivel AA para texto pequeño.
- Pasada 9: el verde azulado pasó de 0E7C7B a 0C6E6D y el azul grisáceo de 5B7B9A a 51708D; sobre fondo claro suben de 4,49 y 3,97 a 5,43 y 4,65.
- Pasada 9: oscurecer el azul grisáceo empeoraba su contraste sobre los fondos oscuros, así que el texto secundario sobre azul marino pasó a 8FA9C4 (6,87 a 1).
- Pasada 9: los rótulos pequeños sobre los paneles azul marino usan ahora un verde más claro, 35B3A3, que sube de 4,16 a 5,35.
- Pasada 9: el rótulo del recuadro ámbar pasó de 9A6B16 a 8A5F13 (5,13 a 1).
- Pasada 9: las etiquetas blancas sobre relleno verde claro daban 3,32; `fila` elige ahora el color del texto según la luminancia del fondo.
- Pasada 9: el pie de los gráficos subió de 9,5 a 10,5 puntos, con lo que el cuerpo más pequeño del mazo queda en 10 puntos. Las 23 combinaciones cumplen AA.
- Pasada 9: 519 de las 522 formas llevan nombre descriptivo; las tres restantes son marcadores de posición de los diseños.
- Pasada 10: revisión final de las treinta láminas renderizadas, sin hallazgos nuevos. Validación del .pptx correcta y exportación a PDF comprobada.
- Pasada 10: el generador se publicó en `doc/presentaciones/_tools/` con su README, de modo que la presentación se reconstruye con `./render.sh`.
- Pasada 10: cierre registrado en CURRENT-TASKS.md como §3.CWK.02, con control de concurrencia antes y después de escribir. Bucle terminado.
