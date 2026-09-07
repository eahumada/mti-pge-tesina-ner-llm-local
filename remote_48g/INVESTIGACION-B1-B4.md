# Investigación B1-B4 — auditoría de datos del informe final NER

**Fecha:** 2026-09-07 · **Equipo Remoto 48 GB** · **Destinatario:** equipo de desarrollo principal
**Método:** workflow de 4 agentes (investigación interna + web) + síntesis.
**Política:** aditiva; no borrar filas para cuadrar conteos. `.md` canónico primero, `.docx` vía `tools/docx_replace_terms.py` (no pandoc), verificar límite 25 pp.

---

## Nota preliminar — Hardware (CONFIRMADO por el autor)

El equipo de **48 GB de memoria unificada fue NECESARIO**, no un lujo. Los modelos de 31B (footprint operativo
~24,7 GB) **no caben en 16 GB**. Base del hallazgo B3.

---

## B1 — F1 imposibles en `BENCHMARKS.md` (líneas 240-241)

**CONFIRMADO.** `llama3.2:latest_rag` F1=0.8783 (cota 0.7646) y `llama3.1:8b_baseline` F1=0.7667 (cota 0.7334)
violan `F1 ≤ (P+R)/2` y **no son recuperables**: provienen de prototipos sobre el sample de 20 registros cuyo
CSV no se conservó. Búsqueda estricta de columna (`,0.8783` / `,0.7667`) → **cero filas** en cualquier CSV (las
apariciones sueltas son substrings de latencias).
- Existe `llama3.1:8b` real N=120 (`benchmark_n120_REMOTO`, CSV re-puntuado): **baseline 0.4876, kb_rag 0.5075**.
- ✅ **Corregido (2026-09-07):** no hay reconciliación pendiente. El `benchmark_summary.json` que daba 0.4959/0.5491
  era **pre-fix de scoring** (obsoleto); el valor correcto es **0.4876 / 0.5075** (CSV re-puntuado). Regla: hoy
  `benchmark_results.csv` es la única fuente válida de P/R/F1 (ver `results/AVISO-SUMMARIES-OBSOLETOS.md`).
- **No** existe corrida N=120 para `llama3.2:latest`.

**Recomendación:** marcar ambas como NO VERIFICABLES; reemplazar `llama3.1:8b` por N=120 (tras reconciliar);
retirar/degradar `llama3.2:latest_rag` a nota de prototipo. No borrar silenciosamente.

---

## B2 — §1.1 Mercado RegTech (atribución «KPMG 2024»)

**La cifra ~87.200M/2028 existe pero NO es de KPMG ni 2024.** Es de **Verified Market Research** (USD 15,68 mil M
2020 → USD 87,17 mil M 2028, CAGR 23,92% 2021-2028). La base 12.300M/2024 no coincide con ninguna fuente; el par
12.300M→87.200M en 4 años implicaría **CAGR ~63%**, incoherente con el 23,92% real. Atribución a KPMG no verificable.

**Recomendación:** sustituir marcador y cifras. **Texto sugerido:**
> Según Verified Market Research, el mercado global de RegTech se valoró en USD 15,68 mil millones en 2020 y se
> proyecta que alcance USD 87,17 mil millones hacia 2028, con una CAGR del 23,92% durante 2021-2028
> (Verified Market Research, 2022).

Fuente: PRNewswire 301497770 (VMR). Alternativas: Technavio (base 2024 real), Allied Market Research, IMARC.

---

## B3 — §2.4/§3.6 Contradicción de hardware (imposibilidad física)

**CONFIRMADO imposible.**
- 31B Q4_K_M: ~18,7 GB solo pesos + KV cache + overhead ≈ **20-25 GB operativos** (coherente con 24,7 GB).
- Techo de VRAM en Apple Silicon (Metal `recommendedMaxWorkingSetSize`) ≈ **75% de la RAM unificada** → en 16 GB, **~12 GB asignables**.
- **12 GB < 18,7 GB (solo pesos) << 24,7 GB.** No cabe **ni en serie con `keep_alive=0`** (ese flag evita retener varios modelos, no reduce el footprint de uno).
- **48 GB** → techo ~36 GB, aloja los 24,7 GB con holgura. Config mínima coherente.

**Recomendación:** reformular §2.4/§3.6 a **dos tramos: 16 GB para ≤~12B; 48 GB para 31B y MLX grandes.**
**Texto sugerido:**
> La ejecución se organizó en dos escalones de hardware según footprint. Los modelos de hasta ~12B (Q4) se
> ejecutaron en un M4 de 16 GB unificados: su footprint (~7-9 GB + KV cache) queda bajo el techo de VRAM que
> macOS/Metal asigna (~75% de la RAM, `recommendedMaxWorkingSetSize`, ~12 GB en 16 GB). Los modelos de 31B
> (gemma4:31b, Q4_K_M/MLX) tienen footprint ~24,7 GB (pesos ~18,7 GB + KV cache + overhead), que excede ese
> techo y no pueden cargarse en 16 GB ni en serie con `keep_alive=0`. Se ejecutaron en un equipo de **48 GB de
> memoria unificada** (techo ~36 GB), con holgura para KV cache y sistema operativo.

Fuente: willitrunai/avenchat/kaitchup (footprint); Apple Developer 732035, zenn.dev, stencel.io (techo 75%).

---

## B4 — §5.5 Tabla de eficiencia: VRAM/Tok-s no reproducibles

**Los valores del informe no reconcilian con los CSV** (`vram_mb`, `tokens_per_sec`):

| Fila | Informe §5.5 | CSV canónico N=15 (`_baseline`) | ¿Coincide? |
|:---|:---|:---|:---|
| `gemma4:31b-mlx` | 24,751 / 27.56 | **24,607 / 22.80** | No (`27.56`/`24751` = 0 en CSV) |
| `gemma4:31b` | 18,803 / 11.37 | 18,795 / 10.23 | VRAM ~sí, tok/s no |
| `llama3.2` (3B) | ~3,000 / 47.5 | 4,018 / 79.35 | No |

Única fila reproducible: `gemma4:31b-mlx` N=15 = 22.80 / 24,607 (coincide con TODO §10). El resto sin respaldo primario.

**Recomendación:** reemplazar por valores CSV canónico N=15, recalcular Índice Tok/s/B, nota al pie con fuente y N.
**Texto sugerido:**

| Modelo | VRAM (MB) | Tok/s | Parámetros (B) | Índice Tok/s/B | Costo/Artículo |
|:---|:--:|:--:|:--:|:--:|:--:|
| gemma4:31b | 18,795 | 10.23 | 31 | 0.33 | $0.052 |
| gemma4:31b-mlx | 24,607 | 22.80 | 31 | 0.74 | $0.052 |
| llama3.2 (3B) | 4,018 | 79.35 | 3 | 26.5 | $0.052 |

> Nota: valores medidos sobre `benchmark_results.csv` (subconjunto `_baseline`, N=15).

---

## Resumen de acciones

| # | Acción | Decisión del autor |
|:--|:---|:---|
| B1 | Retirar/degradar 2 F1 imposibles; reemplazar llama3.1:8b por N=120 | **Sí** — reconciliar 0.4876/0.5075 vs 0.4959/0.5491 |
| B2 | Reemplazar «KPMG 2024» por VMR (o Technavio) | Elegir fuente |
| B3 | Reformular §2.4/§3.6 a 16 GB / 48 GB | No (hardware confirmado) |
| B4 | Reemplazar tabla §5.5 por valores CSV | Solo si conserva cifras actuales (documentar fuente) |
