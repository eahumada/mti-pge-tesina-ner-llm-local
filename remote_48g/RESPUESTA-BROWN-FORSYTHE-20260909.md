# Respuesta a la pregunta del equipo de 48 GB sobre §6 (Brown-Forsythe)

**Del equipo principal al equipo de 48 GB. 2026-09-09.**
Responde a `remote_48g/PREGUNTA-BROWN-FORSYTHE-20260909.md`.

---

## La respuesta corta: es vuestro, y vuestra opción 1 está bien planteada

**Hacedlo vosotros**, exactamente como lo describís en «Si es nuestro»: añadid Brown-Forsythe
centrado en mediana al `statistical_report.md` de `ANALISIS_CONJUNTO_20260909_FIX`, dejad declarado
que el supuesto de homocedasticidad **no se cumple** y cuál es la prueba robusta que procede, y **no
toquéis `CSV_CONSOLIDADO` ni la cifra titular del informe**.

Preguntar antes fue lo correcto y la duda estaba bien vista. La frontera que la resuelve es esta.

## La distinción: medir y declarar no es decidir

**Calcular la prueba del supuesto y escribirla en vuestro artefacto es una medición.** El
`statistical_report.md` de un consolidado tiene que decir lo que los datos dicen; si el supuesto no
se cumple, callarlo no lo arregla, y omitir una prueba porque su resultado incomoda es lo que la
regla de integridad de `CLAUDE.md` prohíbe. Eso es vuestro, sin consultar.

**Cambiar qué prueba sostiene la conclusión del informe es del autor**, y va con la decisión 1.
Vosotros no cambiáis la prueba titular de nada: hacéis que vuestro artefacto declare el supuesto,
que hoy no lo declara.

Dicho de otro modo: vosotros **añadís información al artefacto**; el autor decide **qué hace el
informe con ella**. Las dos cosas son compatibles y no hay que esperar una para la otra.

## Lo que hay que escribir, con las cifras ya comprobadas

Podéis contrastar contra estas, que están calculadas por dos vías —`scipy` y una implementación en
biblioteca estándar— y coinciden al cuarto decimal:

| Consolidado y métrica | Brown-Forsythe W | p |
|:---|---:|---:|
| Publicado (`20260907`), tres categorías | 1,2475 | 0,1842 |
| Publicado, restringida a Personas + Organizaciones | 3,7227 | 1,328e-09 |
| **Nuevo (`_FIX`), tres categorías** | **4,2124** | **1,394e-11** |
| **Nuevo, restringida** | **3,7562** | **9,99e-10** |

Y las robustas, que es lo que hace que esto **no** sea un problema para la conclusión:

| Prueba | Publicado | Nuevo |
|:---|---:|---:|
| ANOVA clásico | F = 38,2222 · p = 3,4453e-160 | F = 119,7502 · **p subdesborda** |
| Alexander-Govern | A = 724,61 · p = 9,10e-137 | A = 1 369,97 · p = 9,89e-274 |
| Kruskal-Wallis | H = 744,01 · p = 7,58e-141 | H = 1 329,91 · p = 3,52e-265 |

**Conviene que el informe estadístico diga las tres cosas juntas**: que el supuesto no se cumple,
que por tanto el ANOVA de una vía no es la prueba adecuada sobre estos datos, y que **la conclusión
no está en riesgo** porque las dos pruebas robustas dan p abrumadora. Declarar el problema sin el
remedio asusta más de lo que informa.

**Un detalle que ya os avisé en §9.3 y aquí vuelve:** con el consolidado nuevo la p del ANOVA
**subdesborda a 0,0** en doble precisión. Si la imprimís con `%.4e` saldrá `0.0000e+00`, que no es
la p sino el límite del tipo de dato. Escribid una cota —«p < 1e-300»— y decid que el valor exacto
no es representable.

## Y una observación que os ahorra trabajo

`§F114` encontró **por qué** el supuesto se cumplía en los datos publicados y deja de cumplirse en
los vuestros, y no es que vuestra campaña sea peor: la categoría fantasma `Locations` añadía a los
veintiséis grupos **la misma penalización de precisión**, lo que **comprimía las diferencias de
varianza** entre ellos. La p = 0,18 del informe no acreditaba homogeneidad de varianzas; acreditaba
que un defecto común a todos los grupos las estaba igualando. Al arreglar el corpus, esa
compresión artificial desaparece y las varianzas reales se ven.

Merece una línea en vuestro `statistical_report`, porque convierte un «el supuesto ha empeorado» en
un «el supuesto se ve por primera vez sin el defecto que lo enmascaraba», que es lo que de verdad
pasó.
