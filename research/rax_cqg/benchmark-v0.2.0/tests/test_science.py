"""Independent finite reference cases; limits are documented in MODEL_CONTRACT.md."""
import itertools
import json
import math
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path
import numpy as np
import scipy.linalg

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rax_cqg_twin import (CausalSet,BDGAction,PCG32,MODELS,diagnose,experiment,
                         generate,load_experiment,sample_diamond_points,thinning_path)
from rax_cqg_matter_astrolab import ClassicalGraphField
from rax_cqg_reference_models import clock_reference,clock_state,move_reference


def bfs_reachability(n,edges):
    adjacency=[[] for _ in range(n)]
    for i,j in edges:adjacency[i].append(j)
    result=np.zeros((n,n),dtype=int)
    for i in range(n):
        seen=set();stack=list(adjacency[i])
        while stack:
            v=stack.pop()
            if v in seen:continue
            seen.add(v);stack.extend(adjacency[v])
        for j in seen:result[i,j]=1
    return result


def direct_counts(r):
    n=len(r);counts={}
    for i in range(n):
        for j in range(n):
            if r[i,j]:
                interior=set(np.flatnonzero(r[i]))&set(np.flatnonzero(r[:,j]))
                counts[len(interior)]=counts.get(len(interior),0)+1
    return [counts.get(k,0) for k in range(max(counts,default=-1)+1)]


