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

## Después de propagar

1. `python3 tools/verificar_informe.py` sobre el Markdown, que debe seguir en cero fallos.
2. Recuento de páginas del PDF: el cuerpo iba en 20 de 25 y la estimación con lo añadido sube a **~24**.
3. Contar guiones largos y negritas del documento generado y compararlos con la fuente: el renderizador no
   debe añadir énfasis.
