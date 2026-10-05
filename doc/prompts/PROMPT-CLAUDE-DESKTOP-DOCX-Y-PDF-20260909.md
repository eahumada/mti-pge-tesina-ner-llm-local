# Encargo a Claude Desktop — cerrar los `.docx` y regenerar el PDF final

**2026-09-09. Sustituye a `PROMPT-CLAUDE-DESKTOP-RESINCRONIZACION-20260908.md`**, que se conserva
como registro y no se borra. Lo que cambia respecto de aquel es lo más importante de este encargo:
**ya no hay que reconstruir a mano la lista de lo que falta**.

**Consolidado el 2026-09-09, tras cerrar el análisis del día.** Diez piezas en total (se añadieron la
7, 8, 9 y 10 sobre la marcha; reordenadas aquí en el orden en que conviene aplicarlas). El criterio de
aceptación de §5 se reescribió para no citar cifras absolutas: se comparan antes/después de tu
trabajo, porque un número fijo escrito en este documento se desfasa en cuanto alguien corrija el
Markdown — ya le pasó dos veces a documentos parecidos (`FINDINGS §F134`, `§F149`).

**Ampliado el mismo día, más tarde: el autor adoptó un consolidado nuevo (decisión 1).**
Ocho piezas más, la 11 a la 18, en la nueva sección **0.bis**, y son las que más texto tocan —
toda la Tabla 7, el párrafo estadístico entero de §5.3.1, el resumen y el abstract. Van
**primero** en la prioridad si el espacio aprieta: son la comprobación más visible para un
tribunal, porque tocan la cifra titular del trabajo. Detalle en `FINDINGS §F154`/`§F155`.

**Ampliado una tercera vez, más tarde ese mismo día: seis pasajes más y una etiqueta que
faltaba.** Piezas 19 a 24 en la nueva sección **0.ter**: un «Corpus 3 —» que faltaba en §4.1, dos
frases de §3.3 y la leyenda de la Figura 1 que seguían describiendo el defecto de Locations como
vigente, los puntos 7 y 8 de §7.2 que proponían como pendiente algo ya hecho, y una tercera
reescritura del resumen/abstract porque «en el dominio» no se entendía sin contexto. Detalle en
`FINDINGS §F158`/`§F159`. **Si estás en medio de aplicar la 0.bis, aplica también la 0.ter antes de
dar el entregable por cerrado**: no son piezas alternativas, son dos rondas del mismo día.

**Ampliado una cuarta vez, más tarde ese mismo día: un párrafo nuevo en §4.1.2.** Pieza 25 en la
nueva sección **0.quater**: el autor pidió que el informe explique qué significa la categoría
`Locations` y por qué importa, y no solo en §3.3 (donde ya se documenta el defecto) sino también
donde se describe el corpus. Es un párrafo nuevo, no una edición de uno existente; no toca ninguna
cifra de las rondas anteriores.

**Ampliado una quinta vez, más tarde ese mismo día: se retiró la Tabla 20 y se corrigieron tres
cifras equivocadas en el párrafo estadístico de §5.3.1.** Piezas 26 a 28 en la nueva sección
**0.quinquies**: el autor pidió, primero, dejar una sola cifra vigente por benchmark y N en todo
el documento (retirar del Anexo I las cifras históricas que duplicaban la Tabla 7), y después,
por separado, simplificar el párrafo del ANOVA/Tukey/Levene/Friedman/correlación de §5.3.1 — al
verificar sus cifras antes de simplificar aparecieron **tres errores reales**, no solo prosa
densa. **Estas piezas SÍ importan de verdad si ya renderizaste antes de hoy**: el verificador
(`tools/verificar_informe.py`) confirma que los tres `.docx` actuales todavía tienen el texto
viejo y las cifras equivocadas — están declaradas en `FALLOS_DECLARADOS` como pendientes tuyas,
no como aceptadas. Detalle en `FINDINGS §F160`/`§F161`, `LEARNING §L78`/`§L79`.

**La pieza 9 de más abajo queda superada por la 27: no la apliques tal como está escrita.**
Describía un párrafo de `gpt-oss:20b` que ya no existe en esa forma; la 27 trae el texto correcto.

**Ampliado una sexta vez, más tarde ese mismo día: sin fechas de calendario en el cuerpo, y una
anécdota retirada por completo.** Piezas 29 y 30 en la nueva sección **0.sexies**: el autor pidió
que el cuerpo (capítulos 1-7, no los Anexos) no mencione fechas de calendario del proceso interno
—ocho frases con «el 8 de septiembre de 2026» y similares, reescritas sin la fecha—, y que se
retire por completo, no se recorte, la nota de §5.3 sobre un F1 de 79,03 % cuyos datos ya no
existen para recalcularlo. Ninguna cifra de resultado cambia. Detalle en `FINDINGS §F162`/`§F163`.

**Ampliado una séptima vez, más tarde ese mismo día: el capítulo 2 (marco teórico) creció y se
renumeró, atendiendo al reparo 4 del profesor guía.** Piezas 31 a 33 en la nueva sección
**0.septies**: una sección `2.4` completamente nueva sobre arquitectura (pub/sub, AIMD,
Factory/Facade), la vieja `2.4` y `2.5` renumeradas a `2.5` y `2.6`, dos párrafos nuevos dentro de
la `2.5` (homocedasticidad/Friedman, Pearson/Spearman) y uno en `2.1` (criterios de coincidencia de
cadenas), con dos recortes correspondientes en §3.3 y §5.3.1 para no duplicar la misma teoría dos
veces. **Aviso de presupuesto**: el margen de páginas quedó en ~121 palabras: si el cuerpo se acerca
al límite al maquetar, consulta al autor antes de recortar nada por tu cuenta. Detalle en
`FINDINGS §F164`.

**Confirmado como límite real (no del autor, de la guía institucional)**: 25 páginas **sin anexos**
más hasta 25 páginas **adicionales** de anexos, no un total de 25. No hay que recortar los Anexos
por presupuesto — hoy miden ~8,7 páginas estimadas. Para hacer sitio al capítulo 2, el listado de
código `LLMProvider` se movió de `§3.2` al nuevo `Anexo A.1` (pieza 34), recuperando el margen a
~178 palabras.

**Ampliado una octava vez, ese mismo día, tras una segunda vuelta del autor: un párrafo más en
`2.3`.** Pieza 35 en la nueva sección **0.octies**: qué es un embedding y una base de datos
vectorial (ChromaDB), mecanismo común a las dos variantes de RAG que `2.3` ya comparaba. El margen
de páginas queda en ~74 palabras — el más ajustado de todo el encargo. Detalle en `FINDINGS §F165`.

