# Kann ein Quellzeiger das Staubstromvorzeichen über einen Zwischenschnitt tragen?

**CST-DUST · Typ 375841 · 21. November 2026 · Endlicher Modellversuch**

Zwei Feinhistorienpakete mit gegenläufigem Staubstrom ergeben im publizierten skalaren Randtest denselben Zustand. In dieser Erweiterung durchläuft derselbe Zweiniveau-Zeiger beide Pakete. Er koppelt vor der Randreduktion an die aus der Wirkung abgeleitete Ladung. Für die festgelegte Hilfspaarung überträgt er einen kleinen Teil der Vorzeicheninformation bis zum Zukunftsrand. Der direkte und der über eine innere Antikette verklebte Rechenweg liefern exakt dieselbe Dekohärenzmatrix einschliesslich der Kreuzterme. Die Zulässigkeit des Zeigers und die physikalische Paarung des gekoppelten Systems bleiben offen.

| Bedingte Wahrscheinlichkeit für denselben Ausgang $Y=+1$ | Positives Paket | Negatives Paket |
|---|---:|---:|
| Quelle aus, exakt | $1/2$ | $1/2$ |
| Quelle ein, bewiesene Schranke | $>0{,}5008325$ | $<0{,}49942625$ |
| Quelle ein, numerisch | 0,500940513261 | 0,499339091640 |

Die bewiesene Lücke übersteigt $9/6400=0{,}00140625$, also **0,140625 Prozentpunkte**. Der numerische Abstand beträgt 0,160142 Prozentpunkte. Die Zahlen sind normierte Antworten je Testpaket. Die Häufigkeiten der Pakete im physikalischen Ensemble und ihre getrennte experimentelle Präparierbarkeit sind offen.

## 1. Quelle und Instrument

Für dieselbe Feinhistorie $h$ und dieselben offenen Zukunftsdaten $z$ sei $S_h(\tau)$ die Wirkung bei gemeinsamer Verschiebung der vier Anfangsuhren um $\tau$. Bei dieser Quellenableitung bleiben innere Felder, Gewichte, Paketfenster und das Integrationsmass fest. Die quadratische Wirkung liefert exakt

$$
p(h)=-S'_h(0)
=\frac{S_h(-s/2)-S_h(s/2)}{s}
=\frac{1}{19\Delta}\sum_{i\in P,\,v\notin P} w_v b_{iv}(Y_i-Y_v),
\qquad \Delta^4=3/722.
$$

Auf diesem Typ verschwinden die direkten Anfangs-Zukunfts-Koeffizienten. Die Quelle liest daher die früheren Felder. Dieselbe Vorschrift wird vor der Summation auf jede Historie angewandt. Das Rechenmodell ergänzt einen Zeiger in $\mathbb C^2$ im Zustand $(1,1)/\sqrt{2}$, mit kontrollierter Phase $U_\lambda(h)=\mathrm{diag}(1,e^{i\lambda p(h)})$. Die erste Komponente dient als kohärente Referenz. Gewählt wurden $\lambda=1$ in den zur Modellladung konjugierten Einheiten, $\lambda=0$ für die Kontrolle und derselbe Pauli-$Y$-Effekt für beide Pakete. Eine Quelle am bereits reduzierten Ausgang hätte für beide Pakete identische Eingaben. Die beiden Zeigerkomponenten bezeichnen Referenz und Quelle. In keiner Komponente wird das Vorzeichen als Etikett eingesetzt.

Die gekoppelten Amplituden auf jedem Paket $P_s$ sind nach Ausklammern der gemeinsamen Gravitationsphase und des normierten Skalarzustands

$$
a_s(z)=\int_{P_s}e^{iS_d(h,z)}d\mu(h),\qquad
b_s(z)=\int_{P_s}e^{iS_d(h,z)+i\lambda p(h)}d\mu(h).
$$

Die sieben offenen Zukunftskoordinaten, die Eingangsdichte im Band $[3/32,5/32]$, das gemeinsame linke Uhrfenster mit der ursprünglichen engen Zelle um $e=-1/4$, die beiden ganzen verschobenen Dichtezellen, das gemeinsame Hilfsmass und das Einzeltypgewicht stammen aus dem bisherigen Versuch. Die Enduhr $Y_7=2$, die markierte Masse $1/4$ und das Zentrum der Anfangsdichte $1/8$ bleiben in beiden Wegen gleich. Das Produkt auf $H_3\otimes L^2(Z,d\nu)\otimes\mathbb C^2$ verwendet die normierte flache Zukunftsbox und die übliche Zeigerpaarung. Dieses zusätzliche Instrument und seine Paarung sind Modellentscheidungen. Die Wirkung bestimmt die Ladungsfunktion $p$. [Quellenableitung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e707dd3450808b611aa884f484619a3907d3fc06/research/rax_cqg/dust_collapse/boundary_mass_sector_v0_1/README.md) · [Vorzeichenpakete und Quellantwort](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e707dd3450808b611aa884f484619a3907d3fc06/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/Teilartikel.md)

## 2. Der Zwischenschnitt und die volle Matrix

