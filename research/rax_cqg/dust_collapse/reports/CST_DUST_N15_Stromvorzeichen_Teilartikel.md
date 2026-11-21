# Welche Information über das Stromvorzeichen bleibt nach der skalaren Randreduktion erhalten?

**CST-DUST · Teilartikel · Überarbeitete Fassung vom 21. November 2026**

## Zusammenfassung

Auf einer festen Kausalordnung mit 15 Ereignissen konstruieren wir zwei Pakete von Feinhistorien mit entgegengesetzter Stromladung. Beide liefern denselben von null verschiedenen skalaren Randzustand. Diese Gleichheit bleibt erhalten, wenn am Zukunftsrand drei Uhren und vier Dichten zusätzlich ausgelesen werden. Im Ensemble aus 453 Ordnungstypen sind die beiden vorzeichenselektierten Randzustände hingegen verschieden und überlappen. Die skalare Auslese kann dort einen Teil der Vorzeicheninformation tragen. Wie häufig ein positives Vorzeichen registriert wird, hängt von der Messregel und von den Gewichten der Historien ab.

## 1. Ladung und skalare Auslese

Die Feinhistorie umfasst eine endliche Kausalordnung, Staubuhren, Dichten und ein Skalarfeld. Die Stromladung $p=-\partial_\tau S_d$ ist die Antwort der Staubwirkung auf eine gemeinsame Verschiebung $\tau$ der vier Anfangsuhren. Bei dieser Ableitung bleiben alle anderen Uhren und sämtliche Dichten fest. Die Markierung $M$ gibt die in der Präparation eingesetzte Modellmasse an. Die physikalische Eichung von $p$ in Einheiten der Ruhemasse ist offen. [Definition der Ladung und Schnittmasse][masse]

Nach der skalaren Reduktion bleibt von einem festen Ordnungstyp $c$ eine skalare Ausgangsfunktion $\phi_c\in H_3=L^2(\mathbb R^3)$ übrig. Werden die Feinhistorien vor der Reduktion nach dem Vorzeichen sortiert, haben die Zweige die Form

$$
\psi_{c,+}=a_{c,+}\phi_c,\qquad \psi_{c,-}=a_{c,-}\phi_c.
$$

Wo beide Amplituden von null verschieden sind, geben die normierten Zustände bis auf eine globale Phase denselben Vektor. Jede Messung am skalaren Ausgang allein hat dann für beide dieselbe bedingte Ergebnisverteilung. Ob sich die Sortierung nach dem Vorzeichen überhaupt als Operation am Rand ausführen lässt, prüfen wir im Folgenden an zwei expliziten Paketen. [Ensemble und Randabbildung][ensemble]

Eine ergänzende Kontrolle auf Typ 375841 hält fest, in welchem der beiden **anfänglichen** Uhrfenster die Präparation lag. Über das ganze rechte Fenster ist der Strom positiv. Im linken Fenster sind beide Vorzeichen möglich. Das Fenster liefert also für einen Teil der Präparation einen eindeutigen Hinweis. Als zusätzlich aufgezeichnete Eingangsgrösse beantwortet es eine andere Messfrage als das skalare Zukunftsfeld. [Kontrolle der Uhrfenster][rand]

<!-- Seitenumbruch -->

## 2. Einzeltyp 375841 · Zwei Vorzeichen, ein Randbild

Wir fixieren $M=1/4$, das Anfangsdichtezentrum $r=1/8$ und dieselben äusseren Daten für beide Pakete. In den dimensionslosen Uhren $Y=T/\Delta$, $\Delta^4=3/722$, lautet die Staubwirkung

$$
S_d=-\tfrac12\sum_v w_v C_v,\qquad
C_v=1+\tfrac1{19}\sum_{i\prec v} b_{iv}(Y_v-Y_i)^2.
$$

Der Intervallkoeffizient $b_{iv}$ ist für null bis drei Zwischenereignisse der Reihe nach $1,-9,16,-8$ und sonst null. Für den Uhrenoffset $e=\delta/\Delta$ und die inneren Dichten $x_v=w_v/[M\Delta(4-e)]$ ist $p/M$ bei festen Uhren linear in $x$. Jeder Beitrag einer inneren Dichte wird mit den Intervallkoeffizienten und der Uhrdifferenz zum Vergangenheitskragen gewichtet. Die Richtung, in der die Wirkung konstant bleibt, kann den Strom deshalb ändern.

**Konstruktion.** Um das präparierte Verweildichteprofil $f$ verschieben wir die drei Komponenten an den Ereignissen $5,12,13$ um den Vektor $d=\tfrac{7600}{8\,000\,000}(C_{12}-C_{13},C_{13}-C_5,C_5-C_{12})$. Alle anderen Komponenten von $d$ sind null. Damit gelten $\sum_v d_v=0$ und $\sum_v C_vd_v=0$ für alle beteiligten Uhrwerte. Im Zentrum bei $e=-1/4$ und den sieben normierten Uhren $(1,2,1,2,3,4,3)/5$ in der Ereignisreihenfolge $(4,5,6,11,12,13,14)$ ist $d=(268,537,-805)/10^6$ auf diesen drei Achsen. Die Stromladung ändert sich entlang dieser Richtung.

