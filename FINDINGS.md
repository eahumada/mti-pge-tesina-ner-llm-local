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
- **``** presenta una anomalía sin explicar: con `think` apagado va **más lento**
  (×0.3, de 7 s a 25 s), lo que **contradice el modelo causal** del hallazgo (el razonamiento genera tokens;
  no puede acelerar). Además una mediana de 7 s para un 26B es llamativamente rápida. Su +0.021 **no debe
  darse por bueno** hasta explicar ese dato.

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
