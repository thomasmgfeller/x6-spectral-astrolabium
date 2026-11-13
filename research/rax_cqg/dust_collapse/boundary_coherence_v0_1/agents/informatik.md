# Informatik: Intervallfortpflanzung und begrenzte R-Erweiterung

## Ergebnis und Geltungsbereich

Die übernommenen komplexen Amplituden reichen aus, um einen von null
getrennten Interferenzkontrast im neuen kohärenten Instrument zu belegen.
Zusätzlich liefern Dowkers analytisch abgeleitete Gaußmomente zwei echte
terminale Materiemoden, deren Verteilung kohärenz- und phasenabhängig ist.
Beide Aussagen gelten für das deklarierte endliche Hilfsmodell und seine
neue Kohärenzannahme. Sie belegen weder einen gebauten Detektor noch eine
geometrische Observable oder gravitative Rückwirkung.

`checks/interference.py` verwendet ausschließlich die ursprünglichen
Real-/Imaginärintervalle aus `sources/result_64.json`. Quelle und Vertrag
werden über SHA-256 geprüft. Rechenpräzision: 75 Dezimalstellen mit
`mpmath.iv`; Ausgabe: 40 Stellen, aus den exakten binären Intervallenden
nach außen gerundet. Es wird kein Integral neu berechnet. Die Rechnung
erbt sämtliche analytischen und numerischen Voraussetzungen der
Quellintervalle und zertifiziert deren ursprüngliche Quadratur nicht neu.

## Schritt 2: vervollständigter Klassenanalysator

Bei festem \(\theta=0\), \(\lambda=1/256\), getrennten inneren Strata und
vollständiger Kohärenz gilt
\(a_{\pm,s}=(a_{1s}\pm a_{2s})/\sqrt2\). Das ist eine neue kohärente
Realisierung vor einer Klassen-Dephasierung. Klassisches Vergessen eines
bereits entstandenen Klassenrecords erzeugt diese Amplituden nicht.

| Größe | g0 | gplus |
|---|---:|---:|
| P(+ gegeben Erfolg), ungefähr | 0.4305477160 | 0.4304855695 |
| Gesamterfolg, ungefähr | 6.56226696e-9 | 1.70961498e-8 |
| volle Phasensichtbarkeit, ungefähr | 0.33867253 | 0.33758640 |

Der eingeschlossene Quellenkontrast ist

\[
P_+(g_+)-P_+(g_0)\in
[-0.0000621608048078364,-0.0000621322024513728].
\]

Die leicht gröberen gedruckten Grenzen umschließen die exakten
Ausgabeintervalle. Die unabhängige rationale Rechnung in
`checks/root_exact_audit.py` ist damit konsistent. Die Umstellung
\(P_+=1/2+\operatorname{Re}C/Z\) vermeidet unnötige Intervallaufweitung.

Für reelles Umweltüberlapp \(\gamma=0,1/2,1\) werden alle vier
bedingten und unbedingten Portwahrscheinlichkeiten ausgegeben. Bei
\(\gamma=0\) sind die Plus-/Minusverteilung und ihre Sichtbarkeit exakt
phasenblind; bei \(\gamma=1/2\) halbiert sich der Interferenzterm.
Der Gesamterfolg und der alte Failure-Effekt bleiben beim vollständigen
Plus-/Minusanalysator algebraisch unverändert.

Der andere Detektor \(C_s=\lambda(a_{1s}+a_{2s})\) ist ebenfalls
ausgewertet. Seine akzeptierten Effekte sind zweimal die Plusporte;
er hat daher einen **neuen** Failure-Effekt. Sein Quellenkontrast
\(P(\text{atom}\mid\text{Erfolg},g_+)-P(\text{atom}\mid\text{Erfolg},g_0)\)
liegt in \([-0.00129881384533063,-0.00129865673821982]\).
Die Erfolgschancen betragen ungefähr 5.65073810e-9 und 1.47192916e-8.

Alle 2×2-Effekte und positiven Failure-Wurzeln werden auf dem ganzen
\(E=\mathrm{span}(g_0,g_+)\) ausgegeben. Positivität beruht auf der
vorab gültigen Schranke
\(B=264069/1310720<0.202\) beziehungsweise \(2B<0.404\).
Die numerische Rekonstruktion der Wurzel ist ein Konsistenzcheck;
die exakte Instrumentvollständigkeit folgt aus den angegebenen
algebraischen Identitäten, nicht allein aus einem nullhaltigen Intervall.

Weitere Kontrollen: alle 24 geerbten Historien-Relabelings,
Klassennamenaustausch, mittransportierte Analysatorphase bei Rephasierung,
Erhaltung des vollen E-Effekts und gemeinsamer Quellenmultiplikator als
algebraische Kontrolle für feste Uhren. Es wird kein Delta-Uhrenzustand
normalisiert und keine neue Uhrenquadratur vorgetäuscht.

