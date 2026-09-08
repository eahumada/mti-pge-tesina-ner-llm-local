# Monitoreo de un equipo remoto y verificación de sus entregas

## Prompt de monitoreo

> **Paso 1.** Cargar el entorno con las credenciales y hacer `git pull`. Si no hay commits nuevos, reportarlo
> en una línea y terminar.
>
> **Paso 2.** Analizar las novedades aplicando **siempre** estas verificaciones antes de aceptar cualquier
> cifra:
>
> 1. **Tasa de fallo por modelo:** cuántos registros con `parse_method='failed'` y cuántos con `recall=0`.
> 2. **Protocolo:** que `run_config.json` use el modo de recuperación correcto y que los parámetros coincidan
>    con la corrida de referencia.
> 3. **Consistencia aritmética:** ninguna fila puede tener F1 mayor que la media de precisión y exhaustividad.
> 4. **Al promediar desde JSON, usar `if x.get('k') is not None` y nunca `if x.get('k')`**, porque `0.0` es
>    falsy y descartaría las filas en cero, inflando la media.
> 5. **Distinguir causas:** latencia cero y cero tokens es rechazo de infraestructura; latencia alta con
>    contenido vacío es que el arnés pierde la respuesta. Cruzar `parse_method` con `recall` para ver si el
>    fallback rescata contenido o encubre un fallo.
>
> **Paso 3.** Entregar el avance en tres bloques: lo realizado, con cifras verificadas y si pasan los
> criterios; el estado global, con cuántos modelos válidos tiene ya el estudio y si conviene rehacer el
> análisis conjunto; y las tareas por realizar, distinguiendo lo que falta del equipo remoto de lo que espera
> una decisión del autor.

## Por qué verificar antes de aceptar

Un diagnóstico propio resultó equivocado en este proyecto: se atribuyó a un modelo una degeneración por bucle
de repetición a partir de dos muestras de registro, y el equipo remoto reprodujo el caso cero veces de cinco
e identificó la causa real, que era un presupuesto de generación agotado. **La conclusión de un agente sobre
un fallo ajeno es una hipótesis hasta que alguien la reproduce.**

## Aviso obligatorio si se reescribe el historial

Si se purga un secreto del historial con `filter-repo` y se hace `--force`, **avisar al equipo remoto de que
sus clones quedan incompatibles** y tienen que volver a clonar. Un `pull` les fallará sin explicación útil.
