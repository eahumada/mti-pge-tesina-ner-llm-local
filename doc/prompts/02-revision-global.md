# Segunda pasada independiente, con seis lentes y un orquestador

El procedimiento que en septiembre de 2026 encontró los tres defectos que bloqueaban la entrega, después de
que tres rondas previas de revisión bibliográfica no los hubieran visto. Su valor está en la **independencia**:
a los auditores no se les dice qué encontró nadie antes.

## Prompt de lanzamiento

> Lanzar un workflow de revisión global del informe con seis auditores independientes y un orquestador que
> sintetice al final. A cada auditor hay que decirle explícitamente:
>
> «Esta es una segunda pasada independiente. Deliberadamente **no** se te dice qué encontró la primera. Tu
> valor está en mirar con ojos limpios: si repites sus conclusiones, las confirmas; si encuentras algo
> distinto, lo aportas; y si contradices algo que ella dio por bueno, eso es lo más valioso de todo. No
> busques confirmar nada: busca lo que falla.»
>
> Fuentes primarias en este orden de autoridad: el código, los datos —el CSV manda sobre cualquier resumen—,
> las normas institucionales y las reglas del proyecto en `CLAUDE.md`. Los auditores trabajan en **solo
> lectura**: reportan, no corrigen. Prohibido inventar datos, referencias o URLs. Cada hallazgo debe citar su
> evidencia: línea del documento, fichero y línea del código, o comando ejecutado.
>
> Al promediar desde JSON, usar `if x.get(k) is not None` y nunca `if x.get(k)`, porque `0.0` es falsy y
> descartaría las filas en cero, inflando la media.

## Las seis lentes

| Lente | Qué mira |
|:---|:---|
| **Bibliografía** | Que cada obra exista y que sostenga lo que se le atribuye |
| **Cifras** | Cada número del documento contra los CSV de resultados, incluida la consistencia aritmética |
| **Método** | Cada afirmación sobre algoritmos, métricas, umbrales y parámetros contra el código fuente |
| **Formato** | Extensión, límites del resumen, citas IEEE, leyendas, ausencia de emojis y de arte ASCII |
| **Profesor guía** | El documento leído con los criterios y reparos del director del trabajo |
| **Coherencia** | Contradicciones internas: dos secciones que digan cosas distintas del mismo hecho |

Conviene incluir en el esquema de salida una gravedad `correcto`, para que se vea qué se revisó y resultó
bien; sin eso no hay forma de distinguir «no lo mira» de «lo mira y está bien».

## Prompt del orquestador

> Cruzar los informes entre sí. Donde dos auditores digan cosas incompatibles sobre el mismo punto,
> **señalarlo explícitamente**: una discrepancia entre auditores es una señal y no un ruido, y hay que decidir
> cuál tiene razón o declarar que queda sin resolver. Descartar lo que no se sostenga: un hallazgo sin
> evidencia citada no es un hallazgo. Ordenar por gravedad real para la defensa, no por número de casos: un
> dato falso en una tabla pesa más que veinte imprecisiones de estilo. Para cada problema que sobreviva,
> indicar la acción concreta y quién debe ejecutarla. Y decir con claridad si el documento está listo para
> entregar o no, y qué falta exactamente.
>
> Verificar por cuenta propia los hallazgos graves que vengan de **una sola fuente**, porque son los que más
> fácilmente son falsos y los que más daño hacen si se aplican sin comprobar.

## Lo que este procedimiento encontró y las rondas anteriores no

- Una categoría de entidad que los prompts pedían y que **ningún corpus anotaba**, responsable del 65 % de los
  falsos positivos de todo el estudio.
- Dos corpus declarados en español que estaban **íntegramente en inglés**, sobre los que además se acreditaba
  el umbral de la hipótesis.
- Tres corridas del mismo experimento de las que el informe **citaba solo la más favorable**; sobre el corpus
  mayor el efecto era nulo con p = 0,9328.
- Un anexo cuya tabla **no se reproducía con ningún criterio** y cuya partición sumaba 119 de 120 artículos.
- Que los `.docx` y el PDF que se iban a entregar **no eran el documento corregido**.
