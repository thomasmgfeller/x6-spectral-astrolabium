# RAX-CQG: Freies Feld und Entropiereferenz

Ein begrenzter Anschluss eines freien reellen Gaußfeldes an die vorhandene
kausale Ordnung. [Zustand, Randbedingungen und Nullmoden](MODEL.md) sind
verbindlich beschrieben; der [Versuchsvertrag](contract.json) trennt
Softwareprüfung, numerische Referenz und späteren Zusatznutzen.

**Stand: Feldkern und kleine Oszillatorreferenz geprüft; der größere Skalierungsversuch bleibt REFERENCE_NOT_ESTABLISHED.** 64 neue Ordnungen sind vollständig berechnet. Die Hauptsteigung 0,358 mit 95%-Intervall [0,260; 0,458] erfüllt die vorab verlangte Präzision und Cutoff-Stabilität nicht. [Ergebnisse und Grenzen](RESULTS.md).

```sh
python3 -m pip install -r research/free_field_entropy/requirements.txt
OPENBLAS_NUM_THREADS=1 python3 -B research/free_field_entropy/test_core.py -v
python3 -B research/free_field_entropy/run.py --source-ref bfdaae666978ffeb0ef92980d15df1aa07271d7e --output /tmp/x6-field-reference
python3 -B research/free_field_entropy/check.py /tmp/x6-field-reference --audit
```

Der angegebene öffentliche Commit enthält `freeze.json`; die Ausführung
prüft die Dateihashes gegen diesen Git-Stand. Das Ausgabeverzeichnis muss neu
sein. Der Arbeiter hat 30 Minuten, 2 GiB virtuellen Adressraum und einen
BLAS-Thread. Abbrüche erhalten Teildaten und werden nicht durch Ersatzseeds
verdeckt. Die Quelldateien benötigen bei Ausführung keinen Netzwerkzugriff.

Die Quelldaten sind durch PCG64-Seed, Größe und SHA-256 der little-endian
float64-Koordinaten, uint8-Ordnung sowie int64-Regionsindizes exakt festgelegt.
Jede Ordnung wird mit ungekürzter, nur global gekürzter und doppelt gekürzter
Entropiediagnostik protokolliert. `check.py` rekonstruiert alle Eingaben und die
statistische Auswertung. `--audit` prüft zusätzlich die erste Ordnung jeder
Größe mit einer anderen, hermiteschen Kovarianz-Eigenwertformel.

Eine erfolgreiche CI bezeichnet Code- und Evidenzkonsistenz. Der wissenschaftliche
Status steht separat im Ergebnisbericht. Geometrieexperimente und der Vergleich
mit bestehenden Ordnungs-/Spektralmerkmalen sind noch nicht freigegeben.
