# CSPP v0.28: Geglättete Intervallgewichte statt grober Koeffizientenhülle

1. November 2026. Eigene deterministische Ableitung auf Main nach PR #160,
Commit `63c8be4df882316a7629907a5da3ee012e47e309`.

## 1. Ergebnis und genaue Reichweite

Die endliche-Zeit-Schranke aus v0.27 wird verschärft, ohne den Operator,
die physikalische Skala q, Quelle, History, Detektor oder das Fehlerziel
zu verändern. Statt max_k |c_k| wird der tatsächliche globale Maximalbetrag
der binomial geglätteten Intervallgewichte verwendet. Die Auslöschung
zwischen Schichtbeiträgen bleibt damit vor der Betragsbildung erhalten.

Eine exakte Binomial-Kompositionsidentität überträgt die so gewonnene
Gewichtshülle auf ALLE höheren Dichten. Ein endlicher rationaler Nachweis
mit analytisch kontrolliertem unendlichem Rest bestimmt die Maxima über
ALLE ganzzahligen Intervallzahlen, nicht nur über ein Suchgitter.

Für den bisherigen theta=21-Kandidaten bei der ursprünglichen Dichte
rho0=3/pi sinkt die gemeinsame 99-Prozent-Verstärkungsobergrenze für
gleich grosse aktive und Historyfehler von etwa 225.5 Millionen auf etwa
82 030. Das entspricht ungefähr Faktor 2749. Die aktive Obergrenze bei
exakter History sinkt von etwa 89 858 auf etwa 585.

Dies sind kleinere hinreichende OBERGRENZEN, keine gemessene Fehlerreduktion.
Die Konstanten reichen weiterhin nicht für eine Qualifizierung der
ursprünglichen Fehlerbilanz. Die v0.25-Genauigkeitsausschlüsse gelten
unverändert. METHOD und G1 bleiben HOLD. Keine neuen Wolken oder Fits.

## 2. Unveränderte Definitionen und neue Dichteuntergrenze

Einheiten und Vorzeichen bleiben wie in v0.25/v0.27. Fixiere q>0,
Koeffizienten c_0,...,c_d und setze c_k=0 für k>d. Für epsilon=q/rho gilt

    w_epsilon(n) = sum_{k=0}^{min(d,n)} c_k binom(n,k)
                                 epsilon^k (1-epsilon)^(n-k),
    K_ij = [a*q/(D*rho)] w_epsilon(n_ij),
    a=4 sqrt(q/6),  D=m^2-a*d_local !=0.

n_ij zählt das gesamte offene Kausalintervall. Passive Proben verändern
die Intervallzahlen nicht. Vorgeschriebene Historywerte propagieren nicht
innerhalb der History weiter.

v0.27 verwendete die für rho>=q gültige Hülle C_raw=max_k|c_k|. Hier wird
eine explizite Untergrenze rho_bar>=q festgelegt, epsilon_bar=q/rho_bar,
und die Klasse rho>=rho_bar untersucht. Für die Hauptaussage wählen wir
die bereits vorhandene Projektdichte rho_bar=rho0=3/pi, also
epsilon_bar=1/16 und weiterhin q=q0=3/(16*pi).

Die neue kleinere Konstante wird NICHT für q<=rho<rho0 behauptet.
Die dort weiterhin gültige gröbere v0.27-Schranke bleibt unberührt.
Die Zusatzwerte epsilon_bar=1/32 und 1/64 betreffen entsprechend
rho>=2*rho0 und rho>=4*rho0, keine neue Änderung von q oder c.

## 3. Satz A: Binomialkomposition und uniforme Gewichtshülle

Sei 0<epsilon<=epsilon_bar<=1 und p=epsilon/epsilon_bar. Dann gilt für
jede ganze Zahl n>=0 exakt

    w_epsilon(n) = sum_{m=0}^n binom(n,m) p^m(1-p)^(n-m)
                                      w_epsilon_bar(m).

BEWEIS. Setze die endliche Definition von w_epsilon_bar ein und vertausche
die Summen. Für jedes k benutzt man
binom(n,m)binom(m,k)=binom(n,k)binom(n-k,m-k). Die innere Summe wird
durch den Binomialsatz zu

    binom(n,k) (p*epsilon_bar)^k
                [1-p+p*(1-epsilon_bar)]^(n-k).

Dies ist genau der k-te Summand von w_epsilon(n). Die Endpunkte p=1
oder epsilon_bar=1 werden mit denselben binomialen Grenzwerten behandelt.
QED.

