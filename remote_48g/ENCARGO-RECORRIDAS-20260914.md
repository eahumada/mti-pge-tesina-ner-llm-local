# Encargo de re-corridas — Equipo 48 GB
**Creado:** 2026-09-14 · **Por:** Antigravity (coordinación) · **Basado en:** hallazgos del autor

> ## CIERRE DEFINITIVO DEL ENCARGO — Instrucción del autor, 2026-09-17
>
> **El encargo está 100% completo y CERRADO. No se ejecuta ninguna corrida más, bajo ningún concepto.**
> R1 Fase 1, R1 Fase 2, R2 (5/5 semillas, 13 200 evaluaciones, 0 fallidas), R3, R4 y R5 terminaron y están
> verificadas directamente contra los datos crudos (`CURRENT-TASKS.md §1.339`, `FINDINGS.md §F186`). R6
> (método del +10,01/+2,19) queda sin respuesta del remoto y **se retira sin más espera**: no bloquea nada,
> la conclusión no cambia con ninguna de las dos cifras candidatas.
>
> **Instrucción explícita: no volver a correr nada de lo que este documento pedía, ni una repetición, ni
> una variación, ni una limpieza.** Los resultados que hoy están en el repositorio bajo `results/` son
> **los últimos y los únicos que cuentan** para el informe. Si en el futuro se detecta un defecto en un
> dato ya publicado, la corrección se declara y se documenta (ver `CLAUDE.md`, Integridad de la medición);
> no se dispara una nueva corrida para «arreglarlo» sin que el autor lo pida expresamente y por escrito.
>
> **Este documento queda congelado como registro histórico de lo que se pidió y cómo se resolvió.** No se
> le añaden peticiones nuevas. Cualquier trabajo nuevo sobre el equipo remoto de 48 GB requiere un encargo
> nuevo, explícito, con su propio documento.


> **Instrucción del autor, 2026-09-15: el encargo se ejecuta completo, sin excepciones ni pausas por
> criterio propio.** R1 Fase 2 (N=120) y R2 no están canceladas ni son opcionales: quedaron **pendientes**,
> no descartadas, y deben ejecutarse en cuanto termine lo que esté en curso (R5 u otra). **Las decisiones
> sobre qué se corre y qué se omite se toman en el equipo principal, no en el equipo remoto.** Si algo de
> este documento parece redundante, de bajo valor o innecesario, la instrucción es señalarlo en
> `CURRENT-TASKS.md` y esperar respuesta — no omitirlo por criterio propio. El estado de todo el encargo se
> repasa en cada pasada de coordinación; lo que siga marcado aquí como pendiente sigue exigido hasta que se
> declare completado o el autor lo retire explícitamente.

> **Reconciliado 2026-09-14 ~21:00 por Claude Code (equipo principal), tras una colisión de edición
> concurrente con Antigravity sobre este mismo fichero** (ver `CURRENT-TASKS.md §1.309`). Se conserva
> íntegra la redacción y los comandos de Antigravity; se **corrige R4**, que aquí decía «no recomendado»
> contra una instrucción del autor posterior y explícita, y se **añaden R5 y R6**, que la versión de
> Antigravity no incluía. Nada se resta de lo que Antigravity escribió salvo la recomendación de R4.
>
> **Instrucción del autor, 2026-09-14, posterior a la redacción original de este documento: «no permitir
> fisuras en la tesis, correr lo que sea necesario; los costes son locales y la máquina de 48 GB está
> destinada solo a esto».** Con ella, **todas las peticiones de este documento son imprescindibles**, R4
> se ejecuta, y el criterio de priorización deja de ser el coste y pasa a ser **qué desbloquea antes una
> parte del informe**.

> **Leer CURRENT-TASKS.md antes de empezar.** Escribir entrada en §3.bis al iniciar cada tarea,
> actualizarla al terminar. Trabajar en `main`. Commitear y pushear al terminar cada corrida.

---

## Contexto: hallazgos que motivan este encargo

### §F175 — corregido (criterio de exclusión f1==0 erróneo)
El criterio `f1==0 OR fallback` mezclaba tres cosas distintas. Con el criterio estricto
(`tp+fp==0 AND fallback`) el efecto del RAG pasa de +13,71 a **+13,04**, y nueve modelos no
cambian nada. De los 20 ceros de `nemotron-mini`, 18 son fallos del modelo (extrajo entidades y
erró todas), **no averías**. La conclusión 1 se sostiene. §F174 (+10,40) se sostiene íntegro.

