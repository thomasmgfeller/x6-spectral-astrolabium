# Rechen- und Layoutvertrag

## 1. Bezugsebenen und notwendige Eingaben

P0: Ausgang von tatsächlicher Quelle und festem Kollimator. P1: feste Referenzebene unmittelbar vor O04 in der nominalen Position, hinter allen Präparations- und Faltoptiken. Bei der Kaustikmessung O04 entfernen. PC: erste Kristallfläche, je Umlaufrichtung getrennt.

Im Tischsystem ist X nach rechts, Y nach oben im Plan und Z vertikal. Draufsicht von +Z. Für jeden Strahl: k ist seine Ausbreitungsrichtung, u = Z × k, v = Z. P1 liegt auf einem +Y-Strahl, daher gilt lokal (x,y,z) = (−X,+Z,+Y). Ein gemessener Hauptachsendrehwinkel und eventuelle u/v-Kopplung müssen explizit angegeben werden.

Pflicht: λ mit Wellenlängenkonvention; D4σ,u/v; M²u/v; signierte Krümmung oder gefittete Taillenlage und -größe; Fit-Kovarianz; Messort und Rohdaten. Ein Radiuswert an nur einer Ebene reicht nicht. Wenn der Pumpvertrag R in mm liefert, wird κ = 1/R gebildet. Nur bei explizit belegter ebener Wellenfront gilt κ = 0; ein fehlender Wert ist kein unendlicher Radius.

Die leere Messstruktur in eingaben.json und das Excel-Blatt Messwerte sind Erfassungshilfen. Die Szenarioberechnung importiert diese Werte nicht automatisch als qualifiziert. Eine Kovarianz bleibt null, solange sie nicht bestimmt ist.

## 2. Gauß- und zweite-Moment-Rechnung

Mit wσ = D4σ/2, Vakuumwellenlänge λ₀ und reduziertem Parameter Q = q/n gilt im skalaren paraxialen Modell

\[
  \frac1Q=\frac nR-i\frac{M^2\lambda_0}{\pi w_\sigma^2},\qquad
  Q_\mathrm{out}=\frac{AQ_\mathrm{in}+B}{CQ_\mathrm{in}+D}.
\]

Für nθ-Strahlkoordinaten:
\[
 P(L,n)=\begin{pmatrix}1&L/n\\0&1\end{pmatrix},\qquad
 F(f)=\begin{pmatrix}1&0\\-1/f&1\end{pmatrix}
\]
für eine dünne Linse in Luft. Bei normaler planarer Grenzfläche bleibt Q stetig. Im Luft-Eingang an P1 ist κ = 1/R und b = M²λ₀/(πwσ²):
\[
 Q_1=\frac{\kappa+i b}{\kappa^2+b^2}.
\]
Eine Verschiebung d der Linse hinter P1 erfordert zuerst Q → Q+d; der geometrische Folgeweg verkürzt sich gleichzeitig um d.

Für den Parameter Qc = a + i b_c in der Kristallmitte:
\[
 w_0=\sqrt{\frac{M^2\lambda_0 b_c}{\pi}},\quad
 w_c=w_0\sqrt{1+(a/b_c)^2},\quad
 \Delta z=-n_c a,\quad z_R=n_c b_c.
\]
u und v werden unabhängig berechnet; M² ist ein Faktor, der nicht nochmals quadriert wird.

Wichtig: Liegt |Δz| außerhalb der halben Kristalllänge, ist dies eine extrapolierte Taille in einem verlängerten homogenen Kristallmedium. Die echte Taille im anschließenden Luftweg erfordert Weiterpropagation durch die reale Austrittsfläche und Folgeoptik. Das Worksheet bezeichnet sie deshalb nicht als physische Luft-Fokusposition.

Das Modell beschreibt zweite Momente. M² und äquivalentes Q enthalten keine vollständige räumliche Feldphase. Daraus wird keine exakte Modenüberlappung, Paarhelligkeit oder Bell-Sichtbarkeit behauptet.

## 3. Geschlossene Pumpgeometrie

