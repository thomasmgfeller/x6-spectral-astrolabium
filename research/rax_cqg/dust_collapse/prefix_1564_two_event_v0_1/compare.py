"""Verify every exact result and the floating-point quadratures separately."""
import json
import sys
from pathlib import Path

def compare(archived,replay):
    for name in archived["cases"]:
        if archived["cases"][name] is None:
            continue
        old = archived["cases"][name].pop("clock")
        new = replay["cases"][name].pop("clock")
        assert len(old)==len(new)==8
        for a,b in zip(old,new):
            z1=a.pop("direct_center"); z2=b.pop("direct_center")
            assert len(z1)==len(z2)==2
            assert abs(complex(*z1)-complex(*z2))<=1e-12
            assert all(0<=x<1e-12 for x in (a.pop("max_absolute_order_difference"),b.pop("max_absolute_order_difference")))
            assert a==b
    assert archived==replay

if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Run without -O")
    compare(*(json.loads(Path(f).read_text()) for f in sys.argv[1:]))
    print("PASS: exact reductions and both sets of fixed-grid quadratures")
