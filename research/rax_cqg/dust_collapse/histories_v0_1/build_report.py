#!/usr/bin/env python3
"""Build the summary report and an exact-formula auxiliary-measure figure."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
NAME='CST_DUST_Positive_Historien_Schnittkonsistenz_v0_1'
FONT='/usr/share/fonts/truetype/dejavu/'
for name,file in [('DV','DejaVuSans.ttf'),('DVB','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,FONT+file))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
BLUE=colors.HexColor('#17445e');GRAY=colors.HexColor('#5b6670');PALE=colors.HexColor('#eef4f7')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=24,leading=30,textColor=BLUE,spaceAfter=18),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=15,leading=19,textColor=BLUE,spaceBefore=12,spaceAfter=10),
 'b':ParagraphStyle('b',fontName='DV',fontSize=10.2,leading=15.1,spaceAfter=9),
 's':ParagraphStyle('s',fontName='DV',fontSize=8.2,leading=11.6,spaceAfter=7,textColor=GRAY),
 'eq':ParagraphStyle('eq',fontName='DV',fontSize=11.2,leading=17,spaceBefore=7,spaceAfter=12,leftIndent=10,textColor=BLUE),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.6,leading=12),
}
story=[]
def p(t,style='b'):story.append(Paragraph(t,styles[style]))
def h(t):p(t,'h')
def eq(t):p(t,'eq')
def page():story.append(PageBreak())
def table(rows,widths):
    cells=[[Paragraph(str(x),styles['cell']) for x in row] for row in rows]
    t=Table(cells,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),
      ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
      ('LINEBELOW',(0,0),(-1,0),0.7,BLUE),('LINEBELOW',(0,1),(-1,-1),0.25,colors.HexColor('#d6dee3'))]))
    story.append(t);story.append(Spacer(1,10))
def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#d6dee3'));c.line(43,49,552,49)
    c.setFont('DV',8);c.setFillColor(GRAY)
    c.drawString(43,35,'CST-DUST • Positive Historien v0.1 • 7. November 2026')
    c.drawRightString(552,35,str(doc.page))
def main():
    figdir=ROOT/'figures';figdir.mkdir(exist_ok=True)
    x=np.linspace(-2,2,401);X,Y=np.meshgrid(x,x)
    joint=np.maximum(0,2-(np.maximum(np.maximum(X,Y),0)-np.minimum(np.minimum(X,Y),0)))/8
    wrong=np.maximum(0,2-np.abs(X))*np.maximum(0,2-np.abs(Y))/16
    fig,axes=plt.subplots(1,2,figsize=(7.8,3.45),constrained_layout=True)
    for ax,data,title in zip(axes,[joint,wrong],['Gemeinsame finale Uhr','Unabhängiges Produkt (anderes Maß)']):
        im=ax.imshow(data,extent=[-2,2,-2,2],origin='lower',vmin=0,vmax=.25,cmap='viridis')
        ax.set(xlabel='r = a − b',ylabel="r′ = a′ − b",title=title)
    fig.colorbar(im,ax=axes,shrink=.82,label='Dichte des Hilfsmaßes, L = 1')
    fig.savefig(figdir/'joint_relative_measure.png',dpi=180);plt.close(fig)

    p('Positive Historien<br/>und Schnittkonsistenz','title')
    p('CST-DUST · v0.1 · 7. November 2026','s')
    h('Ein positiver Kandidat - mit einer klaren Grenze')
    p('Aus der vorhandenen regulierten Amplitude ist ein <b>stark positives Hilfs-Dekohärenzfunktional</b> aufgebaut. Es verwendet vollständige relative Randdaten, einen gewählten Anfangszustand und ein ausdrücklich angenommenes positives Randprodukt.')
    p('<b>Der physikalische Abschluss bleibt offen.</b> Positivität allein begründet weder das Randprodukt noch eine konsistente Fortsetzung des Systems.')
    h('Neuer mathematischer Befund')
    p('Der beschränkte rohe Kern ist bei endlichen Regulatoren auf den deklarierten kontinuierlichen L²-Randräumen kompakt. Auf dem gesamten unendlichdimensionalen Eingangsraum kann er daher durch keinen einzigen positiven Normierungsfaktor isometrisch werden. Das gilt auch bei beschränkt äquivalenten positiven Randnormen.')
    table([['Ausgeführt','Aussage'],['Positives Historienfunktional','Konditionale Konstruktion mit offenem physikalischem Randprodukt'],['Gemeinsames Bra-/Ket-Maß','Finale Uhr koppelt beide Historien; unabhängige Reduktion ist nicht äquivalent'],['Kontinuierlicher Kernvergleich','Zwei normierte L²-Randfunktionen besitzen zertifiziert verschiedene Normfaktoren'],['Schnittkriterium','Erhaltung der Gramform auf dem tatsächlich erreichbaren Raum']], [177,332])
    p('<b>Alle acht physikalischen Gates bleiben HOLD.</b> Kein Nachweis eines globalen Bounce, einer Singularitätsauflösung oder eines physikalischen CST-Junction-Gesetzes. Der Befund ist kein allgemeines No-go für CST.','s')
    p('Basis: Main d9622fb0423725026fab73d6884a499322cb014f, nach PR 247. Vollständige Beweise, Quellen und rationale Zertifikate stehen im begleitenden Prüfpaket.','s')

    page();h('1 · Kandidatenvertrag und positive Form')
    p('Bei festem endlichem N bleiben vollständige Ordnungs-, Materie- und relative Uhrdaten erhalten. Die bestehende Wirkung, das atomar-stetige Dichtemaß und der Labelgruppenfaktor werden übernommen. Ereignisse E werden als Indikatoren in die vollständige gemeinsame Amplitude eingefügt.')
    eq('K<sub>E</sub>(b,a) = |G<sub>fix</sub>|<super>−1</super> Σ<sub>C</sub> ∫ dν(h) 1<sub>E</sub>(C,h,b,a) exp(iS/ℏ)')
    p('Die Randräume sind H<sub>in/out</sub> = L²(B<sub>in/out</sub>, dλ<sub>in/out</sub>) mit endlichen positiven Maßen. Sie sind Hilfsräume; ihre physikalische Vollständigkeit und die benötigte nichtlokale Vorgeschichte sind noch nicht bewiesen. Der Integraloperator zu K<sub>E</sub> heißt C<sub>E</sub>.')
    p('Für eine positive Anfangsdichte ρ mit Spur eins und einen beschränkten positiven Ausgangsoperator M gilt:')
    eq('D<sub>0</sub>(E,F) = Tr(ρ C<sub>E</sub><super>†</super> M C<sub>F</sub>)<br/>Z<sub>ρ</sub> = D<sub>0</sub>(Ω,Ω), &nbsp; D = D<sub>0</sub>/Z<sub>ρ</sub> für Z<sub>ρ</sub> &gt; 0')
    h('Beweis der starken Positivität')
    eq('Σ<sub>ij</sub> z̄<sub>i</sub>D(E<sub>i</sub>,E<sub>j</sub>)z<sub>j</sub><br/>= ‖M<super>1/2</super>(Σ<sub>i</sub>z<sub>i</sub>C<sub>Ei</sub>)ρ<super>1/2</super>‖<sub>HS</sub>² / Z<sub>ρ</sub> ≥ 0')
    p('Hermitizität folgt aus der Spurkonjugation; Biadditivität aus der Addition disjunkter Ereignisindikatoren. Normierung folgt aus Z<sub>ρ</sub>. Bei Z<sub>ρ</sub>=0 bleibt D undefiniert. Nullraumquotient und Vervollständigung ergeben einen Historien-Hilbertraum [1].')
    p('Die Konstruktion rechtfertigt ihre Eingaben nicht nachträglich. Insbesondere bleibt M eine physikalisch zu begründende Wahl. Die Motivation starker Positivität durch Komposition [2] entscheidet diese Wahl nicht.')
    h('Positivität ist noch keine Wahrscheinlichkeit')
    eq('μ(E∪F) = μ(E)+μ(F)+2 Re D(E,F), &nbsp; E∩F=∅')
    p('Die Diagonalen einer interferierenden Partition sind kein klassisches Wahrscheinlichkeitsmaß. Physikalisch geeignete Ereignisse und ihre Dekohärenz müssen zusätzlich qualifiziert werden.')

    page();h('2 · Die gemeinsame finale Uhr bleibt erhalten')
    p('Im Zweistellenproblem mit konstantem Eingangszustand identifiziert die positive Randkontraktion denselben finalen Uhrwert b in Bra und Ket. Es werden drei freie Uhren a, a′, b mit da da′ db/(2L)³ integriert.')
    eq('r = a−b, &nbsp; r′ = a′−b<br/>W<super>(2)</super><sub>L</sub>(r,r′) = [2L−max(0,r,r′)+min(0,r,r′)]<sub>+</sub>/(2L)³')
    p('Beweis: Bei festen Differenzen muss b gleichzeitig in drei verschobenen Intervallen liegen. Ihre gemeinsame Länge ist der Zähler. Der Jacobi-Faktor ist eins. Die beiden Marginalen sind Dreiecksmaße; sie sind jedoch korreliert.')
    story.append(Image(str(figdir/'joint_relative_measure.png'),width=509,height=225))
    eq('E[rr′] = L²/3; &nbsp; E[r²] = E[(r′)²] = 2L²/3')
    p('Das unabhängige Produkt der beiden Dreiecksmaße hätte E[rr′]=0. Es beschreibt daher eine andere Randkontraktion. Die Grafik zeigt ausschließlich das Hilfsmaß, keine vorhergesagten Staubzeitfluktuationen.')
    p('<b>75 exakte Momentprüfungen</b> vergleichen die direkte Binomialrechnung mit sechs Ordnungskammern für p,q=0,…,4 und L=1/2,1,2. Die zweite Rechnung integriert geordnete Abstände u,v über das Dreieck u+v≤2L.')
    p('Bei nichtkonstanten Zuständen, Ereignissen oder bereits fixierten Randuhren müssen diese Faktoren vor der Integration über den gemeinsamen Nullpunkt mitgeführt werden. W<super>(2)</super> allein genügt dann im Allgemeinen nicht. Es wird keine zusätzliche Uhrtranslation als Eichgruppe ausgemittelt.','s')

    page();h('3 · Schnittkriterium und Kompaktheitshindernis')
    p('V sei der erreichbare Spann der Ereignisvektoren v<sub>E</sub>. Wenn eine bereits hergeleitete lineare Fortsetzung J die gehobenen Vektoren Jv<sub>E</sub> erzeugt, bleibt die Gramform bis auf denselben Faktor c&gt;0 genau dann erhalten, wenn')
    eq('⟨v,(J<super>†</super>M′J−cM)w⟩ = 0 &nbsp; für alle v,w ∈ V.')
    p('Der Beweis folgt durch sesquilineare Fortsetzung der Ereignis-Grammatrix und Stetigkeit. Ein passender Faktor für den Gesamtvektor allein reicht nicht. Bei vollständigem V und M=M′=I lautet die Bedingung J<super>†</super>J=cI.')
    p('<b>21 exakte Kontrollen</b> erkennen unitäre und skaliert unitäre Beispiele. diag(1,2) versagt auf dem vollen zweidimensionalen Raum, besteht aber auf der ersten Achse. Der erreichbare Raum darf nicht ungeprüft vergrößert werden.')
    p('Für die vollständige nichtlokale CST-Geschichte ist ein solches J auf bloßen Randuhrwerten noch nicht hergeleitet. Der Satz gilt innerhalb der angegebenen Fortsetzungsdarstellung; er fordert nicht ungeprüft unitäre Markov-Evolution für jede kovariante Historientheorie.')
    h('Kontinuierlicher Satz für den rohen Kern')
    eq('|K(b,a)| ≤ M<sub>N</sub> &nbsp; ⇒ &nbsp; ∫|K|² dλ<sub>out</sub>dλ<sub>in</sub> &lt; ∞')
    p('Damit ist K Hilbert-Schmidt und kompakt. Für jede Orthonormalfolge φ<sub>n</sub> gilt φ<sub>n</sub>⇀0 und ‖Kφ<sub>n</sub>‖→0. Die Annahme K<super>†</super>K=cI würde hingegen für alle n die Norm √c verlangen: Widerspruch.')
    eq('‖K<super>†</super>K−cI‖<sub>op</sub> ≥ c, &nbsp; c&gt;0')
    p('Bei beschränkt äquivalenten positiven Randnormen bleibt der transformierte Kern ebenfalls kompakt. Auch dadurch entsteht keine Isometrie auf dem gesamten unendlichdimensionalen Hilfsraum.')
    p('<b>Reichweite:</b> Endliches N beziehungsweise endliche Sektorsumme, endliche Maße, beschränkter Kern, voller unendlichdimensionaler L²-Eingang. Eingeschränkte physikalische Sektoren, singuläre Kerne, unbeschränkte Umgewichtungen und kontrollierte Grenzprozesse bleiben offen. Endliche Rangprojektionen können beispielsweise stark gegen I konvergieren, ohne in Operatornorm zu konvergieren.','s')

    page();h('4 · Zertifizierter kontinuierlicher Zeuge')
    eq('K(b,a)=G(1/2+(b−a)²/4)<br/>G(q)=1/2 + (1/2)∫<sub>0</sub><super>1</super> exp(−iqw)dw')
    p('Verwendet wird die geerbte Zweistellenordnung: Anfangsdichte null, Enddichte atomar-stetig integriert. Die gemeinsame Gravitationsphase entfällt im Funktional. Das Rechenbeispiel wählt ausdrücklich L=1 und da/2, db/2; die frühere Hilfsbox L=4 wird nicht ersetzt.')
    p('Die orthogonalen Eingänge φ<sub>0</sub>(a)=1 und φ<sub>1</sub>(a)=√3 a haben beide Norm eins. Es sind echte L²-Funktionen, keine normierten Punktzustände.')
    table([['Größe','Zertifiziertes Intervall, konservativ verkürzt'],['Z₀ = ‖Kφ₀‖²','[0.94928176583590, 0.94928176583593]'],['Z₁ = ‖Kφ₁‖²','[0.00164658069420, 0.00164658069423]'],['Z₀ / (Z₀+Z₁)','[0.99826844924727, 0.99826844924730]']], [153,356])
    p('Ein mitgeführtes klassisches Präparationsetikett mit ursprünglichen Gewichten 1/2,1/2 erhält nach Konditionierung auf den erfolgreichen Filter das Gewicht etwa 0.998268 für Etikett 0. Das ist zulässige Nachselektion; es ist keine unveränderte unbedingte Dynamik.')
    h('Die geprüfte Historienpartition interferiert')
    p('Drei Anfangsuhrintervalle teilen bei ψ=1 den Bereich [-1,1] an −1/3 und 1/3. Ihre acht Vereinigungsereignisse werden mit vollständig integriertem Endwert berechnet. Das Gesamtfunktional ist normiert, aber')
    eq('Σ<sub>i=1</sub><super>3</super>D(E<sub>i</sub>,E<sub>i</sub>) ∈ [0.33390672525746, 0.33390672525750].')
    p('Eine reelle Offdiagonale ist zertifiziert positiv. Die Differenz zu eins ist Interferenz, kein Fehler der Gesamt-Normierung.')
    h('Zertifizierung')
    p('Die Wirkungsexponentialfunktion wird bis Grad p=40 integriert. Alle Koeffizienten und Integrale sind rational komplex. Auf dem Gebiet gilt q≤3/2, daher ist der gleichmäßige komplexe Rest')
    eq('r ≤ (3/2)<super>p+1</super> / [2(p+1)!(p+2)], &nbsp; ε<sub>Gram</sub> ≤ 2r+r².')
    p('Nenner werden positiv eingeschlossen; Dezimalgrenzen werden nach außen gerundet. Die angegebenen Intervalle sind keine statistischen Konfidenzintervalle und keine physikalische Präzisionsangabe.','s')

    page();h('5 · Prüfung, Aussagegrenzen und Fortsetzung')
    table([['Prüfung','Umfang / Ergebnis'],['Exakte Ereignisidentitäten','64 Hermitizität; 432 Biadditivität; 1 Normierung; 64 Grad-zwei-Identitäten'],['Positive quadratische Proben','64; allgemeine starke Positivität folgt aus dem Beweis'],['Unabhängige Polynomdarstellung','25 rationale Vergleiche'],['Gemeinsames relatives Maß','75 exakte Momentvergleiche'],['Schnitt-Positiv-/Negativkontrollen','21 exakte Kontrollen'],['Unabhängige Quadratur','26 Vergleiche; maximaler Unterschied 4.45×10⁻¹⁶; nicht zertifiziert'],['Isolierte Nachrechnung','5 exakte Ergebnisdateien bytegleich reproduziert']], [208,301])
    p('Die Ereignisidentitäten werden für die integrierten Taylorpolynome exakt geprüft; beim ungekürzten Kern folgen sie aus der allgemeinen Gramform. Die zusätzliche NumPy-Quadratur verwendet die geschlossene Dichteintegration und 64/96 Gauss-Legendre-Punkte.')
    h('Nächster physikalischer Modellschluss')
    p('Benötigt wird ein eigenständiger Vertrag für physikalische Randdaten und zulässige Zustände einschließlich der nötigen nichtlokalen Vorgeschichte. Danach muss eine begründete Fortsetzungs- oder Verfeinerungsabbildung die Gramform und den klassischen Grenzfall kontrollieren. Ein Randprodukt erst passend zum Kern zu definieren, löst die Auswahlfrage nicht.')
    p('Ein eingeschränkter Zustandssektor oder ein kontrollierter singulärer Grenzübergang sind mögliche Forschungsrouten; hier wird keine davon als erfolgreiche Lösung ausgegeben. Weitere Bounce-Rechnungen erhalten dadurch noch keine Freigabe.')
    p('<b>MODEL, CURRENT, CORRESPONDENCE, BOUNCE, REGULARITY, BOUNDARY, TRAPPING und EXTENSION: jeweils HOLD.</b> Keine neuen physikalischen 4D-Ensembles, keine gravitative Constraint-Herleitung und keine Singularitätsauflösung.')
    h('Reproduktion und Herkunft')
    p('Standardbibliothek: <font name="DVM">python3 -O -B analyze.py</font> und <font name="DVM">python3 -O -B replay.py</font>. Optional: <font name="DVM">verify_quadrature.py</font> mit NumPy. Fünf Vorgängertexte sind bytegleich auf Main nach PR 247 gepinnt.','s')
    p('Der lokale Plan wurde vor der Rechnung gehasht. Mechanismen waren bekannt; keine blinde Vorhersage oder externe Präregistrierung. Ein offener Nachtrag enthält die ergänzenden Maßmomente und Quadraturen. Keine Prüfung durch einen formalen Beweisassistenten.','s')
    p('[1] Dowker, Johnston, Sorkin (2010), Hilbert Spaces from Path Integrals. arXiv:1002.0589v3.<br/>[2] Dowker, Wilkes, An Argument for Strong Positivity of the Decoherence Functional. arXiv:2011.06120v2.<br/>[3] Dowker, Johnston, Surya (2010), On extending the Quantum Measure. arXiv:1007.2725v1. Die unendliche Historienfortsetzung bleibt eine eigene Frage.','s')
    doc=SimpleDocTemplate(str(ROOT/(NAME+'.pdf')),pagesize=(595.276,841.89),leftMargin=43,rightMargin=43,topMargin=43,bottomMargin=64,title='CST-DUST: Positive Historien und Schnittkonsistenz v0.1',author='X6 / Thomas Gfeller')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=lambda *a,**kw:canvas.Canvas(*a,**dict(kw,invariant=1)))
    print(ROOT/(NAME+'.pdf'))
if __name__=='__main__':main()
