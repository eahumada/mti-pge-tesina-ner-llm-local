# Pregunta: ¿por qué las latencias de la re-corrida difieren tanto de las publicadas?

**Del equipo principal al equipo de 48 GB. 2026-09-08.** No bloquea nada; es para entender un dato antes de
tocar el informe.

Comparando la latencia media por artículo entre la corrida publicada y la vuestra, sobre los mismos modelos
y el mismo corpus N=120, los factores van de **×0,02 a ×2,58** y no apuntan en una sola dirección:

| Modelo | Modo | Publicada | Vuestra | Factor |
|:---|:---|---:|---:|---:|
| `gemma4:31b-mlx` | baseline | 1 066,2 s | 20,5 s | ×0,02 |
| `gemma4:12b-mlx` | baseline | 99,1 s | 4,7 s | ×0,05 |
| `gemma4:31b-mlx` | KB RAG | 1 408,5 s | 308,8 s | ×0,22 |
| `gemma4:latest` | KB RAG | 489,6 s | 790,9 s | ×1,61 |
| `gemma4:31b-cloud` | baseline | 1,2 s | 3,1 s | ×2,58 |

Hemos descartado dos explicaciones: **no es el modo de razonamiento** —los dos modelos con mayor caída lo
tienen desactivado en ambas corridas— y **no es solo la concurrencia**, porque más consumidores suben la
latencia por petición y aquí la mayoría baja.

**Actualización: no es la máquina, ya lo hemos comprobado.** Los CSV guardan memoria del sistema y VRAM
por registro, y `gemma4:31b-mlx` corrió con **30 539 MB de sistema y 26 606 de VRAM** en la publicada frente
a **30 331 y 26 720** en la vuestra. Misma máquina, misma huella, latencia 52 veces menor. Descartado.

**Corrección sobre lo que decía antes este documento.** Habíamos escrito que los aumentos ocurren solo en
modo KB RAG. No es así: con cinco modelos rehechos hay **diez pares comparables, ocho bajan y dos suben**, y
uno de los dos que suben es de modo *baseline* (`gemma4:31b-cloud`, de 1,2 a 3,1 s). Ese caso se mueve sobre
una base de uno a tres segundos dominada por el viaje de red, así que no dice nada del arnés. El otro,
`gemma4:latest` con KB RAG de 489,6 a 790,9 s, sí ocurre sobre una base grande y encaja con haber duplicado
el presupuesto de salida de 2 048 a 4 096: una respuesta que antes se truncaba ahora se completa.

**La pregunta que queda: ¿por qué bajan ocho de los diez pares, algunos hasta ×0,02?** De 1 066 a 20,5 segundos en
`gemma4:31b-mlx` y de 99 a 4,7 en `gemma4:12b-mlx`, en la misma máquina. ¿Cambió algo en cómo se mide
`latency_sec` —por ejemplo, si antes incluía la carga del modelo en un barrido que encadenaba varios y ahora
cada uno corre en su propio proceso—, o hay otra explicación que se nos escapa?

**Por qué importa.** El informe publica una tabla de eficiencia con VRAM, tokens/s y un índice por
parámetro. Si la rehacemos sobre la re-corrida, las cifras cambian mucho; si la dejamos, mezcla dos
regímenes. Antes de decidir preferimos entender el mecanismo, porque sustituir unas cifras inexplicadas por
otras no mejora nada.

El F1 no está en cuestión: la comparación de calidad entre corridas es válida y ya está verificada.

---

## Segunda pregunta, de paso: el `+10,01` frente a `+2,19` del manifiesto de contaminados

El `_comment` de `data/knowledge_base/contaminated_exemplar_articles.json` dice que el KB RAG aporta
**+10,01 pp** sobre los siete artículos contaminados frente a **+2,19 pp** sobre los ciento trece restantes.
Es la cifra que justifica la exclusión y la hemos citado en `FINDINGS §F65`.

Al recalcularla aquí sobre el consolidado publicado —promediando el Δ de cada modelo y luego entre los
trece— sale **+11,89 y +3,16**. La conclusión es la misma y hasta un poco más fuerte, así que **la decisión
de excluirlos no está en cuestión**. Pero nos gustaría poder reproducir la cifra exacta antes de que aparezca
en el informe.

**¿Con qué método la calculasteis?** Hay al menos tres formas razonables que dan números distintos: promediar
por modelo y luego entre modelos, agrupar todos los registros a la vez, o restringir a las configuraciones
`kb_combined` frente a todas. Con vuestro script o una línea explicando el criterio nos basta.
