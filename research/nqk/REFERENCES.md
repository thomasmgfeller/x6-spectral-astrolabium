# Quellen und Abgrenzung

## NQK-Ausgangspunkt

[Forschungsfassung 2.0](baseline/NQK_Forschungsfassung_2_0.pdf):
*Metrische Konsistenz und Quantenkorrelationen in endlichen Netzwerken*,
12. Oktober 2026. Intern erstellter Forschungsbericht mit KI-Unterstützung;
keine unabhängige Begutachtung behauptet. Die vollständige dort verwendete
Literaturliste steht in Abschnitt 16.

Die Roadmap ist eine neue Planung. Vorgeschlagene Nachweise und zukünftige
Funktionen sind keine Ergebnisse des Ausgangsberichts.

## Unmittelbare Fachliteratur

- Cao, Carroll, Michalakis (2017): [Space from Hilbert Space: Recovering Geometry
  from Bulk Entanglement](https://arxiv.org/abs/1606.08444).
  Direkte Vorarbeit zur geometrischen Rekonstruktion aus Quanteninformation.
  Die Verwendung von MI, logarithmischen Gewichten, Wegrekonstruktion und MDS
  wird in NQK nicht als neu beansprucht.
- Fawzi, Fawzi, Scalet (2024): [Entropy Constraints for Ground Energy
  Optimization](https://arxiv.org/abs/2305.06855).
  Schwache Monotonie als Grundlage der im NQK-Bericht angewendeten notwendigen
  Qubit-Kompatibilitätsbedingung.
- Watrous (2018): [The Theory of Quantum Information](https://cs.uwaterloo.ca/~watrous/TQI/).
  Zustände, Kanäle, Entropie und Datenverarbeitung. Keine Weiterverteilung des Buchtexts.
- Hein, Eisert, Briegel (2004): [Multiparty entanglement in graph
  states](https://arxiv.org/abs/quant-ph/0307130).
  Graphzustände und Mehrteilchenverschränkung; NQK nutzt kleine konkrete Kontrollen.
- Kunzinger, Sämann (2018): [Lorentzian length
  spaces](https://doi.org/10.1007/s10455-018-9633-1).
  Kausalstruktur und Zeitseparation als eigene Bestandteile lorentzscher Geometrie.
  Die Roadmap behauptet keinen bereits konstruierten lorentzschen Limes.
- Yazdi, Letizia, Kempf (2021): [Lorentzian Spectral Geometry with Causal
  Sets](https://arxiv.org/abs/2008.02291v1).
  Vorarbeit zur Unterscheidung kausaler Mengen durch Spektren, zusätzliche
  Invarianten und kleine Erweiterungen. Endliche Unterscheidungserfolge sind
  keine allgemeine Rekonstruktionsgarantie.

Diese Auswahl dient der konkreten Arbeitsplanung. Sie ist keine vollständige
Literaturrecherche oder Bescheinigung wissenschaftlicher Neuheit.

## Tatsächlich geprüfter Astrolabium-Stand

Repository-Basis für diesen Zweig:
`7c70771936acf52237c658da3d0b566859143aa6`.

- [Projektübersicht am Basiscommit](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c70771936acf52237c658da3d0b566859143aa6/README.md)
- [Mathematischer Geltungsbereich](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c70771936acf52237c658da3d0b566859143aa6/docs/SCIENTIFIC_SCOPE.md)
- [Signal Validation Lab](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c70771936acf52237c658da3d0b566859143aa6/docs/SIGNAL_VALIDATION_LAB.md)
- [Lorentzsche Forschung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c70771936acf52237c658da3d0b566859143aa6/docs/LORENTZ_RESEARCH.md)

Das Signal Lab ist an diesem Stand bereits vorhanden. NQK soll seine künftigen
Robustheits- und Replayfunktionen mit diesem Bestand abstimmen. Die im
Astrolabium dokumentierte kleine Kausalordnungsstudie ist eine vorhandene
Referenz, kein durch dieses Dossier neu ausgeführter NQK-Test. Künftige
Vergleiche müssen die jeweils tatsächlich ausgeführte Revision protokollieren.

Hinweise auf Zeitfenster in anderen Projektdokumenten werden hier nicht als
aktueller Agentenstatus übernommen. Es wurde keine Laufplanung geändert.
