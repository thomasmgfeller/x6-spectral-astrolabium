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
OUT=ROOT/'CST_DUST_Observablenalgebra_Superselektion_Phasenreferenz_v0_1.pdf'
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

p('CST-DUST<br/>Observablenalgebra und<br/>endliche Phasenreferenz','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Aus der bisherigen Staub-Record-Wirkung folgt keine physikalische Superselektionsregel. Wird zusätzlich eine Erhaltung der Gesamtladung angenommen, lässt sich die Genauigkeit einer kohärenten Messung mit einer endlichen Referenz exakt begrenzen.')
f('Optimaler universeller Effektfehler bei L+1 Referenzstufen:\nτ_min(L) = [1 - cos(π/(L+2))] / 2')
table(['Frage','Befund'],[
('Müssen die beiden Dichtestrata getrennt bleiben?','Die vorhandenen Definitionen wählen die vollständige physikalische Algebra noch nicht aus.'),
('Verbietet globale Erhaltung jeden Übergang?','Nein. Ein Referenzsystem kann die entgegengesetzte Ladungsänderung tragen.'),
('Wie gut ist eine endliche Referenz?','Die angegebene Grenze ist im ausdrücklich erklärten Zusatzmodell scharf und positiv.'),
('Ist damit der CST-Detektor hergeleitet?','Nein. Physikalische Ladung, Referenzpräparation, Modenfilter und Kopplung fehlen weiterhin.')],[190,315])
h('Wissenschaftlicher Nutzen')
p('Der nächste Modellentscheid lässt sich jetzt präzise formulieren. Eine Rechenerhöhung allein kann die fehlende Algebra nicht auswählen. Die bedingte Referenzgrenze macht außerdem sichtbar, welche zusätzliche Ressource eine kohärente Auslese überhaupt voraussetzen würde.')
h('Status und Kosten')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Keine hergeleitete Singularitätsauflösung oder Rückwirkung. Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung.')
p('L zählt Referenz-Ladungsstufen, keine Kausalset-Elemente und keine Geldkosten. Die Methode knüpft an etablierte Quantenreferenz- und Superselektionsliteratur an; es wird keine Neuheit der Methode beansprucht.','small')
p('Basis: Main nach PR 263, c77cb607db23a043cd4965ee4efeb206eda22f8e. Vollständiger Beweis und gepinnte Projektquellen im Prüfpaket.','small')

page('1 · Die Wirkung bestimmt die Algebra nicht')
p('Der bisherige kinematische Raum zerfällt in H_a⊕H_c: Dichte-Nullatom und kontinuierlich positiver Dichteanteil, jeweils mit allen Uhrmoden. Record-Observablen und die vorhandene Wirkungsphase sind Multiplikationsoperatoren; sie erhalten diese Zerlegung.')
f('Zwei kompatible Erweiterungen derselben Record-Daten:\nA_block = B(H_a) ⊕ B(H_c)\nA_full  = B(H_a ⊕ H_c)')
p('In der Blockalgebra ist die Atomprojektion Π_a zentral. In der vollen Algebra ist sie es nicht. Beide enthalten die bisher erklärten Record-Operatoren. Die zentrale Rolle von Π_a folgt daher nur, wenn die Blockalgebra zusätzlich als vollständig physikalisch festgelegt wird.')
h('Was die bisherigen Daten nicht unterscheiden')
f('D(ρ) = Π_a ρ Π_a + Π_c ρ Π_c\nTr(Eρ) = Tr(E D(ρ)) für alle blockdiagonalen E')
p('Eine kohärente Dichtematrix und ihre blockweise dephasierte Version liefern dieselben blockdiagonalen Daten. Auch die vorhandene Phasenmultiplikation hebt diese Ununterscheidbarkeit nicht auf. Innerhalb der einzelnen Strata sind Phasen jedoch weiterhin zugänglich.')
h('Der Sektorindex ist keine abgeleitete Staubmasse')
p('In der gepinnten Materiewirkung ist w=v₄ρ ein integriertes Dichtegewicht mit der Dimension Wirkung. Es ist keine Ruhemasse. Eine physikalische Staubmasse benötigt eine geeignete räumliche Fläche und einen kalibrierten Strom. Ihre mögliche Erhaltung beweist keine Erhaltung des binären Projektors Π_c.')
h('Folgerung für das Messziel')
p('Für normierte a∈H_a und c∈H_c wird das feste Ziel P_+=|(a+c)/√2&gt;&lt;(a+c)/√2| betrachtet. Blockdiagonale Effekte haben dazu weiterhin mindestens 1/2 Operatornormfehler. Diese Aussage setzt die beiden kohärenten Testzustände im Vergleichsraum voraus; spätere physikalische Constraints können einen anderen Zielvertrag verlangen.')

