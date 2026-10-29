# CSPP v0.24: Gate-Neubewertung nach der vollständigen globalen Bilanz

29. Oktober 2026. Schritt 3. Grundlage ist der nach PR #155 verifizierte
Main-Commit `0edb8e02aa3dbf5a1b827d7c9aa82385e056e817`.
Dies ist eine deterministische Entwicklungsentscheidung mit ergänzenden
mathematischen Folgerungen, keine neue Bestätigungsstudie.

## 1. Entscheidung und unveränderte Zielgrößen

METHOD und G1 bleiben HOLD. Es wird weder ein neuer skalarer Kandidat
freigegeben noch ein frisches Ensemble zugelassen. Die ganze
Operatorfamilie wird nicht verworfen. Die bereits widerlegte Strategie,
die feste Operatorzelle allein durch ein größeres vergangenes Gebiet
genau zu machen, wird nicht weiter als primärer Genauigkeitsweg verfolgt.

Die ursprünglichen Ziele bleiben auseinandergehalten:

- 0,001 ist die unveränderte absolute Referenzgröße des kompakten
  Detektors. Eine bedingte L1-Restschranke ist kein Beweis des früheren
  realisierungsweisen Genauigkeitsanspruchs.
- Die notwendige relative 10-%-RMS-Bedingung des Gauß-Kontrolloperators
  ist ein anderer Test mit anderer Normierung.
- Eine Kovarianzvorhersage verlangt gemeinsame zweite Momente. Für eine
  Bestätigungsstudie kommen die weiteren v0.14-Voraussetzungen hinzu.

Alle Quellen, Operatorparameter, Archive, Detektorfenster und statistischen
Regeln bleiben unverändert. Kein Alpha, keine Stichprobengröße, kein
Powerziel und kein Seed werden neu gewählt. Die vier Archivkonfigurationen
sind bekannte Entwicklungsdaten, keine unberührte Bestätigungsstichprobe.

## 2. Was v0.23 bewiesen hat und was hier neu ausgewertet wird

Mit B=Omega5, tau=-t-1 und der exakt vorgeschriebenen KG-History zerfällt
der äußere Wurzelbereich in D5 für 0<=tau<=5 und Dinf für tau>5.
Der Nullrand tau=5 wird nicht doppelt gezählt. v0.22 behandelt D5,
v0.23 Dinf und alle direkten, bekannten sowie unbekannten aktiven Pfade.
Für jedes feste Archiv gilt

    E(|A_infinity-A5| | B) <= B_finite + B_near + B_far.

Die Erwartung betrifft die ideale Poissonfortsetzung außerhalb des
vorgegebenen Archivs. Die nahe/ferne Teilung ist s<=sqrt(tau) bzw.
s>sqrt(tau), mit s=(p_t-y_t)^2-|p_space-y_space|^2, und wird unverändert
aus v0.23 übernommen.

Die neue Buchführung verwendet für jeden der 223 bekannten Endpunkte
und 256 Detektorzellen genau die dort gewählte Kerntrennstelle S. Die
gespeicherten nahen und fernen Grenzen werden mit denselben positiven
Detektormassen, |a_j| und dem bekannten Außenpfadfaktor transportiert.
Die beiden uniformen Fensterhüllen liefern den unbekannten Anteil.
Alle Summen reproduzieren die vollständige v0.23-Bilanz innerhalb der
ausgewiesenen arithmetischen Einschließung.

Für die acht Archiv-Fenster-Fälle ergibt sich gerundet:

- Gesamte obere Restschranke: 3,17 bis 3,75 mal 10^10.
- Anteil der nahen Hülle am ausgewiesenen Budget: mehr als 99,9999 %.
- Fernes Budget: ungefähr 7.804 bis 10.180.
- Endliches Budget: ungefähr 0,477 bis 0,549.

Die Größen sind **Obergrenzen des Beweisinstruments**, keine gemessenen
oder notwendigen physikalischen Fehler. Die nahe Hülle dominiert die
Schranke; daraus folgt keine entsprechende Aufteilung des tatsächlichen
Fehlers. Insbesondere können komplexe Feld- und Pfadbeiträge aufheben.

