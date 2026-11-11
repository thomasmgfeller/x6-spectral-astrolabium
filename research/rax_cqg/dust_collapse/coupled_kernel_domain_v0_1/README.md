# CST-DUST: Definitionsbereich des gekoppelten Kerns v0.1

11. November 2026. Anschluss an PR #279–283; Main-Basis `cfd4413c8e9d2338f41567aac249e9ac54a295d8`.

**Ergebnis:** Die ursprüngliche gekoppelte AA-Kontrollamplitude bildet den normierten Atom-/Skalargrundzustand nicht in den bisherigen ungegewichteten Rand-Hilbertraum ab. Der Beweis umfasst alle 33 Historien, die originalen Gravitationsphasen, beide inneren Dichtestrata und sämtliche relevanten Randnormierungen. Entlang einer Ausgangsfeldrichtung verbleiben zwei nicht auslöschbare quadratische Phasen; die integrierte Betragsquadratsumme wächst linear mit der Feldfensterlänge.

Derselbe Kern ist als stetige Amplitude auf dem dichten gewichteten Testraum `V = L²_inv((1+|q|²)^4 dμ_A)` wohldefiniert und bildet `V` in dessen Antidual `V'` ab. Der Abel-Fehler in dieser Operatornorm ist kleiner als `1.342 ε`. Das Gewicht definiert die Testtopologie, kein neues physikalisches Skalarprodukt.

- Vollständiger analytischer Beweis: `DERIVATION.tex` und `CST_DUST_Gekoppelter_Kern_Definitionsbereich_v0_1.pdf`.
- Alle 33 rationalen Schurblöcke, Ränge, Nullrichtungen und rigorosen Konstanten: `results/domain_certificate.json`.
- Herkunft: `provenance.json` und unveränderte Dateien in `inputs/`.
- Reproduktion: `python -B test_domain.py`, danach `python -B verify.py`.

Elf Testgruppen bestanden, darunter 132 unabhängige Float64-Gaußvergleiche. Der Divergenzbeweis ist analytisch; eine numerische Cutoff-Kurve wird nicht als Beweis verwendet. Die positive asymptotische Normdichte ist rigoros größer als `4.5e-8` im deklarierten dimensionslosen Kontrollmodell.

Die bisherigen Matrixpaarungen bleiben gültig. Eine überall definierte Evolution auf dem bisherigen Hilbertraum, eine Hilbertraum-Restnorm für diesen Ausgang oder eine ungeprüfte Komposition `V -> V' -> V'` sind damit nicht gerechtfertigt. Der in der Herleitung charakterisierte maximale Hilbertbereich bezieht sich ausdrücklich auf Eingänge innerhalb von V; dessen vollständige Klassifikation und Dichtheit werden nicht behauptet.

Die vollständige 33er-Kontrollsumme ist keine unendliche physikalische CST-Summe. Der physikalische Kern bleibt `NOT_CONSTRUCTED`; alle acht physikalischen Gates bleiben `HOLD`. Keine kostenpflichtigen Läufe, Messungen oder Produktionssimulationen. Dieses Paket wurde in diesem Arbeitsschritt erstellt, nicht auf GitHub veröffentlicht.
