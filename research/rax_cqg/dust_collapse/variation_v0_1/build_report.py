"""Render the scoped variation result; plotting is illustrative, not evidence."""
from pathlib import Path
import json,math,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image

ROOT=Path(__file__).resolve().parent
TARGET=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'output/pdf/CST_DUST_Physikalische_Variation_v0_1.pdf'
TARGET.parent.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
S=json.loads((ROOT/'results/verification.json').read_text())
N=json.loads((ROOT/'results/normalization_counterexample.json').read_text())
AUDIT=json.loads((ROOT/'results/checkpoint_P1_audit.json').read_text())
if S['exact_variation_residuals']!='ZERO' or AUDIT['decisions']['MODEL']!='FAIL':
    raise RuntimeError('Report requires scoped completed result')
navy='#173e50';teal='#167c70';amber='#ad5636';gray='#5a6d76'
gram=N['gram'];c=(float(gram[0][0]['real'])+float(gram[1][1]['real']))/2
u=float(gram[0][1]['real']);v=float(gram[0][1]['imag']);n0=c+u
xs=[2*math.pi*i/400 for i in range(401)]
ys=[(c+u*math.cos(j)-v*math.sin(j))/n0 for j in xs]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,ax=plt.subplots(figsize=(7,3.1),layout='constrained')
ax.axhline(1,color=gray,ls='--',lw=1.2,label='Erforderlich für normierte geschlossene Evolution')
ax.plot(xs,ys,color=teal,lw=2,label='Deklarierter roher Kern, feste Normierung bei J = 0')
ax.scatter([0,math.pi],[1,float(N['fixed_normalization_Z_pi_pi_interval'][0])],color=amber,zorder=3)
ax.set(xlim=(0,2*math.pi),ylim=(-.04,1.14),ylabel='Z[J, J]',xlabel='Eingangsquelle J')
ax.set_xticks([0,math.pi,2*math.pi],['0','π','2π'])
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
ax.legend(loc='upper right',fontsize=7.5,frameon=False)
fig.savefig(FIG/'fixed_normalization.png',dpi=190,facecolor='white');plt.close(fig)

fonts=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
blue=colors.HexColor(navy);green=colors.HexColor(teal)
st=getSampleStyleSheet()
st.add(ParagraphStyle(name='B',fontName='DV',fontSize=10,leading=14.5,textColor=blue,spaceAfter=8))
st.add(ParagraphStyle(name='S',parent=st['B'],fontSize=8.5,leading=12,spaceAfter=6))
st.add(ParagraphStyle(name='T',fontName='DVB',fontSize=21,leading=26,textColor=blue,spaceAfter=14))
st.add(ParagraphStyle(name='H',fontName='DVB',fontSize=11,leading=15,textColor=green,spaceBefore=5,spaceAfter=7))
st.add(ParagraphStyle(name='E',parent=st['B'],fontSize=10,leading=16,backColor=colors.HexColor('#edf3f5'),borderPadding=8,spaceBefore=4,spaceAfter=13))
st.add(ParagraphStyle(name='C',parent=st['B'],fontSize=8.6,leading=12.2,spaceAfter=0))
st.add(ParagraphStyle(name='L',parent=st['B'],fontName='DVB',fontSize=8,leading=12,textColor=green,spaceAfter=9))
story=[]
def p(t,style='B'):story.append(Paragraph(t,st[style]))
def h(t):p(t,'H')
def eq(t):p(t,'E')
def page(n,title):
    if story:story.append(PageBreak())
    p(f'CST-DUST · VARIATION v0.1 / {n:02d}','L');p(title,'T')
def table(rows,widths):
    t=Table([[Paragraph(str(v),st['C']) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef1')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,green),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cdd8dd'))]))
    story.append(t);story.append(Spacer(1,8))

