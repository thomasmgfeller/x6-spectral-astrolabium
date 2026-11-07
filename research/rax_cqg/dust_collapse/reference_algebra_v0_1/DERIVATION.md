# CST-DUST: Observablenalgebra, Superselektion und endliche Phasenreferenz v0.1

Stand: 7. November 2026. Basis: Main nach PR 263,
`c77cb607db23a043cd4965ee4efeb206eda22f8e`.
Der Prüfplan wurde nach dem analytischen Entwurf und vor den endlichen Kontrollen
eingefroren; er ist keine externe Präregistrierung.

**Ergebnis:** Die bisherige Record-Wirkung bestimmt nicht, ob die beiden
Dichtestrata physikalisch superselektiert sind. Unter einer zusätzlich erklärten
globalen U(1)-Erhaltung folgt dagegen ein scharfes, endliches Referenzbudget für
den bereits erklärten kohärenten Mess-Effekt. Das ist eine bedingte Anwendung
bekannter Quantenreferenz-Methoden, keine Herleitung einer CST-Ladung oder eines
CST-Messapparats. Alle acht physikalischen Gates bleiben **HOLD**.

## 1. Was die vorhandenen Definitionen tatsächlich bestimmen

Der verwendete kinematische Hilbertraum zerfällt in
\(H=H_a\oplus H_c\): Dichte-Nullatom und kontinuierlich positiver Dichteanteil.
Die Uhrmoden sind in beiden Teilen enthalten. Sei \(\Pi_a\) die Atomprojektion,
\(\Pi_c=I-\Pi_a\). Die Record-Algebra besteht aus Multiplikationsoperatoren.
Die reelle Wirkung \(S_d\) wirkt darin als Multiplikation \(M_S\), und die
zugehörige Phasenmultiplikation erhält beide Strata.

Dies ist mit mindestens zwei verschiedenen Operatoralgebren vereinbar:

\[
\mathcal A_{\rm block}=B(H_a)\oplus B(H_c),\qquad
\mathcal A_{\rm full}=B(H_a\oplus H_c).
\]

Beide enthalten dieselben beschränkten Record-Observablen und Phasenoperatoren.
In der ersten ist \(\Pi_a\) zentral, in der zweiten nicht. Die Deklaration einer
Record-Algebra als vollständige physikalische Algebra würde eine Einschränkung
**hinzufügen**; sie folgt nicht aus dem gemeinsamen diagonalen Teil.

Für jede Dichtematrix \(\rho\) definiere
\(D(\rho)=\Pi_a\rho\Pi_a+\Pi_c\rho\Pi_c\).
Für alle \(E\in\mathcal A_{\rm block}\) gilt
\(\operatorname{Tr}(E\rho)=\operatorname{Tr}(ED(\rho))\).
Auch jede Folge aus blockerhaltender Evolution und entsprechenden Operationen
erhält diese Ununterscheidbarkeit. Diagonale Daten können daher nicht zwischen
einer physikalischen Superselektion und einer lediglich eingeschränkten
Messklasse entscheiden. Innerhalb eines Stratums sind Phasen weiterhin möglich.

Wesentliche Einheitenkontrolle aus der gepinnten Variation:
\(w=v_4\rho\) hat die Dimension **Wirkung, nicht Ruhemasse**. Eine räumliche
Staubmasse benötigt eine physikalische Hypersurface und einen kalibrierten Strom.
Aus ihrer möglichen Erhaltung folgt keine Erhaltung des binären Sektorlabels
\(\Pi_c\). Auch das Nullatom ist kein bereits bestimmtes Fock-Vakuum.

## 2. Ziel, Vergleichsraum und zusätzliche Annahmen

Wähle normierte \(a\in H_a,c\in H_c\), einschließlich festgelegter Uhr- und
Dichtemoden. Setze \(\psi_+=(a+c)/\sqrt2\) und
\(P_+=|\psi_+\rangle\langle\psi_+|\), null auf dem orthogonalen Komplement.
Der universelle Effektfehler ist

