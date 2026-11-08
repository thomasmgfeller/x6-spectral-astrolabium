#!/usr/bin/env python3
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
import json
ROOT=Path(__file__).resolve().parent
FONT=Path('/usr/share/fonts/truetype/dejavu')
for n,f in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
NAVY=HexColor('#173447'); TEAL=HexColor('#16756F'); INK=HexColor('#233640'); MUTED=HexColor('#59717C'); LIGHT=HexColor('#EEF4F5'); GOLD=HexColor('#AE701D')
styles={
 'kicker':ParagraphStyle('kicker',fontName='DV-Bold',fontSize=9,leading=13,textColor=TEAL,spaceAfter=14),
 'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=25,leading=31,textColor=NAVY,spaceAfter=18),
 'h':ParagraphStyle('h',fontName='DV-Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=12),
 'sub':ParagraphStyle('sub',fontName='DV-Bold',fontSize=10.3,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='DV',fontSize=9.4,leading=14.8,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.1,leading=11.5,textColor=MUTED,spaceAfter=6),
 'formula':ParagraphStyle('formula',fontName='Mono',fontSize=9,leading=14,textColor=NAVY,spaceAfter=0),
}
def p(s,sty='body'): return Paragraph(s,styles[sty])
def code(lines):
    rows=[[p(escape(line),'formula')] for line in lines]
    t=Table(rows,colWidths=[475]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,0),10),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
    return KeepTogether([t,Spacer(1,11)])
