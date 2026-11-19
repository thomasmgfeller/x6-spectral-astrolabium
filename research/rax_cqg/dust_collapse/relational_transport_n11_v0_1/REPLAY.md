# Offline nachrechnen

Python 3 mit NumPy und SymPy genügt. Getestet mit den in environment.json genannten Versionen. Im entpackten Verzeichnis ausführen.

```sh
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python3 -B verify.py
```

Der Prüfer berechnet die exakten Ausschlussschranken, den Direktweg, beide verschobenen Schnitte und die C0-Staubkontrolle erneut. Er vergleicht jedes gespeicherte numerische Feld mit absoluter Toleranz 5e-9 und prüft zusätzlich die exakten JSON-Werte sowie 48 einzelne Teilintegrale und die unabhängige Phasenmomentrechnung. Die Dateiprüfung bezieht sich auf das ausgelieferte Archiv. Abweichende Bibliotheksversionen können Rundungsdifferenzen erzeugen.

Die unmittelbaren Quellen sind unter sources/ enthalten. provenance.json nennt Repository, Commit und Pfad. Die gespeicherten Zweig-Gramwerte enthalten die Gravitationsphase und die Faktoren 1/2. Die skalar bedingten eindeutigen Treffer haben verschwindenden gemischten Beitrag. Der dritte Ausgang fasst alle übrigen Versuche einschliesslich Fehlschlag zusammen. In allen Routen bleiben die Wahrscheinlichkeiten unbedingt. Für den gemeinsamen Staubtransfer bleiben die tatsächlichen C0-/C1-Schnittbedingungen erhalten.
