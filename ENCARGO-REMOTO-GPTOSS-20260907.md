# 🔬 Encargo al equipo remoto 48 GB — diagnosticar los fallos de `gpt-oss:20b` (y rescatar los datos de N=30)

**Fecha:** 2026-09-07 · **De:** equipo de desarrollo principal · **Decisión del autor:** verificar en remoto.
Va **junto con** [`ENCARGO-REMOTO-N30-20260907.md`](./ENCARGO-REMOTO-N30-20260907.md). Son las **dos únicas**
excepciones al cierre de benchmarks.

---

## Parte A — Antes de nada: ¿sobreviven los datos de N=30 en vuestra máquina?

El dato por registro de la corrida N=30 de julio se perdió por sobrescritura **en la máquina de desarrollo**.
**Puede que en la vuestra no.** Antes de gastar 9 h re-ejecutando, **buscad**:

```bash
find . -path ./venv -prune -o \( -name "*augmented_30*" -o -name "*n30*" -o -name "*_30_*" \) -print
grep -rl "kleptotrace_augmented_30" --include=run_config.json .
```

Cualquier `detailed_results.json`, `benchmark_results.csv` o log de una corrida sobre
`data/kleptotrace_augmented_30.json` **con los 30 registros individuales** valdría: con los `tp/fp/fn`
guardados se puede re-puntuar con `tools/rescore_saved.py` **sin re-inferir**, y nos ahorramos la corrida
entera. Si aparece, decidlo antes de lanzar nada.

Si no aparece, ejecutad el encargo N=30 tal como está descrito.

---

## Parte B — Diagnosticar `gpt-oss:20b`

### Lo que sabemos

`gpt-oss:20b` tiene **76 filas con `recall=0`** de 240: **27/120 en baseline** y **49/120 en kb_rag**. Su
ΔRAG de **−0.097** es el único descenso grande del estudio, y sospechamos que **no mide el RAG sino un fallo
del arnés**.

Los indicios apuntan a un problema corregible, no a un límite del modelo:

| Indicio | Dato |
|:---|:---|
| `parse_method` de los fallos | **67 de 76 son `fallback`**, no `direct_json` |
| Avisos en el log | **69 × «Failed to parse JSON from raw response»** |
| Extracción resultante | **45 de las 49 de kb_rag** quedan en `tp=0, fp=0` — **vacía del todo** |
| ¿Rechazo de infraestructura? | **No.** Latencia mediana de los fallos 838 s frente a 854 s de los aciertos, y volumen de tokens equivalente. **El modelo trabaja y produce salida** |

### La hipótesis

Las dos respuestas crudas que el log conserva legibles muestran **la misma forma**: el modelo extrae
entidades correctas y **después entra en un bucle de repetición** que deja el JSON sin cerrar.

```
{"Persons": ["Chirac", "Aznar", "José María Aznar", way, way, way, way, way, way, …
{"Persons": ["Corín Tellado", "Miguel de Cervantes", "Luis Sepúlveda", "Rosa Regás", "Mario Delgado", "
[Note: This  [Note: This  [Note: This  [Note: This  …
```

Es **degeneración por repetición**, no incapacidad de extraer: las entidades del principio **son correctas**.
El parser falla porque el JSON nunca cierra, cae al *fallback*, y el *fallback* devuelve vacío.

> **Aviso:** el log trunca las respuestas, así que **no hemos podido medir en qué proporción de los 69 casos
> ocurre esto**. Solo tenemos dos muestras legibles y coincidentes. **Esa es exactamente la incógnita que
> tenéis que resolver.**

### Qué ejecutar

Sobre **10 de los registros que fallaron** (5 de baseline y 5 de kb_rag; sacadlos filtrando `recall==0` en
`results/excluidos_n120_REMOTO/benchmark_results.csv`), con el pipeline real y **guardando la respuesta cruda
íntegra**, sin truncar:

1. **Tal cual está hoy** — para reproducir el fallo y capturar la respuesta completa.
2. **Con penalización de repetición** — `repeat_penalty` por encima del 1.1 por defecto (probad 1.15–1.3) y
   ajustad `repeat_last_n`. Si el bucle desaparece, la causa está confirmada.

**Coste estimado:** ~850 s por registro → **~2,5 h** por las dos condiciones.

### Qué mirar además

- **Si el bucle se confirma**, evaluad también un **parser tolerante** que rescate el prefijo válido de un
  JSON sin cerrar. Sería la mejor solución: recupera entidades **sin volver a inferir**, igual que hizo el
  re-puntaje con el bug de *scoring*.
- **Mojibake.** El log muestra `CorÃ­n Tellado` y `José MarÃ­a` — UTF-8 leído como Latin-1. **Comprobad si es
  solo la codificación del fichero de log o si afecta al texto que se compara con el *ground truth***. Si
  fuera lo segundo, ningún nombre español con tilde casaría nunca, y eso **afectaría a todos los modelos**,
  no solo a este. Es la comprobación más importante de este encargo.

### ⚠️ Lo que NO hay que hacer

