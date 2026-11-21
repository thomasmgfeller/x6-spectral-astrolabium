"""Independent numerical double integral. Histories share only the future endpoint."""
import json
import math

import numpy as np
from scipy.stats import qmc

import zertifikat as cert

P,I,F = map(list,(cert.P,cert.I,cert.F))
DELTA = (3/722)**0.25


def phase(points, external, center):
    # 16 earlier coordinates: past offset, seven raw Y, seven raw W, common r.
    cy,cw = center
    n = len(points)
    y = np.tile([float(cy[j]) for j in range(15)],(n,1))
    w = np.empty((n,15))
    r = float(cert.RADIUS)
    y[:,3] += r*points[:,0]
    y[:,I] += r*points[:,1:8]
    y[:,F[1:]] += float(cert.H)*external[:,:3]
    w[:,P] = 0.125+points[:,15:16]/32
    w[:,I] = DELTA*(np.array([float(cw[j]) for j in I])+r*points[:,8:15])
    w[:,F] = 0.125+float(cert.H)*external[:,3:7]
    # Reference arm is always the lower half, signal arm uses w7+h.
    w[:,7] = 0.125 + float(cert.H)*(external[:,3]-1)/2
    action = -w.sum(axis=1)/2
    slope = np.full(n,-0.5)
    for i,j in sorted(cert.ORDER):
        count = sum((i,v) in cert.ORDER and (v,j) in cert.ORDER for v in range(15))
        if count>=4:
            continue
        term = -(1,-9,16,-8)[count]*(y[:,i]-y[:,j])**2/38
        action += w[:,j]*term
        if j==7:
            slope += term
    return action,slope


def estimate(points,center,ref):
    z = points[:,32:39]
    l,d1 = phase(points[:,:16],z,center)
    r,d2 = phase(points[:,16:32],z,center)
    h = float(cert.H)
    t1,t2 = h*(d1-ref),h*(d2-ref)
    diff = r-l
    # Both orders of bra and ket. Remove the odd reference contribution exactly.
    signal = (np.cos(diff+t2/2)*np.sin(t2/2)+np.cos(-diff+t1/2)*np.sin(t1/2))
    norm = np.cos(diff)+np.cos(diff+t2-t1)
    return float(np.mean(signal)/np.mean(norm))


def run():
    plan = json.loads((cert.ROOT/'pruefvertrag.json').read_text())['gegenrechnung']
    pair,ref = cert.centers()
    exact = {name:cert.whole_cell(c,ref)['P_Y_plus_minus_halb'] for name,c in pair.items()}
    rows = []
    for seed in plan['Sobol_Startwerte']:
        max_n = max(plan['Punkte'])
        points = 2*qmc.Sobol(39,scramble=True,seed=seed).random_base2(int(math.log2(max_n)))-1
        for n in plan['Punkte']:
            shifts = {s:estimate(points[:n],c,float(ref)) for s,c in pair.items()}
            for s,value in shifts.items():
                lo,hi = exact[s]
                assert float(lo)<value<float(hi)
            rows.append({'seed':seed,'punkte':n,'P_minus_halb':shifts,
                         'luecke':shifts['positiv']-shifts['negativ']})
    return {'integrationsdimension':39,'art':'Zwei unabhängige frühere Belegungen am gemeinsamen Zukunftswert. Numerische Gegenrechnung.', 'laeufe':rows}


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(run(),indent=2,ensure_ascii=False))
