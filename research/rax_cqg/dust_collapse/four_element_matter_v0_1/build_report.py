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
NAME = 'CST_DUST_Vier_Elemente_Kontinuierliche_Materiephase_v0_1'
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
    c.drawString(43,35,'CST-DUST · Vier-Element-Sektor v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def outward(value,digits,upper=False):
    x=F(value);scale=10**digits;n=x.numerator*scale
    k=-((-n)//x.denominator) if upper else n//x.denominator
    return (str(k//scale)+','+str(k%scale).zfill(digits))


def interval(bounds,digits=9):
    return '['+outward(bounds[0],digits)+'; '+outward(bounds[1],digits,True)+']'


def main():
    read=lambda name:json.loads((ROOT/'results'/name).read_text())
    v=read('verification.json');q=read('quadrature_certificates.json');tails=read('tail_reduction.json')
    cases=read('extended_results.json')['cases'];replay=read('replay.json');controls=read('geometry_controls.json')
    p('Kontinuierliche Materiephase:<br/>der Vier-Element-Sektor','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('40 Ordnungen integriert. Die Restschranken werden nochmals enger.')
    p('Die kontinuierlichen Uhr- und Dichtemarken des gesamten Vier-Element-Sektors sind im geerbten Referenzmaß integriert. Eine vorab festgelegte Kostenentscheidung und ein beschleunigter Intervallkern machen die vollständige Rechnung ohne bezahlten Rechendienst möglich.')
    table([
        ['Bearbeiteter Punkt','Ergebnis'],
        ['Vollständiger Sektor n=4','40 natürliche Ordnungen, 240 Geometrieamplituden und 36 kombinierte Parameterfälle.'],
        ['Zertifizierter Integralfehler','Quadraturrest unter 1,041·10<super>−9</super>, Arithmetikrest unter 1,841·10<super>−12</super>; Amplitudenziel 10<super>−8</super> erfüllt.'],
        ['Verbleibende Phasenmasse','Obere Schranke gegenüber n≥4 um 93,59 bis 99,05 % reduziert; Rest beginnt jetzt bei n=5.'],
        ['Nachrechnung','Sechs Ergebnisdateien im isolierten Replay bytegleich reproduziert.'],
    ],[177,332])
    h('Ein neuer Hinweis für die Arbeitsrichtung')
    p('Bei α=2 stammt jetzt der größte Anteil der verbliebenen oberen Restmasse aus der konservativen Normschranke für n&gt;6. Ihre analytische Schärfung verspricht deshalb mehr Nutzen, bevor weitere Feldintegrale berechnet werden.')
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Maß, kohärenter Historienzugriff und Randwahl sind weiterhin Annahmen. Weder eine physikalische 4D-Dynamik noch Rückwirkung, Bounce oder Junction Law werden hergeleitet.','s')
    p('Basis: Main nach PR 256, Commit e4787d04c78a1da43825dbbac670a0e3dfacee51. Zwölf Quellen sind byteidentisch gepinnt. Die vollständige Herleitung und rationale Zertifikate liegen im Prüfpaket.','s')

    page()
    h('1 · Kostenentscheidung vor der neuen Integralrechnung')
    p('Vier Elemente besitzen 40 natürliche Ordnungen statt sieben bei drei Elementen. Die teure Konfiguration braucht über eine Million Tensorpunkte. Ein bloßes Weiterlaufen der bisherigen Python-Auswertung wäre dafür unnötig aufwendig.')
    table([
        ['Vorgegebenes Budget','Grenze'],
        ['Tensorpunkte je Konfiguration','1 200 000'],
        ['Dichtefunktionsaufrufe über den n=4-Scan','35 000 000'],
        ['Laufzeit des nativen Kerns je Konfiguration','600 Sekunden; Überschreitung führt zum Abbruch'],
        ['Fehler je Geometrieamplitude','≤10<super>−8</super>, davon Quadratur ≤5·10<super>−9</super> und Arithmetik ≤4·10<super>−9</super>'],
    ],[300,209],padding=6)
    h('Aus Ableitungsgrenzen bestimmte Punktzahlen')
    rows=[['h','μ','Punkte je Koordinate','Tensorpunkte']]
    rows += [[x['h'],x['mu'],' × '.join(map(str,x['orders'])),str(x['nodes'])] for x in q['cost_gate']['configurations']]
    table(rows,[50,50,260,149],padding=6)
    p('Gesamt: <b>1 305 984 Tensorpunkte</b>. Nur 24 Dichtepolynome sind verschieden; gemeinsame Auswertung reduziert den Aufwand auf <b>31 343 616 χ-Aufrufe</b>. Gemeinsame Präfixprodukte benötigen 50 komplexe Produkte je Punkt statt 160 separater Produkte.')
    p('Die Kostenentscheidung lautet GO. Alle Läufe blieben innerhalb der erzwungenen Grenzen. Für μ=0 gilt jede Geometrieamplitude exakt eins; eine numerische Integration ist dort unnötig.')
    p('Der Plan wurde nach analytischer Kostenabschätzung und vor neuer Integralrechnung lokal eingefroren. Keine externe Präregistrierung oder blinde Vorhersage wird behauptet. Laufzeiten werden nicht als wissenschaftliche Ergebnisse ausgegeben.','s')

    page()
    h('2 · Gleiches Maß, gleiche Wirkung, kontrollierte Quadratur')
    p('Die Uhr bleibt T=−2+4hx, der Anfangsanker T=−2,w=0. Das Dichtemaß ν=½δ<sub>0</sub>+½ Uniform(0,1) und die vollständigen Intervallgewichte B=(1,−9,16,−8) sind unverändert.')
    eq('S<sub>d</sub>=−Σ<sub>j=1</sub><super>4</super>w<sub>j</sub>a<sub>j</sub>, &nbsp; a<sub>j</sub>=½+4h²Σ<sub>y≺j</sub>B<sub>k(y,j)</sub>(x<sub>j</sub>−x<sub>y</sub>)²<br/>χ(t)=½+½(1−exp(−it))/(it), &nbsp; χ(0)=1')
    p('Die Dichtemarken werden analytisch integriert. Für die geordneten Uhren gilt die Würfeltransformation:')
    eq('x<sub>1</sub>=u<sub>1</sub>u<sub>2</sub>u<sub>3</sub>u<sub>4</sub>, &nbsp; x<sub>2</sub>=u<sub>2</sub>u<sub>3</sub>u<sub>4</sub><br/>x<sub>3</sub>=u<sub>3</sub>u<sub>4</sub>, &nbsp; x<sub>4</sub>=u<sub>4</sub><br/>J(u)=24u<sub>2</sub>u<sub>3</sub>²u<sub>4</sub>³')
    p('Jede einzelne Würfelkoordinate tritt in der reellen Phase θ=μS<sub>d</sub> höchstens quadratisch auf. Die geerbten rationalen Bernstein-Grenzen für |θ′|≤D und |θ″|≤2A liefern:')
    eq('H<sub>0</sub>=1, &nbsp; H<sub>1</sub>=D<br/>H<sub>k</sub>=D H<sub>k−1</sub>+2A(k−1)H<sub>k−2</sub>')
    p('Die Ableitungen des Jacobians werden ausdrücklich mitgerechnet. Der positive Peano-Kern der Gaußregel und positive normierte Gewichte begrenzen den komplexen Tensorfehler durch die Summe der Koordinatenreste.')
    eq('C<sub>q</sub>=(q!)⁴/[(2q+1)((2q)!)³]<br/>|A<sub>p</sub>−Q<sub>p</sub>| ≤ Σ<sub>j</sub>C<sub>qⱼ</sub>B<sub>2qⱼ,j</sub>')
    p('Die Punktzahl wird nur aus diesen Ableitungsgrenzen ausgewählt. Die Integrationspunkte ändern das kontinuierliche Maß nicht. Die geerbten Polynom-, Bernstein- und Gaußroutinen sind bytegleich übernommen.','s')

    page()
    h('3 · Beschleunigung mit eingeschlossener Arithmetik')
    p('Der neue Kern berechnet Intervalle [L,U]/2<super>60</super> mit signierten 128-Bit-Ganzzahlen. Additionen, Subtraktionen und Multiplikationen prüfen den Überlauf. Divisionen werden auch bei negativen Werten ausdrücklich nach außen gerundet.')
    table([
        ['Baustein','Kontrolle'],
        ['Knoten, Gewichte, π','Zuerst geerbte 160-Bit-Zertifikate; Umrechnung auf 60 Nachkommabits nach außen.'],
        ['Sinus, Kosinus, χ','Argumentreduktion und Taylorpolynome mit analytischen Resten; keine libm-Näherung im Integralkern.'],
        ['Überläufe','Abbruch bei jeder erkannten Überschreitung; absichtlicher Überlauf wird im Test zurückgewiesen.'],
        ['Geometriesumme','Rückgabe der eingeschlossenen Intervalle an den geerbten 160-Bit-Code für Gravitationsphasen und Kohärenzsumme.'],
    ],[175,334],padding=7)
    h('Validierung vor der Hauptrechnung')
    p('<b>168</b> signierte rationale Rechenkontrollen bestehen. <b>52</b> Funktionsintervalle schließen die 160-Bit-Referenz ein. Alle <b>28</b> nichttrivialen n=3-Geometrieamplituden des Vorgängers werden erneut berechnet und innerhalb der Summe beider Fehlergrenzen bestätigt.')
    h('Tatsächlich erreichte Fehlergrenzen')
    eq('max ε<sub>Quadratur</sub> &lt; 1,041·10<super>−9</super><br/>max ε<sub>Arithmetik</sub> &lt; 1,841·10<super>−12</super><br/>ε<sub>gesamt</sub> &lt; 10<super>−8</super> je Geometrie')
    p('Die 60 Nachkommabits sind kein Anspruch auf 60 korrekte Ergebnisbits. Entscheidend sind die akkumulierten Intervalle. Der Compiler ist eine neue Nachrechnungsabhängigkeit; sein Quellcode-Eingang ist vollständig enthalten, die Binärdatei wird nur vorübergehend erzeugt.','s')
    p('Die Kontrollen sind keine formale Verifikation des Compilers oder der gesamten Implementierung. Sie ergänzen den analytischen Integrations- und Intervallbeweis.','s')

    page()
    h('4 · Der kohärente Vier-Element-Ausgang')
    p('Die Geometrien werden innerhalb derselben Elementzahl kohärent kombiniert. Der normierte Zahlkanal bleibt unabhängig von α; α verändert die Gewichte der Präparation zwischen verschiedenen Zahlen.')
    eq('a<sub>4</sub>(g,μ)=¹⁄₄₀Σ<sub>p</sub>exp(igG<sub>p</sub>)A<sub>p</sub>(μ)<br/>v<sub>4</sub>=|a<sub>4</sub>|², &nbsp; c<sub>4</sub>=(40h⁴/24)·2<super>−6α</super>')
    h('Sichtbarkeit bei h=1/2')
    rows=[['g','v<sub>4</sub> bei μ=0, ungefähr','v<sub>4</sub> bei μ=1, eingeschlossen']]
    for label,gs in [('0','0'),('π/18','1/18'),('π/9','1/9')]:
        a=next(x for x in cases if x['h']=='1/2' and x['alpha']==1 and x['g_over_pi']==gs and x['mu']=='1')
        b=next(x for x in cases if x['h']=='1/2' and x['alpha']==1 and x['g_over_pi']==gs and x['mu']=='0')
        rows.append([label,f"{float(F(b['number_visibility_intervals'][4][0])):.9f}",interval(a['number_visibility_intervals'][4],10)])
    table(rows,[55,184,270],padding=7)
    p('Die Materiephase verändert die Interferenz der 40 Geometrien. Dies ist ein Ergebnis der erklärten Präparation und des kohärenten Filters. Ein bloßer Elementzähler würde diese Wirkungsphase weiterhin nicht auslesen.')
    h('Unbegrenzter Zahlkanal-Erfolg bei g=0, μ=1')
    rows=[['h / α','Neues eingeschlossenes Erfolgsintervall']]
    for hs in ['1/4','1/2']:
        for alpha in [1,2]:
            a=next(x for x in tails['cases'] if x['h']==hs and x['alpha']==alpha and x['g_over_pi']=='0' and x['mu']=='1')
            rows.append([hs+' / '+str(alpha),interval(a['count_success_infinite_interval'],12)])
    table(rows,[100,409],padding=7)
    p('Alle 36 neuen Zahlkanal-Intervalle liegen innerhalb der bisherigen. Die Sektoren n≤3 wurden samt Fehlern unverändert übernommen. Der phasenfreie Fall g=μ=0 bleibt exakt eins.','s')

    page()
    h('5 · Der Rest beginnt bei fünf Elementen')
    p('Die unbekannten Feldphasen n=5,6 werden über ihre exakte Normmasse begrenzt. Für n&gt;6 bleibt die bisherige analytische Normschranke unverändert, damit der Gewinn der neuen Feldintegration direkt vergleichbar ist.')
    eq('Z<sub>4</sub>=Σ<sub>n=0</sub><super>4</super>c<sub>n</sub>, &nbsp; δ<sub>6</sub>=h⁷/[7!(1−h/8)]<br/>Z<sub>max</sub>=Z<sub>6</sub>+δ<sub>6</sub><br/>R<sub>max</sub>=(Z<sub>6</sub>−Z<sub>4</sub>)+δ<sub>6</sub>')
    rows=[['h / α','Vorher n≥4','Jetzt n≥5','Reduktion ≈']]
    for x in tails['weight_reductions']:
        rows.append([x['h']+' / '+str(x['alpha']),outward(x['old_phase_tail_probability_upper'],12,True),outward(x['new_phase_tail_probability_upper'],12,True),f"{100*float(F(x['fraction_removed'])):.2f} %"])
    table(rows,[70,152,152,135],padding=7)
    p('Die Tabellenwerte sind obere Schranken für R<sub>max</sub>/Z<sub>max</sub>. Sie geben keine gemessene tatsächliche Verteilung der höheren Elementzahlen wieder.','s')
    h('Bei α=2 dominiert nun eine analytische Überabschätzung')
    rows=[['h bei α=2','Anteil δ<sub>6</sub>/R<sub>max</sub>, ungefähr']]
    for hs in ['1/4','1/2']:
        x=next(x for x in tails['cases'] if x['h']==hs and x['alpha']==2)
        share=F(x['normalization_tail_n_gt_6_upper'])/F(x['unintegrated_n_ge_5_mass_upper'])
        rows.append([hs,f'{100*float(share):.2f} %'])
    table(rows,[180,329],padding=7)
    p('Diese Anteile beziehen sich auf die Fehlerschranke. Die geerbte Grenze benutzt nur α≥1 und ist bei α=2 besonders konservativ. Eine α-abhängige kombinatorische Schranke ist deshalb der nächste sinnvolle analytische Kandidat, bevor zusätzliche Feldintegrale gestartet werden.')
    p('Für die kohärente Summe über alle Zahlen werden Rohintervall und Schnitt mit der gültigen Vorgängergrenze getrennt gespeichert. Nichts wird als ausgewertete Feldphase für n≥5 ausgegeben.','s')

    page()
    h('6 · Nachrechnung und physikalische Grenze')
    table([
        ['Kontrolle','Ergebnis'],
        ['Natürliche Ordnungen','40; zwei Enumerationswege liefern dieselbe Menge'],
        ['Vollständige Wirkung und Inkremente','32 400 rationale Kontrollen bestanden'],
        ['Geordnete Domäne und Würfel','320 niedrige Momente exakt gleich'],
        ['Brücke zum Vorgänger','28 Geometrieamplituden innerhalb beider Fehlergrenzen'],
        ['Normierungsblinder Jacobianfehler','Antikette h=1/2: falscher Moment −101/162 statt −5/6 wird zurückgewiesen'],
        ['Isolierter Replay',replay['isolated_replay']+'; sechs Ergebnisdateien bytegleich, einschließlich neuer Kompilation und Integrale'],
    ],[220,289],padding=6)
    h('Nachrechnen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/><font name="DVM">python3 -B verify_package.py</font>','eq')
    p('Benötigt werden Python 3.12 und g++ mit C++17, __int128 und Überlauf-Builtins. Der Replay nutzt nur Quellen, Plan und zwölf gepinnte Vorgängereingaben; keine neuen Ergebnis-Caches. Interne Wiederholbarkeit ist keine externe wissenschaftliche Replikation.','s')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.</b> Die physikalische Begründung des Dichtemaßes, des kohärenten Zugriffs auf Historien und der Endrandwahl bleibt offen.')
    h('Primärquellen und Herkunft')
    p('[1] <link href="https://dlmf.nist.gov/3.5#v" color="#17445e">NIST DLMF §3.5(v)</link>: Gaußquadratur.<br/>[2] <link href="https://gcc.gnu.org/onlinedocs/gcc/Integer-Overflow-Builtins.html" color="#17445e">GCC: Integer Overflow Builtins</link> und <link href="https://gcc.gnu.org/onlinedocs/gcc/_005f_005fint128.html" color="#17445e">128-bit Integers</link>: dokumentierte Compilerfunktionen.<br/>[3] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/256" color="#17445e">X6, PR 256</link>: geerbtes Referenzmaß und zertifizierter n=3-Sektor. Geprüft am 7. November 2026. Spezifische Beweise und Geltungsgrenzen in DERIVATION.md.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: kontinuierlicher Vier-Element-Sektor v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


