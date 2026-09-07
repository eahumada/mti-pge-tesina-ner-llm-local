# Diagnóstico `gpt-oss:20b` — encargo GPTOSS

**Fecha:** 2026-09-07 · **Equipo Remoto 48 GB** · Encargo: `ENCARGO-REMOTO-GPTOSS-20260907.md`

## Método
Re-ejecución de 5 registros baseline que fallaron (recall=0 en `excluidos_n120_REMOTO`):
`real_mixed_9, 21, 22, 23, 27`. Pipeline directo (system prompt + `News text:` + texto), params oficiales
(temp 0.1, seed 42, num_predict 2048). Dos condiciones: **tal cual** y **`repeat_penalty=1.2` + `repeat_last_n=256`**.
Respuesta cruda íntegra guardada en `results/diag_gptoss.json`.

## Resultados

| record | as-is: bucle | JSON cierra | len | eval_count | lat | repeat_penalty: bucle |
|:---|:--:|:--:|--:|--:|--:|:--:|
| real_mixed_9 | **No** | Sí | 248 | 1451 | 36s | No |
| real_mixed_21 | **No** | Sí | 254 | 1500 | 31s | No |
| real_mixed_22 | **No** | Sí | 190 | 482 | 10s | No |
| real_mixed_23 | **No** | Sí | 291 | 664 | 14s | No |
| real_mixed_27 | **No** | Sí | 969 | 1841 | 39s | No |

**Bucle de repetición: 0/5.** Todas produjeron **JSON limpio y cerrado con entidades correctas** (con tildes:
"Rodríguez", "Cáceres", "Mérida"). Ejemplo real_mixed_9 as-is:
`{"Persons":["Juan Carlos Rodríguez Ibarra",...],"Organizations":[...],"Locations":["Aldehuela (Cáceres)","Mérida"]}`

## Hallazgos

1. **La hipótesis del bucle de repetición NO se reproduce** en estos 5. `repeat_penalty` es irrelevante aquí
   (no hay bucle que eliminar). Las 2 muestras que el log del equipo mostró con bucle son minoritarias o
   dependientes de condición (posiblemente *thinking* consumiendo `num_predict` en la corrida oficial y
   truncando → *fallback* → vacío; aquí las salidas fueron cortas y limpias).
2. **Las 5 filas con recall=0 oficial RECUPERAN output válido** al re-ejecutar → el recall=0 es un
   **artefacto de la corrida/arnés**, no incapacidad del modelo (análogo a `nemotron-mini`, pero aquí es el
   32 % de la corrida, no 7 filas).
3. **Mojibake (F46) contribuye.** Corrigiendo el gold, real_mixed_21 sube F1 0.667→0.741 (+0.074). En otros
   no cambia (el gold de esos no tiene mojibake relevante o la falla es otra).
4. **Mojibake — veredicto (lo más importante del encargo):** el mojibake **SÍ afecta la comparación con el
   ground truth**, no es solo la codificación del log. 283/1406 gold del N=120 (20 %) tienen mojibake; 66
   (4.7 %) son irrecuperables (ver `FINDINGS.md §F46`). Afecta a **todos los modelos**, no solo gpt-oss.

## Recomendación (decisión del autor)

`gpt-oss:20b` **necesita re-ejecución completa** (no parchear las 76 filas — sería sesgo al alza sobre el 32 %
de la corrida). La re-ejecución debe hacerse con:
- **thinking ON** (decisión firme; think OFF le baja F1 −0.12, ver §F44/§F45), pero
- **`num_predict` mayor** (p. ej. 4096) para que el razonamiento no trunque la respuesta y caiga a *fallback*, y/o
- **parser tolerante** que rescate el prefijo JSON válido de una respuesta sin cerrar, y
- **gold sin mojibake** al puntuar (afecta a todo el estudio N=120, no solo a gpt-oss).

**ETA re-ejecución `gpt-oss:20b` completo N=120 × 2 modos:** con las latencias medidas (~10-40s/registro sin
truncar, vs 838s de los fallos oficiales) → **~1-1.5 h**. Mucho menor que el estimado original de 2.5 h.

> La decisión de re-ejecutar (y de corregir el mojibake en todo el N=120, que exige re-inferir) es del autor.
> El equipo remoto puede lanzarlo en cuanto se apruebe.

## Verificaciones
Promediado con `if x.get('k') is not None`. Raw íntegro en `results/diag_gptoss.json` (3+ ejemplos completos).

---

## ✅ RE-EJECUCIÓN COMPLETA (num_predict 4096, thinking ON) — confirma el diagnóstico

`results/gptoss_rerun_REMOTO/` — 240/240, **0 failed** (238 direct_json + 2 fallback).

| Condición | Oficial (contaminada) | Re-run 4096 | Δ | recall=0 |
|:---|--:|--:|--:|--:|
| baseline | 0.4467 | **0.5239** | +0.077 | 27 → **6** |
| kb_rag | 0.3419 | **0.5567** | **+0.215** | 49 → **5** |
| ΔRAG | −0.097 (anómalo) | **+0.033** (normal) | — | — |

**Conclusión.** El recall=0 oficial (76 filas, 32 %) era **truncación por thinking** con `num_predict 2048`;
subiendo a 4096 desaparece (11 residuales) y gpt-oss recupera su rendimiento real. **`gptoss_rerun_REMOTO` es
la fuente de verdad**; la corrida oficial `excluidos_n120_REMOTO` queda superada para gpt-oss. Requiere
re-fusionar el ANOVA con esta corrida.
