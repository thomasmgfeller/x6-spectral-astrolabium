# CST-DUST: Normpfad und kohärenter Quotient v0.1

7. November 2026. Auf Main nach PR 249 aufgebaut.

Positive diagonale Hilfsnormen für die vollständige Vergangenheit existieren
für alle Stufen. Sie entsprechen genau konsistenten positiven Zylindermaßen
über h(P)=e(P)^2 μ(P). Eine bekannte transitive Perkolationsfamilie liefert
explizite Beispiele, ohne die geerbten Fortsetzungsamplituden zu verändern.
Das wählt keine physikalische Dynamik oder physikalische Norm aus.

Die unveränderte kohärente Endkontraktion besitzt in dieser gesamten
normalisierten diagonalen, feldunabhängigen Klasse **keine gleichmäßige
Normschranke** über die Elementzahl. Der allgemeine Beweis steht in
`DERIVATION.md`. Ein kohärenter Quotient der unmarkierten Geometrieamplituden
ist zusätzlich exakt konstruiert. Auf ihm scheitert die Isometrie mit
positiven diagonalen Produkten bereits beim Schritt zwei nach drei Elemente.
Nichtdiagonale positive Produkte sind konstruktiv möglich, aber physikalisch
nicht ausgewählt; die markierte Ereignisalgebra bleibt offen.

Alle acht physikalischen Gates bleiben HOLD. Kein allgemeines No-go für CST,
kein Nachweis eines physikalischen unendlichen Quantenmaßes und kein Bounce.

## Reproduktion

```bash
python3 -O -B analyze.py
python3 -O -B replay.py
```

Python 3.10+, nur Standardbibliothek. Fünf Ergebnisdateien werden aus Quellen
isoliert bytegleich reproduziert. Die unabhängige Vergleichsroute enumeriert
33.868 gerichtete azyklische Graphen und bildet ihre transitive Hülle.
15.696 rationale Wahrscheinlichkeitsvergleiche und 17.118 exakte
Horizontvergleiche sind ausgeführt. Die allgemeinen Beweise sind nicht
formal maschinengeprüft. Der lokal vor Implementierung gehashte Plan ist
keine externe Präregistrierung oder blinde Vorhersage.

`norm_contract.json` grenzt Zustandsdarstellung, Kohärenz und physikalische
Auswahl voneinander ab. Sechs unveränderte Quellen sind auf Main
`573084d007ae96d82eb6c241df6ae1d572523418` gepinnt.

## Bericht und Paket

`python3 -B build_report.py` benötigt zusätzlich ReportLab und DejaVu-Schriften.
`python3 -B package.py` erzeugt das ZIP samt vollständigem SHA-256-Manifest.
Vorschaubilder und Python-Caches werden nicht mitverpackt.
