# Inventario de datos incorrectos: candidatos a retirada

**2026-09-08.** Elaborado a petición del autor, que pidió la lista completa **antes** de retirar nada.

Todo lo que sigue está **rastreado en git**. Lo no rastreado no se enumera porque retirarlo no cambia lo que
ve el equipo remoto, que es el objetivo declarado.

La lista separa lo que **afirma** de lo que **atestigua**. Se propone retirar solo lo primero. Los registros
de ejecución, los `run_config.json` y los puntos de control **no se tocan en ningún caso**: son la prueba de
qué se ejecutó, y sin ellos ninguna declaración del informe es verificable.

---

## Grupo 1 — Duplicados de macOS rastreados (ruido puro)

Ficheros con sufijo « 2», « 3», « 4» que Finder creó al copiar. La regla del `.gitignore` los excluye,
pero estos entraron en git **antes** de que la regla existiera y `.gitignore` no desrastrea.
Varios contienen además modelos excluidos del estudio.

| Fichero | Contiene modelos excluidos |
|:---|:---|
| `GEMMA_QUICK_START 2.md` | — |
| `doc/organized/Instructions/archive/evaluacion-propuesta_tesina-formulario-2025 2.md` | — |
| `doc/organized/Instructions/archive/instrucciones-presentaciones-finales 2.md` | — |
| `doc/organized/Instructions/archive/presentaciones-finales 2.md` | — |
| `doc/organized/Instructions/archive/propuesta_tesina-formulario-2023 2.md` | — |
| `doc/organized/Instructions/archive/propuesta_tesina-formulario-2023_JC 2.md` | — |
| `doc/organized/Instructions/archive/propuesta_tesina-formulario-2025 2.md` | — |
| `doc/organized/Presentations/archive/PRESENTACION_DEFENSA_TESINA_Eduardo_Ahumada 2.md` | — |
| `repos/ner-llm-entity-benchmark/results/ANALISIS_MOJIBAKE_20260908/efecto_mojibake 2.json` | nuextract |
| `repos/ner-llm-entity-benchmark/results/CORRECCION_LOCATIONS_20260908/README 2.md` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/CORRECCION_LOCATIONS_20260908/metricas_sin_locations_n120 2.json` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/benchmark_balanced_120_20260824_173036/benchmark_results 2.csv` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/benchmark_balanced_120_20260824_173036/statistical_report 2.md` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/benchmark_n120_REMOTO/benchmark_results 2.csv` | nuextract |
| `repos/ner-llm-entity-benchmark/results/benchmark_n120_REMOTO/statistical_report 2.md` | nuextract |
| `repos/ner-llm-entity-benchmark/results/benchmark_results 2.csv` | minimax-m3 |
| `repos/ner-llm-entity-benchmark/results/benchmark_results 3.csv` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/benchmark_results 4.csv` | minimax-m3 |
| `repos/ner-llm-entity-benchmark/results/statistical_report 2.md` | minimax-m3 |
| `repos/ner-llm-entity-benchmark/results/statistical_report 3.md` | minimax-m3 |
| `repos/ner-llm-entity-benchmark/results/statistical_report 4.md` | minimax-m3, nuextract, q8-64k |
| `repos/ner-llm-entity-benchmark/results/test_nothink/gemma4_latest/confusion_matrix 2.json` | — |

**Total: 22 ficheros.** Ninguno es fuente del consolidado ni lo cita el informe.

---

## Grupo 2 — Filas inválidas dentro de agregados vigentes

Aquí no sobra el fichero, sobran filas concretas. Retirar una fila de un agregado que sí está en uso es más
delicado, y por eso van separadas.

### 2.a — `results/benchmark_results.csv`: 12 filas de `gemma4:31b-cloud`

Las seis filas de cada modo que el servicio rechazó por cuota el 2026-09-03 (HTTP 429), con latencia 0 y
0 tokens/s. Arrastran el F1 de esa corrida a 0,3973 y 0,4272.

- **Impacto en el informe: ninguno.** La Tabla 4 publica `cloud_n15_limpio_20260905` (66,99 %), y la Tabla 15
  ya declara esa procedencia.
- **Sustituto disponible: sí**, y verificado: la corrida limpia resuelve 15 de 15 por análisis directo.
- **Efecto: 330 filas pasan a 318.** Ninguna cifra publicada cambia.
- **Riesgo: bajo.** Es el caso más claro de la lista.

### 2.b — `results/benchmark_n120_REMOTO/benchmark_results.csv`: 480 filas

Las de `gemma4:12b-mlx` y `qwen3:8b`, invalidadas por el modo de razonamiento activo (68, 98, 19 y 31
artículos sin extracción según el grupo).

- **Impacto en el informe: ninguno.** El consolidado toma esos cuatro grupos de otras corridas.
- **Riesgo: ALTO, y por eso se desaconseja.** Este fichero **sí es fuente del consolidado** (`06_P3` en
  `merge_manifest.json`) y aporta las filas publicadas de otros modelos. Editarlo rompe la reproducibilidad
  del consolidado: quien vuelva a ejecutar la fusión sobre el manifiesto obtendrá un fichero distinto del que
  produjo el ANOVA publicado.
- **Recomendación: no tocarlo.** El informe ya declara que esas corridas se descartaron y por qué, con su
  evidencia. La re-corrida en curso las sustituye por completo.

---

## Grupo 3 — Agregado histórico con un modelo excluido

`results/HISTORICO_20260630/benchmark_results_20260630.csv` — 45 filas, de las que 15 son de un modelo
retirado del estudio y además fallaron enteras.

- **Impacto en el informe: ninguno.** No se cita.
- **Consideración en contra:** es el registro de una corrida de junio, anterior al estudio. Pertenece a la
  clase de artefactos que **atestiguan** lo que se ejecutó, no a la que afirma resultados. La política del
  proyecto conserva los datos crudos de corridas históricas.
- **Recomendación: conservarlo.** Si molesta su visibilidad, basta con que el índice `RUNS_INDEX.md` lo
  marque como histórico y ajeno al estudio.

---

## Grupo 4 — Directorio de preparación

`_to_delete/md_20260903.md` y `_to_delete/md_20260907.md`, rastreados. El nombre del directorio ya declara la
intención. Contienen versiones antiguas del informe con modelos excluidos.

- **Recomendación: retirarlos**, previa comprobación de que su contenido está íntegro en el historial de git
  y en las versiones congeladas de `doc/versions/`.

---

## Lo que NO se propone tocar, en ningún caso

| Artefacto | Razón |
|:---|:---|
| Todos los `benchmark.log` y `run_console.log` | Atestiguan qué se ejecutó. Norma expresa del autor tras el incidente del 2026-09-08 |
| `results/DESCARTADA_ragmode_incorrecto_142604/benchmark.log` | Es la prueba de por qué esa corrida se descartó |
| Los `run_config.json` | Sin ellos no puede verificarse el protocolo de ninguna corrida |
| Los `.checkpoint.json` | Atestiguan el avance real de cada barrido |
| `results/ANALISIS_CONJUNTO_20260907/` | Es el consolidado publicado |
| Los ficheros `.bak*` | No están rastreados; retirarlos no cambia lo que ve el equipo remoto |
| `doc/organized/Hito_4_*` y demás hitos entregados | Reescribir un documento ya entregado falsifica el registro |

---

## Resumen de la propuesta

| Grupo | Qué | Recomendación |
|:---|:---|:---|
| 1 | Duplicados de macOS rastreados | **Retirar** |
| 2.a | 12 filas de cuota en el CSV raíz de N=15 | **Retirar** |
| 2.b | 480 filas en una fuente del consolidado | **Conservar** — rompería la reproducibilidad |
| 3 | Agregado histórico de junio | **Conservar** — atestigua |
| 4 | `_to_delete/` rastreado | **Retirar** tras comprobar respaldo |

Nada de esto se ejecuta sin confirmación del autor.

---

## Registro de ejecución — comprobado el 2026-09-08, 23:2x

El documento cierra diciendo que «nada de esto se ejecuta sin confirmación del autor». **La confirmación
llegó y parte se ejecutó**, en el commit `fa23e4b`, de modo que esa frase ha dejado de describir el estado
real. Se deja intacta —es lo que la propuesta decía cuando se escribió— y se registra aquí lo comprobado.

| Grupo | Recomendación | Estado real, verificado hoy |
|:---|:---|:---|
| 1 — duplicados de macOS | Retirar | **Ejecutado.** Ninguno de los nombres de la tabla está rastreado ni existe en disco. Cero ficheros con sufijo « 2», « 3» o « 4» en `git ls-files` |
| 2.a — 12 filas de cuota en el CSV raíz | Retirar | **Ejecutado, y con el efecto previsto exactamente.** El fichero tiene **318 filas**, las que anunciaba el apartado al pasar de 330. Quedan 18 filas de `gemma4:31b-cloud`, nueve por modo, que son las válidas |
| 2.b — 480 filas del `n120_REMOTO` | **No tocar** | **Respetado, y la reproducibilidad está intacta.** El manifiesto declara `06_P3` con **1 440 filas** y el fichero tiene 1 440. La copia de `remote_48g/` conserva 1 680 y no es la fuente del consolidado |
| 3 — agregado histórico de junio | Conservar | **Conservado.** 45 filas, rastreado, en su sitio |
| 4 — `_to_delete/` rastreado | Retirar tras comprobar respaldo | **Sin ejecutar.** Siguen rastreados **ocho** ficheros bajo `_to_delete/_tmp_pdfcheck/`, todos capturas de páginas del PDF |

### Lo único que queda de esta lista

El Grupo 4, y es el de menor peso: ocho imágenes de comprobación de páginas del PDF, sin valor probatorio
—no atestiguan una ejecución, son capturas de una revisión visual— y sin impacto en ninguna cifra. Su
retirada sigue **condicionada a comprobar que existe respaldo**, como decía la recomendación original. No
hay prisa ni riesgo en dejarlo como está.

### Por qué se añade esto

Un inventario que propone retiradas y no registra cuáles se hicieron obliga a rehacer la comprobación entera
cada vez que alguien lo abre, y en el peor caso invita a ejecutar dos veces algo ya ejecutado. Es el mismo
defecto que el desfase de `PROPAGACION-PENDIENTE-DOCX-20260908.md` y el de `TODO-INFORME-FINAL.md`: un
documento de estado que no se actualiza sigue leyéndose como si fuera actual, porque nada en él avisa de lo
contrario.


---

## Grupo 5 — Los diecisiete ceros de `nemotron-mini` en el consolidado nuevo (2026-09-09)

Añadido al cerrarse la re-corrida. El consolidado `ANALISIS_CONJUNTO_20260909` incluye **17 filas de
`nemotron-mini:4b_baseline` que puntúan 0,00 por un `TypeError` del arnés** (`llm_runner.py:167`), no por el
modelo. Detalle en `FINDINGS §F85`.

- **Impacto: alto, y es el único de esta lista que lo tiene.** Hunden la línea base de 30,97 a 26,31 e inflan
  el Δ de ese modelo de +9,58 a +14,23 pp. Como `nemotron-mini` es el punto de mayor influencia del análisis
  —retirarlo anula la correlación central, `§F86`—, el defecto no se queda en su fila.
- **Sustituto disponible: no todavía.** Exige arreglar el fallo y re-ejecutar ese brazo, ciento veinte
  artículos. Pedido en `remote_48g/ALERTA-NEMOTRON-BASELINE-20260909.md`.
- **Recomendación: no retirar las filas, re-ejecutarlas.** Descontarlas deja el diseño en 96 registros
  completos en lugar de 113 y debilita todos los contrastes; sirve como diagnóstico del sesgo, no como
  medición. Y los registros crudos y el `benchmark.log` **se conservan en todo caso**: son la prueba de qué
  ocurrió.

**No forma parte de la propuesta original de este documento**, que era del 2026-09-08 y ya se ejecutó. Se
añade aquí porque es el sitio donde alguien buscará «qué datos incorrectos hay», y dejarlo fuera obligaría a
descubrirlo dos veces.