page(1,'Variationskandidat und Quantennormierung')
p('Die gemeinsame Geometrie-Staub-Amplitude ist als regulierter Kandidat definiert. Daraus sind die endlichen Wirkungsvariationen, ein Variationsstrom und eine bedingte Außenfeldantwort abgeleitet. Eine zusätzliche Prüfung zeigt, dass ihr roher Randkern mit dem festgelegten kinematischen Skalarprodukt keine geschlossene Quantenevolution darstellt.')
eq('<b>Gekoppelte endliche Wirkungsvariation: PASS.</b><br/><b>Roher Kern als Evolution im deklarierten Randraum: FAIL.</b><br/><b>Physikalisches Junction-Gesetz und Außenraum: HOLD.</b>')
table([['Ergebnis','Genaue Bedeutung'],['Konkrete Definition','Materiewirkung, Maß, Regulator, Träger und Variationen sind angegeben. Ihre physikalische Auswahl ist noch nicht begründet.'],['Ausgerechnete Außenfeldantwort','Ein Schur-Komplement löst eine Hilfsuhr bei festem C und w. Es liefert noch keine Vakuumgeometrie.'],['Analytische Ablehnung','Der Kern ist auch nach einer einzigen konstanten Normierung nicht isometrisch bezüglich I₂.'],['Offene physikalische Konstruktion','Physikalischer Zustandsraum, Constraint-/Evolutionsdeutung, klassischer Grenzfall und Verfeinerung sind erforderlich.']], [160,339])
h('Was die Ablehnung nicht entscheidet')
p('Sie betrifft ausschließlich CST-DUST-V1-RAW-K in zwei ausdrücklich deklarierten endlichen kinematischen Randräumen. Eine Interpretation als Zwangskern, andere physikalische Skalarprodukte und kontrollierte Grenzwerte bleiben offen. Es handelt sich nicht um einen No-go-Satz für CST.')
p('Regularität bleibt eine eigene Entscheidung. Ein globaler Bounce wird weder bestätigt noch durch diesen begrenzten Test widerlegt.')
p('6. November 2026 · Main-Basis nach PR 244: 9fa170dfd604. Lokaler Plan vor der Rechnung; analytischer Ausfallmechanismus bereits bekannt. Keine blinde Vorhersage, keine neuen 4D-Ensembles, keine bezahlten Läufe.','S')

page(2,'Der vollständige Kandidat')
p('C ist eine endliche strikte Ordnung mit festem N und markierten Anfangs-/Endantichains. Jedes freie Element liegt zwischen Anfang und Ende. Innen- und Außenbereich gehören zu derselben Geschichte; alle durch die interne Grenze laufenden Intervalle bleiben enthalten.')
eq('S<sub>tot</sub>(C,T,w) = ℏκF<sub>4</sub>(C) + S<sub>d</sub>(C,T,w)<br/>F<sub>4</sub> = N − N<sub>0</sub> + 9N<sub>1</sub> − 16N<sub>2</sub> + 8N<sub>3</sub><br/>κ = (4/√6) ℓ²/ℓ<sub>P</sub>²,   ℓ<sub>P</sub>² = 8πGℏ')
p('N<sub>k</sub> zählt Paare mit k strikt dazwischenliegenden Elementen. Λ = 0 und S<sub>outer</sub> = 0 sind explizite Kandidatenannahmen. Der äußere Rechenrand ist damit noch nicht physikalisch qualifiziert [1–3].')
eq('K<sub>N</sub>(b<sub>out</sub>,b<sub>in</sub>) = (1/|G<sub>fix</sub>|) Σ<sub>C</sub> ∫ dμ(T,w) exp(iS<sub>tot</sub>/ℏ)<br/>dμ = ∏<sub>freie T</sub> dT/(2T<sub>max</sub>) · ∏<sub>freie w</sub> dν(w)<br/>dν(w) = ½ δ<sub>0</sub>(dw) + [1/(2w<sub>max</sub>)] 1<sub>(0,wmax)</sub> dw')
p('Die Uhren liegen in [−T<sub>max</sub>,T<sub>max</sub>]. G<sub>fix</sub> erhält alle vorgegebenen Labels und Marken. Freie Dichtegewichte können auch auf Randstellen liegen, wenn dort nur Uhrwerte fixiert sind. Die Integration ist kompakt; bei festem N ist der Kern endlich.')
table([['Angabe','Status'],['Zählmaß und Gruppengewicht','Explizite, invariant formulierte Modellwahl'],['Halber Atomanteil bei w = 0','Erlaubt exakte Vakuum-Trägermuster; nicht physikalisch abgeleitet'],['T auf allen Elementen','Hilfsfeld auch bei w = 0; nichtlokale Kopplung kann dort fortbestehen'],['Festes N, kleine Ordnungen','Keine variable-N-Dynamik, keine 4D-Selektion'],['Endlicher Kern','Noch kein physikalisches Skalarprodukt und kein Evolutionsgesetz']], [186,313])
p('Die Aufspaltung in Atom- und Positivmuster definiert getrennte Trägerstrata. Ein binärer Materieindikator wird nicht infinitesimal variiert. Annahmen und abgeleitete Identitäten sind in DERIVATION.md getrennt ausgewiesen.','S')

