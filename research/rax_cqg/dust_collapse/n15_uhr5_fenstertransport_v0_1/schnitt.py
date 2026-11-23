"""Direkte Matrix-, Wirkungs- und Quadraturprüfungen für alle 16 Uhrpakete."""
import argparse
import json
from math import pi
import numpy as np
from numpy.polynomial.legendre import leggauss
from fenster import EDGES, INNER, ORDER, ROOT, SRC

K = 3.75
D = K*(3/722)**.25
d = 1/(36*D*K**2)
h = 1/16384
theta = (225*(d/2)**2/608-32331/38912)/(72*K**2)
rails = np.arange(-7,9)
code = np.eye(16,dtype=complex)[:,7:9]
ident = np.eye(16)


def projections(matrix):
    return [(ident+sign*matrix)/2 for sign in (1,-1)]


def matrices(method):
    forward = np.diag(np.ones(15),-1)*1j*np.exp(1j*theta)
    gen = forward+forward.conj().T
    k = np.arange(1,17)
    if method=="gauss":
        lam,v = np.linalg.eigh(gen)
        limited = (v*np.sign(lam)) @ v.conj().T
        delta = rails[:,None]-rails[None,:]
        cropped = np.zeros((16,16),complex)
        odd = delta%2!=0
        cropped[odd] = 2j*np.exp(1j*delta[odd]*theta)/(pi*delta[odd])
    else:
        phase = (1j*np.exp(1j*theta))**np.arange(16)
        modes = phase[:,None]*np.sqrt(2/17)*np.sin(k[:,None]*k[None,:]*pi/17)
        limited = (modes*np.sign(np.cos(k*pi/17))) @ modes.conj().T
        # Fourier integrate a single positive half-period; negative part follows
        # by subtracting from identity. Degree of the exponential is at most 15.
        n,w = leggauss(56)
        q = theta+(n+1)*pi/2
        waves = np.exp(1j*rails[:,None]*q)
        cropped = 2*(waves*(w/4))@waves.conj().T-ident
    return gen,limited,cropped


def projector_onto(columns):
    q,_ = np.linalg.qr(columns,mode="reduced")
    return q @ q.conj().T


def records():
    gen,limited,crop = matrices("gauss")
    _,ref_l,ref_c = matrices("cc")
    assert np.max(abs(limited-ref_l))<5e-14 and np.max(abs(crop-ref_c))<5e-14
    assert np.max(abs(limited@limited-ident))<5e-14
    assert np.min(abs(np.linalg.eigvalsh(gen)))>.18
    c = (8/pi**2)*sum(1/k**2 for k in (1,3,5,7))
    b = crop@code
    j = b/np.sqrt(c)
    interior = [m@code for m in projections(crop)]
    optimal = [projector_onto(code+sign*j) for sign in (1,-1)]
    assert np.max(abs(optimal[0]@optimal[1]))<1e-13
    assert np.max(abs(b.conj().T@b-c*np.eye(2)))<2e-14
    assert np.max(abs(interior[0].conj().T@interior[1]-(1-c)*np.eye(2)/4))<1e-14
    closed = [m@code for m in projections(limited)]
    direct = projections(crop)
    stats = {}
    for label,instrument,second in (("line_same",interior,direct),("line_best",interior,optimal),
                                    ("closed_same",closed,projections(limited))):
        bad = sum(a.conj().T @ e @ a for a,e in zip(instrument,reversed(second)))
        total = sum(a.conj().T @ a for a in instrument)
        error = np.trace(bad).real/np.trace(total).real
        assert np.max(abs(bad-error*total))<2e-14
        assert error>=-1e-13
        stats[label] = float(max(0.,error))
    # Build a concrete three-outcome measurement on the four-dimensional span.
    # Both hypotheses share the *same* unknown failure vector.
    ell=(1-c)/2
    from_block=np.column_stack(interior)
    targets=[]
    for i,a in enumerate(interior):
        eig,vec=np.linalg.eigh(a.conj().T@a-ell*np.eye(2)/2)
        assert np.min(eig)>0
        target=np.zeros((6,2),complex)
        target[2*i:2*i+2]=(vec*np.sqrt(eig))@vec.conj().T
        target[4:]=np.sqrt(ell/2)*np.eye(2)
        targets.append(target)
    to_block=np.column_stack(targets)
    assert np.max(abs(to_block.conj().T@to_block-from_block.conj().T@from_block))<1e-14
    reader=to_block@np.linalg.pinv(from_block)
    assert np.max(abs(reader.conj().T@reader-projector_onto(from_block)))<2e-14
    for i,a in enumerate(interior):
        result=reader@a
        other=1-i
        assert np.max(abs(result[2*other:2*other+2]))<2e-14
        assert np.max(abs(result[4:].conj().T@result[4:]-ell*np.eye(2)/2))<1e-14
    # Four preparations at fixed rails. All native diagonal effects are phase blind.
    phases = (0,pi/2,pi,3*pi/2)
    plus = projections(limited)[0]
    p = []
    for alpha in phases:
        v = code @ np.array([1,np.exp(1j*alpha)])/np.sqrt(2)
        p.append(float((v.conj()@plus@v).real))
    element = np.hypot(p[0]-p[2],p[1]-p[3])/2
    assert abs(element-abs(plus[7,8]))<2e-14
    return {"wrong_given_accepted":stats, "unambiguous_conclusive_per_input":c,"four_phases":p,"absolute_early_matrix_element":element}


