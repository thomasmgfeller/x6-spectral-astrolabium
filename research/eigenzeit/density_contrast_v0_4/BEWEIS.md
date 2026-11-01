# Geometrie und unbekannte Beprobungsdichte bei fester Ereigniszahl

## Beobachtung und Aussagen

Die Modellfamilie aus v0.3 besteht aus Metriken g_h=(1-ht)^(-2)η auf dem
vollständigen 4D-Diamanten |t|+|x|<1/2, 0≤h≤1/2. Bei fester Ereigniszahl
N werden Punkte unabhängig gezogen. Die Spitzen des Diamanten sind keine
zusätzlichen Ereignisse. P_h bezeichnet das normierte physische
Vierervolumengesetz. Der wirkliche Probenprozess hat Einpunktgesetz Q=f P_h
mit positivem f, E_h f=1 und

    ess sup f / ess inf f ≤ K.

K ist der vor der Auswertung von außen begründete maximale Kontrast. K=1,002
bedeutet, dass das dichteste Gebiet gegenüber dem dünnsten höchstens 0,2 %
mehr Punkte pro physischem Volumen liefert. Eine räumlich konstante
Multiplikation der Intensität fällt bei festem N heraus. Gemeint sind weder
eine ±0,2-%-Abweichung um den Mittelwert noch eine bloße Durchschnittsvorgabe.
Spitzen oder Bereiche ohne Beobachtungsmöglichkeit sind durch diesen
begrenzten positiven Kontrast nicht automatisch abgedeckt. Unter zwei
verschiedenen Modellhypothesen sind verschiedene zulässige f erlaubt. Die
gemeinsame beobachtbare Größe ist ausschließlich die unbeschriftete strikte
Ordnung; im praktischen Verfahren wird eine einzige unabhängige Gruppierung
hinzugenommen.

Die Rasterparameter sind h=0,1/4,1/2. Gesucht sind mindestens 95 % Einschluss
jedes wahren Rastermodells und mindestens 80 % korrekte Einzelausgabe für
jedes Rastermodell. Zusätzlich soll das ausgegebene Krümmungsintervall bei
jedem festen h in der ganzen Familie zu mindestens 95 % überdecken.
q=RT²=48 atanh(h/2)². Alle Wahrscheinlichkeiten beziehen sich auf eine neue
Ordnung und ggf. ihre unabhängige Gruppierung, vor jeder Auswahl sichtbarer
Ergebnisse. Die Garantien sind uniform über alle zulässigen f.

## 1. Exakte Dichtezwillinge

Die in v0.1 bewiesene kausale Umparametrisierung bringt alle Kandidaten auf
denselben Diamanten. In der ausgerichteten Karte schreibe
S=4(t²-|x|²)∈[-1,1], s_h=1-h²/4 und δ_h=(1-√s_h)/(1+√s_h).
Die physische Dichte relativ zum flachen normierten Volumen ist

    D_h(S)=(1-δ_h S)^(-4)/Z_h.

Die Kausalrelation ist für alle so dargestellten Modelle dieselbe.
Der Übergang zu den ursprünglichen Nullkoordinaten t±|x| geschieht durch
die gleiche steigende Möbiusfunktion F_k(v)=(v+k/4)/(1+kv),
k=h/(1+√s_h), bei beibehaltener Raumrichtung. Diese bijektive konforme
Abbildung erhält die ganze zeitgerichtete Ordnung.

Für h_i<h_j ist D_j/D_i monoton in S. Nach Kürzen der Normalisierungen
beträgt der Quotient seiner wesentlichen Extremwerte genau

    K_einseitig(i,j)
        = [((1+δ_j)(1-δ_i))/((1-δ_j)(1+δ_i))]^4
        = (s_i/s_j)².

Beliebig kleine Umgebungen der Extremwerte haben positive Volumenmasse.
Wenn j volumengleichmäßig beprobt wird, kann i mit f_i=D_j/D_i
dasselbe Punktgesetz erzeugen. Für flach gegen h=1/4 beträgt der
Dichtequotient 4096/3969, also rund 3,1998 % Unterschied vom Minimum
zum Maximum. Die zugelassene Dichtestörung ist eine Raumzeitfunktion.
Für eine unabhängig vorgeschriebene spezielle Form von f, etwa ausschließlich
zeitabhängig in einer bestimmten Uhr, wird hier kein solches Minimum behauptet.

