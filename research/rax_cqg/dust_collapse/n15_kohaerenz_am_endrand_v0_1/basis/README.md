# Welche Kohärenz trägt die Dichtespur an Ereignis 12?

CST-DUST · N15, Ordnungstyp 2097151 · 25. November 2026 · Anschluss an [PR #372](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/372).

Die gewöhnliche Staubwirkung liefert bei kohärenter Integration von Uhr 4 über das ganze Referenzfenster einen relativen Intensitätsüberschuss der hohen Dichteklasse von 5,6715 bis 6,4996 Milliardstel. Beim getrennten Paketpaar aus PR #372 wechselt das Vorzeichen mit der Kohärenz. Bereits die frühe Dichte an Ereignis 5 kennzeichnet in dieser Präparation das einzelne Uhrfenster eindeutig. Eine zweite, kollektiv verschobene Präparation erlaubt erstmals in dieser Rechnung, die sieben Staubdichten paarweise exakt gleich zu halten. Auch dort entsteht ein Endkontrast. Alle Ergebnisse beziehen sich auf die festgelegte gemeinsame Endauslese, den positiven Referenzsektor und vergleichbaren Eingangsfluss für die beiden Dichteklassen.

## Nachrechnen

Mit Python 3.10 oder neuer im entpackten Ordner ausführen. Die Standardbibliothek genügt.

    python3 -B pruefen.py

`rechnung.py` schliesst die Ergebnisse mit nach aussen gerundeter 256-Bit-Intervallarithmetik ein. `quadratur.py` rechnet getrennt aus allen 50 Paartermen einschließlich der ungekürzten hohen und niedrigen Phasen. `ergebnisse.json` enthält die zertifizierten Grenzen, `gegenrechnung.json` die numerischen Einzelwerte für beide Auflösungen und beide Anfangsdichten 1/8 und 1/4. Die ausgewählten Quellen in `basis/` sind unveränderte Git-Dateien. `Herkunft.json` enthält Commit und SHA-256. Der Prüfer kontrolliert zusätzlich das Paketmanifest und den Zustand aller 60 P3-Prüfpunkte. Der Prüfplan nennt die nachträgliche Erweiterung. Es gab keine externe Vorregistrierung.

## 1. Zwei Fenster mit veränderlicher Kohärenz

Es gelten die zwei getrennten, gleich breiten Uhr-4-Pakete aus PR #372. Ihre Mittelpunkte in Y4 liegen bei C und C+t mit K=15/4, C=−7/4+K/8, D=K(3/722)^(1/4), t=1/(32√D), Halbbreite R=K/2²². Weitere Eingangsbedingungen, Dichtejitter, Uhr-5-Pakete und Endeffekt entsprechen der Ausgangsstudie. Die Anfangsgewichte beider Uhr-4-Fenster betragen je 1/2. Die dimensionslose komplexe Kohärenz γ wird so definiert, dass die Eingangsdichtematrix in der Reihenfolge links/rechts die Diagonale (1/2,1/2) und den Eintrag rechts/links γ/2 hat. Ihre Eigenwerte sind (1±|γ|)/2. Ein gleichphasiger reiner Eingang entspricht γ=1, eine Mischung beider noch in sich kohärenten Fenster entspricht γ=0.

Seien L und R′ die am selben Endpunkt ankommenden komplexen Amplituden. Für jede Dichteklasse σ schreiben wir dσ=∫(|L|²+|R′|²)/2 und cσ=∫L*R′, jeweils mit demselben positiven Endmass. Bis auf einen gemeinsamen Faktor gilt Jσ=dσ+Re(γcσ). Der im Folgenden ausgewiesene Kontrast ist (Jhoch−Jniedrig)/Jniedrig. Der hohe und der niedrige Eingang unterscheiden sich durch die festgelegte Präparation dreier späterer Dichten. Die Angaben sind keine absoluten Ereigniswahrscheinlichkeiten.

| Reeller Wert von γ | Relativer Endkontrast bei festem Referenzprofil, äussere Grenzen |
|---|---:|
| 0 | −5,994 bis −4,543 in 10⁻¹³ |
| 0,001 | +2,058 bis +2,322 in 10⁻¹² |
| 0,1 | +2,412 bis +2,522 in 10⁻¹⁰ |
| 1 | +1,3296 bis +1,3890 in 10⁻⁹ |

Die Differenz der Intensitäten ist exakt affin in Re γ und Im γ. In gemeinsamen Einheiten hat sie die Form a+b Re γ+c Im γ. Das Zertifikat liefert a<0, b>0. Bei bekannter reeller gleichphasiger Kohärenz gibt es genau eine Nullstelle −a/b in [0,000163536648; 0,000225315395]. Die Gegenrechnung ergibt rund 0,0001933. Der kleine Rest bei γ=0 stammt aus den Intensitäten der noch intern kohärenten Pakete. Eine Diagonalisierung jeder einzelnen Feingeschichte ist eine andere Präparation.

Die relative Phase ist ebenfalls messentscheidend. Bei |γ|=1 und γ=exp(iφ) liegt die dem Nullwinkel benachbarte Vorzeichenumkehr zwischen −0,000968 und −0,000925 rad, numerisch bei −0,0009465 rad. Intervallgrenzen für a+b cos φ+c sin φ und seine Ableitung sichern Existenz und Eindeutigkeit in diesem Bereich. Die Schwelle für reelles γ lässt sich daher allein aus |γ| ohne Phasenbezug nicht anwenden.

Ein bedingter Test der Eingangskohärenz kann vier Phasenstellungen am Eingang benutzen. Die normierte Differenz gegenüber der um π versetzten Stellung ist Vθ=Re[exp(iθ) γ cσ]/dσ. Aus V₀ und Vπ/₂ folgt die Grösse |γ||cσ|/dσ. In der niedrigen Klasse liegt |cσ|/dσ zwischen 0,99999952625074 und 1. Die Untergrenze folgt aus Re cσ/dσ, die Obergrenze aus Cauchy-Schwarz. Ein gemeinsamer Eingangsfluss- und Effizienzfaktor kürzt sich bei diesem Test. Eine experimentell kontrollierte Phasenstellung ist eine Voraussetzung.

## 2. Ein früher Dichteeintrag entscheidet über die Kreuzterme

Die normierte Dichte x5=w5/D hat vor dem Jitter das Zentrum f5=(u6−u4)/2. Hier ist u6=3/8 fixiert. Jedes Uhr-4-Fenster hat in u4 Halbbreite 2⁻²². Die Zentren von x5 sind 1/8 und 1/8−t/(2K). Einschliesslich des Dichtejitters ±2⁻²⁰ beträgt der Mindestabstand der beiden Träger mehr als 0,00426807. Die Schwelle 0,122865 trennt die beiden Alternativen für jede präparierte Geschichte, unabhängig von der hohen oder niedrigen späteren Dichte.

Selbst wenn nur für x5 das volle ursprüngliche ±1-%-Dichteband um jedes Profilzentrum zugelassen wird, beträgt der verbleibende Abstand mehr als 0,00181268. Berührung der äussersten Trägerränder erfordert eine relative Halbbreite von rund 1,73767 %. Das ist eine geometrische Trägeraussage für die zwei alten Uhrpakete mit fixierter Uhr 6. Die Intensität wurde mit dem ursprünglichen engen Jitter gerechnet.

Wird an 5 lediglich das binäre Schwellenbit in zwei orthogonale Zustände kopiert und später ungelesen verworfen, multipliziert die partielle Spur den Kreuzterm mit dem Skalarprodukt der beiden Recordzustände, also mit null. Innerhalb eines Fensters bleibt die Kohärenz bei dieser idealen Operation erhalten. Damit liefert ein solcher Record exakt die Mischungszeile in der ersten Tabelle. Wer den vollen kontinuierlichen Dichtewert speichert, kann zusätzlich Kohärenz innerhalb jedes Fensters aufheben.

Das veröffentlichte N15-Hilfsmass integriert innere Felder als Amplituden vor der Endnorm. Unter dieser Paarung wird x5 ohne bleibenden Record summiert. Dass x5 den Fensterindex erkennen lässt, erzeugt allein noch keinen dauerhaft gespeicherten Eintrag. Ein normiertes positives Produktmass gibt die Integrationsgewichte vor. Dieselben Gewichte erlauben zusätzliche Randoperationen mit verschiedenen Kohärenzen. Die physische Auswahl der Eingangskohärenz und die unabhängige Massenkalibrierung sind offen.

## 3. Das volle zusammenhängende Uhrfenster

Für diesen Test wird eine einzelne Uhrbedingung aus PR #372 erweitert. Die Koordinate u4 wird gleichphasig mit flacher Amplitudendichte auf [1/8−1/64,1/8+1/64] integriert. Dabei werden alle früheren Dichtezentren mit dem wirklichen u4 neu berechnet. Die übrigen sechs inneren Uhrpräparationen, die zwei Dichteklassen und der gemeinsame Endeffekt bleiben wie im Ausgangsversuch. Es handelt sich um die volle Breite einer Koordinate im bedingten N15-Versuch.

Bei festem Referenzprofil liegt der relative Endkontrast zwischen 5,6715064 · 10⁻⁹ und 6,4995285 · 10⁻⁹. Die separate Rechnung liefert 6,08563 · 10⁻⁹. Für das ursprüngliche mitlaufende Profil ist er exakt null. Dort ändert der Klassenwechsel jede Feingeschichtsphase um dieselbe Konstante. Diese Null gilt auch für jede gemeinsame Mischung der beiden Uhr-4-Eingangsfenster aus Abschnitt 1.

Für das Zertifikat werden die beiden klassenabhängigen Phasen nach Entfernung der globalen Klassenphase als S±g geschrieben. Am festen Endpunkt setzt man A=E[exp(iS)cos g] und B=E[exp(iS)sin g]. Die Differenz der Intensitäten ist 4(Im A Re B−Re A Im B). Die niedrige Intensität ist |A−iB|². Die Rechnung zerlegt das zusammenhängende Fenster in 1024 gleich gewichtete Intervalle und verwendet je die zwei Uhr-5-Pakete. Alle Einschliessungen gelten gleichmässig für die Enddaten. Analytische gemeinsame Anfangsfaktoren kürzen sich. Die Gegenrechnung integriert über dieselbe kontinuierliche Uhr mit zwei Simpson-Auflösungen, über unabhängige innere und äussere Koordinaten mit gespiegelten Punktfolgen und über uniforme Dichtejitter durch deren exakte sinc-Faktoren.

## 4. Eine Kontrolle mit sieben paarweise identischen Staubdichten

Im ursprünglichen Zweifensterversuch lässt sich das frühe Uhrfenster aus der Dichte ablesen. Für eine zusätzliche Kontrolle wird die zweite Uhrenkonfiguration kollektiv verschoben. Die sieben inneren Ereignisse sind (4,5,6,11,12,13,14). Für sie ist der Versatz in u abwechselnd (+s,−s,+s,−s,+s,−s,+s), mit s=t/K. Alle Uhrpakete liegen vollständig in den zugelassenen ±1/64-Boxen und bleiben geordnet.

Jede innere Zellgrenze ist der Mittelwert zweier Nachbaruhren. Die alternierenden Versätze lassen alle diese Mittelwerte und damit sämtliche Zellanteile f unverändert. Umgekehrt bestimmen identische Zellanteile vom festen linken Rand aus alle Zellgrenzen. Dann muss die Summe je zweier Nachbarversätze null sein. Der alternierende Vektor spannt also den gesamten linearen Verschiebungsraum mit diesem Merkmal auf.

In beiden Armen wird bei jeder gegebenen späteren Dichteklasse derselbe tatsächliche Dichtevektor verwendet, einschliesslich der sieben Jitterkoordinaten und der kleinen Verschiebung an 12,13,14. Diese Verschiebung wird in beiden Armen aus dem unversetzten Partner bestimmt. Die Kontrollpräparation ändert ausdrücklich die gemeinsame Uhren- und Dichteauswahl. Ihre beiden Uhrenzweige besitzen innerhalb jeder Klasse identische positive Verteilungen aller sieben Dichten, auch gemeinsam betrachtet. Das gilt vor der Propagation. Die zwei Dichteklassen selbst bleiben verschieden. Alle Uhren laufen mit ihrem jeweiligen wirklichen Wert durch sämtliche Wirkungsterme.

| Vergleich hohe gegen niedrige Klasse | Relativer Intensitätskontrast, äussere Grenzen |
|---|---:|
| Kollektive Uhrenzweige, gleicher Phasenbezug | −21,462 bis −21,262 Milliardstel |
| Kollektive Uhrenzweige, Mischung beider Zweige | +2,551 bis +3,066 in 10⁻¹² |

Die numerische Gegenrechnung ergibt −21,3619 Milliardstel bzw. +2,8040 · 10⁻¹². Damit kann in der gewöhnlichen Wirkung ein Endkontrast auftreten, obwohl die vorbereiteten Staubdichten zweigweise dieselben sind. Die zusätzlichen Uhren tragen in dieser Präparation selbst Zweiginformation. Die Aussage über Teilkohärenz in Abschnitt 1 und die exakte Null der dortigen mitlaufenden Auswahl gehören zu ihrem jeweils eigenen Präparationsvertrag.

## Quellen und physischer Status

- [Ausgangsstudie auf GitHub, PR #372](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/372)
- [N15-Referenzensemble und inneres Hilfsmass im eingefrorenen Quellstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/0ccd357d9380d09b196dd0d4cf90cbc6a3d253a0/research/rax_cqg/dust_collapse/n15_traeger_uhrzugriff_v0_1/quellen/ensemble.md)
- [Partielle Spur und reduzierte Zustände, J. Watrous, The Theory of Quantum Information, Kap. 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf)

Die 60 physischen P3-Prüfpunkte stehen auf NOT_RUN. Die Resultate vergleichen endliche Referenzpräparationen. Zur physischen Entscheidung braucht es eine Randdynamik oder eine unabhängige Kalibrierung, die den verbleibenden Phasenbezug beziehungsweise einen tatsächlich gespeicherten Record bestimmt.