\[
\tau=\|E-P_+\|=\sup_\rho|\operatorname{Tr}((E-P_+)\rho)|.
\]

Der Supremumsbereich sind alle Dichtematrizen des erklärten Vergleichsraums.
Er ist kein Nachweis, dass diese Zustände bereits physikalisch zulässig sind.
Für blockdiagonale Effekte bleibt die zuvor bewiesene scharfe Grenze
\(\tau\ge1/2\). Ihr Beweis verwendet die beiden Testzustände
\((a\pm c)/\sqrt2\), die blockdiagonal denselben Erwartungswert besitzen.

Nun wird **zusätzlich** ein Referenzmodell definiert:

* \(Q_S=\Pi_c\), also die dimensionslose Sektorladung 0 oder 1;
* \(H_R=\operatorname{span}\{|n\rangle:0\le n\le L\}\), nichtentartet,
  \(Q_R|n\rangle=n|n\rangle\);
* ein fester Referenzzustand \(\sigma\), unabhängig vom unbekannten Eingang;
* \(N=Q_S\otimes I+I\otimes Q_R\) und ein gemeinsamer Effekt
  \(0\le F\le I\), \([F,N]=0\);
* beide Messergebnisse \(F,I-F\) werden mitgezählt; keine nachträgliche
  Normierung auf einen akzeptierten Teil der Versuche;
* einmalige Verwendung und beliebige innerhalb der Gesamtladungsblöcke erlaubte
  Effekte. Physikalische Präparations-, Zeit- oder Energiebudgets fehlen noch.

Diese Ladung wird nicht mit der Staubmasse identifiziert. \(L+1\) zählt die
Referenzstufen, weder Kausalset-Elemente noch Geldkosten.

## 3. Globale Erhaltung erlaubt Austausch

Für \(0\le n<L\) haben \(|a,n+1\rangle\) und \(|c,n\rangle\) dieselbe
Gesamtladung \(n+1\). Eine Rotation in diesem Zweierraum, beispielsweise

\[
U_{n+1}=\begin{pmatrix}3/5&4/5\\-4/5&3/5\end{pmatrix},
\]

ist unitär und erhält \(N\), aber nicht \(Q_S\otimes I\) allein. Erhaltung der
Gesamtladung ist daher schwächer als ein Verbot jedes Sektorwechsels des Systems.
Eine fundamentale, auch mit Referenzsystemen geltende lokale Superselektion wäre
eine stärkere Annahme und würde diesen Austausch gerade ausschließen.

## 4. Scharfer Satz für einen festen Referenzzustand

Definiere die benachbarte Referenzkohärenz

\[
C(\sigma)=\sum_{n=0}^{L-1}|\sigma_{n,n+1}|.
\]

Der reduzierte Effekt wird durch
\(\operatorname{Tr}(E\rho)=\operatorname{Tr}(F(\rho\otimes\sigma))\)
festgelegt. Wegen der Gesamtladungsregel kann sein Kreuzmatrixelement nur die
folgenden Beiträge enthalten:

\[
E_{ac}=\sum_{n=0}^{L-1}\sigma_{n,n+1}
F_{a,n+1;c,n}.
\]

Für orthogonale normierte Vektoren \(u,v\) gilt für jeden Effekt
\(|\langle u,Fv\rangle|=|\langle u,(F-I/2)v\rangle|\le1/2\).
Also \(|E_{ac}|\le C(\sigma)/2\), und

\[
\tau\ge|\langle a,(E-P_+)c\rangle|
\ge\frac{1-C(\sigma)}2.
\tag{1}
\]

Diese Grenze wird erreicht. Setze in jedem Zweierraum
\((|a,n+1\rangle,|c,n\rangle)\) die Diagonale von \(F\) auf \(1/2\) und
\(F_{a,n+1;c,n}=e^{-i\arg\sigma_{n,n+1}}/2\).
Bei einem verschwindenden Kohärenzelement kann die Phase beliebig gewählt
werden. Jeder solche Block ist ein Rang-eins-Projektor. Auf den ungepaarten
Endpunkten \(|a,0\rangle,|c,L\rangle\) setze \(F=1/2\), auf dem gesamten
Komplement von \(\operatorname{span}(a,c)\otimes H_R\) setze \(F=0\).
Die Projektion auf dieses Komplement kommutiert mit \(N\).

