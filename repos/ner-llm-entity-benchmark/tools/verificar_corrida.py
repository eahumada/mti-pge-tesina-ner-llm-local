#!/usr/bin/env python3
"""Verificaciones obligatorias antes de declarar VÁLIDA una corrida (encargo §5).

Aplica sobre el directorio de una corrida las seis comprobaciones que el encargo
PROMPT-EQUIPO-REMOTO-RECORRIDA-COMPLETA-20260908 exige reportar explícitamente:

  1. fn agregado > 0 en CADA categoría puntuada. Si una categoría tiene fn==0 mientras
     fp>0, está puntuando contra el vacío (el defecto de Locations, FINDINGS §F53).
  2. Cero registros con recall > 1.0 (defecto de doble emparejamiento, §F49/§F50).
  3. Ninguna fila con F1 > media aritmética de precisión y exhaustividad (la media
     armónica nunca la supera; si lo hace, las tres cifras son incoherentes).
  4. Recuento de parse_method='failed' y de recall==0 por modelo, con su causa probable:
     latencia 0 y 0 tokens = rechazo de infraestructura; latencia alta con contenido
     vacío = el arnés pierde la respuesta.
  5. Los nueve parámetros de run_config.json, cotejados con una corrida de referencia
     si se pasa --referencia.
  6. Al promediar desde JSON se usa `is not None` (un F1 de 0.0 es un dato, no una
     ausencia): este script lo respeta y lo deja explícito.

Uso:  python3 tools/verificar_corrida.py results/<corrida>/ [--referencia results/<ref>/] [--json salida.json]

Código de salida: 0 si todas las comprobaciones bloqueantes pasan, 1 si alguna falla.
"""
import json, io, os, sys, argparse, collections

CATEGORIAS = ["Persons", "Organizations", "Locations"]
# Los nueve parámetros de corrida que deben coincidir con la referencia (§5.5).
PARAMS_CLAVE = ["temperature", "seed", "fuzzy_threshold", "max_tokens", "max_retries",
                "num_workers", "rag_mode", "data_file", "models"]


def cargar_detailed(run_dir):
    path = os.path.join(run_dir, "detailed_results.json")
    if not os.path.exists(path):
        return None, f"No existe {path}"
    d = json.load(io.open(path, encoding="utf-8"))
    recs = d if isinstance(d, list) else d.get("results", d.get("records", []))
    return recs, None


def cargar_config(run_dir):
    path = os.path.join(run_dir, "run_config.json")
    if not os.path.exists(path):
        return None
    return json.load(io.open(path, encoding="utf-8"))


def check_fn_por_categoria(recs):
    """§5.1: fn agregado y fp agregado por categoría."""
    fn = collections.Counter()
    fp = collections.Counter()
    presentes = set()
    for r in recs:
        per = r.get("metrics", {}).get("per_type", {})
        for c in CATEGORIAS:
            if c in per:
                presentes.add(c)
                fn[c] += per[c].get("fn", 0)
                fp[c] += per[c].get("fp", 0)
    problemas = []
    detalle = {}
    for c in sorted(presentes):
        detalle[c] = {"fn": fn[c], "fp": fp[c]}
        if fn[c] == 0 and fp[c] > 0:
            problemas.append(f"categoría '{c}': fn=0 con fp={fp[c]} (puntúa contra el vacío)")
    return (len(problemas) == 0), detalle, problemas


def check_recall_mayor_1(recs):
    """§5.2: ningún registro con recall > 1.0 (overall o por tipo)."""
    ofensores = []
    for r in recs:
        rid = r.get("record_id")
        if r.get("recall") is not None and r["recall"] > 1.0 + 1e-9:
            ofensores.append((rid, r.get("model"), "overall", r["recall"]))
        per = r.get("metrics", {}).get("per_type", {})
        for c, m in per.items():
            rc = m.get("recall")
            if rc is not None and rc > 1.0 + 1e-9:
                ofensores.append((rid, r.get("model"), c, rc))
    return (len(ofensores) == 0), ofensores


