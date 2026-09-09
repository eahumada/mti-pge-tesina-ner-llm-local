# LEARNING — Lecciones de la Revisión Final

> Lecciones extraídas de los hallazgos de [`FINDINGS.md`](./FINDINGS.md). Cada una nace de un incidente
> concreto de este proyecto, no de una buena práctica genérica.
>
> **Fecha:** 2026-09-03 · **Documentos relacionados:** [`FINDINGS.md`](./FINDINGS.md),
> [`CLAUDE.md`](./CLAUDE.md), `research/rag/WORKLOG.md`

---

## 1. Sobre el método experimental

### L1. Un hallazgo de auditoría es una hipótesis, no un hecho
La auditoría automatizada clasificó dos filas legítimas de la Tabla 2 como «duplicado». Esa interpretación
se propagó sin revisión al prompt del workflow de corrección, y un subagente habría **eliminado datos
experimentales reales** para cuadrar un conteo.

> **Aplicación:** antes de convertir un hallazgo en instrucción de corrección, validarlo contra el
> documento; y si toca datos experimentales, contra el criterio del autor. La verificación adversarial
> descartó 17 de 132 hallazgos (13%), pero no atrapó este: el verificador confirmó que las filas existían,
> sin cuestionar que fueran un error.

### L2. Los defaults silenciosos son el fallo más caro
Tres defaults distintos causaron los tres incidentes más costosos de la sesión:

| Default | Consecuencia |
|:---|:---|
| `rag_mode='entities'` | Habría producido 10 h de datos incomparables con la corrida de referencia |
| `num_workers=2` (ref.: 9) | Proyección de 183 h en vez de 14 h |
| `results_dir='results'` | Pérdida permanente de los datos por registro de N=30 |

> **Aplicación:** al reproducir una corrida previa, **leer su `run_config.json` y replicar todos los
> parámetros**, no solo los que parecen relevantes. Lo que no se especifica, se hereda del default, y el
> default rara vez coincide con el experimento anterior.

### L3. Un mecanismo de recuperación no probado no existe
El flag `--resume` estaba presente, documentado y era **completamente inoperante**: reiniciaba desde cero
en silencio. Nadie lo había ejercitado.

> **Aplicación:** probar explícitamente el camino de recuperación (matar el proceso y reanudar) antes de
> confiarle una corrida larga. Un `--resume` que falla en silencio es peor que no tenerlo.

---

## 2. Sobre el diagnóstico técnico

### L4. Medir `%cpu` distingue «lento» de «roto»
Cuatro paquetes parecían corruptos (`TimeoutError` al importar). En realidad estaban bloqueados en disco:
`import requests` gastó **2m22s de reloj pero 0.18 s de CPU (0%)**.

> **Regla práctica:** ante un timeout, comparar tiempo de CPU contra tiempo de reloj. Cerca de 0% de CPU
> significa contención de I/O, no rotura. Reinstalar habría desperdiciado ancho de banda escaso sin arreglar
> nada.

### L5. Buscar un solo código de error oculta los demás
Se concluyó que `gemma4:31b-cloud` funcionaba porque un `grep` de `402` no lo encontraba. Tenía **720 fallos
con código 429**.

> **Aplicación:** al contar errores, agrupar por categoría (`grep -oE "failed for model '[^']+'"`) antes de
> filtrar por causa concreta.

### L6. Una sola medición no establece una tendencia
Se afirmó que el enlace estaba saturado y que más concurrencia no ayudaría, a partir de **una** medición.
Un test de escalado posterior mostró que el agregado subía de 1.45 MB/s con un stream a 4.43 MB/s con
cuatro: escalaba sublinealmente, pero escalaba.

> **Aplicación:** antes de descartar una optimización por «saturación», medir el escalado con al menos dos
> puntos.

### L7. Los patrones de detección de procesos mienten
`pgrep -f "venv/bin/python src/main.py"` no encontraba nada mientras el proceso corría: el intérprete del
venv se resuelve a su ruta real de Homebrew en la tabla de procesos. Se concluyó erróneamente que el
benchmark había muerto, y esa conclusión llevó a lanzar un **segundo proceso duplicado** sobre el mismo
directorio de resultados.

> **Aplicación:** verificar la existencia de un proceso con `ps aux` y el patrón resuelto, no con el
> comando tal como se escribió.

---

## 3. Sobre la orquestación multi-agente

### L8. Verificar siempre lo que reporta un subagente
Los cinco subagentes de esta sesión reportaron con precisión, pero **cada afirmación se comprobó de forma
independiente** antes de darla por buena: se re-ejecutaron los 15 tests del guardarraíl, se reprodujo
F=10.2096 con el script de fusión, se comprobó que los `.docx` originales seguían intactos y se dif-eó el
cuerpo estadístico contra la referencia. Una de esas verificaciones detectó un **duplicado que yo mismo
introduje** al renombrar un modelo.

> **Aplicación:** el reporte de un subagente es una afirmación a verificar, no un resultado. El coste de
> verificar es minúsculo comparado con propagar un error a la tesina.

### L9. Repartir agentes paralelos por archivos disjuntos
Un workflow con varios agentes editando el mismo documento se pisa. El diseño que funcionó asigna **un
archivo (o grupo disjunto) por agente**, con una etapa posterior de verificación de integridad que
comprueba que no se perdió contenido.

### L10. La política aditiva también protege frente a la concurrencia
La regla «nunca borres, solo añade» se adoptó por trazabilidad académica, pero resultó ser además la mejor
defensa cuando **otra sesión edita los mismos archivos**: un `append` nunca destruye el trabajo ajeno,
mientras que una reescritura completa sí.

> **Aplicación:** releer el archivo inmediatamente antes de escribir; preferir `append`; y si un archivo
> cambió de forma inesperada, **no revertirlo** — puede ser trabajo deliberado de otra sesión.

---

## 4. Sobre la gestión de los entregables

### L11. Los formatos derivados divergen del canónico
Tres `.docx` coexistían con contenidos distintos entre sí y respecto al Markdown. El archivo con nombre de
entregable final (`Informe_Final_Tesina_NER.docx`) resultó ser **el más desactualizado**, sin dos secciones
completas.

> **Aplicación:** declarar explícitamente cuál es la **fuente canónica** y cuáles son derivados, y
> documentar la dirección de propagación. Recogido en `CLAUDE.md §Entregables Finales`.

### L12. Regenerar no siempre es sincronizar
La tentación de regenerar los `.docx` desde el Markdown con pandoc habría destruido correcciones manuales
de numeración multinivel, estilos de fila y saltos de página que costaron recuperar 5 páginas.

> **Aplicación:** cuando el derivado contiene trabajo que no está en la fuente, sincronizar exige
> **edición quirúrgica**, no regeneración. Ver `tools/docx_replace_terms.py`.

### L13. Nombrar mal un artefacto contamina la tesina entera
El sufijo `q8` de un modelo era falso: el artefacto real es 4-bit. Ese nombre viajó a tablas de resultados,
configuración, scripts y documentación, describiendo incorrectamente la cuantización en cada lugar.

> **Aplicación:** verificar los metadatos reales de un artefacto (cuantización, tamaño, formato) antes de
> incorporarlo a la nomenclatura de un trabajo académico. El registro de Ollama expone manifiestos y blobs
> de configuración **sin necesidad de descargar los pesos**.

---

## 5. Lecciones adicionales de la sesión

### L14. Dimensionar el hardware antes de diseñar el experimento
Se planificó un barrido de 16 modelos, entre ellos varios de 13–19 GB, sobre una máquina de **16 GB de RAM**.
El resultado fue swap masivo: 1 extracción cada 3 minutos, con una proyección de **7 días** concentrada en
tres modelos. Aumentar los workers de 2 a 8 **no cambió el ritmo en absoluto**, porque el cuello era memoria
física, no configuración.

> **Aplicación:** antes de fijar la lista de modelos de un benchmark, contrastar sus tamaños contra la RAM
> disponible. Un modelo que iguala o supera la RAM total no se «ejecuta lento»: se ejecuta en disco.
> Y si hay que excluir modelos por esta razón, **declararlo como limitación de hardware en el informe**, no
> disfrazarlo de criterio metodológico.

### L15. Reducir el alcance no siempre rompe la comparabilidad
Excluir dos modelos parecía comprometer la fusión con la corrida de referencia. No fue así: los excluidos
**tampoco estaban** en esa corrida, y los nueve parámetros del protocolo seguían coincidiendo, de modo que
ambos conjuntos permanecían disjuntos sobre el mismo corpus.

> **Aplicación:** antes de descartar un recorte por «rompe la comparabilidad», verificar los parámetros uno
> a uno contra el `run_config.json` de referencia. La comparabilidad la definen el corpus y el protocolo,
> no el número de modelos.

### L16. Un `pull` exitoso no significa que el modelo sirva
Los dos modelos cloud descargaron su manifiesto con `success`, aparecían en `ollama list`, y **toda**
inferencia fallaba (429 por cuota, 402 por suscripción).

> **Aplicación:** validar disponibilidad con una **llamada de inferencia real**, no con la presencia en el
> catálogo. Una comprobación de un solo turno al inicio del barrido habría ahorrado 20 minutos de cómputo y
> 1254 peticiones fallidas.

### L17. La corrección automatizada necesita su propia verificación
El workflow aplicó 84 correcciones e introdujo **5 regresiones**, entre ellas el borrado de un dato
(violando la política aditiva) y un fragmento de código sintácticamente inválido. La etapa de verificación
posterior las detectó todas.

> **Aplicación:** todo workflow que **modifica** archivos necesita una etapa que compare contra el backup y
> compruebe qué se perdió. Sin esa etapa, las cinco habrían llegado al entregable.

### L18. Una corrección puede trasladar la inconsistencia en vez de resolverla
Al unificar el índice Tok/s/B entre dos secciones, la Tabla 2 quedó con dos filas de métricas idénticas pero
throughput 2,4× distinto: la contradicción dejó de ser *entre secciones* y pasó a estar *dentro de la misma
tabla*, donde es más visible para un revisor.

> **Aplicación:** tras corregir una inconsistencia entre dos lugares, releer **ambos** en su contexto
> completo. Un dato coherente con su fuente puede ser incoherente con sus vecinos.

### L19. La verificación adversarial tiene un punto ciego
El verificador confirmó que las filas `(ZS-ES)` y `(FS-ES)` **existían** en el documento, pero no cuestionó
la premisa de que fueran un error. Validó el hecho, no la interpretación.

> **Aplicación:** al diseñar una etapa de verificación, pedir explícitamente que cuestione **la premisa**
> del hallazgo, no solo su evidencia textual. El humano que conoce el experimento sigue siendo el último
> filtro: el autor detectó en segundos lo que dos agentes dieron por bueno.

