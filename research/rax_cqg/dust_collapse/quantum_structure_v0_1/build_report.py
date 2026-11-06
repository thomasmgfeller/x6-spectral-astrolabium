"""Render scoped CST state-space and constraint qualification."""
from pathlib import Path
import csv,json,sys
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
TARGET=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'output/pdf/CST_DUST_Zustandsraum_Constraints_v0_1.pdf'
TARGET.parent.mkdir(parents=True,exist_ok=True);FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
R=json.loads((ROOT/'results/verification.json').read_text());M=json.loads((ROOT/'results/common_metric_certificate.json').read_text())
if R['relabel_projector']!='PASS_EXACT_AUXILIARY_CONSTRUCTION' or M['decision']!='FAIL_EVERY_COMMON_POSITIVE_METRIC':raise RuntimeError('Unexpected scoped result')
navy='#173e50';teal='#167c70';amber='#ad5636';gray='#5a6d76'
rows=list(csv.DictReader((ROOT/'results/relabel_orbits.csv').open()))
sizes=[int(x['orbit_size']) for x in rows if x['m']=='2'];total=sum(sizes)
P=[[0.0]*total for _ in range(total)];offset=0;cuts=[]
for size in sizes:
    for i in range(offset,offset+size):
        for j in range(offset,offset+size):P[i][j]=1/size
    offset+=size;cuts.append(offset-.5)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,ax=plt.subplots(figsize=(5.9,3.2),layout='constrained')
im=ax.imshow(P,cmap='GnBu',vmin=0,vmax=1,interpolation='nearest')
for cut in cuts[:-1]:ax.axhline(cut,color=gray,lw=.7);ax.axvline(cut,color=gray,lw=.7)
ax.set_xlabel('Markierter Basiszustand');ax.set_ylabel('Markierter Basiszustand')
ax.set_xticks([0,3,7,11],[1,4,8,12]);ax.set_yticks([0,3,7,11],[1,4,8,12])
cb=fig.colorbar(im,ax=ax,ticks=[0,.5,1],shrink=.88);cb.set_label('Projektormatrixelement')
ax.set_title('m = 2: 12 markierte Zustände, 7 Orbitblöcke',fontsize=10,color=navy)
fig.savefig(FIG/'relabel_projector.png',dpi=190,facecolor='white');plt.close(fig)
fonts=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
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
    p(f'CST-DUST · ZUSTANDSRAUM UND CONSTRAINTS v0.1 / {n:02d}','L');p(title,'T')
def table(rows,widths):
    t=Table([[Paragraph(str(v),st['C']) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eef1')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,green),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#cdd8dd'))]))
    story.append(t);story.append(Spacer(1,8))

page(1,'Positive Struktur, dynamische Grenze')
p('Ein positiver Hilbertraum für gemeinsame endliche Geometrie-Materie-Historien ist definiert und von internen Elementlabels befreit. Die Umbenennungsconstraints und ihr Quotientprodukt sind exakt geprüft. Diese Konstruktion liefert noch keine gravitativen Constraints oder physikalische CST-Evolution.')
eq('<b>Positive Labelreduktion: PASS als Hilfskonstruktion.</b><br/><b>Gemeinsames positives Skalarprodukt für den alten<br/>rohen Evolutionskern: ausgeschlossen im geprüften Modell.</b><br/><b>Vollständige physikalische Quantendefinition: HOLD.</b>')
table([['Neue Aussage','Reichweite'],['Expliziter Hilfshistorienraum','Gemeinsame Kausalstruktur, Felder und Materie-/Vakuummarken; positives Hilfsmaß'],['234 exakte Orbitblöcke','Umbenennungen von 3 671 markierten Zuständen konsistent reduziert'],['Stärkerer Normierungsbefund','Kein gemeinsames positives M bei der festgelegten Identifikation der zwei Randräume'],['Naive direkte Staubbedingung','Im gewöhnlichen L²-Raum verbleibt auf nichtleeren Staubstrata nur der Nullzustand'],['Distributionelle Positivkontrolle','Constraint und relationale Evolution passen in einer lösbaren Referenz konsistent zusammen']], [192,307])
p('Die Einschränkungen sind wesentlich: Andere begründete Randprodukte, distributionswertige Rigging-Maps, vollständige Randräume und kovariante Historienmodelle werden nicht pauschal ausgeschlossen. Die Referenzkonstruktion ist kein aus CST abgeleiteter Hamiltonian.')
p('Junction-Gesetz, gemeinsame Außenraumgeometrie, Regularität und globaler Bounce bleiben eigenständig offen.')
p('6. November 2026 · Basis: Main nach PR 245, Commit 3595df81b865. Lokaler Plan vor der Rechnung; strukturelle Hindernisse vor der Zertifizierung erwartet. Keine neuen physikalischen 4D-Ensembles oder bezahlten Läufe.','S')

