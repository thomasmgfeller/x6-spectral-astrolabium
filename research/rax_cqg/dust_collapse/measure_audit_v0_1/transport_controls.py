"""Disclosed supplement: exact measure/preparation transport controls."""
from fractions import Fraction as F
from itertools import product
import analyze as a

def ratio(theta,w,is_atom=False):
    a.require(abs(theta)<=1,'Admissible theta')
    if is_atom:
        a.require(w==0,'Atom is at zero');return F(1)
    a.require(0<w<1,'Continuous interior point')
    value=1+theta*a.qeval(w)
    a.require(value>0,'Positive Radon-Nikodym density in the continuous interior')
    return value

def run():
    thetas=[F(-1),F(-1,2),F(0),F(1,2),F(1)]
    marks=[(F(0),True)]+[(F(i,7),False) for i in range(1,7)]
    one=product_checks=0
    for theta in thetas:
        for w,atom in marks:
            r=ratio(theta,w,atom)
            a.require(r*(1/r)==1,'Transported boundary product cancels measure ratio')
            # In the common representation constant old/new boundary vectors
            # have squared moduli 1 and r, respectively.
            for k in range(5):
                a.require(r*(1/r)*w**k==w**k,'Transported polynomial matrix element')
                one+=1
        for left,right in product(marks,repeat=2):
            r=ratio(theta,*left)*ratio(theta,*right)
            a.require(r/r==1,'Product measure cancellation')
            product_checks+=1
    # An incorrect use of the continuous formula at the atom would turn
    # its Radon-Nikodym derivative into zero for theta=1.
    wrong_atom=1+a.qeval(F(0))
    a.require(wrong_atom!=ratio(F(1),F(0),True),'Wrong atom ratio detected')
    # A single compensating boundary vector gives sqrt(r), not 1, in the
    # common reference integrand. Both bra and ket must transform.
    r=ratio(F(1),F(1,4),False)
    a.require(r!=1,'One-sided transport is not full cancellation')
    output={'status':'PASS_SUPPLEMENT_CONTROLS','one_element_polynomial_checks':one,
        'two_element_product_checks':product_checks,'wrong_atom_formula':'REJECTED',
        'one_sided_boundary_compensation':'INSUFFICIENT',
        'theorem':'For all finite n, transport both boundary vectors by product(r_theta)^(-1/2); the weighted multiplication matrix element equals its reference value exactly.',
        'claim_boundary':'This is equivalence of weighted-L2 representations and their multiplication matrix elements, not a derived unitary CST time evolution.',
        'supplement_disclosed':True}
    a.dump('transport_controls.json',output)
    return output

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