Definiere S(epsilon_bar)=sup_{m>=0}|w_epsilon_bar(m)|. Die Faktoren der
Kompositionsformel sind nichtnegative Wahrscheinlichkeiten mit Summe eins.
Daraus folgen die Supremumsnorm-Kontraktion und die verbesserte Hülle

    sup_n |w_epsilon(n)| <= S(epsilon_bar) <= C_raw,
    |K_ij| <= kappa_bar/rho,
    kappa_bar = a*q*S(epsilon_bar)/|D|,   rho>=rho_bar.

Insbesondere ist S bei sinkendem epsilon nicht zunehmend. Über die Klasse
epsilon<=epsilon_bar ist S(epsilon_bar) die kleinste mögliche konstante
Hülle dieser Form, denn epsilon=epsilon_bar ist selbst zugelassen. Ein
maximierender Intervallwert kann als kausales Intervall realisiert werden.
Die Aussage optimiert nur eine skalare Eintragsobergrenze; sie behauptet
keine Optimalität der daraus folgenden Propagatornormabschätzung.

Die Binomialinterpretation entspricht zweimaligem unabhängigem Ausdünnen.
Sie wird hier ausschliesslich als algebraische Beweishilfe benutzt:
Es werden KEINE Punkte aus einer tatsächlichen Projektwolke gelöscht.
Die Identität benötigt selbst weder ein Poisson-Ensemble noch eine
Unabhängigkeit verschiedener Kanten oder Pfade.

## 4. Satz B: Endliches exaktes Zertifikat für alle Intervallzahlen

Für 0<epsilon_bar<1 sei r=1-epsilon_bar und

    A_n = sum_{k=0}^{min(d,n)} |c_k| binom(n,k)
                                  epsilon_bar^k r^(n-k).

Stets gilt |w_epsilon_bar(n)|<=A_n. Für n>=d ist das Verhältnis des
(n+1)-ten zum n-ten binomialen Term mit Index k

    r*(n+1)/(n+1-k).

Es ist <=1, sobald epsilon_bar*(n+1)>=k. Somit sind für jedes
N>=d mit epsilon_bar*(N+1)>=d alle Summanden und A_n für n>=N
nicht zunehmend. Berechne exakt

    S_N = max_{0<=n<=N}|w_epsilon_bar(n)|.

Falls A_N<=S_N, gilt für ALLE n>N ebenfalls |w(n)|<=S_N. Daher ist
S(epsilon_bar)=S_N bewiesen. Bei A_N<S_N liegen alle Maximierer im
bereits vollständig geprüften Bereich. Für nichttriviale endliche c
existiert ein solches N: A_n geht als Polynom mal r^n gegen null,
während mindestens ein bereits erreichter |w(n)| positiv ist.
Für epsilon_bar=1 ist w(n)=c_n; dort gilt direkt S=C_raw.

Die tatsächlichen Zertifikate verwenden rationale Arithmetik. Jede
Gewichtsauswertung wird zusätzlich mit einer rekursiven Binomialverteilung
und einer unabhängigen Auswertung des Fallfaktoriellenpolynoms verglichen.
Der unendliche Rest folgt aus dem obigen Verhältnisbeweis, nicht aus
zusätzlichen Stichproben hinter N.

Für epsilon_bar=1/16 ergeben sich:

    theta=0:  S = 4976184375/4294967296
                   = 1.158608210971579..., Maximum bei n=8, w(n)<0;
              N=102, A_N < 1.156138 < S.
    theta=21: S = 161390925/4194304
                   = 38.47859501838684..., Maximum bei n=5, w(n)<0;
              N=145, A_N < 37.149424 < S.

Zum Vergleich: C_raw=16 bzw. 1331. Die negative Spitze darf nicht durch
den positiven Wert bei n=0 ersetzt werden.

Bei epsilon_bar=1/32 bzw. 1/64 werden die Maxima und Restgrenzen ebenfalls
exakt bestimmt. Bemerkenswert für die Suchkontrolle: Für theta=21 und
epsilon_bar=1/64 liegt das globale Maximum bei n=101. Eine Suche nur bis
n=50 verfehlt es. Dieses Beispiel wird als ausdrückliche Negativkontrolle
geführt. Alle Zahlen, Vorzeichen und Zertifikate stehen in RESULTS.json.

## 5. Übertragung auf das unveränderte Zeit- und Historybudget

Es wird ausschliesslich kappa aus v0.27 durch kappa_bar ersetzt. Für
1+3 Minkowski-Poisson-Kausalsets, eine feste passive Probe und endliches
aktives Zeitfenster T gelten weiterhin

    F(T) = sum_{k>=0} (8*pi*kappa_bar)^k T^(4k)/(4k)!,
    E G_x <= F(T),
    P{G_x > 1+[F(T)-1]/delta} <= delta.

Für vorgeschriebene History im Band -H<t<=0 sei

    Hfun(T,H) = sum_{r=1}^4 H^r/r! * F^(r)(T).

