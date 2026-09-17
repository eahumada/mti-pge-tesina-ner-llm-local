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
# Cada fallo declarado lleva la FECHA en que se declaro, no solo su motivo.
#
# Por que. Una declaracion sin fecha es un aparcamiento indefinido: nada distingue la que se
# escribio hoy, con su responsable trabajando en ella, de la que lleva tres semanas ahi porque se
# olvido. Y cada entrada tiene un coste que §L64 documenta —ciega como centinela a su propia
# comprobacion—, de modo que la lista tiene que ser corta y hay que verla envejecer.
#
# El resumen imprime la edad de cada una. No hay caducidad automatica: caducar un fallo
# declarado lo convertiria en un fallo nuevo y cortaria la puerta sin que nadie haya hecho nada
# mal, que es la clase de alarma que se aprende a ignorar. Lo que se hace es **mostrar la edad**.
# ─────────────────────────────────────────────────────────────────────────────────────────────────
# SOBRE LOS NUMEROS «# --- N.» DE LAS COMPROBACIONES, y por que no hay que citarlos
#
# Esos numeros son ETIQUETAS HISTORICAS y NO identifican nada. Comprobado el 2026-09-09: hay 37
# marcadores para 56 comprobaciones, con un hueco de 26 a 44, un duplicado en el 2, y **34 numeros
# que no coinciden con el orden de ejecucion**. Derivaron porque las funciones nuevas se insertan al
# principio del fichero y sus llamadas `ejecutar(...)` en otro sitio, de modo que el numero del
# comentario y la posicion real se separaron sin que nada avisara.
#
# **El identificador estable de una comprobacion es el texto que pasa a `check()`**, que es lo que
# aparece en la salida y lo que alguien busca con un `grep`. Se cita por ese nombre, no por numero.
# Doce numeros citados en la documentacion del proyecto no existen como marcador, y dos citas
# apuntaban a una comprobacion distinta de la que describian. Ver FINDINGS §F146.
#
# No se renumera: las citas de FINDINGS son registro fechado y renumerar las invalidaria todas.
# ─────────────────────────────────────────────────────────────────────────────────────────────────

# Retiradas 2026-09-09 (segunda pasada de Claude Desktop, §2.25, en tres tandas): ademas de las
# siete de la nota anterior, 'guiones largos frente a' (reabierta y vuelta a cerrar por la pieza 30)
# y 'Vale la pena señalar una particularidad de procedencia' ya no tapan ningun fallo: la nota de
# §F163 se propago a los tres .docx (v14). Comprobado antes de retirar. Ver CURRENT-TASKS §1.291.
#
# Retirada 2026-09-09 (§F166): 'resaltes en el cuerpo, menos que los 9 declarados' ya no tapa
# nada. El recorte de la nota de §3.3 sobre Locations (mas clara y mas corta, a peticion del
# autor) quito varias negritas del cuerpo, y el conteo del .md volvio a coincidir exactamente con
# BOLD_CUERPO_BASE=9 por casualidad. Comprobado: 'el .docx no anade resaltes ni guiones' pasa ok.
# No se toco BOLD_CUERPO_BASE, sigue siendo constante de Claude Desktop.
#
# Retiradas 2026-09-09 (§F167, tercera pasada de Claude Desktop, _v15): trece declaraciones de la
# ronda de enriquecimiento del marco teorico (piezas 31-36, ver §F164/§F165/§F166) ya no tapan
# ningun fallo — la prosa de §2.1, §2.3, §2.4, §2.5, el recorte de §3.3, el Anexo A.1 (codigo de
# LLMProvider) y el recuento de resaltes llegaron a los tres .docx en la misma sesion de
# monitoreo, mientras Claude Desktop seguia trabajando en vivo (las dos ultimas se resolvieron
# entre dos ejecuciones seguidas del verificador). Comprobado antes de retirar cada una.
FALLOS_DECLARADOS = {
    '.rebuild_venv.log': ('2026-09-09',
                          'fichero vacio del commit 880f4f9; decision del autor '
                          '(CURRENT-TASKS §1.103)'),
    '.restore_results.log': ('2026-09-09', 'idem'),
    'ya tiene 120 entidades de referencia': ('2026-09-14',
                                             'no es un defecto: results/validacion_n30_es_REMOTO/ (R4, '
                                             'FINDINGS §F179) es un directorio plano nuevo con Locations '
                                             'correctamente anotada tras la traduccion del N=30. La '
                                             'comprobacion asumia que ningun directorio plano de results/ '
                                             'tendria nunca Locations con referencia real; ese supuesto '
                                             'ya no vale con esta corrida nueva y legitima. No toca al '
                                             'N=120 historico que §3.3/Anexo I describen'),
}


# Declaraciones cuya comprobacion **solo corre con `--red`**, de modo que sin red no tapan nada
# y eso es legitimo. Se enumeran aqui y NO se declaran como fallo, porque una declaracion cuya
# clave describiera el aviso de huerfana silenciaria **todos** los avisos de huerfana, presentes y
# futuros. Es lo que paso: la clave «no tapa ningun fallo. Sin --red» casaba con la plantilla del
# mensaje de la comprobacion 55 y anulaba su deteccion entera. Ver FINDINGS §F133.
# (2026-09-17: vacia desde que la referencia [37] paso a apuntar a un repositorio publico y su
# declaracion se retiro de FALLOS_DECLARADOS; se conserva el mecanismo para el proximo caso.)
SOLO_CON_RED = frozenset()


def _edad_declarado(clave):
    """Texto con la edad de una declaracion, o cadena vacia si no se puede fechar."""
    import datetime as _dt
    fecha = FALLOS_DECLARADOS[clave][0]
    try:
        d = _dt.date.fromisoformat(fecha)
    except ValueError:
        return ''
    dias = (_dt.date.today() - d).days
    if dias <= 0:
        return ' · declarado hoy'
    if dias == 1:
        return ' · declarado ayer'
    return ' · declarado hace %d dias' % dias


def _motivo_declarado(clave):
    return FALLOS_DECLARADOS[clave][1] + _edad_declarado(clave)

resultados = []


# --- 45. La Tabla 7 tambien reproduce desde los recuentos crudos --------------------------------
def c_tabla7_desde_per_type(s):
    """La misma tabla, por la OTRA ruta: `per_type` en lugar de la columna `f1` del CSV.

    `c_tabla7_vs_datos` la ata al CSV consolidado, que es la fuente de la que se escribio. Esta la
    ata a los **recuentos** de los que ese CSV sale, y por tanto puede discrepar de la anterior.
    Discrepa: en `nemotron-mini:4b_baseline` los dos artefactos del grupo dicen cosas distintas,
    porque seis de sus registros se re-extrajeron fuera del arnes y solo el CSV recibio las
    metricas (§F110). Los otros 25 grupos coinciden por las dos rutas, y eso es lo que acredita
    sus cifras: coinciden por dos caminos distintos.

    Se declaro esperando que la re-corrida de `§3.bis.15` lo cerrase. **Llego el 2026-09-09 y no lo
    cierra**: fue a `ANALISIS_CONJUNTO_20260909_FIX`, un consolidado construido sobre trece corridas
    que no comparten ni una fuente con el publicado, y el publicado —que es el que esta
    comprobacion lee— sigue intacto. De modo que ahora depende de la **decision 1**, reabierta en
    `§F113`: si el informe adopta el consolidado nuevo, hay que apuntar `CSV_CONSOLIDADO` al nuevo y
    levantar la exclusion de `tools/sensibilidad_combinada.py`; si no lo adopta, este fallo se queda
    y hay que redeclararlo como permanente.
    """
    import importlib.util as _iu
    ruta = os.path.join(RAIZ, 'tools/sensibilidad_combinada.py')
    if not os.path.exists(ruta):
        check('la Tabla 7 reproduce tambien desde per_type', 0,
              ['no existe tools/sensibilidad_combinada.py'])
        return
    _sp = _iu.spec_from_file_location('_sc', ruta)
    _sc = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_sc)
    datos = _sc.cargar()
    i = s.find('_Tabla 7.')
    if i < 0:
        check('la Tabla 7 reproduce tambien desde per_type', 0, ['no se encuentra la Tabla 7'])
        return
    t7 = {}
    for l in s[i:i + 3000].split('\n'):
        m = re.match(r'^\|\s*([^|]+?)\s*\|\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|'
                     r'\s*\*{0,2}([\d.]+)%\*{0,2}\s*\|', l)
        if m and not m.group(1).startswith('Modelo'):
            t7[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)))
    fallos, n = [], 0
    for mod, (b, r) in sorted(t7.items()):
        for suf, pub in (('_baseline', b), ('_kb_rag', r)):
            g = mod + suf
            if g not in datos:
                fallos.append('%s no tiene per_type en ninguna fuente' % g)
                continue
            n += 1
            got = 100 * sum(x[0] for x in datos[g]) / len(datos[g])
            if abs(got - pub) > 0.05:
                fallos.append('%s: publicado %.2f, per_type %.4f (%+.4f)' % (g, pub, got, got - pub))
    check('la Tabla 7 reproduce tambien desde per_type', n, fallos,
          'ruta independiente de c_tabla7_vs_datos; su unico fallo depende de la decision 1')


# --- 46. El recuento de Tukey del informe, y la coherencia interna del artefacto ----------------
def c_tukey_recuento(s):
    """«158 comparaciones significativas de las 325 posibles»: nadie la recalculaba.

    Es el patron de §F91 una vez mas, en el mismo parrafo que ya obligo a anadir el ANOVA y Levene.
    La cifra es correcta —contrastada el 2026-09-09 con `statsmodels`, que da exactamente 158 de
    325—, pero comprobarla exigia el venv, de modo que aqui se comprueba por dos vias que si
    caben en biblioteca estandar:

    1. **Contra el artefacto**: el `statistical_report.md` del consolidado publica la tabla completa
       de pares con su p ajustada y su veredicto. Se cuentan sus filas y sus veredictos afirmativos
       y se contrastan con lo que el informe declara, y con C(26,2) = 325.
    2. **Coherencia interna del artefacto**: cada veredicto se contrasta contra **su propia p**.
       Un «significativo» con p >= 0,05, o un «no» con p < 0,05, es una incoherencia del artefacto
       que ninguna comparacion de totales detecta, porque dos errores de signo contrario se
       compensan en el recuento.

    La distribucion del rango estudentizado no esta en la biblioteca estandar, asi que esta
    comprobacion **no recalcula Tukey**: verifica el recuento y la coherencia. Se declara aqui para
    que nadie la lea como mas fuerte de lo que es.
    """
    cons = os.path.dirname(CSV_CONSOLIDADO)  # una sola fuente de verdad; ver F149
    art = os.path.join(cons, 'statistical_report.md')
    if not os.path.exists(art):
        check('el recuento de Tukey del informe cuadra con el artefacto', 0,
              ['no existe %s' % os.path.relpath(art, RAIZ)])
        return
    with open(art, encoding='utf-8') as fh:
        t = fh.read()
    # Filas de par: «| A vs B | dif | p | veredicto | IC |»
    pares = []
    for l in t.split('\n'):
        m = re.match(r'^\|\s*(\S.*?)\s+vs\s+(\S.*?)\s*\|\s*(-?[\d.]+)\s*\|'
                     r'\s*([\d.eE+-]+)\s*\|\s*([^|]+?)\s*\|', l)
        if m:
            pares.append((m.group(1), m.group(2), float(m.group(4)), m.group(5)))
    fallos = []
    n = len(pares)
    if n == 0:
        check('el recuento de Tukey del informe cuadra con el artefacto', 0,
              ['no se puede leer ninguna fila de pares del artefacto: revisar su formato'])
        return
    # 1) totales contra el informe y contra C(26,2)
    esp = 26 * 25 // 2
    if n != esp:
        fallos.append('el artefacto trae %d filas de par y C(26,2) son %d' % (n, esp))
    afirm = [x for x in pares if 'Yes' in x[3] or 'Sí' in x[3] or 'Si' in x[3]]
    m = re.search(r'Tukey identifica (\d+) comparaciones significativas de las (\d+) posibles', s)
    if m is None:
        fallos.append('no se encuentra en el informe la frase del recuento de Tukey: '
                      'revisar si se reformulo')
    else:
        pub_sig, pub_tot = int(m.group(1)), int(m.group(2))
        if pub_sig != len(afirm):
            fallos.append('el informe declara %d significativas y el artefacto trae %d'
                          % (pub_sig, len(afirm)))
        if pub_tot != n:
            fallos.append('el informe declara %d comparaciones posibles y el artefacto trae %d'
                          % (pub_tot, n))
    # 2) cada veredicto contra su propia p: dos errores de signo contrario se compensarian
    #    en el recuento y ninguna comparacion de totales los veria.
    for a, b, pv, ver in pares:
        af = ('Yes' in ver or 'Sí' in ver or 'Si' in ver)
        if af and pv >= 0.05:
            fallos.append('%s vs %s: marcado significativo con p = %.4g' % (a, b, pv))
        elif not af and pv < 0.05:
            fallos.append('%s vs %s: marcado no significativo con p = %.4g' % (a, b, pv))
    check('el recuento de Tukey del informe cuadra con el artefacto', n, fallos,
          'no recalcula Tukey —el rango estudentizado no esta en la biblioteca estandar—: '
          'verifica el recuento y la coherencia interna del artefacto')


# --- 47. El chi cuadrado de Friedman del informe, recalculado --------------------------------
def c_friedman(s):
    """La prueba que sostiene «la conclusion no depende de esa eleccion», y nadie la miraba.

    §5 declara una limitacion del contraste —los 26 grupos evaluan los mismos 120 articulos, de
    modo que las observaciones estan apareadas— y la salva con Friedman: «repetido con la prueba de
    Friedman, que es la que corresponde a un diseno de medidas repetidas, el rechazo se sostiene con
    holgura (chi2 = 1 169,23), de modo que la conclusion no depende de esa eleccion». Es la frase
    que responde a la objecion metodologica mas facil de plantear en una defensa.

    **Su cifra no la comprobaba nadie.** `c_defensa` verifica ese mismo chi2, pero en
    `DEFENSA-PREGUNTAS-Y-RESPUESTAS.md`, que es otro documento: si la copia del informe se desviara
    del artefacto, no lo notaria ninguna de las 46 comprobaciones anteriores. Detectado por el
    barrido de `tools/cobertura_cifras.py` y confirmado por mutacion —alterada a 9 999,99, cero
    fallos nuevos— antes de escribir esto (`§F116`).

    Se **recalcula**, no se compara contra el artefacto y nada mas. Friedman cabe en la biblioteca
    estandar: se rangan los 26 valores dentro de cada articulo, se suman los rangos por grupo y
    chi2 = 12/(n*k*(k+1)) * suma(Rj^2) - 3n(k+1). **La correccion por empates es imprescindible**:
    sin ella sale 1 123,0730 y con ella 1 169,2327, de modo que una implementacion que la olvide
    da un fallo donde no lo hay. Las tres vias —este recalculo, el artefacto y el informe—
    coinciden al cuarto decimal.
    """
    import collections as _c
    if not os.path.exists(CSV_CONSOLIDADO):
        check('el chi2 de Friedman se recalcula desde el CSV', 0,
              ['no existe %s' % os.path.relpath(CSV_CONSOLIDADO, RAIZ)])
        return
    import csv as _csv
    por = _c.defaultdict(dict)
    with open(CSV_CONSOLIDADO, encoding='utf-8') as fh:
        for r in _csv.DictReader(fh):
            if r.get('f1') not in (None, ''):        # `is not None`: un F1 de 0,0 es un dato
                por[r['record_id']][r['model']] = float(r['f1'])
    grupos = sorted({g for d in por.values() for g in d})
    comp = [rid for rid, d in por.items() if len(d) == len(grupos)]
    k, n = len(grupos), len(comp)
    if k < 2 or n < 2:
        check('el chi2 de Friedman se recalcula desde el CSV', 0,
              ['no hay bloques completos que rangar: %d grupos, %d bloques' % (k, n)])
        return

    def _rangos(v):
        idx = sorted(range(len(v)), key=lambda i: v[i])
        out = [0.0] * len(v)
        i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and v[idx[j + 1]] == v[idx[i]]:
                j += 1
            med = (i + j) / 2.0 + 1
            for t in range(i, j + 1):
                out[idx[t]] = med
            i = j + 1
        return out

    Rj, T = [0.0] * k, 0.0
    for rid in comp:
        rr = _rangos([por[rid][g] for g in grupos])
        for a in range(k):
            Rj[a] += rr[a]
        T += sum(t ** 3 - t for t in _c.Counter(rr).values())
    chi = 12.0 / (n * k * (k + 1)) * sum(x * x for x in Rj) - 3 * n * (k + 1)
    corr = 1 - T / (n * (k ** 3 - k))
    if corr <= 0:
        check('el chi2 de Friedman se recalcula desde el CSV', 0,
              ['la correccion por empates sale <= 0 (%r): no se puede dividir' % corr])
        return
    chi /= corr

    fallos, mirados = [], 0
    # 1) contra el informe
    mirados += 1
    m = re.search(r'holgura \(χ² = ([\d\s]+),(\d+)\)', s)
    if m is None:
        fallos.append('no se encuentra en el informe la frase de Friedman con su χ²: '
                      'revisar si se reformulo')
    else:
        pub = float('%s.%s' % (m.group(1).replace(' ', '').replace('\u00a0', ''), m.group(2)))
        if abs(pub - chi) > 0.011:
            fallos.append('el informe publica χ² = %s y el recalculo da %.4f' % (pub, chi))
    # 2) contra el artefacto, y su gl
    art = os.path.join(BENCH_DIR, 'results/ROBUSTEZ_ESTADISTICA_20260909_FIX/friedman.json')
    # Adoptado el 2026-09-09 junto con CSV_CONSOLIDADO (decision 1). El artefacto del
    # publicado (2026-09-08) se conserva en su directorio y no se borra.
    if not os.path.exists(art):
        fallos.append('falta %s, del que el indice de defensa toma esta misma cifra'
                      % os.path.relpath(art, RAIZ))
    else:
        import json as _json
        with open(art, encoding='utf-8') as fh:
            fr = (_json.load(fh) or {}).get('friedman_medidas_repetidas') or {}
        mirados += 1
        a_chi = fr.get('chi2')
        if a_chi is None:
            fallos.append('friedman.json no trae chi2')
        elif abs(a_chi - chi) > 1e-3:
            fallos.append('friedman.json dice χ² = %.4f y el recalculo da %.4f' % (a_chi, chi))
        mirados += 1
        gl = fr.get('gl')
        if gl is not None and gl != k - 1:
            fallos.append('friedman.json dice gl = %s y con %d grupos son %d' % (gl, k, k - 1))
    check('el chi2 de Friedman se recalcula desde el CSV', mirados, fallos,
          'con correccion por empates: sin ella daria 1123,07 en lugar de 1169,23')


