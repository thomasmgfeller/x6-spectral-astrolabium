"""Pulsfreier Endausgang für zwei Dichtefenster, 16 ausgehende und zwei eingehende Uhren."""
import argparse
from fractions import Fraction as F
from math import ceil
import json
from fenster import D, K, SPACING, HALF, ROOT, FIRST, LAST, ORDER, INNER, EDGES, I, pi_bound
from intervalle import C, S, cis, gaussian, sinc
from modell import clocks, dwell, INNER_MEANS

N = 24
RAILS = range(FIRST,LAST+1)
TAG = F(1,2048)


def majorant():
    # Simultaneous majorant for separate incoming and outgoing rail polynomials.
    z4,z5 = F(4,64), F(1,64)+4*HALF
    radii = [z4,z5,0,0,0,0,0]
    rad=dict.fromkeys(ORDER,0)
    rad.update({j:K*r for j,r in zip(INNER,radii)})
    y=clocks(F(1,4),INNER_MEANS)
    f=dwell(INNER_MEANS)
    change_f={4:(z4+z5)/2,5:z4/2,6:z5/2,12:0}
    bound=F(0)
    for j in (4,5,6,11,12,13):
        cabs,cim=F(1,2),F(0)
        for (i,jj),b in EDGES.items():
            if jj==j:
                g=abs(y[j]-y[i])+rad[j]+rad[i]
                cabs+=F(abs(b),38)*g**2
                cim+=F(abs(b),19)*g*(rad[i]+rad[j])
        if j in change_f:
            df=change_f[j]
            assert f[j]+df < 1
            bound+=F(101,100)*((f[j]+df)*cim+df*cabs)
        else:
            bound+=(F(1,8)+(TAG+HALF if j==11 else 0))*cim
    assert D.hi<S and F(15,2)*F(SPACING.hi,S)<F(1,64)
    m=3**ceil(bound)
    err=4*F(m,4**(2*N))/(1-F(1,4))
    return bound,err


def action_data(n,z,t,targets):
    u=list(map(I.of,INNER_MEANS))
    u[0]+=z/64
    u[1]+=(n-F(1,2))*SPACING+HALF*t
    y=clocks(F(1,4),u)
    c={j:I.of(F(-1,2)) for j in targets}
    for (i,j),b in EDGES.items():
        if j in c:
            c[j]-=F(b,38)*(y[j]-y[i])**2
    return c,dwell(u)


def currents():
    pi=pi_bound()
    theta=(F(225,608)*(SPACING/2)**2-F(32331,38912))/(72*K**2)
    entries={label:{} for label in ("baseline","line_window","closed_window")}
    for n in RAILS:
        for m in (0,1):
            k=n-m
            delta=I.of(int(k==0))
            entries["baseline"][n,m]=C(delta)
            entries["line_window"][n,m]=(C(0,1)*cis(k*theta)).scale(2/(pi*k)) if k%2 else C(0)
            h=I.of(0)
            for j in range(1,9):
                h+=F(4,17)*cis((n+8)*j*pi/17).im*cis((m+8)*j*pi/17).im
            entries["closed_window"][n,m]=cis(k*(theta+pi/2)).scale(h-delta)
    return entries


def integrals(err):
    res={(n,m,mark):C(0) for n in RAILS for m in (0,1) for mark in (-1,1)}
    for z,wz in gaussian(N):
        for t,wt in gaussian(N):
            left={}
            for m in (0,1):
                c,f=action_data(m,z,t,(4,5,6,11))
                phase=I.of(0)
                volume=I.of(1)
                for j in (4,5,6):
                    arg=D*f[j]*c[j]
                    phase+=arg
                    volume*=f[j]*sinc(arg/100)
                gamma=D*c[11]
                volume*=sinc(HALF*gamma)*wz*wt
                for mark in (-1,1):
                    left[m,mark]=cis(phase+gamma*(F(1,8)+mark*TAG)).scale(volume)
            for n in RAILS:
                c,f=action_data(n,z,t,(12,13))
                arg=D*f[12]*c[12]
                right=cis(arg+D*c[13]/8).scale(f[12]*sinc(arg/100))
                for key,v in left.items():
                    index=(n,*key)
                    res[index]=res[index]+right*v
    return {index:v.pad(err) for index,v in res.items()}


def run():
    b,err=majorant()
    values=integrals(err)
    matrices=currents()
    differences={}
    for label,matrix in matrices.items():
        balances=[]
        for mark in (-1,1):
            z0,z1=values[0,0,mark],values[1,1,mark]
            w=[sum((matrix[n,m]*values[n,m,mark] for n in RAILS),C(0)) for m in (0,1)]
            def intensity(sign):
                t=C(0,sign)
                a=z0+t*z1
                bb=w[0]+t*w[1]
                return ((a*a.conj()).re+(bb*bb.conj()).re)/2
            im,ip=intensity(-1),intensity(1)
            balances.append((im-ip)/(im+ip))
        differences[label]=balances[1]-balances[0]
    original=differences["baseline"]
    return {"gauss_nodes_per_axis":N,"exponent_bound":str(b),"amplitude_error":str(err),
            "balance_difference":{k:v.rounded(24) for k,v in differences.items()},
            "change_vs_baseline":{k:(v-original).rounded(24) for k,v in differences.items() if k!="baseline"},
            "fraction_of_baseline":{k:(v/original).rounded(15) for k,v in differences.items() if k!="baseline"}}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json",action="store_true")
    a=p.parse_args()
    result=run()
    if a.json:
        print(json.dumps(result,indent=2))
    else:
        assert result==json.loads((ROOT/"endintervall.json").read_text())
        print("PASS · Alle 64 pulsfreien Übergangsintegrale und drei Endkontraste eingeschlossen")
