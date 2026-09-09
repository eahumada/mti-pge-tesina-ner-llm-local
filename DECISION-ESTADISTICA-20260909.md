# La decisión estadística, reunida en un sitio

**2026-09-09.** Todo lo que hay que saber para decidir qué prueba sostiene la conclusión del
trabajo, con las cifras verificadas y sin tener que reconstruirlo de seis documentos.

Se escribe porque el material está repartido entre `FINDINGS §F131`, `§F137`, `§F138`, el dictamen
del equipo de 48 GB, la respuesta a ese dictamen, y la decisión 1 de
`DECISIONES-PENDIENTES-20260908.md`. Ninguno de los seis es decidible por sí solo.

**Nada de esto está en el informe.** `CSV_CONSOLIDADO` sigue apuntando al consolidado publicado, la
cifra titular sigue siendo F = 38,2222 y las palabras «Wilcoxon» y «Holm» aparecen **cero veces** en
el Markdown y en los tres `.docx`.

---

## 1. El diagnóstico, en el que dos equipos coinciden por separado

**El defecto atacable no es la heterocedasticidad: es el diseño pareado ignorado.**

Los mismos artículos se evalúan en los 26 grupos —comprobado por intersección de identificadores,
que es completa—, y dentro de cada modelo la línea base y el KB RAG se miden sobre los mismos
artículos. Es un diseño de **medidas repetidas totalmente cruzado**. El ANOVA de una vía que el
informe publica trata esos registros como independientes y **confunde el efecto MODELO con el efecto
MODO**: su F dice «las 26 celdas no son todas iguales», dominado trivialmente por el factor modelo, y
**no aísla el efecto del RAG**, que es la pregunta del estudio.

El equipo de 48 GB llegó a esa conclusión con su propio comité; este equipo la había confirmado por
su cuenta al preparar otro encargo. Convergencia independiente.

**Y la heterocedasticidad no manda, por tres razones que sí se sostienen en una defensa:** el diseño
está **balanceado** —n idéntico en los 26 grupos, y también a nivel de entidad—, lo que hace robusto
el F de Fisher; con N = 2 938 Levene está **sobre-potenciado** y marca diferencias irrelevantes; y el
defecto real es otro. **No vale decir «no aplica porque es un problema de clasificación»**: ese
ANOVA se calcula sobre una respuesta continua, el F1 por artículo, y a ella se le aplican los
supuestos del modelo. Ese argumento es rebatible en una frase; los tres anteriores no.

## 2. Las cifras, todas verificadas por dos vías

Recalculadas con `scipy` y con implementación en biblioteca estándar, y para el contraste pareado
también desde `per_type` además del CSV. Reproducible con `tools/contraste_pareado.py`.

### Omnibus

| Consolidado y métrica | ANOVA una vía | Brown-Forsythe | Friedman (bloques) |
|:---|---:|---:|---:|
| Publicado, 3 categorías | F = 38,2222 · p = 3,445e-160 | W = 1,2475 · p = 0,1842 | χ² = 1 169,2327 |
| Publicado, restringida | F = 70,2802 | W = 3,7227 · p = 1,33e-09 | — |
| Nuevo, 3 categorías | F = 119,7502 · **p subdesborda** | W = 4,2124 · p = 1,394e-11 | χ² = 1 802,3671 |
| Nuevo, restringida | F = 79,6730 | W = 3,7562 · p = 9,99e-10 | — |

η² = **0,2360** en el publicado y **0,5069** en el nuevo. **El informe no lo publica**, y las guías
de reporte lo piden junto al valor p.

### Contraste pareado por modelo, Wilcoxon + Holm

| Métrica | Significativos | Cuáles |
|:---|---:|:---|
| Tres categorías | **3 de 13** | `nemotron-mini:4b`, `gemma4:12b-mlx`, `llama3.2:latest` |
| Restringida | **4 de 13** | los tres anteriores más `llama3.1:8b` |

**Y el aviso que hay que llevarse:** en la métrica restringida **dos de los cuatro tienen mediana
exactamente +0,0000**. No es ausencia de efecto —`gemma4:12b-mlx` mejora en 52 artículos y empeora
en 20 de sus 72 pares no nulos, media +0,0255— sino **efecto concentrado en una minoría**. Con solo
la mediana parecerían no tener efecto: hacen falta **tres cifras**, mediana, media y reparto.

## 3. Las tres decisiones, y son distintas

### Decisión A — ¿Se cambia la prueba titular?

**Recomendación: no, para aprobar.** El informe **ya declara la limitación** con sus palabras: «los
veintiséis grupos evalúan los mismos 120 artículos, de modo que las observaciones están apareadas y
un modelo de medidas repetidas sería el procedimiento estrictamente correcto», y **la salva con
Friedman**, que es la prueba de bloques que corresponde. Esa salvaguarda existe y está publicada.

