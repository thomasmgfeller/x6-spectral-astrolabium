# Zwei Ereignisse am markierten Präfix 1564 ausintegrieren

**Die direkte Reduktion N15 → N13 und beide Folgen von Ein-Ereignis-Reduktionen ergeben in den zwei vorab ausgewählten Beispielen denselben skalaren Kern.** Ein Beispiel enthält eine echte Fourier-Delta-Verteilung. Die Gleichheit gilt bereits für die Felder einer einzelnen markierten N15-Ordnung. Sie gewinnt für die neun freien Endgewichtsrichtungen am Präfix Rang **null**. Für beide früher publizierten A:B-Verhältnisse existiert eine positive lokale N15-Fortsetzung.

## Auswahl

`design.json` legt vor der Enumeration den Träger, die Ordnung der Kandidaten, die singuläre Zusatzprobe, den Uhrenvergleich und das Kriterium für einen neuen Gewichtsselektor fest. SHA-256 ist `79fdf60b0a962172fe579234de3ce85a48a37f32475eccd23835d9b021181417`. Der erste öffentliche Commit dieser Arbeit dokumentiert den Wortlaut der im Arbeitslauf fixierten Auswahlregel. [Festgelegtes Design](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/a886aca66df784f887f3983bba4db718ff02cd5e/research/rax_cqg/dust_collapse/prefix_1564_two_event_v0_1/design.json) Ausgangspunkt sind genau die 16 markierten Fortsetzungen der publizierten Randabbildung. Jedes Paar mit verschiedenen N14-Endtypen wird auf den gemeinsamen fünf alten Innenmarken identifiziert. Die beiden neuen Marken bleiben zunächst unvergleichbar. Nur transitive Vereinigungen mit beiden katalogisierten N14-Zugängen, dem N15-Rangprofil (0,0,0) und regulärem äusserem Skalartransport sind zulässig. Der natürliche N15-Code ist das Minimum über alle linearen Erweiterungen. Die Wahl bevorzugt A = 1790 und B = 5374 und verwendet anschliessend ausschliesslich Ordnungskennzahlen.

| Prüfschritt | Markierte Paare |
| --- | ---: |
| Zwei verschiedene N14-Endtypen | 111 |
| Transitive Vereinigung bei unvergleichbaren neuen Marken | 51 |
| Beide Kanten im veröffentlichten N15-Katalog | 51 |
| Alle Ränge und der äussere reguläre Randtransport zulässig | 42 |
| Darunter mit regulärem Zweierblock / mit Rang eins | 24 / 18 |
| Darunter mit beiden A und B / mit genau einem von beiden | 0 / 13 |

Die 42 markierten Paare entsprechen 22 verschiedenen N15-Endtypen. Für unvergleichbare Marken verschwindet der direkte Skalar-Mischeintrag. Daher gab es im untersuchten Träger auch keinen invertiblen Zweierblock mit verschwindendem Diagonalpivot.

| Ausgewählter Fall | N14-Zwischenordnungen | N15-Endtyp | Neuer Skalarblock | Gravitationszahl N13 → N14 → N15 |
| --- | --- | ---: | --- | --- |
| Primär, regulär | 766 / 1790 | 46078 | diag(−5, −10) | −9 → 26 bzw. 52 → −23 |
| Ergänzung, ein Nullpivot | 926 / 1790 | 59006 | diag(0, −10) | −9 → −15 bzw. 52 → 54 |

## Skalarteil und Fourier-Bedingung

Die alten 13 reellen Felder heissen X, die beiden neuen z. Auf dem gemeinsamen Abel-Regulator der geerbten reellen Skalarintegration lautet die Phase exp[iβ(XᵀAX + 2XᵀUz + zᵀDz)/2], mit β = 4/√6. Für die regulären Einträge h des diagonalen D gibt der gemeinsame Pushforward die Korrektur −Σ uuᵀ/h zur alten Matrix A. Jeder dieser Einträge trägt den Faktor (2π/β)¹ᐟ² |h|⁻¹ᐟ² exp[iπ sgn(h)/4]. Bei h=0 liefert die Fourier-Integration (2π/β) δ(uᵀX). Diese Aussagen gelten gepaart mit Schwartz-Testfunktionen. Die unabhängigen neuen Integrationsrichtungen können bei endlichem Gaußregulator getrennt integriert werden. Für die gewählten Fälle bleibt im Grenzwert höchstens eine nichtverschwindende Delta-Normale.

Im zweiten Beispiel ist die Normale in der Reihenfolge X₀,…,X₁₂ gleich (0,0,−4,8,−9/2,0,1/2,1/2,−9/2,8,−4,0,0). Nach Auflösen der Bedingung in X₄ ist der Faktor **2/9**. Der Prüfer vergleicht die volle verbleibende quadratische Form, die Normalen in den ursprünglichen Koordinaten und die Faktoren für beide Integrationsreihenfolgen mit der direkten Zweierformel. Er substituiert zusätzlich im geerbten Randrahmen die Delta-Bedingung. Der äussere Schur-Kern, die Determinanten und die Fresnel-Signatur stimmen exakt mit der vollständigen N15-Integration überein. Damit stimmt auch die absolute Normierung aus dem Ein-/Ausgangs-Mischblock und der inneren Determinante. Die Ergebnisse enthalten die oberen Dreiecke der rationalen Matrizen.

