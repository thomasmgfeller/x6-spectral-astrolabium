# Was die Gewichte im N22-Fenster unterscheiden

Auf der archivierten Ordnung sind im normierten Modelluhrfenster [15/32, 17/32] die Ereignisse 18 und 19 positiv. An 17 und 20 ist das Gewicht exakt null. Dies ist eine Beschränkung auf die vier Fensterereignisse. Sie ist kein Nachweis für ein räumliches Innen- und Aussensystem der vollständigen Geschichte.

Zunächst bilden wir für diese Kontrolle aus den beiden positiven Gewichten die Anteile p = w18/(w18+w19) und 1−p. Dies ist eine von uns definierte Normierung einer lokalen Gewichtsverteilung. Auf den rationalen Eingabeboxen wird die Unreinheit 2p(1−p) über Monotonie exakt eingeschlossen. Die Werte betragen rund 0,388350908 (schwer) und 0,385538983 (leicht). Die Intervalle sind streng getrennt. Diese Aussage ist eine Gewichtsdiagnose. Sie ist an sich keine Entropie einer quantenmechanischen Teilregion.

Für einen zweiten Test nehmen wir *zusätzlich* unabhängig adressierbare Besetzungsmoden für die vier Fensterereignisse, orthonormale Okkupationszustände und einen einzigen normierten Anregungszustand an. Seine Amplituden an 18 und 19 haben die Beträge √p und √(1−p). An 17 und 20 verschwinden sie. Alle Phasen sind beliebig. Für den Schnitt {18,19} gegen {17,20} lässt sich daher das Vakuum der beiden leeren Moden als Faktor ausklammern. Die reduzierte Dichtematrix des positiven Teilsystems ist rein und S_lin = 0 für beide Präparationen. Bei einer anderen Aufteilung, die 18 und 19 auf zwei Seiten verteilt, sind die Eigenwerte des reduzierten Zustands p und 1−p. Jetzt ergibt sich 2p(1−p). Der Zahlenwert hängt von der Teilung und vom Modell für die Quantisierung ab. Beide Rechnungen benutzen dieselben archivierten Gewichte. Der späte Kragen mit seinen positiven Gewichten oder ein ganzes tensorisiertes Modell der 22 Ereignisse ist damit nicht geprüft.

Ein bei gleichem N22-Feld geänderter kompatibler Kugelradius ändert keine dieser Rechnungen. In der separaten Nullpräparation verschwinden alle vier Gewichte. Dort ist der Nenner der übernommenen Normierung null. Eine gesonderte Vorgabe des Fock-Vakuums würde einen normierten Produktzustand mit S_lin = 0 setzen. Ein solches Vakuum wäre eine zusätzliche Quantisierungsannahme. Der dokumentierte Staub-Nullzeuge weist keine Faktorisierung eines physikalischen Feldvakuums nach.

Eingabe aus [N22-Zwei-Massen-Präparation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/n22_anfangsladung_zwei_massen_transfer_v0_1/Vergleichspaar.json). In diesem Verzeichnis mit Python ab 3.10 und Standardbibliothek ausführen.

    python3 -B fensterkontrolle.py > Neuberechnung.json
    diff -u Ergebnis.json Neuberechnung.json

Die Ergebnisdatei nennt jeweils beide Endpunkte als rationale Brüche. Ihr Vergleich verwendet keine Dezimalrundung.
