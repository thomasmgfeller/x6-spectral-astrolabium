from pathlib import Path
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

HERE=Path(__file__).resolve().parent
OUT=HERE/'CST_DUST_Geometriedynamik_Stationaerer_Kandidat_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV',FONT+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB',FONT+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
ink=HexColor('#142b3b');teal=HexColor('#067f81');muted=HexColor('#4b6170');light=HexColor('#eef5f6')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=26,leading=31,textColor=ink,spaceAfter=14),
 'sub':ParagraphStyle('sub',fontName='DV',fontSize=11,leading=16,textColor=muted,spaceAfter=16),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=16,leading=21,textColor=teal,spaceAfter=13),
 'h2':ParagraphStyle('h2',fontName='DVB',fontSize=11,leading=15,textColor=ink,spaceBefore=11,spaceAfter=6),
 'p':ParagraphStyle('p',fontName='DV',fontSize=9.5,leading=14,textColor=ink,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.4,textColor=muted,spaceAfter=6),
 'math':ParagraphStyle('math',fontName='DV',fontSize=10.4,leading=16,textColor=ink,backColor=light,borderPadding=10,spaceBefore=6,spaceAfter=13),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.7,leading=12,textColor=ink),
 'th':ParagraphStyle('th',fontName='DVB',fontSize=8.7,leading=12,textColor=white),
}
story=[]
def p(t,k='p'): story.append(Paragraph(t,styles[k]))
def table(rows,widths):
 data=[[Paragraph(str(x),styles['th' if i==0 else 'cell']) for x in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[light,white]),('LINEBELOW',(0,0),(-1,0),.5,teal)]))
 story.extend([t,Spacer(1,10)])
def page(): story.append(PageBreak())

class Orders(Flowable):
 def __init__(self): super().__init__();self.width=490;self.height=125
 def draw(self):
  c=self.canv
  for x0,label,edges in [(5,'C₀: drei innere Ereignisse',[(0,1),(1,2)]),(267,'C₁: zwei entfernte Cover',[(0,2)])]:
   c.setFont('DVB',9);c.setFillColor(ink);c.drawString(x0,108,label)
   xy=[(x0+30,60),(x0+100,60),(x0+170,60)]
   c.setStrokeColor(teal);c.setLineWidth(1.8)
   for a,b in edges:
    xa,ya=xy[a];xb,yb=xy[b]
    if b-a==2:
     c.bezier(xa,ya+12,xa+30,ya+50,xb-30,yb+50,xb,yb+12)
    else:c.line(xa+12,ya,xb-12,yb)
   for i,(x,y) in enumerate(xy):
    c.setFillColor(white);c.circle(x,y,12,fill=1);c.setFillColor(ink);c.setFont('DVB',10);c.drawCentredString(x,y-3,str(i+4))
   c.setFont('DV',8);c.drawString(x0,20,'gleicher äußerer Vier-plus-vier-Kragen')

p('CST-DUST','sub')
p('Geometriedynamik:<br/>stationärer Kandidat','title')
p('Gemeinsame Quellen · zwei Ordnungen · kontrollierte Paarung<br/>Version 0.1 · 13. November 2026','sub')
p('<b>Neues Ergebnis:</b> Die unveränderte Wirkung besitzt zwei geometrisch verschiedene stationäre Randwertlösungen mit denselben äußeren Daten und positiven inneren Dichten. Ihre Wirkungsdifferenz hängt exakt von der Quelldichte ab. Die gemeinsame gaußsche Skalar-Randpaarung existiert.','p')
p('ΔS<sub>on</sub>(ρ) = 8 + 23ρ/19, &nbsp; 0 &lt; ρ &lt; 1/2.','math')
story.append(Orders())
table([['Baustein','Befund'],['Positive stationäre Quelle','Explizite Lösungen und regulärer Staubblock'],['Echte Ordnungsänderung','Drei versus eine innere Relation; gleicher Rand'],['Skalarfeld-Paarung','Endlich nach gemeinsamer Schwartz-Randpaarung'],['Physikalische Geometriedynamik','Noch nicht hergeleitet: Maß/Paarung und Verlaufsdeutung offen']],[163,327])
p('Sechs KI-Fachagenten, gegenseitige Prüfung und unabhängiger Wurzel-/Ordnungsabgleich. Exakte endliche Algebra und Intervallzertifikate; keine neue große Quadratur. Das Paket ist eine neue Untersuchung nach PR 290, keine nachträgliche Änderung seiner Ergebnisse.','small')

