"""Build the research report and its scientific plot from frozen results."""
from pathlib import Path
from io import BytesIO
import json,math,re
from flint import arb,acb,ctx
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties,findfont
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from states import STATES,ORIGINAL,label

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'CST_DUST_Reduktion_Verklebung_v0_1.pdf'
DATA=json.loads((ROOT/'results/reduction.json').read_text());GLUE=json.loads((ROOT/'results/gluing.json').read_text())
NAVY=colors.HexColor('#18334C');TEAL=colors.HexColor('#087E8B')
pdfmetrics.registerFont(TTFont('DejaVu',findfont(FontProperties(family='DejaVu Sans'))))
pdfmetrics.registerFont(TTFont('DejaVuBold',findfont(FontProperties(family='DejaVu Sans',weight='bold'))))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVuBold',italic='DejaVu',boldItalic='DejaVuBold')
BODY=ParagraphStyle('body',fontName='DejaVu',fontSize=9.6,leading=14,spaceAfter=8,textColor=NAVY)
SMALL=ParagraphStyle('small',parent=BODY,fontSize=8,leading=11,spaceAfter=6)
TINY=ParagraphStyle('tiny',parent=SMALL,fontSize=7.4,leading=10)
H1=ParagraphStyle('title',parent=BODY,fontName='DejaVuBold',fontSize=24,leading=29,spaceAfter=15)
H2=ParagraphStyle('section',parent=BODY,fontName='DejaVuBold',fontSize=16,leading=21,spaceAfter=13)
H3=ParagraphStyle('sub',parent=BODY,fontName='DejaVuBold',fontSize=11,leading=15,spaceBefore=10,spaceAfter=7)
KICK=ParagraphStyle('kick',parent=SMALL,textColor=TEAL,fontName='DejaVuBold',spaceAfter=12)
story=[]
def p(text,style=BODY):story.append(Paragraph(text,style))
def eq(tex,maxwidth=164*mm):
 tex=re.sub(r'\\frac(\d)(\d)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',tex)
 tex=re.sub(r'\\frac(\d)',lambda m:r'\frac{'+m[1]+'}',tex)
 buf=BytesIO();math_to_image('$'+tex+'$',buf,prop=FontProperties(size=14),dpi=220,format='png',color='#18334C')
 buf.seek(0);im=PILImage.open(buf);w,h=im.size;scale=min(72/220,maxwidth/w)
 obj=Image(buf,width=w*scale,height=h*scale);obj.hAlign='CENTER';story.extend([Spacer(1,3*mm),obj,Spacer(1,4*mm)])
def table(rows,widths,compact=False):
 converted=[[Paragraph(str(x),TINY if compact else SMALL) for x in row] for row in rows]
 t=Table(converted,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5 if compact else 7),('BOTTOMPADDING',(0,0),(-1,-1),4 if compact else 5),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F3F4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F7FA')])]))
 story.extend([t,Spacer(1,4*mm)])
def page(k,title):
 if story:story.append(PageBreak())
 p('CST-DUST  /  SCHRITT 5  /  '+k,KICK);p(title,H2)
def component(record):
 return [f'{float(arb(record[axis]).mid()):+.12f}'.replace('-','−') for axis in ('real','imag')]

# Scientific plot: omitted finite packet coefficients, no probability scale.
(ROOT/'figures').mkdir(exist_ok=True)
rows=[]
names={'0:20':'0, Skalar 20','0:02':'0, Skalar 02','+:20':'+, Skalar 20','+:02':'+, Skalar 02',
       'Delta:00':'Δ, Skalar 00','Delta:20':'Δ, Skalar 20','Delta:02':'Δ, Skalar 02',
       'A:11':'A, korrelierter Skalar 11','+:00:clock2':'+, Skalar 00, Uhr χ₂'}
