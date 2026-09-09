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

ARTEFACTOS = [
    'tools/generar_figuras_informe.py',
    f'{BENCH}/ANALISIS_CONJUNTO_20260907/merge_manifest.json',
    f'{BENCH}/ANALISIS_CONJUNTO_20260907/merged_results.csv',
    f'{BENCH}/COMPOSICION_FP_20260908/composicion_fp_26_grupos.json',
    f'{BENCH}/ANALISIS_MOJIBAKE_20260908/efecto_mojibake.json',
    f'{BENCH}/CORRELACION_CAPACIDAD_20260908/correlacion.json',
    'DEFENSA-PREGUNTAS-Y-RESPUESTAS.md',
]


def verificador():
    return subprocess.run(
        [sys.executable, os.path.join(RAIZ, 'tools/verificar_informe.py')],
        cwd=RAIZ, capture_output=True, text=True)


def main():
    partida = verificador()
    if partida.returncode != 0:
        print('El verificador ya falla sin esconder nada. Corrige eso primero.')
        print(partida.stdout[-800:])
        return 2
    print('control: el verificador pasa con todo en su sitio\n')

    fallos = []
    for rel in ARTEFACTOS:
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

        if r.returncode == 0:
            fallos.append((rel, 'el verificador pasa sin el artefacto'))
            print(f'  NO DETECTA {rel}')
        else:
            marca = 'VACIA' if 'VACIA' in r.stdout else 'fallo'
            print(f'  detecta ({marca:5})  {rel}')

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
