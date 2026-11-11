"""Build the review PDF from explicit mathematical content. No network."""
from pathlib import Path
import re
from io import BytesIO
import tempfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties,findfont
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Mischblock_v0_1.pdf'
NAVY=colors.HexColor('#18334C'); TEAL=colors.HexColor('#087E8B')
pdfmetrics.registerFont(TTFont('DejaVu',findfont(FontProperties(family='DejaVu Sans'))))
pdfmetrics.registerFont(TTFont('DejaVuBold',findfont(FontProperties(family='DejaVu Sans',weight='bold'))))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold',italic='DejaVu',boldItalic='DejaVuBold')
BODY=ParagraphStyle('body',fontName='DejaVu',fontSize=9.6,leading=14,spaceAfter=8,textColor=NAVY)
SMALL=ParagraphStyle('small',parent=BODY,fontSize=8,leading=11,spaceAfter=6)
H1=ParagraphStyle('title',parent=BODY,fontName='DejaVuBold',fontSize=24,leading=29,spaceAfter=15)
H2=ParagraphStyle('section',parent=BODY,fontName='DejaVuBold',fontSize=16,leading=21,spaceAfter=13)
H3=ParagraphStyle('sub',parent=BODY,fontName='DejaVuBold',fontSize=11,leading=15,spaceBefore=10,spaceAfter=7)
KICK=ParagraphStyle('kick',parent=SMALL,textColor=TEAL,fontName='DejaVuBold',spaceAfter=12)
story=[]
def p(text,style=BODY): story.append(Paragraph(text,style))
def eq(tex,maxwidth=164*mm):
    tex=re.sub(r'\\sqrt\s+([A-Za-z])',lambda m:r'\sqrt{'+m[1]+'}',tex)
    tex=re.sub(r'\\frac\s+([A-Za-z])(\d)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',tex)
    tex=re.sub(r'\\(mathcal|mathbf|mathbb)\s*([A-Za-z0-9])',lambda m:'\\'+m[1]+'{'+m[2]+'}',tex)
    tex=re.sub(r'\\frac(\\[A-Za-z]+)(\d)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',tex)
    tex=re.sub(r'\\frac(\d)(\d)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',tex)
    tex=re.sub(r'\\frac(\d)',lambda m:r'\frac{'+m[1]+'}',tex)
    tex=re.sub(r'\\sqrt(\d)',lambda m:r'\sqrt{'+m[1]+'}',tex)
    tex=re.sub(r'\\sqrt(\\[A-Za-z]+)',lambda m:r'\sqrt{'+m[1]+'}',tex)
    buf=BytesIO(); math_to_image('$'+tex+'$',buf,prop=FontProperties(size=14),dpi=220,format='png',color='#18334C')
    buf.seek(0); im=PILImage.open(buf); w,h=im.size; scale=min(72/220,maxwidth/w)
    obj=Image(buf,width=w*scale,height=h*scale); obj.hAlign='CENTER'
    story.extend([Spacer(1,4*mm),obj,Spacer(1,5*mm)])
def table(rows,widths,header=True):
    converted=[[Paragraph(str(x),SMALL) for x in row] for row in rows]
    t=Table(converted,colWidths=widths,hAlign='LEFT')
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.6,TEAL)]
    if header: commands.append(('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F3F4')))
    commands.append(('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7FA')]))
    t.setStyle(TableStyle(commands)); story.extend([t,Spacer(1,4*mm)])
def page(k,title):
    if story: story.append(PageBreak())
    p('CST-DUST  /  SCHRITT 4  /  '+k,KICK); p(title,H2)