page(3,'Materiewirkung mit korrekter Produktidentität')
p('Für den 4D-BD-Operator gelten B<sub>xx</sub> = −A und B<sub>xy</sub> = A b(k) für y ≺ x, mit A = 4/(√6 ℓ²) und b(k) = (1, −9, 16, −8, 0, …). Definiert wird:')
eq('Γ<sub>x</sub>[T] = ½ [B(T²)<sub>x</sub> − 2T<sub>x</sub>(BT)<sub>x</sub> + T<sub>x</sub>²(B1)<sub>x</sub>]<br/>             = ½ Σ<sub>y≺x</sub> B<sub>xy</sub>(T<sub>x</sub> − T<sub>y</sub>)²<br/>S<sub>d</sub> = −½ Σ<sub>x</sub> w<sub>x</sub>(Γ<sub>x</sub> + 1)')
h('Warum der letzte Term erforderlich ist')
p('Wenn B im passenden glatten Bereich zu □ − R/2 wird [1], hebt T²B1 den Nullordnungsterm auf. Γ nähert sich dann formal g<super>ab</super>∂<sub>a</sub>T∂<sub>b</sub>T. Ohne Korrektur bliebe RT²/4. Endlich-diskret ist Γ exakt invariant unter T → T + c.')
eq('S<sub>d</sub><super>cont</super> = −½ ∫ d⁴x √(−g) ρ [g<super>ab</super>∂<sub>a</sub>T∂<sub>b</sub>T + 1]<br/>w = ℓ⁴ρ;   [T] = Länge,   [w] = Wirkung')
p('<b>w ist ein integriertes Dichtegewicht, keine Ruhemasse.</b> Eine Ruhemasse benötigt einen räumlichen Bezug und den kalibrierten physikalischen Strom. Die Tests verwenden dimensionslos A = ℏ = 1.')
h('Kontinuumsziel, noch keine CST-Korrespondenz')
eq('g<super>ab</super>∂<sub>a</sub>T∂<sub>b</sub>T = −1<br/>∇<sub>a</sub>(ρ∇<super>a</super>T) = 0<br/>T<sub>ab</sub> = ρu<sub>a</sub>u<sub>b</sub>,   u<sub>a</sub> = −∂<sub>a</sub>T')
p('Diese Gleichungen folgen aus der angegebenen Kontinuumswirkung für wirbelfreien Staub. Sie gelten vor Mehrstrombildung beziehungsweise Kaustiken. Die Normierung und Gradientenform liefern dort geodätische Bewegung. Der Zusammenhang mit Staubreferenzfeldern ist bekannt [4]; die hier gewählte CST-Amplitude bleibt ein eigener Kandidat.')
p('Für eine Herleitung aus CST fehlen kontrollierte erste Variationen einschließlich Rand und Materieabbildung. Konvergenz im Mittel der Wirkung genügt nicht. Das Modell enthält außerdem kein Gesetz, das diese glatte Näherung über einen Bounce hinweg rechtfertigt.','S')