Der Uhrwert $Y=0$ trennt auf der gesamten Paketspanne dasselbe Ordnungsideal ab. Seine maximalen Ereignisse bilden die Antikette $\{5,11\}$. Ihre individuellen Uhrwerte dürfen innerhalb der Paketfenster variieren. Die beiden inneren Ketten lauten $4\prec5\prec14$ und $6\prec11\prec12\prec13$.

Der Direktweg zählt die offenen Intervalle der Gesamtordnung. Der verklebte Weg erhält die beiden lokalen Ordnungen, identifiziert ihre Antikette und rekonstruiert jede Kreuzrelation aus den erreichbaren Schnittpunkten. Für jedes Kreuzpaar zählt er die Zwischenereignisse links, auf dem Schnitt und rechts. Unter den 39 Kreuzrelationen haben elf einen von null verschiedenen Wirkungskoeffizienten. Fünf davon tragen zur Quelle bei. Aus beiden Teilwirkungen, der einmal abgezogenen Schnittwirkung und diesen Kreuztermen folgen für alle Feldwerte dieselben Staubkoeffizienten, dieselbe skalare Hesse-Matrix und derselbe Gravitationswert $F_4=7$. Die benötigten früheren Uhr- und Skalarwerte sowie die gemeinsame Paketpräparation bleiben bis zum Einsetzen der Kreuzwirkung erhalten. Die gemeinsam verschobenen Dichtefenster dürfen dabei nicht auf beiden Seiten unabhängig gewichtet werden. [Bedingte Verklebung und Schnittdaten](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e707dd3450808b611aa884f484619a3907d3fc06/research/rax_cqg/dust_collapse/extended_sewing_v0_1/DERIVATION.tex)

Damit sind die beiden Zeigerarme vor der Integration punktweise gleich auf den beiden *Rechenwegen*. Sämtliche Massfaktoren werden einmal angesetzt. Im Staubsektor gilt Fubini auf den kompakten Integrationsboxen. Der gemeinsame Skalarfaktor wird durch die etablierte Einzeltyp-Randreduktion ausgewertet. Seine identische quadratische Form auf beiden Wegen ist exakt geprüft. Dies ergibt für jeden Eintrag $i,j\in\{+,-\}$

$$
D_{ij}=\tfrac12\int_Z(\overline a_i a_j+\overline b_i b_j)\,d\nu,
\qquad
D^{Y+}_{ij}=\tfrac14\int_Z\overline{(a_i-i b_i)}(a_j-i b_j)\,d\nu,
\qquad D=D^{Y+}+D^{Y-}.
$$

$D^{Y-}$ verwendet $a+i b$. Bei $\lambda=0$ sind alle vier Einträge von $D$ gleich demselben positiven Wert. Im gekoppelten Lauf beträgt beispielsweise $D_{+-}\simeq0{,}9958348418-0{,}0015947536i$ in der gemeinsamen Referenznormierung. Alle drei komplexen Matrizen auf beiden Wegen stehen in [quadratur.json](quadratur.json). Diese bedingte Verklebung prüft eine Schnittlage und einen Ordnungstyp. Ein reduzierter physikalischer Transportoperator allein auf der Antikette wäre ein weiterer Befund.

## 3. Analytischer Nachweis für ganze Pakete

Für festes $z$ und ein Paket schreibe $a,b$ für seine beiden Arme und $m=\int_{P_s}d\mu>0$. Bei eingeschalteter Quelle gilt mit $u=S_d(h',z)-S_d(h,z)$

$$
\operatorname{Im}(\bar a b)=
\iint d\mu(h)d\mu(h')\int_0^{p(h')}\cos(u+t)\,dt .
$$

Der bei $p=0$ abgezogene Sinusterm integriert sich wegen Antisymmetrie zu null. Die rationale Rechnung schliesst die Staubphase beider Pakete und der ganzen Zukunftsbox in ein Intervall der Breite $<0{,}43$ rad ein. Ferner gilt $p_+>74/40000$, $p_-<-51/40000$ und $|p|<1/500$. Damit ist $\cos(u+t)>9/10$, wie bereits $1-(0{,}43+0{,}002)^2/2>0{,}9$ zeigt. Der Imaginärteil hat auf jedem ganzen Paket das jeweilige Vorzeichen. Der gemeinsame Randzustand bleibt im Referenzarm von null verschieden.

Für den festen Ausgang $Y=+1$ ergibt sich

$$
P_s=\frac{D^{Y+}_{ss}}{D_{ss}}
=\frac12+\frac{\int_Z\operatorname{Im}(\bar a_s b_s)d\nu}
{\int_Z(|a_s|^2+|b_s|^2)d\nu}.
$$

Der Nenner ist höchstens $2\int_Z m^2d\nu$. Dies liefert die strikten Schranken in der ersten Tabelle. Der Beweis gilt ebenso bei gemeinsamer positiver Umgewichtung der Zukunftsbox mit endlichem, von null verschiedenem Gewicht. Die Standardpaarung zwischen den beiden Zeigerarmen bleibt dabei vorausgesetzt.

