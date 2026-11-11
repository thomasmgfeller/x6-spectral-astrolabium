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
OUT=ROOT/'CST_DUST_Amplitudenexistenz_v0_1.pdf'
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
    p('CST-DUST  /  SCHRITT 3  /  '+k,KICK); p(title,H2)

page('ERGEBNIS','Die vollständige endliche Amplitude existiert')
p('Staubintegration und Abel-Grenzwert',H1)
p('Für die 33 festgelegten A → A-Kontrollhistorien mit einem inneren Element ist die gemeinsame Integration einschließlich der Null­dichte-Atome abgesichert. Eine integrierbare Majorante erlaubt die Entfernung des inneren Skalarregulators.')
eq(r'\mathcal M(0)=\lim_{\epsilon\downarrow0}\mathcal M(\epsilon)')
table([['Geprüfter Punkt','Ergebnis'],['Staubintegrale mit Atom und Positivsektor','absolut integrierbar nach innerer Abel-Integration'],['Innerer Skalarblock der 33 Historien','gleichmäßige Lücke unabhängig von den Dichten'],['Regulatorentfernung','dominiert; absoluter Fehler höchstens O(ε)'],['Punktweises Nullraumkriterium allein','nicht ausreichend: explizite Divergenz'],['Automatisierte Kontrollen','22 bestanden']],[91*mm,73*mm])
p('Bei Einheitsbreiten gilt für alle 16 Einträge der primären Viererfamilie und jede nichtnegative Skalarmasse:')
eq(r'|\mathcal M_{ij}(\epsilon)|\leq11.770\,C_\nu,\qquad C_\nu=\sum_C|c_C|')
eq(r'|\mathcal M_{ij}(\epsilon)-\mathcal M_{ij}(0)|\leq9.489\,\epsilon C_\nu')
p('Die Konstanten sind nach oben gerundet. c_C sind feste endliche Historienkoeffizienten; ihre physikalische Auswahl bleibt offen. Die exakten Ausdrücke und der Beweis stehen auf den Folgeseiten und in DERIVATION.md.')
p('<b>Geltungsbereich:</b> endliche Historienfamilie, feste kompakte Uhr- und Dichteboxen, deklarierte volumen­gewichtete Skalarwirkung und normierte Randpakete. Kein Existenzbeweis der unendlichen physikalischen CST-Summe. Alle acht physikalischen Gates bleiben HOLD.',SMALL)

page('01','Maß, Zustände und vollständiges Integral')
p('L={0,1}, I={2}, R={3,4}. Die dimensionslosen Variablen sind t=T/ℓ, r=w/ℏ und q=Φℓ/√ℏ. Beide Ränder verwenden die normierten Pakete aus Schritt 2: Ψ_s,n=√2 d_s h_n mit n=0,1 und konstantem Uhrpaket auf der Box.')
eq(r'd\lambda=\frac12\mathbf1_{[-1,1]}dt,\qquad d\nu=\frac12\delta_0+\frac12\mathbf1_{(0,1)}dr')
eq(r'd\mu_A=\frac12\prod_{j\in A}d\lambda(t_j)d\nu(r_j)dq_j')
p('Die Dichtepakete sind d₀=2·1₀₀ und d₊=2(1₁₀+1₀₁+1₁₁)/√3. „+“ bedeutet mindestens eine positive Randdichte, kohärent mit gleicher Phase. Die Skalarpakete h₀ und h₁ sind die normierten symmetrischen Hermite-Gaußpakete aus Schritt 2. Ihre Breiten bleiben positiv und endlich.')
eq(r'\mathcal M_{s^{\prime}n^{\prime},sn}(\epsilon)=\sum_Cc_Ce^{iS_g(C)/\hbar}\int d\mu_Rd\mu_L\,\overline{\Psi}_{s^{\prime},n^{\prime}}\Psi_{s,n}\,K_{C,\epsilon}')
eq(r'K_{C,\epsilon}=\int d\lambda(t_2)d\nu(r_2)dq_2\,e^{-\epsilon q_2^2/2}e^{i(S_d+S_\Phi)/\hbar}')
p('Bei ε&gt;0 ist das vollständige Integral absolut integrierbar. Die Randpakete sind L1, das innere Feld ist gaußgedämpft und alle Staubmaße sind endlich. Die Summe enthält 33 feste Historien; Cν=Σ|c_C| ist endlich. Ein divergierender regulatorabhängiger Vorfaktor gehört nicht zum Vertrag.')
p('<b>Der Regulator ist unnormalisiert.</b> Bei ε=0 hat das ursprüngliche Integral über alle fünf Skalarvariablen keinen integrierbaren Absolutbetrag: das innere Feld besitzt dann keine reelle Dämpfung. Die Amplitude wird als Abel-Grenzwert definiert. Erst nach analytischer innerer Integration wird das verbleibende Integral absolut integrierbar.')
p('Eine beliebige Umordnung des vollständig unregulierten Integrals ist damit nicht gerechtfertigt. Uhr- und Dichteboxen werden in diesem Grenzwert nicht entfernt.',SMALL)

