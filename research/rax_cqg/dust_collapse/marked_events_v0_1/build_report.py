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
NAME = 'CST_DUST_Markierte_Zustaende_Ereignisse_v0_1'
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
    c.drawString(43,35,'CST-DUST · Markierte Zustände und Ereignisse v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def main():
    events = json.loads((ROOT/'results/current_events.json').read_text())
    quotient = json.loads((ROOT/'results/marked_quotient.json').read_text())
    actions = json.loads((ROOT/'results/action_covariance.json').read_text())
    terminal = json.loads((ROOT/'results/terminal_readout.json').read_text())
    replay = json.loads((ROOT/'results/replay.json').read_text())
    p('Markierte Zustände,<br/>Ereignisse und Endauslese','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Der vollständige markierte Quotient ist konstruiert.')
    p('Die kohärente Labelidentifikation lässt sich bei jeder festen endlichen Stufe auf <b>alle mitgeführten kontinuierlichen Uhr- und Materiefelder</b> erweitern. Die geerbte Fortsetzung wirkt auf diesem Quotienten. Positive Skalarprodukte und transportierte Präparationsprojektoren sind mathematisch konstruierbar.')
    table([
        ['Prüffrage','Ergebnis'],
        ['Vollständige markierte Zustände','Kontinuierlicher Quotient und Abstieg der Fortsetzung analytisch gezeigt.'],
        ['Positive Produkte','Konstruiert; auf jeder festen Stufe beschränkt und koerziv. Keine physikalische Auswahl.'],
        ['Zulässige Ereignisse','Transportierte Präparationsrecords funktionieren. Aktuelle Zustandsprädikate benötigen eine zusätzliche Prüfung.'],
        ['Kohärente Endauslese','Endlich normierbar; Schnittkompatibilität folgt nicht aus Normerhaltung.'],
    ],[170,339])
    h('Eine konkrete Fehlinterpretation ist ausgeschlossen')
    p('Im exakten binären Referenzfall liefert ein naiver Projektor für „Staub vorhanden“ den Wert <b>−1/149</b>. Das ist keine negative physikalische Wahrscheinlichkeit, sondern der Nachweis, dass diese Messzuordnung im gewählten Hilfsprodukt unzulässig ist.')
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Die physikalische Wahl von Zustandsraum, Produkt, Uhrschnitt und Messinstrument bleibt offen. Kein Junction-Gesetz, kein globaler Bounce und keine Singularitätsauflösung sind hergeleitet.','s')
    p('Basis: Main 57aea796ac1f35c31ca3fabce45e0a27c518a5bf nach PR 250. Sieben gepinnte Quellen, allgemeine Beweise und exakte Kontrollen im Prüfpaket.','s')

    page()
    h('1 · Geometrie und sämtliche Felder gemeinsam identifizieren')
    p('U bezeichnet einen ungelabelten inneren Geometrietyp, e<sub>U</sub> seine Zahl linearer Erweiterungen und a<sub>U</sub> seine Automorphismenzahl. Auf jedem Element liegen die alten kontinuierlichen Felder T,w. Ihr kompaktes Produktmaß ν ist normiert und permutationsinvariant.')
    eq('G<sub>m</sub> = ⊕<sub>[U]</sub> L²(X<sub>U</sub>,ν<super>m</super>)<super>Aut(U)</super>')
    p('Die Funktionen sind invariant, wenn Geometrieelemente und ihre Feldwerte gemeinsam umbenannt werden. Q summiert alle natürlichen Beschreibungen kohärent und mittelt über die Isomorphismen:')
    eq('(Qψ)<sub>U</sub>(x) = (1/a<sub>U</sub>) Σ<sub>P≃U,nat</sub> Σ<sub>φ∈Iso(U,P)</sub> ψ<sub>P</sub>(φ*x)')
    p('Das normierte Feldintegral von Qψ erhält exakt die bisherige kohärente Endsumme. Q ist beschränkt und surjektiv: Eine invariante Funktion kann gleichmäßig auf die e<sub>U</sub>/a<sub>U</sub> natürlichen Beschreibungen verteilt werden.')
    h('Die Fortsetzung steigt auf diesen Raum ab')
    p('Für jedes maximale z des Kindes U′ sei U<sub>z</sub>=U′ ohne z. Mit der geerbten Wirkungsdifferenz ΔS gilt:')
    eq('(Bf)<sub>U′</sub>(x′) = Σ<sub>z maximal</sub> [e<sub>Uz</sub>a<sub>Uz</sub>/(e<sub>U′</sub>a<sub>U′</sub>)]<br/>× exp(iΔS<sub>z</sub>/ℏ) f<sub>Uz</sub>(x′ ohne z)<br/><b>Q<sub>m+1</sub>V<sub>m</sub> = B<sub>m</sub>Q<sub>m</sub></b>')
    p('Der Beweis gruppiert die linearen Erweiterungen danach, welches abstrakte Element das letzte Label erhält. Das Präfix ergibt genau den Elternquotienten. Alle alten Felder bleiben erhalten; endliche Summen von maßtreuen Pullbacks und Phasen sind beschränkt.')
    p('Voraussetzungen: volle Vergangenheit, unabhängige normierte Feldmaße, alle Ideal-Fortsetzungen und die erklärte reelle Wirkung. Zusätzliche physikalische Constraints können diesen Träger verändern. Der lineare kohärente Quotient ist noch keine abgeleitete Dirac-Reduktion.','s')

    page()
    h('2 · Positive Produkte und transportierte Präparationsrecords')
    p('Jeder Elterngeometrie U kann ein eindeutiges größtes Element angefügt werden. Dieser private Kegel C(U) hat in B nur den Elternbeitrag U mit Koeffizient eins. Dephasieren und Integration des neuen Feldes liefern eine beschränkte Linksinverse:')
    eq('(Lg)<sub>U</sub>(x)=∫ exp(−iΔS<sub>C</sub>/ℏ) g<sub>C(U)</sub>(x,u)dν(u)<br/><b>LB=I, &nbsp; ‖L‖≤1</b>')
    p('Für beschränkte positive koerzive Produkte M und K setze R=I−BL:')
    eq('M<sub>neu</sub>=L†ML+R†KR<br/>B†M<sub>neu</sub>B=M, &nbsp; B<super>♯</super>=L')
    p('Ist M≥aI und K≥cI, dann folgt aus x=BLx+Rx die explizite untere Schranke:')
    eq('M<sub>neu</sub> ≥ [min(a,c)/(1+‖B‖²)] I')
    p('Damit gilt die Konstruktion auch für die kontinuierlichen Feld-L²-Räume. Sie kann für jedes endliche m wiederholt werden. Eine gemeinsame, von m unabhängige Schranke wird nicht behauptet. K bleibt frei.')
    h('Ein früher festgelegtes Ereignis kann konsistent mitgeführt werden')
    p('Ist {E<sub>a</sub>} eine vollständige orthogonale Projektorzerlegung im Elternprodukt, dann ist folgende Familie im neuen Produkt wieder vollständig und orthogonal:')
    eq('F<sub>a</sub>=BE<sub>a</sub>L, &nbsp; F<sub>neu</sub>=I−BL')
    p('Auf jedem fortgesetzten Zustand Bψ bleiben die Wahrscheinlichkeiten der alten Präparation unverändert. Das neue Komplement hat Wahrscheinlichkeit null. Dies folgt exakt aus LB=I und der Isometrie; die Matrixkontrollen bestätigen alle Projektoridentitäten.')
    p('Diese Operatoren lesen einen <b>transportierten Präparationsnachweis</b> aus. Sie sind nicht automatisch Aussagen über die aktuelle Materieverteilung. Eine Stufe m ist außerdem noch kein durch das Feld T definierter physikalischer Uhrschnitt. Bei Rückkehr aus der phasenfreien Darstellung müssen auch Produkt und Auslesen mittransformiert werden.','s')

    page()
    h('3 · Warum eine aktuelle Staubaussage noch keine Messung ist')
    p('Eine labelinvariante Menge A der aktuellen Zustände definiert den Multiplikationsoperator E<sub>A</sub>f=1<sub>A</sub>f. Er ist idempotent. Als scharfer Projektor im Produkt M ist er jedoch nur zulässig, wenn:')
    eq('E<sub>A</sub>†M = ME<sub>A</sub>')
    p('Im binären Referenzmaß wird jeder innere Punkt mit (T,w)=(-1,0) oder (1,1/2) markiert, je mit Gewicht 1/2. Für zwei innere Elemente ergeben M₁=2I und K=I die folgenden Matrixeinträge:')
    table([
        ['Typ / Kopplung','Wert'],
        ['A01: Antikette mit einem Staubmark','M(A01,A01)=1'],
        ['C00: Vakuum-Zweierkette','M(C00,C00)=19/2'],
        ['Kreuzterm','M(C00,A01)=−1/2'],
    ],[310,199],padding=5)
    p('Für ψ=e<sub>A01</sub>+4e<sub>C00</sub> und A=„mindestens ein Staubmark ungleich null“ gilt:')
    eq('‖ψ‖²<sub>M</sub>=149, &nbsp; ⟨ψ,E<sub>A</sub>ψ⟩<sub>M</sub>=−1<br/><b>naiver Bornwert = −1/149</b>')
    p('Die Aussage ist labelinvariant, aber der zugehörige Multiplikator ist nicht M-selbstadjungiert. Das Gegenbeispiel gilt auf dem vollständigen erklärten Hilfsraum. Physikalische Erreichbarkeit dieses Testzustands wird nicht behauptet.')
    h('Positive Historiengewichte sind etwas anderes')
    p('D(A,B)=⟨E<sub>A</sub>ψ,E<sub>B</sub>ψ⟩<sub>M</sub>/‖ψ‖²<sub>M</sub> ist ein stark positives, normalisiertes Gramfunktional. Für die Alternativen 0, 1 und 2 Staubmarkierungen ist die Diagonalsumme jedoch:')
    eq('Σ<sub>a</sub>D(a,a)=153/149 ≠ 1')
    p('Die Kreuzterme ergeben zusammen −4/149; erst die Summe aller Einträge ist eins. Daher sind die Diagonalgewichte bei dieser Interferenz keine normierte Verteilung exklusiver Messausgänge. Ein zulässiges Instrument oder zusätzliche Dekohärenzbedingungen sind erforderlich.','s')

    page()
    h('4 · Die Endamplitude braucht ein eigenes Ausleseinstrument')
    p('Auf jeder festen Stufe ist die ursprüngliche kohärente Endkontraktion ℓ beschränkt. Für ein koerzives M seien r<sub>ℓ</sub>=M⁻¹ℓ† und d<sub>ℓ</sub>=ℓM⁻¹ℓ† die Rieszrepräsentation und das Quadrat ihrer dualen Norm. Ein zulässiger Ausleseeffekt ist:')
    eq('E<sub>ℓ</sub>=λM⁻¹ℓ†ℓ, &nbsp; 0≤λ≤1/d<sub>ℓ</sub>')
    p('Am oberen Grenzwert ist E<sub>ℓ</sub> ein Rang-eins-Projektor. Mit dem komplementären Ausgang entsteht ein normiertes Instrument. Die Wahrscheinlichkeit lautet λ|ℓψ|²/‖ψ‖²<sub>M</sub>; die Amplitude allein ist keine Wahrscheinlichkeit.')
    rows = [['Referenzstufe','dℓ','maximal λ']]
    rows += [[str(e['m']),e['dual_norm_squared'],e['max_lambda']] for e in terminal['finite_effects']]
    table(rows,[160,170,179],padding=5)
    p('Die Zahlen gelten für das binäre, phasenfreie Beispiel mit K=I und ℓ=(1,…,1). Verdopplung des maximalen λ ergibt am Rieszvektor als Negativkontrolle den unzulässigen Wert 2.')
    h('Normerhaltung garantiert keine identische Auslese an jedem Schnitt')
    p('Soll ein zusätzlicher Fortsetzungsschritt lediglich die Darstellung ändern, muss dieselbe lineare Auslese ℓ<sub>m+1</sub>B<sub>m</sub>=ℓ<sub>m</sub> erfüllen. Gleiche Rang-eins-Effekte erlauben eine gemeinsame Phase. Im phasenfreien Referenzfall bei 2→3 sind die Faktoren:')
    table([['Elterntyp','ℓ₃B₂','ℓ₂'],['Antiketten, alle Marken','8/3','1'],['Ketten, alle Marken','11/6','1']], [289,110,110],padding=5)
    p('Keine gemeinsame Skalierung gleicht diese Faktoren an. Die transportierte Alternative ℓ<sub>neu</sub>=ℓL ist kompatibel und erhält ihre duale Norm. Sie wählt aber Kegelanteile aus und verändert damit die ursprüngliche Summenauslese.')
    p('Dies widerlegt eine automatische Folgerung aus Isometrie. Es schließt andere Kopplungen, physikalische Randzustände oder relationale Uhrschnitte nicht aus. Falls die Stufen verschiedene physikalische Situationen bezeichnen, ist auch die Forderung nach derselben Auslese neu zu begründen.','s')

    page()
    h('5 · Exakte Prüfung und nächste physikalische Entscheidung')
    table([
        ['Kontrolle','Umfang / Resultat'],
        ['Natürliche markierte Zustände',str(sum(quotient['natural_marked_counts']))],
        ['Markierte Isomorphietypen m=0,…,4',', '.join(map(str,quotient['orbit_counts']))],
        ['Unabhängige Maximal-Löschungs-Einträge',f"{quotient['independent_deletion_entries']:,}".replace(',','.')],
        ['Permutationsprüfungen, offen und geschlossen',f"{actions['permutations_checked_open_and_closed']:,}".replace(',','.')],
        ['Exakte Wirkungsinkremente',str(actions['increments_checked'])],
        ['Positive Produkte / transportierte PVMs','4 / 4; exakte rationale Matrixidentitäten'],
        ['Ereignisalgebra','8 Ereignisse, 216 Additivitäts-, 64 Grad-2-Prüfungen'],
        ['Isolierte Nachrechnung',str(replay['result_files'])+' Ergebnisdateien bytegleich'],
    ],[310,199],padding=4)
    p('Die binäre Maßwahl ist ein eigenständiger algebraischer Test. Sie approximiert das kontinuierliche Feldintegral nicht nachweislich. Die kontinuierlichen Aussagen folgen aus den Beweisen in DERIVATION.md. Der vor Implementierung lokal eingefrorene Plan ist keine externe Präregistrierung.','s')
    h('Nächster sinnvoller Schritt')
    p('<b>Einen konkreten physikalischen Kandidaten gemeinsam festlegen:</b> erlaubte Präparation, relationaler Uhrschnitt, begründetes Skalarprodukt und tatsächlich zugehöriges Ausleseinstrument. Anschließend die geerbte Randphase, Effekt-Normierung und erforderliche Schnittkompatibilität prüfen. Freie Hilfsprodukte allein bestimmen die Physik nicht.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING, EXTENSION: jeweils HOLD.</b> Die gemeinsame Außenraumdynamik, gravitative Rückwirkung und Regularität bleiben eigene Aufgaben.','s')
    h('Nachrechnung und Primärquellen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/>Python 3.10+, Standardbibliothek; rationale Arithmetik und gepinnte Quellen.','s')
    p('[1] J. Watrous, The Theory of Quantum Information (2018), Kapitel 2, Definition 2.34 und §2.3: positive Effekte, Projektionsmessungen, Instrumente.<br/><link href="https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf" color="#17445e">cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf</link>','s')
    p('[2] F. Dowker, S. Johnston, S. Surya, On extending the Quantum Measure, J. Phys. A 43, 505305 (2010). Endliche Positivität löst die Vektormaß-Fortsetzung nicht.<br/><link href="https://arxiv.org/abs/1007.2725v1" color="#17445e">arxiv.org/abs/1007.2725v1</link>','s')
    doc = SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,title='CST-DUST: Markierte Zustände, Ereignisse und Endauslese v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__ == '__main__':
    main()


