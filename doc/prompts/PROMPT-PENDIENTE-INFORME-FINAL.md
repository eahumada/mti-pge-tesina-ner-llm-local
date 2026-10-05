# PROMPT — Pendientes del Informe Final de Tesina

**Proyecto:** Tesina MTI/UTFSM — Sistema NER soberano con LLM locales
**Autor:** Eduardo Mauricio Ahumada Gallardo
**Creado:** 2026-09-03
**Uso:** este archivo es a la vez (a) el registro de tareas pendientes y (b) el prompt que debe
entregarse a la sesión que ejecute el cierre. La §5 contiene el texto listo para pegar.

> **Concurrencia.** Pueden coexistir dos sesiones sobre este repositorio: **Claude Code** en el equipo del
> autor (ejecuta benchmarks, edita código y la fuente Markdown) y **Claude Desktop / Cowork** (maqueta y
> verifica el DOCX). Antes de escribir cualquier archivo compartido debe comprobarse su marca de tiempo
> contra la tabla de §2. El formateo final del DOCX se ejecuta **una sola vez, al final**, cuando el
> contenido ya no cambia.

---

## 1. Estado y reparto de responsabilidades

| Bloque | Contenido | Dónde se ejecuta |
|:---|:---|:---|
| **A** | Benchmarks, ANOVA/Tukey, recuperación del corpus N=30 | Claude Code (equipo del autor: Ollama, venv) |
| **B** | Correcciones de contenido sobre la fuente Markdown canónica | Claude Code |
| **C** | Sincronización de entregables y decisiones del autor | Autor + Claude Code |
| **D** | **Maquetación, verificación de formato y versionado del DOCX** | **Claude Desktop (esta sesión)** |

El bloque D es el último y **no debe adelantarse**: cada corrección de contenido posterior obliga a
repetirlo íntegro.

---

## 2. Instantánea de referencia (2026-09-03 19:55)

| Archivo | Tamaño | Modificado |
|:---|---:|:---|
| `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` (canónico) | 201.666 B | 2026-09-03 17:35 |
| `Informe_Final_Tesina_NER.docx` (standalone, incompleto) | 44.747 B | 2026-09-03 15:24 |
| `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` | 67.840 B | 2026-09-03 **19:52** 🔄 |
| `AUDITORIA_CONSISTENCIA_20260903.md` | 129.907 B | 2026-09-03 19:30 |
| `TODO-INFORME-FINAL.md` | 13.555 B | 2026-09-03 **19:51** 🔄 |
| `HISTORIAL-CONSOLIDADO.md` | 18.414 B | 2026-09-03 17:35 |
| `research/rag/WORKLOG.md` | 18.703 B | 2026-09-03 17:35 |

🔄 = en edición activa por la otra sesión al momento de escribir este archivo. El bloque B está **en
curso**: la fuente Markdown canónica y el TODO cambiaron entre las 19:47 y las 19:52, de modo que el
estado real de las tareas B-1…B-15 debe releerse en `TODO-INFORME-FINAL.md` antes de empezar el cierre.

**Versión congelada vigente:** `doc/versions/informe_final/Informe_Final_Tesina_NER_v1.docx`
SHA-256 `6b53ebd4b1b7a37700392ea6f41d7c1e7b498fbd359d7424003460941eab9275` — cuerpo 20 pp., total 29 pp.

---

## 3. Tareas pendientes

Estado: ⬜ pendiente · 🔄 en curso · ✅ hecho · ⛔ bloqueada

### Bloque A — Datos y benchmark (Claude Code)

