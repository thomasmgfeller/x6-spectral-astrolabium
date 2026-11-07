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
OUT=ROOT/'CST_DUST_Stratumwechsel_Randkopplung_Zustandsauswahl_v0_1.pdf'
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

p('CST-DUST<br/>Stratumwechsel, Randkopplung<br/>und Zustandsauswahl','title')
p('Analytischer Prüfbericht v0.1 · 7. November 2026','sub')
p('<b>Ergebnis:</b> Ein mathematisch konsistenter Übergang zwischen dem Dichte-Nullatom und dem kontinuierlichen Dichteanteil lässt sich konstruieren. Die vorhandene Staubwirkung wählt diese Kopplung jedoch nicht aus. Die noch fehlende physikalische Entscheidung ist damit genauer bestimmt.')
table(['Prüfung','Ergebnis'],[
('Nur Bewegung innerhalb der Dichtestrata','Auch diese größere Detektorklasse hat zum erklärten kohärenten Ziel mindestens 1/2 universellen Operatornormfehler.'),
('Zusätzliche Kopplung an eine Randspur','Selbstadjungierter Operator, Domäne, Normfluss und positive Spektrallücke sind analytisch angegeben.'),
('Auswahl des kohärenten Zustands','Zwei zulässige Randvorzeichen wählen bei festem Ziel orthogonale Zustände aus. Die Theorieauswahl fehlt.'),
('Vollständiger Raum und vorhandene Wirkung','Unkontrollierte Uhrmoden verursachen Fehler eins. Ein zusätzliches Wirkungspotential zerstört die konstante Eigenmode.')],[178,327])
h('Was dieser Schritt leistet')
p('Die notwendige Historienmischung ist in eine konkrete mathematische Domänen- und Randfrage übersetzt. Eine Familie mit wohldefinierter Quantenevolution existiert; ihre Parameter, ihre physikalische Bedeutung und ihr Detektor bleiben zusätzliche Annahmen.')
h('Reichweite')
p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein hergeleiteter CST-Detektor, keine gravitative Rückwirkung und kein Bounce-Nachweis. Der Rand der Dichtevariable ist kein nachgewiesener räumlicher Rand. Das Nullatom ist kein bereits definierter Fock-Vakuumzustand.')
p('Kein n=5-Produktionslauf und keine kostenpflichtige Rechenleistung. Die kleinen exakten Kontrollrechnungen ersetzen keine physikalische Auswahl.','small')
p('Basis: Main nach PR 262, Commit 4ed1a338f875172f8eb92798e8a8e9046a126f5f. Vollständige Beweise, sechs gepinnte Quellen und Reproduktionscode stehen im Prüfpaket.','small')

