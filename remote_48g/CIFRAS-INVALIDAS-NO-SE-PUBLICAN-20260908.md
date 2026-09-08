# Norma del autor: una medición inválida no es un resultado, y sus cifras no se publican

**Del autor, a través del equipo principal. 2026-09-08.** Afecta a cómo se reporta la re-corrida que vais
a lanzar. Leedlo antes de empezar.

## La decisión

El informe llegó a incluir una tabla que enfrentaba «corrida publicada» y «corrida sustituida» con las
cifras de las dos. Entre ellas, el **11,21 %** de `gemma4:12b-mlx` con KB RAG. El autor lo ha rechazado: esa
cifra **no es un resultado alternativo, es un resultado incorrecto**, y ponerla al lado de la buena sugiere
que hubo dos mediciones válidas y se escogió una.

Tiene razón, y el mecanismo lo respalda: en esa corrida el modelo **no llegó a responder** en 98 de los 120
artículos, con precisión y exhaustividad cayendo a cero **a la vez** —la firma de no contestar, no la de
equivocarse— y una latencia media de 967 s frente a los 158 s de la corrida válida. Eso no mide al modelo,
mide un arnés que gastaba el presupuesto de salida en el razonamiento.

## La norma, que rige desde ya

**De una medición inválida se declara que existió, por qué se descartó y con qué evidencia. Su F1 no se
publica.** La evidencia sí se publica, porque es lo que acredita la invalidez: cuántos artículos quedaron sin
extracción, la latencia y el modo de análisis de la respuesta.

**De una repetición válida se publican ambas cifras**, porque las dos miden lo mismo y el lector tiene
derecho a ver la dispersión.

Retiradas ya del informe las ocho cifras inválidas de los seis grupos afectados: `gemma4:12b-mlx` y
`qwen3:8b` por razonamiento activo, y `gpt-oss:20b` por presupuesto agotado. Se conservan las dos de
`nemotron-mini:4b`, que son una repetición válida.

## Qué implica para vuestra re-corrida

1. **No reportéis un F1 de una corrida que no superó la verificación.** Si un modelo sale con una fracción
   apreciable de artículos sin extracción, lo que se informa es el diagnóstico, no la métrica. Un número que
   no mide lo que dice medir contamina cualquier tabla en la que se ponga.
2. **El umbral práctico que hemos usado**: si precisión y exhaustividad caen a cero **a la vez** en más del
   15 % de los artículos, la corrida es sospechosa y hay que diagnosticar antes de dar cifras. Por debajo de
   ese orden y con la caída repartida en artículos cortos, suele ser comportamiento legítimo del modelo
   —artículos sin entidades—, no fallo del arnés.
3. **Distinguid las tres causas**, que se confunden y no son lo mismo:
   - latencia **0** y **0** tokens/s → rechazo de infraestructura (cuota, HTTP 429, servicio caído);
   - latencia **alta** con tokens fluyendo y respuesta vacía → el presupuesto de salida se consumió antes de
     emitir la respuesta (razonamiento activo o `max_tokens` corto);
   - latencia normal y respuesta malformada → el modelo contestó mal, y eso **sí** es un resultado.
4. **Los artefactos que atestiguan no se tocan.** Los CSV, los `benchmark.log` y los `run_config.json` de
   cualquier corrida descartada se conservan íntegros en `results/`. Son la prueba de la invalidez: sin
   ellos, la declaración del informe no sería verificable. Se corrige lo que afirma; se conserva lo que
   atestigua.

## Un aviso de lectura que nos costó un despiste hoy

Al listar las filas fallidas de una corrida usamos `valor or -1` y el volcado mostró «ausente» donde había un
**0,0**, que es *falsy*. Es la misma trampa que la cuarta verificación del protocolo advierte para el
promediado, y aparece igual al imprimir. **Comparad siempre contra `None`, nunca contra la veracidad del
valor**, en cualquier lectura de un número que pueda ser cero: latencia, tokens/s, precisión, exhaustividad.

## Lo que no cambia

El régimen de *thinking* del estudio **se mantiene tal cual**: `gpt-oss:20b` con razonamiento **activo** y
congelado, y los modelos de `_THINKING_DISABLED_MODELS` con él desactivado. Está decidido en `FINDINGS §F44`
y `§F45` sobre evidencia medida, y `§F45` desaconseja expresamente cambiarlo porque mezclaría dos regímenes
en el mismo estudio. No lo toquéis en la re-corrida.
