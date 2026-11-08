#!/usr/bin/env python3
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape
import json
ROOT=Path(__file__).resolve().parent
FONT=Path('/usr/share/fonts/truetype/dejavu')
for n,f in [('DV','DejaVuSans.ttf'),('DV-Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
NAVY=HexColor('#173447'); TEAL=HexColor('#16756F'); INK=HexColor('#233640'); MUTED=HexColor('#59717C'); LIGHT=HexColor('#EEF4F5'); GOLD=HexColor('#AE701D')
styles={
 'kicker':ParagraphStyle('kicker',fontName='DV-Bold',fontSize=9,leading=13,textColor=TEAL,spaceAfter=14),
 'title':ParagraphStyle('title',fontName='DV-Bold',fontSize=25,leading=31,textColor=NAVY,spaceAfter=18),
 'h':ParagraphStyle('h',fontName='DV-Bold',fontSize=16,leading=21,textColor=NAVY,spaceAfter=12),
 'sub':ParagraphStyle('sub',fontName='DV-Bold',fontSize=10.3,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='DV',fontSize=9.4,leading=14.8,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8.1,leading=11.5,textColor=MUTED,spaceAfter=6),
 'formula':ParagraphStyle('formula',fontName='Mono',fontSize=9,leading=14,textColor=NAVY,spaceAfter=0),
}
def p(s,sty='body'): return Paragraph(s,styles[sty])
def code(lines):
    rows=[[p(escape(line),'formula')] for line in lines]
    t=Table(rows,colWidths=[475]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,0),10),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
    return KeepTogether([t,Spacer(1,11)])
def table(rows,widths):
    data=[[p(str(c),'small' if i else 'kicker') for c in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#D4DFE2')),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));return t
story=[]
def add(*xs):story.extend(xs)
def page(k,title):
    if story:add(PageBreak())
    add(p('CST-DUST  /  '+k,'kicker'),p(title,'h'))
add(p('FORSCHUNGSNOTIZ  08.11.2026  /  VERSION 0.1','kicker'),p('Kanonische Randrelation<br/>und lokale Reduktion','title'),p('Drei mathematische Vorarbeiten nach PR 267','sub'))
add(p('Die vorhandene Wirkung bestimmt im positiven inneren Dichtesektor eine explizite klassische Randrelation. Ihre geometrische Struktur erklärt, welche Daten gemeinsam zusammenpassen. Sie ist noch keine ausgewählte Evolution und kein physikalischer Quantenzustand.'))
add(table([['Vorarbeit','Ergebnis'],['Stationäre Randrelation','Explizite Momentfläche und lagrangesche Relation bestimmt'],['Constraint-Unterscheidung','Graphgleichungen, Sattelbedingungen und physikalische Constraints getrennt'],['Lokale Reduktion und Maße','Bedingte Dirac-Reduktion und exakter Maßtransport ausgearbeitet']], [205,270]))
add(Spacer(1,13),p('Ein wichtiger Schutz des bisherigen Modells','sub'),p('Das isolierte Dichte-Nullatom erlaubt andere Randdaten als der positive stationäre Zweig. Eine Projektion aller Zustände auf dieselbe Momentfläche würde einen Teil des bisherigen Modells entfernen. Die beiden Zweige bleiben deshalb ausdrücklich getrennt.'))
add(code(['Positive Relation: dim = 4 in dim = 8', 'Momentfläche: dim = 2', 'Nullatom: eigener Zweig mit p = 0', 'Alle acht physikalischen Gates: HOLD']))
add(p('Keine physikalische Präparation, kein Hamiltonian, kein Außenraum und kein Bounce sind hergeleitet. Kein n=5-Produktionslauf, keine kostenpflichtige Rechnung, keine externe Replikation.'))
add(p('Basis: Main a373f318e4a99bf1e2496f4d5bc674da6f6ea59c nach PR 267. Vollständige Beweise, Annahmen, Quellen und Reproduktionscode im begleitenden Prüfpaket.','small'))

page('01  /  WIRKUNG UND RAND','Die stationäre Relation explizit bestimmt')
add(p('Die Geometrie bleibt die feste Kette mit vier Vorgängern; ihre Dichten sind null. Die normierten Uhren erfüllen T₀&lt;T₁&lt;T₂&lt;T₃&lt;t, der innere positive Dichtewert 0&lt;w&lt;1. Es wird keine neue Randwirkung eingeführt.'))
add(code(['B = (-8,16,-9,1)', 'F1 = Σ B_y T_y;   F2 = 2 + Σ B_y T_y²', 'S = (wt/2)F1 - (w/4)F2', '∂t S = w F1/2;   ∂w S = t F1/2 - F2/4']))
add(p('Für w&gt;0 ist innere Stationarität genau gleichbedeutend mit F₁=F₂=0. Die geordnete Lösungsfläche besitzt die globale Karte c=T₃ und b=T₃-T₁:'))
add(code(['D(b) = √(72b²+153)', 'a(b) = [32b+D(b)]/34;   d(b) = [16b-8a(b)]/9', 'T(c,b) = (c-a, c-b, c-d, c)', 'c ∈ R;   b > 1/(2√2)']))
add(p('Alle geordneten Lösungen werden genau einmal erfasst. Der bisherige rationale Kragen liegt bei c=0,b=2. Der passende Randimpuls ist in derselben Orientierung wie PR 267:'))
add(code(['p = α dF1 + β dF2', 'α = -wt/2;   β = w/4', '0<β<1/4;   α < -2βc']))
add(p('Auf dieser vierdimensionalen Relation verschwindet die kanonische Einsform p·dT, weil dF₁=dF₂=0 entlang der Momentfläche gilt. Damit ist die Relation lagrangesch. Das sagt, welche Randdaten zusammenpassen; es wählt weder einen Verlauf noch eine physikalische Randpräparation aus.'))

page('02  /  CONSTRAINT-AUDIT','Der Kommutator bleibt richtig eingeordnet')
add(p('PR 267 prüfte die innere Uhrfunktion q_t als Multiplikationsoperator bei festen t,w. Dazu gehörte R_y=P_y+∂T_y S. Ihr Kommutator ist nicht null.'))
add(code(['[q_t, R_y] = iℏw B_y/2']))
add(p('Führt man stattdessen formal alle sechs kanonischen Paare z=(T₀,T₁,T₂,T₃,t,w) ein, ergeben die vollständigen Gradienten-Graphoperatoren einen anderen Ansatz:'))
add(code(['R_i = P_i + ∂i S', '[R_i,R_j] = 0', '[P_t,q_y] = -iℏw B_y/2']))
add(p('Die ergänzte Ableitung nach t hebt den alten Kommutatorterm exakt auf. Das widerlegt die frühere Schranke nicht: Raum und Operatorforderung sind verschieden.'))
add(p('Warum dies noch keine physikalische Lösung ist','sub'),p('Jede glatte skalare Funktion liefert einen solchen kommutierenden Gradienten-Graphen. Die formale Lösung exp(-iS/ℏ) ist damit weder normiert noch physikalisch ausgewählt. Der Schritt bestimmt keine Observablen, keine Randdomänen und keine Außenraumkopplung.'))
add(table([['Begriff','Was hier gezeigt ist'],['Stationäre Randrelation','Lösungsdaten der vorhandenen endlichen Wirkung'],['Kanonischer Gradienten-Graph','Mathematische Konstruktion auf zusätzlich gewähltem Kotangentialraum'],['Physikalische Constraintalgebra','Weiterhin nicht hergeleitet']], [210,265]))
add(Spacer(1,13),p('Der formale Ableitungsimpuls für w gilt nur lokal im offenen kontinuierlichen Stratum. Seine Übertragung auf das ursprüngliche Maß mit isoliertem Nullatom wäre eine neue, unbegründete Annahme. Eine globale Selbstadjungiertheit wird nicht behauptet.','small'))

page('03  /  LOKALE REDUKTION','Normale Paare korrekt eliminieren')
add(p('Die lokale Karte Q=(c,b,F₁,F₂) ist regulär. Ihre Kotangentialimpulse seien (P_c,P_b,Π₁,Π₂). Für ein zusätzlich festgehaltenes Paar t*,w* wird die passende normale Reaktion durch α*=-w*t*/2 und β*=w*/4 bestimmt.'))
add(code(['χ = (F1, F2, Π1-α*, Π2-β*)', '{F_i,F_j}=0;   {K_i,K_j}=0', '{F_i,K_j}=δ_ij;   K_i=Π_i-(α*,β*)_i', 'det Δ = 1;   Δ⁻¹ = -Δ']))
add(p('Diese vier Bedingungen sind zweitklassig. Ihre Dirac-Reduktion entfernt die normalen Koordinaten und Impulse gemeinsam. Lokal verbleibt T*M mit {c,P_c}=1 und {b,P_b}=1. Die alte normale Unschärfe wird nicht verletzt: Die eliminierten Größen sind keine unabhängigen Operatorpaare des alten Raums mehr.'))
add(p('Zwei verschiedene Maßfragen','sub'))
add(code(['Bedingtes Konfigurationsmaß:', 'd⁴T δ(F1)δ(F2) = k(b) dc db', 'k(b) = 1/[8√(72b²+153)];   k(2)=1/168', 'Reduziertes Liouville-Maß:', 'dc db dPc dPb']))
add(p('Im Phasenraum heben sich Konfigurations- und Impuls-Jacobian auf. Der Konfigurations-Coarea-Faktor darf dort nicht zusätzlich doppelt gezählt werden. Die beiden kinematischen Darstellungen L²(k dc db) und L²(dc db) sind durch Uψ=√k ψ unitär verbunden, wenn Zustände und Operatoren gemeinsam transportiert werden.'))
add(p('Die ursprüngliche stationäre Relation verlangt zusätzlich P_c=P_b=0: eine Nullsektion, kein Hamiltonian. Die Reduktion begründet weder das festgehaltene Paar t*,w* noch einen normierten physikalischen Zustand.','small'))

page('04  /  STRATA UND AMPLITUDE','Das Nullatom bleibt erhalten')
add(p('Am isolierten Atom w=0 gilt S=0. Es gibt dort keine infinitesimale Dichtevariation. Die beiden Momentbedingungen des positiven inneren Sektors dürfen deshalb nicht auf das Atom übertragen werden.'))
add(table([['Zweig','Zulässige stationäre Randdaten'],['Positives inneres w','T auf der Momentfläche M; p=α dF₁+β dF₂'],['Isoliertes Nullatom','Alle geordneten Randuhren T; p=0'],['Grenze w→0 bei endlichem t im positiven Zweig','Nur T auf M; deckt das ganze Atom nicht ab']], [220,255]))
add(Spacer(1,12),p('Die Variablenänderung zum normalen Impulsmaß ist ebenfalls exakt bestimmt. Für ein gleichförmiges Uhrfenster der Länge L und den ursprünglichen positiven Maßanteil dw/2 gilt:'))
add(code(['|∂(α,β)/∂(t,w)| = w/8', '(dt/L)(dw/2) = dα dβ/(Lβ)', '0<β<1/4;   α-Breite = 2βL', 'Kontinuierliche Masse = 1/2', 'Erstes w-Moment = 1/4; zweites = 1/6']))
add(p('Das integrierbare Maß auf diesem beschränkten Bereich ist kein flaches Fouriermaß auf R². Auch eine nachträgliche Normierung des falschen flachen Maßes repariert die Momente nicht.'))
add(code(['Bei F1=0, F2=1:', 'G = 1/2 + (1/2) ∫₀¹ exp(-iw/4) dw', 'Re G ≥ 191/192 > 0']))
add(p('Das endliche normierte Dichteintegral ist somit keine exakte Projektion auf die Momentfläche. Beiträge von Integrationsendpunkten, Uhrfensterrändern und nichtstationären Punkten werden durch die klassische Randrelation allein nicht klassifiziert.','small'))

page('05  /  PRÜFUNG UND WEITERARBEIT','Was jetzt überprüfbar vorliegt')
add(table([['Kontrolle','Umfang / Ergebnis'],['Vollständige Graphklammern','36 symbolische Identitäten / PASS'],['Alter Kommutator und ergänzte Aufhebung','4 Komponenten / PASS'],['Geordnete Momentfläche und Coarea','15 rationale Fälle / PASS'],['Stationäre Reaktionsdaten','135 Fälle / PASS'],['Kotangentialtransport','45 Fälle / PASS'],['Dirac-Reduktion und Umdefinition','4 Varianten / PASS'],['Positive Dichtemomente / Negativkontrollen','5 Momente / 8 Ausschlüsse / PASS']], [300,175]))
add(Spacer(1,11),p('Alle wissenschaftlichen Kontrollen verwenden nur rationale Arithmetik und die Python-Standardbibliothek. Drei Ergebnisdateien werden isoliert bytegleich reproduziert. Plan nach analytischem Entwurf, vor endlichen Kontrollen gehasht; keine externe Präregistrierung.'))
add(code(['python3 -O -B verify_package.py', 'python3 -O -B replay.py']))
add(p('Der nächste konkrete Test','sub'),p('Einen zweiten Rand-/Außenblock aus derselben Materiewirkung koppeln. Dann die gemeinsame Impulsbilanz, alle neuen oder umklassifizierten Kausalintervalle und die durch beide Blöcke bestimmten Daten prüfen. Die jetzt expliziten Randkoordinaten machen diesen Test ohne Großrechenlauf möglich.'))
add(p('Quellen und Reichweite','sub'))
for title,url in [
 ('Projektstand PR 267: Wirkung, Reaktionsbilanz und ursprünglicher Operatoraudit; Quellen unverändert im Paket.','https://github.com/thomasmgfeller/x6-spectral-astrolabium/pull/267'),
 ('Dittrich und Höhn, Canonical simplicial gravity (2012): Kontext für aktionsbasierte kanonische diskrete Systeme, keine übernommene CST-Dynamik.','https://arxiv.org/abs/1108.1974'),
 ('Cattaneo, Mnev, Reshetikhin, Classical BV theories on manifolds with boundary (2014): Kontext für Randphasenräume und Verklebung; hier keine BV/BFV-Quantisierung.','https://arxiv.org/abs/1201.0290')
]:add(p('<link href="'+url+'" color="#16756F">'+escape(title)+'</link>','small'))
add(p('Physikalische Zustandsauswahl, Constraintalgebra, Hamiltonian, Außenraum und Bounce bleiben offen. Alle acht physikalischen Gates bleiben HOLD.','small'))
def footer(c,doc):
    c.saveState();w,h=doc.pagesize
    c.setStrokeColor(TEAL);c.setLineWidth(1);c.line(60,49,w-60,49)
    c.setFont('DV',7.5);c.setFillColor(MUTED)
    c.drawString(60,34,'CST-DUST · Kanonische Randrelation v0.1 · 08.11.2026')
    c.drawRightString(w-60,34,f'{doc.page} / 6')
    c.restoreState()
def invariant_canvas(*a,**kw): kw['invariant']=1;return canvas.Canvas(*a,**kw)
out=ROOT/'CST_DUST_Kanonische_Randrelation_Reduktion_v0_1.pdf'
doc=SimpleDocTemplate(str(out),pagesize=(595.2756,841.8898),rightMargin=60,leftMargin=60,topMargin=48,bottomMargin=65,title='CST-DUST: kanonische Randrelation und lokale Reduktion v0.1',author='Thomas Gfeller · Forschungsprojekt mit ChatGPT')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=invariant_canvas)
print(out)
