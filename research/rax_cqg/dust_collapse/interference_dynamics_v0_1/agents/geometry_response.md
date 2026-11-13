# Geometrische Quellenantwort: unabhängiger Bedeutungs- und Identitätsaudit

Die beiden N11-Ordnungen erlauben eine konkrete intrinsische Geometriefrage unter demselben äußeren Rand. Die Auswertung benötigt die **vollständigen integrierten Gewichte**, weil eine relative Wirkungsphase allein keine Änderung der klassenaufgelösten Geometrieverteilung bestimmt. Dieser Audit leitet die Formel her, prüft ihre Voraussetzungen und wertet die vorhandenen vollständigen N160-Gewichte aus. Bei ausdrücklich gleichen Historiengewichten ergibt sich numerisch E_res=2,47359 beziehungsweise 2,34746. Das ist eine bedingte Randparameterantwort eines auflösenden Hilfsinstruments, keine bereits hergeleitete physikalische Geometriedynamik.

## 1. Fest definierte Geometrie, veränderliche Quelle

Der äußere Dirichletrand ist B={0,1,2,3,7,8,9,10}; I={4,5,6} ist das innere Gebiet. C0 ist die elfgliedrige Kette. C1 entsteht aus deren transitiver Relationsmenge durch Entfernen ausschließlich von (4,5) und (5,6), während (4,6) erhalten bleibt. Beide Mengen sind transitiv. Der Audit bestätigt alle 28 gemeinsamen B–B-Relationen und alle 24 gemeinsamen B–I-Relationen.

Als geometrische Größe dient

\[
O(C)=\#\{(x,y)\in I^2:x\prec_C y\}.
\]

Damit gilt O(C0)=3 und O(C1)=1. Die Werte bleiben unter jeder Umnummerierung der inneren Elemente und allgemeiner bei Transport des markierten Gebiets I unverändert. Die Beschränkung auf I ist Teil des gemeinsamen Rand-/Gebietsvertrags, keine absolute Bedeutung der Zahlenlabels 4,5,6.

Die intrinsischen Pastanzahl-Filtrationen N_k=|{x:|Past_C(x)|≤k}| sind ebenfalls verschieden:

| Ordnung | N_k, k=0,…,10 |
| --- | --- |
| C0 | (1,2,3,4,5,6,7,8,9,10,11) |
| C1 | (1,2,3,4,6,7,7,8,9,10,11) |

Der Quellenvergleich ρ=1/8 versus ρ=1/4 verändert die **festen äußeren Dichtewerte**, nicht diese beiden Ordnungen. Beide Quellen liegen im gemeinsamen Bereich 0<ρ<1/2 der bekannten positiven stationären Zeugen. Dabei wird ρ an sämtlichen acht B-Knoten geändert, also auch am späteren Rand. Der Vergleich ist deshalb zunächst eine **beidseitige Dirichlet-Randparameterantwort**, keine isolierte Variation einer Anfangsquelle bei festem späterem Messfilter. Sie ist keine Entwicklung in verstrichener Zeit. ρ ist ohne weitere Kalibrierung auch keine physikalische Masse.

Die gemeinsame neue Uhrbox ist [−3/2,3/2]. Sie enthält die zentrierten stationären Zeugen mit Δ²=√6/38, denn die maximale quadrierte Randuhr ist 25√6/38<9/4. Im vollständigen Integral wird **keine zusätzliche Ordnungs-Thetafunktion** eingeführt. Deshalb enthält die Box weiterhin nichtmonotone Uhren. Die Vergrößerung gegenüber dem alten Sechshistorienpilot wird ausdrücklich als neuer Träger deklariert, nicht als dort bereits vorhandene Eichfixierung.

## 2. Exakte geometrische Antwort für aufgelöste Records

Schreibe die beiden vollständigen Amplituden als

\[
a_c(\rho)=A_cW_c(\rho),\qquad c=0,1.
\]

A_c=ω_c g_c enthält ausschließlich das feste Historiengewicht und die ρ-unabhängige skalare Gauß-/Fresnel-Konstante. **W_c enthält bereits exp(iF_c)** sowie die vollständige innere Dirichlet-/Uhrboxintegration mit ursprünglichem innerem Atom-plus-Positivmaß und sämtlichen Randdichtephasen. Es wird keine zusätzliche Gravitationsphase vorangestellt. Ein nur am Sattel ausgewertetes exp(iS_c) ersetzt W_c nicht.

Für ein Instrument, das die beiden Geometriealternativen tatsächlich durch getrennte Records auflöst, lautet die auf Erfolg bedingte Größe

\[
\mathbb E_{\rm res}[O\mid\mathrm{Erfolg},\rho]
=\frac{3|a_0(\rho)|^2+|a_1(\rho)|^2}
{|a_0(\rho)|^2+|a_1(\rho)|^2}.
\]

