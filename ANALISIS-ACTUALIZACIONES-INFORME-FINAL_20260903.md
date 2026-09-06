# Análisis de actualizaciones requeridas — Informe Final de Tesina (DOCX)

**Fecha:** 2026-09-03 19:47
**Alcance:** análisis, sin modificar contenido de los entregables.
**Documento analizado:** `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`
(canónico, congelado como `_v1` en `doc/versions/informe_final/`).

> **Concurrencia.** Otra sesión de Claude Code está trabajando sobre este repositorio en este momento
> (`AUDITORIA_CONSISTENCIA_20260903.md` 19:30, `TODO-INFORME-FINAL.md` 19:45, corrida de benchmark
> iniciada 19:31). Este análisis es de solo lectura y no toca ningún archivo compartido. Antes de aplicar
> cualquier cambio debe re-verificarse el estado de los archivos: las marcas de tiempo de referencia están
> en §6.

---

## 1. Qué cambió desde la última revisión del informe

### 1.1 Auditoría de consistencia documental (nueva)
`AUDITORIA_CONSISTENCIA_20260903.md` — 115 hallazgos confirmados con verificación adversarial
(26 altos, 55 medios, 34 bajos), 17 descartados. Reparto por archivo: el `.md` canónico concentra 54;
el DOCX canónico, 11; el DOCX standalone, 7; el resto se reparte entre `BENCHMARKS.md`, `WORKLOG.md`,
`AGENTS.md`, `RUNS_INDEX.md`, `HISTORIAL-CONSOLIDADO.md`, `README.md` y `TODO.md`.

### 1.2 Índice histórico de corridas (nuevo)
`results/RUNS_INDEX.md` cataloga 13 corridas y expone dos hechos con impacto directo en la tesina:

