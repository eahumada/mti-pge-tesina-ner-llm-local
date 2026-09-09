# Revisión completa antes de congelar una entrega

Replica la revisión de referencias, citas, cifras y consistencia ejecutada en septiembre de 2026. Son cuatro
etapas y conviene **leer el resultado de cada una antes de lanzar la siguiente**, porque cada etapa cambia el
documento y la siguiente debe auditar el estado ya corregido, no una versión intermedia.

Coste orientativo: unos treinta agentes en total y alrededor de dos millones de tokens de subagente. No es un
procedimiento rutinario.

---

## Etapa 1 — Correspondencia entre citas y entradas

> Con un workflow, verificar la correspondencia bibliográfica del informe en ambos sentidos: que toda marca de
> cita del cuerpo tenga su entrada en el capítulo de referencias, y que toda entrada esté citada al menos una
> vez. Buscar además referencias, notas y URLs mencionadas en el texto sin estar anotadas como cita. Reportar
> sin editar: la corrección se decide después.

## Etapa 2 — Verificación contra internet, entrada por entrada

> Lanzar múltiples agentes para verificar todas las citas del proyecto contra internet. Para cada entrada:
> comprobar que **la obra exista**, que autores, año, publicación, volumen y páginas coincidan con lo que
> declara la entrada, y que la afirmación que sostiene en el texto sea coherente con el contenido real de la
> fuente. Devolver la URL canónica, con esta preferencia: DOI, ACL Anthology, actas oficiales (NeurIPS, PMLR,
> JMLR), arXiv y, en último lugar, la web del editor.
>
> Reglas absolutas: **prohibido inventar una URL**; una URL que no se haya abierto con WebFetch no cuenta como
> verificada, y responder «no la encuentro» es una respuesta correcta y útil. Sospechar de nombres de autor
> genéricos y de publicaciones sin volumen ni páginas, pero **verificar antes de concluir**. Reportar también
> los errores de metadatos —una inicial equivocada, unas páginas que no cuadran, una editorial errónea— sin
> corregirlos.
>
> Si algún servidor bloquea el lector automático (ACM devuelve 403), acreditar la entrada por resolución del
> DOI, que solo redirige si está registrado, y dejar constancia de que se usó esa vía.

## Etapa 3 — Saneamiento, si aparecen citas no localizables

> Para cada referencia que no corresponda a ninguna obra existente: buscar la obra real que **sostenga la
> misma afirmación**, no una que simplemente trate del mismo tema. Si la afirmación no tiene respaldo real,
> reformularla en lugar de eliminarla. Revisar en particular las **tablas comparativas**: una cita fabricada
> suele arrastrar cifras que nadie ha publicado.
>
> Prohibido eliminar filas de tablas o secciones para cuadrar un conteo. Respaldo previo obligatorio. Y una
> etapa final que compruebe que no se perdió contenido.

## Etapa 4 — Segunda pasada independiente

Usar [`02-revision-global.md`](./02-revision-global.md), **sin entregar a los auditores los hallazgos de las
etapas anteriores**. Es la etapa que más valor aportó en septiembre: encontró los tres bloqueantes que las
tres primeras no habían visto, porque estaban mirando la bibliografía y no la medición.

---

## Verificación final, sobre el documento y no sobre el informe de nadie

```
Comprobar sobre el Markdown canónico:
- ninguna llamada a §x.y, Tabla N o Anexo X apunta a algo inexistente
  (atención: los encabezados llegan al cuarto nivel, #### 5.3.5)
- tablas numeradas de forma contigua en orden de aparición, con leyenda
  inmediatamente encima y un texto que describa lo que la tabla contiene
- entradas bibliográficas contiguas desde [1], todas con URL, sin citas
  huérfanas y sin entradas que nadie cite
- resumen y abstract por debajo de 200 palabras y diciendo lo mismo
- cero emojis, cero arte ASCII
- ningún identificador §F<n> o §L<n> repetido
```

Si alguna cifra cambia, **recontarla contra el fichero de resultados**, no contra lo que se recuerde haber
medido. En esta revisión se colaron dos cifras mal transcritas y ambas se detectaron así.

---

## Comprobaciones mecánicas ejecutables (2026-09-08)

Las comprobaciones que este documento describe en prosa están implementadas en
**`tools/verificar_informe.py`**. Ejecutarlo antes de dar por buena cualquier revisión:

```sh
python3 tools/verificar_informe.py          # detalle
python3 tools/verificar_informe.py --breve  # solo lo que falla o está vacío
```

**Cuántas comprobaciones cubre y cuáles son no se anota aquí: lo dice el propio script al ejecutarse.**
Este párrafo enumeraba diez y se quedó corto en cuanto se añadieron más, sin que nada avisara. Un recuento
copiado a un documento de procedimiento envejece con cada commit al código que describe. La regla está en
`FINDINGS §F134`.

Lo que sí conviene saber es **qué familias cubre**: ficheros vacíos, referencias cruzadas, tablas y figuras
con su leyenda, bibliografía con sus URL, límites del resumen, higiene tipográfica, modelos excluidos,
reproducción de las tablas y figuras desde los datos, los estadísticos titulares recalculados desde el CSV
—ANOVA, Levene, Friedman, el recuento de Tukey—, la sincronía de los tres `.docx` con la fuente, y una
auditoría del propio mecanismo de fallos declarados.

**Además del verificador hay tres herramientas más, y conviene ejecutarlas en la misma tanda:**

```sh
python3 tools/auditar_afirmaciones.py   # que el registro no afirme correcciones sin aplicar
python3 tools/estado_ramas.py           # que main este al dia y las ramas declaradas
python3 tools/cobertura_cifras.py       # que cifra del informe no tiene quien la recalcule
```

Y hay una **puerta de commit** en `.githooks/pre-commit` que ejecuta el verificador y la auditoría cuando el
commit toca el informe, las herramientas o los datos. Es configuración local: un clon nuevo no la tiene, y
`tools/preparar_clon.sh` la instala junto con lo demás que un clon no trae.

**Cada comprobación declara cuántos elementos examinó**, y una que examina cero se marca como VACÍA en lugar
de superada. Es deliberado: el propio informe documenta en §5.3 una prueba de sensibilidad que no podía
marcar nada por construcción y se dio por buena durante meses. Al añadir una comprobación, verificar que su
recuento no sea cero.

Lo que el script **no** cubre y sigue exigiendo lectura: que la leyenda de una tabla describa esa tabla y no
otra heredada; que resumen y abstract digan lo mismo en los dos idiomas; que las URL de la bibliografía
respondan; y el recuento de páginas del PDF, que solo se obtiene generándolo.
