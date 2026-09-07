# TODO — Informe Final de Tesina

> Documento de seguimiento del cierre del Informe Final (Hito 5).
> **Política:** estrictamente aditivo. No se elimina contenido previo; los ítems completados se marcan,
> no se borran. Ver `CLAUDE.md` (§Entregables Finales) y `HISTORIAL-CONSOLIDADO.md`.
> **Restricción institucional vigente:** cuerpo ≤ 25 páginas, excluyendo anexos.
> **Margen real: 5 páginas** — el cuerpo mide **20 pp.** (anexos desde la 21, 29 pp. totales), según la
> verificación de `HISTORIAL-CONSOLIDADO.md §9`. *Corrección 2026-09-05: este documento afirmaba antes un
> margen de 1 página basado en una medición de 24 pp. que quedó superada por la corrección de estilos.*

**Última actualización:** 2026-09-03

---

## 1. Entregables y su estado

| # | Entregable | Ruta | Estado |
|:--|:---|:---|:---|
| 1 | Informe final con plantilla UTFSM/MTI (**canónico**) | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | ✅ Vigente — cuerpo **20 pp.** + anexos (29 pp. totales) |
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
- [x] Persistencia del flag `ablation` en `run_config.json` (antes las corridas de análisis comparativo de prompts eran
      indistinguibles de un baseline en su metadata).

### 2.3 Nomenclatura y terminología
- [x] Eliminación del modelo `gemma4-12b-mlx-q8-64k` de **documentación y configuración**: su sufijo `q8` era **falso**
      (el artefacto real es 4-bit NVFP4, 7.71 GB; un q8 real de 12B pesa 12.84 GB). Nombre canónico
      adoptado: `gemma4:12b-mlx`.
      ⚠️ **Corrección 2026-09-05:** la eliminación cubrió documentación y configuración, **no los datos
      experimentales**. El nombre retirado sigue en 14 archivos de `results/`, incluidas **30 filas** de
      `results/benchmark_results.csv`. Ver §10.
- [x] Terminología: «Análisis Comparativo de Prompts» como término principal, con
      «diseño factorial 2×2» y «análisis comparativo de prompts» como sinónimos glosados. Aplicado al `.md`.
      El abstract en inglés conserva *prompt comparative prompt analysis*.
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
- [ ] Corrida en curso: **7 modelos locales** × 2 modos = 1680 filas, `--rag-mode kb_combined`, `--num-workers 9`.
- [ ] Fusionar con la corrida del 2026-09-01 y recalcular un único ANOVA/Tukey.
- [ ] Actualizar §5.3.5 con el resultado consolidado.
- [ ] ⚠️ **El estudio queda con 12 modelos** (ver §8, que corrige este apartado). Los dos cloud no son ejecutables:
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
| 2026-09-03 | Usar «Análisis Comparativo de Prompts» como término principal, conservando los sinónimos técnicos. |
| 2026-09-03 | Ante divergencia en la re-ejecución de N=30, **reemplazar** por el nuevo resultado. |
| 2026-09-03 | Las filas `gemma4:latest (ZS-ES)` y `(FS-ES)` son legítimas y **no deben eliminarse**. |

---

## 5. Documentos de hallazgos y lecciones

| Documento | Contenido |
|:---|:---|
| [`FINDINGS.md`](./FINDINGS.md) | 25 hallazgos (F1–F25) técnicos y documentales, con evidencia e impacto |
| [`LEARNING.md`](./LEARNING.md) | 22 lecciones (L1–L22) derivadas de esos hallazgos, con su aplicación práctica |
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
``.

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
      «diseño factorial 2×2» va en **negrita** y «análisis comparativo de prompts» en *cursiva*. Son 4 selecciones
      manuales en Word.

### 7.4 Verificación final de formato
- [ ] Confirmar que el cuerpo del informe **no excede 25 páginas** excluyendo anexos tras todas las
      correcciones. **Margen disponible: 5 páginas** (cuerpo actual 20 pp.).
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
      > «Dos modelos (`…` de 16 GB y `gpt-oss:20b` de 13 GB) quedaron fuera del barrido
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