## 3. Sensitivität des bestehenden Zertifikats

Zur Planung werden zwei rein algebraische Gegenrechnungen gespeichert:

    verbleibende Summe bei entferntem nahen Zertifikat = B_finite+B_far,
    verbleibende Summe bei entferntem ganzen Tail-Zertifikat = B_finite.

Diese hypothetischen Entfernungen behaupten weder physikalisches
Verschwinden noch eine neue gültige Fehlerabschätzung. Sie beantworten
die begrenzte Frage, ob eine Verbesserung nur dieses einen Summanden
bei unveränderten übrigen Zertifikaten zur Freigabe ausreichen könnte.

Selbst die zweite verbleibende Summe liegt beim ungefähr 477- bis
549-Fachen von 0,001. Eine alleinige Schärfung der unendlichen Hülle
genügt deshalb nicht, solange die endliche v0.22-Majorante unverändert
weiterverwendet wird. Das ist keine untere Schranke des echten Fehlers
und keine Aussage über alle möglichen neuen Beweise oder Trennstellen.

Markov liefert für jeden Archiv-Fenster-Fall lediglich

    P(|A_infinity-A5|>0,001 | B)
       <= min(1, B_global/0,001) = 1.

Die rechnerische Verbesserung um etwa Faktor 6982 bis 9130 aus v0.23
erzeugt somit noch keine nichttriviale Fehlerwahrscheinlichkeit am Ziel.
Ein kleiner Rest erst jenseits eines sehr großen tau-Cutoffs ersetzt
weiterhin nicht das dazwischenliegende Gebiet.

## 4. Quantitative unbedingte L1-Folgerung für die KG-History-Diagnose

Die vier Archivwerte allein begründen keine Aussage über alle inneren
Konfigurationen. Die uniformen v0.23-Endpunkthüllen wurden jedoch für
**beliebige** endliche Archive hergeleitet. Diese uniformen Hüllen lassen
sich unter dem idealen Poisson-Gesetz mitteln. Dies ist eine zusätzliche
Rechnung, nicht eine Umdeutung der vier Archivwerte als Ensemble.

Die gemeinsame aktive Hülle beider Fenster ist für -1<t<5/4 die Kugel
um d=(0,0,3/2) mit Radius 7/4-t. Wegen rho=3/pi ist ihre Poissonmasse

    lambda_A = 4 Integral_(-1)^(5/4) (7/4-t)^3 dt
             = (11/4)^4-(1/2)^4 = 14625/256.

Aus der exakten Geometrie in v0.17 folgt lambda_E=29/512 für den Teil
außerhalb B und damit lambda_B=29221/512 innerhalb B. Für die **gesamte**
aktive Hülle wird dieselbe konservative Zeitgrenze für beide Fenster
verwendet. Es wird keine Poissonmasse doppelt addiert.

Setze gamma=beta*kappa, beta=1/[16(1+sqrt(2pi))] und
kappa=4976184375/4294967296. M ist die unveränderte globale Feldhülle
aus v0.19. Das vollständige endliche Außengebiet hat
rho|D5|=110567/128. Eine uniforme erste-Forcierungsgrenze ist daher

    F_finite = gamma M (110567/128).

Sie folgt aus Campbell-Mecke, |w(n)|<=kappa, |U|<=M und Vergrößerung
jedes kausalen Wurzelbereichs auf ganz D5. Sie ist konservativer als
die archivbezogene v0.22-Bilanz und ersetzt diese dort nicht.

Sei F_tail,W die uniforme erste-Endpunkt-Grenze aus v0.23. Für ein
beliebiges inneres Archiv mit N_B aktiven Punkten gilt nach demselben
Pfadbeweis

    E(|A_infinity-A5| | B)
      <= (F_finite+F_tail,W) (1+gamma)^N_B exp(gamma lambda_E).

