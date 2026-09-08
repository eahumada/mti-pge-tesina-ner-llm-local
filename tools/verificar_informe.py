#!/usr/bin/env python3
"""Comprobaciones mecánicas del informe final y del repositorio.

Cada comprobación declara **cuántos elementos examinó**. Una que examina cero elementos se marca como
VACÍA y no como superada: este proyecto ya dio por buena una prueba de sensibilidad que no podía marcar
nada por construcción (§5.3 del informe), y una comprobación que no mira nada es indistinguible de una
que pasa.

Uso:  python3 tools/verificar_informe.py            # todas
      python3 tools/verificar_informe.py --breve    # solo el resumen final
Devuelve 0 si no hay fallos, 1 si los hay.
"""
import ast
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(RAIZ, 'doc/organized/Hito_5_Tarea4_Informe_Final/'
                        '2026-07-04_Borrador-Informe-Final-Tesina.md')
DIR_MD = os.path.dirname(MD)
SCRIPT_FIGURAS = os.path.join(RAIZ, 'tools/generar_figuras_informe.py')

EXCLUIDOS = ['nuextract', 'minimax-m3', 'gemini-3.1-flash-lite', 'q8-64k', 'sonct988',
             'gemini-3.5-flash', 'phi3.5', 'gliner']

resultados = []


def check(nombre, examinados, fallos, nota=''):
    resultados.append((nombre, examinados, list(fallos), nota))


def texto():
    with open(MD, encoding='utf-8') as f:
        return f.read()


# --- 1. Ficheros rastreados vacíos -------------------------------------------------------------
def c_vacios():
    r = subprocess.run(['git', 'ls-files'], cwd=RAIZ, capture_output=True, text=True)
    fich = [l for l in r.stdout.split('\n') if l]
    malos = [f for f in fich
             if os.path.isfile(os.path.join(RAIZ, f)) and os.path.getsize(os.path.join(RAIZ, f)) == 0]
    check('ficheros rastreados a cero bytes', len(fich), malos,
          'un fichero vacío no da ningún síntoma; ver FINDINGS §F59')


# --- 2. Referencias cruzadas a secciones --------------------------------------------------------
def c_secciones(s):
    hay = set(re.findall(r'^#{2,4} (\d+(?:\.\d+)*)', s, re.M))
    citadas = set(re.findall(r'§(\d+(?:\.\d+)*)', s))
    check('referencias §x.y con destino existente', len(citadas),
          sorted(citadas - hay), 'los encabezados llegan al cuarto nivel')


# --- 3. Tablas ----------------------------------------------------------------------------------
def c_tablas(s):
    caps = [int(x) for x in re.findall(r'^_Tabla (\d+)\.', s, re.M)]
    fallos = []
    if caps != list(range(1, len(caps) + 1)):
        fallos.append('numeración no contigua en orden de aparición: %s' % caps)
    lineas = s.split('\n')
    for i, l in enumerate(lineas):
        m = re.match(r'^_Tabla (\d+)\.', l)
        if not m:
            continue
        # la leyenda va inmediatamente encima de su tabla, a dos líneas o menos
        if not any(lineas[j].lstrip().startswith('|') for j in range(i + 1, min(i + 4, len(lineas)))):
            fallos.append('leyenda de la Tabla %s sin tabla debajo' % m.group(1))
    for n in caps:
        cuerpo = s.replace('_Tabla %d.' % n, '')
        if not re.search(r'Tabla %d\b' % n, cuerpo):
            fallos.append('Tabla %d sin citar en el texto' % n)
    check('tablas numeradas, con leyenda encima y citadas', len(caps), fallos)


