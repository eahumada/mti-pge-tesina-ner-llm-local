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

### F28. Dos modelos distintos con métricas byte-idénticas
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

### F32. ⚠️ DIAGNOSTICADO — Ningún esquema de promediado explica los F1 imposibles
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

### F33. 🔴 CRÍTICO — El modelo `gemma4:31b` no tiene datos crudos en ninguna corrida
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