## Schritt 3: zwei terminale Materiemoden

`checks/extended_R.py` verwendet zusätzlich
`checks/r_records_results.json`: die analytisch bestimmten Intervalle
\(a_{f_2,c,s}=\eta_c a_{f_0,c,s}\) mit
\(f_2=[((q_4+q_5)^2-1)/\sqrt2]f_0\).
Die orthogonalen Records f0/f2 sind terminale Materiemoden, keine
umbenannten Plus-/Minusflags. Die direkte kohärente Klassensumme erhält
den vor den neuen Ergebniswerten eingefrorenen Gain \(1/1024\) und
für jedes deklarierte \(\gamma\) ihren eigenen Failure-Effekt.

| Größe bei κ=1 und γ=1 | g0 | gplus |
|---|---:|---:|
| P(f2 gegeben Erfolg), ungefähr | 0.01588644034 | 0.01588896201 |
| Gesamterfolg, ungefähr | 3.58872335e-10 | 9.34808867e-10 |

Der eingeschlossene Quellenkontrast liegt in
\([2.5190715309978,2.5242796555484]\times10^{-6}\).
Er stimmt mit dem unabhängigen Fraction-Audit in `checks/root_R_audit.py`
überein. Die kleine Erfolgschance gehört zur Interpretation dieser
bedingten Wahrscheinlichkeiten.

Bereits der dephasierte Materiedetektor hat einen Quellenkontrast von
etwa 2.3393e-6. Ein positiver Quellenkontrast allein ist daher **kein**
Interferenznachweis. Die Datei gibt zusätzlich die Differenzen zwischen
den kohärenten und dephasierten Verteilungen sowie deren Quellenkontrasten
aus und trennt diese von der Gravitationsphasen-Kontrolle.

Für \(\gamma=0,1/2,1\) wird die CP-Mischung
\(E_\gamma=(1-\gamma)E_0+\gamma E_1\) gebildet. Die uniforme
akzeptierte Schranke ist
\((1+\gamma)548451/3276800\), höchstens 0.3347479248046875.
Alle gemeinsamen (R,I)-Records, ihre R-Marginalen, Offdiagonaleffekte,
Erfolg und Failure sind enthalten.

## Wirkungskontrolle, Voraussetzungen und Abbruch

Die Zusatzrechnung κ=0 entfernt allein die Faktoren \(e^{iF_c}\)
aus den übernommenen Amplituden. Sie ist eine **kontrafaktische
Modelländerung**, kein beobachteter Schalter für Gravitation.
Bei γ=0 bleiben beide Instrumente unter dieser Änderung phasenblind.
Bei γ=1 ist die Änderung der f2-Wahrscheinlichkeit ungefähr 0.00236190
beziehungsweise 0.00236083. Die Differenz der beiden Quellenkontraste
(κ=1 minus κ=0) liegt in
\([-1.075768418171,-1.065714822164]\times10^{-6}\) und schließt null aus.
Damit ist die Mitwirkung der Gravitationsphase **innerhalb dieses neuen
Modells** nachgewiesen; ihre physische Realisierung bleibt eine andere Frage.

Schwächste zusätzlich nötige Voraussetzung für den kohärenten Effekt:
die beiden Klassen müssen in denselben akzeptierten Endkanal gelangen,
ohne perfekt unterscheidenden unbeobachteten Umweltrecord. Die relative
Phase ist mit dem Instrument zu definieren. Vollständige Kohärenz γ=1
ist eine zusätzliche Annahme; die Rechnung bestimmt γ nicht.
θ=0 wurde bereits vorab diagnostisch betrachtet und wird deshalb nicht
als unabhängige blinde Vorhersage bezeichnet. Es gab keine Winkelsuche.

Abbruch der weitergehenden physischen Behauptung, wenn Kohärenz,
Quellenkalibrierung oder eine geeignete geometrische Endobservable nicht
unabhängig begründet werden können. Dann verbleibt ein korrektes
endliches Interferenzmodell; zusätzliche numerische Details schließen
diese begrifflichen Lücken nicht.

## Reproduktion und gegenseitige Prüfung

```bash
python boundary_coherence_v0_1/checks/interference.py
python boundary_coherence_v0_1/checks/extended_R.py
```

Witten hat Instrumentformeln, Gain, CP-Mischung und neue Failure-Effekte
gegengeprüft. Hilbert hat die volle E-Rechnung und die positive
2×2-Wurzelformel geprüft. Dowker liefert die von Quellenvorbereitung und
innerem Stratum unabhängigen Gaußfaktoren. Die unabhängigen rationalen
Root-Audits kontrollieren die numerischen Hauptkontraste. Diese Prüfungen
erhöhen die Nachvollziehbarkeit; sie ersetzen keine physische Kalibrierung.
