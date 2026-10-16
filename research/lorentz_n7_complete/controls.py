"""Small exact anchors and rejection controls; safe under python -O."""
import contextlib
import copy
import io
import json
import independent as check


def controls(atlas=None, report=None):
    passed=[]
    def reject(name, call):
        try:call()
        except (ValueError, KeyError, TypeError):passed.append(name);return
        raise ValueError('accepted negative control: '+name)
    reject('duplicate_json_keys',lambda:check.decode('{"n":1,"n":2}'))
    reject('nonfinite_json',lambda:check.decode('{"n":NaN}'))
    reject('boolean_size',lambda:check.validate_rows(['0'],True))
    reject('nontransitive_hasse_chain',lambda:check.validate_rows(['010','001','000'],3))
    reject('directed_cycle',lambda:check.validate_rows(['01','10'],2))
    # Hand-computable matrices include a pivot swap and an asymmetric spectrum.
    check.same(check.polynomial([[0,1],[1,0]]),[1,0,-1],'S edge anchor')
    check.same(check.polynomial([[0,1],[-1,0]]),[1,0,1],'A edge anchor')
    check.same(check.polynomial([[-2,0,0],[0,-2,0],[0,0,4]]),[1,0,-12,-16],'odd coefficient sign anchor')
    fork=check.validate_rows(['011','000','000'],3)
    f=check.feature(fork)
    check.same(f['polynomials_S_A_K'],[[1,0,-2,0],[1,0,2,0],[1,0,-16,0]],'fork anchors')
    check.same([f['W_future'],f['W_past'],f['height']],[1,0,2],'oriented fork anchor')
    check.require(check.determinant([[0,2],[3,4]])==-6,'pivot anchor')
    check.require(check.isomorphic([[0]*3 for _ in range(3)],[[0]*3 for _ in range(3)],count=True)==6,'automorphism anchor')
    passed.append('manual_exact_anchors')
    if atlas is None:return {'status':'PASS','controls':passed}
    # A complete one-point atlas keeps format and summary mutation tests cheap.
    tiny=copy.deepcopy(atlas)
    tiny['maximum_n']=1;tiny['records']=[r for r in tiny['records'] if r['n']==1]
    tiny['by_n']={'1':tiny['by_n']['1']};tiny['n7_height_le_2']=None
    tiny['primary_counterexamples']=[];tiny['hypothesis_status']='SUPPORTED_FINITE_N_LE_1'
    with contextlib.redirect_stdout(io.StringIO()):check.verify(tiny)
    def mutation(name, edit):
        a=copy.deepcopy(tiny);edit(a)
        with contextlib.redirect_stdout(io.StringIO()):reject(name,lambda:check.verify(a))
    mutation('missing_representative',lambda a:a['records'].clear())
    mutation('duplicate_id',lambda a:a['records'].append(copy.deepcopy(a['records'][0])))
    def duplicate(a):
        r=copy.deepcopy(a['records'][0]);r['id']='another-id';a['records'].append(r)
    mutation('duplicate_isomorphism_class',duplicate)
    mutation('false_polynomial',lambda a:a['records'][0]['features']['polynomials_S_A_K'][0].__setitem__(1,1))
    mutation('false_fork_moment',lambda a:a['records'][0]['features'].__setitem__('W_future',1))
    mutation('boolean_integer_metadata',lambda a:a['records'][0].__setitem__('automorphisms',True))
    def corrupt_counts(a):
        a['records'][0]['automorphisms']=2;a['records'][0]['linear_extensions']=2
    mutation('coordinated_automorphism_extension_tamper',corrupt_counts)
    mutation('false_signature_class_count',lambda a:a['by_n']['1']['groups']['F0_W_both'].__setitem__('classes',2))
    mutation('false_outcome',lambda a:a.__setitem__('hypothesis_status','REFUTED_BY_COUNTEREXAMPLE'))
    # Validate witness rejection against the actual complete result, without
    # repeating enumeration for each intentionally damaged copy.
    matrices={r['id']:check.validate_rows(r['relation_rows'],r['n']) for r in atlas['records']}
    damaged=copy.deepcopy(atlas)
    if damaged['primary_counterexamples']:
        damaged['primary_counterexamples'].pop()
        reject('omitted_actual_counterexample',lambda:check.verify_witnesses(damaged,report['by_n'],matrices))
        damaged=copy.deepcopy(atlas);damaged['primary_counterexamples'][0]['isomorphic']=True
        reject('false_actual_counterexample_contents',lambda:check.verify_witnesses(damaged,report['by_n'],matrices))
    else:
        damaged['primary_counterexamples']=[{'ids':['invented','pair']}]
        reject('invented_counterexample',lambda:check.verify_witnesses(damaged,report['by_n'],matrices))
    return {'status':'PASS','controls':passed}


if __name__=='__main__':print(json.dumps(controls(),indent=2))
