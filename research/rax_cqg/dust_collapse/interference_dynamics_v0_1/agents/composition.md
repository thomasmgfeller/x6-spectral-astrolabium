# TASK 3: Exakte N11-Komposition mit vollständiger Vergangenheit

13. November 2026. Grundlage ist der gemeinsame Vertrag `contracts/interference_contract.json`, ausgehend vom Commit `da48df345a20b3922b5764ad795e3bf2444d9bb4`. Diese Fachprüfung enthält keine neue Quadratur.

**Ergebnis:** Die unveränderte gemeinsame Gravitation-, Staub- und Skalarwirkung lässt sich für beide N11-Ordnungen exakt über zwei verschiedene Schnitte zusammensetzen. Dafür müssen die bedingte Vergangenheit und sämtliche schnittübergreifenden Wechselwirkungen erhalten bleiben. Ein vollständiger Speichervertrag und explizite Kopierkerne liefern bei jedem gemeinsamen positiven Abel-Regulator eine assoziative Komposition der Randpaarung. Ein Produkt bereits auf die nackten Schnittfelder reduzierter lokaler Kerne liefert diese Identität nicht.

Es handelt sich um eine genau definierte bedingte Amplitudendynamik. Physikalische Historiengewichte, Paarung, kalibrierte Uhr und normierte geometrische Wahrscheinlichkeiten sind damit nicht hergeleitet. Die natürlich geordnete Bearbeitungsreihenfolge wird insbesondere nicht als physische Zeit ausgegeben.

## 1. Geometrie, Felder und eingefrorene Maße

`C0` ist die Kette auf `0..10`. `C1` entfernt genau `(4,5)` und `(5,6)` und behält alle übrigen Relationen einschließlich `(4,6)`. Die Innenmenge ist `I={4,5,6}`, der gemeinsame Rand `B={0,1,2,3,7,8,9,10}`. Beide Relationen sind transitiv abgeschlossen und besitzen dieselbe Randrestriktion.

Die ursprüngliche Wirkung lautet

\[
S_C=\kappa\left(N-\sum_{y\prec x}b_{yx}\right)
-\frac12\sum_xr_x
-\frac\beta4\sum_{y\prec x}b_{yx}
\left[r_x(T_x-T_y)^2+(q_x-q_y)^2\right],
\]

mit `beta=4/sqrt(6)`, `kappa=1` und `b=(1,-9,16,-8,0,...)`, bestimmt durch die offene Intervallgröße. Die Gravitationswerte sind `F4(C0)=10` und `F4(C1)=18`.

Der gemeinsame Folge-Vertrag legt die inneren Uhrmaße `dT_j/3` auf `[-3/2,3/2]`, das ursprüngliche Dichtemischmaß `(delta0+1_(0,1)dr)/2`, feste Randuhren und Randdichten sowie die gemeinsame Skalar-Gaußpaarung fest. Alle acht inneren Dichtestrata werden behalten. Es wird kein zusätzlicher Indikator einer gerichteten Uhrreihenfolge eingefügt. Dies ist eine ausdrücklich gewählte endliche Vervollständigung, keine Ableitung des physischen Maßes.

Jede innere Variable wird genau einmal integriert. Die Rand-Gaußfunktion

\[
\Phi_B(q_B)=\pi^{-2}\exp\left(-\frac12\sum_{b\in B}q_b^2\right)
\]

und der gemeinsame Regulator `exp(−epsilon sum_I q_j²/2)` werden jeweils einmal eingefügt. Der frühere Faktor zwei des AA-Zweipunktschnitts gehört nicht zu diesem Vertrag. Historiengewichte `omega_C` werden einmal als deklarierte Faktoren eingesetzt; ihre physische Auswahl und eine Produktzerlegung in Wachstumsgewichte sind nicht bewiesen.

## 2. Genügender Speicher und gerichteter Wirkungsschritt

Der maschinenlesbare Vertrag steht in `checks/composition/memory_contract.json`. Nach jedem Schritt bleiben erhalten:

1. die vollständige transitive Relation des vorhandenen kausalen Präfixes;
2. sämtliche bisherigen Uhr-, Dichte- und Skalarvariablen;
3. die gemeinsame bedingte Amplitude und ihre Korrelationen;
4. Rand-/Innenrollen, Maß- und Regulatorzuordnung sowie Historienidentität.

Dies ist ein bewusst ungekürzter, hinreichender Rechenspeicher. Es wird kein sparsamer Minimalzustand behauptet. Die gespeicherte Historienidentität ist Buchhaltung, kein zusätzliches orthogonales Detektorflag. Sie darf am Ende kohärent summiert werden, wenn dies der erklärte Recordvertrag vorsieht; ihre bloße Speicherung darf keine neue Dephasierung erzeugen. Ein neuer maximaler Punkt x wird durch seine vorgeschriebene Vorgängermenge eingefügt; diese ist ein Downset des vorhandenen Präfixes. Für jeden Vorgänger y lässt sich dann

