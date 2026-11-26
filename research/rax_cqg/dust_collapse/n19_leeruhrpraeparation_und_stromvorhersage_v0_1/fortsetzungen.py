"""Construct stationary histories with identical cut inputs in the native action."""
from fractions import Fraction as F
from zustand import nominal,check,gradients

U,Z,H,R=15,16,17,18


def run(early):
    from algebra import box,hull,solve_box,correction
    from gemischt import CLOCK,WEIGHT,FUT,PAST,COEFF,WINDOWS
    from basisdaten import hull as old_hull, box as old_box
    import rand
    y,w=nominal(early)[1]
    variables=[('w',j) for j in WEIGHT+FUT]+[('M',j) for j in FUT]
    oldG,_=gradients(y,w)

    def coeff(i,j):
        return COEFF.get((i,j),0)

    def incoming(j,yy):
        return sum((c*(yy[j]-yy[i]) for (i,k),c in COEFF.items() if k==j),box(0))

    def row(i,yy):
        result=[]
        for kind,j in variables:
            c=coeff(i,j)
            if kind=='M':
                v=box(c)
            elif j in FUT:
                v=-c*yy[i]
            else:
                v=c*(yy[j]-yy[i])-(incoming(j,yy) if i==j else 0)
            result.append(v)
        return result

    unit=lambda k,j:[box((kind,node)==(k,j)) for kind,node in variables]

    def make(mode,alpha):
        yy=y.copy()
        if mode=='all_momenta':
            yy[R]+=alpha
            m_other=incoming(R,y)-(y[R]-y[H])
            radicand=(y[R]-y[H])*(y[R]-y[H])-2*alpha*m_other
            yy[H]=yy[R]-radicand.sqrt()
        native=gradients(yy,w)[0]
        A=[row(i,yy) for i in CLOCK]
        rhs=[oldG[i]-native[i] for i in CLOCK]
        A.append(unit('w',Z))
        rhs.append(box(0))
        if mode=='all_momenta':
            for i in PAST:
                A.append(row(i,yy))
                rhs.append(oldG[i]-native[i])
        else:
            for ids in ([0],PAST,[3]):
                A.append([sum(values) for values in zip(*(row(i,yy) for i in ids))])
                rhs.append(box(0))
            A.append(unit('w',R))
            rhs.append(box(alpha))
        # Keep the receiver-window chart fixed by preserving the far clock Y7.
        A.append([m-y[7]*a for m,a in zip(unit('M',7),unit('w',7))])
        rhs.append(box(0))
        assert len(A)==len(variables)==17
        v=solve_box(A,rhs)
        _,qnorm=correction(A)
        change=dict(zip(variables,v))
        ww=w.copy()
        for i in WEIGHT+FUT:
            ww[i]+=change['w',i]
        for j in FUT:
            yy[j]=(w[j]*y[j]+change['M',j])/ww[j]
        # Exact fixed coordinates, known from the linear constraints.
        assert (ww[Z]-w[Z]).contains_zero() and (yy[7]-y[7]).contains_zero()
        ww[Z]=w[Z]; yy[7]=y[7]
        check(yy,ww)
        G,_=gradients(yy,ww)
        dG=[G[i]-oldG[i] for i in PAST]
        assert dG[0].contains_zero() and sum(dG).contains_zero()
        if mode=='all_momenta':
            assert all(v.contains_zero() for v in dG)
        else:
            assert dG[3].contains_zero() and not dG[1].contains_zero()
        out={'parameter':str(alpha),'q_inverse_bound':str(qnorm),
             'delta_weights_and_far_moments':{kind+str(j):v.data() for (kind,j),v in change.items()},
             'dY17':(yy[H]-y[H]).data(),'dY18':(yy[R]-y[R]).data(),
             'dw18':(ww[R]-w[R]).data(),'dG_past':[v.data() for v in dG]}
        return yy,ww,out

    def pulse(yy,ww,J):
        a={i:old_hull(*v.data()) for i,v in yy.items()}
        m={i:old_hull(*v.data()) for i,v in ww.items()}
        arm=rand.finite(a,m,COEFF,old_box(F(1,6)),WINDOWS,J,False)
        yn=yy.copy(); wn=ww.copy()
        for node,values in arm['future_and_endpoints'].items():
            i=int(node)
            yn[i]+=hull(*values['dY'])
            wn[i]+=hull(*values['dw'])
        check(yn,wn,J)
        s,t,u,h=(yy[i] for i in (Z,R,U,H))
        d=hull(*arm['delta_Y_z']); q=hull(*arm['delta_Y_r'])
        mz=incoming(Z,yy)
        # Eliminate the unobserved far moments using the native z and h rows.
        gain_z=d*(1+(s+d-u)/(s-h))
        gain_r=q*(s+d-u)*(s+d-h)/(mz*(t+q-h))
        reduced=ww[Z]*gain_z+ww[R]*gain_r
        dwz=hull(*arm['future_and_endpoints'][str(Z)]['dw'])
        direct=(s+d-u)*dwz+ww[Z]*d
        assert (direct-reduced).contains_zero()
        return {'Jw':str(J),'dY16':d.data(),'dY18':q.data(),'delta_K':reduced.data(),
                'from_full_continuation':direct.data(),'coefficient_w18':gain_r.data()}

    members={}
    for name in ('fixed_inner_clocks','all_momenta'):
        cases=[]
        for alpha in (-F(1,10**6),F(1,10**6)):
            yy,ww,case=make(name,alpha)
            case['pulses']=[pulse(yy,ww,J) for J in (-F(1,10**6),F(1,10**6))]
            cases.append(case)
        gaps=[]
        for a,b in zip(*(c['pulses'] for c in cases)):
            delta=hull(*b['delta_K'])-hull(*a['delta_K'])
            direct=hull(*b['from_full_continuation'])-hull(*a['from_full_continuation'])
            assert not delta.contains_zero() and not direct.contains_zero()
            assert (direct-delta).contains_zero()
            if name=='fixed_inner_clocks':
                identity=F(2,10**6)*hull(*a['coefficient_w18'])
                assert (delta-identity).contains_zero()
            gaps.append({'Jw':a['Jw'],'delta_K_plus_history_minus_minus_history':delta.data()})
        members[name]={'backgrounds':cases,'gaps':gaps}
    return {'results':members,'shared_baseline_K':(w[Z]*(y[Z]-y[U])).data(),
            'coordinates':[kind+str(i) for kind,i in variables],
            'P3':{'NOT_RUN':60}}