page(4,'Die Variation liefert einen Strom')
eq('∂S<sub>d</sub>/∂w<sub>x</sub> = −½(Γ<sub>x</sub> + 1)<br/>j<sub>y→x</sub> = ½ w<sub>x</sub>B<sub>xy</sub>(T<sub>x</sub> − T<sub>y</sub>)<br/>q<sub>z</sub> = ∂S<sub>d</sub>/∂T<sub>z</sub> = Σ<sub>z→x</sub> j − Σ<sub>y→z</sub> j')
p('Die Dichtegleichung gilt für Variationen innerhalb eines offenen positiven Stratum. Am Atom w = 0 gibt es diese Tangentialvariation nicht. Freie Uhrvariation verlangt q = 0. An minimalen Elementen ist Γ = 0; dort existiert kein positiver innerer Normierungssattel. Anfangskragen beziehungsweise Vorgeschichte müssen gesondert behandelt werden.')
h('Schnittbilanz als genaue Konsequenz')
eq('Σ<sub>z∈A</sub> q<sub>z</sub> = Σ<sub>A→Ā</sub> j − Σ<sub>Ā→A</sub> j')
p('Alle internen Paarbeiträge heben sich auf. Die 130 116 Schnittprüfungen bestätigen die Identität exakt. Damit stammt der Strom nun aus der definierten Wirkung. Wegen alternierender Operatorgewichte kann er jedoch Vorzeichen wechseln; seine physikalische Kalibrierung bleibt offen.')
h('Retardierter Operator und Wirkungsvariation unterscheiden sich')
eq('L = ½ D<super>T</super> diag(w<sub>x</sub>B<sub>xy</sub>) D<br/>S<sub>d</sub> = −½ T<super>T</super>LT − ½ Σw<sub>x</sub>,   q = −LT')
p('D trägt pro kausalem Paar −1 am Vorgänger und +1 am Nachfolger. L ist symmetrisch und im Allgemeinen indefinit. Die Variation enthält Beiträge aus beiden Zeitrichtungen, obwohl B retardiert ist. Einen retardierten Operator direkt als Euler-Ableitung einzusetzen wäre ein anderer Ansatz.')
p('Das beweist für sich keine physikalische Akausalität. Eine kausale Anfangswertentwicklung benötigt zusätzlich einen geeigneten Zustand und eine qualifizierte Quantendynamik. Hier liegt zunächst eine endliche Randwertwirkung vor.')
table([['Kontrolle','Ergebnis'],['Produktidentität, Uhr- und Dichteableitung','Je 22 095 exakte Stellenprüfungen'],['Konstante T-Verschiebung','22 095 exakte Invarianzprüfungen'],['Zweistellen-Beispiel mit w₀ = 0','T₀ kann dennoch an die zukünftige Materiezeile koppeln']], [238,261])

