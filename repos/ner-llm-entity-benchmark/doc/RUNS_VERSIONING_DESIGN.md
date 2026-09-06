# Diseño: versionado e histórico de corridas del benchmark

**Fecha:** 2026-09-03 · **Estado:** propuesta (NO aplicada) · **Archivo nuevo, aditivo.**
**Documento hermano:** `results/RUNS_INDEX.md` (índice de las corridas históricas).

Origen del requisito (textual del autor):

> «mantener historia de las pruebas realizadas en el tiempo para cada N, asegurarse que en el
> futuro puedan hacerse pruebas con N 30 y N 120 con y sin rag y para los diferentes shots»

> ⚠️ Este documento **describe** cambios de código; ninguno fue aplicado. `src/main.py` y
> `src/config.py` quedaron intactos en esta iteración.

---

## 1. Estado actual (línea base)

| Aspecto | Implementación actual | Ubicación |
| :--- | :--- | :--- |
| Nombre del directorio de salida | `results/<basename(data_file)>_<YYYYMMDD_HHMMSS>/` | `src/config.py` → `BenchmarkConfig.__post_init__` |
| Metadata persistida | volcado plano de `BenchmarkConfig` (`asdict`) | `src/main.py` → `export_results()`, paso 5 |
| Selección de corpus | `--data-file` | `src/main.py::main()` |
| Modo RAG | `--rag-study` + `--rag-mode {entities,kb_guidelines,kb_fewshot,kb_combined}` | idem |
| Ablación de prompts | `--ablation` (booleano, pasa como argumento a `run_benchmark`) | idem |
| Prompt individual | `--system-prompt-file` | idem |
| Nombres de condición en el CSV | columna `model` = `condition_name` o el modelo | `src/main.py::process_batch` (`display_model_name`) |

Condiciones generadas hoy:

- baseline simple → `condition_name = None` ⇒ columna `model` = nombre del modelo.
- `--rag-study --rag-mode entities` → `<modelo>_baseline` y `<modelo>_rag_enhanced`.
- `--rag-study --rag-mode kb_*` → `<modelo>_baseline` y `<modelo>_kb_rag`.
- `--ablation` → `zs-en`, `zs-es`, `fs-es`, `fs-en` (un único modelo, `config.models[0]`).

### 1.1 Defectos detectados

1. `ablation` **no** se persiste en `run_config.json` (no es campo de `BenchmarkConfig`) ⇒ una
   corrida de ablación es indistinguible de un baseline por metadata.
2. El nombre del directorio no codifica modo ni prompt.
3. `rag_mode` no existía antes del 2026-09-01 ⇒ corridas viejas sin el campo.
4. Cuando `results_dir == "results"` (o se pasa explícito) las corridas se sobrescriben entre sí:
   causa de 6 corridas perdidas, entre ellas la N=30 con F1 = 79.03 % de la tesina.
5. `results/` está en `.gitignore` ⇒ el histórico no está versionado.
6. No se guarda `N` real ni checksum del corpus.
7. No se distingue modelos solicitados de modelos efectivamente ejecutados.

---

## 2. Convención de nombres propuesta

```
results/<corpus>_N<n>__<modo>__<prompt>__<YYYYMMDD>_<HHMMSS>[__<tag>]/
```

- `__` (doble) separa dimensiones; `_` (simple) vive dentro de una dimensión ⇒ `split("__")`
  recupera las 4–5 dimensiones sin ambigüedad.
- `<corpus>`: slug de `basename(data_file)` — `kleptotrace`→`klepto`,
  `kleptotrace_augmented_30`→`kleptoaug`, `benchmark_balanced_120`→`balanced120`,
  `conll2002_es`→`conll2002es`.
- `N<n>`: número **real** de registros cargados (no el del nombre del archivo).
- `<modo>`: `baseline` · `rag-entities` · `rag-kb-guidelines` · `rag-kb-fewshot` ·
  `rag-kb-combined` · `ablation`.
- `<prompt>`: `zs-en` · `zs-es` · `fs-en` · `fs-es` · `4-prompts` (ablación).
- `<tag>`: opcional, del nuevo flag `--run-tag`.

Ejemplos objetivo del requisito del autor:

```
results/kleptoaug_N30__baseline__zs-en__20260903_101500/
results/kleptoaug_N30__rag-kb-combined__zs-en__20260903_143000/
results/kleptoaug_N30__ablation__4-prompts__20260903_190000/
results/balanced120_N120__rag-kb-combined__zs-es__20260904_090000/
```

**Compatibilidad hacia atrás:** los 5 directorios históricos con el patrón antiguo
(`<dataset>_<timestamp>`) siguen siendo válidos; el parser del índice debe aceptar ambos formatos
(si `split("__")` devuelve 1 elemento ⇒ formato v1, se completa desde `run_config.json` + CSV).

---

## 3. Esquema de `run_config.json` v2 (estrictamente aditivo)

Ninguna clave existente cambia de nombre, tipo ni semántica. Se **agregan**:

