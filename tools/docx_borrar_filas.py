#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_borrar_filas.py — Suprime filas `<w:tr>` de una tabla de un `.docx`, sin regenerarlo.

Por que existe
--------------
`docx_replace_terms.py` reemplaza texto y no puede suprimir una fila. El 2026-09-09 se encontro
que los tres `.docx` nombran cuatro modelos excluidos del estudio en quince sitios, mientras el
Markdown tiene cero (`FINDINGS §F94`), y que la correccion no es reformular sino **suprimir**:
el Markdown no reescribio la glosa, la elimino.

Por que suprimir una fila SI es seguro y parchear un valor no
------------------------------------------------------------
El 2026-09-09 se decidio **no** parchear cifras dentro de la Tabla 19 del `.docx`, porque cambiar
un `F1 restr.` sin cambiar el `P restr.` de su lado deja una fila internamente incoherente, peor
que la que habia. **Suprimir la fila entera no tiene ese problema:** las filas que quedan siguen
exactamente como estaban. De modo que la supresion se puede hacer ya, y el reemplazo de valores
espera a la pasada de maquetacion.

Como
----
Cada regla identifica **una tabla** por un fragmento de texto que solo ella contiene, y dentro de
ella las filas cuya **primera celda** coincide exactamente con uno de los valores dados. Se exige
el numero de filas que se espera suprimir; si no cuadra, no se toca nada y se reporta.

Se conserva todo lo demas byte a byte: el resto de las partes del paquete, su orden, su metodo de
compresion y el marcado XML de las filas que sobreviven.

Uso
---
  python3 tools/docx_borrar_filas.py --reglas tools/filas_excluidos.json --dry-run A.docx B.docx
  python3 tools/docx_borrar_filas.py --reglas tools/filas_excluidos.json --in-place A.docx B.docx
"""
import os
import re
import sys
import json
import time
import shutil
import zipfile
import argparse

RE_TBL = re.compile(r'<w:tbl>.*?</w:tbl>', re.S)
RE_TR = re.compile(r'<w:tr[ >].*?</w:tr>', re.S)
RE_TC = re.compile(r'<w:tc>.*?</w:tc>', re.S)
RE_WT = re.compile(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', re.S)


def texto(frag):
    """Texto visible de un fragmento de XML, uniendo los <w:t> con un espacio.

    `<w:t[^>]*>` encajaria tambien con `<w:tcPr>` y arrastraria marcado (§F88): se exige que
    tras `w:t` venga `>` o un espacio.
    """
    return ' '.join(RE_WT.findall(frag))


def primera_celda(fila):
    celdas = RE_TC.findall(fila)
    return texto(celdas[0]).strip() if celdas else ''


def aplicar(xml, reglas):
    """Devuelve (xml_nuevo, informe). No modifica nada si una regla no cuadra."""
    informe = []
    tablas = list(RE_TBL.finditer(xml))
    nuevo = xml
    # se procesa de atras adelante para que los offsets no se desplacen
    pendientes = []
    for r in reglas:
        marca, valores, esperadas = r['tabla_contiene'], set(r['primera_celda']), r['esperadas']
        cand = [m for m in tablas if marca in texto(m.group(0))]
        if len(cand) != 1:
            informe.append((r['id'], 0, 'la marca «%s» identifica %d tablas, no una'
                            % (marca, len(cand))))
            continue
        m = cand[0]
        filas = list(RE_TR.finditer(m.group(0)))
        fuera = [f for f in filas if primera_celda(f.group(0)) in valores]
        if len(fuera) != esperadas:
            informe.append((r['id'], len(fuera),
                            'se esperaban %d filas y se encontraron %d: %s'
                            % (esperadas, len(fuera),
                               [primera_celda(f.group(0)) for f in fuera])))
            continue
        pendientes.append((m.start(), m.group(0), fuera, r['id']))
        informe.append((r['id'], len(fuera), None))

    if any(err for _, _, err in informe):
        return xml, informe

    for inicio, tbl, fuera, rid in sorted(pendientes, key=lambda x: -x[0]):
        tbl_nueva = tbl
        for f in sorted(fuera, key=lambda x: -x.start()):
            tbl_nueva = tbl_nueva[:f.start()] + tbl_nueva[f.end():]
        nuevo = nuevo[:inicio] + tbl_nueva + nuevo[inicio + len(tbl):]
    return nuevo, informe


def _respaldo_libre(ruta, sufijo):
    """Nombre de respaldo que no pise uno existente.

    El 2026-09-09 `docx_borrar_filas.py` y `docx_replace_terms.py` se ejecutaron en el mismo
    segundo sobre los mismos ficheros, y como los dos derivan el sufijo de la marca de tiempo, el
    segundo **sobrescribio el respaldo del primero**: el `.bak` acabo guardando el estado
    intermedio y no el original. No se perdio nada —el original estaba en git y en respaldos
    anteriores—, pero un respaldo que se pisa no es un respaldo. Se anade un contador.
    """
    cand = ruta + sufijo
    n = 2
    while os.path.exists(cand):
        cand = '%s%s-%d' % (ruta, sufijo, n)
        n += 1
    return cand

def procesar(ruta, reglas, dry_run, respaldo_sufijo):
    with zipfile.ZipFile(ruta) as z:
        partes = [(i, z.read(i.filename)) for i in z.infolist()]
    idx = next((k for k, (i, _) in enumerate(partes)
                if i.filename == 'word/document.xml'), None)
    if idx is None:
        return None, [('-', 0, 'el paquete no trae word/document.xml')]
    xml = partes[idx][1].decode('utf-8')
    nuevo, informe = aplicar(xml, reglas)
    if any(err for _, _, err in informe) or dry_run:
        return nuevo != xml, informe
    respaldo = _respaldo_libre(ruta, respaldo_sufijo)
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
        cfg = json.load(fh)
    reglas = cfg['reglas']
    sufijo = '.bak_' + time.strftime('%Y%m%d-%H%M%S')
    malo = 0
    for ruta in a.docx:
        print('=' * 74)
        print('ARCHIVO : %s' % ruta)
        if not os.path.exists(ruta):
            print('  no existe')
            malo = 1
            continue
        res, informe = procesar(ruta, reglas, a.dry_run, sufijo)
        for rid, n, err in informe:
            if err:
                print('  %-4s ERROR: %s' % (rid, err))
                malo = 1
            else:
                print('  %-4s %d fila(s) suprimida(s)%s' % (rid, n, ' (dry-run)' if a.dry_run else ''))
        if not a.dry_run and isinstance(res, str):
            print('  respaldo: %s' % res)
        if not any(err for _, _, err in informe):
            print('  todas las reglas aplicadas segun lo esperado')
    return malo


if __name__ == '__main__':
    sys.exit(main())
