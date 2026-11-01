# CSPP v0.29 - Intervallvolumen und stabile Ausbreitung auf endlicher Zeit

Die neue positive Pfadmajorante berücksichtigt die Poisson-Verteilung der
Intervallzahlen. Die konstante Gewichtshülle aus v0.28 wird durch das
volumenabhängige mittlere Betragsgewicht ersetzt. Für vollständige
Kausalintervalle gilt die Schranke für jede Dichte rho>=3/pi bei festem
q=3/(16*pi), T=9/4, H=4, delta=0.01 und einem festen Detektormittel Q=1.
Kausaldiamanten, insbesondere Omega5, erfüllen die zusätzliche Gebietsbedingung.

Für theta=21 sinkt die gemeinsame hinreichende Verstärkungsobergrenze von
82030.234 auf höchstens 34819.303. Ein vereinfachter, sicher nach oben
gerundeter Wert ist 34820. Die Verbesserung beträgt mindestens Faktor 2.35.
Es handelt sich um eine kleinere Obergrenze, nicht um gemessene Fehlerreduktion.
METHOD und G1 bleiben HOLD; der Genauigkeitsausschluss aus v0.25 bleibt bestehen.

## Inhalt

- `PROOF.md`: Definitionen, vollständige Beweise, Gebietsvoraussetzung,
  Zeit-/Historyabbildung, zertifizierte numerische Methode und Grenzen.
- `results/RESULTS.json`: Alle eingeschlossenen Zahlen und Prüfresultate.
- `reproduce.py`: Ausschliesslich Python-Standardbibliothek; rationale
  Gewichte und nach aussen gerundete Integer-Intervallarithmetik.
- `evidence/`: Sechs unveränderte Projektquellen mit Git-Blob und SHA256.
- `STATUS.json`: Wissenschaftlicher Status; unveränderte offene Gates.
- `report/Intervallvolumen_Pfadstabilitaet_v0_29.pdf`: Lesefassung.
- `REPLAY.json`: Isolierte Wiederholung und Prüfumfang.
- `SHA256SUMS`: Prüfsummen aller anderen Paketdateien.

## Reproduktion

Python 3.12 und die Standardbibliothek genügen für die mathematische Rechnung:

```sh
python3 -I -O -B reproduce.py --check
```

Der Lauf dauert mehrere Minuten. Er erzeugt keine Zufallswolken, macht keine
Netzabfragen und verändert mit `--check` keine Ergebnisdatei. Explizite
Ausnahmen halten alle Kontrollen auch unter `-O` wirksam. Ohne `--check`
wird `results/RESULTS.json` neu geschrieben. Berichtserzeugung ist getrennt
und benötigt ReportLab und Matplotlib; sie ist keine Voraussetzung für
die Reproduktion der mathematischen Ergebnisse.

Die Rechnung enthält zwei Raum-/Zeitgitter und zwei Integerpräzisionen.
Jede Konfiguration liefert selbst eine gültige Einschliessung, unabhängig
von einem beobachteten Konvergenztrend. Untere Grenzen beziehen sich auf
die Majorante und sind keine unteren Grenzen der tatsächlichen Fehler.

## Reichweite

Die Faktorisierung gilt entlang einer einzelnen Kette mit disjunkten
benachbarten offenen Intervallen. Überlappende Pfade, gemeinsame Knoten
und Mecke-Einfügungen zwischen Pfaden sind ein eigener nächster Auftrag.
Keine neue Kovarianz, keine zeituniforme Schranke, keine unendliche History,
kein wachsendes globales räumliches Maximum und keine KG-Fehlerfreigabe.
Für beliebig beschnittene Intervalle bleibt zunächst die v0.28-Hülle zuständig.

Keine externe Begutachtung, keine Beweisassistent-Verifikation und kein
Prioritätsanspruch. Entwicklungsschritt; noch keine GitHub-Veröffentlichung.
