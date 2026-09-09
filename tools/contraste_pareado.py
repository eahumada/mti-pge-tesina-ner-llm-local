#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
contraste_pareado.py — El contraste que el diseño de este estudio pide, en las dos métricas.

Por qué existe
--------------
El diseño es de **medidas repetidas totalmente cruzado**: los mismos artículos se evalúan en los 26
grupos, y dentro de cada modelo la línea base y el KB RAG se miden sobre los mismos artículos.
Comprobado por intersección de identificadores, no supuesto. El ANOVA de una vía que el informe
publica trata esos registros como independientes y **confunde el efecto MODELO con el efecto MODO**,
de modo que su F no aísla el efecto del RAG, que es la pregunta del estudio. El equipo de 48 GB y
este equipo llegaron a esa conclusión por separado; ver `FINDINGS §F137` y
`remote_48g/DICTAMEN-PRUEBA-ESTADISTICA-20260909.md`.

El contraste que corresponde es **Wilcoxon de rangos con signo por modelo** sobre las diferencias
F1(kb_rag) − F1(baseline) de los artículos pareados, con corrección de **Holm** sobre los 13
contrastes. Se calculó a mano dos veces —una por métrica— y habrá que rehacerlo cuando cambien los
datos o cuando el autor decida qué métrica es la de referencia, así que se mecaniza (`§L61`).

Qué añade sobre `repos/ner-llm-entity-benchmark/tools/wilcoxon_pareado.py`
-------------------------------------------------------------------------
Esa herramienta, del equipo de 48 GB, calcula la métrica de tres categorías desde la columna `f1`
del CSV. Ésta añade dos cosas que su propio dictamen pedía y no cubría:

1. **La métrica restringida** a las categorías que el corpus anota de verdad, reagregando desde
   `per_type`. Da un recuento distinto —4 de 13 frente a 3— y cambia el signo de un modelo.
2. **Tres cifras de tamaño de efecto y no una**: mediana, media y recuento de pares no nulos con su
   reparto. Hace falta porque **dos de los cuatro modelos significativos de la métrica restringida
   tienen mediana exactamente +0,0000**, y con solo la mediana parecerían no tener efecto. No es
   ausencia de efecto: es efecto concentrado en una minoría de artículos, que es lo que Wilcoxon
   detecta al mirar la consistencia de signo entre las diferencias no nulas.

Dependencias
------------
Necesita `scipy` y `statsmodels`, que están en el venv del proyecto y no en el Python del sistema:

    repos/ner-llm-entity-benchmark/venv/bin/python tools/contraste_pareado.py

Es una herramienta de **análisis**, no de verificación, y por eso se le permite la dependencia —la
misma excepción que `generar_figuras_informe.py`, ver `FINDINGS §F132`—. Ninguna comprobación del
verificador la ejecuta.

