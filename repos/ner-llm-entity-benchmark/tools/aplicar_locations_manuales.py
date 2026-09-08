#!/usr/bin/env python3
"""Aplica la anotación manual de localizaciones a los corpus cuya fuente no las aporta.

Es el **paso siguiente** a `recuperar_locations_n120.py`, y hay que ejecutarlo después de él. Aquel recupera
las localizaciones que CoNLL-2002 sí anota y que el conversor descartaba, y cubre 105 de los 120 artículos.
Este cubre el resto: los quince de Kleptotrace y los treinta del corpus sintético, cuyas fuentes no anotan
esa categoría.

Sin los dos pasos, medir localizaciones sigue penalizando al modelo en los artículos sin anotar, que es
exactamente el defecto que `FINDINGS.md §F53` documenta.

La anotación vive en `data/anotaciones/locations_manuales.json`, que declara su criterio y su procedencia.
No se genera aquí: se lee, para que la anotación sea auditable y versionada por separado del código.

Uso:
    python3 tools/aplicar_locations_manuales.py --dry-run
    python3 tools/aplicar_locations_manuales.py
"""
import json, io, os, argparse

ANOT = 'data/anotaciones/locations_manuales.json'


def carga(p):
    d = json.load(io.open(p, encoding='utf-8'))
    return d, (d['dataset'] if isinstance(d, dict) and 'dataset' in d else d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--anotacion', default=ANOT)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if not os.path.exists(a.anotacion):
        raise SystemExit('no encuentro la anotación en %s' % a.anotacion)
    anot = json.load(io.open(a.anotacion, encoding='utf-8'))

    for ruta, bloque in anot['corpora'].items():
        if not os.path.exists(ruta):
            print('AVISO: no encuentro %s, se omite' % ruta)
            continue
        env, recs = carga(ruta)
        por_id = bloque['por_article_id']
        puestas = con = ya = 0
        for r in recs:
            i = str(r.get('article_id'))
            if r.get('locations'):
                ya += 1
                continue          # no se pisa una anotación existente
            L = por_id.get(i, [])
            r['locations'] = L
            if L:
                con += 1
                puestas += len(L)
        print('%-42s %3d artículos · %3d anotados · %3d localizaciones · %d ya tenían'
              % (ruta, len(recs), con, puestas, ya))
        if not a.dry_run:
            json.dump(env if isinstance(env, dict) and 'dataset' in env else recs,
                      io.open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n--dry-run: no se ha escrito nada' if a.dry_run else '\nescrito')


if __name__ == '__main__':
    main()
