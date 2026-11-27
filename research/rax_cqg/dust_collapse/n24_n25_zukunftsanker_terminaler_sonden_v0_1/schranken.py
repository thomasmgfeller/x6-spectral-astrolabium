"""Necessary linear inequalities for a physical root on a pilot order."""
from fractions import Fraction as F
from model import COLLAR, EMPTY, WINDOW, coefficients


class Form(dict):
    """Sparse affine polynomial, with the empty string as constant term."""
    def __add__(self, other):
        if not isinstance(other, Form):
            other = Form({"": F(other)})
        result = self.copy()
        for var, value in other.items():
            result[var] = result.get(var, 0) + value
        return Form({v: c for v, c in result.items() if c})

    __radd__ = __add__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, scalar):
        return Form({v: c * scalar for v, c in self.items() if c * scalar})

    __rmul__ = __mul__


def constraints(pair, side, q, rel):
    """All rows represent L <= 0. The closure enlarges the feasible set."""
    y = [Form({f"y{i}": 1}) for i in range(25)]
    rows = {}
    def eq(name, form):
        rows[name + "+"] = form
        rows[name + "-"] = -form
    k = coefficients(rel, 25)
    for j in sorted(COLLAR):
        lo, hi = map(F, pair[side]["clock_box"][j])
        rows[f"lo{j}"] = lo - y[j]
        rows[f"hi{j}"] = y[j] - hi
    for i, j in sorted(rel):
        rows[f"order{i}_{j}"] = y[i] - y[j]
    for j in (q, 22):
        lo, hi = WINDOW
        scale = y[7] - y[3]
        rows[f"window_lo{j}"] = y[3] + scale * lo - y[j]
        rows[f"window_hi{j}"] = y[j] - y[3] - scale * hi
    for j in (21, 23, 24):
        h = sum(c * (y[j] - y[i]) for (i, end), c in k.items() if end == j)
        if j == 23:
            rows["H23_lower"] = -h
            rows["H23_upper_t"] = 9*h - (y[23] - y[22])
            rows["H23_upper_v"] = 9*h - (y[24] - y[23])
        else:
            assert not any(start == j and end not in EMPTY for start, end in rel)
            eq(f"H{j}", h)
    return rows


ACTIVE = (0, 1, 2, 3, 7, 15, 16, 17, 18, 19, 20, 22, 23, 24)


def square_key(i, j):
    return f"m{min(i,j)}_{max(i,j)}"