### L20. Detener a tiempo vale más que ejecutar rápido
Tres veces en esta sesión se detuvo trabajo en curso al detectar un defecto: un modo RAG incompatible
(20 min perdidos, ~10 h salvadas), un workflow con una instrucción peligrosa (0 archivos tocados) y un
paralelismo mal configurado. En los tres casos el coste de parar fue trivial frente al de continuar.

> **Aplicación:** ante la duda sobre la validez de una corrida larga, **parar y verificar** es casi siempre
> más barato que dejarla terminar y descubrir después que los datos no sirven.

---

## 6. Para Claude Desktop

Las lecciones con impacto directo sobre las tareas de `TODO-INFORME-FINAL.md §7`:

| Lección | Qué implica al editar los `.docx` |
|:---|:---|
| **L11** | La **fuente canónica es el Markdown**; los `.docx` son derivados. Propagar en esa dirección. |
| **L12** | **No regenerar con pandoc**: los `.docx` contienen correcciones manuales de formato que la fuente no tiene. Usar edición quirúrgica. |
| **L1** | Los hallazgos de la auditoría son hipótesis: verificar contra el documento antes de aplicar. |
| **L17** | Tras una tanda de ediciones, **comparar contra el backup** y comprobar qué se perdió. |
| **L18** | Al corregir una cifra, releer las secciones vecinas: la inconsistencia puede desplazarse. |
| **L10** | Otra sesión puede editar en paralelo: releer antes de escribir, preferir `append`, no revertir cambios ajenos. |

---

## 7. Modelos declarados que nunca se ejecutaron

### L21. Una lista de configuración no es evidencia de que algo se haya evaluado
`glm-5.1:cloud` figuraba en el listado de modelos de `BENCHMARKS.md` desde hacía meses. Al verificarlo:

- **Cero resultados** en cualquier CSV, JSON o log del proyecto
- **Ausente** de `src/config.py` (la configuración realmente activa)
- **Inexistente** en el registro público de Ollama (`library/glm-5.1` → `MANIFEST_UNKNOWN`), es decir, ni
  siquiera descargable en local
- **HTTP 402** al probar inferencia real con la API key: requiere suscripción de pago

Era una **declaración de intenciones** que nadie ejecutó, indistinguible a simple vista de un modelo
evaluado. Un lector del documento —o un tribunal— habría asumido que formaba parte del estudio.

> **Aplicación:** antes de citar un modelo en un informe, comprobar que existe **al menos una fila de
> resultados** que lo respalde. La distinción entre «configurado» y «evaluado» debe ser explícita en la
> documentación. El comando de verificación es trivial:
> `grep -rl "<modelo>" results/` — si no devuelve nada, ese modelo no se evaluó.

### L22. Distinguir HTTP 402 de 429 al evaluar modelos de pago
Los tres modelos cloud del proyecto fallan, pero **no por la misma causa**, y la diferencia decide si son
recuperables:

| Código | Significado | ¿Recuperable? |
|:---|:---|:---|
| **429** | Cuota semanal agotada (`gemma4:31b-cloud`) | Sí: se renueva sola |
| **402** | Requiere suscripción de pago (`minimax-m3:cloud`, `glm-5.1:cloud`) | No sin contratar plan |

> **Aplicación:** al descartar un modelo cloud, registrar **el código exacto**. Un 429 justifica esperar;
> un 402 obliga a decidir entre pagar o excluirlo del estudio de forma permanente.

### L23. Antes de comparar dos fuentes discrepantes, verificar que midan lo mismo
Los datos crudos daban F1=0.3973 para un modelo cloud y la tabla del informe 0.6754. Dos fuentes primarias
concordantes entre sí (el CSV y el agregado del pipeline) apuntaban a que la tabla era la equivocada, y se
llegó a recomendar sustituirla.

Era un error. Las extracciones **habían fallado por cuota** en 6 de 15 casos, y esos ceros arrastraban la
media. Excluyéndolos, el dato crudo daba 0.6622 — prácticamente el valor de la tabla.

> **Aplicación:** cuando dos fuentes discrepan, no basta con contar cuál tiene más respaldo. Hay que
> comprobar **qué mide cada una**. Un promedio contaminado por fallos de infraestructura es
> internamente consistente y perfectamente reproducible, y aun así no mide lo que dice medir.
>
> Señales de alarma que estaban a la vista y no se miraron: `parse_method='failed'`, `retries=2`,
> `recall=0` en filas concretas. **La metadata por fila delata la contaminación antes que el agregado.**

### L24. Un fallo de infraestructura no es un resultado del modelo
El pipeline etiqueta como `failed` tanto un rechazo por cuota (HTTP 429/402) como un fallo de parseo del
modelo. La primera causa es ajena al modelo; la segunda es una limitación real que **sí** debe reportarse.

> **Aplicación:** instrumentar la **causa** del fallo, no solo su existencia. Y publicar siempre la **N
> efectiva** junto a la nominal: una tabla que dice «N=15» cuando 6 extracciones fallaron está informando
> mal aunque cada cifra individual sea correcta.

### L25. Un modelo que no cabe en RAM no se ejecuta «más lento»: no se ejecuta
Se asumió que un modelo de 19 GB en una máquina de 16 GB sería lento pero viable, y que bastaría reducir la
concurrencia. Con 8 workers: 0 respuestas en 26 minutos y 16 GB de swap. Con **1 worker**: mismo resultado.

El paralelismo no era la causa. Con los pesos excediendo la memoria física, **cada paso de inferencia
requiere paginar desde disco**, y eso no mejora al reducir peticiones concurrentes.

> **Aplicación:** la regla operativa no es «reducir workers si va lento», sino **«el modelo debe caber en
> RAM, con margen para el KV-cache»**. Si `tamaño_modelo > RAM_física × 0.7`, ese modelo no pertenece al
> plan de evaluación de esa máquina. Comprobarlo *antes* de incluirlo, no después de perder horas.
>
> Señal diagnóstica inequívoca: `llama-server` con **CPU baja (~30%) y swap alto**. Si estuviera calculando,
> la CPU estaría al máximo; una CPU baja con swap alto significa que espera disco.

### L26. Verificar los supuestos operativos antes de planificar alrededor de ellos
Se dio por hecho que `ollama signin` reiniciaría el daemon y por tanto cortaría el benchmark en curso, y se
llegó a plantear al autor una disyuntiva entre autenticar o preservar la corrida.

**Era falso.** El daemon siguió con 2 días y 11 h de uptime tras el signin. La disyuntiva no existía.

> **Aplicación:** antes de trasladar al usuario una decisión incómoda basada en un supuesto técnico,
> **comprobar el supuesto**. Aquí bastaba un `ps -o lstart` sobre el proceso.

### L27. Un modelo irreproducible no pertenece a un benchmark, por buenos que parezcan sus números
`minimax-m3:cloud` figuraba con F1 = 0.6321, una cifra intermedia y nada sospechosa. Detrás había **9 de 15
extracciones fallidas** y una barrera de plan de pago que impide volver a medirlo con **ninguna** de las tres
cuentas disponibles.

Lo decisivo no fue el valor, sino la **irreproducibilidad**: un resultado que nadie —ni el propio autor—
puede volver a obtener no es evidencia científica, es una anécdota.

> **Aplicación:** al admitir un modelo en un benchmark académico, comprobar antes que sea **reproducible
> por un tercero** con los recursos declarados. Un modelo tras un muro de pago que el autor no mantiene
> introduce una dependencia externa que caduca — y cuando caduca, el resultado queda huérfano.
>
> Distinción útil que emergió aquí: **HTTP 429 (cuota) es temporal y se recupera; HTTP 402 (plan) es
> estructural y no**. La primera justifica esperar; la segunda, retirar el modelo.

### L28. Al retirar un elemento, separar la declaración del mecanismo
Retirar `minimax-m3:cloud` no significaba borrar todas sus apariciones. El patrón `"minimax"` de
`is_cloud_model()` no es una declaración del modelo: es **lógica de enrutamiento genérica** que detecta
cualquier modelo remoto con ese nombre. Eliminarlo habría roto el enrutamiento sin que ningún test lo
delatara.

> **Aplicación:** ante un «elimínalo de todas partes», clasificar cada aparición antes de tocarla:
> *declaración* (fuera), *mecanismo* (se queda), *registro histórico* (se conserva, documenta el porqué).
> Un `sed` global sobre el nombre habría hecho las tres cosas indistintamente.

### L29. «Regenerable» no es lo mismo que «reproducible»
Los diccionarios del RAG se excluyeron del repositorio porque existían scripts que los generaban. El
razonamiento parecía sólido y era falso: los scripts leen de **fuentes vivas** —la lista de sanciones OFAC
cambia cada pocos días, y tres repos apuntan a `master`— sin fijar fecha ni commit.

Un artefacto es *regenerable* si el script existe. Es *reproducible* solo si el script, **ejecutado hoy,
produce lo mismo que produjo entonces**. No es la misma propiedad, y confundirlas casi corrompe los
resultados de otro equipo.

> **Aplicación:** antes de excluir algo de git por «se puede regenerar», mirad **de dónde lee el
> generador**. Si la fuente es una URL sin pin de versión, el artefacto es un **snapshot** y hay que
> versionarlo, por grande que sea. 1,8 MB es un precio irrisorio frente a un experimento irrepetible.
>
> Señal de alarma: un archivo generado **sin metadata de procedencia**. Si no dice de dónde salió ni
> cuándo, nadie podrá saber después si el que tiene delante es el mismo que se usó.

### L30. Una instrucción bienintencionada puede ser el vector del error
El encargo al equipo remoto les decía que regenerasen los diccionarios. Era una instrucción útil en
apariencia —evitaba pedirles archivos que no estaban en el repo— y habría corrompido sus resultados en
silencio.

El fallo no estuvo en la ejecución sino en el **supuesto no verificado** que había detrás: que regenerar
equivalía a obtener lo mismo.

> **Aplicación:** cuando redactéis instrucciones para otros, marcad qué pasos descansan en supuestos que no
> habéis comprobado. Los pasos que dicen «generad», «descargad» o «reinstalad» son los candidatos: todos
> presuponen que el resultado será idéntico al original.

### L31. Una métrica agregada no distingue «modelo malo» de «arnés roto»
Un F1 de 0,0987 se interpretó primero como una limitación del modelo. Era un bug del arnés: el modelo
extraía correctamente, pero su respuesta nunca llegaba al pipeline.

Tres señales lo delataban, y ninguna estaba en el F1:

1. **Precisión de 0,93 en un modelo «malo»** — sospechoso. Era el caso degenerado: con el *scorer* de
   entonces, con `tp=0` y `fp=0` la precisión se definía como 1,0. **Un modelo que no extraía nada tenía
   precisión perfecta.** *(Corregido el 2026-09-06 en `src/evaluator.py`, commit `7a6c19f`: el default micro
   es hoy 0,0 y solo vale 1,0 si `tp+fp+fn == 0`. La lección sigue vigente: la métrica agregada no distingue
   el modelo malo del arnés roto.)*
