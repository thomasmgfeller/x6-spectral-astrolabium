"""Render archived results; never runs or selects new simulations."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'results/summary.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,3,figsize=(14.5,4.8),layout='constrained')
fig.suptitle('RSS bei fester Punktzahl: Vorhersage, Näherung und Messrauschen',fontsize=16,fontweight='bold')
p=data['importance'][0]; b=np.array(data['rss_de_sitter_slopes']); y=np.array(p['mean'])/b
ci=np.array(p['interval99_family'])/b[:,None]
ax=axes[0];ax.axhspan(.95,1.05,color='#e5edf3');ax.axhline(1,color='#64748b',lw=1)
ax.errorbar([2,3,4],y,yerr=[y-ci[:,0],ci[:,1]-y],fmt='o',color='#0e7490',capsize=6,lw=2)
ax.set(xticks=[2,3,4],xlabel='Kettenlänge k',ylabel='Geschätzter / vorhergesagter Koeffizient',ylim=(.88,1.11))
ax.set_title('Gemeinsames ±5%-Ziel nicht erreicht',fontsize=11,fontweight='bold')
ax.text(.03,.03,'8.192 Wolken, N=128\n99%-Familienintervalle (approximativ)',transform=ax.transAxes,fontsize=9)
rows=[r for r in data['quadrature'] if r['h']>0]
ax=axes[1];ax.loglog([r['R_tau_squared'] for r in rows],[100*r['relative_remainder_of_curvature_signal'] for r in rows],'o-',color='#0e7490')
ax.axhline(5,color='#be123c',linestyle='--',label='5%-Grenze')
ax.set(xlabel='Krümmungsparameter RT²',ylabel='Näherungsfehler / Krümmungssignal (%)',ylim=(.00001,15))
ax.set_title('Zweierketten: gute Vorhersage im Gitter',fontsize=11,fontweight='bold');ax.legend(loc='lower right',fontsize=9)
ax.text(.03,.76,'Nur diese de-Sitter-Familie und C₂;\nkeine allgemeine Gültigkeitsgrenze.',transform=ax.transAxes,fontsize=9)
rows=[r for r in data['direct'] if r['N']==128 and r['h']>0]
xx=np.arange(len(rows));ax=axes[2]
ax.bar(xx-.18,[r['inverse']['target'][0] for r in rows],.36,label='Wahres RT²',color='#0e7490')
ax.bar(xx+.18,[r['inverse']['single_order_RMSE'][0] for r in rows],.36,label='RMSE des Schätzers',color='#c05a35')
ax.set(yscale='log',xticks=xx,xticklabels=[str(r['h']) for r in rows],xlabel='de-Sitter-Parameter h',ylabel='RT² bzw. absoluter Schätzfehler')
ax.set_title('Einzelne Ordnungen: sehr große Fehler',fontsize=11,fontweight='bold')
ax.legend(fontsize=9,loc='upper left');ax.set_ylim(.04,1800)
fig.supxlabel('Öffentlich fixierter Vertrag · 24.576 unabhängige Wolken · kein qualifizierter Krümmungssensor',fontsize=10)
for ext in ['png','svg']:
    fig.savefig(HERE/('results-overview.'+ext),dpi=170,metadata={'Creator':'X6 RSS fixed-N archived results'})
