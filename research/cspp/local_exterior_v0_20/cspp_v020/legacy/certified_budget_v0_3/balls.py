"""Bounded FLINT computations. Decisions use balls, never display floats."""
import json
from pathlib import Path
from flint import arb, acb, ctx

HERE = Path(__file__).resolve().parent
def plan():
    return json.loads((HERE / 'PROTOCOL.json').read_text())

def integrate(f, a, b):
    p = plan()
    value = acb.integral(f, a, b,
        abs_tol=arb(p['integration_abs_tol']), rel_tol=arb(p['integration_rel_tol']),
        eval_limit=p['integration_eval_limit'], depth_limit=100)
    if not value.is_finite():
        raise ArithmeticError('QUADRATURE_HOLD: non-finite enclosure')
    return value

def inflate(z, error):
    """A disk error is enclosed by a rectangle, without shrinking either side."""
    z = acb(z)
    e = arb(0, arb(error).abs_upper())
    return z + acb(e, e)

def real_value(z):
    if not z.imag.contains(0):
        raise ArithmeticError('real integral excludes zero imaginary part')
    return z.real

def encode(z):
    z = acb(z)
    if not z.is_finite():
        raise ArithmeticError('cannot serialize non-finite certificate')
    re, im = z.real.str(45, more=True), z.imag.str(45, more=True)
    if not arb(re).contains(z.real) or not arb(im).contains(z.imag):
        raise ArithmeticError('decimal serialization lost enclosure')
    return {'real_ball': re, 'imag_ball': im,
            'display_midpoint': [float(z.real.mid()), float(z.imag.mid())],
            'display_radius': [float(z.real.rad()), float(z.imag.rad())]}

def decode(d):
    return acb(arb(d['real_ball']), arb(d['imag_ball']))

def ceil_upper(x):
    return int(arb(x).upper().ceil().unique_fmpz())

def configure(bits=None):
    ctx.prec = plan()['precision_bits'] if bits is None else bits

def write(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
