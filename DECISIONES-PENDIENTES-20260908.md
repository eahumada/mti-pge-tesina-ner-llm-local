# Decisiones que esperan al autor

**Actualizado: 2026-09-08, 21:36.** Reunidas aquí porque estaban repartidas entre `FINDINGS.md`,
`CURRENT-TASKS.md` y varios documentos sueltos, mezcladas con decisiones ya tomadas. Son **siete**, todas con
recomendación y ninguna bloquea a otra.

Las dos últimas —la **6**, sobre `gpt-oss:20b`, y la **7**, sobre el post-hoc— son las que más conviene
resolver pronto: la primera porque afecta a horas de máquina y la segunda porque toca una conclusión del
capítulo de resultados.

---

## 1. ¿El informe adopta ya F = 35,5557, o espera al consolidado nuevo? — **SUPERADA**

> **Resuelta por los hechos el 2026-09-09.** Se recomendaba esperar al consolidado nuevo y **ya existe**:
> `ANALISIS_CONJUNTO_20260909`, trece modelos sobre el corpus corregido, **F = 121,5602**, verificado de
> forma independiente reproduciéndolo desde las corridas. El F = 35,5557 era el recálculo del corpus
> **antiguo** sin los contaminados, y ha dejado de ser una opción: el informe irá con las cifras del
> consolidado nuevo. Lo único que retiene esa adopción es `§F85`, los diecisiete ceros de `nemotron-mini`.

**Qué pasa.** El ANOVA publicado (F = 38,2222, p = 3,4453e-160) se calculó **incluyendo los siete artículos
contaminados** que la propia decisión del 2026-09-08 manda excluir. Sin ellos: **F = 35,5557,
p = 3,6729e-148**, sobre 2 938 observaciones en lugar de 3 120.

**Lo que no cambia:** ninguno de los trece modelos cambia de veredicto. Siguen siendo `nemotron-mini:4b` y
`llama3.2:latest` los dos únicos con mejora significativa. **Lo que sí:** el efecto del RAG se encoge en doce
de los trece.

**Recomendación: esperar.** La re-corrida completa va a sustituir el consolidado entero, así que adoptar la
cifra ahora es trabajo que se hace dos veces. El riesgo de esperar es nulo mientras no se entregue.
**Salvo que haya que entregar antes de que termine la re-corrida**, en cuyo caso hay que adoptarla, porque el
informe no puede publicar una cifra calculada sobre una población que él mismo declara excluida.

Evidencia: `FINDINGS §F66`.

---

## 2. Los respaldos con nombres de modelos excluidos — **recuento corregido, y menos grave**

> **Comprobado el 2026-09-09, y las dos cifras del planteamiento original estaban mal en direcciones
> opuestas.** No son nueve: son **104** los ficheros `.bak*` que contienen algún nombre de modelo excluido.
> Pero **ninguno está rastreado por git** —cero de 104—, porque `.gitignore` los excluye con `*.bak_*`.
>
> Eso cambia lo que se decide. No es un problema de integridad del repositorio ni de los entregables: esos
> ficheros **no llegan al remoto, no aparecen en ningún clon y no forman parte de ninguna entrega**. Es
> higiene del árbol de trabajo local, y como tal no corre prisa.
>
> Se conserva abajo el planteamiento original porque documenta la preocupación, que era razonable antes de
> comprobar el rastreo.

### Planteamiento original (2026-09-08)


**Qué pasa.** De los 36 `.bak_prescore` —instantáneas anteriores a la corrección de puntuación—, doce se
versionaron hoy por ser única copia y estar limpios. **Nueve contienen nombres de modelos excluidos** y
siguen sin versionar, es decir, **sin respaldo**: si alguien los borra, no hay vuelta.

**La tensión es real.** La política prohíbe esos nombres en ficheros de datos versionados; pero también
manda conservar los artefactos que atestiguan, y un respaldo histórico es de esa clase.

**Recomendación: decidir explícitamente, en cualquier sentido.** Lo que no conviene es el estado actual, que
es «ni una cosa ni otra»: fuera de la política y sin respaldo. Si se versionan, conviene una nota que
explique por qué esos nombres siguen ahí.

Evidencia: `FINDINGS §F67.bis`.

---

