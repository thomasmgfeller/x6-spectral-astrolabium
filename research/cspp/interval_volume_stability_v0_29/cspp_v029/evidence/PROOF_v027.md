# CSPP v0.27: Dichteuniforme Schranken auf endlichen Zeitfenstern

31. Oktober 2026. Eigene analytische Ableitung auf Main nach PR #159,
Commit `268516fb5758e87822a5c6302163e2e35d52f641`.

## 1. Ergebnis und Entscheidung

v0.26 schliesst eine deterministische l-infinity-Schranke über sämtliche
Realisierungen nichttrivialer Intervallkerne aus. Hier wird ein anderer,
ausdrücklich schwächerer Anspruch bewiesen: eine in der Sprinklingdichte
uniforme Erwartungs- und Hochwahrscheinlichkeitsschranke für eine feste
passive Probe oder ein festes, normiertes Detektormittel auf einem endlichen
physikalischen Zeitfenster. Ein zusätzliches Anwachsen des räumlichen
Rechengebiets vergrössert diese Schranke nicht.

Der Mechanismus ist hier die Volumenunterdrückung langer kausaler Ketten,
nicht eine bereits nachgewiesene signierte Pfadaufhebung. Die einfache
Koeffizientenhülle macht die Anwendung auf binomial geglättete Intervallkerne
explizit. Vorgeschriebene History wird separat behandelt. METHOD und G1
bleiben HOLD; die Genauigkeitsausschlüsse aus v0.25 bleiben bestehen.

## 2. Definitionen, Einheiten und Quantoren

Wir arbeiten in 1+3 Minkowski-Raum, c=1, mit einer fest gewählten
inertialen Zeitscheibe t=0 als Anfangsgrenze. C_rho ist ein homogener
Poisson-Prozess der Intensität rho d4x in einem deterministischen Gebiet
Omega innerhalb 0<t<T. Für eine feste passive Probe x mit Zeit T genügt
der endliche Bereich Omega geschnitten mit J^-(x). Die Probe ist KEIN
zusätzlicher Sprinklingpunkt; sie verändert keine Intervallzahlen und
propagiert nicht in andere Proben. Grössere oder räumlich unbeschränkte
Gebiete werden durch diese lokale Vergangenheit definiert.

Auf den Poissonpunkten gilt u_i=f_i+sum_{j prec i} K_ij u_j; an der Probe
gilt u_x=f_x+sum_{j prec x} K_xj u_j. Alle Intervallzahlen zählen Punkte
des zugrunde liegenden Prozesses. Die grundlegende Annahme ist

    |K_ij(C_rho)| <= kappa/rho,  |K_xj(C_rho)| <= kappa/rho,

für ALLE Realisierungen, mit kappa unabhängig von rho, N und Omega.
Abhängigkeiten zwischen Gewichten sind erlaubt. K ist messbar und strikt kausal.
Die Feldnorm ist die ungewichtete Maximumsnorm der additiven Fehler in
der diagonalnormalisierten Gleichung. G_x bezeichnet die induzierte Norm
der Abbildung (f auf Poissonpunkten, f_x) -> u_x. Insbesondere G_x>=1.
Für die ursprüngliche Gleichung (B-m²)u=J entspricht ein Quellfehler
delta J dem additiven Fehler f=-delta J/D. Ein Budget für J muss daher
zusätzlich durch |D| dividiert werden; die Normierung wird nicht gewechselt.

rho und kappa haben Einheit Länge^-4. omega=(8*pi*kappa)^(1/4) hat
Einheit Länge^-1. T ist eine Zeitdauer bzw. Länge in c=1-Einheiten.
Die Zeitscheibe ist Teil der Cauchyaufgabe, keine zusätzliche Struktur
im Intervalloperator. Ein koordinatenfreier Satz auf beliebigen Kausalsets
oder ein Satz für gekrümmte Raumzeiten wird nicht behauptet.

Für jedes fest gewählte rho im zugelassenen Bereich und jedes Omega gilt
dieselbe numerische Schranke. Das ist KEIN einziges gemeinsames Ereignis
für sämtliche Dichten einer gekoppelten Verfeinerung. Für endlich viele
geplante Dichten sind Ausfallbudgets gesondert zu verteilen.

## 3. Satz A: Dichteuniforme lokale Stabilität auf endlicher Zeit

