"""Scientific parameter-space map derived only from archived terminal cells.
SPDX-License-Identifier: Apache-2.0
"""
from ps_run import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle,Patch

def plot():
    rows=final_cells(read(HERE/'certificates.json.gz'));summary=read(HERE/'summary.json')
    colors={'TRANSFERRED_LAW_EXCLUDED':'#27648b','ORDER_EXCLUDED':'#d3dbe0','GAP_EXCLUDED':'#72b7a1','MARGINAL_TAIL_EXCLUDED':'#58a6ce','OVERLAP_TAIL_EXCLUDED':'#92539c','HOLD':'#e9a23b'}
    labels={'TRANSFERRED_LAW_EXCLUDED':'Transported count test','ORDER_EXCLUDED':'Order contradiction','GAP_EXCLUDED':'Weight gap <=20%','MARGINAL_TAIL_EXCLUDED':'New marginal Poisson test','OVERLAP_TAIL_EXCLUDED':'New overlap difference test','HOLD':'HOLD / unresolved rectangle'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig,ax=plt.subplots(figsize=(10.5,8.5));fig.subplots_adjust(left=.11,right=.76,bottom=.14,top=.85)
    patches=[];fc=[]
    for r in rows:
        a,d,e,f=map(lambda x:float(F(x)),r['box']);patches.append(Rectangle((a,e),d-a,f-e));fc.append(colors[r['status']])
    ax.add_collection(PatchCollection(patches,facecolors=fc,edgecolors='none',antialiased=False))
    slope=-float(F('292553733423/500000000000'));line,=ax.plot([-.1,.1],[-.1*slope,.1*slope],color='#172c3c',ls='--',lw=1.4,label='Earlier paired line\n(PR115)')
    ax.set(xlim=(-.1,.1),ylim=(-.1,.1),aspect='equal',xlabel='Node 15 boosted-x displacement u',ylabel='Node 17 boosted-x displacement v')
    ticks=[-.1,-.05,0,.05,.1];ax.set_xticks(ticks);ax.set_yticks(ticks);ax.grid(alpha=.2,lw=.5);ax.set_axisbelow(False)
    handles=[Patch(facecolor=colors[k],label=labels[k]) for k in colors]+[line]
    ax.legend(handles=handles,loc='upper left',bbox_to_anchor=(1.02,1),frameon=False,fontsize=9.5)
    fig.suptitle('Independent paired support motion',x=.11,ha='left',fontsize=21,fontweight='bold',y=.97)
    fig.text(.11,.9,'95.2698% of the declared parameter area excluded\n775 HOLD rectangles remain; area is not a probability.',fontsize=12,color='#344857')
    fig.text(.11,.045,'Fixed reference, nodes 15/17, 2+1 Minkowski. Excludes: unchanged order + weight gap >20% + TV <=0.25.\nA HOLD rectangle may contain already certified points on the dashed line. No general stability claim.',fontsize=9,color='#344857')
    fig.savefig(HERE/'coverage.png',dpi=180,facecolor='white');plt.close(fig)

if __name__=='__main__':plot()
