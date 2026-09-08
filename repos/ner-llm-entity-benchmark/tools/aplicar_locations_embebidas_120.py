#!/usr/bin/env python3
"""Aplica las 63 localizaciones de Kleptotrace al subconjunto embebido en el corpus N=120.
Encargo: remote_48g/RESPUESTA-LOCATIONS-EMBEBIDAS-20260908.md.

Empareja por TEXTO NORMALIZADO (NFKD, sin marcas de combinación, espacios colapsados, minúsculas) cada
artículo de data/kleptotrace.json con su homólogo en data/benchmark_balanced_120.json y vuelca su lista
`locations`. Solo rellena artículos con locations vacía (no toca las 482 recuperadas de CoNLL-2002).

Esperado: 15 de 15 emparejados; el corpus de 120 pasa de 104/482 a 119/120 y 545 localizaciones.

Uso:  python3 tools/aplicar_locations_embebidas_120.py [--dry-run]
"""
import json, io, re, sys, unicodedata

C120 = "data/benchmark_balanced_120.json"
KLEP = "data/kleptotrace.json"


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def registros(d):
    return d if isinstance(d, list) else d.get("dataset", d.get("data", d.get("records", [])))


def main():
    dry = "--dry-run" in sys.argv
    d120 = json.load(io.open(C120, encoding="utf-8"))
    r120 = registros(d120)
    rklep = registros(json.load(io.open(KLEP, encoding="utf-8")))

    klep_by_text = {norm(r.get("text", "")): (r.get("locations", []) or []) for r in rklep}

    emparejados = 0
    aplicados = 0
    locs_antes = sum(len(r.get("locations", []) or []) for r in r120)
    for r in r120:
        locs = klep_by_text.get(norm(r.get("text", "")))
        if locs is None:
            continue
        emparejados += 1
        if not (r.get("locations") or []):
            r["locations"] = list(locs)
            aplicados += 1

    con = sum(1 for r in r120 if r.get("locations"))
    tot = sum(len(r.get("locations", []) or []) for r in r120)
    print(f"emparejados kleptotrace<->120 : {emparejados} de {len(rklep)}")
    print(f"artículos rellenados          : {aplicados}")
    print(f"localizaciones antes / después: {locs_antes} / {tot}")
    print(f"artículos con locations        : {con} de {len(r120)}")

    if dry:
        print("--dry-run: no se escribe nada")
        return
    json.dump(d120, io.open(C120, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"escrito: {C120}")


if __name__ == "__main__":
    main()
