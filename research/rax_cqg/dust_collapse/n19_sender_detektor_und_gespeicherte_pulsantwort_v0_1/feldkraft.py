"""Endpoint force and one uniform kinetic shear per event; full initial phase space."""
from fractions import Fraction as F
import json
from sonden import SOURCE, POINTER, labels, topological, arms, bands
from gegenrechnung import transfer, local_operators, normal_cdf
from vorstudie import inputs
from decimal import Decimal as D


def axpy(row, other, a):
    out = row.copy()
    if a:
        for k, x in other.items():
            out[k] = out.get(k, 0) + a*x
            if not out[k]:
                del out[k]
    return out


def bracket(row, other):
    return sum((v if var=='q' else -v)*other.get(('p' if var=='q' else 'q',i),0)
               for (var,i),v in row.items())


def make(bg,b,case,lam,reverse_ties=False):
    src,rec,tx,rx,_=case
    modes=labels(bg)
    phase={(v,k):{(v,k):1} for v in ('q','p') for k in modes}
    def at(v,k):
        return phase[(v,k)]
    def add(v,i,w,j,a):
        phase[(v,i)] = axpy(at(v,i),at(w,j),a)
    live = sorted(set(bg.nodes)-bg.past)
    for j in topological(bg,reverse_ties):
        for i in live:
            if (i,j) in bg.relation and (c:=b[j][i]):
                add('q',j,'q',i,c)
                add('p',i,'p',j,-c)
        if j==src and tx:
            # +Q_A Q_j enters both momentum equations; positions are unaffected.
            add('p',j,'q',SOURCE,-1)
            add('p',SOURCE,'q',j,-1)
        if j==rec:
            if rx:
                add('q',POINTER,'q',j,1)
                add('p',j,'p',POINTER,-1)
            stored=at('q',POINTER).copy()
        add('q',j,'p',j,lam)
    assert stored==at('q',POINTER)
    for (v,i),row in phase.items():
        for (w,j),other in phase.items():
            form=(int(v=='q')-int(w=='q'))*int(i==j)
            assert bracket(row,other)==form
    return phase


def det_integer(matrix):
    a=[row.copy() for row in matrix]
    previous,sign=1,1
    for k in range(len(a)-1):
        pivot=next((j for j in range(k,len(a)) if a[j][k]),None)
        if pivot is None:
            return 0
        if pivot!=k:
            sign=-sign
            a[k],a[pivot]=a[pivot],a[k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                a[i][j],rem=divmod(a[i][j]*a[k][k]-a[i][k]*a[k][j],previous)
                assert rem==0
        previous=a[k][k]
    return sign*a[-1][-1]


def magnitude(var, mode):
    if mode not in (SOURCE, POINTER):
        return F(1,2)
    return F(1) if var=='q' else F(1,4)


def run(bg, select, matrices):
    z,r=select(bg)
    live=sorted(set(bg.nodes)-bg.past)
    flow=transfer(bg,local_operators(bg))
    output={}
    for lam in map(F,('0','1/2','1','2')):
        cases={}
        for key,case in arms(bg,z,r).items():
            src,rec,tx,rx,centre=case
            phase=make(bg,matrices[0],case,lam)
            assert phase==make(bg,matrices[0],case,lam,True)
            row=phase[('q',POINTER)]
            # At the observation phase the recorder's own kinetic step has not happened.
            expected={('q',POINTER):1}
            if rx:
                for k in live:
                    coef=flow[rec,k]
                    if coef:
                        expected['q',k]=coef
                        if k!=rec and lam:
                            expected['p',k]=lam*coef
                if tx and lam and src!=rec and flow[rec,src]:
                    expected['q',SOURCE]=-lam*flow[rec,src]
            assert row==expected
            gain=row.get(('q',SOURCE),0)
            mu=F(gain*centre)
            var=sum(F(v*v)*magnitude(k,i) for (k,i),v in row.items())
            probs=bands(mu,var)
            lo,hi=normal_cdf(-1,mu,var),normal_cdf(1,mu,var)
            assert all(abs(D(a)-b)<D('0.000000000051') for a,b in zip(probs,(lo,hi-lo,1-hi)))
            cases[key]={'mean':str(mu),'variance':str(var),'left_middle_right':probs}
            if key=='on':
                # Field response to the readout momentum after the read event.
                assert phase['p',rec].get(('p',POINTER),0)==-1
                assert phase['q',rec].get(('p',POINTER),0)==-lam
                assert phase['p',SOURCE].get(('q',src),0)==-1
        assert cases['off']==cases['late'] and cases['reversed']==cases['reversed_off']
        if not lam:
            assert cases['on']==cases['off']==cases['negative']==cases['active_zero']
        output[str(lam)]=cases
    grams={}
    for terms in (bg.inner,live):
        covariance2=[[sum(flow[i,k]*flow[j,k] for k in live) for j in terms] for i in terms]
        determinant=det_integer(covariance2)
        assert determinant==1
        grams[str(len(terms))]={'rank':len(terms),'det_twice_covariance':determinant}
    return {'kinetic_step':output,'baseline_position_covariance':grams,
            'four_past_pairs_linear_covariance_rank_at_most':8,
            'full_symplectic_form_checked':[2*len(labels(bg))]*2}


if __name__=='__main__':
    with inputs() as (bg,select,matrices,_):
        print(json.dumps(run(bg,select,matrices),sort_keys=True,indent=2))
