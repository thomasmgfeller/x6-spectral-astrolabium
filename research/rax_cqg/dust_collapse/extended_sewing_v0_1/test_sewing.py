"""Meaningful regression and failure controls for the finite cut contract."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import unittest
import random
from sewing import seal, sew_packets, make_packet, action_components, influence_components, evaluate_influence, doubled_hessian, transitive_closure, local_action
from analysis import packets, oracle, bypass_witness, gaussian_atom, OUTER, INNER
from inputs import prior_core as pc
from flint import ctx

class SewingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec=160
        cls.left,cls.right=packets(25500,25500)
        cls.join=sew_packets(cls.left,cls.right)
        cls.fields={kind:{str(i):str(value(i)) for i in range(8)} for kind,value in
                    [('t',lambda i:Fraction(i-4,5)),('r',lambda i:Fraction(i,8)),('q',lambda i:Fraction(i*i-5,7))]}

    def test_all_history_actions_against_global_order(self):
        for l,r in product(pc.histories(),repeat=2):
            self.assertEqual(sew_packets(*packets(l,r))['joint_action'],oracle(l,r)[0])

    def test_exact_sewing_phase_every_density_mask(self):
        for mask in product((0,1),repeat=8):
            fields=deepcopy(self.fields);fields['r']={str(i):str(Fraction(i+1,9)*mask[i]) for i in range(8)}
            la=action_components(self.left['local_action'],fields);ra=action_components(self.right['local_action'],fields)
            inf=influence_components(self.join,fields);full=action_components(self.join['joint_action'],fields)
            for key in full:self.assertEqual(Fraction(la[key])+Fraction(ra[key])+Fraction(inf[key]),Fraction(full[key]))

    def test_each_of_the_five_terms_is_detectable(self):
        action=self.join['joint_action'];h=doubled_hessian(action)
        terms=[x for x in self.join['cross_intervals'] if x['coefficient']]
        self.assertEqual(len(terms),5)
        for x in terms:
            i,j,c=x['source'],x['target'],x['coefficient']
            dropped=deepcopy(action);dropped['pair_terms'].remove([i,j,c]);dropped['F4']+=c
            hd=doubled_hessian(dropped)
            self.assertEqual(h[i][j]-hd[i][j],c)
            self.assertNotEqual(action['F4'],dropped['F4'])

    def test_measure_factor_two_and_seam_phase_are_needed(self):
        value=gaussian_atom(self.join['joint_action'])
        self.assertFalse(value.overlaps(value/2))
        phase=influence_components(self.join,self.fields)
        self.assertEqual(phase['gravity_over_kappa'],'14') # Delta F=16 minus seam F=2.
        self.assertEqual(phase['dust_constant'],'7/16')
        factor=evaluate_influence(self.join,self.fields,'1/7')
        q2=sum(float(Fraction(self.fields['q'][str(x)]))**2 for x in (3,4))
        import math
        self.assertAlmostEqual(abs(factor),2*math.exp(-q2/14),places=14)
        with self.assertRaises(ValueError):evaluate_influence(self.join,self.fields,'-1')

    def test_regulated_integration_order(self):
        for e in ('1','1/7'):
            self.assertTrue(gaussian_atom(self.join['joint_action'],e).overlaps(
                gaussian_atom(self.join['joint_action'],e,(2,5,3,4)+OUTER)))

    def test_packet_tamper_missing_memory_and_incompatible_rules(self):
        p=deepcopy(self.left);p['profiles'][0]['footprint']=0
        with self.assertRaises(ValueError):sew_packets(p,self.right)
        with self.assertRaises(ValueError):sew_packets(seal(p),self.right)
        p=deepcopy(self.left);del p['field_memory']['0']
        with self.assertRaises(ValueError):sew_packets(seal(p),self.right)
        p=deepcopy(self.right);del p['field_memory']['5']['density']
        with self.assertRaises(ValueError):sew_packets(self.left,seal(p))
        p=deepcopy(self.left);p['scalar_parameters']['mass']=1
        with self.assertRaises(ValueError):sew_packets(seal(p),self.right)
        p=deepcopy(self.right);p['completion']='all_global_extensions'
        with self.assertRaises(ValueError):sew_packets(self.left,seal(p))

    def test_seam_relabelling_covariance(self):
        # Non-symmetric histories force a nontrivial change of profile bit positions.
        l,r=8476,8592;perm={i:(7-i if i in (3,4) else i) for i in range(8)}
        lp=make_packet('left',range(5),{(perm[i],perm[j]) for i,j in pc.relations(l)},(3,4),(0,1))
        rp=make_packet('right',range(3,8),{(perm[i+3],perm[j+3]) for i,j in pc.relations(r)},(3,4),(6,7))
        original=sew_packets(*packets(l,r))['joint_action'];changed=sew_packets(lp,rp)['joint_action']
        self.assertEqual(changed['pair_terms'],sorted([[perm[i],perm[j],c] for i,j,c in original['pair_terms']]))
        self.assertEqual(changed['F4'],original['F4'])

    def test_bypass_relations_are_missing_information(self):
        witness=bypass_witness()
        self.assertTrue(witness['same_local_restrictions'])
        self.assertNotEqual(witness['minimal_F4'],witness['alternative_F4'])

    def test_full_sum_has_distributional_histories(self):
        record=json.loads((Path(__file__).parent/'results/verification.json').read_text())
        self.assertEqual(record['singular_inner_blocks'],32)
        self.assertTrue(record['all_singular_null_modes_couple_to_boundary'])
        self.assertEqual(record['exact_joint_action_matches'],1089)

    def test_capped_profiles_on_larger_finite_orders(self):
        rng=random.Random(4107);reached_cap=False
        for _ in range(100):
            vl=tuple(range(8));vr=tuple(range(6,14));seam=(6,7)
            rl=transitive_closure(vl,{(i,j) for i in vl for j in vl if i<j and i<6 and rng.random()<0.55})
            rr=transitive_closure(vr,{(i,j) for i in vr for j in vr if i<j and j>7 and rng.random()<0.55})
            left=make_packet('left',vl,rl,seam,(0,1));right=make_packet('right',vr,rr,seam,(12,13))
            result=sew_packets(left,right)
            direct=local_action(range(14),transitive_closure(range(14),rl|rr))
            self.assertEqual(result['joint_action'],direct)
            reached_cap|=any(x['interval_count_capped']==4 for x in result['cross_intervals'])
        self.assertTrue(reached_cap)

if __name__=='__main__':unittest.main()
