"""Stationary Dirichlet susceptibility and injectivity on the full accepted windows."""
from fractions import Fraction as Q
import json
from basisdaten import Box,box,hull,dot,det,read

U,Z,H,R=15,16,17,18
LIVE=[('Y',j) for j in (U,Z,H,R)]+[('w',Z),('w',R)]
SITES=[U,Z,H,R]
FUTURE=[7,8,9,10]


def hessian(y,w,edges,coordinates):
    n=len(coordinates)
    mat=[[box(0) for _ in range(n)] for _ in range(n)]
    for (i,j),b in edges.items():
        if not b:continue
        grad=[int(k==j)-int(k==i) if kind=='Y' else 0 for kind,k in coordinates]
        wr=[int(kind=='w' and k==j) for kind,k in coordinates]
        for p in range(n):
            for q in range(n):
                mat[p][q]+=2*b*(w[j]*grad[p]*grad[q]+(y[j]-y[i])*(grad[p]*wr[q]+grad[q]*wr[p]))
    return mat


def restricted(mat,rows,cols):
    return [[mat[i][j] for j in cols] for i in rows]


def cramer(mat):
    denominator=det(mat)
    assert not denominator.contains_zero()
    result=[]
    for i in range(len(mat)):
        row=[]
        for j in range(len(mat)):
            minor=[r[:i]+r[i+1:] for k,r in enumerate(mat) if k!=j]
            row.append((-1)**(i+j)*det(minor)/denominator)
        result.append(row)
    return denominator,result


def domain(y,w,edges,e,windows):
    # A feasible solution in either box obeys both unchanged vacuum clock equations.
    broad=[]
    for window in windows:
        values=[t*(4-d)+d-2 for t in window for d in map(Q,e.data())]
        broad.append(hull(min(values),max(values)))
    s,t=broad;u,h=y[U],y[H]
    wr=w[R]*(y[R]-h)/(t-h)
    wz=(w[Z]*(y[Z]-u)-9*w[R]*(y[R]-u)+9*wr*(t-u))/(s-u)
    yy={**y,Z:s.union(y[Z]),R:t.union(y[R])}
    ww={**w,Z:wz.union(w[Z]),R:wr.union(w[R])}
    rows=[0,2,3,5];cols=[1,3,4,5]
    minor=det(restricted(hessian(yy,ww,edges,LIVE),rows,cols))
    assert not minor.contains_zero() and ww[Z].lo>0 and ww[R].lo>0
    return {'unforced_rows':['Y15','Y17','Y18','w18'],'columns':['Y16','Y18','w16','w18'],
            'determinant_on_secants':minor.data(),'clock_box':[v.data() for v in broad],
            'weight_box':[ww[j].data() for j in (Z,R)]}


def run():
    y,w,rel,b,e,windows=read()
    free=[j for j in y if j not in {0,1,2,3,*FUTURE}]
    coords=[('Y',j) for j in free]+[('w',j) for j in free if w[j].lo>0]
    complete=hessian(y,w,b,coords)
    outside=[j for j in range(len(coords)) if coords[j] not in LIVE]
    ins=[coords.index(k) for k in LIVE]
    assert len(coords)==20 and len(outside)==14
    assert all(v.lo==v.hi==0 for row in restricted(complete,ins,outside) for v in row)
    old_positive=sorted([j for j in free if j not in SITES],
                        key=lambda k:sum(j==k for _,j in rel))
    jac=restricted(complete,[coords.index(('w',j)) for j in old_positive],
                   [coords.index(('Y',j)) for j in old_positive])
    old_det=box(1)
    for i in range(len(jac)):
        assert not jac[i][i].contains_zero() and all(v.lo==v.hi==0 for v in jac[i][i+1:])
        old_det*=jac[i][i]
    mat=restricted(complete,ins,ins);determinant,inv=cramer(mat)
    def label(k):return k[0]+str(k[1])
    return {'coordinates':list(map(label,LIVE)),'separated_old_variables':len(outside),
            'old_density_clock_jacobian_det':old_det.data(),'determinant':determinant.data(),'H':[[v.data() for v in row] for row in mat],
            'inverse':{label(k):{label(c):inv[i][j].data() for j,c in enumerate(LIVE)}
                       for i,k in enumerate(LIVE)},
            'window_test':domain(y,w,b,e,windows),'P3':{'NOT_RUN':60}}


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