Eine gemeinsame Annahmeverstärkung bzw. ein gemeinsamer Akzeptanzfaktor kürzt sich hier heraus. Die Formel konstruiert jedoch weder diesen Faktor noch eine gesamte Erfolgswahrscheinlichkeit oder einen physikalischen Failure-Kanal.

Für a0≠0 definiere das **relative Intensitätsgewicht**

\[
\Lambda(\rho)=\left|\frac{a_1(\rho)}{a_0(\rho)}\right|^2
=\left|\frac{A_1}{A_0}\right|^2
 \left|\frac{W_1(\rho)}{W_0(\rho)}\right|^2.
\]

Im Prüfcode heißt dieses Symbol `lambda_intensity`; es ist kein Instrument-Gain. Dann

\[
\mathbb E_{\rm res}O=\frac{3+\Lambda}{1+\Lambda},\qquad
1\leq\mathbb E_{\rm res}O\leq3.
\]

Wo beide W_c ungleich null und differenzierbar sind, folgt exakt

\[
\frac{d}{d\rho}\mathbb E_{\rm res}O
=-\frac{4\Lambda}{(1+\Lambda)^2}
\frac{d}{d\rho}\log\left|\frac{W_1}{W_0}\right|.
\]

Die Änderung des relativen **Betrags** entscheidet also über die aufgelöste geometrische Antwort. Eine Änderung ausschließlich der relativen Phase kann diese Größe nicht ändern. Für die beiden festgelegten Quellen ist die endliche Differenzformel zweckmäßiger:

\[
E_{1/4}-E_{1/8}
=\frac{2(\Lambda_{1/8}-\Lambda_{1/4})}
{(1+\Lambda_{1/8})(1+\Lambda_{1/4})}.
\]

Diese Identitäten wurden symbolisch geprüft, nicht nur formuliert. An einem Nullpunkt einer einzelnen Amplitude bleibt die direkte Intensitätsformel gültig: a1=0 ergibt E=3, a0=0 ergibt E=1. Wenn beide verschwinden, ist die Bedingung auf Erfolg undefiniert. Die logarithmische Ableitungsformel wird an solchen Nullpunkten nicht verwendet.

## 3. Kohärente Alternativen sind ein anderer Messvertrag

Für gemeinsamen terminalen Ausgang und festen Umweltüberlapp γ ist das akzeptierte Gewicht proportional zu

\[
|a_0|^2+|a_1|^2+2\operatorname{Re}(\gamma a_0a_1^*).
\]

Bei γ=1 sind die beiden ungemessenen Geometriealternativen im Allgemeinen nicht konsistent als klassische Alternativen. Die hierfür relevante Additivitätsbedingung ist Re(γa0a1*)=0. Die tatsächliche numerische Auswertung unten liefert für beide Quellen einen deutlich nichtnulligen Additivitätsdefekt. Ihre Rundungsqualifikation wird dabei nicht zu einer rigorosen Einschließung aufgewertet.

Das Einfügen eines auflösenden Geometrieregisters liefert gerade die oben definierte klassenaufgelöste Verteilung. Als reduzierter gemeinsamer Ausgang entspricht das γ=0. Es ist ein veränderter Instrumentvertrag; die unveränderte kohärente Interferenzmessung darf nicht gleichzeitig so interpretiert werden, als wären die beiden Geometrien darin bereits klassisch aufgelöst. Das schließt kohärente Superpositionen in einem ausdrücklich konstruierten Geometrieregister nicht aus; dort wäre O diagonal, während komplementäre Messungen andere Informationen auslesen.

Die kohärente gewichtete Amplitudenratio

\[
O_{\rm amp}=\frac{3a_0+a_1}{a_0+a_1}
\]

ist keine Born-Erwartung von O. Sie ist nur für a0+a1≠0 definiert und kann komplex sein oder außerhalb [1,3] liegen. Zwei exakt geprüfte **synthetische Gegenkontrollen**, keine Ergebnisse der ursprünglichen W-Integration:

- a0=1, a1=i ergibt O_amp=2−i.
- a0=1, a1=−1/2 ergibt O_amp=5.

Zusätzlich prüft der Code, dass die ausschließlich phasenverschiedenen Beispiele (a0,a1)=(1,1) und (1,−1) beide den aufgelösten Mittelwert E=2 besitzen, während das kohärente Gewicht 4 beziehungsweise 0 beträgt. Damit wird die Verwechslung zwischen Interferenzantwort und aufgelöster Geometrieantwort ausdrücklich abgefangen.

## 4. Ausgeführte numerische Quellenkontrolle

Der Audit liest ausschließlich die Ergebnisse desselben Pakets aus `checks/full_weight/results.json` und `checks/scalar_response/results.json`. Er startet deren Integrationen nicht erneut. Die verwendeten Dateien werden im Ergebnis mit SHA-256 identifiziert. Gewählt wird ausdrücklich ω0=ω1=1. Das ist eine transparente endliche Kontrollkonvention, keine Herleitung des physikalischen Historienmaßes.

