"""Locate the active probability-level bound on the full N15 support."""
from full import inputs,total,conj,mul,scale,modupper,F,write

def calculate(tag):
    names,reach,base,cols,known,mags,radii=inputs(tag)
    b=[scale(F(1,2),known[i][1]) for i in (0,1)]
    rows=[]
    for j,col in enumerate(cols):
        projection=total(mul(conj(z),total(col[k][i] for k in range(3))) for i,z in enumerate(b))
        center=mul(projection,known[j][1])[0] if known[j] else F(0)
        radius=modupper(projection)*(radii[j] if known[j] else mags[j])
        rows.append((center-radius,center+radius))
    witnesses={}
    for key,ids in zip(('chain','one'),reach):
        witnesses[key]={
            'smallest_cross_terms':[[names[j],str(rows[j][0])] for j in sorted(ids,key=lambda j:rows[j][0])[:5]],
            'largest_cross_terms':[[names[j],str(rows[j][1])] for j in sorted(ids,key=lambda j:-rows[j][1])[:5]]}
    return witnesses
if __name__=='__main__':
    write('bottleneck.json',{tag:calculate(tag) for tag in ('coarse','fine')})
