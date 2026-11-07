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
NAME = 'CST_DUST_Kohaerente_Randauslese_Dekohaerenz_v0_1'
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
    c.drawString(43,35,'CST-DUST · Kohärente Randauslese v0.1 · 7. November 2026')
    c.drawRightString(552,35,str(doc.page))


def main():
    read=lambda n:json.loads((ROOT/'results'/n).read_text())
    cont=read('continuous_gravity.json');tails=read('tail_bounds.json')
    audit=read('boundary_audit.json');replay=read('replay.json')
    p('Kohärente Randauslese<br/>und Dekohärenz','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Interferenz ist möglich. Ihre physikalische Randwahl bleibt offen.')
    p('Der Referenztransport vollständiger Historien wird um zwei feste, beschränkte Endauslesen ergänzt. Die eine überlagert alle Elementzahlen kohärent. Die andere unterscheidet die endgültige Elementzahl und erhält Interferenz zwischen Geometrien innerhalb derselben Zahl.')
    table([
        ['Geprüfter Baustein','Ergebnis'],
        ['Kohärente Endauslese','Positiver Effekt mit vollständigem Ausfallkanal.'],
        ['Rücktransport der Auslese','Konsistent zwischen Zeitschnitten; keine nachträgliche Normierung.'],
        ['Eine reine Endprojektion','Ranghindernis für mehrere positive, exakt dekohärente Historienatome.'],
        ['Getrennte Elementzahlkanäle','Normierte Zahlverteilung bei erhaltener Interferenz innerhalb jeder Zahl.'],
        ['Frühere Historienfragen','Dekohärieren dadurch nicht automatisch.'],
    ],[185,324])
    h('Was dieser Schritt leistet')
    p('Die bisher offene kohärente Randkontraktion liegt jetzt als prüfbares Instrument vor. Ein kontinuierlicher Gravitationstest zeigt einen exakten Interferenzeffekt. Gesonderte atomare Kontrollen prüfen zusätzlich die Materiephase und den Rücktransport.')
    p('<b>Acht physikalische Gates: HOLD.</b> Weder die Randwahl noch das Zahlgewicht und der Enduhrwert sind physikalisch ausgewählt. Ein globaler Bounce, Singularitätsauflösung und der Innen-/Außenraumanschluss sind damit nicht hergeleitet.','s')
    p('Basis: Main nach PR 253, Commit 36afc462dc5a9503616e9b016481e3b441b7c123. Vollständige Definitionen und Beweise in DERIVATION.md; exakte Ergebnisse und Nachrechnung im Prüfpaket.','s')

    page()
    h('1 · Ein festes Instrument mit kontrolliertem Rücktransport')
    p('Der Vorgänger liefert Isometrien K zwischen Uhrintervallen mit vollständiger Vergangenheit und gemeinsamem Enduhrwert t*. Übernommen werden das lokale Historienprodukt, der monotone Uhrsektor und die zusätzlichen Zahlgewichte f<sub>α</sub>(n)=2<super>−αn(n−1)/4</super>, α=1 oder 2.')
    p('b bezeichnet den normierten, phasenfrei entwickelten leeren Anfangsrecord. Dieser Randbezug bleibt fest, wenn die Wirkungsphase θ=g(S<sub>g</sub>−1)+μS<sub>d</sub> variiert wird. Der Endzustand lautet ψ<sub>θ</sub>=exp(iθ)b.')
    eq('E<sub>all</sub>=|b⟩⟨b|, &nbsp; E<sub>fail</sub>=I−E<sub>all</sub><br/>p<sub>all</sub>=|⟨b,ψ<sub>θ</sub>⟩|²=|E<sub>p₀</sub> exp(iθ)|² ≤ 1')
    p('Das Effektpaar definiert Erfolg und Ausfall für jeden normierten Zustand. Eine flache Summe über alle Endhistorien ist dagegen auf dem unendlichen lokalen L²-Raum unbeschränkt: Die Zahl der Ordnungen wächst schneller als die geordnete Uhrintegration h<super>n</super>/n! dämpft.')
    h('Die Endauslese an einen früheren Schnitt ziehen')
    eq('b<sub>a</sub>=K<sub>t*,a</sub>† b, &nbsp; E<sub>a</sub>=|b<sub>a</sub>⟩⟨b<sub>a</sub>| ≤ I<br/>b<sub>a</sub>=K<sub>b,a</sub>† b<sub>b</sub>, &nbsp; E<sub>a</sub>=K<sub>b,a</sub>† E<sub>b</sub> K<sub>b,a</sub>')
    p('Die Identitäten folgen aus der Komposition der K. Der zurückgezogene Vektor hat im Allgemeinen Norm kleiner als eins. Er darf <b>nicht neu normiert</b> werden: Auf dem eindimensionalen leeren Anfangssektor ist seine quadrierte Norm genau die Erfolgswahrscheinlichkeit. Renormierung würde daraus eins machen.')
    h('Eine andere Randwahl erzeugt ein anderes Ergebnis')
    p('Wird b mit derselben Phase mitbewegt, also b<sub>θ</sub>=exp(iθ)b gesetzt, ist der Erfolg stets eins. Der Interferenzeffekt hängt somit wesentlich vom festgehaltenen Randbezug ab. Die Wirkung allein wählt dieses Instrument nicht aus.')
    p('Geltung: derselbe Enduhrwert, dieselbe Zahlgewichtung und dieselbe Gesamtzahlgrenze oder deren kontrollierter Grenzwert. Es wird keine surjektive Unitarität und keine physikalische kosmologische Endbedingung behauptet.','s')

    page()
    h('2 · Ein Dekohärenzfunktional ist noch kein klassisches Maß')
    p('Für Historienereignisse A,B und deren lokale Projektoren P definieren wir bei festem 0≤E≤I:')
    eq('D<sub>E</sub>(A,B)=⟨P<sub>A</sub>ψ, E P<sub>B</sub>ψ⟩')
    p('Die Gram-Darstellung mit √E P<sub>A</sub>ψ beweist starke Positivität. Hermitizität, Additivität in disjunkten Ereignissen und die Grad-zwei-Summenregel folgen unmittelbar. Bei positivem Gesamtwert p<sub>E</sub>=D<sub>E</sub>(Ω,Ω) lässt sich D<sub>E</sub>/p<sub>E</sub> normieren.')
    p('Trotzdem sind dessen Diagonalen bei Interferenz keine gewöhnlichen Wahrscheinlichkeiten exklusiver Historien. Exakte mittlere Dekohärenz einer Partition verlangt, dass sämtliche unterschiedlichen Atompaare D(A<sub>i</sub>,A<sub>j</sub>)=0 erfüllen.')
    h('Das Ranghindernis')
    eq('rank(D) ≤ rank(E)<br/>k positive, exakt dekohärente Atome ⇒ rank(E) ≥ k')
    p('Bei reinem Anfangszustand und einer Rang-eins-Endprojektion kann deshalb höchstens ein Atom einer exakt mittel-dekohärenten Partition positiv sein. Das ist kein allgemeiner Ausschluss gemischter Zustände, anderer Ränge oder anderer Dekohärenzkriterien.')
    h('Eine exakte Negativkontrolle')
    table([
        ['Zwei Geometrien, relative Phase π','Wert'],
        ['Anfangszustand nach Phase; fester Endbezug','ψ=(2,−1)/√5; b=(1,1)/√2'],
        ['Erfolg; Ausfall','1/10; 9/10'],
        ['Erste normierte Historien-Atomdiagonale','4 — keine klassische Wahrscheinlichkeit'],
        ['Records ohne beobachtetes Ausleseergebnis','4/5 und 1/5'],
    ],[283,226],padding=6)
    p('Eine ausgewogene destruktive Präparation hat Erfolg null; D darf dann nicht normiert werden. Ein überskalierter Effekt 2|b⟩⟨b| liefert den unzulässigen Wert 2 und scheitert an der Positivität seines Komplements.','s')
    p('Für ein bereits vergangenes Ereignis bleiben die Funktionalwerte beim Schnittwechsel gleich. Dabei muss dieselbe frühere Frage erhalten bleiben; die Elementzahl am jeweils aktuellen Schnitt ist eine andere Frage.','s')

    page()
    h('3 · Zahlkanäle verbinden Interferenz und eindeutige Ausgänge')
    p('Π<sub>n</sub> projiziert auf die endgültige Elementzahl n. Die normierten Teilvektoren b<sub>n</sub> des festen Randbezugs sind orthonormal:')
    eq('p<sub>n</sub>=‖Π<sub>n</sub>b‖², &nbsp; b<sub>n</sub>=Π<sub>n</sub>b/√p<sub>n</sub><br/>E<sub>count</sub>=Σ<sub>n</sub>|b<sub>n</sub>⟩⟨b<sub>n</sub>| ≤ I')
    p('Die starke Summe bleibt auch bei unbegrenzter Elementzahl eine beschränkte Projektion. Jeder n-Kanal besitzt einen eigenen Ausgang. Verschiedene Geometrien innerhalb desselben n können weiterhin interferieren.')
    eq('Pr(n | Erfolg)=|⟨b<sub>n</sub>,ψ⟩|² / p<sub>count</sub><br/>p<sub>count</sub>=Σ<sub>n</sub>|⟨b<sub>n</sub>,ψ⟩|² ≥ p<sub>all</sub>')
    p('Die terminale Zahlpartition ist exakt mittel-dekohärent. Für andere Ereignispartitionen folgt dies nicht. Erfolg plus Ausfall ergibt wieder die ursprüngliche phasenblinde Recordverteilung.')
    h('Ein kontinuierlich integrierter Zwei-Geometrien-Test')
    p('Mit Zahlgrenze 2, α=1, Uhrdauer h=1/2, Geburtsfaktor z=1 und Materiekopplung μ=0 ist die ursprüngliche Zahlverteilung (8,4,1)/13. Bei n=2 besitzt die Antikette G=0 und die Kette G=9. Ihre Erfolgsfraktion ist (1+cos(9g))/2.')
    rows=[['Gravitationsphase g','Gesamterfolg','Zahlverteilung bei Erfolg']]
    rows += [['0','1','(8,4,1)/13'],['π/18','25/26','(16,8,1)/25'],['π/9','12/13','(2/3,1/3,0)']]
    table(rows,[150,130,229],padding=7)
    p('Die n=2-Interferenz ist exakt, Uhr und Dichte wurden analytisch integriert. Der Ausfallkanal ergänzt die verlorene Masse. Ohne Auswahl des Ausleseergebnisses bleibt (8,4,1)/13 bestehen.')
    p('Die Kanäle sind eine erklärte Mess-/Randentscheidung. Ihre unendliche Projektion ist nicht automatisch eine normalisierte finale Dichtematrix. Gravitative Rückwirkung, Staubbewegung oder ein Bounce folgen aus diesem Interferenztest nicht.','s')

    page()
    h('4 · Kontinuierliche Gravitationsphase mit Restschranke')
    p('Für μ=0 hängt die Phase nur von der Ordnung ab. Die natürlichen Ordnungen bis n=6 werden vollständig enumeriert: 1, 1, 2, 7, 40, 357 und 4.824. Alle Werte bei g=kπ/2 sind rational-komplex exakt; die Tabelle ist nur zur Lesbarkeit gerundet.')
    rows=[['α','g','Erfolg: alle Zahlen','Erfolg: Zahlkanäle']]
    for x in cont['cases']:
        if x['gravity_quarter_turn']==3:continue
        rows.append([x['alpha'],['0','π/2','π'][x['gravity_quarter_turn']],
            f"{float(F(x['all_number_success'])):.9f}",f"{float(F(x['number_resolved_success'])):.9f}"])
    table(rows,[45,60,202,202],padding=6)
    p('Beide Gewichte sind zulässig, ergeben aber verschiedene Werte. Dies ist eine Empfindlichkeit gegenüber der zusätzlichen Modellentscheidung, keine physikalische Auswahl zwischen α=1 und α=2. Bei g=3π/2 ergeben sich dieselben Erfolgswerte wie bei g=π/2.','s')
    h('Weitere Elementzahlen sind kontrolliert')
    eq('Z<sub>∞</sub>−Z<sub>6</sub> ≤ δ = 1/604800<br/>t=δ/(Z<sub>6</sub>+δ), &nbsp; |A<sub>∞</sub>−A<sub>6</sub>| ≤ 2t<br/>|p<sub>all,∞</sub>−p<sub>all,6</sub>| ≤ 4t')
    p('Für die Zahlkanäle liegt der unbegrenzte Erfolgswert im Intervall [(1−t)p<sub>count,6</sub>, (1−t)p<sub>count,6</sub>+t]. Der Fehler der Allzahl-Erfolgswerte ist bei beiden Gewichten kleiner als 4,23·10<super>−6</super>. Exakte rationale Grenzen stehen in tail_bounds.json.')
    h('Keine künstliche Normalisierung eines dunklen Ausgangs')
    p('Hier ist Z<sub>6</sub>+δ&lt;2. Der leere Record dominiert stark genug, um für beliebige reelle Wirkungsphasen einen strikt positiven Erfolg abzusichern:')
    eq('p<sub>all,∞</sub> ≥ [2/(Z<sub>6</sub>+δ)−1]² &gt; 0<br/>p<sub>count,∞</sub> ≥ 1/(Z<sub>6</sub>+δ) &gt; 0')
    p('Diese Schranken gelten für die kurze Referenzpräparation. Sie sind weder ein universelles Nichtauslöschungsgesetz noch eine Aussage über Singularitäten. Kontrolliert wird der Elementzahlrest, nicht ein Quadraturfehler der kontinuierlichen Materiephase.','s')

    page()
    h('5 · Beide Wirkungsphasen: 921 exakte atomare Kontrollen')
    p('Ein gesondertes, vollständig deklariertes Maß verwendet vier Uhratome T=(−1,−1/2,0,1/2), je mit Masse 1/4, und Dichtemarken w=(0,1/2), je mit Masse 1/2. Strikt verschiedene Uhren und höchstens vier Elemente ergeben 921 Endrecords.')
    p('Die Phasen exp{iπ[kg(S<sub>g</sub>−1)+kd·32S<sub>d</sub>]/2} sind darauf exakt gaußsch rational. Geprüft werden sechs Paare (kg,kd) und beide α. Die vollständige Wirkung stimmt an jedem Record mit ihrer Inkrementrechnung überein.')
    table([
        ['Prüfung','Ergebnis'],
        ['Rücktransport einzelner Kanalkomponenten',f"{audit['pullback_component_checks']:,}".replace(',','.')+' exakte Gleichheiten'],
        ['Feste vergangene Funktionale an späteren Schnitten',str(audit['fixed_past_functional_cut_checks'])+' exakte Übereinstimmungen'],
        ['Positivität und Vollständigkeit','Erfolgs-/Komplementpaar bestanden; exakte Schur-Prüfung'],
        ['Funktionale','Hermitesch, stark positiv, additiv; Grad-zwei-Regel bestanden'],
        ['Terminale Elementzahlpartition','Bei Zahlkanälen exakt mittel-dekohärent'],
        ['Frühere Drei-Ereignis-Partition','In allen 12 Fällen bei beiden Auslesen nicht mittel-dekohärent'],
    ],[300,209],padding=6)
    h('Ein Beispiel mit nichtverschwindender Materiephase')
    x=next(x for x in audit['cases'] if x['alpha']==1 and x['phase_indices']==[1,1])
    p('Für α=1, kg=kd=1 ergibt sich gerundet p<sub>all</sub>='+f"{float(F(x['all_number_success'])):.9f}"+' und p<sub>count</sub>='+f"{float(F(x['number_channel_success'])):.9f}"+'. Diese Werte gehören ausschließlich zum erklärten atomaren Maß.')
    p('Der Rücktransport wird über fünf Schnitte mit 1, 3, 13, 87 und 921 Präfixrecords geprüft. Das vergangene Ereignis bleibt stets die Zahl 0, 1 oder 2 am Schnitt T=−1/4; es wird an diesem und beiden späteren Schnitten verglichen.')
    p('<b>Keine Kontinuumsquadratur:</b> Das atomare Maß zertifiziert algebraische Identitäten mit beiden Wirkungsphasen. Das kontinuierliche Integral bei μ≠0 wurde nicht ausgewertet. Eine vierdimensionale CST-Population wurde weder simuliert noch aus diesen Records abgeleitet.','s')

    page()
    h('6 · Nachrechenbar, mit klarer Grenze zur offenen Physik')
    p('Die sechs Ergebnisdateien wurden aus Quellcode, eingefrorenem Plan und sechs gepinnten Eingaben in einem frischen Verzeichnis neu erzeugt. Der Vergleich ist für alle sechs Dateien bytegleich. Prüfsummen sichern Eingaben und ausgeliefertes Paket.')
    table([
        ['Evidenz','Einordnung'],
        ['Analytische Definitionen und Beweise','Beschränkte Instrumente, Rücktransport, Ranghindernis, Restschranken'],
        ['Exakte Rechnungen','Kontinuierliche Gravitationsphase; getrennte atomare Materiephasen-Kontrolle'],
        ['Isolierter Replay',replay['isolated_replay']+' · '+str(replay['result_files'])+' bytegleiche Ergebnisdateien'],
        ['Wissenschaftliche Unabhängigkeit','Keine externe Replikation, kein formaler Beweisprüfer'],
        ['Plan','Lokal vor Enumeration eingefroren; keine externe Präregistrierung'],
    ],[185,324],padding=6)
    h('Der nächste Entscheidungspunkt')
    p('Die Rand-Auslese und die dazu passende Ereignisalgebra müssen operational oder dynamisch begründet werden. Danach folgen die kontinuierliche Materiephase mit kontrollierten Integrationsfehlern sowie Robustheit gegenüber Zahlgewichtung und Enduhrwert. Eine neue Randannahme muss als solche ausgewiesen bleiben.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION: HOLD.</b> Auch BOUNDARY bleibt offen: Ein zulässiger Referenzeffekt ersetzt kein abgeleitetes Innen-/Außenraumgesetz.','s')
    h('Nachrechnung und Quellen')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/><font name="DVM">python3 -B verify_package.py</font>','s')
    p('[1] Gell-Mann, Hartle, <i>Time Symmetry and Asymmetry in Quantum Mechanics and Quantum Cosmology</i>. <link href="https://arxiv.org/abs/gr-qc/9304023v2" color="#17445e">arXiv:gr-qc/9304023v2</link>. Kontext für Randbedingungen und dekohärente Historien; keine Auswahl unseres Instruments.<br/>[2] Dowker, Johnston, Surya, <i>On extending the Quantum Measure</i>. <link href="https://arxiv.org/abs/1007.2725v1" color="#17445e">arXiv:1007.2725v1</link>. Erweiterungsprobleme über endliche Ereignisfragen hinaus. Hier wird kein unendliches Zeitmaß hergeleitet.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,
        rightMargin=43,topMargin=43,bottomMargin=64,
        title='CST-DUST: Kohärente Randauslese und Dekohärenz v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))


if __name__=='__main__':main()