## 3. Los dos ficheros JSON que el barrido de exclusión dejó ilegibles — *contexto verificado*

> **Comprobado el 2026-09-09, y el contexto importa más de lo que el planteamiento original decía.**
>
> A diferencia de los **104** respaldos de la decisión 2 —ninguno rastreado—, estos dos **sí están en el
> repositorio**, y no por descuido: el commit `b59b1d6` versionó deliberadamente **doce** respaldos previos a
> la corrección de puntuación, como prueba de qué había antes de tocarla. `.gitignore` excluye `*.bak_*`,
> pero no desrastrea lo que se añadió a propósito.
>
> **De esos doce, once son JSON y nueve están íntegros.** Parsean y traen sus registros: 1 200, 507, 240,
> 240, 120, 60, 30 y dos resúmenes de dos claves. **Los rotos son exactamente los dos de este apartado**, los
> de `excluidos_n120_REMOTO`.
>
> Eso acota la decisión: no hay un problema general con los respaldos versionados, hay dos ficheros
> concretos, y son los del barrido que retiró un modelo excluido. **Y siguen sin parsear**, verificado hoy.


> ### Daño localizado y reparación viable — comprobado el 2026-09-09
>
> Los dos ficheros están roto por el mismo motivo: el nombre del modelo excluido se retiró **como texto**, y
> eso dejó el JSON sin sintaxis válida.
>
> | Fichero | Qué está roto | Alcance |
> |:---|:---|---:|
> | `benchmark_summary.json.bak_prescore` | Dos claves quedaron sin nombre: la línea dice `: {` en lugar de `"modelo": {` | **2** de 4 claves |
> | `detailed_results.json.bak_prescore` | El valor de `"model":` quedó vacío | **240** de 480 registros |
>
> Las mitades intactas son las de `gpt-oss:20b`, que es el modelo que sí forma parte del estudio: el fichero
> vigente `benchmark_summary.json` tiene exactamente `gpt-oss:20b_baseline` y `gpt-oss:20b_kb_rag`.
>
> **La reparación es viable y no exige restituir el nombre prohibido:** basta poner un marcador neutro
> —`"modelo_retirado"`— en las dos claves y en los 240 valores. El fichero vuelve a parsear, la lista cerrada
> se sigue respetando y **no se pierde nada más de lo que ya se perdió**.
>
> | Opción | Qué implica |
> |:---|:---|
> | **a) Reparar con marcador neutro** | Dos claves y 240 valores. El artefacto vuelve a ser legible por cualquier herramienta y deja de necesitar la excepción del verificador |
> | **b) Dejarlos rotos y declarados** | Es el estado actual. Un JSON roto **no es evidencia legible**: nadie puede abrirlo para comprobar nada |
> | **c) Retirarlos** | **Se desaconseja.** Son respaldos previos a la corrección de puntuación, versionados a propósito como prueba de qué había antes |
>
> **Recomendación: (a).** Un respaldo que no se puede abrir no cumple la función por la que se versionó.

### Planteamiento original (2026-09-08)


**Qué pasa.** `results/excluidos_n120_REMOTO/detailed_results.json.bak_prescore` tiene **240 de 480** claves
`"model"` sin valor, y su `benchmark_summary.json.bak_prescore` perdió una clave de primer nivel. Los rompió
la retirada de nombres, hecha por sustitución de texto. **Las otras 240 filas son de `gpt-oss:20b` y están
intactas**, atrapadas dentro de un fichero que ya no se puede cargar.

**Recomendación: reparar quedándose con las filas cuyo `model` tenga valor**, y anotar dentro del fichero
cuántas se retiraron y por qué. Eso deja un JSON válido, respeta la exclusión y salva lo salvable. No lo hice
por iniciativa propia porque implica decidir qué pasa con las 240 del modelo excluido.

Evidencia: `FINDINGS §F70`.

---

## 4. Las cuatro filas sin corrida de origen de `BENCHMARKS.md`

**Qué pasa.** Único bloqueante del `TODO §10` que sigue abierto, de los ocho —los otros siete están cerrados.
Son cuatro filas de configuraciones de prompt cuyas cifras no son trazables a ningún artefacto. Ya están
marcadas con su advertencia, y **el informe no las usa**: su Tabla 5 publica la corrida catalogada.

