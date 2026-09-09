#!/usr/bin/env python3
"""Comprobaciones mecánicas del informe final y del repositorio.

Cada comprobación declara **cuántos elementos examinó**. Una que examina cero elementos se marca como
VACÍA y no como superada: este proyecto ya dio por buena una prueba de sensibilidad que no podía marcar
nada por construcción (§5.3 del informe), y una comprobación que no mira nada es indistinguible de una
que pasa.

Uso:  python3 tools/verificar_informe.py            # todas
      python3 tools/verificar_informe.py --breve    # solo lo que falla
      python3 tools/verificar_informe.py --red      # además comprueba las URL en red
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
        # «§F61.bis» es una subnumeración deliberada, no una colisión con «§F61»: el proyecto ya
        # usa ese sufijo en §2.bis y §3.bis. El identificador incluye el sufijo, cualquiera que sea:
        # la primera versión solo admitía «.bis» y marcó como colisión un «.ter» legítimo.
        nums = re.findall(r'^#{2,3} *§?%s(\d+(?:\.[a-z]+)?)' % pref,
                          open(fich, encoding='utf-8').read(), re.M)
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


# --- 13. Las URL de la bibliografía responden (opcional: --red) ----------------------------------
# Editoriales que bloquean al lector automático. CLAUDE.md ya admite acreditarlas por resolución del
# DOI y dejar constancia: un 403 de ACM no es un enlace roto, es un portero.
# Servidores que devuelven 401/403 a un lector automatico aunque el recurso exista. Comprobado el
# 2026-09-08: zenodo.org responde 403 incluso en su propia raiz, de modo que un 403 suyo no dice nada
# sobre la entrada. Una URL de un portero se acredita por RESOLUCION DEL DOI, nunca dandola por buena.
PORTEROS = ('dl.acm.org', 'acm.org', 'ieeexplore.ieee.org', 'sciencedirect.com',
            'link.springer.com', 'zenodo.org')

# Entradas de un portero cuyo trabajo NO tiene DOI registrado, de modo que la acreditacion por
# resolucion del DOI no puede aplicarse. Cada una lleva la evidencia externa que la sostiene.
# No es una lista para ir ampliando cuando algo moleste: exige una fuente independiente que ate
# el identificador al trabajo, porque ACM devuelve 403 igual a un identificador real que a uno
# inventado — comprobado el 2026-09-08 con 10.5555/000000.000000, que tambien da 403.
# La clave es (numero, URL EXACTA). Atarla solo al numero acreditaria cualquier URL que se
# pusiera en esa entrada, que es el defecto de §L57: devolver el valor del exito sin mirar.
# Comprobado por mutacion: con la clave solo numerica, sustituir la URL de [17] por un
# identificador inventado pasaba sin que nada lo notase.
SIN_DOI_ACREDITADAS = {
    ('17', 'https://dl.acm.org/doi/10.5555/645530.655813'):
          ('Lafferty, McCallum y Pereira, ICML 2001. OpenAlex lo registra con 12 994 citas y '
           'doi: None: el trabajo no tiene DOI, y el 10.5555 es el identificador interno de ACM '
           'para material heredado. Copia abierta verificada (HTTP 200): '
           'https://repository.upenn.edu/handle/20.500.14332/6188'),
}


def c_urls(s):
    import socket
    import urllib.request
    import urllib.error
    # El paréntesis SÍ forma parte de algunos DOI: 10.1016/0169-7552(89)90019-6. Cortar en «)»
    # trunca la referencia [26] y la convierte en un 404 inventado por el propio verificador.
    urls = []
    for m in re.finditer(r'^\[(\d+)\] (.*)$', s, re.M):
        u = re.search(r'https?://[^\s>\]]+', m.group(2))
        urls.append((m.group(1), u.group(0).rstrip('.,;') if u else None))
    def resuelve_doi(url):
        """Un DOI acreditado responde 301/302 con destino. No sigue la redirección:
        el destino es justo el portero que bloquea, y seguirlo devolvería su 403."""
        m = re.search(r'(10\.\d{4,9}/[^\s]+)', url)
        if not m:
            return None
        class NoSigas(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        op = urllib.request.build_opener(NoSigas)
        try:
            op.open('https://doi.org/' + m.group(1), timeout=25)
        except urllib.error.HTTPError as e:
            destino = e.headers.get('Location', '') if e.headers else ''
            if e.code in (301, 302, 303, 307, 308) and destino:
                return destino
        except Exception:
            return None
        return None

    fallos, acreditadas, inciertas = [], [], []
    for n, u in urls:
        if u is None:
            fallos.append('[%s] sin URL' % n)
            continue
        req = urllib.request.Request(u, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status >= 400:
                    fallos.append('[%s] HTTP %d — %s' % (n, r.status, u))
        except urllib.error.HTTPError as e:
            # El portero aparece TRAS la redirección: la entrada cita un doi.org que reenvía a
            # dl.acm.org, y mirar solo la URL de partida no lo detecta nunca.
            destino = getattr(e, 'url', '') or ''
            if e.code in (401, 403) and any(p in u or p in destino for p in PORTEROS):
                # No basta con que sea un portero: hay que acreditar la entrada por otra vía,
                # o un DOI inventado sobre un dominio bloqueado pasaría sin que nadie lo mirase.
                r = resuelve_doi(u)
                if r:
                    acreditadas.append('[%s] %d de %s, DOI resuelve a %s'
                                       % (n, e.code, destino.split('/')[2] if '//' in destino else u, r))
                elif (n, u) in SIN_DOI_ACREDITADAS:
                    acreditadas.append('[%s] sin DOI registrado; %s' % (n, SIN_DOI_ACREDITADAS[(n, u)]))
                else:
                    fallos.append('[%s] HTTP %d de un portero y su DOI no resuelve — %s' % (n, e.code, u))
                continue
            if 500 <= e.code < 600:
                inciertas.append('[%s] HTTP %d, caída del servidor — %s' % (n, e.code, u))
                continue
            fallos.append('[%s] HTTP %d — %s%s'
                          % (n, e.code, u, ' -> %s' % destino if destino and destino != u else ''))
        except Exception as e:
            # Un tiempo de espera agotado no acredita que el enlace esté roto: acredita que el
            # servidor no respondió a tiempo, y se declara aparte. Pero un dominio que no resuelve
            # en el DNS, o que rechaza la conexión, SI es un enlace roto y tiene que fallar.
            # Comprobado por mutación: sin esta distinción, un dominio inventado pasaba como
            # «no concluyente», que es tanto como no comprobar la bibliografía.
            razon = getattr(e, 'reason', None)
            roto = isinstance(razon, (socket.gaierror, ConnectionRefusedError, ConnectionResetError))
            if roto:
                fallos.append('[%s] el dominio no resuelve o rechaza la conexión — %s' % (n, u))
            elif resuelve_doi(u):
                acreditadas.append('[%s] %s, pero su DOI resuelve — %s' % (n, type(e).__name__, u))
            else:
                inciertas.append('[%s] %s — %s' % (n, type(e).__name__, u))
    nota = ('acreditadas por resolución del DOI: %d' % len(acreditadas)) if acreditadas else ''
    if inciertas:
        nota += ('%sno concluyentes (el servidor no respondió, que no es lo mismo que un enlace roto): %s'
                 % (' · ' if nota else '', '; '.join(inciertas)))
    check('las URL de la bibliografía responden', len(urls), fallos, nota)


# --- 14. Protocolo homogéneo ENTRE las corridas fusionadas ---------------------------------------
MANIFIESTO = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                'ANALISIS_CONJUNTO_20260907/merge_manifest.json')
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
# Parámetros que afectan a la medición y deben ser idénticos en todas las fuentes de un consolidado.
PARAMS = ('rag_mode', 'data_file', 'max_tokens', 'temperature', 'batch_size', 'fuzzy_threshold')

# Divergencias que el informe YA declara como reserva de comparabilidad. Se listan aquí para que la
# comprobación no falle indefinidamente: una comprobación que siempre falla se acaba desactivando
# (LEARNING §L48). Añadir una entrada exige haberla declarado antes en el informe, y retirarla cuando
# la corrida que la resuelve esté hecha.
DIVERGENCIAS_DECLARADAS = {
    'max_tokens': ('4096 en gptoss_rerun frente a 2048 en las demás; declarado en el Anexo I, '
                   'apartado «Corridas múltiples». Lo resuelve la re-corrida completa pendiente, '
                   'que fija 4096 para los trece modelos. Ver FINDINGS §F61.bis'),
}


def c_protocolo(s):
    """La comprobación de protocolo se venía aplicando DENTRO de cada corrida y nunca ENTRE ellas.

    Un consolidado que une ocho fuentes hereda las diferencias de las ocho: así se publicó
    gpt-oss:20b con el doble de presupuesto de salida que los otros doce modelos sin que nada lo
    advirtiera. Ver FINDINGS §F61.bis y LEARNING §L49.
    """
    import json
    if not os.path.exists(MANIFIESTO):
        check('protocolo homogéneo entre las corridas fusionadas', 0, ['no existe el manifiesto'])
        return
    man = json.load(open(MANIFIESTO, encoding='utf-8'))
    vistos, fallos = {}, []
    for f in man.get('sources', []):
        cfg = os.path.join(BENCH, os.path.dirname(f['csv_path']), 'run_config.json')
        if not os.path.exists(cfg):
            fallos.append('%s sin run_config.json' % f['label'])
            continue
        d = json.load(open(cfg, encoding='utf-8'))
        for p in PARAMS:
            if p in d:
                vistos.setdefault(p, {}).setdefault(str(d[p]), []).append(f['label'])
    declaradas = []
    for p, valores in sorted(vistos.items()):
        if len(valores) <= 1:
            continue
        detalle = '%s difiere: %s' % (p, '; '.join(
            '%s en %s' % (v, ', '.join(l)) for v, l in sorted(valores.items())))
        if p in DIVERGENCIAS_DECLARADAS:
            declaradas.append(p)
        else:
            fallos.append(detalle)
    nota = 'una diferencia aquí exige declararla como reserva de comparabilidad en el informe'
    if declaradas:
        nota = ('divergencias ya declaradas y pendientes de resolver: %s'
                % '; '.join('%s (%s)' % (p, DIVERGENCIAS_DECLARADAS[p]) for p in declaradas))
    check('protocolo homogéneo entre las corridas fusionadas',
          len(man.get('sources', [])), fallos, nota)
    if declaradas:
        print('  AVISO  %d divergencia(s) de protocolo declaradas, no resueltas:' % len(declaradas))
        for p in declaradas:
            print('           - %s: %s' % (p, DIVERGENCIAS_DECLARADAS[p]))


# --- 15. El Anexo I cuadra con la Tabla 7 ---------------------------------------------------------
def c_anexo_vs_tabla7(s):
    """Las mismas cifras aparecen en el cuerpo y en el anexo, y deben coincidir.

    Se comprobo a mano en una sesion anterior y nunca se automatizo, de modo que cualquier
    correccion posterior en una de las dos podia desincronizarlas sin aviso.
    """
    i = s.find('_Tabla 7.')
    j = s.find('_Tabla 19.')
    if i < 0 or j < 0:
        check('el Anexo I cuadra con la Tabla 7', 0, ['no se encuentran las tablas 7 o 19'])
        return
    t7 = {}
    for l in s[i:i + 3000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|', l)
        if m and not m.group(1).startswith('Modelo'):
            t7[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
    ai = {}
    for l in s[j:j + 12000].split('\n'):
        m = re.match(r'^\|\s*([\w.:\-]+)_(baseline|kb_rag|rag_enhanced)\s*\|\s*([^|]+)\|'
                     r'\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|', l)
        if m:
            ai.setdefault(m.group(1), {})[m.group(2)] = float(m.group(6))
    fallos = []
    for mod, (b, r) in t7.items():
        a = ai.get(mod)
        if not a:
            fallos.append('%s no aparece en el Anexo I' % mod)
            continue
        for modo, val in (('baseline', b), ('kb_rag', r)):
            v = a.get(modo)
            if v is None:
                fallos.append('%s: falta la fila %s en el Anexo I' % (mod, modo))
            elif abs(v - val) > 0.011:
                fallos.append('%s %s: Tabla 7 da %.2f y el Anexo I %.2f' % (mod, modo, val, v))
    check('el Anexo I cuadra con la Tabla 7', 2 * len(t7), fallos,
          'las mismas cifras en el cuerpo y en el anexo deben coincidir')


# --- 16. La Tabla 7 reproduce desde los datos ----------------------------------------------------
CSV_CONSOLIDADO = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                     'ANALISIS_CONJUNTO_20260907/merged_results.csv')


def c_tabla7_vs_datos(s):
    """La tabla central del informe, contrastada contra el CSV del que sale.

    Hasta el 2026-09-08 la Tabla 7 solo se comprobaba contra la Figura 2 y contra el Anexo I, es
    decir, contra otras dos copias de si misma. Que tres sitios coincidan no dice nada si los tres
    se escribieron a mano desde la misma lectura. Esta comprobacion es la unica que la ata al dato.
    """
    import csv as _csv
    import collections as _c
    if not os.path.exists(CSV_CONSOLIDADO):
        check('la Tabla 7 reproduce desde el CSV consolidado', 0,
              ['no existe %s' % os.path.relpath(CSV_CONSOLIDADO, RAIZ)])
        return
    i = s.find('_Tabla 7.')
    if i < 0:
        check('la Tabla 7 reproduce desde el CSV consolidado', 0, ['no se encuentra la Tabla 7'])
        return
    t7 = {}
    for l in s[i:i + 3000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|', l)
        if m and not m.group(1).startswith('Modelo'):
            t7[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
    g = _c.defaultdict(list)
    with open(CSV_CONSOLIDADO, encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            # `is not None` y no la veracidad del valor: un F1 de 0.0 es un dato, no un hueco.
            if r.get('f1') not in (None, ''):
                g[r['model']].append(float(r['f1']))
    dat = {k: 100 * sum(v) / len(v) for k, v in g.items()}
    fallos = []
    for mod, (b, r) in t7.items():
        for suf, val in (('_baseline', b), ('_kb_rag', r)):
            d = dat.get(mod + suf)
            if d is None:
                fallos.append('%s%s no esta en el CSV consolidado' % (mod, suf))
            elif abs(d - val) > 0.011:
                fallos.append('%s%s: la tabla dice %.2f y el dato da %.2f' % (mod, suf, val, d))
    check('la Tabla 7 reproduce desde el CSV consolidado', 2 * len(t7), fallos,
          'es la unica comprobacion que ata la tabla central al dato y no a otra copia suya')


# --- 17. La Tabla 4 reproduce desde sus corridas de origen ----------------------------------------
BENCH_DIR = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')
# Correspondencia fila -> (csv de origen, grupo dentro de ese csv). Refleja la Tabla 15 del informe,
# que declara la procedencia de cada fila; el grupo interno no figura alli porque la corrida de
# ablacion nombra sus condiciones «zs-es» y «fs-es» en lugar de «modelo_baseline».
FUENTES_T4 = {
    'gemma4:31b': ('results/gemma4_31b_n15_REMOTO/benchmark_results.csv', 'gemma4:31b_baseline'),
    'gemma4:31b-cloud': ('results/cloud_n15_limpio_20260905/benchmark_results.csv',
                         'gemma4:31b-cloud_baseline'),
    'gemma4:latest (ZS-ES)': ('results/ablacion_n15_REMOTO/benchmark_results.csv', 'zs-es'),
    'gemma4:latest (FS-ES)': ('results/ablacion_n15_REMOTO/benchmark_results.csv', 'fs-es'),
}
CSV_T4_DEFECTO = 'results/benchmark_results.csv'


def c_tabla4_vs_datos(s):
    """Las 13 filas del benchmark exploratorio, contra las corridas que las sostienen.

    Ademas de comparar los cuatro valores de cada fila, comprueba que la Tabla 15 siga nombrando
    las mismas corridas de origen: si alguien cambia la procedencia alli y no aqui, la
    correspondencia de este script quedaria obsoleta sin que nada avisara.
    """
    import csv as _csv
    import collections as _c
    i = s.find('_Tabla 4.')
    if i < 0:
        check('la Tabla 4 reproduce desde sus corridas', 0, ['no se encuentra la Tabla 4'])
        return
    filas = []
    for l in s[i:i + 3000].split('\n'):
        if not l.startswith('|') or 'Modelo' in l or '---' in l:
            continue
        c = [x.strip().replace('**', '') for x in l.strip().strip('|').split('|')]
        if len(c) >= 7 and c[3].endswith('%'):
            try:
                filas.append((c[0],) + tuple(float(x.rstrip('%')) for x in c[3:7]))
            except ValueError:
                pass
    cache = {}

    def med(p):
        if p not in cache:
            g = _c.defaultdict(lambda: _c.defaultdict(list))
            with open(os.path.join(BENCH_DIR, p), encoding='utf-8') as fh:
                for r in _csv.DictReader(fh):
                    for k in ('f1', 'precision', 'recall', 'hallucination_rate'):
                        if r.get(k) not in (None, ''):
                            g[r['model']][k].append(float(r[k]))
            cache[p] = {m: {k: 100 * sum(v) / len(v) for k, v in d.items()} for m, d in g.items()}
        return cache[p]

    fallos = []
    # guarda: la Tabla 15 debe seguir citando las mismas corridas de origen
    j = s.find('_Tabla 15.')
    t15 = s[j:j + 1500] if j >= 0 else ''
    for path, _ in FUENTES_T4.values():
        run = os.path.basename(os.path.dirname(path))
        if t15 and run not in t15:
            fallos.append('la Tabla 15 ya no cita «%s»: revisar FUENTES_T4' % run)
    for fila in filas:
        nom, f1, p, rc, h = fila
        path, grupo = FUENTES_T4.get(nom, (CSV_T4_DEFECTO, nom + '_baseline'))
        if not os.path.exists(os.path.join(BENCH_DIR, path)):
            fallos.append('%s: no existe %s' % (nom, path))
            continue
        v = med(path).get(grupo)
        if v is None:
            fallos.append('%s: el grupo «%s» no esta en %s' % (nom, grupo, path))
            continue
        for etiq, esperado, clave in (('F1', f1, 'f1'), ('P', p, 'precision'),
                                      ('R', rc, 'recall'), ('alucinacion', h, 'hallucination_rate')):
            d = v.get(clave)
            if d is None or abs(d - esperado) > 0.02:
                fallos.append('%s %s: la tabla dice %.2f y el dato %s'
                              % (nom, etiq, esperado, '—' if d is None else '%.2f' % d))
    check('la Tabla 4 reproduce desde sus corridas de origen', 4 * len(filas), fallos,
          'la correspondencia fila-corrida refleja la Tabla 15 del informe')


# --- 18. La Figura 1 y §3.3 reproducen desde el artefacto de composicion -------------------------
ARTEFACTO_FP = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                  'COMPOSICION_FP_20260908/composicion_fp_26_grupos.json')


def c_figura1_vs_artefacto(s):
    """La composicion de los falsos positivos, atada al fichero que la calcula.

    El informe llego a dar dos cifras distintas para esta magnitud, una de ellas sin respaldo en
    ningun dato (FINDINGS §F69). Esta comprobacion ata las tres apariciones —la prosa de §3.3, la
    del §7.2 y el script que dibuja la Figura 1— al artefacto que las computa.
    """
    import json as _json
    if not os.path.exists(ARTEFACTO_FP):
        check('la Figura 1 reproduce desde el artefacto de composicion', 0,
              ['no existe %s' % os.path.relpath(ARTEFACTO_FP, RAIZ)])
        return
    with open(ARTEFACTO_FP, encoding='utf-8') as fh:
        a = _json.load(fh)
    loc, tot, pct = a['fp_locations'], a['fp_total'], a['pct_fp_locations']
    # el complemento tambien se dibuja en la Figura 1 y debe cuadrar con el artefacto
    comp = a.get('fp_no_locations')
    fallos, mirados = [], 0
    # el artefacto debe declarar su propia cobertura y haberla completado
    mirados += 1
    if a.get('grupos') != a.get('grupos_cubiertos'):
        fallos.append('el artefacto cubre %s de %s grupos' % (a.get('grupos_cubiertos'), a.get('grupos')))
    # §3.3 y §7.2
    esp = '%.1f' % pct
    for etiqueta, patron in (('§3.3', r'\*\*%s\s*%%\*\*[^.]{0,90}?%s de %s'
                              % (esp.replace('.', ','), '{:,}'.format(loc).replace(',', ' '),
                                 '{:,}'.format(tot).replace(',', ' '))),
                             ('§7.2', r'procede el %s\s*%% de los falsos positivos' % esp.replace('.', ','))):
        mirados += 1
        if not re.search(patron, s):
            fallos.append('%s no cita %s %% con %d de %d' % (etiqueta, esp.replace('.', ','), loc, tot))
    # el script de figuras
    mirados += 1
    try:
        sc = open(SCRIPT_FIGURAS, encoding='utf-8').read()
        if not re.search(r'loc,\s*total\s*=\s*%d,\s*%d' % (loc, tot), sc):
            fallos.append('generar_figuras_informe.py no usa %d y %d' % (loc, tot))
        if esp.replace('.', ',') + ' %' not in sc:
            fallos.append('generar_figuras_informe.py no rotula %s %%' % esp.replace('.', ','))
    except Exception as e:
        fallos.append('no se puede leer el script de figuras: %s' % e)
    mirados += 1
    if comp is None or comp + loc != tot:
        fallos.append('el artefacto no declara fp_no_locations o no suma: %s + %s != %s' % (comp, loc, tot))
    check('la Figura 1 y la prosa reproducen desde el artefacto de composicion', mirados, fallos,
          'ata las tres apariciones de la cifra al fichero que la computa')


# --- 19. Las tablas 5, 6 y 8 reproducen desde sus corridas ---------------------------------------
def _medias(rel, campos, escala=100.0):
    import csv as _csv
    import collections as _c
    g = _c.defaultdict(lambda: _c.defaultdict(list))
    with open(os.path.join(BENCH_DIR, rel), encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            for k in campos:
                if r.get(k) not in (None, ''):
                    g[r['model']][k].append(float(r[k]))
    return {m: {k: (escala if k in ('f1', 'precision', 'recall', 'hallucination_rate') else 1.0)
                * sum(v) / len(v) for k, v in d.items()} for m, d in g.items()}


def c_tablas_menores(s):
    """Tabla 5 (variantes de prompt), Tabla 6 (N=30) y Tabla 8 (eficiencia), contra sus corridas.

    Completan la cobertura: con estas, todas las tablas de datos del informe estan atadas al dato y
    no a otra copia suya. La Tabla 5 rotula sus filas en espanol —«Zero-shot Ingles»— mientras la
    corrida nombra sus grupos «zs-en», de modo que la correspondencia se deduce del rotulo.
    """
    fallos, mirados = [], 0

    # --- Tabla 5
    abl = 'results/ablacion_n15_REMOTO/benchmark_results.csv'
    if os.path.exists(os.path.join(BENCH_DIR, abl)):
        d = _medias(abl, ('f1', 'precision', 'recall', 'hallucination_rate', 'latency_sec'))
        i = s.find('_Tabla 5.')
        for l in (s[i:i + 1500].split('\n') if i >= 0 else []):
            if not l.startswith('|') or '---' in l or 'Configuración' in l:
                continue
            c = [x.strip().replace('**', '') for x in l.strip().strip('|').split('|')]
            if len(c) < 6 or not c[1].endswith('%'):
                continue
            n = c[0].lower()
            g = ('fs-' if 'few' in n else 'zs-') + ('es' if 'espa' in n else 'en')
            if g not in d:
                fallos.append('Tabla 5: el grupo «%s» no esta en la corrida de ablacion' % g)
                continue
            for etiq, val, clave, tol in (('F1', c[1], 'f1', 0.02), ('P', c[2], 'precision', 0.02),
                                          ('R', c[3], 'recall', 0.02),
                                          ('alucinacion', c[4], 'hallucination_rate', 0.02),
                                          ('latencia', c[5], 'latency_sec', 0.06)):
                mirados += 1
                try:
                    a = float(str(val).rstrip('%'))
                except ValueError:
                    continue
                b = d[g].get(clave)
                if b is None or abs(a - b) > tol:
                    fallos.append('Tabla 5 %s %s: la tabla dice %.2f y el dato %s'
                                  % (c[0], etiq, a, '—' if b is None else '%.2f' % b))

    # --- Tabla 6
    n30 = 'results/n30_rerun_REMOTO/benchmark_results.csv'
    if os.path.exists(os.path.join(BENCH_DIR, n30)):
        d = _medias(n30, ('f1', 'precision', 'recall'))
        i = s.find('_Tabla 6.')
        for l in (s[i:i + 1200].split('\n') if i >= 0 else []):
            if not l.startswith('|') or '---' in l or 'Modelo' in l:
                continue
            c = [x.strip().replace('**', '').replace('%', '').strip() for x in l.strip().strip('|').split('|')]
            if len(c) < 4 or c[0] not in d:
                continue
            for etiq, val, clave in (('F1', c[1], 'f1'), ('P', c[2], 'precision'), ('R', c[3], 'recall')):
                mirados += 1
                try:
                    a = float(val)
                except ValueError:
                    continue
                b = d[c[0]].get(clave)
                if b is None or abs(a - b) > 0.02:
                    fallos.append('Tabla 6 %s %s: la tabla dice %.2f y el dato %s'
                                  % (c[0], etiq, a, '—' if b is None else '%.2f' % b))

    # --- Tabla 8
    raiz = _medias('results/benchmark_results.csv', ('vram_mb', 'tokens_per_sec'), escala=1.0)
    remoto = ({} if not os.path.exists(os.path.join(BENCH_DIR, 'results/gemma4_31b_n15_REMOTO/benchmark_results.csv'))
              else _medias('results/gemma4_31b_n15_REMOTO/benchmark_results.csv',
                           ('vram_mb', 'tokens_per_sec'), escala=1.0))
    MAPA8 = {'gemma4:31b': (remoto, 'gemma4:31b_baseline'),
             'gemma4:31b-mlx': (raiz, 'gemma4:31b-mlx_baseline'),
             'llama3.2 (3B)': (raiz, 'llama3.2:latest_baseline')}
    i = s.find('_Tabla 8.')
    for l in (s[i:i + 900].split('\n') if i >= 0 else []):
        if not l.startswith('|') or '---' in l or 'Modelo' in l:
            continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 3 or c[0] not in MAPA8:
            continue
        src, g = MAPA8[c[0]]
        if g not in src:
            fallos.append('Tabla 8: el grupo «%s» no esta en su corrida' % g)
            continue
        for etiq, val, clave, tol in (('VRAM', c[1].replace(',', ''), 'vram_mb', 1.0),
                                      ('Tok/s', c[2], 'tokens_per_sec', 0.02)):
            mirados += 1
            try:
                a = float(val)
            except ValueError:
                continue
            b = src[g].get(clave)
            if b is None or abs(a - b) > tol:
                fallos.append('Tabla 8 %s %s: la tabla dice %.2f y el dato %s'
                              % (c[0], etiq, a, '—' if b is None else '%.2f' % b))

    check('las tablas 5, 6 y 8 reproducen desde sus corridas', mirados, fallos,
          'con estas, todas las tablas de datos del informe quedan atadas al dato')


# --- 20. La Tabla 18 reproduce desde el analisis de mojibake -------------------------------------
ARTEFACTO_MOJIBAKE = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                        'ANALISIS_MOJIBAKE_20260908/efecto_mojibake.json')


def c_tabla18_vs_artefacto(s):
    """El efecto diferencial del mojibake, atado al fichero que lo calcula.

    Ultima tabla de datos del informe que quedaba sin contrastar. Con esta, las seis —4, 5, 6, 7, 8
    y 18—, el Anexo I y las dos figuras salen del dato y no de otra copia suya.
    """
    import json as _json
    if not os.path.exists(ARTEFACTO_MOJIBAKE):
        check('la Tabla 18 reproduce desde el analisis de mojibake', 0,
              ['no existe %s' % os.path.relpath(ARTEFACTO_MOJIBAKE, RAIZ)])
        return
    with open(ARTEFACTO_MOJIBAKE, encoding='utf-8') as fh:
        a = _json.load(fh)
    art = {f['grupo']: f for f in a.get('filas', [])}
    i = s.find('_Tabla 18.')
    if i < 0:
        check('la Tabla 18 reproduce desde el analisis de mojibake', 0, ['no se encuentra la Tabla 18'])
        return
    fallos, mirados = [], 0
    vistos = set()
    for l in s[i:i + 3500].split('\n'):
        m = re.match(r'^\|\s*`([^`]+)`\s*\|\s*([+-][\d.]+)\s*\|\s*([+-][\d.]+)\s*\|', l)
        if not m:
            continue
        cfg, x, y = m.group(1), float(m.group(2)), float(m.group(3))
        vistos.add(cfg)
        f = art.get(cfg)
        if f is None:
            fallos.append('%s no esta en el artefacto de mojibake' % cfg)
            continue
        for etiq, val, clave in (('por entidad', x, 'delta_por_entidad'),
                                 ('por texto', y, 'delta_por_texto')):
            mirados += 1
            d = f.get(clave)
            if d is None or abs(val - d) > 0.0002:
                fallos.append('Tabla 18 %s %s: la tabla dice %+.4f y el dato %s'
                              % (cfg, etiq, val, '—' if d is None else '%+.4f' % d))
    # el recuento declarado por el artefacto debe coincidir con las filas de la tabla
    if a.get('configuraciones') and a['configuraciones'] != len(vistos):
        fallos.append('el artefacto declara %s configuraciones y la tabla tiene %d'
                      % (a['configuraciones'], len(vistos)))
    check('la Tabla 18 reproduce desde el analisis de mojibake', mirados, fallos,
          'con esta, todas las tablas de datos del informe estan atadas al dato')


# --- 21. Todo JSON rastreado debe parsear -------------------------------------------------------
# Ficheros que son JSONL de forma legitima —un objeto por linea— y por tanto no parsean como JSON.
JSONL_LEGITIMOS = ('data/sample_an1.json', 'data/sample_an2.json', 'data/sample_sanctions.json')

# Ficheros rotos por el barrido de exclusion, ya diagnosticados y pendientes de decision del autor
# (FINDINGS §F70). Se avisan aparte en lugar de hacer fallar la comprobacion: una que siempre falla
# se acaba desactivando (LEARNING §L48). Retirar la entrada cuando se reparen.
JSON_ROTOS_DECLARADOS = {
    'repos/ner-llm-entity-benchmark/results/excluidos_n120_REMOTO/detailed_results.json.bak_prescore':
        '240 de 480 claves «model» sin valor; las otras 240 son de gpt-oss:20b y estan intactas',
    'repos/ner-llm-entity-benchmark/results/excluidos_n120_REMOTO/benchmark_summary.json.bak_prescore':
        'falta una clave de primer nivel, la del modelo excluido',
}


def c_json_parsea(s):
    """Un fichero de datos roto se comporta igual que uno sano hasta que alguien lo abre.

    El barrido que retiro los nombres de los modelos excluidos edito JSON por sustitucion de texto y
    dejo dos ficheros ilegibles, con `"model":` sin valor en 240 registros. Nadie lo noto porque
    nada los parseaba. Ver FINDINGS §F70.
    """
    import json as _json
    r = subprocess.run(['git', 'ls-files'], cwd=RAIZ, capture_output=True, text=True)
    fich = [l for l in r.stdout.split('\n') if l.endswith('.json') or '.json.bak' in l]
    fallos, mirados, declarados = [], 0, []
    for rel in fich:
        p = os.path.join(RAIZ, rel)
        if not os.path.isfile(p) or any(rel.endswith(j) for j in JSONL_LEGITIMOS):
            continue
        mirados += 1
        try:
            with open(p, encoding='utf-8') as fh:
                _json.load(fh)
        except Exception as e:
            if rel in JSON_ROTOS_DECLARADOS:
                declarados.append(rel)
            else:
                fallos.append('%s no parsea: %s' % (rel, str(e)[:70]))
    nota = 'los .jsonl legitimos estan declarados como excepcion en JSONL_LEGITIMOS'
    if declarados:
        nota = ('%d fichero(s) rotos ya diagnosticados y pendientes de reparar (FINDINGS §F70)'
                % len(declarados))
    check('todo JSON rastreado parsea', mirados, fallos, nota)
    if declarados:
        print('  AVISO  %d JSON rotos declarados, pendientes de decision del autor:' % len(declarados))
        for rel in declarados:
            print('           - %s' % rel)
            print('             %s' % JSON_ROTOS_DECLARADOS[rel])


# --- 22. La correlacion de capacidad, atada a su artefacto -------------------------------------
ARTEFACTO_CORR = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                    'CORRELACION_CAPACIDAD_20260908/correlacion.json')


def c_correlacion(s):
    """La rho que dibuja la Figura 2 y que cita §5.3.1, contra el fichero que la calcula.

    Estuvo un dia entero solo dentro de la imagen: el texto no la mencionaba y ningun artefacto de
    results/ la contenia. Una cifra que solo existe dentro de un PNG no se puede comprobar.
    """
    import json as _json
    if not os.path.exists(ARTEFACTO_CORR):
        check('la correlacion de capacidad reproduce desde su artefacto', 0,
              ['no existe %s' % os.path.relpath(ARTEFACTO_CORR, RAIZ)])
        return
    with open(ARTEFACTO_CORR, encoding='utf-8') as fh:
        a = _json.load(fh)
    rho, p = a['spearman']['rho'], a['spearman']['p']
    pe, pp = a['pearson']['r'], a['pearson']['p']
    fallos, mirados = [], 0
    for etiq, valor in (('Spearman', '%.4f' % rho), ('p de Spearman', '%.4f' % p),
                        ('Pearson', '%.4f' % pe), ('p de Pearson', '%.4f' % pp)):
        mirados += 1
        esp = valor.replace('.', ',').replace('-', '−')
        if esp.lstrip('−').rstrip('0').rstrip(',') not in s.replace('.', ',') and esp not in s:
            fallos.append('§5.3.1 no cita %s = %s' % (etiq, esp))
    mirados += 1
    try:
        sc = open(SCRIPT_FIGURAS, encoding='utf-8').read()
        if ('%.4f' % rho).replace('.', ',').lstrip('-') not in sc:
            fallos.append('generar_figuras_informe.py no usa rho = %.4f' % rho)
    except Exception as e:
        fallos.append('no se puede leer el script de figuras: %s' % e)
    # los dos coeficientes discrepan: el informe debe declararlo, no elegir uno
    mirados += 1
    if a['spearman']['significativo_005'] != a['pearson']['significativo_005']:
        if 'discrepan' not in s:
            fallos.append('los dos coeficientes discrepan en el veredicto y §5.3.1 no lo declara')
    check('la correlacion de capacidad reproduce desde su artefacto', mirados, fallos,
          'una cifra que solo vive dentro de un PNG no se puede comprobar')


# --- 23. La taxonomia de errores (§5.4) reproduce desde los datos --------------------------------
def c_alucinaciones(s):
    """Las cinco cifras de alucinacion de §5.4, contra la poblacion que el propio parrafo declara.

    §5.4 no habla de los 26 grupos publicados sino de los 61 «que aportan los ciento veinte registros
    completos, contando todas las corridas conservadas». Comprobarlo contra el consolidado da un falso
    positivo: el maximo de 21,59 % es de una configuracion de RAG por diccionario que el consolidado
    no incluye. La poblacion hay que tomarla de donde el texto dice.
    """
    import csv as _csv
    import collections as _c
    import glob as _glob
    g = {}
    rutas = _glob.glob(os.path.join(BENCH_DIR, 'results/*/benchmark_results.csv'))
    rutas.append(os.path.join(BENCH_DIR, 'results/benchmark_results.csv'))
    for f in rutas:
        if not os.path.exists(f):
            continue
        por = _c.defaultdict(list)
        try:
            with open(f, encoding='utf-8') as fh:
                for r in _csv.DictReader(fh):
                    v = r.get('hallucination_rate')
                    if v not in (None, ''):
                        por[r['model']].append(float(v))
        except Exception:
            continue
        for k, v in por.items():
            if len(v) == 120:
                g[(os.path.basename(os.path.dirname(f)), k)] = 100 * sum(v) / len(v)
    fallos, mirados = [], 0
    mirados += 1
    if len(g) != 61:
        fallos.append('§5.4 declara 61 grupos de 120 registros y se encuentran %d' % len(g))
    if g:
        mirados += 1
        mx = max(g.values())
        if abs(mx - 21.59) > 0.011:
            fallos.append('el maximo de alucinacion es %.2f %% y §5.4 dice 21,59 %%' % mx)
        mirados += 1
        bajo = sum(1 for v in g.values() if v < 1.0)
        if bajo != 28:
            fallos.append('§5.4 dice que 28 grupos quedan por debajo del 1 %% y son %d' % bajo)
    check('la taxonomia de errores de §5.4 reproduce desde los datos', mirados, fallos,
          'la poblacion son los 61 grupos con 120 registros, no los 26 publicados')


# --- 24. El indice de defensa cita cifras que sus artefactos respaldan -------------------------
DEFENSA = os.path.join(RAIZ, 'DEFENSA-PREGUNTAS-Y-RESPUESTAS.md')
RES = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results')


def c_defensa(s):
    """Las cifras del indice de defensa, contra los artefactos que las calculan.

    Ese documento existe para responder en la sala sin recalcular nada, de modo que una cifra suya
    que haya dejado de ser cierta es peor que no tenerla. Cuando la re-corrida sustituya los datos
    esta comprobacion fallara, y eso es lo que se busca: obliga a actualizarlo.
    """
    import json as _json
    if not os.path.exists(DEFENSA):
        check('el indice de defensa cita cifras respaldadas', 0, ['no existe DEFENSA-PREGUNTAS-Y-RESPUESTAS.md'])
        return
    d = open(DEFENSA, encoding='utf-8').read()

    def carga(rel):
        p = os.path.join(RES, rel)
        return _json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None

    fr = carga('ROBUSTEZ_ESTADISTICA_20260908/friedman.json')
    co = carga('CORRELACION_CAPACIDAD_20260908/correlacion.json')
    ph = carga('ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json')
    fp = carga('COMPOSICION_FP_20260908/composicion_fp_26_grupos.json')
    fallos, mirados = [], 0
    esperadas = []
    if fr:
        esperadas.append(('chi2 de Friedman', '{:,.2f}'.format(fr['friedman_medidas_repetidas']['chi2'])
                          .replace(',', ' ').replace('.', ',')))
    if co:
        esperadas += [('rho de Spearman', '%.4f' % abs(co['spearman']['rho'])).__class__ and
                      ('rho de Spearman', ('%.4f' % abs(co['spearman']['rho'])).replace('.', ',')),
                      ('p de Spearman', ('%.4f' % co['spearman']['p']).replace('.', ',')),
                      ('r de Pearson', ('%.4f' % abs(co['pearson']['r'])).replace('.', ',')),
                      ('p de Pearson', ('%.4f' % co['pearson']['p']).replace('.', ','))]
    # En prosa espanola un recuento pequeno se escribe con letra, y eso es correcto: el verificador
    # debe aceptar ambas formas en lugar de obligar al documento a escribir digitos.
    LETRA = {0: 'cero', 1: 'uno', 2: 'dos', 3: 'tres', 4: 'cuatro', 5: 'cinco', 6: 'seis', 7: 'siete',
             8: 'ocho', 9: 'nueve', 10: 'diez', 11: 'once', 12: 'doce', 13: 'trece', 14: 'catorce',
             15: 'quince', 16: 'dieciseis', 20: 'veinte', 26: 'veintiseis'}

    def formas(n_):
        f_ = ['%d' % n_]
        if n_ in LETRA:
            f_.append(LETRA[n_])
        return f_

    if ph:
        a_, b_ = ph['significativos_pareado'], ph['n_comparaciones']
        alt = ['%s de %s' % (x, y) for x in formas(a_) for y in formas(b_)]
        esperadas.append(('significativos del post-hoc pareado', alt))
    if fp:
        esperadas += [('falsos positivos de Locations',
                       '{:,}'.format(fp['fp_locations']).replace(',', ' ')),
                      ('falsos positivos totales',
                       '{:,}'.format(fp['fp_total']).replace(',', ' '))]
    for etiq, val in esperadas:
        mirados += 1
        opciones = val if isinstance(val, list) else [val]
        if not any(o in d for o in opciones):
            fallos.append('el indice no cita %s = %s' % (etiq, ' o '.join(opciones[:2])))
    check('el indice de defensa cita cifras respaldadas por sus artefactos', mirados, fallos,
          'fallara cuando la re-corrida cambie los datos, y entonces hay que actualizarlo')


# --- 25. Extension del cuerpo frente al limite institucional ------------------------------------
DENSIDAD = 684        # palabras por pagina, medida sobre el PDF entregado al profesor guia
CUERPO_ENTREGADO = 14842   # palabras del cuerpo en la version entregada (commit 6299d13)
PAGINAS_ENTREGADO = 20     # paginas que ocupaba ese cuerpo, contadas sobre el PDF
LIMITE = 25


def frontera_anexos(L):
    """Primer encabezado de anexo, sea cual sea su nivel.

    Criterio unico y explicito porque no serlo ya produjo una cifra falsa: un detector que solo
    reconocia «## Anexos» conto el documento entero como cuerpo en una version que usaba
    «### Anexo A», y dio un crecimiento negativo de 2.673 palabras que no existia.
    """
    for k, l in enumerate(L):
        if re.match(r'^#{2,4}\s*(Anexos?\b|Anexo\s+[A-I]\b)', l.strip(), re.I):
            return k
    return len(L)


def c_extension(s):
    """El cuerpo no puede exceder 25 paginas. La estimacion se declara como tal."""
    L = s.split('\n')
    i = frontera_anexos(L)
    cuerpo = len(' '.join(L[:i]).split())
    pags = PAGINAS_ENTREGADO + (cuerpo - CUERPO_ENTREGADO) / DENSIDAD
    fallos = []
    if i == len(L):
        fallos.append('no se encuentra el comienzo de los anexos: la estimacion no vale')
    elif pags > LIMITE:
        fallos.append('el cuerpo estimado son %.1f paginas y el limite institucional es %d' % (pags, LIMITE))
    check('el cuerpo cabe en el limite de %d paginas' % LIMITE, 1, fallos,
          'estimacion: %d palabras -> ~%.1f pp; margen %d palabras. No sustituye a contar el PDF'
          % (cuerpo, pags, int((LIMITE - pags) * DENSIDAD)))


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
    c_protocolo(s)
    c_anexo_vs_tabla7(s)
    c_tabla7_vs_datos(s)
    c_tabla4_vs_datos(s)
    c_figura1_vs_artefacto(s)
    c_tablas_menores(s)
    c_tabla18_vs_artefacto(s)
    c_json_parsea(s)
    c_correlacion(s)
    c_alucinaciones(s)
    c_defensa(s)
    c_extension(s)
    if '--red' in sys.argv:
        c_urls(s)

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
