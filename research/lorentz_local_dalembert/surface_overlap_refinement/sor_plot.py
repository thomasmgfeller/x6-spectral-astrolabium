"""Combined exact cover, highlighting the final 31 overlap exclusions.
SPDX-License-Identifier: Apache-2.0
"""
from sor_common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle,Patch

def plot():
    ar=read(HERE/'certificates.json.gz');rows=combined(ar);s=read(HERE/'summary.json')
    assert s['status']=='TWO_PARAMETER_SQUARE_EXCLUDED' and not s['unresolved_cells']
    phases={r['path']:stage for stage in ('missing','refined') for r in ar[stage]}
    colors={'TRANSFERRED_LAW_EXCLUDED':'#27648b','ORDER_EXCLUDED':'#d3dbe0','GAP_EXCLUDED':'#72b7a1','MARGINAL_TAIL_EXCLUDED':'#58a6ce','OVERLAP_TAIL_EXCLUDED':'#b097ba','missing':'#8464b1','refined':'#592777'}
    labels={'TRANSFERRED_LAW_EXCLUDED':'Transported count tests (480)','ORDER_EXCLUDED':'Order contradiction (302)','GAP_EXCLUDED':'Weight gap <=20% (450)','MARGINAL_TAIL_EXCLUDED':'Marginal Poisson tests (700)','OVERLAP_TAIL_EXCLUDED':'Earlier overlap tests (141)','missing':'New 64-slice overlap tests (16)','refined':'New 512-slice refinement (15)'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig=plt.figure(figsize=(12,8.8));ax=fig.add_axes([.08,.28,.43,.58]);zoom=fig.add_axes([.62,.28,.26,.58])
    for target in (ax,zoom):
        patches=[];fc=[];ec=[]
        for r in rows:
            a,d,e,f=map(lambda x:float(F(x)),r['box']);patches.append(Rectangle((a,e),d-a,f-e))
            fc.append(colors[phases.get(r['path'],r['status'])]);ec.append('#301647' if target==zoom and r['path'] in phases else 'none')
        target.add_collection(PatchCollection(patches,facecolors=fc,edgecolors=ec,linewidths=.5,antialiased=False))
        target.set(xlabel='Node 15 displacement u',ylabel='Node 17 displacement v',aspect='equal');target.grid(alpha=.15,lw=.5)
    ax.set(xlim=(-.1,.1),ylim=(-.1,.1),title='Complete square: 2,104 certified rectangles')
    ax.set_xticks([-.1,-.05,0,.05,.1]);ax.set_yticks([-.1,-.05,0,.05,.1])
    zoom.set(xlim=(-.048,-.031),ylim=(-.002,.032),title='Final 31 rectangles: all excluded')
    zoom.set_xticks([-.045,-.04,-.035]);zoom.set_yticks([0,.01,.02,.03])
    fig.suptitle('The independent two-support square is closed',x=.08,ha='left',fontsize=20,fontweight='bold',y=.97)
    fig.text(.08,.90,'100% of the declared parameter square covered; no HOLD rectangle remains.\nSmallest new TV lower bound: 0.2593315 > 0.25. This bound applies to the final 31 rectangles.',fontsize=11,color='#344857')
    handles=[Patch(facecolor=colors[k],label=labels[k]) for k in colors]
    fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.07,.12),ncol=3,frameon=False,fontsize=9)
    fig.text(.08,.045,'Fixed reference, independent boosted-x displacements of nodes 15/17. Excluded conjunction:\nunchanged order + symmetric physical weight gap >20% + full conditional count/overlap-law TV <=0.25.\nArea is not probability. Other references and arbitrary multi-support motion remain open.',fontsize=9,color='#344857')
    fig.savefig(HERE/'coverage.png',dpi=180,facecolor='white');plt.close(fig)

if __name__=='__main__':plot()