### R2 — hallazgo nuevo: variabilidad no declarada
Dos corridas con modelo, corpus, semilla 42, temperatura 0,1, max_tokens y prompt **idénticos**
dieron **64,05 y 66,76 de F1** en la misma celda. El estudio entero es de una sola pasada:
ninguna cifra publicada tiene barra de error conocida. **Es lo primero que pregunta un tribunal.**

---

## Tabla de re-corridas

| ID | Qué | Coste estimado | Arregla |
|---|---|---|---|
| **R1** | Variantes 2×2 × 5 semillas, N=15 y N=120 | 45 min (N=15) + 6-7 h (N=120) | §5.2, Tabla 5, §6.1, conclusión 2 |
| **R2** | Barra de error del titular (13 modelos × 5 semillas × N=120) | 8-10 h, nocturno | Tabla 7 |
| **R3** | Instrumentación: respuesta cruda íntegra, 2 columnas, reintento declarado | Solo código | Auditabilidad futura |
| **R4** | Corpus N=30 **traducido al español** (par emparejado) | ~2 h | Anexo F (`§F54`); imprescindible por instrucción del autor |
| **R5** | Variantes 2×2 sobre el par emparejado EN/ES del N=30 | ~2,5 h | el experimento de idioma bien planteado — hoy se mide solo sobre texto inglés |
| **R6** | Método del `+10,01`/`+2,19` del manifiesto (`§3.bis.17`) | sin cómputo | una cifra hoy incitable, pendiente desde 2026-09-08 |

---

## R1 — Variantes 2×2 con 5 semillas (PRIORITARIA)

### Objetivo
Medir el efecto real del idioma del prompt (español vs inglés) y del few-shot (ZS vs FS),
con intervalo de confianza. El experimento actual es N=15 todo en inglés — nunca fue el
experimento correcto para medir el efecto del idioma.

### Comandos

**Fase 1 — N=15 (validación rápida, ~45 min):**
```bash
cd repos/ner-llm-entity-benchmark
source venv/bin/activate

for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models gemma4:latest \
    --ablation \
    --data-file data/kleptotrace_balanced_15.json \
    --seed $SEED \
    --num-workers 4 \
    --results-dir results/variantes_5semillas_n15_REMOTO/seed_${SEED}
done
```

**Fase 2 — N=120 (resultado principal, ~6-7 h):**
```bash
for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models gemma4:latest \
    --ablation \
    --data-file data/benchmark_balanced_120.json \
    --seed $SEED \
    --num-workers 4 \
    --results-dir results/variantes_5semillas_n120_REMOTO/seed_${SEED}
done
```

### Verificación tras cada semilla
```bash
python3 tools/verificar_corrida.py results/variantes_5semillas_n15_REMOTO/seed_42
# failed == 0 obligatorio; ablation = True en run_config.json
```

### Entregables
- `results/variantes_5semillas_n15_REMOTO/seed_{42,123,456,789,1024}/`
- `results/variantes_5semillas_n120_REMOTO/seed_{42,123,456,789,1024}/`
- Cada directorio: `benchmark_results.csv`, `detailed_results.json`, `run_config.json`, `benchmark.log`

---

## R2 — Barra de error del titular (NOCTURNA)

### Objetivo
Cuantificar la variabilidad del F1 por modelo en N=120 con 5 semillas distintas.
Permite reportar el F1 como `μ ± σ` en la Tabla 7.

### Comandos
```bash
MODELS="gemma4:31b-cloud gemma4:31b-mlx gemma4:12b-mlx gemma4:latest \
        qwen3:8b gpt-oss:20b mistral-nemo:latest llama3.2:latest \
        llama3.1:8b nemotron-mini:4b deepseek-r1:1.5b"

for SEED in 42 123 456 789 1024; do
  python3 src/main.py \
    --models $MODELS \
    --rag-study \
    --rag-mode kb_combined \
    --data-file data/benchmark_balanced_120.json \
    --seed $SEED \
    --num-workers 4 \
    --max-tokens 4096 \
    --results-dir results/barras_error_n120_REMOTO/seed_${SEED}
done
```

> ⚠️ **Lanzar por la noche.** ETA ~8-10 h. Usar `caffeinate -dimsu` para evitar suspensiones.
> Usar `--resume` si se interrumpe.

### Entregables
- `results/barras_error_n120_REMOTO/seed_{42,123,456,789,1024}/`
- Incluir `detailed_results.json` en cada directorio (ya no está en `.gitignore`)

---

## R3 — Instrumentación (solo código, no requiere GPU) — ✅ HECHO

