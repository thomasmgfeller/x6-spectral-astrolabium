"""Verify archived sources and reproduce the rational certificates offline."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
from beweis import study, ROOT
from kragenfrei import comparison


def calculate():
    if not __debug__:
        raise ValueError('Bitte Python ohne -O starten.')
    sources=json.loads((ROOT/'Quellen.json').read_bytes())
    for name,item in sources['files'].items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Quelle '+name)
    out=study()
    assert out['old_controls']==21 and out['direct_subcells']==168
    assert len(out['variants'])==4 and all(item['finite_difference_checks']==6 for item in out['variants'].values())
    for label in ['active_bounds','direct_bounds','device_removed_same_collar_bounds']:
        r=out[label]
        assert F('0.023')<=r['clock_raw'][0]<r['clock_raw'][1]<=F('0.144')
        assert r['D19_without_17'][1]<-15 and r['D18_only_17_to_19_upper']<-29 and r['D18_both_lower']>206
        assert r['narrow_vacuum_residual_upper']<0
    reported=out['active_bounds']
    assert reported['D19_without_17'][1] < F('-15.50')
    assert reported['D18_only_17_to_19_upper'] < F('-29.87') and reported['D18_both_lower'] > F('206.95')
    assert reported['minimum_normalized_gap'] > F('0.00218') and reported['signed_deficit'][0] > F('0.00836')
    assert reported['narrow_collar_deficit_lower'] > F('0.00866') and reported['old_clock_gap_upper'] < F('0.001062')
    velocity=out['unit_parameters']['max_abs_velocity']
    k=out['unit_parameters']['k']
    extra=comparison(velocity,k)
    assert extra['all_momenta_above_weight_floor']['load_per_weight_squared_upper']==F(1176,3125)
    out['collar_independent_supplement']=extra
    return out


def encode(value):
    def fraction(obj):
        if isinstance(obj,F):
            return str(obj)
        raise TypeError(type(obj).__name__)
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,default=fraction)+'\n').encode()


if __name__=='__main__':
    for name in ['SHA256SUMS','Pruefplan.sha256','Ergaenzung.sha256']:
        for line in (ROOT/name).read_text().splitlines():
            hashval,rel=line.split('  ',1)
            if sha256((ROOT/rel).read_bytes()).hexdigest()!=hashval:
                raise ValueError('Hash '+rel)
    if (ROOT/'Ergebnisse.json').read_bytes()!=encode(calculate()):
        raise ValueError('Ergebnisabweichung')
    print('PASS · 4 vollständige N21-Ordnungen · 24 Variationen der Wirkung · 21 Kragenfälle · 168 direkte Teilprüfungen.')
    print('Kein stationärer Sattel im vertraglichen Zielfenster. Physisches P3-Register: 60 NOT_RUN.')