Definiere

    F_kappa(T) = sum_{k=0}^infinity (8*pi*kappa)^k T^(4k)/(4k)!
               = [cosh(omega*T)+cos(omega*T)]/2.

Dann gelten

    E G_x <= F_kappa(T),
    P{ G_x > 1 + [F_kappa(T)-1]/delta } <= delta,  0<delta<1.

BEWEIS. Für jede endliche kausale Vergangenheit liefert die endliche
Neumannsumme die Antwort als Summe aller gerichteten Pfade. Mit dem
Betrag der Gewichte gilt realisierungsweise

    G_x <= 1+Z_x,
    Z_x = sum_{k>=1} (kappa/rho)^k C_k(x),

wobei C_k(x) die Zahl aller Ketten y_k prec ... prec y_1 prec x mit k
verschiedenen Poissonpunkten zählt. Gemeint sind Ketten der vollen
Kausalrelation, nicht ausschliesslich Hasse-Pfade. Summanden aus einem
Teilgebiet sind eine Teilmenge der Ketten in der vollen Vergangenheit.

Die k-te faktorielle Momentmassformel für einen Poisson-Prozess
(Last/Penrose, Korollar 4.10) ergibt

    E C_k(x) <= rho^k I_k(T).

Die Punkte sind durch ihre kausale Reihenfolge bereits geordnet. Es kommt
kein weiterer Faktor 1/k! hinzu. Schreibe die aufeinanderfolgenden
Zeitabstände als s_1,...,s_k>0 mit sum s_i<T. Die räumlichen Inkremente
sind unabhängig integrierte Vektoren in Kugeln vom Radius s_i. Diese
lineare Variablentransformation hat Jacobi-Determinante eins. Daher

    I_k(T) = (4*pi/3)^k int_{s_i>0, sum s_i<T} product_i s_i^3 ds
           = (4*pi/3)^k [Gamma(4)]^k T^(4k)/Gamma(4k+1)
           = (8*pi)^k T^(4k)/(4k)!.

Die letzte Identität folgt auch rekursiv aus
I_0=1 und I_k(T)=(4*pi/3) int_0^T s^3 I_(k-1)(T-s) ds.
Durch Nichtnegativität ist Tonelli anwendbar. Die rho-Potenzen kürzen
sich exakt; E Z_x <= F_kappa(T)-1 < infinity. Markov auf Z_x, nicht auf
einem fälschlich gemittelten Operator, beweist die Wahrscheinlichkeitsaussage.
Die Formel mit cosh und cos folgt durch Auswahl der durch vier teilbaren
Potenzen ihrer Taylorreihen. QED.

Diese Schranke gilt gleichzeitig für alle Eingabefehler mit festgelegter
Maximumsnorm, auch wenn deren Vorzeichen von der Realisierung abhängen.
Keine Unabhängigkeit zwischen Fehler, Gewichten oder verschiedenen Pfaden
wird benötigt. Sie sagt nichts über unverzerrte Fluktuationen oder Varianz.
Für kappa=0 oder T=0 ist G_x=1; die Formel wird direkt so interpretiert.

Die reine Punktzahlmajorante würde stattdessen exp(kappa*pi*T^4/3)
im Erwartungswert liefern. Die kausale Kettenzählung verbessert das
Wachstum auf ungefähr exp(omega*T)/4. Auch diese Verbesserung bleibt
exponentiell in der Zeit: Es gibt hier KEINE zeituniforme Stabilität.

## 4. Festes Detektormittel und räumliches Gebiet

Sei D eine feste kompakte Menge passiver Proben mit Zeitkoordinaten <=T
und mu ein deterministisches signiertes oder komplexes endliches Mass
mit Totalvariation Q. Für A=int_D u_x mu(dx) gilt realisierungsweise

    |delta A| <= [Q+int_D Z_x |mu|(dx)] ||delta f||_infinity.

Tonelli und Satz A ergeben daher mit Wahrscheinlichkeit mindestens 1-delta

    |delta A| <= Q [1+(F_kappa(T)-1)/delta] ||delta f||_infinity.

