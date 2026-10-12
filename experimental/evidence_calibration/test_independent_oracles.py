"""Independent parity and rational numerical oracles; synthetic, not lab evidence."""
import itertools
import math
import random
import unittest
from fractions import Fraction
from .core import summarize_replicates
from .ecc import encode_hamming74, decode_hamming74
from .optical import frame_metrics, centroid_drift


def check_oracles():
    def require(condition,message):
        if not condition: raise AssertionError(message)

    def data_of(w): return [w[i] for i in (2,4,5,6)]
    def distance(a,b): return sum(x!=y for x,y in zip(a,b))
    words=list(itertools.product((0,1),repeat=7))
    # Oracle is specified as three explicit parity equations, not copied encoder XORs.
    codewords=[w for w in words if (w[0]+w[2]+w[4]+w[6])%2==0 and
        (w[1]+w[2]+w[5]+w[6])%2==0 and (w[3]+w[4]+w[5]+w[6])%2==0]
    require(len(codewords)==16,'Expected 16 parity-check solutions')
    encoded={tuple(encode_hamming74(list(d))) for d in itertools.product((0,1),repeat=4)}
    require(encoded==set(codewords),'Encoder differs from parity-check solution set')
    min_distance=min(distance(a,b) for a,b in itertools.combinations(codewords,2))
    require(min_distance==3,'Unexpected minimum distance')
    for word in words:
        ds=[distance(word,c) for c in codewords]; best=min(ds)
        require(ds.count(best)==1 and best<=1,'Code spheres do not partition 7-bit space')
        expected=data_of(codewords[ds.index(best)])
        require(decode_hamming74(list(word))['data']==expected,'Decoder/oracle disagreement')
    by_weight={str(k):{'cases':0,'original_data_recovered':0,'zero_syndrome_wrong_data':0} for k in range(8)}
    for cw in codewords:
        original=data_of(cw)
        for err in words:
            received=[a^b for a,b in zip(cw,err)]
            out=decode_hamming74(received)
            group=by_weight[str(sum(err))]; group['cases']+=1
            same=out['data']==original
            group['original_data_recovered']+=int(same)
            group['zero_syndrome_wrong_data']+=int(not same and out['syndrome']==0)
    require(by_weight['0']['original_data_recovered']==16,'Clean recovery failed')
    require(by_weight['1']['original_data_recovered']==112,'Single-bit recovery failed')
    require(by_weight['2']['original_data_recovered']==0,'Unexpected double-error behavior')

    rng=random.Random(104729)
    max_centroid_error=max_variance_error=max_sd_error=0.0
    for k in range(1000):
        h,w=rng.randint(1,8),rng.randint(1,8)
        f=[[rng.randint(0,1000) for _ in range(w)] for _ in range(h)]
        f[0][0]+=1
        total=sum(map(sum,f))
        cx=Fraction(sum(x*f[y][x] for y in range(h) for x in range(w)),total)
        cy=Fraction(sum(y*f[y][x] for y in range(h) for x in range(w)),total)
        vx=sum((Fraction(x)-cx)**2*f[y][x] for y in range(h) for x in range(w))/total
        vy=sum((Fraction(y)-cy)**2*f[y][x] for y in range(h) for x in range(w))/total
        m=frame_metrics(f)
        errors=[abs(m['centroid_x']-float(cx)),abs(m['centroid_y']-float(cy))]
        var_errors=[abs(m['sigma_x']**2-float(vx)),abs(m['sigma_y']**2-float(vy))]
        max_centroid_error=max(max_centroid_error,*errors)
        max_variance_error=max(max_variance_error,*var_errors)
        require(max(errors)<1e-12 and max(var_errors)<1e-12,'Rational optical oracle disagreement')
        values=[rng.randint(-100,100) for _ in range(rng.randint(2,20))]
        exact_mean=Fraction(sum(values),len(values))
        exact_variance=sum((Fraction(v)-exact_mean)**2 for v in values)/(len(values)-1)
        s=summarize_replicates(values)
        max_sd_error=max(max_sd_error,abs(s['sample_sd']-math.sqrt(float(exact_variance))))
        require(abs(s['sample_sd']-math.sqrt(float(exact_variance)))<1e-12,'SD oracle disagreement')

    # Method limitation, not a code-arithmetic bug: only uniform background changes.
    background_example=centroid_drift([[10,0,0]],[[20,10,10]])
    require(background_example['drift_pixels']==0.75,'Unexpected background example')

    return {"received_words": len(words), "codewords": len(codewords),
            "codeword_error_pairs": sum(g["cases"] for g in by_weight.values()),
            "by_error_weight": by_weight, "frames": 1000, "replicate_series": 1000,
            "seed": 104729, "absolute_tolerance": 1e-12,
            "max_centroid_error": max_centroid_error,
            "max_variance_error": max_variance_error, "max_sd_error": max_sd_error,
            "background_counterexample_pixels": background_example["drift_pixels"]}


class IndependentOracles(unittest.TestCase):
    def test_finite_domains_and_rational_references(self):
        self.assertEqual(check_oracles()["codeword_error_pairs"], 2048)