page(2,'Zustände und Skalarprodukt ausdrücklich festlegen')
p('Die Hilfsfamilie enthält vollständige endliche Patches C mit N = m + 2 Elementen. Anfang und Ende sind markiert; jedes innere Element liegt kausal zwischen ihnen. Geometrie, Materie und Außenbereich gehören zu derselben Geschichte.')
eq('H<sub>aux,m</sub> = L²(X<sub>m</sub>, dμ<sub>m</sub>)<br/>dμ<sub>m</sub> = (1/m!) Σ<sub>C gelabelt</sub> ∏<sub>x</sub> dT<sub>x</sub>/8 · ∏<sub>innere x</sub> dν(w<sub>x</sub>)<br/>T<sub>x</sub> ∈ [−4,4],   dν(w) = ½δ₀(dw) + ½1<sub>(0,1)</sub> dw')
p('Alle Uhren sind hier vor einer Randkonditionierung frei. Die beiden äußeren Dichtegewichte sind in dieser Hilfsfamilie null. Dies ist eine neue explizite kinematische Randwahl. Der frühere Kern wird später getrennt mit seinen unveränderten eigenen Randgewichten geprüft.')
h('Dichter Testbereich und Materiestrata')
p('Φ besteht stratumweise aus glatten Funktionen mit kompaktem Träger im Innern der Uhrbox und der positiven Dichteintervalle. Der Atomanteil w = 0 und die positiven Strata sind getrennte Summanden. Interne Permutationen wirken gleichzeitig auf Ordnung, Felder und Materiemarken.')
p('Das positive Hilfsmaß ist eine Modellannahme. Die komplexe Wirkungsphase exp(iS/ℏ) wird nicht als positive Norm verwendet. Eine Normierung des gesamten Geometriezählmaßes auf eins ist für den Hilbertraum nicht erforderlich.')
table([['Definiert','Noch nicht nachgewiesen'],['Vollständiger endlicher Hilfspatch','Geschlossener physikalischer Cauchy-/Randzustand'],['Gemeinsame Geometrie und Materiefelder','Vierdimensionale Kontinuumsnähe'],['Positives Maß bei festem m','Physikalisches Maß und Gewichte verschiedener N'],['Dichter Testbereich','Physikalische Rigging-Map oder dynamischer Hamiltonian']], [224,275])
p('Nichtlokale Intervalle können Vorgeschichte benötigen. Ein endlicher Randkragen darf deshalb nicht ohne Nachweis als vollständiger Zustand behandelt werden. Auch Punktuhrwerte sind keine normierten Zustände des kontinuierlichen L²-Raums; dafür werden geeignete Testzustände oder Wellenpakete benötigt.','S')

page(3,'Die Labelconstraints sind geschlossen')
eq('U<sub>g</sub>ψ(z) = ψ(g<super>−1</super>z),   g ∈ S<sub>m</sub><br/>C<sub>s</sub> = I − U<sub>s</sub> für erzeugende Vertauschungen<br/>P = (1/m!) Σ<sub>g</sub> U<sub>g</sub><br/>P† = P,   P² = P,   Ran P = ∩<sub>s</sub> ker C<sub>s</sub>')
p('Die gemeinsame Permutation identischer Maßfaktoren ist unitär. Jede erzeugende Vertauschung ist eine selbstadjungierte Involution. Die Gruppenmittelung ist deshalb ein orthogonaler Projektor; sie entfernt nur unphysikalische interne Labels.')
eq('B<sub>rel</sub>(ψ,χ) = ⟨ψ,Pχ⟩<sub>aux</sub> = ⟨Pψ,Pχ⟩<sub>aux</sub><br/>H<sub>rel</sub> ≅ H<sub>aux</sub>/ker P ≅ Ran P')
story.append(Image(str(FIG/'relabel_projector.png'),width=453,height=246))
p('Die Abbildung zeigt den exakt bekannten Projektor für zwei innere Elemente. Die Achsen sind Basisindizes, keine Raumzeitkoordinaten. Jeder Orbitblock trägt 1/|O|. Verschiedene Materiemarken bleiben getrennt; Vakuum und Materie werden nicht miteinander identifiziert.','S')
p('Im diskreten, innerhalb jedes Feldstratum konstanten Teilraum hat ein markierter Zustand Gewicht 1/(m!2<super>m</super>). Sein Orbit trägt 1/[2<super>m</super>|Aut(C,σ)|]. Der Stratumfaktor 2<super>−m</super> gehört zum Maß und bleibt erhalten.')
p('Diese Constraints erzeugen keine Staubeigenzeit. Eine kontinuierliche gravitative Constraint-Algebra wurde damit nicht hergeleitet.','S')

