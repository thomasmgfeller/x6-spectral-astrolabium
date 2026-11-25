# Dichte an Ereignis 12 und ihr späterer Nachweis

CST-DUST · 25. November 2026 · Typ 2097151 · Repository-Stand `bc909230d38975d3201175b56dfbe9ae8bfda087`.

Der feste Zukunftsrand besitzt für die beiden Dichteklassen nur eine gemeinsame Zustandsrichtung. Für den hier geprüften vollständigen Ausgang ist ein perfektes Dichtebit ausgeschlossen. Die physikalische Auslese bleibt auf **HOLD**. Am inneren Schnitt hinter 13 lässt sich eine absolute Dichteschwelle mit hoher Genauigkeit aus einer dort noch offenen Uhrdifferenz erschliessen. Der fast gleiche Wert bei ausgeschalteter Wirkungsphase zeigt, wie viel davon bereits im präparierten Dichteband steckt.

## 1 · Zwei verschiedene Fragen an dieselbe Präparation

Verwendet werden die Gesamtordnung (0,1,2,3,4,5,6,11,12,13,14,7,8,9,10), der Publikationsfall M=1, e=1/4, K=15/4, D=K(3/722)^(1/4) und die gemeinsamen reellen, flachen Präparationen aus der [Randrechnung hinter 13](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/bc909230d38975d3201175b56dfbe9ae8bfda087/research/rax_cqg/dust_collapse/n15_uhr5_randpaarung_hinter_13_v0_1/HERLEITUNG.md). Die Dichtemarke M ist dabei ein Modelleingang. Es gilt x=w₁₂/D. Mit v=u₁₁ und b=u₁₃ ist die Zellbreite f=(b−v)/2. Der ursprüngliche Träger ist [0,99f,1,01f].

* **Relative Hälfte.** Liegt x unter f oder mindestens bei f? Das teilt die vorbereitete Streuung jeder Zelle gleich. Beide Klassen besitzen bei gegebenen Uhren das gleiche Volumen. Am Schnitt direkt hinter Ereignis 12 ist b noch offen. Bei demselben Präfix mit v=1/2, x=1/8 und den Fortsetzungen b=3/4±1/1024 hat x/f−1 die Werte +1/255 bzw. −1/257. Das Vorzeichen der relativen Abweichung ist somit erst mit der nächsten Uhr bestimmbar.
* **Absolute Schwelle.** Liegt x unter 1/8 oder mindestens bei 1/8? Bei dem vorgegebenen D hängt die Klassengrenze von keiner späteren Uhr ab. Die beiden Integrale schneiden das jeweilige ursprüngliche Band mit diesen Halbräumen. Leere und einseitig besetzte Zellen bleiben im Lauf. Die Grenze 1/8 ist die Mitte der Referenzzelle. Dieser ergänzende Vergleich wurde am 25. November angesetzt. Er besitzt keine externe Vorregistrierung.

In beiden Fällen teilen wir die Amplitude vor dem Integral über x. Es gilt B = B_L+B_H. Wegen der stetigen Dichte hat der Teilungspunkt Mass null. Der halbe Bandfaktor bzw. die tatsächliche Teilbreite bleiben in den Amplituden. Für die operative Zwei-Klassen-Gegenrechnung werden die Zweigintensitäten addiert. Beim Vergleich mit den bedingten Mittelwerten des zweiklassigen Vorgängercodes kürzt sich für gleich breite Hälften im normierten Uhranteil ein gemeinsamer Faktor. Beim Test der Zustandsunterscheidung werden die beiden nichtverschwindenden Schnittspalten einzeln normiert und gleiche Vorchancen gesetzt. Das sind bedingte Trennbarkeiten in der genannten Hilfspaarung. Eine Aussage über tatsächlich unabhängig präparierbare Eingangszustände oder über die natürliche Häufigkeit der zwei Klassen braucht weitere physikalische Eingaben.

## 2 · Zertifikat der relativen Unterscheidbarkeit