# --- 48. Los tres deltas del 2x2 del idioma del prompt -----------------------------------------
def c_ablacion_idioma(s):
    """El factor que S6.1 pone primero para explicar sus resultados, atado a su re-corrida de 5 semillas.

    [ACTUALIZADA 2026-09-17] La medicion de una sola corrida (ablacion_n15_REMOTO) se sustituyo por
    la media de cinco semillas declaradas (variantes_5semillas_n15_REMOTO, FINDINGS SF176), a
    instruccion explicita del autor de purgar el cuerpo de cifras de una sola pasada cuando existe
    una replica disponible. La Tabla 5 (Hallazgo 5) dice ahora: "el espanol en la instruccion aporta
    +9,01 pp y los ejemplos en ingles +3,61 pp", con "su combinacion alcanza +13,19 pp".

    Reproducen desde las cinco semillas (42-46), promediando cada celda sobre las 5x15=75
    observaciones: zs-en 66,77, zs-es 75,78, fs-en 70,38, fs-es 79,96. La celda de referencia es
    zs-en, la de menos ayuda.

    Se comprueba tambien la afirmacion de interaccion, que es la que sostiene el argumento y no es
    una cifra: que ninguno de los dos factores por separado alcance el efecto conjunto.
    """
    import csv as _csv
    import collections as _c
    import glob as _glob
    ficheros = sorted(_glob.glob(os.path.join(
        BENCH_DIR, 'results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv')))
    if not ficheros:
        check('los deltas del 2x2 del idioma reproducen desde la ablacion', 0,
              ['no existe results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv'])
        return
    g = _c.defaultdict(list)
    for d in ficheros:
        with open(d, encoding='utf-8') as fh:
            for r in _csv.DictReader(fh):
                if r.get('f1') not in (None, ''):     # un F1 de 0,0 es un dato, no un hueco
                    g[r['model']].append(float(r['f1']))
    M = {k: 100 * sum(v) / len(v) for k, v in g.items()}
    faltan = [c for c in ('zs-en', 'zs-es', 'fs-en', 'fs-es') if c not in M]
    if faltan:
        check('los deltas del 2x2 del idioma reproducen desde la ablacion', 0,
              ['las 5 semillas no traen las celdas %s; traen %s' % (faltan, sorted(M))])
        return
    juntos = M['fs-es'] - M['zs-en']
    solo_p = M['zs-es'] - M['zs-en']
    solo_e = M['fs-en'] - M['zs-en']

    fallos, mirados = [], 0
    CASOS = [('ambos en espanol', juntos,
              r'combinación alcanza \+(\d+),(\d+) pp'),
             ('solo el prompt', solo_p,
              r'español en la instrucción aporta \+(\d+),(\d+) pp'),
             ('ejemplos en ingles', solo_e,
              r'los ejemplos en inglés \+(\d+),(\d+) pp')]
    for nombre, calc, pat in CASOS:
        mirados += 1
        m = re.search(pat, s)
        if m is None:
            fallos.append('no se encuentra en el informe la cifra de «%s»: revisar si se reformulo'
                          % nombre)
            continue
        pub = float('%s.%s' % (m.group(1), m.group(2)))
        if abs(pub - calc) > 0.011:
            fallos.append('«%s»: el informe dice %.2f y las 5 semillas dan %.4f' % (nombre, pub, calc))
    # La afirmacion de interaccion, que no es una cifra y es la que sostiene el argumento.
    mirados += 1
    if 'ninguno de los dos factores basta por separado' in s:
        if not (solo_p < juntos and solo_e < juntos):
            fallos.append('el informe afirma que ningun factor por separado alcanza el efecto '
                          'conjunto, y los datos dan juntos=%.4f, solo prompt=%.4f, solo '
                          'ejemplos=%.4f' % (juntos, solo_p, solo_e))
    else:
        fallos.append('no se encuentra la afirmacion de interaccion en Tabla 5: revisar si se reformulo')
    check('los deltas del 2x2 del idioma reproducen desde la ablacion', mirados, fallos,
          'la celda de referencia es zs-en; media de 5 semillas desde 2026-09-17')


# --- 49. El informe se cita a si mismo redondeado, y el redondeo tiene que seguir cuadrando ----
def c_redondeos(s):
    """Los restatements redondeados del resumen y de las conclusiones, contra su cifra precisa.

    El resumen dice «+14,5 y +10,8 puntos» donde §5 mide +14,52 y +10,82; las conclusiones dicen
    «rho = -0,52 con p = 0,071» donde §5 da -0,5165 y 0,0707. Son la **misma cifra escrita dos
    veces con distinta precision**, y esa es exactamente la forma en que se cuelan las
    incoherencias: `§L69` fue eso —propagados 81,45 -> 80,42 y 76,85 -> 76,55, quedo «cinco
    puntos» describiendo una resta de 3,87, y el documento paso de coherente-con-datos-viejos a
    incoherente-consigo-mismo—.

    Ninguna cifra se escribe aqui. Se leen **las dos del documento** y se comprueba que la
    redondeada sea el redondeo de la precisa. Una constante copiada del informe detectaria una
    deriva de los datos pero no una del texto, que es el defecto que la comprobacion 22 ya tuvo y
    que `§L63` deja escrito.

    Cubre tambien una cifra derivada que el barrido de `§F116` dejo al descubierto y que se puede
    recomputar de sus propios operandos, presentes en la frase: la reduccion de coste, **que es
    una estimacion y el informe la declara como tal** en los dos sitios donde aparece.

    [RETIRADA 2026-09-17, segunda vuelta] Esta comprobacion tambien vigilaba la proporcion de
    entidades con *mojibake* (283 de 1 406, 20,1 %). La frase que la sostenia se retiro del cuerpo
    a instruccion directa del autor (purga de referencias a defectos historicos sin asidero en la
    corrida vigente); la cifra sigue intacta en `FINDINGS.md §F53`. Ver FINDINGS §F191.
    """
    fallos, mirados = [], 0

    def _f(t):
        return float(t.replace('−', '-').replace(' ', '').replace(' ', '')
                     .replace(',', '.'))

    # (nombre, regex de la precisa, regex de la redondeada, decimales)
    PARES = [
        # `llama3.2:latest` dejo de citarse en el resumen con un numero pareado desde que la
        # decision 1 lo saco de los modelos significativos (F154): no hay ya una forma "redondeada"
        # de su delta en el resumen, de modo que ese par se retiro de esta lista en lugar de
        # dejarlo fallando contra un texto que ya no tiene por que existir.
        ('mejora de nemotron-mini:4b', r'\*\*\+?(\d+),(\d{2}) pp\*\*.{0,20}modelo m[aá]s d[eé]bil',
         r'el m[aá]s d[eé]bil de los trece \(\+(\d+),(\d) puntos', 1),
        ('efecto del idioma', r'aporta \+(13),(19) puntos', r'aporta \+(13),(\d) puntos', 1),
        # El signo va DENTRO de la negrita: «**Spearman de −0,5165**». Y la p redondeada hay que
        # anclarla a su propia frase: «con p = (0),(\d{3})» a secas casaba con la p = 0,6382 de
        # un ANOVA secundario, que esta en otro sitio y no tiene nada que ver.
        ('rho de Spearman', r'\*\*Spearman de −?(0),(\d{4})\*\*', r'ρ = −(0),(\d{2}) con p', 2),
        # La p precisa se ancla A LA MISMA FRASE que la de Spearman en lugar de un literal fijo:
        # con el consolidado publicado era 0,0707 y con el adoptado es 0,7752, y una constante
        # aqui repetiria el defecto que esta comprobacion existe para evitar.
        ('p de Spearman', r'\*\*Spearman de −?0,\d{4}\*\* \(p = (0),(\d{4})\)',
         r'ρ = −0,\d+ con p = (0),(\d{3})', 3),
    ]
    for nombre, p_pre, p_red, dec in PARES:
        mirados += 1
        a, b = re.search(p_pre, s), re.search(p_red, s)
        if a is None or b is None:
            fallos.append('no se encuentran las dos formas de «%s» (precisa: %s, redondeada: %s): '
                          'revisar si se reformulo' % (nombre, a is not None, b is not None))
            continue
        pre = _f('%s.%s' % (a.group(1), a.group(2)))
        red = _f('%s.%s' % (b.group(1), b.group(2)))
        esp = round(pre, dec)
        if abs(red - esp) > 1e-9:
            fallos.append('«%s»: el informe dice %s donde %s redondeado a %d decimal(es) es %s'
                          % (nombre, red, pre, dec, esp))

    # reduccion de coste: estimacion declarada, pero su aritmetica interna debe cuadrar
    mirados += 1
    mc = re.search(r'Frente a esos USD (0),(\d+), la revisión manual cuesta unos USD '
                   r'(\d+),(\d+) por artículo', s)
    # las DOS apariciones de la reduccion: §5.5 la resalta y §6 la repite sin resalte
    todas_r = [_f('%s.%s' % (x.group(1), x.group(2))) for x in
               re.finditer(r'reducci[óo]n (?:del|estimada es del) \*{0,2}(\d+),(\d) ?%\*{0,2}', s)]
    mr = re.search(r'reducción del \*\*(\d+),(\d) ?%\*\* en coste unitario', s)
    if mc is None or mr is None:
        fallos.append('no se encuentran los dos costes y su reduccion en §5.5: '
                      'revisar si se reformulo')
    else:
        loc = _f('%s.%s' % (mc.group(1), mc.group(2)))
        man = _f('%s.%s' % (mc.group(3), mc.group(4)))
        pub = _f('%s.%s' % (mr.group(1), mr.group(2)))
        calc = round(100 * (1 - loc / man), 1) if man else None
        for v in (todas_r or [pub]):
            if calc is None or abs(v - calc) > 1e-9:
                fallos.append('coste: 1 - %s/%s es %s %% y el informe dice %s %%'
                              % (loc, man, calc, v))
        if len(set(todas_r)) > 1:
            fallos.append('coste: la reduccion aparece con %d valores distintos (%s)'
                          % (len(set(todas_r)), sorted(set(todas_r))))
        # y que siga declarada como estimacion en los dos sitios (regla de CLAUDE.md)
        if s.count('estimaciones y no mediciones') < 1 or 'igualmente estimada' not in s:
            fallos.append('la reduccion de coste ha dejado de declararse como estimacion en alguno '
                          'de los dos sitios donde aparece')
    check('los redondeos que el informe se cita a si mismo cuadran', mirados, fallos,
          'las dos formas se LEEN del documento; una constante aqui no veria una deriva del texto')


# --- 50. La Tabla 17 reproduce desde el corpus HISTORICO -----------------------------------
CORPUS_REL = 'repos/ner-llm-entity-benchmark/data/benchmark_balanced_120.json'
# El corpus se corrigio el 2026-09-08 y la Tabla 17 mide el estado ANTERIOR. Este commit es el
# ultimo que lo conserva con el defecto; localizado recorriendo `git log --follow` sobre el
# corpus y midiendo cada version (§F119).
CORPUS_HIST = 'df9b4c4'


def _fuzz_ratio(a, b):
    """`fuzz.ratio` de rapidfuzz en biblioteca estandar: 200 * LCS / (len(a) + len(b)).

    Es la similitud de Indel normalizada. `rapidfuzz` solo esta en el venv del proyecto, y una
    comprobacion que solo corre en un entorno no corre. **Validada contra rapidfuzz sobre los 283
    pares del corpus historico: diferencia maxima 0,0 y cero discrepancias de veredicto.**

    No sirve `difflib.SequenceMatcher.ratio`, que usa bloques coincidentes y no la subsecuencia
    comun mas larga: da valores parecidos y no iguales, y aqui se compara contra un umbral.
    """
    if not a and not b:
        return 100.0
    m, n = len(a), len(b)
    ant = [0] * (n + 1)
    for i in range(1, m + 1):
        act = [0] * (n + 1)
        ai = a[i - 1]
        for j in range(1, n + 1):
            act[j] = ant[j - 1] + 1 if ai == b[j - 1] else max(ant[j], act[j - 1])
        ant = act
    return 200.0 * ant[n] / (m + n)


def _sin_mojibake(t):
    """La forma correcta de una cadena con mojibake, o None si no lo tiene.

    Se usa la **definicion** del defecto y no una clase de caracteres: una cadena esta corrupta si
    recodificarla de latin-1 a utf-8 tiene exito y cambia el resultado, que es exactamente lo que
    significa «bytes UTF-8 reinterpretados como Latin-1».
    """
    if not isinstance(t, str):
        return None
    try:
        v = t.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None
    return v if v != t else None


