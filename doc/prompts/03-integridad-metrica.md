# Integridad de la medición

## Prompt de contraste contra el código

> Contrastar contra el código fuente toda afirmación del informe sobre algoritmos, métricas, umbrales y
> parámetros: la función de emparejamiento y su umbral, la tasa de alucinación y el suyo, el controlador de
> concurrencia y sus disparadores, la cuantización, el módulo de recuperación, la agregación de métricas y la
> convención ante extracción vacía. **El código manda sobre el documento.**

## La comprobación que hay que hacer siempre, y cuesta un minuto

> Para cada categoría que el evaluador puntúe, comprobar que **existe en la anotación de referencia**. El
> indicador barato es `tp + fn` agregado por categoría: si esa suma vale cero mientras `fp` crece, la categoría
> no tiene ni una entidad de referencia en todo el corpus y está
> puntuando contra el vacío y cada acierto del modelo se cuenta como error.

En este proyecto ese defecto generaba **20 946 de 32 201 falsos positivos**, el 65 %, y sobrevivió dos meses
porque las cifras eran internamente coherentes. **Una cifra baja pero estable no acredita que la medición sea
correcta: acredita que el defecto es sistemático.**

## Otras comprobaciones que aquí destaparon defectos

> - **Varias corridas del mismo experimento.** Antes de escribir una cifra, buscar en `results/` si hay más
>   corridas de lo mismo. Si las hay, declararlas todas y explicar cuál es la de referencia y por qué. Citar
>   la más favorable sin mencionar las demás es indistinguible de seleccionar el resultado.
> - **Consistencia aritmética.** Ninguna fila puede tener F1 mayor que la media de precisión y exhaustividad.
> - **Tasa de fallo por modelo.** Cuántos registros con `parse_method='failed'` y cuántos con `recall=0`.
> - **Distinguir causas de un fallo.** Latencia cero y cero tokens es rechazo de infraestructura; latencia
>   alta con contenido vacío es que el arnés pierde la respuesta. Cruzar `parse_method` con `recall` para ver
>   si el fallback rescata contenido o encubre un fallo.
> - **Un parámetro que el proveedor descarta en silencio.** Un `think` colocado dentro de `options` en lugar
>   de como argumento de primer nivel se ignora y el modelo corre con su valor por omisión.
> - **Un presupuesto de generación agotado.** Un `num_predict` corto produce contenido vacío, que dispara el
>   fallback y acaba en extracción vacía; parece un fallo del modelo y es del arnés.
> - **Un umbral que parece estadístico y no lo es.** Comprobar en el código: uno descrito como «criterio de
>   longitud atípica» era en realidad la media más una constante fija.
> - **Doble emparejamiento.** Si el conteo de aciertos se hace por entidad extraída y las omisiones por
>   entidad de referencia, dos extracciones que casen con un mismo elemento del gold inflan la exhaustividad.
>   Se detecta buscando registros con `recall > 1.0`, pero **eso subestima la incidencia** entre tres y diez
>   veces, porque solo captura los casos que rompen el techo de la métrica.

## Cómo describir una métrica sin equivocarse

La comparación difusa de este proyecto usa `rapidfuzz.fuzz.ratio`, que es la **similitud de Indel
normalizada** multiplicada por cien: una variante de Levenshtein que solo admite inserciones y supresiones,
normalizada como `100 × (1 − d/(|a|+|b|))`. Es a nivel de **carácter**, no de token, no es distancia de
Hamming, y **es sensible al orden**: «Juan Pérez» contra «Pérez Juan» da 50, no 100. Ambas cadenas se pasan a
minúsculas antes de comparar.
