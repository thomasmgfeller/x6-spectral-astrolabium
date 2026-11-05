"""Create the report figure from the recorded verification output."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
r=json.loads((root/'results/verification.json').read_text())
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
t=np.linspace(0,.5,200)
for mass,color in zip((.25,1,4),('#08786f','#245aa0','#aa5426')):
    axs[0].plot(t,4-2*np.sqrt(mass)*t,label=f'M = {mass:g}',color=color,lw=2)
    rows=[x for x in r['semiclassical'] if x['M_central']==mass and x['N']==2048 and x['hbar']==.02]
    axs[0].scatter([x['T'] for x in rows],[x['q_mean'] for x in rows],color=color,s=20,zorder=3)
axs[0].set(xlabel='Staubzeit T',ylabel=r'$q=\sqrt{V}$',title='Reduzierte Referenz: Massenantwort')
axs[0].legend(frameon=False)
axs[0].text(.03,.06,'Linien: klassisch; Punkte: Quantenkern\nκ = 1, zentrale Masse M, ℏ = 0,02',transform=axs[0].transAxes,fontsize=8)
c=r['old_volume_carrier'];ts=c['T_singularity']
t=np.linspace(0,ts,250)
axs[1].plot(t,1+c['initial_slope']*t,color='#173643',lw=2,label='klassisch aus frühen Werten')
tt=np.arange(5)*.4
qq=(np.array([5,4,3,2,1])/5)**1.5
axs[1].plot(tt,qq,'o--',color='#aa5426',label='Beispiel aus altem Träger')
axs[1].axvline(ts,color='#53636b',ls=':',label=f'Singularität T = {ts:.3f}')
axs[1].axvspan(ts,1.6,color='#f4e4dd')
axs[1].set(xlim=(0,1.62),ylim=(0,1.05),xlabel='Staubzeit T',ylabel=r'$q=\sqrt{V}$',title='Zeitfenster des bisherigen Katalogs')
axs[1].legend(frameon=False,fontsize=8,loc='upper right')
for ax in axs: ax.grid(alpha=.18)
fig.savefig(root/'figures/classical_checks.pdf')
fig.savefig(root/'figures/classical_checks.png',dpi=180)
