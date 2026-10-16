"""Counterchecker: exhaustive upper relations, bijections, determinants.

Imports no producer or historical atlas algorithm. All arithmetic is exact.
"""
from collections import defaultdict, Counter
from fractions import Fraction
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def token(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)


def same(left,right,message):
    require(token(left)==token(right),message)


def decode(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate JSON key')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def validate_rows(rows,n):
    require(type(n) is int and 1<=n<=7,'unsupported size')
    require(type(rows) is list and len(rows)==n,'row count')
    require(all(type(row) is str and len(row)==n and not set(row)-{'0','1'} for row in rows),'row encoding')
    c=[[int(x) for x in row] for row in rows]
    require(all(c[i][i]==0 for i in range(n)),'irreflexivity')
    require(all(not(c[i][j] and c[j][k]) or c[i][k]
                for i in range(n) for j in range(n) for k in range(n)),'transitivity')
    return c


def degree_list(c):
    n=len(c)
    return [(sum(c[j][i] for j in range(n)),sum(c[i])) for i in range(n)]


def isomorphic(a,b, count=False):
    if len(a)!=len(b):return 0 if count else False
    da,db=degree_list(a),degree_list(b)
    if sorted(da)!=sorted(db):return 0 if count else False
    options={i:[j for j in range(len(b)) if da[i]==db[j]] for i in range(len(a))}
    order=sorted(options,key=lambda i:len(options[i]))
    assigned={};used=set()
    def visit(k):
        if k==len(order):return 1 if count else True
        total=0
        i=order[k]
        for j in options[i]:
            if j in used or any(a[i][u]!=b[j][v] or a[u][i]!=b[v][j] for u,v in assigned.items()):continue
            assigned[i]=j;used.add(j)
            found=visit(k+1)
            if found and not count:return True
            total+=found
            used.remove(j);del assigned[i]
        return total if count else False
    return visit(0)


def determinant(matrix):
    a=[list(row) for row in matrix];n=len(a);sign=1;previous=1
    if n==0:return 1
    for k in range(n-1):
        if a[k][k]==0:
            pivot=next((i for i in range(k+1,n) if a[i][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        pivot=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=a[i][j]*pivot-a[i][k]*a[k][j]
                require(numerator%previous==0,'inexact Bareiss division')
                a[i][j]=numerator//previous
        for i in range(k+1,n):a[i][k]=0
        previous=pivot
    return sign*a[-1][-1]


def polynomial(a):
    n=len(a)
    differences=[determinant([[x*(i==j)-a[i][j] for j in range(n)] for i in range(n)]) for x in range(n+1)]
    result=[Fraction(0)]*(n+1);basis=[Fraction(1)]
    for k in range(n+1):
        for j,b in enumerate(basis):result[j]+=differences[0]*b
        differences=[v-u for u,v in zip(differences,differences[1:])]
        new=[Fraction(0)]*(len(basis)+1)
        for j,b in enumerate(basis):new[j]-=k*b/(k+1);new[j+1]+=b/(k+1)
        basis=new
    require(all(x.denominator==1 for x in result),'interpolation coefficients not integers')
    coefficients=[int(x) for x in reversed(result)]
    require(coefficients[0]==1,'nonmonic polynomial')
    return coefficients


def feature(c):
    n=len(c)
    s=[[c[i][j]+c[j][i] for j in range(n)] for i in range(n)]
    a=[[c[i][j]-c[j][i] for j in range(n)] for i in range(n)]
    k=[[2*sum(c[v][i]*c[v][j]-c[i][v]*c[j][v] for v in range(n)) for j in range(n)] for i in range(n)]
    # Explicit triples, not the producer's binomial degree formula.
    wf=sum(c[v][i]*c[v][j] for v in range(n) for i,j in combinations(range(n),2))
    wp=sum(c[i][v]*c[j][v] for v in range(n) for i,j in combinations(range(n),2))
    power=[row[:] for row in c];height=1
    while any(x for row in power for x in row):
        height+=1
        require(height<=n,'cyclic relation')
        power=[[sum(power[i][v]*c[v][j] for v in range(n)) for j in range(n)] for i in range(n)]
    return {'n':n,'polynomials_S_A_K':[polynomial(m) for m in (s,a,k)],
            'minimal_maximal':[sum(not any(c[j][i] for j in range(n)) for i in range(n)),sum(not any(row) for row in c)],
            'degree_pairs':[list(x) for x in sorted(degree_list(c))],
            'W_future':wf,'W_past':wp,'relations':sum(map(sum,c)),'height':height}


def all_upper_relations(n):
    # Cartesian product assigns each of n(n-1)/2 binary choices exactly once.
    choices=[range(1 << (n-i-1)) for i in range(n)]
    for raw in product(*choices):
        rows=tuple(value << (i+1) for i,value in enumerate(raw))
        # R_ij implies successors(j) subset successors(i); exactly transitivity.
        valid=True
        for i,row in enumerate(rows):
            active=row
            while active:
                bit=active & -active;j=bit.bit_length()-1
                if rows[j] & ~row:valid=False;break
                active-=bit
            if not valid:break
        yield rows,valid


def group_records(records):
    pools={name:defaultdict(list) for name in ['F0','F0_W_future','F0_W_both','F0_D']}
    for r in records:
        f=r['features'];base=[f['n'],f['polynomials_S_A_K'],f['minimal_maximal']]
        values={'F0':base,'F0_W_future':base+[f['W_future']],
                'F0_W_both':base+[f['W_future'],f['W_past']],'F0_D':base+[f['degree_pairs']]}
        for name,value in values.items():pools[name][token(value)].append(r['id'])
    result={}
    for name,pool in pools.items():
        groups=sorted(sorted(g) for g in pool.values() if len(g)>1)
        result[name]={'classes':len(pool),'collision_groups':groups,'collision_pairs':sum(len(g)*(len(g)-1)//2 for g in groups)}
    return result


def prepare_records(atlas):
    require(atlas.get('schema')=='x6.lorentz-n7-atlas/1','atlas schema')
    maximum=atlas.get('maximum_n');require(type(maximum) is int and 1<=maximum<=7,'maximum_n')
    records=atlas.get('records');require(type(records) is list,'records')
    identifiers=[r.get('id') for r in records]
    require(all(type(x) is str for x in identifiers) and len(set(identifiers))==len(identifiers),'duplicate or invalid ids')
    require(set(atlas['by_n'])=={str(n) for n in range(1,maximum+1)},'size coverage')
    buckets=defaultdict(list);matrices={}
    for r in records:
        n=r['n'];require(type(n) is int and 1<=n<=maximum,'record size')
        require(set(r)=={'id','n','canonical_code','relation_rows','automorphisms','linear_extensions','natural_label_multiplicity','features'},'record fields')
        c=validate_rows(r['relation_rows'],n);matrices[r['id']]=c
        key=(n,tuple(sorted(degree_list(c))))
        require(not any(isomorphic(c,other[1]) for other in buckets[key]),'duplicate isomorphism class')
        buckets[key].append((r,c))
        for field in ['canonical_code','automorphisms','linear_extensions','natural_label_multiplicity']:
            require(type(r[field]) is int and r[field]>=(0 if field=='canonical_code' else 1),'integer metadata')
        expected_code=sum(int(ch) << (n*i+j) for i,row in enumerate(r['relation_rows']) for j,ch in enumerate(row))
        require(r['canonical_code']==expected_code,'matrix code')
        require(r['linear_extensions']==r['automorphisms']*r['natural_label_multiplicity'],'multiplicity product')
    return buckets,matrices


def verify(atlas):
    maximum=atlas['maximum_n'];buckets,matrices=prepare_records(atlas)
    reports={};all_records=[];counts=Counter();polynomials=0
    expected_counts=[1,2,5,16,63,318,2045]
    for n in range(1,maximum+1):
        records=[r for r in atlas['records'] if r['n']==n]
        require(len(records)==expected_counts[n-1],'unlabelled count')
        examined=accepted=0
        for rows,valid in all_upper_relations(n):
            examined+=1
            if not valid:continue
            accepted+=1
            c=[[(row >> j)&1 for j in range(n)] for row in rows]
            options=buckets[(n,tuple(sorted(degree_list(c))))]
            matches=[r['id'] for r,other in options if isomorphic(c,other)]
            require(len(matches)==1,'natural relation not covered exactly once')
            counts[matches[0]]+=1
        require(examined==1 << (n*(n-1)//2),'exhaustive binary coverage')
        independent_records=[]
        for r in records:
            require(counts[r['id']]==r['natural_label_multiplicity'],'natural multiplicity mismatch')
            automorphisms=isomorphic(matrices[r['id']],matrices[r['id']],count=True)
            require(automorphisms==r['automorphisms'],'automorphism count mismatch')
            require(automorphisms*counts[r['id']]==r['linear_extensions'],'linear extension count mismatch')
            f=feature(matrices[r['id']]);same(f,r['features'],'exact feature mismatch '+r['id'])
            independent_records.append({'id':r['id'],'features':f});polynomials+=3
        groups=group_records(independent_records)
        same(groups,atlas['by_n'][str(n)]['groups'],'signature groups differ')
        same(atlas['by_n'][str(n)]['height_counts'],{str(h):sum(r['features']['height']==h for r in independent_records) for h in range(1,n+1)},'height counts')
        require(atlas['by_n'][str(n)]['orders']==len(records),'summary order count')
        require(atlas['by_n'][str(n)]['naturally_labelled_orders']==accepted,'summary natural count')
        reports[str(n)]={'binary_relations_examined':examined,'naturally_labelled_orders':accepted,
                         'nonisomorphic_orders':len(records),'exact_once_coverage':True,
                         'natural_multiplicity_by_id':{r['id']:counts[r['id']] for r in records},'groups':groups}
        all_records.extend(independent_records)
        print(json.dumps({'phase':'independent_exhaustive_check','n':n,'binary_relations':examined,'natural_orders':accepted,'classes':len(records)}),flush=True)
    pairs_checked=verify_witnesses(atlas,reports,matrices)
    outcome='REFUTED_BY_COUNTEREXAMPLE' if pairs_checked else 'SUPPORTED_FINITE_N_LE_'+str(maximum)
    require(atlas['hypothesis_status']==outcome,'hypothesis status mismatch')
    if maximum>=6:
        require({k:v['classes'] for k,v in reports['6']['groups'].items()}=={'F0':314,'F0_W_future':318,'F0_W_both':318,'F0_D':318},'known n6 regression')
    if maximum==7:
        h2=[r for r in all_records if r['features']['n']==7 and r['features']['height']<=2]
        require(len(h2)==164,'known n7 height-two count')
        groups=group_records(h2);same(groups,atlas['n7_height_le_2'],'height-two groups')
        require({k:v['classes'] for k,v in groups.items()}=={'F0':158,'F0_W_future':163,'F0_W_both':164,'F0_D':164},'known n7 height-two regression')
    return {'schema':'x6.lorentz-n7-independent/1','status':'PASS_EXACT_COUNTERCHECK',
            'hypothesis_status':outcome,'representatives_checked':len(atlas['records']),
            'exact_polynomials_checked':polynomials,'primary_pairs_checked':pairs_checked,
            'by_n':reports,'scope':'INDEPENDENT_ALGORITHMS_NOT_EXTERNAL_HUMAN_REVIEW; FINITE_N_LE_7_ONLY'}


def verify_witnesses(atlas,reports,matrices):
    lookup={r['id']:r for r in atlas['records']};expected_pairs=[]
    for level in reports.values():
        for g in level['groups']['F0_W_both']['collision_groups']:expected_pairs.extend(list(p) for p in combinations(g,2))
    require(len(atlas['primary_counterexamples'])==len(expected_pairs),'missing primary pairs')
    for pair,witness in zip(expected_pairs,atlas['primary_counterexamples']):
        same(pair,witness['ids'],'counterexample pair membership')
        left,right=pair;a,b=matrices[left],matrices[right]
        require(not isomorphic(a,b),'claimed counterexample is isomorphic')
        expected={'ids':pair,'n':len(a),'left':lookup[left],'right':lookup[right],
                  'same_D':sorted(degree_list(a))==sorted(degree_list(b)),
                  'dual_isomorphic':isomorphic([list(col) for col in zip(*a)],b),'isomorphic':False}
        same(witness,expected,'counterexample contents')
    return len(expected_pairs)
