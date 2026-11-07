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
NAME = 'CST_DUST_Uhrintervalle_Variable_Elementzahl_v0_1'
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
    c.drawString(43,35,'CST-DUST · Uhrintervalle und variable Elementzahl v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def main():
    read=lambda n:json.loads((ROOT/'results'/n).read_text())
    sew=read('interval_sewing.json');counts=read('counts_norms.json')
    horizon=read('horizon_completion.json');weights=read('weight_alternatives.json')
    entropy=read('entropy_bounds.json');replay=read('replay.json')
    fmt=lambda n:f'{n:,}'.replace(',','.')
    p('Feste Uhrintervalle und<br/>variable Elementzahl','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Eine konsistente Referenz ist konstruiert. Ihre physikalische Auswahl bleibt offen.')
    p('Keine, eine oder mehrere neue Elemente können zwischen festen Materieuhrwerten gemeinsam behandelt werden. Mit vollständiger Vergangenheit ist die Komposition exakt. Die ursprüngliche lokale Historiennorm lässt sich jedoch nicht ohne zusätzliche Gewichtung auf unbegrenzte Elementzahlen erweitern.')
    table([
        ['Geprüfter Baustein','Ergebnis'],
        ['Feste Uhrintervalle, variable Geburtenzahl','Exakte Komposition bei einem gemeinsamen Gesamtzahlregulator.'],
        ['Ungewichtete lokale Historiennorm','Divergent ohne Elementzahlgrenze; analytischer Ausschluss dieses Kandidaten.'],
        ['Explizite Endpunkt-Zahlgewichte','Kontrollierte Summe mit einer uniformen Restschranke.'],
        ['Gemeinsamer Enduhrwert','Normerhaltender und schnittkompatibler Referenztransport.'],
        ['Physikalische Quantendynamik','Nicht ausgewählt: zwei zulässige Gewichte liefern verschiedene Vorhersagen.'],
    ],[185,324])
    h('Was dieser Schritt leistet')
    p('Der offene Übergang von Geburtsnummern zu festen Uhrintervallen ist mathematisch ausgearbeitet. Die erforderlichen zusätzlichen Entscheidungen über Zahlgewicht, Enduhrwert und Ereignisprodukt sind jetzt ausdrücklich sichtbar und prüfbar.')
    p('<b>Acht physikalische Gates: HOLD.</b> Die Konstruktion ist kein hergeleiteter physikalischer Hamiltonoperator. Ein globaler Außenraumanschluss, ein Bounce und Singularitätsauflösung bleiben offen. Der Normausschluss ist kein allgemeines No-go für CST.','s')
    p('Basis: Main 3a26651cb1476b5e3b5d89c343e11487a012e432 nach PR 252. Vollständige Herleitung, sechs exakte Ergebnisdateien und ausführbare Nachrechnung im Prüfpaket.','s')

    page()
    h('1 · Eine feste Uhrdauer ist keine feste Geburtszahl')
    p('Wir behalten sämtliche vergangenen Ordnungs-, Uhr- und Dichtedaten. Mit s=(T+L)/(2L) ist das Uhrmaß ds. Eine vollständige Endgeschichte Y besitzt am Schnitt a genau ein Präfix X=Y<sub>a</sub>. Sind m und n ihre Elementzahlen, lautet ein deklarierter Intervallkandidat:')
    eq('(U<sub>b,a</sub>ψ)(Y)=z<super>n−m</super> [f(n)/f(m)]<br/>· exp{i[S(Y)−S(X)]/ℏ} ψ(X)')
    p('z ist ein freier konstanter Geburtsfaktor. f ist eine positive zusätzliche Zahlgewichtung. Für f=1 und z=1 bleibt der Betrag-eins-Koeffizient des Vorgängers erhalten. Keine Geburt trägt den Koeffizienten eins.')
    h('Warum die Komposition stimmt')
    eq('U<sub>c,b</sub> U<sub>b,a</sub> = U<sub>c,a</sub>')
    p('Die Uhr bestimmt den Zwischenrecord eindeutig. Die Geburtszahlen addieren sich, die mittleren f-Faktoren kürzen sich und die Wirkungsdifferenzen teleskopieren. Das gilt für alle Felder mit demselben <b>Gesamtzahlregulator N</b>. An den Zwischenschnitten wird kein neuer Endanker eingefügt.')
    p('Eine neue Geburtsobergrenze je Einzelintervall wäre falsch: Zwei Intervalle mit jeweils höchstens einer Geburt erlauben zusammen zwei, ein direktes solches Intervall nur eine. Ein zusätzlicher Faktor 1/k! wäre ebenfalls falsch; die geordnete Uhrintegration enthält h<super>k</super>/k! bereits.')
    h('Die vollständige Vergangenheit ist wesentlich')
    table([
        ['Anfügung an eine alte Ein-Element-Geschichte','ΔS<sub>g</sub>','ΔS<sub>d</sub>'],
        ['Vollständige vergangene Kette','9','27/4'],
        ['Neues Element als isoliertes Intervall','0','−33/32'],
    ],[319,95,95],padding=6)
    p('Die Uhren sind T=(0,1/2), die Dichtemarken w=(0,1/2), mit geerbtem Anfangsanker. Das isolierte Intervall verliert die über den Schnitt reichenden Paare. Die unabhängige Inkrementrechnung bestätigt die vollständige Wirkung.','s')

    page()
    h('2 · Die ungewichtete Norm scheitert an der Zahl der Ordnungen')
    p('E<sub>P</sub>(k) zählt alle k-Erweiterungen eines alten P. Weil vollständige Endrecords im erklärten lokalen Produkt orthogonal sind, hebt sich die reelle Wirkungsphase im Normquadrat auf. Für q=|z|² und h=b−a gilt:')
    eq('Z<sub>N</sub>(P,h)=Σ<sub>k≤N−m</sub> E<sub>P</sub>(k)q<super>k</super><br/>· [f(m+k)/f(m)]² h<super>k</super>/k!<br/>U†U = Z<sub>N</sub> als Multiplikationsoperator')
    p('Ohne zusätzliche Zahlgewichtung ist f=1. Eine Familie mit zwei antikettenförmigen Schichten erlaubt jede untere-zu-obere Relation unabhängig. Alle neuen Elemente können über dem gesamten alten P liegen. Daher E<sub>P</sub>(k)≥2<super>floor(k²/4)</super>.')
    eq('B<sub>2r</sub>=2<super>r²</super>x<super>2r</super>/(2r)!, &nbsp; x=qh&gt;0<br/>B<sub>2r+2</sub>/B<sub>2r</sub>=2<super>2r+1</super>x²/[(2r+2)(2r+1)] → ∞')
    p('<b>Die positiven Normsummanden gehen nicht gegen null.</b> Für jedes positive Uhrintervall und jedes z≠0 ist die unbegrenzte lokale Historiennorm unendlich. Ein kleiner konstanter Geburtsfaktor reicht nicht.')
    example=next(x for x in entropy['lower_terms'] if x['x_equals_abs_z_squared_times_h']=='1/4')
    rows=[['Neue Elemente k','Unterer Normsummand bei x=1/4, gerundet']]
    rows += [[x['n'],format(float(F(x['lower_term'])),'.5g')] for x in example['terms'] if x['n']<=32]
    table(rows,[140,369],padding=4)
    p('Die endliche Tabelle illustriert den allgemeinen Beweis. Der Ausschluss betrifft diese orthogonale Quadratsumme; Auslöschung in einer oszillierenden skalaren Summe, andere Skalarprodukte oder Quantenmaße sind damit nicht ausgeschlossen. Dies ist keine physikalische Singularitätsaussage.','s')

    page()
    h('3 · Ein transparentes Zahlgewicht kontrolliert die Summe')
    p('Wir prüfen zwei ausdrücklich zusätzliche Entscheidungen. Sie verändern die Gewichte zwischen Elementzahlen, erhalten aber für festes Ausgangs-m und End-n die relativen Geometrie- und Feldamplituden:')
    eq('f<sub>α</sub>(n)=2<super>−αn(n−1)/4</super>, &nbsp; α=1 oder 2')
    p('Der Quotient f(n)/f(m) bleibt unter Zusammensetzung teleskopisch. Komposition verbietet diese Dämpfung also nicht. Sie ist aber keine Eichumbenennung und wird nicht durch die geerbte Wirkung ausgewählt.')
    h('Eine uniforme Schranke, auch über alle alten Größen')
    p('Bei der j-ten Anfügung gibt es höchstens 2<super>m+j</super> Ideale. Somit gilt E<sub>P</sub>(k)≤2<super>mk+k(k−1)/2</super>. Das quadrierte Zahlgewicht kompensiert diese obere Schranke für jedes α≥1:')
    eq('E<sub>P</sub>(k)[f<sub>α</sub>(m+k)/f<sub>α</sub>(m)]² ≤ 1<br/>1 ≤ Z<sub>∞</sub>(P,h) ≤ e<super>qh</super>, &nbsp; ‖U<sub>b,a</sub>‖² ≤ e<super>qh</super>')
    p('Die unbegrenzte Intervallabbildung ist damit beschränkt und komponiert. Sie ist zunächst noch nicht normerhaltend: Der Keine-Geburt-Beitrag plus weitere Ausgänge ergeben Z&gt;1.')
    h('Der nicht enumerierte Rest bleibt kontrolliert')
    eq('0 ≤ Z<sub>∞</sub>−Z<sub>m+K</sub><br/>≤ [x<super>K+1</super>/(K+1)!] / [1−x/(K+2)], &nbsp; x=qh&lt;K+2')
    table([['Beispiel','Garantierte obere Restgrenze'],['q=1, h=1/2, K=6','1/604800 ≈ 0,000001654']],[270,239],padding=6)
    p('Die Schranke folgt aus der Exponentialreihe und gilt für alle zukünftigen Geometrien und kontinuierlichen Marken im erklärten Referenzmaß. Sie ist keine Fehlerschranke einer physikalischen Staubballvorhersage. Andere Profile können ebenfalls zulässig sein; eine optimale oder eindeutige Dämpfung ist nicht behauptet.','s')

    page()
    h('4 · Ein gemeinsamer Enduhrwert macht die Normierung kompatibel')
    p('Ein festes t<sub>*</sub> muss für alle Zwischenschritte dasselbe bleiben. Die verbleibende Zustandssumme ist Z(P,t<sub>*</sub>−s). Wir definieren den vervollständigten Referenztransport:')
    eq('(K<sub>b,a</sub><super>t*</super>ψ)(Y)=<br/>√[Z(P<sub>Y</sub>,t<sub>*</sub>−b)/Z(P<sub>X</sub>,t<sub>*</sub>−a)] (U<sub>b,a</sub>ψ)(Y)')
    p('Jede Zukunft zerfällt eindeutig am Schnitt b. Ihre Zustandssumme ist daher genau die Summe aus dem ersten Intervallgewicht mal der verbleibenden Zustandssumme. Daraus folgen für jedes Eingangspaket:')
    eq('(K<sub>b,a</sub><super>t*</super>)†K<sub>b,a</sub><super>t*</super>=I<br/>K<sub>c,b</sub><super>t*</super>K<sub>b,a</sub><super>t*</super>=K<sub>c,a</sub><super>t*</super>')
    p('Die mittleren Z-Faktoren kürzen sich. Für endliches N gilt dies exakt; für die gedämpften Gewichte kontrolliert die Restschranke den unbegrenzten Fall. <b>Isometrie ist hier bewiesen; eine surjektive unitäre oder physikalische Evolution ist damit nicht ausgewählt.</b>')
    h('Die unabhängige Einzelintervall-Normierung wäre falsch')
    p('Bei f=1, z=1, N=2 und leerem Ausgang gilt Z(h)=1+h+h². Zwei Viertelintervalle liefern Z(1/4)²=441/256, das direkte Halbintervall aber Z(1/2)=448/256. Schon der Keine-Geburt-Koeffizient wäre verschieden.')
    table([['Gemeinsamer Endwert t*=1/2','Keine-Geburt-Wahrscheinlichkeit'],['Bis zum Zwischenschnitt 1/4','3/4'],['Danach, bedingt auf bisher keine Geburt','16/21'],['Produkt = direkter Gesamtausgang','4/7']],[319,190],padding=5)
    p('Die zugehörige Gesamtrate ist ∂<sub>h</sub>log Z. Für α≥1 bleibt sie auf einem festen Horizont H durch q·e<super>qH</super> beschränkt. Diese Referenz erzeugt dort fast sicher nur endlich viele Geburten. Es ist eine bedingte mathematische Wartezeitregel, keine hergeleitete physikalische Staubrate.','s')

    page()
    h('5 · Konsistenz allein entscheidet nicht zwischen den Gewichten')
    p('Leerer Ausgang, z=1, h=1/2 und gemeinsamer Gesamtzahlregulator N=2. Alle Zeilen sind normiert und schnittkompatibel:')
    rows=[['α','Z','P(0 Geburten)','P(1 Geburt)','P(2 Geburten)']]
    for x in horizon['terminal_demos']:
        rows.append([x['alpha'],x['Z'],*x['terminal_birth_count_probabilities']])
    table(rows,[39,65,135,135,135],padding=6)
    p('α=0 ist nur mit endlichem N zulässig. Die zwei gedämpften Kandidaten α=1 und α=2 bleiben auch ohne Elementzahlgrenze verschieden. Die bis N=6 exakten Summen und die Restschranke liefern für keine Geburt nach außen gerundete, disjunkte Intervalle:')
    table([['Gewähltes Profil','P(0 Geburten), ohne Elementzahlgrenze'],['α=1','[0,607920; 0,607921]'],['α=2','[0,639056; 0,639058]']],[140,369],padding=6)
    p('Der Unterschied ist somit kein bloßer Abschneideeffekt. Es sind Referenzwahrscheinlichkeiten, keine gemessenen Ereignisraten und keine Bounce-Wahrscheinlichkeiten. Die vorhandene Wirkung wählt weder α noch z oder den Enduhrwert aus.')
    h('Die reelle Wirkungsphase löst die physikalische Auswahl hier nicht')
    eq('K<super>S</super><sub>b,a</sub>=D<sub>b</sub>K<super>0</super><sub>b,a</sub>D<sub>a</sub>†,<br/>D<sub>s</sub>ψ=exp(iS/ℏ)ψ')
    p('Für scharfe, diagonale Ereignisse im vollständig gespeicherten Historienraum fallen die Phasen aus den Born-Gewichten heraus. Diese Auslese zeigt deshalb keine gravitative Interferenzunterdrückung unerwünschter Geometrien.')
    p('Eine kohärente Randkontraktion könnte Interferenz tragen. Ihre Positivität, Norm und Schnittkompatibilität müssen aber gesondert geprüft werden. Eine lokale Recordnorm darf nicht stillschweigend als ausgewählte physikalische Quantenmaßstruktur gelten.','s')

    page()
    h('6 · Nachrechnung und nächste physikalische Entscheidung')
    table([
        ['Kontrolle','Umfang / Ergebnis'],
        ['Unabhängige Ordnungszählung bei n=6',fmt(counts['natural_order_census'][-1])],
        ['Markierte vollständige Wirkungsrecords',fmt(sew['marked_records'])],
        ['Wirkung an Uhrschnitten / Zahl-Kozyklen',fmt(sew['full_action_cut_checks'])+' / '+fmt(sew['count_cocycle_checks'])],
        ['Zustandssummen / Rückwärtsgleichung',str(horizon['partition_norm_identities'])+' / '+str(horizon['hazard_identities'])],
        ['Gemeinsame-Horizont-Koeffizienten',fmt(horizon['horizon_coefficient_cocycles'])],
        ['Uniforme Gewichtsgrenzen / Restkontrollen',str(weights['weighted_extension_bound_checks'])+' / '+str(len(weights['tail_controls']))],
        ['Isolierte Nachrechnung',str(replay['result_files'])+' Ergebnisdateien bytegleich'],
    ],[319,190],padding=4)
    p('Exakte Brüche und ganze Zählungen, Python-Standardbibliothek. Die Uhrgitter dienen algebraischen Kontrollen; sie sind keine zertifizierte Quadratur des kontinuierlichen Pfadintegrals. Die unendlichen Aussagen werden analytisch bewiesen. Kein neuer physikalischer 4D-Lauf und kein formaler Beweisassistent.','s')
    h('Jetzt die gravitative Interferenz und Randdefinition prüfen')
    p('Der nächste gezielte Schritt ist eine deklarierte kohärente Randkontraktion oder ein Dekohärenzfunktional. Es muss mit den kontrollierten Summen, zulässigen Ereignissen und Uhrschnitten zusammenpassen. Zusätzlich braucht die physikalische Theorie eine Begründung der Zahlgewichte und des Randzustands; eine weitere frei gewählte Normierung genügt dafür nicht.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.</b> Die Referenz ist ausgearbeitet; die physikalische Quantendefinition bleibt offen.','s')
    h('Reproduzieren und einordnen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/>Sechs gepinnte Repositoryquellen. Lokal eingefrorener Plan; keine externe Präregistrierung. Bytegleicher Replay ist keine unabhängige wissenschaftliche Replikation.','s')
    p('[1] Rideout, Sorkin, A Classical Sequential Growth Dynamics for Causal Sets, Phys. Rev. D 61 (2000). <link href="https://arxiv.org/abs/gr-qc/9904062v3" color="#17445e">arXiv:gr-qc/9904062v3</link>. Weitere Kausalitäts-/Kovarianzbedingungen klassischer Wachstumsmodelle sind hier nicht behauptet.<br/>[2] Sorkin, Quantum Mechanics as Quantum Measure Theory (1994). <link href="https://arxiv.org/abs/gr-qc/9401003v2" color="#17445e">arXiv:gr-qc/9401003v2</link>. Ein Quantenmaß muss nicht durch additive Recordwahrscheinlichkeiten beschrieben sein.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: Feste Uhrintervalle und variable Elementzahl v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