Die Argumentation konditioniert zuerst auf das gesamte innere Archiv.
Die erste bedingte Kernhülle ist uniform in dessen festen Zählwerten;
die später eingefügten Mecke-Kettenpunkte liegen nicht im offenen
ersten Historyintervall. Es wird kein Erwartungswert eines korrelierten
Gewinn-Forcierungsprodukts auseinandergezogen.

Nun ist N_B~Poisson(lambda_B). Die positive Poissonreihe ergibt exakt

    E[(1+gamma)^N_B]=exp(gamma lambda_B).

Tonelli und der Turmsatz liefern damit

    E|A_infinity-A5|
      <= (F_finite+F_tail,W) exp(gamma lambda_A) < infinity.

Die numerischen oberen Grenzen sind nach oben gerundet
3,577614 mal 10^11 für W0 und 3,936052 mal 10^11 für W1.
Dies ist eine Integrabilitätskontrolle, keine Genauigkeitsqualifikation
und keine neue Mittelwert- oder Kovarianzvorhersage.

Auch A5 selbst ist in L1. Sei N_H die Zahl der inneren Historypunkte.
Punktweise gilt durch die endliche Pfadsumme

    |A5| <= gamma M N_H (1+gamma)^N_B.

N_H und N_B zählen disjunkte deterministische Raumzeitgebiete und sind
unter dem Poisson-Gesetz unabhängig. Aus E N_H<=rho|B|=1250 folgt

    E|A5| <= gamma M 1250 exp(gamma lambda_B) < infinity.

Zusammen folgt A_infinity in L1. Die fast sichere absolute Konvergenz
war bereits in v0.17 hergeleitet; hier wird ihre integrierbare
Transportkontrolle quantitativ ergänzt. Eine dichteuniforme Stabilität,
ein Pfadmaximum über alle Realisierungen oder eine Samplerqualifikation
folgt daraus nicht. Die ideale Poissonverteilung ist Teil der Annahmen.

## 5. Warum L1 weder Kovarianz noch Genauigkeit freigibt

Ein großes B mit E|X|<=B impliziert keine positive Fehleruntergrenze:
X=0 erfüllt dieselbe Ungleichung. Selbst ein endliches bekanntes L1-
Moment garantiert kein zweites Moment. Für jedes B>0 setze

    P(X=(B/3)2^n)=3*4^(-n), n=1,2,... .

Die Wahrscheinlichkeiten summieren sich zu 1. Es gilt

    E|X|=B,  E[X^2]=(B^2/3) Sum_(n>=1) 1 = infinity.

Die endlichen Teilsummen werden mit rationaler Arithmetik unabhängig
geprüft. Das Beispiel ist ein Gegenbeispiel zu einer unzulässigen
Schlussregel, keine Behauptung über die tatsächliche CSPP-Verteilung.

Auch bei endlichen Momenten bestimmt L1 keine Varianz: mit
P(X=+B/p)=P(X=-B/p)=p/2 und P(X=0)=1-p gilt E X=0, E|X|=B,
Var(X)=B^2/p. Die gepaarten Kanäle (X,X) und (X,-X) haben identische
Randverteilungen, aber entgegengesetzte Kreuzkovarianzen. Gemeinsame
Intervall- und Anfangsdatenkorrelationen bleiben deshalb erforderlich.

Für eine tatsächliche Attribution darf bei festem endlichem A5 und
Kontinuumswert c aus einer Restgrenze B höchstens geschlossen werden:

    max(0, |A5-c|-B) <= E(|A_infinity-c| | B) <= |A5-c|+B,
    |E(A_infinity|B)-c - (A5-c)| <= B.

Die zweite Aussage benutzt Jensen und die erste die Dreiecksungleichung.
Sie definiert noch keinen intrinsischen Operatorbias. Insbesondere
wird hier kein Omega4-Wert aus v0.15 als Omega5-Wert eingesetzt.
Ein mittlerer Operator ist weiterhin kein gemittelter inverser Propagator.

## 6. Kandidatenidentität und die sechs bestehenden Methodenkriterien

