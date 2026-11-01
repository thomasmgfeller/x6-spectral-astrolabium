# Relative Referenzkalibrierung bei mittlerer Nachweisrate

## 1. Welche Größe gemessen wird

Im vollständigen vierdimensionalen Kausaldiamanten von v0.4 bezeichnet K(f) das Verhältnis von wesentlichem Supremum zu wesentlichem Infimum der wissenschaftlichen Beprobungsdichte pro physischem Vierervolumen. Der Zielwert ist K*=501/500. Bei festem h∈[0,1/2] sind 3.200.000 wissenschaftliche Ereignisse unabhängig. Für die normierte Beprobungsdichte gilt f∝s e t mit Erzeugungsdichte s, Referenzeffizienz e∈(0,1] und Transferfaktor t einschließlich Drift. Wie in v0.5 sind K(s)≤S, K(t)≤D und innerhalb jeder vollständigen Zelle sup(e)/inf(e)≤C extern zu belegen. Hier sind S=D=C=1,0001. Die lokalen Schranken gelten für die Wissenschafts- und Referenzverteilung jeweils fast überall. Die Referenzmessung ist von der Wissenschaftsordnung und ihrer Gruppierung unabhängig.

Die vorab bekannte Partition umfasst J=16 Zellen. Jeder markierte Referenzversuch einschließlich eines Ausfalls wird erfasst. In jeder Zelle j werden n unabhängige Bernoulli-Versuche mit gemeinsamer marginaler Erfolgswahrscheinlichkeit p_j erhoben, unabhängig auch über Zellen. Ein Beispiel sind unabhängig gezogene Positionen mit ortsabhängiger Detektion e. Ein Positionsraster mit deterministischen, unterschiedlich effizienten Einzelpositionen erfüllt das Binomialmodell im Allgemeinen nicht.

Für jede Zelle gilt p_j/C≤e≤C p_j. Daraus folgt K(f)≤SDC²·p_max/p_min. Setze L=K*/(SDC²)=10020000000000000/10004000600040001. Die günstige Klasse besteht wie zuvor aus p_min≥0,49 und p_max/p_min≤r=1,0002. In ihr ist K(f)≤K*. Bei vorheriger Wahl der relativen Route lautet die neue Regel für die beobachteten Trefferquoten x_j

    GO genau dann, wenn max(x) − L min(x) ≤ −t,
    n=47.000.000 je Zelle, t=246/1.000.000.

Die Software vergleicht ganze Trefferzahlen mit einer rational bestimmten Abrundung. Die absolute Route aus v0.5 für sehr hohe Effizienz bleibt als vorab wählbarer separater Plan verfügbar. Das nachträgliche Wählen der günstigeren Route oder das Wiederholen bis zum Bestehen fällt außerhalb des Designs.

## 2. Gerichtete Fehlerschranke für ein Zellenpaar

Schreibe W für die zentrierte Summe aus den n Bernoulli-Variablen von i mit Gewicht 1 und den n Variablen von j mit Gewicht −L. Es gilt Var(W)=nv, v=p_i(1−p_i)+L²p_j(1−p_j)≤v_max=(1+L²)/4. Die folgende Rechnung gilt für W und −W. Für 0≤v_l≤v≤v_h und u>0 setze λ=u/(v_h+Lu/3). Bei v_h>0 gilt λL<3.

Für einen zentrierten Einzelsummanden Z mit |Z|≤L gilt E|Z|ᵏ≤Lᵏ⁻² E Z² (k≥2). Aus k!≥2·3ᵏ⁻², 1+y≤exp(y) und Unabhängigkeit folgt

    log E exp(λW) ≤ nv λ² / [2(1−λL/3)].

Ändere das Wahrscheinlichkeitsmaß mittels dP_λ/dP=exp(λW)/E exp(λW). Dann

    P(W≥nu) ≤ exp[−nu²/(2(v_h+Lu/3))] · A,
    A=E_λ[exp(−λ(W−nu)) 1{W≥nu}] ≤ 1.

Unter P_λ bleiben die Einzelversuche unabhängig und Bernoulli-verteilt. Für einen Summanden mit Gewicht w verschiebt sich der Logarithmus der Erfolgsodds um λw. Die Ableitung von log[p(1−p)] nach dem Logarithmus der Odds ist 1−2p und hat Betrag höchstens 1. Deterministische Summanden tragen Varianz null bei. Die gekippte Varianz erfüllt also σ²≥nv_l exp(−λL)≥nv_l(1−λL). Die rechte Schranke wird nur bei v_l>0 und λL<1 verwendet.

