import json
import unittest
from pathlib import Path

import numpy as np

from agent.epta_filter import P, STUDY, hellings_downs, history_taps, prepare, regression_pairs
from agent.epta_timing import sky_unit
from agent.source_transport import sha256


class EptaTests(unittest.TestCase):
    def test_directions_and_hd(self):
        sky = np.array([sky_unit({"RAJ": "00:00:00", "DECJ": "-00:00:00"}),
                        sky_unit({"ELONG": "180", "ELAT": "0"}),
                        sky_unit({"RAJ": "06:00:00", "DECJ": "00:00:00"})])
        hd, angles = hellings_downs(sky)
        np.testing.assert_allclose(np.diag(hd), 1)
        self.assertAlmostEqual(hd[0, 1], 0.25)
        self.assertAlmostEqual(angles[0, 2], 90)
        self.assertGreater(np.linalg.eigvalsh(hd).min(), 0)

    def test_native_injection_equals_reduced_maps(self):
        # Independent explicit interpolation-free replay, including multi-frequency days and a gap.
        t = np.arange(0., 8041., 13.)
        t = np.sort(np.r_[t, t[::4]+.2])
        t = t[(t < 2200) | (t > 2390)]
        err = 1 + t%7 / 8
        coeff = np.linspace(-1, 1, 10)
        phase = 2*np.pi*t[:, None]*np.arange(1, 6)/t[-1]
        wave = np.c_[np.sin(phase), np.cos(phase)] @ coeff
        taps = history_taps()
        taps /= taps.sum()
        obs = {"name": "fixture", "bat": t, "us": wave, "error": err}
        p = prepare(obs, 0, t[-1], taps)
        np.testing.assert_allclose(p["maps"] @ coeff, p["measured"], atol=1e-9)
        np.testing.assert_allclose(p["measured"][0], coeff, atol=1e-9)
        groups = [np.flatnonzero(np.floor(t) == d) for d in np.unique(np.floor(t))]
        w = 1/err**2
        def avg(x, g):
            return np.average(x[g], axis=0, weights=w[g])
        day = np.array([avg(t, g) for g in groups])
        val = np.array([avg(wave, g) for g in groups])
        native = np.c_[np.ones(len(t)), t/t[-1], (t/t[-1])**2, np.sin(phase), np.cos(phase)]
        X, Y, W = [], [], []
        for i, cur in enumerate(day):
            ids = [np.flatnonzero((day <= cur-lag) & (day >= cur-lag-60)) for lag in (360, 180)]
            if all(len(x) for x in ids):
                X.append(avg(native, groups[i]))
                Y.append(taps @ val[[ids[0][-1], ids[1][-1], i]])
                W.append(np.sqrt(w[groups[i]].sum()))
        direct = np.linalg.lstsq(np.array(X)*np.array(W)[:,None], np.array(Y)*W, rcond=None)[0][3:]
        np.testing.assert_allclose(p["measured"][1], direct, atol=1e-9)

    def test_exact_covariance_by_symmetric_basis_injections(self):
        # Enumerating +/- sqrt(d) times a covariance square root gives exact second moments.
        rng = np.random.default_rng(7)
        sky = np.eye(3)
        hd, _ = hellings_downs(sky)
        coeff = np.array([0.7, 0.3, 0.7, 0.3])
        root = np.kron(np.linalg.cholesky(hd), np.diag(np.sqrt(coeff)))
        dim = len(root)
        s = np.concatenate([root.T, -root.T]).reshape(2*dim, 3, 4)*np.sqrt(dim)
        maps = rng.normal(size=(2,3,4,4))
        measured = rng.normal(size=(2,3,4))
        v = np.einsum("apij,bpj->bapi", maps, s)
        ij = np.triu_indices(3,1)
        direct = (regression_pairs(v+measured, ij)-regression_pairs(measured[None],ij)).mean(axis=0)
        expect = [hd[i,j]*np.sum(maps[:,i]*maps[:,j]*coeff,axis=(1,2))/2 for i,j in zip(*ij)]
        np.testing.assert_allclose(direct, np.array(expect).T, atol=1e-11)

    def test_published_reference(self):
        d = json.loads((STUDY/"reference.json").read_bytes())
        self.assertEqual(d["protocol_sha256"], sha256(STUDY/"protocol.json"))
        self.assertEqual(d["tempo_lock_sha256"], sha256(STUDY/"tempo2.lock"))
        self.assertEqual(sum(p["toas"] for p in d["pulsars"]), 22556)
        self.assertEqual(len(d["pairs"]), 28)
        self.assertEqual(sum(row[2] for row in d["reference_90d"]), 4069)
        self.assertAlmostEqual(d["arms"]["identity"]["expected_hd_power_projection"], 1, places=7)


if __name__ == "__main__":
    unittest.main()
