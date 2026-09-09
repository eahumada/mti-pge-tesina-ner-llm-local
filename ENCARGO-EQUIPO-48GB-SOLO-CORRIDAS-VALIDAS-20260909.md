# Encargo al equipo de 48 GB — el estudio se queda solo con corridas válidas

**Fecha:** 2026-09-09 · **Autoriza:** el autor · **Rama de trabajo:** `main`

---

## 0. Antes de nada: lo que ya habéis hecho, y desbloqueó lo más importante del cierre

Vuestro commit `3716790` entregó **`§3.bis.16`**: los `detailed_results.json` de las trece corridas
de `recorrida_20260908`. Comprobado: **13 de 13** corridas N=120 los traen.

Eso no era un volcado de ficheros más. Era **la única cosa que faltaba para decidir si el informe
adopta el consolidado nuevo**, y con ellos se pudo calcular la respuesta el mismo día.

El asunto era este. El informe concluye que **dos** de los trece modelos mejoran de forma
significativa con KB RAG. Sobre el consolidado nuevo, medido en las **tres** categorías,
`llama3.2:latest` **pierde** la significación y la conclusión se quedaría en uno. Pero el informe
publica también una **medición restringida** a las categorías que el corpus anota de verdad
—personas y organizaciones—, y esa métrica solo se puede calcular desde `per_type`, que es lo que
vosotros acabáis de entregar. Resultado:

| Métrica | Modelos significativos |
|:---|:---|
| Publicado (N=120, tres categorías) | `llama3.2:latest`, `nemotron-mini:4b` |
| Campaña nueva, tres categorías | solo `nemotron-mini:4b` |
| **Campaña nueva, restringida** | **`llama3.2:latest` (+0,1111, p = 0,0075) y `nemotron-mini:4b` (+0,1441, p = 0,0000)** |

**La conclusión del trabajo sobrevive**, y la pérdida en la métrica de tres categorías era un
artefacto de la categoría fantasma —`Locations`— que vuestra campaña arregla: al pasar de aportar
solo falsos positivos a aportar aciertos reales, comprime las diferencias entre modos. Sin vuestros
ficheros esto no se podía saber, solo suponer.

También retirasteis `nemotron-mini_4b__N120_F85_BUGGY`. Eso coincide con la instrucción que el autor
acaba de dar y no hay que revertirlo. Para vuestra tranquilidad: el diagnóstico que ese log
sostenía —los 58 mensajes del `TypeError`, los 18 registros con `parse_method='failed'`, los 18 con
latencia 0 y 0 tokens— está escrito con sus cifras en `FINDINGS §F85`, `§F108` y `§F113`, de modo que
la prueba sobrevive como registro aunque el fichero ya no esté.

---

## 1. La instrucción del autor

> **En el estudio deben existir solo corridas y *benchmarks* exitosos. Quedarse con las últimas
> versiones correctas. No conservar nada defectuoso.**

Aplicada a lo que hay hoy, eso deja **una sola cosa por resolver** y dos por retirar.

---

## 2. Lo único que de verdad hay que resolver: `benchmark_n120_REMOTO`

Es **la única corrida con fallos que alimenta un consolidado del estudio**, y alimenta el
**publicado**:

| Corrida | `parse_method='failed'` | Papel |
|:---|---:|:---|
| `benchmark_n120_REMOTO` | **8 de 1 440** | **fuente del consolidado publicado** (`ANALISIS_CONJUNTO_20260907`) |
| `benchmark_balanced_120_20260824_173036` | 197 de 2 640 | no alimenta ningún consolidado |
| `nemotron_fix7_REMOTO` | 7 de 14 | no alimenta ningún consolidado |

Las dos últimas no son del estudio y no hay nada que hacer con ellas más allá de no incorporarlas.
La primera sí, y hay que decidirlo con criterio, **no borrando**:

**Qué hacer, por orden.**