# --- 4. Figuras ---------------------------------------------------------------------------------
def c_figuras(s):
    caps = [int(x) for x in re.findall(r'^_Figura (\d+)\.', s, re.M)]
    fallos = []
    if caps != list(range(1, len(caps) + 1)):
        fallos.append('numeración no contigua: %s' % caps)
    lineas = s.split('\n')
    for i, l in enumerate(lineas):
        m = re.match(r'^_Figura (\d+)\.', l)
        if m and not any(lineas[j].startswith('![') for j in range(max(0, i - 3), i)):
            fallos.append('leyenda de la Figura %s sin imagen encima (la norma la pone debajo)'
                          % m.group(1))
    for n in caps:
        if not re.search(r'(?:la|La|las|Las) Figura %d\b' % n, s):
            fallos.append('Figura %d sin citar en el texto' % n)
    imgs = re.findall(r'^!\[[^\]]*\]\(([^)]+)\)', s, re.M)
    for m in imgs:
        p = os.path.join(DIR_MD, m)
        if not os.path.exists(p):
            fallos.append('imagen inexistente: %s' % m)
        elif os.path.getsize(p) == 0:
            fallos.append('imagen vacía: %s' % m)
    check('figuras numeradas, con leyenda debajo, citadas y con imagen real',
          len(caps) + len(imgs), fallos)


# --- 5. Bibliografía ----------------------------------------------------------------------------
def c_bibliografia(s):
    ent = sorted(int(x) for x in re.findall(r'^\[(\d+)\] ', s, re.M))
    lineas = re.findall(r'^\[\d+\] .*$', s, re.M)
    fallos = []
    if ent != list(range(1, len(ent) + 1)):
        fallos.append('entradas no contiguas desde [1]')
    fallos += ['entrada sin URL: %s' % l[:60] for l in lineas if 'http' not in l]
    citadas = {int(x) for x in re.findall(r'\[(\d+)\]', s)}
    fallos += ['cita [%d] sin entrada' % c for c in sorted(citadas - set(ent))]
    fallos += ['entrada [%d] nunca citada' % e for e in sorted(set(ent) - citadas)]
    check('bibliografía contigua, con URL y correspondencia en ambos sentidos', len(ent), fallos)


# --- 6. Resumen y abstract ----------------------------------------------------------------------
def c_resumen(s):
    lineas = s.split('\n')
    bloques = []
    for i, l in enumerate(lineas[:40]):
        if len(l.split()) > 40 and not l.startswith(('#', '|', '_', '>')):
            bloques.append((i + 1, len(l.split())))
    fallos = ['línea %d con %d palabras (máximo 200)' % b for b in bloques if b[1] > 200]
    check('resumen y abstract por debajo de 200 palabras', len(bloques), fallos,
          'ambos deben decir lo mismo; la sincronía de contenido no es mecanizable')


# --- 7. Higiene del entregable ------------------------------------------------------------------
def c_higiene(s):
    """Los pictogramas se buscan FUERA del código en línea.

    Dentro de un tramo entre acentos graves el símbolo es un dato literal, no un adorno: el informe
    escribe «JosÃ© Bono» para ilustrar el mojibake, y ese texto contiene un © que no es un pictograma
    sino la mitad de la secuencia corrupta que se está explicando. Buscarlo en todo el documento
    convierte la comprobación en un falso positivo permanente, y una comprobación que siempre falla
    se acaba desactivando.
    """
    fallos = []
    codigo = set()
    for m in re.finditer(r'`[^`\n]*`', s):
        codigo.update(range(m.start(), m.end()))
    emo = {c for i, c in enumerate(s)
           if unicodedata.category(c) == 'So' and c not in '→←↑↓×' and i not in codigo}
    if emo:
        fallos.append('pictogramas fuera de código en línea: %s' % ''.join(sorted(emo))[:40])
    if '\xa0' in s:
        fallos.append('espacios duros \\xa0 presentes')
    if re.search(r'[┌┐└┘├┤┬┴┼─│]{2,}', s):
        fallos.append('arte ASCII presente')
    check('sin emojis, sin espacios duros y sin arte ASCII', len(s), fallos)


# --- 8. Modelos excluidos -----------------------------------------------------------------------
def c_excluidos(s):
    b = s.lower()
    check('sin modelos excluidos del estudio', len(EXCLUIDOS),
          ['aparece «%s»' % e for e in EXCLUIDOS if e in b],
          'la exclusión se aplica, no se narra: tampoco en una glosa')