Dürfen beide Seiten von ihrer jeweiligen homogenen Beprobung abweichen, ist
die normierte geometrische Mitte M ∝ √(D_i D_j) ein gemeinsames Zielgesetz.
Die Gewichte f_i=M/D_i und f_j=M/D_j haben beide Kontrast s_i/s_j. Umgekehrt
erzwingt ein **gemeinsames Punktgesetz in dieser festgelegten Karte**
D_j/D_i=f_i/f_j. Der Kontrast der rechten Seite ist höchstens K². In dieser
Karte ist der kleinste beidseitige Kontrast für exakt diese Übereinstimmung
daher K=s_i/s_j. Für das Beobachtungsexperiment liefert dies eine hinreichende
Unmöglichkeitsschwelle. Gleiche Ordnungsgesetze über andere Kopplungen unterhalb
dieser Schwelle sind dadurch nicht ausgeschlossen.

| Vergleich h_i, h_j | Nur schwächeres Modell verzerrt | Beide Modelle dürfen verzerrt sein |
|---|---:|---:|
| 0 und 1/4 | 4096/3969 | 64/63 |
| 0 und 1/2 | 256/225 | 16/15 |
| 1/4 und 1/2 | 441/400 | 21/20 |

Ziehe N iid Punkte einmal aus dem gemeinsamen Gesetz. Die beiden
physikalischen Interpretationen ergeben punktweise dieselbe Ordnung. Damit
stimmen die Ordnungsgesetze für **jedes N und jede Ordnungsobservable** überein.
Bei einem Rasterverfahren mit höchstens 5 % wahrer Verwerfung je Modell
kann die Ausgabe „nur i“ unter i dann höchstens 5 % haben, weil sie unter j
mit derselben Wahrscheinlichkeit j verwirft. Entsprechendes gilt für „nur j“.
Beide Modelle bleiben gemeinsam mit Wahrscheinlichkeit mindestens 90 % erhalten.
Für zwei kontinuierliche Parameter mit gleichem Gesetz muss jedes Intervall
mit 95 % Überdeckung je Modell mit mindestens 90 % Wahrscheinlichkeit beide
Parameter enthalten. Dies folgt jeweils direkt aus der Vereinigungsabschätzung.

Schon bei K=1,002 lässt sich flach beidseitig mit dem Parameter h* mit
(h*/2)²=1-1/K koppeln. Die q-Differenz beträgt mindestens 0,095936068179.
Folglich muss jedes für die ganze Störklasse ehrliche 95-%-Intervall unter
diesem gemeinsamen Gesetz mit mindestens 90 % Wahrscheinlichkeit mindestens
diese Breite haben, unabhängig von N. Dieser Anspruch ist für ein bestimmtes
Zwillingsgesetz bewiesen, nicht für jeden wahren Parameter und jedes f.
Für große K wird (h*/2)² auf den Modellrand 1/16 begrenzt. Die Rechnung
schließt 48 z (Σ_j z^j/(2j+1))² rational mit positivem geometrischen Rest ein.

## 2. Notwendiges Budget vor der exakten Kollision

Für K<s_i/s_j kann Modell i ein homogenes Modell mit s'_i=s_i/√K nachahmen,
Modell j eines mit s'_j=s_j√K. In jedem Fall kostet die Quotientendichte
gerade K. Die beiden neuen homogenen Gesetze liegen näher beisammen und sind
zulässige Fälle der ursprünglichen beiden zusammengesetzten Hypothesen.
Das ist eine explizite schwierige Teilaufgabe, keine Optimierung über alle f.

Ihre Einpunkt-Affinität A wird mit den rationalen Nullkoordinatenmomenten aus
v0.1 eingeschlossen. Dazu werden s' und die zugehörigen δ nach außen gerundet
und die positiven Normalisierungsintegrale sowie der Mischterm mit ihren
Reihenresten abgeschätzt. Der übergebene Code cross() liefert für das
Affinitätsquadrat eine Untergrenze L. Für N iid Punkte ist die Affinität A^N.
Der Übergang zu den Kategorien „nur i“, „nur j“ und „übrige“ kann diese
Affinität nicht verringern (Cauchy-Schwarz auf jeder Kategorie, unabhängige
Zusatzrandomisierung erlaubt). Für ein erfolgreiches Verfahren müssen die
ersten beiden Kategorien in entgegengesetzten Richtungen mindestens 0,80 und
höchstens 0,05 aufweisen. Die Summe der beiden Terme der quadrierten
Hellinger-Differenz enthält dann mindestens (√0,80-√0,05)²=9/20.
Also A^N≤11/20 und notwendigerweise L^N≤121/400. Die rational nach unten
gerundete Potenz wird ganzzahlig bis zur letzten sicher ausgeschlossenen
Ereigniszahl verglichen. Eine separate 80-stellige Rechnung prüft die
23 endlichen Fallgrenzen mit 39 statt 13 Reihentermen.

