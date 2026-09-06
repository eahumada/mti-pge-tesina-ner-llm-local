# TODO — Informe Final de Tesina

> Documento de seguimiento del cierre del Informe Final (Hito 5).
> **Política:** estrictamente aditivo. No se elimina contenido previo; los ítems completados se marcan,
> no se borran. Ver `CLAUDE.md` (§Entregables) y `HISTORIAL-CONSOLIDADO.md`.
> **Restricción institucional vigente:** cuerpo ≤ 25 páginas, excluyendo anexos. El margen actual es
> de **1 página**, por lo que toda corrección debe ser neutra en extensión o reducirla.

**Última actualización:** 2026-09-03

---

## 1. Entregables y su estado

| # | Entregable | Ruta | Estado |
|:--|:---|:---|:---|
| 1 | Informe final con plantilla UTFSM/MTI (**canónico**) | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | ✅ Vigente — cuerpo 24 pp. + anexos |
| 2 | Fuente Markdown del informe (**canónica**) | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` | ✅ Vigente |
| 3 | DOCX del borrador Hito 5 | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx` | ✅ Vigente |
| 4 | Informe standalone (sin plantilla) | `Informe_Final_Tesina_NER.docx` | ⚠️ **INCOMPLETO** — ver §3.1 |
| 5 | Copia del DOCX canónico en la raíz | raíz del proyecto | ⏳ Pendiente de sincronizar tras las correcciones |

---

## 2. Completado

### 2.1 Corpus y validación estadística
- [x] Corpus real N=120 (`data/benchmark_balanced_120.json`) construido y documentado (§4.1.3).
- [x] Corrida N=120 del 2026-09-01 con 5 modelos × 2 modos (baseline / KB RAG) = 1200 filas.
- [x] ANOVA + Tukey HSD sobre esa corrida: **F=10.2096, p=2.8730e-15**, documentado en §5.3.5.
- [x] Script de fusión multi-corrida `src/merge_and_analyze.py`, validado reproduciendo exactamente
      F=10.2096 y p=2.8730e-15 y con el cuerpo estadístico idéntico al reporte de referencia.

### 2.2 Integridad del pipeline
- [x] Reparación del entorno virtual (rutas apuntaban a un home inexistente).
- [x] Corrección del flag `--resume`, que era **inoperante**: sin `--results-dir` cada ejecución creaba un
      directorio nuevo y el checkpoint jamás se encontraba, reiniciando desde cero en silencio.
- [x] Guardarraíl que impide escribir en la raíz de `results/` (causa de la pérdida de datos de N=30),
      con 15 tests que lo cubren.
- [x] Persistencia del flag `ablation` en `run_config.json` (antes las corridas de ablación eran
      indistinguibles de un baseline en su metadata).

### 2.3 Nomenclatura y terminología
- [x] Eliminación transversal del modelo `gemma4-12b-mlx-q8-64k`: su sufijo `q8` era **falso**
      (el artefacto real es 4-bit NVFP4, 7.71 GB; un q8 real de 12B pesa 12.84 GB). Nombre canónico
      adoptado: `gemma4:12b-mlx`. Cero ocurrencias del nombre viejo en todo el proyecto.
- [x] Terminología: «Comparación de Configuraciones de Prompt» como término principal, con
      «diseño factorial 2×2» y «estudio de ablación» como sinónimos glosados. Aplicado al `.md`.
      El abstract en inglés conserva *prompt ablation study*.
- [x] Herramienta `tools/docx_replace_terms.py` para aplicar el cambio a los `.docx` sin regenerarlos
      (regenerar destruiría las correcciones manuales de numeración y saltos de página).

### 2.4 Auditoría
- [x] Auditoría de consistencia documental con verificación adversarial:
      **115 hallazgos confirmados** (26 altos, 55 medios, 34 bajos), 17 descartados.
      Informe completo: `AUDITORIA_CONSISTENCIA_20260903.md`.

---

## 3. Pendiente

