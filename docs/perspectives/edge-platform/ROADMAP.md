# Roadmap — X6 als erste Edge-Referenz

14. Oktober 2026. Entwicklungsziele, keine zugesagten Produkteigenschaften.

| Stufe | Lieferumfang | Abnahme |
| --- | --- | --- |
| 0 — Lokaler Ausgangspunkt | Bestehender Signal-Lab-Kern, JSON-Auftrag, CLI, Laufnachweis, Replay | Dokumentierter frischer lokaler Lauf; Positiv- und Negativfälle; unabhängige numerische Gegenprüfung |
| 1 — Wiederverwendung | Zweite kleine Anwendung, gemeinsamer eingefrorener App-Vertrag, getrennte fachliche Logik | Beide Anwendungen erfüllen ihren eigenen Referenztest ohne app-spezifische Änderung am gemeinsamen Kern |
| 2 — Plattformtransfer | Benannte Linux-ARM64- und Linux-x86-64-Systeme | Frische Installation je System, gleiche Eingaben, vorab festgelegte Numeriktoleranzen und Ressourcenbudgets |
| 3 — Reale Sonde | Ein lesender Geräteadapter, Zeitbasis, Einheiten, Puffer, Fehlerkennzeichen | Vergleichsmessung im definierten Bereich; Datenlücken und Drift sichtbar; Simulator getrennt ausgewiesen |
| 4 — Zuverlässiger Betrieb | Persistente Aufträge, Abbruch, Wiederanlauf, Ressourcenlimits, Berechtigungen | Fehler- und Negativsuite; keine falsche Ergebnisfreigabe; dokumentierte Wiederherstellung |
| 5 — Externer Pilot | Fünf bis acht externe Maker-/Labor-Teilnehmende, direkter Vergleichsweg | Gemessener Einrichtungs- und Integrationsaufwand sowie Wiederverwendung rechtfertigen den Ausbau |
| Optional | Mehrere Worker, WASM, Beschleuniger, Post-Quanten-Transportprofile | Eigene Konformitäts- und Leistungsnachweise je Erweiterung |

Stufe 0 bildet nur einen Teil der im Plattformkonzept beschriebenen Stufe A ab.
Sie erfüllt insbesondere nicht dessen Drei-App-, Zulassungs- und Plattformgates.
Die dort genannten 20 Prozent Aufwandseinsparung und 10 Prozent Laufzeitaufschlag
sind vorgeschlagene Pilotgrenzen, keine gemessenen Ergebnisse dieser Ausgabe.

Vor jedem Vergleich werden Workloads, Referenzverfahren, Qualitätsgrenzen,
Hardware, Messverfahren und Abbruchentscheidungen festgehalten. Änderungen nach
Sichtung von Testergebnissen erzeugen eine neue Versuchsserie. Ein Ergebnis
einer Anwendung darf Fehler in einer anderen nicht durch Mittelung verdecken.

Ein eigenes Plattform-Repository wird sinnvoll, wenn mindestens zwei Anwendungen
einen gemeinsamen Kern tatsächlich nutzen. Bis dahin hält dieser Zweig den
Entwicklungs- und Wartungsumfang begrenzt.
