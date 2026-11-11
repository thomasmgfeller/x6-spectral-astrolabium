"""Exact boundary states; polynomial indices are (symmetric, antisymmetric)."""
import sympy as s

x,y,t,u=s.symbols('q_s q_a t_1 t_2',real=True)
DENSITY={
 '0':s.Matrix([2,0,0,0]),
 '+':s.Matrix([0,2/s.sqrt(3),2/s.sqrt(3),2/s.sqrt(3)]),
 'Delta':s.Matrix([0,s.sqrt(s.Rational(2,3)),s.sqrt(s.Rational(2,3)),-2*s.sqrt(s.Rational(2,3))]),
 'A':s.Matrix([0,s.sqrt(2),-s.sqrt(2),0])}
SCALAR={'00':s.Integer(1),'10':s.sqrt(2)*x,'20':(2*x*x-1)/s.sqrt(2),
        '02':(2*y*y-1)/s.sqrt(2),'01':s.sqrt(2)*y,'11':2*x*y}
CLOCK=s.sqrt(s.Rational(5,2))*(s.legendre(2,t)+s.legendre(2,u))
STATES=[(d,n,'constant') for d in ('0','+','Delta') for n in ('00','10','20','02')]
STATES += [('A','01','constant'),('A','11','constant'),('+','00','quadratic')]
ORIGINAL=('0:00','0:10','+:00','+:10')

def label(state):
 d,n,c=state
 return d+':'+n+(':clock2' if c=='quadratic' else '')

def gaussian_moment(n):
 return s.Integer(0) if n%2 else s.factorial2(n-1)/2**(n//2)

def scalar_product(a,b):
 p=s.Poly(s.expand(SCALAR[a]*SCALAR[b]),x,y)
 return s.simplify(sum(c*gaussian_moment(i)*gaussian_moment(j) for (i,j),c in p.terms()))

def clock_product(a,b):
 p=s.Poly((CLOCK if a=='quadratic' else 1)*(CLOCK if b=='quadratic' else 1),t,u)
 return s.simplify(sum(c/(i+1)/(j+1) for (i,j),c in p.terms() if i%2==j%2==0))

def gram():
 def entry(i,j):
  d,n,c=STATES[i];e,m,k=STATES[j]
  return s.simplify((DENSITY[d].dot(DENSITY[e])/4)*scalar_product(n,m)*clock_product(c,k))
 return s.Matrix(len(STATES),len(STATES),entry)

def evidence():
 g=gram();swap=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
 invariant=[all(s.simplify(a-b)==0 for a,b in zip(swap*DENSITY[d]*SCALAR[n].subs(y,-y),DENSITY[d]*SCALAR[n])) for d,n,c in STATES]
 return {'labels':[label(v) for v in STATES],'original_labels':list(ORIGINAL),
         'gram':[[str(g[i,j]) for j in range(g.cols)] for i in range(g.rows)],
         'rank':g.rank(),'all_swap_invariant':all(invariant),
         'scalar_polynomials':{k:str(v) for k,v in SCALAR.items()},
         'density_mask_order':['00','10','01','11'],
         'density_vectors_without_common_sqrt2':{k:[str(x) for x in v] for k,v in DENSITY.items()},
         'clock_polynomial':str(CLOCK),
         'completeness_scope':'14 states span mask-constant, clock-constant S2-invariant scalar polynomials of total degree <=2 times the unit-width Gaussian; 15th state is a clock probe, not a complete clock family'}