### 3.1 Correcciones documentales (en curso)
- [ ] Aplicar los 26 hallazgos de gravedad **ALTA**. Los principales:
  - [ ] **Conteo de modelos contradictorio**: §1.4 y §4.2 dicen 15; §2.5, §5.1 y §5.3.5 dicen 16.
        El conteo real de la Tabla 2 es de **12 modelos distintos en 13 configuraciones**
        (`gemma4:latest` aparece legítimamente dos veces: ZS-ES y FS-ES, dos configuraciones de prompt).
  - [ ] **Abstract en inglés corrupto**: contiene «balanceado Kleptotrace/CoNLL-2002/CoNLL-2002»
        (palabra en español y nombre duplicado) y la referencia [18] tiene la URL inválida
        `https://Kleptotrace/CoNLL-2002.org`.
  - [ ] **§4.1.2 autocontradictorio**: dice «datos reales balanceados generados por LLM» cuando el título
        de la subsección es «Corpus Sintético». Residuo de un reemplazo global mal aplicado.
  - [ ] **Tabla 2 partida**: una línea vacía deja `nemotron-mini` y `deepseek-r1` fuera del renderizado.
  - [ ] **§6.1 sesgada**: confirma la hipótesis (F1 ≥ 70%) apoyándose solo en N=30 (79.03%), sin mencionar
        que en el corpus real N=120 el mejor F1 es 59.25%, por debajo del umbral. Es el punto de mayor
        riesgo en la defensa oral.
  - [ ] **Índice Tok/s/B** inconsistente entre §5.1 y §5.5.
  - [ ] **`Informe_Final_Tesina_NER.docx` incompleto**: le faltan las secciones §4.1.3 y §5.3.5 completas
        (verificado: cero ocurrencias de `4.1.3`, `5.3.5` y `10.2096` en su XML).
- [ ] Aplicar los 55 hallazgos de gravedad media y los 34 de baja.

### 3.2 Benchmark N=120 completo
- [ ] Corrida en curso: 9 modelos locales × 2 modos, `--rag-mode kb_combined`, `--num-workers 9`.
- [ ] Fusionar con la corrida del 2026-09-01 y recalcular un único ANOVA/Tukey.
- [ ] Actualizar §5.3.5 con el resultado consolidado.
- [ ] ⚠️ **El estudio quedará con 14 modelos, no 16.** Los dos modelos cloud no son ejecutables:
      `gemma4:31b-cloud` devuelve HTTP 429 (cuota semanal agotada) y `minimax-m3:cloud` HTTP 402
      (requiere suscripción de pago). Verificado contra la API de Ollama. Recuperarlos exige plan de pago.

### 3.3 Recuperación del corpus N=30
- [ ] Re-ejecutar la corrida N=30 para regenerar los datos por registro, perdidos por sobrescritura.
      Solo sobreviven las métricas agregadas en `benchmark_augmented_30.log`.
- [ ] Decisión del autor registrada: **el nuevo resultado será el oficial**; el valor de julio (79.03%)
      se conserva en el WORKLOG para trazabilidad aunque salga del cuerpo de la tesina.
- [ ] Descarga de `gemma4:31b` y `gemma4:31b-mlx` en curso (necesarios para esta corrida).

### 3.4 Sincronización de entregables
- [ ] Propagar las correcciones del `.md` canónico a los tres `.docx`.
- [ ] Colocar copia del `.docx` canónico en la raíz, ya corregido.
- [ ] Verificar que el cuerpo sigue dentro de las 25 páginas tras las correcciones.

---

## 4. Decisiones del autor registradas

| Fecha | Decisión |
|:---|:---|
| 2026-09-03 | Autorizar modelos cloud como línea base de comparación (excepción acotada al corpus público, registrada en `AGENTS.md §2`). |
| 2026-09-03 | Adoptar `gemma4:12b-mlx` como nombre canónico y eliminar toda referencia al nombre con sufijo `q8`. |
| 2026-09-03 | Usar «Comparación de Configuraciones de Prompt» como término principal, conservando los sinónimos técnicos. |
| 2026-09-03 | Ante divergencia en la re-ejecución de N=30, **reemplazar** por el nuevo resultado. |
| 2026-09-03 | Las filas `gemma4:latest (ZS-ES)` y `(FS-ES)` son legítimas y **no deben eliminarse**. |

