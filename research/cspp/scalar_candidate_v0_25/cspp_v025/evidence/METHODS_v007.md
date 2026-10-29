# Skalarer Anfangsdaten- und Propagationsbenchmark v0.7

28. Oktober 2026. Einheiten c=hbar=L0=1, Metrik (-,+,+,+),
Box=-partial_t^2+Delta. Dieses Paket erweitert den unveränderten Pilot v0.1
um einen ausdrücklichen Anfangsdatenadapter, eingeschlossene Dreieckslösungen
und eine vollständige Prüfung der dafür benötigten Kausalrelationen.
Es wird kein neues Sprinkling erzeugt und kein Bestätigungsseed verwendet.

## 1. Festgelegte Daten, Stichprobe und Beobachtungen

Alle 64 archivierten Wolken aus v0.1 bleiben unverändert: je 16 bei erwarteten
Punktzahlen 512,1024,2048,4096 in Omega4={|t|+r<4}, Volumen 512*pi/3.
Die drei Glättungen epsilon=1,1/4,1/16 verwenden dieselbe jeweilige Wolke.
Die Dichte ist rho=nu/Vol(Omega4), keine nachträglich aus N geschätzte Größe.
Die Referenz- und Kausalitätsaussagen beziehen sich auf die exakt als binäre
Gleitkommazahlen gespeicherten Koordinaten.

Zusätzliche analytische Cauchy-Kontrollen verwenden m=1 und die unveränderten
physikalischen Wellenzahlen k=0,2,4,8:

\[
f_k(\mathbf x)=e^{ikz},\qquad g_k(\mathbf x)=-i\omega_k f_k(\mathbf x),
\quad\omega_k=\sqrt{k^2+1},
\quad U_k(t,\mathbf x)=e^{ikz-i\omega_k(t+1)}.
\]

Diese homogenen ebenen Wellen sind neue exakte Anfangsdatenkontrollen; sie
ersetzen weder die alten Felder mit Abschneider noch die kompakte Quelle.
Ihr Verhalten außerhalb des endlichen Simulationsgebiets ist bekannt und
wird nicht durch eine neue Randbedingung stillschweigend abgeschnitten.

Die kompakte Quelle bleibt
f=A*exp[-1/(1-r^2/a^2)]*exp(i*k0*z) für r<a, sonst null,
a=1/2, k0=4, L2-Norm eins, bei t0=-1 und g=0. Für diese Quelle werden
m=0,1,2 auf der vorab gewählten Archivwolke **d0_r00** geprüft. Alle aktiven
Punkte dieser Wolke, einschließlich ihrer vorgeschriebenen Vergangenheit,
erhalten Kontinuumseinschließungen bei 128 und 192 Bit. Die Wahl erfolgte vor
der Produktion, nicht anhand eines günstigen Ergebnisses. Eine Übertragung
dieser vollständigen Quellfehlerzerlegung auf die übrigen 63 Wolken wird
nicht behauptet.

Beobachtet werden die bisherigen 28 festen Proben: 21 innere Punkte bei
t=-1/2,0,1/2 sowie sieben Detektorpunkte bei t=1, Mittelpunkt (0,0,3/2)
und sechs Achsenversetzungen von 1/4. Als zusätzliche skalare Beobachtung
dient die feste gewichtete Punktsumme

\[
I_P(u)=\sum_{p\in P_D}w_p|u_p|^2,\qquad
w_p=\frac{\exp[-1/(1-r_p^2/(1/2)^2)]}
{\sum_{q\in P_D}\exp[-1/(1-r_q^2/(1/2)^2)]}.
\]

Hier ist r_p der Abstand vom Detektorzentrum. Alle Gewichte sind positiv und
summieren sich zu eins. **Dies ist eine diskrete Beobachtung an sieben Punkten,
keine Quadratur des räumlichen Detektors.** Die räumlichen Fehler aus v0.5,
eine Dirac-Detektormatrix und E4-Spurabstände werden damit nicht geschlossen.

## 2. Der diskrete Anfangsdatenadapter

Der bisherige Pilot versorgte sämtliche Punkte t<=-1 mit einer numerischen
Kontinuumsvergangenheit. Diese Orakelvorgabe bleibt nur eine Kontrollrechnung.
Der neue eigentliche Adapter benutzt ausschließlich f,g und deren analytisch
definierte räumliche Laplacians an den bereits vorhandenen History-Punkten.
Mit tau=t+1 und L_m=Delta-m^2 werden zwei feste Fortsetzungen verwendet:

