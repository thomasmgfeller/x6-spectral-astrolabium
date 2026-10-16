# Abhängigkeitsprüfung nach der Widerlegung von H7

**16. Oktober 2026 · Ergebnis: Kein konkreter laufender Rechenweg wurde gefunden,
der die widerlegte H7-Eindeutigkeit voraussetzt. Ein Gesamtstopp ist aus diesem
Befund nicht begründet.** H7 selbst und darauf gestützte Identitäts- oder
Rekonstruktionsbehauptungen bleiben gesperrt. Das ist eine begrenzte Quellen- und
Datenflussprüfung mit gezielten Gegenproben, keine vollständige Neuqualifikation
aller Forschungszweige und kein formaler Beweis der Abwesenheit jedes Fehlers.

Geprüfter Hauptzweig:
[`dc50ffb228e442a230a32e4437e8e452a90b39ad`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/dc50ffb228e442a230a32e4437e8e452a90b39ad).
Alle **39 registrierten Module** sind in [review.json](review.json) einzeln
eingeordnet: 33 im Hauptzweig und sechs an ihren festgelegten Branch-Revisionen.
Die späteren Veröffentlichungsänderungen dieses Audits sind Dokumentation und
Prüfartefakte; die untersuchten Rechenkerne und eingefrorenen Resultate bleiben
unverändert.

## Was H7 tatsächlich widerlegt

Die [vollständige n=7-Studie](../lorentz_n7_complete/README.md) widerlegt die
Implikation, dass gleiche Spektren von S, A und K, gleiche Minimal-/Maximalzahlen
und gleiche Gabelzählungen W_future/W_past Isomorphie erzwingen. Es bleiben zwei
nichtisomorphe Paare. Das stärkere Gradmultiset D trennt zwar den n≤7-Korpus,
besitzt aber ebenfalls ein bekanntes verbundenes Gegenbeispiel bei n=8.

**Nicht mehr zulässig:** Die H7-Signatur als eindeutigen Zustandsschlüssel,
als Isomorphiebeweis oder als alleinige Grundlage eindeutiger geometrischer
Rekonstruktion verwenden. Ebenso unzulässig wäre, verschiedene Historien wegen
gleicher Signatur zu entfernen und ihre Gewichte oder Amplituden zu verlieren.

**Weiter zulässig:** Spektren als Observablen berechnen, Kollisionen untersuchen,
vollständige Relationen behalten und ausdrücklich begrenzte Vergröberungen
definieren. Eine Beobachtungsklasse ist eine Klasse gleicher ausgewählter
Beobachtungen; sie ist nicht automatisch eine Isomorphieklasse.

## Tatsächliche Abhängigkeiten und Entscheidungen

| Bereich | Gefundener Datenfluss oder Anspruch | Konsequenz aus H7 |
|---|---|---|
| Lorentz-Agent n≤5 | Isomorphie durch vollständige Permutationssuche; Spektren separat gruppiert | Weiter nutzbar im festgelegten Bereich. n=7-Eingaben werden von der Kanonisierung abgelehnt. |
| Vollständiger n=6-Atlas | Kanonische volle Relationsmatrizen erzeugen Repräsentanten; spektrale Gruppen enthalten Listen dieser Repräsentanten | Der endliche n=6-Befund bleibt bestehen. Keine Ableitung allgemeiner Eindeutigkeit. |
| n=6-Restpaare / n=7-Höhe≤2 | Begrenzte Teilpopulationen; die damalige H7-Erweiterung war ausdrücklich offen | Teilresultate behalten. Historisches `OPEN` in eingefrorenen Berichten nicht als aktuellen H7-Status lesen. |
| Vollständige n=7-Studie | Alle Relationen und Restpaare werden gespeichert | Negativer Befund ist das korrekte Ergebnis; keine Reparatur zu einem positiven Resultat. |
| RAX-CQG-Benchmark | `CausalSet._r`, `relation_rows`, Import und Ausdünnung bewahren die volle Relation | Keine H7-bedingte Abschaltung. Sechs Gegenbeispielmatrizen bleiben im Python- und JS-Kern erhalten. |
| RAX-CQG-Architektur | Ω_N besteht aus echten Isomorphieklassen; Spektren sind Observablen, Rekonstruktion ist ein separates Gate | Keine Herleitung wird durch H7 bewiesen. Jede spätere Reduktion muss ihre Informationsverluste und Gewichte begründen. |
| Mehrschichtiger Fingerprint | `EXACT_COLLISION` zulässig; `physical_equivalence=NOT_ASSESSED` verpflichtend | Geeignet, die Gegenbeispiele als ungelöst zu melden. Kein allgemeiner Identifikator. |
| Experiment Fabric | Explizite Modell-/Zustands-IDs und registrierte Likelihoods; Hashes für Aufträge und Daten | Kein spektrales Zusammenlegen kausaler Ordnungen gefunden. Aussage bleibt synthetisch und modellgebunden. |
| Neutral Discovery | Quotient nach gleichen Vorhersagen auf einem festen Interventionskatalog | Zulässige begrenzte Beobachtungsklassen. Keine Gleichheit unbekannter Mechanismen oder identifizierte Geometrie. |
| X6-QE / Wolfram-Kausalreferenzen | Nichtisomorphe isospektrale Beispiele werden gerade als Gegenkontrollen verwendet | Von H7 nicht entkräftet. |
| Signal-, Graphschranken-, Steuerungs- und Photonikmodule | Eigene Rohdaten, Matrizen, Referenzen und Geräteverträge; keine konkrete H7-Abhängigkeit gefunden | Kein H7-bedingter Gesamtstopp. Bestehende Mess-, Leistungs- und Hardwaregates bleiben offen. |
| NQK | Zugängliches Dossier enthält eigene Nicht-Eindeutigkeitsgrenzen; vier vollständige Archive fehlen | Keine H7-Abhängigkeit im zugänglichen Dossier gefunden. Fehlende Implementierungen können nicht entlastet werden. |