# [RETIRADA 2026-09-17] La Tabla 17 de la que hablaba esta comprobacion (el alcance medido del
# mojibake, seis filas) se retiro del Anexo H por instruccion del autor: registro forense de un
# defecto ya corregido, no un dato que sostenga la hipotesis vigente. El numero de tabla «17» lo
# ocupa ahora una tabla distinta (Anexo K, IC95% de R2), así que dejar esta comprobacion activa
# validaria contenido equivocado contra un patron que nunca va a encontrar. Ver FINDINGS §F191.
def _c_tabla17_RETIRADA(s):
    """Una medicion que el corpus actual ya NO puede reproducir, atada a la version que si.

    La Tabla 17 mide el alcance del defecto de codificacion sobre el corpus N=120, y el informe
    declara en §2 que «el defecto esta corregido en el corpus desde el 8 de septiembre de 2026» y
    que sus cifras «se conservan tal como se midieron». De modo que **medirla contra el corpus
    actual da cero en todas sus filas**: no porque la tabla este mal, sino porque describe un
    estado que ya no existe. Comprobado: hoy el fichero trae 0 entidades con mojibake y 545
    localizaciones que entonces no tenia.

    Eso la dejaba fuera del alcance de cualquier comprobacion, y es una tabla de **seis medidas**.
    La ruta que si funciona es la historia de git, que es un artefacto que **atestigua** y por
    tanto se conserva: `git show df9b4c4:<corpus>` devuelve la version con el defecto, y sobre ella
    las seis filas reproducen exactas.

    Las cifras se **leen de la tabla**, no se escriben aqui (`§L63`). La fila del umbral difuso
    exige reimplementar `fuzz.ratio`, y esta validada contra `rapidfuzz` en los 283 pares.
    """
    fallos, mirados = [], 0
    i = s.find('_Tabla 17.')
    if i < 0:
        check('la Tabla 17 reproduce desde el corpus historico', 0,
              ['no se encuentra la Tabla 17'])
        return
    bloque = s[i:i + 1400]

    def fila(pat):
        m = re.search(pat, bloque)
        return m

    r = subprocess.run(['git', 'show', '%s:%s' % (CORPUS_HIST, CORPUS_REL)],
                       cwd=RAIZ, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        check('la Tabla 17 reproduce desde el corpus historico', 0,
              ['no se puede leer %s:%s — un clon superficial no trae ese commit, y sin el la '
               'Tabla 17 no se puede verificar contra nada: el corpus actual ya no tiene el '
               'defecto' % (CORPUS_HIST, CORPUS_REL)])
        return
    import json as _json
    try:
        recs = _json.loads(r.stdout)['dataset']
    except (ValueError, KeyError, TypeError) as e:
        check('la Tabla 17 reproduce desde el corpus historico', 0,
              ['el corpus historico no se puede interpretar: %s: %s' % (type(e).__name__, e)])
        return

    CAMPOS = ('name_entities', 'organizations', 'locations')
    tot = moj = arts = igual = correcta = irrec = 0
    for reg in recs:
        t = reg.get('text') or ''
        if _sin_mojibake(t) is not None:
            arts += 1
        for c in CAMPOS:
            for x in (reg.get(c) or []):
                tot += 1
                lim = _sin_mojibake(x)
                if lim is None:
                    continue
                moj += 1
                if x in t:
                    igual += 1
                elif lim in t:
                    correcta += 1
                if _fuzz_ratio(x.lower(), lim.lower()) < 85:
                    irrec += 1

    def comp(nombre, pat, calc, grupo=1):
        nonlocal mirados
        mirados += 1
        m = fila(pat)
        if m is None:
            fallos.append('no se encuentra en la Tabla 17 la fila de «%s»: revisar si se '
                          'reformulo' % nombre)
            return
        pub = int(m.group(grupo).replace(' ', '').replace(' ', ''))
        if pub != calc:
            fallos.append('«%s»: la Tabla 17 dice %d y el corpus historico da %d'
                          % (nombre, pub, calc))

    comp('entidades de referencia totales',
         r'Entidades de referencia totales \|\s*\*{0,2}([\d\s ]+?)\*{0,2}\s*\|', tot)
    comp('entidades con mojibake',
         r'Entidades con \*mojibake\* \|\s*\*{0,2}([\d\s ]+?) \(', moj)
    comp('irrecuperables en el cotejo difuso',
         r'irrecuperables en el cotejo difuso[^|]*\|\s*\*{0,2}([\d\s ]+?) \(', irrec)
    comp('articulos con mojibake en el texto',
         r'Artículos con \*mojibake\* en el campo `text` \|\s*\*{0,2}([\d\s ]+?) de', arts)
    comp('corruptas que aparecen igual de corruptas',
         r'aparecen igual de corruptas en el texto \|\s*\*{0,2}([\d\s ]+?) de', igual)
    comp('corruptas que aparecen correctas en el texto',
         r'aparecen correctas en el texto \|\s*\*{0,2}([\d\s ]+?)\*{0,2}\s*\|', correcta)

    # Los dos porcentajes derivados de la propia tabla
    mirados += 1
    m = re.search(r'irrecuperables en el cotejo difuso[^|]*\|\s*\*{0,2}[\d\s]+ \((\d+),(\d) ?%'
                  r' del total\)', bloque)
    if m is None:
        fallos.append('no se encuentra el porcentaje de irrecuperables en la Tabla 17')
    else:
        pub = float('%s.%s' % (m.group(1), m.group(2)))
        calc = round(100 * irrec / tot, 1) if tot else None
        if calc is None or abs(pub - calc) > 1e-9:
            fallos.append('irrecuperables: %d de %d son %s %% y la tabla dice %s %%'
                          % (irrec, tot, calc, pub))
    # Y el ejemplo que la prosa cita como recuperable
    mirados += 1
    m = re.search(r'`Emiliano Garc[^`]*` obtiene (\d+)', s)
    if m is None:
        fallos.append('no se encuentra en la prosa el ejemplo de cotejo recuperable')
    else:
        par = [(x, _sin_mojibake(x)) for reg in recs for c in CAMPOS
               for x in (reg.get(c) or [])
               if _sin_mojibake(x) and 'Page' in (_sin_mojibake(x) or '')]
        if not par:
            fallos.append('el ejemplo de la prosa no esta en el corpus historico')
        else:
            got = round(_fuzz_ratio(par[0][0].lower(), par[0][1].lower()))
            if got != int(m.group(1)):
                fallos.append('el ejemplo de la prosa: la razon es %d y el informe dice %s'
                              % (got, m.group(1)))
    check('la Tabla 17 reproduce desde el corpus historico', mirados, fallos,
          'el corpus ACTUAL da cero en todas sus filas: la tabla mide el estado anterior a la '
          'correccion del 2026-09-08 y solo la historia de git lo conserva')


# --- 51. La PROSA del entregable esta sincronizada con la del Markdown ------------------------
def _norm_prosa(t):
    import unicodedata as _u
    t = _u.normalize('NFC', t)
    for a in (' ', ' ', ' '):
        t = t.replace(a, ' ')
    return ' '.join(re.sub(r'[`*_]', '', t).split())


def _parrafos_md(s):
    """Parrafos de prosa larga del Markdown, sin tablas, codigo, indice ni leyendas."""
    out, en_codigo = [], False
    for b in s.split('\n\n'):
        b = b.strip()
        if b.startswith('```'):
            en_codigo = not en_codigo
            continue
        if en_codigo or not b or b.startswith(('|', '#', '_Tabla', '!')) or '](#' in b:
            continue
        n = _norm_prosa(re.sub(r'^>\s?', '', b, flags=re.M))
        if len(n) > 160:
            out.append(n)
    return out


def _parrafos_docx(rel):
    import zipfile as _z
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return None, None
    with _z.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    pars = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
        t = _norm_prosa(''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p, re.S)))
        if len(t) > 160:
            pars.append(t)
    todo = _norm_prosa(' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S)))
    return pars, todo


def c_prosa_docx(s):
    """Lo que dejo pasar `§F120`: ninguna comprobacion comparaba la PROSA de los entregables.

    Cinco comprobaciones leen los `.docx` —modelos excluidos, sobriedad, OOXML sano y las dos de
    tablas— y ninguna miraba el texto. El desfase vivia ahi: los tres entregables afirmaban «19 de
    las 24 configuraciones» encima de una tabla de 26 filas que **si** estaba propagada, de modo
    que un documento contradiciendo a su propia tabla pasaba las cincuenta comprobaciones.

    Al construir esta aparecio que el desfase es mucho mayor de lo que `§F120` reporto: **diez
    parrafos del Markdown canonico no estan en el entregable**, no dos (`§F121`). Estan
    **declarados** abajo con su responsable —la pasada de maquetacion, porque insertarlos afecta al
    limite duro de 25 paginas y es decision del autor— de modo que no cortan, y **cualquier
    divergencia nueva si**.

    Como funciona. Para cada parrafo de prosa larga del Markdown se busca su mejor pareja en el
    `.docx` por similitud; si no la hay, se sondea el `.docx` con **cinco frases distintivas
    repartidas por el parrafo**, porque la prueba del arranque literal falla ante cualquier
    reformulacion —de los doce que no casaban, dos si estaban, reescritos—. Solo se declara ausente
    el parrafo del que no aparece **ninguna** sonda.
    """
    import difflib as _dl
    md_pars = _parrafos_md(s)
    if not md_pars:
        check('la prosa de los tres .docx sigue al Markdown', 0,
              ['no se extrajo ningun parrafo de prosa del Markdown'])
        return
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        base = os.path.basename(rel)
        pars, todo = _parrafos_docx(rel)
        if pars is None:
            fallos.append('%s no existe' % base)
            continue
        # Emparejar por fuerza bruta cuesta 78x193 comparaciones de `ratio()` por entregable, y
        # eso llevo el verificador de 0,67 s a 7,80 s y dejo la autoprueba —que lo ejecuta una vez
        # por artefacto vigilado— fuera de tiempo. Una puerta lenta deja de usarse, que es el
        # motivo por el que el gancho de commit corre sin red. Dos atajos, y **el resultado es
        # identico**: comprobado comparando la lista completa de fallos antes y despues.
        #
        #   1. Indice por los primeros 48 caracteres normalizados. La gran mayoria de los parrafos
        #      arrancan igual en los dos documentos, de modo que casan sin comparar nada.
        #   2. Para el resto, cascada `real_quick_ratio -> quick_ratio -> ratio`, que son cotas
        #      superiores sucesivamente mas caras y mas ajustadas: si la barata ya no alcanza el
        #      mejor puntaje visto, la cara no se calcula.
        indice = {}
        for j, b in enumerate(pars):
            indice.setdefault(b[:48], []).append(j)
        usados = set()
        for a in md_pars:
            mirados += 1
            libres = [j for j in indice.get(a[:48], []) if j not in usados]
            if libres:
                usados.add(libres[0])
                continue
            mejor, sc = None, 0.60
            m = _dl.SequenceMatcher(None)
            m.set_seq2(a[:400])
            for j, b in enumerate(pars):
                if j in usados:
                    continue
                m.set_seq1(b[:400])
                if m.real_quick_ratio() <= sc or m.quick_ratio() <= sc:
                    continue
                r = m.ratio()
                if r > sc:
                    mejor, sc = j, r
            if mejor is not None:
                usados.add(mejor)
                continue
            # sin pareja: se sondea antes de declararlo ausente
            pal = a.split()
            sondas = []
            for frac in (0.10, 0.28, 0.46, 0.64, 0.82):
                k = int(len(pal) * frac)
                fr = ' '.join(pal[k:k + 6])
                if len(fr) > 25:
                    sondas.append(fr)
            if any(x in todo for x in sondas):
                continue          # esta, con otra redaccion: no es una ausencia
            fallos.append('%s: parrafo ausente del entregable — «%s...»'
                          % (base, a[:58]))
    check('la prosa de los tres .docx sigue al Markdown', mirados, fallos,
          'lo que dejo pasar §F120; los diez parrafos ausentes estan declarados a nombre de la '
          'pasada de maquetacion, y una divergencia nueva si corta')


# --- 52. Las TABLAS y la BIBLIOGRAFIA del entregable siguen a las del Markdown -----------------
def _norm_celda(t):
    """Normaliza texto de celda. Decodifica las entidades XML ANTES de nada.

    Sin eso la Tabla 7 aparece como divergente y es identica: el `.docx` guarda «p&lt;0.001» donde
    el Markdown escribe «p<0.001». Fue el primer resultado de la comparacion y era un defecto de la
    comparacion, no del documento (§F126).
    """
    import html as _h
    import unicodedata as _u
    t = _u.normalize('NFC', _h.unescape(t))
    for a in (' ', ' ', ' '):
        t = t.replace(a, ' ')
    return ' '.join(re.sub(r'[`*_]', '', t).split())


def _tablas_md(s):
    """(numero de leyenda, filas) de cada tabla del Markdown, en orden."""
    lineas, out, i = s.split('\n'), [], 0
    while i < len(lineas):
        sep = (i + 1 < len(lineas)
               and set(lineas[i + 1].replace('|', '').replace(' ', '')) <= set('-:')
               and lineas[i + 1].strip().startswith('|'))
        if lineas[i].startswith('|') and sep:
            filas, j = [], i
            while j < len(lineas) and lineas[j].startswith('|'):
                c = [_norm_celda(x) for x in lineas[j].strip('|').split('|')]
                if not (set(''.join(c).replace(' ', '')) <= set('-:') and c):
                    filas.append(c)
                j += 1
            num = None
            for k in range(max(0, i - 4), i):
                m = re.match(r'_Tabla (\d+)\.', lineas[k].strip())
                if m:
                    num = int(m.group(1))
            out.append((num, filas))
            i = j
        else:
            i += 1
    return out


def _tablas_docx(rel):
    import zipfile as _z
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return None
    with _z.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    def T(q):
        return _norm_celda(' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', q, re.S)))
    out = []
    for b in re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S):
        filas = [[T(c) for c in re.findall(r'<w:tc>.*?</w:tc>', f, re.S)]
                 for f in re.findall(r'<w:tr[ >].*?</w:tr>', b, re.S)]
        if filas:
            out.append(filas)
    return out


def _biblio_docx(rel):
    """Numeros de entrada de la bibliografia del .docx, uno por parrafo."""
    import html as _h
    import zipfile as _z
    ruta = os.path.join(RAIZ, rel)
    if not os.path.exists(ruta):
        return None
    with _z.ZipFile(ruta) as z:
        x = z.read('word/document.xml').decode('utf-8')
    out = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
        t = _h.unescape(' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p, re.S))).strip()
        m = re.match(r'^\[(\d+)\]', t)
        if m:
            out.append(int(m.group(1)))
    return out


def c_tablas_y_biblio_docx(s):
    """Solo DOS de las veinte tablas se comparaban entre fuente y entregable.

    `c_prosa_docx` cerro el hueco de la prosa que dejo pasar `§F120`. Las tablas seguian igual:
    `auditar_afirmaciones.py` compara la 18 y la 19 celda a celda, y las otras dieciocho —incluida
    la **Tabla 7, la central del estudio**— no las comparaba nadie. Y la bibliografia tampoco.

    Lo que encontro al escribirse (`§F126`): dieciseis tablas identicas, y tres divergencias reales
    —la **Tabla 20 falta por completo** del entregable, la Tabla 9 tiene tres filas menos y la
    Tabla 3 una celda mas corta—, mas la **referencia [38] y sus cuatro citas**, ausentes. Las
    entradas [1] a [37] del entregable si estan y son contiguas, de modo que **no hay corrimiento
    de numeracion**: falta la ultima y nada mas.

    Todo eso queda **declarado** a nombre de la pasada de maquetacion, con el resto de `§F121`.
    """
    md_t = [(n, f) for n, f in _tablas_md(s) if f]
    fallos, mirados = [], 0
    citas_md = {int(x) for x in re.findall(r'\[(\d+)\]', s)}
    i = s.find('## Referencias')
    ent_md = {int(x) for x in re.findall(r'^\[(\d+)\]', s[i:], re.M)} if i >= 0 else set()
    for rel in DOCX_ENTREGABLES:
        base = os.path.basename(rel)
        dx = _tablas_docx(rel)
        if dx is None:
            fallos.append('%s no existe' % base)
            continue
        usados = set()
        for num, filas in md_t:
            mirados += 1
            et = 'Tabla %s' % num if num else 'tabla sin leyenda'
            cab = ' | '.join(filas[0])[:70]
            pareja = next((j for j, fb in enumerate(dx)
                           if j not in usados and fb and ' | '.join(fb[0])[:70] == cab), None)
            if pareja is None:
                fallos.append('%s: %s no esta en el entregable (%d filas, cab: %s)'
                              % (base, et, len(filas), cab[:40]))
                continue
            usados.add(pareja)
            fb = dx[pareja]
            if len(fb) != len(filas):
                fallos.append('%s: %s tiene %d filas y el Markdown %d'
                              % (base, et, len(fb), len(filas)))
                continue
            k = next((z for z in range(len(filas)) if filas[z] != fb[z]), None)
            if k is not None:
                fallos.append('%s: %s, fila %d difiere — .md %s / .docx %s'
                              % (base, et, k, filas[k][:2], fb[k][:2]))
        # bibliografia
        mirados += 1
        ent = _biblio_docx(rel)
        faltan = sorted(ent_md - set(ent or []))
        if faltan:
            fallos.append('%s: le faltan las entradas de bibliografia %s' % (base, faltan))
        if ent and sorted(ent) != list(range(min(ent), max(ent) + 1)):
            fallos.append('%s: las entradas de bibliografia no son contiguas' % base)
    check('las tablas y la bibliografia de los .docx siguen al Markdown', mirados, fallos,
          'las entidades XML se decodifican antes de comparar; sin eso la Tabla 7 sale '
          'divergente siendo identica')


# --- 53. Los ENCABEZADOS del entregable siguen a los del Markdown -----------------------------
def c_encabezados_docx(s):
    """La ultima pieza de estructura sin comparar, y encontro que falta una subseccion entera.

    Las comprobaciones 51 y 52 cerraron la prosa, las tablas y la bibliografia. Los encabezados
    quedaban fuera: la 51 solo mira parrafos de mas de 160 caracteres. Y con diez parrafos, una
    tabla y una referencia ausentes, cabia que faltara una seccion — y falta (`§F127`).

    Tres normalizaciones, las tres necesarias, y las tres se descubrieron dando falsos positivos:

    1. **Los `#` dentro de un bloque de codigo no son encabezados.** Sin esto, tres comentarios de
       un bloque de ejemplo (`# Modo baseline (sin RAG)`) salian como titulos ausentes.
    2. **El numero de seccion no esta en el texto del encabezado del `.docx`.** Lo pone la
       numeracion multinivel de Word, que `CLAUDE.md` advierte que no hay que regenerar. Sin
       quitarlo del lado del Markdown, los siete capitulos salian como ausentes.
    3. **La caja no coincide.** El `.docx` titula en otra capitalizacion, de modo que la
       comparacion va en `casefold`.

    Con las tres, de 69 encabezados quedan **seis** que no aparecen con estilo de encabezado, y
    **cinco de los seis estan en el cuerpo** con otro estilo —el titulo, «Referencias» y los tres
    del bloque de codigo—. El sexto falta por completo.
    """
    import html as _h
    import unicodedata as _u
    import zipfile as _z

    def norm(t):
        t = _u.normalize('NFC', _h.unescape(t))
        for a in (' ', ' ', ' '):
            t = t.replace(a, ' ')
        return ' '.join(re.sub(r'[`*_#]', '', t).split()).casefold()

    def sin_num(t):
        return re.sub(r'^\d+(\.\d+)*\.?\s*', '', t).strip()

    # los `#` de dentro de un bloque de codigo no son encabezados
    md, en_codigo = [], False
    for l in s.split('\n'):
        if l.startswith('```'):
            en_codigo = not en_codigo
            continue
        if en_codigo:
            continue
        m = re.match(r'^(#{1,4})\s+(.+)$', l)
        if m:
            md.append((len(m.group(1)), norm(m.group(2))))
    if not md:
        check('los encabezados de los .docx siguen al Markdown', 0,
              ['no se extrajo ningun encabezado del Markdown'])
        return
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        base = os.path.basename(rel)
        ruta = os.path.join(RAIZ, rel)
        if not os.path.exists(ruta):
            fallos.append('%s no existe' % base)
            continue
        with _z.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        dx = []
        for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
            e = re.search(r'<w:pStyle w:val="([^"]+)"', p)
            if not e or 'eading' not in e.group(1):
                continue
            t = norm(' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', p, re.S)))
            if t:
                dx.append(t)
        conj = set(dx) | {sin_num(t) for t in dx}
        todo = norm(' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S)))
        for niv, t in md:
            mirados += 1
            if t in conj or sin_num(t) in conj:
                continue
            if sin_num(t) in todo:
                continue          # esta en el cuerpo con otro estilo: no es una ausencia
            fallos.append('%s: falta la seccion «%s» (H%d), y su texto no esta en ninguna parte'
                          % (base, t[:62], niv))
    check('los encabezados de los .docx siguen al Markdown', mirados, fallos,
          'los # de un bloque de codigo no cuentan, el numero lo pone la numeracion de Word y la '
          'comparacion va en casefold: sin las tres, 10 falsos positivos')


# --- 54. Las FIGURAS del entregable, y que ninguna cita quede colgando ------------------------
def c_figuras_docx(s):
    """El ultimo tipo de contenido sin comparar entre fuente y entregable.

    Las comprobaciones 51, 52 y 53 cerraron la prosa, las tablas, la bibliografia y los
    encabezados. Faltaban las **imagenes**, y las dos figuras del informe **no estan en ninguno de
    los tres entregables**: cero elementos `<w:drawing>` y cero leyendas «Figura N.» (`§F128`).

    Se comprueban dos cosas, y la segunda es la que evita un defecto peor que la ausencia:

    1. Que cada figura que el Markdown declara —por su leyenda `_Figura N._`— tenga una imagen
       dibujada en el entregable.
    2. Que **ninguna cita a «Figura N» quede colgando**. Hoy el entregable **no** las cita, de modo
       que es incompleto pero coherente; si alguien inserta la prosa que las menciona sin insertar
       las imagenes, el documento pasaria a prometer una figura que no muestra, y eso si es un
       defecto y no una carencia.

    Los ficheros de media del `.docx` con plantilla **no** son las figuras: son las siete
    referencias del encabezado y el pie institucionales, y por eso se cuentan los `<w:drawing>` del
    cuerpo y no los ficheros del paquete.
    """
    import zipfile as _z
    leyendas = sorted({int(x) for x in re.findall(r'_Figura (\d+)\.', s)})
    if not leyendas:
        check('las figuras del Markdown estan en los tres .docx', 0,
              ['el Markdown no declara ninguna figura con leyenda «_Figura N._»'])
        return
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        base = os.path.basename(rel)
        ruta = os.path.join(RAIZ, rel)
        if not os.path.exists(ruta):
            fallos.append('%s no existe' % base)
            continue
        with _z.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        dibujos = len(re.findall(r'<w:drawing>', x))
        txt = ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))
        citadas = sorted({int(y) for y in re.findall(r'[Ff]igura (\d+)', txt)})
        for n in leyendas:
            mirados += 1
            if dibujos == 0:
                fallos.append('%s: la Figura %d del Markdown no esta (cero <w:drawing> en el '
                              'cuerpo)' % (base, n))
        # citas colgantes: prometidas en el texto y sin imagen que mostrar
        mirados += 1
        if citadas and dibujos == 0:
            fallos.append('%s: cita las figuras %s y no tiene ninguna imagen en el cuerpo — una '
                          'cita colgante es peor que la ausencia' % (base, citadas))
    check('las figuras del Markdown estan en los tres .docx', mirados, fallos,
          'se cuentan los <w:drawing> del cuerpo, no los ficheros de word/media: los del .docx '
          'con plantilla son el encabezado y el pie institucionales')


# --- 55. Las propias DECLARACIONES no silencian mas de lo que les toca ------------------------
def c_declaraciones():
    """La comprobacion de la comprobacion, sobre el mecanismo que ya carga 25 declaraciones.

    Cada clave de `FALLOS_DECLARADOS` es un fragmento que se busca en el mensaje del fallo. **Una
    clave demasiado generica taparia fallos que no cubre**, y eso no lo detectaba nada: el resumen
    los contaria como declarados y el codigo de salida seguiria siendo 0. Con cinco declaraciones
    era improbable; con veinticinco conviene comprobarlo (`§F129`).

    Tres cosas, y las tres pasan hoy:

    1. **Ninguna clave toca mas de una comprobacion.** Si una lo hiciera, estaria silenciando algo
       que su motivo no describe.
    2. **Ninguna clave contiene a otra.** Dos claves anidadas hacen que la mas corta se coma los
       fallos de la mas larga, y el motivo que se lee entonces es el equivocado.
    3. **Ninguna clave deja de tapar algo sin explicacion.** Una declaracion que no casa con ningun
       fallo esta caducada —el defecto se arreglo y nadie retiro la declaracion— o pertenece a una
       comprobacion que no ha corrido. El unico caso legitimo hoy es `c_urls`, que solo corre con
       `--red`; **con `--red` esa excusa desaparece** y la comprobacion lo exige.

    Se ejecuta al final, porque necesita los resultados de todas las demas.
    """
    mensajes = [(n, f) for n, _e, fs, _nt in resultados for f in fs]
    claves = list(FALLOS_DECLARADOS)
    fallos, mirados, sin_red = [], 0, 0
    con_red = '--red' in sys.argv

    def _ref(i_, k_):
        """Nombra una declaracion SIN escribirla entera, o se silenciaria a si misma.

        Primera version del defecto que esta comprobacion existe para cazar, cometido por ella:
        el mensaje incluia la clave literal, de modo que la propia declaracion lo tapaba y salia
        como DECLARADO en lugar de como nuevo. Se imprime un **prefijo estricto** —siempre mas
        corto que la clave—, que por construccion no puede contenerla, mas su numero de orden
        para poder localizarla.
        """
        corte = max(6, min(len(k_) - 1, 24))
        return 'n.%d «%s…»' % (i_ + 1, k_[:corte])
    for k in claves:
        mirados += 1
        tocados = {n for n, f in mensajes if k in f}
        if len(tocados) > 1:
            fallos.append('la declaracion %s silencia fallos de %d comprobaciones distintas '
                          '(%s): es demasiado generica y su motivo no las describe todas'
                          % (_ref(claves.index(k), k), len(tocados),
                             '; '.join(sorted(tocados))[:110]))
        if not tocados:
            if k in SOLO_CON_RED and not con_red:
                sin_red += 1          # legitimo y enumerado: no es un fallo
            elif con_red:
                fallos.append('la declaracion %s no tapa ningun fallo ni con --red: esta '
                              'caducada y hay que retirarla' % _ref(claves.index(k), k))
            else:
                fallos.append('la declaracion %s no tapa ningun fallo y no esta en '
                              'SOLO_CON_RED: o esta caducada, o su comprobacion no corrio'
                              % _ref(claves.index(k), k))
    for i, a in enumerate(claves):
        for b in claves[i + 1:]:
            mirados += 1
            if a in b or b in a:
                fallos.append('las declaraciones %s y %s estan anidadas: la mas corta se come '
                              'los fallos de la otra y se lee el motivo equivocado'
                              % (_ref(claves.index(a), a), _ref(claves.index(b), b)))
    nota = ('se ejecuta al final porque lee los resultados de las demas')
    if sin_red:
        nota += '; %d declaracion(es) de SOLO_CON_RED no tapan nada sin red, y es legitimo' % sin_red
    check('las declaraciones no silencian mas de lo que les toca', mirados, fallos, nota)


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


