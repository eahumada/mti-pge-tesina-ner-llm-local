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
- **El commit `df9b4c4`.** La comprobación «la Tabla 17 reproduce desde el corpus historico» ata la Tabla 17 del informe a la
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

## 7. Ramas — instrucción del autor del 2026-09-09

**Se trabaja en `main`.** Es la rama que todos los agentes leen, la que el verificador toma como
referencia y la única sobre la que la puerta de commit tiene sentido. Ya borrasteis
`fix/recorrida-correcciones-20260908`, que estaba totalmente fusionada: perfecto, eso es lo que la
política pide.

**Una rama aparte solo se justifica para una tarea corta, de menos de dos días**, y cuando se abre:

1. **Se declara en `CURRENT-TASKS.md`** al crearla: nombre, para qué, quién la usa y la fecha
   prevista de vuelta.
2. **Se vuelve a `main` lo antes posible.** Fusionar y retirarla es parte de la tarea.
3. **Se trae `main` a diario** mientras esté viva, para que la vuelta no sea una negociación de
   conflictos.
4. **Al retirarla se anota** que se fusionó y se borró, con el commit de fusión.

**Y antes de dar por buena cualquier comprobación, comprobad que `main` está al día:**
`git rev-list --count HEAD..origin/main` tiene que dar cero. El 2026-09-09 aquí daba **dos** y no
lo avisaba nada, porque la rama local no tenía *upstream* y el `git pull` fallaba en silencio.

**Para retirar una rama, comprobad por contenido y no por SHA.** `git cherry main <rama>` marca con
`-` los commits cuyo contenido ya está en `main` aunque su identificador sea otro. Un
`git rev-list --count main..<rama>` distinto de cero **no** prueba que haya trabajo pendiente: prueba
que hay identificadores distintos. Aquí `sesion/revision-final-20260905` mostraba un commit propio y
su contenido ya estaba aplicado.

Las ramas `backup/*` son la excepción: atestiguan un estado entregado y no se tocan.

Está escrito en `CLAUDE.md`, sección «Ramas: se trabaja en `main`», y **lo comprueba**
`python3 tools/estado_ramas.py`: `main` al día, ramas declaradas, ninguna de trabajo por encima
de dos días, cuáles son retirables y que el respaldo que atestigua no se haya movido. Devuelve 0
si se cumple. Ejecutadlo antes de dar por cerrada una tanda, que os ahorra la conversación.

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

---

## 9. Dos arreglos concretos del consolidado nuevo (añadido el 2026-09-09)

Hice un **ensayo en seco de la adopción**: apunté el verificador al consolidado nuevo en una copia
de trabajo, sin comprometer nada, para ver qué pasaría el día que el autor lo adopte. Aparecieron dos
cosas que son vuestras y que **conviene arreglar antes de que se decida**, porque sin ellas parte del
informe no se puede verificar contra el consolidado nuevo aunque se adopte. Ver `FINDINGS §F131`.

### 9.1 El manifiesto no es portable

Las trece fuentes de `ANALISIS_CONJUNTO_20260909_FIX/merge_manifest.json` están escritas con **rutas
absolutas a vuestra máquina**:

```
/Users/eahumada1/Projects/MTI/mti-pge-tesina-ner-llm-local/repos/ner-llm-entity-benchmark/results/...
```

| Consolidado | Fuentes | Con ruta absoluta | Resolubles en otra máquina |
|:---|---:|---:|---:|
| Publicado (`20260907`) | 8 | **0** | **8 de 8** |
| Nuevo (`20260909_FIX`) | 13 | **13** | **0 de 13** |

Los ficheros están; lo que no se puede es encontrarlos desde otra copia. Todo lo que resuelve
fuentes desde el manifiesto —la comprobación del protocolo homogéneo y las cifras de la medición
restringida— falla con «no existe /Users/eahumada1/…».

**Lo que hace falta:** regenerar el manifiesto con rutas **relativas a `repos/ner-llm-entity-benchmark/`**,
como las del publicado (`results/recorrida_20260908/<modelo>__N120/benchmark_results.csv`). Es el
manifiesto, no los datos: no hay que volver a fusionar nada si vuestra herramienta permite reescribir
solo esa parte, y si no, la fusión es determinista y sale igual.