Die vollständige Einzelzuordnung mit Quellenpins steht in
[MODULE_REVIEW.md](MODULE_REVIEW.md). Eine Aussage „keine H7-Abhängigkeit
identifiziert“ bedeutet nicht „wissenschaftlich oder technisch vollständig
validiert“.

## Warum gleiche Wirkung kein Fehler sein muss

Die vier n=7-Gegenbeispiele besitzen im RAX-CQG-Kern dieselben Intervallzahlen
`N0=6`, `N1=2` und dieselbe dimensionslose BDG-Kombination `B4=19`. Das ist kein
Widerspruch: Eine Wirkung muss verschiedene Historien nicht eindeutig benennen.
In einer Summe über Historien dürfen verschiedene Zustände dieselbe Wirkung haben.

Wenn eine Signatur σ zur Vergröberung verwendet wird, müsste die Amplitude einer
Klasse beispielsweise als

\[
\widetilde a(s)=\sum_{[C]:\,\sigma(C)=s} a(C)
\]

gebildet werden, um die ursprüngliche endliche Summe zu erhalten. Einen beliebigen
Repräsentanten pro Klasse mit unverändertem Einzelgewicht zu behalten wäre im
Allgemeinen falsch. Schon bei Einheitseinträgen würde die H7-Zusammenlegung die
Zahl 2.045 durch 2.043 ersetzen. Dies ist eine bedingte mathematische Warnung vor
einer möglichen künftigen Implementierung; eine solche fehlerhafte Historienreduktion
wurde im geprüften ausführbaren Bestand nicht gefunden. Eine konsistente
Ereignis-/Dekohärenz-Vergröberung benötigt darüber hinaus ihren eigenen Vertrag.

## Sechs gezielte Gegenproben

[probes.py](probes.py) lädt unveränderte Dateien anhand ihrer Git-Revisionen,
nicht anhand zufällig aktueller Arbeitskopien. [probes.json](probes.json) enthält
alle Quellhashes und Ergebnisse.

1. Python importiert/exportiert vier n=7- und zwei n=8-Gegenbeispielmatrizen ohne
   Verlust. Unterschiedliche Matrizen eines Paars besitzen unterschiedliche
   gespeicherte SHA-256-Werte. Diese Hashes binden beschriftete Bytes; sie sind
   **keine** kanonischen Isomorphieschlüssel.
2. Ausdünnung mit Retention eins erhält dieselben sechs Relationen.
3. Der vorhandene Lorentz-Agent berechnet die vier n=7-Spektren übereinstimmend,
   weist die außerhalb n≤5 liegende Kanonisierung aber ausdrücklich zurück.
4. Der unveränderte JavaScript-Kern bewahrt alle sechs Relationen und liefert
   dieselben ganzzahligen BDG-Werte wie Python. Dies ist ein Kern-Test in Node,
   kein neuer visueller Browsertest.
5. Der gepinnte Fingerprint-Validator akzeptiert drei vollständige Vergleichsfälle
   als `EXACT_COLLISION`, einschließlich der n=8-Kollision mit D. Er lehnt drei
   erfundene physikalische Gleichheiten und drei unbelegte Trennungsabschlüsse ab.
   Er validiert gespeicherte Merkmalswerte; die exakte Ableitung aus Matrizen ist
   eine getrennte Rechnung im Audit, keine neue Fähigkeit des Validators.
