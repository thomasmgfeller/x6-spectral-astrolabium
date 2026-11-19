# Relationaler Transport am N11-Paar

**CST-DUST · Etappe 6 · 19. November 2026 · v0.1**

Beim selben Eingangs-Uhrpaket und am selben geometrischen Detektor wurde der direkte Übergang über die beiden Randkragen mit einem Übergang über einen inneren Schnitt verglichen. Der Schnitt liegt einmal bei $s=0$, einmal bei $s=1/4$. Mit gespeicherten Angaben zu den drei inneren Uhren gelingt die Verklebung an beiden Stellen. Die Forderung, dass die Ereignisse mit $T\leq s$ selbst eine kausale Vergangenheit bilden, verändert eine gemessene Endwahrscheinlichkeit. **Die physikalische Etappe 6 bleibt auf HOLD.**

## Was am Detektor ankommt

Gemessen wird die unbedingte Wahrscheinlichkeit, dass die geometrische Auslese die Ordnung mit **einem** vergleichbaren inneren Paar eindeutig erkennt. Das gleichphasige geteilte Uhrpaket, der Detektor für einen unbekannten Puls und die Referenzeinstellung $t_1=0,\ t_2=1$ stammen aus der veröffentlichten N11-Rechnung. Das Instrument kennt die Stärke $t_2$ bei der Auslese nicht. Die folgende Tabelle zeigt die gekoppelte Rechnung in Prozent aller Versuche.

| Anfangsuhr | Direkt | Nur kausale Rohschnitte bei 0 | Nur kausale Rohschnitte bei 1/4 |
|:---|---:|---:|---:|
| Fester Zentralwert | 11,31599 % | 6,60962 % | 6,72979 % |
| Schmales Paket | 11,29112 % | 6,59220 % | 6,71193 % |
| Geteiltes Paket | 11,00179 % | 6,38973 % | 6,50441 % |

Bei Speicherung der Schnittdaten ergeben beide Zwischenschnitte in jeder Zeile den Direktwert. Geprüft wurden die beiden Diagonalen und die **komplexe** Nebendiagonale der Zweigkoeffizienten-Grammatrix sowie alle drei Endausgänge. Die grösste numerische Abweichung beträgt $2{,}23\times10^{-16}$ oder weniger bei einer vorgegebenen absoluten Toleranz von $5\times10^{-9}$. Das gilt auch für den Kontrollarm mit gemeinsamem C0-Staubtransfer. Die Identität der vollständigen Verklebung und die unten hergeleitete Untergrenze beruhen zusätzlich auf analytischen Argumenten.

## Übergang und Reichweite

Die Anfangsuhr $T_3$ ist um $-2\Delta$ präpariert, die feste erste Zukunftsuhr ist $T_7=2\Delta$, mit $\Delta^4=3/722$. Alle anderen äusseren Uhren und die Zukunftsdichte folgen der Referenz. Das markierte Innere besteht aus den Ereignissen 4, 5 und 6. Seine Uhren sind im Referenzmass unabhängig und gleichverteilt auf $[-3/2,3/2]$. Die inneren Dichten tragen jeweils zur Hälfte ein Nullatom und eine Gleichverteilung auf $[0,1]$. Beide Anfangsdichtezentren $1/8$ und $1/4$ liefern identische inklusive Paarungen, da die gemeinsame Anfangsphase bei gleichem $(r,t)$ aus jedem Produkt verschwindet.

Die Rechnung untersucht diesen festen Kragenübergang. Auf der Schnittfläche werden zunächst Hilfsdaten der Geschichte mitgeführt. Eine positive physikalische Norm für den gemeinsamen Geometrie-, Staub- und Skalarsektor muss aus Wirkung und Constraints begründet werden.

## Wie der vollständige Übergang verklebt