page('02','Die innere Lücke bleibt bei Dichte null offen')
p('Die minimale Skalarwirkung ist volumen­gewichtet und hängt nicht direkt von den Staubvariablen T,w ab. Sie bleibt daher am Dichteatom dieselbe. Die dimensionslose Wirkungsmatrix ist M_C=F²H_C/ℏ mit F=√ℏ/ℓ. Ihre Blöcke sind B_C am Rand, J_C zwischen Rand und Innerem und −α_C im Inneren.')
eq(r'\beta=\frac4{\sqrt6},\qquad \alpha_C=\frac\beta2(p_C+q_C)+(\mu\ell)^2')
eq(r'\alpha_C\geq\alpha_0=\beta+(\mu\ell)^2>0')
p('p_C und q_C zählen die Vorgänger beziehungsweise Nachfolger des inneren Elements. Beide sind 1 oder 2. Alle inzidenten Relationen sind Links; jeder nichtverschwindende Eintrag von J_C ist β/2.')
table([['(p_C,q_C)','Anzahl Historien','α_C bei μ=0'],['(1,1)','20','β'],['(1,2)','6','3β/2'],['(2,1)','6','3β/2'],['(2,2)','1','2β']],[57*mm,53*mm,54*mm])
eq(r'\|J_C\|^2=\frac{\beta^2}{4}(p_C+q_C),\qquad\frac{\|J_C\|^2}{\alpha_C^2}\leq\frac12')
p('Für η=J_Cb mit b=(q₀,q₁,q₃,q₄) ist das innere Integral exakt:')
eq(r'F_{C,\epsilon}(\eta)=\frac{\sqrt{2\pi}}{(\epsilon+i\alpha_C)^{1/2}}\exp\!\left[-\frac{\eta^2}{2(\epsilon+i\alpha_C)}\right]')
p('Die Wurzel wird aus der rechten Halbebene fortgesetzt. Bei ε=0, η=0 besitzt der Faktor die Phase e^(−iπ/4). Die 33 Hessians wurden unabhängig aus ihren Relationen rekonstruiert und gegen die eingefrorenen Vorgängerdaten geprüft.',SMALL)
p('Die dimensionslose Lücke ist kein Kontinuumssatz für feste physikalische Pakete: bei Änderung von ℓ ändern sich hier auch T_b=ℓ und F=√ℏ/ℓ.',SMALL)

page('03','Eine explizite integrierbare Majorante')
eq(r'|F_{C,\epsilon}(\eta)|=\frac{\sqrt{2\pi}}{(\epsilon^2+\alpha_C^2)^{1/4}}\exp\!\left[-\frac{\epsilon\eta^2}{2(\epsilon^2+\alpha_C^2)}\right]')
eq(r'|F_{C,\epsilon}(\eta)|\leq\sqrt{\frac{2\pi}{\alpha_0}}')
p('Die übrigen Wirkungsfaktoren haben Betrag eins. Nach innerer Integration ist deshalb bezüglich des Produkts aller fünf Staubmaße und des vierdimensionalen Randfeldmaßes folgende Funktion eine Majorante:')
eq(r'g=\frac12|d_{s^{\prime}}d_s|\,|h_{n^{\prime}}h_n|\sqrt{\frac{2\pi}{\alpha_0}}')
p('Der Vorfaktor 1/2 entsteht aus zwei Randquotientmaßen und zwei Faktoren √2 der normierten Zustände. Die L1-Normen sind a₀=a_D=1/2, a_M=1/√2, a₊=√3/2 sowie:')
eq(r'L_0=2\sqrt{\pi\sigma_s\sigma_a},\qquad L_1=4\sqrt{\sigma_s\sigma_a}')
eq(r'\int g=\frac{a_{s^{\prime}}a_s}{2}L_{n^{\prime}}L_n\sqrt{\frac{2\pi}{\alpha_0}}<\infty')
p('Der Satz von der dominierten Konvergenz erlaubt damit den Abel-Grenzwert unter sämtlichen Staubintegralen, den äußeren Skalarintegralen und der endlichen Historiensumme. Die Atome sind Bestandteil des Maßes und werden ausdrücklich mitkontrolliert.')
eq(r'|\mathcal M_{s^{\prime}n^{\prime},sn}(\epsilon)|\leq C_\nu\sqrt{\frac{2\pi}{\alpha_0}}\frac{a_{s^{\prime}}a_s}{2}L_{n^{\prime}}L_n')
p('Für Einheitsbreiten und die Reihenfolge (0,0),(0,1),(+,0),(+,1) ist die entryweise Schrankenmatrix Cν√(2π/β) ffᵀ mit f=(√(π/2), √2, √(3π/2), √6). Ihr größter Eintrag ist 6√(π√6/2) Cν ≈ 11.7692557818 Cν. Größere nichtnegative Skalarmassen verbessern diese Schranke.',SMALL)
p('Diese Werte sind Schranken für Amplituden. Sie sind keine Übergangswahrscheinlichkeiten und keine berechneten physikalischen Matrixeinträge.',SMALL)

