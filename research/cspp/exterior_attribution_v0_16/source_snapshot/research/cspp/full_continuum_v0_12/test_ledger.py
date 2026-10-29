import unittest
from flint import arb,acb,ctx
from run import split_error


class LedgerTests(unittest.TestCase):
    def setUp(self):ctx.prec=128

    def test_exact_signed_cancellation(self):
        # One history node, one evolved node with weight 2.
        q=[acb(1),acb(3)];qhat=[acb(2),acb(4)];T=[acb(7)]
        z=split_error(q,qhat,T,[acb(5)],[acb(6)],[acb(4)],[acb(6),acb(12)],acb(61),acb(20))
        def v(name):return arb(z['components'][name]['value'][0])
        self.assertEqual(v('adapter'),7)
        self.assertEqual(v('operator_domain'),8)
        self.assertEqual(v('integration'),25)
        self.assertEqual(v('solution'),1)
        self.assertEqual(arb(z['total_error'][0]),41)

    def test_zero_local_source_has_zero_numerical_terms(self):
        z=split_error([acb(1)],[acb(2)],[acb(1)],[acb(0)],[acb(0)],[acb(3)],[acb(0)],acb(0),acb(4))
        self.assertEqual(arb(z['components']['integration']['value'][0]),0)
        self.assertEqual(arb(z['components']['solution']['value'][0]),0)
        self.assertEqual(arb(z['total_error'][0]),-4)

    def test_interval_uncertainty_never_claimed_dominant(self):
        q=[acb(arb(1,2))];T=q
        z=split_error(q,[acb(1)],T,[acb(2)],[acb(2)],[acb(1)],[acb(2)],acb(2),acb(1))
        self.assertEqual(z['dominant_component'],'UNRESOLVED')


if __name__=='__main__':unittest.main(verbosity=2)