for key in DATA['omitted_labels']:
 rec=DATA['column'][key]
 if rec['classification']=='EXACT_PARITY_ZERO':continue
 z=rec['certified_ball'];value=math.hypot(float(arb(z['real']).mid()),float(arb(z['imag']).mid()))
 color='#087E8B' if key.startswith(('0:','+:')) and key!='+:00:clock2' else ('#C08038' if key.startswith('Delta') else '#54708C')
 rows.append((key,value,color))
rows.sort(key=lambda x:x[1])
fig,ax=plt.subplots(figsize=(7.6,4.0),layout='constrained')
ax.barh([names[k] for k,v,c in rows],[v for k,v,c in rows],color=[c for k,v,c in rows],height=.62)
for i,(_,v,_) in enumerate(rows):ax.text(v+.0008,i,f'{v:.5f}',va='center',fontsize=8,color='#18334C')
ax.set_xlim(0,.075);ax.set_xlabel('Betrag des ausgelassenen Matrixelements',fontsize=9)
ax.tick_params(axis='both',labelsize=8);ax.spines[['top','right','left']].set_visible(False);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
fig.savefig(ROOT/'figures/omitted_components.png',dpi=240);plt.close(fig)

page('ERGEBNIS','Die Vierzustandsbeschreibung schließt nicht')
p('Zustandsreduktion<br/>und Verklebung',H1)
p('Der bisherige Mischblock bleibt gültig. Die Prüfung zusätzlicher Zustände zeigt jedoch einen erheblichen ausgelassenen Anteil, und die Verklebung der lokalen Teilwirkungen verliert konkrete Intervallinformationen.')
eq(r'r_{15\leftarrow4}=0.102348630703\ \pm\ 10^{-12}')
eq(r'\frac{r_{15\leftarrow4}}{\Vert v_{15}\Vert_2}=0.367087702939\ \pm\ 10^{-12}')
p('<b>36,7 % der Amplitudennorm innerhalb der untersuchten 15er-Ausgangsspalte fehlen im Vierzustandsraum.</b> Die Zahl ist keine Wahrscheinlichkeit und keine obere Schranke für den gesamten unendlichen Zustandsraum.')
table([['Prüffrage','Befund'],['Ändert eine größere Basis den alten Mischblock?','Nein, bei identischen Zuständen und identischem Kern exakt unverändert.'],['Sind ausgelassene Zustandsanteile vorhanden?','Ja, neun zusätzliche Komponenten sind zertifiziert nicht null.'],['Verkleben die lokalen Teilwirkungen zum gemeinsamen Kern?','Im erklärten Achtpunkt-Nullatomtest nein; fünf Intervallterme fehlen.'],['Gibt es bereits eine volle L²-Fehlergrenze?','Nein; die entkoppelte Referenz besitzt sogar eine ungedämpfte Ausgangsrichtung.']],[76*mm,88*mm])
p('32 Prüfungen bestanden; primäre Rechnung und unabhängige Kontrollen stimmen überein.',H3)
p('Geltungsbereich: endliches 33-Historien-Kontrollensemble und separat deklarierter Achtpunkt-Verklebungstest. Physikalischer CST-Kern NOT_CONSTRUCTED; alle acht physikalischen Gates HOLD.',SMALL)

