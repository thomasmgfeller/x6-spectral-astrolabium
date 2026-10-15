# Ein klarer Weg in die Forschung

Wähle einen praktischen Einstieg, verstehe die Evidenzklassen und finde die genauen Quellen hinter einem Ergebnis.

## 1. Das Projekt verstehen

Ein Signal ist eine Folge von Messwerten, etwa eine Schwingung im Zeitverlauf. Ein Graph beschreibt Elemente und ihre Verbindungen. Eine kausale Ordnung beschreibt, welche Ereignisse vor anderen liegen. X6 untersucht Methoden, solche mathematischen Objekte zu analysieren und die Ergebnisse zu prüfen.

Ein Spektrum ist eine aus einer Matrix berechnete Sammlung von Werten. Unterschiedliche Strukturen können dasselbe Spektrum besitzen; das Projekt enthält konkrete Gegenbeispiele. Ein sichtbares Muster allein belegt weder Primzahlstrukturen noch einen neuen physikalischen Mechanismus.

Der aktuelle Schwerpunkt ist die lorentzsche Spektralgeometrie. Signalverarbeitung, RAX, Photonik und industrielle Datenstudien haben jeweils eigene Geltungsbereiche und Abnahmekriterien. Ein fertiger Quantencomputer oder eine bewiesene Quantengravitationstheorie werden nicht behauptet.

- [Lorentz: exakte endliche Referenzen kausaler Ordnungen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/lorentz-n6-residuals.html)
- [X6-QE: unterschiedliche Strukturen mit gleichem Spektrum](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/x6-qe.html)
- [Alle registrierten Forschungsmodule](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/index.html)

## 2. Ein Browserexperiment ausprobieren

Öffne das Signal Validation Lab. Beginne mit einem synthetischen Beispiel, dessen sauberes Signal bekannt ist. Vergleiche Original, verrauschte Version und Ausgaben der Referenzfilter. Prüfe Rekonstruktionsfehler ebenso wie spektrale Zusammenfassungen.

Erkunde die dokumentierten Gegenbeispiele, etwa die Vorzeichenumkehr: Ein Signal und sein Negatives können dasselbe Leistungsspektrum besitzen. Ähnliche spektrale Kennzahlen belegen deshalb keine originalgetreue Signalrekonstruktion.

Exportiere die Experimentdaten und prüfe die Rechnung über den dokumentierten Import- und Replay-Weg. Erfolgreiches Nachrechnen zeigt rechnerische Konsistenz in diesem Verfahren; es beweist weder Datenauthentizität noch physische Geräteleistung.

- [Signal Validation Lab öffnen (DE / EN / FR)](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Geltungsbereich und erwartete Ergebnisse lesen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/signal-lab.html)
- [Die ursprüngliche Astrolabium-Anwendung öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/index.html)
- [Den lokalen Arbeitsablauf installieren und starten](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/integration.html)

## 3. Eine Referenzrechnung reproduzieren

Für die gemeinsame Offline-Referenzsuite werden zunächst Git, Python 3.12 und Node.js 24 benötigt. Das Klonen braucht Netzwerkzugriff; die Referenzrechnung selbst benötigt keinen Paketdownload und keinen neuen Wolfram-Aufruf. Verwende einen neuen Ausgabeordner.

Die Befehle unten prüfen den aktuellen main-Checkout. Für ein versioniertes Ergebnis verwende die Seite zur Referenzausgabe und deren gepinnten Quellencommit oder unveränderliches Release-Paket. Halte Commit und Laufzeitversionen im Prüfbericht fest.

Erwarteter Status: PASS_OFFLINE_REFERENCE_REPLAY. Lies die Geltungsbereiche der Einzelberichte und die Negativkontrollen. Auch die korrekte Reproduktion eines negativen oder unentschiedenen wissenschaftlichen Ergebnisses kann eine bestandene Softwareprüfung sein.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6
cd x6
python3 -S -B x6.py reference qualify --output /tmp/x6-reference-evidence
```

- [Gepinnte Referenzausgabe und externe Nachrechnungsanleitung](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/reference-edition.html)
- [Offline-Suite: Voraussetzungen, Evidenz und nächste Abnahme](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/offline-reference.html)
- [Vollständige Dokumentation der Offline-Suite](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md)
- [Ein reproduzierbares Ergebnis oder Gegenbeispiel melden](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/new/choose)

## 4. Status und Evidenz richtig lesen

MAIN bedeutet, dass die registrierte Quelle im Hauptzweig liegt. BRANCH_ONLY bedeutet, dass der dokumentierte Forschungsstand den genannten Branch und Quellencommit benötigt. Das sind Angaben zum Quellenort, keine Qualitätsbewertungen.

SOFTWARE bezeichnet einen begrenzten ausführbaren Prüfweg. CONCEPT und DOSSIER bezeichnen Pläne oder Dokumente ohne eigenständig ausführbares Gesamtpaket. Ein Photonikmodul kann SOFTWARE sein, weil seine digitale Referenz prüfbar ist, während der physische Aufbau noch unqualifiziert bleibt.

Eine exakte endliche Rechnung betrifft ihre festgelegten endlichen Objekte. Eine numerische Simulation betrifft ihr Modell und dessen Annahmen. Archivierte Labordaten sind Messungen aus ihrem ursprünglichen Erhebungskontext. Daraus folgen nicht automatisch eine neue physische Messung, industrielle Überlegenheit oder unabhängige externe Begutachtung.

PASS, FAIL, NOT_RUN, NOT_READY und INCONCLUSIVE haben verschiedene Bedeutungen. Lies Aussage, Evidenzbericht und nächste Abnahme gemeinsam. Jeder Evidenzbericht behält seine eigene Prüfrevision; ein neuer Quellenpin qualifiziert veränderten Code nicht rückwirkend.

- [Die Geltungsbereiche aller Module lesen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/modules/index.html)
- [Massgebliches maschinenlesbares Register](https://thomasmgfeller.github.io/x6-spectral-astrolabium/MODULE_REGISTRY.json)

## 5. Zitieren, nachnutzen und beitragen

Zitiere das tatsächlich verwendete Release oder den genauen Commit und externe Datensätze separat. CITATION.cff beschreibt die ausgewählte endliche Referenzausgabe; es ist keine Zertifizierung aller Module.

Eigene Projektbeiträge stehen unter Apache-2.0. Separat lizenzierte Komponenten und Daten behalten ihre Bedingungen. Enthaltene Paderborn-Daten bleiben CC BY-NC 4.0; das Portal erteilt dafür keine kommerziellen Nutzungsrechte.

Sinnvolle Beiträge sind unabhängige Reproduktionen, Gegenbeispiele, Verbesserungen der Zugänglichkeit und verständlichere Dokumentation. Die optionale llms.txt und der JSON-Index helfen bei der Orientierung; sie garantieren keine Indexierung, Rangfolge oder Aufnahme in KI-Antworten.

- [Zitationsmetadaten](https://thomasmgfeller.github.io/x6-spectral-astrolabium/CITATION.cff)
- [Lizenzumfang und Bedingungen für Drittinhalte](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/LICENSE_SCOPE.md)
- [Hinweise für Beiträge](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CONTRIBUTING.md)
- [Optionaler Wegweiser für KI-Werkzeuge](https://thomasmgfeller.github.io/x6-spectral-astrolabium/llms.txt)
- [Sitemap der Dokumentation](https://thomasmgfeller.github.io/x6-spectral-astrolabium/sitemap.xml)