Unter dem geänderten Maß ist jeder um seinen neuen Erwartungswert zentrierte Einzelbeitrag betragsmäßig durch L beschränkt. Die Summe der absoluten dritten zentralen Momente ist daher höchstens Lσ². Der Satz von Berry und Esseen für unabhängige, nicht notwendig gleichverteilte Summanden begrenzt den Abstand zur Normalverteilungsfunktion mit passender Lage und Varianz durch ε=0,56 L/σ. Insbesondere hat jedes geschlossene Intervall der Länge s eine Wahrscheinlichkeit von höchstens s/[σ√(2π)]+2ε. Der linke Grenzwert der Verteilungsfunktion schließt einen möglichen Gitteratom am Intervallanfang ein. Durch Integration folgt

    A = ∫₀∞ λ exp(−λs) P_λ(nu≤W≤nu+s) ds
      ≤ min(1, [0,4/λ + 1,12 L]/σ).

Hier wurde 1/√(2π)<0,4 benutzt. Diese Abschätzung verwendet die Normalverteilung nur innerhalb einer expliziten Fehlerschranke; sie ersetzt die endliche Verteilung nicht durch eine asymptotische Formel.

Die Zertifizierung überdeckt [0,v_max] durch 100 lückenlos angrenzende, gleich breite geschlossene Teilintervalle. Auf jedem davon verwendet sie die obere Varianzgrenze im Exponenten und die untere Grenze für den Vorfaktor. Bei v_l=0 verwendet sie A≤1. Alle verwendeten positiven Quadratwurzeln werden rational nach unten eingeschlossen. Für exp(−z) wird der Kehrwert der positiven Taylor-Teilsumme von exp(z) bis einschließlich Grad 64 genommen. Jede ausgewiesene obere Wahrscheinlichkeit ist abschließend auf 10⁻¹² nach oben gerundet. Es werden sämtliche Teilintervalle geprüft, keine Varianz wird aus dem Pilot geschätzt.

## 3. Übergang von einem Paar zur Kalibrierung und Geometrie

Falls K(f)>K*, hat mindestens ein festes gerichtetes Paar p_i−L p_j>0. GO erzwingt für dieses Paar eine negative zentrierte Abweichung von mindestens nt. Das Maximum der 100 Schranken für u=t ist 0,009880972695. Ein Multiplikator für die Anzahl der Paare ist für diese Fehlfreigabe nicht erforderlich.

In der günstigen Klasse gilt für jedes gerichtete Paar p_i−L p_j≤−d mit d=0,49(L−r). Die Regel scheitert nur, wenn mindestens ein Paar eine positive Abweichung größer als n(d−t) zeigt. Die Maximaldifferenz wird auch bei gleichen Zellwerten durch ein Paar mit i≠j erreicht. Es gibt 240 geordnete Paare. Die Vereinigungsabschätzung mit den Varianzgrenzen liefert P(HOLD)≤0,002620553280. Somit ist P(GO)≥0,997379446720.

Bei HOLD ist die Ausgabe der gesamte Bereich h∈[0,1/2], q=RT²∈[0,48 atanh(1/4)²] und h∈{0,1/4,1/2} für das Raster. Bei GO verwendet man ausschließlich die publizierte, nach Kausalordnung gruppierte v0.4-Regel (400.000 disjunkte Achtergruppen und 11.200.000 Vergleichbarkeitsabfragen). Im Bereich K(f)≤K* ist die unbedingte Fehlüberdeckung höchstens 1−0,951569406, weil ein HOLD immer überdeckt. Im disjunkten Bereich K(f)>K* ist sie höchstens die Fehlfreigabe. Das Maximum der beiden Schranken liefert mindestens 0,951569406 Überdeckung für jeden festen Parameter. Bei günstigem Aufbau und wahrem Rasterpunkt folgt aus der Unabhängigkeit der Datenquellen mindestens 0,997379446720 × 0,803252245 ≥ 0,801147279694 Wahrscheinlichkeit für die richtige Einzelausgabe. Die Aussage gilt über alle Wiederholungen einschließlich HOLD. Sie ist keine nachträgliche Vertrauensaussage über einen beobachteten GO-Fall. Zusätzliche Unsicherheit stochastisch ermittelter externer Kontrastgrenzen benötigt ein eigenes Fehlerbudget.

## 4. Warum auch andere feste Pläne viele Messungen benötigen

Betrachte ein beliebiges vorab festgelegtes Paar verschiedener Zellen i,j. Alle anderen Zellen erhalten in beiden Anlagen Effizienz 1/2. Die Referenzpositionen seien unabhängig, gleichförmig innerhalb jeder Zelle. Die externen Zusagen sind in beiden Fällen dieselben. Das Verfahren darf die erfassten Positionen, alle anderen Zellen und unabhängige Randomisierung verarbeiten. Es erhält keine weitere Information, die die beiden Anlagen vorab unterscheidet.