def rule(method):
    if method=="gauss":
        x,w = leggauss(20)
        return x,w/2
    k = np.arange(21)
    x = np.cos(k*pi/20)
    moments = np.zeros(21)
    moments[::2] = 1/(1-k[::2]**2)
    return x,np.linalg.solve(np.cos(k[:,None]*np.arccos(x)),moments)


def phase_factor(method,centre,radius,coefficient):
    if method=="gauss":
        return np.exp(1j*centre*coefficient)*np.sinc(radius*coefficient/pi)
    x,w = leggauss(8)
    return sum(wi/2*np.exp(1j*(centre+xi*radius)*coefficient) for xi,wi in zip(x,w))


def columns(method,u,pulse):
    y = {j:float(j-5) for j in ORDER[:4]}
    y[3] += .25
    y.update({j:y[3]+K*a for j,a in zip(INNER,u)})
    shift = pulse/(8*np.sqrt(D))
    c = {}
    for k,jj in enumerate(ORDER[:ORDER.index(13)+1]):
        if method=="gauss":
            c[jj] = -.5-sum(weight*(y[jj]-y[ORDER[k-lag]]-
                           (shift if ORDER[k-lag]==6 and jj in (12,13) else 0))**2/38
                           for lag,weight in enumerate((1,-9,16,-8),1) if k>=lag)
        else:
            c[jj] = -.5-sum(weight*(y[jj]-y[i])**2/38 for (i,j),weight in EDGES.items() if j==jj)
            if jj in (12,13):
                c[jj] += EDGES[6,jj]*shift*(2*(y[jj]-y[6])-shift)/38
    return c


def outgoing(method,pulse):
    q,w = rule(method)
    z,t = q[:,None]/64,h*q[None,:]
    weights = w[:,None]*w[None,:]
    prefix = {-1:[],1:[]}
    suffix = []
    for n in rails:
        u = [1/8+z, 1/4+(n-.5)*d+t,3/8,1/2,5/8,3/4,7/8]
        c = columns(method,u,pulse)
        faces = [0]+[(l+r)/2 for l,r in zip(u,u[1:])]+[1]
        f = dict(zip(INNER,[r-l for l,r in zip(faces,faces[1:])]))
        if n in (0,1):
            amp = 1
            for j in (4,5,6):
                amp = amp*f[j]*phase_factor(method,D*f[j],D*f[j]/100,c[j])
            for mark in (-1,1):
                prefix[mark].append(amp*phase_factor(method,1/8+mark/2048,h,D*c[11]))
        suffix.append(f[12]*phase_factor(method,D*f[12],D*f[12]/100,c[12])*np.exp(1j*D*c[13]/8))
    _,limited,crop = matrices(method)
    sets = {"no_meter":[code], "line_window":[v@code for v in projections(crop)],
            "closed_window":[v@code for v in projections(limited)]}
    old = json.loads((SRC/"nullausgang.json").read_text())
    out = {}
    for label,ops in sets.items():
        balances = []
        for mark in (-1,1):
            # Order of contractions is deliberately different in the two evaluations.
            if method=="gauss":
                transfer = np.einsum("ntz,itz,tz->ni",suffix,prefix[mark],weights)
                rows = [np.sum(transfer*op,axis=0) for op in ops]
            else:
                rows = []
                for op in ops:
                    measured = np.asarray(suffix)[:,None,:,:]*op[:,:,None,None]
                    rows.append(np.sum(measured*np.asarray(prefix[mark])[None,:,:,:]*weights,axis=(0,2,3)))
            intens = [sum(abs(a[0]+phase*a[1])**2 for a in rows) for phase in (-1j,1j)]
            if label=="no_meter":
                collar = sum(c[j] for j in ORDER[:4])
                for rho in (.125,.25):
                    common = abs(np.exp(1j*collar*rho)*np.sinc(collar/(32*pi)))**2
                    ref = old["gauss20"][f"{pulse}|{rho}"]["intensities_common_scale"][str(mark)]
                    assert np.max(abs(np.asarray(intens)*common-ref))<4e-19
            balances.append((intens[0]-intens[1])/sum(intens))
        out[label] = float(balances[1]-balances[0])
    return out