page('1 · Von der Wirkung zur nötigen Kopplung')
p('Die geerbte Materiewirkung koppelt Uhr-Feldwerte an verschiedenen Ereignissen. Ihr Hessian wirkt auf diesen Feldkomponenten. Er ist damit noch kein Operator zwischen vollständigen Historien im verwendeten L²-Raum.')
f('S_d = -1/2 Σ_x w_x - 1/4 Σ_(y≺x) w_x B_xy (T_x-T_y)^2\nIm n=1-Sektor: S_d(x,w) = -w(1/2 + 4 h² x²)')
p('Auf dem bisherigen Historienraum wirkt diese reelle Funktion als Multiplikation M_S. Die zugehörige Phase ist diagonal. Eine Ableitung nach einer Wellenfunktionskoordinate, ihr Definitionsbereich und ihre Quantisierungsregel sind damit nicht festgelegt.')
h('Die Untergrenze gilt für eine größere Klasse')
p('Zerlege H=H_a⊕H_c in Dichte-Nullatom und kontinuierlichen Anteil. Beide enthalten weiterhin alle Uhrmoden. Ein Effekt E darf innerhalb jedes Blocks beliebig nichtdiagonal sein; gefordert ist nur [E,Π_a]=0.')
f('ψ_± = (a ± c)/√2,   P_+ = |ψ_+><ψ_+|\n<ψ_+,Eψ_+> = <ψ_-,Eψ_-> = q\n||E-P_+|| ≥ max(1-q,q) ≥ 1/2')
p('Die Grenze ist scharf: E₀=(|a&gt;&lt;a|+|c&gt;&lt;c|)/2 erreicht sie. Zeigerkopplungen und adaptive Instrumente, die beide Strata erhalten, können die beiden relativen Vorzeichen nicht unterscheiden. Aus einem blockdiagonalen Eingang erzeugen sie keine Kreuzkohärenz.')
h('Was daraus nicht folgt')
p('Innerhalb eines Stratums kann eine solche Auslese durchaus Phasen erkennen. Es wird daher keine allgemeine Phasenblindheit behauptet. Der Satz setzt beide kohärenten Testzustände im Vergleichsraum voraus. Spätere physikalische Constraints können einen neuen Vergleich erfordern.')
p('Bei unbeschränkten Generatoren müssen die Strata die gesamte unitäre Gruppe reduzieren. Ein formaler Kommutator auf wenigen Testfunktionen ist kein Ersatz für die Domänenprüfung.','small')

page('2 · Eine zusätzliche Randform mit Normfluss')
p('Nach einer angegebenen unitären Umgewichtung ist der Dichteraum C⊕L²(0,1). Der Atomwert a und die stetige Funktion f sind zunächst unabhängig. Ein Randwert f(0) wird erst durch H¹-Regularität sinnvoll.')
f('Q = C ⊕ H¹(0,1),   κ>0, λ≥0, s∈{-1,+1}\nq_s[a,f] = κ ∫₀¹ |f′|² dw + λ |a-s f(0)|²')
p('Diese Form wird ausdrücklich zusätzlich gewählt. Ihre Formnorm ist zur Norm auf C⊕H¹ äquivalent: Die Ableitung wird kontrolliert, und die Randspur ist auf H¹ stetig. Die Form ist dicht definiert, abgeschlossen und nichtnegativ. Der Darstellungssatz liefert einen selbstadjungierten Operator zu genau dieser Form.')
f('A_s(a,f) = (λ(a-s f(0)), -κ f″)\nf ∈ H²(0,1),   f′(1)=0,   κ f′(0)=λ(f(0)-s a)')
p('Die Randbedingungen folgen aus partieller Integration. Für λ=0 bleiben Atom und stetiger Anteil getrennt. Für λ&gt;0 sind sie verbunden: Die Atomprojektion erhält die Operatordomäne im Allgemeinen nicht.')
h('Wahrscheinlichkeit geht über die Randkopplung')
f('j(w) = (2κ/hbar) Im(conj(f) f′)\nj(1)=0,   j(0)=(2sλ/hbar) Im(conj(a) f(0))\nd|a|²/dt = -j(0),   d∫|f|²/dt = j(0)')
p('Für reguläre Lösungen heben sich Atomverlust und kontinuierlicher Zufluss exakt auf. Für allgemeine Hilbertraumzustände folgt die Normerhaltung aus Selbstadjungiertheit.')
p('<b>Zusatzmodell:</b> Dieser Fluss ist ein Wahrscheinlichkeitsfluss zwischen Dichte-Records. Er ist kein abgeleiteter räumlicher Staubmassenstrom. κ, λ, s, Kontrollzeit und die Randbedingung am Regulator w=1 sind physikalisch nicht ausgewählt.','small')

