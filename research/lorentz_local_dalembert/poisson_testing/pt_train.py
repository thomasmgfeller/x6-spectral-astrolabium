"""Train once; seal integer classifier before held-out generation.
SPDX-License-Identifier: Apache-2.0
"""
from pt_common import *
def model(records):
    X=[np.array(r['counts'],dtype=float) for r in records]
    means=[setup(g)['means'] for g in range(2)]
    mu=[np.array([float((lo+hi)/2) for lo,hi in row]) for row in means]
    cov=(np.cov(X[0],rowvar=False)+np.cov(X[1],rowvar=False))/2
    C=F(9,10)*cov+F(1,10)*np.diag(np.diag(cov))
    coeff=np.linalg.solve(np.array(C,dtype=float),mu[1]-mu[0])
    coeff=np.rint(coeff/np.max(abs(coeff))*4096).astype(np.int64)
    threshold=flo(sum(int(a)*sum(means[g][i][k] for g in range(2) for k in range(2))/4 for i,a in enumerate(coeff)))
    assert sum(int(a)*(mu[1][i]-mu[0][i]) for i,a in enumerate(coeff))>0
    return dict(coefficients=coeff.tolist(),threshold=threshold,predict_one='dot(coefficients,counts)>threshold',
                fields='all 90 counts only; pairwise overlaps and physical_count not needed by this test',
                training_source_hashes=[hashlib.sha256((HERE/f'training-{g}.json.gz').read_bytes()).hexdigest() for g in range(2)])
def main():
    frozen();c=read(HERE/'contract.json');f=kernel();rows=[]
    for g in range(2):
        r=simulate(g,'training',c['training_trials_per_geometry'],f);save(HERE/f'training-{g}.json.gz',r);rows.append(r)
    m=model(rows);save(HERE/'model.json',m)
    save(HERE/'model_seal.json',{'model_sha256':hashlib.sha256((HERE/'model.json').read_bytes()).hexdigest(),'validation_generated':False})
    print('MODEL_SEALED_BEFORE_VALIDATION',flush=True)
if __name__=='__main__':main()
