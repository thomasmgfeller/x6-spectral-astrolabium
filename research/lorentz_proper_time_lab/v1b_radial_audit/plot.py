#!/usr/bin/env python3
"""Exact-data scientific figure; no smoothing or selected repetitions."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from diagnose import HERE, load_trace

def main():
    out=HERE/'results';control=out/'control'
    historical=load_trace(out/'historical_d4.bin.gz')
    x=np.linspace(0,1,2001)
    def residual(a):return np.searchsorted(np.sort(a),x,side='right')/len(a)-x
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(1,2,figsize=(12,4.6))
    colors=['#9566b5','#5488b4','#71a17d','#ce8c45']
    for i,(seed,col) in enumerate(zip([0,1,20261017,4294967295],colors)):
        a=historical['u'][i*16384:(i+1)*16384]/2**32
        ax[0].plot(x,residual(a),color=col,alpha=.8,lw=.9,label=f'Seed {seed}')
    ax[0].plot(x,residual(historical['u']/2**32),color='#172d45',lw=2,label='Zusammen, n = 65.536')
    ax[0].set_title('Historischer Befund — vor der Geometrie')
    for arm,color,label in [('mulberry32','#116c89','Mulberry32, p = 0,266'),('philox32','#ad5a27','Philox32, p = 0,757')]:
        summary=json.loads((control/f'{arm}_trace.json').read_text())
        vals=np.concatenate([load_trace(control/g['file'])['w'] for g in summary['groups']])
        ax[1].plot(x,residual(vals),color=color,lw=1.6,label=label)
    ax[1].set_title('Vorab festgelegter Kontrolllauf\nje Generator n = 2.097.152')
    for a in ax:
        a.axhline(0,color='#80909e',lw=.7);a.grid(alpha=.18);a.set_xlabel('Radiale Volumenvariable W');a.set_ylabel('Empirische CDF − W');a.legend(fontsize=9,loc='lower left')
    fig.suptitle('Radiale 4D-Diagnose: derselbe native Sampler, neue feste Zufallsfolgen',fontweight='bold',fontsize=14)
    fig.text(.5,.015,'Unterschiedliche y-Skalen. Alle Stichproben enthalten. Kurven auf festem Raster; KS-Statistik aus sämtlichen Werten.',ha='center',fontsize=9,color='#435565')
    fig.tight_layout(rect=(0,.04,1,.94));fig.savefig(out/'radial_diagnosis.png',dpi=180);fig.savefig(out/'radial_diagnosis.pdf')
if __name__=='__main__':main()
