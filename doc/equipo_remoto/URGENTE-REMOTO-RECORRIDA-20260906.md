# 🔴 URGENTE — Necesitamos la re-corrida de `gemma4:12b-mlx` con prioridad

**Fecha:** 2026-09-06
**De:** equipo de desarrollo principal
**Para:** equipo remoto 48 GB
**Asunto:** análisis de vuestros datos de P3 · por qué falla tanto · qué necesitamos

---

## 1. Lo esencial

Hemos analizado a fondo vuestro checkpoint de P3. **El bug de *thinking* está confirmado en vuestros datos**,
con la misma firma exacta que en los nuestros, y afecta más de lo que se estimó al principio:

| Grupo | F1 (inválido) | recall = 0 | % |
|:---|--:|--:|--:|
| `gemma4:12b-mlx_baseline` | 0,2731 | **66 / 120** | **55 %** |
| `gemma4:12b-mlx_kb_rag` | 0,1121 | **94 / 120** | **78 %** |

**Ninguna de estas cuatro cifras es utilizable.** No miden el modelo: miden al arnés perdiendo su respuesta.

> **La prioridad de la re-corrida sube.** Es el único modelo del barrido cuyos datos hay que descartar por
> completo, y bloquea el ANOVA definitivo.

---

## 2. Por qué falla tanto — análisis completo

### 2.1 Las respuestas llegan vacías, no malformadas
Vuestro `benchmark.log` registra **206 fallos de parseo**, y al inspeccionar la respuesta cruda de cada uno:

```
203 respuestas VACÍAS  ·  3 con contenido  ·  0 errores HTTP  ·  0 timeouts
```

El modelo devuelve HTTP 200 con `message.content` **vacío**. No es la red, no es cuota, no es formato
malformado: **no hay nada que parsear**.

### 2.2 El mecanismo
`gemma4:12b-mlx` declara capacidad `thinking` y Ollama la activa por defecto. El razonamiento consume el
presupuesto de `num_predict` (2048) **antes** de emitir la respuesta.

Reproducido en el peor artículo (8813 chars):

| Configuración | `content` | `thinking` | `eval_count` |
|:---|--:|--:|--:|
| Sin fijar `think` | **0** | 7 651 | **2 048** ← tope exacto |
| `think=False` | **918** | 0 | 311 |

### 2.3 Por qué `kb_rag` falla más que `baseline` — vuestros propios datos lo demuestran

| Condición | Latencia mediana | recall = 0 |
|:---|--:|--:|
| `baseline` | 879 s | 66 / 120 (55 %) |
| `kb_rag` | **1 073 s** (+22 %) | **94 / 120 (78 %)** |

**El RAG inyecta contexto extra en el prompt** ⇒ más razonamiento ⇒ el presupuesto se agota antes. La
latencia un 22 % mayor confirma que procesa más. Es el mismo mecanismo que ya medimos con la longitud del
artículo: los que fallan son **1,36× más largos** que los que sobreviven.

### 2.4 Vuestra máquina alivia el síntoma pero no lo cura

| Máquina | RAM | recall = 0 en baseline |
|:---|:---|--:|
| Equipo principal | 16 GB | 101 / 120 (84 %) |
| **Vosotros** | 48 GB | **66 / 120 (55 %)** |

Con más memoria el razonamiento cabe dentro del presupuesto más veces, pero **sigue fallando en más de la
mitad de los casos**. Confirma que la causa es el presupuesto de tokens, no la memoria.

---

## 3. La solución, ya en el árbol

Commit **`743054d`** en `src/providers/ollama_provider.py`:

1. `think` pasa como **parámetro de primer nivel** de `client.chat()`. Estaba dentro de `options`, donde
   Ollama lo ignora en silencio — por eso el modo *thinking* de Qwen3 tampoco llegó a activarse nunca.