| ID | Asunto | Detalle | Registrada | Depende de | Estado |
|:--:|:---|:---|:---|:---|:--:|
| A-1 | Corrida N=120 con 9 modelos | `results/benchmark_balanced_120_kbrag_9models/`, 9 modelos locales × 2 modos, `--rag-mode kb_combined`, 9 workers | 2026-09-03 | — | 🔄 |
| A-2 | Fusión de corridas y ANOVA/Tukey único | Fusionar A-1 con `benchmark_balanced_120_20260901_140421` y recalcular un **único** ANOVA/Tukey sobre el conjunto consolidado | 2026-09-03 | A-1 | ⛔ |
| A-3 | Alcance final del estudio | Fijar **14 modelos** (no 16): `gemma4:31b-cloud` responde HTTP 429 (cuota) y `minimax-m3:cloud` HTTP 402 (suscripción) | 2026-09-03 | A-2 | ⛔ |
| A-4 | Re-ejecución del corpus N=30 | La corrida titular (2026-07-01) perdió los datos por registro al ser sobrescrita el 2026-07-27; solo sobrevive la métrica agregada en `benchmark_augmented_30.log` | 2026-09-03 | Descarga de `gemma4:31b` y `gemma4:31b-mlx` | ⛔ |
| A-5 | Decisión sobre el F1 titular | Registrada por el autor: **el nuevo resultado será el oficial**; el 79.03 % de julio se conserva en el WORKLOG por trazabilidad | 2026-09-03 | A-4 | ⛔ |
| A-6 | Cierre de la matriz de cobertura | Combinaciones nunca ejecutadas: N=30 con RAG, N=30 con comparación de prompts, N=120 con `kb_guidelines` y con `kb_fewshot` | 2026-09-03 | A-1 | ⬜ |

### Bloque B — Correcciones de contenido sobre la fuente Markdown (Claude Code)

| ID | Asunto | Detalle | Registrada | Estado |
|:--:|:---|:---|:---|:--:|
| B-1 | Conteo de modelos | Unificar en **12 modelos distintos / 13 configuraciones** (`gemma4:latest` aparece legítimamente como ZS-ES y FS-ES). Hoy conviven «15», «16» y «13 configuraciones» en §1.4, §2.5, §4.2, §5.1 y §5.3.5 | 2026-09-03 | ⬜ |
| B-2 | Alcance de la hipótesis (§6.1) | Se confirma solo con N=30 (79.03 %); en el corpus real N=120 el mejor F1 es 59.25 %, bajo el umbral de 70 %. Debe explicitarse. **Punto de mayor riesgo en la defensa oral** | 2026-09-03 | ⬜ |
| B-3 | Abstract corrupto | «balanceado Kleptotrace/CoNLL-2002/CoNLL-2002» (castellano dentro del inglés y nombre duplicado) y URL inválida `https://Kleptotrace/CoNLL-2002.org` en la referencia [18] | 2026-09-03 | ⬜ |
| B-4 | §4.1.2 autocontradictorio | «datos reales balanceados generados por LLM» en una subsección titulada «Corpus Sintético» | 2026-09-03 | ⬜ |
| B-5 | Índice Tok/s/B | Recalcular Tok/s ÷ parámetros(B) y unificar entre Tabla 2 (§5.1), §5.5 y §6.3 | 2026-09-03 | ⬜ |
| B-6 | Métricas idénticas | `gemma4:31b` y `gemma4:31b-mlx` con las seis métricas iguales en Tabla 2, contradiciendo §5.3.1 y §5.5 | 2026-09-03 | ⬜ |
| B-7 | Delta del dict-RAG | El «−33 % vs baseline» son −32,5 puntos porcentuales (o −57,8 % relativo); hoy mezcla dos mini-benchmarks distintos | 2026-09-03 | ⬜ |
| B-8 | Terminología | Propagar «Comparación de Configuraciones de Prompt» + glosa del diseño factorial 2×2 (ya vigente en el `.md`, ausente en los tres DOCX) | 2026-09-03 | ⬜ |
| B-9 | Cifras del corpus | Gold Standard: 4.832,9 caracteres de media (no ~800). N=30: 1,2 PER y 2,3 ORG por artículo, 202 caracteres (no 2,1/1,3 y 187) | 2026-09-03 | ⬜ |
| B-10 | Coherencias menores | Reducción de costos 60–80 % vs 99,4 %; objetivo F1 ≥ 85 % ausente del capítulo 1; «16 proveedores» vs los 4 de §3.3; `gemma:latest` no declarado en §4.2; §5.3.5 dice «locales y en la nube» siendo los 5 locales; VRAM de 24,7 GB sobre hardware de 16 GB; `gemma4:latest` (9B) clasificado como > 10B | 2026-09-03 | ⬜ |
| B-11 | Bibliografía | Citas autor-año en documento IEEE numerado; «[referencia KPMG 2024]» sin entrada; «Borne» vs «Bourne»; falta la entrada [12]; la lista llega a [20] con 19 entradas | 2026-09-03 | ⬜ |
| B-12 | Resumen ≠ Abstract | Restituir la equivalencia: el resumen perdió «+7.4 puntos de F1», la arquitectura pub/sub, los proveedores, las familias de modelos y el sufijo «M4», y añadió una mención a N=120 ausente en el abstract | 2026-09-03 | ⬜ |
| B-13 | «billones» | Traducción incorrecta de *billions* (10⁹) en §1.1, §4.4 y en la definición de Tok/s/B | 2026-09-03 | ⬜ |
| B-14 | Hallazgos de §5.1 | Los Hallazgos 1 y 3 citan cifras de modelos que ya no figuran en la Tabla 5 reducida (`gemma4:31b-cloud` 66.29 %, `llama3.2` 18.73 Tok/s/B) | 2026-09-03 | ⬜ |
| B-15 | Resto de la auditoría | Aplicar los hallazgos medios y bajos restantes de `AUDITORIA_CONSISTENCIA_20260903.md` | 2026-09-03 | ⬜ |