page('ERGEBNIS','Ein belastbarer Nichtnullbefund')
p('Der erste paritätserlaubte Mischblock',H1)
p('Der Übergang vom Atomsektor zum kohärenten Positivsektor mit Materiepaket 0 → 0 ist im festgelegten endlichen AA-Versuch nicht null. Auch die aus der Wirkung definierte entkoppelte Referenz liefert einen Nichtnullwert.')
eq(r'\mathcal M_\lambda=\langle A,+,0_m|K_\lambda|A,0,0_m\rangle')
table([['Amplitudenwert','Realteil','Imaginärteil'],['Ursprüngliche Wirkung M₁','−0.155730245646','+0.132674294297'],['Entkoppelte Referenz M₀','+0.021300694129','−0.066660937892'],['Gepaarte Änderung Δ=M₁−M₀','−0.177030939775','+0.199335232189']],[68*mm,48*mm,48*mm])
p('<b>Fehler der angezeigten Zahlen: höchstens 10⁻¹² je Real- und Imaginärteil.</b> Die Grenze enthält die Tabellenrundung. Sie ist eine deterministische Einschließung; die Null liegt weit außerhalb.')
eq(r'|\mathcal M_1|>0.20458,\quad|\mathcal M_0|>0.06998,\quad|\Delta|>0.26659')
p('<b>Ursache getrennt bewertet:</b> Die untersuchte Geometrieabhängigkeit des zusätzlichen Skalarfelds ist für die Mischung nicht notwendig. Sie verändert die komplexe Amplitude aber nachweislich. Ein zusätzlicher zusammenhängender Amplitudenrest ist ebenfalls von null getrennt.')
p('33 Historien vollständig berücksichtigt; 27 Prüfungen bestanden. Normierungen, Gravitationsphasen, Gaußzweige und Quadraturfehler sind ausdrücklich bilanziert.',H3)
p('Geltungsbereich: explizites endliches Kontrollensemble mit festen Staubboxen und normierten Randpaketen. Historiengewichte und physikalischer CST-Kern sind nicht hergeleitet. Alle acht physikalischen Gates bleiben HOLD.',SMALL)

page('01','Der festgelegte Kontrollversuch')
p('Die Familie enthält alle 33 abgedeckten Ordnungen auf L={0,1}, I={2}, R={3,4}. Eingangs- und Ausgangsrand sind jeweils eine Zweierantichain. Historiengewichte, Parameter und Referenzwirkung wurden vor der numerischen Auswertung festgelegt.')
table([['Eingabe','Festlegung'],['Historienkoeffizienten','c_C=1/33 für jede gelabelte Ordnung'],['Gravitationsphase','exp(i F₄(C)); κ=1, keine Phasenentfernung'],['Zusätzliches Skalarfeld','μ=0; σ_s=σ_a=1'],['Maße und Skalen','unverändert aus Schritt 2; kompakte Staubstützen'],['Entkopplungsendpunkte','λ=1: Original; λ=0: feste mittlere Skalarwirkung'],['Primäre numerische Regel','40 Gaußknoten pro Uhrenachse; 128 Bit']],[66*mm,98*mm])
p('Die Randvertauschungen S₂(L)×S₂(R) ergeben zehn Orbits. Ihre Zusammenfassung ist exakt; es wird kein weiterer Symmetriefaktor hinzugefügt.')
table([['Ordnungscodes','Multiplizitäten','F₄-Werte'],['8476, 8592, 8600, 8604, 8732','4, 4, 4, 4, 4','10, 11, 10, 19, 10'],['8988, 9116, 24860, 25372, 25500','4, 2, 4, 2, 1','9, 18, 19, 18, 37']],[83*mm,40*mm,41*mm])
eq(r'\mathcal M_\lambda=\sum_{\mathrm{Orbits}\ C}\frac{m_C}{33}e^{iF_4(C)}D_CA_{C,\lambda}')
p('Die Gewichte 1/33 und κ=1 sind deklarierte Kontrollentscheidungen. Sie sind kein physikalisch hergeleitetes CST-Maß. Die primären Amplituden werden weder durch die Gravitationssumme Z geteilt noch nachträglich auf einen gemeinsamen Betrag normiert.',SMALL)