\[
H_1=f+\tau g,\qquad
H_3=f+\tau g+\frac{\tau^2}{2}L_mf
+\frac{\tau^3}{6}L_mg.\tag{1}
\]

Sie werden auf allen Wolkenpunkten mit t<=-1 vorgeschrieben. Die aktive
unbekannte Lösung liegt auf -1<t<1. Es werden keine künstlichen Punkte auf
der Anfangsfläche eingefügt und keine Quellpunkte als Sprinkling-Punkte gezählt.
Die passiven Proben sind ebenfalls keine zusätzlichen Intervallpunkte.

(1) erfüllt als glatte Fortsetzung H(t0)=f und partial_t H(t0)=g. Dies
beweist keine intrinsische Cauchy-Wohlgestelltheit des nichtlokalen Operators
und erzwingt nicht die Zeitableitung einer aus der diskreten Lösung erst
zu rekonstruierenden kontinuierlichen Funktion. **H1 und H3 definieren zwei
konkrete finite History-Adapter.** Sie benötigen bekannte Einbettungskoordinaten
und analytische Ableitungen; ein Adapter für verrauschte, ausschließlich
diskrete Messdaten ohne Ableitungsinformation bleibt offen.

Für die ebenen Wellen gilt L_m f=-omega^2*f und L_m g=-omega^2*g.
Für den kompakten Bump, h=1-r^2/a^2>0, ist

\[
L_mf=f\left[-\frac6{a^2h^2}-\frac{8r^2}{a^4h^3}
+\frac{4r^2}{a^4h^4}-k_0^2-m^2
-\frac{4ik_0z}{a^2h^2}\right].\tag{2}
\]

Außerhalb einschließlich der Supportgrenze sind f und alle verwendeten
Ableitungen exakt null. Die Quelle ist glatt, daher entstehen dort keine
zusätzlichen distributionswertigen Randterme. Wegen g=0 ist H1=f und
H3=f+tau^2*L_mf/2. Eine höhere Taylorordnung auf einem bis zu drei
Zeiteinheiten langen History-Streifen ist kein Konvergenzbeweis und kann
gerade bei großen k einen größeren Fehler erzeugen.

## 3. Exaktes endliches diskretes Problem und eingeschlossene Lösung

Der Operator aus v0.1 bleibt

\[
B_\epsilon u_i=a\left[-u_i+\epsilon\sum_{j\prec i}
w_\epsilon(n_{ji})u_j\right],\qquad
a=4\sqrt{\epsilon\rho/6}.
\]

Die Gewichte lauten
w_e(n)=sum_(k=0)^3 c_k binom(n,k)e^k(1-e)^(n-k), c=(1,-9,16,-8).
Für epsilon=1 wird der exakte endliche Grenzfall verwendet. Für alle hier
getesteten homogenen KG-Lösungen ist (Box-m^2)U=0. Deshalb lautet die
normierte diskrete Gleichung

\[
u_i=\sum_{j\prec i}T_{ij}u_j,
\qquad T_{ij}=\frac{a\epsilon}{a+m^2}w_\epsilon(n_{ji}).\tag{3}
\]

Nach exakter Zeitsortierung ist der aktive Block strikt unterdreieckig.
Mit A_U=I-T_UU ist det A_U=1; seine Inverse ist die endliche Summe der
Potenzen von T_UU. Damit ist jedes **dieser endlichen History-Probleme**
eindeutig lösbar. Daraus folgt keine uniforme Stabilität bei steigender Dichte.

Die Produktionsrechnung schließt pi, a, sämtliche Gewichtsfaktoren,
Anfangsdaten und alle Schritte der Vorwärtssubstitution mit Arb/Acb ein.
Kein Koefﬁzient darf wegen einer unsicheren Nullentscheidung ausgelassen
werden: nur `is_zero()` erlaubt das Überspringen einer bewiesenen exakten Null.
Die einmalige Korrektur dieses Randfalls vor abgeschlossener Produktion ist
in [Amendment 01](amendment_01/AMENDMENT.json) mit Originalquellen,
ursprünglichem Freeze und abgebrochenem Protokoll erhalten.