# --- 56. Frases retiradas de la fuente que no pueden sobrevivir en el entregable -----------------
# Las FRASES RETIRADAS: lo que se corrigio en el Markdown y todavia se afirma en los .docx.
#
# La comprobacion de prosa va en UNA sola direccion, del Markdown al entregable, y solo declara
# ausente un parrafo del que no aparece NINGUNA de sus cinco sondas. Eso deja pasar el caso
# peligroso: un parrafo cuyo ARRANQUE sigue igual y cuyo FINAL se corrigio. Las sondas del arranque
# casan, el parrafo se da por presente, y el entregable sigue afirmando lo que la fuente ya
# desmintio.
#
# Ocurrio el 2026-09-09 con la frase «La re-corrida completa pendiente unifica el presupuesto en
# 4096», que era cierta al escribirla y dejo de serlo cuando la re-corrida se ejecuto, el 8 de
# septiembre. Se corrigio en el Markdown y el verificador no dijo nada, porque el resto del parrafo
# no habia cambiado.
#
# Esta comprobacion va al reves: toma las frases que la fuente RETIRO y exige que tampoco esten en
# el entregable. Es lo unico que protege de que el documento que lee el tribunal afirme algo que el
# autor ya corrigio. Cada entrada lleva por que se retiro y por que la sustituye.
RETIRADAS = (
    ('Conviene subrayar que se trata de una penalización exclusivamente de precisión',
     'frase del párrafo largo de §3.3 sobre Locations, comprimido el 2026-09-09 (§F166) porque el '
     'autor lo encontró confuso y temió que un comité lo leyera como una mala decisión histórica '
     'no resuelta. El párrafo nuevo abre diciendo que el defecto ya está corregido y no afecta a '
     'ningún resultado vigente, y remite el detalle histórico al Anexo I'),
    ('Vale la pena señalar una particularidad de procedencia',
     'nota de §5.3 sobre un F1 de 79,03% de una corrida cuyos datos por registro se perdieron '
     'por sobrescritura y no podian recalcularse. Retirada por completo el 2026-09-09 (§F163): '
     'el autor pidio no mencionar datos sin evidencia real verificable, aunque sea en una '
     'anecdota de robustez metodologica'),
    ('re-corrida completa pendiente',
     'la re-corrida se ejecuto el 2026-09-08 y esta completa: 13 corridas __N120, todas con '
     'max_tokens=4096. Declararla pendiente es falso hoy. Retirada el 2026-09-09 (§F160): el '
     'parrafo de gpt-oss:20b ya no declara dos mediciones ni una reserva de comparabilidad — la '
     'unica corrida vigente es la re-corrida adoptada, y sus cifras son las de la Tabla 7'),
    ('la de referencia es la primera',
     'afirmaba que la corrida de 2048 tokens (previa a la re-corrida) era la referencia de la '
     'Tabla 7; falso desde que la re-corrida adoptada, a 4096 tokens para los trece modelos, es '
     'la unica fuente de la Tabla 7. Retirada el 2026-09-09 (§F160)'),
    ('Nueve de los trece modelos mejoran',
     'recuento equivocado: son once de los trece los que mejoran con RAG segun el signo de la '
     'columna Δ RAG de la Tabla 7, no nueve. Retirada el 2026-09-09 (§F161)'),
    ('−0,54 y −0,18 puntos en los dos de 31B',
     'cifras equivocadas: los dos modelos de 31B mejoran con RAG (+0,81 y +0,97 puntos), no '
     'empeoran; recalculado del CSV consolidado adoptado. Retirada el 2026-09-09 (§F161)'),
    ('Grupos con más de una corrida sobre N=120, con el motivo de la sustitución y la evidencia',
     'era la leyenda de la Tabla 20 (Anexo I), retirada el 2026-09-09 junto con la tabla misma: '
     'ocho filas de F1 de corridas descartadas que duplicaban, con apariencia de resultado '
     'vigente, el mismo patron que origino la pregunta sobre gemma4:12b-mlx (§F160)'),
    ('tomados de OpenSanctions',
     'el proveedor esta mal atribuido: PROCEDENCIA.md declara treasury.gov/ofac/downloads/sdn.csv '
     'y no menciona OpenSanctions. La fuente dice ya «la lista SDN del Departamento del Tesoro»'),
    ('de la base de datos OpenSanctions',
     'idem: es la atribucion del corpus del Anexo F, y es una afirmacion falsa, no una ausencia'),
    ('cifras de la última columna',
     'la ultima columna de la Tabla 1 es Idioma; las cifras estan en la de desempeno publicado'),
    ('Composición de los falsos positivos sobre el consolidado publicado (N=120, veintiséis grupos), previo a la',
     'era la leyenda de la Figura 1 (composicion de FP), retirada el 2026-09-12 a peticion expresa '
     'del autor (FINDINGS §F170): el grafico ilustraba un defecto de medicion ya corregido y el '
     'autor considero que no aportaba al cuerpo. El script y el artefacto que la generaban no se '
     'tocan; la fraccion en prosa de §3.3 (66,0 %, 12 852 de 19 464) se conserva integra'),
    ('la Figura 1 lo ilustra',
     'referencia colgante a la Figura 1 retirada (§F170): la frase parentetica se quito de §3.3 '
     'junto con la figura, sin tocar la fraccion que la acompana'),
    ('sin ninguna forma de acertar en ella',
     'frase del parrafo largo de §3.3 sobre Locations (~240 palabras), comprimido a dos frases '
     'el 2026-09-12 (FINDINGS §F170, precision de CLAUDE.md sobre integridad de la medicion desde '
     'el 8 de septiembre): el autor considero que un defecto ya superado por la re-corrida no '
     'necesita desarrollar su mecanismo en el cuerpo. La fraccion 66,0 % / 12 852 de 19 464 y la '
     'remision al Anexo I se conservan'),
    ('no persistido en `results/`',
     'clausula de §7.1 conclusion 6 sobre el dict-RAG (v1.0), un sondeo N=5 sin datos guardados '
     'que remitia ademas a una corrida ya superada. Retirada el 2026-09-12 (FINDINGS §F172): el '
     'autor pidio ejecutar la candidata de LEARNING §L80 sobre cifras de corridas sin evidencia'),
    ('iba de −0,082 a +0,155 de F1',
     'detalle del parrafo viejo de §7.2 punto 7 (mojibake), comprimido el 2026-09-12 (§F172): las '
     'cuatro cifras de rango de efecto se conservan integras en el Anexo H.3, solo se retiro la '
     'repeticion en el cuerpo'),
    ('La solución resultó más barata de lo previsto',
     'frase del parrafo viejo de §7.2 punto 8 (Locations), comprimido el 2026-09-12 (§F172): el '
     'mecanismo completo (105 de 120 articulos ya anotados en CoNLL-2002, conversor que '
     'descartaba la lista) se conserva integro en el Anexo I, solo se retiro la repeticion en el '
     'cuerpo'),
    ('Se documenta por tanto como limitación (§5.3.1) y como línea de trabajo futuro',
     'el Anexo H.4 declaraba la normalizacion de codificacion como trabajo futuro pendiente '
     '(§7.2, punto 7) cuando ya estaba hecha desde la re-corrida del 8 de septiembre: quedo '
     'obsoleta sin que nadie la actualizara. Corregida el 2026-09-12 (§F172) para declarar que '
     'la re-corrida ya la ejecuto'),
)


def c_frases_retiradas(s):
    """Ninguna frase que la fuente retiro puede seguir viva en los tres entregables."""
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        base = os.path.basename(rel)
        txt = _texto_docx(os.path.join(RAIZ, rel))
        if txt is None:
            fallos.append('%s no se pudo leer' % base)
            continue
        plano = ' '.join(txt.split())
        for frase, motivo in RETIRADAS:
            mirados += 1
            if frase in plano:
                fallos.append('%s todavia afirma «%s» — %s' % (base, frase, motivo))
    # Y la otra mitad, que es la que evita que esta comprobacion se quede obsoleta en silencio:
    # una frase retirada que TAMPOCO este ya en el Markdown es lo esperado; una que SIGA en el
    # Markdown significa que la retirada no se aplico a la fuente, o que la entrada esta mal escrita.
    for frase, _motivo in RETIRADAS:
        mirados += 1
        if frase in ' '.join(s.split()):
            fallos.append('«%s» figura como retirada y sigue en el Markdown canonico: o no se '
                          'corrigio la fuente, o la entrada de RETIRADAS esta mal escrita' % frase)
    check('ninguna frase retirada sobrevive en los entregables', mirados, fallos)

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


# 17 el 2026-09-09 al medirlo por primera vez; 16 tras partir el run de §3.3, que era el
# unico de los 17 introducido por una edicion propia. Baja segun se propague la limpieza.
BOLD_CUERPO_BASE = 4    # 8 -> 4 el 2026-09-17 (Claude Desktop, §2.28). La comprobacion volvio a
                        # pedir bajar la base al detectar la mejora: el .md perdio resaltes en la
                        # compresion de §3.3 y del Anexo I. El diagnostico de los que quedan sigue
                        # en §2.25: NO son resaltes anadidos por el renderizador, sino negritas del
                        # Markdown que el constructor de `marcados` no representa (negrita con
                        # cursiva dentro, y negrita que cruza una linea de cita).


PDF_RAIZ = 'Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.pdf'
PDF_ENVIADO = ('doc/versions/enviados/'
               '2026-09-08_Informe_Final_Tesina_NER_ENVIADO-AL-PROFESOR-GUIA.pdf')


# `Locations` puntua contra el vacio en todas las corridas y eso es SABIDO: los prompts piden tres
# categorias y los corpus anotan dos (§F53). El informe lo declara en §3.3 y publica en paralelo la
# metrica restringida a las dos anotadas. La comprobacion de abajo lo espera, de modo que no cuenta
# como fallo y **sigue siendo sensible a que aparezca otra**, que es lo que hay que impedir. No se
# declara como fallo tolerado a proposito: eso cegaria la comprobacion entera (§L64).
CATEGORIA_SIN_REFERENCIA_SABIDA = 'Locations'


CORPUS = 'data/benchmark_balanced_120.json'
# Palabras funcion exclusivas de cada lengua. No hay biblioteca de deteccion de idioma en el
# interprete del sistema y no se anade una dependencia por esto: con articulos, preposiciones y
# auxiliares basta para separar noticias en espanol de noticias en ingles, y el margen que sale
# —105 frente a 15— no es de los que dependan del umbral.
PAL_ES = {'que', 'de', 'la', 'el', 'los', 'las', 'del', 'se', 'por', 'para', 'con', 'una', 'como',
          'pero', 'este', 'esta', 'sus', 'ha', 'han', 'fue', 'anos', 'segun', 'mas', 'tambien',
          'sobre', 'entre', 'desde'}
PAL_EN = {'the', 'of', 'and', 'to', 'in', 'that', 'for', 'with', 'was', 'were', 'has', 'have',
          'been', 'from', 'said', 'which', 'their', 'this', 'these', 'on', 'at', 'by', 'as', 'an',
          'it', 'be'}


NUMERALES = {'un': 1, 'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6,
             'siete': 7, 'ocho': 8, 'nueve': 9, 'diez': 10}


def c_numeral_soberania(s):
    """El numeral en palabras del coste de la soberania cuadra con la resta que lo precede.

    El informe escribe, dos veces, «la variante alojada alcanza **80,42 %** frente al **76,55 %**
    del mejor local … la soberania cuesta del orden de **cuatro puntos** de F1». La resta esta a la
    vista dos lineas antes, de modo que el numeral tiene que cuadrar con ella.

    **Existe porque yo rompi esto.** El 2026-09-09, al propagar las cifras del F1 restringido a los
    `.docx`, cambie 81,45 por 80,42 y 76,85 por 76,55 y **deje la palabra «cinco»**, correcta con
    las viejas —4,60— y falsa con las nuevas —3,87—. Los tres entregables quedaron afirmando en una
    conclusion algo que su propia resta desmentia. Lo encontro la lectura del informe como lector,
    no una comprobacion: de ahi esta.

    La clase de defecto es general y merece nombre: **propagar una cifra sin su prosa dependiente
    deja el documento peor que antes**, porque antes era coherente con datos viejos y despues es
    incoherente consigo mismo. Se comprueba en el Markdown y en los tres `.docx`.
    """
    import zipfile as _zip
    # El informe usa «alcanza» en §6.1 y «obtiene» en la conclusion 3, y el .docx conserva solo la
    # segunda. Un patron con un solo verbo encuentra el Markdown y NO los entregables, que es justo
    # donde estaba el defecto: la comprobacion habria dado por bueno el documento roto mientras
    # verificaba el que estaba bien. Se aceptan los dos verbos.
    # Dos formas de resolucion: «cuesta N puntos» (numeral en palabras) o, cuando la resta es
    # menor que un punto entero, «cuesta menos de un punto». La segunda aparecio el 2026-09-09 al
    # adoptar el consolidado nuevo, donde la diferencia baja a 0,66 pp y ningun numeral entero la
    # describe con precision sin exagerar.
    pat = re.compile(r'(?:alcanza|obtiene)\s+(\d+),(\d+)\s*%\s*frente al\s+(\d+),(\d+)\s*%\s*'
                     r'del mejor local(.{0,200}?)cuesta[^.]{0,28}?\b(?:('
                     + '|'.join(NUMERALES) + r')\s+puntos|menos de un punto)', re.S)
    fuentes = [('el Markdown', s)]
    for rel in DOCX_ENTREGABLES:
        ruta = os.path.join(RAIZ, rel)
        if not os.path.exists(ruta):
            fuentes.append((os.path.basename(rel), None))
            continue
        with _zip.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        fuentes.append((os.path.basename(rel),
                        ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))))
    fallos, mirados = [], 0
    for etiq, txt in fuentes:
        mirados += 1
        if txt is None:
            fallos.append('no existe %s' % etiq)
            continue
        hallados = list(pat.finditer(txt))
        if not hallados:
            fallos.append('%s: no se encuentra la frase del coste de la soberania con su numeral '
                          'en palabras: revisar si se reformulo' % etiq)
            continue
        for m in hallados:
            mirados += 1
            alto = float('%s.%s' % (m.group(1), m.group(2)))
            bajo = float('%s.%s' % (m.group(3), m.group(4)))
            real = alto - bajo
            if m.group(6) is None:
                # se dijo «menos de un punto»: valido solo si la resta real es, en efecto, < 1
                if real >= 1.0 or real < 0.0:
                    fallos.append('%s: dice «menos de un punto» y la resta que lo precede da %.2f '
                                  '(%.2f - %.2f), que no es menor que uno'
                                  % (etiq, real, alto, bajo))
                continue
            dicho = NUMERALES[m.group(6)]
            if abs(real - dicho) > 0.5:
                fallos.append('%s: dice «%s puntos» y la resta que lo precede da %.2f '
                              '(%.2f - %.2f). Propagar una cifra sin su prosa dependiente deja el '
                              'documento incoherente consigo mismo'
                              % (etiq, m.group(6), real, alto, bajo))
    check('el numeral del coste de la soberania cuadra con su resta', mirados, fallos,
          'lo rompi yo el 2026-09-09 al propagar cifras sin la prosa que dependia de ellas')


