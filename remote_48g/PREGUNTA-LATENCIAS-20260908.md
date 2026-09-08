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

**La pregunta concreta:** ¿en qué máquina se ejecutaron las corridas publicadas de `gemma4:31b-mlx` y
`gemma4:12b-mlx` sobre N=120? Si fueron en el equipo de 16 GB, con paginación a disco, eso explicaría las
caídas grandes. Y si es así, ¿se os ocurre por qué `gemma4:latest` con KB RAG **sube** un 61 % en lugar de
bajar?

**Por qué importa.** El informe publica una tabla de eficiencia con VRAM, tokens/s y un índice por
parámetro. Si la rehacemos sobre la re-corrida, las cifras cambian mucho; si la dejamos, mezcla dos
regímenes. Antes de decidir preferimos entender el mecanismo, porque sustituir unas cifras inexplicadas por
otras no mejora nada.

El F1 no está en cuestión: la comparación de calidad entre corridas es válida y ya está verificada.
