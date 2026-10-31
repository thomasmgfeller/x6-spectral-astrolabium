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
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,3.8),layout='constrained')
for theta,C,d,color in [(0,16,-1,TEAL),(21,1331,-71/8,ORANGE)]:
    a=1/math.sqrt(2*math.pi); w=1.5*a*C/(1-a*d); om=w**.25
    xs=[i/80 for i in range(1,501)]
    values=[1+100*((math.cosh(om*t)+math.cos(om*t))/2-1) for t in xs]
    ax.plot(xs,values,color=color,lw=2.2,label=f'θ = {theta}')
ax.set_yscale('log');ax.set_xlabel('Zeitfenster T in Projekt-Längeneinheiten (c = 1)')
ax.set_ylabel('Obere Verstärkungsschranke bei δ = 0,01')
ax.axvline(2.25,color=MUTED,ls=':',alpha=.65); ax.text(2.32,4,'Aktives Band T = 2,25',color=MUTED,fontsize=9)
ax.grid(axis='y',alpha=.2);ax.legend(frameon=False)
fig.savefig(OUT/'finite_time_bounds.png',dpi=180);plt.close(fig)

styles={
 'body':ParagraphStyle('body',fontName='D',fontSize=10.1,leading=15,textColor=HexColor(INK)),
 'small':ParagraphStyle('small',fontName='D',fontSize=8.7,leading=12.6,textColor=HexColor(MUTED)),
 'h2':ParagraphStyle('h2',fontName='DB',fontSize=14,leading=19,textColor=HexColor(INK)),
 'eq':ParagraphStyle('eq',fontName='D',fontSize=12,leading=19,textColor=HexColor(INK)),
 'table':ParagraphStyle('table',fontName='D',fontSize=9.2,leading=13,textColor=HexColor(INK)),
 'white':ParagraphStyle('white',fontName='DB',fontSize=9,leading=13,textColor=white),
}
W,H=595.28,841.89; M=47; CW=W-2*M
pdf=OUT/'Dichteuniforme_Finite_Zeit_Stabilitaet_v0_27.pdf'
c=canvas.Canvas(str(pdf),pagesize=(W,H),invariant=1)
c.setTitle('CSPP v0.27 - Dichteuniforme Stabilität auf endlichen Zeitfenstern')
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
    c.drawString(M,y,'CSPP / EIGENZEIT  ·  FORSCHUNGSNOTIZ 0.27  ·  31.10.2026');y-=37
    c.setFillColor(HexColor(MUTED));c.setFont('DB',9);c.drawString(M,y,kicker);y-=14
    obj=Paragraph(heading,ParagraphStyle('title',fontName='DB',fontSize=25,leading=30,textColor=HexColor(INK)))
    _,height=obj.wrap(CW,180);obj.drawOn(c,M,y-height);y-=height+20

def footer():
    c.setStrokeColor(HexColor('#DCE5E8'));c.line(M,43,W-M,43)
    c.setFillColor(HexColor(MUTED));c.setFont('D',7.3)
    c.drawString(M,29,'CSPP v0.27 · fester Detektor / endliches Zeitfenster · METHOD / G1: HOLD')
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

