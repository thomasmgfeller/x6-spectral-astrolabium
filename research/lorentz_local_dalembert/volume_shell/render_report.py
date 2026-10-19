"""Plot frozen summary outputs; no fitting or additional inferential analysis."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
s=json.loads((HERE/'results/summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(11.5,4.5),layout='constrained')
for method,label,color,style in [('raw','Unveränderte Gewichte','#666666','-'),('volume_shell','Intervallgewichte Schale (primär)','#166b8f','-'),('volume_both','Schale + Zeitpunkte (sekundär)','#d27b26','--')]:
 for ax,key in zip(axes,['metric_rms','affine_drift_rms']):
  ax.plot([c['rho'] for c in s['cells']],[c['arms'][method][key] for c in s['cells']],marker='o',color=color,linestyle=style,label=label)
axes[0].axhline(.5,color='#999',linestyle=':',label='Bisherige Metrikgrenze 0,5')
axes[0].set_ylabel('Relativer Metrik-RMS');axes[0].set_title('Zweite Momente')
axes[1].set_ylabel('RMS von τm · ||B(t,x,y)|| / √3');axes[1].set_title('Drift auf linearen Testfeldern; Ziel = 0')
for ax in axes:
 ax.set_xscale('log',base=4);ax.set_xticks([2048,8192,32768],['2048','8192','32768']);ax.set_xlabel('Punktdichte ρ');ax.grid(axis='y',alpha=.2)
axes[0].legend(fontsize=8)
fig.suptitle('BK: intrinsische Schalenkalibrierung · 48 frische Wolken',fontsize=14)
fig.supxlabel('Gleiche Nachbarn und Referenzrichtungen. Fehler bedingt auf verfügbare Schablonen.\nVerbesserungskriterium ist keine flache Validierung; Phase 3 bleibt HOLD.',fontsize=9)
fig.savefig(HERE/'comparison.png',dpi=160);plt.close(fig)
