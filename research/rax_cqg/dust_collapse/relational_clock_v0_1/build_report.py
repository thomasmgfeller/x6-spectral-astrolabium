#!/usr/bin/env python3
"""Build the compact scientific report; all exact tables come from result files."""
from pathlib import Path
from fractions import Fraction as F
import json
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Relationale_Uhr_Kandidatenpruefung_v0_1'
FONT = '/usr/share/fonts/truetype/dejavu/'
for name, file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, FONT+file))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')
BLUE = colors.HexColor('#17445e')
GRAY = colors.HexColor('#58646e')
styles = {
    'title': ParagraphStyle('title', fontName='DVB', fontSize=25, leading=31, textColor=BLUE, spaceAfter=16),
    'h': ParagraphStyle('h', fontName='DVB', fontSize=15, leading=19, textColor=BLUE, spaceBefore=10, spaceAfter=9),
    'b': ParagraphStyle('b', fontName='DV', fontSize=10.2, leading=15.0, spaceAfter=9),
    's': ParagraphStyle('s', fontName='DV', fontSize=8.2, leading=11.5, textColor=GRAY, spaceAfter=7),
    'eq': ParagraphStyle('eq', fontName='DV', fontSize=11.4, leading=20, textColor=BLUE, leftIndent=10, spaceBefore=5, spaceAfter=12),
    'cell': ParagraphStyle('cell', fontName='DV', fontSize=8.6, leading=12.1),
}
story = []


def p(text, style='b'):
    story.append(Paragraph(text, styles[style]))


def h(text):
    p(text, 'h')


def eq(text):
    p(text, 'eq')


def page():
    story.append(PageBreak())


def table(rows, widths, padding=7):
    t = Table([[Paragraph(str(x),styles['cell']) for x in row] for row in rows], colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef4f7')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),padding),
        ('BOTTOMPADDING',(0,0),(-1,-1),padding),('LINEBELOW',(0,0),(-1,0),.7,BLUE),
        ('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d6dee3'))]))
    story.append(t)
    story.append(Spacer(1,10))


