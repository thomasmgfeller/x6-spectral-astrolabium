# Operator- und Gebietsfehler v0.15

29. Oktober 2026. Deterministische Entwicklungsdiagnose, kein Bestätigungslauf.

## Entscheidung

**Reine Vergrösserung des vergangenen Gebiets bei der bisherigen Operatorzelle wird verworfen.**
Für rho=3/pi, epsilon=1/16 und den bereits eingeführten Gauß-Zeugen L=2 bleibt der
relative Mittelwertfehler für jedes reelle H>=4 grösser als 41.70 %. Ohne
Gebietsabschneidung beträgt er 68.48927465 %. Das verletzt bereits die frühere
notwendige 10-%-RMS-Bedingung, denn RMS ist mindestens der Betrag des Bias.
Die Aussage bezieht sich auf den unveränderten Schichtkern und seine truncierte
Integralwirkung; andere Randkorrekturen oder neue Operatoren werden nicht ausgeschlossen.

**Kein verbesserter skalarer Kandidat ist freigegeben. Die ganze Operatorfamilie
wird nicht verworfen.** Der Fehler des ursprünglichen kompakten Detektormodells
ist weiterhin nicht vollständig in intrinsischen Operator- und ausserhalb des
Gebiets liegenden Historybeitrag aufgeteilt. G1 und METHOD_HOLD bleiben bestehen.

## 1. Unveränderte Grundlage und Daten

Quellfunktion, Masse m=1, Anfangszeit -1, Quellradius 1/2, Trägerwellenzahl 4,
Detektorball B((0,0,3/2),1/2), volle Zeitfenster [3/4,1] und [1,5/4] und die
vollständige v0.12-Kontinuumsreferenz bleiben unverändert. Einheit L0=c=1.
Die kompakte Antwort bleibt ein normierter komplexer Feldmittelwert.

Basis ist Commit 56207e7d36be4cddc897edf01a613c0be8837b86, der veröffentlichte
Stand von PR #146. PR #143-146 waren bei diesem Abruf offen; die Basis wird
nicht als zusammengeführter main-Stand ausgegeben. Alle eingelesenen Dateien
wurden gegen die Git-Blob-IDs des Commitbaums geprüft.

Verwendet werden die acht bekannten Wolken d0_r00 bis d0_r07 sowie genau die
vier bereits archivierten Erweiterungen d0_r00_outer bis d0_r03_outer.
Kein Neusprinkling, keine neuen Zufallsaufrufe und kein Zugriff auf E4-Ströme.
Es wird keine Erweiterung für die übrigen vier Wolken erfunden.

Der Gauß-Zeuge ist ein bereits vorhandener notwendiger Operator-Kontrolltest
aus v0.3/v0.6. Er ersetzt weder die kompakte Quelle noch deren Detektorantwort.
Die hier gewählten H-Werte und Historieschnitte sind Entwicklungsdiagnostik,
keine nachträglich als unabhängig deklarierte Bestätigungsstichprobe.

## 2. Exakte Trennung am Kontrolloperator

Für phi(t,x)=exp[-(t²+|x|²)/8] gilt phi(0)=1 und Box phi(0)=-1/2.
Mit q=epsilon*rho=ell^(-4), a=4 sqrt(q/6), P(z)=1-9z+8z²-4z³/3 und
D_H=I((-H,0),(0,0)) ist

    mu_H = a [-1 + q integral_DH phi(y) exp(-q V(y,0)) P(q V(y,0)) d4y].

Für N~Poisson(rho V) liefert die erzeugende Funktion exakt

    E[binom(N,k) epsilon^k (1-epsilon)^(N-k)]
      = (q V)^k exp(-q V)/k!.

Campbell-Mecke und kausale Konvexität ergeben damit die obige Mittelwertformel.
Bei festem q hängt sie nicht von rho ab. Eine Dichteerhöhung bei festem epsilon
ändert dagegen q und ist ein anderer Eingriff. Diese beiden Grenzübergänge
dürfen nicht vermischt werden.

Definiere b_op=mu_infinity-Box phi(0), b_domain(H)=mu_H-mu_infinity und
eta_C,H=B_C,H phi(0)-mu_H. Dann gilt für jede realisierte Wolke exakt

    B_C,H phi(0)-Box phi(0) = b_op + b_domain(H) + eta_C,H.

Die dritte Grösse ist eine Realisierungsabweichung. Die analytische
Zentrierung bezieht sich auf das ideale deklarierte Poisson-Gesetz; der
vorliegende Archivvergleich ist keine neue Populationsschätzung und zertifiziert
nicht zusätzlich den Abstand des endlichen PRNG/Samplers zu diesem Gesetz.

Operator- und Randbias werden signiert addiert. Ihre Beträge und die
Streuung werden nicht wie unabhängige Varianzen zusammengezählt.

