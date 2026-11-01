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
pdf=OUT/'Intervallvolumen_Pfadstabilitaet_v0_29.pdf'
c=canvas.Canvas(str(pdf),pagesize=(W,H),invariant=1)
c.setTitle('CSPP v0.29 - Intervallvolumen und zertifizierte Pfadstabilität')
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
    c.drawString(M,y,'CSPP / EIGENZEIT  ·  FORSCHUNGSNOTIZ 0.29  ·  01.11.2026');y-=37
    c.setFillColor(HexColor(MUTED));c.setFont('DB',9);c.drawString(M,y,kicker);y-=14
    obj=Paragraph(heading,ParagraphStyle('title',fontName='DB',fontSize=25,leading=30,textColor=HexColor(INK)))
    _,height=obj.wrap(CW,180);obj.drawOn(c,M,y-height);y-=height+20

def footer():
    c.setStrokeColor(HexColor('#DCE5E8'));c.line(M,43,W-M,43)
    c.setFillColor(HexColor(MUTED));c.setFont('D',7.3)
    c.drawString(M,29,'CSPP v0.29 · vollständige Kausalintervalle / endliche Zeit · METHOD / G1: HOLD')
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

old=json.loads((ROOT/'evidence/RESULTS_v028.json').read_text())
budgets={r['theta']:r for r in RESULT['budgets']}
previous={r['theta']:r for r in old['budgets'] if r['kind']=='smoothed_1/16'}
def val(row,key,side): return float(Fraction(row[key][side+'_fraction']))

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
                     'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8,3.8),layout='constrained')
for i,theta in enumerate([0,21]):
    lo=val(budgets[theta],'B_joint','lower');hi=val(budgets[theta],'B_joint','upper')
    before=val(previous[theta],'B_joint','upper')
    ax.plot([lo,hi],[i,i],lw=7,color=TEAL,solid_capstyle='butt')
    ax.scatter([before],[i+.16],marker='D',s=48,color=ORANGE)
    ax.annotate(f'v0.29: [{math.floor(lo):,d}; {math.ceil(hi):,d}]'.replace(',',' '),
                ((lo+hi)/2,i),xytext=(0,-23),textcoords='offset points',ha='center',fontsize=9)
    ax.annotate(f'v0.28: {math.ceil(before):,d}'.replace(',',' '),(before,i+.16),
                xytext=(0,12),textcoords='offset points',ha='center',fontsize=9,color=ORANGE)
ax.set_xscale('log');ax.set_xlim(1200,140000);ax.set_ylim(-.55,1.7)
ax.set_yticks([0,1],['θ = 0','θ = 21'])
ax.set_xlabel('Gemeinsame Verstärkungsmajorante B (logarithmische Achse)')
ax.grid(axis='x',alpha=.2);ax.set_title('Zertifizierte Majorante: gleiche Eingabefehler, 99 %',loc='left',fontsize=11)
fig.savefig(OUT/'budget_enclosures.png',dpi=180);plt.close(fig)

title('01 / ERGEBNIS','Die Intervallgeometrie<br/>verschärft die Schranke')
p('<b>Der Anschluss an v0.28 ist ausgeführt.</b> Die neue Rechnung mittelt den Betrag der geglätteten Gewichte über die Poisson-Verteilung der Intervallzahlen. Dadurch ersetzt eine vom Kausalintervall abhängige Hülle den bisherigen konstanten Maximalwert.')
box('θ = 21, gemeinsame 99-Prozent-Obergrenze:<br/><b>82 031 → 34 820</b><br/>Weitere Verschärfung: mindestens Faktor <b>2,35</b>')
p('Beide Anzeigen sind sicher nach oben gerundet. Verglichen wird dieselbe diagonalnormalisierte Fehlerabbildung bei T = 9/4, Historydauer H = 4, festem q = 3/(16π), ρ ≥ 3/π und einem festen normierten Detektormittel.')
table([['Fall','v0.28','v0.29: sichere obere Anzeige'],
       ['θ = 0, exakte History','54,326','41,055'],
       ['θ = 21, exakte History','584,887','321,952'],
       ['θ = 0, beide Fehlerarten','3 601,925','1 955,877'],
       ['θ = 21, beide Fehlerarten','82 030,234','34 819,303']], [CW*.47,CW*.22,CW*.31])
