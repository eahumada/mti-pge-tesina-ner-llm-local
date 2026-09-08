#!/usr/bin/env python3
"""Efecto del idioma del prompt en la ablación, con réplicas y dispersión (encargo §3.3 / FINDINGS §F55).

El informe citaba solo la corrida más favorable (fs-es +10,40 pp sobre zs-en en N=15) cuando existen tres
corridas del mismo experimento y en N=120 el efecto se invierte a −0,43 pp (p=0,9328). Esta herramienta:

  1. Agrega TODAS las corridas de ablación disponibles (condiciones zs-en, zs-es, fs-es, fs-en).
  2. Reporta tres contrastes, no solo el publicado:
       - fs-es − zs-en : el contraste publicado (mezcla idioma + few-shot).
       - zs-es − zs-en : idioma PURO en zero-shot.
       - fs-es − fs-en : idioma PURO en few-shot.
  3. Da media y dispersión (desviación típica) de cada contraste ENTRE corridas.
  4. Avisa si hay menos de cinco réplicas por celda: §3.3 exige >=5 con semillas declaradas, y sin ellas el
     efecto no se puede declarar. Las réplicas nuevas exigen correr benchmark (fuera del alcance offline).

Promedia con `is not None` (un F1 de 0.0 es dato, no ausencia). Ignora la lista cerrada de modelos excluidos.

Uso:  python3 tools/analisis_ablacion_idioma.py [results/dir1 results/dir2 ...] [--json salida.json]
      sin argumentos, autodetecta corridas cuyo campo 'model' contiene condiciones zs-/fs-.
"""
import json, io, os, glob, sys, argparse, statistics

CONDICIONES = ["zs-en", "zs-es", "fs-es", "fs-en"]
CONTRASTES = [("fs-es", "zs-en", "publicado (idioma+few-shot)"),
              ("zs-es", "zs-en", "idioma puro, zero-shot"),
              ("fs-es", "fs-en", "idioma puro, few-shot")]
# Lista cerrada de modelos excluidos (CLAUDE.md): nunca deben aparecer.
EXCLUIDOS = {"nuextract:latest", "minimax-m3:cloud", "gemini-3.1-flash-lite", "gemini-3.5-flash",
             "phi3.5", "gliner:medium", "sonct988/gemma4-26b", "gemma4-12b-mlx-q8-64k"}


def cargar(run_dir):
    path = os.path.join(run_dir, "detailed_results.json")
    if not os.path.exists(path):
        return None
    d = json.load(io.open(path, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("results", d.get("records", []))


def f1_por_condicion(recs):
    """F1 medio por condición, usando is not None (0.0 es dato)."""
    acc = {c: [] for c in CONDICIONES}
    for r in recs:
        m = r.get("model")
        if m in EXCLUIDOS:
            continue
        if m in acc and r.get("f1") is not None:
            acc[m].append(r["f1"])
    return {c: (statistics.mean(v) if v else None, len(v)) for c, v in acc.items()}


def autodetectar():
    dirs = []
    for path in glob.glob("results/*/detailed_results.json"):
        recs = cargar(os.path.dirname(path))
        if recs and any(r.get("model") in CONDICIONES for r in recs):
            dirs.append(os.path.dirname(path))
    return sorted(dirs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dirs", nargs="*")
    ap.add_argument("--json")
    args = ap.parse_args()

    run_dirs = args.run_dirs or autodetectar()
    if not run_dirs:
        print("No se encontraron corridas de ablación con condiciones zs-/fs-.", file=sys.stderr)
        sys.exit(2)

    por_corrida = []
    for rd in run_dirs:
        recs = cargar(rd)
        if not recs:
            continue
        f1 = f1_por_condicion(recs)
        fila = {"corrida": os.path.basename(rd),
                "n_por_condicion": {c: f1[c][1] for c in CONDICIONES},
                "f1_medio": {c: (round(f1[c][0], 4) if f1[c][0] is not None else None) for c in CONDICIONES},
                "contrastes_pp": {}}
        for a, b, etiqueta in CONTRASTES:
            if f1[a][0] is not None and f1[b][0] is not None:
                fila["contrastes_pp"][f"{a}-{b}"] = round((f1[a][0] - f1[b][0]) * 100, 2)
            else:
                fila["contrastes_pp"][f"{a}-{b}"] = None
        por_corrida.append(fila)

    # Agregado entre corridas: media y dispersión de cada contraste.
    agregado = {}
    for a, b, etiqueta in CONTRASTES:
        clave = f"{a}-{b}"
        vals = [f["contrastes_pp"][clave] for f in por_corrida if f["contrastes_pp"].get(clave) is not None]
        agregado[clave] = {
            "etiqueta": etiqueta,
            "n_corridas": len(vals),
            "media_pp": round(statistics.mean(vals), 2) if vals else None,
            "desv_tipica_pp": round(statistics.stdev(vals), 2) if len(vals) > 1 else None,
            "valores_pp": vals,
        }

    # Réplicas por celda = número de CORRIDAS independientes (semillas) por condición, NO el número de
    # artículos. §3.3 exige >=5 semillas declaradas por celda. Cada corrida aquí aporta una sola réplica,
    # de modo que una condición tiene tantas réplicas como corridas la incluyan.
    repl_por_condicion = {c: sum(1 for f in por_corrida if f["n_por_condicion"][c] > 0) for c in CONDICIONES}
    max_repl = max(repl_por_condicion.values(), default=0)
    aviso = None
    if max_repl < 5:
        aviso = (f"Menos de 5 réplicas (semillas) por celda: máximo observado {max_repl} corrida(s) por "
                 "condición. §3.3 exige >=5 con semillas declaradas; sin réplicas nuevas (que requieren "
                 "correr benchmark, fuera del alcance offline) el efecto del idioma NO se puede declarar. "
                 "La dispersión entre las corridas existentes ya muestra que el signo no es estable.")

    informe = {"fecha": "2026-09-08", "corridas": por_corrida, "agregado_entre_corridas": agregado,
               "replicas_semilla_por_condicion": repl_por_condicion, "replicas_por_celda_max": max_repl,
               "aviso_replicas": aviso,
               "nota": ("El signo del efecto del idioma depende de la corrida y del contraste. El contraste "
                        "publicado mezcla idioma con few-shot; los contrastes de idioma puro lo aíslan.")}
    print(json.dumps(informe, ensure_ascii=False, indent=1))
    if args.json:
        json.dump(informe, io.open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
