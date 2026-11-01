# Primärquellen und Projektbezug

1. David Tong, *Quantum Field Theory*, Kapitel 2, Abschnitt 2.7,
   Gleichung (2.90): positiver Frequenzkern des freien Skalarfeldes.
   [Universität Cambridge](https://www.damtp.cam.ac.uk/user/tong/qft/two.pdf).
   Die Gaußmittelung und die positive Integraltransformation dieses
   Prüfpakets sind in DERIVATION.md selbst hergeleitet.
2. T. Rick Perche, *Closed-form expressions for smeared bidistributions of
   a massless scalar field: Nonperturbative and asymptotic results in
   relativistic quantum information*, Physical Review D 110, 025013 (2024).
   [DOI](https://doi.org/10.1103/PhysRevD.110.025013).
   Literaturbezug für wohldefinierte raumzeitliche Gaußmittelung; die
   konkrete Normierung und massive Erweiterung sind hier ausdrücklich
   festgelegt und gegengeprüft.
3. Wassily Hoeffding, *Probability Inequalities for Sums of Bounded Random
   Variables*, Journal of the American Statistical Association 58, 13-30
   (1963). [DOI](https://doi.org/10.1080/01621459.1963.10500830).
   Grundlage der bedingten endlichen Fehlerschranke für die unabhängigen
   Vorzeichenindikatoren. Die Gauß-Orthantenformel wird im Paket über
   den gleichverteilten Winkel hergeleitet und numerisch gegengeprüft.
4. JCGM 100:2008, *Guide to the expression of uncertainty in measurement*,
   insbesondere Abschnitt 8.
   [BIPM](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf).
5. JCGM 100:2008/Amd.1:2026, *Nonlinearity in measurement models*.
   [Offizieller DOI](https://doi.org/10.59161/PPDI3267).
6. JCGM 102:2011, *Extension to any number of output quantities*,
   Abschnitte 6.2, 6.5, 7.1.7, 7.2.1 und 7.7.
   [BIPM](https://www.bipm.org/documents/20126/2071204/JCGM_102_2011_E.pdf).
   Grundlage der gemeinsamen Kovarianz- und Verteilungsfortpflanzung.
7. JCGM 101:2008, *Propagation of distributions using a Monte Carlo method*.
   [Offizieller DOI](https://doi.org/10.59161/JCGM101-2008).
8. JCGM 106:2012, *The role of measurement uncertainty in conformity
   assessment*.
   [BIPM](https://www.bipm.org/documents/20126/2071204/JCGM_106_2012_E.pdf).
   Bezug für die Trennung von Unsicherheitsangabe und Entscheidungsrisiko;
   die konkrete Zweimodellregel dieses Pakets wird eigenständig bewiesen.

Die [JCGM-Publikationsliste](https://www.bipm.org/en/committees/jc/jcgm/publications)
wurde einschließlich der Ergänzung 2026 geprüft. Die Referenzen begründen
keinen experimentellen Genauigkeitsnachweis dieses Projekts.

Vorgänger ist [KVF-Entwurf v0.13, PR #176](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/176),
Commit a8f4b7dafb79b5ebcdf919b8187b387f8d4935e6. Die unveränderten
Dokumente und ihre Hashes sind unter previous/ enthalten. Dort stehen
auch die experimentellen elektrooptischen Literaturbezüge. Es werden
keine Fremdabbildungen oder fremden Volltexte mitgeliefert.
