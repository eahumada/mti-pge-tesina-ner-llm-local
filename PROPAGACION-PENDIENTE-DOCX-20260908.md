# Lo que falta propagar del Markdown a los tres `.docx`

**2026-09-08.** Para quien maquete: **no regenerar con pandoc.** Los `.docx` llevan correcciones manuales de
numeración multinivel, estilos de fila y saltos de página que una regeneración destruiría. La vía es
`tools/docx_replace_terms.py`, que edita el XML preservando el formato.

## Estado

Los tres `.docx` están congelados en el commit `6299d13` de hoy a las **04:25**. Desde entonces el Markdown
canónico ha recibido **22 commits**. El entregable, por tanto, **no es el informe**: es una versión de hace
medio día.

Verificado sobre el XML de `Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx`: 16 776
palabras, tablas 1 a 19, y **cero apariciones de la palabra «Figura»**.

## Lo que falta, por orden de gravedad

### 1. Una cifra equivocada en §3.3, que además ya no es la buena

El `.docx` dice, en §3.3:

> «el **65 %** de los falsos positivos del estudio, **20 946 de 32 201**, proceden de esa categoría»

Esa cifra es la del **Anexo I**, calculada sobre **42 configuraciones** que incluyen corridas después
declaradas inválidas. No describe «el estudio», que son 26 grupos. El Markdown dice ahora **66,0 %,
12 852 de 19 464**, calculado sobre esos 26 y trazable en `results/COMPOSICION_FP_20260908/`. Ver
`FINDINGS §F69`.

Afecta a **dos** puntos del `.docx`: §3.3 y §7.2, que repite la misma cifra.

### 2. Las dos figuras no existen en el `.docx`

Hay que insertarlas con el estilo `image` y su leyenda debajo y centrada con `figurecaption`, como manda la
norma. Los ficheros están en `doc/figuras/`:

| Figura | Sección | Fichero |
|:---|:---|:---|
| Figura 1 | §4.4, tras «según recoge la Figura 1» | `doc/figuras/falsos-positivos.png` |
| Figura 2 | §5.3.1, tras «La Figura 2 recoge ambas lecturas» | `doc/figuras/efecto-kb-rag.png` |

Las dos leyendas están en el Markdown y deben copiarse literalmente.

### 3. La Tabla 20 no existe

El Anexo I incorpora ahora el apartado «Corridas múltiples del mismo modelo, y cuál se toma como referencia»
con la **Tabla 20**, que declara los ocho grupos medidos más de una vez y por qué se descartó cada corrida.
El `.docx` tiene tablas 1 a 19.

### 4. Texto que dejó de ser cierto

§3.3 afirma en presente que «el campo de localizaciones **está vacío** en los ciento veinte». Desde que el
equipo de 48 GB aplicó las 63 localizaciones embebidas, el corpus tiene **545** en 119 de los 120 registros.
El Markdown acota la frase al alcance que le corresponde y declara la corrección con su fecha.

### 5. Las cifras inválidas retiradas

El Markdown retiró ocho cifras que procedían de mediciones inválidas —entre ellas el 11,21 de
`gemma4:12b-mlx` con KB RAG— por decisión del autor: una medición inválida no es un resultado. Comprobar que
el `.docx` no las reintroduzca al propagar.

### 6. Lo demás

La introducción ampliada, las diecinueve tablas citadas desde el texto, la retirada de negritas de frases
enteras, la alineación de §6.1 con las conclusiones y la unificación de la agregación en macro. El listado
completo son los 22 commits entre `6299d13` y la cabeza actual sobre el Markdown.

## Una nota a favor del `.docx`

En un punto **el `.docx` tenía razón y el Markdown estaba mal**: su resumen ya decía «Las instituciones
financieras» donde el Markdown decía «Las instituciones», que no concordaba con el «Financial institutions»
del abstract. La corrección de hoy alineó el Markdown con lo que el `.docx` ya decía. Conviene recordarlo al
propagar: la dirección no siempre es del Markdown hacia el Word.

## Aviso: el recuento de páginas del `.docx` no se puede leer del metadato

`docProps/app.xml` de los tres `.docx` declara **6 páginas y 1 646 palabras** en el canónico, y **1 página y
83 palabras** en los otros dos. Es falso: el texto real del canónico son **16 776 palabras**, contadas sobre
`word/document.xml`.