page();p('1  Ein gemeinsamer, expliziter Randvertrag','h')
p('Wir verwenden die bestehende dimensionslose Wirkung mit β=4/√6, κ=1 und b=(1,−9,16,−8). Für ein geordnetes Paar i≺j ist b der Koeffizient zur Zahl der strikt inneren Intervallelemente; ab vier inneren Elementen ist er null.','p')
p('F(C) = N − Σ<sub>i≺j</sub> b<sub>ij</sub><br/>C<sub>j</sub>(T) = 1 + (β/2) Σ<sub>i≺j</sub> b<sub>ij</sub>(T<sub>j</sub>−T<sub>i</sub>)²<br/>S = F(C) − ½Σ<sub>j</sub>r<sub>j</sub>C<sub>j</sub>(T) − (β/4)Σ<sub>i≺j</sub>b<sub>ij</sub>(q<sub>j</sub>−q<sub>i</sub>)²','math')
p('Elf Ereignisse tragen einen festen vergangenen Kragen {0,1,2,3}, einen festen zukünftigen Kragen {7,8,9,10} und das Innere I={4,5,6}. C₀ ist die vollständige Kette. C₁ entfernt ausschließlich (4,5) und (5,6); (4,6) bleibt erhalten. Beide Relationenmengen sind transitiv.','p')
table([['Vertragsbestandteil','Gemeinsam für beide Ordnungen'],['Äußerer Rand B','{0,1,2,3,7,8,9,10}; 28 B–B-Relationen identisch'],['Verbindung zum Inneren','Alle 24 B–I-Relationen identisch'],['Skalierte Uhr','u=T/Δ+5; Δ²=2/(19β); am Rand uⱼ=j'],['Randquelle','rⱼ=ρ mit 0&lt;ρ&lt;1/2; stationärer Skalarwert qⱼ=0'],['Uhrträger des Nachfolgers','Gemeinsam [−3/2,3/2]; bei Normierung dt/3'],['Skalar-Testpaarung','exp(−Σ<sub>B</sub>qⱼ²/2), inneres Lebesgue-Maß und gemeinsamer Abel-Regulator']],[164,326])
p('<b>Offengelegter Modellwechsel:</b> Die neue Historienfamilie, positive Kragenquelle und größere Uhrbox ersetzen den bisherigen Sechshistorien-Versuchsvertrag. Die Wirkung bleibt gleich. Max |T<sub>B</sub>|=5Δ≈1,26945 passt nicht in seine alte Box [−1,1]. Ein Dirichlet-Punkt ist außerdem kein normierter Delta-Randzustand im früheren Hilfsraum.','p')
p('q<sub>B</sub>=0 bezeichnet den klassischen stationären Referenzpunkt. Die spätere Skalar-Paarung integriert q<sub>B</sub> mit einem gemeinsamen Gaußgewicht. Diese beiden Operationen werden nicht miteinander verwechselt.','small')

page();p('2  Zwei positive Lösungen aus der vollen Wirkung','h')
p('Alle inneren Dichten, Uhren und Skalarwerte werden variiert; die acht äußeren Kragenereignisse bleiben fest. Die Ableitungen der <b>vollen</b> Wirkung verschwinden an den folgenden Punkten. Nur den isolierten Innenblock zu variieren würde die nötigen Beiträge des Zukunftskragens verlieren.','p')
table([['Größe','Kette C₀','Alternative C₁'],['u<sub>I</sub>','(4,5,6)','(4,4,5)'],['r<sub>I</sub> / ρ','(1,1,1)','(2,1,1)'],['q<sub>I</sub>','(0,0,0)','(0,0,0)'],['F(C)','10','18'],['S<sub>on</sub>','10−151ρ/38','18−105ρ/38'],['Innere Relationen','3','1']],[158,166,166])
p('Gleiche Uhrwerte an 4 und 5 sind in C₁ zulässig: Die beiden Ereignisse sind unvergleichbar. Jede erhaltene Kausalrelation besitzt strikt wachsende Uhrwerte. Der gemeinsame Quellenbereich 0&lt;ρ&lt;1/2 garantiert insbesondere 0&lt;r₄=2ρ&lt;1.','p')
p('S₁−S₀ = 8 + 23ρ/19<br/>∂<sub>ρ</sub>(S₁−S₀) = 23/19 ≠ 0','math')
p('Damit ist eine <b>quellenabhängige geometrische Wirkungsantwort</b> bei gelösten inneren Materiegleichungen konstruiert. Die Quelle ρ verändert hier den gesamten festen äußeren Dichtekragen. Sie ist noch keine kalibrierte Gesamtmasse. Die Zahlen sind Wirkungswerte und Ableitungen, keine Übergangswahrscheinlichkeiten.','p')
p('Für die Kontrollwerte ρ=1/4 und ρ=3/8 sind die Wirkungsdifferenzen 631/76 bzw. 1285/152; ihr Unterschied ist 23/152. Diese rationalen Werte kontrollieren die hergeleitete Formel, sie sind keine unabhängigen verblindeten Vorhersagen.','p')
p('Die Ordnungsfamilie wurde strukturell klein gehalten: Bei drei freien inneren Ereignissen werden alle vier Teilmengen der zwei benachbarten Cover-Löschungen geprüft. Nur eine Löschung ergibt komplexe innere Uhren; die andere verlangt eine negative Dichte. Die doppelte Löschung liefert den positiven Konkurrenten. Minimalität wird ausschließlich für diese untersuchte Familie behauptet.','p')