2. **`tokens_per_sec` × latencia ≈ 24 000 tokens generados**, más que modelos que sí funcionaban. El modelo
   estaba trabajando; los tokens iban a otro sitio.
3. **Cero errores HTTP y cero reintentos** — no era la red.

> **Aplicación:** ante una métrica anómala, mirad la **metadata por fila** antes de interpretarla:
> `parse_method`, `retries`, `recall=0`, tokens generados. El agregado dice *cuánto*; la metadata dice
> *por qué*. Y desconfiad de una precisión alta acompañada de recall ínfimo: casi siempre es el caso
> degenerado disfrazado de virtud.

### L32. Un parámetro en el sitio equivocado falla en silencio
`think` es parámetro de primer nivel de `Client.chat()`, pero el código lo ponía dentro de `options`.
Ollama **ignora las claves desconocidas sin avisar**, así que el modo thinking de Qwen3 nunca se activó —
y el código, los logs y la documentación afirmaban lo contrario durante meses.

> **Aplicación:** cuando una opción de una API externa «no parece hacer nada», verificad su **firma real**
> (`inspect.signature`) antes de asumir que el efecto es sutil. Las APIs que aceptan diccionarios de
> opciones arbitrarias no validan las claves: un error de ubicación no produce excepción, produce un
> comportamiento silenciosamente distinto del declarado.

### L33. Auditar también las conclusiones que salieron bien
Tras descubrir que el F1 anómalo de un modelo era un bug del arnés y no una limitación del modelo, el autor
pidió aplicar el mismo escrutinio a las recomendaciones sobre los modelos *cloud* — que hasta entonces
nadie había cuestionado porque «habían salido bien».

La auditoría confirmó lo esencial (el F1 de 0,6699 se sostiene; los fallos no eran del bug de thinking) pero
**encontró una justificación incorrecta**: se había atribuido la retirada de un modelo al plan de pago,
cuando el log mostraba 140 rechazos por **cuota** y solo 1 por plan. La decisión era correcta; el motivo
declarado, no.

> **Aplicación:** revisar solo lo que falló deja intactas las conclusiones que se apoyan en razonamientos
> igual de frágiles pero cuyo resultado casualmente coincidió. Cuando un método de verificación descubre un
> error, **conviene pasarlo por lo que ya se daba por bueno**, no solo por lo pendiente.

### L34. Latencia y tokens distinguen el fallo de red del fallo del arnés
Dos causas producen la misma señal en `parse_method='failed'`, y se separan mirando otras dos columnas:

| Señal | Latencia | Tokens generados | Causa |
|:---|:---|:---|:---|
| Rechazo de infraestructura (429/402/red) | **0 s** | **0** | La petición nunca obtuvo respuesta |
| Arnés perdiendo la respuesta (bug thinking) | **alta** | **miles** | El modelo trabajó; el pipeline no leyó su salida |

> **Aplicación:** ante un lote de extracciones fallidas, mirar `latency_sec` y `tokens_per_sec` antes de
> concluir la causa. Un `failed` con latencia 0 y otro con latencia 1800 s son problemas opuestos y exigen
> arreglos opuestos: uno se resuelve esperando o pagando, el otro tocando el código.

### L35. Un filtro `if valor` descarta los ceros en silencio
Al analizar los resultados del equipo remoto se reportó un F1 de 0,6302 para un modelo. **El valor real era
0,2731.** La causa: el filtro `[float(x['f1']) for x in v if x.get('f1')]`.

En un checkpoint JSON los valores son tipos nativos, y **`0.0` es *falsy*** en Python. El filtro eliminaba
todas las filas con F1 cero —las 66 fallidas— y promediaba solo las 54 buenas, inflando el resultado en más
del doble.

El mismo código sobre un CSV **no** habría fallado: `csv.DictReader` devuelve cadenas, y `"0.0"` es truthy.
El bug solo aparece al leer JSON.

> **Aplicación:** para filtrar valores ausentes usad `if x.get('k') is not None`, nunca `if x.get('k')`.
> Y como control de sanidad: **el número de filas promediadas debe coincidir con el de filas del grupo**.
> Si `len(f1) != len(v)`, algo se descartó.
>
> Es especialmente insidioso porque el resultado inflado **parece plausible**: 0,63 era una cifra creíble
> para ese modelo, y solo saltó al no cuadrar con las 66 filas en cero que la propia tabla mostraba.

### L36. Comparar una tasa sin comparar su efecto lleva a conclusiones opuestas
Se señaló que `nuextract` tenía «109 de 120 fallback, casi tanto como `gemma4:12b-mlx`», sugiriendo la misma
anomalía. La tasa era comparable; **el efecto, opuesto**:

| Modelo | `fallback` | recall = 0 entre ellos | F1 de esas filas |
|:---|--:|--:|--:|
| `nuextract` | 109 | 2 | 0,4459 |
| `gemma4:12b-mlx` | 70 | 66 | 0,0472 |

En uno el respaldo **rescata** el contenido; en el otro no rescata nada. Una es una ruta de parseo que
funciona, la otra un fallo encubierto.

> **Aplicación:** una tasa de eventos no es un diagnóstico. Antes de equiparar dos síntomas por su
> frecuencia, comprobad **qué consecuencia tiene cada uno sobre el resultado**. Aquí bastaba cruzar
> `parse_method` con `recall` — dos columnas que ya estaban en los datos.

### L37. Terminología: «variantes de prompts», nunca «ablación»
**Contexto.** El estudio que cruza idioma (inglés/español) × estrategia (zero-shot/few-shot) sobre
`gemma4:latest` se denominó en borradores «estudio de ablación». El autor fijó el término correcto.

**Regla.** En informes, reportes, código y documentación usar **«Test de Variación de los prompts»** o
**«Análisis de Variantes de Prompts»**. **No** usar «ablación» ni «estudio de ablación», aunque el diseño
factorial 2×2 reciba ese nombre en parte de la literatura de ML.

> **Aplicación:** revisar toda mención antes de publicar; el término preferido del autor prevalece sobre la
> convención de la literatura.

### L38. Los logs deben llevar fecha/hora y conservarse
**Regla (decisión del autor, 2026-09-07).** Todo log de corrida debe:
1. Incluir en el **archivo** la **fecha y hora de inicio** (y zona), en una cabecera o en el nombre
   (`run_YYYYmmdd_HHMMSS.log`).
2. Ser **detallado** (modelos, corpus, N, modo, parámetros).
3. **Conservarse** —idealmente en carpetas fechadas— y **commitearse** en el futuro (no descartarse).

> **Aplicación:** el re-run N=30 ya usa `results/n30_rerun_REMOTO/run_<timestamp>.log` con cabecera fechada.
> Extender la práctica a todas las corridas.

### L39. Un corpus corrupto de forma coherente no sesga a todos por igual: penaliza a quien lo corrige
**Registrado:** 2026-09-07 16:35 (UTC−3) · Ver `FINDINGS.md §F46` y **§F48**.

Se encontró mojibake en las entidades de referencia del corpus N=120 —`JosÃ© Bono` guardado donde el nombre
real es **`José Bono`**— y la lectura inmediata fue: «afecta a todos los modelos por igual, deprime el recall
un 4,7 % y no altera el ranking». **Las dos mitades de esa frase eran falsas.**

Faltaba una comprobación: **mirar si el defecto estaba también en la entrada**. Lo estaba —87 % de los textos—
y de forma **coherente**: las 283 entidades corruptas del gold aparecen **tal cual** en el texto, ninguna
aparece corregida. El corpus es internamente consistente, así que **el modelo que transcribe literalmente
acierta** y **el que normaliza a español correcto falla**. Medido: el Δ entre registros con y sin mojibake va
de **−0.0695** a **+0.0914** según el modelo, un rango de ~16 puntos.

**La regla.** Antes de aceptar que un defecto del corpus produce un sesgo uniforme, verificar si el defecto
alcanza a la entrada y no solo a la referencia. Si alcanza a ambas y de forma coherente, el sesgo **no es
uniforme**: recompensa una conducta del modelo y castiga la contraria.

**Corolario sobre cómo repararlo.** Arreglar solo el gold invierte la injusticia en vez de eliminarla. Lo
correcto es **normalizar ambos lados al comparar**: aplicar la reparación al gold *y* a la extracción antes del
*fuzzy matching* —`rapidfuzz.fuzz.ratio` con umbral 85, una similitud de **caracteres** (Indel/Levenshtein sin
sustituciones), no de tokens; ver `FINDINGS.md §F46`—, de modo que el resultado no dependa de la codificación.

**Corolario sobre el alcance de un arreglo.** Si se corrige el gold para una sola re-corrida, ese modelo queda
puntuado con una vara distinta de la del resto: es el mismo error que las dos convenciones de puntuación y los
dos regímenes de *thinking* que ya costó unificar. **Una re-corrida aislada debe usar exactamente el mismo
corpus y el mismo evaluador que las demás.**

> **Aplicación:** la re-ejecución de `gpt-oss:20b` se hace con `num_predict` ampliado pero **sin tocar el gold
> ni el evaluador**, para que el único cambio sea el que se quiere aislar.

### L40. Dos agentes pueden asignar el mismo identificador a hallazgos distintos
**Registrado:** 2026-09-07 16:35 (UTC−3).

El equipo remoto publicó `FINDINGS.md §F46` (mojibake) a las 14:01 y el equipo principal registró un hallazgo
**distinto** con el mismo número (degeneración de `gpt-oss`) poco después, sin haber hecho `pull` entre medias.
La colisión se detectó al integrar y se resolvió renumerando el segundo a **§F47**, con nota explícita.

**La regla.** Antes de asignar un identificador correlativo en un documento compartido —hallazgo, aprendizaje,
tarea— hacer `pull` y releer el fichero. Si aparece una colisión, **renumera el que llegó después y deja
constancia**; nunca reutilices el número ni renumeres el ajeno.

### L41. Persistir los estudios completos (zip versionado) y las extracciones crudas

> *Renumerada de L39 a L41 el 2026-09-08: el identificador L39 ya estaba ocupado por la lección sobre el
> corpus corrupto (línea 455). Es la tercera colisión de este tipo y la segunda **después** de escribir L40,
> que advierte precisamente de ella; señal de que la regla necesita una comprobación automática y no solo
> un recordatorio. No se altera el contenido de ninguna de las dos.*
**Contexto.** El corpus N=120 tuvo que catalogarse para re-inferir por el mojibake (F46) porque **las
extracciones crudas por registro no se persistieron** (solo `tp/fp/fn`), y `results/` está gitignored, así
que ni los CSV sobrevivían en git. La corrida N=30 de julio se perdió directamente por sobrescritura.

