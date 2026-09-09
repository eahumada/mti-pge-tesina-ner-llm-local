#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_replace_terms.py — Reemplazo quirúrgico de cadenas de texto dentro de archivos .docx
sin regenerar el documento (NO usa pandoc, NO usa python-docx, sólo stdlib).

Motivación
----------
El .docx de la tesina contiene correcciones manuales (numeración multinivel numId=0,
estilos de fila de tabla, saltos de página) que se perderían si el documento se
regenerara desde el Markdown. Esta herramienta abre el paquete OOXML como ZIP,
edita únicamente el texto visible dentro de los elementos <w:t> de las partes XML
seleccionadas, y reescribe el ZIP conservando:

  * la lista y el ORDEN exacto de las partes del paquete,
  * el método de compresión, fecha, atributos externos y comentario de cada entrada,
  * todas las partes no modificadas byte a byte,
  * todo el marcado XML de las partes modificadas (estilos, rPr, bookmarks, tablas...).

Fragmentación de runs
---------------------
Word suele partir una frase entre varios <w:r>/<w:t> (por revisiones, corrector
ortográfico, rPr distintos...). La herramienta aplica dos estrategias, en orden:

  1) INTRA-RUN: la ocurrencia cabe completa dentro de un único <w:t>. Se reemplaza
     el texto de ese <w:t>. Es el caso seguro y el más frecuente.
  2) CROSS-RUN: la ocurrencia se busca sobre el texto concatenado de cada párrafo
     <w:p>. Si se encuentra a caballo entre varios <w:t>, el texto de reemplazo se
     escribe completo en el PRIMER <w:t> implicado (que hereda su formato) y se
     recorta el fragmento consumido de los <w:t> siguientes. El resto del párrafo
     (rPr, bookmarks, <w:br/>, <w:tab/>, campos...) queda intacto.

Si tras ambas estrategias una regla no alcanza sus ocurrencias esperadas, se
reporta EXPLÍCITAMENTE como no reemplazada; nunca se "adivina".

Uso
---
  # Vista previa (no escribe nada):
  python3 tools/docx_replace_terms.py --rules tools/terms_ablacion.json --dry-run ARCHIVO.docx ...

  # Aplicar in situ creando respaldo .bak_AAAAMMDD-HHMMSS junto al original:
  python3 tools/docx_replace_terms.py --rules tools/terms_ablacion.json --in-place ARCHIVO.docx ...

  # Aplicar escribiendo la salida en otro directorio (los originales no se tocan):
  python3 tools/docx_replace_terms.py --rules tools/terms_ablacion.json --out-dir DIR ARCHIVO.docx ...

Formato del archivo de reglas (JSON, UTF-8)
-------------------------------------------
{
  "parts": ["word/document.xml", "word/footnotes.xml", ...],   # opcional; por defecto
                                                               # document.xml + footnotes/endnotes + headers/footers
  "rules": [
    {"id": "R1", "find": "texto viejo", "replace": "texto nuevo",
     "expect": 1,          # opcional: nº exacto de ocurrencias esperadas
     "optional": true}     # opcional: permite 0 ocurrencias sin marcar error
  ]
}

