"""Plot only recorded forecasts and independently evolved late traces."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
r=json.loads((root/'results/verification.json').read_text())
f=json.loads((root/'forecast.json').read_text())['cases']['G07']
with (root/'results/late_traces.csv').open() as stream:traces=list(csv.DictReader(stream))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
t=np.linspace(1.3,2.6,350)
axes[0].plot(t,f['A']-2*f['J']*t+4*f['E']*t*t,color='#173643',lw=2,label='frühe Vorhersage')
for n,color,style in ((2048,'#aa5426','--'),(8192,'#08786f',':')):
 rows=[x for x in traces if x['case']=='G07' and int(x['N'])==n]
 axes[0].plot([float(x['T']) for x in rows],[float(x['V']) for x in rows],style,color=color,lw=2,label=f'Zeitentwicklung N={n}')
axes[0].plot(f['T_b'],f['V_b'],'x',color='black',ms=8)
axes[0].set(xlim=(1.3,2.6),ylim=(0,3.2),xlabel='Staubzeit T',ylabel=r'$\langle V\rangle$',title='Vorhersage und spätere Entwicklung: G07')
axes[0].legend(frameon=False,fontsize=8)
levels=(2048,4096,8192)
for key,label,color in (('relative_T_error','max. Zeitfehler','#245aa0'),('relative_V_error','max. Volumenfehler','#aa5426')):
 values=[100*max(x[key] for x in r['cases'] if x['N']==n) for n in levels]
 axes[1].plot([0,1,2],values,'o-',color=color,label=label)
axes[1].axhline(1,color='#245aa0',ls=':',lw=1)
axes[1].axhline(3,color='#aa5426',ls=':',lw=1)
axes[1].set(xticks=[0,1,2],xticklabels=['2048 / .005','4096 / .0025','8192 / .00125'],yscale='log',ylabel='maximaler relativer Fehler (%)',xlabel='Raumpunkte N / Zeitschritt',title='Fehlerabnahme über alle zehn Fälle')
axes[1].legend(frameon=False,fontsize=8)
for ax in axes:ax.grid(alpha=.2)
fig.savefig(root/'figures/prediction_test.pdf')
fig.savefig(root/'figures/prediction_test.png',dpi=180)