Die normale binary64-Lösung wird zusätzlich mit der unveränderten
SciPy-Dreiecksroutine des Piloten berechnet. Die eingeschlossene Lösung
mit exakt als Dyaden interpretierten Float-Eingabewerten dient als
unabhängige Vorwärtsfehlerreferenz. Ein kleiner algebraischer Rückwärtsfehler
wird weiterhin berichtet, ersetzt diese Vorwärtsfehlerkontrolle aber nicht.

## 4. Vier getrennte Beiträge bis zu den Messwerten

Sei U die Kontinuumsreferenz, uO die mathematisch exakte diskrete Lösung mit
exakter Kontinuumshistorie, uH die mit exakt ausgewertetem Adapter H,
uR die mit den tatsächlich gerundeten History-Eingabewerten, aber exakt
gelöstem diskreten System, und uF das ausgegebene binary64-Ergebnis.
An jeder Probe gilt die signierte Identität

\[
u_F-U=\underbrace{u_O-U}_{E_{op}}
+\underbrace{u_H-u_O}_{E_{init}}
+\underbrace{u_R-u_H}_{E_{input}}
+\underbrace{u_F-u_R}_{E_{solve}}.\tag{4}
\]

- Eop enthält den diskreten Operator einschließlich der endlichen Gebietstrunkierung.
  Nichtlokalitätsbias, Sprinklingstreuung und Außenrand werden hier nicht erneut
  einzeln geschätzt; die Trennung von v0.6 bleibt davon unberührt.
- Einit ist der Fehler der ausdrücklich gewählten History-Fortsetzung aus den
  unveränderten exakten Cauchy-Daten.
- Einput erfasst die endliche Genauigkeit bei der Auswertung dieses Adapters,
  einschließlich Quellen-Normierung und Funktionen wie exp und sqrt.
- Esolve erfasst die Float-Koeffizientenrechnung und die numerische Lösung
  bei festgehaltenen tatsächlich übergebenen History-Werten.

Die Unsicherheit der Kontinuumsreferenz liegt zusätzlich explizit in den
Intervallradien. Sie wird weder als beobachteter physikalischer Fehler noch
als unabhängige Zufallsvarianz umgedeutet. Alle vier Beiträge werden durch
Differenzen eingeschlossener Größen begrenzt; (4) wird an jeder Probe geprüft.
Ein RMS wird aus eingeschlossenen Betragsquadraten gebildet. Die Komponenten
dürfen wegen möglicher Vorzeichen-Auslöschung nicht als unabhängige Varianzen
quadratisch addiert werden. Ensemble-RMS über die 16 festen Archivwolken sind
deskriptive Zusammenfassungen, keine neue statistische Bestätigung.

Eine zweite Kontrolle benutzt die normierten lokalen Operatordefekte

\[
r_i=U_i-\sum_jT_{ij}U_j,\qquad
r_p=U_p-\sum_jT_{pj}U_j.
\]

Mit eH=0 und eU=uO-U gilt e_i=sum_j T_ij e_j-r_i sowie
e_p=sum_j T_pj e_j-r_p. Diese Identität wird auf den Produktionsdaten
nachgerechnet. Zusätzlich liefert die nichtnegative Rekursion
s_H=0, s_i=|r_i|+sum_j |T_ij|s_j eine sichere obere Schranke
|Eop_p|<=|r_p|+sum_j |T_pj|s_j. Die vollständigen Defekte brauchen auch
alle internen Feldwerte, weshalb für die kompakte Quelle sämtliche aktiven
Knoten der festen Wolke eingeschlossen werden.

## 5. Verstärkung beliebiger Anfangsdatenfehler

Für eine beliebige History-Störung mit sup_H |delta h|<=eta setze
v_H=1 und v_i=sum_j |T_ij|v_j. Dann ist

\[
|\delta u_p|\le G_p\eta,\qquad G_p=\sum_j|T_{pj}|v_j.\tag{5}
\]

Diese Schranke gilt für **alle** History-Richtungen, nicht nur für die
frühere konstante Einheitsstörung. Die G_p werden pro Fall und Probe
eingeschlossen. Auf einem kleinen Kontrollgraphen wird die ganze History-Basis
gelöst und ihre tatsächliche induzierte Norm gegen (5) geprüft.

