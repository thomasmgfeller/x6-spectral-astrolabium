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
NAME = 'CST_DUST_Normpfad_Kohaerenter_Quotient_v0_1'
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
    c.drawString(43,35,'CST-DUST · Normpfad und Quotient v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def main():
    p('Normpfad und<br/>kohärenter Quotient','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Positive Hilfsnormen existieren. Die Kohärenz stellt weitere Bedingungen.')
    p('Die vollständige Vergangenheit erlaubt <b>positive Normpfade für beliebig viele Wachstumsschritte</b>. Eine explizite Familie hält die bisherigen Fortsetzungsamplituden unverändert und ist bei passender Endwahl exakt unabhängig vom Endhorizont. Die Norm ist damit mathematisch möglich, aber nicht physikalisch ausgewählt.')
    table([
        ['Frage','Ergebnis'],
        ['Existiert eine positive diagonale Hilfsnorm?','Ja. Vollständige Klassifikation über konsistente positive Zylindermaße.'],
        ['Ist sie durch Positivität und Labelinvarianz eindeutig?','Nein. Verschiedene Parameter ergeben verschiedene relative Normen.'],
        ['Trägt diese Klasse die unveränderte kohärente Endsumme gleichmäßig beschränkt?','Nein. Eine allgemeine untere Normschranke divergiert mit der Elementzahl.'],
        ['Genügt ein diagonales Produkt nach kohärenter Labelidentifikation?','Im unmarkierten Referenzsektor nein, bereits bei zwei nach drei Elementen.'],
    ],[190,319])
    h('Ein konkreter weiterer Weg bleibt offen')
    p('Nichtdiagonale positive Produkte lassen sich im unmarkierten Quotienten konstruktiv angeben. Ihre freie Wahl erklärt aber weder das physikalische Skalarprodukt noch die erlaubten Ereignisse. Die vollständige markierte Feldtheorie ist damit noch nicht quotientiert.')
    p('<b>Alle acht physikalischen Prüfgates bleiben HOLD.</b> Kein allgemeines No-go für CST, kein physikalisches unendliches Quantenmaß, kein Junction-Gesetz und kein Nachweis eines globalen Bounce oder einer Singularitätsauflösung.','s')
    p('Basis: Main 573084d007ae96d82eb6c241df6ae1d572523418, nach PR 249. Allgemeine Beweise, Quellen und exakte Kontrollen stehen im Prüfpaket.','s')

    page()
    h('1 · Die positiven diagonalen Normpfade sind klassifiziert')
    p('Die geerbte Fortsetzung bewahrt alle alten Felder und trägt den Faktor r=e(P)/e(P′) sowie die Wirkungsphase. e(P) zählt die linearen Erweiterungen der inneren Ordnung. Für geometrieabhängige, feldunabhängige positive Gewichte und normierte Feldmaße ist die Isometrie genau:')
    eq('h<sub>m</sub>(P)=Σ<sub>Kind P′</sub>[e(P)/e(P′)]² h<sub>m+1</sub>(P′)')
    p('Nach Division durch e(P)² wird daraus die Konsistenzregel eines positiven Zylindermaßes. Bei h₀=1 gilt auf jeder Stufe Σμ=1:')
    eq('h<sub>m</sub>(P)=e(P)² μ<sub>m</sub>(P), &nbsp; μ<sub>m</sub>(P)=Σ<sub>Kind P′</sub>μ<sub>m+1</sub>(P′)')
    h('Eine explizite Familie aus bekannter transitiver Perkolation')
    p('Seien L die Linkzahl, R die Relationszahl und 0&lt;p&lt;1. Die bekannte Perkolationsverteilung [1] liefert ein Hilfsbeispiel:')
    eq('μ<sub>m</sub><super>(p)</super>(P)=p<super>L(P)</super>(1−p)<super>m(m−1)/2−R(P)</super>')
    p('Unabhängig gesetzte Vorwärtskanten mit anschließender transitiver Hülle ergeben genau diese Formel: Links müssen vorhanden sein, unvergleichbare Paare fehlen, transitive Zusatzkanten sind frei. Alle zulässigen Ordnungen haben positives Gewicht. Die äußeren Anker werden dabei nicht zufällig perkoliert.')
    table([['p','h₂(Kette) / h₂(Antikette)'],['1/4','1/12'],['1/2','1/4'],['3/4','3/4']], [120,389],padding=5)
    p('Für jedes gewählte p liefert der Rückzug des passenden h<sub>M</sub> exakt dasselbe h<sub>m</sub> bei jedem M≥m. Die verschiedenen relativen Normen in der Tabelle lassen sich durch keine gemeinsame Gesamtnormierung angleichen.')
    p('17.118 endliche Rückzugskontrollen bestätigen die Identität. Sie ist allgemein bewiesen; ein physikalischer Wert von p oder eine vierdimensionale Staubdynamik wird nicht ausgewählt. Für die anderen Endwahlen 1 und 1+R ist kein Grenzwertsatz bewiesen.','s')

    page()
    h('2 · Die kohärente Endsumme ist nicht gleichmäßig beschränkt')
    p('Die ursprüngliche Endkontraktion summiert die Amplituden über alle natürlichen Ordnungen und integriert die Felder. Ihre Randphase b hat Betrag eins. Der Faktor 1/e(P) steckt bereits in den fortgesetzten Amplituden:')
    eq('ℓ<sub>m</sub>(ψ)=Σ<sub>P</sub>∫b(P,ξ)ψ(P,ξ)dν<sub>P</sub>(ξ), &nbsp; |b|=1')
    p('Für jede normalisierte positive diagonale Norm aus der erklärten Klasse gilt exakt:')
    eq('‖ℓ<sub>m</sub>‖²=Σ<sub>P</sub>1/h<sub>m</sub>(P)<br/>‖ℓ<sub>m</sub>‖ ≥ Σ<sub>P</sub>1/e(P) ≥ 2<super>⌊m/2⌋⌈m/2⌉</super>/m! → ∞')
    p('<b>Beweis:</b> Der Riesz-Repräsentant liefert die erste Gleichung. Cauchy-Schwarz mit Σμ=1 liefert die erste Ungleichung. Eine Zweischichtordnung mit beliebigen unteren-zu-oberen Kanten hat 2<super>⌊m/2⌋⌈m/2⌉</super> Möglichkeiten, jeweils e(P)≤m!. Der quadratische Exponent wächst schneller als log(m!).')
    table([
        ['m','Untere Schranke für ‖ℓₘ‖','Art der Schranke'],
        ['3','19/6','Vollständige exakte kleine Summe'],
        ['6','14447/80 = 180,5875','Vollständige exakte kleine Summe'],
        ['16','&gt; 8,8 × 10⁵','Allgemeine Zweischichtschranke'],
        ['32','&gt; 4,4 × 10⁴¹','Allgemeine Zweischichtschranke'],
    ],[40,205,264])
    h('Was damit ausgeschlossen ist')
    p('Auf den vollständigen erklärten Hilfsräumen gibt es keine gemeinsame beschränkte Endfunktional-Realisierung aller unveränderten ℓ<sub>m</sub>. Dafür wäre eine einheitliche Normschranke notwendig. Auch die zusätzliche Kompatibilität der Endkontraktionen müsste gesondert bewiesen werden.')
    p('Unbeschränkte oder distributionelle Endzustände, begründet eingeschränkte physikalische Räume sowie nichtdiagonale oder feldabhängige Produkte sind nicht ausgeschlossen. Der Satz beweist kein allgemeines Hindernis für jedes unendliche Quantenmaß. Die Zahlen sind Operatornormschranken, keine physikalischen Messwerte.','s')

    page()
    h('3 · Kohärente Labelidentifikation erzeugt Kreuzterme')
    p('Im <b>unmarkierten Geometrie-Referenzsektor</b> werden die teleskopierenden Wirkungsphasen entfernt und alle natürlichen Beschreibungen eines Isomorphietyps kohärent addiert. Q bezeichnet diese Summe. Die Anzahl von Idealen mit demselben Kindtyp ist unabhängig vom Vertreter; deshalb gilt exakt QV=BQ.')
    p('Die ursprünglichen Endkoeffizienten bleiben 1/|Aut(P)|. Der vollständige markierte Feldquotient wird hier nicht als erledigt ausgegeben. Für Eltern A=Zweierantikette und C=Zweierkette lautet B:')
    table([
        ['Kindtyp mit drei Elementen','aus A','aus C'],
        ['Antikette','1/3','0'],
        ['Kette plus isoliertes Element','4/3','1/3'],
        ['Zwei Minima, ein Maximum','1','0'],
        ['Ein Minimum, zwei Maxima','0','1/2'],
        ['Dreierkette','0','1'],
    ],[329,90,90])
    h('Eine gemeinsame Zukunft verhindert diagonale Isometrie')
    p('Beide verschiedenen Eltern tragen zum Kind „Kette plus isoliertes Element“ bei. Ein strikt positives diagonales Kindprodukt D₃ hat dafür das Gewicht d. Sein Rückzug enthält zwingend:')
    eq('(B†D₃B)<sub>A,C</sub>=(4/3)·d·(1/3)=4d/9 &gt; 0')
    p('Ein diagonales Elternprodukt D₂ hat an dieser Stelle null. Daher können D₂ und D₃ die Fortsetzung auf dem ganzen Elternraum nicht isometrisch machen. Wiederhergestellte geometrische Wirkungsphasen ändern diesen nichtverschwindenden Kreuzterm nur um eine Phase.')
    p('Das widerspricht der zuvor konstruierten Hilfsnorm nicht: Dort bleiben verschiedene natürliche Records orthogonal. Nach der kohärenten Identifikation werden Beiträge zur selben Zukunft zusammengeführt. Das ist ein präziser Referenzbefund, keine nachgewiesene gravitative Anomalie.')
    p('88 Isomorphietypen einschließlich des leeren Typs, 51 Vertreterkontrollen und 87 erhaltene Endkoeffizienten sind exakt geprüft.','s')

    page()
    h('4 · Nichtdiagonale Produkte sind konstruierbar')
    p('Für jeden unmarkierten Eltern-Typ gibt es ein Kind mit einem eindeutigen größten Element. Dessen Entfernung liefert ausschließlich diesen Eltern-Typ; der zugehörige Koeffizient in B ist eins. Das Auswählen dieser Zeilen definiert eine Linksinverse L mit LB=I.')
    p('Für ein beliebiges positiv definites Elternprodukt M und ein positives Komplementprodukt K ergibt sich:')
    eq('M<sub>neu</sub>=L†ML+(I−BL)†K(I−BL)<br/>B†M<sub>neu</sub>B=M')
    p('<b>Positivitätsbeweis:</b> Hat x die Norm null, sind Lx=0 und (I−BL)x=0. Zusammen folgt x=0. Die Isometrie folgt direkt aus LB=I. Diese algebraische Konstruktion kann auf allen endlichen Stufen wiederholt werden.')
    table([
        ['Ausgeführt','Ergebnis'],
        ['K=I und K=2I, jeweils vier Stufen','Acht positive Produkte; Dimensionen 1, 2, 5, 16'],
        ['Zusätzliche explizite 5×5-Matrix','B†M₃B=I₂ exakt; positive rationale LDL-Pivots'],
        ['Allgemeiner Konstruktionssatz','Mathematische Existenz im unmarkierten Referenzsektor'],
        ['Physikalische Auswahl / uniforme Schranken','Offen'],
    ],[240,269])
    h('Das Skalarprodukt bestimmt auch, was messbar sein kann')
    p('Bei nichtdiagonalem M sind die gewöhnlichen Projektoren auf einzelne Geometrietypen im Allgemeinen nicht M-selbstadjungiert. Sie dürfen deshalb nicht ungeprüft als scharfe physikalische Messungen verwendet werden. Zustände, Produkt, Ereignisse und Endkontraktion müssen gemeinsam festgelegt werden.')
    p('Die diagonale Hilfsfamilie besitzt zwar einen Hilbert-Induktivgrenzraum. Für bloße orthogonale Prefix-Records wird der erzeugte Zustand dort zur konstanten Funktion 1; sein Gramfunktional ist das klassische μ(A∩B). Die kohärente Wirkungsphase bleibt in der separat zu behandelnden Endkontraktion.')
    p('Ein abstrakter Hilbert-Grenzraum beweist keine Fortsetzung des ursprünglichen quantalen Vektormaßes [3]. Natürliche Prefix-Ereignisse sind außerdem nicht automatisch kovariante physikalische Ereignisse [2].','s')

    page()
    h('5 · Verifikation und nächste physikalische Entscheidung')
    table([
        ['Kontrolle','Umfang'],
        ['Natürliche Ordnungen m=0,…,6','5.232'],
        ['Unabhängige DAGs mit transitiver Hülle','33.868'],
        ['Rationale Wahrscheinlichkeitsvergleiche','15.696'],
        ['Zylinder- / Normrekursionen','1.224 / 1.224'],
        ['Kompatible Endprodukte zurückgezogen','17.118 exakte Vergleiche'],
        ['Andere Endwahlen','10 endliche Kontrollen'],
        ['Isolierte Nachrechnung','Fünf Ergebnisdateien bytegleich'],
    ],[310,199],padding=4)
    p('Für Endgewicht 1 sinkt das relative Kette-/Antikette-Normverhältnis von 1 bei M=2 auf rund 0,378109 bei M=6; für 1+R von 2 auf rund 0,446933. Dieser endliche Scan beweist keinen Grenzwert. Die kompatible Perkolationsfamilie besitzt dagegen für jedes gewählte p eine exakt bewiesene Horizontunabhängigkeit.')
    h('Nächster Schritt')
    p('<b>Physikalische Zustände und Ereignisse samt Endkontraktion gemeinsam festlegen.</b> Eine konkrete Route ist ein nichtdiagonales Produkt auf vollständig markierten kovarianten Zuständen; eine andere eine kontrollierte distributionelle Endkontraktion auf einem begründeten eingeschränkten Raum. Freie Hilfsgewichte allein ersetzen die physikalische Auswahl nicht.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.</b> Auch ein qualifiziertes Produkt würde die klassische Korrespondenz, die Innen-/Außenraum-Naht und die Regularität nicht ersetzen.','s')
    h('Nachrechnung und Quellen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/>Python 3.10+, nur Standardbibliothek. Sechs Quellen sind bytegleich auf Main nach PR 249 gepinnt. Plan, Quellen und Paket sind gehasht.','s')
    p('Allgemeine Beweise in DERIVATION.md; exakte Ergebnisse in results/. Keine formale Beweisassistentenprüfung. Der vor der Implementierung lokal gehashte Plan ist keine externe Präregistrierung oder blinde Vorhersage.','s')
    p('[1] Rideout, Sorkin, A Classical Sequential Growth Dynamics for Causal Sets, Phys. Rev. D 61, 024002 (2000), arXiv:gr-qc/9904062v3.<br/>[2] Brightwell et al., “Observables” in causal set cosmology, Phys. Rev. D 67, 084031 (2003), arXiv:gr-qc/0210061v2.<br/>[3] Dowker, Johnston, Surya, On extending the Quantum Measure, J. Phys. A 43, 505305 (2010), arXiv:1007.2725v1.','s')
    doc = SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,title='CST-DUST: Normpfad und kohärenter Quotient v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__ == '__main__':
    main()
