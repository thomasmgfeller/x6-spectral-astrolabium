# CSPP E4-V0.1 — Prüfvertrag, Entwurf 1

27. Oktober 2026. **DRAFT / NOT_FROZEN / NOT_RUN.** Schritt 1 ist die
Spezifikation eines Experiments. Hier wurden keine Wellen-, Dirac- oder
Flavor-Ensembles ausgeführt. Ein bestandener Vertragscheck ist keine
physikalische Qualifikation. CSPP wird als Projektbezeichnung verwendet;
dieser Vertrag führt keine zusätzlichen fundamentalen Axiome ein.

**Fragestellung:** Wie skalieren Propagationsfehler, Flavor-Bias,
Realisierungsstreuung und Kohärenzabweichung bei einer kontrollierten
Kontinuumsannäherung, und welchen Anteil können wir Geometrierekonstruktion,
diskretem Operator und numerischer/statistischer Auswertung zuordnen?

Der Einstieg ist ein synthetisches Zweiflavor-Modell auf flacher
3+1-Minkowski-Raumzeit. Es verwendet keine gemessenen Neutrinoparameter und
modelliert keine schwache Produktion oder Detektion. Die erste Stufe ist
ein Benchmark für gekoppelte Dirac-Wellengleichungen. Dreiflavor-RGB,
Krümmung, Wechselwirkungen und fermionische Vielteilchenstatistik folgen
erst in späteren, separat spezifizierten Versionen.

## Festgelegt und noch offen

| Im Entwurf festgelegt | Vor dem Bestätigungs-Freeze noch offen |
| --- | --- |
| Geometrie, Einheiten, Quelle, Detektor, Massen und Mischung | Konkrete skalare und fermionische Operatoren |
| Primäre Observablen und Fehlerziele | Injektion, Interpolation und Detektorquadratur |
| Fehler- und Risikobudget, Ausfallbehandlung | Gemeinsame Geometrieregion einschließlich Spinstruktur |
| Kontrollen, G1–G3-Kriterien und Entscheidungsregeln | Validierte Referenzimplementation und Fehlernachweise |
| RNG-Zuordnung und Datenvertrag | Endgültige Dichtestufen, Skalenplan, Ensemblegröße und Gesamtbudget |

Alle Zahlen sind **Designentscheidungen dieses Entwurfs**, keine erreichten
Genauigkeiten. Änderungen vor dem Freeze werden begründet versioniert.
Nach Einsicht in Bestätigungsdaten benötigt jede Methodenänderung eine neue
Version und neue Bestätigungsdaten.

## Dateien

- [PROTOCOL.md](PROTOCOL.md): vollständiger mathematischer und statistischer Prüfvertrag.
- [contract.json](contract.json): maschinenlesbare Parameter, Budgets und offene Entscheidungen.
- [DATA_CONTRACT.md](DATA_CONTRACT.md): Datensätze, Status und vollständige Nenner.
- [REFERENCES.md](REFERENCES.md): Primärquellen und ihre genaue Rolle.
- [check_contract.py](check_contract.py): Konsistenzprüfung und Sperre gegen vorzeitigen Freeze.
- [CHECKS.json](CHECKS.json): ausgeführte Vertrags-, Algebra- und Negativkontrollen.

Aus dem Repository-Hauptverzeichnis, Python 3.12, nur Standardbibliothek:

```sh
python3 -B research/cspp/e4_v0_1/check_contract.py --self-test
python3 -B research/cspp/e4_v0_1/check_contract.py --require-frozen
```

Der erste Befehl muss `PASS_CONTRACT_DRAFT` liefern. Der zweite muss mit
Exitcode 2 und `BLOCKED_NOT_FROZEN` enden. Das ist die beabsichtigte Sperre;
ein produktiver Bestätigungslauf muss diese Prüfung zwingend aufrufen.
Das Skript kann auch eine künftige JSON-Datei per `--contract PATH` prüfen;
es verifiziert dabei keine wissenschaftlichen Beweisdateien oder Hashbindungen.
Ein künftiger Freeze benötigt zusätzlich einen ausführbaren Evidence-Prüfer.

## Einordnung in die bisherige Eigenzeitforschung

[Eigenzeit v0.5](../../eigenzeit_4d/constrained_region_v0_5/README.md)
zertifiziert eine Ziel-Eigenzeit im festen Landmarkenmodell. Das ist noch
keine gemeinsame Region für sämtliche Operatorstützpunkte, Bezugssysteme
und Spintransporte. Die dortige Fehlfreigabegrenze pro Beobachtung darf
nicht unverändert als gemeinsame Garantie einer E4-Kampagne benutzt werden.
Die bisherigen wissenschaftlichen HOLDs bleiben bestehen.

Nächste Arbeit ist Schritt 2: ein begrenzter skalarer Entwicklungspilot.
Dieser Vertrag startet diesen Pilot nicht und behauptet keinen
Kontinuumsgrenzsatz, keinen Diskretheitseffekt in der Natur und keine Neuheit.

Eigener Text und Code: Apache-2.0 gemäß Repository-Lizenz.
