# Photonic Link Validation Lab — v0.1.0

Ein neuer Forschungszweig für die **gemeinsame Modellierung von Verlust,
Polarisationsdrift und Zeitzuordnung** eines elementaren Photonenpaar-Links.
Ergebnis dieser Version ist reproduzierbare Forschungssoftware mit Prüfprotokoll.
Es liegen hier **keine neuen Hardwaremessungen, kein Sicherheitsbeweis und kein
Nachweis eines Quantenvorteils** vor.

Der Zweig `research/photonic-link` baut auf Astrolabium-Commit
`132f1df9cc8b97c29d8a8cebb86a17061a2714ce` auf. Er übernimmt ausgewählte
Sagnac-Referenzen unverändert und numerische NQK-Referenzfunktionen mit Herkunfts-
und Lizenznachweis. Die früher vorgeschlagene geometrische Schutzlogik wird
ausdrücklich nicht als physikalische Grundlage übernommen.

## Einstieg

- [Forschungsprogramm und Entscheidungstore](docs/RESEARCH_PROGRAM.md)
- [Mathematisches Modell, Annahmen und Gültigkeitsbereich](docs/MODEL.md)
- [Messplan, Identifizierbarkeit und Unsicherheiten](docs/METROLOGY.md)
- [Übernahme- und Behauptungsregister](docs/ADOPTION.md)
- [Primärquellen mit Verwendungszweck](docs/REFERENCES.md)
- [Ausführbare Validierung](validate.py) und [gespeicherte Ergebnisse](evidence/validation.json)
- [Synthetische Szenarien und Wiederholungen](evidence/experiments.json)
- [Lesbare Ergebnisse einschließlich Fehlfällen](docs/RESULTS.md)

## Reproduzieren

Im Repository:

```bash
cd research/photonic-link
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python validate.py --output /tmp/plvl-validation.json
python experiments.py --output /tmp/plvl-experiments.json
python -m plvl configs/coupled.json --output /tmp/plvl-run.json \
  --raw-output /tmp/plvl-events.npz --snapshot-output /tmp/plvl-snapshot.bin
```

Ausgabepfade müssen neu sein. Ein erfolgreicher Lauf erfordert Exit-Code 0.
Die NPZ-Datei enthält lokale Zeitstempel und Ports sowie die korrigierte gemeinsame
Ereignisliste; keine versteckten Paar-IDs. Der Bericht kennzeichnet interne
Simulationswahrheit separat. SGNCv007 exportiert nur aggregierte synthetische
Zähler. Einstellungsindex 0 ist dabei ein Etikett, keine Behauptung über CHSH-Winkel.

Optional führt `validate.py --ghdl /pfad/zu/ghdl --output /tmp/plvl-full.json`
die unveränderten RTL-Referenztests in einer temporären Kopie aus. Ohne GHDL
bleiben diese und ihre zwei fixtureabhängigen Hosttests `NOT_EXECUTED`.
Ein grüner Softwarelauf ersetzt weder Timing-Closure noch einen Hardwaretest.

## Was das Modell leistet

Ein gemeinsamer latenter Ornstein-Uhlenbeck-Prozess wirkt auf Dämpfung,
Polarisationsrotation und Laufzeit beider Arme. Aus derselben Poisson-Paarquelle
entstehen Messausgänge, Verluste, Dunkelzählungen, Totzeitverluste und Zeitstempel.
Getrennte Zufallsströme machen Simulation und Kalibrierung reproduzierbar.
Eine affine Zeitkorrektur wird an eigenen synthetischen Referenzpulsen angepasst
und an zurückgehaltenen Pulsen geprüft.

Die Auswertung zählt alle 16 Belegungsmasken, leere Fenster, Wiederholungen und
Mehrportereignisse. Sie führt keine Hintergrundsubtraktion durch. Numerische
Verschränkungsgrößen stammen aus bekannten Modellzuständen, nicht aus einer
behaupteten Rekonstruktion weniger Klickzahlen.

Das Modell erlaubt einen konkreten Test einer gemeinsamen Fehlerkette:
Wenn Dämpfung und Polarisationsdrift korrelieren, kann die beobachtete Teilmenge
andere Zustände gewichten als das Zeitmittel des Kanals. Uhrfehler verändern
zusätzlich, welche Ereignisse in dasselbe Auswertefenster fallen.

## Grenzen und Lizenz

Die Konfigurationen sind **synthetische Entwurfsannahmen**, keine gemessenen
Gerätespezifikationen. Zeitstempel in ps und ein angenommener Quantisierungsschritt
belegen keine entsprechende reale Genauigkeit. Kalibrierung ist offline und setzt
genau bekannte Referenzzeiten auf demselben modellierten Pfad voraus.

Nicht implementiert sind unter anderem polarisationsabhängige Verluste,
Polarisationsmodendispersion, spektrale SPDC-Dynamik, Nachpulse, Trojanerangriffe,
aktive Polarisationsregelung, White-Rabbit-Anbindung, Quantenspeicher und ein
vollständiges QKD-Protokoll. Die Forschungstore definieren, wann diese Grenzen
experimentell relevant werden und erweitert werden müssen.

Eigene neue Beiträge: Apache-2.0 gemäß [Repository-Lizenz](../../LICENSE).
Sagnac-Komponenten behalten MIT; der NQK-Snapshot enthält seine Apache-Lizenz
und NOTICE. Literatur wird referenziert, nicht als eigener Inhalt übernommen.