page('04','Der Regulatorfehler ist quantitativ kontrolliert')
p('Existenz allein sagt noch nicht, wie nah ein endliches ε am Grenzwert liegt. Die Ableitung der exakten inneren Gaußformel liefert mit z=ε+iα:')
eq(r'\partial_\epsilon F=F\left(-\frac1{2z}+\frac{\eta^2}{2z^2}\right)')
eq(r'|F_\epsilon-F_0|\leq\epsilon\sqrt{\frac{2\pi}{\alpha}}\left(\frac1{2\alpha}+\frac{\eta^2}{2\alpha^2}\right)')
p('Die absoluten Pakete |h_n|/L_n definieren normierte Verteilungen mit Mittelwert null. Ihre Varianz in der symmetrischen Feldrichtung beträgt σ_s² für n=0 und 2σ_s² für n=1; in der antisymmetrischen Richtung jeweils σ_a².')
eq(r'\Sigma\preceq\Lambda I,\quad\Lambda=\max(2\sigma_s^2,\sigma_a^2),\quad\frac{J\Sigma J^T}{\alpha^2}\leq\frac\Lambda2')
p('Bezeichne die rechte Seite der Amplitudenschranke auf Seite 4 mit B_ij. Dann gilt für jeden primären Eintrag:')
eq(r'|\mathcal M_{ij}(\epsilon)-\mathcal M_{ij}(0)|\leq\epsilon B_{ij}\left(\frac1{2\alpha_0}+\frac\Lambda4\right)')
table([['ε','Maximaler absoluter Fehler / Cν'],['10⁻²','kleiner als 0.09489'],['10⁻³','kleiner als 0.009489'],['10⁻⁴','kleiner als 0.0009489']],[57*mm,107*mm])
p('Die Tabelle verwendet Einheitsbreiten und die konservative masselose Konstante 9.489. Die ungerundete Konstante ist ungefähr 9.488211805615503. Dies ist ein reiner Abel-Regulatorfehler. Historien-Trunkierung, physikalische Modellwahl und ein möglicher Kontinuumsfehler sind darin nicht enthalten.',SMALL)

page('05','Alle fünf Dichteintegrale lassen sich ausführen')
p('Die Staubwirkung ist linear in den fünf Dichten. Für feste Uhrdaten gilt mit κ_x=W(1+Γ_x[T_b t])/(2ℏ):')
eq(r'E(k)=\int_0^1e^{-ikr}dr=e^{-ik/2}\,\mathrm{sinc}(k/2),\qquad E(0)=1')
eq(r'|E(k)|\leq1\quad(k\in\mathbb R)')
p('Atom und Positivachse ergeben 1/2 beziehungsweise E(k)/2. Die scheinbare Polstelle in (1−e^(−ik))/(ik) ist hebbar. Auch κ=0 und negative κ sind zulässig. Nach Einsetzen des jeweiligen Randpakets entstehen folgende Faktoren; u und v sind die beiden zugehörigen E-Werte:')
table([['Randsektor','Integrierter Faktor R_s(u,v)'],['0','1/2'],['M: genau eine positive Dichte','(u+v)/(2√2)'],['D: beide positiv','uv/2'],['+: mindestens eine positiv','(u+v+uv)/(2√3)']],[88*mm,76*mm])
p('Der vollständige Staubfaktor ist damit exakt:')
eq(r'D_C^{s^{\prime}s}=\frac12\int d\lambda^5(t)\,R_{s^{\prime}}(E_3,E_4)R_s(E_0,E_1)\frac{1+E_2}{2}')
p('Hier bedeutet E_x=E(κ_x(t)). Die Formel enthält sämtliche 32 Atom/Positivmasken. Übrig bleibt ein glattes Integral auf der kompakten fünfdimensionalen Uhrbox. Zusammen mit dem separat integrierten Skalarfaktor A_C gilt M_ε=Σ c_C e^(iS_g/ℏ) D_C A_C(ε).')
p('<b>Singuläre Staubuhr-Blöcke sind auf der Box harmlos.</b> Beispielsweise ist (1/2)∫₋₁¹ exp(iat²/2)dt bei a=0 genau eins und für alle reellen a im Betrag höchstens eins. Eine unbeschränkte Fresnel-Determinantenformel darf dieses kompakte Integral nicht ersetzen. Staubuhr-Hessian und Skalar-Hessian sind unterschiedliche Operatoren.',SMALL)