def integration_check():
    q,w = leggauss(12)
    ww = w[:,None]*w[None,:]/4
    z = q[:,None]/64
    _,limited,crop = matrices("gauss")
    tests = 0
    err = 0.
    for u12 in (5/8-1/1024,5/8+1/1024):
        x = ((u12-3/8)/2)*(1+.01*q[None,:])
        for t in (-h,.29*h,h):
            u5 = .25+(rails-.5)*d+t
            for x12 in (.125,.1255):
                u_phase = np.exp(-1j*16*D*x12*K**2*(u12-u5)**2/38)
                for pulse in (-1,0,1):
                    # Integrate over the forgotten u4 and x11. A sample input need
                    # not be separable in the input rail and the forgotten variables.
                    past = np.stack([1+8*z+1j*x,.35+np.exp(9j*z)*(x+.2)])
                    c_common = (-.5+8*K**2*(u12-.125-z)**2/38
                                +9*(K*(u12-.375)-pulse/(8*np.sqrt(D)))**2/38
                                -K**2*(u12-.5)**2/38)
                    common = np.exp(1j*D*x12*c_common)*ww
                    reduced = np.sum(past*common,axis=(1,2))
                    for m in (limited,crop):
                        for sign in (-1,1):
                            op = ((ident+sign*m)/2)@code
                            measured = np.einsum("ni,izx->nzx",op,past)
                            actual = []
                            for idx,v5 in enumerate(u5):
                                u = [.125+z,v5,.375,.5,u12,.75,.875]
                                c = columns("gauss",u,pulse)
                                actual.append(np.sum(ww*np.exp(1j*D*x12*c[12])*measured[idx]))
                            prediction = u_phase*(op@reduced)
                            err = max(err,float(np.max(abs(actual-prediction))))
                            tests += 1
    assert err<2e-14
    return {"cases":tests,"max_absolute_residual":err}


def run():
    r = records()
    r["sewing"] = integration_check()
    r["late_contrast"] = {m:{str(p):outgoing(m,p) for p in (0,1,-1)} for m in ("gauss","cc")}
    for p,row in r["late_contrast"]["gauss"].items():
        assert max(abs(v-r["late_contrast"]["cc"][p][k]) for k,v in row.items()) < 2e-14
    ref = json.loads((SRC/"auslese.json").read_text())["gauss"]
    ratio = 2*r["absolute_early_matrix_element"]/(2/pi)
    r["closed_success_equal_priors"] = .5+ratio*(ref["success_equal_priors"]-.5)
    return r


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json",action="store_true")
    opt = parser.parse_args()
    result = run()
    if opt.json:
        print(json.dumps(result,indent=2))
    else:
        copy = json.loads((ROOT/"schnitt.json").read_text())
        for method,parts in result["late_contrast"].items():
            for p,row in parts.items():
                for k,v in row.items():
                    assert abs(v-copy["late_contrast"][method][p][k])<2e-14
        print("PASS · Vier Phasen, beide Wiederholungsmessungen, 144 Verklebungen und später Kontrast")
