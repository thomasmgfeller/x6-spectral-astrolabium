"""Ten-page scoped research report. Exact evidence lives in JSON and proofs."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
S=json.loads((ROOT/'results/verification.json').read_text())
I=json.loads((ROOT/'results/independent_verification.json').read_text())
audit=json.loads((ROOT/'results/checkpoint_P5_audit.json').read_text())
if not S['all_exact_residuals_zero'] or I['status']!='PASS_IMPLEMENTATION_CROSSCHECK' or set(audit['decisions'].values())!={'HOLD'}:
    raise RuntimeError('Report requires completed scoped verification')

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
navy='#173e50'; teal='#167c70'; amber='#a6532f'; gray='#5a6d76'
fig,axes=plt.subplots(1,2,figsize=(7,2.8),layout='constrained')
for ax,title,pos,edges in [
    (axes[0],'V: zwei Vorgänger',{0:(-.6,0),1:(.6,0),2:(0,1)},[(0,2),(1,2)]),
    (axes[1],'V*: zwei Nachfolger',{0:(0,0),1:(-.6,1),2:(.6,1)},[(0,1),(0,2)])]:
    for a,b in edges:
        ax.annotate('',xy=pos[b],xytext=pos[a],arrowprops={'arrowstyle':'-|>','color':navy,'lw':1.8,'shrinkA':14,'shrinkB':14})
    for k,(x,y) in pos.items():
        ax.scatter([x],[y],s=450,color=teal,zorder=3)
        ax.text(x,y,str(k),color='white',ha='center',va='center',fontsize=11,zorder=4)
    ax.text(0,-.38,'N = 3     F₄ = 1     |Aut| = 2',ha='center',color=navy,fontsize=9)
    ax.set(title=title,xlim=(-1,1),ylim=(-.55,1.35));ax.axis('off')
fig.suptitle('Gleiche grobe Daten, verschiedene Zukunftskerne',color=navy,fontsize=11)
fig.savefig(FIG/'coarse_state_counterexample.png',dpi=190,facecolor='white');plt.close(fig)

fig,ax=plt.subplots(figsize=(7,1.65),layout='constrained')
for x,label,color in [(0,'a',teal),(1,'b',amber),(2,'c',teal)]:
    ax.scatter([x],[0],s=600,color=color,zorder=3)
    ax.text(x,0,label,ha='center',va='center',color='white',fontsize=13,zorder=4)
    ax.text(x,-.24,'Block A' if label!='b' else 'Block B',ha='center',color=color,fontsize=9)
for x in (0,1):
    ax.annotate('',xy=(x+1,0),xytext=(x,0),arrowprops={'arrowstyle':'-|>','lw':1.8,'color':navy,'shrinkA':17,'shrinkB':17})
ax.annotate('',xy=(2,.03),xytext=(0,.03),arrowprops={'arrowstyle':'-|>','lw':1.2,'color':gray,'connectionstyle':'arc3,rad=-.20','shrinkA':18,'shrinkB':18,'linestyle':'--'})
ax.text(1,.49,'Paar (a,c): ein Zwischenpunkt in C, keiner in A',ha='center',color=navy,fontsize=9)
ax.set(xlim=(-.45,2.45),ylim=(-.4,.68));ax.axis('off')
fig.savefig(FIG/'internal_interval_change.png',dpi=190,facecolor='white');plt.close(fig)

fonts=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
blue=colors.HexColor(navy);green=colors.HexColor(teal);muted=colors.HexColor(gray)
st=getSampleStyleSheet()
st.add(ParagraphStyle(name='B',fontName='DV',fontSize=10.2,leading=14.8,textColor=blue,spaceAfter=8))
st.add(ParagraphStyle(name='S',parent=st['B'],fontSize=8.6,leading=12.3,spaceAfter=6))
st.add(ParagraphStyle(name='T',fontName='DVB',fontSize=21,leading=27,textColor=blue,spaceAfter=14))
st.add(ParagraphStyle(name='H',fontName='DVB',fontSize=11.2,leading=15,textColor=green,spaceBefore=6,spaceAfter=7))
st.add(ParagraphStyle(name='E',parent=st['B'],fontSize=10,leading=16,backColor=colors.HexColor('#edf3f5'),borderPadding=8,spaceBefore=4,spaceAfter=13))
st.add(ParagraphStyle(name='C',parent=st['B'],fontSize=8.8,leading=12.5,spaceAfter=0))
st.add(ParagraphStyle(name='L',parent=st['B'],fontName='DVB',fontSize=8.1,leading=12,textColor=green,spaceAfter=10))
story=[]
def p(t,style='B'):story.append(Paragraph(t,st[style]))
def h(t):p(t,'H')
def eq(t):p(t,'E')
def page(n,title):
    if story:story.append(PageBreak())
    p(f'CST-DUST · VERKLEBUNGSREGEL v0.1 / {n:02d}','L');p(title,'T')
def table(rows,widths):
    t=Table([[Paragraph(str(c),st['C']) for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef1')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,green),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cdd8dd'))]))
    story.append(t);story.append(Spacer(1,8))

page(1,'Ein exakter Baustein für den Anschluss')
p('Die BDG-Wirkung ist jetzt mit vollständiger Intervallinformation verklebt. Für ein ausdrücklich angenommenes Zählmaß sind auch die Symmetriefaktoren und Amplitudenkerne geschlossen. Das liefert einen überprüfbaren strukturellen Baustein für eine gemeinsame Innen-/Außenraum-Dynamik.')
eq('<b>Exakte endliche Wirkungsverklebung: PASS.</b><br/><b>Physikalisches CST-Staub-Anschlussgesetz: HOLD.</b><br/>Globaler Bounce und Regularität bleiben getrennt offen.')
table([['Frage','Ergebnis','Reichweite'],['Lassen sich zwei Teilordnungen exakt verkleben?','Ja: Kreuzbeiträge plus Änderungen interner Intervallklassen','Jede endliche Ordnung; allgemeiner algebraischer Beweis'],['Sind Maß und Amplituden konsistent zusammengesetzt?','Ja, unter dem angegebenen markierten Zählmaß','Festes N; kein abgeleitetes physikalisches Staubmaß'],['Genügen Volumen und Wirkungswert als Zustand?','Nein: explizites Gegenbeispiel','Exakte Fortsetzung im deklarierten endlichen Modell'],['Ist der CST-Bounce nun global bestätigt?','Nein: keine physikalische CST-Staubdynamik ausgeführt','Materie, Zustand, klassische Variation und Regularität offen']], [139,180,180])
h('Was der Schritt konkret liefert')
p('130 116 exakte Zweiblockprüfungen, 7 998 Assoziativitätsprüfungen, 1 549 markierte Bahnprüfungen und vollständig bestimmte 2+2-Amplitudenkerne. Eine zweite Enumeration bestätigt die Wirkungswerte und Kopplungen unabhängig von der ersten Implementierung.')
p('Die zugrunde liegende Biaktionsidee ist in der Literatur vorhanden [1]. Dieses Paket arbeitet isolierte gegenüber eingebetteten Teilordnungen, Symmetriefaktoren, Negativkontrollen und die Grenzen grober Zustandsdaten aus. Es beansprucht keinen neuen universellen CST-GHY-Term.')
p('Stand: 6. November 2026 · Basis: Main nach PR 243, Commit bc8c154be60c. Plan vor der Rechnung lokal fixiert; keine externe Präregistrierung. Keine neuen dynamischen Ensembles, Zufallsdaten oder bezahlten Läufe.','S')

page(2,'Die vollständige Wirkungsidentität')
p('C = A ⊔ B ist eine endliche strikte partielle Ordnung. A und B erhalten die aus C induzierten Relationen. k<sub>C</sub>(x,y) zählt Elemente strikt zwischen x und y. N<sub>k</sub> zählt Paare mit genau k solchen Elementen; Links tragen hier den Index 0.')
eq('F<sub>4</sub>(C) = |C| − N<sub>0</sub> + 9N<sub>1</sub> − 16N<sub>2</sub> + 8N<sub>3</sub><br/>S<sub>4</sub>/ℏ = κF<sub>4</sub>,   κ = (4/√6)(ℓ/ℓ<sub>P</sub>)²')
p('Dabei ist ℓ<sub>P</sub>² = 8πGℏ die rationalisierte Plancklänge bei c = 1 [1]. Die Gewichte w(k) sind −1, 9, −16, 8 für k = 0, 1, 2, 3 und sonst null. F(A), F(B) zählen ausschließlich Zwischenpunkte im jeweiligen Block.')
eq('<b>F(C) = F(A) + F(B) + X(A,B;C) + R(A,B;C)</b>')
p('<b>X</b> summiert w(k<sub>C</sub>) über Paare mit Endpunkten in verschiedenen Blöcken, in beiden möglichen Zeitrichtungen. <b>R</b> summiert w(k<sub>C</sub>) − w(k<sub>D</sub>) über Paare mit beiden Endpunkten in demselben Block D = A oder B.')
p('<b>Beweis.</b> Die Elementzahlen addieren sich. Die geordneten Paare zerfallen disjunkt in A-interne, B-interne und grenzüberschreitende Paare. R korrigiert bei den ersten beiden Klassen die Intervallgröße; X ergänzt die dritte Klasse. Der Beweis gilt für jedes Intervallgewicht.')
story.append(Image(str(FIG/'internal_interval_change.png'),width=499,height=118))
eq('Dreierkette: F(C) = 10;  F(A) = F(B) = 1<br/>X = −2,  R = 10.  Ohne R ergäbe die Rekonstruktion 0.')
p('Der interne Paarbeitrag (a,c) wechselt von −1 auf +9. Sind beide Blöcke ordnungskonvex, ist R = 0; bei allgemeinen Schnitten darf dies nicht vorausgesetzt werden. In der eingebetteten Konvention mit vollen C-Intervallen steckt R bereits in den Teilwirkungen und darf nicht nochmals addiert werden.','S')

page(3,'Zulässigkeit, Reihenfolge und Skalen')
h('Eine Vereinigung muss die vorgegebenen Teile erhalten')
p('Für feste induzierte A und B enthält G(A,B) genau die Kreuzrelationen, deren Vereinigung mit den inneren Relationen bereits eine irreflexive transitive Ordnung bildet. Die Einschränkungen auf A und B dürfen sich nicht ändern.')
eq('A = {a,c} als Antikette, B = {b}:<br/>a ≺ b ≺ c erzwingt a ≺ c und ist daher unzulässig.')
p('Blindes transitives Abschließen repariert hier nicht bloß die Verklebung, sondern verändert die vorgegebene Innenordnung. Die implementierten Kontrollen verwerfen diese Änderung sowie Zyklen und nichttransitive Vereinigungen.')
h('Assoziativität mit vollständigem Zwischenzustand')
eq('Δ(A,B) = F(A ∪ B) − F(A) − F(B)<br/>Δ(A,B) + Δ(A ∪ B,D)<br/>= Δ(B,D) + Δ(A,B ∪ D)<br/>= F(C) − F(A) − F(B) − F(D)')
p('Der Beweis ist Teleskopieren der Wirkungsdifferenzen. Jede Zwischenwirkung verwendet ihre tatsächliche induzierte Ordnung. Die 7 998 geordneten Dreiblockfälle bis N = 4 stimmen exakt überein. Ein Zwischenzustand aus nur N und F ist damit nicht legitimiert.')
h('Auch verschmierte Gewichte lassen sich exakt verkleben')
p('Schreibe F<sub>ε</sub> = √ε G<sub>ε</sub> mit G<sub>ε</sub> = N − ε Σ f<sub>4</sub>(k,ε). Für f<sub>4</sub> gilt die endliche Binomialsumme in DERIVATION.md, mit Koeffizienten (1, −9, 16, −8). Der Satz auf Seite 2 bleibt für w<sub>ε</sub> = −ε f<sub>4</sub> unverändert. Alle Teile verwenden dasselbe ε.')
p('6 372 rationale Kontrollen bei ε = 1/2 und 1/4 bis N = 4 ergeben exakt null Rest. Bei ε = 1 werden die ursprünglichen BDG-Gewichte wiedergewonnen.')
eq('<b>Dies ist keine physikalische Dichteverfeinerung.</b><br/>In 4D gilt ε = (ℓ/L<sub>k</sub>)⁴. Eine spätere Familie muss dieselben physikalischen Anfangs-, Materie- und Randdaten abgleichen.')
p('Beliebig gefärbte kleine Ordnungen definieren weder einen endlichen Staubball noch seinen zeitartigen Rand. Der Außenraum ist Teil der gemeinsamen Geschichte; ein äußerer Rechenrand ist davon zu unterscheiden.','S')

page(4,'Maß und Amplituden richtig zählen')
p('Die Kontrollannahme lautet: Alle beliebig gelabelten Ordnungen eines festen 2-Block-Größensektors werden gleich gezählt und durch n<sub>A</sub>! n<sub>B</sub>! dividiert. Isomorphismen müssen alle Block- und Materiemarken erhalten.')
eq('(1 / (n<sub>A</sub>! n<sub>B</sub>!)) Σ<sub>C gelabelt</sub> f(C)<br/>= Σ<sub>[C] markiert</sub> f(C) / |Aut<sub>A,B</sub>(C)|')
p('<b>Beweis.</b> Die markierungstreue Permutationsgruppe hat Ordnung n<sub>A</sub>! n<sub>B</sub>!. Jede Bahn enthält diese Anzahl dividiert durch die Stabilisatorgröße. Für invariantes f ergibt Summation über die Bahnen genau den rechten Ausdruck.')
table([['Beispiel','Erlaubte Symmetrie','Falsche Ersetzung'],['Viererantikette mit festen 2+2-Marken','|Aut<sub>A,B</sub>| = 2! · 2! = 4','|Aut| = 4! = 24 verwischt die Blockmarkierung'],['Weitere fixe Randlabels / Materiemarken','Gruppe neu aus den tatsächlich erhaltenen Marken bestimmen','Keine pauschale Übernahme des unmarkierten Faktors']], [160,173,166])
h('Komposition für feste innere Ordnungstypen')
eq('K<sub>AB</sub>(z) = Σ<sub>X ∈ G(A,B)</sub> z<super>ΔF(C<sub>X</sub>)</super><br/>Z<sub>nA,nB</sub>(z) = Σ<sub>[A],[B]</sub> [z<super>F(A)+F(B)</super> K<sub>AB</sub>(z) / (|Aut A| |Aut B|)]')
p('Jeder innere Typ besitzt n<sub>A</sub>!/|Aut A| beziehungsweise n<sub>B</sub>!/|Aut B| gelabelte Vertreter. Deren Verklebungsfasern sind bijektiv. Aufteilen der Gesamtsumme nach den inneren Typen liefert die Formel; dieselbe Argumentation gilt für drei Blöcke.')
p('Exakt geprüft: zehn Größensektoren, 1 549 markierte Bahnen und koeffizientenweise Gleichheit der direkten und quotientierten Summen. Ein konstanter Kopplungsfaktor ersetzt die verschiedenen Fasern nicht.')
eq('<b>Der Symmetriefaktor ist bedingt begründet.</b><br/>Ein physikalisches Staubmaß, Zustandsgewichte und Gewichte verschiedener N-Sektoren werden dadurch nicht ausgewählt.')
p('z ist zunächst formal und von null verschieden. Die Interpretation z = exp(iκ) erzeugt komplexe Amplituden, keine positiven Wahrscheinlichkeiten. Komposition über eine zeitartige Fläche ist nicht automatisch unitäre Zeitentwicklung.','S')

page(5,'Die Kopplung ist ausgerechnet')
p('Für alle vier Kombinationen zweier Zweierordnungen wurden sämtliche zulässigen Kreuzrelationen bestimmt. A steht in den Formeln für Antikette, K für Kette.')
table([['Typ A / B','Kreuzordnungen','K(1)','K(−1)','K(i)'],['Antikette / Antikette','35','35','3','−13'],['Antikette / Kette','26','26','0','5 − 11i'],['Kette / Antikette','26','26','0','5 − 11i'],['Kette / Kette','20','20','−4','2 + 8i']], [164,102,62,65,106])
eq('K<sub>AA</sub> = 2z<super>−4</super> + 8z<super>−3</super> + 16z<super>−2</super> + 8z<super>−1</super> + 1<br/>K<sub>AK</sub> = K<sub>KA</sub> = z<super>−19</super> + 4z<super>−2</super> + 4z<super>−1</super> + 1<br/>        + 8z<super>7</super> + 6z<super>8</super> + 2z<super>16</super><br/>K<sub>KK</sub> = 2z<super>−18</super> + z<super>−2</super> + 2z<super>−1</super> + 1 + 6z<br/>        + 4z<super>8</super> + 4z<super>17</super>')
h('Direkte und verklebte Gesamtsumme stimmen überein')
eq('Z<sub>2,2</sub> = 3z<super>−16</super> + 3/2 + 8z + 9z² + 9z³ + z⁴/4<br/>    + 12z<super>10</super> + 6z<super>11</super> + 6z<super>19</super>')
p('Diese Formel entsteht sowohl aus der direkten Summe über alle 219 gelabelten Viererordnungen dividiert durch 4 als auch aus den inneren Typen und Kernen. Der Vergleich erfolgt für jeden Laurent-Koeffizienten exakt.')
table([['Bei z = 1','Wert','Bedeutung'],['Vollständige Summe','219/4','Alle gemeinsamen Ordnungen'],['Produkt isolierter Summen','9/4','Kreuzkopplungen ausgelassen']], [210,83,206])
p('Die unterschiedlichen Fasergrößen 35, 26 und 20 zeigen bereits, dass ein einziger universeller Faktor nicht alle bedingten Kopplungen darstellen kann. Die Negativkontrolle ohne Kern wird verworfen.')
p('K<sub>AK</sub>(−1) = 0 ist eine exakte Auslöschung an einer Kontrollphase. Ein Ansatz −iℏ log K kann deshalb komplex, mehrdeutig oder undefiniert sein. Das ist noch kein Nachweis einer physikalischen Unterdrückung von Historien und kein lokales reelles Randpotential.','S')

page(6,'Volumen und Wirkung reichen nicht')
story.append(Image(str(FIG/'coarse_state_counterexample.png'),width=499,height=200))
p('Die Pfeile zeigen die Zukunftsrichtung. V und sein zeitliches Dual besitzen dieselbe Elementzahl, denselben BDG-Wirkungswert und gleich große Automorphismengruppen. Ergänzt wird jeweils ein neues maximales Element. Seine Vergangenheit muss ein Ordnungsideal sein.')
eq('L<sub>V</sub>(z) = z<super>−1</super> + 2 + z + z<super>18</super><br/>L<sub>V*</sub>(z) = z<super>−17</super> + 1 + z + 2z<super>9</super>')
p('Hier enthält ΔF die gesamte Wirkungsänderung einschließlich des neuen Elements. Gegenüber K<sub>AB</sub> ist deshalb der gemeinsame Einzelelementfaktor z noch enthalten. Dieser Faktor ändert den Unterschied zwischen den beiden Kernen nicht.')
table([['Kontrolle','V','V*'],['Anzahl zulässiger Erweiterungen','5','5'],['Amplitude bei z = 1','5','5'],['Amplitude bei z = i','1','1 + 2i']], [235,132,132])
eq('<b>Der Zustand (N, F<sub>4</sub>) ist für diese exakte<br/>Fortsetzungsregel nicht geschlossen.</b>')
p('Ein Modell, das beide Zustände ausschließlich durch N = 3 und F<sub>4</sub> = 1 beschreibt, muss ihnen denselben Zukunftskern zuweisen. Die vollständige Summe widerspricht dem. Selbst gleiche Anzahlen erlaubter Erweiterungen reichen nicht aus.')
p('Dies ist eine zeitliche Strukturkontrolle, keine Stauboberflächen-Simulation. Sie schließt Näherungsmodelle nicht pauschal aus: Diese müssen zusätzliche Zustandsdaten, Gedächtnis oder einen kontrollierten Fehler erklären. Eine Zeitumkehr wird hier nicht als zulässige Identifikation verwendet.','S')

page(7,'Variation und Strom: präzise Grenzen')
h('Endliche Änderung der Summationsvariablen')
p('In einer festen gelabelten Verklebungsfaser schaltet T eine bestimmte gerichtete Kreuzrelation um, sofern das Ergebnis wieder zulässig ist; sonst bleibt die Ordnung unverändert. T ist eine Involution.')
eq('Σ<sub>C</sub> z<super>F(C)</super> [ f(TC) z<super>F(TC)−F(C)</super> − f(C) ] = 0')
p('<b>Beweis.</b> Der erste Summand ist f(TC)z<super>F(TC)</super>. Die Bijektion C → TC benennt die endliche Summe nur um. Getestet werden f = Zahl der Relationen und acht gerichtete Kreuzpaare pro 2+2-Faser: 32 Polynomidentitäten mit 400 nichttrivialen Bewegungsinstanzen.')
p('Bei allgemeinen Gewichten gehört auch deren Quotient w(TC)/w(C) hinein, einschließlich Maß, Materie und Zustand. An Nullgewichten wird die quotientfreie Summenform verwendet. Eine Formulierung direkt auf Isomorphieklassen braucht gesondert korrekte Moves und Symmetriefaktoren.')
eq('<b>Das ist eine Konsistenzidentität, kein Israel-Gesetz.</b><br/>Sie wählt keine physikalische Dynamik aus und fordert nicht ΔS = 0 für jede diskrete Mikrobewegung.')
h('Strombilanz auf demselben Gesamtkausalset')
eq('q<sub>i</sub> = Σ<sub>j</sub> j<sub>ij</sub> − Σ<sub>j</sub> j<sub>ji</sub><br/>Σ<sub>i ∈ A</sub> q<sub>i</sub> = Σ<sub>A → B</sub> j − Σ<sub>B → A</sub> j')
p('Interne Kanten heben sich paarweise auf; nur Kreuzkanten bleiben. Die 130 116 Kontrollen setzen Einheitsströme auf die Überdeckungsrelationen des vollen Kausalsets. Diese Ströme haben im Allgemeinen Quellen und sind keine Lösungen einer Staubdynamik.')
p('Für die Dreierkette gilt q = (1, 0, −1). Werden Kreuzkanten gelöscht, geht die Bilanz gegenüber den ursprünglichen Quellen verloren. Eine mitbewegte Staub-Vakuum-Grenze muss zusätzlich den passenden verschwindenden Materiefluss erfüllen.')
p('Die algebraische Bilanz wählt weder die physikalische Materialgrenze noch Vierergeschwindigkeit, Geodäten oder gravitative Rückwirkung. Restmassenerhaltung ist außerdem keine allgemeine lokale Erhaltung gravitativer Energie.','S')

page(8,'Die Brücke zu Israel und GHY')
p('GHY macht die klassische gravitative Variation mit vorgegebenen Randdaten wohldefiniert. Israel beschreibt den Anschluss einschließlich möglicher Oberflächenspannung. Gesucht ist dieser physikalische Zweck aus derselben CST-Gesamtdynamik.')
p('Raumartige CST-Randterme mit GHY-Grenzwert im Mittel sind bekannt [2]. Bei zeitartigen Gebietsgrenzen zeigt [1] Evidenz für eine mit ℓ<super>−1</super> divergierende mittlere Wirkung in den untersuchten Sprinkling-Situationen. Das ist weder ein allgemeiner Satz über Materiegrenzen noch ein fertiges Staub-Anschlussgesetz.')
h('Wirkungskonvergenz kontrolliert die Variation nicht')
eq('S<sub>n</sub>(q) = S(q) + sin(n²q)/n<br/>sup<sub>q</sub> |S<sub>n</sub> − S| ≤ 1/n<br/>(dS<sub>n</sub>/dq − dS/dq) bei q = 0 ist n.')
table([['n','Schranke des Wirkungsfehlers','Variationsfehler bei q = 0'],['1','1','1'],['2','1/2','2'],['4','1/4','4'],['8','1/8','8'],['16','1/16','16']], [64,220,215])
p('Das Gegenbeispiel widerlegt eine allgemeine Schlussregel, nicht CST. Für den Anschluss müssen effektive Gesamtwirkung und erste Variation gemeinsam auf einer physikalisch abgeglichenen Familie kontrolliert werden, einschließlich Fluktuationen, Nichtlokalität und Zustand.')
h('Bedingte klassische Zielgleichung')
eq('[h<sub>ab</sub>] = 0,    [K<sub>ab</sub> − K h<sub>ab</sub>] = −8πG S<super>Σ</super><sub>ab</sub>')
p('Signatur (−+++), zeitartige Fläche, K<sub>ab</sub> = h<sub>a</sub><super>μ</super>h<sub>b</sub><super>ν</super>∇<sub>μ</sub>n<sub>ν</sub>, gemeinsame Normale vom Inneren zum Äußeren und [Q] = Q<sub>+</sub> − Q<sub>−</sub>. Ohne dünne Schicht verschwindet die rechte Seite [3].')
p('Diese Gleichung folgt erst unter der zusätzlichen Annahme eines kontrollierten lokalen Einstein-Grenzfalls mit korrekten Randbeiträgen. Die endlichen Kontrollen beweisen diese Annahme nicht; in der Quantenzone wird die klassische Naht nicht vorgegeben.','S')

page(9,'Verifikation ohne Hochstufung')
table([['Prüfung','Umfang','Befund'],['Alle Ordnungen N = 1,...,5','4 473 gelabelt; 87 unmarkierte Typen','Keine 4D-Selektion'],['Vollständige Wirkung / Strom','Je 130 116 Zerlegungen','Rest exakt null'],['Verschmierte Wirkung','6 372 rationale Fälle','Rest exakt null'],['Dreiblock-Assoziativität','7 998 Fälle bis N = 4','Rest exakt null'],['Markiertes Zählmaß','10 Sektoren; 1 549 Bahnen','Exakte Gleichheit'],['Kerne / Variationsidentitäten','4 / 32','Exakte Polynome'],['Struktur- / Gate-Kontrollen','13 / 5','Erwartete Resultate'],['Unabhängige Implementierung','4 473 Ordnungen; 130 116 Korrekturen','Vollständige Übereinstimmung']], [183,187,129])
p('Die zweite Implementierung erzeugt vorwärts gerichtete Graphen, schließt transitiv ab und permutiert alle Labels. Sie zählt Zwischenpunkte unabhängig mit Mengen. Der erste Generator prüft dagegen alle drei möglichen Beziehungen jedes ungeordneten Paares.')
p('Naive Additivität ohne Kopplung scheitert in 122 960 Zerlegungen; alleinige Kreuzpaarkorrektur ohne R in 45 888. Das sind kombinatorische Häufigkeiten, keine physikalischen Fehlerraten oder unabhängigen Stichproben.')
h('Ein neuer, eng abgegrenzter P5-Datensatz')
eq('MODEL · CURRENT · CORRESPONDENCE · BOUNCE<br/>REGULARITY · BOUNDARY · TRAPPING · EXTENSION<br/><b>Alle acht physikalischen Entscheidungen: HOLD.</b>')
p('Der unveränderte Model-Contract-Auditor wertet diesen Teilumfang aus. Frühere klassische Nachweise behalten ihren eigenen Geltungsbereich. Der Auditor prüft erklärte Nachweiskategorien, keine Beweise. Fünf ausdrücklich synthetische Tests verhindern, dass endliche Beobachtungen geschützte Regularitäts- oder Fortsetzungsanforderungen ersetzen.')
p('Plan und übernommene Eingaben sind hashgeschützt. Die Ergebnisse werden mit Python im Optimierungsmodus reproduziert; explizite Prüfungen bleiben dabei aktiv. Ein isolierter Wiederholungslauf dient zusätzlich der Paketkontrolle.','S')

page(10,'Physikalischer Engpass und Prüfpaket')
eq('W(C,φ) = μ(C,φ) Ψ<sub>∂</sub>(C,φ)<br/>     × exp{i [S<sub>BDG</sub>(C) + S<sub>dust</sub>(C,φ)] / ℏ}')
p('Diese Schreibweise benennt die noch zu bestimmenden Zutaten: diskrete Staubvariablen, Materiewirkung, begründetes Maß und Randzustand. Die zugehörigen Materie-Kreuzkopplungen fehlen in der rein gravitativen Kontrollsumme. Auch ein Dekohärenz- oder Wahrscheinlichkeitsverfahren ist nötig, bevor von einer Bounce-Wahrscheinlichkeit gesprochen werden kann.')
p('<b>Nächste Prüfung:</b> Zuerst den endlichen Staubball im regulären klassischen Bereich aus einer solchen gemeinsamen Dynamik untersuchen, einschließlich erster Randvariation und physikalisch abgeglichener Verfeinerung. Erst danach werden Hochkrümmung, Regularität, globale Fortsetzung und Bounce entschieden. Toleranzen und Abbruchregeln werden vor dieser neuen Rechnung festgelegt.')
h('Reproduzieren')
eq('python3 -O -B analyze.py<br/>python3 -O -B verify_independent.py')
p('Die exakten Prüfungen brauchen nur die Python-Standardbibliothek. Referenz: Python 3.12.14. DERIVATION.md enthält die vollständigen Beweise; results/ die CSV- und JSON-Daten; inputs/ unveränderte Vorarbeiten mit Herkunft. SHA256SUMS prüft die Integrität des gelieferten Paketstands.')
p('Der optionale Berichtsbau verwendet Matplotlib 3.10.8, ReportLab 4.4.9 und DejaVu Sans. Die Abbildungen stellen exakte kleine Ordnungen dar; sie liefern keine zusätzliche numerische Evidenz.','S')
h('Primärquellen')
p('[1] F. Dowker, R. Liu, D. Lloyd-Jones: <b>Timelike boundary and corner terms in the causal set action.</b> arXiv:2501.00139v2, 25.04.2025. Biaktion, isoliertes/eingebettetes Regime, Anhang A.<br/><link href="https://arxiv.org/html/2501.00139v2" color="#167c70">https://arxiv.org/html/2501.00139v2</link>','S')
p('[2] M. Buck, F. Dowker, I. Jubb, S. Surya: <b>Boundary Terms for Causal Sets.</b> arXiv:1502.05388v2, 29.10.2015.<br/><link href="https://arxiv.org/abs/1502.05388v2" color="#167c70">https://arxiv.org/abs/1502.05388v2</link>','S')
p('[3] P. Musgrave, K. Lake: <b>Junctions and thin shells in general relativity using computer algebra I: The Darmois-Israel Formalism.</b> Class. Quantum Grav. 13 (1996), 1885–1900.<br/><link href="https://arxiv.org/abs/gr-qc/9510052v3" color="#167c70">https://arxiv.org/abs/gr-qc/9510052v3</link>','S')
p('Projektbasis: thomasmgfeller/x6-spectral-astrolabium<br/>Main: bc8c154be60c483c8a5a8f085c1b3b0668d8afa1<br/>Plan-SHA-256: 67f4c8fad70b29f6ac745c6a05a45ff91510397d7ed0383d8d27c4cde6c81cb4','S')

def footer(c,doc):
    c.saveState();c.setStrokeColor(colors.HexColor('#cdd8dd'));c.line(48,42,547,42)
    c.setFont('DV',7.3);c.setFillColor(muted)
    c.drawString(48,29,'CST-DUST-GLUING-001  ·  06.11.2026  ·  Exakte Struktur, physikalische Naht offen')
    c.drawRightString(547,29,str(doc.page));c.restoreState()
def deterministic_canvas(*args,**kwargs):
    kwargs['invariant']=1
    return canvas.Canvas(*args,**kwargs)
out=ROOT/'CST_DUST_Verklebungsregel_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=57,
                      title='CST-DUST-Verklebungsregel v0.1',author='Thomas Gfeller · X6 Forschungsprogramm')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=deterministic_canvas)
print(out)
