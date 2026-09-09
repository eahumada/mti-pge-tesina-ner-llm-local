# Encargo a Claude Desktop — cerrar los `.docx` y regenerar el PDF final

**2026-09-09. Sustituye a `PROMPT-CLAUDE-DESKTOP-RESINCRONIZACION-20260908.md`**, que se conserva
como registro y no se borra. Lo que cambia respecto de aquel es lo más importante de este encargo:
**ya no hay que reconstruir a mano la lista de lo que falta**.

---

## 0. Lo primero, y ahorra la mitad del trabajo

Aquel encargo pedía enumerar qué había cambiado desde la última propagación. **Eso ahora lo produce
una herramienta.** Desde la raíz del repositorio:

```sh
git pull
python3 tools/verificar_informe.py
```

Las comprobaciones **51 a 54** comparan los tres `.docx` contra el Markdown canónico en los cuatro
tipos de contenido, y **lo que falta sale en su salida, fichero por fichero**:

| Comprobación | Qué compara | Fallos hoy |
|:---|:---|---:|
| 51 | la **prosa**, párrafo a párrafo | 30 |
| 52 | las **tablas** celda a celda y la **bibliografía** | 12 |
| 53 | los **encabezados** | 3 |
| 54 | las **figuras** y las citas colgantes | 6 |

**Trabaja contra esa salida, no contra la lista de abajo.** La lista es para que entiendas el
alcance; la salida es la verdad, y se actualiza sola a medida que insertas.

**Coordinación, importante:** un workflow de Claude Code (`wifolz9jz`) está evaluando ahora mismo si
estas inserciones son viables por cirugía OOXML, con una puerta que se detiene si no lo son. **Mira
`CURRENT-TASKS.md` antes de empezar.** Lo más probable es que se detenga —ninguna herramienta de
`tools/` inserta párrafos ni imágenes, solo reemplaza y reescribe— y entonces el trabajo es tuyo,
que tienes Word. Si el workflow hubiera aplicado algo, la salida del verificador lo reflejará.

---

## 1. Qué le falta al entregable: son 51 fallos y **una sola causa**

Los tres `.docx` reflejan un estado anterior del Markdown. No son defectos dispersos:

### Pieza 1 — Una subsección entera de §5, y es la que más pesa

Falta completa: **encabezado, cinco párrafos y su tabla**.

- Encabezado de cuarto nivel: «Corridas múltiples del mismo modelo, y cuál se toma como referencia»
- Sus cinco párrafos, que empiezan por: «Cuatro de los trece modelos se midieron más de una vez…»,
  «Conviene separar dos situaciones que no son la misma…», «Los motivos de invalidez son dos…»,
  «El presupuesto de salida agotado produce el mismo efecto por otra vía…», «La última fila acredita
  que el criterio fue la validez de la medición y no su resultado…»
- **Tabla 20**, nueve filas: «Grupos con más de una corrida sobre N=120, con el motivo de la
  sustitución y la evidencia»

**Por qué es la prioridad.** Es la **declaración de corridas múltiples** que la regla de integridad
de `CLAUDE.md` exige con estas palabras: «citar la más favorable sin mencionar las demás es
indistinguible de seleccionar el resultado, aunque no haya intención de hacerlo, **y es lo que un
tribunal juzga**». El Markdown cumple la regla; **el entregable no la contiene**. Y el último de los
cinco párrafos es el que desarma la objeción, porque muestra un caso en que el criterio de validez
eligió la corrida **menos** favorable.

Va justo después de la tabla a cuya columna «Corrida» se refiere, que es donde el Markdown la tiene.

### Pieza 2 — Cinco párrafos de declaración de límites

Empiezan por: «Dos rasgos del problema explican por qué no basta con una solución puntual…», «La
carencia de datos etiquetados no es una suposición de partida…», «A la carencia de datos se suma una
dificultad de medición…», «Tres advertencias de lectura antes de las cifras…», «El efecto se midió
sobre las veintiséis configuraciones del estudio…».

