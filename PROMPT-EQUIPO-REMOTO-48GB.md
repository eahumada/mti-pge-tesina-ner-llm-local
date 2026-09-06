# Encargo de ejecución — Benchmark NER sobre hardware de 48 GB

> **Para:** equipo con acceso a máquina de **48 GB de RAM**
> **De:** proyecto de tesina *NER con LLMs locales para cumplimiento y sanciones* (Magíster en TI)
> **Fecha:** 2026-09-05
> **Motivo:** el equipo de desarrollo tiene **16 GB de RAM** y varios modelos no caben. Ver §2.

---

## 1. Qué es este proyecto

Benchmark académico que evalúa modelos de lenguaje locales en **reconocimiento de entidades nombradas
(NER)** sobre noticias de sanciones financieras. Mide F1, precisión, recall, tasa de alucinación, latencia y
throughput, y valida las diferencias con **ANOVA + Tukey HSD**.

Repositorio: `repos/ner-llm-entity-benchmark/`. Motor de inferencia: **Ollama** (ejecución local, sin envío
de datos a terceros).

---

## 2. Por qué se os encarga a vosotros

En la máquina de desarrollo (16 GB) se verificó empíricamente que **un modelo cuyos pesos superan
~70 % de la RAM física no se ejecuta**: no va «lento», directamente no responde.

Medición real de `gemma4:31b` (19 GB) sobre 16 GB:

| Configuración | Extracciones lanzadas | Respuestas en 26–31 min | Swap |
|:---|---:|---:|---:|
| 8 workers | 15 | **0** | 16.1 GB de 17.4 |
| 1 worker | 16 | **0** | 15.0 GB |

Reducir la concurrencia no ayudó: el cuello es el tamaño del modelo, no el paralelismo.
Señal diagnóstica: `llama-server` con **CPU ~30 % y swap alto** ⇒ espera disco, no calcula.

**Con 48 GB estos modelos caben con holgura.**

---

## 3. Tareas encargadas, por prioridad

### 3.1 🔴 PRIORIDAD 1 — `gemma4:31b` sobre N=15
Es el bloqueante que impide cerrar la tabla principal de la tesina. Su fila cita F1 = 67.83 % **sin ningún
dato crudo que la respalde** en todo el proyecto.

```bash
ollama pull gemma4:31b     # 19.9 GB

./venv/bin/python src/main.py \
  --data-file data/kleptotrace.json \
  --rag-study --rag-mode entities \
  --results-dir results/gemma4_31b_n15_REMOTO \
  --models gemma4:31b \
  --batch-size 3 --num-workers 4
```

- Corpus: 15 artículos ⇒ **30 extracciones** (baseline + rag_enhanced).
- Referencia: `gemma4:31b-mlx` (mismo tamaño, formato MLX) tardó **415 s/artículo de mediana** en 16 GB.
  Con 48 GB debería bajar bastante.

### 3.2 🔴 PRIORIDAD 2 — Modelos excluidos por RAM, sobre N=120
Quedaron fuera del estudio por no caber en 16 GB. Con 48 GB son viables y **devolverían el estudio a
14 modelos en vez de 12**.

```bash
ollama pull gpt-oss:20b                                    # 13 GB
ollama pull sonct988/gemma4-26b-a4b-it-q4km-256k:latest    # 16 GB

./venv/bin/python src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/excluidos_n120_REMOTO \
  --models gpt-oss:20b "sonct988/gemma4-26b-a4b-it-q4km-256k:latest" \
  --batch-size 3 --num-workers 6
```

> ⚠️ **`--rag-mode kb_combined` es obligatorio aquí.** El valor por defecto es `entities`, que es otra
> implementación de RAG y produciría datos **no comparables** con la corrida de referencia. Es el error más
> costoso que cometimos: 10 h de cómputo desperdiciadas antes de detectarlo.

### 3.3 🟠 PRIORIDAD 3 — Benchmark principal N=120, 7 modelos
En 16 GB avanza a **~2 filas/hora** por presión de memoria; quedan ~1 500 de 1 680 filas. Con 48 GB sería
mucho más rápido.

```bash
./venv/bin/python src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/benchmark_n120_REMOTO \
  --models gemma4:12b-mlx qwen3:8b mistral-nemo:latest nuextract:latest \
           llama3.1:8b nemotron-mini:4b deepseek-r1:1.5b \
  --batch-size 3 --num-workers 8
```

### 3.4 🟡 PRIORIDAD 4 — Estudio de configuraciones de prompt
Las 4 cifras que la tesina cita (0.7169 / 0.6640 / 0.6482 / 0.5874) **no existen en ningún dato**. Hay que
regenerarlas.

```bash
ollama pull gemma4:latest    # 9.6 GB

./venv/bin/python src/main.py \
  --data-file data/kleptotrace.json \
  --ablation \
  --results-dir results/ablacion_n15_REMOTO \
  --models gemma4:latest \
  --batch-size 3 --num-workers 4
```

