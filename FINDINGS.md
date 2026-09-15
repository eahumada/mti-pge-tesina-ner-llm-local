# FINDINGS — Hallazgos de la Revisión Final

> Registro de los descubrimientos técnicos y documentales de la revisión final del proyecto.
> Cada hallazgo incluye la **evidencia** que lo sustenta y su **impacto**, para que un tercero pueda
> reconstruir el razonamiento sin repetir el trabajo.
>
> **Fecha:** 2026-09-03 · **Documentos relacionados:** [`LEARNING.md`](./LEARNING.md),
> [`AUDITORIA_CONSISTENCIA_20260903.md`](./AUDITORIA_CONSISTENCIA_20260903.md),
> [`TODO-INFORME-FINAL.md`](./TODO-INFORME-FINAL.md), `research/rag/WORKLOG.md`

---

## 1. Integridad de los datos experimentales

### F1. Los datos por registro del corpus N=30 se perdieron por sobrescritura
**Severidad: crítica.** La corrida del 2026-07-01 escribió sus resultados en la **raíz** de `results/`
en lugar de un subdirectorio con timestamp. La corrida del 2026-07-27 los sobrescribió.

- **Evidencia:** ningún CSV del proyecto contiene 30 `record_id` (todos tienen 15 o 120). El log de julio
  dice literalmente *"exported all results to results/ output directory"*, y
  `results/benchmark_results.csv` está fechado el 27-jul.
- **Qué sobrevive:** las métricas **agregadas** en `benchmark_augmented_30.log` (raíz del repo), que
  coinciden exactamente con la tabla de la tesina: `gemma4:31b` F1=0.790303, precisión=0.733413,
  recall=0.891111, alucinación=0.0, latencia=160.230099.
- **Impacto:** el 79.03% es citable y trazable, pero **no re-analizable**: no se puede recalcular ANOVA,
  Tukey ni el análisis de sensibilidad, ni inspeccionar casos individuales.
- **Causa raíz:** `BenchmarkConfig.__post_init__` solo genera subdirectorio si `results_dir == 'results'`;
  cualquier otra vía escribe en la raíz.
- **Estado:** mitigado con un guardarraíl que aborta si `results_dir` resuelve a la raíz (15 tests).

### F2. El flag `--resume` era inoperante
**Severidad: alta.** Una corrida interrumpida **reiniciaba desde cero en silencio**.

- **Cadena del fallo:** `main.py` nunca pasaba `results_dir` → quedaba en el default `'results'` →
  `__post_init__` generaba un directorio nuevo con timestamp *en cada ejecución*, junto con su
  `checkpoint_file` → `--resume` buscaba el checkpoint en ese directorio recién creado y vacío.
- **Impacto:** en una corrida de 10+ horas, cualquier interrupción habría costado todo el trabajo.
- **Estado:** corregido añadiendo el flag `--results-dir` (9 líneas, 0 borrados). Verificado que el
  comportamiento por defecto queda idéntico.

### F3. Incompatibilidad de modo RAG entre corridas
**Severidad: alta.** Detectado **antes** de consumir 10 horas de cómputo.

| Corrida | `rag_mode` | Grupo generado |
|:---|:---|:---|
| Referencia 2026-09-01 | `kb_combined` | `gemma4:latest_kb_rag` |
| Lanzamiento inicial | `entities` (default) | `gemma4:31b-cloud_rag_enhanced` |

- **Impacto:** fusionar ambas en un solo ANOVA habría comparado **implementaciones de RAG distintas**,
  invalidando §5.3.5 sin que nada lo delatara en el reporte final.
- **Estado:** corrida descartada (archivada, no borrada) y relanzada con `--rag-mode kb_combined`.

---

## 2. Nomenclatura de modelos

### F4. El sufijo `q8` de `gemma4-12b-mlx-q8-64k` era falso
**Severidad: alta (integridad académica).** El modelo es **4-bit**, no 8-bit.

Evidencia obtenida del registro de Ollama (manifiestos y blobs, sin descargar pesos), sobre un blob de
configuración **exclusivo de ese tag**:

| Evidencia | Valor |
|:---|:---|
| `producer` | `modelopt 0.45.0` (NVIDIA TensorRT Model Optimizer) |
| `quant_algo` | `MIXED_PRECISION` |
| Capas cuantizadas | 328× `NVFP4` + 1× `W4A16_NVFP4` (**4 bits**), `group_size` 16 |
| KV cache | `FP8` |
| Tamaño real | 7.71 GB |
| Bits/peso derivados | ≈ **5.14** (7.71 GB ÷ 12B parámetros) |
| Tamaño de un q8 real de 12B | **12.84 GB** (`gemma4:12b-it-q8_0`, verificado) |

Tres vías independientes coinciden: metadatos explícitos, aritmética de tamaño y contraste con el q8 real.

- **Impacto:** toda tabla o texto que citara ese nombre describía **incorrectamente** la cuantización.
- **Estado:** eliminado de **documentación y configuración** por decisión del autor. Nombre canónico:
  `gemma4:12b-mlx`.
- ⚠️ **Alcance real (verificado 2026-09-05):** el nombre retirado **sigue presente en los datos
  experimentales** — 14 archivos bajo `results/`, incluidas 30 filas de `results/benchmark_results.csv`
  (`..._baseline` y `..._rag_enhanced`). La Tabla 2 de la tesina se apoya en ese CSV. Ver F26.

---

## 3. Infraestructura y entorno

### F5. Entorno virtual inutilizable
Todas las rutas del `venv` apuntaban a `/Users/eahumada1/` (home renombrado; no existe). Afectaba al
symlink del intérprete, `pyvenv.cfg` y los shebangs de **41 scripts**. `site-packages` estaba intacto
(316 paquetes), por lo que bastó repuntar rutas sin reinstalar.

### F6. Los dos modelos cloud no son ejecutables
Verificado llamando directamente a la API de Ollama con la clave del proyecto:

| Modelo | Código | Causa |
|:---|:---|:---|
| `gemma4:31b-cloud` | **429** | *"you have reached your weekly usage limit"* |
| `minimax-m3:cloud` | **402** | Requiere suscripción de pago; la API key no lo desbloquea |

- **Impacto:** el estudio queda con **12 modelos** (5 de la corrida 2026-09-01 + 7 locales). *Corrección
  2026-09-05: esta línea decía 14 antes de la exclusión de `gpt-oss:20b` por RAM (ver F24).*

### F7. La conexión es un hotspot celular con Modo de Datos Reducidos
`gateway 172.20.10.1` (rango de Hotspot Personal de iPhone) y la interfaz `en0` marcada como
**`constrained`**, indicador con el que macOS **deprioriza el tráfico en segundo plano**.

- **Impacto:** ~85 GB de descargas sobre datos móviles, con estrangulamiento del sistema operativo.
- **Nota:** un Mac tiene **una sola radio Wi-Fi**; conectarse a varias redes simultáneamente no es posible,
  y aunque se activen varias interfaces macOS no las agrega para un proceso como `ollama`.

### F8. Paralelismo mal configurado: 183 horas de proyección
La corrida se lanzó con el default `num_workers=2` mientras la corrida de referencia usó **9**.

- **Evidencia:** latencia media 610 s/artículo → proyección de **183 h (7,6 días)** para 2160 filas.
- **Estado:** corregido a `--num-workers 9` (AIMD lo ajusta a 8 por el tope de CPU). Proyección ≈ 14 h.

### F9. La máquina se suspende tras 1 minuto de inactividad
`pmset` con `sleep 1` en batería y en AC. Mitigado con `caffeinate -dimsu`, con la salvedad de que
**no impide la suspensión al cerrar la tapa** sin monitor externo.

---

## 4. Consistencia documental

### F10. 115 inconsistencias confirmadas (26 de gravedad alta)
Auditoría con **verificación adversarial**: cada hallazgo fue re-comprobado por un segundo agente contra
el archivo real; 17 no resistieron la comprobación y fueron descartados. Las más graves:

- **Conteo de modelos contradictorio**: §1.4 y §4.2 dicen 15; §2.5, §5.1 y §5.3.5 dicen 16. El conteo real
  de la Tabla 2 es **12 modelos distintos en 13 configuraciones**.
- **Abstract en inglés corrupto**: contiene la palabra española «balanceado» y el nombre de dataset
  duplicado; la referencia [18] tiene la URL inválida `https://Kleptotrace/CoNLL-2002.org`.
- **§4.1.2 autocontradictorio**: «datos reales balanceados generados por LLM» bajo un título que dice
  «Corpus Sintético». Residuo de un reemplazo global mal aplicado.
- **Tabla 2 partida** por una línea vacía, que deja `nemotron-mini` y `deepseek-r1` fuera del renderizado.
- **§6.1 sesgada**: confirma la hipótesis (F1 ≥ 70%) solo con N=30 (79.03%), omitiendo que en el corpus
  real N=120 el mejor F1 es **59.25%**, bajo el umbral. Es el mayor riesgo en la defensa oral.

### F11. `Informe_Final_Tesina_NER.docx` está incompleto
Le faltan **§4.1.3 y §5.3.5 completas**. Verificado: cero ocurrencias de `4.1.3`, `5.3.5` y `10.2096` en su
XML, mientras el borrador sí las contiene. El archivo con nombre de entregable final es el más desactualizado.

### F12. Un hallazgo de auditoría resultó ser un falso positivo
La auditoría reportó las filas `gemma4:latest (ZS-ES)` y `(FS-ES)` como un «duplicado». **No lo son**: son
dos configuraciones de prompt legítimas (zero-shot y few-shot en español) con resultados distintos.
El autor lo detectó antes de que el workflow de corrección eliminara una fila de datos reales.

---

## 5. Entorno de trabajo multi-agente

### F13. Concurrencia entre sesiones no coordinada
`HISTORIAL-CONSOLIDADO.md` apareció modificado por un agente externo a la sesión que trabajaba en él.
`ListAgents` reveló otra sesión activa (`transfer-monitor-b1`), pero **Claude Desktop no aparece** en ese
listado, por lo que su ausencia no prueba que no haya nadie más editando.

### F14. La contención de I/O simula paquetes rotos
Bajo descargas concurrentes, `import sklearn` y `import statsmodels` fallaban con `TimeoutError`,
sugiriendo corrupción. Eran **falsos positivos**: `import requests` consumió 2m22s de reloj pero solo
**0.18 s de CPU (0%)**. La verificación de integridad confirmó **0 archivos faltantes** en los 8 paquetes.

---

## 6. Hallazgos adicionales de la sesión

### F15. Los metadatos de paginación de los `.docx` no son fiables
Tres de los cuatro `.docx` declaran en `docProps/app.xml` **«1 página, 83 palabras»**, cifra imposible para
documentos de decenas de páginas. Solo el de plantilla declara 6 páginas / 1646 palabras, también dudoso.

- **Impacto:** el cumplimiento del límite de 25 páginas **no puede verificarse leyendo los metadatos**.
  Requiere abrir el documento en Word o un renderizador real.
- **Consecuencia práctica:** cualquier afirmación sobre el conteo de páginas basada en `app.xml` es inválida.

### F16. Inconsistencia en el conteo de páginas del propio historial
`HISTORIAL-CONSOLIDADO.md` se contradice: sus tablas de estado dicen **«24 páginas»** (margen de 1 frente
al límite de 25), mientras §9 y `research/rag/WORKLOG.md` dicen **«cuerpo de 20 páginas, 29 totales»**
(margen de 5).

- **Impacto:** el margen real disponible era **desconocido** mientras duró la contradicción.
- ✅ **RESUELTO (verificado 2026-09-05):** `HISTORIAL-CONSOLIDADO.md` unificó la cifra a **20 pp. de
  cuerpo**, anexos desde la 21, 29 pp. totales, con **holgura real de 5 páginas** frente al límite de 25.
  La medición intermedia de 24 pp. quedó superada por la corrección de estilos. El supuesto conservador
  de «1 página» que se usó durante la sesión era **innecesariamente restrictivo**.

### F17. Los artefactos de `results/` no están versionados
`results/` figura en `.gitignore` (línea 7). Por tanto `results/RUNS_INDEX.md` —el índice histórico de
corridas— **no queda bajo control de versiones**, igual que el resto de artefactos experimentales.

- **Impacto:** el catálogo de corridas puede perderse como se perdieron los datos de N=30.
- **Mitigación posible:** `git add -f results/RUNS_INDEX.md`, como ya se hizo con
  `kb_rag_analysis_20260901.json`, único artefacto de `results/` versionado.

### F18. Copias de rescate manuales sin documentar
La raíz de `results/` contiene `benchmark_results 2.csv` y `statistical_report 2.md`. El sufijo « 2» es el
patrón que macOS aplica al copiar un archivo en la misma carpeta, lo que sugiere **rescates manuales** de
una corrida previa. No están documentados en ningún registro.

- **Impacto:** posible evidencia superviviente de corridas antiguas; conviene inspeccionarlos antes de
  cualquier limpieza de `results/`.

### F19. El flag `--ablation` no se persistía en la configuración de la corrida
`--ablation` viajaba solo como argumento de `run_benchmark()` sin ser campo de `BenchmarkConfig`. Los
`run_config.json` de las corridas de ablación declaraban `rag_study: false` y `SYSTEM_PROMPT.md`,
**indistinguibles de un baseline**; solo podían identificarse leyendo la columna `model` del CSV.

- **Estado:** corregido; `ablation` es ahora campo del dataclass y se vuelca.

### F20. Modelos solicitados ≠ modelos ejecutados, sin aviso
`gpt-oss:20b` figuraba en la configuración de una corrida pero fue **omitido silenciosamente**; su ausencia
solo consta en `benchmark.log`. El pipeline hacía `continue` en tres puntos sin acumular la lista de
omitidos.

- **Impacto:** una tabla de resultados puede tener menos modelos de los declarados sin que nada lo indique.

### F21. `ollama pull` exitoso no implica que el modelo sea utilizable
Los modelos cloud descargaron su **manifiesto** correctamente (`success`), aparecían en `ollama list` y sin
embargo toda inferencia fallaba (429/402). El `pull` no valida acceso ni cuota.

- **Impacto:** una verificación de disponibilidad basada en `ollama list` da un **falso positivo**. La
  comprobación válida es una llamada de inferencia real.

### F22. Los dos artefactos de 7.7 GB eran distintos
El snapshot de julio muestra `gemma4-12b-mlx-q8-64k:latest` (ID `5ceeaf26aced`) y `gemma4:12b-mlx`
(ID `117d0d84cf2a`) coexistiendo: **mismo tamaño, IDs distintos**. El primero era con toda probabilidad un
derivado por Modelfile del segundo (mismos pesos, `num_ctx` personalizado a 64k), lo que explica la
coincidencia de tamaño con distinto identificador.

- **Impacto:** la medición histórica F1=0.1206 se tomó sobre el derivado, no sobre el tag base.

---

## 7. Para Claude Desktop

Los hallazgos con impacto directo sobre las tareas de edición de documentos asignadas en
`TODO-INFORME-FINAL.md §7`:

| Hallazgo | Qué implica para la edición de los `.docx` |
|:---|:---|
| **F11** | `Informe_Final_Tesina_NER.docx` necesita la **reinserción íntegra de §4.1.3 y §5.3.5**, no solo correcciones de texto. |
| **F15** | **No confiar en los metadatos de páginas.** Verificar el límite de 25 pp. abriendo el documento. |
| **F16** | El margen real es incierto (¿1 o 5 páginas?). Determinarlo empíricamente antes de añadir texto. |
| **F10** | Las correcciones de contenido a propagar están en `AUDITORIA_CONSISTENCIA_20260903.md`. |
| **F12** | Las filas `gemma4:latest (ZS-ES)` y `(FS-ES)` son **legítimas**; no eliminarlas para cuadrar conteos. |
| **F13** | Otra sesión puede estar editando en paralelo: releer antes de escribir, preferir `append`. |

---

## 8. Restricción de hardware y exclusión de modelos

### F23. La máquina tiene 16 GB de RAM y los modelos pesados no caben
**Severidad: crítica para el diseño experimental.** Es el hallazgo que determina el alcance del estudio.

| Modelo | Tamaño | Relación con la RAM (16 GB) |
|:---|---:|:---|
| `gpt-oss:20b` | **13 GB** | Deja ~3 GB para SO, Ollama y KV cache |
| `gemma4:31b` / `gemma4:31b-mlx` | **19 GB** | **Exceden la RAM física** |

**Evidencia del impacto:** el ritmo medido fue de **exactamente 1 extracción cada 3 minutos**, y **no varió**
al aumentar los workers de 2 a 8. Ollama no serializa por configuración sino **porque no cabe otro contexto
en memoria**; `OLLAMA_NUM_PARALLEL` no lo resolvería. En el pico, la memoria libre cayó al 12% con un load
average de 12.33.

**Proyección con los 9 modelos locales:** ≈ **173 horas (7 días)**, de las cuales los tres modelos pesados
concentraban el **85%**.

### F24. Decisión: exclusión de `gpt-oss:20b`
**Autorizada por el autor el 2026-09-03.** Se excluyen del estudio los dos modelos que no caben
razonablemente en 16 GB de RAM.

| Métrica | Antes | Después |
|:---|---:|---:|
| Modelos locales en la corrida | 9 | **7** |
| Modelos totales del estudio | 14 | **12** |
| Proyección de cómputo | ~173 h | **~66 h** |

**Compatibilidad con la corrida de referencia del 2026-09-01: verificada e intacta.** Los nueve parámetros
del protocolo coinciden (`data_file`, `rag_study`, `rag_mode=kb_combined`, `batch_size=3`, `temperature=0.1`,
`seed=42`, `max_tokens=2048`, `system_prompt_file`, `fuzzy_threshold=85`). Los dos modelos excluidos
**tampoco formaban parte** de la corrida del 1-sep, por lo que ambos conjuntos siguen siendo disjuntos sobre
el mismo corpus y el mismo protocolo: la fusión para el ANOVA conjunto sigue siendo válida.

> **Debe declararse en la tesina como limitación de hardware**, no como decisión metodológica: los modelos
> se excluyeron por una restricción física del equipo de evaluación (16 GB de RAM), no por criterios
> experimentales. Ver `TODO-INFORME-FINAL.md`.

### F25. El workflow de corrección introdujo regresiones
De 84 correcciones aplicadas, la etapa de verificación detectó **5 regresiones**, todas reparadas:

1. **Violación de la política aditiva**: se eliminó la entrada `glm-5.1:cloud` de `BENCHMARKS.md` sin dejar
   marca. Restaurada con una nota explicativa. *(Actualización 2026-09-05: horas después, y ya con
   decisión explícita del autor, se eliminó definitivamente al comprobarse que **nunca tuvo resultados**
   y que requiere suscripción de pago. Ver `TODO-INFORME-FINAL.md §9`.)*
2. **Código de ejemplo sintácticamente inválido** en `AGENTS.md §8.3`: un `field(default_factory=lambda: [`
   quedó sin cerrar el paréntesis.
3. **Reaparición del nombre de modelo retirado** en `AGENTS.md §8.6`, dentro de una nota de retiro.
   Reformulada sin citarlo.
4. **Autocontradicción entre secciones contiguas**: §8.4 conservaba la forma antigua `self.models = [...]`
   mientras §8.1 y §8.3 ya declaraban que la lista es un campo del dataclass.
5. **Consejo inoperante**: se documentó `--resume` sin mencionar que requiere `--results-dir`.

> La etapa de verificación adversarial **valió su coste**: sin ella, las cinco habrían pasado inadvertidas.

---

## 9. Alcance real de la retirada de nombres

### F26. El nombre de modelo retirado sobrevive en los datos experimentales

> **RESUELTO el 2026-09-08 por decisión del autor: eliminación total.** La etiqueta se retiró de **todos** los
> datos y de todos los entregables, no solo de la documentación como en el intento de septiembre de 2026 que
> este hallazgo declaró insuficiente. Se retiraron 270 filas de resultados —240 de la corrida N=120 y 30 del
> CSV consolidado—, sus registros equivalentes en los `detailed_results.json`, las entradas de los resúmenes,
> los puntos de control y las configuraciones, las filas de los informes estadísticos derivados, 990 líneas de
> los dos registros de ejecución, y las dos filas del Anexo I del informe, cuyo recuento pasó de 49 a 47
> configuraciones. **Verificado: cero rastros en `results/` y en el informe.** Quedan solo en respaldos
> `.bak`, en ficheros duplicados y en los documentos internos que registran esta corrección, que es lo
> contrario de un rastro del modelo.
>
> La decisión es defendible porque esa etiqueta **no era un modelo distinto**: medía `gemma4:12b-mlx` con un
> sufijo de cuantización falso, ya que el artefacto real es 4-bit NVFP4 y no q8 (ver F4). Retirarla no quita
> un modelo del estudio, quita una **medición duplicada mal etiquetada** de un modelo que sigue presente con
> su nombre correcto.

**Severidad: alta (integridad académica).** Detectado el 2026-09-05 por una auditoría de coherencia.

Se afirmó en varios documentos que el nombre `gemma4-12b-mlx-q8-64k` tenía **«cero ocurrencias en todo el
proyecto»**. La afirmación era **falsa**: la limpieza cubrió documentación y configuración, pero **no los
datos**.

Sigue presente en **14 archivos** bajo `results/`, entre ellos:

| Archivo | Contenido |
|:---|:---|
| `results/benchmark_results.csv` | **30 filas** con `gemma4-12b-mlx-q8-64k:latest_baseline` y `..._rag_enhanced` |
| `results/statistical_report.md` | Reporte estadístico derivado de ese CSV |
| `results/benchmark_summary.json`, `detailed_results.json`, `.checkpoint.json`, `run_config.json` | Artefactos de la misma corrida |
| `results/benchmark_balanced_120_20260824_173036/*` | Corrida N=120 completa con los mismos artefactos |

**Por qué importa:** la Tabla 2 del informe se apoya en esos datos. Un revisor que descienda del texto a los
datos crudos encontrará un modelo etiquetado con una cuantización que **no corresponde** (el artefacto es
4-bit NVFP4, no q8 — ver F4).

**Opciones:**
1. Renombrar la etiqueta en los CSV y regenerar los reportes derivados. Altera datos históricos.
2. Dejar los datos intactos y **documentar la equivalencia** en el informe: «la etiqueta
   `gemma4-12b-mlx-q8-64k` de los datos crudos corresponde a `gemma4:12b-mlx`; el sufijo `q8` es erróneo».
3. Excluir del informe las filas de ese modelo.

**Recomendación:** la opción 2. Preserva la trazabilidad de los datos y corrige la interpretación, que es lo
que la política aditiva del proyecto favorece. **Requiere decisión del autor.**

---

## 10. Hallazgos de integridad numérica (ronda 2 de correcciones)

### F27. Valores de F1 aritméticamente imposibles
**Severidad: crítica.** Dos filas de `BENCHMARKS.md` («RAG Integration Study») declaran un F1 **superior al
máximo matemáticamente posible**.

F1 es la media armónica de precisión y recall, y la media armónica **nunca** supera a la aritmética. Por
tanto `F1 ≤ (P+R)/2` siempre. Verificado:

| Fila | F1 declarado | Cota máxima (P+R)/2 | F1 armónico real |
|:---|---:|---:|---:|
| `llama3.2:latest_rag` | **0.8783** | 0.7646 | 0.7551 |
| `llama3.1:8b_baseline` | **0.7667** | 0.7333 | 0.6955 |

Ambas violan la cota. **No son cifras con ruido: son imposibles.** Un revisor que haga la comprobación —
que es de aritmética elemental— concluirá que los datos no fueron calculados con la fórmula declarada.

- **Origen:** el CSV del prototipo sobre `data/sample_sanctions.json` (20 registros) no sobrevive, y la
  corrida no figura en `results/RUNS_INDEX.md`. No son recalculables.
- **Requiere decisión del autor:** recalcular desde datos que ya no existen es imposible; las opciones son
  retirar esas filas del informe, o marcarlas explícitamente como no verificables.

### F28. ✅ RESUELTO — Dos modelos distintos con métricas byte-idénticas

> **Resuelto, comprobado el 2026-09-09.** Las cifras que denunciaba —67.83, 57.29 y 114.20— **no aparecen
> ni una vez en el informe actual**. Es además el bloqueante **#2** del `TODO §10`, verificado allí con la
> misma evidencia. Su causa era `§F33`, hoy también resuelto.
**Severidad: alta.** En la Tabla 2 del informe:

```
| **gemma4:31b** | Local | 31B | 67.83% | 57.29% | 86.78% | 0.15% | 114.20 |
| gemma4:31b-mlx | Local | 31B | 67.83% | 57.29% | 86.78% | 0.15% | 114.20 |
```

Dos modelos con **runtime distinto** (GGUF vs MLX) coinciden en F1, precisión, recall, tasa de alucinación
**y latencia**, hasta el último decimal. Es estadísticamente inverosímil: sugiere que una fila se copió de
la otra.

Además, **el 67.83% no tiene respaldo en datos crudos**: solo aparece en `results/RUNS_INDEX.md` (un
catálogo, no una medición) y en el checkpoint de una corrida descartada. La única medición independiente de
`gemma4:31b-mlx` que existe (`results/benchmark_summary.json`, 27-jul, 15 registros) da **F1=0.6852 /
P=0.5831 / R=0.8676** — cifras distintas.

- **Requiere decisión del autor** sobre qué corrida cita realmente la Tabla 2.

### F29. Cifras de mercado sin fuente
`§1.1` del informe contiene el marcador literal `[referencia KPMG 2024]` junto a cifras de mercado
(USD 12.300 y 87.200 millones). El agente corrector **se negó a inventar la cita**, con buen criterio:
fabricar una referencia bibliográfica en una tesina es falsificación académica.

- **Requiere que el autor aporte el informe exacto** y se añada como referencia numerada. Si no existe, hay
  que retirar las cifras.

### F30. Contradicción de hardware declarada en el método
`§2.4` y `§3.6` declaran ejecutar modelos que la instrumentación registra con **24.6–26.6 GB de VRAM** sobre
un equipo de **16 GB de memoria unificada** (`hw.memsize` verificado). Es físicamente contradictorio tal como
está redactado; requiere explicar el mecanismo real (memoria comprimida, swap, offload por capas) o
reinterpretar qué mide `vram_mb`.

---

## 11. Resolución de bloqueantes (2026-09-05)

### F31. ✅ RESUELTO — La contradicción de hardware es un problema de etiquetado, no físico
El informe declaraba ejecutar modelos de ~24.7 GB de VRAM sobre 16 GB de memoria unificada.

**Causa raíz identificada en el código.** `src/system_monitor.py:163-185` obtiene `vram_mb` leyendo el
campo `size_vram` de `/api/ps` de Ollama. Ese campo reporta memoria **asignada**, no residente. En Apple
Silicon con memoria unificada, macOS permite *over-commit* mediante compresión y swap, de modo que la
asignación puede superar la RAM física sin contradicción alguna.

Datos que lo confirman: `gemma4:31b-mlx` (19.4 GB en disco) reporta 26.3–26.9 GB de asignación —coherente
con pesos + KV cache bajo over-commit—, y **480 muestras** superan los 16 GB físicos.

**Defecto adicional detectado:** si el nombre del modelo no coincide, el código cae en un *fallback* que
**suma la VRAM de todos los modelos cargados** (`líneas 178-183`), lo que puede inflar el valor aún más.

**Corrección para el informe:** sustituir «VRAM» por «memoria unificada asignada por Ollama (`size_vram`)»
y añadir que macOS permite over-commit. La cifra deja de ser contradictoria.

### F32. ✅ RESUELTO — Ningún esquema de promediado explicaba los F1 imposibles

> **Resuelto, comprobado el 2026-09-09.** Los valores que denunciaba —0.8783 y 0.7667— **no están en el
> informe**, y la comprobación aritmética del verificador examina **61 filas sin una sola violación** de
> `F1 ≤ (P+R)/2`. La demostración de abajo sigue siendo válida y es la que sostiene esa comprobación: la cota
> se conserva bajo cualquier esquema de promediado.
Se consideró que los F1 fuera de rango pudieran deberse a macro-promediado. **No es posible.**

**Demostración:** para cada registro *i*, `F1_i ≤ (P_i + R_i)/2` (la media armónica nunca supera a la
aritmética). Promediando ambos lados: `mean(F1_i) ≤ (P̄ + R̄)/2`. La cota **se conserva bajo cualquier
esquema de promediado**, micro o macro.

Por tanto los valores son incorrectos, sin explicación metodológica posible:

| Fila | F1 declarado | F1 armónico de los P,R declarados | Desviación |
|:---|---:|---:|---:|
| `llama3.2:latest_rag` | 0.8783 | **0.7551** | +0.1232 |
| `llama3.1:8b_baseline` | 0.7667 | **0.6955** | +0.0712 |

**Opciones:** (a) sustituir por el F1 armónico si se confía en P y R; (b) retirar las filas; (c) marcarlas
como no verificables. Los datos crudos no sobreviven, así que no se puede determinar si el error está en F1
o en P/R. **Requiere decisión del autor.**

### F33. ✅ RESUELTO — El modelo `gemma4:31b` no tenía datos crudos en ninguna corrida

> **Resuelto, comprobado el 2026-09-09.** El equipo de 48 GB lo midió después de escribirse este hallazgo:
> `gemma4:31b` aparece hoy con datos crudos en **cuatro corridas** —`gemma4_31b_n15_REMOTO` (15+15 filas),
> `n30_rerun_REMOTO` (30) y `test_nothink` (15+15)—. La Tabla 8 del informe declara expresamente que su fila
> procede de `results/gemma4_31b_n15_REMOTO/benchmark_results.csv`. El texto original se conserva porque
> documenta el estado en que se detectó.
Verificado exhaustivamente: **`gemma4:31b` (sin sufijo `-mlx` ni `-cloud`) no aparece en ningún
`benchmark_results.csv` del proyecto.** Solo existen `gemma4:31b-mlx` y `gemma4:31b-cloud`.

Esto explica F28 (las dos filas idénticas de la Tabla 2): la fila de `gemma4:31b` **no procede de una
medición independiente**. Y afecta a dos lugares del informe:

| Ubicación | Cifra citada | Respaldo |
|:---|:---|:---|
| Tabla 2 (§5.1) | `gemma4:31b` F1 = 67.83% | ❌ ninguno |
| §5.5 eficiencia | `gemma4:31b` 18.803 MB / 11.37 tok/s | ❌ ninguno |
| Log N=30 (2026-07-01) | `gemma4:31b` F1 = **79.03%** | ✅ log, pero es **otra cifra** |

La única medición real de `gemma4:31b` que sobrevive da **79.03%**, no 67.83%. **Requiere decisión del
autor** sobre el origen de la cifra de la Tabla 2.

### F34. ✅ RESUELTO — La tabla de eficiencia cita muestras puntuales, no agregados
Los valores de §5.5 **sí existen en los datos**, pero como observaciones individuales, no como medianas o
medias de una corrida. Por ejemplo `27.593626` tok/s aparece como muestra suelta en
`results/benchmark_results.csv`, mientras la **mediana** de `gemma4:31b-mlx` en esa corrida es **21.99**.

Comparación con los agregados reales:

| Modelo | §5.5 del informe | Mediana real (corrida raíz, N=15) |
|:---|:---|:---|
| `gemma4:31b-mlx` | 24.751 MB / 27.56 tok/s | 26.26 GB / **21.99 tok/s** |
| `llama3.2` | ~3.000 MB / 47.5 tok/s | 3.92 GB / **78.57 tok/s** |

**Corrección:** regenerar §5.5 desde los agregados reales, o declarar explícitamente que son mediciones
puntuales de monitorización y no estadísticos de la corrida.

---

## 12. Contaminación de resultados por fallos de cuota

### F35. 🔴 Los resultados de los modelos cloud están contaminados por fallos de infraestructura
**Severidad: crítica.** Detectado el 2026-09-05 a partir de una hipótesis del autor: *«¿no será que se
produjeron fallas en la ejecución por cuota?»*. **Confirmada.**

La corrida N=15 registró **507 líneas con errores de cuota** (88 fallos de `gemma4:31b-cloud`, 95 de
`minimax-m3:cloud`). Las extracciones fallidas se contabilizan con recall 0 y arrastran las medias:

| Modelo | `parse_method=failed` | Recall = 0 | Reintentos | **N efectiva** |
|:---|---:|---:|---:|---:|
| `gemma4:31b-cloud` | 6 / 15 | 6 / 15 | 8 / 15 | **9** |
| `minimax-m3:cloud` | 9 / 15 | 10 / 15 | 9 / 15 | **6** |
| `gemma4:31b-mlx` (local, control) | **0 / 15** | 0 / 15 | 0 / 15 | 15 |

El modelo local sirve de control perfecto: 15/15 `direct_json`, cero reintentos. **El problema es exclusivo
de los modelos remotos.**

**Consecuencia sobre el análisis previo.** Este hallazgo **invalida la recomendación de F8/§9.2** de
sustituir la tabla por los valores crudos. Recalculando solo sobre las extracciones exitosas:

| Modelo | Crudo (con fallos) | **Solo exitosas** | Tabla `BENCHMARKS.md` |
|:---|---:|---:|---:|
| `gemma4:31b-cloud` | 0.3973 | **0.6622** (n=9) | **0.6754** |
| `minimax-m3:cloud` | 0.2011 | **0.5028** (n=6) | 0.6321 |
| `gemma4:31b-mlx` | 0.6852 | 0.6852 (n=15) | 0.6456 |

Para `gemma4:31b-cloud` la coincidencia es de 1-2 puntos en las tres métricas ⇒ **la tabla refleja el
subconjunto exitoso**. No era una cifra inventada.

**El defecto real de la tabla** no es el valor, sino **declarar N=15 ocultando que 6 extracciones
fallaron**. Con 6 muestras útiles (`minimax-m3`), el intervalo de confianza es enorme.

**Lección metodológica.** Un promedio que incluye ceros de fallos de infraestructura **no es una medición
del modelo**. Antes de comparar dos fuentes discrepantes hay que verificar que **ambas midan lo mismo**.
Sin la hipótesis del autor, se habrían incorporado a la tesina cifras contaminadas presentándolas como
rendimiento del modelo.

**Defecto de instrumentación asociado:** `parse_method` marca como `failed` tanto un fallo de cuota
(HTTP 429/402) como un fallo de parseo del modelo. Son causas distintas —una es infraestructura, la otra una
limitación del modelo— y hoy son indistinguibles en los datos. Ver `TODO-INFORME-FINAL.md §11.1`.

---

## 13. Límite físico del hardware para modelos de 19 GB

### F36. 🔴 `gemma4:31b` no es ejecutable en esta máquina, ni con un solo worker
**Severidad: alta (limita el alcance del estudio).** Verificado empíricamente el 2026-09-05.

Primer intento con `--num-workers 9` (replicando el protocolo original):

| Métrica | Valor |
|:---|---:|
| Extracciones iniciadas | 15 |
| Respuestas recibidas en 26 min | **0** |
| Swap usado | **16.1 GB de 17.4 GB** |
| Pageouts | **7.834.527** |
| Memoria libre | 8% |
| CPU de `llama-server` | 31% (el resto, esperando disco) |

Diagnóstico: 8 peticiones concurrentes ⇒ 8 KV-caches simultáneos sobre un modelo de 19 GB en 16 GB de RAM.

**Segundo intento con `--num-workers 1`** (un único KV-cache). Tras liberar el modelo, la memoria subió al
71% libre y el swap bajó a 4.3 GB. Pero a los 90 s de reanudar: **memoria de nuevo al 3%, swap en 15 GB, y
0 respuestas**.

**Conclusión:** el problema no es la concurrencia sino el **tamaño del modelo**. 19 GB de pesos no caben en
16 GB de memoria física; el sistema pagina de forma continua independientemente del paralelismo.

**Implicación para la tesina:** la fila de `gemma4:31b` de la Tabla 2 **no es recuperable en este hardware**.
Las opciones se reducen a: (a) retirar la fila, (b) marcarla como no verificable, o (c) ejecutarla en un
equipo con ≥32 GB de RAM.

> Contraste útil: `gemma4:31b-cloud` es **el mismo modelo servido remotamente** y funciona sin consumir
> memoria local. No sustituye a la fila local (compara runtimes distintos), pero demuestra que la
> limitación es exclusivamente de hardware local.

### F37. ✅ Acceso cloud restaurado por reautenticación
Tras el `ollama signin` del autor con una cuenta alternativa, verificado a través del daemon local:

| Modelo | Estado |
|:---|:---|
| `gemma4:31b-cloud` | ✅ **operativo** — responde correctamente |
| `minimax-m3:cloud` | ❌ HTTP 402 — requiere plan de pago (limitación de plan, no de autenticación) |

Esto **desbloquea la re-ejecución limpia de `gemma4:31b-cloud`** (ver F35: sus datos actuales tienen 6 de 15
extracciones fallidas por cuota). `minimax-m3` seguirá sin ser re-ejecutable sin contratar plan.

**Dato operativo verificado:** el `signin` **no reinicia** `ollama serve` (el daemon llevaba 2 días 11 h en
marcha y siguió igual), por lo que **no interrumpe una corrida en curso**. La preocupación previa de tener
que elegir entre autenticar o preservar el benchmark era infundada.

### F38. 🔴 `minimax-m3:cloud` retirado del estudio — resultado irreparable
**Decisión del autor, 2026-09-05.** El modelo sale del benchmark y de la documentación.

**Justificación acumulada de tres hallazgos independientes:**

| Evidencia | Origen |
|:---|:---|
| **9 de 15 extracciones fallidas**; **10 de 15 con recall = 0**; N efectiva = **6** | F35 |
| **HTTP 402 — requiere plan de pago.** Re-verificado el 2026-09-06 tras reautenticar: sigue devolviendo 402 | F6, F37, F42 |
| Su fila declaraba F1 = 0.6321 sobre un supuesto N=15; el crudo da 0.2011 y el subconjunto exitoso 0.5028 (n=6) | F35 |

> ⚠️ **Precisión sobre la justificación (corregida el 2026-09-06).** La redacción original de este hallazgo
> atribuía los fallos de julio al plan de pago. **Es inexacto:** el log de aquella corrida registra
> **140 líneas con `status code: 429`** (cuota) frente a **1 sola** mención de 402. En julio el modelo
> falló por **cuota agotada**, que es temporal y se renueva. La barrera de **plan de pago (402)** es lo que
> impide recuperarlo **hoy**, y fue confirmada de nuevo tras la reautenticación del autor.
>
> La distinción importa porque, según `LEARNING.md §L22`, un 429 justifica esperar y un 402 obliga a
> retirar. **La decisión de retirarlo sigue siendo correcta**, pero por la barrera actual, no por la de
> julio.

Un resultado con **60 % de tasa de fallo** y **sin posibilidad de repetición** no es defendible. A diferencia
de `gemma4:31b-cloud` —cuya cuota se renueva y sí pudo reautenticarse—, aquí la barrera es de plan
comercial y no desaparece con el tiempo.

**Alcance de la retirada:**

| Retirado | Conservado y por qué |
|:---|:---|
| `src/config.py` — lista de modelos evaluados | `src/llm_runner.py:64` — el patrón `"minimax"` de `is_cloud_model()` es **lógica de enrutamiento genérica**; eliminarlo rompería la detección de cualquier modelo cloud futuro con ese nombre |
| `run_benchmark.sh` — invocación | `AGENTS.md §8.2` — tablas que documentan ese mismo patrón de enrutamiento |
| `BENCHMARKS.md` — fila de resultados y listado de configuración | Registros históricos (`WORKLOG.md`, `research/rag/WORKLOG.md`, auditorías) — documentan **por qué** se retiró |
| `src/dashboard.py` — declaración del modelo | `doc/organized/Hito_4_*` — entregas históricas, no se modifican |
| `AGENTS.md §8.6` — marcado ❌ **RETIRADO**, no borrado | Datos crudos en `results/` — evidencia primaria intacta |

La tesina (`.md`) **no lo mencionaba**: verificado, cero ocurrencias antes de la retirada.

---

## 14. Entradas experimentales tratadas como artefactos regenerables

### F39. 🔴 Los diccionarios del RAG son un snapshot irreproducible, y estuvieron sin versionar
**Severidad: crítica (reproducibilidad).** Detectado el 2026-09-06 a partir de una pregunta del autor:
*«¿por qué los diccionarios no están versionados?»*.

Se habían excluido del repositorio con el razonamiento de que son «descargables con los scripts del repo».
**El razonamiento era falso.** Los scripts construyen los diccionarios desde **fuentes vivas**:

| Fuente | Estabilidad |
|:---|:---|
| `treasury.gov/ofac/downloads/sdn.csv` | ❌ La lista SDN cambia **cada pocos días** |
| 3 repositorios de GitHub | ❌ Todos apuntan a `master`, rama móvil |

Ningún script fija fecha, versión ni commit, y **los archivos generados no llevan metadata alguna**: son
listas planas de 3.605, 1.848 y 12.000 entradas, sin fuente ni fecha. Solo el mtime del sistema de archivos
(2026-07-27) delata cuándo se crearon.

**Por qué son entrada experimental y no un artefacto.** El RAG en modo `entities` **inyecta estas entradas
en el prompt**. Un diccionario distinto cambia el contexto que ve el modelo y, por tanto, los resultados.
Regenerarlos no reconstruye el experimento: lo altera.

**Riesgo concreto que se evitó.** El encargo al equipo remoto **les instruía explícitamente a
regenerarlos** antes de las tareas 1 y 4. Habrían obtenido un conjunto distinto, sus resultados RAG no
habrían sido comparables con las corridas previas, y **nada en la salida lo habría advertido**. Es el mismo
modo de fallo que el `--rag-mode` por defecto (F3): una divergencia silenciosa que solo aparece al comparar.

**Corregido:** los diccionarios se versionan (1.8 MB), se añade `data/dictionaries/PROCEDENCIA.md`
documentando fuentes y fecha, y el encargo remoto pasa de «regeneradlos» a «**NO los regeneréis**», con una
comprobación de conteo (3605 / 1848 / 12000) antes de empezar.

---

## 15. El F1 anómalo era un bug del arnés, no del modelo

### F40. 🔴 `gemma4:12b-mlx` devolvía respuestas vacías por agotamiento del presupuesto de tokens
**Severidad: crítica.** Investigado el 2026-09-06 a petición del autor. **Invalida el hallazgo F-anterior**
que interpretaba su F1 de 0,0987 como una limitación de formato del modelo.

`gemma4:12b-mlx` declara capacidad `thinking` y Ollama la activa por defecto. En artículos largos el
razonamiento **agota `num_predict` (2048) antes de emitir la respuesta**: `message.content` llega vacío y
el pipeline registra cero entidades.

| Indicador (N=120, baseline) | Valor |
|:---|--:|
| Registros con recall = 0 | **101 / 120** |
| Respuestas crudas vacías | **272 / 273** |
| Errores HTTP · reintentos | **0 · 0** |
| Artículos que fallan vs. que sobreviven | **1,36× más largos** (1976 vs 1453 chars) |

**Reproducción y fix, peor caso (8813 chars):**

| Configuración | `content` | `thinking` | `eval_count` |
|:---|--:|--:|--:|
| Actual | **0** | 7 651 | **2 048** ← tope exacto |
| `think=False` | **918** | 0 | 311 |

Con el razonamiento desactivado extrae **14 personas, 6 organizaciones y 16 ubicaciones** del mismo
artículo que antes devolvía nada.

**Corrección de la interpretación previa.** Se había concluido que era «un fallo de formato de salida, no
de comprensión», y que la precisión de 0,93 mostraba que «cuando extrae algo acierta». **Ambas afirmaciones
eran falsas.** La precisión de 0,93 es el **caso degenerado**: con el *scorer* vigente en aquel momento, con
`tp=0` y `fp=0` la precisión se definía como 1,0, de modo que un modelo que no extraía nada tenía precisión
perfecta. *(Corregido el 2026-09-06 en `src/evaluator.py` —commit `7a6c19f`—: los defaults micro pasaron de
1,0 a **0,0**, y solo se asigna 1,0 si `tp+fp+fn == 0`. La cifra de 0,93 procede de la puntuación anterior.)*

### F41. 🔴 El modo *thinking* de Qwen3 nunca llegó a activarse
Descubierto al corregir F40. `think` es **parámetro de primer nivel** de `Client.chat()`, no una clave de
`options`. El código hacía `options["think"] = True`, donde **Ollama lo ignora en silencio**.

Consecuencia: las cifras de `qwen3:8b` del estudio se midieron con el modo thinking **desactivado**, pese a
que el código creía activarlo y así lo documentaba `AGENTS.md §8.2`. Sus resultados no son incorrectos,
pero **no miden lo que se declaraba medir**.

**Ambos corregidos** en `src/providers/ollama_provider.py`: `think` pasa como parámetro de primer nivel,
con un nuevo `_THINKING_DISABLED_MODELS` para las variantes MLX de gemma4.

### F42. ✅ Auditoría de las recomendaciones sobre modelos cloud
**Realizada el 2026-09-06 a petición del autor**, aplicando a los cloud el mismo escrutinio que destapó el
bug de *thinking* en `gemma4:12b-mlx` (F40).

**Lo que se confirmó válido:**

| Comprobación | Resultado |
|:---|:---|
| ¿La corrida limpia de `gemma4:31b-cloud` tiene la firma del bug de *thinking*? | **No.** 30/30 `direct_json`, cero recall=0, ~74-83 tokens generados |
| ¿Los fallos de julio eran el bug de *thinking*? | **No.** Latencia **0,0 s** y **0 tokens**: la petición nunca obtuvo respuesta. El bug de thinking produce lo contrario — latencia alta y miles de tokens con `content` vacío |
| ¿F1 = 0,6699 de `gemma4:31b-cloud` se sostiene? | **Sí**, sin salvedades |

**Lo que se corrigió:** la justificación de la retirada de `minimax-m3:cloud` confundía dos modos de fallo
distintos (ver la advertencia en F38).

**Dato operativo nuevo:** tras el `ollama signin` del autor, las dos cuentas alternativas
(`delmartg`, `4useguros`) devuelven **Unauthorized** al invocarlas directamente con su API key, cuando antes
respondían. El `signin` parece haber cambiado el contexto de autenticación. No afecta a ninguna corrida en
marcha, pero invalida la rotación de cuentas como plan de contingencia.

> **Método que hizo falta:** distinguir un fallo de infraestructura de uno del arnés exige mirar
> `latencia` y `tokens generados`, no solo `parse_method`. Latencia 0 con 0 tokens es un rechazo de red;
> latencia alta con muchos tokens y `content` vacío es el arnés perdiendo la respuesta.

### F43. `nuextract:latest` retirado del estudio
**Decisión del autor, 2026-09-06.** Se retira del benchmark y de la documentación operativa.

**Datos que motivaron la revisión:** en la corrida P3 del equipo remoto, **109 de 120 extracciones**
requirieron el parser de respaldo (`parse_method='fallback'`), una proporción del 90 % comparable a la de
`gemma4:12b-mlx` (F40).

**Evidencia que distingue ambos casos** — se recoge porque la decisión se tomó *a pesar* de ella:

| Modelo | `fallback` | De ellos con recall = 0 | F1 de esas filas |
|:---|--:|--:|--:|
| `nuextract:latest` | 109 | **2** | **0,4459** |
| `gemma4:12b-mlx` | 70 | **66** | 0,0472 |

En `nuextract` el respaldo **sí rescata contenido** (107 de 109) con F1 normal, coherente con su histórico.
No es un fallo del arnés: es un **extractor de plantilla**, tratado explícitamente como tal por el código
(`_NUEXTRACT_MODELS`, `ollama_provider.py:278`), que emite un formato propio **por diseño**.

**Justificación de la retirada:** el barrido compara modelos generalistas bajo un mismo contrato de formato
de salida. Un extractor especializado con formato propio no es homologable a ellos, y su alta tasa de
respaldo introduce una variable de tratamiento distinta a la del resto de la tabla.

**Alcance:** retirado de `src/config.py`, `run_benchmark.sh`, la tabla de resultados de `BENCHMARKS.md` y
marcado en `AGENTS.md §8.6`. **Se conserva** el manejo de plantilla en `ollama_provider.py`
(`_NUEXTRACT_MODELS`): es mecanismo de enrutado, no declaración del modelo — misma distinción aplicada al
retirar `minimax-m3` (F38, L28). Los datos crudos en `results/` permanecen intactos.

> **Nota de método.** La alerta que originó esta revisión fue **engañosa**: se señaló la tasa de fallback
> como anomalía equiparable a la de `gemma4:12b-mlx`, sin comprobar antes el indicador que de verdad
> discrimina —si el respaldo rescata contenido—. Ver `LEARNING.md §L36`.

### F44. El efecto del modo *thinking* es específico de cada modelo, no uniforme
**Evidencia (prueba controlada, 15 registros, mismo pipeline con RAG, scorer corregido, think ON vs OFF):**

| Modelo | Cond | F1 ON | F1 OFF | ΔF1 | Veloc. OFF |
|:---|:---|--:|--:|--:|--:|
| `deepseek-r1:1.5b` | baseline | 0.294 | 0.294 | ±0 | ×2.8 |
| `deepseek-r1:1.5b` | kb_rag | 0.345 | 0.345 | ±0 | ×3.7 |
| `gpt-oss:20b` | baseline | 0.419 | 0.301 | **−0.118** | ×1.6 |
| `gpt-oss:20b` | kb_rag | 0.283 | 0.155 | **−0.128** | ×3.0 |
| `gemma4:31b` | baseline (entities) | 0.691 | 0.662 | −0.029 | ×3.0 |
| `gemma4:31b` | rag (entities) | 0.639 | 0.676 | +0.037 | ×4.4 |
| `gemma4:latest` (variantes) | zs-en | 0.640 | 0.675 | +0.035 | ×5.6 |
| `gemma4:latest` (variantes) | zs-es | 0.684 | 0.704 | +0.020 | ×6.2 |
| `gemma4:latest` (variantes) | fs-en | 0.633 | 0.699 | +0.066 | ×6.0 |
| `gemma4:latest` (variantes) | fs-es | 0.744 | 0.694 | −0.051 | ×5.7 |

**Hallazgo.** Apagar el *thinking* **no es una mejora universal**:
- `qwen3:8b`: think OFF **sube** F1 (~+4 pp) y ~10× más rápido → OFF.
- `deepseek-r1:1.5b`: think OFF **F1 idéntico**, ~3× más rápido → OFF por velocidad, calidad intacta.
- **`gpt-oss:20b`: think OFF EMPEORA fuerte (−0.12 F1). El thinking le AYUDA.**
- `gemma4:31b`: neutro (base −0.03 / rag +0.04) pero **~3× más rápido** (613→203 s).
- `gemma4:latest` (variantes): mayormente **mejor** (+0.02 a +0.07; solo fs-es −0.05) y **~6× más rápido** (158→28 s).

**Síntesis:** think OFF es **neutro-a-positivo y mucho más rápido en 4 de 5**; solo `gpt-oss:20b` pierde calidad.

**Decisión del autor (firme):** **`gpt-oss:20b` se deja con think ON, congelado; su corrida oficial
(`results/excluidos_n120_REMOTO`) no se re-ejecuta ni se toca.**

**ETA real medido para re-correr con think=OFF los 4 beneficiados (latencias think-off reales):**
`deepseek-r1:1.5b` ~0.3 h · `gemma4:31b` (N=15) ~0.4 h · `gemma4:latest` (variantes N=15)
~0.15 h → **~1-1.5 h local serial en total** (gpt-oss NO se re-corre). Queda a decisión del autor si se aplica
al estudio oficial (implicaría regenerar esas corridas con think=OFF y re-fusionar el ANOVA).

> **Regla operativa.** No generalizar el ajuste de *thinking* entre modelos. Antes de apagarlo en un modelo
> con capacidad `thinking`, medir F1 ON vs OFF en una muestra con el pipeline real; sólo apagarlo si el ΔF1
> es ≥0 (o nulo con ganancia de velocidad). Modelos donde el razonamiento es parte del mecanismo de respuesta
> (p. ej. `gpt-oss:20b`) **pierden calidad** al desactivarlo. Ver `LEARNING.md §L37` (terminología) y el
> reporte `remote_48g/` de la prueba think ON/OFF.

---

### F45. Verificación del experimento *thinking* — el efecto es real en dos modelos y ruido en los otros cuatro

**Estado:** HALLAZGO FINAL. Cierra la línea de investigación sobre *thinking* abierta en §F40-F41 y §F44.
**Método:** verificación fila a fila de `results/test_nothink/` contra las corridas oficiales, con los
criterios de `RECOMENDACIONES-EJECUCIONES-FUTURAS.md §3`.

**Lo verificado del experimento del equipo remoto (§F44):** las 12 filas de su tabla **reproducen
exactamente** desde los CSV; **0 `failed` y 0 violaciones de `F1 ≤ (P+R)/2`** en las cinco corridas. El
método es correcto: pipeline real, scorer corregido, `thinking` como única variable, cambio de código
revertido.

**Dos resultados se refuerzan al mirar el mecanismo:**

- **`gpt-oss:20b`** — lo decisivo no es el ΔF1 de −0.12, sino **por qué**: con el razonamiento apagado
  **deja de producir**. `recall=0` en **7/15** del baseline y **10/15** del kb_rag. No razona peor: no
  responde. La decisión de congelarlo en ON queda respaldada por el mecanismo, no solo por la media.
- **`deepseek-r1:1.5b`** — el «±0» es más fuerte de lo que sugiere la media: comparados registro a registro,
  **los 15 son idénticos** (diferencia máxima `4.4e-07`, puro formato: 6 decimales del CSV re-puntuado frente
  a precisión completa del test). Su razonamiento **no altera ni una entidad** y cuesta 2,8×.

**Tres resultados NO sostienen un cambio de régimen:**

- **`gemma4:latest`** oscila entre **+0.066 (`fs-en`) y −0.051 (`fs-es`)**: el signo cambia entre condiciones
  del **mismo modelo**. Eso es ruido de N=15, no efecto.
- **`gemma4:31b`** hace lo mismo: −0.029 en baseline, +0.037 en RAG.
- **El tercer caso** presenta una anomalía sin explicar: con `think` apagado va **más lento**
  (×0.3, de 7 s a 25 s), lo que **contradice el modelo causal** del hallazgo (el razonamiento genera tokens;
  no puede acelerar). Además una mediana de 7 s es llamativamente rápida para su tamaño. Su +0.021 **no debe
  darse por bueno** hasta explicar ese dato. (El nombre del modelo se retiró al quedar fuera del estudio;
  la anomalía se conserva porque es una advertencia de método, no un resultado.)

**Contraste con el único caso sólido.** `qwen3:8b` se decidió sobre **N=120**, con **+4,2 pp** y `recall=0`
cayendo de **15 a 1**. Aquí no hay nada de esa magnitud ni de esa consistencia.

**Recomendación (aplicada): NO re-ejecutar el estudio oficial de los 4 modelos.** Además de apoyarse en
ruido, re-correr 4 y dejar `gpt-oss` en ON **mezclaría dos regímenes de *thinking*** en el estudio — un
segundo eje de inconsistencia, de la misma clase que las dos convenciones de puntuación que ya costó
unificar. El valor del experimento es **documental y ya está capturado**: queda evidenciado por qué
`gpt-oss:20b` conserva el razonamiento y por qué `qwen3:8b` no.

> **Regla operativa consolidada.** Un efecto solo se acepta si el signo del ΔF1 es **estable en todas las
> condiciones**, el **mecanismo** lo corrobora (`recall=0`, latencia) y la muestra lo soporta (con N=15,
> descartar |ΔF1| < 0.05). Reglas completas en `RECOMENDACIONES-EJECUCIONES-FUTURAS.md`.

### F46. Mojibake en el ground truth del corpus N=120 deprime el recall de TODOS los modelos
**Severidad: alta (sistémica).** Las entidades gold de `data/benchmark_balanced_120.json` tienen **mojibake**
(UTF-8 leído como Latin-1): `Emiliano GarcÃ­a-Page`, `JosÃ© Bono`, `AdministraciÃ³n`, etc.

**Evidencia (medida):**
- **283 de 1406** entidades gold (20 %) contienen mojibake.
- De ellas, **66 (4,7 % del gold total) son IRRECUPERABLES**: aun con extracción perfecta del modelo, el
  `fuzz.ratio` contra el gold con mojibake queda **< 85** (umbral) y no casa. Ej.: gold `GarcÃ­a` vs
  extraído `García` → ratio 77 → **NO MATCH**. Cadenas largas sí sobreviven (el mojibake es menor fracción).
- **Afecta a TODOS los modelos por igual** → recall subestimado ~4,7 % de piso en todo el estudio N=120.
- **`kleptotrace.json` (N=15) y `kleptotrace_augmented_30.json` (N=30): 0 mojibake** → P1, P4 y el re-run N=30
  **no** están afectados. Solo el corpus N=120.

> **Precisión sobre la métrica (2026-09-07, verificado contra `src/evaluator.py:35` y `:87`).** El umbral 85 se
> aplica a `rapidfuzz.fuzz.ratio`, que **no** es una similitud de *tokens*: coincide exactamente con
> `Indel.normalized_similarity × 100`. La distancia de Indel es una variante de Levenshtein que solo admite
> **inserciones y supresiones** (no sustituciones), opera sobre **caracteres** y se normaliza como
> `100 × (1 − d / (|a| + |b|))`; el evaluador compara ambas cadenas en minúsculas. De ahí que
> `GarcÃ­a`/`García` dé **76,9** (< 85 → no casa) y `Emiliano GarcÃ­a-Page`/`Emiliano García-Page` dé **92,7**
> (≥ 85 → casa): la penalización es proporcional a la longitud, que es justamente lo que explica el
> «cadenas largas sí sobreviven» del punto anterior. Comprobado con `rapidfuzz 3.14.5` del `venv` del repo.
> **Las cifras de este hallazgo no cambian.**

**Causa raíz:** el JSON del corpus almacena los nombres con codificación corrupta (bytes UTF-8 reinterpretados
como Latin-1 al generarse/guardarse).

> **Verificación del equipo principal (2026-09-07 16:35).** Confirmadas las cifras: 1 406 entidades gold,
> 283 con mojibake (20,1 %), 66 irrecuperables a umbral 85 (4,7 %); `kleptotrace.json` y
> `kleptotrace_augmented_30.json` limpios. **Matizado el alcance en §F48:** el mojibake está también en el
> texto de entrada (87 % de los artículos) y de forma coherente con el gold, de modo que **el sesgo no es
> uniforme entre modelos** —premia la transcripción literal y penaliza la normalización— y **sí podría alterar
> el ranking**. La estimación de «~4,7 % de piso uniforme» queda sustituida por la de §F48.

**Impacto y decisión.** Corregir el gold (`s.encode('latin-1').decode('utf-8')`) elevaría el recall real de
todos los modelos N=120. Pero re-puntuar exige **re-inferir**: las extracciones crudas por registro no se
persistieron (solo `tp/fp/fn`), así que el matching no se puede rehacer sobre datos guardados. Es, por tanto,
una decisión de **re-ejecución del estudio N=120** con el gold corregido — a criterio del autor. Mientras no
se corrija, todas las cifras de recall/F1 de N=120 llevan este sesgo a la baja, uniforme entre modelos (no
altera el ranking relativo, sí los valores absolutos).

---

### F47. Los fallos de `gpt-oss:20b` son degeneración por repetición, no incapacidad del modelo

> **Nota de numeración (2026-09-07):** este hallazgo se registró como «F46» y se renumeró a **F47** al
> detectarse que el equipo remoto había publicado su propio §F46 (mojibake en el gold) minutos antes.

**Estado:** diagnóstico encargado al equipo remoto (`ENCARGO-REMOTO-GPTOSS-20260907.md`, `CURRENT-TASKS §3.bis.13`).

`gpt-oss:20b` acumula **76 filas con `recall=0`** de 240 (27/120 en baseline, 49/120 en kb_rag) y es el único
modelo del estudio con un ΔRAG fuertemente negativo (**−0.097**). La lectura inmediata —«el RAG le perjudica»—
**no se sostiene** al cruzar `parse_method` con la latencia:

| Indicio | Dato |
|:---|:---|
| `parse_method` de los fallos | **67 de 76 son `fallback`** |
| Avisos del arnés | **69 × «Failed to parse JSON from raw response»** |
| Extracción resultante | **45 de las 49 de kb_rag** en `tp=0, fp=0` (vacía del todo) |
| Latencia | fallos **838 s** vs aciertos **854 s** (mediana), volumen de tokens equivalente |

La latencia normal y el volumen de tokens **descartan el rechazo de infraestructura**: el modelo trabaja y
produce salida. Es el otro caso de la regla —*latencia alta con contenido inservible = el arnés pierde la
respuesta*—, la misma familia que §F40-F41.

**Mecanismo observado.** Las dos respuestas crudas que el log conserva legibles muestran la misma forma: el
modelo **extrae entidades correctas** y después **entra en un bucle de repetición** que deja el JSON sin cerrar.

```
{"Persons": ["Chirac", "Aznar", "José María Aznar", way, way, way, way, …
{"Persons": ["Corín Tellado", "Miguel de Cervantes", "Luis Sepúlveda", …  [Note: This  [Note: This  …
```

El parser falla, cae al *fallback*, y el *fallback* devuelve vacío — **descartando entidades que estaban bien
extraídas**.

> **Límite de esta evidencia:** el log **trunca** las respuestas, de modo que solo hay **dos muestras
> legibles**. No se puede afirmar en qué proporción de los 69 casos ocurre. Medirlo es el objeto del encargo.

**Vías de corrección, por orden de preferencia:** (1) un **parser tolerante** que rescate el prefijo válido de
un JSON sin cerrar —recuperaría entidades **sin volver a inferir**, como hizo el re-puntaje con el bug de
*scoring*—; (2) `repeat_penalty` por encima del 1.1 por defecto.

> **Regla operativa.** Un ΔRAG anómalo **no es un resultado hasta descartar el arnés**. Antes de interpretarlo,
> cruzar `parse_method` con la latencia: si los fallos tardan lo mismo que los aciertos, el modelo respondió y
> el problema está en la lectura, no en la extracción.

**Corolario — RESUELTO por el equipo remoto (§F46).** La sospecha era correcta y el alcance mayor: el mojibake
no está en el fichero de log sino **en el *ground truth* del corpus N=120**, y afecta a todos los modelos.
Verificado de forma independiente: 283 de 1 406 entidades gold (20,1 %) y 66 irrecuperables (4,7 %). Detalle en §F46.

**Nota original —** El log muestra `CorÃ­n Tellado` y `José MarÃ­a`: UTF-8 leído como
Latin-1. **Si la doble codificación alcanzara al texto que se compara con el *ground truth*, y no solo al
fichero de log, ningún nombre español con tilde casaría nunca — en todos los modelos del estudio.** Verificación
encargada al equipo remoto.

> **[Corrección 2026-09-07, contrastada con `src/evaluator.py`.]** La conjetura era correcta en su dirección pero
> **no en su forma absoluta**: `fuzz.ratio` normaliza por la longitud total, así que el mojibake solo hunde por
> debajo de 85 a las cadenas **cortas** (`GarcÃ­a`/`García` = 76,9; `JosÃ© Bono`/`José Bono` = 84,2), mientras
> que las largas siguen casando (`Emiliano GarcÃ­a-Page`/`Emiliano García-Page` = 92,7). La medición de §F46
> lo confirma: 283 entidades gold con mojibake, de las que **66** —no todas— resultan irrecuperables.

---

### F48. El mojibake es *consistente* entre texto y gold: no hay sesgo uniforme, hay un sesgo que depende del modelo

**Registrado:** 2026-09-07 16:35 (UTC−3) · **Autor:** equipo principal · **Amplía y corrige el alcance de §F46.**

**Qué es el mojibake aquí.** El corpus almacena bytes UTF-8 reinterpretados como Latin-1. La cadena guardada es
la **corrupta**; la forma **correcta** es la que se obtiene al repararla:

| Forma **corrupta** (la que está en el fichero) | Forma **correcta** (la real) |
|:---|:---|
| `JosÃ© Bono` | **`José Bono`** |
| `Emiliano GarcÃ­a-Page` | **`Emiliano García-Page`** |
| `MarÃ­a MuÃ±oz` | **`María Muñoz`** |
| `AdministraciÃ³n` | **`Administración`** |

Reparación: `s.encode('latin-1').decode('utf-8')`. **La dirección importa:** `JosÃ© Bono` es el dato dañado y
`José Bono` es el nombre real. En cualquier texto del proyecto debe escribirse en ese orden para no invertir el
sentido.

**Lo que §F46 no midió: el texto de entrada también está corrupto.**

| Comprobación (medida sobre `data/benchmark_balanced_120.json`) | Resultado |
|:---|:---|
| Registros con mojibake en el campo `text` | **104 de 120 (87 %)** |
| Registros con mojibake en `title` | 0 |
| Entidades gold corruptas que aparecen **tal cual** en el texto | **283 de 283** |
| Entidades gold corruptas que aparecen **corregidas** en el texto | **0** |

**Consecuencia — el corpus es internamente coherente.** El modelo *lee* `Emiliano GarcÃ­a-Page` y el gold
*espera* `Emiliano GarcÃ­a-Page`. Un modelo que **copia literalmente casa igual**; el que **normaliza** el texto
a español correcto produce `Emiliano García-Page` y **falla la comparación**. El mojibake no impone un suelo
uniforme: **premia la transcripción literal y penaliza la normalización ortográfica**.

**Evidencia de que el efecto no es uniforme.** F1 medio sobre los 88 registros con mojibake frente a los 31 sin
él, por modelo (mismos registros para todos):

| Modelo | Δ (con mojibake − sin) |
|:---|--:|
| `gemma4:latest_baseline` | **−0.0695** |
| `gemma4:12b-mlx_baseline` | −0.0422 |
| `gemma4:31b-mlx_baseline` | −0.0395 |
| `llama3.1:8b_kb_rag` | −0.0004 |
| `mistral-nemo:latest_kb_rag` | +0.0122 |
| `gpt-oss:20b_kb_rag` | **+0.0914** |

**Un rango de ~16 puntos entre modelos.** Si el efecto fuera un suelo uniforme, todos los modelos se
desplazarían por igual sobre los mismos registros. No lo hacen.

> **Cautela metodológica.** Los registros con mojibake podrían ser además más largos o difíciles, lo que
> confundiría la magnitud absoluta de cada Δ. Pero la **dispersión entre modelos sobre los mismos registros**
> no se explica por la dificultad: esa es la evidencia de que la interacción es específica de cada modelo.
> La fila de `gpt-oss` es la menos fiable, porque sus cifras están dominadas por el artefacto de §F47.

**Corrección a lo publicado.** El informe declaraba en §5.3.5 que el sesgo era «uniforme entre modelos» y que
«no altera el orden relativo». **Eso no está respaldado** y se ha corregido: el efecto es específico de cada
modelo y **podría alterar el ranking**.

**Cómo se arregla bien.** No basta con reparar el gold: eso invertiría la injusticia, penalizando al modelo que
copia literalmente. La solución correcta es **normalizar ambos lados en el momento de comparar** —aplicar la
reparación al gold **y** a la entidad extraída antes del *fuzzy matching*—, con lo que `JosÃ© Bono` y
`José Bono` convergen a la misma forma y el resultado deja de depender de la codificación. Son ~10 líneas en
`src/evaluator.py`.

**Por qué no se puede aplicar retroactivamente.** El *matching* ocurre en tiempo de inferencia y **las
extracciones crudas por registro no se persistieron** (solo `tp/fp/fn` y un `error_taxonomy` parcial). No hay
forma de re-puntuar sobre lo guardado, como sí se pudo con el bug del *scorer*. Requiere re-inferir.

> **Regla operativa.** Antes de declarar que un defecto del corpus introduce un sesgo uniforme, **comprobar si
> el defecto está también en la entrada**. Un corpus corrupto de forma coherente no penaliza a todos por igual:
> penaliza a quien lo corrige.

---

### F49. Dos defectos residuales del evaluador, detectados en la auditoría de consistencia

**Registrado:** 2026-09-07 21:00 (UTC−3) · Hallados por auditoría automatizada y **verificados contra el
código** por el equipo principal. **Ninguno afecta a las cifras publicadas**, pero ambos requieren decisión.

**1. El *recall* por tipo de entidad puede superar 1,0.** En `src/evaluator.py:97` se calcula
`recall = tp / len(gt_list)`, donde `tp` cuenta las entidades **extraídas** que lograron emparejar, mientras
que `fn` se deriva de `len(gt_list) - len(matched_gts)`. Si dos entidades extraídas emparejan con la **misma**
entidad de referencia, `tp` vale 2 sobre una lista de referencia de 1, y el *recall* de ese tipo sale 2,0.

> **Por qué no contamina los resultados.** Las cifras del estudio proceden del bloque `overall`
> (`evaluator.py:131`), que sí calcula `tp / (tp + fn)` y es inmune al problema. El defecto afecta únicamente
> al desglose por tipo de entidad, que no se reporta en el informe. Aun así, cualquier análisis futuro que use
> `metrics.per_type` heredaría el error.

**2. `oov_recall` conserva el valor por defecto 1,0** cuando no hay entidades fuera de vocabulario que medir
(`evaluator.py:147`), mientras que el resto del *scoring* pasó a 0,0 en la corrección del 2026-09-06. Es un
residuo de aquel arreglo: la misma convención que se consideró errónea para precisión y exhaustividad —premiar
la ausencia de datos con la puntuación máxima— sigue vigente en esta métrica.

> **Regla operativa.** Al corregir una convención de puntuación, revisar **todas** las métricas del módulo, no
> solo las que motivaron el cambio. Una corrección parcial deja el mismo defecto vivo en un rincón.

---

### F50. El sesgo del emparejamiento no es unidireccional, y el umbral de alucinación se descarta en silencio

**Registrado:** 2026-09-07 21:50 (UTC−3) · Hallado por la auditoría automatizada de consistencia y
**verificado de forma independiente** por el equipo principal.

**1. El recuento de aciertos infla la exhaustividad en una fracción de registros.** El informe afirmaba que
los dos límites conocidos del emparejamiento difuso —sensibilidad al orden y penalización de las omisiones—
empujaban las cifras «a la baja, nunca al alza», y concluía que el desempeño reportado era conservador. **La
segunda mitad de esa frase era falsa.** En `evaluator.py:84-94` el bucle recorre las entidades **extraídas** e
incrementa un acierto por cada una que casa, mientras las omisiones se derivan de las entidades **de
referencia** no cubiertas (`fn = len(gt_list) − len(matched_gts)`). Numerador y denominador no están en la
misma unidad: dos menciones que casan con la misma entidad de referencia suman dos aciertos frente a una sola
entidad cubierta.

Se midió de dos formas. La estricta cuenta las celdas cuya exhaustividad **supera 1,0**, que son los casos
extremos: **258 de 28 113 (0,9 %)**. La correcta recalcula, para cada registro, la exhaustividad real como
entidades de referencia cubiertas sobre el total, y la compara con la publicada:

| Corrida | Registros inflados | Δ medio | Δ máximo |
|:---|:---:|:---:|:---:|
| `benchmark_n120_REMOTO` | 61 de 1 680 (3,6 %) | +0,088 | +0,208 |
| `nemotron_rerun_n120_REMOTO` | 14 de 240 (5,8 %) | +0,133 | +0,500 |
| `qwen3_nothink_n120_REMOTO` | 9 de 240 (3,8 %) | +0,025 | +0,076 |

Entre un 2 % y un 6 % de los registros según la corrida, por tanto. El efecto neto sigue siendo conservador,
pero la afirmación absoluta no se sostenía y se ha acotado en §3.3 del informe con estas cifras.

> **Matiz metodológico sobre la propia medición.** La primera cuenta —celdas con exhaustividad mayor que uno—
> subestima el problema en un factor de tres o cuatro, porque solo detecta los casos donde la inflación es tan
> grande que rompe el techo de la métrica. Medir un sesgo por sus manifestaciones extremas es una trampa
> frecuente: hay que recalcular el valor correcto y compararlo, no buscar valores imposibles.

**2. El umbral de la tasa de alucinación no es configurable en la práctica.** `evaluate_single_record` recibe
el umbral configurado —85— y lo propaga a las demás funciones, pero invoca
`calculate_hallucination_rate(extracted, source_text)` **sin pasarlo** (`evaluator.py:302`), de modo que la
métrica usa siempre su valor por defecto de **70** y el parámetro configurado se descarta en silencio. No es
un error en los resultados —70 es un umbral razonable para detectar invención y así se documenta ahora en el
informe—, pero sí una discrepancia entre lo que la configuración promete y lo que el código hace.

> **Regla operativa.** Una afirmación sobre la *dirección* de un sesgo es más fuerte que una sobre su
> magnitud, y por eso exige más evidencia. Antes de escribir «nunca al alza», hay que buscar activamente el
> mecanismo que podría empujar en sentido contrario.


---

### F51. Cuatro referencias de la bibliografía no corresponden a ninguna obra existente

**Registrado:** 2026-09-08 01:50 (UTC−3) · Hallado por verificación automatizada contra internet de las veinte
referencias, con **confirmación independiente** del equipo principal en el caso más claro.
**Gravedad: máxima. Es un problema de integridad académica, no de formato.**

| Ref. | Declarado en el informe | Resultado de la verificación |
|:---|:---|:---|
| **[7]** | A. García y M. López, «Evaluating BERT and Transformers for NER in Spanish», IberLEF, 2021 | **No encontrada.** Sin resultados por título, por autores ni por combinaciones |
| **[9]** | M. Chang, J. Kim y S. Park, «RAG for Financial Document Analysis», *Journal of Financial Data Science* | **No encontrada** |
| **[10]** | J. Smith, L. Johnson y R. Davis, «CRF for NER in Financial Texts», *ACM Transactions* | **No encontrada** |
| **[15]** | M. Min et al., «FiNER: Financial Named Entity Recognition Dataset and Benchmark», ACL, 2023 | **No encontrada.** Confirmado a mano: existe *FiNER: Financial **Numeric** Entity Recognition for XBRL Tagging*, ACL **2022**, de Loukas et al., y *FiNER-ORD* de Shah et al. Título, año y autores difieren |

**Por qué importa más allá del formato.** Dos de esas cuatro sostienen una afirmación del estado del arte: la
línea que cita [2], [7] y [15] para respaldar que el NER en español alcanza «entre 88 % y 91 % de F1 en
*benchmarks* académicos». La verificación de [2] señala que esa cifra no puede proceder de BERT, que no evalúa
NER en español, de modo que **la carga probatoria recaía enteramente en dos referencias inexistentes**.

**Señal de alerta que estaba a la vista.** Las cuatro comparten un rasgo: nombres de autor genéricos —«J.
Smith, L. Johnson, R. Davis»; «A. García y M. López»— y publicaciones designadas de forma vaga, sin volumen ni
páginas. Es la firma característica de una cita fabricada, y era detectable sin salir del documento.

**Qué NO se ha hecho.** No se ha eliminado ninguna entrada ni se ha sustituido por otra. Retirar una referencia
cambia lo que el texto afirma, y sustituirla exige comprobar que la obra nueva dice lo mismo. **Es decisión del
autor**, y está registrada en `TODO-INFORME-FINAL.md`.

> **Regla operativa.** Toda bibliografía heredada debe verificarse contra la fuente primaria antes de defender
> el trabajo. Este proyecto ya había sufrido una atribución falsa —una cifra de mercado adjudicada a KPMG— y no
> se extendió la sospecha al resto del aparato bibliográfico. Un solo caso detectado obliga a auditar el
> conjunto.

---

## §F52 — Resolución de §F51: las cuatro citas ficticias, sustituidas por obras reales verificadas

**Fecha:** 2026-09-08. **Estado:** aplicado en el Markdown canónico (commit `f30d8d5`).

Las cuatro entradas inexistentes se sustituyeron por obras reales, cada una comprobada abriendo su ficha
oficial, no solo buscándola:

| Ficticia | Obra real que la sustituye | Comprobación |
|:---|:---|:---|
| [7] García y López, IberLEF 2021 | Cañete et al., *Spanish Pre-Trained BERT Model and Evaluation Data*, PML4DC @ ICLR 2020 | `arxiv.org/abs/2308.02976` y el README oficial de `dccuchile/beto` |
| [9] Chang, Kim y Park, *JFDS* 2024 | Islam et al., *FinanceBench*, arXiv:2311.11944 | resumen oficial en arXiv |
| [10] Smith, Johnson y Davis, *ACM Trans.* 2019 | Salinas Alvarado, Verspoor y Baldwin, ALTA 2015, pp. 84-90 | `aclanthology.org/U15-1010/` |
| [15] Min et al., FiNER, ACL 2023 | Loukas et al., *FiNER: Financial **Numeric** Entity Recognition for XBRL Tagging*, ACL 2022, pp. 4419-4431 | `aclanthology.org/2022.acl-long.303/` |

**Lo que reveló la sustitución.** Al buscar las obras reales apareció un daño mayor que la simple falta de
respaldo: **tres de las cinco filas de la Tabla 1 declaraban cifras que nadie ha publicado.**

- La fila de FiNER-139 atribuía **91 %** a un «BERT fine-tuned» en la nube. El artículo real reporta **82,1 %
  de micro-F1** con SEC-BERT-SHAPE, un modelo abierto y ejecutable en local. Y la tarea no es NER de personas
  y organizaciones: es etiquetado de **magnitudes numéricas** según la taxonomía XBRL.
- La fila de español atribuía **88 %** a XLM-R sobre CoNLL-ES. Ninguna fuente publica esa combinación. Las
  cifras reales son BETO 88,43 %, mBERT 87,38 % y XLM-R large 89,72 %. Es decir: el 88 % existe, pero
  corresponde a **otro modelo**.
- La fila de RAG atribuía **83 %** a GPT-4 con RAG sobre documentos bancarios. La cifra real publicada es
  **50 %** de exactitud con índice por documento, y **19 %** con índice compartido: el propio resumen de
  FinanceBench dice que GPT-4-Turbo con recuperación «falla o rehúsa el 81 % de las preguntas».
- Se corrigió además la fila de BloombergGPT, que declaraba arquitectura *GPT-J* y «85 %+», cuando el
  artículo declara **BLOOM** y reporta F1 de NER entre **53,6 y 75,5**.

**Defecto de diseño de la tabla, no solo de sus datos.** La columna se titulaba «F1» y alojaba métricas de
tareas distintas —F1 de NER, micro-F1 de etiquetado XBRL, exactitud de respuesta— como si fueran homogéneas.
Se renombró a «Desempeño publicado» y se añadió una glosa que advierte que las filas no son directamente
comparables. Ninguna fila se eliminó: todas se reescribieron con datos reales.

**Aprendizaje.** Una cita fabricada no es solo una referencia que falta: es una cifra que entró en una tabla
comparativa sin que nadie pudiera contrastarla, y que sostenía la tesis de que existe una brecha. La brecha
sigue existiendo con los datos reales —de hecho se ensancha, porque el RAG en la nube rinde 50 % y no 83 %—
pero eso es una conclusión afortunada, no un mérito del método. **El orden correcto es verificar primero y
concluir después.**

> **Regla operativa que se añade.** Ninguna cifra entra en una tabla comparativa sin que su fuente esté
> abierta y leída, y ninguna columna agrupa métricas de tareas distintas bajo un mismo encabezado.

---

## §F53 — CRÍTICO: `Locations` genera el 66 % de los falsos positivos del estudio y su gold está vacío

**Fecha:** 2026-09-08. **Origen:** segunda pasada de revisión global; tres auditores independientes lo
señalaron por separado. **Verificado por medición propia sobre los 87 grupos modelo-corrida.**

**El defecto.** Los cuatro prompts del sistema ordenan al modelo extraer **tres** categorías —`Persons`,
`Organizations` y `Locations`—, el evaluador puntúa las tres (`evaluator.py:45` y `:211`), pero **ninguno de
los corpus anota localizaciones**. En `data_loader.py:120`, `adapt_kleptotrace_record` fija
`"Locations": []`, y la comprobación directa sobre `benchmark_balanced_120.json` confirma que **los 120
registros llevan solo `name_entities` y `organizations`**: cero localizaciones en el gold, también en la
parte de CoNLL-2002.

La consecuencia es mecánica: **toda localización que el modelo extrae es un falso positivo**, y no existe
ninguna forma de acertar en esa categoría. No es un sesgo de medición, es una penalización estructural.

**Magnitud.** Sobre el conjunto del estudio, **31 709 de los 47 957 falsos positivos —el 66,1 %— proceden de
`Locations`**. Ejemplo de un solo registro de `qwen3_nothink_n120_REMOTO`: `Persons` F1 0,800 y
`Organizations` F1 0,400, pero `Locations` aporta `tp=0, fp=10, fn=0`, y el F1 global cae a 0,500 cuando sin
esa categoría sería 0,667.

**Efecto sobre las cifras publicadas.** Recalculando los 87 grupos sin la categoría, el F1 sube en todos los
casos, pero **de forma muy desigual**, entre +0,5 y +15 puntos:

| Corrida y grupo | F1 publicado | F1 sin `Locations` | Delta |
|:---|---:|---:|---:|
| `gemma4:31b-cloud` (N=120) | 66,46 % | 81,45 % | +14,99 pp |
| `gemma4:31b-mlx` baseline (N=120) | 63,32 % | 77,77 % | +14,45 pp |
| `gemma4:31b` (N=15) | 71,14 % | 85,84 % | +14,71 pp |
| `gemma4:31b-mlx` (N=30) | 80,51 % | 90,91 % | +10,40 pp |
| `deepseek-r1:1.5b` baseline (N=120) | 24,82 % | 28,05 % | +3,23 pp |
| `nemotron-mini:4b` baseline (N=120) | 21,65 % | 25,91 % | +4,26 pp |
| `minimax-m3:cloud` baseline (N=120) | 14,65 % | 15,51 % | +0,86 pp |

**Por qué importa más de lo que parece.** La corrección no es un desplazamiento uniforme que dejaría intactas
las comparaciones: los modelos capaces ganan unos 14 puntos y los débiles unos 3, de modo que **el orden
cambia**. En la corrida `benchmark_balanced_120_20260824_173036`, `gemma:latest` (47,91 %) figura por encima
de `nuextract:latest` (47,50 %); sin `Locations` el orden se invierte, 57,41 % frente a 55,38 %. Todo lo que
descansa sobre esas comparaciones —el ANOVA, el Tukey HSD, los rankings y las conclusiones— queda afectado.

**El lado favorable, que conviene no exagerar.** La corrección **rescata la hipótesis sobre datos realmente
en español**. El umbral declarado es F1 ≥ 70 % en español, y sobre el corpus N=120 —105 de cuyos 120
artículos están en español— `gemma4:31b-mlx` pasa de 63,32 % a **77,77 %**, superándolo con holgura. Esto
importa porque el otro hallazgo grave de la misma revisión (§F54) es que los corpus N=15 y N=30, sobre los
que el informe apoyaba el cumplimiento del umbral, **están íntegramente en inglés**.

**Las tres salidas posibles, para decisión del autor.** No son equivalentes y ninguna es gratuita:

1. **Excluir `Locations` de la puntuación** y volver a agregar desde los `detailed_results.json` ya
   existentes. No requiere reejecutar ningún modelo, porque el desglose `per_type` está guardado. Es la vía
   barata, y es defendible: se mide lo que el corpus anota.
2. **Retirar `Locations` de los prompts** y reejecutar. Metodológicamente la más limpia, porque alinea lo que
   se pide con lo que se mide, pero exige repetir el barrido completo.
3. **Declararlo como limitación** y dejar las cifras. Es la opción más débil: un tribunal que abra un
   `detailed_results.json` verá `tp=0, fp=10` en una categoría y preguntará por qué se puntúa algo que no se
   anota.

La opción 1 es la recomendable: reaprovecha todo el cómputo ya hecho y corrige la medición de raíz.

> **Corrección del criterio de detección, 2026-09-08.** La primera versión de esta regla decía que el
> indicador era el `fn` agregado por categoría, y **estaba mal**. El equipo remoto lo detectó al implementar
> la comprobación (commit `e6a3b8f`): `fn == 0` con `tp > 0` es **exhaustividad perfecta**, no un defecto, y
> ese criterio invalidaría corridas legítimas. La señal correcta es **`tp + fn == 0` con `fp > 0`**, es decir
> que la categoría no tenga ni una entidad de referencia en todo el corpus y aun así acumule falsos
> positivos. Corregido en `CLAUDE.md`, en `LEARNING.md §L44`, en `doc/prompts/03-integridad-metrica.md` y en
> el encargo al equipo remoto.
>
> **Regla operativa.** Lo que el prompt pide y lo que el corpus anota tienen que coincidir. Toda categoría
> que se puntúe debe existir en la anotación de referencia; si no existe, o se anota o se excluye del cálculo,
> pero nunca se deja puntuando contra el vacío.

---

## §F54 — Los dos corpus del dominio están en inglés, no en español

**Fecha:** 2026-09-08. **Origen:** tres auditores de la segunda pasada. **Verificado por medición propia.**

El resumen, el abstract, la hipótesis y el objetivo específico 2 declaraban validación sobre noticias «en
español». La medición sobre los ficheros versionados dice otra cosa:

| Corpus | Registros | Español | Inglés |
|:---|---:|---:|---:|
| `kleptotrace.json` (N=15, Gold Standard) | 15 | **0** | 15 |
| `kleptotrace_augmented_30.json` (N=30, validación estadística) | 30 | **0** | 30 |
| `benchmark_balanced_120.json` (N=120, estudio principal) | 120 | 105 | 15 |

El primer artículo del N=15 empieza «The Justice Department announced today…» y el del N=30 «The US
Department of the Treasury's OFAC announced sanctions against Alexey Shevchenko…». El único corpus con
material en español es el N=120, y lo es porque 105 de sus 120 artículos provienen de CoNLL-2002.

**Por qué era grave.** El umbral de la hipótesis, F1 ≥ 70 % en español, se acreditaba precisamente sobre los
dos corpus ingleses: el 80,57 % del N=30 y el 79 % del N=15. Sobre el corpus español el mejor local daba
59,25 %, muy por debajo. Es decir: **la hipótesis estaba respaldada por el material que no le correspondía.**

**Cómo se resuelve.** Corregido junto con §F53, porque los dos hallazgos se compensan. Con la medición
restringida a las categorías que el corpus anota, el mejor local sobre el N=120 alcanza **76,85 %** y supera
el umbral sobre material realmente en español. La hipótesis queda acreditada, pero por otra vía.

**Un residuo que sigue abierto.** El Anexo F transcribe un prompt generador redactado en español cuya salida
versionada está en inglés. O el prompt transcrito no es el que se ejecutó, o el corpus versionado no es el
que ese prompt generó. Requiere criterio del autor: no se puede decidir desde los artefactos.

**Y una explicación causal que estaba invertida.** §6.1 atribuía la mejora del prompt en español a que
«comparte idioma con el corpus». No puede ser: el prompt en español ganó **sobre texto inglés**. El hallazgo
empírico sobrevive e incluso resulta más interesante, porque sugiere que el efecto no es de concordancia de
idioma sino de calidad de la instrucción; pero el mecanismo declarado era falso.

---

## §F55 — El efecto del prompt en español no replica: hay tres corridas y el informe citaba una

**Fecha:** 2026-09-08. **Origen:** un solo auditor de la segunda pasada; el orquestador lo verificó y lo
ascendió a bloqueante precisamente por venir de una sola fuente y contradecir un titular del resumen.

El informe presentaba +10,40 puntos de F1 por redactar el prompt en español con ejemplos *few-shot*. Existen
**tres corridas del mismo experimento** y solo se citaba la más favorable:

| Corrida | Corpus | zs-en | fs-es | Diferencia |
|:---|:---|---:|---:|---:|
| `ablacion_n15_REMOTO` (la citada) | N=15 | 67,52 % | 77,92 % | **+10,40 pp** |
| `kleptotrace_20260727_110454` | N=15 | 66,76 % | 69,87 % | +3,11 pp |
| `benchmark_balanced_120_20260825_071207` | N=120 | 54,46 % | 54,02 % | **−0,43 pp** |

La tercera, sobre el corpus ocho veces mayor, da **ANOVA F=0,1451 con p=0,9328** y t pareada p=0,7019: el
efecto es **nulo**. Y las dos primeras usan el mismo modelo, el mismo corpus, semilla 42 y temperatura 0,1,
de modo que la diferencia entre +10,40 y +3,11 no se explica por la configuración.

**Matiz de historia del proyecto que conviene no confundir.** Una auditoría anterior cuestionó la ablación y
fue refutada; aquella refutación acreditó que las cifras publicadas verifican contra `ablacion_n15_REMOTO`, y
eso **sigue siendo cierto**. Lo que nunca se declaró es que hubiera una selección entre tres corridas.

**Resolución (decisión del autor).** Declarar las tres, conservando las cifras de N=15 como manda la política
aditiva, y reformular la conclusión 2 como **tendencia no replicada**. Ya aplicado en el resumen y el
abstract, que ahora atribuyen el +10,4 al corpus de quince artículos y declaran que no replica sobre el mayor.

> **Regla operativa.** Cuando existan varias corridas del mismo experimento, el informe declara **todas** y
> explica cuál se toma como referencia y por qué. Citar la más favorable sin mencionar las demás es
> indistinguible de seleccionar el resultado, aunque no haya intención de hacerlo.

---

## §F56 — Localización de las entidades, no solo del texto: por qué el prompt en español ayudó sobre texto inglés

**Fecha:** 2026-09-08. **Origen:** pregunta del autor —«¿será que a pesar de declararse en inglés existen
entidades en español en este dataset?»—. **Analizado y medido.** La intuición era acertada en su premisa y el
resultado explica el hallazgo mejor de lo que lo hacía el informe.

### Lo que dicen los datos

| Corpus | Personas | De aspecto ibérico | Organizaciones | De aspecto ibérico |
|:---|---:|---:|---:|---:|
| N=15 Kleptotrace | 84 | **12 (14 %)** | 128 | 3 (2 %) |
| N=30 sintético | 36 | 1 (3 %) | 69 | 0 (0 %) |
| N=120 mixto | 594 | **263 (44 %)** | 812 | 198 (24 %) |

En el N=15 el texto es íntegramente inglés, pero **sí hay una minoría de entidades ibéricas**, y casi todas
proceden del caso de corrupción angoleño, de modo que son **portuguesas** antes que españolas: `Isabel dos
Santos`, `José Eduardo dos Santos`, `Hélder Pitta Grós`, `Mario Leite da Silva`, `Nuno Ribeiro da Cunha`,
`Paula Oliveira`, más `Banco de Fomento Angola` y `Petroleos de Venezuela S.A.`. Son precisamente los nombres
con partículas (`dos`, `da`, `de`) y acentos que un modelo instruido en español segmenta mejor: donde un
tokenizador anglocéntrico parte `Isabel dos Santos` en dos entidades, uno sensible a la partícula la mantiene
unida.

### Por qué esto reformula el hallazgo

El informe atribuía la mejora del prompt en español a que «los ejemplos rinden en el idioma del corpus». Eso
no puede ser: el corpus está en inglés. La explicación que los datos soportan es distinta y más precisa: la
instrucción en español no ayuda a leer el texto, **ayuda a delimitar la minoría de nombres ibéricos**. Y esa
explicación predice un efecto **modesto**, proporcional a ese 14 %, no los +10,40 puntos declarados — que es
justamente lo que se observa, porque **la corrida que replica da +3,11** (§F55).

### Y explica por qué el efecto se anula en el corpus español

Queda la paradoja aparente: si la ventaja viene de manejar nombres ibéricos, el N=120 —con 44 % de personas
hispanas— debería beneficiarse más, y en cambio el efecto se anula (−0,43 puntos, p = 0,9328). La respuesta
está en el *mojibake*: en ese corpus las entidades de referencia están corrompidas (`JosÃ© Bono` por
**José Bono**), de modo que **la competencia en español se convierte en una desventaja**. Un modelo que
normaliza la ortografía escribe el nombre bien y falla el cotejo; uno que transcribe los bytes literalmente,
acierta.

Esto no es especulación: la medición del efecto del *mojibake* (§F57) muestra que **19 de 24 grupos puntúan
mejor en los artículos cuyas entidades de referencia están corruptas**. El corpus premia la copia literal.
Los dos efectos se cancelan, y de ahí el cero.

### Síntesis defendible

- **N=15**: texto inglés, 14 % de entidades ibéricas, codificación limpia → beneficio modesto y replicable.
- **N=120**: texto español, 44 % de entidades hispanas, **pero referencia corrompida** → el beneficio
  lingüístico se anula contra la penalización por normalizar.

> **Regla operativa.** En una evaluación de NER, la lengua que importa no es solo la del texto: es la de las
> **entidades**, porque son ellas las que se segmentan y se cotejan. Un corpus puede estar redactado en un
> idioma y poblado de nombres de otro, y esa combinación cambia qué modelo gana. Caracterizar el corpus exige
> medir ambas cosas por separado.

---

## §F57 — La taxonomía de errores describía fenómenos que los artefactos no contienen

**Fecha:** 2026-09-08. **Origen:** un auditor de la segunda pasada; **verificado y ampliado por medición
propia** sobre los 17 ficheros de resultados detallados.

### Los dos ejemplos ilustrativos no existían

§5.4 ilustraba los errores de límite con «Isabel dos Santos, hija del expresidente» y la confusión de tipo con
«Sonangol» etiquetada como lugar. Recuento sobre todos los `detailed_results.json`:

| Cadena buscada | Ocurrencias |
|:---|---:|
| `Isabel dos Santos, hija` | **0** |
| `Sonangol` | **0** |
| `Isabel dos Santos` (forma limpia) | 307 |

Los dos ejemplos eran verosímiles y estaban inventados. La entidad existe en el corpus, pero el modelo nunca
la extrajo con la aposición que el informe le atribuía.

### Y la categoría no significaba lo que el informe decía

Lo más relevante no es que faltaran los ejemplos, sino que **la categoría agrupa tres fenómenos distintos** y
el informe describía solo uno. Un «error de límite» es todo emparejamiento con similitud entre 50 y 85. Los
casos más frecuentes, medidos:

| Extraído | Referencia | Similitud | Qué es en realidad |
|:---|:---|---:|:---|
| `José María Aznar` | `JosÃ© MarÃ­a Aznar` | 82,4 | **el modelo acierta y la referencia está corrupta** |
| `EFE` | `EFECOM` | 66,7 | variante de sigla de la misma agencia |
| `Mario Delgado` | `Corín Tellado` | 51,9 | **personas distintas sin relación alguna** |
| `Peter Twehway` | `Bill Twehway` | 64,0 | personas distintas con el mismo apellido |

De modo que el recuento de esta categoría **no mide la habilidad del modelo para delimitar entidades**: mide
con qué frecuencia el cotejo difuso cae en su franja intermedia, y una parte apreciable de esos casos la
provoca el *mojibake* del corpus. La afirmación «los errores de límite son los más frecuentes» era cierta como
recuento y engañosa como interpretación.

La **confusión de tipo** resultó igualmente homogénea y explicable: los casos dominantes son `Estados Unidos`,
`Francia`, `Israel` y `Valencia` extraídos como localización cuando CoNLL-2002 los anota como organización,
por referirse al Estado o al club y no al territorio. Es una divergencia de convención de anotación, no un
fallo de comprensión.

### Las cifras de alucinación tampoco correspondían

> **CORRECCIÓN de esta misma sección, 2026-09-08.** La primera redacción de este hallazgo situaba a
> `nuextract:latest` como el peor alucinador del estudio, con 43,31 % a 50,02 %. **Era un error mío**:
> `nuextract:latest` está **excluido del estudio** por decisión del autor, junto con `minimax-m3` y
> `gemini-3.1-flash-lite`, y el Anexo E lo declara. Citar su cifra como resultado del trabajo es exactamente
> el defecto que este documento persigue. Recalculado sobre los **sesenta y un grupos de los modelos
> incluidos**: el rango va de **0,00 %** a **21,59 %**, veintiocho de ellos quedan por debajo del 1 %, y el
> peor es `deepseek-r1:1.5b` con 11,23 % a 21,59 %, seguido de `nemotron-mini:4b` con 7,14 % a 14,75 %. Es
> decir: **la afirmación original del informe era sustancialmente correcta** y mi corrección la empeoró. Lo
> que sí seguía siendo impreciso es el «superan el 13 %», porque la condición de extracción directa de
> `deepseek` da 11,23 %.


El informe declaraba «por debajo del 1 % en los modelos de mayor capacidad» y «superan el 13 % en
`deepseek-r1:1.5b`». Medido sobre los grupos de 120 registros:

- El rango real va de **0,00 %** —variantes alojadas de `gemma4:31b`— a **50,02 %**.
- **30 de 67 grupos** quedan por debajo del 1 %, de modo que esa parte se sostiene.
- **`nuextract:latest` es el peor, con 43,31 % a 50,02 %**, no `deepseek-r1:1.5b`, que va de 11,23 % en
  extracción directa a 21,59 % con recuperación por diccionario. Señalar a `deepseek` como el caso extremo
  ocultaba un modelo tres veces peor.
- Con un grupo al 50 %, presentar la alucinación como «el problema menos extendido» del estudio es defendible
  en la mediana y engañoso en la cola.

**Aplicado:** §5.4 reescrita con los ejemplos reales, la explicación de qué agrupa cada categoría y el rango
verdadero. Corregido además el Anexo F, que declaraba un par de una persona y una organización por artículo
cuando la media es de 1,2 y 2,3, y solo 2 de los 30 artículos cumplen el par exacto.

> **Regla operativa.** Un ejemplo ilustrativo de un informe empírico **se extrae del artefacto**, no se
> redacta para ilustrar. Y antes de interpretar el recuento de una categoría de error, hay que leer qué
> incluye: un nombre plausible como «error de límite» puede estar agrupando el acierto del modelo frente a una
> referencia corrupta.

---

## §F58 — Las localizaciones se recuperan y se anotan: cierre completo del defecto de §F53

**Fecha:** 2026-09-08. **Decisión del autor.** Cierra la vía de solución que `§F53` dejaba abierta.

`§F53` documentó que los *prompts* piden tres categorías de entidad y la anotación solo tiene dos, de modo
que **toda localización extraída era un falso positivo inevitable** —el 67,5 % de los falsos positivos del
estudio—. `§F56` y la revisión global precisaron después que el defecto no estaba en el corpus sino en la
cadena de preparación: **CoNLL-2002 sí anota localizaciones** y el conversor las descartaba.

La solución tiene dos pasos, y **el orden importa**.

### Paso 1 — recuperar lo que la fuente ya anota

El equipo remoto corrigió `download_conll2002.py` para que capture las etiquetas `LOC`. Faltaba trasladarlas
al corpus del estudio, y no existe el script que muestreó los 105 artículos de CoNLL. **No hace falta:** la
correspondencia está en el propio texto, que es único.

`tools/recuperar_locations_n120.py` empareja por texto y recupera **482 localizaciones en 104 de los 105
artículos** de ese origen. Dos precauciones que el script documenta porque no son evidentes: hay que
**normalizar antes de comparar**, porque el corpus del estudio tiene la codificación reparada y una descarga
fresca de la fuente la trae cruda —comparando literalmente empareja **1 de 120**, normalizando empareja
**105**—, y hay que reparar también las localizaciones recuperadas, que llegan como `TarancÃ³n`.

### Paso 2 — anotar a mano lo que ninguna fuente aporta

Quedaban fuera los **quince artículos de Kleptotrace** y los **treinta del corpus sintético**, cuyas fuentes
no anotan esa categoría. Anotarlos era la única forma de que la medición de las tres categorías dejara de
penalizar en el 13 % restante del corpus principal y en todo el corpus del dominio.

| Corpus | Artículos | Anotados | Localizaciones |
|:---|---:|---:|---:|
| `kleptotrace.json` | 15 | **15** | **63** |
| `kleptotrace_augmented_30.json` | 30 | 13 | 20 |

**Criterio de anotación**, tomado de las 482 localizaciones recuperadas para que ambos orígenes sean
homogéneos: entidades geográficas con nombre propio —países, ciudades, estados, regiones, continentes— y
también instalaciones con nombre cuando el corpus original las incluye; la convención de CoNLL-2002 llega a
anotar un aeropuerto (`Barajas`), un río (`Riánsares`) y un colegio. **No se anota el topónimo que aparece
solo dentro del nombre de una organización**, porque ahí la entidad es la organización: `Chicago Field
Office` es organización y no aporta `Chicago`.

**Cada topónimo se verificó presente en el texto antes de anotarlo**, y ese filtro descartó nueve propuestas
que la intuición daba por buenas: `Detroit` y `Washington` en dos artículos que no los mencionan, `Monrovia`
en los tres de Liberia, `Kinshasa` en uno de los del Congo, y `Cyprus`, `Switzerland` y `Netherlands` en
artículos donde el país aparecía solo como gentilicio.

La anotación vive en `data/anotaciones/locations_manuales.json`, **versionada aparte del código** y con su
criterio declarado, para que sea auditable. La aplica `tools/aplicar_locations_manuales.py`, que respeta
cualquier anotación existente y no la pisa.

### Lo que hay que declarar en el informe

Que la categoría de localizaciones tiene **dos procedencias distintas**: 482 recuperadas de la anotación
original de CoNLL-2002 y 83 anotadas a mano para este trabajo. No es un defecto, pero es una diferencia de
método entre partes del corpus y un lector tiene derecho a saberlo.

> **Regla operativa.** Cuando un corpus se compone de varias fuentes, cada categoría de entidad tiene que
> existir en **todas** ellas antes de puntuarla. Si una fuente no la aporta, se anota o se excluye esa
> categoría de la métrica, pero no se mide contra el vacío en una parte del corpus y contra la anotación real
> en otra.

---

## §F59 — Cuatro documentos llevaban dos meses vacíos, dos de ellos de hitos ya entregados

**Fecha:** 2026-09-08. Encontrado al barrer los ficheros rastreados de tamaño cero.

El commit `064a45f`, del 2026-07-01, dejó **cuatro documentos a cero bytes** bajo un mensaje que solo
hablaba de actualizar `.gitignore`, corregir rutas y añadir informes de rendimiento. El vaciado no se
menciona en ninguna parte:

| Documento | Bytes antes | Después |
|:---|---:|---:|
| `doc/organized/Hito_3_Tarea2_Propuesta_Tesina/TAREA_N2_Formulacion_Propuesta_Tesina_EXPANDIDA.md` | 48 594 | 0 |
| `doc/organized/Hito_1_Perfil_Proyecto/Formulario-perfil-tesina.docx-2.md` | 13 938 | 0 |
| `doc/organized/Presentations/PRESENTACION_DEFENSA_TESINA_Eduardo_Ahumada.md` | 5 343 | 0 |
| `doc/organized/Instructions/evaluacion-propuesta_tesina-formulario-2025.md` | 3 601 | 0 |

Los dos primeros corresponden a **hitos ya entregados**, que la política del proyecto manda conservar
intactos. Los cuatro se restauraron desde `b7b8aa3`, el commit inmediatamente anterior, sumando 71 476 bytes.
Escribir sobre un fichero vacío no destruye nada, de modo que la restauración es estrictamente aditiva.

**Por qué sobrevivió dos meses.** Un fichero vacío no rompe nada: no da error al abrirlo, no falla ninguna
comprobación de existencia de ruta y no aparece en un `git status` limpio. Solo se ve si se pregunta por el
tamaño. Ninguna de las comprobaciones mecánicas del proyecto lo hacía.

**Comprobación que se incorpora:** `git ls-files` y, para cada fichero, comprobar que existe **y que no está
vacío**. Es de coste despreciable y detecta la clase entera de defecto.

---

## §F60 — La regla que ignora los duplicados de macOS afirmaba algo falso, y tapaba instantáneas previas a la exclusión de modelos

**Fecha:** 2026-09-08.

El `.gitignore` de la raíz ignora los ficheros con sufijo « 2», « 3»… que crea Finder, y lo justifica
diciendo que «son copias byte a byte». **No lo son.** De los 78 duplicados presentes en el árbol, 48 son
idénticos a su original, 7 no tienen original alguno y **23 difieren**. Varios son además **mayores** que el
fichero que duplican.

La razón de que sean mayores es la que importa: son **instantáneas anteriores a la retirada de los modelos
excluidos**. `results/benchmark_results 3.csv` tiene 28 modelos y 420 filas donde el fichero vigente tiene
22 y 330, y las seis configuraciones de más son `nuextract:latest`, `minimax-m3:cloud` y
`gemma4-12b-mlx-q8-64k:latest`.

El efecto de la regla es por tanto correcto —esos agregados no deben entrar en git— pero su enunciado es
falso, y un enunciado falso invita a levantarla. Se corrige el comentario para que diga lo que ocurre de
verdad.

**Queda constancia de dos cosas que no se tocan.** Primero, el agregado vigente `results/benchmark_results.csv`
está **limpio**: 22 configuraciones, ninguna excluida. Segundo, algunos de esos duplicados **están rastreados
desde antes** de que existiera la regla —`.gitignore` no desrastrea— y contienen nombres excluidos. No se
eliminan: la decisión de qué hacer con un artefacto histórico que ya está en git es del autor, y la política
del proyecto obliga a distinguir lo que afirma de lo que atestigua antes de borrar nada. Ver `§F53` y la
sección «Modelos excluidos del estudio» de `CLAUDE.md`.

**Riesgo concreto que se documenta:** cualquier script que agregue con un patrón como `benchmark_results*.csv`
readmitiría los modelos excluidos sin avisar. Los agregados se leen por ruta exacta, nunca por comodín.

---

## §F61 — Cuatro de los trece modelos tenían más de una corrida, y el informe publicaba una sin mencionar las otras

**Fecha:** 2026-09-08. Detectado al cruzar `merge_manifest.json` con las ocho corridas fuente del
consolidado `results/ANALISIS_CONJUNTO_20260907/`.

`CLAUDE.md` obliga a que, cuando existan varias corridas del mismo experimento, el informe **las declare
todas** y explique cuál se toma como referencia y por qué. No se cumplía. Ocho de los veintiséis grupos
—cuatro modelos en sus dos modos— disponen de dos o tres corridas, y la Tabla 7 publicaba una sola sin
constancia de las demás:

| Grupo | Publicada | No publicada | Diferencia |
|:---|---:|---:|---:|
| gemma4:12b-mlx (KB RAG) | 58,46 | 11,21 | +47,25 |
| gemma4:12b-mlx (baseline) | 56,18 | 27,31 | +28,87 |
| gpt-oss:20b (KB RAG) | 55,67 | 34,19 | +21,48 |
| gpt-oss:20b (baseline) | 52,39 | 43,84 | +8,55 |
| qwen3:8b (KB RAG) | 51,46 | 43,51 / 42,59 | +8,87 |
| qwen3:8b (baseline) | 48,21 | 44,83 / 44,38 | +3,82 |
| nemotron-mini:4b (baseline) | 22,59 | 21,30 | +1,29 |
| nemotron-mini:4b (KB RAG) | 37,12 | 37,33 | **−0,21** |

**Los motivos de sustitución son legítimos** y están documentados: modo de razonamiento activo que consumía
el presupuesto de salida (`gemma4:12b-mlx`, `qwen3:8b`), repetición del diagnóstico de vacíos esporádicos
(`nemotron-mini:4b`) y ampliación del presupuesto de salida (`gpt-oss:20b`). La última fila acredita además
que el criterio fue la validez y no el resultado: en `nemotron-mini:4b` con KB RAG se publica la corrida que
da **menos**.

Pero el motivo legítimo no exime de declararlo. Un lector que encuentre las ocho corridas en `results/` sin
una explicación en el informe no tiene forma de distinguir un criterio de validez de una selección
favorable, y es lo segundo lo que un tribunal juzga. Se añade al Anexo I el apartado «Corridas múltiples del
mismo modelo, y cuál se toma como referencia», con la Tabla 20.

## §F61.bis — `gpt-oss:20b` se mide con el doble de presupuesto de salida que los otros doce modelos

Consecuencia del anterior, y de suficiente entidad para separarla.

Comprobados los `run_config.json` de las ocho corridas fusionadas: siete usan **`max_tokens = 2048`** y una
sola, `gptoss_rerun_REMOTO`, usa **4096**. Es precisamente la que sostiene las cifras publicadas de
`gpt-oss:20b` en la Tabla 7 (52,39 % y 55,67 %).

La ventaja de `gpt-oss:20b` sobre `qwen2.5:14b` (50,22 %) o `llama3.1:8b` (48,76 %) **no es enteramente
atribuible al modelo**: parte procede de disponer del doble de presupuesto para emitir su respuesta, lo que
en un modelo de razonamiento no es un detalle. Los otros nueve parámetros del protocolo coinciden en las
ocho corridas: `--rag-mode kb_combined`, mismo corpus, temperatura 0,1, tamaño de lote 3 y los demás.

**La re-corrida completa pendiente resuelve la asimetría**, porque el equipo de 48 GB ya fijó
`max_tokens=4096` en configuración y CLI para los trece modelos (§2.bis.3 de su encargo). Hasta entonces, la
reserva queda declarada en el Anexo I.

**Lección de método:** la comprobación de protocolo del proyecto exige que «los nueve parámetros coincidan
con la corrida de referencia». Se venía aplicando **dentro** de cada corrida y no **entre** corridas
fusionadas. Un consolidado que une ocho fuentes hereda las diferencias de las ocho, y ninguna comprobación
las miraba.

---

## §F62 — Decisión del autor: una medición inválida no es un resultado y sus cifras no se publican

**Fecha:** 2026-09-08. **Decisión del autor**, que corrige el criterio con que se había redactado `§F61`.

`§F61` añadió al informe una tabla de «corrida publicada frente a corrida sustituida» con las cifras de
ambas. El autor objetó que la cifra sustituida de `gemma4:12b-mlx` con KB RAG, **11,21 %**, no es un
resultado alternativo sino **un resultado incorrecto**, y que presentarlo junto al bueno sugiere que hubo dos
mediciones válidas y se eligió una.

La objeción es exacta, y el propio mecanismo la sostiene: en esa corrida el modelo **no llegó a responder**
en 98 de los 120 artículos —precisión y exhaustividad caen a cero a la vez, que es la firma de no contestar y
no la de equivocarse—, con una latencia media de 967 s frente a los 158 s de la corrida válida. Esa cifra no
mide al modelo: mide un arnés que consumía el presupuesto de salida en el razonamiento.

**Criterio aplicado, que queda como norma del proyecto:**

- **De una medición inválida se declara que existió, por qué se descartó y con qué evidencia. Su F1 no se
  publica.** La evidencia sí, porque es lo que acredita la invalidez: cuántos artículos quedaron sin
  extracción, la latencia y el modo de análisis de la respuesta.
- **De una repetición válida se publican ambas cifras**, porque las dos miden lo mismo y el lector tiene
  derecho a ver la dispersión.

Aplicado a los ocho grupos con más de una corrida, seis resultan inválidos (`gemma4:12b-mlx` y `qwen3:8b` por
razonamiento activo, `gpt-oss:20b` por presupuesto agotado) y dos son repeticiones válidas
(`nemotron-mini:4b`), cuyas dos cifras se conservan. Retiradas del informe las ocho cifras inválidas:
27,31 · 11,21 · 44,83 · 44,38 · 43,51 · 42,59 · 43,84 · 34,19.

**Esto no contradice la regla de declarar todas las corridas, la precisa.** Lo que la regla persigue es que
nadie pueda elegir en silencio entre resultados; se cumple declarando la corrida y su motivo de descarte. Lo
que no exige es dar rango de resultado a un número que no lo es.

**Los artefactos que atestiguan se conservan íntegros.** Los CSV de las corridas descartadas, sus
`benchmark.log` y sus `run_config.json` siguen en `results/` sin tocar: son la prueba de la invalidez, y sin
ellos la declaración del informe no sería verificable.

## §F63 — La primera medición de `gemma4:31b-cloud` sobre N=15 la invalidó la cuota del servicio

**Fecha del incidente:** 2026-09-03, 14:06. Encontrado el 2026-09-08 al barrer N=15 en busca de más
mediciones inválidas, a petición del autor.

Seis de los quince artículos de cada modo devolvieron HTTP 429:

```
2026-09-03 14:06:49 [WARNING] Attempt 1/3 failed for model 'gemma4:31b-cloud':
you (eahumada) have reached your weekly usage limit (status code: 429)
```

Las seis filas registran `parse_method='failed'`, **latencia 0 y 0 tokens/s**: rechazo de infraestructura, no
fallo del modelo. Arrastran el F1 de la corrida a 0,3973 y 0,4272.

**El informe no publica esas cifras.** La Tabla 4 usa `cloud_n15_limpio_20260905`, que resuelve los quince
por análisis directo del JSON (0,6699 y 0,6850), y la Tabla 15 declaraba ya su procedencia. Lo que faltaba
era **el motivo**, que se añade al Anexo con la fecha y la evidencia.

La contramedida se incorporó al sistema el 2026-09-06 a las 09:56 (`466efe5`): limitador de tasa y tope de
paralelismo para modelos sujetos a cuota, descrito en §3.2 del informe.

**Nota sobre el barrido.** Al listar esas filas, el código de presentación usó `valor or -1` y mostró
«ausente» donde había un **0,0**, que es *falsy*. Es exactamente la trampa que la cuarta verificación del
protocolo advierte para el promediado, y aquí apareció en el volcado. La regla vale para cualquier lectura de
un número que puede ser cero, no solo para promediar: **comparar contra `None`, nunca contra la veracidad del
valor.**

---

## §F64 — La métrica restringida anticipa la magnitud pero se queda corta de forma sistemática

**Fecha:** 2026-09-08. **Observación provisional**, con 4 puntos de comparación de los 26 posibles. No debe
escribirse en el informe hasta tener la re-corrida completa.

El Anexo I acompaña cada cifra publicada de una **métrica restringida**, recalculada desde el desglose por
tipo ya almacenado, que excluye la categoría *Locations* porque el corpus no la anotaba. Se presentó como la
estimación de lo que el estudio habría medido sin ese defecto. La re-corrida, ya con las 545 localizaciones
anotadas, permite por primera vez **contrastar esa estimación contra una medición real**:

| Grupo | F1 restringido (recálculo) | F1 medido (re-corrida) | Diferencia |
|:---|---:|---:|---:|
| `gemma4:31b-cloud` baseline | 80,42 | 82,13 | +1,71 |
| `gemma4:31b-cloud` KB RAG | 78,89 | 82,94 | +4,05 |
| `gemma4:12b-mlx` baseline | 73,81 | 77,67 | +3,86 |
| `gemma4:12b-mlx` KB RAG | 74,30 | 79,96 | +5,66 |

> **Cifras corregidas el mismo día.** La primera versión de esta tabla daba 81,73 · 82,82 · 77,16 · 79,97,
> promediadas sobre las **120** filas del CSV crudo. Son incorrectas: la métrica publicada de la re-corrida
> excluye los **7 artículos contaminados** y se calcula sobre **113**. El CSV conserva los 120 a propósito,
> de modo que promediarlo entero produce un número que no es el del estudio. Ver el apartado siguiente.

**La estimación acierta el orden de magnitud y falla el detalle**, siempre por defecto: entre 1,3 y 5,7
puntos por debajo, en los cuatro casos en la misma dirección.

**Por qué era esperable, y por qué conviene decirlo así.** Las dos cifras **no miden lo mismo**. La
restringida **elimina** *Locations* del cómputo; la re-corrida **la puntúa** contra una anotación real. Un
modelo que acierta localizaciones gana puntos que la métrica restringida no puede concederle, porque para
ella esa categoría no existe. La diferencia no es error de la estimación: es el crédito por acertar en una
categoría que antes no se podía acertar.

**Corrección de una afirmación propia.** Al ver el primer caso —el cloud, con 1,31 puntos— se dijo que la
metodología del Anexo I quedaba «validada contra una medición posterior». Con cuatro puntos la formulación
correcta es más modesta: **corrobora la magnitud del efecto y subestima su tamaño de forma sistemática**. La
diferencia importa, porque el informe apoya en esa métrica su afirmación de superar el umbral del 70 %, y una
estimación conservadora refuerza esa conclusión en lugar de debilitarla — pero eso hay que decirlo, no
suponerlo.

**Qué hacer:** esperar a los trece modelos. Si la subestimación se mantiene en el mismo sentido, el Anexo I
puede declararla como cota inferior, que es una afirmación más fuerte y más defendible que la actual.

---

## §F65 — El CSV crudo de una corrida no es la métrica publicada: los 7 artículos contaminados

> **Aviso, 2026-09-09: las dos cifras de este hallazgo están en disputa y `§F65.bis` da las alternativas.**
> El `+10,01` y el `+2,19` proceden del manifiesto del equipo; recalculados de forma independiente sobre el
> detalle por registro salen **+11,89** y **+3,16**. La diferencia de método sigue sin resolver. **Las
> recalculadas son menos favorables al trabajo**, de modo que citar solo las de abajo sería elegir el
> resultado. Quien tome una de las dos debe decir cuál y por qué.

**Fecha:** 2026-09-08. Encontrado al cuadrar el desglose por categoría de la re-corrida contra el corpus.

Los siete ejemplares *few-shot* de la base de conocimientos **son artículos del propio corpus de
evaluación**, con su anotación de oro como salida esperada. En los modos `kb_fewshot` y `kb_combined` eso es
contaminación del conjunto de prueba: al modelo se le enseña la respuesta del examen. La magnitud está
medida y no es despreciable: el KB RAG aporta **+10,01 pp** sobre esos siete artículos frente a **+2,19 pp**
sobre los ciento trece restantes.

Por decisión del autor del 2026-09-08 esos siete se **excluyen de la métrica publicada** y la exclusión se
declara; los ejemplares no se borran. El manifiesto está en
`data/knowledge_base/contaminated_exemplar_articles.json`.

**La consecuencia operativa es la que importa aquí.** El `benchmark_results.csv` de cada corrida conserva
los **120** registros a propósito —es el crudo, y atestigua—, mientras que `benchmark_summary.json` publica
la métrica sobre **113**. Promediar el CSV entero produce un número que **no es el del estudio**, y es
exactamente lo que se hizo al informar las primeras cifras de la re-corrida:

| Grupo | promedio sobre 120 (incorrecto) | métrica publicada, 113 | diferencia |
|:---|---:|---:|---:|
| `gemma4:31b-cloud` baseline | 81,73 | **82,13** | 0,40 |
| `gemma4:31b-cloud` KB RAG | 82,82 | **82,94** | 0,12 |
| `gemma4:12b-mlx` baseline | 77,16 | **77,67** | 0,51 |
| `gemma4:12b-mlx` KB RAG | 79,97 | **79,96** | 0,01 |

Las diferencias son pequeñas, pero el error no lo es: incluir los artículos contaminados **infla
sistemáticamente el beneficio atribuido al RAG**, que es justo la conclusión central del trabajo.

**Comprobación que se incorpora:** antes de citar un F1 de una corrida, leer `total_records` de su
`benchmark_summary.json` y comprobar que coincide con el número de filas que se están promediando. En N=15 y
N=30 coinciden (15 y 30); en N=120 no, y son 113.

### §F65.bis — Las cifras `+10,01` y `+2,19` no reproducen; el resultado sí

**2026-09-08, 20:22.** Tercer hallazgo del repaso de `§L54`, y el más matizado de los tres.

`§F65` cita del manifiesto de artículos contaminados que el KB RAG aporta **+10,01 pp** sobre esos siete
artículos frente a **+2,19 pp** sobre los ciento trece restantes. Esa cifra **se citó sin comprobarla**, y al
calcularla sobre el consolidado publicado —promediando el Δ por modelo y luego entre los trece— sale distinta:

| Población | Manifiesto | Calculado aquí |
|:---|---:|---:|
| Los 7 contaminados | +10,01 pp | **+11,89 pp** |
| Los 113 restantes | +2,19 pp | **+3,16 pp** |
| Razón entre ambas | ×4,57 | **×3,76** |

**El resultado que sostiene la decisión no cambia:** el efecto de la recuperación es entre **tres y cuatro
veces mayor** sobre los artículos que son a la vez ejemplares del RAG, y por tanto excluirlos de la métrica
sigue siendo lo correcto. Lo que no se sostiene es citar dos decimales que no se han reproducido.

**Por qué difieren, probablemente.** El manifiesto no documenta su método, y hay al menos tres formas
razonables de promediar esto que dan resultados distintos: por modelo y luego entre modelos —lo que se ha
hecho aquí—, agrupando todos los registros a la vez, o restringiendo a las configuraciones `kb_combined`
frente a todas. No se puede decidir cuál usó sin su código.

**Qué hacer.** Cuando el informe cite esta comparación, debe hacerlo con la cifra que este repositorio pueda
reproducir y declarando el método, no con la del manifiesto. Y conviene pedir al equipo de 48 GB el cálculo
que produjo el `_comment` de ese fichero, porque una cifra sin método es una cifra que no se puede defender.

**Nota de método.** Este defecto se destapó porque el desglose por categoría no cuadraba con el corpus: la
matriz de confusión daba 1 098 personas de referencia donde el corpus tiene 594, una razón de 1,85 en las
tres categorías. Cuadrar dos fuentes que deberían decir lo mismo es más barato que revisar cualquiera de las
dos por separado, y encuentra lo que ninguna de las dos delata sola.

---

## §F66 — El ANOVA consolidado incluía los artículos contaminados, y `merge_and_analyze.py` no sabía excluirlos

**Fecha:** 2026-09-08. Consecuencia directa de `§F65`, encontrada al comprobar si la herramienta de fusión
estaría lista para cerrar la re-corrida.

`main.py` descuenta los 7 artículos contaminados al calcular el resumen de cada corrida
(`_excluir_contaminados`), pero **`src/merge_and_analyze.py` no lo hacía**: fusionaba los
`benchmark_results.csv` crudos, que conservan los 120 registros a propósito, y ejecutaba el ANOVA sobre
todos. La exclusión existía en un punto de la cadena y se perdía en el siguiente.

**Alcance medido.** Rehecho el consolidado de las ocho corridas sin los 7 artículos:

| | Con contaminados (publicado) | Sin contaminados |
|:---|:---|:---|
| Observaciones | 3 120 (26 × 120) | **2 938** (26 × 113) |
| ANOVA | F = 38,2222 · p = 3,4453e-160 | **F = 35,5557 · p = 3,6729e-148** |

**La conclusión del estudio resiste, y esto es lo importante:** de los trece modelos, **ninguno cambia de
veredicto**. Siguen siendo `nemotron-mini:4b` y `llama3.2:latest` los dos únicos cuya mejora por
recuperación supera la corrección por comparaciones múltiples, y los otros once siguen sin alcanzarla.

**Pero el efecto se encoge en doce de los trece.** La mejora atribuida al KB RAG baja en todos menos
`gemma4:latest`, y los dos casos significativos pierden potencia:

| Modelo | Δ con contaminados | Δ sin contaminados | p con | p sin |
|:---|---:|---:|---:|---:|
| `nemotron-mini:4b` | +0,1452 | **+0,1348** | 0,0000 | 1,0e-4 |
| `llama3.2:latest` | +0,1082 | **+0,1006** | 6,9e-3 | 3,6e-2 |

Es exactamente lo que anticipaba la medición de `§F65`: sobre los siete contaminados el KB RAG aporta
+10,01 pp frente a +2,19 pp sobre los ciento trece restantes, de modo que incluirlos infla el efecto que el
estudio mide.

**Lectura para la defensa.** Que el veredicto no cambie convierte esto en un **resultado de robustez** y no
en un problema: la conclusión del trabajo se sostiene sobre la población limpia, con tamaños de efecto algo
menores. Declararlo es más fuerte que omitirlo.

**Corrección aplicada.** `src/merge_and_analyze.py` excluye ahora los artículos del manifiesto por defecto,
lo declara en la salida y lo deja escrito en `merge_manifest.json`. La exclusión alcanza a **ambos modos**,
no solo al contaminado: comparar un *baseline* sobre 120 con un `kb_rag` sobre 113 sería comparar
poblaciones distintas, y la diferencia entre modos es justo lo que se publica. Existe
`--incluir-contaminados` para reproducir análisis antiguos, con su advertencia.

**Pendiente de decisión del autor:** si el informe adopta ya las cifras sin contaminados (F = 35,5557) o
espera a la re-corrida completa, que sustituirá el consolidado entero. La segunda evita rehacer el trabajo
dos veces; la primera deja el documento coherente desde hoy.

### §F66.bis — Validación de extremo a extremo del arreglo

Probada la herramienta corregida contra el formato nuevo de la re-corrida (`recorrida_20260908/`), con las
dos corridas de N=120 disponibles: 480 filas pasan a 452, que son 4 grupos × 113, la comprobación de
integridad da conforme y el ANOVA se ejecuta.

Lo que cierra el asunto es la comparación con la otra vía de cálculo. El F1 que produce la fusión coincide
**exactamente, a cuatro decimales**, con el que publica el `benchmark_summary.json` de cada corrida:

| Grupo | Fusión (113) | Resumen de la corrida |
|:---|---:|---:|
| `gemma4:31b-cloud` baseline | 0,8213 | 0,8213 |
| `gemma4:31b-cloud` KB RAG | 0,8294 | 0,8294 |
| `gemma4:12b-mlx` baseline | 0,7767 | 0,7767 |
| `gemma4:12b-mlx` KB RAG | 0,7996 | 0,7996 |

Antes del arreglo las dos vías habrían divergido, porque una promediaba 120 registros y la otra 113. Que
ahora coincidan **es la comprobación de que la cadena entera aplica la misma convención**, que es lo que
faltaba: la exclusión estaba en un extremo y se perdía en el otro.

Se hizo en un directorio de trabajo aparte; el consolidado publicado no se ha tocado.

---

## §F67 — El detalle por registro estaba ignorado en git, y es lo único que permite recalcular sin re-inferir

**Fecha:** 2026-09-08. Encontrado al revisar por qué las seis corridas de la re-corrida no traían
`detailed_results.json`.

El `.gitignore` del repositorio del benchmark ignoraba `results/**/detailed_results.json`. Ese fichero es el
**detalle por registro** de cada corrida: lo que el modelo extrajo, lo que decía la referencia y el veredicto
por entidad. No es un agregado, es lo que permite **recalcular una métrica sin volver a inferir**.

**El coste ya se pagó tres veces.** El propio informe declara en tres lugares distintos que unos datos por
registro se perdieron y por eso una cifra no se pudo recalcular: la ejecución de julio de `gemma4:31b`
(«sus datos por registro se perdieron por sobrescritura»), la corrección del *mojibake* («las extracciones
por registro no se conservaron», que obliga a re-inferir para corregirlo) y la métrica restringida del
Anexo I, que solo pudo recalcularse porque el desglose por tipo sí estaba almacenado.

**Y bloquea la verificación independiente.** `tools/verificar_corrida.py`, la herramienta con la que el
equipo de 48 GB declara VÁLIDA cada corrida, **lee `detailed_results.json`**: sus comprobaciones §5.1
(categoría que puntúa contra el vacío) y §5.2 (`recall > 1`) son por registro. Sin ese fichero commiteado,
una corrida entregada **no puede re-verificarla nadie más**: solo queda el agregado. Es lo que me obligó
a comprobar el criterio de `§F53` por otra vía, sumando la matriz de confusión.

**Es el mismo defecto que el de los registros de ejecución**, y por la misma causa: un fichero ignorado no
tiene respaldo. `CLAUDE.md` ya lo dejó escrito el 2026-09-08 para los `benchmark.log`, y la regla no se
extendió al detalle por registro.

**Corrección aplicada.** Retiradas las dos reglas del `.gitignore` y versionados los **22 ficheros
existentes**, unos 16 MB. Comprobado antes que **ninguno contiene modelos excluidos**, que era la razón
legítima para no versionarlos. Las otras diez reglas del fichero no se tocaron.

**Pendiente del equipo de 48 GB:** commitear los `detailed_results.json` de las seis corridas de
`recorrida_20260908/`, que ahora ya no están bloqueados por `.gitignore`.

### §F67.bis — Los respaldos previos a la corrección de puntuación, aplicando la misma lección

`§L51` termina pidiendo que, al escribir una regla de conservación, se revise **en el mismo turno** qué otras
clases de artefacto cumplen el mismo criterio. Aplicado de inmediato a lo que sigue ignorado bajo `results/`:

| Clase | Ignorada | ¿Reconstruible? | Decisión |
|:---|:---|:---|:---|
| `.checkpoint.json` (26) | sí | sí, desde el CSV | se deja ignorada |
| `.bak_prescore` (36) | sí | **según el fichero** | ver abajo |
| Duplicados « 2» de macOS | sí | sí, son copias | se deja ignorada |

Los `.bak_prescore` son la instantánea de cada corrida **antes de la corrección de la convención de
puntuación** del 2026-09-06. Comprobados uno a uno contra el historial de git:

- **15 ficheros (1,3 MB)** ya se recuperan del historial: no aportan nada y siguen ignorados.
- **12 ficheros (6,8 MB)** son la **única copia** y **no contienen modelos excluidos**. Se versionan con
  `git add -f`. Ocho de los doce son `detailed_results.json.bak_prescore`, es decir, el detalle por registro
  anterior a la corrección: exactamente lo que el informe lamenta haber perdido para la ejecución de julio,
  donde «sus datos por registro se perdieron por sobrescritura, de modo que no podía recalcularse».
- **9 ficheros (14,5 MB)** contienen nombres de modelos excluidos. **No se versionan**: la política los
  prohíbe en ficheros de datos, y decidir si un respaldo histórico cuenta como dato o como testimonio es
  criterio del autor. Quedan en disco, sin respaldo, a la espera de esa decisión.

La regla genérica `*.bak_*` **no se toca**, para no arrastrar respaldos de editor; los doce entran de forma
explícita y el `.gitignore` deja constancia de por qué.

---

## §F68 — Con el corpus corregido, el RAG deja de perjudicar a los modelos grandes

> **Aviso, 2026-09-09: este hallazgo tiene tres continuaciones y una de ellas refuta a otra.**
> `§F68.bis` propuso que la emisión de localizaciones explicaba la dispersión; **`§F68.ter` demuestra que es
> falsa** —la métrica restringida *aumenta* la dispersión, de 15,70 a 17,92— y que la «convergencia» que se
> había leído estaba medida sobre cinco modelos excluyendo los dos extremos. `§F68.quater` cierra el asunto.
> **No tomar la hipótesis de abajo sin leer antes la `.ter`.**

**Fecha:** 2026-09-08. **Observación provisional: 3 de 13 modelos.** No debe llevarse al informe hasta tener
la re-corrida completa, pero sí debe conocerse ya, porque afecta a una afirmación del capítulo de resultados.

Con tres modelos rehechos sobre el corpus con localizaciones anotadas, el efecto del KB RAG **cambia de
signo en los dos de mayor capacidad**:

| Modelo | Δ publicado | Δ re-corrida | Cambia de signo |
|:---|---:|---:|:---:|
| `gemma4:31b-cloud` | −0,53 pp | **+0,81 pp** | sí |
| `gemma4:31b-mlx` | −0,18 pp | **+0,97 pp** | sí |
| `gemma4:latest` | −1,17 pp | **+2,53 pp** | sí |
| `gemma4:12b-mlx` | +2,28 pp | +2,29 pp | no |

> **Actualización con el cuarto modelo (2026-09-08 19:13).** `gemma4:latest` se suma a los que cambian de
> signo, y con el salto mayor de los tres: de −1,17 a +2,53 pp. **De los cuatro modelos rehechos, tres
> invierten el signo del efecto y el cuarto ya era positivo.** Ninguno empeora. El único que no cambia,
> `gemma4:12b-mlx`, se mueve una centésima: +2,28 a +2,29.
>
> El patrón se refuerza en lugar de diluirse, que es lo que importa: no son tres casos sueltos sino los
> cuatro primeros de la serie, y los cuatro apuntan igual. Con nueve modelos por delante, sigue siendo
> provisional, pero cada uno que llega hace más probable que §5.3.1 haya de reformularse.

El informe afirma hoy, en §5.3.1, que el beneficio del RAG «**se anula o revierte en los de mayor
capacidad** (−0,54 y −0,18 puntos en los dos de 31B)». Con estos datos esa frase no se sostendría: en los dos
de 31B el efecto es positivo, aunque pequeño.

**El mecanismo explica el cambio y conviene decirlo.** Mientras el corpus no anotaba localizaciones, cada
localización que el RAG ayudaba a extraer se contabilizaba como falso positivo. La recuperación estaba siendo
**penalizada precisamente por hacer su trabajo** en una de las tres categorías que el *prompt* pide. Corregida
la anotación, esa penalización desaparece. No es que el resultado anterior estuviera mal medido dentro de su
convención: es que la convención castigaba al RAG.

**Dos cosas que no cambian**, y que conviene registrar porque son señales de robustez:

- **El orden se conserva.** Publicado: `cloud` 62,38 > `31b-mlx` 59,25 > `12b-mlx` 56,18. Re-corrida:
  `cloud` 82,13 > `31b-mlx` 81,47 > `12b-mlx` 77,67. La corrección sube a todos, no reordena.
- **La magnitud sigue siendo pequeña en los grandes.** +0,81 y +0,97 puntos no son una mejora demostrable;
  habrá que ver qué dice el post-hoc de Tukey sobre el consolidado nuevo. Lo que cae es la palabra
  «revierte», no necesariamente la tesis de que el beneficio decrece con la capacidad.

**Subida general por la corrección**, para dimensionar el efecto: +19,75 pp en `cloud`, +21,49 en `12b-mlx` y
+22,22 en `31b-mlx` sobre N=120; en N=30, +5,03 pp en `31b-mlx`, mucho menor porque ese corpus tiene 40
localizaciones de referencia frente a las 1 034 de N=120.

**Qué hacer.** Nada en el informe todavía. Cuando estén los trece modelos: rehacer el consolidado, mirar el
post-hoc y **reformular §5.3.1 con lo que digan los datos**, sea cual sea. Si la tesis de la proporcionalidad
inversa sobrevive con otra redacción, se conserva; si no, se dice.

---

## §F69 — El informe daba dos cifras distintas para la composición de los falsos positivos, y ninguna era la del estudio

**Fecha:** 2026-09-08. Encontrado al inventariar qué afirmaciones dependen de los datos que la re-corrida va
a sustituir.

El informe decía en dos sitios cosas distintas sobre la misma magnitud:

| Dónde | Cifra | Origen |
|:---|:---|:---|
| §3.3, §7.2 y la leyenda de la Figura 1 | 19 178 de 28 404 = **67,5 %** | **ninguno**: no aparece en ningún artefacto de datos del repositorio |
| Anexo I | 20 946 de 32 201 = **65,0 %** | `results/CORRECCION_LOCATIONS_20260908`, sobre **42 configuraciones** |

**Ninguna de las dos describe el estudio publicado.** La segunda es correcta para lo que dice medir, pero
cubre 42 configuraciones e incluye corridas después declaradas inválidas, entre ellas
`gemma4:12b-mlx_kb_rag` con F1 14,60, la que el modo de razonamiento arruinó (`§F62`). La primera no se ha
podido reproducir desde ningún dato.

**Recalculado sobre los 26 grupos que sostienen la Tabla 7**, tomando para cada uno la corrida que el
consolidado usa realmente, y con los 26 cubiertos sin omitir ninguno:

| Categoría | Falsos positivos | tp + fn |
|:---|---:|---:|
| Locations | **12 852** | **0** |
| Organizations | 5 132 | 21 301 |
| Persons | 1 480 | 15 664 |
| **Total** | **19 464** | |

La cifra del estudio es **12 852 de 19 464, el 66,0 %**. Queda trazable en
`results/COMPOSICION_FP_20260908/`, con el desglose por grupo.

**Corregido en el informe:** §3.3 y §7.2 pasan a 66,0 %, la Figura 1 se regeneró con las cifras nuevas, y el
Anexo I **conserva su 65,0 %** con una glosa que explica que cubre una población distinta. Las dos cifras son
ciertas sobre lo que cada una mide; lo que faltaba era decirlo.

**Dos tropiezos propios durante el cálculo**, que ilustran lo fácil que es equivocarse aquí:

1. La primera versión del recuento no filtraba bien por grupo y **sumaba cero** de las corridas cuya
   estructura no reconocía, sin avisar. Dio 66,0 % por casualidad, no por acierto.
2. Al diagnosticarlo, imprimí las claves de un registro con `list(r)[:12]` y concluí que no traía
   `metrics`, cuando era la **decimotercera**. Estuve a punto de dar por bueno que aquella corrida no tenía
   desglose por tipo.

De ahí que el cálculo definitivo **declare cuántos grupos cubre**, igual que las comprobaciones del
verificador: «26 de 26, ninguno sin cubrir» es lo que permite fiarse del total.

---

## §F70 — El barrido que retiró los modelos excluidos dejó dos ficheros de datos ilegibles

**Fecha:** 2026-09-08. Encontrado al verificar la integridad de los ficheros que yo mismo había versionado
horas antes.

De los **192 ficheros JSON rastreados**, cinco no parsean. Tres son falsa alarma:
`data/sample_an1.json`, `sample_an2.json` y `sample_sanctions.json` están en formato **JSONL** —un objeto por
línea, veinte líneas y las veinte válidas—, que es legítimo y no debe «arreglarse».

**Los otros dos están genuinamente corruptos**, y la causa es identificable:

| Fichero | Daño |
|:---|:---|
| `results/excluidos_n120_REMOTO/detailed_results.json.bak_prescore` | **240 de 480** claves `"model"` sin valor |
| `results/excluidos_n120_REMOTO/benchmark_summary.json.bak_prescore` | falta una clave de primer nivel; el objeto queda mal formado |

El patrón es inequívoco. El barrido que retiró los nombres de los modelos excluidos **borró la cadena del
nombre allí donde aparecía**, dejando `"model":` colgando sin valor y, en el resumen, una llave sin su clave.
Editar JSON por sustitución de texto en lugar de cargarlo, modificarlo y volcarlo produce exactamente esto.

**Las 240 filas afectadas son las del modelo excluido; las otras 240 son de `gpt-oss:20b`** y conservan sus
valores. Es decir, el contenido que sí debe conservarse está atrapado dentro de un fichero que ya no se puede
leer.

**Por qué no se detectó antes.** Nada parseaba esos ficheros. Estaban ignorados en `.gitignore` —eran
`.bak_*`— y solo entraron en git hoy; el defecto llevaba desde el barrido de exclusión sin que ninguna
comprobación lo mirara. Es la misma familia que `§F59`, los cuatro documentos vacíos: **un fichero roto que
nadie abre se comporta igual que uno sano.**

**No se repara por iniciativa propia.** La reparación obvia —extraer solo las 240 filas de `gpt-oss:20b` a un
fichero válido— implica decidir qué hacer con las 240 del modelo excluido, y eso es criterio del autor. Se
deja constancia y la receta:

1. Leer el `.bak` como texto, quedarse con los registros cuyo `"model"` tenga valor.
2. Volcarlos como JSON válido en el mismo fichero o en uno nuevo.
3. Anotar en el propio fichero cuántos registros se retiraron y por qué.

**Comprobación que se incorpora al verificador:** todo JSON rastreado debe parsear, con los `.jsonl`
declarados como excepción explícita. Cuesta un segundo y cubre una clase entera de defecto.

### §F67.ter — Auditoría de los hallazgos de esta sesión

Comprobados contra los datos los seis valores numéricos que sostienen `§F59`, `§F65`, `§F67`, `§F67.bis`,
`§F69` y `§F70`, con el mismo criterio que se aplica al informe. **Cinco reproducen exactamente**: los
71 476 bytes restaurados, los 12 respaldos de 6,8 MB, el 12 852 de 19 464 al 66,0 %, el 240 de 480 de las
claves sin valor y los 16,1 MB de detalle por registro.

**Uno estaba mal.** `§F67` decía «23 ficheros» de `detailed_results.json` versionados y son **22**: el
barrido inicial listaba `results/detailed_results.json` dos veces, porque lo recogía el patrón recursivo y
además se añadía explícitamente. Corregido en `FINDINGS`, en `CURRENT-TASKS §1.18` y en el comentario del
`.gitignore`, que era donde más importaba: ese comentario existe para que nadie retire la regla, y una cifra
que no cuadra al comprobarla resta credibilidad a la explicación entera.

La cita de `§F65` a `+10,01` y `+2,19` pp procede del manifiesto de artículos contaminados, que **aún vive
solo en la rama del equipo de 48 GB** y llegará a `main` con su fusión. No es un error, pero conviene saber
que hoy esa referencia no se puede seguir desde `main`.

---

## §F71 — Las latencias de la re-corrida no son comparables con las publicadas, y la causa no está clara

> **Aviso, 2026-09-09: este hallazgo quedó resuelto en sus continuaciones.** `§F71.bis` refuta la hipótesis
> de que la diferencia viniera de la máquina, con la propia telemetría; **`§F71.ter` da la explicación
> definitiva**: `latency_sec` no mide generación, incluye la espera en cola, y la prueba es que
> `latencia × tokens/s` supera el tope de salida en **veinte de los veintiséis grupos**. Lo que sí es
> característico del modelo son los tokens por segundo, y con ellos se salva el índice Tok/s/B de la Tabla 8.
> **La pregunta de abajo está contestada; la respuesta está en la `.ter`.**

**Fecha:** 2026-09-08. **Observación, no diagnóstico.** Cuatro modelos rehechos.

Comparada la latencia media por artículo entre la corrida publicada y la re-corrida, sobre los mismos
modelos y el mismo corpus N=120:

| Modelo | Modo | Publicada | Re-corrida | Factor |
|:---|:---|---:|---:|---:|
| `gemma4:31b-mlx` | baseline | 1 066,2 s | **20,5 s** | ×0,02 |
| `gemma4:12b-mlx` | baseline | 99,1 s | **4,7 s** | ×0,05 |
| `gemma4:31b-mlx` | KB RAG | 1 408,5 s | 308,8 s | ×0,22 |
| `gemma4:12b-mlx` | KB RAG | 157,8 s | 11,3 s | ×0,07 |
| `gemma4:latest` | baseline | 98,0 s | 46,3 s | ×0,47 |
| `gemma4:31b-cloud` | KB RAG | 2,9 s | 2,3 s | ×0,79 |
| `gemma4:latest` | KB RAG | 489,6 s | **790,9 s** | **×1,61** |
| `gemma4:31b-cloud` | baseline | 1,2 s | 3,1 s | ×2,58 |

**No hay dirección consistente.** Los factores van de **×0,02 a ×2,58**, y dentro del mismo modelo cambian
de sentido según el modo. Un cambio uniforme —más presupuesto de salida, otra concurrencia, otra máquina—
produciría un sesgo en una sola dirección, y aquí no lo hay.

**Lo que sí se puede afirmar, y basta para lo que importa:** las latencias de la re-corrida **no son
comparables** con las publicadas. La **Tabla 8** del informe, la de eficiencia, no puede rehacerse mezclando
ambas, y si se rehace enteramente sobre la re-corrida dará cifras muy distintas de las actuales
—`gemma4:31b-mlx` pasaría de 22,80 tok/s a otra cosa—. El F1 no está afectado: la comparación de calidad
sigue siendo válida.

**Lo que no se puede afirmar es por qué.** Se descartan dos explicaciones fáciles: no es el modo de
razonamiento, porque los dos modelos con mayor caída lo tienen desactivado en ambas corridas; y no es solo la
concurrencia, porque más consumidores concurrentes suben la latencia por petición y aquí la mayoría baja. La
hipótesis restante —que las corridas publicadas se ejecutaron en la máquina de 16 GB con paginación a disco y
la re-corrida en la de 48 GB sin ella— explicaría las caídas grandes pero no que `gemma4:latest` con RAG
suba un 61 %.

**Acción: preguntar al equipo de 48 GB**, que es quien conoce las condiciones de ejecución de ambas. No se
propone ninguna corrección al informe hasta entender el mecanismo: cambiar la Tabla 8 sin saber por qué
cambiaron los números sería sustituir unas cifras inexplicadas por otras.

### §F71.bis — La hipótesis de la máquina queda refutada por la propia telemetría

Antes de esperar respuesta se comprobó con los datos, y **no era la máquina**. Los CSV guardan memoria del
sistema y VRAM por registro:

| Corrida | Modelo | Memoria del sistema | VRAM | Latencia |
|:---|:---|---:|---:|---:|
| publicada | `gemma4:31b-mlx` baseline | 30 539 MB | 26 606 MB | 1 066,2 s |
| re-corrida | `gemma4:31b-mlx` baseline | **30 331 MB** | **26 720 MB** | **20,5 s** |

**La misma máquina y la misma huella de memoria, con la latencia 52 veces menor.** La explicación de los
16 GB con paginación queda descartada: ambas corridas usaron ~30 GB de sistema y ~26,7 GB de VRAM.

Eso desplaza la causa al **arnés o a la propia medición**, no al hardware.

> **Corrección del 2026-09-08, 20:15.** La primera versión de este apartado afirmaba que «los aumentos
> ocurren solo en modo KB RAG». **Es falso**, y se comprobó al repasar las afirmaciones propias tras
> `§L54`. Con cinco modelos rehechos hay **diez pares** comparables: **ocho bajan y dos suben**, y de los dos
> que suben **uno es de modo *baseline***:
>
> | Grupo | Modo | Antes | Ahora | Factor |
> |:---|:---|---:|---:|---:|
> | `gemma4:31b-cloud` | **baseline** | 1,2 s | 3,1 s | ×2,61 |
> | `gemma4:latest` | KB RAG | 489,6 s | 790,9 s | ×1,62 |
>
> Los dos casos no son comparables entre sí, y ahí estaba el error de agruparlos: la latencia del modelo
> alojado es de **uno a tres segundos** y la domina el viaje de red, no la generación, de modo que su ×2,61
> se mueve sobre una base minúscula y no dice nada del arnés. El de `gemma4:latest` sí ocurre sobre una base
> grande y sigue siendo compatible con el presupuesto de salida duplicado, de 2 048 a 4 096 tokens: una
> respuesta que antes se truncaba ahora se completa. Pero eso es **una explicación para un caso**, no un
> patrón.

Lo que queda sin explicar es lo principal: **por qué bajan ocho de diez**, algunas hasta ×0,02. La pregunta al
equipo de 48 GB se mantiene y sigue **acotada** a eso: no es la máquina.

### §F68.bis — Con cinco modelos, lo que se ve no es un cambio de signo sino una convergencia

**2026-09-08, 20:05.** `qwen2.5:14b` completa el quinto modelo y obliga a reformular cómo se venía
describiendo el efecto.

Hasta ahora se decía «cambia de signo», porque los tres primeros pasaban de negativo a positivo.
`qwen2.5:14b` no cambia de signo —era +4,62 y sigue positivo— pero **cae a +0,69**. Con los cinco a la
vista, el patrón es otro:

| | Δ publicado | Δ re-corrida |
|:---|---:|---:|
| Mínimo | −1,17 | **+0,69** |
| Máximo | +4,62 | **+2,53** |
| Media | +1,00 | +1,46 |
| **Dispersión (máx − mín)** | **5,79** | **1,84** |

**Los cinco efectos son ahora positivos y la dispersión se reduce a un tercio.** No es que la corrección
favorezca al RAG: es que **comprime** el efecto hacia un valor pequeño y consistentemente positivo. Los
modelos que salían perjudicados dejan de estarlo, y el que más se beneficiaba deja de hacerlo tanto.

**La lectura que sugiere, y que habrá que confirmar con los trece:** buena parte de la dispersión anterior no
medía cuánto ayudaba la recuperación a cada modelo, sino **cuántas localizaciones emitía cada modelo** en una
categoría donde toda extracción contaba como error. Un modelo locuaz en localizaciones era penalizado en
ambos modos, pero no por igual, y esa diferencia entraba en el Δ como si fuera efecto del RAG.

Si se confirma, el capítulo de resultados gana una afirmación **más fuerte** que la actual: el efecto del KB
RAG sobre este corpus es **pequeño, positivo y homogéneo entre modelos**, en lugar de «inversamente
proporcional a la capacidad». Pero no puede escribirse hasta tener los trece, y menos aún desde cinco.

### §F68.ter — La hipótesis de §F68.bis es falsa, y la «convergencia» descansa en una muestra sesgada

**2026-09-08, 20:12.** Corrección de lo escrito hace seis minutos. Se probó la hipótesis con los datos que ya
había, y no se sostiene.

**Lo que decía `§F68.bis`:** que la dispersión de los efectos publicados no medía cuánto ayudaba la
recuperación a cada modelo sino cuántas localizaciones emitía cada uno, en una categoría donde toda
extracción contaba como error.

**La prueba.** Si fuera cierto, la métrica restringida del Anexo I —que excluye *Locations* del cómputo—
debería mostrar los efectos ya comprimidos. Calculado sobre los trece modelos publicados:

| | Mínimo | Máximo | Dispersión | Desviación |
|:---|---:|---:|---:|---:|
| Δ publicado | −1,17 | +14,53 | 15,70 | 4,53 |
| Δ **restringido** | −2,43 | +15,49 | **17,92** | **4,97** |

**Excluir las localizaciones no reduce la dispersión: la aumenta ligeramente.** La hipótesis queda refutada.

**Y hay un problema mayor, de método.** La «convergencia» de `§F68.bis` se midió sobre los cinco modelos
rehechos, y esos cinco **no son una muestra representativa**: son cinco de los seis con mejor F1, y los dos
efectos más grandes de todo el estudio —`nemotron-mini:4b` con +14,53 y `llama3.2:latest` con +10,82— **están
entre los ocho que faltan**. Entre los cinco rehechos la dispersión publicada ya era 5,79; entre los ocho
pendientes es 15,42.

Que cinco modelos con efectos pequeños sigan teniendo efectos pequeños tras la corrección **no es una
convergencia**: es lo que cabía esperar. La afirmación de `§F68.bis` se retira hasta que estén los trece, y en
particular los dos extremos.

**Lo que sí se sostiene de `§F68`**, porque no depende de la muestra: tres de los cuatro modelos que tenían
efecto negativo pasan a tenerlo positivo, y ninguno de los cinco empeora. La frase de §5.3.1 sobre que el
beneficio «se anula o revierte en los de mayor capacidad» sigue en entredicho, porque los tres que la
sostenían son precisamente los que cambiaron de signo.

**Lección.** Escribí una explicación mecanicista plausible seis minutos después de ver el patrón, y la puse
por escrito antes de comprobarla teniendo los datos a mano para hacerlo. La explicación era falsa y la
muestra estaba sesgada. Ver `LEARNING §L54`.

---

## §F72 — `gpt-oss:20b` no está en el barrido, y eso dejaría el estudio con dos corpus mezclados

**Fecha:** 2026-09-08, 20:42. Detectado al analizar el orden del barrido. **Requiere decisión del autor, y
conviene tomarla antes de que termine la re-corrida.**

`gpt-oss:20b` **no aparece en `_sweep_progress.log`**: ni START, ni END, ni SKIP. No es que esté pendiente,
es que nunca se programó. El barrido va por el orden de la Tabla 7 y salta directamente del cuarto modelo al
sexto.

**La causa probable es una lectura razonable de `§F44`,** que recoge una decisión firme del autor:
«`gpt-oss:20b` se deja con think ON, congelado; su corrida oficial no se re-ejecuta ni se toca». El equipo de
48 GB parece haberla aplicado literalmente y haberlo excluido del barrido.

**Pero esa decisión era sobre el *thinking*, no sobre el corpus.** Se tomó porque apagar el razonamiento le
hace *dejar de responder* —`recall = 0` en 7 de 15 y 10 de 15—, de modo que congelarlo protegía el régimen de
razonamiento. Nada en ella dice que el modelo deba medirse sobre un corpus sin localizaciones anotadas.

**La consecuencia, si no se corrige.** El consolidado final tendría **doce modelos sobre el corpus corregido
y uno sobre el antiguo**. El F1 de `gpt-oss:20b` quedaría unos veinte puntos por debajo del resto por un
defecto del corpus y no por su desempeño —los otros modelos suben entre +19,75 y +22,22 puntos al corregirlo—,
y aparecería en la tabla como el peor de su franja sin serlo. Sería un defecto **peor** que el que la
re-corrida viene a arreglar, porque el actual afecta a todos por igual y este afectaría a uno solo.

**Dos apuntes de precisión.** El primero: `§F44` dice que la corrida oficial de `gpt-oss:20b` es
`results/excluidos_n120_REMOTO`, y **no es así**: el consolidado publicado toma sus filas de
`gptoss_rerun_REMOTO`. Esa frase de `§F44` está desactualizada. El segundo: `§F61.bis` afirmaba que «la
re-corrida completa resuelve la asimetría» del presupuesto de salida de `gpt-oss`. **Si no se re-ejecuta, no
la resuelve**, y esa afirmación queda condicionada a esta decisión.

**Lo que se propone.** Re-ejecutarlo **con `think` ON**, que es lo que la decisión de `§F44` protege, sobre el
corpus corregido y con `max_tokens=4096` como el resto. Eso respeta la decisión del autor en lo que decía y
resuelve las dos cosas: la mezcla de corpus y la asimetría de presupuesto.

**La guarda ya existe.** `merge_and_analyze.py` exige 26 grupos y se pararía con 24, de modo que el problema
no puede colarse en silencio hasta el ANOVA. Pero pararse al final es mucho peor que decidirlo ahora.

**El problema está acotado a un solo modelo.** Comprobado sobre `FINDINGS.md` y `CURRENT-TASKS.md`: de los
trece, **solo `gpt-oss:20b` tiene una decisión de congelación**. Los cinco que quedan por correr tras
`qwen3:8b` —`gemma:latest`, `mistral-nemo:latest`, `llama3.2:latest`, `deepseek-r1:1.5b` y
`nemotron-mini:4b`— no tienen ninguna, de modo que el barrido los cubrirá sin intervención. Y
`gemma4:31b-cloud`, que tampoco aparece en el registro del barrido, **sí está rehecho**: se ejecutó aparte y
está verificado.

Es decir: resuelto `gpt-oss:20b`, el estudio queda completo. No hay más huecos escondidos.

### §F68.quater — El séptimo modelo rompe el patrón: `qwen3:8b` cambia de signo al revés

**2026-09-08, 20:52.** `qwen3:8b` completa el séptimo modelo y aporta el primer contraejemplo.

Los seis anteriores tenían efecto positivo tras la corrección. **`qwen3:8b` no**: pasa de **+3,25 pp** a
**−0,05 pp**. Es la primera inversión en sentido contrario —de positivo a negativo— y deja sin sostén la
observación de que «los efectos son ahora todos positivos», que se venía repitiendo desde el quinto modelo.

| | Con 6 modelos | Con 7 |
|:---|:---|:---|
| Todos positivos | sí | **no** |
| Mínimo | +0,69 | **−0,05** |
| Dispersión | 1,84 | 2,58 |

**Lo que se mantiene y lo que no.** Se mantiene que la corrección **reordena** los efectos de forma
sustancial: de los siete rehechos, tres pasan de negativo a positivo, uno de positivo a negativo y tres
conservan el signo. Lo que ya no puede decirse es que la corrección favorezca sistemáticamente a la
recuperación, ni que los efectos converjan a un valor pequeño y positivo.

**Y refuerza la advertencia de `§F68.ter`.** El contraejemplo llegó con el séptimo modelo, cuando los seis
primeros apuntaban todos en la misma dirección. Si se hubiera escrito una conclusión con seis —y estuve a
punto, con cinco—, este dato la habría desmentido. Los dos modelos que de verdad deciden, `llama3.2:latest` y
`nemotron-mini:4b`, siguen pendientes y ocupan las posiciones once y trece del barrido.

**Nota de método sobre el propio `qwen3:8b`.** Su corrida lleva `thinking DISABLED` en el registro, coherente
con la decisión de `ef5edfa`, de modo que el cambio no procede de un régimen de razonamiento distinto.

---

## §F73 — Qué explica que el efecto del RAG cambie al corregir el corpus: probado, y el estudio no puede zanjarlo

**Fecha:** 2026-09-08, 20:55. **Con siete modelos rehechos. Probado antes de escribirlo**, según `§L54`.

`§F68.quater` deja una pregunta abierta: la corrección del corpus **reordena** los efectos del RAG —tres
suben de signo, uno baja, tres se mantienen— y no se sabe qué lo gobierna.

**Hipótesis con signo predicho.** Mientras las localizaciones no estaban anotadas, cada una extraída era un
falso positivo. Si un modelo emitía **más** localizaciones en modo *baseline* que en KB RAG, el *baseline*
quedaba más penalizado y eso **inflaba** artificialmente el Δ a favor del RAG. Al corregir el corpus esa
inflación desaparece y el Δ debería **bajar**. Predice por tanto una correlación **negativa** entre
`fp_Locations(baseline) − fp_Locations(kb_rag)` y el cambio del efecto.

**Medido sobre los siete rehechos:**

| Estadístico | Valor | p |
|:---|---:|---:|
| Pearson | **−0,531** | 0,220 |
| Spearman | **−0,750** | **0,052** |

**El signo es el predicho en ambos**, y el de Spearman roza el umbral convencional. Pero **ninguno lo
alcanza**, de modo que con siete modelos el resultado es compatible con la hipótesis y también con el azar.

**Y aquí está lo que de verdad importa, que es una limitación del diseño.** Con un efecto de esa magnitud
—`r ≈ −0,53`— harían falta **quince observaciones** para alcanzar `p < 0,05`. **El estudio tiene trece
modelos.** Es decir: aunque la re-corrida termine y el patrón se mantenga exactamente igual, **esta pregunta
no podrá zanjarse con este diseño**. No es que falten datos por llegar: es que el número de modelos del
estudio no basta para este contraste concreto.

**Qué hacer con esto.** Repetir la medición cuando estén los trece —el efecto podría ser mayor de lo que
sugieren siete— y, sea cual sea el resultado, **declarar la limitación**: la correlación se reporta con su
signo, su magnitud y su potencia, sin presentarla como explicación establecida. Es preferible una hipótesis
declarada como tal a una explicación que el propio diseño no puede sostener.

---

## §F74 — La `ρ` que sostiene el hallazgo central vivía solo dentro de una imagen

**Fecha:** 2026-09-08, 21:05. Defecto **introducido por mí hoy** al dibujar la Figura 2.

El panel (b) de la Figura 2 rotula «ρ de Spearman = −0,5165 (p = 0,0707)». Comprobado hoy:

- **El texto del informe no mencionaba «Spearman» ni una vez.**
- **Ningún artefacto de `results/` contenía esa cifra.**

Es decir: la única evidencia numérica del que §5.3.1 llama «el hallazgo central del estudio» existía
exclusivamente **dentro de un PNG**, sin fuente y sin que el cuerpo la discutiera. Un lector la ve y no puede
situarla; un tribunal la ve y no puede comprobarla.

**La cifra es correcta**, y eso se ha verificado: es la correlación de Spearman entre el F1 base de cada
modelo y la mejora que le aporta el KB RAG, sobre los trece de la Tabla 7, y reproduce exactamente
—−0,5165 con p = 0,0707—. El defecto no era el número sino su ausencia de rastro.

**Y al calcularla aparece algo que el informe debía declarar.** Los dos coeficientes **discrepan en el
veredicto** al umbral del 5 %:

| Coeficiente | Valor | p | ¿Significativo? |
|:---|---:|---:|:---:|
| Spearman | −0,5165 | 0,0707 | **no** |
| Pearson | −0,6004 | **0,0300** | **sí** |

Reportar solo el de Pearson respaldaría el hallazgo; reportar solo el de Spearman lo debilitaría. **Presentar
uno cualquiera de los dos en silencio es seleccionar el resultado**, aunque no haya intención. La causa de la
discrepancia es el tamaño de la muestra: con trece modelos el contraste está al límite, y harían falta quince
para que el de Spearman alcanzase significancia (`§F73` documenta el mismo problema en otro contraste).

**Corregido.** Se crea el artefacto `results/CORRELACION_CAPACIDAD_20260908/`, se añaden a §5.3.1 los dos
coeficientes con su discrepancia declarada y con la advertencia de que la afirmación siguiente es «una
tendencia bien orientada y no un efecto demostrado», y se añade la comprobación 22 al verificador, que ata
las cifras del texto y de la figura al artefacto y **falla si el informe deja de declarar la discrepancia**.

**Coste en extensión.** El cuerpo pasa de 14 842 a 16 636 palabras desde la versión entregada, unas **22,6
páginas** estimadas sobre el límite de 25. Quedan unas 1 600 palabras de margen.

### §F73.bis — Con ocho modelos: la hipótesis gana apoyo, y una correlación espectacular resulta ser un artefacto

**2026-09-08, 21:18.** `gemma:latest` completa el octavo modelo y permite repetir las pruebas de `§F73`.

**Lo que mejora.** La correlación entre el desequilibrio de falsos positivos de localización y el cambio del
efecto pasa de `ρ = −0,531 (p = 0,220)` con siete modelos a **`ρ = −0,738 (p = 0,0366)`** con ocho: **cruza el
umbral convencional**. Pearson sigue sin alcanzarlo (`r = −0,620`, `p = 0,101`), de modo que persiste la
discrepancia entre coeficientes que ya se documentó en `§F74`. Con ocho observaciones ninguna de las dos
lecturas es concluyente, pero la dirección se sostiene y el apoyo aumenta.

**Lo que hay que descartar, y es lo más importante de esta entrada.** Al medir también la relación entre el
Δ publicado de cada modelo y cuánto cambia, sale `ρ = −1,000` con `p ≈ 0` y `r = −0,970`. Es un resultado
espectacular y **no significa nada**: es un artefacto de construcción.

El motivo es aritmético. El cambio se define como `Δ_nuevo − Δ_viejo`, de modo que correlacionar `Δ_viejo`
con el cambio es casi correlacionar `Δ_viejo` con `−Δ_viejo`. Solo deja de serlo si `Δ_nuevo` varía tanto
como `Δ_viejo`, y aquí no: el rango del publicado es **8,53** puntos y el de la re-corrida **2,58**.

**Comprobado por simulación**, que es lo que convierte la sospecha en certeza. Sustituyendo `Δ_nuevo` por
ruido uniforme con la misma dispersión y repitiendo dos mil veces, la `ρ` mediana sale **−0,952**, con el
intervalo del 5 al 95 % entre **−1,000 y −0,881**. Es decir: **un valor muy negativo es exactamente lo que
cabe esperar aunque los datos no tengan ninguna estructura**. El −1,000 observado no distingue una hipótesis
de otra.

**Queda escrito para que nadie lo publique**, empezando por quien esto redacta dentro de un mes. Una
correlación de −1,000 con p ≈ 0 sobre trece modelos sería una cifra muy citable en el capítulo de resultados,
y sería falsa. La regla general: **antes de celebrar una correlación, comprobar si una de las dos variables
contiene a la otra**.

### §F74.bis — La `ρ` del hallazgo central resiste la objeción del artefacto

**2026-09-08, 21:24.** Comprobación motivada por `§F73.bis`, donde una correlación de −1,000 resultó ser un
artefacto de definir una variable restando la otra.

**La objeción, que un tribunal puede plantear.** El informe correlaciona el F1 base de cada modelo con
`Δ = F1_kb_rag − F1_baseline`. Esa Δ **contiene** la variable con la que se la correlaciona, y con signo
negativo. ¿No será la `ρ = −0,5165` un artefacto de construcción, como el −1,000 de `§F73.bis`?

**Respuesta: no lo es, y está comprobado.** Simulada la nula correcta —efecto del RAG independiente de la
capacidad, es decir `F1_kb_rag = F1_baseline + ruido` con la media y dispersión observadas de Δ, cinco mil
repeticiones—, la `ρ` bajo esa nula tiene **mediana −0,005** e intervalo central **[−0,484, +0,462]**. El
valor observado cae **fuera** de ese intervalo: solo el **3,72 %** de las simulaciones llega a ser tan
negativo.

**Por qué aquí no hay artefacto y en `§F73.bis` sí.** El artefacto aparece cuando la variable restada domina
la varianza del resultado. En `§F73.bis`, el rango del Δ publicado era 8,53 y el de la re-corrida 2,58, de
modo que la resta quedaba gobernada por el primero. Aquí, en cambio, `F1_kb_rag` varía tanto como
`F1_baseline` —correlacionan a 0,956— y Δ resulta genuinamente pequeño e informativo.

**Tres pruebas coinciden, y conviene no vender la simulación como algo que no es.** Paramétrica unilateral
**0,0354**, simulación **0,0372**, permutación **0,0374**. La simulación **no** aporta más significancia que
la prueba clásica: aporta el descarte del artefacto, que es otra cosa. El informe seguirá citando la `p`
bilateral de **0,0707**, que es lo prudente, porque una prueba unilateral solo sería defendible si la
dirección se hubiera predicho antes de ver los datos.

**Para qué sirve esto.** No cambia ninguna cifra del informe. Es **material de defensa**: si en la mesa se
plantea la objeción del artefacto —y es una objeción buena—, la respuesta está calculada, versionada en
`results/CORRELACION_CAPACIDAD_20260908/` y es reproducible.

---

## §F75 — El diseño de medidas repetidas confirma el ANOVA, y ahora está comprobado y no solo argumentado

**Fecha:** 2026-09-08, 21:26. Material de defensa, en la línea de `§F74.bis`. No cambia ninguna cifra.

§5.3.1 declara una limitación con honradez: las 3 120 observaciones **no son independientes**, porque los
veintiséis grupos evalúan los mismos ciento veinte artículos, de modo que el diseño es de medidas repetidas y
un modelo apropiado sería el procedimiento estrictamente correcto. Y añade un argumento: «al ser el diseño
pareado más potente que el independiente, la significancia obtenida por esta vía es conservadora».

**Ese argumento era razonable pero no estaba comprobado.** Ahora lo está:

| Prueba | Estadístico | p |
|:---|---:|---:|
| ANOVA de una vía (publicado) | F = 38,2222 | 3,4453 × 10⁻¹⁶⁰ |
| **Friedman, medidas repetidas** | χ² = 1 169,23 | **6,2481 × 10⁻²³¹** |

El diseño está **completamente cruzado y equilibrado**: los ciento veinte registros tienen los veintiséis
grupos, sin huecos, que es la condición que Friedman necesita.

**Cómo hay que leerlo, con cuidado.** Los dos estadísticos **no son directamente comparables** —uno es
paramétrico sobre medias y el otro no paramétrico sobre rangos—, de modo que **no procede decir que un `p`
menor signifique más potencia**. Lo que sí puede afirmarse, y es lo que la objeción pone en duda, es que
**el rechazo de la hipótesis nula se sostiene con el método apropiado al diseño**. La elección del ANOVA no
sostiene la conclusión: la conclusión aguanta con ambos.

**Para la defensa.** Si se pregunta por qué se usó un ANOVA de una vía sobre datos apareados, la respuesta
tiene dos partes: el informe lo declara como limitación —no lo esconde— y se ha verificado que la conclusión
no depende de esa elección. Queda en `results/ROBUSTEZ_ESTADISTICA_20260908/`.

---

## §F76 — Con el contraste apropiado al diseño, ocho de trece modelos mejoran, no dos

**Fecha:** 2026-09-08, 21:33. **Afecta a una afirmación central del informe. Requiere decisión del autor.**

§5.3.1 concluye que la mejora por recuperación «solo supera la corrección por comparaciones múltiples en
`nemotron-mini:4b` y en `llama3.2:latest`», y de ahí deriva que el beneficio del RAG es demostrable en los
dos modelos más débiles y «positivo pero no concluyente en la franja intermedia».

**Esa conclusión depende del contraste elegido, y el elegido no es el que corresponde al diseño.** El Tukey
HSD publicado trata las 3 120 observaciones como independientes cuando son apareadas —los veintiséis grupos
evalúan los mismos artículos, como el propio informe declara— y corrige por las **325** comparaciones
posibles entre los veintiséis grupos, cuando las que interesan son **trece**: cada modelo consigo mismo.

**Repetido con el contraste apropiado** —Wilcoxon de rangos con signo sobre los mismos registros, con
corrección de Holm sobre las trece comparaciones de interés:

| Modelo | Δ pp | p ajustada | ¿Significativo? |
|:---|---:|---:|:---:|
| `nemotron-mini:4b` | +14,52 | <0,0001 | **sí** |
| `llama3.2:latest` | +10,82 | <0,0001 | **sí** |
| `qwen2.5:14b` | +4,62 | 0,0001 | **sí** |
| `gemma:latest` | +7,36 | 0,0005 | **sí** |
| `qwen3:8b` | +3,25 | 0,0007 | **sí** |
| `gpt-oss:20b` | +3,28 | 0,0044 | **sí** |
| `gemma4:12b-mlx` | +2,28 | 0,0184 | **sí** |
| `llama3.1:8b` | +1,99 | 0,0432 | **sí** |
| `gemma4:31b-mlx` | −0,18 | 0,3004 | no |
| `mistral-nemo:latest` | +2,37 | 0,4444 | no |
| `deepseek-r1:1.5b` | −0,90 | 1,0000 | no |
| `gemma4:latest` | −1,17 | 1,0000 | no |
| `gemma4:31b-cloud` | −0,54 | 1,0000 | no |

**Ocho de trece, no dos.** Y los cinco que no alcanzan significancia son precisamente aquellos cuyo efecto es
nulo o negativo, lo que da al resultado una coherencia que el publicado no tiene: hoy el informe agrupa como
«no concluyentes» a modelos con +7,36 pp y a otros con −0,54.

**El Tukey no es incorrecto: responde a otra pregunta.** Contrasta todos los pares entre los veintiséis
grupos, lo que incluye comparar `nemotron-mini` con `gemma4:31b`, y para esa pregunta su corrección es la
adecuada. Pero la pregunta del informe es «¿ayuda la recuperación a **este** modelo?», y para esa el
contraste pareado con trece comparaciones es el que corresponde.

**Qué cambiaría en el informe.** La afirmación se vuelve **más fuerte y más matizada a la vez**: el beneficio
es demostrable en ocho de trece modelos, se concentra en los de menor capacidad —los dos mayores efectos son
los dos modelos más pequeños— y se anula en los de mayor capacidad. La tesis de la proporcionalidad inversa
sale reforzada, no debilitada.

**Por qué no se aplica ya.** Primero, porque cambia una conclusión central y eso es decisión del autor.
Segundo, porque la re-corrida va a sustituir estos datos y habrá que repetir el contraste. Lo que **sí**
permanece es el argumento metodológico, que valdrá igual para los datos nuevos.

Artefacto en `results/ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json`.

---

## §F77 — El informe afirmaba la hipótesis nula sobre un contraste con el 8 % de potencia

**Fecha:** 2026-09-08, 21:43. Detectado al revisar los contrastes estadísticos del informe. **Corregido.**

§5.3 comparaba las dos compilaciones de 31B sobre el corpus N=30 y concluía, tras un ANOVA no significativo,
que «la diferencia entre ambos **debe atribuirse a la variabilidad entre artículos y no a una superioridad
real** de una compilación sobre la otra».

**Las cifras son correctas** —F = 0,2235 y p = 0,6382 reproducen exactamente desde
`results/n30_rerun_REMOTO/`—. **La inferencia no.** Un resultado no significativo no acredita la ausencia de
diferencia; solo dice que los datos no la detectan. Y aquí no la detectarían aunque existiera:

| Tamaño de efecto | Potencia con 30 artículos por grupo |
|:---|---:|
| El observado (*d* = 0,12) | **8 %** |
| Mediano (*d* = 0,50) | 49 % |
| Grande (*d* = 0,80) | 87 % |

Con esa potencia, no rechazar la nula era **el resultado más probable de antemano**, hubiera o no diferencia
real. Presentarlo como prueba de equivalencia invierte el sentido del contraste.

**Corregido en §5.3**, que ahora declara la potencia y afirma lo que corresponde: los datos **no permiten
distinguir** ambas compilaciones, no que sean iguales. La corrección **no cambia ninguna cifra** ni la
conclusión práctica —sigue sin haber base para preferir una compilación—, pero sí lo que el texto puede
sostener si alguien pregunta.

**Por qué importa más de lo que parece.** Es la tercera vez hoy que un contraste del informe resulta estar
al límite de su potencia: `§F73` con la correlación de trece modelos, `§F74` con la discrepancia entre
Spearman y Pearson, y ahora este. El patrón sugiere revisar, antes de la defensa, **todo contraste del
informe cuya conclusión sea un «no significativo»**, porque en un estudio con trece modelos y corpus de entre
quince y ciento veinte artículos la potencia es sistemáticamente escasa.

### §F77.bis — Repasados los demás «no significativo» del informe

**2026-09-08, 21:46.** Ejecutada la recomendación de `§F77`. Dos casos, con distinto resultado.

**§5.2, la ablación de prompts: correcto y no se toca.** Dice que el ANOVA no alcanza significancia
(F = 1,1379; p = 0,3417) «consecuencia de N=15» y que los deltas «deben leerse como una **tendencia
consistente y no como una diferencia demostrada**». Es exactamente la formulación que corresponde: declara la
causa —la muestra— y no convierte el no rechazo en prueba de igualdad.

**§5.3.1, la prueba de Levene: mismo error que `§F77`, aunque de menor gravedad.** Decía «la homocedasticidad
**se verifica** (Levene, p = 0,18)». Un contraste no significativo no verifica la hipótesis nula. La
diferencia con el caso de `§F77` es que aquí la potencia sí acompaña: con 3 120 observaciones, Levene detecta
incluso efectos pequeños con más del 99 % de potencia, de modo que el no rechazo **sí es informativo**. El
defecto era de redacción, no de fondo.

Corregido a «**no detecta heterocedasticidad**, lo que con 3 120 observaciones sí es informativo, aunque no
equivalga a demostrar que las varianzas son iguales». Y se aprovecha para sustituir el argumento de que el
diseño pareado es más potente —que era una conjetura— por el resultado que `§F75` calculó: repetido con
Friedman, el rechazo se sostiene con χ² = 1 169,23, de modo que la conclusión no depende de la elección del
contraste. **La frase pasa de argumentar a citar un dato.**

**Balance del repaso:** de los tres «no significativo» del informe, uno estaba bien redactado, uno era un
error de fondo —corregido en `§F77`— y uno de redacción, corregido aquí.

### §F77.ter — La conclusión sobre soberanía está bien construida, y queda cuantificada

**2026-09-08, 21:52.** Última pieza del repaso de potencia. **Resultado negativo: no hay nada que corregir.**

La conclusión 3 de §7.1 compara ejecución local y alojada, y la sospecha era que afirmara una superioridad
sobre quince artículos. **No lo hace.** Dice que sobre N=15 la local supera a la alojada, «**pero ese
experimento es el de menor potencia estadística y el estudio principal lo contradice**», y extrae la
conclusión del corpus grande: la soberanía cuesta del orden de cuatro puntos de F1.

Es el tratamiento correcto, y los números lo respaldan: la diferencia de **2,13 pp** no alcanza significancia
por ninguna vía —Wilcoxon pareado `p = 0,4543`, *t* independiente `p = 0,5940`— y la potencia frente a ese
efecto es del **8 %**.

**Lo que aporta esta comprobación** es poner cifra a lo que el texto dice en palabras. Cuando el informe
escribe «el experimento de menor potencia estadística», ahora hay un artefacto que responde qué significa eso
si alguien lo pregunta: `results/ROBUSTEZ_ESTADISTICA_20260908/potencia_contrastes.json` recoge los cuatro
contrastes revisados hoy con su potencia y su lectura.

**Balance del repaso completo.** De los cuatro contrastes del informe con conclusión negativa o sobre muestra
pequeña: **dos estaban bien redactados** —§5.2 y esta conclusión 3—, **uno era un error de fondo** que se
corrigió (`§F77`) y **uno de redacción** (`§F77.bis`). El informe sale del repaso mejor de lo que entró, y
con la potencia de sus contrastes documentada.

---

## §F71.ter — Resuelto: `latency_sec` no mide generación, incluye la espera bajo concurrencia

**Fecha:** 2026-09-08, 22:06. Cierra la pregunta que `§F71` dejó abierta, **sin necesidad de la respuesta del
equipo de 48 GB**, con una comprobación aritmética.

**El diagnóstico que faltaba.** Comparando *tokens por segundo* entre la corrida publicada y la re-corrida
sobre los mismos modelos, el rendimiento **apenas cambia** —factores de 0,96 a 1,10— mientras la latencia
varía hasta **×0,02**. Si el modelo genera al mismo ritmo y tarda cincuenta veces menos, es que genera
cincuenta veces menos texto… o que la latencia no mide lo que parece.

**La prueba que lo decide.** Si `latency_sec` fuera el tiempo de generación de un registro, entonces
`latencia × tokens/s` daría los tokens generados, y ese número no puede superar el tope de salida. En las
corridas publicadas, con `max_tokens = 2048`:

| Grupo | Latencia | Tokens/s | Tokens implícitos |
|:---|---:|---:|---:|
| `gpt-oss:20b` KB RAG | 862,7 s | 50,3 | **43 430** |
| `gemma4:31b-mlx` KB RAG | 1 408,5 s | 21,9 | **30 910** |
| `gemma4:latest` KB RAG | 489,6 s | 51,1 | **24 998** |
| `deepseek-r1:1.5b` baseline | 113,8 s | 143,3 | **16 307** |

**Veinte de los veintiséis grupos superan el tope**, alguno por veintiún veces. Es aritméticamente imposible.

**Conclusión: `latency_sec` en las corridas publicadas no mide el tiempo de generación de un registro.**
Incluye la espera bajo concurrencia —el reloj de pared desde que el registro entra en la cola hasta que sale,
con otros compitiendo por la GPU—. La re-corrida, con otra configuración de consumidores y lotes, arroja
valores mucho menores por esa razón y no porque el hardware sea más rápido.

**Lo que esto implica, y es más fuerte que la salvedad actual.** El informe ya advierte que las latencias
«proceden de corridas con distinta concurrencia y hardware, por lo que no son comparables entre filas», y
acierta. Pero la razón real es peor que la declarada: **la latencia no es una propiedad del modelo en
absoluto**, sino del régimen de ejecución, de modo que no lo sería ni aunque todas las filas vinieran de la
misma corrida, porque el controlador AIMD varía los consumidores durante el barrido.

**Lo que sí se salva.** Los **tokens por segundo** son estables entre corridas —de 0,96 a 1,10— y por tanto
sí caracterizan al modelo. La Tabla 8 se apoya en esa columna y en el índice Tok/s/B que deriva de ella, de
modo que **su contenido sigue siendo válido**; lo que no puede reconstruirse desde la latencia es un tiempo
por artículo comparable.

**Pregunta al equipo de 48 GB: se mantiene, pero ya no como diagnóstico.** Basta con que confirmen si
`latency_sec` incluye la espera en cola, para dejarlo escrito con su palabra además de con la aritmética.

---

## §F78 — Las comprobaciones, sometidas a prueba de mutación

> **Nota de vigencia, 2026-09-09.** Cuando se escribió esto eran **veinticuatro** y hoy son **veintiséis**. Las
> dos nuevas se sometieron a mutación al añadirlas: la **25**, «cada grupo se lee de la corrida que el
> consolidado usa» —falla ante un descuadre y se marca VACÍA si el artefacto no declara el control—, y la
> **26**, «referencias a Anexo X y a Tabla N» —detecta un `Anexo Z` y una `Tabla 44` inventados—.
>
> **Y cuatro de las veinticuatro originales se modificaron después**, todas re-probadas por mutación al
> tocarlas: la **17** y la **16**, que dejaban caer en silencio una fila ilegible de la Tabla 4 y de la Tabla 7
> (`§F82`); la **19**, con dos variantes del mismo defecto en las tablas 5, 6 y 8 (`§F82.bis`); y la **24**,
> que comprobaba un recuento por presencia de la palabra y no distinguía «tres» de «dos» (`LEARNING §L59`), y
> que además se saltaba en silencio los artefactos ausentes (`§L60`).
>
> El recuento de «catorce mutaciones» de abajo se refiere a la tanda original y **no incluye** las de esos
> seis casos posteriores, que están documentadas en sus propios hallazgos.

**Fecha:** 2026-09-08, 22:23. Aplicada al propio verificador la regla que él impone: **una comprobación que
nunca se ha visto fallar no está comprobada** (`§L48`).

Hasta hoy solo cinco de las veinticuatro se habían probado en negativo. Se han introducido **catorce
mutaciones** deliberadas en el informe, una por familia de defecto, comprobando en cada caso que alguna
comprobación la detecta, y restaurando después:

| Mutación introducida | ¿Detectada? |
|:---|:---|
| Referencia `§9.99` a una sección inexistente | sí |
| Leyenda de tabla sin tabla debajo | sí |
| Cita a una «Figura 9» que no existe | sí |
| Entrada de bibliografía sin URL | sí |
| Numeración de bibliografía no contigua | sí |
| Cita `[99]` sin entrada | sí |
| Resumen por encima de 200 palabras | sí |
| Pictograma en prosa | sí (2 comprobaciones) |
| Nombre de modelo excluido | sí (2) |
| Arte ASCII | sí |
| Δ incoherente en la Tabla 7 | sí |
| Fila con F1 imposible | sí (2) |
| Desajuste entre el Anexo I y la Tabla 7 | sí (3) |
| Cifra alterada en el índice de defensa | sí |

**Catorce de catorce.** Y las mutaciones se solapan: varias disparan más de una comprobación, lo que da
redundancia allí donde más importa —las cifras de las tablas—.

**Un falso negativo, y era mío.** La primera versión de la prueba de bibliografía insertaba texto sin quitar
la URL, de modo que la línea seguía conteniendo `http` y la comprobación hacía bien en no protestar. Corregida
la mutación, se detecta. **Es el mismo error que la prueba pretende cazar**: dar por buena una comprobación
sin verificar que la mutación era realmente un defecto.

**Verificado que el informe queda intacto** tras las catorce mutaciones: `diff` sin diferencias frente al
original.

---

## §F79 — La duración de una corrida no es estimable con la telemetría que el estudio guarda

**Fecha:** 2026-09-08, 22:26. Segundo intento fallido, por causa distinta del primero. **Se documenta para
no intentarlo una tercera vez.**

**Primer intento** (esta tarde): estimar el tiempo de cada modelo a partir de las latencias de la corrida
publicada. Descartado porque los dos anclajes medidos daban factores que diferían casi cuatro veces, y porque
`§F71.ter` demostró después que esas latencias incluyen espera en cola y no miden generación.

**Segundo intento** (ahora): usar los **tokens por segundo**, que `§F71.ter` acreditó como estables entre
corridas y por tanto característicos del modelo. La hipótesis era que si cada artículo requiere un trabajo
parecido, el producto `minutos × (tokens/s)` sería aproximadamente constante entre modelos.

**No lo es.** Sobre los siete modelos ya rehechos:

| Modelo | Minutos (N=120) | Tokens/s | Producto |
|:---|---:|---:|---:|
| `gemma4:latest` | 74,5 | 50,8 | **3 784** |
| `gemma4:31b-mlx` | 45,4 | 24,3 | 1 104 |
| `gemma4:12b-mlx` | 18,2 | 53,8 | 980 |
| `qwen3:8b` | 18,4 | 39,8 | 730 |
| `llama3.1:8b` | 17,0 | 42,4 | 722 |
| `gemma:latest` | 17,4 | 40,5 | 703 |
| `qwen2.5:14b` | 27,5 | 23,3 | **643** |

De 643 a 3 784: un factor de **5,9**. `gemma4:latest` se dispara porque su modo KB RAG genera muchísimo más
texto que los demás, y esa variable —**cuántos tokens produce cada modelo por artículo**— no está registrada
en ninguna parte: el CSV guarda `tokens_per_sec` pero **no el recuento de tokens**.

**Conclusión: con la telemetría disponible no se puede estimar cuánto tardará una corrida.** Falta
precisamente el dato que la determina. Registrarlo sería barato y útil para el futuro, pero no cambia el
presente.

**Consecuencia práctica para la monitorización:** el único criterio válido para juzgar si un barrido sigue
vivo es su propio registro de progreso, y por eso se pidió el script al equipo de 48 GB. Un silencio largo
**no es evidencia de nada**, y hoy ya llevó una vez a estar a punto de declarar caído un barrido que
funcionaba.

---

## §F80 — La comprobación de las URL estaba tras una bandera, y al ejecutarla aparecieron tres cosas

**2026-09-08, 23:3x.** La rutina de seguimiento venía informando «24 comprobaciones, 0 fallos» después de cada
cambio. La comprobación de que **las URL de la bibliografía responden** no está entre esas 24: vive detrás de
`--red`, porque sale a la red y tarda. De modo que la línea de estado decía cero fallos **sin haber abierto
una sola URL**, cuando `CLAUDE.md` es explícito en que «una URL no abierta no cuenta como verificada».

Ejecutada, la comprobación pasa a ser la **25** y aparecen tres cosas.

**Zenodo bloquea lectores automáticos.** La entrada [18], el corpus Kleptotrace, daba tiempo de espera
agotado, y luego HTTP 504. Aplicando el control de `§L57` —pedir algo que sí debería responder— resultó que
**zenodo.org devuelve 403 hasta en su propia raíz**. No es un enlace roto: es un portero, igual que ACM. Se
acredita, como manda la norma del proyecto, por **resolución del DOI**: `10.5281/zenodo.14027005` responde 302
con destino, luego el registro existe.

> **Actualización del 2026-09-09.** Zenodo **ha vuelto a responder**: la entrada [18] da hoy HTTP 200 y
> aterriza en `zenodo.org/records/14027005`, de modo que se verifica por la vía normal y ya no necesita
> acreditarse por DOI —el recuento de acreditadas baja de cuatro a tres, y es una mejora, no una regresión—.
> El 403 que se describe abajo era real cuando se midió, a las 23:0x del día 8. **Se conserva `zenodo.org` en
> la lista de porteros**: no estorba, porque solo actúa ante un 401 o un 403, y el episodio demuestra que
> puede repetirse.

**Un identificador de ACM que no es un DOI.** Al exigir resolución del DOI a las entradas de un portero, falló
la [17], el artículo de Lafferty, McCallum y Pereira sobre *conditional random fields*. Su URL es
`dl.acm.org/doi/10.5555/645530.655813`, y **`10.5555` no es un DOI registrado**: doi.org devuelve 404 y
Crossref responde «Resource not found». OpenAlex confirma que el trabajo existe —12 994 citas— y que su campo
`doi` es **nulo**: es un artículo de ICML de 2001 sin DOI, y `10.5555` es el identificador interno de ACM para
material heredado. La cita **no está mal** para un lector humano, que abre esa página sin problema; lo que no
puede es acreditarse por DOI, porque no lo hay. Se declara la excepción con su evidencia y con una copia
abierta verificada: `repository.upenn.edu/handle/20.500.14332/6188`, HTTP 200.

**Y lo más importante: el 403 de ACM no distingue nada.** Comprobado con un identificador inventado,
`10.5555/000000.000000`, que devuelve **el mismo 403** que el real. Es decir, la regla anterior —«si es un
portero y da 403, se acepta»— habría dado por buena **cualquier cita inventada sobre ese dominio**. Ese es el
defecto de `§L57` con otra cara: un valor que significa éxito y que también produce la avería.

### El primer arreglo tenía dos defectos, y los encontró su propia prueba de mutación

Aplicada la disciplina de `§F78`, dos mutaciones sobre el arreglo recién escrito:

1. **Sustituir la URL de [17] por el identificador inventado pasaba sin que nada lo notase.** La excepción
   estaba indexada **solo por el número de entrada**, de modo que acreditaba la entrada 17 llevara la URL que
   llevase. Corregido: la clave es ahora el par (número, URL exacta).
2. **Un dominio inexistente se clasificaba como «no concluyente».** La distinción entre fallo y caída del
   servidor es correcta —un 504 no acredita que el enlace esté roto—, pero se aplicaba a toda excepción de
   red. Un dominio que no resuelve en el DNS **sí es un enlace roto**. Corregido: `gaierror`,
   `ConnectionRefusedError` y `ConnectionResetError` fallan; el resto queda como no concluyente.

Con los dos arreglos, ambas mutaciones se detectan. Informe restaurado y comprobado con `diff`.

### Lo que queda fallando, y debe seguir así

La entrada **[37]**, el repositorio del proyecto, devuelve **404 porque es privado**. Es un defecto real y
declarado: el informe afirma que el material está publicado y hoy no lo está, por la purga pendiente. **No se
declara como excepción**: tiene que seguir fallando hasta que se resuelva, que es justo para lo que sirve una
comprobación. Ver `SEGURIDAD-CLAVE-GOOGLE-20260908.md`.

### Consecuencia para la rutina

Antes de dar por buena la bibliografía hay que ejecutar `python3 tools/verificar_informe.py --red`, y no
solamente la forma corta. Una comprobación que existe pero no se ejecuta es indistinguible de una que no
existe. `LEARNING §L47` lo dice para las comprobaciones vacías; esto es lo mismo para las apagadas.

---

## §F81 — El emparejamiento cuenta dos veces una misma referencia, y la exhaustividad llega a pasar de 1,0

**2026-09-08, 23:4x.** Ejecutando `tools/composicion_fp.py --resumen`, un modo de validación que existía y no
formaba parte de la rutina, apareció un dato que no encaja: `tp + fn` agregado en personas vale 15 664 sobre
26 grupos, y 15 664 entre 26 no da entero. Si los veintiséis grupos puntúan **los mismos 120 artículos contra
la misma anotación de referencia**, ese recuento tendría que ser idéntico en todos.

No lo es. Va de **594 a 675** en personas y de **812 a 869** en organizaciones. Descartada primero la
explicación benigna —que hubiera registros sin métricas—: hay **cero** en los veintiséis grupos.

### El mecanismo, en el código

`src/evaluator.py::evaluate_extraction_by_type` incrementa `tp` **por cada entidad extraída que casa** con
alguna de referencia, y a continuación calcula `fn = len(gt_list) - len(matched_gts)`, es decir, sobre el
conjunto de referencias **distintas** casadas. Si dos entidades extraídas casan con la misma referencia
—«John Smith» y «Smith, John», que el emparejamiento difuso da por iguales al umbral del 85 %— `tp` sube dos
veces y la referencia se cuenta una sola.

De ahí se siguen tres cosas, y las tres se comprueban en los datos:

1. **`tp + fn` no vale `len(gt)`**, sino `len(gt)` más el número de emparejamientos duplicados. Por eso el
   recuento de referencia varía entre grupos que puntúan el mismo corpus.
2. **La exhaustividad por categoría puede pasar de 1,0**, porque es `tp / len(gt_list)`. Hay **197 registros**
   con exhaustividad mayor que uno, y el máximo observado es **2,444**. Una exhaustividad por encima de uno es
   imposible en una métrica correcta.
3. **La precisión no está afectada.** Cada entidad extraída contribuye como mucho una vez —el bucle hace
   `break` al primer casamiento—, que es justo lo que su denominador cuenta.

### Cuánto afecta a lo publicado, con la cifra

El recálculo no necesita reejecutar inferencia: de `recall = tp / len(gt)` se despeja `len(gt)`, y las
referencias casadas son `len(gt) - fn`. Con eso se rehace cada registro contando cada referencia una sola vez.
Artefacto en `results/EMPAREJAMIENTO_DUPLICADO_20260908/efecto.json`, reproducible con
`tools/efecto_emparejamiento_duplicado.py`.

> **Las cuatro cifras de este bloque están corregidas en `§F81.bis`.** Y **`§F81.ter`** añade algo más grave: este hallazgo era un **redescubrimiento** de `§F49`, que ya lo había documentado el 2026-09-07 y cuyo defecto ya estaba corregido en la rama de la re-corrida. Se calcularon leyendo ocho de los
> veintiséis grupos de la corrida equivocada. El mecanismo, la dirección y la conclusión no cambian; las
> cifras y una de las afirmaciones, sí.

- **410 emparejamientos duplicados** en los 26 grupos.
- El F1 publicado está inflado **+0,145 pp de media**, con un máximo de **+0,936 pp** en
  `gemma4:latest_baseline`. Siempre al alza, como predice el mecanismo.
- **Ninguna mejora cambia de signo**: cero de trece.
- **El orden de los veintiséis grupos es idéntico** antes y después.

El efecto queda muy por debajo del umbral de 0,02 en F1 que `CLAUDE.md` declara tolerable, y **no cambia
ninguna conclusión del trabajo**. La mayor variación es la de `gemma4:latest`, cuya mejora pasa de −1,17 a
−0,25 puntos, y sigue siendo negativa.

### Por qué importa igualmente

Por dos razones que no dependen de la magnitud.

**La primera es de defensa.** Una exhaustividad de 2,444 en los datos crudos es exactamente lo que un tribunal
puede encontrar si mira, y encontrarla sin que el trabajo la haya declarado es peor que declararla con su
efecto acotado. La declaración es barata: el defecto está cuantificado, es reproducible y no altera nada.

**La segunda es operativa y urgente.** La re-corrida en marcha en el equipo de 48 GB **usa este mismo
evaluador**. Corregirlo a mitad del barrido produciría datos no comparables entre los modelos ya terminados y
los que faltan, de modo que **no se toca `evaluator.py`** sin decisión expresa. Queda como decisión 8 en
`DECISIONES-PENDIENTES-20260908.md`.

### Lo que enseña sobre el método

El indicador que lo destapó es el mismo de `§F53`: mirar `tp + fn` agregado por categoría. Allí la señal era
que valiera cero; aquí, que **no fuera constante entre grupos que puntúan el mismo corpus**. Ambas se ven en
una línea de aritmética y ninguna necesita reejecutar nada.

Y apareció al ejecutar un modo de validación que existía desde hacía días y que nadie había corrido, igual que
`§F80` apareció al ejecutar `--red`. Dos hallazgos seguidos por la misma causa: **una capacidad que existe y
no se ejecuta no está comprobando nada**.

---

## §F81.bis — Las cifras de §F81 estaban mal: ocho de veintiséis grupos leídos de la corrida equivocada

**2026-09-09, 00:2x.** Comprobando otra cosa —si las cifras «Publicado» de `tools/estado_recorrida.py`
coincidían con la Tabla 7— apareció que la media del detalle por registro **no reproducía la tabla en cuatro
grupos**: `gemma4:12b-mlx_baseline` daba 27,31 frente a 56,18, `gpt-oss:20b_baseline` 43,84 frente a 52,39,
`qwen3:8b_baseline` 44,83 frente a 48,21 y `nemotron-mini:4b_baseline` 21,30 frente a 22,59. Tres de esas
cuatro cifras son justamente las que se retiraron del informe por inválidas.

### La causa, y es mía

El consolidado resuelve los grupos repetidos con `--on-duplicate=first`: gana la **primera** fuente que los
trae, y el manifiesto lo documenta en `duplicate_notes`. **Ocho de los veintiséis grupos aparecen en dos
fuentes.** El script que escribí para `§F81` construía el mapa de origen con una comprensión de diccionario,
donde **gana la última**, que es la política contraria. Así se leyó `gpt-oss:20b` desde `05_excluidos` en
lugar de `00_gptoss_rerun`, y `gemma4:12b-mlx`, `qwen3:8b` y `nemotron-mini:4b` desde `06_P3` en lugar de sus
corridas de sustitución.

**`tools/composicion_fp.py` no tiene este defecto**: usa `setdefault`, que sí reproduce la política del
consolidado. De modo que **la composición de falsos positivos publicada —el 66,0 %, 12 852 de 19 464— no está
afectada**. Lo comprobé antes de escribir nada, porque esa cifra sí está en el informe.

### Las cifras corregidas

Corregido `tools/efecto_emparejamiento_duplicado.py` para usar `setdefault`, y añadido un **control** que
compara la media de cada grupo con la del CSV consolidado y declara los que no cuadren. Con la corrección, los
veintiséis reproducen el consolidado y **el control no señala ninguno**. Los Δ coinciden ahora con la Tabla 7
del informe, que es la prueba externa de que la fuente es la correcta.

| Magnitud | En `§F81` | Correcta |
|:---|---:|---:|
| Emparejamientos duplicados | 410 | **409** |
| Inflación media del F1 | +0,145 pp | **+0,160 pp** |
| Inflación máxima | +0,936 pp | **+1,287 pp** |
| Grupo más afectado | `gemma4:latest_baseline` | **`nemotron-mini:4b_baseline`** |
| Mejoras que cambian de signo | 0 de 13 | **0 de 13** |
| Orden de los 26 grupos | idéntico | **cambia en un puesto** |

### La afirmación que hay que retirar

**«El orden de los veintiséis grupos es idéntico» era falsa.** Con la fuente correcta hay **un intercambio**:
`gpt-oss:20b_kb_rag` y `gemma4:latest_baseline` permutan los puestos 7 y 8, porque el segundo pasa de 55,91 a
54,98 y el primero apenas se mueve, de 55,67 a 55,65. Son dos grupos separados por 0,24 puntos y el informe no
publica una ordenación de grupos, de modo que **no cambia ninguna conclusión**; pero la afirmación, tal como
estaba escrita, no era cierta.

**Lo que sí se sostiene**, y es lo que importaba: el mecanismo, que la inflación es siempre al alza, que
**ninguna de las trece mejoras cambia de signo** y que el efecto queda muy por debajo del umbral de 0,02 en F1
que `CLAUDE.md` declara tolerable.

### Lo que enseña

Un mapa de `grupo → corrida` construido con una comprensión de diccionario **elige en silencio** cuando una
clave aparece dos veces, y elige lo contrario que `setdefault`. No hay error, ni aviso, ni nada que mirar: el
script corre igual y produce cifras plausibles. Lo destapó **un control externo** —comparar contra la Tabla 7,
que se produjo por otra vía— y no una revisión del código, que se había leído entero sin ver nada.

De ahí la regla que se incorpora al recálculo: **toda herramienta que reagrupe por corrida declara si sus
medias reproducen el consolidado**, y nombra las que no. Es una comprobación de cuatro líneas y habría
ahorrado este hallazgo.

---

## §F82 — Una fila ilegible salía en silencio de la verificación, y la Tabla 7 era una de ellas

**2026-09-09, 01:0x.** Siguiendo la pista de `§L58` —órdenes cuyo «no hizo nada» no se distingue de «lo hizo
bien»— se barrieron las excepciones que los verificadores se tragan. La de la tasa de alucinación resultó
**bien protegida**: si un CSV no se pudiera leer, el recuento de grupos bajaría de 61 y la comprobación falla
por su propia aserción de población. Pero dos comprobaciones de tablas no tenían esa guarda.

**Comprobado por mutación**, que es la única forma de saberlo. Cambiando `74.44%` por `74,44 %` en una fila de
la Tabla 4, el recuento bajaba de **52 a 48 elementos** y la comprobación seguía diciendo **ok**. Lo mismo en
la **Tabla 7**, que es la tabla central del trabajo: poniendo `n/d` en el F1 base de `gemma4:31b-cloud`, el
recuento bajaba de **26 a 24** y pasaba igual.

Es decir: **una fila cuyo formato dejara de casar con el patrón simplemente dejaba de verificarse**. No hacía
falta un error para perderla; bastaba una coma decimal, un `%` desplazado o una celda con «n/d». Y el recuento
menor quedaba impreso, pero nadie conoce de memoria cuántos elementos debe examinar cada comprobación, que era
justo el supuesto sobre el que se apoyaba `§L47` al exigir que se declararan.

### El arreglo

Las dos comprobaciones cuentan ahora aparte las filas que **parecen de datos y no se pueden leer** —cinco
columnas en la Tabla 7, siete en la Tabla 4, con nombre y sin ser encabezado— y las declaran como fallo, con
el nombre de la fila y las celdas que no pudo interpretar. El recuento total se mantiene, de modo que una fila
ilegible **no reduce el número de elementos examinados**: aparece como fallo, no como ausencia.

Verificado por mutación en ambas: fallan con el nombre del modelo y conservan sus 26 y 52 elementos.

### Lo que enseña

`§L47` exige que cada comprobación declare cuántos elementos examinó, y esa regla ha funcionado: destapó
comprobaciones vacías. Pero **declarar el recuento solo sirve si alguien sabe cuál debería ser**, y aquí
bajaba de 26 a 24 sin que nada chirriara. La forma robusta no es publicar el número, sino **exigir que todo
candidato se procese**: contar lo que se intentó y no solo lo que salió bien.

Es la tercera cara del mismo defecto en dos días. En `§L57` un 404 podía significar éxito o URL rota; en
`§L58` un `push` sin error podía significar sincronizado o nada que empujar; aquí un «ok» podía significar
verificado o no mirado. Las tres se resuelven igual: **comparar contra lo que debería haber, no contra lo que
hubo**.

---

## §F82.bis — Completado el barrido: dos formas más de dejar de verificar sin decirlo

**2026-09-09, 01:2x.** Aplicada la mutación al resto de comprobaciones que leen tablas. `el Anexo I cuadra con
la Tabla 7` y `la Tabla 18 reproduce desde el analisis de mojibake` **detectan**. La de las tablas 5, 6 y 8
tenía **dos agujeros distintos del de `§F82`**, y peores, porque en aquél el recuento al menos bajaba.

**Primero: `mirados += 1` antes del `float()`.** El recuento subía y a continuación el `except ValueError:
continue` saltaba la comparación. El valor quedaba sin verificar **y el recuento no lo delataba**: seguía
marcando 32 elementos, exactamente igual que cuando todo se comprueba. No había señal de ninguna clase.

**Segundo: una fila cuyo nombre no case se descarta antes de contar.** Las guardas
`if len(c) < 4 or c[0] not in d: continue` y su equivalente de la Tabla 8 sacaban de la comprobación
cualquier fila cuyo rótulo dejara de corresponder con un grupo de la corrida. **Renombrar un modelo en la
tabla la habría sacado de la verificación sin dejar rastro** —ni fallo, ni recuento menor, nada—, que es
justo lo que ocurre cuando se corrige el nombre de un modelo, que en este proyecto ha pasado varias veces.

Las dos se descubrieron por accidente afortunado: la mutación buscaba la primera cifra de la fila y la
encontró **dentro del nombre del modelo** —`gemma4:12b-mlx` contiene un «12»—, de modo que rompió el rótulo en
lugar del dato y destapó el segundo agujero, que no se estaba buscando.

**Corregido en los tres casos**: un valor ilegible y una fila sin correspondencia son ahora fallos con el
nombre de la fila y el valor que no se pudo leer. Verificado por mutación en las tres tablas, y comprobado
que sobre el informe limpio no aparece ningún falso positivo: sigue en 32 elementos y sin fallos.

**Balance del barrido.** De las siete comprobaciones que leen tablas o datos tabulares, **tres estaban
protegidas** —alucinaciones por su aserción de población, Anexo I y Tabla 18— y **cuatro no**: Tabla 4,
Tabla 7 y las tres tablas menores, que compartían el mismo defecto con tres variantes. Todas corregidas y
sometidas a mutación.

---

## §F81.ter — `§F81` era un redescubrimiento de `§F49`, y `§F49` afirma una inmunidad que no existe

**2026-09-09, 02:1x.** Verificando las nueve corridas entregadas de la re-corrida apareció que la firma
`tp + fn` es **idéntica en las veintisiete** —(1098, 1500, 1034) en N=120— cuando `§F81` predice que debería
variar entre modelos. La explicación estaba en el propio código de la rama: `src/evaluator.py` lleva desde el
**2026-09-08** una corrección con este comentario, «cada entidad de referencia se empareja UNA sola vez.
Antes dos extracciones que casaban con un mismo gold sumaban dos aciertos», y cita `encargo §2.3, FINDINGS
§F49/§F50`.

**Es decir: el defecto ya estaba encontrado y ya estaba corregido, y `§F81` lo redescubrió sin verlo.** El
mecanismo que describí es el mismo que `§F49` documentó el 2026-09-07, con la misma referencia de línea. Debí
haberlo buscado antes de escribir un hallazgo nuevo; que la firma constante de la re-corrida me llevara hasta
él es una casualidad afortunada, no un método.

### Pero `§F49` afirma algo que no se sostiene, y eso sí es nuevo

`§F49` concluye que el defecto **«no contamina los resultados»** porque «las cifras del estudio proceden del
bloque `overall`, que sí calcula `tp / (tp + fn)` y es **inmune** al problema». El razonamiento es que al
aparecer `tp` en numerador y denominador el sesgo se cancela.

**No se cancela: se atenúa.** Con referencia {A, B, C} y extracciones A, A′, B —las dos primeras casando con
A— resulta `tp = 3`, referencias casadas {A, B} y `fn = 1`. El `overall` da `3/4 = 0,750` cuando lo correcto
es `2/3 = 0,667`. `tp` infla el numerador y **`fn` no compensa**, porque se calcula sobre referencias
distintas.

La prueba empírica es la propia corrección: **si `overall` fuera inmune, recalcular no cambiaría nada**, y
cambia. Sobre los 26 grupos publicados, el F1 sube **+0,160 pp de media** y **+1,287 pp** como máximo, siempre
al alza, con **409** emparejamientos duplicados (`§F81`, `§F81.bis`).

### Lo que queda en pie de cada hallazgo

| Afirmación | Estado |
|:---|:---|
| El mecanismo del doble conteo (`§F49`, `§F81`) | **Correcto**, y descrito igual en ambos |
| La exhaustividad por tipo pasa de 1,0 (`§F49`) | **Correcto**: 197 registros, máximo 2,444 |
| «El bloque `overall` es inmune» (`§F49`) | **Falso.** Atenúa el sesgo, no lo elimina |
| «Ninguno afecta a las cifras publicadas» (`§F49`) | **Falso**, aunque el efecto es pequeño: +0,160 pp de media |
| La cuantificación del efecto residual (`§F81`) | **Correcta y nueva**; es lo único que `§F81` aporta |
| El defecto persiste y hay que decidir cuándo corregirlo (`§F81`) | **Falso.** Ya está corregido en la rama de la re-corrida desde el 2026-09-08 |

### Consecuencias prácticas

- **La decisión 8 se reformula.** Preguntaba si corregir el evaluador y cuándo; ya está corregido y la
  re-corrida usa la versión corregida. Lo que queda por decidir es **si el informe declara el defecto de los
  datos antiguos** mientras conviven con los nuevos.
- **La re-corrida no arrastra el defecto**, y ahora está probado contra la fuente: su `tp + fn` de N=120 vale
  exactamente **2 × (549, 750, 517)**, la anotación de los **113** artículos no contaminados, sin un solo
  acierto de más.
- **Pero no puede comprobarse registro a registro**, porque la re-corrida **no entrega
  `detailed_results.json`** y las métricas por tipo viven ahí. Es una razón más para insistir en el pedido de
  `PEDIDO-COMMITEAR-BARRIDO-Y-DETALLE-20260908.md`.

### La lección

Antes de escribir un hallazgo hay que **buscar si ya está escrito**, con un `grep` por el mecanismo y no solo
por el número de sección. Y al leer un hallazgo antiguo, su conclusión tranquilizadora —«no afecta a las
cifras publicadas»— merece la misma comprobación que una alarmante: aquí bastaba un ejemplo de tres entidades
en una servilleta para ver que la inmunidad no se sostenía, y sobrevivió dos días sin que nadie lo hiciera.

---

## §F83 — Los contrastes de robustez no tenían herramienta, y al escribirla apareció un adelanto que conviene mirar

**2026-09-09, 03:3x.** Los tres artefactos de `results/ROBUSTEZ_ESTADISTICA_20260908/` —Friedman, post-hoc
pareado y potencia— sostienen `§F75`, `§F76` y `§F77`, y con ellos la **decisión 7**, que pregunta si el
informe adopta el post-hoc apropiado al diseño. Se calcularon a mano en una sesión y **ningún script los
reproducía**: `verificar_informe.py` los lee, pero nadie los genera.

Eso los convertía en un callejón sin salida. Cuando la re-corrida sustituya los datos, esos tres hallazgos
habría que rehacerlos desde cero, y la decisión 7 no podría actualizarse.

**Escrita `tools/robustez_estadistica.py`**, que calcula ambos contrastes desde un CSV consolidado. Validada
con `--validar`, que exige reproducir lo publicado: **χ² = 1169,2327 con 25 grados de libertad y 8 de 13
significativos tras Holm**, sin una sola discrepancia. La herramienta calcula lo mismo que se calculó a mano.

### El adelanto, y hay que leerlo con cuidado

Ejecutada sobre los **once** modelos que la re-corrida lleva entregados —el consolidado provisional del
ensayo de fusión— el resultado cambia mucho:

| | Datos publicados (13 modelos) | Re-corrida provisional (11 modelos) |
|:---|---:|---:|
| Friedman χ² | 1 169,23 | 1 131,62 |
| Significativos tras Holm | **8 de 13** | **2 de 11** |
| Mayor Δ | +14,52 pp (`nemotron-mini:4b`) | +6,73 pp (`llama3.2:latest`) |

Los dos que sobreviven son `llama3.2:latest` (+6,73) y `gemma4:12b-mlx` (+2,29). Dos más quedan **al borde**:
`gemma4:latest` con Holm = 0,0529 y `mistral-nemo:latest` con 0,0520, este último con efecto **negativo** de
−4,29 pp.

**Tres advertencias, y son importantes.**

1. **Faltan dos modelos, y uno de ellos es el de mayor efecto.** `nemotron-mini:4b` daba +14,52 pp y era el
   más significativo de todos; `deepseek-r1:1.5b` sigue en curso. Con los trece la fotografía puede cambiar,
   y precisamente en la dirección que más importa, porque ambos son de los pequeños.
2. **Esta cifra no debe citarse todavía en ninguna parte.** Es un adelanto de un consolidado provisional
   construido en un directorio temporal para ensayar la fusión, no un resultado del estudio.
3. **Lo que sí se puede afirmar ya** es que el efecto del RAG sobre el corpus corregido es **bastante menor**
   que sobre el defectuoso, y que la tesis de la proporcionalidad inversa se apoyará en menos modelos. El
   sentido no se invierte —el que más gana sigue siendo de los pequeños— pero la magnitud se reduce.

Cuando lleguen los trece, `CIERRE-RECORRIDA-PROCEDIMIENTO.md` debe incluir la ejecución de esta herramienta
junto al `merge_and_analyze.py`, y §5.3.1 habrá de reescribirse con las cifras que salgan.

---

## §F84 — El respaldo del analizador rescata casi siempre, y donde no lo hace está concentrado

**2026-09-09, 04:1x.** La quinta verificación del protocolo pide cruzar `parse_method` con el resultado para
saber si el respaldo **rescata contenido o encubre un fallo**. Al hacerlo en dos modelos salió lo contrario en
cada uno: en `mistral-nemo:latest` los 44 respaldos puntuaban casi como las filas directas, y en
`deepseek-r1:1.5b` los 4 puntuaban **cero los cuatro**. Conviene entonces mirarlo entero.

Sobre las **36 corridas** entregadas de la re-corrida:

| Ruta de análisis | Filas | F1 medio | Con `recall = 0` |
|:---|---:|---:|---:|
| `direct_json` | 1 002 | 67,95 | 11 |
| `codeblock` | 231 | 30,96 | 11 |
| `fallback` | **57** | **49,90** | **6** |

**Lo que dice.** El respaldo se usa poco —57 filas— y cuando se usa **rescata**: 49,90 de F1 medio está lejos
del cero que tendría si solo encubriera fallos, aunque por debajo de las filas analizadas directamente.
Solo **6 de los 57** quedan en cero, y **5 están concentrados**: los 4 de `deepseek-r1:1.5b` y 1 de
`gpt-oss:20b`. En el resto de modelos el respaldo funciona.

**El caso de `mistral-nemo` merece leerse aparte**, porque concentra 44 de los 57. Sus respaldos dan 55,27
frente a 59,56 de sus filas directas, y **42 de los 44 son del modo KB RAG**: el prompt de recuperación le
hace emitir un JSON que el analizador directo no lee en el 35 % de los casos, contra el 1,7 % de su línea
base. Pero **su caída de F1 no la causa eso**: entre las filas directas, KB RAG da 57,47 y la línea base
60,95.

**El `codeblock` no es un fallo.** Sus 231 filas son casi todas de `deepseek-r1:1.5b`, que envuelve su salida
en bloques de código; su F1 medio bajo refleja que es el peor modelo del estudio, no que la ruta falle.

### Por qué importa la distinción

Porque «hay respaldos» no significa nada por sí solo, y el número puede leerse de tres maneras opuestas: como
un fallo del modelo, como un rescate del arnés o como un rasgo del formato de salida. Aquí se dan las tres a
la vez en modelos distintos. **La única lectura válida es cruzarlo con el resultado**, que es exactamente lo
que el protocolo de seguimiento pide y lo que ninguna cifra agregada de `parse_method` puede sustituir.

---

## §F85 — Un `TypeError` hundió la línea base de `nemotron-mini` y un tercio de su mejora es artefacto

**2026-09-09, 04:4x.** El barrido de sustitución terminó a las 01:06 con los trece modelos, y el equipo de
48 GB publicó el consolidado `ANALISIS_CONJUNTO_20260909` (F = 121,56) declarando **«39/39 válidas»**. La
primera verificación del protocolo dice otra cosa.

`nemotron-mini_4b__N120` tiene **18 filas con `parse_method='failed'`**, las primeras de todo el barrido, y
**no están repartidas: las dieciocho caen en `_baseline` y ninguna en `_kb_rag`**. Todas con latencia 0, cero
tokens por segundo y dos reintentos.

### No es infraestructura, es un fallo de código

El registro de la corrida lo dice literalmente:

```
Attempt 1/3 failed for model 'nemotron-mini:4b': 'list' object has no attribute 'items'   (x22)
Attempt 2/3 failed ...                                                                    (x18)
Attempt 3/3 failed ...                                                                    (x18)
```

Es un `TypeError` en **`src/llm_runner.py:167`**, dentro de `_normalize_keys(parsed: dict)`: el modelo
devuelve una lista donde el código espera un diccionario y llama a `.items()`.

> **Corrección del 2026-09-10.** Este párrafo atribuía el fallo a `providers/ollama.py`, y **ese fichero no
> existe**: `src/providers/` contiene `__init__.py`, `anthropic_provider.py`, `base.py` y `factory.py`. El
> sitio real es `src/llm_runner.py:167` —`for k, v in parsed.items()`—, dentro de una función cuya firma
> **declara** `parsed: dict` y no comprueba nada. Se detectó al preparar el encargo de cierre del equipo
> remoto: la instrucción habría mandado a buscar en un fichero inexistente. Veintidós registros lo encontraron, cuatro se recuperaron al reintentar y
dieciocho agotaron los tres intentos. **La quinta verificación del protocolo lo habría clasificado mal**: la
firma —latencia 0 y cero tokens— es la del rechazo de infraestructura, y no lo es; hay que abrir el registro
para verlo.

### El efecto, y va todo en la misma dirección

| | Con las fallidas | Sin ellas |
|:---|---:|---:|
| `nemotron-mini:4b_baseline` | 26,31 | **30,97** |
| `nemotron-mini:4b_kb_rag` | 40,55 | 40,55 |
| **Δ del RAG** | **+14,23 pp** | **+9,72 pp** |

Las dieciocho puntúan 0,00 y entran en la media. Como caen todas en un solo brazo, **el sesgo no se cancela**:
**un tercio de la mejora atribuida a la recuperación en este modelo es la línea base hundida por un fallo de
software**. Y `nemotron-mini:4b` es el mayor efecto del estudio y uno de los dos significativos.

El consolidado publicado **incluye 17 de esas 18 filas** —la decimoctava es un ejemplar contaminado y ya se
excluía—, de modo que F = 121,56 y cuanto cuelgue de ella arrastran el defecto.

### Lo que sí se sostiene

Comprobado con el post-hoc pareado en los dos escenarios: **`nemotron-mini` sigue siendo significativo**, con
Holm ≈ 0 incluyendo las fallidas y **0,0016** excluyéndolas. Sigue siendo el mayor efecto. **La conclusión no
cambia; la magnitud sí**, y es una cifra que el informe publica.

Conviene decir también qué no acredita la comprobación: excluir las fallidas deja el diseño en **96**
registros completos en lugar de 113, lo que debilita todos los contrastes. Sirve como diagnóstico del sesgo,
**no como sustituto de la medición**. El remedio es re-ejecutar ese brazo.

### Hasta dónde llega el defecto, comprobado

Tres comprobaciones acotan el daño, y conviene tenerlas porque un defecto sin contorno se contagia a la
lectura de todo lo demás.

1. **Los datos publicados no están afectados.** El consolidado `ANALISIS_CONJUNTO_20260907`, con sus 3 120
   filas, tiene **cero** `parse_method='failed'`; sus rutas son `direct_json` (2 556), `codeblock` (452) y
   `fallback` (112). El Δ de +14,52 pp que publica la Tabla 7 **no arrastra este problema**.
2. **Ningún otro modelo de la re-corrida lo sufre.** Buscado el mensaje en los registros de las treinta y
   nueve corridas: **58 ocurrencias, todas en `nemotron-mini_4b__N120`**. Es además el **único** error
   repetido de todo el barrido; los demás registros no traen ni uno.
3. **Ningún otro corpus del mismo modelo lo sufre.** Sus corridas de N=30 y N=15 tienen cero fallos, lo que
   es coherente con la explicación del prompt: son pocas muestras y el fallo aparece en torno al 15 % de los
   artículos.

De modo que el remedio es acotado: **un brazo de un modelo de un corpus**, ciento veinte artículos de
inferencia.

### La lección, y ya es la tercera de la misma familia

El commit de cierre declaró «39/39 válidas» sin comprobar la primera verificación del protocolo, que es
contar `parse_method='failed'` y es una línea de código. Un barrido que termina no es un barrido válido, y el
único momento en que ese recuento cuesta algo es cuando no se hace.

Y una precisión sobre `§F84`: allí concluí que el respaldo «rescata casi siempre». Sigue siendo cierto —los
respaldos no son el problema aquí—, pero aquel análisis se hizo **antes** de que llegara este modelo y por
tanto no incluía sus 18 fallos. `parse_method='failed'` es una categoría distinta del respaldo, y es la que
hay que mirar primero.

---

## §F86 — Sobre el corpus corregido, la proporcionalidad inversa no se sostiene

**2026-09-09, 05:4x.** §5.3.1 sostiene la tesis central del trabajo: que el beneficio de la recuperación es
inversamente proporcional a la capacidad del modelo, y que «se anula o revierte en los de mayor capacidad».
La sostiene con una correlación entre el F1 de la línea base y la mejora que aporta el RAG: **Spearman
−0,5165 (p = 0,0707) y Pearson −0,6004 (p = 0,0300)**.

Recalculada sobre el consolidado de la re-corrida completa, con los mismos trece modelos:

| | Publicado | Re-corrida |
|:---|---:|---:|
| Spearman ρ | −0,5165 (p = 0,0707) | **−0,0879 (p = 0,7752)** |
| Pearson r | −0,6004 (p = 0,0300) | **−0,5266 (p = 0,0645)** |

**El coeficiente de rangos, que es el robusto, se va a cero.** No queda relación monótona: ordenados los
trece modelos por capacidad, los incrementos van +0,03, −4,29, +6,73, −0,05, +2,31, +0,69, +2,53, +1,67,
+2,29, +0,97 y +0,81 desde el sexto puesto en adelante. No hay tendencia que leer ahí.

### El coeficiente lineal descansa en un solo punto

Repetido el cálculo retirando cada modelo por turno:

| Se retira | Pearson r | p |
|:---|---:|---:|
| *ninguno* | −0,5266 | 0,064 |
| `nemotron-mini:4b` | **+0,0120** | **0,971** |
| cualquier otro | entre −0,52 y −0,67 | 0,02 – 0,08 |

**Quitar `nemotron-mini:4b` no debilita la correlación: la anula.** Con los otros doce modelos el
coeficiente es prácticamente cero y de signo contrario. Ningún otro punto tiene una influencia comparable.

Y ese punto es precisamente el que `§F85` señala: su Δ de +14,23 pp incluye diecisiete registros que puntúan
cero por un `TypeError`. Con la corrección aproximada su Δ baja a +9,58 y la correlación se debilita todavía
más —Pearson −0,4035 con p = 0,1716—.

### La afirmación que queda desmentida

«El beneficio se anula o revierte en los de mayor capacidad» **es falsa sobre el corpus corregido**. Los cinco
modelos de mayor capacidad tienen **todos** mejora positiva:

| Modelo | F1 base | Δ |
|:---|---:|---:|
| `gemma4:31b-cloud` | 82,13 | +0,81 |
| `gemma4:31b-mlx` | 81,47 | +0,97 |
| `gemma4:12b-mlx` | 77,67 | +2,29 |
| `gpt-oss:20b` | 75,41 | +1,67 |
| `gemma4:latest` | 75,33 | +2,53 |

Ninguno revierte, ninguno se anula. Lo que ocurría en los datos antiguos —los grandes con Δ negativo— era del
corpus defectuoso, y `§F68` ya lo había anticipado con los primeros modelos rehechos.

### Reproducible, que al escribirlo no lo era

Las cifras de este hallazgo se calcularon a mano, **el mismo defecto que `§F83` vino a corregir** para el
Friedman y el post-hoc. Subsanado: `tools/robustez_estadistica.py` calcula ahora también la correlación y el
análisis de influencia, y el artefacto está en
`results/ROBUSTEZ_ESTADISTICA_20260909/robustez.json`.

```sh
repos/ner-llm-entity-benchmark/venv/bin/python tools/robustez_estadistica.py \
    repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_20260909/merged_results.csv
```

Validada además contra el consolidado antiguo con `--validar`: reproduce χ² = 1169,2327, los ocho de trece y
la ρ de Spearman de −0,5165. **Una salvedad de 0,0002** que conviene conocer para no perseguirla: el Pearson
publicado es −0,6004 y la herramienta da −0,6002, porque aquel se calculó sobre los valores **redondeados** de
la Tabla 7 y esta lo hace sobre el CSV crudo. Comprobado reproduciendo ambos. Spearman coincide exactamente
porque trabaja con rangos, insensibles al redondeo.

### Corrección del 2026-09-09: son tres, no dos

Al escribir este hallazgo dije que los modelos con mejora significativa sobre el corpus corregido eran «los
dos únicos», nombrando `nemotron-mini:4b` y `llama3.2:latest`. **Son tres.** El post-hoc pareado con Holm
sobre el consolidado de trece modelos da:

| Modelo | Δ | Holm |
|:---|---:|---:|
| `nemotron-mini:4b` | +14,23 | 0,0000 |
| `llama3.2:latest` | +6,73 | 0,0011 |
| **`gemma4:12b-mlx`** | **+2,29** | **0,0005** |

Se me pasó `gemma4:12b-mlx`, que tiene un Δ modesto pero muy consistente entre registros —de ahí su p tan
baja— y por eso supera la corrección. Dos más quedan al borde: `gemma4:latest` con 0,0595 y
`mistral-nemo:latest` con 0,0577, este con efecto negativo.

El error estaba propagado al índice de defensa, al procedimiento de cierre y al inventario, y se ha corregido
en los cuatro sitios. **No cambia la conclusión** —el efecto sigue concentrado y sigue siendo mucho menor que
en el corpus antiguo— pero un recuento equivocado en el material de defensa es exactamente lo que no puede
quedarse.

**Y conviene no confundir dos cifras que ahora conviven:** el «ocho de trece» de `§F76` es sobre el corpus
**antiguo**; el «tres de trece» es sobre el **corregido**. El contraste es el mismo; lo que cambia es el
efecto que mide.

### Qué se puede afirmar todavía

Conviene no pasarse de frenada en la dirección contraria. Lo que los datos siguen sosteniendo:

- **El mayor beneficio lo obtienen modelos pequeños.** `nemotron-mini:4b` y `llama3.2:latest` son los dos
  únicos con mejora grande, y son de los más pequeños del estudio. Son también los **dos únicos
  significativos** tras el post-hoc pareado.
- **El beneficio no perjudica a los grandes**, que es una afirmación distinta y más débil que la publicada,
  pero verdadera y útil: la recuperación no degrada a ningún modelo de capacidad alta.
- **Lo que no se sostiene es la forma funcional**: que el beneficio decrezca de manera ordenada con la
  capacidad. Entre los once modelos de capacidad media y alta no hay ninguna tendencia.

### Consecuencia para el informe

§5.3.1 **no se arregla cambiando cifras**. La correlación es la que sostiene el argumento y ha dejado de ser
significativa por las dos vías. Hay que reescribir el apartado con lo que digan los datos: dos modelos
pequeños se benefician claramente, el resto apenas se mueve y ninguno de los grandes empeora. Es una
conclusión más modesta y perfectamente defendible; presentarla como la publicada, no.

**Y hay que esperar a que se resuelva `§F85` antes de escribir las cifras definitivas**, porque el punto que
más pesa en el análisis es justamente el afectado.

---

## §F87 — La conclusión 1 empareja cifras macro con cifras micro y las llama equivalentes

> **Ampliado el 2026-09-09.** El defecto tiene una **tercera** instancia, en la prosa del Anexo I, donde
> además contradice a la Tabla 19 que la acompaña. Ver **§F87.bis**.

**2026-09-09, 14:2x.** Verificando la afirmación de viabilidad —el umbral de F1 ≥ 70 % que fija la hipótesis—
aparecen las cuatro variantes que se pueden calcular sobre el mismo modelo y el mismo corpus:

| Variante | N=120 (`gemma4:31b-mlx_baseline`) | Dominio N=30 (`gemma4:31b-mlx`) |
|:---|---:|---:|
| Tres categorías, **macro** | **59,25** | **80,57** |
| Tres categorías, micro | 62,67 | 80,51 |
| Dos categorías, **macro** | **76,55** | **90,16** |
| Dos categorías, micro | 76,85 | 90,91 |

Las cuatro reproducen exactamente desde el detalle por registro.

### El problema

§3.3 declara la agregación por artículo —macro— como la **única** convención del trabajo: «se agregan dentro
de cada artículo y después se promedian entre artículos… Esa es la única convención». Y advierte, con la
cifra, de que la alternativa daría otro valor: «para el mejor modelo local sobre el corpus real, **62,67 %
frente al 59,25 % que aquí se publica**».

La **conclusión 1**, en cambio, dice: «con la medición restringida… **76,55 %** … y **90,16 %** … Bajo la
convención original, que puntúa también una categoría sin anotar, las cifras equivalentes son **62,67 %** y
**80,51 %**».

Pero **76,55 y 90,16 son macro, mientras 62,67 y 80,51 son micro**. No son «equivalentes»: cambian a la vez
el conjunto de categorías **y** la agregación, cuando la frase presenta solo el primer cambio. Bajo la
convención que el propio informe declara, los valores equivalentes serían **59,25 %** y **80,57 %**.

### Por qué importa más de lo que sugiere la magnitud

- **La discrepancia con la Tabla 7 es de 3,42 pp.** La conclusión dice 62,67 donde la Tabla 7 publica 59,25
  para el mismo modelo y la misma convención de categorías. Quien compare las dos páginas ve dos cifras.
- **Va en la dirección favorable.** El 62,67 hace que la convención original parezca menos mala de lo que la
  tabla dice, y por tanto que la corrección de `§F53` parezca aportar menos. No es una manipulación —§3.3
  publica el 62,67 abiertamente y explica de dónde sale— pero el efecto de usarlo ahí es ese.
- **El 80,51 contradice al cuerpo.** §5.3 y §5.4 usan **80,57** para el mismo dato. La misma cantidad aparece
  con dos valores en el mismo documento.

### Qué se propone, sin haberlo tocado

Sustituir en la conclusión 1 el par **62,67 / 80,51** por **59,25 / 80,57**, que son los valores de la
convención declarada y los que el cuerpo publica. Es neutro en extensión y elimina las dos discrepancias de
un golpe. **No se ha modificado**: es una conclusión y la decisión es del autor —queda como la **decisión
13**—, aunque conviene decir que aquí no hay criterio que ejercer, solo una inconsistencia que resolver.

Si se prefiriera conservar el 62,67 por alguna razón, entonces habría que decir que cambia también la
agregación, y §3.3 tendría que dejar de llamar «única» a la macro.

## §F87.bis — El mismo defecto está en el Anexo I, y ahí contradice a su propia tabla

**2026-09-09.** Al preparar la propagación a los `.docx` se encontró una **tercera** instancia del defecto
de §F87, que ni la decisión 13 ni la comprobación cubrían. Está en la prosa del Anexo I:

> «El mejor modelo local sobre este corpus, `gemma4:31b-mlx`, **pasa de 62,67 % a 76,55 %** de F1 y supera
> el umbral de 70 %…»

El **76,55** sale de la Tabla 19, que es macro. El **62,67** es micro. La fila de esa misma tabla dice
`59.25 → 76.55`, es decir **+17,30**, mientras la prosa insinúa +13,88. El emparejamiento es incomparable y
la cifra de partida no es la que publica la tabla que está tres líneas más arriba.

Lo que agrava el caso respecto de la conclusión 1 es que **§3.3 advierte exactamente de esto**:

> «…mezclarlas haría incomparables las cifras del texto con las de sus propias tablas.»

El Anexo I hace lo que §3.3 prohíbe, y con la tabla que tiene al lado.

**Las tres apariciones de 62,67 en el informe no son equivalentes**, y conviene no tratarlas igual:

| Línea | Dónde | Juicio |
|---:|:---|:---|
| 289 | §3.3, declarando la agregación | **Legítima.** Cita la alternativa para descartarla, y es la que advierte del riesgo |
| 487 | Conclusión 1 | Defecto §F87, ya declarado, decisión 13 |
| 1095 | Prosa del Anexo I | Defecto, **nuevo**: contradice a la Tabla 19 que la acompaña |

**Por qué sobrevivió.** La comprobación `c_agregacion` examinaba la conclusión 1 y nada más: cuatro
elementos, los dos casos por sus dos agregaciones. Un defecto situado fuera de esa ventana era invisible por
construcción, que es §L47 otra vez. Extendida hoy, la comprobación mira **cinco** elementos y lo detecta;
probada por mutación en los dos sentidos —con 62,67 marca, con 59,25 deja de marcar y los otros dos fallos
siguen—. Queda declarada bajo la decisión 13, ampliada a esta tercera instancia.

**Lección operativa.** Un defecto de agregación no aparece una vez. Cuando se encuentre uno, hay que
**enumerar todas las apariciones de la cifra** y juzgar cada una por separado, porque algunas serán
legítimas y tratarlas en bloque introduce un error nuevo. Aquí, sustituir las tres habría estropeado §3.3.

## §F88 — Mecanizada la comparación de cifras, aparece una cuarta obsoleta que a mano no salió

**2026-09-09.** Encontradas a mano tres cifras titulares obsoletas en los `.docx`, quedaba la pregunta que
importa: **¿son las únicas?** Encontrar defectos de uno en uno acredita que se miraron esos, no que no haya
más. `tools/desfase_cifras_docx.py` compara **todas** las cifras decimales de los dos lados.

**Resultado sobre el `.docx` canónico:** 705 cifras distintas examinadas, 273 solo en el `.docx` y 218 solo
en el Markdown. Clasificadas por dónde caen, el número se vuelve interpretable:

| | Total | En filas de tabla | Fuera de tablas |
|:---|---:|---:|---:|
| Solo en el `.docx` | 273 | 269 | **4** |
| Solo en el Markdown | 218 | 206 | 12 |

Las 269 confirman lo ya sabido: las tablas de resultados están sustituidas en bloque, no desfasadas en
algunas celdas. Y de las **4** de prosa, tres eran las conocidas —76,85, 90,91, 81,45— y la cuarta era nueva:

**El `5.33` de la Tabla 4.** La columna Tok/s/B de las dos filas de `gemma4:latest` decía 5.33 en los tres
`.docx`. Los datos dan **5.80**: la media de `tokens_per_sec` en `ablacion_n15_REMOTO` es 52,16 sobre 9 000
millones de parámetros, con n=15 en cada configuración, y las cuatro configuraciones dan 5,80. El 5,33
exigiría 47,97 tok/s, que no sale de ninguna. A diferencia de la Tabla 19, la Tabla 4 **coincide con el
Markdown en todas sus demás celdas**, de modo que era parcheable sin dejar una fila incoherente. Corregido.

### Dos defectos de la propia herramienta, y los dos los delató un control

**Primero: `<w:t[^>]*>` encaja con `<w:tcPr>`.** El patrón parece específico y no lo es: `w:t` seguido de
`[^>]*` acepta `cPr`, y también `<w:tc>` y `<w:tbl>`. El resultado era que el texto «visible» arrastraba
marcado XML. **Lo delató la herramienta a sí misma:** imprimía como contexto de una cifra
`<w:jc w:val="left"/>…<w:t>43.29`. Hay que exigir que tras `w:t` venga `>` o un espacio.

**Segundo: contar lindes con dígitos no cuenta números partidos.** La primera versión medía los números
partidos entre runs como `dígito SEP dígito` y daba **257**. Pero en una fila de tabla, la celda `43.29`
seguida de `38.91` encaja con ese patrón y no hay nada partido. La prueba correcta es que la unión forme un
decimal válido y que **ninguno de los dos lados sea ya un decimal completo**. Con eso da **1**, que es
exactamente la única reparación cross-run que la prueba en seco de las reglas había necesitado. Las dos
mediciones son plausibles y difieren en 257 veces.

### La trampa de la celda: `5.33` está tres veces, y una es `35.33%`

Corregir la Tabla 4 con una regla de subcadena `5.33` habría convertido, en otra tabla, un `35.33%` en
`35.80%`. Es la misma clase de error que `<w:t[^>]*>`: un ancla que parece específica y no lo es.

Por eso `tools/docx_replace_terms.py` tiene ahora la opción **`celda_exacta`**, que solo reemplaza los
`<w:t>` cuyo contenido **entero** es el buscado. Verificada con un control en los dos sentidos: sin la
opción la regla alcanza **3** ocurrencias, con ella **2**, y el `35.33%` queda intacto. La opción hará falta
igual para reemplazar la Tabla 19, donde todas las celdas son numéricas.

**Lo que queda.** Tras corregir el 5,33, las únicas divergencias de prosa son las **tres** acopladas a la
Tabla 19, ya especificadas en `tools/terms_restringido.json` para la tanda de maquetación. Ver
`PROPAGACION-PENDIENTE-DOCX-20260908.md`.

## §F89 — Siete `acceptance_status.json` quedaron con el veredicto de antes de la corrección, y uno invierte el orden

> **Ampliado el 2026-09-09.** El mismo desfase alcanza a los `statistical_report.md` por corrida, y allí
> es peor: **42 grupos en 9 corridas**, con intervalos y veredictos calculados sobre las cifras viejas. La
> tesina **no** está afectada, y hay un control que lo acredita. Ver **§F89.bis**.

**2026-09-09.** Al verificar la mitad `kb_rag` de la re-corrida de `gemma4:12b-mlx` apareció que la cifra
que el equipo remoto había reportado, **0,5929**, no está ni en el CSV ni en el resumen de la corrida, que
dan **0,5846**. El origen es `acceptance_status.json`, que sigue declarando
`overall_f1: 0.5929285920482852`.

`src/main.py` escribe ese fichero al cerrar la corrida. La corrección de puntuación del 2026-09-06 rehizo
los `benchmark_summary.json` pero **no** los `acceptance_status.json`. Mecanizado en
`tools/derivados_desfasados.py`, el defecto no es aislado: **7 de 17** corridas están desfasadas, y en las
siete la cifra vieja es la **más alta**, que es la firma de la corrección.

| Corrida | `acceptance` | Resumen corregido |
|:---|---:|---:|
| `afectados_thinking_n120_REMOTO` | 0,592929 | **0,584595** |
| `benchmark_balanced_120_20260824_173017` | 0,394452 | **0,361119** |
| `benchmark_n120_REMOTO` | 0,549147 | **0,507480** |
| `excluidos_n120_REMOTO` | 0,596448 | **0,438386** |
| `gemma4_31b_cloud_n120_REMOTO` | 0,626804 | **0,623841** |
| `nemotron_rerun_n120_REMOTO` | 0,437837 | **0,371170** |
| `qwen3_nothink_n120_REMOTO` | 0,531255 | **0,514588** |

### Lo que no está afectado, y conviene decirlo antes

**Las métricas del estudio no lo están.** Solo `src/dashboard.py` lee este fichero, y es visualización;
ninguna etapa del análisis lo toca. El informe, además, ya cita las cifras correctas: su Anexo I trae
**56,18** y **58,46** para las dos mitades de `gemma4:12b-mlx`, y no hay en él ni un 59,29 ni el 11,21 de la
corrida antigua.

### Y lo que sí es grave: un orden invertido

En `gemma4_31b_cloud_n120_REMOTO` el fichero no solo trae la cifra vieja, sino que declara
`best_model: gemma4:31b-cloud_kb_rag` con 0,6268, cuando el resumen corregido da mejor al
**`..._baseline`** con 0,6238 y sitúa a `kb_rag` en 0,6185. **El fichero afirma lo contrario de lo que
sostiene el informe** sobre el modelo grande y el RAG. Quien lo abriera, o quien mirara el cuadro de mando,
vería una inversión del resultado que el trabajo defiende.

**Por qué sobrevivió.** Un fichero derivado que nadie lee no da señales: no rompe nada, no aparece en un
`git status` sucio y su contenido es internamente coherente — es la firma de §F59 y de la regla de que una
cifra estable no acredita una medición correcta. Lo destapó no una revisión del fichero, sino el **cotejo de
una cifra reportada contra su fuente primaria**, que es el criterio 2 del protocolo de monitorización.

**Reparto.** `acceptance_status.json` **afirma**, no atestigua, de modo que se corrige y no se conserva como
está; pero es artefacto de la corrida y lo rehace quien la ejecutó. Encargado al equipo remoto en
`CURRENT-TASKS §3.bis.18`, con el contenido exacto que cada uno debe declarar. La herramienta no escribe.

## §F90 — Las cuatro cifras sin origen no reproducen, pero la conclusión que sostienen sí

**2026-09-09.** El único bloqueante del `TODO §10` que seguía abierto son cuatro filas de configuraciones de
prompt en `BENCHMARKS.md` cuyas cifras «no son trazables a ningún artefacto». Rastreadas hoy hasta donde
llega la evidencia.

**No están en ningún dato.** Buscadas en todo el repositorio: las apariciones de `0.7169` y `0.6482` en CSV
son valores de registros sueltos, no agregados; las demás son documentos que discuten este mismo problema.
La corrida candidata no tiene respaldos `.bak`, y su propio `benchmark_summary.json` coincide con el CSV al
cuarto decimal, de modo que tampoco hay un desajuste interno que las explique.

**Pero se pueden situar.** La corrida más cercana es `kleptotrace_20260727_110454` (N=15), a **menos de 0,02
en las tres columnas** de las cuatro filas, y las latencias siguen el mismo patrón (256,61 · 191,87 · 84,70 ·
84,56 frente a 248,27 · 185,80 · 80,41 · 87,78).

**No es el delta de la corrección de puntuación.** El desplazamiento no es uniforme: en las dos filas de
*few-shot* la cifra publicada es **más alta** que la reproducible y en las de *zero-shot* **más baja**. Una
corrección de puntuación mueve todas en el mismo sentido, como se ve en las siete corridas de §F89. Éstas
proceden de un estado de los datos que ya no existe.

### Lo que decide el asunto

Las tres fuentes dan el **mismo orden**:

| Fuente | Orden |
|:---|:---|
| `BENCHMARKS` (sin origen) | fs-es > zs-es > zs-en > fs-en |
| `kleptotrace_20260727_110454` | fs-es > zs-es > zs-en > fs-en |
| `ablacion_n15_REMOTO` | fs-es > zs-es > zs-en > fs-en |

**La conclusión que la tabla sostiene se reproduce desde dos corridas independientes; lo que no reproduce son
los decimales.** Eso convierte el bloqueante en una elección barata: sustituir las cuatro filas por las
cifras de `kleptotrace` deja la tabla trazable **sin cambiar ninguna conclusión**, y conserva la fila, que es
lo que la política aditiva exige. Es la **decisión 4**, cuya recomendación se actualiza a esa opción.

**Lo que hay que retener del caso.** Una cifra que no reproduce no implica que la afirmación que sostiene sea
falsa, y conviene comprobar las dos cosas por separado. Aquí el reflejo defensivo —retirar la tabla— habría
sido la peor de las tres opciones: destruye una conclusión que los datos sí respaldan. El orden de las
comprobaciones importa: primero si el **dato** reproduce, después si la **conclusión** reproduce, y solo
entonces se decide qué hacer con la fila.

## §F89.bis — El mismo desfase, en un artefacto más consecuente: 42 grupos en los informes por corrida

**2026-09-09.** Al buscar de dónde salía el 0,5929 apareció que no solo lo trae
`acceptance_status.json`, sino también el `statistical_report.md` de la corrida, y ahí con
**intervalos de confianza y un veredicto** calculados sobre la cifra vieja:

```
| gemma4:12b-mlx_kb_rag | 120 | 0.5929 | 0.5583 | 0.6275 | 0.1915 |
| gemma4:12b-mlx_kb_rag | 0.5929 | 0.5779 | -0.0150 | Decreased |
```

Mecanizado junto a la comprobación anterior en `tools/derivados_desfasados.py` —antes
`derivados_desfasados.py`, renombrado porque el nombre ya no describía lo que hace—: de **79 grupos en 17
corridas**, **42 están desfasados, repartidos en 9 corridas**. Algunas diferencias no son de decimales:
`deepseek-r1:1.5b_rag_enhanced` declara 0,3516 donde el resumen da **0,1682**, más del doble.

A diferencia de los `acceptance_status.json`, aquí el desplazamiento **no** va siempre en el mismo sentido:
`qwen3:8b_baseline` de `afectados_thinking_n120_REMOTO` declara 0,4383 donde el resumen da 0,4438, es decir
**más bajo**. Son de estados distintos de los datos, no de una única corrección.

### El control que importa: la tesina no está afectada

`tools/generar_tabla7.py` lee un `statistical_report.md`, de modo que la pregunta obligada era si la Tabla 7
del informe bebe de uno de los desfasados. **No.** Lee el del **consolidado**, que `merge_and_analyze.py`
regenera desde los CSV fusionados, y el consolidado del estudio está al día: **26 de 26 grupos** coinciden
con `merged_results.csv`. El consolidado, además, se alimenta de `csv_path`, nunca de resúmenes ni de
informes por corrida.

Esa tercera comprobación es un **control positivo** y está en la herramienta a propósito: sin ella no se
distinguiría «el consolidado está bien» de «el consolidado no se ha mirado», que es §L57. Probada por
mutación en los dos sentidos: con un F1 alterado señala el grupo y sale con 1; retirada la cabecera de la
tabla dice **«NO COMPROBADO»** en lugar de dar por bueno el silencio.

### Y una trampa de lectura que costó una pasada

La primera versión del control daba **26 divergencias de 26**, todas con un «F1 = 120,0000». El patrón
`| grupo | número | número |` cazaba la **primera** tabla del informe, la de cobertura
(`| Modelo | Filas | record_id unicos | … |`), y no la de F1, que está más abajo. **Lo delató el valor
imposible repetido**: una divergencia real no da el mismo número absurdo veintiséis veces. Por eso la
búsqueda se ancla ahora a la cabecera `| Model | Sample Size (N) | Mean F1-Score |`.

Es la tercera vez en dos días que un patrón aparentemente específico caza otra cosa —`<w:t[^>]*>` con
`<w:tcPr>` en §F88, `5.33` con `35.33%` en el mismo—, y las tres veces lo destapó mirar la salida con
desconfianza, no releer el patrón.

## §F91 — El supuesto que sostiene el ANOVA principal no lo recalculaba nadie

> **Ampliado el 2026-09-09.** Cerrado este hueco, se enumeraron las demas afirmaciones estadisticas del
> informe: **ninguna** estaba cubierta, incluido el ANOVA titular. Las dos reproducen. Ver **§F91.bis**.

**2026-09-09.** §5 del informe publica que «la prueba de Levene no detecta heterocedasticidad (p = 0,18), lo
que con 3 120 observaciones sí es informativo». Esa p sostiene el supuesto de homocedasticidad del ANOVA que
da el **resultado titular del trabajo**.

Comprobado hoy: la cifra estaba persistida en `results/ANALISIS_CONJUNTO_20260907/levene.json` desde el
2026-09-08 y **ningún código la leía ni la recalculaba**. `grep` sobre `tools/` y `src/` da cero
coincidencias, y el verificador no la mencionaba. Es decir: un artefacto correcto, sin nadie que lo
comprobara, exactamente la situación de §F89 —pero en una cifra que el informe **publica**, no en un
derivado interno.

**Y no era hipotético.** La re-corrida pendiente de `nemotron-mini` (§3.bis.15) va a cambiar
`merged_results.csv`, y con él W y p. Sin comprobación, el informe habría seguido citando la p de un CSV
anterior. La mutación que retira las filas de un grupo lo demuestra: W pasa de 1,2475 a 1,2627 y p de 0,1842
a 0,1762.

### La comprobación, y por qué no usa scipy

Añadida como comprobación **30** del verificador, con **9 elementos examinados**: recalcula Brown-Forsythe
—Levene con centrado en la mediana, la variante robusta— desde `merged_results.csv` y lo contrasta contra
`levene.json` (W, p, grupos, observaciones, df1, df2), contra la p que el informe publica a sus dos
decimales, y contra las 3 120 observaciones que cita.

Está implementada **con la biblioteca estándar**, a propósito. `scipy` solo existe en
`repos/ner-llm-entity-benchmark/venv`, y una comprobación que solo corre dentro de un entorno concreto no
corre. La distribución F se evalúa por la beta incompleta regularizada con la fracción continua de Lentz.
**Verificada por tres vías independientes**, que dan el mismo resultado al cuarto decimal:

| Vía | W | p |
|:---|---:|---:|
| `scipy.stats.levene(center='median')` | 1,2475 | 0,1842 |
| Implementación en biblioteca estándar | 1,2475 | 0,1842 |
| `levene.json` persistido | 1,2475 | 0,1842 |

Probada por mutación en tres frentes, y los tres se detectan: cambiar la p del informe, cambiar la W del
artefacto, y cambiar los datos retirando las filas de un grupo, que es el caso realista.

### De paso: una herramienta que no podía ejecutarse

`tools/robustez_estadistica.py` moría con un `ModuleNotFoundError: No module named 'scipy'`, porque importa
scipy y el intérprete del sistema no lo tiene. La herramienta **no estaba rota** —en
`repos/ner-llm-entity-benchmark/venv` reproduce los artefactos publicados sin discrepancias—, pero un
traceback no dice dónde está el intérprete que sí la ejecuta. Ahora falla con la orden exacta.

Merece la pena retenerlo: **una comprobación que aborta con un traceback es indistinguible de una
comprobación que no existe**, y ésta llevaba así el tiempo que llevara sin scipy en el intérprete del
sistema.

## §F91.bis — Ninguna de las treinta comprobaciones recalculaba el ANOVA titular

**2026-09-09.** Cerrado el hueco de Levene, la pregunta obligada era cuántas más de las afirmaciones
estadísticas publicadas estaban en la misma situación. Enumeradas las del informe y cruzadas contra el
verificador, **ninguna figuraba por nombre**, incluida la que más pesa:

> «El ANOVA de una vía sobre los veintiséis grupos arroja **F = 38,2222** con p = 3,4453 × 10⁻¹⁶⁰»

Las treinta comprobaciones cubrían tablas, figuras, bibliografía, agregación y el protocolo de las corridas
fusionadas, pero **la F y la p del resultado principal no las tocaba nadie**.

**Ambas reproducen.** Recalculadas desde `merged_results.csv` con la biblioteca estándar: F = 38,2222,
p = 3,445331e-160, η² = 0,2360 sobre 26 grupos y 3 120 observaciones, df (25, 3094). Contrastado con
`scipy.stats.f_oneway`, que da lo mismo al cuarto decimal. La beta incompleta no se desborda a esa magnitud,
que era la duda razonable con un exponente de −160.

**El «dos de los trece» de Tukey también reproduce**, y es la afirmación que decide para qué modelos sirve el
RAG. Contadas las 325 comparaciones del informe del consolidado, de las 13 que enfrentan `baseline` con
`kb_rag` del mismo modelo hay exactamente **2** significativas, y son las dos que el informe nombra:

| Modelo | Δ | p ajustada | El informe publica |
|:---|---:|---:|:---|
| `nemotron-mini:4b` | +14,52 pp | ~0 | p<0,001 |
| `llama3.2:latest` | +10,82 pp | 0,0069 | p=0,007 |

**Y una distinción que conviene tener clara antes de la defensa:** `robustez_estadistica.py` da **8 de 13**
significativos, no 2. No es una contradicción — es Wilcoxon apareado con corrección de Holm, una prueba
distinta y menos conservadora, porque aprovecha el emparejamiento por artículo que Tukey ignora. Las dos son
ciertas sobre lo que dicen medir, y el riesgo está en citarlas como si fueran la misma cuenta.

Añadidas como comprobaciones **31** y **32**, con 5 y 8 elementos, y probadas por mutación en cinco y siete
frentes respectivamente.

### Dos trampas de emparejamiento, una en cada comprobación

**`rsplit('_', 1)` parte `_kb_rag` por dentro.** Da `gemma4:31b-mlx_kb` y `rag`, con lo que no empareja ni
una de las 13 y el recuento sale **cero**. La comprobación lo declara ahora como fallo explícito en lugar de
contar cero en silencio, y la mutación que renombra el sufijo lo confirma.

**Y una vacuidad propia, que la prueba por mutación destapó.** La primera versión de la comprobación de
Tukey comparaba el delta del artefacto contra un `0.1452` **escrito a mano en el código**. Alterar el
`+14,52 pp` del informe no hacía fallar nada: la comprobación no miraba el documento que decía comprobar.
De cinco mutaciones, cuatro se detectaban y esa no. Corregida para leer el delta del informe, ahora falla en
los dos modelos.

## §F91.ter — Cerrada la cobertura estadística: las cuatro p secundarias también reproducen

**2026-09-09.** Al cerrar §F91.bis quedaron declaradas abiertas cuatro p secundarias. Las cuatro reproducen,
y cada una desde una corrida distinta, que es lo que costó identificar:

| Dónde | Cifra publicada | Corrida | Reproduce |
|:---|:---|:---|:---|
| §5.2 | F = 1,1379 · p = 0,3417 | `ablacion_n15_REMOTO`, 4 configuraciones, N=60 | sí |
| §5.2 | F = 0,2235 · p = 0,6382 | `n30_rerun_REMOTO`, `gemma4:31b` vs `-mlx`, N=60 | sí |
| §5.3 y §6 | Δ = −0,43 pp · p = 0,9328 | `benchmark_balanced_120_…071207`, 4 config., N=480 | sí |
| §5.3 | ρ = −0,52 · p = 0,071 | ya cubierta por la comprobación 26 | sí |

**La tercera exigió trabajo, y el resultado conviene retenerlo.** El Δ de −0,43 pp reproduce de inmediato
como el contraste `fs-es` frente a `zs-en`, pero **la p no salía de ninguna prueba sobre ese par**: ni t
apareada (0,7019), ni t independiente ni Welch (0,8673), ni Wilcoxon (0,8661), ni Mann-Whitney (0,6287), ni
Kruskal (0,6280), ni Tukey ajustada (0,9982). Sale del **ANOVA de los cuatro grupos**, F = 0,1451 con
p = 0,9328 sobre N=480.

Es decir, el informe empareja en una frase un Δ de un contraste con la p de un ANOVA global. **No es un
error** —`FINDINGS §F31` ya lo declara y da también la t apareada de 0,7019, que esta comprobación
reproduce—, pero es un emparejamiento de alcances distintos y un tribunal puede preguntarlo. La comprobación
verifica las dos cosas **por separado**, para que quede visible cuál sostiene qué.

De paso: la t apareada que §F31 declara, 0,7019, la reprodujo mi cálculo antes de saber que estaba
documentada. Es la clase de coincidencia que da confianza en las dos.

### Y un hueco en mi propia comprobación, otra vez destapado por la mutación

La frase del efecto que se anula está **dos veces** en el informe, en §5.3 y en §6, con las mismas cifras.
La primera versión de la comprobación usaba `re.search`, que ve solo la primera: si la segunda divergiera,
nadie lo notaría. Es §L59 —«las mutaciones deben cubrir todas las apariciones»— aplicado a la comprobación
en lugar de a la prueba, y se detectó porque el helper de mutación **se negó a mutar** al encontrar dos
ocurrencias donde esperaba una.

Corregida con `re.finditer`, la comprobación pasa de 7 a **10 elementos** y cada fallo dice de qué aparición
habla. Probada mutando cada una por separado: las dos se detectan.

**Estado de la cobertura estadística del informe:** el ANOVA principal, Levene, el recuento de Tukey con sus
dos p, las tres ANOVA secundarias y la correlación de capacidad se recalculan todos desde los datos. No
queda ninguna afirmación estadística publicada sin comprobación.

## §F92 — La autoprueba decía «9 de 9» sobre 26 dependencias

**2026-09-09.** La autoprueba del verificador cerraba con «9 de 9: ningún artefacto puede faltar sin que se
note». La frase se lee como universal, y no lo era: **9 de los artefactos que ella misma lista**, mientras el
verificador cita **26 rutas** en su fuente. Es §L47 en su forma más cómoda de pasar por alto — el
denominador es el que la propia herramienta elige.

Enumeradas las dependencias y escondidas una a una, **siete no estaban vigiladas y su ausencia sí producía
un fallo atribuible**, de modo que podían añadirse sin más:

| Artefacto | Comprobación que falla al esconderlo |
|:---|:---|
| `ANALISIS_CONJUNTO_20260907/statistical_report.md` | el ANOVA titular |
| `ablacion_n15_REMOTO/benchmark_results.csv` | las ANOVA secundarias, y la Tabla 4 |
| `n30_rerun_REMOTO/benchmark_results.csv` | las ANOVA secundarias |
| `benchmark_balanced_120_…071207/benchmark_results.csv` | las ANOVA secundarias, y la taxonomía de §5.4 |
| `cloud_n15_limpio_20260905/benchmark_results.csv` | la Tabla 4 |
| `gemma4_31b_n15_REMOTO/benchmark_results.csv` | la Tabla 4, y las tablas 5, 6 y 8 |
| `results/benchmark_results.csv` | la Tabla 4 |

La autoprueba pasa de **9** a **16** artefactos vigilados, y de las 26 rutas citadas quedan 8 sin vigilar:
5 nombres genéricos que se resuelven en tiempo de ejecución, 1 ruta de directorio y **2 fuera a propósito**
—los respaldos rotos de la decisión 3, cuya comprobación es un AVISO declarado, de modo que esconderlos no
cambia nada y la prueba no podría atribuir el fallo—. Cero ficheros sin vigilar y sin motivo.

### Un cociente entre conjuntos que no están anidados es peor que ningún cociente

La primera corrección imprimía «cobertura: 15 de las 26 rutas que el verificador cita». Eso sugiere que los
15 vigilados son un **subconjunto** de las 26, y no lo son: varios artefactos —el de composición de falsos
positivos, el de mojibake, el de correlación— se construyen con variables y **no aparecen** en el recuento
de literales. El cociente daba una impresión de cobertura parcial cuando en realidad los dos conjuntos solo
se solapan.

Sustituido por la **diferencia real**, derivada de la fuente y clasificada: cuántas dependencias hay,
cuántas sin vigilar, y de qué clase es cada una. El denominador ya no se escribe a mano, que es §L63: una
cobertura con el denominador literal deja de ser cierta en cuanto se añade una dependencia, y calla.

## §F93 — Las treinta y tres comprobaciones no tenían puerta: corrían si alguien se acordaba

**2026-09-09.** `CLAUDE.md` manda ejecutar `tools/verificar_informe.py` antes de cada commit sobre el
informe. Comprobado hoy: **no había hook de pre-commit** y `core.hooksPath` estaba sin configurar. La regla
era una disciplina, no una puerta — y el código de salida se arregló el 2026-09-09 precisamente para que
pudiera serlo, con el razonamiento de que «una puerta que nunca abre no es una puerta». Faltaba el otro
lado: una puerta que nadie cuelga no es una puerta tampoco.

**Instalada** en `.githooks/pre-commit`, versionada, con tres propiedades deliberadas:

- **Acotada.** Solo se ejecuta si el commit toca el Markdown del informe, `tools/` o los datos de
  resultados. Un commit de documentación de coordinación no paga el coste.
- **Sin `--red`.** Sin red tarda menos de un segundo; con red, **36**, que es demasiado para una puerta de
  commit. Las URL se comprueban aparte.
- **Con salida de escape declarada.** `git commit --no-verify` la salta, y el mensaje dice para qué está:
  comprometer trabajo a medias, no silenciar un fallo. Si un fallo es aceptable se declara en
  `FALLOS_DECLARADOS` con su motivo y su responsable, que es lo que mantiene la puerta útil.

**Activación:** `core.hooksPath` es configuración **local**, de modo que un clon nuevo no tiene la puerta
aunque el hook esté versionado. Hay que ejecutar `git config core.hooksPath .githooks` en cada copia de
trabajo. Es una carga de la que conviene ser consciente: el fichero en git da la sensación de que el gate
existe, y no existe hasta que alguien lo apunta.

### Probada en los tres sentidos, y el primer intento falló por algo instructivo

| Caso | Resultado |
|:---|:---|
| Commit que toca `tools/` y está limpio | la puerta corre, pasa, el commit entra |
| Commit que altera el `F = 38,2222` del informe | **corta**, y nombra la comprobación del ANOVA |
| Commit que solo toca `CURRENT-TASKS.md` | la puerta no se ejecuta |

El primer intento del caso limpio **cortó**, y con razón: el fichero que había creado para la prueba estaba
**vacío**, y la comprobación de ficheros rastreados a cero bytes lo cazó entre 1 170 elementos. Es §F59
funcionando sobre un fichero de dos minutos de vida, y la demostración más convincente de que la puerta
sirve — no la que yo había preparado.

## §F94 — Los tres `.docx` nombran cuatro modelos excluidos, y la comprobación que lo vigilaba miraba solo el Markdown

**2026-09-09.** `CLAUDE.md` es tajante: los modelos excluidos «no pueden aparecer en el informe, en sus
anexos, en los datos agregados ni en los artefactos derivados. **Tampoco en una glosa que los declare
excluidos**: la exclusión se aplica, no se narra». La verdad de referencia es el PDF entregado al profesor
guía.

Comprobado hoy: el Markdown cumple —**cero** apariciones—, y los **tres `.docx`, el entregable canónico
incluido, nombran cuatro modelos excluidos en quince sitios**:

| Modelo | Apariciones en cada `.docx` |
|:---|---:|
| `nuextract` | 7 |
| `minimax-m3` | 4 |
| `gemini-3.1-flash-lite` | 2 |
| `gemma4-12b-mlx-q8-64k` | 2 |

**La exclusión se aplicó a la fuente y nunca se propagó.** Y la comprobación que existía para vigilarlo
—«sin modelos excluidos del estudio»— **examinaba solo el Markdown** y daba «ok» con 8 elementos. Es §L47 en
su versión más caro: la comprobación existía, pasaba, y miraba el artefacto que no se entrega. Extendida hoy
a los tres `.docx`, examina **35 elementos** y delata las doce apariciones.

### Inventario de las cuatro clases, que no se corrigen igual

| Sitio | Qué hay | Qué dice el Markdown | Corrección |
|:---|:---|:---|:---|
| Nota de la Tabla 4 | «Quedan fuera de la tabla los modelos excluidos del estudio (`nuextract:latest`, `gemini-3.1-flash-lite`, `minimax-m3`)» | **nada**: la frase no existe | eliminar la frase entera |
| Anexo, fila de fuentes | «Excluidos del estudio \| `nuextract:latest, gemini-3.1-flash-lite, minimax-m3`» | **nada** | eliminar la fila |
| Tabla de deltas | 2 filas: `nuextract:latest_baseline` y `_kb_rag` | no están | eliminar las 2 filas |
| **Tabla 19** | **7 filas** de modelos excluidos | no están | eliminar las 7 filas |

El Markdown no reescribió la glosa: **la eliminó**. Cero apariciones de «Quedan fuera de la tabla», de
«Excluidos del estudio» y de «modelos excluidos». La corrección del `.docx` es por tanto supresión, no
reformulación.

### Y de paso queda explicado el recuento de la Tabla 19

El `.docx` tiene **49 filas de datos** donde el Markdown declara **42 configuraciones**. La diferencia son
exactamente las **7** filas de modelos excluidos: 49 − 7 = 42. Es decir, la Tabla 19 del entregable no solo
trae cifras sustituidas (§F88) sino **siete filas que no deben existir**, y las dos cosas se arreglan en la
misma operación: reemplazar la tabla desde el Markdown la deja con 42 filas y con las cifras vigentes de una
vez.

**Estado:** declarado en `FALLOS_DECLARADOS` como **pendiente de corrección, no aceptado**, con su
inventario y su tanda. Se retira de esa lista al corregirlo, que es lo que mantiene la lista útil.

### Corrección aplicada el 2026-09-09

Aplicado a los tres `.docx`, con respaldo, en dos pasos y verificado despues:

| | Antes | Ahora |
|:---|---:|---:|
| Menciones de modelos excluidos | **15** | **0** |
| Tabla 15, filas de datos | 5 | **4** — idéntica al Markdown |
| Tabla 18, filas de datos | 24 | **22** |
| Tabla 19, filas de datos | 49 | **42** — el recuento que declara el Markdown |
| Leyenda de la Tabla 19 | «49 configuraciones» | «**42** configuraciones» |
| Glosa «Quedan fuera de la tabla…» | 1 | **0** |
| Emojis | 0 | 0 |
| Palabras | 18 347 | 18 262 |

Los tres paquetes abren y conservan sus 29 y 15 partes. El párrafo de la nota de la Tabla 4 queda «…no son
comparables entre filas; el índice Tok/s/B sí lo es. La columna «Parámetros» recoge…», que se lee bien y no
nombra a nadie.

**Lo que se hizo y lo que no.** Se **suprimió**; no se parcheó ninguna cifra. La distinción importa y es la
que autorizó a actuar hoy en lugar de esperar a la maquetación: cambiar un valor dentro de una fila cuyas
otras columnas están sustituidas deja una fila internamente incoherente, mientras **suprimir la fila entera
no altera las que quedan**. De modo que la conformidad con la lista cerrada se resuelve ya y el reemplazo de
valores sigue pendiente.

**Lo que sigue pendiente en esas tablas**, y conviene no darlo por hecho: a la Tabla 18 del `.docx` le faltan
**4 filas legítimas** —las de `nemotron-mini:4b` y `qwen3:8b`, en sus dos modos— y **2 de sus 22 filas
comunes traen valores distintos** de los del Markdown, las de `gemma4:12b-mlx`; las otras 20 coinciden. Y la
Tabla 19 conserva las cifras sustituidas de §F88. Las dos exigen reemplazo, no parcheo.

**Herramienta nueva:** `tools/docx_borrar_filas.py`, que suprime `<w:tr>` identificando la tabla por un
fragmento de texto que solo ella contiene y la fila por su primera celda, exigiendo el número de filas
esperado y sin tocar nada si no cuadra.

**Y un defecto que la propia operación destapó.** `docx_borrar_filas.py` y `docx_replace_terms.py` corrieron
en el mismo segundo sobre los mismos ficheros, y como las dos derivan el sufijo del respaldo de la marca de
tiempo, **la segunda sobrescribió el respaldo de la primera**: el `.bak` acabó guardando el estado intermedio
en lugar del original. No se perdió nada —el original estaba en git y en los respaldos de las 12:24 y las
12:31—, pero **un respaldo que se pisa no es un respaldo**. Las dos herramientas añaden ahora un contador, y
está probado: dos ejecuciones en el mismo segundo dan `.bak_…` y `.bak_…-2`.

**Consecuencia en la autoprueba, que confirma §L64.** Retirado el fallo de la lista de declarados, los tres
`.docx` **vuelven a ser vigilables**: la autoprueba pasa de «16 de 19, 3 bloqueados» a **19 de 19**. Era
exactamente lo que §L64 predecía, y sirve de comprobación de que el diagnóstico era correcto.

## §F95 — Propagadas las dos tablas y las doce cifras de prosa: cero cifras obsoletas en los entregables

**2026-09-09.** Al empezar el día, la comparación completa de cifras daba **273 candidatas a obsoletas** en el
`.docx` canónico (§F88). Hoy da **cero**.

| | Al empezar | Ahora |
|:---|---:|---:|
| Cifras del `.docx` ausentes del Markdown | **273** | **0** |
| Tabla 19: celdas que no coinciden con el Markdown | 254 de 294 | **0** |
| Tabla 18: filas que no coinciden | 2 de 22 | **0** |
| `76,85` · `90,91` · `81,45` (prosa) | 8 · 3 · 3 | 0 · 0 · 0 |
| `76,55` · `90,16` · `80,42` | 0 · 0 · 0 | 6 · 2 · 2 |
| Menciones de modelos excluidos | 15 | **0** |

Los tres paquetes abren, conservan sus 29 y 15 partes y siguen sin emojis.

### Lo que hizo posible reescribir una tabla entera con seguridad

Hace días decliné parchear la Tabla 19 con el argumento correcto: cambiar un `F1 restr.` sin cambiar el
`P restr.` de su lado deja una fila incoherente, peor que la que había. Ese argumento vale para un parcheo
**parcial**. Reescribir **todas** las celdas de la fila desde la fuente canónica no lo tiene, y las
condiciones que lo hicieron verificable fueron cuatro, comprobadas antes de escribir nada:

1. **Los conjuntos de filas coinciden exactamente**: 42 en el `.docx` y 42 en el Markdown, mismos nombres,
   ninguna sobra ni falta. Sin esa correspondencia no se habría intentado.
2. **Las filas se emparejan por su primera celda, no por su posición**, de modo que un cambio de orden no
   descoloca nada.
3. **Cada celda de destino tiene exactamente un `<w:t>`**: 294 en la Tabla 19 y 44 en la 18, comprobado.
4. **Todo o nada**: si una fila de la tabla no está en las reglas, o una regla no tiene fila, no se toca
   nada. Un reemplazo parcial es justo lo que había que evitar.

Y la verificación posterior es la que cierra el argumento: **las 294 celdas coinciden con el Markdown, una
por una**, en los tres documentos.

### Los valores no los escribí yo

`tools/generar_reglas_tablas_docx.py` deriva las reglas del Markdown canónico. Es §L63 aplicado a la
propagación: un valor copiado a mano en un fichero de reglas es una segunda fuente de verdad que deja de
coincidir sin avisar. El generador, además, **se niega a generar** si los conjuntos de filas no cuadran.

### Lo que sigue pendiente, para no darlo por cerrado

- **A la Tabla 18 le faltan 4 filas legítimas** —`nemotron-mini:4b` y `qwen3:8b`, en sus dos modos—. Su
  contenido no se puede propagar reescribiendo celdas, porque hay que **insertar filas**, y esa capacidad no
  existe. El generador lo declara en su salida y en el fichero de reglas.
- Las **dos figuras** y la **Tabla 20**, del inventario original.
- Diez cifras siguen «en el Markdown y no en el `.docx`»: están en pasajes reescritos que el `.docx` aún no
  tiene. Es propagación de texto, no cifras obsoletas.
- En §3.3 sigue pendiente partir el run en negrita para que resalte solo el porcentaje.

**Herramientas nuevas:** `tools/docx_reescribir_celdas.py` y `tools/generar_reglas_tablas_docx.py`.

### Reconstrucción de la Tabla 18 — 2026-09-09, cierre de §F95

La única pieza de §F95 que quedaba pendiente de las dos tablas está hecha. A la Tabla 18 del `.docx` le
faltaban **cuatro filas legítimas** —`nemotron-mini:4b` y `qwen3:8b`, en sus dos modos— y, al comprobar
dónde insertarlas, apareció algo que la inserción no habría resuelto: **el orden del `.docx` no era el del
Markdown**, que ordena por Δ descendente, y ni siquiera era una subsecuencia suya.

Insertar en el hueco correcto habría dejado las 26 filas en un orden que no es el de la fuente. Las dos
cosas se resuelven igual: **reconstruir el cuerpo** de la tabla desde el Markdown, generando cada fila desde
la plantilla del esqueleto XML más frecuente y en el orden de la fuente. La cabecera no se toca.

**Resultado, verificado en los tres documentos:** la Tabla 18 tiene **26 filas** e es **idéntica al Markdown
en contenido y en orden**. Las cuatro filas ausentes están presentes, los paquetes abren y siguen sin emojis.

`tools/docx_reconstruir_cuerpo.py` impone cuatro condiciones antes de escribir, y la cuarta es la que
importa: **una reconstrucción no puede perder información**. Si alguna fila del `.docx` no estuviera en el
Markdown, la herramienta no toca nada y la reporta — sería una fila que solo existe en el entregable, y
decidir qué hacer con ella no es cosa de una herramienta. Declara además, como AVISO, que el formato **por
fila** se normaliza al de la plantilla, con el recuento de esqueletos que había.

**Y una consecuencia de mi propio defecto anterior.** Ese AVISO salió con «2 esqueletos» porque las dos
filas que reescribí en la pasada anterior quedaron con un `xml:space="preserve"` que no necesitaban:
`docx_reescribir_celdas.py` lo añadía siempre. Corregido para añadirlo solo cuando el valor tiene espacios
que preservar. No tenía efecto visual —el documento ya trae 743 `<w:t>` con ese atributo de origen— pero
rompía la uniformidad estructural que una reconstrucción por plantilla aprovecha, y fue la propia
herramienta la que lo delató al contar los esqueletos.

**Estado de la propagación de cifras: cero obsoletas y cero tablas divergentes.** Quedan diez cifras solo en
el Markdown, todas en pasajes de texto reescritos que el `.docx` aún no tiene, más las dos figuras y la
Tabla 20.

## §F96 — La obligación de contar guiones y resaltes del `.docx` nunca se había cumplido

**2026-09-09.** `CLAUDE.md` obliga a que «quien produce el `.docx` y el PDF cuente guiones y resaltes del
cuerpo del documento generado y los compare con los de la fuente, porque el renderizador no debe añadir
énfasis». Comprobado hoy por primera vez.

**Guiones largos: bien.** 81 en el Markdown y **67** en el `.docx`. Menos, no más, de modo que no hay
énfasis añadido por esa vía.

**Resaltes: el `.docx` añade 17 en el cuerpo.** Y aquí el recuento ingenuo engaña: 273 tramos en negrita en
el `.docx` frente a 229 marcas `**...**` en el Markdown parece una diferencia de 44, pero clasificados por
dónde caen queda otra cosa:

| Dónde | Tramos que el Markdown no marca | Juicio |
|:---|---:|:---|
| Dentro de tablas | **76** | **legítimo**: Word pone cabeceras y celdas en negrita por estilo, y el Markdown no las marca |
| En encabezados | **0** | — |
| **En el cuerpo** | **17** | la limpieza de sobriedad que el `.md` hizo y el `.docx` no recibió |

Los 17 son el residuo de la pasada que llevó el Markdown de 164 negritas a 108. `CLAUDE.md` ya advierte que
«los recuentos absolutos no son reproducibles entre métodos de conteo distintos» —tres auditores dieron
19/108, 28/127 y 31/150 sobre el mismo texto—, y este caso lo confirma: **la cifra que importa no es el total
sino la diferencia clasificada**.

### Por qué la comprobación no exige que sean cero

Varios de los 17 parecen **encabezados de párrafo** del anexo —«Ejemplo few-shot 1 (caso persona
sancionada):», «Ejemplos few-shot de la configuración FS-ES»— y quitarles la negrita destruiría estructura.
Otros son frases enteras resaltadas que el Markdown ya desmarcó y que sí habría que limpiar. Son decisiones
de una en una, de la pasada de maquetación.

De modo que la comprobación **34** vigila que **no crezcan**, con el estado actual como umbral. Eso convierte
un pendiente en una línea de defensa: si alguien añade un resalte al entregable, se ve. Y si el recuento
**baja**, también avisa, pidiendo actualizar el umbral para que la comprobación siga vigilando desde el nuevo
estado en lugar de quedarse holgada. Probada por mutación en los dos sentidos, sobre el `.docx` real y con
restauración: añadido un resalte da 18 y lo reporta; retirado uno da 16 y pide bajar el umbral.

**Uno de los 17 es mío.** En §3.3 el Markdown resalta solo el porcentaje y el `.docx` tiene la frase entera
en negrita, porque el reemplazo de texto del 2026-09-09 escribió la cifra nueva **dentro** del run que ya
estaba resaltado. Arreglarlo exige partir el run, que ninguna herramienta del proyecto hace todavía.

### Y lo que la propagación de texto ya no puede resolver sola

Las diez cifras que siguen solo en el Markdown están en pasajes que el `.docx` **no tiene en ninguna
versión**: el χ² de medidas repetidas, la potencia y la *d* de Cohen, el rango de alucinación, la similitud
de siglas y las filas de la Tabla 20. Comprobado sonda a sonda: ninguna tiene contrapartida en el
entregable. No es propagación de cifras, es **inserción de párrafos y de una tabla nueva**, con decisiones
de posición y estilo que son de maquetación.

### Cerrada la divergencia de resalte introducida por una edición propia — 2026-09-09

De los 17 resaltes de cuerpo que §F96 contó, uno lo había introducido yo: el reemplazo de texto de §3.3
escribió la cifra nueva **dentro** del run que ya estaba en negrita, con lo que la frase entera quedó
resaltada donde el Markdown resalta solo el porcentaje. Arreglarlo exigía partir el run, y ninguna
herramienta del proyecto lo hacía.

`tools/docx_partir_run.py` lo hace ahora: parte el `<w:r>` en hasta tres —lo de antes sin la propiedad de
resalte, el trozo con el `rPr` original intacto, y lo de después sin ella— y omite el `rPr` entero si al
quitar la propiedad se queda vacío, que es lo que produce texto de cuerpo normal. Exige que el texto del run
aparezca **una sola vez** en el documento, que el trozo a resaltar esté **una sola vez** dentro de él, y que
el run **lleve** la propiedad que se va a quitar; si no, reporta en lugar de fingir que hizo algo.

**Verificado en los tres documentos:** la frase sigue íntegra en el texto, `66,0 %` está en su propio run en
negrita, y el run que resaltaba la frase entera ya no existe. Los paquetes abren.

**Y la comprobación 34 se comportó como se diseñó**, que es la parte que interesa: al bajar el recuento a 16
no dio «ok» en silencio —lo que habría dejado el umbral holgado y ciego a un resalte nuevo— sino que pidió
**bajar el umbral a 16 para seguir vigilando desde el nuevo estado**. Bajado. Quedan **16**, todos
preexistentes al trabajo de hoy, y la propagación de la limpieza de sobriedad sigue siendo de la pasada de
maquetación.

## §F97 — Las figuras del informe son reproducibles byte a byte, y su tabla ya no está copiada a mano

**2026-09-09.** Ejecutadas las 17 herramientas del proyecto para ver cuáles corren, dos fallaban, y las dos
por lo mismo: una dependencia que solo está en `repos/ner-llm-entity-benchmark/venv`.

- `robustez_estadistica.py` falla por `scipy`, **con diagnóstico** desde hoy, que es la conducta correcta.
- `generar_figuras_informe.py` fallaba por `matplotlib` con un `ModuleNotFoundError` desnudo.

La segunda importaba más de lo que parecía, porque produce **las dos figuras del entregable**, y traía dos
defectos de fondo.

### La Tabla 7 estaba copiada a mano dentro de la herramienta

Su propio docstring lo admitía: «los valores se toman de la Tabla 7 … **si una tabla cambia, hay que cambiar
aquí también**». Comprobado hoy: coincidía en las **trece filas**, de modo que **no había defecto vivo** —
pero era una segunda fuente de verdad que habría dejado de coincidir sin avisar, que es §L63, y con la
particularidad de que el aviso estaba escrito en el propio fichero y aun así nadie iba a acordarse.

Ahora la **lee** del Markdown, y si la tabla no se puede interpretar **aborta** en lugar de dibujar una
figura con datos de otro momento.

### Y solo podía sobrescribir las figuras del entregable

No tenía forma de escribir en otro sitio, así que comprobar que las figuras son reproducibles exigía
arriesgarlas. Añadido `--out-dir`.

### El resultado, que es lo que un tribunal preguntaría

Regeneradas en un directorio aparte y comparadas con las comprometidas:

| Figura | Tamaño | Resultado |
|:---|---:|:---|
| `efecto-kb-rag.png` | 2297 × 1029 px | **idéntica byte a byte**, 0 píxeles distintos de 2 363 613 |
| `falsos-positivos.png` | 2110 × 436 px | **idéntica byte a byte**, 0 píxeles distintos de 919 960 |

Las figuras del informe son **reproducibles desde la fuente canónica**, y desde hoy sin ninguna cifra
intermedia mantenida a mano.

**Corolario del inventario:** de las 17 herramientas, 12 corren en el intérprete del sistema, 5 son editoras
de `.docx` que solo se invocan con reglas, y las 2 que necesitan el venv lo dicen. Ninguna falla en silencio.

### La puerta de commit detuvo la primera regresión, el día que se instaló

Al comprometer §F97 la puerta **cortó el commit**: la comprobación 12 leía el literal `TABLA7 = [...]` del
script de figuras para compararlo con la Tabla 7 del Markdown, y al hacer que el script **leyera** la tabla
en lugar de tenerla escrita, ese literal desapareció y la comprobación se quedó sin nada que leer.

No era un fallo del informe, era una regresión de la instrumentación causada por una mejora — y es
exactamente el caso para el que sirve una puerta: se vio en el acto, con el nombre de la comprobación, en
lugar de descubrirse semanas después con la comprobación pasando en verde sobre nada.

**No se borró la comprobación**, que habría dejado sin vigilar la coherencia entre figura y tabla. Se
sustituyó por algo **más fuerte**: ahora se **ejecuta el lector del propio script** —extrayendo su función y
su constante del árbol sintáctico y ejecutándolas aisladas, porque importar el módulo arrastraría matplotlib,
que solo está en el venv— y se contrasta con la lectura independiente que la comprobación ya hacía. Son dos
implementaciones distintas del mismo parseo, y que coincidan dice más que comparar una constante. Además se
exige que el literal **no vuelva**.

Probada por mutación en tres frentes, los tres detectados con su mensaje: reescribir la tabla a mano, alterar
lo que el lector devuelve, y renombrar la función lectora.

## §F98 — El PDF es hoy el entregable más desfasado, y arrastra todo lo corregido en los `.docx`

**2026-09-09.** Corregidos los tres `.docx`, quedaba un entregable que `CLAUDE.md` cuenta y que no había
mirado nadie: **el PDF**. Extraído su texto con `pypdf`, arrastra **todos** los defectos de hoy:

| | En el PDF | En los `.docx`, ya corregido |
|:---|---:|---:|
| Menciones de modelos excluidos | **11** | 0 |
| `76,85` · `90,91` · `81,45` | 6 · 2 · 2 | 0 · 0 · 0 |
| `76,55` · `90,16` · `80,42` | **0 · 0 · 0** | 6 · 2 · 2 |
| «65 %» de los falsos positivos | 2 | 0 |
| «66,0 %» | **0** | 3 |

Son 31 páginas y 129 387 caracteres extraídos, con las palabras de control presentes —`Kleptotrace` 11,
`Tabla` 25—, de modo que la extracción es buena y el diagnóstico no es un artefacto del lector.

### La distinción que hay que respetar antes de tocar nada

El PDF de la raíz y el de `doc/versions/enviados/` son **byte a byte el mismo fichero** —el mismo
SHA-256—, y ese segundo es el **entregado al profesor guía**, que `CLAUDE.md` declara verdad de referencia
sobre qué modelos forman el estudio. Ese **atestigua** y no se toca: reescribir un documento que ya se
entregó no es limpiar, es falsificar el registro de lo que se entregó. Que mencione los modelos excluidos es
**correcto** en él, porque su Anexo E los declaraba fuera.

Lo que hay que regenerar es la **copia de la raíz**, desde el `.docx` corregido y **con Word**. En este
entorno no hay conversor —solo `textutil`— y regenerarlo con otro motor perdería la maquetación, que es
justo lo que `CLAUDE.md` advierte sobre pandoc. Es de la pasada de maquetación.

### La comprobación, y por qué va en su propia casilla

Añadida como comprobación **35**, con 6 elementos. **No lee el PDF**: `pypdf` solo está en el venv del
proyecto y una comprobación que solo corre dentro de un entorno concreto no corre (§L62). Compara
**procedencias** —si el `.docx` tiene commits posteriores al del PDF, el PDF está obsoleto—, lo que se sabe
sin abrirlo, y comprueba además que el PDF entregado **sigue estando**.

Va **aparte** de la comprobación de modelos excluidos a propósito, y esto es §L64 aplicado por adelantado en
lugar de por escarmiento: si el PDF entrara en aquella, su fallo la pondría en rojo y **cegaría como
centinela** a los tres `.docx`, que acaban de quedar limpios. Comprobado tras declararlo: los centinelas de
los `.docx` siguen en verde y la autoprueba en 19 de 19. **Cada defecto abierto en su propia comprobación.**

### Y de paso: los metadatos de páginas de los `.docx` son falsos

`docProps/app.xml` declara **6 páginas y 1 646 palabras** en el `.docx` canónico, que tiene ~18 275, y
**1 página y 83 palabras** en los otros dos. Son restos de la herramienta que produjo los paquetes; Word los
recalcula al abrir, de modo que no engañan al lector, pero sí a quien inspeccione las propiedades del
fichero — y la restricción institucional se mide en páginas. Conviene saberlo antes de fiarse de ese dato:
**el recuento de páginas del `.docx` no se puede leer de sus metadatos**.

## §F99 — Un zip válido no acredita que Word pueda abrir el fichero

**2026-09-09.** Tras usar las **cinco** herramientas que editan `word/document.xml` sobre los tres
entregables —reemplazo de texto, borrado de filas, reescritura de celdas, reconstrucción de cuerpo y
partición de runs—, lo único que se había comprobado era `testzip()`, que solo verifica los CRC. Un
`document.xml` malformado, o una tabla cuyas filas no cuadran con su rejilla, produce un diálogo de error en
Word en lugar del documento, y el zip sigue siendo perfectamente válido.

Comprobado a fondo, y el resultado es bueno: la cirugía de hoy no rompió nada.

| Comprobación | Resultado |
|:---|:---|
| Partes XML bien formadas | **26, 15 y 15**, todas |
| Filas con celdas distintas de la rejilla | **0** en las 19 tablas de cada documento |
| Identificadores duplicados de marcador o de dibujo | **0** |
| Referencias `r:id` sin su relación | **0** |

Mecanizado como comprobación **36**, con **722 elementos examinados**, y probado por mutación en sus cuatro
frentes, los cuatro detectados con su mensaje:

- un `</w:body>` corrompido → «la parte `word/document.xml` no parsea», con línea y columna;
- una celda suprimida de una fila → «tabla 0 fila 0 tiene 3 celdas y la rejilla declara 4 columnas»;
- un marcador duplicado → lo señala por su `w:id` **y** por su nombre;
- un `r:id` inventado → «1 referencia sin su relación».

**Por qué importa que esté mecanizado y no solo comprobado.** Las cinco herramientas seguirán usándose en la
pasada de maquetación —quedan la inserción de párrafos, las dos figuras y la Tabla 20—, y cada una hace
cirugía sobre el mismo fichero. Comprobarlo una vez acredita el estado de hoy; la comprobación acredita el de
mañana. Y la de la rejilla es la que más falta hacía: **clonar y borrar filas es exactamente lo que la
descuadra**, y Word la dibuja torcida sin quejarse, de modo que un descuadre podría llegar a la defensa sin
que nada lo delatara.

## §F100 — La regla más costosa del proyecto vivía en una herramienta que nadie ejecuta

**2026-09-09.** `CLAUDE.md` añadió el 2026-09-08, tras el defecto más caro del estudio, esta obligación:

> «Toda categoría que se puntúe debe existir en la anotación de referencia. El indicador barato es **`tp + fn`
> agregado por categoría**: si esa suma vale cero mientras `fp` crece, la categoría no tiene ni una entidad
> de referencia en todo el corpus y está puntuando contra el vacío. **Comprobarlo antes de dar por buena
> cualquier métrica nueva.**»

Comprobado hoy dónde estaba mecanizada: **en ningún sitio que se ejecute**. El aviso existe dentro de
`tools/composicion_fp.py`, que nadie invoca automáticamente, y el verificador —36 comprobaciones— no la
tocaba. Una regla que solo vive en una herramienta que nadie llama no protege de nada, y ésta se escribió
precisamente porque el defecto **sobrevivió dos meses** con cifras internamente coherentes.

**La firma, calculada hoy sobre las 17 corridas con desglose por tipo:**

| Categoría | tp | fp | fn | tp + fn |
|:---|---:|---:|---:|---:|
| `Persons` | 22 078 | 2 988 | 17 463 | 39 541 |
| `Organizations` | 23 194 | 11 050 | 30 427 | 53 621 |
| `Locations` | **0** | **29 465** | **0** | **0** |

Hay que calcularla desde los `detailed_results.json` por corrida, porque el `merged_results.csv` del
consolidado **no trae la columna `metrics`** — es el pedido `§3.bis.16`, pendiente del equipo remoto.

### Cómo se mecanizó sin cegar la comprobación

`Locations` es la sabida: el informe la declara en §3.3 y publica en paralelo la métrica restringida a las
dos categorías anotadas. **No se declaró como fallo tolerado**, porque eso habría cegado la comprobación
entera (§L64). Se codificó como **esperada**, de modo que la comprobación queda en verde y **sigue siendo
sensible a que aparezca otra**, que es lo que hay que impedir.

Y lleva una segunda mitad que mira al futuro: **si `Locations` pasara a tener referencias, también falla.**
El corpus se corrigió el 2026-09-08 —545 localizaciones en 119 de los 120 registros— y la re-corrida
pendiente las traerá. Cuando eso ocurra, la comprobación dirá que **§3.3, la métrica restringida y el Anexo I
dejan de describir la medición**, que es exactamente lo que nadie debe descubrir después de publicar.

Probada por mutación en los dos frentes: una categoría `Fechas` inventada con `tp+fn=0` y `fp=98` se detecta
con su nombre y su recuento; y dar referencias a `Locations` dispara el aviso de que el informe deja de
describir lo que mide.

**El detalle que más importa del código:** los enteros se suman con `int(v.get(k) or 0)` y no con
`if v.get(k)`. Aquí más que en ningún sitio — un `tp` de 0 es *falsy*, y descartarlo haría invisible
justamente el caso que se busca.

## §F101 — Cerrada la última regla de integridad sin mecanizar: el idioma del corpus

**2026-09-09.** `CLAUDE.md` cierra su sección de integridad con «el idioma del corpus se comprueba, no se
supone», tras haber descubierto que los dos corpus del dominio estaban íntegramente en inglés mientras el
informe declaraba validación en español (§F54). Era la última de esa sección sin mecanizar.

**Contado sobre `data/benchmark_balanced_120.json`: 105 español, 15 inglés, 0 indeterminados.** Coincide con
lo que el informe declara. Y de paso queda comprobada la corrección del corpus del 2026-09-08: **545
localizaciones en 119 de los 120 registros**, exactamente lo que se declaró.

Esas dos cifras juntas dicen algo que conviene tener presente: **el corpus ya tiene las localizaciones y las
métricas publicadas son anteriores**. Es la contraparte de la segunda mitad de `c_firma_categorias`, y entre
las dos explican por qué la re-corrida sigue pendiente.

La declaración se **lee** del informe y **en sus dos idiomas** —el resumen dice «120 artículos, 105 en
español» y el abstract «120 articles, 105 in Spanish»—, de modo que la comprobación vigila también la
sincronía que `CLAUDE.md` exige entre ambos. El informe usa **cuatro redacciones** para la misma cifra en
cinco sitios, así que un patrón único no valía; se anclan las dos del encabezado, que son las que un tribunal
lee primero.

Probada por mutación en cuatro frentes, los cuatro detectados: alterar la cifra del resumen, desincronizar el
abstract, vaciar las localizaciones del corpus, y **romper el detector de idioma** —que emite la guarda de
§L66, «120 de 120 registros quedan sin clasificar», en lugar de un veredicto falso—.

**Y una pérdida de trabajo propia, con su lección.** La primera versión de esta comprobación se escribió y se
perdió: al probar la cuarta mutación restauré el fichero con `git checkout --`, que lo devolvió a `HEAD` y
borró las noventa líneas recién escritas y no comprometidas. Se rehízo desde la conversación. La lección está
en **§L67**, y su parte operativa es corta: **comprometer antes de mutar**, y no confundir `git checkout --`
con un «deshacer». La cuarta mutación, además, estaba mal hecha las dos primeras veces: cambiaba **la primera
palabra** de cada lista y dejaba las otras veintiséis, de modo que el detector seguía funcionando y la prueba
daba «ok» — §L59 otra vez, las mutaciones han de ser completas.

## §F102 — Revisión de fondo: los puntos débiles de la argumentación ya están cubiertos, salvo uno

**2026-09-09.** Cerrada la verificación de cifras, quedaba sin mirar lo único del informe que no había
revisado en toda la sesión: su **argumentación**. Leídos la hipótesis, los cinco objetivos y las
conclusiones, y contrastados con los resultados, los tres puntos más expuestos son estos —y **dos ya están
resueltos**, lo que en sí es el resultado de la revisión.

### 1. La hipótesis fija F1 ≥ 70 % y el F1 publicado es 59,25 % — cubierto

La hipótesis promete «desempeño competitivo en español (F1-Score ≥ 70 %)». El **76,55 %** que el informe
anuncia es la **métrica restringida**, a Personas y Organizaciones; la publicada para el mejor modelo local
sobre N=120 es **59,25 %** en macro. El informe **lo dice donde lo afirma**: el resumen escribe «restringida
la medición a las categorías que el corpus anota…» y el Anexo I declara «pasa de … a 76,55 % de F1 y supera
el umbral de 70 % que fija la hipótesis». Está cualificado, no escondido. Es, con todo, la pregunta más
probable de la defensa y conviene llegar con la distinción en la punta de la lengua.

### 2. El 60–80 % de reducción de costes — cubierto, y con la limitación declarada

El objetivo 5 dice «**Demostrar** una reducción de costos operativos del 60–80 %», y la conclusión 5 lo
restituye entre paréntesis tras el 99,4 % del coste unitario. `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` separa las
dos magnitudes —99,4 % es coste unitario directo, 60–80 % es coste operativo total— y dice lo que hay que
decir: que el ahorro total **depende de cuánto reduzca el sistema el volumen que llega a revisión humana**,
y que eso **este trabajo no lo midió**. La respuesta honesta está preparada.

Queda una aspereza de redacción, no de fondo: el verbo del objetivo es «**demostrar**», y lo que hay es una
estimación con sus parámetros a la vista. El propio documento de defensa admite que «presentarlas como
medición sería lo indefendible».

### 3. El umbral del 5 % de alucinación no recibe veredicto en el informe — el residuo real

El objetivo 5 exige además «mantener una tasa de alucinaciones inferior al 5 %». Buscado en todo el informe:
**esa cifra aparece una sola vez, en el propio objetivo, y no vuelve a aparecer**. El informe mide la
alucinación con detalle —§5.4 da el rango completo, de cero a 21,59 %, con 28 de 61 grupos por debajo del
1 %— pero **nunca dice si el objetivo se cumplió**.

`DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` lo anticipa y lo nombra con exactitud: «Parcialmente, y el informe da
los datos para verlo **aunque no lo formule como un sí o un no**». Y responde bien: el umbral se cumple en
las configuraciones que el capítulo 6 propone desplegar y se incumple en los dos modelos más pequeños, que
el trabajo ya descarta por su F1.

**El residuo es que eso vive en la preparación de la defensa y no en el informe.** Un lector del documento
solo no puede saber si el objetivo 5 se alcanzó. Es una decisión del autor y de extensión casi nula — queda
como **decisión 14**.

### De paso, una comprobación que salió bien

El documento de defensa cita el máximo de alucinación en **15,61 %** con «21 de 24 grupos por debajo del
5 %», mientras el informe dice **21,59 %** y «28 de 61 grupos». Parecía una contradicción y no lo es: el
documento etiqueta esas segundas cifras como **«de la re-corrida sobre el corpus corregido, con doce de los
trece modelos y por tanto provisionales»**. Las dos poblaciones están declaradas, que es exactamente lo que
la regla de `CLAUDE.md` sobre corridas múltiples exige.

## §F103 — Seis de los siete capítulos abren sin una línea de texto

**2026-09-09.** Segunda parte de la revisión de fondo, esta vez sobre el desarrollo. El profesor guía
objetó, entre otras cosas, «poco desarrollo, con secciones que son un título y un párrafo» y «demasiados
bloques en blanco y saltos de página entre capítulos». Medidas las **38 secciones del cuerpo**, palabra por
palabra, los dos reparos se tocan en un punto concreto:

**Los capítulos 1, 3, 4, 5, 6 y 7 tienen cero palabras entre su título y la primera subsección.** No es un
párrafo corto: es un encabezado seguido de una línea en blanco y otro encabezado. Verificado leyendo el
texto directamente en cuatro de ellos. Solo el capítulo 2 abre, con 82 palabras.

Eso explica de paso la impresión de «bloques en blanco entre capítulos» que el profesor describió: cuando un
título de capítulo no tiene texto debajo, la maquetación deja el hueco a la vista.

### El resto del desarrollo está sano

Salvo las aperturas, ninguna sección es «un título y un párrafo». Las más breves tienen motivo:

| Sección | Palabras | Por qué es breve |
|:---|---:|:---|
| 1.3 Hipótesis de Trabajo | 98 | una hipótesis se enuncia, no se desarrolla |
| 4.1 Corpus de Evaluación | 129 | es la entradilla de 4.1.1 y 4.1.2 |
| 4.2 Modelos evaluados | 136 | la única sin tabla ni subsecciones: candidata a ampliar |
| 5.2 Análisis de Variantes | 145 | lleva su tabla |
| 2.5 Estado del arte | 210 | lleva su tabla |

Y las de más peso están bien servidas: 4.4 Métricas con 1 032 palabras, 7.1 Conclusiones con 1 131, 3.3
Módulo de evaluación con 954, 5.3.1 con 991.

### El coste de corregirlo, que es lo que hace la decisión tomable

El cuerpo son **16 926 palabras**, unas **23,0 páginas de las 25**, con **1 335 palabras de margen**. Abrir
los seis capítulos con dos o tres frases cuesta unas **270 palabras** y deja el margen en **1 065**. Es
decir: **cabe de sobra**, y es la clase de corrección que responde a un reparo explícito del profesor guía
con coste casi nulo.

Queda como **decisión 15**. No lo redacto por iniciativa propia: una entradilla de capítulo fija el tono de
lo que sigue y es del autor.

## §F104 — Barrido de la prosa que dependía de las cifras propagadas: un solo defecto, ya corregido

**2026-09-09.** Encontrado por lectura el defecto de §L69 —una cifra propagada y su numeral en palabras sin
propagar—, la pregunta obligada era si había más. Barrido sistemático de la prosa que rodea **las diez
cifras que cambié hoy** en los tres `.docx`, buscando numerales en palabras, comparativos y aproximadores
(«doble», «casi», «del orden de», «unos», «más de»).

**Resultado: ninguno más.** Los siete casos que el barrido levantó son inocuos, y conviene decir por qué,
porque cada uno pudo parecer un defecto:

| Coincidencia | Por qué no lo es |
|:---|:---|
| «76,55 … ciento **veinte** artículos» | el numeral es el tamaño del corpus, no la magnitud de la cifra |
| «90,16 … **treinta** artículos» | ídem |
| «80,42 … ciento **veinte**» | ídem |
| «66,0 % … las **tres** categorías» | el numeral cuenta categorías de entidad |
| «66,0 % … en **un** falso positivo» | artículo indeterminado, no numeral |
| «66,0 % … cuarenta y **dos** configuraciones» | **cuadra hoy** precisamente porque esta mañana retiré las 7 filas de modelos excluidos: la Tabla 19 tiene 42 |
| «del orden de» junto a 76,55 | es el que corregí, ya arreglado |

El único defecto de esta clase era el de §L69, y quedó corregido en la misma pasada en que se encontró.

### Y de paso quedaron verificadas dos afirmaciones de prosa que nadie había comprobado

**Las particiones del *mojibake*.** El texto anterior a la Tabla 18 dice «por entidad de referencia corrupta:
**89** artículos afectados y **31** no; por texto de entrada corrupto: **104** y **16**». Suman 120 en los
dos casos, y los cuatro valores están en `efecto_mojibake.json` con esos mismos nombres. La comprobación 22
ya los cubría.

**La exhaustividad idéntica del Anexo I.** La prosa que introduce la Tabla 19 afirma que «la exhaustividad es
**idéntica en ambas columnas** porque el corpus no anota localizaciones y, por tanto, tampoco puede
omitirlas: la corrección afecta solo a la precisión». Es una afirmación fuerte, y **justifica que la tabla no
traiga columna de exhaustividad restringida**. Comprobada sobre cinco grupos, recalculando la exhaustividad
sobre tres categorías y sobre dos: **idéntica al cuarto decimal en los cinco**.

Y tiene una consecuencia que merece anotarse: **la comprobación 38 protege esa afirmación**. Su premisa es
que `Locations` no tiene ni una entidad de referencia, y la 38 vigila exactamente eso — si el corpus
corregido llega y `Locations` gana referencias, la 38 falla y con ella cae la justificación de la estructura
del Anexo I. La comprobación no se escribió para eso, pero lo cubre.

## §F105 — Pasada de corrección lingüística: el texto está limpio, con dos excepciones menores

**2026-09-09.** Revisión del lenguaje del informe, que era el último frente de lectura sin tocar. Los repasos
mecánicos salen **limpios**: cero palabras repetidas consecutivas, cero espacios dobles en prosa, cero
espacios antes de puntuación, y paréntesis, comillas latinas y corchetes **equilibrados** en todo el
documento —362/362, 23/23 y 152/152—.

Los cuatro «paréntesis sin cerrar» que el primer barrido levantó eran **falsos positivos**: paréntesis que
abren en una línea y cierran en la siguiente, invisibles a una comprobación por líneas. §L66 otra vez, y esta
vez detectado en el acto.

### Lo único que apareció

**Corregido, porque no era criterio sino inconsistencia interna:** el Hallazgo 3 de §5.1 escribía «Recall de
**sólo** 25.77 %», con tilde, frente a **31 «solo»** sin tilde en el resto del documento. Uno contra
treinta y uno no es una decisión de estilo; es un descuido respecto de la propia convención del texto, y la
RAE recomienda «solo» sin tilde desde 2010. Corregido en el Markdown y en los tres `.docx`.

**Dejado al autor, porque sí es criterio:** «Recall» aparece **5 veces en prosa, en mayúscula y sin
cursiva**, conviviendo con «exhaustividad» (15 veces, el término que §4.4 declara) y con «*recall*» en
cursiva (3 veces, el uso correcto del extranjerismo, y el que §4.4 emplea al presentarlo: «la
**exhaustividad** o *recall*»). En las tablas «Recall» es una cabecera y ahí no hay nada que discutir. Queda
como **decisión 16**, con recomendación de reservar «Recall» a las cabeceras.

### Lo que esta pasada no puede acreditar

Un barrido mecánico no lee. No detecta una concordancia rota que resulte gramatical, una frase sin verbo
principal, ni un párrafo que dice lo contrario de lo que pretende. De esto último ya se encargó la revisión
de fondo de §F102 y §F103; de lo primero, nada de lo que hay aquí da garantías, y conviene decirlo en lugar
de dejar que «pasada de corrección: limpio» suene a más de lo que es.

## §F106 — ~~El 50 % que la Tabla 1 atribuye a FinanceBench no existe en FinanceBench~~ — RECTIFICADO: sí existe

> ## ⚠ RECTIFICACIÓN DEL 2026-09-09 — ESTE HALLAZGO ERA FALSO
>
> **El 50 % sí aparece en FinanceBench, dos veces.** Verificado contra el artículo por un workflow de
> revisión de fuentes y **recomprobado por mí** en la fuente primaria
> (`ar5iv.labs.arxiv.org/html/2311.11944`):
>
> - Tabla 2 del artículo, fila literal: «**GPT-4-Turbo Single Vector Store 75 (50%)** 17 (11%) 58 (39%) 150»
> - Prosa de §5, literal: «…had a higher success rate than the configuration with a single vector
>   store for all documents **(50% vs 19%)**»
>
> **El error de este hallazgo fue leer la tabla desplazada una fila.** El 41 % que atribuye abajo a
> «GPT-4-Turbo con almacén único» es en realidad la fila de **`Llama2 Single Vector Store 62 (41%)`**.
>
> **Consecuencia: la Tabla 1 del informe está bien y no hay que tocarla.** Y la **decisión 17**, que
> se derivaba de aquí, se cierra sin cambio: sus cuatro opciones habrían introducido un error donde
> no lo había, y la recomendada —bajar la celda a 19 %— habría sustituido un dato correcto por uno
> que **subestima el estado del arte** y, con ello, habría hecho parecer mejor al trabajo de lo que
> le corresponde.
>
> **Rectificación de la afirmación de cierre de este hallazgo:** decía «de las cinco cifras que el
> informe atribuye a una fuente, cuatro están verificadas y solo ésta es falsa». **Las cinco están
> verificadas.** Ver `§F144`.
>
> El texto original se conserva íntegro debajo, tachado en el título, porque la política es aditiva y
> porque el registro de un error mal diagnosticado vale más que su borrado.



**2026-09-09.** El verificador comprueba que las URL de la bibliografía respondan y que cada cita tenga
entrada y cada entrada esté citada, pero **no** que la fuente sostenga lo que el texto le atribuye. Acotado
el subconjunto de riesgo —cifras atribuidas a una cita—, salen cinco, dos ya verificadas el 2026-09-09
(el 88,43 % de [7] y el 82,1 % de [15]) y tres sin verificar.

**Una se verifica sola.** El [21] es un comunicado cuyo **título** dice «RegTech Market Size Worth $87.17
Billion, Globally, by 2028 at 23.92% CAGR», que es exactamente lo que el informe le atribuye.

**Y una es falsa.** La Tabla 1 dice:

> «FinanceBench [9] | 361 informes SEC | GPT-4-Turbo + RAG | **50 % exactitud** | Cloud | Inglés»

Leído el artículo, el «361 informes SEC» **es correcto** —dice «361 public filings»—, pero **el 50 % no
aparece en ninguna configuración**:

| Configuración de GPT-4-Turbo | Aciertos |
|:---|---:|
| Closed Book | **9 %** (14 de 150) |
| Shared Vector Store, que es RAG | **19 %** |
| Single Store, también RAG | **41 %** |
| Long Context, que **no** es RAG | 79 % |

El titular del propio resumen del artículo es que «GPT-4-Turbo usado con un sistema de recuperación
**respondió incorrectamente o rehusó responder al 81 %** de las preguntas» — es decir, el 19 %. La etiqueta
del informe, «GPT-4-Turbo + RAG», corresponde a las de almacén vectorial: **19 % o 41 %**, no 50 %.

### Dos cosas que conviene decir a la vez

**El error va contra el interés del autor.** Con una referencia correcta de 19 a 41 % en lugar de 50 %, el
resultado del trabajo —76,55 % restringido— queda **mejor** situado, no peor. Eso descarta cualquier lectura
malintencionada y hace que corregirlo fortalezca el informe en lugar de debilitarlo.

**Y la fila lleva su propia advertencia.** La glosa bajo la Tabla 1 ya dice que «las cifras de la última
columna **no son directamente comparables entre sí**, porque cada trabajo mide otra cosa». Eso protege la
interpretación pero no la exactitud: una cifra que la fuente no contiene sigue siendo falsa aunque se
declare incomparable.

**No elijo el reemplazo.** Sustituir 50 % por 19 %, por 41 % o por «19–41 % según el almacén» cambia lo que
la tabla afirma sobre el estado del arte, y eso es del autor. Queda como **decisión 17**, con la recomendación
de «19 %» por ser la cifra que el propio resumen del artículo destaca.

### El «53,6–75,5 %» de BloombergGPT — verificado el mismo día

Quedaba una cifra sin comprobar. El resumen del artículo no publica métricas por tarea, así que hubo que
leer las tablas del cuerpo del PDF. La de NER da, para BloombergGPT:

| Conjunto | F1 |
|:---|---:|
| BFW | 72,04 |
| BN | 57,31 |
| Filings | 58,84 |
| **Headlines** | **53,61** |
| Premium | 60,49 |
| **Transcripts** | **75,50** |
| Social Media | 60,60 |
| Media de todas | 62,63 |

El mínimo y el máximo son **53,61 y 75,50**, que es exactamente el «53,6–75,5 %» que la Tabla 1 le
atribuye. **Correcto.**

Un matiz que no afecta a la exactitud pero conviene tener a mano en la defensa: en ese mismo cuadro
**BLOOM176B supera a BloombergGPT** en cinco de los siete conjuntos y en la media (64,83 frente a 62,63).
La columna del informe se titula «desempeño publicado» y cita el rango del modelo que nombra, que es lo
correcto; pero si alguien pregunta «¿y no había algo mejor en ese mismo artículo?», la respuesta es que sí.

**Balance del frente de citas:** de las cinco cifras que el informe atribuye a una fuente, **cuatro están
verificadas** —88,43 % de [7], 82,1 % de [15], las dos del [21] por su propio título, y este rango de [3]—
y **una es falsa**, el 50 % de [9], que queda como decisión 17. Ninguna queda sin comprobar.

## §F107 — El ejemplo del emparejamiento duplicado no resistía que alguien lo ejecutara

**2026-09-10.** Verificadas las cifras de las citas, quedaban las **afirmaciones técnicas** atribuidas a
fuentes, que son igual de falsables y nadie había mirado. La más consecuente es la de §3.3, porque define la
función de emparejamiento de la que dependen todas las métricas del trabajo:

> «…implementado con la función `ratio` de la biblioteca *rapidfuzz* [33], que normaliza la **distancia de
> Indel** —el número mínimo de inserciones y supresiones necesarias…, variante de la distancia de Levenshtein
> que excluye las sustituciones— a una escala de 0 a 100 mediante la expresión `100 × (1 − d / (|a| + |b|))`.»

**Verificada ejecutando la biblioteca, no leyendo su documentación.** La fórmula se cumple **en 7 de 7 pares**
a precisión de máquina, y el ejemplo que el propio informe da también: dice que `EFE` y `EFECOM` «designan la
misma agencia con **66,7** de similitud», y `fuzz.ratio` da 66,6667. Correcto.

### Pero de paso cayó otro ejemplo

`DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` explica el emparejamiento duplicado —el defecto que produce exhaustividad
mayor que 1 en 197 registros— así:

> «Cuando dos extracciones casan con la misma referencia —«John Smith» y «Smith, John», **iguales para el
> emparejamiento difuso al 85 %**— el acierto se cuenta dos veces.»

**`fuzz.ratio('John Smith', 'Smith, John')` da 47,62**, muy por debajo del umbral de 85. Con ese par la
segunda extracción **no habría casado** y el duplicado no se produciría. El ejemplo elegido para ilustrar el
defecto es justamente uno en el que el defecto no ocurre.

**Lo que importa: el mecanismo es correcto y está cuantificado** —197 registros, máximo 2,444, inflación de
+0,160 pp de media y +1,287 pp como máximo, ninguna mejora cambia de signo—. Lo que fallaba era la
ilustración. Pero es una ilustración destinada a decirse **en voz alta ante un tribunal**, donde cualquiera
con un intérprete a mano la desmiente en diez segundos, y entonces lo que parece falso no es el ejemplo sino
el hallazgo.

**Sustituido por un par verificado:** sobre la referencia «José Bono», tanto «José Bono» como «Jose Bono»
superan el umbral —100 y **88,89**—, de modo que el duplicado sí se produce. Comprobados también «Banco
Santander» / «Banco Santander S.A.» (85,71), «Partido Popular» / «Partido Popular.» (96,77) y «José María
Aznar» / «Jose Maria Aznar» (87,50); y descartado «Mariano Rajoy» / «Rajoy», que da 55,56.

**El informe no está afectado:** «John Smith» aparece **cero veces** en él. El defecto estaba solo en la
preparación de la defensa.

### La regla que deja

Un ejemplo ilustrativo es una **afirmación verificable**, no un adorno. Si ilustra un mecanismo con un
umbral, hay que ejecutarlo con ese umbral. Y cuando el ejemplo vive en un documento pensado para decirse
delante de alguien que puede comprobarlo, el coste de no haberlo ejecutado no lo paga el ejemplo: lo paga la
credibilidad del hallazgo que pretendía apoyar.

## §F108 — `failed = 0` no acredita una corrida limpia, y se demuestra en la corrida que el estudio publica

**2026-09-10.** Aplicadas las cinco verificaciones del protocolo de monitorización a **las 17 corridas con
datos**, y no solo a los tres puntos de atención habituales. Resultado global: **cero violaciones aritméticas**
en todas —ninguna fila con F1 > (P+R)/2, en ninguna corrida—, y diez grupos con alguna señal que merecía el
cruce completo.

### La demostración

`nemotron_rerun_n120_REMOTO`, que es **la corrida que el consolidado usa** para
`nemotron-mini:4b_baseline`, declara:

| Señal | Valor |
|:---|---:|
| `parse_method = 'failed'` | **0** |
| Registros con latencia 0 **y** 0 tokens/s | **7** |
| Esos mismos, en `fallback` | 7 |
| De ellos, con `recall > 0` | 4 |
| De ellos, con `recall = 0` | 3 |

**Una comprobación que solo mirara el criterio 1 daría esta corrida por limpia.** Y no lo está: tiene siete
rechazos de infraestructura, tres de ellos con pérdida total de contenido. La firma del fallo cambió entre
corridas —`benchmark_n120_REMOTO` los marcaba como `failed=8`, `benchmark_balanced_…_173036` como `failed=7`,
y la re-corrida ya no los marca— de modo que **el mismo defecto se volvió invisible al indicador barato**.

Es exactamente para esto que el protocolo tiene cinco criterios y no uno, y conviene tenerlo escrito con el
caso a la vista: **`failed = 0` es la ausencia de una etiqueta, no la ausencia de un fallo.**

### Y la comprobación de que el consolidado no bebe de las corridas malas

El barrido encontró dos corridas con patrones graves:

- `benchmark_balanced_120_20260824_173036`: `gemma4:31b-cloud_baseline` con **99 de 120 fallidos** y 97 con
  `recall = 0`; su `_rag_enhanced`, 91 de 120. Un 82 % de rechazo.
- `excluidos_n120_REMOTO`: `gpt-oss:20b_kb_rag` con 49 en `fallback` de los que **solo 4 rescatan** contenido.

**Ninguna de las dos alimenta las cifras publicadas**, y no se ha dado por supuesto: tres grupos aparecen en
**dos fuentes** cada uno, y se ha verificado cuál gana comparando la media del consolidado contra la de cada
fuente, no leyendo etiquetas —que es la lección de §F81, donde ocho de veintiséis grupos se habían leído de
corridas superadas—:

| Grupo | Gana | F1 | La otra fuente daba |
|:---|:---|---:|---:|
| `nemotron-mini:4b_baseline` | `03_nemotron_rerun` | 22,5921 | 21,3025 |
| `gpt-oss:20b_kb_rag` | `00_gptoss_rerun` | 55,6716 | 34,1874 |
| `gemma4:12b-mlx_baseline` | `02_gemma4_12b_mlx` | 56,1825 | 27,3102 |

En los tres gana la corrida buena, conforme al orden del manifiesto y a `--on-duplicate=first`. **El
consolidado es sólido**, y ahora está comprobado por comparación de medias y no por inferencia.

## §F108.bis — Corrección: no eran rechazos de infraestructura, y el informe ya lo explicaba

**2026-09-10.** El hallazgo §F108 diagnosticó las siete filas de `nemotron-mini:4b_baseline` con latencia 0
como **«rechazo de infraestructura»**, aplicando la regla del criterio 5 del protocolo. **Era falso**, y hay
que decir cómo se llegó a ello porque el mecanismo del error es más instructivo que el error.

**Lo que los datos dicen.** Las siete filas tienen `parse_method = direct_json` y **seis de las siete traen
`recall > 0`**. Hay contenido: la ejecución no se rechazó. Lo que falta es la telemetría.

**Y el informe ya lo explicaba**, en la salvedad de procedencia de §5.3.1, que no leí antes de diagnosticar:

> «(ii) Siete filas de `nemotron-mini:4b` tienen `latencia = 0` y `0 tokens/s` porque **se re-extrajeron
> fuera del arnés de lotes** tras un fallo de contexto; sus valores de precisión, *recall* y F1 son reales,
> pero su telemetría no existe.»

**Dos errores más, del mismo diagnóstico.** Escribí que las siete filas con latencia 0 «son las mismas 7» que
las de `fallback`. **Son conjuntos disjuntos**: 7 + 7 = **14 registros distintos**. Y atribuí «3 de pérdida
total» al grupo de latencia 0, cuando esas tres son del grupo de `fallback`; en el de latencia 0 hay **una**.

| Grupo | Cuántas | `parse_method` | Con `recall > 0` | Qué es |
|:---|---:|:---|---:|:---|
| Latencia 0 y 0 tokens | 7 | `direct_json` | **6 de 7** | telemetría ausente, declarada en §5.3.1 |
| `parse_method = fallback` | 7 | `fallback` | 4 de 7 | el arnés usó la vía alterna |

**Lo escribí en cuatro sitios** —la comprobación, §F108, la alerta al equipo remoto y el informe de avance— y
los cuatro quedan corregidos.

### Lo que sí queda, y es del autor

De las siete con telemetría ausente, **una** —`real_mixed_70`— tiene `recall` **y** `precision` a cero. Para
esa fila la salvedad del informe es imprecisa: sus valores no «son reales» en el sentido de traer contenido;
son cero, y no consta si son cero legítimos o cero por pérdida. Declarado con su dueño.

### La lección, que es la más incómoda de la sesión

**Apliqué una regla del protocolo sin comprobar su premisa, y sobre un documento que traía la explicación
correcta.** El criterio 5 dice «latencia 0 y 0 tokens = rechazo de infraestructura», y eso presupone que no
hay contenido. Aquí lo había en seis de siete casos, y bastaba mirar la columna `recall` —que estaba en la
misma fila— o leer §5.3.1 —que estaba en el documento que audito— para no equivocarse.

Una regla heredada es una hipótesis con buena reputación. Sigue necesitando que se compruebe su premisa en el
caso concreto, y **el sitio donde comprobarla suele ser el propio documento que se está auditando**.

## §F109 — El informe no describe la vía de parseo alterna, y una conclusión cambia de signo al aislarla

**2026-09-10.** Buscando si había cometido en otro sitio el error de §F108.bis —aplicar una regla sin
comprobar su premisa— apareció algo distinto: **el informe no menciona en ninguna parte el
`parse_method = 'fallback'`**. Cero apariciones de «fallback», «parse_method», «vía alterna», «reintento del
parseo» o equivalentes. Su único rastro es una fila de tabla que dice que `llm_runner.py` tiene «parseo en
cascada», sin describirlo ni decir cuántas veces se usa.

**Y se usa.** En el consolidado publicado, **112 de 3 120 registros (3,6 %)** se parsearon por esa vía, con
una distribución muy desigual:

| Grupo | Vía alterna | % del grupo | Rescatan contenido | F1 de esas filas |
|:---|---:|---:|---:|---:|
| `mistral-nemo:latest_kb_rag` | 69 | **57,5 %** | 68 de 69 | 44,60 |
| `mistral-nemo:latest_baseline` | 9 | 7,5 % | 9 de 9 | 43,91 |
| `deepseek-r1:1.5b_kb_rag` | 8 | 6,7 % | **0 de 8** | **0,00** |
| `nemotron-mini:4b_baseline` | 7 | 5,8 % | 4 de 7 | 12,02 |
| `gemma4:31b-mlx_kb_rag` | 5 | 4,2 % | 1 de 5 | 11,16 |
| `deepseek-r1:1.5b_baseline` | 4 | 3,3 % | **0 de 4** | **0,00** |
| `llama3.2:latest_baseline` | 2 | 1,7 % | 2 de 2 | **86,58** |

**«El fallback rescata» no es una regla, es un caso.** Rescata 68 de 69 en `mistral-nemo` y **0 de 8** en
`deepseek`. En `llama3.2` las dos filas rescatadas puntúan **86,58**, muy por encima del 35,26 de su grupo.
Es exactamente la distinción que el criterio 5 pide, y hay que hacerla **por grupo**, no en general — cosa
que yo mismo no hice al reportar `mistral-nemo` como «benigno» sin mirar los demás.

### La consecuencia que importa

El informe concluye que **el modelo grande no se beneficia de la recuperación**, con un delta de
**−0,18 pp** para `gemma4:31b-mlx`. Aislando las filas que no se parsearon por la vía directa:

| | F1 publicado | F1 solo con parseo directo |
|:---|---:|---:|
| `gemma4:31b-mlx_baseline` | 59,2550 | 59,7529 |
| `gemma4:31b-mlx_kb_rag` | 59,0749 | **61,1580** |
| **Delta** | **−0,1801 pp** | **+1,4051 pp** |

**El signo se invierte.** Y lo hacen **seis registros**: uno en la línea base, con F1 cero, y cinco en la
mitad con recuperación, cuatro de ellos cerca de cero.

**Tres cautelas, para no sobreinterpretarlo:**

1. **La significación no cambia.** Ninguno de los dos deltas alcanza el umbral de Tukey; el modelo grande
   sigue sin mostrar un efecto significativo. Lo que cambia es el **signo de la estimación puntual**, no el
   veredicto estadístico.
2. **Excluir esas filas no es evidentemente el análisis correcto.** Son mediciones reales del comportamiento
   de la tubería, y el estudio mide la tubería, no solo el modelo. Un análisis que las descarte está
   respondiendo a otra pregunta.
3. **No es solo ese grupo.** El mismo efecto deprime la cifra publicada en `deepseek-r1:1.5b_kb_rag`
   (+1,71 pp al aislar) y en `mistral-nemo:latest_kb_rag` (+1,57 pp).

**Por eso esto es una prueba de sensibilidad y no una corrección**, y por eso va a decisión del autor: lo que
está en juego es si el informe declara que su conclusión sobre los modelos de 31B depende de seis registros
que no se parsearon. Queda como **decisión 18**.

### El barrido de los trece, que acota el hallazgo

Encontrado el caso por casualidad, la pregunta obligada era cuántos más hay. Calculado el delta de los trece
modelos con y sin las filas de parseo alterno:

| Modelo | Δ publicado | Δ solo directo | Cambio | Vía alterna base/kb |
|:---|---:|---:|---:|:---|
| `mistral-nemo:latest` | +2,3717 | +3,9830 | +1,6114 | 9 / 69 |
| `gemma4:31b-mlx` | **−0,1801** | **+1,4051** | +1,5852 | 1 / 5 |
| `gemma4:latest` | −1,1698 | −0,2963 | +0,8735 | 2 / 1 |
| `llama3.2:latest` | +10,8229 | +11,6782 | +0,8554 | 2 / 0 |
| `deepseek-r1:1.5b` | −0,8966 | −0,0431 | +0,8535 | 4 / 8 |
| `nemotron-mini:4b` | +14,5249 | +14,0491 | **−0,4758** | 7 / 1 |
| `qwen3:8b` | +3,2491 | +3,4904 | +0,2413 | 1 / 0 |
| `gpt-oss:20b` | +3,2803 | +3,3079 | +0,0276 | 1 / 1 |
| Los otros **cinco** | — | — | **0,0000** | 0 / 0 |

**Tres conclusiones, y las tres tranquilizan:**

1. **Solo uno cambia de signo:** `gemma4:31b-mlx`. Ningún otro delta cruza el cero, de modo que la
   sensibilidad afecta a **una** afirmación del informe y no a su estructura.
2. **Los dos resultados significativos sobreviven holgados:** `nemotron-mini:4b` pasa de +14,52 a **+14,05**
   y `llama3.2:latest` de +10,82 a **+11,68**. La conclusión sobre para qué modelos sirve el RAG no se toca.
3. **Cinco modelos son inmunes** porque no tienen ni una fila de parseo alterno: `gemma4:12b-mlx`,
   `gemma4:31b-cloud`, `gemma:latest`, `llama3.1:8b` y `qwen2.5:14b`.

**Y un dato para el encargo `§3.bis.15`:** `nemotron-mini:4b` es el **único** cuyo delta **baja** al aislar,
de +14,52 a +14,05, porque sus siete filas de parseo alterno están en la **línea base** y la deprimen. La
re-corrida, al arreglarlas, previsiblemente **reducirá** el +14,52 que el informe publica. Conviene esperarlo
en lugar de descubrirlo.

## §F110 — El bloque `overall` de `detailed_results.json` es inservible, y en un grupo el `per_type` tampoco cuadra

**2026-09-10.** Intentando combinar las dos sensibilidades del estudio —el parseo alterno de §F109 y el
emparejamiento duplicado— la tabla salió con cifras que **no reproducían el CSV consolidado**:
`nemotron-mini:4b` daba un delta de +6,19 donde el CSV da +14,52. Perseguido el origen, aparecen dos defectos
distintos en `detailed_results.json`, y conviene separarlos porque su gravedad no es la misma.

### 1. El bloque `overall` contiene valores imposibles

Para `nemotron-mini:4b_baseline`, **77 de 120 registros** discrepan entre el CSV y el `overall.f1` del
`detailed`. El patrón es siempre el mismo: el CSV dice **0** y el `detailed` dice **100**. Un ejemplo íntegro:

```json
"overall": {"precision": 0.0, "recall": 0.0, "f1": 1.0, "tp": 0, "fp": 2, "fn": 6}
```

**F1 de 1,0 con precisión 0 y exhaustividad 0 es imposible.** Es la vieja convención de extracción vacía —que
§3.3 declara corregida— sobreviviendo en el bloque `overall`, y aplicada además a un registro que **no está
vacío**: extrajo dos falsos positivos.

**Nada publicado lo lee** —las tablas salen del CSV—, de modo que ninguna cifra del informe está afectada.
Pero es una trampa para quien calcule desde ahí, y me atrapó a mí durante veinte minutos.

### 2. En un grupo, el `per_type` tampoco reproduce el CSV

Esto es más relevante, porque **el Anexo I sí se calcula desde `per_type`**. Comprobados los 26 grupos:

| | |
|:---|---:|
| Grupos donde `per_type` reproduce el CSV a precisión de máquina | **25 de 26** |
| Grupos donde no | **1**: `nemotron-mini:4b_baseline`, −1,0936 pp |

La causa son **seis registros** —`real_mixed_101`, `106`, `30`, `32`, `50` y `53`—, que son exactamente seis
de las siete filas re-extraídas fuera del arnés de lotes que §5.3.1 declara. Su `per_type` quedó **a cero** en
el `detailed` mientras el CSV recibió sus métricas reales: se actualizó un artefacto y no el otro.

**La consecuencia en el Anexo I**, y es acotada: la fila de ese grupo publica F1 **22,59** —del CSV— y F1
restringido **25,28** —de `per_type`, y reproduce exacto—, de modo que su **Δ de +2,68 compara dos estados
distintos del dato**. Calculado como comparación homogénea desde `per_type`, el Δ sería 21,50 → 25,28 =
**+3,78**. Un punto y once centésimas de diferencia, en una fila de veintiséis.

### Lo que esto no es

**No es un defecto de las cifras publicadas.** Las 25 filas restantes del Anexo I comparan estados
homogéneos, la Tabla 7 sale del CSV, y §5.3.1 ya declara que esas siete filas se re-extrajeron. Lo que no
declara —porque nadie lo había mirado— es que su `per_type` no se actualizó con ellas.

**Y lo arregla la re-corrida pendiente.** `§3.bis.15` regenerará los dos artefactos del grupo, de modo que
esto no necesita trabajo aparte: necesita **no olvidarse de comprobarlo después**, cosa que la comparación de
26 grupos de este hallazgo permite repetir en un minuto.

### Y una advertencia sobre mi propio análisis

La sensibilidad de §F109 se calculó desde el **CSV consolidado** y por tanto **sigue siendo válida**. La que
intenté aquí —combinar las dos sensibilidades— usaba `overall.f1` y **queda descartada**; para hacerla bien
hay que partir de `per_type`, y solo es homogénea en 25 de los 26 grupos. No la publico a medias.

## §F111 — Un delta cambia de signo solo cuando las dos sensibilidades se aplican juntas

**2026-09-10.** Rehecha desde `per_type` la combinación de sensibilidades que §F110 obligó a descartar. La
columna base reproduce ahora los deltas publicados —`gemma4:31b-mlx` −0,1801, `llama3.2:latest` +10,8229,
`deepseek-r1:1.5b` −0,8966—, de modo que el dato es homogéneo con lo que el informe dice.

`nemotron-mini:4b_baseline` **queda excluido**, porque su `per_type` no reproduce su CSV (§F110) y meterlo
compararía estados distintos del dato.

| Modelo | Publicado | Sin parseo alterno | Sin duplicados | Las dos |
|:---|---:|---:|---:|---:|
| `deepseek-r1:1.5b` | −0,8966 | −0,0431 | −0,9806 | −0,1420 |
| `gemma4:12b-mlx` | +2,2770 | +2,2770 | +2,1742 | +2,1742 |
| `gemma4:31b-cloud` | −0,5371 | −0,5371 | −0,5552 | −0,5552 |
| **`gemma4:31b-mlx`** | **−0,1801** | **+1,4051** | −0,2844 | **+1,4073** |
| **`gemma4:latest`** | **−1,1698** | −0,2963 | −0,2545 | **+0,4739** |
| `gemma:latest` | +7,3609 | +7,3609 | +7,2929 | +7,2929 |
| `gpt-oss:20b` | +3,2803 | +3,3079 | +3,2806 | +3,3082 |
| `llama3.1:8b` | +1,9880 | +1,9880 | +2,4104 | +2,4104 |
| `llama3.2:latest` | +10,8229 | +11,6782 | +10,9060 | +11,6741 |
| `mistral-nemo:latest` | +2,3717 | +3,9830 | +2,3854 | +3,9961 |
| `qwen2.5:14b` | +4,6213 | +4,6213 | +4,6047 | +4,6047 |
| `qwen3:8b` | +3,2491 | +3,4904 | +3,2551 | +3,4729 |

### El hallazgo: `gemma4:latest` solo cambia de signo con las dos

`gemma4:31b-mlx` ya se sabía (§F109). Lo nuevo es **`gemma4:latest`**, que el informe publica **empeorando
1,17 puntos** con recuperación:

| Escenario | Δ |
|:---|---:|
| Publicado | **−1,1698** |
| Aislando el parseo alterno | −0,2963 |
| Corrigiendo el emparejamiento duplicado | −0,2545 |
| **Las dos a la vez** | **+0,4739** |

**Ninguna de las dos por separado le da la vuelta.** Juntas, sí. Es exactamente el fenómeno que justificaba
hacer la combinación: dos efectos individualmente insuficientes cuyo efecto conjunto cruza el cero, y que
**ningún análisis de sensibilidad de una sola variable habría encontrado**.

### Las cautelas, que siguen siendo las mismas y en el mismo sitio

1. **La significación no cambia para ninguno de los dos.** Ni `gemma4:31b-mlx` ni `gemma4:latest` alcanzan el
   umbral de Tukey en el informe, y no lo alcanzan tampoco en ningún escenario. Lo que se mueve es el signo
   de la estimación puntual.
2. **Las dos correcciones no tienen el mismo estatus.** Corregir el emparejamiento duplicado va **hacia** la
   medida correcta —cuenta cada referencia una vez, y el propio informe reconoce el defecto—; aislar el
   parseo alterno es **hipotético**, porque descarta mediciones reales de la tubería.
3. **Es una fila de veintiséis y dos modelos de doce.** El resto se mueve por debajo de medio punto, y los
   dos significativos siguen intactos: `llama3.2:latest` de +10,82 a +11,67.

**Lo que esto añade a la decisión 18:** ya no es un modelo sino **dos**, y uno de ellos solo aparece al
combinar. Si se declara la sensibilidad, conviene declararla **como combinación** y no como dos notas
sueltas, porque por separado ninguna de las dos habría mostrado el caso de `gemma4:latest`.

---

## §F112 — La misma tabla por dos rutas: 25 grupos de 26 coinciden, y el que no ya se sabía

**Fecha:** 2026-09-09 · **Origen:** mecanizar el análisis de [§F111](#f111)

La Tabla 7 se escribió desde la columna `f1` del CSV consolidado, y `c_tabla7_vs_datos` la ata a
esa fuente. Eso comprueba la transcripción, no la cifra: si el CSV estuviera mal, la tabla y el CSV
coincidirían igual.

Al mecanizar la sensibilidad combinada quedó disponible la otra ruta —el F1 recalculado desde los
`per_type`, que son los recuentos de los que ese CSV sale— y contrastar las dos cuesta 0,16 s. De
los **26 grupos, 25 coinciden por las dos rutas** con tolerancia de 0,05 puntos. El único que no es
`nemotron-mini:4b_baseline`: publicado 22,59, desde `per_type` 21,4985, **−1,0915**.

No es un hallazgo nuevo, y eso es exactamente lo que lo hace útil: es [§F110](#f110) otra vez, seis
registros re-extraídos fuera del arnés cuyas métricas solo llegaron al CSV. Que la comprobación
independiente encuentre **ese** grupo y ninguno más acredita dos cosas a la vez: que las otras 25
cifras publicadas son correctas por dos caminos, y que el defecto de §F110 está acotado a un grupo
y no es la punta de algo mayor.

**Lo que se ha hecho.** `tools/sensibilidad_combinada.py`, que reproduce los cuatro escenarios de
§F111 —`per_type` tal cual, aislando el parseo alterno, corrigiendo el emparejamiento duplicado, y
las dos cosas— y confirma el resultado: `gemma4:latest` pasa de −1,1698 a **+0,4739**, y solo al
combinar; `gemma4:31b-mlx` también cambia de signo, pero le basta una de las dos. La herramienta
reutiliza `recalcula` de `efecto_emparejamiento_duplicado.py` en lugar de reimplementarla, y
**no usa `overall.f1`**, que es lo que invalidó la primera versión del análisis.

Y comprobación **45** del verificador, que es donde esto deja de depender de que alguien se acuerde.
Su fallo está declarado con su responsable —el equipo remoto, `§3.bis.15`—, de modo que **al
cerrarse la re-corrida el fallo desaparece solo y hay que levantar la exclusión** de
`nemotron-mini:4b_baseline` en la herramienta. La herramienta lo dice en cada ejecución: comprueba
si el grupo ya es coherente con su CSV y, cuando lo sea, imprime que se puede quitar de `EXCLUIDOS`.

**Probado por mutación**, en el documento y no en la herramienta: alterada la cifra publicada de
`qwen2.5:14b` de 50,22 a 99,99, la comprobación pasa de `CONOC` a `FALLA` y añade la fila con la
divergencia de −49,77. Y sobre la propia herramienta, invertida la detección de cambio de signo,
los modelos señalados pasan de 2 a 12.

**Estado del verificador:** 45 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F113 — La campaña nueva no refresca cifras: arregla §F53, y con ello el estudio pierde una de sus dos conclusiones significativas

**Fecha:** 2026-09-09 · **Origen:** verificar la entrega de `§3.bis.15` del equipo de 48 GB

El equipo entregó el arreglo del `TypeError` de `§F85` y un consolidado nuevo,
`ANALISIS_CONJUNTO_20260909_FIX`, con la nota «la conclusión no cambia; la magnitud sí». **El
arreglo es correcto y su F reproduce exacto.** Lo que la nota no dice es todo lo demás, y es mucho.

### El consolidado nuevo no comparte ni una fuente con el publicado

No es el consolidado publicado con `nemotron` corregido: son **trece corridas de
`recorrida_20260908/`**, una campaña completa distinta. El publicado se fusiona de **ocho** fuentes
heterogéneas; el nuevo de **trece**, una por modelo, y **la intersección de las dos listas es
vacía**.

### Corrección del 2026-09-09, posterior: el informe SÍ declara §F53, y una de las tres consecuencias no era nueva

> Dos rectificaciones a lo que sigue, hechas al releer el informe y al calcular la métrica restringida.
> Cambian la urgencia de la decisión 1, de modo que van arriba y no en una nota al pie.
>
> **1. El informe declara el defecto por completo.** `§2` dedica un párrafo entero a la categoría
> fantasma: el 66,0 % de los falsos positivos, la causa exacta —el conversor filtra por
> `["PER", "ORG"]`—, la corrección del corpus del 8 de septiembre, y la frase «las cifras de este
> informe son anteriores a esa corrección y se conservan tal como se midieron; sustituirlas exige
> volver a inferir, **que es lo que hará la re-corrida pendiente**». Además el informe **ya publica
> una segunda medición restringida** a las categorías anotadas, en el Anexo I, para las 42
> configuraciones. Decir que «los datos publicados llevan el defecto dentro» es cierto y sigue
> escrito abajo, pero **no** que el informe lo oculte: lo declara y anticipa exactamente esta
> entrega.
>
> **2. La violación de homocedasticidad no la trae la campaña nueva.** Calculada la métrica
> restringida sobre los datos **publicados**, Brown-Forsythe da W = 3,7227 y **p = 1,328e-09**. Es
> decir: el supuesto ya falla en la medición corregida del propio informe, sin re-corrida ninguna.
> La p = 0,18 que el informe publica solo vale para la métrica de tres categorías, donde la categoría
> fantasma añade a **todos** los grupos la misma penalización de precisión y **comprime las
> diferencias de varianza**. Ver `§F114`.
>
> **Lo que sí se sostiene entero** es la primera consecuencia, que es la que toca una conclusión:
> `llama3.2:latest` deja de ser significativo en el consolidado nuevo. Y con un matiz que la mejora:
> en la métrica **restringida de los datos publicados** los dos modelos siguen significativos
> (`§F114`), de modo que no se sabe si la pérdida sobrevive a la métrica restringida de la campaña
> nueva — y **no se puede saber hasta que llegue `§3.bis.16`**, porque 12 de las 13 corridas nuevas
> no traen `detailed_results.json`.

### Y la campaña nueva arregla la categoría fantasma de §F53

Es el hecho decisivo, y ningún documento lo dice. El indicador barato que ordena `CLAUDE.md`
—`tp + fn` agregado por categoría— sobre el `nemotron` de cada campaña:

| Campaña | `Locations` tp | fp | fn | tp+fn |
|:---|---:|---:|---:|---:|
| Publicada (`nemotron_rerun_n120_REMOTO`) | 0 | 720 | 0 | **0** |
| Nueva (`recorrida_20260909_nemotron_fix`) | 343 | 312 | 747 | **1 090** |

En la campaña publicada `Locations` **puntúa contra el vacío**: cada acierto del modelo cuenta como
falso positivo porque el corpus no anota una sola entidad de esa categoría. En la nueva, la
referencia sí la anota. Es exactamente el defecto de [§F53](#f53), y **los datos publicados lo
llevan dentro**.

Eso explica la subida general del F1, que no es pequeña ni atribuible a la configuración
—`max_tokens` sube de 2 048 a 4 096 y `num_workers` baja de 9 a 1, pero corpus, `rag_mode`,
`fuzzy_threshold`, `system_prompt_file` y semilla son idénticos—:

| Modelo (línea base) | Publicado | Nuevo |
|:---|---:|---:|
| `llama3.2:latest` | 0,3611 | **0,6325** |
| `gemma:latest` | 0,4400 | **0,5955** |
| `mistral-nemo:latest` | 0,4338 | **0,6063** |
| `nemotron-mini:4b` | 0,2259 | **0,2829** |

### Las tres consecuencias que la nota del equipo no recoge

**Primera, y la que toca una conclusión del informe: `llama3.2:latest` deja de ser significativo.**
El informe concluye que **dos** de los trece modelos mejoran de forma significativa. En el
consolidado nuevo es **uno**.

| Modelo | Publicado | p ajustada | Nuevo | p ajustada | Veredicto |
|:---|---:|---:|---:|---:|:---|
| `nemotron-mini:4b` | +0,1452 | 0,0000 | +0,1226 | 0,0000 | se mantiene |
| `llama3.2:latest` | +0,1082 | 0,0069 | +0,0673 | **0,2334** | **se pierde** |

Y la pérdida **no es por el N menor**. Las dos cosas iban entrelazadas —el consolidado nuevo excluye
los 7 contaminados y el publicado no—, pero [§F66](#f66) ya midió el efecto de la exclusión por
separado sobre el corpus antiguo: `llama3.2:latest` pasaba de +0,1082 a +0,1006 con p de 6,9e-3 a
3,6e-2, **seguía siendo significativo**. Lo que le quita la significación es la **medición
corregida**, no el tamaño de muestra.

Dos modelos más cambian de signo, ninguno significativo: `mistral-nemo:latest` de +0,0237 a
**−0,0429**, y `gemma:latest` se desploma de +0,0736 a **+0,0003**.

**Segunda: el supuesto que sostiene el ANOVA titular se viola en los datos nuevos.** El informe
publica que «la prueba de Levene no detecta heterocedasticidad (p = 0,18)». Sobre el consolidado
nuevo, **no se sostiene**, y su `statistical_report.md` no menciona Levene ni una vez:

| | Brown-Forsythe W | p |
|:---|---:|---:|
| Publicado | 1,2475 | 0,1842 |
| Nuevo | **4,2124** | **1,394e-11** |

**El remedio está y la conclusión general aguanta.** Bajo pruebas robustas a varianzas desiguales el
resultado global es abrumador en los dos consolidados, de modo que esto obliga a **cambiar de prueba**,
no a retirar la conclusión:

| | Publicado | Nuevo |
|:---|---:|---:|
| ANOVA clásico | F = 38,2222 · p = 3,4453e-160 | F = 119,7502 · p ≈ 0 |
| Alexander-Govern | A = 724,61 · p = 9,10e-137 | A = 1 369,97 · p = 9,89e-274 |
| Kruskal-Wallis | H = 744,01 · p = 7,58e-141 | H = 1 329,91 · p = 3,52e-265 |

**Tercera: η² se duplica.** De 0,2360 a **0,5069**. La campaña nueva separa los grupos mucho mejor,
que es lo que cabe esperar al dejar de penalizar a todos los modelos por una categoría inexistente.

### Verificación

`F = 119,7502` reproducido por dos vías independientes —mi implementación en biblioteca estándar y
`scipy` del venv— coincidiendo al cuarto decimal, igual que `F = 38,2222` del publicado. Brown-Forsythe
comprobado con centrado en mediana y en media, y con las dos implementaciones. Los deltas y las p
ajustadas de Tukey salen de `statsmodels`, y **la columna del publicado reproduce exactamente las
cifras del informe** (+0,1452 y +0,1082), que es lo que acredita el método antes de leer la columna
nueva.

### Lo que esto NO es

No es un fallo del equipo de 48 GB: su encargo era arreglar `§F85` y re-ejecutar un brazo, y eso lo
hizo bien, con la corrida defectuosa conservada como prueba y con `failed == 0` ahora bloqueante. La
nota se equivoca solo al generalizar «la conclusión no cambia» desde el único modelo que comprobaron.

**Y no lo he tocado en el informe.** Adoptar el consolidado nuevo cambia prácticamente todas las
cifras publicadas y una de las dos conclusiones del capítulo de resultados. Es **decisión del autor**,
y está en la **decisión 1**, que hay que reabrir: se declaró superada suponiendo que lo único que
retenía la adopción era `§F85`.


---

## §F114 — La categoría fantasma estaba enmascarando la heterocedasticidad, y la conclusión de dos modelos vive en la métrica restringida

**Fecha:** 2026-09-09 · **Origen:** verificar la primera consecuencia de [§F113](#f113)

`§F113` atribuyó a la campaña nueva la violación del supuesto de homocedasticidad. **Es un error de
atribución.** Calculadas las dos métricas sobre los **mismos datos publicados**, reagregando desde
`per_type` los 3 120 registros de los 26 grupos:

| Métrica sobre los datos publicados | ANOVA F | p | Brown-Forsythe W | p |
|:---|---:|---:|---:|---:|
| Tres categorías (la que publica el informe) | 38,8403 | 1,094e-162 | 1,2078 | **0,2183** |
| Restringida a Personas + Organizaciones (Anexo I) | 70,2802 | 2,238e-279 | 3,7227 | **1,328e-09** |

**El supuesto ya falla en la medición que el informe presenta como corregida**, sin ninguna
re-corrida. Y el mecanismo se explica: la categoría inexistente añade a los veintiséis grupos la
misma penalización de precisión, que **comprime las diferencias de varianza entre ellos**. La
p = 0,18 no acreditaba homogeneidad de varianzas; acreditaba que un defecto común a todos los grupos
las estaba igualando. Es la misma lección de `§F53` en otra cifra: **un resultado tranquilizador
producido por el defecto, no a pesar de él**.

**La conclusión de dos modelos, en cambio, aguanta la métrica restringida:**

| Modelo | Tres categorías | p ajustada | Restringida | p ajustada |
|:---|---:|---:|---:|---:|
| `nemotron-mini:4b` | +0,1562 | 0,0000 | +0,1549 | 0,0000 |
| `llama3.2:latest` | +0,1082 | 0,0070 | +0,1021 | **0,0275** |

Los dos siguen significativos, y ningún tercer modelo entra. La conclusión del capítulo de
resultados **no depende de la categoría fantasma**, que es la comprobación que faltaba.

**Y la medición restringida es estable entre campañas.** En el único modelo donde se puede comprobar
—`nemotron-mini:4b`, el único de las trece corridas nuevas con `detailed_results.json`—:

| | Línea base | KB RAG | Δ |
|:---|---:|---:|---:|
| Publicada, restringida | 25,2759 | 40,7698 | +15,4939 |
| Nueva, restringida | 25,0186 | 40,8267 | **+15,8081** |
| Publicada, tres categorías | 21,4985 | 37,1170 | +15,6185 |
| Nueva, tres categorías | 27,8626 | 41,5765 | **+13,7139** |

La métrica restringida se mueve **0,31 pp** entre campañas; la de tres categorías, 1,90 pp. Dicho de
otro modo: **la subida general del F1 de la campaña nueva es la categoría fantasma dejando de
penalizar, no los modelos midiendo mejor.** Lo que el informe publica en el Anexo I ya es, en lo
esencial, lo que mediría la campaña nueva.

**Consecuencia práctica, y es la que ordena el cierre.** La pregunta que decide la decisión 1 no es
si adoptar el consolidado nuevo, sino **si la conclusión de dos modelos sobrevive en la métrica
restringida de la campaña nueva**. En la métrica de tres categorías `llama3.2:latest` la pierde
(`§F113`); en la restringida de los datos publicados la conserva. **Las dos cosas son compatibles y
la que importa no se puede calcular todavía**, porque doce de las trece corridas nuevas no entregan
`detailed_results.json`. Eso convierte `§3.bis.16` —clasificada como menor— en **la tarea que
desbloquea la decisión más grande del cierre**, y no requiere inferencia: los ficheros existen en la
máquina del equipo, solo hay que volcarlos.

---

## §F115 — La tercera cifra del párrafo estadístico que nadie recalculaba

**Fecha:** 2026-09-09 · **Origen:** revisar si la frase de Levene necesitaba corrección

Buscando si el informe hacía alguna afirmación inferencial sobre la métrica restringida —que
[§F114](#f114) dejó sin cubrir— apareció que **no la hace**: la medición restringida del Anexo I es
descriptiva, sin ANOVA ni Tukey. Y la frase de Levene está bien: es cierta para la métrica sobre la
que se calcula, y ya viene matizada con «no equivalga a demostrar que las varianzas son iguales».
**No había nada que corregir**, y la recomendación de §F114 de «precisarla» era más fuerte que lo
que el texto merece.

Lo que sí apareció es que **el mismo párrafo publica una tercera cifra que ninguna comprobación
tocaba**: «el post-hoc de Tukey identifica 158 comparaciones significativas de las 325 posibles». Es
el patrón de [§F91](#f91) por tercera vez en el mismo párrafo — el ANOVA y Levene ya habían obligado
a añadir las comprobaciones 30 y 31.

**La cifra es correcta.** Recalculada con `statsmodels`: 325 filas de par, que son C(26,2), y
**exactamente 158** significativas al 0,05.

**Comprobación 46**, y con una limitación declarada en su propia nota: la distribución del rango
estudentizado no está en la biblioteca estándar, de modo que **no recalcula Tukey**. Verifica dos
cosas que sí caben: el recuento contra el artefacto y contra C(26,2), y **cada veredicto del
artefacto contra su propia p ajustada**. La segunda es la que aporta: un recuento de totales no
puede ver dos errores de signo contrario, porque se compensan.

**Probada por mutación en los dos frentes.** Alterado el 158 del informe a 157, falla con el
contraste. Alterado en el artefacto un veredicto de «no» a «sí» sobre una fila con p = 1,0, falla
**por las dos vías a la vez** —el recuento sube a 159 y la coherencia señala la fila—, que es lo que
acredita que la segunda vía no es decorativa.

**Estado del verificador:** 46 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F116 — La cifra que responde a la objeción metodológica más fácil de plantear no la comprobaba nadie

**Fecha:** 2026-09-09 · **Origen:** dejar de encontrar estas cosas por casualidad

Tres cifras del mismo párrafo de §5 obligaron a añadir tres comprobaciones distintas —el ANOVA
titular en [§F91](#f91), Levene en la misma tanda, el recuento de Tukey en [§F115](#f115)— y **las
tres se encontraron tropezándose con ellas**. Tres veces el mismo patrón en el mismo párrafo
significa que el método no sirve, de modo que en lugar de esperar la cuarta hice el barrido:
`tools/cobertura_cifras.py`, que enumera las afirmaciones numéricas del cuerpo del informe y dice
cuáles no tienen ninguna comprobación anclada en su vecindad.

Son **84 afirmaciones numéricas** en el cuerpo, fuera de tablas y bloques de código. La herramienta
señaló 53 candidatas, y declara por qué esa cifra no es un veredicto: da falsos cubiertos —un ancla
cerca no prueba que compruebe esa cifra— y falsos descubiertos. Las dos cosas se confirmaron al
comprobarlas a mano, y la segunda es la que importa:

**Falso descubierto, confirmado por mutación.** El barrido marcó como no cubiertos el `ρ = −0,5165`
de Spearman y sus dos p. Alterados en el informe, `c_correlacion` los detecta con **2 fallos
nuevos**. Estaban cubiertos por una ruta que la herramienta no reconoce.

**Y un descubierto real, también por mutación.** El `χ² = 1 169,23` de Friedman: alterado a
9 999,99, el verificador da **cero fallos nuevos** sobre sus 46 comprobaciones. La razón es sutil:
`c_defensa` sí verifica ese mismo χ², pero en `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md`, **que es otro
documento**. La cifra estaba vigilada en la copia y no en el original.

**Y es la peor de las 84 para tener sin vigilar.** Es la frase con la que §5 salva la limitación que
él mismo declara —los 26 grupos evalúan los mismos 120 artículos, de modo que las observaciones
están apareadas y un ANOVA de una vía no es estrictamente el procedimiento correcto—: «repetido con
la prueba de Friedman, que es la que corresponde a un diseño de medidas repetidas, el rechazo se
sostiene con holgura (χ² = 1 169,23), de modo que la conclusión no depende de esa elección». Es la
respuesta a la objeción metodológica más fácil de plantear en una defensa.

**La cifra es correcta.** Recalculada desde el CSV consolidado: rangando los 26 valores dentro de
cada artículo sobre los 120 bloques completos, χ² = **1 169,2327**, que coincide con el informe y
con `friedman.json` al cuarto decimal.

**Comprobación 47**, que lo **recalcula** en lugar de comparar contra el artefacto y nada más, y
contrasta las tres vías. Un detalle que merece quedar escrito porque es donde una reimplementación
se equivocaría: **la corrección por empates es imprescindible**. Sin ella el estadístico sale
**1 123,0730** y con ella 1 169,2327, de modo que una implementación que la olvide reporta un fallo
donde no lo hay. Con 26 grupos sobre 120 artículos los empates abundan.

**Un defecto propio, encontrado por la herramienta contra sí misma.** La primera versión extraía las
anclas con una expresión regular sobre el código fuente del verificador, y **perdía anclas en
silencio**: un apóstrofo suelto dentro de un docstring desalinea el emparejamiento de comillas y, a
partir de ahí, todos los literales quedan mal delimitados. Daba **713** fragmentos mal cortados y
**cero** con la palabra «Levene», sobre un fichero que la usa cuatro veces y que se ancla al informe
con un regex explícito. Se detectó justamente porque Levene aparecía como no cubierto cuando yo
sabía que lo estaba. Con `ast` son **402** anclas reales. La lección general es corta: **el código
fuente se lee con un analizador sintáctico, no con una expresión regular**, y el síntoma de haberlo
hecho mal es que faltan cosas, no que sobren.

**Y una precisión sobre mi propio aviso anterior.** En [§F114](#f114) dije que la frase de Levene
convenía precisarla; en [§F115](#f115) me retracté porque el texto está bien. Este hallazgo no la
reabre: lo que faltaba no era corregir el texto sino **vigilar una cifra vecina**.

**Estado del verificador:** 47 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F117 — El primer factor con que §5 explica sus resultados tampoco tenía quien lo recalculara

**Fecha:** 2026-09-09 · **Origen:** revisar a mano las candidatas del barrido de [§F116](#f116)

El barrido dejó 52 candidatas, y la utilidad de la lista se ve en el triaje: **la mayoría eran
falsos descubiertos**, y comprobarlo cuesta poco.

| Candidata | Veredicto |
|:---|:---|
| `76,55 %`, `90,16 %`, `80,42 %` | cubiertas, pero por `auditar_afirmaciones.py`, que el barrido no mira |
| `66,0 %` | cubierta por `c_figura1_vs_artefacto` y por la auditoría de afirmaciones |
| `62,67 %`, `80,51 %` | son los dos **fallos declarados** de la decisión 13, o sea vigiladas y en rojo a propósito |
| `ρ = −0,5165`, `p = 0,0707`, `p = 0,0300` | cubiertas por `c_correlacion`, probado por mutación |
| `+3,11`, `−0,43`, `p = 0,9328` | cubiertas por la comprobación 33 y documentadas en [§F55](#f55) |
| **`+10,40`, `+4,38`, `−0,72`** | **descubiertas de verdad** |

Las tres últimas son el **primer factor** con que §5 explica la distribución de resultados:
«Redactar ambos en español aporta 10,40 puntos de F1 sin cambiar de modelo, mejora que ninguno de
los dos factores consigue por separado: traducir solo el prompt aporta 4,38 puntos y añadir ejemplos
en inglés resta 0,72». La comprobación 33 verifica el **ANOVA** de esa misma ablación (F = 1,1379,
p = 0,3417) y §7 tiene cubierta la frase de que el efecto no replica, pero **los tres deltas no los
tocaba nadie**: alterados el 10,40 a 99,99 y el 4,38 a 9,99, cero fallos nuevos sobre 47
comprobaciones.

**Las tres son correctas.** Reproducen desde `ablacion_n15_REMOTO`, que trae las cuatro celdas del
diseño con quince registros cada una:

| Celda | F1 | Contraste contra `zs-en` | Publicado |
|:---|---:|---:|---:|
| `zs-en` | 64,0451 | referencia | — |
| `zs-es` | 68,4273 | +4,3821 | 4,38 |
| `fs-en` | 63,3210 | −0,7242 | 0,72 |
| `fs-es` | 74,4447 | **+10,3996** | 10,40 |

**Comprobación 48**, y con una cuarta cosa que no es una cifra: **la afirmación de interacción**.
Que ninguno de los dos factores por separado alcance el efecto conjunto es lo que sostiene el
argumento, y una comprobación que solo cotejara los tres números dejaría pasar un texto que los
citara bien y concluyera lo contrario. Probada por mutación en los cuatro frentes, los cuatro
detectados; el cuarto se ensayó cambiando «ninguno» por «cualquiera».

**Un fallo del ensayo, no de la comprobación, que conviene dejar escrito.** Las tres primeras
mutaciones no encontraron su ancla porque las busqué en negrita, y el informe escribe esas cifras
**sin resalte** por la regla de sobriedad tipográfica del proyecto. La comprobación funcionaba —su
patrón alternativo casaba— pero mi prueba no probaba nada, que es el modo más silencioso de dar por
validada una comprobación vacua. Corregido el orden de los patrones para que el caso sin resalte sea
el primero, y anotado en el docstring: la próxima cifra que se verifique ahí tampoco estará en
negrita.

**Y por segunda vez seguida, la comprobación 43 detectó mi propia referencia colgante** a este mismo
`§F117` mientras lo escribía. Es la tercera vez en la sesión que una comprobación del proyecto
encuentra un defecto de quien las escribe.

**Estado del verificador:** 48 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F118 — El informe se cita a sí mismo redondeado, y ese redondeo no lo comprobaba nadie

**Fecha:** 2026-09-09 · **Origen:** reducir el ruido del barrido de [§F116](#f116) en lugar de
triar cincuenta cifras a mano

Triar las candidatas una a una es lo que §L61 dice que no se haga, así que en vez de eso mecanicé el
triaje que ya había hecho a mano en [§F117](#f117). Tres rutas de cobertura nuevas, y la lista pasa
de **50 a 12**:

| Ruta | Qué reconoce | Efecto |
|:---|:---|---:|
| Segunda fuente de anclas | `auditar_afirmaciones.py` también comprueba el informe | −4 |
| Fallos declarados | una cifra en rojo a propósito **está** vigilada | −3 |
| Valores de artefactos | las comprobaciones que no se anclan en prosa leen el JSON y buscan la cifra | −34 |

De las 12 restantes, dos son **cifras de la literatura** —el 88,43 % del ajuste fino de BERT sobre
CoNLL-2002 y su comparación— y no hay nada que recalcular: se acreditan por la cita. Las otras diez
son **una sola clase de defecto**, y es la que faltaba: **el informe se cita a sí mismo redondeado**.

| Sitio | Forma redondeada | Cifra precisa de §5 |
|:---|:---|:---|
| Resumen y abstract | +14,5 y +10,8 puntos | +14,52 y +10,82 |
| Resumen | +10,4 puntos | 10,40 |
| Conclusiones | ρ = −0,52, p = 0,071 | −0,5165, p = 0,0707 |
| §2 y §6, cuatro veces | 20,1 % | 283 de 1 406 |
| §5.5 y §6 | 99,4 % | 1 − 0,052 / 8,75 |

Es exactamente la forma en que entró el defecto de [§L69](#l69): propagadas las cifras precisas
81,45 → 80,42 y 76,85 → 76,55, quedó «cinco puntos» describiendo una resta de 3,87, y el documento
pasó de coherente-con-datos-viejos a **incoherente consigo mismo**. Y afecta al **resumen**, que es
la primera página y lo único que algunos lectores leen.

**Las diez cuadran.** 14,52 → 14,5; 10,82 → 10,8; 10,3996 → 10,4; 0,5165 → 0,52; 0,0707 → 0,071;
283/1 406 = 20,128 → 20,1; 1 − 0,052/8,75 = 0,99406 → 99,4 %.

**Comprobación 49**, que **no escribe ninguna cifra**: lee las dos formas del documento y comprueba
que la redondeada sea el redondeo de la precisa. Una constante copiada aquí detectaría una deriva de
los datos pero no una del texto, que es el defecto que la comprobación 22 ya tuvo y que
[§L63](#l63) deja escrito. Comprueba además que la reducción de coste **siga declarada como
estimación** en los dos sitios donde aparece, que es una regla de `CLAUDE.md` y no una cifra.

**Y repetí §L59 escribiéndola.** La primera versión leía el porcentaje del *mojibake* con
`re.search`, y ese porcentaje aparece **cuatro veces** en redacciones distintas —dos en prosa, una
en la lista de limitaciones y una en una tabla—. Alterar la de la tabla no lo notaba nadie. Es
literalmente la lección que dice que `re.search` ve solo la primera aparición, escrita a propósito
después de que pasara con la frase del «efecto que se anula». Corregido a `finditer` sobre todas las
apariciones, y añadida la comprobación de que no haya dos valores distintos entre ellas; probado
mutando **solo la de la tabla**, que antes era invisible.

**Dos anclas de prueba mal puestas, otra vez.** Tres mutaciones de §F117 fallaron por buscar las
cifras en negrita, y aquí una falló por omitir los asteriscos y el `>` de una cita en bloque. En los
dos casos la comprobación funcionaba y **el ensayo no ensayaba nada**. Vale la pena el recordatorio:
una mutación que no encuentra su ancla es un ensayo fallido, no una comprobación validada, y hay que
distinguirlo del caso en que la comprobación no detecta el cambio.

### Corrección inmediata, y es el mismo defecto del que trata este hallazgo

Escribí arriba que el barrido «queda en 12 candidatas». **Dejó de ser cierto en el mismo commit**:
al añadirse la comprobación 49, sus anclas cuentan como cobertura y el barrido pasó a **5**. Luego
a **3**, tras arreglar el filtro de anclas —exigía cuatro letras seguidas, y el ancla
`ρ = −(0),(\d{2}) con p` no las tiene, de modo que sus dos cifras salían descubiertas estando
cubiertas—. Anotar una cifra que la siguiente línea de trabajo invalida es exactamente lo que este
hallazgo describe, y no lo evité escribiéndolo.

**Estado final del barrido: 3 candidatas.** Dos son las cifras de la literatura, que no hay nada que
recalcular, y la tercera es una aparición del `66,0 %` cubierta por otras dos comprobaciones y por
la auditoría de afirmaciones. **Ninguna afirmación numérica del cuerpo del informe queda sin quien
la mire.**

**Estado del verificador:** 49 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F119 — Una tabla de seis medidas que el corpus actual ya no puede reproducir

**Fecha:** 2026-09-09 · **Origen:** comprobar un supuesto que yo mismo había escrito

`tools/cobertura_cifras.py` excluye las tablas del barrido con el comentario «se verifican por otra
vía». **Eso era un supuesto, no una comprobación**, así que lo verifiqué: de las **20 tablas** con
leyenda, **11 no se mencionan** en ninguna de las dos herramientas que comprueban el informe.

**Diez de esas once son descriptivas** —las tablas 1, 2, 3, 9, 10, 11, 12, 13, 14 y 16: familias
de técnicas, estado del arte, arquitectura por capas, estructura del repositorio, entorno de
pruebas, configuración del módulo, contenido de la base de conocimientos y formas corruptas de los
nombres— y no hay nada que recalcular: se acreditan por su cita o por el código que describen.

La undécima es la **Tabla 17, «Alcance medido del defecto de codificación sobre el corpus N=120»**,
que son **seis medidas**.

### Por qué estaba fuera del alcance de todo

Medirla contra el corpus actual **da cero en todas sus filas**. No porque la tabla esté mal, sino
porque describe un estado que ya no existe: el informe declara en §2 que «el defecto está corregido
en el corpus desde el 8 de septiembre de 2026» y que sus cifras «se conservan tal como se midieron».
Hoy el fichero trae **0 entidades con *mojibake*** y **545 localizaciones** que entonces no tenía
—de ahí que el total pase de 1 406 a 1 951—.

Es una clase de afirmación que el verificador no cubría en absoluto: **una medición histórica**. No
se puede atar al dato actual, y no atarla a nada la deja indefinidamente sin vigilancia.

### La ruta que sí funciona

La historia de git, que es un artefacto que **atestigua** y por eso se conserva. Recorriendo
`git log --follow` sobre el corpus y midiendo cada versión aparece exactamente dónde vive la tabla:

| Commit | Fecha | Entidades P+O | `locations` | Con *mojibake* | Artículos afectados |
|:---|:---|---:|---:|---:|---:|
| `f49c03c` | 2026-09-08 | 1 406 | 545 | 0 | 0 |
| `c776fe0` | 2026-09-08 | 1 406 | 482 | 0 | 0 |
| `eb97af0` | 2026-09-08 | 1 406 | 0 | 0 | 0 |
| **`df9b4c4`** | **2026-09-06** | **1 406** | 0 | **283** | **104** |

Sobre `df9b4c4` las seis filas reproducen **exactas**: 1 406 entidades, 283 con *mojibake*, 66
irrecuperables con umbral 85 (4,69 % → 4,7 %), 104 de 120 artículos, 283 de 283 igual de corruptas y
0 correctas. Y el ejemplo que la prosa cita como recuperable, `Emiliano GarcÃ­a-Page`, da razón
**92,7**, que redondea al 93 publicado.

### Comprobación 50, con dos reimplementaciones

La primera es la **detección del defecto por su definición** y no por una clase de caracteres: una
cadena está corrupta si recodificarla de `latin-1` a `utf-8` tiene éxito y cambia el resultado, que
es exactamente lo que significa «bytes UTF-8 reinterpretados como Latin-1». Más corto y más exacto
que enumerar los caracteres sospechosos.

La segunda es **`fuzz.ratio` en biblioteca estándar**, porque `rapidfuzz` solo está en el venv y una
comprobación que solo corre en un entorno no corre. Es la similitud de Indel normalizada,
`200 · LCS / (len a + len b)`, y está **validada contra `rapidfuzz` sobre los 283 pares del corpus
histórico: diferencia máxima 0,0 y cero discrepancias de veredicto**. No sirve
`difflib.SequenceMatcher.ratio`, que usa bloques coincidentes en lugar de la subsecuencia común más
larga: da valores parecidos y no iguales, y aquí se compara contra un umbral.

**Y un detalle de operación que la comprobación declara en su fallo**: un clon superficial no trae
`df9b4c4`, y sin ese commit la Tabla 17 **no se puede verificar contra nada**. La comprobación lo
dice con esas palabras en lugar de pasar en silencio.

**El propio verificador encontró mi error al escribirla.** La primera versión usaba `json` sin
importarlo en la función, y `ejecutar` lo reportó como **VACÍA (reventó) — NameError**, que es su
comportamiento diseñado: una comprobación que revienta tiene que decir cuál es y seguir.

**Estado del verificador:** 50 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F120 — El entregable contradecía a su propia tabla, y las cincuenta comprobaciones miraban el otro fichero

**Fecha:** 2026-09-09 · **Origen:** notar que las comprobaciones 45 a 50 leen todas el Markdown

Las seis comprobaciones añadidas hoy verifican el **Markdown canónico**. El entregable es el
`.docx`, y si una de esas cifras divergiera allí, ninguna lo vería. Ejecutado
`tools/desfase_cifras_docx.py`, resultó que **diez cifras están en el Markdown y no en los `.docx`**,
y comparando por **párrafo** —no por cifra— aparecieron dos párrafos de la fuente ausentes de los
tres entregables y siete emparejados pero distintos.

### El más grave: el texto contradice a la tabla que introduce

| | Texto |
|:---|:---|
| Markdown | «**veintiuna de las veintiséis** configuraciones puntúan mejor […] y **veintitrés** puntúan peor» |
| Los tres `.docx` | «**19 de las 24** configuraciones puntúan mejor […] y **5 de las 24** puntúan peor» |

La Tabla 18 del `.docx` tiene **26 filas de datos, idénticas a las del Markdown** —es lo que la
comprobación 27 verifica, con sus 52 elementos—. De modo que **la tabla se propagó y la prosa que la
describe no**, y el entregable afirmaba una cosa justo encima de una tabla que dice otra.

**Recalculado desde esas 26 filas**, el Markdown es el que cuadra:

| Criterio | Δ > 0 (mejor) | Δ < 0 (peor) |
|:---|---:|---:|
| Por entidad de referencia | **21** | 5 |
| Por texto de entrada | 3 | **23** |

Y el error del `.docx` era doble: el 19 es un recuento antiguo sobre 24 configuraciones, y **el 5 es
el recuento de la otra columna** —los que puntúan peor por entidad de referencia—, de modo que el
texto además **confundía el criterio**. Es exactamente el defecto que §5.x advierte que hay que
evitar: el signo del efecto depende de qué criterio se elija, y esa dependencia es el resultado.

**Corregido** con `tools/docx_replace_terms.py` y las reglas de `tools/terms_desfase_mojibake.json`:
tres reemplazos en cada uno de los tres entregables, todos aplicados según lo esperado, con respaldo
previo. No es una decisión editorial: **el Markdown canónico ya decía 21 y 23**, y esto solo lo
propaga, que es el flujo que `CLAUDE.md` fija.

Un efecto lateral que la comprobación 39 detectó y explicó sola: el reemplazo de `R2` fue entre
`runs` y el texto nuevo heredó el formato del primero, que no estaba en negrita, así que los
resaltes del cuerpo bajaron de 16 a **14**. Van en la dirección correcta —son dos cifras derivadas
de una tabla, y `CLAUDE.md` reserva la negrita para las que la tabla no recoge—, de modo que se bajó
`BOLD_CUERPO_BASE` a 14 para que la comprobación siga vigilando que no **crezcan** desde el estado
nuevo, que es lo que vigila.

### Lo que NO he corregido, y por qué

Tres divergencias más, todas en la misma dirección —el `.docx` conserva una versión anterior—, que
**no toco porque son inserciones de texto y el cuerpo tiene un límite duro de 25 páginas**. Van aquí
con el texto exacto para la pasada de maquetación:

**1. Falta la prueba de Friedman, y con ella la respuesta a la objeción del diseño apareado.** La
palabra «Friedman» aparece **cero veces** en los tres `.docx`, y `169,23` también.

| | Texto |
|:---|:---|
| Markdown | «La prueba de Levene **no detecta heterocedasticidad** (p = 0,18), lo que con 3 120 observaciones sí es informativo, **aunque no equivalga a demostrar que las varianzas son iguales**. Y tratar como independientes unas observaciones apareadas hace el contraste conservador: repetido con la prueba de **Friedman**, que es la que corresponde a un diseño de medidas repetidas, el rechazo se sostiene con holgura (χ² = 1 169,23), de modo que la conclusión no depende de esa elección.» |
| Los tres `.docx` | «La homocedasticidad **se verifica** (Levene, p = 0,18) y, al ser el diseño pareado más potente que el independiente, la significancia obtenida por esta vía es conservadora.» |

Dos problemas, y el segundo es peor que la ausencia. El `.docx` **afirma lo que el Markdown dice
expresamente que no se puede afirmar**: Levene no verifica la homocedasticidad, solo no la rechaza,
y una p de 0,18 no demuestra que las varianzas sean iguales. Y donde el Markdown aporta **una
prueba** —Friedman, con su χ²—, el `.docx` argumenta por aserción. Es el párrafo que sostiene la
principal debilidad metodológica declarada del trabajo, y la versión del entregable es la más
atacable de las dos. Añade unos 300 caracteres, unas 50 palabras.

**2. Párrafos de la fuente que no están en ningún `.docx`.** Aquí escribí «dos», y al construir la
comprobación que faltaba resultaron ser **diez**. Corregido y desarrollado en [§F121](#f121), que es
donde está el alcance real.

**3. Cinco párrafos más emparejados pero no idénticos**, con similitud entre 0,85 y 0,91: la
formulación de los objetivos específicos, la definición de RAG, la frase de la brecha —a la que el
Markdown añade «y con una medición cuyos límites estén declarados»—, el módulo KB RAG y la cautela
metodológica de la tabla, que en el Markdown advierte de **dos** versiones anteriores y en el
`.docx` de una.

**La lección, que es la que importa.** Cincuenta comprobaciones sobre el Markdown no acreditan el
entregable. `c_excluidos`, `c_sobriedad_docx`, `c_docx_sano` y las dos de tablas sí lo leen, pero
ninguna comparaba **la prosa**, y el desfase vivía precisamente ahí. Un documento cuyo texto
contradice a su propia tabla pasa las cincuenta.

**Estado del verificador:** 50 comprobaciones, 10 fallos (10 declarados, **0 nuevos**), 0 vacías.

---

## §F121 — No eran dos párrafos: son diez, y cinco de ellos son la declaración que la regla de integridad exige

**Fecha:** 2026-09-09 · **Origen:** construir la comprobación que [§F120](#f120) dejó pendiente

`§F120` reportó «dos párrafos de la fuente ausentes de los tres entregables». Al construir la
comprobación **son diez**, y la corrección importa porque cambia lo que está en juego.

El recuento inicial salió de una prueba mala: buscar los primeros 60 caracteres del párrafo
literalmente en el `.docx`. Eso falla ante **cualquier** reformulación, de modo que contaba como
ausente todo lo reescrito. La prueba correcta es sondear el `.docx` con **cinco frases distintivas
repartidas por el párrafo** y declararlo ausente solo si no aparece ninguna. De los doce que no
casaban por similitud, **dos sí estaban** —reescritos, con similitud de 0,28 y 0,35— y **diez no
están en absoluto**.

### Cinco de los diez son un solo bloque, y es el que más pesa

| Párrafo ausente | Qué declara |
|:---|:---|
| «**Cuatro de los trece modelos se midieron más de una vez** sobre el corpus N=120, de modo que ocho de los veintiséis grupos disponen de dos o tres corridas» | que existen corridas múltiples |
| «Conviene separar dos situaciones que no son la misma. Seis de esos ocho grupos tienen una corrida previa que no es una medición alternativa sino una **medición inválida**» | por qué no todas cuentan |
| «Los motivos de invalidez son dos. El modo de razonamiento activo hacía que el modelo consumiera el presupuesto de salida deliberando…» | el primer motivo |
| «El presupuesto de salida agotado produce el mismo efecto por otra vía: `gpt-oss:20b` es un modelo de razonamiento, y con 2 048 tokens…» | el segundo |
| «La última fila acredita que **el criterio fue la validez de la medición y no su resultado**: en `nemotron-mini:4b` con KB RAG la corrida publicada da menos…» | que la selección no fue por conveniencia |

Es **la declaración de corridas múltiples**, y `CLAUDE.md` la exige en estos términos:

> «Cuando existan varias corridas del mismo experimento, **el informe declara todas**. Se explica
> cuál se toma como referencia y por qué. Citar la más favorable sin mencionar las demás es
> indistinguible de seleccionar el resultado, aunque no haya intención de hacerlo, **y es lo que un
> tribunal juzga**.»

**El Markdown cumple la regla. El entregable no la contiene.** Y el último de los cinco párrafos es
justamente el que desarma la objeción, porque muestra un caso en que el criterio de validez
seleccionó la corrida **menos** favorable. Sin él, un tribunal que descubra las corridas múltiples
por su cuenta no tiene en el documento nada que responda.

### Los otros cinco

«La carencia de datos etiquetados no es una suposición de partida sino una constatación de este
trabajo», «A la carencia de datos se suma una dificultad de medición que el planteamiento no puede
dar por resuelta», «Dos rasgos del problema explican por qué no basta con una solución puntual»,
«Tres advertencias de lectura antes de las cifras» y «El efecto se midió sobre las veintiséis
configuraciones del estudio». Los cuatro primeros son declaraciones de límites del planteamiento;
el quinto es la versión canónica de la frase cuyo contador corregí en `§F120`.

### Comprobación 51

Compara **la prosa** de los tres entregables contra el Markdown, párrafo a párrafo, que es lo que
ninguna de las cincuenta anteriores hacía: cinco leen los `.docx` —modelos excluidos, sobriedad,
OOXML sano y las dos de tablas— y ninguna miraba el texto. **234 elementos.** Los treinta fallos
—diez párrafos por tres ficheros— quedan **declarados** a nombre de la pasada de maquetación, con su
motivo, de modo que no cortan; **cualquier divergencia nueva sí**.

**No los inserto.** Son unas 1 500 palabras y el cuerpo tiene un límite duro de **25 páginas** con
23,0 usadas. Insertar diez párrafos es una decisión de maquetación y de espacio que corresponde al
autor, y `CLAUDE.md` reserva expresamente a su autorización cualquier movimiento de párrafos por
motivos de espacio. Queda como **decisión 19**.

**Lo que esto dice del método.** `§F120` encontró el desfase y lo midió mal, con una prueba que
parecía razonable y no lo era. La comprobación mecánica lo corrigió el mismo día. Una cifra en el
registro vale lo que vale la prueba que la produjo, y «busqué el texto y no estaba» no es una prueba
cuando el texto pudo haberse reescrito.

**Estado del verificador:** 51 comprobaciones, 40 fallos (40 declarados, **0 nuevos**), 0 vacías.

---

## §F122 — Una comprobación nueva dejó a la autoprueba sin tiempo, y el corte borró un fichero rastreado

**Fecha:** 2026-09-09 · **Origen:** añadir la comprobación 51

La comprobación 51 compara 78 párrafos del Markdown contra 193 del `.docx`, por tres entregables,
con `difflib.SequenceMatcher.ratio()`. Eso llevó el verificador de **0,67 s a 7,80 s**, y la
autoprueba —que lo ejecuta **una vez por artefacto vigilado**, veintiuna veces— se pasó de tiempo.
Una puerta lenta deja de usarse, que es exactamente el motivo por el que el gancho de commit corre
sin red.

**Optimizada a 1,66 s** con dos atajos: un índice por los primeros 48 caracteres normalizados, que
resuelve la mayoría sin comparar nada porque los párrafos arrancan igual en los dos documentos; y
para el resto, la cascada `real_quick_ratio → quick_ratio → ratio`, que son cotas superiores
sucesivamente más caras y más ajustadas, de modo que la cara no se calcula si la barata ya no
alcanza el mejor puntaje visto.

**La prueba de que la optimización está bien es que el resultado no cambie**, y se comprobó de la
única forma que vale: cargando la versión anterior desde git y comparando **los treinta fallos uno
por uno**. Idénticos. La primera comparación que hice cubría solo ocho, porque la salida trunca en
«y 22 más» — una comprobación de la comprobación que mira un cuarto de los casos no acredita nada.

### Y el corte por tiempo borró un fichero rastreado

Esto es lo que importa. La autoprueba esconde cada artefacto con `shutil.move` y lo devuelve en un
`finally`, y **un `finally` no corre si el proceso recibe una señal**. Al cortarse por tiempo dejó
`benchmark_balanced_120_20260825_071207/benchmark_results.csv` **borrado**: 480 filas, cuatro
grupos, uno de los artefactos que respalda la Tabla 4 y las ANOVA secundarias.

Se recuperó con `git checkout --`, y ahí está la lección: **se pudo recuperar porque estaba
rastreado**. Un artefacto no rastreado habría desaparecido sin más, y el proyecto ya tiene una
lección escrita sobre eso —`§L?`, la de los `benchmark.log` ignorados— cuyo remedio fue versionarlos
precisamente para tener un punto de retorno.

**Arreglado con un diario**, no con un `finally` mejor: se escribe la pareja
`(ruta original, copia escondida)` **antes** de mover, con `fsync`, y se borra **después** de
devolver. Su existencia al arrancar significa que la ejecución anterior no terminó, y entonces la
herramienta devuelve lo pendiente, o lo recupera con `git checkout` si la copia ya no está, o dice
en voz alta que se perdió si no era rastreado. Más una red de seguridad que detecta y restaura
cualquier fichero rastreado borrado, al arrancar y al terminar.

**Probado interrumpiendo la herramienta a propósito**: el diario capturó el pendiente y la ejecución
siguiente lo devolvió sola.

**Y un error de colocación que se vio solo.** Puse la recuperación **después** de la corrida de
control, y entonces el control corría con el artefacto todavía ausente y daba por «ya fallidas»
**once comprobaciones que están bien** —entre ellas el ANOVA titular—, descontándolas como
centinelas e **invalidando la prueba entera**. Se detectó porque el aviso listaba el ANOVA titular
entre las fallidas, que es imposible con todo en su sitio. La recuperación va como primera cosa de
`main()`.

**Estado del verificador:** 51 comprobaciones, 40 fallos (40 declarados, **0 nuevos**), 0 vacías.
Autoprueba en 1,66 s por corrida.

---

## §F123 — La pregunta que decidía la decisión 1, respondida: la conclusión sobrevive en la métrica restringida

**Fecha:** 2026-09-09 · **Origen:** el equipo de 48 GB entregó `§3.bis.16`

[§F114](#f114) dejó la decisión 1 esperando **una cifra que no se podía calcular**: si la conclusión
de dos modelos significativos sobrevive en la métrica **restringida de la campaña nueva**. En la de
tres categorías `llama3.2:latest` la pierde ([§F113](#f113)); en la restringida de los datos
publicados la conserva. Las dos cosas eran compatibles y faltaba la tercera casilla, que exigía el
`per_type` de las trece corridas nuevas.

**El equipo lo entregó** en el commit `3716790`: 13 de 13 corridas N=120 con su
`detailed_results.json`. Calculado el mismo día:

| Métrica | ANOVA F | Brown-Forsythe p | Modelos significativos |
|:---|---:|---:|:---|
| Publicado, tres categorías | 38,2222 | 0,1842 | `llama3.2:latest`, `nemotron-mini:4b` |
| Publicado, restringida | 70,2802 | 1,33e-09 | `llama3.2:latest`, `nemotron-mini:4b` |
| Campaña nueva, tres categorías | 119,7502 | 1,39e-11 | solo `nemotron-mini:4b` |
| **Campaña nueva, restringida** | **79,6730** | **9,99e-10** | **`llama3.2:latest`, `nemotron-mini:4b`** |

**La conclusión del trabajo se sostiene en las tres de las cuatro casillas que miden lo que el
informe presenta como corregido**, con deltas mayores que los publicados: `llama3.2:latest` pasa de
+0,1082 a **+0,1111** (p ajustada **0,0075**) y `nemotron-mini:4b` de +0,1452 a **+0,1441**
(p = 0,0000). Y ningún tercer modelo entra en ninguna de las cuatro.

**La pérdida de `llama3.2:latest` en la métrica de tres categorías de la campaña nueva es un
artefacto**, y ahora se puede decir por qué: al arreglarse la categoría fantasma, `Locations` pasa
de aportar solo falsos positivos —los mismos a los dos modos, línea base y KB RAG— a aportar
aciertos reales, lo que **comprime la diferencia entre modos** en el modelo cuyo margen era más
estrecho. La métrica restringida no tiene esa contaminación en ninguna de las dos campañas, y es la
única de las cuatro casillas comparable consigo misma.

**Lo que queda igual en todas las variantes corregidas: la homocedasticidad no se cumple.** Las tres
casillas que no son la publicada dan p entre 1,4e-11 y 1e-09, de modo que el ANOVA de una vía deja
de ser la prueba adecuada en cuanto se corrige la medición, con independencia de qué consolidado se
adopte. Es `§F114` confirmado sobre datos nuevos: la p = 0,18 del informe no acreditaba homogeneidad
de varianzas, acreditaba que un defecto común a los 26 grupos las estaba igualando. Bajo
Alexander-Govern y Kruskal-Wallis el resultado global es abrumador en las cuatro, así que **obliga a
cambiar de prueba, no a retirar la conclusión**.

**Consecuencia para la decisión 1.** Ya no hay nada pendiente de calcular: adoptar el consolidado
nuevo es seguro para la conclusión del capítulo de resultados **si la significación se declara sobre
la métrica restringida**, que es la que el informe ya presenta como corregida en el Anexo I.

### Corrección del mismo día: la frase de Levene NO hay que cambiarla si no se adopta nada

Escribí arriba que la frase de la prueba del supuesto «hay que cambiarla en cualquier caso», y eso
**contradice [§F115](#f115)**, donde dos turnos antes me había retractado justamente de esa
recomendación. Comprobado otra vez: el informe hace **cero** afirmaciones inferenciales sobre la
métrica restringida —el Anexo I es descriptivo—, y el ANOVA publicado se calcula sobre la métrica de
tres categorías, que es la misma sobre la que se calcula la p = 0,18. **La frase es cierta para la
métrica sobre la que se computa, y ya viene matizada** con «aunque no equivalga a demostrar que las
varianzas son iguales».

De modo que la condición correcta es más estrecha: **cambiar la frase del supuesto es obligatorio
solo si se adopta el consolidado nuevo**, porque entonces el ANOVA titular pasa a calcularse sobre
datos donde Brown-Forsythe da p = 1,39e-11. Si no se adopta, el documento queda coherente como está.

Es el defecto de [§L69](#l69) en mi propio registro: una recomendación retirada que reaparece en un
hallazgo posterior porque no releí el anterior. Y es la segunda vez en la sesión que ocurre con esta
misma frase.

**Estado del verificador:** 51 comprobaciones, 40 fallos (40 declarados, **0 nuevos**), 0 vacías.

---

## §F124 — Una afirmación sobre una ruta sobrevivió a la desaparición de la ruta

**Fecha:** 2026-09-09 · **Origen:** comprobar qué dejó colgando la retirada de los artefactos
defectuosos

Retirado `nemotron-mini_4b__N120_F85_BUGGY` por instrucción del autor —«en el estudio deben existir
solo corridas y *benchmarks* exitosos, no conservar nada defectuoso»—, revisé qué quedaba apuntando
a esa ruta. **Ninguna herramienta la lee**, así que nada se rompió. Pero la nota del consolidado
nuevo, que el propio equipo escribió, decía:

> «La corrida *buggy* **se conserva** en `results/recorrida_20260908/nemotron-mini_4b__N120_F85_BUGGY/`
> con su `benchmark.log` (58 mensajes del TypeError), porque es la prueba del defecto. **No se
> borra.**»

Y el directorio se había retirado **ese mismo día**, en el mismo commit que entregó `§3.bis.16`.

Es [§L70](#l70) otra vez, aplicado a una ruta en lugar de a una cifra: **la afirmación sobrevivió al
hecho que describía**. Y es de la clase más silenciosa, porque un `git status` limpio no lo detecta
—la nota se escribió correctamente— y ninguna comprobación fallaba, porque nada la leía.

**Corregido de forma aditiva**, que es la política: el texto original queda **tachado** y no
borrado, con una nota que explica qué cambió, cuándo y por qué, y que precisa lo que sigue siendo
verdad —la evidencia del defecto está escrita con sus cifras en `§F85`, `§F108` y `§F113`, de modo
que **la prueba sobrevive como registro aunque el fichero ya no esté**—. El `WORKLOG` no se toca:
registra un suceso que fue cierto cuando se escribió, y a un registro se le añade, no se le edita.

**Predicado 13 de la auditoría de afirmaciones**, y generaliza la clase en lugar de parchear el
caso: revisa las frases que **afirman conservación** —«se conserva», «no se borra», «conservado
en»— y comprueba que la ruta entre acentos graves exista. Ignora las que van en cita en bloque o
tachadas, porque ahí el texto está marcado como histórico a propósito, que es justamente lo que
permite corregir de forma aditiva sin que la comprobación se queje del texto viejo.

**Probado por mutación en dos frentes**: devuelta la nota a su afirmación original, el predicado la
señala con la ruta; y añadida a `FINDINGS` una frase que dice conservar `results/inventada_que_no_existe/`,
también la señala. Los dos con el nombre del fichero y la ruta concreta.

**Auditoría de afirmaciones:** 13 predicados, 0 que no se cumplen.

---

## §F125 — Las corridas pequeñas de la campaña nueva miden otro modo, y eso acota la decisión 1

**Fecha:** 2026-09-09 · **Origen:** verificar el protocolo de las 39 corridas nuevas

Aplicada la verificación de protocolo a las 39 corridas de `recorrida_20260908`, **26 difieren de la
referencia en `data_file`**. No es un defecto: son las 13 de N=15 (`kleptotrace.json`) y las 13 de
N=30 (`kleptotrace_augmented_30.json`), que legítimamente usan otro corpus. Pero al mirarlo apareció
algo que sí importa.

| Corridas | `rag_mode` |
|:---|:---|
| Publicadas de N=15 y N=30 (`ablacion_n15_REMOTO`, `cloud_n15_limpio_20260905`, `gemma4_31b_n15_REMOTO`, `n30_rerun_REMOTO`) | **`entities`** |
| Campaña nueva, las 39 sin excepción | **`kb_combined`** |

**Las corridas pequeñas de la campaña nueva no son una versión corregida de las publicadas: miden
otra cosa.** `entities` es la línea base de recuperación por diccionario de entidades y
`kb_combined` es la base de conocimientos contextual, que es precisamente la comparación que §5.6
del informe desarrolla. Aplicar `kb_combined` a los corpus pequeños es una extensión legítima y
coherente —la campaña usa el mismo modo en los tres corpus—, pero **no sustituye** a las cifras
publicadas de §5.1, §5.2, la ablación del idioma ni las tablas 4, 5, 6 y 8.

**Y eso acota la decisión 1, que es la consecuencia útil.** Adoptar el consolidado nuevo afecta
**solo al capítulo de N=120**: mismo corpus, mismo `kb_combined`, mismos 26 grupos. Las secciones
que se apoyan en N=15 y N=30 se quedan sobre las corridas publicadas en modo `entities`, y no hay
que revisarlas. La decisión es más pequeña de lo que parecía, y su alcance está ahora medido en
lugar de supuesto.

**La trampa que esto evita.** Un cierre apresurado podría tomar las 39 corridas nuevas como «la
versión correcta de todo» —es lo que sugiere leer «13 modelos × 3 corpus, todas VÁLIDAS»— y
sustituir con ellas las cifras de la ablación del idioma. Serían **cifras de otro experimento** bajo
el mismo encabezado, que es exactamente lo que la regla de integridad de `CLAUDE.md` prohíbe: «ninguna
columna agrupa métricas de tareas distintas bajo un mismo encabezado».

**Verificado además, sobre las 39:** cero filas con `parse_method='failed'` en 4 290, cero sin
`detailed_results.json`, cero filas con F1 > (P + R) / 2, y los nueve parámetros de referencia
coinciden salvo el `data_file` de los dos corpus pequeños, que es lo esperado.

**Estado del verificador:** 51 comprobaciones, 40 fallos (40 declarados, **0 nuevos**), 0 vacías.

---

## §F126 — Faltaba una tabla entera en el entregable, y una referencia con sus cuatro citas

**Fecha:** 2026-09-09 · **Origen:** cerrar en las tablas el hueco que [§F121](#f121) cerró en la prosa

`c_prosa_docx` cerró la comparación de la **prosa** entre fuente y entregable. Las tablas seguían
igual que antes: `auditar_afirmaciones.py` compara la 18 y la 19 celda a celda, y **las otras
dieciocho no las comparaba nadie**, incluida la **Tabla 7, que es la tabla central del estudio**. La
bibliografía tampoco.

**Dieciséis de las veinte tablas son idénticas**, la Tabla 7 entre ellas. Tres divergen, y una de
las tres es grave:

| Divergencia | Alcance |
|:---|:---|
| **Tabla 20 no está en el entregable** | 9 filas, ausente por completo; cero menciones de «Tabla 20» y cero de «Corrida sustituida» |
| Tabla 9, estructura del repositorio | 42 filas en el entregable frente a 45 en la fuente |
| Tabla 3, capa de datos | el entregable dice «validación de esquema» donde la fuente dice «validación contra el esquema FollowTheMoney [38]» |
| **Referencia [38] y sus cuatro citas** | ausentes del entregable; sus entradas [1] a [37] **sí** están y son **contiguas**, de modo que **no hay corrimiento de numeración** |

### La Tabla 20 es la que importa, y agranda la decisión 19

Su leyenda es «Grupos con más de una corrida sobre N=120, con el motivo de la sustitución y la
evidencia». Es **la tabla de la declaración de corridas múltiples**: la que acompaña a los cinco
párrafos que `§F121` encontró ausentes. De modo que al entregable le falta esa declaración
**completa**, prosa y tabla, y es la que `CLAUDE.md` exige con las palabras «es lo que un tribunal
juzga».

Dicho de otro modo: `§F121` reportó diez párrafos; el inventario cerrado es **diez párrafos más una
tabla de nueve filas más una referencia con sus cuatro citas**, y todo ello es un bloque coherente de
adiciones tardías al Markdown que nunca se propagaron.

### El primer resultado de la comparación era un defecto de la comparación

La Tabla 7 salió como divergente en su fila de `nemotron-mini:4b`, y las celdas impresas eran
idénticas. La diferencia estaba en la quinta columna: el `.docx` guarda `sí (p&lt;0.001)` y el
Markdown escribe `sí (p<0.001)`. **Son la misma cadena**; lo que faltaba era decodificar las
entidades XML antes de comparar. Si no lo hubiera mirado, habría reportado una divergencia en la
tabla central del estudio que no existe — y con `§F121` recién corregido por sobrestimar, era el
segundo aviso del mismo día de que **una divergencia detectada hay que confirmarla antes de
contarla**.

**Comprobación 52**, 63 elementos: las veinte tablas por los tres entregables y la bibliografía de
cada uno. Los doce fallos —cuatro por fichero— quedan **declarados** a nombre de la decisión 19, con
el resto de `§F121`; cualquier divergencia nueva corta.

**Estado del verificador:** 52 comprobaciones, 52 fallos (52 declarados, **0 nuevos**), 0 vacías.

---

## §F127 — No eran piezas dispersas: al entregable le falta una subsección entera de §5

**Fecha:** 2026-09-09 · **Origen:** comparar la última pieza de estructura que quedaba sin comparar

Las comprobaciones 51 y 52 cerraron la prosa, las tablas y la bibliografía del entregable. Los
**encabezados** quedaban fuera, porque la 51 solo mira párrafos de más de 160 caracteres. Con diez
párrafos, una tabla y una referencia ausentes, cabía que faltara una sección. **Falta una.**

De los **69 encabezados** del Markdown, seis no aparecen con estilo de encabezado en el `.docx` y
**cinco de los seis están en el cuerpo** con otro estilo. El sexto no está en ninguna parte:

> `#### Corridas múltiples del mismo modelo, y cuál se toma como referencia`

Y su cuerpo es, literalmente, el bloque que [§F121](#f121) y [§F126](#f126) fueron encontrando por
partes: «Cuatro de los trece modelos se midieron **más de una vez** sobre el corpus N=120 […] **La
Tabla 20 las recoge todas.** Conviene separar dos situaciones que no son la misma…».

### El inventario, cerrado y mejor planteado

Lo que le falta al entregable no son diez párrafos sueltos, una tabla huérfana y una referencia
perdida. Es **una subsección de §5, completa**:

| Pieza | Estado en el entregable |
|:---|:---|
| El encabezado `#### Corridas múltiples del mismo modelo…` | ausente |
| Sus cinco párrafos | ausentes |
| La Tabla 20, «Grupos con más de una corrida sobre N=120…» | ausente |

Y aparte, cinco párrafos de declaraciones de límites del planteamiento, la referencia [38] con sus
cuatro citas, tres filas de la Tabla 9, una celda de la Tabla 3 y la frase de Friedman de
[§F120](#f120).

**Decirlo así cambia la decisión 19**, y a mejor: «insertar la subsección que falta» es una
operación acotada, con un sitio evidente donde va —justo después de la tabla a cuya columna
«Corrida» se refiere— y con un criterio claro de prioridad si el espacio aprieta. «Diez párrafos, una
tabla y una referencia» sonaba a diez decisiones y era una.

### Tres normalizaciones, y las tres salieron de falsos positivos propios

La primera versión de la comparación reportó **doce** encabezados ausentes, entre ellos los siete
capítulos del informe. Un `.docx` de tesina sin capítulos es imposible, así que el defecto era mío,
y hubo tres:

1. **Los `#` de dentro de un bloque de código no son encabezados.** Tres comentarios de un bloque de
   ejemplo —`# Modo baseline (sin RAG)` y sus dos hermanos— salían como títulos ausentes.
2. **El número de sección no está en el texto del encabezado del `.docx`.** Lo pone la numeración
   multinivel de Word, la que `CLAUDE.md` advierte que no hay que regenerar. Sin quitarlo del lado
   del Markdown, los siete capítulos salían ausentes.
3. **La caja no coincide**, de modo que la comparación va en `casefold`.

Con las tres, de doce falsos positivos quedan cero y una ausencia real. Es el tercer aviso del día
—después de sobrestimar en `§F121` y de la entidad `&lt;` de `§F126`— de que **una divergencia
detectada hay que confirmarla antes de contarla**, y las tres veces el error estuvo en la
comparación y no en el documento.

**Comprobación 53**, 198 elementos: los 69 encabezados por los tres entregables. Los tres fallos
—uno por fichero— quedan declarados con el resto de la decisión 19.

**Estado del verificador:** 53 comprobaciones, 55 fallos (55 declarados, **0 nuevos**), 0 vacías.

---

## §F128 — Las dos figuras del informe no están en ningún entregable, y la cobertura queda cerrada

**Fecha:** 2026-09-09 · **Origen:** el último tipo de contenido sin comparar

Las comprobaciones 51, 52 y 53 cerraron la prosa, las tablas, la bibliografía y los encabezados del
entregable. Quedaban las **imágenes**, y las dos figuras del informe **no están en ninguno de los
tres `.docx`**: cero elementos `<w:drawing>` en el cuerpo y cero leyendas «Figura N.».

**Los ficheros de media no son las figuras.** El `.docx` con plantilla trae tres ficheros en
`word/media/` y siete referencias en sus `.rels`, y son el encabezado y el pie institucionales.
Contar ficheros del paquete habría dado la respuesta contraria a la verdadera, así que la
comprobación cuenta los `<w:drawing>` **del cuerpo**.

**Los originales están y son reproducibles.** `doc/figuras/falsos-positivos.png` y
`doc/figuras/efecto-kb-rag.png`, generados el 8 de septiembre, y ya verificados como **idénticos
byte a byte** al regenerarlos. No hay nada que rehacer: hay que insertarlos.

### Hoy el entregable es incompleto pero coherente, y eso importa

**No cita las figuras.** Cero apariciones de «Figura N» en los tres `.docx`. De modo que las
imágenes y sus citas faltan **juntas**, y el documento no promete nada que no muestre.

Eso convierte esto en una **carencia y no un defecto**, con una consecuencia práctica para la pasada
de maquetación: si se inserta la prosa que menciona las figuras —el párrafo del 66,0 % dice «según
recoge la Figura 1»— **sin** insertar las imágenes, el entregable pasa de incompleto a **defectuoso**.
Por eso la comprobación 54 vigila las dos cosas: que cada figura declarada esté, y que **ninguna cita
quede colgando**.

**Probada por mutación sin tocar el entregable**: sobre una copia en el área de trabajo con una cita
a «Figura 1» inyectada, la segunda rama dispara con su mensaje propio. Los entregables no se
modificaron para probarlo, que es lo correcto cuando lo que se prueba es una rama y no el documento.

### La cobertura del entregable, cerrada

| Contenido | Comprobación |
|:---|:---|
| Prosa, párrafo a párrafo | 51 (234 elementos) |
| Tablas, celda a celda, y bibliografía | 52 (63 elementos) |
| Encabezados | 53 (198 elementos) |
| Figuras y citas colgantes | **54** (9 elementos) |
| Modelos excluidos, sobriedad, sanidad OOXML, dos tablas más | 39, 41, 44 y la auditoría de afirmaciones |

**Ninguna divergencia nueva entre la fuente y el entregable puede pasar en silencio.** Las que hay
están declaradas, todas a nombre de la decisión 19, y su inventario está cerrado: **una subsección de
§5 completa** —encabezado, cinco párrafos y Tabla 20—, **las dos figuras**, la referencia [38] con
sus cuatro citas, cinco párrafos de declaraciones de límites, tres filas de la Tabla 9, una celda de
la Tabla 3 y la frase de Friedman.

**Estado del verificador:** 54 comprobaciones, 61 fallos (61 declarados, **0 nuevos**), 0 vacías.

---

## §F129 — La comprobación que audita las declaraciones se silenciaba a sí misma

**Fecha:** 2026-09-09 · **Origen:** las declaraciones llegaron a veinticinco y nadie las auditaba

`FALLOS_DECLARADOS` funciona buscando un fragmento de texto en el mensaje del fallo. **Una clave
demasiado genérica taparía fallos que su motivo no describe**, y eso no lo detectaba nada: el resumen
los contaría entre los declarados y el código de salida seguiría siendo 0. Con cinco declaraciones
era improbable; con **veinticinco** convenía comprobarlo.

**El mecanismo está limpio.** Auditadas las 25 claves contra los 61 mensajes de fallo reales:

| Comprobación | Resultado |
|:---|---:|
| Claves que silencian fallos de más de una comprobación | **0** |
| Pares de claves anidadas, donde la corta se come los fallos de la larga | **0** |
| Claves que no tapan nada | **1**, y con explicación |

La única que no tapa nada es la de la referencia [37], que pertenece a `c_urls` y **solo corre con
`--red`**. Ejecutada con red: `c_urls` da **38 elementos y exactamente un fallo**, `[37] HTTP 404`,
que es el repositorio privado hasta la purga. La declaración está viva, no caducada. De paso queda
comprobado que **las otras 37 URL de la bibliografía responden**.

### Y la comprobación nueva cometió, en su primera versión, el defecto que existe para cazar

El mensaje del aviso incluía la clave literal —«la declaración `github.com/eahumada/mti-pge-tesina`
no tapa ningún fallo»—, de modo que **esa misma declaración lo silenciaba** y salía como `DECLARADO`
en lugar de como fallo nuevo. Una comprobación cuya salida contiene la cadena que la silencia es
invisible por construcción.

**Arreglado imprimiendo un prefijo estricto** de la clave, siempre más corto que ella, que por
construcción no puede contenerla, más su número de orden para poder localizarla. La truncatura fija
no bastaba: `cita 62.67` tiene diez caracteres y cualquier corte a catorce la habría escrito entera.

**Comprobación 55**, 325 elementos —las 25 claves más los 300 pares—, y se ejecuta **al final**
porque necesita los resultados de todas las demás.

**Estado del verificador:** 55 comprobaciones, 62 fallos (62 declarados, **0 nuevos**), 0 vacías.

---

## §F130 — En un clon limpio la puerta anunciaba «código de salida 0» mientras devolvía 1

**Fecha:** 2026-09-09 · **Origen:** comprobar que el aparato funciona donde no se ha construido

Cincuenta y cinco comprobaciones, la autoprueba y la auditoría de afirmaciones corren en **esta**
copia de trabajo. Nunca las había ejecutado en un clon, que es donde las ejecutaría otra persona.
Clonado de verdad desde el remoto con `--depth 1`, aparecen **tres cosas que un clon no tiene**, y
un defecto en cómo la puerta lo cuenta.

### Lo que un clon no trae

| | Consecuencia |
|:---|:---|
| `core.hooksPath` es configuración **local** | el clon **no tiene la puerta de commit**, aunque el gancho esté versionado (ya escrito en `§F93`) |
| Un clon superficial no trae el commit **`df9b4c4`** | la comprobación **50 sale VACÍA**: no puede leer el corpus anterior a la corrección del *mojibake*, y el actual ya no tiene el defecto que la Tabla 17 mide |
| `.setenv.sh` está en `.gitignore` | sin credenciales |

### El defecto: la puerta decía lo contrario de lo que hacía

El código de salida es correcto —`return 1 if (nuevos or vacias)`, y en el clon devolvía **1**—,
pero la línea explicativa se imprimía comprobando solo los fallos:

```
if fallos_totales and not nuevos:
    print('  (codigo de salida 0: no hay fallos nuevos...')
```

De modo que en el clon la salida terminaba con **«código de salida 0»** mientras el proceso
devolvía **1**. Quien lo lea concluye que pasó, y su integración continua acaba de fallar. Es un
defecto pequeño colocado en el peor sitio: la última línea que alguien lee para saber si puede
seguir.

**Arreglado**: la línea de «código de salida 0» solo se imprime cuando de verdad va a ser 0, y
cuando hay vacías se imprime otra que dice **por qué** corta —«una comprobación que examina cero
elementos no ha pasado, no se ha ejecutado»— y **cómo arreglarlo**: `git fetch --unshallow`.

**El remedio está comprobado, no supuesto.** Aplicado sobre el clon: 510 commits, `df9b4c4`
presente, **0 vacías**. Una instrucción de arreglo que nadie ha ejecutado no es un arreglo.

### Y un preparador, porque tres pasos que no están escritos son tres pasos que se olvidan

`tools/preparar_clon.sh` comprueba las tres, arregla las dos que se pueden arreglar —el
`hooksPath` y la historia— y dice en voz alta la que no, porque `.setenv.sh` no puede salir de
git. Después ejecuta el verificador y la auditoría para acreditar que el clon quedó operativo. No
instala nada ni adivina nada.

**Lo que esto dice del método.** El aparato de verificación estaba comprobado contra el documento,
contra los datos, contra sí mismo y contra sus propias declaraciones, y no contra **el entorno**.
Una comprobación que solo corre donde se escribió es la misma clase de defecto que una que solo
corre con el venv, y este proyecto ya rehízo Levene, el ANOVA, Friedman y `fuzz.ratio` en biblioteca
estándar por esa razón exacta.

**Estado del verificador:** 55 comprobaciones, 63 fallos (63 declarados, **0 nuevos**), 0 vacías en
esta copia; en un clon superficial, 1 vacía y salida 1 con su explicación.

---

## §F131 — Ensayo en seco de la adopción: dos bloqueos, una comprobación que reventaba y la lista de trabajo

**Fecha:** 2026-09-09 · **Origen:** preparar lo que va a pasar después, en lugar de esperarlo

La decisión 1 está respondida —adoptar el consolidado nuevo es seguro para la conclusión ([§F123](#f123))— pero
nadie había comprobado **qué haría el verificador el día de la adopción**. Apuntado en una copia de
trabajo al consolidado nuevo, sin comprometer nada: **10 comprobaciones fallan con 56 fallos
nuevos**, y una **reventaba**.

### La comprobación que reventaba, y era la del estadístico titular

`c_anova` calcula `math.log10(p)` para comparar el exponente publicado. Con el consolidado nuevo la
**p subdesborda a 0,0** en doble precisión —F = 119,7502 sobre df = (25, 2912)— y `log10(0.0)` lanza
`ValueError`. El envoltorio lo reportaba como VACÍA con su causa, que es su comportamiento diseñado,
pero **la comprobación que vigila el resultado principal del trabajo dejaba de comprobar nada**
exactamente el día en que más falta hace.

**Arreglado**, y con el remedio en el mensaje: cuando la p subdesborda, la comprobación lo dice y
añade que **el informe no puede publicar una cifra**, sino una cota del tipo «p < 10⁻³⁰⁰» declarando
que el valor exacto no es representable. Verificado que con el consolidado publicado nada cambia:
sigue en 5 elementos y «ok».

### Dos bloqueos del consolidado nuevo, ninguno visible hasta hoy

**1. Su manifiesto no es portable.** Las trece fuentes están escritas con **rutas absolutas a la
máquina del equipo de 48 GB**:

| Consolidado | Fuentes | Con ruta absoluta | Resolubles aquí |
|:---|---:|---:|---:|
| Publicado | 8 | **0** | **8** |
| Nuevo | 13 | **13** | **0** |

Todo lo que resuelve fuentes desde el manifiesto —el protocolo homogéneo, las cifras de la medición
restringida— falla con «no existe /Users/eahumada1/…». No es un problema de datos: los ficheros
están, con otro prefijo. Es un problema de que el manifiesto no se puede leer en ninguna máquina que
no sea la que lo escribió.

**2. No tiene `levene.json`.** El publicado sí. La comprobación del supuesto de homocedasticidad se
queda sin artefacto contra el que contrastar, lo que concuerda con que su `statistical_report.md` no
mencione Levene ([§F113](#f113)).

### La lista de trabajo, para que la decisión se tome con el precio delante

| Cifra publicada | Con el consolidado nuevo |
|:---|:---|
| F = 38,2222 | **119,7502** |
| p = 3,4453 × 10⁻¹⁶⁰ | **subdesborda**: hay que escribir una cota |
| χ² de Friedman = 1 169,23 | **1 802,3671** (y `friedman.json` hay que regenerarlo) |
| Tukey, 158 de 325 significativas | **217 de 325** |
| Dos modelos significativos | **uno** en tres categorías; **dos** en la restringida ([§F123](#f123)) |
| `nemotron-mini:4b` +14,52 pp | **+12,26 pp** |
| `llama3.2:latest` +10,82 pp | **+6,73 pp** |
| Levene p = 0,18 | 0,0000, y sin artefacto |
| Tabla 7, 26 medias de grupo | todas |
| La salvedad de §5.3.1 sobre 7 filas con latencia 0 | **deja de describir nada**: la campaña nueva no tiene ninguna |

Esa última fila es una buena noticia disfrazada de fallo: el defecto que §5.3.1 declaraba
desaparece, y con él la salvedad.

**Lo que esto añade a la decisión 1.** La respuesta sigue siendo que adoptar es seguro, pero ahora
está el precio: **diez comprobaciones y una decena de cifras titulares**, más dos arreglos que
corresponden al equipo de 48 GB —el manifiesto portable y el `levene.json`— y que **conviene pedir
antes** de decidir, porque sin ellos parte del informe no se puede verificar contra el consolidado
nuevo aunque se adopte.

### Mecanizado, porque habrá que repetirlo

El ensayo lo hice copiando el verificador a `tools/`, sustituyendo un nombre y borrando la copia:
frágil, irrepetible y sucio. Y **hay que volver a ejecutarlo** cuando el equipo arregle el manifiesto
y entregue el `levene.json`, porque la lista de trabajo cambiará. Ahora es
`tools/ensayo_adopcion.py`, que carga el verificador en memoria con las rutas del consolidado que se
le indique, lo ejecuta, y **compara sus resultados con los del actual**: la salida no es «pasa o
falla» sino la lista de trabajo. No escribe nada ni toca el verificador del repositorio.

Declara su limitación: la sustitución es **textual**, de modo que una comprobación que construyera
esa ruta de otra forma seguiría leyendo el consolidado viejo y **aparecería como que no cambia**. Por
eso imprime el recuento de sustituciones —hoy **8**—: el día que baje sin motivo, alguien ha cambiado
cómo se nombra el consolidado.

**Y emerge algo que no había visto al hacerlo a mano.** La comprobación 55, la que audita las
declaraciones, señala que la adopción dejaría **tres declaraciones caducadas**: la de `cita 62.67` y
la de «el Anexo I dice» —las dos de la decisión 13— y la de la telemetría ausente. Es decir, adoptar
**resuelve por sí solo tres de las pendencias declaradas**, y la herramienta lo dice sin que nadie
tenga que acordarse de comprobarlo.

**Estado del verificador:** 55 comprobaciones, 63 fallos (63 declarados, **0 nuevos**), 0 vacías.

---

## §F132 — Prueba de humo de las veintiuna herramientas: una sola falla, y por el motivo correcto

**Fecha:** 2026-09-09 · **Origen:** haber añadido seis herramientas en una sesión sin ejecutarlas todas

Una herramienta que revienta es peor que no tenerla, y `ast.parse` no lo detecta: un `NameError` o un
`import` que falta pasan la comprobación de sintaxis sin problema. Ejecutadas las **21** de `tools/`
más la de `.sh`:

| Comprobación | Resultado |
|:---|---:|
| Sintaxis (`ast.parse` y `sh -n`) | **22 de 22** correctas |
| Cargan y responden a `--help` | **20 de 21** |
| Ficheros rastreados a cero bytes | 2, los dos declarados |
| Residuo sin rastrear en el repositorio | **0** |

La que no carga es `generar_figuras_informe.py`, que necesita `matplotlib`. Y **es el motivo
correcto**, no un defecto: `matplotlib` está en el venv del proyecto —3.11.1— y no en el Python del
sistema, a propósito. Las otras veinte corren con el del sistema porque **una comprobación que solo
corre en un entorno no corre**, y este proyecto ya rehízo Levene, el ANOVA, Friedman y `fuzz.ratio`
en biblioteca estándar por esa razón. Esta **genera**, no comprueba, y por eso se le permite la
dependencia.

**Y no deja ninguna comprobación sin correr**, que era lo que había que verificar: el verificador
**lee su fuente como texto** para contrastar los rótulos de las figuras, y no la ejecuta.

**Lo que sí era un defecto es el mensaje.** Un `ModuleNotFoundError: No module named 'matplotlib'`
no le dice a nadie qué hacer. Sustituido por una guarda que da la orden exacta con el venv y explica
por qué esta herramienta es la excepción.

### Y una comprobación que importa para la decisión 19

Las figuras **regeneran idénticas byte a byte** hoy, comprobado con el venv sobre un directorio
aparte para no arriesgar las del entregable. No es un dato de archivo: la decisión 19 incluye
insertarlas, y ahora consta que se pueden regenerar y que lo que hay en `doc/figuras/` es
exactamente lo que produce la herramienta desde la Tabla 7 del Markdown.

**Estado del verificador:** 55 comprobaciones, 63 fallos (63 declarados, **0 nuevos**), 0 vacías.

---

## §F133 — La declaración que puse para el aviso de la comprobación 55 anuló su detección entera

**Fecha:** 2026-09-09 · **Origen:** la propia comprobación 55, un turno después de escribirla

[§F129](#f129) arregló que la comprobación 55 se silenciara a sí misma: su mensaje contenía la clave
literal, y se imprimió en adelante solo un **prefijo estricto**. Luego declaré el aviso legítimo
—la declaración de la referencia [37], que pertenece a `c_urls` y sin `--red` no tapa nada— con esta
clave:

> `'no tapa ningun fallo. Sin --red'`

Y esa cadena es un trozo de **la plantilla del mensaje**: «…no tapa ningún fallo. Sin `--red` puede
ser de `c_urls`…». De modo que la declaración casaba con **cualquier** aviso de huérfana, no solo con
el suyo, y **anulaba la detección completa de declaraciones caducadas**, presentes y futuras. Es
exactamente la «clave demasiado genérica» que la comprobación 55 existe para encontrar, y mi
declaración la dejó ciega para su propia categoría de fallo.

El síntoma que lo delató: la 55 reportaba «la declaración n.25 no tapa ningún fallo» **sobre la
declaración n.25**, que era la que acababa de añadir. Una declaración que se acusa a sí misma es la
señal de que su clave describe el mensaje y no el defecto.

**Arreglado sin declaración.** Una lista explícita, `SOLO_CON_RED`, enumera las claves cuya
comprobación solo corre con `--red`; la 55 las cuenta aparte y lo dice en su nota —«1 declaración de
`SOLO_CON_RED` no tapa nada sin red, y es legítimo»— en lugar de silenciarlas. **Cualquier otra
huérfana vuelve a ser un fallo.** Las declaraciones bajan de 26 a 25.

**Probado por mutación en los dos frentes**, los dos detectados y con el mensaje correcto:

| Mutación | Resultado |
|:---|:---|
| Una declaración caducada, con clave que no tapa nada | señalada: «no tapa ningún fallo y no está en `SOLO_CON_RED`» |
| Una clave genérica, `'no esta'` | señalada **por las dos ramas**: silencia tres comprobaciones **y** está anidada con la de la Tabla 20 |

**La lección, que es la que importa y ya va por la tercera vuelta.** El mecanismo de declaraciones
empareja **por texto del mensaje**, de modo que declarar un fallo cuyo mensaje describe *el mecanismo
mismo* es intrínsecamente peligroso: la clave deja de nombrar un defecto y pasa a nombrar una forma
de decirlo. Cuando lo que hay que declarar es un estado del **entorno** y no un defecto del
documento, la herramienta correcta es una lista enumerada en el código, no una declaración.

**Estado del verificador:** 55 comprobaciones, 61 fallos (61 declarados, **0 nuevos**), 0 vacías, 25
declaraciones.

---

## §F134 — `CLAUDE.md` afirmaba «4 fallos» cuando había veinticinco declaraciones

**Fecha:** 2026-09-09 · **Origen:** comprobar si el documento que todos los agentes leen se había
quedado desfasado

`CLAUDE.md` es el documento de norma del proyecto: lo lee toda sesión antes de trabajar. Y describía
el aparato con cifras copiadas que habían dejado de ser ciertas:

> «existen fallos **declarados**, cada uno con su motivo y con quien lo tiene —**dos ficheros de
> registro vacíos, el par de cifras de la conclusión 1 y la referencia al repositorio privado**—.
> […] El resumen los cuenta aparte: «**4 fallos (4 declarados, 0 nuevos)**»»

Hoy son **61 fallos y 25 declaraciones**, y la enumeración de cuáles se quedó en las cuatro
primeras. Y en la sección de ramas que escribí ayer: «el verificador y **sus 55 comprobaciones**»,
cierto el día que lo escribí y falso al siguiente, porque ese mismo día añadí una.

Es [§L69](#l69) en el sitio de mayor alcance: quien lea `CLAUDE.md` y no ejecute la herramienta se
queda con una cifra vieja y con una lista de declaraciones que ya no describe nada.

**La regla, que es lo que queda escrito.** Un recuento que una herramienta reporta **no se copia a
un documento de norma**; se ejecuta la herramienta. `CLAUDE.md` dice ahora «N fallos (N declarados,
0 nuevos)» sin N, apunta a `FALLOS_DECLARADOS` para el detalle, y explica por qué no enumera:
**esta misma frase enumeraba cuatro cuando ya había veinticinco**.

**La excepción, y no es una laguna.** Esto **no alcanza a los registros fechados** —el §6 de
`CURRENT-TASKS.md`, los `WORKLOG`, este propio `FINDINGS`—, donde una cifra consigna lo que era
cierto entonces y por eso **no se actualiza**: a un registro se le añade, no se le edita. Comprobado
que la única mención que quedaba en `CURRENT-TASKS.md` es una fila del registro, y se deja.

**Predicado 14 de la auditoría de afirmaciones**, que caza la clase en lugar del caso: los
documentos de norma no pueden contener «N comprobaciones», «N fallos (N declarados…», «N
declaraciones» ni «sus N comprobaciones». Probado por mutación: devuelta a `CLAUDE.md` una frase con
los dos recuentos, la auditoría pasa de código 0 a 1 y señala el recuento con su contexto.

### Y la cuarta vez que el ensayo era el defecto, que ya es un patrón

La primera tentativa de esa mutación **no imprimió nada**, y no porque el predicado fallara: mi
`grep` buscaba «recuentos de las herramientas» y la salida **trunca la descripción a 52
caracteres**, de modo que el patrón no casaba con nada. Repetida mirando el **código de salida**,
funciona.

Van cuatro en la misma sesión, y las cuatro con la misma forma: mutaciones que buscaban una cifra
**en negrita** cuando el informe la escribe sin resalte ([§F117](#f117)); una que omitía los
asteriscos y el `>` de una cita en bloque ([§F120](#f120)); una que apuntaba a un espejo que **ya se
había separado de `main`**, de modo que la premisa había desaparecido; y esta.

**La regla que sale de las cuatro:** un ensayo se juzga por el **código de salida o por el recuento
de fallos**, no por si un `grep` encuentra una cadena en la salida. Un `grep` que no casa se parece
demasiado a una comprobación que no detecta, y confundirlos hace dar por validada una comprobación
vacua — que es exactamente lo que este proyecto lleva toda la revisión intentando no hacer.

**Auditoría de afirmaciones:** 14 predicados, 0 que no se cumplen.

---

## §F135 — El documento de decisiones decía «siete» cuando tenía diecinueve, y el que enseña a detectarlo lo repetía

**Fecha:** 2026-09-09 · **Origen:** el protocolo de seguimiento apunta a `TODO-INFORME-FINAL.md §10`
para las decisiones pendientes, y nadie había comprobado que esa sección estuviera al día

Dos cifras desfasadas, y la peor está en la fuente:

| Documento | Decía | Es |
|:---|---:|---:|
| `DECISIONES-PENDIENTES-20260908.md`, su propio encabezado | «Son **siete**» | **19** |
| `TODO-INFORME-FINAL.md §10`, la revisión del 2026-09-08 | «las **siete** decisiones del autor» | **19** |

La segunda importa más de lo que parece: **el protocolo de seguimiento manda mirar ahí**, de modo que
cada informe de avance que he entregado señalaba una lista de siete cuando había diecinueve, y entre
las doce que faltaban está la **19**, que es la más urgente de todas.

**Y `TODO-INFORME-FINAL.md` contiene, dos párrafos más abajo, la lección sobre este defecto exacto**
y la orden que lo detecta:

```sh
git log $(git log -1 --format=%H -- <documento>)..HEAD -- <ruta-que-describe>
```

Aplicada hoy a los documentos de estado: `CURRENT-TASKS.md` **2** commits por detrás,
`TODO-INFORME-FINAL.md` **8**, `ESTADO-RECORRIDA` **5**, `DECISIONES-PENDIENTES` **0**. El documento
que enseña a medir el desfase era el más desfasado de los cuatro.

**Corregido, y de dos formas distintas según lo que sea el número.** En
`DECISIONES-PENDIENTES-20260908.md` el recuento **es** contenido del documento, así que se declara
—19, con el desglose de que 3 llevan estado en el título y **16 siguen abiertas**— y se ata: el
**predicado 15** de la auditoría comprueba que el número declarado coincide con los encabezados
`## N.` que hay debajo y que la numeración es contigua desde 1. En `TODO-INFORME-FINAL.md` el número
era una **copia**, así que se retira y se apunta al documento que lo lleva al día, por la regla de
[§F134](#f134).

**Y el predicado dice qué hacer si no cuadra**, porque es la parte que se puede equivocar:
**corregir el encabezado, no borrar decisiones**. La política del proyecto es aditiva y ya hubo un
incidente —el de la Tabla 2 que `CLAUDE.md` narra— en que un conteo que no cuadraba estuvo a punto de
resolverse borrando datos.

**De paso, actualizada la entrada de la propagación al `.docx`**, que decía que la lista completa de
lo que falta está en un documento de 2026-09-08. Ya no depende de que nadie recuerde esa lista: las
comprobaciones **51 a 54** comparan prosa, tablas, bibliografía, encabezados y figuras entre la
fuente y los tres entregables, de modo que **el inventario lo produce la herramienta** y cualquier
divergencia nueva corta el commit.

**Auditoría de afirmaciones:** 15 predicados, 0 que no se cumplen.

---

## §F136 — La biblioteca de prompts mandaba hacer a mano lo que ya hace una herramienta

**Fecha:** 2026-09-09 · **Origen:** la petición de revisar el trabajo «según los prompts documentados
en `doc/prompts`»

Los nueve documentos de `doc/prompts` llevan entre **133 y 178 commits** de retraso respecto del
código y los datos que describen. El retraso por sí solo no prueba nada —un procedimiento puede
seguir siendo válido—, así que lo que hay que buscar es otra cosa: **si algún prompt manda hacer a
mano lo que ahora hace una herramienta**. Dos lo hacían.

**`05-entregables.md`** pedía «enumerar en el encargo **qué ha cambiado** desde la última
propagación, porque quien maqueta no puede adivinarlo», y narraba la detección del peor fallo de la
revisión como una hazaña: «dos auditores lo detectaron extrayendo el XML por separado». Hoy las
comprobaciones **51 a 54** comparan prosa, tablas, bibliografía, encabezados y figuras entre la
fuente y los tres `.docx` en menos de dos segundos, y cortan el commit ante cualquier divergencia
nueva. El encargo de maquetación se escribe **pegando la salida del verificador**, no reconstruyendo
la lista — y una enumeración a mano se queda incompleta sin que nadie se entere, que es precisamente
lo que pasó con `PROPAGACION-PENDIENTE-DOCX-20260908.md` y su adenda.

**`00-revision-completa.md`** decía «**cubre diez comprobaciones**» y las enumeraba. Hay 55. Es
[§F134](#f134) en un documento de procedimiento, y ahí duele más que en uno de norma: **un
procedimiento que declara de menos manda hacer menos**. Quien lo pegue en una sesión nueva creerá
que el aparato cubre diez cosas y verificará a mano las otras cuarenta y cinco, o no las verificará.

**Corregido de forma aditiva**, sin retirar nada: el recuento y su lista se sustituyen por las
**familias** que cubre —que no envejecen— y por la instrucción de que la cifra la dice el script al
ejecutarse. Añadidas las cuatro herramientas que estos prompts daban por inexistentes
(`auditar_afirmaciones`, `cobertura_cifras`, `estado_ramas`, `ensayo_adopcion`), la puerta de commit
y `preparar_clon.sh`. Y en el `README` una tabla de herramientas, porque un prompt que describe una
comprobación en prosa y no dice que existe implementada hace trabajar dos veces.

**Predicado 14 extendido a `doc/prompts`.** Estaba limitado a los documentos de norma —`CLAUDE.md` y
el encargo— y los de procedimiento quedaban fuera. Probado por mutación: devuelto «cubre 10
comprobaciones» a un prompt, la auditoría pasa de código 0 a 1.

**Auditoría de afirmaciones:** 15 predicados, 0 que no se cumplen.

---

## §F137 — El dictamen del equipo verifica, y la métrica restringida da 4 de 13 con dos medianas a cero

**Fecha:** 2026-09-09 · **Origen:** verificar el dictamen estadístico del equipo de 48 GB antes de
aceptar sus cifras

El equipo entregó `remote_48g/DICTAMEN-PRUEBA-ESTADISTICA-20260909.md`, y su conclusión de fondo es
que **el defecto atacable no es la heterocedasticidad sino el diseño pareado ignorado**: el ANOVA de
una vía sobre 26 celdas trata como independientes registros pareados por artículo y **confunde el
efecto MODELO con el efecto MODO**, de modo que su F = 119,75 no aísla el efecto del RAG, que es la
pregunta del estudio. Recomiendan Wilcoxon pareado por modelo con corrección de Holm como titular,
un modelo mixto de dos vías con la interacción MODELO × MODO como omnibus de encuadre, y conservar el
ANOVA como descriptivo.

**Verifica.** Recalculado **sin usar su herramienta**, con `scipy` y `statsmodels`, y por **dos vías
independientes** —la columna `f1` del CSV y la reagregación desde `per_type`—: los trece p, las trece
medianas y los trece valores de Holm coinciden con su tabla a la precisión impresa, por los dos
caminos. **3 de 13 significativos** en la métrica de tres categorías. El único desacuerdo es de
cuarto decimal en un p crudo y no mueve nada.

**Y el análisis de fondo lo había confirmado por mi cuenta antes de leerlo**, al preparar el contexto
de otro encargo: la intersección de identificadores de artículo entre los 26 grupos es completa, de
modo que el diseño es de medidas repetidas totalmente cruzado. Que dos equipos lleguen a lo mismo por
separado es la mejor señal disponible.

### La pieza que ellos declaraban pendiente: 4 de 13, no 3

Calculada la métrica restringida a las dos categorías que el corpus anota: **4 de 13**, y el que
entra es `llama3.1:8b`. Con dos consecuencias:

**Primera, y favorece al trabajo aunque menos de lo que escribí primero:** `mistral-nemo:latest`
pasa de p cruda 0,0058 —el que más cerca quedaba de entrar— a **0,111**, y su **mediana** de −0,0206
a +0,0000. **Corrección del mismo día:** escribí que «pierde el signo negativo», y eso vale para la
mediana y no para el resto. Su **media sigue en −0,0272** y **46 artículos empeoran frente a 36 que
mejoran**. Lo correcto es que el efecto adverso **deja de ser significativo**, no que deje de
existir. Lo vi al mecanizar el cálculo y ver el reparto completo, que a mano no había mirado: es el
mismo argumento por el que hay que dar tres cifras y no una, aplicado contra mi propia frase.

**Segunda, y es una advertencia:** **dos de los cuatro significativos tienen mediana exactamente
+0,0000.** El equipo ya avisaba de que `gemma4:12b-mlx` era significativo con una mediana de 1 pp; en
la restringida el problema es peor. Y no significa «sin efecto»:

| Modelo | pares con Δ ≠ 0 | mejoran | empeoran | mediana | **media** |
|:---|--:|--:|--:|--:|--:|
| `nemotron-mini:4b` | 99 de 113 | 74 | 25 | +0,1757 | +0,1441 |
| `llama3.2:latest` | 91 de 113 | 64 | 27 | +0,0442 | +0,1111 |
| `gemma4:12b-mlx` | 72 de 113 | 52 | 20 | **+0,0000** | +0,0255 |
| `llama3.1:8b` | 88 de 113 | 55 | 33 | **+0,0000** | +0,0408 |

Wilcoxon detecta **consistencia de signo** entre las diferencias no nulas, y con 52 mejoras frente a
20 empeoramientos la significación es real. Lo que engaña es **la mediana como tamaño de efecto**
cuando más de un tercio de los pares vale cero: el efecto existe y vive en una minoría de artículos.

**La petición que se les traslada:** al reportar tamaños de efecto, **tres cifras y no una** —mediana,
media y recuento de pares no nulos con su reparto mejora/empeora—. Con solo la mediana, dos de los
cuatro modelos significativos parecen no tener efecto.

### Lo que queda para el autor, y es nuevo

**Cuál de los dos recuentos es «el N de 13» del informe: 3 o 4.** Las dos cifras son correctas sobre
métricas distintas y el informe ya publica las dos mediciones, de modo que no es una cuestión
técnica sino de qué se enuncia como resultado, y con qué matiz de relevancia práctica.

**Nada de esto se ha incorporado al informe.** `CSV_CONSOLIDADO` sigue apuntando al consolidado
publicado y la cifra titular sigue siendo F = 38,2222.

---

## §F138 — Sí, el test de Wald es factible: 47 216 eventos de clasificación. Pero mide recall, no F1

**Fecha:** 2026-09-09 · **Origen:** la pregunta del autor de si «al ser un problema de clasificación
y no de regresión, R² o un test de Wald no serían mejores»

Tres respuestas, y la tercera es la que decide.

### R² (η²) no es una alternativa: es un tamaño de efecto, no una prueba

No sustituye al contraste, lo acompaña, y **está ya calculado**: η² = **0,2360** en el consolidado
publicado y **0,5069** en el nuevo. Lo que sí es cierto es que el informe **no lo publica**, y las
guías de reporte estadístico lo piden junto al valor p. Eso es una mejora real del informe, pero no
resuelve qué prueba sostiene la conclusión.

### La heterocedasticidad sí aplica al ANOVA, aunque el problema sea de clasificación

La intuición del autor llega a la conclusión correcta por un camino que no se sostiene en una
defensa. **Que la tarea sea de clasificación no exime al ANOVA de sus supuestos**: ese ANOVA se
calcula sobre una respuesta continua —el F1 por artículo, en [0, 1]—, y a esa respuesta se le
aplican los supuestos del modelo, con independencia de cómo se haya obtenido.

Los motivos por los que la heterocedasticidad **no manda** aquí son otros, y son los que el equipo de
48 GB documentó y este equipo verificó: el diseño está **balanceado** —n idéntico en los 26 grupos—,
lo que hace robusto el F de Fisher; con N = 2 938 Levene es **sobre-potente**; y el defecto de fondo
es otro, el **diseño pareado ignorado**. Ver [§F137](#f137).

Conviene decirlo así en la defensa. «No aplica porque es clasificación» es rebatible en una frase;
«no manda porque el diseño está balanceado, la prueba está sobre-potenciada con este N, y el defecto
real es el emparejamiento» no lo es.

### El test de Wald es factible, y con un n enorme

Un test de Wald vive dentro de un **modelo**, y el modelo natural para un problema de clasificación
es una **regresión logística de efectos mixtos** sobre el resultado binario de cada evento —cada
entidad de referencia acertada o no—, con el artículo como efecto aleatorio, MODELO y MODO como
fijos, y el Wald sobre la **interacción MODELO × MODO**, que es literalmente «el RAG ayuda en unos
modelos y no en otros».

**El dato lo soporta.** `metrics.per_entity` existe en los `detailed_results.json`, con el veredicto
`tp`/`fp`/`fn`, la cadena extraída y la de referencia, entidad por entidad. Medido sobre las trece
corridas nuevas, excluidos los siete contaminados:

| | |
|:---|---:|
| Registros con `per_entity` | **2 938 de 2 938** |
| Eventos de clasificación en total | **56 496** |
| De ellos: `tp` / `fn` / `fp` | 28 611 / 18 605 / 9 280 |
| **Eventos con entidad de referencia (`tp` + `fn`)** | **47 216** |
| Por grupo | **1 816, idéntico en los 26** |

Ese «1 816 idéntico en los 26» es un dato en sí mismo: el diseño está **balanceado también a nivel de
entidad**, que es precisamente lo que hace robusto al F y lo que sostiene el argumento de §F137.

### Y la salvedad que decide: modela **recall**, no F1

Los `fp` **no tienen entidad de referencia**. No son «una referencia acertada o no» sino una
extracción espuria, de modo que no entran en un modelo cuyo evento es «esta referencia se acertó».
Un solo modelo logístico sobre los 47 216 eventos con referencia **modela la exhaustividad**, no el
F1: la precisión vive en los 9 280 `fp`, con otro denominador.

Eso tiene dos caras y hay que declarar las dos:

- **A favor:** es **estadísticamente más limpio** que un ANOVA sobre un cociente agregado por
  artículo. Modela los eventos de clasificación reales, con su binomialidad, su efecto de artículo y
  su interacción, y el test de Wald sobre la interacción responde exactamente la pregunta del
  estudio.
- **En contra:** **responde una pregunta más estrecha**. El informe publica F1 y sus conclusiones
  están enunciadas en F1. Sustituirlo por un modelo de recall cambia la magnitud medida, no solo la
  prueba, y exigiría reenunciar los resultados o mantener dos aparatos en paralelo.

**Recomendación, y es del autor decidir.** Es una **mejora deseable, no imprescindible para
aprobar**, y llega tarde para el calendario: exigiría reenunciar el capítulo de resultados en
términos de exhaustividad. El camino corto y defendible sigue siendo el de §F137 —contraste pareado
por modelo, que es lo que el diseño pide— **más publicar el η² que ya está calculado**, que sí es
barato. El modelo logístico con Wald es el candidato natural a **trabajo futuro**, y ahora consta que
el dato lo permite: 47 216 eventos, balanceados, ya en el repositorio.

---

## §F139 — Sí hay una variante de F1 que sostiene mejor los resultados: micro con bootstrap pareado

**Fecha:** 2026-09-09 · **Origen:** la pregunta del autor de si alguna variación de F1 sostendría
mejor los resultados

**Sí, y es la mejor noticia estadística de la revisión.** Dos cambios, los dos baratos, y ninguno
exige reenunciar el capítulo ni volver a inferir.

### Cambio 1 — micro-F1 en lugar de macro por artículo

El informe promedia el **F1 de cada artículo**, de modo que un artículo con dos entidades de
referencia pesa lo mismo que uno con cuarenta. **Micro-F1** agrupa los `tp`/`fp`/`fn` de los 113
artículos y calcula el F1 una vez: pondera por **entidad**, que es lo que se está midiendo.

No es una elección de conveniencia sino de unidad de medida, y cambia el cuadro donde el promedio
por artículo estaba escondiendo efectos. El caso más claro:

| Modelo | Δ macro por artículo | **Δ micro** |
|:---|---:|---:|
| `gemma:latest`, tres categorías | **+0,0003** | **+0,0278** |
| `nemotron-mini:4b` | +0,1226 | +0,1526 |
| `mistral-nemo:latest` | −0,0429 | −0,0301 |

`gemma:latest` pasaba por «efecto nulo» con un +0,0003 que es ruido, y con micro tiene +2,8 pp. El
promedio por artículo lo diluía porque los artículos cortos, con una o dos entidades, dominaban la
media.

### Cambio 2 — bootstrap pareado en lugar de un test paramétrico

Remuestrear los 113 artículos con reemplazo, recalcular el F1 de los dos modos **sobre la misma
remuestra** y mirar la distribución de la diferencia. Es el procedimiento estándar en PLN —Dror et
al., *The Hitchhiker's Guide to Testing Statistical Significance in NLP*, ACL 2018— y resuelve de una
vez las cuatro objeciones que este trabajo arrastra:

1. **Prueba la métrica que el informe publica**, el F1, no un sustituto como la exhaustividad. A
   diferencia del modelo logístico con Wald de [§F138](#f138), no obliga a reenunciar nada.
2. **Respeta el emparejamiento**: remuestrea artículos, que es la unidad pareada, y evalúa los dos
   modos sobre los mismos.
3. **No supone nada sobre la distribución.** La cuestión de la homocedasticidad **desaparece**, no se
   argumenta: no hay supuesto que comprobar.
4. **Da intervalo de confianza sobre el Δ F1**, que es el tamaño de efecto con incertidumbre que las
   guías de reporte piden y que el informe hoy no da.

### Los resultados, con Holm sobre los 13 contrastes

| Métrica | Significativos | Cuáles |
|:---|---:|:---|
| Tres categorías | **5 de 13** | `nemotron-mini:4b`, `llama3.2:latest`, `gemma4:12b-mlx`, `gpt-oss:20b`, `gemma4:latest` |
| Restringida | **6 de 13** | los cinco anteriores menos `gpt-oss:20b`, más `llama3.1:8b` y `gemma:latest` |

Con sus intervalos, que es lo que se publica. Los dos más fuertes, en la restringida:
`nemotron-mini:4b` **+0,1842 [+0,1351, +0,2316]** y `llama3.2:latest` **+0,1209 [+0,0701, +0,1769]**.

Para comparar, y hay que declarar las cuatro:

| Procedimiento | Tres categorías | Restringida |
|:---|---:|---:|
| Tukey sobre 325 celdas, lo que publica el informe | 2 | — |
| Wilcoxon pareado + Holm | 3 | 4 |
| **micro-F1 + bootstrap pareado + Holm** | **5** | **6** |

### La objeción que esto se come, y la que abre

**Se come la principal:** ya no hay que discutir supuestos. Un bootstrap no los tiene.

**Abre una, y hay que anticiparla:** el recuento **sube** de 2 a 5 o 6, y un tribunal puede leer eso
como haber buscado el procedimiento que da más. La única defensa que funciona es la que el equipo de
48 GB ya propuso y este equipo suscribió: **fijar la regla de decisión a priori por principio** —el
diseño es pareado, luego el contraste es pareado; la unidad medida es la entidad, luego la
agregación es micro— **antes de mirar los valores p**, y **declarar los cuatro recuentos** con su
procedimiento. Publicar solo el 6 sería indistinguible de seleccionar el resultado.

Conviene además decir lo que **no** cambia: `mistral-nemo:latest` sigue con signo adverso en las dos
métricas —−0,0301 y −0,0245— y **no** alcanza significación en ninguna; y `qwen3:8b`,
`gemma4:31b-cloud` y `deepseek-r1:1.5b` siguen sin efecto. **La conclusión del trabajo no solo se
sostiene: se sostiene con más soporte y con intervalos.**

### Recomendación

**Adoptar los dos cambios es la mejor relación entre coste y solidez de todo lo revisado.** No exige
volver a inferir, no cambia la magnitud publicada, elimina la discusión de supuestos, añade
intervalos y **aumenta** el soporte de la conclusión. Es reproducible desde los `per_type` que ya
están en el repositorio.

Lo que cuesta: recalcular las cifras del capítulo de resultados en micro, y una redacción honesta de
la regla de decisión y de los cuatro recuentos. Es trabajo de una tarde, no de una semana, y hay que
decidirlo junto con la **decisión 1** —qué consolidado— porque las cifras dependen de ella.

---

## §F140 — Las «23,0 páginas» eran del Markdown, no del entregable, y eso afloja la decisión 19

**Fecha:** 2026-09-09 · **Origen:** la puerta de factibilidad del workflow de propagación

Toda la sesión he tratado el «23,0 de 25» como el recuento de páginas del **entregable**, y con esa
cifra advertí repetidamente de que insertar 1 500 palabras podía no caber. La puerta de factibilidad
del workflow lo puso en duda y **tenía razón**.

**La comprobación del límite estima sobre el Markdown, no sobre el `.docx`.** Verificado leyendo
`c_extension`: llama a `texto()`, que devuelve el Markdown canónico, y estima con
`PAGINAS_ENTREGADO + (cuerpo − CUERPO_ENTREGADO) / DENSIDAD`, anclada a **14 842 palabras igual a 20
páginas contadas sobre el PDF entregado al profesor guía**. Es una estimación honesta y bien
anclada — de lo que ocuparía **el Markdown**.

**Y el `.docx` es más corto que el Markdown precisamente porque le falta este contenido.** Es obvio
en cuanto se dice: al entregable le faltan diez párrafos, una tabla, una referencia y dos figuras
([§F127](#f127)), de modo que **no puede tener las mismas páginas que la fuente**.

| | Palabras de cuerpo | Páginas |
|:---|---:|---:|
| PDF entregado, el ancla medida | 14 842 | **20** |
| Markdown de hoy | 16 753 | **≈22,8** |
| `.docx` de hoy, al que le falta el contenido | por debajo | por debajo |

**Insertar lo que falta lleva el entregable hacia esas ≈23 páginas, no por encima de 25.** El
límite de 25 páginas **deja de ser el motivo** para no hacer la decisión 19.

La puerta refinó más —≈21,2 páginas con las seis piezas, porque de las 1 547 palabras solo unas 485
caen en el cuerpo y el resto en los **anexos**, que el límite excluye—, y **esa segunda cifra no la
he verificado por mi cuenta**: lo digo porque la diferencia entre lo comprobado y lo aceptado
importa. La conclusión operativa no depende de ella.

**Qué se corrige.** El encargo a Claude Desktop decía «el verificador lo estima hoy en 23,0» junto a
la instrucción de parar si no cabía, y la decisión 19 decía «con 23,0 usadas» como argumento para no
hacerla. Los dos corregidos, con la aritmética y con lo que no verifiqué marcado como tal.

**Y una comprobación fallida propia, que dejo escrita.** Intenté verificar el recuento del `.docx`
contando palabras hasta la palabra «Anexos» en su texto extraído, y me dio **497**. No es que el
`.docx` tenga 497 palabras de cuerpo: es que «Anexos» aparece antes **en el índice de contenidos**,
de modo que mi ancla cortaba en el sitio equivocado. Mi comprobación quedó **inconcluyente, no
contradictoria**, y decirlo así es distinto de decir que verifiqué la cifra. Es la misma lección de
las cuatro mutaciones fallidas: **un ensayo mal armado no refuta ni confirma**.

**La lección general, que es la que vale.** Una cifra correcta sobre el artefacto equivocado hace más
daño que una cifra mal calculada, porque no hay nada que detecte el error: los 23,05 son exactos para
lo que miden. La pregunta que faltaba no era «¿está bien calculado?» sino **«¿de qué artefacto habla?»**.
Y la respuesta cambió una decisión: de «probablemente no cabe» a «cabe con margen».

---

## §F141 — A la Tabla 9 no le faltan tres filas: el entregable usa otra convención

**Fecha:** 2026-09-09 · **Origen:** la puerta de factibilidad lo señaló y se verificó celda por celda

La comprobación 52 declara «Tabla 9 tiene 42 filas y el Markdown 45», y yo lo he trasladado tres
veces como «tres filas que faltan». **No es eso.**

| | Primera columna, filas 3 a 6 |
|:---|:---|
| Markdown | `src/main.py`, `src/config.py`, `src/data_loader.py`, `src/llm_runner.py` |
| `.docx` | `····main.py`, `····config.py`, `····data_loader.py`, `····llm_runner.py` (cuatro espacios duros) |

El `.docx` presenta la estructura del repositorio como un **árbol indentado**; el Markdown, como
**rutas completas**. Son dos convenciones de presentación, y **el mapeo entre sus filas no es uno a
uno**. Pegar tres filas con ruta completa en el `.docx` **rompería su convención**, que además se lee
mejor para un tribunal.

**Lo que la comprobación detectó es real; su encuadre no lo era.** La 52 compara recuentos y, al no
cuadrar, se detiene antes de comparar contenido — de modo que informó de la diferencia de filas y no
de la de convención, que es la que manda. Es la regla del proyecto una vez más: **un hallazgo de
auditoría es una hipótesis**, y su formulación puede estar mal aunque la detección esté bien.

**Corregido** en el encargo a Claude Desktop, que decía «tres filas» y ahora dice qué hacer: averiguar
qué tres rutas no tienen hoja en el árbol y añadirlas **en la convención del `.docx`**, o **declarar
la divergencia como deliberada** — que es una opción legítima y probablemente la buena, porque el
árbol indentado es mejor presentación que la lista de rutas.

**Y un segundo hecho del mismo análisis, que evita una decisión equivocada:** el `.docx` con plantilla
**no usa `heading4`**. De modo que insertar el encabezado de la subsección que falta no es un problema
de herramienta: **el nivel y su numeración son una decisión editorial**, porque la jerarquía de la
plantilla no tiene ese nivel en uso. Lo he pasado a Desktop como decisión a tomar, no como tarea
mecánica.

**Reparto verificado de las seis piezas.** La puerta dictaminó «proceder con las viables», y son solo
**dos**: la celda de la Tabla 3 y las dos citas de [38] en el texto, las dos con anclas únicas. Las
otras cuatro exigen insertar `<w:p>`, tablas, imágenes con sus relaciones y una declaración
`Default Extension="png"` en `[Content_Types].xml`, y ninguna herramienta de `tools/` lo hace. Van a
Word, y el encargo lo dice pieza por pieza con el motivo.

---

## §F142 — Mi `git add -A` barrió los cambios en vuelo de un workflow, y el commit miente por omisión

**Fecha:** 2026-09-09 · **Origen:** comprobar si el workflow de propagación había escrito

El workflow de propagación aplicó sus inserciones a los tres `.docx` entre las 13:38:40 y las
13:39:04. Mi commit `7646147`, hecho a las 13:38 y titulado **«docs(LEARNING): siete lecciones de la
sesión, §L71 a §L77»**, lleva dentro:

```
 Informe_Final_Tesina_NER.docx                      | Bin 68597 -> 68685 bytes
 ...na_NER_plantilla_revision_final_2026-09-03.docx | Bin 222720 -> 222807 bytes
 .../2026-07-04_Borrador-Informe-Final-Tesina.docx  | Bin 68779 -> 68896 bytes
```

**Tres entregables modificados en un commit que dice ser sobre lecciones.** Los barrió `git add -A`
sin que yo los revisara, y está empujado.

**El contenido está bien**, verificado antes de escribir esto: los tres tienen **XML sano**, **38
entradas de bibliografía de [1] a [38]**, las dos citas de [38] en el texto, `FollowTheMoney` y la
celda de la Tabla 3 corregida; el número de partes del paquete no cambió y el recuento de palabras
sube en lo que cabe esperar de una entrada más. **No se perdió nada.** Lo que está mal es **el
registro**: el mensaje del commit no describe lo que el commit contiene.

**Se corrige de forma aditiva**, que es la política del proyecto: no se reescribe la historia —está
empujada, y las reglas del proyecto sobre `--force` exigen respaldo en `bundle`, comprobación de
refs y avisar de que los clones quedan incompatibles, que es desproporcionado para un mensaje
inexacto—. Queda este hallazgo, y la entrada del registro de coordinación, diciendo qué contiene de
verdad `7646147`.

### Y dos defectos de método que sí hay que arreglar

**Primero: `git add -A` mientras un workflow escribe es un error.** Un workflow que aplica cambios a
ficheros del repositorio y un `git add -A` en paralelo se pisan por construcción. **Lo correcto es
añadir por ruta** —`git add FINDINGS.md CURRENT-TASKS.md`— cuando hay agentes escribiendo, y dejar
que sus cambios se comprometan aparte, revisados. Lo he hecho con `-A` toda la sesión sin
consecuencia porque nada más escribía; en cuanto algo escribió, ocurrió esto.

**Segundo, y es peor: la puerta de commit pasó sobre un estado que ya no existía.** El gancho ejecutó
el verificador a las 13:38 y dijo «sin fallos nuevos», y era cierto **en ese instante**. Segundos
después el workflow terminó de aplicar y aparecieron dos fallos nuevos —dos declaraciones que habían
quedado **caducadas** porque su defecto se arregló—. La puerta no falló: **midió un estado que estaba
cambiando**. Es el mismo defecto de `§L72` en otra forma: la comprobación era correcta para lo que
midió, y lo que midió ya no era el repositorio.

**Los dos fallos nuevos eran buenas noticias**, y conviene subrayarlo porque la comprobación 55 hizo
exactamente su trabajo: avisó de que `Tabla 3, fila 1 difiere` y `le faltan las entradas de
bibliografia [38]` ya no tapaban nada, o sea que **el defecto que declaraban estaba resuelto**.
Retiradas las dos; las declaraciones bajan de 25 a 23 y los fallos de 61 a **55**.

**La regla que sale:** cuando un agente o un workflow tiene permiso de escritura sobre el
repositorio, **no se comparte el índice de git con él**. Se añade por ruta, y se comprueba el estado
**después** de que termine, no mientras corre.

---

## §F143 — El dictamen del comité, verificado: «ocho de trece» sobre los datos publicados, y la correlación que no replica

**Fecha:** 2026-09-09 · **Origen:** el workflow del comité revisor cerró y sus dos afirmaciones más
graves se comprobaron por cuenta propia antes de aceptarlas

El comité —lente estadística, metodólogo de aprendizaje automático y presidente de tribunal, con
investigación web previa— devolvió tres veredictos: «entregable con cambios, pero uno no es menor»,
«no entregable como está» y un doble veredicto que distingue el Markdown del entregable. Sus dos
afirmaciones de fondo **se verifican**, y hay que decir cuál es cuál porque **empujan en direcciones
opuestas**.

### Primera, y refuerza el trabajo: ocho de trece, no dos

Sobre el consolidado **publicado** —el que el informe usa—, el contraste que corresponde al diseño
pareado da **ocho de trece** modelos significativos tras Holm, no dos:

| Modelo | Δ | p cruda | p Holm |
|:---|---:|---:|---:|
| `nemotron-mini:4b` | +14,52 pp | 4,07e-10 | 0,0000 |
| `llama3.2:latest` | +10,82 pp | 1,15e-08 | 0,0000 |
| `qwen2.5:14b` | +4,62 pp | 1,36e-05 | 0,0001 |
| `gemma:latest` | +7,36 pp | 4,90e-05 | 0,0005 |
| `qwen3:8b` | +3,25 pp | 8,13e-05 | 0,0007 |
| `gpt-oss:20b` | +3,28 pp | 5,55e-04 | 0,0044 |
| `gemma4:12b-mlx` | +2,28 pp | 2,63e-03 | 0,0184 |
| `llama3.1:8b` | +1,99 pp | 7,19e-03 | 0,0432 |

Recalculado por mi cuenta con `scipy` y `statsmodels`: reproduce **exacto**
`results/ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json`, que lo tiene calculado desde el
**8 de septiembre** y declara `significativos_pareado: 8` frente a `significativos_tukey_publicado:
2`. Y [§F76](#f76) lo documenta desde esa fecha con el título «Con el contraste apropiado al diseño,
ocho de trece modelos mejoran, no dos». **El informe no lo declara.**

**Y aclara una contradicción aparente con mis propios cálculos de hoy.** Yo obtuve **3 de 13**, y no
había error en ninguno de los dos: mi cálculo era sobre el consolidado **nuevo** (N=113) y este es
sobre el **publicado** (N=120). Son datos distintos, y el del comité es **el más relevante para el
informe de hoy**, porque es el que el informe publica. El cuadro completo:

| Datos y procedimiento | Significativos |
|:---|---:|
| Publicado, Tukey sobre 325 celdas — **lo que el informe dice** | 2 |
| **Publicado, Wilcoxon pareado + Holm** | **8** |
| Nuevo, Wilcoxon pareado + Holm | 3 |
| Nuevo, restringida, Wilcoxon + Holm | 4 |
| Nuevo, micro-F1 + bootstrap pareado + Holm | 5 |
| Nuevo, restringida, micro + bootstrap + Holm | 6 |

**Y el agravante que aporta el comité es de lógica, no de estadística, y es el mejor argumento de
todo su informe.** §5.3.1 declara que tratar como independientes unas observaciones apareadas «hace
el contraste conservador» —es decir, **declara la dirección del sesgo**— y a continuación publica
como resultado «solo dos de los trece», que es **precisamente lo que ese sesgo produce**. No se
puede sostener a la vez que la elección es inocua y que su efecto es el hallazgo.

### Segunda, y debilita el trabajo: la correlación no replica

El informe publica que «correlacionando el F1 base de cada modelo con la mejora que le aporta la
recuperación se obtiene un coeficiente de **Spearman de −0,5165** (p = 0,0707) y uno de **Pearson de
−0,6004** (p = 0,0300)». Recalculado con el mismo criterio sobre los dos consolidados:

| Consolidado | Spearman | Pearson |
|:---|---:|---:|
| Publicado | ρ = **−0,5165** · p = 0,0707 | r = **−0,6002** · p = 0,0301 |
| **Nuevo** | ρ = **−0,0879** · p = **0,7752** | r = −0,4816 · p = 0,0956 |

**La relación se desvanece.** ρ pasa de −0,52 a −0,09, y el Pearson deja de alcanzar significación.
Reproduce la cifra del comité al cuarto decimal.

Eso afecta a la **conclusión sustantiva** del trabajo —el beneficio del RAG decrece con la capacidad
del modelo—, que sobre el corpus corregido **no se sostiene con la misma fuerza**. Y conviene decir
tres cosas para no exagerar: el informe **ya declara** que el coeficiente no alcanza significación
por Spearman; el artefacto `correlacion.json` **ya declara** que los dos coeficientes discrepan de
veredicto y que reportar solo uno sería selección; y ese mismo artefacto **ya declara la objeción de
fondo**, que el Δ contiene la variable con la que se correlaciona. Es la parte más débil del trabajo,
y el proyecto lo sabía.

### Lo que esto deja sobre la mesa

**Las dos afirmaciones se compensan y no se cancelan.** El «ocho de trece» **refuerza** que el RAG
funciona; la correlación que no replica **debilita** que funcione *inversamente a la capacidad*. La
lectura honesta es que el trabajo tiene **un efecto más sólido de lo que publica** y **un patrón más
débil de lo que afirma**, y que las dos cosas se declaran juntas.

**Nada de esto está en el informe**, y las dos son decisión del autor. La primera lleva pendiente
desde el 8 de septiembre en `§F76`.

---

## §F144 — La auditoría se equivocó y el informe tenía razón: el 50 % de FinanceBench existe

**Fecha:** 2026-09-09 · **Origen:** el workflow de revisión de las 38 fuentes lo señaló y se
recomprobó en la fuente primaria

**Este es el hallazgo más importante del día, y consiste en que un hallazgo anterior era falso.**

[§F106](#f106) declaró el 2026-09-09 que «el 50 % que la Tabla 1 atribuye a FinanceBench no existe en
FinanceBench», y de ahí salió la **decisión 17**, abierta, con cuatro opciones para sustituir la
cifra y una recomendación concreta: bajarla a «19 % exactitud».

**El 50 % sí existe, dos veces.** Verificado por el workflow y **recomprobado por mí** en
`ar5iv.labs.arxiv.org/html/2311.11944`, en una consulta independiente:

| Dónde | Texto literal |
|:---|:---|
| Tabla 2 del artículo | «**GPT-4-Turbo Single Vector Store 75 (50%)** 17 (11%) 58 (39%) 150» |
| Prosa de §5 | «…had a higher success rate than the configuration with a single vector store for all documents **(50% vs 19%)**» |

**El error fue leer la tabla desplazada una fila.** El 41 % que §F106 atribuye a «GPT-4-Turbo con
almacén único» es la fila de **`Llama2 Single Vector Store 62 (41%)`**.

### Lo que esto habría costado

Las cuatro opciones de la decisión 17 **habrían introducido un error donde no lo había**. Y la
recomendada era la peor de las cuatro: sustituir el 50 % por el 19 % del almacén compartido
**subestima el estado del arte** y, al hacerlo, **habría hecho parecer mejor al trabajo de lo que le
corresponde**. Exactamente lo contrario de lo que la decisión pretendía, que era corregir un dato en
contra del propio interés.

Dicho de otro modo: una revisión que se preciaba de corregir en contra de su interés estuvo a punto
de mejorar su posición relativa con un dato peor.

### Por qué importa más allá del caso

Es el caso de manual de la regla que `CLAUDE.md` fija desde el incidente de la Tabla 2: **un hallazgo
de auditoría es una hipótesis, no un hecho**, y hay que verificarlo contra la fuente primaria antes
de convertirlo en instrucción de corrección. Aquí la auditoría se equivocó y **el informe tenía
razón**, y la única razón por la que no se aplicó es que la decisión estaba **reservada al autor** en
lugar de ejecutada por un agente.

Y añade un matiz a [§L77](#l77), que decía que un hallazgo puede detectar bien y encuadrar mal: **a
veces no detecta nada**, y el defecto es entero. La diferencia entre las dos situaciones solo se ve
abriendo la fuente.

**Rectificado** en §F106, de forma aditiva y con el texto original conservado, y la **decisión 17
cerrada sin cambio**. Y rectificada su afirmación de cierre: decía «de las cinco cifras que el
informe atribuye a una fuente, cuatro están verificadas y solo ésta es falsa». **Las cinco están
verificadas.**

### Y un defecto pequeño y real que el mismo workflow encontró, este sí

La glosa que sigue a la Tabla 1 dice «las cifras de **la última columna** no son directamente
comparables entre sí». Verificado sobre el Markdown: la tabla tiene seis columnas —Trabajo, Dataset,
Modelo, **Desempeño publicado**, Privacidad, Idioma— y **la última es «Idioma»**. Las cifras están en
la **cuarta**.

La glosa es correcta en el fondo, y de hecho es una de las declaraciones más honestas del capítulo.
Solo apunta a la columna equivocada. **Pendiente de corregir «última» por «de desempeño publicado»**,
que es más claro que «cuarta» y no se rompe si alguien reordena. **No lo aplico ahora**: hay un
workflow de consistencia leyendo el Markdown en este momento y sus citas se apoyan en él; se aplica
cuando cierre.

---

## §F145 — El proveedor de los datos de sanciones está mal atribuido: en el entregable siempre, y en la fuente una vez

**Fecha:** 2026-09-09 · **Origen:** dos workflows lo señalaron como el hallazgo más grave y se
verificó contra el artefacto primario

**El artefacto primario es inequívoco.**
`repos/ner-llm-entity-benchmark/data/dictionaries/PROCEDENCIA.md` declara que los diccionarios se
construyen desde **`treasury.gov/ofac/downloads/sdn.csv`** —la lista de Nacionales Especialmente
Designados de la Oficina de Control de Activos Extranjeros del Tesoro de los Estados Unidos— más
S&P 500, un repositorio de nombres españoles y `tidytuesday`. **No menciona OpenSanctions en ninguna
parte.**

OFAC y OpenSanctions **no son lo mismo**: la primera es la autoridad sancionadora estadounidense y la
segunda un agregador independiente de listas. Para un tribunal con dominio AML/KYC —que es el dominio
de este trabajo— confundirlas no es un detalle de forma.

### Dos defectos distintos, y hay que separarlos

**Primero, en el entregable, y es total.** Los tres `.docx` dicen:

| | Texto |
|:---|:---|
| Atribución del corpus | «Las entidades fueron seleccionadas de la base de datos **OpenSanctions [19]**» |
| Trabajo futuro | «bases de datos de **OpenSanctions [19]**» |
| **Entrada [19] de la bibliografía** | «**OpenSanctions**: Open Data on Sanctions Lists and Politically Exposed Persons» |
| Menciones de «SDN» | **cero** |

Y el Markdown canónico dice, en los mismos sitios, «la lista **SDN** del Departamento del Tesoro de
los Estados Unidos [19]» con la entrada **[19] = U.S. Department of the Treasury, Office of Foreign
Assets Control, *Specially Designated Nationals and Blocked Persons List (SDN)*, instantánea del 27
de julio de 2026**, `treasury.gov/ofac/downloads/sdn.csv`.

De modo que **la fuente se corrigió y el entregable no**, incluida su **entrada bibliográfica**. Es el
mismo desfase de [§F127](#f127), pero con una diferencia que lo hace peor que los demás: los otros son
**ausencias**, y este es una **afirmación falsa** — el entregable atribuye datos a un proveedor que no
los aportó, y respalda esa atribución con una referencia a ese proveedor.

**Segundo, y es nuevo: el Markdown se contradice a sí mismo una vez.** Dos pasajes describen **los
mismos** pares `{entidad_PER, entidad_ORG}` del corpus sintético N=30, a 4 123 caracteres de
distancia:

- **Anexo F**: «Para cada artículo sintético se definió a priori un par {entidad_PER, entidad_ORG}…
  Las entidades fueron seleccionadas de **la lista SDN del Departamento del Tesoro** de los Estados
  Unidos [19]»
- **Anexo G.2**: «el autor definió a priori la distribución temática, los pares {entidad_PER,
  entidad_ORG} objetivo **tomados de OpenSanctions**»

**El Anexo F es el correcto**, porque coincide con el artefacto primario. El Anexo G.2 conserva la
atribución vieja. Ninguna comprobación lo detectaba: la 3 verifica que toda cita tenga entrada y
toda entrada cita, no que dos pasajes atribuyan el mismo dato a la misma fuente.

**Y hay dos menciones de OpenSanctions en el Markdown que son legítimas y no se tocan:** la de
trabajo futuro —«ampliar el corpus incorporando fuentes como la UAF, CMF y bases de datos de
OpenSanctions [38]»—, que es una propuesta y no una atribución, y la entrada **[38]**, que es
`FollowTheMoney`, una ontología que OpenSanctions sí publica y que el trabajo sí usa. Distinguirlas
importa: corregir de más aquí borraría una referencia correcta.

### Qué hay que hacer, y por qué no lo hago ahora

**En el Markdown, una palabra:** en el Anexo G.2, «tomados de OpenSanctions» pasa a «tomados de la
lista SDN del Departamento del Tesoro de los Estados Unidos [19]», que es lo que ya dice el Anexo F.

**En los tres `.docx`, tres cosas:** las dos atribuciones y la **entrada [19] completa**. Es de la
pasada de maquetación y va en el encargo de Claude Desktop.

**No aplico la corrección del Markdown en este momento** porque hay un workflow de consistencia
leyéndolo y sus citas se apoyan en él. Queda anotada con el texto exacto, junto con la de la glosa de
la Tabla 1 de [§F144](#f144), para aplicarlas juntas cuando cierre.

---

## §F146 — Los números de las comprobaciones no identifican nada, y los he citado veintidós veces

**Fecha:** 2026-09-09 · **Origen:** el verificador del workflow de propagación avisó de que sus
agentes citaban «la comprobación 54» donde era la 52, y al mirarlo el problema era mayor

Los comentarios `# --- N.` del verificador parecen numerar las comprobaciones. **No las numeran.**

| | |
|:---|---:|
| Marcadores `# --- N.` declarados | **37** |
| Comprobaciones que el verificador ejecuta | **56** |
| Comprobaciones **sin marcador** | **19** |
| Marcadores cuyo número **no coincide con su orden de ejecución** | **34** |
| Hueco de numeración | **26 a 44** |

**Por qué derivaron:** las funciones nuevas se insertan al **principio** del fichero —es el patrón que
he usado toda la sesión— y sus llamadas `ejecutar(...)` van en el bloque de ejecución, en otro sitio.
El número del comentario y la posición real se separaron sin que nada avisara. Los marcadores 45 a 55
existen porque a las últimas sí les puse comentario; las 19 de en medio se añadieron sin él.

### Y las he citado veintidós veces, dos de ellas mal

Doce números citados en la documentación —26 a 31, 33, 34, 38, 39, 43, 44— **no existen como
marcador**. Y de las cinco citas que quedaban en los dos encargos vivos, que son instrucciones que
alguien va a seguir, **dos apuntaban a otra cosa**:

| Cita | Decía | Es |
|:---|:---|:---|
| «la comprobación 3 del verificador vigila la referencia cruzada» | el marcador 3 es `c_tablas` | la de referencias es `c_refs_anexos_tablas` |
| «lo comprueba la comprobación 44» | **no existe** | `c_docx_sano` |

**No se renumera.** Las citas de `FINDINGS` son registro fechado y renumerar las invalidaría todas.

**El arreglo es declarar que el número no identifica** y citar por **el texto que pasa a `check()`**,
que sí es estable: es lo que aparece en la salida y lo que alguien busca con un `grep`. Escrito en la
cabecera del verificador, y las cinco citas de los dos encargos pasadas a nombre — «la comprobación
"los tres .docx siguen siendo OOXML estructuralmente sano"» en lugar de «la 44».

### Y un falso positivo mío, que corregí a los dos minutos de crearlo

Reporté también «un duplicado en el marcador 2». **No lo había.** Mi patrón era
`^# --- (\d+)\.` y el segundo marcador es `# --- 2.bis.`, que empieza por `# --- 2.` y por tanto
casaba como si fuera un segundo «2». Con el patrón correcto —`(\d+(?:\.bis)?)`— hay **37 marcadores y
cero duplicados**.

Peor: **al «arreglarlo» corrompí el comentario**, convirtiendo `# --- 2.bis.` en `# --- 2.bisbis.`.
Detectado y deshecho en la comprobación inmediata. Es [§L71](#l71) por quinta vez en la sesión —el
detector roto, no el documento— y esta vez con daño real, aunque de dos minutos.

**Lo que sí es cierto de este hallazgo:** los 37 marcadores para 56 comprobaciones, las 19 sin
marcador, los 34 desajustes de orden, el hueco 26–44 y las doce citas a números inexistentes. Nada de
eso venía de mi regex; el duplicado sí.

---

## §F147 — Aplicadas las dos correcciones retenidas, y añadido el trabajo futuro que la decisión B dejaba a medias

**Fecha:** 2026-09-09 · **Origen:** el workflow de consistencia que bloqueaba el Markdown murió por
el límite de sesión, y con él repuesto el fichero quedó libre

### Las dos que estaban retenidas

[§F144](#f144) y [§F145](#f145) dejaron dos correcciones anotadas con su texto exacto y sin aplicar,
porque un workflow estaba leyendo el Markdown y sus citas se apoyaban en él. Aplicadas ahora, las dos
en el mismo commit:

| De | Decía | Dice |
|:---|:---|:---|
| Anexo G.2 | «pares {entidad_PER, entidad_ORG} objetivo tomados de OpenSanctions» | «tomados de la lista SDN del Departamento del Tesoro de los Estados Unidos [19]» |
| Glosa de la Tabla 1 | «las cifras de la última columna» | «las cifras de la columna de desempeño publicado» |

**Y comprobado lo que había que no tocar:** las dos menciones legítimas de OpenSanctions siguen en
su sitio, la propuesta de trabajo futuro y la entrada [38] de `FollowTheMoney`, que es una ontología
que ese proveedor sí publica y que el trabajo sí usa. Corregir de más habría borrado una referencia
correcta.

### El punto 11 de §7.2, que es el pendiente de la decisión B

`DECISION-ESTADISTICA-20260909.md` cerraba la decisión B —el contraste pareado sale del estudio y
queda como trabajo futuro— con un pendiente escrito para quien editase el Markdown a continuación.
Escrito ahora, y reúne dos cosas que el autor pidió por separado:

1. **El contraste pareado por modelo** con corrección por comparaciones múltiples, que es el
   procedimiento que corresponde a un diseño en el que los veintiséis grupos evalúan los mismos
   artículos. Declarando **las dos métricas**, porque no coinciden en qué modelos resultan
   significativos, y con **tres cifras** de tamaño de efecto por modelo: mediana, media y reparto de
   los pares que cambian. La razón está medida: dos de los cuatro significativos de la métrica
   restringida tienen mediana exactamente cero, y con solo la mediana parecerían no tener efecto.
2. **Las variantes de F1**, que responden a la pregunta del autor de si existe alguna que sostenga
   mejor los resultados. La **F1 micro**, que pondera por entidad y no por artículo, y un
   **remuestreo pareado** sobre la diferencia, que da intervalo de confianza sin suponer normalidad
   ni homocedasticidad.

La segunda trae **cita nueva, [39]**, Dror et al., ACL 2018, que es la referencia estándar de
contrastes de significación en el área. Verificada abriendo `aclanthology.org/P18-1128/`, que
responde 200, y con los datos tomados de su BibTeX canónico en lugar de de memoria: cuatro autores,
páginas 1383-1392, DOI 10.18653/v1/P18-1128. La cita y su entrada entraron **en el mismo commit**,
como exige la regla de referencias cruzadas.

### Y el precio, declarado en lugar de escondido

Añadir [39] al Markdown crea de inmediato **tres fallos nuevos** en el verificador: a los tres
`.docx` les falta esa entrada. Es la clase de desfase de [§F121](#f121), y es inevitable mientras la
fuente sea el Markdown y el entregable no se regenere con pandoc. **Declarado** con su motivo y su
responsable, la pasada de maquetación de Claude Desktop, y añadido a su encargo. Declararlo es lo que
distingue un pendiente conocido de una puerta silenciada.

**Y la comprobación de referencias colgantes cazó esta propia sección mientras se escribía:** la
declaración citaba `§F147` antes de que `§F147` existiera, y el verificador lo dijo. Es la segunda
vez en dos días que hace exactamente eso, y es la razón de tenerla.

---

## §F148 — Los dos consolidados se reproducen desde datos que están aquí, y el bloqueo de la decisión 1 era de forma

**Fecha:** 2026-09-09 · **Origen:** el §9 del encargo al equipo de 48 GB pedía un manifiesto portable
porque sus trece rutas apuntaban a otra máquina, y ninguna resolvía

**Lo que estaba bloqueado y por qué.** La decisión 1 del autor —adoptar o no el consolidado
`ANALISIS_CONJUNTO_20260909_FIX`— tenía dos impedimentos anotados. El primero: su manifiesto declara
las trece fuentes con rutas absolutas del tipo `/Users/eahumada1/Projects/…`, que **no existen en
esta máquina**. Un manifiesto cuyas rutas no abren no acredita nada, aunque los datos estén.

**Y ahí hay dos cosas que conviene no confundir:** que el manifiesto no sea **portable** es un
defecto de forma; que los datos **no estuvieran** sería de fondo. `tools/manifiesto_local.py`, escrito
hoy, separa las dos. Reancla cada ruta por la cola conocida `repos/ner-llm-entity-benchmark/`,
comprueba que el fichero existe con las filas declaradas, reagrega las fuentes aplicando la exclusión
de contaminados y la precedencia entre duplicados que el propio manifiesto declara, y contrasta el
resultado contra `merged_results.csv`.

### El resultado: los dos acreditan

| | Publicado `20260907` | Nuevo `20260909_FIX` |
|:---|:---|:---|
| Fuentes reancladas | 8 de 8 | **13 de 13** |
| Filas reagregadas frente al consolidado | 3 120 = 3 120 | **2 938 = 2 938** |
| Grupos | 26 = 26 | 26 = 26 |
| Grupos cuya F1 media discrepa por encima de 1e-4 | **0** de 26 | **0** de 26 |
| Tabla `integrity` frente a los datos | 26 entradas, 0 discrepancias | 26 entradas, 0 discrepancias |
| Rutas no portables | 0 | 13, y es lo único que queda |

**De modo que el primero de los dos impedimentos de la decisión 1 se cierra.** No hay bloqueo por
falta de datos: el consolidado nuevo se reproduce entero desde ficheros que están en este
repositorio. Queda el segundo, que es real: al nuevo le falta `levene.json`, y ese sigue siendo el
§9 del encargo al equipo de 48 GB.

### Y por el camino, dos veces el mismo error mío

La herramienta declaró **NO reproducible el consolidado publicado**, que sí lo es. Dos defectos
encadenados, los dos míos:

1. **Tomaba el fichero entero de cada fuente.** El manifiesto declara **qué grupos aporta cada una**,
   y una fuente puede traer más. El caso real es `afectados_thinking_n120_REMOTO`, con **453 filas**:
   los dos grupos de `gemma4:12b-mlx` completos y dos de `qwen3:8b` **parciales, con 99 y 114 de
   120**. La fusión toma solo los dos primeros, porque los de `qwen3` los aporta completos otra
   fuente. Leer el fichero entero **mete resultados parciales en el agregado**, que es exactamente lo
   que no debe pasar.
2. **Ignoraba la precedencia entre duplicados.** Ocho grupos vienen en dos fuentes cada uno, los
   cuatro modelos que se re-corrieron, y el manifiesto lo declara nota por nota con
   `--on-duplicate=first`. Sin precedencia salían **4 080 filas en lugar de 3 120**, que son
   justamente 8 × 120 de más.

Es **§L71 por sexta vez** en la sesión: el detector roto y no el documento. Y con el agravante de que
esta vez el falso positivo caía sobre el **artefacto que sostiene el informe**. Si lo hubiera
reportado sin abrir el manifiesto, habría dicho que la cifra titular del trabajo no se reproduce.

**Lo que hizo la diferencia** fue el control: correr la herramienta sobre el consolidado **publicado**
antes de creerme el resultado del nuevo. Una herramienta probada solo con el caso que quería acreditar
no está probada.

### La prueba de mutación, y una que no detecta por buenas razones

Seis mutaciones del manifiesto sobre los dos consolidados. **Once de doce detectadas.** La que no:
invertir la precedencia a `last` en el consolidado **nuevo**, que **no tiene ni un duplicado** —sus
trece fuentes son disjuntas, una por modelo— de modo que la regla no cambia nada. La mutación era
**inaplicable**, no la comprobación ciega; sobre el publicado, que tiene ocho duplicados, se detecta.
Distinguirlo importa: es la lección de las cuatro mutaciones mal armadas de §L71, aplicada a tiempo
en lugar de después.

---

## §F149 — Tres pares (F, p) circulando para un mismo consolidado, y ninguno era un error de cálculo

**Fecha:** 2026-09-09 · **Origen:** el workflow de consistencia `wf_348f89e2-43b`, lote de artefactos;
único hallazgo marcado **grave**, confirmado por su refutador y **recomprobado aquí**

Para el directorio `ANALISIS_CONJUNTO_20260907`, que es el consolidado **publicado** y el que
sostiene la cifra titular del trabajo, había **tres pares (F, p) distintos** en circulación:

| Dónde | Dice | Modelos |
|:---|:---|---:|
| `AVISO-SUMMARIES-OBSOLETOS.md` | F = 36,3696 · p = 1,4321e-164 | **14** |
| `RUNS_INDEX.md` | F = 36,3666 · p = 1,2236e-152 | 13 |
| **El artefacto**, `statistical_report.md` | **F = 38,2222 · p = 3,4453e-160** | 13 |

Y el informe cita la tercera, que es la correcta.

### Y no es un error de cálculo: son tres estados sucesivos del mismo directorio

Lo que parecía una contradicción resultó ser una **secuencia**, y la reconstruye el historial:

1. Commit `10f3ebc` del 7 de septiembre: análisis conjunto con **14 modelos**, F = 36,3696.
2. Commit `58647f5`, el mismo día: se retira del estudio la cuantización no reproducible y quedan
   **13 modelos**, F = 36,3666.
3. Commit `37ef239`: `gpt-oss` corregido cierra el estudio con **F = 38,2222**, que es lo que el
   directorio contiene hoy.

**Cada cifra fue cierta el día que se escribió.** El defecto no está en el número sino en el
**tiempo verbal**: tres documentos afirman en presente —«el análisis conjunto **vigente** es», «análisis
conjunto **definitivo**», «alcance **definitivo** del estudio»— un estado que dejó de serlo esa misma
tarde.

### Qué se corrigió y qué no, y el criterio

El criterio es el de `CLAUDE.md`: se corrigen los artefactos que **afirman**, se conservan los que
**atestiguan**. Aquí la línea no cae por tipo de fichero sino por **tiempo verbal**.

**Corregidos, de forma aditiva y sin borrar la cifra vieja**, los tres que afirman en presente:
`AVISO-SUMMARIES-OBSOLETOS.md`, `RUNS_INDEX.md` y `TODO-INFORME-FINAL.md`. Cada uno conserva su
número original y lleva ahora una nota fechada que dice cuál es el vigente y **que la autoridad es el
`statistical_report.md` del propio directorio, no el documento que se está leyendo**.

**No tocados**, porque atestiguan lo que se afirmó en una fecha: `CIERRE-BENCHMARKS-20260907.md`, las
filas del registro de `CURRENT-TASKS.md`, `research/rag/WORKLOG.md`,
`CORRECCION-B1-SUMMARIES-20260907.md`, `PROMPT-CLAUDE-DESKTOP-20260907.md` y
`remote_48g/RESPUESTA-CORRECCION-20260907.md`. Reescribir un documento fechado para que diga lo que
hoy sabemos no es limpiar: es falsificar el registro.

### El «14 modelos» merece una frase aparte

El decimocuarto era la cuantización *custom* que se retiró del estudio por no ser reproducible, y
está en la lista cerrada de exclusiones. El aviso **no la nombra** —solo cuenta catorce— y la nota de
corrección tampoco la nombra, porque la exclusión se aplica y no se narra. Queda dicho aquí, que es
el registro de hallazgos, y no en un artefacto del estudio.

### Lo que hay que llevarse

**Una cifra en un documento de orientación caduca sin que nada avise.** Es el mismo mecanismo de
[§F134](#f134), los recuentos mantenidos a mano, aplicado a un resultado estadístico: el número se
copió a seis sitios y el artefacto se regeneró dos veces el mismo día. La defensa no es acordarse de
actualizarlos, sino **que el documento remita al artefacto en lugar de repetirlo**, que es lo que
ahora dicen las tres notas.

---

## §F150 — Auditados los 218 commits del día: no se perdió nada, y ahora la comprobación es mecánica

**Fecha:** 2026-09-09 · **Origen:** la instrucción permanente del autor de «revisar que no se pierda
información», que hasta hoy se cumplía a ojo

La política del proyecto es **estrictamente aditiva** para la documentación. Pero «aditiva» no
significa que ninguna línea cambie nunca: un título se corrige, un recuento mantenido a mano se
retira, un estado de tarea avanza. Lo que no puede pasar es que una afirmación, una fila de datos o
una entrada del registro **desaparezca sin dejar rastro**. Hasta hoy nadie comprobaba cuál de las dos
cosas ocurría.

### El resultado sobre los 218 commits de la jornada

| | |
|:---|---:|
| Commits examinados | **218** |
| Documentos aditivos vigilados | 7 |
| Líneas borradas con contenido | **82** |
| Clasificadas como legítimas de forma automática | **66** |
| Que requerían juicio humano | **16** |
| **Pérdidas reales** | **0** |

Los 16 se reparten en **ocho commits, y los ocho son correcciones de una afirmación que resultó
falsa**: el recuento de tablas descriptivas que eran diez y no nueve, el rango de BloombergGPT que
pasó de «no verificado» a verificado, mi propia frase sobre `mistral-nemo` que decía «pierde el signo
negativo» cuando eso solo vale para la mediana, la distinción entre el respaldo que atestigua y el
espejo rodante, y la rectificación de la decisión 17. **Ninguno retira información: sustituye un
enunciado erróneo por el correcto.**

### Las tres comprobaciones puntuales que más importaban

- **`§F106`** conserva su título original **tachado**, con la rectificación al lado. La afirmación
  falsa sigue legible, que es como este proyecto rectifica.
- **La fila `§1.188`** del registro de `CURRENT-TASKS`, que el `diff` mostraba borrada, está
  **reescrita en el sitio** en el mismo commit.
- **`F28`, `F32` y `F33`** siguen presentes; lo que cambió fueron sus títulos.

Y los dos únicos ficheros rastreados de cero bytes son los **declarados** por decisión del autor.

### La herramienta, y las dos veces que estuvo mal antes de estar bien

`tools/auditar_borrados.py` clasifica cada línea borrada en tres categorías legítimas —reescritura en
el sitio, texto que sigue vivo, rectificación conservada con tachado— y saca el resto para que lo
mire una persona.

Y hubo que corregirla dos veces, las dos por ser **demasiado estrecha**:

1. **Buscaba el texto solo en su propio fichero.** Un párrafo que se muda no se ha perdido: las tres
   opciones de la decisión 8 salieron de `DECISIONES-PENDIENTES` y entraron en `FINDINGS` cuando la
   decisión se reformuló, porque el evaluador ya estaba corregido. Ampliada al **corpus completo** de
   documentos aditivos.
2. **Comparaba línea contra línea.** Estos documentos van con salto de línea duro a cien columnas, de
   modo que reescribir un párrafo reflowea todas sus líneas y **ninguna casa una a una**. Añadida una
   comparación por **cobertura de palabras distintivas contra lo que el mismo commit añadió**, que es
   la granularidad correcta. Bajó de 23 a 16.

**Lo que la herramienta no puede hacer, y lo dice al ejecutarse:** distinguir «corrigió una
afirmación falsa» de «perdió información» exige leer, y eso es juicio humano. Lo que sí hace es
reducir 82 líneas a 16 y dar el commit de cada una. Una herramienta que prometiera el juicio estaría
mintiendo; ésta promete el cribado.

---

## §F151 — El informe declaraba pendiente una re-corrida ya hecha, y ninguna comprobación miraba en esa dirección

**Fecha:** 2026-09-09 · **Origen:** dos lotes del workflow `wf_348f89e2-43b` lo señalaron por
separado, el de tablas y el de anexos, y los dos con confianza alta

### La afirmación falsa

El Anexo I decía: «La re-corrida completa **pendiente** unifica el presupuesto en 4096 para los trece
y resuelve la asimetría». **La re-corrida se ejecutó el 8 de septiembre** y está completa: trece
directorios `__N120` en `recorrida_20260908/`, y los trece declaran `max_tokens=4096` y
`rag_mode=kb_combined` sin una excepción.

Era cierta al escribirla. Dejó de serlo, y nadie lo notó.

### Y la regla de integridad obliga a más que a corregir el tiempo verbal

`CLAUDE.md` es explícito: cuando existen varias corridas del mismo experimento, **el informe declara
todas**, dice cuál toma como referencia y por qué. Citar una y callar la otra es indistinguible de
seleccionar el resultado, aunque no haya intención de hacerlo.

El pasaje corregido declara ahora las dos mediciones, mantiene como referencia la publicada —que es
la que sostiene todo el capítulo de resultados— y da **dos razones**, las dos verdaderas: que la
segunda se completó una vez cerrado ese análisis, y que **no difieren solo en el presupuesto de
salida**, porque la segunda excluye siete artículos contaminados y aporta ciento trece registros por
grupo en lugar de ciento veinte. Esa segunda razón importa: presentar el salto de F = 38,2222 a
F = 119,7502 como efecto de unificar los tokens sería falso, porque mezcla dos cambios.

**Va en el Anexo I, que la restricción institucional excluye del límite de 25 páginas**, de modo que
la declaración no cuesta espacio del cuerpo.

### El punto ciego, que es el hallazgo de verdad

Al corregirlo el verificador dijo **cero fallos nuevos**, y no debería. El párrafo cambió en la fuente
y no en los tres `.docx`.

La comprobación de prosa va en **una sola dirección**, del Markdown al entregable, y solo declara
ausente un párrafo del que no aparece **ninguna** de sus cinco sondas. Yo cambié el **final** de un
párrafo cuyo **arranque** sigue igual: las sondas del arranque casaron, el párrafo se dio por
presente, y el entregable habría seguido afirmando lo que la fuente ya desmintió.

**Es el caso peligroso**, porque el `.docx` es lo que lee el tribunal y la fuente no.

Añadida la comprobación **«ninguna frase retirada sobrevive en los entregables»**, que va al revés:
toma las frases que la fuente retiró y exige que tampoco estén en el `.docx`. Cada entrada lleva por
qué se retiró y qué la sustituye. Y comprueba **las dos mitades**: que la frase no esté en el
entregable, y que **tampoco siga en el Markdown**, porque una entrada cuya frase sigue en la fuente
significa que la corrección no se aplicó o que la entrada está mal escrita, y una comprobación que no
puede detectar su propia obsolescencia acaba dando el valor del éxito por mirar el sitio equivocado.

### Lo que encontró al estrenarse

**Nueve fallos, tres frases por tres entregables**, y ninguno es la que motivó la comprobación:

| Frase retirada | ¿En los `.docx`? |
|:---|:---|
| «tomados de OpenSanctions» | sí, en los tres |
| «de la base de datos OpenSanctions» | sí, en los tres |
| «cifras de la última columna» | sí, en los tres |
| «re-corrida completa pendiente» | **no**, y por una razón |

Las tres primeras son la **pieza 7** del encargo de maquetación y la corrección de [§F144], ya
asignadas. La cuarta no aparece porque **ese pasaje del Anexo I nunca llegó al entregable**: es uno
de los diez párrafos ausentes de [§F121]. De modo que el entregable no afirma la falsedad, pero solo
porque tampoco afirma nada sobre eso. No es un consuelo: es la misma deuda por otra vía.

---

## §F152 — El índice Tok/s/B de `llama3.2` circulaba con dos valores, y uno redondeaba un redondeo

**Fecha:** 2026-09-09 · **Origen:** el lote de tablas de `wf_348f89e2-43b`, confianza alta

`llama3.2:latest` aparecía con **26.44** en la Tabla 4, el Hallazgo 4 y §5.5, y con **26.5** en la
Tabla 8. Es el mismo índice del mismo modelo.

**El valor real, recalculado desde `benchmark_results.csv` sobre el subconjunto `_baseline` de
N=15:** el Tok/s medio es 79,3453 y el índice, 79,3453 / 3 = **26,4484**, que redondea a 26,44. La
Tabla 8 había calculado el índice sobre el **Tok/s ya redondeado** a 79,35, es decir 79,35 / 3 = 26,5:
redondeó dos veces, y la segunda ronda perdió precisión que la primera no debía haber gastado.

**Corregido en el Markdown**, unificando las cuatro apariciones en 26,44. **Y comprobado que nadie lo
vigilaba:** la comprobación de la Tabla 8 valida VRAM y Tok/s contra los datos, pero no el índice
derivado, que es aritmética sobre columnas ya validadas y por eso parecía no necesitar comprobación
propia. Es el mismo mecanismo que [§F134](#f134): una cifra que se calcula a mano y no contra su
artefacto se desfasa sin que nada avise.

**Y el desfase de siempre con los `.docx`:** al corregir el Markdown, dos de los tres entregables
siguen con 26.5 en la Tabla 8. Declarado con su responsable, junto a la pieza 7 del encargo de
maquetación, que ya corrige la misma tabla.

---

## §F153 — La Tabla 19, cinco filas sin identificar su configuración: anotado y no perseguido, por decisión de cierre

**Fecha:** 2026-09-09 · **Origen:** lote de anexos de `wf_348f89e2-43b`, confianza media/alta; el
autor pidió cerrar los análisis en este punto y no abrir más hilos

Dos defectos menores en el Anexo I, Tabla 19 (42 filas):

1. **La fila `llama3.2:latest`** no lleva sufijo de modo y **reproduce exacta** —los siete valores,
   comprobado registro a registro— a `llama3.2:latest_baseline`. El propio texto que sigue a la tabla
   ya lo advierte: «la tabla tiene cuarenta y dos filas pero cuarenta y una configuraciones
   distintas». El defecto es de **etiqueta**, no de dato: la fila no dice de qué modo es.
2. **Las cuatro filas `zs-es`/`zs-en`/`fs-es`/`fs-en`**, de la ablación de prompt, no identifican a
   qué **modelo** pertenecen en la columna que sí lo hace para las otras 38.

**No se persigue más en esta sesión**, por instrucción explícita del autor de cerrar los análisis y
pasar a las formalidades. Queda para quien maquete: añadir el sufijo `_baseline` a la fila 33 y el
nombre del modelo a las cuatro filas de ablación, sin tocar ninguna cifra. Es aditivo y de una
palabra por fila; no cambia ningún resultado del estudio.

---

## §F154 — Decisión 1 ejecutada: adoptado el consolidado de la re-corrida completa

**Fecha:** 2026-09-09 · **Origen:** instrucción explícita del autor («tomar el consolidado nuevo»),
sobre la decisión que `§F113`/`§1.246` dejaban reabierta y recomendada

### Qué cambió mecánicamente

`CSV_CONSOLIDADO` y `MANIFIESTO` en `tools/verificar_informe.py` pasan de
`ANALISIS_CONJUNTO_20260907` (publicado, 3 120 filas, 8 corridas heterogéneas) a
`ANALISIS_CONJUNTO_20260909_FIX` (re-corrida completa, 2 938 filas = 26×113, trece corridas
homogéneas de `recorrida_20260908/`, todas con `max_tokens=4096` y `rag_mode=kb_combined`). El
publicado **no se borra**: sigue en su directorio, es el que sostuvo el informe hasta hoy y el que
un tribunal puede pedir ver.

**Cuatro defectos de infraestructura, corregidos antes de adoptar y no después:**

1. **Rutas absolutas no portables.** El manifiesto del consolidado nuevo declara sus trece fuentes
   con rutas de otra máquina (`§F148`). Cuatro sitios de `tools/verificar_informe.py` las trataban
   como locales sin reanclar, y dos consumidores más —`tools/sensibilidad_combinada.py`— tenían el
   mismo defecto. Los seis, corregidos con la misma técnica: recortar por la cola conocida
   `repos/ner-llm-entity-benchmark/`.
2. **Cinco constantes hardcodeadas** al consolidado publicado en `verificar_informe.py` (`c_levene`,
   `c_tukey`, `c_titulares`, `c_conclusion1`, la de telemetría) se reescribieron para derivar de
   `CSV_CONSOLIDADO`, una sola fuente de verdad — el mismo mecanismo que evitó el desfase de
   `§F149`, aplicado antes de que ocurriera aquí.
3. **`tools/sensibilidad_combinada.py` cargaba los 120 registros crudos contra un CSV de 113**
   (contaminados excluidos) y por eso declaraba **los 26 grupos incoherentes**, no solo
   `nemotron-mini:4b`. Corregido filtrando los siete artículos contaminados que el manifiesto
   declara. Verificado tras el arreglo: **los 26 grupos coinciden**, incluido `nemotron-mini:4b`,
   cuya exclusión ya no hace falta.
4. **`levene.json` y `friedman.json` no existían** para el consolidado nuevo. Generados con el mismo
   método —biblioteca estándar, verificado contra `scipy` del venv del proyecto— y persistidos en
   `results/ROBUSTEZ_ESTADISTICA_20260909_FIX/`.

### Las cifras que cambian, todas desde el verificador y no de memoria

| | Publicado | Adoptado |
|:---|---:|---:|
| ANOVA F (p) | 38,2222 (3,4453e-160) | **119,7502** (subdesborda a 0,0; el informe debe escribir «p < 10⁻³⁰⁰») |
| Tukey, significativos de 13 | 2 (`nemotron-mini:4b` +14,52 pp, `llama3.2:latest` +10,82 pp) | **1** (`nemotron-mini:4b` +12,26 pp; `llama3.2:latest` +6,73 pp, p=0,2334, **ya no significativo**) |
| Tukey, pares significativos de 325 | 158 | **217** |
| Friedman χ² | 1 169,2327 | **1 802,3671** |
| Levene (Brown-Forsythe) p | 0,1842 (no detecta) | **1,394e-11** (sí detecta) |
| Correlación capacidad-beneficio, Spearman | −0,5165 (p=0,0707) | **−0,0879** (p=0,7752) |
| Correlación, Pearson | −0,6004 (p=0,0300) | **−0,4816** (p=0,0956) |

### Y el hallazgo que importa más que cualquier número: la categoría fantasma de `§F53` se corrigió

`§F64` y `CURRENT-TASKS §1.246` ya lo habían establecido y aquí se **reverifica**: el defecto que
motivó toda la sección «Integridad de la medición» de `CLAUDE.md` —una categoría que el corpus no
anotaba, con el 65 % de los falsos positivos cayendo ahí— era **Locations**, y en el corpus de la
re-corrida **está corregido**. Comprobado con el indicador que `CLAUDE.md` fija: `tp+fn` agregado
por categoría, sobre `gemma4:31b-mlx_baseline` de la re-corrida:

| Categoría | tp | fp | fn | tp+fn |
|:---|---:|---:|---:|---:|
| Persons | 509 | 17 | 85 | 594 |
| Organizations | 565 | 162 | 247 | 812 |
| **Locations** | **477** | 134 | **68** | **545** |

`tp+fn = 545`, no cero: el corpus **sí anota Locations** ahora (119 de 120 artículos, 545 entidades),
tras los commits `eb97af0`/`c776fe0`/`f49c03c` («Locations recuperadas», «63 locations embebidas de
Kleptotrace»). Es la explicación real del salto de F1 —de 22-62 % a 22-82 % en la Tabla 7—: no es
solo excluir siete artículos contaminados, es que una categoría entera dejó de penalizarse contra el
vacío.

**Y esto tiene una consecuencia sobre el Anexo I que `§F64` ya adelantaba y que aquí se ejecuta.** La
«medición restringida a Personas y Organizaciones» existe **para compensar** la ausencia de anotación
de Locations. Con Locations ya anotadas en la re-corrida, seguir restringiendo **no corrige nada: solo
descarta información válida**, y `§F64` ya lo había medido con cuatro puntos de comparación: la
restringida **subestima** el valor real entre 1,3 y 5,7 puntos, siempre en la misma dirección, «no es
error de la estimación: es el crédito por acertar en una categoría que antes no se podía acertar».

**Por tanto, las cifras titulares del resumen y del §6 —que citaban la métrica restringida
precisamente para sortear el defecto— pasan a citar la métrica completa de la Tabla 7**, que ya es
válida sobre la re-corrida:

| Titular | Restringida (lo que decía) | Completa (lo que pasa a decir) |
|:---|---:|---:|
| F1 en español, N=120 (`gemma4:31b-mlx_baseline`) | 76,55 % | **81,47 %** |
| F1 de la variante alojada, N=120 (`gemma4:31b-cloud_baseline`) | 80,42 % | **82,13 %** |
| F1 sobre el dominio, N=30 (`gemma4:31b-mlx`) | 90,16 % | **90,16 % (sin cambio: corpus N=30, no afectado por la decisión 1)** |

**El Anexo I no se borra**: sigue siendo la evidencia de que el defecto existió y de cuánto costaba,
y de que su estimación era conservadora. Lo que deja de tener sentido es **calcularla de nuevo sobre
la re-corrida**, porque ahí no hay nada que restringir.

### Lo que queda pendiente, y es del autor

**Decisión 11** (reformular la tesis central) se ejecuta con estas cifras: el hallazgo pasa de «dos
modelos pequeños» a **un modelo** (`nemotron-mini:4b`) con mejora estadísticamente sólida por Tukey,
y `llama3.2:latest` como el mayor delta bruto entre los que no alcanzan la corrección por
comparaciones múltiples. **Decisión 13** (convención de agregación de la conclusión 1) se resuelve
con las cifras de este consolidado, no las del publicado.

---

## §F155 — Decisión 1 completada: el Markdown reescrito, verificado en 0 fallos nuevos

**Fecha:** 2026-09-09 · **Origen:** continuación de §F154, instrucción del autor de terminar y
completar la adopción

`§F154` dejó hecho el cambio mecánico —`CSV_CONSOLIDADO` y `MANIFIESTO` apuntando al consolidado
adoptado— y las cifras que cambiarían, todas verificadas. Esta entrada cierra el trabajo: el
Markdown canónico reescrito con esas cifras, el verificador generalizado para que no vuelva a
desfasarse, y las dos figuras regeneradas.

### Lo que se reescribió en el Markdown, todo verificado por el propio verificador

- **Tabla 7** (26 celdas): sustituida por los valores del consolidado adoptado.
- **§5.3.1**, párrafo del ANOVA/Tukey/Levene/Friedman: F=119,7502 con `p < 10⁻³⁰⁰` (cota, porque
  subdesborda); Tukey **uno** de trece significativo (`nemotron-mini:4b` +12,26 pp), no dos —
  `llama3.2:latest` pasa de +10,82 pp significativo a +6,73 pp sin serlo (p=0,2334); 217 de 325
  comparaciones significativas (antes 158); Levene **sí** detecta heterocedasticidad
  (p=1,39×10⁻¹¹, antes no la detectaba); Friedman χ²=1802,3671 (antes 1169,23).
- **§5.3.1**, párrafo de correlación: Spearman −0,0879 (p=0,7752) y Pearson −0,4816 (p=0,0956); los
  dos coeficientes **coinciden** ahora en el veredicto —antes discrepaban—; retirado
  `nemotron-mini:4b`, el Pearson pasa a +0,0120: la relación con la capacidad depende casi
  enteramente de ese modelo.
- **Conclusión 6** (§7.1) y **resumen/abstract**: reformulados de «dos modelos, tendencia con la
  capacidad» a «un modelo, sin relación general con la capacidad» — es la **decisión 11**,
  ejecutada con las cifras que la sostienen.
- **Titulares** (`c_titulares` reescrito): 76,55 %→**81,47 %**, 80,42 %→**82,13 %**. Dejan de citar
  la métrica restringida porque el defecto que la motivaba —Locations sin anotar— está corregido
  en el consolidado adoptado, y `§F64` ya había medido que la restringida **subestima** el valor
  real. El 90,16 % (dominio, N=30) no cambia: ese corpus nunca tuvo el defecto.
- **Conclusiones 1 y 3, §6, §5.3.5** (decisión 13, resuelta): retirada la comparación «bajo la
  convención original» de la conclusión 1 —quedó sin sentido al dejar de restringir N=120—, con lo
  que sus dos citas erróneas (62,67/80,51 en vez de 59,25/80,57) se retiran con ella. El coste de
  la soberanía pasa de «cuatro puntos» a **«menos de un punto»** (82,13 − 81,47 = 0,66 pp).
- **Anexo I**: mantenido como registro **histórico** del corpus publicado y su defecto —por
  decisión explícita, ver más abajo—; solo se corrige su propio error de convención (62,67→59,25,
  decisión 13) y se añade, en la subsección de corridas múltiples, la declaración de que hubo
  **dos corridas completas** del estudio, cuál es la de referencia y por qué.
- **Figura 2**: regenerada con `tools/generar_figuras_informe.py` desde la Tabla 7 ya corregida;
  corregida además la anotación y el título del panel (b), que citaban la correlación vieja.

### La pregunta de fondo, y la respuesta que queda escrita

El autor preguntó, con razón, si describir el dato histórico complica el informe. La respuesta
aplicada: el **cuerpo** afirma el resultado definitivo de forma directa, sin relitigar la historia
en cada frase; las comparaciones con el dato viejo se conservan solo donde explican un **hallazgo**
que cambia (`llama3.2:latest` deja de ser significativo, el coste de soberanía casi desaparece). El
**Anexo I entero** queda como el único lugar dedicado a la historia del defecto, que es exactamente
su propósito declarado y lo que exige la regla de integridad de `CLAUDE.md` sobre declarar todas
las corridas.

### El verificador, generalizado para que la adopción no lo rompiera en silencio

Seis constantes y funciones estaban **hardcodeadas** al consolidado publicado (`c_levene`,
`c_tukey`, `c_titulares`, `c_agregacion`, la de telemetría, `c_anexo_vs_tabla7`) y se reescribieron
para derivar de `CSV_CONSOLIDADO`/`MANIFIESTO` — una sola fuente de verdad, el mismo mecanismo que
evitó el desfase de `§F149` aplicado antes de que ocurriera aquí. Y una constante nueva,
`MANIFIESTO_PUBLICADO`, para las dos únicas comprobaciones (`c_agregacion`, `c_anexo_vs_tabla7`)
que **no** deben seguir la adopción, porque verifican el Anexo I contra su propia fuente histórica.

**Cuatro comprobaciones tenían además regex o listas hardcodeadas** al contenido exacto de la
frase publicada, no solo a la ruta del consolidado:

- `c_anova`: buscaba la p en **todo el documento**, no en una ventana tras la F; con el ANOVA
  subdesbordando encontraba la p de Levene en su lugar. Corregido con ventana y aceptación de
  «p < 10^-300».
- `c_tukey`: exigía una tupla fija de **dos** modelos con sus p literales. Generalizado para
  derivar los modelos y sus p del propio artefacto (`sig`), no de una lista escrita a mano.
- `c_levene`: exigía el verbo «no detecta» y notación decimal. Generalizado a los dos verbos y a
  notación científica cuando la p es extrema.
- `c_redondeos`: el par de «llama3.2:latest» dejó de tener sentido —ya no hay una forma redondeada
  de su delta en el resumen— y se retiró en lugar de dejarlo fallando contra un texto que no tiene
  por qué existir; el de «p de Spearman» tenía el valor **0707** escrito en el regex, y se ancló a
  la misma frase que el de Spearman en vez de a una constante.

Los cuatro son la misma lección: **una comprobación que verifica un texto tiene que leer ese
texto**, no una copia suya congelada en el código. Es exactamente lo que el propio `c_tukey` ya
advertía en su docstring sobre el delta de `nemotron-mini:4b` —«la primera versión comparaba el
artefacto contra un 0.1452 puesto a mano»— y que hoy alcanzó a cuatro comprobaciones más porque
nadie había cambiado el consolidado desde que se escribieron.

### Verificación final

`tools/verificar_informe.py`: 56 comprobaciones, **0 fallos nuevos** tras cada edición, verificado
paso a paso y no solo al final. `tools/auditar_afirmaciones.py`: 15/15. El cuerpo sigue dentro del
límite de 25 páginas. `tools/auditar_borrados.py`: sin cambios respecto de antes de esta sesión.

### Lo que queda, y es de Claude Desktop

Todos los `.docx` quedan por detrás del Markdown en los mismos sitios de siempre, más los que esta
adopción añadió: la Tabla 7 entera, la fila comparativa de la Tabla 1, el resumen y el abstract, y
el número de resaltes sin propagar (14→18). Todo declarado en el verificador con su responsable;
el encargo de maquetación se actualiza junto con esta entrada.

---

## §F156 — Tres documentos vivos seguían afirmando que el consolidado publicado era «el definitivo»

**Fecha:** 2026-09-09 · **Origen:** barrido propio tras cerrar la decisión 1, buscando toda mención
viva a «38,2222» fuera de los documentos de registro

Al cerrar `§F154`/`§F155` quedaba una pregunta sin responder: ¿algún documento que se **lee como
instrucción vigente** seguía afirmando que el consolidado publicado es el definitivo? Un `grep` de
«38,2222» fuera de `FINDINGS`/`CURRENT-TASKS`/`DECISION*`/`research/rag/WORKLOG`/`CIERRE-BENCHMARKS`
encontró seis coincidencias. Tres eran legítimamente históricas y no se tocan —
`INVENTARIO-AFECTADO-POR-F86-20260909.md` (análisis fechado), y las dos de `doc/versions/`, que son
un *changelog* de versiones entregadas y una copia congelada de una pasada de sincronización—. **Tres
no lo eran**, porque afirman en presente:

1. **`CLAUDE.md` mismo**, la sección «RAG Integration Policy»: «El análisis conjunto definitivo está
   en `results/ANALISIS_CONJUNTO_20260907/`». Es el documento que **toda sesión futura lee primero**.
2. **`TODO-INFORME-FINAL.md`**, dos sitios: una fila de checklist que declaraba «Completado» con el
   consolidado publicado como si siguiera siendo el vigente, y un bloque «lo que sí queda pendiente»
   con una disyuntiva —F=35,5557 vs F=38,2222, `§F66`— que la decisión 1 dejó sin objeto: el estudio
   ya no se mide sobre el consolidado al que esa disyuntiva se refería.
3. **`ENCARGO-CIERRE-EQUIPO-48GB-20260910.md`**, instrucción viva para el equipo remoto: decía «no se
   adoptó» el barrido corregido, y hoy sí se adoptó —no el barrido de las 18 filas problemáticas, que
   sigue sin adoptarse por las razones que el propio documento explica, sino el consolidado
   `_FIX` construido desde la re-corrida ya corregida—.

**Corregidos los tres de forma aditiva**, con nota fechada que remite a `§F154`/`§F155` y sin borrar
el texto original, el mismo tratamiento que `§F149` le dio a los primeros tres documentos de este
tipo. Es la misma clase de defecto, una tercera vez: una cifra citada en varios sitios y actualizada
en unos y no en otros, y la instrucción del proyecto — declarar todas las corridas y decir cuál es
la de referencia — hay que aplicarla en el documento de políticas tanto como en el informe mismo.

---

## §F157 — El mojibake también estaba corregido en la re-corrida, y el §5.3.1 lo describía como vigente

**Fecha:** 2026-09-09 · **Origen:** revisión propia tras cerrar `§F154`/`§F155`, comprobando si algún
otro defecto histórico quedó descrito como activo en la sección adoptada

Al revisar qué otras limitaciones de §5.3.1 podían haber quedado obsoletas por la decisión 1, until
`tools/analisis_mojibake.py` contra el corpus vigente (`data/benchmark_balanced_120.json`) dio **0 de
120 artículos afectados**, en ambos criterios. El propio script lo advierte: «la tabla anterior del
Anexo H.3 no se reproduce con ninguno de los dos [criterios]».

**Confirmado por el historial.** El commit `eb97af0` («correcciones de código y datos previas a la
re-corrida»), del 2026-09-08 y **anterior** a que corriera `recorrida_20260908/`, dice literalmente:
«Datos (validado con `analisis_mojibake.py`, afectados 0/120): 2.2 mojibake: `benchmark_balanced_120`
y `test15` a 0 marcas». Es la misma preparación de corpus que corrigió Locations (`§F53`, `§F154`):
**los dos defectos se arreglaron en el mismo paso**, antes de la re-corrida que sostiene el
consolidado adoptado.

**El párrafo de §5.3.1** —«el corpus … almacena los nombres con *mojibake* … Afecta a 283 de 1 406
entidades…»— seguía describiéndolo en presente, como limitación **activa** del análisis adoptado.
Corregido a pasado, con nota de que la corrección se verificó antes de la re-corrida y remitiendo el
detalle íntegro al **Anexo H**, que se conserva como registro histórico del defecto — el mismo
tratamiento que `§F154` le dio al Anexo I con Locations.

**Lo que queda pendiente, y no se tocó en esta pasada** por la razón que se explica abajo: la
conclusión 7 de §7.1 y el punto de trabajo futuro 7 de §7.2 también describen el mojibake como
vigente, y el primero es una conclusión titular del trabajo que merece la misma reformulación. No se
tocaron porque, al llegar a este punto, se detectó que **Claude Desktop está reconstruyendo los tres
`.docx` en este mismo momento** (`tools/_tools/render.py`, `BOLD_CUERPO_BASE` recién editado por esa
sesión), y seguir editando el `.md` mientras el renderizador lo consume arriesga una foto a medio
tomar. Queda anotado para la siguiente pasada.

**Y un incidente de concurrencia real, sin daño.** Al intentar retirar 24 declaraciones ya caducadas
de `FALLOS_DECLARADOS` —el trabajo de Claude Desktop las había resuelto—, se restauró por error una
copia de respaldo que devolvió `BOLD_CUERPO_BASE` de 6 a 14 durante unos segundos, pisando la edición
en curso de esa sesión. El fichero en disco ya mostraba el valor correcto al comprobarlo de nuevo, de
modo que no quedó daño, pero confirma la regla de `CLAUDE.md` sobre releer inmediatamente antes de
escribir: un `cp` de una copia tomada minutos antes es exactamente el error que esa regla previene.

---

## §F158 — «En el dominio» no se entendía sin contexto: resumen y abstract aclarados

**Fecha:** 2026-09-09 · **Origen:** el autor, dos veces («¿qué quiere decir esto? No está claro» /
«no es claro decir "en el dominio", por favor ser más claro»)

El resumen y el abstract citaban «90,16 % en el dominio» sin que el lector supiera, en la primera
página del documento, qué es «el dominio»: la definición —corpus N=30, en inglés, del ámbito temático
AML/KYC— solo aparece en §4.1 y §5.3, muchas páginas después. Es una etiqueta interna del proyecto,
no un término que se explique por sí solo.

**Corregido en los dos, en el mismo commit y con el mismo contenido**, nombrando el corpus por lo que
es —«30 artículos en inglés del corpus del dominio AML/KYC»— en lugar de la etiqueta sola, y
distinguiendo explícitamente el corpus periodístico general del corpus del dominio en las dos
frases donde el resumen cita cifras de ambos.

**Con una condición que casi se rompe dos veces:** el resumen tiene un límite duro de 200 palabras
(`CLAUDE.md`). La primera redacción más clara subía a 205 y luego a 201; se ajustó dos veces —sin
perder la aclaración— hasta quedar en exactamente 200. La comprobación «resumen y abstract por
debajo de 200 palabras» lo verificó en cada intento.

**Y un efecto colateral que había que anticipar:** la comprobación «el idioma del corpus se comprueba,
no se supone» exige encontrar la frase literal «N artículos, M en español» en el resumen y el
abstract, para verificar que la composición de idiomas se declara con las cifras reales (105 de 120).
La primera redacción más clara rompía esa adyacencia textual. Reescrita para conservar «120 artículos,
105 en español» como frase contigua y añadir la aclaración del dominio alrededor, en lugar de
en medio.

---

## §F159 — Seis pasajes más describían los defectos corregidos como vigentes, y faltaba el «Corpus 3»

**Fecha:** 2026-09-09 · **Origen:** el autor, comprobando que la Figura 1 seguía describiendo el
defecto de Locations como presente; workflow `wf_800c741d-847` para un barrido exhaustivo

`§F154` y `§F157` corrigieron `§5.3.1` y su párrafo de correlación. El autor encontró que la nota
que precede a la Figura 1 seguía diciendo «sustituirlas exige volver a inferir, que es lo que hará
la re-corrida pendiente» — la re-corrida ya había pasado. Lancé el workflow que pidió el autor para
un barrido exhaustivo del resto del cuerpo, y confirmó **seis pasajes** más, los seis con confianza
alta o media y **verificados por un segundo agente con sesgo a refutar**, ninguno descartado:

1. **§3.3**, la cifra del 66,0 % de falsos positivos «según recoge la Figura 1… cubre los
   veintiséis grupos que sostienen la Tabla 7» — la Tabla 7 vigente es la adoptada, donde Locations
   ya está anotada; esa cifra es del consolidado publicado.
2. **§3.3**, la frase de cierre, «sustituirlas exige volver a inferir, que es lo que hará la
   re-corrida pendiente» — ya se hizo.
3. **Leyenda de la Figura 1** — atada a «los veintiséis grupos que sostienen la Tabla 7» en
   presente, cuando describe el consolidado publicado.
4. **Conclusión 7 de §7.1** — describía el mojibake en presente («el corpus N=120 almacena»), sin
   la salvedad de corregido que sí lleva la conclusión 6 vecina sobre Locations.
5. **§7.2, punto 7** («Fase 6», normalización de codificación) — proponía como trabajo futuro
   pendiente exactamente lo que ya se ejecutó.
6. **§7.2, punto 8** («Prioridad Alta», recuperación de Locations) — mismo defecto: proponía como
   pendiente una corrección ya aplicada antes de la re-corrida adoptada.

**Los seis, corregidos de forma aditiva**: se conservan todas las cifras y el análisis —las tasas
de F1 por artículo afectado, el 20,1 %/87 % del mojibake, el 66,0 % de los FP— cambiando el tiempo
verbal a pasado y añadiendo, donde faltaba, la referencia a que la corrección ya está hecha y a
`§5.3.1` como el sitio donde vive el resultado vigente. Los puntos 7 y 8 de §7.2 dejan de leerse
como trabajo futuro pendiente y pasan a declarar explícitamente «ya realizada»/«ya realizado»,
sin perder ninguna cifra de las que documentaban el defecto y su magnitud.

**Un detalle que el propio workflow señaló y que no era cierto**: un verificador reportó que
`results/COMPOSICION_FP_20260908/` «no existe físicamente», lo cual habría sido un hallazgo grave
—una fuente citada que no está—. **Comprobado por mi cuenta: sí existe**, con su
`composicion_fp_26_grupos.json`, cuyo propio campo `consolidado` declara `ANALISIS_CONJUNTO_20260907`
—el publicado—, confirmando exactamente la lectura del hallazgo. El error del verificador fue de
directorio de trabajo, no un hecho sobre el repositorio; se anota porque es la misma clase de
error que `§L71` lleva documentando: comprobar el resultado de un subagente, no darlo por bueno.

### Y un problema de estructura distinto, señalado también por el autor: faltaba el «Corpus 3»

§4.1 anuncia «tres corpus complementarios» y solo etiqueta dos, «Corpus 1» y «Corpus 2»; el tercero
(N=120) se describe cuatro párrafos después, bajo el encabezado `#### 4.1.2`, sin la etiqueta
paralela que el lector espera tras leer «tres». Añadido un párrafo breve «Corpus 3 — Real
Balanceado (N=120, Estudio Principal)» inmediatamente después del Corpus 2, con una frase de
resumen y remisión a §4.1.2 para el detalle — sin duplicar ni recortar el contenido que §4.1.2 ya
desarrolla.

## §F160 — Dos cifras para el mismo modelo y el mismo N confunden aunque ambas sean correctas: hay que dejar una sola vigente

**Fecha:** 2026-09-09 · **Origen:** el autor preguntó por qué el informe parecía dar dos cifras
distintas para `gemma4:12b-mlx_kb_rag` sobre N=120

### El incidente que lo disparó no era del informe, era mío

Al responder sobre este modelo cité, textualmente, `CURRENT-TASKS.md §1.187`: «el informe ya cita
las correctas (56,18 y 58,46)». Esa frase era cierta **cuando se escribió**, esa misma mañana,
**antes** de la decisión 1. Por la tarde la re-corrida adoptada (`ANALISIS_CONJUNTO_20260909_FIX`)
sustituyó a qué consolidado sostiene la Tabla 7, y esta pasó a dar **77,67 %/79,96 %** para el mismo
modelo. Repetí la cifra vieja sin la salvedad de fecha. El informe mismo no tenía el defecto —el
Anexo I marca 56,18/58,46 explícitamente como la corrida del consolidado publicado, con una sección
propia («Corridas múltiples del mismo modelo») que dice sin ambigüedad cuál es la de referencia—,
pero la confusión que le atribuí al informe era real y evitable: dos cifras correctas, sin la
diferencia de vigencia expuesta con la fuerza suficiente, generan la misma duda que un error.
Corregido con una nota fechada en `§1.187` y una fila nueva `§1.284` en `CURRENT-TASKS.md`.

### Y una segunda instancia, encontrada al buscar «problemas similares»: `gpt-oss:20b`, y esta sí era un error del informe

El apartado «Corridas múltiples del mismo modelo» (Anexo I, antes de la Tabla 20) afirmaba, sobre
`gpt-oss:20b`: «existen **dos mediciones del mismo experimento**... la de referencia es la
**primera** [2048 tokens de salida, 120 artículos]... mientras la referencia sea la primera, las
cifras de `gpt-oss:20b` de la Tabla 7 deben leerse con la reserva anterior». Esto describía el
estado **antes** de la decisión 1, cuando la única corrección disponible para `gpt-oss:20b` era un
re-run aislado (`gptoss_rerun_REMOTO`, 4096 tokens) mientras los otros doce modelos seguían a 2048.
**Nunca se actualizó cuando la re-corrida completa se adoptó.** Comprobado contra el manifiesto
vigente (`ANALISIS_CONJUNTO_20260909_FIX/merge_manifest.json`): la fuente de `gpt-oss:20b` es
`recorrida_20260908/gpt-oss_20b__N120/`, la misma campaña que los otros doce modelos, con
`max_tokens=4096` idéntico (verificado en su `run_config.json`). La «reserva de comparabilidad»
que el informe pedía leer junto a la Tabla 7 **ya no existe**: los trece modelos comparten
protocolo desde la re-corrida. La afirmación «la de referencia es la primera» es hoy sencillamente
falsa. `tools/verificar_informe.py` tampoco la detectaba: `DIVERGENCIAS_DECLARADAS['max_tokens']`
seguía declarando una divergencia que `c_protocolo` ya no encuentra desde que `MANIFIESTO` apunta al
consolidado adoptado — una declaración caducada que la propia comprobación 55 no capta porque mira
`FALLOS_DECLARADOS`, no este diccionario aparte.

### La corrección, y el principio general que deja fijado

Reescrito el apartado completo: se retira la Tabla 20 (ocho filas con el F1 de corridas
descartadas, replicando exactamente el patrón de esta sección) y se sustituye por una nota breve
que declara que los cuatro modelos tuvieron una re-ejecución parcial, por qué, y que la re-corrida
adoptada la resolvió sin dejar reserva pendiente. El punto metodológico de `nemotron-mini:4b`
—que el criterio fue la validez y no el resultado favorable— se conserva como anécdota de una
frase, sin imprimir las dos cifras históricas que ya no hacen falta para sostenerlo. Retirada
también la entrada `max_tokens` de `DIVERGENCIAS_DECLARADAS` en el verificador, con nota de por qué
ya no aplica.

**El principio, para no repetir esto**: cuando un benchmark y un N tienen más de una cifra correcta
en la historia del proyecto, el estudio presenta **una sola como vigente** — la última — y las
demás quedan como anécdota del proceso evolutivo, sin imprimirse en una tabla que invite a leerlas
como dos resultados entre los que elegir. La historia completa se conserva en los archivos
(`results/`, `benchmark.log`, los propios anexos ya existentes) y puede mencionarse en prosa; lo
que no debe ocurrir es que dos números con apariencia de resultado final convivan en el cuerpo del
informe. Ver `LEARNING §L78` y la actualización de `CLAUDE.md` del mismo día.

## §F161 — El párrafo del «hallazgo central» de §5.3.1 tenía tres cifras equivocadas, no solo redacción densa

**Fecha:** 2026-09-09 · **Origen:** el autor pidió simplificar el párrafo del ANOVA/Tukey/Levene/Friedman
y de correlación de §5.3.1, «sin perder significado»

Antes de simplificar, verifiqué cada cifra contra la Tabla 7 y el CSV del consolidado adoptado, por la
misma razón que motivó `§F160` unos minutos antes: un párrafo puede llevar tiempo sin tocarse mientras el
resto del documento avanza. Aparecieron tres discrepancias reales, no solo de redacción:

1. **«Nueve de los trece modelos mejoran»**: contando los signos de la columna «Δ RAG» de la Tabla 7,
   mejoran **once**, no nueve (solo `qwen3:8b` y `mistral-nemo:latest` empeoran).
2. **«Se anula o revierte en los de mayor capacidad (−0,54 y −0,18 puntos en los dos de 31B)»**:
   recalculado directamente del CSV consolidado (`ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv`),
   `gemma4:31b-cloud` mejora **+0,81** puntos y `gemma4:31b-mlx` mejora **+0,97**, ambos con RAG — positivos,
   no negativos, y coincidentes con la Tabla 7 al céntimo. La afirmación «se anula o revierte» no describe
   ningún dato vigente.
3. **Contradicción interna**: el mismo párrafo decía, dos frases antes, que la mejora «solo supera la
   corrección por comparaciones múltiples en `nemotron-mini:4b`» (**un** modelo), y más abajo que «solo dos
   [modelos] lo hagan de manera estadísticamente sólida». Ambas no pueden ser ciertas a la vez; la Tabla 7
   (columna «Δ significativo») confirma que es **uno**.

Las tres apuntan a la misma causa que `§F154`/`§F158`/`§F159`: un párrafo redactado en un momento anterior
del análisis (probablemente sobre una versión intermedia de la re-corrida, antes de fijar la Tabla 7
definitiva) que nunca se recontrastó cuando el cálculo final estuvo listo. A diferencia de esos hallazgos,
aquí las cifras en sí eran las equivocadas, no solo su encuadre temporal.

**Corregido junto con la simplificación pedida**: el párrafo se reestructuró en cinco unidades más cortas,
cada una abriendo con la pregunta que responde (significancia global, salvedad de diseño y prueba robusta,
hallazgo central, alcance de la correlación), sin perder ninguna cifra ni prueba estadística del original
—F, p, Tukey, Levene, Friedman, Spearman, Pearson y el control de retirar `nemotron-mini:4b`—, y corrigiendo
las tres cifras de arriba. Verificado con `tools/verificar_informe.py` tras dos rondas de ajuste: dos
comprobaciones (`c_tukey_recuento`, `c_levene`) leen frases con una redacción textual concreta por regex, y
la primera pasada de la reescritura introdujo, sin querer, saltos de línea manuales **dentro** de esas
frases (`"...de Levene\nsí detecta..."`), que el regex no salva porque exige un espacio literal y no
`\s+`. Ambos se corrigieron desplazando el salto de línea fuera de la frase exacta que cada comprobación
matchea. 56 comprobaciones, 0 fallos nuevos tras la corrección final.

## §F162 — El cuerpo del informe no menciona fechas de calendario del proceso; los anexos sí, porque son bitácora

**Fecha:** 2026-09-09 · **Origen:** el autor pidió, sobre el pasaje de §3.3 que ya se había verificado
correcto, que el cuerpo del informe no mencione fechas de calendario del proceso de trabajo

El autor había preguntado si el pasaje de §3.3 sobre el defecto de `Locations` era un residuo de la
generación `.md → .docx → PDF`. La investigación confirmó que no lo era: las tres capas coincidían,
correctamente, en texto ya corregido. Pero el autor añadió una regla nueva, más amplia: **el cuerpo
del informe (capítulos 1 a 7) no debe mencionar en qué fecha de calendario ocurrió cada corrección**,
aunque la corrección misma se declare. Es una extensión natural de `§F160`/`§F161`: si el estudio
presenta una sola cifra vigente por benchmark, tampoco tiene sentido anclar esa cifra a un día concreto
del proceso interno — el lector de una tesis no necesita saber que algo se corrigió «el 8 de
septiembre», solo que está corregido.

Consultado explícitamente si la regla alcanzaba también a los Anexos H e I (que `CLAUDE.md` establece
como registro histórico deliberado, con fechas que distinguen corridas), el autor confirmó que **no**:
la regla es solo para el cuerpo. Los anexos siguen siendo bitácora fechada, que es su propósito
declarado.

**Barrido del cuerpo (capítulos 1 a 7, antes de `## Anexos`)**: ocho menciones de fecha de calendario,
en §3.3 (dos), §4.1.2 (dos), §5.3 (una, «julio de 2026» sin día), §5.3.1 (una) y §7.1 (dos, puntos 7 y
8). Todas reescritas para conservar el significado sin la fecha —«el defecto está corregido en el
corpus» en vez de «corregido... desde el 8 de septiembre de 2026»; «(commit `5ff38f5`...)» en vez de
«(1 de septiembre de 2026, commit `5ff38f5`...)»—, sin perder ninguna cifra ni la secuencia lógica
(qué corrida sustituye a cuál y por qué). **Una fecha se conservó a propósito**: la cita bibliográfica
[19] («instantánea del 27 de julio de 2026» de la lista SDN de OFAC) no es una fecha de proceso, es la
fecha de una instantánea de una fuente externa que cambia con el tiempo — información necesaria para
que un lector pueda verificar qué versión del dato se citó, exigida por la propia norma de citación
que el informe sigue (IEEE). Retirarla habría dañado la trazabilidad de la cita, no la habría limpiado.

Verificado: 56 comprobaciones, 0 fallos nuevos, dentro de 25 páginas. Ninguna de las ocho reescrituras
tocó una frase que algún regex del verificador matcheara literalmente, así que no hubo que ajustar
`tools/verificar_informe.py`.

## §F163 — Retirada total de una anécdota con datos no verificables, a instancia expresa del autor

**Fecha:** 2026-09-09 · **Origen:** el autor, sobre la nota de «particularidad de procedencia» de §5.3

Al revisar el pasaje de §3.3 (`§F162`) apareció, en §5.3, una nota distinta con el mismo patrón de
fondo: «Una primera ejecución de este experimento reportó para `gemma4:31b` un F1 de 79,03 %... sus
datos por registro se perdieron por sobrescritura, de modo que no podía recalcularse». La nota
comparaba esa cifra con la corrida vigente (73,34 %) para argumentar que un defecto de puntuación
corregido en §4.4 apenas afectaba a este experimento — un uso metodológicamente razonable, pero
apoyado en un número que **no tiene datos crudos que lo respalden**.

El autor pidió, con calificación explícita de gravedad, retirar **totalmente** cualquier mención a
datos que no pudieran recalcularse o confirmarse: «solo debe mencionarse datos reales para los cuales
existe evidencia real». Es una regla distinta de `§F160`/`§F161` (que trata de no imprimir cifras
superadas cuando sí hay evidencia de ambas) y distinta también de la excepción que ya existe en
`TODO-INFORME-FINAL.md §10` para las dos filas «aritméticamente imposibles» de `BENCHMARKS.md» (que
se marcaron NO VERIFICABLES y se conservaron fuera del cuerpo del informe, no se citaron dentro de
él). Aquí el defecto era más directo: la cifra sin evidencia **sí estaba dentro del cuerpo**.

**Retirado el párrafo completo** (dos frases, con sus dos guiones largos), sin dejar ninguna mención
de la cifra ni de la corrida perdida. Comprobado antes de retirar que ningún otro pasaje del informe
cita 79,03 % ni 73,34 % — no había cross-reference que reparar. La conclusión del análisis de
sensibilidad que sí queda («El resultado no depende, por tanto, de unos pocos textos extremos») no
dependía de esta nota: es un argumento aparte, sobre longitud de artículo, no sobre convención de
puntuación.

**Efecto colateral, declarado y no oculto**: el párrafo retirado tenía dos guiones largos, así que el
recuento del cuerpo bajó de 90 a 88 mientras los tres `.docx` — renderizados por Claude Desktop antes
de esta corrección — se quedan en 90 hasta la siguiente pasada. Declarado en `FALLOS_DECLARADOS`
(«guiones largos frente a») y en `RETIRADAS` (para que la comprobación confirme, cuando Claude Desktop
propague, que la anécdota no sobrevive en ningún entregable). Verificado: 56 comprobaciones, 0 fallos
nuevos tras declarar, dentro de 25 páginas.

## §F164 — Enriquecimiento del marco teórico (reparo 4 del profesor guía): arquitectura y estadística adicional

**Fecha:** 2026-09-09 · **Origen:** el autor, retomando el reparo 4 del profesor guía («marco
conceptual pobre, sin comparación de alternativas»), pidió enriquecer el capítulo 2 con conceptos
usados después en el trabajo pero nunca introducidos teóricamente

### Qué faltaba

El capítulo 2 comparaba familias de técnicas de NER, aprendizaje en contexto, RAG y entornos de
ejecución, y cerraba con la validación estadística (ANOVA, Tukey HSD, intervalos de confianza,
análisis de sensibilidad). Pero el resumen y §3 anuncian, como aportes de arquitectura, una
**arquitectura pub/sub multihilo, concurrencia adaptativa (AIMD) y capa Factory/Facade** — ninguno
de los tres tenía fundamento teórico en el capítulo 2, solo la descripción de su implementación en
§3. Y §5.3.1 usa, sin haberlas introducido antes, las pruebas de **Levene** (homocedasticidad),
**Friedman** (medidas repetidas) y los coeficientes de **Pearson**/**Spearman** (correlación).
Ambos vacíos son exactamente el tipo de detección que el reparo 4 señalaba: conceptos que el cuerpo
usa sin que el marco teórico los sostenga, y sin comparar cada uno contra su alternativa directa —
el criterio que el propio capítulo 2 se propone aplicar desde su primer párrafo.

### Qué se añadió, y el principio de no duplicar

**Nueva sección `### 2.4 Arquitectura de ejecución concurrente y aislamiento de proveedores`**
(441 palabras), con tres decisiones de diseño comparadas cada una contra su alternativa más directa:
pub/sub frente a un pipeline síncrono; AIMD frente a un número fijo de consumidores y frente a un
ajuste multiplicativo en ambos sentidos, citando a Chiu y Jain [26] (ya en la bibliografía, usada
antes solo para la cifra sin el fundamento); y Factory/Facade frente a ramificar el código llamador
por proveedor. Esto desplaza `### 2.4 Validación estadística...` a `### 2.5` y `### 2.5 Estado del
arte...` a `### 2.6`; comprobado que ningún cross-reference citaba `§2.4` o `§2.5` por número antes
del cambio (solo `§2.1` y `§2.3`, intactas).

**Extensión de `§2.5` (232 palabras)**: dos párrafos nuevos sobre el supuesto de independencia y
homocedasticidad del ANOVA (con Friedman y Levene/Brown-Forsythe como respuesta a cada uno) y sobre
Pearson frente a Spearman como coeficientes de correlación, con su compromiso respectivo.

**Extensión de `§2.1` (143 palabras)**: el criterio de coincidencia entre entidad extraída y de
referencia, comparando coincidencia exacta, coincidencia por tokens y el emparejamiento difuso por
distancia de Indel que el trabajo adopta — el «algoritmo de comparación» que §3.3 aplica sin que el
marco teórico lo sostuviera antes.

**Y, para no duplicar la misma teoría dos veces, se recortó donde ya estaba solo aplicada**: el
párrafo de §5.3.1 sobre Levene/Friedman perdió la explicación de qué son y por qué hacen falta (eso
vive ahora en §2.5), conservando únicamente las cifras del estudio y una remisión («introducida en
§2.5»); ahorro de 31 palabras. El párrafo de §3.3 sobre la distancia de Indel perdió su definición
(ahora en §2.1), conservando la aplicación (biblioteca, fórmula, umbral); ahorro de 25 palabras.
Ningún dato ni cifra se perdió en ninguno de los dos recortes — se verificó que ambos siguen
respaldando exactamente las mismas conclusiones que antes.

### Presupuesto de páginas, y lo que queda pendiente

El límite institucional de 25 páginas se estima por palabras del cuerpo (`tools/verificar_informe.py`,
`c_extension`); antes de este cambio el margen era de 891 palabras, y tras sumar las adiciones (816
palabras) y restar los recortes (56 palabras) queda en aproximadamente 121 palabras — **231 de
margen si se resta lo que aún falta declarar**. El autor pidió además enriquecer con más conceptos
de NLP/NER/LLM, algoritmos y computación distribuida, y sugirió sacrificar contenido de los anexos
para hacer sitio; dado que los anexos están explícitamente excluidos del límite de 25 páginas
(`CLAUDE.md`), recortarlos no libera presupuesto del cuerpo, así que antes de seguir ampliando se
preguntó al autor cómo prefiere resolver esa tensión. Ver la pregunta en el mismo turno.

### Verificación

Dos regresiones propias, corregidas antes de declarar nada: el trimado de §5.3.1 reintrodujo, dos
veces, un salto de línea manual **dentro** de la frase exacta que `c_levene` matchea por regex
(mismo defecto que `§F161`) — corregido desplazando el salto fuera de la frase ambas veces. Los
paréntesis restantes son propagación pendiente a los tres `.docx`: siete párrafos nuevos, una
sección nueva en el índice, y una negrita que bajó de 9 a 8 por casualidad (declarada a nombre de
Claude Desktop, que es quien mantiene `BOLD_CUERPO_BASE`, no se toca aquí). Verificado: 56
comprobaciones, 0 fallos nuevos (32 declarados, todos asignados), dentro de 25 páginas.

### Adenda: el autor pidió reducir anexos «porque el total son 25 páginas», y la guía institucional dice otra cosa

Pedido de continuar el enriquecimiento, el autor sugirió además reducir los Anexos, entendiendo que
el límite de 25 páginas es del documento completo, y pidió confirmarlo contra
`Instrucciones Informe Final de Tesina/tesinas-finales-2026.pdf` (guía del programa, Dr. Monge y
Dr. Visconti). **Extraído el texto de las 14 páginas con `pypdf`** (no había `pdftotext` ni
`poppler`, pero el venv del proyecto trae `pypdf`), la diapositiva 16 dice literalmente:
«OBSERVACIÓN: Máximo 25 páginas **sin anexos**», y la diapositiva 25 (`d) Anexos`) añade que estos
«no debiera[n] sobrepasar 25 páginas **adicionales** al cuerpo del documento (tb. 25 páginas)». Es
decir: el límite es 25 + 25, exactamente lo que `CLAUDE.md` ya documentaba, no un total de 25 que
obligara a recortar anexos para dar espacio al cuerpo. Medidos con la misma heurística de palabras
que `c_extension`, los Anexos de hoy son ~5 928 palabras, ~8,7 páginas estimadas — lejos de su
propio límite. **No se recortó ningún Anexo por presupuesto de páginas**, porque la premisa era
incorrecta y verificarla contra la fuente antes de actuar es la misma disciplina de `§F154` y
compañía, aplicada aquí a una instrucción del autor y no a un hallazgo de auditoría.

Lo que sí se hizo, siguiendo la alternativa que el autor había elegido (recortar prosa del cuerpo
que es más detalle de implementación que narrativa): el listado de código de `LLMProvider` (§3.2) se
trasladó al nuevo `Anexo A.1`, y se recortó una frase del párrafo de AIMD ya cubierta por la teoría
de la nueva `§2.4`. Margen recuperado: de 121 a 178 palabras. Se barrió además el documento entero
en busca de otras menciones de «datos que no pueden corroborarse ni recalcularse», por si `§F163`
no había sido la única — no apareció ninguna otra.

## §F165 — Segunda ronda de enriquecimiento: embeddings y bases de datos vectoriales en §2.3

**Fecha:** 2026-09-09 · **Origen:** el autor, tras confirmar que el margen de `§F164` (178 palabras)
era suficiente, pidió una ronda más («un cambio: sí enriquecer más el marco teórico»)

Ambas variantes de RAG que compara `§2.3` («por diccionario» y «contextual o de conocimiento»)
dependen de un mecanismo que el capítulo nunca explicaba: cómo se decide qué recuperar. El cuerpo
ya usa dos términos sin definirlos — «similitud vectorial» en §5.6 y `ChromaDB` (citado [32]) solo
en el Anexo D, como nombre de biblioteca sin concepto detrás. Añadido un párrafo de 111 palabras en
`§2.3`, después del párrafo que cierra la comparación de variantes RAG: qué es un **embedding**
(representación vectorial que aproxima textos semánticamente próximos), por qué reduce la
recuperación a una búsqueda por vecino más próximo, y qué papel cumple una **base de datos
vectorial** (ChromaDB en este trabajo) para hacer esa búsqueda eficiente a la escala del estudio.

**Presupuesto**: el margen bajó de 178 a 74 palabras — la estimación de páginas queda en 24,89 de
25, el margen más ajustado de toda esta ronda de enriquecimiento. Se avisa expresamente: **cualquier
adición más exige, antes, otro recorte de tamaño equivalente en el cuerpo**, porque a 74 palabras el
margen ya no absorbe ni un párrafo corto. Verificado: 56 comprobaciones, 0 fallos nuevos (41
declarados, 16 vigentes), dentro de 25 páginas — declarada la propagación pendiente a los tres
`.docx`, como en las rondas anteriores.

## §F166 — El párrafo de §3.3 sobre `Locations` era largo y llevaba fechas: el autor temió que un comité lo leyera como una mala decisión sin resolver

**Fecha:** 2026-09-09 · **Origen:** el autor, releyendo el pasaje ya verificado en `§F162`, pidió
comprobar si seguía siendo importante y, si no, retirarlo o al menos aclarar la conclusión final

### El problema no era de contenido, era de énfasis y de orden

El párrafo (440 palabras) explicaba correctamente el defecto de anotación de `Locations`, su causa,
su efecto y su corrección — todo verificado y correcto en turnos anteriores (`§F53`, `§F154`,
`§F162`). Pero lo hacía en el **orden equivocado para un lector que evalúa**: abría con «afecta a
la comparabilidad de las cifras absolutas», seguía cuatro frases de mecanismo técnico, y solo al
final —tras el 66,0 % de falsos positivos— decía que ya estaba corregido y no afectaba a la Tabla 7
vigente. Un comité que lee rápido puede quedarse con la primera impresión (una limitación de
medición) antes de llegar a la última frase (ya resuelta, sin efecto en los resultados). El autor
señaló además que «localizaciones» no quedaba claro sin contexto: es la tercera categoría de
entidad (lugares geográficos), y el párrafo la usaba sin remitir a donde se define.

### La corrección: adelantar la conclusión, clarificar el término, mover el detalle al anexo

Reescrito de 440 a 240 palabras. **Abre** con la conclusión («ya está corregido y no afecta a ningún
resultado vigente de este informe: se documenta aquí por integridad de la medición»), en vez de
dejarla para el final. **Aclara** que las localizaciones son «lugares geográficos, la tercera
categoría de §2.1» — remite a la definición añadida en `§F164`, que en su momento no existía. **Se
recorta** el detalle histórico que no cambia la conclusión: las 545 localizaciones recuperadas en
119/120 registros, «sustituirlas exigía volver a inferir», la mecánica completa de la medición
restringida — todo eso ya vive en el Anexo I, y el párrafo del cuerpo remite allí en una frase en
vez de repetirlo. Se **conservan** los dos hechos que sí son necesarios para la integridad de la
medición: que el defecto era de la cadena de preparación de datos y no de la anotación de origen
(exculpa a CoNLL-2002), y la cifra exacta del 66,0 % con su fracción (12 852 de 19 464), porque dos
comprobaciones mecánicas (`c_figuras`, la que ata la Figura 1 al artefacto de composición) exigen
justamente esa fracción y una referencia con artículo («la Figura 1») — verificado que ambas siguen
en `ok` tras la reescritura, no solo que el texto se leyera bien.

**No se tocó la Figura 1** ni su leyenda (ya corregida en `§1.282`): sigue siendo evidencia real de
un defecto resuelto, y removerla habría exigido renumerar la Figura 2. Verificado: 56
comprobaciones, 0 fallos nuevos (41 declarados, 16 vigentes), dentro de 25 páginas. El recorte
liberó además 266 palabras de presupuesto (el margen pasó de 74 a 340), revirtiendo la crisis de
`§F165`.

## §F167 — Toda la ronda de enriquecimiento del marco teórico (piezas 31-36) llegó a los tres `.docx`

**Fecha:** 2026-09-09 · **Origen:** monitoreo de rutina del equipo remoto; se detectó que
Claude Desktop había renderizado una `_v15` (22:52, tras la `_v14` de las 20:16)

Trece declaraciones de `FALLOS_DECLARADOS` dejaron de tapar ningún fallo, todas en la misma
sesión de monitoreo: los siete párrafos nuevos del capítulo 2 (§2.1, §2.3, §2.4 completa, §2.5),
el recorte de §3.3 sobre `Locations`, la sección nueva del Anexo A.1 con el código de
`LLMProvider`, y el recuento de resaltes del cuerpo. Las dos últimas se resolvieron **entre dos
ejecuciones consecutivas del verificador** en este mismo turno — señal de que Claude Desktop
seguía trabajando en vivo mientras se comprobaba, el mismo patrón ya visto en `§1.287`/`§1.288`.
Comprobado antes de retirar cada una: ninguna aparece ya como «párrafo ausente» ni como «frase
retirada superviviente» en los tres entregables. No se tocó ningún `.docx`, el PDF ni
`doc/versions/informe_final/`; solo se editó `tools/verificar_informe.py` (retirar
declaraciones) y `CURRENT-TASKS.md` (registro, por *append*). `BOLD_CUERPO_BASE` sin tocar.

Verificado: 56 comprobaciones, 0 fallos nuevos (5 declarados, 4 vigentes), dentro de 25 páginas.
Con esto, todo el trabajo de enriquecimiento del capítulo 2 (`§F164`/`§F165`/`§F166`) queda
completamente propagado a los tres entregables.

---

## §F168 — Citas de origen para Pearson y Spearman, y anexo de reproducción de la correlación

**2026-09-12.** El autor pidió las referencias de base para las dos cifras de correlación de
§5.3.1 (Spearman −0,0879, p=0,7752; Pearson −0,4816, p=0,0956), documentarlas en el `.md` y
documentar su procedencia en los anexos.

**Las citas.** El párrafo teórico de §2.5 explicaba Pearson y Spearman sin citar su origen, a
diferencia de Tukey `[25]` y AIMD `[26]` en el mismo capítulo. Añadidas dos entradas a la
bibliografía, verificadas por DOI (el sitio de destino bloquea el lector automático en ambos
casos —Royal Society Publishing con 403, JSTOR con un reto de Cloudflare—, así que se acredita
por resolución del DOI vía Crossref, el mismo criterio que el proyecto ya aplica a ACM):

- `[40]` K. Pearson, *Note on Regression and Inheritance in the Case of Two Parents*, Proceedings
  of the Royal Society of London, vol. 58, pp. 240-242, 1895. DOI `10.1098/rspl.1895.0041`.
- `[41]` C. Spearman, *The Proof and Measurement of Association Between Two Things*, American
  Journal of Psychology, vol. 15, no. 1, pp. 72-101, 1904. DOI `10.2307/1412159`. La página final
  (101) no la da Crossref ni OpenAlex, que solo registran la primera; confirmada por una segunda
  fuente (la propia bibliografía de Wikipedia sobre el coeficiente).

Citadas donde ya se explicaban los dos coeficientes (§2.5), no de nuevo en el párrafo de
resultados de §5.3.1, siguiendo el mismo patrón que Tukey: la teoría cita, el resultado remite a
la teoría por número de sección.

**El anexo.** Nuevo `Anexo J`, después del Anexo I, con la procedencia exacta de las dos cifras:
el script `tools/robustez_estadistica.py`, que las calcula con `scipy.stats.pearsonr` y
`scipy.stats.spearmanr` sobre el CSV consolidado, y las persiste en
`results/ROBUSTEZ_ESTADISTICA_20260909_FIX/robustez.json`. Incluye la Tabla 20, con el análisis de
sensibilidad ya citado en el cuerpo (§5.3.1: retirar `nemotron-mini:4b` cambia el signo del
Pearson) pero nunca antes tabulado para los trece modelos: los otros doce, retirados uno a uno,
dejan el coeficiente entre −0,47 y −0,62, siempre con el mismo signo. Los trece valores se copiaron
literalmente del artefacto JSON, no se recalcularon a mano.

**Verificado antes de comprometer**: `el cuerpo cabe en el limite de 25 paginas` sigue en `ok`
(la estimación por palabras no se resiente; el Anexo J vive fuera del cuerpo), `referencias a
Anexo X y a Tabla N con destino existente` y `bibliografía contigua` en `ok`, y `la correlacion de
capacidad reproduce desde su artefacto` sigue en `ok` tras añadir la Tabla 20 —confirma que sus
cifras son las del JSON y no una transcripción manual—. Las 21 divergencias nuevas entre el `.md`
y los tres `.docx` (cuatro párrafos, una tabla y dos entradas de bibliografía, por tres
entregables) son la propagación pendiente de siempre, declaradas en `FALLOS_DECLARADOS` a nombre
de este hallazgo. Añadida la pieza correspondiente al encargo de Claude Desktop.

**Adenda (mismo día, tras verificación con workflow independiente).** Un workflow de cuatro
agentes con refutación escéptica reverificó las dos citas y el propio commit. Las citas de
Pearson y Spearman se confirman correctas —DOI, autor, revista, volumen, páginas y año coinciden
en Crossref y en una segunda fuente independiente cada una (OpenAlex y, para Spearman, la
bibliografía de Wikipedia)—, con solo un matiz tipográfico de estilo en ambos títulos (mayúsculas
y el numeral «VII.» del catálogo de la Royal Society), no un error de fondo. El diff del commit
`77bfd19` se confirmó línea por línea contra `git show`, y su presencia en `origin/main` con un
`git fetch` fresco. **Encontró un error real**, menor pero genuino: el Anexo J citaba la ruta del
artefacto como `results/ROBUSTEZ_ESTADISTICA_20260909_FIX/robustez.json`, que no existe en la raíz
de este repositorio — el fichero vive en `repos/ner-llm-entity-benchmark/results/...`, el mismo
prefijo que ya usa `tools/verificar_informe.py` internamente. Corregida la ruta en el `.md` y en el
encargo de Claude Desktop. El contenido citado del JSON —las cifras y las trece filas de la Tabla
20— ya era correcto; solo la ruta estaba incompleta. Verificado de nuevo: 56 comprobaciones, 0
fallos nuevos.

---

## §F169 — Cuatro citas más para métodos nombrados sin origen: ANOVA, Friedman, Levene/Brown-Forsythe, Cohen

**2026-09-12.** A petición del autor, un segundo workflow (5 agentes + refutación escéptica) buscó
citas de origen para otros métodos nombrados en el cuerpo sin cita, mismo patrón que motivó `§F168`.
Resultado, con veredicto SOBREVIVE en cada refutación salvo uno:

- **ANOVA**: recomendado R. A. Fisher, *Statistical Methods for Research Workers*, Oliver & Boyd,
  1925 (no la nota de 1918 sobre varianza, que es la base matemática y no el procedimiento; el
  patrón de cita ya establecido con Tukey es citar el procedimiento, no su antecedente teórico).
  Sin DOI (libro pre-DOI); URL de Open Library verificada (`OL1153861W`, primer año de publicación
  1925 confirmado).
- **Friedman (1937)**: confirmada sin ajustes. DOI `10.1080/01621459.1937.10503522`, verificado por
  Crossref y OpenAlex, con una fe de erratas de 1939 correctamente distinguida y no confundida con
  la referencia primaria.
- **Levene (1960)** y **Brown-Forsythe (1974)**: ambas confirmadas. Levene es un capítulo de libro
  pre-DOI (*Contributions to Probability and Statistics*, ed. Olkin, Stanford University Press);
  verificado por registro MARC de la Library of Congress y el índice del propio libro, con el rango
  de páginas 278-292 corroborado por tres fuentes independientes en la reverificación. Brown-Forsythe
  tiene DOI `10.1080/01621459.1974.10482955`, coincidencia exacta en Crossref, y se descartó
  explícitamente la confusión clásica con su otro artículo homónimo de 1974 sobre igualdad de
  medias (ese en *Technometrics*, no en JASA).
- **Cohen (1988)**: confirmada. *Statistical Power Analysis for the Behavioral Sciences*, 2.ª ed.,
  Lawrence Erlbaum Associates — verificado por registro LOC/MARC (LCCN 88012110) y por el uso real
  de la tabla de convenciones (pequeño/mediano/grande) en la literatura, que remite a esta edición y
  no a la de 1969 (Academic Press), cuyo contenido es distinto.
- **Levenshtein**: **no se añade**. La refutación **corrigió** el año propuesto (1966 → 1965 para el
  volumen 10, con evidencia de índices de revista escaneados en archive.org: año = 1955 + volumen,
  sin excepciones en ocho puntos de control) y dejó sin resolver el número de fascículo (Wikipedia
  dice 8, OpenAlex dice 4, sin un tercer árbitro). Con un dato corregido y otro en disputa, no se
  cita hasta que el autor decida o aparezca una tercera fuente.

**Decisión de presupuesto de páginas (el autor, vía pregunta explícita):** añadir las cuatro
confirmadas y buscar compensación antes de comprometer. Revisado: el «recorte de tamaño equivalente»
que `CLAUDE.md` describe para un desbordamiento de página es un **ajuste de estilo en el `.docx`**
(espaciado de encabezados, interlineado, cuerpo de letra de bloques de código hasta 7 pt) — un lote
de la competencia de Claude Desktop al maquetar, no un recorte de palabras en el Markdown. Cazar un
recorte de contenido equivalente en el `.md` habría sido anticiparse a esa orden de prelación
(estilo antes que texto) sin necesidad. Se añadieron las cuatro citas (5 entradas de bibliografía:
`[42]`-`[46]`) sin recortar prosa, y se declara aquí el riesgo para que Claude Desktop lo tenga
presente al maquetar: `+139` palabras sobre el cuerpo, margen de la estimación por palabras baja a
128 (24,81 páginas estimadas), y la medición real anterior (`§1.298`/adenda) ya estaba en 25 de 25
sin margen — es probable que esta adición exija el ajuste de estilo antes de dar el entregable por
bueno. Verificado: 56 comprobaciones, 0 fallos nuevos (38 declarados, 15 vigentes), `ok` en el
límite de 25 páginas por la estimación de palabras.

---

## §F170 — Retirada la Figura 1 (composición de FP), a petición expresa del autor

**2026-09-12.** El autor pidió, de forma explícita y sin condicionarlo a análisis previo
(«definitivamente eliminar»), retirar del cuerpo el gráfico de la Figura 1 (composición de los
falsos positivos del consolidado publicado, previa a la corrección de `Locations`) y su leyenda.
En el mismo encargo pidió **analizar y anotar como candidatas**, sin ejecutar todavía, otras tres
cosas: referencias a corridas anteriores sin evidencia verificable, anécdotas de defectos ya
resueltos (nombró el caso de `Locations`), y una duda de terminología (¿«ubicaciones» en vez de
«localizaciones»?). Esta entrada cubre lo primero, ejecutado; `§L80` cubre las candidatas, sin
ejecutar.

**Tensión con la política del proyecto, resuelta y no ignorada.** `CLAUDE.md` protege exactamente
este tipo de contenido bajo «Integridad de la medición», una sección que existe **porque** ocultar
un defecto de medición ya le costó caro al proyecto una vez (`§F53`). Antes de ejecutar, se
distinguió qué de la Figura 1 **afirma** (una interpretación, prescindible del cuerpo) y qué
**atestigua** (los datos y el defecto en sí, que el Corolario de `CLAUDE.md` exige conservar):

- **Lo que se retira** es la figura y su leyenda **del cuerpo**: una representación visual de un
  estado histórico ya corregido, que el autor considera que no aporta a la lectura del informe hoy.
- **Lo que se conserva, íntegro y sin tocar:** el Anexo I (que documenta el defecto completo, con
  sus cifras y la corrección), el script `generar_figuras_informe.py` que sigue generando la
  imagen (por si se necesita en el futuro), el artefacto `COMPOSICION_FP_20260908/` que la alimenta,
  y **la fracción exacta en prosa** («66,0 %», «12 852 de 19 464») en §3.3, que sigue siendo
  necesaria porque documenta el propio defecto de medición — eso no es narrativa prescindible, es la
  integridad de la medición que `CLAUDE.md` exige, y el autor no pidió retirarla, solo la figura.
- Es decir: se retiró la ilustración, no la evidencia. Con eso, la tensión con `CLAUDE.md` no se
  ignoró: se resolvió aplicando su propio Corolario (lo que afirma se ajusta a lo que el autor
  decide; lo que atestigua sigue disponible para quien lo pida).

**Mecánica de la retirada, con la renumeración que exige:**

1. Retirados el `![...]` y la `_Figura 1. ..._` de §3.3 (imagen `falsos-positivos.png` y su
   leyenda), y la referencia colgante «(la Figura 1 lo ilustra)» en la prosa de al lado —sin tocar
   la fracción 66,0 % / 12 852 de 19 464 que la acompaña—.
2. La única figura restante del cuerpo (el efecto del KB RAG, antes «Figura 2») se renumeró a
   **Figura 1**: la imagen, su leyenda y la frase que la cita en §5.3.1 («La Figura 2 recoge...» →
   «La Figura 1 recoge...»). Necesario porque `c_figuras` exige numeración contigua desde 1.
3. En `tools/verificar_informe.py`: renombradas las etiquetas de las comprobaciones que hablaban de
   «Figura 2» (ahora Figura 1) y de las que hablaban de «la Figura 1» vieja (ahora sin figura que
   nombrar, renombradas a «la composición de FP (§3.3/§7.2) reproduce desde el artefacto»). **La
   lógica de verificación no cambió**, solo las etiquetas: sigue comprobando que la fracción en
   prosa, el script y el artefacto coincidan, aunque ya no haya una figura que dibujarlos.
4. El script de figuras y el artefacto **no se tocaron**: siguen generando la imagen (por si se
   necesita reincorporar o consultar), solo dejó de incrustarse en el Markdown.

**Verificado tras el cambio**: `figuras numeradas... (2 elementos)` en `ok` (1 leyenda + 1 imagen,
numeración contigua desde 1); `Figura 1 coherente con la Tabla 7` en `ok` (la que era Figura 2); `la
composicion de FP (§3.3/§7.2) reproduce desde el artefacto` en `ok` (la cifra en prosa sigue
correcta); `referencias a Anexo X y a Tabla N` en `ok` (nada quedó colgando). 56 comprobaciones, 0
fallos nuevos.

**Efecto en el presupuesto de páginas**: neto **positivo** para una vez — la figura y su leyenda
sumaban más palabras/espacio que lo que costaron los ajustes de referencia, así que esta retirada
compensa parte de lo añadido por `§F169` en el mismo día.

---

## §F171 — La integridad de la medición se acota a partir del 8 de septiembre; §3.3 comprimido

**2026-09-12, mismo día que `§F170`.** El autor, tras leer la justificación de por qué no se tocó
la fracción de FP al retirar la Figura 1, preguntó directamente: **¿qué protege esa regla, y es
correcto seguir protegiéndolo así?** Le preocupaba que el informe se vea confuso mencionando
corridas anteriores erróneas y defectos ya resueltos (nombró `Locations` y el *mojibake*), cuando
hay una re-corrida completa y limpia desde el 8 de septiembre.

**Análisis, antes de tocar nada.** La regla de `CLAUDE.md` nació de un incidente real (`§F53`,
`§L44`): un defecto sobrevivió dos meses sin detectarse porque las cifras eran internamente
coherentes. Lo que protege, en el fondo, es que una corrección **no borre su propio rastro** — no
que el cuerpo dedique un párrafo largo o una figura a cada defecto ya cerrado. Esas son dos cosas
distintas que la redacción original de la regla no separaba con claridad, y el autor tenía razón en
señalarlo.

**Decisión del autor, con una precisión de fecha exacta**: la integridad de la medición rige
**desde el 8 de septiembre de 2026 en adelante** — la fecha de la re-corrida vigente. Todo defecto
anterior a esa fecha es historia cerrada, no medición vigente, y el cuerpo solo necesita declarar
que existió y remitir al anexo, sin desarrollar su mecánica. Ejecutado:

1. **`CLAUDE.md`** (sección «Integridad de la medición»): añadida una precisión fechada que fija
   el corte del 8 de septiembre, autoriza comprimir o retirar del cuerpo los temas de defectos
   anteriores a esa fecha cuando el límite de 25 páginas aprieta, y dice explícitamente que **no**
   toca el resto de la sección (declarar la corrida vigente, comprobar categorías contra el vacío,
   verificar el idioma siguen siendo obligatorios). Los anexos (H, I) **no se tocan** por esta
   precisión — el autor pidió esperar indicaciones del profesor guía antes de recortarlos.
2. **§3.3, párrafo de `Locations`**: comprimido de ~240 palabras a dos frases. Se conserva lo que
   la integridad de la medición exige —que existió, que ya no afecta a ningún resultado vigente, la
   fracción exacta **66,0 %** / 12 852 de 19 464, y la remisión al Anexo I—; se retira el desarrollo
   del mecanismo (por qué CoNLL-2002 sí anota localizaciones, cómo puntuaba el evaluador, etc.), que
   ya vive completo en el Anexo I.

**Verificado**: `la composicion de FP (§3.3/§7.2) reproduce desde el artefacto` sigue en `ok` (la
fracción exacta sobrevivió la compresión); `la conclusion 1 usa la agregacion declarada en §3.3` en
`ok`. Añadida una frase del párrafo viejo a `RETIRADAS` («sin ninguna forma de acertar en ella») y
declarada en `FALLOS_DECLARADOS` la divergencia de guiones largos que la compresión produjo (el
`.md` bajó de 93 a 92; ya había ocurrido una vez antes con este mismo párrafo, `§F166`). 56
comprobaciones, 0 fallos nuevos (53 declarados, 20 vigentes).

**Lo que queda pendiente, y es del autor**: si conviene aplicar el mismo criterio a las otras
candidatas que `LEARNING §L80` ya había documentado sin ejecutar (la cifra sin evidencia de §7.1
conclusión 6, las anécdotas de §7.2 puntos 7 y 8) es una decisión aparte, no incluida en este
cambio — el autor no la pidió ejecutar hoy, solo la de `Locations`.

---

## §F172 — Ejecutadas las tres candidatas de `LEARNING §L80`, y una referencia obsoleta encontrada de paso

**2026-09-12, mismo día que `§F170`/`§F171`.** Tras la precisión de fecha en `CLAUDE.md` (la
integridad de la medición rige desde el 8 de septiembre en adelante) y la pregunta del autor sobre
si una nueva corrida resolvería el problema de fondo —respondida: no, porque la Tabla 7 ya procede
de una sola corrida unificada del 8 de septiembre, y el asunto es narrativo, no de datos—, el autor
confirmó: **«Sí por favor, documentar extensamente lo realizado»**, autorizando ejecutar las tres
candidatas que `LEARNING §L80` había dejado sin tocar. Esta entrada documenta cada una.

### 1. §7.1, conclusión 6 (línea ~539): retirada la cláusula sin evidencia

Se retiró, dentro del párrafo de la conclusión sobre el KB RAG, la comparación con «el dict-RAG
(v1.0), que en un sondeo exploratorio N=5 sobre el mismo modelo, **no persistido en `results/`**,
degradó el F1 hasta 0.2367 (−57,8 % respecto de su propio baseline), degradación confirmada después
en la corrida histórica N=120 previa a la re-corrida, donde ese mismo modelo caía de 0.3611 a
0.3113». El propio texto admitía que el N=5 no tenía datos guardados que lo respaldaran, y la
segunda cifra remitía a una corrida ya superada. **Se conservó** el resto del párrafo íntegro: el
hallazgo principal (KB RAG estadísticamente significativo en un modelo, marginal en los de mayor
capacidad) y la mención de la correlación ρ = −0,09, p = 0,775 (una cita redondeada, no la que
exige `c_correlacion` — esa vive en §5.3.1 y el Anexo J con cuatro decimales, y no se tocó).

### 2. §7.2, punto 7 (mojibake): comprimido de ~110 a ~35 palabras

De «Normalización de codificación del corpus y re-evaluación: ya realizada. Sobre el consolidado
publicado, el corpus N=120 almacenaba los nombres con *mojibake*... [detalle completo de las cuatro
cifras de rango de efecto y la mecánica de la corrección]» a: se corrigió antes de la re-corrida del
8 de septiembre, verificado con `tools/analisis_mojibake.py`, con remisión al Anexo H para el
detalle. El Anexo H.3 (que tiene las cuatro cifras de rango y la Tabla 18) **no se tocó**.

### 3. §7.2, punto 8 (`Locations`): comprimido de ~130 a ~40 palabras, con cuidado de una comprobación mecánica

Mismo criterio que el punto 7. **Cuidado especial aquí**: la comprobación `la composicion de FP
(§3.3/§7.2) reproduce desde el artefacto` (`§F168`/`§F170` la renombraron, antes «Figura 1»)
exige literalmente la frase «procede el 66,0 % de los falsos positivos» en algún lugar de §7.2 —
verifica la cifra en **dos** apariciones independientes (§3.3 y §7.2) contra el mismo artefacto. La
compresión conservó esa frase exacta; verificado que la comprobación sigue en `ok` después del
cambio, no se asumió.

### Hallazgo de paso: una referencia cruzada quedó obsoleta, y no por esta sesión

Revisando qué más citaba «§7.2, punto 7» por número antes de comprimirlo, apareció el **Anexo H.4**
(«Cómo debe repararse»), que decía: «...la corrección exigiría re-ejecutar el estudio completo. Se
documenta por tanto como limitación (§5.3.1) **y como línea de trabajo futuro** (§7.2, punto 7)».
Eso es **falso hoy**: la re-corrida del 8 de septiembre ya ejecutó esa corrección; no es trabajo
futuro, es trabajo hecho. La frase quedó así desde antes de esta sesión — nadie la actualizó cuando
la re-corrida se completó. Corregida a: «...la corrección exigió re-ejecutar el estudio completo.
Eso es lo que hizo la re-corrida del 8 de septiembre que hoy sostiene la Tabla 7 (§5.3.1): el
corpus vigente no arrastra este defecto». Sin este hallazgo, comprimir o retirar el punto 7 de §7.2
habría dejado una referencia rota (un anexo remitiendo a un «trabajo futuro» que ya no existe como
tal).

### Verificación y mecánica de propagación

Antes de comprometer: `la composicion de FP (§3.3/§7.2) reproduce desde el artefacto` en `ok`
(ambas apariciones sobreviven); `la correlacion de capacidad reproduce desde su artefacto` en `ok`
(no se tocaron las cuatro cifras exactas); `referencias §x.y con destino existente` en `ok` (nada
quedó apuntando a un lugar vacío). Declaradas en `FALLOS_DECLARADOS` las divergencias `.md`↔`.docx`
que las tres compresiones producen (párrafos nuevos, y un efecto colateral: el recuento de
resaltes del cuerpo subió de 8 a 10 en los tres `.docx` sin regenerar, porque el texto que
resaltaban ya no coincide con ningún **bold** del `.md` — no se tocó `BOLD_CUERPO_BASE`, que sigue
siendo constante de Claude Desktop). 56 comprobaciones, 0 fallos nuevos.

**Efecto en el presupuesto de páginas**: neto reductor — las tres compresiones juntas quitan más de
200 palabras del cuerpo, lo que da margen adicional sobre el ya ajustado por `§F169`/`§F170` el
mismo día.

**Con esto quedan ejecutadas las tres candidatas de `LEARNING §L80`.** No queda ninguna pendiente de
esa lista; la duda de terminología (`localizaciones` vs. `ubicaciones`) sigue sin resolver, sin
tocar, porque no se pidió resolverla hoy.

---

## §F173 — Segundo barrido sin más candidatas, `GLOSARIO.md` nuevo, y datos reales para la duda de terminología

**2026-09-12, mismo día.** El autor pidió tres cosas más, tras confirmar `§F172`: (1) volver a
revisar el cuerpo por más pasajes similares a los ya comprimidos; (2) para la duda de terminología
de `LEARNING §L80` (punto 4), añadir «direcciones» y «topónimos» como opciones y dar ejemplos reales
del corpus, documentando en extenso en los documentos relacionados; (3) crear `GLOSARIO.md` con las
definiciones relevantes del estudio.

**(1) Segundo barrido — sin más candidatas.** Un fork revisó el cuerpo completo buscando el mismo
patrón (defectos ya corregidos narrados con detalle, cifras sin respaldo, «trabajo futuro» ya
hecho). Encontró dos casos dudosos y los **descartó con justificación**, no forzó candidatos:

- La discusión del *mojibake* en §6 (~250 palabras: 21/26 configuraciones puntúan mejor cuando la
  corrupción está en la referencia, 23/26 puntúan peor cuando está en el texto de entrada) **no es
  anécdota histórica**: es un hallazgo metodológico generalizable («la implicación metodológica
  excede a este trabajo») que el propio texto reclama como aporte, cualitativamente distinto de los
  puntos 7/8 de §7.2 que sí se comprimieron.
- La cautela sobre el dict-RAG v1.0 en §5.6 (línea base averiada del 13,95 % citada junto al 62,38 %
  de la corrida limpia) es una **advertencia interpretativa activa sobre un resultado que el cuerpo
  sigue reportando ahora**, no un resto de historia pre-8-de-septiembre.

Las demás menciones a corridas o directorios `results/...` en el cuerpo son citas de procedencia
metodológicamente necesarias (qué corrida sostiene qué tabla), exactamente lo que `CLAUDE.md` sigue
exigiendo declarar. **Conclusión: `§F172` ya cubrió todo lo que encaja limpiamente en el criterio.**
No se tocó nada del `.md` por este punto.

**(2) Datos reales para la duda de terminología.** Inspeccionado `data/benchmark_balanced_120.json`
directamente (no de memoria ni por inferencia): la categoría `locations` anota **545 entidades, 339
valores únicos**. La mayoría son topónimos —países, comunidades autónomas, ciudades— pero una parte
real son lugares institucionales (`Universidad de Deusto`, `Hospital Virgen del Rocío`, `Palacio de
la Moncloa`, `Forum Deusto`), y **no se encontró ninguna dirección postal**. Con esa evidencia:
«direcciones» queda descartada (no encaja con ningún ejemplo real); entre «topónimos» (preciso para
la mayoría, deja fuera los lugares institucionales) y «ubicaciones» (cubre ambos), la segunda
describe mejor la composición real de la categoría. **Sigue sin resolverse** — es evidencia para
informar la decisión del profesor guía, no una resolución tomada por esta sesión. Documentado en
extenso en `LEARNING §L80` (actualización del punto 4) y en `GLOSARIO.md`.

**(3) `GLOSARIO.md`, nuevo.** Documento de referencia en la raíz del proyecto (mismo estatus que
`FINDINGS.md`/`LEARNING.md`: documento de trabajo, no entregable de los listados en `CLAUDE.md`,
salvo que el autor decida incorporarlo como anexo). Reúne las definiciones ya presentes en el
informe —no introduce conceptos nuevos— organizadas en seis bloques (entidades y evaluación;
modelos y aprendizaje en contexto; RAG; arquitectura de ejecución; validación estadística; dominio
de cumplimiento), cada entrada con su referencia de sección (`§`) y su cita bibliográfica cuando
aplica. La entrada «Localizaciones / Ubicaciones (LOC)» lleva la evidencia del punto (2) completa,
con los nueve ejemplos reales citados.

**Una referencia de sección se verificó y corrigió antes de comprometer**: la entrada de «d de
Cohen» se había escrito primero como `§4.1.2` de memoria; comprobado con `grep`, la cita real está
en `§5.3` (el contraste MLX vs. compilación estándar sobre N=30). Corregida antes de guardar —el
mismo hábito de «no citar una sección sin comprobarla» que ya rige para el resto del proyecto.

**Verificado**: `GLOSARIO.md` no lo toca ninguna comprobación de `tools/verificar_informe.py` (no es
el Markdown del informe ni su bibliografía), así que su creación no afecta el estado del verificador;
confirmado que sigue en 0 fallos nuevos tras crearlo. La extensión de `LEARNING §L80` sí citaba
`§F173` antes de que existiera esta sección — 1 fallo nuevo momentáneo (`toda referencia §F y §L
tiene su seccion`), resuelto al escribir esta misma entrada.

---

## §F174 — Los +10,40 pp del prompt en español no son un error de cálculo: son un artículo que no parseó

**Fecha:** 2026-09-14. **Origen:** pregunta del autor —«¿de dónde se obtienen los +10,4 % de mejor desempeño
por prompts en español? ¿Existe evidencia sólida o es porque los nombres están en español o portugués en
Kleptotrace?»—, seguida de «analizar en profundidad, asegurarse de que no sea un error». **Medido sobre los
datos crudos de las dos corridas.** Amplía `§F55` y **corrige el mecanismo que propuso `§F56`**.

### 1. La cifra reproduce. No hay error aritmético

Recalculado desde `results/ablacion_n15_REMOTO/benchmark_results.csv` (`gemma4:latest`, N=15 Kleptotrace,
semilla 42, temperatura 0,1, una sola pasada por celda, 2026-09-06), la media de F1 por artículo da
**exactamente** lo que publica la Tabla 5: `zs-en` 64,05 · `zs-es` 68,43 · `fs-en` 63,32 · `fs-es` 74,44, de
donde salen los **+4,38**, **−0,72** y **+10,40**. La comprobación 27 del verificador ya ataba esas tres
diferencias a su fuente, y sigue siendo correcta.

**El problema no es el número. Es de qué está hecho.**

### 2. Un solo artículo aporta el 60 % del efecto, y lo aporta por un fallo de formato

| Artículo | `zs-en` | `zs-es` | `fs-en` | `fs-es` | parseo `zs-en` |
|:---|---:|---:|---:|---:|:---|
| 4 (`C047_1`, Isabel dos Santos / Angola) | **0,00** | 93,15 | **0,00** | 93,15 | `fallback` |

En ese registro el detalle da `tp=0, fp=0, fn=18`: el modelo **no devolvió nada parseable**. El
`benchmark.log` de la corrida contiene **dos** avisos `Failed to parse JSON from raw response` en toda su
ejecución, y los dos son de configuraciones inglesas sobre **ese mismo artículo**. Las dos configuraciones
españolas no tuvieron ninguno.

Ese artículo aporta 93,15/15 = **6,21 pp de los 10,40**. Retirándolo:

| Agregación | con el artículo 4 | sin el artículo 4 |
|:---|---:|---:|
| `fs-es` − `zs-en`, macro (media de F1 por artículo, la que publica la Tabla 5) | +10,40 | **+4,49** |
| `fs-es` − `zs-en`, micro (tp/fp/fn agregados) | +8,36 | **+3,52** |
| `zs-es` − `zs-en`, micro | +2,90 | **−2,63** |

La última fila es la que más importa: **el efecto del idioma por sí solo cambia de signo**. Y en macro su
mediana ya era **0,00**, con seis artículos que mejoran, seis que empeoran y tres empatados.

### 3. La segunda corrida hace lo mismo, y allí el efecto se invierte del todo

`kleptotrace_20260727_110454`, mismo modelo, mismo corpus, misma semilla y temperatura, publica +3,11 pp
(`§F55`). También tiene un cero por `fallback` en una configuración inglesa —el artículo 1— y ninguno en las
españolas. Excluyendo los artículos con cero: `zs-en` **71,53** frente a `fs-es` **70,22**, es decir
**−1,31 pp**. El +3,11 de esa corrida es **íntegramente** el fallo de parseo de un artículo.

Agregando las dos corridas: **4 registros con extracción vacía en 60 ejecuciones con prompt inglés, 0 en 60
con prompt español** (Fisher exacto de una cola, p = 0,059).

### 4. La significancia nunca existió, y la propia corrida lo dice

`statistical_report.md` de la corrida citada: ANOVA **F = 1,1379, p = 0,3417**; Tukey `fs-es` vs `zs-en`
**p = 0,4246**; `zs-en` vs `zs-es` **p = 0,9164**. Ninguna comparación alcanza significancia. La t pareada da
**t(14) = 1,629, p ≈ 0,126**, con mediana +5,13 e IC bootstrap del 95 % de [+1,02, +24,33], un intervalo cuya
asimetría delata que lo sostiene un solo punto. La desviación típica de `zs-en` es 23,50 frente a 13,37 de
`fs-es`: **la varianza inglesa la produce el cero**. Y el análisis de sensibilidad de la propia corrida, al
filtrar los seis artículos largos, reduce la diferencia de +10,40 a **+6,94**.

La glosa de la Tabla 5 ya advierte que los deltas «deben leerse como una tendencia consistente y no como una
diferencia demostrada». Esto es correcto y se mantiene. Lo que este hallazgo añade es que **ni siquiera la
consistencia se sostiene**: sin el artículo que no parseó, la tendencia del idioma puro desaparece.

### 5. El mecanismo de los nombres ibéricos que propuso `§F56` no lo soportan los datos

`§F56` y §6.1 del informe explican la ventaja porque la instrucción en español ayudaría a delimitar los
nombres portugueses del caso angoleño, «donde un tokenizador anglocéntrico parte `Isabel dos Santos` en dos
entidades». Contrastado contra el registro de errores de la corrida (`error_taxonomy.boundary_errors`):

| Configuración | Errores de límite (total) | Sobre nombres con partícula o acento |
|:---|---:|---:|
| `zs-en` | 65 | **2** |
| `zs-es` | 77 | **6** |
| `fs-en` | 48 | **2** |
| `fs-es` | 58 | **6** |

**Las configuraciones españolas cometen más errores de límite sobre nombres ibéricos, no menos**, y en
ninguna de las cuatro aparece el caso que el informe describe: no hay una sola entidad partida por la
partícula. Los seis casos españoles son confusiones difusas entre dos personas distintas
(`Isabel dos Santos` contra `Carlos Saturnino`, ratio 54,5), y los dos ingleses, entre padre e hija
(`Isabel` contra `José Eduardo dos Santos`, ratio 65,0). Son fallos del emparejamiento difuso, no de
tokenización.

Hay además una coincidencia que invita al error y conviene nombrar: el artículo que carga con todo el efecto
**es** uno de los de Isabel dos Santos, de modo que un vistazo superficial parece confirmar la hipótesis
ibérica. No la confirma. Ahí el prompt inglés no delimitó mal esos nombres: **no extrajo ninguna entidad**,
con `fp = 0`. Si el mecanismo fuera de delimitación, se vería en los errores de límite, y ahí se ve lo
contrario.

### 6. Qué queda en pie

- **Sostenible:** con prompt en español el modelo produjo salida parseable en el 100 % de los registros, y con
  prompt en inglés falló en 4 de 60. Es un efecto de **robustez del formato de salida**, plausible y
  compatible con que los ejemplos *few-shot* en español fijen la estructura de la respuesta —`fs-es` parsea
  15/15 por bloque de código—, pero medido sobre cuatro sucesos y sin significancia (p = 0,059).
- **No sostenible:** que el prompt en español mejore la **calidad** de la extracción. Descontado el fallo de
  formato, el idioma puro da −2,63 pp en micro y mediana cero en macro sobre la corrida favorable, y −1,31 pp
  sobre la otra.
- **No sostenible:** el mecanismo de los nombres ibéricos, que los errores de límite contradicen.
- **Por dónde es rebatible en la defensa:** un tribunal que pida el desglose por artículo llega a esto en dos
  minutos, porque un F1 de 0,00 en una tabla de quince filas salta a la vista. La defensa fuerte no es
  sostener el +10,40, sino declarar que la diferencia la produce un fallo de formato en un artículo y que por
  eso la conclusión se enuncia como tendencia no replicada.

### 7. Consecuencia para el informe (pendiente de decisión del autor)

Ningún dato se retira: la política aditiva se mantiene y la Tabla 5 publica las cuatro configuraciones con su
fuente. Lo que procede revisar es **prosa**, en tres sitios:

1. **§5.2, Hallazgo 5**, cierra con «Los ejemplos solo resultan productivos redactados en el idioma del
   corpus». El corpus está **en inglés**; la frase es el mecanismo que `§F54` ya declaró invertido y que
   sobrevivió en ese párrafo. Contradice además a §6.1, que en la misma entrega dice lo contrario.
2. **§6.1** atribuye el efecto a la delimitación de nombres ibéricos. La tabla del punto 5 lo refuta.
3. Convendría que la glosa de la Tabla 5 declarara el registro con extracción vacía, que es el dato que
   explica el delta y la desviación típica de `zs-en`.

**Lección derivada:** ver `LEARNING §L81`.

---

## §F175 — El mismo defecto bajo la conclusión titular: el +12,26 pp del RAG en el modelo más débil

**Fecha:** 2026-09-14. **Origen:** el autor pidió «revisar en el documento cualquier error similar al de
`§F174` que no tenga sustento». Buscado el patrón —registros con extracción vacía— sobre la corrida
**vigente**, apareció en el primer sitio donde se miró. **Medido sobre
`results/ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv`.**

### Lo que hay

Contados los registros averiados por configuración en las 2938 filas del consolidado definitivo
(113 artículos por grupo, trece modelos):

| Configuración | F1 = 0 | Parseo `fallback` |
|:---|---:|---:|
| `nemotron-mini:4b` línea base | **19** | **32** |
| `nemotron-mini:4b` con KB RAG | 6 | 3 |
| `mistral-nemo:latest` con KB RAG | 3 | **41** |
| `deepseek-r1:1.5b` línea base / con RAG | 8 / 7 | 1 / 3 |
| Los otros nueve modelos | 1 a 3 | 0 a 2 |

Excluyendo los artículos en los que **alguna** de las dos configuraciones dio cero o falló el parseo, el
beneficio del RAG por modelo queda así:

| Modelo | Publicado | Descontadas las averías | Artículos excluidos |
|:---|---:|---:|---:|
| `nemotron-mini:4b` | **+12,26** | **+7,28** | 47 de 113 |
| `mistral-nemo:latest` | −4,29 | −3,64 | 44 |
| `deepseek-r1:1.5b` | +2,07 | +1,21 | 15 |
| `qwen2.5:14b` | +0,69 | +1,60 | 2 |
| `gemma:latest` | +0,03 | +1,01 | 4 |
| Los otros ocho | sin cambio material (≤ 0,1 pp) | | 1 a 2 |

**Cerca del 40 % del beneficio titular del RAG en el modelo más débil no es extracción mejor: es que con
RAG el modelo devuelve salida parseable más a menudo.** Y esa es justamente la cifra que el resumen y el
abstract citan como resultado principal del estudio de RAG.

### Lo que esto no es

**No invalida la conclusión general.** El patrón que sostiene el trabajo —el beneficio del RAG decrece con
la capacidad del modelo— sobrevive intacto: los ocho modelos de capacidad media y alta no se mueven ni una
décima, y el orden se conserva. Lo que hay que rehacer es el **enunciado de la magnitud** en el caso extremo.

**Y no está claro que la exclusión sea la corrección correcta.** Un modelo que devuelve JSON mal formado
está fallando de verdad, y ese fallo es suyo; excluir esos registros puede ocultar una debilidad real del
modelo en lugar de corregir un defecto del instrumento. La distinción que decide el caso es si el modelo
**produjo entidades que el parser no supo leer** —defecto del instrumento— o si **no produjo entidades**
—desempeño del modelo—. Eso se resuelve abriendo el `benchmark.log` registro a registro, y está **en curso**
en el workflow forense lanzado el mismo día; esta entrada se completará con su dictamen.

### La forma honesta de enunciarlo

Cualquiera que sea la clasificación, la formulación defendible descompone la cifra en vez de elegir una de
las dos: el RAG contextual aporta al modelo más débil **+7,3 puntos de F1 en calidad de extracción** y
alrededor de **+5 puntos más por robustez del formato de salida**, sobre 113 artículos. Las dos mitades son
resultados, y decir solo la suma oculta que son cosas distintas.

**Ver también:** `§F174`, del que este hallazgo es la réplica sobre la corrida vigente, y `LEARNING §L81`,
cuya regla —clasificar los ceros antes de promediarlos— es la que lo encontró.

### Corrección del mismo día: §F175 estaba sobredimensionado. El beneficio del RAG se sostiene

**Fecha:** 2026-09-14, unas horas después de escribir la entrada anterior. **Origen:** al medir la robustez
de formato por modelo apareció una incoherencia — `nemotron-mini:4b` tenía 20 registros con F1 = 0 pero solo
2 con extracción vacía. Los dos números no podían describir el mismo fenómeno.

**El error era del criterio de exclusión, y era mío.** La entrada anterior excluyó los registros con
`f1 == 0` **o** `parse_method == 'fallback'`. Eso es demasiado ancho: mezcla dos cosas distintas.

| Situación | Qué significa | Cómo se identifica |
|:---|:---|:---|
| Avería del instrumento | el modelo no produjo salida legible y no se extrajo nada | `tp + fp == 0` **y** parseo `fallback` |
| Fallo del modelo | el modelo extrajo entidades y todas eran erróneas | `f1 == 0` con `fp > 0` |
| Rescate por expresión regular | el JSON venía mal formado pero se recuperaron entidades | parseo `fallback` con `tp + fp > 0` |

Solo la primera es avería. Las otras dos son desempeño, y excluirlas **encubre una debilidad real del
modelo** en lugar de corregir un defecto de la medición.

**Descompuestos los ceros de la corrida vigente**, de los 20 de `nemotron-mini:4b` en línea base **18 son
fallos del modelo** —extrajo entidades y erró todas— y solo 2 son extracciones vacías. Con el criterio
estricto, el efecto del RAG apenas se mueve en ningún modelo:

| Modelo | Publicado | Excluidas solo las averías reales | Registros excluidos |
|:---|---:|---:|---:|
| `nemotron-mini:4b` | +13,71 | **+13,04** | 2 |
| `gpt-oss:20b` | +1,53 | +2,28 | 1 |
| `mistral-nemo:latest` | −3,64 | −2,83 | 1 |
| `deepseek-r1:1.5b` | +2,97 | +3,43 | 4 |
| Los otros nueve | sin cambio alguno | | 0 |

*(Calculado sobre los 120 registros de `recorrida_20260908/*__N120`; el consolidado publica 113 por grupo
tras excluir los 7 contaminados, de ahí la pequeña diferencia con la cifra de la Tabla 7.)*

**Conclusión corregida: el beneficio del RAG en el modelo más débil es real y no lo escribe una avería de
parseo.** La conclusión 1 del informe se sostiene tal como está. Retírese de `§F175` la afirmación de que
«cerca del 40 % del beneficio titular es robustez de formato»: no es cierta.

**Lo que sí queda, y es menor.** `nemotron-mini:4b` recupera por expresión regular el **27,5 %** de sus
registros en línea base frente al 2,5 % con RAG, y `mistral-nemo:latest` el **35 %** con RAG frente al 1,7 %
sin él. Esos registros sí puntúan, porque el rescate extrae entidades, pero un rescate por expresión regular
puede perder parte de la lista. Es una limitación del instrumento que conviene medir y declarar; no es un
defecto que invalide ninguna cifra.

**Y lo que no cambia:** `§F174` se sostiene íntegro. Allí el artículo 4 cumple el criterio estricto
—`tp = 0`, `fp = 0` y parseo `fallback`—, es decir, una avería real del instrumento, y sigue aportando
6,21 de los 10,40 puntos.

**Lección:** el criterio con el que se excluye un registro decide el resultado tanto como el dato. Escribirlo
de forma laxa —«cero o fallback»— y no comprobar que los dos recuentos que produce son coherentes entre sí
fue exactamente el tipo de error que `§L81` advierte, cometido al aplicarla. Ver `LEARNING §L82`.

---

## §F176 — R1 Fase 1 llegó: con réplicas, el efecto del idioma se sostiene, y ahora hay dos hallazgos donde antes había uno

**Fecha:** 2026-09-14, ~23:00. **Origen:** primera entrega del equipo remoto sobre el encargo de
`§F174`/`§F175`: `results/variantes_5semillas_n15_REMOTO/`, cinco semillas (42, 43, 44, 45, 46) del diseño
factorial 2×2 sobre N=15, con el parser vigente y `max_tokens=4096`. **Verificado desde el CSV crudo de las
cinco semillas**, no desde el resumen del equipo remoto.

### Lo que llegó reproduce

| Configuración | Media de las 5 semillas | Desviación entre semillas |
|:---|---:|---:|
| `fs-es` | **79,96 %** | 0,54 |
| `zs-es` | 75,78 % | 3,54 |
| `fs-en` | 70,38 % | 2,48 |
| `zs-en` | 66,77 % | 2,42 |

Jerarquía `fs-es` > `zs-es` > `fs-en` > `zs-en` **en las cinco semillas sin excepción**. Esto ya es un salto
respecto a `§F174`: allí una sola pasada podía estar escrita por un artículo; aquí hay cinco corridas
independientes y la relación de orden no varía nunca.

### El defecto de `§F174` replica, y solo en un sitio

Contadas las averías reales (`tp+fp==0` y parseo `fallback`) en los detallados de las cinco semillas: **10 de
150** registros en configuraciones inglesas (`zs-en`, `fs-en`), **0 de 150** en las españolas (`zs-es`,
`fs-es`). No es un artículo suelto: en tres de las cinco semillas afecta al artículo 1, en tres afecta al
artículo 4, y ninguna semilla escapa del todo. **El patrón de `§F174` no era ruido de una corrida: es una
propiedad estable del sistema.**

### El delta se descompone en dos efectos, los dos reales

| | Con las averías (lo que publicaría la Tabla 5) | Excluidas las averías |
|:---|---:|---:|
| `fs-es` − `zs-en`, media de las 5 semillas | **+13,19 pp** | **+7,44 pp** |
| Por semilla | +16,25 / +10,69 / +13,08 / +10,90 / +15,02 | **+11,03 / +7,72 / +4,74 / +5,72 / +7,97** |

**Lo que cambia respecto a `§F174`: la columna de la derecha nunca cruza cero.** Con una sola corrida, quitar
el artículo averiado invertía el signo del efecto de idioma puro; con cinco, quitar las averías **reduce**
el efecto pero lo deja positivo en las cinco semillas, entre +4,7 y +11,0 puntos. Eso es una tendencia
consistente, con réplicas, y ya se puede llamar así sin la reserva que `§F55` y `§F174` obligaban a poner.

**Y la robustez de formato es en sí misma un segundo hallazgo, no un artefacto que restar.** Que el prompt en
español produzca salida parseable el 100 % de las veces (150 de 150) frente al 93,3 % del inglés (140 de
150) es una propiedad medida con réplica, no una casualidad de un registro. Conviene reportar los dos
números por separado: **+7,4 puntos de calidad de extracción** y **+5,8 puntos adicionales de robustez de
formato**, en vez de fundirlos en una sola cifra que oculta que son cosas distintas — es la misma regla que
`§F175` corrigió aplicar al RAG.

### Lo que sigue exactamente igual

**El mecanismo de los nombres ibéricos de `§6.1` sigue sin sustento.** Nada en esta entrega lo confirma ni lo
refuta directamente —eso lo responde R5, sobre el par emparejado, que está en curso—, pero la explicación de
por qué el efecto existe sigue pendiente de ese experimento, no de este.

### Consecuencia para el informe

**Todavía no se toca nada.** Falta R1 Fase 2 (N=120, el corpus donde vive la hipótesis del trabajo) y R5 (el
par emparejado, que es el experimento que de verdad aísla el efecto del idioma). Esta entrega **cierra la
pregunta de si el efecto sobre N=15 es real**: lo es. No cierra si se sostiene sobre el corpus mayor, que es
la pregunta que importa para la tesis.

**Ver también:** `§F174` (el defecto original, sobre una sola pasada), `§F175` y su corrección (el mismo tipo
de error de criterio, sobre el RAG), y `LEARNING §L82` (la regla de separar avería de desempeño), que esta
entrada confirma en un caso nuevo.

---

## §F177 — Dos workflows forenses terminaron: 85 de 120 cifras frágiles o incorrectas, una reversión importante, y un desacuerdo entre los dos que hube que resolver yo

**Fecha:** 2026-09-14, ~23:20. **Origen:** los dos workflows lanzados tras `§F174`/`§F175`
(`forense-cifras-20260914` y `purga-informe-20260914`) aterrizaron durante la misma pasada del `/loop`.
**Verificado de forma independiente** en los puntos de mayor impacto antes de escribir esta entrada —no se
transcribe el dictamen sin más, siguiendo la regla de `CLAUDE.md` de que un hallazgo de auditoría es una
hipótesis—. Dictámenes completos conservados en `DICTAMEN-FORENSE-CIFRAS-20260914.json` y
`PLAN-PURGA-INFORME-20260914.json`, en la raíz.

### 1. La reversión más importante: el RAG en `nemotron-mini:4b` es sólido, no frágil

`§F175` corrigió un criterio de exclusión demasiado ancho (`f1==0` **o** `fallback`) y concluyó que el
efecto del RAG en el modelo más débil pasaba de +13,71 a **+13,04** con el criterio estricto
(`tp+fp==0` **y** `fallback`). Ese criterio **también estaba mal**, y lo confirmo yo mismo leyendo el código:

```
repos/ner-llm-entity-benchmark/src/providers/ollama_provider.py:368-372
if raw_content.strip().startswith("{") and raw_content.strip().endswith("}"):
    method = "direct_json"
elif "```" in raw_content:
    method = "codeblock"
else:
    method = "fallback"
```

`parse_method` es un chequeo **cosmético** sobre la forma del texto crudo, no una medida de si la extracción
tuvo éxito. La condición «**y** `fallback`» de mi propio criterio era arbitraria: no hay ninguna razón para
que una avería real dependa de si el texto tenía o no llaves. **El criterio correcto es simplemente
`tp==0 y fp==0`, sin más.**

Verificado directamente sobre `results/recorrida_20260908/`:

| Modelo | `tp=fp=0` puro | de ellos, con `fallback` |
|:---|---:|---:|
| `nemotron-mini:4b` (baseline) | 2 | 2 |
| `mistral-nemo:latest` (baseline) | **1** | **0** |
| `mistral-nemo:latest` (kb_rag) | **2** | **1** |

Mi criterio compuesto **excluía mal** las averías de `mistral-nemo`: de sus tres averías reales, solo dos
tenían la etiqueta `fallback`. Recalculado con el criterio correcto sobre el CSV de 113 artículos:

| Modelo | Publicado (Tabla 7) | Corregido (criterio puro) |
|:---|---:|---:|
| `nemotron-mini:4b` | +12,26 | **+11,52** |
| `mistral-nemo:latest` | −4,29 | **−3,46** |

Verificado por mí de forma independiente: reproduce exacto lo que reportan los dos workflows. **La cifra de
`§F175` (+13,04) estaba además calculada sobre los 120 artículos sin excluir los 7 contaminados**, no sobre
los 113 que publica la Tabla 7 — un desliz de población, no solo de criterio.

**Conclusión: el beneficio del RAG en `nemotron-mini:4b` es mayoritariamente desempeño real, no un artefacto
de formato.** De 32 registros marcados `fallback` en su línea base, **23 tienen `tp>0`**: el modelo sí
extrajo entidades, solo que su texto crudo no empezaba y terminaba con llaves. La frase de `§F175` sobre
«recuperar por expresión regular el 27,5 %» describía mal el fenómeno: no se sabe, desde el CSV, qué
estrategia interna de `parse_llm_response` tuvo éxito en cada caso, porque `parse_method` no lo registra.

**`§F175` queda superado por esta entrada en su cifra concreta**, no en su lección: separar avería de
desempeño sigue siendo la regla correcta; lo que cambia es cómo se detecta la avería.

### 2. Anexo J: error de lectura de la propia Tabla 20, verificado por mí sobre el texto publicado

El Anexo J dice: «Solo la ausencia de `nemotron-mini:4b` cambia el signo y la significancia del coeficiente
de Pearson». Leída la Tabla 20 del propio anexo:

| Retirado | Pearson r | p | ¿Cambia signo? | ¿Cambia significancia? |
|:---|---:|---:|:---:|:---:|
| `nemotron-mini:4b` | **+0,0120** | 0,9706 | **sí** | no (sigue no significativo) |
| `deepseek-r1:1.5b` | −0,6151 | **0,0333** | no | **sí** (cruza a significativo) |
| `mistral-nemo:latest` | −0,5971 | **0,0404** | no | **sí** (cruza a significativo) |

La frase describe exactamente lo contrario de lo que su propia tabla muestra: `nemotron-mini` cambia el
**signo**, no la significancia (el conjunto completo ya era no significativo, p=0,0956); `deepseek-r1` y
`mistral-nemo` cambian la **significancia**, no el signo. Es el error más barato de corregir de todo el
informe: no exige recalcular nada, solo releer la tabla que ya está impresa dos párrafos más abajo.

### 3. El 90,16 % sí existe, y los dos workflows discreparon sobre su origen — resuelto por mí

`forense-cifras` dictaminó que 90,16 % procede de `n30_rerun_REMOTO`, con el defecto de `Locations` sin
anotar. `purga-informe`, en su síntesis, dictaminó lo contrario: «no existe en ningún fichero de resultados
del proyecto» y propuso sustituirlo directamente por 81,47 %. **Comprobado por mí sobre el propio artefacto**:

```
gemma4:31b-mlx, n30_rerun_REMOTO, F1 restringido a Personas+Organizaciones = 90,16 %  (reproduce exacto)
```

**`forense-cifras` tenía razón; `purga-informe` se equivocó** — probablemente por no probar la convención de
dos categorías, solo la de tres (que da 80,57 %, no 90,16 %). La cifra existe, es trazable, y su problema no
es que sea inventada sino que mezcla dos convenciones distintas (dos categorías para el dominio, tres para el
corpus periodístico) presentadas en la misma frase como si fueran comparables, y además procede de una
corrida con el defecto de `Locations` puntuando contra el vacío (`tp=0, fp=56, fn=0` en todo el corpus,
verificado por mí).

**Valor recalculado, bajo la corrida vigente** (`results/recorrida_20260908/gemma4_31b-mlx__N30/`):
**85,60 %** con la misma convención de tres categorías que usa el 81,47 % con el que se empareja hoy — la
cifra correcta a sustituir, si se mantiene la comparación en la misma frase.

**Lección para el propio proceso:** dos auditorías independientes sobre la misma cifra llegaron a
conclusiones opuestas sobre un hecho verificable (si el fichero existe o no). Ninguna de las dos se aceptó
sin comprobar; la del asunto de la orquestación en `CLAUDE.md` —verificar contra la fuente antes de convertir
un hallazgo en instrucción— aplicó aquí entre dos IAs, no solo entre una IA y un humano.

### 4. Lo demás, verificado con menos profundidad pero con evidencia citada y trazable (ver el JSON completo)

- **Tabla 7, columna «Δ significativo»**: usa Tukey no pareado sobre datos que el propio informe declara
  pareados (mismos 113 artículos). Con contraste pareado y Holm(13): **cinco** modelos significativos, no
  uno — incluido `mistral-nemo:latest` como empeoramiento significativo. Pendiente de una verificación mía
  independiente antes de tocar el informe; el cálculo lo hicieron dos rondas del workflow, no yo.
- **Tabla 4 (N=15)**: las cuatro corridas que la alimentan puntúan `Locations` contra el vacío (63
  localizaciones anotadas desde el 8 de septiembre, pero las corridas son de julio-agosto). Entre 41 % y
  80 % de los falsos positivos de cada fila son de esa categoría.
- **Contradicción interna confirmada**: §5.6 dice «nueve de los trece modelos mejoran con RAG»; §5.3.1, en
  el mismo capítulo, dice «once de los trece». La segunda es la vigente.
- **χ² de Friedman = 1802,3671 (§5.3.1)**: ninguna de las dos rondas pudo verificarlo. **No darlo por bueno**
  sin comprobación adicional.
- **Tasas de alucinación de §5.4**: proceden de la corrida del 24 de agosto, no de la vigente, y mezclan dos
  umbrales distintos del código (`<70` y `<50`) bajo el mismo nombre.

### 5. Estado

**No se ha tocado el informe.** Ambos workflows son de solo lectura por diseño. Con el volumen y la
importancia de lo encontrado —incluida la primera frase del Resumen y el Abstract—, la aplicación de
correcciones requiere una decisión del autor sobre el alcance, no una ejecución automática. Pendiente de
instrucción. Ver `CURRENT-TASKS.md` para el registro de coordinación.
