# CSPP: massive Kontinuumsreferenz v0.5

**Die 50 fehlenden außerzentralen Werte sind eingeschlossen.** Zusammen mit
v0.3 sind damit alle **84 Amplituden an den 28 festen Proben** für m=0,1,2
abgedeckt. Eine eigene räumliche Detektorrechnung liefert jetzt ebenfalls
Fehlergrenzen, erreicht aber die angestrebte Genauigkeit noch nicht.
**G1 bleibt HOLD; G2/G3 bleiben NOT_RUN.**

## Punktreferenz abgeschlossen

| Umfang | Ergebnis |
|---|---:|
| Neue Werte für m=1,2 außerhalb des Zentrums | 50 von 50 |
| Abgedeckte feste Probe/Masse-Paare einschließlich v0.3 | 84 von 84 |
| Größter Komponentenradius, einschließlich Quadratur und Quellenrand | < 3,60 × 10⁻²² |
| Vorab festgelegter Komponentenradius | 10⁻¹² |
| Größte Abweichung zur früheren feinen Ortsraumrechnung | < 8,20 × 10⁻¹⁵ |
| Separat ausgeführte Präzisionen | 128 und 192 Bit |

Die Ortsraum-Übereinstimmung ist eine Gegenprüfung. Die Einschließungen
beruhen auf Ballarithmetik, der KG-Cauchyformel, expliziten Quadraturgrenzen
und analytischen Abschneideresten. Das negative Lichtkegel-Oberflächenglied
bleibt enthalten. Die Normierungsunsicherheit der unveränderten Quelle
wird durchgehend mitgeführt.

Maschinenlesbar: [50 Werte bei 128 Bit](results/SOURCE.json),
[Wiederholung bei 192 Bit](results/SOURCE_192bit.json).
Die [34 früheren Werte](../certified_budget_v0_3/results/SOURCE.json)
bleiben unverändert; der Verifier prüft die vollständige Vereinigung ohne
Lücken oder doppelte Identitäten.

## Räumliche Detektorintegration: eingeschlossen, noch zu grob

Die sieben bisherigen Detektor-Punktproben werden nicht als Volumenintegral
ausgegeben. Das neue Verfahren integriert über die ganze festgelegte Kugel
(t=1, Mittelpunkt (0,0,1,5), Radius 0,5) die skalaren Überlappungen
Gᵢⱼ=∫D φₘᵢ conj(φₘⱼ) d³x für m₁=1, m₂=2.

648 Raumzellen erhalten vollständige Intervallbereiche und eingeschlossene
exakte positive Volumina. Auch die Quellenintegration innerhalb einer Zelle
wird durch vollständige Wertebereiche abgesichert. Quellenrand und eine
winzige abgeschnittene Detektorspitze besitzen zusätzliche explizite Grenzen.

| Komponente | Größter Radius über beide Präzisionen, aufgerundet |
|---|---:|
| G₁₁ | 9,080 × 10⁻³ |
| G₂₂ | 1,640 × 10⁻² |
| Re G₁₂ | 1,213 × 10⁻² |
| Im G₁₂ | 1,141 × 10⁻² |

Der analytische Quellenrand trägt höchstens **7,71 × 10⁻⁷**, die ausgelassene
Detektorspitze höchstens **1,98 × 10⁻¹⁰** zu einem Eintragsfehler bei.
Die wesentliche Überbreite entsteht somit aus den Quellen- und Raumzellbereichen.
Diese beiden Bereichsanteile werden nicht als getrennt gemessene Fehler
behauptet. Höhere Bitpräzision allein löst dieses Problem nicht.

Der gesonderte Komponentenradius-Screen **10⁻³ ist nicht erfüllt**. Dies ist
keine Erfüllung oder Umrechnung des E4-Spurabstandsbudgets. Die Intervalle
werden weder still auf positive Werte beschnitten noch renormiert.

Nachweise: [räumliche Einschließungen](results/DETECTOR.json),
[192-Bit-Wiederholung](results/DETECTOR_192bit.json),
[Herleitung und Fehlertransport](METHODS.md).

## Prüfung und Reproduktion

Der Audit umfasst unter anderem vier unabhängige Kugelschnittvolumina,
24 massive Symmetrieprüfungen, vier Support-/Anfangsdatenprüfungen, acht
Enthaltenseinsprüfungen gegenüber den scharfen Punktwerten und vier exakte
Detektormomente. Die früheren 27 KG-Ebenenwellen und sechs
Vorzeichen-Negativkontrollen werden ebenfalls erneut ausgeführt.
Alle 50 Punktwerte und drei komplex beziehungsweise reelle Detektoreinträge
wurden bei 128 und 192 Bit berechnet. Lokaler vollständiger Lauf: etwa 167 s;
keine neuen Zufallswolken, kein Bestätigungsseed.

```sh
python3 -m pip install -r research/cspp/massive_reference_v0_5/requirements.txt
python3 -O -B research/cspp/massive_reference_v0_5/verify_publication.py
python3 -B research/cspp/massive_reference_v0_5/verify_publication.py --replay
```

Der Replay schreibt in ein temporäres Verzeichnis. Für explizite eigene
Ausgaben:

```sh
python3 -B research/cspp/massive_reference_v0_5/run.py all --out /tmp/cspp-massive-replay
```

[Audit](results/AUDIT.json) · [Laufumgebung](results/COMPUTE.json) ·
[Protokoll](PROTOCOL.json) · [Quellsperre](FREEZE.json) · [Prüfsummen](SHA256SUMS).
Die Quellsperre wurde nach einer ausdrücklich explorativen Vorprüfung und
vor dem gespeicherten Produktionslauf erstellt; dies ist kein bestätigender
E4-Versuch und keine externe unabhängige Reproduktion.

## Was weiterhin offen ist

- Engere räumliche Integrationsgrenzen. Der nächste Schritt sollte die
  Überabschätzung der Zellbereiche reduzieren, etwa durch validierte lokale
  Taylor-Quadratur; bloß mehr Bits helfen hier nicht.
- Die übrigen 256 archivierten Abfragepositionen und ein globaler Fehler
  der Lösung beziehungsweise der verwendeten numerischen Vorgeschichte.
- Die vollständige Dirac-Spinor-Detektorreferenz, ihr Fehlertransport zur
  Dichtematrix und eine abgesicherte bedingte Normierung.

Die neue Matrix gehört zur skalaren Null-Anfangsgeschwindigkeitsaufgabe.
Sie ersetzt keine Dirac- oder Flavorqualifikation. Der unabhängige
Vergleichsbestand ist wesentlich vollständiger; die volle Referenz bleibt HOLD.
