"""Render the six-page reading report; scientific replay uses only stdlib."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Vergangenheitskragen_Stationaritaet_Randzustaende_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
NAVY=colors.HexColor('#12354A');TEAL=colors.HexColor('#087E8B');PALE=colors.HexColor('#EDF5F7')
styles={
'title':ParagraphStyle('title',fontName='DVB',fontSize=23,leading=28,textColor=NAVY,spaceAfter=16),
'sub':ParagraphStyle('sub',fontName='DV',fontSize=10,leading=15,textColor=TEAL,spaceAfter=10),
'h1':ParagraphStyle('h1',fontName='DVB',fontSize=15,leading=20,textColor=NAVY,spaceAfter=12),
'h2':ParagraphStyle('h2',fontName='DVB',fontSize=11,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=6),
'body':ParagraphStyle('body',fontName='DV',fontSize=9.2,leading=14,spaceAfter=8),
'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.5,spaceAfter=6),
'formula':ParagraphStyle('formula',fontName='Mono',fontSize=8,leading=12,backColor=PALE,borderPadding=7,spaceBefore=4,spaceAfter=12),
'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11.5),
'head':ParagraphStyle('head',fontName='DVB',fontSize=8.2,leading=11.5,textColor=colors.white)}
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'h2')
def f(text):p(escape(text).replace('\n','<br/>'),'formula')
def page(title):story.append(PageBreak());p(title,'h1')
def table(headers,rows,widths):
    data=[[Paragraph(escape(str(x)),styles['head']) for x in headers]]
    data.extend([[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),0.6,TEAL)]))
    story.append(t);story.append(Spacer(1,10))

p('CST-DUST<br/>Vergangenheitskragen<br/>und Randzustände','title')
p('Gemeinsame Stationarität und endliche Randbreite · v0.1<br/>8. November 2026 · Zürich','sub')
p('<b>Ergebnis:</b> Ein rationaler Kragen aus vier festen Vorgängern erfüllt die Staub-Normierung und die Uhrgleichung gemeinsam. Die Lösung ist jedoch eine flache Familie mit notwendigen Randreaktionen. Bei endlicher Randbreite verschwinden die Constraint-Residuen nicht, obwohl ihre Mittelwerte exakt null sind.')
table(['Frage','Befund'],[
('Gemeinsame Lösung möglich?','Ja, für ein letztes freies Element auf einer festen Kette mit vier Vorgängern.'),
('Physikalischer Zustand ausgewählt?','Nein. Freie Uhr und Dichte bleiben unbestimmt; die Randpräparation ist nicht hergeleitet.'),
('Wie wirkt Randunsicherheit?','Unabhängige endliche Breite erzeugt positive Residuen. Allgemeine Randfehler lassen sich durch die freie Uhr nicht reparieren.'),
('Dürfen Grenzwerte vertauscht werden?','Nein: Eine scharfe Randvorgabe und eine starke Materiephase ergeben je nach Reihenfolge Rückkehramplituden 1 oder 1/2.')],[175,330])
h('Bedeutung für das Forschungsprogramm')
p('Der kurze Kragen aus PR 265 erfüllte nur die Normierung. Der neue Zeuge schließt diese konkrete algebraische Lücke. Zugleich zeigt er, weshalb eine exakt eingestellte Vorgeschichte nicht automatisch einen konsistenten physikalischen Randzustand liefert.')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Keine hergeleitete Quantisierung, keine vollständige Geometrievariation, kein Bounce. Kein kostenpflichtiger Rechenlauf und kein n=5-Produktionslauf.')
p('Basis: Main nach PR 265, 2b422800dcc0bd79643e1c946069acf8875a5291. Beweise, normierte Zustandsdefinitionen und exakte Nachrechnung befinden sich im Prüfpaket.','small')

page('1 · Wann beide Variationsgleichungen gelten')
p('Die Geometrie und alle Vorgängerwerte sind fest. Nur die Uhr t und das positive innere Dichtegewicht w eines letzten Elements werden variiert. Zukünftige Elemente und zusätzliche Randwirkungsterme fehlen. Die normierte Materiewirkung verwendet die geerbten Intervallgewichte.')
f('b₀ = Σ B_y,   m₁ = Σ B_y T_y,   m₂ = Σ B_y T_y²\nC(t) = 1 + (b₀t² − 2m₁t + m₂)/2\nS_f = −w C(t)/2\n∂_w S_f = −C/2,   q_t = −w(b₀t−m₁)/2')
table(['Fall','Gemeinsame innere Stationarität'],[
('b₀ ≠ 0','t=m₁/b₀; 2+m₂−m₁²/b₀=0; zusätzlich t größer als jede Vorgängeruhr.'),
('b₀ = 0','m₁=0 und m₂=−2; dann ist jede kausal zulässige freie Uhr und jedes positive innere w stationär.')],[90,415])
h('Warum eine Kette mindestens vier Vorgänger braucht')
p('Die positiven Abstände vom jüngsten zum ältesten Vorgänger seien d₁&lt;d₂&lt;d₃. Für eine, zwei oder drei Vorgänger kann die Uhrableitung nicht verschwinden:')
f('m=1:  d₁ > 0\nm=2:  d₁ − 9d₂ < 0\nm=3:  d₁ − 9d₂ + 16d₃ > 0')
p('Ab vier Vorgängern summieren sich die relevanten Gewichte zu 1−9+16−8=0. Ältere Kettenvorgänger haben Gewicht null. Jede gemeinsame Lösung in dieser Klasse erfüllt deshalb die flachen Momentbedingungen m₁=0 und m₂=−2.')
p('<b>Geltungsgrenze:</b> Die Minimalität betrifft eine Kette, genau ein letztes freies Element und die Wirkung ohne zusätzliche Randterme. Sie gilt nicht allgemein für beliebige Kausalsets. Das Dichtegewicht wird nicht als physikalische Ruhemasse identifiziert.','small')

page('2 · Exakte Lösung, flache Richtung, Randreaktion')
p('Ein rationaler Zeuge besitzt die folgenden vier festgehaltenen Vorgängeruhren. Alle vier Vorgängerdichten liegen im Nullatom des geerbten Maßes.')
f('T = (−5/2, −2, −4/3, 0)\nB = (−8, 16, −9, 1)\nb₀ = 0,   m₁ = 20−32+12 = 0\nm₂ = −50+64−16 = −2\nC(t)=q_t=S_f=0   für jedes t>0 und 0<w<1')
h('Stationarität wählt keine Entwicklung aus')
p('Die gesamte Hessematrix in den freien Variablen (t,w) ist null. Es gibt weder einen isolierten Sattel noch einen ausgewählten Uhrwert oder Dichtewert. Eine Dynamik für einen vollständigen Staubball folgt aus dieser einzelnen stationären Zeile nicht.')
h('Die äußeren Daten tragen eine Reaktion')
f('j_(y→f) = w B_y(t−T_y)/2\nq_y = j_(y→f),   q_t = −Σ j_(y→f)\nΣ_z T_z q_z = −Σ_x w_x Γ_x\nAm stationären freien Element: Σ_Rand T_y q_y = w')
p('Für t=w=1/2 sind die vier Randreaktionen (−6, 10, −33/8, 1/8). Sie summieren sich zu null, ihre mit den Randuhren gewichtete Summe ist aber 1/2. Das ist eine exakte Variationsbilanz.')
p('Die Vorgänger bleiben gerade deshalb äußere Daten: Ihre Uhrableitungen verschwinden nicht. Bei einer späteren gemeinsamen Randvariation muss diese Reaktion berücksichtigt werden. Vorzeichenbehaftete Variationsströme sind noch kein positiver physikalischer Massenstrom.')
p('<b>Erreicht:</b> gemeinsamer Normierungs- und Uhrzeuge in der angegebenen Randklasse. <b>Offen:</b> physikalische Auswahl und Präparation des Randes sowie die Dynamik des gesamten Systems.','small')

page('3 · Endliche Randbreite: Mittelwert genügt nicht')
p('Für Randabweichungen δ_y definiere die beiden Momentänderungen. Die Störungsgleichungen sind exakt, ohne abgeschnittene Entwicklung:')
f('d⁽¹⁾ = Σ B_y δ_y\nd⁽²⁾ = 2Σ B_y T_y δ_y + Σ B_y δ_y²\nC_δ(t) = −t d⁽¹⁾ + d⁽²⁾/2\nq_δ = w d⁽¹⁾/2')
p('Beide Gleichungen verschwinden nur bei d⁽¹⁾=d⁽²⁾=0. Die lokale Momentfläche hat Kodimension zwei. Eine freie Uhrkorrektur beseitigt d⁽¹⁾≠0 nicht. Gemeinsame Verschiebungen aller Randuhren bleiben dagegen stationär, sofern die Kausalordnung erhalten bleibt.')
h('Normierter kinematischer Prüfzustand')
p('Wir erklären zusätzlich einen L²-Randraum mit Lebesgue-Maß. Die vier Randfehler sind unabhängig und uniform in [−ε,ε], die freie Uhr ist uniform in [1/4,1]. Die Dichtewellenfunktion ist konstant im ursprünglichen Maß ½δ₀+½dw. Dies ist ein Prüfvertrag, keine abgeleitete physikalische Präparation.')
f('Ψ_B,ε = (2ε)⁻² · 1_[−ε,ε]⁴\nφ_t = 2/√3 · 1_[1/4,1],   φ_w=1,   ||ψ_ε||=1\nE C = E q = 0\n||Cψ_ε||² = (21751/24) ε² + (134/15) ε⁴\n||qψ_ε||² = (67/12) ε²\n||wCψ_ε||² = ||Cψ_ε||²/6')
p('Trotz verschwindender Mittelwerte sind die Constraint-Residuen bei jeder positiven Breite ungleich null. Die exakte Momentfläche hat Maß null; sie trägt keinen nichtverschwindenden L²-Zustand unter dem erklärten Randmaß.')
p('Beim Halbieren der Breite beträgt das Überlappungsquadrat 1/16. Die normierten Pakete konvergieren nicht in Norm zum scharfen Kragen; ihre schwache Grenze ist null. Ein anderes physikalisches Skalarprodukt könnte die Frage ändern und müsste erst hergeleitet werden.','small')

page('4 · Warum die beiden Grenzen nicht vertauschen')
p('Auf dem erklärten kinematischen Raum betrachten wir eine normierte Rückkehramplitude. Die identische Präparation und Auslese sind Bestandteil dieses zusätzlichen Vertrags; ein realer Detektor ist damit nicht hergeleitet.')
f('A_ε(μ) = <ψ_ε, exp(−iμwC/2) ψ_ε>\n       = E_(δ,t) χ(μC/2)\nχ(u) = 1/2 + (1−exp(−iu))/(2iu),   χ(0)=1')
p('Bei exakt festem stationärem Kragen verschwindet C identisch: A₀=1. Für jede positive Breite ist C ein nichtverschwindendes Polynom. Seine Nullmenge hat Maß null. Damit konvergiert χ fast überall gegen 1/2; |χ|≤1 erlaubt dominierte Konvergenz.')
table(['Reihenfolge','Amplitude / Rückkehrwahrscheinlichkeit'],[
('Zuerst ε→0, dann |μ|→∞','1 / 1'),
('Zuerst |μ|→∞, dann ε→0','1/2 / 1/4')],[245,260])
p('Die scharfe Randvorgabe verändert die Voraussetzung des bisherigen Atomgrenzsatzes: Ein Phasenpolynom ist jetzt identisch null. Das ist kein Widerspruch zum Satz aus PR 265 und kein hergeleiteter semiklassischer Grenzwert der Gravitation.')
h('Rigorose endliche Fehlerbudgets')
f('Für ε≤1/64, t∈[1/4,1]:   |C|≤B_ε=98ε+17ε²\n|A_ε−1| ≤ min(2, |μ|B_ε/8, μ² E[C²]/48)\nTaylor-Mittelpunkt bis Grad vier mit Fehlerradius\nr₅ ≤ |μ|⁵ B_ε⁵ / 46080')
p('Die Momente werden exakt rational integriert. Zwölf endliche Amplitudenbudgets decken drei Breiten und vier Phasenwerte ab. Für gekoppelte Folgen ε→0 führt με→0 zur Amplitude 1; |μ|ε→∞ führt zu 1/2. Eine allgemeine Konvergenzrate wird nicht behauptet.','small')

page('5 · Evidenz und nächste physikalische Entscheidung')
table(['Kontrolle','Ergebnis'],[
('Kettenfälle','216 exakt; davon 135 gemeinsam stationär und 81 kurze nichtstationär.'),
('Randstörungen','2187 Fälle; Störungsgesetze und uniforme Schranken erfüllt.'),
('Normierte Randpakete','Drei Breiten; exakte Momente bis Ordnung vier.'),
('Bedingte Amplitudenbudgets','Zwölf rationale Mittelpunkte und rigorose Fehlerradien.'),
('Negativannahmen / Nachrechnung','Neun zurückgewiesen; fünf Ergebnisdateien isoliert bytegleich.')],[190,315])
p('Die allgemeinen Aussagen werden analytisch bewiesen; die endlichen Kontrollen ergänzen die Beweise. Es gibt keine externe Replikation oder Beweisassistentenprüfung. Ketten mit bis zu acht festen Vorgängern prüfen nur eine freie Variationszeile und sind kein n=5-Produktionslauf.','small')
f('python3 -B verify_package.py\npython3 -B replay.py')
h('Was jetzt mathematisch vorbereitet ist')
p('Das gemeinsame Momentkriterium, ein exakter Zeuge, die Randreaktion und ein Unsicherheitsbudget sind geschlossen. Ein größerer Rechenlauf muss diese elementare Randfrage nicht mehr erst entdecken.')
h('Was als Nächstes physikalisch begründet werden muss')
p('<b>Eine Randpräparation samt Maß beziehungsweise Skalarprodukt und eine Randwirkung oder gemeinsame Randvariation, welche die Reaktionsbilanz trägt.</b> Sie müsste entscheiden, ob und warum die Momentfläche ausgewählt wird. Ein einfach darauf eingeschränkter Zustand wäre eine neue Annahme. Erst anschließend ist die zugehörige Constraint- und Observablenkonstruktion sinnvoll prüfbar.')
p('Alle acht physikalischen Gates bleiben HOLD. Kein kostenpflichtiger Rechenlauf, kein n=5-Produktionslauf und keine Bounce-Aussage.','small')
h('Quellen und Reproduktionsstand')
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/265" color="#087E8B">Projektbasis PR 265</link>; sechs commitgenau gepinnte Projektdateien. Hintergrund: <link href="https://arxiv.org/abs/1001.2725" color="#087E8B">Benincasa und Dowker (2010)</link>, korrigierte Operatorfassung; <link href="https://arxiv.org/abs/gr-qc/9409001" color="#087E8B">Brown und Kuchař (1995)</link>, eigenständige kanonische Staubkonstruktion. Diese Quellen liefern keine bereits abgeleitete Randquantisierung des hier geprüften Historienmodells.','small')
p('Kontrollplan nach analytischem Entwurf und vor den endlichen Kontrollen eingefroren; keine externe Präregistrierung. Vollständige Beweise und Dateiprüfsummen im Paket.','small')

def footer(c,doc):
    c.setStrokeColor(TEAL);c.setLineWidth(.5);c.line(45,42,550,42)
    c.setFillColor(NAVY);c.setFont('DV',7)
    c.drawString(45,30,'CST-DUST · Vergangenheitskragen / Stationarität / Randzustände · v0.1')
    c.drawRightString(550,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=50,topMargin=48,bottomMargin=60,
    title='CST-DUST: Vergangenheitskragen, Stationarität und Randzustände v0.1',author='Thomas Gfeller · CST-DUST research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)

