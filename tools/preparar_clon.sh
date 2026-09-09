#!/bin/sh
# preparar_clon.sh — pone un clon recien hecho en estado de trabajo.
#
# Por que existe
# --------------
# Un clon del repositorio NO queda listo, y de tres formas distintas que solo se ven cuando algo
# falla. Comprobado el 2026-09-09 clonando de verdad (FINDINGS §F130):
#
#   1. `core.hooksPath` es configuracion LOCAL, de modo que el clon no tiene la puerta de commit
#      aunque el gancho este versionado. Ya estaba escrito en CLAUDE.md y en FINDINGS §F93.
#   2. Un clon superficial (`--depth 1`) no trae el commit `df9b4c4`, y sin el la comprobacion 50
#      no puede leer el corpus anterior a la correccion del mojibake: sale VACIA, y una comprobacion
#      vacia no ha pasado, no se ha ejecutado.
#   3. `.setenv.sh` esta en `.gitignore`, asi que el clon no tiene credenciales.
#
# Esto no adivina nada ni instala nada: comprueba las tres, arregla las dos que se pueden arreglar
# y dice en voz alta la que no.

set -e
cd "$(dirname "$0")/.."

echo "  preparando $(basename "$(pwd)")"
echo

# 1. la puerta de commit
ACTUAL=$(git config core.hooksPath || true)
if [ "$ACTUAL" = ".githooks" ]; then
  echo "  [ok]  la puerta de commit ya esta configurada"
else
  git config core.hooksPath .githooks
  echo "  [arreglado] core.hooksPath -> .githooks (antes: ${ACTUAL:-sin configurar})"
fi

# 2. la historia completa
if [ -f .git/shallow ]; then
  echo "  [aviso] el clon es superficial: la comprobacion 50 saldra VACIA."
  echo "          se trae la historia completa..."
  git fetch --unshallow
  echo "  [arreglado] historia completa: $(git rev-list --count HEAD) commits"
else
  echo "  [ok]  historia completa ($(git rev-list --count HEAD) commits)"
fi
if git cat-file -e df9b4c4 2>/dev/null; then
  echo "  [ok]  df9b4c4 presente: la comprobacion 50 puede leer el corpus historico"
else
  echo "  [FALLA] falta df9b4c4 incluso con la historia completa. Sin ese commit la Tabla 17"
  echo "          del informe no se puede verificar contra nada, porque el corpus actual ya no"
  echo "          tiene el defecto que ella mide. No reescribir la historia de git."
fi

# 3. los secretos, que no se pueden arreglar desde aqui
if [ -f .setenv.sh ]; then
  echo "  [ok]  .setenv.sh presente"
else
  echo "  [aviso] no hay .setenv.sh, y no esta en git a proposito. Sin el no hay token para"
  echo "          empujar ni claves de proveedor. Hay que copiarlo de una copia de trabajo."
fi

echo
echo "  comprobando que el aparato corre..."
if python3 tools/verificar_informe.py > /tmp/preparar_clon.salida 2>&1; then
  tail -2 /tmp/preparar_clon.salida | sed 's/^/  /'
  echo "  [ok]  el verificador devuelve 0"
else
  tail -4 /tmp/preparar_clon.salida | sed 's/^/  /'
  echo "  [aviso] el verificador devuelve distinto de 0. Si es por VACIAS, mirar arriba; si es"
  echo "          por fallos NUEVOS, hay trabajo que hacer y no un problema del clon."
fi
python3 tools/auditar_afirmaciones.py 2>&1 | tail -1 | sed 's/^/  /'