Für flach gegen schwach ergeben sich beispielsweise 285099 notwendige
Ereignisse bei K=1,002, 913670 bei K=1,0081 und 1603478 bei K=1,01. Somit
kann bei 1 % unbekanntem Kontrast selbst ein Test der gesamten Ordnung mit
900000 Ereignissen das gemeinsame 80/95-Ziel nicht sichern. Die hinreichende
Ereigniszahl ist aus einer notwendigen Schranke allein nicht bestimmbar.

## 3. Kontrollierte Änderung des mittleren Paaranteils

Seien G(x,y) die binäre Vergleichbarkeit, p=E_P G, r(x)=E_P[G(x,Y)|x],
v=Var_P r(X) und H(x,y)=G(x,y)-r(x)-r(y)+p. Setze u=f-1. Für a=ess inf f,
b=ess sup f gilt a≤1≤b≤Ka. Aus E[(f-a)(b-f)]≥0 folgt
E u²≤(b-1)(1-a)≤(Ka-1)(1-a)≤(K-1)²/(4K). Der letzte Schritt maximiert
die quadratische Funktion in a. Schreibe η=(K-1)/(2√K).

Mit E_P u=0 und unabhängigen Punkten ist die Verschiebung der
Paarwahrscheinlichkeit exakt

    p_Q-p = 2 E_P[u(X)(r(X)-p)] + E_(P⊗P)[u(X)u(Y)H(X,Y)].

Der Rest H ist zu beiden Punktprojektionen orthogonal. Seine Varianz ist
p(1-p)-2v. Zweimal Cauchy-Schwarz liefert

    |p_Q-p| ≤ 2η√v + η²√(p(1-p)-2v).

Für das Zertifikat wird v im ersten Term nach oben und im zweiten nach unten
abgeschätzt. Die stetigen Grenzen von p und v stammen aus der
64-Zellen-Einschließung von v0.3. Sie gelten für alle 0≤h≤1/2.
Der so gewonnene einheitliche Bias B beträgt bei K=1,002 höchstens
0,000205590 in der dimensionslosen Paarwahrscheinlichkeit. Dieser B ist eine
obere Schranke für alle Profile, keine gemessene Störung und keine Behauptung
eines optimalen Worst Case.

## 4. Streuung und robuste Umkehrung

Eine unabhängige zufällige Permutation teilt die Ereignisse in m=N/8 disjunkte
Gruppen. Der Anteil Z vergleichbarer Paare innerhalb einer Gruppe nutzt alle
28 Paare. Z∈[0,1]. Bei homogener Beprobung gilt bei b=8

    Var_P(Z)=[2p(1-p)+4(b-2)v]/[b(b-1)].

Da E_P f=1 und das Extremwertverhältnis beschränkt ist, gilt 1/K≤f≤K fast
überall. Für eine ganze Gruppe liegt dQ^8/dP^8 in [K^(-8),K^8].
Wegen Var Z=inf_c E(Z-c)² folgt mit der jeweils passenden Richtung

    K^(-8) Var_P Z ≤ Var_Q Z ≤ K^8 Var_P Z.

Die äußeren Grenzen seien L_s und U_s (Varianzen). Unter Q sind die ganzen
Gruppen für jede vorab feste Partition unabhängig. Das gilt auch marginal
unter der unabhängigen uniformen Gruppierung, da die Produktverteilung für
alle festen Partitionen dieselbe ist. Die Paarvergleiche innerhalb einer
Gruppe werden als abhängig behandelt.

Mit p_* = p_min - B und p_max+B≤1/2 gilt E_Q|Z-p_Q|³≤(1-p_*)Var_Q Z.
Die endliche i.i.d.-Berry-Esseen-Schranke von Shevtsova liefert für jeden
positiven d und beide Vorzeichen

    P_Q(±(Y-p_Q) ≥ d) ≤ Φ(-d√m/√U_s) +
             0,3328[(1-p_*)/√L_s+0,429]/√m = T(d),

wobei Y der gepoolte Paaranteil ist. Die Rechnung rundet in jeder
Fehlerobergrenze nach außen. Die Normalverteilungsfunktion wird wie in v0.2
mit gerichteter rationaler Taylor-Schranke kontrolliert. Eine geschlossene
Schwanzwahrscheinlichkeit wird über einseitigen Grenzübergang behandelt.

