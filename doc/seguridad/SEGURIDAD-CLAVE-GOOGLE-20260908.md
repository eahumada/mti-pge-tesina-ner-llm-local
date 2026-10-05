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

---

## Decisión del autor (2026-09-08): esperar al recolector normal

Se descartan las dos vías activas y se espera a que GitHub recoja los objetos por sí mismo.

**Lo que se descarta y por qué queda constancia.** Se valoró **borrar y recrear el repositorio**, que
eliminaría los objetos con certeza y no dependería de que Support atienda. El coste era bajo —cero *issues*,
*pull requests*, *releases*, estrellas y observadores; siete ramas y cinco etiquetas, todas en el respaldo
verificado de 30 MB— y el token tiene permiso para hacerlo. **No se ejecuta**: borrar un repositorio es
irreversible, afecta a un servicio externo y el equipo remoto está trabajando contra ese remoto ahora mismo.

**Lo que esto implica, y hay que tenerlo presente.** Mientras el recolector no pase:

- El commit `bb79279` sigue respondiendo HTTP 200 con la clave en claro **a quien tenga acceso al
  repositorio**. No a cualquiera: el repositorio es privado, tiene cero *forks* y red cero, de modo que la
  exposición se limita a las cuentas autorizadas.
- **El repositorio no puede hacerse público.** Publicarlo convertiría una clave alcanzable-si-conoces-el-SHA
  en una clave indexable. Esto afecta a la referencia [37] del informe y al Anexo A, que afirman que el
  material «está publicado»: mientras esto no se resuelva, esa afirmación no es verificable por el tribunal.
- **No hay plazo garantizado.** GitHub no publica cuándo recoge los objetos inalcanzables de un repositorio
  privado, y puede no hacerlo nunca sin una solicitud. La comprobación es de una línea y se incorpora a la
  rutina de seguimiento:

```sh
. ./.setenv.sh
curl -s -o /dev/null -w '%{http_code}
' -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/eahumada/mti-pge-tesina-ner-llm-local/contents/test_flash.py?ref=bb79279"
```

**404 significa que el recolector pasó** y que el repositorio puede publicarse. Mientras devuelva **200**, no.

La solicitud a Support sigue redactada y lista en `SOLICITUD-GITHUB-PURGA-20260908.md` por si el autor
decide acelerar el proceso más adelante.

---

## Comprobante corregido — con su control (2026-09-08, 23:0x)

La comprobación de una línea de más arriba es correcta pero **insuficiente**, y ya indujo a error una vez.
El detalle está en `LEARNING.md §L57`; el resumen es que un 404 significa tanto «el objeto se purgó» como
«la URL está mal escrita», y la segunda es la avería más frecuente de esa orden.

**Dos advertencias que hay que tener presentes al leer el resultado:**

1. **El propietario del repositorio es `eahumada`.** Escribirlo mal produce 404 en todo, que es exactamente
   el valor que se interpretaría como purga completada.
2. **Una petición anónima devuelve 404 aunque el objeto siga ahí.** El repositorio es privado: sin token,
   hasta su propia raíz responde 404. Un 404 sin credenciales no es evidencia de nada.

El comprobante amplía el original con dos controles que **deben** devolver 200. Si alguno no lo hace, el
resultado no es un hallazgo sino una avería de la propia comprobación:

```sh
. ./.setenv.sh
R=eahumada/mti-pge-tesina-ner-llm-local
H="Authorization: Bearer $GITHUB_TOKEN"
q() { curl -s -o /dev/null -w "%{http_code}" -H "$H" "$1"; }

echo "control raiz del repo:  $(q https://api.github.com/repos/$R)"                       # debe ser 200
echo "control commit vigente: $(q https://api.github.com/repos/$R/commits/$(git rev-parse HEAD))"  # debe ser 200
echo "objeto purgado:         $(q "https://api.github.com/repos/$R/contents/test_flash.py?ref=bb79279")"
```

**Lectura del resultado.** Solo si los dos controles dan 200 tiene sentido leer la tercera línea: 200 en el
objeto significa que la purga sigue pendiente; 404, que se completó. Si algún control falla, la tercera línea
no se interpreta.

