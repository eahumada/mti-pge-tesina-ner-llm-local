# Respuesta a `DECISIONES-PENDIENTES-AUTOR.md`

**Fecha:** 2026-09-08. **De:** equipo principal, verificado sobre el Markdown canónico.

**Los siete puntos están resueltos.** Vuestro documento es del 6 de septiembre y se ha quedado atrás: las
tres sustituciones del bloque A se aplicaron con **vuestras** mediciones limpias, y los cuatro del bloque B
se cerraron entre el 6 y el 8. No hace falta que esperéis nada de este documento para lanzar la re-corrida.

## Bloque A — las tres sustituciones, aplicadas con vuestros valores

| # | Qué | Vuestra medición | Estado en el informe |
|:--|:---|:---|:---|
| A1 | `gemma4:31b` en la Tabla 4 (N=15) | 0,6912 | **69.12 %**, aplicado |
| A2 | Variantes de prompt | fs-es 0,7444 · zs-es 0,6843 · zs-en 0,6405 · fs-en 0,6332 | **74.44 / 68.43 / 64.05 / 63.32**, aplicado |
| A3 | `gemma4:31b-cloud` en N=120 | 0,6238 / 0,6185 | **62.38 % / 61.85 %** en la Tabla 7, aplicado |

Los cuatro valores de A2 coinciden al dígito con lo que medisteis, y el 67,83 % sin respaldo desapareció.

## Bloque B — los cuatro que pedían criterio, cerrados

**B1, F1 aritméticamente imposibles.** Las dos filas problemáticas —`llama3.2_rag` con 0,8783 sobre una cota
de 0,7646, y `llama3.1:8b_baseline` con 0,7667 sobre 0,7333— **ya no existen en el informe**. Se comprueba
además de forma sistemática: ninguna fila del documento tiene F1 por encima de la media de precisión y
exhaustividad, y esa verificación está ahora en el guion mecánico de `doc/prompts/00-revision-completa.md`.

**B2, la cita inventada de KPMG.** El marcador `[referencia KPMG 2024]` desapareció. Y el problema resultó
ser más amplio de lo que ese marcador sugería: una verificación contra internet encontró que **cuatro
referencias completas no correspondían a ninguna obra existente**, y se sustituyeron por obras reales
comprobadas una a una abriendo su ficha oficial. La bibliografía pasó de 20 a 38 entradas, todas con URL
verificada. El detalle está en `FINDINGS.md §F51` y `§F52`.

**B3, la contradicción de hardware.** Resuelta declarando **dos escalones**: 16 GB para los modelos que se
mantuvieron por debajo de unos 12 GB de footprint, y el equipo de 48 GB para los de 31B y las variantes MLX
mayores. El informe dice ahora expresamente que las compilaciones de 31B «no pueden cargarse en 16 GB ni
siquiera de forma serial», y reparte por footprint medido y no por número de parámetros.

**B4, la tabla de eficiencia no reproducible.** Los valores que no salían de ningún CSV (24.751 MB y 27,56
tok/s) desaparecieron. La Tabla 8 se reconstruyó desde `benchmark_results.csv` y la nota al pie declara la
procedencia de cada fila, incluidas las que vienen de corridas distintas.

## Lo que sí necesitáis leer antes de lanzar

`PROMPT-EQUIPO-REMOTO-RECORRIDA-COMPLETA-20260908.md`, y en particular su **sección 2.bis**, que se añadió
después del resto del encargo y recoge cuatro defectos descubiertos en la tercera revisión global. Los cuatro
invalidarían la re-corrida si no se reparan antes: la contaminación del conjunto de prueba en los ejemplares
de la base de conocimientos, la pérdida de las localizaciones de CoNLL-2002 en la conversión, el presupuesto
de generación desigual de `gpt-oss:20b`, y la repuntuación de la extracción vacía que no llegó a los
`detailed_results.json`.

**El disparador `TURK_182_GOGO` ya está en el encargo**, de modo que la orden de ejecución está dada.

## Una decisión del autor que sí os afecta, ya tomada

**La convención de agregación pasa a ser macro en todo el informe**: la media del F1 por artículo, que es lo
que `§4.4` declaraba y lo que ya usan las Tablas 4, 6 y 7. El resumen publicaba una cifra micro y quedaba
descolgado de su propia tabla. Para la re-corrida: **agregad macro**, y si publicáis también micro, declaradlo
como columna aparte y no como equivalente.
