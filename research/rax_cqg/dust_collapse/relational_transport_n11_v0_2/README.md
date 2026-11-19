# Staubuhrschnitte mit kausaler Vergangenheit

**CST-DUST · Relationaler Transport v0.2 · 19. November 2026 · Physikalische Etappe 6 auf HOLD**

Auf jeder der beiden festen N11-Ordnungen reichen am Schnitt die freigegebene kausale Vergangenheit und die Uhrwerte ihrer inneren Ereignisse. Einzelne Angaben darüber, welche verdeckten Uhren unter der Schwelle liegen, müssen nicht gespeichert werden. Das gilt für einen einzelnen und für zwei aufeinanderfolgende Schnitte. Werden die Alternativen „noch leer“ und „bereits besetzt“ jedoch mit einer orthogonalen Markierung unterscheidbar gemacht, sinkt am bisherigen Detektor die spätere Trefferquote. Das Schnittdatum lässt sich in einer Rechnung mitführen. Seine physikalische Messung ist ein eigener Eingriff.

## 1. Welche Daten genügen?

Fixiere eine endliche Kausalordnung $P$ und unabhängige stetige Uhren $T_i$, hier gleichverteilt auf $[-3/2,3/2]$. Für die N11-Innenrechnung sind die äusseren Uhren bei der Verklebung zunächst fest. Die beiden betrachteten Schnitte liegen nach allen vergangenen und vor allen zukünftigen Kragenuhren der benutzten Pakete. Ein Ereignis $j$ wird erstmals bei $U_j=\max_{i\preceq j}T_i$ freigegeben. Das freigegebene Ideal $D_s=\{j:U_j\le s\}$ enthält mit jedem Ereignis alle Vorgänger. Die Information am Schnitt ist die Menge $D_s$ samt den freigegebenen Uhren $T_i$, $i\in D_s$. Auf einer vorgegebenen Ordnung lässt sich der gesamte frühere Freigabeverlauf daraus rekonstruieren.

Sei $F(D)$ die Menge der minimalen Ereignisse im Komplement eines Ideals $D$. Es gilt genau

$$
D_s=D\ \Longleftrightarrow\ T_i\le s\ (i\in D),\qquad T_j>s\ (j\in F(D)),
$$

wobei alle anderen Uhren frei bleiben. Denn jedes ausgeschlossene Ereignis hat einen minimalen ausgeschlossenen Vorgänger oder ist selbst minimal. Zwischen einem Teil der freigegebenen Vergangenheit und ihrer noch unerreichten Fortsetzung gibt es deshalb keine zusätzliche Entscheidung über die übrigen Uhrwerte. Für $p_s=(s+3/2)/3$ hat dieses Rechteck $B_s(D)$ das Mass $q_s(D)=p_s^{|D|}(1-p_s)^{|F(D)|}$. Die Bedingung am minimalen Rand ist wesentlich. Ohne sie summiert sich beim Schnitt 0 die Masse aller Rechtecke für die Kette C0 zu 15/8 und für C1 zu 21/8.

Bei gegebenem $D_s$ und seinen Uhrwerten sind die verbleibenden Uhren unter dem Referenzmass unabhängig. Die Uhren der gegenwärtig minimalen Ergänzungen liegen oberhalb von $s$, die übrigen besitzen weiter ihr ursprüngliches Mass. Wird eine neue Ergänzung freigegeben, dürfen ihre bislang verdeckten Nachfolger ältere rohe Uhrwerte haben und zugleich mit ihr eintreten. Es wird nach der vorgegebenen Kausalordnung fortgeschritten. Auf eine bestimmte künftige Uhrbelegung braucht das Verfahren nicht zuzugreifen.

## 2. Norm und Zusammensetzung

Für den ungewichteten Idealprozess lautet der Übergang von $D$ nach $E$ bei $s<t$

$$
K_{s,t}(D,E)=\mu(B_s(D)\cap B_t(E))/q_s(D).
$$

Für einen Zustand mit gespeicherten Uhrwerten in $D$ bleiben diese Werte fest. Sie liegen bei späteren Schnitten ohnehin unterhalb der Schwelle. Welche Ereignisse neu hinzukommen, hängt bei festen Ordnungsdaten nur vom aktuellen Ideal ab. Für die Wirkungsfaktoren können deren alte Uhrwerte dagegen erforderlich sein.

