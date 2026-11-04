# Freiwillige Staubball-Läufe A und B

Wer einen eigenen Linux-Rechner oder bereits bewilligte institutionelle Rechenzeit zur Verfügung stellen möchte, kann **einen** der beiden vollständigen Läufe übernehmen. Das Budget von Thomas Gfeller und dem Projekt beträgt **CHF 0**. Freiwillige stellen Rechner, Strom und Rechenzeit unentgeltlich bereit. Bitte zuerst im [öffentlichen Aufruf #192](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/192) die bisherigen Kommentare prüfen und beispielsweise schreiben «Ich übernehme Lauf A unentgeltlich auf eigener oder bereits bewilligter Hardware.» Den zweiten Lauf kann eine andere Person reservieren.

| Lauf | Zeitfenster vor / nach dem Schnitt | Fester Startwert | Geschätzte Dauer mit vier Threads | Zeit zum Einplanen |
| --- | --- | ---: | ---: | ---: |
| A · lange Zukunft | 0,11 / 0,24 | 20261102921 | 4 Std. 39 Min. | ca. 6 Std. |
| B · kurze Zukunft | 0,24 / 0,11 | 20261102922 | 5 Std. 13 Min. | ca. 7 Std. |

Die Hochrechnung beruht auf je 32 zeitlich verteilten Endpunkten des publizierten Laufzeitversuchs auf einer AMD-EPYC-VM. Hardware und Lastverteilung beeinflussen die tatsächliche Dauer. Die alten Richtwerte von 16 bzw. 27 CPU-Stunden beziehen sich auf die serielle Referenz. Die vollständigen Piloten messen bei der Eingangsdichte 6 000 000 und effektiven Dichte 600 000 je eine vollständige Kausalordnung. Die Stichprobe zur Laufzeitmessung dient allein der Aufwandsschätzung.

## Lokal starten

Vorausgesetzt werden vier verfügbare CPU-Threads, Linux, Bash, GNU coreutils, lscpu, unzip, GNU patch, g++ mit C++17 und OpenMP sowie Python 3 mit NumPy und SciPy. Getestet wurde mit Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 und GCC 13.3.0. Das Skript führt den gewählten Modus lokal aus und prüft beide ZIP-Dateien per SHA-256.

1. In einen neuen Ordner diese drei Dateien herunterladen. Die ZIP-Dateien gepackt lassen. [run.sh](run.sh) · [Staubball-Modell und Referenzdaten](../packages/CST_Staubkollaps_Geglaetteter_Massestrom_Pruefpaket.zip) · [CPU-Optimierung und Messwerte](../packages/X6_CPU_Optimierung_Pruefpaket.zip)
2. In diesem Ordner die acht kleinen Kontrollrechnungen gegen die direkte nichtperiodische Referenz ausführen. Das letzte Argument ist ein neuer Ergebnisordner.

   ```sh
   bash run.sh check . kontrolle
   ```

3. Nach der Reservierung **nur den übernommenen Lauf** starten. Beispiel für A. Für B beide Buchstaben A durch B ersetzen.

   ```sh
   bash run.sh A . rueckgabe-A
   ```

In einer vorhandenen Repository-Kopie kann man im Ordner `community_pilots` dieselben Befehle mit `../packages` als Archivverzeichnis verwenden. Der Serienlauf ist im Modellarchiv unter `UEBERGABE.md` beschrieben.

## Rückgabe

Den Ergebnisordner als ZIP in [Issue #192](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues/192) anhängen. Er enthält `pilot_A.json` bzw. `pilot_B.json`, `halo_checks.csv` und `environment.txt` mit CPU, Softwareversionen und verstrichener Laufzeit. Auch Werte ausserhalb des Zielbands sind wissenschaftlich relevant. Bei Abbruch Laufbuchstabe, Laufzeit und Fehlermeldung melden. Eine Datei mit Endung `.partial` ist ein unvollständiger Lauf. Für einen erneuten Versuch denselben Buchstaben und einen neuen Ausgabeordner verwenden.

Der Vier-Thread-Kern verteilt vollständige Endpunkte und addiert anschliessend in der seriellen Reihenfolge. Der Aufwandstest reproduzierte beide seriellen Teilsummen bitgleich. Für jeden vollständigen Lauf gilt die bisherige Auswertungsregel. Ein gesicherter Treffer verlangt, dass der geglättete Massenwert einschliesslich seiner Abschneidefehlerschranke im Zielband [0,9, 1,1] liegt. Zwei Einzelwerte allein bestimmen keine Trefferwahrscheinlichkeit von 95 %.

**English.** Claim A or B in issue #192 before starting. Use your own machine or approved donated compute time and confirm that no costs will be passed on to Thomas Gfeller or the project. Download the two ZIPs and the shell script above. Run the local controls, then run your chosen letter. Attach the result directory as a ZIP in the same issue, including unsuccessful or out-of-band outcomes.
