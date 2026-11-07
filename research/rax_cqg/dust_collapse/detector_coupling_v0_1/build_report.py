"""Render the human-readable report. Calculation/replay need only stdlib."""
from pathlib import Path
from fractions import Fraction as F
import json
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Detektorkopplung_Historienmischung_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
NAVY=colors.HexColor('#12354A');TEAL=colors.HexColor('#087E8B');PALE=colors.HexColor('#EDF5F7')
styles={
'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=23,leading=28,textColor=NAVY,spaceAfter=16),
'sub':ParagraphStyle('sub',fontName='DV',fontSize=10,leading=15,textColor=TEAL,spaceAfter=10),
'h1':ParagraphStyle('h1',fontName='DV-Bold',fontSize=15,leading=20,textColor=NAVY,spaceAfter=12),
'h2':ParagraphStyle('h2',fontName='DV-Bold',fontSize=11,leading=16,textColor=TEAL,spaceBefore=10,spaceAfter=6),
'body':ParagraphStyle('body',fontName='DV',fontSize=9.3,leading=14,spaceAfter=8),
'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.5,spaceAfter=6),
'formula':ParagraphStyle('formula',fontName='Mono',fontSize=8.1,leading=12,backColor=PALE,borderPadding=7,spaceBefore=4,spaceAfter=12),
'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.2,leading=11.5),
'head':ParagraphStyle('head',fontName='DV-Bold',fontSize=8.2,leading=11.5,textColor=colors.white)}
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

p('CST-DUST<br/>Detektorkopplung und<br/>notwendige Historienmischung','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Eine Kopplung, die klassische Historienrecords nur ausliest und nicht mischt, erzeugt den geforderten kohärenten Rückkehrdetektor nicht. Ihr universeller Effektfehler beträgt im erklärten Referenzraum mindestens 1/2 in Operatornorm. Diese Grenze ist scharf.')
table(['Prüffrage','Entscheidung'],[
('Kopplung ohne Mischung der Historien','Als universeller Rückkehrdetektor mit Fehler unter 1/2 ausgeschlossen.'),
('Mehr Hilfssystempulse oder Rückkopplung','Beseitigen die Grenze innerhalb derselben Klasse nicht.'),
('Zusätzlicher historienmischender Term','Notwendig; seine integrierte Operatornorm muss eine untere Schranke erfüllen.'),
('Richtiger Zweimodentest','Genügt nicht: Auf zusätzlichen Modi kann der vollständige Effekt trotzdem falsch sein.')],[180,325])
h('Was damit erreicht ist')
p('Eine konkret erklärte Kandidatenklasse scheidet mit Beweis aus. Für den nächsten Kandidaten gibt es eine quantitative Mindestanforderung und einen Test gegen Fehler außerhalb des untersuchten Unterraums. Die Prüfung benötigt keine großen Feldintegrale.')
h('Reichweite')
p('<b>Kein allgemeines Verbot lokaler Kopplungen oder von CST.</b> Diagonalität im Historienraum ist nicht dasselbe wie räumliche Lokalität. Die physikalische Zulässigkeit des Referenzraums und die gesuchte Materie-/Detektordynamik bleiben offen. Der endliche Mischkontrollfall ist keine physikalische Herleitung.')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein n=5-Produktionslauf, keine kostenpflichtige Rechenleistung und keine neu behauptete Detektorrealisierung.','small')
p('Basis: Main nach PR 261, Commit 7398a19f90e0c3736e2041b7f1480fc9223bbf9e. Vollständige Beweise, vier gepinnte Quellen und Reproduktionscode liegen im Prüfpaket.','small')

