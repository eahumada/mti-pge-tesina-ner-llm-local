# Propagación al `.docx` y al PDF, y verificación del resultado

## Prompt de encargo

> Resincronizar los `.docx` y el PDF con el Markdown canónico, que es la fuente: toda diferencia se resuelve a
> favor del Markdown. Enumerar en el encargo **qué ha cambiado** desde la última propagación, porque quien
> maqueta no puede adivinarlo, y declarar el SHA-256 del Markdown para que se compruebe al terminar que no se
> movió mientras se propagaba.
>
> **No regenerar con pandoc.** Los `.docx` contienen correcciones manuales de numeración multinivel
> (`numId=0`), estilos de fila y saltos de página que una regeneración destruiría. Usar
> `tools/docx_replace_terms.py`, que edita el XML preservando el formato, o edición dirigida del XML. Si el
> volumen de cambio desborda esa vía, **decirlo antes de empezar** y que lo decida el autor.
>
> Respaldo de los cuatro artefactos antes de tocarlos, y declaración de la tarea en `CURRENT-TASKS.md`.

## Reglas que el documento generado tiene que cumplir

> - Cuerpo por debajo de **25 páginas** sin contar anexos; los anexos admiten 25 más y no cuentan.
> - **Resumen y abstract fundidos en la primera página**, sincronizados y por debajo de 200 palabras cada uno.
> - **Leyendas encima** de las tablas, numeradas de forma contigua en orden de aparición.
> - **Cero emojis, marcas de agua, sellos de borrador y arte ASCII.** Donde un símbolo hacía de valor se
>   escribe la palabra: «sí», «no», «parcial».
> - **Guiones largos y negritas al mínimo** en el cuerpo. Contarlos en el documento generado y compararlos con
>   los de la fuente: el renderizador no debe añadir énfasis al restituir estilos ni al aplicar la plantilla.
> - Los espacios en blanco se recortan **por estilo, nunca por contenido**. Suprimir párrafos para ganar
>   espacio requiere autorización expresa del autor.

## Verificación, sobre el PDF y no sobre el Word

> Contar páginas sobre el **PDF**, porque su paginación y la del `.docx` no siempre coinciden. Comprobar en el
> documento generado: número de entradas bibliográficas y ausencia de las retiradas; que las tablas
> reescritas sean las nuevas; que **todos los anexos estén**, contándolos y no dándolos por supuestos; que el
> resumen y el abstract quepan en la primera página; y que no haya páginas en blanco ni encabezados
> solapados.

Un aviso que ahorra discusiones: los **recuentos absolutos de guiones y negritas no son reproducibles entre
métodos de conteo distintos**. Tres auditores dieron 19/108, 28/127 y 31/150 sobre el mismo texto, según
incluyeran o no tablas, citas y encabezados. Lo que importa es que el generado no añada énfasis respecto de la
fuente, no acertar con una cifra concreta.

## Actualización del 2026-09-09: el inventario ya no hay que enumerarlo a mano

Arriba se pide «enumerar en el encargo **qué ha cambiado** desde la última propagación, porque quien maqueta
no puede adivinarlo». **Eso ya lo produce una herramienta**, y conviene usarla en lugar de escribir la lista:
una enumeración a mano se queda incompleta y nadie se entera.

Las comprobaciones **51 a 54** de `tools/verificar_informe.py` comparan los tres `.docx` contra el Markdown
canónico en los cuatro tipos de contenido, y **el que falta en el entregable sale en su salida**:

| Comprobación | Qué compara |
|:---|:---|
| 51 | la **prosa**, párrafo a párrafo, con sondeo por frases distintivas para no confundir un párrafo reescrito con uno ausente |
| 52 | las **tablas**, celda a celda, y la **bibliografía** entrada por entrada |
| 53 | los **encabezados**, normalizando la numeración multinivel de Word, la caja y los `#` de los bloques de código |
| 54 | las **figuras**, y que ninguna cita a «Figura N» quede colgando sin imagen |

De modo que el encargo de maquetación se escribe **pegando la salida del verificador**, no reconstruyendo la
lista. Lo que hoy falta en los entregables está declarado a nombre de la decisión 19 del autor.

**Dos avisos sobre estas comprobaciones**, los dos aprendidos a golpes:

- **Las entidades XML se decodifican antes de comparar.** El `.docx` guarda `p&lt;0.001` donde el Markdown
  escribe `p<0.001`: sin decodificar, la Tabla 7 —la central del estudio— sale divergente siendo idéntica.
- **Una divergencia detectada hay que confirmarla antes de contarla.** Tres veces en una sola sesión el
  defecto estaba en la comparación y no en el documento. Y un ensayo se juzga por el código de salida, no
  por si un `grep` encuentra una cadena en la salida.

## El fallo que más caro sale

En septiembre de 2026 los tres `.docx` y el PDF que se iban a entregar **no eran el documento corregido**:
conservaban veinte referencias frente a las treinta y siete del Markdown, incluidas cuatro no localizables, y
una tabla comparativa con cifras que nadie había publicado. Dos auditores lo detectaron extrayendo el XML por
separado. **Verificar el entregable, no la fuente**, es la única forma de encontrarlo.

**Y desde el 2026-09-09 ya no depende de que dos auditores se pongan a extraer XML**: las comprobaciones 51
a 54 lo hacen en menos de dos segundos y cortan el commit ante cualquier divergencia nueva. Que ese fallo
costara una revisión entera es exactamente el argumento para que sea una comprobación y no una tarea.