Die Information $\mathcal F_s$ aus Ideal und freigegebenen Uhrwerten ist eine aufsteigende Familie. Der Schnittraum trägt die positive Norm $\|f\|_s^2=\mathbb E_\mu |f(D_s,T_{D_s})|^2$. Das entspricht einer Summe über die Ideale mit Gewichten $q_s(D)$ und normiertem Produktmass der Uhren in $D$. Diese Norm folgt aus der gewählten Referenzverteilung. In N11 wird der geerbte bedingte Skalarraum am äusseren Rand verwendet.

Jedes analytisch integrierte innere Dichtemittel $H_j$ hat Betrag höchstens eins. Es wird wirksam, sobald das Ereignis und alle für seinen Wirkungsterm benötigten inneren Uhren vorliegen. Bezeichne mit $A_s$ die Menge solcher fertigen Faktoren und mit $Z_{s,t}$ das Produkt der bis $t$ neu fertigen Faktoren. Auch bei der C0-Staubkontrolle auf der C1-Geometrie wird jeder Term bis zum Eingang seiner tatsächlich benötigten Uhren zurückgehalten. Der Rückwärtstransport von Endfunktionen ist

$$
L_{s,t} f = \mathbb E_\mu[Z_{s,t} f\mid\mathcal F_s].
$$

Die bedingte Erwartung und $|Z_{s,t}|\le1$ geben $\|L_{s,t} f\|_s\le\|f\|_t$. Für drei Schnitte liefert die Turmeigenschaft zusammen mit $Z_{s,t}Z_{t,u}=Z_{s,u}$ die exakte Zusammensetzung $L_{s,t}L_{t,u}=L_{s,u}$. Am Ende werden die verbleibenden Faktoren, Zukunftsphase, feste Gravitationsphase und die skalare Randkarte eingesetzt. Bei den N11-Endkragen können innere rohe Uhren ausserhalb der äusseren Kragenuhrwerte liegen. Die Endintegration umfasst weiterhin ihren gesamten Träger. Die Zweiggewichte 1/2 bleiben erhalten. Es findet keine Messung des zwischenzeitlichen Zweigs statt.

Dies ist eine Aussage auf jeder vorgegebenen Gesamtordnung. Sich auf die induzierte Vergangenheit beider unbekannter Ordnungen gemeinsam zu beschränken ist eine stärkere Forderung. Im leeren N11-Inneren ist die induzierte Vergangenheit in C0 und C1 gleich, einschliesslich der identisch gesetzten Kragendaten. C0 hat eine minimale Ergänzung, C1 hat zwei. Bedingt auf einen leeren Schnitt bei 0 ist die Wahrscheinlichkeit, im **Referenzmass** bis 1/4 leer zu bleiben, für C0 genau 5/6, für C1 genau 25/36. Eine gemeinsame Zahl für diesen Übergang weicht in mindestens einem der beiden Fälle um mindestens 5/72 ab. Das schliesst eine einzige, beide zweigspezifischen Referenzgesetze reproduzierende Wahrscheinlichkeit aus dem induzierten leeren Ideal allein aus. Ein aus der Gesamtwirkung hergeleitetes Gesetz für unbeobachtete Fortsetzungen ist damit weiterhin möglich. Die Referenzzahlen sind keine physikalischen Geburtsraten.

## 3. Komplexer N11-Endvergleich

Der Direktweg, der Weg über 0, der Weg über 1/4 und der Weg über beide Schnitte in dieser Reihenfolge wurden bei identischer Präparation und Auslese gerechnet. Die zusammengesetzte Rechnung integriert die neuesten, neu freigegebenen und früheren Uhren stufenweise auf den durch die Idealfolge bestimmten Produktintervallen. Sie bildet die Schnitte kohärent ab. Im gekoppelten Modell und in der Kontrolle mit gemeinsamem C0-Staubtransfer wurden beide Zweigdiagonalen, der komplexe Koeffizienten-Kreuzterm und alle drei unbedingten Endausgänge verglichen. Die maximale absolute Abweichung der Schnittwege zum Direktweg beträgt rund $4{,}44\times10^{-16}$ bei einem Prüflimit von $5\times10^{-9}$. Die des neuen Direktwegs zur archivierten Rechnung aus PR 322 liegt unter $2{,}8\times10^{-17}$.

