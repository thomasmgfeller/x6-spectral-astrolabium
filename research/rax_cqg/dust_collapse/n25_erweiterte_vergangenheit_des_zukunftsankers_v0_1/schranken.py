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
    if (21,24) in rel:
        coeff={i:c for (i,j),c in k.items() if j==21 and c}
        A=abs(sum(coeff.values()))
        assert A>0
        M={}
        for i in coeff:
            if i in COLLAR:
                interval=pair[side]["clock_box"][i]
            else:
                assert (0,i) in rel and (i,7) in rel
                interval=(pair[side]["clock_box"][0][0],pair[side]["clock_box"][7][1])
            M[i]=max(abs(F(value)) for value in interval)
        cap=1+max(2*sum(abs(c)*M[i] for i,c in coeff.items()),
                  19+sum(abs(c)*M[i]**2 for i,c in coeff.items()))/A
        rows["D21_cauchy_upper"]=y[21]-cap
    for j in (21, 23, 24):
        h = sum(c * (y[j] - y[i]) for (i, end), c in k.items() if end == j)
        if j == 21 and not terminal_21(rel):
            # From G21 and the ratio fixed by G22, with w21,w23,w24 > 0.
            if (21,23) not in rel:
                assert k[21,24]==1
                rows["H21_new_positive"] = -h
            elif (21,22) in rel:
                assert (k[21,23],k[21,24])==(-9,16)
                rows["H21_new_negative"] = h
            continue
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
    density = [j for j in (4,5,6,16,18,19,21,23) if j in active]
    if 23 in active:
        density.append(24)
    for j in density:
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
    for v in (active if 23 in active else ()):
        prod = sum(-c*m[i,v] for (i,j),c in k.items() if j==24)
        if 24 in active:
            prod += sum(c for (i,j),c in k.items() if j==24)*m[24,v]
        rows[f"H24_y{v}+"] = prod
        rows[f"H24_y{v}-"] = -prod
    if 21 in active and terminal_21(rel):
        for v in active:
            prod = sum(c*(m[21,v]-m[i,v]) for (i,j),c in k.items() if j==21)
            rows[f"H21_y{v}+"] = prod
            rows[f"H21_y{v}-"] = -prod
    if 21 in active and (21,23) in rel and (21,22) not in rel:
        assert (k[21,23],k[21,24])==(1,-9)
        # w21 H21 = w23 v (Y22-Y21)/(t+v).
        product = sum(c*((m[21,22]-m[21,21])-(m[i,22]-m[i,21]))
                      for (i,j),c in k.items() if j==21 and c)
        rows["H21_new_middle"] = -product
    if 24 in active:
        def gaps_product(i,j,a,b):
            return m[j,b]-m[j,a]-m[i,b]+m[i,a]
        # 9 H23 (Y24-Y22) = (Y23-Y22)(Y24-Y23).
        balance = sum(9*c*gaps_product(i,23,22,24) for (i,j),c in k.items() if j==23)
        balance -= gaps_product(22,23,23,24)
        rows["paired_impulses+"] = balance
        rows["paired_impulses-"] = -balance
    if 23 not in active:
        assert 24 not in active
        add_projected_rows(rows,k,y,m)
    return rows


def add_projected_rows(rows,k,y,m):
    # These identities eliminate two potentially unbounded successor clocks.
    first={i:c for (i,j),c in k.items() if j==23 and c}
    last={i:c for (i,j),c in k.items() if j==24 and i!=23 and c}
    assert sum(first.values())==sum(last.values())==0 and k[23,24]==1
    h={i:-c for i,c in first.items()}
    v=last
    def linear(coeff):
        return sum(c*y[i] for i,c in coeff.items())
    def product(u,v):
        return sum(a*b*m[i,j] for i,a in u.items() for j,b in v.items())
    def centered(coeff):
        return 19+sum(c*(m[22,22]-2*m[22,i]+m[i,i]) for i,c in coeff.items())
    a=centered(first)
    b=centered(last)-product(v,v)
    rows["proj_H"]=-linear(h)
    rows["proj_V"]=9*linear(h)-linear(v)
    rows["proj_D23"]=a
    rows["proj_D24"]=-b
    poly=b+9*a-18*product(h,v)
    rows["proj_balance+"]=poly
    rows["proj_balance-"]=-poly


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
    if cap_event is None:
        del boxes[23],boxes[24]
        return boxes
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

def terminal_21(rel):
    return not any(i == 21 and j not in EMPTY for i,j in rel)


def initial_order_boxes(pair,side,upper,event,rel,use_terminal):
    boxes=initial_boxes(pair,side,upper,event)
    for i in range(22):
        if (i,24) not in rel or i in boxes or i==21:
            continue
        assert (0,i) in rel and (i,7) in rel
        boxes[i]=boxes[0][0],boxes[7][1]
    if use_terminal:
        assert terminal_21(rel)
        return with_terminal_clock(boxes,rel)
    if (21,24) in rel:
        # Positive interior 21 still obeys D21=0. In A x² - 2B x + C
        # Cauchy's bound holds for every root even without stationarity of its clock.
        coeff={i:c for (i,j),c in coefficients(rel,25).items() if j==21 and c}
        a=abs(sum(coeff.values()))
        assert a>0 and (0,21) in rel
        m={i:max(abs(z) for z in boxes[i]) for i in coeff}
        b=sum(abs(c)*m[i] for i,c in coeff.items())
        d=19+sum(abs(c)*m[i]**2 for i,c in coeff.items())
        radius=1+max(2*b,d)/a
        hi=min([radius]+[boxes[j][1] for j in (23,24) if j in boxes and (21,j) in rel])
        boxes[21]=boxes[0][0],hi
    return boxes
