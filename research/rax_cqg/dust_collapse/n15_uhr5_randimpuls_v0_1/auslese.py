"""Zwei Auswertungen der Dichteauslese und direkte Fourier-Spektralkontrolle."""
import argparse
import json
from math import pi
import numpy as np
from numpy.polynomial.legendre import leggauss
from pruefen import ROOT, ORDER, EDGES, INNER, reduced_phase

K = 3.75
D = K*(3/722)**.25
s = 1/(72*D*K*K)
h = 1/16384
theta = float(reduced_phase(0,0,s))/(72*K**2)


def rule(n, method):
    if method == "gauss":
        v,w = leggauss(n)
        return v,w/2
    k = np.arange(n)
    v = np.cos(k*pi/(n-1))
    moments = np.zeros(n)
    moments[::2] = 1/(1-k[::2]**2)
    return v, np.linalg.solve(np.cos(np.outer(k,np.arccos(v))), moments)


def arm(z, t, sign, method):
    u = [1/8+z, 1/4+t+sign*s, 3/8, 1/2, 5/8, 3/4, 7/8]
    y = {j:float(j-5) for j in ORDER[:4]}
    y[3] += .25
    y.update({j:y[3]+K*v for j,v in zip(INNER,u)})
    faces = [0]+[(a+b)/2 for a,b in zip(u,u[1:])]+[1]
    f = {j: right-left for j,left,right in zip(INNER,faces,faces[1:])}
    c = {}
    for j in (4,5,6,11):
        if method == "gauss":
            c[j] = -.5-sum(b*(y[j]-y[i])**2/38 for (i,k),b in EDGES.items() if j==k)
        else:
            k = ORDER.index(j)
            c[j] = -.5-sum(b*(y[j]-y[ORDER[k-lag]])**2/38
                            for lag,b in enumerate((1,-9,16,-8),1))
    amp = 1
    for j in (4,5,6):
        a = D*f[j]*c[j]
        if method == "gauss":
            factor = np.exp(1j*a)*np.sinc(a/(100*pi))
        else:
            v,w = leggauss(7)
            factor = sum(wi/2*np.exp(1j*a*(1+vi/100)) for vi,wi in zip(v,w))
        amp = amp*f[j]*factor
    return amp, D*c[11]


def readout(method):
    v,w = rule(20 if method=="gauss" else 21, method)
    z,t = v[:,None]/64, v[None,:]*h
    weight = w[:,None]*w[None,:]
    am,gm = arm(z,t,-1,method)
    ap,gp = arm(z,t,1,method)
    norm = np.sum(weight*(abs(am)**2+abs(ap)**2))
    means, probabilities = [], []
    for mark in (-1,1):
        xc = 1/8+mark/2048
        if method=="gauss":
            slope = -4*(.25-t)/304
            cross = am.conjugate()*ap*np.exp(1j*slope*xc)*np.sinc(h*slope/pi)
        else:
            v,w = leggauss(9)
            cross = sum(wi/2*(am*np.exp(1j*gm*(xc+vi*h))).conjugate()
                        *(ap*np.exp(1j*gp*(xc+vi*h))) for vi,wi in zip(v,w))
        c = np.sum(weight*cross)/norm
        means.append(c)
        if method=="gauss":
            prob = .5+2/pi*np.imag(c*np.exp(-1j*theta))
        else:
            # Integrate the normalized phase density over theta < q < theta+pi.
            q,w = leggauss(14)
            angle = theta+(q+1)*pi/2
            prob = np.sum(w*(1+2*np.real(c*np.exp(-1j*angle))))/4
        probabilities.append(float(prob))
    diff = means[0]-means[1]
    return {"p_plus_low":probabilities[0], "p_plus_high":probabilities[1],
            "success_equal_priors":(1+probabilities[0]-probabilities[1])/2,
            "optimal_success_if_entire_modular_phase_used":float(.5+abs(diff)/pi)}


