#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_partir_run.py — Parte un `<w:r>` para que el resalte cubra solo el trozo que debe.

Por que existe
--------------
`docx_replace_terms.py` escribe el texto nuevo **dentro** del run que ya existia, con su formato.
El 2026-09-09 eso dejo en §3.3 una frase entera en negrita donde el Markdown resalta solo el
porcentaje: la sustitucion era correcta en el texto y heredaba un enfasis que la fuente no tiene.
Es una de las 17 divergencias de resalte que §F96 cuenta, y la unica introducida por una edicion
propia, de modo que arreglarla es cerrar lo que se abrio.

Que hace
--------
Cada regla da el **texto completo del run** y el **trozo que debe conservar el resalte**. El run
se parte en hasta tres:

    [antes]  sin la propiedad de resalte
    [trozo]  con el `rPr` original intacto
    [despues] sin la propiedad de resalte

Si al quitar la propiedad el `rPr` se queda vacio, se omite entero, que es lo que produce texto de
cuerpo normal.

Condiciones de seguridad
------------------------
1. El texto del run tiene que aparecer **exactamente una vez** en el documento.
2. El trozo a resaltar tiene que estar **una sola vez** dentro de ese texto.
3. El run tiene que llevar la propiedad que se va a quitar; si no, no hay nada que partir y se
   reporta en lugar de fingir que se hizo algo.

Si alguna falla, no se toca nada.
"""
import os
import re
import sys
import json
import time
import shutil
import zipfile
import argparse


def escapar(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _run(rpr, texto):
    """Un `<w:r>` con el rPr dado (o ninguno) y el texto, preservando espacios."""
    if not texto:
        return ''
    r = '<w:r>'
    if rpr:
        r += rpr
    r += '<w:t xml:space="preserve">%s</w:t></w:r>' % escapar(texto)
    return r


def aplicar(xml, reglas):
    informe = []
    nuevo = xml
    for r in reglas:
        texto, trozo = r['texto_del_run'], r['resaltar']
        prop = r.get('propiedad', '<w:b/>')
        # el run cuyo <w:t> contiene exactamente ese texto
        pat = re.compile(r'<w:r>((?:(?!</w:r>).)*?)<w:t(\s[^>]*)?>%s</w:t></w:r>'
                         % re.escape(escapar(texto)), re.S)
        ms = list(pat.finditer(nuevo))
        if len(ms) != 1:
            informe.append((r['id'], 'el texto del run aparece en %d runs, no en uno' % len(ms)))
            continue
        m = ms[0]
        rpr = m.group(1) or ''
        if prop not in rpr:
            informe.append((r['id'], 'el run no lleva %s: nada que partir' % prop))
            continue
        if texto.count(trozo) != 1:
            informe.append((r['id'], 'el trozo a resaltar aparece %d veces en el texto, no una'
                            % texto.count(trozo)))
            continue
        i = texto.index(trozo)
        antes, despues = texto[:i], texto[i + len(trozo):]
        rpr_sin = rpr.replace(prop, '')
        if re.fullmatch(r'<w:rPr>\s*</w:rPr>', rpr_sin or ''):
            rpr_sin = ''
        reemplazo = _run(rpr_sin, antes) + _run(rpr, trozo) + _run(rpr_sin, despues)
        nuevo = nuevo[:m.start()] + reemplazo + nuevo[m.end():]
        informe.append((r['id'], None))
    return nuevo, informe


def _respaldo_libre(ruta, sufijo):
    cand, n = ruta + sufijo, 2
    while os.path.exists(cand):
        cand, n = '%s%s-%d' % (ruta, sufijo, n), n + 1
    return cand


def procesar(ruta, reglas, dry_run, sufijo):
    with zipfile.ZipFile(ruta) as z:
        partes = [(i, z.read(i.filename)) for i in z.infolist()]
    idx = next((k for k, (i, _) in enumerate(partes) if i.filename == 'word/document.xml'), None)
    xml = partes[idx][1].decode('utf-8')
    nuevo, informe = aplicar(xml, reglas)
    if any(e for _, e in informe) or dry_run or nuevo == xml:
        return None, informe
    respaldo = _respaldo_libre(ruta, sufijo)
    shutil.copy2(ruta, respaldo)
    partes[idx] = (partes[idx][0], nuevo.encode('utf-8'))
    tmp = ruta + '.tmp'
    with zipfile.ZipFile(tmp, 'w') as out:
        for info, datos in partes:
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.internal_attr = info.internal_attr
            zi.create_system = info.create_system
            zi.comment = info.comment
            out.writestr(zi, datos)
    os.replace(tmp, ruta)
    return respaldo, informe


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--reglas', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--in-place', action='store_true')
    ap.add_argument('docx', nargs='+')
    a = ap.parse_args()
    if not (a.dry_run or a.in_place):
        print('  hay que elegir --dry-run o --in-place')
        return 2
    with open(a.reglas, encoding='utf-8') as fh:
        reglas = json.load(fh)['reglas']
    sufijo = '.bak_' + time.strftime('%Y%m%d-%H%M%S')
    malo = 0
    for ruta in a.docx:
        print('=' * 74)
        print('ARCHIVO : %s' % ruta)
        respaldo, informe = procesar(ruta, reglas, a.dry_run, sufijo)
        for rid, err in informe:
            if err:
                print('  %-4s ERROR: %s' % (rid, err))
                malo = 1
            else:
                print('  %-4s run partido%s' % (rid, ' (dry-run)' if a.dry_run else ''))
        if respaldo:
            print('  respaldo: %s' % respaldo)
    return malo


if __name__ == '__main__':
    sys.exit(main())
