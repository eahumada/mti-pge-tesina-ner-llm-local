#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_reescribir_celdas.py — Reescribe el contenido de celdas de una tabla de un `.docx`.

Por que existe
--------------
`docx_replace_terms.py` reemplaza texto por texto y `docx_borrar_filas.py` suprime filas. Faltaba
poder poner en cada celda de una tabla el valor que le corresponde, que es lo que exige propagar
una tabla entera recalculada: la Tabla 19 del informe difiere del Markdown **en las 42 filas**, y
la 18 en dos de sus veintidos.

Por que no se hizo antes, y que cambio
--------------------------------------
El 2026-09-09 se decidio no parchear cifras dentro de esas tablas, porque cambiar un `F1 restr.`
sin cambiar el `P restr.` de su lado deja una fila internamente incoherente, peor que la que
habia. Eso vale para un parcheo **parcial**. Reescribir **todas** las celdas de la fila desde la
fuente canonica no tiene ese problema: la fila queda como en el Markdown, entera.

Condiciones de seguridad, todas comprobadas antes de escribir nada
-----------------------------------------------------------------
1. La tabla se identifica por un fragmento de texto que **solo ella** contiene.
2. Las filas se emparejan por su **primera celda**, no por su posicion, de modo que un cambio de
   orden no descoloca nada.
3. Toda fila de la tabla tiene que aparecer en las reglas y toda regla en la tabla: si sobra o
   falta una, no se toca nada. Un reemplazo parcial es justo lo que hay que evitar.
4. Cada celda de destino tiene que contener **exactamente un** `<w:t>`. Comprobado el 2026-09-09:
   294 celdas de la Tabla 19 y 44 de la 18, todas con uno.
5. El numero de valores de cada regla tiene que coincidir con el numero de celdas de la fila.

Si alguna falla, se reporta y el fichero no se modifica.

Los valores NO se escriben a mano
---------------------------------
Las reglas se generan desde el Markdown canonico con `--desde-md`, por la razon de §L63: un valor
copiado a mano en un fichero de reglas es una segunda fuente de verdad que deja de coincidir sin
avisar.
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
RE_WT_ABIERTA = re.compile(r'<w:t(?:\s[^>]*)?>')


def texto(frag):
    return ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', frag, re.S))