## 3. Zahlen für die bisherige Zelle

rho=3/pi, epsilon=1/16, q=3/(16*pi), ell=2.02319223797.
Der Sollwert des Zeugen ist -0.5. Gerundete Anzeigen:

| Vergangenheitsdauer H | mu_H | mu_H-mu_infinity |
|---|---:|---:|
| 4 | -0.184842278993 | -0.027288652257 |
| 5 | -0.156801290301 | +0.000752336435 |
| 8 | -0.156932630580 | +0.000620996156 |
| 12 | -0.157551820460 | +0.000001806276 |
| 16 | -0.157553626044 | +0.000000000692 |
| Unbegrenzt | -0.157553626736 | 0 |

Bei H=4 verdeckt der Rand einen Teil des positiven Operatorbias. Die Erweiterung
4 auf 5 verbessert hier die lokale Genauigkeit des Mittelwerts nicht; sie nimmt
eine günstige Fehleraufhebung zurück. Kleinere Randfehler müssen deshalb nicht
zu einem kleineren Gesamtfehler führen.

Die drei bereits verwendeten Glättungen bei unverändertem rho liefern im
unbegrenzten Gebiet relative Biaswerte 50.90035273 % (epsilon=1),
61.39672466 % (1/4) und 68.48927465 % (1/16). Keine dieser drei
Konfigurationen qualifiziert einen neuen Kandidaten. Dies ist keine Aussage
über alle kontinuierlichen q oder andere Schichtkoeffizienten.

## 4. Beweis für alle reellen H>=4

Eine endliche H-Tabelle allein würde keine kontinuierliche Bereichsaussage
tragen. In Nullkoordinaten s=-t-r, v=-t+r gilt d4y=(pi/2)(v-s)² ds dv,
0<=s<=v<=H, qV=(pi*q/24)s²v². Daher

    d mu_H/dH = a q pi/2 integral_0^H (H-s)²
      exp[-(pi*q/24)s²H²-(H²+s²)/16] P((pi*q/24)s²H²) ds.

Für z>=0 folgt aus z^j exp(-z)<=j^j exp(-j)

    |exp(-z)P(z)| <= C = 1+9/e+32/e²+36/e³.
    |d mu_H/dH| <= a q pi C/6 * H³ exp(-H²/16) <= M,
    M = a q pi C/6 * 24^(3/2) exp(-3/2).

Auf [4,12] liegen 129 exakt rationale Stützstellen H_i=4+i/16. Jeder Punkt
hat Abstand höchstens 1/32 von einer Stützstelle. Validierte Quadratur liefert
für jede Stützstelle mu_i; damit ist

    |mu_H+1/2| >= lower(|mu_i+1/2|) - upper(M)/32.

Für H>=12 wird die im Vorgänger bewiesene monotone Gauß-Resthülle verwendet:

    |mu_H-mu_infinity| <= 56*pi*q*L²*exp[-H²/(4L²)], L=2.

Beide Teile ergeben zusammen eine relative Untergrenze grösser als
0.417028051007, ausgewiesen konservativ als 41.70 %. Die vollständigen
Stützstellen, Intervallwerte, Ableitungs- und Restgrenzen stehen in
results/DOMAIN_CERTIFICATE_128.json und _192.json.
Ein statistischer Test und eine neue Stichprobengrösse sind für diesen
deterministischen Ausschluss nicht erforderlich.

Die Erweiterungsfamilie kann als Omega_H=I((-H,0),(4,0)) verstanden werden.
Ihre Vergangenheit am Ursprung ist genau D_H; H ist keine symmetrische
Halbbreite. Für das symmetrische archivierte Omega5 ist dieselbe Vergangenheit
D_5 relevant. Eine spätere Zukunftsgrenze beeinflusst diese retardierte Probe
nicht. Beliebige Gebietsformen oder geänderte Randoperatoren sind nicht erfasst.

## 5. Gepaarte Archivprüfung: Rand und Realisierungsstreuung

Ist Omega kausal konvex und Omega subset Omega+, bleibt jedes Intervall
zwischen zwei inneren Endpunkten innerhalb von Omega. Beim Hinzufügen einer
Aussenschale ändern sich die inneren Intervallzahlen und inneren Gewichte
daher nicht. Der Operatorunterschied am Ursprung ist genau die gewichtete
Summe über zusätzliche kausale Schalenpunkte. Das wird an allen inneren
Endpunkten der vier Archivpaare mit exakten Kausalprädikaten bestätigt.

| Archiv-ID | B_5-B_4 | Abweichung vom analytischen Schalenmittel |
|---|---:|---:|
| d0_r00 | 0.061839389145 | 0.033798400453 |
| d0_r01 | 0.030783865141 | 0.002742876449 |
| d0_r02 | 0.142352987400 | 0.114311998708 |
| d0_r03 | 0.066019925917 | 0.037978937225 |

