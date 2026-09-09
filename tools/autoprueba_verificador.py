#!/usr/bin/env python3
"""Autoprueba de `verificar_informe.py`: comprueba que no aprueba a ciegas.

El verificador lee sus cifras de artefactos externos. Si uno de ellos desaparece
o cambia de ruta, la comprobacion que lo usa no debe pasar: debe marcarse VACIA y
devolver codigo distinto de cero. Es el defecto de `LEARNING.md §L57` — una
comprobacion que devuelve el valor del exito porque miro el sitio equivocado.

Esta autoprueba esconde cada artefacto por turno y exige que el verificador se
entere. Restaura siempre, incluso si se interrumpe.

    python3 tools/autoprueba_verificador.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = 'repos/ner-llm-entity-benchmark/results'

# Cada artefacto con la comprobacion que TIENE que enterarse de su ausencia. Sin ese segundo campo
# la autoprueba solo pregunta «fallo algo», y varios ficheros los leen dos o tres comprobaciones: basta
# con que una se entere para dar el visto bueno mientras las otras se lo saltan en silencio. Paso el
# 2026-09-09 —el indice de defensa bajaba de 13 a 9 elementos y seguia en «ok»— y esta escrito en
# `LEARNING §L60`. El texto es un fragmento del nombre de la comprobacion, no el nombre entero.
ARTEFACTOS = [
    ('tools/generar_figuras_informe.py', 'Figura 1'),
    (f'{BENCH}/ANALISIS_CONJUNTO_20260907/merge_manifest.json', 'protocolo homog'),
    (f'{BENCH}/ANALISIS_CONJUNTO_20260907/merged_results.csv', 'Tabla 7 reproduce'),
    (f'{BENCH}/COMPOSICION_FP_20260908/composicion_fp_26_grupos.json', 'Figura 1'),
    (f'{BENCH}/ANALISIS_MOJIBAKE_20260908/efecto_mojibake.json', 'Tabla 18'),
    (f'{BENCH}/CORRELACION_CAPACIDAD_20260908/correlacion.json', 'indice de defensa'),
    ('DEFENSA-PREGUNTAS-Y-RESPUESTAS.md', 'indice de defensa'),
    (f'{BENCH}/ROBUSTEZ_ESTADISTICA_20260909/robustez.json', 'indice de defensa'),
    (f'{BENCH}/ANALISIS_CONJUNTO_20260907/levene.json', 'homocedasticidad'),
    # Anadidos el 2026-09-09: el verificador cita 26 rutas y esta lista cubria 9. Las seis de
    # abajo respaldan cifras PUBLICADAS y su ausencia produce un fallo atribuible, comprobado
    # escondiendolas una a una. Ver FINDINGS §F92.
    (f'{BENCH}/ANALISIS_CONJUNTO_20260907/statistical_report.md', 'ANOVA titular'),
    (f'{BENCH}/ablacion_n15_REMOTO/benchmark_results.csv', 'ANOVA secundarias'),
    (f'{BENCH}/n30_rerun_REMOTO/benchmark_results.csv', 'ANOVA secundarias'),
    (f'{BENCH}/benchmark_balanced_120_20260825_071207/benchmark_results.csv', 'ANOVA secundarias'),
    (f'{BENCH}/cloud_n15_limpio_20260905/benchmark_results.csv', 'Tabla 4'),
    (f'{BENCH}/gemma4_31b_n15_REMOTO/benchmark_results.csv', 'tablas 5, 6 y 8'),
    (f'{BENCH}/benchmark_results.csv', 'Tabla 4'),
    # Anadido el 2026-09-09: lo detecto la propia cobertura de esta autoprueba al aparecer la
    # comprobacion 45, que es para lo que se escribio (§F112). Su comprobacion ya falla —fallo
    # declarado a nombre del equipo remoto—, de modo que esconderlo cambia el TEXTO del fallo y no
    # su existencia; la autoprueba lo situa en el tercer estado, «bloqueado por un fallo abierto»,
    # y eso es lo correcto: no puede acreditarse hasta que §3.bis.15 cierre.
    ('tools/sensibilidad_combinada.py', 'per_type'),
    # Anadido el 2026-09-09 con la comprobacion 47: hasta entonces `friedman.json` solo lo leia
    # `c_defensa`, y esconderlo no producia un fallo atribuible a esa cifra (§F116).
    (f'{BENCH}/ROBUSTEZ_ESTADISTICA_20260908/friedman.json', 'Friedman'),
    # Los tres entregables: desde §F94 el verificador los lee, y esconder uno debe notarse.
    ('Informe_Final_Tesina_NER_plantilla_revision_final_2026-09-03.docx', 'modelos excluidos'),
    ('Informe_Final_Tesina_NER.docx', 'modelos excluidos'),
    ('doc/organized/Hito_5_Tarea4_Informe_Final/2026-07-04_Borrador-Informe-Final-Tesina.docx',
     'modelos excluidos'),
]


def _rutas_del_verificador():
    """Rutas o nombres de fichero que cita el verificador, leidos de su fuente.

    Se derivan, no se escriben a mano: un denominador escrito a mano deja de ser cierto en cuanto
    se anade una dependencia, y calla (§L63).
    """
    import re as _re
    try:
        with open(os.path.join(RAIZ, 'tools/verificar_informe.py'), encoding='utf-8') as fh:
            src = fh.read()
    except OSError:
        return 0
    lit = set()
    for m in _re.finditer(r"[\'\"]((?:results|repos|doc|tools)/[A-Za-z0-9_./:-]+)[\'\"]", src):
        lit.add(m.group(1))
    for m in _re.finditer(r"[\'\"]([A-Za-z0-9_.-]+\.(?:json|csv|md|py|docx))[\'\"]", src):
        lit.add(m.group(1))
    return lit


def _informe_cobertura():
    """Dice que dependencias del verificador NO estan vigiladas, y por que es aceptable.

    La primera version imprimia «15 de las 26 rutas que el verificador cita», y eso sugeria que
    los 15 vigilados son un subconjunto de las 26, cuando no lo son: varios se construyen con
    variables y no aparecen en ese recuento. Un cociente entre dos conjuntos que no estan
    anidados es peor que no dar cociente. Aqui se enumera la diferencia real.
    """
    citadas = _rutas_del_verificador()
    vigilados = {rel for rel, _ in ARTEFACTOS}

    def _vigilada(r):
        return any(r in v or v.endswith(r) for v in vigilados)

    sin = sorted(r for r in citadas if not _vigilada(r))
    generico = [r for r in sin if '/' not in r]
    directorio = [r for r in sin if '/' in r
                  and not os.path.splitext(r)[1]]
    resto = [r for r in sin if r not in generico and r not in directorio]
    print('  dependencias citadas en la fuente del verificador: %d · sin vigilar: %d'
          % (len(citadas), len(sin)))
    print('    %d nombres genericos que se resuelven en tiempo de ejecucion' % len(generico))
    print('    %d rutas de directorio, no de fichero' % len(directorio))
    # Los dos respaldos de la decision 3 quedan fuera A PROPOSITO: su comprobacion es un AVISO
    # declarado —«2 JSON rotos declarados, pendientes de decision del autor»—, de modo que
    # esconderlos no cambia el resultado y la prueba no podria atribuir nada.
    APOSTA = {'benchmark_summary.json.bak_prescore', 'detailed_results.json.bak_prescore'}
    aposta = [r for r in resto if os.path.basename(r) in APOSTA]
    inesperados = [r for r in resto if r not in aposta]
    if aposta:
        print('    %d fuera a proposito: los respaldos rotos de la decision 3, cuya '
              'comprobacion es un AVISO declarado' % len(aposta))
    if inesperados:
        print('    %d ficheros concretos SIN VIGILAR Y SIN MOTIVO:' % len(inesperados))
        for r in inesperados:
            print('      - %s' % r)
    print('  (el recuento se deriva de la fuente; los artefactos que el verificador construye')
    print('   con variables no aparecen en el, de modo que no es un cociente entre conjuntos')
    print('   anidados y no se presenta como tal)')


def verificador():
    return subprocess.run(
        [sys.executable, os.path.join(RAIZ, 'tools/verificar_informe.py')],
        cwd=RAIZ, capture_output=True, text=True)


def malas(r):
    """Nombres de las comprobaciones que fallan o quedan vacias.

    Se comparan CONJUNTOS y no el codigo de salida. Exigir que el verificador pase por completo
    dejaba esta autoprueba inerte en cuanto algo ajeno fallara: ocurrio el 2026-09-09, cuando la
    fusion del equipo trajo dos `.log` a cero bytes que no se pueden borrar —son registros— y la
    autoprueba se abortaba entera sin protejer nada. Lo que hay que exigir es que esconder un
    artefacto **anada** un fallo, no que no hubiera ninguno antes.
    """
    fuera = set()
    for l in (r.stdout or '').split('\n'):
        s = l.strip()
        # CONOC es el estado de una comprobacion cuyos fallos estan todos declarados. Se cuenta
        # igual que FALLA: para esta autoprueba lo que importa es que la comprobacion **no esta en
        # verde**, de modo que un fallo nuevo suyo tiene que distinguirse del que ya traia.
        if s.startswith('FALLA') or s.startswith('VACIA') or s.startswith('CONOC'):
            fuera.add(' '.join(s.split()[1:]).split('(')[0].strip())
    return fuera


def main():
    partida = verificador()
    previas = malas(partida)
    if previas:
        print('aviso: %d comprobacion(es) ya fallan sin esconder nada '
              '(declaradas o no), y se descuentan:' % len(previas))
        for x in sorted(previas):
            print('    - %s' % x)
        print()
    else:
        print('control: el verificador pasa con todo en su sitio\n')

    fallos, bloqueadas = [], []
    for rel, esperada in ARTEFACTOS:
        ruta = os.path.join(RAIZ, rel)
        if not os.path.isfile(ruta):
            fallos.append((rel, 'el artefacto no existe; la prueba no puede correr'))
            print(f'  AUSENTE   {rel}')
            continue
        tmp = tempfile.mkdtemp(prefix='autoprueba-')
        guardado = os.path.join(tmp, os.path.basename(rel))
        shutil.move(ruta, guardado)
        try:
            r = verificador()
        finally:
            shutil.move(guardado, ruta)
            shutil.rmtree(tmp, ignore_errors=True)

        nuevas = malas(r) - previas
        # Comparacion insensible a acentos: la primera version esperaba «protocolo homogeneo» y la
        # comprobacion se llama «protocolo homogéneo», de modo que la atribucion fallaba por una tilde
        # y se reportaba como hueco de cobertura.
        def _pl(s_):
            import unicodedata
            return ''.join(c for c in unicodedata.normalize('NFD', s_.lower())
                           if unicodedata.category(c) != 'Mn')
        atribuida = [n for n in nuevas if _pl(esperada) in _pl(n)]
        # Una comprobacion que YA esta en rojo no puede servir de centinela: esconder el artefacto
        # no cambia el CONJUNTO de comprobaciones fallidas, de modo que `nuevas` sale vacio y la
        # prueba lo reportaria como hueco de cobertura cuando en realidad esta bloqueada por otra
        # cosa. Aparecio el 2026-09-09 al poner los tres .docx bajo vigilancia mientras §F94 esta
        # sin corregir. Se distingue en lugar de disimularse, y no cuenta como fallo: es §L57, un
        # control que no puede distinguir «bien» de «no mirado».
        if any(_pl(esperada) in _pl(x) for x in previas):
            bloqueadas.append((rel, esperada))
            print(f'  BLOQUEADO  {rel}  ->  «{esperada}» ya esta en rojo, no puede hacer de centinela')
            continue
        if not nuevas:
            fallos.append((rel, 'esconderlo no anade ninguna comprobacion fallida'))
            print(f'  NO DETECTA  {rel}')
        elif not atribuida:
            fallos.append((rel, 'falla otra comprobacion, pero no «%s», que es la que lo usa; '
                                'fallan: %s' % (esperada, ', '.join(sorted(nuevas))[:90])))
            print(f'  MAL ATRIBUIDO  {rel}')
        else:
            marca = 'VACIA' if any('VACIA' in l and any(n in l for n in atribuida)
                                   for l in r.stdout.split('\n')) else 'fallo'
            print(f'  detecta ({marca:5})  {rel}  ->  «{esperada}»')

    print()
    if bloqueadas:
        print(f'{len(bloqueadas)} artefacto(s) no se pueden vigilar todavia, porque la '
              f'comprobacion que los usa ya esta en rojo:')
        for rel, esp in bloqueadas:
            print(f'  - {rel}  («{esp}»)')
        print('  Vuelven a ser vigilables en cuanto ese fallo se corrija. No es un hueco de')
        print('  cobertura de esta prueba: es una consecuencia de que el defecto siga abierto.')
        print()
    if fallos:
        print(f'{len(fallos)} de {len(ARTEFACTOS)} artefactos no se vigilan:')
        for rel, por in fallos:
            print(f'  - {rel}: {por}')
        return 1
    # La cifra que importa no es «N de N», que siempre sale redonda: es cuantos de los
    # artefactos que el verificador REALMENTE lee estan vigilados. Un «9 de 9» sobre 26
    # dependencias se lee como universal y no lo es (§L47).
    n_vig = len(ARTEFACTOS) - len(bloqueadas)
    print(f'{n_vig} de {len(ARTEFACTOS)} artefactos vigilados: ninguno puede faltar sin que se '
          f'note' + (f' ({len(bloqueadas)} bloqueado(s) por un fallo abierto)' if bloqueadas else ''))
    _informe_cobertura()
    return 0


if __name__ == '__main__':
    sys.exit(main())
