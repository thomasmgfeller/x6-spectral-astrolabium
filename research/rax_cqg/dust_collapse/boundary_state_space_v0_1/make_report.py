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
OUT=ROOT/'CST_DUST_Randzustandsraum_v0_1.pdf'
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
    tex=re.sub(r'\\frac(\d)(\d)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',tex)
    tex=re.sub(r'\\frac(\d)',lambda m:r'\frac{'+m[1]+'}',tex)
    tex=re.sub(r'\\sqrt(\d)',lambda m:r'\sqrt{'+m[1]+'}',tex)
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
    p('CST-DUST  /  SCHRITT 2  /  '+k,KICK); p(title,H2)

page('ERGEBNIS','Ein kleiner, eindeutiger Randzustandsraum')
p('A → A mit einem inneren Element',H1)
p('Ein expliziter kinematischer Testraum mit gemeinsam definierten Dichtestrata, Randpaketen, Maß und Skalarprodukt. Anschluss an den Wirkungsansatz CST-DUST-KG-MIN-v0.1, PR #279.')
eq(r'\mathcal{B}_{\min}=\{|A,0,0_m\rangle,|A,0,1_m\rangle,|A,+,0_m\rangle,|A,+,1_m\rangle\}')
eq(r'G_{\min}=I_4,\qquad\mathrm{rank}\,G_{\min}=4')
p('<b>Vier unabhängige Zustände pro Rand.</b> Diese Zahl folgt aus den berechneten Skalarprodukten. Ein- und Ausgang verwenden dieselben normierten Pakete und sind dadurch unmittelbar vergleichbar.')
table([['Familie','Benannte Vektoren','Gram-Rang'],['Minimal: 0 und +, je n=0,1','4','4'],['Aufgelöst: 0, M und D, je n=0,1','6','6'],['Aufgelöst plus zusätzliches +','8','6']],[85*mm,40*mm,39*mm])
p('<b>„+“ ist festgelegt:</b> mindestens eine positive Randdichte. Die Belegungen 10, 01 und 11 werden mit gleicher positiver Amplitude kohärent zusammengefasst. Das ist eine konkrete Zustandswahl, keine weitere unabhängige Belegung.')
p('20 automatisierte Prüfungen bestanden. Der vollständige Hilbertraum bleibt unendlichdimensional. Das physikalische CST-Skalarprodukt, die Übergangsmatrix und die dynamische Geschlossenheit dieses kleinen Raums sind damit nicht hergeleitet.',BODY)
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b>',H3)

page('01','Träger, Maß und Skalarprodukt')
p('Der Eingang L={0,1} und der Ausgang R={3,4} sind Zweierantichains; I={2} enthält das einzige innere Element. Die bisherige abgedeckte AA-Kontrollfamilie enthält 33 Ordnungen. Ihre physikalische Eignung als vierdimensionales Ensemble oder vollständiger Cauchy-Kragen wird nicht vorausgesetzt.')
eq(r't=T/T_b,\quad r=w/W,\quad q=\Phi/F')
p('Kontrollwerte: T_b=ℓ, W=ℏ, F=√ℏ/ℓ bei ℓ,ℏ&gt;0. Die beiden Ränder verwenden dieselben Werte. T ist die Staubuhr, w das integrierte Staubdichtegewicht und Φ das zusätzliche reelle Skalarfeld. w=0 bedeutet keine Abwesenheit dieses Skalarfelds.')
eq(r'd\lambda=\frac12\mathbf{1}_{[-1,1]}dt,\qquad d\nu=\frac12\delta_0(dr)+\frac12\mathbf{1}_{(0,1)}dr')
eq(r'd\mu_{\mathrm{lab}}=\prod_{j=1}^2d\lambda(t_j)d\nu(r_j)dq_j')
eq(r'\langle\Psi,\Xi\rangle_A=\frac12\int\overline{\Psi}\,\Xi\,d\mu_{\mathrm{lab}}')
p('Die zwei Randpunkte sind unmarkiert. S₂ vertauscht ihre gesamte Ausstattung (t,r,q). H_A ist der S₂-invariante Teil des L²-Raums; P_A=(1+U_swap)/2. Der Faktor 1/2 im Skalarprodukt ist die Division durch |S₂|. Er wird bei der Normierung genau einmal berücksichtigt.')
p('<b>Atom und Kontinuum werden getrennt integriert.</b> Der Nullpunkt besitzt durch δ₀ Masse 1/2. Eine reine stetige Quadratur würde ihn verlieren. Für das isolierte Dichtemuster sind die Quotientmassen 1/8 für 00, 1/4 für {10,01} und 1/8 für 11.')
p('Das Uhrpaket χ(t₁,t₂)=1 hat Norm eins im normierten Boxmaß. Hilfsuhren bleiben auch an Atomstellen erhalten, weil sie in der gerichteten Staubwirkung an spätere positive Dichten koppeln können. Ein Uhrtranslationsquotient oder physikalischer Zeitparameter wird hier nicht abgeleitet.',SMALL)

