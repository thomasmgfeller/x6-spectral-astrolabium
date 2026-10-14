# X6 Edge Reference — Entwicklungsperspektive

Stand: 14. Oktober 2026. **Experimenteller Softwarestand 0.1.0; keine produktive Freigabe.**

Dieser Forschungszweig untersucht, wie vorhandene X6-Rechenfunktionen als
lokale, nachvollziehbare Anwendung einer künftigen Edge-Plattform ausgeführt
werden können. Die Veröffentlichung liefert einen kleinen ausführbaren Einstieg
und das weiter gefasste [Plattformkonzept 0.1](Edge_Application_Platform_Konzept_v0_1.docx).
Das Word-Dokument wird unverändert veröffentlicht. Die Plattformbeschreibung
ist ein Entwurf; ihre Freigabegates sind durch diesen Demonstrator nicht erfüllt.

## Jetzt ausprobieren

[Startanleitung und Quellcode](../../../experimental/edge_reference/README.md)
führen einen JSON-Auftrag mit dem bereits vorhandenen X6 Signal-Lab-Kern aus.
Das Ergebnis enthält synthetische Zeitreihen, vier Vergleichsverfahren,
Qualitätskennwerte und einen exportierbaren Laufnachweis. Ein zweiter Aufruf
prüft Dateiintegrität, Zuordnung zum Auftrag und numerische Wiederholung.

Der Kernel wird über seine vorhandene JavaScript-Schnittstelle wiederverwendet.
Ein neues physikalisches Modell oder eine überlegene Entrauschungsmethode wird
daraus nicht abgeleitet. Der X6-Phasenfilter bleibt eines der zu prüfenden Verfahren.

## Status und Grenzen

| Bestandteil | Status dieser Ausgabe |
| --- | --- |
| Lokaler JSON-Auftrag und Node.js-Ausführung | Implementiert; siehe [Prüfbericht](VALIDATION.md) |
| Export und rechnerische Wiederholung | Implementiert, gleicher Rechenkern; kein unabhängiger Beweis |
| NumPy/SciPy-Gegenprüfung | Bestehende unabhängige Tests; aktueller Lauf im Prüfbericht |
| Hardwaremessung und Sondenadapter | Nicht in diesem Referenzumfang implementiert |
| Generischer App-Vertrag und Gerätevertrag | Konzept; der lokale Job-Vertrag ist nur ein begrenzter Vorläufer |
| Persistenter Scheduler, mehrere Worker, Wiederanlauf | Geplant; ein Ergebnisverzeichnis ist keine Job-Datenbank |
| ARM64/x86-64-Transfer und Wiederverwendung in weiteren Apps | Offen; ein Lauf auf einer Architektur belegt keinen Transfer |
| Sicherheitsisolation, Paketidentitäten, Post-Quanten-Profil | Nicht implementiert oder geprüft durch diesen Demonstrator |
| Maker-ready, Laborfreigabe, Industriereife | Nicht erreicht |

## Repository-Struktur

- `experimental/edge_reference/`: ausführbarer begrenzter Referenzadapter.
- `docs/perspectives/edge-platform/`: Konzept, Roadmap, Vertragsbeschreibung und Prüfnachweise.
- Branch [`research/x6-edge-reference`](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/research/x6-edge-reference): Ausgangspunkt für weitere Entwicklungsarbeit.
- `main`: dokumentierter veröffentlichter Ausgangsstand, ausdrücklich experimentell.

Der Plattformkern soll anwendungsunabhängig werden. Dafür reicht X6 allein nicht:
Die nächste Generalisierung muss an einer zweiten unabhängigen Anwendung geprüft
werden. Die [Roadmap](ROADMAP.md) bindet Ausbauschritte an konkrete Abnahmekriterien.

## Lizenz und Mitwirkung

Für eigene Projektbeiträge gilt die bestehende [Apache License 2.0](../../../LICENSE)
gemäss [Lizenzumfang](../../../LICENSE_SCOPE.md). Copyright 2026 Thomas Gfeller.
Separate Lizenzen und fremde Rechte gelten unverändert.

Besonders hilfreich sind reproduzierbare Installationsberichte, konkrete
Fehlfälle und Adapter für klar benannte Geräte mit dokumentiertem Messbereich.
Bitte Betriebssystem, Architektur, Node-Version, Commit und vollständigen
Fehlertext angeben; vertrauliche Messdaten gehören nicht in öffentliche Issues.
