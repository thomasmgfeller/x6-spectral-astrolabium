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
OUT=ROOT/'CST_DUST_Massabhaengigkeit_Zustandstransport_v0_1.pdf'
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

p('CST-DUST<br/>Maßabhängigkeit und<br/>Zustandstransport','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Gleicher Nullanteil, Mittelwert und gleiche Varianz legen die kohärente Referenzauslese nicht eindeutig fest. Ein bloßer Maßwechsel erzeugt jedoch keine neue Physik, wenn Zustand und Auslese passend mittransformiert werden.')
table(['Vergleich','Gesichertes Ergebnis'],[
('Konstante Randvektoren bei verändertem Maß','Acht Gegenvergleiche im bedingten Ein-Element-Kanal sind mit exakten rationalen Intervallen von null getrennt.'),
('Beide Randvektoren mit dem Maß transportiert','Die betrachteten Matrixelemente bleiben für jede endliche Elementzahl exakt unverändert.'),
('Physikalische Deutung','Die Auswahl von Maß, Präparation und Auslese muss gemeinsam und unabhängig von der Darstellung begründet werden.')],[154,351])
h('Was unverändert bleibt')
p('Uhrmaß, geankerte Kausalordnungen, Wirkung, Kopplungen, α-Gewichte und die Ausleseformel bleiben im ersten Vergleich fest. Alle Materiemaße sind positiv und normiert, haben einen Nullanteil von 1/2, Mittelwert 1/4 und Varianz 5/48. Auch die ersten beiden Momente der Materiewirkung stimmen überein.')
h('Was daraus nicht folgt')
p('Das sind festgelegte mathematische Vergleichsbedingungen. Sie beweisen weder gleiche klassische Dynamik noch die physikalische Zulässigkeit aller verglichenen Zustände. Der Darstellungssatz ist keine Herleitung einer unitären CST-Zeitentwicklung.')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung. Der veröffentlichte Community-Auftrag behält seinen ursprünglichen Referenzfall ν₀.')
p('Basis: Main nach PR 258, Commit 3177458a7f8545f845054e235cd3dcd7e829eff3. Vollständige Herleitung, Quellprovenienz, exakte Brüche und Reproduktionscode liegen im begleitenden Prüfpaket.','small')

page('1 · Eine positive Familie mit denselben Momenten')
p('Wir variieren ausschließlich das an allen neuen Elementen gleiche, unabhängige Dichtemaß. Die Referenz ist θ = 0. Für -1 ≤ θ ≤ 1 gilt:')
f('q(w) = 20 w³ - 30 w² + 12 w - 1\nνθ = 1/2 δ₀ + 1/2 [1 + θ q(w)] dw,  0 < w < 1')
p('Die Polynomidentitäten liefern einen vollständigen Positivitätsbeweis auf [0,1]:')
f('q(w) + 1 = 2w [10(w - 3/4)² + 3/8]\n1 - q(w) = 2(1-w) [10(w - 1/4)² + 3/8]')
p('Beide rechten Seiten sind nichtnegativ und im Innern positiv. Also |q| ≤ 1, im Innern sogar |q| &lt; 1. Damit sind alle Dichten der Familie nichtnegativ. Der diskrete Nullanteil bleibt exakt 1/2.')
p('Für jedes ganze k ≥ 0 ergibt direkte Integration die Identität:')
f('I_k = ∫₀¹ w^k q(w) dw\n    = k(k-1)(k-2) / [(k+1)(k+2)(k+3)(k+4)]')
table(['Größe','Wert für alle θ'],[('Normierung m₀','1'),('Mittelwert m₁','1/4'),('Zweites Moment m₂','1/6'),('Varianz m₂ - m₁²','5/48'),('Drittes / viertes Moment','m₃(θ)-m₃(0) = θ/280; m₄(θ)-m₄(0) = θ/140')],[177,328])
h('Konsequenz für beliebige endliche Kausalsets')
p('Bei festen Uhren und fester Geometrie ist S_d = -Σ w_j a_j. Unabhängige Dichtevariablen liefern:')
f('Eθ[S_d] = -m₁ Σ a_j\nEθ[S_d²] = m₂ Σ a_j² + 2m₁² Σ_(i<j) a_i a_j')
p('Beide Ausdrücke sind θ-unabhängig, auch nach dem unveränderten Uhrintegral. Normierte Dichtemaße erhalten außerdem die Sektornormmassen c_n und damit die zuvor bewiesenen Normrestschranken. Die ersten beiden Momente sind noch keine klassische Bewegungsgleichung.')

