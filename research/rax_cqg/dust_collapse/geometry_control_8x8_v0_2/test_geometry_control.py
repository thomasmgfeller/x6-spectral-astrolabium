#!/usr/bin/env python3
"""Regression tests for the reviewed basis, mixing, validation and export failures."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import numpy as np
import cst_dust_geometry_kernel_8x8 as g

class GeometryControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='cst-geometry8-test-')
        self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def cli(self,*args):
        output=self.root/'result.npz'
        result=subprocess.run([sys.executable,'-O','-B',str(Path(g.__file__)),*args,'--output',str(output)],capture_output=True,text=True)
        return result,output
    def test_three_exact_source_phases(self):
        for phase,z in g.PHASES.items():
            with self.subTest(phase=phase):
                self.assertTrue(np.array_equal(g.kernels(z),np.array(g.EXPECTED[phase])))
                self.assertEqual(g.source_controls()[phase],'PASS_EXACT_GAUSSIAN_INTEGER_EVALUATION')
    def test_basis_conversion_and_old_block_trap(self):
        kg,k=g.build8(1)
        inverse=np.argsort(g.PERMUTATION)
        old=k[np.ix_(inverse,inverse)]
        self.assertTrue(np.array_equal(old[:4,4:],26*np.eye(4)))
        self.assertTrue(np.array_equal(k[:4,4:],np.zeros((4,4))))
        self.assertTrue(np.array_equal(k[4:,:4],np.zeros((4,4))))
        self.assertEqual(g.BASIS,['A|0|0m','A|0|1m','K|0|0m','K|0|1m','A|+|0m','A|+|1m','K|+|0m','K|+|1m'])
    def test_diagonal_residual_is_not_mixing(self):
        kg,k=g.build8(1);k[0,0]+=1;d,_=g.diagnostics(kg,k)
        self.assertEqual(d['tensor_residual_fro'],1)
        self.assertEqual(d['stratum_mixing_fro'],0)
        self.assertEqual(d['matter_mixing_fro'],0)
    def test_stratum_mixing_is_detected(self):
        kg,k=g.build8(1);k[0,4]=1;d,_=g.diagnostics(kg,k)
        self.assertEqual(d['stratum_mixing_fro'],1);self.assertEqual(d['matter_mixing_fro'],0)
        with self.assertRaises(g.FixtureError):g.validate_fixture(kg,k)
    def test_matter_mixing_is_detected(self):
        kg,k=g.build8(1);k[0,1]=1;d,_=g.diagnostics(kg,k)
        self.assertEqual(d['matter_mixing_fro'],1);self.assertEqual(d['stratum_mixing_fro'],0)
        with self.assertRaises(g.FixtureError):g.validate_fixture(kg,k)
    def test_geometry_change_is_not_label_mixing(self):
        kg,k=g.build8(1);k[0,2]+=1;d,_=g.diagnostics(kg,k)
        self.assertEqual(d['tensor_residual_fro'],1);self.assertEqual(d['either_label_mixing_fro'],0)
    def test_exact_determinants_and_defects(self):
        expected={'1':([24,0],35421700),'-1':([-12,0],1156),'i':([70,6],1075652)}
        for phase,(det,squared) in expected.items():
            with self.subTest(phase=phase):
                data=g.exact_phase_data(phase);self.assertEqual(data['det_K_geom'],det)
                self.assertEqual(data['defect_8x8_I8_fro_squared'],squared)
        self.assertEqual(g.exact_phase_data('1')['defect_geom_I2'],[[[1900,0],[1430,0]],[[1430,0],[1075,0]]])
    def test_nonfinite_cli_rejected_without_outputs(self):
        for args in [('--z-real','nan'),('--z-real','inf'),('--z-imag','nan'),('--kappa','inf')]:
            with self.subTest(args=args):
                result,out=self.cli(*args);self.assertEqual(result.returncode,2)
                self.assertFalse(out.exists());self.assertFalse(out.with_suffix('.json').exists())
    def test_zero_cli_rejected(self):
        result,out=self.cli('--z-real','0','--z-imag','0')
        self.assertEqual(result.returncode,2);self.assertFalse(out.exists())
    def test_conflicting_modes_rejected(self):
        result,out=self.cli('--phase','1','--kappa','0')
        self.assertEqual(result.returncode,2);self.assertFalse(out.exists())
    def test_overflow_cli_rejected(self):
        for value in ['1e300','1e-300']:
            with self.subTest(value=value):
                result,out=self.cli('--z-real',value)
                self.assertEqual(result.returncode,2);self.assertFalse(out.exists())
    def test_wrong_suffix_rejected(self):
        with self.assertRaises(g.FixtureError):g.create_dataset(1,self.root/'wrong.bin')
        self.assertEqual(list(self.root.iterdir()),[])
    def test_failed_source_control_stops_export(self):
        out=self.root/'bad.npz'
        with mock.patch.object(g,'kernels',return_value=np.zeros((2,2))),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(g.main(['--output',str(out)]),2)
        self.assertFalse(out.exists());self.assertFalse(out.with_suffix('.json').exists())
    def test_failed_structure_control_stops_export(self):
        kg,k=g.build8(1);k[0,4]=1;out=self.root/'bad.npz'
        with mock.patch.object(g,'build8',return_value=(kg,k)),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(g.main(['--output',str(out)]),2)
        self.assertFalse(out.exists());self.assertFalse(out.with_suffix('.json').exists())
    def test_nonfinite_matrix_rejected(self):
        kg,k=g.build8(1);k[0,0]=float('nan')
        with self.assertRaises(g.FixtureError):g.validate_fixture(kg,k)
    def test_pickle_free_export_and_metadata(self):
        out=self.root/'data.npz';r=g.create_dataset(1,out)
        with np.load(out,allow_pickle=False) as a:
            self.assertNotIn('channel_dim',a.files);self.assertNotIn('G_in',a.files)
            self.assertEqual(a['n_channels'].item(),2);self.assertEqual(a['states_per_channel'].item(),4)
            self.assertEqual(a['basis'].tolist(),g.BASIS);self.assertEqual(a['K'].shape,(8,8))
            self.assertTrue(np.array_equal(a['G_in_diagnostic'],np.eye(8)))
        self.assertIsNone(r['physical_gram']);self.assertIsNone(r['delta_chi'])
        self.assertEqual(r['physical_8x8_matter_matrix'],'NOT_CONSTRUCTED')
        self.assertTrue(all(v=='HOLD' for v in r['physical_gates'].values()))
        json.loads(out.with_suffix('.json').read_text(),parse_constant=lambda x:self.fail('Nonstandard JSON constant: '+x))
    def test_deterministic_export(self):
        a=self.root/'a.npz';b=self.root/'b.npz'
        g.create_dataset(1j,a);g.create_dataset(1j,b)
        self.assertEqual(a.read_bytes(),b.read_bytes())
        self.assertEqual(a.with_suffix('.json').read_bytes(),b.with_suffix('.json').read_bytes())
    def test_general_phase_is_numeric_only(self):
        r=g.create_dataset(complex(np.exp(.37j)),self.root/'numeric.npz')
        self.assertIsNone(r['exact_source_phase_data']);self.assertIsNone(r['physical_clock'])
        self.assertIsNone(r['physical_kernel_convention']);self.assertFalse(r['physical_kernel'])
    def test_source_hash_tamper_rejected(self):
        with mock.patch.object(g,'SOURCE_SHA256','0'*64):
            with self.assertRaises(g.FixtureError):g.create_dataset(1,self.root/'bad.npz')
        self.assertEqual(list(self.root.iterdir()),[])

class RecordingResult(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.passed=[]
    def addSuccess(self,test):super().addSuccess(test);self.passed.append(test._testMethodName)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(GeometryControlTests)
    result=unittest.TextTestRunner(verbosity=1,resultclass=RecordingResult).run(suite)
    record={'test_count':result.testsRun,'passed':sorted(result.passed),'failures':len(result.failures),'errors':len(result.errors),
            'scope':'software regression and exact finite source controls; no physical validation'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(g.canonical(record),encoding='utf-8')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':sys.exit(main())
