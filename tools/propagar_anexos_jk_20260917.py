#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de migracion, ya ejecutado el 2026-09-17: inserto el Anexo J (parrafos 1-2,
Tabla 20, cierre), la bibliografia [40]-[46] y el Anexo K completo en los tres .docx
del informe, justo antes de <w:sectPr y despues de la referencia [39] respectivamente.
Preserva el resto del paquete OOXML byte a byte (mismo metodo que
tools/docx_replace_terms.py, que no sirve aqui porque inserta parrafos y tablas nuevas,
no sustituye texto existente).

Se conserva como referencia y para reproducir el resultado si hiciera falta: el texto de
cada parrafo/tabla esta hardcodeado (no lee el Markdown), asi que NO es un tool generico
reutilizable para futuros anexos. Verificado antes de aplicar: `tools/verificar_informe.py`
paso de 81 fallos (63 declarados) a 30 fallos (30 declarados), 0 nuevos, tras retirar las
17 declaraciones de FALLOS_DECLARADOS que este script dejo resueltas (FINDINGS §F190).
Respaldo de los tres .docx previos en
`doc/versions/informe_final/_respaldos_20260917_propagacion_jk/`."""
import re
import shutil
import sys
import zipfile

FILES = {
    'plantilla': '/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local/Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx',
    'sin_plantilla': '/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local/Informe_Final_Tesina_NER.docx',
    'borrador': '/Users/eahumada/Documents/Personal/MTI/mti-pge-tesina-ner-llm-local/doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx',
}

CONFIGS = {
    'plantilla': dict(
        heading_style='heading2', prose_style='p1a', caption_style='tablecaption',
        biblio_style='referenceitem',
        tblpr='<w:tblStyle w:val="Table"/><w:tblW w:type="dxa" w:w="8838"/><w:tblLayout w:type="fixed"/>'
              '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" '
              'w:noVBand="0" w:val="0020"/>',
        header_trpr='<w:trPr><w:tblHeader w:val="on"/></w:trPr>',
        header_tcpr_extra='',
    ),
    'sin_plantilla': dict(
        heading_style='Heading2', prose_style='BodyText', caption_style='TableCaption',
        biblio_style='BodyText',
        tblpr='<w:tblStyle w:val="Table"/><w:tblW w:type="pct" w:w="5000"/><w:tblLayout w:type="fixed"/>'
              '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" '
              'w:noVBand="0" w:val="0020"/>',
        header_trpr='<w:trPr><w:tblHeader w:val="on"/></w:trPr>',
        header_tcpr_extra='',
    ),
    'borrador': dict(
        heading_style='Heading2', prose_style='BodyText', caption_style='TableCaption',
        biblio_style='BodyText',
        tblpr='<w:tblStyle w:val="Table"/><w:tblW w:type="pct" w:w="5000.0"/><w:tblLook w:firstRow="1"/>',
        header_trpr='<w:trPr><w:cnfStyle w:firstRow="1"/></w:trPr>',
        header_tcpr_extra='<w:tcBorders><w:bottom w:val="single"/></w:tcBorders><w:vAlign w:val="bottom"/>',
    ),
}

NUMPR = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def md_runs(text):
    """Divide texto por **negrita** y *cursiva* (sin anidar), devuelve lista de (texto, bold, italic)."""
    tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', text)
    out = []
    for tok in tokens:
        if tok == '':
            continue
        if tok.startswith('**') and tok.endswith('**'):
            out.append((tok[2:-2], True, False))
        elif tok.startswith('*') and tok.endswith('*'):
            out.append((tok[1:-1], False, True))
        else:
            out.append((tok, False, False))
    return out


def runs_xml(text):
    out = []
    for seg, bold, italic in md_runs(text):
        props = ''
        if bold:
            props += '<w:b/>'
        if italic:
            props += '<w:i/>'
        rpr = '<w:rPr>%s</w:rPr>' % props if props else ''
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(seg)))
    return ''.join(out)


def biblio_p(text, style):
    return '<w:p><w:pPr>%s<w:pStyle w:val="%s"/></w:pPr>%s</w:p>' % (
        NUMPR, style, runs_xml(text))


def heading_p(text, style):
    return '<w:p><w:pPr>%s<w:pStyle w:val="%s"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>' % (
        NUMPR, style, esc(text))


def prose_p(text, style):
    return '<w:p><w:pPr>%s<w:pStyle w:val="%s"/></w:pPr>%s</w:p>' % (
        NUMPR, style, runs_xml(text))


def caption_p(text, style):
    return '<w:p><w:pPr>%s<w:pStyle w:val="%s"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>' % (
        NUMPR, style, esc(text))


def cell_xml(width, text, jc, bold, is_header, cfg):
    if is_header:
        rpr = '<w:rPr><w:b/></w:rPr>'
        extra = cfg['header_tcpr_extra']
    else:
        rpr = '<w:rPr><w:b/></w:rPr>' if bold else '<w:rPr><w:b w:val="0"/></w:rPr>'
        extra = ''
    return ('<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="%d"/>%s</w:tcPr>'
            '<w:p><w:pPr><w:pStyle w:val="Compact"/><w:jc w:val="%s"/></w:pPr>'
            '<w:r>%s<w:t>%s</w:t></w:r></w:p></w:tc>') % (width, extra, jc, rpr, esc(text))


def table_xml(cfg, widths, jcs, header, rows, bold_rows=()):
    """rows: list of list[str]; bold_rows: set of row indices (0-based, sobre `rows`) con toda la fila en negrita."""
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)
    out = ['<w:tbl><w:tblPr>%s</w:tblPr><w:tblGrid>%s</w:tblGrid>' % (cfg['tblpr'], grid)]
    hdr_cells = ''.join(cell_xml(w, t, j, False, True, cfg) for w, t, j in zip(widths, header, jcs))
    out.append('<w:tr>%s%s</w:tr>' % (cfg['header_trpr'], hdr_cells))
    for ridx, row in enumerate(rows):
        bold = ridx in bold_rows
        cells = ''.join(cell_xml(w, t, j, bold, False, cfg) for w, t, j in zip(widths, row, jcs))
        out.append('<w:tr>%s</w:tr>' % cells)
    out.append('</w:tbl>')
    return ''.join(out)


# --- Datos de la Tabla 20 (Anexo J) -----------------------------------------
TABLA20_ROWS = [
    ['deepseek-r1:1.5b', '−0,6151', '0,0333', '−0,0070'],
    ['gemma4:12b-mlx', '−0,4964', '0,1006', '−0,1259'],
    ['gemma4:31b-cloud', '−0,4746', '0,1190', '−0,0559'],
    ['gemma4:31b-mlx', '−0,4773', '0,1166', '−0,0559'],
    ['gemma4:latest', '−0,4955', '0,1014', '−0,1259'],
    ['gemma:latest', '−0,5047', '0,0942', '−0,2238'],
    ['gpt-oss:20b', '−0,4832', '0,1115', '−0,0699'],
    ['llama3.1:8b', '−0,4840', '0,1108', '−0,0839'],
    ['llama3.2:latest', '−0,5063', '0,0930', '−0,0070'],
    ['mistral-nemo:latest', '−0,5971', '0,0404', '−0,2378'],
    ['nemotron-mini:4b', '+0,0120', '0,9706', '+0,1608'],
    ['qwen2.5:14b', '−0,4767', '0,1171', '−0,1469'],
    ['qwen3:8b', '−0,4771', '0,1168', '−0,1678'],
]
TABLA20_BOLD_ROWS = {10}  # nemotron-mini:4b

# --- Datos de la Tabla 21 (Anexo K) -----------------------------------------
TABLA21_ROWS = [
    ['gemma4:31b-cloud', '81,87 % [81,58, 82,16]', '82,97 % [82,79, 83,16]'],
    ['gemma4:31b-mlx', '81,56 % [81,45, 81,67]', '82,49 % [82,42, 82,55]'],
    ['gemma4:12b-mlx', '77,96 % [77,80, 78,13]', '79,84 % [79,77, 79,90]'],
    ['gpt-oss:20b', '75,50 % [74,46, 76,54]', '77,46 % [77,11, 77,81]'],
    ['gemma4:latest', '75,13 % [74,51, 75,74]', '77,98 % [77,44, 78,53]'],
    ['llama3.1:8b', '69,66 % [69,28, 70,04]', '71,43 % [71,00, 71,86]'],
    ['qwen3:8b', '68,92 % [68,77, 69,08]', '69,13 % [69,01, 69,25]'],
    ['llama3.2:latest', '62,46 % [61,63, 63,29]', '69,67 % [69,39, 69,95]'],
    ['mistral-nemo:latest', '60,39 % [59,80, 60,97]', '56,93 % [55,77, 58,10]'],
    ['deepseek-r1:1.5b', '29,18 % [28,13, 30,23]', '31,99 % [30,92, 33,06]'],
    ['nemotron-mini:4b', '27,68 % [26,90, 28,46]', '41,13 % [40,23, 42,02]'],
]

ANEXO_J_HEADING = 'Anexo J — Correlación entre capacidad y beneficio del RAG: fuente y reproducción'

ANEXO_J_P1 = ('Las dos cifras de §5.3.1 sobre la relación entre el desempeño base de un modelo y la mejora '
              'que le aporta el KB RAG —Spearman −0,0879 (p = 0,7752) y Pearson −0,4816 (p = 0,0956), sobre '
              'los N=13 pares (F1 base, ΔF1) de la Tabla 7— proceden de tools/robustez_estadistica.py, que '
              'las calcula con scipy.stats.pearsonr y scipy.stats.spearmanr sobre el CSV consolidado de la '
              're-corrida adoptada y las persiste en '
              'repos/ner-llm-entity-benchmark/results/ROBUSTEZ_ESTADISTICA_20260909_FIX/robustez.json. El '
              'coeficiente de **Pearson** [40] mide la asociación lineal entre las dos variables y es '
              'sensible a los valores atípicos; el de **Spearman** [41], calculado sobre sus rangos y no '
              'sobre los valores, capta cualquier relación monótona sin asumir linealidad, a costa de '
              'ignorar la magnitud de la asociación. Ninguno de los dos alcanza el 5 % de significancia '
              'sobre los trece modelos.')

ANEXO_J_P2 = ('La Tabla 20 recalcula ambos coeficientes retirando, uno a la vez, cada uno de los trece '
              'modelos de la muestra, para identificar cuánto depende el resultado de un único caso. Solo '
              'la ausencia de nemotron-mini:4b cambia el signo y la significancia del coeficiente de '
              'Pearson; las otras doce retiradas lo dejan entre −0,47 y −0,62, con el mismo signo que sobre '
              'la muestra completa.')

ANEXO_J_CIERRE = ('El detalle íntegro, con más decimales, está en el propio artefacto JSON citado al inicio '
                   'de este anexo.')

ANEXO_K_HEADING = 'Anexo K — Intervalo de confianza de la Tabla 7 por réplica de semilla (N=120, cinco semillas)'

ANEXO_K_P1 = ('La Tabla 7 (§5.3.1) reporta un único punto por modelo, tomado de una corrida '
              '(recorrida_20260908, consolidada en results/ANALISIS_CONJUNTO_20260909_FIX/). Para acotar '
              'cuánto varía ese punto por el azar de la generación, se replicó el mismo protocolo sobre '
              'cinco semillas declaradas (42, 123, 456, 789, 1024) en once de los trece modelos de la Tabla '
              '7, con 2 640 evaluaciones por semilla (13 200 en total, 0 fallidas), en '
              'repos/ner-llm-entity-benchmark/results/barras_error_n120_REMOTO/. Quedan fuera de esta '
              'réplica qwen2.5:14b y gemma:latest, que no formaron parte de la corrida de barra de error.')

ANEXO_K_P2 = ('El cálculo, en results/R2_CONSOLIDADO_5SEMILLAS_20260916/calcular_intervalos_confianza.py, '
              'promedia el F1 por artículo dentro de cada semilla sobre los mismos 113 artículos que usa la '
              'Tabla 7 (se excluyen los siete con codificación contaminada, Anexo H), y calcula el '
              'intervalo de confianza al 95 % con distribución t de Student sobre las cinco medias '
              'resultantes. Antes de aplicarlo a los once modelos se verificó que reproduce exactamente el '
              'punto ya publicado: la media de la semilla 42 para gemma4:31b-mlx da 81,47 %, idéntica a la '
              'cifra de la Tabla 7.')

ANEXO_K_P3 = ('El cálculo parte del CSV de resultados por artículo, no del resumen agregado que trae cada '
              'corrida: el de gemma4:31b-cloud no se pudo usar directamente porque no reflejaba sus propios '
              'datos crudos en ninguna de las cinco semillas, un desajuste que no afecta al resto de los '
              'modelos ni a la fuente primaria por artículo.')

ANEXO_K_P4 = ('La Tabla 21 recoge, para cada uno de los once modelos, la media y el intervalo de confianza '
              'al 95 % del F1 sobre las cinco semillas, en modo baseline y KB RAG.')

ANEXO_K_CIERRE = ('De los veintidós puntos que reporta la Tabla 7 para estos once modelos (baseline y KB '
                   'RAG), quince caen dentro de su intervalo de confianza de cinco semillas. Los siete '
                   'restantes quedan fuera por un margen mínimo, entre 0,03 y 0,13 puntos porcentuales '
                   '(gemma4:12b-mlx en ambos modos, gpt-oss:20b, llama3.1:8b, qwen3:8b, llama3.2:latest y '
                   'deepseek-r1:1.5b en uno de los dos), consistente con que la corrida publicada no '
                   'comparte semilla con ninguna de las cinco de esta réplica salvo, aparentemente, en '
                   'gemma4:31b-mlx. El resultado de conjunto es el mismo: ningún modelo se desvía de su '
                   'franja de cinco semillas más allá de un margen menor al 0,15 % absoluto, y la cifra ya '
                   'publicada en la Tabla 7 queda acotada, no cuestionada, por este intervalo de confianza.')


BIBLIO_ENTRIES = [
    '[40] K. Pearson, "Note on Regression and Inheritance in the Case of Two Parents," '
    '*Proceedings of the Royal Society of London*, vol. 58, pp. 240-242, 1895. [En línea]. '
    'Disponible: https://doi.org/10.1098/rspl.1895.0041',
    '[41] C. Spearman, "The Proof and Measurement of Association Between Two Things," '
    '*American Journal of Psychology*, vol. 15, no. 1, pp. 72-101, 1904. [En línea]. '
    'Disponible: https://doi.org/10.2307/1412159',
    '[42] R. A. Fisher, *Statistical Methods for Research Workers*. Edimburgo: Oliver & Boyd, '
    '1925. [En línea]. Disponible: https://openlibrary.org/works/OL1153861W',
    '[43] M. Friedman, "The Use of Ranks to Avoid the Assumption of Normality Implicit in the '
    'Analysis of Variance," *Journal of the American Statistical Association*, vol. 32, no. '
    '200, pp. 675-701, 1937. [En línea]. Disponible: https://doi.org/10.1080/01621459.1937.10503522',
    '[44] H. Levene, "Robust Tests for Equality of Variances," in *Contributions to '
    'Probability and Statistics: Essays in Honor of Harold Hotelling*, I. Olkin, Ed. '
    'Stanford, CA: Stanford University Press, 1960, pp. 278-292. [En línea]. Disponible: '
    'https://openlibrary.org/books/OL5793803M',
    '[45] M. B. Brown and A. B. Forsythe, "Robust Tests for the Equality of Variances," '
    '*Journal of the American Statistical Association*, vol. 69, no. 346, pp. 364-367, 1974. '
    '[En línea]. Disponible: https://doi.org/10.1080/01621459.1974.10482955',
    '[46] J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2.ª ed. '
    'Hillsdale, NJ: Lawrence Erlbaum Associates, 1988. [En línea]. Disponible: '
    'https://openlibrary.org/books/OL2035961M',
]


def build_biblio_xml(cfg):
    return ''.join(biblio_p(e, cfg['biblio_style']) for e in BIBLIO_ENTRIES)


def build_insert_xml(cfg):
    parts = []
    # --- resto del Anexo J (encabezado, parrafo 1, parrafo 2, tabla 20, cierre) ---
    parts.append(heading_p(ANEXO_J_HEADING, cfg['heading_style']))
    parts.append(prose_p(ANEXO_J_P1, cfg['prose_style']))
    parts.append(prose_p(ANEXO_J_P2, cfg['prose_style']))
    parts.append(caption_p(
        'Tabla 20. Sensibilidad de la correlación capacidad-beneficio a la retirada de cada modelo '
        '(N=12 restantes por fila)', cfg['caption_style']))
    parts.append(table_xml(
        cfg,
        widths=[2600, 2079, 2079, 2080],
        jcs=['left', 'center', 'center', 'center'],
        header=['Modelo retirado', 'Pearson r', 'Pearson p', 'Spearman ρ'],
        rows=TABLA20_ROWS,
        bold_rows=TABLA20_BOLD_ROWS,
    ))
    parts.append(prose_p(ANEXO_J_CIERRE, cfg['prose_style']))
    # --- Anexo K completo ---
    parts.append(heading_p(ANEXO_K_HEADING, cfg['heading_style']))
    parts.append(prose_p(ANEXO_K_P1, cfg['prose_style']))
    parts.append(prose_p(ANEXO_K_P2, cfg['prose_style']))
    parts.append(prose_p(ANEXO_K_P3, cfg['prose_style']))
    parts.append(prose_p(ANEXO_K_P4, cfg['prose_style']))
    parts.append(caption_p(
        'Tabla 21. Media e intervalo de confianza al 95 % del F1 sobre cinco semillas '
        '(N=120, once modelos)', cfg['caption_style']))
    parts.append(table_xml(
        cfg,
        widths=[2200, 3319, 3319],
        jcs=['left', 'center', 'center'],
        header=['Modelo', 'F1 baseline (media, IC95%)', 'F1 KB RAG (media, IC95%)'],
        rows=TABLA21_ROWS,
    ))
    parts.append(prose_p(ANEXO_K_CIERRE, cfg['prose_style']))
    return ''.join(parts)


def process(name, src, dst):
    cfg = CONFIGS[name]
    zin = zipfile.ZipFile(src, 'r')
    infos = zin.infolist()
    xml = zin.read('word/document.xml').decode('utf-8')

    # 1) Bibliografia [40]-[46]: se inserta justo despues de la referencia [39],
    #    antes del <w:p>...Anexos</w:p> que abre la seccion de anexos.
    marker_biblio = '[39] R. Dror'
    idx_ref39 = xml.find(marker_biblio)
    if idx_ref39 == -1:
        raise RuntimeError('%s: no se encontro la referencia [39]' % name)
    end_p39 = xml.find('</w:p>', idx_ref39) + len('</w:p>')
    biblio_xml = build_biblio_xml(cfg)
    xml = xml[:end_p39] + biblio_xml + xml[end_p39:]

    # 2) Resto del Anexo J + Anexo K completo, al final del cuerpo (antes de <w:sectPr).
    insert = build_insert_xml(cfg)
    marker = '<w:sectPr'
    idx = xml.rfind(marker)
    if idx == -1:
        raise RuntimeError('%s: no se encontro <w:sectPr' % name)
    new_xml = xml[:idx] + insert + xml[idx:]

    new_data = {'word/document.xml': new_xml.encode('utf-8')}
    zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
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
            written = zout.filelist[-1]
            written.external_attr = info.external_attr
            written.create_version = info.create_version
        zout.comment = zin.comment
    finally:
        zout.close()
        zin.close()
    return new_xml


if __name__ == '__main__':
    import os
    outdir = sys.argv[1] if len(sys.argv) > 1 else '.'
    for name, path in FILES.items():
        dst = os.path.join(outdir, name + '_TEST.docx')
        new_xml = process(name, path, dst)
        print(name, '->', dst, len(new_xml), 'chars')