### Pieza 3 — La referencia [38] y sus cuatro citas

El `.docx` tiene las entradas **[1] a [37] contiguas** y le falta solo la última. **No hay
corrimiento de numeración**: se añade [38] al final de la bibliografía y sus cuatro citas donde el
Markdown las tiene. La obra es el esquema **FollowTheMoney**.

### Pieza 4 — Tres filas de la Tabla 9

Estructura del repositorio: el `.docx` tiene **42** filas y el Markdown **45**.

### Pieza 5 — Una celda de la Tabla 3

El `.docx` dice «validación de esquema» donde el Markdown dice «validación contra el esquema
FollowTheMoney [38]». Va con la pieza 3.

### Pieza 6 — Las dos figuras

**Cero elementos `<w:drawing>`** en el cuerpo de los tres `.docx`. Los PNG están en
`doc/figuras/falsos-positivos.png` y `doc/figuras/efecto-kb-rag.png`, y están **verificados como
reproducibles byte a byte** con `tools/generar_figuras_informe.py` desde la Tabla 7 — no hay que
rehacerlos, hay que insertarlos, con su leyenda **debajo** y a 300 puntos por pulgada.

> **Regla de coherencia, y es la que más importa de esta pieza.** Hoy el `.docx` **no cita** las
> figuras: cero apariciones de «Figura N». De modo que es **incompleto pero coherente**, y no
> promete nada que no muestre. Si insertas la prosa que las menciona —el párrafo del 66,0 % dice
> «según recoge la Figura 1»— **sin** insertar las imágenes, el entregable pasa de incompleto a
> **defectuoso**. **Las dos cosas van juntas o no van.** La comprobación 54 vigila exactamente eso.

---

## 2. La restricción dura, y qué hacer si no cabe

**El cuerpo no puede exceder 25 páginas**, sin contar anexos. El verificador lo estima hoy en
**23,0**, y las piezas 1 y 2 suman del orden de **1 500 palabras**.

**Cuenta las páginas sobre el PDF y no sobre el Word**: su paginación no siempre coincide, y el
metadato de páginas del `.docx` no sirve.

Si no cabe, la regla de `CLAUDE.md` es explícita y no admite atajo:

> Los espacios en blanco se recortan **por estilo, nunca por contenido**. Ante un desbordamiento se
> ajustan los espaciados de `Heading`, `abstract` y `table caption`, el interlineado y el cuerpo de
> letra de los bloques de código —hasta 7 pt si hace falta—, y solo entonces se considera tocar el
> texto. **Suprimir párrafos para ganar espacio requiere autorización expresa del autor.**

Esa autorización **no se ha dado**. Si tras agotar los ajustes de estilo sigue sin caber, **para y
dilo**, con el número de páginas y qué ajustes ya probaste. Y si hay que priorizar, el orden es:
**pieza 1 primero** —la subsección de corridas múltiples, que es la que un tribunal juzga—, después
las figuras con su prosa, después la referencia [38] con la celda de la Tabla 3, y al final los cinco
párrafos de límites y las filas de la Tabla 9, que tienen eco en otras partes del documento.

---

## 3. El PDF, que es lo que se entrega

**Está desfasado.** El `.docx` con plantilla se modificó hoy a las 11:26 y el PDF de la raíz es del
**8 de septiembre a las 04:31**: no contiene ninguna corrección de hoy, incluida la del Anexo H.3,
donde el texto contradecía a su propia tabla.

**Hay que regenerarlo desde el `.docx` con Word**, que es lo que tú puedes hacer y Claude Code no.

> **Y hay un PDF que NO se toca bajo ninguna circunstancia:**
> `doc/versions/enviados/2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf`.
> Atestigua qué se entregó al profesor guía y es la verdad de referencia sobre qué modelos forman el
> estudio. Reescribirlo no sería limpiar: sería falsificar el registro de lo que se entregó.

El PDF que hay que regenerar es el de la **raíz**:
`Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.pdf`.

---

## 4. Cómo hacerlo

