"""Build the German research report and exact-data illustrative pointer plot."""
from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / 'CST_DUST_Physikalischer_Rand_Auslesevertrag_v0_1.pdf'
data = json.loads((ROOT/'checks/local_detector/results.json').read_text())['conditional_reduced_detector']
font='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV',font+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB',font+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
ink=HexColor('#142b3b');teal=HexColor('#067f81');muted=HexColor('#4b6170');light=HexColor('#eef5f6')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=30,textColor=ink,spaceAfter=15),
 'sub':ParagraphStyle('sub',fontName='DV',fontSize=11,leading=16,textColor=muted,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=16,leading=21,textColor=teal,spaceAfter=13),
 'h2':ParagraphStyle('h2',fontName='DVB',fontSize=11,leading=15,textColor=ink,spaceBefore=8,spaceAfter=6),
 'p':ParagraphStyle('p',fontName='DV',fontSize=9.4,leading=13.7,textColor=ink,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.2,textColor=muted,spaceAfter=6),
 'math':ParagraphStyle('math',fontName='DV',fontSize=10,leading=16,textColor=ink,backColor=light,borderPadding=9,spaceBefore=5,spaceAfter=13),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.4,leading=11.7,textColor=ink),
 'th':ParagraphStyle('th',fontName='DVB',fontSize=8.4,leading=11.7,textColor=white),
}
story=[]
def p(t,k='p'):story.append(Paragraph(t,styles[k]))
def page():story.append(PageBreak())
def table(rows,widths):
 d=[[Paragraph(str(x),styles['th' if i==0 else 'cell']) for x in row] for i,row in enumerate(rows)]
 t=Table(d,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[light,white])]))
 story.extend([t,Spacer(1,10)])

p('CST-DUST · N11 · Version 0.1 · 13. November 2026','sub')
p('Physikalischer Rand-<br/>und Auslesevertrag','title')
p('Ein konstruktiver gemeinsamer Skalarvertrag.<br/>Eine präzise Grenze seiner physikalischen Herleitung.','sub')
p('<b>Das Ergebnis ist positiv und bedingt:</b> Für beide N11-Geometrien sind jetzt konkrete, exakt normierte Quantenübergänge auf demselben dreimodigen Skalarraum konstruiert. Ein gemeinsamer lokaler Detektor liefert daraus vollständige Wahrscheinlichkeiten, einschließlich kohärenter Interferenz und eines Fehlschlagausgangs.','p')
p('Gemeinsamer Raum: H₃=L²(R³,dx)<br/>Akzeptierte Karte: K=ω₀W₀V₀+ω₁W₁V₁, &nbsp; ‖K‖≤1.<br/>Auslese: M<sub>y</sub>K; &nbsp; Fehlschlageffekt: I−K†K.','math')
table([['Frage','Ergebnis'],['Welche Möglichkeiten scheiden aus?','Unreduzierte gemeinsame Vier-Moden-Norm und gleichzeitiger starker Randconstraintkern scheitern.'],['Was funktioniert konkret?','Ein zusätzlicher gemeinsamer Drei-Moden-Quotient mit berechneten Normfaktoren und festgelegten Fresnelphasen.'],['Wählt die ursprüngliche Wirkung ihn aus?','Nein. Die gemeinsame Projektion, das volle Uhr-/Dichteskalarprodukt, Historienmaß und Apparatur benötigen weitere physikalische Festlegungen.']],[165,325])
p('<b>Wichtige neue Einordnung:</b> Die bisherige Antwort auf den beidseitigen Dichteparameter stammt im geprüften Vertrag vollständig vom späteren Rand. Eine isolierte Änderung der früheren Dichte hat bei festen Randuhren exakt keinen Einfluss auf die Records.','p')
p('Ausgangspunkt: veröffentlichter Stand aus PR #292, Commit 06ca1444d582f2c3563e0be015b5ae7c3dbc9c49. Sechs Fachagenten; unabhängige exakte Rekonstruktionen. Interne KI-gestützte Prüfung, keine externe wissenschaftliche Begutachtung.','small')

