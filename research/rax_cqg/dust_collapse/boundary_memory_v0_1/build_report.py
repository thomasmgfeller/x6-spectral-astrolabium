#!/usr/bin/env python3
"""Build the summary PDF and a schematic exact-order counterexample."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
NAME='CST_DUST_Randgedaechtnis_Fortsetzung_v0_1'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
BLUE=colors.HexColor('#17445e');GRAY=colors.HexColor('#5b6670');PALE=colors.HexColor('#eef4f7')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=31,textColor=BLUE,spaceAfter=18),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=15,leading=19,textColor=BLUE,spaceBefore=11,spaceAfter=9),
 'b':ParagraphStyle('b',fontName='DV',fontSize=10.2,leading=15.1,spaceAfter=9),
 's':ParagraphStyle('s',fontName='DV',fontSize=8.2,leading=11.6,spaceAfter=7,textColor=GRAY),
 'eq':ParagraphStyle('eq',fontName='DV',fontSize=11.3,leading=17,spaceBefore=7,spaceAfter=12,leftIndent=10,textColor=BLUE),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.5,leading=12),
}
story=[]
def p(t,s='b'):story.append(Paragraph(t,styles[s]))
def h(t):p(t,'h')
def eq(t):p(t,'eq')
def page():story.append(PageBreak())
def table(rows,widths,padding=8):
    t=Table([[Paragraph(str(x),styles['cell']) for x in row] for row in rows],colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
       ('TOPPADDING',(0,0),(-1,-1),padding),('BOTTOMPADDING',(0,0),(-1,-1),padding),
       ('LINEBELOW',(0,0),(-1,0),.7,BLUE),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d6dee3'))]))
    story.append(t);story.append(Spacer(1,10))
def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#d6dee3'));c.line(43,49,552,49)
    c.setFont('DV',8);c.setFillColor(GRAY);c.drawString(43,35,'CST-DUST • Randgedächtnis v0.1 • 7. November 2026');c.drawRightString(552,35,str(doc.page))
def figure():
    path=ROOT/'figures';path.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(7.6,3.55));ax.set_xlim(-1.3,3.9);ax.set_ylim(-.6,4.7);ax.axis('off')
    ax.add_patch(FancyBboxPatch((-.45,1.65),1.05,2.75,boxstyle='round,pad=0.05',facecolor='#e7f0f5',edgecolor='#537d93'))
    coords={'a':(0,0),'y':(0,1),'c₁':(0,2),'c₂':(0,3),'c₃':(0,4),'z':(2.1,2.7)}
    for u,v in [('a','y'),('y','c₁'),('c₁','c₂'),('c₂','c₃'),('y','z')]:
        x1,y1=coords[u];x2,y2=coords[v]
        ax.annotate('',xy=(x2,y2-.12),xytext=(x1,y1+.12),arrowprops={'arrowstyle':'->','lw':1.7,'color':'#354d5c'})
    for name,(x,y) in coords.items():
        color='#b44434' if name=='y' else '#2c7882' if name=='z' else '#17445e'
        ax.scatter([x],[y],s=125,color=color,zorder=3);ax.text(x-.24,y,name,ha='right',va='center',fontsize=12)
    ax.text(.77,3.75,'Gespeicherter Kragen\nc₁, c₂, c₃',fontsize=11,color='#17445e',va='center')
    ax.text(.25,.8,'Verborgene Vakuumuhr\nTᵧ = 1/4 oder 3/4',fontsize=11,color='#b44434',va='center')
    ax.text(2.37,2.7,'Neu: Tz = 1\nwz = 1/2',fontsize=11,color='#236c76',va='center')
    ax.text(2.0,1.25,'Vergangenheit von z: {a,y}\nΔS zwischen den Fällen: 1/16',fontsize=11,ha='center')
    ax.text(0,-.35,'Anfangsanker, Ta = −1',fontsize=10,ha='center',color='#5b6670')
    fig.tight_layout(pad=.5);fig.savefig(path/'hidden_clock_collar.png',dpi=190);plt.close(fig)
def main():
    figure()
    p('Randgedächtnis und<br/>exakte Fortsetzung','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Die endliche Amplitude lässt sich vollständig fortsetzen')
    p('Die vollständige Vergangenheit ist jetzt als <b>hinreichende Zustandsdarstellung</b> festgelegt. Ein neues maximales Element kann angefügt werden, ohne alte Intervalle, Uhren oder Materiemarken zu verlieren. Der Wirkungszuwachs und die korrekte Zählung natürlicher Geburtslabels sind exakt hergeleitet und geprüft.')
    p('Dies ist eine <b>Umschreibung des bestehenden Modells</b> bei festem endlichem Elementzahlsektor. Die Geburtsnummer ist keine physikalische Eigenzeit; eine neue Wachstumsdynamik wird nicht postuliert.')
    table([['Gewonnener Baustein','Ergebnis'],['Vollständiges Gedächtnis','Exakte Wirkungserweiterung; alter Feldinhalt bleibt erhalten'],['Korrektes Zählmaß','1/e(P) verhindert Mehrfachgewichtung durch natürliche Labels'],['Fortsetzungsoperator','Kein beschränkter integrierter Kern in allen alten und neuen Variablen; früheres Kompaktheitshindernis greift hier nicht'],['Unabhängige physikalische Norm','Weiterhin offen; lokale Normierung verändert die ursprünglichen Amplituden']], [174,335])
    h('Geprüfte Grenze')
    p('Vier Intervallschichten bedeuten nicht vier ausreichende Randlagen. Für jeden festen oberen Kragen gibt es erlaubte Fortsetzungen, die von einer tiefer liegenden Vakuumuhr abhängen. Eine allgemeine Gegenbeispielfamilie zeigt einen exakten Wirkungsunterschied von 1/16.')
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein Nachweis eines CST-Junction-Gesetzes, eines globalen Bounce oder einer Singularitätsauflösung. Die physikalische Randnorm und der Umgang mit redundanten Geburtslabels bleiben eigenständige Aufgaben.','s')
    p('Basis: Main 886052d8eb9d619da91896d23e0a7ede511ef30f, nach PR 248. Vollständige Beweise und reproduzierbarer Code liegen im Prüfpaket.','s')

    page();h('1 · Zustandsvertrag und exakter Wirkungszuwachs')
    p('Der Anfangsanker a bleibt unter allen inneren Elementen. Die vollständige innere Ordnung P mit sämtlichen T- und w-Feldern wird gespeichert. Ein neues maximales Element z erhält als Vergangenheit I={a}∪J, wobei J ein beliebiges Ordnungsideal von P ist. Der Endanker f wird erst beim Abschluss über alle inneren Elemente gesetzt.')
    p('Ordnungsideal bedeutet: Liegt x in J, so liegen auch alle Vorgänger von x in J. Die Konstruktion bewahrt die geerbten Feldmaße und äußeren Marken. Vakuumuhren werden nicht allein wegen w=0 entfernt.')
    h('Die nötigen Daten für einen vorgeschlagenen Schritt')
    eq('k<sub>y</sub> = |{u∈I : y≺u}|<br/>n<sub>k</sub> = Σ<sub>y∈I</sub>1<sub>ky=k</sub>, &nbsp; M<sub>k</sub><super>(j)</super> = Σ<sub>y∈I, ky=k</sub>T<sub>y</sub><super>j</super>')
    p('Mit b=(1,−9,16,−8), T<sub>z</sub>=t und w<sub>z</sub>=w gilt im verwendeten Einheitenmaß A=ℏ=1:')
    eq('ΔF₄ = 1 − Σ<sub>k=0</sub><super>3</super>b<sub>k</sub>n<sub>k</sub><br/>ΔS<sub>d</sub> = −w/2 − (w/4)Σ<sub>k=0</sub><super>3</super>b<sub>k</sub>[n<sub>k</sub>t²−2M<sub>k</sub><super>(1)</super>t+M<sub>k</sub><super>(2)</super>]')
    p('<b>Beweis:</b> Ein neues maximales Element liegt in keinem Intervall zwischen alten Elementen. Alle alten Paarbeiträge bleiben deshalb unverändert. Neu sind nur z, seine Dichtekonstante und die Paare y≺z. Ausmultiplizieren und Gruppieren nach k<sub>y</sub> liefert die Formeln.')
    h('Was die Momentformel nicht behauptet')
    p('Die zwölf Momente genügen für dieses vorgeschlagene I. Für andere zukünftige Ideale und deren Zulässigkeit wird weitere Ordnungsinformation benötigt. Weder ist dies eine universelle endliche Kompression noch ist die vollständige Vergangenheit als minimal bewiesen.')
    p('408 natürliche Ordnungen und 407 zulässige Erweiterungen wurden vollständig erfasst. 2 442 rationale Wirkungsfälle stimmen mit dem geerbten direkten Rechner überein. Zwei unvergleichbare Geburten liefern bei vertauschter Reihenfolge dieselbe Endwirkung; 268 Austauschdiamanten mit 536 Feldprüfungen bestätigen dies.')
    p('w bleibt ein integriertes Dichtegewicht, keine kalibrierte Ruhemasse. Die frühere offene physikalische Begründung äußerer Randterme wird durch diese Identitäten nicht ersetzt.','s')

    page();h('2 · Eine tiefe Vakuumuhr bleibt relevant')
    p('Betrachte dieselbe alte Kette a≺y≺c₁≺…≺c<sub>r</sub>. Gespeichert seien a und nur die letzten r inneren Ordnungslagen. Alle alten Dichten sind null. Die verborgene Uhr y hat entweder den Wert 1/4 oder 3/4; Ordnung, alte Wirkung und sichtbarer Kragen sind identisch.')
    story.append(Image(str(ROOT/'figures/hidden_clock_collar.png'),width=509,height=238))
    p('Ordnungsdiagramm für r=3; die Positionen sind keine Raumzeitkoordinaten. Pfeile zeigen Überdeckungsrelationen. Die neue Verzweigung ist zu den sichtbaren c-Knoten unvergleichbar.','s')
    p('Das neue Element z hat die erlaubte Vergangenheit {a,y}, Uhrwert 1 und Dichtegewicht 1/2. y wird dadurch zu einem direkten Vorgänger von z, unabhängig von seinem Abstand zum bisherigen oberen Rand.')
    eq('S<sub>d</sub><super>(3/4)</super>−S<sub>d</sub><super>(1/4)</super><br/>= −(1/8)[(1−3/4)²−(1−1/4)²] = 1/16')
    p('Die gemeinsamen gravitativen und übrigen Beiträge heben sich im Vergleich auf. Ein später identisch angefügter Endanker mit w<sub>f</sub>=0 bewahrt den Unterschied. Alle Uhren der Familie liegen in der früheren Hilfsbox L=4.')
    p('<b>Ergebnis:</b> Kein festes r garantiert die exakte Fortsetzung für alle zulässigen zukünftigen Ideale. Acht rationale Fälle r=1,…,8 prüfen die allgemeine Familie. Kleinere Zustände mit zusätzlicher Information, eingeschränkte Träger oder kontrollierte Näherungen sind dadurch nicht ausgeschlossen.')

    page();h('3 · Geburtsreihenfolgen richtig zählen')
    p('e(P) ist die Zahl der linearen Erweiterungen der m inneren Elemente. Für einen invariant mittransformierten Integranden gilt bei fixierten äußeren Ankern:')
    eq('(1/m!) Σ<sub>P beliebig gelabelt</sub>I(P)<br/>= Σ<sub>P natürlich gelabelt</sub>I(P)/e(P)')
    p('<b>Beweis:</b> Ein Isomorphietyp hat m!/|Aut(P)| beliebig gelabelte und e(P)/|Aut(P)| natürlich gelabelte Vertreter. Beide korrekt gewichteten Summen ergeben I(P)/|Aut(P)|. Vollständige Materiemarken und kontinuierliche Felder werden gemeinsam umbenannt; ihre symmetrischen Maße bleiben erhalten.')
    table([['Zwei innere Elemente','e(P)','Korrektes Endgewicht'],['Kette zwischen a und f','1','z³'],['Antikette zwischen a und f','2','½ z⁻¹⁶']], [230,60,219])
    eq('Z₂(z)=z³+½z⁻¹⁶, &nbsp; z=exp(iκ)')
    p('Unkorrigierte natürliche Zählung ergäbe z³+z⁻¹⁶. Sie verändert das relative Gewicht. Die Verwendung natürlicher Labels allein ist daher keine Reduktion mit unverändertem Einheitsgewicht.')
    h('Schrittweise Zerlegung des richtigen Faktors')
    eq('r(P→P′)=e(P)/e(P′)<br/>Π<sub>Schritte</sub>r = 1/e(P<sub>Ende</sub>)')
    p('Die Verhältnisse teleskopieren. Gemeinsam mit den Wirkungszuwächsen, den vollständigen neuen Feldintegralen, dem Anfangsphasenfaktor und dem Endanker reproduzieren sie exakt die feste-m-Amplitude. Kein weiterer Automorphismenfaktor wird daneben eingefügt.')
    p('Sechs vollständige Sektorsummen m=0,…,5 stimmen als Laurentpolynome exakt mit der unabhängigen beliebigen Labelenumeration überein. Die natürlichen Zählzahlen lauten 1,1,2,7,40,357. Eine physikalische Auswahl von κ oder ein vierdimensionaler Grenzfall wurde dabei nicht getestet.')
    p('Natürliche Labels und Pfadunabhängigkeit sind bekannte CST-Strukturen [1]. Hier werden keine klassischen Übergangswahrscheinlichkeiten übernommen. Die unendliche Fortsetzung eines Quantenmaßes bleibt eine zusätzliche Frage [2].','s')

    page();h('4 · Fortsetzung mit erhaltenem Feldgedächtnis')
    p('Im Hilfsraum mit orthogonalen natürlichen Ordnungen und den normierten Feldmaßen wird die vollständige alte Konfiguration ξ behalten:')
    eq('(V<sub>m</sub>ψ)(P′,ξ,u)=r(P,P′) exp(iΔS/ℏ) ψ(P,ξ)')
    p('Die neuen Felder heißen u. In einer Kernschreibweise stehen Deltafaktoren in den alten Variablen. Dieser Operator gehört nicht zur früher untersuchten beschränkten integrierten Kernklasse. Das Kompaktheitshindernis greift hier deshalb nicht.')
    p('Das erklärte Produkt behandelt natürliche Beschreibungen orthogonal. Es ist kein qualifizierter physikalischer Labelquotient. Die korrekte Endamplitude summiert redundante Beschreibungen kohärent; eine physikalische Endkontraktion muss dies berücksichtigen.')
    h('Eine einzige Normierung genügt weiterhin nicht')
    eq('V<sub>m</sub><super>†</super>V<sub>m</sub>=Z<sub>m</sub>(P), &nbsp; Z<sub>m</sub>(P)=Σ<sub>Ideale J</sub>[e(P)/e(P′)]²')
    table([['Elternzustand','Exakter Normfaktor'],['Ein inneres Element','5/4'],['Zweierkette','49/36'],['Zweierantikette','2']], [290,219])
    p('V/√Z ist formal isometrisch, verändert aber die ursprünglichen Endamplituden. Für denselben Endtyp Kette plus isoliertes Element haben zwei Geburtsrouten danach die quadratischen Gewichte 16/245 und 2/45; zuvor waren beide 1/9.')
    h('Positive Produkte lassen sich zurückziehen')
    eq('h<sub>m</sub><super>[M]</super>(P)=Σ<sub>J</sub> r(P,P′)² h<sub>m+1</sub><super>[M]</super>(P′)')
    p('Mit einem gewählten positiven Endprodukt bei M ist V zwischen diesen gewichteten Produkten isometrisch. Die Wahl bleibt jedoch frei: Bei M=3 und Endgewicht 1 ergeben sich 49/36 und 2; beim Endgewicht 1+Relationenanzahl dagegen 179/36 und 44/9 für Kette und Antikette.')
    p('30 Kontrollen bei zwei Horizonten und zwei Endprodukten bestätigen diese endlichen Identitäten. Sie wählen kein physikalisches Produkt aus und beweisen keinen unendlichen konsistenten Normpfad.','s')

    page();h('5 · Verifikation und nächste Entscheidung')
    table([['Prüfung','Umfang'],['Natürliche innere Ordnungen / Erweiterungen','408 / 407'],['Rationale Wirkungszuwächse','2 442'],['Direkte Endwirkungen / lineare Erweiterungszählung','408 / 408'],['Austauschdiamanten / Feldprüfungen','268 / 536'],['Abschließende Endanker-Prüfungen','816'],['Vollständige Labelsummen','6 Sektoren'],['Kragen-Gegenbeispiele / positive Endprodukt-Rückzüge','8 / 30'],['Isolierte Nachrechnung','5 exakte Ergebnisdateien bytegleich']], [300,209],padding=4)
    p('Ein zusätzlicher Hilfsrecord-Test trennt Gesamtnorm und Ereigniskonsistenz: Der erreichbare Record „erste zwei innere Geburten bilden eine Kette“ ändert unter Fortsetzung und erneuter Gesamtnormierung sein Gewicht von 4/5 auf 49/67. Dieser Record ist nicht als physikalisch kovariantes Ereignis qualifiziert.')
    h('Die nächste konkrete Forschungsfrage')
    p('<b>Besitzt die Gedächtnisfortsetzung einen begründeten positiven Normpfad, dessen Horizontabhängigkeit kontrolliert ist und der die ursprünglichen relativen Amplituden sowie die Redundanz der Geburtslabels erhält?</b> Dafür sind Endwahlabhängigkeit, relative Normverhältnisse und erlaubte Ereignisidentifikationen zu prüfen.')
    p('Der vollständige Gedächtnisvertrag ist jetzt konkret. Die unabhängige physikalische Normauswahl bleibt offen. Eine lokale Nachnormierung darf nicht als unveränderte alte Dynamik ausgegeben werden. Auch ein erfolgreicher Normpfad würde klassische Korrespondenz, Innen-/Außenraum-Naht und Regularität noch nicht ersetzen.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION: jeweils HOLD.</b> Keine neuen physikalischen 4D-Ensembles und keine Singularitätsauflösung.')
    h('Nachrechnung und Herkunft')
    p('<font name="DVM">python3 -O -B analyze.py</font><br/><font name="DVM">python3 -O -B replay.py</font><br/>Python 3.10+, nur Standardbibliothek. Sieben Vorgängerquellen sind bytegleich auf Main nach PR 248 gepinnt. Plan und Paket enthalten SHA-256-Hashes.','s')
    p('Lokaler Plan vor der Rechnung; erwartete Mechanismen waren bekannt. Keine externe Präregistrierung, blinde Vorhersage oder formale Beweisassistentenprüfung. Allgemeine Beweise und der genaue Vertrag stehen in DERIVATION.md und boundary_contract.json.','s')
    p('[1] Rideout, Sorkin, A Classical Sequential Growth Dynamics for Causal Sets, Phys. Rev. D 61, 024002 (2000), arXiv:gr-qc/9904062v3.<br/>[2] Surya, Zalel, A Criterion for Covariance in Complex Sequential Growth Models (2020), arXiv:2003.11311v1. Die speziellen Literaturmodelle werden nicht mit unserer BDG-Staubamplitude gleichgesetzt.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,rightMargin=43,topMargin=43,bottomMargin=64,title='CST-DUST: Randgedächtnis und exakte Fortsetzung v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))
if __name__=='__main__':main()
