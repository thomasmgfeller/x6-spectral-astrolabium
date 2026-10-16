# RAX — Relationales Forschungsprogramm v0.1

**Forschungsfassung vom 14. Oktober 2026. Aktueller Stand: RAX-U1 als synthetische Kontrolle ausgeführt und intern gegengeprüft; technische Gesamtabnahme offen. RAX-B1-Messplanbenchmark ausgeführt, acht primäre Überlegenheitsentscheidungen unentschieden. RAX-U2 und die weiteren Forschungsversuche bleiben geplant.**

**Neu: [RAX-CQG Forschungsarchitektur v0.1](cqg-v0.1/README.md)** —
kausale Historien, diskrete Wirkung, Destillation und stabile Rekonstruktion.
[PDF, 19 Seiten](cqg-v0.1/RAX_CQG_Forschungsarchitektur_v0_1.pdf) ·
[Markdown](cqg-v0.1/ARCHITECTURE.md) ·
[Word](cqg-v0.1/RAX_CQG_Forschungsarchitektur_v0_1.docx).
Forschungsentwurf; CQG-01–08 sind noch nicht als Kampagne ausgeführt.

[Forschungsprogramm herunterladen (DOCX, 14 Seiten)](RAX_Relationales_Forschungsprogramm_v0_1.docx)

[RAX-U1-Gegenprüfung v0.1: Bericht und vollständiges Reproduktionspaket](countercheck-v0.1/README.md)

[RAX-B1-Benchmarking v0.1: gleiche Budgets, getrennte Prüfdaten und vollständige Ergebnisse](benchmark-v0.1/README.md)

[RAX-M1-Methodenprüfung v0.1: Datenlecks, Unabhängigkeit und Aussagegrenzen mit reproduzierbaren Gegenbeispielen](method-review-v0.1/README.md)

[RAX-W1-Wolfram-Gegenprüfung v0.1: 44 exakte Matrixfälle, symbolische Bedingungen und Gegenkontrollen](wolfram-check-v0.1/README.md)

Der [gemeinsame lokale Ablauf](../../INTEGRATION.md) installiert die Umgebung
und führt die vollständige B1/M1-Nachrechnung mit `python3 x6.py run rax` aus.
Prüfung und ZIP-Export verwenden dieselben Kommandos wie die Signal- und
Spektraladapter. Die veröffentlichten Forschungsarchive bleiben unverändert.

Das unveränderte Forschungsprogramm dokumentiert den Planungsstand vor den
U1-Läufen. Der später ausgeführte U1-Kontrollversuch und seine Gegenprüfung
werden im separat versionierten Paket dokumentiert. Die interne Gegenprüfung
bestätigt 160 Matrizen, 3,2 Millionen Übergänge und die Entscheidungen
8 gestützt / 16 verworfen / 16 unentschieden. Der Archivvorfall bleibt ungeklärt;
eine störungsfreie Erfassung und externe Begutachtung sind nicht nachgewiesen.

RAX untersucht, ob verschiedene relationale Mikrostrukturen eine gemeinsame
reduzierte Beschreibung zulassen, die neue Beobachtungen und kontrollierte
Interventionsantworten vorhersagt. Ein solcher prädiktiver Rückstand bleibt
relativ zum registrierten Messvertrag, zur Auflösung und zu den geprüften
Interventionen.

Die Leitfrage lautet: **Welche nächste zulässige Intervention liefert den
grössten erwarteten Informationsgewinn zwischen den noch möglichen
Erklärungsklassen?**

## Wissenschaftliche Regeln

- Exakte operationale Äquivalenz, statistische Nichtunterscheidbarkeit und
  strukturelle Äquivalenz werden getrennt behandelt.
- Eine Reduktion muss Vorhersagen auf neuen Daten erhalten. Ein konstanter
  Rückstand und verdeckte Zugriffe auf verworfene Mikrodaten sind Gegenkontrollen.
- Gesetzeskandidaten und konkurrierende Generatoren werden vor geometrischen
  oder theoretischen Deutungen geprüft. Gegenversuche erhalten eigene Prüfdaten.