```jsonc
{
  // ── claves v1 existentes: models, batch_size, num_workers, max_retries,
  //     fuzzy_threshold, redis_url, data_file, results_dir, checkpoint_file,
  //     system_prompt_file, ollama_base_url, temperature, max_tokens, seed,
  //     rag_study, rag_mode  ────────────────────────────────────────────────

  "schema_version": "2",
  "run_id": "kleptoaug_N30__rag-kb-combined__zs-en__20260903_143000",
  "run_tag": "rerun-tesina",

  "started_at_utc": "2026-09-03T17:30:00Z",
  "finished_at_utc": "2026-09-03T19:11:42Z",
  "duration_sec": 6102.4,

  "dataset_name": "kleptotrace_augmented_30",
  "dataset_n_records": 30,
  "dataset_sha256": "9f2c…",
  "dataset_kind": "synthetic",          // synthetic | real | mixed

  "ablation": false,                     // ← HOY NO SE GUARDA (defecto #1)
  "mode": "rag-kb-combined",             // etiqueta canónica derivada
  "conditions": ["gemma4:latest_baseline", "gemma4:latest_kb_rag"],

  "prompt_variant": "zs-en",             // zs-en | zs-es | fs-en | fs-es | 4-prompts
  "prompt_files": {"zs-en": "SYSTEM_PROMPT.md"},
  "prompt_sha256": {"zs-en": "c41a…"},

  "models_requested": ["gemma4:latest", "gpt-oss:20b"],
  "models_available": ["gemma4:latest"],
  "models_skipped":   ["gpt-oss:20b"],

  "git_commit": "bb79279",
  "git_branch": "main",
  "git_dirty": true,
  "python_version": "3.13.1",
  "platform": "macOS-15.5-arm64",
  "hostname": "…",

  "status": "completed",                 // completed | partial | failed
  "n_rows": 60,
  "notes": ""
}
```

Los consumidores actuales (`src/dashboard.py`, análisis ad-hoc) leen claves por nombre, de modo
que campos añadidos no rompen nada.

---

## 4. Cambios de código recomendados (NO aplicados)

### C1 — `src/config.py`: campos nuevos en `BenchmarkConfig`

Agregar, **al final** del bloque de campos y todos con default (para no romper llamadas
posicionales ni `asdict`):

```python
ablation: bool = False
run_tag: str = ""
dataset_n_records: int = 0
dataset_sha256: str = ""
prompt_variant: str = ""
conditions: list[str] = field(default_factory=list)
models_available: list[str] = field(default_factory=list)
models_skipped: list[str] = field(default_factory=list)
git_commit: str = ""
started_at_utc: str = ""
finished_at_utc: str = ""
status: str = "unknown"
schema_version: str = "2"
```

### C2 — `src/config.py`: `__post_init__` construye el nombre canónico

Reemplazar el cuerpo actual por un helper `build_run_id(...)`:

```python
CORPUS_SLUGS = {
    "kleptotrace": "klepto",
    "kleptotrace_subset": "kleptosub",
    "kleptotrace_augmented_30": "kleptoaug",
    "kleptotrace_augmented_60": "kleptoaug",
    "kleptotrace_augmented_120": "kleptoaug",
    "benchmark_balanced_120": "balanced120",
    "conll2002_es": "conll2002es",
}
PROMPT_VARIANTS = {
    "SYSTEM_PROMPT.md": "zs-en",
    "SYSTEM_PROMPT_ES.md": "zs-es",
    "SYSTEM_PROMPT_EN_FEWSHOT.md": "fs-en",
    "SYSTEM_PROMPT_ES_FEWSHOT.md": "fs-es",
}

def mode_label(rag_study: bool, rag_mode: str, ablation: bool) -> str:
    if ablation:
        return "ablation"
    if not rag_study:
        return "baseline"
    return "rag-entities" if rag_mode == "entities" else "rag-" + rag_mode.replace("_", "-")
```

`__post_init__` pasa a:
`results/{corpus}_N{n}__{mode}__{prompt}__{ts}[__{tag}]`.
`N{n}` solo se conoce tras cargar el dataset ⇒ dos opciones:
**(a)** contar los registros en `__post_init__` (lectura barata de un JSON pequeño), o
**(b)** dejar `N0` y renombrar el directorio una vez conocido `total_records`.
Se recomienda **(a)**: `json.load(data_file)["dataset"]` y `len(...)`, con `try/except` que caiga
a `N0` si el archivo aún no existe (caso `--generate-sample-data`).

### C3 — `src/config.py`: guardarraíl anti-sobrescritura

```python
if os.path.abspath(self.results_dir) == os.path.abspath("results"):
    raise ValueError(
        "results_dir no puede ser 'results' (sobrescribiría corridas previas). "
        "Ver results/RUNS_INDEX.md §7.4"
    )
```

Es el cambio de mayor valor: evita repetir la pérdida de la corrida N=30.

### C4 — `src/main.py::main()`: propagar `--ablation` y `--run-tag`

```python
parser.add_argument("--run-tag", type=str, default="",
                    help="Etiqueta libre para distinguir corridas equivalentes")
...
config = BenchmarkConfig(..., ablation=args.ablation, run_tag=args.run_tag)
...
run_benchmark(config, resume=args.resume, ablation=config.ablation)
```