**Regla (decisión del autor, 2026-09-07).**
1. **Guardar cada estudio completo como `.zip` versionado en el repo** (NO gitignored): CSV, detailed, summary,
   statistical_report y logs fechados.
2. **Persistir las extracciones crudas por registro** (el JSON extraído del modelo), no solo las métricas
   agregadas: permite re-puntuar ante cualquier corrección (scorer, gold/mojibake) **sin re-inferir**.

> **Aplicación:** al cierre de cada estudio, empaquetar `results/<estudio>/` en
> `remote_48g/estudio_<fecha>.zip` y commitearlo. Ver `FINDINGS.md §F46`.

---

## 8. Lecciones de la segunda pasada de revisión (2026-09-08)

### L42. Una segunda pasada solo vale si no sabe lo que encontró la primera

Los seis auditores de la revisión global recibieron una instrucción explícita: *«esta es una segunda pasada
independiente; deliberadamente no se te dice qué encontró la primera»*. Encontraron 172 hallazgos, 61 graves,
y entre ellos los tres que bloquean la entrega — ninguno de los cuales había aparecido en la primera ronda,
que se había centrado en la bibliografía. Si se les hubiera entregado el informe anterior, habrían dedicado
el esfuerzo a confirmarlo.

> **Aplicación:** al encargar una verificación independiente, ocultar los resultados previos y decirlo en el
> prompt. Y valorar por encima de todo la **contradicción**: cuando dos auditores discrepan sobre el mismo
> punto, ahí hay algo que ninguno de los dos ha entendido del todo, y es lo primero que hay que ir a mirar.

### L43. Reescribir el historial de git no borra un secreto de GitHub

`git filter-repo` purgó la clave de API de los 20 commits afectados y el force-push dejó el remoto limpio.
Pero al comprobarlo después, el commit antiguo seguía respondiendo HTTP 200 en la API y su versión del
fichero **todavía contenía la clave en claro**. Los objetos quedan sin referencia pero GitHub los sigue
sirviendo por SHA directo, y no ejecuta el recolector por iniciativa propia.

> **Aplicación:** la reescritura es mitigación, no remedio. El remedio es **revocar la credencial**, y hay que
> hacerlo primero. Después, pedir a GitHub Support la purga de objetos inalcanzables. Y nunca publicar un
> repositorio que tuvo un secreto sin haber completado los dos pasos: publicar convierte una clave
> recuperable-si-conoces-el-SHA en una clave indexable.

### L44. Lo que el prompt pide y lo que el corpus anota tienen que coincidir

El 65 % de los falsos positivos de todo el estudio provenían de una categoría, `Locations`, que los cuatro
prompts ordenaban extraer y que **ningún corpus anotaba**. El evaluador la puntuaba igual, de modo que cada
localización correctamente identificada contaba como error. Nadie lo advirtió en dos meses porque las cifras
eran internamente consistentes: bajas, pero coherentes entre sí.

> **Aplicación:** antes de dar por buena una métrica, comprobar que **cada categoría puntuada existe en la
> anotación de referencia**. El indicador barato es `tp + fn` agregado por categoría: si esa suma vale cero
> mientras `fp`
> crece, esa categoría está puntuando contra el vacío. Y una cifra baja pero estable no prueba que la
> medición sea correcta; prueba que el defecto es sistemático.

### L45. Con varias corridas del mismo experimento, se declaran todas

El informe presentaba +10,40 puntos por el prompt en español. Había tres corridas: esa, otra con +3,11 sobre
el mismo corpus y modelo, y una tercera sobre el corpus ocho veces mayor con **−0,43 puntos y p=0,9328**.
Ninguna de las dos últimas se mencionaba. No hubo intención de seleccionar, pero el resultado es
indistinguible de haberlo hecho, y eso es lo que un tribunal juzga.

> **Aplicación:** al escribir una cifra, buscar en `results/` si hay más corridas del mismo experimento antes
> de citarla. Si las hay, declararlas y explicar cuál se toma como referencia y por qué. La política aditiva
> del proyecto ya obliga a conservarlas; lo que faltaba era obligarse a **mencionarlas**.

### L46. Un defecto de datos puede tener la solución en los datos mismos

El corpus del estudio perdía las localizaciones que CoNLL-2002 sí anota, y el equipo remoto planteó tres
salidas: recuperar el script de construcción perdido, renunciar a la categoría, o pagar anotación experta.
Las tres asumían que la correspondencia entre el corpus y su fuente se había perdido con el script.

No era así. **El texto de cada artículo es su propia clave.** Emparejando por texto se recuperaron 482
localizaciones sin necesitar el script, y el resto se anotó a mano en una tarde: quince artículos y treinta
párrafos cortos.

> **Aplicación:** antes de aceptar que un dato es irrecuperable, preguntar qué campo del propio dato podría
> servir de clave. Y antes de pedir anotación experta, medir cuánto queda realmente por anotar: aquí eran
> 45 documentos, no un corpus.

**Corolario sobre la normalización.** El emparejamiento por texto **falló al primer intento**, con 1 de 120
coincidencias, y estuve a punto de concluir que la vía no servía. La causa era que un lado tenía la
codificación reparada y el otro no. Normalizando ambos, 105 de 120. Cuando un emparejamiento por contenido
da casi cero, la hipótesis más probable no es que el contenido difiera, sino que **difiera su
representación**.

### L47. Un fichero vacío no rompe nada, y por eso sobrevive

Cuatro documentos del proyecto llevaban dos meses a cero bytes, dos de ellos de hitos ya entregados
(`§F59`). Ninguna comprobación los detectó porque un fichero vacío se comporta como un fichero: existe, se
abre, se lee, y `git status` no dice nada de él. La ausencia de contenido no genera ningún síntoma.

La lección general es que **las comprobaciones de existencia son más débiles de lo que parecen**. Comprobar
que una ruta existe no comprueba que tenga algo dentro, igual que comprobar que una tabla tiene una leyenda
no comprueba que la leyenda describa esa tabla, y que comprobar que una URL está escrita no comprueba que
responda. En los tres casos el proyecto ya se llevó un susto.

El corolario práctico es barato: cuando una comprobación mecánica verifique que algo está presente, que
verifique además que **no está vacío**.

### L48. Una regla acertada con una justificación falsa acaba levantándose

El `.gitignore` ignoraba los duplicados de macOS diciendo que «son copias byte a byte». La regla acierta
—esos ficheros no deben entrar—, pero la razón era falsa: 23 de 78 difieren, y varios son instantáneas
anteriores a la retirada de los modelos excluidos (`§F60`).

Importa porque una justificación falsa es frágil de una forma peculiar: el día que alguien compruebe la
afirmación y vea que no se sostiene, concluirá que la regla sobra y la quitará, reintroduciendo justo lo que
la regla evitaba. **Una regla se documenta con la razón por la que se cumple, no con la primera razón que
pareció explicarla.**

### L49. Fusionar corridas hereda sus diferencias de configuración, y nadie las mira

El consolidado del estudio une ocho corridas. Cada una había pasado la comprobación de protocolo —que sus
nueve parámetros fueran los de la corrida de referencia—, pero esa comprobación se aplicaba **dentro** de
cada corrida, nunca **entre** ellas. El resultado es que `gpt-oss:20b` acabó publicado con el doble de
presupuesto de salida que los otros doce modelos sin que ninguna verificación lo advirtiera (`§F61.bis`).

El patrón es general y vale para cualquier agregación: **una propiedad que se comprueba por parte no queda
comprobada en el todo**. Ocho ficheros internamente coherentes producen un conjunto que puede no serlo, y la
coherencia de cada parte da además una falsa sensación de haberlo verificado.

La comprobación que faltaba es barata: leer los `run_config.json` de todas las fuentes de un consolidado y
exigir que los parámetros que afectan a la medición sean **idénticos entre sí**, no solo correctos por
separado. Cuando no puedan serlo, declararlo en el informe como reserva de comparabilidad.

Emparenta con `§L47`: comprobar que algo existe no es comprobar que tenga contenido, y comprobar cada parte
no es comprobar el conjunto. Las dos son la misma debilidad, que la comprobación mire menos de lo que su
nombre promete.

### L50. El fichero crudo y la métrica publicada no son el mismo número, y el crudo es el que está a mano

La re-corrida guarda 120 registros por corrida en el CSV y publica la métrica sobre 113, porque siete
artículos del corpus son a la vez ejemplares de la base de conocimientos y contaminan el conjunto de prueba
(`§F65`). Las dos cosas son correctas: el crudo atestigua, el resumen afirma.

El problema es que **el crudo es el que invita a promediarlo**. Está en formato tabular, se lee con dos
líneas y da un número plausible. El resumen exige abrir otro fichero y confiar en que su convención sea la
que declara el informe. Al informar las primeras cifras se promedió el crudo, y el resultado infla
justamente el efecto que el trabajo mide.

La regla es corta: **antes de citar una métrica agregada, comprobar sobre cuántos registros se calculó y que
ese número sea el que corresponde.** `total_records` está en el resumen precisamente para eso.

Emparenta con `§L47` y `§L49`: las tres son la misma debilidad, que una comprobación mire menos de lo que su
nombre promete. Aquí lo que se mira de menos es *sobre qué población* se calculó el número.

### L51. Lo que no se versiona no existe, y el detalle por registro es lo primero que se echa de menos

Los `detailed_results.json` estaban ignorados en git. Nadie lo decidió por una razón vigente: quedó así, y
el coste apareció tres veces en forma de «esa cifra no se puede recalcular, hay que volver a inferir»
(`§F67`).

El patrón se repite con los `benchmark.log`, que también estuvieron ignorados hasta que se perdieron líneas
de dos de ellos y solo se pudieron reconstruir las de uno. **Dos veces el mismo defecto, sobre dos ficheros
distintos, y la regla que se escribió la primera vez no alcanzó al segundo.**

Lo que distingue a estos ficheros no es su tamaño ni su formato, sino **qué se pierde si desaparecen**. Un
agregado se puede volver a calcular a partir del detalle; el detalle solo se puede volver a obtener
re-ejecutando el experimento, que en este proyecto son decenas de horas de máquina. La pregunta correcta
antes de ignorar algo no es «¿ocupa mucho?» sino **«¿podría reconstruirlo si mañana no estuviera?»**.

Corolario operativo: cuando se escriba una regla de conservación para una clase de artefacto, revisar en el
mismo turno qué **otras** clases cumplen el mismo criterio. La regla de los logs se escribió sin mirar si
había algo más en la misma situación, y lo había.

### L52. Editar JSON por sustitución de texto lo rompe, y nadie se entera

