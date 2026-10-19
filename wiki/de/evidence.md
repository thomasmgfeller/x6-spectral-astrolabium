# Prüfergebnisse richtig verstehen

Frage bei einem Ergebnis immer: Welche Aussage wurde geprüft, mit welchen Daten und unter welchen Bedingungen?

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/evidence.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-19 · `26432e3d4cde20adabb510f17d5639891f4ac642`

## Vier unterschiedliche Arten von Belegen

| Art | Was sie leisten kann | Was daraus nicht automatisch folgt |
| --- | --- | --- |
| Softwareprüfung | Ein Programm erfüllt die geprüften Regeln und Kontrollfälle. | Dass das Modell die Natur beschreibt. |
| Exakte endliche Rechnung | Eine mathematische Aussage gilt für die angegebenen endlichen Objekte. | Dass sie für alle Größen oder einen Kontinuumsgrenzfall gilt. |
| Synthetische Simulation | Ein Verhalten tritt unter den programmierten Modellannahmen auf. | Dass ein echtes Messgerät denselben Effekt zeigt. |
| Physische Messung | Daten eines realen Aufbaus stützen eine begrenzte Messbehauptung. | Allgemeine Gültigkeit ohne Kalibrierung, Unsicherheiten und Wiederholung. |

Ein archivierter Labordatensatz stammt aus realen Messungen. Seine Auswertung im Projekt ist dennoch keine neue eigene Geräteabnahme. Eine KI-Konzeptillustration ist kein Foto eines aufgebauten Experiments.

## Statuswörter übersetzen

| Status | Bedeutung |
| --- | --- |
| PASS | Die ausdrücklich geprüften Kriterien wurden erfüllt. |
| QUALIFIED_IN_DECLARED_MODEL | Alle festgelegten Hauptkriterien im ausdrücklich genannten Modell sind erfüllt; keine allgemeine physikalische Bestätigung. |
| FAIL | Mindestens ein bestimmtes Kriterium wurde verletzt. |
| INCONCLUSIVE | Die Frage bleibt mit dieser Prüfung unentschieden. |
| NOT_RUN / NOT_PERFORMED / NOT_EXECUTED | Die betreffende Prüfung wurde nicht ausgeführt. |
| INSUFFICIENT_COMMON_SUPPORT | Es gibt zu wenige passende Vergleichsfälle für die festgelegte Auswertung. |
| MAIN / BRANCH_ONLY | Beschreibt den Ablageort des Quellcodes, nicht seine wissenschaftliche Reife. |

Die genaue Bedeutung steht im jeweiligen Prüfvertrag. Beispiel: Ein Gegenbeispieltest kann PASS melden, gerade weil ein ungeeigneter Filter korrekt zurückgewiesen wurde.

## Nachrechnen ist mehr als eine Prüfsumme

Eine Prüfsumme wie SHA-256 hilft zu erkennen, ob Bytes verändert wurden. Sie beweist allein weder die Herkunft noch die Richtigkeit eines Ergebnisses. Ein Replay führt die Berechnung erneut aus. Ein getrennt programmierter Prüfer reduziert bestimmte gemeinsame Fehlerquellen; gleiche Autorenschaft oder Bibliotheken können trotzdem Abhängigkeiten erzeugen.

Externe Replikation bedeutet hier, dass andere Personen mit eigener Prüfung den Befund wiederholen. Automatische GitHub-Prüfungen und interne Gegenrechnungen sind wertvoll, ersetzen diesen Schritt aber nicht.

1. Lies die genaue Behauptung und die Grenzen.
2. Notiere Quellencommit, Datenstand, Zufallsseed und Softwareversionen.
3. Suche den ausgeführten Bericht, nicht nur einen geplanten Test.
4. Prüfe, ob Gegenbeispiele und unentschiedene Fälle erhalten sind.
5. Vergleiche das berichtete Ergebnis mit dem vorab festgelegten Kriterium.

- [Referenzedition und externe Reproduktion](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/reference-qe-v0.1/EXTERNAL_REPRODUCTION.md)
- [Numerische Reparatur und ursprüngliche Fehler](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/numerics-v1/README.md)

## Was ein Unsicherheitsintervall sagt

Ein Intervall beschreibt Unsicherheit unter einem bestimmten Auswertungsmodell. Wenn das Intervall für den Zusatznutzen sowohl negative als auch positive Werte enthält, ist ein Vorteil dadurch nicht nachgewiesen. Das ist kein Beweis exakter Gleichheit.

Bei gepaarten Vergleichen werden passende Fälle gemeinsam ausgewertet. Manche Bootstrap-Intervalle halten Training und Fallauswahl fest. Sie decken dann nicht zusätzlich die Unsicherheit durch andere Trainingsdaten, neue Erzeuger oder eine andere Auswahl ab.
