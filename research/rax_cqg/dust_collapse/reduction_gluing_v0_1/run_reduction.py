"""Certified first-column expansion; exact density and scalar integrations."""
import argparse,json
from time import monotonic
from flint import arb,acb,ctx
from inputs import prior_core as pc
from calculus import ROOT,scalar_factors,gaussian_data,summarize,norm_ball
from states import STATES,ORIGINAL,label

class DustQuadrature:
 def __init__(self,n):
  self.n=n;rule=[arb.legendre_p_root(n,k,weight=True) for k in range(n)]
  self.t=[x[0] for x in rule];self.w=[x[1]/2 for x in rule]
  assert all(w>0 for w in self.w) and sum(self.w).contains(1)
  self.p2=[(3*x*x-1)/2 for x in self.t]
  self.dd=[[(x-y)*(x-y)*pc.beta()/4 for y in self.t] for x in self.t]
  self.cache={}

 def output(self,coeff,indices):
  items=tuple(sorted((c,i) for c,i in zip(coeff,indices) if c));mirrored=tuple(sorted((c,self.n-1-i) for c,i in items))
  key=min(items,mirrored)
  if key not in self.cache:
   f=acb(0);f2=acb(0)
   for l,w in enumerate(self.w):
    k=arb(1)/2+sum(c*self.dd[l][i] for c,i in key)
    term=w*pc.E(k);f+=term;f2+=term*self.p2[l]
   if not f.is_finite() or not f2.is_finite():raise ArithmeticError('nonfinite clock contraction')
   self.cache[key]=(f,f2)
  return self.cache[key]

 def evaluate(self,code):
  coeff=pc.pair_coefficients(code);pred=[i for i,j,c in coeff if j==2]
  output=[[next((c for i,j,c in coeff if i==a and j==x),0) for a in (0,1,2)] for x in (3,4)]
  total={k:acb(0) for k in ('0','+','Delta','A','clock2')}
  for i,wi in enumerate(self.w):
   for j,wj in enumerate(self.w):
    for k,wk in enumerate(self.w):
     inds=(i,j,k);k2=arb(1)/2+sum(self.dd[k][inds[a]] for a in pred)
     f,f2=self.output(output[0],inds);g,g2=self.output(output[1],inds)
     w=wi*wj*wk*(1+pc.E(k2))
     total['0']+=w;total['+']+=w*(f+g+f*g)
     total['Delta']+=w*(f+g-2*f*g);total['A']+=w*(f-g)
     total['clock2']+=w*(f2+g2+f2*g+f*g2)
  factors={'0':arb(1)/16,'+':1/(16*arb(3).sqrt()),
           'Delta':(arb(2)/3).sqrt()/32,'A':arb(2).sqrt()/32,
           'clock2':(arb(5)/2).sqrt()/(16*arb(3).sqrt())}
  result={k:v*factors[k] for k,v in total.items()}
  if not all(v.is_finite() for v in result.values()):raise ArithmeticError('nonfinite density amplitude')
  return result

def dust_errors(code,n):
 e,degrees=pc.dust_error(code,n)
 # Clock probe on the single complex Bernstein-ellipse axis; all others real.
 a=arb(5)/4;clock_bound=(arb(5)/2).sqrt()*3*(a*a+1)/2
 ratios={'0':1/arb(3).sqrt(),'+':arb(1),'Delta':2*arb(2).sqrt()/3,
         'A':(arb(2)/3).sqrt(),'clock2':clock_bound}
 return {k:e*v for k,v in ratios.items()},degrees

def compute(n=48,precision=192,progress=True):
 if not isinstance(n,int) or n<2 or not isinstance(precision,int) or precision<64:raise ValueError('n>=2 and precision>=64 required')
 ctx.prec=precision;quad=DustQuadrature(n);names=[label(x) for x in STATES]
 widths={'sigma_s=1/2':'1/2','sigma_s=2':'2'}
 total={k:acb(0) for k in names+list(widths)};error={k:arb(0) for k in total};records=[];start=monotonic()
 for index,(code,members) in enumerate(pc.orbits().items(),1):
  d=quad.evaluate(code);de,degrees=dust_errors(code,n);sf,meta=scalar_factors(pc.h0(code))
  phase=acb(0,pc.f4(code)).exp();weight=arb(len(members))/33
  for state in STATES:
   density,mode,clock=state;key=label(state);dk='clock2' if clock=='quadratic' else density
   total[key]+=weight*phase*d[dk]*sf[mode];error[key]+=weight*de[dk]*abs(sf[mode])
  widthf={}
  for key,value in widths.items():
   wf,_,_=gaussian_data(pc.h0(code),sigma_s=value);widthf[key]=pc.pack(wf)
   total[key]+=weight*phase*d['+']*wf;error[key]+=weight*de['+']*abs(wf)
  records.append({'representative':code,'members':members,'multiplicity':len(members),'F4':pc.f4(code),
                  'dust':{k:pc.pack(v) for k,v in d.items()},'dust_errors':{k:v.str(25,more=True) for k,v in de.items()},
                  'weighted_degrees':degrees,'scalar_factors':{k:pc.pack(v) for k,v in sf.items()},
                  'width_scalar_factors':widthf,'gaussian':meta})
  if progress:print(f'orbit {index}/10; cache {len(quad.cache)}; elapsed {monotonic()-start:.1f}s',flush=True)
 column={k:summarize(total[k],error[k]) for k in names};width_results={k:summarize(total[k],error[k]) for k in widths}
 omitted=[k for k in names if k not in ORIGINAL]
 residual=norm_ball([column[k] for k in omitted]);column_norm=norm_ball(column.values())
 ref=json.loads((ROOT/'inputs/prior_mixing_48.json').read_text())
 preserved=pc.unpack(column['+:00']['certified_ball']).overlaps(pc.unpack(ref['amplitudes']['coupled']['certified_ball']))
 if not preserved:raise ArithmeticError('original mixed matrix element changed')
 return {'experiment_id':'CST-DUST-AA-REDUCTION-GLUING-v0.1','input':'0:00','quadrature':{'n':n,'precision_bits':precision,'rho':2},
         'column':column,'omitted_labels':omitted,
         'projection_error_15_vs_4':residual.str(25,more=True),
         'column_norm_in_15':column_norm.str(25,more=True),
         'relative_projection_error_in_15':(residual/column_norm).str(25,more=True),
         'not_a_probability_or_full_space_upper_bound':True,
         'original_entry_enclosures_overlap':preserved,'original_entry_change_under_basis_extension':'exactly zero by unchanged bra, ket and kernel',
         'width_controls':width_results,'width_control_interpretation':'different normalized outgoing preparations, not a cutoff error',
         'orbits':records,'physical_gates':json.loads((ROOT/'experiment_contract.json').read_text())['physical_gates']}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=48);p.add_argument('--precision',type=int,default=192)
 p.add_argument('--output',type=str,default='results/reduction.json');a=p.parse_args()
 result=compute(a.n,a.precision);(ROOT/a.output).write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('orbits','physical_gates')},indent=2))
