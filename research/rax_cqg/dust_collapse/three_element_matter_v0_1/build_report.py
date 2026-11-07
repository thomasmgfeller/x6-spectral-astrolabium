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
NAME = 'CST_DUST_Drei_Elemente_Kontinuierliche_Materiephase_v0_1'
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
    c.drawString(43,35,'CST-DUST · Drei-Element-Sektor v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def outward(value,digits,upper=False):
    x=F(value);scale=10**digits;n=x.numerator*scale
    k=-((-n)//x.denominator) if upper else n//x.denominator
    return (str(k//scale)+','+str(k%scale).zfill(digits))


def interval(bounds,digits=9):
    return '['+outward(bounds[0],digits)+'; '+outward(bounds[1],digits,True)+']'


def main():
    read=lambda name:json.loads((ROOT/'results'/name).read_text())
    controls=read('geometry_controls.json');cert=read('quadrature_certificates.json')
    amplitudes=read('three_element_amplitudes.json');cases=read('extended_results.json')['cases']
    tails=read('tail_reduction.json');replay=read('replay.json');verification=read('verification.json')
    p('Kontinuierliche Materiephase:<br/>der Drei-Element-Sektor','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Alle sieben Ordnungen integriert. Der bislang größte Phasenrest wird deutlich kleiner.')
    p('Der nächste quantitative Schritt ist abgeschlossen: Im festgehaltenen Referenzmaß sind nun die kontinuierlichen Uhr- und Dichtemarken aller Drei-Element-Geometrien integriert. Die Rechnung schließt sowohl Integrations- als auch Rundungsfehler ein.')
    table([
        ['Bearbeiteter Punkt','Ergebnis'],
        ['Vollständiger Sektor n=3','Sieben natürliche Ordnungen; 42 Geometrieamplituden; 36 kombinierte Parameterfälle.'],
        ['Zertifizierte Genauigkeit','Einzelgeometrie-Quadraturrest unter 6,50·10<super>−12</super>; Ziel 10<super>−10</super> erfüllt.'],
        ['Verbleibende Phasenunsicherheit','Obere Schrankenmasse gegenüber n≥3 um 91,36 bis 99,44 % reduziert; Rest beginnt jetzt bei n=4.'],
        ['Nachrechnung','Sechs Ergebnisdateien im isolierten Replay bytegleich reproduziert.'],
    ],[175,334])
    h('Der wissenschaftliche Gewinn')
    p('Die Intervalle für die unbegrenzte Elementzahlsumme werden erheblich enger. Alle 36 neuen Zahlkanal-Erfolgsintervalle liegen innerhalb der bisherigen Grenzen. Eine nur scheinbar genaue Rechnung mit unkontrolliert abgeschnittener Elementzahl wird damit vermieden.')
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Die Rechnung setzt weiterhin ein bestimmtes Dichtemaß, eine Präparation und kohärenten Zugriff auf Historien voraus. Sie leitet weder einen physikalischen Detektor noch Rückwirkung, Bounce oder Innen-/Außenraumanschluss her.','s')
    p('Basis: Main nach PR 255, Commit 9869528d008966a88052b65216da14eafce8db6f. Acht byteidentisch gepinnte Quellen; Herleitung und rationale Zertifikate im Prüfpaket.','s')

    page()
    h('1 · Sieben Ordnungen mit kontinuierlichen Feldern')
    p('Die monotone Uhr legt die Reihenfolge der drei neuen Elemente fest. Ein Tupel enthält ihre Vorgänger-Bitmasken. Deshalb gehören sieben natürliche Ordnungen zum Sektor; die fünf unbeschrifteten Isomorphieklassen wären hier keine gleichgewichtige Ersatzsumme.')
    rows=[['Vorgänger-Tupel p','G=S<sub>g</sub>−1']]
    rows += [[str(tuple(x['order'])),x['G']] for x in controls['records'] if x['h']=='1/2']
    table(rows,[320,189],padding=4)
    p('Der Anfangsanker bei T=−2 und w=0 bleibt Teil der Wirkung, wird aber nicht als neues Element gezählt. Mit T=−2+4hx und den Intervallgewichten B=(1,−9,16,−8) gilt:')
    eq('S<sub>d</sub>=−Σ<sub>j</sub>w<sub>j</sub>a<sub>j</sub>, &nbsp; a<sub>j</sub>=½+4h²Σ<sub>y≺j</sub>B<sub>k(y,j)</sub>(x<sub>j</sub>−x<sub>y</sub>)²')
    p('Die Dichtemarken haben das unveränderte normierte Maß ν=½δ<sub>0</sub>+½ Uniform(0,1). Ihre Integration ist analytisch:')
    eq('χ(t)=½+½(1−exp(−it))/(it), &nbsp; χ(0)=1<br/>A<sub>p</sub>(μ)=6∫<sub>0&lt;x₁&lt;x₂&lt;x₃&lt;1</sub>∏<sub>j</sub>χ(μa<sub>j</sub>) d³x')
    h('Ein Würfel mit dem richtigen Gewicht')
    eq('x<sub>1</sub>=u<sub>1</sub>u<sub>2</sub>u<sub>3</sub>, &nbsp; x<sub>2</sub>=u<sub>2</sub>u<sub>3</sub>, &nbsp; x<sub>3</sub>=u<sub>3</sub><br/>J(u)=6u<sub>2</sub>u<sub>3</sub>², &nbsp; ∫<sub>[0,1]³</sub>J(u)d³u=1')
    p('Die Transformation erhält das vollständige kontinuierliche Uhrmaß. Die Integrationspunkte sind ein Rechenverfahren mit Restglied, keine neue diskrete Feldverteilung.','s')

    page()
    h('2 · Zwei getrennte Fehler: Quadratur und Arithmetik')
    p('Für jede Würfelkoordinate ist die reelle Phase θ=μS<sub>d</sub> höchstens quadratisch. Exakte Bernstein-Koeffizienten begrenzen |θ′|≤D und |θ″|≤2A auf der gesamten Uhr-/Dichtedomäne. Aus der Ableitungsrekursion folgt:')
    eq('H<sub>0</sub>=1, &nbsp; H<sub>1</sub>=D<br/>H<sub>k</sub>=D H<sub>k−1</sub>+2A(k−1)H<sub>k−2</sub>')
    p('Die H<sub>k</sub> begrenzen die Ableitungen von exp(iθ). Die positive Dichteintegration vergrößert diese Grenzen nicht. Die Ableitungen des Jacobians werden ausdrücklich mitgerechnet.')
    h('Analytischer Gaußrest')
    eq('C<sub>q</sub>=(q!)⁴ / [(2q+1)((2q)!)³]<br/>|A<sub>p</sub>−Q<sub>p</sub>| ≤ Σ<sub>j</sub>C<sub>qⱼ</sub>B<sub>2qⱼ,j</sub>')
    p('Die positive Peano-Kern-Darstellung kontrolliert auch komplexe Integranden. Positive normierte Gaußgewichte erlauben die Addition der Koordinatenfehler. Die Punktzahlen werden allein aus diesen Grenzen ausgewählt.')
    rows=[['h','μ','Punkte je Koordinate','Gesamtpunkte']]
    rows += [[x['h'],x['mu'],' × '.join(map(str,x['orders'])),x['evaluations']]
             for x in cert['configurations'] if x['orders']]
    table(rows,[60,60,230,159],padding=5)
    h('Auch Nullstellen und Funktionswerte sind eingeschlossen')
    p('160-Bit-Festkomma-Intervalle runden nach außen. Legendre-Nullstellen werden durch rationale Vorzeichenwechsel zertifiziert; Gleitkommazahlen liefern lediglich Startvorschläge. π, Sinus, Kosinus und χ erhalten analytische Restgrenzen.')
    p('Maximaler Einzelgeometrie-Quadraturrest: &lt;6,50·10<super>−12</super>.<br/>Maximaler eingeschlossener Arithmetik-/Funktionsrest: &lt;1,61·10<super>−37</super>.<br/>Vorgegebenes Gesamtziel je Geometrie: 10<super>−10</super>.','s')
    p('Die Grenzen beruhen auf der Herleitung und Ganzzahlarithmetik. Ein unabhängiger formaler Beweisprüfer wurde nicht eingesetzt. Standardreferenz: NIST DLMF §3.5(v); vollständige Spezialisierung in DERIVATION.md.','s')

    page()
    h('3 · Der neue kohärente Drei-Element-Kanal')
    p('Innerhalb des Zahlsektors werden die sieben Geometrieamplituden kohärent kombiniert. Die Gravitationsphasen sind hier im Allgemeinen keine gaußrationalen Zahlen und werden deshalb ebenfalls eingeschlossen.')
    eq('a<sub>3</sub>(g,μ)=⅐Σ<sub>p</sub>exp(igG<sub>p</sub>)A<sub>p</sub>(μ)<br/>v<sub>3</sub>=|a<sub>3</sub>|²')
    rows=[['p bei h=1/2, μ=1','Re A<sub>p</sub>, ungefähr','Im A<sub>p</sub>, ungefähr']]
    for x in amplitudes['records']:
        if x['h']=='1/2' and x['mu']=='1':
            rows.append([str(tuple(x['order'])),f"{float(F(x['amplitude_center']['re'])):.8f}",f"{float(F(x['amplitude_center']['im'])):.8f}"])
    table(rows,[175,167,167],padding=5)
    p('Die Tabelle zeigt gerundete Amplitudenmittelpunkte. Die vollständigen rationalen Mittelpunkte und separaten Fehlergrenzen stehen in three_element_amplitudes.json.','s')
    h('Sichtbarkeit bei h=1/2')
    rows=[['g','v<sub>3</sub> bei μ=0, ungefähr','v<sub>3</sub> bei μ=1, eingeschlossen']]
    for label,gs in [('0','0'),('π/18','1/18'),('π/9','1/9')]:
        x=next(x for x in cases if x['h']=='1/2' and x['alpha']==1 and x['g_over_pi']==gs and x['mu']=='1')
        z=next(x for x in cases if x['h']=='1/2' and x['alpha']==1 and x['g_over_pi']==gs and x['mu']=='0')
        rows.append([label,f"{float(F(z['number_visibility_intervals'][3][0])):.9f}",interval(x['number_visibility_intervals'][3],11)])
    table(rows,[55,184,270],padding=6)
    p('Bei g=π/9 unterdrückt μ=1 den Drei-Element-Ausgang zusätzlich. Das ist eine konditionale Interferenzwirkung des gewählten Filters und der erklärten Präparation. Daraus folgt keine gravitative Rückwirkung.')
    p('α verändert die Präparationsgewichte zwischen Zahlen. Innerhalb eines festen Zahlkanals ist die normierte Auslese weiterhin unabhängig von α.','s')

    page()
    h('4 · Der Rest beginnt jetzt bei vier Elementen')
    p('Die bekannten Normmassen werden bis n=6 exakt summiert. Für n&gt;6 gilt dieselbe analytische Normschranke wie zuvor. Nur die Grenze der vollständig integrierten Feldphasen verschiebt sich von n=2 auf n=3.')
    eq('Z<sub>3</sub>=Σ<sub>n=0</sub><super>3</super>c<sub>n</sub>, &nbsp; c<sub>3</sub>=7h³·2<super>−3α</super>/6<br/>Z<sub>max</sub>=Z<sub>6</sub>+h⁷/[7!(1−h/8)]<br/>R<sub>max</sub>=Z<sub>max</sub>−Z<sub>3</sub>')
    rows=[['h / α','Alte Phasenrestgrenze','Neue Phasenrestgrenze','Reduktion ≈']]
    for x in tails['weight_reductions']:
        rows.append([str(x['h'])+' / '+str(x['alpha']),outward(x['old_phase_tail_probability_upper'],12,True),
                     outward(x['new_phase_tail_probability_upper'],12,True),f"{100*float(F(x['fraction_removed'])):.2f} %"])
    table(rows,[70,152,152,135],padding=6)
    p('Die beiden Grenzen betreffen die normierte obere Schrankenmasse R<sub>max</sub>/Z<sub>max</sub>. Die neue Restmasse umfasst unbekannte Feldphasen bei n=4,...,6 und den gesamten Normrest n&gt;6.','s')
    h('Unbegrenzte Erfolgswahrscheinlichkeit bei g=0, μ=1')
    rows=[['h / α','Neues eingeschlossenes Zahlkanal-Erfolgsintervall']]
    for hs in ['1/4','1/2']:
        for alpha in [1,2]:
            x=next(x for x in tails['cases'] if x['h']==hs and x['alpha']==alpha and x['g_over_pi']=='0' and x['mu']=='1')
            rows.append([hs+' / '+str(alpha),interval(x['count_success_infinite_interval'],12)])
    table(rows,[100,409],padding=6)
    p('Alle 36 neuen Zahlkanal-Intervalle liegen innerhalb der bisherigen. Beim Filter über sämtliche Zahlen wird zusätzlich der Schnitt mit dem weiterhin gültigen alten Intervall genommen; Rohintervall und Schnitt sind beide gespeichert.')
    p('Die verbleibende Gesamtbreite wird von n≥4 bestimmt. Eine noch höhere Genauigkeit derselben n=3-Quadratur würde diesen Engpass praktisch nicht verbessern.','s')

    page()
    h('5 · Prüfungen einschließlich eines normierungsblinden Fehlers')
    table([
        ['Kontrolle','Ergebnis'],
        ['Vollständige Wirkung und Inkremente','3780 rationale Vergleiche bestanden'],
        ['Würfel- und geordnete Integration','56 niedrige Momente exakt gleich'],
        ['Brücke zu n=1 und n=2','Drei Vergleiche mit den früheren exakten Momentreihen innerhalb beider Fehlergrenzen'],
        ['Gaußregeln','Alle Nullstellen eingeschlossen; positive Gewichte; Monomiale bis Grad 2q−1 geprüft'],
        ['Intervall-Arithmetik','95 rationale Rechenkontrollen, fünf Quadranten und χ(0) geprüft'],
        ['Unbegrenzte Zahlkanal-Intervalle','36 Inklusionen in die Vorgängerintervalle'],
        ['Isolierter Replay',replay['isolated_replay']+'; sechs Ergebnisdateien bytegleich'],
    ],[220,289],padding=6)
    h('Eine korrekte Normierung allein reicht nicht')
    p('Wird nur der variable Jacobianfaktor weggelassen, bleibt fälschlich die Dichte 6; die Normierung erkennt den Fehler. Wird dagegen der gesamte Jacobian durch eins ersetzt, ist das falsche Würfelmaß wieder normiert.')
    eq('Antikette, h=½:<br/>⟨S<sub>d</sub>⟩<sub>richtig</sub>=−5/8, &nbsp; ⟨S<sub>d</sub>⟩<sub>ohne gesamten Jacobian</sub>=−107/216')
    p('Diese zweite Negativkontrolle fällt erst beim Materiemoment durch. Deshalb wurden neben Normierungsprüfungen unabhängige niedrige Momente aufgenommen. Auch ein fehlender Ordnungsfaktor und eine fehlende natürliche Ordnung werden zurückgewiesen.')
    p('Der Replay berechnet alle neuen Integrale erneut. Er übernimmt nur die gepinnten Vorgängerquellen und den eingefrorenen Plan. Er belegt Wiederholbarkeit dieser Implementierung, keine externe wissenschaftliche Replikation.','s')

    page()
    h('6 · Was damit geschlossen ist – und was physikalisch offen bleibt')
    p('Die Materieintegration des gesamten Drei-Element-Sektors ist unter den festgehaltenen Annahmen abgeschlossen. Quadraturfehler, Rundungsfehler, Normmassen n=4,...,6 und der Rest n&gt;6 werden getrennt ausgewiesen.')
    table([
        ['Nächster Gegenstand','Wissenschaftliche Aufgabe'],
        ['Quantitative Fortsetzung','Den vollständigen n=4-Sektor erst nach einem Kostenbudget bearbeiten. Der Nutzen wäre eine weitere Verengung der unbekannten Phasenmasse.'],
        ['Physikalische Auswahl','Das Dichtemaß, den kohärenten Zugriff auf vollständige Historien und die Endrandwahl aus einer physikalischen CST-Amplitude begründen.'],
        ['Dynamische Aussage','Erst mit ausgewählter Amplitude und Zustands-/Randdeutung können klassische Korrespondenz, Rückwirkung und globale Konsistenz neu bewertet werden.'],
    ],[165,344],padding=7)
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION: HOLD.</b> Weder eine Zahlgewichtung noch ein gut kontrollierter kohärenter Filter ersetzt die fehlende physikalische Auswahl.')
    h('Nachrechnung')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/><font name="DVM">python3 -B verify_package.py</font>','eq')
    p('Die wissenschaftliche Rechnung verwendet ausschließlich die Python-Standardbibliothek. Das Prüfpaket enthält Quellen, eingefrorenen Plan, vollständige Herleitung, rationale Zertifikate, Bericht und SHA-256-Manifest. Die PDF-Erzeugung benötigt ReportLab und DejaVu Sans.','s')
    h('Referenz und Herkunft')
    p('[1] <link href="https://dlmf.nist.gov/3.5#v" color="#17445e">NIST DLMF §3.5(v)</link>, insbesondere (3.5.19) und (3.5.21): Standardrest der Gaußquadratur. Geprüft am 7. November 2026. Die spezifische Bernstein-/Ableitungsabschätzung und Fehlerfortpflanzung stehen in DERIVATION.md.','s')
    p('[2] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/255" color="#17445e">X6, PR 255</link>: geerbtes Messmodell, kontinuierliches Dichtemaß und zertifizierte Sektoren n≤2. Herkunftscommit und Git-Blob-Identitäten aller acht Eingaben stehen in inputs/provenance.json.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: kontinuierlicher Drei-Element-Sektor v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


