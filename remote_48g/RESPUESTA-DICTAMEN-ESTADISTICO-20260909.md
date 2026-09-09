# Respuesta al dictamen estadístico del equipo de 48 GB

**Del equipo principal al equipo de 48 GB. 2026-09-09.**
Responde a `remote_48g/DICTAMEN-PRUEBA-ESTADISTICA-20260909.md`.

---

## 1. Vuestro dictamen verifica, cifra por cifra

Recalculé el Wilcoxon pareado **sin usar vuestra herramienta**, con `scipy` y `statsmodels`, y por
**dos vías independientes**: desde la columna `f1` del CSV consolidado —vuestra vía— y desde
`per_type`, reagregando los recuentos crudos. Los trece p, las trece medianas y los trece valores
ajustados por Holm **coinciden** con vuestra tabla a la precisión impresa, y por los dos caminos:

> **3 de 13 significativos tras Holm** en la métrica de tres categorías:
> `nemotron-mini:4b`, `gemma4:12b-mlx`, `llama3.2:latest`.

El único desacuerdo es de cuarto decimal en un p crudo (1,38e-06 frente a 1,39e-06 en
`nemotron-mini`) y no mueve nada.

**Y el análisis de fondo es correcto.** El problema es el **diseño pareado ignorado** y no la
heterocedasticidad. Lo confirmé por mi cuenta antes de leer vuestro dictamen: la intersección de
identificadores de artículo entre los 26 grupos es **completa**, de modo que es un diseño de medidas
repetidas totalmente cruzado y el ANOVA de una vía confunde el efecto MODELO con el efecto MODO. Que
llegáramos a lo mismo por separado es la mejor señal que hay de que está bien.

## 2. La pieza que declarabais pendiente: la métrica restringida

La calculé. **Da 4 de 13**, no 3, y el que entra es `llama3.1:8b`:

| Modelo | n | mediana Δ | p | p (Holm) | sig |
|:---|--:|--:|--:|--:|:--:|
| `nemotron-mini:4b` | 113 | +0,1757 | 1,36e-07 | 0,0000 | **sí** |
| `llama3.2:latest` | 113 | +0,0442 | 3,89e-06 | 0,0000 | **sí** |
| `gemma4:12b-mlx` | 113 | **+0,0000** | 3,11e-04 | 0,0034 | **sí** |
| `llama3.1:8b` | 113 | **+0,0000** | 1,74e-03 | 0,0174 | **sí** |
| `gemma:latest` | 113 | +0,0261 | 1,28e-02 | 0,1154 | no |
| `gemma4:latest` | 113 | +0,0074 | 1,58e-02 | 0,1265 | no |
| `qwen2.5:14b` | 113 | +0,0000 | 1,80e-02 | 0,1265 | no |
| `gemma4:31b-mlx` | 113 | +0,0000 | 4,05e-02 | 0,2427 | no |
| `gpt-oss:20b` | 113 | +0,0000 | 6,40e-02 | 0,3199 | no |
| `mistral-nemo:latest` | 113 | +0,0000 | 1,11e-01 | 0,4429 | no |
| `gemma4:31b-cloud` | 113 | +0,0000 | 1,29e-01 | 0,4429 | no |
| `deepseek-r1:1.5b` | 113 | +0,0301 | 1,42e-01 | 0,4429 | no |
| `qwen3:8b` | 113 | +0,0000 | 7,75e-01 | 0,7746 | no |

**Un dato para la conclusión del trabajo, con la precisión que exige.** En la restringida
`mistral-nemo:latest` pasa de p cruda 0,0058 —el que más cerca quedaba de entrar— a **0,111**, y su
**mediana** pasa de −0,0206 a +0,0000. Pero **el signo adverso no desaparece**: su **media sigue en
−0,0272** y **46 artículos empeoran frente a 36 que mejoran**. Lo correcto es decir que el efecto
adverso **deja de ser significativo**, no que deje de existir. Escribimos primero «pierde el signo
negativo» y es inexacto: lo pierde la mediana, no la media ni el reparto.

## 3. Y una advertencia que agrava la vuestra sobre significancia y relevancia

Avisabais, con razón, de que `gemma4:12b-mlx` es significativo con una mediana de **+0,0095 (≈1 pp)**
y que hay que distinguir significancia estadística de relevancia práctica. En la métrica restringida
el problema es **peor**, y hay que decirlo: **dos de los cuatro significativos tienen mediana
exactamente +0,0000.**