def c_resumen_docx(s):
    """El resumen y el abstract de los `.docx` dicen lo que dice el Markdown, palabra por palabra.

    `CLAUDE.md` singulariza este par: «Resumen y abstract van fundidos, sincronizados y en la
    primera pagina. Deben decir **exactamente lo mismo** en ambos idiomas… si divergen, el
    documento deja de ser coherente para un lector que compare ambas versiones.» Es la primera
    pagina y es lo primero que se lee.

    Y divergio en silencio. El 2026-09-09 los tres `.docx` abrian con «Las instituciones sujetas a
    regulaciones AML/KYC» mientras el Markdown decia «Las instituciones **financieras** sujetas
    a», que es lo que concuerda con el «**Financial** institutions» del abstract. Una palabra, en
    la primera pagina, en el par que la regla protege expresamente.

    Lo instructivo es la direccion del error: `PROPAGACION-PENDIENTE-DOCX-20260908.md` anotaba lo
    **contrario** —que el `.docx` tenia razon y el Markdown estaba mal—, y era cierto **el dia
    anterior**. El Markdown se corrigio y el `.docx` no recibio el cambio, de modo que la nota
    quedo describiendo un estado invertido. Una nota de propagacion sin fecha de caducidad envejece
    hacia la mentira.

    Se compara el texto **completo** de los dos bloques, normalizando espacios, no solo su primera
    frase: una divergencia puede estar en cualquier punto.
    """
    import zipfile as _zip
    # El Markdown escribe el enfasis con marcadores —`*few-shot*`, `**cifra**`, backticks— y el
    # .docx lo lleva como formato real, de modo que comparar en crudo da falsos positivos: la
    # primera version reporto una divergencia en la palabra 153 que era solo un par de asteriscos.
    # Se comparan los TEXTOS, no el marcado.
    def norm(z):
        z = re.sub(r'\*\*([^*]+)\*\*', r'\1', z)
        z = re.sub(r'\*([^*]+)\*', r'\1', z)
        z = z.replace('`', '')
        return ' '.join(z.split())
    L = s.split('\n')
    # el resumen y el abstract del Markdown son los parrafos que siguen a sus encabezados
    def _md(enc):
        for k, l in enumerate(L):
            if l.strip() == enc:
                for m in range(k + 1, min(k + 6, len(L))):
                    if L[m].strip():
                        return norm(L[m])
        return None
    res_md, abs_md = _md('## Resumen'), _md('## Abstract')
    if not res_md or not abs_md:
        check('el resumen y el abstract de los .docx coinciden con el Markdown', 0,
              ['no se encuentran el resumen o el abstract en el Markdown'])
        return
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        ruta = os.path.join(RAIZ, rel)
        base = os.path.basename(rel)
        if not os.path.exists(ruta):
            mirados += 1
            fallos.append('no existe el entregable %s' % rel)
            continue
        with _zip.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        # En el .docx con la plantilla institucional los dos bloques llevan el estilo `abstract`.
        # El .docx sin plantilla NO usa esos estilos —la primera version reportaba «hay 0» y era un
        # defecto del detector, no del documento—, de modo que ahi se localizan por el parrafo que
        # sigue a los encabezados RESUMEN y ABSTRACT.
        parrafos = []
        for m in re.finditer(r'<w:p[ >].*?</w:p>', x, re.S):
            par = m.group(0)
            txt = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', par, re.S)).strip()
            if txt:
                parrafos.append((txt, 'w:val="abstract"' in par))
        bloques = [norm(z) for z, es in parrafos if es]
        if len(bloques) < 2:
            bloques = []
            for k, (z, _) in enumerate(parrafos):
                if z.strip().upper() in ('RESUMEN', 'ABSTRACT') and k + 1 < len(parrafos):
                    bloques.append(norm(parrafos[k + 1][0]))
        mirados += 1
        if len(bloques) < 2:
            fallos.append('%s: no se localizan los dos bloques de resumen y abstract, ni por el '
                          'estilo «abstract» ni tras los encabezados RESUMEN y ABSTRACT'
                          % base)
            continue
        for etiq, esperado, hallado in (('el resumen', res_md, bloques[0]),
                                        ('el abstract', abs_md, bloques[1])):
            mirados += 1
            if hallado == esperado:
                continue
            # localizar la primera palabra que difiere, para que el mensaje sirva
            a, b = esperado.split(), hallado.split()
            pos = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            fallos.append('%s: %s difiere del Markdown en la palabra %d de %d — el .md dice «%s» y '
                          'el .docx «%s»'
                          % (base, etiq, pos + 1, len(a),
                             ' '.join(a[max(0, pos - 2):pos + 3]),
                             ' '.join(b[max(0, pos - 2):pos + 3])))
    check('el resumen y el abstract de los .docx coinciden con el Markdown', mirados, fallos,
          'CLAUDE.md exige que digan exactamente lo mismo, y estan en la primera pagina')


def c_indice(s):
    """El indice de contenidos coincide con la estructura real, anclajes incluidos.

    Un indice desfasado es un defecto clasico y silencioso: nadie lo relee, y el documento va a
    seguir editandose en la pasada de maquetacion —entran la Tabla 20, dos figuras y varios
    parrafos—. Se comprueban tres cosas: que cada anclaje del indice corresponda a un encabezado
    real, que el texto del enlace este contenido en el encabezado al que apunta, y que **ningun
    encabezado de nivel dos se quede sin entrada**.

    Comprobado el 2026-09-09: **9 entradas y 9 encabezados**, sin un solo desajuste. Los nueve son
    los siete capitulos numerados mas Referencias y Anexos, que es lo que la norma cuenta como
    «nueve capitulos». Los anexos son **nueve, A-I**, no ocho: la revision previa decia A-H y el
    propio registro del proyecto ya lo habia corregido.

    **Trampa del anclaje, que costo una pasada.** El texto del enlace es «Introduccion» —el numero
    va como marcador de la lista— pero el encabezado es `## 1. Introduccion`, de modo que el
    anclaje correcto es `1-introduccion`. Derivar el anclaje esperado del **texto del enlace** da
    siete fallos de nueve, todos falsos. Se deriva del **encabezado**, que es de donde lo saca
    cualquier renderizador. Siete de nueve fallando fue la senal de §L66: cuando una comprobacion
    nueva reporta casi todo mal, la primera hipotesis es que esta mal ella.
    """
    def _ancla(titulo):
        z = titulo.strip().lower().replace('\u2014', '').replace('\u2013', '')
        z = re.sub(r'[^\w\s-]', '', z, flags=re.U)
        return re.sub(r'\s+', '-', z.strip())

    i = s.find('## \u00cdndice de contenidos')
    if i < 0:
        check('el indice coincide con la estructura real', 0,
              ['no se encuentra el «Indice de contenidos»'])
        return
    j = s.find('\n## ', i + 5)
    entradas = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', s[i:j if j > 0 else len(s)])
    enc = [m.group(1).strip() for m in re.finditer(r'^## (.+)$', s, re.M)]
    enc = [e for e in enc if e not in ('Resumen', 'Abstract', '\u00cdndice de contenidos')]
    if not entradas or not enc:
        check('el indice coincide con la estructura real', 0,
              ['el indice no trae entradas o no hay encabezados de nivel dos'])
        return
    reales = {_ancla(e): e for e in enc}
    fallos, mirados = [], 0
    for titulo, ancla in entradas:
        mirados += 1
        if ancla not in reales:
            fallos.append('el anclaje «#%s» del indice no corresponde a ningun encabezado' % ancla)
        elif titulo.strip().lower() not in reales[ancla].lower():
            fallos.append('la entrada «%s» apunta al encabezado «%s», que no la contiene'
                          % (titulo, reales[ancla]))
    usadas = {a for _, a in entradas}
    for e in enc:
        mirados += 1
        if _ancla(e) not in usadas:
            fallos.append('el encabezado «%s» no tiene entrada en el indice' % e)
    check('el indice coincide con la estructura real', mirados, fallos,
          '%d entradas y %d encabezados de nivel dos' % (len(entradas), len(enc)))


def c_ninguna_comprobacion_huerfana(s):
    """Ninguna comprobacion definida puede quedarse sin ejecutarse.

    Anadir una funcion `c_*` y olvidar registrarla en el orquestador la deja **silenciosamente
    ausente**: el fichero la contiene, se lee como si vigilara algo, y no corre nunca. Es el mismo
    defecto que §L62 describe para una herramienta que aborta —una comprobacion que no se ejecuta
    es indistinguible de una que no existe— pero mas dificil de notar, porque aqui no hay ni un
    traceback.

    El 2026-09-09 se audito a mano: **40** funciones definidas y **39** registradas, y la que
    faltaba resulto ser `c_urls`, que se invoca aparte porque depende de `--red`. Ninguna
    huerfana. Habiendo hecho la auditoria a mano, corresponde mecanizarla (§L61): la proxima vez
    que alguien anada una comprobacion y no la registre, esto lo dira.

    Se comprueba sobre la **fuente** del propio fichero, que es la unica forma de ver una funcion
    que nunca se llama. Y se declara el recuento, para que la comprobacion no pueda pasar mirando
    cero funciones.

    **Solo vigila una direccion**, y a proposito. El caso inverso —registrada y no definida— no
    necesita comprobacion: levanta un `NameError` en la linea del `ejecutar` y aborta el
    verificador con salida 1. Python lo detecta antes y de forma mas terminante.
    """
    ruta = os.path.abspath(__file__)
    try:
        with open(ruta, encoding='utf-8') as fh:
            src = fh.read()
    except OSError as e:
        check('ninguna comprobacion queda sin ejecutarse', 0,
              ['no se puede leer la propia fuente: %s' % e])
        return
    definidas = set(re.findall(r'^def (c_\w+)', src, re.M))
    registradas = set(re.findall(r'ejecutar\((c_\w+)', src))
    directas = set(re.findall(r'^\s+(c_\w+)\(', src, re.M)) - registradas
    fallos = []
    if len(definidas) < 20:
        fallos.append('solo se detectan %d funciones c_*: el patron esta roto y esta comprobacion '
                      'no acredita nada' % len(definidas))
        check('ninguna comprobacion queda sin ejecutarse', len(definidas), fallos)
        return
    huerfanas = sorted(definidas - registradas - directas)
    if huerfanas:
        fallos.append('%d comprobacion(es) definida(s) y nunca ejecutada(s): %s. Registrarlas en '
                      'el orquestador o retirarlas; una comprobacion que no corre es '
                      'indistinguible de una que no existe'
                      % (len(huerfanas), ', '.join(huerfanas)))
    # El caso inverso —registrada y no definida— NO se comprueba aqui, y la primera version si lo
    # intentaba. Es codigo vacuo: `ejecutar(c_inexistente, s)` levanta un NameError en la propia
    # linea, de modo que el verificador aborta con salida 1 antes de que esta comprobacion pueda
    # opinar. Comprobado el 2026-09-09 mutandolo: sale un traceback, no un fallo. Python lo detecta
    # antes y de forma mas terminante que cualquier rama que se escriba aqui, y una rama que no
    # puede dispararse es peor que no tenerla: se lee como cobertura y no cubre nada.
    check('ninguna comprobacion queda sin ejecutarse', len(definidas), fallos,
          '%d definidas · %d por el orquestador · %d invocadas aparte (%s)'
          % (len(definidas), len(registradas), len(directas),
             ', '.join(sorted(directas)) or 'ninguna'))


def c_telemetria_ausente(s):
    """Las filas con latencia 0 y 0 tokens estan DECLARADAS, y se distingue perdida de rechazo.

    **Esta comprobacion nacio mal y se corrigio el mismo dia; conviene que se lea.** La primera
    version aplicaba el criterio 5 del protocolo —«latencia 0 y 0 tokens = rechazo de
    infraestructura»— y reportaba como rechazadas las siete filas de `nemotron-mini:4b_baseline`.
    Eso era **falso**: esas siete tienen `parse_method = direct_json` y **seis de las siete traen
    `recall > 0`**. Hay contenido, de modo que la ejecucion no se rechazo.

    Y el informe **ya lo declaraba**, en la salvedad de procedencia de §5.3.1: «siete filas de
    `nemotron-mini:4b` tienen latencia 0 y 0 tokens/s porque **se re-extrajeron fuera del arnes de
    lotes** tras un fallo de contexto; sus valores de precision, recall y F1 son reales, pero su
    telemetria no existe». Se aplico la regla sin comprobar su premisa, sobre un documento que
    traia la explicacion correcta.

    Lo que la comprobacion hace ahora:

    1. Cuenta, en las corridas que el consolidado usa, las filas con **latencia 0 y 0 tokens**.
    2. Las separa en **sin contenido** —recall y precision a cero, que si es rechazo o perdida
       total— y **con contenido** —telemetria ausente, que es lo que el informe declara—.
    3. Exige que el recuento de las que tienen contenido **coincida con el que el informe declara**.
       Si el numero cambia, la salvedad deja de describir los datos.
    4. Las que **no** tienen contenido si son un fallo, y se reportan.

    Comprobado el dia que se escribio: siete filas con telemetria ausente, seis con contenido y una
    sin el, y el informe declara siete. La discrepancia de esa una queda a la vista en lugar de
    diluirse.
    """
    import csv as _csv
    # Se cuenta en el CONSOLIDADO, no en las fuentes. La salvedad del informe describe las filas
    # que llegan a las cifras publicadas, y varias fuentes del manifiesto aportan grupos que
    # PIERDEN la fusion —`benchmark_n120_REMOTO` trae ocho filas de nemotron que el consolidado
    # descarta en favor de la re-corrida—. Contarlas aqui daba 15 donde el informe declara 7, y la
    # discrepancia era del contador, no del documento.
    ruta = CSV_CONSOLIDADO  # una sola fuente de verdad; ver F149/F154
    con, sin, mirados, fallos = 0, [], 0, []
    mirados += 1
    if not os.path.exists(ruta):
        check('las filas sin telemetria estan declaradas en el informe', mirados,
              ['no existe el CSV del consolidado'])
        return
    rel = os.path.relpath(CSV_CONSOLIDADO, RAIZ)
    if True:
        with open(ruta, encoding='utf-8') as fh:
            for r in _csv.DictReader(fh):
                lat, tok = r.get('latency_sec'), r.get('tokens_per_sec')
                if lat in (None, '') or tok in (None, ''):
                    continue
                if float(lat) != 0.0 or float(tok) != 0.0:
                    continue
                # `is not None` de facto: 0.0 es el valor buscado y `if x` lo descartaria
                rc = r.get('recall')
                pr = r.get('precision')
                vacio = ((rc in (None, '') or float(rc) == 0.0)
                         and (pr in (None, '') or float(pr) == 0.0))
                if vacio:
                    sin.append('%s / %s / %s'
                               % (os.path.basename(os.path.dirname(rel)),
                                  r.get('model'), r.get('record_id')))
                else:
                    con += 1
    mirados += 1
    if con + len(sin) == 0:
        # Nada que declarar: el consolidado adoptado no trae ni una fila con latencia 0 y 0
        # tokens, de modo que exigir una frase «N filas de nemotron-mini:4b tienen latencia = 0»
        # obligaria al informe a afirmar un defecto que ya no existe.
        pass
    else:
        m = re.search(r'(\w+) filas de `nemotron-mini:4b` tienen `latencia = 0`', s)
        PAL = {'Siete': 7, 'siete': 7, 'Ocho': 8, 'ocho': 8, 'Seis': 6, 'seis': 6,
               'Nueve': 9, 'nueve': 9, 'Diez': 10, 'diez': 10}
        declaradas = PAL.get(m.group(1)) if m else None
        if declaradas is None:
            fallos.append('no se encuentra en el informe la salvedad de las filas con latencia 0, '
                          'o su numeral no se puede leer. Los datos traen %d con contenido' % con)
        elif declaradas != con + len(sin):
            fallos.append('el informe declara %d filas con latencia 0 y los datos traen %d '
                          '(%d con contenido, %d sin el): la salvedad deja de describirlos'
                          % (declaradas, con + len(sin), con, len(sin)))
    mirados += 1
    if sin:
        fallos.append('%d fila(s) con latencia 0, 0 tokens y **sin contenido**, que no es '
                      'telemetria ausente sino perdida: %s' % (len(sin), ', '.join(sin[:4])))
    check('las filas sin telemetria estan declaradas en el informe', mirados, fallos,
          '%d con contenido —telemetria ausente, declarada en §5.3.1— y %d sin el. La regla del '
          'criterio 5 no se aplica cuando hay contenido: eso no es rechazo' % (con, len(sin)))


def c_corpus_idioma(s):
    """El idioma del corpus se comprueba, no se supone. Y sus localizaciones, tambien.

    `CLAUDE.md` cierra su seccion de integridad con esto: «El idioma del corpus se comprueba, no se
    supone. Los dos corpus del dominio de este trabajo resultaron estar integramente en ingles
    mientras el informe declaraba validacion en espanol (§F54)». Era la ultima regla de esa seccion
    sin mecanizar.

    El informe lo declara en cinco sitios con cuatro redacciones —«105 de los 120», «Espanol
    (105/120)», «de los que 105 estan en espanol»—, de modo que un patron unico no vale. Se anclan
    las dos del encabezado, que son las que un tribunal lee primero, y **en los dos idiomas**: el
    resumen dice «120 articulos, 105 en espanol» y el abstract «120 articles, 105 in Spanish». Como
    `CLAUDE.md` exige que digan lo mismo, comprobar los dos vigila tambien esa sincronia.

    Contado el 2026-09-09 sobre el corpus: **105 espanol, 15 ingles, 0 indeterminados**. Coincide.

    De paso se comprueba la correccion del corpus del 2026-09-08: **545 localizaciones en 119 de
    los 120 registros**, exactamente lo declarado. Es la contraparte de la segunda mitad de
    `c_firma_categorias`: el corpus **ya** las tiene y las metricas publicadas **son anteriores**,
    de modo que las dos cifras juntas dicen por que la re-corrida sigue pendiente.

    Guarda de §L66: si las listas de palabras no clasifican casi nada, la comprobacion **dice que
    su detector esta roto** en lugar de reportar ciento veinte registros indeterminados.
    """
    import json as _json
    ruta = os.path.join(BENCH_DIR, CORPUS)
    if not os.path.exists(ruta):
        check('el idioma del corpus se comprueba, no se supone', 0,
              ['no existe el corpus %s' % CORPUS])
        return
    try:
        with open(ruta, encoding='utf-8') as fh:
            datos = _json.load(fh)
    except (ValueError, OSError) as e:
        check('el idioma del corpus se comprueba, no se supone', 0,
              ['el corpus no se puede leer: %s' % e])
        return
    regs = datos.get('dataset') if isinstance(datos, dict) else datos
    if not isinstance(regs, list) or not regs:
        check('el idioma del corpus se comprueba, no se supone', 0,
              ['el corpus no trae una lista de registros'])
        return
    es = en = indet = locs = con_loc = 0
    for r in regs:
        txt = ((r.get('title') or '') + ' ' + (r.get('text') or '')).lower()
        pal = re.findall(r'[a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc]+', txt)
        n_es = sum(1 for x in pal if x in PAL_ES)
        n_en = sum(1 for x in pal if x in PAL_EN)
        if n_es == n_en == 0:
            indet += 1
        elif n_es > n_en:
            es += 1
        else:
            en += 1
        L = r.get('locations') or []
        locs += len(L)
        con_loc += 1 if L else 0
    fallos, mirados = [], 0
    # guarda del detector antes de cualquier veredicto (§L66)
    mirados += 1
    if indet > len(regs) // 10:
        fallos.append('%d de %d registros quedan sin clasificar: las listas de palabras no sirven '
                      'para este corpus y esta comprobacion daria un veredicto falso'
                      % (indet, len(regs)))
        check('el idioma del corpus se comprueba, no se supone', mirados, fallos)
        return
    for etiq, patron in (('el resumen', r'(\d+) art\u00edculos, (\d+) en espa\u00f1ol'),
                         ('el abstract', r'(\d+) articles, (\d+) in Spanish')):
        mirados += 1
        m = re.search(patron, s)
        if m is None:
            fallos.append('no se encuentra en %s la declaracion «M articulos, N en espanol»: '
                          'revisar si se reformulo. El corpus da %d en espanol de %d'
                          % (etiq, es, len(regs)))
            continue
        d_tot, d_es = int(m.group(1)), int(m.group(2))
        if d_tot != len(regs):
            fallos.append('%s habla de %d articulos y el corpus trae %d'
                          % (etiq, d_tot, len(regs)))
        if d_es != es:
            fallos.append('%s declara %d articulos en espanol y el corpus da %d '
                          '(%d en ingles, %d sin clasificar). Ver FINDINGS §F54'
                          % (etiq, d_es, es, en, indet))
    mirados += 1
    if locs == 0:
        fallos.append('el corpus no trae ninguna localizacion: la correccion del 2026-09-08, que '
                      'anadio 545 en 119 de 120 registros, no esta en este fichero')
    check('el idioma del corpus se comprueba, no se supone', mirados, fallos,
          '%d en espanol, %d en ingles, %d sin clasificar · %d localizaciones en %d registros'
          % (es, en, indet, locs, con_loc))


