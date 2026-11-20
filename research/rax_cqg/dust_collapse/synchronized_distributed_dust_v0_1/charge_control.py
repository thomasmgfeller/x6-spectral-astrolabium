"""Initial cut source response in the finite-width tube with rational enclosures."""
from fractions import Fraction as Q
import support
import tube
from coherence import add, bounds, mul, sub


def run():
    profile = tube.run()
    _,rel = support.geometry(2324)
    def bd(y,x):
        n=sum((y,k) in rel and (k,x) in rel for k in range(15))
        return (1,-9,16,-8)[n] if n < 4 else 0
    assert all(bd(y,x)==0 for y in support.PAST for x in support.FUTURE)
    report = {}
    for label,(left,right) in zip(("left","right"),support.WINDOWS):
        intervals = []
        for j in range(32):
            step = (right-left)/32
            e = mul((left+j*step,left+(j+1)*step),
                    (1/support.DELTA[1],1/support.DELTA[0]))
            total = bounds(Q(0))
            for v in support.I:
                clock = Q(profile["clock_center"][str(v)])
                r = Q(profile["clock_halfwidth"])
                u = (clock-r,clock+r)
                b = [bd(i,v) for i in support.PAST]
                z = (-2+4*u[0]+(1-u[0])*e[0],-2+4*u[1]+(1-u[1])*e[1])
                past = add(bounds(sum(x*(i-5) for i,x in enumerate(b))),
                           mul(bounds(b[3]),e))
                kernel = sub(past,mul(bounds(sum(b)),z))
                f = tuple(map(Q,profile["dwell_affine_ranges_per_vertex"][str(v)]))
                total = add(total,mul(mul((Q(99,100),Q(101,100)),f),kernel))
            intervals.append(mul(mul(bounds(Q(1,19)),sub(bounds(4),e)),total))
        lo,hi = min(a for a,b in intervals),max(b for a,b in intervals)
        report[label] = {"p_over_M_enclosure":list(map(str,(lo,hi))),
                         "display":[float(lo),float(hi)]}
    return {"fine_source_only":report,"matched_empty_interior_p":0,"true_vacuum_p":0,
            "interpretation":"finite field-history source in reference units; full-sector positive instrument and physical calibration unavailable"}


if __name__=="__main__":
    import json
    print(json.dumps(run(),indent=2))