def footer(c, doc):
    c.setStrokeColor(colors.HexColor('#d6dee3'))
    c.line(43,49,552,49)
    c.setFont('DV',8)
    c.setFillColor(GRAY)
    c.drawString(43,35,'CST-DUST · Relationale Uhr und Kandidatenprüfung v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def main():
    order=json.loads((ROOT/'results/clock_ordering.json').read_text())
    domain=json.loads((ROOT/'results/domain_measure.json').read_text())
    replay=json.loads((ROOT/'results/replay.json').read_text())
    p('Relationale Uhr und<br/>Kandidatenprüfung','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Ein konkreter Weg zur Uhrentwicklung scheitert an einer klaren Bedingung.')
    p('Kausal geordnete Materie-Uhren erlauben eine eindeutige chronologische Beschreibung der Historien. Präparation und scharfe Uhrereignisse lassen sich darin definieren. Doch die zusätzliche Deutung <b>„genau ein neues Element ist ein geschlossener normerhaltender Evolutionsschritt“</b> besteht die Prüfung nicht.')
    table([
        ['Geprüfter Baustein','Ergebnis'],
        ['Relationaler Schnitt nach T','Auf dem monotonen Uhrsektor ein labelinvariantes Ordnungsideal.'],
        ['Chronologische Zählung','Exakt hergeleitet; der bisherige Faktor 1/e(P) fällt nach der Umnummerierung weg.'],
        ['Präparation und lokales Produkt','Explizit definiert; noch keine physikalische Constraint-Reduktion.'],
        ['Geschlossene Ein-Geburts-Fortsetzung','Ausgeschlossen auf den erklärten vollständigen Räumen mit äquivalenten beschränkten Produkten.'],
        ['Geburt / keine Geburt','Als Hilfsinstrument möglich; relative Gewichtung und physikalische Uhrentwicklung bleiben unbestimmt.'],
    ],[175,334])
    h('Warum das für den Staubball wichtig ist')
    p('Die Materieuhr darf nicht durch eine bloße Geburtsnummer ersetzt werden. Ihre Auswahl verändert die zulässigen Historien und die verbleibende Feldmaßmasse. Eine positive Norm aus dem bisherigen freien Uhrraum lässt sich deshalb nicht unverändert übernehmen.')
    p('<b>Konkreter Zusatzkandidat: FAIL. Acht physikalische Gates: HOLD.</b> Der Befund ist kein No-go für CST oder Staubuhren. Ein physikalisches Skalarprodukt, eine globale Uhr im Vakuumaußenraum, ein Junction-Gesetz und ein Bounce bleiben offen.','s')
    p('Basis: Main 5e08cef8dcac5c7d1214dd2beff1b1533427e856 nach PR 251. Allgemeine Beweise, exakte Daten und Nachrechnung im Prüfpaket.','s')

    page()
    h('1 · Einen Uhrsektor wählen ist mehr als Labels umbenennen')
    p('Der Schnitt J<sub>τ</sub> enthält alle Elemente mit T≤τ. Wenn T entlang jeder kausalen Relation streng wächst, enthält dieser Schnitt auch jeden Vorgänger seiner Elemente: Er ist ein Ordnungsideal. Ohne diese Annahme kann schon eine Zweierkette einen „Schnitt“ liefern, der nur das spätere Element enthält.')
    eq('J<sub>τ</sub>={x:T<sub>x</sub>≤τ}, &nbsp; y≺x ⇒ T<sub>y</sub>&lt;T<sub>x</sub>')
    p('Die maximalen Elemente des Ideals sind eine Antikette. Sie sind damit noch keine qualifizierte physikalische Cauchyfläche und ersetzen bei der nichtlokalen Wirkung nicht die benötigte Vergangenheit. Im Vakuum bleibt T zunächst ein Hilfsfeld.')
    h('Nach der Auswahl ist chronologische Beschriftung exakt möglich')
    p('D<sub>P</sub> ist der kausal geordnete Uhrbereich einer natürlichen Ordnung P; Δ<sub>m</sub> enthält die global steigenden Uhrwerte. e(P) zählt die linearen Erweiterungen. Für jede gemeinsam labelinvariante Einfügung F, auch mit voller Wirkungsphase, gilt:')
    eq('Σ<sub>P nat</sub> [1/e(P)] ∫<sub>D(P)</sub> F dν = Σ<sub>P nat</sub> ∫<sub>Δm</sub> F dν')
    p('Jeder vollständige chronologische Datensatz besitzt e(P) natürliche Beschreibungen. Ihre Gewichte 1/e(P) summieren sich zu eins. Der Faktor darf nach der Sortierung nicht nochmals eingefügt werden. Alle Uhr- und Dichtemarken werden gemeinsam permutiert.')
    h('Die Monotonieselektion selbst verändert relative Amplituden')
    eq('Maß(D<sub>P</sub>)=e(P)/m!, &nbsp; Maß(Δ<sub>m</sub>)=1/m!')
    table([['Phasenfreier Geometrietyp','Freie Uhren','Monotoner Sektor'],['Zweierantikette','1/2','1/2'],['Zweierkette','1','1/2']],[279,115,115],padding=5)
    p('Diese relative Änderung ist keine gemeinsame Normierung. Ein nachträgliches Normieren jeder Geometrie auf Maß eins wäre eine weitere Modellwahl. Die Gleichheit der vollständigen festen-m-Summen ist außerdem kein Beweis einer unitären Konjugation der alten beliebigen Präfixentwicklung.','s')

    page()
    h('2 · Ein konkreter Präparations- und Auslesekandidat')
    p('Nach chronologischer Beschriftung wählen wir das gewöhnliche lokale L²-Produkt über die geordneten Uhrwerte und alle Dichtewerte, getrennt nach natürlichen Geometrien:')
    eq('H<sub>m</sub><super>chron</super>=⊕<sub>P nat</sub> L²(Δ<sub>m</sub>×[0,1]<super>m</super>,dν<sub>T</sub><super>m</super>dν<sub>w</sub><super>m</super>)')
    p('Hier ist dν<sub>T</sub>=dT/(2L) und dν<sub>w</sub>=½δ₀+½dw auf (0,1). Indikatoren aktueller Uhrbereiche oder Staubmarkierungen sind in diesem Produkt orthogonale Projektoren. Ihre physikalische Dirac-Deutung ist noch nicht hergeleitet.')
    h('Explizite positive Staubpräparation, L=1 und m=1')
    eq('ψ<sub>I</sub>(T,w)=√(4/|I|) · 1<sub>I</sub>(T) · 1<sub>w&gt;0</sub>')
    p('Für I<sub>−</sub>=[−1/2,0] und I<sub>+</sub>=[0,1/2] ist die Norm jeweils exakt eins. Diese Präparation wurde unabhängig von einem gewünschten Bounce festgelegt. Sie erfüllt nicht automatisch die dynamischen Staubgleichungen.')
    h('Die chronologische Fortsetzung und ihre Norm')
    p('Ein neues Element erhält einen Uhrwert t größer als alle alten und ein beliebiges Vergangenheitsideal J. Die korrekte chronologische Amplitude trägt nur die geerbte Wirkungsphase. Sei d(P) die Zahl der Ideale:')
    eq('(A<sub>m</sub>ψ)(Kind)=exp(iΔS/ℏ)ψ(Eltern), &nbsp; T<sub>m</sub>&lt;t&lt;L<br/>A<sub>m</sub>†A<sub>m</sub>=r<sub>m</sub>, &nbsp; r<sub>m</sub>=d(P)(L−T<sub>m</sub>)/(2L)')
    table([['Normierte Präparation','Ausgangsnorm²'],['I−=[−1/2,0]','5/4'],['I+=[0,1/2]','3/4']],[339,170],padding=5)
    p('Keine einzige skalare Normierung macht beide Werte eins. Der Normfaktor folgt exakt durch Integration der neuen Uhr; die volle Wirkungsphase hebt sich dabei auf. Das Ergebnis benötigt keine phasenfreie Näherung.','s')
    p('Eine feste Endauslese bleibt separat beschränkt: Für eine Randphase vom Betrag eins ist ihre duale Norm² gleich |Ω<sub>m</sub><super>nat</super>|/m!. Ein entsprechend skalierter Rang-eins-Effekt ist zulässig, löst aber die Fortsetzungsprüfung nicht.','s')

    page()
    h('3 · Auch ein anderes beschränktes Produkt behebt das nicht')
    p('Der Ausschluss gilt auf den vollständigen gewählten Stufenräumen und umfasst nichtdiagonale, feldabhängige Produkte. Es genügt, dass das Elternprodukt M<sub>m</sub> nach unten und das Kindprodukt M<sub>m+1</sub> nach oben beschränkt ist:')
    eq('M<sub>m</sub>≥aI, &nbsp; 0≤M<sub>m+1</sub>≤bI, &nbsp; a&gt;0, b&lt;∞')
    p('Wähle einen festen Geometrieblock und normierte Uhrpakete, deren letzte Uhr gleichmäßig in (L−ε,L) liegt. Alle früheren Uhren können in einem davon getrennten unteren Bereich liegen. Dann gilt exakt:')
    eq('‖A<sub>m</sub>ψ<sub>ε</sub>‖²=d(P)ε/(4L) → 0')
    p('Eine Isometrie müsste zugleich verlangen:')
    eq('a ≤ ⟨ψ<sub>ε</sub>,M<sub>m</sub>ψ<sub>ε</sub>⟩<br/>= ⟨A<sub>m</sub>ψ<sub>ε</sub>,M<sub>m+1</sub>A<sub>m</sub>ψ<sub>ε</sub>⟩<br/>≤ b·d(P)ε/(4L) → 0')
    p('Das ist ein Widerspruch für jedes m≥1. Auch eine feste skalare Änderung von A hilft nicht. Fünf exakte Kontrollwerte illustrieren den allgemeinen Beweis bei m=1, L=1 und d=2:')
    table([['ε','1/2','1/4','1/8','1/16','1/32'],['Ausgangsnorm²','1/4','1/8','1/16','1/32','1/64']],[139,74,74,74,74,74],padding=5)
    h('Die Grenze betrifft diesen Kandidaten, nicht alle Staubuhren')
    p('Physikalisch eingeschränkte Räume, garantierter Abstand zum Uhrregulator, nichtkoerzive oder unbeschränkte Produkte und eine Evolution mit variabler Elementzahl sind nicht ausgeschlossen. Der Uhrregulator ist keine physikalische Singularität.')
    p('Der vorige markierte Normsatz ließ neue Uhren im ganzen unabhängigen Intervall zu. Jetzt schrumpft das erlaubte neue Uhrintervall nahe L auf null. Damit ist eine entscheidende Voraussetzung geändert. Eine Normierung A·r⁻½ wäre zwar formal isometrisch, veränderte aber die Historienamplituden.','s')

    page()
    h('4 · Ein ergänztes Instrument zeigt, welche Entscheidung fehlt')
    p('Weil ‖A<sub>m</sub>‖²=2<super>m</super>, lassen sich für 0≤α≤2<super>−m</super> zwei positive Ausgänge konstruieren:')
    eq('K<sub>Geburt</sub>=√α A<sub>m</sub>, &nbsp; K<sub>keine</sub>=√(I−αr<sub>m</sub>)<br/>E<sub>Geburt</sub>+E<sub>keine</sub>=αr<sub>m</sub>+(I−αr<sub>m</sub>)=I')
    table([['α, bei m=1','P(Geburt | I−)','P(Geburt | I+)'],['1/4','5/16','3/16'],['1/2','5/8','3/8']],[169,170,170],padding=5)
    p('Beide Skalen ergeben zulässige, aber verschiedene Hilfsinstrumente. Keine ist durch die vorhandene feste-m-Amplitude ausgewählt. α=1 verletzt die Effektgrenze: Bei T=−1/2 wäre der Geburtswert 3/2 und sein Komplement −1/2.')
    p('<b>„Keine Geburt“ ist noch keine physikalische Wartezeit.</b> Es fehlen eine Regel für feste Δτ, die relative Gewichtung unterschiedlicher Elementzahlen und deren Komposition. Die zusätzlichen Ausgänge dürfen nicht als bereits hergeleitete CST-Dynamik ausgegeben werden.')
    h('Auch die Materiegleichung verlangt die vollständige Geschichte')
    p('Ein konkretes monotones Beispiel benutzt a≺y≺z mit den Uhren 0, 11/45, 43/90 und Dichtegewichten 0, 0, 1/2. Vor dem Anfügen von z ist die freie Hilfsuhr y stationär. Das neue positive w<sub>z</sub> erfüllt seine Dichtestationarität:')
    eq('Γ<sub>z</sub>=½[(7/30)²−9(43/90)²]=−1')
    p('Trotzdem verändert der neue Beitrag die alte Uhrgleichung:')
    eq('q<sub>y</sub> vorher = 0, &nbsp; q<sub>y</sub> nachher = 7/120 ≠ 0')
    p('Das volle Randwertproblem muss das alte Feld erneut bestimmen. Die drei Uhrableitungen und die neue Dichteableitung sind exakt gegen die vollständige Wirkung geprüft. Das Beispiel beweist keine physikalische Akausalität und setzt die Eulergleichungen nicht mit kanonischen Quantenconstraints gleich.','s')

    page()
    h('5 · Verifikation und Konsequenz für den nächsten Schritt')
    fmt=lambda n:f'{n:,}'.replace(',','.')
    table([
        ['Kontrolle','Umfang / Ergebnis'],
        ['Markierte natürliche Darstellungen',fmt(order['total_natural_marked_representations'])],
        ['Chronologische Kontrollrecords',fmt(order['total_chronological_marked_records'])],
        ['Wirkung vor/nach Umnummerierung',fmt(order['open_and_closed_phase_covariance_checks'])+' offen und geschlossen'],
        ['Uhrschwellen als Ordnungsideale',fmt(order['threshold_ideal_checks'])],
        ['Falscher zusätzlicher 1/e-Faktor',fmt(order['wrong_factor_entries_detected'])+' abweichende Recordgewichte erkannt'],
        ['Wellenpaket-Normen / Effekte','350 / 250 exakte Kontrollen'],
        ['Isolierte Nachrechnung',str(replay['result_files'])+' Ergebnisdateien bytegleich'],
    ],[300,209],padding=4)
    p('Die 5- und 6-Punkt-Uhrgitter und binären Dichtemarken sind eigenständige Kontrollmaße. Sie sind keine zertifizierte Approximation des kontinuierlichen Pfadintegrals. Die allgemeinen Aussagen werden analytisch bewiesen; keine neuen dynamischen 4D-Ensembles oder bezahlten Läufe.','s')
    h('Jetzt braucht es eine Zuordnung zwischen festen Uhrwerten')
    p('Der nächste physikalische Kandidat muss <b>variable Elementzahlen zwischen festgelegten relationalen Uhrwerten</b> zulassen und keine, eine oder mehrere Geburten gemeinsam behandeln. Die Gewichtung, Randzustände und zulässigen Ereignisse müssen aus einer begründeten Quantendefinition stammen. Ein beliebiger positiver Instrumentabschluss genügt nicht.')
    p('<b>Alle acht übergeordneten physikalischen Gates bleiben HOLD.</b> Der konkret geprüfte geschlossene Ein-Geburts-Ansatz ist verworfen. Die physikalische Auswahl und ein globaler Bounce bleiben offen.','s')
    h('Nachrechnung und Primärquellen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/>Python 3.10+, Standardbibliothek; sechs gepinnte Repositoryquellen. Der lokal eingefrorene Plan ist keine externe Präregistrierung.','s')
    p('[1] Brown, Kuchař, Dust as a Standard of Space and Time in Canonical Quantum Gravity (1995). <link href="https://arxiv.org/abs/gr-qc/9409001v1" color="#17445e">arXiv:gr-qc/9409001v1</link>.<br/>[2] Świeżewski, On the properties of the irrotational dust model (2013). <link href="https://arxiv.org/abs/1307.4687v2" color="#17445e">arXiv:1307.4687v2</link>.<br/>[3] Benincasa, Dowker, The Scalar Curvature of a Causal Set, korrigierte Fassung. <link href="https://arxiv.org/abs/1001.2725v4" color="#17445e">arXiv:1001.2725v4</link>.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,title='CST-DUST: Relationale Uhr und Kandidatenprüfung v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':
    main()