---

## 5. Documentos de hallazgos y lecciones

| Documento | Contenido |
|:---|:---|
| [`FINDINGS.md`](./FINDINGS.md) | 14 hallazgos técnicos y documentales de la revisión final, con evidencia e impacto |
| [`LEARNING.md`](./LEARNING.md) | 13 lecciones derivadas de esos hallazgos, cada una con su aplicación práctica |
| [`AUDITORIA_CONSISTENCIA_20260903.md`](./AUDITORIA_CONSISTENCIA_20260903.md) | 115 inconsistencias documentales verificadas adversarialmente |

---

## 6. Stack tecnológico del proyecto

### 6.1 Núcleo de ejecución

| Componente | Versión | Rol |
|:---|:---|:---|
| Python | 3.14.7 | Lenguaje del pipeline |
| Ollama | 0.33.2 | Motor de inferencia local (ejecución soberana, sin fuga de datos) |
| ChromaDB | — | Base vectorial local para el RAG de diccionarios |
| Redis | ≥ 5.0 | Cola Pub/Sub para desacoplar ingesta de inferencia |

### 6.2 Análisis y evaluación

| Componente | Rol |
|:---|:---|
| `pandas` ≥ 2.0 | Manipulación de resultados y agregación de métricas |
| `scipy` ≥ 1.11 | ANOVA de una vía |
| `statsmodels` ≥ 0.14 | Tukey HSD post-hoc e intervalos de confianza |
| `scikit-learn` ≥ 1.3 | Cohen's Kappa (acuerdo inter-anotador) |
| `rapidfuzz` ≥ 3.0 | Emparejamiento difuso de entidades (umbral 85) |
| `streamlit`, `plotly`, `matplotlib`, `seaborn` | Dashboard de KPIs y visualización |
| `psutil`, `tqdm` | Telemetría de recursos y progreso |

### 6.3 Modelos evaluados

Familias: **Gemma** (`gemma4:31b-mlx`, `gemma4:latest`, `gemma4:12b-mlx`, `gemma:latest`), **Qwen**
(`qwen3:8b`, `qwen2.5:14b`), **Llama** (`llama3.1:8b`, `llama3.2:latest`), **Mistral**
(`mistral-nemo:latest`), **DeepSeek** (`deepseek-r1:1.5b`), **NVIDIA** (`nemotron-mini:4b`), además de
`gpt-oss:20b`, `nuextract:latest` (especializado en extracción estructurada) y
`sonct988/gemma4-26b-a4b-it-q4km-256k`.

> ⚠️ Los modelos cloud (`gemma4:31b-cloud`, `minimax-m3:cloud`) quedaron **fuera del estudio**: HTTP 429
> por cuota semanal agotada y HTTP 402 por requerir suscripción de pago. Ver `FINDINGS.md §F6`.

### 6.4 Herramientas de IA asistida empleadas en el desarrollo

Este proyecto se desarrolló con asistencia de agentes de IA de **Anthropic** y **Google**. Su uso está
gobernado por los ficheros de instrucciones del repositorio, que comparten `AGENTS.md` como fuente única.

| Herramienta | Proveedor | Rol en el proyecto | Fichero de instrucciones |
|:---|:---|:---|:---|
| **Claude Code** | Anthropic | Agente CLI: implementación del pipeline, orquestación de subagentes y workflows, auditoría de consistencia, verificación estadística | `CLAUDE.md`, `AGENTS.md` |
| **Claude Desktop** | Anthropic | Edición de documentos y correcciones de formato sobre los `.docx` (ver §7) | `CLAUDE.md` |
| **Antigravity** | Google | Asistencia de desarrollo en el IDE agéntico | `ANTIGRAVITY.md` → `AGENTS.md` |
| **Gemini** | Google | Asistencia de desarrollo y revisión | `GEMINI.md` → `AGENTS.md` |