**No parchear solo las filas que fallan.** Sería sesgar el resultado al alza: se corrigen únicamente las
perdedoras y la media sube sin que el modelo haya mejorado. Es distinto del caso de `nemotron-mini` (7 filas
vacías por un artefacto del contexto batch); aquí hablamos del **32 % de la corrida**.

Si el diagnóstico confirma una causa corregible, lo correcto es **re-ejecutar `gpt-oss:20b` completo** en
ambos modos con el arreglo aplicado —como se hizo con `gemma4:12b-mlx`—, no remendar las 76 filas.
**Esa decisión la toma el autor**, no vosotros ni nosotros: reportad el diagnóstico y esperad.

## Qué entregar

Un reporte con: la respuesta cruda íntegra de al menos 3 fallos; en cuántos de los 10 aparece el bucle de
repetición; si `repeat_penalty` lo elimina; el veredicto sobre el mojibake; y, si procede, la ETA de una
re-ejecución completa de `gpt-oss:20b`. Con las verificaciones de siempre — tasa de fallo, `recall=0`,
protocolo, `F1 ≤ (P+R)/2`— y **promediando con `if x.get('k') is not None`**, nunca `if x.get('k')`.

Declaradlo en `CURRENT-TASKS.md` §3.bis y avisad por *push*.

---

## Adenda (2026-09-07 16:35) — resultado del diagnóstico y cómo acotar el arreglo a `gpt-oss`

Vuestro `DIAGNOSTICO-GPTOSS-20260907.md` **descarta mi hipótesis**: el bucle de repetición **no se reproduce**
(0 de 5) y `repeat_penalty` es irrelevante. Las cinco filas recuperan **JSON limpio y cerrado**. Bien visto.

Lo que sí destaca de vuestros datos es **la latencia**: **10–40 s por registro al re-ejecutar frente a 838 s**
en la corrida oficial. Un factor de 20–80×. Eso apunta a vuestra propia explicación —el razonamiento agotando
`num_predict=2048` antes de emitir la respuesta, con truncado y caída a *fallback*— que es **exactamente el
patrón de §F40-F41** con `gemma4:12b-mlx`, salvo que aquí el *thinking* no puede apagarse.

### Cómo re-ejecutar sin contaminar el resto del estudio

**Ejecutad `gpt-oss:20b` completo (N=120 × 2 modos) cambiando UNA sola cosa: `num_predict` a 4096.**

- **thinking ON**, sin tocar (decisión firme, §F44-F45).
- **Mismo corpus, sin reparar el mojibake.**
- **Mismo evaluador, sin normalización de codificación.**

> **Por qué es importante no arreglar el gold en esta corrida.** Si `gpt-oss` se puntúa contra un gold
> corregido y los otros doce modelos contra el gold corrupto, queda medido **con otra vara** — el mismo error
> que las dos convenciones de puntuación y los dos regímenes de *thinking* que ya costó unificar. El mojibake
> es un problema **de todo el estudio** (§F46, §F48) y su corrección es una decisión aparte del autor. Aquí el
> objetivo es aislar **un** cambio: el presupuesto de tokens.

### Qué comprobar en la entrega

Además de las verificaciones de siempre: **cuántas filas alcanzan el tope de `num_predict`** (si con 4096
siguen truncando, el problema es otro), la **tasa de `fallback`** comparada con las 67 de la corrida oficial, y
el conteo de `recall=0` frente a los 76 actuales. Si el artefacto desaparece, la cifra de `gpt-oss` en el
estudio se sustituye por la nueva; si persiste, hay que reabrir el diagnóstico.

**ETA vuestra:** ~1–1,5 h. **No parchear filas sueltas**, sigue vigente.

### Sobre el mojibake — matiz importante que cambia el diagnóstico (§F48)

Verificamos vuestro §F46 y las cifras son correctas, pero **falta un dato que cambia la conclusión**: el
mojibake **no está solo en el gold, también en el texto de entrada** (87 % de los artículos), y de forma
**coherente** — las 283 entidades corruptas del gold aparecen **tal cual** en el texto, ninguna aparece
corregida.

Es decir: el modelo lee `Emiliano GarcÃ­a-Page` y el gold espera `Emiliano GarcÃ­a-Page`. **Quien copia
literalmente acierta; quien normaliza a español correcto falla.** No es un suelo uniforme del 4,7 %: medido por
modelo, el Δ entre registros con y sin mojibake va de **−0.070 a +0.091**.

**Consecuencia para la reparación:** arreglar solo el gold **invertiría** la injusticia en lugar de eliminarla.
Lo correcto sería **normalizar ambos lados al comparar** (reparar gold *y* extracción antes del *fuzzy
matching*, ~10 líneas en `src/evaluator.py`). **No lo implementéis todavía**: es una decisión de alcance del
autor, registrada en `TODO-INFORME-FINAL.md §15.4`.

**Nota terminológica para todos los documentos:** la forma corrupta es `JosÃ© Bono` y la correcta es
**`José Bono`**. Escribirlo siempre en ese orden; invertirlo confunde el dato dañado con el real.
