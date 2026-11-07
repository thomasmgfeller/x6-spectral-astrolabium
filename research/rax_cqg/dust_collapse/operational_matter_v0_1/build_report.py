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
NAME = 'CST_DUST_Messmodell_Kontinuierliche_Materiephase_v0_1'
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
    c.drawString(43,35,'CST-DUST · Messmodell und Materiephase v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def outward(value,digits,upper=False):
    x=F(value);scale=10**digits;n=x.numerator*scale
    k=-((-n)//x.denominator) if upper else n//x.denominator
    return (str(k//scale)+','+str(k%scale).zfill(digits))


def interval(bounds,digits=9):
    return '['+outward(bounds[0],digits)+'; '+outward(bounds[1],digits,True)+']'


def main():
    read=lambda name:json.loads((ROOT/'results'/name).read_text())
    moments=read('moments.json');cases=read('continuous_results.json')
    bounds=read('certified_bounds.json');ins=read('instrument.json');replay=read('replay.json')
    p('Messmodell und<br/>kontinuierliche Materiephase','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Kontrollierte Materieintegration. Eine zusätzliche kohärente Messannahme bleibt nötig.')
    p('Die Zahlkanäle des Vorgängers erhalten eine explizite unitäre Realisierung mit einem Hilfssystem. Zugleich wird sichtbar: Ein bloßer Elementzähler kann die Wirkungsphase nicht erkennen. Dafür ist ein kohärenter Filter zwischen Historien derselben Zahl erforderlich.')
    table([
        ['Bearbeiteter Punkt','Ergebnis'],
        ['Operationale Auslese','Vollständiges Messmodell mit Erfolg und Ausfall; zusätzliche kohärente Kopplung ausdrücklich angegeben.'],
        ['Kontinuierliche Materiephase','Uhr- und Dichtemarken für n=0,1,2 integriert; Amplitudenrest unter 1,65·10<super>−14</super>.'],
        ['Höhere Elementzahlen','Feldphasen ab n=3 noch offen; ihre Wirkung wird über Normmassen sicher eingeschlossen.'],
        ['Wiederholbarkeit','36 Parameterfälle; sechs bytegleich reproduzierte Ergebnisdateien.'],
    ],[180,329])
    h('Der neue quantitative Befund')
    p('Eine nichtverschwindende Materiephase hebt im geprüften Zwei-Geometrien-Referenzfall einen zuvor vollständig dunklen Ausgang auf. Der Effekt wird im kontinuierlichen Maß berechnet. Seine Fehlerschranke stammt aus exakten Momenten und einem analytischen Restglied.')
    p('<b>Alle acht physikalischen Gates: HOLD.</b> Das Messmodell setzt kohärenten Zugriff auf Historien voraus. Es wählt weder einen realen Detektor noch eine kosmologische Endrandbedingung aus und leitet keinen Bounce her.','s')
    p('Basis: Main nach PR 254, Commit 35a0d886c4a7ca1d639f09b2933ffeb6c255ad9e. Vollständige Herleitung, rationale Zertifikate und Nachrechnung im Prüfpaket.','s')

    page()
    h('1 · Was über eine reine Zahlmessung hinausgeht')
    p('Ein reiner Elementzähler hat Effekte Π<sub>n</sub>. Sie kommutieren mit jeder lokalen Wirkungsphase exp(iθ). Ihre Ausgänge sind daher phasenblind. Das gilt ebenso für alle Effekte, die in der vollständigen Recordbasis diagonal sind.')
    eq('⟨exp(iθ)b, Π<sub>n</sub> exp(iθ)b⟩ = ⟨b,Π<sub>n</sub>b⟩')
    p('Die kohärente Auslese ergänzt innerhalb jedes Zahlsektors einen normierten Randvektor b<sub>n</sub> und einen Filter:')
    eq('E<sub>n</sub>=|b<sub>n</sub>⟩⟨b<sub>n</sub>|, &nbsp; F<sub>n</sub>=Π<sub>n</sub>−E<sub>n</sub><br/>Σ<sub>n</sub>(E<sub>n</sub>+F<sub>n</sub>)=I')
    p('E und F sind orthogonale Projektoren. Als Krausoperatoren liefern sie eine konkrete lineare, vollständige Messrealisierung. Erfolg und Ausfall behalten jeweils die Zahl n als Ausgang.')
    h('Eine explizite Zeigerkopplung')
    eq('U=Σ<sub>j</sub>P<sub>j</sub> ⊗ S<sub>j</sub>, &nbsp; U†U=UU†=I')
    p('P<sub>j</sub> nummeriert die orthogonalen Erfolgs-/Ausfallprojektoren; S<sub>j</sub> sind unitäre Verschiebungen des Hilfszeigers. Aus dem vorbereiteten Zeigerzustand |0⟩ liest Ergebnis j genau den Krausoperator P<sub>j</sub> aus. Eine rationale 16×16-Kontrolle bestätigt beide Unitaritätsrichtungen und alle vier Ausgänge.')
    h('Ignorierte Ergebnisse können den Zustand verändern')
    table([
        ['Zwei Geometrien derselben Zahl','Vorher','Nach ignorierter Filterauslese'],
        ['Scharfer erster Geometrierecord','(1,0)','Recorddiagonale (1/2,1/2)'],
        ['Elementzahlverteilung','n sicher','Unverändert'],
    ],[224,90,195],padding=6)
    p('Die Funktionalidentität des Vorgängers betrifft vor der Endauslese definierte Historienfragen. Sie beweist keine Identität des nichtselektiven Nachmesskanals. Die abstrakte Zeigerkopplung beweist außerdem noch keine physikalische Verfügbarkeit des kohärenten Filters.','s')

    page()
    h('2 · Die kontinuierlichen Feldvariablen bleiben erhalten')
    p('Die normierte Uhr s liegt im festen Intervall (0,h); die ursprüngliche Uhr ist T=−2+4s. Das Dichtemaß enthält sowohl ein Atom bei null als auch einen kontinuierlichen Anteil:')
    eq('ν(dw)=½δ<sub>0</sub>(dw)+½1<sub>(0,1)</sub>(w)dw<br/>d<sub>0</sub>=1, &nbsp; d<sub>k</sub>=⟨w<super>k</super>⟩=1/[2(k+1)] für k≥1')
    p('Die Materiewirkung ist bei festen Uhren linear in den Dichtemarken: S<sub>d</sub>=−Σ<sub>j</sub>w<sub>j</sub>a<sub>j</sub>. Deren charakteristische Funktion kann exakt integriert werden:')
    eq('χ(t)=½+½(1−exp(−it))/(it), &nbsp; χ(0)=1<br/>⟨exp(iμS<sub>d</sub>)⟩<sub>w</sub>=∏<sub>j</sub>χ(μa<sub>j</sub>)')
    p('Das Atom darf nicht entfallen: Ohne seinen Beitrag wäre χ(0)=1/2 statt eins. Eine normalisierte uniforme Ersatzverteilung würde das Modell ebenfalls verändern, bereits im Mittelwert ⟨w⟩.')
    h('Zwei Geometrien bis zur Elementzahl zwei')
    p('Mit s=hx ist für ein Element a<sub>1</sub>=1/2+4h²x². Für zwei Elemente gilt 0&lt;x<sub>1</sub>&lt;x<sub>2</sub>&lt;1 mit normierter Uhrdichte 2. Der Anfangsanker bleibt in der Wirkung enthalten.')
    eq('a<sub>1</sub>=½+4h²x<sub>1</sub>²<br/>a<sub>2,anti</sub>=½+4h²x<sub>2</sub>²<br/>a<sub>2,chain</sub>=½+4h²x<sub>1</sub>²−8h²x<sub>1</sub>x<sub>2</sub>−32h²x<sub>2</sub>²')
    p('Die Gravitationswerte sind G=S<sub>g</sub>−1=0 für die Antikette und G=9 für die Kette. Die vollständige Zwei-Element-Materiewirkung lautet −w<sub>1</sub>a<sub>1</sub>−w<sub>2</sub>a<sub>2</sub>. 390 rationale Kontrollen bestätigen die Übereinstimmung mit der geerbten vollständigen Wirkung.')
    p('Die kontinuierlichen Integrale sind keine Auswertung des früheren Vier-Uhr-Gitters. Dieses Paket arbeitet mit dem vollständigen geordneten Uhrgebiet und dem erklärten gemischten Dichtemaß.','s')

    page()
    h('3 · Exakte Momente liefern eine analytische Fehlerschranke')
    p('Die Dichtemomente und die Uhrintegrale sind rational. Für die normierte Zwei-Uhr-Domäne gilt:')
    eq('2∫<sub>0&lt;x₁&lt;x₂&lt;1</sub>x<sub>1</sub><super>a</super>x<sub>2</sub><super>b</super>dx<sub>1</sub>dx<sub>2</sub><br/>=2/[(a+1)(a+b+2)]')
    p('Die Momente M<sub>k</sub>=⟨S<sub>d</sub><super>k</super>⟩ werden bis k=48 exakt berechnet. Ein zweiter Rechenweg expandiert die volle Vier-Variablen-Wirkung für k≤3 und bestätigt 16 Momente einschließlich der Normierungen.')
    rows=[['h','Geometrie','⟨S<sub>d</sub>⟩','⟨S<sub>d</sub>²⟩']]
    labels={'one':'Ein Element','antichain':'Antikette','chain':'Kette'}
    rows += [[x['h'],labels[x['geometry']],x['moments'][1],x['moments'][2]] for x in moments['records']]
    table(rows,[55,174,140,140],padding=5)
    h('Taylorrest auf der reellen Phase')
    eq('t<sub>48</sub>=Σ<sub>k=0</sub><super>48</super>(iμ)<super>k</super>M<sub>k</sub>/k!<br/>|⟨exp(iμS<sub>d</sub>)⟩−t<sub>48</sub>| ≤ (|μ|M)<super>49</super>/49!')
    p('M ist eine uniforme Schranke für |S<sub>d</sub>| auf dem ganzen Integrationsgebiet. Der größte geprüfte Fall hat M=10 und |μ|=1. Sein Rest ist 10<super>49</super>/49! &lt; 1,65·10<super>−14</super>. Das vorab festgelegte Ziel 10<super>−12</super> ist erfüllt.')
    p('Für eine Amplitudenfehlerschranke ε wird die Sichtbarkeit v=|a|² durch |t|² ± (2ε+ε²), geschnitten mit [0,1], eingeschlossen. Alle Zertifikate verwenden rationale Endpunkte; Berichtintervalle sind nach außen gerundet.')
    p('Diese Schranke kontrolliert ausschließlich die vollständig integrierten Sektoren n≤2. Sie ist nicht als Gesamtfehler einer unbegrenzten Elementzahlsumme auszugeben.','s')

    page()
    h('4 · Die Materiephase verändert den kohärenten Ausgang')
    p('Bei n=2 werden die beiden Geometrien innerhalb desselben Zahlkanals kohärent zusammengeführt:')
    eq('a<sub>2</sub>(g,μ)=[a<sub>anti</sub>(μ)+exp(i9g)a<sub>chain</sub>(μ)]/2<br/>v<sub>2</sub>=|a<sub>2</sub>|²')
    p('Der Scan umfasst h=1/4 und 1/2, α=1 und 2, g=0,π/18,π/9 sowie μ=0,1/4,1: insgesamt 36 Fälle. Die Faktoren exp(i9g) sind dabei exakt 1, i oder −1.')
    rows=[['g bei h=1/2','v<sub>2</sub> bei μ=0, exakt','v<sub>2</sub> bei μ=1, eingeschlossen']]
    for gi,g in enumerate(['0','1/18','1/9']):
        x=next(x for x in cases['cases'] if x['alpha']==1 and x['h']=='1/2' and x['mu']=='1' and x['g_over_pi']==g)
        rows.append([['0','π/18','π/9'][gi],['1','1/2','0'][gi],interval(x['number_visibility_intervals'][2],12)])
    table(rows,[100,159,250],padding=7)
    h('Ein dunkler Referenzausgang wird wieder positiv')
    x=next(x for x in cases['cases'] if x['alpha']==1 and x['h']=='1/2' and x['mu']=='1' and x['g_over_pi']=='1/9')
    p('Bei μ=0 ist der Kanal für g=π/9 vollständig destruktiv. Mit μ=1 ergibt die kontinuierliche Rechnung das strikt positive Intervall:')
    eq('v<sub>2</sub> ∈ '+interval(x['number_visibility_intervals'][2],15))
    p('Der Effekt folgt aus den unterschiedlichen Materiephasenmitteln der zwei Geometrien. Er ist ein Ergebnis des festgehaltenen Referenzfilters und der erklärten Präparation. Er ist weder ein Nachweis gravitativer Rückwirkung noch einer Singularitätsauflösung.')
    h('Welche Modellentscheidung verändert α?')
    eq('V<sub>n</sub>=E<sub>n</sub>h<super>n</super>/n!, &nbsp; b<sub>n</sub>=1/√V<sub>n</sub><br/>c<sub>n</sub>=f<sub>α</sub>(n)²V<sub>n</sub>')
    p('Innerhalb eines festen n kürzt sich das Zahlgewicht aus b<sub>n</sub> heraus. Die Sichtbarkeit v<sub>n</sub> und das Zahlkanal-Instrument sind bei festem h unabhängig von α. α verändert die Gewichte c<sub>n</sub> der Präparation zwischen verschiedenen Zahlen.')

    page()
    h('5 · Höhere Elementzahlen bleiben eine eigene Unsicherheit')
    p('Die Normmassen bis n=6 sind exakt bekannt, auch wenn ihre Materiephasen ab n=3 noch nicht integriert sind. Für den verbleibenden Normrest gilt:')
    eq('0≤Z<sub>∞</sub>−Z<sub>6</sub>≤δ<sub>6</sub>=h<super>7</super>/7! /(1−h/8)<br/>Z<sub>max</sub>=Z<sub>6</sub>+δ<sub>6</sub>, &nbsp; R<sub>max</sub>=Z<sub>max</sub>−Z<sub>2</sub>')
    p('Jeder noch unbekannte Zahlkanal hat Sichtbarkeit zwischen null und eins. Mit S<sub>L</sub> und S<sub>U</sub> als gewichteten Erfolgsgrenzen der integrierten Sektoren folgt:')
    eq('S<sub>L</sub>/Z<sub>max</sub> ≤ p<sub>count,∞</sub> ≤ (S<sub>U</sub>+R<sub>max</sub>)/Z<sub>max</sub>')
    rows=[['h','α','Erfolgsintervall bei g=0, μ=1','n≥3-Masse, obere Grenze']]
    for hs in ['1/4','1/2']:
        for alpha in [1,2]:
            x=next(x for x in bounds['cases'] if x['h']==hs and x['alpha']==alpha and x['g_over_pi']=='0' and x['mu']=='1')
            rows.append([hs,alpha,interval(x['count_success_infinite_interval']),outward(x['unintegrated_n_ge_3_probability_upper'],9,True)])
    table(rows,[48,30,275,156],padding=6)
    p('Die vier Erfolgsintervalle liegen strikt unter dem phasenfreien Wert eins. Die α-Intervalle sind bei jeder der zwei Uhrdauern disjunkt. Das belegt die Abhängigkeit von der erklärten Präparation; ein physikalisch richtiger α-Wert ist dadurch nicht ausgewählt.')
    table([
        ['Fehlerquelle','Behandlung'],
        ['Uhr-/Dichteintegration bei n≤2','Exakte Momente und Taylorrest'],
        ['Feldphasen bei n=3 bis 6','Exakte Normmassen, Sichtbarkeiten in [0,1]'],
        ['Alle n&gt;6','Analytischer Normrest δ<sub>6</sub>'],
    ],[215,294],padding=6)
    p('R<sub>max</sub> ist größer als δ<sub>6</sub>: Es umfasst auch die noch nicht integrierten n=3,...,6. Die derzeitige Breite der Gesamtintervalle stammt überwiegend aus diesen fehlenden Feldphasen, nicht aus dem Taylorrest.','s')

    page()
    h('6 · Nachrechnung und verbleibende physikalische Auswahl')
    table([
        ['Prüfbaustein','Ergebnis'],
        ['Explizite Zeigerkopplung',str(ins['unitary_dimension'])+'×'+str(ins['unitary_dimension'])+' unitär; vier vollständige Krausausgänge'],
        ['Vollständige Wirkungsformeln',str(moments['action_polynomial_checks'])+' exakte Punktkontrollen'],
        ['Zweiter Integrationsweg',str(moments['independent_low_order_moment_checks'])+' übereinstimmende niedrige Momente'],
        ['Kontinuierliche Parameterfälle',str(len(cases['cases']))+' mit rationalen Zertifikaten'],
        ['Isolierter Replay',replay['isolated_replay']+'; sechs bytegleiche Ergebnisdateien'],
    ],[235,274],padding=6)
    p('Der Plan wurde lokal nach dem analytischen Entwurf und vor der Implementierung eingefroren. Sechs Repositoryquellen sind auf den Ausgangscommit gepinnt. Die Nachrechnung ist Wiederholbarkeit derselben Implementierung, keine externe Replikation oder formale Beweiszertifizierung.')
    h('Was als Nächstes wissenschaftlich zählt')
    p('Quantitativ lohnt die kontrollierte Integration der Feldphasen ab n=3: Sie begrenzt derzeit die Aussagekraft der unbegrenzten Summe. Physikalisch bleibt zu begründen, warum kohärenter Zugriff auf vollständige Historien, dieses Dichtemaß und diese Endrandwahl verfügbar oder dynamisch ausgezeichnet sein sollten.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.</b> Die unitäre Messdilatation ist kein abgeleitetes CST-Wechselwirkungsgesetz. Kein globaler Bounce und kein Innen-/Außenraumanschluss wurden hergeleitet.','s')
    h('Nachrechnen und einordnen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/><font name="DVM">python3 -B verify_package.py</font>','s')
    p('[1] Preskill, <i>Quantum Information, Chapter 3: Measurement and Evolution</i> (2018). <link href="https://www.preskill.caltech.edu/ph219/chap3_15.pdf" color="#17445e">Caltech-Vorlesungsnotizen</link>.<br/>[2] Paris, <i>The modern tools of quantum mechanics</i>, Eur. Phys. J. ST 203, 61 (2012). <link href="https://arxiv.org/abs/1110.6815v2" color="#17445e">arXiv:1110.6815v2</link>.<br/>Kontext für Messinstrumente und unitäre Dilatation; die konkrete CST-Referenzwahl und die Integrationsbeweise stehen in DERIVATION.md.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: Messmodell und kontinuierliche Materiephase v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