**Estado: completado el 2026-09-14 20:29** (commit `738accd`). `src/main.py` ya añade `raw_response` y
`retry_count` al CSV de salida. No requiere más acción; se deja el detalle original para referencia.

### Objetivo
Que cada corrida futura guarde la **respuesta cruda íntegra** del modelo y el número real
de reintentos, en dos columnas adicionales del CSV.

### Cambios en `src/evaluator.py` o `src/worker.py`
Añadir al CSV de salida:
- `raw_response` — respuesta cruda completa del modelo (antes de parsear)
- `retry_count` — número de reintentos efectivos (0 = éxito en el primer intento)

Estos datos permiten:
1. Auditar casos de `parse_method='fallback'` sin re-inferir
2. Diagnosticar variabilidad (R2) a nivel de respuesta individual
3. Reproducir métricas futuras sin repetir la inferencia

### Sin re-corridas
Este cambio solo aplica a corridas futuras. Las corridas existentes no se rehacen.

---

## R4 — Corpus N=30 traducido al español (IMPRESCINDIBLE)

### Por qué se corrige la recomendación original

Este documento decía «no recomendado, a 16 días de la defensa el coste no justifica el beneficio». El autor
dio instrucción posterior y explícita en sentido contrario: **correr todo lo necesario, sin fisuras, sin que
el coste sea el criterio**, porque el cómputo es local y la máquina está dedicada. Bajo esa instrucción, dejar
sin cerrar un hueco documentado (`FINDINGS §F54`: el Anexo F transcribe un prompt generador en español cuya
salida versionada está en inglés) es exactamente la fisura que no se permite.

### Ya está construido: `tools/traducir_corpus_n30_es.py`

No hace falta escribirlo. Genera `data/kleptotrace_augmented_30_es.json` a partir del corpus inglés,
traduciendo el texto y conservando la anotación de referencia (personas, organizaciones y **también los
nombres de lugar**, instruidos al modelo traductor para que no cambien de forma) sin tocarla. Es la decisión
de diseño correcta: traducir sin re-anotar deja una entidad de referencia en inglés dentro de un texto en
español, lo cual habría que declarar como limitación conocida — no es una fisura, es un compromiso
documentado, y es preferible a introducir de nuevo el defecto de anotación que ya costó dos meses detectar en
`Locations` (`§F53`).

```bash
cd repos/ner-llm-entity-benchmark
source venv/bin/activate

# Genera data/kleptotrace_augmented_30_es.json (verificar que existe antes de seguir)
python3 tools/traducir_corpus_n30_es.py --resume
ls -la data/kleptotrace_augmented_30_es.json
```

**Verificación obligatoria antes de correr los modelos:** cada entidad de referencia debe aparecer
literalmente en el texto traducido. Un fallo aquí reproduce el defecto de `Locations` sobre un corpus nuevo.

```bash
python3 - <<'PYEOF'
import json
es = json.load(open('data/kleptotrace_augmented_30_es.json'))
en = json.load(open('data/kleptotrace_augmented_30.json'))
arts = es['dataset'] if isinstance(es, dict) and 'dataset' in es else es
faltan = 0
for a in arts:
    txt = a.get('text', '')
    for campo in ('name_entities', 'organizations', 'locations'):
        for ent in a.get(campo, []):
            nombre = ent if isinstance(ent, str) else ent.get('text', '')
            if nombre and nombre not in txt:
                faltan += 1
                print(f"FALTA: articulo {a.get('article_id')} campo {campo}: '{nombre}'")
print(f"\nTotal entidades sin coincidencia literal: {faltan}")
PYEOF
```

**Si `faltan > 0`**, no se continúa con las corridas: se ajusta el prompt del traductor y se regenera. Un
`faltan == 0` es condición de aceptación de este paso, igual que `failed == 0` lo es de una corrida.

### Correr los trece modelos sobre el corpus traducido

```bash
MODELS="gemma4:31b-cloud gemma4:31b-mlx gemma4:12b-mlx gemma4:latest \
        qwen3:8b gpt-oss:20b mistral-nemo:latest llama3.2:latest \
        llama3.1:8b nemotron-mini:4b deepseek-r1:1.5b qwen2.5:14b gemma:latest"

python3 src/main.py \
  --models $MODELS \
  --rag-study \
  --rag-mode kb_combined \
  --data-file data/kleptotrace_augmented_30_es.json \
  --seed 42 \
  --num-workers 4 \
  --max-tokens 4096 \
  --results-dir results/n30_espanol_REMOTO
```

**No se toca `kleptotrace_augmented_30.json` (inglés)**: queda intacto como el otro lado del par emparejado.

