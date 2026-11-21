"""Independent numerical measurements in the native labels of each input."""
import numpy as np
from scipy.stats import qmc

import model


def points(settings):
    ns, nz = settings["inner_points"][-1], settings["outer_points"][-1]
    def cloud(dim, n, seed):
        assert n & (n-1) == 0
        return 2*qmc.Sobol(dim,scramble=True,seed=seed).random_base2(n.bit_length()-1)-1
    return (cloud(8,ns,settings["inner_sobol_seed"]),cloud(7,nz,settings["outer_sobol_seed"]))


def scalar_state(g):
    # Fit native rows to the inherited H3 routine's public coordinate layout.
    # Interior slots stay in native sorted order, never in the reference order.
    layout = np.empty(15, dtype=int)
    layout[model.P], layout[model.F], layout[model.I] = g.data.past, g.data.future, g.data.inside
    state = model.scalar(g.b[np.ix_(layout,layout)])
    return state, model.gram([state])[0,0].real


def amplitudes(g, u_offsets, z_offsets, radius, eta):
    """Integrate collective past density and seven xi coordinates analytically."""
    d = g.data
    inner, past, future = list(d.inside), list(d.past), list(d.future)
    e = -.25 + radius*u_offsets[:,0]
    u = np.array([float(g.centers[v]) for v in inner]) + radius*u_offsets[:,1:]
    n = len(e)
    dur = model.DELTA*(4-e)
    mass_duration = .25*dur
    dwell = np.zeros((n,7))
    for path in g.paths:
        j = [inner.index(v) for v in path]
        cuts = np.column_stack([np.zeros(n),(u[:,j[:-1]]+u[:,j[1:]])*.5,np.ones(n)])
        dwell[:,j] += np.diff(cuts,axis=1)/len(g.paths)
    y = np.zeros((n,15))
    y[:,past] = [-5.,-4.,-3.,-2.]
    y[:,past[-1]] += e
    y[:,inner] = -2+e[:,None]+(4-e[:,None])*u
    colsums = g.b.sum(axis=0)
    axis = [inner.index(v) for v in d.axes]
    values = []
    for z in z_offsets:
        y[:,future] = [2.,3.,4.,5.]
        y[:,future[1:]] += eta*z[:3]
        future_density = .125 + eta*z[3:]
        # Vectorized contraction over all sources; exact certificate separately
        # reconstructs individual ordered pairs and their interval cardinality.
        C = 1 + (y*y @ g.b - 2*y*(y @ g.b) + y*y*colsums) / 19
        ci = C[:,inner]
        shift = np.zeros_like(dwell)
        a,b,c = axis
        shift[:,axis] = (7600/8_000_000)*np.column_stack(
            [ci[:,b]-ci[:,c],ci[:,c]-ci[:,a],ci[:,a]-ci[:,b]])
        past_sum = C[:,past].sum(axis=1)
        # sinc uses sin(pi x)/(pi x). Widths below are half widths.
        phase = g.gravity - .5*(past_sum/8 + C[:,future] @ future_density)
        common = (np.exp(1j*phase)*np.sinc(past_sum/(64*np.pi))
                  *np.prod(np.sinc(.5*ci*mass_duration[:,None]*radius/np.pi),axis=1)
                  *(dur/(model.DELTA*4.25))**14)
        branches = []
        for direction in (-1,1):
            x = dwell+direction*shift
            dust = -.5*mass_duration*np.sum(ci*x,axis=1)
            branches.append(np.mean(common*np.exp(1j*dust)))
        values.append(branches)
    return np.array(values)


def evaluate(g, labels, reference_inside, clouds, sizes, radius, eta):
    inner, outer = clouds
    # Transport Sobol axes by their physical events; independently redetermine
    # the action, preparation, native coordinate sums and scalar reduction.
    physical = {labels[v]:j+1 for j,v in enumerate(reference_inside)}
    cols = [0] + [physical[v] for v in g.data.inside]
    (precision,prefactor), scalar_norm = scalar_state(g)
    probes = np.array([[0.,0.,0.],[.125,-.0625,.25],[-.25,.1875,.125]])
    phi = prefactor*np.exp(-.5*np.einsum('ni,ij,nj->n',probes,precision,probes))
    levels = []
    for ni,no in sizes:
        a = amplitudes(g, inner[:ni,cols], outer[:no], radius, eta)
        gram = (a.conj().T@a)*(scalar_norm/no)
        levels.append({'coefficients':a,'wave':a[:,:,None]*phi,'gram':gram})
    return precision,prefactor,levels


def deviation(x,y):
    return float(np.max(np.abs(x-y)))


def check_close(x,reference,tolerance):
    if not np.all(np.isfinite(x)) or not np.all(np.abs(x-reference) <= tolerance*(1+np.abs(reference))):
        raise AssertionError(f"Numeric transport discrepancy: {deviation(x,reference):.12g}")
    return deviation(x,reference)
