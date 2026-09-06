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

## Versiones previstas

| Versión | Contenido previsto | Bloqueada por |
|:---|:---|:---|
| `_v2` | Correcciones de consistencia documental (auditoría del 2026-09-03) que no dependen de datos nuevos | Nada — ejecutable de inmediato |
| `_v3` | Incorporación del benchmark N=120 consolidado (14 modelos) y de la re-ejecución del corpus N=30 | Corridas en curso |
| `_v4` | Versión de entrega, tras la revisión final del autor | `_v3` |

## Respaldos previos al versionado

Anteriores al esquema `_vN`, se conservan como referencia histórica y no se renumeran:

- `doc/organized/Hito_5_Tarea4_Informe_Final/Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx.bak_pre-cumplimiento-25pp`
