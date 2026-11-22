"""Numerical cross-check of the certified contrast and transfers with a fixed calibration."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
import hashlib,json,math
from modell import ROOT
from quadratur import amplitudes,readout

def pair(z):return [z.real,z.imag]

def contrast(rho,n,k,method):
    arms=['0','4+','4-'];broad=amplitudes(1,rho,'positive',n,k,method,arms);packet=amplitudes(1,rho,'packet',n,k,method,arms)
    z={a:[(broad[a][0]+v)/2 for v in packet[a]] for a in arms};assert abs(z['0'][0]-z['0'][1])<1e-13
    ref=json.loads((ROOT/'quellen/referenz.json').read_bytes());old=complex(*ref[str(F(rho))+'|positive|1|wide']['fine']['kernels']['0'])
    assert abs(broad['0'][0]-old)<1e-7
    out={}
    for tag in ('4+','4-'):
        rows=[]
        for s in (0,1):
            a=z['0'][s];b=z[tag][s];cross=b*a.conjugate();values={}
            for name,rot in [('0',1),('minus_pi_over_2',-1j)]:
                plus=abs(a+rot*b)**2/4;minus=abs(a-rot*b)**2/4
                assert abs((plus-minus)-(rot*cross).real)<1e-13
                incoherent=sum(abs(t/2)**2 for t in (a,rot*b));assert abs(incoherent-(plus+minus)/2)<1e-14
                values[name]={'p_plus':plus,'p_minus':minus,'balance':plus-minus,'orthogonal_record_balance':0}
            rows.append(values)
        out[tag]={'minus':rows[0],'plus':rows[1],'delta_balance':{w:rows[1][w]['balance']-rows[0][w]['balance'] for w in rows[0]},'delta_Z':pair(z[tag][1]-z[tag][0])}
    return {'null_broad':pair(broad['0'][0]),'null_common':pair(z['0'][0]),'shifted':out}

def calc(case):
    kind,rho,m=case
    if kind=='packet':
        return 'witness|'+str(F(rho)),{f'{method}{n}x{k}':contrast(rho,n,k,method) for method,n,k in [('gauss',3,4),('gauss',5,10),('cc',5,9)]}
    frozen=(ROOT/'eichung.json').read_bytes();assert hashlib.sha256(frozen).hexdigest()==(ROOT/'eichung.sha256').read_text().split()[0];c=json.loads(frozen);g=float(c['gain']);b=float(c['offset']);rows={}
    for method,n,k in [('gauss',3,4),('gauss',4,8),('gauss',5,10),('cc',5,9)]:
        z=amplitudes(m,rho,kind,n,k,method);view={a:v[0] for a,v in z.items()};row=readout(view);row['calibrated']=g*(row['raw']-b)
        if m:row['relative_error']=(row['calibrated']-m)/m
        if method=='gauss' and n==5:row['eleven_amplitudes']={a:pair(t) for a,t in view.items()}
        rows[f'{method}{n}x{k}']=row
    return f'{F(rho)}|{kind}|{F(m)}',rows

def run():
    cases=[(kind,rho,m) for rho in (.125,.25) for kind,m in [('packet',1),('empty',0),('vacuum',0),('positive',.25),('positive',1),('positive',4)]]
    with ProcessPoolExecutor(max_workers=3) as pool:return dict(pool.map(calc,cases))
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