Die Regel gibt die Rasterwerte mit Vorwärtsintervall im nominalen Band
[Y-R,Y+R] aus (nichtleerer Schnitt). Das kontinuierliche Intervall verwendet
die nach außen gerundete 1024-Zellen-Inversion aus v0.3. Für jeden erlaubten
f gilt Überdeckung ≥1-2T(R-B), ebenso für den Einschluss eines wahren
Rasterwertes. Für ein wahres Raster i sind die v0.3-Margen links und rechts
das Minimum aus R und dem zertifizierten Abstand zum Nachbarn minus R.
Ohne Nachbarn gilt R. Von **beiden** Margen muss B abgezogen werden.
Auf dem verbleibenden offenen Ereignis wird genau i ausgegeben. Dies
begrenzt die korrekte Einzelausgabe durch 1-T(d_links-B)-T(d_rechts-B)
nach unten. Eine bloße Erweiterung des Ausgabebandes ohne Kontrolle der
geänderten Varianz oder ohne zweiten Biasabzug wäre nicht ausreichend.

| Kontrast K | N | Abfragen | R | Überdeckung mindestens | Korrekte Alleinausgabe mindestens |
|---|---:|---:|---:|---:|---:|
| 1 | 900000 | 3150000 | 0,000580 | 95,05 % | 80,40 % |
| 1,001 | 1600000 | 5600000 | 0,000530 | 95,22 % | 82,17 % |
| 1,002 | 3200000 | 11200000 | 0,000500 | 95,15 % | 80,32 % |
| 1,003 | 12000000 | 42000000 | 0,000460 | 95,57 % | 81,77 % |

Die Radien dürfen in dieser Tabelle sinken, weil gleichzeitig das
Ereignisbudget steigt. Alle nichtleeren kontinuierlichen Ausgaben bei
K≤1,002 und N=3200000 haben Breite höchstens 0,912 in RT². Das gilt
auch bei nicht glatt variierender Dichte. Die Garantiemenge reicht nie über
die deklarierte Modellfamilie hinaus. Ein aus der Beobachtung heraus geratenes
K, abhängige Ziehungen, Randmasken und unbekannte Auswahl der Ereignisse
sind nicht zertifiziert.

## 5. Prüfungen und Quellen

- Die 32 Implementierungsfälle nutzen bei K=1,002 zwei entgegengesetzte
  Störprofile. Die Ablehnungsbeprobung erzeugt das normierte Produkt aus
  Volumendichte und Störgewicht. Der Klassifikator sieht nur Gruppenzahlen. Die Profile
  bevorzugen Regionen mit hohem bzw. niedrigem flachen Vergleichbarkeitsprofil.
  Pro wahrer Krümmung und Profil sind zwei ursprüngliche und zwei ausgerichtete
  Karten vorgesehen. 32 Fälle reichen nicht zur unabhängigen empirischen
  Qualifikation der Leistungsgrenzen.
- Eine getrennte Kopplung vergleicht alle Kausalrelationen von je zwölf
  256er-Ordnungen pro Modellpaar und Dichteszenario. Dies sind 72 vollständige
  Ordnungspaare. Die mathematische Gleichheit der Gesetze folgt aus der
  Konstruktion und ist von diesem numerischen Wiederholungstest unabhängig.
- In den 32 archivierten h=1/4-Pilotfällen aus v0.3 schied „flach“ 28-mal
  aus. Unter der einseitigen exakten Flach-Zwillingsinterpretation wären
  diese Ausgaben falsche Verwerfungen der flachen Geometrie. Dieselben
  Ordnungen werden anders interpretiert; dies ist kein zusätzliches Ensemble.
- Die positiven Ergebnisse sind modellbedingte Garantien und keine Messung
  der räumlichen Beprobung eines realen Detektors. Die Lücke zwischen
  hinreichender Positivgarantie und expliziter Unmöglichkeit bleibt offen.

Referenzen:

1. X6 v0.1, ausgerichtete Karte und Affinitätsrechnung: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/163
2. X6 v0.2–v0.3, Einzelordnungen und kontinuierliche Umkehrung: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/165 und https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/166
3. Frühere Dichtezwillinge und Negativkontrollen: https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/48
4. S. N. Cohen und E. Fausti, Hyperbolic contractivity and the Hilbert metric on probability measures: https://arxiv.org/abs/2309.02413 (Hintergrund zum logarithmischen Dichtekontrast; die hier verwendeten Extremwertargumente sind oben ausgeschrieben.)
5. I. Shevtsova, On the absolute constants in the Berry-Esseen type inequalities for identically distributed summands: https://arxiv.org/abs/1111.6554 (erste Strukturungleichung).