### Entregables
- `data/kleptotrace_augmented_30_es.json`, con el resultado de la verificación de cobertura arriba.
- `results/n30_espanol_REMOTO/`: `benchmark_results.csv`, `detailed_results.json`, `run_config.json`,
  `benchmark.log`.

---

## R5 — Variantes de prompt sobre el par emparejado EN/ES del N=30 (IMPRESCINDIBLE)

Con el corpus traducido de R4 ya existe un **par emparejado**: mismo contenido, mismas entidades, dos
idiomas. Esto es lo que convierte la pregunta del idioma del prompt en un experimento con respuesta limpia,
porque hoy §5.2 compara prompt inglés contra prompt español **sobre un corpus inglés** — la diferencia de
idioma del prompt se mide sin controlar el idioma del texto.

```bash
for CORPUS in data/kleptotrace_augmented_30.json data/kleptotrace_augmented_30_es.json; do
  for SEED in 42 123 456 789 1024; do
    python3 src/main.py \
      --models gemma4:latest \
      --ablation \
      --data-file $CORPUS \
      --seed $SEED \
      --num-workers 4 \
      --results-dir results/variantes_n30_parEmparejado_REMOTO/$(basename $CORPUS .json)/seed_${SEED}
  done
done
```

**Qué responde, y por qué son dos preguntas distintas:** el idioma del *prompt* cuando coincide con el del
texto (rama `_es`), y cuando no coincide (rama sin sufijo, inglés). Hoy esas dos preguntas están confundidas
en una sola cifra.

### Entregables
- `results/variantes_n30_parEmparejado_REMOTO/kleptotrace_augmented_30/seed_{...}/` (inglés)
- `results/variantes_n30_parEmparejado_REMOTO/kleptotrace_augmented_30_es/seed_{...}/` (español)

---

## R6 — Método del `+10,01` / `+2,19` (`§3.bis.17`, sin cómputo)

Pendiente desde el 2026-09-08, sin respuesta. Vuestro manifiesto declaraba que el KB RAG aporta **+10,01 pp**
sobre los siete artículos contaminados y **+2,19 pp** sobre los ciento trece restantes; recalculado aquí
desde los `detailed_results.json`, promediando el delta de cada modelo y luego entre los trece, salen
**+11,89** y **+3,16**. La conclusión no cambia con ninguna de las dos parejas de cifras, y las nuestras son
peores para el trabajo, de modo que no hay incentivo en preferirlas.

**Lo único que hace falta es el método:** ¿promediasteis los registros de los siete y de los ciento trece por
separado y restasteis, o promediasteis por modelo y luego entre modelos? ¿Sobre qué corridas? Con eso se
elige una cifra y se declara en vez de publicar dos sin saber cuál mide qué. Contestad en
`CURRENT-TASKS.md §3.bis`, no hace falta un commit de datos.

---

## Protocolo de entrega

1. `git pull` antes de empezar
2. Escribir entrada en `CURRENT-TASKS.md`, numerada `§3.bis.22` en adelante (`§3.bis.18`, `.20` y `.21` ya
   están tomados; comprobar con `grep -oE "§3\.bis\.[0-9]+" CURRENT-TASKS.md | sort -t. -k3 -n -u | tail -1`
   antes de escribir, porque ya hubo una colisión de numeración el mismo día)
3. Al terminar cada corrida: `python3 tools/verificar_corrida.py <directorio>`
4. `failed == 0` obligatorio. Si hay fallos, documentarlos antes de continuar
5. `git add results/<dir>/ && git commit -m "feat(remoto): R1/R2 semilla N"`
6. `git push`
7. Actualizar entrada en `CURRENT-TASKS.md` con F1 obtenido y estado final

---

## Orden de ejecución (todo imprescindible; el criterio es qué desbloquea antes)

1. **Ya en curso, no interrumpir:** R1 Fase 1 (N=15, ~45 min-1,7 h) — arrancada 20:08.
2. **A continuación:** R4 (traducir + verificar cobertura + correr, ~2 h) y R6 (sin cómputo, en paralelo).
3. **Esta noche:** R1 Fase 2 (N=120, 6-7 h) y R5 (par emparejado, ~2,5 h) — pueden ir en paralelo si la
   máquina lo permite; si no, R1 Fase 2 primero, es el resultado que más pesa en el cuerpo del informe.
4. **Noche siguiente:** R2 (barra de error, 8-10 h).
5. **Entregad cada petición en cuanto termine, no esperéis a tenerlo todo.** Cada una desbloquea una parte
   distinta del informe que se reescribe en paralelo a vuestras corridas.
