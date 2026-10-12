# Primärquellen und genaue Rolle

Geprüfte Onlinequellen, Abruf 2026-10-12. Die Literatur stützt bestimmte Bausteine,
nicht die Validierung dieser neuen Implementierung. Keine Messzahl aus einer
Publikation wird als eigenes Messergebnis übernommen.

- **R1:** Y. Li, Z.-Y. Zhou, D.-S. Ding, B.-S. Shi,
  *CW-pumped telecom band polarization entangled photon pair generation in a
  Sagnac interferometer*, Optics Express 23, 28792–28800 (2015).
  [DOI](https://doi.org/10.1364/OE.23.028792),
  [Autorenfassung](https://arxiv.org/abs/1510.08191).
  Rolle: experimentelles Beispiel einer ppKTP-Sagnac-Quelle bei 1550 nm;
  keine Validierung unserer hypothetischen Stückliste oder Quellstatistik.
- **R2:** C. Ho, A. Lamas-Linares, C. Kurtsiefer,
  *Clock synchronization by remote detection of correlated photon pairs*,
  New Journal of Physics 11, 045011 (2009).
  [DOI](https://doi.org/10.1088/1367-2630/11/4/045011),
  [Autorenfassung](https://arxiv.org/abs/0901.3203).
  Rolle: alternative korrelationsbasierte Offset-/Frequenzsynchronisation.
  Dieser Algorithmus ist hier nicht implementiert; v0.1 nutzt bekannte
  synthetische Referenzpulse und affine Regression.
- **R3:** Y. Shi et al., *Entanglement Distribution over a
  Polarization-Stabilized Aerial Fiber*, arXiv:2601.11753 (2026).
  [Primärfassung](https://arxiv.org/abs/2601.11753).
  Rolle: reale Polarisationsstabilisierung und verteilte Photonenpaarmessung
  sind experimentelle Ingenieursaufgaben. Die Veröffentlichung belegt keine
  Leistung oder Überlegenheit unseres Aufbaus.
- **R4:** CERN White Rabbit Collaboration,
  [WR Technology](https://white-rabbit-collaboration-website.web.cern.ch/wr-technology/).
  Rolle: offizielle technische Beschreibung einer möglichen Zeitreferenz.
  Die Synchronisationsangaben beziehen sich auf passende WR-Knoten/-Switches.
  Hier werden weder WR-Code noch Hardware integriert oder deren Leistung behauptet.
- **R5:** G. Vidal, R. F. Werner, *Computable measure of entanglement*,
  Physical Review A 65, 032314 (2002).
  [DOI](https://doi.org/10.1103/PhysRevA.65.032314).
  Rolle: Definition und Einordnung der Negativität für bekannte Dichtematrizen.
  Die Kenntnis dieser Matrix ist im Simulator gegeben, im Experiment nicht automatisch.
- **R6:** R. K. L. Colmenar, U. Güngördü, J. P. Kestner,
  *Conditions for Equivalent Noise Sensitivity of Geometric and Dynamical
  Quantum Gates*, PRX Quantum 3, 030310 (2022).
  [DOI](https://doi.org/10.1103/PRXQuantum.3.030310).
  Rolle: Gegenargument gegen eine pauschale Ableitung von Robustheit aus
  geometrischer Implementierung. Die Arbeit untersucht Gatter und ist kein
  vollständiges No-go-Theorem für alle denkbaren optischen Kodierungen.
- **R7:** C. H. Bennett, G. Brassard, N. D. Mermin,
  *Quantum cryptography without Bell's theorem*, Physical Review Letters 68,
  557 (1992). [DOI](https://doi.org/10.1103/PhysRevLett.68.557).
  Rolle: ursprüngliche Protokollidee einer verschränkungsbasierten
  Schlüsselverteilung; ersetzt keine moderne gerätespezifische endliche
  Sicherheitsanalyse dieses Projekts.

Die dB-Umrechnung, OU-Übergangsverteilung, Born-Wahrscheinlichkeiten,
Poisson-Ausdünnung, affine Kalibrierung und der feste-Fenster-Retentionsintegral
sind in `MODEL.md` spezifiziert und durch ausführbare Grenz-/Referenztests
geprüft. Die benannten Veröffentlichungen werden nicht als angeblicher
Peer-Review dieses Codes verwendet.
