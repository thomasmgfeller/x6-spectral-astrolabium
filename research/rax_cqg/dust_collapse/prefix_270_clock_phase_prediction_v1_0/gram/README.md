# Skalare Gram-Matrix für Präfix 270

Das Zertifikat rekonstruiert aus dem archivierten Kettensektor 15 zulässige markierte Fortsetzungen mit elf verschiedenen kanonischen Endtypen. Verwendet werden der zentrierte skalare Gauss-Eingang, die gemeinsame Randkarte und die kanonische Normierung des ursprünglichen Quellenpakets. Die geerbte Reduktion weist bei keinem Endtyp eine freie reine Bulk-Nullrichtung auf. Die vier Endkerne 623, 718, 751 und 5295 enthalten jeweils eine lineare Fourier-Bedingung, die bei der Paarung mit dem Eingangsgauss berücksichtigt wird.

Für den normierten Dreimodenzustand mit symmetrischer Präzision βΩᵢ ist der reelle Teil Re Ωᵢ positiv definit. Die drei positiven führenden Minoren sind jeweils rational dokumentiert. Das Gauss-Integral liefert

$$
|G_{ij}|^4 =
\frac{64\,\det(\operatorname{Re}\Omega_i)\,\det(\operatorname{Re}\Omega_j)}
{|\det(\overline{\Omega_i}+\Omega_j)|^2}.
$$

Das gemeinsame β und die Phasen der einzelnen Zustände fallen aus dieser Identität heraus. Alle 55 vierten Potenzen stehen als exakte Brüche in der Datei. Der unabhängige Prüfer kontrolliert mit rationaler Arithmetik jede Determinante und jede nach oben gerundete vierte Wurzel. Die Diagonale von G ist durch die kanonische Normierung eins. Die grösste obere ausserdiagonale Zeilensumme ist 1540449/10000000 bei Endtyp 760. Die Gershgorin-Einschliessung für die hermitesche Matrix ergibt

$$
\frac{8459551}{10000000}I\;\leq\;G\;\leq\;\frac{11540449}{10000000}I .
$$

Die Datei enthält zusätzlich die 121 komplexen Einträge der mit den geerbten Phasen ausgewerteten Gram-Matrix als Dezimalnäherungen. Die bewiesene Spektralschranke verwendet die rationalen Betragszertifikate. Ihre Gültigkeit ist unabhängig von Dichte und Uhrmodulation. Für einen Quotienten äusserer Normquadrate werden ausserdem Referenzamplituden mit positiven unteren Betragsgrenzen benötigt.

## Reproduktion

Die vollständige Rekonstruktion benötigt SymPy 1.14.0 und mpmath 1.3.0. Die Pfadangabe bezeichnet das unveränderte Originalpaket für die neun Richtungen am Präfix 1564. Die abschliessende Prüfung ab den rekonstruierten Präzisionen verwendet die Python-Standardbibliothek.

~~~sh
python3 -B gram270.py --source /pfad/CST_DUST_Praefix_1564_Neun_Richtungen_v0_1_Pruefpaket.zip --output replay.json
cmp gram.json replay.json
python3 -B verify_gram.py gram.json
~~~