page('06','Wann singuläre Innenblöcke trotzdem zulässig sind')
p('Für spätere Modelle sei H(θ) reell, symmetrisch und stetig in den Staubparametern θ. Der Träger sei kompakt, einschließlich seiner Grenzstrata und Atome. Ω&gt;0 bezeichnet eine feste Rand-Gaußpräzision. Definiere:')
eq(r'Q_0(\theta)=\mathrm{diag}(\Omega,0)-iH(\theta)')
eq(r'Q_\epsilon=Q_0+\epsilon\,\mathrm{diag}(0,I)')
p('Mit Innenblock A und Rand-Innenkopplung J ist Q₀ genau dann invertierbar, wenn das bekannte Nullraumkriterium gilt:')
eq(r'\ker A(\theta)\cap\ker J(\theta)^T=\{0\}')
p('Beweis: Aus Q₀z=0 folgt durch den Realteil von z*Q₀z zuerst, dass die Randkomponente null ist. Die verbleibende Innenkomponente muss dann gleichzeitig von A und Jᵀ annihiliert werden.')
p('<b>Der zusätzliche Schritt:</b> Gilt das Kriterium an jedem Punkt des abgeschlossenen Trägers, liefern Kompaktheit und Stetigkeit eine positive kleinste Singulärwertschranke δ. Dann gilt für 0≤ε≤δ/2:')
eq(r'\delta=\inf_\theta\sigma_{\min}(Q_0(\theta))>0')
eq(r'\|Q_\epsilon^{-1}\|\leq2/\delta,\qquad |\det Q_\epsilon|\geq(\delta/2)^d')
p('Der Gaußdeterminantenfaktor und die endlichgradigen Wick-Polynome für Hermitepakete sind gleichmäßig beschränkt. Bei endlichem Staubmaß und beschränkten Staubpaketen folgt dominierte Konvergenz auch dann, wenn A selbst singulär ist.')
p('Gilt das Kriterium nur für positive Dichten oder fast überall, kann δ null sein. Dann muss die Singularität gesondert integriert werden. Für Maß r^(k−1+γ)dr und Betrag von Ordnung r^(−p) ist die lokale Bedingung p&lt;k+γ; Gleichheit führt bei nichtverschwindendem führenden Betrag zur logarithmischen Divergenz. Atome müssen separat geprüft werden.',SMALL)

page('07','Drei exakte Gegenproben zur Nullraumprüfung')
p('Diese reduzierten Zweivariablenmodelle sind Gegenproben, keine Bestandteile der gewählten 33-Historien-Wirkung. Ein Randfeld hat Gaußpräzision eins; das innere Feld besitzt Regulator ε. Nach Entfernung eines gemeinsamen Faktors 2π gilt U_ε=(det Q_ε)^(−1/2).')
p('1 · Singulärer Innenblock, tragende Randkopplung',H3)
eq(r'A=0,\ J=1:\qquad U_\epsilon=(1+\epsilon)^{-1/2}\longrightarrow1')
p('Der Innenblock allein muss nicht invertierbar sein. Eine gleichmäßig wirksame Kopplung zum Rand kann die Nullrichtung erfassen.',SMALL)
p('2 · Kontinuierlich integrierbar, am Atom divergent',H3)
eq(r'A=r,\ J=0:\qquad U_\epsilon(r)=(\epsilon-ir)^{-1/2}')
eq(r'\int_0^1U_\epsilon(r)dr\longrightarrow2e^{i\pi/4},\qquad U_\epsilon(0)=\epsilon^{-1/2}')
p('Auf der positiven Achse dominiert die integrierbare Funktion r^(−1/2). Das Atom trägt dagegen eine echte ε^(−1/2)-Divergenz. Eine stetige Quadratur allein würde sie übersehen.',SMALL)
p('3 · Punktweise zulässig, nach Dichteintegration divergent',H3)
eq(r'A=0,\ J=r:\qquad U_\epsilon(r)=(\epsilon+r^2)^{-1/2}')
eq(r'\int_0^1U_\epsilon(r)dr=\mathrm{arsinh}(\epsilon^{-1/2})=\log2-\frac12\log\epsilon+o(1)')
p('Für jedes r&gt;0 gilt das Nullraumkriterium. Trotzdem divergiert das positive Dichteintegral logarithmisch. Mit dem Mischmaß aus Schritt 2 kommt der Atomterm hinzu:')
eq(r'\int U_\epsilon\,d\nu=\frac1{2\sqrt\epsilon}+\frac12\mathrm{arsinh}(\epsilon^{-1/2})')
p('Alle Beiträge dieses Beispiels sind positiv. Eine oszillatorische Auslöschung kann seine Divergenz daher nicht beseitigen.',SMALL)

