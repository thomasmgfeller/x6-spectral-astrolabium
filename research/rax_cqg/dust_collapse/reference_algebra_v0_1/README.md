# CST-DUST: Observablenalgebra und endliche Phasenreferenz v0.1

Die bisherige Record-Wirkung legt keine physikalische Superselektionsregel fest.
Unter einer ausdrücklich zusätzlichen globalen U(1)-Erhaltung ist der beste
universelle Fehler einer kohärenten Zweimodenmessung mit L+1 Referenzstufen
exakt `(1-cos(pi/(L+2)))/2`. Die Ladung ist ein Modelllabel und keine abgeleitete
Staubmasse. Alle acht physikalischen Gates bleiben HOLD.

- `DERIVATION.md`: vollständige Annahmen, Beweise und Primärquellen.
- `algebra_contract.json`: maschinenlesbarer Geltungsbereich und offene Auswahl.
- PDF: sechsseitiger Lesebrief mit Ergebnis, Grenzen und nächster Entscheidung.
- `results/`: exakte endliche Kontrollen und zertifizierte rationale Intervalle.
- `inputs/`, `provenance.json`: fünf gepinnte Quellen einschließlich Lizenz.
- `plan.json`, `plan.sha256`: nach analytischem Entwurf, vor Kontrollen fixierter Plan.

## Reproduktion

```sh
python3 -B verify_package.py
python3 -B replay.py
```

Die wissenschaftliche Nachrechnung benötigt nur Python 3 und seine
Standardbibliothek, keinen Netzzugang, keine Cloud, kein NumPy und keinen
n=5-Lauf. `replay.py` schreibt seine Rechnung in ein vorübergehendes Verzeichnis
und vergleicht alle vier Ergebnisdateien bytegenau mit den beigefügten Dateien.
Erwartet: 336 Referenzfälle, 2016 Born-/Mittelungsidentitäten, acht abgewiesene
Negativkontrollen. Die allgemeinen Aussagen sind analytisch bewiesen;
die endlichen Kontrollen sind keine externe Replikation oder formale Verifikation.

Optionaler Neuaufbau des PDFs: ReportLab und DejaVu-Schriften werden benötigt.
Der reproduzierbare ZIP-Aufbau verwendet `package.py` und ein explizites
Dateimanifest; die enthaltene PDF-Datei wird dabei unverändert übernommen.
Ein erneutes Rendern des PDFs kann dessen Metadaten und damit Hash verändern.

## Wissenschaftliche Grenze

Noch nicht hergeleitet: physikalische Algebra und Zustands-Constraints,
Sektorladung, erlaubte Referenzpräparation, vollständige Modenfilter,
CST-Wechselwirkung und Messinstrument. Ein idealer Zweimodenfilter darf nicht
ohne Prüfung auf den gesamten Historienraum übertragen werden. Das Budget
bezieht sich auf einmalige Nutzung einer unabhängig vorbereiteten Referenz;
Verbrauch und Wiederverwendung bleiben offen.

Basis: Main `c77cb607db23a043cd4965ee4efeb206eda22f8e` nach
[PR 263](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/263).
Dieses Paket enthält weder eine GitHub-Actions-Datei noch einen automatischen
Produktions- oder Finanzierungsauftrag.

## Freiwillige Prüfung

Hilfreich ist zuerst eine fachliche Prüfung von DERIVATION.md, besonders der
Trennung lokaler Superselektion von globaler Erhaltung und der Frage, welche
Algebra durch die konkrete CST-Materie-/Randtheorie überhaupt bestimmt wird.
Die kleine Nachrechnung kann eine freiwillige Person auf vorhandener Hardware
ausführen. Daraus entsteht kein Anspruch auf Kostenerstattung durch Thomas
Gfeller. Große Rechenläufe sind nicht Bestandteil dieses Pakets.

Lizenz: Apache-2.0, siehe `LICENSE` und `NOTICE`.
