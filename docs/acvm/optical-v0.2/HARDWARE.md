# Aufbauentscheidung O02

Arbeitsprofil: Typ-II-ppKTP-Sagnac, nominell 405 nm → 810 nm + 810 nm,
Polarisationsanalyse in beiden Ausgängen. Zuerst wird die Ansteuerung mit einem
abgeschwächten klassischen 810-nm-Referenzstrahl abgenommen; erst danach folgt
die Einzelphotonenmessung. Komponenten sind ausgewählt, nicht beschafft oder
als vorhandener Besitz vorausgesetzt. Quellen/Versionsgrenzen: [SOURCES](SOURCES.md).

## Komponenten und mechanische Schnittstellen

| Funktion / Menge | Konkrete Auswahl | Abgleich vor Bestellung/Inbetriebnahme |
|---|---|---|
| Pumpe, 1 | TOPTICA TopMode 405 HP, frei gestrahlt, zugehöriger CHARM-Regler | Hersteller nennt 405 ±2 nm, <5 MHz, 100 mW. Reale Wellenlänge messen; Kristall darauf auslegen. Volle Ausgangsleistung ist kein gewählter Arbeitspunkt. |
| Pumpenpolarisation, je 1 | Newlight WPA03-H-405 und WPA03-Q-405 | Achsnullen, Retardanz und Pumpenanteile CW/CCW messen; zunächst manuelle SM1-Halter. |
| SPDC-Kristall, 1 | Raicol Typ-II-ppKTP, Auftragsspezifikation O02-K1 | Anfrageprofil: kollinear, tatsächliche Pumpenwellenlänge, degeneriert, Länge zunächst 10 mm, freie Apertur mindestens 1×2 mm, AR 405/810 in beiden Richtungen. **Polungsperiode, Solltemperatur, Toleranzen und Geometrie bedürfen Herstellerbestätigung.** Keine erfundene Katalognummer. |
| Kristalltemperatur, 1 | Zum angebotenen Raicol-Kristall passender Ofen mit geregeltem Temperaturfühler | Mechanische Schnittstelle, zulässige Temperatur und Stabilität gemeinsam mit O02-K1 festlegen; Host steuert diesen Ofen hier nicht. |
| Sagnac-PBS, 1 | Newlight PBS0025-405/810 | Tatsächliches Extinktionsverhältnis und Phasenwirkung bei beiden Wellenlängen und beiden Richtungen prüfen. Ein 810-nm-PBS allein ersetzt ihn nicht. |
| Sagnac-Wellenplatte, 1 | Newlight WPD03-H810-H405 | Halbwelleneffekt bei **beiden** Wellenlängen. H810-F405 ist ein anderes Bauteil und kein stiller Ersatz. |
| Schleifenspiegel, 2 | O02-M1: duale HR-Beschichtung 405/810 nm, 25.4 mm, tatsächlicher Einfallswinkel 45°, s und p | Lieferant/Angebot noch offen. R und s/p-Phasenverschiebung für beide Farben verlangen und messen. BB1-E02 (nur 400–750 nm garantiert) ist für diesen Platz nicht freigegeben. |
| Pumpentrennung | Thorlabs DMLP650, danach FELH0750, anschließend FBH810-10 je Analysearm | DMLP bei spezifiziertem Einfallswinkel; Filter nahe Normalinzidenz. Gemessene Pumpenunterdrückung und Gesamtverlust bestimmen, keine Addition nomineller OD ohne Streulichtprüfung. |
| Analyse QWP/HWP, je 2 | Newlight WPA03-Q-810 / WPA03-H-810, 1-Zoll-Fassungen | Nominal genau 810 nm; Retardanz am tatsächlichen Spektrum messen. Alternative WPQ05M-808/WPH05M-808 verlangt expliziten 808→810-Abgleich. |
| Analyse-PBS, 2 | Thorlabs CCM1-PBS252/M | 620–1000 nm, vier SM1-Ports. Kanalzuordnung T/R ↔ +/− kalibrieren. |
| Motorisierte Analyse, 4 | Thorlabs ELL14 mit ELL14K-USB/Versorgungsinterface bzw. kompatibler Busverkabelung | SM1-Rotation; Plattendicke, Haltering und freie Apertur mechanisch prüfen. Eigene Adresse und Seriennummer je Achse. |
| Langsamer relativer Phasensteller, optional 1 Satz | 2 × WPA03-Q-810 + 1 × WPA03-H-810, 3 × ELL14 | Q(45°)–H(θ)–Q(45°), kalibrierte Achsen. Relative H/V-Phase; keine globale optische Phase und kein schneller EOM. |
| Langsamer Intensitätssteller, optional 1 Satz | 1 × WPA03-H-810 + ELL14, 1 × CCM1-PBS252/M | Nur eine monotone Kennlinienhälfte verwenden; verworfener Port im Strahlfänger. Ändert Verluste/Postselektion eines Quantenexperiments. |
| Klassische Leistungsmessung | Vorhandener/geliehener **Legacy PM100D** mit S120C | Seriennummern, Kalibrierdatum, 810-nm-Korrektur, Nullpunkt, Bereich und Detektorsättigung prüfen. Dieser Adapter ist nicht als PM100D2/D3-Adapter getestet. |
| Photonendetektoren / Zeitmessung | 4 × SPCM-AQRH-14 und kalibrierter Mehrkanal-Time-Tagger als bereits dokumentierte Referenzkandidaten | Exakte TTL-/Abschlussvarianten und Rohzeitstempelpfad aus dem bestehenden Sagnac-Hardwareprofil übernehmen; keine neue Beschaffung vorausgesetzt. |
| Mechanik | Metrisches optisches Breadboard, 30-mm-Cage/SM1-Teile, einstellbare Spiegelhalter, schwarze Abdeckung, Strahlfänger | Schleifenlänge und Fokus erst aus Kristall/Modenabgleich bestimmen. Es gibt noch keine abgenommene CAD-Baugruppe. |

