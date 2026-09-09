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

Y lo hemos acotado más, para que no haya dudas sobre el alcance:

- Los **datos publicados** del estudio no están afectados: el consolidado de septiembre 7 tiene **cero**
  `failed` en sus 3 120 filas.
- El mensaje aparece **58 veces y todas en `nemotron-mini_4b__N120`**. Es el **único error repetido de las
  treinta y nueve corridas**; los demás registros están limpios.
- Las corridas de **N=30 y N=15 del mismo modelo** tampoco fallan, lo que encaja con la explicación: el
  fallo aparece en torno al 15 % de los artículos y esas muestras son pequeñas.

**El remedio es un brazo, de un modelo, de un corpus**: ciento veinte artículos de inferencia.

---

## Refinamiento del 2026-09-10: los 7 registros perdidos no son uniformes

Aplicado el criterio 5 del protocolo de monitorización a `nemotron-mini:4b_baseline` en
`nemotron_rerun_n120_REMOTO`, con el cruce completo de `latencia`, `tokens_per_sec`, `parse_method` y
`recall`:

| Señal | Valor | Lectura |
|:---|---:|:---|
| Registros con latencia 0 | **7** | coincide exactamente con los 7 de §F85 |
| De esos, con 0 tokens/s | **7** | **rechazo de infraestructura**, no pérdida del arnés |
| Registros con `parse_method='fallback'` | **7** | son los mismos 7 |
| De esos, con `recall > 0` | **4** | el *fallback* **sí** rescató contenido |
| De esos, con `recall = 0` | **3** | el *fallback* **encubre** un fallo |

**Lo que esto cambia para el encargo.** La pérdida no son 7 registros en blanco: son **3 de pérdida
total** y **4 de rescate parcial**. El F1 de 22,59 % está deprimido por las dos cosas, y por tanto la
re-corrida no solo recuperará los 3 perdidos sino que **cambiará también los 4 rescatados**, cuyo contenido
salió del camino de excepción y no del normal.

Conviene tenerlo presente al comparar: la mejora que la re-corrida produzca **no** será atribuible solo a los
registros que faltaban.

**Y el contraste con `mistral-nemo`, que confirma el veredicto de §3.bis.7.** Su mitad `kb_rag` tiene **69 de
120 en `fallback`**, más de la mitad, y a primera vista alarma. Pero **cero registros con latencia 0** —no hay
rechazo de infraestructura— y **68 de los 69 rescatan contenido**, con `recall > 0`. El *fallback* ahí
funciona como vía alternativa de parseo, no como tapadera. **Benigno, confirmado con la evidencia del
criterio 5** y no solo por inspección de los logs.


---

## CORRECCIÓN del 2026-09-10: el refinamiento de arriba estaba mal

El apartado anterior afirmaba que los siete registros con latencia 0 son «rechazo de infraestructura» y que
son «los mismos 7» que están en `fallback`, con «3 de pérdida total». **Las tres cosas son falsas** y quedan
retiradas. Lo correcto:

| Grupo | Cuántas | `parse_method` | Con `recall > 0` | Qué es |
|:---|---:|:---|---:|:---|
| Latencia 0 y 0 tokens | 7 | `direct_json` | **6 de 7** | **telemetría ausente**, no rechazo |
| `parse_method = fallback` | 7 | `fallback` | 4 de 7 | el arnés usó la vía alterna |

**Son conjuntos disjuntos: 14 registros distintos, no 7.**

Y las siete de latencia 0 **no son un fallo pendiente**: el informe ya las declara en la salvedad de
procedencia de §5.3.1 —«se re-extrajeron fuera del arnés de lotes tras un fallo de contexto; sus valores de
precisión, *recall* y F1 son reales, pero su telemetría no existe»—. Se aplicó la regla del criterio 5 sin
comprobar su premisa, que exige que **no haya contenido**.

**Lo que esto cambia para el encargo §3.bis.15.** Menos de lo que decía el apartado anterior: el defecto de
`llm_runner.py:167` que motiva la re-corrida sigue en pie tal como lo describe `FINDINGS §F85`, pero **no hay
siete registros rechazados que recuperar**. Lo que hay es siete filas cuya telemetría no existe —y que por
tanto no deben usarse en comparaciones de latencia ni de tokens/s, cosa que el informe ya advierte— y siete
más, distintas, que pasaron por el camino de excepción del parseo.

Ver `FINDINGS §F108.bis`. Disculpas por el ruido: el apartado anterior se deja a la vista, tachado por este,
porque retirarlo escondería que el error se cometió.


---

## Qué esperar de la re-corrida — 2026-09-10

Un dato para que el resultado no sorprenda. `nemotron-mini:4b` es el **único** de los trece modelos cuyo
delta con recuperación **baja** al aislar las filas de parseo alterno, porque **sus siete están en la línea
base** y la deprimen:

| | Δ publicado | Δ aislando el parseo alterno |
|:---|---:|---:|
| `nemotron-mini:4b` | +14,5249 | **+14,0491** |

Es decir: al arreglar el `TypeError` y recuperar esas filas, la línea base **sube** y por tanto la mejora que
la recuperación aporta **baja**. Previsiblemente el **+14,52 pp** que el informe publica se reducirá hacia el
entorno del **+14,05**.

**Eso no invalida nada** —sigue siendo, con holgura, el mayor efecto del estudio y uno de los dos
significativos según Tukey— pero conviene saberlo antes de comparar, para no leer un descenso como un
problema de la re-corrida.