6. Neutral Discovery erzeugt bei duplizierter Generatorbeschreibung dieselben
   drei registrierten Vorhersageklassen. `geometry=NOT_IDENTIFIED` bleibt erhalten.
   Der Test deckt den vorhandenen Interventionskatalog ab.

Alle sechs Gruppen bestanden, auch unter `python -O`. Sie beantworten die
konkrete H7-Abhängigkeitsfrage; sie ersetzen keine vollständigen Modultests,
Hardwaremessungen oder externe Begutachtung.

## Umfang und Grenzen der Sichtung

[scan.json](scan.json) enthält die gehashten Git-Dateien, Archivmitglieder,
Textfundstellen, Suchmuster und expliziten Ausschlüsse. Der Hauptzweig hat 963
versionierte Dateien. Die sechs registrierten Branch-Wurzeln sowie benannte
Querverweise auf Fingerprint, Fabric, n=6-Atlas und Lorentz-Kern wurden zusätzlich
einbezogen. ZIP-Inhalte wurden nur gelesen, nicht ausgeführt. PDF-Text und
Word-XML wurden extrahiert; Bilder und eingebettete Binärdaten wurden nicht
inhaltlich oder per OCR geprüft. Die Anzahl der inventarisierten Einträge zählt
auch mehrfach enthaltene Archivkopien, nicht unabhängige Studien.

Die Quellensuche dient der Fundstellensuche. Die Entscheidungen beruhen zusätzlich
auf der Sichtung der relevanten Klassenbildungs-, Vergleichs-, Import-/Export-
und Zustandswege sowie den Gegenproben. Es ist keine vollständige formale
Datenflussanalyse. Nicht registrierte Branches, andere Repositories,
unveröffentlichte Dateien, unbekannte NQK-Archive und spätere Revisionen liegen
außerhalb dieser Prüfung. Fehlende Quellen werden nicht als bestanden gewertet.

Historische Verträge, Originalarchive und Resultate wurden nicht umgeschrieben.
Aktueller H7-Status ist ausschließlich `REFUTED_BY_COUNTEREXAMPLE`; das ebenfalls
erfolgreiche Prüfstatusfeld `PASS` beschreibt die Rechnung, nicht die Hypothese.
Keine geplanten Jobs, Agenten, Geräte oder Dienste wurden abgeschaltet.

## Reproduktion

Voraussetzungen: vollständige Git-Objekte der angegebenen Revisionen, Python 3.12,
Node.js 24; für die Textsichtung zusätzlich Poppler `pdftotext`. Fehlende Branch-
Objekte gegebenenfalls zuerst über die registrierten Branches abrufen. Die
eigentliche Rechnung benötigt kein Netzwerk.

```sh
python3 -m venv /tmp/h7-audit-venv
/tmp/h7-audit-venv/bin/pip install -r research/lorentz_h7_dependency_audit/requirements.txt
/tmp/h7-audit-venv/bin/python -O research/lorentz_h7_dependency_audit/probes.py --output /tmp/h7-probes.json
cmp research/lorentz_h7_dependency_audit/probes.json /tmp/h7-probes.json
python3 -O research/lorentz_h7_dependency_audit/verify_review.py
python3 research/lorentz_h7_dependency_audit/scan.py --output /tmp/h7-scan.json
```

Der letzte Befehl wiederholt die Sichtung. Extrahierter PDF-Text kann zwischen
Poppler-Versionen abweichen; die Hashes der ursprünglichen Eingabedateien sind
davon unabhängig. `verify_review.py` prüft Quellenbindungen und Modulabdeckung,
nicht die Wahrheit semantischer Begutachtungsurteile. Die eigene GitHub-CI
wiederholt die Gegenproben ohne Netzwerk und vergleicht das Ergebnis bytegenau.

## Entscheidung für die weitere Arbeit

Das Programm kann innerhalb seiner bisherigen Evidenzgrenzen weitergeführt
werden. Der nächste fachliche Schritt ist die strukturelle Erklärung der
minimalen Gegenbeispiele. Vor einem künftigen Rekonstruktions- oder
Historienreduktionsmodul muss ein eigener Vertrag festlegen, welche Informationen
erhalten bleiben, welche Gleichheit beansprucht wird und wie Mehrdeutigkeit und
Gewichte behandelt werden. Ein ungeprüfter stärkerer Fingerprint ist kein Ersatz
für diesen Nachweis.