def c_firma_categorias(s):
    """Ninguna categoria NUEVA puede puntuar contra el vacio: `tp + fn = 0` mientras `fp` crece.

    Es la regla que `CLAUDE.md` puso el 2026-09-08 despues del defecto mas caro del proyecto: el
    65 % de los falsos positivos procedia de una categoria que ningun corpus anotaba, y sobrevivio
    dos meses porque las cifras eran internamente coherentes. La regla dice que **el indicador
    barato es `tp + fn` agregado por categoria** y que hay que comprobarlo «antes de dar por buena
    cualquier metrica nueva» — pero hasta hoy solo existia dentro de `composicion_fp.py`, que nadie
    ejecuta automaticamente. Una regla que solo vive en una herramienta que nadie invoca no protege
    de nada.

    Se calcula desde los `detailed_results.json` por corrida, porque el `merged_results.csv` del
    consolidado **no trae la columna `metrics`** — es el pedido §3.bis.16, pendiente del equipo
    remoto—. Comprobado el dia que se anadio: 17 corridas con desglose, y la firma agregada da
    `Persons` tp+fn=39 541, `Organizations` 53 621 y `Locations` **0** con fp=29 465.

    `Locations` es la sabida y esta esperada; **cualquier otra categoria en la misma situacion es
    un fallo**. Sumar los enteros con `int(v.get(k) or 0)` y no con `if v.get(k)` importa aqui mas
    que en ningun sitio: un `tp` de 0 es *falsy* y descartarlo haria invisible justo el caso que se
    busca.
    """
    import json as _json
    import glob as _glob
    from collections import Counter as _C
    res = os.path.join(BENCH_DIR, 'results')
    tot, corridas = {}, 0
    for d in sorted(_glob.glob(os.path.join(res, '*'))):
        ruta = os.path.join(d, 'detailed_results.json')
        if not os.path.exists(ruta):
            continue
        try:
            with open(ruta, encoding='utf-8') as fh:
                recs = _json.load(fh)
        except (ValueError, OSError):
            continue
        if not isinstance(recs, list):
            continue
        visto = False
        for r in recs:
            pt = ((r.get('metrics') or {}).get('per_type')) or {}
            if pt:
                visto = True
            for cat, v in pt.items():
                c = tot.setdefault(cat, _C())
                for k in ('tp', 'fp', 'fn'):
                    c[k] += int(v.get(k) or 0)
        if visto:
            corridas += 1
    fallos, mirados = [], 0
    if not tot:
        check('ninguna categoria nueva puntua contra el vacio', 0,
              ['no se encuentra ningun detailed_results.json con desglose por tipo: la '
               'comprobacion no puede correr'])
        return
    for cat in sorted(tot):
        mirados += 1
        c = tot[cat]
        if c['tp'] + c['fn'] == 0 and c['fp'] > 0:
            if cat == CATEGORIA_SIN_REFERENCIA_SABIDA:
                continue                      # sabido, declarado en §3.3 y compensado
            fallos.append('«%s» puntua contra el vacio: tp+fn=0 con fp=%d. Ninguna entidad de '
                          'referencia en todo el corpus, de modo que cada acierto del modelo se '
                          'contabiliza como error. Ver FINDINGS §F53 y CLAUDE.md'
                          % (cat, c['fp']))
    # y que la sabida siga siendo la sabida: si de pronto tuviera referencias, el informe cambia
    mirados += 1
    sab = tot.get(CATEGORIA_SIN_REFERENCIA_SABIDA)
    if sab is not None and sab['tp'] + sab['fn'] > 0:
        fallos.append('«%s» ya tiene %d entidades de referencia: el corpus se corrigio y §3.3, la '
                      'metrica restringida y el Anexo I dejan de describir la medicion. Revisar '
                      'antes de dar por buena ninguna cifra'
                      % (CATEGORIA_SIN_REFERENCIA_SABIDA, sab['tp'] + sab['fn']))
    check('ninguna categoria nueva puntua contra el vacio', mirados, fallos,
          '%d corridas con desglose; «%s» esta esperada y documentada en §3.3'
          % (corridas, CATEGORIA_SIN_REFERENCIA_SABIDA))


def c_referencias_findings(s):
    """Todo `§F<n>` y `§L<n>` citado en el proyecto tiene su seccion.

    La comprobacion hermana vigila que ningun identificador se defina **dos veces**; esta vigila lo
    contrario: que ninguno se **cite sin existir**. Son defectos distintos y ninguno implica al
    otro. Un puntero colgando pierde exactamente la informacion que pretendia conservar, y como los
    hallazgos se citan desde `CLAUDE.md`, desde los encargos al equipo remoto y desde el codigo de
    las propias herramientas, el rastro se rompe sin que nada lo diga.

    **La trampa: hay dos convenciones de encabezado.** Las secciones antiguas son `### L47. ...`,
    sin `§`, y las nuevas `## §L61 — ...`. Un patron que solo acepte la nueva encuentra **9**
    secciones §L donde hay **65**, y entonces reporta **40 referencias colgando** que estan
    perfectamente bien. Ocurrio el 2026-09-09 al escribir esta comprobacion, y lo delato mirar la
    lista: entre las supuestas colgantes estaban §L43, §L44 y §L47, que cita `CLAUDE.md` y que
    obviamente existen. Se aceptan **las dos** convenciones.

    Comprobado el dia que se anadio: **185** secciones definidas —120 §F y 65 §L—, **118**
    identificadores citados en 290 ficheros y **cero** sin destino.
    """
    import glob as _glob
    def _definidas(fich, pref):
        ruta = os.path.join(RAIZ, fich)
        if not os.path.exists(ruta):
            return None
        with open(ruta, encoding='utf-8') as fh:
            txt = fh.read()
        out = set()
        for m in re.finditer(r'^#{1,4}\s+\u00a7?%s(\d+)((?:\.[a-z]+)*)\s*[\u2014.\-]' % pref,
                             txt, re.M):
            out.add('\u00a7%s%s%s' % (pref, m.group(1), m.group(2)))
        return out

    dF, dL = _definidas('FINDINGS.md', 'F'), _definidas('LEARNING.md', 'L')
    if dF is None or dL is None:
        check('toda referencia §F y §L tiene su seccion', 0,
              ['falta FINDINGS.md o LEARNING.md'])
        return
    existe = dF | dL
    fallos, mirados = [], 0
    # una definicion vacia no es un fallo de referencias, pero sí una senal de deteccion rota
    if len(dL) < 20 or len(dF) < 20:
        fallos.append('solo se detectan %d secciones §F y %d §L: el patron de encabezados esta '
                      'roto y esta comprobacion daria falsos positivos en masa' % (len(dF), len(dL)))
        check('toda referencia §F y §L tiene su seccion', len(existe), fallos)
        return
    citados = {}
    ficheros = [f for f in (_glob.glob(os.path.join(RAIZ, '*.md'))
                            + _glob.glob(os.path.join(RAIZ, 'tools/*.py'))
                            + _glob.glob(os.path.join(RAIZ, 'doc/**/*.md'), recursive=True))
                if os.path.isfile(f)]
    for f in ficheros:
        try:
            with open(f, encoding='utf-8') as fh:
                txt = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for m in re.finditer(r'\u00a7([FL])(\d+)((?:\.[a-z]+)*)', txt):
            k = '\u00a7%s%s%s' % (m.group(1), m.group(2), m.group(3))
            citados.setdefault(k, set()).add(os.path.relpath(f, RAIZ))
    for k in sorted(citados):
        mirados += 1
        if k not in existe:
            fallos.append('%s se cita en %s y no tiene seccion'
                          % (k, ', '.join(sorted(citados[k]))[:80]))
    check('toda referencia §F y §L tiene su seccion', mirados, fallos,
          'hay dos convenciones de encabezado, «### L47.» y «## §L61 —»: se aceptan las dos')


def c_docx_sano(s):
    """Los tres `.docx` siguen siendo OOXML estructuralmente sano tras la cirugia sobre su XML.

    El proyecto tiene **cinco** herramientas que editan `word/document.xml` —reemplazo de texto,
    borrado de filas, reescritura de celdas, reconstruccion de cuerpo y particion de runs— y el
    2026-09-09 se usaron todas sobre los entregables. Un zip valido no acredita nada: `testzip()`
    solo comprueba los CRC, y un `document.xml` malformado o con una tabla descuadrada abre un
    dialogo de error en Word en lugar del documento.

    Cuatro comprobaciones, en orden de gravedad:

    1. **Toda parte XML del paquete parsea.** No solo `document.xml`: tambien los `.rels`, los
       estilos y la numeracion, que una reescritura del ZIP podria truncar.
    2. **Cada fila de cada tabla tiene tantas celdas como columnas declara la rejilla**, contando
       los `gridSpan`. Es el descuadre tipico de borrar o clonar filas, y Word lo dibuja torcido
       sin quejarse.
    3. **Ningun identificador duplicado** de marcador o de propiedad de dibujo. Clonar una fila
       como plantilla es la forma facil de duplicar uno, y Word rechaza el fichero.
    4. **Ninguna referencia `r:id` sin su relacion**, que dejaria una imagen o un hiperenlace roto.

    Comprobado el dia que se anadio: 26, 15 y 15 partes XML bien formadas, 19 tablas por documento
    sin un solo descuadre, cero identificadores duplicados y cero referencias colgando.
    """
    import zipfile as _zip
    import collections as _col
    from xml.etree import ElementTree as _ET
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        ruta = os.path.join(RAIZ, rel)
        base = os.path.basename(rel)
        if not os.path.exists(ruta):
            mirados += 1
            fallos.append('no existe el entregable %s' % rel)
            continue
        try:
            z = _zip.ZipFile(ruta)
        except _zip.BadZipFile as e:
            mirados += 1
            fallos.append('%s no es un zip valido: %s' % (base, e))
            continue
        # 1) toda parte XML parsea
        for n in z.namelist():
            if not n.endswith(('.xml', '.rels')):
                continue
            mirados += 1
            try:
                _ET.fromstring(z.read(n))
            except _ET.ParseError as e:
                fallos.append('%s: la parte %s no parsea: %s' % (base, n, e))
        try:
            x = z.read('word/document.xml').decode('utf-8')
        except KeyError:
            fallos.append('%s no trae word/document.xml' % base)
            continue
        # 2) rejilla contra celdas
        for i, tb in enumerate(re.findall(r'<w:tbl>.*?</w:tbl>', x, re.S)):
            cols = len(re.findall(r'<w:gridCol\b', tb))
            if not cols:
                continue
            for k, f in enumerate(re.findall(r'<w:tr[ >].*?</w:tr>', tb, re.S)):
                mirados += 1
                nc = len(re.findall(r'<w:tc>', f))
                extra = sum(int(v) - 1 for v in re.findall(r'<w:gridSpan w:val="(\d+)"', f))
                if nc + extra != cols:
                    fallos.append('%s: tabla %d fila %d tiene %d celdas (+%d de gridSpan) y la '
                                  'rejilla declara %d columnas'
                                  % (base, i, k, nc, extra, cols))
        # 3) identificadores duplicados
        for nom, pat in (('marcador', r'<w:bookmarkStart[^>]*\bw:id="([^"]+)"'),
                         ('nombre de marcador', r'<w:bookmarkStart[^>]*\bw:name="([^"]+)"'),
                         ('propiedad de dibujo', r'<wp:docPr[^>]*\bid="([^"]+)"')):
            mirados += 1
            c = _col.Counter(re.findall(pat, x))
            dup = sorted(k for k, v in c.items() if v > 1)
            if dup:
                fallos.append('%s: %d identificador(es) de %s duplicado(s): %s'
                              % (base, len(dup), nom, dup[:4]))
        # 4) relaciones colgando
        mirados += 1
        try:
            rels = z.read('word/_rels/document.xml.rels').decode('utf-8')
        except KeyError:
            rels = ''
        ids = set(re.findall(r'Id="([^"]+)"', rels))
        usados = set(re.findall(r'r:(?:id|embed|link)="([^"]+)"', x))
        colgando = sorted(usados - ids)
        if colgando:
            fallos.append('%s: %d referencia(s) sin su relacion: %s'
                          % (base, len(colgando), colgando[:4]))
    check('los tres .docx siguen siendo OOXML estructuralmente sano', mirados, fallos,
          'un zip valido no acredita nada: testzip() solo comprueba los CRC')


def c_pdf_al_dia(s):
    """El PDF de la raiz no puede ser mas viejo que el `.docx` del que sale.

    El 2026-09-09 se encontro que el PDF arrastraba **todos** los defectos corregidos ese dia en
    los `.docx`: once menciones de modelos excluidos, `76,85` seis veces, `90,91` dos, `81,45` dos
    y `65 %` dos, con cero de las cifras correctas. Ver `FINDINGS §F98`.

    **Una distincion que hay que respetar.** El PDF de la raiz y el de `doc/versions/enviados/` son
    **byte a byte el mismo fichero**, y ese segundo es el **entregado al profesor guia**, que
    `CLAUDE.md` declara verdad de referencia sobre que modelos forman el estudio. Ese **atestigua**
    y no se toca: reescribir un documento que ya se entrego no es limpiar, es falsificar el
    registro de lo que se entrego. Lo que hay que regenerar es la **copia de la raiz**, y desde el
    `.docx` corregido, con Word — no hay conversor en este entorno y regenerarlo con otro motor
    perderia la maquetacion, que es lo que `CLAUDE.md` advierte para pandoc.

    La comprobacion **no lee el PDF**: pypdf solo esta en el venv del proyecto y una comprobacion
    que solo corre dentro de un entorno concreto no corre (§L62). Compara **procedencias**: si el
    `.docx` tiene commits posteriores al del PDF, el PDF esta obsoleto, y eso se sabe sin abrirlo.

    Va **aparte** de la comprobacion de modelos excluidos a proposito. Si el PDF entrara en
    aquella, su fallo la pondria en rojo y **cegaria como centinela** a los tres `.docx`, que es
    §L64. Cada defecto abierto en su propia comprobacion.
    """
    import subprocess as _sp

    def _fecha_commit(rel):
        try:
            r = _sp.run(['git', 'log', '-1', '--format=%ct', '--', rel],
                        cwd=RAIZ, capture_output=True, text=True, timeout=20)
            return int(r.stdout.strip()) if r.stdout.strip() else None
        except (OSError, ValueError):
            return None

    fallos, mirados = [], 0
    mirados += 1
    if not os.path.exists(os.path.join(RAIZ, PDF_RAIZ)):
        fallos.append('no existe el PDF de la raiz: %s' % PDF_RAIZ)
        check('el PDF de la raiz no es mas viejo que el .docx', mirados, fallos)
        return
    t_pdf = _fecha_commit(PDF_RAIZ)
    mirados += 1
    if t_pdf is None:
        fallos.append('el PDF de la raiz no esta rastreado o no se puede fechar')
    for rel in DOCX_ENTREGABLES:
        mirados += 1
        t_doc = _fecha_commit(rel)
        if t_doc is None:
            fallos.append('%s no se puede fechar' % os.path.basename(rel))
        elif t_pdf is not None and t_doc > t_pdf:
            import datetime as _dt
            f = lambda x: _dt.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M')
            fallos.append('%s cambio el %s y el PDF es del %s: hay que regenerarlo desde el .docx '
                          'con Word. NO tocar el PDF de doc/versions/enviados/, que atestigua'
                          % (os.path.basename(rel), f(t_doc), f(t_pdf)))
    # y que el enviado siga intacto: es la verdad de referencia
    mirados += 1
    if not os.path.exists(os.path.join(RAIZ, PDF_ENVIADO)):
        fallos.append('falta el PDF entregado al profesor guia, que es la verdad de referencia: %s'
                      % PDF_ENVIADO)
    check('el PDF de la raiz no es mas viejo que el .docx', mirados, fallos,
          'el PDF de doc/versions/enviados/ se conserva; el de la raiz se regenera con Word')


