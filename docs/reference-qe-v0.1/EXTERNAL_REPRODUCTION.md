# Externe Wiederholung: eingefrorene Referenzedition 2026-10-15 / QE v0.1

**Status: Noch keine außenstehende Person hat eine Wiederholung eingereicht.**
Lokale Läufe und GitHub CI stammen aus demselben Projekt. Ein Werkzeug kann die
Übereinstimmung von Ergebnissen prüfen, aber keine personelle Unabhängigkeit
beweisen. Das Verfahren fordert keine Zustimmung zu Forschungsbehauptungen.

## Übergabe ohne Gesprächshistorie

1. Von der [Referenzfreigabe](https://github.com/thomasmgfeller/x6-spectral-astrolabium/releases/tag/reference-2026.10.15-qe1)
   `x6-reference-2026.10.15-qe1.zip`, `x6-reference-qualification.zip` und
   `SHA256SUMS` herunterladen.
   `sha256sum -c SHA256SUMS` ausführen. Quellcommit und Dateiinventar stehen nach
   dem Entpacken in `x6-reference/RELEASE_BUNDLE.json`. Der äußere Hash ist ein
   Inhaltsabgleich; GitHub/Checkout bleiben die Vertrauensquelle.
2. Linux/POSIX x86-64, Python **3.12** und Node.js **24** bereitstellen. Keine
   pip-Pakete, Wolfram-Anmeldung, Geräte oder weiteren Daten nötig. Der Ablauf
   arbeitet nach dem Download offline. Zielordner muss neu sein.
3. Paket entpacken und ausschließlich anhand dieser Anleitung ausführen:

```sh
python3 -m zipfile -e x6-reference-2026.10.15-qe1.zip /tmp/x6-reference-unpacked
cd /tmp/x6-reference-unpacked/x6-reference
python3 -S -B tools/release/reproduce.py --output /tmp/x6-external-result
```

Erwartung: Exit **0**, `PASS_REFERENCE_REPRODUCTION`; zehn Referenzberichte,
27 übergreifende, 17 Lorentz-interne und 21 QE-interne Fehlerkontrollen, 33 Zurückweisungen des
neuen RAX-Runners, Fehlerbudgetprüfung und drei Archivprüfungen. Exakte Werte
und berichtsweise SHA-256-Erwartungen stehen in `expected-reference.json`.
Das n=6-Ergebnis bleibt: vier Restpaare getrennt, n=7/n=8-Gültigkeitsgrenzen
explizit dokumentiert. Keine Fortsetzung auf ungetestete Größen.

Der Lauf schreibt **REPRODUCTION.json**, alle Standardausgaben/Fehlerlogs,
Referenzberichte und RAX-Ergebnisse. Er führt keinen Code aus dem Ergebnisordner
aus. Runtime-Versionen, OS und sämtliche Ergebnisdateihashes werden erfasst.
Andere Patchstände/Architekturen können letzte Gleitkommabits unterscheiden.
Solche Abweichungen führen zu `FAIL` mit Dateinamen und beiden Hashes; die
Rohresultate bleiben erhalten. Keine Referenzwerte an die Abweichung anpassen.

Neue RAX-Kontrollläufe erhalten neue Seeds: deren Brier-Werte dürfen abweichen.
Jeder einzelne Lauf muss aus seinen offengelegten Seeds exakt nachrechenbar
sein; seine 33 Angriffstests müssen bestehen. Die zehn eingefrorenen
wissenschaftlichen Referenzberichte werden dagegen gegen feste Werte geprüft.

## Rückgabe und Abnahme

Die ausführende Person ergänzt eine Kopie von `../validation-v1/external-report.template.json`:
öffentlich verwendbarer Name/Kennung, Verhältnis zum Projekt, ob sie den Code
mitentwickelt hat, Datum, Bundle-Hash, Quellcommit, benutzte Befehle, benötigte
Hilfestellung und sämtliche Abweichungen. Keine private Adresse erforderlich.
Ergebnisse samt vollständigem `REPRODUCTION.json` und Logs über einen selbst
angelegten GitHub-Issue/PR oder einen vereinbarten Dateikanal zurückgeben.
Die Issue-Vorlage „External reference reproduction“ enthält dieselben Felder.

Annahme erst nach: (a) Quellen-/Bundleidentität geprüft; (b) Ergebnisinventar
vollständig; (c) Referenzresultate erneut gegen den eingefrorenen Stand geprüft;
(d) Abweichungen erklärt oder als offen registriert; (e) personelle Rolle und
Hilfestellung transparent bewertet. Ein zweiter interner Agent oder CI-Lauf
schließt `EXT-1` nicht. Die unabhängige Person muss tatsächlich selbst ausführen.
Das Projekt führt ungeklärte Abweichungen im Fehlerbudget weiter.

Der kleine Umfang ist bewusst auf vorhandene endliche Referenzen begrenzt.
Die komplette B1-Kampagne, der industrielle Leistungsvergleich und physische
ACVM-/Sagnac-Abnahmen gehören nicht zu dieser Referenzfreigabe.

X6-QE ergänzt vier Graphen in drei bekannten Referenzfällen: K1,6, C4,
Turmgraph/Shrikhande. Kein Billiard-, Gedächtnis- oder Primzahlbefund folgt daraus.
Die ursprüngliche Referenzedition und ihre Ergebnisse bleiben unverändert.
