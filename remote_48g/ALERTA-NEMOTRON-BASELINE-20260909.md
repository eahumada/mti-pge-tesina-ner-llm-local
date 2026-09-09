# Alerta — `nemotron-mini:4b` línea base: 18 registros perdidos por un fallo de código

**2026-09-09, 04:4x. Urgente, y afecta al consolidado que acabáis de publicar.**

## Qué pasa

La corrida `nemotron-mini_4b__N120` tiene **18 filas con `parse_method='failed'`**, y no están repartidas:
**las dieciocho están en `_baseline` y ninguna en `_kb_rag`**. Todas con latencia 0, cero tokens por segundo y
`retries=2`, es decir, agotaron los tres intentos.

La causa está en vuestro propio registro, `benchmark.log`:

```
Attempt 1/3 failed for model 'nemotron-mini:4b': 'list' object has no attribute 'items'   (x22)
Attempt 2/3 failed for model 'nemotron-mini:4b': 'list' object has no attribute 'items'   (x18)
Attempt 3/3 failed for model 'nemotron-mini:4b': 'list' object has no attribute 'items'   (x18)
```

**No es un rechazo de infraestructura: es un `TypeError` en `providers/ollama.py`.** El modelo devuelve una
lista donde el código espera un diccionario y llama a `.items()` sobre ella. Veintidós registros lo
encontraron en el primer intento y cuatro se recuperaron; dieciocho agotaron los tres.

## Por qué importa, y por qué es urgente

Esas dieciocho filas **puntúan 0,00 y entran en la media**. El efecto sobre el modelo que sostiene el mayor
resultado del estudio es este:

| | Con las fallidas | Sin ellas |
|:---|---:|---:|
| `nemotron-mini:4b_baseline` | **26,31** | **30,97** |
| `nemotron-mini:4b_kb_rag` | 40,55 | 40,55 |
| **Δ del RAG** | **+14,23 pp** | **+9,72 pp** |

Es decir: **un tercio de la mejora que se le atribuye a la recuperación en este modelo no es mejora, es la
línea base hundida por un fallo de software**. Y como las fallidas están todas en un solo brazo, el sesgo va
íntegro en la misma dirección.

**El consolidado `ANALISIS_CONJUNTO_20260909` que habéis publicado incluye 17 de esas 18 filas** —la
decimoctava es uno de los ejemplares contaminados y ya se excluía—. La cifra de F = 121,56 y todo lo que
cuelgue de ella arrastran el defecto.

## Lo que sí se sostiene

Comprobado con el post-hoc pareado, para que no cunda la alarma más de lo debido: **`nemotron-mini` sigue
siendo significativo en los dos escenarios** —Holm ≈ 0 con las fallidas y 0,0016 sin ellas— y sigue siendo el
mayor efecto del estudio. **La conclusión no cambia; la magnitud sí**, y en una cifra que el informe publica.

## Lo que pedimos

1. **Re-ejecutar `nemotron-mini:4b` en modo baseline sobre N=120**, o al menos sobre los dieciocho artículos
   afectados, después de arreglar el `TypeError`.
2. **Arreglar el fallo antes de repetir**, porque volverá a darse: no es aleatorio, lo dispara la forma de la
   respuesta del modelo. **Localizado**: `src/llm_runner.py`, línea **167**, dentro de la función que
   normaliza las claves a `Persons` / `Organizations` / `Locations`:

   ```python
   for k, v in parsed.items():      # <-- revienta si `parsed` es una lista
   ```

   La función da por hecho que el modelo devuelve un **objeto** JSON. Si devuelve un **array** en el nivel
   superior —`[{...}]`, o una lista de entidades sueltas— `parsed` es una `list` y `.items()` lanza
   exactamente el `TypeError` del registro.

   **Y explica por qué solo falla la línea base.** En modo `kb_combined` el prompt lleva un ejemplar anotado
   que guía al modelo a devolver un objeto; sin él, `nemotron-mini:4b` se va al array en unos ciento
   ochenta artículos de cada mil. Por eso `_kb_rag` tiene cero fallos y `_baseline` dieciocho.

   Un arreglo mínimo sería envolver el caso: si `parsed` es una lista y todos sus elementos son
   diccionarios, fusionarlos antes de normalizar; si es una lista de otra cosa, registrarlo como respuesta
   con formato inesperado en lugar de perder el registro entero. **No lo hemos tocado**: es vuestro código y
   cambiarlo altera cómo se mide, de modo que la decisión es vuestra.
3. **Rehacer el consolidado después**, no antes.
4. **Comprobar antes de declarar una corrida válida que `parse_method='failed'` vale cero.** El commit de
   cierre dice «39/39 válidas» y esta corrida tenía un 15 % de fallos en un brazo. Es la primera verificación
   del protocolo y habría bastado con ella.

**No hace falta rehacer nada más.** Los otros doce modelos están verificados y limpios: cero `failed` en las
2 730 filas restantes.