Dies gilt ohne Unabhängigkeit der Proben; gemeinsam benutzte Punkte werden
nicht als unabhängige Stichproben behandelt. Diskrete deterministische
Quadraturgewichte sind als Mass ebenfalls enthalten. Für ein positives
normiertes Mittel ist Q=1. Ein normiertes kontinuierliches Feldmittel
über den räumlich-zeitlichen KG-Detektor aus v0.25 hat diese Form, wenn
Fehler und Ausgabe in derselben Feldnormierung vorliegen. Die Normierung
durch A/e ist vor Einsetzen der Fehlergrössen anzuwenden.

Die räumliche Uniformität betrifft ein festes Detektormittel. Sobald das
Gebiet seine vollständige kausale Vergangenheit im betrachteten Zeitband
enthält, können weitere räumlich entfernte Punkte die Intervallantwort
nicht ändern. Auch vorher gilt die obere Schranke, aber ein abgeschnittenes
Gebiet definiert weiterhin eine andere Dynamik. Gebietsfehler werden
dadurch nicht zu null erklärt. Randomisierte selbstnormierte Detektoren,
insbesondere Division durch eine zufällige Punktzahl, sind nicht umfasst.

## 5. Satz B: Vorgeschriebene History nicht nochmals propagieren

Die Historypunkte liegen auf -H<t<=0; ihre Werte h werden vorgeschrieben.
Nur Punkte mit 0<t<T werden propagiert. Der Prozess auf dem ganzen Band
ist Poisson; alle Gewichte, auch History-zu-Aktiv und History-zu-Probe,
erfüllen dieselbe kappa/rho-Hülle. In einer Matrixdarstellung werden
Historyzeilen auf null gesetzt. Historyfehler eta_h und additive aktive
bzw. passive Quellfehler eta_f werden getrennt gemessen.

Definiere, mit w=8*pi*kappa,

    H_kappa(T,H) = sum_{j=0}^3 [H^(4-j)/(4-j)!] w
                         sum_{k=0}^infinity w^k T^(4k+j)/(4k+j)!
                 = sum_{r=1}^4 H^r/r! * d^r F_kappa(T)/dT^r.

Es gibt nichtnegative Pfadmajoranten Z_A und Z_H mit

    |delta u_x| <= eta_f (1+Z_A) + eta_h Z_H,
    E Z_A <= F_kappa(T)-1,   E Z_H <= H_kappa(T,H).

Folglich gilt für vorher festgelegte nichtnegative eta_f, eta_h mit
Wahrscheinlichkeit mindestens 1-delta

    |delta u_x| <= eta_f +
                  [eta_f (F_kappa(T)-1)+eta_h H_kappa(T,H)]/delta.

Für den festen Detektor aus Abschnitt 4 wird die rechte Seite mit Q
multipliziert. Beide Beiträge teilen ein einziges Markov-Budget; ihre
Korrelation wird nicht durch eine Unabhängigkeitsannahme entfernt.

BEWEIS. Eine History-zu-Probe-Kette hat genau einen Startpunkt in der
History, danach ausschliesslich aktive Punkte. Für eine aktive Probe
zur Zeit t hat die direkt erreichbare History im vollen räumlichen Band
das Volumen (pi/3)[(t+H)^4-t^4]. Ihre erwartete direkte Betragsmajorante ist

    g(t) = (w/24)[(t+H)^4-t^4].

Jeder zusätzliche aktive Kettenschritt faltet mit h(s)=(w/6)s^3.
Faktorielle Momentmasse liefern daher Z_H im Erwartungswert höchstens
sum_{k>=0} h^{*k}*g (mit k=0 als Identität). Die Rekursion
h^{*k}(t)=w^k t^(4k-1)/(4k-1)! für k>=1 und die Beta-Integralidentität
geben nach Entwicklung von g genau die angegebene positive Reihe.
Die Auswertung von Z_A ist Satz A im aktiven Band. Markov auf
eta_f Z_A+eta_h Z_H beweist die gemeinsame Aussage. QED.

Für eta_f=eta_h=eta ist der Verstärkungsfaktor
1+[F_kappa(T)-1+H_kappa(T,H)]/delta. Für exakt bekannte History eta_h=0
gilt der deutlich kleinere Faktor aus Satz A. H_kappa ist keine Aussage
über eine unendliche History: Es wächst für festes T polynomial in H.
Der Grenzübergang H->infinity ist hier unkontrolliert.

## 6. Explizite Anwendung auf die v0.25-Intervallfamilie