# --- 9. La figura no puede divergir de su tabla -------------------------------------------------
def c_figura_vs_tabla(s):
    i = s.find('_Tabla 7.')
    if i < 0:
        check('Figura 2 coherente con la Tabla 7', 0, ['no se encuentra la Tabla 7'])
        return
    filas = []
    for l in s[i:i + 4000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|'
                     r'\s*\*{0,2}([−+-][\d.]+) pp\*{0,2}\s*\|\s*(\*\*sí\*\*|no)', l)
        if m:
            filas.append((m.group(1), float(m.group(2)), float(m.group(3)),
                          float(m.group(4).replace('−', '-')), m.group(5).startswith('**')))
    fallos = []
    for nom, base, rag, d, _ in filas:
        if abs(round(rag - base, 2) - d) > 0.011:
            fallos.append('Δ de %s: declara %+.2f, calcula %+.2f' % (nom, d, round(rag - base, 2)))
    try:
        sc = open(SCRIPT_FIGURAS, encoding='utf-8').read()
        lit = sc[sc.index('TABLA7 = ['):]
        lit = lit[:lit.index(']\n') + 1]
        script = ast.literal_eval(lit.split('=', 1)[1].strip())
    except Exception as e:
        fallos.append('no se puede leer TABLA7 del script: %s' % e)
        script = []
    if script:
        if len(script) != len(filas):
            fallos.append('el script tiene %d filas y la tabla %d' % (len(script), len(filas)))
        for a, b in zip(filas, script):
            if a[0] != b[0] or abs(a[1] - b[1]) > 1e-9 or abs(a[2] - b[2]) > 1e-9 or a[4] != b[3]:
                fallos.append('fila distinta: tabla %s vs script %s' % (a[:3], b[:3]))
    check('Figura 2 coherente con la Tabla 7 y Δ aritméticamente correcto', len(filas), fallos)


# --- 10. Identificadores sin colisión ------------------------------------------------------------
def c_identificadores():
    fallos = []
    total = 0
    for fich, pref in ((os.path.join(RAIZ, 'FINDINGS.md'), 'F'), (os.path.join(RAIZ, 'LEARNING.md'), 'L')):
        if not os.path.exists(fich):
            continue
        nums = re.findall(r'^#{2,3} *§?%s(\d+)' % pref, open(fich, encoding='utf-8').read(), re.M)
        total += len(nums)
        vistos = {}
        for n in nums:
            vistos[n] = vistos.get(n, 0) + 1
        fallos += ['§%s%s aparece %d veces' % (pref, n, c) for n, c in vistos.items() if c > 1]
    check('identificadores §F y §L sin colisión', total, fallos,
          'ha habido tres colisiones; comprobarlo en el mismo turno en que se escribe')


# --- 11. Aritmética de las tablas de métricas ---------------------------------------------------
PALABRAS = {'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8,
            'nueve': 9, 'diez': 10, 'once': 11, 'doce': 12, 'trece': 13, 'catorce': 14,
            'quince': 15, 'dieciséis': 16, 'veintiséis': 26, 'treinta': 30, 'cuarenta y dos': 42}


def _celdas(l):
    return [c.strip() for c in l.strip().strip('|').split('|')]


def _num(c):
    return float(re.sub(r'[^\d.,-]', '', c).replace(',', '.')) if re.search(r'\d', c) else None


def _tablas(s):
    """Devuelve (numero, leyenda, cabecera, filas) por cada tabla con leyenda."""
    L = s.split('\n')
    out, i = [], 0
    while i < len(L):
        m = re.match(r'^_Tabla (\d+)\. (.*)_$', L[i])
        if not m:
            i += 1
            continue
        j = i + 1
        while j < len(L) and not L[j].lstrip().startswith('|'):
            j += 1
        if j >= len(L):
            i += 1
            continue
        k, filas = j + 2, []
        while k < len(L) and L[k].lstrip().startswith('|'):
            filas.append(L[k])
            k += 1
        out.append((m.group(1), m.group(2), _celdas(L[j]), filas))
        i = k
    return out


