"""Independent NumPy tensor oracle: all 33 histories, no orbits/contraction."""
import json
import numpy as np
from inputs import prior_core as pc
from calculus import ROOT

def scalar(h):
 m=np.array([[float(v) for v in row] for row in h])*4/np.sqrt(6)
 b=[0,1,3,4];alpha=-m[2,2];j=m[2,b];k=m[np.ix_(b,b)]+np.outer(j,j)/alpha
 eig=np.linalg.eigvalsh(k)
 a=4*np.pi*np.sqrt(2*np.pi/alpha)*np.prod((1+eig*eig)**(-.25))*np.exp(-1j*np.pi/4+.5j*np.arctan(eig).sum())
 v=np.linalg.inv(np.eye(4)-1j*k)
 return {'00':a,'10':0j,'01':0j,'20':a*(v[2,2]+2*v[2,3]+v[3,3]-1)/np.sqrt(2),
         '02':a*(v[2,2]-2*v[2,3]+v[3,3]-1)/np.sqrt(2),'11':a*(v[2,2]-v[3,3])}

def direct_dust(code,n=8):
 nodes,weights=np.polynomial.legendre.leggauss(n);weights=weights/2
 ts=[];ws=[]
 for axis in range(5):
  shape=[1]*5;shape[axis]=n;ts.append(nodes.reshape(shape));ws.append(weights.reshape(shape))
 w=ws[0]*ws[1]*ws[2]*ws[3]*ws[4];coeff=pc.pair_coefficients(code);es=[]
 for x in (2,3,4):
  k=.5+4/np.sqrt(6)/4*sum(c*(ts[x]-ts[i])**2 for i,j,c in coeff if j==x)
  es.append(np.exp(-.5j*k)*np.sinc(k/(2*np.pi)))
 e2,f,g=es;chi=np.sqrt(5/2)*((3*ts[3]**2-1)/2+(3*ts[4]**2-1)/2)
 v=w*(1+e2)
 return {'0':np.sum(v)/16,'+':np.sum(v*(f+g+f*g))/(16*np.sqrt(3)),
         'Delta':np.sum(v*(f+g-2*f*g))*np.sqrt(2/3)/32,
         'A':np.sum(v*(f-g))*np.sqrt(2)/32,
         'clock2':np.sum(v*(f+g+f*g)*chi)/(16*np.sqrt(3))}

def compute(n=8):
 from states import STATES,label
 total={label(x):0j for x in STATES};records=[]
 for code in pc.histories():
  d=direct_dust(code,n);sf=scalar(pc.h0(code));phase=np.exp(1j*pc.f4(code))/33
  for state in STATES:
   den,mode,clock=state;key='clock2' if clock=='quadratic' else den
   total[label(state)]+=phase*d[key]*sf[mode]
  records.append({'code':code,'dust':{k:[float(v.real),float(v.imag)] for k,v in d.items()}})
 return {'n':n,'arithmetic':'NumPy float64; validation oracle, not a certified error bound',
         'histories':len(records),'column':{k:[float(v.real),float(v.imag)] for k,v in total.items()},'records':records}

if __name__=='__main__':
 result=compute();(ROOT/'results/independent_5d_n8.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('Computed independent full 5D tensor rule for all',result['histories'],'histories')