---

## 10. 🔴 BLOQUEANTES antes de la defensa (detectados 2026-09-05)

Requieren **decisión del autor**. Ninguno es corregible automáticamente: o exigen datos que ya no existen,
o una fuente que solo tú puedes aportar.

| # | Problema | Ubicación | Por qué bloquea |
|:--|:---|:---|:---|
| 1 | **F1 aritméticamente imposible** en 2 filas: `llama3.2:latest_rag` (0.8783 > cota 0.7646) y `llama3.1:8b_baseline` (0.7667 > cota 0.7333) | `BENCHMARKS.md`, tabla RAG Integration Study | F1 nunca puede superar (P+R)/2. Un revisor lo detecta con aritmética elemental. Los datos crudos no sobreviven ⇒ no recalculables |
| 2 | **`gemma4:31b` y `gemma4:31b-mlx` con métricas byte-idénticas** (67.83/57.29/86.78/0.15/114.20) | Informe, Tabla 2 L375-376 | Dos runtimes distintos no producen resultados idénticos hasta el decimal. Además el 67.83% no tiene respaldo crudo; la única medición independiente da F1=0.6852 |
| 3 | **Cita inventada pendiente**: marcador `[referencia KPMG 2024]` junto a cifras de mercado (USD 12.300 y 87.200 millones) | Informe §1.1, L65 | Sin la fuente real, las cifras no tienen respaldo. Fabricar la cita sería falsificación académica |
| 4 | **Contradicción de hardware**: se declara ejecutar modelos de ~24.7 GB de VRAM sobre 16 GB de memoria unificada | Informe §2.4 (L125) y §3.6 (L210) | Físicamente contradictorio tal como está redactado |
| 5 | **Tabla de eficiencia no reproducible**: VRAM y Tok/s de §5.5 no se derivan de ningún CSV | Informe §5.5, L471-473 | El CSV da 24.607 MB / 22.80 tok/s frente a 24.751 / 27.56 de la tabla |
| 6 | **Tabla de configuraciones de prompt sin corrida de origen**: 0.7169 / 0.6640 / 0.6482 / 0.5874 solo existen en `BENCHMARKS.md` | `BENCHMARKS.md` L195-202 | No trazables a ningún resultado |
| 7 | **Etiqueta `q8-64k` viva en los datos** que alimentan la Tabla 2 (30 filas del CSV) | `results/benchmark_results.csv` | Ver `FINDINGS.md §F26`. Recomendación: documentar la equivalencia en el informe |
| 8 | **Discrepancia tabla vs crudo** en modelos cloud: 0.6754 vs 0.3973 (`gemma4:31b-cloud`), 0.6321 vs 0.2011 (`minimax-m3:cloud`) | `BENCHMARKS.md`, nota de trazabilidad | Requiere decidir cuál es la fuente válida |

### Modelos evaluados sin declarar — ✅ RESUELTO (2026-09-05)
`AGENTS.md §8.6` catalogaba como «Active» a `gliner:medium`, `gemini-3.1-flash-lite`, `gemini-3.5-flash` y
`phi3.5`.
- [x] **Decisión del autor: ninguno forma parte del estudio.** No están entre los 12 modelos evaluados.
      Registrado como nota en `AGENTS.md §8.6`: figuran solo como soporte de la plataforma multi-proveedor
      y **sus métricas no deben citarse como resultados de la tesina**.

---

## 11. Plan priorizado tras la verificación de datos (2026-09-05)

### 11.0 Hallazgo que reordena las prioridades
Las cifras bajas de los modelos cloud en los datos crudos **no miden el rendimiento del modelo**: miden una
corrida contaminada por **fallos de cuota**. Evidencia:

| Modelo | Extracciones fallidas | Recall = 0 | N efectiva |
|:---|---:|---:|---:|
| `gemma4:31b-cloud` | 6 / 15 | 6 / 15 | **9** |
| `minimax-m3:cloud` | 9 / 15 | 10 / 15 | **6** |
| `gemma4:31b-mlx` (local, control) | 0 / 15 | 0 / 15 | 15 |

