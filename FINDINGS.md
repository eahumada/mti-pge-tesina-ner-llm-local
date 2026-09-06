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
- **Estado:** eliminado de todo el proyecto por decisión del autor. Nombre canónico: `gemma4:12b-mlx`.

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

- **Impacto:** el estudio queda con **14 modelos** (5 + 9 locales), no 16.

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

- **Impacto:** el margen real disponible para las correcciones es **desconocido** hasta verificarlo en Word.
  Se adoptó el supuesto conservador (1 página) para no arriesgar el incumplimiento.

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
| `sonct988/gemma4-26b-a4b-it-q4km-256k` | **16 GB** | Igual a la RAM total |
| `gpt-oss:20b` | **13 GB** | Deja ~3 GB para SO, Ollama y KV cache |
| `gemma4:31b` / `gemma4:31b-mlx` | **19 GB** | **Exceden la RAM física** |

**Evidencia del impacto:** el ritmo medido fue de **exactamente 1 extracción cada 3 minutos**, y **no varió**
al aumentar los workers de 2 a 8. Ollama no serializa por configuración sino **porque no cabe otro contexto
en memoria**; `OLLAMA_NUM_PARALLEL` no lo resolvería. En el pico, la memoria libre cayó al 12% con un load
average de 12.33.

**Proyección con los 9 modelos locales:** ≈ **173 horas (7 días)**, de las cuales los tres modelos pesados
concentraban el **85%**.

### F24. Decisión: exclusión de `sonct988` y `gpt-oss:20b`
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
   marca. Restaurada con una nota explicativa.
2. **Código de ejemplo sintácticamente inválido** en `AGENTS.md §8.3`: un `field(default_factory=lambda: [`
   quedó sin cerrar el paréntesis.
3. **Reaparición del nombre de modelo retirado** en `AGENTS.md §8.6`, dentro de una nota de retiro.
   Reformulada sin citarlo.
4. **Autocontradicción entre secciones contiguas**: §8.4 conservaba la forma antigua `self.models = [...]`
   mientras §8.1 y §8.3 ya declaraban que la lista es un campo del dataclass.
5. **Consejo inoperante**: se documentó `--resume` sin mencionar que requiere `--results-dir`.

> La etapa de verificación adversarial **valió su coste**: sin ella, las cinco habrían pasado inadvertidas.