page(5,'Geometrie, Grenze und Quantenvariation')
p('Ein Geometriemove muss die strikte Ordnung und alle extern fixierten Daten erhalten. Bei festen Feldern lautet seine vollständige Wirkungsänderung:')
eq('ΔS = ℏκ ΔF<sub>4</sub> − ¼ Σ<sub>yx</sub> w<sub>x</sub>(B′<sub>xy</sub> − B<sub>xy</sub>)(T<sub>x</sub> − T<sub>y</sub>)²')
p('Es müssen alle geänderten Intervalle berücksichtigt werden, auch bei Paaren abseits der umgeschalteten Relation. 1 240 zulässige Relationstoggles in der breiteren algebraischen Testklasse bestätigen diese gemeinsame Differenz exakt.')
h('Interne Kopplung ist Teil der vollen Wirkung')
eq('S<sub>d</sub>(C) = S<sub>d</sub>(A) + S<sub>d</sub>(B) + X<sub>d</sub> + R<sub>d</sub>')
p('X<sub>d</sub> enthält grenzüberschreitende Paare. R<sub>d</sub> korrigiert bei internen Paaren die durch außerhalb liegende Zwischenpunkte veränderten Intervallgewichte. Der Beweis ist eine disjunkte Zerlegung aller Paare; die 130 116 Kontrollen haben exakt null Rest. Zusammen mit der vorherigen BDG-Verklebung ist die gewählte endliche Gesamtwirkung geschlossen.')
p('Ein zusätzlicher interner Oberflächenterm darf diese Beiträge nicht unbegründet doppelt zählen. Der äußere Rechenrand bleibt eine eigene offene Aufgabe. Endliche Umbenennungsidentitäten wählen keine Dynamik und verlangen nicht ΔS = 0 für jeden Mikromove.')
h('Regulatorränder verschwinden nicht von selbst')
eq('∫<sub>−L</sub><super>L</super> dT ∂<sub>T</sub>(f e<super>iS/ℏ</super>) = [f e<super>iS/ℏ</super>]<sub>−L</sub><super>L</super>')
p('Für S = 0 und f = T beträgt die linke Seite nach Normierung mit 2L genau 1. Der Randterm ist ebenfalls 1. Eine randfreie Schwinger-Dyson-Gleichung wäre hier falsch. Ebenso liefert das positive kompakte Dichteintegral einen endlichen Fourierfaktor und keine exakte Delta-Zwangsbedingung.')
p('Bei Änderungen von Maß, Integrationsgebiet oder externem Zustand gehören deren Beiträge zur Amplitudenvariation. Eine Gleichung für die klassische Wirkung allein ist keine vollständige Quantenvariation.','S')
h('Exakte Amplitudenvariation unter festen Bedingungen')
eq('W = −iℏ log K,   ∂<sub>q</sub>W = ⟨∂<sub>q</sub>S<sub>tot</sub>⟩<sub>K</sub>')
p('Für K ≠ 0 und eine externe Uhr q bei festem Maß, Träger und Integrationsgebiet folgt dies durch Differentiation der vollständigen endlichen Summe. Die Klammer ist ein komplexes Amplitudenverhältnis. Die zweite Ableitung enthält zusätzlich eine verbundene Zweipunktinsertion; DERIVATION.md gibt sie explizit an. Diese Antwort ist noch keine kausale In-in-Gleichung.','S')

page(6,'Eine Außenfeldantwort ist ausgerechnet')
p('Bei festem C und w können Hilfsuhren E stationär eliminiert werden. X bezeichnet gehaltene Uhren und b die fixierten äußeren Daten. Für invertierbares L<sub>EE</sub> folgt:')
eq('T<sub>E</sub> = −L<sub>EE</sub><super>−1</super>(L<sub>EX</sub>T<sub>X</sub> + L<sub>Eb</sub>T<sub>b</sub>)<br/>L<sub>eff</sub> = L<sub>XX</sub> − L<sub>XE</sub>L<sub>EE</sub><super>−1</super>L<sub>EX</sub>')
h('Fünferkette mit zwei Materiegewichten')
p('Es gilt 0 ≺ 1 ≺ 2 ≺ 3 ≺ 4, w = (0,0,1,1,0), T₀ = 0 und T₄ = 4. Die Variablen T₂,T₃ werden gehalten; die Hilfsuhr T₁ wird eliminiert. Der Operatorvorfaktor beträgt 1.')
eq('L<sub>EE</sub> = −4,   T₁ = (−T₂ + 9T₃)/8<br/>L<sub>eff</sub> = (1/16) [ [−55, −17], [−17, 145] ]<br/>q₃ = (17T₂ − 145T₃)/16')
table([['Berechnet','Noch nicht daraus ableitbar'],['Neun rationale Feldpaare','Keine physikalische Außenraumfamilie'],['q₁ = 0 exakt','Keine Erfüllung aller Dichtenormierungen'],['Reduzierte Wirkung stimmt exakt','Keine Vakuummetrik oder Staubtrajektorie'],['Gemeinsame Grenzantwort q₃','Kein kausales effektives Junction-Gesetz']], [220,279])
p('Das eliminierte w = 0-Element trägt weiterhin eine Hilfsuhr. Es ist kein rekonstruierter Außenraum. Die negative Eigenzahl des eliminierten Blocks beschreibt einen stationären Sattel, kein Minimum.')
h('Warum dies noch keine Quantenelimination ist')
p('Eine Quantenintegration über beschränkte Felder lässt sich nicht durch Einsetzen des stationären Wertes ersetzen. Determinanten, Phasen und Boxrandkorrekturen sowie die Summe über Geometrien müssen mitgeführt werden. Bei singulärem L<sub>EE</sub> sind außerdem Nullraum- und Verträglichkeitsbedingungen zu lösen.')
p('Die konkrete Rechnung macht die verbleibende Aufgabe sichtbar: Ein gemeinsamer Response ist algebraisch erreichbar; seine Deutung als physikalische Rand- und Außenraumdynamik setzt eine qualifizierte Gesamtamplitude voraus.','S')

