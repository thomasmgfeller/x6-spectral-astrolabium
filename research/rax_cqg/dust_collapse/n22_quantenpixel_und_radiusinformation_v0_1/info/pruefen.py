"""Diagnostik für einen explizit vorgegebenen reinen Zustand im orthonormalen Produktregister."""
from fractions import Fraction as Q
import json
from pathlib import Path


def linear_entropy(coefficients):
    """Jede Zeile gehört zu A, jede Spalte zu B. Eintrag = (rationaler Real-, Imaginärteil)."""
    if not coefficients or not coefficients[0]:
        raise ValueError('Beide Register benötigen mindestens einen Basiszustand.')
    width = len(coefficients[0])
    if any(len(row) != width for row in coefficients):
        raise ValueError('Koeffizienten müssen ein Rechteck bilden.')
    matrix = [[(Q(r), Q(i)) for r, i in row] for row in coefficients]
    norm = sum(r*r+i*i for row in matrix for r,i in row)
    if not norm:
        raise ValueError('Der Nullvektor definiert keinen normierten Zustand.')
    # Purity = Sum_ab |(C C^dagger)_ab|² / norm² für ein orthonormales Produktregister.
    sum_squares = Q(0)
    for row_x in matrix:
        for row_y in matrix:
            pairs = list(zip(row_x, row_y, strict=True))
            real = sum(a*c+b*d for (a,b),(c,d) in pairs)
            imag = sum(b*c-a*d for (a,b),(c,d) in pairs)
            sum_squares += real*real+imag*imag
    return 1-sum_squares/(norm*norm)


def controlled_phase(real, imag):
    if Q(real)**2+Q(imag)**2 != 1:
        raise ValueError('Die Phase hat Betrag eins.')
    # Der Normierungsfaktor 1/2 darf hier entfallen, weil linear_entropy selbst normiert.
    return [[(1,0),(1,0)],[(1,0),(real,imag)]]


def check():
    phases = [(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(3,5),Q(4,5))]
    same_diagonal = []
    for r,i in phases:
        coefficients = controlled_phase(r,i)
        probabilities = [(Q(a)**2+Q(b)**2)/4 for row in coefficients for a,b in row]
        assert probabilities == [Q(1,4)]*4
        value = linear_entropy(coefficients)
        assert value == (1-r)/4
        same_diagonal.append({'phase_real':str(r),'phase_imag':str(i),
                              'probabilities':list(map(str,probabilities)),'linear_entropy':str(value)})
    assert [r['linear_entropy'] for r in same_diagonal] == ['0','1/2','1/4','1/10']

    # |00> und |11> sind Produktzustände. Ihre gleiche Mischung ist auch die gleiche
    # Mischung von (|00>±|11>)/sqrt(2), mit abweichender Komponentenentropie.
    purified_examples=[[(1,0,0,0),(0,0,0,1)],[(1,0,0,1),(1,0,0,-1)]]
    mixtures = []
    averages = []
    for vectors in purified_examples:
        p = [[Q(0) for _ in range(4)] for _ in range(4)]
        av = Q(0)
        for v in vectors:
            norm = sum(t*t for t in v)
            for a,x in enumerate(v):
                for b,y in enumerate(v):
                    p[a][b] += Q(x*y,2*norm)
            c=[[(x,0) for x in v[:2]],[(x,0) for x in v[2:]]]
            av += linear_entropy(c)/2
        mixtures.append(p)
        averages.append(av)
    assert mixtures[0] == mixtures[1] and averages == [0,Q(1,2)]

    # Basis e0,e1 hat Überlappung 1/2. Die Koordinaten des Vektors sind (1,1).
    gram=[[Q(1),Q(1,2)],[Q(1,2),Q(1)]]
    q=[Q(1),Q(1)]
    bra=[sum(q[a]*gram[a][j] for a in range(2)) for j in range(2)]
    norm=sum(x*y for x,y in zip(bra,q,strict=True))
    naive = sum(x*x for x in q)/norm
    correct = sum(q[j]*bra[j] for j in range(2))/norm
    assert (norm,naive,correct) == (3,Q(2,3),1)
    # Nullvektor und normierter Modellvakuumvektor sind zwei verschiedene Eingaben.
    try:
        linear_entropy([[(0,0)]])
    except ValueError:
        pass
    else:
        raise AssertionError('Nullvektor wurde akzeptiert')
    assert linear_entropy([[(1,0),(0,0)],[(0,0),(0,0)]]) == 0
    return {'type':'Algebraische Kontrollen auf ausdrücklich gewählten Hilberträumen',
            'same_joint_diagonal':same_diagonal,
            'mean_pure_linear_entropy_same_mixed_state':list(map(str,averages)),
            'coordinate_density_N_naive_trace_correct_trace':list(map(str,(norm,naive,correct)))}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Ohne -O starten.')
    result=json.dumps(check(),ensure_ascii=False,indent=2)+'\n'
    if (Path(__file__).parent/'Ergebnisse.json').read_text() != result:
        raise ValueError('Abweichung vom archivierten Ergebnis.')
    print('Vier phasenverschiedene Zustände, zwei Zerlegungen, Gram-Normierung und Nullvektor geprüft.')
