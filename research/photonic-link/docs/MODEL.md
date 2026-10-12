# Gemeinsames Verlust-, Drift- und Zeitmodell

Status: ausführbares, endliches stochastisches Referenzmodell v0.1.0. Alle
Beispielparameter sind synthetische Annahmen. Die Formeln spezifizieren den Code;
ihre Eignung für einen konkreten Aufbau ist eine separat zu prüfende Hypothese.

## 1. Quelle, Zeit und gemeinsamer Umwelteinfluss

Ein elementarer Link besteht aus einer Paarquelle und zwei Messstationen A/B.
Die Quellzeit t liegt in [0,T). Die Paarzahl ist Poisson(RT); bedingt auf die
Paarzahl sind Emissionszeiten unabhängig und gleichverteilt. Das ist die
homogene Poisson-Näherung einer schwach betriebenen, effektiv multimodigen
CW-Quelle. Sie beschreibt mehrere Paare innerhalb eines Auswertefensters,
aber keine allgemeine thermische SPDC-Paarstatistik oder bosonische
Mehrphotoneninterferenz. Gepulste Quellen benötigen ein anderes Quellmodell.

Ein dimensionloser latenter Umwelteinfluss x wird an Zellen der Breite h erzeugt:

\[
x_0\sim\mathcal N(0,\sigma_x^2),\qquad
x_{k+1}=a x_k+\sigma_x\sqrt{1-a^2}\,z_k,\quad
a=e^{-h/\tau},\quad z_k\sim\mathcal N(0,1).
\]

Dies ist die exakte OU-Übergangsverteilung am Gitter. Zwischen den Gitterpunkten
werden x, Verlust, Rotation und Laufzeit stückweise konstant gehalten. Die
deterministische Rotation wird am Zellmittelpunkt ausgewertet. Das ist eine
numerische Näherung; eine Konvergenzstudie über h ist vor Vorhersagen erforderlich.
x ist kein behauptetes Temperaturmesssignal. Die Koeffizienten müssten gegen
tatsächliche Temperatur-/Spannungsdaten identifiziert werden.

## 2. Verlust als Löschung eines Photons

Für Arm i mit Länge L_i in km, Dämpfung alpha_i in dB/km,
Einfügedämpfung ell_i in dB und Kopplung c_i:

\[
\ell_i(t)=\alpha_iL_i+\ell_{i,0}+g_i x(t),\qquad
\eta_i(t)=c_i\eta_{\mathrm{det},i}\,10^{-\ell_i(t)/10}.
\]

Jedes Photon wird bedingt auf t mit Wahrscheinlichkeit eta_i registrierbar.
Die Verluste beider Arme sind **bedingt auf x unabhängig**, aber marginal
korreliert. Daher lautet die Paarüberlebensrate vor Totzeit und Zeitselektion:

\[
R_{AB}=R\langle\eta_A\eta_B\rangle,
\qquad R\langle\eta_A\rangle\langle\eta_B\rangle
\text{ ist im Allgemeinen eine andere Größe.}
\]

Die Realisierung muss ell_i(t)>=0 erfüllen; der Code verwirft angenommene
Verstärkung. Er klemmt negative Dämpfung nicht stillschweigend auf null.
Ein unbeschränkter OU-Prozess kann diese Domäne verletzen. Das wird als
Modellfehler gemeldet und verlangt ein anderes physikalisches Verlustmodell
oder plausiblere Parameter, keine nachträgliche Auswahl günstiger Seeds.

Dieses eta ist skalar und polarisationsunabhängig. Physikalisch entspricht
Faserverlust einer Löschung in einen Vakuumsektor, nicht einem Übergang
zwischen den beiden Polarisationsbasiszuständen. Der Simulator realisiert
diese Löschung durch Ereignisausfall. Das NQK-Qubit-Amplitudendämpfungsmodell
wird deshalb **nicht als Faserverlust wiederverwendet**.

## 3. Polarisationszustand und Messung