page(7,'Der rohe Kern besteht den Normtest nicht')
p('Geprüft wird eine zusätzliche Modellannahme: Der rohe Kern sei bereits ein Evolutionsoperator zwischen zwei zweidimensionalen kinematischen Räumen mit Skalarprodukt I₂. Die orthonormal deklarierten Randlabels sind anfangs T = (0,1), am Ende T = (2,3). Es handelt sich nicht um vollständige kontinuierliche Uhrbasen.')
p('Für die einzelne Kausalrelation 0 ≺ 1 ist w₀ = 0 fixiert; w₁ wird mit ½δ₀ + ½dw auf (0,1) integriert. Es gilt A = ℏ = 1. Die Gravitationswirkung trägt nur eine gemeinsame Phase, die in K†K wegfällt.')
eq('a = ½ + (β − α)²/4<br/>G(a) = ½ + ½ ∫₀¹ dw e<super>−iaw</super><br/>       = ½ + ½ e<super>−ia/2</super> sinc(a/2)<br/>K = [ [G(3/2), G(3/4)], [G(11/4), G(3/2)] ]')
h('Analytischer Nachweis ohne numerische Toleranz')
p('Alle drei Argumente liegen zwischen 0 und π. Daher ist Re G(a) &gt; ½ und Im G(a) &lt; 0. Der Realteil jedes Produkts G(a)<super>*</super>G(b), mit komplexer Konjugation am ersten Faktor, ist größer als ¼. Für die Summe der zwei Produkte folgt:')
eq('<b>Re (K†K)₀₁ &gt; ½.</b><br/>Somit K†K ≠ c I₂ für jedes konstante c &gt; 0.')
p('Keine einzelne zustands- und quellenunabhängige Normierung kann diesen Kern isometrisch machen. Die numerische Rechnung bestätigt Re (K†K)₀₁ ≈ 1.432358276431. Sie wird für die analytische Ablehnung nicht benötigt.')
h('Begrenzung des Ergebnisses')
p('Eine Gravitationsamplitude muss nicht unmittelbar unitäre Zeitentwicklung sein. Sie könnte nach weiterer Konstruktion als Constraint-Kern oder Rigging-Map wirken. Eine physikalische Hilbertraumreduktion oder ein anderes begründetes Skalarprodukt ist hier nicht ausgeschlossen. Das FAIL gilt allein der angegebenen rohen Evolutionsinterpretation.')
p('Der Mechanismus war vor der Rechnung bekannt und im Plan offengelegt. Dieses Ergebnis ist keine unabhängige Vorhersage eines physikalischen Kollaps- oder Bounceverhaltens.','S')

