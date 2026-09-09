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
]


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

    fallos = []
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
    if fallos:
        print(f'{len(fallos)} de {len(ARTEFACTOS)} artefactos no se vigilan:')
        for rel, por in fallos:
            print(f'  - {rel}: {por}')
        return 1
    print(f'{len(ARTEFACTOS)} de {len(ARTEFACTOS)}: ningun artefacto puede faltar sin que se note')
    return 0


if __name__ == '__main__':
    sys.exit(main())