page('2 · Gegenvergleich ohne Feldquadratur')
p('Ein neues Element genügt. Mit x gleichverteilt auf [0,1] ist a(x) = 1/2 + 4h²x² und U = w a(x). Die konstante Randvorschrift hat Amplitude Aθ = E exp(-iμU) und Sichtbarkeit Vθ = |Aθ|². Gemeint ist der <b>bedingte n=1-Kanal</b>.')
f('M_k(h) = E[a^k]\n       = Σ_(j=0..k) binom(k,j)(1/2)^(k-j)(4h²)^j/(2j+1)\nEθ[U^k] = m_k(θ) M_k(h)')
p('Der erste Unterschied der Amplituden tritt bei Ordnung μ³ auf. Für die Sichtbarkeit folgt:')
f('Vθ - V₀ = θ μ⁴ [2M₄ - M₁M₃]/3360 + O(μ⁶)')
p('Der Koeffizient ist positiv: 2 Cov(a,a³) = E[(a-a′)(a³-a′³)] ≥ 0 für eine unabhängige Kopie a′. Daher M₄ ≥ M₁M₃ und 2M₄ - M₁M₃ ≥ M₄ &gt; 0.')
h('Einschluss bei den vorher festgelegten Parameterwerten')
p('Für eine unabhängige Kopie U′ gilt Vθ = E cos[μ(U-U′)]. Alle geraden Differenzmomente sind rationale Summen der bekannten U-Momente. Weil 0 ≤ U ≤ a_max = 1/2 + 4h², ist der Kosinusrest nach Grad 24 höchstens (|μ|a_max)²⁶/26!.')
table(['h','μ','V(+1) - V(0), ungefähr','V(-1) - V(0), ungefähr'],[
('1/4','1/4','+1.55596214 × 10⁻⁷','-1.55588700 × 10⁻⁷'),
('1/4','1','+3.90460795 × 10⁻⁵','-3.90156528 × 10⁻⁵'),
('1/2','1/4','+1.35418804 × 10⁻⁶','-1.35407273 × 10⁻⁶'),
('1/2','1','+3.22433506 × 10⁻⁴','-3.21985807 × 10⁻⁴')],[45,45,207,208])
p('Alle acht Differenzintervalle schließen null aus. Ihre maximale Breite ist kleiner als 3.757 × 10⁻²². Dies ist eine mathematische Einschließungsbreite, keine experimentelle Messunsicherheit. Ein separater Amplituden-Taylorrest sowie die exakte Koeffizientenfaltung A·conj(A) kontrollieren die Rechnung.')
p('Die konstante Randvorschrift ist damit unter den erklärten Momentbedingungen nicht invariant. Ob sie bei verändertem Maß denselben physikalischen Zustand bezeichnet, ist eine eigene Frage - sie wird auf der nächsten Seite getrennt geprüft.')

