#!/usr/bin/env python3
"""PDF summary and scientific plot; mathematical evidence is RESULTS.json."""
from pathlib import Path
from fractions import Fraction
import json
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle

ROOT=Path(__file__).resolve().parent; OUT=ROOT/'report'; OUT.mkdir(exist_ok=True)
RESULT=json.loads((ROOT/'results/RESULTS.json').read_text())
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf'),('DM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
INK='#163040'; MUTED='#536B78'; TEAL='#007F79'; PALE='#EDF5F4'; ORANGE='#AD4D2B'
styles={
 'body':ParagraphStyle('body',fontName='D',fontSize=10.1,leading=15,textColor=HexColor(INK)),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.7,leading=12.6,textColor=HexColor(MUTED)),
 'h2':ParagraphStyle('h2',fontName='DB',fontSize=14,leading=19,textColor=HexColor(INK)),
 'eq':ParagraphStyle('eq',fontName='D',fontSize=12,leading=19,textColor=HexColor(INK)),
 'table':ParagraphStyle('table',fontName='D',fontSize=9.2,leading=13,textColor=HexColor(INK)),
 'white':ParagraphStyle('white',fontName='DB',fontSize=9,leading=13,textColor=white),
}
W,H=595.28,841.89; M=47; CW=W-2*M
pdf=OUT/'Geglaettete_Intervallgewichte_Stabilitaetsbudget_v0_28.pdf'
c=canvas.Canvas(str(pdf),pagesize=(W,H),invariant=1)
c.setTitle('CSPP v0.28 - Geglättete Intervallgewichte und schärfere Stabilitätsbudgets')
c.setAuthor('CSPP Forschungsnotiz');page=0;y=0

def p(txt,style='body',gap=10):
    global y
    obj=Paragraph(txt,styles[style]);_,height=obj.wrap(CW,1000)
    if y-height<57: raise ValueError(('page overflow',page,txt[:50],y,height))
    obj.drawOn(c,M,y-height); y-=height+gap

def title(kicker,heading):
    global y,page
    page+=1;y=H-53
    c.setFillColor(HexColor(TEAL));c.setFont('DB',8.3)
    c.drawString(M,y,'CSPP / EIGENZEIT  ·  FORSCHUNGSNOTIZ 0.28  ·  01.11.2026');y-=37
    c.setFillColor(HexColor(MUTED));c.setFont('DB',9);c.drawString(M,y,kicker);y-=14
    obj=Paragraph(heading,ParagraphStyle('title',fontName='DB',fontSize=25,leading=30,textColor=HexColor(INK)))
    _,height=obj.wrap(CW,180);obj.drawOn(c,M,y-height);y-=height+20

def footer():
    c.setStrokeColor(HexColor('#DCE5E8'));c.line(M,43,W-M,43)
    c.setFillColor(HexColor(MUTED));c.setFont('D',7.3)
    c.drawString(M,29,'CSPP v0.28 · feste Skala / kontrollierter Dichtebereich · METHOD / G1: HOLD')
    c.drawRightString(W-M,29,str(page));c.showPage()

def box(txt):
    global y
    obj=Paragraph(txt,styles['eq']);_,height=obj.wrap(CW-26,250)
    if y-height-24<57: raise ValueError(('box overflow',page))
    c.setFillColor(HexColor(PALE));c.roundRect(M,y-height-22,CW,height+22,6,fill=1,stroke=0)
    obj.drawOn(c,M+13,y-height-11);y-=height+34

def table(rows,widths):
    global y
    data=[[Paragraph(str(v),styles['white'] if i==0 else styles['table']) for v in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(INK)),('VALIGN',(0,0),(-1,-1),'TOP'),
         ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
         ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
         ('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#F0F5F6'),white])]))
    _,height=t.wrap(CW,1000)
    if y-height<57:raise ValueError(('table overflow',page))
    t.drawOn(c,M,y-height);y-=height+16