p('<b>Zusätzliche Voraussetzung:</b> Die benutzten Kausalintervalle müssen vollständig im Zählgebiet enthalten sein. Kausaldiamanten wie das bisherige Ω₅ erfüllen diese Bedingung. Für beliebig beschnittene Intervalle bleibt zunächst die v0.28-Hülle zuständig.')
p('Das Ergebnis ist eine kleinere hinreichende Obergrenze, keine gemessene Fehlerreduktion. Die tatsächliche KG-Fehlerbilanz ist weiterhin offen; METHOD und G1 bleiben HOLD.','small')
footer()

title('02 / MATHEMATISCHER MECHANISMUS','Einzelketten lassen sich<br/>korrekt mitteln')
p('Fixiere die Dichteuntergrenze ρ̄ und ε̄ = q/ρ̄. Das mittlere Betragsgewicht eines vollständigen Intervalls mit Volumen V ist bei dieser Dichte:')
box('Ā(V) = E |w<sub>ε̄</sub>(N)|, &nbsp; N ∼ Pois(ρ̄V)<br/>Ā(V) = e<super>−μ</super> Σ<sub>n≥0</sub> |w<sub>ε̄</sub>(n)| μ<super>n</super>/n!, &nbsp; μ = ρ̄V')
p('Die Binomialkomposition aus v0.28 und die Poisson-Ausdünnung liefern für jede höhere Dichte ρ ≥ ρ̄ die Hülle E |w<sub>q/ρ</sub>(Pois(ρV))| ≤ Ā(V). Bei ρ = ρ̄ gilt Gleichheit. Die Kontrolle betrifft ein ganzes Dichteintervall, nicht einen Dichtescan.')
p('Warum das für eine Kette funktioniert','h2',gap=7)
table([['Geometrische Tatsache','Folge im Poisson-Modell'],
       ['Benachbarte offene Kettenintervalle sind disjunkt.','Ihre Punktzahlen sind unter der Mecke-Einfügung unabhängig.'],
       ['Weitere Kettenpunkte liegen in keinem dieser Intervalle.','Die Einfügung verschiebt diese Zählungen nicht.'],
       ['Jeder Punkt liefert ρ; jede Kante liefert 1/ρ.','Die Dichtefaktoren kürzen sich im Pfadintegral.']], [CW*.49,CW*.51])
p('Die Konfigurationsabhängigkeit der Gewichte wird über die multivariate Mecke-Formel behandelt [1]. Die einfachere Formel für faktorielle Momentmasse allein würde diese Einfügungsfrage nicht beantworten.')
p('<b>Die Grenze:</b> Verschiedene Pfade dürfen Intervalle teilen. Für ihre gemeinsame Verteilung gilt die Einzelketten-Faktorisierung nicht. Die Rechnung nutzt nur die Linearität des Erwartungswerts der positiven Pfadsumme.','small')
footer()