page('3 · Maßwechsel oder anderer Zustand?')
p('Alle νθ sind zueinander äquivalent. Ihre Dichte relativ zu ν₀ ist am <b>Atom w=0 gleich 1</b>; im kontinuierlichen Innern ist sie rθ(w)=1+θq(w)&gt;0. Die kontinuierliche Randformel darf nicht an die Stelle des atomaren Verhältnisses gesetzt werden.')
f('Uθ : L²(νθ) → L²(ν₀),   f → √rθ f\n||Uθ f||²_ν₀ = ∫ rθ |f|² dν₀ = ||f||²_νθ')
p('Die Abbildung ist surjektiv: Zu jedem g in L²(ν₀) gehört f=g/√rθ in L²(νθ). Damit ist Uθ unitär zwischen den beiden gewichteten Räumen. Das gilt auch für θ=±1: Mögliche Nullstellen der kontinuierlichen Dichte am Rand sind Lebesgue-Nullmengen, und das Atom bleibt erhalten.')
h('Zwei verschiedene Vergleiche')
table(['Vorschrift in νθ','Im gemeinsamen ν₀-Raum','Bedeutung'],[
('Beide Randvektoren sind konstant 1','Beide werden √rθ','Präparation und Auslese ändern sich.'),
('Beide Randvektoren sind rθ^(-1/2)','Beide werden konstant 1','Derselbe Zustand und dieselbe Auslese werden transportiert.')],[155,160,190])
p('Die Wirkung in der hier betrachteten Amplitude ist Multiplikation mit exp(iS). Sie kommutiert mit dem Dichtefaktor. Für n Elemente mit Rθ = Π rθ(w_j) folgt deshalb unmittelbar:')
f('<Rθ^(-1/2), exp(iS) Rθ^(-1/2)>_νθ^n\n    = ∫ exp(iS) dν₀^n')
p('Beide Randvektoren sind normiert. Die Gleichheit gilt für jede endliche Elementzahl. Unter der vorhandenen absolut konvergenten Sektormajorante gilt sie auch nach der Zahlensumme. Es ist dafür kein n=5-Rechenlauf nötig.')
p('<b>Interpretation:</b> Der Gegenvergleich von Seite 3 kann vollständig als Änderung der Referenzpräparation und Auslese im selben Hilbertraum dargestellt werden. Er beweist keine physikalische Ungleichwertigkeit nach korrektem Zustandstransport.')
p('Diese Ergänzung wurde nach Einfrieren des ursprünglichen Plans und Start der Rechnung aufgenommen. Sie ist in supplement.json offengelegt; Parameter und Fehlerordnung wurden nicht verändert. Der Beweis ist ein Darstellungssatz, keine Herleitung unitärer CST-Zeitentwicklung.','small')

page('4 · Änderungsschranken für die Referenzvorschrift')
p('Auch für größere endliche Kausalsets lässt sich die Änderung ohne neue Feldintegrale begrenzen. Da die Perturbation die Momente bis Grad zwei erhält, verschwinden die entsprechenden Taylor-Terme der charakteristischen Funktion χθ(t).')
f('|χθ(t)-χη(t)| ≤ |θ-η| |t|³/48\n|χθ(t)-χη(t)| ≤ |θ-η|/2')
p('Die erste Grenze folgt aus |q|≤1 und dem Taylor-Rest |t w|³/6 unter dem Faktor 1/2 des kontinuierlichen Maßes. Die zweite ist eine Totalvariationsgrenze. Mit |χθ|≤1 liefert die teleskopierende Produktdifferenz:')
f('|A_(p,θ)-A_(p,η)| ≤ D_p\nD_p = min(2, n|θ-η|/2,\n          |θ-η||μ|³ Σ_j E|a_j|³/48)')
p('Für n≤4 werden die Bereiche der a_j durch rationale Bernstein-Koeffizienten begrenzt. Bei festem Vorzeichen ist E|a_j|³ ein exaktes Polynom-Moment; sonst verwenden wir sup|a_j|·E a_j². Das sind kleine algebraische Rechnungen. Die Mittelung über Geometrien liefert D_n, der Sichtbarkeitsunterschied höchstens min(1,2D_n).')
h('Kontrollierter Übergang zur unbegrenzten Zahlensumme')
p('R=c₅+c₆+Δ₆ begrenzt die unbekannten Phasensektoren; Zmax=Z₄+R. Mit D₀=0 und K_v=Σ_(n≤4)c_n min(1,2D_n) folgen:')
f('|ΔP_count| ≤ (K_v + R)/Zmax\n|ΔP_coh| ≤ min(1, 2[Σ_(n≤4)c_n D_n + 2R]/Zmax)')
p('Die Monotonie in der unbekannten Restnorm ist zulässig, weil K_v≤Z₄ beziehungsweise Σc_nD_n≤2Z₄. Normmassen und Normrestschranke bleiben beim normierten Dichtewechsel erhalten.')
table(['h','α','|ΔP_count| höchstens','|ΔP_coh| höchstens'],[
('1/4','1','0.003357','0.003364'),('1/4','2','0.002280','0.002280'),
('1/2','1','0.098477','0.121626'),('1/2','2','0.052303','0.056020')],[45,45,207,208])
p('Tabelle: μ=1, |θ-η|=1, beliebige unveränderte Gravitationskopplung g; Dezimalwerte nach oben gerundet. Das sind konservative Obergrenzen für konstante Randvektoren, keine gemessenen Änderungen der unbegrenzten Kanäle. Für den mittransportierten Vergleich auf Seite 4 gilt exakt ΔP=0.','small')