page('08','Abgeschlossener Schritt und verbleibende Grenzen')
table([['Aussage','Status'],['Endliche AA-Amplitude im deklarierten Abel-Sinn','bewiesen'],['Dichteatome und beliebig kleine positive Dichten','in der Majorante enthalten'],['Alle fünf Dichteintegrale','analytisch eliminiert'],['Gemeinsame Staubintegration und Abel-Entfernung','für feste Boxen abgeschlossen'],['Unendliche CST-Summe / physikalische Gewichtung','offen'],['Entfernung der Staubboxen / Kontinuum bei festen physikalischen Zuständen','nicht bewiesen'],['Physikalische Übergangsmatrix / Unitarität / Bounce','nicht hergeleitet']],[111*mm,53*mm])
p('<b>Warum die Uhrbox wesentlich bleibt:</b> Ersetzt man nur das innere Uhrmaß durch unnormalisiertes dT₂ auf [−L,L], dann ist im Sektor mit allen fünf Dichten am Atom S_d=0. Für einen nichtverschwindenden Einzelhistorienbeitrag entsteht ∫dT₂=2L→∞. Eine Normierung durch 2L würde stattdessen das Maß ändern. Der jetzige Existenzsatz rechtfertigt diese Erweiterung nicht.')
p('<b>Reproduktion:</b> python verify.py mit Python 3.10+ und SymPy 1.14.0. Der Prüfer verlangt 22 bestandene Tests, vollständige Datei-Hashdeckung, fünf unveränderte Herkunfts-Blobs und bytegleichen Ergebnis-Replay. Numerische Stichproben begleiten die analytischen Beweise; sie ersetzen sie nicht.',SMALL)
p('<b>Vollständige Herleitung:</b> DERIVATION.md im Prüfpaket. Der maschinenlesbare Vertrag trennt mathematische Existenz, physikalische Interpretation und ausgeschlossene Grenzwerte. Alle acht physikalischen Gates bleiben HOLD.',SMALL)
p('Herkunft und Quellen',H3)
p('Projektbasis: Main 602e4d5f2ab713ed6825061577cba4f471cd51a5. Exakte Herkunftspfade und Git-Blob-Werte: provenance.json.',SMALL)
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/278" color="#087E8B">PR #278: gerichteter Randvertrag</link> · <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/279" color="#087E8B">PR #279: gemeinsame Wirkung</link> · <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/280" color="#087E8B">PR #280: normierte Randzustände</link>',SMALL)
p('<link href="https://dlmf.nist.gov/7.2" color="#087E8B">NIST DLMF §7.2</link> und <link href="https://dlmf.nist.gov/7.7" color="#087E8B">§7.7</link>: Hintergrund zu Gauß- und Fehlerfunktionsintegralen. Die Modellschranken und Gegenbeispiele sind in dieser Ausarbeitung eigenständig hergeleitet.',SMALL)

def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(TEAL);canvas.setLineWidth(.6)
    canvas.line(23*mm,282*mm,187*mm,282*mm)
    canvas.setFont('DejaVu',8);canvas.setFillColor(NAVY)
    canvas.drawString(23*mm,286*mm,'CST-DUST  /  Amplitudenexistenz A → A  /  v0.1')
    canvas.drawString(23*mm,12*mm,'11. November 2026  |  Endlicher Kandidat; physikalische Gates HOLD')
    canvas.drawRightString(187*mm,12*mm,str(doc.page));canvas.restoreState()

if __name__=='__main__':
    doc=SimpleDocTemplate(str(OUT),pagesize=(210*mm,297*mm),leftMargin=23*mm,rightMargin=23*mm,
                         topMargin=23*mm,bottomMargin=22*mm,title='CST-DUST Amplitudenexistenz A zu A v0.1',author='X6 Forschungsprogramm / Arbeitsausarbeitung')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)