Für jedes aktive Paar mit j als späterem Ende gelten die Gewichte bᵢⱼ=(1,−9,16,−8) für 0 bis 3 Zwischenereignisse, sonst null. Der dimensionslose Koeffizient ist cⱼ=−1/2−Σᵢbᵢⱼ(Yⱼ−Yᵢ)²/38. Die beiden rechten Pulse verändern die Verwendung von Y₆ bei j=12,13,14 um ±1/(8√D). Die Zellen und das Mass bleiben auf den ursprünglich vorbereiteten Uhren definiert. Das Verbinden jedes Punkts der tiefen Hälfte mit x+f/100 in der hohen Hälfte erhält alle Massfaktoren und ergibt punktweise den Phasenzuwachs δ=D c₁₂ f/100. Bei zentralen Uhren ohne Puls gilt c₁₂=−799/2048 und δ=−799D/1638400 ≈ −0,000464306 rad. Diese Zahl gehört zu zwei Dichtehälften. Der ältere Wert 1/2736 bezog sich auf die zwei Uhr-5-Pakete.

Das Programm schliesst das Intervall [δ₁,δ₂] sowie die ganze Phase am Schnitt mit 256-Bit-Intervallarithmetik ein. Konstante, gemeinsame Kragenfaktoren werden vorher entfernt. Für beide Hälften liegt die Phase in einem Sektor mit Halbwinkel θ. Für positive reelle Eingangsgewichte folgt |B_H| ≥ (1−θ²/2)∫W, und ebenso für B_L. Dabei ist W das positive Integrationsgewicht der jeweiligen Hälfte. Mit d=(δ₂−δ₁)/2 und δ₀=(δ₁+δ₂)/2 gilt punktweise nach den frühen Integrationen |exp(−iδ₀)B_H−B_L| ≤ d∫W. Leere Ausgangspunkte tragen null bei. Die Aussagen gelten auch für jedes einzelne Uhr-5-Paket und die gleichphasige Summe.

Die Projektion der hohen Spalte auf das orthogonale Komplement der tiefen hat somit Norm höchstens d‖B_H‖/(1−θ²/2). Für jedes gemeinsame nichtnegative diagonale Randmass mit endlichen, positiven Ausgangsnormen ist dies eine Schranke für die Spurweite T=√(1−|⟨L,H⟩|²) der normierten reinen Zustände. Die optimale Einzelentscheidung bei gleichen Vorchancen hat Trefferwahrscheinlichkeit (1+T)/2. [Watrous, The Theory of Quantum Information, Kap. 3, Satz 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf)

| Rechte Pulswahl | Untergrenze der normierten Überlappung | Obergrenze der optimalen Trefferquote |
|---|---:|---:|
| − | 0,999999958245 | 50,014449 % |
| 0 | 0,999999956863 | 50,014687 % |
| + | 0,999999955806 | 50,014866 % |

Die Prozentobergrenzen sind aufwärts gerundet. Numerisch erhält man im flachen Schnittmass beim niedrigen Dichtetag, gleichphasiger Präparation und Nullpuls 50,00121548 %. Die Relativphase der integrierten Spalten beträgt −0,000465036 rad. Bei relativer Eingangsphase π sind es 50,01633293 %. Diese Präparation hat gegenphasige Beiträge und liegt ausserhalb der bewiesenen Sektorabschätzung. Das Ergebnisarchiv enthält beide Tags, beide Einzelpakete, alle vier relativen Phasen und alle drei Pulse.

## 3 · Absolute Schwelle am inneren Schnitt

Für die nachfolgende Tabelle gelten der niedrige frühe Tag, beide gleichphasigen Uhrpakete, der Nullpuls und das flache positive Randmass des Vorgängers. Der Schnitt hält die beiden Uhren v und b noch fest. Bereits das Beobachten von f und die einfache Regel „hoch genau dann, wenn f≥1/8“ erlauben die unten gezeigte Zuordnung. Wer nur dann entscheidet, wenn das gesamte Band auf einer Seite liegt, hat in diesen Fällen exakt null Fehler. Der unentschiedene Rest beträgt rund 10,7862 %. Das optimale binäre Hilfsgerät dürfte allgemein beide normierten Zustandsfunktionen im Schnittraum messen. Seine Wirkung ist im Staubmodell noch herzuleiten.

