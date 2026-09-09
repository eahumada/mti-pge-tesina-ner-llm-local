# Consolidado corregido tras el arreglo del TypeError §F85 (2026-09-09)

Este consolidado **sustituye** a `ANALISIS_CONJUNTO_20260909/`, que incluía la corrida buggy de
`nemotron-mini:4b` baseline con 18 filas `parse_method='failed'` (TypeError de `llm_runner.py:167`, §F85).

## Qué cambió

- **Arreglo:** `_normalize_keys` acepta ahora arrays JSON de nivel superior (fusiona `[{...}]`), en vez de
  reventar con `'list' object has no attribute 'items'`. Ver `FINDINGS §F85`.
- **Re-corrida** de `nemotron-mini:4b` N=120 con el código arreglado: **0 TypeErrors, failed=0**, VÁLIDA,
  TP+FN 1098/1500/1034.
- **`nemotron-mini:4b`**: baseline `0,2629 → 0,2829` (recuperadas las 18 filas), kb_rag `0,4055` (sin
  cambio). ΔRAG `+0,142 → +0,123`. Sigue siendo el mayor efecto del estudio y significativo (Tukey).
- **ANOVA consolidado:** `F = 121,56 → 119,7502`, p ≈ 0. La conclusión no cambia; la magnitud sí, como
  anticipaba `remote_48g/ALERTA-NEMOTRON-BASELINE-20260909.md`.

## Conservado como evidencia

> **Actualizado el 2026-09-09.** Lo que sigue **dejó de ser cierto** ese mismo día: por instrucción
> del autor —«en el estudio deben existir solo corridas y *benchmarks* exitosos, no conservar nada
> defectuoso»— la corrida se **retiró** en el commit `3716790`, y el directorio ya no existe. Se deja
> el texto original abajo porque esta nota es parte del registro y la política del proyecto es
> aditiva, pero **no describe el estado actual del repositorio**.
>
> La evidencia del defecto **sobrevive como registro**: los 58 mensajes del `TypeError`, los 18
> registros con `parse_method='failed'` y los 18 con latencia 0 y 0 tokens están escritos con sus
> cifras en `FINDINGS §F85`, `§F108` y `§F113`. Lo que ya no hay es el fichero.

~~La corrida buggy se conserva en `results/recorrida_20260908/nemotron-mini_4b__N120_F85_BUGGY/` con su
`benchmark.log` (58 mensajes del TypeError), porque es la prueba del defecto. No se borra.~~

## Verificación del protocolo reforzada

`tools/verificar_corrida.py` ahora hace **bloqueante** `parse_method='failed'==0` (§F108): la corrida buggy
que antes pasaba por VÁLIDA con 18 fallos ahora da NO VÁLIDA. Comprobado.
