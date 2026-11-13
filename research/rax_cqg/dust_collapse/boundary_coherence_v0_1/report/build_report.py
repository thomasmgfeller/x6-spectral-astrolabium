#!/usr/bin/env python3
"""Compact four-page report from the saved follow-up results."""
from pathlib import Path
from decimal import Decimal
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'report/CST_DUST_Kohaerente_Endrandmessung_v0_1.pdf'
font=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DV-B','DejaVuSans-Bold.ttf'),('DV-I','DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(font/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-B',italic='DV-I',boldItalic='DV-B')
BLUE=colors.HexColor('#173C53')
TEAL=colors.HexColor('#006D77')
LIGHT=colors.HexColor('#EEF4F6')
INK=colors.HexColor('#172B38')
GRAY=colors.HexColor('#53646D')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='T',fontName='DV-B',fontSize=22,leading=27,textColor=BLUE,spaceAfter=13))
styles.add(ParagraphStyle(name='H',fontName='DV-B',fontSize=14,leading=18,textColor=BLUE,spaceAfter=9,spaceBefore=8))
styles.add(ParagraphStyle(name='B',fontName='DV',fontSize=9.5,leading=13.5,textColor=INK,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallD',fontName='DV',fontSize=8,leading=11,textColor=GRAY,spaceAfter=6))
styles.add(ParagraphStyle(name='Eq',fontName='DV',fontSize=10,leading=15,textColor=BLUE,backColor=LIGHT,borderPadding=8,spaceBefore=5,spaceAfter=12))
styles.add(ParagraphStyle(name='CellD',fontName='DV',fontSize=8.1,leading=11,textColor=INK))
styles.add(ParagraphStyle(name='CellH',fontName='DV-B',fontSize=8.1,leading=11,textColor=colors.white))
story=[]
def p(text,style='B'): story.append(Paragraph(text,styles[style]))
def h(text): p(text,'H')
def eq(text): p(text,'Eq')
def table(rows,widths):
    cells=[[Paragraph(str(c),styles['CellH' if i==0 else 'CellD']) for c in row] for i,row in enumerate(rows)]
    t=Table(cells,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
       ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[LIGHT,colors.white]),
       ('LINEBELOW',(0,0),(-1,0),0.6,TEAL)]))
    story.append(t);story.append(Spacer(1,10))
def mid(pair): return (Decimal(pair[0])+Decimal(pair[1]))/2
def pct(pair): return f'{100*mid(pair):.7f}'.replace('.',',')+' %'
def sci(pair): return f'{mid(pair):.6E}'.replace('.',',')
r=json.loads((ROOT/'checks/root_R_audit.json').read_text())
a=json.loads((ROOT/'checks/root_exact_audit.json').read_text())
m=json.loads((ROOT/'checks/r_records_results.json').read_text())
g=json.loads((ROOT/'checks/physical_gate.json').read_text())
audit=json.loads((ROOT/'checks/hilbert_audit.json').read_text())
extra=json.loads((ROOT/'checks/extended_R_results.json').read_text())

p('CST-DUST<br/>Kohärente Endrandmessung','T')
p('Ausführung der fünf Schritte · Version 0.1 · 13. November 2026','SmallD')
p('<b>Ergebnis:</b> Die relative Gravitationsphase kann im erklärten endlichen Modell eine Verteilung tatsächlicher terminaler Skalarmoden verändern. Dazu wurden zwei unabhängige Endrandpakete konstruiert und mit den vorhandenen Amplituden ausgewertet. Eine physische Quellen- oder Geometriekalibrierung folgt daraus noch nicht.')
table([
 ['Schritt','Ausgeführt','Einordnung'],
 ['1 · Recordvertrag','Gemeinsame Randereignisse, Umweltüberlapp und vollständige kohärente Instrumente hergeleitet.','Bedingte Existenz; physische Kohärenz nicht bestimmt.'],
 ['2 · Interferenz','Vorhandene Amplitudenintervalle auf kohärente, dephasierte und klassisch zusammengefasste Auslese fortgepflanzt.','Interferenzkontrollen bestanden.'],
 ['3 · Endrand','Zwei normierte, orthogonale Skalarmoden; Gaußmomente und Randverteilungen berechnet.','Materie-Records bestanden; keine Radiusmessung.'],
 ['4 · Quelle/Uhr','Quellenbedingungen, Strombilanzen, Reflexionsparität und einen unübernommenen gerichteten Uhrkandidaten geprüft.','Begrenzte Hindernisse bestätigt.'],
 ['5 · Geometrie','Zulässigkeit eines physischen Zwei-Quellen-Geometrievergleichs geprüft.','HOLD: physischer Vergleich nicht definiert.']
],[79,258,166])
p('Der neue bedingte Präparationsunterschied im zweiten Endrandrecord liegt bei <b>2,52 × 10<super>-6</super></b>. Er ist unter den übernommenen Amplitudeneinschließungen strikt von null getrennt. Auch die getrennte Entfernung nur der F<sub>4</sub>-Phasen verändert die Randverteilung. Diese Entfernung ist eine kontrafaktische Änderung der Wirkung, kein physisch verfügbarer Gravitationseinsteller.')
p('<b>Vollständige Bilanz:</b> Die Erfolgswahrscheinlichkeiten des neuen Hilfsinstruments liegen nur bei etwa 3,59 × 10<super>-10</super> und 9,35 × 10<super>-10</super>. Alle Resultate führen auch Misserfolg mit. Die Zahlen sind keine Zählraten realer Hardware.')
p('Umfang: sechs vorhandene Historien; null neue Uhrquadraturen; kein bezahlter Rechenauftrag. Fünf KI-Arbeitsperspektiven mit gegenseitiger Prüfung und zusätzlichem unabhängigem rationalem Audit. Die historischen Personennamen der Agenten bezeichnen ausschließlich diese Perspektiven.','SmallD')
story.append(PageBreak())