La causa es que Word solo actualiza ese metadato al guardar desde Word, y estos ficheros se editan con
`tools/docx_replace_terms.py`, que toca el XML sin recalcularlo. El dato que queda es el de la última vez que
alguien los abrió y guardó a mano, hace vaya usted a saber cuánto.

**Consecuencia práctica:** quien quiera comprobar el límite institucional de 25 páginas **no puede leerlo de
ahí**. Hay que abrir el documento en Word o generar el PDF y contar. La única cifra fiable disponible hoy es
la del PDF entregado: 31 páginas totales, Anexo A en la 21, cuerpo 20.

## Adenda 2026-09-08, 23:1x — cinco cambios posteriores a esta lista

Esta lista se escribió a las 18:44. Después el Markdown recibió **cinco correcciones más**, ninguna de ellas
recogida arriba. Se añaden aquí para que la propagación no se las deje: son todas de párrafo completo y
todas afectan a la solidez estadística del informe, que es lo que un tribunal mira primero.

Los textos nuevos se transcriben en la lista de abajo de forma abreviada; **la versión literal que hay que
llevar al `.docx` es siempre la del Markdown**, no la de este documento, que solo sirve para localizar el
párrafo y saber por qué cambió.

| Commit | Sección | Qué cambió |
|:---|:---|:---|
| `2f7eda0` | §5.3.1 | Párrafo **nuevo**: la correlación entre capacidad base y mejora por RAG se declara con **ambos** coeficientes, Spearman −0,5165 (p = 0,0707) y Pearson −0,6004 (p = 0,0300), y se advierte de que **discrepan en el veredicto** al 5 %. La conclusión pasa a leerse como tendencia, no como efecto demostrado |
| `d944fca` | §5.3 | Párrafo **sustituido**: donde se afirmaba que la diferencia entre las dos compilaciones de 31B «debe atribuirse a la variabilidad», ahora se precisa que el contraste **no acredita equivalencia**: con treinta artículos por grupo su potencia frente a una *d* de 0,12 es del **8 %**. Se concluye que los datos **no permiten distinguir** ambas compilaciones |
| `bbe61cb` | §5.3 | Párrafo **sustituido**: la frase sobre Levene deja de decir «se verifica la homocedasticidad» y pasa a «no detecta heterocedasticidad, lo que con 3 120 observaciones sí es informativo, aunque no equivalga a demostrar que las varianzas son iguales». Se añade que el rechazo se sostiene con **Friedman, χ² = 1 169,23** |
| `a464570` | Nota bajo la Tabla 8 | La glosa deja de decir solo que las latencias «no son comparables entre filas» y explica **por qué**: el valor es reloj de pared bajo concurrencia, **incluye la espera en cola** y no es propiedad del modelo |
| `f6765db` | §4.4 | Párrafo **sustituido**: la definición de latencia pasa a declarar que **no es tiempo de inferencia**, con la comprobación aritmética que lo demuestra —latencia × tokens/s supera el tope de salida en **veinte de los veintiséis grupos**, en un caso por veintiuna veces— y que caracteriza al régimen de ejecución, no al modelo |

**Cómo aplicarlas.** Los cinco son reemplazos de párrafo, no de término, de modo que `tools/docx_replace_terms.py`
sirve si se le pasa el párrafo entero como cadena a buscar. Ninguno toca numeración, estilos de fila ni saltos
de página, así que no hay riesgo para las correcciones manuales que el `.docx` conserva.

**Efecto en la extensión.** Los cinco suman texto: §4.4 y §5.3 crecen un párrafo largo cada una y §5.3.1 gana
uno entero. Es la razón por la que la estimación de páginas del apartado siguiente se dejó en ~24 y no en 23,
y por la que conviene contar en cuanto el `.docx` esté regenerado.

**Por qué se dejaron fuera al escribir la lista.** No se dejaron fuera: son posteriores. La lección es que un
documento de propagación fechado envejece con cada commit al Markdown, y que hay que comprobar los commits
que tocaron la fuente **después** de su última actualización antes de darlo por completo. La orden es
`git log <sha-de-este-documento>..HEAD -- <ruta-del-md>`.

## Cómo comprobar que la propagación se hizo de verdad

Medido el 2026-09-09 comparando el Markdown con el `.docx` canónico. **El recuento de palabras no sirve** para
esto —el Markdown incluye sintaxis de tablas y bloques de código, de modo que sus 22 995 palabras no son
comparables con las 16 776 del `.docx`—. Lo que sí sirve es buscar **términos que solo existen en las
correcciones pendientes**:

