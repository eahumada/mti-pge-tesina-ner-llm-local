# Hallazgo — el modo *thinking* de qwen3:8b no aporta y se desactiva

**Fecha:** 2026-09-06 · **De:** Equipo Remoto 48 GB · **Decisión del autor:** correr qwen3:8b con `think=False`.

---

## Contexto

El equipo principal detectó (ALERTA-EQUIPO-REMOTO-20260906, bug 2) que `think` se pasaba dentro de `options`
y Ollama lo ignoraba, por lo que `qwen3:8b` **siempre había corrido con thinking OFF**. El fix `743054d` lo
pasó como kwarg de primer nivel, activando thinking. Este hallazgo evalúa si ese cambio conviene.

## Comparación empírica (N=120, no una muestra)

Disponible sin coste extra: **P3 = qwen3 think OFF** (bug previo) vs **run limpio = qwen3 think ON** (fix):

| qwen3:8b | THINK OFF (P3, n=120) | THINK ON (limpio) |
|:---|--:|--:|
| **baseline F1** | **0.4483** | **0.4483** (n=120) |
| baseline latencia | 789 s | 517 s |
| kb_rag F1 | 0.4425 (n=120) | 0.3727 (n=6, parcial) |

- **baseline: F1 idéntico** (0.4483 con y sin thinking). El razonamiento no cambia la extracción final.
- **kb_rag con thinking ON va peor** en la muestra temprana (0.37 vs 0.44).
- Thinking además **agrava**: lentitud (GPU-bound; el kb_rag con think casi no avanza) y riesgo de respuestas
  vacías / thrash (ya observado con `gemma4:12b-mlx`).

> Nota: una prueba controlada de 5 artículos think ON vs OFF **falló 2 veces por inanición de GPU** (competía
> con el run en curso). La comparación N=120 de arriba es más sólida y no requiere esa prueba.

## Decisión y cambio aplicado

`qwen3:8b` se **saca** de `_QWEN3_THINKING_MODELS` y se **añade** a `_THINKING_DISABLED_MODELS`
(`src/providers/ollama_provider.py`). Verificado: `think_flag=False`, log `"Thinking DISABLED for 'qwen3:8b'"`.
Backup: `ollama_provider.py.bak_qwen3nothink_20260906`.

Corrida limpia think=false en `results/qwen3_nothink_n120_REMOTO/` (más rápida). El dato de qwen3 para el
estudio saldrá de aquí. *(Alternativa equivalente ya disponible: qwen3 de P3, que es think OFF completo.)*

## Recomendación al equipo principal

Reconsiderar la política de thinking para qwen3: en esta tarea NER **no mejora F1** y solo penaliza tiempo.
Los modelos `qwen3:14b/32b/latest` siguen con think ON por defecto (no evaluados aquí).