El log de esa corrida tiene **507 líneas con errores de cuota**. Excluyendo los fallos, `gemma4:31b-cloud`
da **F1 = 0.6622**, muy próximo al 0.6754 de la tabla ⇒ **la tabla refleja el subconjunto exitoso**, no una
cifra inventada. Su defecto real es **declarar N=15 ocultando que 6 fallaron**.

> ⚠️ **No sustituir la tabla por los valores crudos.** Serían métricas contaminadas por fallos de
> infraestructura presentadas como rendimiento del modelo.

### 11.1 🔴 PRIORIDAD ALTA — Instrumentar la causa de fallo
- [ ] `parse_method` no distingue un **fallo de cuota** (HTTP 429/402) de un **fallo de parseo del modelo**:
      ambos quedan como `failed`. Añadir a cada fila el **código HTTP** y la **causa**, para que un fallo de
      infraestructura no vuelva a confundirse con una limitación del modelo.
- [ ] Registrar en el resumen agregado la **N efectiva** y la **tasa de fallo** por modelo.

### 11.2 🔴 PRIORIDAD ALTA — Re-ejecutar los modelos cloud
**Viable ahora.** Verificado el 2026-09-05:

| Cuenta | Estado |
|:---|:---|
| `eahumada@gmail.com` | ❌ HTTP 429 — cuota semanal agotada |
| `eduardo.ahumada@delmartg.com` | ✅ **operativa** |
| `Eahumada@4useguros.com` | ✅ **operativa** |

- [ ] **Requiere `ollama signin`** con una de las cuentas operativas, o arrancar `ollama serve` con
      `OLLAMA_API_KEY` en su entorno. El daemon local es quien autentica contra la nube; las claves de
      `.setenv.sh` no bastan para el proceso ya en marcha.
      ⚠️ Reiniciar `ollama serve` **interrumpe el benchmark en curso** — hacerlo entre corridas.
- [ ] Re-ejecutar `gemma4:31b-cloud` y `minimax-m3:cloud` sobre N=15 con el logging mejorado de §11.1.
- [ ] Verificar que la tasa de fallo sea 0 antes de dar las cifras por buenas.

### 11.3 🟠 Paralelismo: los cloud SÍ pueden correr con los locales
Los modelos cloud **no consumen memoria local** — la inferencia ocurre en el servidor remoto. La
restricción de ejecución serial (un modelo a la vez para que disponga de toda la RAM) **aplica solo a los
modelos locales**.

- [ ] Ejecutar los cloud **en paralelo** con la corrida local en curso, sin esperar a que termine.
- [ ] Mantener la serialización estricta **entre modelos locales**.

### 11.4 🟠 PRIORIDAD MEDIA — Declarar la N efectiva mientras tanto
- [ ] Hasta tener la re-ejecución limpia, la tabla debe declarar junto a cada modelo cloud su **N efectiva**
      y su **tasa de fallo por cuota**. Es honesto y no requiere datos nuevos.

### 11.5 🟡 Filas sin respaldo alguno
- [x] **RESUELTO 2026-09-07.** Tabla «RAG Integration Study»: `llama3.2:latest_rag` (F1 0.8783) y `llama3.1:8b_baseline` (0.7667)
      quedan marcadas **NO VERIFICABLES** en `BENCHMARKS.md` (se conservan por política aditiva); la fuente oficial de
      `llama3.1:8b` es la corrida N=120 re-puntuada (0.4876 / 0.5075). Original:
      tienen F1 **aritméticamente imposibles**, y **ninguno de sus seis valores existe en dato alguno** del
      proyecto (verificado sobre CSV, JSON y logs). No es que el CSV no sobreviva: no hay rastro.
      → Retirar, o marcar como «prototipo temprano, cifras no verificables».
