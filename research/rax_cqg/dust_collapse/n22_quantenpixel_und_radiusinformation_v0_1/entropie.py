"""Exakte partielle Spur für einen gegebenen reinen Zustand in einer Produktbasis.

Benötigt SymPy. C[a,b] ist eine Amplitude, kein Dichtegewicht. G_in und
G_out enthalten die Gramprodukte <i|j> der beiden Basen. Bei Nullrichtungen
zuerst den physikalisch begründeten Quotienten und die Produktstruktur klären.
"""
from sympy import Float, I, Matrix, Rational, eye, simplify, sqrt, zeros


def reduzierte_dichte(C, G_in=None, G_out=None):
    C = Matrix(C)
    G_in = eye(C.rows) if G_in is None else Matrix(G_in)
    G_out = eye(C.cols) if G_out is None else Matrix(G_out)
    if not C.rows or not C.cols:
        raise ValueError("Leere Produktbasis.")
    for gram, size in ((G_in, C.rows), (G_out, C.cols)):
        if gram.shape != (size, size) or gram.is_hermitian is not True:
            raise ValueError("Gram-Matrix muss hermitesch und von passender Grösse sein.")
        if gram.is_positive_definite is not True:
            raise ValueError("Eine nachweislich positive definite Produktpaarung ist erforderlich.")
    if any(v.has(Float) for m in (C, G_in, G_out) for v in m):
        raise ValueError("Exakte Zahlen einsetzen, zum Beispiel Rational(1, 2).")
    # Koordinaten eines Operators mit einem kontravarianten und einem kovarianten Index.
    K = C * G_out.T * C.H * G_in
    norm = simplify(K.trace())
    if norm.is_positive is not True:
        raise ValueError("Zustandsnorm ist null oder nicht als positiv nachgewiesen.")
    return (K / norm).applyfunc(simplify)


def lineare_entropie(C, G_in=None, G_out=None):
    rho = reduzierte_dichte(C, G_in, G_out)
    return simplify(1 - (rho * rho).trace())


def kontrollen():
    half = Rational(1, 2)
    a = Matrix([[1, 1], [1, 1]]) / 2
    b = Matrix([[1, 1], [1, -1]]) / 2
    c = Matrix([[1, 1], [1, (1+I)/sqrt(2)]]) / 2
    for state in (a, b, c):
        assert all(simplify(x*x.conjugate()) == Rational(1, 4) for x in state)
    assert lineare_entropie(a) == 0
    assert lineare_entropie(b) == half
    assert simplify(lineare_entropie(c) - (2-sqrt(2))/8) == 0
    # Neue, nicht orthogonale Basen. Die physischen Zustände bleiben gleich.
    inside = Matrix([[1, 1+I], [0, 1]])
    outside = Matrix([[1, I], [I, 2]])
    for state in (a, b, c):
        new_coefficients = inside.inv() * state * outside.inv().T
        assert simplify(lineare_entropie(new_coefficients, inside.H*inside, outside.H*outside)
                        - lineare_entropie(state)) == 0
    try:
        lineare_entropie(zeros(2))
    except ValueError:
        pass
    else:
        raise AssertionError("Nullvektor wurde als normierter Zustand behandelt")
    return "Exakte Produkt-, Phasen-, Gram- und Nullvektorkontrollen bestanden."


if __name__ == "__main__":
    if not __debug__:
        raise RuntimeError("Ohne -O ausführen.")
    print(kontrollen())
