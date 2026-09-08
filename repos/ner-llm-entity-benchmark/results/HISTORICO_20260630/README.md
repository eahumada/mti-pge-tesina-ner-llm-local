# Corrida exploratoria del 30 de junio / 1 de julio de 2026

Rescatada el 2026-09-08. Estos dos ficheros aparecieron como duplicados con sufijo numérico —el patrón que
macOS crea al copiar sobre un directorio que ya los tiene— y, a diferencia de los otros ciento ochenta y uno,
**su contenido no estaba versionado en ninguna parte**. Se conservan por la política aditiva del proyecto.

| Fichero | Contenido |
|:---|:---|
| `benchmark_results_20260630.csv` | 45 filas, tres modelos: `llama3.1:8b`, `nemotron-mini:4b` y un tercer modelo que no forma parte del estudio final |
| `statistical_report_20260630.md` | ANOVA con **F = 65,9428** y **p = 1,1033e-13** |

## Por qué no contradicen el resultado del estudio

El ANOVA de esta corrida (F = 65,9428) es **más alto** que el definitivo (F = 38,2222 con
p = 3,4453e-160), y eso podría parecer una discrepancia. No lo es: se calculó sobre **tres modelos y 45
observaciones**, mientras el definitivo cubre trece modelos en veintiséis grupos con 3 120 observaciones. Un
estadístico F crece cuanto mayor es la separación entre grupos y cuantos menos grupos hay, de modo que las dos
cifras no son comparables. Lo que sí es comparable, y va en la misma dirección, es el veredicto: en ambos
casos las diferencias entre modelos son estadísticamente significativas.

Estos datos **no se usan en el informe**. Se archivan por trazabilidad, como el primer punto de una serie que
termina en `results/ANALISIS_CONJUNTO_20260907/`. Emplean además la convención de puntuación anterior a la
unificación del commit `7a6c19f`, de modo que sus cifras absolutas no son comparables con las publicadas.
