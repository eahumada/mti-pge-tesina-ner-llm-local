#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba que la politica aditiva se cumplio: que nada se perdio de los documentos que no borran.

La politica del proyecto es **estrictamente aditiva** para la documentacion. Pero «aditiva» no
significa que ninguna linea cambie nunca: un titulo se corrige, una cifra mantenida a mano se retira,
un estado de tarea pasa de PENDIENTE a COMPLETADA. Lo que no puede pasar es que una afirmacion, una
fila de datos o una entrada del registro **desaparezca sin dejar rastro**.

Esta herramienta distingue las dos cosas. Para cada linea borrada de un documento aditivo en un rango
de commits, comprueba si se da alguna de estas tres circunstancias, que son borrados **legitimos**:

  1. **Reescritura en el sitio.** El mismo commit anade una linea muy parecida. Es el caso de una
     correccion de redaccion o de un estado de tarea que avanza.
  2. **Sigue viva.** El texto borrado esta hoy en el fichero, en otro sitio. Es el caso de un
     parrafo que se movio de seccion.
  3. **Conservada tachada.** El texto esta hoy en el fichero dentro de un tachado `~~...~~`, que es
     como este proyecto rectifica sin borrar: `§F106` conserva asi su titulo original.

Si una linea borrada no cumple ninguna, se reporta como **posible perdida** con su commit, para que
alguien la mire. Devuelve 0 si no hay ninguna. Solo lectura; no toca git ni el arbol.

    python3 tools/auditar_borrados.py                 # desde medianoche de hoy
    python3 tools/auditar_borrados.py --desde 3.days  # cualquier expresion que entienda git log
"""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Los documentos que no borran. Los ficheros de datos y los logs no entran: tienen su propia
# politica —los logs se conservan enteros— y un CSV reescrito no es una perdida de informacion.
ADITIVOS = (
    'FINDINGS.md',
    'LEARNING.md',
    'CURRENT-TASKS.md',
    'CLAUDE.md',
    'HISTORIAL-CONSOLIDADO.md',
    'TODO-INFORME-FINAL.md',
    'DECISIONES-PENDIENTES-20260908.md',
)

MIN_LONG = 25          # una linea mas corta que esto no afirma nada por si sola
UMBRAL_PARECIDO = 0.55  # por encima de esto, se considera reescritura en el sitio


def _parecido(a, b):
    """Similitud por subsecuencia comun mas larga, en biblioteca estandar. 0 a 1."""
    if not a or not b:
        return 0.0
    m, n = len(a), len(b)
    ant = [0] * (n + 1)
    for i in range(1, m + 1):
        act = [0] * (n + 1)
        ai = a[i - 1]
        for j in range(1, n + 1):
            act[j] = ant[j - 1] + 1 if ai == b[j - 1] else max(ant[j], act[j - 1])
        ant = act
    return 2.0 * ant[n] / (m + n)


def _norm(t):
    return ' '.join(t.split())


def main():
    desde = 'midnight'
    if '--desde' in sys.argv:
        desde = sys.argv[sys.argv.index('--desde') + 1]
    os.chdir(RAIZ)

    print('auditando la politica aditiva desde «%s»' % desde)
    sospechas = []
    examinadas = 0
    ficheros = 0

    for f in ADITIVOS:
        if not os.path.exists(f):
            continue
        ficheros += 1
        vivo = open(f, encoding='utf-8').read()
        vivo_n = _norm(vivo)
        salida = subprocess.run(
            ['git', 'log', '--since', desde, '-p', '--format=COMMIT %h %s', '--', f],
            capture_output=True, text=True).stdout
        commit = ''
        borradas, anadidas = [], []

        def cierra():
            """Al terminar un commit, contrasta sus borrados contra sus anadidos."""
            for b in borradas:
                nb = _norm(b)
                if len(nb) < MIN_LONG:
                    continue
                globals()['_EX'] = globals().get('_EX', 0) + 1
                # 1. reescritura en el sitio
                if any(_parecido(nb, _norm(a)) >= UMBRAL_PARECIDO for a in anadidas):
                    continue
                # 2. sigue viva hoy
                if nb in vivo_n:
                    continue
                # 3. conservada tachada
                nucleo = nb.lstrip('#').strip().lstrip('|').strip()
                if nucleo and ('~~%s' % nucleo[:60]) in _norm(vivo).replace('~~ ', '~~'):
                    continue
                if nucleo and nucleo[:60] in vivo_n:
                    continue
                sospechas.append((f, commit, b))
            del borradas[:]
            del anadidas[:]

        for l in salida.split('\n'):
            if l.startswith('COMMIT '):
                cierra()
                commit = l[7:]
            elif l.startswith('-') and not l.startswith('---'):
                borradas.append(l[1:])
            elif l.startswith('+') and not l.startswith('+++'):
                anadidas.append(l[1:])
        cierra()

    examinadas = globals().get('_EX', 0)
    print('  %d documento(s) aditivo(s) · %d linea(s) borrada(s) con contenido, examinadas'
          % (ficheros, examinadas))
    if examinadas == 0:
        print('  VACIA: no habia ninguna linea borrada que examinar en ese rango.')
        print('  Una comprobacion que no mira nada no es una comprobacion superada.')
        return 0
    if not sospechas:
        print()
        print('  Ninguna perdida: cada borrado es una reescritura en el sitio, un texto que sigue')
        print('  vivo en el fichero, o una rectificacion conservada con tachado.')
        return 0

    print()
    print('  %d posible(s) perdida(s), que hay que mirar una a una:' % len(sospechas))
    for f, c, b in sospechas[:40]:
        print('    %s  [%s]' % (f, c[:70]))
        print('      - %s' % b.strip()[:150])
    return 1


if __name__ == '__main__':
    sys.exit(main())