- **La corrida titular N=30 (#7, 2026-07-01) perdió sus datos por registro.** Escribió en `results/` raíz
  y fue sobrescrita el 2026-07-27. Del F1 = 79.03 % que sostiene la hipótesis solo sobrevive la métrica
  agregada en `benchmark_augmented_30.log`. Es la única corrida N=30 jamás ejecutada.
- **Combinaciones nunca ejecutadas:** N=30 con RAG, N=30 con comparación de prompts, N=120 con
  `kb_guidelines` y con `kb_fewshot`, y el cruce prompt × RAG.

### 1.3 Corridas y decisiones nuevas
- **En curso (19:31):** `results/benchmark_balanced_120_kbrag_9models/` — 9 modelos locales × 2 modos,
  `--rag-mode kb_combined`, 9 workers. Solo hay checkpoint y log; **sin resultados consolidados aún**.
- **Descartada:** `results/DESCARTADA_ragmode_incorrecto_142604/`.
- **Los dos modelos cloud no son ejecutables:** `gemma4:31b-cloud` responde HTTP 429 (cuota agotada) y
  `minimax-m3:cloud` HTTP 402 (requiere plan de pago). **El estudio quedará con 14 modelos, no 16.**
- **Excepción de soberanía de datos** registrada en `AGENTS.md §2`: modelos cloud autorizados solo como
  línea base sobre el corpus público.

### 1.4 Correcciones de código y nomenclatura
- `src/config.py` incorpora un **guardarraíl**: `assert_not_results_root()` aborta cualquier corrida que
  intente escribir en `results/` raíz, con el incidente de julio documentado en el propio código.
- Nombre canónico **`gemma4:12b-mlx`**; eliminado el sufijo `q8` de `BENCHMARKS.md` y `AGENTS.md`.
  Sobrevive solo en artefactos crudos de dos corridas y en respaldos (no requiere acción sobre la tesina,
  salvo verificar que el nombre proscrito no aparezca en ninguna tabla).
- Terminología: **«Comparación de Configuraciones de Prompt»** como término principal, con glosa de
  *diseño factorial 2×2* y el sinónimo «estudio de ablación» conservado. **Ya aplicado en el `.md`
  canónico; aún no en ninguno de los tres DOCX.**

### 1.5 Divergencia entre fuente y entregable
El `.md` canónico y el DOCX canónico se han desincronizado en ambos sentidos:

| Contenido | `.md` canónico | DOCX canónico |
|:---|:---:|:---:|
| Terminología «Comparación de Configuraciones de Prompt» + glosa 2×2 | ✅ | ❌ |
| §4.1.3 (corpus N=120 conmutable) y §5.3.5 (validación complementaria) | ✅ | ✅ |
| Anexos D, E, F y G | ❌ | ✅ |
| Maquetación institucional (leyendas, encabezado, 20 pp. de cuerpo) | n/a | ✅ |

Antes de tocar el DOCX hay que decidir **cuál es la fuente de verdad**. Regenerar el DOCX desde el `.md`
con pandoc destruiría la maquetación institucional y los cuatro anexos; editar solo el DOCX perpetúa la
divergencia. Recomendación: incorporar primero al `.md` los anexos D–G, y a partir de ahí mantener el
`.md` como fuente única, aplicando la maquetación como paso final reproducible.

---

## 2. Actualizaciones al DOCX que dependen de datos (bloqueadas)

| # | Sección afectada | Cambio requerido | Bloqueada por |
|:-:|:---|:---|:---|
| D1 | §5.3.5, §5.6.5, Anexo E, §7.2 | Sustituir el subconjunto de 5 modelos por el resultado consolidado (corrida en curso + corrida del 2026-09-01), con un **único** ANOVA/Tukey recalculado sobre el conjunto fusionado | Corrida de 9 modelos en curso |
| D2 | §5.1, §4.2, §2.5, resumen, abstract | Fijar el alcance real del estudio en **14 modelos** y explicar por qué los dos cloud quedan fuera (cuota/suscripción), en lugar de «16 modelos» | D1 |
| D3 | Resumen, abstract, §5.3.1, §5.3.3, §6.1, §7.1, Tabla 1 (§2.5) | Reemplazar el F1 = 79.03 % por el valor de la re-ejecución N=30. Decisión del autor ya registrada: **el nuevo resultado será el oficial**; el de julio se conserva en el WORKLOG por trazabilidad | Descarga de `gemma4:31b` / `gemma4:31b-mlx` + re-ejecución |
| D4 | §5.3.5, §7.2 | Reescribir «los 11 modelos restantes quedan pendientes» según el alcance final | D1 |
| D5 | §4.1, §5.3 | Declarar que la corrida N=30 fue re-ejecutada y por qué (pérdida de datos por sobrescritura), o bien acotar el alcance de lo que se afirma sobre ese corpus | D3 |

**Riesgo asociado a D3:** si la re-ejecución no reproduce el 79.03 %, cambia el resultado titular de la
tesina y con él la validación de la hipótesis. Es el mayor riesgo abierto del proyecto.

---

## 3. Actualizaciones al DOCX que **no** dependen de datos (ejecutables ya)

### 3.1 Coherencia numérica y de alcance — prioridad alta

| Hallazgo | Sección | Corrección |
|:---|:---|:---|
| A1/A3/M25 | §1.4-Obj.2, §2.5, §4.2, título §5.1, §5.3.5, Anexo E | Conteo real: **12 modelos distintos en 13 configuraciones** (`gemma4:latest` aparece dos veces, ZS-ES y FS-ES, decisión del autor: son legítimas). Hoy conviven «15», «16» y «13 configuraciones» |
| A5 | §6.1 | La hipótesis se confirma solo con N=30 (79.03 %); en el corpus real N=120 el mejor F1 es 59.25 %, **bajo el umbral de 70 %**. Debe explicitarse el alcance de la confirmación. *Punto de mayor riesgo en la defensa oral* |
| A4/M2/A20 | Tabla 2 (§5.1), §5.5, §6.3 | Recalcular Tok/s/B = Tok/s ÷ parámetros(B) y usar el mismo valor en las tres secciones. `gemma4:31b` y `gemma4:31b-mlx` figuran con las seis métricas idénticas, contradiciendo §5.3.1 y §5.5 |
| A23 | §5.6.1 | El «−33 % vs baseline» del dict-RAG mezcla dos mini-benchmarks: son −32.5 puntos porcentuales, o −57.8 % en variación relativa |
| M9 | Resumen, §1.4, §5.5, §7.1 | Reducción de costos: 60–80 % en el resumen frente a 99.4 % en resultados y conclusiones |
| M10 | §6.1, §7.2 | El objetivo F1 ≥ 85 % no aparece en el capítulo 1, donde la hipótesis fija ≥ 70 % |
| M8 | Resumen, abstract, §3.3 | «16 proveedores de modelos» frente a los cuatro proveedores que documenta §3.3 |
| M6 | §4.2, Tabla 2 | `gemma:latest` se usa en §5.3.5, §5.6.5 y §6.5 sin estar declarado |
| M5 | §5.3.5 | Los 5 modelos del subconjunto son todos locales; el texto dice «locales y en la nube» |
| M13 | §3.6, §4.5 | Se declaran modelos de ~24.7 GB de VRAM sobre hardware de 16 GB |
| M14 | §5.6.5 | `gemma4:latest` (9B) clasificado como modelo grande > 10B |
| A24/A25/M11/M12 | §4.1, §4.1.1 | Cifras del corpus medidas: Gold Standard 4.832,9 caracteres de media (no ~800); N=30 con 1,2 PER y 2,3 ORG por artículo y 202 caracteres (no 2,1/1,3 y 187) |

### 3.2 Texto y terminología

| Hallazgo | Sección | Corrección |
|:---|:---|:---|
| A7/M20 | Abstract, referencia [18] | Abstract corrupto: «balanceado Kleptotrace/CoNLL-2002/CoNLL-2002» (castellano dentro del inglés y nombre duplicado) y URL inválida `https://Kleptotrace/CoNLL-2002.org` |
| A6/M21 | §4.1.2 | «datos reales balanceados generados por LLM» en una subsección titulada «Corpus Sintético»: residuo de un reemplazo global mal aplicado |
| A11/M18/M19 | §4.3, §5.2, resumen, §1.4, §2.5 | Propagar «Comparación de Configuraciones de Prompt» + glosa del diseño factorial 2×2, ya vigente en el `.md` |
| B10 | Resumen / abstract | Dejaron de ser equivalentes: el resumen perdió «+7.4 puntos de F1», la arquitectura pub/sub, los proveedores, las familias de modelos y el sufijo «M4», y añadió una mención a N=120 que el abstract no tiene |
| M26/B5/B30 | §1.1, §4.4 | «billones» como traducción de *billions* (10⁹) y en la definición del índice Tok/s/B |
| M16/B27/B28 | Bibliografía y citas | Citas autor-año en un documento que declara IEEE numerado; «[referencia KPMG 2024]» sin entrada; «Borne» vs. «Bourne»; falta la entrada [12] y la lista llega a [20] con 19 entradas |
| B9 | §5.1 | Los Hallazgos 1 y 3 citan cifras de modelos que ya no están en la Tabla 5 reducida (`gemma4:31b-cloud` 66.29 %, `llama3.2` 18.73 Tok/s/B): o se reponen las filas o se reescriben los hallazgos |
| B6 | §5.3.5 | Remite a §6.3 por «la meseta de rendimiento», que §6.3 no documenta |
| B1/B26/B2/B33/B18/B29 | varias | 8.13 % vs 8.10 % de alucinaciones; 8B–32B vs 8B–31B; `llama3.1:latest (8b)` vs `llama3.1:8b`; versiones de software declaradas (Python 3.13 / Streamlit 1.58) frente a las reales (3.14.7 / 1.60.0) |

### 3.3 Estructura y maquetación

| Hallazgo | Ubicación | Corrección |
|:---|:---|:---|
| M22 | §2.5, §3.1, §5.1 | Llamadas a tablas desactualizadas tras la renumeración institucional: el texto remite a «Tabla 1» y «Tabla 2» donde ahora están la 2, la 3 y la 5 |
| B7 | §2.5 y §3.1 | Dos objetos distintos citados como «La Tabla 1» |
| M23 | §5.6 | Salto de numeración: no existe §5.6.6 (su tabla se trasladó al Anexo D.5); se pasa de 5.6.5 a 5.6.7 |
| M24 | Anexos | Las subsecciones D.6, D.7 y D.8 quedaron físicamente **después** del Anexo F |
| B8 | Anexo D | El bloque de cierre («Informe Final de Tesina — Magíster… Julio 2026») quedó incrustado entre D.3 y D.4 |
| B4 | §4.2, tablas de §5 | `gemma4:12b` se declara entre los modelos evaluados pero no aparece en ninguna tabla de resultados |

### 3.4 Presupuesto de páginas
El cuerpo está hoy en **20 páginas** sobre un límite de 25. Las correcciones de §3.1 (sobre todo el
matiz de §6.1) y la consolidación de §5.3.5 añaden texto y filas de tabla. Hay margen suficiente, pero
debe re-verificarse tras cada bloque de cambios. *Nota: `TODO-INFORME-FINAL.md` declara «24 pp. de
cuerpo»; ese dato quedó obsoleto — la verificación posterior del mismo día midió 20 pp.*

---

## 4. Entregables paralelos que también requieren actualización

| Entregable | Estado | Acción requerida |
|:---|:---|:---|
| `Informe_Final_Tesina_NER.docx` (standalone) | ⚠️ **Incompleto** | Le faltan §4.1.3 y §5.3.5 completas (cero ocurrencias de `4.1.3`, `5.3.5` y `10.2096` en su XML). Decidir si se mantiene como entregable o se declara obsoleto en favor del canónico |
| `2026-07-04_Borrador-Informe-Final-Tesina.md` | Fuente canónica | Le faltan los anexos D–G que sí están en el DOCX (M26) |
| `2026-07-04_Borrador-Informe-Final-Tesina.docx` | Derivado | Se regenera desde el `.md` con pandoc; hereda sus 54 hallazgos |
| `HISTORIAL-CONSOLIDADO.md` | Vigente | 4 hallazgos: cuerpo de 24 pp. vs 20 pp. (M29), «tarea 11» inexistente en la tabla de §7 (M30), «de 40 a 27 páginas» vs 29 totales (B15) |

---

## 5. Secuencia recomendada

1. **Congelar `_v1`** — hecho (`doc/versions/informe_final/Informe_Final_Tesina_NER_v1.docx`).
2. **Decidir la fuente de verdad** entre `.md` y DOCX (§1.5). Sin esta decisión, cualquier corrección se
   duplica o se pierde.
3. **Aplicar el bloque de §3** (no depende de datos) → congelar **`_v2`** y re-verificar las 25 páginas.
4. **Esperar** la corrida de 9 modelos y la re-ejecución de N=30.
5. **Aplicar el bloque de §2** (D1–D5) → congelar **`_v3`**.
6. **Sincronizar** los entregables paralelos de §4.
7. **Revisión final del autor** → congelar **`_v4`** como versión de entrega.

---

## 6. Marcas de tiempo de referencia (para detectar cambios concurrentes)

| Archivo | Tamaño | Modificado |
|:---|---:|:---|
| `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` | 201.666 B | 2026-09-03 17:35:15 |
| `Informe_Final_Tesina_NER.docx` | 44.747 B | 2026-09-03 15:24:53 |
| `HISTORIAL-CONSOLIDADO.md` | 18.414 B | 2026-09-03 17:35:56 |
| `AUDITORIA_CONSISTENCIA_20260903.md` | 129.907 B | 2026-09-03 19:30:02 |
| `TODO-INFORME-FINAL.md` | 7.089 B | 2026-09-03 19:45:27 |
| `research/rag/WORKLOG.md` | 18.703 B | 2026-09-03 17:35:35 |
| `…/2026-07-04_Borrador-Informe-Final-Tesina.md` | 67.880 B | 2026-09-03 17:06:20 |

SHA-256 del DOCX canónico congelado como `_v1`: `6b53ebd4b1b7a37700392ea6f41d7c1e7b498fbd359d7424003460941eab9275`
