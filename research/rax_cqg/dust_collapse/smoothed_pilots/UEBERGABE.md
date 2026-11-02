# Zwei freiwillige Probeläufe auf eigener Rechenzeit

Gesucht ist eine Forschungsgruppe oder eine freiwillige Person mit eigener, bereits verfügbarer und für dieses Projekt nutzbarer CPU-Rechenzeit. Übernommen werden zunächst genau zwei vollständige Hochdichteordnungen am homogenen Staubball, eine pro Zeitfenster. Der Beitrag ist für den Projekteigner kostenfrei. Die übernehmende Seite trägt Rechenzeit, Betrieb und einen etwaigen Abbruch selbst. Vor dem Start bestätigt sie diese Übernahme. Das Paket verlangt keine Zugangsdaten des Projekteigners.

## Auftrag

| Lauf | Dichte je Einheit Vierervolumen | Vergangenheit | Zukunft | Zufallsstartwert | grober Aufwand |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 6 000 000 | 0,11 | 0,24 | 20261102921 | 16 CPU-Stunden |
| B | 6 000 000 | 0,24 | 0,11 | 20261102922 | 27 CPU-Stunden |

Diese Richtwerte kommen aus je 32 nach Zeit geschichteten Endpunkten auf einem einzelnen CPU-Kern. Reale Laufzeiten hängen vom Rechner ab. Die effektive Glättungsdichte ist 600 000. Der Generator bildet alle möglichen Vorfahren der Einheitskugel im räumlich unbeschränkten Raum ab. Der grössere der beiden Läufe enthält im Mittel rund 2,8 Millionen Ereignisse. Beide Läufe sind unabhängig und können auf verschiedenen Rechnern ausgeführt werden.

## So führt eine übernehmende Gruppe die Läufe aus

1. ZIP entpacken, ins entpackte Verzeichnis wechseln und die Prüfsummen mit `sha256sum -c SHA256SUMS` überprüfen. Die getesteten Softwareversionen stehen in der README. Erforderlich sind Linux, Python mit NumPy und SciPy sowie ein C++17-Compiler mit OpenMP-SIMD-Unterstützung.
2. Im eigenen Rechenkontingent den Kern bauen und die kurzen nichtperiodischen Kontrollfälle prüfen. Diese Gegenrechnung vergleicht das Produktionsverfahren mit expliziten Zwischenmengen. Bei einer fehlgeschlagenen Prüfung zuerst die Ursache klären.
3. Die beiden einmaligen Befehle unten getrennt ausführen und alle Ergebnisse zurückgeben, einschliesslich Fehlschlägen. Ein erneuter Versuch nach einem technischen Abbruch nutzt denselben Startwert. Eine Wiederholung wird als derselbe Lauf gezählt.

```sh
export OPENBLAS_NUM_THREADS=1
python3 -c 'import full_run; full_run.compile_kernel()'
python3 halo_reference.py
python3 halo_reference.py --one 20261102921 --window 0 --density 6000000 > pilot_A.json
python3 halo_reference.py --one 20261102922 --window 1 --density 6000000 > pilot_B.json
```

**Erbetene Rückgabe**  
Beide JSON-Dateien, die Datei `halo_checks.csv` sowie die CPU-Bezeichnung und die Ausgaben von `g++ --version` und `python3 -m pip show numpy scipy`. Bei einem Abbruch genügen Laufkennung, Fehlermeldung und erreichte Laufzeit. Jede Ergebnisdatei enthält die normierte geglättete und lokale Masse, die deterministische Abschneidefehlerschranke, Punktzahlen, Zufallsstartwert und CPU-Zeit. Ein Treffer gilt als numerisch gesichert, wenn das gesamte Intervall aus geglättetem Wert plus/minus Fehlerschranke in [0,9, 1,1] liegt.

Die beiden Einzelwerte prüfen Übertragbarkeit, Rechenaufwand und Grössenordnung. Für eine Entscheidung über eine Trefferwahrscheinlichkeit von mindestens 95 % wäre eine eigene vorab geplante Kohorte erforderlich. Dieses Übergabepaket löst weder eine automatische Berechnung noch die Bestellung weiterer Rechenzeit aus.

## Text für eine freiwillige Übernahme

Kann eure Gruppe zwei unabhängige CPU-Läufe zur Einzelmasse eines diskretisierten homogenen Staubballs auf bereits verfügbarer eigener Rechenzeit übernehmen? Zusammen sind ungefähr 43 CPU-Stunden veranschlagt. Wir stellen geprüften Python-/C++-Code, feste Startwerte, Referenzwerte und ein Rückgabeformat bereit. Voraussetzung ist eine unentgeltliche Durchführung ohne Weiterberechnung an den Projekteigner. Als Ergebnis genügen zwei JSON-Dateien, der Kontrolllauf und Angaben zur Rechnerumgebung.

Eine europäische Hochschulgruppe kann prüfen, ob sie bereits passende Rechenzeit besitzt oder ob ihr Projekt die Bedingungen eines EuroHPC-Zugangs erfüllt. Über Zulassung und Zuteilung entscheidet die jeweilige Einrichtung. [EuroHPC-Zugangsbedingungen](https://www.eurohpc-ju.europa.eu/supercomputers/supercomputers-access-policy-and-faq_en)
