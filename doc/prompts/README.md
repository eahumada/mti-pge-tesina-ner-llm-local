# Biblioteca de prompts del proyecto

Prompts de uso recurrente, con los que se ejecutaron las revisiones de septiembre de 2026. Están redactados
para poder **pegarse tal cual** en una sesión nueva de Claude Code, y agrupados por temática.

| Fichero | Para qué sirve | Cuándo usarlo |
|:---|:---|:---|
| [`00-revision-completa.md`](./00-revision-completa.md) | **Replica la revisión íntegra** de referencias, citas, cifras y consistencia con orquestación multiagente | Antes de congelar una versión de entrega |
| [`01-bibliografia.md`](./01-bibliografia.md) | Verifica que cada obra exista, que los metadatos sean correctos y que toda entrada lleve URL abierta | Al añadir referencias o heredar una bibliografía |
| [`02-revision-global.md`](./02-revision-global.md) | Segunda pasada independiente: seis auditores con lentes distintas y un orquestador que cruza sus informes | Cuando el documento parece terminado |
| [`03-integridad-metrica.md`](./03-integridad-metrica.md) | Contrasta contra el código toda afirmación sobre métricas, umbrales y algoritmos | Antes de publicar cualquier cifra |
| [`04-caracterizacion-corpus.md`](./04-caracterizacion-corpus.md) | Mide qué contiene realmente un corpus: idioma del texto **y de las entidades** | Al incorporar o describir un corpus |
| [`05-entregables.md`](./05-entregables.md) | Propaga el Markdown a los `.docx` y al PDF y verifica el resultado sobre el documento generado | Tras cada tanda de correcciones |
| [`06-equipo-remoto.md`](./06-equipo-remoto.md) | Monitorea entregas de un equipo remoto y las verifica antes de aceptar sus cifras | Mientras haya ejecuciones delegadas |
| [`07-defensa-simulada.md`](./07-defensa-simulada.md) | **Solo lectura.** Revisión como profesor guía y comisión evaluadora, con cuatro preguntas de defensa | Al cerrar un capítulo, antes de darlo por bueno |

## Herramientas que estos prompts dan por supuestas (2026-09-09)

Varios de estos prompts describen en prosa comprobaciones que **hoy están implementadas**. Conviene
ejecutarlas antes de pedirle a nadie que las haga a mano:

| Herramienta | Qué comprueba |
|:---|:---|
| `tools/verificar_informe.py` | el informe contra los datos, el código y los tres `.docx`; devuelve 0 si no hay fallos **nuevos** |
| `tools/auditar_afirmaciones.py` | que el registro no afirme correcciones que no se aplicaron |
| `tools/cobertura_cifras.py` | qué cifra del informe **no tiene quien la recalcule** |
| `tools/estado_ramas.py` | que `main` esté al día y las ramas declaradas |
| `tools/ensayo_adopcion.py` | qué costaría adoptar otro consolidado, sin adoptarlo |
| `tools/preparar_clon.sh` | pone un clon recién hecho en estado de trabajo |
| `.githooks/pre-commit` | puerta que detiene el commit ante fallos **nuevos** |

**Ningún recuento de comprobaciones se anota en estos documentos**, por la razón que explica
`FINDINGS §F134`: una cifra copiada envejece con cada commit al código que describe y nadie se entera. Lo
dice el script al ejecutarse.

## Cómo se usan

Los prompts de `00` y `02` **lanzan workflows** y consumen bastante presupuesto; conviene ejecutarlos cuando
haya algo sustancial que revisar y no de forma rutinaria. Los demás son prompts de sesión normal.

El `07` es de **solo lectura por diseño**: devuelve un informe y no toca ningún fichero. Se usa **por
capítulos**, no con la tesina entera, porque un texto largo diluye la crítica que se le pide.

Tres reglas valen para todos, y están en `CLAUDE.md`:

1. **Un hallazgo de auditoría es una hipótesis, no un hecho.** Verificarlo contra la fuente primaria antes de
   convertirlo en instrucción de corrección. En septiembre de 2026 una auditoría automatizada reportó como
   «duplicado» una fila que eran dos configuraciones legítimas del mismo modelo, y de haberse aplicado sin
   revisar se habría borrado un resultado del informe.
2. **Ningún prompt dirige a eliminar contenido.** La política del proyecto es aditiva: si un conteo no cuadra,
   se corrige el conteo y no los datos. La única excepción autorizada hasta hoy fueron cuatro citas
   inexistentes, porque una cita fabricada no puede conservarse ni como histórico.
3. **Agentes en paralelo, archivos disjuntos.** Y respaldo previo a toda modificación.

## Por qué existe esta biblioteca

La revisión de septiembre de 2026 encontró, entre otras cosas, cuatro referencias que no correspondían a
ninguna obra existente, tres filas de una tabla comparativa con cifras que nadie había publicado, una
categoría de entidad que generaba el 65 % de los falsos positivos del estudio sin estar anotada en ningún
corpus, dos corpus declarados en español que estaban en inglés, y un anexo cuya tabla no se reproducía con
ningún criterio. Ninguno de esos defectos se detecta leyendo el documento: todos requieren contrastarlo
contra el código, los datos y la web. Estos prompts son el procedimiento que los encontró.