page();p('1  Modell und einseitiger Quellentest','h')
p('C₀ ist die vollständige Kette aus elf Ereignissen. C₁ entfernt ausschließlich (4,5) und (5,6), behält (4,6). P={0,1,2,3}, I={4,5,6}, F={7,8,9,10}. β=4/√6; b=(1,−9,16,−8), danach null.','p')
p('Cⱼ(T)=1+(β/2)Σ<sub>i≺j</sub>bᵢⱼ(Tⱼ−Tᵢ)²<br/>S=F(C)−½ΣⱼrⱼCⱼ(T)−(β/4)Σ<sub>i≺j</sub>bᵢⱼ(qⱼ−qᵢ)².','math')
p('Äußere Uhren: Tⱼ=(j−5)Δ, Δ²=√6/38. Inneres Uhrmaß: dT/3 auf [−3/2,3/2] je Variable, ohne zusätzliches Ordnungs-Theta. Inneres Dichtemaß: (δ₀+1<sub>(0,1)</sub>dr)/2 je Variable. Alle acht Atom-/Positivstrata bleiben erhalten. Frühere und spätere Randdichten heißen jetzt getrennt ρ<sub>P</sub> und ρ<sub>F</sub>.','p')
p('Für beide Ordnungen gilt unabhängig von inneren Uhren<br/>Σ<sub>j∈P</sub>Cⱼ=151/19.<br/>Daher exakt: W<sub>c</sub>(ρ<sub>P</sub>,ρ<sub>F</sub>)=<br/>exp(−i151ρ<sub>P</sub>/38) W̃<sub>c</sub>(ρ<sub>F</sub>).','math')
p('Eine alleinige Änderung von ρ<sub>P</sub> erzeugt dieselbe globale Phase in beiden Zweigen. Sie fällt aus allen Record- und Fehlschlagwahrscheinlichkeiten des festgehaltenen Instruments heraus. Diese Aussage gilt auch für die konditionierten Records, sofern die Akzeptanzwahrscheinlichkeit positiv ist.','p')
table([['ρ<sub>F</sub>','|W₁/W₀|, beide ρ<sub>P</sub>','∂<sub>ρP</sub> log(W₁/W₀)'],['1/8','1,605547531','0 exakt'],['1/4','1,869370057','0 exakt']],[95,220,175])
p('Vier Kombinationen aus ρ<sub>P</sub>,ρ<sub>F</sub>∈{1/8,1/4} und getrennte Ableitungen wurden mit n=128 und n=160 pro Uhrenachse gerechnet. Der relative Zukunftsrandkontrast bleibt vorhanden. Die frühere Variation ρ<sub>P</sub>=ρ<sub>F</sub> hat beide Ränder gleichzeitig verändert.','p')
p('<b>Reichweite:</b> Kein allgemeiner Unmöglichkeitssatz für Rückwirkung. Bei integrierten vergangenen Uhrpaketen steht die Phase im Integral und lässt sich nicht ohne Weiteres herausziehen. Die Rechnung korrigiert die kausale Interpretation dieses konkreten Dirichletexperiments. W enthält die vollständige Wirkung bereits; eine weitere On-shell-Phase würde doppelt zählen.','small')

page();p('2  Was die skalare Randvariation ausschließt','h')
p('Mit S<sub>φ</sub>=½qᵀHq, H=−βL/2, sind die orientierten Randimpulse p<sub>P</sub>=−∂<sub>P</sub>S und p<sub>F</sub>=∂<sub>F</sub>S. Wir schreiben π=p/β; damit [q,π]=i/β. Die sieben unbekannten inneren und zukünftigen Konfigurationen sind aus dem Anfangsrand durch die Legendre-Matrix H<sub>(I,P),(I,F)</sub> bestimmt, falls diese invertierbar ist.','p')
table([['','C₀','C₁'],['Legendre-Rang','7; det=−16384β⁷','6'],['Randstruktur','Reguläre Vier-Paar-Karte M₀','Je ein Prä- und Postconstraint'],['Gemeinsame unreduzierte L²(R⁴)-Norm','Normierbar unter kanonischer Paarungswahl','Nichtnulliger Ausgang nicht normierbar']],[200,145,145])
p('A₋=−128q₀+241q₁+119q₂−232q₃<br/>−46π₀−32π₁−16π₂.<br/>A₊=−232q₇+119q₈+241q₉−128q₁₀<br/>+16π₈+32π₉+46π₁₀.','math')
p('Die C₁-Identität Â₊K₁=0 folgt bereits punktweise aus dem vollen Wirkungshessian. Nichtverschwindende Lösungen haben konstanten Betrag entlang einer nichtkompakten Constraint-Richtung. Ihr Vier-Moden-Lebesgue-Normquadrat divergiert. Eine endliche Schwartz-Paarung ist deshalb noch keine Ausgangsnorm.','p')
p('Ein vollständiger Detektor repariert diese Norm nicht:<br/>∫dy ‖M<sub>y</sub>ψ‖²=‖ψ‖², &nbsp; auch beim Wert ∞.','math')
p('Zieht man den Postconstraint mit der regulären Karte zurück, B=A₊M₀, ergibt sich die physische Klammer {A₋,B}=−52625/(32β). Beide starken Quantenbedingungen gleichzeitig besitzen daher nur die Null-Lösung auf einem kompatiblen gemeinsamen Testbereich.','p')
p('<b>Dieser Ausschluss ist eng.</b> Er betrifft die bloße starke Einschränkung des ursprünglichen Vier-Moden-Operators. Ein Rigging-Sandwich zwischen Quotienten ist eine andere Konstruktion. Gerade die nichtverschwindende Klammer ermöglicht die im nächsten Abschnitt verwendete transversale Auswahl.','p')