---

## 0. Lo primero, y ahorra la mitad del trabajo

Aquel encargo pedía enumerar qué había cambiado desde la última propagación. **Eso ahora lo produce
una herramienta.** Desde la raíz del repositorio:

```sh
git pull
python3 tools/verificar_informe.py
```

Cuatro comprobaciones comparan los tres `.docx` contra el Markdown canónico, cada una en un tipo
de contenido, y **lo que falta sale en su salida, fichero por fichero**. Se citan por **nombre**, no
por número: el número de comentario del código fuente (`# --- N.`) es una etiqueta histórica que no
identifica la comprobación, y dos de ellas ya llevaban una cita mal puesta por confiar en el número
(`FINDINGS §F146`).

| Comprobación (nombre) | Qué compara |
|:---|:---|
| «la prosa de los tres .docx sigue al Markdown» | la **prosa**, párrafo a párrafo |
| «las tablas y la bibliografia de los .docx siguen al Markdown» | las **tablas** celda a celda y la **bibliografía** |
| «los encabezados y su nivel siguen al Markdown» (o equivalente) | los **encabezados** |
| «las figuras del Markdown estan en los tres .docx» | las **figuras** y las citas colgantes |
| «ninguna frase retirada sobrevive en los entregables» | frases que la fuente **corrigió** y el `.docx` todavía afirma |

**No hay una cifra de «fallos hoy» escrita aquí a propósito.** Cambia cada vez que se corrige el
Markdown —es el defecto de `FINDINGS §F134`, que ya alcanzó a un resultado estadístico en `§F149`— y
un número copiado en este documento se desfasa sin que nada avise. **Ejecuta tú mismo**
`python3 tools/verificar_informe.py` y trabaja contra esa salida, no contra una cifra de este
documento.

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

## 0.bis Se adoptó un consolidado nuevo el 2026-09-09: la Tabla 7 entera cambió

**Esto es nuevo desde que se escribió este encargo y va primero, porque toca más texto que
cualquier otra pieza.** El autor decidió la decisión 1: el estudio se mide ahora sobre
`ANALISIS_CONJUNTO_20260909_FIX` (re-corrida completa, 113 artículos por grupo, sin el defecto de
`Locations` sin anotar) en lugar de `ANALISIS_CONJUNTO_20260907` (publicado). Detalle completo en
`FINDINGS §F154` y `§F155`.

**Lo que cambia, y por tanto lo que hay que copiar al `.docx` tal cual está en el Markdown, no
reconstruir de memoria:**

### Pieza 11 — La Tabla 7 entera (26 celdas) y su párrafo introductorio

Las 26 celdas de F1 cambian, y con ellas la columna «Δ significativo»: **solo uno** de los trece
modelos es significativo ahora (`nemotron-mini:4b`), no dos. `llama3.2:latest` pierde el resalte en
negrita y su «sí (p=0,007)».

### Pieza 12 — El párrafo de §5.3.1 con el ANOVA, Tukey, Levene y Friedman

F pasa de 38,2222 a **119,7502**, y la p ya no se escribe como número: se escribe **«p < 10⁻³⁰⁰»**,
porque subdesborda. Tukey pasa de «dos de los trece» a **«uno de los trece»**. Levene **cambia de
verbo**: pasaba de «no detecta» a «sí detecta» heterocedasticidad. Friedman pasa de 1 169,23 a
**1 802,3671**. Es un párrafo largo y denso; cópialo entero, no lo edites cifra a cifra.

### Pieza 13 — El párrafo de correlación de §5.3.1 y la conclusión 6 (§7.1)

Los dos coeficientes **coinciden** ahora en el veredicto —antes discrepaban—, y ninguno alcanza
significancia. La conclusión 6 pasa de «dos modelos» a **«uno»**, con la explicación de por qué
`llama3.2:latest` ya no cuenta.

### Pieza 14 — El resumen y el abstract, sincronizados

Cambian en el mismo punto los dos: «dos de los trece» → «el más débil de los trece»; «76,55 % / 
90,16 %» → «81,47 % / 90,16 %» (el 90,16 % del dominio **no cambia**). Cópialos **enteros y a la
vez**: la regla de `CLAUDE.md` exige que digan exactamente lo mismo en los dos idiomas.

### Pieza 15 — Las conclusiones 1 y 3, y el párrafo de soberanía de §6

La conclusión 1 pierde la cláusula «bajo la convención original…» —ya no aplica— y cita 81,47 % en
vez de 76,55 %. El coste de soberanía (conclusión 3 y §6) pasa de **«cuatro puntos»** a **«menos de
un punto»** (82,13 − 81,47 = 0,66 pp). Es un cambio de conclusión, no solo de cifra: revisa que no
quede ninguna mención suelta a «cuatro puntos» en el entregable.

### Pieza 16 — La fila de este trabajo en la Tabla 1 (comparación con la literatura)

Su celda de F1 pasa de 76,55 % a **81,47 %**.

### Pieza 17 — La Figura 2

Se **regeneró** (`tools/generar_figuras_informe.py`), no solo cambió el dato: el título del panel
(b) y su anotación de correlación son distintos. Sustituye el PNG entero, no lo retoques.

### Pieza 18 — El párrafo de corridas múltiples del Anexo I, ampliado

Se le añadieron dos párrafos nuevos al principio, declarando que hubo **dos corridas completas**
del estudio y cuál es la de referencia. Va con la pieza 1 si decides insertar esa subsección.

**El resto del Anexo I NO cambia**: se mantiene deliberadamente histórico, describiendo el corpus
publicado. No propagues los números de la Tabla 7 nueva hacia la Tabla 19 del Anexo I.

**El resaltado creció de 14 a 18** por estos cambios de prosa cuando se escribió esta sección; ya
había vuelto a moverse antes de que llegaras a esta pieza (ver 0.ter). **No copies este número**:
usa el recuento en vivo de la comprobación «el .docx no anade resaltes ni guiones».

---

## 0.ter Seis correcciones más el mismo día (`FINDINGS §F158`, `§F159`), después de que empezaras

Llegaron mientras la pieza anterior ya estaba escrita, y son más prosa que hay que resincronizar.
Ninguna toca la Tabla 7 ni ninguna cifra de la 0.bis; son pasajes que quedaron describiendo un
defecto ya corregido como si siguiera vigente, más una etiqueta que faltaba.

### Pieza 19 — El «Corpus 3» que faltaba en §4.1