- [x] **RESUELTO 2026-09-07.** Tabla de variantes de prompts sustituida por `ablacion_n15_REMOTO` (zs-en 0.6405 · zs-es 0.6843 ·
      fs-en 0.6332 · fs-es 0.7444). Original: sus 4 cifras (0.7169 / 0.6640 / 0.6482 / 0.5874) no existían en datos.
      Re-ejecutable con `gemma4:latest` (9.6 GB) sobre N=15, 4 configuraciones de prompt.

### 11.6 ⬜ PRIORIDAD BAJA — Aparcado por decisión del autor
- [x] **RESUELTO 2026-09-07** (B2): sustituida por Verified Market Research (15,68 mil M 2020 → 87,17 mil M 2028, CAGR 23,92 %).
      La atribución a KPMG no se sostenía: 12.300 → 87.200 M en cuatro años implica una CAGR del ~63 %. Original: tras
      completar todos los benchmarks.

### 11.7 Orden de ejecución acordado
1. `gemma4:31b` sobre N=15 — **en curso** (local, en solitario)
2. Cloud en paralelo, en cuanto se resuelva el `signin`
3. Reanudar el benchmark principal N=120 (local, en solitario) — pausado en 153/1680
4. Análisis comparativo de prompts con `gemma4:latest` si se decide re-ejecutarla
5. KPMG y cierre documental

---

## 12. Estado del trabajo en curso (2026-09-05, 23:05)

### 12.1 Resultados de la sesión de ejecución

| Tarea | Estado | Detalle |
|:---|:---|:---|
| Recuperar `gemma4:31b` (N=15) | 🔴 **INVIABLE en este hardware** | 19 GB sobre 16 GB de RAM. 0 respuestas en 26 min con 8 workers; **tampoco con 1 worker**. Swap saturado a 16 GB. Ver `FINDINGS.md §F36` |
| Acceso a Ollama Cloud | ✅ **RESTAURADO** | Tras tu `signin`: `gemma4:31b-cloud` operativo. `minimax-m3:cloud` sigue en HTTP 402 (plan de pago) |
| Benchmark principal N=120 | ⏸️ **PAUSADO, checkpoint íntegro** | 153/1680 filas · `gemma4:12b-mlx_baseline` 40/40, `_kb_rag` 11/40 |

### 12.2 🔴 Decisión requerida — fila de `gemma4:31b` en la Tabla 2
No es recuperable aquí. Tres salidas:

| Opción | Consecuencia |
|:---|:---|
| **Retirar la fila** | Tabla íntegramente trazable. Se pierde la comparación GGUF vs MLX |
| **Marcarla no verificable** | Se conserva, con nota de que su origen no consta en `results/` |
| **Ejecutar en equipo con ≥32 GB** | Única vía de recuperar el dato real |

> `gemma4:31b-cloud` es el mismo modelo en remoto y **sí funciona**, pero no sustituye a la fila local:
> son runtimes distintos y esa comparación es justamente lo que la tabla mide.

### 12.3 🔴 PRIORIDAD INMEDIATA — Re-ejecutar `gemma4:31b-cloud` limpio
Desbloqueado por la reautenticación. Corrige la contaminación documentada en `FINDINGS.md §F35`
(6 de 15 extracciones fallidas por cuota, N efectiva 9).

- [x] **HECHO** — `results/cloud_n15_limpio_20260905` (baseline 0.6699 / rag 0.6850, 0 fallos). Alimenta la fila de la Tabla 2 (66.99 %).
- [ ] **Puede correr EN PARALELO** con el benchmark local: los cloud no consumen memoria local.
- [x] **Verificado**: 0 fallos.
- [x] **Comparado**: la Tabla 2 usa ahora 66.99 % (N=15 limpio) y el estudio N=120 usa 0.6238 / 0.6185.