1. **Identificar los 8 registros** y decir a qué modelo y a qué configuración pertenecen. Con
   `grep 'Failed to parse JSON from raw response:' results/benchmark_n120_REMOTO/benchmark.log`
   sale la causa de cada uno; ese `grep` ya resolvió los diagnósticos de `nemotron-mini` y de
   `gemma4:12b-mlx`, así que es el primer sitio donde mirar.
2. **Comprobar si esos 8 grupos tienen ya una medición válida** en `recorrida_20260908`, que es la
   campaña completa y la que no arrastra el defecto. Si la tienen —y probablemente la tengan, porque
   la campaña cubre los trece modelos—, **no hay que re-ejecutar nada**: el consolidado nuevo ya es
   la versión correcta y la instrucción se cumple adoptándolo.
3. **Si algún grupo no la tiene**, re-ejecutar **solo ese grupo**, con el código ya arreglado, y
   comprobar antes de declararla válida: `failed == 0` **y** ninguna fila con latencia 0 y 0 tokens
   con el campo de contenido vacío. Las dos cosas, no una.
4. **Rehacer el consolidado después**, nunca antes.

**No re-ejecutéis la campaña entera.** Son 8 registros de 1 440, y el alcance comprobado es el que
digo arriba: los grupos concretos a los que pertenezcan esos 8.

---

## 3. Lo que hay que retirar del estudio

**`ANALISIS_CONJUNTO_20260909`**, el consolidado intermedio. Lo dice su propio sucesor en
`ANALISIS_CONJUNTO_20260909_FIX/NOTA-FIX-F85.md`: «este consolidado **sustituye** a
`ANALISIS_CONJUNTO_20260909/`, que incluía la corrida *buggy* de `nemotron-mini:4b` baseline con 18
filas `parse_method='failed'`». Incluía la corrida defectuosa, ya está sustituido, y su F de 121,56
no debe aparecer en ningún sitio como cifra del estudio: la del consolidado nuevo es **119,7502**.

Retiradlo del estudio y **decidlo en el `RUNS_INDEX.md`**, para que quien lo busque sepa por qué no
está y cuál lo sustituye. Un directorio que desaparece sin nota deja a la siguiente persona
preguntándose si se perdió algo.

---

## 4. Qué NO hay que tocar, y por qué os lo digo

Esto no es una excepción a la instrucción del autor: es su alcance.

- **Los `benchmark.log` de las corridas que sí son del estudio.** Una corrida válida no deja de
  serlo porque su log mencione un error recuperado. Los logs de corridas válidas se conservan
  íntegros, sin editar líneas: son la prueba de qué se ejecutó, y este proyecto ya los ha necesitado
  dos veces para diagnosticar.
- **`results/RUNS_INDEX.md` y los `WORKLOG.md`.** Son el catálogo y el registro. Ahí las corridas
  retiradas **se anotan como retiradas**; no se borra su línea.
- **El commit `df9b4c4`.** La comprobación 50 del verificador ata la Tabla 17 del informe a la
  versión del corpus **anterior** a la corrección del *mojibake*, porque el corpus actual ya no
  tiene el defecto y esa tabla mide el estado anterior. Es historia de git y no un fichero de
  trabajo, así que nada de lo de arriba la afecta; solo que no reescribáis historia.

---

## 5. Criterio de aceptación, y es gratuito

Al terminar, desde la raíz del repositorio:

```
python3 tools/verificar_informe.py
python3 tools/verificar_corrida.py <directorio de la corrida>
```

El primero devuelve 0 si no hay fallos **nuevos**. Fijaos en dos comprobaciones concretas:

- **«la Tabla 7 reproduce tambien desde per_type»**: hoy falla por `nemotron-mini:4b_baseline`, con
  22,59 publicado frente a 21,4985 en los recuentos. Ese fallo depende de la **decisión 1** —adoptar
  o no el consolidado nuevo—, que es del autor, no vuestro. No intentéis cerrarlo.
- **«el ANOVA titular se recalcula desde el CSV»**: si adoptáis el consolidado nuevo sin que el autor
  lo decida, esta comprobación empieza a fallar. **No cambiéis `CSV_CONSOLIDADO`.**

El segundo ya hace **bloqueante** `parse_method='failed' == 0`, que lo pusisteis vosotros y está bien.

