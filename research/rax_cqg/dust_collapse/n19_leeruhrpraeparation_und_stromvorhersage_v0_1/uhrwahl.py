"""Complete stationary clock alternatives and a scheduled positive control."""
from fractions import Fraction as F
from zustand import nominal,check


def run(early):
    from gemischt import Action, N, COEFF,CLOCK,WINDOWS,certify,propose
    from algebra import mid
    from quelle import box,Box
    start,(y,w)=nominal(early)
    native=Action(False)
    zaxis=CLOCK.index(16)

    class FarWeight:
        def __init__(self,mu):
            self.mu=mu                           # None means the far weight is an unknown.

        def fields(self,x):
            ys,ws=native.fields(x[:N])
            mu=x[-1] if self.mu is None else (box(self.mu) if isinstance(x[0],Box) else mid(self.mu))
            ws[7]+=mu
            return ys,ws

        def evaluate(self,x,targets=(0,0)):
            ys,ws=self.fields(x)
            g,H=native.evaluate(x[:N])
            cast=box if isinstance(x[0],Box) else mid
            mu=x[-1] if self.mu is None else cast(self.mu)
            column=[cast(0) for _ in range(N)]
            for k,i in enumerate(CLOCK):
                coefficient=2*COEFF.get((i,7),0)
                column[k]=coefficient*(ys[i]-ys[7])
                g[k]+=mu*column[k]
                H[k][k]+=mu*coefficient
            if self.mu is None:
                for row,v in zip(H,column):
                    row.append(v)
                last=[cast(0)]*(N+1)
                last[zaxis]=cast(1)
                H.append(last)
                g.append(ys[16]-cast(F(1,12)))
            return g,H

    tests=[]
    for delta in (-F(1,10**8),F(1,10**8),-F(1,10**9),F(1,10**9),None):
        model=FarWeight(delta)
        x=propose(model,[mid(v) for v in start]+([mid(0)] if delta is None else []))
        domain,proof=certify(model,x,(0,0),F(1,10**22))
        ys,ws=model.fields(domain)
        passed=check(ys,ws,require_windows=delta is None or abs(delta)<F(1,10**8))
        res={'mode': 'scheduled' if delta is None else 'fixed_future_offset',
             'both_windows':passed, 'delta_w7':(ws[7]-w[7]).data(),'Y15':ys[15].data(),'Y16':ys[16].data(),
             'delta_Y15':(ys[15]-y[15]).data(),'proof':proof}
        if delta is None:
            target=(1-box(937).sqrt())/12
            assert (ys[15]-target).contains_zero()
            assert ys[15].hi<ys[16].lo
            from basisdaten import hull as old_hull, box as old_box
            from quelle import hull
            import rand
            a={i:old_hull(*v.data()) for i,v in ys.items()}
            m={i:old_hull(*v.data()) for i,v in ws.items()}
            arms=[]
            for J in (-F(1,10**6),F(1,10**6)):
                pulse=rand.finite(a,m,COEFF,old_box(F(1,6)),WINDOWS,J,False)
                yy,ww=ys.copy(),ws.copy()
                for node,changes in pulse['future_and_endpoints'].items():
                    i=int(node)
                    yy[i]+=hull(*changes['dY'])
                    ww[i]+=hull(*changes['dw'])
                check(yy,ww,J)
                d=-box(J)/(2*(target+3))
                assert (yy[16]-F(1,12)-d).contains_zero()
                dw=hull(*pulse['future_and_endpoints']['16']['dw'])
                change=(ys[16]+d-ys[15])*dw+ws[16]*d
                assert not change.contains_zero()
                arms.append({'Jw':str(J),'predicted_dY16':d.data(),'delta_K':change.data()})
            res['scheduled_pulses']=arms
        tests.append(res)
    from quelle import hull
    gap=hull(*tests[3]['Y15'])-hull(*tests[2]['Y15'])
    assert not gap.contains_zero()
    midpoint=F(-5,2)
    output=(midpoint**2-6)/(2*(midpoint+3))
    chart=(output+F(11,6))/F(23,6)
    assert output==F(1,4) and chart>WINDOWS[0][1]
    return {'tests':tests,'Y15_pair_gap':gap.data(),'half_tick':{'Y15':str(midpoint),
            'Y16':str(output),'x16':str(chart),'in_sender_window':False}}
