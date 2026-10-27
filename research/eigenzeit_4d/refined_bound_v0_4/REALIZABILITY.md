# Physical consistency of the region-width witnesses

This diagnostic was added after the fresh experiment was frozen. It does
not alter the certifier, its thresholds, the data or the primary gate.

For five affinely independent anchors e0,...,e4, set e0=0 and let G be
their 4 by 4 Lorentzian Gram matrix. For either target a=p,q, polarization
gives the four anchor inner products

```text
b_a,i = (s_0i + s_0a - s_ia)/2,   i=1,...,4.
```

Affine independence makes the anchor vectors a basis. Any actual target
therefore necessarily satisfies

```text
b_a^T G^-1 b_a = s_0a.
```

The common positive scaling of the signed squared distances leaves these
equalities valid. They provide two exact consistency constraints that the
unrestricted twenty-cell confidence region in v0.3/v0.4 does not impose.

[realizability.py](realizability.py) evaluates both residuals with directed
interval arithmetic. It first checks the exact rational mean vectors of
all 20 original geometries: all 40 residual enclosures contain zero.
It then checks the ten explicit mean vectors in the five region-width
witness pairs. Every vector has at least one residual enclosure excluding
zero. Thus **none of these ten vectors realizes the stated flat-space
five-anchor model**. The complete intervals are in
[REALIZABILITY.json](REALIZABILITY.json).

This finding narrows the interpretation of the witnesses: they obstruct
certification over an unnecessarily large mean region, and do not provide
physical counterexamples. Intersecting the confidence region with these
exact model constraints would retain its original coverage under the
model, because the true parameter satisfies both constraints. Turning
that constrained region into a verified, computationally practical bound
is a separate next step. This diagnostic does not claim that the two
constraints alone characterize every physically admissible mean vector,
nor that they already yield additional 10% certificates.
