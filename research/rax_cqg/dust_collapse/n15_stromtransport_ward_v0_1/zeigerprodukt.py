"""Exact generator and readout equations for the constant two-arm metric."""
import json

def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def commutes(a, b):
    return matmul(a,b) == matmul(b,a)


def check():
    # Generator of the controlled phase, and the two-outcome Y observable.
    generator = [[0,0],[0,1]]
    readout = [[0,-1j],[1j,0]]
    # Contrast-positive metrics with different diagonal weights, plus a
    # positive definite off-diagonal example. All entries are exactly
    # representable Gaussian integers.
    examples = [[1,0,1], [1,0,3], [2,1+1j,2]]
    rows = []
    for a,b,d in examples:
        g = [[a,b],[complex(b).conjugate(),d]]
        assert a>0 and a*d>int(complex(b).real)**2+int(complex(b).imag)**2
        respects_source = commutes(generator,g)
        respects_y = commutes(readout,g)
        assert respects_source == (b==0)
        assert respects_y == (a==d and complex(b).real==0)
        rows.append({'G00':a,'G11':d,'Re_G01':int(complex(b).real),'Im_G01':int(complex(b).imag),
                     'quelle_isometrisch':respects_source,'Y_selbstadjungiert':respects_y})
    return {'klasse':'gemeinsame konstante positiv definite hermitesche 2x2-Zeigermetrik',
            'quelle_allein':'diag(a,d), a,d>0',
            'quelle_und_unveraenderte_projektive_Y_auslese':'a*Identitaet, a>0',
            'beispiele':rows,'physikalische_paarung_gekoppelter_rand':'HOLD'}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Bitte ohne -O ausführen.')
    print(json.dumps(check(), indent=2, ensure_ascii=False))
