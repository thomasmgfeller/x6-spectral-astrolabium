"""Independent four-dimensional tensor and junction identities, exact algebra."""
import sympy as s


def einstein(g, coordinates):
    n=len(coordinates); inv=s.simplify(g.inv()); C={}
    def gamma(a,b,c):return C.get((a,b,c),s.S.Zero)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                z=s.simplify(sum(inv[a,d]*(s.diff(g[d,c],coordinates[b])+s.diff(g[d,b],coordinates[c])-s.diff(g[b,c],coordinates[d]))/2 for d in range(n)))
                if z!=0:C[a,b,c]=z
    Ric=s.zeros(n)
    for a in range(n):
        for b in range(n):
            Ric[a,b]=s.simplify(sum(s.diff(gamma(c,a,b),coordinates[c])-s.diff(gamma(c,a,c),coordinates[b])+sum(gamma(c,a,b)*gamma(d,c,d)-gamma(d,a,c)*gamma(c,b,d) for d in range(n)) for c in range(n)))
    scalar=s.simplify(sum(inv[a,b]*Ric[a,b] for a in range(n) for b in range(n)))
    return s.simplify(Ric-g*scalar/2)


def run():
    checks=[]
    def zero(name,expr):
        val=s.simplify(expr)
        if val!=0:raise ValueError(name+': '+str(val))
        checks.append({'identity':name,'exact_residual':'0'})
    t,r,th,ph=s.symbols('T R theta phi',real=True); v=s.Function('v')(t,r)
    g=s.Matrix([[-1+v*v,v,0,0],[v,1,0,0],[0,0,r*r,0],[0,0,0,r*r*s.sin(th)**2]])
    E=einstein(g,(t,r,th,ph));u=s.Matrix([1,-v,0,0]);n=s.Matrix([0,1,0,0])
    density=(v*v+2*r*v*s.diff(v,r))/r**2
    pressure=(2*r*s.diff(v,t)-v*v-2*r*v*s.diff(v,r))/r**2
    transverse=s.diff(v,t)/r+s.diff(v,t,r)-s.diff(v,r)**2-v*s.diff(v,r,2)-2*v*s.diff(v,r)/r
    zero('PG G_uu from full metric',(u.T*E*u)[0]-density)
    zero('PG G_un from full metric',(u.T*E*n)[0])
    zero('PG G_nn from full metric',(n.T*E*n)[0]-pressure)
    zero('PG angular pressure from full metric',E[2,2]/r**2-transverse)
    h=s.Function('h')(t); mu=s.symbols('mu',positive=True)
    for name,expr,target in [('density',density,3*h*h),('radial pressure',pressure,2*s.diff(h,t)-3*h*h),('angular pressure',transverse,2*s.diff(h,t)-3*h*h)]:
        zero('FLRW '+name,expr.subs(v,h*r).doit()-target)
    for name,expr in [('density',density),('radial pressure',pressure),('angular pressure',transverse)]:
        zero('Schwarzschild '+name,expr.subs(v,s.sqrt(2*mu/r)).doit())
    w,R,A=s.symbols('w R A',real=True);Rpos=s.symbols('Rpos',positive=True)
    zero('No delta angular stress at comoving boundary',-s.Rational(3,2)*w*w/R-w*(-s.Rational(3,2)*w/R))
    B=s.sqrt(w*w+1-2*mu/Rpos)
    sig=(1-B)/Rpos; p=(A+mu/Rpos**2)/B+(B-1)/Rpos
    D=lambda expr:s.diff(expr,Rpos)*w+s.diff(expr,w)*A
    zero('Shell conservation with zero normal energy flux',D(sig)+2*w/Rpos*(sig+p/2))
    zero('Shell normal pressure balance',-sig*(A+mu/Rpos**2)/B+p*(B+1)/Rpos-(2*A/Rpos+w*w/Rpos**2))
    zero('Interior geometric mass pressure work',D(Rpos*w*w/2)+Rpos**2*(-2*A/Rpos-w*w/Rpos**2)*w/2)
    Ms=Rpos*(1-B)
    zero('Shell mass including binding energy',mu-(Rpos*w*w/2+Ms-Ms**2/(2*Rpos)))
    z=s.symbols('z',positive=True);vdot=1/(1+z)
    zero('EF induced proper-time metric',-(1-z*z)*vdot**2-2*z*vdot+1)
    zero('Outgoing null slope in EF',(1-z)/(2/(1+z))-(1-z*z)/2)
    f=s.Function('f')(r)
    gs=s.diag(-f,1/f,r*r,r*r*s.sin(th)**2);Es=einstein(gs,(t,r,th,ph))
    rho=(1-f-r*s.diff(f,r))/r**2;pr=-rho;pt=s.diff(f,r,2)/2+s.diff(f,r)/r
    zero('Static exterior density from full metric',Es[0,0]/f-rho)
    zero('Static exterior radial pressure from full metric',Es[1,1]*f-pr)
    zero('Static exterior angular pressure from full metric',Es[2,2]/r**2-pt)
    a=s.symbols('a',positive=True);F=1-2*mu/r+2*mu*a/r**4
    zero('Conditional atmosphere density',rho.subs(f,F).doit()-6*mu*a/r**6)
    zero('Conditional atmosphere radial pressure',pr.subs(f,F).doit()+6*mu*a/r**6)
    zero('Conditional atmosphere transverse pressure',pt.subs(f,F).doit()-12*mu*a/r**6)
    zero('Conditional atmosphere radial stress conservation',s.diff(-6*mu*a/r**6,r)+2*(-6*mu*a/r**6-12*mu*a/r**6)/r)
    energy=2*mu/r*(1-a/r**3);acc=-mu/r**2+4*mu*a/r**5
    zero('Conditional angular junction',energy+F-1)
    zero('Conditional temporal junction',acc+s.diff(F,r)/2)
    zero('Conditional boundary normal pressure',-(2*acc/r+energy/r**2)+6*mu*a/r**6)
    zero('Conditional acceleration from energy law',s.diff(energy,r)/2-acc)
    K=s.diff(F,r,2)**2+4*(s.diff(F,r)/r)**2+4*((1-F)/r**2)**2
    zero('Conditional exterior curvature polynomial',K-mu**2/r**6*(48-480*a/r**3+1872*a*a/r**6))
    x=s.symbols('x',real=True)
    zero('Exterior curvature monotonicity polynomial',s.diff(x*x*(48-480*x+1872*x*x),x)-96*x*(1-15*x+78*x*x))
    zero('Positive quadratic certificate',1-15*x+78*x*x-(78*(x-s.Rational(5,52))**2+s.Rational(29,104)))
    # An exact polynomial parameterization of the conditional classical event horizon.
    y=s.symbols('y',positive=True);delta=s.Rational(9,2)*mu*y**3
    Rb=s.Rational(9,2)*mu*y**2;chi=3*(1-y);Rh=Rb*chi
    # d/dT = -(d/dy)/(d delta/dy), h=2/(3 delta).
    zero('Classical event horizon outgoing null generator',-s.diff(Rh,y)/s.diff(delta,y)-(1-2*Rh/(3*delta)))
    zero('Classical EH boundary endpoint',Rh.subs(y,s.Rational(2,3))-2*mu)
    zero('Classical EH center endpoint',Rh.subs(y,1))
    return checks


if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