### 12.4 Reglas operativas aprendidas (aplicar de aquí en adelante)
1. **Modelos locales: estrictamente en serie**, uno a la vez con toda la RAM disponible.
2. **Modelos cloud: en paralelo sin restricción** — no consumen memoria local.
3. **Regla de admisión de modelos:** si `tamaño_modelo > RAM_física × 0.7`, no incluirlo en el plan de
   evaluación de esta máquina. Con 16 GB, el techo práctico es **~11 GB**.
   - Esto **excluye retroactivamente**: `gemma4:31b` (19 GB), `gemma4:31b-mlx` (19.4 GB),
`gpt-oss:20b` (13 GB).
   - `gemma4:12b-mlx` (7.7 GB) está dentro del límite, aunque su latencia de ~930 s ya refleja presión.
4. **`ollama signin` NO reinicia el daemon** ⇒ puede hacerse sin interrumpir una corrida (verificado).
5. **Diagnóstico de saturación:** `llama-server` con CPU baja (~30%) y swap alto significa que espera
   disco, no que calcule.

### 12.5 Orden de ejecución actualizado
1. ~~`gemma4:31b` local~~ — **descartado por hardware**
2. **`gemma4:31b-cloud` limpio** — puede empezar ya, en paralelo
3. **Reanudar benchmark principal N=120** — local, en serie, desde 153/1680
4. Análisis comparativo de prompts con `gemma4:latest` (9.6 GB, dentro del límite) si se decide re-ejecutarla
5. KPMG y cierre documental

---

## 13. ✅ EJECUTADO (2026-09-07) — Renombrado a «Análisis de Variantes de Prompts»

> **Cierre 2026-09-07.** La condición de disparo (datos completos) se cumplió con el cierre de benchmarks.
> Aplicado en el informe canónico (§4.3, §5.2, resumen y conclusión 2), en `BENCHMARKS.md` y en `RUNS_INDEX.md`.
> **No se tocaron** el flag `--ablation`, la clave `ablation` de `run_config.json`, los nombres de directorio
> (`ablacion_n15_REMOTO`) ni los registros históricos, según lo previsto en este mismo apartado.

### Detalle original del diferimiento

**Decisión del autor (2026-09-06).** Se aceptan **dos formulaciones**, ambas válidas:

| Término | Dónde encaja mejor |
|:---|:---|
| **«Test de Variación de los Prompts»** | Títulos de sección y referencias al procedimiento. Más corto y nombra el método. |
| **«Análisis de Variantes de Prompts»** | Prosa corrida, cuando se habla del análisis en sí. Fluye mejor dentro de una frase. |

Ambas son intercambiables; usar la que mejor suene en cada contexto. Lo que importa es que **ninguna use
«ablación»**.
Se aplicará **de forma global al final**, cuando haya terminado de generarse toda la evidencia, para no
hacer el cambio dos veces ni desincronizar documentos mientras el equipo remoto sigue entregando.

### Estado actual
El término vigente en toda la documentación es **«Análisis Comparativo de Prompts»** (commit `852ccd5`).
Es correcto y neutro; solo se sustituirá por el definitivo en la pasada final.

### Por qué «variación» es el término correcto
Las cuatro configuraciones evaluadas —zs-en, zs-es, fs-en, fs-es— **son variaciones** del mismo prompt:
cambia el idioma y la presencia de ejemplos, no el prompt en sí. «Variación» describe con exactitud lo que
se manipula, es de uso corriente en español, y **no arrastra ninguna connotación** — que era el motivo de
fondo para abandonar «ablación».

**Prohibido en adelante:** «test de ablación de los prompts», «estudio de ablación» y cualquier variante en
español de ese término.

### Qué habrá que cambiar cuando llegue el momento