def c_sobriedad_docx(s):
    """El `.docx` no puede AÑADIR resaltes respecto del Markdown, y hoy añade 17 en el cuerpo.

    `CLAUDE.md` obliga a que «quien los produce cuente guiones y resaltes del cuerpo del documento
    generado y los compare con los de la fuente, porque el renderizador no debe añadir énfasis».
    Comprobado el 2026-09-09 y nunca antes: el `.docx` canonico tenia **17 tramos en negrita en el
    cuerpo** que el Markdown no marca, hoy **16**. Los guiones largos, en cambio, bajan de 81 a 67, sin
    añadidos.

    Clasificados, para no contar de mas: **76** de los resaltes que el Markdown no marca estan
    **dentro de tablas** —cabeceras y celdas, que Word pone en negrita por estilo mientras el
    Markdown no las marca— y **0** en encabezados. Esos son legitimos. Los 17 del cuerpo son la
    limpieza de sobriedad que el `.md` hizo (de 164 negritas a 108) y el `.docx`, congelado antes,
    no recibio.

    **Esta comprobacion no exige que sean cero**, porque varios de los 17 parecen encabezados de
    parrafo del anexo —«Ejemplo few-shot 1 (caso persona sancionada):»— y quitarles la negrita
    destruiria estructura: son decisiones de una por una, de la pasada de maquetacion. Lo que
    exige es que **no crezcan**. Un umbral fijo con el estado actual convierte el pendiente en una
    linea de defensa: si alguien anade un resalte al entregable, se ve.

    Uno de los 17 es consecuencia de una edicion propia: en §3.3 el Markdown resalta solo el
    porcentaje y el `.docx` tiene la frase entera en negrita, porque el reemplazo de texto escribio
    la cifra nueva dentro del run que ya estaba resaltado. Arreglarlo exige partir el run.
    """
    import zipfile as _zip
    norm = lambda z: re.sub(r'\s+', ' ', z.strip().strip('`'))
    marcados = set(norm(m.group(1)) for m in re.finditer(r'\*\*([^*]+)\*\*', s))
    fallos, mirados = [], 0
    for rel in DOCX_ENTREGABLES:
        ruta = os.path.join(RAIZ, rel)
        mirados += 1
        if not os.path.exists(ruta):
            fallos.append('no existe el entregable %s' % rel)
            continue
        with _zip.ZipFile(ruta) as z:
            x = z.read('word/document.xml').decode('utf-8')
        tablas = [(m.start(), m.end()) for m in re.finditer(r'<w:tbl>.*?</w:tbl>', x, re.S)]
        en_tabla = lambda i: any(a <= i < b for a, b in tablas)
        cuerpo = 0
        for pm in re.finditer(r'<w:p[ >].*?</w:p>', x, re.S):
            par = pm.group(0)
            est = re.search(r'<w:pStyle w:val="([^"]+)"', par)
            est = est.group(1) if est else ''
            if en_tabla(pm.start()) or est.startswith('Heading'):
                continue
            actual = []
            tramos = []
            for r in re.findall(r'<w:r[ >].*?</w:r>', par, re.S):
                txt = ''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', r, re.S))
                if re.search(r'<w:b\s*/>', r) and txt:
                    actual.append(txt)
                else:
                    if actual:
                        tramos.append(''.join(actual))
                        actual = []
            if actual:
                tramos.append(''.join(actual))
            cuerpo += sum(1 for x_ in tramos if norm(x_) not in marcados)
        mirados += 1
        if cuerpo > BOLD_CUERPO_BASE:
            fallos.append('%s: %d resaltes en el cuerpo que el Markdown no marca, y el estado '
                          'declarado son %d. No se ha propagado la limpieza de sobriedad y ademas '
                          'ha crecido: revisar que se ha resaltado'
                          % (os.path.basename(rel), cuerpo, BOLD_CUERPO_BASE))
        # que baje es una buena noticia y hay que actualizar la base para que siga vigilando
        elif cuerpo < BOLD_CUERPO_BASE:
            fallos.append('%s: %d resaltes en el cuerpo, menos que los %d declarados. Es una '
                          'mejora: bajar BOLD_CUERPO_BASE a %d para que la comprobacion siga '
                          'vigilando desde el nuevo estado'
                          % (os.path.basename(rel), cuerpo, BOLD_CUERPO_BASE, cuerpo))
        # guiones largos: el .docx no puede tener MAS que la fuente
        mirados += 1
        td = ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))
        if td.count('\u2014') > s.count('\u2014'):
            fallos.append('%s: %d guiones largos frente a %d del Markdown: el renderizador no '
                          'puede anadir'
                          % (os.path.basename(rel), td.count('\u2014'), s.count('\u2014')))
    check('el .docx no anade resaltes ni guiones respecto del Markdown', mirados, fallos,
          'los 17 del cuerpo son la limpieza de sobriedad sin propagar; lo que se vigila es que '
          'no crezcan')


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
        check('Figura 1 coherente con la Tabla 7', 0, ['no se encuentra la Tabla 7'])
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
    # Hasta el 2026-09-09 el script tenia la Tabla 7 copiada a mano y aqui se comparaba ese
    # literal contra la tabla. Desde que la LEE (§F97) no hay literal que comparar, y borrar la
    # comprobacion habria dejado sin vigilar la coherencia entre figura y tabla. Se sustituye por
    # algo mas fuerte: se **ejecuta el lector del propio script** y se contrasta con la lectura
    # independiente de arriba. Son dos implementaciones distintas del mismo parseo, y que
    # coincidan dice mas que comparar una constante.
    #
    # No se importa el modulo, porque importa matplotlib y eso solo esta en el venv del proyecto:
    # se extrae el codigo de `leer_tabla7` y su constante MD y se ejecuta aislado.
    sc = ''
    try:
        with open(SCRIPT_FIGURAS, encoding='utf-8') as fh:
            sc = fh.read()
    except OSError as e:
        fallos.append('no se puede abrir el script de figuras: %s' % e)
    if sc:
        if re.search(r'^TABLA7 = \[', sc, re.M):
            fallos.append('el script vuelve a tener la Tabla 7 escrita a mano: debe leerla del '
                          'Markdown (§F97, §L63)')
        arb = ast.parse(sc)
        pedazos = [n for n in arb.body
                   if (isinstance(n, ast.FunctionDef) and n.name == 'leer_tabla7')
                   or (isinstance(n, ast.Assign)
                       and any(getattr(x, 'id', '') == 'MD' for x in n.targets))]
        if len(pedazos) != 2:
            fallos.append('no se encuentran en el script la constante MD y la funcion '
                          'leer_tabla7: son %d de 2' % len(pedazos))
        else:
            ns = {'os': os, 're': re, '__file__': SCRIPT_FIGURAS}
            try:
                exec(compile(ast.Module(body=pedazos, type_ignores=[]), SCRIPT_FIGURAS, 'exec'), ns)
                script = ns['leer_tabla7']()
            except Exception as e:                                   # noqa: BLE001
                fallos.append('el lector del script falla: %s: %s' % (type(e).__name__, e))
                script = []
            if script:
                if len(script) != len(filas):
                    fallos.append('el lector del script da %d filas y esta comprobacion %d'
                                  % (len(script), len(filas)))
                for a, b in zip(filas, script):
                    if a[0] != b[0] or abs(a[1] - b[1]) > 1e-9 or abs(a[2] - b[2]) > 1e-9 \
                            or a[4] != b[3]:
                        fallos.append('fila distinta: esta comprobacion %s vs el lector del '
                                      'script %s' % (a[:3], b[:3]))
    check('Figura 1 coherente con la Tabla 7 y Δ aritméticamente correcto', len(filas), fallos)


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
                                'ANALISIS_CONJUNTO_20260909_FIX/merge_manifest.json')
# Adoptado el 2026-09-09 (decision 1, autorizada por el autor). El consolidado publicado
# queda en results/ANALISIS_CONJUNTO_20260907/ y NO se borra: es el que sostenia el informe
# hasta hoy y el que un tribunal puede pedir ver. Ver FINDINGS §F154.
MANIFIESTO_PUBLICADO = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                          'ANALISIS_CONJUNTO_20260907/merge_manifest.json')
# Fijo al publicado A PROPOSITO, y nunca sigue a la decision 1. El Anexo I describe un
# defecto del corpus PUBLICADO (Locations sin anotar) y su estimacion restringida; ese
# parrafo no se actualiza con la adopcion, es historico por diseno. Si `c_agregacion`
# resolviera su comparacion contra `MANIFIESTO` (el adoptado), compararia el numero
# historico del Anexo I contra el macro del consolidado NUEVO, que no es lo que describe.
BENCH = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark')


def _reancla_manifiesto(ruta_o_dir):
    """Una ruta declarada por un `csv_path` del manifiesto, reanclada a este repositorio.

    Con el consolidado publicado, `csv_path` es relativo (`results/gptoss_rerun_REMOTO/...`) y basta
    unirlo a `BENCH`. Con el consolidado nuevo son rutas ABSOLUTAS de otra maquina
    (`/Users/eahumada1/Projects/.../repos/ner-llm-entity-benchmark/results/...`), y unir con `BENCH`
    las descarta silenciosamente porque `os.path.join` con un segundo argumento absoluto ignora el
    primero: el resultado es la ruta literal de la otra maquina, que no existe aqui. Es el mismo
    defecto que `tools/manifiesto_local.py` corrigio para el ensayo de adopcion (`FINDINGS §F148`),
    aplicado aqui a los tres sitios que leen `csv_path` como ruta de fichero.
    """
    COLA = 'repos/ner-llm-entity-benchmark/'
    if os.path.isabs(ruta_o_dir):
        i = ruta_o_dir.find(COLA)
        if i < 0:
            return ruta_o_dir
        return os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark', ruta_o_dir[i + len(COLA):])
    return os.path.join(BENCH, ruta_o_dir)
# Parámetros que afectan a la medición y deben ser idénticos en todas las fuentes de un consolidado.
PARAMS = ('rag_mode', 'data_file', 'max_tokens', 'temperature', 'batch_size', 'fuzzy_threshold')

# Divergencias que el informe YA declara como reserva de comparabilidad. Se listan aquí para que la
# comprobación no falle indefinidamente: una comprobación que siempre falla se acaba desactivando
# (LEARNING §L48). Añadir una entrada exige haberla declarado antes en el informe, y retirarla cuando
# la corrida que la resuelve esté hecha.
# Retirada 2026-09-09: la entrada 'max_tokens' (4096 en gptoss_rerun frente a 2048 en las demás,
# FINDINGS §F61.bis) se declaró mientras esta comprobación leía MANIFIESTO_PUBLICADO. Desde que
# MANIFIESTO apunta a ANALISIS_CONJUNTO_20260909_FIX (decisión 1), las 13 fuentes vienen de
# recorrida_20260908/ con max_tokens=4096 sin excepción: la condición de retiro que la propia
# entrada fijaba ("en cuanto se rehaga el consolidado desde la re-corrida") ya se cumplió, y
# `c_protocolo` no vuelve a detectar la divergencia (comprobado antes de retirarla). Ver §F160.
DIVERGENCIAS_DECLARADAS = {}


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
        cfg = os.path.join(_reancla_manifiesto(os.path.dirname(f['csv_path'])), 'run_config.json')
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


# --- 15. [RETIRADA 2026-09-17] El Anexo I cuadra con la Tabla 7 ------------------------------------
# La Tabla 19 (el detalle historico de 42 configuraciones que esta comprobacion contrastaba contra
# el consolidado PUBLICADO) se retiro del Anexo I por instruccion del autor: el cuerpo del informe
# deja de narrar resultados historicos ya superados, y esa tabla era exactamente eso — un registro
# forense de una corrida sustituida, no un dato que sostenga la hipotesis vigente. Con la tabla fuera,
# esta comprobacion no tiene nada que contrastar. Ver FINDINGS §F191.
def _c_anexo_vs_tabla7_RETIRADA(s):
    j = s.find('_Tabla 19.')
    if j < 0:
        check('el Anexo I cuadra con la Tabla 7', 0, ['no se encuentra la Tabla 19'])
        return
    cons_pub = os.path.dirname(MANIFIESTO_PUBLICADO)
    csv_pub = os.path.join(cons_pub, 'merged_results.csv')
    if not os.path.exists(csv_pub):
        check('el Anexo I cuadra con la Tabla 7', 0, ['no existe %s' % csv_pub])
        return
    g_pub = _grupos_f1(csv_pub)
    t7 = {}
    for grupo, vals in g_pub.items():
        if not grupo.endswith('_baseline') or not vals:
            continue
        mod = grupo[:-len('_baseline')]
        kb = g_pub.get(mod + '_kb_rag')
        if not kb:
            continue
        t7[mod] = (100 * sum(vals) / len(vals), 100 * sum(kb) / len(kb))
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
          'contra el consolidado publicado, no contra la Tabla 7 actual: el Anexo I es historico '
          'por diseno desde la decision 1 (§F154)')


# --- 16. La Tabla 7 reproduce desde los datos ----------------------------------------------------
CSV_CONSOLIDADO = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                     'ANALISIS_CONJUNTO_20260909_FIX/merged_results.csv')


