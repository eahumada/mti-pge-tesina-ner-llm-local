#!/usr/bin/env python3
"""Recupera las localizaciones del corpus N=120 sin necesitar el script de muestreo original.

Responde a la decisión que el equipo remoto planteó en §2.bis.2: el corpus de ciento veinte artículos
perdió las localizaciones que CoNLL-2002 sí anota, y no existe un pipeline de construcción reproducible
porque no se conservó el script que muestreó los 105 artículos de CoNLL.

**No hace falta ese script.** La correspondencia se recupera por el propio texto de los artículos, que es
único, con dos precauciones: hay que normalizar antes de comparar, porque el corpus del estudio tiene la
codificación reparada mientras la descarga fresca de la fuente la trae cruda, y hay que reparar también las
localizaciones recuperadas antes de escribirlas.

Verificado el 2026-09-08: empareja 105 de 120 artículos y recupera 482 localizaciones en 104 de ellos. Los
quince artículos de Kleptotrace quedan con la lista vacía, porque su fuente no las anota, y eso debe
declararse en el informe como anotación parcial de esa categoría.

Uso:
    python3 download_conll2002.py                      # regenera la fuente CON localizaciones
    python3 tools/recuperar_locations_n120.py          # transfiere al corpus N=120
"""
import json, io, re, unicodedata, argparse, os

FUENTE = 'data/conll2002_es.json'
CORPUS = 'data/benchmark_balanced_120.json'


def repara_mojibake(t):
    """Deshace la doble codificación: bytes UTF-8 que se leyeron como Latin-1."""
    try:
        return t.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return t


def clave(t):
    """Texto normalizado para emparejar: sin acentos, sin dobles espacios, en minúsculas.

    La normalización es necesaria porque los dos lados difieren en codificación y espaciado, no en
    contenido. Comparar el texto literal empareja 1 de 120; normalizado, empareja 105.
    """
    t = repara_mojibake(t or '')
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', t).strip().lower()


def carga(p):
    d = json.load(io.open(p, encoding='utf-8'))
    return d['dataset'] if isinstance(d, dict) and 'dataset' in d else d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fuente', default=FUENTE)
    ap.add_argument('--corpus', default=CORPUS)
    ap.add_argument('--salida', help='por omisión, sobrescribe el corpus')
    ap.add_argument('--dry-run', action='store_true', help='mide sin escribir')
    a = ap.parse_args()

    for p in (a.fuente, a.corpus):
        if not os.path.exists(p):
            raise SystemExit('no encuentro %s' % p)

    src = carga(a.fuente)
    if not any(r.get('locations') for r in src):
        raise SystemExit('la fuente %s NO tiene localizaciones: ejecuta primero download_conll2002.py '
                         'con el conversor corregido' % a.fuente)

    idx = {}
    for r in src:
        idx.setdefault(clave(r.get('text')), r)

    corpus = carga(a.corpus)
    emparejados = recuperadas = 0
    for r in corpus:
        k = clave(r.get('text'))
        if k in idx:
            r['locations'] = [repara_mojibake(x) for x in idx[k].get('locations', [])]
            emparejados += 1
            recuperadas += len(r['locations'])
        else:
            # Los quince artículos de Kleptotrace: su fuente no anota localizaciones.
            r['locations'] = []

    print('emparejados por texto normalizado : %d de %d' % (emparejados, len(corpus)))
    print('artículos con alguna localización  : %d' % sum(1 for r in corpus if r.get('locations')))
    print('localizaciones recuperadas         : %d' % recuperadas)
    print('sin emparejar (esperado: los 15 de Kleptotrace): %d' % (len(corpus) - emparejados))

    if a.dry_run:
        print('\n--dry-run: no se escribe nada')
        return
    salida = a.salida or a.corpus
    json.dump({'dataset': corpus}, io.open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\nescrito: %s' % salida)


if __name__ == '__main__':
    main()
