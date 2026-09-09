#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_reglas_tablas_docx.py — Deriva del Markdown las reglas de reescritura de celdas.

Los valores no se teclean: se leen de la fuente canonica. Es §L63 —un valor copiado a mano en un
fichero de reglas es una segunda fuente de verdad que deja de coincidir sin avisar— aplicado a la
propagacion de tablas.

Genera `tools/celdas_tablas_docx.json` para `docx_reescribir_celdas.py`, con dos tablas:

  Tabla 19  «F1 restr.»         42 filas x 7 celdas
  Tabla 18  «Δ F1 por entidad»  las filas que el `.docx` tiene, 2 celdas

De la Tabla 18 se generan **solo las filas que el `.docx` ya trae**, porque reescribir celdas no
puede anadir filas: al `.docx` le faltan cuatro legitimas y eso exige insertar, no reescribir. Se
declara en la salida para que no se confunda con una propagacion completa.
"""
import os
import re
import sys
import json
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, 'doc/organized/Hito_5_Tarea4_Informe_Final',
                  '2026-07-04_Borrador-Informe-Final-Tesina.md')
DOCX = os.path.join(RAIZ, 'Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx')
SALIDA = os.path.join(RAIZ, 'tools/celdas_tablas_docx.json')


def filas_md(cabecera, ncols):
    with open(MD, encoding='utf-8') as fh:
        t = fh.read()
    i = t.find(cabecera)
    if i < 0:
        return None
    out = {}
    for l in t[i:].split('\n')[2:]:
        if not l.startswith('|'):
            break
        c = [y.strip().strip('`') for y in l.strip('|').split('|')]
        if len(c) == ncols:
            out[c[0]] = c[1:]
    return out


def filas_docx(marca):
    with zipfile.ZipFile(DOCX) as z:
        x = z.read('word/document.xml').decode('utf-8')
    T = lambda s: ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', s, re.S))
    cand = [b for b in re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S) if marca in T(b)]
    if len(cand) != 1:
        return None
    out = []
    for f in re.findall(r'<w:tr[ >].*?</w:tr>', cand[0], re.S)[1:]:
        celdas = re.findall(r'<w:tc>.*?</w:tc>', f, re.S)
        out.append(T(celdas[0]).strip())
    return out


def main():
    t19 = filas_md('| Configuración | Corrida | P | R | F1 | P restr. | F1 restr. | Δ F1 |', 8)
    t18 = filas_md('| Configuración | Δ F1 por entidad de referencia | Δ F1 por texto de entrada |', 3)
    if t19 is None or t18 is None:
        print('  no se encuentran las cabeceras en el Markdown')
        return 2
    d19, d18 = filas_docx('F1 restr.'), filas_docx('Δ F1 por entidad')
    if d19 is None or d18 is None:
        print('  no se identifica una de las tablas en el .docx')
        return 2

    # La Tabla 19 debe cuadrar fila por fila; si no, no se genera nada.
    if set(d19) != set(t19):
        print('  la Tabla 19 no cuadra: solo en docx %s · solo en MD %s'
              % (sorted(set(d19) - set(t19))[:3], sorted(set(t19) - set(d19))[:3]))
        return 2

    # De la Tabla 18, solo las filas que el .docx ya tiene.
    faltan = [k for k in d18 if k not in t18]
    if faltan:
        print('  la Tabla 18 del .docx trae filas que el Markdown no tiene: %s' % faltan[:4])
        return 2
    sub18 = {k: t18[k] for k in d18}
    sin_propagar = sorted(set(t18) - set(d18))

    cfg = {
        '_comment': [
            'GENERADO por tools/generar_reglas_tablas_docx.py desde el Markdown canonico.',
            'No editar a mano: se regenera. Los valores se leen de la fuente (§L63).',
            '',
            'R19: las %d filas de la Tabla 19, 7 celdas cada una. Los conjuntos de filas del' % len(t19),
            '     .docx y del Markdown coinciden exactamente, comprobado antes de generar.',
            '',
            'R18: las %d filas que el .docx trae. Reescribir celdas NO anade filas.' % len(sub18),
            ('     Al .docx le faltan estas %d legitimas, que exigen insercion: %s'
             % (len(sin_propagar), ', '.join(sin_propagar))) if sin_propagar else
            '     No le falta ninguna: coincide con el Markdown en el conjunto de filas.',
        ],
        'reglas': [
            {'id': 'R19', 'tabla_contiene': 'F1 restr.', 'filas': t19},
            {'id': 'R18', 'tabla_contiene': 'Δ F1 por entidad', 'filas': sub18},
        ],
    }
    with open(SALIDA, 'w', encoding='utf-8') as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print('  escrito %s' % os.path.relpath(SALIDA, RAIZ))
    print('    R19: %d filas x 7 celdas = %d celdas' % (len(t19), 7 * len(t19)))
    print('    R18: %d filas x 2 celdas = %d celdas' % (len(sub18), 2 * len(sub18)))
    print('    filas de la Tabla 18 SIN PROPAGAR (exigen insercion, no reescritura): %d'
          % len(sin_propagar))
    for k in sin_propagar:
        print('      - %s' % k)
    return 0


if __name__ == '__main__':
    sys.exit(main())