Compara 4 configuraciones: zero-shot EN, zero-shot ES, few-shot EN, few-shot ES.

---

## 4. Protocolo — respetar EXACTAMENTE

Estos parámetros hacen los resultados comparables con las corridas ya validadas. **No cambiarlos.**

| Parámetro | Valor | Nota |
|:---|:---|:---|
| `temperature` | `0.1` | por defecto |
| `seed` | `42` | por defecto |
| `max_tokens` | `2048` | por defecto |
| `fuzzy_threshold` | `85` | por defecto |
| `system_prompt_file` | `SYSTEM_PROMPT.md` | por defecto |
| `--rag-mode` | **`kb_combined`** para N=120 · **`entities`** para N=15 | ⚠️ crítico, ver §3.2 |
| `--results-dir` | **siempre explícito** | ver §5.1 |

---

## 5. Trampas verificadas — leed esto antes de ejecutar

### 5.1 `--resume` NO funciona sin `--results-dir`
Sin `--results-dir`, cada ejecución crea un directorio nuevo con timestamp y **el checkpoint jamás se
encuentra**: la corrida reinicia desde cero **en silencio**. Pasar siempre `--results-dir` explícito.

### 5.2 Nunca escribir en la raíz de `results/`
Una corrida de julio escribió ahí y otra posterior **la sobrescribió**, destruyendo permanentemente los
datos por registro del corpus N=30. Hay un guardarraíl que ahora aborta si se intenta, pero no lo forcéis.

### 5.3 Un `pull` exitoso NO significa que el modelo sirva
Los modelos cloud descargan su manifiesto con `success` y aparecen en `ollama list`, pero la inferencia
puede fallar con **429 (cuota)** o **402 (requiere plan de pago)**. **Validad con una llamada de inferencia
real** antes de lanzar el barrido completo.

### 5.4 Distinguir fallo de infraestructura de fallo del modelo
`parse_method='failed'` agrupa hoy ambas causas. Tras cada corrida, comprobad:

```bash
# tasa de fallo por modelo — debe ser 0
python3 -c "
import csv,collections
r=list(csv.DictReader(open('results/<DIR>/benchmark_results.csv')))
c=collections.Counter((x['model'], x['parse_method']) for x in r)
for k,v in sorted(c.items()): print(k,v)"
```

Si hay `failed`, **los promedios están contaminados**: las extracciones fallidas puntúan recall 0 y hunden
la media. En una corrida nuestra, 6 de 15 fallos convirtieron un F1 real de 0.66 en un 0.40 aparente.

### 5.5 Impedir la suspensión del equipo
Una suspensión con peticiones en vuelo **contamina las latencias**: el tiempo dormido se contabiliza como
tiempo de inferencia. Nos generó muestras de 15 860 s y 106 095 s para un solo artículo.

```bash
sudo pmset -a disablesleep 1     # macOS; revertir con 0 al terminar
```

### 5.6 Serialidad entre modelos locales
Ejecutad **un modelo local a la vez**, para que disponga de toda la memoria. Los **modelos cloud sí pueden
correr en paralelo** con los locales: no consumen memoria local.

---

## 6. Qué devolver

Por cada corrida, el directorio `results/<nombre>_REMOTO/` completo:

| Archivo | Contenido |
|:---|:---|
| `benchmark_results.csv` | Resultados por registro — **el más importante** |
| `detailed_results.json` | Extracciones completas |
| `benchmark_summary.json` | Agregados por modelo |
| `statistical_report.md` | ANOVA + Tukey |
| `run_config.json` | Configuración efectiva |
| `benchmark.log` | Log completo, **necesario para auditar fallos** |

Acompañad la entrega con:
1. **Tasa de fallo por modelo** (§5.4). Debe ser 0; si no, indicad la causa.
2. **RAM del equipo y pico de uso** durante la corrida.
3. **Confirmación de que no hubo suspensiones** durante la ejecución.
4. Cualquier desviación del protocolo, y por qué.

---

## 7. Preparación del entorno

### 7.1 Rama y dependencias

```bash
git clone <repo> && cd repos/ner-llm-entity-benchmark
git checkout sesion/revision-final-20260905     # rama con los corpus versionados

python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama serve &          # dejar corriendo
```

### 7.2 Verificad que los corpus llegaron

Los corpus **sí van en el repositorio** desde 2026-09-06 (antes estaban excluidos por `.gitignore`, lo que
habría impedido ejecutar cualquier tarea). Comprobadlo antes de empezar:

```bash
python3 -c "
import json
for f in ['data/kleptotrace.json','data/benchmark_balanced_120.json']:
    d=json.load(open(f)); r=d if isinstance(d,list) else d.get('dataset',[])
    print(f'{f}: {len(r)} registros')"
```

Debe imprimir **15** y **120** respectivamente. **No los regeneréis**: los resultados tienen que ser
comparables con las corridas existentes.

### 7.3 ⚠️ Datos del RAG — necesarios para las tareas 1 y 4