page('02','Normierte Zustände und sämtliche Maßfaktoren')
eq(r'd\lambda(t)=\frac12\mathbf1_{[-1,1]}dt,\qquad d\nu(r)=\frac12\delta_0+\frac12\mathbf1_{(0,1)}dr')
eq(r'd\mu_A=\frac12\prod_{j\in A}d\lambda(t_j)d\nu(r_j)dq_j')
p('Die dimensionslosen Variablen sind t=T/ℓ, r=w/ℏ und q=Φℓ/√ℏ. Jeder Rand besitzt den Quotientfaktor 1/2. Die zwei Grundpaketzustände sind bezüglich desselben Maßes normiert und kinematisch orthogonal.')
eq(r'\Psi_{s,0}=\sqrt2\,d_sh_0,\qquad h_0=\pi^{-1/2}e^{-(q_1^2+q_2^2)/2}')
eq(r'd_0=2\mathbf1_{00},\qquad d_+=\frac2{\sqrt3}(\mathbf1_{10}+\mathbf1_{01}+\mathbf1_{11})')
p('„+“ bedeutet mindestens eine positive Randdichte: 10, 01 und 11, kohärent mit gleichen positiven Amplituden. Es ist keine Mischung von Wahrscheinlichkeiten. Die zwei Eingangsdichten liegen am Atom; die innere Dichte besitzt Atom und Positivachse.')
eq(r'\frac14\cdot2\cdot2\cdot\frac2{\sqrt3}\cdot\frac1{32}=\frac1{16\sqrt3}')
p('Die Faktoren sind der Reihe nach: beide Randquotienten, die zwei √2-Paketfaktoren, d₀, d₊ und die fünf Atom/Positivgewichte. Es bleiben drei Ausgangsmasken mal zwei Innenmasken. Alle übrigen Masken werden durch das Eingangspaket auf null gesetzt.')
p('Die Rand-Skalarpakete liefern gemeinsam π⁻¹ exp(−|b|²/2). Dieser Faktor steht in der Gaußprojektion und wird nicht nochmals im Staubintegral verwendet. Uhren bleiben auch an Atomstellen erhalten.',SMALL)
p('Der berechnete Nichtnullwert ist ein Matrixelement eines Integraloperators zwischen orthogonalen Zuständen. Er ist kein unnormierter Paketüberlapp und keine bereits normalisierte Übergangswahrscheinlichkeit.',SMALL)

page('03','Entkopplung aus der Wirkung')
p('Im minimalen Kandidaten hängt der zusätzliche Skalarblock von der Historie C ab, nicht direkt von den Staubvariablen. Die direkte Staub-Skalar-Kopplung ist bereits null. Untersucht wird deshalb die Kopplung dieses Skalarfelds an die Historiengeometrie.')
eq(r'\overline{H}=\frac1{33}\sum_CH_C')
eq(r'S_{\Phi,\lambda}(C)=\frac12\Phi^T[\overline{H}+\lambda(H_C-\overline{H})]\Phi')
p('Bei λ=1 ist die ursprüngliche Wirkung wiederhergestellt. Bei λ=0 hat jede Historie dieselbe Skalarwirkung. Staubwirkung, Gravitationsphasen, Historiengewichte, Maße und Randpakete bleiben unverändert.')
p('Die feste Referenzmatrix M̄/β, mit M=F²H/ℏ und β=4/√6, lautet in der Reihenfolge 0,1,2,3,4:')
table([['28/11','0','10/33','−47/33','−47/33'],['0','28/11','10/33','−47/33','−47/33'],['10/33','10/33','−40/33','10/33','10/33'],['−47/33','−47/33','10/33','28/11','0'],['−47/33','−47/33','10/33','0','28/11']],[32.8*mm]*5,header=False)
eq(r'\overline{\alpha}=\frac{40}{33}\beta>0,\qquad\alpha_{C,\lambda}\geq\beta\quad(0\leq\lambda\leq1)')
p('Die Referenz behält eine nichttriviale kinetische Wirkung, die konstante Feldnullrichtung der masselosen Gesamtmatrix und eine positive innere Gaußlücke. Sie ist unter beiden Randvertauschungen invariant.')
p('<b>Die gesamte Skalarwirkung wird nicht auf null gesetzt.</b> Das würde den inneren Skalar integralbedingt ungedämpft lassen. Die hier definierte Referenz ist ein klarer Wirkungsvergleich; sie muss nicht dem Operator einer einzelnen Kausalordnung entsprechen und ist keine neue behauptete physikalische CST-Dynamik.',SMALL)