**Recomendación: dejarlas donde están, con su advertencia.** No bloquean la defensa. Retirarlas también sería
defendible; lo que no lo sería es publicarlas sin la advertencia, y eso ya está resuelto.

---

## 5. Quién propaga los commits pendientes a los tres `.docx`, y cuándo

> **Recuento actualizado el 2026-09-09: son 27, no 22.** Los `.docx` siguen congelados en `6299d13`
> (2026-09-08, 04:25) y el Markdown ha recibido veintisiete commits desde entonces. La cifra del título se
> deja sin número porque envejece con cada corrección; el recuento vigente se obtiene con
> `git rev-list --count 6299d13..HEAD -- <ruta-del-md>`. **La lista de propagación sí está al día**: cero
> commits al Markdown desde su última actualización.
>
> **Y ha aparecido un motivo nuevo para esperar**, más fuerte que el de no propagar dos veces: la re-corrida
> desmiente la tesis central tal como está escrita (`FINDINGS §F86`), de modo que §5.3.1, §6, el resumen y el
> abstract van a reescribirse. Propagar ahora sería maquetar un texto que va a cambiar. Ver la **decisión 11**.

**Qué pasa.** Los tres `.docx` están congelados en el commit de las 04:25 y el Markdown ha recibido 22
commits desde entonces. **El entregable no es el informe.** Y lo más delicado no es lo que falta sino lo que
dice: su §3.3 afirma «el 65 %, 20 946 de 32 201», que es la cifra del Anexo I sobre 42 configuraciones
aplicada a una sección que habla del estudio.

**Recomendación: propagar antes de cualquier entrega, y no con pandoc.** La lista exacta, con ubicaciones,
está en `PROPAGACION-PENDIENTE-DOCX-20260908.md`. Conviene esperar a que termine la re-corrida para no
propagar dos veces, **salvo** que haya entrega antes.

---

## 6. ¿Se re-ejecuta `gpt-oss:20b` sobre el corpus corregido? — **HECHO**

> **Ejecutada el 2026-09-08 a las 23:44** y verificada con las cinco comprobaciones del protocolo: cero
> `parse_method='failed'` en 330 registros, cero violaciones de `F1 ≤ (P+R)/2`, cero rechazos de
> infraestructura y firma del corpus correcta en los tres. **N=120: 75,41 base y 77,08 con RAG, Δ +1,67**,
> frente al +3,28 publicado; el signo se mantiene. Un solo respaldo frente a los 67 que producía el
> presupuesto de 2048 *tokens*, que era lo que el equipo quería demostrar. **No queda nada que decidir.**

**Qué pasa.** No está en el barrido: ni `START`, ni `END`, ni `SKIP`. La causa probable es una lectura literal
de `§F44`, donde usted lo congeló «con think ON, sin re-ejecutar».

**Por qué importa.** Esa decisión era sobre el *thinking*, no sobre el corpus. Si no se re-ejecuta, el
consolidado final tendría **doce modelos sobre el corpus corregido y uno sobre el antiguo**, y su F1 quedaría
unos veinte puntos por debajo del resto por un defecto del corpus y no por su desempeño.

**Recomendación: re-ejecutarlo con `think` ON**, que es lo que la decisión protege, sobre el corpus corregido
y con 4 096 tokens. Respeta `§F44` en lo que decía y resuelve de paso la asimetría de presupuesto que hoy lo
hace incomparable con los otros doce.

Evidencia: `FINDINGS §F72`. La guarda de 26 grupos impediría que se colara en silencio, pero descubrirlo al
fusionar cuesta otra tanda de horas de máquina.

---

## 7. ¿Cambia el informe su post-hoc al contraste apropiado al diseño? — *cifras nuevas*

> **Actualización del 2026-09-09.** La pregunta sigue viva, pero las cifras que la motivaban han cambiado.
> El «ocho de trece» de más abajo es sobre el corpus **antiguo**. Sobre el **corregido**, el mismo contraste
> pareado da **tres de trece** —`nemotron-mini:4b`, `llama3.2:latest` y `gemma4:12b-mlx`—, con
> `gemma4:latest` y `mistral-nemo:latest` al borde (Holm 0,0595 y 0,0577). El argumento metodológico se
> mantiene intacto: Tukey sobre 325 comparaciones responde a otra pregunta. Lo que cambia es que **ya no
> reclasifica ocho modelos, sino uno**, y por tanto pesa menos en la decisión. Artefacto:
> `results/ROBUSTEZ_ESTADISTICA_20260909/robustez.json`.