**Modelos de Claude usados como orquestadores.** La política vigente (`CLAUDE.md §Orquestación de
Workflows`) exige que **un orquestador Opus revise las instrucciones entregadas a los subagentes antes de
despacharlas**, tras el incidente en que una instrucción no revisada estuvo a punto de eliminar una fila de
datos experimentales del informe.

> **Nota de cumplimiento.** El uso de estas herramientas se ajusta a la política institucional: los datos
> procesados son corpus públicos (Kleptotrace, CoNLL-2002) sin información personal ni confidencial, y toda
> la inferencia del benchmark se ejecuta **localmente vía Ollama**, sin envío de datos a APIs externas
> (`AGENTS.md §2`). Todo contenido generado por IA fue revisado y validado por el autor antes de
> incorporarse al informe.

---

## 7. Tareas asignadas a Claude Desktop — edición y formato de los `.docx`

> **Responsable: Claude Desktop.** Estas tareas requieren manipulación de documentos Word con preservación
> de formato, que es su ámbito. **No deben ejecutarse desde Claude Code**: regenerar los `.docx` con pandoc
> destruiría correcciones manuales de numeración multinivel (`numId=0`), estilos de fila y saltos de página
> que costaron recuperar 5 páginas (ver `LEARNING.md §L12`).

### 7.1 Reinserción de secciones faltantes (prioritario)
- [ ] **`Informe_Final_Tesina_NER.docx`**: reinsertar íntegras las secciones **§4.1.3** («Extensión a Corpus
      Real N=120 — Dataset Conmutable») y **§5.3.5** («Validación Estadística Complementaria sobre Corpus
      Real N=120», que incluye la tabla de 5 modelos × 2 modos y las cifras ANOVA F=10.2096 / p=2.873e-15).
      Ambas existen íntegras en `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx`
      y en el Markdown canónico. Verificado: cero ocurrencias de `4.1.3`, `5.3.5` y `10.2096` en su XML.

### 7.2 Propagación de las correcciones del Markdown a los `.docx`
- [ ] Aplicar a los tres `.docx` las correcciones ya aplicadas al Markdown canónico (conteo de modelos,
      abstract en inglés, §4.1.2, §6.1, índice Tok/s/B). Consultar `AUDITORIA_CONSISTENCIA_20260903.md`.
- [ ] Existe `tools/docx_replace_terms.py`, validado, para reemplazos de texto que preservan el paquete
      OOXML íntegro (solo modifica `word/document.xml`). Útil para cambios de cadena; **no** sirve para
      insertar secciones nuevas.

### 7.3 Correcciones tipográficas pendientes
- [ ] Las glosas de terminología quedaron en los `.docx` con formato de párrafo plano. En el Markdown,
      «diseño factorial 2×2» va en **negrita** y «estudio de ablación» en *cursiva*. Son 4 selecciones
      manuales en Word.

### 7.4 Verificación final de formato
- [ ] Confirmar que el cuerpo del informe **no excede 25 páginas** excluyendo anexos tras todas las
      correcciones. El margen antes de esta ronda era de **1 página** (24 pp.).
- [ ] Verificar que no quedan páginas en blanco espurias ni tablas partidas.
- [ ] Confirmar que la numeración multinivel sigue correcta (sin prefijos `1.1`, `1.1.49`).
- [ ] Dejar copia del `.docx` canónico ya corregido **en la raíz** del proyecto.

### 7.5 Coordinación
- [ ] ⚠️ **Concurrencia:** Claude Code puede estar editando el Markdown canónico y los documentos de
      seguimiento en paralelo. Releer cada archivo inmediatamente antes de escribir y preferir `append`
      sobre reescritura. Ver `CLAUDE.md §Concurrencia entre Sesiones`.

---

## 8. Actualización 2026-09-03 (tarde) — Alcance final del estudio

