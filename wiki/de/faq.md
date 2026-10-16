# Häufige Fragen und Hilfe

Kurze Antworten für den Alltag – mit dem passenden Weg zu den Details.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/faq.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-16 · `08c64744caa584c940b45a8825d0b099ae0c92fb`

## Brauche ich Mathematikkenntnisse oder ein Konto?

Zum Lesen und für die öffentlichen Browserlabore brauchst du kein GitHub-Konto. Für den ersten Signalversuch reicht Neugier. Mathematik und Programmierung werden wichtig, wenn du Beweise, Quellcode oder neue Forschungsfragen selbst prüfen möchtest.

## Ist X6 ein Quantencomputer oder eine bewiesene Gravitationstheorie?

Nein. Das Projekt enthält Forschungsfragen mit Quanten- und Raumzeitbezug, außerdem klassische Rechenwerkzeuge und endliche Referenzen. Der Browserbenchmark setzt bei seiner Zweiqubit-Uhr Quantenmechanik voraus; er leitet sie nicht aus der kausalen Ordnung her.

## Alles ist grün. Ist meine Hypothese damit bewiesen?

Nur die angegebenen Prüfbedingungen sind bestanden. Ein mathematischer Beweis braucht eine passende allgemeine Argumentation. Eine Aussage über die Natur braucht geeignete physische Daten. Auch viele kopierte oder abhängige Versuche sind nicht automatisch viele unabhängige Bestätigungen.

## Ein Filter zeigt FAIL. Ist die App kaputt?

Nicht unbedingt. Der Versuch kann korrekt zeigen, dass dieser Filter bei diesen Einstellungen Information verliert. Kontrolliere zuerst Referenz, Störungen und Kriterien. Melde einen Fehler, wenn die Berechnung oder Bedienung selbst nicht mit der Dokumentation übereinstimmt.

## Der lokale Start oder Export funktioniert nicht

- Starte die Befehle im Projektordner, in dem x6.py liegt.
- Prüfe die Voraussetzungen mit doctor --profile research.
- Verwende bei belegtem Port serve --port 8001.
- Wähle einen neuen Ausgabeordner, statt einen alten Lauf zu überschreiben.
- Für JSON-Exporte verwende einen Browser mit WebCrypto über HTTPS oder localhost.
- Lies bei einem Abbruch die Logs und den Fehlerbericht; ein unvollständiger Lauf ist kein abgeschlossener Nachweis.

- [Vollständige lokale Anleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md)

## Wie melde ich einen Fehler oder helfe mit?

Eine hilfreiche Meldung nennt den Commit, Browser bzw. Laufzeitversion, die genauen Schritte, Eingabedaten oder Seed, das erwartete und das tatsächliche Ergebnis sowie die Fehlermeldung. Entferne vertrauliche Daten, bevor du sie in ein öffentliches Issue einfügst.

Besonders nützlich sind verständliche Gegenbeispiele, externe Wiederholungen und konkrete Dokumentationskorrekturen. Auch ein negatives Ergebnis hilft, wenn klar ist, was geprüft wurde.

- [GitHub-Issues](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues)
- [Beitragsrichtlinien](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CONTRIBUTING.md)

## Darf ich X6 weiterverwenden und zitieren?

Eigene Projektbeiträge stehen unter Apache-2.0. Drittinhalte und Datensätze behalten ihre eigenen Bedingungen; für den verwendeten Paderborn-Datensatz gilt eine separat dokumentierte nichtkommerzielle Lizenz. Prüfe den Lizenzumfang der konkreten Datei.

Nenne beim Zitieren das Projekt, den genauen Commit oder die Veröffentlichung und den verwendeten Prüfbericht. Übernimm dessen Grenzen. Die Zitiermetadaten sind ein Einstieg; eine allgemeine Wiki-Zitation ersetzt die konkrete Ergebnisquelle nicht.

- [Zitiermetadaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CITATION.cff)
- [Lizenzumfang](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/LICENSE_SCOPE.md)

## Wie wird dieses Wiki gepflegt?

Deutsch und Englisch werden gemeinsam versioniert. Die Seiten sind auch ohne JavaScript lesbar und als Markdown verfügbar. Aktualisierungen beginnen bei den Originalquellen und ihren ausgeführten Berichten; geplante Tests werden nicht allein durch eine Textänderung zu bestandenen Tests.

- [Wiki-Quellen und Pflegeanleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/wiki/README.md)