Lo que un tribunal competente puede objetar es que la prueba **titular** siga siendo el ANOVA de una
vía teniendo la de bloques ya calculada. La respuesta preparada es que Friedman se reporta y
converge. Es defendible.

**Lo que sí conviene hacer, y es barato:** publicar el **η²** que ya está calculado. Es una cifra,
una frase, y cierra una objeción estándar de las guías de reporte.

### Decisión B — El Wilcoxon pareado: fuera del estudio, a trabajo futuro

**Decidido por el autor el 2026-09-09.** El contraste pareado por modelo es metodológicamente
superior, pero es una rama de análisis excesivamente detallada para este punto del cierre y su
resultado **no cambia la conclusión**: los dos modelos del informe siguen entre los significativos en
las dos métricas.

**Confirmado que no hay nada que retirar:** «Wilcoxon» y «Holm» aparecen **cero veces** en el
Markdown y en los tres `.docx`. No es un borrado —la política del proyecto es aditiva y esto nunca se
incorporó—: es una **decisión de alcance**.

**Queda como trabajo futuro**, y con el material ya hecho para que quien lo retome no empiece de
cero: `tools/contraste_pareado.py` lo calcula en las dos métricas, el dictamen del equipo lleva sus
fuentes bibliográficas, y `§F137` la verificación independiente.

> **Pendiente concreto, y no es de este documento:** añadir el punto correspondiente a la lista de
> trabajo futuro de §7 del informe. Toca el Markdown canónico, y hoy hay workflows leyéndolo; lo
> hace quien edite el `.md` a continuación. El texto sugerido: replicar el análisis con un contraste
> pareado por modelo, que es el que corresponde al diseño, declarando las dos métricas y los tamaños
> de efecto con mediana, media y reparto.

### Decisión C — El modelo logístico con test de Wald: trabajo futuro, y consta que se puede

**Es factible**, y ahora está medido. `metrics.per_entity` existe en los **2 938 de 2 938**
registros, con el veredicto y las cadenas entidad por entidad:

| | |
|:---|---:|
| Eventos de clasificación | **56 496** |
| Con entidad de referencia (`tp` + `fn`) | **47 216** |
| Por grupo | **1 816, idéntico en los 26** |

Permitiría una regresión logística de efectos mixtos con el artículo como efecto aleatorio y un
**test de Wald sobre la interacción MODELO × MODO**, que es literalmente «el RAG ayuda en unos
modelos y no en otros».

**Y la salvedad que lo manda a trabajo futuro:** los `fp` no tienen entidad de referencia, de modo
que ese modelo mide **exhaustividad y no F1**. Es más limpio estadísticamente y responde una pregunta
**más estrecha**; adoptarlo exigiría reenunciar el capítulo de resultados. Llega tarde para el
calendario.

## 4. Lo que queda abierto y es tuyo

| # | Decisión | Estado |
|:--|:---|:---|
| A | ¿Se publica el η² ya calculado? | **abierta**, y es barata: una cifra y una frase |
| B | Wilcoxon fuera del estudio, a trabajo futuro | **decidida**; falta el punto en §7 del `.md` |
| C | Modelo logístico con Wald | **decidida**: trabajo futuro, con el dato acreditado |
| D | ¿Se adopta el consolidado nuevo? | **abierta** — es la decisión 1, con su precio en `§F131` |
| E | ¿Cuál es «el N de 13», 3 o 4? | **abierta** — solo si se adopta el marco pareado, o sea probablemente **no aplica** dado B |

**La E se cae con la B**, y conviene notarlo: si el Wilcoxon queda fuera del estudio, no hay «N de
13» que elegir. El informe sigue con sus **dos** modelos significativos por Tukey, que es lo que
publica hoy y lo que las dos métricas del contraste pareado confirman como núcleo.

## 5. Trazabilidad

- Diagnóstico y dictamen del equipo: `remote_48g/DICTAMEN-PRUEBA-ESTADISTICA-20260909.md`
- Verificación independiente y métrica restringida: `FINDINGS §F137`, y la respuesta en
  `remote_48g/RESPUESTA-DICTAMEN-ESTADISTICO-20260909.md`
- Wald, η² y el dato a nivel de entidad: `FINDINGS §F138`
- Precio de adoptar el consolidado nuevo: `FINDINGS §F131` y `tools/ensayo_adopcion.py`
- Herramienta que recalcula el contraste: `tools/contraste_pareado.py`
- Un comité revisor con investigación web está en marcha (`wf_6f71302e-12d`); su dictamen se añadirá
  aquí cuando cierre, y **puede contradecir algo de lo anterior**, que es para lo que se lanzó.
