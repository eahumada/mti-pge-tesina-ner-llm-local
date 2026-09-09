#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar_afirmaciones.py — Comprueba que el registro no afirme correcciones que no se aplicaron.

Por que existe
--------------
El 2026-09-10 un reemplazo en `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md` **fallo** —el texto buscado tenia
saltos de linea y la cadena de busqueda no— y la orden compuesta **siguio adelante hasta el
`git commit`**. Resultado: `FINDINGS §F107` quedo afirmando «sustituido por un par verificado»
mientras el documento seguia con el ejemplo viejo. El `assert` del script detecto el fallo y lo
dijo; lo que no hizo fue abortar la cadena que lo invocaba.

Es la forma mas silenciosa de que un proyecto acabe mintiendo sobre si mismo: **el registro
sobrevive al fallo de la edicion que describe**. Un `git status` limpio no lo detecta, porque el
registro si se escribio.

Que hace
--------
Cada afirmacion concreta del registro se expresa aqui como un **predicado sobre los ficheros
reales**. No es una copia de la afirmacion —eso seria una segunda fuente de verdad (§L63)—: es una
prueba de ella. Si el predicado falla, o el entregable no esta como el registro dice, o el registro
esta mal; en los dos casos hay que mirar.

Limitacion, declarada
---------------------
La lista se mantiene a mano, y por tanto **solo cubre lo que alguien se acordo de anotar**. No
pretende ser exhaustiva: pretende que las correcciones de mas peso no puedan quedarse en el
registro sin estar en el fichero. Al aplicar una correccion sustantiva, se anade su predicado.
"""
import os
import re
import sys
import zipfile
import argparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D1 = 'Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx'
D2 = 'Informe_Final_Tesina_NER.docx'
D3 = 'doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx'
MD = 'doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.md'
EXCLUIDOS = ('nuextract', 'minimax-m3', 'gemini-3.1-flash-lite', 'q8-64k')


def texto(rel):
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return None
    if rel.endswith('.docx'):
        with zipfile.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        return ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))
    with open(ruta, encoding='utf-8') as fh:
        return fh.read()


def celdas(rel, valor):
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return -1
    with zipfile.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    return len(re.findall(r'<w:t(?:\s[^>]*)?>%s</w:t>' % re.escape(valor), x))


def _filas_md(cabecera, ncols):
    """Filas de una tabla del Markdown, en orden, como lista de listas."""
    txt = texto(MD)
    if txt is None:
        return None
    i = txt.find(cabecera)
    if i < 0:
        return None
    out = []
    for l in txt[i:].split('\n')[2:]:
        if not l.startswith('|'):
            break
        c = [z.strip().strip('`') for z in l.strip('|').split('|')]
        if len(c) == ncols:
            out.append(c)
    return out or None


def _filas_docx(rel, marca):
    """Filas de la tabla que contiene `marca`, en orden, como lista de listas."""
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return None
    with zipfile.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    T = lambda s: ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', s, re.S))
    cand = [b for b in re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S) if marca in T(b)]
    if len(cand) != 1:
        return None
    out = []
    for f in re.findall(r'<w:tr[ >].*?</w:tr>', cand[0], re.S)[1:]:
        out.append([T(c).strip() for c in re.findall(r'<w:tc>.*?</w:tc>', f, re.S)])
    return out or None


def _tabla_igual(marca, cabecera, ncols):
    """La tabla de los tres .docx coincide con la del Markdown, en contenido y en orden."""
    m = _filas_md(cabecera, ncols)
    if m is None:
        return False, 'no se puede leer la tabla del Markdown'
    malos = []
    for rel in (D1, D2, D3):
        d = _filas_docx(rel, marca)
        base = os.path.basename(rel)
        if d is None:
            malos.append('%s: no se identifica la tabla' % base)
            continue
        if len(d) != len(m):
            malos.append('%s: %d filas frente a %d del Markdown' % (base, len(d), len(m)))
            continue
        dif = next((k for k in range(len(m)) if d[k] != m[k]), None)
        if dif is not None:
            malos.append('%s: la fila %d difiere — .docx %s vs .md %s'
                         % (base, dif + 1, d[dif][:2], m[dif][:2]))
    return (not malos), ' · '.join(malos)


def _resalte_33():
    """En §3.3 el resalte cubre solo el porcentaje, no la frase entera."""
    malos = []
    for rel in (D1, D2, D3):
        ruta = os.path.join(RAIZ, rel)
        base = os.path.basename(rel)
        if not os.path.exists(ruta):
            malos.append('%s no existe' % base)
            continue
        with zipfile.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        solo = re.search(r'<w:r><w:rPr><w:b/></w:rPr><w:t[^>]*>66,0 %</w:t></w:r>', x) is not None
        frase = 'el 66,0 % de los falsos positivos' in re.sub(
            r'<[^>]+>', '', x[max(0, x.find('<w:b/></w:rPr><w:t')):]) and \
            re.search(r'<w:b/></w:rPr><w:t[^>]*>el 66,0 %', x) is not None
        if not solo:
            malos.append('%s: «66,0 %%» no esta en su propio run en negrita' % base)
        if frase:
            malos.append('%s: la frase entera sigue en negrita' % base)
    return (not malos), ' · '.join(malos)


def _rutas_afirmadas():
    """Ninguna afirmacion de que algo «se conserva en <ruta>» puede apuntar a una ruta inexistente.

    El 2026-09-09 la nota del consolidado nuevo decia «la corrida buggy **se conserva** en
    `results/recorrida_20260908/nemotron-mini_4b__N120_F85_BUGGY/` [...] **No se borra**», y el
    directorio se habia retirado ese mismo dia por instruccion del autor. La afirmacion sobrevivio
    al hecho que describia, que es la forma exacta de fallo que esta herramienta existe para cazar,
    aplicada esta vez a una ruta y no a una cifra.

    Se revisan las frases que **afirman conservacion** —«se conserva», «se conservan», «no se
    borra», «conservado en», «esta en»— y se comprueba que la ruta entre acentos graves exista. Se
    ignoran las que van dentro de una cita en bloque o tachadas, porque ahi el texto esta
    explicitamente marcado como historico.
    """
    DOCS = ['CURRENT-TASKS.md', 'FINDINGS.md', 'LEARNING.md',
            'repos/ner-llm-entity-benchmark/results/ANALISIS_CONJUNTO_20260909_FIX/NOTA-FIX-F85.md']
    AFIRMA = ('se conserva', 'se conservan', 'no se borra', 'conservado en', 'conservada en')
    malos, mirados = [], 0
    for rel in DOCS:
        t = texto(rel)
        if t is None:
            continue
        for linea in t.split('\n'):
            l = linea.strip()
            if l.startswith('>') or l.startswith('~~') or '~~' in l:
                continue          # citado como historico o tachado
            if not any(a in l.lower() for a in AFIRMA):
                continue
            for m in re.finditer(r'`([A-Za-z0-9_./-]*(?:results|repos|doc|tools)/[A-Za-z0-9_./-]+)`', l):
                ruta = m.group(1).rstrip('/')
                if ruta.startswith('results/'):
                    ruta = 'repos/ner-llm-entity-benchmark/' + ruta
                mirados += 1
                if not os.path.exists(os.path.join(RAIZ, ruta)):
                    malos.append('%s afirma conservar `%s`, que no existe'
                                 % (os.path.basename(rel), m.group(1)))
    if mirados == 0:
        return False, 'VACIA: no se examino ninguna ruta afirmada como conservada'
    return (not malos), ' · '.join(malos) or '%d rutas afirmadas, todas existen' % mirados


def _sin_recuentos_copiados():
    """Los documentos de norma no copian recuentos que las herramientas reportan.

    `CLAUDE.md` afirmaba «el resumen los cuenta aparte: 4 fallos (4 declarados, 0 nuevos)» y
    enumeraba cuales eran, cuando ya habia **veinticinco** declaraciones y sesenta y un fallos. Y
    decia «el verificador y sus 55 comprobaciones», cierto el dia que se escribio y falso al
    siguiente. Es el defecto de `LEARNING §L69` en el documento que **todos los agentes leen** para
    saber como trabajar: quien lo lea y no ejecute la herramienta se queda con una cifra vieja.

    La regla: un recuento que una herramienta reporta **no se copia a un documento de norma**. Se
    ejecuta la herramienta. Esto no alcanza a los **registros fechados** —el §6 de
    `CURRENT-TASKS.md`, los `WORKLOG`, `FINDINGS`— donde una cifra consigna lo que era cierto
    entonces y por eso no se actualiza: a un registro se le anade, no se le edita.
    """
    # `doc/prompts` entra desde el 2026-09-09: son documentos de PROCEDIMIENTO, que alguien pega
    # en una sesion nueva para ejecutar una revision, y llevaban recuentos copiados —«cubre diez
    # comprobaciones» con su lista, cuando habia cincuenta y cinco—. Un procedimiento que declara
    # de menos manda hacer menos.
    import glob as _g
    DOCS = (['CLAUDE.md', 'ENCARGO-EQUIPO-48GB-SOLO-CORRIDAS-VALIDAS-20260909.md']
            + sorted(os.path.relpath(x, RAIZ)
                     for x in _g.glob(os.path.join(RAIZ, 'doc/prompts/*.md'))))
    PATRONES = [
        (r'\b(\d+)\s+comprobaciones\b', 'un recuento de comprobaciones'),
        (r'\b(\d+)\s+fallos?\s*\((\d+)\s+declarad', 'el resumen de fallos del verificador'),
        (r'\b(\d+)\s+declaraciones\b', 'un recuento de declaraciones'),
        (r'\bsus\s+(\d+)\s+comprobacion', 'un recuento de comprobaciones'),
    ]
    malos, mirados = [], 0
    for rel in DOCS:
        t = texto(rel)
        if t is None:
            continue
        mirados += 1
        for pat, que in PATRONES:
            for m in re.finditer(pat, t):
                ctx = ' '.join(t[max(0, m.start() - 60):m.start() + 50].split())
                malos.append('%s copia %s («%s»): ejecutar la herramienta en lugar de anotarlo — '
                             '...%s...' % (os.path.basename(rel), que, m.group(0), ctx[:90]))
    if mirados == 0:
        return False, 'VACIA: no se examino ningun documento de norma'
    return (not malos), (' · '.join(malos)
                         or '%d documento(s) de norma sin recuentos copiados' % mirados)


def _recuento_de_decisiones():
    """El numero que el documento de decisiones declara coincide con las que tiene.

    Su encabezado decia «Son **siete**» el 2026-09-09, cuando tenia **diecinueve**, y
    `TODO-INFORME-FINAL.md` —que es donde el protocolo de seguimiento manda mirar las decisiones
    pendientes— repetia la misma cifra. Un recuento escrito a mano en el documento que lo define se
    queda atras con cada entrada que se anade, y nada avisa.

    **Si no cuadra, se corrige el encabezado y no se borran decisiones.** La politica del proyecto es
    aditiva: cuando un recuento no cuadra, el defecto esta en el recuento.
    """
    DEC = 'DECISIONES-PENDIENTES-20260908.md'
    t = texto(DEC)
    if t is None:
        return False, '%s no existe' % DEC
    reales = re.findall(r'^## (\d+)\. ', t, re.M)
    n = len(reales)
    if n == 0:
        return False, 'VACIA: no se localiza ningun encabezado «## N.» de decision'
    m = re.search(r'\*\*Son (\d+)\*\*', t)
    if m is None:
        return False, ('el encabezado no declara cuantas decisiones hay («**Son N**»), de modo que '
                       'nada ata el recuento; hay %d' % n)
    dec = int(m.group(1))
    if dec != n:
        return False, ('el encabezado declara %d decisiones y hay %d encabezados «## N.». '
                       'Corregir el ENCABEZADO, no borrar decisiones' % (dec, n))
    # y que la numeracion sea contigua desde 1, para que no haya huecos ni repetidas
    nums = sorted(int(x) for x in reales)
    if nums != list(range(1, n + 1)):
        return False, ('la numeracion de las decisiones no es contigua desde 1: %s' % nums)
    return True, '%d decisiones, el encabezado las declara y la numeracion es contigua' % n


def afirmaciones():
    """(descripcion, quien la afirma, predicado). Cada una devuelve (ok, detalle)."""
    def _todos(rel_list, fn):
        malos = []
        for rel in rel_list:
            t = texto(rel)
            if t is None:
                malos.append('%s no existe' % os.path.basename(rel))
                continue
            ok, det = fn(t)
            if not ok:
                malos.append('%s: %s' % (os.path.basename(rel), det))
        return (not malos, ' · '.join(malos))

    TRES = [D1, D2, D3]
    return [
        ('cero modelos excluidos en los tres .docx', '§F94',
         lambda: _todos(TRES, lambda t: (
             sum(t.lower().count(e) for e in EXCLUIDOS) == 0,
             '%d menciones' % sum(t.lower().count(e) for e in EXCLUIDOS)))),
        ('la cifra de falsos positivos es 66,0 % y 12 852', '§F88',
         lambda: _todos(TRES, lambda t: (
             '66,0 %' in t and '12 852' in t and
             'de los falsos positivos del estudio, 20 946' not in t,
             'no trae 66,0 % / 12 852, o conserva el 20 946 atribuido al estudio'))),
        ('Tok/s/B de la Tabla 4 es 5.80 en dos celdas', '§F88',
         lambda: _todos(TRES, lambda t: (True, ''))
         if all(celdas(r, '5.80') == 2 and celdas(r, '5.33') == 0 for r in TRES)
         else (False, 'alguna copia no tiene 2 celdas a 5.80 y 0 a 5.33')),
        ('las tres cifras del F1 restringido estan propagadas', '§F95',
         lambda: _todos(TRES, lambda t: (
             all(v in t for v in ('76,55', '90,16', '80,42')) and
             not any(v in t for v in ('76,85', '90,91', '81,45')),
             'conserva alguna cifra vieja o le falta alguna nueva'))),
        ('la leyenda de la Tabla 19 declara 42 configuraciones', '§F94',
         lambda: _todos(TRES, lambda t: ('42 configuraciones' in t,
                                         'no dice 42 configuraciones'))),
        ('el resumen dice «instituciones financieras»', 'CLAUDE.md',
         lambda: _todos(TRES, lambda t: ('Las instituciones financieras sujetas' in t,
                                         'el resumen no concuerda con el abstract'))),
        ('el coste de la soberania dice «cuatro puntos»', '§L69',
         lambda: _todos(TRES, lambda t: (
             'cuatro puntos' in t and 'cinco puntos' not in t,
             'el numeral no cuadra con la resta'))),
        ('«solo» sin tilde en el .md y en los tres .docx', '§F105',
         lambda: _todos([MD] + TRES, lambda t: ('sólo' not in t,
                                                'conserva «solo» con tilde'))),
        # Las tres correcciones de mas peso del 2026-09-09 no tenian predicado, que es justo el
        # hueco que esta herramienta declara. Anadidas: las dos tablas propagadas y la particion
        # del run de §3.3.
        ('la Tabla 19 coincide con el Markdown celda por celda', '§F95',
         lambda: _tabla_igual('F1 restr.',
                              '| Configuración | Corrida | P | R | F1 | P restr. | F1 restr. | Δ F1 |',
                              8)),
        ('la Tabla 18 coincide con el Markdown en contenido y orden', '§F95',
         lambda: _tabla_igual('Δ F1 por entidad',
                              '| Configuración | Δ F1 por entidad de referencia | '
                              'Δ F1 por texto de entrada |', 3)),
        ('en §3.3 el resalte cubre solo el porcentaje', '§F96',
         lambda: _resalte_33()),
        ('el recuento de decisiones cuadra con las que hay', '§F135',
         lambda: _recuento_de_decisiones()),
        ('los documentos de norma no copian recuentos de las herramientas', '§F134',
         lambda: _sin_recuentos_copiados()),
        ('ninguna ruta afirmada como conservada ha desaparecido', '§F124',
         lambda: _rutas_afirmadas()),
        ('DEFENSA usa el ejemplo verificado del duplicado', '§F107',
         lambda: ((lambda t: ('Jose Bono' in t.replace('é', 'e') and '88,89' in t,
                              'no trae el par verificado'))(texto(
                                  'DEFENSA-PREGUNTAS-Y-RESPUESTAS.md') or ''))),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()
    filas = afirmaciones()
    malas = 0
    print('  %-52s %-10s %s' % ('afirmacion del registro', 'quien', 'estado'))
    for desc, quien, pred in filas:
        try:
            ok, det = pred()
        except Exception as e:                                        # noqa: BLE001
            ok, det = False, '%s: %s' % (type(e).__name__, e)
        print('  %-52s %-10s %s' % (desc[:52], quien, 'se cumple' if ok else '** NO **'))
        if not ok:
            print('      %s' % det)
            malas += 1
    print('\n  %d afirmaciones comprobadas · %d que no se cumplen' % (len(filas), malas))
    if not filas:
        print('  VACIA: no se comprobo ninguna afirmacion')
        return 2
    if malas:
        print('  Una afirmacion que no se cumple significa que el entregable no esta como el')
        print('  registro dice, o que el registro esta mal. En los dos casos hay que mirar.')
        return 1
    print('  el registro no afirma ninguna correccion que no se haya aplicado')
    return 0


if __name__ == '__main__':
    sys.exit(main())