page('04','Gaußprojektion mit kontrollierter Phase')
p('Mit b=(q₀,q₁,q₃,q₄) und x=q₂ besitzt M die Blöcke B,Jᵀ,J,−α. Setze z=ε+iα. Das innere Skalarintegral liefert:')
eq(r'\int e^{-zx^2/2+i(Jb)x}dx=\frac{\sqrt{2\pi}}{\sqrt z}\exp\!\left[-\frac{(Jb)^2}{2z}\right]')
eq(r'Q_\epsilon=I-iB+\frac{J^TJ}{z}')
eq(r'A_{C,\lambda}(\epsilon)=\frac{4\pi\sqrt{2\pi}}{\sqrt z\prod_{j=1}^4\sqrt{d_j(\epsilon)}}')
p('d_j sind die komplexsymmetrischen Gauß-Eliminationspivots von Q. Sie liegen in der rechten Halbebene; jeder Wurzelzweig wird dort festgehalten. Im Abel-Grenzwert gilt 1/√(iα)=α^(-1/2) exp(−iπ/4). Die ganze Determinante wird nicht unbesehen unter eine einzelne Hauptwurzel gestellt.')
p('Die unabhängige Kontrolle verwendet die reellen Eigenwerte k_j von K=B+JᵀJ/α:')
eq(r'A=4\pi\sqrt{\frac{2\pi}{\alpha}}\prod_j(1+k_j^2)^{-1/4}\exp\!\left[-\frac{i\pi}{4}+\frac i2\sum_j\arctan k_j\right]')
p('Alle Gravitationsphasen exp(iF₄) werden danach unverändert mitgeführt. Die Referenzprojektion beträgt ungefähr A_ref=0.5073499675465727+1.6840996012876250 i. Ein Test mit K=10I₄ reproduziert das falsche Vorzeichen der naiven Determinanten-Hauptwurzel.',SMALL)
p('Parität als exakte Nullkontrolle',H3)
eq(r'\langle A,+,1_m|K_\lambda|A,0,0_m\rangle=0')
p('Die gemeinsame Feldumkehr lässt Wirkung und Maße invariant; eine einzelne h₁-Einfügung ist ungerade. Daher verschwindet dieser andere Übergang exakt an beiden Endpunkten. Der berechnete 0_m→0_m-Kanal ist gerade und paritätserlaubt.',SMALL)

page('05','Staubintegrale und analytische Quadraturgrenze')
eq(r'\kappa_x=\frac12+\frac\beta4\sum_{y\prec x}c_{xy}(t_x-t_y)^2,\qquad E_x=E(\kappa_x)')
eq(r'E(k)=e^{-ik/2}\,\mathrm{sinc}(k/2),\qquad E(0)=1')
eq(r'D_C=\frac1{16\sqrt3}\int d\lambda^5(t)(1+E_2)(E_3+E_4+E_3E_4)')
p('Damit sind sämtliche Dichteintegrale einschließlich ihrer Atome analytisch ausgeführt. Da die Ausgangspunkte unvergleichbar sind, können ihre Uhrsummen getrennt kontrahiert werden. Mit Fₓ=∫dλ(tₓ)Eₓ verbleibt die dreidimensionale äußere Summe (1+E₂)(F₃+F₄+F₃F₄). Dies ist dieselbe 5D-Tensorregel, nur effizient ausgewertet.')
p('Der Fehler wird aus Analytizität bewiesen. Für eine in der Bernsteinellipse mit Parameter ρ beschränkte Funktion, |f|≤M, ergeben die Chebyshevkoeffizienten und die Exaktheit bis Grad 2n−1:')
eq(r'|I(f)-Q_n(f)|\leq\frac{4M\rho^{-2n}}{1-\rho^{-1}}')
p('Mit Ellipsenhalbachsen a=(ρ+ρ⁻¹)/2, b=(ρ−ρ⁻¹)/2 und W_j als Summe der Beträge der inzidenten Paargewichte folgt nach Teleskopieren über fünf Achsen:')
eq(r'e_C(n)\leq\frac{\sqrt3}{2}\frac{\rho^{-2n}}{1-\rho^{-1}}\sum_{j=0}^4\exp\!\left[\frac\beta2b(a+1)W_j(C)\right]')
p('Eingesetzt werden ρ=2, a=5/4, b=3/4 und die je Historie exakt bestimmten W_j≤19. Die ganze Funktion E besitzt auch bei κ=0 keine Singularität. Der vollständige Beweis steht in DERIVATION.md.',SMALL)