**Qué pasa.** §5.3.1 concluye que solo dos modelos mejoran de forma significativa. Con el contraste que
corresponde al diseño —Wilcoxon pareado sobre los mismos registros, con corrección de Holm sobre las **trece**
comparaciones de interés en lugar de Tukey sobre las **325** posibles— resultan **ocho de trece**.

**Por qué importa.** No es un tecnicismo: hoy el informe agrupa como «no concluyentes» a modelos con **+7,36
pp** y a otros con **−0,54**, lo que es difícil de defender. Con el contraste pareado los cinco que no
alcanzan significancia son exactamente los de efecto nulo o negativo.

**Recomendación: adoptarlo, y declarar ambos.** La afirmación resultante es **más fuerte y más matizada**, y
la tesis de la proporcionalidad inversa **sale reforzada**: los dos mayores efectos son los dos modelos más
pequeños. El Tukey no se retira —responde a otra pregunta, la de todos los pares— sino que se acompaña.

**Cuándo.** Después de la re-corrida, porque los datos cambian; pero el argumento metodológico vale igual
para los datos nuevos, así que conviene decidirlo ya.

Evidencia: `FINDINGS §F76`.

---

## 8. El emparejamiento duplicado: qué declara el informe — *reformulada el 2026-09-09*

> **Esta decisión estaba mal planteada y se reformula.** Preguntaba si corregir `evaluator.py` y cuándo.
> **Ya está corregido**, en la rama de la re-corrida y desde el 2026-09-08, con la referencia
> `encargo §2.3, FINDINGS §F49/§F50`; la re-corrida entera usa la versión corregida y se ha comprobado
> contra la fuente que su `tp + fn` vale exactamente la anotación de los 113 artículos, sin un acierto de
> más. Lo que sigue abierto es otra cosa: **qué dice el informe de los datos antiguos**, que sí lo
> arrastran y que conviven con los nuevos hasta que la re-corrida termine. Ver `FINDINGS §F81.ter`.

`src/evaluator.py` cuenta `tp` por cada entidad extraída que casa, pero `fn` sobre las referencias
**distintas** casadas. Cuando dos extracciones casan con la misma referencia —«John Smith» y «Smith, John»,
iguales para el emparejamiento difuso al 85 %— `tp` sube dos veces y la referencia se cuenta una. Consecuencia
medible: la exhaustividad por categoría **pasa de 1,0 en 197 registros**, con un máximo de 2,444. Evidencia
completa en `FINDINGS §F81`; artefacto en `results/EMPAREJAMIENTO_DUPLICADO_20260908/efecto.json`.

**El efecto está acotado y no cambia ninguna conclusión.** Recalculado contando cada referencia una vez: el F1
publicado está inflado **+0,160 pp de media**, máximo **+1,287 pp** en `nemotron-mini:4b_baseline`; **ninguna**
de las trece mejoras cambia de signo. Queda muy por debajo del umbral de 0,02 en F1 que `CLAUDE.md` declara
tolerable. El orden de los veintiséis grupos cambia en **un solo puesto**, entre dos separados por 0,24 pp, y
el informe no publica una ordenación de grupos.

*(Cifras corregidas el 2026-09-09: las primeras se calcularon leyendo ocho de los veintiséis grupos de la
corrida equivocada. Ver `FINDINGS §F81.bis`.)*

**Ya no es urgente, y la razón por la que lo parecía era equivocada:** se dio por hecho que la re-corrida
usaba el evaluador defectuoso, y usa el corregido desde el primer modelo.

