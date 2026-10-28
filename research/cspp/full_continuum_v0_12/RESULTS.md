# Ergebnisse: vollständige skalare Kontinuumsreferenz v0.12

**Referenz abgeschlossen; METHOD_HOLD und G1 HOLD bleiben bestehen.**

Die neue Referenz integriert den ganzen bisherigen Detektorball und die ganzen beiden Zeitfenster. Das Zeitintegral wird exakt als Differenz des Sine-Propagators an den Fenstergrenzen berechnet. Die räumliche Reduktion und alle Restgrenzen stehen in README.md. Der Code verwendet keine diskreten Kausalsetantworten zur Konstruktion der Referenz.

## 1. Kontinuumsantwort und Referenzfehler

Die folgende komplexe Antwort ist durch die bisherige Feldskala F0=A/e geteilt. Sie ist ein linearer Feldmittelwert, keine Intensität. Die Tabellenmitten sind auf 24 Nachkommastellen gerundet; der jeweils genannte gemeinsame Radius gilt separat für Real- und Imaginärteil und schließt diese Anzeigerundung ein.

| Zeitfenster | Realteil | Imaginärteil | Radius je Komponente |
|---|---:|---:|---:|
| [3/4, 1] | -0.020732687086922060979949 | +0.001678303092685356509942 | 4.9e-22 |
| [1, 5/4] | -0.005907886606641349247619 | +0.006495610877105028863749 | 3.2e-22 |

Unskaliert, einschließlich der Unsicherheit der L2-Normierung A:

| Zeitfenster | Realteil | Imaginärteil | Radius je Komponente |
|---|---:|---:|---:|
| [3/4, 1] | -0.069588630157516998691090 | +0.005633173004514621729117 | 1.7e-21 |
| [1, 5/4] | -0.019829640719433989552519 | +0.021802319259385140507689 | 1.1e-21 |

Die folgenden nach oben gerundeten Schranken beziehen sich auf die normierte Antwort. Ein komplexer Fehlerbetrag wird zur sicheren Einschließung auf beide Komponenten übertragen.

| Referenzbeitrag | Fenster 1 | Fenster 2 |
|---|---:|---:|
| Quadratur plus Intervallarithmetik (Komponentenradius) | 4.84E-22 | 3.11E-22 |
| Abgeschnittener Quellenrand (Betrag) | 1.05E-26 | 1.31E-26 |
| Rest der Bessel-Reihe (Betrag) | 2.37E-30 | 1.86E-28 |
| Zusätzliche zeitliche Quadratur | 0 | 0 |
| Ausgelassener Detektorrand | 0 | 0 |

Die Referenztoleranz 1e-12 ist in beiden Fenstern erfüllt. Quellenrand und Reihenrest werden analytisch begrenzt; sie werden nicht aus der Differenz zweier Auflösungen geschätzt.

## 2. Getrennte Bilanz der diskreten Rechnung

Für jede vorhandene Wolke, jedes Fenster und beide Adapter wird dieselbe signierte Identität geprüft:

\[a_{\rm num}-\mathcal C=E_A+E_O+E_I+E_S.\]

- EA: ideale Adapterhistory gegenüber der exakten KG-History, bis zum Detektor übertragen.
- EO: diskreter Operator und endliches Gebiet bei exakter KG-History gegenüber der vollen Kontinuumsantwort.
- EI: Anfangsdatenintegration/-rundung plus Detektorkubatur; beide Teilbeiträge bleiben in den Rohdaten einzeln verfügbar.
- ES: Koeffizientenrundung, endlicher Dreieckssolve und abschließende Gleitkommasummation.

Die bis zum Detektor fortgepflanzte Zertifikatsunsicherheit der KG-Kontrollhistory beträgt höchstens 1.7e-23. Sie ist in den Beitragsintervallen eingeschlossen und erklärt deren Größenordnung nicht.

Die Kontrollhistory ist kein neuer Adapter und wird nicht in die eigentliche Modellrechnung eingesetzt. Operator und Gebiet werden gemeinsam bilanziert; ihre weitere Trennung ist noch offen. Die idealen PU-Koeffizienten und ihre numerischen Repräsentanten dürfen nicht gleichgesetzt werden.

Die nächste Tabelle gibt je Fenster und Methode die größte Betragsobergrenze unter den acht Wolken an (nach oben gerundet). Das sind konservative Obergrenzen einzelner Beiträge, keine positiven Fehlernachweise und keine unabhängigen Varianzen.

| Fenster | Adapter | EA | EO | EI | ES |
|---|---|---:|---:|---:|---:|
| 1 | lokal H1 | 1.40E-2 | 3.06E-2 | 3.23E-3 | 1.79E-18 |
| 1 | nichtlokal PU H1 | 1.77E-1 | 3.06E-2 | 1.68E-1 | 1.17E-18 |
| 2 | lokal H1 | 1.89E-2 | 1.61E-2 | 2.32E-3 | 6.22E-18 |
| 2 | nichtlokal PU H1 | 1.98E-1 | 1.61E-2 | 1.89E-1 | 2.35E-18 |

Bei der nichtlokalen Projektion sind EA und der Anfangsdatenanteil von EI korreliert. Ihre breiten Intervalle lassen derzeit keine eindeutige Attribution zu. Sie belegen weder einen so großen tatsächlichen Projektionsfehler noch eine Verschlechterung gegenüber dem lokalen Adapter. Der direkte Gesamtfehler der ausdrücklich festgelegten numerischen Realisierung bleibt trotzdem eng eingeschlossen.

## 3. Woher kommt die Abweichung?

