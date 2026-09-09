#!/usr/bin/env python3
"""Detecta documentos de estado desfasados respecto de lo que describen.

Un documento de seguimiento fechado envejece con cada commit a los ficheros que
describe, y nada avisa: sigue abriendose, sigue leyendose y sus casillas siguen
vacias. El 2026-09-08 tres documentos del proyecto estaban asi a la vez —la lista
de propagacion a los `.docx` por cinco commits, `TODO-INFORME-FINAL.md` por
setenta y el inventario de datos incorrectos por setenta y seis— y el ultimo
cerraba afirmando que nada se habia ejecutado cuando parte si.

Para cada documento vigilado se cuenta cuantos commits han tocado sus fuentes
desde que el documento se actualizo por ultima vez. Un desfase no es un error por
si mismo: significa que hay que releerlo antes de fiarse.

    python3 tools/desfase_documentos.py            # informe
    python3 tools/desfase_documentos.py --umbral 5 # falla si alguno lo supera
"""
import argparse
import subprocess
import sys

MD = ('doc/organized/Hito_5_Tarea4_Informe_Final/'
      '2026-07-04_Borrador-Informe-Final-Tesina.md')
BENCH = 'repos/ner-llm-entity-benchmark/results'

# documento -> ficheros o directorios cuyo cambio lo desactualiza
VIGILADOS = {
    'CURRENT-TASKS.md': ['.'],
    'PROPAGACION-PENDIENTE-DOCX-20260908.md': [MD],
    'TODO-INFORME-FINAL.md': [MD, 'Informe_Final_Tesina_NER.docx'],
    'INVENTARIO-DATOS-INCORRECTOS-20260908.md': [BENCH],
    'ESTADO-RECORRIDA-20260908.md': [BENCH],
    'DECISIONES-PENDIENTES-20260908.md': ['FINDINGS.md', MD],
    'DEFENSA-PREGUNTAS-Y-RESPUESTAS.md': [MD, 'FINDINGS.md'],
    'README.md': ['CLAUDE.md', 'tools'],
}


def git(*args):
    return subprocess.run(['git', *args], capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--umbral', type=int, default=None,
                    help='devuelve 1 si algun documento supera este desfase')
    args = ap.parse_args()

    filas = []
    for doc, fuentes in VIGILADOS.items():
        sha = git('log', '-1', '--format=%H', '--', doc)
        if not sha:
            filas.append((doc, None, 0, 'sin historial en git'))
            continue
        cuando = git('log', '-1', '--format=%ad', '--date=format:%m-%d %H:%M', '--', doc)
        salida = git('log', '--format=%h', f'{sha}..HEAD', '--', *fuentes)
        n = len([x for x in salida.split('\n') if x])
        filas.append((doc, cuando, n, ''))

    filas.sort(key=lambda f: -f[2])
    ancho = max(len(f[0]) for f in filas)
    print(f'{"documento":{ancho}}  actualizado    commits a sus fuentes desde entonces')
    print('-' * (ancho + 46))
    for doc, cuando, n, nota in filas:
        marca = '  <-- releer antes de fiarse' if n else ''
        print(f'{doc:{ancho}}  {cuando or "—":13}  {n:>3}{marca}  {nota}')

    peor = max(f[2] for f in filas)
    print(f'\ndesfase mayor: {peor} commits')
    if args.umbral is not None and peor > args.umbral:
        print(f'supera el umbral de {args.umbral}')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