Die Ein-Paar-Trefferquote beim geteilten Paket beträgt auf allen vier Wegen rund 11,00179 %. Die positiven Dichtefenster bei 1/8 und 1/4 liefern dieselben inklusiven Paarungen, da sich ihre gemeinsame Anfangsphase punktweise herauskürzt. Die Rechnungen verwenden die kalibrierte Einpuls-Auslese v0.5 und deren Referenzpuls $t_2=1$. Die kontinuierliche Gliederungsidentität ist analytisch. Die absoluten Dezimalwerte der N11-Uhrquadratur bleiben numerische Ergebnisse.

## 4. Ist die Leerheit des Schnitts störungsfrei ablesbar?

Der ergänzende Versuch kopiert die binäre Eigenschaft „$D_s$ leer oder besetzt“ ideal in zwei orthogonale Zustände eines Hilfsregisters. Danach werden beide Ausgänge ohne Auswahl summiert. An der Eingangspräparation und am Enddetektor ändert sich sonst nichts. Der eindeutige Ein-Paar-Ausgang schliesst C0 aus, sodass der Vergleich nur die beiden Alternativen innerhalb von C1 betrifft. Die Annahme einer idealen Kopie definiert den Versuch. Ihre technische Realisierbarkeit folgt daraus nicht.

Für festes äusseres $t$ seien $A(t),B(t)$ die unnormierten C1-Staubamplituden des leeren und des besetzten inneren Schnitts. Beim direkten Übergang ist die Trefferwahrscheinlichkeit $\eta_1\,\mathbb E_t|A+B|^2/4$. Bei orthogonalen Markierungen lautet sie $\eta_1\,\mathbb E_t(|A|^2+|B|^2)/4$. Die Differenz ist ein experimentell definierter Interferenzbeitrag im bedingten Modell.

| Geteiltes Eingangspaket | Ohne Markierung | Markierung, Ergebnis ungelesen | Differenz in Prozentpunkten | Bewiesene Untergrenze |
|---|---:|---:|---:|---:|
| Schnitt 0 | 11,00179 % | 6,95097 % | 4,05082 | > 2,7602 |
| Schnitt 1/4 | 11,00179 % | 7,94042 % | 3,06137 | > 1,6690 |

Die positiven Differenzen lassen sich unabhängig von einer Quadraturfehlerschätzung herleiten. Bei festem $t$ seien $X,Y$ zwei unabhängige Belegungen der inneren Uhren und Dichtemarken, $\Phi$ die reelle C1-Staubphase ohne gemeinsame Anfangsphase und $v=(1-p_s)^2$ die Masse des leeren Ereignisses. Dann ist $\operatorname{Re}(A^*B)$ das Integral von $\cos(\Phi_X-\Phi_Y)$ über „$X$ leer, $Y$ besetzt“. Der zweite Moment der Phasendifferenz auf diesem Teil des Produktraums ist wegen Vertauschungssymmetrie höchstens $\mathrm{Var}(\Phi\mid t)$. Mit $\cos z\ge1-z^2/2$ und $\mathbb E_t\mathrm{Var}(\Phi\mid t)\le\mathrm{Var}(\Phi)$ folgt

$$
P_{\mathrm{ohne}}-P_{\mathrm{markiert}}\ \ge\frac{\eta_1}{4}\,[2v(1-v)-\mathrm{Var}(\Phi)].
$$

Die rational eingeschlossenen Phasenvarianzen aus v0.1 werden im Paket exakt neu berechnet. Für die Effizienz gilt die archivierte exakte Untergrenze $\eta_1>0{,}4956269034$. Für das geteilte Paket liefert die rechte Seite an beiden Schnitten die in der Tabelle abgerundeten positiven Grenzen. Auch für die scharfe und die schmale Präparation liegen exakte Grenzen und numerische Werte vor. Das Ergebnis schliesst die störungsfreie ideale Markierung dieser binären Alternative beim bisherigen Enddetektor aus. Es klassifiziert weder sämtliche möglichen Uhrmessungen noch Dekohärenz in einer anderen Präparation. Das Weglassen nichtkausaler Rohmasken aus v0.1 und die hier untersuchte Markierung sind verschiedene Eingriffe.