### Bloque C — Decisiones y sincronización (autor)

| ID | Asunto | Detalle | Registrada | Estado |
|:--:|:---|:---|:---|:--:|
| C-1 | **Fuente de verdad** | El `.md` tiene la terminología nueva pero no los anexos D–G; el DOCX tiene los anexos y la maquetación institucional pero no la terminología. Recomendación: incorporar D–G al `.md` y dejarlo como fuente única | 2026-09-03 | ⬜ |
| C-2 | Destino del standalone | `Informe_Final_Tesina_NER.docx` carece de §4.1.3 y §5.3.5 completas. Completarlo o declararlo obsoleto | 2026-09-03 | ⬜ |
| C-3 | Discrepancia «16 modelos» en §5.1 | Ajustar el título o reponer las filas faltantes desde `results/` | 2026-09-03 | ⬜ |
| C-4 | Menciones históricas a la organización | Definir criterio uniforme para los documentos de hitos anteriores | 2026-09-03 | ⬜ |
| C-5 | Palabras clave ACM 2012 | Incorporarlas o registrar la decisión de omitirlas (recomendación institucional, no obligatoria) | 2026-09-03 | ⬜ |
| C-6 | Actualizar documentos de estado | `TODO-INFORME-FINAL.md` declara «24 pp. de cuerpo» (real: 20); `HISTORIAL-CONSOLIDADO.md` tiene la «tarea 11» inexistente y «de 40 a 27 páginas» frente a 29 totales | 2026-09-03 | ⬜ |

### Bloque D — Cierre de formato en Claude Desktop (esta sesión)

| ID | Asunto | Detalle | Registrada | Estado |
|:--:|:---|:---|:---|:--:|
| D-1 | Regenerar el DOCX desde la fuente | Solo si C-1 resuelve a favor del `.md`: `pandoc … --reference-doc` y volver a aplicar D-2…D-9 | 2026-09-03 | ⬜ |
| D-2 | Estilos ausentes | Verificar/definir `Table` y `Compact` en `styles.xml` | 2026-09-03 | ⬜ |
| D-3 | Encabezado | Unificar las tres variantes con imágenes **en línea** | 2026-09-03 | ⬜ |
| D-4 | Márgenes y saltos | Superior 3,3 cm; resumen y cada capítulo en página propia | 2026-09-03 | ⬜ |
| D-5 | Tablas | Anchos proporcionales; leyendas `table caption` sobre cada tabla, numeradas | 2026-09-03 | ⬜ |
| D-6 | Estructura XML | `sectPr` como último hijo de `w:body`; anexos en orden; numeración literal con `numId=0` | 2026-09-03 | ⬜ |
| D-7 | Limpieza | Sin páginas en blanco, sin líneas estiradas, sin listas en línea | 2026-09-03 | ⬜ |
| D-8 | Verificación | Render a PDF, cuerpo ≤ 25 pp., sin solapamientos, cifras trazables | 2026-09-03 | ⬜ |
| D-9 | Versionado | Congelar `_v2`, `_v3`, `_v4` según corresponda y registrar en `VERSIONES.md` | 2026-09-03 | ⬜ |

---

## 4. Procedimiento de cierre en Claude Desktop (bloque D, detallado)

Ejecutar **en este orden**, íntegro, sobre una copia de trabajo. Cada paso incluye su criterio de
aceptación verificable.

### D-0. Preparación
- Confirmar que los bloques A, B y C están cerrados y que nadie más está editando (comparar marcas de
  tiempo contra §2, actualizadas).