page(4,'Die direkte Staubbedingung leert den L²-Sektor')
p('Die frühere Materiewirkung liefert auf einem positiven Dichtestratum die stationäre Bedingung Γ<sub>x</sub> + 1 = 0. Geprüft wird die zusätzliche Vorschrift, sie unmittelbar als Multiplikationsconstraint auf gewöhnliche Hilfswellenfunktionen anzuwenden:')
eq('C<sub>x</sub>(T) = Γ<sub>x</sub>(T) + 1<br/>Γ<sub>x</sub> = ½ Σ<sub>y≺x</sub> B<sub>xy</sub>(T<sub>x</sub> − T<sub>y</sub>)²<br/>C<sub>x</sub> ψ = 0')
h('Allgemeiner Beweis für die gewählte Darstellung')
p('C<sub>x</sub> ist ein reelles Polynom in den freien Uhren. Bei konstantem T gilt C<sub>x</sub> = 1; es ist also nicht identisch null. Seine Nullmenge besitzt Lebesgue-Maß null. Eine gewöhnliche L²-Funktion, deren Träger vollständig in einer solchen Menge liegt, ist das Nullelement.')
eq('<b>Auf jedem nichtleeren positiven Staubstratum:</b><br/>∩<sub>x besetzt</sub> ker C<sub>x</sub> = {0} im gewöhnlichen L²-Raum.')
p('7 249 besetzte Stellen der endlichen Kontrollklasse bestätigen den konstanten Polynomwert 1 exakt. Der Satz selbst folgt aus dem Nullmengenargument und gilt über diese Kontrollen hinaus.')
h('Die Aussage schließt verallgemeinerte Zustände nicht aus')
p('Die Uhren sind in diesem Satz vor einer festen Randkonditionierung frei und absolut stetig verteilt. Bei singulären oder speziell konditionierten Maßen muss neu geprüft werden. Auf dem leeren Staubstratum werden keine dieser Staubbedingungen auferlegt.')
p('Distributionelle Lösungen in Φ* können trotz trivialem L²-Kern existieren. Eine Rigging-Map kann daraus eine positive physikalische Norm konstruieren, wenn ihre Voraussetzungen erfüllt sind [1,2]. Die stationäre Eulergleichung ist aber nicht automatisch ein kanonischer Dirac-Constraint.')
p('Die korrekte Folgerung lautet: Diese direkte L²-Vorschrift ist für einen nichttrivialen Staubsektor ungeeignet. Es folgt kein No-go für Staub, CST oder wohldefinierte Constraint-Quantisierung.','S')

