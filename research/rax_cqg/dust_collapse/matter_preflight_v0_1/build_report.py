#!/usr/bin/env python3
"""Compact, explicitly scoped reading edition of DERIVATION.md."""
from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Materieblock_Vorpruefung_v0_1.pdf'
FONT='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DejaVu',FONT+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',FONT+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyD',fontName='DejaVu',fontSize=9.5,leading=14,spaceAfter=8,textColor=colors.HexColor('#23313a')))
styles.add(ParagraphStyle(name='TitleD',fontName='DejaVu-Bold',fontSize=22,leading=27,spaceAfter=13,textColor=colors.HexColor('#123e51')))
styles.add(ParagraphStyle(name='HeadD',fontName='DejaVu-Bold',fontSize=15,leading=20,spaceAfter=12,textColor=colors.HexColor('#123e51')))
styles.add(ParagraphStyle(name='SubD',fontName='DejaVu-Bold',fontSize=10.5,leading=15,spaceBefore=7,spaceAfter=6,textColor=colors.HexColor('#12615e')))
styles.add(ParagraphStyle(name='SmallD',fontName='DejaVu',fontSize=8,leading=11,spaceAfter=6))
story=[]
def p(text,style='BodyD'): story.append(Paragraph(text,styles[style]))
def h(text): p(text,'SubD')
def eq(text):
    fig=plt.figure(figsize=(7,.55))
    fig.text(.5,.5,'$'+text+'$',ha='center',va='center',fontsize=14,color='#123e51')
    buf=BytesIO();fig.savefig(buf,format='png',dpi=200,bbox_inches='tight',pad_inches=.08,transparent=True);plt.close(fig);buf.seek(0)
    from PIL import Image as PIL
    im=PIL.open(buf);w,hh=im.size;buf.seek(0)
    width=min(485,w*.38);story.append(Image(buf,width=width,height=hh*width/w));story.append(Spacer(1,8))