In der günstigen Anlage haben die beiden Zellen konstante Effizienzen a=r/(1+r) und 1−a. Beide überschreiten 0,49 und die Quote der Zellmittel ist genau r. In der zweiten Anlage wähle b>L/(1+L), nahe an diesem Grenzwert, und zunächst die Basiswerte b,1−b. In einem Untergebiet positiver Referenzmasse η der hohen Zelle setze e=Cb und in einem ebensolchen Untergebiet der niedrigen Zelle e=(1−b)/C. Die Untergebiete haben positives physisches Volumen. Für diese b bleiben die Effizienzen zwischen 0 und 1. Die Zellkontraste erfüllen die zugesagte C-Grenze. Wähle in beiden Anlagen s=S und den Transferfaktor t_ext=D in der hohen Zelle, sonst jeweils 1. Eine tatsächliche Wissenschaftsselektion e·t_ext liegt in dieser Konstruktion ebenfalls unter eins. In der zweiten Anlage ist K(f)=SDC² b/(1−b)>K*. Jede gültige Regel muss hier P(GO)≤0,01 einhalten.

Bei jeder endlichen, festen Versuchszahl m=n_i+n_j ist die Chance, überhaupt einen der geänderten Teilbereiche zu treffen, höchstens mη. Eine Kopplung mit identischen Positionen und Detektionszufällen zeigt, dass die Beobachtungsgesetze für η→0 in Totalvariation gegen die konstanten Basiswerte konvergieren. Anschließend lasse b↓b*=L/(1+L). Bei den endlichen Bernoulli-Stichproben bleiben alle Testwahrscheinlichkeiten stetig. Daher gilt P(GO)≤0,01 auch für das Grenzgesetz. Der Grenzparameter wird nur für diesen Testvergleich gebraucht.

Zähle in der hohen Zelle Treffer und in der niedrigen Ausfälle. Der Gesamtscore T ist dann Bin(m,a) unter der günstigen und Bin(m,b*) unter der grenzwertigen Anlage. Die Likelihood-Quote des vollständigen Versuchs für günstig gegen grenzwertig ist streng fallend in T. Weitere Zellzählungen, Positionen und unabhängige Randomisierung ändern diese Quote nicht. Also maximiert bei gegebener GO-Wahrscheinlichkeit unter dem Grenzgesetz ein unterer Schwellenwerttest, ggf. mit Randomisierung am Rand, die GO-Wahrscheinlichkeit unter dem günstigen Gesetz (Neyman–Pearson).

Bei m=52.600.000 und k=26.312.578 ergibt die gerichtete Binomialrechnung

| Gesetz | Untere Schranke für P(T≤k) | Obere Schranke |
|---|---:|---:|
| günstig | 0,996960670953 | 0,996960670954 |
| grenzwertig | 0,010003844730 | 0,010003844731 |

Selbst der Schwellentest, dem unter dem Grenzgesetz mehr als 1 % GO erlaubt wird, erreicht günstig weniger als 99,7 %. Jede Regel mit höchstens 1 % Fehlfreigabe verfehlt hier also die günstige Zielrate. Kleinere m können durch das Verwerfen zusätzlicher Beobachtungen dargestellt werden. Jedes mögliche Zellenpaar muss daher n_i+n_j≥52.600.001 erfüllen. Die Summe über acht disjunkte Paare liefert mindestens **420.800.008** Versuche. Bei gleichen festen Zellbudgets sind je Zelle mindestens 26.300.001 und insgesamt **420.800.016** nötig. Die erste Schranke ist bewusst als einfache gültige Untergrenze ausgewiesen. Die vollständige Menge aller Paarbedingungen kann sie bei ganzzahligen Budgets noch um einzelne Versuche verbessern. Die Rechnung beansprucht weder optimale Budgets noch eine Untergrenze für adaptive Versuchspläne, andere Referenzinformationen oder schwächere Fehlerziele.

Für die gerichtete Rechnung setzt die Implementierung das Gewicht des Binomialmodus auf eins und erzeugt in beiden Richtungen relative Wahrscheinlichkeiten mit den exakten benachbarten Gewichtsquotienten. Die Gewichte werden mit Skala 2¹⁹² nach unten und oben gerundet. Bei ±90.000 ganzzahligen Schritten um den Modus endet die Rekursion. Jede ausgelassene Masse ist wegen der Monotonie außerhalb des Modus höchstens die Anzahl ausgelassener Terme mal das letzte obere Gewicht derselben Seite. Der Quotient aus Teilsumme und Gesamtsumme wird nach außen eingeschlossen.

## 5. Herkunft und Einordnung

- Publizierte Modellannahmen, Dichtezwillinge und Geometriezertifikat. [Eigenzeit v0.4](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/167).
- Vorherige Messpläne, Evidenzfelder und Hellinger-Untergrenze. [Eigenzeit v0.5](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/168).
- Konstante in der allgemeinen Berry–Esseen-Ungleichung. Shevtsova berichtet ≤0,5583. Hier genügt 0,56. [Informatics and Applications 7 (2013), S. 124–125](https://www.mathnet.ru/eng/ia252).
- Optimalität des Likelihood-Quotiententests für zwei einfache Gesetze. [Penn State, STAT 415, 26.1](https://online.stat.psu.edu/stat415/lesson/26/26.1).

Die Garantie bezieht sich auf das definierte statistische Experiment. Die synthetischen Belastungstests im Paket sind unabhängig von ihrer mathematischen Herleitung.