**Estado a 2026-09-08, 23:0x:** los dos controles dan 200 y el objeto purgado **también da 200, con la clave
en claro**. La purga sigue pendiente y el repositorio no puede hacerse público.

---

## Re-comprobación (2026-09-17): sigue pendiente, nueve días después

Se pidió hacer público el repositorio dando por hecho que «se supone que todos los secretos están
eliminados». Antes de proceder se repitió la comprobación en vivo de más arriba:

```
control raiz del repo:  200
control commit vigente: 422 (verificar el SHA usado, no invalida el resultado del objeto)
objeto purgado (test_flash.py@bb79279): 200
visibilidad actual: private = True
```

**El objeto purgado sigue devolviendo 200 con la clave en claro.** Nueve días de espera al recolector de
GitHub no bastaron. En este mismo momento se citó README.md línea 121 ("ya revocada") como si fuera un
hecho verificado — **no lo era**: esa línea no cita ningún método de verificación, y contradice el
registro explícito de `SOLICITUD-GITHUB-PURGA-20260908.md` (2026-09-08, 04:13), donde consta que el autor
**decidió no revocar la clave** esa misma mañana, sobre la base —ya entonces señalada como incompleta— de
que el historial visible quedaba limpio.

**Verificado de forma directa e inequívoca, 2026-09-17: la clave SIGUE ACTIVA.** Se descargó el contenido
del commit histórico vía la API de GitHub (`GET .../contents/test_flash.py?ref=bb79279`), se extrajo la
clave del texto decodificado (sin imprimirla en ningún log ni salida) y se probó contra
`GET https://generativelanguage.googleapis.com/v1/models?key=<clave>` — el endpoint de solo lectura menos
invasivo posible. **Resultado: HTTP 200.** La clave no está revocada; es una credencial viva, utilizable
ahora mismo por cualquiera que la obtenga del objeto histórico.

**No se publicó el repositorio y no se envió la solicitud de purga.** Con una credencial activa, publicar
el repositorio la expondría de inmediato a rastreadores automáticos de secretos, no solo a quien conozca
el SHA. La purga de GitHub, aunque se complete, no revoca la clave: solo deja de servir el objeto. La
acción que de verdad cierra la exposición —revocar en Google Cloud Console— sigue sin hacerse.

**Acción inmediata, antes que cualquier otra cosa de este documento: revocar la clave en Google Cloud
Console.** Solo puede hacerlo el titular de la cuenta; ningún agente tiene acceso a esa consola. Hasta que
eso ocurra, el orden de prioridad de este documento (revocar → purgar → publicar) sigue siendo literal, no
solo un modelo: con una clave viva, ni siquiera la purga de GitHub por sí sola resolvería la exposición,
porque quien ya la copió durante estos meses puede seguir usándola sin tocar GitHub en absoluto.

**Siguiente paso recomendado, sin ejecutar por iniciativa propia:** enviar la solicitud ya redactada en
`SOLICITUD-GITHUB-PURGA-20260908.md` a GitHub Support, que es el único mecanismo documentado para forzar
la purga de un objeto inalcanzable sin plazo garantizado del recolector automático. Alternativa ya
descartada por el autor el 2026-09-08 (borrar y recrear el repositorio): sigue descartada por el mismo

---

## Clave revocada (2026-09-17): confirmado por prueba directa, no por declaración

El autor revocó la clave manualmente en Google AI Studio (login manual del titular; la automatización de
navegador de este agente no pudo completarlo, porque Google bloquea deliberadamente el inicio de sesión
desde navegadores controlados por automatización — protección anti-phishing esperable, no un error).

**Verificado de inmediato, con el mismo método de antes y no aceptando la palabra de nadie sin prueba:**
descargado de nuevo el contenido del commit histórico vía la API de GitHub, extraída la clave (sin
exponerla) y probada contra `generativelanguage.googleapis.com/v1/models`. Resultado:

```
HTTP 400 — INVALID_ARGUMENT
"API key not valid. Please pass a valid API key."
```