title('01 / ERGEBNIS','Eine positive Schranke<br/>mit klaren Grenzen')
p('<b>Der Anschluss an v0.26 ist ausgeführt.</b> Für eine feste Probe oder ein festes Detektormittel lässt sich die Fehlerverstärkung auf einem endlichen Zeitfenster mit expliziter Ausfallwahrscheinlichkeit begrenzen. Bei festem q wächst die Schranke nicht mit der Sprinklingdichte ρ.')
box('E G ≤ F(T), &nbsp; F(T) = [cosh(ωT) + cos(ωT)] / 2<br/>P{G &gt; 1 + [F(T) − 1] / δ} ≤ δ<br/>ω = (8πκ)<super>1/4</super>, &nbsp; |K<sub>ij</sub>| ≤ κ/ρ')
p('G misst die Verstärkung beliebiger punktweise begrenzter additiver Gleichungsfehler zur festen passiven Probe. Die Wahrscheinlichkeit bezieht sich auf ideale Poisson-Realisierungen in 1+3 Minkowski-Raum. Es handelt sich um einen analytischen Satz, nicht um eine Monte-Carlo-Beobachtung.')
table([['Kontrolliert','Weiterhin offen'],['Dichte ρ bei festem q und T','Beliebig lange Ausbreitungszeit'],['Räumliche Gebietserweiterung bei festem Detektor','Globales Maximum über immer mehr Orte'],['Vorgeschriebene endliche History','Unendliche History und Spektralstabilität']], [CW/2,CW/2])
p('<b>Praktische Bewertung:</b> Die Schranke ist endlich und auswertbar; die Konstanten des bisherigen Kandidaten sind jedoch noch zu gross für eine Fehlerfreigabe. METHOD und G1 bleiben HOLD. Der Genauigkeitsausschluss aus v0.25 wird nicht aufgehoben.')
p('Der Beweis nutzt kausale Kettenvolumina und eine Gewichtshülle. Eine robuste signierte Pfadaufhebung in einer physikalisch qualifizierten Operatorfamilie ist damit noch nicht nachgewiesen.','small')
footer()

title('02 / MATHEMATISCHER MECHANISMUS','Die kausale Ordnung<br/>unterdrückt lange Ketten')
p('<b>1. Alle Beiträge kausal entwickeln.</b> Auf jeder endlichen Realisierung ist die retardierte Inverse eine endliche Neumannsumme. Jeder Term entspricht einer geordneten Kette. Ihre Betragsgewichte sind höchstens (κ/ρ)<super>k</super>.')
p('<b>2. Die Poisson-Ketten zählen.</b> Das faktorielle Momentmass liefert einen Faktor ρ<super>k</super>. Er kürzt die inverse Dichte jedes Kettenschritts exakt. Unabhängigkeit zwischen den tatsächlichen Operatorgewichten wird dafür nicht benötigt [1].')
box('E C<sub>k</sub>(x) ≤ ρ<super>k</super> I<sub>k</sub>(T)<br/>I<sub>k</sub>(T) = (8π)<super>k</super> T<super>4k</super> / (4k)!')
p('<b>3. Das Kettenvolumen integrieren.</b> Bei Zeitinkrement s ist das zulässige räumliche Volumen 4πs³/3. Die positiven Zeitinkremente aller k Schritte müssen zusammen kleiner als T sein. Das entsprechende Simplexintegral erzeugt den Nenner (4k)!. Es kommt kein zusätzliches 1/k! hinzu.')
p('<b>4. Eine überprüfbare Wahrscheinlichkeitsschranke bilden.</b> Für die nichtnegative Pfadmajorante Z gilt G ≤ 1 + Z und E Z ≤ F − 1. Markovs Ungleichung liefert die explizite Ausfallwahrscheinlichkeit δ. Das direkte Eingabesignal mit Faktor eins bleibt erhalten.')
box('Reine Punktzahl: ungefähr exp(κπT⁴/3)<br/>Kausale Ketten: ungefähr exp(ωT)/4')
p('Die zweite Abschätzung wächst wesentlich langsamer mit T, bleibt aber eine endliche-Zeit-Aussage. Der Satz ist kompatibel mit seltenen, beliebig grossen Verstärkungen aus v0.26. Jede Dichte hat dieselbe Schranke; ein gemeinsames Ereignis für unendlich viele Dichten ist nicht behauptet.','small')
footer()