Bei festem q>0, rho>=q, epsilon=q/rho, festen Koeffizienten c_0,...,c_d,
a=4 sqrt(q/6) und lokaler Diagonale D=m^2-a*d_local !=0 gilt

    K_ij = (a*epsilon/D) sum_l c_l binom(n_ij,l)
                                      epsilon^l(1-epsilon)^(n_ij-l).

Die binomialen Faktoren sind nichtnegative Wahrscheinlichkeiten, deren
Teilsumme <=1 ist. Mit C=max_l |c_l| folgt deshalb für alle n und rho

    |K_ij| <= (a*q*C/|D|)/rho,  kappa = a*q*C/|D|.

Das gilt ebenso für passive Proben und die festen Historykopplungen.
rho>=q und festes q sind wesentlich. Bei festem epsilon und wachsendem
rho bleibt die Konstante im Allgemeinen NICHT gleich. Parameterfamilien
benötigen ein uniformes |D|>0 und eine uniforme Grenze für a*q*C/|D|.

Zur unveränderten Projektkalibrierung q0=3/(16*pi), m=1:

    a=1/sqrt(2*pi), omega^4 = (3/2)*a*C/|1-a*d_local|.
    theta=0: C=16, d_local=-1.
    theta=21: C=1331, d_local=-71/8.

Die folgenden Werte sind Anzeigen rational eingeschlossener Konstanten;
alle verwendbaren unteren/oberen Grenzen stehen in results/RESULTS.json.
delta=0.01. Auf dem aktiven Zeitband ab -1 bis 5/4 ist T=9/4.
Omega5 hat früheste Zeit -5; die vorgeschriebene History umfasst also
höchstens H=4. Die volle räumliche Historyhülle ist bewusst grösser als
Omega5. Sie ist gültig, aber nicht optimal.

Bei theta=21 ist F(9/4) ungefähr 899.57. Die aktive 99-Prozent-Schranke
ist ungefähr 89 858. Für den normierten absoluten Ausgabefehler 0.001
würde diese Hülle einen uniformen additiven Fehler von etwa 1.11e-8
verlangen, sofern die History exakt ist. Das ist ein bedingtes Budget,
KEINE Messung oder Qualifizierung des tatsächlich erreichten Residuums.
Mit Historyfehlern ist Satz B zu verwenden; die numerischen Werte werden
im Bericht und in RESULTS.json getrennt ausgewiesen.

Der bereits durch Genauigkeit ausgeschlossene theta=21-Kandidat wird
hier nicht rehabilitiert. Seine grossen Gewichte verschlechtern die
Stabilitätshülle stark. Aus einer grossen oberen Schranke folgt jedoch
keine tatsächliche Instabilität.

## 7. Weiterer Ausschluss: globales räumliches Maximum

Die räumliche Uniformität aus Abschnitt 4 darf nicht auf ein Maximum über
beliebig viele räumlich getrennte Beobachtungsorte übertragen werden.
Für einen festen nichttrivialen, realisierungsunabhängigen Intervallkern
und jede feste positive Dichte gilt auf einem Zeitband positiver Länge:
Zu jeder endlichen Schranke L gibt es für eine passive Probe ein Ereignis
positiver Wahrscheinlichkeit p_L, auf dem G_x>L.

BEWEIS. Der Fächer aus v0.26 mit M Blättern und r Zwischenpunkten lässt
sich durch Skalierung vollständig in die endliche Vergangenheit der
festen Probe legen. Genau ein Poissonpunkt in jeder kleinen robusten
Umgebung und kein weiterer Punkt im Vergangenheitskegel hat positive
Wahrscheinlichkeit. Dann ist G_x=1+M|t_r|. Wähle M gross genug.

Platziere nun J gleichzeitige passive Proben mit räumlichen Abständen
grösser als 2T. Ihre vergangenen Kegel im Zeitband sind disjunkt. Die
lokalen Ereignisse sind unabhängig; für den hier betrachteten
Intervallkernel hängt G_x nur von diesem Kegel ab. Daher

    P{max_(i<=J) G_(x_i) <= L} <= (1-p_L)^J -> 0.

Im unendlich ausgedehnten Band ist das Supremum über diese abzählbare
Probenfamilie fast sicher unendlich. QED. Dieser Ausschluss betrifft den
globalen räumlichen Maximalwert bei beliebiger räumlicher Gebietszunahme,
nicht die feste Probe, das normierte Mittel oder typische Einzelwerte.