v0.14 verlangt vor einer Bestätigungsplanung:
Kontrollreproduktion, totale Ensembleabbildung, gemeinsame Originalmomente,
viertes Moment oder geeignete Tail-Kontrolle, ensembleweiten numerischen
Fehlernachweis und Übereinstimmung mit dem deklarierten Samplinggesetz.

Die alten Kandidaten bleiben unverändert:

| Kriterium | Lokaler H1-Adapter | Nichtlokaler PU-H1-Adapter |
|---|---|---|
| Kontrollreproduktion | PASS | PASS |
| Totale Ensembleabbildung | PASS | Auf einer Menge positiver Wahrscheinlichkeit undefiniert |
| Gemeinsame Originalmomente | Nicht ausgewertet | Nicht ausgewertet |
| Viertes Moment / geeignete Tail-Kontrolle | PASS | Nicht zertifiziert |
| Ensembleweiter numerischer Fehler | Nicht zertifiziert | Nicht zertifiziert |
| Samplinggesetz stimmt überein | Nicht zertifiziert | Nicht zertifiziert |

Beide bleiben REJECTED_FOR_CONFIRMATORY_RUN. Das ist eine fehlende
Zulassung wegen offener Methodenvoraussetzungen, kein neuer statistischer
Verwerfungstest auf frischen Daten.

Die exakt vorgeschriebene volle KG-History der v0.16-v0.24-Diagnose ist
eine andere Eingabeabbildung. Ihre fast sichere Definition und ihr neues
L1-Zertifikat reparieren weder den Quellverlust des lokalen H1-Adapters
noch die fehlende Definition des nichtlokalen Projektors. Umgekehrt
wird die H1-Nullwahrscheinlichkeit exp(-21/16) nicht als Nullanteil der
vollständigen KG-History ausgegeben. Die KG-Diagnose ist kein stiller
Ersatzkandidat für das eingefrorene v0.14-Experiment.

## 7. Der unabhängige notwendige Operatorzeuge bleibt entscheidend

Die v0.15-Einschließungen bleiben unverändert. Für die feste Zelle
rho=3/pi, epsilon=1/16, q=3/(16pi) und den schon verwendeten Gauß-Zeugen
phi=exp[-(t^2+|x|^2)/8] gilt für **jedes reelle H>=4** ein relativer
Mittelwertfehler größer als 0,417028051007. Für unbegrenzte Vergangenheit
beträgt er ungefähr 0,6848927465. Bereits diese notwendige Bedingung
verfehlt die frühere relative 10-%-RMS-Schranke, denn RMS>=|Bias|.

Hier werden die 129 einschließenden Stützstellen je Präzision, die
Ableitungshülle und der analytische Rest ab H=12 erneut zur durchgehenden
Untergrenze zusammengesetzt. Die ursprünglichen Gaußquadraturen werden
nicht als neue v0.24-Rechnung ausgegeben.

Die Aussage gilt für die festgelegte Zelle, den gegebenen Schichtkern,
die betrachtete Familie von Vergangenheitsdiamanten und diesen notwendigen
Kontrollzeugen. Sie ist kein Anteil des kompakten Detektorfehlers, keine
universelle Aussage über alle Randkorrekturen und keine Widerlegung
sämtlicher skalarer Operatoren. Auch die drei bereits geprüften
Glättungen liefern keinen neuen qualifizierten Kandidaten.

## 8. Begründete Anschlussentscheidung

1. Die ursprüngliche Fehlerattribution bleibt ein sinnvoller, optionaler
   Diagnosezweig. Ein weiterer Tail-Gewinn allein rettet jedoch weder
   die bestehende positive Gesamtmajorante noch die bereits durch den
   Kontrollzeugen ausgeschlossene reine Gebietsreparatur der festen Zelle.