page('3 · Zustandsauswahl und unbeschränkte Randspur')
p('Bei λ&gt;0 verschwindet die Form genau dann, wenn f konstant ist und a=sf(0). Der Grundraum ist eindimensional. Bei λ=0 sind die beiden konstanten Komponenten unabhängig.')
table(['Randwahl','Grundraum','Wert des festen Ziels P_+'],[
('λ=0','Zweidimensional','Keine eindeutige Auswahl'),
('λ>0, s=+1','ψ_+=(1,1)/√2','1'),
('λ>0, s=-1','ψ_-=(-1,1)/√2','0')],[133,196,176])
p('Beide Vorzeichen sind mit Positivität, Normerhaltung und reellen Koeffizienten vereinbar. Werden Ziel und Instrument bei einem unitären Vorzeichenwechsel mitgeführt, ist dies dagegen nur ein Darstellungswechsel. Der Vergleich oben hält den Zielvertrag fest.')
h('Eine kontrollierte Spektrallücke')
f('Für u⊥ψ_s: ||u||² ≤ |a-s f(0)|² + (1/2)||f′||²\nDaraus: Δ_w ≥ min(λ,2κ) > 0')
p('Die Schranke folgt aus einer Spurabschätzung und einem Doppelintegral für die Varianz von f. Die Formeinbettung ist kompakt; der kontinuierliche Operator ist spektral wohldefiniert. Ein Grundzustand allein implementiert jedoch weder einen Detektor noch seine Präparation.')
h('Das frühere beschränkte Mischbudget gilt hier nicht automatisch')
p('Die Randspur f(0) ist in der L²-Norm unbeschränkt, und die Operatordomäne ändert sich mit λ. Daher ist λ nicht einfach in das frühere Budget ∫||V||dt/hbar einzusetzen. In den endlichen gewichteten Kontrollmatrizen beträgt die Norm des Randzusatzes λ(m+1), die seines reinen Blockübergangs λ√m.')
p('Diese Zunahme mit der Zellzahl m ist kein physikalischer Divergenznachweis. Sie zeigt, dass das beschränkte Budget keine uniforme Zertifizierung dieser Formfamilie liefert. Eine eigene zeitabhängige Fehlerkontrolle bleibt erforderlich.','small')

page('4 · Uhrmoden und Rückbindung an die Wirkung')
h('Die vollständige Uhrvariable mitprüfen')
p('Auf L²(x)⊗H_w hat I_x⊗A_+ unendlich viele Nullmoden: Jede Uhrfunktion kann mit der Dichtegrundmode kombiniert werden. Der zugehörige Filter ist daher nicht der verlangte Rang-eins-Effekt.')
f('E_Dichte = I_x ⊗ P_w,   E_Ziel = P_x ⊗ P_w\n||E_Dichte-E_Ziel|| = 1')
p('Ein zusätzlich gewählter Neumann-Operator A_x=−κ_x∂²_x mit κ_x&gt;0 reduziert die Grundmode auf die konstante Uhrfunktion. Der Tensoroperator hat eine Lücke mindestens min(π²κ_x, λ, 2κ). Diese Ableitung nach einem historischen Uhrrecord ist eine weitere Modellannahme, keine hergeleitete CST-Zeitentwicklung.')
h('Ein Wirkungspotential erhält die Zielmode nicht')
p('Auch die Identifikation einer Wirkung mit einem Hamiltonpotential wäre zusätzlich zu begründen. Für den ausdrücklich nur diagnostischen Ansatz H_η=A_full+ηM_S lässt sich ihre Konsequenz exakt prüfen.')
f('||(I-P_+) H_η ψ_+||² = η² Var(S_d)\nVar(S_d) = 5/192 + 5h²/36 + 19h⁴/45 > 0')
p('Bei η≠0 ist der konstante Zielzustand kein Eigenzustand dieses Operators mehr. Die Formel folgt aus dem ursprünglichen Atom-/Gleichmaß und der gepinnten n=1-Wirkung; es wird kein Integral über große Kausalsets benötigt.')
table(['Prüffrage','Befund'],[
('Ist die Dichtegrundmode ausreichend?','Nein; Uhrmoden bleiben ohne weitere Dynamik unkontrolliert.'),
('Wählt die alte Wirkung automatisch den konstanten Grundzustand?','Nein; selbst der zusätzliche Potentialansatz besitzt ein exakt positives Eigenresiduum.'),
('Ist dadurch jede physikalische Auslese ausgeschlossen?','Nein; geprüft sind die angegebenen Ziel- und Hamiltonannahmen.')],[215,290])