Fehler der Cauchy-Daten und ihrer Laplacians lassen sich ohne einen neuen
Sprinkling in diese Schranke einsetzen. Auf dem History-Streifen gilt |tau|<=3.
Für sup-Normen eta_f,eta_g,eta_Df,eta_Dg der vier Eingabefehler folgt

\[
\eta_{H1}\le\eta_f+3\eta_g,
\]
\[
\eta_{H3}\le(1+\tfrac92m^2)\eta_f
+(3+\tfrac92m^2)\eta_g
+\tfrac92\eta_{Df}+\tfrac92\eta_{Dg}.\tag{6}
\]

(5) und (6) verfolgen also auch vorgegebene Datenunsicherheiten bis zu den
Beobachtungen. Es wird keine Schranke für Ableitungsfehler aus einer bloßen
Schranke für Funktionswerte erfunden. Für den konkreten Adapterfehler
H-U auf der History wird zusätzlich sein eingeschlossenes Maximum eingesetzt.
Die signierte direkte Auswertung in (4) ist häufig wesentlich enger als (5).

Für die Punktintensität gilt bei beliebigem Beitrag delta u

\[
|I_P(u+\delta u)-I_P(u)|
\le\sum_pw_p\left(2|u_p||\delta u_p|+|\delta u_p|^2\right).\tag{7}
\]

Die vier Stufen U -> uO -> uH -> uR -> uF werden mit jeweils dem richtigen
Ausgangsfeld ausgewertet. Sowohl ihre signierten Intensitätsänderungen als
auch die absoluten Schranken (7) werden gespeichert. Die Änderungen
teleskopieren; eine Summe unabhängiger Intensitätsvarianzen wird nicht benutzt.

## 6. Kontinuumsreferenz und numerische Fehler

Die ebenen Wellen werden direkt mit eingeschlossenen Elementarfunktionen
ausgewertet. Für die kompakte Quelle werden die unveränderten, in v0.3/v0.5
hergeleiteten Kirchhoff- und massiven Bessel-Formeln verwendet. Deren
Quellenrand, Quadraturrest und Normierungsunsicherheit bleiben enthalten.
Die 84 bereits publizierten Probe/Masse-Einschließungen werden unverändert
übernommen; die älteren 34 Probe-Einschließungen werden bei der 192-Bit-Rechnung
nicht als neu berechnete 192-Bit-Werte ausgegeben.

Neu sind die Einschließungen an allen aktiven Knoten von d0_r00, jeweils
bei 128 und 192 Bit. Der maximale erlaubte Komponentenradius einer solchen
Referenz ist 1e-12; für die propagierten Lösungswerte gilt 1e-10. Eine
Überschreitung beendet die Rechnung mit HOLD und wird nicht durch Entfernen
des betreffenden Falls oder Erhöhen einer Toleranz geheilt.

## 7. CPU-Regel für sämtliche tatsächlich verwendeten Kausalrelationen

Für exakt gespeicherte endliche binary64-Koordinaten gilt die strikte Ordnung
b.t>a.t und (b.t-a.t)^2>sum_(k=1)^3(b_k-a_k)^2. Exakt nullartige Paare sind
nicht geordnet. Der neue Kern benutzt für jede Subtraktion, Multiplikation
und Summenoperation nach außen erweiterte Intervalle mittels `nextafter`.
Nur ein eindeutig positives oder negatives Ergebnis wird direkt entschieden.
Jeder verbleibende Fall wird mit Python-`Fraction` auf den **exakten binären
Eingabewerten** entschieden. Das Ergebnis hängt nicht von der Breite eines
plattformabhängigen `long double` ab.

Der Kern wird ohne fast-math und ohne FMA-Kontraktion kompiliert. IEEE binary64,
Rundung auf den nächsten Wert und aktive Subnormalzahlen werden geprüft;
eine Bereichsgrenze verhindert Überläufe des Filters. Jeder Filterwert enthält
die exakte elementare Operation, daher enthält auch der resultierende Bereich
den exakten Kegelausdruck. Im unentschiedenen Fall liefert die rationale
Rechnung sein genaues Vorzeichen. Die allgemeine Idee adaptiver exakter
Prädikate folgt [1]; der hier verwendete Kegeltest ist separat implementiert.