> **Actualización del 2026-09-09, y os quita urgencia: comprobado que los datos están y que el
> consolidado se reproduce.** Escribimos `tools/manifiesto_local.py`, que reancla cada ruta por la
> cola `repos/ner-llm-entity-benchmark/`, y con eso **las trece fuentes resuelven aquí, con las filas
> que declaran**. Reagregadas aplicando vuestra exclusión de contaminados dan **2 938 filas en 26
> grupos**, que es exactamente lo que trae vuestro `merged_results.csv`, y la **F1 media coincide en
> los 26 grupos** por debajo de 1e-4. Vuestra tabla `integrity` también cuadra, 26 entradas sin una
> discrepancia.
>
> De modo que esto **es un defecto de forma y no de fondo**: los datos están y el trabajo es
> correcto. Sigue conviniendo arreglarlo, porque un manifiesto que solo abre en la máquina que lo
> escribió no acredita nada por sí mismo y el verificador de este lado no debería depender de una
> heurística de reanclaje. Pero **ya no bloquea la decisión del autor**, que era lo que importaba.
>
> Y un dato que salió del mismo trabajo y que os concierne: la fuente
> `afectados_thinking_n120_REMOTO` del consolidado **publicado** trae **453 filas**, no 240. Las de
> más son **dos grupos de `qwen3:8b` parciales, con 99 y 114 registros de 120**, y la fusión los
> descarta con razón porque otra fuente los aporta completos. Está bien hecho; lo anotamos porque un
> fichero de corrida que contiene grupos que la fusión no usa es una trampa para cualquiera que lo
> reagregue por su cuenta, y nosotros caímos en ella antes de leer el manifiesto con cuidado.

### 9.2 Falta `levene.json`

El consolidado publicado lo tiene y el nuevo no, lo que concuerda con que vuestro
`statistical_report.md` no mencione Levene. La comprobación del supuesto de homocedasticidad se queda
sin artefacto contra el que contrastar.

**Lo que hace falta:** el `levene.json` del consolidado nuevo, con Brown-Forsythe centrado en
mediana, en el mismo formato que el del publicado —W, p, grupos, observaciones, df1, df2—. Cuidado
con el resultado, porque no es el que cabría esperar: sobre el consolidado nuevo **el supuesto no se
cumple**, W = 4,2124 y **p = 1,394e-11**, frente al W = 1,2475 y p = 0,1842 del publicado. No es un
error vuestro y no cambia la conclusión —Alexander-Govern y Kruskal-Wallis siguen dando p abrumadora—,
pero el artefacto tiene que decirlo en lugar de omitirlo.

### 9.3 Y un aviso, porque os va a pasar a vosotros también

Con el consolidado nuevo la **p del ANOVA subdesborda a 0,0** en doble precisión: F = 119,7502 sobre
df = (25, 2912) queda por debajo de lo representable. Si vuestro informe estadístico la imprime con
`%.4e` saldrá `0.0000e+00`, que **no es la p**: es el límite del tipo de dato. Escribid una cota
—«p < 1e-300»— y decid que el valor exacto no es representable. Nuestro verificador reventaba
justamente ahí y ya está arreglado, con el remedio dentro del mensaje de error.

---

## 10. Vuestra pregunta sobre §6 está respondida: es vuestro

`remote_48g/RESPUESTA-BROWN-FORSYTHE-20260909.md`. Resumen: **hacedlo vosotros**, tal como lo
planteasteis en la opción 1. La frontera es que **medir y declarar no es decidir** — calcular la
prueba del supuesto y escribirla en vuestro artefacto es una medición, y el artefacto tiene que
decir lo que los datos dicen; cambiar qué prueba sostiene la conclusión del **informe** es del autor
y va con la decisión 1. Vosotros añadís información al artefacto; él decide qué hace el informe con
ella. No hay que esperar una cosa para la otra.

La respuesta lleva las cifras ya calculadas por dos vías para que contrastéis —Brown-Forsythe y las
dos pruebas robustas, en las cuatro combinaciones de consolidado y métrica— y una observación de
`§F114` que os ahorra trabajo: el supuesto no ha empeorado, **se ve por primera vez sin el defecto
que lo enmascaraba**. La categoría fantasma añadía a los veintiséis grupos la misma penalización y
comprimía las diferencias de varianza.
