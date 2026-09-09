#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
estado_ramas.py — Comprueba la política de ramas, que si no se comprueba se podre.

Por qué existe
--------------
El 2026-09-09 el autor fijó la política: **se trabaja en `main`**, una rama aparte solo se justifica
para una tarea de menos de dos días, se declara en `CURRENT-TASKS.md` al crearla y se vuelve cuanto
antes. Quedó escrita en `CLAUDE.md` y en `CURRENT-TASKS.md`, y **nadie la comprobaba**. Es el patrón
que esta revisión ha encontrado una docena de veces: una regla que solo vive en un documento se
incumple sin que nada avise. Y ya se había incumplido antes de escribirla —`main` estaba dos commits
por detrás del remoto y una rama del día anterior guardaba la única copia declarada de una
dependencia real—.

Qué comprueba
-------------
1. **`main` está al día con el remoto.** Si va por detrás, todo lo demás se juzga sobre una copia
   vieja. El caso real: la rama local no tenía *upstream* y el `git pull` fallaba **en silencio**.
2. **Toda rama que no sea `main` ni `backup/*` está declarada** en el inventario de
   `CURRENT-TASKS.md`. Una rama sin entrada es una rama que nadie sabe que existe.
3. **Ninguna rama de trabajo pasa de dos días** sin actividad. Es el límite que fija la política.
4. **Qué ramas son retirables**, comprobado **por contenido y no por SHA**: `git cherry` marca lo
   que ya está aplicado en `main` aunque el identificador sea otro. Un recuento de commits distinto
   de cero no prueba trabajo pendiente.
5. **El respaldo que atestigua no se ha movido.** `backup/entrega-final-dataset-real-120` congela un
   estado entregado y su valor es que no cambia; si coincidiera con `main`, alguien lo avanzó. Esta
   comprobación existe porque **yo cometí ese error**, avanzando un `backup/` en el mismo commit en
   que escribía que no se avanzan.