Das analytische Schalenmittel ist 0.028040988692. Eine einzelne gepaarte
Differenz ist also kein reiner deterministischer Randbias. Für jedes Paar
werden Operatorbias, Randbias und Realisierungsabweichung einzeln gespeichert
und ihre signierte Summe geprüft. Vier bekannte Paare ergeben keine
Populationsfreigabe und keine Aussage über die ganze fehlende Vergangenheit.

## 6. Ursprünglicher kompakter Detektor: Randvorschrift und Verstärkung

Die gespeicherten v0.12-KG-Historywerte und v0.10-Transferintervalle werden
unverändert wiederverwendet. Für A=T h_KG wird jeweils die alte History
t<=s ausdrücklich nullgesetzt, s=-4,-3,-2,-3/2. Die exakte Differenz ist

    A_s-A = -sum_(t_j<=s) T_j h_KG,j.

Das ist eine kontrollierte Änderung der Historyvorschrift bei identischen
inneren Daten und Gewichten. Sie ist keine Gebietserweiterung und keine
Schätzung der ausserhalb von Omega4 fehlenden KG-History.

Für t<=-3 ist die maximale eingeschlossene Änderung über alle 16
Wolken-Fenster-Fälle kleiner als 0.000068961. Bei Schnitten -2 und -3/2
liegen die maximalen Betragsobergrenzen unter 0.00522410 bzw. 0.01017791.
Die tatsächliche Änderung ist in 8 bzw. 12 Fällen nachweislich grösser
als 0.001. Keine dieser vier diagnostischen Historyvorschriften erreicht
in einem der 16 Fälle den bestehenden Fehlerwert 0.001. Das qualifiziert
weder eine alternative History noch eine neue Genauigkeitsmarge.

Weiter wird der aktive Block K_AA aus den unveränderten Intervallzahlen
aufgebaut. Für die normierten Operatordefekte
r_i=U_i-sum_j K_ij U_j sowie r_p=U(p)-sum_j K_pj U_j gilt exakt

    E_O = -mean_detector(r_p) - Q_A (I-K_AA)^(-1) r_A.

Die Matrix ist kausal strikt dreieckig, daher existiert die endliche Inverse.
Der rückwärts berechnete Adjungiertenvektor z_A=Q_A(I-K_AA)^(-1) liefert

    |E_O| <= |mean_detector(r_p)| + sum_i |z_i| * max_i |r_i|.

Seine Normobergrenzen liegen in den 16 Fällen zwischen etwa 0.162815 und
0.444694. Der entsprechende Historygain ist überall kleiner als 0.817824.
Die berechneten Historytransfers überlappen zusätzlich die archivierten
unabhängigen Transfers. Diese endlichen Schranken kontrollieren beliebige
Störrichtungen auf diesen Geometrien. Sie beweisen weder ensembleweite
Stabilität noch Stabilität bei wachsender Dichte und liefern keinen
vollständigen neuen Wert des kompakten Operatorrestes r_A.

## 7. Was für die vollständige Attribution noch fehlt

Die exakte algebraische Grenze lässt sich benennen. Bei gleichem innerem
Historywert und einer festgelegten Erweiterung mit äusseren Zuständen v_E gilt

    Delta A = [Q_E + Q_A (I-K_AA)^(-1) K_AE] v_E.

Damit ist ein fehlender Aussengebietsbeitrag sowohl direkt als auch über
die innere Dynamik zu transportieren. Eine reine direkte Randsumme reicht
für den Detektor im Allgemeinen nicht. Die Formel wird zusätzlich auf
einem unabhängigen rationalen Kausalgraphen geprüft, einschliesslich einer
Negativkontrolle für das Vorzeichen und für das Weglassen des Transportterms.

Für den ursprünglichen kompakten Detektor fehlen noch eingeschlossene
äussere KG-Historywerte bzw. eine deklarierte physikalische Aussenlösung,
die zugehörigen integrierten Q_E/K_AE-Koeffizienten und der Rest jenseits
einer endlichen Erweiterung. Weder der Gauß-Bias noch die vier
Gauß-Schalendifferenzen ersetzen diese Grössen. Im Allgemeinen gilt auch
E[(I-K)^(-1)] != (I-E[K])^(-1); ein mittlerer Operator ist kein bereits
gemittelter Detektorpropagator.

Die lokale KG-Supportschranke r<=|t+1|+1/2 schliesst bei rückwärtigen Zeiten
t<-9/4 nicht aus, dass History ausserhalb von Omega4 liegt. Exakte Werte
nur innerhalb des Gebiets beseitigen diesen offenen Beitrag deshalb nicht.
Die Quellauslöschung des lokalen H1-Adapters aus v0.14 bleibt ein weiterer
separater Mechanismus und wird durch diese Studie nicht behoben.