page();p('3  Ein gemeinsamer positiver Drei-Moden-Vertrag','h')
p('Wir wählen zusätzlich die C₁-Prä-/Postquotienten als gemeinsamen Randvertrag beider Geometrien. Sektionen sind q₀=0,A₋=0 am Eingang und q₁₀=0,A₊=0 am Ausgang. Die verbleibenden Positionen sind x=(q₁,q₂,q₃), Q=(q₇,q₈,q₉).','p')
p('Für C₀ wird entlang des A₋-Flusses der Vertreter B=0 gewählt, dann M₀ angewandt und am Ausgang quotiert. C₁ wird direkt aus seiner eingeschränkten Randrelation gelöst. Beide erhaltenen 6×6-Karten R₀,R₁ sind exakt symplektisch. Die vollständigen rationalen Matrizen liegen im Prüfpaket.','p')
p('C₀: S₀=⟨Π<sub>t,+</sub>=0|T₊U₀T₋⁻¹|Π<sub>t,−</sub>=0⟩<br/>S₀†S₀=β/[2π(52625/32)] · I.<br/>V₀=√[2π(52625/32)/β] · S₀.','math')
p('Der Ausdruck wird als oszillierender Kern zwischen Quotienten ausgewertet; er ist kein Produkt gewöhnlicher beschränkter Vier-Moden-Projektoren. Der berechnete Zweivariablen-Gaußhessian besitzt det=4716800/9 und Signatur −2. Zusammen mit der ursprünglichen Fresnelphase erhält der normierte C₀-Kern die Phase −π/4.','p')
p('C₁: V₁(Q,x)=[92√2 β/(2π)] δ(ℓ) exp(iβΦ₁),<br/>ℓ=8x₀−(9/2)x₁+x₂/2+Q₀/2−(9/2)Q₁+8Q₂.<br/>V₁†V₁=V₁V₁†=I.','math')
p('Die beiden Kompositionsrichtungen liefern denselben Delta-Jacobi-Betrag 2116. Der Faktor relativ zum nackten Sektionskern ist 23√2 β³/(4π³); seine Fresnelphase ist null. Das nichtkompakte Orbitvolumen wird quotiert; doppeltes unbereinigtes Gruppenmitteln wäre divergent.','p')
table([['Berechnet innerhalb des Vertrags','Zusätzlich festgelegt'],['R₀,R₁, beide Quanten-Normfaktoren, konkrete Gauß-/Deltakerne','Gemeinsamer C₁-Quotient auch für C₀; CCR und Lebesgue-Paarung'],['Relative Phase aus positiver Normierung und geerbter Abel-/Fourierkonvention','Genau diese Fourier-/Quotienten- und Phasenfortsetzung']],[245,245])
p('Die Operatoren implementieren die linearen kanonischen Karten unitär. Die Karte allein bestimmt keine globale U(1)-Phase. Eine universelle Phasen-/Kompositionsregel für beliebige weitere Geometrien und Schnitte ist hier nicht bewiesen. Das ursprüngliche kompakte Staubmaß wählt diese gemeinsame Reduktion ebenfalls nicht aus.','small')

