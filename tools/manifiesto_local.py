#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Acredita que un consolidado se reproduce desde fuentes que existen EN ESTA maquina.

Por que existe. El manifiesto de ANALISIS_CONJUNTO_20260909_FIX declara sus trece fuentes con rutas
absolutas de otra maquina —`/Users/eahumada1/Projects/...`—, de modo que **ninguna resuelve aqui**.
Eso deja la decision 1 del autor, adoptar o no ese consolidado, sin forma de comprobarse: un
manifiesto cuyas rutas no abren no acredita nada, aunque los datos esten.

Y son dos cosas distintas que conviene no confundir: que el manifiesto **no sea portable** es un
defecto de forma; que los datos **no esten** seria de fondo. Esta herramienta separa las dos.

Que hace, y no toca ningun fichero:

 1. Resuelve cada ruta declarada contra el repositorio local, recortando el prefijo de la otra
    maquina por la cola conocida `repos/ner-llm-entity-benchmark/`. Y toma de cada fuente **solo los
    grupos que el manifiesto le atribuye**: la primera version de esta herramienta tomaba el fichero
    entero y por eso declaro NO reproducible el consolidado publicado, que si lo es. Un fichero de
    corrida puede traer grupos que la fusion descarta a proposito.
 2. Comprueba que el fichero existe y que trae **las filas que el manifiesto declara**.
 3. Reagrega las trece fuentes aplicando la exclusion de contaminados que el manifiesto declara, y
    comprueba que el resultado **reproduce** `merged_results.csv`: numero de filas, conjunto de
    grupos, y la F1 media de cada grupo al cuarto decimal.
 4. Comprueba la tabla `integrity` del propio manifiesto contra los datos.

Devuelve 0 si el consolidado se reproduce. Solo lectura.

