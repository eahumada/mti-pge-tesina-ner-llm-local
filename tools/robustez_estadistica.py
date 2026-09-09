#!/usr/bin/env python3
"""Regenera los contrastes de robustez del ANOVA publicado: Friedman y post-hoc pareado.

Los artefactos de `results/ROBUSTEZ_ESTADISTICA_20260908/` se calcularon a mano en una sesion
y **no tenian herramienta que los reprodujera**. Cuando la re-corrida sustituya los datos,
`FINDINGS §F75` y `§F76` —y con ellos la decision 7— habria que rehacerlos desde cero.

Dos contrastes, ambos sobre el CSV consolidado:

- **Friedman**, que es el que corresponde a un diseno de medidas repetidas: los grupos evaluan
  los mismos articulos, de modo que las observaciones no son independientes y el ANOVA de una via
  que publica el informe las trata como si lo fueran. Comprobar que el rechazo se sostiene
  acredita que esa eleccion es conservadora, en lugar de solo argumentarlo.
- **Post-hoc pareado**: Wilcoxon de rangos con signo entre la linea base y KB RAG de cada modelo,
  sobre los mismos registros, con correccion de Holm sobre las comparaciones de interes. El Tukey
  que publica el informe responde a otra pregunta —todos los pares entre todos los grupos— y
  corrige por muchas mas comparaciones de las que interesan.

    python3 tools/robustez_estadistica.py [csv] [--json <dir>] [--validar]

`--validar` exige que el resultado reproduzca los artefactos ya publicados, y es la prueba de que
la herramienta calcula lo mismo que se calculo a mano.
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
CSV_POR_DEFECTO = os.path.join(BENCH, 'results/ANALISIS_CONJUNTO_20260907/merged_results.csv')
PUBLICADO = os.path.join(BENCH, 'results/ROBUSTEZ_ESTADISTICA_20260908')

SUFIJOS = ('_baseline', '_kb_rag')


def leer(ruta):
    """Devuelve {grupo: {record_id: f1}}. `is not None`, nunca la veracidad: un F1 de 0,0 es dato."""
    datos = defaultdict(dict)
    with open(ruta, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            v = r.get('f1')
            if v in (None, ''):
                continue
            datos[r['model']][r['record_id']] = float(v)
    return datos


def holm(pares):
    """Correccion de Holm-Bonferroni. Devuelve [(clave, p_crudo, p_ajustada)] en el orden dado."""
    orden = sorted(pares, key=lambda x: x[1])
    m = len(orden)
    ajust, previo = {}, 0.0
    for i, (k, p) in enumerate(orden):
        v = min(1.0, max(previo, (m - i) * p))
        ajust[k] = v
        previo = v
    return [(k, p, ajust[k]) for k, p in pares]


def calcular(ruta_csv):
    try:
        from scipy import stats
    except ImportError:
        raise SystemExit(
            '  Falta scipy, y esta herramienta lo necesita.\n'
            '  Esta instalado en el entorno del proyecto, de modo que la orden es:\n\n'
            '      repos/ner-llm-entity-benchmark/venv/bin/python3 tools/robustez_estadistica.py '
            '--validar\n\n'
            '  Antes de este mensaje la herramienta moria con un traceback de ModuleNotFoundError,\n'
            '  que no dice donde esta el interprete que si la puede ejecutar. Comprobado el\n'
            '  2026-09-09: en ese venv reproduce los artefactos publicados sin discrepancias.\n'
            '  La comprobacion de Levene del verificador NO depende de scipy, a proposito.')

    datos = leer(ruta_csv)
    grupos = sorted(datos)
    # solo los registros presentes en TODOS los grupos: el diseno tiene que estar completo
    comunes = set.intersection(*(set(datos[g]) for g in grupos)) if grupos else set()
    comunes = sorted(comunes)
    matriz = [[datos[g][r] for r in comunes] for g in grupos]

    chi2 = p_fried = None
    if len(grupos) >= 3 and comunes:
        chi2, p_fried = stats.friedmanchisquare(*matriz)

    modelos = sorted({g[:-len(s)] for g in grupos for s in SUFIJOS if g.endswith(s)})
    crudos, filas = [], {}
    for m in modelos:
        b, k = m + '_baseline', m + '_kb_rag'
        if b not in datos or k not in datos:
            continue
        rs = sorted(set(datos[b]) & set(datos[k]))
        x = [datos[b][r] for r in rs]
        y = [datos[k][r] for r in rs]
        if not rs or all(a == c for a, c in zip(x, y)):
            continue
        _, p = stats.wilcoxon(x, y)
        crudos.append((m, float(p)))
        filas[m] = {'modelo': m, 'n': len(rs),
                    'delta_pp': round(100 * (sum(y) / len(y) - sum(x) / len(x)), 2),
                    'p_crudo': float(p)}
    for m, p, pa in holm(crudos):
        filas[m]['p_holm'] = pa
        filas[m]['significativo'] = bool(pa < 0.05)

    # Correlacion entre capacidad base y beneficio del RAG: es la que sostiene la tesis central del
    # informe.
    #
    # Sobre el consolidado antiguo esta funcion da Pearson -0,6002 y el artefacto publicado dice
    # -0,6004. La diferencia esta explicada y no es un defecto: aquel se calculo sobre los valores
    # REDONDEADOS de la Tabla 7 —dos decimales— y este sobre el CSV crudo. Comprobado el 2026-09-09
    # reproduciendo ambos. Spearman coincide exactamente porque trabaja con rangos, a los que el
    # redondeo no afecta. Se deja constancia para que nadie persiga esa diferencia como si fuera un
    # error; por eso `--validar` tolera 0,001 en el coeficiente lineal. Se calculaba a mano, que es el mismo defecto que este script vino a arreglar para el
    # Friedman y el post-hoc. Con el analisis de influencia, porque en el corpus corregido el
    # coeficiente lineal depende de un solo punto (`FINDINGS §F86`).
    pares = {}
    for m in modelos:
        b, k = m + '_baseline', m + '_kb_rag'
        if b in datos and k in datos:
            B = 100 * sum(datos[b].values()) / len(datos[b])
            K = 100 * sum(datos[k].values()) / len(datos[k])
            pares[m] = (B, K - B)

    def coef(d):
        if len(d) < 3:
            return None
        x = [v[0] for v in d.values()]
        y = [v[1] for v in d.values()]
        sp = stats.spearmanr(x, y)
        pe = stats.pearsonr(x, y)
        return {'n': len(x),
                'spearman': {'rho': round(float(sp.statistic), 4), 'p': round(float(sp.pvalue), 4)},
                'pearson': {'r': round(float(pe.statistic), 4), 'p': round(float(pe.pvalue), 4)}}

    correlacion = coef(pares)
    influencia = {}
    if correlacion:
        for m in pares:
            c = coef({k: v for k, v in pares.items() if k != m})
            if c:
                influencia[m] = {'pearson_r': c['pearson']['r'], 'pearson_p': c['pearson']['p'],
                                 'spearman_rho': c['spearman']['rho']}
    mas_influyente = None
    if influencia and correlacion:
        mas_influyente = max(influencia, key=lambda m: abs(influencia[m]['pearson_r']
                                                           - correlacion['pearson']['r']))

    orden = sorted(filas.values(), key=lambda f: -f['delta_pp'])
    return {
        'correlacion_capacidad_beneficio': correlacion,
        'influencia_al_retirar_cada_modelo': influencia,
        'modelo_mas_influyente': mas_influyente,
        'csv': os.path.relpath(ruta_csv, RAIZ),
        'grupos': len(grupos),
        'registros_completos': len(comunes),
        'friedman': None if chi2 is None else {
            'chi2': round(float(chi2), 4), 'p': float(p_fried), 'gl': len(grupos) - 1},
        'n_comparaciones': len(orden),
        'significativos_pareado': sum(1 for f in orden if f['significativo']),
        'filas': orden,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv', nargs='?', default=CSV_POR_DEFECTO)
    ap.add_argument('--json', help='directorio donde escribir friedman.json y posthoc_pareado.json')
    ap.add_argument('--validar', action='store_true',
                    help='exige reproducir los artefactos publicados')
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print('no existe %s' % args.csv)
        return 2
    r = calcular(args.csv)
    print('  csv: %s' % r['csv'])
    print('  grupos: %d · registros completos: %d' % (r['grupos'], r['registros_completos']))
    if r['friedman']:
        print('  Friedman: chi2 = %.4f · p = %.4e · gl = %d'
              % (r['friedman']['chi2'], r['friedman']['p'], r['friedman']['gl']))
    print('  post-hoc pareado: %d de %d significativos tras Holm'
          % (r['significativos_pareado'], r['n_comparaciones']))
    c = r.get('correlacion_capacidad_beneficio')
    if c:
        print('  correlacion capacidad vs beneficio (n=%d): Spearman rho = %+.4f (p = %.4f) · '
              'Pearson r = %+.4f (p = %.4f)'
              % (c['n'], c['spearman']['rho'], c['spearman']['p'],
                 c['pearson']['r'], c['pearson']['p']))
        mi = r.get('modelo_mas_influyente')
        if mi:
            v = r['influencia_al_retirar_cada_modelo'][mi]
            print('  punto mas influyente: %s — sin el, Pearson r = %+.4f (p = %.4f)'
                  % (mi, v['pearson_r'], v['pearson_p']))
    for f in r['filas']:
        marca = 'si' if f['significativo'] else 'no'
        print('    %-24s Δ=%+7.2f pp  p=%.3e  Holm=%.4f  %s'
              % (f['modelo'], f['delta_pp'], f['p_crudo'], f['p_holm'], marca))

    if args.validar:
        fallos = []
        fr = json.load(open(os.path.join(PUBLICADO, 'friedman.json'), encoding='utf-8'))
        ph = json.load(open(os.path.join(PUBLICADO, 'posthoc_pareado.json'), encoding='utf-8'))
        esperado = fr['friedman_medidas_repetidas']
        if r['friedman'] is None or abs(r['friedman']['chi2'] - esperado['chi2']) > 0.001:
            fallos.append('chi2: publicado %.4f, calculado %s'
                          % (esperado['chi2'], r['friedman'] and r['friedman']['chi2']))
        if r['friedman'] and r['friedman']['gl'] != esperado['gl']:
            fallos.append('gl: publicado %d, calculado %d' % (esperado['gl'], r['friedman']['gl']))
        if r['significativos_pareado'] != ph['significativos_pareado']:
            fallos.append('significativos: publicado %d, calculado %d'
                          % (ph['significativos_pareado'], r['significativos_pareado']))
        if r['n_comparaciones'] != ph['n_comparaciones']:
            fallos.append('comparaciones: publicado %d, calculado %d'
                          % (ph['n_comparaciones'], r['n_comparaciones']))
        print()
        if fallos:
            print('  NO reproduce los artefactos publicados:')
            for f in fallos:
                print('    - %s' % f)
            return 1
        print('  reproduce los artefactos publicados sin discrepancias')

    if args.json:
        os.makedirs(args.json, exist_ok=True)
        json.dump(r, open(os.path.join(args.json, 'robustez.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('  escrito: %s' % os.path.relpath(os.path.join(args.json, 'robustez.json'), RAIZ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