h('1. Was die neue Messung voraussetzt')
p('Im geerbten Vertrag sind P={0}, A={1,2}, I={3}, R={4,5}. Beide Klassen besitzen denselben induzierten äußeren Rand. Ihre komplexen Amplituden lassen sich daher gemeinsam paaren. Die P/A-Präparation und sämtliche ursprünglichen Wirkungsbeiträge bleiben erhalten. Das innere Atom-/Positivstratum s wird zunächst weiterhin unterschieden.')
eq('a<sub>1s</sub> = exp(9iκ)b<sub>1s</sub>, &nbsp; a<sub>2s</sub> = exp(-7iκ)b<sub>2s</sub><br/>D<sub>12,s</sub> = λ² γ<sub>s</sub> a<sub>1s</sub> a<sub>2s</sub>*')
p('γ<sub>s</sub>=&lt;e<sub>2s</sub>|e<sub>1s</sub>&gt; beschreibt einen festen, präparationsunabhängigen Umweltüberlapp. Klassisches Weglassen eines fertigen Klassenrecords erzeugt keinen Kreuzterm. γ=0 und γ=1 sind mit denselben alten Klassenwahrscheinlichkeiten vereinbar. Deshalb bestimmen die alten Daten weder die physische Kohärenz noch die gemeinsame Phasenreferenz. γ=1 ist hier ein ausdrücklich angenommener neuer Randvertrag.')
eq('Diagnose: M<sub>±,s</sub> = λ(a<sub>1s</sub> ± a<sub>2s</sub>)/√2, &nbsp; λ=1/256<br/>Direkter Endkanal: C<sub>s</sub> = λ(a<sub>1s</sub> + a<sub>2s</sub>)')
p('Die beiden Diagnoseports zusammen erhalten den alten akzeptierten Effekt und dessen Misserfolgsoperator exakt. Der direkte Kanal ist ein anderes Instrument mit eigener Misserfolgsergänzung. Er ist kein deterministisches Löschen eines schon dephasierten Registers. Rephasierungen der Amplituden müssen gemeinsam mit der Detektorreferenz transformiert werden.')
h('2. Zwei tatsächliche Endrandpakete')
eq('f<sub>0</sub> = R<sub>f</sub>, &nbsp; f<sub>2</sub> = [(q<sub>4</sub>+q<sub>5</sub>)²-1] f<sub>0</sub>/√2<br/>a<sup>(2)</sup><sub>c,s</sub> = η<sub>c</sub> a<sup>(0)</sup><sub>c,s</sub>')
p('f<sub>2</sub> ist der niedrigste nichtkonstante gerade Hermitemodus im symmetrischen Endskalar. Breite und Maß bleiben unverändert. Die Pakete sind exakt orthonormal, invariant unter 4↔5 und global skalarparitätsgerade. Der Faktor η<sub>c</sub> folgt durch Differentiation desselben Gaußintegrals: η<sub>c</sub>=(ℓᵀQ<sub>c</sub><super>-1</super>ℓ-1)/√2. Alle sechs Historien und die bestehenden Abel-/Fresnelzweige wurden geprüft.')
p('η<sub>1</sub> ≈ -0,118080653112 - 0,036700132704i<br/>η<sub>2</sub> ≈ -0,073016405704 - 0,015693835688i')
p('Die unterschiedlichen Faktoren ergeben zusammen mit dem vorhandenen Nichtnullminor Rang zwei der kohärenten Eingangs-/Endmateriekarte im positiven Innenstratum. Ein alter einzelner Endprojektor hätte diese neue Randverteilung nicht bestimmen können; die zusätzliche Information stammt aus der ursprünglichen quadratischen Wirkung.')
story.append(PageBreak())