\[
n(y,x)=\#\{z\text{ im gespeicherten Präfix}:y\prec z\prec x\}
\]

berechnen. Der Wert darf für die Auswertung von b bei vier abgeschnitten werden. Ein solcher abgeschnittener Einzelwert erlaubt jedoch nicht, die gesamte frühere Relation für alle späteren Fortsetzungen zu vergessen.

Beim Anfügen eines maximalen Punktes verändern sich keine Intervalle zwischen bereits vorhandenen Punkten. Der neue Wirkungsfaktor ist deshalb exakt durch

\[
s_x=\kappa\left(1-\sum_{y\prec x}b_{yx}\right)-\frac{r_x}{2}
-\frac\beta4\sum_{y\prec x}b_{yx}
\left[r_x(T_x-T_y)^2+(q_x-q_y)^2\right]
\]

gegeben, und `S_C=sum_x s_x`. Für C1 wurde außerdem die zulässige Reihenfolge `0,1,2,3,5,4,6,7,8,9,10` geprüft. Die vollständige Wirkung ändert sich nicht.

Das ist ein gerichtetes Auswertungsverfahren für eine erklärte Ordnung. Es enthält keine Gleichung, die aus einem physischen Anfangszustand die nächste Ordnung auswählt.

## 3. Explizite Kopierkerne und Kompositionsidentität

Sei `x_k` der im Schritt k eingefügte Vertex, `m_k` die vollständige Erinnerung danach und `p_k` ihre Projektion auf die vorherige Erinnerung. Mit einer Dirac-Punktmaß-Notation lautet der Kernel

\[
\mathcal T_k^\epsilon(m_k;dm_{k-1})
=e^{is_{x_k}(m_k)}e^{-\epsilon\,1_I(x_k)q_{x_k}^2/2}
\delta_{p_k(m_k)}(dm_{k-1}).
\]

Das Delta kopiert die alte Erinnerung, statt sie unabhängig zu mitteln. Es ist hier ein Punktmaß im Erinnerungskernel; es wird keine unbegründete Delta-Dichte relativ zum atomar-kontinuierlichen Dichtemischmaß verwendet. Die ursprünglichen Feldmaße treten erst bei der finalen gemeinsamen Paarung beziehungsweise ihrer erlaubten Fubini-Gruppierung auf.

Für eine Folge von Schritten folgt unmittelbar

\[
\mathcal T_{c:b}^\epsilon\circ\mathcal T_{b:a}^\epsilon
=\mathcal T_{c:a}^\epsilon.
\]

Die Kopierprojektionen komponieren, die Wirkungsinkremente addieren sich, und jeder neu eingeführte innere Skalarregulator erscheint genau einmal. In beiden Klammerungen dreier Schalen ergibt sich derselbe gemeinsame Integrand.

Die final gepaarte feste Historienamplitude ist

\[
\mathcal A_C^\epsilon=
\int d\lambda_I(T)\,d\nu_I(r)\,dq_I\,dq_B\;
\Phi_B(q_B)\,e^{iS_C}\,e^{-\epsilon\sum_Iq_j^2/2},
\]

bei den festen gemeinsamen Randuhren und Randdichten. Für jedes `epsilon>0` ist dieser endliche Integrand absolut integrierbar: Uhr- und Dichtemaße sind endlich, der gemeinsame Rand-Gaußfaktor ist integrierbar, und alle drei inneren Skalarintegrationen sind gedämpft. Deshalb darf nach den Schnitten hinter 3 und hinter 5 gruppiert werden. Die Gleichheit der Integrale und ihre Assoziativität folgen hier aus der exakten Integrandidentität und Fubini; sie wurden nicht durch eine neue numerische Quadratur geschätzt.

Beim Übergang `epsilon→0+` ist die **gemeinsame** Randtestpaarung beizubehalten. Insbesondere ist C1 ein distributioneller innerer Skalarfall. Eine Komposition separat vorgenommener singulärer Grenzwerte ist aus dieser Rechnung nicht gerechtfertigt. Wenn der gemeinsame Testgrenzwert existiert, sind die Gruppierungen gleich, weil sie für jedes positive epsilon identisch sind. Die Existenzprüfung dieses Skalargrenzwertes bleibt die des gemeinsamen Amplitudenvertrags.

Die Gravitationsphase ist bereits Teil von `S_C` und damit des in TASK 1 bezeichneten Faktors `W_C`. Eine erneute Multiplikation mit `exp(i S_stationär)` würde die Wirkung doppelt zählen und ist ausgeschlossen.

## 4. Zwei Schnitte und nachweislich fehlende Kreuzterme

