#!/usr/bin/env python3
"""Contraste PAREADO del efecto RAG por modelo (Wilcoxon signed-rank + Holm).

Motivación (dictamen del comité 2026-09-09): la conclusión titular «el KB RAG mejora en N de 13 modelos» es
una afirmación PAREADA Y POR MODELO —baseline y kb_rag se miden sobre los mismos 113 artículos dentro de cada
modelo—, de modo que el ANOVA de una vía sobre las 26 celdas no la sostiene: ignora el emparejamiento y
confunde el efecto MODELO con el efecto MODO. La prueba correcta es un Wilcoxon signed-rank pareado por modelo
sobre la diferencia F1(kb_rag) − F1(baseline), con corrección de Holm entre los 13 modelos. El recuento de
rechazos tras Holm es literalmente el «N de 13».

Reporta también la mediana de la diferencia (tamaño de efecto pareado) para distinguir significancia de
relevancia práctica. Auditable: los 13 p crudos y ajustados quedan visibles; no se elimina ninguna fila.

Uso:  python3 tools/wilcoxon_pareado.py results/ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv
"""
import sys, numpy as np, pandas as pd
from scipy import stats


def holm(pvals):
    p = np.array([1.0 if (v is None or np.isnan(v)) else v for v in pvals], float)
    k = len(p)
    order = np.argsort(p)
    adj = np.empty(k)
    prev = 0.0
    for i, o in enumerate(order):
        val = min(1.0, (k - i) * p[o])
        prev = max(prev, val)
        adj[o] = prev
    return adj


def main():
    csv = sys.argv[1] if len(sys.argv) > 1 else "results/ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv"
    df = pd.read_csv(csv)
    df["modo"] = df["model"].str.extract(r"_(baseline|kb_rag)$")[0]
    df["base"] = df["model"].str.replace(r"_(baseline|kb_rag)$", "", regex=True)

    filas = []
    for m, g in df.groupby("base"):
        b = g[g.modo == "baseline"].set_index("record_id")["f1"]
        r = g[g.modo == "kb_rag"].set_index("record_id")["f1"]
        idx = b.index.intersection(r.index)
        d = (r.loc[idx] - b.loc[idx]).values
        p = np.nan
        if len(d) >= 5 and not np.all(d == 0):
            try:
                _, p = stats.wilcoxon(r.loc[idx], b.loc[idx])
            except ValueError:
                p = np.nan
        filas.append({"modelo": m, "n": len(idx), "medianaΔ": float(np.median(d)), "p": float(p)})

    adj = holm([f["p"] for f in filas])
    for f, a in zip(filas, adj):
        f["p_holm"] = float(a)
    filas.sort(key=lambda x: x["p_holm"])

    print(f'{"modelo":22s} {"n":>3s} {"medΔ":>8s} {"p":>10s} {"p_holm":>9s}  sig')
    sig = 0
    for f in filas:
        s = "*" if f["p_holm"] < 0.05 else ""
        sig += bool(s)
        print(f'{f["modelo"]:22s} {f["n"]:3d} {f["medianaΔ"]:+8.4f} {f["p"]:10.2e} {f["p_holm"]:9.4f}  {s}')
    print(f"\nSignificativos tras Holm (α=0,05): {sig} de {len(filas)}")


if __name__ == "__main__":
    main()