El autor señaló que §4.1 promete «tres corpus complementarios» y solo etiqueta dos («Corpus 1»,
«Corpus 2»); el de N=120 se describía después, sin la misma etiqueta, y quedaba confuso. Se añadió
un párrafo breve, «Corpus 3 — Real Balanceado (N=120, Estudio Principal)», inmediatamente después
del párrafo del Corpus 2 y antes de `#### 4.1.1`. Cópialo tal cual: es nuevo, no una edición de un
párrafo existente.

### Pieza 20 — Dos frases de §3.3, antes de la Figura 1

La frase de la cifra del 66,0 % de falsos positivos y la frase de cierre del párrafo («…exige
volver a inferir, que es lo que hará la re-corrida pendiente») cambiaron para decir que esa cifra
es del **consolidado publicado** y que la re-corrida **ya se hizo**. Es el mismo párrafo largo de
siempre, con dos frases reescritas dentro; no lo sustituyas entero, localiza las dos frases nuevas
y reemplázalas donde correspondan dentro del párrafo que ya tienes.

### Pieza 21 — La leyenda de la Figura 1

Cambia de «los veintiséis grupos que sostienen la Tabla 7» (presente) a una redacción que aclara
que describe el consolidado publicado, previo a la corrección. Es solo la leyenda bajo la imagen;
la imagen misma no cambia.

### Pieza 22 — La conclusión 7 de §7.1

Pasa de presente («el corpus N=120 almacena…») a pasado, con la misma salvedad de «ya corregido»
que ya lleva la conclusión 6 vecina sobre Locations. Las cifras (20,1 %, 87 %, los rangos de F1 por
artículo afectado) no cambian, solo el tiempo verbal y una frase final nueva.

### Pieza 23 — Los puntos 7 y 8 de §7.2

Los dos dejaron de ser «trabajo futuro pendiente»: ambos pasan a título con **«ya realizada»** /
**«ya realizado»**, sin la etiqueta «Prioridad Alta» que llevaba el punto 8 (ya no aplica a trabajo
completado). El contenido y las cifras se conservan; cambia el encuadre de pendiente a hecho.

### Pieza 24 — El resumen y el abstract, otra vez (`§F158`)

Sobre la pieza 14 de la 0.bis: el autor pidió aclarar más «en el dominio», que no se entendía sin
contexto en la primera página. El resumen y el abstract se reescribieron una tercera vez ese mismo
día para nombrar el corpus AML/KYC explícitamente. **Cópialos enteros y a la vez** —la regla de
`CLAUDE.md` exige que digan lo mismo en los dos idiomas—, no apliques solo la diferencia con tu
versión anterior: es más seguro sustituir el párrafo completo.

---

## 0.quater Un párrafo nuevo en §4.1.2, sobre qué es `Locations` y por qué importa

### Pieza 25 — Definición de la categoría `Locations` en la descripción del Corpus 3

§3.3 ya documenta el defecto de anotación de `Locations` (por qué estaba vacía y cómo se corrigió),
pero no dice en ningún sitio, con la claridad que pide un lector que llega sin ese contexto, qué es
la categoría: lugares geográficos mencionados en el artículo (países, ciudades, sedes de organismos
reguladores), relevantes para establecer la jurisdicción de un caso de cumplimiento normativo. Se
añadió un párrafo nuevo en `#### 4.1.2 Extensión a Corpus Real N=120`, inmediatamente después del
párrafo que cierra esa subsección («Los resultados sobre N=120 se presentan como complemento...») y
antes de `### 4.2 Modelos evaluados`. Da la definición y remite a §3.3 para el defecto y su
corrección; no repite esa narrativa. Cópialo tal cual, es nuevo, no una edición de un párrafo
existente, y no toca ninguna cifra de las piezas anteriores.

---

## 0.quinquies Se retiró la Tabla 20, y el párrafo de §5.3.1 traía tres cifras equivocadas

El autor preguntó, sobre `gemma4:12b-mlx`, por qué el informe daba dos cifras para el mismo
benchmark y N; la investigación mostró que el informe estaba bien (el error era una cita mía sin
fecha), pero el autor pidió ir más allá: **para cada benchmark y N, el cuerpo del estudio presenta
una sola cifra vigente, la última**, y la historia queda como anécdota de prosa, no como tabla de
resultados alternativos. Es una excepción explícita a la política aditiva por defecto de
`CLAUDE.md`, confirmada por el autor tras preguntarle directamente si quería tocar el Anexo I.

### Pieza 26 — Se retiró la Tabla 20 del Anexo I

La Tabla 20 («Grupos con más de una corrida sobre N=120, con el motivo de la sustitución y la
evidencia», ocho filas) y el párrafo que la introducía se sustituyeron por dos párrafos de prosa
más cortos, sin tabla, que declaran los cuatro modelos que tuvieron una re-ejecución parcial y por
qué, sin imprimir las cifras de las corridas descartadas. Si ya insertaste el Anexo I completo
(piezas 1 y 9) en algún `.docx`, **retira la Tabla 20 y su leyenda** y sustitúyelos por el texto
nuevo del Markdown, copiado tal cual. Si no lo habías insertado, no hay nada que retirar, solo que
no insertar la tabla vieja de ahora en adelante.

### Pieza 27 — El párrafo de `gpt-oss:20b` decía algo que ya no es cierto — **sustituye a la pieza 9**

La pieza 9, más abajo, describía un párrafo que afirmaba «la de referencia es la primera [corrida
a 2048 tokens]... las cifras de `gpt-oss:20b` de la Tabla 7 deben leerse con la reserva anterior».
Eso era correcto antes de que la re-corrida completa se adoptara para la Tabla 7, y dejó de serlo:
comprobado contra `run_config.json` de la fuente vigente, los trece modelos —incluido
`gpt-oss:20b`— comparten `max_tokens=4096` en la re-corrida adoptada, así que **no queda ninguna
reserva de comparabilidad que declarar**. El texto nuevo, dentro de la misma subsección «Corridas
múltiples del mismo modelo», ya no habla de «dos mediciones» ni de cuál es «la referencia»: dice
que la re-corrida completa resolvió los tres defectos operativos de una vez y que las cifras
vigentes son las de la Tabla 7, sin reserva. Cópialo tal cual si insertas esa subsección.

### Pieza 28 — Tres cifras equivocadas en el párrafo de §5.3.1, y de paso más corto de leer

