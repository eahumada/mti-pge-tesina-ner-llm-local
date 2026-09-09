# Cierre del equipo remoto de 48 GB — instrucciones

**2026-09-10.** Respuesta a las dos preguntas planteadas: si borrar la rama temporal y si queda alguna
re-ejecución. Todo lo que sigue está verificado contra el repositorio, no supuesto.

---

## 1. La rama `fix/recorrida-correcciones-20260908` se puede borrar

**Sí, sin riesgo.** Comprobado de tres formas independientes:

| Comprobación | Resultado |
|:---|:---|
| Commits que existen **solo** en esa rama | **0** |
| `git merge-base --is-ancestor` contra `origin/main` | **su punta es antecesora de main** |
| Commits de `main` que ella no tiene | 114 |

Su punta es `0ca0901`, un *merge* de `origin/main` del 2026-09-09 a las 01:10. **Todo su trabajo está en
`main`**, de modo que borrar la referencia no pierde nada.

```
git push origin --delete fix/recorrida-correcciones-20260908
```

No hay copias locales en este clon —solo la referencia remota—, así que no hace falta borrar nada más aquí.

## 2. La rama a la que volver es `main`

`main` es la rama de trabajo y está al día: contiene su trabajo y todo lo posterior. Las otras dos que
existen, `sesion/revision-final-20260908` y `backup/revision-final-20260908`, apuntan **al mismo commit que
`main`** y son la sesión de revisión y su respaldo; **no son ramas de trabajo** y no hay que partir de ellas.

```
git checkout main && git pull --ff-only origin main
```

## 3. Sí queda re-ejecución, y una sola

### 3.1 Re-correr la línea base de `nemotron-mini:4b` sobre N=120 — §3.bis.15

**El defecto.** En `results/recorrida_20260908/nemotron-mini_4b__N120`, la mitad `_baseline` tiene
**18 filas con `parse_method = 'failed'`** de 120, y **ninguna** en `_kb_rag`:

```
nemotron-mini:4b_baseline   direct_json 90 · fallback 12 · failed 18
nemotron-mini:4b_kb_rag     direct_json 117 · fallback 3
```

El registro de la corrida da la causa literal:

```
Attempt 1/3 failed for model 'nemotron-mini:4b': 'list' object has no attribute 'items' (x22)
Attempt 2/3 failed ... (x18)
Attempt 3/3 failed ... (x18)
```

**Dónde está, y esto conviene leerlo antes de tocar nada.** El fallo está en
**`src/llm_runner.py`, línea 167**:

```python
def _normalize_keys(parsed: dict) -> dict:      # línea 149
    ...
    for k, v in parsed.items()                  # línea 167  <-- aquí
```

La firma **declara** `parsed: dict` y la función no comprueba nada. Cuando el modelo devuelve una lista
—`[{"Persons": [...]}]` en lugar de `{"Persons": [...]}`— la llamada a `.items()` levanta el `TypeError`.

> `FINDINGS §F85` atribuía este fallo a `providers/ollama.py`. **Ese fichero no existe** —`src/providers/`
> contiene `__init__.py`, `anthropic_provider.py`, `base.py` y `factory.py`— y el hallazgo queda corregido
> hoy. Si alguien empezó a buscar ahí, era nuestro error, no suyo.

**Qué hacer, en este orden:**

1. Añadir la guarda en `_normalize_keys`: si `parsed` es una lista, tomar su primer elemento si es un
   diccionario, y si no, devolver la estructura vacía en lugar de levantar la excepción.
2. Re-correr **solo** `nemotron-mini:4b` en modo `baseline` sobre N=120. No hace falta repetir `_kb_rag`,
   que no tiene ni una fila fallida, ni ningún otro modelo.
3. **Antes de declarar la corrida válida, comprobar `failed = 0`.** Y no solo eso: comprobar también que
   ninguna fila tenga latencia 0 con 0 tokens **y sin contenido**, porque el mismo defecto se presentó con
   tres firmas distintas en tres corridas —`failed=8`, `failed=7` y `failed=0` con siete filas sin
   telemetría— y el indicador barato dejó de verlo mientras seguía ahí.
4. **Reconstruir el consolidado DESPUÉS**, no antes, con `src/merge_and_analyze.py`.

**Aviso sobre el consolidado.** Existen dos: `ANALISIS_CONJUNTO_20260907`, que es **el que el informe
publica** (F = 38,2222), y `ANALISIS_CONJUNTO_20260909`, el de su barrido (F = 121,56), que **no se adoptó**
precisamente por estas 18 filas. Al reconstruir, el nuevo sustituye al `_20260907` y hay que dejar constancia
de cuál se toma como referencia y por qué.

## 4. Lo demás que falta no es re-ejecución

### 4.1 El desglose por tipo — §3.bis.16

El `merged_results.csv` del consolidado **no trae la columna `metrics`**, y sin ella no se puede calcular la
firma `tp + fn` por categoría desde las cifras publicadas: hay que ir corrida por corrida. Basta con
**exportar lo que ya existe** —el `per_type` que los `detailed_results.json` ya almacenan— sin repetir
inferencia. Es un volcado, no una corrida.

### 4.2 Los derivados desfasados — §3.bis.18

La corrección de puntuación del 2026-09-06 rehizo los `benchmark_summary.json` y **no** los derivados:

- **7 de 17** `acceptance_status.json` conservan el veredicto anterior. En
  `gemma4_31b_cloud_n120_REMOTO` además **invierte el orden**: declara mejor a `..._kb_rag` cuando el
  resumen corregido da mejor al `..._baseline`.
- **42 grupos en 9 corridas** tienen un `statistical_report.md` con cifras viejas, y algunas no son de
  decimales: `deepseek-r1:1.5b_rag_enhanced` declara 0,3516 donde el resumen da **0,1682**.

`python3 tools/derivados_desfasados.py` los enumera e imprime lo que cada fichero debería declarar.
Recalcular desde el `benchmark_summary.json` corregido, sin repetir inferencia, y buscar el mejor con
`f is not None` y **nunca** con `if f`: un F1 de 0,0 es *falsy*.

**No tocar el consolidado**: sus 26 grupos coinciden con `merged_results.csv` y está al día. La herramienta
lo comprueba como control positivo; si una regeneración lo estropeara, se vería.

**No tocar los `benchmark.log` ni los `*.bak_prescore`**: atestiguan qué había antes de la corrección y son
la prueba de que se hizo. Lo que se corrige es el fichero que **afirma**.

### 4.3 El método detrás del +10,01 — §3.bis.17

Menor. Falta el cálculo que produjo el +10,01 y el +2,19 que su informe citaba; el nuestro da **+11,89** y
**+3,16**. No bloquea nada, pero conviene saber cuál es el bueno.

---

## Resumen

| | |
|:---|:---|
| Borrar `fix/recorrida-correcciones-20260908` | **Sí**, verificado: 0 commits propios, punta antecesora de `main` |
| Rama a la que volver | **`main`** |
| Re-ejecución pendiente | **Una**: línea base de `nemotron-mini:4b` en N=120, tras arreglar `llm_runner.py:167` |
| Sin re-ejecución | el desglose por tipo, los derivados desfasados y el método del +10,01 |

Gracias por el trabajo. Los tres puntos que se les pidió vigilar quedaron verificados y pasan los criterios:
`gemma4:12b-mlx` con 56,18 y 58,46 y cero fallidas, `gpt-oss:20b` con 52,39 y 55,67, y la investigación de
`nemotron-mini` y `mistral-nemo` cerrada — el 57,5 % de *fallback* de `mistral-nemo` es benigno, con 68 de 69
registros rescatando contenido.