| Opción | Qué implica |
|:---|:---|
| **a) Declarar el defecto de los datos antiguos** | Una línea en las limitaciones: las cifras anteriores a la re-corrida están infladas +0,160 pp de media por un doble conteo ya corregido, y ninguna conclusión cambia. Cuesta poco y desactiva la objeción |
| **b) No declararlo** | Defendible si la re-corrida sustituye **todas** las cifras del informe antes de la entrega. Riesgo: si alguna tabla se queda con datos antiguos, queda sin declarar |
| **c) Recalcular las cifras antiguas** | `tools/efecto_emparejamiento_duplicado.py` lo hace sin reejecutar inferencia, y la tabla ya está en `tabla7_recalculada.md`. Obligaría a rehacer Anexo I, Figura 2, ANOVA y post-hoc |

**Recomendación: (a) si queda alguna cifra antigua en el informe, y (b) solo si no queda ninguna.** La (c)
tiene poco sentido cuando la re-corrida va a sustituir esos datos de todos modos.

**La tabla ya está calculada, para que la decisión se tome mirando cifras.**
`results/EMPAREJAMIENTO_DUPLICADO_20260908/tabla7_recalculada.md` trae la Tabla 7 completa con las dos
columnas enfrentadas, modelo por modelo, y el recuento de emparejamientos duplicados de cada uno. Los
extremos: `gemma4:latest` acumula **143** duplicados y su línea base baja de 55,91 a 54,98, mientras
`nemotron-mini:4b` con solo **11** baja de 22,59 a 21,31 —más, porque su exhaustividad es pequeña y unos
pocos aciertos repetidos pesan proporcionalmente más—. Los dos únicos Δ significativos del estudio,
`llama3.2:latest` y `nemotron-mini:4b`, **crecen** al corregir: +10,82 → +10,91 y +14,52 → +15,75.

**Y hay que decidir si el informe lo declara.** Declararlo es barato y protege: una exhaustividad de 2,444 en
los datos crudos es justo lo que un tribunal encuentra si mira, y hallarla sin que el trabajo la mencione es
peor que la propia cifra.

---

## 9. El 60–80 % de reducción de coste total: ¿se matiza en la conclusión 4?

La conclusión 4 dice, entre paréntesis, «60–80 % del costo operativo total, que incluye la supervisión
humana». **El informe no deriva esa cifra en ninguna parte.** Es el rango que fijaron los objetivos al
principio del trabajo, no un resultado calculado a partir de los datos.

El resto del párrafo está bien construido: declara que las cifras son estimaciones y no mediciones, y §5.5
advierte de que el ahorro real «depende de cuánto reduzca el volumen que llega a revisión humana», que es
justo lo que el estudio no midió. **La única cifra sin respaldo es el 60–80 %**, y va sin matiz, presentada
como dato junto al 99,4 %, que sí tiene sus parámetros a la vista.

| Opción | Qué implica |
|:---|:---|
| **a) Dejarlo** | La conclusión ya declara que son estimaciones. Riesgo: quien pregunte por el 60–80 % encontrará que no hay de dónde sacarlo, y la respuesta tendrá que darse en la sala |
| **b) Matizarlo** | Añadir que ese rango es **el objetivo planteado** y no un resultado medido, porque el ahorro total depende de la reducción de volumen que el trabajo no midió. Cuesta una línea y convierte un flanco en una limitación declarada |
| **c) Retirarlo** | Dejar solo el 99,4 % unitario. **Se desaconseja**: el objetivo 5 lo menciona y desaparecería la conexión entre objetivo y conclusión |

**Recomendación: (b).** Es neutra en extensión y es lo que ya hace el resto del informe con sus otras
limitaciones. La respuesta preparada, por si se decide (a), está en
`DEFENSA-PREGUNTAS-Y-RESPUESTAS.md §Sobre las cifras económicas`.

*Antecedente:* la auditoría del 2026-09-03 ya trató la contradicción entre 60–80 % y 99,4 % (hallazgo M9) y
la resolvió distinguiendo coste unitario de coste total, y retirando la afirmación del resumen. Lo que quedó
sin resolver es el respaldo del rango, no su coherencia.

---

## 10. ¿Qué se hace con la Tabla 4, que la re-corrida no puede sustituir?

La Tabla 4 publica el benchmark exploratorio de N=15 y su glosa declara expresamente que las cifras se
midieron «sobre `results/benchmark_results.csv` (N=15, modo `entities`)». **La re-corrida mide sus N=15 en
modo `kb_combined`**, en las veintisiete corridas, porque así lo encargó
`remote_48g/LANZAMIENTO-RECORRIDA-20260908.md`.