\[
\rho_0=v|\Psi^-\rangle\langle\Psi^-|+(1-v)I_4/4,\quad 0\le v\le1,
\]
\[
U_i(t)=R_z(\phi_{i,0}+b_i x(t))
        R_y(\theta_{i,0}+\omega_i t+a_i x(t)),
\quad R_j(q)=\exp(-iq\sigma_j/2).
\]

Reihenfolge und Winkel sind festgelegt: SU(2)-Blochrotationen, keine unmittelbaren
Wellenplattenstellwerte. Die Implementierung erlaubt eine begrenzte Familie
zeitabhängiger Rotationen, keinen beliebigen, identifizierten Faser-Jonesprozess.

Nach den lokalen Rotationen wirkt optional pro Arm eine Dephasierung
\(\mathcal D_p(\rho)=(1-p/2)\rho+(p/2)Z\rho Z\).
Sie dämpft Offdiagonale um 1-p. Diese intrinsische Mischung ist von unbekannter
lokaler Basisrotation zu unterscheiden. Verlust und die optionalen lokalen
Dephasierungen werden nicht aus den Zähldaten geschätzt.

Ein linearer Analysator mit Winkel beta verwendet
\(M(\beta)=\sin(2\beta)X+\cos(2\beta)Z\),
\(\Pi_{\pm}=(I\pm M)/2\). Die gemeinsame Wahrscheinlichkeit ist
\(p_{ab}(t)=\operatorname{Tr}[\rho(t)(\Pi_a\otimes\Pi_b)]\),
in der Reihenfolge ++,+-,-+,--. Die Messbasen sind pro Lauf fest.
Es gibt keine schnelle zufällige Basisauswahl und keine QKD-Implementierung.

Ohne Dephasierung bleibt die instantane Negativität unter lokalen Unitaries
erhalten. Dagegen sind folgende Größen verschieden:

\[
\langle\mathcal N(\rho(t))\rangle,\quad
\mathcal N(\langle\rho(t)\rangle),\quad
\mathcal N\!\left(\frac{\langle\eta_A(t)\eta_B(t)\rho(t)\rangle}
 {\langle\eta_A(t)\eta_B(t)\rangle}\right).
\]

Die dritte Größe beschreibt nur die durch skalares Überleben gewichtete
Modellmischung, **vor** Totzeit und Zeitfensterselektion. Sie ist keine aus
beobachteten Koinzidenzen rekonstruierte Dichtematrix. Bei null Überlebensgewicht
wird null/`None` statt eines fingierten Zustands ausgegeben. Die Negativität
\(\mathcal N=(\|\rho^{T_B}\|_1-1)/2\) folgt [R5](REFERENCES.md).

## 4. Laufzeit, Detektoren und Uhren

Die physikalische Ankunftszeit des Signalphotons lautet

\[
u_i=t+d_i(t),\quad
d_i(t)=n_{g,i}1000L_i/c+d_{\mathrm{el},i}+q_i x(t).
\]

Negative Gesamtlaufzeiten sind unzulässig. Sprünge zwischen Zellen über h/100
werden zurückgewiesen. Auch kleinere Sprünge sind eine Diskretisierungsannahme,
keine mechanische Faserbewegung. Die Ereignisse werden nach Ankunft sortiert.

Unabhängige Dunkelereignisse werden mit Rate d pro **Port** erzeugt, also 2d
pro Station. Ihr physikalisches Erzeugungsintervall entspricht [0,T) plus
nominaler Stationslaufzeit; sie durchlaufen keine Photonentransmission.
Jeder Port hat eine unabhängige, nichtparalysierbare Totzeit tau_d.
Ein Ereignis innerhalb der Totzeit wird verworfen, verlängert sie aber nicht.
Die Detektoren beginnen im Bereitschaftszustand. Jitter folgt erst danach.

Für Gaussian-Jitter epsilon_i mit Standardabweichung sigma_i bildet die Uhr

\[
s_i=Q_{q_i^{\mathrm{tick}}}
 \left[o_i+(1+f_i10^{-6})(u_i+\epsilon_i)
       +\tfrac12 k_i10^{-6}(u_i+\epsilon_i)^2\right].
\]