A petición del autor de simplificar el párrafo del ANOVA/Tukey/Levene/Friedman/correlación,
verifiqué cada cifra contra la Tabla 7 antes de tocar la prosa y aparecieron tres errores reales:
«nueve de los trece modelos mejoran» (son **once**), «−0,54 y −0,18 puntos en los dos de 31B»
(son **+0,81 y +0,97**, ambos positivos) y una contradicción interna entre «solo... en
`nemotron-mini:4b`» (un modelo) y «solo dos [modelos] lo hagan de manera estadísticamente sólida»
en el mismo párrafo (es **uno**, según la Tabla 7). El párrafo completo se reescribió más corto,
en cinco unidades que abren con la pregunta que responden, sin perder ninguna prueba estadística
del original (F, p, Tukey, Levene, Friedman, Spearman, Pearson, el control de retirar
`nemotron-mini:4b`). **Sustituye el párrafo entero por el del Markdown**, no apliques solo el
cambio de cifras sobre tu versión: cambió también la estructura de frases.

> **Actualización: ya se propagó.** La nota de arriba avisaba que los tres `.docx` todavía tenían
> el texto viejo; en tu segunda pasada (§2.25) ya no lo tienen — comprobado con
> `tools/verificar_informe.py`, que confirmó que las siete frases retiradas de esta ronda (las tres
> de aquí más las de sobriedad tipográfica) dejaron de aparecer en los tres entregables. Retiradas
> de `FALLOS_DECLARADOS`. Si aún no habías llegado a esta pieza al leer esto, ya no hace falta:
> compruébalo con el verificador antes de repetir trabajo.

---

## 0.sexies Sin fechas de calendario en el cuerpo, y una anécdota retirada por completo

Dos pedidos del autor, seguidos, sobre pasajes que ya habías rendereado en tu segunda pasada.
**Ninguno cambia una cifra de resultado**; los dos son prosa.

### Pieza 29 — Ocho fechas de calendario retiradas del cuerpo (capítulos 1-7)

El autor pidió que el cuerpo del informe no mencione en qué fecha del proceso interno ocurrió cada
corrección, aunque la corrección misma se siga declarando. Afectó a §3.3 (dos frases), §4.1.2 (dos),
§5.3 (una, ahora también retirada entera por la pieza 30), §5.3.1 (una) y §7.1 (dos, puntos 7 y 8).
Ningún cambio de cifra, solo se quitó «el 8 de septiembre de 2026» / «(1 de septiembre de 2026,
commit...)» y variantes, dejando el resto de cada frase intacto. **Los Anexos H e I no cambian**: el
autor confirmó que la regla es solo para el cuerpo, esos anexos siguen siendo bitácora fechada. Copia
las frases del Markdown, son ediciones puntuales dentro de párrafos existentes, no párrafos nuevos.
Detalle en `FINDINGS §F162`.

### Pieza 30 — Retirada por completo la nota de «particularidad de procedencia» en §5.3

El párrafo que empezaba «Vale la pena señalar una particularidad de procedencia» (F1 de 79,03 % para
`gemma4:31b`, de una corrida cuyos datos se perdieron por sobrescritura) se **eliminó entero**, no se
reescribió: el autor pidió, con calificación explícita de gravedad, no mencionar en el cuerpo ningún
dato que no tenga evidencia recalculable, ni siquiera como anécdota de robustez metodológica. **Borra
el párrafo completo** de tu `.docx` (las dos frases, entre «El resultado no depende, por tanto, de
unos pocos textos extremos.» y el encabezado `#### 5.3.1`); no queda ningún resto suyo en el Markdown
que copiar. Esto baja el recuento de guiones largos del cuerpo de 90 a 88 — normal, no lo compenses
añadiendo nada. Detalle en `FINDINGS §F163`.

---

## 0.septies El profesor pidió enriquecer el marco teórico (reparo 4), y el capítulo 2 cambió de tamaño y de numeración

**El capítulo 2 entero creció y sus subsecciones se renumeraron.** Antes de esta ronda tenías
`### 2.4 Validación estadística de comparaciones múltiples` y `### 2.5 Estado del arte y criterios
de selección`. Ahora hay una `### 2.4` nueva antes de esas dos, que pasan a ser `### 2.5` y `### 2.6`
respectivamente. **No es una renumeración cosmética**: la `2.4` nueva tiene texto propio que copiar,
no solo un cambio de etiqueta.

### Pieza 31 — Sección nueva completa: `2.4 Arquitectura de ejecución concurrente y aislamiento de proveedores`

Cuatro párrafos nuevos (441 palabras) entre el final de `2.3` (que termina en «...lo que resulta
incompatible con el requisito de soberanía que motiva el trabajo.») y el inicio de la antigua `2.4`
(que ahora es `2.5`, ver pieza 32). Copia el encabezado y los cuatro párrafos tal cual del Markdown:
son contenido nuevo, no una edición de texto existente.

### Pieza 32 — Renumerar `2.4` → `2.5` y `2.5` → `2.6`, y dos párrafos nuevos dentro de la `2.5`

Cambia el número de los dos encabezados (el título de cada uno no cambia, solo el número). Dentro de
la que pasa a ser `### 2.5 Validación estadística de comparaciones múltiples`, entre el párrafo que
termina en «...ninguna conclusión depende de unos pocos casos extremos.» y el que empieza «Conviene
retener una asimetría de interpretación...», se insertan dos párrafos nuevos (232 palabras, sobre
homocedasticidad/Friedman y sobre Pearson/Spearman). Cópialos del Markdown.

### Pieza 33 — Un párrafo nuevo en `2.1`, y dos recortes en `§3.3` y `§5.3.1` que van con ella

En `### 2.1`, después de la frase que termina en «...coincidan a la vez sus límites y su categoría.»,
se añade un párrafo nuevo (143 palabras) sobre los criterios de coincidencia entre entidad extraída y
de referencia (exacta, por tokens, difusa por distancia de Indel). **Esto viene acompañado de dos
recortes en otras secciones, para no duplicar la misma explicación dos veces**:

- En `§3.3`, el párrafo que empieza «La comparación entre lo extraído y la anotación de referencia...»
  perdió la definición de la distancia de Indel (ahora vive en `2.1`) y quedó más corto. Sustituye el
  párrafo entero por el del Markdown; no es solo un recorte de frase, la redacción cambió alrededor.
- En `§5.3.1` (ahora bajo la sección `2.5` renumerada, no confundir), el párrafo que empieza «Una
  salvedad de diseño...» perdió la explicación de qué son Levene y Friedman (ahora en `2.5`) y quedó
  más corto. Sustituye el párrafo entero por el del Markdown.