No es un error de nadie: el encargo unificó el modo a propósito para que el barrido fuera homogéneo. Pero
tiene una consecuencia que conviene ver ahora y no el último día: **los N=15 de la re-corrida no sustituyen a
la Tabla 4**, porque miden otra cosa. Ni siquiera son comparables fila a fila.

Además hay un segundo desajuste, anterior: la Tabla 4 cubre **doce modelos en trece configuraciones**
—`gemma4:latest` aparece en dos variantes de prompt— mientras la re-corrida hace **trece modelos en una sola
configuración**. Las dos poblaciones no coinciden.

| Opción | Qué implica |
|:---|:---|
| **a) Dejar la Tabla 4 como está** | Publica lo medido en modo `entities` sobre el corpus antiguo, con su glosa declarándolo. Es coherente consigo misma. Riesgo: el informe acabaría con una tabla sobre el corpus viejo y otras sobre el corregido, y hay que decirlo en algún sitio |
| **b) Retirar la Tabla 4** | **Se desaconseja.** Es el único material del capítulo exploratorio y su retirada dejaría §5.1 sin datos |
| **c) Encargar un N=15 en modo `entities`** | Trece corridas más de quince artículos, baratas en máquina. Daría una Tabla 4 sobre el corpus corregido y comparable con la publicada |

**Recomendación: (a), y añadir una línea que declare la asimetría** —que la Tabla 4 procede del corpus y del
modo anteriores mientras el resto del capítulo usa el corregido—, que es lo que el informe ya hace con sus
otras corridas múltiples en el Anexo I. La opción (c) solo merece la pena si al cerrar la re-corrida sobra
tiempo de máquina.

**Lo que no debe hacerse** es sustituir las cifras de la Tabla 4 por las de la re-corrida sin más: parecen la
misma medición y no lo son.

### La Tabla 8 está en el mismo caso, y por partida doble

Comprobado el 2026-09-09. La glosa de la Tabla 8 declara que sus valores se miden «sobre
`benchmark_results.csv` (subconjunto `_baseline`, **N=15**)», de modo que hereda el problema anterior: la
re-corrida mide sus N=15 en otro modo. Y hay un segundo obstáculo, este insalvable: **su primera fila,
`gemma4:31b`, no existe en la re-corrida**, que solo trae `gemma4:31b-cloud` y `gemma4:31b-mlx`. Esa fila
procede de `results/gemma4_31b_n15_REMOTO/`, una corrida anterior, y la propia glosa lo declara.

**Lo tranquilizador es que apenas importa.** Contrastadas las otras dos filas con los datos de N=120 de la
re-corrida, las magnitudes se mueven poco y en la dirección esperable:

| Fila de la Tabla 8 | Tok/s publicado | Tok/s en la re-corrida | VRAM publicada | VRAM en la re-corrida |
|:---|---:|---:|---:|---:|
| `gemma4:31b-mlx` | 22,80 | 25,04 | 24 607 | 26 720 |
| `llama3.2 (3B)` | 79,35 | 85,16 | 4 018 | **4 018** |
| `gemma4:31b` | 10,23 | *no medido* | 18 795 | *no medido* |

La VRAM de `llama3.2` reproduce **exactamente**. El índice Tok/s/B pasaría de 0,74 a 0,81 en el 31B y de 26,5
a 28,4 en el 3B, de modo que **la afirmación que la tabla sostiene —dos órdenes de magnitud de diferencia en
eficiencia por unidad de capacidad— se mantiene con holgura**. No hay urgencia en tocarla.

**Recomendación para la Tabla 8: dejarla**, con la glosa que ya declara su procedencia. Actualizar dos de sus
tres filas y dejar la tercera con datos de otra corrida sería peor que no tocar ninguna.

---

## 11. Cómo se reformula la tesis central — *la decisión de fondo*

`FINDINGS §F86` deja establecido que la proporcionalidad inversa entre capacidad y beneficio del RAG **no se
sostiene sobre el corpus corregido**: Spearman cae de −0,5165 a **−0,0879 (p = 0,7752)**, el Pearson que queda
**descansa en un solo punto** —sin `nemotron-mini:4b` es +0,0120 con p = 0,971— y los cinco modelos de mayor
capacidad tienen **todos** mejora positiva, lo que desmiente la frase literal del informe.