page('2 · Ein scharfer Satz für eine feste Referenz')
p('Für diese Rechnung wird ausdrücklich ein Zusatzmodell eingeführt: Q_S=Π_c, eine nichtentartete Referenzladung Q_R mit Stufen 0 bis L, ein unabhängig vom unbekannten Eingang fest vorbereiteter Zustand σ und ein gemeinsamer Effekt F, der die Gesamtladung N erhält.')
f('N = Q_S ⊗ I + I ⊗ Q_R\n0 ≤ F ≤ I,   [F,N] = 0\nTr(Eρ) = Tr(F(ρ ⊗ σ)),   τ = ||E-P_+||')
p('Die Zustände |a,n+1&gt; und |c,n&gt; haben dieselbe Gesamtladung. Übergänge zwischen ihnen sind erlaubt, obwohl sich die Systemladung ändert. Beide Messergebnisse F und I−F bleiben in der Statistik; es wird nicht auf akzeptierte Versuche nachnormiert.')
h('Nur benachbarte Referenzkohärenz trägt bei')
f('C(σ) = Σ_(n=0,...,L-1) |σ_(n,n+1)|\nE_ac = Σ_n σ_(n,n+1) F_(a,n+1;c,n)\n|F_(a,n+1;c,n)| ≤ 1/2\nτ ≥ (1-C(σ))/2')
p('Die Matrixelementgrenze folgt aus ||F−I/2||≤1/2. Zum Zielkreuzelement 1/2 bleibt daher mindestens die angegebene Abweichung. Diese untere Grenze wird erreicht: Jeder gepaarte Ladungsblock erhält einen passend phasierten Rang-eins-Effekt; ungepaarte Endpunkte erhalten 1/2.')
f('Erreichter reduzierter Effekt im Zielzweierraum:\nE = 1/2 · [[1, C(σ)], [C(σ), 1]]\nAuf dem gesamten orthogonalen Komplement: E = 0')
p('Der vollständige Operatornormfehler ist dann genau (1−C)/2. Eine ladungsdiagonale Referenz hat C=0 und bleibt bei 1/2. Die obere Konstruktion setzt alle benötigten Modenfilter voraus; sie ist noch kein physikalischer Detektor.')

page('3 · Endliche Referenz: exaktes Größenbudget')
p('Aus Positivität folgt |σ_(n,n+1)|≤√(p_n p_(n+1)), mit p_n=σ_nn. Die Optimierung ist damit ein Eigenwertproblem einer endlichen Matrix mit Nebendiagonalen 1/2. Ihr größter Eigenwert ist cos(π/(L+2)).')
f('Optimale Referenzamplituden:\nr_n = √(2/(L+2)) sin((n+1)π/(L+2))\nτ_min(L) = [1-cos(π/(L+2))]/2 > 0')
p('Die Sinusfolge löst die Eigenwertgleichung mit verschwindenden äußeren Randwerten. Der zugehörige reine Referenzzustand erreicht die Kohärenzobergrenze und der Effekt von Seite 3 erreicht die Fehleruntergrenze.')
table(['Ziel: τ höchstens','Kleinster Index L','Referenzstufen L+1'],[
('0,1','3','4'),('0,01','14','15'),('0,001','48','49'),('0,0001','156','157')],[170,155,180])
p('Jeder Minimalwert ist mit rationalen Intervallen zertifiziert: Die obere Fehlerschranke genügt der Toleranz; beim unmittelbar kleineren L überschreitet schon die untere Schranke die Toleranz. Die kleinen Dezimalzahlen werden nicht nur gerundet verglichen.')
h('Die Verteilung ist entscheidend')
p('Gleichmäßige Amplituden ergeben nur τ=1/[2(L+1)]. Die optimale Sinusreferenz erreicht asymptotisch π²/[4(L+2)²]. Kein endlicher Träger erreicht in diesem Modell die ideale Zielmessung exakt.')
h('Geltungsbereich des Budgets')
p('Die Grenze gilt für einmalige Nutzung einer festen, unabhängig vorbereiteten Referenz, den erklärten nichtentarteten Ladungsträger und beliebige erlaubte invariante Effekte. Referenzverbrauch, Wiederverwendung, reale Präparierbarkeit und ein physikalisches Zeit- oder Energiebudget sind nicht bestimmt.')
p('Die Stufenzahl ist weder eine Aussage über die Größe der CST-Historien noch über den Preis eines Experiments. Ohne die zusätzlich angenommene Erhaltung ist der Satz kein allgemeines CST-Verbot.','small')

