"""Recompute optimization witnesses; verify.py checks them without SciPy."""
import json
from fractions import Fraction as Q
from scipy.optimize import linprog
import support


def certify(code):
    _, rows, rhs = support.system(code)
    opt = linprog([0]*7+[1], A_ub=[[float(v) for v in row] for row in rows],
                  b_ub=list(map(float,rhs)), bounds=(None,None), method="highs")
    if not opt.success:
        raise RuntimeError((code,opt.message))
    def rational(v):
        return str(Q(float(v)).limit_denominator(10**7))
    result = {"primal":list(map(rational,opt.x)),
              "dual":{str(i):rational(v) for i,v in enumerate(opt.ineqlin.marginals)
                      if abs(v)>1e-10}}
    optimum = support.verify(code,result)
    result["support"] = support.statuses(optimum)
    return result


if __name__ == "__main__":
    certs = {str(c):certify(c) for c in support.catalogue()}
    (support.HERE/"certificates.json").write_text(json.dumps(certs,sort_keys=True)+"\n")
    print(json.dumps(support.summarize(certs),indent=2,sort_keys=True))