page('1 · Die konkret geprüfte Kopplung')
p('Im erklärten Raum H=L²(Ω,ν) sind klassische Recordfunktionen Multiplikationsoperatoren M_f. Das Detektorhilfssystem startet in einem festen, vom unbekannten Eingang ρ unabhängigen Zustand σ. Die Auslese F wirkt nur auf das Hilfssystem.')
f('(WΨ)(Y) = U(Y)Ψ(Y),       U(Y)†U(Y) = I\nAnfang: ρ ⊗ σ              Auslese: I ⊗ F')
p('Bei jedem Record Y wird nur das Hilfssystem verändert. Eine konkrete Hamiltonklasse lautet:')
f('H_d(t) = M_g(t) ⊗ I + I ⊗ H_A(t)\n         + Σ_r λ_r(t) M_F_r ⊗ B_r(t)')
p('Die Hilfssystemoperatoren dürfen untereinander nicht kommutieren. Die gesamte Entwicklung bleibt dennoch nach Historien zerlegt, solange kein zusätzlicher Term Historien mischt. In einem begrenzten Elementzahl-/Uhrsektor kann etwa die vorhandene Materiewirkung als beschränkte Recordfunktion verwendet werden.')
h('Der erzeugte Effekt bleibt diagonal')
f('E = M_e\ne(Y) = Tr[σ U(Y)† F U(Y)],       0 ≤ e(Y) ≤ 1')
p('Die Formel folgt direkt aus der gemeinsamen Born-Regel. Sie gilt auch für gemischte Hilfssystemzustände. Für den festen Effekt gilt [E,exp(iS)]=0: Eine allein im System eingeprägte diagonale Wirkungsphase verändert seine Ausgänge nicht.')
h('Warum Wiederholung und Postselektion nicht helfen')
p('Die Krausoperatoren sind Multiplikationen. Produkte auf jedem rückgekoppelten Ergebniszweig und Summen akzeptierter Zweige bleiben diagonal. Aus einem Zustand ohne Kohärenz zwischen Nullatom und kontinuierlichem Anteil entsteht auch bei erfolgreicher Konditionierung keine solche Kreuzkohärenz.')
p('Die Kopplungszeit ist hier ein deklarierter Kontrollparameter. Ihre Identifikation mit einer physikalischen CST-Uhr wird nicht hergeleitet. Bereits korrelierte System-/Detektoranfangsdaten oder eine veränderte Apparatur im Phasenscan sind andere Voraussetzungen.','small')

page('2 · Eine scharfe Grenze von 1/2')
p('Im n=1-Referenzmodell haben Nullatom und kontinuierlicher Dichteanteil je Gewicht 1/2. Ihre normierten Moden |a> und |c> sind orthogonal. Die beiden Zustände besitzen dieselben vollständigen klassischen Recordwahrscheinlichkeiten:')
f('|ψ_±> = (|a> ± |c>)/√2\nP_+ = |ψ_+><ψ_+|')
table(['Auslese','Eingang ψ₊','Eingang ψ₋'],[
('Beliebiger diagonaler Effekt M_e','q','q'),
('Gewünschter Rückkehrprojektor P₊','1','0')],[305,100,100])
p('Die beiden Erwartungswerte liefern bereits die universelle Operatornorm-Untergrenze:')
f('||M_e − P_+|| ≥ max{1−q, q} ≥ 1/2\ninf_(0≤e≤1) ||M_e − P_+|| = 1/2')
p('Die Grenze wird von E=I/2 erreicht, denn (I/2−P₊)²=I/4. Sie ist daher scharf. Ein korrekt gemeinsam transportiertes Maß, Ziel und Zustand ändern den Abstand nicht.')
h('Was die Zahl bedeutet')
p('1/2 ist ein <b>universeller Fehler des Messeffekts in Operatornorm</b>. Es ist kein gemessener Prozentfehler einer ausgewählten Wahrscheinlichkeit. Ein Detektor kann für einen einzelnen bekannten Eingang dieselbe Zahl liefern, ohne denselben Effekt für andere Eingänge zu implementieren.')
p('Die Aussage setzt beide Testzustände im Vergleichsraum voraus. Falls spätere physikalische Constraints diesen Raum einschränken, muss der Nachweis dort erneut geführt werden. Andere Protokolle zur Schätzung von Phasenmittelwerten werden nicht allgemein ausgeschlossen.')
h('Auch die Präparation bleibt eingeschränkt')
p('Aus einem bezüglich Atom und kontinuierlichem Anteil blockdiagonalen Anfangszustand kann diese Instrumentklasse keinen Zielzustand mit Fidelität über 1/2 zu ψ₊ herstellen. Die Grenze gilt auf jedem nichtleeren konditionierten Zweig. Vorhandene Eingangskohärenz wird dadurch nicht ausgeschlossen.','small')