---

## 6. Una petición sobre cómo declarar los resultados

Vuestra nota de entrega de `§3.bis.15` decía «la conclusión no cambia; la magnitud sí». Para
`nemotron-mini:4b`, que es el modelo que re-ejecutasteis, era cierto. Generalizado a los trece, no:
`llama3.2:latest` pasaba de p ajustada 0,0069 a 0,2334 en la métrica de tres categorías. Al final la
conclusión **sí** se sostiene, pero por la métrica restringida, no por la que comprobasteis.

**La petición, concreta:** cuando declaréis que una conclusión no cambia, comprobadla en **los trece
modelos** y **en las dos métricas**, no en el modelo re-ejecutado. Y añadid la prueba del supuesto
—Brown-Forsythe, centrado en mediana— al `statistical_report.md` del consolidado: es lo que sostiene
el ANOVA, y en los datos nuevos **no se cumple** (p = 1,39e-11 en tres categorías, 9,99e-10 en la
restringida), de modo que la prueba adecuada pasa a ser Alexander-Govern o Kruskal-Wallis. Las dos
dan p abrumadora, así que la conclusión no está en riesgo; lo que está mal es la prueba, y conviene
que el informe estadístico lo diga.

**Una precisión para que no la apliquéis de más:** eso vale para **vuestro** `statistical_report.md`
del consolidado nuevo, no para el informe de tesina. El informe calcula su ANOVA sobre la métrica de
tres categorías del consolidado **publicado**, donde Brown-Forsythe sí da p = 0,18, de modo que su
frase es correcta tal como está. Cambiarla solo hace falta si el autor decide adoptar el consolidado
nuevo, y esa decisión no es vuestra.

---

## 7. Rama

Trabajad sobre **`main`**, que es donde está todo fusionado. `fix/recorrida-correcciones-20260908`
está **totalmente fusionada** —cero commits que no estén en `main`, y 132 detrás— y podéis borrarla.

---

## 8. Añadido el 2026-09-09 tras verificar vuestra entrega del `RUNS_INDEX`

**Vuestras cinco afirmaciones están confirmadas, una por una.** Los 8 `failed` de
`benchmark_n120_REMOTO` son **todos** `nemotron-mini:4b_baseline` —y los ocho tienen latencia 0, 0
tokens y recall 0, o sea rechazo de infraestructura con pérdida total, el defecto de `§F85`
exacto—; las **39** corridas dan **cero** `failed` en 4 290 filas, cero sin `detailed_results.json`
y cero filas con F1 > (P + R) / 2; `ANALISIS_CONJUNTO_20260909` está retirado; y el
`TP+FN = 1098/1500/1034` sale **sobre los dos modos con los 7 contaminados excluidos** —lo comprobé
mal la primera vez, dividiendo por dos, y la cifra que falla era la mía—.

**Y una cosa que conviene que sepáis, porque afecta a cómo se lee vuestra campaña.** Las 39 corridas
usan `rag_mode=kb_combined`, incluidas las de N=15 y N=30. Las corridas **publicadas** de esos dos
corpus usan `entities`. De modo que **las pequeñas de vuestra campaña no son una versión corregida
de las publicadas: miden otro modo** —diccionario de entidades frente a base de conocimientos
contextual, que es la comparación de §5.6—.

No hay que cambiar nada: la campaña es coherente consigo misma y la extensión es legítima. Lo que
hay que **no** hacer es presentarlas como sustitutas de las cifras de §5.1, §5.2, la ablación del
idioma o las tablas 4, 5, 6 y 8. Si alguien lee «13 modelos × 3 corpus, todas VÁLIDAS» y concluye
que ya hay versión correcta de todo, mezclaría dos experimentos bajo el mismo encabezado.

**Sugerencia concreta para el `RUNS_INDEX`:** añadid una línea diciendo que las corridas de N=15 y
N=30 de la campaña son en modo `kb_combined` y **no reemplazan** a las publicadas en modo
`entities`. Es una frase y ahorra el malentendido. Ver `FINDINGS §F125`.