def spectrum_test():
    # Continuous momentum. A normalized triangular packet is used solely to bound
    # the high-frequency tail. It has the same two supports as the actual prefix.
    d = 2*s
    v,w = leggauss(18)
    stop = 2048
    # Bound of squared envelope and two coherent arms: <= 24/(pi*h^3*p^4).
    pmin = (stop*pi-2*pi)/d
    tail = 16/(pi*h**3*pmin**3)
    assert tail < 1e-6
    phases = (0., pi/2, -pi/2, .77)
    errors = []
    for alpha in phases:
        positive = norm = incoherent = 0.
        for k in range(-stop,stop):
            q = theta+(k+(v+1)/2)*pi
            p = q/d
            # |FT of sqrt(3/(2h)) * (1-|u|/h)_+|^2, unitary transform.
            base = 3*h/(4*pi)*np.sinc(h*p/(2*pi))**4
            scale = w*pi/(2*d)
            prob = np.sum(scale*base*(1+np.cos(alpha-q)))
            norm += prob
            if k%2==0:
                positive += prob
                incoherent += np.sum(scale*base)
        theory = .5+np.sin(alpha-theta)/pi
        err = max(abs(positive-theory), abs(norm-1), abs(incoherent-.5))
        assert err < tail+2e-12
        errors.append(float(err))
    return {"phase_preparations":len(phases),"half_periods":2*stop,
            "analytic_tail_upper":tail,"max_abs_error_including_negative_control":max(errors)}


def controls():
    # Ancilla operations can vary between the retained rails. Outcomes on the
    # ancilla alone add probabilities because the rail supports are disjoint.
    detector = np.array([[1, 2j], [2j, 1]], complex)/np.sqrt(5)
    rotations = (np.array([[3,4],[-4,3]],complex)/5,
                 np.array([[5,12j],[12j,5]],complex)/13)
    states = [detector @ u @ np.array([1,0]) for u in rotations]
    native, ideal = [], []
    for phase in (theta+pi/2, theta-pi/2):
        amplitudes = np.array([states[0], np.exp(1j*phase)*states[1]])/np.sqrt(2)
        native.append(float(np.sum(abs(amplitudes[:,0])**2)))
        ideal.append((1+np.sin(phase-theta))/2)
    assert abs(native[0]-native[1])<1e-14 and abs(ideal[0]-ideal[1]-1)<1e-14

    # Fourier coefficients of sign(sin(q-theta)). Translate a concrete state into
    # its disjoint copied windows and sum squared norms outside the two old rails.
    v = np.array([.6, .8j])
    indices = np.arange(-16383,16384)
    def coeff(n):
        odd = np.abs(n)%2==1
        out = np.zeros(len(n),complex)
        out[odd] = 2j*np.exp(1j*n[odd]*theta)/(pi*n[odd])
        return out
    kicked = coeff(indices)*v[0]+coeff(indices-1)*v[1]
    leakage = float(.5*np.sum(abs(kicked[(indices!=0)&(indices!=1)])**2))
    theory = (1-4/pi**2)/2
    assert 0 < theory-leakage < 1e-4
    return {"native_difference":native[0]-native[1],"ideal_difference":ideal[0]-ideal[1],
            "finite_sum_leakage_lower":leakage,"omitted_leakage":theory-leakage}


def run():
    a,b = readout("gauss"),readout("cc")
    assert max(abs(a[k]-b[k]) for k in a) < 2e-14
    assert a["p_plus_low"]>a["p_plus_high"]
    return {"gauss":a, "clenshaw_curtis":b,"independent_fourier_integral":spectrum_test(), "instrument_controls":controls()}


if __name__=="__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json",action="store_true")
    args = p.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out,indent=2))
    else:
        old = json.loads((ROOT/"auslese.json").read_text())
        for key in ("gauss","clenshaw_curtis"):
            assert all(abs(val-old[key][k])<2e-13 for k,val in out[key].items())
        from fractions import Fraction
        interval = json.loads((ROOT/"exakt.json").read_text())["tag_certificate"]["success_equal_priors"]
        lo, hi = (float(Fraction(v)) for v in interval)
        assert lo <= out["gauss"]["success_equal_priors"] <= hi
        print("PASS · Dichteauslese in zwei Rechnungen und direkte Fourier-Integration mit Negativkontrolle")