title('03 / HISTORY UND DETEKTOR','Vorgegebene Vergangenheit<br/>getrennt behandeln')
p('Die History liegt in −H &lt; t ≤ 0 und wird vorgeschrieben. Nur 0 &lt; t &lt; T wird dynamisch fortgesetzt. Eine History-zu-Probe-Kette beginnt genau einmal in der History; anschliessend enthält sie ausschliesslich aktive Punkte. Zusätzliche Propagation innerhalb der History würde die Schranke künstlich vergrössern.')
box('ℋ(T,H) = Σ<sub>r=1…4</sub> H<super>r</super> F<sup>(r)</sup>(T) / r!')
p('Mit aktiver bzw. passiver additiver Fehlerhülle η<sub>f</sub> und Historyfehler η<sub>h</sub> gilt mit Wahrscheinlichkeit mindestens 1 − δ:')
box('|Δu<sub>x</sub>| ≤ η<sub>f</sub> +<br/>[η<sub>f</sub>(F − 1) + η<sub>h</sub>ℋ] / δ')
p('Die Herleitung startet mit dem direkt erreichbaren Historyvolumen π[(t+H)⁴−t⁴]/3. Wiederholte Faltung mit dem aktiven Kegelkern 4πκs³/3 ergibt die obige positive Reihe. Die beiden Fehlerbeiträge teilen ein gemeinsames Ausfallbudget; sie müssen nicht unabhängig sein.')
p('Übertragung auf den festen KG-Detektor','h2')
p('Für ein deterministisches Detektormass mit Totalvariation Q wird die Fehlergrenze mit Q multipliziert. Ein positives normiertes räumlich-zeitliches Mittel hat Q = 1. Gemeinsame kausale Vorgänger verschiedener Proben bleiben erlaubt.')
p('Im ursprünglichen finiten Gebiet Ω₅ gilt für das aktive Band T = 9/4; die vorgeschriebene Vergangenheit hat höchstens H = 4. Fehlergrössen müssen in derselben Feldnormierung wie die Ausgabe vorliegen. Eine zufällige Detektornormierung oder eine unendliche Vergangenheit ist von diesem Satz nicht abgedeckt.','small')
footer()

title('04 / KONKRETE BUDGETS','Endlich bedeutet noch<br/>nicht ausreichend scharf')
p('Die geglätteten Schichtgewichte erfüllen die Voraussetzung mit κ = aq max|c<sub>l</sub>| / |D|, wenn q fest, ρ ≥ q und D ≠ 0 sind. Für q₀ = 3/(16π), m = 1 und δ = 0,01 ergeben sich folgende Anzeigen der zertifizierten Intervalle:')
table([['Verstärkungsgrenze','θ = 0','θ = 21'],['Aktiv, T = 2,25; exakte History','809,32','89 858,07'],['Aktiv plus History H = 4; gleiche Fehlerhüllen','136 119,89','225 534 007,30'],['Grobe Behandlung des ganzen Bands T = 6,25','613 970,82','1,89 × 10¹¹']], [CW*.49,CW*.23,CW*.28])
p('θ = 21: Die Historyzerlegung verbessert die gemeinsame grobe Grenze um etwa Faktor 838. Bei exakter History müsste ein uniformer additiver Fehler für das Ausgabebudget 0,001 dennoch höchstens etwa 1,11 × 10⁻⁸ betragen. Ein solches Residuum wurde hier nicht nachgewiesen.','small')
c.drawImage(str(OUT/'finite_time_bounds.png'),M,y-225,width=CW,height=225,mask='auto');y-=238
p('Abbildung: aktive 99-Prozent-Schranke bei exakter History; keine gemessene Verstärkung. Die Grafik nutzt Gleitkommawerte. Die Tabelle wird durch rationale Intervalle mit kontrolliertem Reihenrest abgesichert. Die grossen Konstanten beweisen keine tatsächliche Instabilität.','small')
footer()

