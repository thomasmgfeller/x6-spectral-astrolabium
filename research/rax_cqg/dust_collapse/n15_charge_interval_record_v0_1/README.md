# N15-Ladungsverteilung · Prüfung des nächsten Forschungsschritts

## Ergebnis

Für die primäre Kettenfortsetzung und die zwei Anfangsdichtezentren 1/8 und 1/4 liegt die grösste Spannweite einer einzelnen Ladungsklasse auf der geprüften Ein-Kanten-Verbindung bei 0,02585 Prozentpunkten für die markierte Masse 1/4, 0,10585 für 1 und 0,26638 für 4. Bei Masse 1/4 und Dichtezentrum 1/8 verschiebt sich der positive Gesamtanteil im Sechsklassenregister um 0,02585 Prozentpunkte. Der Wechsel zum zweiten Kettenzeugen mit denselben 70 N13-Marginalen verschiebt diesen Anteil bei festem A:B = 1:1 um 4,84 Prozentpunkte.

In den zwölf Basisfällen beträgt der normierte Betrag des Überlapps der beiden unregistrierten Vorzeichenzweige im Drei-Moden-Randraum 0,01130 bis 0,07696. Eine fehlerfreie deterministische Unterscheidung zweier reiner Endzustände erfordert Orthogonalität. Als nächstes ist deshalb zu prüfen, ob die Stromselektion am gekoppelten Rand mit den physikalischen Nullrichtungen verträglich ist und ob die Randdaten einen messbaren Vorzeichenrecord tragen.

## Zahlen lesen

In `intervalle.csv` ist die unabhängige Variable die affine Mischung λ der beiden vollständigen Ein-Kanten-Gewichtszeugen. λ = 0 entspricht 1:1, λ = 1 entspricht 1:3. Das lokale Verhältnis ist A/B = (2−λ)/(2+λ). Pro Zeile ist der Kettenzeuge fest, beide Elternordnungen erhalten je das halbe Amplitudengewicht. Die sechs Klassen und die beiden positiven Gesamtanteile sind getrennt ausgewiesen. In der positiven Präparation besitzt die zusätzliche Klasse {0} exakt Gewicht null. Bei den Vakuumkontrollen gilt eine andere Präparation.

Zähler und Nenner sind quadratisch in λ. Die Auswertung vergleicht beide Endpunkte und alle reellen stationären Punkte im Inneren. Sie verwendet das Mittel der komplexen Amplituden der vier 4096er-Sobol-Scrambles. Die Resultate sind numerische Extrema entlang benannter Gewichtsverbindungen. Das vollständige Gebiet zulässiger Fortsetzungen sowie ein physikalisches Fehlerbudget bleiben offen.

In `ueberlapp.csv` werden jeweils die drei negativen und die drei positiven Amplituden vor der Paarung kohärent addiert. Aus der archivierten Dekohärenzmatrix folgt der normierte Betrag |D(−,+)|/√[D(−,−) D(+,+)]. Diese Grösse ist dimensionslos.

## Wiederholung

Die Eingabe ist das Studienverzeichnis aus PR #336, Commit `b2bfb334d2a24de3eca2d7e8734a3715c43e9280`. Das vollständige Offline-Paket desselben Stands hat SHA-256 `3e08cb9c2dc88911e18c7ce69e97ee1543142356670cccb354ac505819b15a85`. Es genügen das entpackte Paket und die dort aufgeführten Python-Abhängigkeiten.

```sh
OPENBLAS_NUM_THREADS=1 python -B pruefen.py /pfad/zur/entpackten/N15-Studie ausgabe
```

[Studie und Eingabedaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/b2bfb334d2a24de3eca2d7e8734a3715c43e9280/research/rax_cqg/dust_collapse/joint_charge_distribution_v0_1)
