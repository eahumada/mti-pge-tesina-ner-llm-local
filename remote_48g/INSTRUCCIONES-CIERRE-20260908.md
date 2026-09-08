# Instrucciones para el equipo remoto — actualización y cierre

**Fecha:** 2026-09-08. **De:** equipo principal. **Esta rama ya contiene todo lo que necesitáis**: se ha
fusionado `main` en ella, de modo que no tenéis que ir a buscar nada a otra rama. Ese fue el problema de
hace un rato y no debería repetirse.

---

## 1. Estabais bloqueados por algo que ya estaba resuelto

Vuestro cierre de avances paralelos declaraba que lo que restaba dependía de correr el benchmark, «bloqueado
por §2.bis.2 Locations». **Ese bloqueo ya no existía cuando lo escribisteis.** La solución llevaba un rato en
`main` y, como trabajáis en rama, no la visteis. Con esta fusión la tenéis aquí.

Es un fallo de coordinación que nos toca a los dos: nosotros publicamos en `main` y vosotros trabajáis en
rama. La regla que sacamos de esto, y que conviene que apliquéis: **antes de declarar un bloqueo, traed
`main`**. Un `git fetch origin && git log origin/main --oneline -10` cuesta segundos y os habría ahorrado el
cierre en falso.

## 2. Lo que os desbloquea, ya en esta rama

**`tools/recuperar_locations_n120.py`** recupera las localizaciones sin el script de muestreo perdido,
emparejando por el texto de cada artículo, que es único. Verificado: **105 de 120 emparejados y 482
localizaciones**. Las dos precauciones que exige están documentadas en el propio script; la que importa es
que hay que **normalizar antes de comparar**, porque comparando el texto literal empareja 1 de 120.

**`tools/aplicar_locations_manuales.py`** con `data/anotaciones/locations_manuales.json` cubre lo que ninguna
fuente aporta: el autor decidió anotar a mano los quince de Kleptotrace y los treinta del sintético, **63 y
20 localizaciones**, con el criterio tomado de las 482 recuperadas para que ambos orígenes sean homogéneos.

**La secuencia completa, en orden, está en la sección 2.bis.2.bis del encargo.** Y un aviso que ya os hicimos
dos veces y repetimos porque es fácil de pasar por alto: **vuestro `conll2002_es.json` no tiene
localizaciones**. El arreglo del conversor es correcto, pero el fichero commiteado quedó con la salida
anterior. Hay que reejecutar `download_conll2002.py` antes del paso 1.

## 3. Vuestras dos investigaciones, aceptadas — y una mejora nuestro hallazgo

**§3.3, la ablación. Vuestro resultado es mejor que el nuestro.** Nosotros habíamos concluido que el efecto
del prompt en español «no replica». Vosotros separáis dos cosas que teníamos mezcladas: el contraste
publicado —idioma **más** ejemplos— tiene desviación 5,52 sobre valores de 10,4 / −0,43 / 3,11 y es
inestable; pero el **idioma puro en zero-shot** da **+2,24 pp con desviación 1,86, consistentemente
positivo**. Es decir: hay un efecto pequeño y estable del idioma, y lo que no replica es su interacción con
los ejemplos. Eso es más preciso que «no replica» a secas, y así se redactará en el informe.

**§3.2, la composición.** Vuestros totales coinciden **exactamente** con los nuestros —84/36/594 personas y
128/69/812 organizaciones— y la fracción ibérica de organizaciones casi, 196 frente a 198. Que la de personas
infra-cuente por no marcar apellidos sin acento está bien documentado, y documentar un límite en lugar de
disimularlo es lo que hay que hacer.

## 4. Un requisito nuevo que sale de vuestro trabajo: registro por entidad

Tenéis razón en lo importante: **el contraste por subconjunto de entidad no se puede calcular con los
artefactos actuales**, porque los `detailed_results.json` guardan métricas por artículo y no qué entidad se
extrajo ni si acertó. Sin eso, **la re-corrida tampoco respondería** a la pregunta que más nos interesa.

Hemos añadido la **sección 3.bis** al encargo: que el evaluador persista, por registro, la lista de entidades
extraídas con su veredicto —acierto, falso positivo, falso negativo— y la entidad de referencia con la que
emparejó. Con eso, el contraste se calcula después sin reejecutar nada.

Ese registro habría permitido además diagnosticar sin discusión otros dos defectos de este estudio: el doble
emparejamiento, que se detectó indirectamente por `recall > 1.0`, y la naturaleza de los «errores de límite»,
que resultaron agrupar tres fenómenos distintos.

**Sobre la clasificación de entidades ibéricas:** para el contraste conviene una **lista explícita revisada a
mano** en lugar de una heurística. Son unos pocos cientos de entidades de referencia distintas. Una heurística
que falla en un tercio de los casos, como la vuestra reconoce, contaminaría justo el contraste que se quiere
medir.

## 5. Al terminar: fusionar y limpiar

Cuando la re-corrida esté completa y verificada con vuestra propia `tools/verificar_corrida.py`:

1. **Fusionad esta rama en `sesion/revision-final-20260908`**, que es la rama de trabajo del equipo principal,
   y desde ahí se lleva a `main`. No empujéis directamente a `main`.
2. **Borrad las ramas temporales** una vez fusionadas, en local y en el remoto:
   `git branch -d fix/recorrida-correcciones-20260908` y
   `git push origin --delete fix/recorrida-correcciones-20260908`.
3. **No borréis** `backup/revision-final-20260908` ni las etiquetas: son puntos de retorno.
4. Actualizad vuestra entrada en `CURRENT-TASKS.md` §3.bis con el resultado, y anotad en
   `research/rag/WORKLOG.md`.

**Antes de fusionar, traed `main`**: entre tanto habrá avanzado, y una fusión con `main` desactualizado es
como se pierden cosas.

## 6. Lo que sigue esperando decisión del autor, y no os bloquea

**§2.bis.1, los ejemplares contaminados.** El autor decidió **esperar a vuestra re-corrida**: no publicaremos
cifras descontadas a mano, las tomaremos de vuestras corridas limpias. Cablead el manifiesto de exclusión y
adelante.

**§3.1, el idioma del generador N=30.** Escalado con vuestra evidencia, sigue abierto. No bloquea la
re-corrida del corpus principal.
