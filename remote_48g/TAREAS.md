# Lista de tareas — Equipo Remoto 48 GB

**Actualizado:** 2026-09-06 09:32

## ✅ Realizadas
- Verificación de entorno (48 GB, Ollama, repo, modelos ya locales — cero `pull`).
- Pre-checks: corpus 15/120, diccionarios 3605/1848/12000. Diccionarios **no** regenerados.
- Validación de inferencia real de `gemma4:31b` (trampa 03).
- Anti-suspensión `caffeinate -dimsu` (trampa 05).
- **P1** `gemma4:31b` N=15 — COMPLETADA, fallo 0/30, F1 0.6912/0.6391, VRAM 18.8 GB.
- **P2** `sonct988/gemma4-26b` N=120 — COMPLETADA, fallo 0/240, F1 0.5627/0.5964.
- Diagnóstico + fix del bug de routing `gpt-oss:20b` (`factory.py`, aprobado por el autor).
- Coordinación en `CURRENT-TASKS.md §3.bis` + §6 al día.
- Push de resultados parciales para el equipo principal (`remote_48g/`).
- Merge de cambios remotos concurrentes sin pérdida (política aditiva).
- Actualización de la URL del remote al repo movido.

## ▶️ En curso
- **P3** benchmark principal N=120, 7 modelos — 1137/1680 (~68%), fallo 0.
  - Completos válidos: `mistral-nemo`, `nuextract`.
  - Completos pero INVÁLIDOS (bug thinking, se re-corren): `gemma4:12b-mlx`, `qwen3:8b`.
  - En curso: `llama3.1:8b` (baseline 87/120).
  - Faltan: `llama3.1:8b` kb_rag, `nemotron-mini:4b`, `deepseek-r1:1.5b`.

## ⏳ Por realizar
- **P4** estudio de ablación de prompts (`gemma4:latest`, `--ablation`) — regenera 4 cifras (ZS/FS × EN/ES)
  que el informe cita sin dato crudo.
- **P2 (completar)** re-corrida de `gpt-oss:20b` con el routing ya corregido → estudio 13 → 14 modelos.
- **Re-corrida modelos afectados por bug thinking** (`gemma4:12b-mlx`, `qwen3:8b`) con el fix `743054d`, en
  `results/afectados_thinking_n120_REMOTO/`. Encolada tras gpt-oss. Ref: `ALERTA-EQUIPO-REMOTO-20260906.md`.
  El equipo principal fusiona.
- Verificación final de tasa de fallo por tarea antes de dar cifras por buenas (incl. recall=0 residual en
  los afectados: criterio de aceptación del alerta §4.3).
- Copia definitiva de las corridas a `remote_48g/results/` + push de cierre.
- Reflejar el fix de routing en `AGENTS.md §8.2` (contradicción `gpt-oss` Local vs regla `gpt-*→OpenAI`).

## Alertas recibidas del equipo principal
- 🔴 `ALERTA-EQUIPO-REMOTO-20260906.md`: bug thinking invalida `gemma4:12b-mlx` + `qwen3:8b`. Fix ya en árbol.
  Acción tomada: re-corrida encolada de esos 2 (arriba).
- 📄 `INFORME-AVANCE-20260906.md`: ANOVA conjunto 9 modelos (F=64.06, p=7.26e-177); `sonct988` (recuperado
  por este equipo) **lidera** el ranking N=120; hallazgo RAG diferencial (modelos pequeños ganan, grandes pierden).

## Orden de ejecución restante
P3 → P4 → re-run `gpt-oss` → re-run afectados (`gemma4:12b-mlx`, `qwen3:8b`).
Serialidad: un modelo local a la vez (trampa 06).
