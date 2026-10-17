"""Post-run descriptive figure only; never changes the frozen estimators."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent

def main():
    data=[json.loads(line) for line in (HERE/'results/records.jsonl').read_text().splitlines()]
    summary=json.loads((HERE/'results/summary.json').read_text())
    fig,axes=plt.subplots(1,2,figsize=(11,4.3),gridspec_kw={'width_ratios':[1.2,1]})
    colors={'0.75':'#2e728f','1.0':'#153f2b','1.25':'#ad6132'}
    for key,color in colors.items():
        groups=[[r for r in data if r['n']==n] for n in [256,512,1024,2048]]
        x=[np.mean([.5*np.log(r['n_a']) for r in group]) for group in groups]
        y=[[r['diagnostics']['cutoffs'][key]['double']['entropy_nats'] for r in group] for group in groups]
        axes[0].errorbar(x,[np.mean(g) for g in y],yerr=[np.std(g,ddof=1)/np.sqrt(len(g)) for g in y],
                         fmt='o-',color=color,capsize=3,label='κ = '+key)
        fit=summary['fits'][key]
        ci=fit['ci95']; position=list(colors).index(key)
        axes[1].errorbar(fit['primary_slope'],position,xerr=[[fit['primary_slope']-ci[0]],[ci[1]-fit['primary_slope']]],
                         fmt='o',color=color,capsize=4)
    axes[0].set(xlabel='ln √N_A (Gruppenmittel)',ylabel='Entropie S_A [nats]',title='Doppelte Regularisierung')
    axes[0].legend(frameon=False)
    band=summary['reference_band']
    axes[1].axvspan(*band,color='#dce8e1',label='Vorab festgelegte Toleranz')
    axes[1].axvline(1/3,color='#49685a',linestyle='--',linewidth=1)
    axes[1].set(yticks=[0,1,2],yticklabels=['κ = 0.75','κ = 1.0 (primär)','κ = 1.25'],xlabel='Steigung gegen ln √N_A',title='Hauptfit: N = 512–2048')
    for ax in axes:
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='x',alpha=.15)
    fig.suptitle('Freies Gaußfeld auf festen kausalen Mengen',fontsize=14,fontweight='bold')
    fig.text(.02,.012,'64 neue Ordnungen. Links: Mittelwert ± 1 Standardfehler. Rechts: 95%-Bootstrap-Intervalle; keine Physikvalidierung.',fontsize=8)
    fig.tight_layout(rect=[0,.05,1,.96])
    fig.savefig(HERE/'results/scaling.svg',metadata={'Date':None})
    fig.savefig('/tmp/x6-free-field-scaling.png',dpi=160)
    plt.close(fig)
    svg=HERE/'results/scaling.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')

if __name__=='__main__':
    main()