El sistema RAG usa dos fuentes distintas según el modo, y **solo una viaja en el repositorio**:

| Recurso | ¿Versionado? | Lo necesitan |
|:---|:---|:---|
| `data/knowledge_base/` | ✅ sí | Tareas **2 y 3** (`--rag-mode kb_combined`) |
| `data/dictionaries/` | ❌ **no** (1.8 MB, descargable) | Tareas **1 y 4** (`--rag-mode entities`) |
| `data/chroma_db/` | ❌ no (60 MB) | Se genera solo a partir de los diccionarios |

**Antes de las tareas 1 y 4**, regenerad los diccionarios:

```bash
python3 fetch_dictionaries.py
python3 download_ofac.py           # listas de sanciones OFAC
python3 generate_metadata_dicts.py
```

`src/rag_manager.py` indexa automáticamente en ChromaDB la primera vez que se ejecuta, así que
`data/chroma_db/` **no hay que crearlo a mano** — pero la primera corrida tardará algo más mientras indexa.

Si `data/dictionaries/` está vacío al lanzar una tarea con `--rag-mode entities`, el RAG no inyectará
contexto y la condición `_rag_enhanced` será **indistinguible del baseline**, sin que nada lo advierta.

### 7.4 Comprobación previa del modelo

```bash
# ¿responde de verdad, o solo está en `ollama list`?
curl -s http://localhost:11434/api/chat \
  -d '{"model":"gemma4:31b","messages":[{"role":"user","content":"di OK"}],"stream":false}'
```

---

## 8. Contexto adicional

- `FINDINGS.md` — 38 hallazgos técnicos con su evidencia
- `LEARNING.md` — 28 lecciones operativas
- `TODO-INFORME-FINAL.md` — estado y pendientes del informe
- `repos/ner-llm-entity-benchmark/AGENTS.md` — arquitectura y gestión de modelos

**Contacto para dudas de protocolo:** antes de desviaros de §4, preguntad. Un parámetro distinto invalida la
comparabilidad con las corridas ya validadas, y eso no se detecta hasta el análisis final.

---

## 9. 🔴 OBLIGATORIO — Reportad en el archivo de sincronización

Este proyecto lo trabajan **varios agentes y equipos en paralelo** (Claude Code, Claude Desktop, Antigravity
y vosotros). La coordinación se lleva en un único documento vivo:

### 📄 [`CURRENT-TASKS.md`](./CURRENT-TASKS.md) — sección **§3.bis Equipo Remoto (48 GB RAM)**

Ahí tenéis un bloque por cada una de las 4 tareas, ya creado y esperando vuestros datos.

### Protocolo por cada tarea — los 5 pasos

1. **LEER** `CURRENT-TASKS.md` antes de empezar. Comprobad que ningún otro agente declara estar trabajando
   sobre los mismos archivos.
2. **ESCRIBIR** vuestra entrada en §3.bis: cambiad el estado a `▶️ EN CURSO`, con hora de inicio y qué
   archivos vais a producir.
3. **EJECUTAR** la tarea.
4. **ACTUALIZAR** la entrada al terminar, usando la plantilla de §3.bis.5: resultados, **tasa de fallo**,
   hardware, desviaciones del protocolo. Añadid además una fila al **§6 Registro de actualizaciones**.
5. **VOLVER A LEER** el documento, por si alguien escribió mientras trabajabais.

### Reglas de convivencia

- Si un archivo figura como `EN CURSO` por otro agente, **no lo toquéis**. Esperad o elegid otra tarea.
- Escribid siempre por **append** dentro de vuestra sección. **Nunca reescribáis entradas ajenas.**
- Si una tarea se interrumpe y la retomáis, **actualizad también su entrada** (estado y motivo del corte).
- Si un archivo cambió de forma inesperada, **no lo revirtáis**: puede ser trabajo deliberado de otro
  equipo. Reportadlo y preguntad.

> **Por qué insistimos.** El 2026-09-03 un documento apareció modificado por un agente externo a la sesión
> que lo estaba editando, y estuvimos a punto de perder trabajo. La política de **solo añadir, nunca
> reescribir** es lo que ha permitido que varios agentes trabajen sin destruirse el trabajo mutuamente.

### Lo mínimo que debe quedar registrado

Aunque una tarea falle o no se complete, dejad constancia de:

| Campo | Por qué importa |
|:---|:---|
| **Tasa de fallo** por modelo | Sin esto no sabemos si los promedios están contaminados (nos pasó: 6/15 fallos convirtieron un F1 de 0.66 en 0.40) |
| **RAM total y pico de uso** | Determina si el modelo cupo de verdad o paginó |
| **Confirmación de que no hubo suspensiones** | Una suspensión contamina las latencias con valores imposibles |
| **`--rag-mode` empleado** | Si no fue el correcto, los datos no son comparables y hay que repetir |
| **Cualquier desviación del protocolo §4** | Invalida silenciosamente la comparabilidad si no se declara |
