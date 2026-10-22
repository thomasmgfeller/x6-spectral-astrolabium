"""Adaptive precision and scalar Jensen-bias diagnostics, no correction fit.
SPDX-License-Identifier: Apache-2.0
"""
from decimal import Decimal as D,localcontext
import gzip,json,itertools,collections
import numpy as np
from scipy.stats import poisson
from diagnose import SRC,OUT,save,matrices,reconstruct,summary_geometry,intervals

def decimal_pi():
    def atan_inverse(n):
        x=D(1)/D(n);x2=x*x;term=x;s=term;k=1
        while True:
            term=-term*x2;new=s+term/D(2*k+1)
            if new==s:return s
            s=new;k+=1
    return 16*atan_inverse(5)-4*atan_inverse(239)

def high_intervals(counts,packet,rho,precision):
    with localcontext() as ctx:
        ctx.prec=precision
        pi=decimal_pi();scale=D.from_float(packet['scale'])
        q=[(D(int(n))/(D(rho)*pi/12))**(D(2)/3)/(scale*scale) for n in counts]
        lookup={tuple(x):v for x,v in zip(packet['pairs'],q)}
        def get(a,b):return D(0) if a==b else lookup[tuple(sorted((a,b)))]
        l=packet['landmarks'];root=packet['root'];ids=l+[root]+packet['support']
        h=[[(get(l[i],l[j])-get(l[i],l[0])-get(l[0],l[j]))/2 for j in range(1,4)] for i in range(1,4)]
        mat=[h[i]+[D(int(i==j)) for j in range(3)] for i in range(3)]
        for k in range(3):
            p=max(range(k,3),key=lambda i:abs(mat[i][k]));mat[p],mat[k]=mat[k],mat[p]
            f=mat[k][k];mat[k]=[x/f for x in mat[k]]
            for i in range(3):
                if i!=k:
                    f=mat[i][k];mat[i]=[x-f*y for x,y in zip(mat[i],mat[k])]
        inv=[x[3:] for x in mat]
        z=[[(get(l[i],x)-get(l[0],x)-get(l[i],root)+get(l[0],root))/2 for i in range(1,4)] for x in ids]
        out={}
        for i,j in itertools.combinations(range(len(ids)),2):
            v=[z[j][k]-z[i][k] for k in range(3)]
            val=sum(v[k]*inv[k][r]*v[r] for k in range(3) for r in range(3))
            out[(i,j)]=(int(val>0)-int(val<0),str(val))
        return out,[str(v) for v in q]

def main():
    c=json.loads((SRC/'contract.json').read_text());precision_rows=[];bias_rows=[];residual=[];original_status=collections.Counter()
    for path in sorted((SRC/'results/truth').glob('cloud-*.json')):
        t=json.loads(path.read_text());i=t['index'];p=np.array(t['points'])
        row=json.loads(gzip.decompress((SRC/f'results/cloud-{i:02d}.json.gz').read_bytes()))
        pk=row['selection']['fourth']['packet'];H,Z,groups,ids=matrices(pk);lookup={a:k for k,a in enumerate(ids)}
        truth=-intervals(p)/pk['scale']**2
        qt=np.array([truth[lookup[a],lookup[b]] for a,b in pk['pairs']])
        lam=c['count_density']*np.pi/12*(qt*pk['scale']**2)**1.5
        factor=(c['count_density']*np.pi/12)**(-2/3)/pk['scale']**2
        means=[];bounds=[]
        for mu in lam:
            cutoff=int(poisson.ppf(1-1e-14,mu));n=np.arange(cutoff+1)
            means.append(factor*np.sum(n**(2/3)*poisson.pmf(n,mu)))
            bounds.append(factor*(mu*poisson.sf(cutoff-1,mu)+poisson.sf(cutoff,mu)))
        mean=np.array(means);geo=reconstruct(mean,pk,H,Z)
        assert np.max(mean/qt-1)<1e-9
        bias_rows.append(dict(index=i,geometry=summary_geometry(geo),
            relative_input_bias_range=[float(np.min(mean/qt-1)),float(np.max(mean/qt-1))],
            max_tail_bound=float(max(bounds)),qtrue=qt,poisson_means=lam,mean_transformed_q=mean))
        for rep in row['replicates']:
            original_status[rep['inference']['four']['status']]+=1
            q=np.array(rep['inference']['q']);asq=np.where(np.isin(groups,['A','S']),qt,q)
            g=reconstruct(asq,pk,H,Z)
            # R is a common translation for all nodes except the separately
            # fixed root, because root-anchor q are also distances for node 4.
            mask=np.array(groups=='R')
            nonroot=[k for k in range(len(ids)) if k!=4]
            for a,b in itertools.combinations(nonroot,2):assert np.max(abs((Z[a]-Z[b])[:,mask]))==0
            if not g['passed']:
                observed=np.array(pk['full_order'],bool)
                for a,b in itertools.combinations(range(len(ids)),2):
                    if (g['order'][a,b]!=observed[a,b] or g['order'][b,a]!=observed[b,a]):
                        residual.append(dict(index=i,replicate=rep['replicate'],local_nodes=[a,b],involves_root=4 in [a,b]))
        primary=row['replicates'][0]
        if primary['inference']['four']['status']!='WEIGHTS_VALID':continue
        vals80,q80=high_intervals(primary['observed']['counts'],pk,c['count_density'],80)
        vals120,q120=high_intervals(primary['observed']['counts'],pk,c['count_density'],120)
        stored=intervals(np.array(primary['inference']['four']['coordinates']))
        sign_disagreements=[];max_abs=0.;max_pdiff=D(0)
        for pair,(sign,value) in vals80.items():
            assert sign==vals120[pair][0]
            if sign!=np.sign(stored[pair]):sign_disagreements.append(pair)
            max_abs=max(max_abs,abs(float(value)-stored[pair]))
            with localcontext() as ctx:
                ctx.prec=130
                max_pdiff=max(max_pdiff,abs(D(value)-D(vals120[pair][1])))
        assert not sign_disagreements
        precision_rows.append(dict(index=i,pairs=len(vals80),sign_disagreements=sign_disagreements,
            max_absolute_interval_difference_vs_binary64=max_abs,max_precision80_vs120_difference=str(max_pdiff),
            max_q_difference_vs_binary64=float(max(abs(float(x)-v) for x,v in zip(q120,primary['inference']['q'])))))
    out=dict(status='PASS',scope='adaptive explanatory check; no change to gates',
        precision=dict(clouds=len(precision_rows),pairs=sum(x['pairs'] for x in precision_rows),
          all_signs_agree=True,max_interval_difference=max(x['max_absolute_interval_difference_vs_binary64'] for x in precision_rows),records=precision_rows),
        mean_input=dict(clouds=len(bias_rows),geometry_order_pass=sum(x['geometry'].get('passed',False) for x in bias_rows),
            max_poisson_tail_bound=max(x['max_tail_bound'] for x in bias_rows),
            interpretation='G(E[q]) is evaluated, not E[G(q)]; double-precision summation with tail bound, not interval-arithmetic certification',records=bias_rows),
        exact_AS_residual=residual,original_measurement_statuses=dict(original_status),
        root_translation_cancellation='Exact coefficient identities checked for all nonroot pairs in all 162 repeats')
    save('supplement.json',out)
    print(json.dumps({k:v if k not in ['precision','mean_input'] else {kk:vv for kk,vv in v.items() if kk!='records'} for k,v in out.items()},indent=2))

if __name__=='__main__':main()