Die erforderliche Inventarliste umfasst:

1. alle Wolke/Wolke-Relationen, einschließlich der Relationen für interne
   Intervallpunkte und zwischen History- und aktiven Knoten;
2. alle Wolke/Probe-Relationen für sämtliche 32 alten Proben, also auch die
   vier historischen Randproben;
3. die exakten Vergangenheits-/Zukunftsspitzenrelationen für Omega4 bzw. Omega5
   und die zugehörige äußere Schalenmitgliedschaft;
4. die exakten Vergleiche t<=-1 und t<1 für die vorgeschriebene History und
   den aktiven Lösungsbereich.

Zeitlich umgekehrte bzw. gleichzeitige Paare sind durch exakte Vergleiche
der gespeicherten Zeiten ausgeschlossen. Probe/Probe-Relationen und Relationen
zu eingefügten Anfangspunkten werden nicht benötigt: Beide Arten zusätzlicher
Intervallpunkte existieren in diesem Adapter nicht.

In beiden CPU-Konfigurationen werden alle 64 inneren Wolken und acht äußeren
Erweiterungen aus den alten RNG-Identitäten regeneriert. Archiv- und
RNG-Ausgabehashes bleiben exakt. Rohrelations-Bitfelder, sämtliche benötigten
Intervallzahlen und Bereichsmasken müssen exakt übereinstimmen. Ein eigener
Gegentest zeigt, dass gleiche Probe-Intervallzahlen allein eine veränderte
interne Kausalrelation übersehen können.

Die bisherige 2^-48-Koordinatenschranke bleibt ein technischer Vergleichstest,
kein Beweis über ideal reelle Zufallskoordinaten. Die eigentliche Produktion
verwendet die kanonischen Archivkoordinaten. Ihr numerischer Replay läuft
in beiden CPU-Modi mit den alten Toleranzen atol=1e-10, rtol=1e-11;
die mathematischen Einschließungen sind davon unabhängig. Der 48-Wolken-
Operatorvergleich v0.2 wird hier nicht zur vollständig geprüften Graphfamilie
umdeklariert, da er in dieser Propagation nicht benutzt wird.

## 8. Ressourcen, Provenienz und Aussagegrenzen

Die Quelltexte und geerbten Daten sind vor der vollständigen Produktion
eingefroren. Der erste Freeze und die vor Abschluss entdeckte
Unsicher-Null-Korrektur bleiben im Amendment erhalten; danach wird die
gesamte Produktion wiederholt. Alle Zahlen verwenden die korrigierte Fassung.
Ein vollständiger Replay wird isoliert in temporären Dateien ausgeführt.
Die Obergrenzen bleiben 4 GiB, ein Worker und 21.600 Sekunden.

Präzisionsüberlappung, unabhängiger dichter Ball-Löser auf einem Kontrollgraphen,
exakte rationale Intervallzählung, nullartige/um ein ULP versetzte Paare,
Initialwerte, Ableitungsregression und bewusst falsche Lösungen bilden
verschiedene Tests. Die mathematischen Einschließungen folgen aus den
Rekursionen und Restschranken; ein erfolgreicher Replay ersetzt diese Beweise
nicht. Neue Archivwolken, ein Bestätigungsexperiment und eine Freigabe von
G1/G2/G3 folgen daraus nicht.

## Primärquellen und Vorgänger

1. J. R. Shewchuk, [Adaptive Precision Floating-Point Arithmetic and Fast Robust
   Geometric Predicates](https://www.cs.cmu.edu/~quake/robust.html), 1997.
2. FLINT, [Arb-Matrizen und eingeschlossene lineare Gleichungssysteme](https://flintlib.org/doc/arb_mat.html).
   Die Produktion verwendet python-flint 0.8.0 / FLINT 3.3.1 und eine explizite
   Vorwärtssubstitution; neuere Dokumentation ändert diese Versionsbindung nicht.
3. [Skalarpilot v0.1](../scalar_pilot_v0_1/METHODS.md),
   [CPU-Qualifizierung](../scalar_pilot_portability_v0_1/README.md),
   [Kontinuumsreferenz v0.5](../massive_reference_v0_5/METHODS.md),
   [gemeinsame Budgetentscheidung v0.6](../joint_budget_v0_6/METHODS.md).
