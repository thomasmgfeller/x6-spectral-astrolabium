# Eigenzeit v0.15 - Kontrollierter KVF-Antwortkanal

**Der Antwortkanal ist mathematisch spezifiziert und synthetisch geprüft.**
Eine kompakt geschaltete Quelle und Auslese unterscheiden ein masseloses
und ein massives freies Skalarfeld in derselben 3+1-Minkowski-Geometrie.
Der reale Feldversuch bleibt **HOLD_FIELD_TRANSFER**.

| Ergebnis | Wert / Grenze |
|---|---|
| Späte Antwort M0 | Exakt null im gesamten Geometrievertrag |
| Späte Antwort M1, nominal | -0.00905497439 ell0^-2 |
| Garantierte M1-Spanne | [-0.01034932433, -0.00808529701] ell0^-2 |
| Hinreichendes Primärbudget | 2048 unabhängige ABBA-Blöcke = 8192 Quellstellungen mit parallelem Referenzkanal |
| Bedingte Fehlerschranke | Unter 0.743 % je Richtung |
| Synthetische Zuordnung | Beide Modelle richtig zugeordnet |
| Endpunktkontrolle | 16 bzw. 15 Fehler unter je 20000 Läufen |
| Gemeinsame GUM-Auswertung | Vier Antworten, vollständige Kovarianz, exakte Momentenfortpflanzung |

Die Fehlerschranke setzt unter anderem begrenztes vorzeichenabhängiges
Übersprechen, eine begrenzte Verstärkung und unabhängige subgaußsche
Blockkontraste voraus. Der vorausgesetzte Maßstab ell0 ist nicht
physisch gewählt. Die Ergebnisse tragen keinen Quantennachweis,
keine Raumzeitrekonstruktion und keinen Quantengravitationstest.

## Transparenz der Unsicherheitskontrolle

Der nominelle M1-Vektor liegt in der einen synthetischen Stichprobe
außerhalb des geschätzten gemeinsamen 95-%-Ellipsoids. Die erste
numerische PDF-Kontrolle für M1 lag ebenfalls knapp unter dem Zielwert.
Beide Befunde bleiben dokumentiert.

Ein anschließend gesondert fixierter Audit mit je einer Million neuen
PDF-Ziehungen, unveränderten Rohdaten und unveränderten Radien ist
mit dem Zielwert 0.95 vereinbar. Die gemeinsame Absicherung der zwei
Überdeckungswahrscheinlichkeiten beträgt mindestens 99 %.
Dies validiert keine physische Überdeckung und garantiert nicht,
dass ein einzelner 95-%-Bereich den wahren Wert enthält.

## Inhalt

[Originalbericht (PDF)](Eigenzeit_KVF_Antwortkanal_v0_15.pdf) · [Vollständiges Prüfpaket (ZIP)](Eigenzeit_KVF_Antwortkanal_v0_15_Pruefpaket.zip) · [Vorgänger v0.14](../kvf_control_v0_14/README.md)

- [Ergebnisbericht](Eigenzeit_KVF_Antwortkanal_v0_15.pdf)
- [Herleitung und rationale Schranke](DERIVATION.md)
- [Acht GUM-Schritte und exakte Momentenfortpflanzung](GUM.md)
- [Vertrag vor dem Datenlauf](CONTRACT.json)
- [Separate Kontrollen und Gegenbeispiele](records/check.json)
- [Unveränderter ursprünglicher Lauf](records/summary.json)
- [Offengelegter Auditplan](AUDIT_PLAN.json), [Auditresultat](records/coverage_audit.json)
- [Laborbelege und nächste praktische Schritte](LAB_GATES.md)
- [Primärquellen und Herkunft](SOURCES.md)

## Reproduktion

Mit Python 3.12 im Wurzelverzeichnis des Repositorys ausführen:

~~~sh
python -m pip install -r research/eigenzeit/kvf_response_v0_15/requirements.txt
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research/eigenzeit/kvf_response_v0_15/publication_check.py --replay
~~~

Der erste Lauf prüft das gesamte Inventar, führt den ursprünglichen
Versuch in einem frischen Verzeichnis aus und vergleicht sechs
Ergebnisprotokolle sowie sechs Rohdatendateien. Danach wird der separate
Audit mit unveränderten Parametern erneut ausgeführt.
FREEZE.sha256 dokumentiert die Fixierung vor dem ursprünglichen
Rohdatenlauf; AUDIT_FREEZE.sha256 die spätere Fixierung des Audits.

Zwei unabhängige numerische Darstellungen des freien Kerns, symbolische
Normierungsprüfungen und rationale Schranken sind interne Kontrollen.
Eine externe Reproduktion durch andere Personen steht aus.

Der nächste praktische Engpass ist die unabhängig belegte Grenze
des quellenabhängigen Übersprechens. Sie kann durch zusätzliche
Simulationen allein nicht als Hardwareeigenschaft nachgewiesen werden.

## Veröffentlichung

Die direkt sichtbaren Programme und Protokolle sind unveränderte Auszüge. Das ZIP enthält alle Rohdaten und das ursprüngliche README. Der Repository-Einstieg publication_check.py prüft die Originale, alle 43 Archiveinträge, beide Fixierungen und die Herkunft der übernommenen Quellen. Anschließend führt er das vollständige Paket in einem temporären Verzeichnis aus. audit_reproduce.py und reproduce.py benötigen den vollständigen Archivinhalt. [Veröffentlichungsnachweis](PUBLICATION.json)
