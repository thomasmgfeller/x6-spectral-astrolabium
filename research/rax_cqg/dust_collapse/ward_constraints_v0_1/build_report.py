"""Render the six-page reading report; scientific replay uses only stdlib."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Uhrsymmetrie_Constraints_Atomgrenze_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
NAVY=colors.HexColor('#12354A');TEAL=colors.HexColor('#087E8B');PALE=colors.HexColor('#EDF5F7')
styles={
'title':ParagraphStyle('title',fontName='DVB',fontSize=23,leading=28,textColor=NAVY,spaceAfter=16),
'sub':ParagraphStyle('sub',fontName='DV',fontSize=10,leading=15,textColor=TEAL,spaceAfter=10),
'h1':ParagraphStyle('h1',fontName='DVB',fontSize=15,leading=20,textColor=NAVY,spaceAfter=12),
'h2':ParagraphStyle('h2',fontName='DVB',fontSize=11,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=6),
'body':ParagraphStyle('body',fontName='DV',fontSize=9.2,leading=14,spaceAfter=8),
'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.5,spaceAfter=6),
'formula':ParagraphStyle('formula',fontName='Mono',fontSize=8,leading=12,backColor=PALE,borderPadding=7,spaceBefore=4,spaceAfter=12),
'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11.5),
'head':ParagraphStyle('head',fontName='DVB',fontSize=8.2,leading=11.5,textColor=colors.white)}
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'h2')
def f(text):p(escape(text).replace('\n','<br/>'),'formula')
def page(title):story.append(PageBreak());p(title,'h1')
def table(headers,rows,widths):
    data=[[Paragraph(escape(str(x)),styles['head']) for x in headers]]
    data.extend([[Paragraph(escape(str(x)),styles['cell']) for x in row] for row in rows])
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,-1),(-1,-1),0.6,TEAL)]))
    story.append(t);story.append(Spacer(1,10))

p('CST-DUST<br/>Uhrsymmetrie, Constraints<br/>und Atomgrenze','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Die vorhandene Uhrsymmetrie begründet eine Variationsbilanz, aber keine binäre Dichtesektorladung. Im bisherigen Ein-Anker-Modell kann das erste freie Element die klassische innere Staub-Normierung nicht erfüllen. Eine ungeprüfte Übertragung dieser Bedingung auf Quantenzustände scheitert deshalb bereits am Randmodell.')
table(['Prüfung','Befund'],[
('Uhrverschiebung und Strom','Gemeinsame Verschiebung aller Uhren erhält die Wirkung. Die zugehörige Bilanz ist kein hergeleiteter positiver Massenstrom.'),
('Erster freier Dichtepunkt','C₁=1+8h²x₁²≥1. Ein positiver innerer Normierungssattel fehlt.'),
('Zusätzliche Operator-Constraints','Je nach Wahl entsteht ein leerer Raum oder nur der erste Dichte-Atomunterraum. Kleine gewichtete Residuen genügen nicht.'),
('Starke Materiephase bei festem n','Die Materieamplitude konvergiert zu 2⁻ⁿ, dem ursprünglichen Gewicht des Stratum mit ausschließlich verschwindenden Dichten.')],[182,323])
h('Was damit geklärt ist')
p('Die fehlende physikalische Algebra darf nicht durch eine frei gewählte Normierungsprojektion ersetzt werden. Vergangenheitskragen, Randzustand, Dichtevariation und Quantisierungsregel müssen zusammenpassen. Der Bericht zeigt dazu konkrete Gegenbeispiele und eine exakte Grenze des vorhandenen Maßmodells.')
h('Status und Kosten')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein allgemeines CST-Verbot, kein hergeleiteter physikalischer Zustandsraum und kein Bounce. Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung.')
p('Die analytische Dichteintegration war bereits im Vier-Element-Kern implementiert. Daraus wird keine neue Dimensions- oder Laufzeiteinsparung beansprucht.','small')
p('Basis: Main nach PR 264, 0ee861d67f7d28e2c2762ef01e70f428796f1f53. Vollständige Beweise, sechs gepinnte Quellen und Reproduktionscode im Prüfpaket.','small')

page('1 · Welche Erhaltung aus der Wirkung folgt')
p('Die geerbte Wirkung enthält nur Differenzen der Materieuhren. Werden alle Uhrwerte einschließlich äußerer Daten gemeinsam verschoben, bleibt sie unverändert. Die Dichtegewichte w werden dabei nicht bewegt.')
f('S_d = -Σ_x w_x C_x/2\nC_x = 1 + 1/2 Σ_(y≺x) B_xy (T_x-T_y)²\nS_d(T+c·1,w) = S_d(T,w)')
p('Der gerichtete Variationsstrom und die zugehörige Uhrableitung sind exakt bestimmt. Innere Beiträge heben sich für jede Teilmenge U auf.')
f('j_(y→x) = 1/2 · w_x B_xy (T_x-T_y)\nq_z = ∂S_d/∂T_z = Σ_(z→x) j - Σ_(y→z) j\nΣ_z q_z = 0\nΣ_(z∈U) q_z = Σ_(U→außen) j - Σ_(außen→U) j')
h('Diese Symmetrie ist nicht die binäre Sektorladung')
p('Eine Uhrtranslation wirkt auf T; die Sektorprojektion Π_c wirkt auf w. Auf einem zusätzlich erklärten unbeschränkten Uhrraum wäre der Translationsgenerator ein Ableitungsoperator −iℏΣ∂_T. Er ist nicht der Multiplikationsprojektor Π_c. Auf kompakten Fenstern wären zusätzlich selbstadjungierte Randbedingungen auszuwählen.')
p('Die alternierenden BD-Gewichte können vorzeichenbehaftete Ströme erzeugen. Eine positive Ruhemasse, ein kanonischer Phasenraum und eine physikalische Constraintalgebra sind damit noch nicht gegeben. Das Dichtegewicht w hat die Dimension Wirkung.')
h('Wirkungssymmetrie und Eichfreiheit unterscheiden')
p('Eine starre Symmetrie beweist nicht allein eine lokale Eichfreiheit. Äußere Uhrdaten, Präparation und Auslese gehören zum Modell. Die kanonische Staubkonstruktion von Brown und Kuchař besitzt eine eigene gekoppelte Constraintstruktur; diese ist hier noch nicht auf den CST-Historienraum übertragen.')

page('2 · Das erste freie Element und der Rand')
p('Im offenen positiven Dichtestratum fordert ein innerer stationärer Punkt ∂S_d/∂w₁=0. Im geankerten Historienmodell hat das erste freie Element nur den Anfangsanker als Vorgänger. Das betreffende BD-Intervallgewicht ist positiv.')
f('T₁-T₀ = 4h x₁\nC₁ = 1 + 1/2(T₁-T₀)² = 1+8h²x₁² ≥ 1\n∂S_d/∂w₁ = -C₁/2 ≠ 0')
p('Damit fehlt in dieser Randklasse ein vollständiger reeller innerer Sattel mit frei variiertem positivem w₁. Die Aussage gilt für jede natürliche Ordnung und jedes feste n≥1 im Ein-Anker-Modell. Ein zusätzlicher Anker allein behebt das zuvor bekannte Problem am minimalen Element nicht.')
h('Das Nullatom hat eine andere Variationsdomäne')
p('Am Atom w₁=0 gibt es keine infinitesimale Dichtevariation innerhalb des Atoms. Eine Gleichung, die im offenen positiven Stratum folgt, darf dort nicht ohne weitere Begründung als identische Operatorbedingung auferlegt werden. Randendpunkte und Trägerwechsel benötigen eigene Regeln.')
h('Ein längerer Vergangenheitskragen verändert die Frage')
p('Ein ergänzender rationaler Zeuge verwendet die Kette 0≺1≺2 mit zwei festgehaltenen Vorgängeruhren. Dann ist auch das negative Intervallgewicht −9 vorhanden.')
f('T₀=0,   T₁=7/18,   T₂=17/36\nΓ₂ = 1/2[(T₂-T₁)² - 9(T₂-T₀)²] = -1\nBei w₀=w₁=0, w₂=1/2 bleibt q₂=25/24 ≠ 0')
p('Die einzelne Normierung kann jetzt erfüllt werden; die Uhrgleichung jedoch nicht. Das ist kein vollständiger Sattel und keine geprüfte Randreparatur. Es zeigt, weshalb das Ergebnis kein allgemeines CST-Verbot ist.')
p('Dieser analytische Zeuge wurde nach dem eingefrorenen Kontrollgitter ergänzt und ist im Prüfpaket ausdrücklich gesondert markiert.','small')

page('3 · Warum kleine Constraint-Residuen täuschen')
p('Auf dem bisherigen kinematischen L²-Raum lassen sich drei Multiplikationsbedingungen vergleichen. Sie sind zusätzliche Quantisierungskandidaten; der regulierte Amplitudenkern leitet keine davon her.')
table(['Zusätzlicher Operator','Exakter Nullraum / Konsequenz'],[
('C₁ auf dem ganzen Raum','Nur Nullvektor; dehnt die positive Tangentialvariation unzulässig auf das Atom aus.'),
('Π_c C₁','Atomunterraum des ersten Dichtewerts; positiver erster Dichteanteil ausgeschlossen.'),
('w₁ C₁','Derselbe Atomunterraum, aber keine Spektrallücke zum positiven Stratum.')],[155,350])
h('Ein exaktes Gegenbeispiel zur Residuenqualifikation')
p('Für n=1,h=1/2 ist C₁(x)=1+2x². Wähle eine auf 0&lt;w&lt;ε konzentrierte Wellenfunktion, am Atom null. Das ursprüngliche Maß enthält jeweils die Hälfte Atom- und Gleichmaß.')
f('ψ_ε(x,w) = √(2/ε) · 1_(0,ε)(w)\n||ψ_ε||² = 1,   ||Π_a ψ_ε||² = 0\n||C₁ ψ_ε||² = 47/15\n||w C₁ ψ_ε||² = 47 ε²/45 → 0')
p('Das gewichtete Residuum wird beliebig klein, obwohl die Zustände vollständig im positiven Stratum bleiben und Abstand eins zum Atomkern haben. Bei halbierten ε beträgt das Überlappungsquadrat aufeinanderfolgender Zustände stets 1/2. Die Folge konvergiert nicht in Norm; ihre schwache Grenze ist null.')
h('Folge für das bisherige Messziel')
p('Der balancierte konstante Zielzustand besitzt im selben Beispiel das positive gewichtete Residuum 47/90. Wird eine der sektorweisen Bedingungen zusätzlich als physikalisch verlangt, muss der bisherige kohärente Zielvertrag geändert werden. Daraus folgt nicht, dass die CST diese Bedingungen tatsächlich vorschreibt.')
p('Eine Zustandsqualifikation braucht somit den richtigen Operator, seine Domäne und eine geeignete Stabilitäts- oder Spektralabschätzung. Ein kleiner Zahlenwert allein genügt nicht.','small')

page('4 · Ward-Ränder und der überlebende Atomterm')
p('Bei einer festgehaltenen absoluten Uhrbox bleibt der Integrationsrand in der Quantenidentität erhalten. Für eine freie Uhr gilt mit q_T=∂S/∂T:')
f('∫_(−L)^L [∂_T f + (i/ℏ)f q_T] exp(iS/ℏ) dT/(2L)\n= [f exp(iS/ℏ)]_(−L)^L / (2L)')
p('Ein Ein-Link-Test hat bei b=1/2,L=1 einen nachweislich nichtverschwindenden Randterm. Werden dagegen Anker, alle Uhren und das relative Fenster gemeinsam verschoben, bleibt die geankerte Amplitude exakt invariant. Die beiden Randfälle dürfen nicht verwechselt werden.')
h('Das Dichteintegral erzwingt keine Delta-Bedingung')
f('χ(u) = 1/2 + (1-exp(−iu))/(2iu),   χ(0)=1\nRe χ(u) ≥ (1−1/π)/2 > 1/3')
p('Die Hälfte Atomgewicht hält jeden einzelnen Faktor auf der reellen Achse von null fern. Das endliche Dichteintegral projiziert deshalb nicht exakt auf die klassische Normierung. Diese analytische Integration ist bereits im veröffentlichten Kern enthalten.')
h('Ein fester endlicher Materiesektor hat eine exakte Grenze')
f('A_p(μ) = n! ∫_(geordnetes Uhrsimplex) Π_j χ(μ a_j(x)) dx\nlim_(|μ|→∞) A_p(μ) = 2^(−n)')
p('Jedes a_j ist ein nicht identisch verschwindendes Polynom; seine Nullmenge hat Maß null. Fast überall geht jeder Faktor gegen 1/2. Wegen |χ|≤1 liefert dominierte Konvergenz die Formel. Der Rest entspricht dem ursprünglichen Gewicht aller verschwindenden Dichten.')
p('<b>Grenze der Aussage:</b> festes endliches n und feste Ordnung, Gravitationsphase ausgeklammert. Keine uniforme n-Konvergenzrate, keine vertauschte unendliche Summe und kein physikalischer semiklassischer Grenzwert. Einzelne Faktoren von null fernzuhalten schließt Interferenznullstellen in weiteren Integralen nicht aus.','small')

page('5 · Prüfevidenz und nächste physikalische Arbeit')
v=json.loads((ROOT/'results/verification.json').read_text())
table(['Kontrolle','Umfang'],[
('Wirkungsfälle / exakte Ableitungskomponenten','270 / 972'),
('Gemeinsame Uhrverschiebungen / Schnittbilanzen','810 / 3564'),
('Erste-Dichtepunkt-Fälle / approximative Nullzustände','90 / 4'),
('Ward-Koeffizienten / komplexe Funktionseinschlüsse','117 / 10'),
('Negativkontrollen / isolierte Nachrechnung','8 zurückgewiesen / 5 Dateien bytegleich')],[315,190])
p('Allgemeine Aussagen beruhen auf den Beweisen. Die Kontrollen verwenden höchstens drei neue Elemente. Die komplexen Funktionen sind durch rationale Taylor- und Rundungsradien eingeschlossen. Keine externe Replikation und keine Beweisassistentenprüfung.','small')
f('python3 -B verify_package.py\npython3 -B replay.py')
h('Die nächste Entscheidung betrifft das physikalische Modell')
p('<b>Vergangenheitskragen und Randzustand, erlaubte Dichtevariation sowie Quantisierungsregel sind gemeinsam zu begründen.</b> Erst daraus können eine physikalische Zustandsdomäne und die passende Observablenalgebra folgen. Die binäre Sektorladung oder ein frei gewählter Multiplikations-Constraint ersetzen diese Herleitung nicht.')
p('Der Ein-Anker-Kandidat bleibt ein mathematisch definiertes reguliertes Amplitudenmodell. Seine naive klassische beziehungsweise Dirac-artige Interpretation schließt die physikalischen Gates nicht. Ein größerer Integrationslauf allein behebt diese Definitionslücke nicht.')
p('Alle acht physikalischen Gates bleiben HOLD. Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung.','small')
h('Primärquellen')
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/264" color="#087E8B">Projektbasis PR 264</link> und sechs gepinnte Projektdateien; <link href="https://arxiv.org/abs/gr-qc/9409001" color="#087E8B">Brown und Kuchař, Phys. Rev. D 51, 5600 (1995)</link>: eigenständige kanonische Staub- und Constraintkonstruktion; <link href="https://arxiv.org/abs/1001.2725" color="#087E8B">Benincasa und Dowker, Phys. Rev. Lett. 104, 181301 (2010)</link>: kausale skalare Operatoren, korrigierte arXiv-Fassung. Keine dieser Quellen liefert bereits die hier noch fehlende physikalische Quantisierung des Staub-Historienraums.','small')

def footer(c,doc):
    c.setStrokeColor(TEAL);c.setLineWidth(.5);c.line(45,42,550,42)
    c.setFillColor(NAVY);c.setFont('DV',7)
    c.drawString(45,30,'CST-DUST · Uhrsymmetrie / Constraints / Atomgrenze · v0.1')
    c.drawRightString(550,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=50,topMargin=48,bottomMargin=60,
    title='CST-DUST: Uhrsymmetrie, Constraints und Atomgrenze v0.1',author='Thomas Gfeller · CST-DUST research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)

