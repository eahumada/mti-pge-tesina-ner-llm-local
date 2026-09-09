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

**Coordinación, y ya está resuelta.** Un workflow de Claude Code evaluó estas inserciones por
cirugía OOXML y dictaminó **«proceder con las viables»**, que son solo dos. **Haz `git pull` antes de
empezar** y trabaja contra la salida del verificador, que reflejará lo ya aplicado.

**El reparto, verificado:**

| Pieza | Quién |
|:---|:---|
| **5** — la celda de la Tabla 3 | **el workflow**: cadena única, un solo `<w:t>`, run sin resalte |
| **3, en parte** — las dos citas de [38] en el texto (§2.1 y §7.2) | **el workflow**: anclas únicas en los tres |
| **1** — la subsección completa | **tú**: ninguna herramienta inserta párrafos, encabezados ni tablas |
| **2** — los cinco párrafos | **tú**: exigen `<w:p>` nuevos, y uno exige **partir en dos** un párrafo que el `.docx` tiene fundido |
| **3, el resto** — la entrada [38] de la bibliografía | **tú**: `<w:p>` nuevo con `pStyle` `referenceitem` en A y `BodyText` en B y C, `numId=0` y un run en cursiva |
| **4** — la Tabla 9 | **tú, y no es lo que parecía**: ver abajo |
| **6** — las dos figuras | **tú**: `word/media/`, relaciones, `w:drawing`, y en B y C hace falta declarar `Default Extension="png"` en `[Content_Types].xml` |

> **Dos hechos del análisis que te ahorran una decisión equivocada.**
>
> **El `.docx` con plantilla no usa `heading4`.** De modo que el encabezado de la pieza 1 no es un
> problema de herramienta: **el nivel y su numeración son una decisión editorial** que hay que tomar,
> porque la jerarquía de la plantilla no tiene ese nivel en uso. Decide con qué estilo va y dilo.
>
> **La Tabla 9 no le faltan tres filas: usa otra convención.** Verificado celda por celda: el
> `.docx` escribe la hoja **indentada con espacios duros** —`&nbsp;&nbsp;&nbsp;&nbsp;main.py`— y el
> Markdown escribe la **ruta completa** —`src/main.py`—. Son 41 filas de datos frente a 44, pero el
> mapeo **no es uno a uno**: pegar tres filas con ruta completa **rompería la convención del
> entregable**, que es un árbol indentado y se lee mejor así. Lo que hay que hacer es averiguar qué
> tres rutas del Markdown no tienen su hoja en el árbol del `.docx` y añadirlas **en la convención
> del `.docx`**. Y si decides que la convención del entregable es la buena —lo es, para un lector—,
> di que la divergencia es **deliberada** y quedará declarada como tal en lugar de como defecto.

---

## 1. Qué le falta al entregable, y hay **una sola causa**

> El número exacto de fallos **no se anota aquí**, porque cambia cada vez que se corrige el
> Markdown y un recuento copiado se queda desfasado sin que nada avise (es el defecto de
> `FINDINGS §F134`). Lo dice el verificador al ejecutarse: `python3 tools/verificar_informe.py`.

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

### Pieza 4 — La Tabla 9, y no es lo que el recuento sugiere

El `.docx` tiene **41 filas de datos** y el Markdown **44**. Pero la diferencia **no son tres filas
que falten**: las dos tablas usan **convenciones distintas**, verificado celda por celda. El `.docx`
presenta un **árbol indentado con espacios duros** (`&nbsp;&nbsp;&nbsp;&nbsp;main.py`) y el Markdown
**rutas completas** (`src/main.py`).

Ver el aviso del apartado 0: hay que averiguar qué tres rutas no tienen hoja en el árbol y añadirlas
**en la convención del `.docx`**, o declarar la divergencia como deliberada. Lo que **no** hay que
hacer es pegar tres filas con ruta completa.

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
> **defectuoso**. **Las dos cosas van juntas o no van.** La comprobación «las figuras del Markdown estan en los tres .docx» vigila exactamente eso.

### Pieza 7 — La atribución del proveedor de los datos, y es la más grave de la lista

**Es la única pieza que no es una ausencia sino una afirmación falsa.** El entregable atribuye los
datos de sanciones a un proveedor que no los aportó, y respalda la atribución con una referencia a
ese proveedor. Para un tribunal con dominio en prevención de lavado de activos, que es el dominio de
este trabajo, confundir la autoridad sancionadora con un agregador de listas no es un detalle de
forma.

El artefacto primario es inequívoco: `data/dictionaries/PROCEDENCIA.md` declara que los
diccionarios se construyen desde `treasury.gov/ofac/downloads/sdn.csv`, la lista de Nacionales
Especialmente Designados de la Oficina de Control de Activos Extranjeros del Tesoro de los Estados
Unidos, y **no menciona OpenSanctions en ninguna parte**. El Markdown ya está corregido; el `.docx`
conserva la atribución vieja. **Son tres cambios y van juntos:**