> Esta sección **corrige el alcance declarado en §3.2**, que hablaba de 14 modelos. El número final es **12**.

### 8.1 Exclusión de modelos por restricción de hardware
El equipo de evaluación tiene **16 GB de RAM**. Dos modelos no caben razonablemente y provocaban swap
masivo (1 extracción cada 3 minutos, sin mejora al aumentar los workers de 2 a 8):

| Modelo excluido | Tamaño | Motivo |
|:---|---:|:---|
| `sonct988/gemma4-26b-a4b-it-q4km-256k` | 16 GB | Igual a la RAM total del equipo |
| `gpt-oss:20b` | 13 GB | Deja ~3 GB para SO, Ollama y KV cache |

**Efecto:** proyección de cómputo de ~173 h a **~66 h**. Los dos concentraban el 85% del tiempo.

### 8.2 Composición final del estudio: 12 modelos

| Origen | Modelos |
|:---|:---|
| Corrida 2026-09-01 (5) | `gemma4:31b-mlx`, `gemma4:latest`, `gemma:latest`, `llama3.2:latest`, `qwen2.5:14b` |
| Corrida 2026-09-03 (7) | `gemma4:12b-mlx`, `qwen3:8b`, `mistral-nemo:latest`, `nuextract:latest`, `llama3.1:8b`, `nemotron-mini:4b`, `deepseek-r1:1.5b` |

**Compatibilidad verificada:** coinciden los nueve parámetros del protocolo entre ambas corridas, y los
conjuntos de modelos son disjuntos sobre el mismo corpus. La fusión para el ANOVA conjunto es válida.

### 8.3 Redacción obligatoria en la tesina
- [ ] Declarar la exclusión como **limitación de hardware**, no como decisión metodológica. Redacción
      sugerida para §7 (Limitaciones), neutra en extensión:
      > «Dos modelos (`sonct988/gemma4-26b…` de 16 GB y `gpt-oss:20b` de 13 GB) quedaron fuera del barrido
      > sobre N=120 por una restricción física del equipo de evaluación (16 GB de RAM), que forzaba
      > paginación a disco y multiplicaba por un orden de magnitud el tiempo de inferencia.»
- [ ] Declarar también la exclusión de los **dos modelos cloud** por límites de cuenta (HTTP 429 y 402),
      no por criterios experimentales.
- [ ] Verificar que **todo conteo de modelos** del informe quede en **12**, coherente con §1.4, §2.5, §4.2,
      §5.1 y §5.3.5. Recordar que la Tabla 2 lista 13 filas porque `gemma4:latest` aparece en dos
      configuraciones de prompt legítimas (ZS-ES y FS-ES).

### 8.4 Coordinación
- [ ] Toda tarea sobre estos documentos debe declararse en [`CURRENT-TASKS.md`](./CURRENT-TASKS.md)
      antes de empezar y actualizarse al terminar. Ver `CLAUDE.md §Coordinación entre Agentes`.

---

## 9. Política de modelos cloud (decisión del autor, 2026-09-03)

**Criterio:** un modelo cloud **se conserva** en la documentación si tiene resultados experimentales que lo
respalden; **se elimina** si nunca llegó a evaluarse.

### 9.1 Estado de los tres modelos cloud

| Modelo | Resultados históricos | Estado actual | Decisión |
|:---|:---|:---|:---|
| `glm-5.1:cloud` | **Ninguno** — cero filas en todo `results/` | HTTP 402 (requiere suscripción); no existe en el registro público | ✅ **Eliminado globalmente** |
| `minimax-m3:cloud` | 30 filas (N=15) + **240 filas (N=120)**, corrida `..._20260824_173036` | HTTP 402 (requiere suscripción) | ✅ **Se conserva** — tiene datos |
| `gemma4:31b-cloud` | 30 filas (N=15), `results/benchmark_results.csv` | HTTP 429 (cuota semanal agotada) | ✅ **Se conserva** como parámetro de comparación |

