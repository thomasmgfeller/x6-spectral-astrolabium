"""Descriptive plots from all archived results; no research rerun or refitting."""
import json
import io
from pathlib import Path
import zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent
with zipfile.ZipFile(HERE/'results.zip') as z:
    rows=json.loads(z.read('grid.json'))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.titleweight':'bold'})
fig,axes=plt.subplots(2,2,figsize=(12,8.3),layout='constrained')
fig.suptitle('Eigenzeit v0.2 · Modellannahmen bestimmen die Aussagekraft',fontsize=17,fontweight='bold')
colors=['#176d8c','#b06116','#854e9d','#ba3541']
models=[('uniform_flat',0.,'Uniform, flach'),('de_sitter',.5,'de Sitter h=0,5'),
        ('density',4.,'Dichte β=4'),('thinning',.5,'Innen nur 50 % erfasst')]
def select(model,param,interval='nominal'):
    return [r for r in rows if r['d']==4 and r['model']==model and r['parameter']==param
            and r['planning_theta']==.2 and r['interval']==interval]
for color,(model,param,label) in zip(colors,models):
    rr=select(model,param)
    xx=[r['m'] for r in rr]
    axes[0,0].plot(xx,[100*r['coverage'] for r in rr],marker='o',ms=4,label=label,color=color)
    axes[0,1].plot(xx,[100*r['false_precision_probability'] for r in rr],marker='o',ms=4,label=label,color=color)
for ax in axes[0]:
    ax.set_xscale('log',base=4); ax.set_xlabel('Beobachtete Punkte m'); ax.set_ylim(-3,103)
    ax.grid(alpha=.16); ax.set_ylabel('Wahrscheinlichkeit (%)')
axes[0,0].axhline(95,ls='--',lw=1,color='#59616a'); axes[0,0].set_title('A · Überdeckung nomineller 95%-Intervalle')
axes[0,0].legend(fontsize=8,loc='lower left')
axes[0,1].set_title('B · Falsche Meldung „≤10 % relativer Fehler“')
axes[0,1].text(.03,.94,'4D · wahres τ/T=0,2 · feste Budgets',transform=axes[0,1].transAxes,va='top',fontsize=9)

for color,name,label in zip(['#176d8c','#59813c','#b06116'],['nominal','bounded_mild','bounded_broad'],
                            ['r=1 bekannt','r ∈ [0,8; 1,25]','r ∈ [0,5; 2]']):
    rr=select('uniform_flat',0.,name)
    axes[1,0].plot([r['m'] for r in rr],[100*r['precision_probability'] for r in rr],marker='o',color=color,label=label)
axes[1,0].axhline(90,ls='--',lw=1,color='#59616a'); axes[1,0].set_xscale('log',base=4)
axes[1,0].set_ylim(-3,103); axes[1,0].set_ylabel('Präzision verfügbar (%)'); axes[1,0].set_xlabel('Beobachtete Punkte m')
axes[1,0].set_title('C · Begrenzte Dichteunsicherheit\nkostet Präzision',fontsize=12)
axes[1,0].legend(fontsize=8); axes[1,0].grid(alpha=.16)

ax=axes[1,1]
theta=[.1,.2,.4,.7]; intervals=['nominal','bounded_mild','bounded_broad']
for j,(name,label,color) in enumerate(zip(intervals,['r=1','r ∈ [0,8; 1,25]','r ∈ [0,5; 2]'],['#176d8c','#59813c','#b06116'])):
    vals=[next(r['asymptotic_interval_relative_radius'] for r in rows if r['model']=='uniform_flat' and r['d']==4 and r['theta']==t and r['interval']==name) for t in theta]
    ax.plot(theta,100*np.array(vals),marker='o',label=label,color=color)
ax.axhline(10,ls='--',lw=1,color='#59616a'); ax.set_ylim(-.5,20)
ax.set_title('D · Verbleibender Intervallradius\nbei unendlich vielen Punkten',fontsize=12)
ax.set_xlabel('Wahre normierte Eigenzeit τ/T'); ax.set_ylabel('Relativer Radius (%)'); ax.legend(fontsize=8); ax.grid(alpha=.16)
for extension in ['png','svg']:
    buffer=io.BytesIO()
    fig.savefig(buffer,format=extension,dpi=170)
    target=HERE/('results-overview.'+extension)
    target.write_bytes(buffer.getvalue())
print('Plots rendered from archived results; fixed 4D examples, complete grid in results.zip')