Damit ist \(F\) ein invarianter Effekt und

\[
E=\frac12\begin{pmatrix}1&C(\sigma)\\C(\sigma)&1\end{pmatrix}\oplus0,
\qquad \|E-P_+\|=\frac{1-C(\sigma)}2.
\tag{2}
\]

Insbesondere ergibt eine ladungsdiagonale Referenz wieder genau \(1/2\).
Endpunkt- und Fehlerausgänge dürfen nicht weggelassen werden: Schon für die
gleichgewichtete Referenz mit \(L=1\) ändert Weglassen beider Endpunkte die
Erfolgswahrscheinlichkeit bei \(\psi_+\) von \(3/4\) auf \(1/2\).

## 5. Optimierung über alle Referenzen mit endlichem Träger

Sei \(p_n=\sigma_{nn}\). Positivität liefert
\(|\sigma_{n,n+1}|\le\sqrt{p_np_{n+1}}\). Für \(r_n=\sqrt{p_n}\)
gilt \(\sum r_n^2=1\) und

\[
C(\sigma)\le\sum_{n=0}^{L-1}r_nr_{n+1}=r^T T_L r,
\]

wobei \(T_L\) nur die beiden Nebendiagonalen \(1/2\) besitzt.
Mit den Randwerten \(r_{-1}=r_{L+1}=0\) löst
\(r_n\propto\sin((n+1)\theta)\) die Eigenwertgleichung
\((r_{n-1}+r_{n+1})/2=(\cos\theta)r_n\).
Die erlaubten Winkel sind \(\theta_k=k\pi/(L+2)\), \(1\le k\le L+1\).
Der größte Eigenwert ist daher \(\cos(\pi/(L+2))\). Er wird durch den reinen
Referenzzustand mit den positiven Amplituden

\[
r_n=\sqrt{\frac2{L+2}}\sin\frac{(n+1)\pi}{L+2}
\]

erreicht. Zusammen mit (2) ergibt sich der scharfe Satz

\[
\boxed{\tau_{\min}(L)=\frac{1-\cos(\pi/(L+2))}{2}>0
\quad\text{für jedes endliche }L.}
\tag{3}
\]

Für \(L=0\) ist die Grenze \(1/2\). Gleichmäßige statt sinusförmiger
Amplituden liefern nur \(\tau=1/[2(L+1)]\). Asymptotisch gilt für die optimale
Referenz \(\tau_{\min}\sim\pi^2/[4(L+2)^2]\).

| Geforderter universeller Fehler | Kleinster maximaler Ladungsindex L | Referenzstufen L+1 |
|---|---:|---:|
| höchstens 0,1 | 3 | 4 |
| höchstens 0,01 | 14 | 15 |
| höchstens 0,001 | 48 | 49 |
| höchstens 0,0001 | 156 | 157 |

Die Tabelle ist durch rationale Intervalle zertifiziert: Für jeden Eintrag liegt
die obere Fehlerschranke unter der Toleranz, beim unmittelbar kleineren \(L\)
die untere Schranke darüber. Das ist ein Messfehlerbudget im Zusatzmodell,
keine Ressourcen- oder Finanzzusage für eine reale Umsetzung.

## 6. Globale Invarianz und relative Phase ohne Verwechslung

Definiere die Gesamtladungsmittelung
\(\mathcal G(X)=\sum_q\Pi_q^N X\Pi_q^N\). Für invariante Effekte gilt exakt

\[
\operatorname{Tr}(F\mathcal G(\rho\otimes\sigma))
=\operatorname{Tr}(F(\rho\otimes\sigma)).
\]