PBS0 = (500,410), M1 = (600,410), M2 = (500,510) mm. Der Weg PBS0→M1→M2→PBS0 ist in der Draufsicht CCW; die Gegenrichtung CW. Die geometrische Halbringlänge beträgt h = 100 + 50√2 = 170,710678 mm.

Die duale HWP HD sitzt auf PBS0–M2 bei (500,460). CW durchläuft HD vor der Erzeugung; CCW danach. Sei s der Kristallversatz entlang CCW relativ zum Hypotenusenmittelpunkt. Für die Pumpwege gilt

\[
 B_\mathrm{CW}=c-d+h-s-t_\mathrm{PBS}(1-1/n_\mathrm{PBS})
 -\tfrac L2(1-1/n_c)-t_H(1-1/n_H),
\]
\[
 B_\mathrm{CCW}=c-d+h+s-t_\mathrm{PBS}(1-1/n_\mathrm{PBS})
 -\tfrac L2(1-1/n_c).
\]

c ist der gemeinsame mechanische Weg P1→PBS-Mitte; d die Linsenverschiebung. PBS-Glasweg 10 mm, HWP-Dicke 1 mm, nPBS = 1,53, nH = 1,55, nK = 1,85 sind Platzhalter. Die PBS-Dicke ist der gesamte durchlaufene Glasweg, auch beim intern reflektierten Zweig; der Mittelpunkt im Plan liegt auf der internen Fläche.

Mit
\[
 s=-\tfrac12t_H(1-1/n_H)=-0,177419\ \mathrm{mm}
\]
werden die reduzierten Wege gleich. Die daraus folgende Kristallposition ist (550,125454; 459,874546) mm. Der gemeinsame Weg c = 72,212265 mm bringt beide Taillen im Beispiel auf die Kristallmitte. O04 liegt bei (460;377,787735) mm; DM bei (460;410) mm.

Für CW muss bei einem gemeinsamen Ortsvergleich das Vorzeichen von Δz umgekehrt werden. Die Differenz zwischen den beiden Taillen ist daher |ΔzCW + ΔzCCW|, nicht die Differenz der lokalen Werte.

**Nicht verwechseln:** B enthält L/n, die optische Phase dagegen nL. Gruppenlaufzeit und spektrale Phase benötigen ng sowie alle Beschichtungs- und Retardanzbeiträge. Gleiche Fokuslage beweist keine spektrale oder zeitliche Ununterscheidbarkeit.

## 4. Optikrichtungen und Polarisation

PBS0-Ports: P1 West, P2 Ost, P3 Nord, P4 Süd. H wird ideal transmittiert, V intern reflektiert. Port P1 wird für Pumpeingang und Photonenausgang A genutzt; DM reflektiert 405 nm aus Süden nach Osten und transmittiert den westwärts laufenden 810-nm-Arm. Ausgang B liegt an P4. DB transmittiert 810 nm nach Süden und reflektiert verbleibende Pumpe zum östlichen BD1.

| Umlauf | Eingang am PBS | Bis zur Erzeugung | Nach Erzeugung | Vor Analysator A/B |
|---|---|---|---|---|
| CCW | H → P2 | M1 → K, H-Pumpe | Hs/Vi → M2 → HD: Vs/Hi → P3 | Vs in A, Hi in B |
| CW | V → P3 | HD: V→H → M2 → K | Hs/Vi → M1 → P2 | Hs in A, Vi in B |

Dieser ideale Portvertrag ordnet Signal in beiden Alternativen A und Idler B zu. Native Kristallachsen im Entwurf: Xc entlang CCW-Diagonale, Zc vertikal, Yc = Zc × Xc. H entspricht lokal Yc, V Zc. Die tatsächliche Typ-II-Wechselwirkung, Pumpachse und RFQ-Achsen müssen vom Lieferanten bestätigt werden.

HD-Fast-Axis als Ausgangspunkt 45° zwischen H und V; erforderliche Retardanz π modulo 2π bei beiden Wellenlängen. Slow-Axis orthogonal. Reale Vorzeichen, Nullpunkte und spektrale Phasen müssen kalibriert werden. HP und QP präparieren den gemessenen Stokes-Zustand an P1; es gibt keine vorausgesetzten Motorwinkel. Die beiden nachfolgenden Faltspiegel sind Teil dieses Stokes-Transfers.

