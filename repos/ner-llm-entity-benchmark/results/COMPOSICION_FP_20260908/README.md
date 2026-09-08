# Composición de los falsos positivos del estudio publicado (26 grupos)

**2026-09-08.** Calculado desde los `detailed_results.json`, **sin reejecutar inferencia**.

Cubre los **26 grupos** —trece modelos en sus dos modos— que sostienen la Tabla 7 del informe, tomando para
cada uno la corrida que el consolidado `ANALISIS_CONJUNTO_20260907` usa realmente. Los 26 quedan cubiertos;
ninguno se omite en silencio.

| Categoría | Falsos positivos | Aciertos | Omisiones | tp + fn |
|:---|---:|---:|---:|---:|
| Locations | **12 852** | 0 | 0 | **0** |
| Organizations | 5 132 | 10 479 | 10 822 | 21 301 |
| Persons | 1 480 | 9 880 | 5 784 | 15 664 |
| **Total** | **19 464** | | | |

**12 852 de 19 464 falsos positivos, el 66,0 %, proceden de las localizaciones**, categoría cuyo `tp + fn`
agregado vale **cero**: no había ni una entidad de referencia en todo el corpus, de modo que ningún modelo
podía acertar en ella. Es el indicador de `FINDINGS §F53`.

## Por qué existe este artefacto

El informe daba **dos cifras distintas** para esta misma magnitud: 19 178 de 28 404 (67,5 %) en §3.3, §7.2 y
la leyenda de la Figura 1, y 20 946 de 32 201 (65,0 %) en el Anexo I. Ninguna de las dos describe el estudio
publicado:

- El **65,0 %** procede de `results/CORRECCION_LOCATIONS_20260908`, que cubre **42 configuraciones** e
  incluye corridas después declaradas inválidas —entre ellas `gemma4:12b-mlx_kb_rag` con F1 14,60, la que el
  modo de razonamiento arruinó—. Es correcto para lo que dice medir, pero no es «el estudio».
- El **67,5 %** no aparece en ningún artefacto de datos del repositorio. No se ha podido reproducir.

Este fichero fija la cifra que corresponde al estudio publicado y la deja trazable, con el desglose por grupo
en `composicion_fp_26_grupos.json`.
