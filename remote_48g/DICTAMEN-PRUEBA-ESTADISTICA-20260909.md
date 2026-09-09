# Dictamen — qué prueba debe sostener la conclusión titular (heterocedasticidad y diseño pareado)

**Del equipo de 48 GB al equipo principal. 2026-09-09.** Responde a `PREGUNTA-BROWN-FORSYTHE-20260909.md`.
**Método:** workflow de investigación en internet + panel de comité (revisor bioestadístico, metodólogo de
evaluación de LLMs, tribunal de tesis) + síntesis de profesor guía. La recomendación fue **unánime**.
**Esto es una recomendación documentada; la decisión final es del autor / equipo principal.**

## 1. El problema que planteábamos no es el problema de fondo

Preguntábamos si sustituir el ANOVA por Alexander-Govern / Kruskal-Wallis o solo añadir Brown-Forsythe. El
comité es unánime: **ninguna de las dos.** El defecto atacable en una defensa **no es la heterocedasticidad,
es el diseño pareado ignorado.**

El ANOVA de una vía sobre las 26 celdas trata como **independientes** registros que están **pareados** por
artículo (baseline y kb_rag se miden sobre los mismos 113 artículos dentro de cada modelo) y **confunde el
efecto MODELO con el efecto MODO**. Su F=119,75 solo dice «las 26 celdas no son todas iguales», dominado
trivialmente por el factor modelo; **no aísla el efecto del RAG**, que es la pregunta del estudio. Cambiarlo a
Welch/Alexander-Govern/Kruskal-Wallis corrige un síntoma (varianzas) y deja intacto el error de fondo, porque
todas son pruebas de una vía que también ignoran el emparejamiento.

## 2. Sobre la heterocedasticidad (la pregunta original)

- Con **diseño balanceado** (n=113 idéntico en los 26 grupos) el F de Fisher es **robusto** a la
  heterogeneidad de varianzas: el caso problemático es heterocedasticidad **más** desbalance, que aquí no se
  da (Blanca et al. 2018; regla clásica de Box del ratio de varianzas 3-4 en diseño balanceado).
- Con **N grande** (2938 por métrica) Levene/Brown-Forsythe es **sobre-potente**: marca como significativas
  diferencias de varianza prácticamente irrelevantes (arXiv 1010.0308). p=1,39e-11 no justifica por sí sola
  descartar el F.
- La heterocedasticidad es además **sustantiva y esperable**: los modelos débiles dan F1 baja y muy variable,
  los fuertes F1 alta y estable. Es el propio fenómeno que el estudio describe, no un defecto.

Conclusión de este punto: **la heterocedasticidad se declara como hallazgo, no obliga a cambiar la prueba.**

## 3. Recomendación unánime del comité

1. **Titular = Wilcoxon signed-rank PAREADO por modelo** sobre F1(kb_rag) − F1(baseline) de los 113 artículos:
   13 contrastes, corrección de **Holm**, con **tamaño de efecto pareado** (mediana de la diferencia con IC, o
   r de rangos) por modelo. El recuento de rechazos tras Holm **es** literalmente el «N de 13». Cada contraste
   usa solo las diferencias de un modelo, de modo que la heterogeneidad de varianzas **entre** modelos es
   irrelevante para su validez, y F1 por artículo no es normal (por eso Wilcoxon y no t pareada).
2. **Omnibus de encuadre = modelo mixto de dos vías** (artículo como bloque/efecto aleatorio; MODELO y MODO
   fijos) cuyo término clave es la **interacción MODELO × MODO** —exactamente «el RAG ayuda en unos modelos y
   no en otros»—; **Friedman** como respaldo no paramétrico de bloques.
3. El **ANOVA de una vía y su F=119,75 se conservan solo como descriptivo** de heterogeneidad global. Si se
   quiere un omnibus robusto de una vía, **Welch** se reporta como referencia **convergente**, nunca titular.
4. Si se conservan post-hoc entre celdas no pareadas, **Games-Howell**, no Tukey HSD (que asume la
   homocedasticidad ya refutada).

## 4. Evidencia mecánica que aportamos (parte 48 GB, ya calculada)

Ejecutado el Wilcoxon pareado por modelo + Holm sobre `ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv`
(métrica de tres categorías). Reproducible: `tools/wilcoxon_pareado.py`. Los 13 p crudos y ajustados quedan
visibles; **no se eliminó ninguna fila.**

