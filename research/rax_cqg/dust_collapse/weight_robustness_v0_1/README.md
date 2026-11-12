# CST-DUST: Gewichtsrobustheit des vollständigen Blocks v0.1

12. November 2026. Für die schon festgelegte 33-Historien-Familie ist der gesamte V-normierte Differenzblock über die gesamte bisher zugelassene Gewichtsklasse von null getrennt.

| Ziel | Zertifizierte untere Grenze des globalen Minimums | Zertifizierte obere Grenze |
|---|---:|---:|
| vollständiger 6×6-Block | 0.0022939794998 | 0.0022939795002 |
| vollständiger Atom→Positiv-Block, 4×2 | 0.0003502439596 | 0.0003502439599 |

Die Ziele werden separat minimiert. Die Intervalle sind deterministische Schranken, keine statistischen Konfidenzintervalle. Das Infimum über strikt positive Gewichte ist gleich dem Minimum über die abgeschlossene Klasse nichtnegativer Gewichte.

## Was unverändert bleibt

Alle nichtnegativen, normierten Gewichte, invariant unter unabhängigen Vertauschungen der beiden Eingangs- und Ausgangslabels, unabhängig von λ und Integrationsvariablen. Es gibt zehn freie Orbitmassen w_o≥0, Summe 1; jedes Label in Orbit o trägt w_o/n_o. Keine zusätzliche Mindestmasse und keine aus dem Ergebnis abgeleitete Symmetrie-, Zähl- oder Verklebungsbedingung.

E6/F6, E2/F4, gewichtete V-Norm, alle Phasen und inneren Dichtemasken entsprechen dem vorherigen Kopplungsbefund. Die entkoppelte Referenz ist weiterhin die uniforme gelabelte mittlere Hessian; sie wird bei Gewichtsänderungen nicht neu gebildet. Keine Normierung durch die komplexe Gravitationssumme.

## Warum die Untergrenze global gilt

Der vollständig normierte 6×6-Block besitzt eine exakte isometrische Darstellung durch einen 6×2-Block C(w)=Σw_o C_o. Zwei feste rationale komplexe Vektoren u,v liefern für jeden Orbit eine eingeschlossene reelle Zahl q_o=Re(u* C_o v)/(‖u‖‖v‖). Für jedes Gewicht gilt ‖C(w)‖≥Σw_o q_o≥min q_o>0. Zehn überprüfte Ungleichungen erfassen damit die ganze Klasse. Der Optimierer schlägt nur Kandidaten vor.

Ein explizites rationales Gewicht liefert die obere Grenze über die analytische 2×2-Gram-Eigenwertformel. Ein zusätzlicher Zeuge mit w^(ε)=(1−ε)w+ε(n_o/33), ε=10^-12, hat strikt positive Gewichte auf allen 33 Historien und erfüllt dieselbe publizierte Obergrenze. ε schränkt die Gewichtsklasse nicht ein.

Die Zertifikate enthalten auch das feste Paar von V-Einheitszuständen, das für alle Gewichte einen positiven Realteil der Antwort bezeugt. Vier feste Eingangsnullrichtungen bestehen dennoch weiter.

## Zusammenhängender Anteil bleibt getrennt

Der vollständige Unterschied wird weiterhin in zusammenhängenden Historienanteil und Änderung der mittleren Skalarantwort zerlegt, wo Z(w)≠0. Die Differenzblock-Minimierung enthält keine Z-Beschränkung.

An jedem Orbitvertex ist der zusammenhängende Anteil exakt null, während der Differenzblock ungleich null bleibt. Bei strikt positiven Gewichten ist sein Infimum ebenfalls null. Der robuste Gesamtbefund begründet also **keine** positive uniforme Untergrenze des zusammenhängenden Anteils. Alle fünf vollständigen Blöcke für uniforme, bisherige Einzelkanal-Auslöschungs- und neue beinahe minimierende Gewichte stehen in results/diagnostics.json.

## Reproduktion

```sh
python -m pip install -r requirements.txt
python -B verify.py
```

Der Verifizierer kontrolliert alle Paketdateien, rechnet die 40-Knoten-/192-Bit-Quadratur und beide Zertifikate in einer temporären Kopie neu und verlangt identische Ergebnisdateien. Danach laufen neun Kontrollgruppen mit fünf gezielten Negativkontrollen. Die eingefrorenen rationalen Vektoren machen die Zertifizierung unabhängig von plattformspezifischen SVD-Vorschlägen.

- `compute.py`: Ballarithmetik, globale Unter-/Obergrenzen, Ursachenzerlegung und sämtliche Orbitblöcke.
- `tests.py`: Gewichte, 33↔10-Historien-Summe, Gram-Matrix, isometrische Kompression, Vorbefunde, Ursachenzerlegung, Basiswechsel und Negativkontrollen.
- `inputs/*_candidate.json`: exakt definierte rationale Gewichte und rationale komplexe Dualvektoren.
- `results/*_certificate.json`: alle zehn Dualintervalle, obere Schranke, positiv gewichteter Zeuge und universelle Zustandskoeffizienten.
- `discover.py`: optionale numerische Kandidatensuche; `python discover.py --output /tmp/new-weight-candidates`. Ihre Ergebnisse sind keine Zertifikate und überschreiben die geprüften Kandidaten nicht.
- `basis.py`, `inputs/core.py`, `inputs/prior_quadrature.py`: unveränderte, eingefrorene Module des vorherigen Pakets; keine eigenständigen Programmeinstiege.
- `DERIVATION.tex`, PDF: Beweis, explizite Gewichte, Fehlerbilanz und Grenzen. PDF-Neubau mit `python build_pdf.py` und TeX Live.

## Aussagegrenzen

Befund nur für den erklärten endlichen Test-/Antidualbereich, die erklärte Historiensumme und feste Intervention. Keine volle V-Operatornorm, kein neu hergeleitetes physikalisches Historienmaß, kein Nichtnullsignal für jeden Zustand, keine physikalische Evolution oder Bounce-Aussage. Kompakte Reduktion bleibt HOLD; physikalische CST-Evolution bleibt NOT_CONSTRUCTED. Kein neuer 1089-Historienlauf, keine externe Begutachtung.

Quellstand: main 558339f0c40a3309d108674d411f548d2061dd57, PR #287; Gewichtsklasse aus Mischungsqualifikation v0.1. Der neue Prüfvertrag wurde vor der Gewichtsoptimierung angelegt, ohne externen Zeitstempel. Apache-2.0.