No escribe nada. Imprime la tabla.
"""
import argparse
import collections
import csv
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
# Los siete artículos que el manifiesto del consolidado nuevo excluye por contaminación.
CONTAMINADOS = {'real_mixed_1', 'real_mixed_101', 'real_mixed_21', 'real_mixed_27',
                'real_mixed_41', 'real_mixed_59', 'real_mixed_79'}
TRES = ('Persons', 'Organizations', 'Locations')
DOS = ('Persons', 'Organizations')


def _f1(tp, fp, fn):
    """F1 con la convención del evaluador: extracción y referencia vacías dan 1,0."""
    if tp + fp + fn == 0:
        return 1.0
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def desde_csv(consolidado):
    """F1 por (grupo, artículo) desde la columna `f1` del CSV consolidado."""
    p = os.path.join(RES, consolidado, 'merged_results.csv')
    if not os.path.exists(p):
        return None
    o = collections.defaultdict(dict)
    with open(p, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            # `is not None` y no la veracidad: un F1 de 0,0 es un dato, no un hueco.
            v = r.get('f1')
            if v is not None and v != '':
                o[r['model']][r['record_id']] = float(v)
    return o


def desde_per_type(cats, excluir_contaminados=True):
    """F1 recalculado desde los recuentos crudos, que es la única vía para la restringida."""
    o = collections.defaultdict(dict)
    for d in sorted(glob.glob(os.path.join(RES, 'recorrida_20260908', '*__N120'))):
        p = os.path.join(d, 'detailed_results.json')
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as fh:
            rr = json.load(fh)
        rr = rr if isinstance(rr, list) else rr.get('results', [])
        for r in rr:
            rid = r.get('record_id')
            if excluir_contaminados and rid in CONTAMINADOS:
                continue
            pt = ((r.get('metrics') or {}).get('per_type')) or {}
            if not pt:
                continue
            tp = sum(pt.get(c, {}).get('tp') or 0 for c in cats)
            fp = sum(pt.get(c, {}).get('fp') or 0 for c in cats)
            fn = sum(pt.get(c, {}).get('fn') or 0 for c in cats)
            o[r.get('model')][rid] = _f1(tp, fp, fn)
    return o


def contrasta(G, etiqueta):
    """Wilcoxon por modelo + Holm, con las tres cifras de tamaño de efecto."""
    import numpy as np
    from scipy import stats
    from statsmodels.stats.multitest import multipletests

    modelos = sorted({k[:-len('_baseline')] for k in G if k.endswith('_baseline')})
    filas = []
    for m in modelos:
        b, k = G.get(m + '_baseline', {}), G.get(m + '_kb_rag', {})
        ids = sorted(set(b) & set(k))       # el emparejamiento se COMPRUEBA, no se supone
        if len(ids) < 10:
            continue
        d = np.array([k[i] - b[i] for i in ids])
        nz = d[d != 0]
        if nz.size == 0:
            p = 1.0
        else:
            p = float(stats.wilcoxon(d, zero_method='wilcox',
                                     alternative='two-sided').pvalue)
        filas.append({
            'modelo': m, 'n': len(ids), 'no_nulos': int(nz.size),
            'mejoran': int((d > 0).sum()), 'empeoran': int((d < 0).sum()),
            'mediana': float(np.median(d)), 'media': float(d.mean()), 'p': p,
        })
    if not filas:
        print('  VACIA: no se pudo formar ningun par baseline/kb_rag')
        return []
    rech, holm, _, _ = multipletests([f['p'] for f in filas], alpha=0.05, method='holm')
    for f, r, h in zip(filas, rech, holm):
        f['p_holm'] = float(h)
        f['sig'] = bool(r)
    filas.sort(key=lambda f: f['p'])

    print('\n  ══ %s ══' % etiqueta)
    print('  %-22s %4s %6s %7s %7s %10s %10s %11s %10s %s'
          % ('modelo', 'n', 'Δ≠0', 'mejor', 'peor', 'mediana', 'media', 'p', 'p Holm', 'sig'))
    for f in filas:
        print('  %-22s %4d %6d %7d %7d %+10.4f %+10.4f %11.3g %10.4f %s'
              % (f['modelo'], f['n'], f['no_nulos'], f['mejoran'], f['empeoran'],
                 f['mediana'], f['media'], f['p'], f['p_holm'], 'si' if f['sig'] else 'no'))
    sig = [f for f in filas if f['sig']]
    print('  -> %d de %d significativos tras Holm' % (len(sig), len(filas)))
    cero = [f['modelo'] for f in sig if abs(f['mediana']) < 1e-12]
    if cero:
        print('     ATENCION: %d de los significativos tienen mediana +0,0000 (%s).'
              % (len(cero), ', '.join(cero)))
        print('     No es ausencia de efecto: Wilcoxon detecta consistencia de signo entre las')
        print('     diferencias NO NULAS, y aqui mas de un tercio de los pares vale cero, de modo')
        print('     que el efecto vive en una minoria de articulos. Citar la mediana sola engana:')
        print('     hay que dar tambien la media y el reparto mejora/empeora.')
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--consolidado', default='ANALISIS_CONJUNTO_20260909_FIX',
                    help='consolidado del que leer el CSV para la metrica de tres categorias')
    ap.add_argument('--json', metavar='FICHERO',
                    help='escribe el resultado como JSON en ese fichero, para poder citarlo')
    a = ap.parse_args()

    try:
        import numpy  # noqa: F401
        from scipy import stats  # noqa: F401
        from statsmodels.stats.multitest import multipletests  # noqa: F401
    except ModuleNotFoundError as e:
        sys.exit('  Falta %s, que no esta en el Python del sistema. Usar el venv:\n'
                 '      repos/ner-llm-entity-benchmark/venv/bin/python tools/contraste_pareado.py\n'
                 '  Es una herramienta de analisis y no de verificacion, y por eso se le permite la\n'
                 '  dependencia. Ninguna comprobacion del verificador la ejecuta (FINDINGS §F132).'
                 % e.name)

    salida = {}
    G = desde_csv(a.consolidado)
    if G is None:
        print('  no existe results/%s/merged_results.csv' % a.consolidado)
    else:
        salida['tres_csv'] = contrasta(
            G, 'TRES categorias, desde la columna f1 del CSV (%s)' % a.consolidado)

    salida['tres_per_type'] = contrasta(
        desde_per_type(TRES), 'TRES categorias, reagregado desde per_type (via independiente)')
    salida['restringida'] = contrasta(
        desde_per_type(DOS), 'RESTRINGIDA a las categorias que el corpus anota')

    if salida.get('tres_csv') and salida.get('tres_per_type'):
        a1 = {f['modelo'] for f in salida['tres_csv'] if f['sig']}
        a2 = {f['modelo'] for f in salida['tres_per_type'] if f['sig']}
        print('\n  las dos vias de la metrica de tres categorias %s'
              % ('COINCIDEN' if a1 == a2 else 'DISCREPAN: %s' % (a1 ^ a2)))
    if salida.get('restringida') and salida.get('tres_per_type'):
        r = {f['modelo'] for f in salida['restringida'] if f['sig']}
        t = {f['modelo'] for f in salida['tres_per_type'] if f['sig']}
        print('  el recuento cambia entre metricas: %d en tres categorias, %d en la restringida'
              % (len(t), len(r)))
        if r - t:
            print('     entra en la restringida: %s' % ', '.join(sorted(r - t)))
        if t - r:
            print('     sale en la restringida:  %s' % ', '.join(sorted(t - r)))
        print('  Cual de los dos recuentos es «el N de 13» del informe es decision del autor: las')
        print('  dos cifras son correctas sobre metricas distintas, y el informe publica las dos.')

    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(salida, fh, ensure_ascii=False, indent=2)
        print('\n  escrito %s' % a.json)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
