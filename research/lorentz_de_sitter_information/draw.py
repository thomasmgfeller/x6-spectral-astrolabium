"""Render the fixed result tables; no scientific refitting."""
import io
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
s = json.loads((HERE/'results/summary.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.6), layout='constrained')
primary = s['primary']
ratio = primary['rmse_ratio']
lo, hi = primary['paired_percentile_bootstrap_approx95']
a = axes[0]
a.errorbar([ratio], [0], xerr=[[ratio-lo], [hi-ratio]], fmt='o', color='#166a75', capsize=6)
a.axvline(.9, color='#a64b32', ls='--', label='Vorabziel: obere Grenze ≤ 0,90')
a.axvline(1, color='#8b9094', lw=1)
a.set(xlim=(.88, 1.01), ylim=(-.7, .7), yticks=[], xlabel='RMSE-Verhältnis GLS234 / C2',
      title='Nur 1,37% weniger Schätzfehler\nN=128, h=0,5 · frischer Test')
a.text(.945, .4, '10%-Ziel verfehlt', ha='center', color='#a64b32', weight='bold')
a.text(.945, -.34, 'Gepaarter Bootstrap · approximative 95%', ha='center', fontsize=9)
a.legend(loc='lower left', fontsize=8)
b = axes[1]
x = np.arange(3)
for off, method, color in ((-.17, 'C2', '#6b818c'), (.17, 'GLS234', '#166a75')):
    rows = [r for r in s['rows'] if r['method'] == method and r['h'] > 0]
    vals = [r['budget_relative_20pct'] for r in rows]
    b.bar(x+off, vals, width=.32, label=method, color=color)
b.set(yscale='log', ylim=(1000, 8e6), xticks=x, xticklabels=['0,1', '0,25', '0,5'],
      xlabel='Modellparameter h', ylabel='Unabhängige Wolken zu je 128 Ereignissen',
      title='Schwache Krümmung bleibt datenhungrig\n20%-Halbbreite · nominell 95%')
b.grid(axis='y', alpha=.18)
b.legend()
fig.suptitle('De-Sitter-Informationsplanung: 16.384 neue Punktwolken', fontsize=14, weight='bold')
fig.supxlabel('Budget = Normalapproximation für Zufallsstreuung. Keine garantierte Überdeckung; Modellfehler bleiben offen.', fontsize=9)
for ext in ('png', 'svg'):
    buffer = io.BytesIO()
    fig.savefig(buffer, format=ext, dpi=170)
    (HERE/f'results-overview.{ext}').write_bytes(buffer.getvalue())
plt.close(fig)