def escapar(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def preservar(attrs, valor):
    """Anade xml:space=preserve SOLO si el valor lo necesita.

    La primera version lo anadia siempre, y eso dejo dos filas de cada tabla con un esqueleto
    XML distinto del resto —justo las que se reescribieron— sin ningun efecto visual, pero
    rompiendo la uniformidad estructural que una reconstruccion por plantilla aprovecha. Es
    inocuo —el documento ya trae 743 `<w:t>` con ese atributo de origen— y aun asi no hay razon
    para ponerlo en un valor como `+0.0789`, que no tiene espacios que preservar.
    """
    if 'xml:space' in (attrs or '') or valor == valor.strip():
        return attrs or ''
    return (attrs or '') + ' xml:space="preserve"'


def reescribir_celda(celda, valor):
    """Sustituye el contenido del unico <w:t> de la celda. Devuelve (celda, cambiada)."""
    m = re.search(r'<w:t(\s[^>]*)?>(.*?)</w:t>', celda, re.S)
    if m is None:
        return celda, False
    if m.group(2) == escapar(valor):
        return celda, False
    nuevo = '<w:t%s>%s</w:t>' % (preservar(m.group(1) or '', valor), escapar(valor))
    return celda[:m.start()] + nuevo + celda[m.end():], True


def aplicar(xml, reglas):
    informe, cambios_por_regla = [], {}
    nuevo = xml
    pendientes = []
    for r in reglas:
        marca, filas = r['tabla_contiene'], r['filas']
        cand = [m for m in RE_TBL.finditer(xml) if marca in texto(m.group(0))]
        if len(cand) != 1:
            informe.append((r['id'], 'la marca «%s» identifica %d tablas, no una'
                            % (marca, len(cand))))
            continue
        m = cand[0]
        trs = list(RE_TR.finditer(m.group(0)))[1:]          # sin la cabecera
        vistas, errores = set(), []
        for f in trs:
            celdas = RE_TC.findall(f.group(0))
            clave = texto(celdas[0]).strip() if celdas else ''
            if clave not in filas:
                errores.append('la fila «%s» de la tabla no esta en las reglas' % clave)
                continue
            vistas.add(clave)
            vals = filas[clave]
            if len(vals) != len(celdas) - 1:
                errores.append('«%s»: la tabla tiene %d celdas tras la primera y las reglas dan %d'
                               % (clave, len(celdas) - 1, len(vals)))
                continue
            for c in celdas[1:]:
                if len(RE_WT_ABIERTA.findall(c)) != 1:
                    errores.append('«%s»: una celda no tiene exactamente un <w:t>' % clave)
                    break
        sobran = sorted(set(filas) - vistas)
        if sobran:
            errores.append('%d regla(s) sin fila en la tabla: %s' % (len(sobran), sobran[:4]))
        if errores:
            informe.append((r['id'], ' · '.join(errores[:3])))
            continue
        pendientes.append((m.start(), m.group(0), trs, filas, r['id']))
        informe.append((r['id'], None))

    if any(err for _, err in informe):
        return xml, informe, cambios_por_regla

    for inicio, tbl, trs, filas, rid in sorted(pendientes, key=lambda x: -x[0]):
        tbl_nueva = tbl
        n = 0
        for f in sorted(trs, key=lambda x: -x.start()):
            fila = f.group(0)
            celdas = list(RE_TC.finditer(fila))
            clave = texto(celdas[0].group(0)).strip()
            vals = filas[clave]
            fila_nueva = fila
            for c, v in sorted(zip(celdas[1:], vals), key=lambda p: -p[0].start()):
                cel, cambiada = reescribir_celda(c.group(0), v)
                if cambiada:
                    n += 1
                    fila_nueva = fila_nueva[:c.start()] + cel + fila_nueva[c.end():]
            tbl_nueva = tbl_nueva[:f.start()] + fila_nueva + tbl_nueva[f.end():]
        cambios_por_regla[rid] = n
        nuevo = nuevo[:inicio] + tbl_nueva + nuevo[inicio + len(tbl):]
    return nuevo, informe, cambios_por_regla


def _respaldo_libre(ruta, sufijo):
    """Un respaldo no puede pisar otro; ver la nota de docx_borrar_filas.py."""
    cand, n = ruta + sufijo, 2
    while os.path.exists(cand):
        cand, n = '%s%s-%d' % (ruta, sufijo, n), n + 1
    return cand


def procesar(ruta, reglas, dry_run, sufijo):
    with zipfile.ZipFile(ruta) as z:
        partes = [(i, z.read(i.filename)) for i in z.infolist()]
    idx = next((k for k, (i, _) in enumerate(partes) if i.filename == 'word/document.xml'), None)
    if idx is None:
        return None, [('-', 'el paquete no trae word/document.xml')], {}
    xml = partes[idx][1].decode('utf-8')
    nuevo, informe, cambios = aplicar(xml, reglas)
    if any(err for _, err in informe) or dry_run:
        return None, informe, cambios
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
    return respaldo, informe, cambios


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
        if not os.path.exists(ruta):
            print('  no existe')
            malo = 1
            continue
        respaldo, informe, cambios = procesar(ruta, reglas, a.dry_run, sufijo)
        for rid, err in informe:
            if err:
                print('  %-4s ERROR: %s' % (rid, err))
                malo = 1
            else:
                # El recuento se calcula tambien en seco: `aplicar` construye el XML nuevo
                # y solo se omite la escritura. Decir «no se cuentan» era falso.
                print('  %-4s %d celda(s) que difieren%s'
                      % (rid, cambios.get(rid, 0),
                         ' (dry-run: no se escribe)' if a.dry_run else ', reescritas'))
        if respaldo:
            print('  respaldo: %s' % respaldo)
        if not any(err for _, err in informe):
            print('  todas las reglas cumplen las condiciones de seguridad')
    return malo


if __name__ == '__main__':
    sys.exit(main())
