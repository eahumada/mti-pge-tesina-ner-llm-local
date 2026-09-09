#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
desfase_cifras_docx.py — Compara TODAS las cifras decimales de un `.docx` contra el Markdown canonico.

Por que existe
--------------
El 2026-09-09 se encontraron a mano tres cifras titulares obsoletas en los tres `.docx`
—76,85 / 90,91 / 81,45, en catorce sitios por documento, resumen y abstract incluidos—.
Encontrarlas de una en una no acredita que no queden mas: acredita que se miraron esas.
Esta herramienta hace la comparacion completa.

Como
----
Extrae los numeros decimales de los dos lados y compara sus CONJUNTOS:

  * presente en el `.docx` y ausente del Markdown  -> candidata a OBSOLETA
  * presente en el Markdown y ausente del `.docx`  -> candidata a NO PROPAGADA

El separador decimal se normaliza, de modo que `76,85` y `76.85` son la misma cifra: el informe
usa coma en la prosa espanola y punto en las tablas, y tratarlas como distintas daria ruido puro.

La trampa de las tablas
-----------------------
Word parte el texto en elementos `<w:t>`, y una fila de tabla concatenada sin separador produce
basura como `62.6782.2576.85`, que tokenizada da cifras que nadie escribio. Por eso el texto se
reconstruye **uniendo cada `<w:t>` con un separador**, no pegandolos. El precio es que un numero
partido entre dos runs se pierde; se cuentan y se declaran (`partidos`), porque una herramienta
que descarta en silencio es peor que no tenerla.

Limite declarado
----------------
Una cifra puede coincidir por casualidad: `0.05` es un umbral estadistico y aparece en los dos
lados por motivos distintos. La herramienta senala CANDIDATAS, no defectos. El juicio es humano,
y para eso imprime el contexto de cada una.
"""
import os
import re
import sys
import zipfile
import argparse
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, 'doc/organized/Hito_5_Tarea4_Informe_Final',
                  '2026-07-04_Borrador-Informe-Final-Tesina.md')
DOCX = os.path.join(RAIZ, 'Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx')

SEP = '\x00'
NUM = re.compile(r'(?<![\d.,])(\d{1,3})[.,](\d{1,2})(?![\d.,])')


def texto_docx(ruta):
    """Texto visible, uniendo cada <w:t> con un separador, y el numero de numeros partidos."""
    with zipfile.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    # OJO: `<w:t[^>]*>` tambien encaja con `<w:tcPr>`, `<w:tc>` y `<w:tbl>`, y arrastra XML al
    # texto. Hay que exigir que tras `w:t` venga `>` o un espacio. Lo dio la propia herramienta:
    # imprimia como contexto de una cifra `<w:jc w:val="left"/>...<w:t>43.29`.
    trozos = re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S)
    unido = SEP.join(trozos)
    # Un numero PARTIDO entre runs no es lo mismo que dos celdas numericas contiguas. Contar
    # `digito SEP digito` da lo segundo: en una fila de tabla, `43.29` seguida de `38.91` encaja
    # y no hay nada partido. La primera version de esta herramienta contaba asi y daba 257 donde
    # hay 3. La prueba correcta es que la union forme un decimal valido y que NINGUNO de los dos
    # lados sea ya un decimal completo por su cuenta.
    partidos = 0
    for izq, der in zip(trozos, trozos[1:]):
        mi = re.search(r'[\d.,]+$', izq or '')
        md_ = re.match(r'[\d.,]+', der or '')
        if not mi or not md_:
            continue
        a, b = mi.group(), md_.group()
        completo = re.compile(r'^\d{1,3}[.,]\d{1,2}$')
        if re.match(r'^\d{1,3}[.,]\d{1,2}$', a + b) \
                and not completo.match(a) and not completo.match(b):
            partidos += 1
    for e, c in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")):
        unido = unido.replace(e, c)
    return unido, partidos


def texto_md(ruta):
    with open(ruta, encoding='utf-8') as fh:
        t = fh.read()
    # los bloques de codigo llevan cifras de configuracion que no son resultados
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    return t


def cifras(t):
    """Cuenta las cifras decimales normalizando el separador, con un contexto por cifra."""
    c, ctx = Counter(), {}
    for m in NUM.finditer(t):
        k = '%s.%s' % (m.group(1), m.group(2))
        c[k] += 1
        if k not in ctx:
            a = max(0, m.start() - 70)
            ctx[k] = re.sub(r'\s+', ' ', t[a:m.end() + 55].replace(SEP, ' ')).strip()
    return c, ctx


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--docx', default=DOCX)
    ap.add_argument('--md', default=MD)
    ap.add_argument('--todas', action='store_true',
                    help='no recortar la lista de candidatas')
    a = ap.parse_args()

    for r in (a.docx, a.md):
        if not os.path.exists(r):
            print('  falta %s' % r)
            return 2

    td, partidos = texto_docx(a.docx)
    tm = texto_md(a.md)
    cd, xd = cifras(td)
    cm, xm = cifras(tm)

    print('  %s' % os.path.basename(a.docx))
    print('  contra %s' % os.path.basename(a.md))
    print('  cifras decimales distintas: %d en el .docx, %d en el Markdown' % (len(cd), len(cm)))
    if partidos:
        print('  numeros partidos entre runs, no examinados: %d '
              '(el reemplazo los repara solo; aqui se declaran)' % partidos)

    solo_d = sorted(set(cd) - set(cm), key=lambda k: -cd[k])
    solo_m = sorted(set(cm) - set(cd), key=lambda k: -cm[k])

    def tabla(titulo, claves, cnt, ctx, tope):
        print('\n  %s: %d' % (titulo, len(claves)))
        if not claves:
            print('    ninguna')
            return
        for k in (claves if a.todas else claves[:tope]):
            print('    %-9s x%-3d %s' % (k, cnt[k], ctx[k][:110]))
        if not a.todas and len(claves) > tope:
            print('    ... y %d mas (--todas para verlas)' % (len(claves) - tope))

    tabla('en el .docx y NO en el Markdown, candidatas a obsoletas', solo_d, cd, xd, 25)
    tabla('en el Markdown y NO en el .docx, candidatas a no propagadas', solo_m, cm, xm, 25)

    examinadas = len(set(cd) | set(cm))
    print('\n  examinadas %d cifras distintas · %d solo en el .docx · %d solo en el Markdown'
          % (examinadas, len(solo_d), len(solo_m)))
    if examinadas == 0:
        print('  VACIA: no se examino ninguna cifra, que no es lo mismo que no haber desfase')
        return 2
    print('  son CANDIDATAS, no defectos: una cifra puede coincidir o diferir por motivos legitimos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
