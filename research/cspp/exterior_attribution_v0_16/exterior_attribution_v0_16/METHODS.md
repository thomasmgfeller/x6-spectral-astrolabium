# CSPP v0.16 - Aeussere Forcierung des kompakten Detektors

Stand: 29. Oktober 2026. Deterministische Entwicklungsrechnung auf den vier
vorhandenen Paaren d0_r00 bis d0_r03 / d0_r00_outer bis d0_r03_outer.
Keine neue Zufallswolke, keine unabhaengige Bestaetigung, keine Aenderung der
Quelle, der beiden vollen Zeitfenster oder der v0.12-Kontinuumsreferenz.

## 1. Festgelegte Fortsetzungen und exakte lokale Stuetzenaussage

Die unveraenderte KG-Loesung U hat bei t=-1 Anfangswert
exp(1-1/(1-4|x|^2)) exp(4 i z) fuer |x|<1/2 und Null sonst, sowie
verschwindende Anfangsgeschwindigkeit. U ist hier durch das urspruengliche
Maximum A/e normiert. Die physikalische Quelle bleibt dieselbe.

Endliche Ausbreitung der lokalen KG-Gleichung liefert
supp U(t,.) subset {r <= |t+1|+1/2}. Fuer -1<t<=5/4 gilt daher r<=t+3/2.
Im Diamanten Omega4 ist r<4-|t|. Fuer -1<t<=0 ist
4+t > t+3/2; fuer 0<=t<=5/4 ist 4-t >= t+3/2.
Somit ist U im aktiven Aussengebiet von Omega4 bis zum Ende des Detektors
exakt null, einschliesslich der tangentialen Gleichheit durch Stetigkeit.
In der frueheren History t<-1 gilt das nicht. Gerade dort liegen die
zu berechnenden fehlenden KG-Werte.

Es werden zwei verschiedene Rechnungen explizit gefuehrt:

* **Vorgeschriebene KG-Aussenwerte:** Die zusaetzlichen Historypunkte erhalten
  U; die aktiven Aussenpunkte erhalten exakt null. Nur innere aktive Gleichungen
  werden geloest. Dies ist eine kontrollierte Randvorschrift mit bekannter
  Kontinuumsloesung, keine vollstaendige diskrete Omega5-Evolution.
* **Vollstaendige endliche Omega5-Evolution:** Alle Historypunkte t<=-1
  erhalten U. Alle aktiven Knoten, auch die aeusseren, werden mit dem
  unveraenderten nichtlokalen diskreten Operator weiterentwickelt. Deren
  aeussere aktive Werte muessen nicht null sein.

## 2. Endliche Transportidentitaet und Vorzeichen

H bezeichnet innere History, A innere aktive Knoten und E zusaetzliche
relevante Aussenknoten. R_A=(I-K_AA)^(-1) existiert als endliche
Neumannsumme, weil K_AA streng kausal dreieckig ist. Das ist keine Aussage
ueber eine unendliche Vergangenheit oder dichteuniforme Stabilitaet.

Kausale Konvexitaet erhaelt alle Intervalle zwischen inneren Endpunkten
und zwischen einem inneren Knoten und einem Detektorpunkt. Damit sind
K_AA, K_AH und die inneren integrierten Detektorkoeffizienten Q unveraendert.
Bei identischer innerer History gilt

    delta v_A = R_A K_AE v_E
    delta A = A5-A4 = (Q_E + Q_A R_A K_AE) v_E = L_E v_E.

Die beiden Teile Q_E v_E und Q_A R_A K_AE v_E werden signiert getrennt
ausgegeben. Weglassen des zweiten Terms oder Umkehren des Vorzeichens
ist eine andere Rechnung und scheitert an den rationalen Negativkontrollen.

Fuer die KG-Randvorschrift ist delta A_KG = L_EH h_EH, da U_EA=0.
Fuer die volle diskrete Erweiterung gilt exakt

    delta A_full = delta A_KG + L_EA v_EA_full.

Ein relevanter aeusserer Punkt kann kein kausaler Nachfolger eines inneren
Punkts sein: Zusammen mit einem inneren Detektor-Endpunkt wuerde dies die
kausale Konvexitaet verletzen. Dieser Nullblock wird an allen Archivpaaren
geprueft. Aussenwerte werden daher nicht versehentlich aus einem bereits
veraenderten inneren Zustand zurueckgekoppelt.

Der verbleibende Fehler E5=A5-A_KG,detector ist weiterhin ein endlicher
Operator-und-Gebietsrest. Die Identitaet E4 = -delta A + E5 macht daraus
keinen bereits bestimmten unendlichen Operatorbias.

## 3. Exakte Datenreduktion, Integration und Rechenkontrolle

Ein Punkt (t,y) kann nur dann einen Detektorpunkt vor 5/4 erreichen, wenn
t<5/4 und |y-(0,0,3/2)| < 5/4-t+1/2. Diese Ungleichung wird nach
Quadrieren mit exakten rationalen Werten der archivierten binary64-Koordinaten
entschieden. Die kausale Vergangenheit dieses gesamten Detektorgebiets ist
nach unten abgeschlossen. Entfernte Punkte koennen deshalb weder eine
relevante Gleichung noch deren Intervallzahlen beeinflussen.

Vollstaendige und reduzierte C++-Inventare werden verglichen. Zusaetzlich
werden 64 Intervalle mit Fraction-Arithmetik direkt ausgezaehlt, ohne den
C++-Kausaltest aufzurufen. Alle KG-Historywerte im Inneren werden aus v0.12
wiederverwendet; aeussere Werte erhalten dieselbe validierte KG-Quadratur
mit Lichtkegelflaeche, Bessel-Volumenterm und analytischem Bump-Rest.