h('3. Numerische Ergebnisse und Kontrollen')
p('Die folgende Tabelle zeigt P(f<sub>2</sub>|Erfolg). γ=1 bezeichnet die ideale kohärente Annahme; γ=0 die vollständig dephasierte Kontrolle. κ=0 entfernt ausschließlich die Gravitationsphasen und ist eine kontrafaktische Wirkungskontrolle. Alle übrigen Eingaben bleiben gleich. Angegeben sind gerundete Intervallmitten; die maschinenlesbaren Dateien enthalten die vollständigen äußeren Schranken.')
rows=[['Eingabe','γ=0, κ=1','γ=1, κ=1','γ=1, κ=0','P(Erfolg)<br/>γ=1, κ=1']]
for row in r['results']:
    rows.append([row['input'],pct(row['dephased']['R2_given_success']),pct(row['coherent']['R2_given_success']),pct(row['counterfactual_kappa0_R2_given_success']),sci(row['coherent']['success'])])
table(rows,[51,113,113,113,113])
table([
 ['Kontrolle / Kontrast','Konservative Einschließung'],
 ['Δ P(f2|Erfolg), g+ minus g0, γ=1, κ=1','[2,5194; 2,5240] × 10<super>-6</super>'],
 ['Zusätzlicher Quellenkontrast: γ=1 minus γ=0','[1,7819; 1,8659] × 10<super>-7</super>'],
 ['Änderung des Quellenkontrasts: κ=1 minus κ=0','[-1,0750; -1,0665] × 10<super>-6</super>'],
 ['Alte ±-Diagnose: Δ P(+|Erfolg), g+ minus g0','[-6,2196; -6,2097] × 10<super>-5</super>']
],[293,210])
p('<b>Wichtig:</b> Schon die dephasierte Zwei-R-Karte reagiert auf die Präparation. Ein Nichtnull-Präparationskontrast allein ist daher kein Interferenznachweis. Der zusätzliche Beitrag wird durch den Gamma-Vergleich und die separate F<sub>4</sub>-Kontrolle abgegrenzt.')
h('Normierung auf dem gesamten Eingangsraum')
p('Für die gewichteten Endnormen gilt ‖f<sub>0</sub>‖²<sub>V</sub>=65 und ‖f<sub>2</sub>‖²<sub>V</sub>=799. Der alte Gain durfte deshalb nicht ungeprüft übernommen werden. λ<sub>R</sub>=1/1024 wurde vor den neuen Randwerten aus der analytischen Majorante festgelegt.')
eq('Q<sub>R</sub> ≤ (548451/1638400) I<sub>E</sub><br/>= 0,3347479248046875 I<sub>E</sub> &lt; I<sub>E</sub><br/>F<sub>R</sub> = (I<sub>E</sub> - Q<sub>R</sub>)<super>1/2</super>')
p('Diese Schranke gilt auf E=span(g<sub>0</sub>,g<sub>+</sub>), auch für kohärente Superpositionen. Der neue Misserfolgsoperator wurde eigenständig ergänzt. Die Ergänzung ist ein endliches Instrument auf E; sie identifiziert Misserfolg nicht mit einem bereits hergeleiteten vollständigen physikalischen Außenraum.')
p('Die geerbten Amplitudenrechtecke wurden mit mpmath.iv und unabhängig mit exakten rationalen Intervalloperationen fortgepflanzt. Für die unabhängige Phasenkontrolle werden sin(16), cos(16) durch rationale Taylorpolynome samt reellem Lagrangerest eingeschlossen. Die alte Quadratur wird dabei als dokumentierte Voraussetzung übernommen.','SmallD')
story.append(PageBreak())

