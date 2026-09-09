#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
acceptance_desfasado.py — Comprueba que cada `acceptance_status.json` concuerda con su resumen.

Por que existe
--------------
`acceptance_status.json` lo escribe `src/main.py` al cerrar una corrida, con el mejor F1, el
modelo que lo consigue y un veredicto `target_f1_met`. La correccion de puntuacion del
2026-09-06 rehizo los `benchmark_summary.json` pero **no** los `acceptance_status.json`, de modo
que siete corridas quedaron con un veredicto calculado sobre cifras que ya no existen.

Nada del analisis lo lee —solo `src/dashboard.py`, que es visualizacion—, asi que **no contamina
las metricas del estudio**. Importa por otras dos razones:

  1. Es la fuente de la cifra equivocada que circula. El informe del equipo remoto cito
     `gemma4:12b-mlx_kb_rag = 0,5929` porque es lo que dice este fichero; el valor valido, tras la
     correccion, es **0,5846**.
  2. En una corrida **invierte el orden**. En `gemma4_31b_cloud_n120_REMOTO` declara mejor a
     `..._kb_rag` (0,6268) cuando el resumen corregido da mejor al `..._baseline` (0,6238), con
     kb_rag en 0,6185. Es lo contrario de lo que el informe sostiene sobre el modelo grande y el
     RAG, y quien abriera el fichero o el cuadro de mando veria esa inversion.

Que hace
--------
Por cada corrida que tenga los dos ficheros, compara `overall_f1` y `best_model` contra el mejor
del resumen, y dice cual deberia ser el contenido correcto. **No escribe nada:** estos ficheros
son artefactos de la corrida y los rehace quien la ejecuto.

Nota sobre el promediado
------------------------
El mejor del resumen se busca con `f is not None`, **nunca** con `if f`: un F1 de 0.0 es *falsy*
y una corrida entera en cero quedaria fuera de la comparacion, que es justo el caso que hay que
detectar.
"""
import os
import sys
import json
import glob
import argparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
TOL = 5e-5


def mejor_del_resumen(S):
    """(f1, nombre) del mejor grupo del resumen. Guarda `is not None`, no `if f`."""
    mejor = nombre = None
    for k, v in S.items():
        if not isinstance(v, dict):
            continue
        f = v.get('f1')
        if f is None:
            continue
        if mejor is None or f > mejor:
            mejor, nombre = f, k
    return mejor, nombre


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--results', default=RES)
    ap.add_argument('--estricto', action='store_true',
                    help='salir con 1 si hay alguna corrida desfasada')
    a = ap.parse_args()

    filas, ilegibles = [], []
    for d in sorted(glob.glob(os.path.join(a.results, '*'))):
        pa = os.path.join(d, 'acceptance_status.json')
        ps = os.path.join(d, 'benchmark_summary.json')
        if not (os.path.exists(pa) and os.path.exists(ps)):
            continue
        try:
            with open(pa, encoding='utf-8') as fh:
                A = json.load(fh)
            with open(ps, encoding='utf-8') as fh:
                S = json.load(fh)
        except (ValueError, OSError) as e:
            ilegibles.append((os.path.basename(d), str(e)[:60]))
            continue
        of = A.get('overall_f1')
        mejor, nombre = mejor_del_resumen(S)
        if of is None or mejor is None:
            ilegibles.append((os.path.basename(d), 'sin overall_f1 o sin F1 en el resumen'))
            continue
        filas.append((os.path.basename(d), of, mejor, A.get('best_model'), nombre))

    print('  %-38s %10s %10s  %s' % ('corrida', 'acceptance', 'resumen', 'estado'))
    desf = []
    for n, of, mejor, bm, nombre in filas:
        cifra_ok = abs(of - mejor) < TOL
        orden_ok = (bm == nombre)
        if cifra_ok and orden_ok:
            est = 'al dia'
        elif not orden_ok:
            est = '** DESFASADO, y con el ORDEN INVERTIDO **'
            desf.append((n, of, mejor, bm, nombre))
        else:
            est = '** desfasado **'
            desf.append((n, of, mejor, bm, nombre))
        print('  %-38s %10.6f %10.6f  %s' % (n[:38], of, mejor, est))

    for n, e in ilegibles:
        print('  %-38s %10s %10s  ILEGIBLE: %s' % (n[:38], '-', '-', e))

    print('\n  examinadas %d corridas con los dos ficheros · desfasadas %d · ilegibles %d'
          % (len(filas), len(desf), len(ilegibles)))
    if not filas:
        print('  VACIA: no se examino ninguna corrida, que no es lo mismo que estar todo al dia')
        return 2

    if desf:
        print('\n  lo que cada fichero desfasado deberia declarar:')
        for n, of, mejor, bm, nombre in desf:
            print('    %s' % n)
            print('        overall_f1: %.6f  ->  %.6f' % (of, mejor))
            if bm != nombre:
                print('        best_model: %s  ->  %s   (el orden esta invertido)' % (bm, nombre))
        print('\n  NO se corrigen aqui: son artefactos de la corrida y los rehace quien la ejecuto.')
        print('  Nada del analisis los lee —solo src/dashboard.py—, de modo que las metricas del')
        print('  estudio no estan afectadas. Ver FINDINGS §F89.')
    return 1 if (desf and a.estricto) else 0


if __name__ == '__main__':
    sys.exit(main())
