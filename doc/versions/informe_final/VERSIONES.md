# Versionado del Informe Final de Tesina

Registro de versiones congeladas del informe final. **Solo lectura**: una vez publicada, una versión no
se modifica nunca; cualquier cambio produce la versión siguiente.

## Convención

| Elemento | Regla |
|:---|:---|
| Archivo de trabajo (mutable) | `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`, en la raíz del proyecto |
| Versión congelada | `doc/versions/informe_final/Informe_Final_Tesina_NER_v<N>.docx` |
| Numeración | Entera y correlativa: `_v1`, `_v2`, `_v3`… Sin sufijos de fecha ni de estado |
| Cuándo se congela | Al cerrar un bloque de cambios coherente (correcciones documentales, incorporación de resultados nuevos, entrega) |
| Trazabilidad | Cada versión se registra abajo con fecha, SHA-256, extensión y el cambio que la origina |
| Inmutabilidad | Nunca se sobrescribe una versión existente. Si el contenido cambia, se crea la siguiente |

## Registro

| Versión | Fecha | SHA-256 (12) | Cuerpo | Total | Contenido / motivo |
|:---|:---|:---|:---:|:---:|:---|
| `_v1` | 2026-09-03 17:35 | `6b53ebd4b1b7` | 20 pp. | 29 pp. | Línea base tras el ajuste al formato institucional: cuerpo bajo el límite de 25 páginas, resumen de 163 palabras, 23 leyendas de tabla con estilo `table caption`, anexos D–G, encabezado unificado con imágenes en línea, estilos `Table`/`Compact` definidos y estructura XML del `sectPr` restituida. |

| `_v2` | 2026-09-07 17:22 | `600c424ff991` | 21 pp. | 29 pp. | Sincronización con el Markdown canónico tras el cierre de benchmarks: Tabla 2 (§5.1) reconstruida a 12 modelos en 13 configuraciones desde los CSV re-puntuados · §5.2 con las mediciones limpias y la lectura de **interacción** idioma × *few-shot* (+11.12 pp) · §5.3.5 reescrita con el estudio completo de 13 modelos (F=36.3666, p=1.2236e-152), la limitación de *mojibake* del corpus y las dos salvedades de procedencia · terminología «Análisis de Variantes de Prompts» · citas IEEE numeradas y referencia [12] repuesta · Anexo E reconvertido en tabla de procedencia · fila de versión y fecha en la ficha. |

## Versiones previstas

| Versión | Contenido previsto | Bloqueada por |
|:---|:---|:---|
| ~~`_v2`~~ | ✅ Publicada el 2026-09-07 (ver registro) | — |
| `_v3` | Resolución del F1 titular de N=30 (decisión del autor, `TODO-INFORME-FINAL.md §15.3`) y cierre de los hallazgos de auditoría de gravedad media y baja | Criterio del autor |
| `_v4` | Versión de entrega, tras la revisión final del autor | `_v3` |

## Respaldos previos al versionado

Anteriores al esquema `_vN`, se conservan como referencia histórica y no se renumeran:

- `doc/organized/Hito_5_Tarea4_Informe_Final/Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx.bak_pre-cumplimiento-25pp`
