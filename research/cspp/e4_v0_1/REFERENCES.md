# Primärquellen und Claim-Grenzen

Geprüft am 27. Oktober 2026. Quellen motivieren die Prüfungen; keine Quelle
validiert den noch nicht implementierten E4-Kandidaten. Eigene Designzahlen
im Vertrag sind nicht aus diesen Veröffentlichungen abgeleitet.

1. Belenchia, Benincasa, Dowker: *The continuum limit of a 4-dimensional
   causal set scalar d'Alembertian*, CQG 33 (2016) 245018.
   https://arxiv.org/abs/1510.04656v2
   Behandelt den Grenzwert des Mittels unter Voraussetzungen sowie getrennt
   Fluktuationen und Glättung. Kein pauschales endliches Einzelwolkenzertifikat.
2. Boguñá, Krioukov: *Local d'Alembertian for causal sets*, PRD 113 (2026)
   024046. https://doi.org/10.1103/np89-qzjp
   https://arxiv.org/abs/2506.18745
   Lokaler Minkowski-Kandidat. Deshalb keine universelle Zwangsannahme
   nichtlokaler Operatoren. Unsere lokale Implementierung bleibt separat zu prüfen.
3. Johnston: *Quantum Fields on Causal Sets*, Dissertation (2010), Kapitel 6.
   https://arxiv.org/abs/1010.5514
   Spin-half-/Propagatoransätze und Mehrdeutigkeit der Quadratwurzel.
   Die bloße Quadratbeziehung qualifiziert keinen Dirac-Operator.
4. Kay: *Editorial note to: Erwin Schrödinger, Dirac electron in the
   gravitational field I*, GRG 52 (2020) 3, mit Addendum.
   https://arxiv.org/abs/1906.10765v7
   Herleitung/Einordnung der Spinverbindung und der R/4-Struktur beim
   quadrierten Dirac-Operator. Krümmung ist aus E4-V0.1 ausgeschlossen.
5. Giunti: *Neutrino Wave Packets in Quantum Field Theory*, JHEP 0211 (2002)
   017. https://arxiv.org/abs/hep-ph/0205014v2
   Produktion, Detektion und Wellenpakete sind für physikalische
   Flavorinterpretation wesentlich. Der kompakte E4-Eingang ist ein Toymodell.
6. Howard, Ramdas, McAuliffe, Sekhon: *Time-uniform, nonparametric,
   nonasymptotic confidence sequences*, Ann. Statist. 49 (2021) 1055–1080.
   https://arxiv.org/abs/1810.08240v9
   Grundlage für eine mögliche spätere adaptive Stoppregel. Der aktuelle
   Entwurf verwendet feste Stichproben und die unten angegebene Schranke.
7. Hoeffding: *Probability Inequalities for Sums of Bounded Random
   Variables*, JASA 58 (1963) 13–30.
   https://doi.org/10.1080/01621459.1963.10500830
   Für unabhängige Xi in [a,b] gilt
   P(|mean(X)-E[X]|>=h) <= 2 exp(-2 M h^2/(b-a)^2).
   Die Kampagnenformel folgt durch Vereinigungsabschätzung für K Größen.
8. NumPy 2.3: Parallel RNG und Kompatibilität.
   https://numpy.org/doc/2.3/reference/random/parallel.html
   https://numpy.org/doc/2.3/reference/random/compatibility.html
   Explizite Generatoren und SeedSequence; Seed allein ist keine beliebige
   plattform-/versionsübergreifende Reproduktionsgarantie.
9. Python: `assert`-Semantik.
   https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
   Assertions können unter Optimierung entfallen. Wissenschaftliche
   Ausführungs-/Freeze-Sperren müssen explizite Kontrollpfade benutzen.

Repository-Bezug: [Eigenzeit v0.5](../../eigenzeit_4d/constrained_region_v0_5/README.md),
[lokaler Operatorzweig](../../lorentz_local_dalembert/README.md).
Es wird kein Neuheitsanspruch und keine externe Begutachtung behauptet.