page('02','Welche Belegungen umfasst „+“?')
p('Eine 0 im Maskennamen bezeichnet das Atom, eine 1 die positive Achse 0&lt;r&lt;1. Im gelabelten Dichtemaß hat jede der vier Masken Masse 1/4. Innerhalb positiver Achsen sind die gewählten Pakete konstant.')
table([['Sektor','Belegungen','Dichtepaket d_s'],['0','00','2 · 1₀₀'],['M: genau ein positiver Punkt','10, 01','√2 · (1₁₀ + 1₀₁)'],['D: beide positiv','11','2 · 1₁₁'],['+: mindestens einer positiv','10, 01, 11','(2/√3) · (1₁₀ + 1₀₁ + 1₁₁)']],[57*mm,36*mm,71*mm])
eq(r'd_+=\sqrt{\frac23}\,d_M+\frac1{\sqrt3}d_D')
p('Der Zustand + hat relative Phase null. Seine drei Maskenwahrscheinlichkeiten sind jeweils 1/3. Für die vertauschungsinvarianten Teilsektoren folgt P(M)=2/3 und P(D)=1/3.')
p('<b>Kohärenter Zustand und statistische Mischung sind verschieden.</b> Der reine Zustand |+⟩⟨+| besitzt im M,D-Block die Nebendiagonale √2/3. Die Mischung (2/3)|M⟩⟨M|+(1/3)|D⟩⟨D| besitzt dort null. Beide liefern dieselben Maskenwahrscheinlichkeiten; ihre Reinheiten sind 1 beziehungsweise 5/9.')
p('Diese Kohärenz ist eine offengelegte Präparationsannahme. Ihre physikalische Realisierung folgt nicht aus dem Wirkungsansatz. Falls eine Superselektion verlangt wird, muss der Zustandsvertrag geändert werden.')
eq(r'\langle d_+,d_D\rangle=\frac1{\sqrt3}\ne1')
p('„+“ und „beide positiv“ sind deshalb nicht austauschbar. Auch mit einer anderen positiven Paketform oder einer relativen Phase entsteht ein anderer Versuch. Solche Änderungen müssen zusammen mit Maß und Skalarprodukt dokumentiert werden.')