Aviso que cambia el resultado: al leer metricas se usa `is not None` y nunca la verdad del valor,
porque un F1 de 0,0 es falsy en Python y descartarlo inflaria las medias.
"""
import collections
import csv
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
COLA = 'repos/ner-llm-entity-benchmark/'


def resuelve(ruta):
    """La ruta declarada, reanclada a este repositorio. None si no se puede reanclar."""
    if os.path.isabs(ruta):
        i = ruta.find(COLA)
        if i < 0:
            return None
        ruta = ruta[i + len(COLA):]
        cand = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark', ruta)
        return cand if os.path.exists(cand) else None
    for base in (RES, os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark'), RAIZ):
        cand = os.path.join(base, ruta)
        if os.path.exists(cand):
            return cand
    return None


def f1_de(fila):
    """La F1 de una fila del CSV, o None. Nunca descarta un 0,0."""
    for c in ('f1_score', 'f1'):
        v = fila.get(c)
        if v is not None and v != '':
            try:
                return float(v)
            except ValueError:
                return None
    return None


def main():
    cons = sys.argv[1] if len(sys.argv) > 1 else 'ANALISIS_CONJUNTO_20260909_FIX'
    dcon = os.path.join(RES, cons)
    man = json.load(open(os.path.join(dcon, 'merge_manifest.json'), encoding='utf-8'))
    print('acreditando %s' % cons)

    excl = set(man.get('contaminados_excluidos') or [])
    esperado = man.get('expected_n_per_group')
    print('  el manifiesto declara %d fuentes, %s filas, %d grupos, %s por grupo'
          % (man.get('num_sources', 0), man.get('merged_rows'),
             len(man.get('merged_groups') or []), esperado))
    print('  y excluye %d articulo(s) contaminado(s)' % len(excl))

    fallos = []

    # ── 1 y 2. resolucion de las fuentes y sus filas ──────────────────────────────────────────────
    fuentes = man.get('sources') or []
    reanclado = []
    for s in fuentes:
        ruta = s.get('csv_path') or ''
        loc = resuelve(ruta)
        if not loc:
            fallos.append('la fuente %s no resuelve aqui: %s' % (s.get('label'), ruta))
            continue
        todas = list(csv.DictReader(open(loc, encoding='utf-8')))
        # Una fuente aporta SOLO los grupos que el manifiesto le atribuye, no todas sus filas. Un
        # fichero de corrida puede contener grupos que la fusion descarta a proposito: el caso real
        # es afectados_thinking_n120_REMOTO, que trae 453 filas —los dos grupos de gemma4:12b-mlx
        # completos y dos de qwen3:8b PARCIALES, con 99 y 114 de 120— y de el solo entran los dos
        # primeros, porque los de qwen3 los aporta completos otra fuente. Tomar el fichero entero
        # mete resultados parciales en el agregado, que es precisamente lo que no debe pasar.
        decl = s.get('models')
        filas = [x for x in todas if x.get('model') in set(decl)] if decl else todas
        descartadas = len(todas) - len(filas)
        if s.get('rows') is not None and len(filas) != s['rows']:
            fallos.append('%s declara %d filas para sus grupos y se leen %d'
                          % (s.get('label'), s['rows'], len(filas)))
        elif descartadas:
            print('  %s: %d fila(s) de grupos que esta fuente NO aporta, descartadas como manda'
                  ' el manifiesto' % (s.get('label'), descartadas))
        reanclado.append((s, loc, filas))
    cuadran = len(reanclado) - sum(1 for f in fallos if 'declara' in f and 'filas para sus grupos' in f)
    print('  %d de %d fuentes reancladas · %d con las filas que declaran'
          % (len(reanclado), len(fuentes), cuadran))
    if len(reanclado) != len(fuentes):
        print('  NO se puede seguir: faltan fuentes')
        for f in fallos:
            print('    - %s' % f)
        return 1
    absol = sum(1 for s in fuentes if os.path.isabs(s.get('csv_path') or ''))
    if absol:
        print('  AVISO de forma, no de fondo: %d de %d rutas son ABSOLUTAS y de otra maquina.'
              % (absol, len(fuentes)))
        print('         Los datos estan; el manifiesto no es portable. Se acredita por la cola'
              ' «%s».' % COLA)

    # ── 3. reagregacion y contraste contra merged_results.csv ─────────────────────────────────────
    # Precedencia: un grupo puede venir en DOS fuentes, y el manifiesto declara cual gana. Las
    # notas dicen «--on-duplicate=first», de modo que manda la primera fuente en el orden en que el
    # manifiesto las lista. En el consolidado publicado son OCHO grupos, los cuatro modelos que se
    # re-corrieron: la corrida nueva desplaza a la vieja. Ignorar la precedencia duplica esos ocho
    # grupos y da 4 080 filas en lugar de 3 120, que es lo que le paso a la primera version de esta
    # herramienta y por lo que declaro NO reproducible un consolidado que si lo es.
    primero_gana = not any('on-duplicate=last' in str(n) for n in (man.get('duplicate_notes') or []))
    mio = collections.defaultdict(list)
    duenno = {}
    for s, loc, filas in reanclado:
        et = s.get('label')
        for fila in filas:
            if fila.get('record_id') in excl:
                continue
            g = fila.get('model')
            if g in duenno and duenno[g] != et:
                if primero_gana:
                    continue          # ya lo aporto una fuente anterior; esta se descarta
                mio[g] = []           # gana la ultima: se descarta lo acumulado
            duenno[g] = et
            mio[g].append(fila)
    n_dup = len(man.get('duplicate_notes') or [])
    if n_dup:
        print('  precedencia aplicada a %d grupo(s) duplicado(s), con la regla «%s» que declara el'
              ' manifiesto' % (n_dup, 'first' if primero_gana else 'last'))

    ref = collections.defaultdict(list)
    for fila in csv.DictReader(open(os.path.join(dcon, 'merged_results.csv'), encoding='utf-8')):
        ref[fila.get('model')].append(fila)

    n_mio = sum(len(v) for v in mio.values())
    n_ref = sum(len(v) for v in ref.values())
    print('  reagregado: %d filas en %d grupos · el consolidado: %d filas en %d grupos'
          % (n_mio, len(mio), n_ref, len(ref)))
    if n_mio != n_ref:
        fallos.append('la reagregacion da %d filas y el consolidado %d' % (n_mio, n_ref))
    if set(mio) != set(ref):
        fallos.append('los grupos no coinciden: sobran %s, faltan %s'
                      % (sorted(set(mio) - set(ref))[:3], sorted(set(ref) - set(mio))[:3]))
    if man.get('merged_rows') is not None and n_ref != man['merged_rows']:
        fallos.append('el manifiesto declara %d filas y el CSV trae %d'
                      % (man['merged_rows'], n_ref))

    # la F1 media por grupo, al cuarto decimal
    desajustes = 0
    comparados = 0
    for g in sorted(set(mio) & set(ref)):
        a = [f1_de(x) for x in mio[g]]
        b = [f1_de(x) for x in ref[g]]
        a = [x for x in a if x is not None]
        b = [x for x in b if x is not None]
        if not a or not b:
            continue
        comparados += 1
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        if abs(ma - mb) > 1e-4:
            desajustes += 1
            fallos.append('%s: F1 media reagregada %.4f frente a %.4f del consolidado'
                          % (g, ma, mb))
    print('  F1 media contrastada en %d grupos · %d desajuste(s) por encima de 1e-4'
          % (comparados, desajustes))

    # ── 4. la tabla integrity del manifiesto, contra los datos ───────────────────────────────────
    integ = man.get('integrity') or []
    mal = 0
    for e in integ:
        g = e.get('model')
        if g not in ref:
            mal += 1
            fallos.append('integrity nombra el grupo %s, que no esta en el consolidado' % g)
            continue
        if e.get('rows') is not None and len(ref[g]) != e['rows']:
            mal += 1
            fallos.append('integrity declara %d filas para %s y el CSV trae %d'
                          % (e['rows'], g, len(ref[g])))
        if esperado is not None and e.get('expected') not in (None, esperado):
            mal += 1
            fallos.append('integrity espera %s para %s y el manifiesto declara %s'
                          % (e.get('expected'), g, esperado))
    print('  tabla integrity: %d entradas examinadas · %d discrepancia(s)' % (len(integ), mal))

    print()
    if fallos:
        print('  NO acreditado: %d problema(s)' % len(fallos))
        for f in fallos[:20]:
            print('    - %s' % f)
        return 1
    print('  ACREDITADO: el consolidado se reproduce desde fuentes que existen en esta maquina,')
    print('  con las filas, los grupos, la precedencia y las medias que su manifiesto declara.')
    if absol:
        print('  Lo que queda es un defecto de FORMA del manifiesto —%d de %d rutas no son'
              % (absol, len(fuentes)))
        print('  portables—, y no impide comprobar el dato: no hay bloqueo por falta de datos.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