| Dónde | El `.docx` dice hoy | Tiene que decir |
|:---|:---|:---|
| Atribución del corpus (Anexo F) | «seleccionadas de la base de datos OpenSanctions [19]» | «seleccionadas de la lista SDN del Departamento del Tesoro de los Estados Unidos [19]» |
| Anexo G.2 | «pares {entidad_PER, entidad_ORG} objetivo tomados de OpenSanctions» | «tomados de la lista SDN del Departamento del Tesoro de los Estados Unidos [19]» |
| Entrada [19] de la bibliografía | «OpenSanctions: Open Data on Sanctions Lists and Politically Exposed Persons» | «U.S. Department of the Treasury, Office of Foreign Assets Control, *Specially Designated Nationals and Blocked Persons List (SDN)*, instantánea del 27 de julio de 2026», con `treasury.gov/ofac/downloads/sdn.csv` |

> **Y aquí es fácil corregir de más, así que atención.** Quedan en el Markdown **dos** menciones de
> OpenSanctions que son **correctas y no se tocan**: la propuesta de trabajo futuro de §7.2 —«ampliar
> el corpus incorporando fuentes como la UAF, CMF y bases de datos de OpenSanctions [38]»—, que es
> una propuesta y no una atribución; y la **entrada [38]**, que es `FollowTheMoney`, una ontología
> que ese proveedor sí publica y que el trabajo sí usa. Un reemplazo global de la cadena
> «OpenSanctions» borraría una referencia correcta. Copia el texto del Markdown, no busques y
> reemplaces.

### Pieza 8 — El punto 11 de §7.2 y la referencia [39]

Añadidos al Markdown el 2026-09-09 a petición del autor: el punto 11 de la lista de trabajo futuro
declara el **contraste pareado por modelo** y las **variantes de la métrica** como línea pendiente, y
cita **[39]**, que es Dror et al., ACL 2018, la referencia estándar de contrastes de significación en
el área. Su URL está verificada y sus datos vienen del BibTeX canónico.

Igual que la pieza 3: las entradas van **contiguas hasta [38]** y [39] se añade al final, de modo que
**no hay corrimiento de numeración**. El punto 11 y la entrada [39] **van juntos**, porque una cita
sin entrada es un fallo del verificador, y una entrada sin cita también.

Es un punto **largo**, de unas dieciséis líneas, y por tanto es el primer candidato a chocar con el
límite de 25 páginas. Si no cabe, aplica el orden del apartado 2.ter: primero espaciados y cuerpo de
letra, y solo con autorización expresa del autor se toca el texto. **Lo que no se puede hacer es
insertar la entrada [39] sin el punto que la cita, ni el punto sin la entrada.**

---

---

## 2. La restricción dura, y qué hacer si no cabe

**El cuerpo no puede exceder 25 páginas**, sin contar anexos.

> **Corrección del 2026-09-09, y afloja la restricción.** Aquí decía «el verificador lo estima hoy
> en 23,0», y eso **no es el entregable**: la comprobación del límite estima sobre el **Markdown**,
> anclada a 14 842 palabras igual a 20 páginas contadas en el PDF entregado. El `.docx` es **más
> corto que el Markdown precisamente porque le falta este contenido**. Verificado: el cuerpo del
> Markdown son 16 753 palabras, que dan **≈22,8 páginas** con esa densidad; el `.docx` de hoy está
> por debajo.
>
> **Insertar lo que falta lleva el entregable hacia esas ≈23 páginas, no por encima de 25.** La
> puerta de factibilidad del workflow lo estimó en **≈21,2 páginas** con las seis piezas, con la
> precisión de que **de las 1 547 palabras solo unas 485 caen en el cuerpo** y el resto en los
> anexos, que el límite excluye. Esa segunda cifra no la he verificado por mi cuenta; la primera sí.
>
> **Conclusión operativa: cabe, y con margen.** Sigue contando sobre el PDF y sigue aplicando el
> orden de abajo si aprieta, pero no des por hecho que hay que sacrificar piezas: probablemente no.

**Cuenta las páginas sobre el PDF y no sobre el Word**: su paginación no siempre coincide, y el
metadato de páginas del `.docx` no sirve.

Si no cabe, la regla de `CLAUDE.md` es explícita y no admite atajo:

> Los espacios en blanco se recortan **por estilo, nunca por contenido**. Ante un desbordamiento se
> ajustan los espaciados de `Heading`, `abstract` y `table caption`, el interlineado y el cuerpo de
> letra de los bloques de código —hasta 7 pt si hace falta—, y solo entonces se considera tocar el
> texto. **Suprimir párrafos para ganar espacio requiere autorización expresa del autor.**

