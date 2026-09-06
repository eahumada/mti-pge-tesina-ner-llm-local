# HISTORIAL CONSOLIDADO — Tesina NER con LLM Locales (MTI/UTFSM)

**Autor:** Eduardo Mauricio Ahumada Gallardo
**Profesor Guía:** José Luis Martí Lara
**Última actualización:** 2026-09-03
**Propósito de este archivo:** conservar, en un único lugar y con el máximo detalle relevante, toda la
información que fue **condensada, reubicada o resumida** en el documento final de tesina durante el ajuste
al límite institucional de 25 páginas, junto con el cronograma que guía las modificaciones finales del
documento. Nada de lo aquí registrado se perdió: o permanece en el cuerpo del informe, o fue trasladado a
los Anexos D–G, o queda archivado en este historial.

---

## 1. Estado de los documentos

| Documento | Ruta | Estado |
|:---|:---|:---|
| Informe final (plantilla UTFSM/MTI) | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | **Vigente** — cuerpo **20 pp.**, anexos desde la 21, 29 pp. totales (verificado 2026-09-03, §9; la cifra intermedia de 24 pp. es anterior a la corrección de estilos) |
| Respaldo previo al ajuste 25 pp. | `doc/organized/Hito_5_Tarea4_Informe_Final/…docx.bak_pre-cumplimiento-25pp` | Archivo histórico, no modificar |
| Informe standalone (sin plantilla) | `Informe_Final_Tesina_NER.docx` | ⚠️ **INCOMPLETO** — le faltan íntegras §4.1.3 (corpus real N=120) y §5.3.5 (ANOVA F=10.2096 / p=2.873×10⁻¹⁵); verificado: cero ocurrencias de «4.1.3», «5.3.5» y «10.2096» en su `word/document.xml`, mientras el borrador y la plantilla sí las contienen. Además, **pendiente** de aplicar el ajuste de 25 pp. |
| Borrador Hito 5 | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md/.docx` | Vigente con §4.1.3 y §5.3.5 aditivas |
| Registro de trabajo vigente | `research/rag/WORKLOG.md` | Vigente (aditivo) |
| Registro de trabajo técnico vigente | `repos/ner-llm-entity-benchmark/WORKLOG.md` | Vigente (aditivo) |
| Registro de trabajo histórico | `/WORKLOG.md` (raíz del proyecto) | Histórico, no modificar |

---

## 2. Requisitos institucionales aplicados (`Instrucciones Informe Final de Tesina/`)

Fuentes: `tesinas-finales-2026.pdf`, `ieee-citationref.pdf`, `examen-grado-orientacion.pdf`,
`plantilla_final-2026.docx`.

| Requisito | Exigencia | Estado |
|:---|:---|:---|
| Extensión del cuerpo | ≤ 25 páginas, excluyendo anexos | ✅ **20 páginas** — holgura real de 5 pp. (verificado en §9; la medición previa de 24 pp. quedó superada) |
| Resumen | ≤ 200 palabras, sin referencias, sin describir la organización del documento | ✅ 163 palabras |
| Introducción | ≤ 3 páginas, cerrando con un párrafo de síntesis de la organización | ✅ 2 páginas |
| Marco Teórico / Estado del Arte | Capítulo obligatorio | ✅ Capítulo 2 |
| Leyendas de tabla | Estilo `table caption`, centradas, **sobre** la tabla, numeradas correlativamente | ✅ 23 tablas |
| Leyendas de figura | Estilo `figure caption`, **bajo** la figura | ✅ No aplica (sin figuras) |
| Referencias | Formato IEEE, estilo `referenceitem` | ⚠️ Pendiente de revisión ítem por ítem |
| Papel y márgenes | Carta, 3 cm / 2.5 cm | ✅ Heredado de la plantilla |
| Tipografía | Times New Roman 10 pt (estilos `Normal` / `p1a`) | ✅ Heredado de la plantilla |
| Anexos | Sin límite propio (≤ 25 pp. adicionales) | ✅ Anexos A–G |
| Clasificación ACM 2012 en palabras clave | Recomendado | ⚠️ Opcional, no incorporado |

---

## 3. Contenido reubicado a los Anexos (íntegro, sin pérdida)

| Origen en el cuerpo | Contenido | Destino |
|:---|:---|:---|
| §3.3 | Snippet de la interfaz `LLMProvider` (patrón Factory/Facade) | Anexo A |
| §4.1.1 | Protocolo completo Paso 1–5 de generación del corpus sintético N=30 + prompt de generación literal | **Anexo F** |
| §4.3.3 | Los tres ejemplos few-shot completos (persona sancionada, organización sancionada, caso PEP) | Anexo B |
| §5.1 | Tabla completa del benchmark general (13 configuraciones, N=15) | **Anexo E** |
| §5.6.1 | Tabla de flujo «RAG Original (Degradado)» | Anexo D.1 |
| §5.6.1 | Tabla de degradación Baseline vs. RAG-Dict | Anexo D.6 |
| §5.6.2 | Tabla de flujo «KB RAG (Mejorado)» | Anexo D.2 |
| §5.6.2 | Tabla de reglas de la base de conocimientos | Anexo D.8 |
| §5.6.3 | Implementación técnica completa: 4 modos de operación, colecciones ChromaDB, flags CLI, templates de inyección diferenciados | Anexo D.3 |
| §5.6.4 | Catálogo de guías tipológicas y ejemplares few-shot | Anexo D.4 |
| §5.6.5 | Mini-benchmark de validación preliminar N=5 | Anexo D.7 |
| §5.6.6 | Comparación cronológica RAG v1.0 vs. v1.1 | Anexo D.5 |

En el cuerpo, cada bloque reubicado quedó reemplazado por un resumen de una a tres oraciones con
referencia explícita al anexo correspondiente.

---

## 4. Texto condensado en el cuerpo — detalle de lo suprimido

Se conservan aquí los pasajes que fueron reescritos de forma más compacta. Ninguna cifra experimental fue
eliminada: la verificación automatizada confirmó que **el 100 % de los valores porcentuales del documento
original sigue presente** en la versión vigente.

### §4.1.2 Validez estadística del corpus sintético
- *Suprimido (TLC):* «El TLC establece que, para N ≥ 30 observaciones independientes, la distribución de la
  media muestral se aproxima a una distribución normal independientemente de la distribución poblacional
  subyacente. Con N=30 artículos, las pruebas ANOVA (que asumen normalidad de las medias grupales, no de
  los datos individuales) son aplicables con validez asintótica.»
- *Suprimido (independencia):* «El diseño experimental garantiza esta independencia al procesar cada
  artículo de forma aislada sin contexto de artículos previos.»
- *Suprimido (validez de constructo):* «(1) la distribución temática del corpus sintético replica la del
  corpus real (Kleptotrace/CoNLL-2002); (2) las entidades provienen de una fuente oficial de sanciones
  reales (OpenSanctions); y (3) la capacidad del LLM para generar texto coherente con el dominio financiero
  ha sido validada empíricamente (el mismo modelo que genera los artículos es el que se evalúa, creando una
  condición de evaluación conservadora). Este enfoque es metodológicamente análogo al uso de paráfrasis
  automáticas para aumento de corpus en NLP, práctica ampliamente aceptada en la literatura
  [Brown et al., 2020; Borne, 2024].»
- *Suprimido (consistencia entre corpus):* la cifra comparativa del corpus real N=15 (`gemma4:31b`:
  **67.83 %**) y la frase «sin saltos discontinuos que indicarían artefactos del aumento. La diferencia es
  atribuible a la menor complejidad promedio de los artículos breves del corpus sintético, lo que es
  esperado y documentado».

### §4.3.1–4.3.2 Prompting few-shot
- *Suprimido:* la estructura canónica de un prompt few-shot en bloque de código
  (`[Instrucción de sistema] / [Ejemplo n: Entrada] / [Ejemplo n: Salida esperada] / [Tarea real]`).
- *Suprimido (formato de salida):* «Sin este anclaje, los LLMs tienden a variar el formato de respuesta
  entre artículos, dificultando el parseo programático.»
- *Suprimido (umbral semántico):* «Este criterio no puede especificarse exhaustivamente en texto
  descriptivo, pero se transmite implícitamente mediante 2-3 ejemplos contrastivos.»
- Las tres funciones cognitivas (formato, umbral semántico, adaptación al dominio) se conservan en el
  cuerpo, fusionadas en un solo párrafo.

### §5.4 Taxonomía de errores NER
Las tres categorías (Boundary Errors, Type Confusion, Extrinsic Hallucinations) y sus ejemplos
(«Isabel dos Santos, hija del expresidente»; «Sonangol» clasificada como LOC) se conservan íntegramente,
fusionadas en un párrafo único en lugar de tres viñetas.

### §5.6.1 Semantic Mismatch
- *Suprimido:* los ejemplos literales de entidades recuperadas incorrectamente
  (**«GRANJA LA SIERRA LTDA.»**, **«Reina Esperanza Ornelas Cintrón»**) y la mención explícita del modelo de
  embeddings sobre artículos de 300–800 palabras. Se conserva el mecanismo del fallo, la cifra de caída de
  Recall (**62.8 % → 21.6 %**) y la referencia al informe
  `research/rag/2026-08-31_analisis_contenido_rag_base_conocimientos.md`.

### §5.6.5 y §6.5 KB RAG
Se fusionaron los párrafos de «Hallazgo clave», «patrón crítico», «modelos grandes», «modelos
pequeños/medianos» e «implicación práctica» en un único párrafo. Se conservan todas las cifras
(**+25.3 %**, **+12.0 %**, **+8.9 %**, Δ ≈ 0 para modelos > 10B, **+1.2 pp** de Recall en `gemma4:31b-mlx`).

### §4.5 Infraestructura y §5.6 nota cronológica
Fusionadas en un párrafo cada una, sin pérdida de datos (hardware, versiones de software, checkpointing,
fechas del ciclo 31 de agosto – 1 de septiembre de 2026).

---

## 5. Correcciones de integridad detectadas y aplicadas

1. **Filas huérfanas de tabla (§5.1).** El texto plano `nemotron-mini:4b | … | deepseek-r1:1.5b | …`
   había quedado fuera de la tabla real como residuo de una conversión Markdown → DOCX. Ambas filas fueron
   incorporadas a la tabla y el texto residual eliminado. La tabla pasó de 11 a 13 configuraciones.
2. **Discrepancia de recuento.** El título de §5.1 declara «16 Modelos» pero la tabla consolidada contiene
   13 configuraciones (12 modelos distintos más una variante de prompt). **Pendiente de decisión del autor:**
   ajustar el título o recuperar las filas faltantes desde `results/`.
3. **Numeración automática de encabezados.** Los encabezados nuevos incorporados a los anexos heredaban la
   numeración multinivel nativa de la plantilla, produciendo prefijos erróneos (`1.1`, `1.1.49`). Se aplicó
   el mismo criterio ya vigente en el documento: `numId = 0` por párrafo y numeración literal en el texto.
4. **Páginas en blanco.** Se detectaron dos páginas completamente vacías. Causas: (a) una fila de tabla
   añadida programáticamente sin el estilo de párrafo `Compact` de sus filas hermanas, lo que alteraba el
   cálculo de altura y desplazaba la tabla dos páginas; (b) párrafos vacíos residuales antes de encabezados
   de capítulo con salto de página forzado. Corregidas ambas: se recuperaron **5 páginas**.
5. **Nomenclatura de cuantización (registro previo, WORKLOG 2026-09-03 tarde).** El modelo derivado de 12B
   con sufijo `q8` no era q8: la auditoría del registro de Ollama arrojó `MIXED_PRECISION`, capas `NVFP4`
   (4 bits), `kv_cache FP8`, ≈ 5.14 bits/peso (7.71 GB para 12B), frente a los 12.84 GB de un q8 real.
   **RESUELTO (2026-09-03).** Por decisión del autor se adoptó el tag upstream `gemma4:12b-mlx` como nombre
   canónico y se eliminaron todas las referencias al nombre derivado en `BENCHMARKS.md` (fila de resultados
   F1=0.1206, entrada de `run_config` y línea del snapshot de `ollama list`), `src/config.py`,
   `run_benchmark.sh` y ambos WORKLOG vigentes (`research/rag/WORKLOG.md` y `repos/ner-llm-entity-benchmark/WORKLOG.md`). La tesina (`.docx`) nunca lo mencionó (verificado). El tamaño de
   contexto pasa a documentarse como parámetro de ejecución (`num_ctx`), no como parte del nombre.
6. **Corpus mal nombrado en el registro histórico (nota aditiva, no editable en origen).** La entrada del
   2026-07-01 de `/WORKLOG.md` (líneas 18–19) atribuye a `gemma4:31b` un F1 de **67.83 %** sobre
   `benchmark_balanced_120.json` y una suite de 16 modelos. Es un anacronismo: ese corpus entró al
   repositorio el 2026-09-01 y su primera corrida es del 2026-08-24 (`results/RUNS_INDEX.md`, fila #10).
   El 67.83 % corresponde a la corrida #6 sobre `kleptotrace.json` (N=15, 15 modelos). `/WORKLOG.md` es
   histórico y no se edita: la corrección queda registrada aquí. La tesina sí atribuye correctamente el
   67.83 % al corpus real N=15.

---

## 6. Trazabilidad de los corpus y resultados

| Corpus | Archivo | N | Naturaleza | Uso en la tesina |
|:---|:---|:---:|:---|:---|
| Kleptotrace/CoNLL-2002 | `data/kleptotrace.json` | 15 | Real, anotación experta | Benchmark general §5.1 |
| Aumentado sintético | `data/kleptotrace_augmented_30.json` | 30 | Generado por `gemma4:31b`, entidades de OpenSanctions, ground truth verificado a mano | Validación estadística principal §5.3 (F1 = 79.03 %) |
| Balanceado real | `data/benchmark_balanced_120.json` | 120 | Real (15 Kleptotrace + 105 CoNLL-2002 ES muestreados) | Validación complementaria §5.3.5 y estudio KB RAG §5.6 |
| CoNLL-2002 ES completo | `data/conll2002_es.json` | 833 | Real, público | Fuente de muestreo |

Ambos corpus coexisten y son conmutables mediante el flag `--data-file` de `src/main.py`; el corpus
sintético **no fue descartado ni reemplazado**.

Resultados vigentes de §5.3.5: `results/benchmark_balanced_120_20260901_140421/` — 5 modelos en modo
baseline y KB RAG, N=120 por grupo, **F = 10.2096**, **p = 2.873 × 10⁻¹⁵**.

---

## 7. Cronograma para las modificaciones finales del documento

Orden de ejecución recomendado. Cada tarea indica su condición de entrada, el criterio de término y el
riesgo asociado.

| # | Tarea | Entrada requerida | Criterio de término | Riesgo |
|:--:|:---|:---|:---|:---|
| 1 | **Completar benchmark N=120 con los 11 modelos restantes** | Descarga de modelos en Ollama finalizada (~60 GB) y `venv` operativo | `results/` con las 16 configuraciones y `statistical_report.md` regenerado | Alto (tiempo de cómputo) |
| 2 | **Recalcular ANOVA/Tukey sobre los 16 modelos** | Tarea 1 completa | Nuevo F, p y matriz Tukey documentados | Bajo |
| 3 | **Actualizar §5.3.5 en los tres documentos** (informe plantilla, informe standalone, borrador) | Tarea 2 completa | Reemplazo del «subconjunto de 5 modelos» por los 16; tabla del Anexo E ampliada | Medio (revalidar 25 pp.) |
| 4 | **Corregir la nomenclatura `q8` de forma transversal** | Ninguna | Sin ocurrencias de `q8` para `gemma4-12b-mlx` en tesina ni en código/documentación | Bajo |
| 5 | **Resolver la discrepancia «16 modelos» vs. 13 configuraciones** en §5.1 | Decisión del autor | Título y tabla coherentes | Bajo |
| 6 | **Revisar las referencias contra IEEE** (`ieee-citationref.pdf`) | Ninguna | Iniciales antes del apellido, *et al.* desde tres autores, corchetes en el texto, un ítem por número, estilo `referenceitem` | Bajo |
| 7 | **Aplicar el mismo ajuste de 25 pp. al informe standalone** | Tareas 3–6 | Cuerpo ≤ 25 pp. en `Informe_Final_Tesina_NER.docx` | Medio |
| 8 | **Decidir sobre las menciones históricas a la organización vinculada** | Decisión del autor | Criterio uniforme documentado en el WORKLOG | Bajo |
| 9 | **Evaluar palabras clave con clasificación ACM 2012** | Ninguna | Palabras clave añadidas o decisión de omitirlas registrada | Bajo |
| 10 | **Verificación final** (siempre la última en ejecutarse) | Todas las anteriores | Recuento de páginas del cuerpo ≤ 25, sin páginas en blanco, numeración correlativa correcta, todas las cifras trazables a `results/` | — |
| 11 | **Reincorporar al cuerpo parte del material de los Anexos D–F** (candidato: tabla completa del benchmark general, Anexo E, en §5.1) — *ejecutar antes de la tarea 10* | Decisión del autor | Tabla del Anexo E restituida en §5.1 (o decisión de omitirla registrada) y cuerpo aún ≤ 25 pp. | Medio |
| 12 | **Completar `Informe_Final_Tesina_NER.docx`**: reinsertar §4.1.3 y §5.3.5 desde el `.md` vigente | Ninguna | Las cadenas «4.1.3», «5.3.5» y «10.2096» presentes en el `.docx` | Medio |

### Reglas permanentes para cualquier modificación futura

1. **Aditividad.** Nunca eliminar historia: condensar en el cuerpo y trasladar el detalle a los anexos o a
   este historial.
2. **Trazabilidad.** Toda cifra del informe debe corresponder a un archivo versionado bajo `results/`.
3. **Verificación de extensión.** Tras cada edición, reconvertir a PDF y confirmar que los Anexos comienzan
   en la página 26 o antes.
4. **Numeración.** Los encabezados llevan numeración literal en el texto y `numId = 0`; nunca reactivar la
   numeración automática de la plantilla.
5. **Formato de tablas.** Toda fila añadida programáticamente debe replicar el estilo de párrafo `Compact`
   y la estructura `tcPr` de sus filas hermanas.
6. **Documentos históricos.** Los archivos bajo `doc/organized/Hito_1..4/`, el `/WORKLOG.md` de la raíz del
   proyecto y los respaldos `.bak_*` no se modifican. `research/rag/WORKLOG.md` y
   `repos/ner-llm-entity-benchmark/WORKLOG.md` **sí** son registros vigentes y se actualizan de forma aditiva.

---

## 8. Registro de la sesión 2026-09-03 (ajuste de cumplimiento)

- Lectura íntegra de los tres instructivos oficiales y del `plantilla_final-2026.docx`.
- Diagnóstico inicial: cuerpo de **35 páginas** contra un límite de 25; resumen de **230 palabras**;
  ausencia de leyendas de tabla con el estilo institucional.
- Estrategia autorizada por el autor: **mover + condensar**.
- Resultado: cuerpo de **24 páginas**, resumen de **163 palabras**, **23 leyendas** de tabla con estilo
  `table caption`, anexos **D, E, F y G** creados, dos páginas en blanco eliminadas y dos filas de datos
  recuperadas.
- Verificación automatizada: ninguna tabla perdida (22 → 23, por el desdoblamiento de la tabla del
  benchmark general en versión resumida y versión completa) y ningún valor porcentual ausente.
- Se añadió el **Anexo G — Declaración de Uso de Inteligencia Artificial**, redactado sobre la base del
  historial de commits y de los WORKLOG, distinguiendo el trabajo intelectual del autor del apoyo
  instrumental de la IA.

---

## 9. Corrección del renderizado (2026-09-03, cierre)

### Causa raíz de la mala maquetación
El documento fusionado referenciaba dos estilos **inexistentes** en `styles.xml`, heredados de la
conversión pandoc → DOCX:

- `w:tblStyle="Table"` — aplicado a las 23 tablas.
- `w:pStyle="Compact"` — aplicado a los párrafos de las celdas.

Sin esas definiciones, todas las tablas se renderizaban **apiladas en una sola columna y sin bordes**, con
grandes huecos en blanco. Ese solo defecto inflaba el informe en 13 páginas. Al definir ambos estilos
(bordes finos grises de 0.5 pt, márgenes de celda y párrafo compacto de 8 pt), las tablas recuperaron su
forma y el documento pasó de 40 a 27 páginas sin quitar una sola línea de contenido; las correcciones de
maquetación de la tabla siguiente (saltos de página por capítulo, salto antes del Resumen, margen superior
a 3.3 cm) lo llevaron a las **29 páginas** del estado final.

### Correcciones aplicadas

| Defecto | Corrección |
|:---|:---|
| `w:sectPr` en medio del cuerpo, con los anexos D–G después (XML inválido) | Restituido como último hijo de `w:body` |
| Tres encabezados distintos; dos con imágenes flotantes que se solapaban con el texto | Unificados en una tabla de 3 columnas con imágenes **en línea**: banner UTFSM, texto centrado, logo MTI |
| Imágenes en línea recortadas | Interlineado `exact` reemplazado por `auto` en las celdas con imagen |
| Cuerpo pegado al encabezado | Margen superior a 3.3 cm (laterales 3 cm, inferior 2.5 cm) |
| Columnas que partían palabras («gemma4:l atest») | Anchos proporcionales al contenido sobre el ancho útil de 8838 twips |
| Resumen a continuación de la portada | Salto de página antes del Resumen |
| Capítulo 1 sin salto de página | Salto añadido (usaba el estilo nativo `Heading 1`, no `heading1`) |
| Líneas estiradas en párrafos justificados | Saltos manuales convertidos en párrafos independientes; negrita restaurada en prefijos («Hallazgo 1:») |
| Listas escritas en línea («… : - Ítem 1. - Ítem 2.») | Convertidas en viñetas reales (4 párrafos) |
| Página en blanco al final | Párrafos vacíos finales eliminados |

### Estado final verificado

- **29 páginas** totales; **cuerpo de 20 páginas** (portada, resumen y capítulos 1–8); anexos desde la 21.
- Sin páginas en blanco intermedias, sin solapamiento con encabezado ni pie.
- Resumen/Abstract en página propia; los nueve capítulos comienzan en página nueva.

### Consecuencia para el cronograma

Con el defecto de estilos corregido quedan **5 páginas de holgura** respecto al límite de 25. La reducción
de contenido decidida antes (mover + condensar) se hizo sobre un diagnóstico equivocado: el exceso no venía
del contenido sino del renderizado roto. Queda a decisión del autor **reincorporar al cuerpo** parte del
material trasladado a los anexos D–F —el candidato natural es la tabla completa del benchmark general
(Anexo E) en §5.1—. Se añade como tarea 11 del cronograma (§7).
