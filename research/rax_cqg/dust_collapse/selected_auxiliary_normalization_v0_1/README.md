# CST-DUST · Normierungsprüfung einer ausgewählten Hilfsbasis v0.1

**11. November 2026 · endliche Hilfsraumkontrolle · alle physikalischen Gates HOLD**

Dieses Paket schließt an den [Randkern-Benchmark](../boundary_kernel_benchmark_v0_1/README.md) und den [korrigierten 8×8-Geometriekontrollkern v0.2](../geometry_control_8x8_v0_2/README.md) an. Es konstruiert eine positive Gramstruktur für eine **explizit ausgewählte Hilfsbasis**, korrigiert die Basisordnung und unterscheidet Basiswechsel von einer zusätzlichen Zuordnung der Kernzahlen.

Das Hauptergebnis ist reproduzierbare Hilfsraumalgebra. Ein physikalischer Randraum, eine physikalische Uhr, Materiemoden und eine geschlossene CST-Evolution sind weiterhin nicht hergeleitet.

## Auswahl und Aussagegrenze

Der vorhandene diskrete Hilfsraum bei m=2 hat **sieben Orbits**. Wir wählen vier Indikatorfunktionen: vollständig unmarkierte bzw. vollständig positiv markierte Zweier-Antikette und Zweier-Kette. Die drei gemischt markierten Orbits bleiben außerhalb dieser Auswahl. Dazu kommt ein ausdrücklich **externes zweidimensionales Testlabel**, das keine hergeleitete Materiemode darstellt.

| Größe | Konstruktion |
|---|---|
| Orbitgewichte | $\mu_O=1/(2^m\lvert\mathrm{Aut}(C,\sigma)\rvert)$ |
| Gewählte Quellindizes, nullbasiert | 0, 3, 2, 6 |
| Ausgelassene Quellindizes | 1, 4, 5 |
| Reihenfolge | A\|0\|0m, A\|0\|1m, K\|0\|0m, K\|0\|1m, A\|+\|0m, A\|+\|1m, K\|+\|0m, K\|+\|1m |
| $G_{\rm sel}$ | $\operatorname{diag}(1/8,1/8,1/4,1/4,1/8,1/8,1/4,1/4)$ |
| Einbettung | $E^\dagger(G_7\otimes I_2)E=G_{\rm sel}$ |
| Normierte Einbettung | $J=E G_{\rm sel}^{-1/2}$, $J^\dagger(G_7\otimes I_2)J=I_8$ |

Die Positivität ist für diese Auswahl belegt. Ihre dynamische Abgeschlossenheit ist **nicht** belegt. Die Identifizierung mit der formalen Geometrie-Testbasis ist eine zusätzliche, offengelegte Hilfskonstruktion.

## Ergebnis bei z=1

Die Quelle liefert $A_e=I_2\otimes K_g\otimes I_2$ mit $K_g=\left(\begin{smallmatrix}35&26\\26&20\end{smallmatrix}\right)$ als Koeffizientenabbildung in einer orthonormalen formalen Testbasis. Drei Fälle werden getrennt exportiert:

| Modus | Bedeutung | Singularwerte, jeweils vierfach | Spektralnorm des Unitaritätsdefekts |
|---|---|---:|---:|
| transport (Standard) | Derselbe formale Operator in der gewählten Hilfsbasis | 54.5601182555; 0.4398817445 | 2975.8065040508 |
| assign_coefficients | Dieselben Quellzahlen zusätzlich als Indikator-Koeffizienten zugeordnet | 57.5745276597; 0.4168510099 | 3313.8262352355 |
| assign_covariant | Dieselben Quellzahlen zusätzlich als kovariante Matrixelemente zugeordnet | 357.8538726033; 2.1461273967 | 128058.3941371973 |

