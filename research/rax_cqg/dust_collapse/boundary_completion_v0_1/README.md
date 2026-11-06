# CST-DUST: Innen-/Außenraum-Anschluss v0.1

**Klassische Referenz geschlossen. Physikalischer CST-Anschluss weiterhin
HOLD_NOT_ELIGIBLE / NOT_RUN. Regularität und Fortsetzung für CST bleiben
getrennt HOLD.**

Das Paket schließt den endlichen marginal gebundenen Einstein-Staubball an
einen vollständigen Schwarzschild-Außenraum an. Es umfasst die erste und zweite
Fundamentalform, die Feldgleichungen beiderseits, distributionelle Erhaltung,
den regulären Horizontdurchgang und die asymptotische Region. Unter ausdrücklich
zusätzlicher klassischer Zukunftswahl wird auch der Ereignishorizont angegeben;
diese Zukunft bleibt singulär.

Ein schichtfreier Bounce ist im untersuchten Schwarzschild-Sektor ausgeschlossen.
Eine bedingte statische Nichtvakuum-Vergleichsgeometrie demonstriert den nötigen
effektiven Stress, ohne den verworfenen Bounce-Kandidaten wieder freizugeben.
Ihre globale Fortsetzung wird nicht als qualifiziert ausgegeben. Exakte
Kettenkontrollen zeigen außerdem den Verlust von Wirkungsbeiträgen beim
isolierten Abschneiden von Teilgebieten. Diese Kontrollen sind keine
vierdimensionalen dynamischen Kausalset-Ensembles.

## Lesen

- `CST_DUST_Innen_Aussen_Anschluss_v0_1.pdf`: neunseitiger Ergebnisbericht.
- `DERIVATION.md`: Voraussetzungen, vollständige Herleitungen, Quellen und
  wissenschaftliche Geltungsgrenzen.
- `plan.json`, `plan.sha256`: vor der neuen Rechnung lokal fixierter Plan;
  keine externe Präregistrierung oder verblindete Vorhersageprüfung.
- `results/closure_decision.json`: getrennte Abschlussentscheidungen.
- `results/checkpoint_P5_records.json`, `checkpoint_P5_audits.json`:
  60 Datensätze nach dem unveränderten Modellvertrag; alle acht physikalischen
  Gates bleiben HOLD. Die vier Dichtestufen sind **geplant**, nicht ausgeführt.

## Nachrechnen

Referenzumgebung: Python 3.12.14, SymPy 1.14.0, mpmath 1.3.0. Im entpackten
Paketverzeichnis:

```sh
python3 -m pip install -r requirements.txt
python3 -O -B analyze.py
```

Die Prüfung benötigt keine Netzwerkverbindung und keine Zufallszahlen.
Das Installieren fehlender Abhängigkeiten kann eine Netzwerkverbindung benötigen.
Das Skript überschreibt seine eigenen Dateien in `results/` deterministisch.
Die Kontrollen verwenden explizite Ausnahmen, sodass `python -O` keine Prüfung
abschaltet. `symbolic_checks.py` berechnet die Einstein-Tensoren direkt aus den
vierdimensionalen Metriken. Die geerbte Intervallarithmetik ist unverändert.

Erwartet werden:

| Prüfung | Umfang |
| --- | ---: |
| Exakte symbolische Identitäten | 34 |
| Klassische Oberflächenfälle | 15 |
| Klassische Außenraumwerte | 75 |
| EF-Einbettungen einschließlich Horizontdurchgang | 9 |
| Bedingte klassische Ereignishorizontfälle | 3 |
| Bedingte Nichtvakuum-Anschlüsse | 20 |
| Kausale Kettenschnitte | 27 |
| Labelpermutationen | 24 |
| Entscheidungskontrollen | 19 |
| P5-Datensätze, sämtliche physikalischen Gates HOLD | 60 |
| Neue dynamische CST-Ensembles | 0 |

Alle 34 symbolischen Restwerte sind exakt null. Die größte klassische numerische
Resthülle ist `1.069476213704089327604567990955E-29`, unter dem vorher fixierten
technischen Cap `1e-20`. Das ist eine algebraische Nachrechnungsgrenze und keine
physikalische Genauigkeitsangabe. Quadrat- und Kubikwurzeln werden durch
100 rationale Bisektionen eingeschlossen; weitere Operationen verwenden
60-stellige nach außen gerundete Decimal-Arithmetik.

Die Zahlenläufe setzen `G = c = 1`. Geprüfte Zeiten bleiben im bisherigen
gemeinsamen Fenster, sofern eine Zeile nicht ausdrücklich als analytische
klassische Fortsetzung markiert ist. Keine Toleranz aus P3/P4 wurde geändert.

## Bericht erneut erzeugen

```sh
python3 -m pip install -r report-requirements.txt
python3 build_report.py
```

Dies erzeugt die beiden Darstellungsfiguren in `figures/` und den PDF-Bericht
unter `../output/pdf/CST_DUST_Innen_Aussen_Anschluss_v0_1.pdf`. Benötigt werden
die DejaVu-Schriften in `/usr/share/fonts/truetype/dejavu/`. Diagramme dienen
der Darstellung; sie sind keine zusätzliche numerische Evidenz. PDF-Metadaten
können bei erneutem Erzeugen variieren.

## Herkunft und Integrität

Ausgangspunkt ist der veröffentlichte Main-Commit
`bb59cc03e762b5b2133f4f12fdd975b219bf4406` nach
[PR 242](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/242).
`inputs/provenance.json` enthält die unveränderten Eingabeprüfsummen;
`results/run_manifest.json` dokumentiert die ausgeführten Quelltexte und Versionen.
`SHA256SUMS.txt` erfasst alle ausgelieferten Paketdateien außer sich selbst.
Vor erneutem Erzeugen können diese unter Linux mit
`sha256sum -c SHA256SUMS.txt` geprüft werden. Bei abweichenden Python-Versionen
kann sich der Versionsanteil des Manifests und damit dessen referenzierte
Prüfsumme ändern; numerische Ergebnisse und Entscheidungen bleiben getrennt
zu vergleichen.

Ein isolierter Replay des numerischen Pakets wurde mit der genannten
Referenzumgebung durchgeführt; Ergebnisdateien müssen dabei bytegleich sein.
Der Bericht wurde auf neun Seiten gerendert und visuell geprüft.

Lizenz: Apache-2.0 gemäß `LICENSE` und `NOTICE`. Die Literatur wird zitiert;
ihre Ergebnisse werden nicht als neue CST-Herleitung ausgegeben. Die konkrete
noch fehlende CST-Wirkung, der Außenraumzustand, die physikalisch abgeglichene
Verfeinerung sowie uniforme Regularitäts- und Fortsetzungskontrollen werden
in `DERIVATION.md` und `results/closure_decision.json` benannt.