- Copiar el DOCX vigente a la sesión y trabajar sobre esa copia; **nunca** editar la plantilla
  `plantilla_final-2026.docx` ni los respaldos `.bak_*`.

### D-1. Origen del contenido
- Si C-1 resolvió a favor del `.md`: regenerar con
  `pandoc <fuente.md> -o <salida.docx> --reference-doc=<docx anterior>` y **volver a aplicar D-2…D-9**,
  porque pandoc no conserva ninguna de esas correcciones.
- Si se decidió editar el DOCX directamente: saltar a D-2.

### D-2. Estilos ausentes (causa raíz del descuadre histórico)
- Verificar que `word/styles.xml` define `Table` (tabla) y `Compact` (párrafo). El contenido generado por
  pandoc los referencia y la plantilla institucional **no los trae**; sin ellos las tablas se renderizan
  apiladas en una sola columna, sin bordes, inflando el documento ~13 páginas.
- `Table`: basada en `TableNormal`, bordes `single sz=4 color=808080` en los seis lados, márgenes de celda
  28/72/28/72 twips. `Compact`: basada en `Normal`, `spacing before=20 after=20 line=200 exact`, `sz=16`.
- **Criterio:** ninguna tabla se renderiza como columna única; todas muestran bordes.

### D-3. Encabezado
- Las tres partes (`header1` par, `header2` predeterminado, `header3` primera página) deben ser idénticas
  y usar imágenes **en línea** dentro de una tabla de 3 columnas (2736 / 4374 / 1728 twips): banner UTFSM a
  la izquierda, las tres líneas institucionales centradas a 7,5 pt, logo MTI a la derecha.
- Las imágenes flotantes (`wp:anchor`) se solapan con el texto en Word: convertirlas a `wp:inline`.
- En los párrafos que contienen imagen, el interlineado debe ser `auto`; un `lineRule="exact"` recorta la
  imagen a la altura de línea.
- **Criterio:** en el PDF, el encabezado termina ≥ 12 pt por encima de la primera línea del cuerpo, y el
  logo no pisa el texto en ninguna página.

### D-4. Márgenes y saltos de página
- `pgMar`: superior 1871 twips (3,3 cm), inferior 1418 (2,5 cm), laterales 1701 (3 cm), `header`/`footer`
  851 (1,5 cm).
- Salto de página antes del `Resumen:` y antes de **cada** encabezado de capítulo. Atención: el capítulo 1
  usa el estilo nativo `Heading 1` y el resto el estilo `heading1` de la plantilla — deben tratarse ambos.
- Eliminar los párrafos vacíos que preceden a un encabezado con salto forzado (generan páginas en blanco).
- **Criterio:** resumen en página propia; nueve capítulos empezando en página nueva; cero páginas en blanco.

### D-5. Tablas y leyendas
- Ancho útil 8838 twips. Repartir las columnas en proporción al contenido (mínimo 700 twips), fijando
  `tblW dxa`, `tblLayout fixed`, `gridCol` y `tcW` de cada celda.
- Toda fila añadida por script debe replicar el estilo `Compact` y la estructura `tcPr` de sus hermanas;
  una fila con formato distinto altera el cálculo de altura y puede desplazar la tabla dos páginas.
- Leyenda **sobre** cada tabla, estilo `table caption`, centrada, numerada correlativamente
  («Tabla N. Título»). Las figuras, si las hubiera, llevan leyenda **debajo** con `figure caption`.
- **Criterio:** ninguna palabra partida en los encabezados de columna; numeración de tablas sin saltos;
  las llamadas del texto («la Tabla N…») coinciden con la numeración real.

### D-6. Estructura XML
- `w:sectPr` debe ser el **último hijo** de `w:body`. Al insertar contenido al final es fácil dejarlo en
  medio, lo que produce un documento inválido.
- Anexos en orden alfabético (A, B, C, D con sus D.1…D.n, E, F, G); ningún bloque de cierre incrustado
  entre subsecciones.
- Numeración de encabezados: literal en el texto y `numPr` con `numId=0`. **Nunca** reactivar la
  numeración automática de la plantilla: comparte `numId` entre niveles y no reinicia los contadores.
- **Criterio:** el documento abre sin advertencias; la numeración de §5.6 y de los anexos es continua.