> **Aviso de presupuesto de páginas.** Estas tres piezas juntas añaden bastante más de lo que quitan:
> el margen antes de este encargo era de unas 891 palabras respecto del límite de 25 páginas, y bajó
> a ~121. **Confirmado contra la guía institucional** (`Instrucciones Informe Final de
> Tesina/tesinas-finales-2026.pdf`, diapositivas 16 y 25): el límite es 25 páginas **sin anexos**
> más hasta 25 páginas **adicionales** de anexos — no un total de 25. No hay que recortar ningún
> Anexo por presupuesto: hoy miden ~8,7 páginas estimadas, lejos de su propio límite.

### Pieza 34 — El listado de código `LLMProvider` se movió de `§3.2` al nuevo `Anexo A.1`

Para recuperar parte del margen (de 121 a ~178 palabras), el bloque de código Python de `§3.2`
(la clase `LLMProvider(ABC)`) se trasladó a una subsección nueva, `#### A.1 Interfaz común de
proveedores (LLMProvider)`, justo después de la Tabla 9 del Anexo A y antes del Anexo B. En `§3.2`
solo queda una frase que remite a ella («...tras una interfaz común (`LLMProvider`, Anexo A.1)»,
reemplazando el párrafo y el bloque de código que tenías). Copia ambos cambios del Markdown: el
párrafo recortado de `§3.2` y la subsección nueva del Anexo A.

Detalle completo en `FINDINGS §F164`.

> **La nota de cierre que iba aquí quedó superada: sí hubo una ronda más.** El autor había
> confirmado que el margen de 178 palabras bastaba, y una revisión después cambió de opinión («un
> cambio: sí enriquecer más el marco teórico»). Ver la **0.octies** justo debajo.

---

## 0.octies Segunda ronda: embeddings y bases de datos vectoriales en `2.3`

### Pieza 35 — Un párrafo nuevo en `2.3`, sobre qué es un embedding y una base de datos vectorial

Después del párrafo que cierra la comparación de las variantes de RAG (el que termina en «...El
capítulo 5 contrasta empíricamente ambas.») se añade un párrafo nuevo (111 palabras) que explica el
mecanismo común a las dos variantes: qué es un **embedding**, por qué reduce la recuperación a una
búsqueda por vecino más próximo, y qué papel cumple una **base de datos vectorial** (ChromaDB [32]
en este trabajo). Es contenido nuevo, no una edición de un párrafo existente. Cierra un vacío real:
el cuerpo usaba «similitud vectorial» (§5.6) y citaba ChromaDB (Anexo D) sin definir ninguno de los
dos conceptos antes.

> **Aviso de presupuesto, más urgente que en la ronda anterior.** El margen bajó de 178 a **74
> palabras** respecto del límite de 25 páginas (estimado en 24,89). A este nivel, **cualquier
> párrafo adicional que el autor pida más adelante necesitará, primero, un recorte de tamaño
> equivalente en otra parte del cuerpo** — ya no hay margen para sumar sin restar. Si al maquetar
> te acercas al límite real, avisa al autor antes de recortar nada por tu cuenta.

Detalle completo en `FINDINGS §F165`.

> **Actualización: la crisis de presupuesto de arriba ya se resolvió, con margen de sobra.** La
> pieza 36, justo debajo, comprime un párrafo grande de `§3.3` y libera 266 palabras. El margen
> pasó de 74 a ~327. Ya no hace falta vigilar el presupuesto con la urgencia que pedía esta nota.

---

## 0.nonies El párrafo de `§3.3` sobre `Locations` se reescribió: más corto, más claro, y con la conclusión primero

### Pieza 36 — Reescrito el párrafo largo de `§3.3` sobre el defecto de `Locations`

El autor lo encontró confuso al releerlo y temió que un comité lo interpretara como una mala
decisión histórica sin resolver — el párrafo abría con la limitación técnica y solo mencionaba al
final que ya estaba corregida. **Sustituye el párrafo entero** (el que empieza «Un tercer límite,
de naturaleza distinta a los anteriores...» y termina en «...adoptada en §5.3.1 como fuente de la
Tabla 7 vigente.») por el nuevo del Markdown: no es un recorte de frases sueltas, cambió el orden y
se resumió el detalle histórico con una remisión al Anexo I. **Dos cifras no se pueden tocar**: la
fracción «12 852 de 19 464» junto al 66,0 %, y la referencia «la Figura 1» con artículo — dos
comprobaciones del verificador exigen exactamente esa forma. Si reformulas la frase, consérvalas
literales.

**Efecto en el presupuesto de páginas**: este recorte por sí solo libera ~266 palabras, más que
suficiente para compensar la pieza 35. Detalle completo en `FINDINGS §F166`.

---

## 0.decies El autor pidió las referencias de Pearson y Spearman, y hay un anexo nuevo (`FINDINGS §F168`)

### Pieza 37 — Dos citas nuevas en la bibliografía: `[40]` y `[41]`

Añadidas al final de la lista de referencias, después de `[39]` (Dror et al.):

- `[40] K. Pearson, "Note on Regression and Inheritance in the Case of Two Parents," Proceedings of
  the Royal Society of London, vol. 58, pp. 240-242, 1895.`
- `[41] C. Spearman, "The Proof and Measurement of Association Between Two Things," American
  Journal of Psychology, vol. 15, no. 1, pp. 72-101, 1904.`

En §2.5 (Validación estadística), el párrafo que explica los dos coeficientes ahora los cita:
«El coeficiente de **Pearson** [40] mide la asociación lineal... el de **Spearman** [41], calculado
sobre los rangos...». **No se citan de nuevo en §5.3.1**: ahí solo se dan las cifras, siguiendo el
mismo patrón que ya usan Tukey y AIMD en este informe (la teoría cita, el resultado remite a ella).

### Pieza 38 — Anexo J, nuevo, después del Anexo I

**Anexo entero por añadir**, con su encabezado H3 («Anexo J — Correlación entre capacidad y
beneficio del RAG: fuente y reproducción»), dos párrafos y la **Tabla 20**.

**Sobre el número de la tabla**: hubo una Tabla 20 antes, la que la pieza de `0.quinquies` mandó
retirar (ocho filas de F1 de corridas descartadas). Esa ya no existe en el Markdown ni en el
entregable desde entonces. **Esta es una tabla distinta**, sobre un tema distinto, que reutiliza el
mismo número porque vuelve a ser el siguiente disponible tras el retiro. No es la misma pieza ni
hay que buscar una Tabla 20 vieja que sustituir: es contenido nuevo, íntegro.

