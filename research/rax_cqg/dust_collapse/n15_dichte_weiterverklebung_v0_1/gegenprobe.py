"""Independent high-precision quadrature of the original density-coordinate action."""
from fractions import Fraction
import json
import mpmath as mp

from anschluss import old

def real(q):
    q=Fraction(q)
    return mp.mpf(q.numerator)/q.denominator


def calculate(precision):
    with mp.workdps(precision):
        centers,dref=old.centers()
        h=real(old.H)
        mid=mp.mpf(1)/8
        delta=(mp.mpf(3)/722)**(mp.mpf(1)/4)
        rho=mp.exp(-mp.j*h*real(dref))
        x,weight=mp.gauss_quadrature(12,'legendre')
        I,P,F=set(old.I),set(old.P),set(old.F)
        rows=[]
        for z in (0,Fraction(1,3),-Fraction(3,5)):
            modes={}
            for name,(yc,wc) in centers.items():
                y={j:real(v) for j,v in yc.items()}
                for j in (8,9,10):
                    y[j]+=h*real(z)
                w={j:delta*real(wc[j]) if j in I else mid for j in yc}
                for j in (8,9,10):
                    w[j]=mid+h*real(z)
                for j in P:
                    w[j]=mid+real(z)/32
                def phase(t):
                    ww=dict(w)
                    ww[7]=mid+h*t
                    value=-sum(ww.values())/2
                    for i,j in old.ORDER:
                        n=sum((i,v) in old.ORDER and (v,j) in old.ORDER for v in yc)
                        if n<4:
                            value-=(1,-9,16,-8)[n]*ww[j]*(y[i]-y[j])**2/38
                    return mp.exp(mp.j*value)
                halves=[]
                for shift in (-1,1):
                    halves.append(sum(wg*phase((u+shift)/2) for u,wg in zip(x,weight))/2)
                low,high=halves
                flat=(low+high)/2
                re=((low-mp.j*rho*high)+(high+mp.j*mp.conj(rho)*low))/4
                p2=mp.mpf('0.5')+mp.im(mp.conj(low)*rho*high)/(abs(low)**2+abs(high)**2)
                jump=(mp.j*mp.conj(rho)*phase(-1)+mp.j*rho*phase(1))/2
                modes[name]=(flat,re/flat,p2,jump/phase(0))
            u,v=modes['positiv'],modes['negativ']
            # R removes every spectator-dependent relative phase at the centers.
            rows.append((u[0]/v[0],u[1]-v[1],u[2]-v[2],u[3],v[3]))
        assert max(abs(row[0]-rows[0][0]) for row in rows)<mp.mpf('1e-45')
        assert all(abs(row[1].imag)<mp.mpf('1e-45') for row in rows)
        assert all(mp.mpf('2.90146e-12')<row[1].real<mp.mpf('2.90148e-12') for row in rows)
        assert all(mp.mpf('5.80293e-12')<row[2]<mp.mpf('5.80295e-12') for row in rows)
        assert all(abs(a-mp.j)<mp.mpf('1e-21') for row in rows for a in row[3:])
        return {'praezision_dezimalstellen':precision,'behaltene_randbelegungen':len(rows),
                'quadraturpunkte_je_halbfenster':12,
                'Re_RE_auf_normierter_zentren_differenz':mp.nstr(rows[0][1].real,24),
                'zwei_moden_P_differenz_zentren':mp.nstr(rows[0][2],24),
                'max_aenderung_des_flachen_zentrenverhaeltnisses_kleiner_als':'1e-45'}

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps([calculate(60),calculate(85)],indent=2,ensure_ascii=False))