def check_f1_coherente(recs):
    """§5.3: F1 (media armónica) no puede superar la media aritmética de precisión y recall."""
    ofensores = []
    for r in recs:
        p, rc, f1 = r.get("precision"), r.get("recall"), r.get("f1")
        if None in (p, rc, f1):
            continue
        if f1 > (p + rc) / 2 + 1e-9:
            ofensores.append((r.get("record_id"), r.get("model"), p, rc, f1))
    return (len(ofensores) == 0), ofensores


def check_fallos_por_modelo(recs):
    """§5.4: recuento de parse_method='failed' y recall==0 por modelo, con causa probable."""
    por_modelo = collections.defaultdict(lambda: {"failed": 0, "recall0": 0,
                                                   "rechazo_infra": 0, "arnes_pierde": 0})
    for r in recs:
        m = r.get("model", "?")
        pm = str(r.get("parse_method", "")).lower()
        if pm == "failed":
            por_modelo[m]["failed"] += 1
        if r.get("recall") is not None and r["recall"] == 0.0:
            por_modelo[m]["recall0"] += 1
            lat = r.get("latency_sec", 0) or 0
            tps = r.get("tokens_per_sec", 0) or 0
            if lat == 0 and tps == 0:
                por_modelo[m]["rechazo_infra"] += 1
            elif lat > 0:
                por_modelo[m]["arnes_pierde"] += 1
    return {k: dict(v) for k, v in por_modelo.items()}


def check_config(cfg, ref_cfg):
    """§5.5: los nueve parámetros clave, cotejados con la referencia si existe."""
    if cfg is None:
        return False, {"error": "no hay run_config.json"}, []
    valores = {k: cfg.get(k) for k in PARAMS_CLAVE}
    discrepancias = []
    if ref_cfg is not None:
        for k in PARAMS_CLAVE:
            if cfg.get(k) != ref_cfg.get(k):
                discrepancias.append({"param": k, "corrida": cfg.get(k), "referencia": ref_cfg.get(k)})
    return (len(discrepancias) == 0), valores, discrepancias


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--referencia", help="directorio de corrida de referencia para cotejar run_config.json")
    ap.add_argument("--json", help="ruta donde volcar el informe")
    args = ap.parse_args()

    recs, err = cargar_detailed(args.run_dir)
    if err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(2)

    cfg = cargar_config(args.run_dir)
    ref_cfg = cargar_config(args.referencia) if args.referencia else None

    ok1, det_fn, prob_fn = check_fn_por_categoria(recs)
    ok2, ofens_recall = check_recall_mayor_1(recs)
    ok3, ofens_f1 = check_f1_coherente(recs)
    fallos = check_fallos_por_modelo(recs)
    ok5, valores_cfg, discrep = check_config(cfg, ref_cfg)

    informe = {
        "corrida": args.run_dir,
        "n_registros": len(recs),
        "check_1_fn_por_categoria": {"ok": ok1, "detalle": det_fn, "problemas": prob_fn},
        "check_2_recall_mayor_1": {"ok": ok2, "ofensores": ofens_recall},
        "check_3_f1_coherente": {"ok": ok3, "ofensores": ofens_f1},
        "check_4_fallos_por_modelo": fallos,
        "check_5_config": {"ok": ok5, "valores": valores_cfg, "discrepancias": discrep,
                           "referencia": args.referencia},
    }

    # Comprobaciones BLOQUEANTES: 1, 2, 3 y (si hay referencia) 5.
    bloqueantes = [ok1, ok2, ok3]
    if ref_cfg is not None:
        bloqueantes.append(ok5)
    todo_ok = all(bloqueantes)
    informe["veredicto"] = "VÁLIDA" if todo_ok else "NO VÁLIDA"

    print(json.dumps(informe, ensure_ascii=False, indent=1))
    if args.json:
        json.dump(informe, io.open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(0 if todo_ok else 1)


if __name__ == "__main__":
    main()