Mit festen Fehlerhüllen eta_f für aktive/passive additive Gleichungsfehler
und eta_h für Historyfehler gilt mit Wahrscheinlichkeit mindestens 1-delta

    |delta u_x| <= eta_f +
                 [eta_f*(F(T)-1)+eta_h*Hfun(T,H)]/delta.

Ein festes deterministisches Detektormass mit Totalvariation Q multipliziert
die rechte Seite mit Q. Für das positive normierte Detektormittel ist Q=1.
Die Fehler stehen in derselben Feldnormierung wie die Ausgabe. Ein Fehler
der ursprünglichen Quelle J muss wegen f=-delta J/D zuvor durch |D|
geteilt werden. Keine neue Normierung verdeckt das Wachstum.

Für gleiche Fehlerhüllen eta_f=eta_h=eta definieren wir

    B_active = 1+(F-1)/delta       (exakte History),
    B_joint  = 1+(F-1+Hfun)/delta  (beide Eingaben mit Norm <=eta).

Es gelten unverändert q0=3/(16*pi), m=1, T=9/4, H=4, delta=1/100,
Q=1 und Ausgabebudget 1/1000. Für die numerische Auswertung ist

    a=1/sqrt(2*pi),
    omega^4=8*pi*kappa_bar=(3/2)*a*S/|1-a*d_local|.

Die abgesicherte Rechnung liefert für rho>=rho0 folgende ungefähre
Anzeigen; die vollständigen nach aussen gerundeten Intervalle sind bindend:

| Fall | B_active v0.27 | B_active v0.28 | B_joint v0.27 | B_joint v0.28 |
|---|---:|---:|---:|---:|
| theta=0 | 809.311813 | 54.325096 | 136119.886035 | 3601.924202 |
| theta=21 | 89858.066096 | 584.886646 | 225534007.292840 | 82030.233862 |

Für theta=21 erlaubt diese Hülle bei exakter History beispielsweise ein
additives Budget von 1.70e-6. Bei gleich grossen aktiven und Historyfehlern
ist beispielsweise 1.21e-8 hinreichend. Diese Werte sind konservativ nach
unten gerundete Anzeigen der eingeschlossenen erlaubten Budgets. Das sind Bedingungen,
die die tatsächlichen Residuen erst noch erfüllen müssten. Hier werden
keine neuen KG-Residuen gemessen oder berechnet.

Die physikalischen Koeffizienten bleiben c=(1,-9,16,-8), d_local=-1 für
theta=0 bzw. c=(197/8,-3033/8,2363/2,-1331,504), d_local=-71/8 für
theta=21. Der ausgeschlossene theta=21-Kandidat wird nicht rehabilitiert.

## 6. Welche Aufhebung jetzt erfasst wird - und welche offen bleibt

Erfasst wird die Aufhebung positiver und negativer Schichtbeiträge INNERHALB
eines geglätteten Intervallgewichts, bevor dessen Betrag begrenzt wird.
Anschliessend behandelt die geerbte Pfadmajorante unterschiedliche kausale
Pfade weiterhin über ihre Beträge. Aufhebung zwischen direkten und indirekten
Pfaden, zwischen verschiedenen Pfadlängen oder über mehrere Ausgänge ist
damit nicht neu bewiesen. Der Schur-Pfadansatz aus v0.26 bleibt ein eigener
offener Anschluss für physikalisch qualifizierte Familien.

Die Anwendung auf jede Realisierung betrifft nur die Eintragshülle. Die
Ausgabegrenze bleibt probabilistisch. Der Fächer-Ausschluss aus v0.26 wird
nicht verletzt: Beliebig viele Einträge können weiterhin zusammenlaufen.
Die neue Dichteuniformität ist wie in v0.27 eine Wahrscheinlichkeitsschranke
je fest gewählter Dichte, kein gemeinsames Ereignis für unendlich viele
Dichten. Räumliche Uniformität gilt für eine feste Probe oder ein festes
Detektormittel, nicht für ein wachsendes globales räumliches Maximum.
T->infinity und H->infinity bleiben unkontrolliert.

Eine weitere Grenze des BEWEISVERFAHRENS folgt aus w_epsilon(0)=c_0:

    S(epsilon)>=|c_0|  für jedes epsilon>0.

Weil F und Hfun positive Potenzreihen in kappa sind, kann selbst beliebige
Dichteerhöhung die Eintrags-Hüllen-Methode für diese beiden c_0!=0-Fälle
nicht unter die mit C=|c_0| berechnete Budgetobergrenze drücken. Die
entsprechenden Vergleichswerte sind ebenfalls eingeschlossen. Dies ist
KEINE positive Untergrenze der tatsächlichen Propagatorverstärkung,
kein exakter Grenzwert von S und kein physikalischer Unmöglichkeitssatz.
Es zeigt, warum später Intervallgeometrie und Pfadaufhebung benötigt werden.

