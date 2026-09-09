#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ensayo_adopcion.py — Qué costaría adoptar otro consolidado, sin adoptarlo.

Por qué existe
--------------
La decisión 1 —si el informe adopta el consolidado nuevo— estaba respondida en cuanto a si la
conclusión sobrevive (`FINDINGS §F123`), y sin embargo **nadie había comprobado qué haría el
verificador el día de la adopción**. Hecho a mano el 2026-09-09, encontró dos bloqueos del
consolidado nuevo y una comprobación que reventaba en el estadístico titular (`§F131`).

Lo hice copiando el verificador a `tools/`, sustituyendo un nombre y borrando la copia. Eso es
frágil, irrepetible y ensucia el directorio de herramientas. Y hay que **volver a ejecutarlo**
cuando el equipo de 48 GB arregle el manifiesto y entregue el `levene.json`, porque la lista de
trabajo cambiará. De modo que se mecaniza.

Qué hace
--------
Carga el verificador en memoria con las rutas del consolidado que se le indique, lo ejecuta y
**compara sus resultados con los del consolidado actual**. La salida no es «pasa o falla»: es la
**lista de trabajo** que la adopción produciría, comprobación por comprobación, con las cifras que
habría que rehacer.

No escribe nada. No toca el verificador del repositorio, no crea ficheros temporales dentro de
`tools/` y no modifica ningún consolidado. Es un ensayo.

Limitación, declarada
---------------------
La sustitución es **textual** sobre la fuente del verificador en memoria: cambia el nombre del
directorio del consolidado por otro. Si alguna comprobación construyera esa ruta de una forma que
la sustitución no alcance, esa comprobación seguiría leyendo el consolidado viejo y **aparecería
como que no cambia**. El recuento de sustituciones se imprime para que se pueda juzgar: el día que
baje sin motivo, alguien ha cambiado cómo se nombra el consolidado.
"""
import argparse
import importlib.util
import os
import sys
import types

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = os.path.join(RAIZ, 'tools/verificar_informe.py')
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
ACTUAL = 'ANALISIS_CONJUNTO_20260907'


def _corre(consolidado):
    """Ejecuta el verificador con el consolidado indicado y devuelve sus resultados.

    Se carga desde la fuente en memoria, con un nombre de modulo propio para que dos ejecuciones
    no se pisen el estado global `resultados`.
    """
    with open(VER, encoding='utf-8') as fh:
        src = fh.read()
    n = src.count(ACTUAL)
    if consolidado != ACTUAL:
        src = src.replace(ACTUAL, consolidado)
    mod = types.ModuleType('_ver_%s' % consolidado.replace('-', '_').replace('.', '_'))
    mod.__file__ = VER          # para que RAIZ salga bien
    mod.__dict__['__name__'] = mod.__name__
    # El verificador imprime sus 56 comprobaciones al ejecutarse, y aqui se ejecuta DOS veces:
    # sin silenciarlo, la salida propia de esta herramienta queda sepultada bajo dos informes
    # completos y no se lee. Se captura y se descarta.
    import contextlib
    import io
    argv = sys.argv
    sys.argv = ['verificar_informe.py']
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, VER, 'exec'), mod.__dict__)
            mod.resultados.clear()
            try:
                mod.main()
            except SystemExit:
                pass
    finally:
        sys.argv = argv
    return n, list(mod.resultados)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('consolidado', nargs='?', default='ANALISIS_CONJUNTO_20260909_FIX',
                    help='nombre del directorio del consolidado a ensayar '
                         '(por omision, ANALISIS_CONJUNTO_20260909_FIX)')
    ap.add_argument('--detalle', action='store_true',
                    help='imprime todos los mensajes, no solo los tres primeros por comprobacion')
    a = ap.parse_args()

    if not os.path.isdir(os.path.join(RES, a.consolidado)):
        print('  no existe %s' % os.path.join('results', a.consolidado))
        print('  consolidados disponibles: %s'
              % ', '.join(sorted(d for d in os.listdir(RES) if d.startswith('ANALISIS_CONJUNTO'))))
        return 2

    print('  ensayo de adopcion: %s  ->  %s\n' % (ACTUAL, a.consolidado))
    n_sust, antes = _corre(ACTUAL)
    _, despues = _corre(a.consolidado)
    print('  referencias al consolidado sustituidas en la fuente: %d' % n_sust)
    if n_sust == 0:
        print('  VACIA: cero sustituciones, el ensayo no ha ensayado nada')
        return 2

    ant = {nom: fs for nom, _e, fs, _n in antes}
    des = {nom: fs for nom, _e, fs, _n in despues}
    nuevas, resueltas, revientan = [], [], []
    for nom, fs in des.items():
        prev = set(ant.get(nom, []))
        extra = [f for f in fs if f not in prev]
        if 'reventó' in nom or 'revento' in nom:
            revientan.append((nom, fs))
        elif extra:
            nuevas.append((nom, extra))
    for nom, fs in ant.items():
        if fs and not des.get(nom):
            resueltas.append(nom)

    if revientan:
        print('\n  ══ COMPROBACIONES QUE REVIENTAN con el consolidado nuevo ══')
        print('     Una que revienta no comprueba nada. Hay que arreglarla ANTES de adoptar.')
        for nom, fs in revientan:
            print('     %s' % nom)
            for f in fs:
                print('        %s' % f[:170])

    print('\n  ══ LISTA DE TRABAJO: %d comprobacion(es) con fallos nuevos ══' % len(nuevas))
    total = 0
    for nom, fs in sorted(nuevas, key=lambda x: -len(x[1])):
        total += len(fs)
        print('\n     %s  (%d fallo(s) nuevo(s))' % (nom, len(fs)))
        for f in (fs if a.detalle else fs[:3]):
            print('        - %s' % f[:170])
        if not a.detalle and len(fs) > 3:
            print('        ... y %d mas (usar --detalle)' % (len(fs) - 3))
    print('\n  %d fallos nuevos en total' % total)

    if resueltas:
        print('\n  ══ Y lo que la adopcion ARREGLA ══')
        for nom in sorted(resueltas):
            print('     %s deja de fallar' % nom)

    print('\n  Esto no adopta nada: el verificador del repositorio no se ha tocado y no se ha')
    print('  escrito ningun fichero. Volver a ejecutarlo cuando cambie el consolidado nuevo.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