Jeder inneren Uhr wird ein Bit zugeordnet, das angibt, ob $T_j\leq s$ gilt. Die acht möglichen Bitmuster $m$ zerlegen den vollständigen Integrationsbereich. Sei $D_m$ die grösste kausal abgeschlossene Teilmenge der markierten Ereignisse unterhalb der Schwelle. Ein Ereignis gehört genau dann zu $D_m$, wenn es selbst und alle seine inneren Vorgänger unterhalb der Schwelle liegen. Der Vergangenheitskragen kommt vollständig hinzu. Wird der Schnitt nach vorne verschoben, können so zurückgehaltene Ereignisse hinzukommen. Der geometrische Schnitt folgt in jeder Ordnung derselben Regel.

Bei vorgegebenem $m$ ist der Integrationsbereich ein Produkt von Intervallen. Schreibe $q_m$ für sein normiertes Volumen, $x$ für die inneren Uhrkoordinaten auf der linken Seite und $y$ für die übrigen. Die bedingten Produktmasse auf den beiden Seiten seien $\nu_L$ und $\nu_R$. Die volle Wirkung bestimmt die Kantenkoeffizienten $c_{ij}$ auch am Schnitt. Für einen Zielknoten $j$ kann der grenzüberschreitende quadratische Ausdruck durch die drei Summen $a_j=\sum c_{ij}$, $b_j=\sum c_{ij}T_i$ und $d_j=\sum c_{ij}T_i^2$ ausgewertet werden. Er beträgt $a_jT_j^2-2b_jT_j+d_j$. Eine Dichtemarke wird erst nach Zusammenführung aller Terme ihres Zielknotens integriert.

Der linke Faktor $L_m(x)$ enthält die bereits vollständig bestimmten inneren Markenmittel. Der rechte Faktor $R_m(x,y)$ enthält die übrigen Markenmittel, die Zukunftsphase und die übergreifenden Kopplungen. Beide Faktoren haben Betrag höchstens eins. Beim Kontrollarm kann ein übernommener C0-Staubterm in einen geometrisch linken C1-Knoten zeigen. Dieser Term mitsamt seinem Markenmittel verbleibt bis zur Zusammenführung im rechten Faktor. Die Geometrie des Schnitts bleibt dieselbe.

Für feste äussere Daten und je Zweig ist die folgende Schnittnorm positiv. Bei Bedarf trägt jeder Summand zusätzlich den bedingten skalaren Hilbertraum $H_3$.

$$
\mathcal H_s=\bigoplus_m L^2(\nu_L),\qquad
\|f\|_s^2=\sum_m\int |f_m(x)|^2\,d\nu_L(x).
$$

Die erste Teilkarte überträgt $z$ auf $f_m(x)=\sqrt{q_m}L_m(x)z$. Die zweite bildet $f$ auf
$$
\sum_m\sqrt{q_m}\int d\nu_L(x)\, f_m(x)
                   \int d\nu_R(y)\,R_m(x,y)
$$
ab. Beide Karten sind Kontraktionen nach Cauchy–Schwarz und $\sum_m q_m=1$. Ihre Zusammensetzung ist nach Zerlegung des Integrals und Fubini exakt die direkte Staubamplitude. Die feste Gravitationsphase, die Zweiggewichte $1/2$, der skalare Endoperator $V_c$ und die äusseren Paketfaktoren werden wie im direkten Übergang angewendet. Damit stimmt auch jede aus denselben Endzuständen und Effekten gebildete Paarung überein. Die Zweige und Felder werden an der Zwischenfläche kohärent summiert. Eine Zwischenmessung mit verworfenem Ergebnis wäre ein anderer Versuch.

Die Faktorisierung gilt für das kontinuierliche kompakte Staubintegral. Sie benutzt die bereits reduzierten skalaren Randkarten. Einen eigenen skalaren oder gravitativen Zeitentwickler für jedes Teilgebiet leitet sie nicht her. Insbesondere ist das vollständige Bitmuster eine Information über die Geschichte, deren lokale Verfügbarkeit ein physikalischer Schnitt erst begründen müsste.

