# Tesina MTI/UTFSM — Reconocimiento de entidades con LLM locales

Estudio comparativo de trece modelos de lenguaje ejecutados localmente sobre la tarea de reconocimiento de
entidades nombradas en noticias de sanciones financieras, con y sin recuperación aumentada por conocimiento.

Este fichero es el **índice de la raíz**, que acumula medio centenar de documentos. Describe qué es cada uno y cuáles siguen
vigentes, para que no haya que abrirlos uno a uno.

## Los entregables

| Rol | Ruta |
|:---|:---|
| Fuente canónica del informe | `doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md` |
| Entregable con plantilla institucional | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx` |
| Versión entregada al profesor guía | `doc/versions/enviados/` (es la verdad de referencia sobre el alcance del estudio) |
| Código y datos del experimento | `repos/ner-llm-entity-benchmark/` |

La regla de extensión, la política aditiva y el resto de restricciones están en `CLAUDE.md`.

## Normas para agentes

`CLAUDE.md`, `AGENT.md`, `ANTIGRAVITY.md` y `GEMINI.md` fijan las reglas del proyecto para cada herramienta.
`CLAUDE.md` es el más completo y el que se mantiene al día; los otros tres derivan de él.

## Estado vigente

Estos documentos describen dónde está el trabajo hoy y son los que hay que leer primero.

| Documento | Para qué sirve |
|:---|:---|
| `CURRENT-TASKS.md` | Qué agente trabaja en qué. Se lee y se actualiza **antes** de tocar nada |
| `ESTADO-RECORRIDA-20260908.md` | Avance de la re-corrida completa en el equipo de 48 GB. Se regenera con `tools/estado_recorrida.py` |
| `DECISIONES-PENDIENTES-20260908.md` | Las siete decisiones que esperan al autor y no puede tomar un agente |
| `TODO-INFORME-FINAL.md` | Pendientes del informe |
| `PROPAGACION-PENDIENTE-DOCX-20260908.md` | Qué cambios del Markdown no han llegado aún a los `.docx` |
| `CIERRE-RECORRIDA-PROCEDIMIENTO.md` | Los pasos a seguir cuando la re-corrida termine |

## Conocimiento acumulado

| Documento | Contenido |
|:---|:---|
| `FINDINGS.md` | Hallazgos numerados `§F<n>`: qué se encontró y con qué evidencia |
| `LEARNING.md` | Lecciones numeradas `§L<n>`: qué se aprendió del error, para no repetirlo |
| `RECOMENDACIONES-EJECUCIONES-FUTURAS.md` | Verificaciones obligatorias antes de dar por buena una métrica |
| `HISTORIAL-CONSOLIDADO.md` | Trazabilidad de decisiones y versiones |
| `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` | Preguntas probables de la mesa y dónde está calculada cada respuesta |
| `DEFENSE_CHECKLIST.md` | Lista de comprobación previa a la defensa |

## Verificación

`tools/verificar_informe.py` pasa **25 comprobaciones** sobre el Markdown canónico: referencias cruzadas,
tablas, bibliografía, higiene del entregable, coherencia entre cifras publicadas y datos crudos, y extensión.
Una comprobación que no examina nada se marca como **vacía**, no como superada.

```
python3 tools/verificar_informe.py          # las 25, sin red
python3 tools/verificar_informe.py --red    # además abre las URL de la bibliografía
```

**La forma corta no comprueba la bibliografía.** Verificar que las URL responden exige salir a la red y vive
tras `--red`; sin esa bandera se informa de cero fallos sin haber abierto una sola (`FINDINGS §F80`). Hoy
`--red` deja un fallo vivo y debe seguir así: la referencia [37] apunta al repositorio, que es privado hasta
que se complete la purga.

`tools/autoprueba_verificador.py` comprueba lo contrario: que el verificador **no apruebe a ciegas**. Esconde
cada artefacto por turno y exige que se entere. Si alguno pudiera faltar sin que ninguna comprobación lo
notase, esa comprobación estaría devolviendo el valor del éxito por haber mirado el sitio equivocado
(`LEARNING.md §L57`).

Los demás scripts de `tools/` regeneran artefactos concretos, y todos leen de las fuentes primarias para que
el documento y los datos no puedan divergir en silencio:

| Script | Qué produce |
|:---|:---|
| `generar_figuras_informe.py` | Las dos figuras del informe |
| `generar_tabla7.py` | La Tabla 7; con `--validar` comprueba que reproduce la publicada |
| `composicion_fp.py` | La composición de los falsos positivos por categoría, con control contra el consolidado |
| `estado_recorrida.py` | `ESTADO-RECORRIDA-20260908.md`, con la firma del corpus calculada y no escrita a mano |
| `robustez_estadistica.py` | Friedman y post-hoc pareado; con `--validar` reproduce los artefactos publicados |
| `efecto_emparejamiento_duplicado.py` | El efecto del doble conteo del emparejamiento sobre las cifras antiguas |
| `desfase_documentos.py` | Qué documentos de estado han envejecido respecto de lo que describen |
| `docx_replace_terms.py` | Ediciones de texto en los `.docx` preservando el formato |

## Documentos fechados

Los ficheros con fecha en el nombre son **registro de un momento**, no estado actual:

- **Encargos a otros agentes**: `PROMPT-*`, `ENCARGO-REMOTO-*`, `ADENDA-*`, `ALERTA-*`, `CORRECCION-*`,
  `URGENTE-*`. Casi todos cumplidos; se conservan porque documentan qué se pidió y con qué justificación.
  Los dirigidos al equipo de 48 GB viven además en `remote_48g/`.
- **Auditorías e informes**: `VEREDICTO-REVISION-GLOBAL-20260908.md`, `AUDITORIA_CONSISTENCIA_20260903.md`,
  `INVENTARIO-DATOS-INCORRECTOS-20260908.md`, `INFORME-AVANCE-20260906.md`, `REPORTE-SESION-20260906.md`,
  `ANALISIS-ACTUALIZACIONES-INFORME-FINAL_20260903.md`.
- **Seguridad**: `SEGURIDAD-CLAVE-GOOGLE-20260908.md` y `SOLICITUD-GITHUB-PURGA-20260908.md` documentan una
  credencial expuesta en el historial, ya revocada, y la purga pendiente. **El repositorio no debe hacerse
  público hasta que esa purga se complete**; el porqué está en `LEARNING.md §L43`.

## Documentos históricos

Anteriores al cierre del estudio, se conservan como registro y **no reflejan el estado actual**:
`BACKLOG.md`, `EXECUTIVE_SUMMARY.md`, `F1_IMPROVEMENT_ROADMAP.md`, `GEMMA_MODELS_INVESTIGATION.md`,
`GEMMA_QUICK_START.md`, `REPORTS_INDEX.md`, `THESIS_PROJECT_ANALYSIS_REPORT.md`, `TODO.md`,
`CIERRE-BENCHMARKS-20260907.md`.

`WORKLOG.md` de la raíz es **histórico y no se modifica**. El registro de trabajo vigente es
`research/rag/WORKLOG.md`.

## Los registros de ejecución se conservan

Los `benchmark.log` y los datos crudos de cada corrida no se editan ni se borran: no son datos del estudio,
son la prueba de qué se ejecutó, y este proyecto ya los ha necesitado para diagnosticar dos fallos. La regla
completa, con su corolario sobre artefactos que afirman frente a artefactos que atestiguan, está en
`CLAUDE.md`.
