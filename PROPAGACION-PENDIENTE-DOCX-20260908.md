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

**Cuatro de los seis están a cero**, lo que confirma que ninguna de esas correcciones ha llegado. Y da la
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
