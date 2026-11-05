"""Build the report from the frozen JSON contracts; optional reportlab dependency."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
P=Path(__file__).resolve().parent
for n,f in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DI','DejaVuSans.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='DI',boldItalic='DB')
ink=colors.HexColor('#152e43');blue=colors.HexColor('#096b86');gray=colors.HexColor('#eaf0f4');amber=colors.HexColor('#fff0d1')
styles={
 'body':ParagraphStyle('body',fontName='D',fontSize=10,leading=14,textColor=ink,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.8,leading=12,textColor=ink,spaceAfter=5),
 'h1':ParagraphStyle('h1',fontName='DB',fontSize=23,leading=28,textColor=ink,spaceAfter=17),
 'h2':ParagraphStyle('h2',fontName='DB',fontSize=15,leading=20,textColor=blue,spaceBefore=2,spaceAfter=12),
 'h3':ParagraphStyle('h3',fontName='DB',fontSize=10.5,leading=14,textColor=blue,spaceBefore=8,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName='D',fontSize=9,leading=12.4,textColor=ink),
 'head':ParagraphStyle('head',fontName='DB',fontSize=9,leading=12.4,textColor=colors.white)}
story=[]
def p(text,style='body'):return Paragraph(text,styles[style])
def add(text,style='body'):story.append(p(text,style))
def title(n,text):add(f'{n:02d} / {text}','h2')
def para(text):add(escape(text))
def block(title_,text):story.append(KeepTogether([p(escape(title_),'h3'),p(escape(text))]))
def table(head,rows,widths):
 t=Table([[p(escape(str(x)),'head') for x in head]]+[[p(escape(str(x)),'cell') for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),blue),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,gray]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.5,blue)]));story.append(t);story.append(Spacer(1,10))
def box(text):
 t=Table([[p(text)]],colWidths=[491]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),amber),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#d4ad58')),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10)]));story.append(t);story.append(Spacer(1,9))
def nextpage():story.append(PageBreak())
R=json.loads((P/'Referenzvertrag.json').read_text())
F=json.loads((P/'Eigenfrontend_Pruefmatrix.json').read_text())
D=json.loads((P/'Rechenergebnisse.json').read_text())
S=json.loads((P/'Quellen.json').read_text())
add('X6 · PHOTONIK / LABORQUALIFIKATION','small')
add('Referenzdetektion elektrisch qualifizieren','h1')
add('Eigenfrontend getrennt charakterisieren','h2')
para('Prüf- und Auswertungspaket v0.1 · 5. November 2026')
box('<b>Ergebnis dieses Arbeitsschritts:</b> Herstelleranschlüsse rechnerisch abgeglichen, Prüfbedingungen festgelegt und Offline-Auswertung geprüft. <b>Hardware: NOT_RUN. BOM-Freeze: HOLD.</b> Es liegen keine realen Oszillogramme, Zähltests oder Detektormessungen vor.')
table(['Prüfpfad','Gegenstand','Freigabeumfang'],[
 ('A · Referenz','4 × SPCM-AQRH-14-FC → Kabel → Time Tagger Ultra','15 Prüfungen R00–R14. Elektrik und Archivpfad; keine optische Effizienzfreigabe.'),
 ('B · Eigenfrontend','Kaskode → ADCMP607 → CML → Empfängeradapter','10 Prüfungen F00–F09. Zunächst ausschließlich Niedervolt-Elektrik.'),
 ('C · Detektorbenchmark','Vollständiger APD-/Quench-Detektor nach F09','7 Metriken B01–B07; Referenz und DUT getrennt bewerten.')],[80,189,222])
block('Wichtigster Anschlussbefund','Die Referenzkette ist unter den spezifizierten Pegel- und Lastbedingungen plausibel kompatibel. Das Eigenfrontend benötigt vor einem Ultra-Anschluss einen gesondert qualifizierten Leitungsadapter. Sein RAW-Logikausgang ist kein nachgewiesener 50-Ohm-Treiber.')
block('Was die Software belegt','47 synthetische Regressionstests bestanden. Dazu kommen unabhängige numerische Vergleichswerte für die Poisson-Grenze. Die Programme steuern keine Hardware, extrahieren keine Oszillogramme und erstellen kein Kalibrierzertifikat.')
para('Lesefolge: Anschlussvertrag S. 2 → Referenztests S. 3–5 → Zeitbudget S. 6 → Eigenfrontend S. 7–9 → Detektormetriken S. 10–13 → Freigabe und Dateien S. 14 → Quellen S. 15.')
add('Projektbasis: main @ '+R['baseline_commit'],'small')
nextpage();title(2,'Anschlussvertrag der Referenz')
table(['Position / Signal','Vorgabe','Vor Anschluss nachweisen'],[
 ('DET-0..3','SPCM-AQRH-14-FC; A+, A−, B+, B−','Seriennummer, 1X-Pulsvariante und gültige Lieferrevision [P2,S1,S2].'),
 ('CAB-0..3','Je ein 50-Ohm-Koax BNC → SMA; nominal 1 m','Konkreter Artikel, Länge, Dämpfung, Verzögerung und Schirmung sind OPEN.'),
 ('TDC-01','Time Tagger Ultra; Standardmodus, SDK 1..4','Lizenz, reale Kanäle, Flanke, Firmware/SDK und Konfigurationsdump [S3].'),
 ('Detektorausgang','Nominal 2,2 V ±0,4 V, 10 ns; positiver Impuls','Gesamte Signalhülle einschließlich Ringing am realen Empfänger [S2].'),
 ('Empfänger','Interne 50 Ohm; empfohlener Bereich −3..+3 V','Kein zweiter 50-Ohm-Abschluss. Absolutgrenze ist kein Betriebsziel [S3].'),
 ('Schwelle','Startwert 1,0 V; Hersteller TTL High ≥1,5 V, Low ≤0,8 V','Daraus 0,5 / 0,2 V nominale Mindestreserven; Plateauscan und Unsicherheit [S2].'),
 ('Pulsbreite','Ultra mindestens 0,5 ns','Auf realer Triggerhöhe messen; Flanken und Mehrfachüberquerungen prüfen [S3].'),
 ('PSU/PWR-01','5 V, am Verbraucher 4,75..5,25 V; separate abgesicherte Zweige','4 × max. 1,2 A =4,8 A; 6 A mit 25 % Planreserve, noch keine PSU-Auswahl [S2].')],[100,181,210])
block('Rechenreserve und Verkabelung','Bei 5,00 V, 50 mV negativer Netzteilabweichung und 50 mV dynamischer Reserve bleiben 150 mV Leitungsabfall: RSchleife ≤0,125 Ohm bei 1,2 A. Das ist ein Planungsszenario; reale Einschalt- und Lastspitzen messen. Steckerpolarität und Steckermaß am konkreten Liefergerät bestätigen.')
box('Scope zunächst <b>als einzige 50-Ohm-Last</b> anschließen und danach durch den Ultra ersetzen. Ein T-Stück mit zwei 50-Ohm-Eingängen ergibt 25 Ohm und verfälscht Pegel und Timing. Ein 4,4-V-SPCM oder ein anderer Tagger ist kein automatischer Ersatz.')
para('Das SPCM-Gate besitzt eine interne Last und verlangt einen geeigneten Treiber; kein direkter Raspberry-GPIO-Anschluss. Ohne separat geprüfte Gate-Schaltung den dokumentierten Hersteller-Standardzustand verwenden. [S2]')
nextpage();title(3,'Referenzprüfung: Identität und Pegel')
for r in R['tests'][:5]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion'])+' <font color="#667988">['+escape(r['origin'])+']</font>','small')
box('Für jede Prüfung speichern: Rohdatei, Geräte-/Kalibrier-ID, UTC-Zeit, Schaltung und Last, tatsächliche Bedingungen, Unsicherheit, Entscheidung und Reviewer. Status ist zunächst überall <b>NOT_RUN</b>.')
nextpage();title(4,'Referenzprüfung: Zählen und Timing')
for r in R['tests'][5:10]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion'])+' ['+escape(r['origin'])+']','small')
para('0 Fehler in 1 000 000 unabhängigen Bernoulli-Versuchen ergeben nur eine bedingte einseitige 99-%-Obergrenze von 4,6052 × 10⁻⁶ pro Versuch. Das beweist keine absolute Fehlerfreiheit. Periodische, korrelierte und sich in der Summe kompensierende Fehler brauchen eigene Stimulusmuster und Ereignis-IDs.')
nextpage();title(5,'Referenzprüfung: Archiv und Freigabe')
for r in R['tests'][10:]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion'])+' ['+escape(r['origin'])+']','small')
box('<b>Vorhandener Treiber ≠ vollständige Qualifikation.</b> Der veröffentlichte Treiber prüft bereits Testsignal, Divider, Triggerschwelle, FileWriter-Counts und Overflows. Modus-/Lizenznachweis, vollständige Filter-/Delayprüfung sowie der unabhängig validierte .ttbin-Roundtrip bleiben gesonderte Nachweise. [P3]')
nextpage();title(6,'Zeitbudget und Unsicherheiten')
table(['Größe','Grenze / Definition','Auswertung'],[
 ('Elektrischer Paarjitter S03a','≤200 ps Standardabweichung','Alle sechs Paare, kompletter Datensatz; Konfidenz-/Unsicherheitsobergrenze statt bloßem Punktwert.'),
 ('Restoffset S03b','|μij|+U ≤100 ps','Trainingsdaten bestimmen Offsets; unabhängige Validierung darf sie nicht neu schätzen.'),
 ('Zeitstempelschritt S03c','>0 und ≤100 ps','Raster getrennt von Präzision, Zeitbasisgenauigkeit und DNL erfassen.'),
 ('Drift S05a','|Δμij|+U ≤100 ps','30-s-Blöcke gegen eingefrorenen Referenzwert; gleiche Kalibrieranteile korreliert behandeln.'),
 ('Optische Paarantwort S04','FWHM ≤1000 ps','Erst mit Photonen gemessen; RMS und lange Tails zusätzlich, kein universeller Faktor 2,355.'),
 ('Primäres Fenster','Volle Breite 2000 ps','|tB−tA−δ| ≤1000 ps. Weder Jitterdaten beschneiden noch Fenster nach Ergebnis optimieren.')],[107,170,214])
block('Messmodell','Für den korrigierten Unterschied gilt Δtij=(tj−ti)−(δj−δi). Die Paarvarianz enthält Kanalrauschen, Verteiler-/Kabelanteile und Kovarianzen. Ein gemeinsamer Eingang kann korrelierte Beiträge aufheben. Eine kleine Paarstreuung ist deshalb kein Nachweis der absoluten Einzeldetektor-Zeitgenauigkeit.')
block('Unsicherheitsplan vor dem Lauf','Scope-/TDC-Kalibrierung, Generator-/Fan-out-Skew, Kabeltemperatur, Schwellenmessung und Amplitudenwanderung getrennt budgetieren. Für stationäre normalverteilte unabhängige Werte sind χ²-Grenzen für σ möglich; bei Tails/Abhängigkeit vorab begründetes Blockverfahren oder konservatives Modell verwenden. Für eine gemeinsame Aussage über sechs Paare/80 Zeitblöcke simultane Abdeckung planen; Einzelintervalle sind keine globale Garantie.')
block('Rechenpfad','Zeitmarken bleiben uint64-Pikosekunden bis nach der Subtraktion. Das verhindert Verlust kleiner Zeitdifferenzen bei großen absoluten Zählern. timing_groups meldet Mittelwert, Standardabweichung, Extrema und Fensteranteil, berechnet aber keine automatische Konfidenzgrenze.')
nextpage();title(7,'Eigenfrontend: klare elektrische Grenzen')
para('Der veröffentlichte Schaltplan ist ein erster Kaskoden-/Komparatorentwurf. APD-Hochspannung, Quench-Leistungspfad, Hold-off und vollständige Totzeitlogik fehlen. Der folgende Anschlussplan übernimmt den geprüften Projektstand, keine Fertigungsfreigabe. [P4]')
table(['Anschluss','Mess-/Betriebsvertrag'],[
 ('J301','Pin 1 +3,3 V, Pin 2 GND; Pilotstart mit 100-mA-Stromlimit. Keine Verpolschutzschaltung.'),
 ('J101','SENSE/GND, zunächst 5..25 mV positive Pulse tatsächlich am Knoten. Kein HV-Eingang; C101 isoliert nicht galvanisch, BAS70 ist kein HV-Schutz.'),
 ('J203','3,3-V-SPI und CMP_EN. VTH physisch messen, kein DAC-SPI-Readback. Keine SPI-Aktivität in Timingaufnahmen.'),
 ('J201 / J202','Q / QN; zwei 50-Ohm-Leitungen. Am Empfänger jede mit 49,9 Ohm nach 3V3_TERM terminieren, nicht nach GND.'),
 ('J302 → J403','Gemeinsame 3V3_CML/3V3_TERM und GND. Keine unabhängigen Netzteile parallelschalten.'),
 ('U401','SN65LVDS34D ohne interne Terminierung. Zwei belastende Empfängergruppen am kurzen Endpunkt; Leitung/Last real prüfen.'),
 ('J404','EVENT_3V3 und QUENCH_3V3 sind RAW-Logik. QUENCH ist keine APD-Leistungsstufe; Validität muss separat gesichert werden.')],[103,388])
box('<b>Kein direkter Ultra-Anschluss:</b> CML-Abschluss und Gleichtaktlage passen nicht zum üblichen 50-Ohm-Eingang nach GND. Auch J404 ist nicht als 50-Ohm-Treiber belegt. 3,3 V / 50 Ohm =66 mA; der Empfänger-Datenblattpegel bei wenigen mA beweist diese Lastfähigkeit nicht. [S4,S5]')
block('Entwicklungsziel richtig einordnen','Wenige Pikosekunden Komparator-RJ unter Datenblattbedingungen belegen keinen 50-ps-Gesamtpfad. Empfängerlaufzeit, Skew, Time walk und Random Jitter sind unterschiedliche Größen. Der ältere 200-ps-Restfehler im Frontendentwurf ersetzt nicht das aktuelle 100-ps-Kriterium der Referenzkette.')
nextpage();title(8,'Frontend: Analogpfad und Schwelle')
for r in F['electrical'][:5]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Ergebnis / Kriterium:</b> '+escape(r['criterion']),'small')
para('Jeder Datensatz enthält Amplitude am Eingangsknoten, tatsächliche Flankensteilheit, Pulsbreite, Rate, Last, Temperatur, Versorgung, DAC-Code und gemessenes VTH. Nur dann lassen sich zwei Frontendversionen sinnvoll vergleichen.')
nextpage();title(9,'Frontend: Ausgang, Fehler und Übergabe')
for r in F['electrical'][5:]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Ergebnis / Kriterium:</b> '+escape(r['criterion']),'small')
box('F00–F08 können ein <b>elektrisches Frontend</b> charakterisieren. Erst F09 macht daraus einen Kandidaten für den <b>Detektorbenchmark</b>. Fehlende APD-/Quench-Hardware lässt sich nicht durch elektrische Ersatzpulse ersetzen.')
nextpage();title(10,'Benchmark: Effizienz und Dunkelrate')
for r in F['full_detector_only'][:2]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion']))
block('B01 · Berechnungsmodell für isolierte Poisson-Lichtpulse','Photonfluss Φ=P·λ/(h·c), mit h und c als exakten SI-Konstanten; 1 pW bei 810 nm entspricht etwa 4,0776 Millionen Photonen/s. Für mittlere Photonenzahl μ pro Puls gilt unter unabhängiger Hintergrundannahme: η=[ln(1−pdark)−ln(1−pclick)]/μ. Promptfenster, vollständige Recovery, Pulsstatistik und vernachlässigbare/begrenzte Afterpulse müssen belegt sein. Pulsed_efficiency liefert nur den Punktwert.')
block('B01 · Unsicherheit und Referenzebene','Kalibriertes Powermeter, Dämpfung, Splitter, Wellenlänge, Polarisation, Verbindung/Reproduzierbarkeit, Quellenmonitor und Zählstatistik gehören ins Budget; gemeinsame Kalibrierungen nicht unabhängig addieren. Der Verlust zwischen Moduleingang und APD gehört zur Systemeffizienz. Eine absolute APD-PDE erfordert dessen getrennte Bestimmung. [S6,S7]')
block('B02 · Statistik','Für n Counts in T Sekunden ist die einseitige Poisson-Obergrenze r99=χ²(2(n+1),0,99)/(2T). Bei n=0 und T=600 s sind es 0,0076753/s. Bei 60 000 Counts sind es 100,95385/s. Das Modell setzt geeignete Stationarität und Poisson-Zählung voraus; Clustering/Afterpulse können es verletzen.')
box('99 % gilt hier <b>je Kanal</b> gemäß bestehendem S10a. Wer gemeinsam 99 % für vier Kanäle fordert, braucht z.B. α=0,0025 je Kanal oder eine begründete simultane Methode. Diese zusätzliche Aussage wird nicht stillschweigend aus vier Einzeltests abgeleitet.')
nextpage();title(11,'Benchmark: Recovery und Afterpulsing')
for r in F['full_detector_only'][2:4]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion']))
block('B03 · Bedingte Doppelpulsantwort','Nur Versuche mit registriertem ersten Photonereignis zählen in den konditionierten Nenner. Vergleichspulse bei großem Abstand bestimmen p∞. Der Quotient p2(Δ)/p∞ braucht Unsicherheit beider Größen und eine Korrektur/Schranke für Dunkel- und Nachpulse im Promptfenster. Gemeinsame Konfidenzbänder über das Delay-Raster und Interpolation vorab definieren. Ohne hinreichende Auflösung bleibt t95 ein Intervall.')
block('B04 · Beobachtbare Größe','Für pobs=P(mindestens ein Sekundärereignis im Fenster) und gematchten Hintergrund pb lautet ein einfaches unabhängiges Modell pexcess=(pobs−pb)/(1−pb). Das ist eine fensterabhängige Überschusswahrscheinlichkeit, keine intrinsische Trap-Freisetzungswahrscheinlichkeit. Die mittlere Anzahl sekundärer Counts ist eine andere Größe. Negative Schätzwerte nicht auf null kappen, sondern Intervall und Modellprüfung berichten.')
block('B04 · Verdeckte Bereiche','Die anfängliche 50-ns-Grenze ist keine Behauptung über die reale Totzeit. Wenn Recovery oder Blanking länger ist, fehlt ein größerer Teil der frühen Antwort. Bei unvollständigem Nachlauf bleibt ein unbekannter Rest außerhalb des Fensters. Fensterränder, Wiederholrate, Triggerselektion und Re-Armierung sind Bestandteil des Ergebnisses.')
box('Herstellerunterlagen nennen für die 1X-Familie unterschiedliche Totzeitwerte (Produktseite 24 ns; Manual-Tabelle 22 ns). Lieferrevision und optische Recovery am konkreten Exemplar entscheiden. Die 10-ns-Ausgangspulsbreite ersetzt keine Totzeitmessung. [S1,S2]')
nextpage();title(12,'Benchmark: Jitter und Linearität')
for r in F['full_detector_only'][4:6]:
 block(r['id']+' · '+r['name'],r['procedure'])
 add('<b>Entscheidung:</b> '+escape(r['criterion']))
block('B05 · Deconvolution nur mit begründetem Modell','Für eine Zeitdifferenz gilt σΔ²=σD²+σR²−2·Cov(D,R), ergänzt um die separat definierte Instrumentantwort. Nur wenn die Beiträge unabhängig sind und nichts doppelt gezählt wird, darf man Varianzen subtrahieren. Ein negatives oder nullnahes Ergebnis bedeutet unaufgelöst, nicht einen perfekten jitterfreien Detektor. Nichtgaußsche Antwortfunktionen verlangen mehr als eine FWHM-Subtraktion.')
block('B06 · Vorhersage statt nachträglicher Normierung','Mit vorab bestimmtem Niedrigfluss-Gain g ist ε=(r−rdark)/(g·Φ)−1. Den Gain nicht aus derselben gesamten Kurve optimieren, deren Linearität geprüft werden soll. Flusspunkte, Wiederholungen, Reihenfolge und zulässige Drift vorab einfrieren; relative Kalibrierkorrelationen berücksichtigen.')
block('B06 · Totzeitmodell separat testen','Für ein ideal nichtparalysierbares Modell ist rtrue=m/(1−m·τ). Dieses Modell gilt nicht automatisch bei Recovery, Afterpulsing, variabler Schwelle oder Quenchinstabilität. Bei 100 kcps und 50 ns ergibt sich m·τ=0,005 als Größenordnung; das ist keine Messung und keine pauschale Korrekturfreigabe.')
box('Die sieben Metriken bleiben getrennt. Eine höhere PDE kann mit mehr Dunkelcounts oder Afterpulsing einhergehen; eine schmalere Kern-FWHM kann lange Tails verdecken. Primäre Bell-Counts bleiben roh, ohne Effizienz-, Totzeit- oder Hintergrundkorrektur.')
nextpage();title(13,'Benchmark: Koinzidenz und Archiv')
r=F['full_detector_only'][6];block(r['id']+' · '+r['name'],r['procedure']);add('<b>Entscheidung:</b> '+escape(r['criterion']))
block('Unveränderte Paarregel','A-Kanäle 0/1 und B-Kanäle 2/3 bilden einen bipartiten Graphen. Eine Kante liegt vor, wenn die korrigierte Zeitdifferenz im festen ±1000-ps-Fenster liegt. Eine Komponente mit genau einem A- und einem B-Tag zählt als eindeutiges Paar; größere Komponenten zählen als mehrdeutig. Isolierte Singles gehören nicht in M/(M+U).')
block('Verzögerte Fenster','Jeder der vier B-Zeitverschiebungen +50, −50, +100, −100 ns wird separat mit identischer Paarregel ausgewertet. Die vier Werte und ihr vorab festgelegter Mittelwert werden als Diagnose berichtet; keine nachträgliche Wahl der günstigsten Verschiebung. Ein leerer zentraler Nenner ist unbestimmt, nicht null Hintergrund.')
block('Kontrollierter Vergleich','Referenz → DUT → Referenz in identischer optischer Ebene; Quellenmonitor und Wiederholungen. Armtausch/ABBA-Reihenfolge mindert Driftverwechslung. Dunkelrate, Effizienz, Recovery, Timing und Filterzustand mitloggen. Ein Referenzvergleich ohne absolute Kalibrierung liefert relative Leistungsdaten, keine absolute PDE.')
table(['Archivbestandteil','Pflichtinhalt'],[
 ('Rohdaten','Unveränderte native .ttbin plus verwendete SDK-/Firmware-/Treiber-Version; Zähler und Fehlerereignisse erhalten.'),
 ('Kanonische Daten','Kanal, ganzzahliger Zeitstempel, Eventtyp/Status nach validiertem Mapping; unabhängiger Roundtrip, Einheiten und Byteformat im Vertrag.'),
 ('Segmentkontext','Eindeutige Run-/Segment-ID, Start/Stop, Totintervalle, Motor-/Settlingphasen, Konfiguration, Offsets und deren Trainingshash.'),
 ('Integrität','SHA-256, Dateigröße, UTC-Zeit, Instrumentkalibrierungen, Review. Keine Paare über Segment- oder Zeitbasisresets.')],[110,381])
para('Kapazitätsplanung: 4 × 100 000 Tags/s × 2400 s =960 Millionen Tags. Bei einem kanonischen 24-Byte-Datensatz sind das 23,04 GB dezimal, zuzüglich nativer Dateien, Metadaten und Reserve. Das ist eine Formatannahme, nicht die Größe des .ttbin-Formats. Der vorhandene Mindestfreiplatztest ersetzt diese Planung nicht.')
nextpage();title(14,'Freigaben, offene Positionen und Dateien')
table(['Gegenstand','Aktueller Status','Was noch fehlt'],[
 ('DET-0..3 / CAB-0..3','OPEN · Messung NOT_RUN','Serienrevisionen, Kabelartikel, gelieferte Einzelgeräte, R00–R14, danach optische Moduleffizienz/Recovery.'),
 ('TDC-01 / SDK-Archiv','OPEN · Integration nicht freigegeben','Exakte Edition/Lizenz, Readbacks, reale Pulstests, Roundtrip und kanonischer Konverter.'),
 ('PSU-01 / PWR-01','OPEN · Planung','Konkretes Netzteil und Zweigschutz; Spannungs-/Startmessung an allen Verbrauchern.'),
 ('Eigenfrontend','HOLD für Detektorersatz','F00–F09, Leitungsadapter und vollständiger APD-/Quenchpfad; anschließend B01–B07.'),
 ('Gesamte BOM / Bell-System','HOLD','Zusätzlich Pump-, Gaussian/Layout-, Polarisation-, Filter-, Spektral- und optische Systemgates schließen.')],[111,142,238])
block('Verbindliche Statusbedeutung','VERIFIED darf nur eine konkret bezeichnete überprüfte Eigenschaft meinen, z.B. dokumentierter Anschluss oder bestandene Rechnung. Es ist keine Sammelfreigabe des Bauteils. OPEN bedeutet fehlenden Beleg; HOLD sperrt den jeweiligen Freigabeschritt. NOT_RUN bezeichnet eine nicht ausgeführte Messung. Dieses Paket ändert keine vorhandene BOM-Position auf VERIFIED.')
block('Paketinhalt','Referenzvertrag.json und Referenzmessung.template.json bilden Prüfvertrag und ausfüllbaren Messdatensatz. Eigenfrontend_Pruefmatrix.json und Benchmarkmessung.template.json trennen elektrische und optische Kriterien. Zeitmarken-/Koinzidenzvorlagen beschreiben kleine Diagnoseeingaben. analysis.py, test_analysis.py und verify_package.py liefern reproduzierbare Offline-Prüfung.')
block('Nächster ausführbarer Laborschritt','Gelieferte Detektoren, Tagger/Lizenz, Kabel und Netzteil eindeutig aufnehmen; R00–R03 an realer Hardware ausführen. Danach Zähl-/Timing-/Archivpfad. Das Eigenfrontend beginnt unabhängig mit F00/F01 und bleibt von der APD-Hochspannung getrennt. Für B01 zusätzlich kalibrierten Photonfluss bereitstellen; die Referenzdetektion allein ersetzt ihn nicht.')
box('<b>Softwareprüfung:</b> 47 Tests bestanden. <b>Physikalische Prüfung:</b> nicht durchgeführt. Der Offline-Screen bleibt für die leere Vorlage auf HOLD und kann selbst bei vollständigen Daten nur eine nachfolgende unabhängige Freigabe vorbereiten.')
nextpage();title(15,'Quellen und Reproduzierbarkeit')
para('Primärquellen und eingefrorene Projektstände, geprüft am 5. November 2026. Herstellerunterlagen werden verlinkt; sie sind nicht Bestandteil des ZIP. Bei abweichender Lieferrevision gilt vor Anschluss die konkrete Gerätedokumentation.')
for s in S:
 add('<b>'+escape(s['id']+' · '+s['title'])+'</b>','small')
 # compact linked label keeps immutable URL in Quellen.json without unreadable long hash wraps
 add('<link href="'+escape(s['url'])+'" color="#096b86">'+escape('Projektdatei am eingefrorenen Commit öffnen' if s['id'].startswith('P') else s['url'])+'</link>','small')
block('Rechen- und Testnachweise','Rechenergebnisse.json enthält ausschließlich Designrechnungen. Validierung.json nennt Softwaretests und die unabhängige χ²-Referenzprüfung. Referenzscreen_TEMPLATE.json zeigt die erwartete HOLD-Entscheidung bei fehlenden Messwerten. SHA256.json prüft die Paketdateien, nicht die Wahrhaftigkeit ihrer Messinhalte.')
para('Python ≥3.10 genügt für Auswertung und Tests. Der optionale PDF-Neubau verwendet ReportLab und DejaVu-Schriften. Alle aktuellen Messvorlagen sind leer. Synthetische Werte entstehen ausschließlich innerhalb der Regressionstests und dürfen nicht als Labornachweise eingetragen werden.')
add('Eigene Projektbeiträge: Apache-2.0 im X6-Projektumfang. Keine Gerätesteuerung, kein Einkaufsauftrag, keine automatische BOM- oder CHSH-Freigabe.','small')

def footer(c,doc):
 c.saveState();w,h=A4;c.setStrokeColor(colors.HexColor('#cbd6de'));c.line(52,47,w-52,47)
 c.setFont('D',7.5);c.setFillColor(ink);c.drawString(52,33,'X6 · Detektionsqualifikation v0.1 · Hardware NOT_RUN');c.drawRightString(w-52,33,f'{doc.page} / 15');c.restoreState()
out=P/'X6_Detektionsqualifikation_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=52,leftMargin=52,topMargin=44,bottomMargin=60,title='X6 Referenzdetektion und Eigenfrontend v0.1',author='X6 Photonikprojekt')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