page();p('3  Nullmoden kontrollieren statt übergehen','h')
p('Die Skalarwirkung ist S<sub>φ</sub>=½qᵀHq. Bei festen äußeren Skalarwerten kann H<sub>II</sub> singulär sein. Entscheidend für eine Testpaarung ist, ob ein innerer Nullvektor auch vom gesamten Rand entkoppelt ist.','p')
table([['Kontrolle','Innerer Skalarblock 2H<sub>II</sub>/β','Folge'],['N=10, Kette mit einer entfernten inneren Coverrelation','Nullmatrix; e₄−e₅ ist voller Nullvektor','Abel-Divergenz; Randgauß heilt sie nicht'],['N=11, C₀','[[0,1,−9],[1,0,1],[−9,1,0]]','Determinante −18; regulär'],['N=11, C₁','[[0,0,1],[0,0,0],[1,0,0]]','Nullrichtung e₅ koppelt an B']],[115,210,165])
p('Für beide N11-Ordnungen hat die vollständige innere Spaltenmatrix H[:,I] Rang 3. Setze P<sub>B</sub> gleich der Diagonalprojektion auf die acht Randvariablen und','p')
p('A<sub>ε</sub> = P<sub>B</sub> + εP<sub>I</sub> − iH, &nbsp; ε&gt;0.','math')
p('Die gemeinsame Paarung ist das Gaußintegral über alle elf q-Variablen mit Matrix A<sub>ε</sub>. Wäre A₀v=0, ergäbe der Realteil von v†A₀v zunächst v<sub>B</sub>=0. Dann folgte H[:,I]v<sub>I</sub>=0. Der nachgewiesene Spaltenrang erzwingt v=0. Also ist A₀ invertierbar und der gemeinsame Abel-Grenzwert endlich und ungleich null. Die Wurzel des Gaußdeterminantenfaktors wird durch stetige Fortsetzung von ε&gt;0 festgelegt.','p')
p('Dies rechtfertigt die Skalar-Testpaarung mit denselben Randdatenkonventionen. Bei exakt festgehaltenem q<sub>B</sub>=0 ist C₁ weiterhin distributionell; dort darf man keinen gewöhnlichen Punktwert einer Delta-Distribution einsetzen. Die vollständige Uhr-/Dichteintegration und ein physikalisches Zustandsmaß sind hierdurch nicht berechnet.','p')
p('Die N10-Negativkontrolle ist wesentlich: Ein diskreter Permutationsfaktor kann das kontinuierliche Nullvolumen eines vollständig entkoppelten Skalarmodus nicht entfernen. Ein neuer Quotient, eine Masse oder ein Innenzustand wäre eine zusätzliche Modellannahme.','small')