Die unterschiedlichen Wahrscheinlichkeiten erzwingen linear unabhängige Paketbilder für den erweiterten Rand. Zugleich ist der Realteil von $D_{+-}$ strikt positiv. Im Referenzarm liegen beide Phasen im selben Kegel, im Quellenarm wächst die mögliche Phasendifferenz höchstens um $2\max|p|$. Auch dann ist der Kosinus grösser als $9/10$. Die beiden Zustände sind daher nicht orthogonal. Der Zeiger liefert **teilweise Unterscheidbarkeit**. Ein scharfer selbstadjungierter Vorzeichenprojektor mit diesen Bildern als gegensätzlichen Eigenzuständen ist für diese Paarung ausgeschlossen.

## 4. Physikalische Entscheidung

Im alten skalaren Randquotienten gilt $n=\chi_+-\chi_-\sim0$. Der erweiterte Zeiger gibt $n$ positive Hilfsnorm. Folglich kann diese Kopplung auf der geprüften Spanne **nicht** als Operation allein auf dem alten Quotienten realisiert werden. Dieser Ausschluss gilt unabhängig von der numerischen Genauigkeit.

Für einen physischen Record fehlen ein aus der gekoppelten Dynamik begründeter Zeigertransport und eine aus den Constraints hergeleitete positive Paarung. Ein solcher Transport muss die physikalischen Nullrichtungen respektieren und direkt wie über den Zwischenschnitt dieselben Auslesewahrscheinlichkeiten liefern. Die Bedingung am alten Quotienten ist entschieden, die entsprechende Frage für einen physikalisch erweiterten Rand bleibt **HOLD**. Der Versuch ergibt keine Masseneichung. Die acht physischen frühen P3-Radiuswerte bleiben auf **NOT_RUN**. [Physikalische Zwischenrandpaarung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e707dd3450808b611aa884f484619a3907d3fc06/research/rax_cqg/dust_collapse/seam_pairing_v0_1/README.md) · [Stand des Teilartikels und der Masseneichung](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/339)

## 5. Nachrechnung

Aus dem entpackten Studienordner ausführen. Der rationale Nachweis braucht nur die Python-Standardbibliothek. Die numerischen Gegenrechnungen verwenden NumPy und SciPy. Referenzumgebung war Python 3.12.14, NumPy 2.3.5 und SciPy 1.17.0.

```sh
sha256sum -c SHA256SUMS
python3 -B nachweis.py
OPENBLAS_NUM_THREADS=1 python3 -B gegenrechnung.py
OPENBLAS_NUM_THREADS=1 python3 -B doppelintegral.py
```

Der Direktweg der numerischen Rechnung variiert die Originalwirkung symmetrisch. Der verklebte Weg verwendet rekonstruierte lokale und kreuzende Kanten sowie die analytische Quellenableitung. Die gemeinsame Dichte am Anfangsrand und die sieben freien Dichteverschiebungen werden analytisch über ihre vollen Intervalle integriert. Für die acht verbleibenden früheren und sieben äusseren Variablen werden zwei unabhängige Sobol-Verwürfelungen auf drei Stufen verwendet. Der gemeinsame Volumenfaktor entspricht den Fensterbreiten und der Zeitdauer im Zentrum. Der verbleibende Jacobi-Faktor $(D_T/D_{T,0})^{14}$ wird in jeder Amplitude integriert. Die direkten und verklebten Matrizen differieren in diesen Einheiten um höchstens $1{,}4\cdot10^{-15}$. Diese Abweichung misst den Vergleich der beiden Rechenwege. Die garantierte Trennung der Antworten stammt aus dem analytischen Beweis.

Lässt die Gegenprobe bei festgehaltener Präparation die Kreuzwirkung weg, verschiebt sich mindestens ein Matrixeintrag um rund 0,02754. Eine ergänzende Kontrolle nach der ersten Auswertung berechnet das 39-dimensionale Doppelintegral mit getrennten Bra- und Ket-Variablen am gemeinsamen Zukunftswert und direkt gezogenen Dichten. Bei zweimal 65 536 Punkten weichen ihre Matrizen um weniger als $8\cdot10^{-14}$ von der Rechnung mit analytischer Dichteintegration ab. Diese Dezimalwerte sind empirische Kontrollen.

[Prüfvertrag](pruefvertrag.json) und [Vertragshash](pruefvertrag.sha256) wurden vor dem neuen Lauf lokal festgehalten. Die bereits publizierte Lage der Pakete und der Unterschied der Quellsteigungen waren bekannt. Es gab keine öffentliche Blindregistrierung. [Rationales Zertifikat](nachweis.json) · [Direkte Doppelintegrale](doppelintegral.json)

Die übernommene Datei [density_translation_375841.py](quellen/density_translation_375841.py) ist bytegleich mit dem Repository-Blob `3942b4b53841741ee64145b529433d7da2149315` im [festen Quellenstand](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/e707dd3450808b611aa884f484619a3907d3fc06/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/density_translation_375841.py). Die Prüfprogramme und Texte stehen unter [Apache-2.0](LICENSE). [NOTICE](NOTICE)