El barrido que retiró los nombres de los modelos excluidos borró la cadena del nombre allí donde aparecía,
en lugar de cargar el fichero, modificar la estructura y volcarla. El resultado son dos ficheros con
`"model":` colgando sin valor en 240 registros y un objeto al que le falta una clave (`§F70`).

Lo que hace que este error sea caro no es la edición en sí, sino que **el daño es invisible**. Un JSON roto
pesa lo mismo, se abre igual, aparece en un `ls` y pasa cualquier comprobación de existencia. Solo se
manifiesta cuando alguien intenta cargarlo, y en este caso nadie lo intentó durante un día entero porque los
ficheros estaban además ignorados en git.

Dos reglas, y la segunda importa más:

- **Un fichero estructurado se edita cargándolo y volcándolo**, nunca por sustitución de texto. Si hay que
  hacerlo por texto, se valida después.
- **Después de cualquier edición masiva de datos, parsear todo lo tocado.** No es una comprobación de la
  edición, es una comprobación del fichero: cuesta un segundo por fichero y cubre la clase entera.

Es hermana de `§L47` —un fichero vacío no da síntoma— y de `§L51` —lo que no se versiona no existe—. Las
tres describen lo mismo desde ángulos distintos: **los defectos que sobreviven son los que no producen
ningún síntoma**, y por eso hay que ir a buscarlos en vez de esperar a que aparezcan.

### L53. Las horas de un documento de coordinación se leen del reloj, no se estiman

Las veinte entradas que escribí hoy en `CURRENT-TASKS.md` llevaban horas inventadas. No al azar: fui
incrementando una hora plausible en cada anotación, de modo que la deriva **creció de forma monótona** desde
11 minutos hasta **5 horas y 38**, y la última entrada aparecía fechada al día siguiente. Corregidas las
veinte contra la marca de tiempo del commit que introdujo cada una.

Lo grave no es la imprecisión, es **dónde** estaba. `CURRENT-TASKS.md` existe para que varios agentes que
trabajan a la vez sepan quién hizo qué y cuándo, y este proyecto ya ha tenido incidentes por edición
concurrente. Una entrada fechada con dos horas de adelanto sitúa un trabajo después de otro que en realidad
lo precedió, y hace irreconstruible la secuencia justo cuando hace falta reconstruirla.

El error tiene además una forma reconocible: **una serie plausible es más creíble que un valor absurdo, y por
eso sobrevive**. Nadie mira dos veces un «21:35» entre un «21:10» y un «22:00». Lo mismo pasó con los tres
recuentos de guiones y negritas que dieron 19, 28 y 31 sobre el mismo texto: cada uno era plausible por
separado.

La regla es trivial y la omití veinte veces seguidas: **si hay que escribir una hora, se pregunta al
sistema.** Y su corolario, que vale para cualquier dato que se anota de pasada: si un valor se puede
obtener, no se estima.

### L54. Una explicación plausible escrita antes de comprobarla es una hipótesis disfrazada de hallazgo

Al ver que cinco modelos rehechos mostraban efectos muy parecidos, escribí en `§F68.bis` que la dispersión
anterior venía de cuántas localizaciones emitía cada modelo. Sonaba bien, encajaba con el mecanismo conocido
y explicaba el dato. Seis minutos después la comprobé con datos que ya estaban en el repositorio y resultó
falsa: excluir las localizaciones del cómputo **aumenta** la dispersión en lugar de reducirla (`§F68.ter`).

Peor todavía: la «convergencia» que pretendía explicar se medía sobre cinco modelos que **excluyen los dos
efectos más grandes del estudio**, ambos pendientes de rehacer. Estaba explicando un artefacto de muestreo.

Lo que falló no fue el razonamiento sino el **orden**. La prueba costó dos minutos y los datos llevaban horas
en el disco. Escribir primero y comprobar después convierte una hipótesis en un hallazgo aparente que otros
—o yo mismo mañana— citarán como establecido.

La regla, para cuando aparezca un patrón atractivo: **antes de escribir por qué ocurre algo, comprobar si
ocurre.** Y con muestras parciales, mirar explícitamente **qué queda fuera** antes de describir lo que se ve;
aquí lo que quedaba fuera eran justamente los dos casos que definían el fenómeno.

Emparenta con `§L53` —una serie plausible sobrevive porque nadie la mira dos veces— y con la nota de método
de `§F44`: un hallazgo de auditoría es una hipótesis, no un hecho.

### L55. El recuento en prosa se desvía del dato, y siempre en cifras pequeñas

El repaso que abrió `§L54` ha encontrado hoy **cinco** afirmaciones numéricas propias que no reproducían: una
explicación mecanicista falsa, un «solo en modo KB RAG» que ignoraba un contraejemplo, dos decimales citados
de un fichero sin comprobarlos, un «23 ficheros» que eran 22, un «nueve de los doce» que eran ocho y un
«cuatro de cuatro» que era tres de cuatro.

Ninguna cambió una conclusión. Todas eran **cifras pequeñas escritas de memoria** mientras la atención estaba
en el argumento: cuántos ficheros, cuántos de cuántos, en qué modo. Es donde el cuidado se relaja, porque el
número parece un detalle de la frase y no un dato.

Lo que las hace peligrosas es que **son verificables y por tanto verificables en la defensa**. Un tribunal
que abra el repositorio y cuente doce ficheros donde el texto dice trece no concluye que hubo un desliz:
concluye que las cifras del trabajo no se comprueban.

La regla operativa que se deriva: **cuando una frase contiene un recuento, obtenerlo en el mismo turno en que
se escribe**, aunque parezca obvio. Y al terminar una tanda de documentación, repasar los recuentos contra
los datos, que es lo que hizo aparecer estos cinco.

### L56. Un criterio de medida que cambia entre dos llamadas produce una cifra falsa y plausible

Al calcular cuánto había crecido el cuerpo del informe usé dos veces la misma idea —«contar palabras hasta
donde empiezan los anexos»— con dos detectores ligeramente distintos. Uno reconocía `### Anexo A` y el otro
solo `## Anexos`. En la versión antigua, que usaba el primer formato, el segundo detector no encontró
frontera y contó el documento entero como cuerpo.

El resultado fue que el cuerpo había **encogido 2 673 palabras** cuando en realidad había **crecido 2 084**.
La cifra tenía el signo contrario y era perfectamente creíble: encajaba con la idea de que las correcciones
del día habían sido de precisión y no de adición.

Lo que falla aquí no es el conteo sino **la frontera**. Cualquier medida que dependa de dónde se corta un
documento —cuerpo frente a anexos, capítulo frente a capítulo, corrida frente a corrida— hereda la fragilidad
de ese corte, y dos implementaciones «equivalentes» del mismo corte no lo son.

La regla: **cuando una medida dependa de una frontera, escribir la frontera una vez y reutilizarla**, en
lugar de reimplementarla en cada cálculo. Y si el resultado sorprende, sospechar de la frontera antes que del
dato.

Es hermana de `§L47` y `§L52`: las tres describen medidas que fallan sin dar ningún síntoma, porque devuelven
un número en lugar de un error.

---

## §L57 — Una comprobación cuyo valor «bueno» puede producirse por avería necesita su control en la misma orden

**2026-09-08, 23:0x.** La rutina de seguimiento incluye una comprobación de la purga de GitHub: si el commit
que contiene la clave de API deja de responder, la purga se ha completado. Llevaba todo el día devolviendo
HTTP 200, es decir, sin purgar. Esta vez devolvió **404**, y durante unos segundos eso se leyó como que el
objeto había desaparecido.

No había desaparecido. La orden usaba `eahumadaFID/…` como propietario del repositorio, cuando el propietario
es `eahumada/…`. Un repositorio inexistente devuelve 404 para todo. El comprobante correcto, ejecutado después
con el token y la URL que registra `SEGURIDAD-CLAVE-GOOGLE-20260908.md`, devolvió **HTTP 200 y la clave en
claro**: la situación no había cambiado en absoluto.

**Lo que lo destapó** fue pedir el control en la misma orden: además del commit purgado, la raíz del
repositorio y un commit vigente de `HEAD`. Los tres dieron 404. Un commit vigente que no responde no es una
purga, es una URL rota, y ahí se acabó la interpretación optimista.

**La lección.** El 404 era simultáneamente el resultado esperado del éxito y el síntoma de la avería más
común de esa orden: escribir mal la URL. Cuando el valor que indica éxito coincide con el que produce un
fallo de la propia comprobación, la comprobación no distingue nada por sí sola, y leerla como buena noticia
es lo que el sesgo hace por defecto.

- **Toda comprobación cuyo valor bueno sea «algo ya no está» lleva su control adjunto**: pedir en la misma
  orden algo que *sí debe seguir estando*. Si el control también falla, el resultado no es un hallazgo, es
  una avería.
- **Un resultado que mejora sin causa conocida se verifica antes de celebrarse.** Nadie ejecutó nada entre
  las dos mediciones. Un cambio de estado sin causa es primero sospechoso y solo después bueno.
- Esto es lo mismo que `[[L47]]` sobre las comprobaciones vacías, aplicado un paso más allá: allí una
  comprobación que no examinaba nada se marcaba como superada; aquí una que examina el objeto equivocado
  devuelve el valor del éxito. En ambos casos el defecto no está en el dato, sino en que la orden no puede
  distinguir entre haber acertado y no haber mirado.

**Aplicado.** La comprobación documentada en `SEGURIDAD-CLAVE-GOOGLE-20260908.md` se amplía con su control, y
declara explícitamente que un 404 anónimo no significa nada: el repositorio es privado y responde 404 a
cualquiera sin credenciales, incluida su propia raíz.

---

## §L58 — `git branch -f` no puede mover la rama activa, y no dice nada al no hacerlo

**2026-09-08, tarde y noche.** Tras cada commit se ejecutaba esta secuencia para mantener las tres ramas
alineadas:

```sh
for b in sesion/revision-final-20260908 backup/revision-final-20260908; do
  git branch -f "$b" main >/dev/null 2>&1
done
git push -q origin main sesion/... backup/... --force-with-lease
```

Y después se informaba «ramas en `<sha>`, todo empujado». **No era exacto.** La rama activa era
`sesion/revision-final-20260908`, de modo que los commits avanzaban *esa* rama y `main` se quedaba donde
estaba. La orden `git branch -f sesion/... main` habría retrocedido la rama de sesión hasta `main`
—destruyendo el trabajo— pero git **se niega a mover la rama que está activa**, y ese rechazo iba directo a
`/dev/null` por el `>/dev/null 2>&1`. El `push` entonces empujaba `main` y `backup` en su estado viejo, sin
error, porque no había nada que empujar.

**Resultado:** trece commits vivían solo en la rama de sesión. No se perdió nada —estaban comprometidos y
empujados ahí— pero `main` llevaba cinco horas de retraso mientras el informe de estado decía lo contrario.

