# CST-DUST · Geometrische Auslese am N11-Paar

**19. November 2026 · Etappe 5A · Arbeitsfassung v0.1.** Beim Wechsel des Anfangsdichtezentrums von 1/8 auf 1/4 ist die unbedingte Antwort des vollständig ausgelesenen Ordnungsregisters exakt null. In einem getrennten Versuch reagiert dasselbe Register auf die Breite der Anfangsuhr. Der physikalische Status bleibt **HOLD**. Die orthogonale Speicherung der Ordnung und die Mitführung der kollektiven Eingangskoordinaten sind zusätzliche Instrumentannahmen.

## Geometrie und Präparation

Im markierten Inneren I = {4,5,6} der Elfereigniskette C0 liegen drei vergleichbare Paare. In C1 entfallen (4,5) und (5,6), während (4,6) erhalten bleibt. Der äussere Kragen und seine Inzidenzen sind gleich. Die Zahl der Paare bleibt unter Umnummerierung des markierten Inneren erhalten. Der Test fragt nach einer Ordnungseigenschaft der Geschichte. Eine räumliche Volumenmessung oder eine Zeitreihe gehört zu einer anderen Fragestellung.

Aus PR 294 stammen die beiden normierten Eingangspakete auf dem kollektiven Raum mit Mass dμ = (δ₀ + dr auf (0,1))/2 × dt/3 auf dem Uhrintervall [−3/2,3/2]. Der Dichteindikator hat Halbbreite 1/32. Die beiden Uhrfenster haben Zentren t₀ ± 1/16, Halbbreite 1/32 und gleiche positive Amplitude. Die Zukunftsdichte bleibt 1/8. Die normierte skalare Eingangsform ψ und die beiden unitären Karten Vc kommen aus dem bedingten Drei-Moden-Vertrag. Beide Historien tragen denselben Amplitudenkoeffizienten 1/2. Der Anfangskragen ist fest, die Kontrolle der Ordnungen ist identisch vorbereitet und trägt keine anfängliche Korrelation mit der Wahl des Dichtepakets.

## Messoperator und Entkopplung

Für jeden Kern z wirkt die erfolgreiche Karte als direkte Summe zweier Zweige. Ihre Komponente für die markierte Ordnung c ist

    (Mzc Ψ)(r,t) = Wzc(r,t) Vc Ψ(r,t) / 2 .

Die zwei Komponenten landen in orthogonalen Registerzuständen. Im primären Experiment wird über die gesamte kollektive Ausgangsmode und alle skalaren Ergebnisse summiert. Dadurch ist Ezc = Mzc† Mzc die Multiplikation mit |Wzc|²/4. Da jedes W ein Mittel von Phasen über ein normiertes Mass ist, gilt |W| ≤ 1. Der zusätzliche Fehlschlageffekt I − Ez0 − Ez1 ist positiv, und die drei Effekte summieren sich zu I. Entsprechend ergibt der Fehlschlag zusammen mit den beiden Registerwahrscheinlichkeiten für jedes normierte Eingangspaket eins. Auch ein gemischter Anfangszustand ist im gleichen Hilfsraum zulässig.

Im gekoppelten Kern gehört die gesamte integrierte Staubwirkung zur jeweiligen Ordnung. Im Kontrollkern wird in beiden Zweigen die Staub-/Uhrwirkung der Kette C0 **vor der Integration** eingesetzt. Gravitationsphase exp(iFc), Skalartransfer Vc, Integrationsbereich, Mass, Gewichte und Auslese werden beibehalten. Im Code ist daher Wref,c = exp(i(Fc−F0)) W0, mit F0=10 und F1=18. Nur die Unterschiede des Staubtransfers zwischen den beiden Ordnungen werden entfernt. Die gemeinsame Abhängigkeit des Referenztransfers von der Uhr bleibt erhalten.

## Warum der Dichtekontrast verschwindet

Für die vier vergangenen Knoten hängen alle im Staubkoeffizienten auftretenden Vorgänger wiederum nur vom gemeinsamen Vergangenheitskragen ab. Aus den Ordnungsrelationen und den Schichtkoeffizienten folgt mit u = T₃/Δ und Δ² = 2/(19β) für beide Zweige

    B(t) = (8u² + 94u + 307)/19 ,
    Wzc(r,t) = exp(−ir B(t)/2) vzc(t) .

Bei affinen Uhren ist u = −2 und B = 151/19. Im gesamten variablen Uhrfenster ist |Wzc(r,t)|² = |vzc(t)|² punktweise. Somit hängt pzc = ∫ |f(r,t)|² |vzc(t)|² dμ / 4 nur von der Uhrmarginale ab. Beide Dichtepräparationen haben dieselbe Uhrmarginale. Dies beweist δ₁ = δ₀ = δ₁−δ₀ = 0 für das Ereignis mit einem Paar. Dasselbe Argument gilt für drei Paare und den Fehlschlag. Es benötigt keine numerische Toleranz. Der Satz setzt die diagonale Mitführung von (r,t) im gewählten Instrument voraus. Der Ausgangskragen der ursprünglichen Wirkung liefert dafür bisher keine eindeutige physikalische Vorschrift.

Die konstante normierte Mode 1 des kollektiven Raums liefert dagegen pzc,const = |∫ f Wzc dμ|² / 4. Der orthogonale Rest hat Gewicht pzc − pzc,const. Die Rechnung prüft diesen Rest zusätzlich als direkt integrierte quadratische Norm, einschliesslich des Gebiets ausserhalb des Paketträgers. Der konditionierte Anteil im angenommenen Teilraum wäre nochmals eine andere Grösse. Alle im Ergebnisbericht ausgewiesenen Modengewichte beziehen sich auf sämtliche Versuche.