## 8. Kontrolle, Grenzen und nächster begrenzter Auftrag

reproduce.py verwendet nur die Python-Standardbibliothek. Es enumeriert
alle 407 partiellen Ordnungen mit festgelegter topologischer Nummerierung
auf 1 bis 5 Punkten (nicht isomorphiequotientiert), bildet reale
Intervallzahlen und vergleicht rationale dichte Inversion,
Vorwärtsrekursion und vollständige Kettenenumeration. Zwei signierte
Projektkoeffizientensätze und vier epsilon-Werte ergeben 3256 Fälle,
zusätzlich jeweils mit eingefrorener History. Diese kleinen Ordnungen
prüfen Algebra; sie sind kein Poisson-Ensemble und müssen nicht sämtlich
in 4D einbettbar sein.
Die algebraischen Fälle verwenden den rationalen Vorfaktor 1/7 anstelle
von a/D. Sie sind keine physikalische Produktion; die tatsächlichen
Projektkonstanten werden separat rational eingeschlossen.

24 kausale Faltungskoeffizienten und 48 Historyintegrale werden durch
unabhängig expandierte rationale Polynomintegrale geprüft. Machins
pi-Reihe, ganzzahlige Quadratwurzelgrenzen und positive Reihen mit
geometrisch eingeschlossenem Rest liefern die Zahlentabellen in drei
Präzisionen. Sechs absichtlich falsche Varianten müssen scheitern.
--check reproduziert die Ergebnisdatei bytegenau, auch unter python -O.
Dies ist keine Beweisassistent-Verifikation und kein externes Peer Review.

Der nächste gezielte Verbesserungsauftrag lautet: Die hier grobe uniforme
Koeffizientenhülle durch kontrollierte Intervall- und signierte
Pfadabschätzungen ersetzen. Ein formales E[(I-K)^-1]=(I-EK)^-1 wird dabei
nicht angenommen. Insbesondere hängen Pfadpaare über gemeinsame Intervalle
zusammen; eine Einzelpfadidentität wäre noch kein Varianzsatz. Eine
verbesserte Schranke muss die eingefrorene History und das feste
Detektormittel mitführen und am unveränderten Fehlerziel budgetiert werden.

Der Grad-5-Genauigkeitsauftrag aus v0.25 bleibt unabhängig offen. Keine
neuen Bestätigungswolken, keine spektrale Langzeitfreigabe, keine Änderung
des Operators und kein neuer GitHub-Publikationsschritt gehören zu diesem
Prüfpaket. Der vorliegende Schritt endet mit einem bewiesenen lokalen
Finite-Zeit-Satz und einer ehrlichen Bewertung seiner noch groben Konstanten.

## Quellen und Zuschreibung

1. Projektquellen v0.25/v0.26 am oben fixierten Commit; Pfade, Git-Blobs
   und SHA256 in evidence/SOURCES.json. Definitionen, ursprüngliche
   Quelle, Detektor, Normierung und HOLD-Entscheide werden beibehalten.
2. G. Last, M. Penrose, Lectures on the Poisson Process, Version 21.08.2017,
   Satz 4.4 und Korollar 4.10, https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf.
   Verwendet werden die faktorielle Momentmassformel und Poisson-Unabhängigkeit.
3. S. Johnston, Particle propagators on discrete spacetime, 2008,
   https://arxiv.org/abs/0806.3083, Abschnitt 3.1.1: kausale Kettensummen
   und deren erwartete Integralform. Das allgemeine Kettensummenverfahren
   wird nicht als neue Erfindung beansprucht.
4. S. Aslanbeigi, M. Saravani, R. D. Sorkin, Generalized Causal Set
   d'Alembertians, 2014, https://arxiv.org/abs/1403.1622. Kontext:
   Infrarotnormierung und dynamische Stabilität sind getrennte Fragen.
   Deren spektrale Aussagen werden nicht mit dem vorliegenden lokalen
   endlichen-Zeit-Normsatz gleichgesetzt.

Die spezifischen Schranken, Historyzerlegung und Anwendungsbudgets wurden
hier hergeleitet. Keine wissenschaftshistorische Prioritätsbehauptung.