**Lo que falló, en orden de importancia:**

1. **Silenciar la salida de una orden que puede negarse a actuar.** El `2>&1` de conveniencia convirtió un
   rechazo explícito de git en nada. Si una orden puede fallar de forma legítima, su error se lee.
2. **Informar del estado sin comprobarlo.** «Todo empujado» se decía a partir del código de salida del
   `push`, que era cero porque no tenía nada que hacer. La comprobación correcta es
   `git rev-list --count origin/<rama>..<rama>` **por cada rama**, y compararla con cero.
3. **Usar `git branch -f` teniendo una rama activa.** Para adelantar otra rama a la actual, la dirección es
   la contraria: `git branch -f main <rama-activa>`, que sí funciona porque `main` no está activa.

**La comprobación que lo destapa** cabe en una línea y ahora cierra cada tanda:

```sh
for r in main sesion/... backup/...; do
  echo "$r: $(git rev-list --count origin/$r..$r) por empujar"
done
```

Es el mismo patrón de `[[L57]]`: una orden cuyo «no hizo nada» es indistinguible de «lo hizo bien» si nadie
mira el resultado. Allí un 404 podía significar éxito o URL rota; aquí un `push` sin error puede significar
sincronizado o nada que empujar.

---

## §L59 — Un recuento no se comprueba por presencia de la palabra

**2026-09-09, 07:1x.** Tras escribir en el índice de defensa que los modelos con mejora significativa eran
«dos» cuando son tres (`FINDINGS §F86`), se amplió la comprobación 24 del verificador para atar las cifras de
la re-corrida a su artefacto. Entre ellas, el recuento de significativos.

La primera versión lo comprobaba como todas las demás: **buscando si «3» o «tres» aparece en el documento**.
Sometida a la mutación exacta del error —cambiar esa frase de «tres» a «dos»— **la comprobación pasó**.

La razón es obvia una vez vista: «tres» aparece muchas veces en ese documento por otros motivos —«tres
comprobaciones», «los tres corpus», «tres advertencias»— de modo que la presencia de la palabra no dice nada
sobre la frase que interesa. La comprobación no verificaba una afirmación: verificaba un vocabulario.

**Corregido** exigiendo que el número aparezca **en la misma oración** que la palabra `significativ`, con una
expresión regular que admite las dos direcciones. Repetida la mutación, ahora falla y nombra el problema.

### Un matiz, y un tropiezo propio al comprobarlo

Al revisar si el verificador tenía más recuentos comprobados por presencia apareció el del post-hoc antiguo,
que usa la forma compuesta «ocho de trece». Mutado, **la comprobación pasó**, y por un momento pareció el
mismo defecto.

No lo era: **la frase aparece dos veces en el documento y la mutación solo cambió una**. Con las dos mutadas,
la comprobación falla y nombra la cifra que falta. La forma compuesta sí ancla, porque «ocho de trece» no
aparece por casualidad. **El fallo era de mi mutación**, no del verificador — y es la segunda vez en esta
revisión que una mutación mal construida produce un falso negativo, después del caso de la bibliografía
en `[[L47]]`.

De ahí una regla para las propias pruebas: **una mutación debe alcanzar todas las apariciones de lo que
altera**, o lo que se está midiendo es cuántas veces se repite el dato, no si la comprobación funciona.

**Y «todas las apariciones» incluye las variantes de formato.** El 2026-09-09, probando la comprobación de
las dos cifras titulares del resumen, se mutó `76,55` en sus siete apariciones y la comprobación **siguió
pasando**: el informe escribe además `76.55` **con punto** dos veces, en las tablas, y el patrón de la
comprobación —`76[.,]55`— admite las dos formas, correctamente. Mutando ambas, falla y nombra las dos cifras.

De modo que en este informe **una cifra se muta en sus dos separadores decimales**: coma en la prosa, punto en
las tablas. Van cinco mutaciones incompletas en esta revisión y las cinco produjeron por un momento la misma
conclusión falsa: «la comprobación no funciona». Ninguna era eso.

Queda además un límite real, menor pero conviene saberlo: una comprobación por presencia se satisface con que
la cifra sobreviva **en algún sitio** del documento. Si una cifra obsoleta aparece dos veces y solo se corrige
una, no salta. En la práctica es tolerable —un dato que envejece suele estar en un sitio— y el remedio, si
alguna vez importa, es comprobar que **todas** las apariciones del patrón coinciden con el artefacto, no que
exista una.

### Lo que generaliza

- **Una cifra decimal distintiva —«0,0879»— sí puede comprobarse por presencia**, porque no aparece por
  casualidad. Un número pequeño en letra o en dígito, **no**.
- **Toda comprobación de recuento necesita anclaje**: el número junto al sustantivo que cuenta, en la misma
  oración. Sin eso comprueba que el documento está escrito en español.
- Y una vez más, **lo destapó la mutación y no la lectura**. El código parecía correcto, era simétrico con las
  demás cifras y pasaba en verde. Es la cuarta vez en dos días que una comprobación escrita hace minutos
  resulta no comprobar nada, y la cuarta que la prueba de mutación lo dice en un segundo. Ver `[[L47]]`,
  `[[L57]]` y `[[L58]]`.

---

## §L60 — Una autoprueba que solo pregunta «¿falla algo?» no dice cuál comprobación protege

**2026-09-09, 07:4x.** `tools/autoprueba_verificador.py` esconde cada artefacto por turno y exige que el
verificador se entere. Pasaba **8 de 8**, y aun así una comprobación estaba ciega.

La razón es que la autoprueba pregunta si **alguna** comprobación falla, no si falla **la que depende de ese
artefacto**. Varios ficheros los leen dos o tres comprobaciones distintas, de modo que basta con que una se
entere para que la autoprueba dé el visto bueno mientras las otras siguen saltándoselo en silencio.

Comprobado: escondiendo `correlacion.json`, la comprobación del índice de defensa bajaba de **13 a 9
elementos** y seguía diciendo **ok**. Lo mismo con el post-hoc y con Friedman, de 13 a 12. La autoprueba no lo
veía porque el artefacto también lo lee la comprobación de la correlación, que sí fallaba.

**Corregido en la comprobación**, no en la autoprueba: las cinco fuentes del índice de defensa se cargan ahora
en un bucle que **declara cada ausencia como fallo** y cuenta cada intento, de modo que el recuento sube de 13
a 18 y ninguna puede desaparecer sin nombre. Verificado por mutación con dos de ellas.

### La regla

- **Un recuento que baja es un síntoma que nadie mira.** Ya lo dijo `[[L47]]` para el caso de cero; aquí baja
  de trece a nueve, que es peor, porque parece un estado normal.
- **Una autoprueba de cobertura debe atribuir**: no basta con «algo falló», hay que saber **qué** falló y que
  sea lo que corresponde. Mientras no lo haga, su «8 de 8» acredita menos de lo que parece.
- Y el corolario incómodo: **esta autoprueba se escribió ayer para detectar exactamente esta clase de
  ceguera**, y era ciega a una variante suya. Ver `[[L57]]`, `[[L58]]` y `[[L59]]` — la familia ya tiene
  cuatro miembros y todos se descubrieron probando, ninguno leyendo.

## §L61 — Encontrar defectos de uno en uno no acredita que no haya más

Tres cifras obsoletas encontradas a mano en el entregable dejaban abierta la única pregunta que importa:
si son las únicas. La respuesta era no — había una cuarta, el `5.33` de la Tabla 4, que ninguna lectura
había visto y que los datos contradicen sin ambigüedad. Apareció al **mecanizar la comparación completa**
en lugar de seguir leyendo. Ver `FINDINGS §F88`.

**La regla:** cuando se encuentran varios defectos del mismo tipo a mano, el paso siguiente no es buscar el
próximo a mano, es **escribir la comprobación que los enumera todos**. Un hallazgo aislado es un dato; una
serie de hallazgos del mismo tipo es la especificación de una herramienta que falta.

**Y la herramienta también necesita su control.** Ésta tuvo dos defectos, y ninguno se habría visto sin
mirar sus resultados con desconfianza:

- Un patrón que parecía específico y no lo era: `<w:t[^>]*>` encaja con `<w:tcPr>`. **Lo delató su propia
  salida**, que imprimía marcado XML donde debía haber texto. Merece la pena imprimir contexto aunque no se
  necesite: es lo que hace visible un extractor roto.
- Una medición plausible que medía otra cosa: contar `dígito SEP dígito` daba 257 números «partidos» donde
  hay 1, porque dos celdas numéricas contiguas encajan con el patrón. **Una cifra plausible no es una cifra
  correcta**, y aquí las dos mediciones difieren en 257 veces.

**Corolario sobre las anclas.** Un ancla textual que parece única suele no serlo. `5.33` estaba tres veces
en el documento y la tercera era `35.33%`: la regla ingenua lo habría convertido en `35.80%`. Antes de
aplicar un reemplazo hay que **contar las ocurrencias y mirarlas una por una**, y cuando el objetivo es una
celda de tabla, anclar en la celda y no en el texto. Es la misma lección que `<w:t[^>]*>`, en otro nivel.

## §L62 — Persistir una cifra no es verificarla

`levene.json` se creó el 2026-09-08 precisamente porque la p publicada «no estaba guardada en ningún
artefacto, de modo que no era verificable sin recalcularla». El artefacto se escribió, la nota se redactó
con cuidado, y **nadie lo volvió a leer**: ningún código lo cargaba y ninguna comprobación lo miraba. Un
cambio en el CSV fusionado lo habría dejado obsoleto en silencio. Ver `FINDINGS §F91`.

**La regla:** persistir una cifra resuelve la trazabilidad y no resuelve la vigencia. Son dos problemas
distintos y el segundo necesita algo que **recalcule** y compare. Cuando se guarda un artefacto para hacer
verificable una cifra, en el mismo commit hay que dejar quien lo verifique; si no, se ha creado una segunda
copia de la cifra, que es una fuente más de divergencia y no una garantía.

**Corolario sobre las dependencias.** Una comprobación que solo corre dentro de un entorno concreto no
corre. `tools/robustez_estadistica.py` moría con un `ModuleNotFoundError` porque scipy solo está en el venv
del proyecto, y un traceback no dice dónde está el intérprete que sí funciona: durante ese tiempo la
herramienta era indistinguible de no existir. Por eso la comprobación de Levene se implementó con la
biblioteca estándar, aun teniendo scipy a mano, y se validó **contra** scipy en lugar de **con** scipy.

## §L63 — Una comprobación que compara contra una constante escrita a mano no comprueba el documento