page();p('4  Quelle und Uhr: konkrete Fortschritte und Grenze','h')
p('Die Kettenkoeffizienten erfüllen Σb=0, Σkb=−1 und Σk²b=−19. Deshalb löst eine affine Uhr mit Δ²=2/(19β) die inneren Dichtegleichungen. Konstante positive Dichten lösen die vollen Uhrbilanzen bei vier festen Randlagen beidseits.','p')
p('Ein zusätzlicher Zeuge bleibt sogar in der ursprünglichen Uhrbox: Für N=10 ist<br/>T=(−1,−a,−b,−1/4,−d,d,1/4,b,a,1),<br/>mit a≈0,740258643, b≈0,485719827 und d≈0,123211769 ein gemeinsamer regulärer stationärer Materiepunkt. Eine algebraische Quartik über Q(√6), ein einfaches isolierendes Intervall und exakte Restidentitäten zertifizieren ihn. Die Dichte bleibt positiv; der Skalar-Innenblock ist invertierbar.','p')
p('Damit ist das frühere C<sub>A</sub>≥1-Hindernis als Hindernis des damaligen Randaufbaus eingegrenzt. Ein vierlagiger Kragen liefert einen anderen, tatsächlich zulässigen stationären Quellenbereich. Das ist kein Beweis eines physikalischen Hilbert-Sektors.','p')
p('Die wirkungsabgeleitete Vorwärtsrekursion lautet, sofern ihr Nenner nicht verschwindet:','p')
p('Tⱼ = [1 + (β/2)Σ<sub>k=1…4</sub>bₖT²<sub>j−k</sub>] / [βΣ<sub>k=1…4</sub>bₖT<sub>j−k</sub>].','math')
p('Die Linearisierung um die affine Lösung hat das charakteristische Polynom','p')
p('P(λ)=(λ−1)(λ³+2λ²−16λ+32).','math')
p('Eine reelle Wurzel liegt strikt zwischen −6 und −5. Damit wächst ein alternierender Störmodus um mehr als den Faktor fünf pro Vorwärtsschritt. <b>Die reguläre stationäre Randwertlösung ist keine nachgewiesene stabile Anfangswertdynamik.</b> Die Aussage betrifft diese Rekursion; sie verbietet keine andere kovariante Historiendeutung.','p')
p('Auch die gewählte positive Stromorientierung ist noch keine Massekalibrierung. Quellenbilanz, gerichtete Uhr, beobachtbare Eigenzeit und stabile Dynamik bleiben getrennte Fragen.','small')

page();p('5  Der noch fehlende physikalische Schluss','h')
p('Die ursprüngliche Dichteintegration erzeugt keinen Constraint-Projektor. Für dν(r)=(δ₀+1<sub>(0,1)</sub>dr)/2 gilt exakt','p')
p('D(C)=∫e<sup>−irC/2</sup>dν(r)=½+i(e<sup>−iC/2</sup>−1)/C, &nbsp; D(0)=1.<br/>C·D(C)=C/2+i(e<sup>−iC/2</sup>−1).','math')
p('Die rechte Seite verschwindet nicht identisch. Atom- und Endpunktbeiträge bleiben erhalten. Das Ersetzen dieses Faktors durch δ(C) wäre ein neuer Maß- und Zustandsvertrag. Eine positive Coarea-Konditionierung auf einem regulären Constraint-Ort wäre mathematisch möglich, ist aber nicht durch die ursprüngliche kompakte Integration hergeleitet.','p')
p('Die kausale Präfixzerlegung S(Cₙ)−S(Cₙ₋₁) reproduziert dagegen die volle Wirkung exakt. Auf einer Kette genügt ein Gedächtnis der letzten vier Vorgängerfelder; allgemein müssen die schnittübergreifenden Intervall- und Feldinformationen erhalten bleiben. Die neue Quellenstationarität schließt erst mit den Beiträgen des gemeinsamen Zukunftskragens.','p')
p('Eine phasenabhängige Materieauslese allein identifiziert keine Geometriedynamik. Die vorherigen sechs Historien haben nur zwei reine invariante Ordnungsalternativen; ihre intrinsischen Verläufe sind bereits definierbar. Im akzeptierten kohärenten Sektor bleibt jedoch ein strikt nichtverschwindender Kreuzterm. Ein physikalisches Gesamt-Dekohärenzfunktional einschließlich aller Ausgänge ist damit nicht vorgegeben.','p')
table([['Nächster notwendiger Schluss','Konkretes Ziel'],['Physikalische Paarung','Aus Wirkung, Maß und vollständiger Schnittinformation begründen; Atom-/Endpunktterme erhalten'],['Geometrische Verlaufsdeutung','Den inneren Relationszähler 3 versus 1 in einem konsistenten normierten Instrument oder Historienschema auswerten'],['Physische Korrespondenz','Quelle, Uhr und räumliche Geometrie gemeinsam kalibrieren; Stabilität und Verfeinerung prüfen']],[164,326])
p('<b>Arbeitsentscheidung:</b> Der N11-Vergleich ist jetzt ein konkreter Prüfstein für diesen Schluss. Ein frei gewähltes K†K, willkürliche Geschichtsgewichte oder eine nachträgliche Normierung pro Eingabe würden die offene Frage nur neu definieren. Eine Schrödinger-unitäre Darstellung wird nicht als einzig zulässige Form kovarianter Dynamik verlangt.','p')

