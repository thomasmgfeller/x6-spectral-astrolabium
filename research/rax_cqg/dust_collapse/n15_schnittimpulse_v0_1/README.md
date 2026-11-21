# Lässt sich der Anfangsstrom aus den Uhrimpulsen eines Zwischenschnitts rekonstruieren?

**CST-DUST · N15, Typ 375841 · 21. November 2026**

Für die zwei publizierten Paketpaare unterscheiden sich die ersten Uhrableitungen am Zwischenschnitt. Ein neues Paar widerlegt die allgemeine Rekonstruktion aus diesen Daten. Seine erste Antwort ist auch bei gleicher Gesamtdichte identisch, während die Anfangsströme entgegengesetzt sind. Eine zweite Uhrableitung liefert eine exakte Rückrechnung, falls Uhrprofil, Schnitt- und Zukunftsdichten und die tatsächliche innere Dichtesumme mitgegeben werden. Eine zusätzliche Kontrolle zeigt, wie viel Information ohne diese Summe selbst bei vollständiger lokaler Quellenantwort fehlt. [Vorarbeit, PR #341](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/341)

## 1. Quellen am Schnitt

Beide Feinhistorien jeder Paarung haben die gleiche Ordnung, dieselben Uhren, Skalarfelder und Zukunftsdaten und die Präparation bei markierter Masse $M=1/4$. Wir benutzen $Y=T/\Delta$, $W=w/\Delta$ und $\Delta^4=3/722$. Die Antikette bei $Y=0$ enthält die Ereignisse 5 und 11. Definiere $E_s=\partial_{T_s}S$ und $H_{ss}=\partial^2_{T_s}S$ als Variationen der Wirkung bei festgehaltenen übrigen Feldern und Paketfenstern. Für den quadratischen Staubanteil gilt

$$
19E_s=W_s\sum_{i\prec s} b_{is}(Y_i-Y_s)-\sum_{j\succ s}b_{sj}W_j(Y_s-Y_j),
\qquad
-19\Delta H_{ss}= W_s\sum_{i\prec s}b_{is}+\sum_{j\succ s}b_{sj}W_j.
$$

Die Eingangsterme und Ausgangsterme beider Uhrimpulse werden getrennt geprüft. Der durch eine gemeinsame Verschiebung des *ganzen* Ordnungsideals gewonnene Gesamtfluss aus PR #341 enthält weitere Kreuzbeziehungen. Die Wirkung bestimmt die Ableitungen. Ihre Realisierung durch ein physikalisches Messinstrument ist offen. [Wirkung und Paketgeometrie](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/b64c528f6d0fffaffc3bdb314260f1f348d48cb1/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/Teilartikel.md)

| Paar bei gepaarten Feldern | Differenz $E_{11,+}-E_{11,-}$ im Zentrum | Differenz $\Delta(H_{11,+}-H_{11,-})$ im Zentrum |
|---|---:|---:|
| Originalpaar aus PR #340 | −0,001428554 | +0,000870355 |
| Gegenpaar aus PR #341 | −0,000829782 | +0,000499599 |
| Neues Paar bei gleicher innerer Dichtesumme | exakt 0 | +0,000000448553 |
| Zusatzkontrolle bei variabler innerer Dichtesumme | exakt 0 | exakt 0 |

Die Differenz der ersten Antwort ist bei den publizierten Paaren auf den ganzen gepaarten Zellen von null getrennt. Eine gepaarte Differenz ist noch keine fehlerfreie Klassifikation unbekannter Einzelbelegungen. [Rationale Einschlüsse](ergebnis.json)

## 2. Ein Gegenpaar trotz gleicher Summe, Wirkung und erster Impulse

Die inneren Ketten sind $4\prec5\prec14$ und $6\prec11\prec12\prec13$. Die normierten Uhren $u_4,u_6$ werden im gemeinsamen Zentrum um $+1/128,-1/128$ verschoben und bleiben im ursprünglichen Uhrfenster mit Halbbreite $1/64$. Die offenen Zellen in $e,u,\xi$ behalten die Halbbreite $10^{-7}$. Das Zentrum der normierten Dichte $x=w/[M\Delta(4-e)]$ erhält auf 12 den Zusatz $1/8320$, auf 13 den Zusatz $-1/8320$. Diese gemeinsame Verschiebung setzt die Ladung des Zentrums vor der Aufspaltung auf null. Die Konstruktion testet Eindeutigkeit. Sie bestimmt keine Häufigkeit im Ensemble.

Sei $C_j=1+\sum_{i\prec j} b_{ij}(Y_i-Y_j)^2/19$. Setze $r=b_{11,13}(Y_{11}-Y_{13})$, $t=-b_{11,12}(Y_{11}-Y_{12})$, $a=C_4-C_6$ und $h=(C_{12}-C_6)r+(C_{13}-C_6)t$. Wir addieren und subtrahieren auf vier Dichteachsen den Vektor

$$
(d_4,d_6,d_{12},d_{13})=10^{-4}(-h,\,h-a(r+t),\,ar,\,at).
$$

Die Translation hat bei festen Uhren Jacobi-Determinante eins. Beide ganzen Zellen liegen strikt in den ursprünglichen 1-%-Dichtebändern. Identisch gelten $\sum d_v=0$, $\sum C_vd_v=0$ und $-t d_{12}+r d_{13}=0$. Damit stimmen die Gesamtdichte, die Wirkung und der abgehende Beitrag bei 11 überein. Beide ankommenden Beiträge und der abgehende Beitrag bei 5 bleiben ebenfalls gleich. Die ersten Dichteableitungen hängen bei festen Uhren und fester Ordnung nur von diesen Uhren ab. Für die Skalarableitungen werden dieselben Skalarfelder verwendet.

Am Zentrum betragen die beiden Anfangsladungen exakt $\pm2903583/473169920000$. Auf den ganzen Zellen gilt $p_+>4{,}61\cdot10^{-6}$ und $p_-<-4{,}61\cdot10^{-6}$. Die beiden ersten Schnittimpulse, die Feldwerte am Schnitt und die Zukunftsdaten liefern dieselbe Eingabe. Auch die kohärenten Amplituden gegen jede gemeinsame beschränkte Testfunktion dieser Daten stimmen überein, weil die Paarzuordnung das Mass und die Wirkung erhält.

Die zweite Uhrantwort bei 11 erfüllt über die ganzen gepaarten Zellen $4{,}46\cdot10^{-7}<\Delta(H_{11,+}-H_{11,-})<4{,}52\cdot10^{-7}$. Der Unterschied überlebt die Integration. In $\partial^2 e^{iS}=(iH-E^2)e^{iS}$ fällt der Term mit $E^2$ beim Paketvergleich weg. Nach Ausklammern der gemeinsamen Gravitationsphase und des Skalarzustands gilt $\operatorname{Re} e^{iS_d}>4/5$ auf der ganzen Zukunftsbox. Der Realteil von $-i\Delta\,\partial^2_{T_{11}}(A_+-A_-)$ je Paketmass übersteigt deshalb $3{,}5\cdot10^{-7}$. Diese Schranke betrifft die Amplitudenantwort.

## 3. Rückrechnung unter benannten Zusatzdaten

Vorgegeben werden die Uhren, die zwei Schnittdichten, die vier Zukunftsdichten und die tatsächliche Summe $W_{\rm ges}$ aller sieben inneren Dichten. Nach Einsetzen der bekannten Eingangs- und Zukunftsterme in $E_s$ ist $J_s=\sum_{j\in I,\,s\prec j} b_{sj}W_j(Y_s-Y_j)$ bestimmt. Aus $H_{11,11}$ folgt auf dieselbe Weise $L_{11}=W_{12}-9W_{13}$. Für $a_0=Y_{11}-Y_{12}$ erhält man

$$
W_{14}=\frac{J_5}{Y_5-Y_{14}},\qquad
W_{13}=\frac{J_{11}-a_0 L_{11}}{9(Y_{13}-Y_{12})},\qquad
W_{12}=L_{11}+9W_{13}.
$$

Die Uhrabstände in den Nennern haben im ganzen ursprünglichen Uhrfenster einen Betrag von mindestens $783/1280$. Die Summe liefert nun $W_4+W_6$. Die Anfangskoeffizienten $g_v=\sum_{i\in P}b_{iv}(Y_i-Y_v)$ erfüllen $g_4=g_6$, weil die vier Kantenkoeffizienten bei 4 und 6 identisch sind und sich zu null addieren. Deshalb liefert

$$
19p_P=g_4(W_4+W_6)+g_5W_5+g_{11}W_{11}+g_{12}W_{12}+g_{13}W_{13}+g_{14}W_{14}
$$

Betrag und Vorzeichen der ursprünglichen Ladung. Uhrprofil und Dichtesumme sind dabei mitgegebene Zusatzdaten. Die lokalen Felder der Antikette allein stellen sie nicht bereit.

Auf den hier geprüften Zellen kann auch der schnittübergreifende Gesamtfluss des Ideals $Y=0$ die Krümmung ersetzen. Nach Bestimmung von $W_{14}$ liefert er die zweite Gleichung zur Trennung von $W_{12}$ und $W_{13}$. Der exakte Determinantentest schliesst null auf den vier Testfällen aus. Für die Krümmungsvariante gilt die stärkere Nennerschranke auf dem gesamten ursprünglichen Uhrfenster. [Ausführbare Inversion](rueckrechnung.py) · [Schranken](rekonstruktion.json)

## 4. Was ohne unabhängige Summeninformation fehlt

In einer Zusatzkontrolle entfällt die Gleichheit der inneren Dichtesummen. Die markierte Masse, die Präparation, die Uhren und alle Dichtebänder bleiben gleich. Vom selben gemeinsamen Zentrum wie in Abschnitt 2 werden nur $x_4,x_6$ um $\pm(C_6,-C_4)/64$ verschoben. Die Wirkung und das Integrationsmass stimmen wieder überein. Die unterschiedlichen Summen sind innerhalb der erlaubten 1-%-Bänder möglich, da $C_4\ne C_6$. Die veränderten Dichten sitzen an Empfängern vor dem Schnitt. Ihre Wirkungsterme hängen weder von den Schnitt- noch von den Zukunftsfeldern ab.

So haben beide Pakete bei beliebigen gemeinsamen endlichen Quellenänderungen an Schnitt und Zukunft dieselbe Wirkung, wenn die übrigen Felder und die ursprünglichen Paketfenster bei der Quellenvariation festgehalten werden. Auch der schnittübergreifende Gesamtfluss ist gleich. Die Anfangsladungen im Zentrum betragen jedoch $\pm2601/757071872$, die Zellen tragen durchgehend entgegengesetzte Vorzeichen. Daher kann eine allgemeine Rekonstruktion selbst bei mitgegebenem Uhrprofil nicht allein auf der vollständigen lokalen Quellenantwort beruhen. Dieses Ergebnis grenzt den fehlenden Eingang der Rückrechnung ein. Andere unabhängige Information über die früheren Dichten könnte die Dichtesumme ersetzen.

## Nachrechnung und Geltungsbereich

Die drei Programme verwenden ausschliesslich die Python-Standardbibliothek. Vom Studienordner aus die Prüfsummen mit `sha256sum -c SHA256SUMS` prüfen und `python3 -B schnittimpulse.py`, `python3 -B rueckrechnung.py` und `python3 -B gegenprobe.py` ausführen. Die zugehörigen Ergebnisdateien sind [ergebnis.json](ergebnis.json), [rekonstruktion.json](rekonstruktion.json) und [gegenprobe.json](gegenprobe.json).

Die Identitäten des Verschiebungsvektors sind zusätzlich auf einem unisolventen Gitter mit 729 Punkten für den Grad der Polynome geprüft. Die unabhängige Gegenrechnung rekonstruiert die Wirkung aus einzelnen Intervallzählungen und benutzt exakte symmetrische Differenzen für beide Ableitungen. Sie umfasst 100 rationale Paketpaare und 32 weitere Feldbelegungen aus der breiteren Präparation. Beide Rückrechnungswege liefern jeweils in **232 Prüfungen** exakt die direkt aus der Anfangsvariation bestimmte Ladung. Ein absichtlicher Tausch der Summeninformation kehrt bei allen 25 geprüften Paaren der Zusatzkontrolle das Ergebnisvorzeichen um.

Der [Prüfvertrag](pruefvertrag.json) wurde vor der neuen Rechnung lokal festgelegt. Die publizierten Paketpaare waren bekannt. Die konkreten Zentren und Verschiebungen sind konstruierte Gegenbeispiele. Die Kontrolle bei verschiedenen Summen und die alternative Inversion über den Gesamtfluss entstanden ergänzend. Der Versuch betrifft diese endliche Ordnung und die ausgewiesene Präparation. Die physikalische Auslese und die Paarung des gekoppelten Rands bleiben offen. [Quellenstand](quellen.json) · [Lizenz](LICENSE) · [NOTICE](NOTICE)