### 9.2 Tareas pendientes
- [x] Eliminar `glm-5.1:cloud` de la configuración y la documentación. Se conserva únicamente en los
      registros de auditoría y aprendizaje (`FINDINGS.md`, `LEARNING.md §L21-L22`, `AUDITORIA_*`), que
      documentan por qué se retiró.
- [ ] **Etiquetar explícitamente** los resultados de `minimax-m3:cloud` y `gemma4:31b-cloud` como
      **históricos y no re-ejecutables**, indicando el código HTTP y la fecha de la última corrida válida.
      Sin esa etiqueta, un lector asume que podrían reproducirse.
- [ ] Verificar que ninguna tabla del informe presente resultados cloud **sin** esa salvedad.
- [ ] ⚠️ **Resolver la discrepancia de trazabilidad ya detectada** (`BENCHMARKS.md`, nota de trazabilidad):
      la tabla de resultados da `gemma4:31b-cloud` F1 = 0.6754 mientras el archivo crudo da
      F1 = 0.3973 (baseline). Lo mismo ocurre con `minimax-m3:cloud` (tabla 0.6321 vs crudo 0.2011) y
      `gemma4:31b-mlx`. **Requiere decisión del autor sobre cuál es la fuente válida** antes de citar
      cualquiera de esas cifras en la tesina.

### 9.3 Nota sobre el corpus de los resultados cloud
Los resultados de `gemma4:31b-cloud` provienen de `results/benchmark_results.csv`, que contiene
**15 `record_id` únicos → N=15** (las «30 filas» son 15 registros × 2 modos: `baseline` y `rag_enhanced`).
No existen resultados de este modelo sobre N=30: aquella corrida (2026-07-01) solo incluyó `gemma4:31b` y
`gemma4:31b-mlx`, ambos locales.

### 9.4 Refinamiento (2026-09-03): inventario completo de resultados cloud

La tabla de §9.1 listaba una sola corrida por modelo. El inventario completo muestra que **ambos modelos
cloud conservados tienen resultados en dos corridas**, y todos se conservan:

| Modelo | Corrida | Corpus | Filas | Grupos |
|:---|:---|:---:|---:|:---|
| `gemma4:31b-cloud` | `results/benchmark_results.csv` | **N=15** | 30 | `_baseline`, `_rag_enhanced` |
| `gemma4:31b-cloud` | `results/benchmark_balanced_120_20260824_173036/` | **N=120** | 240 | `_baseline`, `_rag_enhanced` |
| `minimax-m3:cloud` | `results/benchmark_results.csv` | **N=15** | 30 | `_baseline`, `_rag_enhanced` |
| `minimax-m3:cloud` | `results/benchmark_balanced_120_20260824_173036/` | **N=120** | 240 | `_baseline`, `_rag_enhanced` |

**Decisión del autor:** se conservan **todos** estos resultados como parámetro de comparación histórica.

### 9.5 ⚠️ Salvedad crítica sobre los resultados RAG de esas corridas

Ambos `run_config.json` **no declaran `rag_mode`**: son anteriores a la introducción de ese flag, por lo que
sus condiciones RAG corresponden al modo **legacy `entities`** (diccionarios de entidades), *no* al
`kb_combined` (KB RAG contextual) usado en la corrida de referencia del 2026-09-01.

**Consecuencia para el informe:**

| Tipo de resultado | ¿Comparable con la corrida 2026-09-01? |
|:---|:---|
| Columnas `_baseline` | ✅ **Sí** — el baseline no usa RAG, la condición es idéntica |
| Columnas `_rag_enhanced` | ❌ **No** — es otra implementación de RAG (`entities` vs `kb_combined`) |

- [ ] Al citar resultados cloud en la tesina, usar **solo las condiciones `_baseline`** para comparaciones
      transversales, o etiquetar explícitamente que la condición RAG es de modo `entities`.
- [ ] No incorporar las filas `_rag_enhanced` de estas corridas al ANOVA conjunto con la corrida
      `kb_combined`: mezclaría dos tratamientos distintos bajo una misma etiqueta.
