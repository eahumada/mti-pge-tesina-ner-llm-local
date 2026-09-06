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