o: Sekunden; f: ppm; k: ppm/s; Tick: ps. Q rundet auf den nächsten Tick,
bei Gleichstand auf gerade Ganzzahlen. Der elektronische Detektorjitter liegt
in physikalischer Zeit vor der Uhrskalierung. Optische Pump-/Trägerphase wird
nicht gemessen. Das Modell beschränkt T auf 10 s und interne relative Epochen
auf 20 s, damit Float64-Rundung deutlich unter dem kleinsten 1-ps-Tick bleibt.
Absolute Kalender-/UNIX-Zeiten gehören nicht in diese Float-Simulation.

## 5. Unabhängige Zeitkalibrierung

Genau bekannte synthetische Referenzpulse durchlaufen denselben modellierten
Pfad; ihr eigener Jitter ist konfigurierbar. Gerade Pulsindizes einschließlich
beider Intervallenden bilden den Trainingssatz, ungerade den Prüfsatz.
OLS passt lokale Zeit gegen genaue Referenzzeit an; Zentrierung vermeidet
schlecht konditionierte absolute Epochen. Die inverse affine Abbildung korrigiert
die Signalzeitstempel. Geprüft werden Mittelwert, RMS und maximaler Absolutfehler
auf den zurückgehaltenen Pulsen.

Das ist eine **Offline-Interpolation mit Referenzpulsen während des ganzen
Laufs**, keine kausale Echtzeitregelung. Einseitige Laufzeit und Uhrenoffset
bleiben dabei miteinander vermischt. Referenzjitter ist kein Ersatz für
Referenzunsicherheit oder Kalibriertransferfehler. Zeitlich benachbarte Prüf-
und Trainingspunkte teilen denselben Umweltprozess; der Prüfsatz beweist
keine Generalisierung auf einen anderen Tag.

`max_abs_residual <= W/4` pro Arm ist ein vorab festgelegter synthetischer
Entwurfs-Screen. Bei Überschreitung bleibt der Bericht sichtbar und zeigt false;
es werden weder Daten entfernt noch die Toleranz angepasst. Das ist kein
Sicherheitskriterium und keine garantierte Schranke für ungesehene Ereignisse.

## 6. Zeitfenster und vollständige Bilanz

Korrigierte Zeitstempel werden auf gemeinsame ganzzahlige ps gerundet.
Fenster sind halboffen: [jW,(j+1)W). Ereignisse außerhalb [0,T) werden separat
gezählt. Alle verbleibenden Ereignisse sind zeitgeordnet. Ein Bit pro Port
A+, A-, B+, B- bildet eine der 16 Belegungsmasken. Zusätzlich werden gespeichert:
Gesamtfenster, Wiederholungsfenster, vier Rohklickzahlen, zusätzliche gleiche
Portklicks sowie Mehrportfenster. Leere Fenster sind **leere Auswertefenster**,
keine Zählung verlorener erzeugter Paare.

Die bedingte Korrelation verwendet nur Masken 5,6,9,10. Ein solcher Belegungsfall
kann mehrere Photonen pro Port enthalten und ist daher keine eindeutige
Paarzuordnung. Die gleichportige Fraktion ist bei gleicher Basis und Singletziel
ein Fehlerraten-Diagnostikum, bei anderen Basen nicht ohne Weiteres eine QBER.
Wiederholungen und Mehrportfälle bleiben im Bericht. Eine statistische
iid-Konfidenzschranke wird bei möglicher Drift nicht automatisch ausgegeben.

Für isolierte Paare mit gleichverteilter Fensterphase und unabhängigem
Differenzzeitfehler D~N(delta,sigma_delta²) ist die analytische Retention

\[
A(W,\delta,\sigma_\Delta)=
\mathbb E[(1-|D|/W)_+],\qquad
\sigma_\Delta^2=\sigma_A^2+\sigma_B^2
\]