Je Analysearm QWP → HWP → PBS. T ist nominal +, R nominal −. Für lineare Analyse und kalibrierte neutrale QWP ist θHWP = α/2 ein Startvertrag; die CHSH-Analysewinkel sind keine ungeprüften Motorbefehle. PBS B besitzt eine andere interne Flächennormale als PBS A, damit der reflektierte Strahl nach Osten läuft.

Die Aufspaltung der H/V-Amplituden und die Phase werden so kalibriert, dass a|HV⟩ + b exp(iφ)|VH⟩ dem Zielzustand entspricht. Die Tabelle ersetzt keine komplexen Jones-Matrizen gemessener PBS-/HWP-/Spiegelphasen.

## 5. Maßstab, Halter und Justage

800 × 600 mm ist eine Planungsfläche, keine bestätigte vorhandene Grundplatte. Strahlhöhe 75 mm. Alle XYZ beziehen sich auf optische Haupt- beziehungsweise Bezugsflächen. Linsenfassung, PBS-Gehäuse und Ofenmittelpunkt können davon abweichen.

SVG: 594 × 420 mm mit viewBox 1188 × 840. Eine Koordinateneinheit für 1 mm am Aufbau wird als 0,5 mm gedruckt: 1:2. Drucker-Skalierung kontrollieren. Die Radien der gezeichneten Strahlen sind aus Darstellungsgründen nicht maßstäblich.

M1/M2 haben nominell 22,5° AOI, nicht die oft pauschal angenommenen 45°. Pump-Faltspiegel und Dichroika: 45°. Normale Eintrittsflächen an Kristall, Linsen und Wellenplatten: 0°. PBS-Außenflächen: 0°, interne Trennfläche: 45°. Koordinatenliste enthält die Azimute der reflektierenden Flächennormalen; die Reflexionsgesetze werden automatisch geprüft.

Gestrichelte 26-mm-Quadrate sind reservierte Flächen, beim Ofen 40 mm, bei der Quelle 36 mm. Sie sind keine behaupteten Halterabmessungen. Die Reservierungen überlappen nominell nicht; Fasern und zugehörige letzte Linse gehören jeweils zu einer integrierten Kopplerbaugruppe. Reale CAD-Hüllen samt Schrauben, Kabeln und Temperaturanschlüssen fehlen.

Justage: Ring von oben zugänglich halten; M1/M2 kinematisch, O04 axial ±10 mm als Planungsreserve, Ofen lateral/axial, vier Faserbaugruppen mit x/y/z und Tip/Tilt. Die tatsächliche Verstellbarkeit, Werkzeugzugänge, Aperturen und Zugänglichkeit nach Einhausung bleiben OPEN. Die Quellfläche ist im Plan markiert; sie ist keine geprüfte Kollisionsfreigabe.

Rücklauf an DM geht zur Pumpstrecke zurück. ISO/BD0 reservieren den Isolation-/Dump-Pfad; dessen konkrete Richtung, Rückflussverträglichkeit und Isolation hängen vom Modell ab. BD1 nimmt den ausgekoppelten Pumpanteil aus Arm B auf. Streulicht, Mehrfachreflexe und Restpumptransmission müssen zusätzlich am Aufbau geprüft werden.

## 6. Vier Sammelpfade

Der bisherige ideale 160/5-mm-Relaiskandidat lässt sich mit dieser Halbringlänge nicht als externe 4f-Stufe unverändert positionieren. Neuer **Platz- und Rechenkandidat**: f1 = 250 mm, f2 = 8 mm, rückprojizierter Sammelradius 80 µm, angenommener Faser-MFD 5,0 µm.

Die ideale reduzierte 4f-Matrix ist diag(−f2/f1,−f1/f2). Sie ergibt einen Bildradius 2,56 µm, verglichen mit 2,50 µm Faser-Modenradius. Der isolierte Größenüberlapp ist 0,999438. Dies ist keine absolute oder gemessene Kopplungseffizienz.