page(5,'Auch ein gemeinsames anderes M genügt nicht')
p('Für den unveränderten Zweistellen-Kern werden die Anfangslabels (0,1) und Endlabels (2,3) durch Translation identifiziert. Innerhalb dieser ausdrücklich zusätzlichen Interpretation wird jedes positive Hermitesche gemeinsame Skalarprodukt M zugelassen:')
eq('K = [ [G(3/2), G(3/4)], [G(11/4), G(3/2)] ]<br/>G(a) = ½ + ½ ∫₀¹ e<super>−iaw</super> dw<br/>Gesucht: K†MK = cM,   M &gt; 0,   c &gt; 0')
p('Wenn ein solches M existiert, ist M<super>1/2</super>KM<super>−1/2</super>/√c unitär. Die beiden Eigenwerte von K haben dann gleichen Betrag. Daher muss gelten:')
eq('R = (tr K)²/det K = 2 + 2 cos(θ₁ − θ₂) ∈ [0,4]')
p('R ist unter einer gemeinsamen Basisänderung sowie jeder von null verschiedenen skalaren Normierung invariant. Die positive untere Schranke für |det K|² liegt bei etwa 0,019907. Die zertifizierte Rechnung liefert:')
eq('Im R ∈ ['+M['trace_determinant_ratio']['imag_interval'][0]+',<br/>             '+M['trace_determinant_ratio']['imag_interval'][1]+']<br/><b>R ist nicht reell. Ein gemeinsames positives M existiert nicht.</b>')
p('Der Realteil liegt zusätzlich bei etwa 22,2335. Die frühere Ablehnung für I₂ ist somit auf alle gemeinsamen positiven Produkte unter dieser Identifikation erweitert. Die Labelgruppe des Zweistellenfalls ist trivial; die Labelreduktion kann diesen Befund nicht verändern.')
h('Die genaue Grenze des Satzes')
p('Für unterschiedliche Randräume ohne die festgelegte Identifikation wird keine Spurbehauptung gemacht. Andere unabhängig begründete Ein-/Ausgangsprodukte, vollständige Randräume, Constraint-Amplituden und kontrollierte Grenzwerte sind nicht ausgeschlossen.')
p('Bei invertierbarem K kann man M<sub>in</sub> = K†M<sub>out</sub>K immer definieren. Das erzeugt formal eine Isometrie zwischen zwei Produkten; ihre physikalische Begründung ist damit jedoch nicht geliefert. Eine Polarzerlegung ersetzt dagegen den Amplitudenoperator.','S')

page(6,'Eine positive Constraint-/Evolutionsreferenz')
p('Eine vollständig lösbare mathematische Referenz zeigt, wie Constraint- und Evolutionsdeutung zusammenpassen. Ihr Hamiltonian wird ausdrücklich nicht als CST-Gesetz ausgegeben.')
eq('H<sub>aux</sub> = L²(ℝ,dτ) ⊗ ℂ²,   Φ = Schwartz-Testbereich<br/>C = −i∂<sub>τ</sub> + H,   H = diag(1,−1),   ℏ = 1')
p('Die Gruppenmittelung ist distributionswertig. In Fourierdarstellung erhält man durch Auswertung bei p = −E<sub>a</sub>:')
eq('B(f,g) = Σ<sub>a</sub> f̃<sub>a</sub>(−E<sub>a</sub>)* g̃<sub>a</sub>(−E<sub>a</sub>)<br/>H<sub>phys</sub> ≅ ℂ²<br/>Ψ(τ) = e<super>−iHτ</super>ψ,   i∂<sub>τ</sub>Ψ = HΨ')
p('Die positive Form annihiliert den Constraint. Ihr Nullraum wird quotientiert; die resultierende Norm ist positiv. Die Lösungen müssen nicht in L² über der ganzen Zeitachse liegen. Der physikalische Raum entsteht erst durch die distributionelle Konstruktion.')
table([['Kontrolle','Ergebnis'],['U†U = I bei vier Zeiten kπ/2','Exakt bestanden'],['U(τ₂+τ₁) = U(τ₂)U(τ₁)','16 exakte Kontrollen'],['Vier Fourier-Testfunktionen','Constraint-Annihilation und positive Norm exakt'],['Nichttriviales gemeinsames M','K = S diag(1,i) S⁻¹ besteht mit M = [[1,−1],[−1,2]]'],['Kontrollkern diag(1,2)','Scheitert am notwendigen Wert R = 9/2']], [245,254])
h('Positivität wählt die Dynamik nicht aus')
p('Auf demselben ℂ² sind sowohl H₀ = 0 als auch H₁ = diag(1,−1) selbstadjungiert. Für den Zustand (1,1)/√2 liefert die Observable σ<sub>x</sub> bei τ = π/2 die unterschiedlichen Werte +1 und −1. Es wird nicht behauptet, dass beide die CST-Amplitude reproduzieren.')
p('Die Staubzeitreduktion besitzt eine Kontinuumsreferenz [3]. Ein entsprechender CST-Hamiltonian, die Eignung der Uhr und ihre Beziehung zum gemeinsamen Außenraum bleiben herzuleiten.','S')

