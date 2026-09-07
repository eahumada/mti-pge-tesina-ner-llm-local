# Adenda al encargo — tarea nueva y consolidación de lo pendiente

**Fecha:** 2026-09-06
**De:** equipo de desarrollo principal
**Base:** `PROMPT-EQUIPO-REMOTO-48GB.md` · `ALERTA-EQUIPO-REMOTO-20260906.md`

> **Decisión del autor:** todo lo que queda pasa a vosotros. El equipo principal no ejecutará más
> corridas; su máquina de 16 GB queda libre y su corrida local se da por cerrada.

---

## 1. 🆕 TAREA NUEVA — `gemma4:31b-cloud` sobre N=120

### Por qué
Este modelo tiene una corrida sobre N=120 (`results/benchmark_balanced_120_20260824_173036/`) que es
**inservible**: **190 de 240 extracciones fallidas (79 %)** por errores de cuota, y además usó el modo RAG
legacy `entities`, no `kb_combined`.

Su único dato limpio es sobre **N=15** (F1 0,6699, 0 fallos), que sirve para la Tabla 2 pero **no** para el
estudio N=120. Por eso **no está** entre los 9 modelos del ANOVA conjunto.

### Por qué es viable ahora
- ✅ El modelo **responde** tras la reautenticación del autor (verificado 2026-09-06).
- ✅ **No consume RAM local** — puede correr **en paralelo** con vuestras corridas locales, sin esperar turno.
- ✅ Sumaría un **décimo modelo** al ANOVA.

### Comando

```bash
./venv/bin/python src/main.py \
  --data-file data/benchmark_balanced_120.json \
  --rag-study --rag-mode kb_combined \
  --results-dir results/gemma4_31b_cloud_n120_REMOTO \
  --models gemma4:31b-cloud \
  --batch-size 3 --num-workers 3
```

### ⚠️ Riesgo específico y criterio de parada
Es un modelo **cloud sujeto a cuota**. Su corrida anterior falló al 79 % por HTTP 429.

- **Comprobad la tasa de fallo a mitad de camino**, no solo al final. Si supera el **10 %**, **parad**: los
  promedios ya estarían contaminados (una extracción fallida puntúa recall 0 y hunde la media).
- Si aparecen 429, **esperad a que renueve la cuota** en vez de forzar. Un 429 es temporal.
- Si aparece **402**, avisad: sería una barrera de plan y no se resuelve esperando.

```bash
# a mitad de corrida y al final
python3 -c "
import csv, collections
r = list(csv.DictReader(open('results/gemma4_31b_cloud_n120_REMOTO/benchmark_results.csv')))
c = collections.Counter(x['parse_method'] for x in r)
fail = c.get('failed', 0)
print(f'fallos: {fail}/{len(r)} ({100*fail/len(r):.1f}%) · {dict(c)}')"
```

---

## 2. Consolidación — todo lo pendiente, en orden

| # | Tarea | Estado | Notas |
|--:|:---|:---|:---|
| 1 | **P3** principal N=120, 7 modelos | ▶️ En curso (62 %) | 5 modelos válidos; 2 afectados por el bug de *thinking* |
| 2 | **P4** configuraciones de prompt | ⏳ En cola | Regenera 4 cifras que no existen en ningún dato |
| 3 | **`gpt-oss:20b`** N=120 | ⏳ En cola | Con vuestro fix de enrutado |
| 4 | **Re-corrida de afectados** (`gemma4:12b-mlx`, `qwen3:8b`) | ⏳ En cola | Con el fix `743054d` ya en el árbol |
| 5 | 🆕 **`gemma4:31b-cloud`** N=120 | ⬜ **Nueva** | **Puede ir en paralelo** — no compite por RAM |

**Serialidad:** los locales, uno a la vez. El cloud (#5) **no** cuenta para esa restricción y puede lanzarse
ya, solapado con cualquier otro.

---

## 3. Estado al que se aspira

| Origen | Modelos |
|:---|--:|
| Corrida 2026-09-01 (equipo principal) | 5 |
| P3, modelos no afectados | 5 |
| Re-corrida de afectados | 2 |
| `gpt-oss:20b` | 1 |
| 🆕 `gemma4:31b-cloud` | 1 |
| **Total potencial** | **15** |

Frente a los 9 del ANOVA preliminar actual (`F=64,06 · p=7,26e-177`).

---

## 4. Recordatorios que siguen vigentes

Del encargo original y la alerta, lo que más nos ha costado:

1. **`--rag-mode kb_combined`** en todo lo de N=120. El default es `entities` y produce datos **no
   comparables** sin avisar.
2. **`--results-dir` siempre explícito.** Sin él, `--resume` reinicia desde cero en silencio.
3. **Verificad la tasa de fallo antes de dar cifras por buenas.** Un 6/15 de fallos convirtió un F1 real de
   0,66 en un 0,40 aparente.
4. **No regeneréis los diccionarios.** Son un snapshot del 27-jul con fuentes vivas.
5. **Distinguid el tipo de fallo** mirando `latency_sec` y `tokens_per_sec`:
   - latencia **0 s** y **0 tokens** → rechazo de infraestructura (esperar o pagar)
   - latencia **alta** y **miles de tokens** con `content` vacío → el arnés pierde la respuesta (tocar código)

---

## 5. Qué hace el equipo principal a partir de ahora

- **No ejecuta más corridas.** Su máquina queda libre y su corrida local se cierra donde está.
- **Fusiona y analiza** vuestras entregas con `src/merge_and_analyze.py`.
- **Verifica** cada entrega antes de incorporarla: tasa de fallo, protocolo, consistencia aritmética.
- **Mantiene** `FINDINGS.md`, `LEARNING.md` y `TODO-INFORME-FINAL.md`.

Reportad como hasta ahora en `CURRENT-TASKS.md §3.bis`. El reporte anterior fue impecable: las
verificaciones previas que documentasteis permitieron descartar rápido que el problema estuviera en los
datos cuando apareció el bug de *thinking*.