El texto completo del anexo, tal cual debe quedar en el Markdown (cópialo entero, incluida la
tabla):

> ### Anexo J — Correlación entre capacidad y beneficio del RAG: fuente y reproducción
>
> Las dos cifras de §5.3.1 sobre la relación entre el desempeño base de un modelo y la mejora que
> le aporta el KB RAG —Spearman −0,0879 (p = 0,7752) y Pearson −0,4816 (p = 0,0956), sobre los N=13
> pares (F1 base, ΔF1) de la Tabla 7— proceden de `tools/robustez_estadistica.py`, que las calcula
> con `scipy.stats.pearsonr` y `scipy.stats.spearmanr` sobre el CSV consolidado de la re-corrida
> adoptada y las persiste en `repos/ner-llm-entity-benchmark/results/ROBUSTEZ_ESTADISTICA_20260909_FIX/robustez.json`. El
> coeficiente de **Pearson** [40] mide la asociación lineal entre las dos variables y es sensible a
> los valores atípicos; el de **Spearman** [41], calculado sobre sus rangos y no sobre los valores,
> capta cualquier relación monótona sin asumir linealidad, a costa de ignorar la magnitud de la
> asociación. Ninguno de los dos alcanza el 5 % de significancia sobre los trece modelos.
>
> La Tabla 20 recalcula ambos coeficientes retirando, uno a la vez, cada uno de los trece modelos
> de la muestra, para identificar cuánto depende el resultado de un único caso. Solo la ausencia de
> `nemotron-mini:4b` cambia el signo y la significancia del coeficiente de Pearson; las otras doce
> retiradas lo dejan entre −0,47 y −0,62, con el mismo signo que sobre la muestra completa.
>
> _Tabla 20. Sensibilidad de la correlación capacidad-beneficio a la retirada de cada modelo (N=12
> restantes por fila)_
>
> | Modelo retirado | Pearson r | Pearson p | Spearman ρ |
> |:---|---:|---:|---:|
> | deepseek-r1:1.5b | −0,6151 | 0,0333 | −0,0070 |
> | gemma4:12b-mlx | −0,4964 | 0,1006 | −0,1259 |
> | gemma4:31b-cloud | −0,4746 | 0,1190 | −0,0559 |
> | gemma4:31b-mlx | −0,4773 | 0,1166 | −0,0559 |
> | gemma4:latest | −0,4955 | 0,1014 | −0,1259 |
> | gemma:latest | −0,5047 | 0,0942 | −0,2238 |
> | gpt-oss:20b | −0,4832 | 0,1115 | −0,0699 |
> | llama3.1:8b | −0,4840 | 0,1108 | −0,0839 |
> | llama3.2:latest | −0,5063 | 0,0930 | −0,0070 |
> | mistral-nemo:latest | −0,5971 | 0,0404 | −0,2378 |
> | **nemotron-mini:4b** | **+0,0120** | **0,9706** | **+0,1608** |
> | qwen2.5:14b | −0,4767 | 0,1171 | −0,1469 |
> | qwen3:8b | −0,4771 | 0,1168 | −0,1678 |
>
> El detalle íntegro, con más decimales, está en el propio artefacto JSON citado al inicio de este
> anexo.

**Efecto en el presupuesto de páginas**: el anexo vive fuera del cuerpo (25 páginas), que no se
toca. La bibliografía y la cita de §2.5 sí están en el cuerpo, pero son dos líneas y dos palabras
sueltas — la estimación por palabras sigue en `ok` tras añadirlas. Detalle completo en
`FINDINGS §F168`.

### Pieza 39 — Cuatro citas más en §2.5 y §4.1.2, y cinco entradas de bibliografía nuevas (`FINDINGS §F169`)

Mismo patrón que la pieza 37: el párrafo de §2.5 sobre ANOVA/Friedman/Levene y el de §4.1.2 sobre
la `d` de Cohen ya explicaban esos métodos sin citar su origen. Añadidas cinco entradas más a la
bibliografía, después de `[41]`:

- `[42] R. A. Fisher, "Statistical Methods for Research Workers". Edimburgo: Oliver & Boyd, 1925.`
- `[43] M. Friedman, "The Use of Ranks to Avoid the Assumption of Normality Implicit in the Analysis of Variance," Journal of the American Statistical Association, vol. 32, no. 200, pp. 675-701, 1937.`
- `[44] H. Levene, "Robust Tests for Equality of Variances," in Contributions to Probability and Statistics: Essays in Honor of Harold Hotelling, I. Olkin, Ed. Stanford, CA: Stanford University Press, 1960, pp. 278-292.`
- `[45] M. B. Brown and A. B. Forsythe, "Robust Tests for the Equality of Variances," Journal of the American Statistical Association, vol. 69, no. 346, pp. 364-367, 1974.`
- `[46] J. Cohen, "Statistical Power Analysis for the Behavioral Sciences", 2.ª ed. Hillsdale, NJ: Lawrence Erlbaum Associates, 1988.`

En el párrafo de §2.5 (Validación estadística), el texto pasa de «el análisis de varianza (ANOVA)
de una vía, que contrasta...» a «...de una vía [42], que contrasta...»; de «La prueba no paramétrica
de **Friedman** es su análogo...» a «...de **Friedman** [43] es su análogo...»; y de «se contrasta
con la prueba de **Levene**, en su variante centrada en la mediana (Brown-Forsythe), más robusta...»
a «...de **Levene** [44], en su variante centrada en la mediana (Brown-Forsythe) [45], más
robusta...». En §4.1.2, «una *d* de Cohen de 0,12» pasa a «una *d* de Cohen [46] de 0,12».

**Presupuesto de páginas — atención aquí, no es solo una nota de rutina.** Esta pieza añade ~139
palabras al cuerpo (cinco entradas de bibliografía). La estimación por palabras de este equipo sigue
en `ok` (margen de ~128 palabras), pero la medición **real** que tu propia entrada `§2.27` reportó
—25 de 25 páginas, sin margen— es anterior a esta pieza. Es probable que, al maquetar esto, el
cuerpo pase a 26 páginas. **Antes de considerar tocar el texto**, aplica el orden que fija
`CLAUDE.md`: ajustar el espaciado de encabezados, el interlineado y el cuerpo de letra de los
bloques de código (hasta 7 pt si hace falta) — eso es lo que probablemente baste. Solo si eso no
alcanza, avisa antes de tocar contenido: no está autorizado suprimir texto para ganar espacio sin
que el autor lo confirme expresamente.

### Pieza 40 — Retirada la Figura 1 vieja (composición de FP), y renumerada la que queda (`FINDINGS §F170`)