Reglas: se aplican EN ORDEN. Poner primero las reglas cuyo "find" contenga al de otra.
"""

from __future__ import print_function

import argparse
import datetime
import json
import os
import re
import shutil
import sys
import zipfile

# --------------------------------------------------------------------------- #
# Constantes
# --------------------------------------------------------------------------- #

DEFAULT_PART_PATTERNS = [
    re.compile(r"^word/document\d*\.xml$"),
    re.compile(r"^word/footnotes\.xml$"),
    re.compile(r"^word/endnotes\.xml$"),
    re.compile(r"^word/header\d*\.xml$"),
    re.compile(r"^word/footer\d*\.xml$"),
]

# <w:t ...>contenido</w:t>  (también soporta <w:t/> vacío, que se ignora)
RE_WT = re.compile(r"<w:t(\s[^>]*?)?>(.*?)</w:t>", re.DOTALL)
# <w:p ...> ... </w:p>  (los <w:p> no anidan en WordprocessingML de nivel de párrafo,
# salvo dentro de celdas de tabla, donde el no-greedy corta correctamente en el
# primer </w:p>; eso es exactamente lo que queremos: párrafos "hoja")
RE_WP = re.compile(r"<w:p(?:\s[^>]*?)?>.*?</w:p>", re.DOTALL)


# --------------------------------------------------------------------------- #
# Utilidades XML
# --------------------------------------------------------------------------- #

def xml_unescape(s):
    return (s.replace("&lt;", "<")
             .replace("&gt;", ">")
             .replace("&quot;", '"')
             .replace("&apos;", "'")
             .replace("&amp;", "&"))


def xml_escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;"))


def ensure_preserve(attrs):
    """Garantiza xml:space='preserve' en los atributos de <w:t>."""
    attrs = attrs or ""
    if "xml:space" in attrs:
        return attrs
    return attrs + ' xml:space="preserve"'


# --------------------------------------------------------------------------- #
# Estrategia 1: reemplazo dentro de un único <w:t>
# --------------------------------------------------------------------------- #

def replace_intra_run(xml, find, repl):
    """Reemplaza `find` por `repl` cuando cabe completo dentro de un <w:t>.

    Devuelve (xml_nuevo, n_reemplazos).
    """
    counter = {"n": 0}
    find_esc_needed = find

    def _sub(m):
        attrs, body = m.group(1), m.group(2)
        text = xml_unescape(body)
        if find_esc_needed not in text:
            return m.group(0)
        n = text.count(find_esc_needed)
        counter["n"] += n
        new_text = text.replace(find_esc_needed, repl)
        return "<w:t%s>%s</w:t>" % (ensure_preserve(attrs), xml_escape(new_text))

    new_xml = RE_WT.sub(_sub, xml)
    return new_xml, counter["n"]


# --------------------------------------------------------------------------- #
# Estrategia 0: celda de tabla completa (opcional, por regla)
# --------------------------------------------------------------------------- #

def replace_whole_cell(xml, find, repl):
    """Reemplaza sólo los <w:t> cuyo contenido ENTERO es `find`.

    Para qué. Una celda de tabla que vale `5.33` no se puede corregir con una búsqueda de
    subcadena: el 2026-09-09 el mismo documento tenía dos celdas `5.33` y, en otra tabla, un
    `35.33%` que una regla de `5.33` habría convertido en `35.80%`. Es la misma clase de trampa
    que `<w:t[^>]*>` encajando con `<w:tcPr>`: el ancla parece específica y no lo es.

    Con esta estrategia el ancla es la celda, no el texto, y `35.33%` queda fuera por
    construcción. No se intenta cross-run: una celda numérica es un único run, y si no lo es la
    regla devuelve cero y se reporta como no alcanzada, que es la conducta correcta.

    Se conserva el espaciado original de la celda, por si el estilo dependiera de él.
    """
    counter = {"n": 0}

    def _sub(m):
        attrs, body = m.group(1), m.group(2)
        text = xml_unescape(body)
        if text.strip() != find:
            return m.group(0)
        counter["n"] += 1
        izq = text[:len(text) - len(text.lstrip())]
        der = text[len(text.rstrip()):]
        return "<w:t%s>%s</w:t>" % (ensure_preserve(attrs), xml_escape(izq + repl + der))

    return RE_WT.sub(_sub, xml), counter["n"]


# --------------------------------------------------------------------------- #
# Estrategia 2: reemplazo a caballo entre varios <w:t> del mismo párrafo
# --------------------------------------------------------------------------- #

def _rewrite_paragraph_cross_run(para_xml, find, repl):
    """Intenta reemplazar `find` en el texto concatenado del párrafo.

    Devuelve (nuevo_para_xml, n_reemplazos).
    """
    nodes = []  # (span_ini, span_fin, attrs, texto_plano)
    for m in RE_WT.finditer(para_xml):
        nodes.append([m.start(), m.end(), m.group(1), xml_unescape(m.group(2))])
    if len(nodes) < 2:
        return para_xml, 0

    concat = "".join(n[3] for n in nodes)
    if find not in concat:
        return para_xml, 0

    # Mapa: índice global -> (idx_nodo, offset_local)
    bounds = []  # (inicio_global, idx_nodo)
    acc = 0
    for i, n in enumerate(nodes):
        bounds.append((acc, i))
        acc += len(n[3])

    def locate(gidx):
        lo, hi = 0, len(bounds) - 1
        best = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if bounds[mid][0] <= gidx:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        start_g, node_i = bounds[best]
        return node_i, gidx - start_g

    n_done = 0
    # Reemplazar de derecha a izquierda para no invalidar los offsets ya calculados.
    positions = []
    pos = concat.find(find)
    while pos != -1:
        positions.append(pos)
        pos = concat.find(find, pos + len(find))

    texts = [n[3] for n in nodes]
    for pos in reversed(positions):
        i_start, off_start = locate(pos)
        i_end, off_end = locate(pos + len(find) - 1)
        off_end += 1  # exclusivo
        if i_start == i_end:
            # Cabía en un solo nodo (ya lo habría cogido la estrategia 1, pero
            # puede darse si la estrategia 1 no se ejecutó); se trata igual.
            texts[i_start] = texts[i_start][:off_start] + repl + texts[i_start][off_end:]
        else:
            texts[i_start] = texts[i_start][:off_start] + repl
            for k in range(i_start + 1, i_end):
                texts[k] = ""
            texts[i_end] = texts[i_end][off_end:]
        n_done += 1

    if n_done == 0:
        return para_xml, 0

    # Reconstruir el párrafo preservando todo lo que no sea <w:t>
    out = []
    cursor = 0
    for i, n in enumerate(nodes):
        s, e, attrs, old = n
        out.append(para_xml[cursor:s])
        out.append("<w:t%s>%s</w:t>" % (ensure_preserve(attrs), xml_escape(texts[i])))
        cursor = e
    out.append(para_xml[cursor:])
    return "".join(out), n_done


def diagnose_near_miss(xml, find):
    """Explica por qué una regla no encontró coincidencias.

    Reintenta la búsqueda sobre el texto visible del documento con los espacios
    "flexibilizados" (espacio duro U+00A0, espacio fino, tabuladores, saltos de
    línea) — la causa más habitual de un fallo silencioso en documentos que
    pasaron por Word — y devuelve el fragmento real hallado, si lo hay.
    """
    plain = "".join(xml_unescape(m.group(2)) for m in RE_WT.finditer(xml))
    flexible = r"[\s\u00a0\u202f\u2009]+".join(
        re.escape(tok) for tok in re.split(r"[\s\u00a0\u202f\u2009]+", find) if tok)
    m = re.search(flexible, plain)
    if m:
        return ("coincide con espacios flexibles; el documento contiene "
                "caracteres invisibles distintos: %r" % (m.group(0),))
    # ¿Existe al menos un prefijo reconocible?
    for cut in (60, 40, 25, 15):
        if len(find) > cut and find[:cut] in plain:
            return "sólo coincide el prefijo %r; el texto diverge después" % find[:cut]
    return "el texto no aparece en las partes analizadas"


def replace_cross_run(xml, find, repl):
    counter = {"n": 0}

    def _sub(m):
        new_para, n = _rewrite_paragraph_cross_run(m.group(0), find, repl)
        counter["n"] += n
        return new_para

    new_xml = RE_WP.sub(_sub, xml)
    return new_xml, counter["n"]


# --------------------------------------------------------------------------- #
# Aplicación de reglas sobre una parte XML
# --------------------------------------------------------------------------- #

def apply_rules_to_xml(xml, rules):
    """Aplica la lista de reglas. Devuelve (xml_nuevo, stats_por_regla)."""
    stats = []
    for rule in rules:
        find = rule["find"]
        repl = rule["replace"]
        if rule.get("celda_exacta"):
            # el ancla es la celda entera; ver replace_whole_cell
            xml, n_intra = replace_whole_cell(xml, find, repl)
            n_cross = 0
        else:
            xml, n_intra = replace_intra_run(xml, find, repl)
            xml, n_cross = replace_cross_run(xml, find, repl)
        stats.append({"id": rule.get("id", find[:30]), "intra": n_intra, "cross": n_cross})
    return xml, stats


# --------------------------------------------------------------------------- #
# Nivel paquete .docx
# --------------------------------------------------------------------------- #

def select_parts(names, explicit):
    if explicit:
        return [n for n in names if n in set(explicit)]
    out = []
    for n in names:
        for pat in DEFAULT_PART_PATTERNS:
            if pat.match(n):
                out.append(n)
                break
    return out


def process_docx(src, dst, rules, parts=None, dry_run=False, verbose=True):
    """Procesa un .docx. Devuelve un dict con el informe."""
    zin = zipfile.ZipFile(src, "r")
    infos = zin.infolist()
    names = [i.filename for i in infos]
    targets = select_parts(names, parts)

    report = {
        "src": src,
        "dst": dst,
        "src_size": os.path.getsize(src),
        "parts_in": len(names),
        "parts_scanned": targets,
        "rules": {},          # id -> {"intra": n, "cross": n}
        "unmatched": [],
        "modified_parts": [],
    }
    for r in rules:
        report["rules"][r.get("id", r["find"][:30])] = {"intra": 0, "cross": 0}

    new_data = {}
    scanned_xml = []
    for part in targets:
        raw = zin.read(part)
        try:
            xml = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned_xml.append(xml)
        out_xml, stats = apply_rules_to_xml(xml, rules)
        for s in stats:
            report["rules"][s["id"]]["intra"] += s["intra"]
            report["rules"][s["id"]]["cross"] += s["cross"]
        if out_xml != xml:
            new_data[part] = out_xml.encode("utf-8")
            report["modified_parts"].append(part)

    # Verificación de expectativas
    for r in rules:
        rid = r.get("id", r["find"][:30])
        total = report["rules"][rid]["intra"] + report["rules"][rid]["cross"]
        expect = r.get("expect")
        optional = r.get("optional", False)
        if total == 0 and not optional:
            why = diagnose_near_miss("".join(scanned_xml), r["find"])
            report["unmatched"].append((rid, "0 ocurrencias encontradas — %s" % why))
        elif expect is not None and total != expect and not (optional and total == 0):
            report["unmatched"].append((rid, "esperadas %s, encontradas %d" % (expect, total)))

    if dry_run:
        zin.close()
        report["dst_size"] = None
        report["parts_out"] = len(names)
        return report

    # Reescritura del ZIP preservando orden, compresión y metadatos por entrada.
    dst_dir = os.path.dirname(os.path.abspath(dst))
    if dst_dir and not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    tmp = dst + ".tmp_write"
    zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    try:
        for info in infos:
            data = new_data.get(info.filename)
            if data is None:
                data = zin.read(info.filename)
            ni = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            ni.compress_type = info.compress_type
            ni.external_attr = info.external_attr
            ni.internal_attr = info.internal_attr
            ni.create_system = info.create_system
            ni.comment = info.comment
            ni.extra = info.extra
            zout.writestr(ni, data)
            # zipfile fuerza external_attr=0o600<<16 y create_version=20 cuando el
            # original traía 0. Esos dos campos viven SÓLO en el directorio central,
            # así que se pueden restaurar sin desincronizar la cabecera local.
            written = zout.filelist[-1]
            written.external_attr = info.external_attr
            written.create_version = info.create_version
        zout.comment = zin.comment
    finally:
        zout.close()
        zin.close()

    shutil.move(tmp, dst)

    report["dst_size"] = os.path.getsize(dst)
    zchk = zipfile.ZipFile(dst, "r")
    report["parts_out"] = len(zchk.namelist())
    report["testzip"] = zchk.testzip()  # None == todos los CRC correctos
    zchk.close()
    return report


def validate_docx(path):
    """Validación estructural mínima de un paquete OOXML .docx."""
    issues = []
    try:
        z = zipfile.ZipFile(path, "r")
    except Exception as exc:  # noqa: BLE001
        return ["no es un ZIP válido: %s" % exc], []
    names = z.namelist()
    bad = z.testzip()
    if bad is not None:
        issues.append("CRC inválido en %s" % bad)
    for required in ("[Content_Types].xml", "_rels/.rels", "word/document.xml"):
        if required not in names:
            issues.append("falta la parte obligatoria %s" % required)
    # XML bien formado en todas las partes XML
    from xml.etree import ElementTree as ET
    for n in names:
        if n.endswith(".xml") or n.endswith(".rels"):
            try:
                ET.fromstring(z.read(n))
            except Exception as exc:  # noqa: BLE001
                issues.append("XML mal formado en %s: %s" % (n, exc))
    z.close()
    return issues, names


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", nargs="+", help="archivos .docx a procesar")
    ap.add_argument("--rules", required=True, help="archivo JSON de reglas")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="sólo informa, no escribe")
    g.add_argument("--in-place", action="store_true",
                   help="modifica el original creando respaldo .bak_AAAAMMDD-HHMMSS")
    g.add_argument("--out-dir", help="escribe los resultados en este directorio")
    ap.add_argument("--no-backup", action="store_true",
                    help="con --in-place, no crear respaldo (desaconsejado)")
    args = ap.parse_args(argv)

    with open(args.rules, "rb") as fh:
        cfg = json.loads(fh.read().decode("utf-8"))
    rules = cfg["rules"]
    parts = cfg.get("parts")

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    exit_code = 0

    for src in args.docx:
        if not os.path.isfile(src):
            print("ERROR: no existe %s" % src)
            exit_code = 2
            continue

        if args.dry_run:
            dst = None
        elif args.in_place:
            dst = src
            if not args.no_backup:
                bak = "%s.bak_%s" % (src, stamp)
                shutil.copy2(src, bak)
                print("respaldo: %s" % bak)
        else:
            dst = os.path.join(args.out_dir, os.path.basename(src))

        rep = process_docx(src, dst if dst else src, rules, parts=parts,
                           dry_run=args.dry_run)

        print("=" * 78)
        print("ARCHIVO : %s" % src)
        if not args.dry_run:
            print("SALIDA  : %s" % dst)
        print("partes ZIP: %d -> %d %s" % (
            rep["parts_in"], rep["parts_out"],
            "OK" if rep["parts_in"] == rep["parts_out"] else "*** DIFERENTE ***"))
        if rep.get("dst_size"):
            print("tamaño    : %d -> %d bytes (%+d)" % (
                rep["src_size"], rep["dst_size"], rep["dst_size"] - rep["src_size"]))
        else:
            print("tamaño    : %d bytes (dry-run)" % rep["src_size"])
        total = 0
        for rid, st in rep["rules"].items():
            n = st["intra"] + st["cross"]
            total += n
            flag = ""
            if st["cross"]:
                flag = "  <-- %d reparada(s) por fragmentación de runs" % st["cross"]
            print("  %-6s %d reemplazo(s) [intra-run=%d, cross-run=%d]%s"
                  % (rid, n, st["intra"], st["cross"], flag))
        print("TOTAL reemplazos: %d" % total)
        if rep["modified_parts"]:
            print("partes modificadas: %s" % ", ".join(rep["modified_parts"]))
        if rep["unmatched"]:
            exit_code = 1
            print("*** REGLAS SIN REEMPLAZAR (revisar manualmente) ***")
            for rid, why in rep["unmatched"]:
                print("    - %s: %s" % (rid, why))
        else:
            print("todas las reglas aplicadas segun lo esperado")

        if not args.dry_run:
            issues, names = validate_docx(dst)
            if issues:
                exit_code = 1
                print("*** VALIDACION OOXML FALLIDA ***")
                for i in issues:
                    print("    - %s" % i)
            else:
                print("validacion OOXML: OK (%d partes, XML bien formado, CRC correcto)"
                      % len(names))

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
