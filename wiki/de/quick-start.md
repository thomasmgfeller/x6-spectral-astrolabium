# Schnellstart: dein erster Versuch

Beginne im Browser. Die lokale Installation ist ein eigener, optionaler Weg für reproduzierbare Rechenläufe.

[English](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/quick-start.md) · [Wiki-Übersicht](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/)

Quellenstand: 2026-10-18 · `01430ce5f0a648ad63d611a451f0d0fd7ccb16aa`

## In fünf Minuten im Signal Lab

1. Öffne das Signal Validation Lab und wähle bei Bedarf Deutsch.
2. Übernimm die Standardwerte und klicke auf „Test ausführen“.
3. Vergleiche Identität, gleitenden Mittelwert, FFT-Tiefpass und X6-Phasenfilter. Sie verwenden denselben Eingang.
4. Betrachte Referenz und Ausgabe gemeinsam. Lies anschließend den Fehlerwert und die einzelnen Kriterien.
5. Ändere nur die Rauschstärke und führe erneut aus. So bleibt erkennbar, welche Änderung welchen Effekt hatte.
6. Wähle „Gegenbeispiele prüfen“. Ein bestandener Gegenbeispielfall bedeutet, dass der erwartete Fehler erkannt wurde.
7. Exportiere den JSON-Prüfbericht. Importiere ihn anschließend über „JSON-Prüfbericht wiederholen“ und lasse ihn neu berechnen.

Das Ergebnis muss nicht überall PASS zeigen. Auch ein korrekt ausgeführter Versuch kann zeigen, dass ein Filter das Signal verschlechtert. JSON bewahrt den vollständigen Prüfbericht; CSV enthält Zeitreihen zur weiteren Auswertung.

- [Signal Validation Lab öffnen](https://thomasmgfeller.github.io/x6-spectral-astrolabium/app/signal-lab.html)
- [Ausführliche Bedienung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/SIGNAL_VALIDATION_LAB.md)

## Lokal starten

Der dokumentierte lokale Prüfweg verwendet Linux/POSIX auf x86-64, Python 3.12, Git und Node.js ab Version 22. Andere Plattformen sind durch diesen Prüfbericht nicht automatisch mitabgedeckt. Führe die Befehle in einem neuen Projektordner aus.

```sh
git clone --branch main https://github.com/thomasmgfeller/x6-spectral-astrolabium.git x6-wiki-start
cd x6-wiki-start
python3 x6.py setup --profile research
python3 x6.py doctor --profile research
python3 x6.py serve
```

Öffne die ausgegebene lokale Adresse. Strg+C beendet den Server. Bei belegtem Port: python3 x6.py serve --port 8001. Für eine exakt gleiche Wiederholung verwende den Quellencommit aus dem betreffenden Modulbericht; main entwickelt sich weiter.

- [Installations- und Integrationsanleitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md)

## Einen Lauf ausführen und prüfen

```sh
python3 x6.py run signal --output runs/wiki-signal-001
python3 x6.py verify runs/wiki-signal-001
python3 x6.py export runs/wiki-signal-001 --output exports/wiki-signal-001.zip
python3 x6.py verify exports/wiki-signal-001.zip
```

Benutze für den nächsten Lauf einen neuen Ausgabenamen. verify prüft nicht nur Prüfsummen, sondern berechnet die vorgesehenen Ergebnisse erneut. Das erfolgreiche Exportieren ändert das fachliche Urteil über den Filter nicht.

Für den Einstieg ist keine neue Wolfram-Abfrage und kein Messgerät erforderlich. Die separat dokumentierte Offline-Referenzsuite verwendet Python 3.12 und Node.js 24.

- [Offline-Referenzsuite](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/OFFLINE_REFERENCE.md)