# Visual diagnostics only. Exact maxima, cutoffs and number intervals are in RESULTS.json.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,1,figsize=(8,5.2),layout='constrained')
coeff=[197/8,-3033/8,2363/2,-1331,504]
for ax,den,stop in zip(axes,[16,64],[180,650]):
    cert=next(row for row in RESULT['certificates'] if row['theta']==21 and row['epsilon']==f'1/{den}')
    e=1/den
    def w(n):return sum(ck*math.comb(n,k)*e**k*(1-e)**(n-k) for k,ck in enumerate(coeff) if k<=n)
    xs=list(range(stop+1));ys=[w(n) for n in xs]
    cap=float(Fraction(cert['maximum']));imax=cert['maximizers'][0]
    ax.plot(xs,ys,color=TEAL,lw=1.9,label='Signiertes geglättetes Gewicht')
    ax.axhline(cap,color=ORANGE,ls='--',lw=1);ax.axhline(-cap,color=ORANGE,ls='--',lw=1,label='Exakte globale Betragshülle ±S')
    ax.axvline(cert['cutoff'],color=MUTED,ls=':',lw=1,label='Beginn des zertifizierten Rests')
    ax.scatter([imax],[w(imax)],color=ORANGE,zorder=5,s=23)
    ax.annotate(f'Maximaler Betrag bei n = {imax}',(imax,w(imax)),xytext=(.34,.16 if w(imax)<0 else .83),textcoords='axes fraction',fontsize=9,color=ORANGE,arrowprops=dict(arrowstyle='-',color=ORANGE))
    ax.set_title(f'θ = 21, ε = 1/{den}',loc='left',fontsize=11)
    ax.set_ylabel('wε(n)');ax.set_xlabel('Anzahl n im offenen Kausalintervall');ax.grid(axis='y',alpha=.18)
axes[0].legend(loc='upper right',frameon=False,fontsize=8)
fig.savefig(OUT/'smoothed_weights.png',dpi=180);plt.close(fig)

title('01 / ERGEBNIS','Die vorhandene Aufhebung<br/>in den Gewichten nutzen')
p('<b>Der Anschluss an v0.27 ist ausgeführt.</b> Die Fehlerobergrenze wird deutlich kleiner, sobald die tatsächlichen geglätteten Intervallgewichte anstelle des grössten ungeglätteten Schichtkoeffizienten verwendet werden. Operator und physikalische Aufgabe bleiben unverändert.')
box('θ = 21, gemeinsame 99-Prozent-Obergrenze:<br/><b>225 534 008 → 82 031</b><br/>Verschärfung um etwa Faktor <b>2 749</b>')
p('Die gerundeten Zahlen sind konservative obere Anzeigen. Der Vergleich gilt bei gleich grossen begrenzten aktiven und Historyfehlern, T = 9/4, H = 4 und festem q. Die neue Schranke gilt ab der ursprünglichen Dichte ρ₀ = 3/π für alle höheren Dichten.')
table([['Arbeitsschritt','Ergebnis'],['Geglättete Gewichte global begrenzen','Exakte Maxima über alle Intervallzahlen'],['Höhere Dichten kontrollieren','Analytische Binomialkomposition'],['History und Detektor mitführen','Unveränderte v0.27-Fehlerabbildung']], [CW*.47,CW*.53])
p('<b>Wissenschaftliche Bewertung:</b> Es handelt sich um kleinere hinreichende Obergrenzen, nicht um eine gemessene Fehlerreduktion. Die ursprüngliche Fehlerbilanz ist weiterhin nicht freigegeben. Der Genauigkeitsausschluss des θ = 21-Kandidaten bleibt bestehen; METHOD und G1 bleiben HOLD.')
p('Erfasst wird die Aufhebung zwischen Schichtbeiträgen innerhalb eines Intervallgewichts. Eine robuste Aufhebung zwischen verschiedenen Ausbreitungspfaden ist damit noch nicht nachgewiesen.','small')
footer()

title('02 / MECHANISMUS UND DICHTE','Eine exakte Identität<br/>ersetzt den Dichtescan')
p('Schreibe das geglättete Gewicht als w<sub>ε</sub>(n) = Σ c<sub>k</sub> Bin(n,k;ε). Für 0 &lt; ε ≤ ε̄ und p = ε/ε̄ gilt durch zweimalige Binomialauswahl:')
box('w<sub>ε</sub>(n) = Σ<sub>m=0…n</sub> Bin(n,m;p) w<sub>ε̄</sub>(m)<br/>|w<sub>ε</sub>(n)| ≤ S(ε̄), &nbsp; S(ε̄) = sup<sub>m≥0</sub> |w<sub>ε̄</sub>(m)|')
p('Die rechte Seite ist eine konvexe Kombination der Gewichte bei ε̄. Ihr Betrag kann deren globales Maximum nicht überschreiten. Weil ε = q/ρ gilt, umfasst ein einziges Zertifikat bei ε̄ alle Dichten ρ ≥ q/ε̄. Das ist ein analytischer Kontinuumsbefund, kein endlicher Dichtescan.')
p('Die übertragene Eintragsbedingung','h2',gap=7)
box('|K<sub>ij</sub>| ≤ κ̄/ρ, &nbsp; κ̄ = aq S(ε̄)/|D|<br/>bisher: κ = aq max<sub>k</sub>|c<sub>k</sub>|/|D|')
p('Bei ε̄ = 1/16 sinkt die Gewichtshülle für θ = 21 von 1331 auf 38,478595…; für θ = 0 von 16 auf 1,158608…. Die Vorzeichen werden vor der Betragsbildung summiert. Die lokale Diagonale D bleibt unverändert.')
p('<b>Grenze der Aussage:</b> Die neue kleinere Hülle gilt ab ρ₀, nicht auf dem gesamten früheren Bereich ρ ≥ q. Bei ρ = q wäre ε = 1 und die geglätteten Werte wären wieder die ungeglätteten Koeffizienten. Diese unzulässige Ausweitung wird als Negativkontrolle erkannt.')
p('Das gedankliche Ausdünnen dient nur dem Beweis [1]. Es löscht keine Punkte aus Projektwolken, verändert keinen Sampler und setzt keine Unabhängigkeit zwischen Kanten voraus.','small')
footer()