page('01','Ein gemeinsames Maß für alle fünfzehn Zustände')
eq(r'd\mu_A=\frac12\prod_{j=1}^2d\lambda(t_j)d\nu(r_j)dq_j,\qquad\Psi=\sqrt{2}\,d\,h\,\chi')
p('Uhren bleiben in [−1,1], dλ=dt/2; jede Dichte besitzt die Mischung dν=δ₀/2+dr/2 auf (0,1). Die gesamte Punktausstattung wird gemeinsam vertauscht. Skalarfelder laufen über die reelle Linie.')
p('Maskenfolge 00,10,01,11. „+“ bleibt die kohärente Überlagerung aller drei positiven Belegungen; Δ ist die bisher ausgelassene Einfach-/Doppeldichterichtung.')
eq(r'd_0=(2,0,0,0),\quad d_+=\frac{2}{\sqrt{3}}(0,1,1,1)')
eq(r'd_\Delta=\sqrt{\frac23}(0,1,1,-2),\quad d_A=\sqrt{2}(0,1,-1,0)')
table([['Skalarmodus','Polynom vor h₀₀','Vertauschung'],['00','1','gerade'],['10','√2 q_s','gerade'],['20','(2q_s²−1)/√2','gerade'],['02','(2q_a²−1)/√2','gerade'],['01','√2 q_a','ungerade'],['11','2q_s q_a','ungerade']],[34*mm,90*mm,40*mm],compact=True)
p('Zwölf Produkte aus (0,+,Δ) und (00,10,20,02), dazu (A,01) und (A,11), ergeben 14 invariante Zustände. Die antisymmetrische Dichte wird nur mit einer ebenfalls antisymmetrischen Feldmode kombiniert.')
eq(r'\chi_2=\sqrt{\frac52}\,[P_2(t_1)+P_2(t_2)],\qquad G_{15}=I_{15}')
p('Der zusätzliche Zustand (+,00)χ₂ prüft eine nichtkonstante Uhrform. Alle 15 Zustände sind exakt normiert und orthogonal. Höhere Feldmoden und weitere Uhr-/Dichteprofile bleiben offen. Die Indizes sind Paketindizes, keine hergeleiteten Teilchenzahlen.',SMALL)

page('02','Die erweiterte Ausgangsspalte')
p('Eingang: normierter Zustand (0,00). Alle 33 bisherigen AA-Historien, Gewichte 1/33, κ=1, μ=0 und die ursprüngliche gekoppelte Wirkung bleiben fest. Es wird diese Spalte berechnet, keine vollständige 15×15-Matrix.')
tab=[['Ausgang','Realteil','Imaginärteil']]
for state in STATES:
 key=label(state);display=key.replace('Delta','Δ').replace(':clock2',' · χ₂').replace(':',' / ')
 if key in ORIGINAL:display+=' *'
 tab.append([display]+component(DATA['column'][key]['certified_ball']))
table(tab,[48*mm,58*mm,58*mm],compact=True)
p('* Bestandteil des bisherigen Vierzustandsraums. Fehler jedes gerundeten Real-/Imaginärteils höchstens 10⁻¹². Die vier ungeraden Übergänge sind exakte Paritätsnullen, keine numerisch kleinen Näherungen.',SMALL)
p('Der bisherige Atom-zu-Positiv-Eintrag −0.155730245646+0.132674294297 i bleibt unverändert. Die neuen Zeilen machen bisher unberücksichtigte Komponenten sichtbar; sie verteilen den alten Eintrag nicht nachträglich um.',SMALL)

page('03','Welche Zustände fehlen?')
story.append(Image(str(ROOT/'figures/omitted_components.png'),width=164*mm,height=86.3*mm))
p('Neun zusätzliche Nichtnullkomponenten. Die Darstellung zeigt Beträge von Paketmatrixelementen; numerische Fehler sind kleiner als die sichtbare Strichbreite. Vollständige Einschließungen stehen in results/reduction.json.',SMALL)
eq(r'r_{15\leftarrow4}^{\,2}=\sum_{j\notin P_4}|M_{j,0:00}|^2')
table([['Größe im getesteten Raum','Zertifizierter Wert, gerundet'],['Norm der 15er-Spalte','0.278812474196 ± 10⁻¹²'],['Norm des ausgelassenen Anteils','0.102348630703 ± 10⁻¹²'],['Relativer Anteil an dieser Spaltennorm','0.367087702939 ± 10⁻¹²']],[87*mm,77*mm])
p('Bereits die geraden Feldmoden 20 und 02 tragen deutlich bei. Hinzu kommen die aufgelöste Dichte Δ, die erlaubte Dichte-/Feldkorrelation A×11 und das Uhrpaket χ₂.')
p('<b>Für den vollständigen Raum ist dies eine untere Schranke, sofern die gekoppelte Ausgangswelle dort überhaupt in L² liegt.</b> Eine obere globale Restschranke folgt nicht. Eine Vierzustandsapproximation dieser Spalte mit absolutem Fehler unter 0.10234 ist bereits durch die getesteten Paarungen ausgeschlossen.')