**Zusatzbeobachtung im Anschluss an die festgelegte Auswahl.** Die beiden gewünschten A/B-Zwischenordnungen sind am markierten Präfix durch die Codes 25769807420 und 545263164 eindeutig festgelegt. In ihrer Vereinigung erfordern die Ketten 5≺3≺6 und 5≺4≺6 der sieben Innenmarken die neue Relation 5≺6. Die transitive Vervollständigung besitzt den zulässigen Endtyp 343038. Hier ergibt sich der gemischte Zweierblock [[−10,8],[8,−1]] mit Determinante −54 und Signatur null. Beide mathematischen Eliminationsreihenfolgen liefern exakt dieselbe Reduktion. Die Richtung 5≺6 ist durch die Kausalordnung festgelegt. Diese nachträgliche Skalarprüfung illustriert, weshalb die Reihenfolge der Feldintegration allein keine unabhängige Wahl einer kausalen Geburt ist.

## Staub, Uhr und Gravitation

Für einen festen N15-Zweig wird jeder neue Uhrwert mit ds/3 auf [−3/2,3/2] und jede Dichte mit ½ δ₀ + ½ dr auf [0,1] integriert. Die Integration der neuen Dichte mit Wirkungsterm −rC/2 liefert d(C) = [1 + exp(−iC/4) sinc(C/4)]/2. Alle Phasen haben auf reellen Argumenten Betrag eins und die übrigen Masse sind endlich. Für festgehaltene alte Daten gilt daher die Vertauschbarkeit der beiden Staub-/Uhrintegrale auf diesem Zweig. Die gemeinsame Wirkung wird dabei in jeder Zwischenordnung einschliesslich aller geänderten Intervalle neu aufgebaut. Der Gravitationszuwachs teleskopiert für beide Wege zur gleichen Differenz F₄(N15) − F₄(N13).

Für beide ausgewählten N15-Ordnungen berechnet eine zusätzliche Kontrolle mit den alten Uhr- und Dichtewerten aus `design.json` die komplexe Punktantwort. Eine direkte Doppelsumme wird auf jedem identischen Gitter mit zwei getrennt faktorisierten Wegen über die nackten N14-Wirkungen verglichen. Bei den Uhrenordnungen 8 und 16, beiden Dichtezentren und beiden Lappenzentren beträgt der grösste Unterschied unter den 32 Wegvergleichen weniger als **1,1 × 10⁻¹⁵** in der verwendeten Umgebung. Die Kontrolle betrifft feste alte Daten. Eine Fehlergrenze für die kontinuierliche Amplitudenhöhe oder ein vollständig integriertes äusseres Uhrenpaket wird daraus nicht abgeleitet.

## Gewichtsprüfung

Die neue gemeinsame Rechenidentität gilt für jeden festen N15-Zweig und bleibt bei Multiplikation mit jedem beliebigen Pfadkoeffizienten erhalten. Jeder Gradient dieser Differenz entlang der neun N14-Präfixrichtungen verschwindet daher identisch. Das gilt unabhängig von der Genauigkeit der Uhrquadratur.

Die lokale Eliminierung lässt sich auch konstruktiv prüfen. Für einen zulässigen markierten N14-Pfad mit Gewicht x verteile x gleichmässig auf seine einzeln zugelassenen N15-Einfügungen. Nach Zusammenfassen nach N15-Endtyp erhält eine Tochter mit Multiplikation m den Koeffizienten x·m/Σm. Der publizierte Katalog enthält für jeden der zehn Endtypen eine nichtleere Menge solcher Einfügungen. Die Summe reproduziert jedes x exakt. Die folgende Tabelle gibt zwei explizite Präfixzeugen wieder. Die übrigen acht Gewichte stehen in `result.json`.

| Parameter der geerbten zulässigen Linie | q(A) | q(B) | A:B |
| --- | ---: | ---: | ---: |
| 0 | 1/18 | 1/18 | 1:1 |
| 1/1764 | 1/36 | 1/12 | 1:3 |

Diese Fortsetzung ist ein Existenzzeuge für die lokale Verzweigung. Sie setzt keine Austauschbarkeit aller vier Einfügungsmarken voraus. Der Vergleich vieler markierter Pfade über einen physikalischen gemeinsamen Rand braucht weiterhin eine unabhängig begründete Paarung und relative Normierung. Für einen Gewichtsentscheid müsste eine solche Bedingung nach Eliminierung aller zulässigen feinen Gewichte mindestens eine grobe Verschiebung ausschliessen. Der vorliegende Test belegt endliche Zusammensetzung in den ausgewählten Ordnungen. Eine über mehrere Skalen geschlossene Wirkungsfamilie, Etappe 6 und der physikalische P3-Pilot bleiben offen.

## Nachrechnung

Die Prüfer wurden mit Python 3.12, SymPy 1.14 und NumPy 2.3.5 ausgeführt. Alle Eingaben liegen im Unterordner `inputs/`. Ein CPU-Prozess genügt. Der zweite Befehl vergleicht die exakten Ergebnisse vollständig und die wenigen Quadraturwerte mit der festgelegten numerischen Toleranz.

~~~sh
python3 -B two_event.py > replay.json
python3 -B compare.py result.json replay.json
~~~

[Ein-Ereignis-Randabbildung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/prefix_1564_boundary_map_v0_1) · [N15-Katalog und Prüfer](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/extension_stability_v0_7) · [N13-Gewichtszeugen](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/8723cba93224931a6fdffc525c798524ab38bebb/research/rax_cqg/dust_collapse/prefix_1564_selection_v0_1)