- **Puedes usar Word**, y para insertar párrafos, una tabla y dos imágenes es la vía correcta: la
  cirugía OOXML de `tools/` sirve para **reemplazar** texto y reescribir celdas, no para insertar
  estructura.
- **No regeneres el `.docx` desde el Markdown con pandoc.** Contiene correcciones manuales de
  numeración multinivel (`numId=0`), estilos de fila y saltos de página que una regeneración
  destruiría. Esto sigue valiendo aunque trabajes con Word: abre el `.docx` existente y edítalo.
- **Respaldo de los cuatro artefactos antes de tocarlos**, y di dónde quedaron.
- **Los tres `.docx` tienen que quedar consistentes entre sí.** Tres entregables que no coinciden es
  peor que tres incompletos, y las comprobaciones 51 a 54 los comparan uno por uno.
- **Declara la tarea en `CURRENT-TASKS.md`** al empezar y actualízala al terminar. Es la única
  fuente de verdad sobre qué agente hace qué, y hay sesiones concurrentes.

### Reglas que el documento generado tiene que cumplir

- Resumen y abstract **fundidos en la primera página**, sincronizados, por debajo de 200 palabras
  cada uno.
- **Leyendas encima** de las tablas y **debajo** de las figuras, numeradas de forma contigua en
  orden de aparición.
- **Cero emojis, marcas de agua, sellos de borrador y arte ASCII.** Donde un símbolo hace de valor se
  escribe la palabra: «sí», «no», «parcial».
- **Guiones largos y negritas al mínimo** en el cuerpo. El renderizador no debe **añadir** énfasis
  respecto de la fuente. Aviso que ahorra discusiones: los recuentos absolutos **no son reproducibles
  entre métodos de conteo distintos** —tres auditores dieron 19/108, 28/127 y 31/150 sobre el mismo
  texto—. Lo que importa es que el generado no añada, no acertar una cifra.

---

## 5. Criterio de aceptación, y es mecánico

Al terminar, desde la raíz:

```sh
python3 tools/verificar_informe.py
python3 tools/auditar_afirmaciones.py
```

**Lo que tiene que pasar:**

1. El recuento de **fallos declarados baja de 61**. Cada pieza que insertes cierra 3 fallos, uno por
   `.docx`. Si insertas todo, deben cerrar **51** y quedar los 10 restantes, que no son tuyos: el
   PDF (3, que cierran cuando lo regeneres), los dos ficheros de registro vacíos, la telemetría de
   `real_mixed_70`, el `per_type` de `nemotron-mini` y las tres de la decisión 13.
2. Las comprobaciones **51 a 54 pasan a `ok`**. Si alguna sigue en `CONOC`, su salida dice
   exactamente qué falta.
3. **Cero fallos NUEVOS.** El verificador devuelve 0 si no hay nuevos; si aparece uno, es que la
   inserción rompió algo y **eso es más importante que lo que arregló**.
4. La auditoría de afirmaciones sigue en **15 predicados y 0 incumplidos**.
5. Los tres `.docx` siguen siendo OOXML estructuralmente sano, que lo comprueba la comprobación 44.

**Si algo va mal, restaura desde el respaldo y dilo.** Un entregable corrupto es peor que un
entregable incompleto, y las 55 comprobaciones no sirven de nada si el fichero no abre.

---

## 6. Lo que NO es tuyo, para que no lo toques

- **El Markdown canónico.** Es la fuente y está correcto. Toda diferencia se resuelve **a favor del
  Markdown**.
- **Las tres decisiones de la decisión 13** (`cita 62.67`, `cita 80.51`, «el Anexo I dice»): son del
  autor, sobre agregación macro frente a micro.
- **El `per_type` de `nemotron-mini:4b`**: depende de la decisión 1, adoptar o no el consolidado
  nuevo, cuyo precio está calculado en `FINDINGS §F131`.
- **Los dos ficheros de registro vacíos** y la telemetría de `real_mixed_70`: decisiones del autor.
- **El PDF de `doc/versions/enviados/`**, ya dicho.