Der volle Raum-Zeit-Detektor wird mit der unveraenderten v0.10-Methode
integriert: analytische Zeitintegration, nach aussen gerundete
Ankunftsintervalle, signierte Schichtdifferenzen und Kugelsektoren gleichen
Volumens. Die Gitter 4, 8, 16 wurden vor der Ergebnisproduktion festgelegt.
Die inneren Q-Werte werden mit ihren archivierten Einschliessungen
geschnitten. Die geometrischen Koeffizienten werden einmal bei 192 Bit
zertifiziert und fuer beide History-/Loesungsrechnungen (128/192 Bit)
wiederverwendet. Das ist keine unabhaengige zweite Raumquadratur.

Vorwaertsloesung, adjungierter Transfer und volle History-zu-Detektor-
Darstellung muessen ueberlappende Einschliessungen liefern. Ein gesonderter
rationaler Graph prueft die Formeln durch explizite Pfadsummen. Zusaetzlich
werden drei falsche Varianten verworfen: falsches Vorzeichen, fehlender
innerer Transport und Verwechslung von vorgeschriebenen KG-Aussenwerten
mit vollstaendiger diskreter Aussenentwicklung.

FREEZE.json fixiert Produktionsskript, Protokoll und saemtliche verwendeten
Vorgaengerdateien vor dem neuen Lauf. Verifikation und Bericht werden als
nachgelagerte Auswertung erfasst; sie sind keine vorregistrierte Inferenz.

## 4. Welche Restgrenze tatsaechlich noch benoetigt wird

Sei Omega5 subset Omega6 subset ... eine deklarierte kausal konvexe
Ausschoepfung, mit konsistenten Historywerten und demselben Operator.
Bezeichne die wirklich vollstaendig weitergereichten Antwortaenderungen
mit d_k=A_(k+1)-A_k. Wenn fuer alle k>=5 nachgewiesene b_k>=|d_k|
existieren und sum_(k>=5) b_k endlich ist, folgt aus dem Cauchy-Kriterium

    A_infinity existiert und |A_infinity-A5| <= sum_(k>=5) b_k.

Eine geometrische Majorante b_k=C theta^(k-5), 0<=theta<1, ergäbe
C/(1-theta). C und theta muessen fuer ALLE restlichen Schalen bewiesen
werden. Sie duerfen nicht aus der einen beobachteten Erweiterung 4->5
abgelesen werden. Dieses Lemma ist eine konditionale Restgrenze, noch kein
numerischer Restnachweis fuer das vorliegende Modell.

Es ergibt sich bereits eine quantitative notwendige Bedingung fuer jede
spaetere Rettung der Genauigkeit. Wenn ell5 eine zertifizierte Untergrenze
fuer |A5-A_ref| ist und das unveraenderte Ziel tau=0.001 erreicht werden
soll, muss die spaetere Korrektur R5=A_infinity-A5 mindestens den Betrag
max(0,ell5-tau) haben. Umgekehrt schliesst eine unabhaengig bewiesene
Restobergrenze eta<ell5-tau das Genauigkeitsziel aus, denn
|A_infinity-A_ref|>=ell5-eta>tau. Die ausgegebene Groesse
necessary_beyond5_correction_lower ist diese notwendige Reparaturgroesse,
KEINE behauptete Untergrenze des tatsaechlichen unberechneten Rests.

Alternativ kann fuer einen festgelegten endlichen Aussenblock F eine
gewichtete Schaetzung |L_5F v_F| <= sum_j |L_5F,j| M_j verwendet werden,
sofern |v_F,j|<=M_j bewiesen ist. Bei unendlichem F werden zusaetzlich
Konvergenz, absolute Summierbarkeit oder ein explizit gerechtfertigtes
anderes Grenzverfahren benoetigt. Der direkte Aussenterm allein genuegt nicht.

Die Archive bestimmen weder die noch nicht spezifizierte unendliche
Aussenrealisierung noch deren transportierte Majorante. Eine nicht
begrenzte Randvariable mit nichtverschwindendem L kann bereits in einem
endlichen Kausalgraphen beliebige Antworten erzeugen. Diese algebraische
Nichtbestimmbarkeit ist KEIN Gegenbeweis gegen Konvergenz fuer festgelegte
KG-Daten und eine festgelegte Poisson-Fortsetzung.

Es wird deshalb kein Restwert 0 eingesetzt, keine endliche Schale mit der
ganzen fehlenden Vergangenheit gleichgesetzt und keine Freigabe erteilt.
Die offenen globalen Voraussetzungen werden explizit als NOT_CERTIFIED
ausgewiesen. METHOD_HOLD und G1 HOLD bleiben bestehen.

## 5. Quellen und Aussagegrenzen

Projektbasis: Commit 61ff6bfae105b14d3dfd69359f11b8f0516872ec, PR #147;
v0.10 integrierter Detektor, v0.12 kompakte KG-Referenz, v0.15 endlicher
Residualtransfer. Der mitgelieferte source_snapshot bleibt unveraendert.

Aslanbeigi, Saravani, Sorkin (2014), Generalized Causal Set d'Alembertians,
https://arxiv.org/abs/1403.1622: nichtlokale Mittelwertoperatoren und separate
Stabilitaetsfrage; kein externer Beleg der hier berechneten Archivwerte.

Belenchia, Benincasa, Dowker (2016), The continuum limit of a 4-dimensional
causal set scalar d'Alembertian, https://arxiv.org/abs/1510.04656:
Mittelwert-Kontinuumsgrenze unter Skalenbedingungen; kein Beweis fuer den
unendlich ausgedehnten diskreten Propagator dieser groben Operatorzelle.
