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
NAME = 'CST_DUST_Alpha_Abhaengige_Normrestschranke_v0_1'
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
    c.drawString(43,35,'CST-DUST · α-abhängige Normrestschranke v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def outward(value,digits,upper=False):
    x=F(value);scale=10**digits;n=x.numerator*scale
    k=-((-n)//x.denominator) if upper else n//x.denominator
    return (str(k//scale)+','+str(k%scale).zfill(digits))


def interval(bounds,digits=9):
    return '['+outward(bounds[0],digits)+'; '+outward(bounds[1],digits,True)+']'


def percent(value,digits=2):
    return f'{100*float(F(value)):.{digits}f}'.replace('.',',')+' %'


def scientific_upper(value,digits=5):
    x=F(value)
    if not x:return '0'
    power=0
    while x<1:x*=10;power-=1
    while x>=10:x/=10;power+=1
    return outward(x,digits,True)+'·10<super>'+str(power)+'</super>'


def main():
    summary=json.loads((ROOT/'results/improvement_summary.json').read_text())['records']
    cases=json.loads((ROOT/'results/refined_results.json').read_text())['cases']
    verification=json.loads((ROOT/'results/verification.json').read_text())
    replay=json.loads((ROOT/'results/replay.json').read_text())
    p('Eine schärfere Normrestgrenze<br/>für das CST-DUST-Referenzmodell','title')
    p('α-abhängige Schranke · v0.1 · 7. November 2026','s')
    h('Mehr Information aus den vorhandenen Ergebnissen')
    p('Die analytische Grenze für den unendlichen Normrest nutzt jetzt sowohl α als auch die exakt bekannten 4824 Sechs-Element-Ordnungen. Die bisherigen Feldamplituden und ihre Fehler bleiben unverändert; neue Feldintegrale waren nicht nötig.')
    table([
        ['Ergebnis','Geprüfter Umfang'],
        ['Gesamte Phasenrest-Gewichtsschranke bei α=2','Weitere Reduktion um 81,85 bis 94,91 % gegenüber dem Vier-Element-Stand.'],
        ['Gesamte Phasenrest-Gewichtsschranke bei α=1','Weitere Reduktion um 0,37 bis 1,47 %.'],
        ['Ausleseintervalle','36 Zahlkanal- und 36 kohärente Erfolgsintervalle liegen innerhalb ihrer Vorgänger.'],
        ['Nachrechnung','Fünf neue Ergebnisdateien im isolierten Replay bytegleich reproduziert.'],
    ],[205,304],padding=8)
    h('Der nächste quantitative Engpass ist jetzt sichtbar')
    p('Rund 96,35 bis 99,95 % der verbleibenden oberen Restmasse entfallen auf den n=5-Sektor. Der bisher besonders grobe Normrest dominiert das Fehlerbudget bei α=2 damit nicht mehr.')
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Die Verbesserung betrifft eine Schranke im erklärten Referenzmodell. Eine vollständige CST-Dynamik, Rückwirkung, Bounce oder Junction sind weiterhin nicht hergeleitet.','s')
    p('Basis: Main nach PR 257, Commit 0067da907da4ea8df5b625ea9f8f99ce1527e9ed. Acht Quellen sind byteidentisch gepinnt. Exakte rationale Werte und vollständiger Beweis stehen im Prüfpaket.','s')

    page()
    h('1 · Der Beweis: Verzweigung und α gemeinsam bilanzieren')
    p('N<sub>n</sub> zählt natürlich durch die monotone Uhr beschriftete Ordnungen. Das neue letzte Element wählt ein Vergangenheitideal aus höchstens 2<super>n</super> Teilmengen. Jedes Paar aus Präfix und Ideal bestimmt genau eine Fortsetzung:')
    eq('N<sub>n+1</sub> ≤ 2<super>n</super>N<sub>n</sub><br/>c<sub>n</sub> = N<sub>n</sub> h<super>n</super> / n! · 2<super>−α n(n−1)/2</super>')
    p('Daraus folgt für h≥0 und α≥1 eine monoton fallende obere Schranke auf die Sektorquotienten:')
    eq('c<sub>n+1</sub> ≤ r<sub>n</sub> c<sub>n</sub>, &nbsp; r<sub>n</sub> = h/(n+1) · 2<super>−(α−1)n</super><br/>q<sub>K</sub> = r<sub>K+1</sub> &lt; 1')
    p('Die positive Restreihe ist deshalb durch eine geometrische Reihe mit erstem Term c<sub>K</sub>r<sub>K</sub> eingeschlossen:')
    eq('Σ<sub>n&gt;K</sub> c<sub>n</sub> ≤ Δ<sub>K</sub> = c<sub>K</sub>r<sub>K</sub> / (1−q<sub>K</sub>)')
    h('Für den verwendeten Cutoff K=6')
    eq('Δ<sub>6</sub> = (603/4096) · h<super>7</super> · 2<super>−21(α−1)</super><br/> &nbsp; / [7! · (1−h·2<super>−7(α−1)</super>/8)]')
    p('Der Faktor 603/4096 ist exakt N<sub>6</sub>/2<super>15</super>. Bei α=1 verkleinert er die alte Normrestschranke um 85,2783 %. Bei α=2 kommt bereits im ersten ausgelassenen Term der Faktor 2<super>−21</super> hinzu.')
    p('Der Satz gilt für reelle α≥1. Die Implementierung verwendet ganzzahlige α≥1 und exakte rationale Arithmetik. Bei q<sub>K</sub>≥1 wird die Formel zurückgewiesen. Für α&lt;1 wird hier weder ein gültiges Zertifikat noch ein allgemeiner Divergenzsatz behauptet.','s')
    p('Der unendliche Beweis beruht auf der Präfix-Ideal-Bijektion und der geometrischen Domination. Endliche Tests kontrollieren die Umsetzung, ersetzen diesen Beweis aber nicht.','s')

    page()
    h('2 · Normrest und gesamter Phasenrest sind verschieden')
    p('Die Phasen der Sektoren n=5 und n=6 sind weiterhin unbekannt. Ihre Normmassen sind exakt bekannt und bleiben vollständig in der Unsicherheitsbilanz:')
    eq('Z<sub>max</sub> = Z<sub>6</sub> + Δ<sub>6</sub><br/>R<sub>max</sub> = (Z<sub>6</sub>−Z<sub>4</sub>) + Δ<sub>6</sub><br/>p<sub>max</sub> = R<sub>max</sub>/Z<sub>max</sub>')
    h('Obere Grenzen für den Normrest n&gt;6')
    rows=[['h / α','Vorher','Jetzt']]
    for x in summary:
        rows.append([x['h']+' / '+str(x['alpha']),scientific_upper(x['old_norm_tail_upper']),scientific_upper(x['anchored_norm_tail_upper'])])
    table(rows,[65,222,222],padding=8)
    p('Dezimale Tabellenwerte sind nach oben gerundet. Bei α=2 sinkt die Normrestschranke allein um mehr als 99,99999 %. Dieser Prozentsatz gilt nicht für die gesamte Phasenrestschranke.','s')
    h('Gewinn bei der gesamten Phasenrest-Gewichtsschranke')
    rows=[['h / α','Vorher p<sub>max</sub>','Jetzt p<sub>max</sub>','Reduktion ≈']]
    for x in summary:
        rows.append([x['h']+' / '+str(x['alpha']),scientific_upper(x['old_phase_tail_probability_upper']),scientific_upper(x['new_phase_tail_probability_upper']),percent(x['phase_tail_fraction_removed'],3)])
    table(rows,[65,159,159,126],padding=8)
    p('Diese Größen sind obere Schranken innerhalb des Referenzmaßes. Sie stellen keine gemessene tatsächliche Elementzahlverteilung dar. Die Normierung bleibt bei K=6, die Feldintegration bei n≤4.','s')

    page()
    h('3 · Engere Grenzen für die bestehende Auslese')
    p('Die eingeschlossenen Amplituden t<sub>n</sub>, ihre Fehler ε<sub>n</sub> und die Sichtbarkeitsintervalle v<sub>n</sub> werden bytegleich übernommen. Für den Zahlkanal gilt mit S<sub>±</sub>=Σ<sub>n≤4</sub>c<sub>n</sub>v<sub>n</sub><super>±</super>:')
    eq('P<sub>count</sub> ∈ [S<sub>−</sub>/Z<sub>max</sub>, (S<sub>+</sub>+R<sub>max</sub>)/Z<sub>max</sub>]')
    p('Ein kleineres Z<sub>max</sub> hebt die Untergrenze an und senkt die Obergrenze. Der kohärente Kanal erhält ebenfalls ein engeres Rohintervall; dessen Schnitt mit der gültigen Vorgängergrenze wird getrennt gespeichert.')
    h('Beispiele bei g=0 und μ=1')
    rows=[['h / α','Neues Erfolgsintervall der unbegrenzten Elementzahlsumme']]
    for hs in ['1/4','1/2']:
        for alpha in [1,2]:
            x=next(x for x in cases if x['h']==hs and x['alpha']==alpha and x['g_over_pi']=='0' and x['mu']=='1')
            rows.append([hs+' / '+str(alpha),interval(x['count_success_infinite_interval'],12)])
    table(rows,[65,444],padding=10)
    table([
        ['Prüfung','Ergebnis'],
        ['Zahlkanal','36/36 neue Intervalle innerhalb ihrer Vorgänger.'],
        ['Kohärenter Kanal','36/36 Rohintervalle und endgültige Intervalle innerhalb ihrer Vorgänger.'],
        ['Bedingte Auslese n=0,...,4','180/180 Intervalle innerhalb ihrer Vorgänger.'],
        ['Phasenfreier Fall g=μ=0','Weiterhin exakt eins.'],
    ],[180,329],padding=7)
    p('Unbegrenzt ist hier die Elementzahlsumme bei festem endlichem h. Ein Grenzübergang zu unendlicher Zeit wird nicht behauptet. Es wurden keine neuen Feldphasen ausgewertet und keine Fehler der geerbten Amplituden entfernt.','s')

    page()
    h('4 · Kontrollen und reproduzierbares Prüfpaket')
    table([
        ['Kontrolle','Ergebnis'],
        ['Zwei Enumerationswege','Identische Ordnungen für n=0,...,7: 1, 1, 2, 7, 40, 357, 4824, 96428.'],
        ['Endliche Kontrolle bis n=7','Die tatsächlich enumerierte positive Restmasse liegt in allen 157 gültigen Fällen unter der analytischen Grenze.'],
        ['Majoranten','7536 rationale Schritte prüfen Rekurrenz, monotone Quotienten und geometrische Domination.'],
        ['Ungültige Quotienten','11 Fälle mit q<sub>K</sub>≥1 werden zurückgewiesen.'],
        ['Falscher Exponent oder fehlendes N<sub>6</sub>','Beide falschen Grenzen unterschreiten schon die exakte n=7-Masse und werden zurückgewiesen.'],
        ['Weitere Negativkontrollen','α&lt;1, negatives h, negativer Cutoff und q<sub>K</sub>=1 werden zurückgewiesen.'],
        ['Isolierter Replay',replay['isolated_replay']+': fünf neue Ergebnisdateien bytegleich.'],
    ],[190,319],padding=8)
    h('Nachrechnen')
    p('<font name="DVM">python3 -B analyze.py</font><br/><font name="DVM">python3 -B replay.py</font><br/><font name="DVM">python3 -B verify_package.py</font>','eq')
    p('Python 3.12 und Standardbibliothek genügen. Der Replay setzt ein Zeitlimit von 180 Sekunden durch. Kein C++-Compiler, kein neuer nativer Integrallauf und kein bezahlter Rechendienst sind nötig.','s')
    p('Die n=7-Enumeration ist eine Kontrolle; sie erhöht den Produktionscutoff nicht. Die geerbten Amplituden werden nicht neu zertifiziert. Bytegleiche Wiederholung derselben Implementierung ist keine externe Replikation oder formale Beweisassistenzprüfung.','s')

    page()
    h('5 · Was die Verbesserung für den nächsten Schritt bedeutet')
    p('Der bisher grobe Normrest war bei α=2 die wichtigste vermeidbare Überabschätzung. Nach seiner Schärfung dominiert die exakt bekannte Normmasse des weiterhin unbekannten n=5-Feldphasensektors:')
    rows=[['h / α','n=5-Anteil an R<sub>max</sub>, ungefähr','Normrest-Anteil, ungefähr']]
    for x in summary:
        rows.append([x['h']+' / '+str(x['alpha']),percent(x['n5_share_of_Rmax'],3),percent(x['new_norm_tail_share_of_Rmax'],6)])
    table(rows,[65,244,200],padding=9)
    p('Diese Anteile beziehen sich auf das konservative Fehlerbudget, nicht auf gemessene Wahrscheinlichkeiten. Der nächste quantitative Kandidat ist eine Kosten- und Fehlerentscheidung für die n=5-Feldintegration. Weitere Normrestschärfung bleibt möglich, hat nun aber wesentlich weniger Gewicht.')
    h('Die physikalische Aufgabe bleibt davon getrennt')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD.</b>')
    p('Die physikalische Begründung von α, Dichtemaß, kohärentem Historienzugriff und Endrandwahl ist weiterhin offen. Es folgt keine vollständige vierdimensionale CST-Dynamik, gravitative Rückwirkung, Singularitätsauflösung, Bounce- oder Junction-Aussage.')
    h('Quellen und Beweisumfang')
    p('[1] <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/257" color="#17445e">X6, PR 257</link>: unverändertes Referenzmaß und eingeschlossene Vier-Element-Amplituden; acht Quellen mit Git-Blob-Identitäten im Paket.<br/>[2] <link href="https://dlmf.nist.gov/1.2.E11" color="#17445e">NIST DLMF 1.2.11</link>: geometrische Summenidentität.<br/>[3] DERIVATION.md: vollständiges Präfix-Ideal-Lemma, unendliche Restschranke und Übertragung auf die Auslese. Der Beweis betrifft das erklärte mathematische Referenzmodell.','s')
    p('Plan: nach symbolischer Herleitung lokal eingefroren, vor neuen Zahlenwerten und Implementierung. Keine externe Präregistrierung und keine blinde Vorhersage.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: alpha-abhängige Normrestschranke v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