Beispiel: \(L=1\), Referenz \((|0\rangle+|1\rangle)/\sqrt2\), und die
Eingänge \(\psi_\pm\). Nach globaler Mittelung sind beide lokalen
Systemmarginalen diagonal, aber die beiden gemeinsamen Zustände liefern am
invarianten Effekt die Wahrscheinlichkeiten \(3/4\) und \(1/4\).
Die Unterscheidung sitzt in der relativen, gemeinsamen Kohärenz.

Dies kann auch als algebraische relationale Kodierung
\(\rho\mapsto\mathcal G(\rho\otimes\sigma)\) gelesen werden. Die lokale
Marginale ist dann \(D(\rho)\), nicht der kohärente Eingangsparameter selbst.
Die physikalische Präparation dieser Familie, ihre Kalibrierung und ihre
Zulässigkeit unter tatsächlichen Constraints sind weiterhin zu begründen.
Eine unter einer stärkeren lokalen Superselektion verbotene Ressource wird
hierdurch nicht kostenlos erzeugt. Referenzverbrauch und wiederholte Nutzung
werden nicht zertifiziert.

## 7. Vollständiger Messraum und Instrument

Die scharfe obere Konstruktion in (2) kontrolliert ausdrücklich auch alle
weiteren Uhr- und Dichtemoden durch den Effekt null auf dem Komplement.
Sie **setzt** damit die modenselektiven Filter auf \(a,c\) voraus. Die
Phasenreferenz allein liefert diese Filter nicht. Fügt man zum gemeinsamen
Effekt die Identität auf einem orthogonalen, ladungsdefinierten Leckagemodus
hinzu, bleibt die Zweimodenkompression gleich, während der vollständige
Operatornormfehler eins wird. Ein Zweimodentest zertifiziert somit keinen
realen Detektor auf dem gesamten Historienraum.

Auf abstrakter Ebene besitzt jeder hier konstruierte invariante Effekt eine
ladungserhaltende Zweiausgangsrealisierung. Mit einem neutralen Zeiger lautet
eine unitäre Erweiterung auf zwei Zeigerkomponenten

\[
U_F=\begin{pmatrix}\sqrt F&-\sqrt{I-F}\\
\sqrt{I-F}&\sqrt F\end{pmatrix}.
\]

Die Einträge kommutieren, \(U_F\) ist unitär, und jeder Eintrag kommutiert mit
\(N\). Beim Zeigereingang 0 liefert Ausgang 0 den Effekt \(F\). Dies beweist
abstrakte Realisierbarkeit im Zusatzmodell. Es bestimmt weder ein physikalisches
CST-Wechselwirkungsgesetz noch eine eindeutige Zustandsänderung oder einen
beliebig oft nutzbaren Referenzapparat.

## 8. Kontrollen, Fehlergrenzen und Reproduktion

`analyze.py` verwendet nur rationale komplexe Zahlen und die Python-
Standardbibliothek. Die fünf Quellen einschließlich Lizenz sind mit Git-Blob-
Identitäten an den angegebenen Main-Commit gebunden. Der Plan-Hash lautet
`ed1552e6f65e16aeb142190e02a095af357e40888cb17e77501de86ecc5a4b4d`.

Geprüft werden 24 Identitäten auf einer Basis der Blockalgebra, eine exakt
unitäre Austauschmatrix, 336 Referenz-/Effektfälle und 2016 Born-/Mittelungs-
Identitäten für sechs Eingänge einschließlich eines Leckagemodus. In 192
Fällen verschwindet die benachbarte Kohärenz; alle ergeben den Fehler 1/2.
Die endlichen Kontrollen benutzen vier rationale Amplitudenprofile, drei
Mischparameter und vier komplexe Phasen. Sie sind keine Diskretisierung des
Staub-Kontinuums und ersetzen den allgemeinen Beweis nicht.

