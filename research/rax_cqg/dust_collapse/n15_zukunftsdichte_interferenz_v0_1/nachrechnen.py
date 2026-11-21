"""Machine-readable exact certificate with three negative controls and optimality."""
from collections import Counter
import json

import zertifikat as cert
from optimal import compare


def legacy_control():
    # The earlier translated density vector d=(C2-C3,C3-C1,C1-C2)
    # has identically zero dot product with the three action coefficients.
    terms = Counter()
    for i,j,k in ((5,12,13),(12,13,5),(13,5,12)):
        terms[tuple(sorted((i,j)))] += 1
        terms[tuple(sorted((i,k)))] -= 1
    assert not any(terms.values())
    assert all((f,j) not in cert.ORDER for f in cert.F for j in (5,12,13))
    cert.ref.enclose(0)
    bounds = cert.ref.enclose(cert.ref.RADIUS)
    return {'p_durch_M_alte_zellen':bounds,'P_differenz_beider_ausgaenge':0}


def run():
    result = cert.run()
    pair,reference = cert.centers()
    result['optimum_flache_randpaarung'] = compare(pair,result['pakete'])
    result['kontrolle_altes_skalares_nullpaar'] = legacy_control()
    widths = {}
    for k in (24,23):
        radius = cert.Q(1,2**k)
        regions = {s:cert.whole_cell(v,reference,radius) for s,v in pair.items()}
        pos,neg = regions['positiv'],regions['negativ']
        pure = pos['p'][0]>0>neg['p'][1]
        gap = cert.sub(pos['P_Y_plus_minus_halb'],neg['P_Y_plus_minus_halb'])
        assert pure==(k==24) and gap[0]>0
        widths[str(radius)]={'p_positives_zentrum':pos['p'],'p_negatives_zentrum':neg['p'],
                             'vorzeichenreinheit_durch_einschluss_bewiesen':pure,'portluecke':gap}
    result['ergaenzende_breitenkontrolle'] = widths
    return result


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(run(),indent=2,ensure_ascii=False,default=str))
