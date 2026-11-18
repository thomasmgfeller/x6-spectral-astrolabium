# CST-DUST · Anfangspräparation am Vergangenheitskragen

**18. November 2026 · Zwei N11-Historien, Version 0.1.** Eine isolierte Änderung der Anfangsdichte bleibt bei festen Randuhren exakt unbeobachtbar. Ein gemeinsames kohärentes Uhr- und Dichtepaket macht einen kleinen Dichteunterschied am selben Zukunftsdetektor sichtbar. Die Stärke und das Vorzeichen hängen von der gewählten Präparation ab. Die physikalische Auswahl der Randpaarung und eine Dynamik der Geometrie bleiben offen.

[Einseitiger Ergebnisbericht (PDF)](../reports/CST_DUST_Anfangspraeparation_v0_1.pdf) · [Prüfpaket (ZIP)](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/rax_cqg/dust_collapse/packages/CST_DUST_Anfangspraeparation_v0_1_Pruefpaket.zip) · [Rand- und Auslesevertrag aus PR 293](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/rax_cqg/dust_collapse/PHYSICAL_BOUNDARY_READOUT_PUBLICATION.md)

## 1. Was wird gemeinsam gepaart?

Beide Kausalordnungen verwenden denselben Vergangenheitskragen mit Knoten 0–3, dasselbe Innere mit Knoten 4–6 und denselben Zukunftskragen mit Knoten 7–10. Die gemeinsame **kollektive** Anfangsdichte $r$ belegt alle vier vergangenen Knoten. Eine Uhr $t=T_3$ darf variieren. Alle übrigen äusseren Uhren behalten ihre affinen Werte. Die Zukunftsdichte beträgt durchgehend $1/8$. Skalarquotient, Phase, beide Historiengewichte $1/2$ und der lokale Gaußdetektor an $q_7$ stammen aus [PR 293](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/293). Der Skalarabschnitt setzt $q_0=0$.

Für dieses Präparationsprotokoll wählen wir die positive Paarung in $L^2(\mu;H_3)$ mit $H_3=L^2(\mathbb R^3)$ und

$$
d\mu(r,t)=\tfrac12(\delta_0+\mathbf{1}_{(0,1)}\,dr)\,dt/3,\qquad -3/2\le t\le3/2.
$$

Sie übernimmt die normierten Ein-Koordinaten-Masse des Vorgängers. Der gemeinsame Dichtewert ist eine eigene kollektive Koordinate. Vier unabhängige kontinuierliche Randdichten hätten auf ihrer Diagonalen Mass null. Die neue Annahme ist deshalb als eigene Präparation deklariert. Als akzeptierte Randmode wählen wir die normierte konstante Funktion 1 auf dem gesamten Raum. Eine normierte Eingangsform $f$ liefert den Erfolgsoperator

$$
K_f=\sum_{c=0}^1 \tfrac12\!\int f(r,t) W_c(r,t)\,d\mu(r,t)\, V_c .
$$

Die Beträge der inneren Amplituden sind höchstens eins, weil die Wirkung reell und das innere Mass normiert ist. Die $V_c$ sind im bedingten Drei-Moden-Vertrag unitär. Cauchy–Schwarz ergibt $\|K_f\|\le1$. Zu den drei positiven Zeigereffekten kommt somit der positive Fehlschlageffekt $I-K_f^\dagger K_f$. Entsprechend ist die lineare Abbildung vom gemeinsamen Eingangsraum nach $H_3$ kontraktiv. Diese Konstruktion begründet die Wahrscheinlichkeitsbilanz für den gewählten Versuch. Die ursprüngliche Wirkung wählt weder den kollektiven Randsektor noch den konstanten Analysator eindeutig aus. Eine physikalische Auswahl durch Constraints oder ein vollständiges physikalisches Skalarprodukt bleibt ausstehend.

## 2. Uhr und Skalar getrennt variieren

Bei fixiertem $t$ gilt für **beide** Historien $W_c(r,t)=\exp[-irB(t)/2]v_c(t)$, wobei $B(t)=\sum_{j=0}^{3}C_j(t)$. Die Vergangenheitsterme sind unabhängig von den inneren Uhren. Deshalb fällt die Phase für jedes feste Uhrprofil aus allen Wahrscheinlichkeiten heraus, auch aus der Fehlschlagwahrscheinlichkeit. Für den affinen Referenzwert $t_0=-2\Delta$ ist $B(t_0)=151/19$. Die innere Uhrkopplung an $T_3$ ist für alle drei inneren Knoten in beiden Ordnungen vorhanden.

| Variation | Unterer Wert | Referenz | Oberer Wert |
|---|---:|---:|---:|
| Uhrverschiebung $T_3-t_0$, zentrierter Skalar | −1/16 | 0 | +1/16 |
| Erfolgswahrscheinlichkeit | 0,29905679 | 0,31289945 | 0,31068223 |
| Mittleres Zeigerintervall bei Erfolg | 0,39176134 | 0,39190287 | 0,39195026 |
| Skalare Verschiebung von $q_1$, affine Uhren | −1/4 | 0 | +1/4 |
| Erfolgswahrscheinlichkeit | 0,31310129 | 0,31289945 | 0,31310129 |
| Zeigermittelwert bei Erfolg | −0,20590658 | 0 | +0,20590658 |

