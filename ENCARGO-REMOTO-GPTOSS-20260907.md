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