title('03 / HISTORY UND DETEKTOR','Aus Intervallvolumen<br/>wird eine Zeitrekursion')
p('In 1+3 Minkowski-Dimensionen ist V = π(s²−r²)²/24. Die räumliche Integration definiert einen positiven Zeitkern h; die History ist genau ein Startbeitrag g:')
box('h(s) = 4πβ ∫<sub>0</sub><super>s</super> r² Ā(π(s²−r²)²/24) dr<br/>g(t) = ∫<sub>t</sub><super>t+H</super> h(s) ds, &nbsp; β = aq/|D|')
p('Die beiden Volterra-Gleichungen sammeln alle aktiven Pfadlängen:')
box('F = 1 + h ∗ F, &nbsp; J = g + h ∗ J<br/>B<sub>aktiv</sub> = 1 + (F(T)−1)/δ<br/>B<sub>gemeinsam</sub> = 1 + (F(T)−1+J(T))/δ')
p('Historyzeilen werden weiterhin eingefroren. Ein Historyfehler wird einmal eingespeist und danach nur durch aktive Punkte weitergegeben. Eine zusätzliche Ausbreitung innerhalb der vorgeschriebenen History wäre eine andere Dynamik.')
p('Gemeinsame Wahrscheinlichkeit statt unabhängiger Fehlerarten','h2',gap=7)
box('|ΔA| ≤ Q {η<sub>f</sub> + [η<sub>f</sub>(F−1)+η<sub>h</sub>J]/δ}<br/>mit Wahrscheinlichkeit mindestens 1−δ')
p('Ein einziges Markov-Budget kontrolliert beide Beiträge. Das feste Detektormass hat Totalvariation Q; beim positiven normierten Mittel ist Q = 1. Weder Proben noch Fehlerarten werden als unabhängig behandelt.')
p('Die Aussage gilt je fest gewählter Dichte mit denselben Konstanten. Sie kontrolliert weder ein gemeinsames Ereignis über unendlich viele Dichten noch ein globales Maximum über wachsende Beobachtungsgebiete. Quellfehler ΔJ sind vorher durch |D| zu teilen.','small')
footer()

title('04 / ZERTIFIZIERTE ZAHLEN','Die Unsicherheit der<br/>Rechnung bleibt sichtbar')
p('Die Balken zeigen Einschliessungen der neuen mathematischen Majorante. Die Rauten zeigen die praktisch punktförmig eingeschlossenen v0.28-Werte. Untere Grenzen sind keine Untergrenzen tatsächlicher Fehler.')
c.drawImage(str(OUT/'budget_enclosures.png'),M,y-239,width=CW,height=239,mask='auto');y-=251
table([['θ = 21','Zertifiziertes Intervall'],
       ['F(T)','[3,921873189179; 4,209516773755]'],
       ['History J(T)','[306,387912821809; 344,973509984005]'],
       ['Gemeinsame Majorante B','[30 931,978601098938; 34 819,302675775900]']], [CW*.34,CW*.66])
p('Bedingte Eingabebudgets für das Ausgabeziel 0,001','h2',gap=7)
p('Bei exakter History genügt für θ = 21 konservativ <b>η<sub>f</sub> ≤ 3,10 × 10⁻⁶</b>. Sind aktive und Historyfehler gleich gross, genügt jeweils <b>η ≤ 2,87 × 10⁻⁸</b>. Beide Anzeigen wurden sicher nach unten gerundet.')
p('Die tatsächlichen KG-Residuen wurden hier nicht berechnet. Der frühere Genauigkeitsausschluss von θ = 21 bleibt unverändert. Ein kleinerer Verstärkungsfaktor ersetzt weder eine Genauigkeitsprüfung noch eine Kovarianzvorhersage.','small')
footer()

title('05 / REPRODUKTION','Kontrollierte Reste<br/>statt blosser Gitterwerte')
table([['Rechenschritt','Absicherung'],
       ['Poisson-Summe bis n = 512','Unendlicher Rest durch geometrische Majorante'],
       ['Werte zwischen μ-Gitterpunkten','Analytische Lipschitzgrenze |Ψ′| ≤ S'],
       ['Räumliche Schalen','Exakte Massformel mit eingeschlossenen Wurzeln'],
       ['Volterra-Rekursion','Linke/rechte monotone Summen; oberer erster Term implizit gelöst'],
       ['Verfeinerung / Rundung','Zwei Raum-/Zeitgitter, 120 und 160 Integer-Dezimalstellen']], [CW*.40,CW*.60])