def moment_rows(pair, side, q, rel, intervals):
    rows = constraints(pair, side, q, rel)
    # The linear rows involving other variables are optional necessary conditions.
    active = tuple(sorted(intervals))
    names = {f"y{i}" for i in active} | {""}
    rows = {label: v for label, v in rows.items() if set(v) <= names}
    k = coefficients(rel, 25)
    y = {i: Form({f"y{i}": 1}) for i in active}
    m = {(i, j): Form({square_key(i, j): 1}) for i in active for j in active}
    def square_difference(i,j):
        return m[i,i] - 2*m[i,j] + m[j,j]
    def bounds_square(name, variable, square, l, h):
        rows[name + "sec"] = square - (l+h)*variable + l*h
        for idx, point in enumerate((l, (l+h)/2, h)):
            rows[name + f"tan{idx}"] = 2*point*variable - point*point - square
    for i in active:
        l, h = intervals[i]
        rows[f"boxlo{i}"] = l-y[i]
        rows[f"boxhi{i}"] = y[i]-h
        bounds_square(f"sq{i}", y[i], m[i,i], l, h)
        for j in active:
            if j >= i:
                continue
            a,b = intervals[j]
            z = m[i,j]
            name = f"product{i}_{j}_"
            rows[name+"ll"] = l*y[j]+a*y[i]-l*a-z
            rows[name+"hh"] = h*y[j]+b*y[i]-h*b-z
            rows[name+"hl"] = z-h*y[j]-a*y[i]+h*a
            rows[name+"lh"] = z-l*y[j]-b*y[i]+l*b
    for j in ((16,18,19,21,23,24) if 21 in active else (16,18,19,23,24)):
        d = Form({"": F(19)})
        if j not in active:
            assert j == 24 and sum(c for (i,t),c in k.items() if t==24)==0
            # H24=0 removes the linear term in Y24, and its square coefficient is zero.
            d += sum(c*m[i,i] for (i,t),c in k.items() if t==24)
            rows["D24+"] = d
            rows["D24-"] = -d
            continue
        for (i,end),c in sorted(k.items()):
            if end != j or not c:
                continue
            g = y[j]-y[i]
            l = max(0, intervals[j][0]-intervals[i][1])
            h = intervals[j][1]-intervals[i][0]
            s = square_difference(i,j)
            bounds_square(f"gap{i}_{j}", g, s, l, h)
            d += c*s
        rows[f"D{j}+"] = d
        rows[f"D{j}-"] = -d
    # H24 is identically zero, so its product with any clock is zero.
    for v in active:
        prod = sum(-c*m[i,v] for (i,j),c in k.items() if j==24)
        if 24 in active:
            prod += sum(c for (i,j),c in k.items() if j==24)*m[24,v]
        rows[f"H24_y{v}+"] = prod
        rows[f"H24_y{v}-"] = -prod
    if 21 in active:
        for v in active:
            prod = sum(c*(m[21,v]-m[i,v]) for (i,j),c in k.items() if j==21)
            rows[f"H21_y{v}+"] = prod
            rows[f"H21_y{v}-"] = -prod
    if 24 in active:
        def gaps_product(i,j,a,b):
            return m[j,b]-m[j,a]-m[i,b]+m[i,a]
        # 9 H23 (Y24-Y22) = (Y23-Y22)(Y24-Y23).
        balance = sum(9*c*gaps_product(i,23,22,24) for (i,j),c in k.items() if j==23)
        balance -= gaps_product(22,23,23,24)
        rows["paired_impulses+"] = balance
        rows["paired_impulses-"] = -balance
    return rows


def initial_boxes(pair,side, upper=8, cap_event=24):
    boxes = {i:(F(-6),F(8)) for i in ACTIVE}
    for i in set(ACTIVE)&COLLAR:
        boxes[i] = tuple(map(F,pair[side]["clock_box"][i]))
    # Every old inner clock used here lies strictly between the two collars.
    for i in set(ACTIVE)-COLLAR-{22,23,24}:
        boxes[i] = boxes[0][0],boxes[7][1]
    lo = (1-WINDOW[0])*boxes[3][0]+WINDOW[0]*boxes[7][0]
    hi = (1-WINDOW[1])*boxes[3][1]+WINDOW[1]*boxes[7][1]
    boxes[22]=(lo,hi)
    for i in (23,24):
        boxes[i]=(lo,F(upper))  # upper bound proved separately on each order
    if cap_event==23:
        del boxes[24]
    return boxes


def variable_box(v, boxes):
    if v.startswith("y"):
        return boxes[int(v[1:])]
    i,j = map(int,v[1:].split("_"))
    products = [a*b for a in boxes[i] for b in boxes[j]]
    if i==j and boxes[i][0]<=0<=boxes[i][1]:
        products.append(F(0))
    return min(products),max(products)


def margin(rows, weights, boxes=None):
    total = Form()
    for key,value in weights.items():
        value = F(value)
        assert value >= 0
        total += rows[key]*value
    c = total.pop("", F(0))
    if boxes is None:
        assert not total, total
        return c
    return c + sum(min(a*k for a in variable_box(v, boxes)) for v,k in total.items())

def with_terminal_clock(boxes,ext):
    k=coefficients(ext,25)
    coeff={i:c for (i,j),c in k.items() if j==21 and c}
    total=sum(coeff.values())
    assert total and not any(i==21 and j not in EMPTY for i,j in ext)
    numerator=[(min(c*x for x in boxes[i]),max(c*x for x in boxes[i])) for i,c in coeff.items()]
    ends=[sum(v[t] for v in numerator)/total for t in (0,1)]
    return boxes | {21:(min(ends),max(ends))}