2. Primär wird eine deterministische Entwicklung und notwendige Prüfung
   eines geänderten skalaren Kandidaten vorgesehen. Änderungen an q oder
   Schichtkoeffizienten wären ausdrücklich neue Kandidaten; sie müssen
   bei unveränderter physikalischer Quelle und denselben Kontrollfeldern
   Operatorbias, Retardierung, Stabilität und komplette Fehlerbilanz
   bestehen. v0.24 wählt keinen solchen Parameter und behauptet keinen PASS.
3. Erst nach erfüllter Methodenkontrolle werden statistisches Design,
   Rechenbudget und öffentliche Vorregistrierung festgelegt. Erst danach
   kommen frische Daten. Die Fluktuations- und makroskopischen Entscheidungen
   bleiben getrennt. Der Nachweis von L1-Existenz überspringt keinen Schritt.

Der genaue nächste Arbeitsauftrag steht in NEXT_WORK_PACKAGE.md. Schritt 3
ist als Neubewertung abgeschlossen; die Entwicklung eines neuen Kandidaten
und eine Bestätigungsstudie werden nicht als ausgeführt ausgegeben.

## 9. Prüfung und Herkunft

34 Eingaben sind gegen SHA256 und die Git-Blobs des Main-Commits geprüft.
Die fünf unveränderten v0.23-Ergebnisdateien stimmen mit dessen Replay
überein. Die neue Rechnung läuft bei 128 und 192 Bit. 16 globale
Zerlegungen, 24 Einträge der alten Methodenkriterien und 258 Punkte der
übernommenen kontinuierlichen H-Abdeckung werden geprüft.

Zwölf unabhängige positive Poissonsummen bis 1023 mit explizitem
Chernoff-Rest prüfen die erzeugende Funktion. 60 rationale Identitäten
kontrollieren die Momentengegenbeispiele; zwei weitere Kontrollen
prüfen das Vorzeichen der gemeinsamen Kovarianz. Sechs unzulässige
Schlussfolgerungen werden ausdrücklich ausgeschlossen.

Die acht übernommenen endlichen Majoranten hängen geringfügig von der
Präzision ihrer früheren numerischen Einschließung ab. Ihr größter neuer
relativer Vergleichsunterschied ist ungefähr 2,41e-15. Eine rein
arithmetische Konsistenzgrenze 1e-12 wird dafür getrennt von 1e-20 für
die übrigen Vergleichsgrößen verwendet. Dies ändert kein physikalisches
Genauigkeitsziel und ist keine statistische Unsicherheit.

Der isolierte Replay verlangt Byteidentität aller vier neuen numerischen
Ergebnisdateien und unveränderte Eingaben. Die Kontrollen sind keine
unabhängige wissenschaftliche Begutachtung oder Beweisassistent-Verifikation.

## 10. Primärquellen und begrenzte Verwendung

- Projekt: Main nach PR #155, https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/0edb8e02aa3dbf5a1b827d7c9aa82385e056e817/research/cspp .
  Die projektspezifischen Zahlen stammen aus den unveränderten Dateien
  in evidence/ und den hier dokumentierten eigenen Rechnungen.
- Last/Penrose, Lectures on the Poisson Process (2017), Gleichung 1.8
  und Theorem 4.4: https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf .
  Verwendet werden die Poisson-erzeugende Funktion und die Mecke-Identität;
  die konkrete Modellhülle und deren Zahlen sind eigene Anwendungen.
- Aslanbeigi/Saravani/Sorkin (2014), Generalized Causal Set d'Alembertians:
  https://arxiv.org/abs/1403.1622 . Kontext für getrennte Untersuchung von
  Mittelwertoperator, Infrarotbedingungen und Stabilität; keine Quelle
  unserer konkreten Genauigkeits- oder Gate-Entscheidung.
- Belenchia/Benincasa/Dowker (2016), The continuum limit of a 4-dimensional
  causal set scalar d'Alembertian: https://arxiv.org/abs/1510.04656 .
  Ein Kontinuumsgrenzwert unter Skalenbedingungen ist kein Genauigkeitsbeweis
  für die hier festgehaltene grobe Skala. Quellen geprüft am 29.10.2026.
