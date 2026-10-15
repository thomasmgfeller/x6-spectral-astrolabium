# RAX-G1: geschützter deklarativer Runner und Fehlerbudget

**Technische Qualifikation, keine neue RAX-B1-/U2-Leistungskampagne.** Der neue
Runner schließt die konkreten M1-Zugriffswege für sein ausdrücklich begrenztes
Planerformat. Alle historischen B1-/M1-Archive bleiben bytegleich.

## Zugelassene Planer und Vertrauensgrenze

Planer sind streng geprüfte JSON-Daten: eine feste Aktion, die eingebaute
Informationsgewinnregel oder eine endliche Verzweigung über eine **bereits
freigegebene** Beobachtung. Alle Zweige werden vor der Ausführung geprüft,
auch nicht erreichte. Indexbereiche/-typen, Aktionsbereich, Budget, Tiefe,
Eingabegröße und unbekannte Felder werden begrenzt. Negative Indizes und
boolesche Zahlen-Aliase sind ungültig. Es gibt keine frei programmierbaren
Ausdrücke, Imports, Dateipfade, URLs, `eval`, Plugins oder Python-Callbacks.

Ein vertrauenswürdiger Broker hält die Potentialdaten. Jede Aktionsentscheidung
läuft in einem frischen Python-Prozess mit `-I -S -B`, leerem Arbeitsordner,
bereinigter Umgebung, geschlossenen zusätzlichen Deskriptoren und drei Sekunden
Timeout. Übergeben werden nur öffentliches Modell, deklarativer Plan,
Messbudget und bisherige `(Aktion, Beobachtung)`-Paare. Eine Antwort kann genau
eine zulässige Aktion anfordern. Posterior und Vorhersagen berechnet der Broker.

**Die Schutzgrenze ist die endliche Sprache samt vertrauenswürdigem Interpreter.**
Prozesstrennung allein ist keine allgemeine Python-Sandbox. Fremde ausführbare
Planer werden nicht zugelassen. Kein Schutz wird gegen einen manipulierten
Broker/Interpreter, Kernel-Angriffe, privilegierte Mitleser, externe Kollusion
oder einen Menschen behauptet, der bekannte Prüfantworten in einen festen Plan
kodiert. Für beliebigen fremden Python-Code bleibt eine separat qualifizierte
OS-/Container-Isolation offen. Ein lokaler Namespace-Versuch war hier gesperrt;
es wird dafür kein bestandener Sandbox-Test behauptet.

## Phasen und prüfbarer Umfang

1. Vollständigen Vertrag und sämtliche Planer prüfen; neues Ausgabeverzeichnis
   anlegen. Bestehende Verzeichnisse werden abgelehnt.
2. Quellen, Vertrag und Commitments der beiden getrennten Zufallsseeds fixieren.
3. Messungen über den Broker ausgeben, Budget verbuchen und alle Vorhersagen
   dauerhaft schreiben, bevor Prüfbeobachtungen erzeugt werden.
4. Holdout erzeugen, danach Seeds zur Reproduktion offenlegen. Bewertung und
   abschließendes vollständiges Dateiinventar schreiben.
5. Beim Replay alle Quellenbindungen, Datengenerierung, Aktionen, exakten
   rationalen Vorhersagen und Berichtszellen erneut berechnen. Neu gehashte
   Fälschungen reichen nicht aus. JSON-Vergleich unterscheidet `true` und `1`.

Die Commitments und Dateireihenfolge bescheinigen lokale Programmordnung,
keine externe Präregistrierung oder vergangene menschliche Blindheit. Ein
Abbruch lässt einen unvollständigen Ordner zurück, der beim Replay scheitert.
Ein einzelnes `fsync` ist kein nachgewiesener Stromausfall-/Dateisystemschutz.

Der enthaltene Kontrollvertrag hat drei Mechanismen mit Wahrscheinlichkeiten
`(3/4,1/2)`, `(1/2,3/4)`, `(1/2,1/2)`, sechs Episoden, drei Planer, Budget vier
und acht Prüfbeobachtungen je Aktion. Alle 18 Zellen müssen vorliegen. Die
Brier-Werte sind beschreibende synthetische Funktionskontrollen ohne
Überlegenheitsprüfung. Die Zufallswerte sind deterministische SHA-256-basierte
Pseudodaten nach Offenlegung der Seeds; keine physischen Zufallsnachweise.

## Ausführen

Nur Python 3.12, Standardbibliothek; neue Zielpfade:

```sh
python3 -S -B tests/rax-guarded/qualify.py --output /tmp/rax-g1-qualification
python3 -S -B experimental/rax_guarded/runner.py run --output /tmp/rax-g1-new
python3 -S -B experimental/rax_guarded/runner.py verify /tmp/rax-g1-new
```

Qualifikation: `PASS`, **33 erwartete Zurückweisungen**; Replay:
`PASS_GUARDED_REPLAY`, 18 Zellen. Fehler: Exitcode ungleich null. Ein neuer Lauf
hat neue Seeds und darf andere Scores erzeugen; der Replay desselben Laufs muss
exakt übereinstimmen. [Gespeicherte Qualifikation](evidence/guarded/qualification.json).

Die Isolationstests verändern die tatsächlich verwendeten zukünftigen
Akquisitionswerte und Holdout-Antworten. Aktionen vor Freigabe veränderter
Beobachtungen bleiben gleich; spätere Beobachtungen beziehungsweise Scores
müssen sich ändern. Ein absichtlich holdoutabhängiger Kontrollplaner wird durch
den Vergleich zweier Datenwelten erkannt. Produktionsplaner mit Holdout-,
Zukunfts-, Callback-, Datei- oder Netzzugriff werden bereits syntaktisch verworfen.
Ein unabhängiges kleines Rechenbeispiel liefert exakt `13/24` für beide
Vorhersagen des festen Plans nach vier Nullbeobachtungen.

## Dauerhaftes Fehlerbudget

[ERROR_BUDGET.json](ERROR_BUDGET.json) bindet die M1-Befunde an neue Regressionen,
nennt verbleibende Grenzen und führt neue Befunde als Historie. Für angenommene
unzulässige Zugriffe, fehlende/zusätzliche Zellen, und still akzeptierte
Ergebnisfälschungen ist das Budget **null**. Unentschiedene wissenschaftliche
Ergebnisse und erwartete Zurückweisungen sind keine Softwarefehler.

Neue Kampagnen dürfen nur im qualifizierten deklarativen Profil starten.
Jeder nicht erwartete Fehler blockiert die Freigabe; nicht durch Wiederholung
wegzählen oder als statistische Fehlalarmtoleranz behandeln. Neue Befunde erhalten
ID, betroffene Revision, Ursache, Wirkung und Regression. Alte Einträge werden
nicht gelöscht; Änderungen sind über Git nachvollziehbar. `check_budget.py`
prüft die Nullgrenzen und die Zuordnung tatsächlich bestandener Kontrollen.
Die CI prüft zusätzlich, dass bereits geführte Befund-IDs erhalten bleiben.

Externe personelle Wiederholung: **NOT_PERFORMED**. Der dokumentierte Übergabeweg
steht in [EXTERNAL_REPRODUCTION.md](EXTERNAL_REPRODUCTION.md). Die acht historischen
B1-Entscheidungen bleiben unentschieden; die Lorentz-Priorität und die bestehende
n=6-Gegenprüfung werden durch diese technische Härtung nicht verändert.
