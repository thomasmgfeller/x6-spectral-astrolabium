"""Set-valued rounding, including ties, with independent calibration and reading error."""
from math import ceil,floor
from fractions import Fraction as F

STEP=F(2,10**7)
REFERENCE=4073422
ERROR=STEP/4

def digits(a,b):
    assert a<=b
    return range(ceil(a/STEP-F(1,2)),floor(b/STEP+F(1,2))+1)

def decode(value,ref):
    offset=value-ref
    if offset<=-3:return 1
    if offset>=3:return -1
    return 0

def evaluate(bounds,expected):
    a,b=map(F,bounds)
    possible=digits(a-ERROR,b+ERROR)
    references=range(REFERENCE-1,REFERENCE+2)
    readings={decode(d,r) for d in possible for r in references}
    assert readings=={expected}
    return [min(possible),max(possible)]

def verify_reader():
    # Check the explicit quantizer cells, including both half-integer ties.
    for k in range(REFERENCE-12,REFERENCE+13):
        for frac in (F(-1,2),F(-1,4),F(0),F(1,4),F(1,2)):
            x=(k+frac)*STEP
            brute=[d for d in range(k-2,k+3) if abs(x-d*STEP)<=STEP/2]
            assert list(digits(x,x))==brute
    assert [decode(REFERENCE+d,REFERENCE) for d in (-3,-2,0,2,3)]==[1,0,0,0,-1]