page('3 · Mindestanforderung an einen Mischterm')
p('Erweitere die Kopplung zu H(t)=H_d(t)+V(t), bei derselben Hilfssystempräparation und Auslese. Für diese Abschätzung sind die Generatoren beschränkt, selbstadjungiert, stückweise normstetig und normintegrierbar.')
f('γ = (1/hbar) ∫₀ᵀ ||V(t)|| dt\n||E − E_d|| ≤ γ\nτ := ||E − P_+|| ≥ max{0, 1/2 − γ}')
p('Beweisidee: Im Vergleichsbild hat die zeitliche Änderung des zurückgezogenen Effekts die Form i[V,B_d]/ℏ. Aus 0≤B_d≤I folgt ||[V,B_d]||≤||V||. Integration und die normkontraktive Hilfssystemerwartung ergeben ||E−E_d||≤γ. Die Dreiecksungleichung liefert anschließend die Zielschranke.')
table(['Gewünschter Effektfehler τ höchstens','Notwendiges γ mindestens'],[
('0','1/2'),('1/100','49/100'),('1/10','2/5'),('1/4','1/4'),('1/2','0')],[305,200])
h('Notwendig ist nicht hinreichend')
p('Ein Kandidat mit zu kleinem γ kann den geforderten Effekt unter diesen Bedingungen nicht liefern. Ein ausreichend großes γ beweist dagegen noch keine geeignete Kopplung. Die Schranke ist nicht als optimaler Quantum-Speed-Limit-Satz behauptet.')
p('γ ist eine dimensionslose integrierte Operatornorm, kein Preis und keine Rechnerzeit. Die Tabelle enthält mathematische Anforderungen, keine gemessenen Kopplungsstärken. Die Zerlegung in H_d und V muss offengelegt werden.')
p('Unbeschränkte Feldgeneratoren oder andere Anfangskorrelationen sind ohne zusätzliche Definitionsbereichs- und Propagatornachweise nicht automatisch von dieser Hamiltonabschätzung erfasst.','small')

page('4 · Mischkontrolle und ungeprüfte Zusatzmodi')
p('In einem ausschließlich zweidimensionalen Kontrollraum kann man zuerst die Historienmoden drehen und danach den Record a messen:')
f('R(θ) = [[cos θ, sin θ], [−sin θ, cos θ]]\nE_θ = R(θ)† P_a R(θ)\nθ = π/4  ⇒  E_θ = P_+')
p('Ein Generator V=−ℏθ σ_y/T erzeugt diese Rotation. Seine integrierte Norm ist γ=π/4. Er mischt die Historien ausdrücklich und verlässt die ausgeschlossene Klasse. Sechs rationale Rotationen kontrollieren die Fehlerformeln; der ideale Fall wird algebraisch ohne Gleitkommarundung geprüft.')
p('<b>Das ist ein algebraischer Kontrollfall, kein aus CST hergeleiteter Wechselwirkungsterm.</b> Seine physikalische Zulässigkeit, kausale Unterstützung und Einbettung in den vollständigen Raum bleiben offen.')
h('Ein perfekter Testblock kann täuschen')
f('E_falsch = P_+ ⊕ 1\nE_ziel   = P_+ ⊕ 0')
table(['Vergleich','Abweichung'],[
('Nur die ersten beiden Testmoden','0'),
('Eingang im zusätzlichen dritten Modus','Erfolg 1 statt 0'),
('Vollständiger Operatornormfehler','1')],[335,170])
p('Im kontinuierlichen Modell ist die Recordmessung auf w=0 nicht dasselbe wie der Rang-eins-Projektor auf die einzelne konstante Atommode: Sie akzeptiert zusätzliche Uhrmoden. Eine Drehung allein des Testblocks beseitigt diese unerwünschten Erfolge nicht.')
h('Konsequenz für den nächsten Kandidaten')
p('Eine behauptete Rückkehrmessung muss den vollständigen Effekt samt orthogonalem Komplement und Ausfallausgang kontrollieren. Richtige Matrixelemente auf wenigen ausgewählten Zuständen genügen dafür nicht.')