| Ámbito | Acción |
|:---|:---|
| **Prosa de documentos vigentes** | Sustituir «Análisis Comparativo de Prompts» → «Test de Variación de los Prompts». Afecta a: informe final (§4.3 y §5.2), `TODO-INFORME-FINAL.md`, `BENCHMARKS.md`, `README.md`, `RUNS_INDEX.md`, `research/rag/WORKLOG.md` |
| **Las dos glosas del informe** | Hoy citan *ablation study* en cursiva como término de la literatura anglosajona. **Mantener así**: preserva la trazabilidad académica sin usar la palabra en español |
| **Identificadores técnicos** | ⚠️ **NO tocar**: el flag `--ablation`, la clave `ablation` de `run_config.json` y los nombres de directorio (`ablacion_n15_REMOTO`, `klepto_N15__ablation__4-prompts__…`). Renombrarlos rompería comandos documentados, scripts del equipo remoto y rutas ya publicadas en el encargo |
| **Registros históricos** | ⚠️ **NO tocar**: Hito 4, carpetas `archive/` y volcados de auditoría |
| **Los `.docx`** | Propagar con `tools/docx_replace_terms.py` (edición quirúrgica; **no** regenerar con pandoc) |

### Condición de disparo
- [x] **EJECUTADO 2026-09-07** (ver §13, cerrado). Condición original: solo cuando el remoto cerrara sus tareas y el ANOVA definitivo estuviera
      calculado. Antes de eso, cualquier cambio global habría que repetirlo.

---

## 14. Anexo — Tareas futuras y reglas para ejecuciones posteriores (2026-09-07)

> **Naturaleza:** este anexo **no lista trabajo pendiente del informe**. Recoge las reglas con las que se
> ejecutarán los benchmarks de aquí en adelante, derivadas de hallazgos ya cerrados. Documento canónico:
> [`RECOMENDACIONES-EJECUCIONES-FUTURAS.md`](./RECOMENDACIONES-EJECUCIONES-FUTURAS.md).

### 14.1 Régimen de *thinking* — decidido y cerrado

| Modelo | Régimen | Fundamento |
|:---|:---|:---|
| `gpt-oss:20b` | **ON, congelado** | Sin razonamiento deja de responder (`recall=0` en 7/15 y 10/15). Su corrida oficial no se toca |
| `qwen3:8b` | **OFF** | +4,2 pp sobre N=120, `recall=0` de 15 → 1, ~10× más rápido |
| `gemma4:12b-mlx`, `gemma4:31b-mlx` | **OFF** | El razonamiento agotaba `num_predict` y vaciaba `content` |

**Decisión aplicada:** **no** se re-ejecutan esos 4 modelos con `think=OFF`. Hacerlo introduciría un segundo
eje de inconsistencia (unos modelos con razonamiento y otros sin él) apoyado en ruido muestral.

### 14.2 Reglas para futuras ejecuciones

1. **No generalizar** el ajuste de *thinking* entre modelos: el efecto es específico de cada uno.
2. **`think` es kwarg de primer nivel** de `Client.chat()`, nunca dentro de `options`: Ollama descarta en
   silencio las claves desconocidas y el modelo corre con su **valor por defecto (ON)**.
3. **Medir antes de cambiar**, con el pipeline real y `thinking` como única variable.
4. **Umbral:** aceptar solo si el ΔF1 es ≥ 0 **en todas las condiciones** y el signo es **estable**. Con
   N=15, descartar |ΔF1| < 0.05.
5. **Exigir mecanismo:** conteo de `recall=0` y latencia, no solo la media de F1.
6. **La latencia debe corroborar la hipótesis:** el razonamiento no puede acelerar. Si «OFF» sale más lento,
   detenerse y explicarlo.
7. **Declarar el régimen** en el `run_config.json` y no mezclar regímenes en silencio.
8. **Comparar solo lo comparable:** si dos corridas dan métricas idénticas fila a fila, tenían la misma
   configuración y no han comparado nada.

### 14.3 Pendiente para el equipo remoto (cuando se retome)

- [ ] Evaluar `qwen3:14b`, `qwen3:32b` y `qwen3:latest` (siguen con thinking ON, sin medir).
- [ ] **Enumerar todos los modelos del estudio con capacidad `thinking`** (`ollama show`): toda corrida
      anterior al fix `743054d` los ejecutó con el razonamiento **activo por defecto**.

- [ ] Si se amplía el estudio, medir el régimen **a N=120**, no a N=15.

---

## 15. 🔒 CIERRE DE BENCHMARKS (2026-09-07)

