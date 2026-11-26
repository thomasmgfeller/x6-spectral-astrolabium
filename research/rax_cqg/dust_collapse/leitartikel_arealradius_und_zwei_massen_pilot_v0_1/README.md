# Wann bestimmen endliche Kausaldaten den Radius eines Staubballs?

Arbeitsfassung 0.1 des CST-DUST-Leitartikels und Offline-Prüfung des frühen Zwei-Massen-Piloten. Ausgangspunkt ist das [auf GitHub veröffentlichte Exposé](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse/reports/CST_DUST_Flagship_Expose_und_Forschungsprioritaet.pdf). Die Referenzmodelle und der physische Prüfvertrag sind auf [Commit 7c45c6f](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/7c45c6fc7dce37a34505d1f91cddd9da6002fdfc/research/rax_cqg/dust_collapse) fixiert.

## Lesen und nachrechnen

Der Artikel liegt als `Leitartikel.pdf` und editierbar als `Leitartikel.md` vor. Das Archiv in einen Ordner entpacken und dort mit Python 3.11 oder neuer ausführen. Die Rechnung verwendet die Standardbibliothek und alle benötigten Eingaben liegen bei.

```sh
python3 -B pruefen.py
```

Das Programm prüft die Dateien anhand von SHA-256, berechnet die Ergebnisse erneut und vergleicht die Ausgabe byteweise mit `Ergebnisse.json`. Die Prüfung endet bei einer Abweichung mit einem Fehler. Ein erfolgreiches Ende bestätigt die aufgeführten Rechnungen.

## Gegenstand der Prüfung

| Rechnung | Ergebnis und Geltungsbereich |
|---|---|
| N15-Zeuge | Für die zwei kinematischen Geometrien mit identischen radialen Beobachtungen ist der scharfe relative Minimaxfehler 7/92. Die Rechnung liest die archivierten Radien ein und gleicht Schätzer und Fehler rational mit den veröffentlichten Werten ab. |
| Klassische Kontrolle | Eine unabhängige Anfangsladung und zwei benachbarte Schalen derselben LTB-Lösung liefern bei T* = 5√5/6 die Radiusintervalle [9,4669; 9,7002] für M = 1/4 und [8,1548; 8,3648] für M = 4. Gewährt sind vollständige radiale Abdeckung, radiale Ordnung und getrennte synthetische Eigenvolumen- und Eigendickenkanäle mit jeweils ±1 % um den Idealwert. |
| Direkte N19-Auslese | Auf dem geprüften positiven Viertelzweig gibt es genau zwei materielle Vierer-Antiketten. Unter drei Quellwerten und in allen sieben Driftzellen liegt die notwendige Halbbreite für die erste solche Gruppe zwischen 0,31677018633540372 und 0,31677018633540374 in der normierten Modelluhr um x = 1/2. Vier unvergleichbare Ereignisse sind nur eine notwendige Bedingung für das hier betrachtete direkte Dreiecksnetz. |
| Physischer P3-Pilot | Acht Zielwerte am gemeinsamen Schnitt (zwei Massen, vier Dichten) bleiben offen. Für dieselbe gekoppelte Historie fehlen ein unabhängiger Massenstandard mit Vakuumkontrolle, ein vollständiger materieller Rand mit geometrischer Flächenmessung sowie ein Fehlerbudget über die zulässigen Gewichte. Im Gesamtregister stehen alle 60 Einträge auf NOT_RUN. |

## Unterlagen

- `Pruefplan.md` hält die lokal vor der neuen Rechnung festgelegten Kriterien fest. `Ergaenzung.md` dokumentiert die spätere explorative Rückwegfrage. Beide haben eine separate Prüfsumme. Die klassischen Zielwerte waren bereits öffentlich.
- `klassische_kontrolle.py` führt die Massen-, Rand- und Radiusauslese der klassischen Kontrolle aus. `ereignisschnitt.py` zählt Antiketten und prüft Uhrgrenzen sowie die strikte Zukunft des Empfängers. `pruefen.py` verknüpft die Teilrechnungen mit dem P3-Register.
- `basis/` enthält die verwendeten publizierten Eingaben. `Quellen.json` ordnet jeder Datei ihren Repository-Pfad und ihren SHA-256-Wert zu. `SHA256SUMS` deckt die Paketdateien ab.

Die nächste offene Prüfung betrifft eine räumlich ausgedehnte geometrische Auslese auf derselben materiell geeichten Historie. Der Nachweis über vier direkte Eckereignisse lässt diesen Weg offen.