| Grösse am Schnitt | Gekoppelte Staubphase | Alle Staubphasen auf 1, identische Fenster und Jacobifaktoren |
|---|---:|---:|
| Überlappung der normierten Spalten | 0,05475777 | 0,05475776 |
| Optimale Trefferquote, gleiche Vorchancen | 99,92498340 % | 99,92498341 % |
| Trefferquote aus f allein | 98,61525047 % | 98,61525061 % |
| Anteil sicherer Antworten bei zugelassener Enthaltung | 89,21383696 % | 89,21383766 % |

Ein geometrischer Nachweis des gemeinsamen Trägers gelingt bei v=1/2, b=3/4. Beide Teilbänder haben positive Länge, auch auf einer offenen Umgebung dieses Punkts. Die beiden Amplituden liegen dort im selben engen Phasensektor. Der reelle Kreuzterm ist auf der Überlappung strikt positiv und ausserhalb null. Die gewöhnliche flache Randpaarung macht die absolute Klassenteilung damit ebenfalls nicht orthogonal. Die beiden unnormierten Gewichte besitzen im Nullpulsfall das Verhältnis H/L≈1,090155. Die gleiche Vorchance in der Tabelle ist ein ausdrücklich gewählter Vergleich. Das Berechnen einer physikalischen Verteilung aus den Klassengewichten ist eine separate Frage.

## 4 · Pulsprüfung und geschlossener Ausgang

Der frühe Prüftag für die Statistik der Uhr 11 ist der Schnitt ihres Fensters bei u₁₁=1/2. Nach beiden Dichtezweigen und allen zulässigen späten Randwerten wird summiert. Der relative Jittertest reproduziert für den niedrigen Tag und Eingangsphase π den früheren numerischen Unterschied p(u₁₁<1/2 | Pluspuls) − p(u₁₁<1/2 | Minuspuls) ≈ +5,6993·10⁻¹⁰. Der absolute Schwellentest gibt bei gleichem Tag und Eingangsphase 0 für dieselbe Uhrstatistik −1,4519·10⁻⁹. Der aus beiden Gewichten normierte Anteil der niedrigen absoluten Dichteklasse ändert sich um +1,8518·10⁻⁹. Dies sind Diagnosen der vorgeschlagenen Randpaarung. Die Unterschiede sind numerisch per zweiter Quadratur kontrolliert, ohne strengen Integrationsfehlerbeweis. Auf einer exakt aufgelösten Dichtefaser am Schnitt 13 fällt die gemeinsame Pulsphase aus der Intensität. Ein physisch erzeugter Dichtespeicher ist im geprüften Modell offen.

Bei vollständigem Abschluss werden sämtliche inneren Uhren und Dichten integriert. Alle vier Zukunftsuhren und alle vier Zukunftsdichten sind fixiert. Auf dem festen Typ faktorisiert die masselose Skalarwirkung bei der gegebenen gemeinsamen Präparation von den Staubvariablen. Damit gilt für beide Klassenteilungen Ψ_L=Z_L χ und Ψ_H=Z_H χ mit derselben skalaren Randwelle χ. Die gewöhnliche Gravitationsphase und der gemeinsame frühe Kragenfaktor sind ebenfalls unabhängig von der Klasse. Der früh integrierte Kragenfaktor ist bei festem e ungleich null, da |Σ_p c_p|/32<1. Der ganze verbleibende staubabhängige Phasenbereich besitzt selbst im ungünstigsten der drei Pulse eine Halbbreite unter 0,273 rad. Damit ist für jede Klasse mit positivem Volumen und den gleichphasigen Paketen der Staubkoeffizient von null verschieden. Die Bilddimension ist bei nichtverschwindender gemeinsamer Skalarwelle genau eins. Nach Normierung sind die Dichtematrizen identisch, die Spurweite ist null. Auch eine neue positive Paarung auf demselben eindimensionalen Bild kann die Spalten nicht trennen. Ein Nullarm bei einer anderen destruktiven Präparation wäre ein Ausfall. Eine relative Phase der Koeffizienten könnte mit einer gesonderten kohärenten Referenz interferieren. Hier hat der Empfänger nur den festgelegten Ausgangszustand.

## 5 · Test der Kausaldiamanten an der Wirkung