page('03','Randwellenfunktionen und Normierung')
eq(r'q_s=\frac{q_1+q_2}{\sqrt2},\qquad q_a=\frac{q_1-q_2}{\sqrt2}')
eq(r'h_0=\frac{e^{-(q_s^2/\sigma_s^2+q_a^2/\sigma_a^2)/2}}{\sqrt{\pi\sigma_s\sigma_a}},\qquad h_1=\sqrt2\frac{q_s}{\sigma_s}h_0')
p('Die Breiten σ_s,σ_a sind positiv und endlich; im Kontrollpunkt beide 1. Die zweite skalare Richtung verbleibt im Grundpaket. n=0,1 bezeichnet zwei Paketbesetzungen in derselben symmetrischen Richtung, keine zwei verschiedenen Modenprofile und kein bereits identifiziertes physikalisches Vakuum.')
eq(r'\int_{\mathbb{R}^2}\overline{h_n}h_m\,d^2q=\delta_{nm}')
p('Die Normen folgen aus den Gaußmomenten ∫e^(−x²)dx=√π, ∫xe^(−x²)dx=0 und ∫x²e^(−x²)dx=√π/2. Die zwei ersten Hermite-Gaußpakete sind damit direkt integriert; die exakten Kontrollen stehen im Prüfpaket. Standardorthogonalität: NIST DLMF §18.3.')
eq(r'\Psi_{s,n}=\sqrt2\,\chi\,d_s\,h_n,\qquad s\in\{0,M,D,+\},\ n\in\{0,1\}')
p('Der Faktor √2 kompensiert genau den Faktor 1/2 im Quotientmaß. Somit gilt für jeden der benannten Zustände ‖Ψ_s,n‖=1. Die Produkte von Uhr-, Dichte- und Skalarintegralen liefern alle Überlappungen.')
eq(r'G_{(s,n),(s^{\prime},m)}=\langle d_s,d_{s^{\prime}}\rangle_\nu\,\delta_{nm}')
p('Unter Punktvertauschung bleibt q_s fest und q_a wechselt das Vorzeichen. Beide gewählten h_n sind invariant. Unter Gesamtfeldumkehr q→−q besitzt h_n die Parität (−1)^n. Orthogonale Dichteträger allein begründen keine dynamische Superselektion.',SMALL)

page('04','Die Gram-Matrix entscheidet den Rang')
p('Für die primäre Reihenfolge (0,0),(0,1),(+,0),(+,1) folgt G_min=I₄. Für die aufgelöste Produktfamilie (0,0),(0,1),(M,0),(M,1),(D,0),(D,1) folgt G_res=I₆.')
p('Nimmt man + zusätzlich zu 0,M,D auf, ist die Dichte-Gram-Matrix in der Reihenfolge (0,M,D,+):')
table([['','0','M','D','+'],['0','1','0','0','0'],['M','0','1','0','√(2/3)'],['D','0','0','1','1/√3'],['+','0','√(2/3)','1/√3','1']],[20*mm,36*mm,36*mm,36*mm,36*mm])
eq(r'G_{\mathrm{red}}=G_{\mathrm{density}}\otimes I_2')
eq(r'\mathrm{spec}(G_{\mathrm{red}})=\{0,0,1,1,1,1,2,2\},\qquad\mathrm{rank}=6')
p('Für jedes n=0,1 ist die lineare Abhängigkeit exakt:')
eq(r'\Psi_{+,n}-\sqrt{\frac23}\Psi_{M,n}-\frac1{\sqrt3}\Psi_{D,n}=0')
p('Die zwei zusätzlichen unabhängigen Dichterichtungen außerhalb des primären Viererraums sind:')
eq(r'\Psi_{\Delta,n}=\frac1{\sqrt3}\Psi_{M,n}-\sqrt{\frac23}\Psi_{D,n}')
p('Sie haben Norm eins und sind orthogonal zu allen vier primären Zuständen. „+“ reduziert die gewählte Familie also durch Auswahl einer Richtung im positiven Teilraum. Das ist keine hergeleitete Zwangsbedingung.')

