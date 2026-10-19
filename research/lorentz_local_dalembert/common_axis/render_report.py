"""Display the frozen analysis without changing its data, gates or estimators."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent

def plot():
    s=json.loads((HERE/'results/summary.json').read_text())
    colors={'raw':'#9b9b9b','volume_shell':'#23476b','axis_shell':'#bb572f','oracle_axis_shell':'#468365'}
    labels={'raw':'Original weights','volume_shell':'Volume weights (baseline)','axis_shell':'Intrinsic common axis','oracle_axis_shell':'Exact-time axis (diagnostic)'}
    fig,axes=plt.subplots(1,3,figsize=(12,4.6));fig.patch.set_facecolor('white')
    for key in colors:
        xs=[c['rho'] for c in s['cells']]
        values=[[c['arms'][key]['metric_rms'] for c in s['cells']],
                [c['arms'][key]['affine_drift_rms'] for c in s['cells']],
                [c['arms'][key]['reference_quality']['mean_rapidity']['mean'] for c in s['cells']]]
        for ax,ys in zip(axes,values):
            ax.plot(xs,ys,'o-',color=colors[key],label=labels[key],lw=1.6,ms=5)
    axes[0].axhline(.5,color='#444444',ls=':',lw=1)
    for ax,title in zip(axes,['Relative metric RMS','Normalized affine drift RMS','Mean reference rapidity']):
        ax.set_title(title,fontsize=11);ax.set_xscale('log',base=4)
        ax.set_xticks(xs,[str(x) for x in xs]);ax.set_xlabel('Density');ax.set_ylim(bottom=0)
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
    axes[0].set_ylabel('Error');axes[2].set_ylabel('Rapidity')
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2,fontsize=9,bbox_to_anchor=(.5,.04))
    fig.suptitle('Common-axis trial · 48 fresh clouds · Phase 3 remains on hold',fontsize=13,y=.98)
    fig.text(.5,.015,'RMS and rapidities use available clouds; denominators and paired gates are reported in RESULTS.md.',ha='center',fontsize=8,color='#555555')
    fig.tight_layout(rect=[0,.19,1,.94]);fig.savefig(HERE/'comparison.png',dpi=160);plt.close(fig)

if __name__=='__main__':plot()