page('06','Das vollständige numerische Fehlerbudget')
table([['Fehleranteil','M₁','M₀','Δ'],['Analytische Uhrquadratur; komplexer Betrag','&lt;1.723·10⁻¹³','&lt;2.861·10⁻¹³','&lt;2.602·10⁻¹³'],['Interne Arithmetik; komplexer Radius','&lt;8.13·10⁻³⁵','&lt;4.21·10⁻³⁵','&lt;1.02·10⁻³⁴'],['Dichtequadratur','0, analytisch','0, analytisch','0, analytisch'],['Abel-Extrapolation','0, analytisch','0, analytisch','0, analytisch'],['Auslassung innerhalb der 33er-Familie','0','0','0']],[65*mm,33*mm,33*mm,33*mm])
p('Arb/Acb schließt auch Knoten, Gewichte, Wurzeln, Phasen und Gaußpivots ein. Der analytische komplexe Quadraturfehler wird zu beiden Komponentenradien addiert. Die Dezimalexporte enthalten ihre Darstellungsrundung; die zwölfstelligen Werte auf Seite 1 werden auf 10⁻¹² je Komponente erweitert.')
eq(r'e_\Delta\leq\sum_C\frac1{33}|A_C-A_{\mathrm{ref}}|e_C')
p('Die Differenz wird mit denselben Staubquadraturdaten direkt gebildet. Ihr Fehler ist separat eingeschlossen; ein kleiner Unterschied zweier Quadraturregeln wird nicht als Fehlerbeweis verwendet.')
p('Unabhängige Kontrollen',H3)
p('<b>48 Knoten, 192 Bit:</b> Die Kontrollintervalle überlappen die primären Werte. Die analytischen Amplitudenfehler liegen dann unter 4.37·10⁻¹⁸. Der berichtete Hauptbefund verwendet weiterhin die vorab festgelegte 40er-Regel.')
p('<b>Direkte 5D-Implementierung:</b> Eine separate Float64-Rechnung mit acht Knoten integriert alle 33 gelabelten Historien ohne Orbitreduktion und ohne Uhrkontraktion. Sie stimmt mit der kontrahierten 8er-Regel überein; ihre Skalarphasen werden über Schur-Eigenwerte berechnet.',SMALL)
p('<b>Nicht beziffert:</b> physikalische Historienauswahl und Gewichtung, andere Maße oder Randpräparationen, unendliche CST-Summe und Kontinuumsfehler. Diese offenen Modellfragen sind keine Bestandteile der kleinen numerischen Fehlerbalken.',SMALL)

page('07','Was verursacht die Änderung der Amplitude?')
p('M₀≠0 zeigt: Die untersuchte zusätzliche Skalar-Geometrie-Kopplung ist für den Mischungszeugen nicht notwendig. Δ≠0 zeigt zugleich: Das Zuschalten der deklarierten Kopplung verändert den Zeugen. Diese beiden Aussagen sind miteinander vereinbar.')
p('Die Änderung enthält jedoch auch eine Verschiebung der mittleren Skalarantwort. Eine Gaußantwort auf die mittlere Wirkung ist im Allgemeinen nicht gleich der gemittelten Gaußantwort. Zur Trennung definieren wir rein diagnostisch:')
eq(r'p_C=\frac{e^{iF_4(C)}}{33},\quad Z=\sum_Cp_C,\quad d=\sum_Cp_CD_C,\quad\widetilde{A}=\frac{\sum_Cp_CA_C}{Z}')
eq(r'\Delta=\sum_Cp_CD_C(A_C-\widetilde{A})+d(\widetilde{A}-A_{\mathrm{ref}})')
table([['Beitrag','Realteil','Imaginärteil'],['Zusammenhängender Amplitudenrest','−0.080381634846','+0.002889997971'],['Änderung der mittleren Skalarantwort','−0.096649304929','+0.196445234218']],[68*mm,48*mm,48*mm])
p('Fehler je angezeigter Komponente: höchstens 2·10⁻¹². Beide Beiträge sind zertifiziert nicht null; ihre Summe stimmt mit dem gepaarten Δ überein. Z≈−0.072101781033−0.343279080577 i ist von null getrennt.')
p('<b>Diese Gewichte sind komplex und keine Wahrscheinlichkeiten.</b> Die diagnostische Division durch Z ändert die primären Amplituden nicht. Der zusammenhängende Rest ist ein endlicher Amplitudenbefund, kein allgemeiner Verschränkungsnachweis.')
p('Die direkte Staub-Skalar-Wechselwirkung fehlt an beiden Endpunkten. Sie kann hier deshalb nicht als Ursache identifiziert werden. Ein nichtdiagonaler Dichtekernel kann die orthogonalen Atom- und Positivpakete bereits ohne diese neue Kopplung verbinden.',SMALL)