## 5. Kontrolle an acht Ereignissen im flachen 1+3-Raum

Zur Prüfung des Übergangsgesetzes wurde eine feste Geometrie gewählt. Vier Ereignisse liegen zur Zeit 0 an den Ecken des Tetraeders $(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)$. Vier weitere liegen zur Zeit 3 an den jeweils am Ursprung gespiegelten Orten. Beim Übergang zur gleichen Ecke im gespiegelten Tetraeder ist das Quadrat des räumlichen Abstands 12, bei den drei anderen 4. Daraus folgen bei Zeitabstandsquadrat 9 genau zwölf strikte zeitartige Paare. Es gibt keine lichtartigen Paare. Die Koordinaten spannen den affinen 1+3-Raum auf. Die eingebettete Minkowski-Zeit definiert hier die Ordnung, die separat integrierten Staubuhren definieren die Schnitte.

Die Ordnung hat 35 Ideale. Die Uhren wurden für die Schwellen $0,1/4,1/2$ in vier Intervalle mit Gewichten $(6,1,1,4)/12$ zerlegt. Alle $4^8=65\,536$ Zuweisungen wurden gezählt. Die so bestimmten gemeinsamen Dreizeitgewichte stimmen für alle $35^3=42\,875$ Idealtripel exakt mit dem Produkt der bedingten Übergänge überein. 3 226 Tripel tragen positives Gewicht. Auf demselben Träger wurde zusätzlich die Staubamplitude mit einem Mittelpunkt je Uhrintervall und dem vollständigen Atom-/Intervallmass jeder Dichte berechnet. Die zwölf Kanten haben alle Schichtkoeffizient eins. Die Gravitationsphase der ungerandeten Testordnung hat in der übernommenen Konvention die Wirkung $8-12=-4$.

Die direkte komplexe Summe ist rund $0{,}3338148990+0{,}0912784352\,i$. Eine zweite Implementierung erzeugt beim Fortschreiten nur jeweils kausal freigegebene Uhrwerte. Sie erreicht bei zwei oder drei Zwischenschnitten jede vollständige Belegung genau einmal, mit einer numerischen Amplitudendifferenz unter $4\times10^{-16}$. Vier Mittelpunkte definieren diese endliche Amplitudenprobe. Eine Genauigkeitsaussage für die feinere kontinuierliche 4D-Amplitude wurde daraus nicht abgeleitet. Dieser flache Träger hat weder eine dynamisch erzeugte Staubballgeometrie noch den physikalischen Innen-/Aussenrand oder einen P3-Messadapter.

## Stand für den Staubball

Geprüft sind die kausale Rechnung ohne künftige Uhrenablesungen auf fester Ordnung, ihre Zusammensetzung und der Verlust von Endinterferenz bei einer idealen binären Zwischenablesung. Offen ist eine gemeinsame **kohärente Regel für mögliche Fortsetzungen bei identischer sichtbarer Vergangenheit**. Sie muss erklären, welche Ergänzungen zugelassen sind, wie sie aus der Wirkung gewichtet werden und wie ihre Beiträge am Endrand zusammengesetzt werden. Aus diesem Zwischenergebnis folgen weder eine physikalische 4D-Norm noch eine absolute Zähldichte. Etappe 6 bleibt auf HOLD, der physikalische P3-Ressourcenpilot bei M=1 bleibt bei 0 von 38 Vergleichen.

## Nachrechnung

Python 3.12 mit NumPy 2.3.5 und SymPy 1.14.0 genügt. Im entpackten Ordner ausführen:

    sha256sum --check SHA256SUMS
    OPENBLAS_NUM_THREADS=1 python3 -B verify.py

Die Prüfung vergleicht die exakten Ergebnisse, alle numerischen Endwerte und die unabhängige 4D-Vollsumme. Die vollständige Ausführung benötigt weder Netzwerk noch Zufallsziehungen. Die Ausgangsprüfung ist in contract.json dokumentiert, die anschliessend festgelegte Interferenzprüfung in record_contract.json. Herkunft und Git-Objekte der übernommenen Eingaben stehen in provenance.json. [N11-Ausgangsstudie auf main nach PR 322](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/502214f03c7fe72b1540634cd136f256d31d2847/research/rax_cqg/dust_collapse/relational_transport_n11_v0_1)
