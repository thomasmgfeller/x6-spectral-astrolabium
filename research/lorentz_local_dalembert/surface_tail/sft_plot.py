"""Exact-status map and zoom of the remaining 31 inherited HOLD rectangles.
SPDX-License-Identifier: Apache-2.0
"""
from sft_common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle,Patch

def plot():
    rows=combined(read(HERE/'certificates.json.gz'));s=read(HERE/'summary.json')
    colors={'TRANSFERRED_LAW_EXCLUDED':'#27648b','ORDER_EXCLUDED':'#d3dbe0','GAP_EXCLUDED':'#72b7a1','MARGINAL_TAIL_EXCLUDED':'#58a6ce','OVERLAP_TAIL_EXCLUDED':'#92539c','HOLD':'#e9a23b'}
    labels={'TRANSFERRED_LAW_EXCLUDED':'Transported count tests','ORDER_EXCLUDED':'Order contradiction','GAP_EXCLUDED':'Weight gap <=20%','MARGINAL_TAIL_EXCLUDED':'Marginal Poisson tests','OVERLAP_TAIL_EXCLUDED':'Overlap difference tests','HOLD':'HOLD / unresolved rectangle'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig=plt.figure(figsize=(12,8.2));ax=fig.add_axes([.08,.22,.43,.63]);zoom=fig.add_axes([.62,.22,.26,.63])
    slope=-float(F('292553733423/500000000000'))
    for target in (ax,zoom):
        patches=[];fc=[];ec=[]
        for r in rows:
            a,d,e,f=map(lambda x:float(F(x)),r['box']);patches.append(Rectangle((a,e),d-a,f-e));fc.append(colors[r['status']]);ec.append('#94651f' if target==zoom and r['status']=='HOLD' else 'none')
        target.add_collection(PatchCollection(patches,facecolors=fc,edgecolors=ec,linewidths=.45,antialiased=False))
        target.plot([-.1,.1],[-.1*slope,.1*slope],color='#172c3c',ls='--',lw=1.2)
        target.set(xlabel='Node 15 displacement u',ylabel='Node 17 displacement v',aspect='equal')
        target.grid(alpha=.15,lw=.5)
    ax.set(xlim=(-.1,.1),ylim=(-.1,.1),title='Complete declared square');ax.set_xticks([-.1,-.05,0,.05,.1]);ax.set_yticks([-.1,-.05,0,.05,.1])
    zoom.set(xlim=(-.048,-.031),ylim=(-.002,.032),title='Remaining region: 31 HOLD cells');zoom.set_xticks([-.045,-.04,-.035]);zoom.set_yticks([0,.01,.02,.03])
    fig.suptitle('744 additional rectangles excluded',x=.08,ha='left',fontsize=20,fontweight='bold',y=.97)
    fig.text(.08,.905,'99.810791% of the declared parameter area excluded; 0.189209% remains HOLD.\nNo refinement or post-evaluation budget extension. Area is not a probability.',fontsize=11,color='#344857')
    handles=[Patch(facecolor=colors[k],label=labels[k]) for k in colors]
    fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.07,.095),ncol=3,frameon=False,fontsize=9)
    fig.text(.08,.035,'Fixed reference; nodes 15/17 independently displaced in boosted x. Strong gate: unchanged order + weight gap >20% + TV <=0.25.\nDashed: earlier fully excluded paired line (PR115). HOLD may contain certified points. No general stability claim.',fontsize=9,color='#344857')
    fig.savefig(HERE/'coverage.png',dpi=180,facecolor='white');plt.close(fig)

if __name__=='__main__':plot()
