# Caracterización de un corpus

## Prompt

> Caracterizar el corpus antes de describirlo en el informe. Medir, no suponer:
>
> - **Cuántos registros** tiene realmente cada fichero de datos.
> - **El idioma del texto**, contando marcadores léxicos, artículo por artículo y no por muestreo.
> - **El idioma de las entidades**, que es distinto del anterior y a menudo más importante.
> - **Qué categorías anota** el gold, y cuáles quedan vacías en todos los registros.
> - **La codificación**: si hay *mojibake*, medirlo por separado en la referencia y en el texto de entrada.
> - **La distribución de entidades por artículo**, contrastada con lo que el informe declara del diseño.

## Por qué el idioma de las entidades importa tanto como el del texto

> En una evaluación de reconocimiento de entidades, la lengua que importa no es solo la del texto: es la de
> las **entidades**, porque son ellas las que se segmentan y se cotejan. Un corpus puede estar redactado en un
> idioma y poblado de nombres de otro, y esa combinación cambia qué modelo gana.

En este proyecto, el corpus de quince artículos está **íntegramente en inglés**, y sin embargo un *prompt* en
español mejoraba el resultado. La explicación no era la que parecía: el corpus contiene doce personas de
nombre ibérico entre ochenta y cuatro, casi todas portuguesas y procedentes de un caso de corrupción angoleño
—`Isabel dos Santos`, `Hélder Pitta Grós`, `Mario Leite da Silva`—, con partículas y acentos cuya delimitación
es justo donde un tokenizador anglocéntrico falla. La instrucción en español no ayudaba a leer el texto:
ayudaba a **delimitar esa minoría de nombres**.

## La comprobación de la codificación, en dos criterios y no en uno

> Medir la corrupción de codificación por separado según dónde esté, porque **el signo del efecto depende del
> criterio**: por entidad de referencia corrupta y por texto de entrada corrupto.

Sobre veinticuatro configuraciones, diecinueve puntúan **mejor** cuando la referencia está corrompida —el
cotejo premia transcribir los bytes literalmente y castiga escribir el nombre bien— y diecinueve puntúan
**peor** cuando lo está el texto de entrada. Declarar solo un criterio, o mezclarlos, produce una tabla que no
se reproduce.

## Consecuencia para la redacción

Un corpus del dominio en un idioma y un corpus general en otro **no son intercambiables** para acreditar una
hipótesis. Si la hipótesis dice «en español», la cifra que la acredita tiene que venir del corpus que está en
español, aunque sea la más baja.
