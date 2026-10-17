# Freies skalares Feld auf einer festen kausalen Menge

## Geltungsbereich und Zustandsvertrag

Dieses Modul implementiert ein freies, reelles, masseloses Gaußfeld in einem
endlichen flachen 1+1-dimensionalen Minkowski-Diamanten. Die Geometrie wird
vorgegeben. Weder Quantisierung der Geometrie noch eine Entstehung von Materie,
Gravitation oder eine vierdimensionale Kontinuumsaussage werden untersucht.

Wir setzen hbar=c=1 und u=(t-x)/sqrt(2), v=(t+x)/sqrt(2). Der äußere Diamant
ist [-L,L]^2 mit L=1 und Volumen 4L². N Punkte werden unabhängig nach dem
Volumenmaß du dv gezogen: ein Poisson-Sprinkling **bedingt auf N**, kein
Poisson-zufälliges N. Die innere Region hat |u|,|v|<l, l/L=1/2.
Die Ordnung lautet C[i,j]=1 genau wenn u_i<u_j und v_i<v_j.

Mit der ersten Matrixposition als Empfangspunkt setzen wir

    G_R = C.T/2,  G_A = G_R.T,
    Delta = G_R-G_A,  H = i Delta,  W = Pos(H).

Die Transposition gegenüber manchen Literaturkonventionen ist beabsichtigt.
Der positive Spektralteil liefert den Sorkin-Johnston-Zustand [1]. Im Modul
werden ungewichtete Kernelmatrizen verwendet. Integraloperatoren mit Gewicht
V/N haben andere Eigenwerte: dann müssen auch beide Cutoffs entsprechend
skaliert werden. Die Normierung anderer Astrolabium-Module darf nicht ungeprüft
übernommen werden.

Die Observablen sind reelle verschmierte Felder phi(f) mit
[phi(f),phi(g)]=i f.T Delta g. Exakte gemeinsame Nullrichtungen werden als
Relationen quotientiert. Der Zustand ist durch Mittelwert null und
<phi_i phi_j>=W_ij festgelegt; höhere Momente folgen aus Wick-Kontraktionen.
W ist hermitesch, positiv semidefinit und erfüllt W-W.T=H. **W ist keine auf
Spur eins normierte Dichtematrix.** Endlich viele Feldorte erlauben keine
endlichdimensionale Hilbertraumdarstellung nichttrivialer exakter CCR.

Lineare Messgrößen phi(f) haben gaußsche Ergebnisverteilungen mit Varianz
f.T Re(W) f. Retardierte Antwort auf eine klassische Quelle ist durch G_R
vorgegeben. Messinstrumente, Rückwirkung, Wechselwirkungen, eine zusätzliche
Hamilton-Dynamik und zeitabhängige Geometrie gehören nicht zu diesem Vertrag.

## Randbedingungen

G_R ist der masselose retardierte 1+1-Kernel, auf den kausal konvexen äußeren
Diamanten beschränkt; keine periodischen oder reflektierenden Ränder werden
hinzugefügt. Die SJ-Zustandswahl hängt vom gesamten äußeren Diamanten ab.
Sie ist nicht automatisch das unendliche Minkowski-Vakuum. Auch eine allgemeine
Hadamard-Eigenschaft wird nicht beansprucht; hierfür bestehen bekannte Grenzen
[4]. Die feste äußere Region und der innere Ausschnitt sind Teil des Modells.

## Nullmoden und Entropie

Für eine Region A werden zunächst W_A und H_A eingeschränkt. Die Formel [2]

    W_A v = lambda H_A v,   S_A = sum lambda log|lambda|

wird nur auf einem geeigneten nichtentarteten Quotienten verwendet. H_A ist
indefinit; ein verallgemeinerter hermitescher Löser mit positiv definiter
zweiter Matrix wäre unzulässig. Der Kern verwendet deshalb einen allgemeinen
Eigenwertlöser und prüft Residuen, Realität und lambda/(1-lambda)-Paarung.

Numerische Nulltoleranz: 50*n*eps*max(1,max|eig(H_A)|). Für Nullbasis Z wird
||W_A Z||_F/max(1,||W_A||_F) geprüft. Über 1e-9 folgt KERNEL_MISMATCH und
**keine endliche Entropiezahl**. Das Gegenbeispiel W=[1], H=[0] muss scheitern:
eine Pseudoinverse, die hier null liefert, beseitigt das algebraische Problem
nicht. Eine gemeinsame Nullrichtung mit WZ=0 kann dagegen quotientiert werden.