Nur der erste Fall ist ein reiner Darstellungstransport des zuvor deklarierten Operators. Der dritte reproduziert die großen Zahlen des eingereichten Normierungsberichts unter dessen zusätzlicher Konvention. Diese Zahlen sind **kein basisunabhängiger Befund über einen bereits hergeleiteten physikalischen Randkern**.

Alle drei deklarierten Testabbildungen sind nicht isometrisch. Ein einziger skalarer Normierungsfaktor kann ihre ungleichen Singularwerte nicht beide auf eins setzen. Die tatsächlichen Stratum- und Testlabel-Mischblöcke verschwinden. Das folgt hier aus der übernommenen Zuschauerstruktur; eine physikalische Superselektion ist damit nicht gezeigt.

## Reproduzieren

Python 3.11 oder neuer und NumPy 2.3.5; die geprüfte Umgebung steht in [environment.json](environment.json). Im Paketverzeichnis:

    python build_evidence.py
    python test_normalization.py --report results/tests.json
    python package.py
    python verify_package.py

Für einen einzelnen ausdrücklich gewählten Vergleich:

    python normalize_cst_dust_8x8.py --mode assign_covariant --outdir /tmp/cst-dust-auxnorm

**21 Tests bestehen.** Neun Ergebnisdateien werden in einem frischen temporären Verzeichnis bytegleich reproduziert, ebenso nach Entpacken des Prüfpakets. Diese Bytegleichheit ist an die dokumentierte numerische Umgebung gebunden. Andere BLAS-/Plattformversionen können Rundungsabweichungen erzeugen; die exakten endlichen Zertifikate bleiben separat nachvollziehbar.

## Dateien und Anschluss

- [Herleitung, Konventionen und beschränkte Produktobstruktion](DERIVATION.md)
- [Korrekturen gegenüber dem eingereichten Normalisierer](CORRECTIONS.md)
- [Datenformat und Validierungsregeln](DATA_FORMAT.md)
- [Normalisierer](normalize_cst_dust_8x8.py), [Tests](test_normalization.py), [Prüfer](verify_package.py)
- [Standard: NPZ](data/cst_dust_auxnorm_transport_z1.npz) und [JSON](data/cst_dust_auxnorm_transport_z1.json)
- [Zusätzliche Koeffizientenzuordnung: NPZ](data/cst_dust_auxnorm_assign_coefficients_z1.npz) und [JSON](data/cst_dust_auxnorm_assign_coefficients_z1.json)
- [Zusätzliche Matrixelementzuordnung: NPZ](data/cst_dust_auxnorm_assign_covariant_z1.npz) und [JSON](data/cst_dust_auxnorm_assign_covariant_z1.json)
- [Exakte Zertifikate](results/exact_certificates.json), [Orbitauswahl](results/selection.json), [Testergebnis](results/tests.json)
- [Quellen und Upload-Hashes](provenance.json), [Status](status.json), [SHA-256-Manifest](SHA256SUMS.json)
- [Vollständiges Prüfpaket](CST_DUST_Ausgewaehlte_Hilfsbasis_Normierungspruefung_v0_1_Pruefpaket.zip)

Der nächste physikalische Anschluss benötigt unabhängig begründete Randräume samt Produkten, die Zuordnung der gemeinsamen Amplitude zu einer eindeutigen Kernkonvention und tatsächlich berechnete Materieblöcke. Unterschiedliche Ein-/Ausgangsprodukte allein machen einen Kern nicht physikalischer. Die Herleitung zeigt bereits eine begrenzte Obstruktion für **positive diagonale** Produkte bei z=1; sie schließt allgemeinere Produkte nicht aus.

**Kein physikalischer Hamiltonoperator, kein Nullatom-Bounce, kein allgemeines CST-No-go.** Die ältere Negativkontrolle des rohen Uhrkerns bleibt ein getrenntes Ergebnis. Dieses Paket startet keine Produktionsläufe und verwendet keine externe kostenpflichtige Rechenleistung.
