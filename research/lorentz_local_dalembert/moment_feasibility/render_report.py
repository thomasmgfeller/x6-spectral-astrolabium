"""Plot frozen feasibility/mass summaries without treating fitted error as evidence."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
HERE=Path(__file__).resolve().parent

def plot():
    s=json.loads((HERE/'results/summary.json').read_text());cell=s['cells'][-1]
    policies=['fixed_time','free_time','unrestricted'];labels=['Fixed temporal','Free temporal','Any signs']
    fig,axes=plt.subplots(1,3,figsize=(12,4.6));colors={'caps':'#23476b','full_shells':'#bd663f'}
    for family,offset in [('caps',-.18),('full_shells',.18)]:
        data=cell['supports'][family]['policies'];x=np.arange(3)+offset
        means=[data[p]['mass_ratio']['mean'] or 0 for p in policies]
        errors=[data[p]['mass_ratio']['se'] or 0 for p in policies]
        axes[2].bar(x,means,yerr=errors,width=.34,color=colors[family],capsize=3)
    line_colors=['#23476b','#bd663f','#428066']
    for ax,family in zip(axes[:2],['caps','full_shells']):
        for policy,label,color in zip(policies,labels,line_colors):
            xs=[c['rho'] for c in s['cells']]
            ax.plot(xs,[c['supports'][family]['policies'][policy]['counts']['FEASIBLE'] for c in s['cells']],
                    'o-',color=color,label=label,lw=1.6,ms=5)
        ax.set_xscale('log',base=4);ax.set_xticks(xs,[str(x) for x in xs],fontsize=9)
        ax.set_ylim(0,17.5);ax.set_yticks([0,4,8,12,16]);ax.set_xlabel('Density');ax.set_ylabel('Feasible clouds out of 16')
    for ax,title in zip(axes,['Selected caps: feasibility','Full shells: feasibility','Density 32768: minimum mass']):
        ax.set_title(title,fontsize=11);ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True)
    axes[2].set_xticks(np.arange(3),labels,fontsize=9,rotation=15)
    axes[2].axhline(1,color='#666666',ls=':',lw=1);axes[2].set_ylabel('Mass / baseline; error bars = cloud SE')
    axes[2].legend(handles=[plt.Rectangle((0,0),1,1,color=colors[k]) for k in colors],
                   labels=['Selected caps','Full shells'],fontsize=8,loc='upper right')
    fig.suptitle('Joint moments · 48 fresh clouds · coordinate-assisted diagnosis only',fontsize=13,y=.98)
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,ncol=3,loc='lower center',bbox_to_anchor=(.5,.045),fontsize=10)
    fig.text(.5,.015,'Fitted moments are constraints, not validation. Mass means use feasible cases; all counts retain the 16-cloud denominator.',ha='center',fontsize=8,color='#555555')
    fig.tight_layout(rect=[0,.16,1,.94]);fig.savefig(HERE/'comparison.png',dpi=160);plt.close(fig)

if __name__=='__main__':plot()