- Lorentz, andere Geometrien und nicht geometrische Erklärungen unterliegen
  denselben Evidenzregeln. Lorentz-Symmetrie und Selbstähnlichkeit sind keine
  Optimierungsziele.
- Unentschiedene Ergebnisse, Modellraumversagen und fehlende geometrische
  Identifizierbarkeit sind zulässige Ausgänge.

## Arbeitspakete

| Paket | Gegenstand | Abnahme |
| --- | --- | --- |
| AP1 | U1-Vertrag, zwei endliche Markov-Mikrofamilien, exakter Referenzprüfer | Gültige Matrizen, analytische Reduktion, Gegenkontrollen und eingefrorener Vertrag |
| AP2 | Messadapter und statistische U1-Qualifikation | 160 Messzellen, simultane Fehlergrenzen, reproduzierbare Auswertung und explizite Statuswerte |
| AP3 | Offene U2-Suche nach Reduktionen und Generatoren; adaptive Messplanung | Neue Ensembles und Eingriffe; Vergleich mit festen und zufälligen Messplänen |
| AP4 | Skalenstudie mit verschiedenen Vergröberungsverfahren | Prädiktive Stabilität und kontrollierte endliche Grösseneffekte |
| AP5 | Geometrische Repräsentationen und Theoriepakete | Zusätzliche Messvorhersagen, mathematische Voraussetzungen und faire Konkurrenz |
| AP6 | RAX-S1 und unabhängige Gegenprüfung | Getrennte Informations-, Algebra- und Geometriediagnostik; reproduzierbare Gegenversuche |

Der erste Versuch **RAX-U1** nutzt eine absichtlich konstruierte gemeinsame
Markov-Reduktion und deren kontrollierte Verletzung. Seine Aufgabe ist die
Qualifikation der Methodik. Ein Bestehen wäre kein Nachweis einer neu entdeckten
Universalitätsklasse. Die offene Entdeckung beginnt erst mit RAX-U2.

Die Singularitätskette bleibt eine gesonderte, ungetestete Hypothese. Ein
Rangwechsel, eine veränderte Partition oder eine aus demselben Operator
abgeleitete metrische Degeneration genügt nicht als Nachweis einer
physikalischen Raumzeitsingularität.

## Bezug zu X6 und Evidenzstand

X6 soll Kandidatenregister, mehrschichtige Fingerprints, adaptive Messplanung,
verteilte Messnodes und ein unabhängiges Widerlegungsgate verbinden. Der
[bestehende logische Referenzversuch](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/1a02c482d59a42d554337fb83e0f6d6e6d84b516/experimental/neutral_discovery)
ist ein methodischer Vorläufer mit engerem Prüfbereich. Seine Softwareergebnisse
sind keine ausgeführten RAX-U1- oder RAX-U2-Ergebnisse.

Neben dem freigegebenen Forschungsprogramm ist nun das vollständige
[U1-Gegenprüfungspaket](countercheck-v0.1/README.md) verfügbar. Es enthält die
U1-Quellen, eingefrorenen Verträge, vollständigen und beschädigten Rohdaten,
Gegenprüfer und maschinenlesbaren Befunde. Der nächste technische Schritt ist
die Qualifikation dauerhafter Speicherung und einer vereinheitlichten
Ressourcenprüfung. U2 benötigt einen eigenen Prüfvertrag; physikalische
Nachweise bleiben ausstehend.

## Messplanbenchmark RAX-B1

Der separat ausgeführte [RAX-B1-Benchmark](benchmark-v0.1/README.md) vergleicht
adaptive, vorab optimierte feste und zufällige Messpläne bei Budgets 4, 8, 16
und 32. Alle 67.584 Testläufe wurden separat nachgerechnet. Adaptive Pläne
zeigen die kleinsten mittleren Prüf-Brier-Scores; die konservativen simultanen
Intervalle bestätigen keine Überlegenheit. Quellcode, sämtliche Rohdaten und
Nachrechnungen liegen im Reproduktionspaket. Das ist ein endlicher synthetischer
Vergleich der Messplanung und kein ausgeführtes RAX-U2. Rechenzeiten sind
Diagnostik; externe Begutachtung und physikalische Nachweise fehlen.