## Vergleich mit der vorhandenen kohärenten Auslese

Die normierten Skalarausgänge ψ₀ und ψ₁ erfüllen exakt 0 < |s|⁴ < 1, s = ⟨ψ₀,ψ₁⟩. Aus ihren rationalen komplexen Präzisionsmatrizen Ωc ergibt sich

    |s|⁴ = 64 det(Re Ω₀) det(Re Ω₁) / |det(conj(Ω₀) + Ω₁)|²
         = 213027365739430936576000000 / 48302375511159976015329778787094473 .

Ein perfekter binärer Effekt E auf diesem Skalarausgang müsste für normierte Einzelzweige Eψ₁ = ψ₁ und Eψ₀ = 0 erfüllen. Die Selbstadjungiertheit ergäbe s = 0. Der Vergleich schliesst die perfekte, immer entscheidende Identifikation durch die skalaren Zustände aus. Auslesen mit Fehler oder unentschiedenem Ausgang bleiben möglich.

Mit Ac = ∫ f Wc dμ / 2 reproduziert die unabhängige Rekombination |A₀|² + |A₁|² + 2 Re(A₀* A₁ s) die archivierten skalaren Annahmeraten. Der Interferenzterm ist bei beiden Präparationen numerisch von null verschieden. Das explizite Ordnungsregister beschreibt also eine zusätzliche Messung. Seine Vollständigkeit gilt auf dem deklarierten positiven Hilfsraum. Die Wirkung und ihre Constraints müssen einen solchen Record und dessen Skalarprodukt noch physikalisch begründen.

## Zweiter Eingriff und Geltungsbereich

Nach Abschluss des primären Tests wurde separat ein Test auf Empfindlichkeit gegenüber der Uhrbreite festgelegt. Bei identischer Dichtepräparation (Zentrum 1/8) wird ein normiertes Uhrfenster um t₀ mit der ursprünglichen Zweifensterpräparation verglichen. Beide mittleren Uhrzeiten stimmen überein, ihre Varianzen unterscheiden sich um exakt 1/256. Das Ergebnis bezieht sich auf den Wechsel der gesamten Paketform. Da das Instrument über alle Randmoden summiert, ist es bei gleicher Uhrmarginale auch gegenüber der relativen Phase der beiden Fenster unempfindlich.

Für die geometrische Statistik X werden ein Paar mit +1, drei mit −1 und Fehlschlag mit 0 bewertet. Ihr Mittel ist die Differenz zweier unbedingter Registerwahrscheinlichkeiten. Beim Referenztransfer haben die beiden Ordnungen in jeder Präparation dieselbe Wahrscheinlichkeit, weshalb der Referenzmittelwert exakt null ist. Die Anteile von Erfolg und Fehlschlag dürfen sich bei einem Uhrwechsel auch dort ändern. Im gekoppelten Modell ergibt sich für die Verbreiterung ein numerischer Mittelwertunterschied von −0,00361409946. Die ursprünglichen Einzelwahrscheinlichkeiten sind vollständig in der Ergebnisdatei angegeben. Dieser Versuch ändert die Staubuhrpräparation bei fester Anfangsdichte. Eine physikalisch hergeleitete Auslese am gemeinsamen Geometrie-Staub-Skalar-Sektor bleibt offen.

## Offline nachrechnen

Benötigt werden Python 3, NumPy, SymPy und mpmath. Im entpackten Ordner ausführen. Die Rechnungen verwenden ausschliesslich die beiliegenden Eingaben.

    python3 -B verify.py
    python3 -B clock_sensitivity.py

Die Rechnungen vergleichen 32/6, 64/8 und 96/12 Gauss-Legendre-Knoten für jede der drei inneren Uhren bzw. pro äusserem Uhrfenster. Alle acht Dichtestrata der Innenknoten sind enthalten. Das äussere Dichtefenster wird sowohl direkt mit zwölf Knoten als auch mit seinem analytischen sinc-Faktor ausgewertet. Exakt sind die Geometriezählung, das gemeinsame Phasenpolynom, die Nullantwort und der rationale Gram-Befund. Die absoluten Wahrscheinlichkeiten und der Uhrkontrast sind Gleitkommaresultate mit Gittervergleich. Eine Einschliessung ihres gesamten numerischen Fehlers steht aus.

Die primäre Spezifikation steht in contract.json. Die getrennte Uhrkontrolle steht in clock_control.json. Die numerischen Ausgaben stehen in results.json und clock_sensitivity_results.json. Die in inputs/ übernommenen Dateien stammen bytegleich aus dem unten angegebenen Commit. Der Befund braucht weder externen Rechendienst noch neue Messdaten.

[Etappenprüfung und bisheriger Befund](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/17a3396d958bd79f77d03470b8255538ea0669c7/research/rax_cqg/dust_collapse/stage_reviews_4_7) · [Anfangspräparation und Quadratur](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/17a3396d958bd79f77d03470b8255538ea0669c7/research/rax_cqg/dust_collapse/initial_preparation_v0_1) · [Bedingter skalarer Randvertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/17a3396d958bd79f77d03470b8255538ea0669c7/research/rax_cqg/dust_collapse/physical_boundary_readout_v0_1)