page('04','Fehlerbudget und Rechenkontrollen')
p('Alle Dichten einschließlich ihrer Atome werden analytisch integriert. Die inneren und äußeren Skalarintegrale sind Gaußintegrale mit exakt berechneten polynomialen Momenten. Nur die fünf kompakten Uhrintegrale benötigen Quadratur.')
eq(r'Q=I-iK,\quad V=Q^{-1},\quad A_{20}=\frac{A_{00}}{\sqrt{2}}(V_{22}+2V_{23}+V_{33}-1)')
eq(r'A_{02}=\frac{A_{00}}{\sqrt{2}}(V_{22}-2V_{23}+V_{33}-1),\quad A_{11}=A_{00}(V_{22}-V_{33})')
table([['Fehlerquelle / Kontrolle','Behandlung'],['Primäre Uhrquadratur','48 Knoten je Achse; analytische Bernsteinellipsen-Schranke; maximaler komplexer Fehler &lt;1.60·10⁻¹⁷.'],['Arithmetik','192 Bit Arb/Acb; Knoten, Gewichte, Wurzeln, Phasen, Inversen und Momente eingeschlossen.'],['Dichte-/Skalarintegration und Abel-Grenzwert','Analytisch; keine numerische Extrapolation.'],['Kontrollrechnung','56 Knoten, 224 Bit; überlappende Intervalle, analytischer Fehler &lt;2.44·10⁻²².'],['Unabhängiger Strukturtest','Direkte 5D-Float64-Rechnung aller 33 Historien bei acht Knoten; ohne Orbits und ohne Uhrkontraktion.'],['Darstellungsrundung','Alle Tabellenintervalle auf ±10⁻¹² je Komponente erweitert.']],[64*mm,100*mm])
p('Die Fehlerabschätzung wird aus Analytizität, positiven Gaußgewichten und Exaktheit bis Grad 2n−1 bewiesen. Der Unterschied zweier Quadraturregeln wird nicht als Fehlerbeweis verwendet.',SMALL)
p('32 Tests prüfen unter anderem Gram-Rang, Symmetrie, Masken, Phasenzweige, Momente, direkte Tensorrechnung, zusätzliche Restkomponenten, Intervallüberlappung, Wirkungsterme und Verklebungsnormierung.',SMALL)

page('05','Basisvergrößerung und andere Randpakete')
p('Eine Basisvergrößerung ändert das Matrixelement zwischen denselben beiden Zuständen nicht. Eine neue Paketbreite bezeichnet dagegen eine andere Präparation. Beide Fragen werden getrennt gerechnet.')
eq(r'\langle\varphi,K\psi\rangle=\langle\varphi,P_EKP_E\psi\rangle,\qquad\varphi,\psi\in\mathrm{ran}\,P_E')
p('Für den Atom-zu-Positiv-Übergang bleibt der Eingang unverändert. Nur die Breite des ausgehenden symmetrischen Skalargrundpakets wird geändert; die antisymmetrische Breite bleibt eins. Jedes Paket wird mit demselben Maß normiert.')
tab=[['Ausgehende Breite σ_s','Realteil','Imaginärteil']]
for name,key in [('1/2','sigma_s=1/2'),('1',None),('2','sigma_s=2')]:
 record=DATA['width_controls'][key] if key else DATA['column']['+:00']
 tab.append([name]+component(record['certified_ball']))