bei unabhängigen Jittern und gleicher Uhrskalierung. Für sigma_delta=0 ergibt
sich max(0,1-|delta|/W). Das unterscheidet sich von einer gleitenden
Koinzidenzsuche |tA-tB|<W/2. `fixed_bin_retention` wird gegen unabhängige
Quadratur und Ereignissampling geprüft. Quantisierung, Totzeit, Referenzfehler,
Korrelationen und Randverluste sind in dieser Näherung nicht enthalten.

Im niedrigen Besetzungsregime liefert RA*RB*W eine Größenordnung für zufällige
gemeinsam belegte Fenster unkorrelierter Klickströme. Sie ist kein allgemeiner
Untergrundabzug für korrelierte Signal-/Dunkelströme. Der Simulator führt keinen
solchen Abzug durch.

Die gemeinsame analytische Näherung für echte, isolierte Paarbeiträge zum
Portfall ab fasst alle drei Modellteile zusammen:

\[
\mu^{\mathrm{true}}_{ab}\simeq
R\int_0^T\eta_A(t)\eta_B(t)\,p_{ab}(t)\,
A\!\left(W,\delta(t),\sigma_\Delta(t)\right)\,dt.
\]

delta(t) ist der verbleibende relative Zeitfehler nach der jeweiligen
Kalibrierung. Verlustgewichte, Born-Wahrscheinlichkeiten und Zeitakzeptanz
werden **vor** dem Zeitmittel miteinander multipliziert. Ihre Mittelwerte
getrennt zu multiplizieren verliert die gemeinsamen Korrelationen. Diese
Formel gilt nur ohne relevante Mehrpaarbelegung, Totzeit, Portabhängigkeit
der Zeitfehler und Randverluste. Sie ist nicht identisch mit den beobachteten
Belegungszählern. Das Ereignismodell stellt zusätzlich Mehrfachbelegung,
unabhängige Dunkelereignisse, Totzeit, Quantisierung und Gate-Ränder explizit dar.

Eine zeitselektierte Zustandsmischung hätte unter denselben eingeschränkten,
portunabhängigen Bedingungen Gewicht eta_A*eta_B*A. Der aktuelle Bericht
berechnet absichtlich nur die klar benannte Überlebensgewichtung eta_A*eta_B;
er behauptet keinen aus diesen approximativen Gewichten tomografierten Zustand.

## 7. Digitaler Vertrag und ausgeschlossene Effekte

Die geerbte Schnittstelle verwendet **uint64 ps-Zeitstempel und 24 uint64-Zähler**;
uint32 ist unter anderem die Kalibrier-ID. Die neun einfachen Kategorien ersetzen
die sieben übrigen Belegungsmasken nicht. SGNCv007 umfasst 244 Byte mit CRC32.
CRC erkennt Übertragungsfehler, authentisiert aber keinen Sender.

Der Export ist eine synthetische Host-Aggregation. Er implementiert keine neue
FPGA-Pipeline. Für spätere verteilte Streams müssen Stationsepochen, Reihenfolge,
Kalibrier-ID, Verlustflags und konservative Watermarks gemeinsam spezifiziert
werden. Bei positiven affinen Abbildungen kann jede garantierte lokale
Watermark in die gemeinsame Zeit abgebildet werden; erst das Minimum der
beiden garantierten Frontiers darf gemeinsame Fenster schließen. Pufferung,
Nachzügler und Kalibrierwechsel benötigen einen separaten Echtzeitnachweis.
Die Offline-Sortierung synthetischer Ereignisse liefert keinen Nachweis, dass
ein realer Empfangspuffer beliebige Jitter-/Transportnachzügler korrekt behandelt.

Nicht modelliert: PDL, PMD, dispersive Wellenpakete, spektrale Filterkopplung,
Temperaturabhängigkeit der Quelle, Detektor-Nachpulse, Blinding, TDC-DNL/INL,
FIFO-Durchsatz, driftende Detektionseffizienz, nichtgaußförmige Jitterausläufer,
faserinduzierter klassischer Raman-Untergrund, synchronisierte Störer,
Quantenrepeater, Quantenspeicher oder QKD-Nachverarbeitung.