page('5 · Evidenz und nächste physikalische Aufgabe')
table(['Kontrolle','Ergebnis'],[
('Gemeinsame Zweipuls-Unitaritäten','75 exakt geprüft'),
('Reduzierte Effekte und gemeinsame Born-Regel','900 exakte Fälle'),
('Rückgekoppelte Instrumente','25 Instrumente, 100 Zweige'),
('Nichtleere konditionierte Zustände','81 ohne erzeugte Kreuzkohärenz'),
('Scharfe diagonale Grenze','25 Fälle und exakte Erreichbarkeit'),
('Darstellung / Mischung / Einbettung','3 gewichtete, 6 rationale und 2 Sonderkontrollen'),
('Negativkontrollen / Nachrechnung','7 zurückgewiesen; 4 Dateien bytegleich')],[305,200])
p('Die allgemeinen Sätze beruhen auf den vollständigen Beweisen. Die kleinen Matrizen kontrollieren die Implementierung; sie sind keine kontinuierliche CST-Quadratur, externe Replikation oder formale Beweisassistentenprüfung.','small')
h('Reproduktion')
f('python3 -B verify_package.py\npython3 -B replay.py')
p('Python-Standardbibliothek genügt. DERIVATION.md enthält die Beweise, coupling_contract.json die exakte Kandidatenentscheidung und die verbleibenden Anforderungen.','small')
h('Der nächste Kandidat muss mehr liefern')
p('<b>Ein aus Materie-/Randdynamik begründeter Mischterm V muss angegeben werden.</b> Danach sind Zustandsdomäne, Symmetrien, Kausalität, vollständiger Effekt und Nachmesskanal zu prüfen. Für gravitative Aussagen kommt die Rückwirkung hinzu. Das bloße Einsetzen des gewünschten Projektors als Kopplung wäre keine solche Herleitung.')
p('Alle acht physikalischen Gates bleiben HOLD. Die recorderhaltende Klasse ist für das erklärte Ziel ausgeschieden; andere Quantenkopplungen bleiben offen. Kein großer Rechenlauf wurde gestartet.','small')
h('Quellen und Einordnung')
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/261" color="#087E8B">Projektbasis PR 261</link>; <link href="https://www.preskill.caltech.edu/ph219/chap3_15.pdf" color="#087E8B">Preskill, Quantum Information, Kapitel 3</link>. Feldtheoretische Vergleichspfade: <link href="https://arxiv.org/abs/1605.03973" color="#087E8B">Belenchia et al., Detektorantwort nichtlokaler Feldtheorien</link> und <link href="https://arxiv.org/abs/1411.6513" color="#087E8B">Skalarfeldtheorie aus Kausalsets</link>. Eine Abbildung dieser Feldmodelle auf den hier geforderten Historienprojektor wurde nicht hergeleitet.','small')

def footer(c,doc):
    c.saveState();c.setStrokeColor(TEAL);c.setLineWidth(.6);c.line(45,42,550,42)
    c.setFont('DV',7.5);c.setFillColor(NAVY)
    c.drawString(45,29,'CST-DUST · Detektorkopplung / Historienmischung · v0.1')
    c.drawRightString(550,29,str(doc.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=45,
    topMargin=43,bottomMargin=55,title='CST-DUST Detektorkopplung und notwendige Historienmischung v0.1',
    author='Thomas Gfeller - Forschungsunterlagen',subject='Eingeschränkte Kopplungsklasse und notwendige Mischressource')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)