## Warum der rohe Uhrwert als kausaler Schnitt scheitert

Für $p=(s+3/2)/3$ ist $p$ der Anteil jeder inneren Uhrenachse vor dem Schnitt. In der Kette C0 ist eine Rohmaske nur als Anfangsstück von $4\prec5\prec6$ zulässig. Im Zweig C1 gilt innen allein $4\prec6$. Daraus folgen die **Massanteile der nicht kausal abgeschlossenen Rohmasken**. Es handelt sich um Anteile des Integrationsmasses vor der komplexen Summation.

| Ordnung | Ausgelassener Massanteil | Bei 0 | Bei 1/4 |
|:---|:---:|:---:|:---:|
| C0, drei Paare | $2p(1-p)$ | $1/2$ | $35/72$ |
| C1, ein Paar | $p(1-p)$ | $1/4$ | $35/144$ |

Ein positiver Massverlust allein entscheidet noch nicht über die Endauslese. Für C1 lässt sich sein beobachtbarer Effekt mit einer Momentenschranke beweisen. Sei $\Phi=\frac12\sum_{j=4}^{10}\rho_j C_j$ die reelle Staubphase ohne gemeinsame Anfangsphase. Dabei ist $C_j=1+(\beta/2)\sum_{i\prec j} c_{ij}(T_j-T_i)^2$ und $\beta=4/\sqrt6$. Die exakten Polynom-Momente geben für alle drei Eingangsuhren $\mathrm{Var}(\Phi)<1/5$. Für das geteilte Paket ergibt sich beispielsweise

$$
\mathrm{Var}(\Phi)=\frac{91655}{147456}\Delta^2+
                     \frac{36047006333}{327055048704}.
$$

Mit $\cos x\geq 1-x^2/2$ ist $|\mathbb E e^{-i\Phi}|>9/10$. Der inklusive direkte Zweigwert $\mathbb E_t |\mathbb E(e^{-i\Phi}\mid t)|^2/4$ ist daher grösser als $81/400$. Für den abgeschnittenen Zweig mit verbleibendem Mass $v$ ergibt die Dreiecksungleichung höchstens $v^2/4$. Das sind $9/64$ bei $s=0$ und $11881/82944$ bei $s=1/4$. Der eindeutige Ein-Paar-Ausgang hat denselben skalaren Effizienzfaktor auf beiden Wegen, im Einpulsvertrag oberhalb von $0{,}4956269034$. Die unbedingte Trefferwahrscheinlichkeit liegt damit beim Direktweg an **beiden Schnitten um mehr als 2,9 Prozentpunkte** höher. Der Ausschluss gilt ohne Quadraturannahme und für den unveränderten, nicht nachnormierten Rohschnitt.

## Was der Befund entscheidet

**Mathematisch** existiert in der bedingten N11-Paarung eine positive Schnittdarstellung mit übereinstimmenden Endpaarungen. **Physikalisch** ist die Zulassung weiter offen. Wer eine relationale Entwicklung allein mit kausalen Vergangenheiten aufbauen will, muss aus der vollständigen Wirkung begründen, welche Information an der Zwischenfläche gespeichert wird oder wie ein Einflussfunktional die ausgelassenen Zeitzuweisungen repräsentiert. Eine Änderung des Uhrmasses oder eine Renormierung nach dem Schnitt wäre ein neuer Modellvertrag. Die vorliegende Rechnung deckt den bestehenden N11-Sektor ab. Der 4D-Pilot P3 bleibt gesperrt.

**Quellen und Nachrechnung.** Grundlage ist der [Repository-Stand f319a64](https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/f319a644633fcb2eeb717db178477c54171d7667) mit [Präparation](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/294) und [geometrischer Auslese](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/321). Im Prüfpaket stehen der eingefrorene Vergleichsvertrag, exakte Momente, alle Endpaarungen und die unabhängige Rechteck- und Momentkontrolle. Die Ausführung ist in REPLAY.md beschrieben.