h('4. Quellen, Uhren und physikalisches Entscheidungstor')
eq('C<sub>i</sub> = 1 + β(T<sub>i</sub>-T<sub>0</sub>)²/2 ≥ 1, &nbsp; i=1,2<br/>S(-T)=S(T), &nbsp; J(-T)=-J(T)')
p('Auf allen sechs Historien wurden zwölf Quellenidentitäten, 36 Strom-/Divergenzidentitäten und 68 Stromparitäten exakt geprüft. C<sub>A</sub>≥1 schließt die betreffende frei variierte positive stationäre Quelle aus. Es schließt allgemein vorbereitete Quantenrandzustände nicht aus. Ihre physische Constraintpaarung und Massenkalibrierung sind weiterhin nicht hergeleitet.')
p('Die ursprünglichen Uhrpakete sind reflektionsgerade. Einzelne orientierte Strominsertionen verschwinden deshalb exakt. Sowohl die Klassenmischung als auch f<sub>0</sub>/f<sub>2</sub> erhalten diese Eigenschaft. Das ist kein physischer Stromerwartungswert und kein Nachweis verschwindender Masse. Alle intrinsischen R-Ordnungsobservablen sehen dieselbe Zweierantichain; die Skalarmoden messen keine abgeleitete Raumgeometrie.')
eq('Unübernommener Kandidat:<br/>χ=(T<sub>1</sub>+T<sub>2</sub>)/2-T<sub>0</sub><br/>h<sub>η</sub>=(1+ηχ/2)/√(1+η²/8), &nbsp; -1&lt;η&lt;1')
p('Dieser glatte relative Uhrfaktor wurde exakt normiert und auf Symmetrien geprüft. Er behält die volle Uhrstütze und zeigt, dass kinematische Orientierung möglich ist. Er liegt außerhalb des eingefrorenen Vertrages: Weder sein physischer Auswahlgrund noch ein nichtverschwindender wirkungsgewichteter Strom wurden nachgewiesen. Er wurde nicht in die erfolgreichen Resultate eingesetzt.')
p('<b>Schritt 5: HOLD.</b> Der physische Zwei-Quellen-Geometrievergleich wurde auf Zulässigkeit geprüft. Es fehlen eine begründete Quellen-/Uhrkalibrierung und geometrische Randobservable; auch Skala, Verfeinerungsfamilie und globaler Außenraum sind nicht festgelegt. Daher wurden keine physische Kollapskurve und keine Rückwirkung behauptet. Der getrennte positive kanonische Quellenpatch wurde algebraisch nachgeprüft, jedoch nicht in den Quantenpiloten übertragen.')
h('Reproduktion und nächster sinnvoller Arbeitspunkt')
p('Das Prüfpaket ist ohne ältere Nachbarverzeichnisse ausführbar: <b>python checks/run_all.py</b>. Alle sieben Prüfer bestanden auch einen isolierten Wiederholungslauf. Hilberts unabhängiger Audit enthält '+str(len(audit['checks']))+' bestandene Checks. Die wissenschaftlichen Skripte benötigen Python, mpmath, SymPy und NumPy; keine neue Uhrintegration.')
p('Der nächste Arbeitspunkt ist eine gemeinsame physische Quellen-/Uhr-/Observable-Konstruktion mit klarer Constraintpaarung. Der orientierte Uhrkandidat ist dafür eine prüfbare Möglichkeit, aber noch keine Lösung. Eine größere Historienfamilie oder weitere Dezimalstellen würden diese fehlende Begründung nicht ersetzen.')
p('Provenienz: Wirkungsstand 338a3ebb28507790fe916ae577920d0c264acab9; veröffentlichter Sammelstand 9f31ae8034c398efc979e47d7fa5b66b61e13517. Vollständige Hashes, Verträge und Quellen liegen im Paket. θ=0 war vorher bekannt; keine neue blinde Validierung wird behauptet. Diese Ausführung verändert GitHub nicht.','SmallD')
p('Methodischer Anschluss: Mozota Frauca / Sorkin, How to Measure the Quantum Measure, arXiv:1610.02087. Die Literatur begründet nicht die physische Realisierung dieses CST-Instruments.','SmallD')

def footer(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D1DEE3'))
    canvas.line(46,40,A4[0]-46,40)
    canvas.setFont('DV',7.5);canvas.setFillColor(GRAY)
    canvas.drawString(46,27,'CST-DUST · Kohärente Endrandmessung v0.1 · Bedingtes endliches Modell')
    canvas.drawRightString(A4[0]-46,27,str(doc.page))
    canvas.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=43,bottomMargin=53,
    title='CST-DUST: Kohärente Endrandmessung v0.1',author='CST-DUST Forschungsauswertung mit KI-Agentenunterstützung',
    subject='Ausgeführte Interferenz-, Endrand- und physikalische Zulässigkeitsprüfungen')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