class OrderTests(unittest.TestCase):
    def test_pcg_published_reference_vector(self):
        rng=PCG32(42,54)
        self.assertEqual([rng.next_uint32() for _ in range(6)],
                         [0xa15c02b7,0x7b47f409,0xba1d3330,0x83d2f293,0xbfa4784b,0xcbed606e])

    def test_all_upper_dags_n5_against_bfs(self):
        possible=list(itertools.combinations(range(5),2));unique=set()
        for mask in range(1<<len(possible)):
            edges=[e for k,e in enumerate(possible) if mask>>k&1]
            expected=bfs_reachability(5,edges)
            c=CausalSet.from_edges(5,list(reversed(edges)))
            np.testing.assert_array_equal(c.R,expected)
            self.assertEqual(c.interval_histogram(),direct_counts(expected))
            hist=direct_counts(expected)
            ref=5+sum(v*(hist[k] if k<len(hist) else 0) for k,v in enumerate([-1,9,-16,8]))
            self.assertEqual(BDGAction.compute(c),ref)
            longest=max(len(ids) for length in range(1,6) for ids in itertools.combinations(range(5),length)
                        if all(expected[i,j] for i,j in zip(ids,ids[1:])))
            self.assertEqual(c.height(),longest)
            unique.add(tuple(c.rows()))
        self.assertEqual(len(unique),357)

    def test_order_independence_all_permutations_chain4_edges(self):
        for order in itertools.permutations([(0,1),(1,2),(2,3)]):
            np.testing.assert_array_equal(CausalSet.from_edges(4,order).R,np.triu(np.ones((4,4),int),1))

    def test_arbitrary_labels_and_cycle_atomicity(self):
        c=CausalSet.from_edges(4,[(3,1),(1,0)])
        self.assertEqual(c.R[3,0],1);old=c.R
        with self.assertRaises(ValueError):c.add_relation(0,3)
        np.testing.assert_array_equal(old,c.R)
        public=c.R;public[:]=0;np.testing.assert_array_equal(old,c.R)

    def test_matrix_rejects_nonorders(self):
        for matrix in [[[0,1],[1,0]],[[1]],[[0,1,0],[0,0,1],[0,0,0]],[[0,2],[0,0]],[[0,float('nan')],[0,0]],[[0,1]]]:
            with self.assertRaises(ValueError):CausalSet.from_matrix(matrix)

    def test_inputs_rejected(self):
        for n in [-1,1.2,True,513]:
            with self.assertRaises(ValueError):CausalSet(n)
        for p in [-.1,1.1,float('nan'),float('inf'),True]:
            with self.assertRaises(ValueError):generate('percolation',4,42,p)
        for seed in [-1,2**32,.5,True]:
            with self.assertRaises(ValueError):PCG32(seed)

    def test_empty_and_singleton_defined(self):
        for n in [0,1]:
            d=diagnose(CausalSet(n));self.assertEqual(d['bdg4_bracket'],n)
            self.assertIsNone(d['h2_spectral_entropy']);self.assertIsNone(d['algebraic_connectivity'])
            self.assertEqual(d['spectral_radius'],0)
            self.assertEqual(d['height'],n)

    def test_bdg_hand_examples(self):
        examples=[(CausalSet(4),4), (CausalSet.from_edges(4,[(0,1),(1,2)]),11),
                  (CausalSet.from_edges(4,[(0,1),(0,2),(0,3)]),1),
                  (CausalSet.from_edges(4,[(0,1),(0,2),(1,3),(2,3)]),-16)]
        for c,expected in examples:self.assertEqual(BDGAction.compute(c),expected)

    def test_adjacency_and_laplacian_exact_cases(self):
        c,_=generate('chain',8);d=diagnose(c)
        np.testing.assert_allclose(d['adjacency_spectrum'],[-1]*7+[7],atol=1e-12)
        np.testing.assert_allclose(d['laplacian_spectrum'],[0]+[8]*7,atol=1e-12)
        self.assertAlmostEqual(d['algebraic_connectivity'],8,12)
        disconnected=CausalSet.from_edges(4,[(0,1),(1,2)])
        self.assertAlmostEqual(diagnose(disconnected)['algebraic_connectivity'],0,12)

    def test_relabelling(self):
        c,_=generate('percolation',16,123,.3);ids=np.random.default_rng(7).permutation(16)
        other=CausalSet.from_matrix(c.R[np.ix_(ids,ids)])
        d1,d2=diagnose(c),diagnose(other)
        for k in ['bdg4_bracket','interval_counts','height','relations','links']:self.assertEqual(d1[k],d2[k])
        for k in ['adjacency_spectrum','laplacian_spectrum']:np.testing.assert_allclose(d1[k],d2[k],atol=1e-12)

    def test_entropy_and_moment_identities(self):
        c,_=generate('percolation',18,123,.3);d=diagnose(c);h=(c.R+c.R.T).astype(float)
        rho=h@h/np.trace(h@h);w=scipy.linalg.eigvalsh(rho);w=w[w>1e-14]
        self.assertAlmostEqual(d['h2_spectral_entropy'],float(-np.sum(w*np.log(w))),11)
        self.assertAlmostEqual(sum(e*e for e in d['adjacency_spectrum']),2*d['relations'],10)
        self.assertAlmostEqual(sum(e**3 for e in d['adjacency_spectrum']),6*d['triangles'],9)

    def test_spectrum_does_not_claim_causal_reconstruction(self):
        a=CausalSet.from_edges(3,[(0,1),(0,2)]);b=CausalSet.from_edges(3,[(0,2),(1,2)])
        self.assertNotEqual(int((a.R.sum(0)==0).sum()),int((b.R.sum(0)==0).sum()))
        np.testing.assert_allclose(diagnose(a)['adjacency_spectrum'],diagnose(b)['adjacency_spectrum'],atol=1e-12)

    def test_no_global_rng_side_effect(self):
        np.random.seed(876);expected=np.random.rand(5)
        np.random.seed(876);generate('minkowski_4d',12,42);actual=np.random.rand(5)
        np.testing.assert_array_equal(expected,actual)

    def test_all_generators_are_orders_and_repeatable(self):
        for model in MODELS:
            for seed in [0,42,2**32-1]:
                a,meta=generate(model,16,seed);b,_=generate(model,16,seed)
                np.testing.assert_array_equal(a.R,b.R)
                np.testing.assert_array_equal(a.R,bfs_reachability(a.size,list(zip(*np.where(a.R)))))

    def test_minkowski_sampling_4d_volume_moments(self):
        count=20000;pts=sample_diamond_points(count,4,PCG32(104729))
        time2=pts[:,0]**2;radius2=(pts[:,1:]**2).sum(1)
        self.assertTrue(np.all(np.sqrt(radius2)<=.5-np.abs(pts[:,0])+1e-14))
        # Exact volume moments on the unit-proper-time diamond; six-standard-error gate.
        self.assertLess(abs(time2.mean()-1/60),6*math.sqrt((1/1120-1/3600)/count))
        self.assertLess(abs(radius2.mean()-1/10),6*math.sqrt((3/224-1/100)/count))

    def test_minkowski_2d_uniform_null_coordinates(self):
        pts=sample_diamond_points(12000,2,PCG32(123))
        u=pts[:,0]+.5-pts[:,1];v=pts[:,0]+.5+pts[:,1]
        for x in [u,v]:
            self.assertTrue(np.all((x>0)&(x<1)))
            self.assertLess(abs(x.mean()-.5),6/math.sqrt(12*len(x)))

    def test_export_roundtrip_and_hash_tampering(self):
        r=experiment('minkowski_4d',16,42);c=load_experiment(json.loads(json.dumps(r)))
        self.assertEqual(c.digest(),r['relation_sha256'])
        r['relation_sha256']='0'*64
        with self.assertRaises(ValueError):load_experiment(r)

    def test_thinning_endpoints_and_induced_relations(self):
        c,_=generate('percolation',16)
        zero=thinning_path(c,0,3);one=thinning_path(c,1,3)
        self.assertEqual([x['metrics']['size'] for x in zero['path']],[16,0,0,0])
        self.assertTrue(all(x['relation_rows']==c.rows() for x in one['path']))
        path=thinning_path(c,.75,5)
        previous=set(range(16))
        for item in path['path']:
            ids=item['original_indices'];self.assertTrue(set(ids)<=previous);previous=set(ids)
            self.assertEqual(item['relation_rows'],c.induced(ids).rows())

    def test_thinning_semigroup_distribution_exact(self):
        q1,q2=Fraction(2,3),Fraction(3,5);n=4
        for bmask in range(1<<n):
            b=bmask.bit_count();summed=Fraction(0)
            for amask in range(1<<n):
                if amask&bmask!=bmask:continue
                a=amask.bit_count()
                summed+=q1**a*(1-q1)**(n-a)*q2**b*(1-q2)**(a-b)
            self.assertEqual(summed,(q1*q2)**b*(1-q1*q2)**(n-b))