## 8. Validierung, Reproduktion und Grenzen

38 Kontrollen bestehen. 659 Intervalle gleicher exakter Zielgrössen überlappen
zwischen 128 und 192 Bit. 342 präzisionsabhängige Ober-/Untergrenzen werden
separat geführt: Ihre Endpunkte sind keine identischen exakten Zielgrössen
und müssen nicht überlappen. Ihre grösste diagnostische Abweichung beträgt
1.674e-10. Der kontinuierliche H-Ausschluss wird bei beiden Präzisionen
jeweils eigenständig nachgewiesen.

Neun unabhängige Gaußquadraturen in Zeit-/Radiuskoordinaten bestätigen die
Nullkoordinatenrechnung bis auf weniger als 4.42e-13. Das ist eine
diagnostische Gegenrechnung, keine eigene Restzertifizierung. 32 weitere
Intervallzählungen werden mit exakter Fraction-Arithmetik auf archivierten
Dyaden nachgerechnet. Falsches Randvorzeichen, fehlender Transportterm und
die verwechselte Vorzeichenwahl der Defekte werden kontrolliert.

Die geprüfte Umgebung nutzt Python 3.12.14, NumPy 2.3.5, python-flint 0.8.0
und einen C++17-Compiler ohne fast-math/FMA-Kontraktion für exakte Kausalität.
Der Daten- und Quellstand liegt im mitgelieferten source_snapshot. Die
Dateien dort bleiben unverändert. Aus dem Paketwurzelverzeichnis:

```bash
python -m pip install -r operator_gebiet_v0_15/requirements.txt
python operator_gebiet_v0_15/run.py --bits 128
python operator_gebiet_v0_15/run.py --bits 192
python operator_gebiet_v0_15/domain_certificate.py --bits 128
python operator_gebiet_v0_15/domain_certificate.py --bits 192
python operator_gebiet_v0_15/residual_gain.py --bits 128
python operator_gebiet_v0_15/residual_gain.py --bits 192
python operator_gebiet_v0_15/verify.py
```

FREEZE.json bindet Hauptrechnung und Eingaben vor ihrer Produktion.
DOMAIN_PLAN.json dokumentiert die nach der ersten Diagnose vorgenommene
deterministische Verfeinerung zur kontinuierlichen H-Aussage. Die zusätzlichen
Residual- und Verifikationsskripte werden im abschliessenden SHA256SUMS erfasst;
sie werden nicht rückwirkend als vorregistrierte Bestandteile ausgegeben.

## 9. Wissenschaftlich begründete Anschlussentscheidung

1. Keine weitere Kampagne, die bei q=3/(16*pi) ausschliesslich das vergangene
   Gebiet vergrössert und damit die bisherige Operatorgenauigkeit retten soll.
2. Keine Freigabe eines der drei bisherigen Glättungswerte als neuer Kandidat.
   Eine Änderung von q, Schichtkoeffizienten oder Operatorfamilie muss zuerst
   dieselben notwendigen Kontrollfelder und eine Stabilitätsprüfung bestehen.
3. Für eine vollständige Fehlerzuordnung des alten Detektors ist die oben
   festgelegte äussere Forcierung samt Restgrenze nötig. Das ist eine
   eigenständige noch offene Rechnung, keine durch die Kontrollfelder
   erledigte Aufgabe.
4. Ein frisches Ensemble bleibt hinter der v0.14-Methodenkontrolle gesperrt.
   Kein neues alpha, n, Powerziel oder nachträglich angepasstes Fehlerziel.

## Quellen

- Projektbasis: https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/56207e7d36be4cddc897edf01a613c0be8837b86/research/cspp
- v0.3 und v0.6: Gauß-Mittelwert, explizite Resthüllen und vorhandene Genauigkeitsbudgets.
- v0.7 und v0.10: exakte Kausalprädikate, endliche retardierte Systeme und volle Detektorkoeffizienten.
- v0.12: unveränderte kompakte Kontinuumsreferenz und KG-History; v0.14: offene Methodenvoraussetzungen.
- Aslanbeigi, Saravani, Sorkin (2014), Generalized Causal Set d'Alembertians, https://arxiv.org/abs/1403.1622.
  Kontext für nichtlokale Mittelwertoperatoren und die eigenständige Stabilitätsfrage;
  kein externer Beweis der hier berechneten Projektwerte.
- Belenchia, Benincasa, Dowker (2016), The continuum limit of a 4-dimensional causal set scalar d'Alembertian,
  https://arxiv.org/abs/1510.04656. Ein Grenzwert unter geeigneten Skalenbedingungen
  qualifiziert die hier festgehaltene grobe Skala nicht automatisch.
