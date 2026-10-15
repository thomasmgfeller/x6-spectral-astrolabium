# Modulregister — Abnahme am 15. Oktober 2026

**Lokale Registerabnahme bestanden.** Ein Leser findet vom README oder Portal
aus den Quellstand, den Startweg, die geprüfte Aussage und die nächste Abnahme
für jedes der 31 registrierten Module. Sieben Module benötigen weiterhin sechs
separate Forschungsbranches. Konzepte und das nicht vollständig ausführbare
NQK-Dossier sind ausdrücklich gekennzeichnet.

Der [Quellen-Snapshot](../MODULE_REGISTRY.json) umfasst alle 24 am Beginn
beobachteten Branches. Er ist eine datierte Bestandsaufnahme, kein Live-Monitor.
Der [lesbare Registertext](MODULE_REGISTRY.md) wird daraus erzeugt.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis / Beleg |
| --- | --- |
| Register, Quellpins, Dokument- und Programmeinstiege | PASS für 31 Module und 24 Branches; alle Git-Objekte und angegebenen Archiv-Einstiege vorhanden. [Bericht](module-register-evidence/register-check.json) |
| Negative Registerkontrollen | Veränderte UTC-Frist, unbekannter Commit und nicht vorhandener Einstieg werden abgelehnt. [Kontrollen](module-register-evidence/negative-checks.json) |
| Agentenfrist | Mathematikkonfiguration, Daten-/Quellenworkflow und UTC→Europe/Zurich-Umrechnung stimmen überein: exklusiv 19.10.2026, 00:00 Uhr Zürich. Kein Agentenlauf wurde durch die lokale Abnahme gestartet. |
| Hauptnavigation | README, Portal, Integrations- und Lorentz-Anleitung verlinken das Register. HTML-Prüfung: eindeutige IDs, beide Registerlinks und korrektes datetime-Attribut. |
| Frischer Checkout | PASS_CORE_WORKFLOW, 19/19 Schritte, einschliesslich 12 bestehender Integrationsregressionen. Installation, Signal/Spektral/RAX, ZIP-Export und Replay, Ablehnung ungültiger Jobs und Überschreibschutz bestanden. [Bericht](module-register-evidence/fresh-checkout/qualification.json), [Logs](module-register-evidence/fresh-checkout/) |
| RAX-W1 und Wolfram-Fälle 2, 4, 5 | Fünf Offline-Kommandos Exit 0. Fall 2 führt zusätzlich X6 in Node erneut aus. Kein neuer Wolfram-Kernelaufruf. [Befehle und Laufzeiten](module-register-evidence/archive-replays.json) |
| Übernommene Branch-Inhalte | n=6-, Industrial-V1-, Fingerprint- und Fabric-Dateien sind im späteren Neutral-Discovery-Stand bytegleich zu ihren eigenen Quellpins. [Vergleich](module-register-evidence/inherited-module-comparison.json) |
| Quellinventare | PASS_WITH_EXCLUSIONS nach der dokumentierten Inventarkorrektur; keine fehlenden/ungeführten Dateien. Die schon vorhandenen historischen Ausnahmen bleiben ausdrücklich sichtbar. |
| Geschützte Forschung | Signal-Lab-Buildprüfung besteht. App, mathematische Kerne, Agentenkonfiguration, drei Agentenworkflows, Budgets und alle bisherigen ZIP-Archive sind bytegleich zum Ausgangsstand. |

Die frische Checkout-Abnahme lief auf dem ersten Register-Implementierungscommit
`7c14eaf` (lokaler Commit; vollständige SHA im Bericht), Linux x86-64, Python 3.12.14,
Node 24.19.0, NumPy 2.3.5 und SciPy 1.17.0. Der Checkout begann ohne virtuelle
Umgebung und blieb nach dem Lauf sauber; alle getrackten Dateien blieben
unverändert. Die späteren Änderungen betreffen Navigationslinks, eine
README-Grössenangabe, diesen Bericht und dazugehörige Inventare, keine der
qualifizierten Laufzeitquellen.

Der exakt lokal geprüfte Commit ist im
[Git-Bundle](module-register-evidence/qualification-source.bundle) erhalten.
In einem separaten Checkout mit dem main-Ausgangscommit lässt er sich mit
`git fetch /pfad/zu/qualification-source.bundle HEAD` und
`git checkout FETCH_HEAD` wiederherstellen. Der öffentliche Publikationscommit
kann eine andere SHA haben; die geprüften Laufzeitquellen bleiben bytegleich.

Die lokalen Browsertests wurden in diesem Lauf **NOT_EXECUTED**. Der vorhandene
Integrationsworkflow führt die vollständige Browser-/CLI-Abnahme im Pull Request
aus; dessen Ergebnis ist im konkreten Actions-Lauf zu lesen. Dieser lokale
Bericht nimmt keinen Remote-Erfolg vorweg. Die erzeugten Lauf-/Exportdaten wurden
für den Test neu angelegt; hier sind der Bericht und sämtliche Schrittlogs
enthalten, keine zweite Veröffentlichung der unveränderten RAX-Roharchive.

## Vorbestehender Inventarfehler

Ein unveränderter Checkout von `1dd5f65e1046edab6175998552362ad3856f8549`
lieferte bereits FAIL: zwei veraltete README-Hashbindungen sowie acht nicht im
Repository-Inventar erfasste Dateien der Wolfram-Fälle 4 und 5.
[Unveränderter Ausgangsbefund](module-register-evidence/baseline-inventory.json).

Die acht veröffentlichten Dateien sind nun explizit inventarisiert. Aktuelle
Navigationsdokumente erhalten passende Hashes. Der ursprüngliche ACVM-README-Hash
bleibt als historische Angabe im Publikationsmanifest erhalten; die Original-
Konzeptdokumente sind unverändert. Keine unbekannten Dateien werden pauschal
ausgenommen, und die Inventarprüfung wurde nicht abgeschwächt.

## Reichweite der Abnahme

Diese Arbeit prüft Auffindbarkeit, konsistente Statusangaben und die genannten
Softwarewege. Sie führt keine unabhängige wissenschaftliche Gesamtbegutachtung,
neue physische Messung oder neue Forschungskampagne durch. Nicht jedes
Forschungsmodul wurde erneut vollständig berechnet; die übrigen Evidenzangaben
verweisen auf ihre tatsächlich vorhandenen, getrennt datierten Belege.
Eine neue Registerzeile macht weder einen Entwurf ausführbar noch einen
synthetischen Befund zu einem Geräte- oder Theorienachweis.