Esa autorización **no se ha dado**. Si tras agotar los ajustes de estilo sigue sin caber, **para y
dilo**, con el número de páginas y qué ajustes ya probaste. Y si hay que priorizar —que según la
estimación de arriba probablemente **no haga falta**—, el orden es:
**pieza 1 primero** —la subsección de corridas múltiples, que es la que un tribunal juzga—, después
las figuras con su prosa, después la referencia [38] con la celda de la Tabla 3, y al final los cinco
párrafos de límites y las filas de la Tabla 9, que tienen eco en otras partes del documento.

---

## 2.bis Las cuatro recomendaciones del profesor guía, que siguen abiertas

**Esto es lo que el director del trabajo devolvió, y es lo que va a volver a mirar.** No lo
confundas con las críticas nuevas de esta revisión: son anteriores y siguen sin atender del todo.
Están registradas en `TODO-INFORME-FINAL.md`.

| # | Reparo del profesor guía | Qué toca hacer, y es tuyo |
|:--|:---|:---|
| 1 | **Bloques en blanco y saltos de página** | Es de maquetación pura y es enteramente tuyo. Al insertar contenido y regenerar el PDF, revisa que no queden páginas semivacías, encabezados solapados ni saltos que dejen una tabla separada de su leyenda. La leyenda va **con** su tabla en la misma página. |
| 2 | **Ficha del estudiante en la primera hoja** | Comprueba que está y que la plantilla la coloca donde `plantilla_final-2026.docx` manda. Si falta, se añade: es requisito institucional, no estilo. |
| 3 | **Poco desarrollo: secciones de un solo párrafo** | **Y aquí hay una coincidencia que conviene aprovechar.** Este reparo y la decisión 19 apuntan al mismo sitio: las piezas 1 y 2 de este encargo son **diez párrafos y una tabla** que el Markdown ya tiene y el entregable no. Insertarlas **atiende el reparo 3 con texto ya escrito y revisado**, sin redactar nada nuevo. Es el argumento más fuerte para que quepan. |
| 4 | **Marco conceptual pobre, sin comparar metodologías** | Este **no es tuyo**: exige escribir marco teórico nuevo y es del autor. Anótalo como pendiente y no improvises. |

**Los reparos 1, 2 y 3 los cierra este encargo. El 4 no, y hay que decirlo al entregar** en lugar de
dar por atendidas las cuatro.

---

## 2.ter Las 25 páginas: el límite manda sobre todo lo demás

Lo dice ya el apartado 2, pero conviene repetirlo porque es el punto donde se toman malas
decisiones bajo presión:

> **El cuerpo no puede exceder 25 páginas, sin contar anexos. Es una restricción institucional, no
> una preferencia.** Un informe de 26 páginas se devuelve, y entonces no importa lo bien que esté
> el resto.

**El orden de actuación cuando aprieta, y no admite atajos:**

1. **Primero, estilo.** Espaciados de `Heading`, `abstract` y `table caption`; interlineado; cuerpo
   de letra de los bloques de código, hasta **7 pt** si hace falta. Esto está expresamente
   autorizado por `CLAUDE.md`.
2. **Después, los anexos.** Admiten 25 páginas más y **no cuentan** para el límite. Si una tabla
   larga del cuerpo puede vivir en un anexo con su llamada desde el cuerpo, eso libera espacio sin
   perder nada. Comprueba que la referencia cruzada queda correcta: la comprobación «referencias a Anexo X y a Tabla N con destino existente» del
   verificador la vigila.
3. **Solo entonces, y con autorización expresa del autor que HOY NO ESTÁ DADA**, se considera tocar
   texto. **Suprimir párrafos para ganar espacio sin esa autorización no es una opción.**
4. **Si tras 1 y 2 sigue sin caber, PARA Y DILO**, con el recuento de páginas y qué ajustes probaste.
   Y aplica el orden de prioridad del apartado 2: la subsección de corridas múltiples primero.

**Cuenta sobre el PDF y no sobre el Word.** Su paginación no siempre coincide y el metadato de
páginas del `.docx` no sirve. Cuenta el cuerpo, sin anexos, y di la cifra en tu informe.

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
  peor que tres incompletos, y las cuatro comprobaciones de sincronía —prosa, tablas y bibliografía, encabezados y figuras— los comparan uno por uno.
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
5. Los tres `.docx` siguen siendo OOXML estructuralmente sano, que lo comprueba «los tres .docx siguen siendo OOXML estructuralmente sano».

**Si algo va mal, restaura desde el respaldo y dilo.** Un entregable corrupto es peor que un
entregable incompleto, y las 55 comprobaciones no sirven de nada si el fichero no abre.

---

## 5.bis Si el autor decide publicar el eta cuadrado

Es una mejora barata que las guías de reporte piden y el informe no trae: el **tamaño de efecto**
junto al valor p. Está **ya calculado**: η² = **0,2360** en el consolidado publicado. Si el autor
decide incluirlo, es **una frase** en §5, junto a la del ANOVA, y no altera el recuento de páginas.

No lo añadas por tu cuenta: es contenido y lo decide él. Queda anotado aquí para que, si te lo pide,
no haya que buscar la cifra.

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