table(tab,[48*mm,58*mm,58*mm])
eq(r'\langle h_{00}^{(1)},h_{00}^{(\sigma_s)}\rangle=\sqrt{\frac{2\sigma_s}{1+\sigma_s^2}}<1\quad(\sigma_s=1/2,2)')
p('Die geänderten Breiten führen zu von null getrennten Amplitudenänderungen. Sie sind keine numerische Instabilität des alten Matrixelements und kein Abschneidefehler bei festem Zustand.')
p('Eine spätere physikalische Auswertung muss die Präparation der Randpakete und ihre Unsicherheiten festlegen. Der kleine numerische Quadraturfehler ersetzt diese Aufgabe nicht.',H3)

page('06','Was beim Verkleben über den Schnitt reicht')
p('Die gemeinsame Ordnung hat acht Punkte in den Schichten (2,1,2,1,2). Jeder frühere Schichtpunkt liegt vor jedem späteren. Beide Teilordnungen sind die bereits zugelassene AA-Historie 25500.')
table([['Teil','Punkte'],['Anfang / linkes Inneres','{0,1} / {2}'],['Gemeinsamer Schnitt','{3,4}'],['Rechtes Inneres / Ende','{5} / {6,7}'],['Linkes Gebiet L / rechtes Gebiet R','{0,1,2,3,4} / {3,4,5,6,7}']],[65*mm,99*mm])
p('Vor dem Vergleich werden die doppelt gezählten Schnittterme abgezogen: S_sew=S_L+S_R−S_S. Ein Faktor 2 gleicht das Schnitt-Quotientmaß an das gelabelte Innenmaß der gemeinsamen Rechnung an.')
table([['Fehlendes Paar','Intervallgröße','Koeffizient c'],['(0,5)','3','−8'],['(1,5)','3','−8'],['(2,5)','2','+16'],['(2,6)','3','−8'],['(2,7)','3','−8']],[70*mm,47*mm,47*mm],compact=True)
eq(r'F_4(C)=88,\qquad F_4(L)+F_4(R)-F_4(S)=72')
eq(r'\frac{\Delta S_\phi}{\hbar}=-\frac{\beta}{4}\sum_{(i,j)\in X}c_{ij}(q_j-q_i)^2')
eq(r'\frac{\Delta S_d}{\hbar}=-\frac{\beta}{4}\sum_{(i,j)\in X}c_{ij}r_j(t_j-t_i)^2')
p('Die gemischte Ableitung nach q₀ und q₅ beträgt −4β. Eine Korrektur nur aus den momentanen Schnittvariablen 3 und 4 kann diese Abhängigkeit nicht herstellen. Benötigt werden schnittübergreifende Intervall- und Feldinformationen.',SMALL)

page('07','Gemeinsamer Kern und lokale Teilwirkungen')
p('Der numerische Vergleich isoliert den nichtverschwindend gewichteten Stratumbeitrag mit allen acht Dichten am Nullatom. Alle Uhren werden integriert. Die äußeren Atom-/Grundpakete sind normiert; vier innere Skalarvariablen werden im Abel-Sinn integriert.')
eq(r'\frac14(\sqrt{2}\,2)^2\left(\frac12\right)^8=\frac1{128}')
table([['Innenblock H₀,II','Determinante','Signatur'],['Gemeinsame Wirkung','−17170','+2'],['Korrigierte Teilwirkungssumme','+1190','0']],[85*mm,42*mm,37*mm])
tab=[['Normierter Nullatombeitrag','Realteil','Imaginärteil']]
for title,key in [('Gemeinsame Wirkung','joint'),('Lokale Teilwirkungen','sewn_local_action'),('Differenz','difference')]:tab.append([title]+component(GLUE['kernel_comparison'][key]['certified_ball']))
table(tab,[62*mm,51*mm,51*mm],compact=True)
p('Fehler je gerundetem Real-/Imaginärteil höchstens 10⁻¹². Auch nach Entfernung der Gravitationsphasen bleibt der skalare Unterschied nicht null. Für äußere Felder null ist das Verhältnis der inneren Kernelbeträge exakt √(7/101) ≈ 0.263262.',SMALL)
p('Positive Kontrolle: dieselbe gemeinsame Wirkung',H3)
p('Die exakte Elimination zuerst von (2,5), danach von (3,4), ergibt dasselbe Schur-Komplement und dieselbe Determinante wie die gemeinsame Elimination. Die Teilsignaturen 0 und +2 liefern auch dieselbe Fresnelphase. Bei ε=1 und 1/7 bestätigen zwei Integrationsreihenfolgen und eine unabhängige Eigenphasenrechnung die Gleichheit.')
p('<b>Der Unterschied liegt in den fehlenden Wirkungstermen.</b> Die Gegenprobe betrifft diese feste Historie und den dichteaufgelösten Nullatombeitrag. Die vollständige 1089-Paar-Summe und alle positiven Achtpunkt-Dichtestrata wurden nicht ausgewertet.',SMALL)