**Decisión del autor:** se conservan los **13 modelos actuales** y **se cierra la fase de ejecución**. No se
lanzan más corridas. Documento de cierre: [`CIERRE-BENCHMARKS-20260907.md`](./CIERRE-BENCHMARKS-20260907.md).

- **Alcance definitivo del estudio N=120:** **13 modelos × 2 modos**, F = 36.3666, p = 1.2236e-152
  (`results/ANALISIS_CONJUNTO_20260907/`).
- **Integridad:** convención de puntuación única · 0 violaciones de `F1 ≤ (P+R)/2` · 0 filas degeneradas ·
  0 `failed` · `summary` == `CSV` en todas las corridas.
- **`sonct988/gemma4-26b` eliminado del estudio** (commit `33fbe7d`): cuantización *custom* de un usuario, no
  citable ni reproducible. Sin rastro en el árbol de trabajo.

### 15.1 ⚠️ El «12» del informe y el «13» del ANOVA no son el mismo conjunto

Los 12 modelos que declaran §1.4, §3.2 y §5.1 corresponden a la **Tabla 2 (N=15, modo `entities`,
12 modelos en 13 configuraciones)**. El estudio N=120 con KB RAG tiene **13 modelos**. Son conjuntos
distintos y hay que decirlo en el texto: un revisor que lea «12» y luego vea un ANOVA de 13 asumirá que falta
un modelo.

### 15.2 Pendiente documental (ninguna ejecución)

- [x] **A1-A3 aplicadas (2026-09-07)** — sustituciones (`remote_48g/DECISIONES-PENDIENTES-AUTOR.md`).
- [x] **Tabla 2 reconstruida (2026-09-07)** desde los CSV re-puntuados: retirados `gemini-3.1-flash-lite` y `nuextract:latest` (fuera del estudio), aplicar
      A1 (`gemma4:31b` → 0.6912) y resolver las dos filas con cifras idénticas (`gemma4:31b` y
      `gemma4:31b-mlx`, ambas 67.83 %).
- [ ] **(Claude Desktop) Declarar las dos salvedades de datos:** la latencia de `gemma4:31b-cloud` no mide inferencia (está
      cuantizada por el `--request-delay`) y las 7 filas de `nemotron-mini:4b` con telemetría en cero.
- [x] **Renombrado terminológico global** aplicado (§13).
- [ ] **(Claude Desktop) Cierre de formato del `.docx`** (§2.1-2.5) — encargo en `PROMPT-CLAUDE-DESKTOP-20260907.md`. Verificar el límite de
      **25 páginas**: las correcciones B1-B4 añadieron texto.

### 15.3 Decisión del autor aún abierta

- [x] **DECIDIDO (2026-09-07): re-ejecutar la corrida N=30.** Encargo al equipo remoto en
      `ENCARGO-REMOTO-N30-20260907.md` (§3.bis.12), ETA ~9 h. Cuando llegue el resultado se decidirá si
      sustituye a 79.03 % en el cuerpo o si ambas cifras conviven con nota de procedencia.
      **Hasta entonces no tocar la cifra en el informe.**

- [ ] ~~F1 titular de N=30 (79.03 %)~~ *(superado por la decisión anterior)* — aparece en el resumen, §4.1 y la conclusión 1. Está registrado que «el
      nuevo resultado es el oficial y el de julio queda en el WORKLOG», pero **no existe una corrida N=30 limpia
      que lo reemplace**. Decidir entre mantenerlo con nota de procedencia o retirarlo. Nadie debe cambiarlo por
      iniciativa propia.

### 15.4 🔴 Decisión del autor — mojibake en el gold del corpus N=120

Hallazgo del equipo remoto (`FINDINGS.md §F46`), **verificado de forma independiente** por el equipo principal:
las entidades de referencia de `data/benchmark_balanced_120.json` tienen **mojibake** (UTF-8 leído como
Latin-1). **283 de 1 406 (20,1 %)** están afectadas y **66 (4,7 %) son irrecuperables** al umbral de
coincidencia difusa 85, de modo que **el *recall* y el F1 de todo el estudio N=120 están subestimados en torno
a 4,7 pp**.

