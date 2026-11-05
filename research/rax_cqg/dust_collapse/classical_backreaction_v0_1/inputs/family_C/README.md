# Zwei-Massen-Test auf vorhandenen Amplituden der Randfamilie C

Ziel ist die Frage, ob die Materiemasse nur eine gemeinsame Phase oder Norm liefert. Dazu skalieren wir die drei gleichen Quellmassen bei gleicher Diskretisierungslänge ell und gleichem hbar gemeinsam. In Einheiten c=1 gilt eta=m_Quelle ell/hbar. Die publizierte Hauptwahl eta=1 entspricht der Gesamtmasse M0=3 hbar/ell. M=4M0 entspricht eta=4. M=2M0 ist ein vor der neuen Auswertung benannter Zwischenwert. Der Plan wurde lokal vor den neuen Ergebnissen fixiert. Die alten Werte für eta=1 waren bekannt. Dies war keine externe Präregistrierung.

## Zwei getrennte Fragen

1. Test auf einen einzigen komplexen Faktor in den Zweigen derselben endlichen Summe, mit festem geometrischem Träger, unveränderten Auslesekanälen und unveränderten Grundgewichten.
2. Ablesetest auf vorgeschriebenen klassischen Staubverläufen. Dieser Kontrollversuch wird nur zum Prüfen der Messmethode verwendet. Die dazu synthetisch erzeugten Zeitfenster zählen nicht als dynamisch erzeugte Verlaufsklassen.

## Reproduktion

Python 3.12.14, python-flint 0.9.0, NumPy 2.3.5 und SciPy 1.17.0 unter Linux. Die Eingangstabellen befinden sich in inputs/. Die Skripte benötigen keinen Netzzugriff. Ohne -O starten.

    sha256sum -c SHA256SUMS
    python3 -m venv .venv
    .venv/bin/python -m pip install python-flint==0.9.0 numpy==2.3.5 scipy==1.17.0
    .venv/bin/python amplitudes.py > replay-amplitudes.json
    cmp replay-amplitudes.json amplitudes.json
    .venv/bin/python audit.py > replay-fixed.json
    cmp replay-fixed.json fixed_audit.json
    OPENBLAS_NUM_THREADS=1 .venv/bin/python readout.py > replay-readout.json
    cmp replay-readout.json readout.json
    sha256sum -c SHA256SUMS

Die letzte Kontrolle schliesst die neu erzeugte Tabelle readout_counts.csv ein. Sie enthält die Kern- und Flügelzählungen zu jeder Messzeit jeder Realisierung. Andere Softwareversionen können die Anzeige der Ballradien oder den Pseudozufallsstrom verändern. Das JSON-Zertifikat speichert die vorab festgelegten Regeln, die Ergebnisse und die zugrunde gelegten Rechenkonventionen in getrennten Dateien.

## Konstruktion und Nullkontrollen

Die drei Quellen erreichen die beiden frühen Stellen wie in PR 210. Untersucht wird die unveränderte Familie C mit 840 unmarkierten Orbitgeometrien. Für jede Markierung wählen die drei Quellen ihre Routen mit unveränderten positiven Übergangsgewichten. Zwischen Quelle und Ziel durchläuft jede vier Abschnitte. Die offene Intervallzählung ist auf den normalen Abschnitten eins und auf der ausgewählten doppelten Kante zwei. Daher hat eine Route in Einheiten ell die Dauer L0=4(24/pi)^(1/4) oder L0+delta mit delta=(48/pi)^(1/4)−(24/pi)^(1/4). Nach Ausklammern der gemeinsamen Phase exp(−3i eta L0) bleibt exp(−i eta delta h), h=0,1,2,3 je nach Zahl der Quellen auf der doppelten Kante. Die drei Einzelmassen und der konservierte Gesamtfluss werden um denselben Faktor skaliert. Dies folgt aus der Linearität des Flusses in den Quellmassen. Die Randpräparation der Gravitationsimpulse wird im vorhandenen endlichen Modell nicht als massenabhängige Lösung einer Zwangsgleichung bestimmt.

Im früheren reinen Differenzzeit-Modell ist die Wegdauer exakt T_f−T_i=4 für jede Route. Deshalb gilt bei normiertem Transport W(M)=exp(−4iM) in den dortigen Einheiten. Bei M=3 und 12 liefert dies den einzigen Faktor exp(−36i) für alle Historien. Die aktuelle Kontrolle blind setzt analog die zusätzliche Wegdauer delta auf null. Nach Entfernung der gemeinsamen Phase sind die Zweigvektoren dann exakt gleich. Die Kontrolle g_zero schaltet dagegen nur die BDG-Phase aus, so dass die Wegdauer weiterhin wirkt.