page();p('6  Prüfnachweis und Einordnung','h')
p('Das begleitende Prüfpaket enthält sechs Fachberichte, eigenständige endliche Rechner, deren Ergebnisse, den neuen Modellvertrag und die gehashten relevanten Ausgangsdaten. Die Ordnungs- und Wirkungsformeln wurden von mehreren Bearbeitern unabhängig aus den Relationen rekonstruiert. Diese internen Kontrollen sind keine externe Begutachtung.','p')
table([['Prüfung','Reichweite'],['Quellen und Uhren','Exakte Euler-Gleichungen, reguläre Jacobi-/Hesseblöcke, zertifizierte Uhrintervalle'],['Geometrievergleich','Gemeinsamer äußerer Rand, zulässige Ordnungen, positive stationäre Quellen, exakte ΔS'],['Skalarfeld','Entkoppelte Nullmode als Negativkontrolle; endliche gemeinsame N11-Abel-Testpaarung'],['Zusammensetzung','Vollständige Präfixwirkung und Kragenbeiträge; Ableitung der stationären Wirkung nach ρ'],['Interpretation','Keine Geometrie-Wahrscheinlichkeit, kein bevorzugtes physisches Maß und keine 4D-Kollapsdynamik behauptet']],[145,345])
p('Reproduktion aus dem entpackten Verzeichnis:<br/><b>python -m pip install -r requirements.txt</b><br/><b>python -B verify.py</b><br/>Der Prüfer verwendet isolierte Kopien, kontrolliert das Manifest und vergleicht die reproduzierten JSON-Ergebnisse. Der PDF-Generator ist dafür nicht erforderlich.','p')
p('Ausgangspunkt: GitHub PR 290, main-Commit f5ee44d7cb4dc1f924eee580f1eaf0cfcb4a5bc6. Der neue Vertrag ist explorativ und nach Kenntnis der bisherigen Befunde entstanden. Die bisherigen Pakete bleiben unverändert. GitHub wurde in dieser Untersuchung nicht verändert.','small')
p('Primärliteratur zur begrifflichen Einordnung','h2')
p('1. Benincasa, Dowker: <i>The Scalar Curvature of a Causal Set</i>, Phys. Rev. Lett. 104 (2010) 181301. arxiv.org/abs/1001.2725. Die Kontinuumsdeutung setzt passende Approximationsbedingungen voraus; die kleinen Ketten erfüllen sie nicht nachgewiesen.','small')
p('2. Brightwell et al.: <i>“Observables” in causal set cosmology</i>, Phys. Rev. D 67 (2003) 084031. arxiv.org/abs/gr-qc/0210061. Intrinsische Ereignisse und Kovarianz; keine Übernahme der dortigen klassischen Wachstumswahrscheinlichkeiten.','small')
p('3. Dowker, Johnston, Surya: <i>On extending the Quantum Measure</i>, J. Phys. A 43 (2010) 505305. arxiv.org/abs/1007.2725. Positivität, Konsistenz und Erweiterung eines Historienschemas sind zusätzliche mathematische Fragen.','small')
p('4. Bombelli, Pilgrim: <i>A Tale of Two Actions: A Variational Principle for Two-Dimensional Causal Sets</i>, Class. Quantum Grav. (2021). arxiv.org/abs/2010.12985. Ein diskretes Variationskriterium ist zu begründen; eine einzelne Cover-Löschung ist hier kein Einstein-Gesetz.','small')
p('Diese Literatur stützt die begrifflichen Grenzen; sie beweist die neuen endlichen Rechnungen nicht. Deren Belege liegen im ausführbaren Paket.','small')

def footer(c,doc):
 c.saveState();c.setStrokeColor(teal);c.line(42,41,553,41);c.setFont('DV',7.2);c.setFillColor(muted)
 c.drawString(42,28,'CST-DUST · Stationärer Geometriekandidat v0.1 · Physische Dynamik offen')
 c.drawRightString(553,28,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=49,rightMargin=49,topMargin=46,bottomMargin=55,title='CST-DUST: Geometriedynamik - stationärer Kandidat v0.1',author='Thomas Gfeller · Forschungsprogramm; KI-gestützte Ausarbeitung')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