La comprobación del «dos de los trece» de Tukey contrastaba el delta del artefacto contra un `0.1452`
literal, puesto en el código porque era lo que el informe decía **en el momento de escribirla**. El efecto
es que la comprobación validaba el artefacto contra sí misma: cambiar el `+14,52 pp` del informe no producía
ningún fallo. Ver `FINDINGS §F91.bis`.

**La regla:** en una comprobación que enfrenta documento y dato, **los dos lados se leen**. El valor
esperado no se teclea en el código; se extrae del documento, aunque sea más trabajo y aunque el patrón sea
más frágil. Un patrón frágil falla de forma visible cuando el texto cambia; una constante escrita a mano
calla.

**Cómo se detecta:** solo por mutación, y **mutando el documento**, no el dato. De cinco mutaciones, cuatro
se detectaban —el recuento, la p publicada, el veredicto del artefacto y el emparejamiento roto— y la que
tocaba la cifra publicada no. Si la prueba se hubiera limitado a mutar el artefacto, la vacuidad habría
sobrevivido, porque contra el artefacto la comprobación sí funcionaba.

**Corolario:** al escribir una comprobación conviene preguntarse, por cada valor que aparece en su código,
de dónde sale. Si sale del documento que se está comprobando, es una constante y hay que reemplazarla por
una lectura. Si sale de la teoría —un umbral, un nivel de significación—, puede quedarse.

## §L64 — Una comprobación que ya está en rojo no puede servir de centinela

Al poner los tres `.docx` bajo la vigilancia de la autoprueba, esconder cualquiera de ellos **no producía
ningún fallo nuevo**, y la prueba lo reportaba como hueco de cobertura. El motivo no era un hueco: la
comprobación que los usa —«sin modelos excluidos»— **ya estaba en rojo** por §F94, y la autoprueba compara
*conjuntos* de comprobaciones fallidas, de modo que esconder el fichero no cambiaba el conjunto.

**La regla:** un centinela tiene que estar en verde para poder ponerse en rojo. Mientras un defecto siga
abierto, la comprobación que lo delata **no puede vigilar además la presencia de sus artefactos**, y una
prueba de cobertura que no lo distinga confundirá «bloqueado» con «no cubierto». Es el corolario de §L57
—controlar que «bien» no sea indistinguible de «no mirado»— aplicado a la dependencia entre comprobaciones.

**Cómo se resolvió:** la autoprueba distingue ahora tres estados en lugar de dos —vigilado, **bloqueado por
un fallo abierto**, y no vigilado— y solo el tercero cuenta como fallo suyo. El mensaje dice qué artefactos
vuelven a ser vigilables al corregir el defecto, de modo que la deuda queda anotada donde se va a leer.

**Y el efecto colateral que conviene prever:** declarar un fallo para que la puerta de commit siga abierta
tiene este coste oculto. El fallo declarado **desactiva como centinela** a su propia comprobación. Es una
razón más para que la lista de declarados sea corta y se pode: cada entrada no solo tolera un defecto, sino
que ciega una comprobación.

## §L65 — Una excepción sin fecha es un aparcamiento indefinido

La lista de fallos declarados del verificador llegó a siete entradas en un día. Auditadas una por una, las
siete eran válidas y correctamente atribuidas, de modo que la lista no escondía nada — pero el ejercicio
dejó ver la carencia: **ninguna tenía fecha**. Nada distinguía la que se acababa de escribir, con su
responsable trabajando en ella, de la que llevaría tres semanas ahí porque se olvidó.

Y declarar tiene un coste que §L64 documenta: cada entrada **ciega como centinela a su propia
comprobación**. De modo que la lista tiene que ser corta y hay que **verla envejecer**.

**La regla:** toda excepción declarada lleva **la fecha en que se declaró**, y la herramienta **muestra su
edad**. Sin eso, «declarado» deja de significar «alguien se ocupa» y pasa a significar «nadie mira».

**Y una decisión deliberada: no caducan.** Caducar automáticamente un fallo declarado lo convertiría en un
fallo nuevo y cortaría la puerta de commit sin que nadie haya hecho nada mal — que es exactamente la clase de
alarma que se aprende a ignorar, y una alarma ignorada es peor que ninguna. Lo que se hace es **mostrar la
edad** y, pasadas dos semanas, decir en voz alta que una declaración tan vieja suele significar que su
responsable no la tiene. La decisión sigue siendo de una persona; lo que cambia es que ya no puede tomarse
por omisión.

**Comprobado en los dos sentidos:** con las fechas reales el resumen dice «la más antigua lleva 0 días»; con
una fecha de hace veinte, emite el aviso. Las fechas, además, se verificaron contra el historial de git en
lugar de suponerse — las siete se habían añadido el mismo día.

## §L66 — Una comprobación tiene que distinguir «el documento está mal» de «mi detector está roto»

La comprobación que verifica que todo `§F<n>` y `§L<n>` citado tenga su sección reportó, en su primera
versión, **40 referencias colgando**. Ninguna lo estaba. El proyecto tiene **dos convenciones de
encabezado** —las secciones antiguas son `### L47. …`, sin `§`, y las nuevas `## §L61 — …`— y el patrón solo
aceptaba la nueva: encontraba **9** secciones §L donde hay **65**, y todo lo que no cabía en esas nueve
salía como colgante.

**Lo delató mirar la lista, no el número.** Entre las supuestas colgantes estaban §L43, §L44 y §L47, que
`CLAUDE.md` cita y que obviamente existen. Un recuento de 40 es plausible; que §L47 no exista, no.

**La regla:** una comprobación cuyo veredicto depende de un detector propio —un patrón, un extractor, un
parseo— tiene que **comprobar antes que su detector funciona**, y decirlo cuando no. Si no, informa del fallo
de su detector como si fuera un fallo del documento, y esa confusión es peor que no comprobar: manda a
corregir cuarenta cosas que están bien.

**Cómo se implementó:** la comprobación exige detectar un mínimo razonable de secciones de cada clase antes
de emitir un solo veredicto sobre referencias. Si detecta menos, dice **«el patrón de encabezados está roto y
esta comprobación daría falsos positivos en masa»** y no reporta ninguna referencia. Probado degradando el
detector a propósito: emite el aviso de guarda en lugar de los cuarenta falsos positivos.

**Y el corolario, que es el mismo de §L61 desde otro ángulo:** cuando una comprobación nueva reporta *muchos*
fallos a la vez, la primera hipótesis no es que el proyecto esté lleno de defectos — es que la comprobación
está mal. Conviene mirar tres de los fallos antes de creerse el recuento.

## §L67 — No se muta un fichero con trabajo sin comprometer, y `git checkout --` no es un «deshacer»

Al probar por mutación una comprobación recién escrita **y no comprometida**, restauré el fichero con
`git checkout -- tools/verificar_informe.py`. Eso lo devolvió a `HEAD`, y con ello **borró la comprobación
entera**: unas noventa líneas escritas ese mismo turno. Ningún respaldo la tenía, porque los que había hecho
eran anteriores a escribirla. Se pudo rehacer solo porque el código estaba en la conversación.

Hay una simetría instructiva con el error del sentido contrario, cometido también hoy: entonces comprometí
una comprobación **antes** de probarla por mutación, y la conclusión fue «mutar, verificar y luego
comprometer». Es media verdad. La regla completa tiene dos mitades:

- **El trabajo se compromete antes de mutar**, porque la mutación va a exigir restaurar y toda restauración
  puede llevarse lo que no esté guardado.
- **La mutación se prueba antes de dar la comprobación por buena**, porque una comprobación que no se ha
  visto fallar no acredita nada.

Las dos caben: se compromete, se muta, se verifica, y si la verificación descubre que la comprobación era
vacua, se corrige en un segundo commit. Un commit de más es barato; noventa líneas perdidas, no.

**Y el corolario sobre la herramienta:** `git checkout -- <fichero>` **no es un «deshacer»**. Es «tráeme la
versión de `HEAD`», que es una operación destructiva sobre todo lo que haya encima. Para revertir una
mutación hay que restaurar desde **una copia hecha inmediatamente antes de mutar** — que es lo que hice con
los `.docx`, con el corpus y con el Markdown durante todo el día, y lo que olvidé precisamente en el fichero
donde acababa de escribir.

## §L68 — Una rama que no puede dispararse se lee como cobertura y no cubre nada

La comprobación que detecta comprobaciones huérfanas llevaba, en su primera versión, una segunda mitad para
el caso inverso: una función **registrada y no definida**. Probada por mutación, no produjo ningún fallo —
`ejecutar(c_inexistente, s)` levanta un `NameError` en esa misma línea y **aborta el verificador con salida
1** antes de que la comprobación pueda opinar.

Es decir: la rama era **inalcanzable**. No estaba mal escrita; no podía ejecutarse nunca.

**La regla:** antes de escribir una rama defensiva, hay que preguntarse si el caso que cubre puede llegar
hasta ella. Si el lenguaje, el sistema o una capa anterior ya lo interceptan, la rama no añade proteccion —
añade la **apariencia** de protección, que es peor, porque quien lea el código contará una cobertura que no
existe. Aquí Python detecta el caso antes y de forma más terminante que cualquier comprobación propia.

**Cómo se descubrió:** por mutación, y solo porque la mutación **no produjo salida**. Un fallo que no
aparece es tan informativo como uno que sí, y la tentación es darlo por «no aplicable» y seguir. Conviene
mirar por qué no apareció: aquí la respuesta era que el programa había muerto antes.

**Corolario, que enlaza con §L66:** una comprobación puede fallar de tres maneras y hay que distinguirlas —
porque el documento está mal, porque su detector está roto, o porque el caso **nunca llega**. La tercera no
se arregla mejorando la comprobación; se arregla **retirándola** y diciendo quién cubre ese caso.

## §L69 — Propagar una cifra sin su prosa dependiente deja el documento peor que antes

Al propagar a los `.docx` las cifras recalculadas del F1 restringido cambié 81,45 por 80,42 y 76,85 por
76,55, y dejé intacta la frase que dependía de ellas: «la soberanía cuesta unos **cinco** puntos de F1». Era
correcta con las cifras viejas —81,45 − 76,85 = 4,60— y es falsa con las nuevas —80,42 − 76,55 = 3,87—. Los
tres entregables quedaron afirmando, en una conclusión, algo que **su propia resta desmentía dos líneas
antes**.

**Antes de mi cambio el documento era coherente con datos viejos. Después era incoherente consigo mismo.** Lo
segundo es peor: un lector que no conozca los datos no puede detectar lo primero, y detecta lo segundo sin
herramientas, con solo restar.

**La regla:** al propagar una cifra hay que buscar **la prosa que depende de ella** — numerales en palabras,
comparativos («el doble», «tres veces más»), redondeos y signos. Un reemplazo de texto cambia la cifra y no
sabe nada de lo que la cita. La búsqueda no es opcional: la cifra vieja desaparece del documento, así que
después ya no hay forma de encontrar lo que la mencionaba.