Beim Skalarversuch tauschen die beiden äusseren Zeigerintervalle ihre Wahrscheinlichkeiten. Der Vergleich misst den Transport einer Präparation zum Detektor im bedingten Skalarmodell. [Skalarrechnung und vollständige Bilanz](controls/results.json)

## 3. Ein kohärentes Anfangspaket auslesen

Das normierte Dichtepaket ist auf $[r_0-1/32,r_0+1/32]$ konstant. Seine Mittelpunkte sind $1/8$ und $1/4$. Für die Uhr nehmen wir zwei disjunkte normierte Intervallpakete $L,R$ mit Zentren $t_0\pm1/16$ und Halbbreite $1/32$. Die Masse eines Dichtefensters ist $1/32$, jene eines einzelnen Uhrfensters $1/48$. Ein normierter Indikator ist der Indikator geteilt durch die Quadratwurzel seiner Masse. Solche $L^2$-Pakete genügen für das Integral der beschränkten Amplitude. Hier wird keine Ableitung des scharfen Fensterrands verwendet.

Der Hauptversuch benutzt $(L+R)/\sqrt{2}$ mit fester Phase, Form und Breite. Nur das Dichtezentrum wechselt. Die instrumentengleiche inkohärente Kontrolle verwendet die Mischung der beiden normierten Uhrpakete zu gleichen Teilen. Sie erhält die Kohärenz innerhalb jedes Intervalls und zwischen den beiden Kausalordnungen. Ein separater Versuch kehrt nur die relative Uhrphase um. Für jedes Dichtezentrum ist das Mittel der vollständigen Ausgangsverteilungen beider Vorzeichen gleich der Verteilung der Mischung.

| Präparation | Erfolg bei $1/8$ | Erfolg bei $1/4$ | Änderung |
|---|---:|---:|---:|
| Kohärent, gleiche Phase | 0,000386336819 | 0,000379656344 | −0,000006680475 |
| Zwischen Uhrpaketen dephasiert | 0,000196756509 | 0,000196497596 | −0,000000258913 |
| Kohärent, relative Phase $\pi$ | 0,000007176200 | 0,000013338848 | +0,000006162648 |
| Präparationsphase $+rB(t)/2$ kompensiert die Wirkungsphase | 0,000393021202 | 0,000393021202 | exakt 0 |

Beim Hauptversuch steigt der Fehlschlag von **0,999613663181** auf **0,999620343656**. Unter den akzeptierten Ereignissen sinkt der Anteil im mittleren Zeigerintervall von **0,391342736** auf **0,391139074**. Auch das komplexe Verhältnis der integrierten Historienamplituden ändert sich von $-0{,}707231+1{,}433504i$ auf $-0{,}706024+1{,}431246i$. Die kleine unbedingte Erfolgsrate enthält die Projektion des schmalen Eingangspakets auf die breite konstante Randmode.

Die Anfangsdichte verändert bei variablem $t$ die relative Phase verschiedener Uhranteile. Dieser Effekt erklärt, weshalb ein kohärenter Versuch überhaupt auf $r_0$ antworten kann. Eine eigens präparierte Gegenphase löscht ihn punktweise. Ein weiterer Vergleich mittelt scharfe Uhr- und Dichteeinstellungen als klassische Präparationen **ohne** kohärente Randprojektion. Er ist exakt dichteunabhängig und hat bei beiden Zentren Erfolg 0,304277196. Sein absoluter Erfolg bezieht sich auf dieses andere Präparationsprotokoll. [Alle drei Zeigerintervalle, Fehlschläge und Kontrollen](clock_packet_results.json)

## Reproduktion und Reichweite

Der [Skalarkontrollstand vom 13. November](controls/contract.json) samt Originalrechnung und Ergebnisprotokoll wurde wiedergefunden und bytegleich nachgerechnet. Der [Paketvertrag](packet_contract.json), die [Uhrintegration](clock_packets.py) und die gemeinsame Auswertung wurden am 18. November ergänzt. Drei innere Uhren werden jeweils mit normierter Gauss-Legendre-Quadratur integriert. Die drei inneren Dichteintegrale enthalten alle acht Atom-/Positivsektoren analytisch. Die Gravitation geht je Historie einmal ein. Das kollektive äussere Dichteintegral über das positive Fenster ergibt einen sinc-Faktor und wird zusätzlich durch direkte Quadratur geprüft.

Im Paketlauf werden 64 und 96 Knoten je innerer Uhr sowie 8 und 12 Knoten je äusserem Uhrintervall verglichen. Die maximale absolute Gitterdifferenz der ausgegebenen Werte liegt unter $4\times10^{-15}$. Die affine Referenz wird zudem gegen die veröffentlichte 160-Knoten-Rechnung geprüft. Diese Gittervergleiche sind empirisch. Ein vollständiges Rundungsfehlerzertifikat liegt offen.

Aus dem Repository-Stamm oder dem entpackten Prüfpaket mit Python 3.12:

```bash
dust=research/rax_cqg/dust_collapse
python -m pip install -r "$dust/physical_boundary_readout_v0_1/requirements.txt"
python -B "$dust/initial_preparation_v0_1/verify.py"
```

**Wissenschaftlicher Status.** Nachgewiesen ist eine präparationsabhängige Antwort des festen Zukunftsdetektors in diesem endlichen Randmodell. Der Vergleich lässt eine dynamische Auswahl der Geometrie, gravitative Rückwirkung und eine Bounce-Aussage offen.