| Término | En el `.md` | En el `.docx` hoy | Qué corrección acredita |
|:---|---:|---:|:---|
| `Spearman` | 2 | **0** | Los dos coeficientes de correlación de §5.3.1 (`§F74`) |
| `Friedman` | 1 | **0** | El contraste de medidas repetidas de §5.3.1 (`§F75`, `§F77.bis`) |
| `reloj de pared` | 2 | **0** | La definición corregida de la latencia en §4.4 (`§F71.ter`) |
| `Corridas múltiples` | 1 | **0** | La sección nueva del Anexo I con la Tabla 20 |
| `emparejamiento` | 6 | 3 | Las precisiones sobre el umbral y el cotejo difuso |
| `potencia` | 9 | 7 | La potencia declarada de los contrastes (`§F77`) |

**Cuatro de los seis están a cero**, lo que confirma que ninguna de esas correcciones ha llegado.

**Y los tres `.docx` están en el mismo estado: 6 de 6 sin propagar en cada uno.** Eso simplifica el trabajo
más de lo que parece: no hay estados parciales que reconciliar, ni un fichero más adelantado que otro. Es una
sola tanda de correcciones aplicada tres veces, y los tres se comprueban con la misma orden cambiando el
nombre del fichero. Y da la
comprobación posterior: **tras propagar, los seis recuentos deben coincidir**. Es una orden de una línea y no
depende de contar commits, que es lo que envejece.

```sh
python3 - <<'EOF'
import zipfile, re, pathlib
md = pathlib.Path('doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md').read_text(encoding='utf-8')
dx = re.sub(r'<[^>]+>', '', zipfile.ZipFile('Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx').read('word/document.xml').decode('utf8','replace'))
for k in ('Spearman','Friedman','reloj de pared','Corridas múltiples','emparejamiento','potencia'):
    print(f'{k:20} md={md.count(k):2} docx={dx.count(k):2} {"ok" if md.count(k)==dx.count(k) else "FALTA"}')
EOF
```

## Después de propagar

1. `python3 tools/verificar_informe.py` sobre el Markdown, que debe seguir en cero fallos.
2. Recuento de páginas del PDF: el cuerpo iba en 20 de 25 y la estimación con lo añadido sube a **~24**.
3. Contar guiones largos y negritas del documento generado y compararlos con la fuente: el renderizador no
   debe añadir énfasis.

---

## Inventario corregido — 2026-09-09

Al preparar la propagación se cotejaron los tres `.docx` contra el Markdown cifra por cifra. **El inventario
de arriba está incompleto, y su apartado 1, leído literalmente, estropearía el Anexo I.** Lo que sigue lo
sustituye.

### El apartado 1 se equivoca en dos cosas

Dice que la cifra de los falsos positivos «afecta a dos puntos del `.docx`: §3.3 y §7.2, que repite la misma
cifra». Comprobado sobre el XML, son **tres** puntos, el segundo **no** es §7.2 sino el Anexo I, y **no todos
se corrigen igual**:

| Punto | El `.docx` dice | El Markdown dice | Acción |
|:---|:---|:---|:---|
| §3.3 | `el 65 % … 20 946 de 32 201, proceden de esa categoría` | `el 66,0 % … 12 852 de 19 464` | sustituir la cifra |
| Conclusiones | `de ahí procede el 65 % de los falsos positivos del estudio` | `el 66,0 %` | sustituir solo el porcentaje |
| **Anexo I** | `20946 de los 32201 … del estudio (65.0 %)` | `20 946 de los 32 201 … de estas cuarenta y dos configuraciones (65,0 %)` | **conservar las cifras**; corregir la población y añadir la glosa |

En el Anexo I **las cifras son correctas**: describen las cuarenta y dos configuraciones de esa tabla, no el
estudio. Lo que estaba mal era llamarlas «del estudio». El Markdown las conservó y añadió la glosa que
explica por qué no coinciden con el 66,0 % de §3.3. Sustituirlas ahí, como el apartado 1 sugiere, introduciría
un error donde no había ninguno — y es el incidente de 2026-09-03 otra vez: un hallazgo de auditoría tomado
por hecho.

### Lo que el inventario no recogía: tres cifras titulares obsoletas

