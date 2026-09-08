# Verificación del aparato bibliográfico

## Prompt de verificación completa

> Verificar el aparato bibliográfico entrada por entrada contra internet, como si nadie lo hubiera revisado
> antes. Para cada una: que la obra exista, que autores, año, publicación, volumen y páginas sean correctos, y
> que la afirmación que sostiene en el texto sea coherente con su contenido real. Comprobar la correspondencia
> en ambos sentidos: toda marca con entrada, toda entrada citada.
>
> **Abrir cada página con WebFetch**; una URL no abierta no está verificada. Prohibido inventar una URL: si no
> se encuentra fuente canónica, decirlo. Reportar los errores de metadatos sin corregirlos.

## Prompt para añadir URLs a una bibliografía que no las tiene

> El autor pide que cada entrada lleve una URL de apoyo verificada, cuando exista. Para cada entrada: buscar
> la obra, **abrir la página** y comprobar que el título, los autores, el año, el volumen y las páginas
> coinciden con lo que declara la entrada, y devolver la URL canónica. Preferencia: DOI, ACL Anthology, actas
> oficiales, arXiv, editor comercial. Para libros, la ficha del editor o el ISBN.
>
> Si una entrada corresponde a un recurso de proyecto que quizá no tenga URL pública, decirlo en lugar de
> forzar la URL de un proyecto homónimo.

## Señales que en este proyecto resultaron ser defectos reales

- **Nombres de autor genéricos** en combinación improbable (Smith, Johnson y Davis; García y López; Chang, Kim
  y Park). Tres de las cuatro citas inexistentes tenían esta forma. **Pero no basta como prueba**: hay obras
  reales con autores comunes, y hay que verificar antes de concluir.
- **Publicación sin volumen ni páginas**, o con un nombre de revista que no existe con ese título exacto
  («ACM Transactions on Intelligent Systems» es en realidad *ACM TIST*, con «and Technology»).
- **Un título que es en realidad una descripción.** El corpus del estudio se citaba como «Kleptotrace corpus:
  Financial Sanctions and Money Laundering News Corpus»; el recurso real se titula *Kleptotrace-micro-dataset*
  y tiene DOI en Zenodo.
- **Una cita correcta que sostiene una cifra que la fuente no publica.** El caso más difícil de detectar:
  FiNER existe, pero es de 2022 y no de 2023, sus autores son otros, su mejor resultado es 82,1 % y no 91 %, y
  su tarea es etiquetado numérico XBRL y no reconocimiento de personas y organizaciones.
- **Una atribución de arquitectura equivocada.** BloombergGPT figuraba como GPT-J con «85 %+»; el artículo
  declara BLOOM y reporta F1 entre 53,6 y 75,5.
- **La fuente de los datos no es la que dice el texto.** Los diccionarios se atribuían a OpenSanctions y
  provienen de la lista SDN de OFAC; OpenSanctions solo aporta el esquema FollowTheMoney.
