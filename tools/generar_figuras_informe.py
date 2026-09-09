#!/usr/bin/env python3
"""Genera las figuras del informe final a partir de las cifras ya publicadas en sus tablas.

Los valores no se recalculan desde los CSV: se toman de la Tabla 7 y de §4.4 del Markdown canónico,
de modo que figura y tabla no puedan divergir. Si una tabla cambia, hay que cambiar aquí también.
Salida en doc/figuras/ a 300 ppp, en escala de grises legible al imprimir.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SALIDA = 'doc/figuras'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.edgecolor': '#444444', 'axes.linewidth': 0.6,
                     'xtick.color': '#444444', 'ytick.color': '#444444'})

# Tabla 7: modelo, F1 baseline, F1 KB RAG, delta significativo
TABLA7 = [
    ('gemma4:31b-cloud',    62.38, 61.85, False),
    ('gemma4:31b-mlx',      59.25, 59.07, False),
    ('gemma4:12b-mlx',      56.18, 58.46, False),
    ('gemma4:latest',       55.91, 54.74, False),
    ('gpt-oss:20b',         52.39, 55.67, False),
    ('qwen2.5:14b',         50.22, 54.84, False),
    ('llama3.1:8b',         48.76, 50.75, False),
    ('qwen3:8b',            48.21, 51.46, False),
    ('gemma:latest',        44.00, 51.36, False),
    ('mistral-nemo:latest', 43.38, 45.76, False),
    ('llama3.2:latest',     36.11, 46.93, True),
    ('deepseek-r1:1.5b',    24.83, 23.94, False),
    ('nemotron-mini:4b',    22.59, 37.12, True),
]

GRIS, OSCURO, ACENTO = '#9a9a9a', '#1a1a1a', '#000000'


def figura_1():
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.1, 3.5),
                               gridspec_kw={'width_ratios': [1.35, 1]})

    # (a) desplazamiento de cada modelo entre baseline y KB RAG
    y = range(len(TABLA7))
    for i, (m, base, rag, sig) in enumerate(TABLA7):
        a.plot([base, rag], [i, i], color=ACENTO if sig else '#bbbbbb',
               lw=1.6 if sig else 1.0, zorder=1, solid_capstyle='round')
        a.scatter([base], [i], s=26, facecolor='white', edgecolor=OSCURO, lw=0.9, zorder=2)
        a.scatter([rag], [i], s=26, facecolor=ACENTO if sig else GRIS,
                  edgecolor=OSCURO, lw=0.6, zorder=3)
    a.set_yticks(list(y))
    a.set_yticklabels([m for m, *_ in TABLA7], fontsize=7.2,
                      fontweight=['normal', 'bold'][0])
    for t, (_, _, _, sig) in zip(a.get_yticklabels(), TABLA7):
        if sig:
            t.set_fontweight('bold')
    a.invert_yaxis()
    a.set_xlabel('F1 (%)', fontsize=8)
    a.set_xlim(18, 68)
    a.grid(axis='x', color='#e4e4e4', lw=0.6, zorder=0)
    a.set_axisbelow(True)
    for s in ('top', 'right', 'left'):
        a.spines[s].set_visible(False)
    a.tick_params(axis='y', length=0)
    a.set_title('(a) Desplazamiento del F1 al añadir la base\nde conocimientos, modelo a modelo',
                fontsize=8.4, pad=8, loc='left')
    a.scatter([], [], s=26, facecolor='white', edgecolor=OSCURO, lw=0.9, label='baseline')
    a.scatter([], [], s=26, facecolor=GRIS, edgecolor=OSCURO, lw=0.6, label='KB RAG')
    a.legend(loc='lower right', frameon=False, fontsize=7.2, handletextpad=0.4)

    # (b) la ganancia decrece con el desempeno de partida
    for m, base, rag, sig in TABLA7:
        d = rag - base
        b.scatter([base], [d], s=34, facecolor=ACENTO if sig else GRIS,
                  edgecolor=OSCURO, lw=0.6, zorder=3)
        if sig or abs(d) > 4:
            b.annotate(m, (base, d), textcoords='offset points', xytext=(5, 3),
                       fontsize=6.4, color='#333333')
    b.axhline(0, color='#888888', lw=0.7, ls=(0, (4, 3)), zorder=1)
    b.set_xlabel('F1 baseline (%)', fontsize=8)
    b.set_ylabel('Δ al añadir KB RAG (pp)', fontsize=8)
    b.grid(color='#e4e4e4', lw=0.6, zorder=0)
    b.set_axisbelow(True)
    for s in ('top', 'right'):
        b.spines[s].set_visible(False)
    b.set_title('(b) Tendencia, no significativa: la ganancia\ndecrece conforme mejor es el modelo de partida',
                fontsize=8.4, pad=8, loc='left')
    b.text(0.97, 0.95, 'ρ de Spearman = −0,5165\n(p = 0,0707)', transform=b.transAxes,
           ha='right', va='top', fontsize=7, color='#333333')

    fig.tight_layout()
    fig.savefig(f'{SALIDA}/efecto-kb-rag.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


def figura_2():
    """Composicion de los falsos positivos del estudio (§4.4)."""
    fig, ax = plt.subplots(figsize=(7.1, 1.5))
    # Cifras de results/COMPOSICION_FP_20260908/, sobre los 26 grupos que sostienen la Tabla 7.
    loc, total = 12852, 19464
    otros = total - loc
    ax.barh([0], [loc], color='#333333', edgecolor='none', height=0.55)
    ax.barh([0], [otros], left=[loc], color='#cccccc', edgecolor='none', height=0.55)
    ax.text(loc / 2, 0, f'localizaciones: {loc:,}'.replace(',', ' ') + '  (66,0 %)',
            ha='center', va='center', color='white', fontsize=8)
    ax.text(loc + otros / 2, 0, f'personas y organizaciones: {otros:,}'.replace(',', ' '),
            ha='center', va='center', color='#222222', fontsize=8)
    ax.set_xlim(0, total)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xlabel(f'falsos positivos en los 26 grupos que sostienen la Tabla 7 (N=120) '
                  f'(total {total:,})'.replace(',', ' '), fontsize=8)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis='x', labelsize=7)
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{int(v):,}'.replace(',', '\u2009')))
    fig.tight_layout()
    fig.savefig(f'{SALIDA}/falsos-positivos.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    figura_1()
    figura_2()
    print('figuras generadas en', SALIDA)
