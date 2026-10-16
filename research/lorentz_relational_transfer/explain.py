"""Post-hoc algebraic interpretation and supplemental negative controls.

This is not part of the pre-target source freeze or the compared feature panel.
It reads the completed fixed run, never generates or selects new target data.
"""
import copy
import gzip
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent

def require(ok,why):
    if not ok: raise ValueError(why)
def product(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def coefficients(factors):
    # Ascending coefficients while multiplying, then descending monic order.
    p=[1]
    for constant,power in factors:
        for _ in range(power):
            q=[0]*(len(p)+2)
            for i,x in enumerate(p): q[i]-=constant*x; q[i+2]+=x
            p=q
    return list(reversed(p))

def run(directory):
    import check
    records=[json.loads(s) for s in gzip.decompress((directory/'records.jsonl.gz').read_bytes()).decode().splitlines()]
    targets=[next(r for r in records if r['id']==name) for name in ['closed-rook','closed-shrikhande']]
    trace=json.loads(gzip.decompress((directory/'rounds.json.gz').read_bytes()))['32']
    canonical_colors=[]
    for r in targets:
        c=[[int(x) for x in row] for row in r['relation_rows']]; b=[row[16:] for row in c[:16]]
        a=[[b[i][j]-int(i==j) for j in range(16)] for i in range(16)]; z=[[int(i!=j)-a[i][j] for j in range(16)] for i in range(16)]
        require(all(sum(row)==6 for row in a),'SRG degree')
        require(a==list(map(list,zip(*a))),'symmetric adjacency')
        aa,az,zz=product(a,a),product(a,z),product(z,z)
        for i in range(16):
            for j in range(16):
                require(aa[i][j]==6*int(i==j)+2*a[i][j]+2*z[i][j],'A squared')
                require(az[i][j]==3*a[i][j]+4*z[i][j],'A N')
                require(zz[i][j]==9*int(i==j)+6*a[i][j]+4*z[i][j],'N squared')
        spectra=[coefficients([(49,1),(9,6),(1,9)]),coefficients([(-49,1),(-9,6),(-1,9)]),coefficients([(9604,1),(324,6),(4,9)])]
        require(r['features']['H7']==[32,spectra,16,16,336,336],'H7 factorizations')
        graph_index=trace['ids'].index(r['id']); rounds=[]
        for step in trace['rounds']:
            groups={}
            for u in range(32):
                for v in range(32):
                    i,j=u%16,v%16; typ=0 if i==j else 1 if a[i][j] else 2
                    groups.setdefault((u//16,v//16,typ),set()).add(step['matrices'][graph_index][u][v])
            require(len(groups)==12 and all(len(s)==1 for s in groups.values()),'coherent class was split')
            rounds.append([[list(key),next(iter(value))] for key,value in sorted(groups.items())])
        canonical_colors.append(rounds)
    require(canonical_colors[0]==canonical_colors[1],'cross-control coherent class colors differ')
    require(targets[0]['features']==targets[1]['features'],'joint feature equality')
    actual={'inputs':json.loads((directory/'inputs.json').read_text()),'records':records,'summary':json.loads((directory/'summary.json').read_text())}
    rejected=[]
    for kind in ['lost_R2_histogram_occurrence','omitted_structured_residual_pair']:
        bad=copy.deepcopy(actual)
        if kind.startswith('lost'): bad['records'][0]['features']['R2'][0][1]-=1
        else: bad['summary']['cells']['structured/n32']['methods']['H7+N1+Q1+R2']['pairs'].pop()
        try: check.validate(bad,actual)
        except ValueError: rejected.append(kind)
    require(len(rejected)==2,'supplemental negative controls')
    result={'schema':'x6.transfer-posthoc-explanation/1','evidence_class':'POST_HOC_ALGEBRA_AND_SUPPLEMENTAL_CHECKS',
        'targets':[r['id'] for r in targets],'joint_feature_equality':True,'srg_algebra_checked':True,'H7_factorizations_checked':True,
        'coherent_class_count':12,'common_round_class_colors':canonical_colors[0],'supplemental_negative_controls_rejected':rejected,
        'chronology_note':'Original frozen run perturbed histogram multiplicity by adding one. This separately labelled post-hoc check additionally removes one and omits the structured residual pair. No frozen source or result was changed.'}
    (directory/'explanation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='common_round_class_colors'},indent=2))

if __name__=='__main__': run(Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'results')