page('4 · Relative Phase und vollständiger Messraum')
h('Globale Invarianz lässt relationale Information zu')
p('Die Mittelung über Gesamtladungen entfernt Kohärenzen zwischen verschiedenen Gesamtladungsblöcken. Für den invarianten Effekt F ändert sie die gemeinsamen Messwahrscheinlichkeiten nicht.')
f('G(X) = Σ_q Π_q X Π_q\nTr(F G(ρ ⊗ σ)) = Tr(F(ρ ⊗ σ))')
p('Mit zwei Referenzstufen, σ=|+&gt;&lt;+| und den Systemeingängen ψ_± sind beide lokalen Systemmarginalen nach der Mittelung diagonal. Trotzdem liefert die gemeinsame Messung 3/4 für ψ_+ und 1/4 für ψ_−. Die relative Phase steckt in den gemeinsamen Korrelationen.')
p('Dies definiert eine mögliche relationale Kodierung. Ihre physikalische Präparation ist noch nicht hergeleitet. Eine stärkere lokale Superselektion, die auch den Austausch mit Referenzen verbietet, wird dadurch nicht aufgehoben. Ebenso wenig wird eine unbegrenzt wiederverwendbare Referenz erzeugt.')
h('Leckagemoden und Endpunkte sind Teil der Rechnung')
p('Der beste konstruierte Effekt weist sämtliche weiteren Uhr- und Dichtemoden zurück. Diese Modenselektion ist eine zusätzliche Voraussetzung. Ein Effekt, der auf einem unkontrollierten Leckagemodus stattdessen eins ist, hat dieselbe Zweimodenkompression, aber vollständigen Fehler eins.')
table(['Kontrolle','Exaktes Gegenbeispiel'],[
('Nur Zielzweierraum geprüft','Fehler dort 1/4; mit akzeptierter Leckagemode im vollständigen Raum Fehler 1.'),
('Ungepaarte Endpunkte weggelassen','Bei L=1 und gleichmäßiger Referenz sinkt die unbedingte Erfolgswahrscheinlichkeit für ψ_+ von 3/4 auf 1/2.')],[200,305])
h('Ein Effekt ist noch kein ausgewähltes CST-Instrument')
p('Mit √F und √(I−F) lässt sich eine abstrakte unitäre Zweiausgangsrealisierung an einem neutralen Zeiger konstruieren; sie erhält die Gesamtladung. Damit sind weder eine physikalische Wechselwirkung noch eine eindeutige Zustandsänderung festgelegt. Der vollständige Beweis dieser algebraischen Erweiterung steht im Prüfpaket.')

page('5 · Prüfevidenz und nächste Entscheidung')
result=json.loads((ROOT/'results/verification.json').read_text())
table(['Kontrolle','Umfang'],[
('Blockalgebra / ladungserhaltender Austausch','24 Identitäten / eine exakt unitäre Austauschmatrix'),
('Referenz- und Effektfälle',str(result['reference_effect_cases'])),
('Born-Regel und globale Ladungsmittelung',str(result['born_and_twirl_controls'])+' exakte Identitäten'),
('Zertifizierte Budgets / Minimalitätsgrenzen','10 / 4'),
('Negativkontrollen / Nachrechnung','8 zurückgewiesen / 4 Ergebnisdateien bytegleich')],[285,220])
p('Die allgemeinen Sätze beruhen auf den ausgeschriebenen Beweisen. Die rationalen Kontrollmatrizen sind keine Kontinuumsdiskretisierung. Keine externe Replikation und keine Beweisassistentenprüfung.','small')
f('python3 -B verify_package.py\npython3 -B replay.py')
p('Python-Standardbibliothek genügt. Das Prüfpaket enthält die Herleitung, den maschinenlesbaren Vertrag, den eingefrorenen Plan, fünf gepinnte Projektdateien und sämtliche Ergebnisse.','small')
h('Was jetzt physikalisch festzulegen ist')
p('<b>Algebra, zulässige Zustände und Referenzen müssen gemeinsam aus der Materie-/Randtheorie begründet werden.</b> Bei einer echten lokalen Superselektion ist der Zielvertrag zu ändern. Bei globaler Erhaltung und erlaubter Referenz sind Ladung, Präparation und vollständiges Messinstrument herzuleiten. Ohne diese Erhaltungsrestriktion ist die passende Kopplung direkt zu begründen.')
p('Die vorliegenden Record-Daten entscheiden nicht zwischen diesen Fällen. Mehr n=5-Feldintegrale allein lösen diese Definitionsfrage nicht. Alle acht physikalischen Gates bleiben HOLD.','small')
h('Primärquellen und methodische Einordnung')
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/263" color="#087E8B">Projektbasis PR 263</link>; <link href="https://arxiv.org/abs/quant-ph/0610030" color="#087E8B">Bartlett, Rudolph, Spekkens (2007)</link>: Quantenreferenzen, Superselektion und relationale Kodierungen; <link href="https://arxiv.org/abs/quant-ph/0009117" color="#087E8B">Berry, Wiseman (2000)</link>: optimierte Phasenschätzung; <link href="https://arxiv.org/abs/quant-ph/0112154" color="#087E8B">Ozawa (2002)</link>: Messgrenzen durch Erhaltungsgesetze. Deren Phasenvarianz beziehungsweise Rauschoperator werden nicht mit dem hier verwendeten Operatornormfehler gleichgesetzt. Der konkrete Satz ist im Paket eigenständig für die angegebenen Annahmen bewiesen.','small')

def footer(c,doc):
    c.setStrokeColor(TEAL);c.setLineWidth(.5);c.line(45,42,550,42)
    c.setFillColor(NAVY);c.setFont('DV',7)
    c.drawString(45,30,'CST-DUST · Observablenalgebra / Superselektion / Phasenreferenz · v0.1')
    c.drawRightString(550,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=50,topMargin=48,bottomMargin=60,
    title='CST-DUST: Observablenalgebra, Superselektion und endliche Phasenreferenz v0.1',author='Thomas Gfeller · CST-DUST research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)

