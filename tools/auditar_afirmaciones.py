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
