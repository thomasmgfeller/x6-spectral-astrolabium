# Welche Entropiewerte die zertifizierten N15-Gewichte zulassen

Der Prüfer liest die markierten Vier-Marken-Daten und die zehn veröffentlichten primalen und dualen Extremwertzertifikate. Er prüft die 928 globalen Spalten mittels zweier Katalogrekonstruktionen, die 72 festen N13-Präfixmassen und die affine Dimension neun der zehn lokalen N15-Endtypanteile am Präfix 1564. Ein Eintrag des Zertifikatkatalogs bezeichnet einen Extremwertzeugen eines linearen Programms. Die zehn Zeugen sind unterschiedliche Verteilungen.

## Ein neuer exakter Zeuge

Die bestehenden Constraints lassen die lokale Gleichverteilung pⱼ=1/10 zu. Gleichverteilung.json enthält einen rationalen globalen Zeugen mit 43 positiven Spalten. Gleichverteilung_strikt.json enthält einen zweiten Zeugen mit positivem Grundgewicht 1/1 000 000 auf jeder der 928 Spalten und 47 rationalen Zuschlägen. Der Prüfer rekonstruiert die ganze Projektion direkt aus den Eingabedaten. Jede der 72 Präfixmassen und sämtliche zehn Zielanteile werden genau getroffen.

Zusammen mit dem publizierten Zeugen für p₇₆₆=1 folgt eine vollständige Spannweite für die diagonale Endtypstatistik I(p)=1−Σpⱼ². Für p(t)=(1−t)e₇₆₆+t(1/10,…,1/10) ist I(p(t))=(9/10)(2t−t²). Entlang dieses Weges bleiben alle linearen Nebenbedingungen erfüllt. Bei 0<t≤1 kann für die Gleichverteilung der strikt positive globale Zeuge gewählt werden. Global folgt 0≤I≤9/10 aus pⱼ≥0, Σpⱼ=1 und Cauchy-Schwarz. Auf der abgeschlossenen Familie ist damit [0,9/10] exakt erreichbar, auf der Familie der **strikt positiven** globalen Gewichte (0,9/10]. Ein Wert null erfordert einen lokalen Einheitsvektor. Jede der zehn Komponenten ist bei durchweg strikt positiven globalen Gewichten positiv, denn für jede gibt es mindestens eine beitragende Spalte.

I(p) ist eine klassische Kollisionsstatistik, numerisch gleich der linearen Entropie einer zusätzlich gewählten diagonal gemischten Endtyp-Matrix. Die Physik einer räumlichen Teilspur setzt eine Präparation und eine Innen-/Aussenalgebra voraus. Der Zeuge enthält weder eine solche Abbildung auf die 22 Knoten noch eine Entscheidung zwischen den geometrischen Kontrollkugeln. Speziell für die Endtypbasis würde ein reiner kohärenter Zustand mit denselben diagonalen Wahrscheinlichkeiten global stets Reinheit 1 haben.

Der Prüfer wiederholt ausserdem die kubischen Ergänzungen des Radiusoperators von Abschnitt 4 bei x=1/2. Bei jeder festgehaltenen Gewichtung und positivem Normnenner ergeben sie für die Massendifferenz −505/384 bzw. +95/384.

## Offline wiederholen

    python3 -B pruefen.py

Python ab 3.10 und Standardbibliothek genügen. Die Suche nach den neuen Gewichten verwendete ein lineares Programm und eine anschliessende rationale Lösung des Systems auf den gewählten Spalten. Alle hier ausgewiesenen Bescheinigungen werden im Prüfer rational ohne Optimierer kontrolliert. Ergebnisse.json gibt die erwartete Ausgabe wieder.

[Ursprungsstudie, Abschnitte 2 und 4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/early_areal_radius_two_masses_v0_1) · [Kohärente N15-Auslese am äusseren skalaren Rand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/e2e2597ce45b9fa1aa5982c99943cde002bda8a0/research/rax_cqg/dust_collapse/prefix_1564_nine_directions_v0_1)