Die physikalische UV-Regularisierung ist eine gesonderte Modellentscheidung.
Nach [3] werden global Eigenmoden mit |eig(H)| <= kappa*sqrt(N)/(4*pi)
verworfen und W,H gemeinsam projiziert. Erst danach wird auf A eingeschränkt
und nochmals mit kappa*sqrt(N_A)/(4*pi) projiziert. Beide Vorzeichen werden
zusammen behalten. kappa=1 ist primär; 0.75 und 1.25 prüfen die Empfindlichkeit.

Diese Projektion **ändert die Feldalgebra**. Insbesondere braucht der projizierte
Kommutator die ursprüngliche lokale kausale Stütze nicht mehr zu besitzen.
Die relative Änderung wird mitprotokolliert. Eine fehlende physikalisch
behaltene Mode ergibt EMPTY_PHYSICAL_ALGEBRA, keinen Null-Entropie-Erfolg.
Numerische Rundungen nahe lambda=0,1 (1e-8) werden gezählt. Größere Verletzungen
führen zu NUMERICAL_FAILURE. Entropien sind in nats angegeben.

## Zwei getrennte Referenzen

1. Zwei gekoppelte harmonische Oszillatoren mit K=[[1+g,-g],[-g,1+g]].
   Q=K^(-1/2)/2 und P=K^(1/2)/2 definieren einen reinen Grundzustand. Bei g=0
   ist die Teilentropie null; bei g=1 ist sie unabhängig mit Decimal auf
   70 Stellen berechenbar: nu=sqrt(2+sqrt(3)+1/sqrt(3))/4 und
   S=(nu+1/2)ln(nu+1/2)-(nu-1/2)ln(nu-1/2)
   =0.09439246594441708441433031523006307995540757161965704414646431290484782.
2. Im Diamanten wird die bekannte logarithmische Referenz geprüft [3]. Die
   erwartete Steigung ist 1/3 gegen ln(sqrt(N_A)), also 1/6 gegen ln(N_A).
   Der Interzept hängt von Zustands- und Regularisierungskonventionen ab.
   Der Vertrag legt vor dem Zielversuch 64 neue Ordnungen, Größen, Seeds,
   Hauptfit, Bootstrap, Toleranz und Sensitivitätsprüfung fest.

Ein vorheriger Pilot ist im Vertrag ausdrücklich als explorativ ausgewiesen.
Die neue Studie prüft endliche numerische Übereinstimmung, keinen mathematischen
Kontinuumsbeweis. Die Gleichheit von Teilentropien wird nicht für beliebige
mengen-theoretische Raumzeitkomplemente vorausgesetzt.

## Anschluss und Grenzen

W ist deterministisch aus C berechnet. Im ungekürzten masselosen Modell lässt
sich die Ordnung sogar aus W-W.T zurückgewinnen. Das Modul liefert keine neue
Information gegenüber der vollständigen Ordnung. Möglich ist ein Nutzen
regionaler Feldmerkmale gegenüber **verdichteten** bisherigen Merkmalen.
Globale SJ-Entropie null und das positive H-Spektrum allein belegen ihn nicht;
auch kausale Umkehr kann gleiche Entropien liefern.

Kontrollierte Ordnungsstörungen, echte Krümmungsfamilien, allgemeine Regionen,
Randvariation und Zusatznutzen bei gleichem Rechenbudget brauchen jeweils einen
Folgevertrag. Positions-Jitter in flacher Raumzeit ist keine Krümmung. Ein
späterer Vergleich muss ganze Geometrien als unabhängige Testeinheiten behandeln,
gleiche Regionsmarkierungen und Extraktionskosten zulassen und fehlende gemeinsame
Unterstützung melden. Es wird kein industrieller Mehrwert aus einem Referenzfit
abgeleitet.

## Quellen

[1] S. Johnston (2009), Feynman Propagator for a Free Scalar Field on a Causal Set.
https://arxiv.org/abs/0909.0944

[2] R. D. Sorkin (2012), Expressing entropy globally in terms of (4D) field-correlations.
https://arxiv.org/abs/1205.2953

[3] R. D. Sorkin, Y. K. Yazdi (2018), Entanglement Entropy in Causal Set Theory,
insbesondere Abschnitt 3. https://arxiv.org/abs/1611.10281

[4] C. J. Fewster, R. Verch (2012), On a Recent Construction of “Vacuum-like”
Quantum Field States in Curved Spacetime. https://arxiv.org/abs/1206.1562