p('Jeder Lauf ist bereits einzeln eine gültige Einschliessung. Die Gitterverfeinerung ist eine zusätzliche Kontrolle; sie ist nicht die Begründung der Schranke. Die verbleibende Intervallbreite stammt vor allem von der Diskretisierung, nicht von Rundungsfehlern.')
table([['Gegenprüfung','Umfang'],
       ['Kettenintervalle auf kleinen Ordnungen','407 Ordnungen; 2 164 Ketten'],
       ['Bedingte Binomial-Jensen-Hülle','200 exakte Fälle'],
       ['Poissonwerte unabhängig gerechnet','10 Fraction-Gegenprüfungen'],
       ['Konstante Hülle / Kegelvolumen','v0.28-Reihen und 202 Schalenkontrollen'],
       ['Quellen und absichtliche Fehler','6 Quellprüfungen; 8 Negativkontrollen']], [CW*.55,CW*.45])
p('Reproduktion mit Python 3.12 und Standardbibliothek:<br/><font face="DM">python3 -I -O -B reproduce.py --check</font><br/>Die isolierte Wiederholung muss die Ergebnisdatei bytegenau erzeugen und alle Paketdateien unverändert lassen. Der vollständige Beweis liegt in PROOF.md.','small')
p('Kein neues Ensemble, kein Fit, kein externes Peer Review und keine Beweisassistent-Verifikation. Die technische Reproduzierbarkeit ist von den wissenschaftlichen Gates METHOD und G1 getrennt.','small')
footer()

title('06 / GRENZE UND ANSCHLUSS','Überlappende Pfade sind<br/>der nächste offene Schritt')
p('Für zwei Intervalle mit Volumina V₁, V₂ und Überlappung W lautet die gemeinsame Poisson-Erzeugende:')
box('E[z₁<super>N₁</super>z₂<super>N₂</super>] = exp{ρ[V₁(z₁−1)<br/>+ V₂(z₂−1) + W(z₁−1)(z₂−1)]}')
p('Bei W &gt; 0 darf der letzte Term nicht entfernt werden. Bei zwei eingefügten Pfaden können zudem Punkte des jeweils anderen Pfads im offenen Intervall liegen. Diese deterministischen Zählverschiebungen müssen zusätzlich berücksichtigt werden.')
p('Nächster begrenzter Auftrag','h2',gap=7)
p('Eine Zweipfad-Formel mit Überlappungsvolumina, gemeinsamen Knoten und Einfügungszahlen herleiten und gegen explizite Gegenbeispiele prüfen. Erst danach lässt sich entscheiden, ob ein kontrolliertes zweites Moment die bisherige Markov-Schranke sinnvoll ersetzt.')
p('Was weiterhin offen bleibt','h2',gap=7)
p('Signierte Pfadaufhebung, Kovarianztransfer, tatsächliche KG-Residuen, die getrennte Grad-5-Genauigkeitsaufgabe, unendliche History und ein zeituniformer Satz. Schon die positive Majorante wächst bei nichttrivialem Kernel unbegrenzt mit T; das ist eine Grenze dieses Verfahrens, kein Instabilitätsbeweis für die signierte Dynamik.')
p('Quellen und Projektbasis','h2',gap=7)
p('[1] Last / Penrose, <i>Lectures on the Poisson Process</i>, 21.08.2017: Theorem 4.4, Theorem 5.2, Corollary 5.9.<br/>stoch.math.kit.edu/img/Last/lastpenrose2017.pdf<br/>[2] Aslanbeigi / Saravani / Sorkin, <i>Generalized Causal Set d’Alembertians</i>, JHEP 1406 (2014) 024.<br/>arxiv.org/abs/1403.1622','small')
p('Eigene Ableitung auf Main nach PR #161, Commit 9a12332…; sechs eingefrorene Projektquellen mit Git-Blob und SHA256. Keine Neuheits- oder Prioritätsbehauptung. Dieser Entwicklungsschritt umfasst noch keine GitHub-Veröffentlichung.','small')
footer()
c.save()
print(pdf)