page();p('4  Ein real formulierter lokaler Messvertrag','h')
p('Der neue normierte Eingang ist ψ<sub>in</sub>(x)=(β/π)<super>3/4</super>exp(−β|x|²/2). Ein Pointer mit Gaußbreite σ koppelt an Q=q₇: U<sub>g</sub>=exp(−igq₇p<sub>y</sub>). q₇ ist unter dem C₁-Postconstraint invariant. Derselbe Apparat wird für beide Geometrien verwendet.','p')
p('M<sub>y</sub>=(2πσ²)<super>−1/4</super> exp[−(y−gq₇)²/(4σ²)],<br/>∫dy M<sub>y</sub>†M<sub>y</sub>=I.<br/>Nichtselektiver Kohärenzfaktor:<br/>exp[−g²(q₇−q′₇)²/(8σ²)].','math')
p('Der Überlapp ist damit ein aus der Kopplung abgeleiteter Feldkern. Er ist kein unabhängig einstellbares Klassen-γ. Seine Integration mit den beiden tatsächlichen Ausgangszuständen bestimmt den Record-Kreuzterm.','p')
rows=[['Einzeln präparierter Zweig','Var(y), g=σ=1','P(|y|≤1)']]
for label,row in zip(['C₀','C₁'],data['actual_branch_records']):
 rows.append([label,f"{float(row['pointer_variance_decimal']):.8f}",f"{float(row['P_abs_y_le_1_decimal']):.8f}"])
table(rows,[190,150,150])
y=np.linspace(-14,14,1200)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(7.4,2.75),layout='constrained')
for label,color,row in zip(['C₀','C₁'],['#067f81','#a84a24'],data['actual_branch_records']):
 v=float(row['pointer_variance_decimal']);ax.plot(y,np.exp(-y*y/(2*v))/math.sqrt(2*math.pi*v),color=color,label=label,lw=2)
ax.axvspan(-1,1,color='#b4c3cc',alpha=.22);ax.set(xlabel='Pointerwert y (erklärte Modellkoordinate)',ylabel='Normierte Dichte',xlim=(-14,14),ylim=(0,.28));ax.legend(frameon=False);ax.grid(alpha=.15)
fig.savefig(HERE/'pointer_branch_reference.png',dpi=180);plt.close(fig)
story.append(Image(str(HERE/'pointer_branch_reference.png'),width=490,height=182))
p('Bedingte Referenz: jede Kurve ist ein separat präparierter reduzierter N11-Zweig. Sie zeigt nicht die kohärente Gesamtverteilung und ist keine Messdatenauswertung. Die schattierte Fläche markiert |y|≤1.','small')
p('Die vollständigen Zweigzustände haben |⟨ψ₀|ψ₁⟩|≈0,00814923. Der klassische Überlapp der Pointerverteilungen ist dagegen ≈0,77564616. Diese Größen haben unterschiedliche Bedeutung; unterschiedliche Kurven ergeben keine perfekte Historienmessung.','p')

