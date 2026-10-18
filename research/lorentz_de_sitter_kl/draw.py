"""Render exact archived decisions; display floats do not determine acceptance."""
import io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from support import read

HERE = Path(__file__).resolve().parent
planning = read(HERE/'results/planning.json')
fresh = read(HERE/'results/groups-3.json.gz')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, (a, b) = plt.subplots(1, 2, figsize=(12.6, 5.6), layout='constrained')
colors = {'Hoeffding':'#73818c', 'KL':'#087e83'}
y = np.arange(3)
for method, offset in [('Hoeffding', -.17), ('KL', .17)]:
    values = [r['sufficient_clouds'] for r in planning['rows'] if r['method'] == method]
    a.barh(y+offset, values, height=.29, color=colors[method], label=method)
    for yi, value in zip(y+offset, values):
        a.text(value*1.12, yi, f'{value:,}'.replace(',', '.'), va='center', fontsize=9)
a.set(xscale='log', xlim=(1e4, 9e8), yticks=y, yticklabels=['h = 0,1', 'h = 0,25', 'h = 0,5'],
      xlabel='Hinreichendes Budget: Wolken à 128 Punkte (log)',
      title='2,71–2,77× weniger Wolken\nVerfeinerte Grenzen, keine optimalen Minima')
a.invert_yaxis(); a.legend(loc='lower right', frameon=False)
a.grid(axis='x', alpha=.17); a.set_axisbelow(True)
groups = [g for g in fresh['groups'] if g['group_size'] == 16384]
for method, offset in [('Hoeffding', -.12), ('KL', .12)]:
    for j, group in enumerate(groups):
        lo, hi = [q['approximate'] for q in group['intervals'][method]['q']]
        b.plot([lo, hi], [j+offset, j+offset], color=colors[method], lw=5, solid_capstyle='round')
        radius=group['intervals'][method]['radius']['approximate']
        b.text(hi+.035, j+offset, f'{100*radius:.2f}%'.replace('.', ','), va='center', fontsize=9,
               color=colors[method])
b.axvline(3.1313138147509614, color='#b54c31', ls=':', lw=1.4)
b.set(yticks=np.arange(4), yticklabels=['Gruppe 1', 'Gruppe 2', 'Gruppe 3', 'Gruppe 4'],
      xlim=(1.8, 3.58), ylim=(-.5, 3.5), xlabel='Dimensionslose Krümmung q = R T²',
      title='20%-Präzision: KL 4/4, Hoeffding 1/4\nh = 0,5 · je 16.384 frische Wolken')
b.invert_yaxis(); b.grid(axis='x', alpha=.17)
b.text(.99, .01, 'Beschriftung: relativer Radius', transform=b.transAxes,
       ha='right', va='bottom', fontsize=8)
fig.suptitle('Eigenzeit: schärfere C2-Intervalle, gleiche endliche Absicherung', fontsize=15, weight='bold')
fig.supxlabel('≥95% bei bekanntem uniformem Modell und festem Budget. Vier Gruppen liefern keine präzise Erfolgsrate.\nDie vorab feste obere Modellgrenze hilft bei h=0,5; keine Garantie bei unbekannter Dichte oder freiem Stoppen.', fontsize=9)
for ext in ('png', 'svg'):
    buffer=io.BytesIO(); fig.savefig(buffer, format=ext, dpi=170)
    (HERE/f'results-overview.{ext}').write_bytes(buffer.getvalue())
plt.close(fig)
