# Solicitud a GitHub Support: purga de objetos inalcanzables

**Para enviar en** https://support.github.com/contact — categoría *Repositories* / *Other*.
GitHub **no expone ninguna API** para forzar el recolector de basura; la única vía es esta solicitud.

## Estado verificado el 2026-09-08

| Comprobación | Resultado |
|:---|:---|
| Commit `bb79279` con autenticación | **HTTP 200**, y su `test_flash.py` contiene la clave en claro |
| Commit `bb79279` sin autenticar | HTTP 404 (el repositorio es privado) |
| *Forks* del repositorio | **0** |
| Red del repositorio (`network_count`) | **0** |
| Refs visibles tras la reescritura | limpios: 0 de 139 commits contienen la clave |

Los ceros en *forks* y red son la razón por la que la purga puede ser completa: no hay ningún repositorio
derivado que conserve los objetos.

## Texto para pegar en la solicitud

> Subject: Request garbage collection of unreachable objects after history rewrite
>
> Hello,
>
> I rewrote the history of my private repository `eahumada/mti-pge-tesina-ner-llm-local` using
> `git filter-repo` to remove a credential that had been committed, and force-pushed all branches and tags.
> The visible history is now clean: none of the 139 commits contains the credential.
>
> However, the pre-rewrite objects are still served. For example,
> `GET /repos/eahumada/mti-pge-tesina-ner-llm-local/contents/test_flash.py?ref=bb79279` returns HTTP 200 with
> the credential in plaintext. The repository has 0 forks and a network count of 0, so no fork network should
> be holding these objects.
>
> Could you please run garbage collection on this repository to permanently remove the unreachable objects?
> I intend to make the repository public afterwards, and I would rather not publish it while those objects
> remain retrievable by SHA.
>
> Thank you.

## Verificación posterior, obligatoria antes de publicar

Cuando GitHub confirme la purga, comprobar que el objeto ha desaparecido:

```sh
. ./.setenv.sh
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/eahumada/mti-pge-tesina-ner-llm-local/contents/test_flash.py?ref=bb79279"
```

Debe devolver **404**. Mientras devuelva 200, **no hacer público el repositorio**: publicarlo convertiría una
clave recuperable-si-conoces-el-SHA en una clave indexable por cualquier rastreador.

## Decisión del autor registrada

El autor decide **no revocar la clave** sobre la base de que queda limpia del historial. Queda constancia de
que esa premisa es cierta para los refs visibles y **no lo es todavía** para los objetos que GitHub sirve,
razón por la cual la purga pasa a ser condición necesaria para la publicación y no una medida
complementaria. Ver `SEGURIDAD-CLAVE-GOOGLE-20260908.md` y `LEARNING.md §L43`.