Auf der Referenzkette besitzen beide Dichteklassen alle 105 gleichen vergleichbaren Paare. Zwischen den inneren Kragenrändern liegen sieben Ereignisse und die längste Kette hat acht Kanten. Jedes reine Ordnungshistogramm ist auf beiden Klassen gleich.

Im Katalog mit 1 048 Typen wurden drei Signaturen zusätzlich mit den publizierten Entscheidungen zur Zwei-Prozent-Grenze bei M=4 abgeglichen. Diese Tabelle deckt 61 Typen und zwei Eingangsdichtezentren ab. Die Referenzkette gehört nicht zu diesen 61. Die Angaben über Konflikte gelten je Dichtezentrum.

| Signatur | Klassen im Vollkatalog | Belegt durch 61 Typen | Klassen mit ≥2 geprüften Typen | Davon mit widersprechenden Entscheidungen, bei 1/8 bzw. 1/4 |
|---|---:|---:|---:|---:|
| Festes Kragenpaar | 6 | 2 | 2 | 2 / 2 |
| Alle Paare, ohne Sektoren | 527 | 43 | 11 | 3 / 3 |
| Alle Paare, mit Endpunktsektoren | 1 021 | 54 | 7 | 0 / 0 |

Für alle 1 048 Typen ist ein exakter, direkt aus der Staubwirkung berechenbarer Test verfügbar. Für ein inneres Ziel j ist λⱼ = −19 ∂wⱼ ∂²Yⱼ S = Σᵢ bᵢⱼ. Bewertet wird die sortierte Multimenge dieser sieben Zahlen. Vier der 25 mehrfach besetzten sektormarkierten Diamantklassen enthalten verschiedene Multimengen. So hat 338877 die Werte (−15,0,0,0,0,0,1), 339639 die Werte (−24,0,0,0,0,0,10). Das gleiche Diamanthistogramm reicht somit für diese lokale Antwort der Wirkung nicht aus. Ergänzt um die sieben sortierten Werte entstehen 1 025 Klassen. Der Test bezeichnet eine mathematische Wirkungsableitung. Er setzt keine physikalisch zugängliche Einzeluhrmessung voraus.

**Physikalischer Stand.** Die Präparation enthält am Schnitt 13 einen starken Hinweis auf eine absolute Dichteklasse. Das dynamische Kriterium verlangt, dass diese Information in einem später zugänglichen Freiheitsgrad erhalten bleibt und die ausgangssummierte frühe Statistik eine unabhängig begründete positive Paarung hat. Für die Fortsetzung braucht es einen solchen konkreten Träger mit Kopplung vor dem Verlust der Dichteinformation. Die 60 physischen P3-Einträge führen weiterhin NOT_RUN. Hier wurden keine der 524 physischen Einzelvergleiche freigeschaltet.

## Offline-Reproduktion

Python 3.10+ und NumPy. Referenzlauf mit Python 3.12 und NumPy 2.3.5. `fenster.py` und `diamantklassen.py` verwenden die Standardbibliothek. Bei der relativen Teilung werden Gauss-Legendre mit 5 und Clenshaw-Curtis mit 6 Knoten je Achse verwendet, bei der absoluten Schwelle 4 und 5. Alle tagabhängigen Intervallgrenzen werden vor der Auswertung aufgelöst. Bei f-abhängigen Grenzen werden auch die beweglichen Schnittpunkte in b und ihre Wechselpunkte in v separat behandelt. Ein Arm integriert die Schichtkoeffizienten aus der Rangdistanz, der zweite aus den offenen Ordnungsintervallen. Die beiden Verfahren teilen den Modellvertrag und Teile des Programms. Die Übereinstimmung dient als numerische Kontrolle.

```sh
sha256sum -c SHA256SUMS
OPENBLAS_NUM_THREADS=1 python3 -B pruefen.py
```

Das Quellenregister benennt die Git-Objekte und das Prüfpaket vom 24. November. Das lokale Manifest deckt alle mitgelieferten Eingaben, Resultate, Programme und den Kurzbericht ab. Die Eingaben der etablierten Hilfsrechnung wurden gegen die publizierten Git-Objekte geprüft.