Für einen natürlichen Präfixschnitt `P|F` sind P und F ordnungskonvex. Deshalb bleiben die Koeffizienten innerhalb der beiden Restriktionen unverändert. Die vollständige Identität ist

\[
S_C=S_{C|P}+S_{C|F}+S_\times,
\]

wobei alle Beziehungen `y in P`, `x in F` mit ihrer **vollen** Intervallgröße in `S_cross` stehen. Das bloße Produkt lokaler Wirkungsphasen lässt diesen Faktor weg.

| Ordnung | Schnitt hinter | Nichtverschwindende Kreuzpaare | Fehlender Gravitationsbeitrag |
|---|---:|---:|---:|
| C0 | 3 | 10 | 1 |
| C0 | 5 | 10 | 1 |
| C1 | 3 | 12 | 9 |
| C1 | 5 | 12 | 9 |

In allen vier Fällen wurden sämtliche rationalen Monomkoeffizienten der vier Sektoren `kappa`, `dust_constant`, `beta*dust`, `beta*scalar` verglichen. Der direkte gemeinsame Ausdruck stimmt exakt mit dem lokalen Ausdruck plus Erinnerungsterm überein. Der lokale Ausdruck allein stimmt nicht überein. Das gezielte Entfernen eines echten Kreuzpaares lässt die Kontrolle ebenfalls fehlschlagen.

Ein zusätzlicher exakter rationaler Feldtest steht vollständig in `results.json`. Er dient nur als unabhängig lesbarer algebraischer Kontrollpunkt und wird nicht als weitere Quelle oder als Stationärzustand des Experiments ausgegeben. Beispiel C0, Schnitt hinter 3: Der fehlende Kreuzbeitrag besitzt die Koeffizienten `(1,0,523/800,8879/484)`. Bei C1 sind es `(9,0,81/100,11969/484)`.

Die Relation `(0,10)` hat in beiden Ordnungen neun offene Zwischenpunkte und deshalb den Koeffizienten null. Auch diese lange Relation bleibt als Ordnungsinformation im vollständigen Speicher vorhanden. Ihr verschwindender unmittelbarer Wirkungsbeitrag ist keine allgemeine Erlaubnis, alte Relationsinformation zu löschen.

## 5. Ein wirklich geometrisches, aber noch nicht physisch kalibriertes Ereignis

Die Zahl vergleichbarer ungeordneter Innenpaare

\[
O(C)=\#\{\{a,b\}\subset I:a\prec b\text{ oder }b\prec a\}
\]

ist ein relabelungsinvariantes kombinatorisches Historienobservable. Es ergibt `O(C0)=3` und `O(C1)=1`. Damit unterscheidet der Kandidat tatsächlich zwei innere Kausalgeometrien. O ist weder ein terminaler Skalarmodus noch ein willkürlich als Radius bezeichneter Feldwert.

Aus diesen zwei Werten folgt jedoch noch keine physische Verteilung `P(O|Quelle)`. Die kohärente Einsetzung eines Quellenfaktors `exp(i J O(C))` in die Historienamplitude ist algebraisch möglich, liefert aber zunächst eine eingefügte Amplitude. Ein orthogonales Detektorflag für O würde die beiden Ordnungen unterscheiden und die zugehörigen Kreuzterme aus den nicht nachselektierten Klassenwahrscheinlichkeiten entfernen. Welche geometrische Messung oder Dekohärenzpaarung physisch zulässig ist, bleibt separat zu begründen. Dieser Unterschied darf bei der Übertragung der Interferenzanalyse auf eine Geometrieantwort nicht übersprungen werden.

## 6. Status und Reproduktion

```sh
python -B checks/composition/check.py
```

Python-Standardbibliothek genügt. Bestanden sind 22 Präfixidentitäten, vier vollständige Schnittvergleiche, vier gezielte Weglasskontrollen, beide Klammerungen der drei Schalen, alternative natürliche Beschriftung und die geometrischen Werte 3 beziehungsweise 1. Der Code liest den gemeinsamen Vertrag und dokumentiert dessen Hash. Null neue Integrationen; keine neue physische Wahrscheinlichkeit.

**Geschlossen:** eine explizite, vollständige und assoziative Kompositionsregel für diesen endlichen bedingten Wirkungs-/Randamplitudenkandidaten.

**Weiter offen:** physische Auswahl der Historiengewichte und Randpaarung, geometrische Messdeutung, Massenskala, physische Uhr und geometrische Evolution unter Verfeinerung. Weder `K†K` noch ein frei gewähltes `log(K)` wird zur Schließung dieser Lücke eingesetzt. Auch ein externzeitlicher unitärer Operator wird nicht als einzige mögliche Definition physikalischer CST-Dynamik vorausgesetzt.