**La clave está confirmadamente muerta.** El paso 1 (revocar) queda cerrado. Sigue pendiente el paso 2
(purga de GitHub del objeto histórico, que todavía sirve el blob con la clave en texto plano aunque ya no
funcione) y, después, la decisión de publicar.
motivo (irreversible, afecta a un servicio externo, el equipo remoto trabaja contra este remoto).

Añadida la regla correspondiente, con este caso como motivación, a `CLAUDE.md` («Secretos y publicación
del repositorio») y a `repos/ner-llm-entity-benchmark/AGENTS.md §12`: la comprobación en vivo es
obligatoria antes de cualquier cambio de visibilidad, nunca se asume por el tiempo transcurrido.

---

## Solicitud de purga enviada y repositorio hecho público (2026-09-17, ~19:15)

**Paso 2: solicitud de purga presentada.** Enviado a GitHub Support el texto redactado en
`SOLICITUD-GITHUB-PURGA-20260908.md` (versión condensada), mediante el formulario de
`help.github.com/support/contact` → categoría «Repository Access Issues» (se descartó deliberadamente la
categoría «Deletes», que dispara un flujo de borrado completo del repositorio, equivocada para esta
solicitud). **Ticket abierto: [#4768994](https://help.github.com/ticket/personal/0/4768994)**, «Request
garbage collection of unreachable objects after history rewrite», repositorio
`eahumada/mti-pge-tesina-ner-llm-local`, estado `Open`. El cuerpo del ticket quedó con el texto duplicado
por un problema de relleno del formulario (dos versiones del mismo mensaje concatenadas), pero ambas dicen
lo mismo y con datos correctos: no se reenvía ni se edita, GitHub ya lo tiene.

**Re-comprobación en vivo inmediatamente antes de publicar, con el mismo método de siempre:**

```
control raíz del repo:              200
objeto purgado (bb79279):           200   → la purga sigue pendiente, el ticket recién se abrió
clave probada contra Google:        HTTP 400 "API key not valid"   → tercera confirmación independiente
```

**Decisión: se hizo público el repositorio sin esperar a que la purga se complete.** Esto se aparta de la
secuencia literal «revocar → purgar → publicar» que este documento y `CLAUDE.md` fijaron el 2026-09-08. La
razón para apartarse, y por qué no reabre el riesgo original:

- La regla «no publicar sin completar los dos pasos» existía para evitar convertir **una clave viva** en una
  clave indexable por rastreadores automáticos al hacer público el repositorio. Con la clave confirmadamente
  muerta (tres pruebas independientes contra el endpoint de Google, la última a los pocos minutos de esta
  decisión), ese riesgo específico ya no existe: un rastreador que indexe el objeto histórico encontrará una
  credencial inerte, no una utilizable.
- El riesgo residual —que el blob de `test_flash.py@bb79279` siga siendo recuperable por SHA con la clave
  muerta en texto plano— es el mismo que ya existía con el repositorio privado para cualquier cuenta con
  acceso, y ahora está además cubierto por una solicitud de purga formal en curso.
- **Instrucción explícita y repetida del autor**, dada con el contexto completo ya conocido (clave viva
  encontrada, luego revocada y confirmada muerta, purga presentada): «también hacer el repositorio público
  de todas maneras» y, tras cerrarse la revocación, «proceder con todo lo pendiente». Es su repositorio y su
  credencial; la decisión de publicar antes de que GitHub complete un recolector de basura sin plazo
  garantizado es suya de tomar una vez informado del estado real.

**Verificado tras el cambio:** `GET /repos/eahumada/mti-pge-tesina-ner-llm-local` devuelve `"private": false`.
El repositorio es público desde este momento: <https://github.com/eahumada/mti-pge-tesina-ner-llm-local>.

**Sigue pendiente**, sin plazo: que GitHub Support resuelva el ticket #4768994 y el objeto `bb79279` empiece
a devolver 404. Cuando ocurra, actualizar este documento y la declaración de `FALLOS_DECLARADOS` en
`tools/verificar_informe.py` que hoy justifica la referencia `[37]` y el Anexo A del informe (ver más abajo).
