#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_reconstruir_cuerpo.py — Reconstruye el cuerpo de una tabla de un `.docx` desde el Markdown.

Por que existe
--------------
`docx_reescribir_celdas.py` cambia valores pero no puede **anadir** ni **reordenar** filas. A la
Tabla 18 del informe le faltan cuatro filas legitimas —`nemotron-mini:4b` y `qwen3:8b`, en sus dos
modos— y ademas su orden no es el del Markdown, que la ordena por Δ descendente. Insertar en el
sitio correcto sin reordenar dejaria una tabla con las 26 filas en un orden que no es el de la
fuente, de modo que las dos cosas se resuelven igual: **reconstruir el cuerpo**.

Como
----
Se toma como **plantilla** la fila de datos mas frecuente de la tabla —su esqueleto XML con el
texto vaciado— y se genera una fila por cada linea del Markdown, en el orden del Markdown. La
cabecera **no se toca**.

Condiciones de seguridad, comprobadas antes de escribir nada
------------------------------------------------------------
1. La tabla se identifica por un fragmento de texto que **solo ella** contiene.
2. La plantilla tiene que tener el mismo numero de celdas que las filas del Markdown.
3. Cada celda de la plantilla tiene que contener **exactamente un** `<w:t>`.
4. El conjunto de filas resultante tiene que **contener** todas las que la tabla ya tenia: una
   reconstruccion no puede perder informacion. Si alguna fila del `.docx` no esta en el Markdown,
   no se toca nada y se reporta —seria una fila que solo existe en el entregable, y decidir que
   hacer con ella no es cosa de una herramienta—.

Que se pierde y hay que saberlo
-------------------------------
El formato **por fila** se normaliza al de la plantilla. Si una fila tenia un resalte propio, se
va. Antes de usar esto hay que comprobar que las filas de datos son uniformes; en la Tabla 18 lo
son, salvo dos que quedaron con un `xml:space="preserve"` de mas por un defecto ya corregido de
`docx_reescribir_celdas.py`, y ese atributo no tiene efecto visual.
"""
import os
import re
import sys
import json
import time
import shutil
import zipfile
import argparse
import collections
import hashlib

RE_TBL = re.compile(r'<w:tbl>.*?</w:tbl>', re.S)
RE_TR = re.compile(r'<w:tr[ >].*?</w:tr>', re.S)
RE_TC = re.compile(r'<w:tc>.*?</w:tc>', re.S)
RE_WT = re.compile(r'(<w:t(?:\s[^>]*)?>)(.*?)(</w:t>)', re.S)


def texto(frag):
    return ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', frag, re.S))


def escapar(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def esqueleto(fila):
    return RE_WT.sub(lambda m: m.group(1) + '@' + m.group(3), fila)


def plantilla_de(filas):
    """El esqueleto mas frecuente entre las filas de datos, con su fila de ejemplo."""
    c = collections.Counter()
    ejemplo = {}
    for f in filas:
        h = hashlib.md5(esqueleto(f).encode()).hexdigest()
        c[h] += 1
        ejemplo.setdefault(h, f)
    h, n = c.most_common(1)[0]
    return ejemplo[h], n, len(c)


def fila_con(plantilla, valores):
    """La plantilla con un valor en cada celda, en orden."""
    celdas = list(RE_TC.finditer(plantilla))
    out, ultimo = [], 0
    for c, v in zip(celdas, valores):
        out.append(plantilla[ultimo:c.start()])
        cel = RE_WT.sub(lambda m: m.group(1) + escapar(v) + m.group(3), c.group(0), count=1)
        out.append(cel)
        ultimo = c.end()
    out.append(plantilla[ultimo:])
    return ''.join(out)


def aplicar(xml, reglas):
    informe, pend = [], []
    for r in reglas:
        marca, filas_md = r['tabla_contiene'], r['filas_ordenadas']
        cand = [m for m in RE_TBL.finditer(xml) if marca in texto(m.group(0))]
        if len(cand) != 1:
            informe.append((r['id'], 0, 'la marca «%s» identifica %d tablas' % (marca, len(cand))))
            continue
        m = cand[0]
        trs = RE_TR.findall(m.group(0))
        cab, datos = trs[0], trs[1:]
        plant, n_igual, n_esq = plantilla_de(datos)
        ncel = len(RE_TC.findall(plant))
        errs = []
        if any(len(v) != ncel for v in filas_md):
            errs.append('la plantilla tiene %d celdas y alguna fila del Markdown no' % ncel)
        for c in RE_TC.findall(plant):
            if len(re.findall(r'<w:t(?:\s[^>]*)?>', c)) != 1:
                errs.append('una celda de la plantilla no tiene exactamente un <w:t>')
                break
        actuales = {texto(RE_TC.findall(f)[0]).strip() for f in datos}
        nuevas = {v[0] for v in filas_md}
        perdidas = sorted(actuales - nuevas)
        if perdidas:
            errs.append('la reconstruccion perderia %d fila(s) que el .docx tiene y el Markdown '
                        'no: %s' % (len(perdidas), perdidas[:4]))
        if errs:
            informe.append((r['id'], 0, ' · '.join(errs[:2])))
            continue
        cuerpo = ''.join(fila_con(plant, v) for v in filas_md)
        tbl_nueva = m.group(0).replace(''.join(datos), cuerpo, 1)
        if tbl_nueva == m.group(0):
            informe.append((r['id'], 0, 'no se pudo sustituir el cuerpo: las filas no son '
                                        'contiguas en el XML'))
            continue
        pend.append((m.start(), m.group(0), tbl_nueva))
        informe.append((r['id'], len(filas_md),
                        None if n_esq == 1 else
                        None))
        if n_esq > 1:
            informe.append(('%s*' % r['id'], 0,
                            'AVISO: habia %d esqueletos de fila y se usa el de %d filas; el '
                            'formato por fila se normaliza' % (n_esq, n_igual)))
    if any(e for _, _, e in informe if e and e.startswith('la ') or (e and 'no se pudo' in e)):
        return xml, informe
    nuevo = xml
    for inicio, viejo, nueva in sorted(pend, key=lambda x: -x[0]):
        nuevo = nuevo[:inicio] + nueva + nuevo[inicio + len(viejo):]
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
    duro = [e for _, _, e in informe if e and not e.startswith('AVISO')]
    if duro or dry_run or nuevo == xml:
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
        for rid, n, err in informe:
            if err and err.startswith('AVISO'):
                print('  %-5s %s' % (rid, err))
            elif err:
                print('  %-5s ERROR: %s' % (rid, err))
                malo = 1
            else:
                print('  %-5s cuerpo con %d fila(s)%s'
                      % (rid, n, ' (dry-run)' if a.dry_run else ''))
        if respaldo:
            print('  respaldo: %s' % respaldo)
    return malo


if __name__ == '__main__':
    sys.exit(main())
