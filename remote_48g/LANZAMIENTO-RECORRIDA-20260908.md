# Autorización de lanzamiento: la re-corrida completa va entera en el equipo de 48 GB

**Del autor, a través del equipo principal. 2026-09-08.**
Responde a vuestro pendiente: «lanzar la re-corrida completa de los 13 modelos (N=120, dos modos, un modelo
por turno). El harness está probado y listo. […] a la espera de confirmar dónde se lanza.»

## Decisión

**Todo en el equipo de 48 GB.** Los trece modelos, los dos modos, de principio a fin. No se reparte con el
equipo de 16 GB.

Se consideró repartir —los modelos de hasta ~12B en el de 16 GB y los de 31B y MLX en el de 48— para acortar
el tiempo total, y se descartó. La razón es de validez, no de comodidad: el estudio publica latencia,
tokens/s y un índice Tok/s/B por modelo, y esas columnas dejan de ser comparables entre filas si unas se
midieron en una máquina y otras en otra. El informe ya arrastra dos salvedades de telemetría —la latencia de
`gemma4:31b-cloud`, cuantizada por el `--request-delay`, y las siete filas de `nemotron-mini:4b` con latencia
cero— y añadir una tercera, esta vez estructural y afectando a media tabla, sería peor que esperar.

## Antes de lanzar

1. Aplicad primero las 63 localizaciones de Kleptotrace al subconjunto embebido en el corpus de 120, según
   `remote_48g/RESPUESTA-LOCATIONS-EMBEBIDAS-20260908.md`. **Va antes que la corrida**: si se lanza sin eso,
   quince de los ciento veinte artículos siguen puntuando *Locations* contra el vacío y habría que repetirla.
   Comprobación: 119 de 120 con `locations`, 545 en total.
2. `tools/verificar_corrida.py` en VÁLIDA sobre el smoke test.
3. `run_config.json` con `--rag-mode kb_combined` y `max_tokens=4096`.

## Durante y después

Mantened el punto de control por corrida, que ya salvó barridos de varias decenas de horas. Al terminar cada
modelo conviene comprobar tres cosas antes de pasar al siguiente, porque detectarlas tarde cuesta la corrida
entera:

- `parse_method='failed'` y cuántos registros con `recall=0`.
- `tp + fn` agregado por categoría **mayor que cero** en las tres, *Locations* incluida.
- Ninguna fila con F1 por encima de la media de precisión y exhaustividad.

Y distinguid las dos causas de fallo, que se parecen y no son lo mismo: latencia cero con cero tokens es un
rechazo de infraestructura; latencia alta con `content` vacío es el arnés perdiendo la respuesta.

## Al cerrar

Fusionad en la rama de trabajo del equipo principal y borrad las ramas temporales, según
`remote_48g/INSTRUCCIONES-CIERRE-20260908.md`. Vuestra rama va **13 commits por delante** en código y datos y
**12 por detrás** en documentación, así que conviene traer `main` antes de fusionar.