page('08','Prüfbarkeit und verbleibende Physik')
table([['Frage','Ergebnis'],['Ist der paritätserlaubte Mischblock null?','Nein, zertifiziert nicht null'],['Verschwindet er bei der festgelegten Entkopplung?','Nein'],['Ändert die untersuchte Kopplung seine Amplitude?','Ja, gepaarte Differenz nicht null'],['Erklärt nur die mittlere Skalarantwort die Änderung?','Nein, zusätzlicher verbundener Rest nicht null'],['Ist damit physikalische Stauberzeugung bewiesen?','Nein'],['Physikalische CST-Matrix / alle acht Gates','NOT_CONSTRUCTED / HOLD']],[107*mm,57*mm])
p('<b>27 Prüfungen bestanden:</b> unabhängige Enumeration und Hesse-Matrizen, vollständige Gravitationsphasen, Orbitgewichte, Randnormierung, Masken, Entkopplungsendpunkte, Parität, Gaußzweige, exakte Gaußmomente, direkte 5D-Kontrolle, Intervallschranken und Darstellungsrundung.')
p('<b>Reproduktion:</b> python verify.py prüft alle Datei-Hashes und fünf Herkunfts-Blobs, wiederholt die primäre Ballrechnung und vergleicht die Ergebnisdateien bytegleich. Mit --extended wird zusätzlich die 48er-Kontrolle wiederholt. Python-FLINT 0.9.0 und NumPy 2.3.5 sind festgehalten. Das Prüfpaket enthält Code, Zwischenfaktoren, alle Orbitbeiträge und vollständige Herleitung.',SMALL)
p('Erstmals liegt für diesen deklarierten Kontrollpunkt ein normierter, phasenrichtiger und numerisch eingeschlossener Mischungszeuge vor. Der physikalische Kern K₀₊ bleibt NOT_COMPUTED. Geschlossene Evolution, Unitarität und Singularitätsauflösung folgen daraus nicht.',SMALL)
p('Herkunft und Quellen',H3)
p('Projektbasis: Main d2ad347fc6028e5a85f745e95fd5737e840e03a9; PR #279–281. Exakte Pfade und Blobwerte: provenance.json.',SMALL)
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/281" color="#087E8B">GitHub: endliche Amplitudenexistenz, PR #281</link><br/><link href="https://python-flint.readthedocs.io/en/latest/arb.html" color="#087E8B">Python-FLINT: Arb-Ballarithmetik und Gaußknoten</link><br/><link href="https://python-flint.readthedocs.io/en/latest/acb.html" color="#087E8B">Python-FLINT: komplexe Acb-Einschließungen und Wurzelzweige</link>',SMALL)

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(TEAL);canvas.setLineWidth(.6)
    canvas.line(23*mm,282*mm,187*mm,282*mm)
    canvas.setFont('DejaVu',8);canvas.setFillColor(NAVY)
    canvas.drawString(23*mm,286*mm,'CST-DUST  /  Paritätserlaubter Mischblock A → A  /  v0.1')
    canvas.drawString(23*mm,12*mm,'11. November 2026  |  Endlicher Kontrollversuch; physikalische Gates HOLD')
    canvas.drawRightString(187*mm,12*mm,str(doc.page));canvas.restoreState()

if __name__=='__main__':
    doc=SimpleDocTemplate(str(OUT),pagesize=(210*mm,297*mm),leftMargin=23*mm,rightMargin=23*mm,
                         topMargin=23*mm,bottomMargin=22*mm,title='CST-DUST Paritaetserlaubter Mischblock v0.1',author='X6 Forschungsprogramm / Arbeitsausarbeitung')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)