page(8,'Auch die feste In-in-Normierung scheitert')
p('Für ρ₀ = |+⟩⟨+| mit |+⟩ = (1,1)/√2 und die Eingangsquelle D(J) = diag(1,e<super>iJ</super>) wird nur einmal bei J = 0 normiert:')
eq('n(J) = Tr[K D(J) ρ₀ D(J)† K†]<br/>Z[J₊,J₋] = Tr[K D(J₊) ρ₀ D(J₋)† K†] / n(0)')
p('Eine normierte geschlossene Evolution müsste bei gleichen Quellen Z[J,J] = 1 erfüllen. Der Kandidat ergibt stattdessen:')
table([['Größe','Wert'],['n(0)','2.916131516588 (gerundet)'],['n(π)','0.0514149637264 (gerundet)'],['Z[π,π]','0.01763122254053348… statt 1']], [190,309])
story.append(Image(str(FIG/'fixed_normalization.png'),width=499,height=221))
p('Das Diagramm verwendet gerundete Anzeigewerte. Die Entscheidung beruht auf dem analytischen Beweis und rationalen Intervallen. Die Spur ist ein kinematischer Normtest, keine Staubtrajektorie oder Bouncewahrscheinlichkeit.','S')
h('Was keine Reparatur derselben Dynamik ist')
p('Für jede Quelle separat zu normieren verändert das erzeugende Funktional. Auch ein positiver Gram-Dekohärenzausdruck garantiert allein keine normierte kausale Evolution. Der CTP-Rahmen kann kausale Rückwirkung organisieren [5], benötigt hier aber zuerst eine geeignete physikalische Realisierung.')

page(9,'Prüfumfang und getrennte Entscheidungen')
table([['Exakte Prüfung','Umfang'],['Gelabelte Ordnungen N = 1…5','4 473'],['Produktidentität / Uhrableitung / Dichteableitung','Je 22 095 Stellen'],['Konstante Uhrverschiebung','22 095 Stellen'],['Materieverklebung / Stromschnittsaldo','Je 130 116 Fälle'],['Labelpermutationen bis N = 4','5 377 Fälle'],['Zulässige Relationstoggles bis N = 4','1 240 Instanzen'],['Bedingte Außenfeldantwort / strukturelle Kontrollen','9 Feldpaare / 10 Kontrollen']], [351,148])
p('Alle algebraischen Residuen sind exakt null. Die Enumeration ist breiter als der Amplitudenträger; 24 Ordnungen gehören zur implementierten Anfang-/Endelement-Spezialklasse. Keine dieser Zählungen qualifiziert eine physikalische 4D-Staubdynamik.')
h('Zertifizierte komplexe Amplitude')
eq('Taylorgrad p = 80;   r(a) = |a|<super>p+1</super> / [2(p+1)!(p+2)]<br/>Gram-Fehler ≤ 2(2r + r²),   r = max r(a)<br/>'+N['fixed_normalization_Z_pi_pi_interval'][0]+'<br/>≤ Z[π,π] ≤<br/>'+N['fixed_normalization_Z_pi_pi_interval'][1])
p('Vergleiche und Quotientengrenzen werden rational gerechnet; Intervallenden nach außen gerundet. Der zusätzliche Rundungsfehler nominaler komplexer Dezimaleinträge ist separat ausgewiesen. Es gibt keine angepasste Fehlertoleranz.')
table([['P1-Entscheidung','Status / Geltungsbereich'],['MODEL','FAIL nur für CST-DUST-V1-RAW-K mit den deklarierten I₂-Randräumen'],['CURRENT, CORRESPONDENCE, BOUNDARY','HOLD: physikalische Qualifikation offen'],['BOUNCE, REGULARITY, TRAPPING, EXTENSION','HOLD: keine neue physikalische Freigabe']], [252,247])
p('Der geerbte Contract bleibt unverändert. Der Audit prüft den deklarierten Evidenzdatensatz; er ersetzt keinen mathematischen oder physikalischen Beweis. Frühere P5-Datensätze werden nicht überschrieben.','S')

