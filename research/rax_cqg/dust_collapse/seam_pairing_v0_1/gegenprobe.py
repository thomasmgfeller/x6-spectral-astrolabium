"""Unabhängiger numerischer Vergleich mit NumPy, ohne Import des Hauptrechners."""
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss
from numpy.polynomial.legendre import leggauss

ROOT = Path(__file__).resolve().parent
B = 4/np.sqrt(6)
hist = json.loads((ROOT.parent/"amplitude_existence_v0_1/inputs/aa_hessians.json").read_text())["histories"]
ref = json.loads((ROOT/"ergebnis.json").read_text())
ref_fold = ref["identity_fold"]


def check(value, target, tol, label):
    if not abs(value-target) <= tol:
        raise ValueError(f"{label}: {value} / {target}")


def poset(code):
    return {(i,j) for i in range(5) for j in range(5) if (code >> (i*5+j)) & 1}


def full_action(code1, code2):
    relations = poset(code1) | {(i+3,j+3) for i,j in poset(code2)}
    indirect = {(i,k) for i,j in relations for v,k in relations if j==v}
    while not indirect.issubset(relations):
        relations.update(indirect)
        indirect = {(i,k) for i,j in relations for v,k in relations if j==v}
    h = np.zeros((8,8))
    f4 = 8
    for i,j in relations:
        count = sum((i,k) in relations and (k,j) in relations for k in range(8))
        factor = (1,-9,16,-8)[count] if count<4 else 0
        v = np.zeros(8)
        v[i],v[j] = 1,-1
        h -= factor*np.outer(v,v)/2
        f4 -= factor
    return f4,h


def forward_check():
    rows = ref["extended_sewing_fixed_record"]["partial_amplitudes"]
    maxerr = 0
    for record in rows:
        total = 0j
        for h in hist:
            f4, mat = full_action(record["left"],h["order_code"])
            mat = np.diag([1,1,0,0,0,0,1,1])-1j*B*mat
            ev = np.linalg.eigvals(mat)
            if np.any(ev.real < -1e-10) or np.min(abs(ev))<1e-10:
                raise ValueError("Zweig der Eigenwertwurzel")
            total += math.pi**3/8*np.exp(1j*f4)/np.prod(np.sqrt(ev))/1089
        maxerr = max(maxerr,abs(total-complex(*map(float,record["complex"]))))
    check(maxerr,0,1e-13,"33 Zwischenrandamplituden aus globalen Ordnungen")
    return maxerr


def atom_fields(x, y):
    from fractions import Fraction
    field = np.stack([x.ravel(),y.ravel()],axis=0)
    total = np.zeros((2,field.shape[1]),dtype=complex)
    for h in hist:
        raw = np.array([[float(Fraction(t)) for t in row] for row in h["H0_over_va"]])
        inds = [0,1,3,4]
        hess = B*(raw[np.ix_(inds,inds)]-np.outer(raw[inds,2],raw[2,inds])/raw[2,2])
        left, cross, right = hess[:2,:2],hess[:2,2:],hess[2:,2:]
        a = np.eye(2)-1j*left
        s = cross.T@np.linalg.solve(a,cross)-1j*right
        n = (2*math.sqrt(math.pi)*np.sqrt(2*math.pi/(-B*raw[2,2]))*np.exp(-1j*math.pi/4)
             /np.prod(np.sqrt(1-1j*np.linalg.eigvalsh(left))))
        total[h["p"]-1] += np.exp(1j*h["F4"])*n/264*np.exp(-np.sum(field*(s@field),axis=0)/2)
    return total


def dust_grid():
    x,w = leggauss(20)
    x,w = (x+1)/2,w/2
    def chi(k):
        return (1+np.exp(-.5j*k)*np.sinc(k/(2*math.pi)))/2
    res = []
    for u,weight in zip(x/8,w/8):
        v = B*(x-u)**2
        z1 = np.sum(w*chi(.5+v))
        z2 = np.sum(w[:,None]*w[None,:]*chi(.5+v[:,None]+v[None,:]))
        res.append((weight,z1,z2))
    return res


def fresnel_check(zvalues):
    # Independent factorization in the symmetric/antisymmetric field axes.
    s = np.ones(2)/np.sqrt(2)
    def axial(left,cross,right,c,f4):
        a = np.eye(2)-1j*B*left
        prefactor = (2*np.sqrt(math.pi)*np.sqrt(2*math.pi/(B*c))
                     *np.exp(1j*(f4-math.pi/4))
                     /np.prod(np.sqrt(1-1j*B*np.linalg.eigvalsh(left)))/264)
        decay = s@(B**2*cross.T@np.linalg.solve(a,cross)-1j*B*right)@s
        return prefactor,decay
    a,k = axial(np.diag([26/3,-1]),np.array([[-13/3,-13/3],[.5,.5]]),
                np.array([[11/3,1/6],[1/6,11/3]]),1.5,18)
    mat = np.array([[69,1],[1,69]])/8
    b,l = axial(mat,-35*np.ones((2,2))/8,mat,2,37)
    time = sum(w*z1.conjugate()*z2 for w,z1,z2 in zvalues)
    value = (a.conjugate()*b*time*np.sqrt(2*math.pi/(k.conjugate()+l))
             *np.sqrt(math.pi/(-1j*5*B/2)))
    example = ref_fold["finite_part_example_in_clock_window"]
    check(value,complex(*map(float,example["cross"])),1e-16,"Fresnel-Kreuzterm")
    check(-abs(value)**2,float(example["two_by_two_determinant"]),1e-22,"Determinante")


def folded_check():
    zvalues = dust_grid()
    fresnel_check(zvalues)
    coeffs = [9/69185,9/12871,9/1423450]
    density = 8*math.pi**2.5/(B*264**2)*sum(
        w*(4*math.sqrt(coeffs[1])*abs(z1)**2
           +(2*math.sqrt(coeffs[0])+math.sqrt(coeffs[2]))*abs(z2)**2)
        for w,z1,z2 in zvalues)
    check(density,float(ref_fold["atom_fold_leading_density"]),1e-14,"Längendichte")
    maxerr = 0
    for eps in (4,8):
        nodes, weights = hermgauss(110)
        x,y = np.meshgrid(nodes/np.sqrt(eps),nodes/np.sqrt(eps),indexing="ij")
        v1,v2 = atom_fields(x,y)
        w = np.outer(weights,weights).ravel()/eps
        weight = sum(du*np.dot(w,abs(z1*v1+z2*v2)**2) for du,z1,z2 in zvalues)
        target = float(ref_fold["direct_quadrature_controls"][str(eps)])
        maxerr = max(maxerr,abs(target-weight))
    check(maxerr,0,2e-13,"Direkte Quadratur des gemeinsamen Feldes")
    return maxerr


if __name__=="__main__":
    print("Maximaler Fehler, 33 Vorwärtsamplituden:", format(forward_check(),".3g"))
    print("Maximaler Fehler, zwei gemeinsame Feldintegrale:",format(folded_check(),".3g"))