def c_aritmetica(s):
    """F1 no puede superar la media de precisión y exhaustividad."""
    fallos, filas_vistas, tablas = [], 0, 0
    for n, _, cab, filas in _tablas(s):
        c = [x.lower() for x in cab]

        def idx(*claves):
            """Coincidencia exacta, nunca por prefijo.

            «Parámetros» empieza por «p» y se tomaba por «Precisión», con lo que la comprobación
            leía el número de parámetros como si fuera la precisión y daba catorce falsos positivos.
            Una abreviatura de una letra solo vale si la celda ES esa letra.
            """
            for k, v in enumerate(c):
                if any(v == x or v.rstrip('.') == x for x in claves):
                    return k
            return None

        ip = idx('precisión', 'precision', 'p')
        ir = idx('recall', 'exhaustividad', 'r')
        i1 = idx('f1')
        if None in (ip, ir, i1) or len({ip, ir, i1}) < 3:
            continue
        tablas += 1
        for l in filas:
            cel = _celdas(l)
            if len(cel) <= max(ip, ir, i1):
                continue
            p, r, f = _num(cel[ip]), _num(cel[ir]), _num(cel[i1])
            if None in (p, r, f):
                continue
            filas_vistas += 1
            if f > (p + r) / 2 + 0.02:
                fallos.append('Tabla %s, «%s»: F1 %.2f supera la media de P y R (%.2f)'
                              % (n, cel[0][:32], f, (p + r) / 2))
    check('F1 nunca superior a la media de P y R', filas_vistas, fallos,
          'comprobadas %d tablas con las tres métricas' % tablas)


# --- 12. La leyenda cuenta lo que la tabla tiene -------------------------------------------------
def c_recuentos(s):
    """Si la leyenda declara «trece modelos» o «42 configuraciones», deben ser tantas filas."""
    fallos, declarados = [], 0
    for n, ley, _, filas in _tablas(s):
        vistos = []
        for m in re.finditer(r'(\d+|%s)\s+(modelos|configuraciones|filas)'
                             % '|'.join(PALABRAS), ley, re.I):
            crudo = m.group(1).lower()
            v = int(crudo) if crudo.isdigit() else PALABRAS.get(crudo)
            if v is not None:
                vistos.append((v, m.group(2)))
        if not vistos:
            continue
        declarados += 1
        # Basta con que UNO de los recuentos declarados sea el de filas. La Tabla 4 dice «doce
        # modelos en trece configuraciones» y tiene trece filas: las dos cifras son ciertas y
        # describen cosas distintas, porque un modelo aporta dos configuraciones de prompt.
        if not any(v == len(filas) for v, _ in vistos):
            fallos.append('Tabla %s declara %s y tiene %d filas'
                          % (n, ' y '.join('%d %s' % x for x in vistos), len(filas)))
    check('los recuentos que declara una leyenda coinciden con sus filas', declarados, fallos,
          'solo se comprueban las leyendas que declaran un recuento explícito')


def main():
    s = texto()
    c_vacios()
    c_secciones(s)
    c_tablas(s)
    c_figuras(s)
    c_bibliografia(s)
    c_resumen(s)
    c_higiene(s)
    c_excluidos(s)
    c_figura_vs_tabla(s)
    c_identificadores()
    c_aritmetica(s)
    c_recuentos(s)

    breve = '--breve' in sys.argv
    fallos_totales = vacias = 0
    for nombre, n, fallos, nota in resultados:
        if n == 0:
            estado, vacias = 'VACIA ', vacias + 1
        elif fallos:
            estado, fallos_totales = 'FALLA ', fallos_totales + len(fallos)
        else:
            estado = 'ok    '
        if not breve or fallos or n == 0:
            print('  %s %-62s (%d elementos)' % (estado, nombre, n))
            for f in fallos[:8]:
                print('           - %s' % f)
            if len(fallos) > 8:
                print('           ... y %d más' % (len(fallos) - 8))
            if (fallos or n == 0) and nota:
                print('           nota: %s' % nota)
    print('\n  %d comprobaciones · %d fallos · %d vacías' % (len(resultados), fallos_totales, vacias))
    return 1 if (fallos_totales or vacias) else 0


if __name__ == '__main__':
    sys.exit(main())
