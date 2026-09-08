#!/usr/bin/env python3
"""Genera las filas de la Tabla 7 del informe desde un consolidado.

La Tabla 7 son trece filas con cinco columnas cada una, y la de significancia sale del post-hoc de
Tukey: escribirlas a mano al cerrar la re-corrida es trabajo mecanico y propenso a erratas. Este
script las produce listas para pegar.

Validacion: ejecutado sobre el consolidado vigente debe reproducir **exactamente** la Tabla 7 que hoy
publica el informe. Si no lo hace, el script esta mal y no debe usarse para la tabla nueva.

Uso:
    python3 tools/generar_tabla7.py [dir_consolidado]
    python3 tools/generar_tabla7.py --validar     # compara con la tabla del informe
"""
import collections
import csv
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POR_DEFECTO = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_20260907')
MD = os.path.join(RAIZ, 'doc/organized/Hito_5_Tarea4_Informe_Final/'
                        '2026-07-04_Borrador-Informe-Final-Tesina.md')


def medias(csv_path):
    """F1 medio por grupo. `is not None`, no la veracidad: un F1 de 0.0 es un dato."""
    g = collections.defaultdict(list)
    with open(csv_path, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r.get('f1') not in (None, ''):
                g[r['model']].append(float(r['f1']))
    return {k: 100 * sum(v) / len(v) for k, v in g.items()}


def significancia(report_path):
    """Del post-hoc de Tukey: por modelo, (significativo, p) del contraste baseline vs kb_rag."""
    out = {}
    if not os.path.exists(report_path):
        return out
    with open(report_path, encoding='utf-8') as fh:
        for l in fh:
            m = re.match(r'\|\s*(\S+)_baseline vs (\S+)_kb_rag\s*\|\s*[-\d.]+\s*\|\s*([\d.eE+-]+)\s*\|'
                         r'\s*(?:❌|✅)?\s*(\w+)', l)
            if m and m.group(1) == m.group(2):
                out[m.group(1)] = (m.group(4).lower() in ('yes', 'si', 'sí'), float(m.group(3)))
    return out


def filas(dir_cons):
    med = medias(os.path.join(dir_cons, 'merged_results.csv'))
    sig = significancia(os.path.join(dir_cons, 'statistical_report.md'))
    modelos = sorted({k.rsplit('_', 1)[0].replace('_kb', '') for k in med
                      if k.endswith('_baseline')},
                     key=lambda m: -med.get(m + '_baseline', 0))
    out = []
    for m in modelos:
        b, r = med.get(m + '_baseline'), med.get(m + '_kb_rag')
        if b is None or r is None:
            continue
        d = r - b
        s, p = sig.get(m, (False, None))
        col = ('**sí** (p<0.001)' if s and p is not None and p < 0.001 else
               '**sí** (p=%.3f)' % p if s and p is not None else 'no')
        out.append((m, b, r, d, col))
    return out


def formatea(f):
    L = ['| Modelo | F1 baseline | F1 KB RAG | Δ RAG | Δ significativo |',
         '|:---|:---:|:---:|:---:|:---:|']
    for m, b, r, d, col in f:
        L.append('| %s | %.2f%% | %.2f%% | %s%.2f pp | %s |'
                 % (m, b, r, '−' if d < 0 else '+', abs(d), col))
    return '\n'.join(L)


def validar(f):
    """Compara las filas generadas con la Tabla 7 que publica el informe."""
    s = open(MD, encoding='utf-8').read()
    i = s.find('_Tabla 7.')
    pub = {}
    for l in s[i:i + 3000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|', l)
        if m and not m.group(1).startswith('Modelo'):
            pub[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
    fallos = []
    for m, b, r, _, _ in f:
        p = pub.get(m)
        if p is None:
            fallos.append('%s no esta en la Tabla 7 del informe' % m)
        elif abs(p[0] - b) > 0.011 or abs(p[1] - r) > 0.011:
            fallos.append('%s: informe %.2f/%.2f vs generado %.2f/%.2f' % (m, p[0], p[1], b, r))
    for m in pub:
        if m not in {x[0] for x in f}:
            fallos.append('%s esta en el informe y no se genera' % m)
    return fallos


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dir_cons = args[0] if args else POR_DEFECTO
    f = filas(dir_cons)
    if '--validar' in sys.argv:
        fallos = validar(f)
        print('  filas generadas: %d · discrepancias con el informe: %d' % (len(f), len(fallos)))
        for x in fallos:
            print('   - %s' % x)
        return 1 if fallos else 0
    print(formatea(f))
    return 0


if __name__ == '__main__':
    sys.exit(main())