Für die Gegenrechnung benutzt audit.py die archivierte nach aussen gerundete Festkommaarithmetik. pi wird über die Machin-Identität mit eingeschlossenen Arkustangensresten gewonnen, die Materiephase über eine Taylorentwicklung bei eta=1 mit garantiertem Rest und ganzzahlige Potenzen. Die gravitative fünfte Einheitswurzel wird aus Radikalen berechnet. Die zehn Komponenten beider binären Zweige werden direkt akkumuliert. Der Nachweis der Nichtproportionalität erfolgt alternativ durch die Summe aller 45 quadrierten Zweierminoren. Die Resultate aus 160-Bit-Ballarithmetik müssen innerhalb der unabhängigen rationalen Einschliessungen liegen, mit einem separaten exakten Gleichheitstest in der blinden Kontrolle. Ein positives Ergebnis betrifft die konkrete Amplitudendarstellung. Eine Änderung der normierten Zweiggewichte zeigt hier zusätzlich eine Änderung der geometrischen Klassenstatistik des Modells.

## Ablesekontrolle und Grenze der Vorhersage

Y=sqrt(V) in Einheiten von sqrt(V_i), die Zeit in Einheiten sqrt(V_i/(6 pi G M0)). Auf der vorgeschriebenen marginal gebundenen Lösung gilt Y=1−sqrt(m) tau, m=M/M0. Innerhalb eines symmetrischen Fensters der Breite h ist der mittlere Wert von V gleich V(tau)+m h²/12. Aus den Zählungen unabhängiger Bereiche (innere Fensterhälfte sowie beide äusseren Flügel zusammen) folgt Vhat=(7 N_Kern−N_Flügel)/(3 rho h). Sein Erwartungswert ist bei quadratischem V exakt der zentrale Wert. Die Mittelwertkorrektur garantiert keine fehlerfreie einzelne Messung. Die Punktzahl pro Fenster wird ohne Festlegung einer Gesamtpunktzahl Poisson-gezogen; es handelt sich um exakt integrierte Zählstatistiken bei vorgegebenen Staubmarken, nicht um die Rekonstruktion der Uhr aus unmarkierten Ordnungen.

Eine einzelne Realisierung besteht nur, wenn alle drei Volumenschätzer positiv und beide Abweichungen der Y-Inkremente seit tau=0 höchstens 0,05 sind. In diesem Vergleich wird auch die Messunsicherheit der frühen Volumenablesung mitgetragen. Pro Zelle stehen 256 Realisierungen. Das gemeinsame 95%-Konfidenzniveau für sechs Trefferraten folgt aus zweiseitigen Clopper-Pearson-Intervallen mit Bonferroni-Korrektur. Zwei Stufen derselben physikalischen Region, identische Uhrzeiten und eine neue Zwischenmasse sind nur auf der klassischen Kontrollseite verfügbar.

In den endlichen C-Tabellen bleiben ein binärer Endwert und fünf Signaturen der Ankunftswege. Weder ein kalibrierter räumlicher Volumenwert noch die gemeinsame Verteilung eines mehrzeitigen Volumenverlaufs ist darin kodiert. Ein marginales Endergebnis kann verschiedene Zwischenverläufe besitzen. Auch auf dem geometrischen Referenzmass aus PR 213 sind keine brauchbaren Orbitgewichte für die Auswertung vorhanden. Es gibt daher keinen aus dieser Historiensumme bestimmten Steigungsquotienten, keine Schätzung der Schrittresiduen von Gleichung (20) und keine Prüfung von Gleichung (21) für eine CST-Vorhersage. Der klassische Pass eines Zählers ersetzt diese Angaben nicht.

## Quellen

Die Originalarchive und Mitglieder für alle kopierten Eingaben sind mit SHA-256 in inputs/provenance.json verzeichnet. Der Code und die endlichen Modellkonventionen stammen aus dem öffentlichen [Projekt](https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/main/research/rax_cqg/dust_collapse). Zum Massenparameter siehe CST_Staubtransport_Wegphasen, Seite 3; zur Einzelroute Kausalordnung_Rekursive_Wegteilung, Seite 4; zur Normierung und Signatur Kausalordnung_Endzustaende_Pruefbericht, Seite 2. Geometriemasse und Vergleichswerte stammen aus [PR 211](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/211) und [PR 212](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/212), die geometrische Sperre aus [PR 213](https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/213). Die Referenzbewegung und die Fehlerbedingung sind im [Quantendynamik-Bericht](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/research/rax_cqg/dust_collapse/reports/CST_Staubkollaps_Quantendynamik_Herleitung.pdf) hergeleitet.