Im Entwurf sitzt die erste Linse vor dem Analysator und die letzte Linse in jedem der vier Ausgänge. Es handelt sich daher um zwei gemeinsame Sammellinsen und vier letzte Koppler. Die übertragene Polarisation jeder gemeinsamen Linse und jedes Filterpakets muss geeignet sein.

Die eingetragenen Koordinaten verwenden als skalaren Startwert nK = 1,80 bei 810 nm, nPBS = 1,51 und den mittleren HD-Beitrag; der Analysator-PBS wird als 10-mm-Glasweg berücksichtigt. Transmittierte Dichroika bei 45°, Filter- und Wellenplattendicken, anisotrope Beugung, individuelle y/z-Indizes, tatsächliche Hauptflächen, Modenfeld und NA fehlen. Beide Erzeugungsalternativen müssen jeweils auf dieselbe Faser rückprojiziert werden. Diese 810-nm-Rechnung ist **noch nicht geschlossen** und ist keine Beschaffungsvorgabe.

## 7. Budget und Freigabelogik

Sweeps werden bei festem restlichem Aufbau gerechnet, keine automatische Nachjustage. D ±5 %, M² ±0,1, f ±1 %, O04 ±1 mm sind gewählte Störgrößen. ±0,001 mm⁻¹ Krümmung zeigt ausdrücklich einen großen R = ±1 m-Stressfall; das kombinierte Raster benutzt ±0,0002 mm⁻¹. Für nK werden ±0,05 gescannt. Keine dieser Grenzen ist bereits eine zulässige Fertigungs- oder Betriebstoleranz.

Bei gemessenen Werten y = g(x) wird zunächst JΣJᵀ gerechnet und mit korrelierten nichtlinearen Szenarien gegengeprüft. Fitparameter von Radius, Taille, M² und Krümmung sind nicht gleichzeitig als voneinander unabhängige Eingaben anzusetzen. Ein gemeinsamer Material- oder Linsenfehler ist über CW/CCW korreliert.

Eine vollständige Freigabe verlangt: verifizierte Pumpe, geeignete Kaustik, Materialien und Hauptflächen; toleranzbehaftete Radien in beiden Achsen; definierte zulässige Fokus-/CW-CCW-Abweichung aus dem Kopplungsbudget; freie Aperturen; reale Komponenten-Hüllen; vollständige Polarisations- und 810-nm-Ausbreitung. Die Suchspanne 100–180 µm und ein nominaler Fokus innerhalb des Kristalls reichen dafür allein nicht.

VERIFIED ist nur für die jeweils benannte dokumentierte oder numerisch geprüfte Eigenschaft zulässig. Messungen bleiben NOT_RUN; konkrete fehlende Lieferdaten OPEN; von ihnen abhängige O04-, Montage- und BOM-Freigabe HOLD.

## Quellen und Bezug

- Projektbasis: Pump-Eingangsprofil v0.1 und Optikplan v0.2, Commit 10153372a97123a6106af22130993da8292cb2db.
- S. A. Self, „Focusing of spherical Gaussian beams“, Applied Optics 22, 658–661 (1983), https://doi.org/10.1364/AO.22.000658. Hintergrund der Gauß-Fokusrechnung.
- Herstellererläuterung zu Gaußstrahlen und Linsen: https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=12211 . Dient der Konventionsprüfung, nicht als Datensatz für vorhandene Hardware.
- T. Kim, M. Fiorentino, F. N. C. Wong, „Phase-stable source of polarization-entangled photons using a polarization Sagnac interferometer“, Physical Review A 73, 012316 (2006), https://doi.org/10.1103/PhysRevA.73.012316. Architektur und idealer Polarisationsvertrag.
- Die vorliegende Zeichnung, Annahmen, Koordinaten, Reduktionsrechnung und Toleranzbeispiele wurden neu erstellt. Literaturwerte für tatsächlich gemessene Quellenleistung oder Sichtbarkeit werden nicht auf unseren Entwurf übertragen.
