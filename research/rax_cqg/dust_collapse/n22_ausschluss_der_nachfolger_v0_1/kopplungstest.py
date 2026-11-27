"""Test each dust clock separately in the compiled 11 stationarity conditions."""
from fractions import Fraction
import subprocess

from staubuhren import DUST_ORDER, SCALE


def check(binary, header, coefficients):
    # In a directed dust-to-device edge i -> j, only D_j and G_j among these
    # residuals depend on Y_i. Shifting that clock checks the individual edge,
    # even when two or more dust clocks have equal values on a physical branch.
    clocks = tuple(range(15, 22))
    positive = (16, 18, 19, 21)
    y = {j: (j-17) * SCALE//8 for j in clocks}
    w = {j: (n+1) * SCALE//16 for n, j in enumerate(positive)}
    fields = [y[j] for j in clocks] + [w[j] for j in positive]
    lines = header.splitlines()
    start = 1 + int(lines[0]) + 8
    step = SCALE // 4

    def values(shift_node):
        payload = lines.copy()
        for offset, j in enumerate(DUST_ORDER):
            val = step if j == shift_node else 0
            payload[start+offset] = f'{j} {val} {val}'
        payload += [f'{x} {x}' for x in fields]
        proc = subprocess.run([str(binary), '0', '1', '0', 'algebra'],
                              input='\n'.join(payload)+'\n', capture_output=True, text=True, check=True)
        return [tuple(map(int, row.split()[:2])) for row in proc.stdout.splitlines()]

    baseline = values(None)
    assert len(baseline) == len(positive) + len(clocks)
    comparisons = 0
    for i in DUST_ORDER:
        trial = values(i)
        assert len(trial) == len(baseline)
        expected = [Fraction(coefficients.get((i,j),0) * (step**2 - 2*y[j]*step), SCALE)
                    for j in positive]
        expected += [Fraction(coefficients.get((i,j),0) * w.get(j,0) * step, SCALE)
                     for j in clocks]
        for ref, new, delta in zip(baseline, trial, expected):
            lo, hi = new[0]-ref[1], new[1]-ref[0]
            assert lo <= delta <= hi, (i, ref, new, delta)
            comparisons += 1
    return comparisons