Die zehn Referenzbudgets und vier Minimalitätsgrenzen benutzen die Machin-Formel
\(\pi=16\arctan(1/5)-4\arctan(1/239)\), je 32 alternierende Terme mit
Restgliedeinschluss und nach außen gerundete rationale Intervallenden. Für den
Kosinus werden Grad 24 und der Rest \(|x|^{26}/26!\) verwendet. Das funktioniert,
weil das Taylorpolynom bis Grad 25 mit dem bis Grad 24 übereinstimmt. Die
Monotonie des Kosinus im verwendeten Bereich kontrolliert die Argumentintervalle.

Acht Negativkontrollen weisen falsche Zentralität, falsche lokale Erhaltung,
einen Vorteil ohne Referenzkohärenz, exakte Messung bei endlichem Träger,
ignorierte Leckage, verworfene Endpunkte, die unbewiesene Massenidentifikation
und eine veränderte Quelldatei zurück. `replay.py` berechnet die vier Ergebnis-
dateien isoliert neu und verlangt Bytegleichheit. Keine externe Replikation,
kein Beweisassistent, kein n=5-Produktionslauf und keine kostenpflichtige
Rechenleistung.

## 9. Die jetzt präzise offene physikalische Entscheidung

| Physikalisch zu begründende Auswahl | Konsequenz |
|---|---|
| Vollständige lokale Algebra und alle zulässigen Operationen erhalten die Strata | Das kohärente Ziel ist keine verfügbare lokale Observable; Zielvertrag ändern. |
| Nur globale Ladungserhaltung, zulässige Referenz und relative Kodierung | Der bedingte Satz gilt; tatsächliche Ladung, Referenzpräparation, Modenfilter und Instrument herleiten. |
| Keine entsprechende Erhaltungsrestriktion auf der vollen Algebra | Das abstrakte Ziel ist erlaubt; die physikalische Kopplung bleibt herzuleiten. Der endliche Ladungssatz ist dann kein universelles CST-Verbot. |

Die vorhandene Record-Wirkung wählt keine dieser Zeilen aus. Der nächste
physikalische Vertrag muss Observable-Algebra, Zustands-/Constraintbereich,
zulässige Referenzsysteme und ihre kausalen Operationen gemeinsam festlegen.
Erst danach ist eine Zielmessung oder ein weiterer großer Integrationslauf
physikalisch interpretierbar. Zusätzliche n=5-Feldintegrale allein entscheiden
diese Definitionsfrage nicht. MODEL, BOUNDARY, CURRENT, CORRESPONDENCE,
TRAPPING, REGULARITY, EXTENSION und BOUNCE bleiben HOLD.

## 10. Primärquellen und Einordnung

1. [Projektbasis PR 263](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/263)
   und die fünf in `provenance.json` identifizierten Dateien.
2. S. D. Bartlett, T. Rudolph, R. W. Spekkens,
   [Reference frames, superselection rules, and quantum information](https://arxiv.org/abs/quant-ph/0610030),
   Rev. Mod. Phys. 79, 555 (2007). Bezug: globale/lokale Superselektion,
   Quantenreferenzen und relationale Kodierungen.
3. D. W. Berry, H. M. Wiseman,
   [Optimal states and almost optimal adaptive measurements for quantum interferometry](https://arxiv.org/abs/quant-ph/0009117),
   Phys. Rev. Lett. 85, 5098 (2000). Bezug: optimierte endliche Phasenreferenzen
   und Phasenschätzung. Ihre Phasenvarianz ist nicht unser Operatornormfehler;
   die konkrete Gleichung (3) ist oben unabhängig für den erklärten Effekt bewiesen.
4. M. Ozawa,
   [Conservation laws, uncertainty relations, and quantum limits of measurements](https://arxiv.org/abs/quant-ph/0112154),
   Phys. Rev. Lett. 88, 050402 (2002). Bezug: Messgrenzen durch Erhaltungsgesetze.
   Der dortige Rauschoperator wird hier nicht mit \(\tau\) gleichgesetzt.

Es wird weder Neuheit der Referenzmethodik noch eine Bestätigung der
CST-Physik durch diese Quellen behauptet.