Ein Beitrag gilt nur dann als dominant, wenn seine Betragsuntergrenze die Summe aller anderen Betragsobergrenzen übersteigt. In der folgenden Tabelle bezeichnet O diesen Nachweis für EO, ein Fragezeichen eine unentschiedene Zuordnung. Die EO-Intervalle sind für beide Adapter gleich. Gesamtfehlerbeträge sind gerundete Anzeigen der engen Intervalle.

| Wolke | Fenster | Betrag EO: untere/obere Grenze | Gesamt lokal | Ursache lokal | Gesamt PU |
|---|---:|---:|---:|:---:|---:|
| d0_r00 | 1 | [2.07E-2, 2.19E-2] | 0.021712 | O | 0.022551 |
| d0_r00 | 2 | [8.78E-3, 1.10E-2] | 0.011465 | O | 0.009601 |
| d0_r01 | 1 | [2.48E-2, 2.78E-2] | 0.020801 | O | 0.017713 |
| d0_r01 | 2 | [1.26E-2, 1.55E-2] | 0.008780 | O | 0.005877 |
| d0_r02 | 1 | [2.13E-2, 2.66E-2] | 0.019380 | O | 0.019457 |
| d0_r02 | 2 | [1.08E-2, 1.48E-2] | 0.004680 | ? | 0.007397 |
| d0_r03 | 1 | [2.34E-2, 2.59E-2] | 0.020761 | O | 0.024116 |
| d0_r03 | 2 | [1.14E-2, 1.47E-2] | 0.010331 | O | 0.011800 |
| d0_r04 | 1 | [2.22E-2, 2.66E-2] | 0.020801 | O | 0.019351 |
| d0_r04 | 2 | [9.59E-3, 1.41E-2] | 0.008780 | O | 0.006894 |
| d0_r05 | 1 | [1.84E-2, 2.16E-2] | 0.021532 | O | 0.021659 |
| d0_r05 | 2 | [6.71E-3, 8.61E-3] | 0.009734 | O | 0.008980 |
| d0_r06 | 1 | [2.64E-2, 3.06E-2] | 0.020801 | O | 0.017517 |
| d0_r06 | 2 | [1.05E-2, 1.61E-2] | 0.008780 | O | 0.010319 |
| d0_r07 | 1 | [2.03E-2, 2.28E-2] | 0.013599 | O | 0.018006 |
| d0_r07 | 2 | [9.55E-3, 1.20E-2] | 0.005574 | ? | 0.001879 |

Bei der nichtlokalen PU-History bleibt die Ursache in allen 16 Fällen unentschieden. Die lokale Zuordnung ist in d0_r02/Fenster 2 und d0_r07/Fenster 2 unentschieden.

**Belastbarer Befund:** Mit exakter Kontinuumshistory liegt der Operator-/Gebietsbeitrag in allen 16 Wolken-Fenster-Fällen nachweislich über 1e-3. Beim lokalen H1-Adapter dominiert er in 14/16 Fällen nach dem strengen Kriterium. Die maximale Lösungsfehlerschranke liegt unter 6.3e-18. Eine genauere Lösung des gleichen endlichen Systems würde diese Abweichung daher nicht beseitigen.

Alle 32 festgelegten numerischen Realisierungen überschreiten die Gesamtvergleichstoleranz 1e-3. Dies ist eine Aussage über diese deklarierten numerischen Realisierungen, nicht über jede mögliche genaue Realisierung der noch breit eingeschlossenen idealen PU-Projektion.

Für die drei Wolken d0_r01, d0_r04 und d0_r06 löscht der lokale H1-Adapter die Quelle weiterhin exakt aus. Seine numerische Antwort ist null; Integrations- und Lösungsfehler sind dort exakt null. Die Gesamtfehlerbeträge sind dann etwa 0.0208005052 und 0.0087804376. Die nichtlokale Konstruktion ändert diesen geometrischen Befund nicht rückwirkend.

## 4. Prüfstatus und verbleibende Arbeit

- 15 analytische Kontrollen bestanden; 886 Intervalle derselben Zielgrößen bei 128 und 192 Bit überlappen.
- 64 signierte Fehlerbilanzen geprüft, verteilt auf zwei Präzisionsläufe.
- 624 zertifizierte KG-Historywerte je Präzision; alle bisherigen Koordinaten- und Kausalzählwerte unverändert.
- Keine zusätzlichen Zufallswolken, Kausalsetknoten, angepassten Quellen oder geänderten Detektorfenster.
- Eine unabhängige Fourier-Diagnose bestätigt die Zahlen bis ungefähr 2.3e-13. Deren Fourier-Abschneidung ist nicht zertifiziert; sie ist nur eine zusätzliche Kontrolle.

Abgeschlossen ist die volle skalare Kontinuumsreferenz für diese kompakte massive Quelle und diese zwei Fenster. Offen bleiben eine ausreichend enge nichtlokale Projektionsintegration, die getrennte Untersuchung von Operator und Gebietsrand, die Genauigkeitsqualifikation der Adapterhistory sowie G1 und die weitergehende physikalische Interpretation. Die acht Archivwolken sind Entwicklungsfälle, keine unabhängige Bestätigungsstichprobe.

`continuum.py` enthält die unabhängige Referenz, `run.py` die Bilanz, `verify.py` die Ausgabekontrolle. `PROTOCOL.json` und `FREEZE.json` halten Parameter, Datenidentität und lokalen Methodenstand fest. Die vollständigen signierten Intervalle stehen in den beiden komprimierten Benchmarkdateien; `CHECKS.json` enthält die maschinenlesbaren Entscheidungen. Die Reproduktionsbefehle und die vollständige Herleitung stehen in README.md.
