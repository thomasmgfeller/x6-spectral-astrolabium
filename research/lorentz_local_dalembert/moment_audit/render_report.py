"""Render already-frozen analysis outputs; no new inference or fit."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent
s=json.loads((HERE/'results/summary.json').read_text())
primary=next(c for c in s['cells'] if c['rho']==32768)
names=['raw','T','S','TS','D','TD','SD','TSD']
fig,axes=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
colors=['#166b8f','#dc7a29']; labels=['Intrinsische Auswahl','Exakte Abstandskappe (Kontrolle)']
x=np.arange(8)
for i,(arm,label,color) in enumerate(zip(['balanced64','oracle_cap'],labels,colors)):
 a=primary['arms'][arm]
 axes[0].plot(x,[a['variants'][v]['rms'] for v in names],marker='o',color=color,label=label)
 axes[1].errorbar(np.arange(3)+i*.16-.08,[a['shapley'][f]['mean'] for f in ['T','S','D']],yerr=[a['shapley'][f]['se'] for f in ['T','S','D']],fmt='o',capsize=5,color=color)
axes[0].axhline(.5,color='#555',linestyle='--',linewidth=1,label='Bisherige Fehlergrenze 0,5')
axes[0].set_xticks(x,names);axes[0].set_ylabel('Relativer Metrik-RMS');axes[0].set_title('Alle acht festgelegten Kombinationen')
axes[0].legend(fontsize=8,loc='upper right');axes[0].grid(axis='y',alpha=.2)
axes[1].axhline(0,color='#555',linewidth=1);axes[1].set_xticks([0,1,2],['Zeitpunkte T','Schalen S','Richtungen D'])
axes[1].set_ylabel('Beitrag zur Reduktion des quadrierten Fehlers')
axes[1].set_title('Shapley-Zuordnung; Balken = 1 Standardfehler')
axes[1].grid(axis='y',alpha=.2)
fig.suptitle('BK-Momentendiagnose · Dichte 32768 · je 16 neue Wolken',fontsize=14)
fig.supxlabel('T: Eigenzeit der Zeitpunkte   S: Eigenzeit auf der Schale   D: gemeinsame Zeitrichtung\nAlle Eingriffe nutzen Simulationskoordinaten; Phase 3 bleibt HOLD.',fontsize=9)
fig.savefig(HERE/'comparison.png',dpi=160);plt.close(fig)
