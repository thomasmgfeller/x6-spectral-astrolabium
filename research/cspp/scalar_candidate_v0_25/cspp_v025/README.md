# CSPP v0.25 - Skalarer Kandidat und Zweiskalen-Ausschluss

Der nach v0.24 vorgesehene erste Kandidatenschritt ist mit einem begründeten
negativen Ergebnis abgeschlossen. Ein normierter fünflagiger Kandidat wurde
definiert; der erweiterte Kontrolltest schliesst sogar seine gesamte
eindimensionale Koeffizientenfamilie bei festem q0 aus.

- Konkreter Kandidat theta=21: alter Gauß-Zeuge L=2 mit 0.153 % Mittelwertfehler;
  zusätzliche Skalenkontrolle L=4 mit 84.65 %.
- Für alle reellen theta: mindestens 28.4732 % Fehler in einem der zwei
  Mittelwertkontrollen. Das 10-%-Ziel ist für diese Familie unerreichbar.
- Retardierung, korrekte IR-Normierung und eindeutige finite History-Lösung
  sind nachgewiesen. Uniforme und unendliche Propagatorstabilität sind offen.
- Kompakte Detektorproduktion und volle Spektralsuche: NOT_RUN_EARLY_ABORT.
- METHOD / G1: HOLD. Keine frischen Wolken, keine Bestätigungsstudie.

Das ist keine Widerlegung aller skalaren Operatoren und keine numerische
Fehlerbilanz des kompakten Detektors. L=4 ist ein neuer Entwicklungszeuge;
die physikalische Quelle und die alten statistischen Ziele bleiben gleich.

## Dateien

- PROTOCOL.json: Kandidat, Parameter, Eingabeabbildung und Abbruchregel.
- PROOF.md: vollständige Herleitung und Einschränkungen.
- run.py: rationale IR-Identitäten, Arb/Acb-Zertifikate und finite Kontrollen.
- verify.py: Herkunft, Präzisionsvergleich, alte Referenzen, unabhängige Koordinatenquadratur.
- reproduce.py: isolierter Replay; evidence/ bleibt unverändert.
- results/: vollständige einschliessende Zahlen und Nachweise.
- report/: kompakter deutschsprachiger PDF-Bericht.

## Reproduktion

Python 3.12.14; python-flint 0.8.0; SciPy 1.17.0.

```bash
python3 -m pip install -r requirements.txt
python3 reproduce.py
```

Nur Prüfungen: `python3 reproduce.py --quick`.
Neue numerische Dateien: `python3 run.py --bits 128` und `--bits 192`.
PDF: `python3 build_report.py` (erfordert die im Skript verwendeten DejaVu-Schriften).
Bytevergleich gilt für die dokumentierte Laufzeit; andere Python-Versionen
ändern die in den JSON-Dateien enthaltenen Metadaten.

Die Entwicklung enthielt explorative Gleitkommarechnungen vor der
Kandidatenwahl. Keine Vorregistrierung oder externe Reproduktion wird behauptet.
Basis ist der unveränderte Main-Commit 4c755221b76364c02beca5e7a40c0f8d50931375.
Das Paket ist zur Prüfung und späteren Publikation vorbereitet.