A petición expresa del autor. **Se retira del cuerpo**, en §3.3:

- La imagen `![Composición de los falsos positivos...](../../figuras/falsos-positivos.png)`.
- Su leyenda: `_Figura 1. Composición de los falsos positivos sobre el consolidado publicado...`
  (la que empieza así y termina en «...a partir de `results/COMPOSICION_FP_20260908/`»).
- La frase parentética «(la Figura 1 lo ilustra)» dentro del párrafo de al lado. **No toques nada
  más de ese párrafo**: la fracción «66,0 %» y «12 852 de 19 464» se conservan literales, palabra
  por palabra — dos comprobaciones del verificador las exigen así.

**La otra figura del cuerpo (el efecto del KB RAG) se renumera de Figura 2 a Figura 1**, porque
ahora es la única y la numeración debe empezar en 1:

- La imagen y su leyenda no cambian de contenido, solo el número: `_Figura 2. Efecto...` pasa a
  `_Figura 1. Efecto...`.
- La frase que la cita en el cuerpo del texto: «La Figura 2 recoge ambas lecturas» pasa a «La
  Figura 1 recoge ambas lecturas».

**No toques** el script `generar_figuras_informe.py` ni el artefacto `COMPOSICION_FP_20260908/`:
siguen existiendo, solo la imagen dejó de incrustarse en el Markdown.

**Efecto en el presupuesto de páginas**: neto positivo, compensa parte de lo que añadió la pieza 39
el mismo día — la figura y su leyenda pesaban más que las cinco entradas de bibliografía nuevas.

### Pieza 41 — §3.3 comprimido de ~240 palabras a dos frases (`FINDINGS §F171`)

El autor decidió, tras revisar qué protege `CLAUDE.md`, que la integridad de la medición rige
**desde el 8 de septiembre en adelante**; un defecto anterior a esa fecha es historia cerrada y no
necesita desarrollar su mecanismo en el cuerpo. **Sustituye el párrafo entero** de §3.3 sobre
`Locations` (el que empieza «Un tercer límite, de naturaleza distinta...» y termina en «...se
conservan en el Anexo I.») por el nuevo, más corto:

> Un tercer límite, anterior a la re-corrida del 8 de septiembre de 2026 que hoy sostiene la Tabla
> 7, ya está corregido y no afecta a ningún resultado vigente: un defecto de la cadena de
> preparación de datos dejaba sin anotar la categoría **localizaciones** (§2.1) en el consolidado
> publicado, de modo que cada acierto del modelo en ella se contabilizaba como falso positivo, y de
> ahí procedía el **66,0 %** de los falsos positivos de aquel consolidado, 12 852 de 19 464. El
> detalle histórico y la medición restringida equivalente se conservan en el Anexo I.

**Cifras que no se pueden tocar**: «66,0 %» y «12 852 de 19 464», exactas, una comprobación del
verificador las exige literales. **No toques el Anexo I**: sigue con el detalle completo, sin
cambios — esta pieza es solo del cuerpo.

**Efecto colateral en guiones largos**: el párrafo viejo tenía dos guiones largos que el nuevo no
tiene; el recuento de guiones del `.md` bajó de 93 a 92. Cuando regeneres, tu propio recuento
debería bajar en la misma proporción; si no baja, revisa que copiaste el párrafo nuevo completo y no
una mezcla con el viejo.

### Pieza 42 — Tres compresiones más en §7.1/§7.2, y una referencia obsoleta corregida en el Anexo H (`FINDINGS §F172`)

Mismo criterio que la pieza 41, aplicado a tres lugares más:

**a) §7.1, conclusión 6.** Dentro del párrafo largo sobre el KB RAG, **retira por completo** (no
sustituyas, borra) la frase: «, versus el dict-RAG (v1.0), que en un sondeo exploratorio N=5 sobre
el mismo modelo, no persistido en `results/`, degradó el F1 hasta 0.2367 (−57.8% respecto de su
propio baseline), degradación confirmada después en la corrida histórica N=120 previa a la
re-corrida, donde ese mismo modelo caía de 0.3611 a 0.3113.» — el párrafo debe quedar con «...sin el
signo negativo que mostraba el corpus con el defecto de anotación sin corregir. Su efectividad
parece modularse...» (nota el punto donde antes había una coma). **No toques nada más del párrafo**:
la mención de ρ = −0,09 más adelante se queda igual.

**b) §7.2, punto 7 (mojibake).** Sustituye el párrafo completo (el que empieza «Normalización de
codificación del corpus y re-evaluación: ya realizada...» y termina en «...verificado con
`tools/analisis_mojibake.py`.») por: «**Normalización de codificación del corpus: ya realizada.** El
corpus N=120 publicado tenía nombres con *mojibake* (`JosÃ© Bono` en vez de **José Bono**), corregido
antes de la re-corrida del 8 de septiembre que hoy sostiene la Tabla 7: el corpus vigente tiene 0
artículos con este defecto, verificado con `tools/analisis_mojibake.py`. Detalle del efecto y su
magnitud en el Anexo H.» **No toques el Anexo H** (ni H.3 ni la Tabla 18): esta pieza es solo del
punto 7 de §7.2.

**c) §7.2, punto 8 (`Locations`).** Sustituye el párrafo completo (el que empieza «Recuperación de
las localizaciones que el conversor descartaba: ya realizada...» y termina en «...119 de los 120
registros.») por: «**Anotación de la categoría `localizaciones`: ya realizada.** El consolidado
publicado no anotaba esta categoría (§3.3), y de ahí procede el 66,0 % de los falsos positivos de
ese consolidado. Corregido antes de la re-corrida del 8 de septiembre: el corpus vigente tiene 545
localizaciones en 119 de los 120 registros. Detalle en el Anexo I.» **La frase «procede el 66,0 % de
los falsos positivos» debe quedar literal**: una comprobación del verificador la exige así. **No
toques el Anexo I.**

**d) Anexo H.4, «Cómo debe repararse» — una referencia que quedó obsoleta.** El párrafo final de esa
subsección decía «...y la corrección exigiría re-ejecutar el estudio completo. Se documenta por
tanto como limitación (§5.3.1) y como línea de trabajo futuro (§7.2, punto 7).» — **esto es falso
hoy**, esa corrección ya se ejecutó. Sustitúyelo por: «...y la corrección exigió re-ejecutar el
estudio completo. Eso es lo que hizo la re-corrida del 8 de septiembre que hoy sostiene la Tabla 7
(§5.3.1): el corpus vigente no arrastra este defecto.»