page(7,'Physikalische Observablen und Historienalternative')
h('Welche Observablen bereits definiert sind')
p('Beschränkte reelle Funktionen, die unter gemeinsamer Umbenennung invariant sind, wirken als selbstadjungierte Multiplikatoren auf H<sub>rel</sub>. Dazu gehören Relationen- und Materieträgeranzahlen. Ihre Eigenschaft als gravitative Dirac-Observablen folgt erst nach Qualifikation der dynamischen Constraints.')
p('Ein Skalarprodukt muss auch zur verlangten Observablenalgebra passen. Wenn die beiden nichtentarteten diagonalen Uhrmatrizen im Zweistellentest selbstadjungiert bleiben sollen, müssen die zugehörigen Produkte diagonal sein. Für positive diagonale Randprodukte bleibt der Realteil des Nebendiagonaleintrags von K†M<sub>out</sub>K strikt positiv; ein diagonales M<sub>in</sub> ist damit unmöglich. Dieses Korollar gilt nur unter der genannten Uhr-Observablenannahme.')
h('Eine kovariante Historienformulierung ist eine weitere Möglichkeit')
p('Ein stark positives Dekohärenzfunktional D kann auf Ereignissen eine semidefinite Form und nach Nullraumquotient einen Historien-Hilbertraum erzeugen [4]. Die physikalische Dynamik steckt dabei bereits in D. Eine kanonische Hamilton-Konstruktion ist deshalb nicht die einzig denkbare Quantendefinition.')
table([['Erforderlich für diesen anderen Zweig','Stand hier'],['D aus gemeinsamer Geometrie-Materie-Amplitude und Zustand','Nicht konstruiert'],['Normierung, starke Positivität, Additivität und Kovarianz','Nicht für die volle CST-Dynamik qualifiziert'],['Verklebung und physikalisch abgeglichene Verfeinerung','Offen'],['Benötigte Ereignisse und Fortsetzbarkeit','Eigene Prüfung; nicht automatisch gegeben [5,6]']], [306,193])
p('Eine positive kleine Gram-Matrix oder die Normierung für nur einen Zustand reicht dafür nicht. Dieser alternative Zweig wird hier nicht ausgeschlossen und nicht als erledigt dargestellt. Ein Wechsel dorthin benötigt eine explizite neue Definition.')
p('Im staubfreien Außenraum ist das zuvor eingeführte T zunächst ein Hilfsfeld. Seine Verwendung als globale physikalische Uhr, Kaustiken und der gemeinsame kausale Anfangswertbereich bleiben offene Modellpflichten.','S')

page(8,'Exakte Prüfungen, getrennte Entscheidungen')
table([['Markierte Kontrollklasse','Umfang'],['Innere Elemente m = 0…4','3 671 Ordnung-/Trägermuster'],['Gruppenwirkungen','85 035'],['Orbit- und Projektorblöcke','234'],['Gemeinsame Wirkungsumbenennungen','4 817'],['Nichtverschwindende Normierungspolynome','7 249'],['Relationale Norm-/Kompositionskontrollen','4 / 16'],['Distributionelle Constraint-Proben','4']], [326,173])
p('Die Projektormatrix wird durch direkte Gruppensummen und unabhängig über Orbitgrößen geprüft. Idempotenz, Adjungiertheit, Positivität und Nullvektoren stimmen exakt. Die Kontrollen betreffen kleine Hilfshistorien und keine physikalischen 4D-Ensembles.')
h('Zertifikat ohne angepasste Toleranz')
eq('G-Taylorgrad p = 80<br/>r(a) = |a|<super>p+1</super> / [2(p+1)!(p+2)]<br/>Rationale Rechteckintervalle für alle komplexen Operationen')
p('Die Restschranke schließt jeden komplexen Eintrag ein. Determinante, Spurquadrat und Division werden mit rationalen Intervallen gerechnet. Alle Entscheidungen erfolgen exakt vor der nach außen gerundeten 32-stelligen Anzeige. Der erforderliche Nenner ist strikt von null getrennt.')
table([['Neuer P1-Datensatz','Entscheidung'],['CST-DUST-QS1-RELABEL','Alle acht physikalischen Gates HOLD; Labelquotient mathematisch qualifiziert'],['CST-DUST-V1-RAW-K-COMMON-M','MODEL=FAIL nur für diese gemeinsame-M-Interpretation; sieben weitere Gates HOLD']], [238,261])
p('Der geerbte Model-Contract bleibt unverändert. Frühere Ergebnisse werden nicht überschrieben oder nachträglich hochgestuft. Ein bestandener mathematischer Referenztest ist keine Freigabe für eine physikalische Staubdynamik.')
p('Der lokale Plan war vor der Rechnung fixiert; die strukturellen Hindernisse waren vor der numerischen Zertifizierung erwartet. Keine blinde Vorhersage, keine externe Präregistrierung, keine neuen Sprinklings, Zufallsdaten oder bezahlten Läufe.','S')

