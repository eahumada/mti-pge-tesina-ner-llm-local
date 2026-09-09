#!/usr/bin/env python3
"""Comprobaciones mecánicas del informe final y del repositorio.

Cada comprobación declara **cuántos elementos examinó**. Una que examina cero elementos se marca como
VACÍA y no como superada: este proyecto ya dio por buena una prueba de sensibilidad que no podía marcar
nada por construcción (§5.3 del informe), y una comprobación que no mira nada es indistinguible de una
que pasa.

Uso:  python3 tools/verificar_informe.py            # todas
      python3 tools/verificar_informe.py --breve    # solo lo que falla
      python3 tools/verificar_informe.py --red      # además comprueba las URL en red
      python3 tools/verificar_informe.py --estricto # los fallos declarados también cortan
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

# Fallos conocidos, con quien los tiene y desde cuando. La clave es un fragmento del texto del
# fallo; si aparece, se cuenta como DECLARADO y no como nuevo. Sin esto el resumen decia «4 fallos»
# sin distinguir los deliberados de los inesperados, y **un fallo nuevo se habria perdido entre
# ellos** — que es el mismo defecto que tener una cifra sin contexto.
#
# Retirar una entrada de aqui en cuanto se resuelva: una lista de excepciones que nadie poda acaba
# silenciando defectos de verdad.
FALLOS_DECLARADOS = {
    '.rebuild_venv.log': 'fichero vacio del commit 880f4f9; decision del autor (CURRENT-TASKS §1.103)',
    '.restore_results.log': 'idem',
    'cita 62.67': 'decision 13, pendiente del autor (FINDINGS §F87)',
    'cita 80.51': 'decision 13, pendiente del autor (FINDINGS §F87)',
    'el Anexo I dice': 'decision 13, ampliada a la tercera instancia del defecto '
                       '(FINDINGS §F87.bis)',
    'github.com/eahumada/mti-pge-tesina': 'referencia [37]: el repositorio es privado hasta la purga '
                                          '(SEGURIDAD-CLAVE-GOOGLE-20260908.md)',
}

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


# --- 2.bis. Referencias a anexos y a tablas -----------------------------------------------------
def c_refs_anexos_tablas(s):
    """Toda llamada a «Anexo X» y a «Tabla N» debe apuntar a algo que exista.

    `CLAUDE.md` lo exige junto con las referencias §x.y, pero solo estas ultimas se comprobaban.
    Verificado por mutacion el 2026-09-09: insertar «el **Anexo Z**» o «la **Tabla 44**» en el
    informe **no lo detectaba nada**, mientras «§9.9» si fallaba. Es el hueco de una comprobacion
    que existia a medias, que es peor que no tenerla, porque su nombre sugiere cobertura completa.
    """
    anexos_hay = set(re.findall(r'^#{2,4}\s*Anexo\s+([A-Z])\b', s, re.M))
    anexos_cit = set(re.findall(r'Anexo\s+([A-Z])\b', s))
    tablas_hay = set(re.findall(r'^_Tabla (\d+)\.', s, re.M))
    tablas_cit = set(re.findall(r'Tabla\s+(\d+)\b', s))
    fallos = ['se cita el Anexo %s y no existe' % a for a in sorted(anexos_cit - anexos_hay)]
    fallos += ['se cita la Tabla %s y no existe' % n
               for n in sorted(tablas_cit - tablas_hay, key=lambda x: int(x))]
    check('referencias a Anexo X y a Tabla N con destino existente',
          len(anexos_cit) + len(tablas_cit), fallos,
          'CLAUDE.md las exige igual que las §x.y, y antes solo se comprobaban estas')


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
DOCX_ENTREGABLES = (
    'Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx',
    'Informe_Final_Tesina_NER.docx',
    'doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx',
)


def _texto_docx(ruta):
    """Texto visible de un .docx, uniendo cada <w:t> con un espacio.

    OJO: `<w:t[^>]*>` tambien encaja con `<w:tcPr>` y arrastra XML al texto (§F88). Hay que
    exigir que tras `w:t` venga `>` o un espacio.
    """
    import zipfile
    with zipfile.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    return ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))


def c_excluidos(s):
    """Los modelos excluidos no pueden aparecer, y la regla alcanza a los `.docx`, no solo al `.md`.

    Hasta el 2026-09-09 esta comprobacion miraba **solo el Markdown** y daba «ok» mientras los tres
    `.docx` —el entregable canonico incluido— nombraban **cuatro** modelos excluidos en **quince**
    sitios. La exclusion se habia aplicado a la fuente y nunca se propago. Es §L47 en su version
    mas caro: la comprobacion existia, pasaba, y examinaba el artefacto que no se entrega.

    Ver `FINDINGS §F94` para el inventario exacto de las cuatro clases de aparicion.
    """
    fallos = []
    b = s.lower()
    mirados = len(EXCLUIDOS)
    fallos += ['el Markdown: aparece «%s»' % e for e in EXCLUIDOS if e in b]
    for rel in DOCX_ENTREGABLES:
        ruta = os.path.join(RAIZ, rel)
        mirados += 1
        if not os.path.exists(ruta):
            fallos.append('no existe el entregable %s' % rel)
            continue
        try:
            td = _texto_docx(ruta).lower()
        except Exception as e:                                    # noqa: BLE001
            fallos.append('%s no se puede leer: %s' % (os.path.basename(rel), e))
            continue
        for e in EXCLUIDOS:
            mirados += 1
            n = td.count(e)
            if n:
                fallos.append('%s: aparece «%s» %d vez/veces'
                              % (os.path.basename(rel), e, n))
    check('sin modelos excluidos del estudio, en el .md y en los tres .docx', mirados, fallos,
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
                   'apartado «Corridas múltiples». **Ya resuelto en la re-corrida**, comprobado el '
                   '2026-09-09: las 39 corridas de recorrida_20260908/ declaran max_tokens=4096 sin '
                   'una sola excepción. La divergencia sigue siendo real en el consolidado PUBLICADO, '
                   'que es lo que esta comprobación lee, y esta entrada se retira en cuanto se rehaga '
                   'el consolidado desde la re-corrida. Ver FINDINGS §F61.bis'),
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
    # Una fila que deje de casar con el patron salia en silencio de la comprobacion, que seguia
    # diciendo «ok» con menos elementos. Comprobado por mutacion el 2026-09-09 sobre la fila de
    # `gemma4:31b-cloud`: el recuento bajaba de 26 a 24 y la comprobacion pasaba igual. Es la
    # tabla central del trabajo, de modo que una fila suya sin verificar es lo peor que puede
    # pasar aqui. Por eso se cuentan aparte las filas que parecen de datos y no se pueden leer.
    t7, ilegibles = {}, []
    for l in s[i:i + 3000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|', l)
        if m and not m.group(1).startswith('Modelo'):
            t7[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
            continue
        celdas = [x.strip() for x in l.strip().strip('|').split('|')]
        if (l.startswith('|') and '---' not in l and len(celdas) == 5
                and celdas[0] and not celdas[0].startswith('Modelo')):
            ilegibles.append('%s: no se pueden leer sus dos porcentajes (%s | %s)'
                             % (celdas[0], celdas[1], celdas[2]))
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
    check('la Tabla 7 reproduce desde el CSV consolidado',
          2 * (len(t7) + len(ilegibles)), ilegibles + fallos,
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
    # Toda fila de datos tiene que parsearse. Sin esta cuenta, una fila que dejara de ser legible
    # —un numero reformateado, un `%` perdido— salia en silencio de la comprobacion, que seguia
    # diciendo «ok» con menos elementos. Comprobado por mutacion el 2026-09-09: cambiar «74.44%»
    # por «74,44 %» bajaba el recuento de 52 a 48 y la comprobacion pasaba igual.
    filas, ilegibles = [], []
    for l in s[i:i + 3000].split('\n'):
        if not l.startswith('|') or 'Modelo' in l or '---' in l:
            continue
        c = [x.strip().replace('**', '') for x in l.strip().strip('|').split('|')]
        if len(c) < 7:
            continue
        try:
            filas.append((c[0],) + tuple(float(x.rstrip('%').replace(',', '.')) for x in c[3:7]))
        except ValueError:
            ilegibles.append('%s: no se pueden leer sus cuatro metricas (%s)'
                             % (c[0] or '(fila sin nombre)', ' | '.join(c[3:7])))
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
    check('la Tabla 4 reproduce desde sus corridas de origen',
          4 * (len(filas) + len(ilegibles)), ilegibles + fallos,
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
                    # No basta con saltar: `mirados` ya ha subido, de modo que el valor quedaria
                    # sin comparar y el recuento no lo delataria. Ver `FINDINGS §F82`.
                    fallos.append('Tabla 5 %s %s: el valor «%s» no se puede leer'
                                  % (c[0], etiq, val))
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
            if len(c) < 4:
                continue
            if c[0] not in d:
                # Antes se saltaba en silencio: renombrar una fila la sacaba de la comprobacion
                # sin dejar rastro, porque `mirados` ni siquiera llegaba a subir. `FINDINGS §F82`.
                mirados += 1
                fallos.append('Tabla 6: la fila «%s» no corresponde a ningun grupo de la corrida'
                              % c[0])
                continue
            for etiq, val, clave in (('F1', c[1], 'f1'), ('P', c[2], 'precision'), ('R', c[3], 'recall')):
                mirados += 1
                try:
                    a = float(val)
                except ValueError:
                    fallos.append('Tabla 6 %s %s: el valor «%s» no se puede leer'
                                  % (c[0], etiq, val))
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
        if len(c) < 3 or not c[0]:
            continue
        if c[0] not in MAPA8:
            mirados += 1
            fallos.append('Tabla 8: la fila «%s» no esta en el mapa de correspondencias' % c[0])
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
                fallos.append('Tabla 8 %s %s: el valor «%s» no se puede leer' % (c[0], etiq, val))
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
    # Las tres cifras se LEEN de §5.4 en lugar de estar escritas aqui. Antes eran constantes —61,
    # 21.59 y 28— copiadas del informe al escribir la comprobacion, de modo que detectaba una
    # deriva de los datos pero **no** una del informe: comprobado por mutacion el 2026-09-09,
    # cambiar «21,59» por «21,99» en el texto no lo notaba nadie. Y los mensajes decian «y §5.4
    # dice 21,59 %» sin haber leido §5.4 nunca.
    PAL = {'cero': 0, 'una': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6,
           'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10, 'veintiocho': 28, 'veintinueve': 29,
           'sesenta y un': 61, 'sesenta y uno': 61, 'sesenta y dos': 62, 'sesenta y tres': 63}

    def num(txt):
        txt = txt.strip().lower()
        if re.fullmatch(r'\d+', txt):
            return int(txt)
        return PAL.get(txt)

    # Se ancla en la propia frase y no en un encabezado: buscar «## 5.4» seleccionaba otro bloque y
    # la expresion casaba con «El primero de esos dos casos», que no tiene nada que ver.
    m_max = re.search(r'el rango va de \*\*\w+\*\*.{0,120}?al \*\*(\d+,\d+) ?%\*\*', s, re.S)
    m_cnt = re.search(r'y ([\wáéíóú ]+?) de esos ([\wáéíóú ]+?) grupos quedan por debajo del \*\*1 ?%\*\*',
                      s, re.S)
    esp_max = float(m_max.group(1).replace(',', '.')) if m_max else None
    esp_bajo = num(m_cnt.group(1)) if m_cnt else None
    esp_grupos = num(m_cnt.group(2)) if m_cnt else None
    if esp_max is None or esp_bajo is None or esp_grupos is None:
        fallos.append('no se pueden leer de §5.4 las tres cifras que esta comprobacion ata al dato '
                      '(maximo de alucinacion, grupos por debajo del 1 %% y total de grupos); '
                      'leidas: max=%s bajo=%s grupos=%s' % (esp_max, esp_bajo, esp_grupos))
        esp_max, esp_bajo, esp_grupos = 21.59, 28, 61

    if len(g) != esp_grupos:
        fallos.append('§5.4 declara %s grupos de 120 registros y se encuentran %d'
                      % (esp_grupos, len(g)))
    if g:
        mirados += 1
        mx = max(g.values())
        if abs(mx - esp_max) > 0.011:
            fallos.append('el maximo de alucinacion es %.2f %% y §5.4 dice %s %%' % (mx, esp_max))
        mirados += 1
        bajo = sum(1 for v in g.values() if v < 1.0)
        if bajo != esp_bajo:
            fallos.append('§5.4 dice que %s grupos quedan por debajo del 1 %% y son %d'
                          % (esp_bajo, bajo))
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

    # Cada artefacto ausente es un FALLO, no un silencio. Sin esto, el bloque `if fr:` se saltaba sus
    # cifras y la comprobacion seguia diciendo «ok» con menos elementos: comprobado el 2026-09-09,
    # escondiendo `correlacion.json` bajaba de 13 a 9 y pasaba igual. La autoprueba no lo veia porque
    # OTRAS comprobaciones leen esos mismos ficheros y si fallaban. Es el defecto de §L47 y §F82.
    fallos, mirados = [], 0
    FUENTES = [('friedman', 'ROBUSTEZ_ESTADISTICA_20260908/friedman.json'),
               ('correlacion', 'CORRELACION_CAPACIDAD_20260908/correlacion.json'),
               ('post-hoc pareado', 'ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json'),
               ('composicion de falsos positivos', 'COMPOSICION_FP_20260908/composicion_fp_26_grupos.json'),
               ('robustez de la re-corrida', 'ROBUSTEZ_ESTADISTICA_20260909/robustez.json')]
    cargados = {}
    for nombre, rel in FUENTES:
        mirados += 1
        cargados[rel] = carga(rel)
        if cargados[rel] is None:
            fallos.append('falta el artefacto de %s (%s), del que el indice toma cifras' % (nombre, rel))
    fr = cargados['ROBUSTEZ_ESTADISTICA_20260908/friedman.json']
    co = cargados['CORRELACION_CAPACIDAD_20260908/correlacion.json']
    ph = cargados['ROBUSTEZ_ESTADISTICA_20260908/posthoc_pareado.json']
    fp = cargados['COMPOSICION_FP_20260908/composicion_fp_26_grupos.json']
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
    # Las cifras de la re-corrida, que son las que el indice cita primero desde el 2026-09-09.
    # Se anaden porque el error de escribir «dos modelos significativos» cuando son tres estuvo en
    # ese documento y no lo detecto nada: la comprobacion solo miraba los artefactos antiguos.
    rb = cargados['ROBUSTEZ_ESTADISTICA_20260909/robustez.json']
    if rb:
        co2 = rb.get('correlacion_capacidad_beneficio') or {}
        mi = rb.get('modelo_mas_influyente')
        inf = (rb.get('influencia_al_retirar_cada_modelo') or {}).get(mi or '', {})
        if co2:
            esperadas += [
                ('rho de Spearman de la re-corrida',
                 ('%.4f' % abs(co2['spearman']['rho'])).replace('.', ',')),
                ('p de Spearman de la re-corrida',
                 ('%.4f' % co2['spearman']['p']).replace('.', ',')),
                ('r de Pearson de la re-corrida',
                 ('%.4f' % abs(co2['pearson']['r'])).replace('.', ',')),
            ]
        if inf:
            esperadas.append(('Pearson al retirar el punto mas influyente',
                              ('%.4f' % abs(inf['pearson_r'])).replace('.', ',')))
        if rb.get('significativos_pareado') is not None:
            # Un recuento NO se comprueba por presencia de la palabra: «tres» aparece muchas veces en
            # el documento por otros motivos, de modo que la comprobacion pasaria aunque la frase
            # dijera «dos». Comprobado por mutacion el 2026-09-09, que es como se descubrio: hay que
            # exigir que el numero este JUNTO a «significativ», en la misma oracion.
            n_ = rb['significativos_pareado']
            patron = r'(?:%s)\b[^.]{0,120}significativ|significativ[^.]{0,120}\b(?:%s)\b' % (
                '|'.join(formas(n_)), '|'.join(formas(n_)))
            mirados += 1
            if not re.search(patron, d, re.I):
                fallos.append('el indice no dice que los significativos de la re-corrida son %d, '
                              'o no lo dice junto a la palabra' % n_)

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


def c_fuentes_de_los_grupos(_s):
    """Cada grupo de la composicion de falsos positivos se lee de la corrida que el consolidado usa.

    Ocho de los veintiseis grupos aparecen en dos fuentes del manifiesto, y el consolidado se queda
    con la primera (`--on-duplicate=first`). Leer la ultima produce cifras plausibles calculadas
    sobre corridas superadas, sin error ni aviso: paso el 2026-09-08 y se leyo `gpt-oss:20b` desde
    un directorio llamado `excluidos`. El control es externo —comparar la media de cada grupo con la
    del CSV consolidado, que se produjo por otra via— porque leer el codigo no lo destapo.
    Ver `FINDINGS §F81.bis`.
    """
    import json as _json
    if not os.path.exists(ARTEFACTO_FP):
        check('cada grupo se lee de la corrida que el consolidado usa', 0,
              ['no existe %s' % os.path.relpath(ARTEFACTO_FP, RAIZ)])
        return
    with open(ARTEFACTO_FP, encoding='utf-8') as fh:
        a = _json.load(fh)
    descuadres = a.get('grupos_que_no_reproducen_el_consolidado')
    if descuadres is None:
        check('cada grupo se lee de la corrida que el consolidado usa', 0,
              ['el artefacto no declara el control; regenerar con tools/composicion_fp.py'])
        return
    mirados = len(a.get('detalle') or {})
    check('cada grupo se lee de la corrida que el consolidado usa', mirados, list(descuadres))


def c_agregacion(s):
    """Las cifras de la conclusion 1 usan la agregacion que §3.3 declara: macro, por articulo.

    §3.3 dice que agregar dentro de cada articulo y promediar entre articulos es la **unica**
    convencion del trabajo, y advierte de que la alternativa daria «62,67 % frente al 59,25 % que
    aqui se publica». La conclusion 1, sin embargo, presenta el **62,67** y el **80,51** como los
    equivalentes de sus cifras restringidas, y esos dos son **micro**: mezcla las dos agregaciones
    y las llama equivalentes. Ver `FINDINGS §F87` y la **decision 13**.

    Esta comprobacion **falla a proposito** mientras el autor no decida, igual que la referencia [37]
    falla hasta que se complete la purga. Su mensaje dice que sustituir.
    """
    import json as _json
    if not os.path.exists(MANIFIESTO):
        check('la conclusion 1 usa la agregacion declarada en §3.3', 0,
              ['no existe el manifiesto, del que sale la corrida de referencia'])
        return
    with open(MANIFIESTO, encoding='utf-8') as fh:
        srcs = _json.load(fh)['sources']
    d120 = next((os.path.dirname(x['csv_path']) for x in srcs
                 if 'gemma4:31b-mlx_baseline' in x.get('models', [])), None)
    CASOS = ((d120, 'gemma4:31b-mlx_baseline', 'N=120'),
             ('results/n30_rerun_REMOTO', 'gemma4:31b-mlx', 'dominio'))
    fallos, mirados = [], 0
    agreg = {}
    for rel, grupo, etiq in CASOS:
        mirados += 1
        if rel is None:
            fallos.append('el manifiesto no dice de que corrida sale %s' % etiq)
            continue
        ruta = os.path.join(BENCH_DIR, rel, 'detailed_results.json')
        if not os.path.exists(ruta):
            fallos.append('no existe %s, de donde salen las cifras de %s' % (rel, etiq))
            continue
        with open(ruta, encoding='utf-8') as fh:
            R = [r for r in _json.load(fh) if r.get('model') == grupo]
        if not R:
            fallos.append('%s no trae el grupo %s' % (rel, grupo))
            continue
        T3 = ('Persons', 'Organizations', 'Locations')

        def _macro(cats):
            v = []
            for r in R:
                pt = ((r.get('metrics') or {}).get('per_type')) or {}
                tp = sum((pt.get(c, {}).get('tp', 0) or 0) for c in cats)
                fp = sum((pt.get(c, {}).get('fp', 0) or 0) for c in cats)
                fn = sum((pt.get(c, {}).get('fn', 0) or 0) for c in cats)
                if tp + fp + fn == 0:
                    v.append(1.0)
                    continue
                pr = tp / (tp + fp) if tp + fp else 0.0
                rc = tp / (tp + fn) if tp + fn else 0.0
                v.append(2 * pr * rc / (pr + rc) if pr + rc else 0.0)
            return 100 * sum(v) / len(v)

        def _micro(cats):
            TP = FP = FN = 0
            for r in R:
                pt = ((r.get('metrics') or {}).get('per_type')) or {}
                for c in cats:
                    TP += pt.get(c, {}).get('tp', 0) or 0
                    FP += pt.get(c, {}).get('fp', 0) or 0
                    FN += pt.get(c, {}).get('fn', 0) or 0
            pr = TP / (TP + FP) if TP + FP else 0.0
            rc = TP / (TP + FN) if TP + FN else 0.0
            return 100 * 2 * pr * rc / (pr + rc) if pr + rc else 0.0

        ma, mi = _macro(T3), _micro(T3)
        agreg[etiq] = (ma, mi)
        # la conclusion 1 debe citar la macro; si cita la micro, esta mezclando agregaciones
        i7 = s.find('1. **Viabilidad demostrada')
        concl = s[i7:i7 + 1200] if i7 >= 0 else ''
        mirados += 1
        pat_mi = r'%s[.,]%s' % (int(mi), ('%.2f' % mi).split('.')[1])
        pat_ma = r'%s[.,]%s' % (int(ma), ('%.2f' % ma).split('.')[1])
        if re.search(pat_mi, concl):
            fallos.append('la conclusion 1 cita %.2f (micro) para %s; la convencion declarada da '
                          '%.2f (macro). Sustituir. Ver FINDINGS §F87 y la decision 13'
                          % (mi, etiq, ma))
        elif not re.search(pat_ma, concl):
            fallos.append('la conclusion 1 no cita ni %.2f (macro) ni %.2f (micro) para %s: '
                          'revisar de donde sale su cifra' % (ma, mi, etiq))
    # El Anexo I empareja la cifra restringida con su cifra publicada: «pasa de X % a 76,55 %».
    # Esa X debe ser la macro, porque el 76,55 sale de la Tabla 19, que es macro. Si es la micro,
    # el propio Anexo hace lo que §3.3 advierte que no se haga: incomparables el texto y su tabla.
    if 'N=120' in agreg:
        ma, mi = agreg['N=120']
        mirados += 1
        m = re.search(r'pasa de\s+(\d+)[.,](\d+)\s*%\s*a\s*\*{0,2}(\d+)[.,](\d+)', s)
        if m is None:
            fallos.append('no se encuentra en el Anexo I la frase «pasa de X % a Y %» que empareja '
                          'la cifra publicada con la restringida: revisar si se reformulo')
        else:
            x = float('%s.%s' % (m.group(1), m.group(2)))
            if abs(x - mi) < 0.01:
                fallos.append('el Anexo I dice «pasa de %.2f %%» (micro) y lo empareja con el %s,%s '
                              'restringido, que sale de la Tabla 19 y es macro; la convencion da '
                              '%.2f. Es el mismo defecto que la conclusion 1, en otro sitio. '
                              'Ver FINDINGS §F87.bis y la decision 13'
                              % (x, m.group(3), m.group(4), ma))
            elif abs(x - ma) >= 0.01:
                fallos.append('el Anexo I dice «pasa de %.2f %%», que no es ni la macro (%.2f) ni la '
                              'micro (%.2f): revisar de donde sale' % (x, ma, mi))
    check('la conclusion 1 usa la agregacion declarada en §3.3', mirados, fallos,
          'falla a proposito hasta que se resuelva la decision 13, como el [37] hasta la purga')


def _betacf(a, b, x):
    """Fraccion continua de la beta incompleta, metodo de Lentz."""
    TINY, EPS, MAXIT = 1e-300, 3e-16, 500
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < TINY:
        d = TINY
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = TINY if abs(d) < TINY else d
        c = 1.0 + aa / c
        c = TINY if abs(c) < TINY else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = TINY if abs(d) < TINY else d
        c = 1.0 + aa / c
        c = TINY if abs(c) < TINY else c
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < EPS:
            break
    return h


def _f_sf(F, df1, df2):
    """P(X > F) con X ~ F(df1, df2), por la beta incompleta regularizada."""
    import math
    if F <= 0:
        return 1.0
    a, b, x = df2 / 2.0, df1 / 2.0, df2 / (df2 + df1 * F)
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lb = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
          + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1.0) / (a + b + 2.0):
        return math.exp(lb) * _betacf(a, b, x) / a
    return 1.0 - math.exp(lb) * _betacf(b, a, 1.0 - x) / b


SUPER = {'\u2070': '0', '\u00b9': '1', '\u00b2': '2', '\u00b3': '3', '\u2074': '4',
         '\u2075': '5', '\u2076': '6', '\u2077': '7', '\u2078': '8', '\u2079': '9',
         '\u207b': '-'}


def _exp_super(txt):
    """Convierte un exponente escrito en superindices unicode a entero. '\u207b\u00b9\u2076\u2070' -> -160."""
    s = ''.join(SUPER.get(c, '') for c in txt)
    try:
        return int(s)
    except ValueError:
        return None


def _grupos_f1(csv_path):
    """f1 por grupo desde un CSV de resultados. Guarda `is not None`, no `if v`."""
    import csv as _csv
    from collections import defaultdict as _dd
    g = _dd(list)
    with open(csv_path, encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            v = r.get('f1')
            if v is not None and v != '':
                g[r['model']].append(float(v))
    return g


def _anova_una_via(g):
    """(F, df1, df2, p, eta2, k, N) del ANOVA de una via sobre los grupos dados."""
    k = len(g)
    N = sum(len(v) for v in g.values())
    gran = sum(x for v in g.values() for x in v) / N
    ssb = sum(len(v) * (sum(v) / len(v) - gran) ** 2 for v in g.values())
    ssw = sum((x - sum(v) / len(v)) ** 2 for v in g.values() for x in v)
    df1, df2 = k - 1, N - k
    F = (ssb / df1) / (ssw / df2)
    return F, df1, df2, _f_sf(F, df1, df2), ssb / (ssb + ssw), k, N


def c_anova(s):
    """El ANOVA titular se recalcula desde el CSV, no se cita del informe de la corrida.

    §5 publica «El ANOVA de una via sobre los veintiseis grupos arroja **F = 38,2222** con
    p = 3,4453 x 10^-160». Es **el resultado estadistico principal del trabajo** y, hasta hoy,
    ninguna de las comprobaciones lo recalculaba: la 16 comprueba que el protocolo de las corridas
    fusionadas sea homogeneo y la 18 que la Tabla 7 reproduzca, pero la F y la p no las tocaba
    nadie. Es §F91 otra vez, en la cifra que mas pesa.

    Se recalcula con la biblioteca estandar, por lo mismo que Levene: `scipy` solo esta en el venv
    del proyecto. Contrastado contra scipy el 2026-09-09: las dos vias dan F = 38,2222 y
    p = 3,445331e-160, y la beta incompleta no se desborda a esa magnitud.

    Se comprueba tambien contra el `statistical_report.md` del consolidado, que es el que
    `tools/generar_tabla7.py` lee, y contra el numero de grupos que el informe declara en palabras.
    """
    cons = os.path.join(BENCH_DIR, 'results/ANALISIS_CONJUNTO_20260907')
    csv_path = os.path.join(cons, 'merged_results.csv')
    if not os.path.exists(csv_path):
        check('el ANOVA titular se recalcula desde el CSV', 0, ['no existe %s' % csv_path])
        return
    g = _grupos_f1(csv_path)
    if not g:
        check('el ANOVA titular se recalcula desde el CSV', 0,
              ['el CSV fusionado no trae ninguna f1 legible'])
        return
    F, df1, df2, pv, eta2, k, N = _anova_una_via(g)
    fallos, mirados = [], 0

    # 1) la F que publica el informe
    mirados += 1
    m = re.search(r'ANOVA de una v\u00eda sobre los \w+ grupos arroja \*\*F = (\d+),(\d+)\*\*', s)
    if m is None:
        fallos.append('no se encuentra en el informe la frase del ANOVA con su F: '
                      'revisar si se reformulo')
    else:
        pub = float('%s.%s' % (m.group(1), m.group(2)))
        if abs(pub - F) >= 5e-5:
            fallos.append('el informe publica F = %s y el CSV da %.4f' % (pub, F))

    # 2) la p, con el exponente en superindices
    mirados += 1
    m = re.search(r'p = (\d+),(\d+) \u00d7 10([\u2070-\u2079\u00b9\u00b2\u00b3\u207b]+)', s)
    if m is None:
        fallos.append('no se encuentra en el informe la p del ANOVA en notacion cientifica')
    else:
        mant = float('%s.%s' % (m.group(1), m.group(2)))
        ex = _exp_super(m.group(3))
        if ex is None:
            fallos.append('no se puede leer el exponente de la p del ANOVA: %r' % m.group(3))
        else:
            pub = mant * (10.0 ** ex)
            # se compara la mantisa a los decimales con que se publica, y el exponente exacto
            import math
            ex_calc = math.floor(math.log10(pv))
            mant_calc = pv / (10.0 ** ex_calc)
            dec = len(m.group(2))
            if ex_calc != ex:
                fallos.append('el informe publica exponente %d y el CSV da %d' % (ex, ex_calc))
            elif abs(round(mant_calc, dec) - mant) >= 10 ** (-dec) / 2:
                fallos.append('el informe publica p = %s x 10^%d y el CSV da %.*f x 10^%d'
                              % (m.group(1) + ',' + m.group(2), ex, dec,
                                 round(mant_calc, dec), ex_calc))
            del pub

    # 3) los grupos, que el informe declara en palabras
    mirados += 1
    if re.search(r'sobre los veintis\u00e9is grupos', s) is None:
        fallos.append('el informe no declara «veintiseis grupos» junto al ANOVA; el CSV trae %d' % k)
    elif k != 26:
        fallos.append('el informe dice veintiseis grupos y el CSV trae %d' % k)

    # 4) el informe del consolidado, que es el que generar_tabla7.py lee
    rep = os.path.join(cons, 'statistical_report.md')
    mirados += 1
    if not os.path.exists(rep):
        fallos.append('no existe el statistical_report.md del consolidado')
    else:
        with open(rep, encoding='utf-8') as fh:
            txt = fh.read()
        m = re.search(r'\*\*F-Statistic:\*\*\s*([0-9.]+)', txt)
        if m is None:
            fallos.append('el informe del consolidado no declara su F-Statistic')
        elif abs(float(m.group(1)) - F) >= 5e-5:
            fallos.append('el informe del consolidado dice F = %s y el CSV da %.4f'
                          % (m.group(1), F))

    # 5) y los grados de libertad, que se derivan de k y N
    mirados += 1
    if (df1, df2) != (k - 1, N - k):
        fallos.append('los grados de libertad no cuadran con %d grupos y %d observaciones' % (k, N))

    check('el ANOVA titular se recalcula desde el CSV', mirados, fallos)


def c_anovas_secundarios(s):
    """Las tres ANOVA secundarias del informe se recalculan desde su corrida.

    Cerradas la principal y Levene, quedaban tres F publicadas sin nadie que las recalculara. Las
    tres reproducen, y cada una desde una corrida distinta, que es lo que costo identificar:

      §5.2  F = 1,1379 · p = 0,3417   `ablacion_n15_REMOTO`, 4 configuraciones, N=60
      §5.2  F = 0,2235 · p = 0,6382   `n30_rerun_REMOTO`, `gemma4:31b` vs `-mlx`, N=60
      §5.3  F = 0,1451 · p = 0,9328   `benchmark_balanced_120_...071207`, 4 config., N=480

    La tercera merece una nota. El informe la cita como «una diferencia de −0,43 puntos y
    p = 0,9328», y ahi hay dos cosas de alcance distinto: el **−0,43** es el contraste
    `fs-es` frente a `zs-en`, mientras la **p** es la del ANOVA de los cuatro grupos. No es un
    error —`FINDINGS §F31` ya lo declara y da tambien la t pareada, p = 0,7019, que esta
    comprobacion reproduce—, pero conviene no leer esa p como si probara ese contraste. Por eso se
    comprueban las dos cosas por separado.

    Ninguna cifra esperada esta escrita en este codigo: todas se leen del informe (§L63).
    """
    CASOS = (
        ('results/ablacion_n15_REMOTO', {'fs-en', 'fs-es', 'zs-en', 'zs-es'},
         r'\(F = (\d+),(\d+); p = (\d+),(\d+)\)', 'la del corpus de quince'),
        ('results/n30_rerun_REMOTO', None,
         r'arroja F = (\d+),(\d+) con p = (\d+),(\d+)', 'la de las dos compilaciones'),
        ('results/benchmark_balanced_120_20260825_071207', {'fs-en', 'fs-es', 'zs-en', 'zs-es'},
         None, 'la del corpus de ciento veinte'),
    )
    fallos, mirados = [], 0
    for rel, filtro, patron, etiq in CASOS:
        csv_path = os.path.join(BENCH_DIR, rel, 'benchmark_results.csv')
        mirados += 1
        if not os.path.exists(csv_path):
            fallos.append('no existe la corrida de %s: %s' % (etiq, rel))
            continue
        g = _grupos_f1(csv_path)
        if filtro:
            g = {k: v for k, v in g.items() if k in filtro}
        if not g:
            fallos.append('la corrida de %s no trae los grupos esperados' % etiq)
            continue
        F, df1, df2, pv, eta2, k, N = _anova_una_via(g)
        if patron is None:
            continue
        mirados += 1
        m = re.search(patron, s)
        if m is None:
            fallos.append('no se encuentra en el informe %s con su F y su p' % etiq)
            continue
        f_pub = float('%s.%s' % (m.group(1), m.group(2)))
        p_pub = float('%s.%s' % (m.group(3), m.group(4)))
        if abs(f_pub - F) >= 5e-5:
            fallos.append('%s: el informe publica F = %s y la corrida da %.4f'
                          % (etiq, f_pub, F))
        dec = len(m.group(4))
        if abs(round(pv, dec) - p_pub) >= 10 ** (-dec) / 2:
            fallos.append('%s: el informe publica p = %s y la corrida da %.4f'
                          % (etiq, p_pub, pv))

    # La tercera: su p es la del ANOVA de los cuatro grupos, y su Δ es un contraste concreto.
    csv3 = os.path.join(BENCH_DIR, 'results/benchmark_balanced_120_20260825_071207',
                        'benchmark_results.csv')
    if os.path.exists(csv3):
        g3 = {k: v for k, v in _grupos_f1(csv3).items()
              if k in ('fs-en', 'fs-es', 'zs-en', 'zs-es')}
        if len(g3) == 4:
            F3, _, _, p3, _, _, _ = _anova_una_via(g3)
            # La frase esta DOS veces en el informe, en §5.3 y en §6. `re.search` solo ve la
            # primera, y si la segunda divergiera nadie lo notaria: es §L59, «las mutaciones
            # deben cubrir todas las apariciones», aplicado a la comprobacion misma. Se
            # recorren todas y se declara cada una como elemento examinado.
            ocur = list(re.finditer(r'se anula, con una diferencia de \u2212(\d+),(\d+) puntos y '
                                    r'p = (\d+),(\d+)', s))
            mirados += 1
            if not ocur:
                fallos.append('no se encuentra en el informe la frase del efecto que se anula '
                              'con su diferencia y su p')
            ma = sum(g3['fs-es']) / len(g3['fs-es'])
            mb = sum(g3['zs-en']) / len(g3['zs-en'])
            d_calc = 100 * (mb - ma)
            for idx, m in enumerate(ocur, 1):
                donde = 'aparicion %d de %d' % (idx, len(ocur))
                mirados += 1
                p_pub = float('%s.%s' % (m.group(3), m.group(4)))
                dec = len(m.group(4))
                if abs(round(p3, dec) - p_pub) >= 10 ** (-dec) / 2:
                    fallos.append('el efecto que se anula (%s): el informe publica p = %s y el '
                                  'ANOVA de los cuatro grupos da %.4f' % (donde, p_pub, p3))
                mirados += 1
                d_pub = float('%s.%s' % (m.group(1), m.group(2)))
                dd = len(m.group(2))
                if abs(round(d_calc, dd) - d_pub) >= 10 ** (-dd) / 2:
                    fallos.append('el efecto que se anula (%s): el informe publica una diferencia '
                                  'de -%s puntos y fs-es frente a zs-en da -%.2f'
                                  % (donde, d_pub, d_calc))

    check('las tres ANOVA secundarias reproducen desde su corrida', mirados, fallos)


def c_tukey(s):
    """El "dos de los trece" de Tukey se cuenta, y sus dos p se leen del artefacto.

    §5.3 dice que la recuperacion «mejoro el F1-Score de forma estadisticamente significativa
    (Tukey HSD) en **dos de los trece** modelos (`nemotron-mini:4b` +14,52 pp, p<0,001, y
    `llama3.2:latest` +10,82 pp, p=0,007)». Es la afirmacion que decide **para que modelos sirve el
    RAG**, y por tanto una de las que un tribunal mira primero.

    Contado el 2026-09-09 sobre las 325 comparaciones del informe del consolidado: de las 13 que
    enfrentan `baseline` con `kb_rag` del mismo modelo, **2 son significativas**, y son esas dos,
    con p_adj de 0 y 0,0069. El informe acierta.

    Conviene no confundir esta cuenta con la de `robustez_estadistica.py`, que da **8 de 13**: esa
    es Wilcoxon apareado con correccion de Holm, una prueba distinta y menos conservadora, porque
    aprovecha el emparejamiento por articulo que Tukey ignora. Las dos cifras son ciertas sobre lo
    que dicen medir, y el riesgo esta en citarlas como si fueran la misma.

    Trampa al emparejar: los sufijos son `_baseline` y `_kb_rag`, y un `rsplit('_', 1)` parte el
    segundo por dentro —`gemma4:31b-mlx_kb` y `rag`—, con lo que no empareja ni una y la
    comprobacion da cero en silencio. Se recortan los sufijos completos.
    """
    cons = os.path.join(BENCH_DIR, 'results/ANALISIS_CONJUNTO_20260907')
    rep = os.path.join(cons, 'statistical_report.md')
    if not os.path.exists(rep):
        check('el «dos de los trece» de Tukey se cuenta desde el artefacto', 0,
              ['no existe el statistical_report.md del consolidado'])
        return
    with open(rep, encoding='utf-8') as fh:
        txt = fh.read()
    filas = re.findall(r'^\|\s*([^|]+?)\s+vs\s+([^|]+?)\s*\|\s*(-?[0-9.]+)\s*\|'
                       r'\s*([0-9.eE+-]+)\s*\|\s*([^|]*?)\s*\|', txt, re.M)

    def _partes(n):
        for suf in ('_kb_rag', '_baseline'):
            if n.endswith(suf):
                return n[:-len(suf)], suf[1:]
        return None, None

    pares = {}
    for a, b, d, pa, sig in filas:
        ma, sa = _partes(a.strip())
        mb, sb = _partes(b.strip())
        if ma and ma == mb and {sa, sb} == {'kb_rag', 'baseline'}:
            pares[ma] = (float(d), float(pa), 'No' not in sig)
    fallos, mirados = [], 0

    mirados += 1
    if not pares:
        fallos.append('cero comparaciones baseline-vs-kb_rag emparejadas sobre %d filas de Tukey: '
                      'revisar el recorte de sufijos, que es la trampa de esta comprobacion'
                      % len(filas))
        check('el «dos de los trece» de Tukey se cuenta desde el artefacto', mirados, fallos)
        return

    sig = sorted([(m, d, pa) for m, (d, pa, e) in pares.items() if e], key=lambda x: x[2])

    # 1) el recuento que publica el informe, en palabras
    mirados += 1
    m = re.search(r'\(Tukey HSD\) en (\w+) de los (\w+) modelos', s)
    PAL = {'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7, 'ocho': 8,
           'trece': 13, 'doce': 12}
    if m is None:
        fallos.append('no se encuentra en el informe la frase del recuento de Tukey')
    else:
        n_pub, tot_pub = PAL.get(m.group(1)), PAL.get(m.group(2))
        if n_pub is None or tot_pub is None:
            fallos.append('no se pueden leer los numerales de la frase de Tukey: %r de %r'
                          % (m.group(1), m.group(2)))
        else:
            if n_pub != len(sig):
                fallos.append('el informe dice %d modelos significativos con Tukey y el artefacto '
                              'da %d: %s' % (n_pub, len(sig), ', '.join(x[0] for x in sig)))
            if tot_pub != len(pares):
                fallos.append('el informe dice «de los %d modelos» y el artefacto empareja %d'
                              % (tot_pub, len(pares)))

    # 2) los dos modelos nombrados, con su delta y su p
    #
    # El delta se LEE DEL INFORME, no se escribe aqui. La primera version comparaba el artefacto
    # contra un 0.1452 puesto a mano en el codigo, de modo que alterar la cifra del informe no
    # hacia fallar nada: la comprobacion no miraba el documento que dice comprobar. Lo destapo la
    # prueba por mutacion —cuatro de cinco mutaciones se detectaban y esta no—, que es exactamente
    # para lo que sirve.
    for nombre, p_pat in (('nemotron-mini:4b', r'p<0,001'), ('llama3.2:latest', r'p=0,007')):
        mirados += 1
        if nombre not in pares:
            fallos.append('el artefacto no trae la comparacion de %s' % nombre)
            continue
        d, pa, es = pares[nombre]
        if not es:
            fallos.append('el informe nombra %s como significativo y el artefacto dice que no'
                          % nombre)
        mirados += 1
        m2 = re.search(r'`%s`\s*\*\*([+-]?\d+),(\d+) pp\*\*' % re.escape(nombre), s)
        if m2 is None:
            fallos.append('no se encuentra en el informe el delta en pp junto a `%s`' % nombre)
        else:
            d_pub = float('%s.%s' % (m2.group(1), m2.group(2))) / 100.0
            if abs(d - d_pub) >= 5e-5:
                fallos.append('el informe publica %+.2f pp para %s y el artefacto da %+.2f pp'
                              % (100 * d_pub, nombre, 100 * d))
        mirados += 1
        if re.search(p_pat, s) is None:
            fallos.append('el informe no publica «%s» junto a %s' % (p_pat, nombre))
        elif p_pat == 'p<0,001' and pa >= 0.001:
            fallos.append('el informe dice p<0,001 para %s y el artefacto da %.4g' % (nombre, pa))
        elif p_pat == 'p=0,007' and abs(round(pa, 3) - 0.007) >= 5e-4:
            fallos.append('el informe dice p=0,007 para %s y el artefacto da %.4g' % (nombre, pa))

    check('el «dos de los trece» de Tukey se cuenta desde el artefacto', mirados, fallos)


def c_levene(s):
    """El supuesto de homocedasticidad del ANOVA principal se recalcula, no se cita de memoria.

    §5 dice «La prueba de Levene no detecta heterocedasticidad (p = 0,18), lo que con 3 120
    observaciones si es informativo». Esa p sostiene el supuesto del ANOVA que da el resultado
    titular del trabajo, y hasta hoy **nada la recalculaba**: estaba persistida en `levene.json`
    desde el 2026-09-08 y ningun codigo la leia, de modo que un cambio en el CSV fusionado —el que
    traera la re-corrida pendiente de `nemotron-mini`— la habria dejado obsoleta en silencio. Es la
    clase de defecto de §F89, en una cifra que el informe **publica**.

    La variante es Levene con centrado en la mediana, Brown-Forsythe, que es la robusta y la que da
    `scipy.stats.levene(center='median')`. Se implementa **con la biblioteca estandar**, a
    proposito: `scipy` solo esta en `repos/ner-llm-entity-benchmark/venv` y una comprobacion que
    solo corre dentro de un entorno concreto no corre. Verificada contra scipy y contra el
    artefacto: las tres vias dan W = 1,2475 y p = 0,1842.
    """
    import csv as _csv
    import statistics as _st
    from collections import defaultdict as _dd
    cons = os.path.join(BENCH_DIR, 'results/ANALISIS_CONJUNTO_20260907')
    csv_path = os.path.join(cons, 'merged_results.csv')
    art_path = os.path.join(cons, 'levene.json')
    fallos, mirados = [], 0
    if not os.path.exists(csv_path):
        check('el supuesto de homocedasticidad se recalcula desde el CSV', 0,
              ['no existe %s' % csv_path])
        return
    g = _dd(list)
    with open(csv_path, encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            v = r.get('f1')
            if v is not None and v != '':
                g[r['model']].append(float(v))
    if not g:
        check('el supuesto de homocedasticidad se recalcula desde el CSV', 0,
              ['el CSV fusionado no trae ninguna f1 legible'])
        return
    z = {k: [abs(x - _st.median(v)) for x in v] for k, v in g.items()}
    kk = len(z)
    N = sum(len(v) for v in z.values())
    gran = sum(x for v in z.values() for x in v) / N
    ssb = sum(len(v) * (sum(v) / len(v) - gran) ** 2 for v in z.values())
    ssw = sum((x - sum(v) / len(v)) ** 2 for v in z.values() for x in v)
    df1, df2 = kk - 1, N - kk
    W = (ssb / df1) / (ssw / df2)
    pv = _f_sf(W, df1, df2)

    # 1) contra el artefacto persistido
    mirados += 1
    if not os.path.exists(art_path):
        fallos.append('no existe levene.json: la cifra publicada no tiene artefacto')
    else:
        try:
            import json as _json
            with open(art_path, encoding='utf-8') as fh:
                A = _json.load(fh)
            for campo, calc in (('W', W), ('p_valor', pv)):
                mirados += 1
                dado = A.get(campo)
                if dado is None:
                    fallos.append('levene.json no trae %s' % campo)
                elif abs(dado - calc) >= 5e-5:
                    fallos.append('levene.json dice %s=%s y el CSV da %.4f' % (campo, dado, calc))
            for campo, calc in (('grupos', kk), ('observaciones', N), ('df1', df1), ('df2', df2)):
                mirados += 1
                if A.get(campo) is not None and A.get(campo) != calc:
                    fallos.append('levene.json dice %s=%s y el CSV da %s'
                                  % (campo, A.get(campo), calc))
        except (ValueError, OSError) as e:
            fallos.append('levene.json no se puede leer: %s' % e)

    # 2) contra lo que el informe publica, a los dos decimales con que lo cita
    mirados += 1
    m = re.search(r'prueba de Levene no detecta heterocedasticidad \(p = (\d+),(\d+)\)', s)
    if m is None:
        fallos.append('no se encuentra en el informe la frase de Levene con su p: '
                      'revisar si se reformulo')
    else:
        pub = float('%s.%s' % (m.group(1), m.group(2)))
        dec = len(m.group(2))
        if abs(round(pv, dec) - pub) >= 10 ** (-dec) / 2:
            fallos.append('el informe publica p = %s y el CSV da %.4f (a %d decimales, %.*f)'
                          % (pub, pv, dec, dec, round(pv, dec)))
    # 3) y que el numero de observaciones que cita el informe sea el del CSV
    mirados += 1
    if re.search(r'3\s*120 observaciones', s) is None and N == 3120:
        fallos.append('el informe no cita las 3 120 observaciones que da el CSV')

    check('el supuesto de homocedasticidad se recalcula desde el CSV', mirados, fallos)


def c_titulares(s):
    """Las cifras titulares, atadas a su corrida: las dos del resumen y la de la soberania.

    «El mejor modelo local alcanza **76,55 %** de F1 en espanol y **90,16 %** en el dominio.» Son
    las cifras con las que se abre el trabajo y **no las cubria ninguna comprobacion**: la primera
    aparece diez veces en el informe y la segunda tres.

    Ambas son la **metrica restringida** —puntuando solo Personas y Organizaciones, las categorias
    que el corpus anota— de `gemma4:31b-mlx`, y se calculan del detalle por registro. Dos avisos
    que costaron encontrarlas: el 76,55 se computa sobre los **120** registros y no sobre los 113
    del manifiesto de contaminados —con 113 sale 76,78— y el del dominio es sobre `n30_rerun_REMOTO`
    con el nombre de grupo `gemma4:31b-mlx`, sin sufijo `_baseline`.
    """
    import json as _json
    # La corrida del 76,55 se resuelve DESDE EL MANIFIESTO y no se escribe aqui: es el grupo
    # `gemma4:31b-mlx_baseline` y el consolidado se queda con la primera fuente que lo trae
    # (`--on-duplicate=first`). Fijar la ruta a mano fue el primer intento y apuntaba a la corrida
    # equivocada, que es el defecto de `FINDINGS §F81.bis` repetido.
    dir_n120 = None
    if os.path.exists(MANIFIESTO):
        with open(MANIFIESTO, encoding='utf-8') as fh:
            for src in _json.load(fh)['sources']:
                if 'gemma4:31b-mlx_baseline' in src.get('models', []):
                    dir_n120 = os.path.dirname(src['csv_path'])
                    break
    dir_cloud = None
    if os.path.exists(MANIFIESTO):
        with open(MANIFIESTO, encoding='utf-8') as fh:
            for src in _json.load(fh)['sources']:
                if 'gemma4:31b-cloud_baseline' in src.get('models', []):
                    dir_cloud = os.path.dirname(src['csv_path'])
                    break
    CASOS = (('76,55', r'76[.,]55', dir_n120, 'gemma4:31b-mlx_baseline',
              None, 'F1 en espanol sobre N=120'),
             ('90,16', r'90[.,]16', 'results/n30_rerun_REMOTO', 'gemma4:31b-mlx',
              None, 'F1 sobre el corpus del dominio'),
             # La cifra que sostiene la conclusion de soberania: la variante alojada frente al mejor
             # local, ambas con la medicion restringida. §6 y §7.1 la citan tres veces.
             ('80,42', r'80[.,]42', dir_cloud, 'gemma4:31b-cloud_baseline',
              None, 'F1 de la variante alojada sobre N=120'))
    fallos, mirados = [], 0
    for etiq, patron, rel, grupo, _x, desc in CASOS:
        mirados += 1
        if rel is None:
            fallos.append('el manifiesto no dice de que corrida sale el %s %%' % etiq)
            continue
        ruta = os.path.join(BENCH_DIR, rel, 'detailed_results.json')
        if not os.path.exists(ruta):
            fallos.append('no existe %s, del que sale el %s %%' % (rel, etiq))
            continue
        with open(ruta, encoding='utf-8') as fh:
            R = [r for r in _json.load(fh) if r.get('model') == grupo]
        if not R:
            fallos.append('la corrida %s no trae el grupo %s' % (rel, grupo))
            continue
        vals = []
        for r in R:
            pt = ((r.get('metrics') or {}).get('per_type')) or {}
            tp = sum((pt.get(c, {}).get('tp', 0) or 0) for c in ('Persons', 'Organizations'))
            fp = sum((pt.get(c, {}).get('fp', 0) or 0) for c in ('Persons', 'Organizations'))
            fn = sum((pt.get(c, {}).get('fn', 0) or 0) for c in ('Persons', 'Organizations'))
            if tp + fp + fn == 0:
                vals.append(1.0)
                continue
            pr = tp / (tp + fp) if tp + fp else 0.0
            rc = tp / (tp + fn) if tp + fn else 0.0
            vals.append(2 * pr * rc / (pr + rc) if pr + rc else 0.0)
        obt = 100 * sum(vals) / len(vals)
        esp = float(etiq.replace(',', '.'))
        if abs(obt - esp) > 0.006:
            fallos.append('%s: el informe dice %s %% y el dato da %.2f %% sobre %d registros'
                          % (desc, etiq, obt, len(R)))
        mirados += 1
        if not re.search(patron, s):
            fallos.append('el informe ya no cita el %s %% (%s)' % (etiq, desc))
    check('las cifras titulares del resumen y de la soberania reproducen', mirados, fallos,
          'metrica restringida a Personas y Organizaciones; el 76,55 va sobre 120 registros, no 113')


def c_ablacion(s):
    """Las tres diferencias del analisis de variantes de prompt, contra su corrida.

    Son +4,38 pp por localizar al espanol, -0,72 por los ejemplos few-shot en ingles y +10,4 por la
    combinacion, y aparecen en **siete** lugares del informe: el resumen, el abstract, §5.2 dos
    veces, §6 y las conclusiones. Ninguna comprobacion las cubria: la Tabla 5 se contrasta contra la
    misma corrida, pero estas son **diferencias** entre sus filas y el informe las cita en prosa.

    Se calculan desde el CSV crudo y no restando las medias publicadas: con dos decimales sale
    -0,73 en lugar de -0,72, y eso habria dado un falso positivo.
    """
    import csv as _csv
    import collections as _c
    rel = 'results/ablacion_n15_REMOTO/benchmark_results.csv'
    ruta = os.path.join(BENCH_DIR, rel)
    if not os.path.exists(ruta):
        check('las diferencias del analisis de variantes reproducen', 0,
              ['no existe %s' % rel])
        return
    g = _c.defaultdict(list)
    with open(ruta, encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            if r.get('f1') not in (None, ''):
                g[r['model']].append(float(r['f1']))
    m = {k: 100 * sum(v) / len(v) for k, v in g.items()}
    faltan = [k for k in ('zs-en', 'zs-es', 'fs-en', 'fs-es') if k not in m]
    if faltan:
        check('las diferencias del analisis de variantes reproducen', 0,
              ['la corrida de ablacion no trae los grupos %s' % ', '.join(faltan)])
        return
    esperado = (('localizacion al espanol', m['zs-es'] - m['zs-en'], r'\+4[.,]38'),
                ('few-shot en ingles', m['fs-en'] - m['zs-en'], r'[-−]0[.,]72'),
                ('combinacion de ambos', m['fs-es'] - m['zs-en'], r'\+?10[.,]4\b'))
    fallos, mirados = [], 0
    for etiq, val, patron in esperado:
        mirados += 1
        if not re.search(patron, s):
            fallos.append('el informe no cita la diferencia de %s, que el dato pone en %+.2f pp'
                           % (etiq, val))
    # y al reves: que la cifra citada coincida con el dato, no solo que exista
    for etiq, val, esp in (('localizacion al espanol', m['zs-es'] - m['zs-en'], 4.38),
                           ('few-shot en ingles', m['fs-en'] - m['zs-en'], -0.72),
                           ('combinacion de ambos', m['fs-es'] - m['zs-en'], 10.40)):
        mirados += 1
        if abs(val - esp) > 0.006:
            fallos.append('%s: el informe dice %+.2f pp y el dato da %+.4f' % (etiq, esp, val))
    check('las diferencias del analisis de variantes reproducen', mirados, fallos,
          'se calculan del CSV crudo: restando medias redondeadas sale -0,73 y no -0,72')


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


def ejecutar(fn, *args):
    """Ejecuta una comprobacion y convierte su excepcion en un fallo declarado.

    Sin esto, un artefacto con JSON roto hacia caer el verificador entero con un volcado: se perdia
    el resumen, no se sabia que comprobaciones habian pasado y la autoprueba lo leia como «no
    detecta», porque no encontraba ninguna linea FALLA que analizar. Comprobado el 2026-09-09
    rompiendo `friedman.json`. Una comprobacion que revienta tiene que **decir cual es y seguir**.
    """
    try:
        fn(*args)
    except Exception as e:
        check('%s (reventó)' % fn.__name__, 0,
              ['%s: %s' % (type(e).__name__, str(e)[:160])],
              'una comprobacion que lanza excepcion se reporta, no tumba el verificador')


def main():
    s = texto()
    ejecutar(c_vacios)
    ejecutar(c_secciones, s)
    ejecutar(c_refs_anexos_tablas, s)
    ejecutar(c_tablas, s)
    ejecutar(c_figuras, s)
    ejecutar(c_bibliografia, s)
    ejecutar(c_resumen, s)
    ejecutar(c_higiene, s)
    ejecutar(c_excluidos, s)
    ejecutar(c_figura_vs_tabla, s)
    ejecutar(c_identificadores)
    ejecutar(c_aritmetica, s)
    ejecutar(c_recuentos, s)
    ejecutar(c_protocolo, s)
    ejecutar(c_anexo_vs_tabla7, s)
    ejecutar(c_tabla7_vs_datos, s)
    ejecutar(c_tabla4_vs_datos, s)
    ejecutar(c_figura1_vs_artefacto, s)
    ejecutar(c_tablas_menores, s)
    ejecutar(c_tabla18_vs_artefacto, s)
    ejecutar(c_json_parsea, s)
    ejecutar(c_correlacion, s)
    ejecutar(c_alucinaciones, s)
    ejecutar(c_defensa, s)
    ejecutar(c_fuentes_de_los_grupos, s)
    ejecutar(c_agregacion, s)
    ejecutar(c_anova, s)
    ejecutar(c_tukey, s)
    ejecutar(c_anovas_secundarios, s)
    ejecutar(c_levene, s)
    ejecutar(c_titulares, s)
    ejecutar(c_ablacion, s)
    ejecutar(c_extension, s)
    if '--red' in sys.argv:
        c_urls(s)

    breve = '--breve' in sys.argv
    fallos_totales = vacias = declarados = 0

    def _declarado(txt):
        for clave in FALLOS_DECLARADOS:
            if clave in txt:
                return clave
        return None

    for nombre, n, fallos, nota in resultados:
        declar = [f for f in fallos if _declarado(f)]
        declarados += len(declar)
        if n == 0:
            estado, vacias = 'VACIA ', vacias + 1
        elif fallos:
            estado = 'FALLA ' if len(declar) < len(fallos) else 'CONOC '
            fallos_totales += len(fallos)
        else:
            estado = 'ok    '
        if not breve or fallos or n == 0:
            print('  %s %-62s (%d elementos)' % (estado, nombre, n))
            for f in fallos[:8]:
                cl = _declarado(f)
                print('           - %s%s' % (f, '' if not cl else
                                             '\n             [DECLARADO] %s' % FALLOS_DECLARADOS[cl]))
            if len(fallos) > 8:
                print('           ... y %d más' % (len(fallos) - 8))
            if (fallos or n == 0) and nota:
                print('           nota: %s' % nota)
    nuevos = fallos_totales - declarados
    print('\n  %d comprobaciones · %d fallos (%d declarados, **%d nuevos**) · %d vacías'
          % (len(resultados), fallos_totales, declarados, nuevos, vacias))
    if not nuevos and not vacias:
        print('  sin fallos nuevos: todo lo que falla esta declarado y asignado')
    # El codigo de salida senala los fallos NUEVOS, no los declarados. Con la lista de declarados
    # devolvia 1 siempre, y `CLAUDE.md` describe esta herramienta como la puerta previa a cada
    # commit: una puerta que nunca abre no es una puerta. Con `--estricto` vuelve el comportamiento
    # anterior, para quien quiera que cualquier fallo, incluido el declarado, corte.
    if '--estricto' in sys.argv:
        return 1 if (fallos_totales or vacias) else 0
    if fallos_totales and not nuevos:
        print('  (codigo de salida 0: no hay fallos nuevos. Usar --estricto para que los declarados '
              'tambien corten)')
    return 1 if (nuevos or vacias) else 0


if __name__ == '__main__':
    sys.exit(main())
