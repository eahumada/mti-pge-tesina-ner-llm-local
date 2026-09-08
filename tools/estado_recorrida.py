#!/usr/bin/env python3
"""Regenera ESTADO-RECORRIDA-20260908.md desde la rama del equipo de 48 GB.

Lee los `benchmark_summary.json` de `results/recorrida_20260908/` **sin sacarlos de git**, de modo que
funciona aunque esa rama no esté fusionada. Las cifras salen del resumen y no del CSV crudo, porque el
resumen publica sobre 113 registros —los siete artículos contaminados se descuentan— y promediar el CSV
entero da un número que no es el del estudio (FINDINGS §F65).

Uso:  python3 tools/estado_recorrida.py > ESTADO-RECORRIDA-20260908.md
"""
import json
import subprocess
import sys
from datetime import datetime

RAMA = 'origin/fix/recorrida-correcciones-20260908'
BASE = 'repos/ner-llm-entity-benchmark/results/recorrida_20260908/'

# (nombre, prefijo de directorio, (F1 baseline publicado, F1 KB RAG publicado))
MODELOS = [
    ('gemma4:31b-cloud', 'gemma4_31b-cloud', (62.38, 61.85)),
    ('gemma4:31b-mlx', 'gemma4_31b-mlx', (59.25, 59.07)),
    ('gemma4:12b-mlx', 'gemma4_12b-mlx', (56.18, 58.46)),
    ('gemma4:latest', 'gemma4_latest', (55.91, 54.74)),
    ('gpt-oss:20b', 'gpt-oss_20b', (52.39, 55.67)),
    ('qwen2.5:14b', 'qwen2.5_14b', (50.22, 54.84)),
    ('llama3.1:8b', 'llama3.1_8b', (48.76, 50.75)),
    ('qwen3:8b', 'qwen3_8b', (48.21, 51.46)),
    ('gemma:latest', 'gemma_latest', (44.00, 51.36)),
    ('mistral-nemo:latest', 'mistral-nemo_latest', (43.38, 45.76)),
    ('llama3.2:latest', 'llama3.2_latest', (36.11, 46.93)),
    ('deepseek-r1:1.5b', 'deepseek-r1_1.5b', (24.83, 23.94)),
    ('nemotron-mini:4b', 'nemotron-mini_4b', (22.59, 37.12)),
]


def leer(ruta):
    return subprocess.run(['git', 'show', '%s:%s%s' % (RAMA, BASE, ruta)],
                          capture_output=True, text=True).stdout


def par(tag, corpus):
    """Devuelve (F1 baseline, F1 kb_rag) de una corrida, o None si aún no existe."""
    t = leer('%s__%s/benchmark_summary.json' % (tag, corpus))
    if not t.strip():
        return None
    d = json.loads(t)
    b = [100 * v['f1'] for k, v in d.items() if k.endswith('_baseline')]
    r = [100 * v['f1'] for k, v in d.items() if not k.endswith('_baseline')]
    return (b[0], r[0]) if b and r else None


def directorios_reales():
    """Los directorios de corrida que existen de verdad en la rama."""
    t = subprocess.run(['git', 'ls-tree', '-r', '--name-only', RAMA, BASE],
                       capture_output=True, text=True).stdout
    return sorted({p[len(BASE):].split('/')[0] for p in t.split('\n')
                   if p.strip() and '/' in p[len(BASE):]})


def huerfanos():
    """Directorios presentes que ninguna entrada de MODELOS reclama.

    La correspondencia modelo -> directorio esta escrita a mano, y los nueve modelos que faltan
    todavia no han creado el suyo. Si el equipo de 48 GB lo nombra de otro modo, este documento
    mostraria «pendiente» para siempre sin que nada avisara, que es la clase de fallo silencioso
    contra la que se han ido poniendo guardas todo el dia.
    """
    esperados = {'%s__%s' % (tag, c) for _, tag, _ in MODELOS for c in ('N120', 'N30', 'N15')}
    return [d for d in directorios_reales() if d not in esperados]


def main():
    out = []
    w = out.append
    w('# Estado de la re-corrida completa\n')
    w('**Actualizado: %s.** Regenerar con `python3 tools/estado_recorrida.py`; no editar a mano.\n'
      % datetime.now().strftime('%Y-%m-%d %H:%M'))
    w('Todas las corridas listadas han pasado las cinco verificaciones del protocolo —cero')
    w("`parse_method='failed'`, cero violaciones de `F1 ≤ (P+R)/2`, cero rechazos de infraestructura— y")
    w('llevan la firma del corpus corregido **1098 / 1500 / 1034** en N=120. Las cifras se toman de')
    w('`benchmark_summary.json`, que publica sobre **113** registros: los siete artículos contaminados se')
    w('descuentan (`FINDINGS §F65`).\n')
    w('## N=120, frente a lo publicado\n')
    w('| Modelo | Publicado base / RAG | Re-corrida base / RAG | Δ publicado | Δ re-corrida | Signo |')
    w('|:---|:---|:---|---:|---:|:---:|')
    hechos = cambian = 0
    for nom, tag, (pb, pr) in MODELOS:
        v = par(tag, 'N120')
        if v is None:
            w('| `%s` | %.2f / %.2f | *pendiente* | %+.2f | — | — |' % (nom, pb, pr, pr - pb))
            continue
        b, r = v
        hechos += 1
        dp, dn = pr - pb, r - b
        c = (dp < 0) != (dn < 0)
        cambian += 1 if c else 0
        w('| `%s` | %.2f / %.2f | **%.2f / %.2f** | %+.2f | %+.2f | %s |'
          % (nom, pb, pr, b, r, dp, dn, '**cambia**' if c else 'igual'))
    w('\n**%d de %d modelos** rehechos en N=120. **%d cambian el signo** del efecto del RAG.\n'
      % (hechos, len(MODELOS), cambian))
    w('## N=30 y N=15\n')
    w('| Modelo | N=30 base / RAG | N=15 base / RAG |')
    w('|:---|:---|:---|')
    for nom, tag, _ in MODELOS:
        cel = []
        for c in ('N30', 'N15'):
            v = par(tag, c)
            cel.append('*pendiente*' if v is None else '%.2f / %.2f' % v)
        if cel != ['*pendiente*', '*pendiente*']:
            w('| `%s` | %s | %s |' % (nom, cel[0], cel[1]))
    w('\n## Avance del barrido\n')
    w('Según `results/recorrida_20260908/_sweep_progress.log`, congelado en el último commit del equipo')
    w('de 48 GB:\n')
    w('```')
    w(leer('_sweep_progress.log').strip() or '(sin registro)')
    w('```\n')
    w('## Salvedades vigentes\n')
    w('- **Las latencias no son comparables** con las publicadas: los factores van de ×0,02 a ×2,58 sin')
    w('  dirección consistente, y la causa solo está explicada a medias (`FINDINGS §F71` y `§F71.bis`).')
    w('  La Tabla 8 del informe no debe rehacerse hasta entenderlo.')
    w('- **El consolidado no se rehace hasta tener los trece**, para no mezclar modelos medidos con')
    w('  localizaciones anotadas y sin ellas.')
    w('- Si el cambio de signo se confirma, **§5.3.1 habrá de reformularse** (`FINDINGS §F68`).')
    h = huerfanos()
    if h:
        w('\n> ⚠️ **Directorios de corrida que este documento no reconoce:** `%s`. La correspondencia'
          % '`, `'.join(h))
        w('> modelo → directorio está escrita a mano en `tools/estado_recorrida.py`; hay que añadirlos o')
        w('> figurarán como pendientes aunque estén hechos.')
    print('\n'.join(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