page('5 · Evidenz und nächste physikalische Entscheidung')
result=json.loads((ROOT/'results/verification.json').read_text())
table(['Exakte Kontrolle','Umfang'],[
('Blockerhaltende Effekte',result['block_effect_controls']),
('Gewichtete Randmatrizen / Cayley-Unitaritäten','72 / 72; davon 54 gekoppelte Fälle'),
('Green-Identitäten / Flussbilanzen','216 / 72'),
('Uhrmoden / Wirkungspunkte / Residualfälle','6 / 45 / 9'),
('Negativkontrollen / Nachrechnung','7 zurückgewiesen / 4 Dateien bytegleich')],[290,215])
p('Die allgemeinen Sätze beruhen auf den ausgeschriebenen Beweisen. Die kleinen Matrizen sind endliche Analoga ohne hier zertifizierten kontinuierlichen Konvergenzfehler. Die rationale Cayley-Abbildung ist genau unitär, aber keine exakt ausgewertete Zeitexponentialfunktion. Keine externe Replikation oder Beweisassistentenprüfung.','small')
h('Reproduktion')
f('python3 -B verify_package.py\npython3 -B replay.py')
p('Python-Standardbibliothek genügt. DERIVATION.md enthält die Beweise, selection_contract.json die Zusatzannahmen und die noch offenen Entscheidungen.','small')
h('Der nächste Kandidat braucht eine physikalische Auswahl')
p('<b>Zuerst ist zu entscheiden, ob die physikalische Quantenalgebra kohärente Übergänge zwischen Dichte-Nullatom und positivem Stratum überhaupt erlaubt.</b> Bei einer echten Superselektion muss der Zielvertrag geändert werden. Andernfalls müssen Übergangsoperator, Domäne, Randwahl und kausale Bedeutung aus der Materie-/Randdynamik begründet werden. Danach folgen Präparation, vollständiges Messinstrument und Rückwirkung.')
p('Die Randform dieses Pakets ist mathematisch konsistent, physikalisch nicht ausgewählt. Alle acht physikalischen Gates bleiben HOLD. Weitere n=5-Feldintegrale entscheiden diese Definitionsfrage nicht.','small')
h('Primärquellen und mathematischer Bezug')
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/262" color="#087E8B">Projektbasis PR 262</link>; <link href="https://radon.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe2.pdf" color="#087E8B">Teschl, §2.3, Satz 2.14</link> (Darstellung abgeschlossener Formen); <link href="https://arxiv.org/abs/0909.0944" color="#087E8B">Johnston 2009</link> und <link href="https://arxiv.org/html/2402.08555v2" color="#087E8B">Albertini et al. 2024, §2.2</link> (Feldquantisierung auf Kausalsets). Eine Abbildung ihrer Feldalgebren auf den hier erklärten Staub-Historienraum wurde nicht hergeleitet.','small')

def footer(c,doc):
    c.setStrokeColor(TEAL);c.setLineWidth(.5);c.line(45,42,550,42)
    c.setFillColor(NAVY);c.setFont('DV',7)
    c.drawString(45,30,'CST-DUST · Stratumwechsel / Randkopplung / Zustandsauswahl · v0.1')
    c.drawRightString(550,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(595.276,841.89),rightMargin=45,leftMargin=50,topMargin=48,bottomMargin=60,
    title='CST-DUST: Stratumwechsel, Randkopplung und Zustandsauswahl v0.1',author='Thomas Gfeller · CST-DUST research')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
