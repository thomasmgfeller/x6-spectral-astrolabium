# Ergebnisse der synthetischen Referenzläufe

Alle Werte in dieser Datei sind **Simulationsergebnisse**, keine Messungen an
einer eigenen Quelle oder Faser. Die volle Parametrisierung, Seeds und
Softwarehashes stehen in `evidence/experiments.json`; die Ergebnisse lassen sich
mit `python experiments.py --output <neuer_pfad>` neu erzeugen.

## Verifikation der Implementierung

- 38 neue Modell-, Schnittstellen- und CLI-Tests: bestanden.
- 28 geerbte GHDL-Fälle: bestanden, einschließlich erwarteter Fehler-/Timeoutfälle.
- 17 geerbte Hosttests: bestanden, nach Erzeugung der benötigten RTL-Fixtures.
- Byteidentität der übernommenen Dateien: geprüft gegen das Herkunftsmanifest.

Diese Zahlen bezeichnen Testfälle unterschiedlicher Art. Sie werden nicht zu
einem wissenschaftlichen Gütescore addiert. NQK liefert eine alternative
numerische Implementierung innerhalb desselben Projektumfelds; die analytischen
Spezialfälle und die separate Fenster-Quadratur liefern weitere Referenzen.
Eine Replikation durch eine unabhängige Forschungsgruppe liegt nicht vor.

## Vier festgelegte Szenarien

Jeweils T=0,1 s, W=2 ns, 30 Wiederholungen mit Seeds 2000–2029. Die Tabelle
zeigt arithmetische Mittel pro Lauf. Standardfehler beziehen sich auf den
Mittelwert über diese unabhängigen Modellrealisierungen. Sie umfassen keine
Unsicherheit unbekannter Geräteparameter und sind keine Sicherheitsgrenzen.

| Szenario | Bedingte Portfenster nach Korrektur, Mittel ± Standardfehler | Gleichportige Fraktion, Mittel | Zeitbudget eingehalten |
|---|---:|---:|---:|
| Konstante Baseline | 2431,1 ± 9,1 | 1,046 % | 30/30 |
| Zusätzlicher Offset/Skew, geringe Krümmung | 2431,9 ± 8,7 | 1,043 % | 30/30 |
| Gemeinsame Verlust-, Polarisations- und Laufzeitdrift | 580,2 ± 18,8 | 12,179 % | 20/30 |
| Starke nichtlineare Uhrdrift | 192,1 ± 2,3 | 1,380 % | 0/30 |

Die gekoppelte Konfiguration hat zusätzlich eine höhere angenommene
Einfügedämpfung als die Baseline. Der Unterschied der Zählraten isoliert daher
**nicht** den kausalen Beitrag der gemeinsamen Drift. Zur isolierten Prüfung
werden gezielte Kontrollen in den Tests und das paarige Studienprotokoll in
`RESEARCH_PROGRAM.md` verwendet. Die vier Szenarien sind Illustrationen,
kein optimierter Benchmark eines neuen Verfahrens.

Im Offset-/Skewszenario stellt die Offline-Kalibrierung unter ihren Annahmen
nahezu die Baselinezählung wieder her. Das ist kein Nachweis, dass reale
White-Rabbit-Hardware oder unbekannte Referenzpfade dieselbe Leistung erreichen.
Die starke nichtlineare Uhr zeigt einen Gegenfall: Mehr Koinzidenzen nach
Korrektur allein reichen nicht aus, um eine Kalibrierung freizugeben.

Bei gekoppelter Drift überschreiten 10 von 30 Läufen das synthetische Zeitbudget;
sie bleiben vollständig im Bericht und in den Mittelwerten enthalten. Es erfolgt
keine nachträgliche Auswahl bestandener Läufe. Der Bericht zeigt auch, dass
die Negativität des Zeitmittelzustands von der mittleren instantanen Negativität
abweichen kann. Diese Größen werden aus bekannten Simulationsmatrizen berechnet.

## Offene Evidenz

Vor Hardwarevorhersagen fehlen insbesondere reale Parameterkalibrierungen,
Kontrollen für PDL/PMD/Nachpulse, eine OU-Diskretisierungsstudie für den konkreten
Einsatz und eine Prüfung auf getrennten Messtagen. Der deterministische
Driftanteil besitzt eine getestete Konvergenzprüfung; daraus folgt keine
universelle Genauigkeitsgarantie für beliebige stochastische Pfade.

Die erste Ausführung der geerbten Hosttests ohne RTL-Fixtures meldete zwei
fehlende Dateien. Nach tatsächlicher GHDL-Erzeugung in einer temporären Kopie
bestanden alle 17 Tests. Die fehlenden Dateien wurden weder ignoriert noch
durch angeblich gemessene Daten ersetzt. Maßgeblich ist der abschließende
gespeicherte Prüfbericht mit seiner genauen Quellinventur.