Las tres cifras del **F1 restringido** se recalcularon después de congelar los `.docx`. La divergencia es
total y limpia: el valor viejo aparece solo en los `.docx` y el nuevo solo en el Markdown.

| Cifra | `.docx` | Markdown | Apariciones en cada `.docx` |
|:---|:---|:---|---:|
| F1 restringido, mejor local, N=120 | 76,85 % | **76,55 %** | 8 |
| F1 restringido, dominio | 90,91 % | **90,16 %** | 3 |
| F1 restringido, variante en la nube | 81,45 % | **80,42 %** | 3 |

Son **14 apariciones por documento, 42 en los tres**, y entre ellas están **el resumen y el abstract**: el
entregable anuncia en su primera página una cifra que los datos ya no sostienen. Las tres nuevas están
verificadas contra las corridas por la comprobación `c_titulares` de `tools/verificar_informe.py`; el 76,85 no
sale de ninguna agregación vigente — sobre los 113 registros del manifiesto saldría 76,78, no 76,85.

### Y la Tabla 19 no es parcheable: está entera sustituida

La fila del mejor modelo local difiere **en todas sus columnas**:

| | P | R | F1 | P restr. | F1 restr. | Δ |
|:---|---:|---:|---:|---:|---:|---:|
| `.docx` | 55.41 | 72.11 | 62.67 | 82.25 | 76.85 | +14.18 |
| Markdown | 52.89 | 72.35 | 59.25 | 80.85 | 76.55 | +17.30 |

**Por eso no se ha aplicado nada todavía.** Cambiar `76,85` por `76,55` dentro de esa fila dejaría un
`F1 restr.` que no se corresponde con el `P restr.` de su lado: una fila internamente incoherente, peor que
la que hay. La Tabla 19 entera debe reemplazarse desde el Markdown, y las catorce cifras de prosa van **en la
misma pasada** que ella, porque derivan de sus filas. Propagar solo la prosa dejaría el resumen
contradiciendo a la tabla del anexo.

### Reglas preparadas, no aplicadas

Las sustituciones de **prosa** están escritas y ancladas por contexto en `tools/terms_restringido.json`, de
modo que ninguna toca la Tabla 19. **No ejecutarlas por separado:** están ahí para lanzarse junto al
reemplazo de la tabla, que es trabajo de maquetación.

Una advertencia sobre el énfasis: en §3.3 el `.docx` tiene **toda la frase en negrita**, mientras el Markdown
resalta solo el porcentaje. Es la divergencia que la regla de sobriedad tipográfica prohíbe, y no se arregla
con reemplazo de texto porque exige partir el run del XML. Queda para la pasada de maquetación.

### Estado tras el 2026-09-09: aplicado lo independiente, pendiente lo acoplado

**Aplicado** en los tres `.docx` con `tools/docx_replace_terms.py --rules tools/terms_fp_poblacion.json
--in-place`, respaldo `*.bak_20260909-062438`:

| | Antes | Ahora |
|:---|---:|---:|
| «65 % de los falsos positivos **del estudio**» | 2 | **0** |
| 66,0 % · 12 852 | 0 | 3 · 1 |
| Anexo I: «de estas cuarenta y dos configuraciones» | 0 | 1 |
| Anexo I: conserva 20 946 / 32 201 | sí | **sí** |
| Fila de la Tabla 19 (`62.67 · 82.25 · 76.85`) | intacta | **intacta** |
| Emojis | 0 | 0 |
| Palabras | 16 776 | 16 822 (+46, todas en el Anexo) |

Los tres paquetes abren, conservan sus 29 y 15 partes, y las +46 palabras caen en un anexo, que no cuenta
para el límite de 25 páginas del cuerpo. Las tres reglas alcanzaron su cuenta exacta en los tres documentos.

**Pendiente y acoplado**, para la pasada de maquetación, en una sola tanda:

1. Reemplazar la **Tabla 19** entera desde el Markdown.
2. En la misma pasada, `tools/terms_restringido.json`: las **12** cifras de prosa del F1 restringido
   (76,85→76,55, 90,91→90,16, 81,45→80,42), resumen y abstract incluidos. Probadas en seco: las 8 reglas
   alcanzan su cuenta en los tres documentos, y **R7 requiere reparación por fragmentación de runs**, que la
   herramienta hace sola. Ninguna ancla toca la Tabla 19.
