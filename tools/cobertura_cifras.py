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
AUD = os.path.join(RAIZ, 'tools/auditar_afirmaciones.py')

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


def _literales(ruta):
    """Cadenas largas de un fichero .py, leidas con `ast`.

    Con `ast` y no con una expresion regular sobre el codigo: un apostrofo suelto dentro de un
    docstring desalinea el emparejamiento de comillas y, a partir de ahi, los literales quedan mal
    delimitados. La primera version de esta herramienta lo hacia asi y **perdia anclas en silencio**
    —713 fragmentos mal cortados y cero con la palabra «Levene», sobre un fichero que la usa cuatro
    veces—. El sintoma de leer codigo con un regex es que faltan cosas, no que sobren.
    """
    import ast as _ast
    if not os.path.exists(ruta):
        return set()
    with open(ruta, encoding='utf-8') as fh:
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


def anclas():
    """Anclas al texto del informe, de TODAS las herramientas que lo comprueban.

    Al principio solo se leia el verificador, y eso producia falsos descubiertos en masa: las tres
    cifras del F1 restringido y el 66,0 % de la categoria fantasma **si** estan vigiladas, pero por
    `auditar_afirmaciones.py`, que es otra herramienta. Se leen las dos.
    """
    out = set()
    for r in (VER, AUD):
        out |= _literales(r)
    return out


def valores_de_artefactos():
    """Cifras que viven en un artefacto JSON que el verificador lee.

    Es la tercera ruta de cobertura, y hace falta porque varias comprobaciones **no se anclan en la
    prosa**: leen un valor del artefacto, lo formatean a la espanola y buscan esa cadena en el
    documento. `c_correlacion` es el caso —el `rho = -0,5165` de Spearman y sus dos p estan
    verificados, comprobado por mutacion, y la herramienta los daba por descubiertos porque no hay
    ninguna frase que anclar—.

    Se recogen los numeros de los JSON bajo `results/` **que la fuente del verificador nombra**, no
    de todos: un artefacto que nadie lee no acredita nada. La correspondencia es por los digitos,
    con dos y cuatro decimales, que es como el informe los escribe.
    """
    import json as _json
    import glob as _glob
    citados = set()
    for t in _literales(VER) | {c for c in _crudos(VER)}:
        for m in re.finditer(r'[\w./-]+\.json', t):
            citados.add(os.path.basename(m.group(0)))
    if not citados:
        return set()
    out = set()

    def _hoja(v):
        if isinstance(v, dict):
            for x in v.values():
                _hoja(x)
        elif isinstance(v, list):
            for x in v:
                _hoja(x)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            for d in (2, 4):
                out.add(('%.*f' % (d, abs(v))).replace('.', ','))
                out.add(('%.*f' % (d, abs(v) * 100)).replace('.', ','))
    base = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')
    for ruta in _glob.glob(os.path.join(base, '**', '*.json'), recursive=True):
        if os.path.basename(ruta) not in citados:
            continue
        try:
            with open(ruta, encoding='utf-8') as fh:
                _hoja(_json.load(fh))
        except (OSError, ValueError):
            continue
    return out


def _crudos(ruta):
    """Los literales cortos tambien, solo para buscar nombres de fichero .json en ellos."""
    import ast as _ast
    if not os.path.exists(ruta):
        return set()
    with open(ruta, encoding='utf-8') as fh:
        arbol = _ast.parse(fh.read())
    return {n.value for n in _ast.walk(arbol)
            if isinstance(n, _ast.Constant) and isinstance(n.value, str)}