2. Nuevo `_THINKING_DISABLED_MODELS`: las variantes MLX de gemma4 reciben `think=False`, de modo que todo su
   presupuesto de tokens va a la respuesta, en igualdad con el resto de modelos del estudio.

**Validado end-to-end:** el artículo que devolvía nada ahora extrae **14 personas, 6 organizaciones y
16 ubicaciones**.

```bash
git pull origin sesion/revision-final-20260905   # imprescindible antes de re-lanzar
```

---

## 4. Qué necesitamos, en orden

### 4.1 🔴 Re-corrida de `gemma4:12b-mlx` — **subir de prioridad**
Su re-corrida estaba encolada tras P4 y `gpt-oss`. **Pedimos adelantarla**: es el único modelo cuyos datos
hay que descartar íntegros, y bloquea el ANOVA definitivo. Los otros pendientes sí pueden esperar.

```bash
./venv/bin/python src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/afectados_thinking_n120_REMOTO \
  --models gemma4:12b-mlx \
  --batch-size 3 --num-workers 8
```

### 4.2 Criterio de aceptación — verificad ANTES de darla por buena

```bash
python3 -c "
import csv, collections
r = list(csv.DictReader(open('results/afectados_thinking_n120_REMOTO/benchmark_results.csv')))
for m in sorted({x['model'] for x in r}):
    g = [x for x in r if x['model'] == m]
    ceros = sum(1 for x in g if float(x.get('recall') or 0) == 0)
    pm = collections.Counter(x['parse_method'] for x in g)
    print(f'{m}: recall=0 en {ceros}/{len(g)} · {dict(pm)}')"
```

| Indicador | Antes (inválido) | **Esperado tras el fix** |
|:---|--:|:---|
| `recall = 0` | 66 y 94 de 120 | **residual** (unos pocos) |
| `parse_method` | 70 y 95 `fallback` | mayoría `direct_json` |

**Si volvéis a ver decenas de ceros, parad y avisadnos**: significaría que el fix no se aplicó (¿pull hecho?
¿proceso reiniciado con el código nuevo?) o que hay una segunda causa.

### 4.3 `qwen3:8b` — contexto, no urgente
Sus cifras actuales **no son inválidas**, pero **no miden lo que se declaraba**: el modo *thinking* nunca se
activó por el bug del parámetro. Con el fix, ahora sí se activará. Conviene re-correrlo para que el estudio
diga la verdad sobre su configuración, pero **sin la urgencia** del anterior.

---

## 5. Lo que sí seguimos dando por bueno de vuestra P3

Estos cinco no usan *thinking* y sus datos son válidos:

| Modelo | F1 baseline | F1 kb_rag | recall = 0 |
|:---|--:|--:|--:|
| `llama3.1:8b` | 0,4959 | 0,5549 | 1 y 2 |
| `mistral-nemo` | 0,4505 | 0,4826 | 3 y 4 |
| `qwen3:8b` | 0,4483 | 0,4425 | 15 y 27 *(ver §4.3)* |

`nuextract` fue **retirado del estudio** por decisión del autor (extractor de plantilla, no homologable a
los generalistas). No hace falta que lo re-corráis.

---

## 6. Método, por si os sirve

Lo que permitió separar «el modelo es malo» de «el arnés está roto», con datos que ya estaban en vuestro
checkpoint:

| Señal | Qué indica |
|:---|:---|
| Latencia **0 s** y **0 tokens** | Rechazo de infraestructura (429/402/red) |
| Latencia **alta** y `content` **vacío** | El arnés pierde la respuesta |
| **Precisión alta con recall ínfimo** | Caso degenerado: con `tp=0` y `fp=0`, la precisión se define como 1,0. **Un modelo que no extrae nada tiene precisión perfecta** |

Cruzar `parse_method` con `recall` distingue un respaldo que funciona de uno que encubre un fallo: en
`nuextract`, 107 de 109 `fallback` rescatan contenido; en `gemma4:12b-mlx`, 66 de 70 quedan en cero.
