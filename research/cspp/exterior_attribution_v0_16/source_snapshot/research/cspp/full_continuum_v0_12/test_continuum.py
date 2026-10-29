"""Independent identities and integral controls for the full detector reduction."""
import unittest
from flint import arb,acb,fmpq as Q,fmpq_poly as Poly,ctx
import continuum as c


class ContinuumTests(unittest.TestCase):
    def setUp(self):ctx.prec=128

    def test_detector_ball_volume(self):
        for R in ['1','3/2','2']:
            r=acb(R);b=acb('1/2')
            z=c.integral(lambda x,_:arb.pi()/r*x*(b*b-(x-r)**2),r-b,r+b)
            self.assertTrue(z.real.overlaps(arb.pi()/6))

    def test_first_massive_full_ball_term(self):
        p=c.detector_poly('3','full',0,1)
        self.assertEqual(p,Poly([0,-Q(1,12)]))

    def test_massless_lightcone_ball_intersection(self):
        p=c.detector_poly('2','partial',16,0)
        self.assertEqual(p,Poly([-Q(15,4),4,-1]))
        self.assertEqual(c.detector_poly('2','full',16,0),Poly([]))

    def test_analytic_gaussian_moments(self):
        for n in [0,1,2,5,12]:
            v=c.gaussian_moments(acb('5/4'),acb('7/4'),n)[n]
            w=c.integral(lambda r,_:r**n*(acb(0,-Q(4,3))*r*r).exp(),'5/4','7/4')
            self.assertTrue(v.overlaps(w))

    def test_zero_carrier_moments(self):
        v=c.gaussian_moments(1,2,6,k=0)
        self.assertTrue(v[6].real.contains(arb(127)/7))

    def test_bessel_polynomial_against_entire_kernel(self):
        for tau in ['7/4','2','9/4']:
            for R in ['9/8','3/2','15/8']:
                t=arb(tau);r=arb(R);b=arb('1/2')
                regime='full' if r+b<=t else 'partial'
                upper=min(r+b,t);lower=r-b
                q=arb(0) if regime=='full' else b*b-(t-r)**2
                direct=q-c.integral(lambda x,_:x*(b*b-(x-r)**2)*(-(t*t-x*x)/4).hypgeom_0f1(2)/2,lower,upper)
                p=c.detector_poly(tau,regime,16,1)
                value=acb(p(acb(R).real.mid().fmpq()))
                # Kernel polynomial omitted term is bounded by maximum integrand.
                tail=(upper-lower)*upper*b*b/2*c.bessel_series_tail(t)
                self.assertTrue(c.inflate(value,tail).overlaps(direct))

    def test_causal_zero_before_arrival(self):
        z=c.endpoint('1/4')
        self.assertTrue(z['core'].is_zero())

    def test_common_time_endpoint_cancels(self):
        vals=[c.endpoint(t)['core'] for t in ['7/4','2','9/4']]
        first=(vals[1]-vals[0])/arb('1/4')
        second=(vals[2]-vals[1])/arb('1/4')
        combined=(vals[2]-vals[0])/arb('1/2')
        self.assertTrue(((first+second)/2).overlaps(combined))

    def test_bessel_tail_covers_degree_change(self):
        low=c.endpoint('2',degree=8);high=c.endpoint('2',degree=16)
        self.assertTrue(c.inflate(low['core'],low['series_tail']).overlaps(c.inflate(high['core'],high['series_tail'])))

    def test_source_cut_change_is_enclosed(self):
        a=c.endpoint('7/4',hcut_string='1/32');b=c.endpoint('7/4',hcut_string='1/64')
        self.assertTrue(c.inflate(a['core'],a['source_tail']+a['series_tail']).overlaps(c.inflate(b['core'],b['source_tail']+b['series_tail'])))

    def test_original_L2_normalization(self):
        A,I,tail=c.normalization()
        self.assertTrue((A*A*(I+arb(0).union(tail))).contains(1))
        self.assertTrue(A>0)

    def test_massive_tail_nonzero(self):
        massive=c.endpoint('2',mass=1)['core'];massless=c.endpoint('2',mass=0)['core']
        self.assertFalse(massive.overlaps(massless))


if __name__=='__main__':unittest.main(verbosity=2)