## Methodenprüfung RAX-M1

Die [interne nachträgliche Methodenprüfung](method-review-v0.1/README.md)
belegt zwei Validierungsfehler: Der Referenzprüfer akzeptiert eine gezielt
veränderte Kopie mit negativem Episodenindex und doppelter Kontrollzeile; ein
absichtlich prüfdatenabhängiger Planer besteht den bisherigen Isolationstest.
Weitere Versuche zeigen Grenzen der Callback-Abschottung und der Freeze-
Selbstauskunft. Exakte statistische Gegenbeispiele verdeutlichen die Folgen
falscher Unabhängigkeitsannahmen und selektiver Auswertung.

Die Originaldaten bestehen die strengere Abdeckungsprüfung und vollständige
Nachrechnung. Alle acht B1-Hauptentscheidungen bleiben unentschieden. Neun
Prüfblöcke wurden in einem frischen Verzeichnis reproduziert; ergänzende
Prüfregeln sind mitgeliefert. Die eingefrorenen Benchmarkquellen bleiben
unverändert. Externe Begutachtung oder physikalische Nachweise sind damit
nicht erbracht.

## Neuer geschützter Runner für begrenzte Planer

[RAX-G1](../../validation-v1/README.md) ergänzt einen neuen deklarativen
Ausführungsweg mit frischen öffentlichen Präfix-Prozessen, phasengebundener
Prüfdatenerzeugung, 33 Angriffskontrollen und dauerhaftem Fehlerbudget. Er führt
keinen beliebigen fremden Python-Code aus und ersetzt weder die historischen
B1-Quellen noch deren acht unentschiedene Entscheidungen. Externe Wiederholung
bleibt offen.

## Exakte Gegenprüfung mit Wolfram RAX-W1

Die [RAX-W1-Gegenprüfung](wolfram-check-v0.1/README.md) rekonstruiert 44 von
160 veröffentlichten U1-Matrixfällen separat in Wolfram Language. Alle
Matrix-Hashes und exakten Eigenschaften stimmen mit dem historischen Bericht
und beiden Python-Rechenwegen überein: zehn gültige starke Reduktionen und
34 erwartete Verletzungen bei positiver Störstärke. Symbolische Bedingungen,
verschobene Modelle, ein konstanter Wechselprädiktor und verdeckende Mittelung
werden mit exakten Gegenkontrollen untersucht.

Der vierseitige Bericht und das vollständige Paket enthalten alle Eingaben und
Antworten einschliesslich einer bei der Übertragung gekürzten Ausgabe. Die
vollständigen Teilausgaben sowie acht Manipulationsprüfungen des Abgleichs
bestanden. W1 ist eine interne nachträgliche Gegenprüfung mit anderem Rechenkern;
es ersetzt keine externe personelle Begutachtung oder physikalischen Nachweis.
U1- und B1-Entscheidungen bleiben unverändert. Die separate Offline-Nachprüfung
ist auf der W1-Seite dokumentiert.

## Dokumentstand und Lizenz

Die DOCX-Datei entspricht unverändert der freigegebenen Fassung. Ihr SHA-256 ist:

```text
1f76e77a5783802daee5034ee227d760270b0dd092bec070f26c9fbd4988ab28
```

Der Digest dient dem Inhaltsvergleich; er ist kein wissenschaftlicher Nachweis.
Die methodischen Quellen und ihre Geltungsgrenzen sind im Dokument aufgeführt.

Copyright 2026 Thomas Gfeller. Originale Projektbeiträge unter
[Apache-2.0](../../../LICENSE), gemäss
[Lizenzumfang](../../../LICENSE_SCOPE.md). Verlinkte Fachliteratur behält
ihre jeweiligen Rechte.
