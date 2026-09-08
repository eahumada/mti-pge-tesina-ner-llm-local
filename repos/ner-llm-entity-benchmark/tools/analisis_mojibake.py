#!/usr/bin/env python3
"""Efecto del mojibake sobre el F1, por modelo y por criterio de «artículo afectado».

Reproduce la tabla del Anexo H.3 del informe final. Se publica porque la versión
anterior de esa tabla no era reproducible: declaraba una partición de 88/31
—cuya suma es 119 y no 120— y unos deltas que no se obtienen con ninguno de los
dos criterios naturales.

El punto de fondo es que **el signo del efecto depende del criterio elegido**, de
modo que declarar el criterio no es un detalle de forma sino parte del resultado.

Uso:  python3 tools/analisis_mojibake.py [--json salida.json]
"""
import json, io, glob, collections, re, argparse, os

MOJIBAKE = re.compile(r'Ã|Â|â€|Ã‚')
CORPUS = 'data/benchmark_balanced_120.json'
CORRIDAS = ['results/benchmark_balanced_120_20260901_140421/detailed_results.json',
            'results/benchmark_n120_REMOTO/detailed_results.json',
            'results/gemma4_31b_cloud_n120_REMOTO/detailed_results.json',
            'results/qwen3_nothink_n120_REMOTO/detailed_results.json',
            'results/nemotron_rerun_n120_REMOTO/detailed_results.json',
            'results/gptoss_rerun_REMOTO/detailed_results.json']


def corrupto(x):
    return bool(MOJIBAKE.search(x or ''))


def particiones(corpus):
    """Devuelve los dos criterios de «afectado» como conjuntos de article_id."""
    por_entidad, por_texto, todos = set(), set(), set()
    for r in corpus:
        i = str(r['article_id'])
        todos.add(i)
        if any(corrupto(e) for e in (r.get('name_entities', []) + r.get('organizations', []))):
            por_entidad.add(i)
        if corrupto(r.get('text', '')):
            por_texto.add(i)
    return todos, por_entidad, por_texto


def delta(registros, afectados):
    """F1 medio de los afectados menos F1 medio de los no afectados."""
    con = [r['f1'] for r in registros if str(r.get('record_id')) in afectados]
    sin = [r['f1'] for r in registros if str(r.get('record_id')) not in afectados]
    if not con or not sin:
        return None
    return sum(con) / len(con) - sum(sin) / len(sin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', help='ruta donde volcar el resultado')
    args = ap.parse_args()

    corpus = json.load(io.open(CORPUS, encoding='utf-8'))['dataset']
    todos, por_entidad, por_texto = particiones(corpus)

    grupos = collections.defaultdict(list)
    for f in CORRIDAS:
        if not os.path.exists(f):
            continue
        d = json.load(io.open(f, encoding='utf-8'))
        recs = d if isinstance(d, list) else d.get('results', d.get('records', []))
        for r in recs:
            # `is not None`: un F1 de 0.0 es un dato, no una ausencia
            if r.get('model') and r.get('f1') is not None:
                grupos[r['model']].append(r)

    filas = []
    for m, rs in sorted(grupos.items()):
        if len(rs) != 120:
            continue
        filas.append({'grupo': m,
                      'delta_por_entidad': delta(rs, por_entidad),
                      'delta_por_texto': delta(rs, por_texto)})

    salida = {
        'fecha': '2026-09-08',
        'corpus': CORPUS,
        'particion_por_entidad_de_referencia': {'afectados': len(por_entidad),
                                                'no_afectados': len(todos) - len(por_entidad)},
        'particion_por_texto_de_entrada': {'afectados': len(por_texto),
                                           'no_afectados': len(todos) - len(por_texto)},
        'nota': ('El signo del efecto depende del criterio: por entidad de referencia corrupta la mayoría de '
                 'los modelos puntúa MEJOR en los artículos afectados, y por texto de entrada corrupto puntúa '
                 'PEOR. La tabla anterior del Anexo H.3 no se reproduce con ninguno de los dos.'),
        'filas': filas,
    }
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    if args.json:
        json.dump(salida, io.open(args.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
