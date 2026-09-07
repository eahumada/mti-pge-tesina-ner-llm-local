# Auditoría de Consistencia Documental — 2026-09-03

Generada por auditoría automatizada con **verificación adversarial**: cada hallazgo fue
re-comprobado por un segundo agente contra el archivo real, abriendo el fichero y validando
la cita textual. Se descartaron los que no resistieron esa comprobación.

- **Confirmados:** 115
- **Descartados por el verificador:** 17
- Gravedad alta: 26 · media: 55 · baja: 34

## Distribución por archivo

| Archivo | Hallazgos |
|:---|---:|
| `2026-07-04_Borrador-Informe-Final-Tesina.md` | 54 |
| `BENCHMARKS.md` | 13 |
| `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | 11 |
| `Informe_Final_Tesina_NER.docx` | 7 |
| `WORKLOG.md` | 7 |
| `AGENTS.md` | 6 |
| `RUNS_INDEX.md` | 5 |
| `HISTORIAL-CONSOLIDADO.md` | 4 |
| `README.md` | 3 |
| `TODO.md` | 3 |
| `config.py.bak_pre20260903, benchmark_final_run_v2.log)` | 1 |
| `benchmark_results.csv` | 1 |


## 🔴 Gravedad ALTA (26)

### A1. Conteo de modelos contradictorio: 15 en §1.4-Obj.2 y §4.2 vs 16 en §2.5, título de §5.1 y §5.3.5

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L90, L139, L267, L369, L435
- **Verificación:** Las cinco citas existen LITERALMENTE en las líneas indicadas (verificado con sed). L90 y L267 dicen 15; L139, L369 y L435 dicen 16. La Tabla 2 (L375-388) tiene 13 filas = 12 modelos distintos y §4.2 enumera 12 nombres, por lo que ninguna de las dos cifras es correcta. Nota: el archivo NO está bajo repos/ sino en la raíz del proyecto.
- **Corrección sugerida:** Fijar el conteo real (12 modelos distintos en Tabla 2; 12 nombres en §4.2, aunque no son el mismo conjunto: §4.2 incluye gemma4:12b y omite gemma4:31b-mlx) y propagarlo a §1.4, §2.5, §4.2, §5.1 y §5.3.5.

### A2. §4.2 anuncia 15 modelos pero enumera 12 (6+4+2)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L267-270
- **Verificación:** Verificado: L267 dice «Se evaluaron 15 modelos LLM generativos distribuidos en tres categorías:» y las tres viñetas (L268-270) suman exactamente 6+4+2 = 12 nombres. La cita es literal.
- **Corrección sugerida:** Corregir el encabezado a 12 y añadir los modelos efectivamente reportados que faltan (gemma4:31b-mlx).

### A3. Título de §5.1 anuncia 16 modelos; la Tabla 2 tiene 13 filas = 12 modelos distintos (gemma4:latest duplicado ZS-ES/FS-ES)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L369-388
- **Verificación:** Conteo directo de las filas L375-388: 13 filas de datos, con gemma4:latest repetido en dos configuraciones → 12 modelos distintos. El título L369 dice 16. Cita literal confirmada. (Detalle adicional no reportado: hay una línea en blanco espuria en L386 que parte la tabla markdown en dos, dejando nemotron-mini y deepseek-r1 fuera del renderizado de la tabla.)
- **Corrección sugerida:** Ajustar el título a 12 modelos, aclarar que dos filas son configuraciones del mismo modelo y eliminar la línea en blanco de L386 que rompe la tabla.

### A4. Índice Tok/s/B no cuadra entre Tabla 2 (§5.1) y la tabla de eficiencia (§5.5)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L375-376, L381 vs L472-474
- **Verificación:** Citas literales confirmadas. Además la aritmética favorece a §5.5: 11.37/31=0.37, 27.56/31=0.89, 47.5/3=15.83, todas correctas; los valores 0.81 y 18.73 de la Tabla 2 no se derivan de ningún par (Tok/s, B) declarado en el informe.
- **Corrección sugerida:** Recalcular Tok/s/B = Tok/s ÷ parámetros(B) con los throughput medidos y usar el mismo valor en Tabla 2, §5.5 y §6.3.

### A5. §6.1 confirma la hipótesis solo con N=30 (79.03%) ignorando que en N=120 el mejor F1 es 59.25%, bajo el umbral de 70%

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L669 vs L439 y L456
- **Verificación:** Citas literales verificadas. Además el dato N=120 está confirmado en benchmark_summary.json (gemma4:31b-mlx_baseline f1=0.592549). §6.1 no menciona el corpus N=120 en ningún punto (grep de «N=120» no arroja coincidencias en §6.1), pese a que §5.3.5 lo presenta como la validación de mayor potencia estadística. Es el hallazgo con mayor riesgo en defensa oral.
- **Corrección sugerida:** Reescribir §6.1 para discutir ambos corpus: hipótesis confirmada sobre el corpus AML específico N=30 y no alcanzada sobre el corpus real heterogéneo N=120, explicando la diferencia de dominio y longitud.

### A6. §4.1.2 llama al corpus sintético «datos reales balanceados generados por LLM», expresión autocontradictoria

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L249 y L255
- **Verificación:** Citas literales verificadas: L249 «El uso de datos reales balanceados generados por LLM para pruebas de hipótesis es válido» y L255 «La validez de los datos reales balanceados como proxy del dominio real». El título de la propia subsección (L247) dice «Validez Estadística del Corpus Sintético», confirmando que es residuo de un reemplazo global mal aplicado.
- **Corrección sugerida:** Restituir «datos sintéticos» / «corpus sintético» en ambas frases.

### A7. Nombre del dataset corrupto en el abstract («balanceado Kleptotrace/CoNLL-2002/CoNLL-2002») y URL inválida en la referencia [18]

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L39 y L767
- **Verificación:** Citas literales verificadas carácter por carácter, incluida la palabra española «balanceado» dentro del abstract en inglés y la URL «https://Kleptotrace/CoNLL-2002.org», que no es una URL válida. Es el defecto más visible para un evaluador externo.
- **Corrección sugerida:** Normalizar el nombre del dataset en todo el documento (el nombre compuesto «Kleptotrace/CoNLL-2002» aparece en ~20 lugares y conviene revisarlo por completo) y restaurar una URL válida en [18].

### A8. Falta por completo la seccion 4.1.3 'Extension a Corpus Real N=120 (Dataset Conmutable)'; el documento pasa de §4.1.2 apartado d) directamente a §4.2.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** Entre §4.1.2 apartado d) y §4.2 (texto extraido de word/document.xml, lineas 133-134 de mi extraccion)
- **Verificación:** CONFIRMADO. Extraje el texto de los tres .docx. El indice de encabezados de Informe_Final_Tesina_NER.docx salta de '4.1.2 Validez Estadistica del Corpus Sintetico' a '4.2 Modelos Evaluados'. La cadena '4.1.3' no aparece ni una sola vez en el documento, mientras que si aparece en 2026-07-04_Borrador-Informe-Final-Tesina.docx (linea 141), en Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx (linea 105) y en el .md vigente (§4.1.3). La evidencia citada (apartado d) seguido de '4.2 Modelos Evaluados') existe literalmente.
- **Corrección sugerida:** Reinsertar §4.1.3 integra antes de §4.2, tomandola del .md vigente o del docx borrador (que la conserva identica), o regenerar el .docx desde el .md.

### A9. Falta por completo la seccion 5.3.5 'Validacion Estadistica Complementaria sobre Corpus Real N=120'; se pierden la tabla 5 modelos x 2 modos y las cifras ANOVA F=10.2096 / p=2.873e-15.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** Entre §5.3.4 (Analisis de Sensibilidad) y §5.4 (Taxonomia de Errores NER)
- **Verificación:** CONFIRMADO. Los encabezados del documento pasan de '5.3.4 Analisis de Sensibilidad (Outliers)' a '5.4 Taxonomia de Errores NER'. Un grep de '10.2096', '2.873' y '5.3.5' sobre el texto completo del docx no devuelve NINGUNA coincidencia; en cambio ambos valores aparecen en el docx borrador (linea 260) y en la plantilla (linea 188), y en el .md vigente. La evidencia citada ('F1 estable (no filtrado): gemma4:31b = 0.7903 | gemma4:31b-mlx = 0.7747' seguido de '5.4 Taxonomia de Errores NER') existe literalmente. Ademas las cifras coinciden con los datos verificados de la corrida 2026-09-01 (results/benchmark_balanced_120_20260901_140421/).
- **Corrección sugerida:** Reinsertar §5.3.5 completa (tabla N=120 + ANOVA F=10.2096 / p=2.873e-15 + Tukey HSD + lectura conjunta con N=30) desde el .md vigente.

### A10. Referencias huerfanas a N=120: el docx invoca el corpus N=120 siete veces (incluida la conclusion sobre KB RAG y el trabajo futuro) sin que ninguna seccion lo defina ni reporte su validacion estadistica.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** §5.6.1, §5.6.5 (tabla del benchmark KB RAG), §6.5, §7.1 conclusion 6, §7.2 (dos veces) y Anexo A
- **Verificación:** CONFIRMADO. Grep de 'N=120' sobre el texto extraido devuelve exactamente 7 ocurrencias (lineas 252, 327, 368, 380, 382, 384, 438 de mi extraccion), correspondientes a §5.6.1, §5.6.5, §6.5, §7.1, §7.2 x2 y el arbol de repositorio del Anexo A. La frase citada como evidencia ('Durante el benchmark principal sobre N=120 articulos reales, se observo un fenomeno inesperado...') existe literalmente. En §4.1 el docx solo describe los corpus N=15 y N=30, de modo que N=120 nunca queda definido. Consecuencia directa y verificada de los dos hallazgos anteriores.
- **Corrección sugerida:** Restaurar §4.1.3 y §5.3.5; luego verificar que toda mencion a N=120 tenga antecedente definido en el mismo documento.

### A11. Los TRES docx conservan 'estudio de ablacion' como termino PRINCIPAL en cinco ubicaciones donde el .md vigente ya lo reemplazo por 'Comparacion de Configuraciones de Prompt'.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §1.4 objetivo especifico 3; §2.5 (aporte original, punto 2); titulo §4.3; §4.3.4; titulo §5.2 (en la plantilla tambien el pie 'Tabla 6')
- **Verificación:** CONFIRMADO en los tres archivos, ubicacion por ubicacion. Los tres docx dicen literalmente '4.3 Configuraciones de Prompt (Estudio de Ablacion)' y '5.2 Estudio de Ablacion del Prompt (gemma4:latest, N=15)'; el objetivo 3 dice 'Ejecutar un estudio de ablacion sistematico'; §2.5 dice '(2) estudio de ablacion linguistica (ES vs. EN)'; §4.3.4 dice 'Los resultados del estudio de ablacion muestran'. El .md vigente dice en cambio '### 4.3 Comparacion de Configuraciones de Prompt' (linea 272), '### 5.2 Comparacion de Configuraciones de Prompt (gemma4:latest, N=15)' (linea 394), '(2) comparacion de configuraciones de prompt entre idiomas (ES vs. EN)' (linea 139) y una formulacion del objetivo 3 con el termino como sinonimo glosado (linea 91). La plantilla ademas rotula 'Tabla 6. Estudio de Ablacion del Prompt'. El borrador esta en Hito_5 (hito vigente, ya modificado en esta sesion segun git status), no en Hito_4 ni archive/, por lo que la politica de no-modificacion no aplica.
- **Corrección sugerida:** Sincronizar los tres docx con el .md: 'Comparacion de Configuraciones de Prompt' como termino principal en las cinco ubicaciones (mas el pie de Tabla 6 en la plantilla), dejando 'diseno factorial 2x2' y 'estudio de ablacion' como sinonimos tecnicos glosados. No tocar el abstract en ingles.

### A12. BENCHMARKS.md linea 101 documenta `python src/main.py --run-config results/run_config.json`, flag inexistente en el argparse.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 101
- **Verificación:** CONFIRMADO. BENCHMARKS.md:101 contiene literalmente `python src/main.py --run-config results/run_config.json`. El argparse de src/main.py (lineas 702-729) define exactamente: --models, --batch-size, --data-file, --resume, --results-dir, --generate-sample-data, --temperature, --max-tokens, --seed, --system-prompt-file, --compare-annotators, --ablation, --rag-study, --rag-mode, --num-workers. No existe --run-config, por lo que el comando aborta con 'unrecognized arguments'.
- **Corrección sugerida:** Reemplazar por un comando valido, p.ej. `python src/main.py --data-file data/benchmark_balanced_120.json --models gemma4:latest --batch-size 3`.

### A13. BENCHMARKS.md linea 33 instruye editar results/run_config.json como archivo de entrada, pero es una salida generada por la corrida.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 33 (Configure the Benchmark)
- **Verificación:** CONFIRMADO. La cita existe literal en BENCHMARKS.md:33. src/main.py:190 escribe `os.path.join(config.results_dir, 'run_config.json')` con `json.dump(config.to_dict(), ...)`; ningun modulo lo lee como entrada (grep de 'run_config' en src/ solo devuelve esa escritura). Contradice AGENTS.md 8.1, que declara src/config.py como unico lugar para cambiar modelos.
- **Corrección sugerida:** Documentar que la lista de modelos se define en src/config.py (campo BenchmarkConfig.models, linea 59) o via --models, y aclarar que results/<run_dir>/run_config.json es un artefacto de reproducibilidad generado por la corrida.

### A14. BENCHMARKS.md instruye `rm -rf results/*.json` antes de cada corrida, contra la politica de retencion aditiva.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 132-141 (Cleaning Up)
- **Verificación:** CONFIRMADO y agravado. Las lineas 137-138 contienen literal `rm -f results/.checkpoint.json` y `rm -rf results/*.json`. Verificado con `git ls-files results/`: el unico archivo de results/ versionado en git es `results/kb_rag_analysis_20260901.json`, evidencia derivada de la corrida N=120 del 2026-09-01; ese comando lo borraria. Contradice RUNS_INDEX.md 4.3 regla 4 ('los directorios historicos no se borran') y ya es innecesario: src/config.py __post_init__ (lineas 98-107) crea un subdirectorio con timestamp por corrida y assert_not_results_root (lineas 31-54) aborta si se apunta a la raiz.
- **Corrección sugerida:** Eliminar la seccion 'Cleaning Up' o reemplazarla por: 'no se borra nada; cada corrida genera su propio directorio results/<dataset>_<timestamp>/'.

### A15. El encabezado 'Latest Benchmark Results (July 24, 2026)' no corresponde a la ultima corrida ni a ninguna corrida catalogada.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 146
- **Verificación:** CONFIRMADO. BENCHMARKS.md:146 dice literal '## Latest Benchmark Results (July 24, 2026)' y la linea 148 la presenta como 'the final benchmark performance results from the latest full sweep'. La corrida vigente es la del 2026-09-01 (results/benchmark_balanced_120_20260901_140421/), verificada en este mismo directorio: benchmark_summary.json tiene 10 condiciones (5 modelos x baseline/kb_rag) y statistical_report.md linea 4 registra F-Statistic 10.2096. BENCHMARKS.md no la menciona. Ademas RUNS_INDEX.md no cataloga ninguna corrida del 24 de julio: las de esa ventana son #8 y #9, ambas del 2026-07-27.
- **Corrección sugerida:** Agregar de forma aditiva la seccion de resultados de balanced120_N120__rag-kb-combined__zs-en__20260901_140421 y reetiquetar la tabla de julio como historica, citando el run_id de RUNS_INDEX que le corresponde.

### A16. La tabla 'Prompt Ablation Study (gemma4:latest)' no coincide con ninguna corrida de ablacion catalogada y no declara corpus ni N.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 171-178
- **Verificación:** CONFIRMADO leyendo los datos crudos. La tabla dice fs-es 0.7169 / zs-es 0.6640 / zs-en 0.6482 / fs-en 0.5874. results/kleptotrace_20260727_110454/benchmark_summary.json (corrida #9, N=15) da fs-es 0.6987, zs-es 0.6793, zs-en 0.6676, fs-en 0.5817; results/benchmark_balanced_120_20260825_071207/benchmark_summary.json (#12, N=120) da zs-es 0.5562, fs-en 0.5450, zs-en 0.5446, fs-es 0.5402. Un grep de '0.7169', '0.5874' y '0.6482' en todo el repo (logs, json, csv, md) solo devuelve las propias lineas de BENCHMARKS.md: las cifras no son trazables a ningun artefacto.
- **Corrección sugerida:** Etiquetar la tabla con run_id, corpus y N de origen, o reemplazarla por las cifras verificadas de #9 (N=15) y #12 (N=120) como dos tablas separadas.

### A17. La tabla 8.6 de AGENTS.md esta desactualizada: omite gemma4:31b-mlx, gemma4:12b-mlx y gliner:medium, y lista un gemini-1.5-flash-lite inexistente.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Lineas 169-189 (seccion 8.6)
- **Verificación:** CONFIRMADO en los tres puntos. (a) La tabla (lineas 173-189) no incluye gemma4:31b-mlx pese a ser uno de los 5 modelos de la corrida N=120 del 2026-09-01 (verificado en su benchmark_summary.json) y el segundo modelo del resultado titular N=30; tampoco incluye gemma4:12b-mlx, presente en src/config.py:68 y en run_benchmark.sh:25. (b) AGENTS.md:175 lista `gemini-1.5-flash-lite`; src/config.py:60 declara `gemini-3.1-flash-lite` y `gemini-3.5-flash`, y RUNS_INDEX.md linea 52 (#4) usa gemini-3.1-flash-lite. `gemini-1.5-flash-lite` no aparece en ningun log ni corrida. (c) `gliner:medium` figura en RUNS_INDEX.md linea 51 (#3, F1 0.4767) y tiene provider propio (src/providers/gliner_provider.py) pero no esta en la tabla. El encabezado ademas se autodata 'as of 2026-06-30'.
- **Corrección sugerida:** Regenerar la tabla desde BenchmarkConfig.models con fecha 2026-09-03, anadiendo gemma4:31b-mlx, gemma4:12b-mlx y gliner:medium, y corrigiendo el nombre a gemini-3.1-flash-lite / gemini-3.5-flash.

### A18. RUNS_INDEX seccion 7 limitacion 1 afirma que --ablation no se persiste; ya forma parte de BenchmarkConfig.

- **Archivo:** `RUNS_INDEX.md`
- **Ubicación:** Lineas 179-182
- **Verificación:** CONFIRMADO. La cita existe literal en las lineas 179-182. src/config.py:92-96 declara `ablation: bool = False` con el comentario 'Persisted so that a run's run_config.json records whether it was an ablation sweep'; src/main.py:754 lo pasa al constructor (`ablation=args.ablation`) y run_benchmark() lo reconcilia en las lineas 216-221 (`ablation = bool(ablation) or bool(getattr(config, 'ablation', False)); config.ablation = ablation`) antes de escribir run_config.json (linea 190). La limitacion solo aplica retroactivamente a #9 y #12. Nota: la seccion se autodata 'estado al 2026-09-03', el mismo dia del cambio de codigo, y la politica del archivo es estrictamente aditiva.
- **Corrección sugerida:** Anadir una nota nueva en la seccion 6 (aditiva, sin tocar la seccion 7) indicando que la limitacion 1 quedo resuelta el 2026-09-03 en src/config.py:92-96 y src/main.py:216-221, y que solo afecta retroactivamente a #9 y #12.

### A19. La nota de cierre de RUNS_INDEX afirma que no se aplico ningun cambio a src/main.py ni src/config.py, lo cual es falso.

- **Archivo:** `RUNS_INDEX.md`
- **Ubicación:** Lineas 200-202
- **Verificación:** CONFIRMADO. Las lineas 200-202 dicen literal '(documento de diseño; **no** se aplicó ningún cambio a `src/main.py` ni a `src/config.py`)'. En el codigo actual src/config.py incorpora el campo `ablation` (92-96) y el guardrail completo `_is_results_root` / `assert_not_results_root` (13-54), invocado desde __post_init__ (linea 111) y desde ensure_directories (linea 143); src/main.py reconcilia y persiste el flag ablation (216-221). `git status` confirma ademas que src/config.py y src/main.py estan modificados respecto del ultimo commit.
- **Corrección sugerida:** Reemplazar (o anadir en seccion 6, respetando la politica aditiva) una nota que distinga lo ya aplicado (guardrail de raiz + persistencia de `ablation`) de lo que sigue pendiente (nomenclatura de directorios, sha256 del corpus, models_skipped, runs_index.json).

### A20. `gemma4:31b` y `gemma4:31b-mlx` se listan como dos modelos distintos con valores IDENTICOS en las 6 metricas (67.83/57.29/86.78/0.15/114.20/0.81), pese a ser runtimes distintos (GGUF vs MLX); en §5.3.1 (N=30) los mismos dos modelos SI difieren (79.03% vs 77.47%).

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** lineas 375-376 (§5.1, Tabla 2)
- **Verificación:** CONFIRMADO. Las lineas 375 y 376 son literalmente identicas en las 6 columnas de metricas. Los datos crudos demuestran que los dos artefactos NO empatan: benchmark_mlx_serial.log (2026-07-01 15:28) reporta gemma4:31b f1=0.682966 p=0.581714 r=0.86438 h=0.00155 lat=359.53 y gemma4:31b-mlx f1=0.685191 p=0.580943 r=0.86735 h=0.00000 lat=451.39; benchmark_console.log reporta gemma4:31b f1=0.687572. Y §5.3.1 (lineas 411-412) los diferencia (79.03% vs 77.47%), contradiciendo la fila duplicada. Matiz sobre la descripcion del hallazgo: es INEXACTO decir que `gemma4:31b` no existe — existe en benchmark_console.log, benchmark_mlx_serial.log y benchmark_augmented_30.log; lo que no existe es una fila suya en los CSV (esas corridas fueron sobrescritas, RUNS_INDEX #5, #6, #7).
- **Corrección sugerida:** Sustituir las dos filas por los valores reales de benchmark_mlx_serial.log (gemma4:31b 68.30/58.17/86.44/0.16/359.5; gemma4:31b-mlx 68.52/58.09/86.74/0.00/451.4) o fusionarlas en una sola fila declarando que se reporta un unico artefacto.

### A21. El F1 de `gemma4:31b-cloud` (66.29%) que sostiene el argumento de soberania de datos ('67.83% vs. 66.29%') no se reproduce desde ninguna fuente.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 377 (§5.1), linea 683 (§6.4), linea 706 (§7.1 conclusion 3)
- **Verificación:** CONFIRMADO tras busqueda exhaustiva. Las citas existen literalmente en las tres ubicaciones. Un grep de '0.662', '0.5543', '0.8412', '66.29' sobre todos los .log, .csv, .json y .md del repositorio no devuelve ninguna ocurrencia fuera de los propios documentos derivados de la tesina (WORKLOG.md linea 19 y Hito_4). Todas las mediciones supervivientes de ese modelo son mucho menores: benchmark_console.log linea 1459 -> f1=0.000000 (las peticiones fallaron con HTTP 429 'session usage limit'); results/statistical_report.md linea 15 -> gemma4:31b-cloud_baseline F1=0.3973 (IC 0.2054-0.5892) y _rag_enhanced 0.4272; benchmark_final_run_v2.log lineas 24267-24268 (N=120) -> 0.139467 / 0.185243. A diferencia de gemini-3.1-flash-lite y de la corrida N=30, aqui NO hay ningun log que respalde la cifra. La conclusion 3 y §6.4 descansan sobre ella.
- **Corrección sugerida:** Reemplazar por el unico valor N=15 con respaldo documental (results/statistical_report.md: F1=39.73%, IC95% 0.21-0.59, corrida 20260727) o retirar la fila y reescribir §6.4 y la conclusion 3, que hoy afirman una 'equivalencia de rendimiento' que los datos supervivientes no sostienen.

### A22. Se afirma que la degradacion por RAG-diccionario fue 'consistente a lo largo de todos los modelos evaluados' en N=120, cuando el RAG mejoro el F1 en 8 de 15 modelos.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 486 (§5.6.1)
- **Verificación:** CONFIRMADO. La cita existe literalmente en la linea 486. Recalculo propio sobre results/benchmark_balanced_120_20260824_173036/benchmark_results.csv (3600 filas, 15 modelos x 2 modos x 120): mejoran 8 modelos y degradan 7. Deltas verificados: nemotron-mini:4b +0.1055 (0.3650->0.4704), nuextract:latest +0.0630 (0.4455->0.5085), gemma4:31b-cloud +0.0458, llama3.2:latest +0.0252, deepseek-r1:1.5b +0.0116, minimax-m3:cloud +0.0046, +0.0002, qwen3:8b +0.0001; degradan gemma4-12b-mlx -0.1017, mistral-nemo -0.0570, gemma:latest -0.0475, llama3.1:8b -0.0337, gemma4:latest -0.0189, qwen2.5:14b -0.0117, gemma4:31b-mlx -0.0115. La tabla que sigue a la afirmacion solo muestra 4 modelos y un unico delta, ocultando el patron real. Ademas la afirmacion contradice al propio §5.6.5, que documenta un efecto modulado por capacidad del modelo.
- **Corrección sugerida:** Sustituir 'consistente a lo largo de todos los modelos evaluados' por 'en los modelos de mayor capacidad (7 de 15 modelos degradaron, entre ellos los cinco de mayor F1 baseline)' e incluir la tabla completa de 15 modelos con los deltas positivos y negativos.

### A23. El '-33% vs baseline' del dict-RAG no se sostiene: 0.2367 proviene de un sondeo N=5 cuyo baseline en la misma tabla es 0.5614 (-57.8%); el -33% solo resulta al dividirlo contra 0.3521, baseline de OTRO mini-benchmark N=5.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 646 (§5.6.6) y linea 712 (§7.1 conclusion 6)
- **Verificación:** CONFIRMADO. Cita literal verificada en linea 646 ('0.2367 (-33% vs baseline)') y en la conclusion 6, linea 712 ('versus la degradacion de -33% producida por el dict-RAG (v1.0) en el mismo modelo'). Fuente de 0.2367: research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md, tabla 7.1 (linea 146), cuyo baseline en la MISMA tabla (linea 145) es 0.5614 -> la caida real de ese experimento es -57.8%. Aritmetica del -33%: 0.2367/0.3521-1 = -32.8%, es decir se divide contra el baseline de un mini-benchmark N=5 distinto (research/rag/WORKLOG.md linea 83, 2026-09-01). Confirmado ademas que en la corrida N=120 comparable (benchmark_balanced_120_20260824_173036) llama3.2:latest_rag_enhanced=0.4196 vs baseline 0.3945, es decir +6.4%. La tabla contrasta un -33% de N=5 contra un +25.3% de N=120 sin advertir la diferencia de escala.
- **Corrección sugerida:** Usar el dato N=120 comparable (dict-RAG llama3.2 0.4196 vs baseline 0.3945) o etiquetar 0.2367 como sondeo N=5 con su propio baseline 0.5614 (-57.8%), y en la conclusion 6 no contraponer una cifra N=5 a una N=120.

### A24. Se afirma que los 15 articulos del Gold Standard tienen ~800 caracteres promedio; la medicion real es 4.832,9 caracteres.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 221 (§4.1, Corpus 1)
- **Verificación:** CONFIRMADO. Cita literal verificada en linea 221: 'Longitud promedio: ~800 caracteres por articulo.' Medicion propia con ./venv/bin/python sobre data/kleptotrace.json (15 articulos, campo 'text'): media 4832.9, mediana 5280, min 725, max 8813, sd 2870.7. Error por factor ~6x. Ademas contradice el argumento de §5.3.5 (linea 439), que atribuye el menor F1 sobre N=120 a que los articulos reales son 'mas largos': la media medida de data/benchmark_balanced_120.json es 2110.3 caracteres, menos de la mitad que Kleptotrace.
- **Corrección sugerida:** Corregir a '~4.833 caracteres promedio (mediana 5.280; rango 725-8.813)' y reformular el argumento de longitud de §5.3.5, que hoy queda invertido.

### A25. La distribucion de entidades del corpus N=30 esta invertida (se reporta 2.1 PER y 1.3 ORG cuando lo real es 1.2 PER y 2.3 ORG) y la longitud promedio es 202 caracteres, no 187.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 245 (§4.1.1, Paso 5)
- **Verificación:** CONFIRMADO. Cita literal verificada en linea 245. Medicion propia sobre data/kleptotrace_augmented_30.json (30 articulos): longitud media 202.03, mediana 200, sd 32.78, rango 145-293; entidades 'name_entities' media 1.20 (rango 1-3) y 'organizations' media 2.30 (rango 1-5). Los valores de la tesina (2.1 PER / 1.3 ORG) estan efectivamente intercambiados y desplazados. La discrepancia de longitud (187 vs 202) es menor; la inversion PER/ORG es el error sustantivo.
- **Corrección sugerida:** Corregir a 'longitud promedio 202 caracteres (rango 145-293), con 1,2 entidades PER y 2,3 entidades ORG por articulo'.

### A26. Marcador de referencia sin resolver '[referencia KPMG 2024]' sin entrada bibliografica, y uso de 'billones' (10^12) para traducir 'billion' en la cifra del mercado RegTech.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 65 (§1.1)
- **Verificación:** CONFIRMADO en ambos extremos. La cita existe literal en la linea 65. Un grep -i 'kpmg' sobre todo el documento devuelve UNICAMENTE esa linea 65: no hay ninguna entrada KPMG en la bibliografia §8 (verificada entrada por entrada, referencias [1]-[20]). El falso amigo tambien es real: 'USD 12.3 billones' en espanol significa 12,3 x 10^12, cifra que excede el PIB mundial; la fuente original es 12.3 billion = USD 12.300 millones.
- **Corrección sugerida:** Sustituir 'billones' por 'miles de millones' en ambas cifras (12.300 y 87.200 millones) y reemplazar '[referencia KPMG 2024]' por una cita IEEE numerada con su entrada correspondiente en §8.


## 🟠 Gravedad MEDIA (55)

### M1. F1 baseline N=120 con dos valores distintos: §5.6.1 (0.5983 / 0.5446) vs §5.3.5 y §5.6.5 (0.5925 / 0.5591)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L488-493 vs L439-441 y L616-617
- **Verificación:** Las citas son literales. PERO la corrección propuesta por el agente anterior es ERRÓNEA y destruiría datos reales: verifiqué que 0.5983/0.5868/0.5446/0.5189/0.3945 provienen íntegramente de la corrida dict-RAG results/benchmark_balanced_120_20260824_173036/benchmark_summary.json, mientras 0.5925/0.5591 provienen de results/benchmark_balanced_120_20260901_140421/. Son dos corridas distintas del mismo corpus, ambas válidas. La inconsistencia real es de trazabilidad: el texto de L486 dice «el benchmark principal sobre N=120» sin declarar de qué corrida procede cada tabla.
- **Corrección sugerida:** NO unificar cifras. Añadir en §5.6.1 la procedencia explícita (corrida 20260824_173036, dict-RAG) y en §5.6.5 la suya (20260901_140421, KB RAG), señalando que los baselines difieren por ser ejecuciones distintas.

### M2. gemma4:31b y gemma4:31b-mlx con métricas idénticas en Tabla 2, contradiciendo §5.3.1 y §5.5

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L375-376 vs L411-412 y L472-473
- **Verificación:** Verificado: L375 y L376 son idénticas en las seis columnas de métricas (67.83% / 57.29% / 86.78% / 0.15% / 114.20 / 0.81). En §5.3.1 (N=30) sí difieren (79.03% vs 77.47%) y en §5.5 tienen VRAM y Tok/s muy distintos (18.803 MB/11.37 vs 24.751 MB/27.56). La duplicación exacta es implausible como medición independiente.
- **Corrección sugerida:** Reportar los valores medidos para cada artefacto en N=15 o declarar explícitamente que la fila mlx replica la del artefacto GGUF por no existir corrida independiente en ese corpus.

### M3. Se declara Tabla 2 «ordenada por F1-Score» pero no lo está; el líder en negrita no es el de mayor F1

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L371, L375-388
- **Verificación:** Secuencia real de F1 en la tabla: 67.83, 67.83, 66.29, 69.81, 69.76, 65.47, 61.29... No es monótona decreciente. Además gemma4:31b (67.83%) va en negrita como líder pese a que gemma4:latest ZS-ES alcanza 69.81%.
- **Corrección sugerida:** Reordenar por F1 descendente o cambiar la frase al criterio real de orden, y revisar el resaltado del modelo líder.

### M4. Hallazgo 1 compara Recall de gemma4:31b (86.78%) contra el F1 del modelo cloud (66.29%), no contra su Recall (84.12%)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L390 vs L377
- **Verificación:** Cita literal de L390 confirmada. En L377 el 66.29% figura en la columna F1 de gemma4:31b-cloud y su Recall es 84.12%. La comparación mezcla dos métricas distintas.
- **Corrección sugerida:** Comparar Recall vs Recall (86.78% vs 84.12%) o explicitar que 66.29% es el F1 del modelo cloud.

### M5. §5.3.5 describe el subconjunto N=120 como «locales y en la nube», pero los 5 modelos son todos locales

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L435 y tabla L439-448
- **Verificación:** Cita literal verificada en L435. La tabla lista gemma4:31b-mlx, gemma4:latest, qwen2.5:14b, gemma:latest y llama3.2:latest; ninguno es cloud. Confirmado también contra benchmark_summary.json de la corrida 20260901_140421, cuyas 10 condiciones son esos 5 modelos locales × 2 modos.
- **Corrección sugerida:** Eliminar «y en la nube» de L435.

### M6. gemma:latest aparece en §5.3.5, §5.6.5 y §6.5 pero no está declarado en §4.2 ni en la Tabla 2

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L445-446, L454, L618, L634 vs L267-270 y L375-388
- **Verificación:** grep de «gemma:latest» en el documento devuelve solo L445, L446, L454, L618 y L634 (todas en §5.3.5/§5.6.5/§6.5). No aparece en §4.2 ni en Tabla 2. El modelo sí existe en los datos reales de la corrida (gemma:latest_baseline f1=0.4734), por lo que el problema es de declaración, no de dato.
- **Corrección sugerida:** Agregar gemma:latest al listado de §4.2 con su tamaño real, o justificar su incorporación tardía en §5.3.5.

### M7. «Los 11 modelos restantes» no cuadra con el número real de modelos del benchmark general

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L456
- **Verificación:** Cita literal confirmada en L456. El 11 solo se obtiene restando 5 de 16 (conteo erróneo). Con los 12 modelos distintos de Tabla 2, de los cuales 4 ya fueron re-evaluados en N=120 (gemma4:31b-mlx, gemma4:latest, qwen2.5:14b, llama3.2:latest), quedan 8.
- **Corrección sugerida:** Recalcular a 8 tras fijar el conteo real del benchmark general.

### M8. Resumen y abstract afirman «16 proveedores de modelos»; §3.3 documenta cuatro proveedores

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L29 y L39 vs L193
- **Verificación:** Citas literales verificadas. L193 enumera OllamaProvider, OpenAIProvider, AnthropicProvider y VertexAIProvider. En el repo hay además gliner_provider.py, es decir 5 implementaciones — en ningún caso 16. Se confunde «proveedores» con «modelos».
- **Corrección sugerida:** Cambiar a «cuatro proveedores» (o cinco, si se cuenta GLiNER) en resumen y abstract, o reformular a «modelos» con el conteo corregido.

### M9. Reducción de costos declarada como 60–80% en resumen/objetivos y 99.4% en resultados/conclusiones

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L29, L93 vs L476, L708
- **Verificación:** Las cuatro citas existen literalmente. L476 sí acota «en costo unitario», pero L708 (conclusión 4) presenta el 99.4% sin acotación y L29/L93 hablan de «costos operativos» en 60–80%, sin que el documento explique en ningún punto la diferencia de base de cálculo.
- **Corrección sugerida:** Añadir una frase que distinga costo unitario directo (99.4%) de costo operativo total incluyendo supervisión humana (60–80%), y repetir la acotación en la conclusión 4.

### M10. §6.1 y §7.2 invocan un objetivo de F1 ≥ 85% que no aparece en el capítulo 1 (donde la hipótesis fija ≥ 70%)

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L671 y L719 vs L79-93
- **Verificación:** Verificado: L79 fija F1 ≥ 70% y ninguno de los cinco objetivos específicos (L89-93) menciona 85%. L671 habla de «El objetivo original del proyecto propuso un F1 ≥ 85%» y L719 de «la brecha hacia el 85% de F1 objetivo». La aritmética de la brecha (85 − 79.03 = 5.97) es correcta, pero la meta nunca se declaró.
- **Corrección sugerida:** Declarar la meta aspiracional del 85% en §1.3/§1.4 o eliminar la referencia en §6.1 y §7.2.

### M11. Longitud del corpus N=30: ~200-400 caracteres en §4.1 vs promedio medido de 187 caracteres en el Paso 5

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L224 y L245 (repetido en L456)
- **Verificación:** Ambas citas verificadas literalmente. 187 queda fuera del rango declarado 200-400, y el rango se repite en L456 al comparar con el corpus N=120.
- **Corrección sugerida:** Homologar el rango declarado con la longitud promedio medida (p. ej. «~150-300 caracteres, promedio 187»).

### M12. El método declara un único par {PER, ORG} por artículo y verificado como únicas entidades, pero el Paso 5 reporta 2.1 PER y 1.3 ORG por artículo

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L232, L243 y L245
- **Verificación:** Las citas existen; corrijo la ubicación: la frase «eran las únicas entidades nombradas del tipo PER u ORG presentes» está en L243 (Paso 4), no en L238 (que es parte del prompt de generación). El contenido de la contradicción se sostiene: diseño de 1 PER + 1 ORG con descarte de artículos con entidades adicionales vs promedio reportado de 2.1/1.3.
- **Corrección sugerida:** Corregir la descripción del método (admitir múltiples entidades por artículo) o revisar las estadísticas del Paso 5.

### M13. Se afirma ejecutar modelos de ~24.7 GB de VRAM sobre hardware declarado con 16 GB de memoria unificada

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L125, L210 vs L361 y L833
- **Verificación:** Citas literales verificadas. Además comprobé el hardware: sysctl hw.memsize = 17.179.869.184 bytes = 16 GB (hw.model Mac17,4), y la corrida 20260901_140421 registra vram_mb = 26.606 para gemma4:31b-mlx y model_disk_mb = 17.768. Es decir, las cifras de memoria reportadas exceden la RAM física del equipo sin que el informe explique el mecanismo.
- **Corrección sugerida:** Explicar el mecanismo (memoria comprimida/swap de macOS, offload por capas) o revisar la interpretación de la métrica vram_mb instrumentada, que puede estar midiendo memoria del sistema y no residencia real en GPU.

### M14. §5.6.5 clasifica gemma4:latest como modelo grande >10B pese a declararlo de 9B, y etiqueta gemma:latest como 9B

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L632 y L634 vs L378 y L268
- **Verificación:** Verificado: L632 agrupa «gemma4:31b-mlx, gemma4:latest, >10B parámetros» mientras Tabla 2 (L378-379) y §4.2 (L268) declaran gemma4:latest como 9B; y L634 asigna «gemma:latest 9B» al grupo de pequeños/medianos. El mismo tamaño se atribuye a dos modelos distintos y el umbral de 10B es incompatible con 9B.
- **Corrección sugerida:** Cambiar el umbral a «≥9B» o reagrupar, y verificar el tamaño real de gemma:latest (Ollama gemma:latest es 7B, no 9B).

### M15. §5.6.1 afirma degradación RAG «consistente a lo largo de todos los modelos» pero la tabla solo aporta un valor RAG-Dict

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L486 y tabla L488-493
- **Verificación:** Confirmado y AGRAVADO por los datos: la corrida 20260824_173036 sí tiene RAG-dict para todos (gemma4:latest 0.5257, qwen2.5:14b 0.5071, llama3.2:latest 0.4196), es decir las celdas vacías son innecesarias. Y la afirmación de consistencia es falsa: con dict-RAG llama3.2 MEJORÓ (0.3945 → 0.4196), igual que nemotron-mini (0.3650 → 0.4704) y nuextract (0.4455 → 0.5085). La degradación fue mayoritaria, no universal.
- **Corrección sugerida:** Completar la columna RAG-Dict con los valores reales de la corrida 20260824_173036 y matizar el texto a «en la mayoría de los modelos evaluados», señalando las excepciones.

### M16. Citas del cuerpo en formato autor-año pese a declarar IEEE numerado; marcador de posición «[referencia KPMG 2024]»; «Alvarado et al., 2023» sin entrada; «Borne» vs «Bourne»

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L65, L107, L134, L255 vs L733-771
- **Verificación:** Todo verificado: L733 declara «*Formato IEEE*»; L65 contiene el marcador literal «[referencia KPMG 2024]»; L134 cita «[Alvarado et al., 2023]» y la bibliografía solo tiene [15] «M. Min et al., FiNER»; L255 cita «Borne, 2024» frente a [5] «K. Bourne». El marcador de posición sin resolver es el defecto más grave del conjunto.
- **Corrección sugerida:** Convertir las citas del cuerpo a numeración IEEE, resolver el marcador KPMG con una referencia real, alinear la cita de FiNER-139 con [15] y corregir Borne → Bourne.

### M17. La Tabla 1 atribuye a este trabajo un F1 de 79% sobre el dataset Kleptotrace/CoNLL-2002, cuando ese valor es del corpus sintético N=30

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L137
- **Verificación:** Cita literal verificada. El 79,03% procede del corpus sintético N=30 (§5.3.1 y log benchmark_augmented_30.log: gemma4:31b f1=0.790303), mientras que sobre el corpus nombrado en la tabla el informe reporta 67,83% (N=15, §5.1) y 59,25% en el corpus real N=120. Al ser la tabla de comparación con el estado del arte, la atribución induce a error frente a BloombergGPT/FiNER. Elevo la gravedad de baja a media por su ubicación en el posicionamiento del aporte.
- **Corrección sugerida:** Indicar en la celda el corpus exacto («corpus sintético AML N=30») o usar la cifra correspondiente al dataset nombrado (67,83% en N=15).

### M18. Falta en los tres docx la glosa metodologica de 'diseno factorial 2x2' que el .md vigente introdujo en §4.3 y §1.4.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §4.3 (parrafo introductorio) y §1.4 objetivo especifico 3
- **Verificación:** CONFIRMADO. La cadena 'factorial' NO aparece ni una vez en ninguno de los tres docx (grep sobre el texto completo de los tres = 0 coincidencias). El .md si la contiene dos veces: linea 91 ('un diseno factorial 2x2, denominado *estudio de ablacion* en la literatura de aprendizaje automatico') y linea 274 ('constituye un **diseno factorial 2x2**, procedimiento conocido en la literatura de aprendizaje automatico como *estudio de ablacion*'). El parrafo de los docx citado como evidencia ('Se evaluaron cuatro configuraciones de prompt sobre el modelo gemma4:latest (9B): 1. Zero-shot ingles (ZS-EN)...') existe literalmente y va directo a la enumeracion sin justificar el diseno.
- **Corrección sugerida:** Incorporar en los tres docx el parrafo de glosa del .md (§4.3, linea 274) y la formulacion del objetivo 3 (.md linea 91).

### M19. El RESUMEN en espanol de dos docx dice 'El estudio de ablacion de prompts demuestra' donde el .md vigente ya dice 'La comparacion de configuraciones de prompt demuestra'.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** RESUMEN, segundo parrafo
- **Verificación:** CONFIRMADO literalmente. Informe_Final_Tesina_NER.docx (parrafo 20) y 2026-07-04_Borrador-Informe-Final-Tesina.docx (parrafo 18) contienen la frase exacta 'El estudio de ablacion de prompts demuestra que la localizacion linguistica al espanol produce una mejora de +7.4 puntos de F1 sobre el baseline zero-shot en ingles'. El .md vigente (linea 29) dice 'La comparacion de configuraciones de prompt demuestra que...'. Verificado tambien que la plantilla no presenta la divergencia porque su resumen fue reescrito y omite la frase.
- **Corrección sugerida:** Reemplazar en los dos docx por 'La comparacion de configuraciones de prompt demuestra que...'. Dejar intacto el abstract en ingles ('The prompt ablation study demonstrates').

### M20. Nombre del dataset corrompido y en castellano dentro del abstract en ingles: 'dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002'.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** ABSTRACT (ingles), segundo parrafo
- **Verificación:** CONFIRMADO literalmente en los dos docx y en el .md. La cadena exacta 'real financial sanctions dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002 (N=15 expert-annotated articles)' aparece en Informe_Final_Tesina_NER.docx (parrafo 25), en el borrador (parrafo 23) y en el .md vigente (linea 39). La plantilla ya dice correctamente 'real financial sanctions dataset Kleptotrace/CoNLL-2002 (N=15 expert-annotated articles)', confirmando la desincronizacion entre los tres archivos. Se trata de un residuo de un reemplazo de texto mal aplicado (palabra espanola 'balanceado' + duplicacion de 'CoNLL-2002').
- **Corrección sugerida:** Unificar los dos docx y el .md al texto ya corregido en la plantilla: 'the real financial sanctions dataset Kleptotrace/CoNLL-2002 (N=15 expert-annotated articles)'.

### M21. Formulacion internamente contradictoria en §4.1.2: llama 'datos reales balanceados' a un corpus que la misma frase declara 'generados por LLM' y que el propio apartado c) llama 'corpus sintetico'.

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** §4.1.2, frase de apertura y apartado c)
- **Verificación:** CONFIRMADO literalmente. En Informe_Final_Tesina_NER.docx (parrafos 129 y 132) y en el borrador (parrafos 136 y 139) aparecen exactamente 'El uso de datos reales balanceados generados por LLM para pruebas de hipotesis es valido...' y 'c) Validez de constructo del corpus sintetico: La validez de los datos reales balanceados como proxy del dominio real descansa en tres pilares'. La contradiccion es interna al mismo parrafo (reales vs. generados por LLM vs. sintetico). La plantilla ya lo corrigio a 'El uso de datos aumentados por LLM para pruebas de hipotesis es valido en este estudio porque...' (parrafo 103), de modo que los tres docx efectivamente no coinciden. Defecto heredado del .md.
- **Corrección sugerida:** Adoptar en el .md y en los dos docx afectados la redaccion de la plantilla: 'datos aumentados por LLM' / 'corpus sintetico', eliminando el calificativo 'reales balanceados'.

### M22. Llamadas a tablas desactualizadas tras la renumeracion segun plantilla institucional: el texto remite a 'Tabla 1' y 'Tabla 2' mientras las tablas inmediatamente debajo son la 2, la 3 y la 5.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §2.5 (llamada vs. Tabla 2), §3.1 (llamada vs. Tabla 3), §5.1 (llamada vs. Tabla 5)
- **Verificación:** CONFIRMADO con las tres parejas adyacentes verificadas en el texto extraido: parrafo 52 'La Tabla 1 posiciona este trabajo...' seguido del pie 'Tabla 2. Comparacion con Trabajos Relacionados...'; parrafo 64 'La Tabla 1 resume la arquitectura de cinco capas' seguido de 'Tabla 3. Arquitectura de Cinco Capas del Sistema'; parrafo 137 'La Tabla 2 resume los tres mejores y el peor desempeno' seguido de 'Tabla 5. Resultados Destacados del Benchmark General'. Ademas verifique que 'Tabla 1. Ficha del Informe' es efectivamente la primera tabla del documento. Comprobe tambien en word/document.xml que NO existen campos SEQ ni REF: los numeros y las llamadas son texto plano, por lo que Word no los corregira solo.
- **Corrección sugerida:** Actualizar las tres llamadas a 'la Tabla 2', 'la Tabla 3' y 'la Tabla 5' respectivamente; idealmente convertirlas en referencias cruzadas automaticas de Word (campos SEQ/REF), hoy inexistentes.

### M23. Salto en la numeracion de subsecciones: no existe §5.6.6; se pasa de 5.6.5 a 5.6.7.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §5.6, entre 5.6.5 (Resultados Empiricos del KB RAG) y 5.6.7 (Justificacion Metodologica)
- **Verificación:** CONFIRMADO. Los encabezados de nivel 5.6.x de la plantilla son exactamente: 5.6.1, 5.6.2, 5.6.3, 5.6.4, 5.6.5 y 5.6.7 — no hay 5.6.6. El .md vigente si tiene '5.6.6 Analisis Comparativo Cronologico' y los otros dos docx tambien la incluyen (Informe_Final_Tesina_NER.docx la lista entre 5.6.5 y 5.6.7). Verifique tambien la evidencia: el ultimo parrafo de 5.6.5 remite al Anexo D ('La comparacion detallada entre el sistema RAG v1.0 ... se documenta en el Anexo D.') y a continuacion arranca '5.6.7 Justificacion Metodologica'. El contenido efectivamente se traslado a 'D.5 Analisis Comparativo Cronologico — RAG v1.0 vs. v1.1', pero no se renumero.
- **Corrección sugerida:** Renumerar 5.6.7 como 5.6.6, o reponer una 5.6.6 breve de una linea que remita al Anexo D.5.

### M24. Las subsecciones D.6, D.7 y D.8 aparecen fisicamente DESPUES del Anexo F, rompiendo el orden de los anexos.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** Seccion 9 (Anexos): tras '9.6 Anexo F' y antes de '9.7 Anexo G'
- **Verificación:** CONFIRMADO. La secuencia real de encabezados de anexos es: 9.1 Anexo A, 9.2 Anexo B, 9.3 Anexo C, 9.4 Anexo D, D.1, D.2, D.3, D.4, D.5, 9.5 Anexo E, 9.6 Anexo F, D.6 (Degradacion Observada — RAG por Diccionario), D.7 (Mini-Benchmark de Validacion Preliminar N=5), D.8 (Reglas de la Base de Conocimientos Contextual), 9.7 Anexo G. Las Tablas 21, 22 y 23 cuelgan de esos tres bloques desubicados. La evidencia citada coincide con el texto real.
- **Corrección sugerida:** Mover los bloques D.6, D.7 y D.8 con sus Tablas 21, 22 y 23 al interior del Anexo D, despues de D.5 y antes de '9.5 Anexo E'.

### M25. Contradiccion numerica visible: el titulo de §5.1 dice '16 Modelos' mientras la linea siguiente y el Anexo E dicen '13 configuraciones evaluadas'.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §5.1 (titulo y parrafo introductorio) y §9.5 Anexo E (titulo y pie de Tabla 20)
- **Verificación:** CONFIRMADO, con una precision. La plantilla dice literalmente '5.1 Benchmark General — 16 Modelos sobre Kleptotrace/CoNLL-2002 (N=15)' seguido de 'La Tabla 2 resume los tres mejores y el peor desempeno del benchmark completo (13 configuraciones evaluadas)...', y '9.5 Anexo E — Resultados Completos del Benchmark General (13 Configuraciones, N=15)'. Verifique ademas que la cadena '13 configuraciones' no aparece ni en el .md ni en los otros dos docx, y que la Tabla 20 tiene efectivamente 13 filas de datos — es decir, '13' es el numero CORRECTO. PRECISION al hallazgo original: la contradiccion de fondo (titulo '16 Modelos' sobre una tabla de 13 filas, mas §4.2 '15 modelos' y §2.5 '16 modelos') existe identica en el .md y en los otros dos docx; lo exclusivo de la plantilla es hacerla explicita en lineas contiguas. Tambien confirmo la discrepancia heredada 15 vs. 16 modelos en §4.2 y §2.5 de los cuatro documentos.
- **Corrección sugerida:** Unificar el conteo con un criterio unico (p. ej. '13 configuraciones sobre 11 modelos') y corregir de forma coherente el titulo de §5.1, la cifra de §4.2 y la de §2.5 en los CUATRO documentos, no solo en la plantilla.

### M26. La plantilla contiene cuatro anexos (D, E, F y G) que no existen ni en el .md vigente ni en los otros dos docx; la fuente maestra quedo por detras del entregable.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** Seccion 9, apartados 9.4 a 9.7
- **Verificación:** CONFIRMADO. La plantilla lista 9.1 Anexo A, 9.2 Anexo B, 9.3 Anexo C, 9.4 Anexo D (Detalle Tecnico KB RAG, con D.1-D.8 y Tablas 14-19, 21-23), 9.5 Anexo E (Resultados Completos, Tabla 20), 9.6 Anexo F (Metodologia del Corpus N=30) y 9.7 Anexo G (Declaracion de Uso de IA, con G.1-G.4). El .md vigente solo declara 'Anexo A', 'Anexo B' y 'Anexo C' (lineas 777, 824, 828), y lo mismo Informe_Final_Tesina_NER.docx y el borrador. Verifique tambien el dato nuevo citado: '20 commits entre el 29 de junio y el 1 de septiembre de 2026' existe literalmente en el Anexo G. Buena parte de D, E y F es contenido del cuerpo reubicado por limite de extension, pero el Anexo G es material genuinamente nuevo que no tiene contraparte en ningun otro documento.
- **Corrección sugerida:** Portar los Anexos D, E, F y G al .md vigente de forma aditiva (sin borrar contenido previo, conforme a la politica del proyecto) para que la fuente maestra y el entregable dejen de divergir.

### M27. La entrada del 2026-07-01 declara finalizado el benchmark del dataset real benchmark_balanced_120.json sobre la suite de 16 modelos y atribuye a gemma4:31b un F1 de 67.83% sobre ese corpus, lo que es anacronico y confunde corpus y numero de modelos.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Lineas 18-19
- **Verificación:** CONFIRMADO textualmente: las lineas 18-19 dicen exactamente lo citado. El corpus benchmark_balanced_120.json entro a git recien en el commit 5ff38f5 del 2026-09-01 (git log -S 'benchmark_balanced_120' no muestra nada anterior), y results/RUNS_INDEX.md fecha la primera corrida sobre ese corpus el 2026-08-24 17:30 (fila #10). El 67.83% corresponde a la corrida #6 del RUNS_INDEX (kleptotrace.json N=15, 2026-07-01 14:45), coherente con HISTORIAL-CONSOLIDADO.md linea 90 y con doc/organized/Hito_4_Tarea3_Informe_Avance/Informe-Avance-2-v2.md linea 58 ('15 modelos ... 15 articulos'). ATENUANTES verificados: (a) el archivo esta declarado historico e inmodificable en HISTORIAL-CONSOLIDADO.md linea 23 y regla 6 (linea 200); (b) la cifra NO se propago mal a la tesina: en doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md lineas 257 y 375 el 67.83% se atribuye correctamente al corpus real N=15. El riesgo practico es por tanto bajo, pero la contradiccion existe.
- **Corrección sugerida:** NO editar /WORKLOG.md. Anotar de forma aditiva en HISTORIAL-CONSOLIDADO.md que la entrada del 2026-07-01 nombra mal el corpus (era kleptotrace.json N=15, no benchmark_balanced_120.json) y el numero de modelos, remitiendo a results/RUNS_INDEX.md filas #6 y #10.

### M28. En la entrada de Confidencialidad se declara pendiente propagar la eliminacion de la mencion a la organizacion vinculada a los otros DOCX, cuando dos lineas antes se declara ya hecha.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Linea 151 vs linea 149
- **Verificación:** CONFIRMADO. Las lineas 149 y 151 existen literalmente y se contradicen: 149 afirma haber eliminado la mencion en los tres DOCX; 151 la declara pendiente para Informe_Final_Tesina_NER.docx y para la version fusionada con la plantilla. Verificado en disco descomprimiendo los tres DOCX completos (no solo word/document.xml): grep -ril sobre TODAS las partes de Informe_Final_Tesina_NER.docx, Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx y doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx devuelve cero coincidencias, incluidos encabezados y pies. La linea 151 esta superada.
- **Corrección sugerida:** Anadir nota aditiva bajo la linea 151: 'propagacion completada y verificada el 2026-09-03 en los tres DOCX (0 coincidencias en todas las partes del paquete OOXML)'. El unico pendiente real sigue siendo la decision del autor sobre los documentos historicos de Hito 4, que por politica no se modifican.

### M29. Las tablas de estado (§1 y §2) declaran 24 paginas de cuerpo, pero §9, escrita despues el mismo dia, verifica 20 paginas de cuerpo y anexos desde la 21.

- **Archivo:** `HISTORIAL-CONSOLIDADO.md`
- **Ubicación:** Lineas 18 y 34 vs linea 253
- **Verificación:** CONFIRMADO literalmente. Linea 18: 'Vigente - cuerpo 24 pp. + anexos'. Linea 34: '| Extension del cuerpo | <= 25 paginas, excluyendo anexos | OK 24 paginas |'. Linea 253: '29 paginas totales; cuerpo de 20 paginas (portada, resumen y capitulos 1-8); anexos desde la 21'. La misma cifra de 20 pp. se repite en research/rag/WORKLOG.md linea 285. Las tablas de estado, que son las que se leen como estado vigente, quedaron desactualizadas y hacen creer que la holgura frente al limite de 25 pp. es de 1 pagina cuando §9 y la linea 287 del WORKLOG RAG dicen 5.
- **Corrección sugerida:** Actualizar (o anotar con remision a §9) las lineas 18 y 34 a 'cuerpo 20 pp., anexos desde la 21 (verificado 2026-09-03, §9)'.

### M30. §9 afirma anadir una 'tarea 11' al cronograma de §7, pero la tabla de §7 termina en la tarea 10.

- **Archivo:** `HISTORIAL-CONSOLIDADO.md`
- **Ubicación:** Linea 263 vs lineas 176-187
- **Verificación:** CONFIRMADO. La linea 263 dice literalmente 'Se anade como tarea 11 del cronograma (§7).' La tabla de §7 va de la linea 178 (fila 1) a la linea 187 (fila 10, 'Verificacion final'); no hay fila 11. grep de '| 11 ' y de 'tarea 11' en todo el archivo devuelve una unica coincidencia, la propia linea 263. La tarea de reincorporar al cuerpo el material de los Anexos D-F efectivamente no quedo registrada en el cronograma.
- **Corrección sugerida:** Anadir la fila 11 a §7 (o insertarla antes de 'Verificacion final', que debe quedar ultima), con entrada requerida 'decision del autor' y criterio de termino explicito sobre la tabla del Anexo E en §5.1.

### M31. El porcentaje de mejora del mini-experimento N=5 esta mal calculado: se cita +105% para un salto de F1 0.2367 a 0.7216.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Linea 14
- **Verificación:** CONFIRMADO. La linea 14 dice literalmente 'Mini-experimento N=5 (llama3.2): Dict-RAG F1=0.2367 vs KB-RAG F1=0.7216 (+105%)'. Los dos F1 coinciden con la tabla del documento fuente research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md (linea 146: Dict-RAG 0.2367; linea 147: KB-RAG 0.7216; linea 145: Baseline 0.5614). Aritmetica: variacion relativa (0.7216-0.2367)/0.2367 = +204.9%; diferencia absoluta = +48.5 pp; frente al baseline, (0.7216-0.5614)/0.5614 = +28.5%. Ninguna lectura da 105%. HALLAZGO ADICIONAL VERIFICADO: el mismo tipo de error SI se propago a la tesina; en Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx aparece '0.2367 (-33% vs baseline)', y -33 es en realidad la diferencia en puntos porcentuales (0.5614-0.2367 = -32.5 pp); la variacion relativa seria -57.8%.
- **Corrección sugerida:** Corregir a '+204.9% relativo (=+48.5 pp) respecto del Dict-RAG' y explicitar el Baseline 0.5614. Revisar ademas la tesina: cambiar '0.2367 (-33% vs baseline)' por '-32.5 pp vs baseline' o por '-57.8%', segun la magnitud que se quiera reportar, y aplicar el mismo criterio a las demas cifras de esa tabla.

### M32. BENCHMARKS.md declara Redis como prerequisito obligatorio y exige `redis-cli ping`, pero ninguna ruta de ejecucion lo usa.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 9-13 y 91-92
- **Verificación:** CONFIRMADO parcialmente en su nucleo. BENCHMARKS.md:9 dice literal '3. **Redis** – Required for the Pub/Sub coordination' y la linea 92 exige `redis-cli ping`. src/main.py llama `create_task_queue(use_redis=False)` en sus cuatro rutas (259, 386, 461, 546) y src/pub_sub.py:138-145 solo instancia RedisTaskQueue si use_redis=True. Por tanto ninguna corrida catalogada necesita Redis. Matiz: `redis>=5.0` sigue en requirements.txt y RedisTaskQueue existe (src/pub_sub.py:86), asi que la dependencia es opcional, no inexistente.
- **Corrección sugerida:** Marcar Redis como opcional (solo si se activa RedisTaskQueue en src/pub_sub.py) y sacar `redis-cli ping` de la secuencia obligatoria.

### M33. BENCHMARKS.md afirma que ./run_benchmark.sh lanza el benchmark 'con la configuracion de arriba'; el script tiene su propia lista fija y pasos no documentados.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 88-96
- **Verificación:** CONFIRMADO. BENCHMARKS.md:88 dice literal 'The repository ships a convenience script that launches the benchmark with the configuration above'. run_benchmark.sh (lineas 22-41) pasa --data-file data/benchmark_balanced_120.json --rag-study --batch-size 3 con 16 modelos hardcodeados por --models (el echo de la linea 21 dice '15 models', otra inconsistencia menor del propio script), y luego ejecuta ademas `--ablation` sobre gemma4:latest (linea 44) y `src/simulate_production.py` (linea 47). Nada de eso figura en BENCHMARKS.md.
- **Corrección sugerida:** Documentar lo que realmente hace run_benchmark.sh (barrido --rag-study con lista fija de 16 modelos + corrida de ablacion + simulacion de produccion) o parametrizarlo para que lea la lista desde src/config.py.

### M34. BENCHMARKS.md referencia results/summary_metrics.json, archivo que ningun modulo produce.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 116 y 128
- **Verificación:** CONFIRMADO. Las lineas 116 y 128 citan `results/summary_metrics.json`. src/main.py:178 escribe `benchmark_summary.json` y src/dashboard.py lo lee con ese nombre en las lineas 40, 56 y 106. No existe ningun summary_metrics.json en el repositorio.
- **Corrección sugerida:** Reemplazar `summary_metrics.json` por `benchmark_summary.json` en las lineas 116 y 128.

### M35. BENCHMARKS.md remite al notebook visualize_results.ipynb en notebooks/, que no existe.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 130
- **Verificación:** CONFIRMADO. La linea 130 cita literal el notebook. `ls notebooks` devuelve 'No such file or directory' y no hay ningun .ipynb en el repo. La herramienta de visualizacion real es src/dashboard.py (Streamlit), documentada en README.md seccion 6.
- **Corrección sugerida:** Sustituir por `streamlit run src/dashboard.py`.

### M36. En la tabla 'RAG Integration Study' hay filas con F1 aritmeticamente imposible respecto de su Precision y Recall.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Lineas 190-196
- **Verificación:** CONFIRMADO en dos de las tres filas citadas, con un razonamiento mas fuerte que el del hallazgo original. src/evaluator.py:356-359 promedia por registro (mean de f1, precision y recall por separado), no deriva F1 de P/R agregados. Aun asi, como f1_i <= (p_i+r_i)/2 para todo registro, mean(F1) <= (mean(P)+mean(R))/2. Fila llama3.2:latest_rag (linea 193): cota 0.7646 < 0.8783 declarado -> imposible. Fila llama3.1:8b_baseline (linea 194): cota 0.7334 < 0.7667 -> imposible. En cambio llama3.1:8b_rag_enhanced (linea 195): cota 0.8334 >= 0.7750 -> esa fila NO es inconsistente, el hallazgo original se equivoca al incluirla. La tabla tampoco declara corpus, run_id ni metodo de agregacion.
- **Corrección sugerida:** Recalcular las filas llama3.2:latest_rag y llama3.1:8b_baseline desde el CSV de la corrida de origen y declarar explicitamente que el F1 es la media de F1 por registro (src/evaluator.py::aggregate_model_results). No tocar la fila llama3.1:8b_rag_enhanced, que es consistente.

### M37. La lista de modelos de BENCHMARKS.md incluye glm-5.1:cloud, inexistente en el resto del proyecto, y no cuadra con la tabla de resultados de la misma pagina.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 40 (bloque JSON) y tabla lineas 154-167
- **Verificación:** CONFIRMADO. `grep -rn 'glm-5'` en todo el repo (excluyendo venv) devuelve solo BENCHMARKS.md:40 y su copia BENCHMARKS.md.bak_pre20260903:41. No esta en BenchmarkConfig.models (src/config.py:59-69), ni en la tabla 8.6 de AGENTS.md, ni en run_benchmark.sh, ni en ninguna corrida de RUNS_INDEX.md. Ademas el bloque JSON lista 17 modelos (lineas 38-54) y la tabla de resultados tiene 14 filas (154-167): faltan gemma4:12b-mlx, gpt-oss:20b, phi3.5:latest y glm-5.1:cloud, y la tabla incluye gemma4:latest, que no esta en el JSON. src/config.py si incluye gemini-3.1-flash-lite y gemini-3.5-flash, ausentes del bloque JSON.
- **Corrección sugerida:** Sincronizar la lista con BenchmarkConfig.models (src/config.py:59-69) y con AGENTS.md 8.6, eliminando glm-5.1:cloud si nunca fue evaluado o documentando por que se solicito y no se ejecuto.

### M38. AGENTS.md 8.1 indica una ruta incorrecta para la lista de modelos (__post_init__ en vez de campo del dataclass) y afirma que no hay que tocar ningun otro archivo.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Lineas 67-75 (y 104-113)
- **Verificación:** CONFIRMADO. AGENTS.md:72 dice literal 'src/config.py  →  BenchmarkConfig.__post_init__  →  self.models = [...]' (repetido en el snippet de la linea 106). En src/config.py, `models` es campo del dataclass en la linea 59 (`models: list[str] = field(default_factory=lambda: [...])`); __post_init__ empieza en la linea 98 y solo deriva results_dir/checkpoint_file y ejecuta assert_not_results_root. Ademas 'No other file needs to be changed' (linea 75) es falso: run_benchmark.sh lleva 16 modelos hardcodeados en las lineas 25-40 pasados por --models, que sobreescriben config.models (src/main.py:764-765).
- **Corrección sugerida:** Corregir la ruta a `src/config.py -> BenchmarkConfig.models (campo del dataclass, linea 59)` y anadir run_benchmark.sh (lineas 25-40) a la lista de lugares a sincronizar.

### M39. Contradiccion interna en AGENTS.md sobre si los modelos Cloud (Ollama) requieren `ollama pull`; la tabla 8.2 tampoco contempla los modelos gemini-*.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Linea 84 (tabla 8.2) vs lineas 97-102 (paso 1 de 8.3)
- **Verificación:** CONFIRMADO. AGENTS.md:84 dice para Cloud (Ollama) 'Needs ollama pull: ✅ Yes (`ollama pull`)', mientras AGENTS.md:97 y 101 dicen '(skip for cloud models)' y 'Cloud models are already available, no pull needed.' Son afirmaciones opuestas. Ademas la tabla 8.2 solo contempla Local / Cloud (Ollama) / NuExtract / Qwen3, y src/providers/factory.py:45-49 enruta gpt-* a OpenAIProvider, claude-* a AnthropicProvider, gemini-* a VertexAIProvider (linea 48) y gliner:* a GlinerProvider: esos patrones caerian erroneamente en la fila 'Local'.
- **Corrección sugerida:** Unificar el criterio (los modelos cloud de Ollama no requieren pull) y agregar filas para los patrones `gemini-*`, `gpt-*`, `claude-*` y `gliner:*` con su provider correspondiente.

### M40. AGENTS.md seccion 5 lista como pendientes tareas ya ejecutadas y remite a secciones que no existen en TODO.md.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Lineas 40-47 (seccion 5)
- **Verificación:** CONFIRMADO. AGENTS.md:44 dice literal 'Expand evaluation sweeps from the 20-record prototype sample to the full financial compliance sanctions dataset'. Ese barrido se hizo: RUNS_INDEX #11 (N=120, 15 modelos, 3600 filas) y #13 (N=120, 1200 filas), esta ultima verificada en disco. El punto 2 pide Tukey HSD y matrices de confusion 'once large-scale results are fully generated': src/main.py:22 ya importa run_tukey_posthoc y la linea 182 escribe confusion_matrix.json en cada corrida (presente en results/kleptotrace_20260727_110454/ y en los directorios de agosto/septiembre). Ademas TODO.md (39 lineas) contiene unicamente el plan RAG: ninguno de los items de AGENTS.md 5 existe alli, pese a que la linea 41 lo llama 'master TODO.md'.
- **Corrección sugerida:** Marcar como completadas de forma aditiva, con fecha y run_id (#11, #13), y alinear la referencia al TODO.md real.

### M41. La seccion 'Running the Pipeline' del README no cubre --rag-study/--rag-mode ni --ablation, los experimentos centrales de la tesina.

- **Archivo:** `README.md`
- **Ubicación:** Lineas 23-59
- **Verificación:** CONFIRMADO. Las seis subsecciones del README (lineas 25-59) cubren activar venv, barrido basico, simulate_production, --compare-annotators, memory_stress_test y el dashboard. Un grep de 'rag' y 'ablation' en README.md no devuelve nada. src/main.py:713-728 expone --ablation y --rag-mode {entities,kb_guidelines,kb_fewshot,kb_combined}, y la corrida vigente de la tesina (#13, verificada en disco con rag_mode kb_combined) no es reproducible siguiendo solo el README.
- **Corrección sugerida:** Anadir subsecciones para el estudio RAG (`--rag-study --rag-mode kb_combined`) y para la Comparacion de Configuraciones de Prompt (`--ablation`), con los comandos exactos de las corridas catalogadas en RUNS_INDEX.md.

### M42. TODO.md mantiene pendiente ampliar benchmark_balanced_120.json a >100 records, tarea ya cumplida.

- **Archivo:** `TODO.md`
- **Ubicación:** Linea 38
- **Verificación:** CONFIRMADO. TODO.md:38 tiene la casilla sin marcar con el texto citado. Verificado por lectura del archivo: data/benchmark_balanced_120.json es un dict con clave 'dataset' de longitud 120, por encima del umbral >100. Ademas ya se corrieron dos barridos completos sobre el (#11 y #13, ambos con directorio propio en results/).
- **Corrección sugerida:** Marcar como [x] con nota de cierre citando la corrida balanced120_N120__rag-kb-combined__zs-en__20260901_140421.

### M43. TODO.md mantiene pendiente experimentar con modelos mas grandes (Gemma 31B / Qwen 14B) con RAG, ya ejecutado.

- **Archivo:** `TODO.md`
- **Ubicación:** Linea 39
- **Verificación:** CONFIRMADO. TODO.md:39 sigue con casilla vacia. results/benchmark_balanced_120_20260901_140421/benchmark_summary.json contiene exactamente gemma4:31b-mlx_baseline (F1 0.5925) / gemma4:31b-mlx_kb_rag (0.5907) y qwen2.5:14b_baseline (0.5189) / qwen2.5:14b_kb_rag (0.5651), junto a gemma4:latest, gemma:latest y llama3.2:latest. Los deltas coinciden con los de RUNS_INDEX #13 (qwen2.5:14b +4.62 pp, gemma4:31b-mlx -0.18 pp).
- **Corrección sugerida:** Marcar como [x] con los resultados verificados de la corrida del 2026-09-01.

### M44. TODO.md mantiene pendiente implementar few-shot dinamico via RAG, ya implementado.

- **Archivo:** `TODO.md`
- **Ubicación:** Linea 37
- **Verificación:** CONFIRMADO. TODO.md:37 sigue con casilla vacia. src/main.py:715-728 define --rag-mode con las opciones kb_fewshot ('dynamic few-shot annotated example') y kb_combined ('guidelines + exemplar (recommended, best F1)'); src/config.py:84-91 documenta los mismos modos apuntando a src/kb_rag_manager.py, que existe en el repo. La corrida #13 se ejecuto con kb_combined.
- **Corrección sugerida:** Marcar como [x] referenciando `--rag-mode kb_fewshot` / `kb_combined` y src/kb_rag_manager.py.

### M45. La regla 1 de la seccion 4.3 de RUNS_INDEX se presenta como propuesta, pero ya esta implementada y activa.

- **Archivo:** `RUNS_INDEX.md`
- **Ubicación:** Linea 93 (encabezado seccion 4) y lineas 142-143 (regla 1)
- **Verificación:** CONFIRMADO. El encabezado de la linea 93 dice '## 4. Esquema de versionado propuesto (a partir de 2026-09-03)' y las lineas 142-143 enuncian la regla 1 en futuro. src/config.py:31-54 define assert_not_results_root(), que lanza ResultsDirRootError con el mensaje 'ABORT: refusing to run with results_dir=...', y se invoca incondicionalmente al final de __post_init__ (linea 111) y de nuevo en ensure_directories (linea 143) como segunda linea de defensa. Ninguna corrida puede ya escribir en la raiz de results/.
- **Corrección sugerida:** Marcar la regla 1 como IMPLEMENTADA (2026-09-03, src/config.py::assert_not_results_root) mediante nota aditiva en la seccion 6, dejando las reglas 2-4 como propuestas.

### M46. El conteo de directorios de resultados de RUNS_INDEX (5) esta desactualizado y el catalogo omite directorios existentes.

- **Archivo:** `RUNS_INDEX.md`
- **Ubicación:** Linea 21 (resumen ejecutivo) y tabla de la seccion 2
- **Verificación:** CONFIRMADO, con una correccion al numero del hallazgo. La linea 21 declara '**5**'. Hoy existen SIETE subdirectorios en results/: benchmark_balanced_120_20260824_173017, _20260824_173036, _20260825_071207, _20260901_140421, kleptotrace_20260727_110454, DESCARTADA_ragmode_incorrecto_142604 (2026-09-03 14:25; solo .checkpoint.json de 956 KB y benchmark.log de 1.0 MB, sin run_config.json) y benchmark_balanced_120_kbrag_9models (2026-09-03 14:27, solo benchmark.log, aparentemente una corrida en curso). El hallazgo original decia 6 porque el septimo aparecio despues. Ninguno de los dos ultimos tiene fila en la seccion 2, pese a que el encabezado (linea 3) se declara exhaustivo ('Cataloga TODAS las corridas del benchmark encontradas en el repositorio').
- **Corrección sugerida:** Agregar aditivamente filas #14 (DESCARTADA_ragmode_incorrecto_142604, estado 'Descartada / abortada') y #15 (benchmark_balanced_120_kbrag_9models, verificar si sigue en ejecucion antes de catalogarla), y actualizar el conteo mediante nota en la seccion 6.

### M47. El mismo modelo y modo baseline sobre 'N=120' aparece con dos F1 distintos en el mismo capitulo (0.5983 en §5.6.1 vs 59.25% en §5.3.5/§5.6.5) porque provienen de corridas distintas que el texto no distingue.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 490 (§5.6.1) vs lineas 439 y 630 (§5.3.5 y §5.6.5)
- **Verificación:** CONFIRMADO, y ambas cifras reproducen exactamente de corridas distintas. Recalculo propio: results/benchmark_balanced_120_20260824_173036 -> gemma4:31b-mlx_baseline 0.5983, _rag_enhanced 0.5868 (delta -0.0115), gemma4:latest_baseline 0.5446, qwen2.5:14b 0.5189, llama3.2 0.3945 = tabla de §5.6.1 al centesimo. results/benchmark_balanced_120_20260901_140421 -> gemma4:31b-mlx_baseline 0.5925, _kb_rag 0.5907 = tablas de §5.3.5 y §5.6.5. §5.3.5 SI cita su directorio (linea 435); §5.6.1 (linea 486) solo dice 'el benchmark principal sobre N=120', sin identificar corrida, de modo que el lector no puede reconciliar 0.5983 con 0.5925. Es un defecto de trazabilidad, no de calculo.
- **Corrección sugerida:** Anadir al encabezado de la tabla de §5.6.1 la cita explicita 'corrida results/benchmark_balanced_120_20260824_173036 (RAG por diccionario, 24-25 ago 2026)' para distinguirla de la corrida KB RAG del 1 de septiembre.

### M48. Se describe el subconjunto N=120 como '5 modelos (locales y en la nube, de distinto tamano)' cuando los cinco son locales.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 435 (§5.3.5)
- **Verificación:** CONFIRMADO. Cita literal verificada en linea 435. results/benchmark_balanced_120_20260901_140421/run_config.json lista exactamente: llama3.2:latest, gemma4:latest, gemma4:31b-mlx, qwen2.5:14b, gemma:latest. El CSV de esa corrida (1200 filas) contiene solo esos 5 modelos x 2 modos (baseline/kb_rag). Ningun modelo cloud (gemma4:31b-cloud, minimax-m3:cloud, gemini) participo. Coincide ademas con la fila #13 de results/RUNS_INDEX.md.
- **Corrección sugerida:** Cambiar a 'un subconjunto de 5 modelos locales de distinto tamano (3B a 31B)'.

### M49. Los valores de VRAM y Tok/s de la tabla de eficiencia (§5.5) no se reproducen desde ningun CSV.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** lineas 472-474 (§5.5)
- **Verificación:** CONFIRMADO. Citas literales verificadas en lineas 472-474. Un grep de '24751|24,751|27.56|18803|18,803|11.37' sobre todos los .md, .log, .json y .csv del proyecto devuelve UNICAMENTE las lineas 472-473 del propio borrador: ningun otro archivo del repositorio contiene esos valores. Los datos crudos difieren: results/benchmark_results.csv da para gemma4:31b-mlx vram_mb medio 24607.3 y tokens_per_sec 22.80; results/benchmark_balanced_120_20260901_140421 da 26606.2 y 22.88. Para llama3.2 los CSV dan 4018.4 MB / 79.35 tok/s (N=15) y 3920.4 MB / 84.98 tok/s (N=120), frente a '~3.000' y 47.5 de la tesina. Ademas la fila gemma4:31b (18.803 MB) es incompatible con la fila gemma4:31b-mlx (24.751 MB) que en §5.1 comparte metricas identicas.
- **Corrección sugerida:** Regenerar la tabla promediando vram_mb y tokens_per_sec desde el CSV de la corrida que se decida citar, o etiquetar explicitamente los valores como medidas puntuales de monitorizacion no persistidas.

### M50. Contradiccion interna del indice Tok/s/B: §5.1 reporta 0.81 para gemma4:31b-mlx y §5.5 reporta 0.89; el Hallazgo 3 usa 0.81.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 473 (§5.5) vs linea 376 (§5.1)
- **Verificación:** CONFIRMADO, y la contradiccion es incluso mayor que la reportada. Linea 376 (§5.1): gemma4:31b-mlx -> 0.81. Linea 473 (§5.5): gemma4:31b-mlx -> 0.89. Linea 375 (§5.1): gemma4:31b -> 0.81 vs linea 472 (§5.5): gemma4:31b -> 0.37. Y para llama3.2, linea 381 (§5.1) da 18.73 mientras la linea 474 (§5.5) da 15.8. Ninguno de los tres pares coincide. El dato crudo (results/benchmark_results.csv) da 22.80 tok/s / 31B = 0.735 para gemma4:31b-mlx y 79.35/3 = 26.45 para llama3.2.
- **Corrección sugerida:** Unificar el indice a un unico valor por modelo calculado desde tokens_per_sec del CSV citado, y propagarlo a §5.1, §5.5, Hallazgo 3 y §6.3.

### M51. Error de razon en §6.3: 18.73 es el valor absoluto del indice Tok/s/B de llama3.2, no un multiplicador respecto a gemma4:31b.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 679 (§6.3)
- **Verificación:** CONFIRMADO. Cita literal verificada en linea 679: 'un indice de eficiencia de hardware (Tok/s/B) 18.73 veces mayor'. En la Tabla 2 (linea 381) 18.73 es la columna Tok/s/B de llama3.2 en valor absoluto, y el Hallazgo 3 (linea 392) lo usa correctamente asi ('llama3.2 (18.73 Tok/s/B)'). Como razon frente a gemma4:31b (0.81 Tok/s/B, misma tabla) el cociente es 23.1x. Con datos crudos (llama3.2 79.35/3=26.45; gemma4:31b-mlx 22.80/31=0.735) la razon seria ~36x. La formulacion actual confunde magnitud con razon.
- **Corrección sugerida:** Reformular como 'un indice de eficiencia de hardware de 18,73 Tok/s/B, aproximadamente 23 veces superior al de gemma4:31b (0,81)'.

### M52. El mini-benchmark N=5 (§5.6.5) no tiene datos crudos persistidos y sus cifras contradicen el otro experimento N=5 con el mismo modelo y corpus.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** lineas 606-610 (§5.6.5)
- **Verificación:** CONFIRMADO en lo esencial, con un matiz. Verificado que ningun benchmark_results.csv del repositorio tiene 5 registros: los seis CSV existentes tienen 450, 3600, 60, 1200, 120 y 480 filas; los dos directorios sin CSV (DESCARTADA_ragmode_incorrecto_142604 y benchmark_balanced_120_kbrag_9models) solo contienen .checkpoint.json y benchmark.log. Matiz: F1 0.3521->0.5489 SI estan documentados como texto en research/rag/WORKLOG.md (linea 83) y research/rag/TODO-RAG-20260901.md (linea 35), y el WORKLOG tambien registra 'Recall: 33.3% -> 59.5%', que coincide con la tabla; solo las precisiones 0.4250/0.5227 no aparecen en ninguna otra fuente. La contradiccion senalada es real: research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md (tabla 7.1) reporta para el mismo modelo, mismo corpus y misma condicion baseline F1=0.5614 / P=0.5238 / R=0.6286, frente a 0.3521 / 0.4250 / 0.3333 aqui.
- **Corrección sugerida:** Etiquetar la tabla como 'sondeo de validacion funcional N=5 (2026-09-01), resultados no persistidos en results/', explicar por que su baseline difiere del sondeo del 31-08 (0.3521 vs 0.5614), y apoyar las conclusiones en el benchmark N=120 que si es reproducible.

### M53. El par 'Recall: 62.8% -> 21.6%' se presenta bajo un encabezado que habla del benchmark N=120 y se cita en §5.6.7 como evidencia empirica cuantitativa, cuando procede de un sondeo de 5 articulos.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 513 (diagrama de §5.6.1) y linea 658 (§5.6.7)
- **Verificación:** CONFIRMADO. Ambas citas existen literalmente. El origen es research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md, tabla 7.1: baseline recall 0.6286 y RAG-diccionario 0.2158 sobre 'un protocolo de pruebas controlado sobre 5 articulos reales'. La seccion §5.6.1 en la que se inserta el diagrama abre con 'Durante el benchmark principal sobre N=120 articulos reales'. El dato equivalente en la corrida N=120 real (benchmark_balanced_120_20260824_173036) es llama3.2 recall 0.4081 -> 0.3291 (recalculo propio). Confirmada tambien la contradiccion interna del documento fuente: su linea 116 dice 'Recall cae de 62.8% a 14.9%' mientras su tabla 7.1 da 21.58%.
- **Corrección sugerida:** Etiquetar la cifra como 'sondeo cualitativo N=5 (llama3.2, 31-08-2026)' y anadir junto a ella el dato del benchmark N=120 (recall 40.8% -> 32.9%); resolver de paso la discrepancia 14.9% / 21.6% del documento de investigacion.

### M54. Recuento de modelos inconsistente: §5.1 dice '16 Modelos', §4.2 y el objetivo especifico 2 dicen '15 modelos', y la lista de §4.2 enumera solo 12.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 369 (§5.1) vs linea 267 (§4.2) vs linea 89 (objetivo 2)
- **Verificación:** CONFIRMADO. Linea 369: '### 5.1 Benchmark General — 16 Modelos sobre Kleptotrace/CoNLL-2002 (N=15)'. Linea 267: 'Se evaluaron 15 modelos LLM generativos distribuidos en tres categorias'. Linea 89 (objetivo 2): 'Evaluar y comparar el desempeno de 15 modelos'. Conteo de la lista de §4.2 (lineas 268-270): 6 locales grandes + 4 compactos + 2 cloud = 12. La Tabla 2 tiene 13 filas de datos pero 12 modelos distintos (gemma4:latest aparece dos veces, ZS-ES y FS-ES). results/benchmark_results.csv contiene 15 modelos distintos y la Tabla 2 omite cuatro con resultados (qwen3:8b, minimax-m3:cloud, gemma:latest). Nota: la corrida N=120 del 24-08 confirma que se solicitaron 16 modelos pero solo 15 corrieron (gpt-oss:20b no disponible), lo que probablemente explica el origen del '16'.
- **Corrección sugerida:** Fijar un recuento unico y explicito ('15 modelos ejecutados de 16 solicitados') y usarlo de forma consistente en el objetivo 2, §4.2, §5.1 y §5.3.5; o bien completar la lista de §4.2 hasta los 15 modelos realmente presentes en los CSV.

### M55. La referencia [18] quedo corrompida por una sustitucion global ('Kleptotrace/CoNLL-2002/CoNLL-2002', URL 'https://Kleptotrace/CoNLL-2002.org'); el mismo defecto aparece en el abstract en ingles.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 767 (§8, referencia [18]) y linea 39 (abstract en ingles)
- **Verificación:** CONFIRMADO literalmente en ambos puntos. Linea 767: '[18] Kleptotrace/CoNLL-2002 Project, "balanced Kleptotrace/CoNLL-2002/CoNLL-2002 dataset: ..." [Online]. Available: https://Kleptotrace/CoNLL-2002.org, 2024.' — el nombre aparece duplicado y la URL no es un dominio valido (una barra dentro del host). Linea 39: '...on the real financial sanctions dataset balanceado Kleptotrace/CoNLL-2002/CoNLL-2002 (N=15 expert-annotated articles)...' — la palabra espanola 'balanceado' quedo incrustada en el texto ingles junto a la misma duplicacion. Es el residuo evidente de un reemplazo global de cadenas.
- **Corrección sugerida:** Separar [18] en dos entradas distintas (Kleptotrace por un lado; CoNLL-2002 / Tjong Kim Sang, 2002 por otro) con sus URLs reales, y reescribir la frase del abstract en ingles como '...on the real financial sanctions dataset Kleptotrace (N=15 expert-annotated articles)...'.


## 🟡 Gravedad BAJA (34)

### B1. Alucinaciones de deepseek-r1:1.5b: 8.13% en el Hallazgo 2 vs 8.10% en la tabla de la misma sección

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L391 vs L388
- **Verificación:** Ambas citas verificadas literalmente: L388 «| deepseek-r1:1.5b | Local | 1.5B | 31.28% | 35.12% | 28.90% | 8.10% | 38.40 | 25.60 |» y L391 «hallucination rate de 8.13%». Discrepancia menor pero real dentro de la misma sección.
- **Corrección sugerida:** Homologar a 8.10% en L391.

### B2. Rango de tamaño de modelos: 8B–32B en la hipótesis vs 8B–31B en el marco teórico

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L79 y L117
- **Verificación:** Ambas citas verificadas literalmente. Discrepancia menor pero real; el modelo mayor efectivamente evaluado es de 31B.
- **Corrección sugerida:** Unificar en 8B–31B.

### B3. La bibliografía salta de [11] a [13]: no existe la referencia [12]

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L755-757
- **Verificación:** Verificado leyendo el bloque completo de referencias (L735-771): la secuencia es [1]…[11], [13], [14]…[20]. No hay entrada [12]. Ninguna cita del cuerpo invoca [12], por lo que el impacto es formal.
- **Corrección sugerida:** Renumerar correlativamente o restituir la entrada [12] faltante.

### B4. gemma4:12b se declara entre los modelos evaluados pero no aparece en ninguna tabla de resultados

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L268 vs L375-388
- **Verificación:** grep de «12b» en el documento devuelve solo dos líneas: L268 (listado de modelos evaluados) y L837 (Anexo C, modelos descargados). No hay ninguna fila de resultados para gemma4:12b en Tabla 2 ni en §5.3/§5.6. Recordatorio de contexto: el nombre canónico acordado para el artefacto MLX es gemma4:12b-mlx, y el documento no incurre en el nombre eliminado.
- **Corrección sugerida:** Retirarlo del listado de §4.2 o declarar explícitamente que se descargó pero no se incluyó en el benchmark reportado.

### B5. Uso de «billones» como traducción de billions (10^9) en §4.4 y §1.1

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L357 y L65
- **Verificación:** Citas literales verificadas. La aritmética del propio índice lo confirma: 11,37 tok/s ÷ 31 = 0,37, es decir la normalización es por miles de millones de parámetros. En L65 el mercado RegTech de «USD 12.3 billones» corresponde a 12,3 mil millones en el original inglés. En español «billón» = 10^12.
- **Corrección sugerida:** Reemplazar por «miles de millones» en ambos casos (y en L65 también para los USD 87.2).

### B6. §5.3.5 remite a §6.3 por «la meseta de rendimiento documentada», pero §6.3 no documenta ninguna meseta

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** L454 vs L677-679
- **Verificación:** Verificado: §6.3 (L677-679) es un párrafo único sobre el trade-off llama3.2 (3B) vs gemma4:31b en el corpus N=15; no menciona meseta ni compara gemma4:31b-mlx / gemma4:latest / qwen2.5:14b entre sí. La referencia cruzada apunta a contenido inexistente.
- **Corrección sugerida:** Agregar en §6.3 el párrafo sobre la meseta entre 9B y 31B que soporta el resultado de Tukey, o corregir la referencia cruzada.

### B7. Colision de numeracion: dos objetos distintos se citan como 'La Tabla 1' en el mismo documento (§2.5 trabajos relacionados y §3.1 arquitectura de cinco capas).

- **Archivo:** `Informe_Final_Tesina_NER.docx`
- **Ubicación:** §2.5 y §3.1
- **Verificación:** CONFIRMADO. Grep de 'La Tabla [0-9]' sobre Informe_Final_Tesina_NER.docx devuelve tres llamadas: parrafo 70 'La Tabla 1 posiciona este trabajo respecto a investigaciones recientes...', parrafo 82 'La Tabla 1 resume la arquitectura de cinco capas del sistema.' y parrafo 195 'La Tabla 2 presenta los resultados consolidados...'. El docx borrador solo tiene dos (Tabla 1 y Tabla 2, sin la de arquitectura) y el .md vigente igual (lineas 129 y 371). La segunda 'Tabla 1' se anadio al convertir el diagrama ASCII de arquitectura en tabla. Confirmado ademas que el documento no usa campos SEQ/REF (solo 2 instrText, no de numeracion de tablas).
- **Corrección sugerida:** Renumerar la tabla de arquitectura (p. ej. Tabla 2) y desplazar la llamada de resultados a Tabla 3, o adoptar la numeracion completa de la plantilla.

### B8. El bloque de cierre del informe ('Informe Final de Tesina — Magister... Julio 2026') quedo incrustado en mitad del Anexo D, entre D.3 y D.4.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** Anexo D, entre D.3 (Implementacion Tecnica) y D.4 (Catalogo de Guias Tipologicas)
- **Verificación:** CONFIRMADO. En la plantilla el bloque de tres lineas 'Informe Final de Tesina — Magister en Tecnologias de la Informacion (MTI) / Universidad Tecnica Federico Santa Maria — Valparaiso, Chile / Julio 2026' aparece en el parrafo 403, inmediatamente despues del ultimo parrafo de D.3 ('KB RAG (nuevo): Template positivo ... sin suprimir su capacidad de extraccion.') y justo antes del encabezado 'D.4 Catalogo de Guias Tipologicas...'. En los otros dos docx el mismo bloque aparece al final del documento (parrafo 470 de 472 en Informe_Final_Tesina_NER.docx; parrafo 505 de 507 en el borrador). Ademas, en la plantilla el documento continua otras ~85 lineas despues de ese cierre, confirmando que esta fuera de sitio.
- **Corrección sugerida:** Eliminar ese bloque del cuerpo del Anexo D y dejarlo unicamente en el cierre/pie del documento.

### B9. Los Hallazgos 1 y 3 de §5.1 citan cifras de modelos que ya no figuran en la Tabla 5 reducida (gemma4:31b-cloud 66.29% y llama3.2 18.73 Tok/s/B).

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §5.1, Hallazgo 1 y Hallazgo 3
- **Verificación:** CONFIRMADO en cuanto a los hechos. La Tabla 5 de la plantilla contiene solo 4 filas (gemma4:31b, gemma4:latest ZS-ES, gemma4:latest FS-ES, deepseek-r1:1.5b); ni gemma4:31b-cloud ni llama3.2:latest aparecen en ella, pero los Hallazgos 1 y 3 se conservaron intactos citando 66.29% y 18.73 Tok/s/B, cifras que solo estan en la Tabla 20 del Anexo E. En Informe_Final_Tesina_NER.docx y en el borrador la tabla completa de 13 filas acompana a los hallazgos. ATENUANTE que el hallazgo original no menciona: el parrafo introductorio de §5.1 ya remite genericamente al Anexo E ('la tabla completa con todas las configuraciones se documenta en el Anexo E'), de modo que el lector puede localizar las cifras; el defecto es de legibilidad, no una cifra huerfana sin respaldo.
- **Corrección sugerida:** Anadir en los Hallazgos 1 y 3 una remision explicita (p. ej. 'ver Tabla 20, Anexo E'), o reincorporar las dos filas citadas a la Tabla 5.

### B10. Resumen en espanol y abstract en ingles del mismo documento dejaron de ser equivalentes: el resumen perdio '+7.4 puntos de F1', la arquitectura pub/sub, los '16 proveedores', las familias 'Gemma, Llama, DeepSeek' y el sufijo 'M4', y anadio una mencion a N=120 que el abstract no tiene.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** RESUMEN frente a ABSTRACT (primeras paginas)
- **Verificación:** CONFIRMADO elemento por elemento comparando los dos parrafos de la plantilla. El Resumen (parrafo 13) dice 'ejecutados 100% localmente mediante Ollama en hardware Apple Silicon. La validacion experimental se realizo sobre el dataset real Kleptotrace/CoNLL-2002 (N=15) y un corpus sintetico estadisticamente significativo (N=30), con validacion complementaria sobre un corpus real N=120' — sin '+7.4', sin pub/sub/AIMD, sin '16 proveedores', sin las familias de modelos y sin 'M4'. El Abstract (parrafo 16) del mismo documento si contiene todos esos elementos ('Gemma, Llama, DeepSeek families', 'Apple Silicon M4 hardware', 'Factory/Facade layer unifying 16 model providers', '+7.4 F1-point improvement') y no menciona N=120. Verifique tambien que el resumen del .md vigente no menciona N=120.
- **Corrección sugerida:** Reequilibrar ambos: reponer en el resumen el hallazgo +7.4 F1 y 'Apple Silicon M4', o condensar el abstract en la misma medida y anadirle la mencion a N=120.

### B11. Divergencia de contenido tecnico: dos docx listan cuatro proveedores LLM en la capa 3 y anaden anthropic_provider.py y vertexai_provider.py al arbol del Anexo A; el .md vigente solo dibuja tres proveedores y lista solo openai_provider.py.

- **Archivo:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
- **Ubicación:** §3.1 (tabla de capas, capa 3) y Anexo A (arbol de repositorio)
- **Verificación:** CONFIRMADO, y ademas verificado contra el codigo real. Los dos docx dicen '3. Proveedores LLM | Factory / Facade | OllamaProvider, OpenAIProvider, AnthropicProvider, VertexAIProvider' y listan en el Anexo A openai_provider.py, anthropic_provider.py y vertexai_provider.py. El .md vigente (linea 158) y el docx borrador (parrafo 88) dibujan solo 'OllamaProvider | OpenAIProvider | AnthropicProvider' y su Anexo A lista unicamente openai_provider.py (.md linea 798). Los cuatro documentos coinciden en cambio en §3.3, que si nombra VertexAIProvider. Comprobacion decisiva: src/providers/ del repositorio contiene anthropic_provider.py, ollama_provider.py, openai_provider.py, vertexai_provider.py (mas gliner_provider.py y base.py/factory.py). Es decir, los dos docx son la version correcta y el .md/borrador estan desactualizados. Nota adicional no reportada por el agente original: ninguno de los cuatro documentos menciona gliner_provider.py.
- **Corrección sugerida:** Actualizar el .md vigente (§3.1 y Anexo A) y el docx borrador para incluir VertexAIProvider y los archivos anthropic_provider.py y vertexai_provider.py; evaluar de paso si corresponde documentar tambien gliner_provider.py.

### B12. La afirmacion 'El benchmark aun NO se ha ejecutado: bloqueado hasta completar las descargas de modelos' esta obsoleta; el benchmark ya se ejecuto.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Linea 306
- **Verificación:** La cita existe literalmente en la linea 306 y hoy es falsa: hay una corrida en ejecucion (ps muestra src/main.py vivo, PID 75678) escribiendo en results/benchmark_balanced_120_kbrag_9models/benchmark.log desde el 2026-09-03 14:26:50. PERO los detalles del hallazgo estan desactualizados: el directorio results/benchmark_balanced_120_16models/ ya no existe (renombrado a results/DESCARTADA_ragmode_incorrecto_142604/ a las 14:27) y sus 480 filas de gemma4:31b-cloud y minimax-m3:cloud fueron DESCARTADAS por usar rag_mode incorrecto; no deben presentarse como avance valido. Es ademas una seccion de estado fechada dentro de un registro aditivo, por lo que la correccion es agregar una entrada nueva, no editar la linea.
- **Corrección sugerida:** Anadir entrada aditiva: corrida 14:06 en rag_mode entities DESCARTADA (results/DESCARTADA_ragmode_incorrecto_142604/); corrida valida relanzada a las 14:26:50 con --rag-mode kb_combined sobre 9 modelos locales en results/benchmark_balanced_120_kbrag_9models/; los 2 modelos cloud quedan pendientes.

### B13. 'Benchmark de los 11 modelos: NO ejecutado aun (bloqueado por descargas)' y 'ANOVA/Tukey de los 16 modelos: pendiente' estan obsoletos.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Lineas 191-192
- **Verificación:** Cita verificada literalmente en las lineas 191-192. La parte del benchmark esta obsoleta: hay corrida activa desde el 2026-09-03 14:26:50 (results/benchmark_balanced_120_kbrag_9models/, --rag-mode kb_combined, proceso vivo). La segunda linea ('ANOVA/Tukey de los 16 modelos: pendiente') SIGUE SIENDO CORRECTA y no debe tocarse: la corrida activa cubre 9 modelos, no 11 (faltan gemma4:31b-cloud y minimax-m3:cloud), asi que 5+9=14 y el ANOVA de 16 sigue pendiente. Igual que el hallazgo anterior, la referencia a 480 filas ya persistidas es incorrecta: esas filas pertenecen a la corrida descartada por rag_mode.
- **Corrección sugerida:** Actualizar aditivamente solo la linea 191 ('en ejecucion desde 2026-09-03 14:26:50, 9 modelos locales, rag_mode kb_combined'); dejar la linea 192 intacta porque el ANOVA de 16 sigue pendiente.

### B14. La verificacion de paginacion de 24 pp. de cuerpo quedo superada por la entrada de cierre del mismo dia (20 pp. de cuerpo).

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Linea 241 vs linea 285
- **Verificación:** CONFIRMADO literalmente. Linea 241: 'Cuerpo: 24 paginas; anexos desde la pagina 25. Sin paginas en blanco.' Linea 285: '29 paginas totales. Cuerpo: 20 paginas (portada, resumen y capitulos 1-8); anexos desde la 21.' Es la superposicion normal de un registro aditivo, pero la cifra intermedia puede leerse como vigente, sobre todo porque es la que quedo copiada en las tablas de estado de HISTORIAL-CONSOLIDADO.md (lineas 18 y 34).
- **Corrección sugerida:** Anadir en la entrada de las 24 pp. una remision del tipo '(superado por la entrada de cierre del mismo dia: 20 pp. de cuerpo, anexos desde la 21)'.

### B15. Inconsistencia numerica en §9: se dice que el documento paso 'de 40 a 27 paginas' pero el estado final verificado inmediatamente despues declara 29 paginas totales.

- **Archivo:** `HISTORIAL-CONSOLIDADO.md`
- **Ubicación:** Linea 234 vs linea 253
- **Verificación:** CONFIRMADO literalmente. Linea 234: 'las tablas recuperaron su forma y el documento paso de 40 a 27 paginas sin quitar una sola linea de contenido.' Linea 253: '29 paginas totales'. Entre ambas, las lineas 236-249 listan correcciones de maquetacion que anaden paginas (saltos de pagina por capitulo, salto antes del Resumen, margen superior a 3.3 cm), lo que explica plausiblemente el +2, pero el texto no lo dice y ambas cifras se presentan como resultado de la misma intervencion.
- **Corrección sugerida:** Explicitar la secuencia: 40 pp. -> 27 pp. al definir los estilos Table/Compact, y -> 29 pp. tras las correcciones de maquetacion de la tabla de la seccion 'Correcciones aplicadas'.

### B16. Las ganancias del estudio de prompts estan etiquetadas como porcentaje relativo ('% gain') cuando son diferencias en puntos porcentuales.

- **Archivo:** `WORKLOG.md`
- **Ubicación:** Lineas 69-71 (y /WORKLOG.md lineas 165-166)
- **Verificación:** CONFIRMADO literalmente. Linea 69: 'Zero-Shot English (zs-en): 51.41% F1'; linea 70: 'Zero-Shot Spanish (zs-es): 57.43% F1 (+6.02% gain)'; linea 71: 'Few-Shot Spanish (fs-es): 70.18% F1 (+18.77% gain over zero-shot baseline)'. Aritmetica: 57.43-51.41 = 6.02 pp y 70.18-51.41 = 18.77 pp; las ganancias relativas serian +11.7% y +36.5%. La misma redaccion se repite en /WORKLOG.md lineas 165-166. ATENUANTE verificado: la cifra NO se propago a la tesina: grep de '6.02' y '18.77' en doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md y en el texto de ambos DOCX del informe final devuelve cero coincidencias. Nota de politica: /WORKLOG.md es historico e inmodificable (HISTORIAL-CONSOLIDADO.md regla 6), asi que ahi la correccion solo puede ser una nota aditiva externa.
- **Corrección sugerida:** En el WORKLOG del repo, anotar de forma aditiva que se trata de puntos porcentuales (+6.02 pp y +18.77 pp; relativos +11.7% y +36.5%). No editar /WORKLOG.md. Mantener el criterio pp vs % al redactar la tabla de Comparacion de Configuraciones de Prompt en la tesina.

### B17. La referencia 'WORKLOG.md (raiz)' es ambigua entre /WORKLOG.md y repos/ner-llm-entity-benchmark/WORKLOG.md, y este ultimo, que es un registro vigente, no figura en la tabla §1.

- **Archivo:** `HISTORIAL-CONSOLIDADO.md`
- **Ubicación:** Linea 23 y lineas 200-201
- **Verificación:** CONFIRMADO. Linea 23: '| Registro de trabajo historico | WORKLOG.md (raiz) | Historico, no modificar |'. Lineas 200-201, regla 6: 'Los archivos bajo doc/organized/Hito_1..4/, el WORKLOG.md de la raiz y los respaldos .bak_* no se modifican.' La tabla §1 solo lista research/rag/WORKLOG.md como vigente. Verificado que repos/ner-llm-entity-benchmark/WORKLOG.md pertenece al mismo repositorio git (no es submodulo) y esta modificado: git status lo marca ' M repos/ner-llm-entity-benchmark/WORKLOG.md' y git diff --stat da '137 insertions(+)'. Verificado tambien que /WORKLOG.md NO esta modificado, coherente con su caracter historico. La linea 149 menciona 'ambos WORKLOG.md', lo que refuerza la ambiguedad de a que archivos se refiere cada regla.
- **Corrección sugerida:** Desambiguar con rutas completas: declarar /WORKLOG.md como historico e inmodificable en la regla 6, y anadir a la tabla §1 la fila repos/ner-llm-entity-benchmark/WORKLOG.md como registro tecnico vigente (aditivo).

### B18. El identificador `llama3.1:latest (8b)` es inconsistente con `llama3.1:8b` usado en el resto del documento.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 184
- **Verificación:** CONFIRMADO. La linea 184 dice literal '**Proceso de Iteración para llama3.1:latest (8b):**', mientras el encabezado de la seccion (linea 180) y las filas 194-196 usan `llama3.1:8b`, que es el nombre en src/config.py:67 y en RUNS_INDEX.md.
- **Corrección sugerida:** Usar `llama3.1:8b` de forma uniforme.

### B19. La ruta de log documentada (`tail -f results/benchmark.log`) ya no corresponde a las corridas actuales.

- **Archivo:** `BENCHMARKS.md`
- **Ubicación:** Linea 123
- **Verificación:** CONFIRMADO. src/main.py:35 construye `log_file = os.path.join(results_dir, 'benchmark.log')` y results_dir es siempre un subdirectorio con timestamp (src/config.py:98-107), con assert_not_results_root abortando cualquier intento de usar la raiz. El archivo results/benchmark.log que existe hoy esta fechado 27-jul 11:04, residuo de la corrida plana #8.
- **Corrección sugerida:** Cambiar a `tail -f results/<dataset>_<timestamp>/benchmark.log`.

### B20. La descripcion del patron de modelo cloud en la tabla 8.2 (ends in / starts with) no coincide con la implementacion, que usa contencion.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Lineas 83-84 (tabla 8.2, columna 'Name pattern')
- **Verificación:** CONFIRMADO. AGENTS.md:84 dice 'name ends in `-cloud` OR starts with `minimax`'. src/llm_runner.py:61-64 implementa: `key = model_name.lower(); return "-cloud" in key or "minimax" in key`, es decir contencion en cualquier posicion. Con la regla escrita, un nombre como `foo-cloud-bar` seria local segun la doc y cloud segun el codigo.
- **Corrección sugerida:** Reformular como 'el nombre CONTIENE -cloud o CONTIENE minimax', citando textualmente is_cloud_model() (src/llm_runner.py:61-64).

### B21. El delta de sensibilidad de AGENTS.md (+8.42%) no cuadra con las cifras que lo preceden y se expresa como % en vez de puntos porcentuales.

- **Archivo:** `AGENTS.md`
- **Ubicación:** Lineas 31-34 (seccion 4, US17)
- **Verificación:** CONFIRMADO. AGENTS.md:32-34 dice Standard F1 42.41%, Cleaned F1 50.84%, 'Performance Delta: **+8.42%** improvement'. 50.84 - 42.41 = 8.43, no 8.42. Y la diferencia entre dos porcentajes son puntos porcentuales (el aumento relativo seria +19.9%). Es un error aritmetico menor pero real; conviene recalcular desde los datos crudos por si las cifras base tienen mas decimales.
- **Corrección sugerida:** Corregir a '+8.43 puntos porcentuales' o recalcular desde los datos crudos.

### B22. README.md identifica el modelo por defecto `gemma4` como 'Gemma 2 9B'.

- **Archivo:** `README.md`
- **Ubicación:** Linea 19
- **Verificación:** CONFIRMADO como inconsistencia de nomenclatura, aunque de menor gravedad que la reportada. README.md:19 dice literal '4. **Model Pulling:** Retrieves the default model `gemma4` (Gemma 2 9B) locally.' setup.sh:97 ejecuta `ollama pull gemma4` sin tag, que resuelve a gemma4:latest (9.6 GB segun BENCHMARKS.md:80). Llamar 'Gemma 2 9B' a un artefacto de la familia gemma4 (con variantes 12b/31b documentadas en todo el proyecto) es contradictorio con el resto de la documentacion. Bajo gravedad porque no afecta a ningun resultado ni a la reproducibilidad.
- **Corrección sugerida:** Indicar el tag completo (`gemma4:latest`) y eliminar la equivalencia con 'Gemma 2 9B'.

### B23. El nombre del corpus aparece con 'CoNLL-2002' duplicado en el README.

- **Archivo:** `README.md`
- **Ubicación:** Linea 32
- **Verificación:** CONFIRMADO literalmente. README.md:32 dice 'Evaluate a model sweep on the primary balanced Kleptotrace/CoNLL-2002/CoNLL-2002 dataset:'. Es un artefacto de sustitucion automatica; AGENTS.md:28 y 31 usan la forma correcta 'Kleptotrace/CoNLL-2002'.
- **Corrección sugerida:** Dejar 'Kleptotrace/CoNLL-2002'.

### B24. RUNS_INDEX usa exclusivamente 'ablacion' como termino principal en espanol, contra la decision terminologica del proyecto.

- **Archivo:** `RUNS_INDEX.md`
- **Ubicación:** Lineas 26, 40, 57, 60, 78, 89, 105, 162
- **Verificación:** CONFIRMADO como uso, aunque es un item de estilo y no un error factual. Verificado: 'ablation' en las lineas 25-26 (leyenda de modos y combinaciones nunca ejecutadas), 40-41 (leyenda), 57 (#9 'Ablación de prompts sobre N=15'), 60 (#12 'Ablación sobre corpus real'), 78 (encabezado de la matriz), 89, 105 y 162 ('Ablación de prompts sobre N=30'). No aparece 'Comparacion de Configuraciones de Prompt' en ninguna parte del archivo. Aclaracion: el flag CLI `--ablation` y el campo `ablation` de BenchmarkConfig son identificadores de codigo y no deben tocarse; el impacto es menor por tratarse de un indice interno y no de un entregable de hito.
- **Corrección sugerida:** Introducir 'Comparacion de Configuraciones de Prompt' como termino principal en la leyenda de la seccion 2 y en la seccion 3, glosando '(estudio de ablacion, diseno factorial 2x2)' en la primera aparicion. No modificar el flag CLI.

### B25. El nombre de modelo proscrito gemma4-12b-mlx-q8-64k sobrevive en copias de respaldo sin versionar y en un log.

- **Archivo:** `config.py.bak_pre20260903, benchmark_final_run_v2.log)`
- **Ubicación:** BENCHMARKS.md.bak lineas 38, 79, 170; run_benchmark.sh.bak linea 25; src/config.py.bak linea 17
- **Verificación:** CONFIRMADO con un matiz de forma. Los archivos vigentes (BENCHMARKS.md, AGENTS.md, README.md, TODO.md, RUNS_INDEX.md, run_benchmark.sh, src/config.py) ya NO contienen el nombre. Sobrevive en: BENCHMARKS.md.bak_pre20260903 lineas 38 ('gemma4-12b-mlx-q8-64k:latest'), 79 (fila de `ollama list`) y 170 (fila de resultados con F1 0.1206 / P 0.9019 / R 0.1528); run_benchmark.sh.bak_pre20260903 linea 25; y benchmark_final_run_v2.log con 806 ocurrencias. Matiz: en src/config.py.bak_pre20260903 la linea 17 usa la variante con dos puntos `gemma4:12b-mlx-q8-64k`, no el guion, por lo que un grep del nombre exacto no la encuentra. `git status` confirma que los tres .bak estan sin versionar (??).
- **Corrección sugerida:** Mover los archivos *.bak_pre20260903 y benchmark_final_run_v2.log a un directorio archive/ excluido de busquedas e indexacion (o eliminarlos) tras confirmar que el contenido vigente es correcto. Buscar ambas grafias: 'gemma4-12b-mlx-q8-64k' y 'gemma4:12b-mlx-q8-64k'.

### B26. El Hallazgo 2 cita 8.13% de alucinaciones para deepseek-r1:1.5b mientras la Tabla 2 reporta 8.10%.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 391 (Hallazgo 2) vs linea 388 (Tabla 2)
- **Verificación:** CONFIRMADA la discrepancia interna (8.13% en linea 391 vs 8.10% en linea 388), pero REFUTADA la explicacion del hallazgo: el valor correcto es 8.13% y esta perfectamente respaldado. benchmark_console.log (linea 1457) da deepseek-r1:1.5b hallucination_rate = 0.081287, es decir 8.13%. El erroneo es el 8.10% de la tabla, no el 8.13% del Hallazgo. Los valores del CSV que cita el agente (0.013462 / 0.087379) pertenecen a otra corrida (rag-entities del 27-07) y no son la referencia aplicable. Bajo la gravedad respecto de lo reportado: es un typo de una centesima, no una cifra sin respaldo.
- **Corrección sugerida:** Corregir la Tabla 2 (linea 388) de 8.10% a 8.13% para alinearla con el Hallazgo 2 y con benchmark_console.log.

### B27. La numeracion IEEE de la bibliografia salta del [11] al [13]: no existe entrada [12]. La lista llega a [20] pero contiene solo 19 entradas.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** lineas 755-757 (§8)
- **Verificación:** CONFIRMADO. Enumeracion completa de §8 verificada: [1] Lewis, [2] Devlin, [3] Wu, [4] Vaswani, [5] Bourne, [6] Gao, [7] Garcia & Lopez, [8] Brown, [9] Chang, [10] Smith, [11] Ahia, [13] Wei, [14] Zhao, [15] Min, [16] Schwartz, [17] Lafferty, [18] Kleptotrace, [19] OpenSanctions, [20] Dettmers. Un `grep -c '^\[[0-9]*\]'` sobre el documento devuelve 19. No hay entrada [12] y la ultima es [20].
- **Corrección sugerida:** Renumerar correlativamente de [1] a [19] actualizando las citas en texto, o restituir la referencia [12] omitida.

### B28. La cita en texto dice 'Borne, 2024' pero la entrada bibliografica [5] es 'K. Bourne'; ademas se usa formato autor-ano en un documento que declara formato IEEE numerado.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 255 (§4.1.2 c)
- **Verificación:** CONFIRMADO. Linea 255: 'practica ampliamente aceptada en la literatura [Brown et al., 2020; Borne, 2024].' Linea 743 (§8): '[5] K. Bourne, Unlocking Data with Generative AI and RAG. O'Reilly Media, 2024.' Apellido mal escrito ('Borne' por 'Bourne'). El documento usa citas autor-ano en varios puntos (lineas 115, 117, 255, 675) pese a que §8 esta numerada en formato IEEE.
- **Corrección sugerida:** Corregir a 'Bourne' y convertir la cita a formato IEEE numerado ([8], [5]); revisar de paso las demas citas autor-ano del documento.

### B29. Versiones de software desactualizadas respecto al entorno real (Python 3.13 / Streamlit 1.58 declarados, frente a 3.14.7 / 1.60.0 instalados).

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 362 (§4.5) y linea 835 (Anexo C)
- **Verificación:** CONFIRMADO, y no es un artefacto de actualizacion posterior. `./venv/bin/python -V` devuelve Python 3.14.7; venv/pyvenv.cfg declara version=3.14.7; el site-packages esta en venv/lib/python3.14/. El venv anterior (venv_corrupt_old, fechado 1-jul-2026, la epoca de las corridas N=15/N=30) tambien usa lib/python3.14, de modo que la version 3.13 declarada no fue correcta ni siquiera historicamente. Versiones instaladas verificadas: streamlit 1.60.0, scikit-learn 1.9.0, statsmodels 0.14.6, pandas 3.0.5. Las citas existen literales en la linea 362 ('Python 3.13, Ollama 0.6+, scikit-learn 1.9, statsmodels 0.14, pandas 3.0, Streamlit 1.58') y en el Anexo C ('Python | 3.13.0').
- **Corrección sugerida:** Actualizar a 'Python 3.14, scikit-learn 1.9, statsmodels 0.14, pandas 3.0, Streamlit 1.60' en §4.5 y a '3.14.7' en el Anexo C.

### B30. Falso amigo en la definicion del indice Tok/s/B: 'billones de parametros' deberia ser 'miles de millones' (10^9).

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 357 (§4.4, tabla de metricas)
- **Verificación:** CONFIRMADO. Cita literal en linea 357: '| **Indice Tok/s/B** | Tokens por segundo normalizados por billones de parametros |'. La 'B' del indice corresponde a 'billion' en ingles = 10^9 = mil millones en espanol; 'billones' en espanol es 10^12. Con la definicion escrita, el 0.81 de gemma4:31b estaria tres ordenes de magnitud fuera de escala. Es el mismo falso amigo que en la linea 65 (mercado RegTech).
- **Corrección sugerida:** Cambiar a 'Tokens por segundo normalizados por cada mil millones (10^9) de parametros'.

### B31. Una linea en blanco parte la Tabla 2 en dos tablas Markdown independientes, dejando huerfanas las filas de nemotron-mini:4b y deepseek-r1:1.5b.

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 386 (§5.1, Tabla 2)
- **Verificación:** CONFIRMADO por inspeccion carácter a carácter. Volcado de las lineas 384-389: la 385 es la fila nuextract, la 386 esta VACIA, y las 387-388 son nemotron-mini y deepseek-r1. En Markdown una linea en blanco termina la tabla, por lo que las dos ultimas filas se renderizan como una tabla separada sin encabezado al exportar a DOCX/PDF.
- **Corrección sugerida:** Eliminar la linea en blanco 386 para restituir una unica tabla continua.

### B32. Discrepancias de latencia y de indice Tok/s/B entre las tablas de §5.1 y §5.2 para las mismas condiciones (22.70 vs 22.67; 44.50 vs 44.47; 6.30 vs 6.32).

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** lineas 378-379 (§5.1) vs lineas 399 y 401 (§5.2)
- **Verificación:** CONFIRMADO literalmente. Linea 378: gemma4:latest (ZS-ES) latencia 22.70, Tok/s/B 6.30. Linea 399: Zero-shot Espanol latencia 22.67. Linea 379: gemma4:latest (FS-ES) latencia 44.50, Tok/s/B 6.32. Linea 401: Few-shot Espanol latencia 44.47. Los valores de §5.2 son los exactos (benchmark_console.log da 68.004785 y 133.399894, que divididos por batch_size=3 dan 22.668 y 44.467); los de §5.1 estan redondeados de forma inconsistente. El Tok/s/B difiere (6.30 vs 6.32) entre dos filas del mismo modelo de 9B, lo que es imposible si comparten parametros. Discrepancia trivial, sin efecto sobre ninguna conclusion.
- **Corrección sugerida:** Unificar ambas tablas a 22.67 / 44.47 y usar un unico valor de Tok/s/B para gemma4:latest en las dos filas.

### B33. El rango de tamano de modelo declarado en la hipotesis (8B-32B) no coincide con el de §2.2 (8B-31B).

- **Archivo:** `2026-07-04_Borrador-Informe-Final-Tesina.md`
- **Ubicación:** linea 79 (§1.3) vs linea 117 (§2.2)
- **Verificación:** CONFIRMADO. Linea 79: 'modelos de lenguaje de codigo abierto de escala media-grande (8B-32B parametros) ejecutados localmente'. Linea 117: 'modelos de codigo abierto de escala media-grande (8B-31B parametros) ejecutados localmente'. Misma formula, dos limites superiores distintos. El rango realmente evaluado segun los CSV va de 1.5B (deepseek-r1) a 31B (gemma4:31b-mlx), por lo que ninguno de los dos describe el conjunto completo, aunque la hipotesis se restringe deliberadamente al subconjunto media-grande. Inconsistencia cosmetica.
- **Corrección sugerida:** Unificar en '8B-31B' en ambos puntos y aclarar en §4.2 que el barrido completo abarca de 1,5B a 31B, siendo el rango 8B-31B el subconjunto que sustenta la hipotesis.

### B34. El nombre de modelo eliminado del proyecto por sufijo q8 falso ('gemma4-12b-mlx-q8-64k:latest') sigue presente en los datos crudos de dos corridas.

- **Archivo:** `benchmark_results.csv`
- **Ubicación:** columna 'model' (tambien en results/benchmark_balanced_120_20260824_173036/benchmark_results.csv)
- **Verificación:** CONFIRMADO. Conteo propio sobre results/benchmark_results.csv: 'gemma4-12b-mlx-q8-64k:latest_baseline' 15 filas y 'gemma4-12b-mlx-q8-64k:latest_rag_enhanced' 15 filas (30 en total). En results/benchmark_balanced_120_20260824_173036/benchmark_results.csv el mismo artefacto aparece con baseline F1=0.2844 y rag_enhanced F1=0.1827 sobre 120 registros cada uno (240 filas). Dado que el nombre canonico acordado es gemma4:12b-mlx y que ninguna mencion al nombre viejo debe sobrevivir en la entrega, cualquier tabla o anexo regenerado desde esos CSV reintroduciria el nombre eliminado. El propio hallazgo recomienda correctamente NO tocar los CSV historicos. Verificado tambien que ninguna tabla del borrador contiene hoy ese nombre.
- **Corrección sugerida:** No modificar los CSV historicos. Anadir un mapeo de renombrado ('gemma4-12b-mlx-q8-64k:latest' -> 'gemma4:12b-mlx') en cualquier script que genere tablas desde esa columna, y dejar constancia del renombrado en results/RUNS_INDEX.md §6 (seccion aditiva de notas y correcciones).


## ⚪ Descartados por el verificador (17)

Reportados por el auditor pero NO confirmados. Se listan por transparencia.

- `2026-07-04_Borrador-Informe-Final-Tesina.md` — §3.3 declara AnthropicProvider y VertexAIProvider pero el Anexo A no los incluye: se afirma que esos módulos no existen → *REFUTADO en su premisa: los módulos SÍ existen. ls de repos/ner-llm-entity-benchmark/src/providers/ devuelve anthropic_provider.py (6.572 B), vertexai_provider.py, gliner_provider.py, además de base.py, factory.py, ollama_provider.py y openai_provider.py. §3.3 es correcto; el árbol del Anexo A simplemente es abreviado y omite tres archivos. No hay contradicción de fondo, a lo sumo una omisión cosmética opcional de completar.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — Anexo C indica ~29 minutos para el benchmark N=30 con 2 modelos, incompatible con latencias de 160 s/artículo → *REFUTADO con evidencia primaria: benchmark_augmented_30.log arranca a las 17:27:56 y termina a las 17:57:43 → 29,8 minutos reales, exactamente lo que dice el Anexo C. El cálculo del agente anterior asume ejecución de artículos uno a uno, pero el log muestra el controlador AIMD operando con 4-6 workers concurrentes ([AIMD] current_workers 4 y 6), de modo que 4.807 s de latencia agregada por modelo caben en ~22 min de reloj. La latencia de 160,23 s es por artículo, no acumulativa. El único matiz menor es la palabra «(serial)», que aplica a la secuencia de modelos, no a los artículos.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — Caída de Recall 62.8% → 21.6% del diagrama §5.6.1 no aparece en ninguna tabla del informe → *REFUTADO: las cifras son reales y trazables al documento que la propia §5.6.1 cita en L495. En research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md, §7.1, el protocolo controlado de N=5 con llama3.2 reporta Recall baseline 0.6286 (=62.9%) y Recall con RAG de diccionario 0.2158 (=21.6%). No procede sustituirlas por las del mini-benchmark KB RAG de §5.6.5, que corresponde a otra condición (KB RAG, no dict-RAG) y otra fecha. Nota lateral para el autor: el diagrama del propio documento de investigación dice «14.9%» en vez de 21.6%, inconsistencia que está en el archivo de research, no en la tesina.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — §5.5 asigna el mismo costo por artículo (USD 0.052) a modelos con throughput y latencia muy distintos → *Las citas existen, pero no constituyen una contradicción: la nota inmediatamente siguiente (L476) define el 0,052 USD como una estimación única del sistema soberano local («El costo por artículo en el sistema soberano local se estima en USD 0.052»), no como un cálculo por modelo. Repetir el mismo valor en las tres filas es coherente con esa definición y no contradice el análisis de latencia de §6.3, que trata tiempo y no dinero. Es a lo sumo una imprecisión de presentación.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — En §5.2 la fila Zero-shot Inglés tiene F1 (62.41%) casi 10 puntos por debajo de precisión y recall → *Ubicación mal citada por el agente anterior (indicó L379, que es la fila FS-ES de la Tabla 2; la fila real está en L398). Y el fenómeno no es un error: §3.4 (L199) documenta explícitamente «Métricas por registro: Precisión, Recall, F1-Score calculados por artículo y promediados», y bajo macro-promedio por registro el F1 medio puede quedar por debajo de la precisión media y del recall medio (basta con artículos donde P=1 y R=0, cuyo F1 individual es 0). No hay contradicción demostrada ni evidencia de cálculo erróneo.*
- `WORKLOG.md` — El plan del WORKLOG (completar 11 modelos con baseline+KB RAG y combinar con la corrida del 2026-09-01 para un ANOVA de 16 modelos x 2 modos) seria inejecutable porque la corrida lanzada el 2026-09-03 14:06 usaba la condicion legacy rag_enhanced (rag_mode entities) en lugar de kb_combined. → *REFUTADO por el estado actual del disco. El directorio citado como evidencia, results/benchmark_balanced_120_16models/, YA NO EXISTE: fue renombrado a results/DESCARTADA_ragmode_incorrecto_142604/ el 2026-09-03 a las 14:27, es decir el propio nombre del directorio documenta que la corrida se descarto justamente por el rag_mode incorrecto. A las 14:26:50 se relanzo con el modo correcto: results/benchmark_balanced_120_kbrag_9models/benchmark.log registra literalmente "[KBRAGManager] Initialized | mode='kb_combined'" y "[RAG] Using Knowledge Base mode: 'kb_combined'", y el proceso sigue vivo (ps: PID 75678, 'src/main.py --data-file data/benchmark_balanced_120.json --rag-study --rag-mode kb_combined --results-dir results/benchmark_balanced_120_kbrag_9models'). Por lo tanto el plan de las lineas 232/313 SI es combinable con results/benchmark_balanced_120_20260901_140421/ (run_config.json: rag_mode 'kb_combined'). Salvedad real pero distinta a la reportada: la corrida activa cubre 9 modelos locales (gemma4:12b-mlx, gpt-oss:20b, qwen3:8b, mistral-nemo:latest, nuextract:latest, llama3.1:8b, nemotron-mini:4b, deepseek-r1:1.5b), no 11: los dos modelos cloud (gemma4:31b-cloud, minimax-m3:cloud) quedaron solo en la corrida descartada, de modo que 5+9=14 y no 16. Eso si conviene registrarlo.*
- `HISTORIAL-CONSOLIDADO.md` — Contradiccion interna: la tarea 4 del cronograma (§7) figura como pendiente aunque el propio documento la declara RESUELTA en §5 punto 5. → *REFUTADO por dos vias. (1) La tabla de §7 no tiene columna de estado: sus columnas son '# | Tarea | Entrada requerida | Criterio de termino | Riesgo' (linea 176). Ninguna celda declara la tarea 4 'pendiente'; es una lectura inferida. (2) Mas importante, el criterio de termino de la propia tarea 4 ('Sin ocurrencias de q8 para gemma4-12b-mlx en tesina ni en codigo/documentacion') NO se cumple: grep -rn sobre el proyecto SI arroja ocurrencias vivas del nombre eliminado, en rag.patch linea 24 ('gemma4:12b-mlx-q8-64k', archivo versionado en git, confirmado con git ls-files) y en repos/ner-llm-entity-benchmark/results/run_config.json ('12b-mlx-q8-64k:latest'), ademas de results/benchmark_results.csv, results/statistical_report.md, results/benchmark_summary.json, results/detailed_results.json, results/.checkpoint.json y results/benchmark_balanced_120_20260824_173036/*. Marcar la tarea 4 como COMPLETADA seria introducir un error, no corregir uno.*
- `WORKLOG.md` — El pendiente 'Correccion transversal de la nomenclatura q8' ya estaria resuelto y deberia cerrarse. → *REFUTADO. La cita de la linea 249 existe, pero la premisa del hallazgo ('no queda ninguna referencia al nombre de modelo eliminado ... ni en ningun .md del proyecto') es falsa en su alcance completo: quedan ocurrencias vivas en rag.patch linea 24 (archivo versionado en git) y en repos/ner-llm-entity-benchmark/results/run_config.json, ademas de varios artefactos bajo results/. Es cierto que BENCHMARKS.md (lineas 54 y 78), src/config.py (linea 68) y run_benchmark.sh (linea 25) ya usan gemma4:12b-mlx, pero cerrar el pendiente como RESUELTO ocultaria el residuo. Ante la duda, se descarta: es preferible dejar el pendiente abierto que cerrarlo antes de tiempo.*
- `WORKLOG.md` — El pendiente 2 del repo (aplicar la correccion q8 en AGENTS.md §8.6, BENCHMARKS.md, README.md, results/run_config.json, src/config.py) ya estaria resuelto. → *REFUTADO de forma directa por la propia lista citada. El texto de la linea 311 enumera explicitamente results/run_config.json entre los artefactos a corregir, y ese archivo TODAVIA contiene '12b-mlx-q8-64k:latest' (verificado con grep sobre repos/ner-llm-entity-benchmark/results/run_config.json). Es cierto que src/config.py:68 y run_benchmark.sh:25 ya declaran gemma4:12b-mlx y que BENCHMARKS.md:54,78 tambien, pero el punto 2 no esta completo. Ademas rag.patch:24 conserva el nombre viejo. Cerrar el punto 2 como resuelto seria factualmente incorrecto.*
- `WORKLOG.md` — El 'Hallazgo 3' presenta la autorizacion de los modelos cloud como una excepcion nueva del 2026-09-03, pese a que el mismo archivo documenta su uso operativo desde el 2026-06-30. → *Ambas citas existen (linea 260 en el Hallazgo 3, y linea 156 dentro de la seccion '2026-06-30: AIMD Adaptive Worker Concurrency Controller' que empieza en la linea 148), y es cierto que el uso operativo de gemma4:31b-cloud y minimax-m3:cloud precede a septiembre (results/RUNS_INDEX.md fila #1 registra minimax-m3:cloud el 2026-06-30). Pero el texto del Hallazgo 3 NO afirma que sea la primera vez que se usan: dice que el autor autorizo explicitamente su uso como linea base y que ESO se documento como excepcion acotada en AGENTS.md §2. Documentar formalmente el 2026-09-03 una practica preexistente no contradice nada de lo escrito; la acusacion de narrativa enganosa es una sobrelectura. Ante la duda, se descarta.*
- `WORKLOG.md` — La entrada nueva usa 'estudio de ablacion' como termino principal sin glosarlo con 'Comparacion de Configuraciones de Prompt', el termino adoptado por el proyecto. → *Las citas existen (linea 344-345: 'registre si la corrida fue un estudio de ablacion'; linea 345-346: 'las corridas de ablacion eran indistinguibles de un baseline'), pero el uso es tecnicamente correcto y de bajo riesgo: la prosa describe la semantica de un campo de codigo que se llama literalmente 'ablation' en BenchmarkConfig y del flag --ablation, de modo que 'estudio de ablacion' es aqui el termino natural. La convencion de nomenclatura acordada aplica a la prosa de la TESINA, no a un registro tecnico de cambios de codigo; verificado que estas lineas no se citan en el informe (grep de '6.02', '18.77' y del texto de la entrada no aparece en el borrador ni en los DOCX). Ante la duda, se descarta para no generar ruido de edicion sobre un WORKLOG tecnico.*
- `BENCHMARKS.md` — Se afirma que el estudio RAG se hizo sobre un corpus de 20 registros, N que segun RUNS_INDEX no fue ejecutado. → *REFUTADO. La cita existe (linea 188, 'En nuestro corpus de prueba de 20 records'), pero SI existe un corpus de exactamente 20 registros: data/sample_sanctions.json tiene 20 lineas JSONL y es el valor por defecto de --data-file en src/main.py:704, ademas de que --generate-sample-data se describe como 'Generate 20-record sample dataset'. Las iteraciones descritas en las lineas 184-188 (llama3.1:8b, latencias de 1.02 s y 15.21 s) tienen pinta de prototipos tempranos sobre ese sample, no de la corrida #8. RUNS_INDEX.md solo cataloga corridas con evidencia superviviente, por lo que su silencio no prueba que el N=20 sea falso. Corregir el N a 15 podria introducir un dato erroneo.*
- `AGENTS.md` — El guardrail 'Pub/Sub Required' de AGENTS.md contradiria al codigo, que no usaria Pub/Sub. → *REFUTADO. La cita existe en AGENTS.md:16, pero la premisa del hallazgo es falsa: el codigo SI implementa Pub/Sub. src/pub_sub.py define AbstractTaskQueue con publish/subscribe/acknowledge (lineas 38-52) y dos implementaciones, InMemoryTaskQueue (55) y RedisTaskQueue (86); src/main.py publica y consume tareas a traves de esa cola en sus cuatro rutas. El guardrail prohibe 'synchronous sequential batching' — que efectivamente no se hace — y menciona Redis/Celery/ZeroMQ como ejemplos ('e.g.'), no como requisito exclusivo. Que el broker por defecto sea en memoria no viola el guardrail tal como esta redactado. A lo sumo cabria una nota aclaratoria, no una correccion de inconsistencia.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — Ninguna fila de la Tabla 2 (§5.1, N=15) se reproduce desde results/benchmark_results.csv; las cifras solo existirian en el doc de Hito_4 'sin CSV de respaldo'. → *REFUTADO EN SU PREMISA. El agente comparo contra la corrida equivocada. results/benchmark_results.csv NO es la corrida de la Tabla 2: segun results/RUNS_INDEX.md (fila #8) es la corrida `klepto_N15__rag-entities__zs-en__20260727_1104` (estudio RAG legacy, 15 modelos x 2 condiciones). La fuente real de la Tabla 2 es repos/ner-llm-entity-benchmark/benchmark_console.log (corrida del 2026-07-01 06:37, RUNS_INDEX #2), cuyo bloque FINAL BENCHMARK PERFORMANCE RESULTS (linea 1454 y ss.) contiene: llama3.1:8b f1=0.596058 p=0.530372 r=0.735783 h=0.036153 -> tesina 59.61/53.04/73.58/3.62 (COINCIDENCIA EXACTA en las 4 metricas); gemma4:31b r=0.867777 h=0.001550 -> tesina 86.78%/0.15% (exacto); llama3.2 f1=0.612932 -> tesina 61.29% (exacto); nemotron-mini r=0.350797 -> tesina 35.08% (exacto); deepseek-r1 h=0.081287 -> Hallazgo 2 8.13% (exacto). Es decir, SI existe respaldo y varias filas reproducen al centesimo. La correccion sugerida ('regenerar la Tabla 2 desde results/benchmark_results.csv') seria ACTIVAMENTE ERRONEA: mezclaria una corrida de estudio RAG con una corrida baseline. Queda un residuo menor y distinto del reportado: las filas de mistral-nemo (57.12 vs 0.541209), nuextract (54.20/46.10/68.20 vs 0.548173/0.497117/0.431924), qwen2.5:14b (58.74/51.12 vs 0.612060/0.582271), deepseek-r1 (31.28 vs 0.411969) y las columnas F1/Precision de gemma4:31b (67.83/57.29 vs 0.687572/0.583935) no reproducen desde ninguna fuente superviviente, y la tabla no cita su corrida de origen.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — El modelo `gemini-3.1-flash-lite` (Tabla 2 y §4.2) no existe en ningun benchmark_results.csv del repositorio; deberia eliminarse de la tabla y de §4.2. → *REFUTADO. La corrida existe y las cifras reproducen EXACTAMENTE. repos/ner-llm-entity-benchmark/benchmark_gemini_active.log (2026-07-01 12:51, catalogada como corrida #4 en results/RUNS_INDEX.md) contiene: `gemini-3.1-flash-lite  0.654714  0.540897  0.846883  0.0  1.694567` -> tesina 65.47% / 54.10% / 84.69% / 0.00% / 1.69. Coincidencia perfecta en las cinco metricas. Lo unico cierto es que no sobrevive el CSV por registro (la corrida escribio en results/ raiz y fue sobrescrita), igual que la corrida N=30 titular. Eliminar el modelo destruiria un resultado real y documentado. La subafirmacion sobre `gemma4:12b` (linea 268) tambien es dudosa: el CSV contiene el artefacto `gemma4-12b-mlx-q8-64k:latest` (renombrado a gemma4:12b-mlx) con 30 filas en results/benchmark_results.csv y 240 en la corrida N=120 del 24-08.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — Las cuatro filas del diseno factorial 2x2 (§5.2) no se reproducen desde results/kleptotrace_20260727_110454/benchmark_results.csv; la ganancia por localizacion al espanol seria +1.17 pp y no +7.40 pp, lo que invalidaria el Hallazgo 4, §4.3.4, §6.2 y la conclusion 2. → *REFUTADO CATEGORICAMENTE. El agente comparo contra otra corrida de ablacion. Existen DOS ablaciones N=15 sobre gemma4:latest: la del 2026-07-27 (results/kleptotrace_20260727_110454/, RUNS_INDEX #9) y la del 2026-07-01 (benchmark_console.log, lineas 1848-1855). La tesina usa la segunda, y coincide al centesimo en F1, precision, recall y hallucination en las CUATRO condiciones: zs-en 0.624150/0.722659/0.724275/0.000000 -> 62.41/72.26/72.42/0.00; zs-es 0.698142/0.625922/0.827018/0.001961 -> 69.81/62.59/82.70/0.19; fs-en 0.673777/0.668302/0.800688/0.000000 -> 67.38/66.83/80.07/0.00; fs-es 0.697577/0.616719/0.845507/0.018030 -> 69.76/61.67/84.55/1.80. Incluso las latencias coinciden dividiendo por el batch_size=3: 71.257/3=23.75, 68.005/3=22.67, 196.603/3=65.53, 133.400/3=44.47. La ganancia +7.40 pp (62.41 -> 69.81) es EXACTA para esa corrida. El Hallazgo 4, §4.3.4, §6.2 y la conclusion 2 quedan intactos.*
- `2026-07-04_Borrador-Informe-Final-Tesina.md` — El costo de USD 0.052 por articulo se asigna identico a tres modelos con latencias muy distintas, y ni ese valor ni los USD 8.75 de revision manual tendrian fuente o formula de calculo en el repositorio. → *REFUTADO EN SU AFIRMACION CENTRAL. Si existe una formula de costeo documentada en el repositorio: THESIS_PROJECT_ANALYSIS_REPORT.md, seccion 'Cost Comparison' (lineas 871-890), desglosa Local (Apple M4): hardware amortizado ~$0.05/articulo a 1 ano + electricidad ~$0.002 = ~$0.052; y Manual Analysis: analista de compliance $35/hora x ~15 min/articulo = ~$8.75. La misma cifra aparece replicada en EXECUTIVE_SUMMARY.md (linea 114), DEFENSE_CHECKLIST.md (linea 194) y REPORTS_INDEX.md (linea 247). La observacion sobre el costo identico entre modelos tampoco constituye error: la formula es de amortizacion de hardware por articulo, deliberadamente independiente del modelo. La reduccion del 99.4% es aritmeticamente correcta (1 - 0.052/8.75). Queda solo una observacion menor de estilo, no una inconsistencia: el borrador no cita en §5.5 el documento donde vive la formula, y la afirmacion '60-80% de reduccion' del resumen ejecutivo convive con el '99.4%' de la conclusion 4.*