**Lo encontró una lectura, no una comprobación.** Estaba revisando el informe como lector, leyendo las siete
conclusiones una por una, y la 3 daba las dos cifras y su diferencia en la misma frase. Ninguna de las
cuarenta y tantas comprobaciones lo habría visto, porque todas comparaban cifras contra cifras y ésta era una
cifra contra una **palabra**.

**Y la comprobación que se escribió después casi nació inútil.** El informe usa «alcanza» en §6.1 y
«obtiene» en la conclusión 3, y el `.docx` conserva solo la segunda. Con un solo verbo en el patrón, la
comprobación encontraba el Markdown —que estaba bien— y no los entregables —que era donde estaba el
defecto—: habría dado por bueno el documento roto mientras verificaba el que no lo estaba. Es §L66 con una
vuelta más: **un detector puede estar lo bastante roto como para mirar solo donde no hay nada que encontrar.**

## §L70 — El registro puede sobrevivir al fallo de la edición que describe

Un reemplazo en `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` falló —el texto buscado tenía saltos de línea y la cadena
de búsqueda no— y **la orden compuesta siguió adelante hasta el `git commit`**. El resultado quedó
comprometido y empujado: `FINDINGS §F107` afirmaba «sustituido por un par verificado» mientras el documento
conservaba el ejemplo viejo.

El `assert` **sí** detectó el fallo y lo dijo. Lo que no hizo fue abortar la cadena que lo invocaba: un
`assert` aborta su propio script, no el `&&` implícito de la orden que lo llamó.

**Es la forma más silenciosa de que un proyecto acabe mintiendo sobre sí mismo.** Un `git status` limpio no lo
detecta, porque el registro sí se escribió. Y nada vuelve a mirar el fichero que debía haber cambiado: la
siguiente pasada lee el registro, no el documento.

**La regla, en dos partes:**

- **La edición y su registro no van en la misma orden.** Primero se aplica, después se **verifica leyendo el
  resultado**, y solo entonces se anota. Si se hacen juntas, el registro puede sobrevivir al fallo.
- **Toda corrección sustantiva deja un predicado**, no solo una frase. `tools/auditar_afirmaciones.py`
  expresa cada afirmación del registro como una **prueba sobre los ficheros reales** — no una copia de la
  afirmación, que sería una segunda fuente de verdad (§L63), sino un test de ella. Nueve afirmaciones de hoy
  comprobadas así, las nueve se cumplen; el fallo ocurrió una vez y se cazó.

**Y una advertencia sobre esa herramienta:** su lista se mantiene a mano, de modo que **solo cubre lo que
alguien se acordó de anotar**. No pretende ser exhaustiva. Pretende que las correcciones de más peso no puedan
quedarse en el registro sin estar en el fichero — que es exactamente lo que pasó una vez hoy.

---

## §L71 — Un ensayo mal armado no refuta ni confirma, y confundirlo con «no detecta» valida comprobaciones vacías

**Cuatro veces en una sesión**, y las cuatro con la misma forma: la mutación no disparó y el defecto
estaba en el ensayo, no en la comprobación.

- Busqué la cifra a mutar **en negrita** y el informe la escribe sin resalte (`§F117`).
- Omití los asteriscos y el `>` de una cita en bloque (`§F120`).
- Apunté la prueba a un espejo de `main` que **ya se había separado**, de modo que la premisa había
  desaparecido (`§F133`).
- Mi `grep` buscaba una cadena que **la salida trunca a 52 caracteres** (`§F134`).

Las cuatro veces la primera lectura fue «la comprobación no detecta», que es lo contrario de lo que
pasaba. Y esa confusión es peligrosa en una dirección concreta: **hace dar por validada una
comprobación que en realidad no se ha probado**, que es exactamente la comprobación vacua contra la
que existe todo este aparato.

**La regla:** un ensayo se juzga por el **código de salida o el recuento de fallos**, nunca por si un
`grep` encuentra algo en la salida. Y si la mutación no encuentra su ancla, eso es un **ensayo
fallido**, que se arregla y se repite; no un resultado.

---

## §L72 — Una cifra correcta sobre el artefacto equivocado hace más daño que una mal calculada

Toda una sesión advirtiendo de que «el cuerpo está en 23,0 de 25 páginas y no cabe lo que falta».
Los 23,05 eran **exactos**: la comprobación los calcula bien, con una densidad medida sobre el PDF
entregado y un ancla verificada. Lo que ocurría es que describen **el Markdown**, y yo los usaba como
si describieran **el entregable** — que es más corto precisamente porque le falta el contenido que
discutíamos (`§F140`).

**Nada lo detecta**, y ahí está el daño: no hay error de cálculo que encontrar, no hay comprobación
que falle, y la cifra resiste cualquier revisión de su aritmética. La equivocación vive en el salto
entre lo que la cifra mide y aquello para lo que se invoca.

**La pregunta que faltaba no era «¿está bien calculado?» sino «¿de qué artefacto habla?»**, y hay
que hacérsela a toda cifra que se herede de una herramienta. Cambió una decisión: de «probablemente
no cabe» a «cabe con margen».

---

## §L73 — Un recuento copiado a un documento envejece sin avisar, y en un procedimiento es peor

`CLAUDE.md` decía «4 fallos (4 declarados, 0 nuevos)» y enumeraba cuáles, cuando había veinticinco
declaraciones. `doc/prompts/00-revision-completa.md` decía «cubre diez comprobaciones» y las listaba,
cuando había cincuenta y cinco (`§F134`, `§F136`).

**Y la gravedad depende de qué clase de documento sea.** En un documento de **norma**, una cifra vieja
desinforma. En uno de **procedimiento** —de los que alguien pega en una sesión nueva para ejecutar una
revisión— hace algo peor: **declarar de menos manda hacer menos**. Quien lo lea creerá que el aparato
cubre diez cosas y verificará a mano las otras cuarenta y cinco, o no las verificará.

**La regla:** un recuento que una herramienta reporta **no se copia**; se ejecuta la herramienta. Si
el recuento **es** el contenido del documento —como en una lista de decisiones—, entonces se declara
y **se ata con una comprobación** que verifique que coincide con lo que hay debajo.

**La excepción, que no es una laguna:** los **registros fechados** —un `WORKLOG`, el registro de
actualizaciones, este propio fichero— consignan lo que era cierto entonces y **por eso no se
actualizan**. A un registro se le añade, no se le edita.

---

## §L74 — Un mecanismo de excepciones se ciega si se lo aplica a sí mismo

`FALLOS_DECLARADOS` silencia un fallo buscando un fragmento **en el texto de su mensaje**. Al declarar
el aviso de la comprobación que audita las declaraciones, usé como clave un trozo de **la plantilla
de ese mensaje**. Resultado: la declaración casaba con **cualquier** aviso de huérfana y **anuló la
detección completa** de declaraciones caducadas, presentes y futuras (`§F133`).

El síntoma que lo delató tiene forma reconocible: la comprobación **se acusaba a sí misma** —«la
declaración n.25 no tapa ningún fallo», sobre la n.25—. Una excepción que se nombra a sí misma
describe el mensaje y no el defecto.

**La regla:** cuando lo que hay que declarar es un **estado del entorno** y no un defecto del
documento, la herramienta correcta es una **lista enumerada en el código**, no una excepción. Y toda
comprobación que audite un mecanismo debe emitir sus mensajes de forma que **el mecanismo no pueda
capturarlos**: un prefijo estricto de la clave, nunca la clave entera.

---

## §L75 — El código fuente se lee con un analizador sintáctico, y el síntoma de no hacerlo es que faltan cosas

Extraía literales de una fuente Python con una expresión regular sobre las comillas. **Un apóstrofo
suelto dentro de un docstring desalinea el emparejamiento** y, a partir de ahí, todos los literales
quedan mal delimitados. Daba **713 fragmentos mal cortados** y **cero** con la palabra que buscaba,
sobre un fichero que la usa cuatro veces. Con `ast`, **402** reales (`§F116`).

**Lo que hace este defecto difícil es su síntoma:** no produce basura evidente, produce **ausencias**.
Una lista con 713 entradas parece más completa que una con 402, y el hueco solo se nota si por
casualidad sabes que algo tenía que estar. Aquí se notó porque una comprobación conocida aparecía como
no cubierta.

**La regla:** para leer código se usa `ast` y no un regex. Y **una cadena que compila como expresión
regular no es por ello una expresión regular**: `| Columna | Otra |` compila sin error y significa
alternancia con ramas vacías, de modo que casa con todo. El guardián preciso es que **un patrón que
casa con la cadena vacía no sirve como ancla**.

---

## §L76 — Una regla que solo vive en un documento se incumple sin que nada avise

La política de ramas se escribió, quedó en `CLAUDE.md` y en el documento de coordinación, y **nada la
comprobaba**. Y ya se había incumplido **antes** de escribirse: `main` iba dos commits por detrás del
remoto en silencio —la rama no tenía *upstream* y el `git pull` fallaba sin avisar— y una rama del día
anterior guardaba la única copia declarada de una dependencia real del sistema.

Es el patrón que esta revisión ha encontrado una docena de veces con formas distintas: la regla de las
categorías puntuadas, la de los recuentos copiados, la de las rutas afirmadas como conservadas. En
todas, el documento decía lo correcto y la realidad iba por otro lado.

**La regla:** al escribir una regla, escribir a la vez **lo que la comprueba**. Si no se puede
comprobar mecánicamente, decirlo en la propia regla, para que quien la lea sepa que descansa en la
disciplina y no en una puerta.

---

## §L77 — Un hallazgo puede detectar bien y encuadrar mal, y el encuadre es lo que se ejecuta

La comprobación de tablas informó «la Tabla 9 tiene 42 filas y el Markdown 45». La detección era
**correcta**. El encuadre con que lo trasladé —«le faltan tres filas»— era **falso**: las dos tablas
usan convenciones distintas, árbol indentado con espacios duros frente a rutas completas, y el mapeo
entre sus filas **no es uno a uno**. Pegar tres filas con ruta completa habría **roto la convención
del entregable**, que además se lee mejor (`§F141`).

La causa es concreta y vale para cualquier comprobación de este tipo: **compara recuentos y se detiene
antes de comparar contenido**, de modo que informa de lo que vio primero y no de lo que manda.

**La regla, que el proyecto ya tenía y esto confirma:** un hallazgo de auditoría es una **hipótesis**,
y hay que verificarlo contra la fuente antes de convertirlo en instrucción. Con una precisión que
faltaba: **verificar no es solo confirmar que el defecto existe, es confirmar que es el defecto que se
cree**. Y cuando una divergencia resulta ser una convención deliberada, la salida correcta es
**declararla como tal**, no igualar los documentos.
