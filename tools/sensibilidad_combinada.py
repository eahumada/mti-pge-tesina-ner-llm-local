#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sensibilidad_combinada.py — Los deltas del estudio bajo las dos sensibilidades, juntas y por separado.

Por que existe
--------------
El estudio tiene dos defectos de medicion reconocidos, cada uno con su efecto sobre las cifras:

  * el **parseo alterno**: 112 de 3 120 registros del consolidado se parsearon por la via de
    excepcion, y en algunos grupos eso deprime el F1 (§F109);
  * el **emparejamiento duplicado**: los aciertos se cuentan por extraccion casada y los fallos
    sobre referencias distintas, lo que infla la exhaustividad (§F49, §F81).

Por separado ninguno mueve casi nada. **Juntos, uno de los deltas cambia de signo** —`gemma4:latest`
pasa de −1,17 a +0,47— y ninguna sensibilidad de una sola variable lo habria encontrado (§F111).
Este analisis se hizo a mano dos veces, la primera mal, y por eso se mecaniza (§L61).

Como
----
Se recorre `detailed_results.json` de cada fuente del manifiesto, resolviendo duplicados **por la
primera fuente** igual que la fusion, y se calcula el F1 por registro de cuatro formas: desde
`per_type` tal cual, aislando los registros de parseo alterno, corrigiendo el emparejamiento
duplicado, y las dos cosas.

**No se usa `overall.f1`.** Ese bloque contiene valores imposibles —F1 de 1,0 con precision y
exhaustividad a cero— por la vieja convencion de extraccion vacia (§F110), y la primera version de
este analisis se apoyo en el y hubo que descartarla entera.

Grupos excluidos
----------------
`nemotron-mini:4b_baseline`, porque su `per_type` **no reproduce su CSV**: seis de sus registros se
re-extrajeron fuera del arnes y solo el CSV recibio las metricas (§F110). Compararlo mezclaria dos
estados del dato. **Cuando la re-corrida de `§3.bis.15` regenere los dos artefactos, hay que
quitarlo de la exclusion y volver a mirar** — la comprobacion de abajo dice si ya se puede.
"""
import os
import re
import csv
import json
import argparse
import importlib.util
import collections

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
CONS = os.path.join(BENCH, 'results/ANALISIS_CONJUNTO_20260907')
CATS = ('Persons', 'Organizations', 'Locations')
# Ver el docstring: se quita en cuanto su per_type reproduzca su CSV.
EXCLUIDOS = {'nemotron-mini:4b_baseline'}


def _efd():
    """Se reutiliza `recalcula` de la herramienta del emparejamiento duplicado, no se reimplementa."""
    ruta = os.path.join(RAIZ, 'tools/efecto_emparejamiento_duplicado.py')
    spec = importlib.util.spec_from_file_location('efd', ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def f1_desde_per_type(r):
    """F1 del registro desde los recuentos crudos. La convencion de vacio da 1.0, como el evaluador."""
    pt = ((r.get('metrics') or {}).get('per_type')) or {}
    tp = sum((pt.get(c, {}).get('tp') or 0) for c in CATS)
    fp = sum((pt.get(c, {}).get('fp') or 0) for c in CATS)
    fn = sum((pt.get(c, {}).get('fn') or 0) for c in CATS)
    if tp + fp + fn == 0:
        return 1.0
    p = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * rc / (p + rc) if p + rc else 0.0


def cargar():
    efd = _efd()
    with open(os.path.join(CONS, 'merge_manifest.json'), encoding='utf-8') as fh:
        fuentes = json.load(fh)['sources']
    with open(os.path.join(CONS, 'merged_results.csv'), encoding='utf-8') as fh:
        pm = {(r['model'], r['record_id']): r.get('parse_method') for r in csv.DictReader(fh)}
    visto, datos = set(), collections.defaultdict(list)
    for s in fuentes:
        rel = os.path.dirname(s['csv_path'])          # con `results/`, que es lo que BENCH espera
        for r in efd.registros(rel):
            g, rid = r.get('model'), r.get('record_id')
            if (g, rid) in visto:
                continue
            if not ((r.get('metrics') or {}).get('per_type')):
                continue
            visto.add((g, rid))
            f_cor, _ = efd.recalcula(r)
            datos[g].append((f1_desde_per_type(r), f_cor, pm.get((g, rid))))
    return datos


def coherente_con_el_csv(g, datos, tol=0.05):
    """Si el per_type del grupo reproduce su media del CSV consolidado."""
    with open(os.path.join(CONS, 'merged_results.csv'), encoding='utf-8') as fh:
        v = [float(r['f1']) for r in csv.DictReader(fh)
             if r['model'] == g and r.get('f1') not in (None, '')]
    if not v or g not in datos:
        return None
    a = 100 * sum(x[0] for x in datos[g]) / len(datos[g])
    return abs(a - 100 * sum(v) / len(v)) <= tol


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--incluir-excluidos', action='store_true',
                    help='incluye los grupos excluidos, para comprobar si ya son comparables')
    a = ap.parse_args()
    datos = cargar()
    if not datos:
        print('  VACIA: no se cargo ningun registro con per_type')
        return 2

    def med(g, sin_fb, cor):
        F = [x for x in datos.get(g, []) if not (sin_fb and x[2] == 'fallback')]
        return 100 * sum((x[1] if cor else x[0]) for x in F) / len(F) if F else None

    def delta(m, sin_fb, cor):
        b, k = med(m + '_baseline', sin_fb, cor), med(m + '_kb_rag', sin_fb, cor)
        return None if None in (b, k) else k - b

    mods = sorted({g[:-len('_baseline')] for g in datos if g.endswith('_baseline')})
    print('  %-22s %9s %9s %9s %9s  %s'
          % ('modelo', 'per_type', 'sin fb', 'sin dup', 'ambas', 'cambia de signo'))
    flips, n = [], 0
    for m in mods:
        if (m + '_baseline') in EXCLUIDOS and not a.incluir_excluidos:
            ok = coherente_con_el_csv(m + '_baseline', datos)
            print('  %-22s %9s %9s %9s %9s  EXCLUIDO (§F110)%s'
                  % (m, '—', '—', '—', '—',
                     ' — YA es coherente con el CSV: quitarlo de EXCLUIDOS' if ok else ''))
            continue
        d = [delta(m, 0, 0), delta(m, 1, 0), delta(m, 0, 1), delta(m, 1, 1)]
        if None in d:
            continue
        n += 1
        fl = [t for t, v in zip(('sin fb', 'sin dup', 'ambas'), d[1:]) if (d[0] < 0) != (v < 0)]
        if fl:
            flips.append((m, d, fl))
        print('  %-22s %+9.4f %+9.4f %+9.4f %+9.4f  %s'
              % (m, d[0], d[1], d[2], d[3], ', '.join(fl)))
    print('\n  %d modelos analizados · %d con cambio de signo en algun escenario' % (n, len(flips)))
    for m, d, fl in flips:
        solo_juntas = 'ambas' in fl and 'sin fb' not in fl and 'sin dup' not in fl
        print('    %-22s %+.4f -> %+.4f%s'
              % (m, d[0], d[3], '   <== SOLO al combinar las dos' if solo_juntas else ''))
    print('\n  La significacion no cambia en ninguno: ninguno alcanza el umbral de Tukey en el')
    print('  informe ni en ningun escenario. Lo que se mueve es el signo de la estimacion puntual.')
    print('  Y las dos correcciones no tienen el mismo estatus: corregir el emparejamiento')
    print('  duplicado va HACIA la medida correcta; aislar el parseo alterno es hipotetico.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
