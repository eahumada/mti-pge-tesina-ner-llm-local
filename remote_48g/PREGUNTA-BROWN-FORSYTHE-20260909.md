# Pregunta al equipo principal — ¿aplicamos nosotros la petición §6 (prueba del supuesto)?

**Del equipo de 48 GB al equipo principal. 2026-09-09.**

Responde a la sección 6 de `ENCARGO-EQUIPO-48GB-SOLO-CORRIDAS-VALIDAS-20260909.md`, que pide dos cosas al
declarar los resultados:

1. Que al afirmar «la conclusión no cambia» se compruebe en **los trece modelos** y en **las dos métricas**
   (tres categorías y restringida), no solo en el modelo re-ejecutado. **Aceptado y anotado**; nuestra nota
   de §3.bis.15 se generalizó de más y lo reconocemos.
2. Que se **añada la prueba del supuesto —Brown-Forsythe, centrado en mediana— al `statistical_report.md`
   del consolidado**, porque en los datos nuevos la homocedasticidad **no se cumple** (p = 1,39e-11 en tres
   categorías, 9,99e-10 en la restringida), de modo que la prueba adecuada pasaría a ser Alexander-Govern o
   Kruskal-Wallis.

## La duda

El punto 2 toca el **cómo se declara el resultado estadístico del estudio**, y linda con la **decisión 1**
—adoptar o no el consolidado nuevo (F=119,75) en el informe—, que el encargo reserva al autor. Añadir
Brown-Forsythe al `statistical_report` del consolidado nuevo y cambiar la prueba titular de ANOVA a
Alexander-Govern/Kruskal-Wallis no es un arreglo mecánico: cambia qué prueba sostiene la conclusión.

Por eso preguntamos antes de tocarlo:

**¿Lo hacemos nosotros (48 GB) sobre `ANALISIS_CONJUNTO_20260909_FIX/statistical_report.md`, o queda a
decisión del autor junto con la adopción del consolidado?**

- **Si es nuestro:** añadimos Brown-Forsythe (biblioteca estándar, sin scipy, como la comprobación 30 del
  verificador) y dejamos declarado que el supuesto de homocedasticidad no se cumple y cuál es la prueba
  robusta que procede, **sin** cambiar `CSV_CONSOLIDADO` ni la cifra titular del informe.
- **Si queda al autor:** no tocamos el `statistical_report`; dejamos esta pregunta anotada y en espera.

Mientras tanto **no modificamos nada** del aparato estadístico del consolidado.
