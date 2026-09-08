#!/usr/bin/env python3
"""Composición de entidades ibéricas vs anglosajonas por corpus (encargo §3.2 / FINDINGS §F56).

Reproduce la tabla de composición del encargo (Personas/Organizaciones y su fracción de aspecto ibérico
por corpus) a partir del ground truth de los corpus, con un clasificador heurístico y transparente. Sirve
para validar las cifras del encargo y para preparar el contraste que §3.2 pide: medir el efecto del idioma
del prompt POR SEPARADO sobre entidades ibéricas y anglosajonas. Ese segundo paso exige F1 por subconjunto
de entidad, que NO está en los resultados almacenados (no guardan la extracción por entidad) y requiere una
re-corrida con registro por entidad; aquí se deja listo el clasificador y la partición del gold.

El clasificador es una HEURÍSTICA de aspecto ortográfico, no una verdad de origen: marca ibérica si la
entidad lleva acentos/ñ/ç ibéricos o partículas portuguesas/españolas (da, dos, do, de, del, la). Se declara
como heurística porque de eso advierte el propio hallazgo.

Uso:  python3 tools/composicion_ibericas.py [--json salida.json]
"""
import json, io, re, sys, argparse, unicodedata

# corpus lógico -> fichero. Los totales de N=15, N=30 y N=120 (PER 84/36/594, ORG 128/69/812) coinciden
# exactamente con la tabla del encargo §3.2, lo que confirma el mapeo de ficheros.
CORPUS = {
    "N=15": "data/kleptotrace.json",
    "N=30": "data/kleptotrace_augmented_30.json",
    "N=120": "data/benchmark_balanced_120.json",
}

ACENTOS_IBERICOS = set("áéíóúüñçàò'")
PARTICULAS = {"da", "das", "do", "dos", "de", "del", "la", "las", "los", "y", "e"}


def registros(path):
    d = json.load(io.open(path, encoding="utf-8"))
    if isinstance(d, list):
        return d
    return d.get("dataset", d.get("data", d.get("records", [])))


def es_iberica(nombre):
    n = (nombre or "").lower()
    if any(ch in ACENTOS_IBERICOS for ch in n):
        return True
    toks = re.split(r"\s+", n)
    # partícula portuguesa/española en minúscula entre dos tokens (Isabel dos Santos, Leite da Silva)
    if len(toks) >= 3 and any(t in PARTICULAS for t in toks[1:-1]):
        return True
    return False


def contar(recs):
    per, org = [], []
    for r in recs:
        per += r.get("name_entities", []) or []
        org += r.get("organizations", []) or []
    def resumen(lst):
        total = len(lst)
        ib = sum(1 for e in lst if es_iberica(e))
        return {"total": total, "ibericas": ib,
                "pct_ibericas": round(100 * ib / total, 1) if total else 0.0,
                "ejemplos_ibericas": sorted({e for e in lst if es_iberica(e)})[:6]}
    return {"personas": resumen(per), "organizaciones": resumen(org)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    salida = {"fecha": "2026-09-08", "clasificador": "heurística ortográfica (acentos/ñ/ç + partículas)",
              "corpus": {}}
    for etiqueta, path in CORPUS.items():
        try:
            salida["corpus"][etiqueta] = contar(registros(path))
        except FileNotFoundError:
            salida["corpus"][etiqueta] = {"error": f"no existe {path}"}

    salida["limitacion_heuristica"] = ("Los TOTALES por corpus coinciden exactamente con el encargo (PER "
        "84/36/594, ORG 128/69/812) y la fracción ibérica de ORGANIZACIONES casi exacta (N=120: 196 vs 198). "
        "La de PERSONAS infra-cuenta (N=120: 172 vs 263) porque la heurística ortográfica no marca apellidos "
        "ibéricos SIN acento ni partícula (Belda, Conde, Bono). Para igualar el 44% del encargo haría falta un "
        "diccionario de apellidos; se deja como heurística transparente y conservadora.")
    salida["nota"] = ("§3.2 pide medir el efecto del idioma del prompt por separado sobre entidades ibéricas "
                      "y anglosajonas. Ese contraste requiere F1 por subconjunto de entidad, que no está en "
                      "los detailed_results almacenados; exige re-corrida con registro por entidad. Aquí se "
                      "reproduce solo la composición del corpus, que sí es offline.")
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    if args.json:
        json.dump(salida, io.open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