### D-7. Limpieza tipográfica
- Dividir en párrafos independientes los párrafos justificados que contienen saltos de línea manuales
  (producen líneas estiradas), conservando la negrita de los prefijos («Hallazgo 1:», «Nota Cronológica:»).
- Convertir las listas escritas en línea («…: - Ítem 1. - Ítem 2.») en párrafos de viñeta.
- Verificar que ningún párrafo de texto corrido use el estilo `programcode`.
- **Criterio:** sin líneas con espaciado anómalo; sin listas embebidas en párrafo.

### D-8. Verificación final
Convertir a PDF (`soffice --headless --convert-to pdf`) y comprobar, con evidencia:

1. **Extensión:** páginas del cuerpo (portada → referencias, sin anexos) **≤ 25**.
2. **Resumen:** ≤ 200 palabras, sin referencias y sin describir la organización del documento.
3. **Introducción:** ≤ 3 páginas.
4. **Páginas en blanco:** ninguna, salvo la final del PDF.
5. **Solapamientos:** en cada página, la primera línea del cuerpo queda bajo el encabezado y la última
   sobre el pie.
6. **Tablas:** todas con bordes, columnas legibles y leyenda numerada encima.
7. **Cifras:** cada valor citado es trazable a un archivo bajo `results/`.
8. **Anexos:** presentes A–G, en orden, y el Anexo G (declaración de uso de IA) actualizado si el reparto
   de trabajo cambió.

### D-9. Versionado y registro
- Congelar la versión: copiar a `doc/versions/informe_final/Informe_Final_Tesina_NER_v<N>.docx`,
  sin sobrescribir ninguna existente.
- Registrar en `doc/versions/informe_final/VERSIONES.md`: número, fecha, SHA-256, páginas de cuerpo y
  total, y el motivo del cambio.
- Añadir una entrada **aditiva** a `research/rag/WORKLOG.md` y actualizar `HISTORIAL-CONSOLIDADO.md`.
- Entregar el DOCX al autor y dejar copia en la raíz del proyecto.

---

## 5. Prompt listo para pegar

> Vas a ejecutar el **cierre de formato** del informe final de tesina (bloque D de
> `PROMPT-PENDIENTE-INFORME-FINAL.md`). El contenido ya está congelado: **no cambies texto, cifras ni
> conclusiones**; tu trabajo es exclusivamente de maquetación, verificación y versionado.
>
> 1. Lee `PROMPT-PENDIENTE-INFORME-FINAL.md` §4 completo y sigue los pasos D-0 a D-9 en ese orden.
> 2. Trabaja sobre `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` en
>    `/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local`. No toques
>    `plantilla_final-2026.docx` ni los respaldos `.bak_*`.
> 3. Antes de escribir, comprueba las marcas de tiempo de §2: puede haber otra sesión de Claude Code
>    editando. Si algún archivo cambió, avísame antes de continuar.
> 4. Verifica cada paso renderizando a PDF y midiendo; no des por bueno nada sin evidencia. Presta especial
>    atención a la causa raíz histórica: si las tablas se ven apiladas o sin bordes, faltan los estilos
>    `Table` y `Compact` en `styles.xml` (paso D-2).
> 5. Al terminar, entrégame el informe de verificación de D-8 con las ocho comprobaciones, congela la
>    versión siguiente en `doc/versions/informe_final/` y registra el cambio en `VERSIONES.md`, en
>    `research/rag/WORKLOG.md` y en `HISTORIAL-CONSOLIDADO.md`.
> 6. Sé aditivo: no elimines historia. Lo que salga del cuerpo se traslada a los anexos o al historial
>    consolidado, nunca se borra.

---

## 6. Reglas permanentes

1. **Aditividad.** No se elimina historia: se condensa en el cuerpo y se traslada al anexo o al historial.
2. **Trazabilidad.** Toda cifra del informe corresponde a un archivo versionado bajo `results/`.
3. **Inmutabilidad de versiones.** `_v1`, `_v2`, `_v3`… nunca se sobrescriben.
4. **Documentos históricos intactos.** `doc/organized/Hito_1..4/`, el `WORKLOG.md` de la raíz y los
   respaldos `.bak_*` no se modifican.
5. **Formato al final.** El bloque D se ejecuta una sola vez, cuando el contenido ya no cambia.
6. **Verificar antes de escribir.** Con dos sesiones activas, toda escritura va precedida de una
   comprobación de marca de tiempo.