def table(rows,widths):
    data=[[p(str(c),'small' if i else 'kicker') for c in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#D4DFE2')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
story=[]
def add(*xs): story.extend(xs)
def page(k,title):
    if story: add(PageBreak())
    add(p('CST-DUST  /  '+k,'kicker'),p(title,'h'))
add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Randpräparation und<br/>Reaktionsbilanz','title'),p('Staubball: nächster mathematischer Prüfschritt nach PR 266','sub'))
add(p('Eine passende Randphase kann die benötigte Reaktion des Vergangenheitskragens tragen. Ihr Gradient ist jedoch zusätzliche Randinformation: Am selben Kragen unterstützt eine einzelne glatte Phase höchstens einen inneren Lösungszweig.'))
add(code(['Kragen: T* = (-5/2, -2, -4/3, 0)', 'Gewichte: B = (-8, 16, -9, 1)', 'Für t = w = 1/2 benötigt der Rand:', 'p = (6, -10, 33/8, -1/8).']))
add(p('Das zentrale neue Ergebnis','sub'),p('Ein expliziter normierter Zustand endlicher Breite trägt diese Reaktion im Mittel. Die stärkere Forderung nach gleichzeitig exakt verschwindenden inneren und äußeren Operatorbedingungen scheitert im geprüften kinematischen Ansatz an einem nichtverschwindenden Kommutator.'))
add(table([['Ergebnis','Status'],['Reaktionsdaten und lokale Phasenbedingung','analytisch bestimmt'],['Normierter Prüfzustand mit mittlerer Randbilanz','konstruiert'],['Gemeinsame exakte naive Operatorbedingungen','in diesem Ansatz ausgeschlossen'],['Physikalische Präparation / Skalarprodukt / Bounce','weiterhin offen']], [330,145]))
add(Spacer(1,14),p('<b>Alle acht physikalischen Gates: HOLD.</b> Kein kostenpflichtiger Rechenlauf. Kein n=5-Produktionslauf. Keine externe Replikation.','body'))
add(p('Basis: Main 8d1a3e0906611ec23fdee3088a6bf864d0bd9edc, nach PR 266. Vollständige Beweise, Quellenbindung und Reproduktionscode liegen im begleitenden Prüfpaket.','small'))

page('01  /  KLASSISCHE RANDDATEN','Welche Randinformation fehlt?')
add(p('Die Geometrie bleibt eine feste Kette. Vier frühere Dichten sind null; nur die Uhr t und die positive innere Dichtevariable 0&lt;w&lt;1 des letzten Elements werden frei variiert. Es wird keine physikalische Ruhemasse aus w abgeleitet.'))
add(code(['m1 = Σ B_y T_y;   m2 = Σ B_y T_y²', 'C = 1 - t m1 + m2/2;   S = -w C/2', 'q_t = w m1/2;   q_y = w B_y(t-T_y)/2']))
add(p('Am Kragen T* gilt m1=0, m2=-2. Beide inneren Gleichungen sind erfüllt, aber die Randreaktion verschwindet nicht: Σq_y=0 und ΣT_yq_y=w. Eine nur geometrieabhängige Randwirkung kann diese Uhrreaktion bei festgehaltener Geometrie nicht ausgleichen.'))
add(p('Lokale Phasenbedingung','sub'),p('Für die ausdrücklich gewählte Kontraktion ∫ψ_B(T)exp(iS/ℏ)dT, mit ψ_B=a exp(iW/ℏ), verlangt reelle Phasenstationarität ∂W=-q. Eine konjugierte Randamplitude würde das Vorzeichen umkehren.'))
add(code(['p_y = (w/2) B_y(T*_y-t)', 'w = -Σ T*_y p_y;   t = -2 p_3/w', 'Zusätzlich: 0<w<1, t>0 und alle vier', 'Komponenten der ersten Zeile rückprüfen.']))
add(p('Die Vektoren B und B·T* sind unabhängig. Deshalb kann derselbe Gradient p am selben Kragen nur ein Paar (t,w) tragen. Ein beliebiger Vektor mit Σp=0 genügt nicht. Mehrere Phasenzweige, andere Kragen oder Korrelationen mit Außenvariablen bleiben möglich.'))
add(p('Kritische Abgrenzung','sub'),p('W=-S mit nachgeführten freien t,w würde die gesamte Wirkung auslöschen und damit die Normierungsbedingung entfernen. Zulässig als Diagnose ist eine Phase, die auf ein festes Paar (t*,w*) eingestellt bleibt. Auch diese Wahl ist keine dynamisch begründete Zustandsauswahl.'))

page('02  /  KONKRETER PRÜFZUSTAND','Ein Randpaket mit endlicher Breite')
add(p('Für diese Diagnose werden t=t*≥1/4 und w=w*&gt;0 fixiert. Der zusätzliche kinematische Raum ist L²(Ω,d⁴δ), Ω=(-ε,ε)⁴, mit δ=T-T* und 0&lt;ε≤1/64. Die Amplitude hat verschwindende Randspur; dadurch bleibt der Träger innerhalb der richtigen Kettenordnung.'))
add(code(['aε(δ) = ε^(-2) Π_y cos(πδ_y/(2ε))', 'ψε = aε exp[-i S(t*,w*,T*+δ)/ℏ]', '||ψε|| = 1;   <P_y> = -<q_y> = p_y']))
add(p('Das Produkt ist normiert, weil jeder cos²-Faktor auf (-ε,ε) zu ε integriert. Der mittlere Ableitungsterm der reellen Amplitude verschwindet. Die Phase trägt deshalb genau den notwendigen mittleren Randimpuls.'))
add(p('Mittelwert und vollständige Abweichung','sub'),p('Prüft man zusätzlich R_y=P_y+q_y als Randoperator, bleiben trotz ⟨R_y⟩=0 positive Normresiduen. Das ist eine zusätzliche Operatorinterpretation; sie folgt nicht aus der bisherigen CST-Amplitude.'))
add(code(['E_R = Σ ||R_y ψε||² = π²ℏ²/ε²', 'c2 = 1/3 - 2/π²', 'c4 = 1/5 - 4/π² + 24/π⁴', 'K(t) = 402t² + 1560t + 1568', 'E_q = ||q_t ψε||² = (201/2)w*²c2 ε²', 'E_C = ||C ψε||²', '    = c2 K(t*)ε² + (201/2)(c4-c2²)ε⁴']))
add(p('Die Grenze für E_R ist auf diesem Würfel mit Nullrandspur optimal: Nach Entfernung der Phase ist sie die erste Dirichlet-Eigenzahl. Der Produkt-Cosinus erreicht sie. Ein schärferer Rand senkt E_q und E_C, erhöht bei festem ℏ aber E_R.'))
add(p('P_y wird auf H₀¹ als symmetrischer Differentialoperator verwendet. Eine selbstadjungierte Dirichlet-Impulsrealisierung und ein physikalisches Skalarprodukt werden nicht behauptet.','small'))

page('03  /  CONSTRAINT-PRÜFUNG','Warum die naive gemeinsame Bedingung scheitert')
add(p('Das Problem liegt nicht nur an der Wahl des Pakets. Auf dem deklarierten Raum besitzt die innere Uhrfunktion mit den getesteten Randoperatoren eine feste Kommutatorantwort.'))
add(code(['[q_t, R_y] = iℏ w* B_y/2', 'v = B/√402;   R_v = Σ v_y R_y', '||q_t ψ|| ||R_v ψ|| ≥ ℏ w*√402/4', 'E_q Σ ||R_y ψ||² ≥ (201/8)ℏ²w*²']))
add(p('Der Beweis benötigt nur Integration durch Teile und Cauchy-Schwarz; die verschwindende Randspur beseitigt die Randterme. Er gilt in der entsprechenden schwachen Form auf H₀¹. Für ℏ&gt;0 und w*&gt;0 können damit nicht alle geforderten Residuen zugleich null sein.'))
add(p('Bedeutung für den nächsten Theorievertrag','sub'),p('Schon die analoge kanonische Poissonklammer ist ungleich null. Das gemeinsame Erzwingen dieser Gleichungen ist also kein nachgewiesenes erstklassiges Constraint-System. Eine vollständige kanonische Analyse, zusätzliche Randvariablen oder eine Reduktion könnten eine andere physikalische Konstruktion liefern.'))
add(table([['Aussage','Reichweite'],['Exakte gemeinsame Nullbedingungen','ausgeschlossen im getesteten Raum / Operatoransatz'],['Mittlere Reaktionsbilanz','durch das explizite Paket erfüllt'],['Physikalische CST-Randzustände allgemein','durch diesen Test nicht ausgeschlossen'],['Verschwindende Breite bei festem ℏ','Randresiduum wächst ohne Grenze']], [237,238]))
add(Spacer(1,12),p('Im zusätzlichen formalen Doppellimit ε→0 und ℏ/ε→0 können die Residuen zugleich klein werden. Das ist weder eine normierte Zustandsgrenze bei festem ℏ noch ein kalibrierter semiklassischer CST-Limes.','small'))

page('04  /  MASS UND MODELLAUSWAHL','Eine Momentfläche ist noch keine Präparation')
add(p('Die zwei Bedingungen F₁=m₁=0 und F₂=m₂+2=0 definieren lokal eine zweidimensionale Fläche in den vier Randuhren. Einfach alle Zustände darauf zu beschränken wäre eine zusätzliche Entscheidung über Wirkung und Skalarprodukt.'))
add(code(['J_F² = 4[(Σ B²)(Σ B²T²) - (Σ B²T)²]', 'Am Kragen: J_F² = 87744 > 0', 'd⁴T δ(F1)δ(F2) = dH²(T)/J_F(T)']))
add(p('Die Coarea-Formel zeigt, dass sogar ein zusätzlich gewähltes konditioniertes Lebesgue-Maß einen Jacobian braucht. Eine Neubeschreibung der Bedingungen verändert dessen Gewicht, sofern das Maß nicht passend mittransformiert wird. Eine physikalische Rigging-Map ist damit nicht gegeben.'))
add(p('Was die vorbereitete Rechnung jetzt ermöglicht','sub'))
for s in [
 'Eine vorgeschlagene Außenraum- oder Randamplitude kann gegen die konkrete Reaktionsanforderung ∂W=-q geprüft werden.',
 'Ein Vorschlag für Operator-Constraints kann mit dem berechneten Kommutator auf gemeinsame Verträglichkeit getestet werden.',
 'Endliche Präparationsbreiten können mit getrennten inneren und äußeren Normresiduen bewertet werden; verschwindende Mittelwerte reichen nicht.'
]: add(p('• '+s))
add(p('Nächster physikalischer Schritt','sub'),p('Eine Randamplitude aus einer unabhängig begründeten Materie-/Außenraumkopplung herleiten oder eine vollständige kanonische Reduktion des gemeinsamen Systems formulieren. Dabei müssen Randvariablen, Phase, Amplitude, Maß und die Bedeutung der Gleichungen gemeinsam festgelegt werden.'))
add(p('<b>Offen bleiben:</b> physikalische Präparation, Constraintalgebra, Skalarprodukt, gemeinsame Geometrievariation, Rückwirkung, klassischer Anschluss und Bounce. Ein größerer Integrationslauf ersetzt diese Modellentscheidung nicht.'))

page('05  /  PRÜFUNG UND QUELLEN','Reproduzierbar, mit klaren Anspruchsgrenzen')
r=json.loads((ROOT/'results/verification.json').read_text())
add(table([['Kontrolle','Umfang / Ergebnis'],['Stationäre Kragen und Impulsrekonstruktion',str(r['exact_stationary_cases'])+' / PASS'],['Verschiedene lokale Phasengradienten',str(r['distinct_phase_pairs'])+' Paarvergleiche / PASS'],['Gestörte Randdaten',str(r['perturbed_cases'])+' Fälle / PASS'],['Ableitungen von Wirkung und fester Randphase','je 2916 exakt rationale Komponenten / PASS'],['Kommutatorkoeffizienten','108 exakt rationale Ableitungen / PASS'],['Paketbudgets','9 rationale Intervalle / PASS'],['Konkrete Negativkontrollen','6 erwartete Ausschlüsse / PASS']], [295,180]))
add(Spacer(1,12),p('Rationale Grenzen für π entstehen aus der Machin-Identität und alternierenden arctan-Reihen. Gleitkommawerte in den Ergebnissen sind nur Lesehilfen. Drei Ergebnisdateien werden in einem isolierten Verzeichnis bytegleich reproduziert. Der Plan wurde nach analytischem Entwurf und vor den endlichen Kontrollen gehasht; keine externe Präregistrierung.'))
add(code(['python3 -B verify_package.py', 'python3 -B replay.py']))
add(p('Quellen und Abgrenzung','sub'))
for text,url in [
 ('Projekt: PR 266, Vergangenheitskragen und Randzustände. Vier unveränderte Quellendateien samt Git-Identitäten im Paket.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/266'),
 ('Buck et al. (2015), Boundary Terms for Causal Sets. Geometrische raumartige Randterme, keine Herleitung der hier gewählten Materiephase.','https://arxiv.org/abs/1502.05388'),
 ('Brown und Kuchař (1995), Dust as a standard of space and time in canonical quantum gravity. Eigenständige kanonische Staubkonstruktion.','https://doi.org/10.1103/PhysRevD.51.5600'),
 ('Dowker, Liu, Lloyd-Jones, Timelike boundary and corner terms in the causal set action. Geometrische Rand- und Eckbeiträge.','https://arxiv.org/abs/2501.00139')
]: add(p('<link href="'+url+'" color="#16756F">'+escape(text)+'</link>','small'))
add(p('Keine Neuheitsbehauptung für allgemeine Variations-, Unschärfe-, Poincaré- oder Coarea-Methoden. Die Anwendung prüft den versionierten Projektkandidaten. Alle acht physikalischen Gates bleiben HOLD.','small'))
def footer(c,doc):
    c.saveState();w,h=doc.pagesize
    c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49)
    c.setFont('DV',7.5);c.setFillColor(MUTED)
    c.drawString(60,34,'CST-DUST · Randpräparation v0.1 · 08.11.2026')
    c.drawRightString(w-60,34,f'{doc.page} / 6')
    c.restoreState()
def invariant_canvas(*a,**kw): kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Randpraeparation_Reaktionsbilanz_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: Randpräparation und Reaktionsbilanz v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)