def table(rows,widths):
    data=[[Paragraph(str(x),styles['SmallD']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7f0f2')),
       ('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#9fb7bf')),
       ('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d9e1e5')),
       ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
       ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(t);story.append(Spacer(1,10))
def page(title):
    story.append(PageBreak());p(title,'HeadD')

p('CST-DUST | ARBEITSARTEFAKT v0.1','SmallD')
p('Materieblöcke:<br/>Randvertrag, Schur- und<br/>Paritätsprüfung','TitleD')
p('Korrigierter Anschluss an die Normierungsprüfung einer ausgewählten Hilfsbasis, PR #277. Stand: 11. November 2026.','BodyD')
table([['Ergebnis','Aussagegrenze'],['25 exakte Kontrollen bestanden','Vorbereitung und endliche Algebra'],['Physikalische 8×8-Matrix','NOT_CONSTRUCTED'],['Physikalischer Mischblock K₀₊','NOT_COMPUTED'],['Alle acht physikalischen Gates','HOLD']],[230,265])
h('Der wichtige neue Befund')
p('Der vorgeschlagene Vakuum-zu-Einteilchen-Zeuge verschwindet bei einer unter gemeinsamer Feldspiegelung symmetrischen quadratischen Theorie bereits aus Parität. Das gilt unter ausdrücklich zu prüfenden Annahmen an Randzustände, Maß und Integrationsgebiet. Gerade Mischblöcke können dennoch vorhanden sein.')
h('Was zuerst geklärt werden muss')
p('Die vorhandenen Geometriepolynome zählen Verklebungen, noch keine zeitlichen Randübergänge. Die vorhandene Hesse-Matrix gehört zur Staubuhr. Ihre Eigenvektoren sind weder ein Vakuum noch Einteilchenzustände eines zusätzlichen Skalarfelds.')
h('Arbeitsziel')
p('Ein gemeinsamer, überprüfbarer Randvertrag muss Historien, zusätzliche Feldwirkung, echte Randwellenfunktionen, positive Produkte und Integrationsvorschrift festlegen. Erst dann kann ein paritätserlaubter gemischter Amplitudenzeuge berechnet werden.')
p('Diese Lesefassung fasst DERIVATION.md zusammen. Das Prüfpaket enthält die vollständige Herleitung, gepinnte Projektquellen, Ordnungs-IDs, offene Eingaben und reproduzierbaren Code. Es enthält keine erfundenen Materieblöcke.','SmallD')

page('1 | Die Historienklasse ist Teil der Physik')
p('Die vollständige Neuauszählung der 219 gelabelten Viererordnungen reproduziert die vier bekannten Fasergrößen. Schon eine zusätzliche Orientierungsbedingung verändert sie:')
table([['Klassen','Bekannte Verklebung','Ohne Rückrelationen'],['AA','35','16'],['AK','26','9'],['KA','26','9'],['KK','20','6']],[110,190,195])
p('„Ohne Rückrelationen“ bedeutet ausschließlich: keine Relation vom rechten Zweierblock zum linken; fehlende Kreuzrelationen bleiben erlaubt. Die Zahlen 16=2⁴, 9=3² und 6=binom(4,2) folgen auch unabhängig kombinatorisch.')
p('<b>Diese eingeschränkten Summen sind diagnostische Kontrollen.</b> Sie sind kein bereits begründetes zeitliches Randmodell. Die Zweierkette K ist keine Antikette und somit kein gewöhnlicher raumartiger Cauchyrand.')
h('Ein leerer Innenraum ergibt kein neues Schurproblem')
p('Werden beide Zweierblöcke vollständig zu Randvariablen erklärt, umfasst der Rand alle vier Elemente. Es gibt dann keine übrigen inneren Feldwerte: Der Schurblock ist die ursprüngliche Hesse-Matrix, der innere Gaußfaktor eins. Eine nichttriviale Elimination benötigt einen anderen Träger oder eine andere Randzuordnung.')
h('Basisordnung erhalten')
p('Die stratumweise Reihenfolge aus PR #277 bleibt die Planungsbasis:<br/>A|0|0m, A|0|1m, K|0|0m, K|0|1m,<br/>A|+|0m, A|+|1m, K|+|0m, K|+|1m.')
p('Eine andere Reihenfolge ist möglich, muss aber für Kern, Gram-Matrix und Zustandslabels gemeinsam permutiert werden. Die acht Labels sind weiterhin keine acht hergeleiteten physikalischen Zustände.')

page('2 | Wirkung und stationäre Elimination')
p('Die vorhandene gemeinsame Wirkung enthält die Staubuhr T und Dichtegewichte w. Ein zusätzliches reelles Feld Φ ist bis zum Nachweis seiner Beziehung zu T,w eine Modellerweiterung.')
eq(r'S_\Phi=\frac{1}{2}\Phi^{\mathrm{T}}H_C(T,w)\Phi,\qquad H_C=H_C^{\mathrm{T}}')
p('Ein retardierter Operator D ist nicht automatisch diese Hesse-Matrix. Für reelle Felder gilt:')
eq(r'\nabla_\Phi\left(\frac{1}{2}\Phi^{\mathrm{T}}D\Phi\right)=\frac{D+D^{\mathrm{T}}}{2}\Phi')
p('Die Symmetrisierung einer Bilinearform ist eine ausgewiesene Wirkungsentscheidung; sie bewahrt nicht automatisch die ursprüngliche retardierte Feldgleichung. Maßgewicht, Einheiten, Masse, Vorzeichen und Randterme müssen explizit sein.')
h('Für eine invertierbare innere Hesse-Matrix')
eq(r'q_*=-H_{II}^{-1}H_{Ib}b')
eq(r'H_{\rm eff}=H_{bb}-H_{bI}H_{II}^{-1}H_{Ib}')
p('Diese Formel ist eine exakte stationäre Substitution bei festem C,T,w. Sie ersetzt nicht allgemein das innere Integral. Der bisherige kompakte Uhrregulator darf nicht still gegen volle reelle Integrationsachsen ausgetauscht werden.')
p('Bei kompakten Gebieten verschiebt q→q−q* auch die Integrationsgrenzen. Der Restfaktor hängt dann im Allgemeinen vom Rand b ab. Bei T,w-abhängiger Hesse-Matrix bleiben Schurblock, Determinante und Phase innerhalb der Staubintegrale.')
h('Singuläre Fälle')
eq(r'N^{\mathrm{T}}H_{Ib}b=0\qquad(N\ \mathrm{spannt}\ \ker H_{II})')
p('Die Verträglichkeit ist separat zu prüfen. Die Pseudoinverse allein beseitigt weder Nullraumvolumen noch distributionelle Bedingungen. Nullrichtungen sind ohne Beweis keine Eichrichtungen.')

page('3 | Gaußphase und echte Randzustände')
p('Für volle reelle Achsen, Lebesgue-Maß, ℏ&gt;0, invertierbares reell-symmetrisches H und festgelegte Abel-Dämpfung lautet der innere Faktor:')
eq(r'\mathcal{N}(H)=(2\pi\hbar)^{r/2}\frac{e^{i\pi\,\mathrm{sgn}(H)/4}}{\sqrt{|\det H|}}')
eq(r'I(j)=\mathcal{N}(H)\exp\left[-\frac{i}{2\hbar}j^{\mathrm{T}}H^{-1}j\right]')
p('Die Signaturphase ist hier bereits enthalten. Alternativ gilt exp(iπr/4) exp(−iπn₋/2). Ein weiterer Morse-/Maslov-Faktor darf nicht dieselbe Phase doppelt zählen. Ein anderes Integrationsmaß verlangt dessen zusätzliche Faktoren.')
p('Unbeschränkte Nullachsen erzeugen distributionelle Deltafaktoren oder bei verschwindender Quelle ein formales Volumen. Kompakte Nullachsen geben Fourier-/Volumenfaktoren. Eine Eichquotientierung benötigt eine eigenständige Begründung.')
h('Ein Feldprofil ist keine Wellenfunktion')
eq(r'H_{\rm eff}v_k=\lambda_k W_bv_k')
p('Die Vektoren vₖ beschreiben Feldprofile auf Randelementen. Ein Besetzungszustand Ψₙ[φ] ist dagegen eine Funktion des gesamten Konfigurationsraums. Für |0⟩ und |1⟩ braucht es zusätzlich eine positive Zustandswahl bzw. Polarisation und eine begründete Quantisierung.')
p('Eine indefinite Raumzeit-Hesse-Matrix ist keine positive Oszillatorsteifigkeit. Der Schurblock eines ganzen Patches liefert außerdem nicht automatisch getrennte lokale Ein- und Ausgangsbasen.')
h('Zustände zählen und vergleichen')
p('Zwei räumliche Moden mit jeweils nₖ=0,1 ergeben vier Fockzustände pro Geometrie/Stratum, also 16 Gesamtzustände. Acht Zustände erfordern eine weitere Auswahl, etwa Vakuum plus genau eine Einteilchenanregung. Modenüberlappungen benötigen eine explizite Identifikation der jeweiligen Feldräume und Maße.')

page('4 | Ein korrigierter Test für Stratumkopplung')
p('Voraussetzungen: Wirkung, Historienklasse, Maß und Gebiet sind unter der gemeinsamen Spiegelung Φ→−Φ invariant. Es gibt keine ungerade Quelle oder asymmetrische Präparation. Ein- und Ausgangspaket besitzen Paritäten p_i,p_f=±1. Die Staubstrata werden durch diese Spiegelung nicht vertauscht.')
eq(r'B^{fi}_{s_fs_i}=p_fp_i B^{fi}_{s_fs_i}')
eq(r'p_fp_i=-1\quad\Longrightarrow\quad B^{fi}_{s_fs_i}=0')
p('<b>Folge:</b> Der Vakuum-zu-Einteilchen-Kandidat ist unter diesen Bedingungen exakt null, auch wenn gerade Stratum-Mischblöcke koppeln. Das ist Gesamtfeldparität, keine automatisch separat erhaltene Parität jeder einzelnen Mode.')
h('Paritätserlaubte erste Kandidaten')
table([['Kandidat','Was er prüfen könnte'],['0,+ mit Vakuum → Vakuum','Gemischte Randamplitude ohne ungerade Anregung'],['0,+ mit Einteilchen → Einteilchen','Gemischte Amplitude im ungeraden Paritätssektor'],['0,+ mit Vakuum → Zweiquanten','Gerade Anregung; benötigt erweiterten Kontrollraum']],[235,260])
p('Diese Einträge sind noch nicht berechnet. Eine leere Historienfaser erzwingt null; eine nichtleere Faser garantiert wegen möglicher Auslöschung keinen Nichtnullwert. Ein numerischer Nichtnull-Zeuge braucht einen Fehlerbereich, der den Ursprung ausschließt.')
h('Mischung und Materievermittlung getrennt nachweisen')
p('Ein Nichtnullblock belegt zunächst nur eine Mischamplitude der deklarierten Familie. Für eine Zuschreibung an Materie braucht es zusätzlich einen aus derselben Wirkung definierten Entkopplungsvergleich bei unveränderten Randpaketen und Maßen. Ein einzelner Nullwert beweist keine Superselektion; das Dichte-Nullatom bleibt vom Materievakuum verschieden.')

page('5 | Randvertrag, Maß und nächste Rechnung')
p('Die gemeinsame Summe muss dieselben Historien, Staubvariablen, Feldzustände und Randmaße verwenden. Die Feldintegration gehört innerhalb dieser Summe; eine Faktorisierung in einen fertigen Geometriekern und eine universelle Materiematrix ist nicht vorausgesetzt.')
h('Gewichte nicht doppelt anwenden')
p('Der bisherige Orbitwert 1/(2ᵐ|Aut(C,σ)|) enthält bereits den integrierten Dichte-Stratumfaktor der stratumskonstanten Hilfsbasis. Derselbe Faktor darf nicht nochmals über das vollständige Dichtemaß eingebracht werden. Für dν=½δ₀+½1_(0,1)dw haben konstante Indikatoren zwar beide Norm²=½; das positive Randpaket f(w)=w besitzt dagegen Norm²=1/6.')
h('Konvention und Vollständigkeit')
eq(r'\widehat{A}=G_{\rm out}^{1/2}A G_{\rm in}^{-1/2},\qquad \widehat{B}=G_{\rm out}^{-1/2}B G_{\rm in}^{-1/2}')
eq(r'B=G_{\rm out}A,\qquad B_{21}=B_2G_{\rm mid}^{-1}B_1')
p('Die zweite Kompositionsformel setzt einen vollständigen gemeinsamen Zwischenraum voraus. Eine Trunkierung fügt einen Projektor ein; Leckage und Änderungen behaltener Einträge sind separat zu prüfen. Bei nichtlokaler Wirkung ist auch die Vollständigkeit des Randkragens offen.')
h('Elf erforderliche Eingaben')
p('open_inputs.json konkretisiert: Historien-/Randträger; Feldinhalt; Wirkung/Hesse-Matrix; Quantenzustand; Randpakete und Maße; Integrations-/Nullraumvorschrift; Gruppengewicht; Kernkonvention; Parität; Fehlerbudget; Entkopplungsvergleich.')
p('<b>Umfang:</b> 64 komplexe Einträge je Phase; bei z=1,−1,i insgesamt 192. Kontrollmoden und weitere Parameter erhöhen diesen Umfang.')
h('Reproduktion und Quellen')
p('25 exakte Kontrollen; zwei Ergebnisdateien werden isoliert bytegleich reproduziert. Ausführung: python analyze.py; python verify.py. Keine physikalische Feldquadratur wurde ausgeführt. Quellen und Git-Hashes stehen in provenance.json.','SmallD')
p('Projektbasis: thomasmgfeller/x6-spectral-astrolabium, Main fdf1deb6ac071056d533a0937e21c238f42b2974. Zustandsraum-, Variations- und Randkern-Herleitungen sowie der exakte Verklebungscode sind unverändert eingebettet.','SmallD')
p('Literatur: [L1] Aslanbeigi et al., arXiv:1403.1622; [L2] Sorkin, arXiv:1107.0698; [L3] Nomaan X, arXiv:2306.04800. Die Literatur qualifiziert keine hier bereits hergeleiteten physikalischen Randzustände. Vollständige Links und Aussagen in DERIVATION.md.','SmallD')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#bfd1d7'));c.line(45,44,550,44)
    c.setFont('DejaVu',7.2);c.setFillColor(colors.HexColor('#526772'))
    c.drawString(45,32,'CST-DUST | Materieblock-Vorprüfung v0.1 | 11.11.2026 | Physik: HOLD')
    c.drawRightString(550,32,str(doc.page))
class StableCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs): kwargs['invariant']=1;super().__init__(*args,**kwargs)
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),leftMargin=45,rightMargin=45,
                     topMargin=42,bottomMargin=58,title='CST-DUST Materieblock-Vorprüfung v0.1',
                     author='Thomas Gfeller / CST-DUST Arbeitsartefakt')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=StableCanvas)
print(OUT)