page('5 · Evidenz, Grenzen und nächster Engpass')
table(['Kontrolle','Ergebnis'],[
('Momentformeln','33 exakte Identitäten'),('Ein-Element-Auslese','12 Fälle; 8 von null getrennte Gegenvergleiche'),
('Vollwirkung und Inkremente','100 exakte Kontrollen'),('Momentvergleich / geometrische Budgets','Je 100 Geometrie-/Uhrfälle'),
('Unbegrenzte Änderungsschranken','8 Parametersätze'),('Negative Kontrollen','6 Fehlerfälle zurückgewiesen'),
('Darstellungstransport','175 polynomiale und 245 Produktkontrollen'),('Isolierte Nachrechnung','6 Ergebnisdateien bytegleich reproduziert')],[218,287])
p('Die allgemeinen Sätze werden durch die angegebenen algebraischen Beweise getragen. Endliche Kontrollen prüfen ihre Implementierung. Die Nachrechnung verwendet dieselbe Implementierung; sie ist keine externe Replikation und keine formale Beweisassistenzprüfung.')
h('Reproduktion')
f('python3 -B analyze.py\npython3 -B transport_controls.py\npython3 -B replay.py\npython3 -B verify_package.py')
p('Die wissenschaftlichen Rechnungen benötigen nur die Python-Standardbibliothek. Der Berichtserzeuger benötigt zusätzlich ReportLab. Der Hauptplan blieb unverändert; die Interpretationsergänzung ist separat dokumentiert. Quellbytes, Ergebnisse und Bericht sind im Prüfpaket mit SHA-256-Prüfsummen enthalten.')
h('Nächster wissenschaftlicher Schritt')
p('<b>Präparation und Messauslese operational und unabhängig von der Maßdarstellung festlegen.</b> Danach ist zu prüfen, welche zusätzliche physikalische Bedingung die untersuchte Zustandsfreiheit einschränkt. Die bloße Forderung gleicher erster zwei Materiemomente reicht dafür nicht.')
p('MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION bleiben HOLD. Keine Aussage über vollständige 4D-CST-Dynamik, Rückwirkung, einen geschlossenen Innen-/Außenraum-Anschluss oder einen Bounce wird hochgestuft.')
h('Quellen und vollständige Beweise')
p('Projektbasis: <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/258" color="#087E8B">GitHub PR 258</link>. Die byteidentischen Eingangsmodule sind in provenance.json dokumentiert. Modellbezogene Herleitungen: DERIVATION.md im Prüfpaket.','small')
p('Einordnung der Legendre-Polynome: <link href="https://dlmf.nist.gov/18.3" color="#087E8B">NIST DLMF 18.3</link> und <link href="https://dlmf.nist.gov/18.5" color="#087E8B">18.5</link>. Die konkret benötigten Polynom-, Positivitäts-, Moment- und Transportidentitäten sind im vorliegenden Paket unmittelbar hergeleitet.','small')

def footer(c,doc):
    c.saveState();c.setStrokeColor(TEAL);c.setLineWidth(.6);c.line(45,42,550,42)
    c.setFont('DV',7.5);c.setFillColor(NAVY)
    c.drawString(45,29,'CST-DUST · Maßabhängigkeit / Zustandstransport · v0.1')
    c.drawRightString(550,29,str(doc.page));c.restoreState()

doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=45,
    topMargin=43,bottomMargin=55,title='CST-DUST Maßabhängigkeit und Zustandstransport v0.1',
    author='Thomas Gfeller - Forschungsunterlagen',subject='Analytischer Vergleich im erklärten Referenzmodell')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