`INVENTARIO-AFECTADO-POR-F86-20260909.md` localiza los cuatro pasajes que hay que tocar y, tan importante como
eso, los que **no** hay que tocar.

| Opción | Qué implica |
|:---|:---|
| **a) Reformular a lo que los datos sostienen** | «Dos modelos pequeños se benefician de forma significativa, el resto apenas se mueve y ninguno de los grandes empeora.» Más modesto, verdadero y defendible. Exige reescribir §5.3.1, §6, el resumen y el abstract |
| **b) Publicar ambas mediciones** | Presentar la relación como dependiente del corpus: fuerte en el defectuoso, ausente en el corregido. Es honesto y da material de discusión, pero **alarga** un informe que ya va por 23 de 25 páginas |
| **c) Mantener la tesis publicada** | **No procede.** Los datos que la sostenían son los del corpus con las localizaciones sin anotar |

**Recomendación: (a).** Y una observación que conviene tener presente: la conclusión resultante **es más
fuerte de lo que parece**. Que la recuperación aporte de forma significativa a los modelos pequeños y no
perjudique a los grandes es exactamente lo que justifica la arquitectura en dos niveles del capítulo 6.
El argumento práctico del trabajo no depende de la forma funcional que se cae.

**Antes de escribir nada hay que esperar a `§F85`**: el punto que más pesa en el análisis es el que arrastra
los diecisiete ceros del `TypeError`.

**Y hay una parte que no es de redacción.** Las cuatro afirmaciones están también en los dos `.docx` **y en el
PDF de 31 páginas que ya se entregó al profesor guía**, comprobado. No era un error entonces —era lo que
decían los datos—, pero el profesor tiene hoy un documento que la re-corrida desmiente. **Comunicárselo por
iniciativa propia** es una decisión del autor, y probablemente la mejor: la alternativa es que la pregunta
llegue en la defensa.

---

## 12. Las dos glosas de `BENCHMARKS.md` que narran la exclusión

**Hallado el 2026-09-09** revisando las premisas del `TODO §10`. `BENCHMARKS.md` contiene dos bloques con esta
forma:

> **Retirado del estudio (2026-09-05, decisión del autor).** `minimax-m3:cloud` se elimina del benchmark: su
> única medición tenía 9 de 15 extracciones fallidas por cuota…

y otro equivalente para `nuextract:latest`. `CLAUDE.md` es explícito en este punto: los modelos excluidos no
pueden aparecer «**tampoco en una glosa que los declare excluidos**: la exclusión se aplica, no se narra».

**Lo que hace ambigua la decisión** es que `CLAUDE.md` enumera qué artefactos se conservan —`benchmark.log`,
`RUNS_INDEX.md`, los `WORKLOG.md`, los datos crudos históricos y los hitos entregados— y **`BENCHMARKS.md` no
está en ninguna de las dos listas**. Cabe leerlo como artefacto derivado, y entonces las glosas sobran; o como
documento de trabajo que atestigua qué se decidió y por qué, y entonces se quedan.

| Opción | Qué implica |
|:---|:---|
| **a) Retirar las dos glosas** | Cumple la norma al pie de la letra. La justificación de por qué se excluyeron **no se pierde**: está en `FINDINGS §F38` y en la lista cerrada de `CLAUDE.md`, que es donde corresponde |
| **b) Dejarlas** | Defendible si se considera `BENCHMARKS.md` un documento que atestigua. Riesgo: es el fichero de resultados del repositorio, el primero que abre quien quiera comprobar cifras |
| **c) Retirarlas y anotar en `CLAUDE.md` a qué lista pertenece `BENCHMARKS.md`** | Resuelve el caso y la ambigüedad que lo permitió |

**Recomendación: (c).** El coste es una línea en cada sitio y evita que la misma duda vuelva.

**No se ha tocado nada.** Editar un documento de resultados por interpretación de una norma es del autor, y
la política aditiva desaconseja retirar texto sin su visto bueno.