page();p('5  Kohärente vollständige Wahrscheinlichkeiten','h')
p('Zur Normierung des gesamten Experiments wird eine zusätzliche Kontrolle mit |w⟩=Σ√ω<sub>c</sub>|c⟩, ω<sub>c</sub>≥0, Σω<sub>c</sub>=1, eingeführt. Eine Hilfsumwelt L²(μ) trägt das ursprüngliche normierte innere Uhr-/Dichtemaß; ihr Eingang ist die konstante Einsfunktion. Die kontrollierte Multiplikation mit exp(iS<sub>c</sub>) und der jeweilige Skalaroperator V<sub>c</sub> sind unitär.','p')
p('Akzeptanz der gleichen Kontroll-/Umweltpräparation ergibt<br/>K=Σ<sub>c</sub>ω<sub>c</sub>W<sub>c</sub>V<sub>c</sub>, &nbsp; ‖K‖≤Σω<sub>c</sub>|W<sub>c</sub>|≤1.<br/>∫dy K†M<sub>y</sub>†M<sub>y</sub>K + (I−K†K)=I.','math')
p('Das orthogonale Ancillakomplement liefert den Fehlschlagkanal. Die Karte ist damit auf ganz H₃ vollständig, ohne einen willkürlichen kleinen Verstärkungsfaktor einzusetzen. Die Umwelt- und Kontrollinterpretation ist ein explizites zusätzliches Modell; ω ist eine Präparation und kein hergeleitetes fundamentales Historienmaß.','p')
p('Die geerbten, fixierten Kernphasen ergeben<br/>z=⟨ψ₀|ψ₁⟩≈0,003116950321+0,007529582765 i.<br/>Für ω₀=ω₁=½:<br/>p<sub>acc</sub>=(|W₀|²+|W₁|²)/4 + Re(W₀*W₁z)/2.','math')
table([['Größe','ρ<sub>F</sub>=1/8','ρ<sub>F</sub>=1/4'],['p<sub>acc</sub>','0,31289945','0,29064945'],['p<sub>fail</sub>','0,68710055','0,70935055'],['Var(y | acc)','7,81211583','6,70761575'],['P(|y|≤1 | acc)','0,39190287','0,40990763']],[220,135,135])
p('Die Tabellenwerte gelten für beide geprüften früheren Dichten ρ<sub>P</sub>=1/8 und 1/4. Analytische Gaußfortsetzung bestimmt die komplexen Wurzeln; ein unkontrollierter Hauptwurzelwechsel wird vermieden. Die Veränderung mit ρ<sub>F</sub> ist eine Änderung des künftigen Randfilters, keine nachgewiesene anfängliche Quellenrückwirkung.','p')
p('Die Zahlen verwenden die vollständigen endlichen W-Gewichte. Der größte beobachtete Unterschied zwischen n=128 und n=160 in den neuen kohärenten Kennzahlen liegt etwa bei 1,6·10⁻¹⁴. Dies ist eine Konvergenzdiagnose, kein vollständiges Rundungsintervall.','small')

page();p('6  Warum die volle physische Auswahl offen bleibt','h')
p('Die vollständige Uhr-/Dichte-Randvariation besitzt vier identisch verschwindende Zeilen in der 14×14-Zukunftsmatrix. Die früheren Dichteimpulse sind Constraints p<sub>r,P</sub>=C<sub>P</sub>/2. An den stationären Referenzen ergeben sich Ränge 10 (C₀) und 9 (C₁); beide inneren Hesseformen sind regulär.','p')
p('Für C₁ bleibt sogar bei festen Zukunftsdichten und allen gleichen anfänglichen kanonischen Daten eine exakte Familie:<br/>u<sub>F</sub>=(7,8,9,10)+α(0,8,16,23),<br/>ΔS=−αρ(932α+217)/19.','math')
p('Innere Gleichungen und sämtliche Anfangsimpulse bleiben gleich, zukünftige Impulse ändern sich. Kleine α bleiben im zulässigen Bereich. Das ist keine bloße lineare Nullrichtung und keine globale Uhrverschiebung. Eine physische Eichidentifikation dieser Ausgänge muss zusätzlich begründet werden. Auch die bekannten C₀-/C₁-Sättel besitzen verschiedene anfängliche Uhrimpulse; sie waren keine Vergleiche mit vollständig identischen Cauchydaten.','p')
table([['Verbleibender Vertrag','Konkretes Hindernis'],['Kompakte Dichteintegration als Constraintprojektor','D(C)=½+(1−exp(−iC/2))/(iC); bei C=4π ist C·D(C)=2π statt null.'],['Dichteverschiebung als globale unitäre Eichgruppe','r hat Spektrum [0,1]. Unitäre Konjugation kann es nicht auf [s,1+s] verschieben. Andere Quantisierungen bleiben möglich.'],['Uhr-Shift im festen Integrationskasten','Partielle Integration erzeugt Randflächen. Wirkungsinvarianz allein entfernt sie nicht.'],['Historienmaß aus Konsistenzbedingungen','Positive kovariante komponierbare Familien und normierte kausale Wachstumsfamilien bleiben mehrparametrig.']],[185,305])
p('Explizit: μ<sub>λ</sub>(C)=exp[−λR(C)] liefert μ₁/μ₀=exp(2λ). Transitive Perkolation liefert p(1−p)² pro festem natürlichen Vertreter oder 3p(1−p)² nach Vergessen der natürlichen Beschriftung. Beide Konventionen sind verschieden; der Faktor drei ist kein Automorphismenfaktor. Die Wahl p bleibt frei.','p')
p('Normierte kompakte Uhr-/Dichtepakete sind im bisherigen Hilfsmaß konstruiert; ein physisches Skalarprodukt und ihre vollständige Integration in das neue Experiment sind nicht hergeleitet. Klassische Wachstumswahrscheinlichkeiten bestimmen zudem nicht von selbst Quantenamplituden oder deren Phasen.','small')