page('08','Die noch offene Frage nach dem Operatorraum')
p('Die Existenz einzelner Gaußpaket-Matrixelemente genügt nicht, um den Kern als beschränkten Operator auf dem gesamten Rand-Hilbertraum zu behandeln. Die entkoppelte Referenz aus Schritt 4 liefert hier eine konkrete Gegenkontrolle.')
eq(r'K_{a_R,a_R}=\beta\frac{28}{11},\qquad K_{a_R,q_0}=K_{a_R,q_1}=K_{a_R,s_R}=0')
eq(r'g=G(t_R,r_R)F(q_{s,R})\exp\!\left(i\frac{\beta}{2}\frac{28}{11}q_{a,R}^2\right)')
p('Der ausgehende antisymmetrische Feldmodus ist eine ungedämpfte quadratische Phase. Sein Betrag hängt nicht von q_a ab. Der frühere zertifizierte Befund M₀≠0 zeigt, dass der Vorfaktor nicht fast überall null ist. Auf der ganzen reellen Feldachse folgt daher ∫|g|²dμ_A=∞.')
p('Jede endliche Hermite-Paketprojektion liegt in L². Ihr Fehler gegenüber dieser Referenzantwort kann keine endliche volle L²-Norm besitzen. Die Paarungen mit einzelnen Gaußpaketen bleiben trotzdem endlich. Für die gekoppelte Hauptwirkung wird diese Aussage hier weder bewiesen noch behauptet.')
p('Was eine obere Verklebungsfehlergrenze verlangen würde',H3)
p('Für einen orthogonalen Schnittprojektor P setze Q=I−P.',SMALL)
eq(r'PK_2K_1P-PK_2PK_1P=PK_2(I-P)K_1P')
eq(r'|\langle g,K_2QK_1f\rangle|\leq\Vert QK_2^\dagger g\Vert\,\Vert QK_1f\Vert')
p('Diese Identität und die Normschranke setzen geeignete Operatorbereiche voraus. Benötigt werden obere Schranken der vollständigen Restanteile sowie eine richtige Wirkungs- und Maßverklebung. Die nachgewiesenen Zusatzkomponenten sind dafür nur untere Schranken. Mehr Zwischenzustände können fehlende grenzüberschreitende Wirkungsterme nicht ersetzen.',SMALL)