**Lo que no está en cuestión:** los siete ficheros de **código** que mencionan esos modelos —`config.py`,
`llm_runner.py`, `ollama_provider.py`, `gliner_provider.py`, `dashboard.py`, `run_remoto_chain.sh` y
`test_flash.py`—. Dan soporte a proveedores, no citan cifras como resultado del estudio, y retirarlos rompería
la plataforma. Tampoco lo está `results/HISTORICO_20260630/`, que el inventario ya decidió conservar.

---

## 13. La conclusión 1 cita cifras micro donde el informe declara macro

**Hallado el 2026-09-09** verificando la afirmación de viabilidad. Detalle completo en `FINDINGS §F87`; el
resumen es que la conclusión 1 dice:

> «con la medición restringida… **76,55 %** … y **90,16 %** … Bajo la convención original, que puntúa también
> una categoría sin anotar, las cifras equivalentes son **62,67 %** y **80,51 %**»

y **76,55 y 90,16 son macro mientras 62,67 y 80,51 son micro**. Los valores equivalentes bajo la convención
que §3.3 declara **única** serían **59,25 %** y **80,57 %**. Las cuatro variantes se han calculado del detalle
por registro y reproducen exactamente.

**Dos discrepancias concretas:** el 62,67 difiere en **3,42 pp** del 59,25 que publica la Tabla 7 para el
mismo modelo, y el 80,51 contradice al **80,57** que usan §5.3 y §5.4 para el mismo dato.

| Opción | Qué implica |
|:---|:---|
| **a) Sustituir por 59,25 / 80,57** | Son los valores de la convención declarada y los que publica el cuerpo. Neutro en extensión, resuelve las dos discrepancias de un golpe |
| **b) Conservar 62,67 / 80,51 y declarar el doble cambio** | Habría que decir que cambia también la agregación, y §3.3 tendría que dejar de llamar «única» a la macro |
| **c) Dejarlo** | **Se desaconseja.** Quien compare la conclusión con la Tabla 7 encuentra dos cifras para lo mismo, y con la conclusión favoreciendo a la convención antigua |

**Recomendación: (a).** Y con una salvedad sobre el resto de las decisiones de esta lista: **aquí no hay
criterio que ejercer**, solo una inconsistencia que resolver.

**Y está comprobado que la corrección basta.** La **comprobación 29** del verificador falla hoy con este
mensaje —«la conclusión 1 cita 62.67 (micro) para N=120; la convención declarada da 59.25 (macro)»— y **pasa
en verde en cuanto se sustituye el par**, probado aplicando la corrección y revirtiéndola. La comprobación
falla a propósito mientras esto no se resuelva, igual que la referencia [37] falla hasta que se complete la
purga: es la forma de que no se olvide. Se deja como decisión porque toca una conclusión
y eso no se cambia sin el autor, no porque haya dos lecturas defendibles.

---

## Y un aviso que todavía no es decisión

Con tres de los trece modelos rehechos, el efecto del KB RAG **cambia de signo en los dos de 31B**: de −0,53
y −0,18 a +0,81 y +0,97. Si eso se confirma con los trece, la frase de §5.3.1 que dice que el beneficio «se
anula o revierte en los de mayor capacidad» **habrá que reformularla**. No hay nada que decidir todavía, pero
conviene no encontrárselo el último día. Evidencia: `FINDINGS §F68`.


**Actualización del 2026-09-09, y ya no es solo un cambio de signo.** Con **once** de los trece rehechos, el
post-hoc pareado sobre el corpus corregido da **2 significativos de 11**, frente a los **8 de 13** de los
datos publicados (`FINDINGS §F83`). Sobreviven `llama3.2:latest` con +6,73 pp y `gemma4:12b-mlx` con +2,29;
`gemma4:latest` y `mistral-nemo:latest` quedan al borde, con Holm de 0,0529 y 0,0520, y el segundo con efecto
**negativo** de −4,29 pp. Sigue sin haber nada que decidir hasta que lleguen los trece —falta
`nemotron-mini:4b`, que era el de mayor efecto—, pero conviene ir asumiendo que **§5.3.1 no se arregla
cambiando cifras**: el efecto del RAG sobre el corpus corregido es sustancialmente menor y se apoyará en
menos modelos. El sentido de la tesis no se invierte; su fuerza sí disminuye.