title('05 / AUSSAGEGRENZEN','Lokal kontrolliert;<br/>global bleibt ein Hindernis')
p('<b>Räumlich grösseres Rechengebiet:</b> Für eine feste Probe auf endlichem Zeitband ist die kausale Vergangenheit beschränkt. Sobald sie vollständig enthalten ist, können weitere räumlich entfernte Punkte den Intervalloperator an dieser Probe nicht verändern.')
p('<b>Immer mehr Beobachtungsorte:</b> Für jeden endlichen Grenzwert L besitzt die Fächerkonstruktion aus v0.26 eine lokale Überschreitungswahrscheinlichkeit p<sub>L</sub> &gt; 0. Genügend weit getrennte vergangene Kegel sind unabhängig. Für J solche Proben gilt:')
box('P{max<sub>i≤J</sub> G<sub>i</sub> ≤ L} ≤ (1 − p<sub>L</sub>)<super>J</super> → 0')
p('Damit ist eine feste Wahrscheinlichkeitsschranke für das globale räumliche Maximum über beliebig wachsende Gebiete ausgeschlossen, sofern derselbe nichttriviale Intervallkern unverändert eingesetzt wird. Für ein festes Detektormittel gilt dieser Ausschluss nicht.')
table([['Befund','Bedeutung'],['Dichteuniforme lokale Schranke','Analytisch bewiesen unter expliziten Voraussetzungen'],['Noch grosse obere Grenzen','Schärfung nötig; kein Instabilitätsnachweis'],['Normierung und Genauigkeit','Bleiben eigenständige Anforderungen'],['Langzeit- und Spektralstabilität','Durch diesen Schritt nicht entschieden']], [CW*.43,CW*.57])
p('Die gewählte Anfangszeitscheibe gehört zur Cauchyaufgabe. Der Operator selbst bleibt durch Kausalrelationen und Intervallzahlen definiert. Eine intrinsische Aussage für beliebige nicht eingebettete Kausalsets wird hier nicht beansprucht.','small')
footer()

title('06 / VALIDIERUNG UND ANSCHLUSS','Exakt geprüft;<br/>der nächste Engpass ist sichtbar')
table([['Kontrolle','Ergebnis'],['407 Ordnungen auf 1 bis 5 Punkten','3256 signierte Operatorfälle bestanden'],['Eingefrorene History','3256 zusätzliche Fälle bestanden'],['Dichte Inversion / Vorwärtsrekursion / Kettenenumeration','Exakte rationale Übereinstimmung'],['Kausal- und Historyintegrale','24 + 48 rationale Identitäten'],['Zahlenschranken / Negativkontrollen','Drei Präzisionen / sechs Fehler erkannt']], [CW*.57,CW*.43])
p('Die Ergebnisdatei wird mit <font face="DM">python3 -O -B reproduce.py --check</font> bytegenau reproduziert. Alle mathematischen Kontrollen benötigen nur die Python-Standardbibliothek. Keine neuen Poisson-Wolken, keine Parameteranpassung und keine neue physikalische Freigabe.')
p('Nächster begrenzter Auftrag','h2',gap=7)
p('Die grobe Hülle max|c<sub>l</sub>| durch kontrollierte Intervall- und signierte Pfadabschätzungen ersetzen. History, Detektornorm und Ausfallbudget müssen unverändert mitgeführt werden. Der Grad-5-Genauigkeitsauftrag bleibt separat offen.')
p('Quellen und vollständiger Beweis','h2',gap=7)
p('[1] Last / Penrose, <i>Lectures on the Poisson Process</i>, 2017, Satz 4.4 und Korollar 4.10.<br/>stoch.math.kit.edu/img/Last/lastpenrose2017.pdf<br/>[2] Johnston, <i>Particle propagators on discrete spacetime</i>, 2008, Abschnitt 3.1.1. arxiv.org/abs/0806.3083<br/>[3] Aslanbeigi / Saravani / Sorkin, <i>Generalized Causal Set d’Alembertians</i>, 2014. arxiv.org/abs/1403.1622','small',gap=7)
p('PROOF.md enthält die vollständigen eigenen Herleitungen und Quantoren. Unveränderte Projektquellen sind am Main-Commit 268516fb5758… mit Git-Blob und SHA256 gesichert. Die endlichen Prüfungen ersetzen kein externes Peer Review und keine formale Beweisverifikation. Keine Prioritätsbehauptung.','small')
footer();c.save()
print(pdf)