`run_benchmark()` conserva su firma (el parámetro `ablation` sigue existiendo) ⇒ cambio no
disruptivo; simplemente el valor queda también dentro del config y por lo tanto en el JSON.

### C5 — `src/main.py::export_results()`: enriquecer el volcado

Antes del `json.dump(config.to_dict(), …)`, componer:

```python
meta = config.to_dict()
meta.update({
    "finished_at_utc": datetime.now(timezone.utc).isoformat(),
    "conditions": sorted({r["model"] for r in results}),
    "n_rows": len(results),
    "status": "completed" if results else "failed",
    "git_commit": _git("rev-parse --short HEAD"),
    "git_branch": _git("rev-parse --abbrev-ref HEAD"),
    "git_dirty": bool(_git("status --porcelain")),
    "python_version": platform.python_version(),
    "platform": platform.platform(),
    "hostname": socket.gethostname(),
})
json.dump(meta, f, indent=2)
```

`_git()` debe capturar excepciones y devolver `""` si git no está disponible.
Guardar además una copia como `run_meta.json` para no alterar la semántica de `run_config.json`
para lectores existentes (opción conservadora, recomendada).

### C6 — Registrar modelos omitidos

En los bucles de `run_benchmark` donde hoy se hace `if not check_model_available(...): continue`,
acumular en `config.models_skipped` / `config.models_available` antes del `continue`.
(3 sitios: fase productor RAG, fase worker RAG, y el bucle de modelos del baseline.)

### C7 — Snapshot de prompts

Copiar los `SYSTEM_PROMPT*.md` efectivamente usados dentro del directorio de la corrida
(`<run_dir>/prompts/`) y registrar su SHA-256. Un prompt editado a posteriori invalida
silenciosamente la comparabilidad de corridas viejas.

### C8 — Herramienta de índice `tools/index_runs.py` (script nuevo)

- Recorre `results/*/`, lee `run_config.json` + `benchmark_results.csv`.
- Deriva corpus, N, modo, prompt, nº de modelos, condiciones, filas y F1 medio por condición.
- Escribe `results/runs_index.json` (machine-readable, regenerable) y **agrega** al final de la
  tabla §2 de `results/RUNS_INDEX.md` solo las corridas cuyo `run_id` aún no figura (append-only,
  nunca reescribe filas).
- Modo `--check`: falla si hay un directorio de resultados no catalogado (útil en pre-commit).

### C9 — `.gitignore`: excepciones para artefactos livianos

Añadir **al final** (no eliminar la regla `results/`):

```gitignore
!results/RUNS_INDEX.md
!results/runs_index.json
!results/**/run_config.json
!results/**/run_meta.json
!results/**/statistical_report.md
!results/**/benchmark_summary.json
!results/**/acceptance_status.json
```

Nota: git no desciende a un directorio excluido, por lo que en la práctica hace falta además
`!results/` + `results/*` con re-inclusión selectiva, o simplemente seguir usando
`git add -f <archivo>` como se hizo con `kb_rag_analysis_20260901.json`. Verificar con
`git check-ignore -v` antes de adoptar.

### C10 — `run_benchmark.sh`: matriz explícita de corridas

Añadir (sin quitar el barrido actual) un bloque parametrizable:

```bash
for DS in data/kleptotrace_augmented_30.json data/benchmark_balanced_120.json; do
  for MODE in "" "--rag-study --rag-mode kb_combined"; do
    for P in SYSTEM_PROMPT.md SYSTEM_PROMPT_ES.md \
             SYSTEM_PROMPT_EN_FEWSHOT.md SYSTEM_PROMPT_ES_FEWSHOT.md; do
      ./venv/bin/python src/main.py --data-file "$DS" $MODE \
        --system-prompt-file "$P" --models "${MODELS[@]}" --batch-size 3
    done
  done
done
```

Son 2 corpus × 2 modos × 4 prompts = **16 corridas**, cada una con directorio propio e
inequívoco bajo la convención de §2 — exactamente lo que pide el requisito del autor.

---

## 5. Orden de implementación sugerido

| Paso | Cambio | Riesgo | Valor |
| :-: | :--- | :--- | :--- |
| 1 | C3 (guardarraíl anti-sobrescritura) | nulo | 🔴 alto — evita repetir la pérdida de N=30 |
| 2 | C1 + C4 (persistir `ablation`, `run_tag`) | bajo | 🔴 alto — desambigua ablación vs. baseline |
| 3 | C5 + C6 (metadata enriquecida, modelos omitidos) | bajo | 🟠 medio |
| 4 | C2 (nombres canónicos de directorio) | medio (afecta rutas citadas en la tesina) | 🟠 medio |
| 5 | C8 (indexador) + C9 (.gitignore) | bajo | 🟠 medio |
| 6 | C7 (snapshot de prompts) + C10 (matriz en el script) | bajo | 🟡 normal |

> **Importante sobre C2:** la tesina cita rutas literales
> (`results/benchmark_balanced_120_20260901_140421/`). Los directorios existentes **no deben
> renombrarse**; la convención nueva aplica solo a corridas futuras.