| Paketzentrum | $p/M$ im Zentrum, exakt | Rationale Schranken auf dem ganzen Paket |
|:---|:---|:---|
| $f-d$ | $1429581/190000000$ | $0{,}0074<p/M<0{,}0077$ |
| $f+d$ | $-1004581/190000000$ | $-0{,}0054<p/M<-0{,}0051$ |

Die beiden offenen Pakete haben in $e$, den sieben inneren Uhrkoordinaten und den sieben Dichteabweichungen jeweils Halbbreite $10^{-7}$. Sie liegen strikt im zulässigen Dichteband und haben positives Integrationsmass.

**Randbild und Beweis.** Die Zukunftsuhr $Y_7=2$ bleibt fest. Drei spätere Uhren und vier Dichten variieren in einer Box $Z$ mit Halbbreite $2^{-20}$ um $(3,4,5,1/8,1/8,1/8,1/8)$. Für jedes $z\in Z$ erhält die Translation zwischen den Paketen die Staubwirkung, weil $C\cdot d=0$. Ihr Jacobi-Faktor ist eins. Auch Gravitationsphase und skalare Ausgangsfunktion sind gleich. Die eingeschlossene Staubphase erfüllt $\operatorname{Re}(e^{iS_d})>0{,}69$ auf beiden Paketen. Ihre Integrale sind daher von null verschieden. Für die Paketindikatoren $\chi_+,\chi_-$ und die Randabbildung $F_Z$ folgt punktweise $F_Z\chi_+=F_Z\chi_-=v$.

Die Referenzpaarung integriert das $H_3$-Skalarprodukt mit dem normierten flachen Mass auf $Z$. Auf der Zweipaketspanne hat ihre Gram-Matrix vier gleiche Einträge $\gamma=\|v\|^2>0$. Die Differenz $n=\chi_+-\chi_-$ hat Randnorm null, ihr positiv selektierter Anteil $S_+n=\chi_+$ hat Normquadrat $\gamma$. Ein scharfer Selektor auf dem Randquotienten müsste jede Nullrichtung erhalten. Dieser Selektor verletzt die Bedingung. Der Beweis gilt für die angegebene Referenzpaarung. Ob die physikalischen Constraints beide Pakete im selben Zustandsraum zulassen, bleibt offen. [Vollständige Herleitung und Nachrechnung][rand]

<!-- Seitenumbruch -->

## 3. Ensemble · Wie viel Vorzeicheninformation bleibt?

Zwei Elternfamilien tragen 310 und 206 Endtypen, davon 63 gemeinsam. Auf den insgesamt 453 Endtypen können die skalaren Funktionen $\phi_c$ verschiedene Richtungen haben. Bei festen Gewichten $q_c$ entstehen die Vorzeichenzweige durch kohärente Summation, $\Psi_\pm=\sum_c q_c a_{c,\pm}\phi_c$. In den zwölf Basisfällen – drei Markermassen, zwei Dichtezentren und zwei lokale Gewichtsverhältnisse – beträgt ihr normierter Überlappbetrag

$$
0{,}01130\ \text{bis}\ 0{,}07696,\qquad
\mathcal O=\frac{|\langle\Psi_-,\Psi_+\rangle|}{\|\Psi_-\|\,\|\Psi_+\|}.
$$

Die Werte sind gerundet. Weil $0<\mathcal O<1$, können geeignete skalare Messungen die konditionierten Ensemblezustände statistisch unterscheiden. Eine fehlerfreie Zuordnung jedes Einzelfalls allein am skalaren Ausgang ist ausgeschlossen. Eine positive Umskalierung der Zweigvektoren lässt $\mathcal O$ unverändert. [Überlappdaten der zwölf Fälle][overlap]

**Verteilung bei vorgegebener Registrierung.** Die Tabelle zeigt Prozentanteile für $r=1/8$, das lokale Verhältnis $A:B=1:1$ und die primäre Kettenfortsetzung. In den ersten sechs Zeilen besitzt jedes Ladungsintervall einen eigenen orthogonalen Registerzustand. In der letzten Zeile werden die drei Amplituden *innerhalb* jedes Vorzeichens vor der Paarung kohärent addiert. Die Punktladung $p=0$ hat in der verwendeten positiven Präparation Hilfsmass null.

| Registrierter Ausgang | $M=1/4$ | $M=1$ | $M=4$ |
|:---|---:|---:|---:|
| $p<-1$ | < 0,01 | < 0,01 | 0,56 |
| $-1\le p<-1/4$ | < 0,01 | 1,14 | 0,06 |
| $-1/4\le p<0$ | 7,80 | 5,32 | 0,03 |
| $0<p<1/4$ | 90,62 | 5,75 | 0,15 |
| $1/4\le p<1$ | 1,58 | 86,16 | 3,45 |
| $p\ge1$ | < 0,01 | 1,63 | 95,76 |
| **Positiv, sechs Klassen zusammengefasst** | **92,20** | **93,55** | **99,35** |
| **Positiv, nur Vorzeichen registriert** | **92,23** | **92,27** | **99,24** |

