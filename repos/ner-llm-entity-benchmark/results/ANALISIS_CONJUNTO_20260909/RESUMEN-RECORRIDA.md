# Resumen de la re-corrida completa (2026-09-09)

Re-corrida de los 13 modelos del estudio sobre el corpus N=120 con **todas las correcciones aplicadas**
(mojibake reparado, Locations recuperadas 545/119-de-120, doble emparejamiento corregido, presupuesto
unificado 4096, registro por entidad, exclusión de los 7 ejemplares contaminados). Ejecutada íntegramente en
el equipo de 48 GB, un modelo por turno, `num_workers=1`, `temperature=0.1`, `seed=42`, `fuzzy_threshold=85`,
`rag_mode=kb_combined`.

## Verificación

- **39/39 corridas VÁLIDAS** (13 modelos × 3 corpus) con `tools/verificar_corrida.py`.
- Los 13 N=120 con `TP+FN` = **1098 / 1500 / 1034** por categoría (corpus corregido confirmado).
- ANOVA sobre el conjunto (26 grupos, 113 registros, contaminados excluidos): **F = 121,56, p ≈ 0**.

## F1 por modelo (N=120, contaminados excluidos)

| Modelo | baseline | kb_combined | ΔRAG |
|:---|---:|---:|---:|
| gemma4:31b-cloud (nube) | 0,821 | **0,829** | +0,008 |
| gemma4:31b-mlx (local) | 0,815 | **0,824** | +0,010 |
| gemma4:12b-mlx | 0,777 | 0,800 | +0,023 |
| gemma4:latest | 0,753 | 0,779 | +0,025 |
| gpt-oss:20b | 0,754 | 0,771 | +0,017 |
| llama3.1:8b | 0,692 | 0,715 | +0,023 |
| qwen2.5:14b | 0,696 | 0,703 | +0,007 |
| llama3.2:latest | 0,633 | 0,700 | +0,067 |
| qwen3:8b | 0,690 | 0,690 | −0,001 |
| gemma:latest | 0,595 | 0,596 | +0,000 |
| mistral-nemo:latest | 0,606 | 0,563 | −0,043 |
| nemotron-mini:4b | 0,263 | 0,405 | **+0,142** |
| deepseek-r1:1.5b | 0,287 | 0,308 | +0,021 |

## Hallazgos

1. **El mejor local supera con holgura el umbral del 70 %**: `gemma4:31b-mlx` a **0,824** (kb_combined).
2. **El RAG contextual aporta más cuanto más débil es el modelo**: nemotron-mini +0,142 y llama3.2 +0,067,
   frente a ~+0,01 en los fuertes. Confirma el hallazgo central del estudio.
3. **Aviso al equipo principal (§6 del encargo).** La distancia entre la nube (0,829) y el mejor local
   (0,824) es de **~0,5 pp**, no los ~5 pp que anticipaba §6. La causa probable es que `gemma4:31b-mlx` es un
   local grande de la **misma familia** que el `gemma4:31b-cloud`, de modo que rivaliza con él; el «coste de
   soberanía de cinco puntos» se sostiene mejor frente a un local de tamaño desplegable en hardware modesto.
   Se declara la cifra observada, no se ajusta. Queda a criterio del autor cómo redactarlo.
4. **`gpt-oss:20b` corrió limpio** con el presupuesto unificado 4096: un solo respaldo frente a los 67 con
   2048. Cierra §2.bis.3.