| Modelo | n | mediana Δ (RAG−base) | p | p (Holm) | sig |
|:---|--:|--:|--:|--:|:--:|
| nemotron-mini:4b | 113 | +0,1538 | 1,39e-06 | 0,0000 | sí |
| gemma4:12b-mlx | 113 | +0,0095 | 4,33e-05 | 0,0005 | sí |
| llama3.2:latest | 113 | +0,0507 | 9,94e-05 | 0,0011 | sí |
| mistral-nemo:latest | 113 | −0,0206 | 5,77e-03 | 0,0577 | no |
| gemma4:latest | 113 | +0,0138 | 6,61e-03 | 0,0595 | no |
| gpt-oss:20b | 113 | +0,0030 | 1,55e-02 | 0,1236 | no |
| gemma4:31b-mlx | 113 | +0,0000 | 2,87e-02 | 0,2010 | no |
| gemma4:31b-cloud | 113 | +0,0000 | 1,00e-01 | 0,5999 | no |
| llama3.1:8b | 113 | +0,0000 | 1,79e-01 | 0,8971 | no |
| qwen2.5:14b | 113 | +0,0000 | 2,76e-01 | 1,0000 | no |
| gemma:latest | 113 | +0,0061 | 3,55e-01 | 1,0000 | no |
| deepseek-r1:1.5b | 113 | +0,0268 | 4,84e-01 | 1,0000 | no |
| qwen3:8b | 113 | −0,0021 | 6,95e-01 | 1,0000 | no |

**Resultado: 3 de 13 significativos** tras Holm en la métrica de tres categorías, no 2. Se añade
`gemma4:12b-mlx`. **Aviso importante:** su mediana Δ es **+0,0095 (≈1 pp)** —significativa por consistencia de
signo entre los 113 artículos pareados, pero **prácticamente diminuta**—, de modo que la lectura correcta
distingue *significancia estadística* de *relevancia práctica*. Falta correr lo mismo sobre la **métrica
restringida** (personas+organizaciones) antes de fijar el «N de 13»: el comité insiste en declarar **ambas
métricas**.

## 5. Cómo declararlo (para no parecer elección a conveniencia)

Fijar y firmar la **regla de decisión a priori por principio** —«diseño pareado por artículo → contraste
pareado por modelo»— antes de mirar los p. Declarar Brown-Forsythe con su p y el **ratio de varianzas
observado**. Reportar **todas** las pruebas corridas (ANOVA clásico, Welch, Kruskal-Wallis, Friedman,
Tukey/Games-Howell, Holm, Wilcoxon) y su convergencia. Declarar las **dos métricas** y cuál es la de
referencia. **No** presentar N=2938 como si diera independencia: el n efectivo del contraste RAG es 113 por
modelo.

## 6. Reparto 48 GB vs autor

- **48 GB (mecánico, sin juicio de fondo):** matriz de diferencias verificando los mismos 113 pareados
  (hecho); 13 Wilcoxon + Holm (hecho, arriba); tamaños de efecto por modelo; modelo mixto 2 vías + Friedman;
  Brown-Forsythe + ratio de varianzas en ambas métricas; tabla de convergencia; **lo mismo sobre la métrica
  restringida**. Todo auditable, con backup, sin borrar filas.
- **Reservado al AUTOR (no delegable):** firmar la regla de decisión a priori; confirmar la dirección e
  interpretación del efecto (que sea mejora real, no artefacto de cola), en especial el `gemma4:12b-mlx` de
  +0,95 pp; decidir métrica y corrida de referencia declarando las demás; redactar la narrativa titular;
  validar antes de incorporar al informe. **Y decidir si se adopta este marco** en lugar del ANOVA titular.

## 7. ¿Sobrevive la conclusión?

**Sí.** El comité es unánime: la conclusión del trabajo (el RAG mejora en los modelos débiles, con efecto
mayor cuanto más débil el modelo) se sostiene bajo la prueba correcta; lo que cambia es el aparato que la
sostiene y, en la métrica de tres categorías, el recuento pasa de 2 a **3** con el matiz de que el tercero es
de magnitud práctica muy pequeña. **No tocamos `CSV_CONSOLIDADO` ni la cifra del informe**: esto es una
recomendación para vuestra decisión.

## Fuentes principales

- Blanca et al. (2018), *Effect of variance ratio on ANOVA robustness*, Behavior Research Methods — https://link.springer.com/article/10.3758/s13428-017-0918-2
- Delacre, Leys, Mora & Lakens (2019), *Taking Parametric Assumptions Seriously* (Welch por defecto), RIPS — https://rips-irsp.com/articles/10.5334/irsp.198
- *The Impact of Levene's Test…* (N grande y significancia trivial), arXiv 1010.0308 — https://arxiv.org/pdf/1010.0308
- Kruskal–Wallis test (dominancia estocástica, no medianas), Wikipedia — https://en.wikipedia.org/wiki/Kruskal%E2%80%93Wallis_test
- The Analysis Factor, *When Unequal Sample Sizes Are and Are NOT a Problem in ANOVA* — https://www.theanalysisfactor.com/when-unequal-sample-sizes-are-and-are-not-a-problem-in-anova/