**Lo importante:** el sesgo es **uniforme entre modelos**. No altera el ranking ni las conclusiones
comparativas — solo los valores absolutos. Los corpus **N=15 y N=30 están limpios**, así que la Tabla 2, §5.2,
§5.3.1–5.3.4 y la re-corrida N=30 **no** están afectados.

**Por qué no se puede arreglar sin re-ejecutar:** corregir el gold es trivial
(`s.encode('latin-1').decode('utf-8')`), pero el *matching* se resuelve en tiempo de inferencia y **las
extracciones crudas por registro no se persistieron** (solo `tp/fp/fn`). No hay forma de re-puntuar sobre datos
guardados, como sí se pudo con el bug del *scorer*.

**Opciones:**

- [ ] **(a) Declarar la limitación y no re-ejecutar (recomendada).** Ya está redactada en §5.3.5 del informe.
      Es práctica estándar cuando el sesgo es conocido, acotado y uniforme. Coste: cero.
- [ ] **(b) Corregir el gold y re-ejecutar el estudio N=120 completo.** Elevaría los valores absolutos ~4,7 pp.
      Coste: **~200 h de cómputo** —el estudio entero— y contradice el cierre de benchmarks.
- [ ] **(c) Corregir el gold y re-ejecutar solo un subconjunto** para cuantificar el efecto real y citarlo como
      corrección estimada, manteniendo las cifras actuales. Coste intermedio; aporta una medición en vez de una
      cota.

### 15.5 Corrección de §15.4 y decisiones sobre `gpt-oss` (2026-09-07 16:35)

**§15.4 quedó mal planteada** y se corrige aquí de forma aditiva. Decía que el mojibake produce «un sesgo
uniforme de ~4,7 pp que no altera el ranking». **Faltaba comprobar la entrada:** el mojibake está también en
el **texto** de los artículos (87 %), y de forma **coherente** con el gold — las 283 entidades corruptas
aparecen **tal cual** en el texto, ninguna corregida (`FINDINGS.md §F48`).

Por tanto el corpus es internamente consistente y **el efecto no es uniforme**: premia al modelo que transcribe
literalmente y penaliza al que normaliza la ortografía. Medido, el Δ entre registros con y sin mojibake va de
**−0.070 a +0.091** según el modelo — **sí podría alterar el ranking**. La opción (a) de §15.4 sigue siendo
viable, pero su justificación ya no es «el sesgo es uniforme» sino «el sesgo está declarado y acotado».

**Terminología obligatoria:** la forma **corrupta** es `JosÃ© Bono`; la **correcta** es **`José Bono`**.
Escribirlo siempre en ese orden.

**Cómo se repara bien:** no basta con arreglar el gold —eso invertiría la injusticia—. Hay que **normalizar
ambos lados al comparar**, aplicando la reparación al gold *y* a la extracción antes del *fuzzy matching*
(~10 líneas en `src/evaluator.py`). Exige re-inferir: las extracciones por registro no se conservaron.

#### Decisión del autor — `gpt-oss:20b`

- [ ] **Re-ejecutar `gpt-oss:20b` completo con `num_predict=4096`** (thinking ON, **mismo corpus y mismo
      evaluador que los demás**, sin tocar el mojibake). El diagnóstico del remoto descartó el bucle de
      repetición y apunta al agotamiento del presupuesto de tokens: 10–40 s por registro al re-ejecutar frente
      a **838 s** en la corrida oficial. **ETA ~1–1,5 h.** El cambio queda **aislado a `gpt-oss`** y el estudio
      sigue siendo comparable. Encargo: adenda de `ENCARGO-REMOTO-GPTOSS-20260907.md`.
- [ ] **Aparte y de alcance global:** decidir si se implementa la normalización de codificación en el
      evaluador, lo que obligaría a re-ejecutar el estudio N=120 completo (~200 h). **No mezclar con lo
      anterior.**
