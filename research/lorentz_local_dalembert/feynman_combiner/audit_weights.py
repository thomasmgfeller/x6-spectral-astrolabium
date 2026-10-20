"""Retrospective intrinsic weight audit. No simulator coordinates used."""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'moment_feasibility'))
from feasibility import design, solve


def main():
    contract = json.loads((BASE/'moment_feasibility/contract.json').read_text())
    c = json.loads((BASE/'phase12/contract.json').read_text())['coefficient_C']
    records = []
    for path in sorted((BASE/'joint_feasibility/results').glob('rho-*-seed-*.json')):
        raw = path.read_bytes(); cloud = json.loads(raw)
        row = dict(file=str(path.relative_to(BASE)), sha256=hashlib.sha256(raw).hexdigest(),
                   rho=cloud['rho'], seed=cloud['seed'], policies={})
        w = cloud['selection']['selected']
        if w is None:
            row['status'] = 'NO_SUPPORT'; records.append(row); continue
        row['status'] = 'AUDITED'
        cert = w['certificate']; scale = w['scale']; root = w['root']
        counts = {tuple(sorted(pair)): n for pair,n in zip(cert['interval_pairs'],cert['interval_counts'])}
        mask = np.array([b in w['temporal'] for b in w['support']])
        a0 = []
        for b, temporal in zip(w['support'],mask):
            q = (counts[tuple(sorted((root,b)))]/(cloud['rho']*np.pi/12))**(2/3)
            population = next((len(side) for side in w['support_sides'] if b in side),None)
            a0.append((-(c+3) if temporal else c/population)*scale**2/q)
        a0 = np.array(a0); d = design(np.array(cert['features'])/scale)
        row.update(scale=scale, design=d.tolist(), baseline=a0.tolist(), temporal_mask=mask.tolist(),
                   support=w['support'], baseline_mass=float(np.abs(a0).sum()))
        # Root field is shared by every difference: include its coefficient.
        def noise(a):
            full = np.r_[-np.sum(a),a]
            return dict(iid_field_noise_gain=float(full@full),
                        arbitrary_covariance_marginal_bound=float(np.abs(full).sum()**2))
        row['baseline_noise'] = noise(a0)
        for policy in ['fixed_time','free_time','unrestricted']:
            result = solve(d,a0,mask,policy,contract)
            if result['status']=='FEASIBLE':
                a = np.array(result['weights']); result.update(noise(a))
                result['iid_gain_ratio'] = result['iid_field_noise_gain']/row['baseline_noise']['iid_field_noise_gain']
                result['half_moment_residuals'] = []
                t = np.array(cert['transform'])
                for half in cert['half_vectors']:
                    dh = design((t@np.array(half)).T/scale)
                    result['half_moment_residuals'].append(float(np.linalg.norm(dh@a-np.array([0,0,0,-2,2,2,0,0,0]))))
            row['policies'][policy] = result
        records.append(row)
    summary = {}
    for rho in [2048,8192,32768]:
        rows = [r for r in records if r['rho']==rho]
        summary[rho] = dict(total=len(rows), supports=sum(r['status']=='AUDITED' for r in rows),policies={})
        for p in ['fixed_time','free_time','unrestricted']:
            good = [r['policies'][p] for r in rows if r['policies'].get(p,{}).get('status')=='FEASIBLE']
            summary[rho]['policies'][p] = dict(feasible=len(good),
                infeasible=sum(r['policies'].get(p,{}).get('status')=='INFEASIBLE' for r in rows),
                unresolved=sum(r['policies'].get(p,{}).get('status')=='UNRESOLVED' for r in rows),
                mass_le_2=sum(r['mass_ratio']<=2 for r in good),
                mass_ratio_range=[min(r['mass_ratio'] for r in good),max(r['mass_ratio'] for r in good)] if good else None,
                iid_gain_ratio_range=[min(r['iid_gain_ratio'] for r in good),max(r['iid_gain_ratio'] for r in good)] if good else None)
    result = dict(scope='Retrospective diagnostic; fitted flat moments are not validation; HOLD_PHASE3',
                  source_base_commit='560f717c0e25c957bc58bb9df5ec5ac6ad23cad0',summary=summary,records=records)
    (Path(__file__).parent/'weight_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
