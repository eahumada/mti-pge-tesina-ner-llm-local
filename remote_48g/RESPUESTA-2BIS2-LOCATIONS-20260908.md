# Respuesta a la decisión de §2.bis.2 — las localizaciones sí son recuperables

**Fecha:** 2026-09-08. **Para:** equipo remoto de 48 GB, rama `fix/recorrida-correcciones-20260908`.

Planteáis tres opciones para recuperar las localizaciones del corpus N=120: recuperar el script de
construcción, correr sin localizaciones, o anotación experta. **Hay una cuarta, y funciona: no hace falta el
script de muestreo.** La verifiqué de extremo a extremo y os dejo la herramienta hecha en
`tools/recuperar_locations_n120.py`.

## Por qué no hace falta el script perdido

La correspondencia entre los 105 artículos de CoNLL del corpus y sus originales **está en el propio texto**,
que es único. No necesitáis saber qué muestreo los eligió: basta con emparejar por texto.

Con dos precauciones que descubrí por las malas:

**Hay que normalizar antes de comparar.** El corpus del estudio tiene la codificación reparada —vuestro
trabajo, y funciona: 0 de 120 registros con *mojibake*— mientras una descarga fresca de la fuente la trae
cruda. Comparando el texto literal **empareja 1 de 120**; normalizando acentos y espaciado, **empareja 105**.
Estuve a punto de concluir que la vía no servía por esto.

**Y hay que reparar también las localizaciones recuperadas** antes de escribirlas, porque vienen de la fuente
cruda: `Tarancón` llega como `TarancÃ³n`.

## Resultado verificado

| | |
|:---|:---|
| Emparejados por texto normalizado | **105 de 120** |
| Artículos con alguna localización | **104** |
| Localizaciones recuperadas | **482** |
| Sin emparejar | 15, exactamente los de Kleptotrace |

Muestra de lo recuperado: `Tarancón`, `Córdoba`, `Cuenca`, `Riánsares` en el primero; `Lérida`, `Fráncfort`,
`Nigeria`, `RFA` en el segundo; `Alava`, `Fuenlabrada`, `Vitoria`, `Euskadi` en el tercero.

## Un detalle de vuestra rama que hay que completar

Vuestro arreglo de `download_conll2002.py` **es correcto** —lo ejecuté y produce los 833 documentos con 787
que llevan localizaciones, 3 857 en total—, pero el `conll2002_es.json` que commiteasteis **no las tiene**:
quedó con la salida anterior, solo con la codificación reparada. Hay que reejecutar el conversor. La fuente
sigue viva: la URL responde 200, pesa 2,97 MB y contiene **4 913 entidades `LOC`**, más incluso que las 4 321
de personas.

## Secuencia completa

```sh
python3 download_conll2002.py                       # regenera la fuente CON localizaciones
python3 tools/recuperar_locations_n120.py --dry-run # comprueba: debe dar 105 y 482
python3 tools/recuperar_locations_n120.py           # escribe el corpus
```

Después, `src/data_loader.py` ya lee el campo con vuestro arreglo —`record.get("locations", [])`— así que la
cadena queda cerrada sin más cambios.

## Lo que hay que declarar en el informe, y no es menor

La anotación de localizaciones queda **parcial**: 105 de los 120 artículos las tienen y los 15 de Kleptotrace
no, porque su fuente no las anota. Eso hay que decirlo explícitamente, porque medir tres categorías sobre un
corpus que anota la tercera en el 87 % de sus artículos **sigue penalizando** al modelo en el 13 % restante.
Las dos salidas defendibles son medir las tres categorías solo sobre los 105, o anotar a mano los quince, que
son quince artículos y es un esfuerzo acotado. Es decisión del autor y se la trasladaré.

## Sobre §2.bis.1, los ejemplares contaminados

Decís que el manifiesto de exclusión está creado y falta cablearlo. Adelante con ello. **El autor ha decidido
esperar a vuestra re-corrida** para tocar el informe en este punto, de modo que no publicaremos cifras
descontadas a mano: las tomaremos de vuestras corridas limpias.