page('05','Was dieser kleine Raum auslässt')
p('<b>Die vollständige Randkinematik ist unendlichdimensional.</b> Vier und sechs sind Ränge bestimmter Paketfamilien. Weitere Dichte-, Uhr- und Skalarprofile sowie ihre Korrelationen bleiben zulässig.')
p('Die reine skalare antisymmetrische Anregung h_a=√2 q_a h₀/σ_a wird zusammen mit symmetrischen Dichtepaketen vom Vertauschungsprojektor auf null abgebildet. Sie darf nicht als zusätzlicher normierter Zustand gezählt werden.')
eq(r'h_a=\sqrt2\frac{q_a}{\sigma_a}h_0,\qquad P_A(d_s h_a)=0')
p('Eine Korrelation zwischen antisymmetrischer Dichte und antisymmetrischem Skalarpaket ist dagegen insgesamt invariant:')
eq(r'\Xi=2(\mathbf{1}_{10}-\mathbf{1}_{01})\,\chi\,h_a')
eq(r'U_{\mathrm{swap}}\Xi=\Xi,\qquad\|\Xi\|_A=1')
p('Dieser Zustand ist orthogonal zu den sechs ausgewählten Produktzuständen. Die Kontrolle zeigt, weshalb selbst die aufgelöste Sechserfamilie nicht der vollständige vertauschungsinvariante Raum der niedrigen Anregungen ist.')
p('<b>Ein- und Ausgang sind isomorphe Kopien.</b> Zwei mögliche Identifikationen der unmarkierten Antichains wirken auf invariant gewählte Pakete gleich. Gemeinsame Skalen, Breiten, Uhrpakete und Dichtemasken liefern eine unitäre Identifikation und Kreuzüberlapp I₄.')
p('Die Übergangsmatrix zwischen den primären Räumen hat deshalb vier Zeilen und vier Spalten. Zeilen sind ausgehend, Spalten eingehend. Eine direkte Summe beider Randräume hätte als Buchhaltung Dimension acht; sie verdoppelt nicht die Zahl der Zustände pro Rand.')
p('Die jetzige Gram-Matrix ist eine kinematische Norm. Ein später begründetes physikalisches Constraint- oder Rigging-Verfahren kann eine andere Gram-Matrix und weitere Nullrichtungen erzeugen. Damit bleibt das physikalische Skalarprodukt ausdrücklich offen.',SMALL)

page('06','Vergleich, Maßtransport und inneres Element')
p('Bei unterschiedlichen Breiten bleiben die Einzelzustände normiert, aber ihr Kreuzüberlapp ist nicht automatisch die Einheitsmatrix. Definiere für die symmetrische Richtung R_s und analog R_a:')
eq(r'R_s=\frac{2\sigma_s^{\mathrm{in}}\sigma_s^{\mathrm{out}}}{(\sigma_s^{\mathrm{in}})^2+(\sigma_s^{\mathrm{out}})^2}')
eq(r'S_{00}=\sqrt{R_sR_a},\quad S_{11}=R_s\sqrt{R_sR_a},\quad S_{01}=S_{10}=0')
p('Für σ_s^in=1, σ_s^out=2 und σ_a=1 sind die beiden Diagonalwerte 2/√5 und 8/(5√5). Ein solcher Überlapp ist kein dynamischer Übergangskern.')
p('Bei dμ′=r dμ muss derselbe Zustand durch Ψ′=r^(−1/2)Ψ dargestellt werden. Für denselben Integraloperator sind beide Kernargumente mitzutragen:')
eq(r'K^{\prime}(y,x)=r_{\mathrm{out}}(y)^{-1/2}K(y,x)r_{\mathrm{in}}(x)^{-1/2}')
p('Im dimensionalen Skalarmaß ist ψ_Φ(Φ)=F^(−1)h(Φ/F). Im Gaußadapter gilt H_q=F²H_Φ und in (q_s,q_a) Ω_q=ℏ diag(σ_s⁻²,σ_a⁻²). Die Wirkungs- und Paketbreitenmatrizen bleiben getrennt.')
p('Für die feste Kontrollhistorie wird das innere Maß mit einem Abel-Regulator ergänzt:')
eq(r'd\mu_{I,\epsilon}=d\lambda(t_2)d\nu(r_2)dq_2\,e^{-\epsilon q_2^2/2},\qquad\epsilon>0')
p('Der Skalarregulator wird nicht als Wahrscheinlichkeit normalisiert. Die Uhr- und Dichtebox bleiben fest. Der Vorgänger beweist für alle 33 Kontrollen bei festem ℓ&gt;0 einen invertierbaren inneren Skalarblock; das ist kein gleichmäßiger Kontinuumsgrenzwert und keine physikalische Kernnormierung.')
p('Die spätere Projektion verwendet ∫dμ_out dμ_in Ψ̄_out K_ε Ψ_in. Historiengewichte, der physikalische Vorfaktor und der vollständige Kern werden in diesem Schritt nicht festgelegt oder berechnet.',SMALL)