page(10,'Was jetzt tatsächlich fehlt')
p('Der nächste wissenschaftliche Engpass ist die physikalische Bedeutung der Gesamtamplitude: Zustandsraum, Skalarprodukt, Constraints, Anfangszustand und zulässige Quellen. Ein neuer Kandidat muss aus diesen Anforderungen begründet werden. Ein nachträgliches Normieren auf einen gewünschten Bounce wäre keine Herleitung.')
eq('Ziel nach dieser Qualifikation:<br/>δΓ<sub>eff</sub>[q₊,q₋] / δq<sub>Δ</sub> = 0 bei q<sub>Δ</sub> = 0<br/>q<sub>Δ</sub> = q₊ − q₋')
p('Diese gemeinsame In-in-Variation ist hier ein Ziel, keine abgeleitete Gleichung. Ihre Konstruktion muss Innen- und Außenraum, alle Kreuzintervalle, Maß, Zustände und äußere Randdaten enthalten. Einfach −iℏ log K zu variieren genügt nicht. Der Vakuumaußenraum und der materielle Anschluss müssen aus derselben Lösung hervorgehen.')
p('Danach folgen erste Variationen im klassischen Bereich und physikalisch abgeglichene Verfeinerung. Regularität behält einen eigenen Prüfpunkt: Dichte/Krümmung, inverse Momente, Verteilungsschwänze und Zeitbereich. Das Minimum eines mittleren Volumens entscheidet keine dieser Fragen.')
h('Reproduzierbarkeit')
p('Das Prüfpaket enthält DERIVATION.md, den vorab fixierten Plan, Python-Quellen, zehn Ergebnisdateien, geerbte Eingaben mit Herkunftshashes, den isolierten Replay-Nachweis und ein Integritätsmanifest. Die Berechnung läuft mit der Python-Standardbibliothek über <b>python3 -O -B analyze.py</b>. Referenz: Python 3.12.14.','S')
h('Primärquellen und genaue Rolle')
for text in [
'[1] Benincasa, Dowker (2010), <i>The Scalar Curvature of a Causal Set</i>. <link href="https://arxiv.org/abs/1001.2725" color="#167c70">arXiv:1001.2725</link>. BD-Operator; keine Ableitung dieser Materieamplitude.',
'[2] Dowker, Liu, Lloyd-Jones, <i>Timelike boundary and corner terms in the causal set action</i>. <link href="https://arxiv.org/html/2501.00139v2" color="#167c70">arXiv:2501.00139v2</link>. BDG-Biaktion und untersuchte zeitartige Randbeiträge.',
'[3] Buck, Dowker, Jubb, Surya (2015), <i>Boundary Terms for Causal Sets</i>. <link href="https://arxiv.org/abs/1502.05388" color="#167c70">arXiv:1502.05388</link>. Raumartige Randkonstruktionen.',
'[4] Brown, Kuchař (1995), <i>Dust as a standard of space and time in canonical quantum gravity</i>. <link href="https://arxiv.org/abs/gr-qc/9409001" color="#167c70">arXiv:gr-qc/9409001</link>. Kontinuumsreferenz; hier nur wirbelfreier Kandidat.',
'[5] Calzetta, Hu (1987), <i>Closed-time-path functional formalism in curved spacetime</i>. <link href="https://doi.org/10.1103/PhysRevD.35.495" color="#167c70">Phys. Rev. D 35, 495</link>. Rahmen kausaler Rückwirkung; der endliche Normbeweis steht im Prüfpaket.'
]:p(text,'S')
p('Die Primärliteratur qualifiziert weder das gewählte Maß noch die kinematischen Randräume dieses Kandidaten. Eine vollständige physikalische Variationsdefinition bleibt daher als Forschungsaufgabe offen.','S')

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cdd8dd'));canvas.line(48,37,A4[0]-48,37)
    canvas.setFont('DV',7.4);canvas.setFillColor(colors.HexColor(gray))
    canvas.drawString(48,25,'CST-DUST · Variationskandidat v0.1 · 06.11.2026')
    canvas.drawRightString(A4[0]-48,25,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(TARGET),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=50,
                      title='CST-DUST: Variationskandidat und Quantennormierung v0.1',author='Thomas Gfeller · CST-DUST',
                      subject='Scoped finite variation and raw-kernel normalization counterexample')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(TARGET)