Mit dem berechneten skalaren Verhältnis g1/g0≈0,3297873431+0,1726821549i und den vollständigen N160-Gewichten erhält man:

| Quelle ρ | Λ=|g1 W1/(g0 W0)|² | Aufgelöstes E_res[O] | dE_res/dρ |
| --- | ---: | ---: | ---: |
| 1/8 | 0,3572261045 | 2,4735938200 | −0,6937849162 |
| 1/4 | 0,4842698347 | 2,3474638865 | −1,3184399340 |

Die numerische Differenz E_res(1/4)−E_res(1/8) beträgt **−0,1261299336**. Der größte beobachtete Unterschied dieser Mittelwerte zwischen den gespeicherten Quadraturordnungen 64,96,128,160 beträgt rund 7,11×10⁻¹⁵. Die direkte Ableitung des Intensitätsquotienten und die oben hergeleitete logarithmische Formel stimmen numerisch überein.

Die Kontrolle, die jedes W_c durch W_c/|W_c| ersetzt und sämtliche tatsächlichen Phasen sowie g_c erhält, ergibt dagegen an beiden Quellen E_res≈2,7565758012: Der Quellenkontrast verschwindet. Friert man nur beide W-Beträge auf ihre Werte bei ρ=1/8 ein und behält weiterhin ihre jeweiligen Phasen, bleibt E_res≈2,4735938200 ebenfalls konstant. Diese beiden Ablationen sind algebraische Diagnosen, keine aus der Wirkung hergeleitete Entkopplung. Sie zeigen, dass der hier berechnete aufgelöste Kontrast aus einer Änderung der relativen Beträge stammt und nicht aus einer bloßen relativen Phasenverschiebung.

Die kohärente Ratio liefert stattdessen O_amp≈3,64414−1,80001i beziehungsweise 4,73314−2,69479i. Der auf |a0|² bezogene Additivitätsdefekt 2Re(a1/a0) beträgt ungefähr −0,96628 beziehungsweise −1,29557. Die hypothetische klassenaufgelöste Geometrieverteilung und die kohärente Auslese sind somit auch in diesen tatsächlich ausgewerteten Daten deutlich unterschiedliche Verträge.

**Numerische Reichweite:** Diese Zahlen sind Float64-Diagnosen aus den vollständigen Gewichtsintegralen, kombiniert mit einem zuvor hochpräzise berechneten skalaren Faktor. Die analytischen Quadratur-Trunkationsschranken decken die Gleitkommaauswertung nicht mit ab. Die Differenz ist numerisch stabil, aber hier nicht durch ein vollständiges Intervallzertifikat eingeschlossen. Die Werte sind keine physikalischen Zählraten, und eine Abnahme von O ist keine Aussage über räumliche Kontraktion oder einen Bounce.

## 5. Ergebnisstatus und verbleibende Bedeutungsebenen

Der ausführbare Audit `checks/geometry_response/check.py` besteht mit 19 Kontrollen. Er prüft die beiden transitiven Ordnungen, gemeinsame Randinzidenzen, sämtliche sechs inneren Umnummerierungen, das geometrische Spektrum, die Ableitungs- und Differenzidentität, den Wertebereich, Gegenkontrollen und die zusätzliche numerische Auswertung der tatsächlich gespeicherten W-Werte. `numeric_response.py` berechnet die Quelle-zu-Geometrie-Diagnostik als eigenen nachvollziehbaren Auswertungsschritt.

| Ebene | Was dieser Audit trägt |
| --- | --- |
| Intrinsische Geometrie | O=3 versus 1 und unterschiedliche N_k sind exakt definiert und relabelinvariant. |
| Vollständige Quellengewichte | Zahlen stammen aus der gemeinsamen W-Integration; Trunkation ist analytisch begrenzt, Float-Auswertung nicht vollständig zertifiziert. |
| Aufgelöste Randparameterantwort | Numerisch −0,1261299336 für E_res bei gleichen Historiengewichten. Gehört zum auflösenden Recordvertrag und ändert beide äußeren Dichteränder. |
| Kohärente Interferenzantwort | Gehört zum gemeinsamen Ausgang; allein daraus folgt keine klassische Geometrieverteilung. |
| Physikalische Geometriedynamik | Benötigt zusätzlich begründetes Maß/Paarung, physikalisches Instrument bzw. Historiendeutung, Quellen- und Uhrkalibrierung sowie Zusammensetzung. |
| Staubball-Kollaps | Benötigt darüber hinaus räumliche/zeitliche Skalierung, Außenraum und kontrollierte Korrespondenz/Verfeinerung. |

Eine eventuell berechnete Änderung von E_res ist deshalb ein konkreter endlicher geometrischer Quellenbefund unter deklariertem Instrumentvertrag. Sie ist weder eine zeitliche Kollapskurve noch allein ein Nachweis gravitativer Rückwirkung in einem physikalischen CST-Zustandsraum.
