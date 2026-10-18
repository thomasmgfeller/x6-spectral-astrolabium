"""Plot frozen outputs; decisions use exact fractions, not these display floats."""
import io
from fractions import Fraction as Q
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from support import read
from exact import q_bounds

HERE = Path(__file__).resolve().parent
math = read(HERE/'results/mathematics.json')
fig, axes = plt.subplots(1, 2, figsize=(11.7, 4.8), layout='constrained')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
h = [float(Q(r['h'])) for r in math['probability_grid']]
p = [sum(x['approximate'] for x in r['enclosure'])/2 for r in math['probability_grid']]
a = axes[0]
a.plot(h, p, color='#166a75', lw=2)
a.set(xlabel='Modellparameter h', ylabel='Paarwahrscheinlichkeit p(h)',
      title='Geometrische Umkehrung abgesichert\nMonotonie auf dem gesamten Bereich')
a.text(.03, .1030, 'Einschliessungsbreite ≤ 1,674 · 10⁻¹⁴', fontsize=9)
a.ticklabel_format(axis='y', style='plain', useOffset=False)
a.grid(alpha=.18)
b = axes[1]
for j in range(4):
    d = read(HERE/f'results/groups-{j}.json.gz')
    interval = list(map(Q, d['groups'][-1]['h_interval']))
    lo, hi = float(q_bounds(interval[0])[0]), float(q_bounds(interval[1])[1])
    true = float(q_bounds(Q(d['h']))[0])
    b.plot([lo, hi], [j, j], color='#6b818c', lw=6, solid_capstyle='round')
    b.scatter([true], [j], color='#a64b32', s=48, zorder=3,
              label='Wahrer Modellwert' if j == 0 else None)
b.set(yticks=np.arange(4), yticklabels=['h=0', 'h=0,1', 'h=0,25', 'h=0,5'],
      xlabel='Dimensionslose Krümmung q = R T²', xlim=(-.1, 3.45), ylim=(-.65, 3.7),
      title='Statistische Intervalle bleiben breit\nJe 4.096 Wolken · 128 Punkte pro Wolke')
b.text(1.6, 3.45, 'Keine 20%-Präzisionsfreigabe', ha='center', color='#a64b32', fontsize=10)
b.legend(loc='lower right', fontsize=9)
b.grid(axis='x', alpha=.18)
fig.suptitle('Zweierketten: kontrollierte Geometrie, konservative Überdeckung', fontsize=14, weight='bold')
fig.supxlabel('Mindestens 95% bei bekanntem uniformem Modell und festem Budget. Keine Garantie bei unbekannter Dichte oder freiem Stoppen.', fontsize=9)
for ext in ('png', 'svg'):
    buffer = io.BytesIO()
    fig.savefig(buffer, format=ext, dpi=170)
    (HERE/f'results-overview.{ext}').write_bytes(buffer.getvalue())
plt.close(fig)