def declaradas():
    """Cifras que el verificador tiene como FALLO DECLARADO: vigiladas y en rojo a proposito.

    Aparecian como no cubiertas y son el caso contrario: hay una comprobacion que las mira, falla, y
    el fallo esta declarado con su motivo y su responsable. Marcarlas como descubiertas manda a
    revisar algo que ya esta decidido.
    """
    out = set()
    # las claves de FALLOS_DECLARADOS son fragmentos del mensaje de fallo; se leen del diccionario
    import ast as _ast
    if not os.path.exists(VER):
        return out
    with open(VER, encoding='utf-8') as fh:
        arbol = _ast.parse(fh.read())
    for nodo in _ast.walk(arbol):
        if not isinstance(nodo, _ast.Assign):
            continue
        if not any(isinstance(d, _ast.Name) and d.id == 'FALLOS_DECLARADOS' for d in nodo.targets):
            continue
        if isinstance(nodo.value, _ast.Dict):
            for k in nodo.value.keys:
                if isinstance(k, _ast.Constant) and isinstance(k.value, str):
                    for m in re.finditer(r'\d+[.,]\d+', k.value):
                        out.add(m.group(0).replace('.', ','))
    return out



def _a_regex(anc):
    """Un ancla puede ser una expresion regular o texto literal, y distinguirlo importa.

    La version anterior compilaba el ancla como regex y solo caia al literal **si la compilacion
    fallaba**. Eso deja pasar lo peor: una cadena que compila sin error y significa otra cosa. Los
    dos encabezados de tabla de `auditar_afirmaciones.py` —«| Configuracion | Corrida | P | R |
    ...»— contienen `|`, que en una expresion regular es **alternancia con ramas vacias**, de modo
    que casaban **129 734 veces** cada uno en el informe y marcaban como cubiertas las 84 cifras.
    El resultado era una herramienta que reportaba cero descubiertas, o sea exactamente la
    comprobacion vacua contra la que este proyecto lleva toda la revision avisando.

    El guardian es preciso y no heuristico: **un patron que casa con la cadena vacia no es un
    ancla**. Una alternancia con ramas vacias lo hace; `Tabla\\s+(\\d+)\\b` no. Asi que se compila, se
    prueba contra `''`, y si casa se trata como texto literal.

    La leccion general: que una cadena compile como expresion regular no la convierte en una.
    """
    try:
        r = re.compile(anc)
    except re.error:
        return re.compile(re.escape(anc))
    if r.search('') is not None:
        return re.compile(re.escape(anc))
    return r


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

    decl = declaradas()
    arte = valores_de_artefactos()
    desc, en_rojo, por_arte = [], [], []
    for tipo, i, t in hallados:
        ven = txt[max(0, i - a.ventana): i + a.ventana]
        if any(r.search(ven) for r in anc):
            continue
        # Una cifra que es FALLO DECLARADO no esta sin vigilar: esta vigilada, falla, y el fallo
        # tiene motivo y responsable. Marcarla como descubierta manda a revisar algo ya decidido.
        num = re.search(r'\d+,\d+', t)
        if num and num.group(0) in decl:
            en_rojo.append((tipo, t))
            continue
        if num and num.group(0) in arte:
            por_arte.append((tipo, t))
            continue
        desc.append((tipo, i, t, ' '.join(ven.split())[:150]))

    print('  %d afirmaciones numericas en el cuerpo · %d sin ninguna comprobacion que las mire'
          % (len(hallados), len(desc)))
    print('  (%d anclas de verificar_informe.py y auditar_afirmaciones.py, ventana de %d '
          'caracteres)' % (len(anc), a.ventana))
    if por_arte:
        print('  %d mas coinciden con un valor de un artefacto JSON que el verificador lee, que es'
              % len(por_arte))
        print('     como las comprueban las que no se anclan en la prosa (p. ej. c_correlacion):')
        for tipo, t in por_arte:
            print('     [%s] %s' % (tipo, t))
    if en_rojo:
        print('  %d mas estan vigiladas y en FALLO DECLARADO, que no es lo mismo que sin vigilar:'
              % len(en_rojo))
        for tipo, t in en_rojo:
            print('     [%s] %s' % (tipo, t))
    print()
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