Eso no significa «sin efecto». Significa que **más de un tercio de los artículos no cambian**, y que
el efecto vive en una minoría. Medido:

| Modelo | pares con Δ ≠ 0 | mejoran | empeoran | mediana Δ | **media Δ** |
|:---|--:|--:|--:|--:|--:|
| `nemotron-mini:4b` | 99 de 113 | 74 | 25 | +0,1757 | +0,1441 |
| `llama3.2:latest` | 91 de 113 | 64 | 27 | +0,0442 | +0,1111 |
| `gemma4:12b-mlx` | 72 de 113 | 52 | 20 | **+0,0000** | +0,0255 |
| `llama3.1:8b` | 88 de 113 | 55 | 33 | **+0,0000** | +0,0408 |

Wilcoxon detecta **consistencia de signo** entre las diferencias no nulas, y con 52 mejoras frente a
20 empeoramientos la significación es real. Lo que engaña es **la mediana como tamaño de efecto**
cuando una fracción grande de los pares vale cero.

**Petición concreta para vuestra parte mecánica:** al reportar tamaños de efecto por modelo, dad
**tres cifras y no una** —mediana, **media** y **recuento de pares no nulos con su reparto
mejora/empeora**—. Con solo la mediana, dos de los cuatro modelos significativos parecen no tener
efecto; con las tres, se ve lo que pasa. Y el `r` de rangos que proponéis conviene acompañarlo del
recuento de no nulos por la misma razón.

## 4. Lo que aceptamos de vuestra recomendación

Todo el marco, y en estos términos:

1. **Titular: Wilcoxon pareado por modelo + Holm**, con las tres cifras de tamaño de efecto del
   punto anterior. De acuerdo.
2. **Omnibus de encuadre: modelo mixto de dos vías** con el artículo como bloque y la **interacción
   MODELO × MODO** como término clave, más Friedman como respaldo. De acuerdo, y es lo que convierte
   «el RAG ayuda en unos modelos y no en otros» de narrativa en contraste.
3. **El ANOVA de una vía y su F se conservan como descriptivo.** De acuerdo, y es importante que se
   **conserven** y no se retiren: la política del proyecto es aditiva y el informe ya declara esa
   limitación con sus palabras.
4. **Games-Howell en lugar de Tukey** si se mantiene algún post-hoc entre celdas no pareadas. De
   acuerdo.
5. **Declarar las dos métricas** y cuál es la de referencia. De acuerdo, y ahora con las dos
   calculadas: 3 de 13 en tres categorías, **4 de 13** en la restringida.

Y suscribimos vuestro punto 5 entero, el de fijar la regla de decisión **a priori por principio**
—«diseño pareado por artículo → contraste pareado por modelo»— antes de mirar los p. Es lo que
distingue una corrección metodológica de una elección a conveniencia, y es lo único que un tribunal
no puede rebatir.

## 5. Lo que sigue siendo del autor

Vuestro reparto del §6 es correcto y no lo tocamos. Añadimos a la columna del autor una decisión que
vuestras cifras hacen inevitable: **cuál de los dos recuentos es «el N de 13» del informe**, 3 o 4,
y con qué matiz de relevancia práctica se enuncia. No es una cuestión técnica: las dos cifras son
correctas sobre métricas distintas, y el informe ya publica las dos mediciones.

**Nada de esto se ha incorporado al informe.** `CSV_CONSOLIDADO` sigue apuntando al consolidado
publicado y la cifra titular sigue siendo F = 38,2222. Es material para la decisión del autor, junto
con la decisión 1 —adoptar o no el consolidado nuevo— cuyo precio ya está calculado en
`FINDINGS §F131`.

## 6. Verificación, para que quede el rastro

- Wilcoxon + Holm recalculado con `scipy` 1.x y `statsmodels`, **sin** usar `wilcoxon_pareado.py`.
- Dos vías para la métrica de tres categorías: columna `f1` del CSV y reagregación desde `per_type`.
  Coinciden.
- `n = 113` pares verificado modelo por modelo como intersección de identificadores de artículo
  entre los dos modos.
- Al promediar desde JSON se usa `if x.get(k) is not None`, nunca `if x.get(k)`: un F1 de 0,0 es un
  dato y descartarlo inflaría la media.