Bei $M=1$ ergeben dieselben Eingangsdaten je nach Registrierung 93,55 % oder 92,27 % positive Ausgänge. Ein Register legt fest, welche Alternativen unterscheidbar bleiben und welche interferieren. Der in der Tabelle angenommene orthogonale Eintrag ist eine zusätzliche Messannahme. Der Einzeltyp-Beweis zeigt, weshalb sich ein solcher Eintrag am skalaren Rand eigens begründen muss. [Verteilungsdaten und Messregeln][verteilung]

<!-- Seitenumbruch -->

## 4. Empfindlichkeit gegenüber den Historiengewichten

Bei $M=1/4$ und $r=1/8$ wurden dieselben komplexen Feldamplituden zweimal neu gewichtet. Verglichen wird jeweils der positive Gesamtanteil im Sechsklassenregister.

| Änderung gegenüber der Basisreihe | Änderung in Prozentpunkten |
|:---|---:|
| Lokales Verhältnis $A:B$ von $1:1$ auf $1:3$, gleiche Kettenfortsetzung | $+0{,}02585$ |
| Andere Kettenfortsetzung bei festem $A:B=1:1$ und denselben 70 N13-Präfixgewichten | $+4{,}84159$ |

Beim zweiten Vergleich ändern sich 46 der 206 Endtypgewichte des Kettenzweigs. Der positive Anteil steigt von 92,20 % auf 97,05 %. Die Zahlen stammen aus den gemittelten Amplituden von vier Sobol-Wiederholungen mit je 4 096 Punkten. Beim zweiten Vergleich liegen die vier einzeln berechneten Verschiebungen zwischen 4,82694 und 4,85082 Prozentpunkten. Das beschreibt die beobachtete numerische Streuung. Die beiden Vergleiche erfassen nur die angegebenen Gewichtsänderungen innerhalb des grösseren Raums zulässiger Fortsetzungen. [Gepaarte Gewichtsvergleiche][gewicht]

## 5. Reichweite für den Staubkollaps

Die endliche Randrechnung beantwortet eine Frage über den Erhalt von Information. Für den frühen klassischen Radiustest P3 braucht es zusätzlich einen unabhängig geeichten Massenstandard und einen geometrischen Messwert. Dieselbe mitbewegte Stauboberfläche muss vom Anfangsschnitt bis zur Staubeigenzeit $T_*=5\sqrt5/6$ verfolgt werden. Aus ihrer **intrinsisch rekonstruierten Fläche** $A(T_*)$ folgt ihr Arealradius $R_A(T_*)=\sqrt{A(T_*)/(4\pi)}$. Der markierte Fluss allein liefert keine Flächenmetrik.

| Markierte Zielmasse | Klassischer Referenzradius bei $T_*$ | Physische CST-Radiuswerte |
|:---|---:|:---|
| $1/4$ | 9,578868 | Dichtestufen 1, 2, 4, 8 jeweils `NOT_RUN` |
| $4$ | 8,254818 | Dichtestufen 1, 2, 4, 8 jeweils `NOT_RUN` |

Die acht ausstehenden Werte sind zwei Massen auf je vier Dichtestufen beim selben frühen Zeitpunkt. Ein späterer Erfolg würde die **frühe klassische Korrespondenz** des Arealradius stützen. Die übrigen P3-Observablen hätten ihre eigenen Kriterien zu erfüllen. Für eine reguläre Re-Expansion verlangt der eigene Prüfvertrag den Nachweis, dass dieselbe Staubregion bei eingefrorener Dynamik durch das Hochdichteregime fortgesetzt wird, unter kontrollierter Verfeinerung regulär bleibt und nach der Kontraktion wieder expandiert. Die physikalische Endklassifikation steht auf `HOLD`. [Früher Radiustest][radius] · [Materielle Oberfläche][oberflaeche] · [Regularität und Fortsetzung][reg] · [Endklassifikation E3][ende]

**Ergebnis.** Für zwei explizite Pakete löscht die Randreduktion die Vorzeichenunterscheidung vollständig. Über mehrere Ordnungstypen bleibt im skalaren Zustand eine statistisch auslesbare Unterscheidung erhalten. Die Häufigkeiten eines registrierten Vorzeichens gelten jeweils für die angegebene Präparation, Messregel und Gewichtung.

[masse]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/cut_mass_charge_vacuum_v0_1/README.md
[ensemble]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/joint_charge_distribution_v0_1/README.md
[rand]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_future_boundary_v0_1/Teilartikel.md
[overlap]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_charge_interval_record_v0_1/ueberlapp.csv
[verteilung]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/joint_charge_distribution_v0_1/distribution.csv
[gewicht]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/n15_sign_record_audit_v0_1/README.md
[radius]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/early_areal_radius_two_masses_v0_1/README.md
[oberflaeche]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/material_current_surface_v0_1/README.md
[reg]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/stage_reviews_8_9/README.md
[ende]: https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/397f867ba5318127cd9f7fbefbb0b388c8cdae05/research/rax_cqg/dust_collapse/stage_review_10/README.md