page(9,'Der verbleibende physikalische Engpass')
p('Ausgearbeitet sind der Hilfshistorienraum, sein Testbereich, die Umbenennungsdarstellung, die zugehörigen Constraints, ein positives Quotientprodukt und labelinvariante Observablen. Eine vollständig physikalische Quantendefinition ist dadurch noch nicht gewonnen.')
eq('Noch zu begründen:<br/>dynamische Constraints und η<sub>phys</sub>,<br/>oder ein aus CST abgeleiteter relationaler Hamiltonian,<br/>oder eine qualifizierte kovariante Historien-Quantendynamik.')
p('Diese Wahl muss die gemeinsame Geometrie-Materie-Amplitude, Zustände, Observablen und Innen-/Außenraumkopplung konsistent verbinden. Sie darf nicht allein zur Reparatur einer Normprüfung oder für einen gewünschten Bounce getroffen werden. Kausales Junction-Gesetz, Korrespondenz, Verfeinerung und globale Entwicklung bleiben anschließende Qualifikationen.')
p('Regularität bleibt eigenständig: Dichte und Krümmung, inverse Momente, Verteilungsschwänze und Verhalten bei physikalisch abgeglichener Verfeinerung. Es wird weder ein globaler Bounce noch Singularitätsauflösung behauptet.')
h('Prüfpaket und Wiederholung')
p('DERIVATION.md enthält die vollständigen Beweise und Grenzen. Der Plan, Python-Quellen, 13 Ergebnisdateien, unveränderte Vorgängereingaben, isolierter Replay und SHA-256-Manifest sind enthalten. <b>python3 -O -B analyze.py</b> benötigt nur die Standardbibliothek. Referenz: Python 3.12.14.','S')
h('Primärquellen und ihre Rolle')
for t in [
'[1] Giulini, Marolf (1999), <i>On the Generality of Refined Algebraic Quantization</i>. <link href="https://arxiv.org/abs/gr-qc/9812024" color="#167c70">gr-qc/9812024</link>. Bedingungen für Rigging-Map und physikalisches Produkt.',
'[2] Marolf (2000), <i>Group Averaging and Refined Algebraic Quantization</i>. <link href="https://arxiv.org/abs/gr-qc/0011112" color="#167c70">gr-qc/0011112</link>. Voraussetzungen der Gruppenmittelung.',
'[3] Brown, Kuchař (1995), <i>Dust as a standard of space and time in canonical quantum gravity</i>. <link href="https://arxiv.org/abs/gr-qc/9409001" color="#167c70">gr-qc/9409001</link>. Kontinuumsreferenz der Staubzeitreduktion.',
'[4] Dowker, Johnston, Sorkin (2010), <i>Hilbert Spaces from Path Integrals</i>. <link href="https://arxiv.org/abs/1002.0589" color="#167c70">1002.0589</link>. Hilbertraum aus Dekohärenzfunktional.',
'[5] Dowker, Johnston, Surya (2010), <i>On extending the Quantum Measure</i>. <link href="https://arxiv.org/abs/1007.2725" color="#167c70">1007.2725</link>. Fortsetzbarkeit als eigene Frage.',
'[6] Surya, Zalel (2020), <i>A Criterion for Covariance in Complex Sequential Growth Models</i>. <link href="https://arxiv.org/abs/2003.11311" color="#167c70">2003.11311</link>. Spezifische CST-Wachstumsmodelle; nicht dieser BDG-Staubkandidat.'
]:p(t,'S')

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cdd8dd'));canvas.line(48,37,A4[0]-48,37)
    canvas.setFont('DV',7.4);canvas.setFillColor(colors.HexColor(gray))
    canvas.drawString(48,25,'CST-DUST · Zustandsraum und Constraints v0.1 · 06.11.2026')
    canvas.drawRightString(A4[0]-48,25,str(doc.page));canvas.restoreState()
SimpleDocTemplate(str(TARGET),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=50,
    title='CST-DUST: Zustandsraum, Skalarprodukt und Constraints v0.1',author='Thomas Gfeller · CST-DUST',
    subject='Positive auxiliary quotient and scoped obstructions to a physical quantum interpretation').build(story,onFirstPage=footer,onLaterPages=footer)
print(TARGET)
