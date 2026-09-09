#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cobertura_cifras.py — Que cifras del informe no tiene quien las recalcule.

Por que existe
--------------
El mismo parrafo de `§5` obligo a anadir **tres** comprobaciones distintas, una por cifra, y las
tres se encontraron por casualidad: el ANOVA titular al revisar los supuestos (`§F91`), Levene al
mirar si alguien leia su artefacto, y el recuento de Tukey al ir a corregir otra cosa (`§F115`).
Tres veces el mismo patron en el mismo parrafo significa que el metodo —tropezarse— no sirve. Esta
herramienta lo cambia por un barrido.

Que hace
--------
Enumera las afirmaciones numericas del **cuerpo** del informe —fuera de tablas y de bloques de
codigo, que se verifican por otra via— y dice, para cada una, si alguna comprobacion del verificador
se ancla en su vecindad. La cobertura se decide asi: se extraen de la fuente del verificador los
literales largos que sirven de ancla al texto del informe, y una cifra se considera **cubierta** si
alguno de ellos aparece en la ventana de texto que la rodea.

Limitaciones, declaradas
------------------------
Es una **aproximacion, y conservadora en un sentido y no en el otro**:

* Da **falsos cubiertos**: que una comprobacion se ancle cerca de una cifra no prueba que compruebe
  esa cifra. Puede leer la frase por otro motivo.
* Da **falsos descubiertos**: una comprobacion que recalcula desde los datos y compara por una
  ruta que esta herramienta no reconoce aparecera como ausente.

Por eso la salida **no es un veredicto sino una lista de candidatos a mirar a mano**, ordenada para
que las cifras con pinta de estadistico titular salgan primero. Su valor esta en que la lista es
**finita y repetible**, no en que sea exacta.
"""
import os
import re
import argparse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, 'doc/organized/Hito_5_Tarea4_Informe_Final/'
                        '2026-07-04_Borrador-Informe-Final-Tesina.md')
VER = os.path.join(RAIZ, 'tools/verificar_informe.py')

# Tipos de afirmacion, de mas a menos grave si nadie la recalcula.
PATRONES = [
    ('estadistico', r'(?:F|W|H|A|χ²|η²|R²|ρ)\s*=\s*[\d.,\s]+(?:\s*×\s*10[⁻⁰-⁹\d-]+)?'),
    ('p-valor',     r'p\s*[=<]\s*[\d.,]+(?:\s*×\s*10[⁻⁰-⁹\d-]+)?'),
    ('puntos',      r'\d+,\d+\s+puntos'),
    ('porcentaje',  r'\d+,\d+\s?%'),
]
ORDEN = {k: i for i, (k, _) in enumerate(PATRONES)}


def cuerpo():
    """El texto del informe sin tablas ni bloques de codigo."""
    with open(MD, encoding='utf-8') as fh:
        s = fh.read()
    out, en_codigo = [], False
    for l in s.split('\n'):
        if l.startswith('```'):
            en_codigo = not en_codigo
            out.append('')
            continue
        out.append('' if (en_codigo or l.startswith('|')) else l)
    return '\n'.join(out)


def anclas():
    """Literales de la fuente del verificador que sirven de ancla al texto del informe.

    Se leen con `ast`, no con una expresion regular. La primera version usaba un regex sobre el
    codigo fuente y **perdia anclas en silencio**: un apostrofo suelto dentro de un docstring
    desalinea el emparejamiento de comillas y, a partir de ahi, los literales siguientes quedan mal
    delimitados. Se detecto porque la comprobacion de Levene, que **si** se ancla en el informe con
    un regex explicito, aparecia como ausente: cero anclas con la palabra «Levene» sobre un fichero
    que la usa cuatro veces.

    Se toman las cadenas largas: las cortas coinciden por casualidad y marcarian casi todo como
    cubierto.
    """
    import ast as _ast
    with open(VER, encoding='utf-8') as fh:
        src = fh.read()
    out = set()
    for nodo in _ast.walk(_ast.parse(src)):
        if not (isinstance(nodo, _ast.Constant) and isinstance(nodo.value, str)):
            continue
        t = nodo.value
        if not 14 <= len(t) <= 400:
            continue
        if not re.search(r'[a-záéíóúñ]{4}', t, re.I):
            continue
        if t.startswith(('%', '  ')) or t.endswith(('.py', '.json', '.csv', '.md')):
            continue
        out.add(t)
    return out



def _a_regex(anc):
    """Un ancla puede ser una expresion regular o texto literal; se prueban las dos."""
    try:
        return re.compile(anc)
    except re.error:
        return re.compile(re.escape(anc))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--ventana', type=int, default=160,
                    help='caracteres a cada lado de la cifra donde se busca un ancla (160)')
    ap.add_argument('--todo', action='store_true', help='listar tambien las cubiertas')
    a = ap.parse_args()

    txt = cuerpo()
    anc = [_a_regex(x) for x in anclas()]
    if not anc:
        print('  VACIA: no se extrajo ningun ancla de la fuente del verificador')
        return 2

    hallados = []
    for tipo, pat in PATRONES:
        for m in re.finditer(pat, txt):
            hallados.append((tipo, m.start(), m.group(0).strip()))
    # una cifra puede casar con dos patrones; gana el mas grave
    mejor = {}
    for tipo, i, t in hallados:
        k = (i, t)
        if k not in mejor or ORDEN[tipo] < ORDEN[mejor[k][0]]:
            mejor[k] = (tipo, i, t)
    hallados = sorted(mejor.values(), key=lambda x: (ORDEN[x[0]], x[1]))

    desc = []
    for tipo, i, t in hallados:
        ven = txt[max(0, i - a.ventana): i + a.ventana]
        if not any(r.search(ven) for r in anc):
            desc.append((tipo, i, t, ' '.join(ven.split())[:150]))

    print('  %d afirmaciones numericas en el cuerpo · %d sin ancla de ninguna comprobacion'
          % (len(hallados), len(desc)))
    print('  (%d anclas extraidas de la fuente del verificador, ventana de %d caracteres)\n'
          % (len(anc), a.ventana))
    porTipo = {}
    for tipo, _, _, _ in desc:
        porTipo[tipo] = porTipo.get(tipo, 0) + 1
    for tipo, _ in PATRONES:
        n = sum(1 for x in hallados if x[0] == tipo)
        print('  %-12s %3d en el informe · %3d sin ancla' % (tipo, n, porTipo.get(tipo, 0)))
    print()
    for tipo, i, t, ctx in desc:
        print('  [%s] %s' % (tipo, t))
        print('      ...%s...' % ctx)
    if a.todo:
        print('\n  ── cubiertas ──')
        for tipo, i, t in hallados:
            if not any(x[1] == i and x[2] == t for x in desc):
                print('  [%s] %s' % (tipo, t))
    print('\n  Esto NO es un veredicto: hay falsos cubiertos —un ancla cerca no prueba que se')
    print('  compruebe esa cifra— y falsos descubiertos —una comprobacion que recalcula por una')
    print('  ruta que esta herramienta no reconoce—. Es una lista finita y repetible que mirar.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