title('03 / UNENDLICHER REST','Eine endliche Suche<br/>wird zum globalen Zertifikat')
p('Für A<sub>n</sub> = Σ |c<sub>k</sub>| Bin(n,k;ε̄) gilt |w(n)| ≤ A<sub>n</sub>. Sobald N ≥ d und ε̄(N+1) ≥ d sind, nehmen alle positiven Summanden für n ≥ N ab. Ist zusätzlich A<sub>N</sub> kleiner als das schon gefundene Maximum, kann kein späterer Intervallwert es übertreffen.')
table([['θ','ε̄','Globales S (Anzeige)','Maximierer n','Rest ab N'],['0','1/16','1,158608211','8','102'],['0','1/32','1,081648548','16','210'],['0','1/64','1,046882119','33','424'],['21','1/16','38,478595018','5','145'],['21','1/32','34,891328546','11','296'],['21','1/64','33,356389496','101','599']], [34,53,156,130,CW-373])
c.drawImage(str(OUT/'smoothed_weights.png'),M,y-277,width=CW,height=277,mask='auto');y-=287
p('Bei ε̄ = 1/64 verfehlt ein Scan nur bis n = 50 das spätere globale Maximum bei n = 101. Die Grafik ist Gleitkomma-Diagnostik; Maxima und unendliche Reste sind separat exakt rational zertifiziert.','small')
footer()

title('04 / FEHLERBUDGETS','Die neue Hülle in die<br/>bestehende Dynamik einsetzen')
p('Für F(T) = [cosh(ωT)+cos(ωT)]/2 mit ω⁴ = 8πκ̄ und ℋ(T,H) = Σ<sub>r=1…4</sub> H<super>r</super>F<sup>(r)</sup>(T)/r! bleibt die gemeinsame Fehlerabbildung unverändert:')
box('|ΔA| ≤ η<sub>f</sub> + [η<sub>f</sub>(F−1) + η<sub>h</sub>ℋ]/δ<br/>mit Wahrscheinlichkeit mindestens 1−δ; Q = 1')
p('T = 2,25; H = 4; δ = 0,01; festes q; ρ ≥ ρ₀. Die folgenden Anzeigen sind auf zwei Dezimalstellen nach oben gerundet:','small')
table([['Verstärkung','θ = 0','θ = 21'],['v0.27, aktive Fehler / exakte History','809,32','89 858,07'],['v0.28, aktive Fehler / exakte History','54,33','584,89'],['v0.27, gleiche aktive und Historyfehler','136 119,89','225 534 007,30'],['v0.28, gleiche aktive und Historyfehler','3 601,93','82 030,24']], [CW*.55,CW*.21,CW*.24])
p('Was das für den bisherigen Kandidaten bedeutet','h2',gap=7)
p('Für das unveränderte normierte Ausgabebudget 0,001 wäre mit θ = 21 und exakter History eine additive Fehlerhülle von höchstens 1,70 × 10⁻⁶ hinreichend. Sind aktive und Historyfehler gleich gross, ist jeweils höchstens 1,21 × 10⁻⁸ hinreichend. Beide Anzeigen sind konservativ nach unten gerundet.')
p('Diese Eingabehüllen wurden hier nicht für die tatsächlichen KG-Residuen nachgewiesen. Fehler der ursprünglichen Quelle J müssen vorab durch |D| geteilt und in derselben Feldnormierung ausgewiesen werden. Die Wahrscheinlichkeit bezieht sich auf Poisson-Realisierungen; sie ist keine Konfidenzaussage über neu gemessene Daten.','small')
footer()

