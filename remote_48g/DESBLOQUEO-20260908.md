# Estáis desbloqueados: §2.bis.2 ya está resuelto

**Fecha:** 2026-09-08. **De:** equipo principal.

Vuestro cierre de avances paralelos dice que lo que resta «depende de correr benchmark (bloqueado por
§2.bis.2 Locations)». **Ese bloqueo ya no existe.** La solución está en `origin/main` desde hace un rato, y
como trabajáis en una rama puede que no la hayáis visto.

## Lo que hay en `main` y os desbloquea

**`tools/recuperar_locations_n120.py`** — recupera las localizaciones sin necesitar el script de muestreo
perdido, emparejando por el texto de cada artículo, que es único. Verificado: **105 de 120 emparejados y 482
localizaciones** en 104 artículos. El detalle de por qué funciona y las dos precauciones que exige están en
`remote_48g/RESPUESTA-2BIS2-LOCATIONS-20260908.md`.

**`tools/aplicar_locations_manuales.py`** con `data/anotaciones/locations_manuales.json` — cubre lo que
ninguna fuente aporta. El autor decidió anotar a mano los quince de Kleptotrace, y de paso los treinta del
sintético: **63 y 20 localizaciones**, con el criterio tomado de las 482 recuperadas para que ambos orígenes
sean homogéneos.

La secuencia completa, en orden, está en la sección **2.bis.2.bis** del encargo. Un aviso que ya os hicimos y
repetimos porque es fácil de pasar por alto: **vuestro `conll2002_es.json` no tiene localizaciones**. El
arreglo del conversor es correcto, pero el fichero commiteado quedó con la salida anterior. Hay que
reejecutar `download_conll2002.py` antes del paso 1.

## Vuestras dos investigaciones, aceptadas

**§3.3.** Vuestro resultado es más informativo que el mío. El contraste publicado tiene desviación 5,52 sobre
valores de 10,4 / −0,43 / 3,11, y es inestable; pero el **idioma puro en zero-shot** da +2,24 pp con
desviación 1,86, consistentemente positivo. Eso separa dos cosas que estaban mezcladas: el efecto del idioma
y el de los ejemplos. La conclusión de que sin réplicas no se declara sigue en pie, y ahora con un matiz que
mejora el hallazgo.

**§3.2.** Vuestros totales coinciden **exactamente** con los nuestros —84/36/594 personas y 128/69/812
organizaciones— y la fracción ibérica de organizaciones casi (196 frente a 198). Que la de personas
infra-cuente por no marcar apellidos sin acento está bien documentado y es el tipo de límite que hay que
declarar en lugar de disimular.

Y tenéis razón en lo importante: **el contraste por subconjunto de entidad no se puede calcular con los
artefactos actuales**. Por eso hemos añadido al encargo la sección **3.bis**, que pide persistir el registro
por entidad en la re-corrida. Sin él, la re-corrida tampoco respondería a esa pregunta.

## Lo que sigue esperando decisión del autor

**§2.bis.1, los ejemplares contaminados.** El autor decidió **esperar a vuestra re-corrida**: no
publicaremos cifras descontadas a mano, las tomaremos de vuestras corridas limpias. Cablead el manifiesto de
exclusión y adelante.

**§3.1, el idioma del generador N=30.** Escalado, con vuestra evidencia. Sigue abierto.
