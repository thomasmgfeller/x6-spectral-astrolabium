"""Independent exact action differences for the residual and all 121 slope entries."""
from fractions import Fraction as F
import subprocess

C=tuple(range(15,22))
P=(16,18,19,21)
Q=10**9

def check(binary,header,coefficients,collar):
    # Integer arithmetic for the cubic action on a shared 10^-9 lattice.
    # A/Q^3 is the unscaled action. Differences below are exact for degree <=2
    # in any single coordinate, including after one earlier differentiation.
    y=[0]*22;w=[0]*22
    for k,(l,h,a,b) in collar.items():y[k]=(l+h)//2;w[k]=(a+b)//2
    for j,t in zip(C,[-16,-8,-4,5,1,2,7]):y[j]=t*(Q//8)
    for j,v in zip(P,[5,3,2,1]):w[j]=v*(Q//32)
    lines=header.splitlines()
    start=1+int(lines[0])
    for i in range(8):
        k=int(lines[start+i].split()[0]);lines[start+i]=f'{k} {y[k]} {y[k]} {w[k]} {w[k]}'
    inputs=[y[j] for j in C]+[w[j] for j in P]
    lines.extend(f'{x} {x}' for x in inputs)
    received=subprocess.run([str(binary),'0','1','0','algebra'],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    rows=[list(map(int,line.split())) for line in received.stdout.splitlines()]
    assert len(rows)==11 and all(len(v)==24 for v in rows)
    def action():
        return 19*Q**2*sum(w[j] for j in range(22))+sum(v*w[j]*(y[j]-y[i])**2 for (i,j),v in coefficients.items())
    step=Q//8
    def variation(fn,field,j):
        field[j]+=step
        up=fn()
        field[j]-=2*step
        down=fn()
        field[j]+=step
        return F(up-down,2*step)
    for k,(field,j) in enumerate([(w,j) for j in P]+[(y,j) for j in C]):
        factor=F(1) if k<4 else F(-1,2)
        def residual():return factor*variation(action,field,j)/Q**2
        targets=[residual()*Q]+[Q**2*variation(residual,axis,node) for axis,node in [(y,n) for n in C]+[(w,n) for n in P]]
        for a,(value,lo,hi) in enumerate(zip(targets,rows[k][::2],rows[k][1::2])):
            assert lo<=value<=hi,(j,a,value,lo,hi)
    return 11*12
