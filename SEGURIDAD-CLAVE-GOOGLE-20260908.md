# Clave de API de Google expuesta en el historial — estado y acciones pendientes

**Fecha:** 2026-09-08. **Detectado al preparar la publicación del repositorio**, que el informe declara
público en la referencia [37] y en el Anexo A.

## Qué había

Una clave de API de Google (`AIzaSyDrJn…ENwc`, 39 caracteres) en `test_flash.py`, presente en **20 de los
139 commits**, desde el commit inicial `0cc973b` (1 de julio de 2026) hasta `bb79279` (1 de septiembre).
La versión vigente del fichero ya estaba limpia: lee la clave de `GOOGLE_API_KEY` en el entorno. Lo que
seguía expuesto era el historial.

## Qué se ha hecho

1. **Respaldo completo** en `git bundle` de todas las ramas y etiquetas antes de tocar nada.
2. **Reescritura del historial** con `git filter-repo --replace-text`, sustituyendo la clave por el
   marcador `<GOOGLE_API_KEY-PURGADA-DEL-HISTORIAL>` en los 20 commits afectados.
3. **Verificación:** 0 commits con la clave, 139 commits conservados, 3 ramas, 4 etiquetas, 692 ficheros.
   El informe final intacto: 16 666 palabras, 837 líneas, 37 entradas bibliográficas.
4. **Push forzado** de las tres ramas y las cuatro etiquetas. Local y remoto coinciden.

## Lo que NO resuelve la reescritura

**GitHub sigue sirviendo los objetos antiguos.** Comprobado el mismo día: la API devuelve HTTP 200 para el
commit `bb79279` y su versión de `test_flash.py` **todavía contiene la clave en claro**. Los objetos quedan
sin referencia pero siguen recuperables por SHA directo, y GitHub no ejecuta el recolector de basura por
iniciativa propia.

A eso se añade que la clave estuvo en un remoto durante **dos meses**: cualquiera que clonara el repositorio
en ese periodo la tiene, y ninguna reescritura alcanza a esas copias.

## Acciones pendientes, por orden de urgencia

1. **REVOCAR la clave en Google Cloud Console.** Es la única medida que cierra la exposición de verdad, y
   solo puede hacerla el titular de la cuenta. Todo lo demás es mitigación parcial.
2. **Solicitar a GitHub Support la purga de objetos inalcanzables** del repositorio, que es el procedimiento
   documentado para forzar el recolector. Sin ese paso, el blob antiguo sigue accesible.
3. **NO hacer público el repositorio hasta completar el punto 1.** Publicarlo ahora convertiría una clave
   recuperable-si-conoces-el-SHA en una clave indexable.
4. Avisar a los equipos con clon del repositorio —el remoto de 48 GB, Claude Desktop— de que **la historia
   se reescribió y deben volver a clonar**: sus clones son incompatibles con el remoto.

## Por qué importa para la tesina

La referencia [37] y el Anexo A afirman que el código y los corpus «están publicados en el repositorio del
trabajo». Hoy el repositorio es **privado** (verificado contra la API: `"private": true`), de modo que la
afirmación no es cierta para un tribunal que intente comprobarla. La secuencia correcta es revocar la clave,
pedir la purga a GitHub y solo entonces hacerlo público.
