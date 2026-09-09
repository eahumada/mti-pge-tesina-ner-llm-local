#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
derivados_desfasados.py — Artefactos derivados que la correccion de puntuacion dejo atras.

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
Tres comprobaciones, en orden de gravedad creciente y con la tercera como **control positivo**:

  1. `acceptance_status.json` de cada corrida, contra el mejor F1 de su resumen.
  2. `statistical_report.md` de cada corrida, grupo por grupo, contra su resumen. Es el mas
     consecuente de los dos, porque no trae solo cifras sino intervalos de confianza y veredictos
     calculados sobre ellas.
  3. **El `statistical_report.md` del CONSOLIDADO contra `merged_results.csv`.** Este es el que
     alimenta la Tabla 7 del informe, via `tools/generar_tabla7.py`, y por tanto el unico cuyo
     desfase alcanzaria a la tesina. Sin esta tercera comprobacion la herramienta no distinguiria
     «el consolidado esta bien» de «el consolidado no se ha mirado», que es §L57.

**No escribe nada:** son artefactos de la corrida y los rehace quien la ejecuto.

Una trampa que costo una pasada
-------------------------------
El informe consolidado tiene **varias** tablas, y la primera es la de cobertura
(`| Modelo | Filas | record_id unicos | ... |`). Un patron que busque
`| grupo | numero | numero |` caza esa y no la de F1, que esta mas abajo. La primera version daba
26 divergencias de 26 con un «F1 = 120,0000» en todas: **el valor imposible repetido es lo que
delato el error**, porque una divergencia real no da el mismo numero absurdo veintiseis veces. De
ahi que la busqueda se ancle a la cabecera `| Model | Sample Size (N) | Mean F1-Score |`.

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

import csv
import re
import collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
CONS = os.path.join(RES, 'ANALISIS_CONJUNTO_20260907')
TOL = 5e-5
# La tabla de F1 del informe consolidado. Anclar aqui y no en la primera tabla del documento.
CAB_F1 = '| Model | Sample Size (N) | Mean F1-Score |'


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


def f1_del_informe(texto, grupo, seccion=None):
    """F1 y N que el informe declara para un grupo, buscando solo en `seccion` si se da."""
    donde = seccion if seccion is not None else texto
    m = re.search(r'^\|\s*%s\s*\|\s*(\d+)\s*\|\s*([0-9.]+)' % re.escape(grupo), donde, re.M)
    return (int(m.group(1)), float(m.group(2))) if m else (None, None)


def seccion_f1(texto):
    """El trozo del informe que contiene la tabla de F1, desde su cabecera."""
    i = texto.find(CAB_F1)
    if i < 0:
        return None
    j = texto.find('\n\n', i)
    return texto[i:j if j > 0 else len(texto)]


def informes_por_corrida(res):
    """statistical_report.md de cada corrida contra su benchmark_summary.json."""
    filas = []
    for d in sorted(glob.glob(os.path.join(res, '*'))):
        ps = os.path.join(d, 'benchmark_summary.json')
        pr = os.path.join(d, 'statistical_report.md')
        if not (os.path.exists(ps) and os.path.exists(pr)):
            continue
        try:
            with open(ps, encoding='utf-8') as fh:
                S = json.load(fh)
            with open(pr, encoding='utf-8') as fh:
                txt = fh.read()
        except (ValueError, OSError):
            continue
        ok, dif = 0, []
        for k, v in S.items():
            if not isinstance(v, dict):
                continue
            f = v.get('f1')
            if f is None:
                continue
            n_rep, f_rep = f1_del_informe(txt, k)
            if f_rep is None:
                continue
            if abs(f_rep - round(f, 4)) < 1e-4:
                ok += 1
            else:
                dif.append((k, f_rep, f))
        if ok or dif:
            filas.append((os.path.basename(d), ok, dif))
    return filas


def consolidado(dir_cons):
    """Control positivo: el informe del consolidado contra su merged_results.csv."""
    pr = os.path.join(dir_cons, 'statistical_report.md')
    pc = os.path.join(dir_cons, 'merged_results.csv')
    if not (os.path.exists(pr) and os.path.exists(pc)):
        return None, 'faltan statistical_report.md o merged_results.csv en %s' % dir_cons
    by = collections.defaultdict(list)
    with open(pc, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            v = r.get('f1')
            if v is not None and v != '':
                by[r['model']].append(float(v))
    with open(pr, encoding='utf-8') as fh:
        sec = seccion_f1(fh.read())
    if sec is None:
        return None, 'no se encuentra la cabecera de la tabla de F1 en el informe del consolidado'
    ok, dif = 0, []
    for k, v in sorted(by.items()):
        mu = sum(v) / len(v)
        n_rep, f_rep = f1_del_informe('', k, sec)
        if f_rep is None:
            dif.append((k, len(v), mu, None, None))
            continue
        if abs(f_rep - round(mu, 4)) < 1e-4 and n_rep == len(v):
            ok += 1
        else:
            dif.append((k, len(v), mu, n_rep, f_rep))
    return (ok, dif), None


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

    # --- 2) los statistical_report.md por corrida ---
    print('\n  === statistical_report.md por corrida, grupo por grupo ===')
    porc = informes_por_corrida(a.results)
    tot_g = tot_d = 0
    for nom, ok, dif in porc:
        tot_g += ok + len(dif)
        tot_d += len(dif)
        marca = '  ** %d desfasados **' % len(dif) if dif else ''
        print('  %-38s grupos %3d · al dia %3d%s' % (nom[:38], ok + len(dif), ok, marca))
        for k, fr, f in dif:
            print('        %-34s informe %.4f · resumen %.4f' % (k, fr, f))
    print('  examinados %d grupos en %d corridas · desfasados %d' % (tot_g, len(porc), tot_d))
    if tot_g == 0:
        print('  VACIA: no se examino ningun grupo')

    # --- 3) control positivo: el consolidado, que es el unico que alcanza a la tesina ---
    print('\n  === CONTROL: el informe del consolidado, que alimenta la Tabla 7 ===')
    r, err = consolidado(os.path.join(a.results, 'ANALISIS_CONJUNTO_20260907'))
    cons_mal = False
    if err:
        print('  NO COMPROBADO: %s' % err)
        cons_mal = True
    else:
        ok, dif = r
        print('  grupos %d · coinciden con merged_results.csv %d · difieren %d' % (ok + len(dif), ok, len(dif)))
        for k, n, mu, nr, fr in dif:
            print('        %-34s csv n=%d F1=%.4f · informe %s'
                  % (k, n, mu, 'AUSENTE' if fr is None else 'n=%s F1=%.4f' % (nr, fr)))
        if dif:
            cons_mal = True
        elif ok == 0:
            print('  VACIA: cero grupos examinados, que no es lo mismo que estar al dia')
            cons_mal = True
        else:
            print('  el consolidado esta AL DIA: el desfase de los informes por corrida')
            print('  no alcanza a la tesina. Nada aguas abajo los lee.')

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
    if cons_mal:
        return 1
    return 1 if ((desf or tot_d) and a.estricto) else 0


if __name__ == '__main__':
    sys.exit(main())
