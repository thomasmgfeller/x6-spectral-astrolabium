# Kontinuierlicher Vier-Element-Sektor v0.1

Arbeitspaket vom 7. November 2026. Basis ist Main nach PR 256,
Commit `e4787d04c78a1da43825dbbac670a0e3dfacee51`.

## Ergebnis und Geltungsbereich

Alle 40 natürlich beschrifteten Vier-Element-Ordnungen sind im geerbten
Referenzmaß integriert. Gegenüber dem Drei-Element-Stand beginnt der
unbekannte Phasenrest jetzt bei n=5. Seine obere Gewichtsschranke sinkt
je nach Uhrhorizont und Zahlgewicht um weitere **93,59 bis 99,05 Prozent**.
Dies ist eine Verbesserung einer oberen Schranke, keine Messung der
tatsächlichen Wahrscheinlichkeit höherer Elementzahlen.

Die Rechnung umfasst 240 Geometrieamplituden und 36 kombinierte Parameterfälle.
Alle 36 neuen Zahlkanal-Erfolgsintervalle liegen innerhalb ihrer Vorgänger.
Der maximale Quadraturrest ist kleiner als `1.041e-9`, der maximale
Arithmetik-/Funktionsrest kleiner als `1.841e-12`. Das vorab festgelegte
Gesamtziel `1e-8` je Geometrieamplitude wird erfüllt. Diese Fehlergrenzen
sind nicht der Gesamtfehler der unbegrenzten Elementzahlsumme.

Die Dichtemarken werden analytisch integriert. Positive Gauß-Legendre-
Quadratur mit rationalen Ableitungsgrenzen kontrolliert die geordneten
Uhrintegrale. Ein neuer C++17-Kern verwendet nach außen gerundete Intervalle
mit 60 Nachkommabits und geprüften signierten 128-Bit-Ganzzahloperationen.
Knoten, Gewichte und π werden aus den geerbten 160-Bit-Einschließungen nach
außen konvertiert. Sinus, Kosinus und Dichtefunktion besitzen explizite
Taylorreste; im zertifizierten Integralkern wird keine libm-Näherung verwendet.
Die 60 Nachkommabits sind kein Anspruch auf 60 korrekte Ergebnisbits.

Der Kostenplan wurde nach analytischer Aufwandsabschätzung, aber vor der
neuen Implementierung und den neuen n=4-Integralwerten lokal eingefroren.
Keine externe Präregistrierung oder blinde Vorhersage wird behauptet.
Die teuerste Konfiguration benötigt 1 172 864 Tensorpunkte, unter dem
festgelegten Limit von 1 200 000. Gemeinsame Auswertung von 24 verschiedenen
Dichtepolynomen begrenzt den gesamten n=4-Scan auf 31 343 616 χ-Aufrufe
gegenüber einem Budget von 35 000 000. Pro nativer Konfiguration gilt ein
erzwungenes Zeitlimit von 600 Sekunden. Es wurde kein bezahlter Rechendienst
verwendet.

**MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und
EXTENSION bleiben HOLD.** Das Dichtemaß, kohärenter Zugriff auf vollständige
Historien und die Endrandwahl bleiben Annahmen. Ein physikalischer Detektor,
eine vollständige vierdimensionale CST-Dynamik, gravitative Rückwirkung,
ein Bounce oder ein Innen-/Außenraumanschluss werden nicht hergeleitet.
Feldphasen ab n=5 und ein unendlicher Zeithorizont bleiben unausgewertet.

## Artefakte

- [Bericht (PDF)](../reports/CST_DUST_Vier_Elemente_Kontinuierliche_Materiephase_v0_1.pdf)
- [Originales Prüfpaket (ZIP)](../packages/CST_DUST_Vier_Elemente_Kontinuierliche_Materiephase_v0_1_Pruefpaket.zip)
- [Vollständige Herleitung](DERIVATION.md)
- [Maschinenlesbarer Vertrag](four_element_contract.json)
- [Nachrechnung und Nutzung](README.md)
- [Ergebnisstatus](results/verification.json)
- [Restgrenzen und Intervallverbesserung](results/tail_reduction.json)
- [Kosten-, Quadratur- und Arithmetikzertifikate](results/quadrature_certificates.json)

## Verifikation

Zwei Enumerationswege liefern dieselben 40 natürlichen Ordnungen.
32 400 rationale Kontrollen prüfen vollständige Wirkung und Inkremente;
320 niedrige Momente stimmen auf geordneter Uhrdomäne und Würfel exakt überein.
168 rationale Rechenkontrollen, 52 punktweise Einschließungen der
160-Bit-Referenz und ein absichtlich zurückgewiesener Überlauf prüfen den
nativen Kern. Alle 28 nichttrivialen n=3-Geometrieamplituden werden innerhalb
der Summe beider Fehlergrenzen bestätigt.

Die zusätzliche Negativkontrolle erkennt einen normierungserhaltenden
Jacobianfehler: Bei der Vier-Element-Antikette und h=1/2 würde der erste
Materiemoment `-101/162` statt `-5/6` betragen. Die Norm allein bliebe eins.

Sechs Ergebnisdateien wurden in einem frischen Verzeichnis bytegleich
reproduziert. Der Replay kompiliert den Kern erneut und berechnet alle
neuen Integrale ohne neue Ergebnis-Caches. Dies ist interne Wiederholbarkeit,
keine externe Replikation und keine formale Verifikation des Compilers oder
der gesamten Implementierung.

Vom Repository-Stamm, mit Python 3.12 und g++ mit C++17, `__int128` und
geprüften Überlauf-Builtins; keine zusätzlichen C++-Bibliotheken:

```bash
python3 -O -B research/rax_cqg/dust_collapse/four_element_matter_v0_1/publication_check.py --replay
```

Der Prüfer kontrolliert das unveränderte Originalarchiv, alle 37 Mitglieder,
36 Manifest-Prüfsummen, beide PDF-Kopien, den eingefrorenen Plan, zwölf
bytegleiche Repositoryquellen sowie Kosten, Fehlergrenzen und Aussageumfang.
Der Workflow `cst-dust-four-element-matter.yml` führt Integrität und Replay
auf Pull Requests und Main aus. ReportLab und DejaVu Sans werden nur zum
optionalen Neubau des Berichts benötigt, nicht für die wissenschaftliche
Nachrechnung oder die CI-Prüfung.

| Objekt | SHA-256 |
|---|---|
| Original ZIP | `d26fdd01ffdb121e3372a8971146366794b99741d6c588e9e70f3c69e68416d2` |
| PDF | `e35a7201a66d7301808acdd6fcce4207e3cde98d5a6822a58c8e82839301c19d` |
| Plan | `89d0a80bc70a25f8cbf06b68b32f391c9f7820b42f3741ec246e002bc89b033f` |

Alle Originaldateien bleiben unverändert. Publikationsnotiz, Repository-
Prüfer, CI und Index-/Integritätsdateien ergänzen das veröffentlichte Paket.

## Nächste wissenschaftliche Grenze

Für α=2 stammen etwa 81,85 % beziehungsweise 94,91 % der verbleibenden
oberen Restmasse aus der konservativen Normschranke für n>6. Diese Anteile
beziehen sich auf das Fehlerbudget, nicht auf die tatsächliche Verteilung.
Die geerbte Schranke nutzt nur α≥1. Ihre α-abhängige analytische Verbesserung
ist daher der nächste quantitative Kandidat vor weiteren Feldintegralen.
Die physikalische Begründung von Maß, kohärentem Historienzugriff und Randwahl
bleibt davon getrennt offen.