title('05 / METHODENGRENZE','Mehr Dichte allein<br/>macht diese Hülle nicht null')
p('Weitere Dichteuntergrenzen verbessern das Zertifikat etwas: Für θ = 21 sinkt die gemeinsame Grenze bei ρ ≥ 2ρ₀ auf etwa 69 945 und bei ρ ≥ 4ρ₀ auf etwa 65 066. Der Hauptgewinn ist bereits bei der ursprünglichen Dichte vorhanden.')
box('w<sub>ε</sub>(0) = c₀ &nbsp; ⇒ &nbsp; S(ε) ≥ |c₀|')
p('Da F und ℋ positive Potenzreihen in κ̄ sind, begrenzt dieser einfache Sachverhalt die Leistungsfähigkeit einer konstanten Eintragshülle. Selbst der optimistische Einsatz von |c₀| ergäbe für θ = 21 hier noch eine gemeinsame Grenze von etwa 40 585. Das ist eine Grenze dieses Beweisverfahrens, keine Untergrenze der tatsächlichen Fehlerverstärkung.')
table([['Erledigt','Offen'],['Aufhebung innerhalb geglätteter Schichtgewichte','Aufhebung zwischen unterschiedlichen Pfaden'],['Alle Intervallzahlen und höhere Dichten ab ρ₀','Unendliche Ausbreitungszeit und History'],['Festes normiertes Detektormittel','Globales Maximum über wachsende Beobachtungsgebiete'],['Schärfere Verstärkungsobergrenzen','Tatsächliche KG-Residuen und vollständige Fehlerfreigabe']], [CW/2,CW/2])
p('Der Fächer-Ausschluss aus v0.26 bleibt gültig: Viele beschränkte Einträge können gemeinsam eine grosse Antwort erzeugen. Die Ausgabegrenze ist deshalb weiterhin probabilistisch. Ein einziges gemeinsames Ereignis für unendlich viele Dichten wird nicht behauptet.','small')
footer()

title('06 / VALIDIERUNG UND ANSCHLUSS','Exakte Rechnung;<br/>physikalische Gates bleiben HOLD')
table([['Kontrolle','Ergebnis'],['Sechs globale Gewichtszertifikate','1782 Intervallwerte auf drei Rechenwegen'],['Binomialkomposition','648 rationale Identitäten'],['Operator / eingefrorene History','2442 + 2442 exakte Graphfälle'],['Zahlenbudgets','Zehn Zeilen, drei Präzisionen; v0.27-Abgleich'],['Absichtlich falsche Varianten','Sechs Negativkontrollen erkannt'],['Unveränderte Projektquellen','Fünf Git-Blob- und SHA256-Prüfungen']], [CW*.52,CW*.48])
p('Die Reproduktion benötigt nur Python 3.12 und die Standardbibliothek. <font face="DM">python3 -I -O -B reproduce.py --check</font> vergleicht die Ergebnisdatei bytegenau. Die kleinen Graphfälle nutzen einen rationalen Vorfaktor 1/7; die tatsächlichen Projektkonstanten sind separat eingeschlossen.')
p('Nächster präziser Auftrag','h2',gap=7)
p('Die konstante Gewichtshülle durch eine Intervallvolumen-abhängige Pfadabschätzung ersetzen und erneut das feste History-/Detektorbudget auswerten. Einzelketten und überlappende Pfadpaare müssen getrennt behandelt werden. Der Grad-5-Genauigkeitsauftrag bleibt separat offen.')
p('Quellen und Grenzen der Validierung','h2',gap=7)
p('[1] Last / Penrose, <i>Lectures on the Poisson Process</i>, 2017, Abschnitt 5.3 und Korollar 5.9; geerbte Kettenzählung: Korollar 4.10.<br/>stoch.math.kit.edu/img/Last/lastpenrose2017.pdf<br/>[2] Aslanbeigi / Saravani / Sorkin, <i>Generalized Causal Set d’Alembertians</i>, 2014. arxiv.org/abs/1403.1622','small',gap=7)
p('Vollständige eigene Herleitung in PROOF.md; Projektbasis Main nach PR #160. Keine neuen Wolken, kein externes Peer Review, keine Beweisassistent-Verifikation und kein Prioritätsanspruch. Die Genauigkeitsausschlüsse werden durch die schärfere Obergrenze nicht aufgehoben.','small')
footer();c.save();print(pdf)