3. Las dos **figuras** y la **Tabla 20**, como decía el inventario original.
4. En §3.3, partir el run en negrita para que resalte solo el porcentaje, y añadir entonces la frase de
   alcance y la llamada a la Figura 1, que ahora no se pusieron por no existir aún la figura.

### Comparación completa de cifras — 2026-09-09, y una cuarta obsoleta

Encontradas tres cifras obsoletas a mano, quedaba por saber si eran las únicas. Ahora está mecanizado en
`tools/desfase_cifras_docx.py`, que compara **todas** las cifras decimales de los dos lados: 705 distintas
examinadas.

| | Total | En filas de tabla | Fuera de tablas |
|:---|---:|---:|---:|
| Solo en el `.docx` | 273 | 269 | **4** |
| Solo en el Markdown | 218 | 206 | 12 |

Las 269 en filas de tabla confirman el diagnóstico de arriba y lo generalizan: **las tablas de resultados no
están desfasadas en algunas celdas, están sustituidas en bloque.** Reemplazarlas desde el Markdown es la
única vía; parchear celdas no lo es.

De las cuatro de prosa, tres eran las conocidas y **la cuarta era nueva**: la columna Tok/s/B de las dos
filas de `gemma4:latest` en la **Tabla 4** decía `5.33`, y los datos dan `5.80` —media de `tokens_per_sec` en
`ablacion_n15_REMOTO`, 52,16 sobre 9 000 millones de parámetros, n=15; el 5,33 exigiría 47,97 tok/s, que no
sale de ninguna configuración—. La Tabla 4 **coincide con el Markdown en todas sus demás celdas**, así que
era parcheable. **Aplicada** con `tools/terms_tabla4_throughput.json`, respaldo `*.bak_20260909-063106`:
dos celdas a 5.80, cero a 5.33, y el `35.33%` de otra tabla intacto.

Ese `35.33%` es el aviso que conviene retener: **`5.33` estaba tres veces en el documento**, y una era parte
de otra cifra. Una regla de subcadena la habría convertido en `35.80%`. Para eso
`tools/docx_replace_terms.py` tiene ahora la opción **`celda_exacta`**, que ancla en la celda y no en el
texto; hará falta igual al reemplazar la Tabla 19, donde todas las celdas son numéricas.

**Estado de la prosa:** tras corregir el 5,33, las únicas divergencias fuera de tablas son las **tres**
acopladas a la Tabla 19 —76,85, 90,91, 81,45—, ya escritas en `tools/terms_restringido.json`. Es decir: la
pasada de maquetación tiene delante un conjunto cerrado y verificado, no una búsqueda.

---

## Gravedad máxima, por encima de todo lo anterior — 2026-09-09

**Los tres `.docx` nombran cuatro modelos excluidos en quince sitios**, mientras el Markdown tiene cero.
`nuextract` (×7), `minimax-m3` (×4), `gemini-3.1-flash-lite` (×2) y `gemma4-12b-mlx-q8-64k` (×2). Incumple
la lista cerrada de `CLAUDE.md`, que prohíbe esos nombres **incluso en una glosa que los declare excluidos**.

Cuatro sitios, y **no se corrigen igual** — el Markdown no reescribió nada, **eliminó**:

1. **Nota de la Tabla 4:** eliminar la frase «Quedan fuera de la tabla los modelos excluidos del estudio
   (…)» completa. El Markdown no la tiene.
2. **Fila «Excluidos del estudio»** de la tabla de fuentes del anexo: eliminar la fila.
3. **Tabla de deltas:** eliminar las 2 filas de `nuextract:latest_baseline` y `_kb_rag`.
4. **Tabla 19:** eliminar las **7** filas de modelos excluidos.

**El punto 4 explica el recuento que quedaba abierto:** el `.docx` tiene 49 filas de datos y el Markdown
declara 42 configuraciones, y la diferencia son exactamente esas 7. Reemplazar la Tabla 19 desde el Markdown
resuelve **las dos cosas a la vez** —las cifras sustituidas y las filas que no deben existir—, de modo que
no hay que suprimir filas a mano: se reemplaza la tabla y quedan 42.

Verificable con `python3 tools/verificar_informe.py`, cuya comprobación «sin modelos excluidos del estudio,
en el .md y en los tres .docx» examina 35 elementos y las enumera una a una. Está **declarada como pendiente
de corrección, no aceptada**, y se retira de la lista al corregirla. Detalle en `FINDINGS §F94`.
