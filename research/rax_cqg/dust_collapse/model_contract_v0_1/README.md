# CST-DUST Model Contract v0.1

Stand: 6. November 2026. ID `CST-DUST-MC-001`, Version `0.1.0`.

Der Prüfvertrag ist spezifiziert. Der physikalische CST-Modellschluss ist offen.
Alle acht Entscheidungen für den Zielkandidaten `CST-DUST-C1` bleiben **HOLD**.
Es wurden keine neuen CST-Ensembles erzeugt. Eine GitHub-Veröffentlichung ist
nicht Bestandteil dieses Erstellschritts.

## Inhalt

- `CST_DUST_Model_Contract_v0_1.pdf`: zehnseitiger lesbarer Vertrag.
- `CONTRACT.md`: textgleiche lesbare Fassung, einschließlich Quellen und Grenzen.
- `contract.json`: maschinenlesbare Regeln, Referenz, Toleranzen, offene Pflichten.
- `build_contract.py`: reproduzierbarer Ursprung von `contract.json`.
- `gate.py`: prüft Entscheidungsrecords und die beiden Datei-Hashes. Prüft keine mathematischen Beweise.
- `examples/`: P0-Laufmanifest und vollständiger P0-Record.
- `verify.py`: klassische algebraische Kontrollen und gezielte Kontrollen der Entscheidungslogik.
- `results/`: Referenzwerte, Softwarekontrollen und unabhängige CST-Entscheidungen.
- `inputs/`: unveränderte Veröffentlichungsübersichten mit Quellenherkunft.
- `SHA256SUMS`: Prüfsummen aller Paketdateien außer der Prüfsummenliste selbst.

## Nachrechnung

Python 3.10 oder neuer, nur Standardbibliothek:

```sh
python3 verify.py
python3 gate.py examples/checkpoint_P0.json
```

`verify.py` schreibt die lokalen Referenz-/Softwareergebnisse und P0-Beispielrecords
neu. Alle Softwarefixtures sind ausdrücklich **keine physikalische Evidenz**.
Die klassischen Zahlen kontrollieren Gleichungen einer bereits gekoppelten
Einstein-Staub-Referenz, nicht die Emergenz dieser Gleichungen aus CST.

Der Gate-Prozess liefert bei einem gültigen Record Exitcode 0, auch wenn
physikalische Entscheidungen HOLD oder FAIL lauten. Exitcode 2 bezeichnet einen
ungültigen Record. Ein erfolgreicher Prozess ist deshalb kein physikalisches PASS.
Für eigene Records: `python3 gate.py record.json --manifest manifest.json`.

## Bericht reproduzieren

```sh
python3 -m pip install -r report-requirements.txt
python3 make_report.py
```

Erfordert DejaVu Sans im üblichen Systemverzeichnis. Der Bericht wird aus
`contract.json` und den geprüften Ergebnissen erzeugt; der erläuternde Text steht
in `make_report.py`. `build_contract.py` ist nur zum gezielten Neuaufbau des
Vertrags vorgesehen. Eine semantische Änderung verlangt eine neue Version,
neue Hashes und die erneute Bewertung betroffener Entscheidungen.

## Wissenschaftlicher Umfang

Regularität wird an P0 bis P5 sowie bei jeder Masse, Auflösung und Zeitauswertung
separat berichtet. Das Standardziel sind kontrollierte physikalische Momente
mit uniformer Integrierbarkeit und Konvergenz im angegebenen Gebiet. Das ist
keine automatische Aussage über alle Realisierungen, Gezeitenkomponenten,
kausale Vollständigkeit oder globale Singularitätsauflösung. Der Vertrag enthält
einen endlichen Korrespondenz-Screeningtest; seine numerischen Toleranzen sind
Leistungsanforderungen, keine Naturkonstanten.

Der neue mikroskopische Materie-Geometrie-Kern ist nicht vollständig definiert.
Die sieben offenen Pflichten D1-D7 sind echte Sperrgründe für den dynamischen
CST-Test. Der Vertrag macht sie überprüfbar und ersetzt ihre Herleitung nicht.