Salida
------
Código 0 si la política se cumple. Distinto de 0 si algo la incumple, con el motivo y qué hacer.
Las ramas retirables **no** son un incumplimiento: son una recomendación, porque retirar una rama
remota afecta a los clones de otras sesiones y eso lo confirma el autor.
"""
import argparse
import datetime
import os
import re
import subprocess

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAREAS = os.path.join(RAIZ, 'CURRENT-TASKS.md')
ATESTIGUA = 'backup/entrega-final-dataset-real-120'
DIAS_MAX = 2


def git(*args):
    r = subprocess.run(['git'] + list(args), cwd=RAIZ, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sin-red', action='store_true',
                    help='no hace fetch; juzga con los refs remotos que ya haya en local')
    a = ap.parse_args()

    if not a.sin_red:
        rc, _, err = git('fetch', '--all', '--prune', '--quiet')
        if rc != 0:
            print('  AVISO: el fetch fallo (%s). Se juzga con los refs locales, que pueden estar '
                  'viejos.' % (err.split('\n')[0][:80] or 'sin detalle'))

    fallos, avisos, retirables = [], [], []

    # 1) main al dia
    rc, detras, _ = git('rev-list', '--count', 'HEAD..origin/main')
    rc2, rama, _ = git('branch', '--show-current')
    n_detras = int(detras) if detras.isdigit() else None
    print('  rama actual: %s' % (rama or '(desprendida)'))
    if rama != 'main':
        avisos.append('se esta trabajando en «%s» y la politica dice que en «main». Si es una '
                      'tarea de menos de dos dias, tiene que estar declarada en CURRENT-TASKS.md'
                      % rama)
    if n_detras is None:
        fallos.append('no se puede comparar con origin/main: ¿la rama tiene upstream? '
                      '`git branch --set-upstream-to=origin/main main`')
    elif n_detras:
        fallos.append('main va %d commit(s) por detras de origin/main. Todo lo que se comprueba '
                      'sobre esta copia se juzga sobre datos viejos. Hacer `git pull` y repetir'
                      % n_detras)
    else:
        print('  [ok]  main esta al dia con el remoto')

    # inventario declarado en CURRENT-TASKS.md
    try:
        with open(TAREAS, encoding='utf-8') as fh:
            tareas = fh.read()
    except OSError:
        tareas = ''
        fallos.append('no se puede leer CURRENT-TASKS.md, de modo que no se puede comprobar que '
                      'las ramas esten declaradas')

    _, salida, _ = git('for-each-ref', '--format=%(refname:short)|%(committerdate:short)',
                       'refs/remotes/origin')
    hoy = datetime.date.today()
    ramas = []
    for l in salida.split('\n'):
        if '|' not in l:
            continue
        nom, fecha = l.split('|', 1)
        nom = nom.strip()
        if nom in ('origin', 'origin/HEAD') or nom.endswith('/HEAD'):
            continue
        ramas.append((nom[len('origin/'):] if nom.startswith('origin/') else nom, fecha.strip()))

    print('\n  %-46s %-11s %-9s %s' % ('rama', 'ultimo', 'declarada', 'contenido'))
    for nom, fecha in sorted(ramas):
        if nom == 'main':
            print('  %-46s %-11s %-9s %s' % (nom, fecha, 'n/a', 'la rama de trabajo'))
            continue
        declarada = ('`%s`' % nom) in tareas
        # 4) retirable: ningun commit propio con contenido sin aplicar
        _, cherry, _ = git('cherry', 'main', 'origin/%s' % nom)
        pend = [l for l in cherry.split('\n') if l.startswith('+')]
        estado = 'todo aplicado' if not pend else '%d commit(s) SIN aplicar' % len(pend)
        print('  %-46s %-11s %-9s %s'
              % (nom, fecha, 'si' if declarada else '** NO **', estado))
        es_backup = nom.startswith('backup/')
        if not declarada and not es_backup:
            fallos.append('la rama «%s» no esta declarada en el inventario de CURRENT-TASKS.md' % nom)
        if not es_backup:
            try:
                d = (hoy - datetime.date.fromisoformat(fecha)).days
            except ValueError:
                d = None
            if d is not None and d > DIAS_MAX:
                avisos.append('la rama «%s» lleva %d dias sin actividad y la politica fija un '
                              'maximo de %d. O se vuelve a main, o se retira' % (nom, d, DIAS_MAX))
        if not pend and not es_backup:
            retirables.append(nom)
        if not pend and nom.startswith('backup/') and nom != ATESTIGUA:
            retirables.append('%s (espejo rodante, no atestigua nada)' % nom)

    # 5) el respaldo que atestigua no se ha movido
    _, sha_at, _ = git('rev-parse', 'origin/%s' % ATESTIGUA)
    _, sha_main, _ = git('rev-parse', 'main')
    if sha_at and sha_main:
        if sha_at == sha_main:
            fallos.append('«%s» coincide con main: alguien lo AVANZO. Atestigua un estado '
                          'entregado y su valor es no moverse. Devolverlo a su punta original'
                          % ATESTIGUA)
        else:
            print('\n  [ok]  %s sigue congelado en %s, distinto de main'
                  % (ATESTIGUA, sha_at[:7]))

    if retirables:
        print('\n  ── retirables: su contenido esta entero en main ──')
        for r in retirables:
            print('     %s' % r)
        print('     No es un incumplimiento. Retirar una rama remota afecta a los clones de otras')
        print('     sesiones, de modo que lo confirma el autor. `git cherry` ya acredita que no se')
        print('     llevan nada.')

    if avisos:
        print('\n  ── avisos ──')
        for x in avisos:
            print('     %s' % x)
    if fallos:
        print('\n  ── INCUMPLE la politica ──')
        for x in fallos:
            print('     %s' % x)
        print('\n  Politica completa: CLAUDE.md, seccion «Ramas: se trabaja en `main`».')
        return 1
    print('\n  la politica de ramas se cumple%s' % (' (con %d aviso(s))' % len(avisos) if avisos else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