## 7. Validierung und Reproduktionsumfang

reproduce.py benötigt nur Python 3.12 und die Standardbibliothek. Fünf
Projektquellen werden gegen Git-Blob und SHA256 geprüft. Die unveränderte
v0.27-Reproduktion dient als klar ausgewiesene Basis für rationale
Matrixroutinen, pi-/Wurzeleinschliessungen und positive Reihen mit Rest.
Ihr Hauptprogramm wird nicht stillschweigend als neue Rechnung ausgeführt.

Sechs globale Gewichtszertifikate prüfen insgesamt 1782 ganzzahlige
Intervallwerte jeweils auf drei Rechenwegen und sichern ihre unendlichen
Reste analytisch ab. 648 rationale Kompositionskontrollen enthalten auch
n=101 und nichtdyadische Ausdünnungsparameter. Die allgemeinen Aussagen
folgen aus den Beweisen, nicht aus diesen endlichen Kontrollen.

Die 407 natürlich nummerierten Ordnungen auf 1 bis 5 Punkten werden mit
beiden Koeffizientensätzen und epsilon=1/16,1/32,1/64 geprüft: 2442
Operatorfälle und 2442 Fälle mit eingefrorener History. Dichte Inversion,
Vorwärtsrekursion und vollständige Kettenenumeration stimmen exakt überein;
die neue positive Hülle begrenzt die signierte Antwort. Diese Algebrafälle
verwenden wie zuvor den rationalen Vorfaktor 1/7 und sind keine physikalische
Produktion. Die eigentlichen Projektkonstanten werden separat eingeschlossen.

Alle zehn Budgetzeilen werden in drei Präzisionen (40/60/80) eingeschlossen;
die alten v0.27-Werte müssen mit deren archivierten Intervallen überlappen.
Die Ausgaben werden nach aussen auf 30 Dezimalstellen gerundet. Sechs
absichtliche Fehler werden abgewiesen: nur c_0 statt globalem Maximum,
unzulässige Ausdehnung unter rho0, falscher Kompositionsparameter,
übersehene späte Spitze, verschwindende Hülle allein durch Dichte und
Abschneiden vor der bewiesenen Restmonotonie.

--check muss die Ergebnisdatei bytegenau reproduzieren, auch unter -O.
Eine isolierte Wiederholung muss sämtliche Paketdateien unverändert lassen.
Das ist kein externes Peer Review und keine Beweisassistent-Verifikation.
Es werden keine wissenschaftshistorischen Neuheitsansprüche erhoben.

## 8. Nächster begrenzter Auftrag und Status

Der nächste sinnvolle Schritt ist eine Intervallvolumen-abhängige
Pfadabschätzung unter dem Poissongesetz. Sie soll die universelle konstante
Eintragshülle dort ersetzen, wo reale Intervalle stärkere Dämpfung liefern.
Dabei sind bedingte Zählungen entlang einer einzelnen Kette und gemeinsame
Intervalle zwischen unterschiedlichen Ketten ausdrücklich auseinanderzuhalten.
Eine Einzelketten-Identität wäre noch keine Varianz- oder Kovarianzkontrolle.

Die Schranke muss wieder mit dem unveränderten T, H, Detektor und Fehlerziel
ausgewertet werden. Auch der Grad-5-Genauigkeitsauftrag bleibt separat offen.
Ein Parameterwechsel oder ein frisches Bestätigungsensemble wird durch
diese Verbesserung nicht freigegeben. METHOD=HOLD und G1=HOLD.
GitHub-Veröffentlichung wurde innerhalb dieses Entwicklungsschritts nicht
ausgeführt; die wissenschaftlichen Dateien sind für eine spätere Publikation
versioniert und reproduzierbar vorbereitet.

## Quellen und Zuschreibung

1. Projektquellen v0.25/v0.27 am oben fixierten Commit, mit Pfaden,
   Git-Blobs und SHA256 in evidence/SOURCES.json. Die neuen Budgetwerte
   sind eigene Rechnungen auf diesen unveränderten Definitionen.
2. G. Last, M. Penrose, Lectures on the Poisson Process, Version 21.08.2017,
   Abschnitt 5.3 und Korollar 5.9 zum Ausdünnen; für die geerbte
   Kettenzählung Korollar 4.10. https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf.
   Die konkrete Binomial-Kompositionsformel wird oben vollständig hergeleitet.
3. S. Aslanbeigi, M. Saravani, R. D. Sorkin, Generalized Causal Set
   d'Alembertians, 2014, https://arxiv.org/abs/1403.1622. Kontext zur
   Trennung von langwelliger Normierung und dynamischer Stabilität;
   keine Übertragung ihres Modenbefunds auf unsere neue Normschranke.