**Efecto colateral en resaltes**: estas tres compresiones quitan negritas que el `.docx` todavía
tiene («ya realizada» en dos títulos de punto, entre otras); tu propio recuento de resaltes del
cuerpo puede subir temporalmente frente a `BOLD_CUERPO_BASE=8` hasta que regeneres — es exactamente
lo que este mismo encargo ya advirtió en la pieza 30 con el mismo mecanismo.

**Efecto en el presupuesto de páginas**: neto reductor, con margen — estas tres compresiones juntas
quitan más de 200 palabras del cuerpo.

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

> **Y una celda mas de la misma Tabla 8, corregida hoy en el Markdown:** el indice Tok/s/B de
> `llama3.2 (3B)` pasa de **26.5** a **26.44**, para unificarlo con las otras tres apariciones del
> mismo dato (Tabla 4, Hallazgo 4, §5.5). El 26.5 redondeaba un Tok/s que ya venia redondeado; el
> valor real es 79,3453 / 3 = 26,4484. Ver `FINDINGS §F152`.

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

### Pieza 9 — Un pasaje del Anexo I que hoy dice algo falso, si decides insertarlo

Va **con la pieza 1**, no aparte: forma parte de los párrafos del Anexo I que no llegaron al
entregable. Se anota como pieza propia porque si algún día se insertan, hay que insertar **la versión
corregida** y no la que el `.docx` habría tenido.

El Markdown decía «La re-corrida completa **pendiente** unifica el presupuesto en 4096 para los
trece». Era cierto al escribirlo y **dejó de serlo el 8 de septiembre**, cuando la re-corrida se
ejecutó: hay trece corridas `__N120` y las trece declaran `max_tokens=4096`. La fuente ya está
corregida y ahora **declara las dos mediciones**, dice cuál es la de referencia y por qué, que es lo
que la regla de integridad de `CLAUDE.md` obliga a hacer.

**Copia el texto del Markdown, no reconstruyas el párrafo de memoria.** Y si decides no insertar
ninguno de los párrafos del Anexo I, no pasa nada por esta pieza: el entregable no afirma la
falsedad porque tampoco afirma nada sobre eso.

> **Comprobación nueva que vigila esto, y la vas a ver fallar hasta que hagas la pieza 7.** Se llama
> **«ninguna frase retirada sobrevive en los entregables»** y va al revés que las demás: en lugar de
> comprobar que lo que está en la fuente llegó al `.docx`, comprueba que lo que la fuente **retiró**
> no siga vivo en él. Hoy da **nueve fallos**, tres frases por tres entregables, y son exactamente
> las dos atribuciones a OpenSanctions y la glosa de la última columna. Cuando termines la pieza 7 y
> la corrección de la Tabla 1, baja a cero sola.



### Pieza 10 — Dos etiquetas de fila de la Tabla 19, opcional y solo si insertas el Anexo I

Menor, y no bloquea nada: si decides insertar el Anexo I (piezas 1 y 9), de paso hay dos etiquetas de
fila que no identifican su configuración. **Es de una palabra por fila y no cambia ninguna cifra.**

1. La fila `llama3.2:latest` (sin sufijo) reproduce exacta a `llama3.2:latest_baseline` —el propio
   texto que sigue a la tabla ya lo dice—. Añádele el sufijo `_baseline`.
2. Las cuatro filas `zs-es` / `zs-en` / `fs-es` / `fs-en` no dicen a qué modelo pertenecen. Añade el
   nombre del modelo delante de la etiqueta de ablación.

Si no insertas el Anexo I, esta pieza no aplica y no hay que hacer nada. Ver `FINDINGS §F153`.

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
**pieza 7 primero** —es la única afirmación **falsa** de la lista, y no cuesta espacio nuevo porque corrige texto que ya está—, después **la pieza 1** —la subsección de corridas múltiples, que es la que un tribunal juzga—, después las figuras (pieza 6) con su prosa, después la referencia [38] con la celda de la Tabla 3 (piezas 3 y 5), después el punto 11 con la referencia [39] (pieza 8), que es el más largo y el primer candidato a no caber, y al final los cinco párrafos de límites y las filas de la Tabla 9 (pieza 2 y 4), que tienen eco en otras partes del documento. Las piezas 9 y 10 solo aplican si insertas la pieza 1, y van con ella.

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

**No compares contra un número fijo de fallos escrito en este documento.** Ese número cambia cada vez
que se corrige el Markdown —hoy va por la tercera cifra distinta en dos días— y un recuento copiado
aquí se desfasa sin que nada avise (es el defecto de `FINDINGS §F134`, y le pasó otra vez a
`§F149` con un resultado estadístico). **La comparación correcta es relativa**, antes y después de tu
trabajo:

1. **Corre el verificador ANTES de tocar nada** y guarda su resumen: `N fallos (N declarados, 0
   nuevos)`. Es tu línea de base.
2. Aplica las piezas que decidas aplicar.
3. **Corre el verificador DESPUÉS.** El número de declarados tiene que **bajar** — cada pieza cierra
   los fallos de las tres comprobaciones que la citan como responsable, y el propio verificador te
   dice cuáles son al ejecutarse; no hay que memorizarlos.
4. **Cero fallos NUEVOS, antes y después.** El verificador imprime «0 nuevos» cuando está limpio; si
   aparece un número mayor que cero, la inserción rompió algo, y **eso es más grave que lo que
   arregló**. Léelo, no lo ignores.
5. Las comprobaciones que citan tu pasada de maquetación —búscalas por nombre, no por número: **«las
   tablas y la bibliografía de los `.docx` siguen al Markdown»**, **«la prosa de los tres `.docx`
   sigue al Markdown»** y **«ninguna frase retirada sobrevive en los entregables»**— deben tener
   **menos** entradas que antes, idealmente ninguna. (Los números de comentario `# --- N.` del código
   fuente son etiquetas históricas y no identifican la comprobación: ver la nota al principio de
   `tools/verificar_informe.py`.)
6. La auditoría de afirmaciones sigue en **0 incumplidos**. El número de predicados también cambia
   con el tiempo; lo que importa es que la segunda columna sea cero.
7. Los tres `.docx` siguen siendo OOXML estructuralmente sano, que lo comprueba la comprobación
   **«los tres .docx siguen siendo OOXML estructuralmente sano»**.

**Si algo va mal, restaura desde el respaldo y dilo.** Un entregable corrupto es peor que un
entregable incompleto, y ninguna comprobación sirve de nada si el fichero no abre.

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