page('07','Prüfbarkeit und verbleibende Physik')
table([['Ergebnis','Status'],['Normierte Randpakete und positive kinematische Norm','konstruiert'],['Gram-Matrizen, Ränge und Nullrelationen','exakt berechnet'],['Automatisierte Kontrollen','20 bestanden'],['Physikalisches CST-Skalarprodukt','nicht hergeleitet'],['Physikalischer Kern / K₀₊','nicht konstruiert / nicht berechnet'],['Dynamische Geschlossenheit des Viererraums','nicht bewiesen'],['Alle acht physikalischen Gates','HOLD']],[111*mm,53*mm])
p('<b>Reproduktion:</b> python verify.py mit Python 3.10+ und SymPy 1.14.0. Das Paket kontrolliert Gaußintegrale, Masken- und Orbitgewichte, Vertauschungsprojektor, Labelduplikate, exakte Ränge, Nullrelationen, ausgelassene Richtungen, kohärente Summe gegen Mischung, Parität und Breitenüberlapp. Dazu kommen Hashprüfung, Herkunfts-Blobs und bytegleicher Ergebnis-Replay.')
p('<b>Nächster Anschluss:</b> die regulierte AA-Kandidatenwirkung auf die vier normierten Pakete projizieren, sobald Historiengewicht und Kernvorfaktor zusätzlich festgelegt sind. Die beiden Δ-Richtungen und höhere skalare Besetzungen müssen als Austrittskanäle kontrolliert werden.')
p('Die konstruierten Zustände beweisen keine geschlossene Evolution, Unitarität, Rückwirkung, Junction-Physik oder Singularitätsauflösung. Maß, kohärente Präparation und Paketbreiten bleiben explizite Modellentscheidungen. Die vollständige Herleitung und der maschinenlesbare Vertrag liegen im Prüfpaket.',SMALL)
p('Quellen und Herkunft',H3)
p('Projektbasis: Main <b>91f46fe5f827f823c1c2a9e967c8bd031afb7f0d</b>, PR #279. Gerichteter Randvertrag: PR #278. Exakte Pfade und Git-Blob-Werte: provenance.json.',SMALL)
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/279" color="#087E8B">GitHub: gemeinsamer Skalarwirkungsansatz, PR #279</link><br/><link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/278" color="#087E8B">GitHub: gerichteter Randvertrag, PR #278</link>',SMALL)
p('<link href="https://dlmf.nist.gov/18.3" color="#087E8B">NIST DLMF §18.3: Hermite-Orthogonalität</link><br/><link href="https://arxiv.org/abs/1001.2725v4" color="#087E8B">Benincasa / Dowker: The Scalar Curvature of a Causal Set</link> (Operatorhintergrund; keine Begründung des hier gewählten Randmaßes).',SMALL)

def footer(canvas,doc):
    canvas.saveState(); canvas.setStrokeColor(TEAL); canvas.setLineWidth(.6)
    canvas.line(23*mm,282*mm,187*mm,282*mm)
    canvas.setFont('DejaVu',8); canvas.setFillColor(NAVY)
    canvas.drawString(23*mm,286*mm,'CST-DUST  /  Randzustandsraum A → A  /  v0.1')
    canvas.drawString(23*mm,12*mm,'11. November 2026  |  Kinematischer Kandidat; physikalische Gates HOLD')
    canvas.drawRightString(187*mm,12*mm,str(doc.page)); canvas.restoreState()

if __name__=='__main__':
    doc=SimpleDocTemplate(str(OUT),pagesize=(210*mm,297*mm),leftMargin=23*mm,rightMargin=23*mm,
                         topMargin=23*mm,bottomMargin=22*mm,title='CST-DUST Randzustandsraum A zu A v0.1',author='X6 Forschungsprogramm / Arbeitsausarbeitung')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(OUT)
