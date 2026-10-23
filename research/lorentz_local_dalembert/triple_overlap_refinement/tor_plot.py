"""Four exact parameter slices of the three-support certificate cover.
SPDX-License-Identifier: Apache-2.0
"""
from tor_common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle,Patch

def plot():
    ar=read(HERE/'certificates.json.gz');s=read(HERE/'summary.json');rows=combined(ar)
    colors={'PROJECTION_EXCLUDED':'#27648b','AXIS_LAW_EXCLUDED':'#58a6ce','ORDER_EXCLUDED':'#d3dbe0','GAP_EXCLUDED':'#72b7a1','MARGINAL_TAIL_EXCLUDED':'#a485bc','OVERLAP_TAIL_EXCLUDED':'#643683','HOLD':'#e9ad50'}
    labels={'PROJECTION_EXCLUDED':'Source square projection','AXIS_LAW_EXCLUDED':'Node 5 count-law strips','ORDER_EXCLUDED':'Order contradiction','GAP_EXCLUDED':'Joint weight gap <=20%','MARGINAL_TAIL_EXCLUDED':'Marginal event exclusions','OVERLAP_TAIL_EXCLUDED':'Overlap event exclusions','HOLD':'HOLD / unresolved box'}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig,axs=plt.subplots(2,2,figsize=(11.5,10.2));fig.subplots_adjust(left=.08,right=.94,bottom=.22,top=.82,hspace=.35,wspace=.25)
    for ax,w in zip(axs.flat,map(F,('-9/100','-1/100','1/100','9/100'))):
        patches=[];fc=[]
        for r in rows:
            a,d,e,f,l,h=map(F,r['box'])
            if not l<w<h:continue
            patches.append(Rectangle((float(a),float(e)),float(d-a),float(f-e)));fc.append(colors[r['status']])
        ax.add_collection(PatchCollection(patches,facecolors=fc,edgecolors='white',linewidths=.15,antialiased=False))
        ax.set(xlim=(-.1,.1),ylim=(-.1,.1),aspect='equal',xlabel='Node 15 displacement u',ylabel='Node 17 displacement v',title=f'Node 5 displacement w = {float(w):+.2f}')
        ax.set_xticks([-.1,-.05,0,.05,.1]);ax.set_yticks([-.1,-.05,0,.05,.1]);ax.grid(alpha=.15,lw=.5)
    fig.suptitle('Three independently moving supports: overlap refinement',x=.08,y=.97,ha='left',fontsize=19,fontweight='bold')
    percent=float(F(s['excluded_volume_fraction'])*100)
    fig.text(.08,.895,f"{percent:.6f}% of declared parameter volume excluded; {s['states'].get('HOLD',0)} terminal boxes remain HOLD.\nThe full w = 0 plane retains the earlier two-support theorem. Volume is not probability.",fontsize=11,color='#344857')
    present=[k for k in colors if s['states'].get(k,0)]
    fig.legend(handles=[Patch(facecolor=colors[k],label=f"{labels[k]} ({s['states'][k]})") for k in present],loc='lower left',bbox_to_anchor=(.07,.095),ncol=2,fontsize=9,frameon=False)
    fig.text(.08,.035,'Fixed rational reference, independent boosted-x displacements in [-0.1,0.1]^3. Excluded target:\nunchanged order + symmetric physical weight gap >20% + full conditional count/overlap-law TV <=0.25.\nHOLD is not a counterexample. These four slices do not replace the exact three-dimensional cover.',fontsize=9,color='#344857')
    fig.savefig(HERE/'coverage.png',dpi=180,facecolor='white');plt.close(fig)

if __name__=='__main__':plot()