Die Beschaffungsentscheidung ist damit für Analyse und langsame Ansteuerung
konkret. **Die Quelle ist wegen O02-K1, Ofen und O02-M1 noch nicht vollständig
bestell- oder montagefreigegeben.** Ein Angebot mit Datenblatt kann diese drei
Schnittstellen schließen; kein Dokument ersetzt anschließend die Kalibrierung.

## Optischer und elektrischer Zusammenhang

Pumpe → Pumpen-HWP/QWP → dichroitische Einkopplung → Sagnac-PBS.
Die gegenläufigen Wege teilen ppKTP, duale HWP und Schleifenspiegel.
Die beiden 810-nm-Ausgänge werden von der Pumpe getrennt und jeweils durch
QWP → HWP → PBS auf die beiden Detektorkanäle analysiert.
Die gemeinsame Erfassung liefert A+, A−, B+, B−. Räumliche, spektrale und
zeitliche Ununterscheidbarkeit sowie relative Phase müssen gemessen werden.

Für die erste langsame Regelung: linear polarisierter klassischer 810-nm-Strahl
→ motorisierte HWP → PBS → S120C/PM100D → USB/VISA → Host-PI → USB/ELL14.
Diese gesonderte Abnahme verwendet keine angeschlossenen Einzelphotonendetektoren.
Ein zweiter Referenzmonitor oder zeitnah gemessene Referenzleistung dient der
Kennlinienkalibrierung; der implementierte Live-Regler regelt absolute Leistung
an seinem einen Messpunkt, keine photonische Koinzidenzrate.

ELL14 wird über das dafür vorgesehene Interface versorgt. Das interne
Kommunikationsinterface ist 3.3-V-TTL mit den Herstelleranforderungen an den Bus;
kein direkter ±RS-232-Anschluss und keine Versorgung aus einem GPIO. Software:
9600 Baud, 8N1, keine Flusskontrolle, expliziter Port, `in`, `ma`, `gs`, `gp`, `st`.
Encodermaßstab wird **nicht geraten**: Geräteinformation sichern und eine
bekannte Winkelbewegung unabhängig nachmessen. Die Einheitenbeschreibung in
Herstellerständen ist nicht hinreichend für einen ungeprüften Defaultwert.

Der C1-MCP4921-Ausgang bleibt ein separater elektrischer Versuchskanal.
0–2 V DC darf weder als LCVR-Wechselspannungsantrieb noch als Pockelszellen-
Hochspannung ausgegeben werden. Hier besteht kein Anschluss an einen solchen
Treiber. Hersteller LCC25/LCVR benötigen einen geeigneten AC-Antrieb; dafür
wurde bewusst kein unbestätigter Direktadapter freigegeben.

## Betriebsgrenzen

Alle Laserjustagen erfolgen im geeigneten Laserarbeitsplatz mit geschlossenem
Strahlweg/Strahlfängern und fachkundiger Laboraufsicht. Die 405-nm-Pumpe bleibt
bei der klassischen 810-nm-Steuerkanalabnahme aus. Leistung am PM100D-Messpunkt
zunächst höchstens 1 mW; der Profilgrenzwert ist keine optische Abschaltung.
Die hardwareseitige Strahlunterbrechung muss unabhängig vom Host möglich sein.
Ein Verbindungsfehler beendet die Software, garantiert aber keine Dunkelheit.