page('09','Konkrete Lücken und reproduzierbare Evidenz')
table([['Bereich','Was dieser Schritt nachweist'],['Zustandsbeschränkung','Vier Zustände schließen die untersuchte Spalte nicht. n=2, Δ, Dichte-/Feldkorrelation und Uhrform liefern zusätzliche Nichtnullanteile.'],['Verklebung','Momentane Zweipunkt-Schnittdaten und lokale Teilwirkungen verlieren fünf konkret benannte Intervallkopplungen.'],['Voller Fehlerbegriff','Eine globale obere L²-Restschranke fehlt; die entkoppelte Referenz scheitert an einer ungedämpften Feldrichtung.'],['Weiterhin offen','Andere Eingangsspalten, höhere Moden, allgemeine Schnittdaten, physikalisches Skalarprodukt, Historiengewichte und unendliche CST-Summe.']],[52*mm,112*mm])
p('Der 15er-Raum ist ein geprüfter Ausbau, noch kein geschlossener Evolutionsraum. Für die Verklebung muss ein gemeinsames Einflussfunktional oder ein Randzustand mit ausreichender Gedächtnisinformation die fehlenden Abhängigkeiten bewahren, bevor innere Variablen getrennt integriert werden.')
p('32 Tests; vollständiger Offline-Replay',H3)
p('python verify.py prüft Dateiinventar, Hashes, sieben Herkunfts-Blobs, 32 Tests und wiederholt die primäre Rechnung, die exakte Zustandsprüfung und den Verklebungsvergleich. python verify.py --extended wiederholt zusätzlich die 56er-Rechnung und die unabhängige direkte 5D-Kontrolle. Die Verifikation überschreibt keine Ergebnisse.',SMALL)
p('Das Prüfpaket enthält vollständige Herleitung, Versuchsvertrag, 15er-Gram-Matrix, alle Orbitbeiträge, Fehlerintervalle, Wirkungsmatrizen, Grafik und Reproduktionscode. Python-FLINT 0.9.0, NumPy 2.3.5 und SymPy 1.14.0 sind festgehalten.',SMALL)
p('Herkunft und Quellen',H3)
p('Basis: Main d4cac775a044177e9d66d517c11c941cb812f0a6, PR #280–282. Exakte Pfade und Git-Blob-Werte: provenance.json. Ausführliche Beweise und alle Geltungsgrenzen: DERIVATION.md.',SMALL)
p('<link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/282" color="#087E8B">Projektbasis: zertifizierter AA-Mischblock</link><br/><link href="https://dlmf.nist.gov/18.3" color="#087E8B">NIST DLMF: Hermite-Orthogonalität</link><br/><link href="https://dlmf.nist.gov/18.12" color="#087E8B">NIST DLMF: erzeugende Funktionen</link><br/><link href="https://python-flint.readthedocs.io/en/latest/acb_mat.html" color="#087E8B">Python-FLINT: komplexe Ballmatrizen</link>',SMALL)
p('<b>Physikalischer CST-Kern NOT_CONSTRUCTED. Alle acht physikalischen Gates bleiben HOLD.</b> Eine Bewegungsgleichung, physikalische Stauberzeugung, Unitarität oder Singularitätsauflösung wird mit diesen endlichen Kontrollen nicht nachgewiesen.',SMALL)

def decorate(canvas,doc):
 canvas.saveState();canvas.setFillColor(NAVY);canvas.setFont('DejaVu',8)
 canvas.drawString(23*mm,280*mm,'CST-DUST  /  Zustandsreduktion und Verklebung  /  v0.1')
 canvas.setStrokeColor(TEAL);canvas.setLineWidth(.5);canvas.line(23*mm,276*mm,187*mm,276*mm)
 canvas.setFont('DejaVu',7);canvas.drawString(23*mm,13*mm,'11. November 2026  |  Endliche Kontrollmodelle; physikalische Gates HOLD')
 canvas.drawRightString(187*mm,13*mm,str(doc.page));canvas.restoreState()

if __name__=='__main__':
 SimpleDocTemplate(str(OUT),pagesize=(210*mm,297*mm),rightMargin=23*mm,leftMargin=23*mm,topMargin=31*mm,bottomMargin=24*mm,title='CST-DUST Zustandsreduktion und Verklebung v0.1',author='Thomas Martin Gfeller und Beiträge').build(story,onFirstPage=decorate,onLaterPages=decorate)
 print(OUT)