class FieldClockTests(unittest.TestCase):
    def test_gaussian_precision_lower_bound_and_action(self):
        for model in MODELS:
            c,_=generate(model,12,42);f=ClassicalGraphField(c)
            self.assertGreaterEqual(np.linalg.eigvalsh(f.Q)[0],1.2**2-1e-12)
            phi=f.sample();self.assertGreaterEqual(f.action(phi),0)
            manual=0.
            h=c.R+c.R.T
            for a in range(f.internal_dim):
                manual+=.5*f.mass**2*np.sum(phi[:,a]**2)
                for i,j in itertools.combinations(range(c.size),2):
                    manual+=.5*f.coupling*h[i,j]*(phi[i,a]-phi[j,a])**2
            self.assertAlmostEqual(f.action(phi),manual,10)

    def test_gaussian_bad_parameters(self):
        for mass,coupling in [(0,.6),(-1,.6),(1,-.1),(float('nan'),1)]:
            with self.assertRaises(ValueError):ClassicalGraphField(CausalSet(3),mass,coupling)

    def test_gaussian_covariance_identity(self):
        c,_=generate('percolation',8);f=ClassicalGraphField(c)
        inv=np.linalg.solve(f.cholesky.T,np.eye(8))
        np.testing.assert_allclose(inv@inv.T,np.linalg.inv(f.Q),atol=1e-12)

    def test_clock_constraint_and_schrodinger(self):
        r=clock_reference();self.assertEqual(r['constraint_residual'],0.)
        self.assertLess(r['max_unitary_reference_error'],1e-12)
        self.assertLess(r['max_schrodinger_residual'],1e-8)
        for row in r['samples']:
            self.assertAlmostEqual(row['overlap_weight'],.5,13)
            self.assertAlmostEqual(row['p_plus_x'],(1+math.cos(row['tau']))/2,13)

    def test_clock_povm_resolution_and_periodicity(self):
        summed=np.zeros((2,2),complex);hs=np.array([-.5,.5]);points=64
        for k in range(points):
            ket=np.exp(-1j*hs*2*math.pi*k/points)/math.sqrt(2)
            summed+=2/points*np.outer(ket,ket.conj())
        np.testing.assert_allclose(summed,np.eye(2),atol=1e-14)
        a=clock_state(.7)[0];b=clock_state(.7+2*math.pi)[0]
        np.testing.assert_allclose(np.outer(a,a.conj()),np.outer(b,b.conj()),atol=1e-14)

    def test_move_reference_scope(self):
        r=move_reference();self.assertTrue(r['exact_relation_insertions_commute'])
        self.assertEqual(r['classical_reset_commutator'],[[1,1],[-1,-1]])
        self.assertEqual(r['QSG_status'],'NOT_IMPLEMENTED')


class ParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[{'model':model,'size':n,'seed':seed,'p':.25}
                   for model in MODELS for n,seed in [(4,0),(16,42),(48,123),(96,104729)]]
        cls.cases.extend([{'rows':[]},{'rows':['0']},{'rows':['0110','0010','0000','0000']},
                          {'rows':['0000','0000','1000','1100']}])
        raw=subprocess.check_output(['node',str(ROOT/'tests/js_bridge.js')],input=json.dumps({'cases':cls.cases}),text=True)
        cls.javascript=json.loads(raw)

    def test_all_metrics_and_matrices(self):
        for case,result in zip(self.cases,self.javascript['results']):
            if 'rows' in case:
                c=CausalSet.from_matrix([[int(x) for x in row] for row in case['rows']]);expected=diagnose(c)
            else:
                record=experiment(case['model'],case['size'],case['seed'],case['p']);c=load_experiment(record);expected=record['metrics']
            self.assertEqual(c.rows(),result['relation_rows'])
            self.assertEqual(set(expected),set(result['metrics']))
            for key,value in expected.items():
                if value is None:self.assertIsNone(result['metrics'][key])
                else:np.testing.assert_allclose(result['metrics'][key],value,atol=1e-9,rtol=1e-9,err_msg=f'{case} {key}')

    def test_thinning_paths(self):
        for result in self.javascript['results']:
            c=CausalSet.from_matrix([[int(x) for x in row] for row in result['relation_rows']])
            expected=thinning_path(c,.75,3,104729)
            for a,b in zip(expected['path'],result['thinning']['path']):
                self.assertEqual(a['original_indices'],b['original_indices']);self.assertEqual(a['relation_rows'],b['relation_rows'])

    def test_js_selftest_and_clock(self):
        self.assertEqual(self.javascript['selftest']['passed'],self.javascript['selftest']['total'])
        for a,b in zip(clock_reference()['samples'],self.javascript['clock']['samples']):
            for k in ['tau','overlap_weight','clock_probability_density','p_plus_x']:self.assertAlmostEqual(a[k],b[k],12)


if __name__=='__main__':unittest.main(verbosity=2)