def c_tabla7_vs_datos(s):
    """La tabla central del informe, contrastada contra el CSV del que sale.

    Hasta el 2026-09-08 la Tabla 7 solo se comprobaba contra la Figura 1 y contra el Anexo I, es
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
    # [ACTUALIZADA 2026-09-17] Una sola corrida (ablacion_n15_REMOTO) sustituida por la media de
    # 5 semillas (FINDINGS §F176); el glob se resuelve en med() agregando las 5 seed_*.
    'gemma4:latest (ZS-ES)': ('results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv',
                              'zs-es'),
    'gemma4:latest (FS-ES)': ('results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv',
                              'fs-es'),
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
    import glob as _glob
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
            rutas = sorted(_glob.glob(os.path.join(BENCH_DIR, p))) if '*' in p \
                else [os.path.join(BENCH_DIR, p)]
            for ruta in rutas:
                with open(ruta, encoding='utf-8') as fh:
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
        d = os.path.dirname(path)
        # un path con seed_* nombra la corrida un nivel mas arriba (el directorio padre)
        run = os.path.basename(os.path.dirname(d)) if os.path.basename(d).startswith('seed_') \
            else os.path.basename(d)
        if t15 and run not in t15:
            fallos.append('la Tabla 15 ya no cita «%s»: revisar FUENTES_T4' % run)
    for fila in filas:
        nom, f1, p, rc, h = fila
        path, grupo = FUENTES_T4.get(nom, (CSV_T4_DEFECTO, nom + '_baseline'))
        existe = bool(_glob.glob(os.path.join(BENCH_DIR, path))) if '*' in path \
            else os.path.exists(os.path.join(BENCH_DIR, path))
        if not existe:
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


# --- 18. §3.3/§7.2 y el script de figuras reproducen desde el artefacto de composicion -----------
# Hasta el 2026-09-12 esta cifra tambien ilustraba una Figura 1 en el cuerpo, retirada por decision
# del autor (FINDINGS §F170): el grafico y su leyenda mostraban un defecto de medicion ya corregido,
# y el autor considero que una figura dedicada a un estado historico ya resuelto no aportaba al
# cuerpo. El script que la genera y el artefacto que la alimenta NO se tocan (son lo que atestigua),
# asi que esta comprobacion sigue vigilando que el script siga correcto aunque ya no se incruste.
ARTEFACTO_FP = os.path.join(RAIZ, 'repos/ner-llm-entity-benchmark/results/'
                                  'COMPOSICION_FP_20260908/composicion_fp_26_grupos.json')


# [RETIRADA 2026-09-17, segunda vuelta] La cita en prosa de esta magnitud (66,0 %, 12 852 de
# 19 464) ya no aparece en ningun sitio del cuerpo: se retiro de §3.3 en la primera vuelta del
# 2026-09-17 y de §7.2 (antes item 7 de la lista de hallazgos, y el item 8 de trabajo futuro) en
# la segunda, a instruccion directa del autor de purgar del Markdown canonico toda referencia a
# defectos historicos ya corregidos que no tenga asidero en la corrida vigente. La cifra sigue
# intacta en `FINDINGS.md §F53` y en `CAMBIOS-DESDE-ENVIO-PROFESOR-20260908.md`, fuera del
# producto final. Se conserva solo la vigilancia del artefacto y del script de figuras, que
# siguen existiendo y deben seguir siendo correctos aunque nada los cite ya en prosa.
def c_figura1_vs_artefacto(s):
    """El artefacto y el script de figuras de la composicion de FP, sin cita en prosa que atar.

    Historial: el informe llego a dar dos cifras distintas para esta magnitud, una de ellas sin
    respaldo en ningun dato (FINDINGS §F69). Esta comprobacion ataba las apariciones en prosa
    —§3.3 y §7.2— y el script de figuras (que ya no se incrusta en el cuerpo, §F170) al artefacto
    que las computa; ya no hay cita en prosa que atar (ver el comentario previo a esta funcion).
    """
    import json as _json
    if not os.path.exists(ARTEFACTO_FP):
        check('la composicion de FP reproduce desde el artefacto (sin cita en prosa)', 0,
              ['no existe %s' % os.path.relpath(ARTEFACTO_FP, RAIZ)])
        return
    with open(ARTEFACTO_FP, encoding='utf-8') as fh:
        a = _json.load(fh)
    loc, tot, pct = a['fp_locations'], a['fp_total'], a['pct_fp_locations']
    # el complemento tambien se dibujaba en la figura retirada y debe cuadrar con el artefacto
    comp = a.get('fp_no_locations')
    fallos, mirados = [], 0
    # el artefacto debe declarar su propia cobertura y haberla completado
    mirados += 1
    if a.get('grupos') != a.get('grupos_cubiertos'):
        fallos.append('el artefacto cubre %s de %s grupos' % (a.get('grupos_cubiertos'), a.get('grupos')))
    # el script de figuras
    esp = '%.1f' % pct
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
    check('la composicion de FP reproduce desde el artefacto (sin cita en prosa)', mirados, fallos,
          'ya no hay cita en prosa que atar (§F170, purga del 2026-09-17); solo se vigila que el '
          'artefacto y el script sigan siendo correctos')


# --- 19. Las tablas 5, 6 y 8 reproducen desde sus corridas ---------------------------------------
def _medias(rel, campos, escala=100.0):
    import csv as _csv
    import collections as _c
    import glob as _glob
    g = _c.defaultdict(lambda: _c.defaultdict(list))
    rutas = sorted(_glob.glob(os.path.join(BENCH_DIR, rel))) if '*' in rel \
        else [os.path.join(BENCH_DIR, rel)]
    for ruta in rutas:
        with open(ruta, encoding='utf-8') as fh:
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
    import glob as _glob
    fallos, mirados = [], 0

    # --- Tabla 5 [ACTUALIZADA 2026-09-17: media de 5 semillas, FINDINGS §F176]
    abl = 'results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv'
    if _glob.glob(os.path.join(BENCH_DIR, abl)):
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


# [RETIRADA 2026-09-17] La Tabla 18 (efecto diferencial del mojibake, 26 filas) se retiro del
# Anexo H por instruccion del autor: registro forense de un defecto ya corregido, no un dato que
# sostenga la hipotesis vigente. El numero «18» ya no lo ocupa ninguna tabla nueva (el cuerpo
# termina en la Tabla 17 tras el recorte), asi que esta comprobacion simplemente no tiene nada que
# contrastar. Ver FINDINGS §F191.
def _c_tabla18_vs_artefacto_RETIRADA(s):
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
                                    'CORRELACION_CAPACIDAD_20260909_FIX/correlacion.json')
# Adoptado con la decision 1. El del publicado se conserva en
# results/CORRELACION_CAPACIDAD_20260908/ y no se borra.


def c_correlacion(s):
    """La rho que dibuja la Figura 1 y que cita §5.3.1, contra el fichero que la calcula.

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
    # SIEMPRE el publicado, nunca MANIFIESTO (que sigue la decision 1): el Anexo I, unico
    # consumidor real de este calculo desde que la decision 1 volvio moot la comparacion de
    # conclusion 1, describe el defecto del corpus PUBLICADO. Ver MANIFIESTO_PUBLICADO arriba.
    if not os.path.exists(MANIFIESTO_PUBLICADO):
        check('la conclusion 1 usa la agregacion declarada en §3.3', 0,
              ['no existe el manifiesto publicado, del que sale la corrida de referencia'])
        return
    with open(MANIFIESTO_PUBLICADO, encoding='utf-8') as fh:
        srcs = _json.load(fh)['sources']
    d120 = next((_reancla_manifiesto(os.path.dirname(x['csv_path'])) for x in srcs
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
        # Esta funcion esta fijada a MANIFIESTO_PUBLICADO (nunca sigue la decision 1), y el
        # consolidado publicado NO excluye articulos contaminados: ese filtro es propio de la
        # re-corrida, por un defecto de codificacion distinto (mojibake), y aplicarlo aqui quitaria
        # 7 de los 120 registros que el propio CSV publicado SI cuenta. Se calcula sobre los 120.
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
        # la conclusion 1 debe citar la macro; si cita la micro, esta mezclando agregaciones.
        # Y si la conclusion 1 YA NO comenta un equivalente "bajo la convencion original" —lo hizo
        # hasta que la decision 1 volvio moot esa comparacion para N=120 y de paso se quito tambien
        # la de dominio, que iba en la misma frase—, no hay nada que verificar aqui: no es un
        # fallo que la frase no exista, solo lo seria que existiera con el numero equivocado.
        i7 = s.find('1. **Viabilidad demostrada')
        concl = s[i7:i7 + 1200] if i7 >= 0 else ''
        if re.search(r'convenci[oó]n original', concl) is None:
            continue
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
    #
    # [2026-09-17] La Tabla 19 y el emparejamiento «pasa de X % a Y %» se retiraron del Anexo I por
    # instruccion del autor (registro forense de un defecto ya corregido, no un dato que sostenga
    # la hipotesis vigente): si la frase no esta, no es un fallo, es que ya no hay nada que
    # emparejar. Mismo criterio que el «convencion original» de arriba.
    if 'N=120' in agreg and re.search(r'pasa de\s+\d+[.,]\d+\s*%\s*a', s):
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
    cons = os.path.dirname(CSV_CONSOLIDADO)  # una sola fuente de verdad; ver F149
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
    m1 = re.search(r'ANOVA de una v\u00eda sobre los \w+ grupos arroja \*\*F = (\d+),(\d+)\*\*', s)
    if m1 is None:
        fallos.append('no se encuentra en el informe la frase del ANOVA con su F: '
                      'revisar si se reformulo')
    else:
        pub = float('%s.%s' % (m1.group(1), m1.group(2)))
        if abs(pub - F) >= 5e-5:
            fallos.append('el informe publica F = %s y el CSV da %.4f' % (pub, F))

    # 2) la p, con el exponente en superindices. Se busca en una VENTANA corta despues de la F, no
    # en todo el documento: buscar en `s` entero hace que esta comprobacion case con la PRIMERA
    # «p = mantisa x 10^exp» del informe, que puede ser la de Levene o la de otra prueba, no la del
    # ANOVA. Paso con el consolidado nuevo: la p del ANOVA subdesborda y se escribe «p < 10^-300»,
    # sin mantisa, y el regex encontro en su lugar la frase de Levene, cien caracteres mas adelante.
    ventana = s[m1.end():m1.end() + 200] if m1 else s
    m = re.search(r'p = (\d+),(\d+) \u00d7 10([\u2070-\u2079\u00b9\u00b2\u00b3\u207b]+)', ventana)
    # Si la p subdesborda, lo correcto es que el informe escriba una COTA («p < 10^-300») y no una
    # mantisa: eso es una ausencia legitima de `m`, no un fallo. Solo hace falta comprobar que la
    # cota este ahi.
    if pv <= 0.0:
        mirados += 1
        if not re.search(r'p\s*<\s*10', ventana):
            fallos.append('la p del ANOVA subdesborda a 0,0 en doble precision y el informe no '
                          'escribe una cota del tipo «p < 10^-300» junto a la F')
        m = None  # nada mas que comprobar: no hay mantisa que contrastar
    elif m is None:
        fallos.append('no se encuentra en el informe la p del ANOVA en notacion cientifica')
    else:
        mant = float('%s.%s' % (m.group(1), m.group(2)))
        ex = _exp_super(m.group(3))
        if ex is None:
            fallos.append('no se puede leer el exponente de la p del ANOVA: %r' % m.group(3))
        else:
            pub = mant * (10.0 ** ex)
            # se compara la mantisa a los decimales con que se publica, y el exponente exacto.
            # El caso pv<=0 (subdesbordamiento) ya se filtro arriba: si m no es None aqui, pv>0.
            import math
            ex_calc = math.floor(math.log10(pv))
        if ex is not None and ex_calc is not None:
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
    """La ANOVA secundaria que queda en el cuerpo se recalcula desde su corrida.

    [ACTUALIZADA 2026-09-17] Esta comprobacion vigilaba tres ANOVA. Las otras dos ya no tienen
    cita en el cuerpo: la de N=15 (F = 1,1379; p = 0,3417, sobre ablacion_n15_REMOTO, una sola
    corrida) porque §5.2/§6.1 se reescribieron con la media de 5 semillas (§F176), y la de N=120
    ("una diferencia de −0,43 puntos y p = 0,9328", el efecto que se anulaba) porque esa lectura de
    una sola corrida se sustituyo por el resultado replicado de 5 semillas: fs-en gana en las cinco
    semillas sobre N=120 (§F184), justo lo opuesto de "se anula". Ver FINDINGS §F195/§17.

    Sobrevive la de N=30, dos compilaciones del mismo modelo:

      §5.3  F = 0,2235 . p = 0,6382   n30_rerun_REMOTO, gemma4:31b vs -mlx, N=60

    Ninguna cifra esperada esta escrita en este codigo: se lee del informe (§L63).
    """
    CASOS = (
        ('results/n30_rerun_REMOTO', None,
         r'arroja F = (\d+),(\d+) con p = (\d+),(\d+)', 'la de las dos compilaciones'),
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

    check('la ANOVA secundaria reproduce desde su corrida (N=30, dos compilaciones)', mirados, fallos)


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
    cons = os.path.dirname(CSV_CONSOLIDADO)  # una sola fuente de verdad; ver F149
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
    PAL = {'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5, 'seis': 6, 'siete': 7,
           'ocho': 8, 'trece': 13, 'doce': 12}
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

    # 2) los modelos SIGNIFICATIVOS, con su delta y su p, derivados del artefacto y no de una
    # lista fija.
    #
    # El delta se LEE DEL INFORME, no se escribe aqui. La primera version comparaba el artefacto
    # contra un 0.1452 puesto a mano en el codigo, de modo que alterar la cifra del informe no
    # hacia fallar nada. Lo destapo la prueba por mutacion.
    #
    # Y la lista de NOMBRES tambien se leia a mano —('nemotron-mini:4b', 'llama3.2:latest')—, de
    # modo que al adoptar un consolidado donde solo el primero sigue siendo significativo, esta
    # comprobacion seguia exigiendo una frase sobre el segundo que el informe, correctamente, ya
    # no escribe. Se deriva de `sig`, que es lo que el artefacto declara.
    for nombre, d, pa in sig:
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
        p_pat = r'p<0,001' if pa < 0.001 else (r'p=%s' % ('%.3f' % pa).replace('.', ','))
        if re.search(re.escape(p_pat), s) is None:
            fallos.append('el informe no publica «%s» junto a %s' % (p_pat, nombre))

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
    cons = os.path.dirname(CSV_CONSOLIDADO)  # una sola fuente de verdad; ver F149
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

    # 2) contra lo que el informe publica. Con el consolidado publicado la p de Levene se escribe
    # en decimal («p = 0,18») porque no es extrema; con el nuevo sube a heterocedasticidad real y
    # el p baja a magnitudes que solo caben en notacion cientifica («p = 1,39 x 10^-11»), igual que
    # la del ANOVA. Y el verbo cambia: «no detecta» pasa a «detecta». Se aceptan ambas formas.
    mirados += 1
    m = re.search(r'prueba de Levene,? (?:no detecta|s\u00ed detecta|detecta) heterocedasticidad'
                  r',? \(p = (\d+),(\d+)\)', s)
    m_cient = re.search(r'prueba de Levene,? (?:no detecta|s\u00ed detecta|detecta) '
                        r'heterocedasticidad,? \(p = (\d+),(\d+) \u00d7 10'
                        r'([\u2070-\u2079\u00b9\u00b2\u00b3\u207b]+)\)', s)
    if m is not None:
        pub = float('%s.%s' % (m.group(1), m.group(2)))
        dec = len(m.group(2))
        if abs(round(pv, dec) - pub) >= 10 ** (-dec) / 2:
            fallos.append('el informe publica p = %s y el CSV da %.4f (a %d decimales, %.*f)'
                          % (pub, pv, dec, dec, round(pv, dec)))
    elif m_cient is not None:
        mant = float('%s.%s' % (m_cient.group(1), m_cient.group(2)))
        ex = _exp_super(m_cient.group(3))
        if ex is None:
            fallos.append('no se puede leer el exponente de la p de Levene: %r' % m_cient.group(3))
        else:
            import math
            ex_calc = math.floor(math.log10(pv)) if pv > 0 else None
            if ex_calc is None:
                fallos.append('la p de Levene subdesborda a 0,0: revisar la cota que escribe')
            elif ex_calc != ex:
                fallos.append('el informe publica exponente %d para Levene y el CSV da %d'
                              % (ex, ex_calc))
            else:
                dec = len(m_cient.group(2))
                mant_calc = pv / (10.0 ** ex_calc)
                if abs(round(mant_calc, dec) - mant) >= 10 ** (-dec) / 2:
                    fallos.append('el informe publica p = %s x 10^%d para Levene y el CSV da '
                                  '%.*f x 10^%d' % (m_cient.group(1) + ',' + m_cient.group(2), ex,
                                                     dec, round(mant_calc, dec), ex_calc))
    else:
        fallos.append('no se encuentra en el informe la frase de Levene con su p: '
                      'revisar si se reformulo')
    # 3) y que el numero de observaciones que cita el informe sea el del CSV. Formateado con
    # espacio como separador de miles («2 938», «3 120»); se acepta espacio normal, de no separacion
    # o ninguno, porque el informe usa el primero y algunos editores lo normalizan al segundo.
    mirados += 1
    miles = '{:,}'.format(N).replace(',', ' ')
    patron_num = re.escape(miles).replace(r'\ ', r'[\s\u00a0]?')
    if re.search(patron_num + r' observaciones', s) is None:
        fallos.append('el informe no cita las %s observaciones que da el CSV' % miles)

    check('el supuesto de homocedasticidad se recalcula desde el CSV', mirados, fallos)


def c_titulares(s):
    """Las cifras titulares, atadas a su corrida: las dos del resumen y la de la soberania.

    Hasta el consolidado publicado, las dos cifras de N=120 eran la **metrica restringida**
    —puntuando solo Personas y Organizaciones, porque el corpus no anotaba Locations—, calculada a
    mano del detalle por registro. Adoptado el consolidado de la re-corrida (decision 1, `§F154`),
    Locations SI esta anotada (545 entidades, verificado por `tp+fn` != 0), de modo que restringir
    ya no corrige nada: `§F64` midio que la restringida SUBESTIMA el valor real entre 1,3 y 5,7
    puntos. Las dos cifras de N=120 pasan a citar la metrica COMPLETA de la Tabla 7 —el mismo `f1`
    del CSV consolidado, no un recalculo aparte—, que es la unica manera de que esta comprobacion no
    diverja de `c_tabla7_vs_datos` por construccion.

    La del dominio (N=30) no cambia: ese corpus no tiene el defecto de Locations sin anotar, `§F64`
    no le aplica, y sigue siendo la metrica restringida de siempre sobre `n30_rerun_REMOTO`.
    """
    import json as _json
    g = _grupos_f1(CSV_CONSOLIDADO)
    CASOS_N120 = (('81,47', r'81[.,]47', 'gemma4:31b-mlx_baseline', 'F1 en espanol sobre N=120'),
                  ('82,13', r'82[.,]13', 'gemma4:31b-cloud_baseline',
                   'F1 de la variante alojada sobre N=120'))
    fallos, mirados = [], 0
    for etiq, patron, grupo, desc in CASOS_N120:
        mirados += 1
        if grupo not in g or not g[grupo]:
            fallos.append('%s no tiene f1 en %s' % (grupo, os.path.relpath(CSV_CONSOLIDADO, RAIZ)))
            continue
        obt = 100 * sum(g[grupo]) / len(g[grupo])
        esp = float(etiq.replace(',', '.'))
        if abs(obt - esp) > 0.006:
            fallos.append('%s: el informe dice %s %% y el CSV consolidado da %.2f %% sobre %d '
                          'registros' % (desc, etiq, obt, len(g[grupo])))
        mirados += 1
        if not re.search(patron, s):
            fallos.append('el informe ya no cita el %s %% (%s)' % (etiq, desc))

    # El del dominio (N=30), sin cambios: sigue restringido, porque ese corpus no tiene el defecto.
    import json as _json2
    ruta = os.path.join(BENCH_DIR, 'results/n30_rerun_REMOTO/detailed_results.json')
    mirados += 1
    if not os.path.exists(ruta):
        fallos.append('no existe results/n30_rerun_REMOTO, del que sale el 90,16 %')
    else:
        with open(ruta, encoding='utf-8') as fh:
            R = [r for r in _json2.load(fh) if r.get('model') == 'gemma4:31b-mlx']
        if not R:
            fallos.append('n30_rerun_REMOTO no trae el grupo gemma4:31b-mlx')
        else:
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
            if abs(obt - 90.16) > 0.006:
                fallos.append('F1 sobre el corpus del dominio: el informe dice 90,16 %% y el dato '
                              'da %.2f %% sobre %d registros' % (obt, len(R)))
            mirados += 1
            if not re.search(r'90[.,]16', s):
                fallos.append('el informe ya no cita el 90,16 % (F1 sobre el corpus del dominio)')

    check('las cifras titulares del resumen y de la soberania reproducen', mirados, fallos,
          'N=120 cita la metrica completa desde la decision 1; N=30 sigue restringido, sin cambio')


def c_ablacion(s):
    """Las tres diferencias del analisis de variantes de prompt, contra su corrida.

    [ACTUALIZADA 2026-09-17] Eran +4,38 pp / -0,72 / +10,4 sobre una sola corrida
    (ablacion_n15_REMOTO); con la media de 5 semillas declaradas (variantes_5semillas_n15_REMOTO,
    FINDINGS §F176) son +9,01 pp por localizar al espanol, +3,61 por los ejemplos few-shot en
    ingles y +13,19 por la combinacion. Aparecen en el resumen, el abstract (redondeadas a +13,2),
    §5.2 dos veces, §6.1 y las conclusiones.

    Se calculan desde el CSV crudo de las cinco semillas y no restando medias redondeadas.
    """
    import csv as _csv
    import collections as _c
    import glob as _glob
    ficheros = sorted(_glob.glob(os.path.join(
        BENCH_DIR, 'results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv')))
    if not ficheros:
        check('las diferencias del analisis de variantes reproducen', 0,
              ['no existe results/variantes_5semillas_n15_REMOTO/seed_*/benchmark_results.csv'])
        return
    g = _c.defaultdict(list)
    for ruta in ficheros:
        with open(ruta, encoding='utf-8') as fh:
            for r in _csv.DictReader(fh):
                if r.get('f1') not in (None, ''):
                    g[r['model']].append(float(r['f1']))
    m = {k: 100 * sum(v) / len(v) for k, v in g.items()}
    faltan = [k for k in ('zs-en', 'zs-es', 'fs-en', 'fs-es') if k not in m]
    if faltan:
        check('las diferencias del analisis de variantes reproducen', 0,
              ['las 5 semillas no traen los grupos %s' % ', '.join(faltan)])
        return
    esperado = (('localizacion al espanol', m['zs-es'] - m['zs-en'], r'\+9[.,]01'),
                ('few-shot en ingles', m['fs-en'] - m['zs-en'], r'\+3[.,]61'),
                ('combinacion de ambos', m['fs-es'] - m['zs-en'], r'\+?13[.,]19\b'))
    fallos, mirados = [], 0
    for etiq, val, patron in esperado:
        mirados += 1
        if not re.search(patron, s):
            fallos.append('el informe no cita la diferencia de %s, que el dato pone en %+.2f pp'
                           % (etiq, val))
    for etiq, val, esp in (('localizacion al espanol', m['zs-es'] - m['zs-en'], 9.01),
                           ('few-shot en ingles', m['fs-en'] - m['zs-en'], 3.61),
                           ('combinacion de ambos', m['fs-es'] - m['zs-en'], 13.19)):
        mirados += 1
        if abs(val - esp) > 0.006:
            fallos.append('%s: el informe dice %+.2f pp y el dato da %+.4f' % (etiq, esp, val))
    check('las diferencias del analisis de variantes reproducen', mirados, fallos,
          'media de 5 semillas desde 2026-09-17 (antes, una sola corrida)')

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
    ejecutar(c_sobriedad_docx, s)
    ejecutar(c_numeral_soberania, s)
    ejecutar(c_resumen_docx, s)
    ejecutar(c_indice, s)
    ejecutar(c_ninguna_comprobacion_huerfana, s)
    ejecutar(c_telemetria_ausente, s)
    ejecutar(c_corpus_idioma, s)
    ejecutar(c_firma_categorias, s)
    ejecutar(c_referencias_findings, s)
    ejecutar(c_docx_sano, s)
    ejecutar(c_pdf_al_dia, s)
    ejecutar(c_figura_vs_tabla, s)
    ejecutar(c_identificadores)
    ejecutar(c_aritmetica, s)
    ejecutar(c_recuentos, s)
    ejecutar(c_protocolo, s)
    ejecutar(c_tabla7_vs_datos, s)
    ejecutar(c_tabla7_desde_per_type, s)
    ejecutar(c_tukey_recuento, s)
    ejecutar(c_friedman, s)
    ejecutar(c_ablacion_idioma, s)
    ejecutar(c_redondeos, s)
    ejecutar(c_prosa_docx, s)
    ejecutar(c_frases_retiradas, s)
    ejecutar(c_tablas_y_biblio_docx, s)
    ejecutar(c_encabezados_docx, s)
    ejecutar(c_figuras_docx, s)
    ejecutar(c_tabla4_vs_datos, s)
    ejecutar(c_figura1_vs_artefacto, s)
    ejecutar(c_tablas_menores, s)
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
    # AL FINAL: lee los resultados de todas las anteriores.
    ejecutar(c_declaraciones)

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
                                             '\n             [DECLARADO] %s' % _motivo_declarado(cl)))
            if len(fallos) > 8:
                print('           ... y %d más' % (len(fallos) - 8))
            if (fallos or n == 0) and nota:
                print('           nota: %s' % nota)
    nuevos = fallos_totales - declarados
    print('\n  %d comprobaciones · %d fallos (%d declarados, **%d nuevos**) · %d vacías'
          % (len(resultados), fallos_totales, declarados, nuevos, vacias))
    if not nuevos and not vacias:
        print('  sin fallos nuevos: todo lo que falla esta declarado y asignado')
    # La edad de la declaracion mas vieja, para que la lista no se vuelva un aparcamiento. Cada
    # entrada ciega como centinela a su comprobacion (§L64), de modo que envejecer es un coste.
    if declarados:
        import datetime as _dt
        edades = []
        for _k, (_f, _m) in FALLOS_DECLARADOS.items():
            try:
                edades.append(((_dt.date.today() - _dt.date.fromisoformat(_f)).days, _k))
            except ValueError:
                pass
        if edades:
            d, k = max(edades)
            print('  %d declaraciones vigentes · la mas antigua lleva %d dia(s): «%s»'
                  % (len(FALLOS_DECLARADOS), d, k))
            if d >= 14:
                print('  ATENCION: una declaracion de mas de dos semanas suele significar que su '
                      'responsable no la tiene. Revisarla o reasignarla; cada una ciega una '
                      'comprobacion.')
    # El codigo de salida senala los fallos NUEVOS, no los declarados. Con la lista de declarados
    # devolvia 1 siempre, y `CLAUDE.md` describe esta herramienta como la puerta previa a cada
    # commit: una puerta que nunca abre no es una puerta. Con `--estricto` vuelve el comportamiento
    # anterior, para quien quiera que cualquier fallo, incluido el declarado, corte.
    if '--estricto' in sys.argv:
        return 1 if (fallos_totales or vacias) else 0
    # El mensaje se imprimia sin mirar `vacias`, de modo que en un clon superficial anunciaba
    # «codigo de salida 0» mientras la funcion devolvia 1: la comprobacion 50 sale VACIA porque el
    # clon no trae el commit `df9b4c4`. Quien lea eso cree que paso y su CI acaba de fallar. Ver
    # FINDINGS §F130.
    if fallos_totales and not nuevos and not vacias:
        print('  (codigo de salida 0: no hay fallos nuevos. Usar --estricto para que los declarados '
              'tambien corten)')
    if vacias:
        print('  (codigo de salida 1 POR LAS %d VACIAS, no por los fallos: una comprobacion que '
              'examina cero elementos no ha pasado, no se ha ejecutado.' % vacias)
        print('   Si es un clon superficial, le falta historia y la comprobacion 50 no puede '
              'leer el corpus anterior a la correccion: `git fetch --unshallow`.)')
    return 1 if (nuevos or vacias) else 0


if __name__ == '__main__':
    sys.exit(main())