page();p('7  Prüfstatus und anschlussfähiger nächster Schritt','h')
table([['Aussage','Status'],['Ein gemeinsamer positiver Skalar- und Messvertrag existiert','Konstruiert und unabhängig geprüft'],['Seine Normfaktoren sind bloße Fitparameter','Nein: im erklärten Vertrag exakt berechnet'],['Der ursprüngliche Vier-Moden-Vertrag ist ausreichend','Ausgeschlossen für nichtverschwindenden C₁-Zweig'],['Die Wirkung wählt die neue Projektion und Apparatur eindeutig','Nicht gezeigt; explizite Zusatzannahmen'],['Bisheriger Kontrast belegt eine frühe Quellenrückwirkung','Nein, im festen Uhrvertrag vollständig Zukunftsrandantwort'],['Physikalische Geometriedynamik und Staubball-Bounce abgeleitet','Weiterhin offen']],[310,180])
p('<b>Reproduzierbarkeit:</b> Der Prüfer kontrolliert Elternprovenienz und vollständige SHA-256-Dateihashes. Er führt die wissenschaftlichen Rechner in einer isolierten Kopie aus und vergleicht deren Ergebnisse. Exakte Ränge, Matrixidentitäten, Normfaktoren, Ward-Identitäten und Quellenfaktorisierung werden algebraisch geprüft; die Uhrgewichte werden neu integriert.','p')
p('Historienkontrollen: 6.390 natürliche Präfixvergleiche, 51 Elternnormierungen und 3.645 Bell-Verhältnisse. Die skalaren Ausgangs-Gaußformen werden zusätzlich gegen die kanonischen Karten geprüft. Die gemeinsame Quelle und die Quantennormierungen wurden unabhängig rekonstruiert.','p')
p('Reproduktion:<br/><b>python -m pip install -r requirements.txt</b><br/><b>python -B verify.py</b>','math')
p('<b>Nächster physikalischer Schritt:</b> Eine Anfangspräparation von Uhr und Dichte samt positivem physischem Skalarprodukt begründen und bei festem späterem Instrument einsetzen. Dann die frühere Materiequelle variieren, ohne spätere Filter oder Historiengewichte mitzudrehen. Erst eine robuste Antwort in diesem Vertrag wäre ein geeigneter nächster Kandidat für dynamische Rückwirkung.','p')
p('Die noch fehlende Wahl ist kein bloß numerischer Rest. Sie verlangt zusätzliche physikalische Struktur oder eine experimentell begründete Präparation. Ein weiterer großer Rechenlauf im unveränderten Dirichletvertrag kann sie nicht ersetzen. Die vorhandene Drei-Moden-Konstruktion liefert dafür einen konkret überprüfbaren Ausgangspunkt.','p')
p('Primärliteratur zur Einordnung','h2')
p('P. A. Höhn: <i>Quantization of systems with temporally varying discretization I: Evolving Hilbert spaces</i>, arxiv.org/abs/1401.6062. D. Giulini: <i>Group Averaging and Refined Algebraic Quantization</i>, arxiv.org/abs/gr-qc/0003040. D. P. Rideout, R. D. Sorkin: <i>A Classical Sequential Growth Dynamics for Causal Sets</i>, arxiv.org/abs/gr-qc/9904062, §4.2, Gl. (6). Die neuen endlichen Rechnungen sind eigene Ableitungen im Prüfpaket; die Literatur wird nicht als Beweis dieser Ergebnisse ausgegeben.','small')

def footer(c,doc):
 c.saveState();c.setStrokeColor(teal);c.line(42,41,553,41);c.setFont('DV',7);c.setFillColor(muted)
 c.drawString(42,28,'CST-DUST · Bedingter positiver Randvertrag · Physikalische Auswahl offen')
 c.drawRightString(553,28,str(doc.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=49,rightMargin=49,topMargin=46,bottomMargin=55,title='CST-DUST: Physikalischer Rand- und Auslesevertrag v0.1',author='Thomas Gfeller · Forschungsprogramm; KI-gestützte Ausarbeitung')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
