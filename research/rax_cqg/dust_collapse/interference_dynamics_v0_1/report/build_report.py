from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'CST_DUST_Interferenz_Randantwort_Dynamikpruefung_v0_1.pdf'
weights=json.loads((ROOT/'checks/full_weight/results.json').read_text())
combined=json.loads((ROOT/'checks/combined_response/results.json').read_text())
font='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV',font+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB',font+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
ink=HexColor('#142b3b');teal=HexColor('#067f81');muted=HexColor('#4b6170');light=HexColor('#eef5f6')
styles={
 'title':ParagraphStyle('title',fontName='DVB',fontSize=25,leading=30,textColor=ink,spaceAfter=15),
 'sub':ParagraphStyle('sub',fontName='DV',fontSize=11,leading=16,textColor=muted,spaceAfter=14),
 'h':ParagraphStyle('h',fontName='DVB',fontSize=16,leading=21,textColor=teal,spaceAfter=13),
 'h2':ParagraphStyle('h2',fontName='DVB',fontSize=11,leading=15,textColor=ink,spaceBefore=8,spaceAfter=6),
 'p':ParagraphStyle('p',fontName='DV',fontSize=9.4,leading=13.7,textColor=ink,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='DV',fontSize=8,leading=11.2,textColor=muted,spaceAfter=6),
 'math':ParagraphStyle('math',fontName='DV',fontSize=10,leading=16,textColor=ink,backColor=light,borderPadding=9,spaceBefore=5,spaceAfter=13),
 'cell':ParagraphStyle('cell',fontName='DV',fontSize=8.4,leading=11.7,textColor=ink),
 'th':ParagraphStyle('th',fontName='DVB',fontSize=8.4,leading=11.7,textColor=white),
}
story=[]
def p(t,k='p'):story.append(Paragraph(t,styles[k]))
def page():story.append(PageBreak())
def table(rows,widths):
 data=[[Paragraph(str(x),styles['th' if i==0 else 'cell']) for x in row] for i,row in enumerate(rows)]
 t=Table(data,colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),ink),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[light,white])]))
 story.extend([t,Spacer(1,10)])
def cx(v,d=6):return f"{float(v['real']):.{d}f} {'+' if float(v['imag'])>=0 else '-'} {abs(float(v['imag'])):.{d}f} i"

p('CST-DUST · N11 · Version 0.1 · 13. November 2026','sub')
p('Interferenz, Randantwort<br/>und Dynamikprüfung','title')
p('Drei Aufgaben ausgeführt: vollständige innere Gewichte,<br/>Auslesestruktur und konsistente Zusammensetzung.','sub')
p('<b>Ergebnis:</b> Unter einem ausdrücklich festgelegten gemeinsamen Dirichlet-/Boxvertrag ist die vollständige innere Uhr-/Dichteamplitude berechnet. Sie verändert sowohl Betrag als auch Phase des relativen Geometriebeitrags. Eine komplexe skalare Randantwort lässt sich daraus reproduzierbar bestimmen.','p')
p('|W₁/W₀|: &nbsp;1,60555 → 1,86937<br/>bei ρ: &nbsp;1/8 → 1/4.','math')
table([['Aufgabe','Ausgeführtes Ergebnis','Physikalische Reichweite'],['Vollständiges Gewicht','Alle acht inneren Dichtestrata und drei Uhren integriert; Randwirkung erhalten','Gilt für gewählten Uhrträger und feste äußere Daten'],['Auslese begründen','Positive endliche Dekohärenzmodelle und vollständige bedingte Instrumente konstruiert','Wirkung wählt Historiengewichte und Records nicht eindeutig aus'],['Dynamik prüfen','Zwei Schnitte und dreiteilige Zusammensetzung exakt geschlossen','Vollständiges Gedächtnis; keine abgeleitete physische Zeitentwicklung']],[109,195,186])
p('<b>Die physikalische Geometriedynamik bleibt offen.</b> Der neue Befund ist stärker als ein stationärer Phasenvergleich: Wir kennen jetzt eine vollständige endliche Randamplitude im deklarierten Modell. Noch fehlen ihre ausgezeichnete physikalische Paarung und eine geometrisch kalibrierte Verlaufsdeutung.','p')
p('Sechs Fachagenten, eigenständige algebraische Kontrollen und unabhängiger Quadraturaudit. Interne KI-gestützte Prüfung, keine externe Begutachtung. Ausgangspunkt ist der veröffentlichte stationäre Kandidat auf main, Commit da48df345a20b3922b5764ad795e3bf2444d9bb4.','small')

page();p('1  Das vollständige innere Gewicht','h')
p('Die Wirkung bleibt unverändert. C₀ ist die Kette mit elf Ereignissen; C₁ entfernt nur (4,5) und (5,6), behält (4,6). Das Innere ist I={4,5,6}, der gemeinsame Rand B={0,1,2,3,7,8,9,10}. β=4/√6; b=(1,-9,16,-8), danach null.','p')
p('Cⱼ(T)=1+(β/2)Σ<sub>i≺j</sub>bᵢⱼ(Tⱼ-Tᵢ)²<br/>S=F(C)-½ΣⱼrⱼCⱼ(T)-(β/4)Σ<sub>i≺j</sub>bᵢⱼ(qⱼ-qᵢ)²','math')
p('Am Rand gelten Tⱼ=(j-5)Δ mit Δ²=√6/38 und rⱼ=ρ. Für jede innere Uhr wählen wir dT/3 auf [-3/2,3/2]; für jede innere Dichte bleibt dν=(δ₀+1<sub>(0,1)</sub>dr)/2. Es wird kein zusätzliches Ordnungs-Theta eingeführt: Auch nichtmonotone Uhrkonfigurationen gehören zur Integration. Dies ist die ausdrücklich gewählte optionale Fortsetzung des Vorgängerpakets.','p')
p('D(C)=∫exp(-irC/2)dν(r)=½+(1-exp(-iC/2))/(iC), &nbsp;D(0)=1.<br/>W<sub>c</sub>(ρ)=exp(iF<sub>c</sub>) ∫<sub>Box</sub>(d³T/27)<br/>× exp[-iρ Σ<sub>j∈B</sub>Cⱼ(T)/2] Π<sub>j∈I</sub>D(Cⱼ(T)).','math')
p('Das Produkt enthält genau acht Atom-/Positivkombinationen, mit je 1/8 vor der kontinuierlichen Integration. Feste Randkragenbeiträge sind vollständig enthalten. Die äußeren Dichten und Uhren werden nicht als Randpakete integriert.','p')
rows=[['Quelle ρ','W₀: Kette','W₁: Alternative']]
for rho in ['1/8','1/4']:
 rows.append([rho,*[cx(weights['quadrature'][c][-1]['sources'][rho]['W']) for c in ['chain','two_cover_deleted']]])
table(rows,[70,210,210])
p('<b>Keine zweite stationäre Phase:</b> W enthält bereits F und sämtliche Staub-/Uhrphasen. Die korrekte Gesamtamplitude ist a<sub>c</sub>=ω<sub>c</sub>W<sub>c</sub>g<sub>c</sub>. Eine weitere Multiplikation mit exp(iS<sub>on</sub>) würde dieselbe Wirkung doppelt zählen.','p')
p('ρ verändert die Dichten sowohl des vergangenen als auch des zukünftigen Kragens. Die Rechnung untersucht eine beidseitige Randparameterantwort, keine isolierte Anfangsstörung bei festem späteren Filter. ρ ist weder Zeit noch kalibrierte Masse.','small')

page();p('2  Interferenz und skalare Randantwort','h')
p('Die Wirkung und die festgelegten Maße zerfallen exakt in Skalar- und Uhr-/Dichteteil. Der gemeinsame skalare Schwartz-Test ist f<sub>B</sub>=π⁻² exp(-|q<sub>B</sub>|²/2), L²-normiert bezüglich des Hilfs-Lebesgue-Maßes. Das ist keine bereits hergeleitete physikalische Norm. Der Abel-Regulator wirkt auf alle drei inneren Skalarvariablen.','p')
p('g₁/g₀=0,3297873431+0,1726821549 i<br/>h₀=0,04148882883-0,06239920545 i<br/>h₁=0,12580792249-0,09864166841 i','math')
p('h<sub>c</sub> bezeichnet die auf g<sub>c</sub> normierte Einsetzung q₀q₁₀. Beide Werte folgen aus dem entsprechenden Randblock der inversen Gaußmatrix. Der singuläre Innenblock von C₁ wird über eine Delta-Distribution und die gemeinsame Randpaarung behandelt. Ein Quotient ungepaarter Distributionen wird nicht verwendet.','p')
p('R=(ω₁W₁g₁)/(ω₀W₀g₀), &nbsp; H=(h₀+Rh₁)/(1+R).<br/>H′=(h₁-h₀)R[W₁′/W₁-W₀′/W₀]/(1+R)²','math')
p('Für die folgende Diagnose setzen wir <b>ω₀=ω₁=1, fest und quellenunabhängig</b>. Diese Gleichgewichtung ist eine erklärte Referenz, keine aus der Wirkung hergeleitete Wahl.','p')
rows=[['Größe','ρ=1/8','ρ=1/4']]
for label,key in [('Relative Amplitude R','relative_amplitude_R'),('Rand-Einsetzung H','complex_q0q10_insertion'),('Quellenableitung H′','insertion_source_derivative')]:
 rows.append([label,*[cx(combined['results'][r][key]) for r in ['1/8','1/4']]])
table(rows,[120,185,185])
p('Der Kontrast beträgt ΔH≈-0,02969735+0,05745731 i. Die Phasensteigung Im ∂<sub>ρ</sub>log(W₁/W₀) ist ≈2,29840 bzw. 1,72661; die stationäre Näherung hätte lediglich 23/19≈1,21053 geliefert. Auch Re ∂<sub>ρ</sub>log(W₁/W₀) ist ungleich null: Der Betrag verändert sich.','p')
p('<b>Interpretation:</b> H ist eine komplexe Lorentzsche Amplituden-Einsetzung. Sie darf nicht als positive Kovarianz oder bereits vorhergesagter Messwert ausgegeben werden. Bei 1+R=0 wäre die normierte Einsetzung undefiniert; an beiden geprüften Punkten ist der Nenner deutlich von null entfernt.','small')

page();p('3  Auslese: konstruiert, aber nicht ausgezeichnet','h')
p('Für die beiden endlichen Historien lässt sich eine konsistente Familie von Recordmodellen angeben. Sei γ die Überlappung der beiden Recordzustände. Dann gilt','p')
p('η=[[1,γ],[γ*,1]], &nbsp; |γ|≤1.<br/>D=diag(a₀,a₁) η diag(a₀,a₁)† ≥ 0.<br/>Z=D(Ω,Ω)=Σ<sub>c,d</sub>D<sub>cd</sub>.','math')
p('Bei Z&gt;0 ist D/Z ein normiertes stark positives Dekohärenzfunktional auf der endlichen Zweihistorien-Ereignisalgebra. Die Konstruktion ist mathematisch konsistent, bestimmt aber weder das physische Historienmaß noch γ. Eine konsistente Fortsetzung auf weitere Historien wird damit nicht bewiesen.','p')
table([['Auslesevertrag','Folge'],['γ=1: gemeinsamer kohärenter Record','Kreuzterm bleibt; geometrische Einzelalternativen sind im Allgemeinen nicht konsistent probabilistisch auflösbar'],['γ=0: orthogonale Geometrierekords','Kreuzterm verschwindet; bedingte Geometriewahrscheinlichkeiten proportional |a<sub>c</sub>|²'],['Endliches Instrument mit Failure-Ausgang','Für hinzugefügten endlichen Eingangsraum und gemeinsamen ausreichend kleinen Gain vollständig positiv und spurtreu vervollständigbar']],[185,305])
p('Die Instrument-Vervollständigung ist ausdrücklich ein äußerer Detektorvertrag. Sie liefert keine Herleitung des physikalischen Zustandsraums aus der ursprünglichen Gravitation–Materie-Wirkung. Die festen äußeren Dichte-/Uhrwerte sind außerdem Dirichlet-Daten, keine normierten physikalischen Zustände.','p')
p('Eine scharfe Negativkontrolle: a=(1,-1/2), γ=1 ergibt Z=1/4. Die vermeintlichen Einzelwahrscheinlichkeiten D₀₀/Z und D₁₁/Z wären 4 und 1. Positivität allein rechtfertigt daher nicht die Interpretation der Diagonalen als exklusive kohärente Geometrieausgänge. D/tr(D) kann eine andere Dichtematrix-Konstruktion definieren, ersetzt aber nicht D/Z.','p')
p('Auch die Gewichte sind nicht identifiziert: Für beliebige nichtverschwindende W<sub>c</sub>g<sub>c</sub> kann ein positives Verhältnis ω₁/ω₀ an einem festen Quellenwert jede aufgelöste Fraktion p∈(0,1) erzeugen. Die unveränderte Wirkung lässt somit verschiedene bedingte Vorhersagen zu, solange Maß und Auslesevertrag frei bleiben.','p')
p('Die ursprüngliche Dichteintegration löst das nicht: C·D(C) verschwindet nicht identisch. Sie ist kein Delta-Constraint-Projektor. Ein Group-Averaging-Verfahren würde eine begründete erstklassige Constraintstruktur voraussetzen; diese wurde hier nicht hergeleitet.','small')

page();p('4  Zusammensetzung und geometrische Observable','h')
p('Die Wirkung wird nach dem späteren Ereignis j zerlegt. Dabei bleibt jeder Beitrag eines über den Schnitt reichenden Paares genau einmal erhalten:','p')
p('sⱼ=1-rⱼ/2-Σ<sub>i≺j</sub>bᵢⱼ<br/>- (β/4)Σ<sub>i≺j</sub>bᵢⱼ[rⱼ(Tⱼ-Tᵢ)²+(qⱼ-qᵢ)²],<br/>S=Σⱼsⱼ.','math')
p('Ein hinreichender Gedächtniszustand enthält die vollständige vergangene Kausalrelation und die noch benötigten Felder. Kopierkerne erhalten diese Daten; jedes Integrationsmaß und jeder Abel-Faktor wird nur einmal zugeordnet. Für ε&gt;0 erlaubt absolute Integrabilität die Zusammensetzung. Der Grenzwert wird erst nach gemeinsamer Randpaarung genommen.','p')
table([['Kontrolle','Befund'],['22 Präfixidentitäten','Alle rationalen Wirkungsmonome stimmen exakt überein'],['Schnitte nach Ereignis 3 und 5','Beide Ordnungen geprüft: vier exakte Schnittidentitäten'],['Naives Produkt ohne Kreuzbeiträge','Scheitert an allen vier Schnitten; allein der fehlende Gravitationsbeitrag ist 1 bzw. 9'],['Dreiteilige Zusammensetzung','Assoziativ mit voller Schnittinformation und einmaligem Maß'],['Verschiedene natürliche Beschriftungen','Gleiche vollständige Wirkung; keine physische Zeit aus der Beschriftung abgeleitet']],[180,310])
p('Als intrinsische Observable verwenden wir O=Zahl vergleichbarer Paare im dreielementigen Inneren: O(C₀)=3, O(C₁)=1. Sie ist unter randtreuen Umbenennungen invariant. Sie ist kein arealer Radius und kein räumliches Volumen.','p')
p('Nur für den gesonderten aufgelösten Recordvertrag γ=0 gilt<br/>E[O|Record,Erfolg]=(3+Λ)/(1+Λ), &nbsp;Λ=|a₁/a₀|².<br/>Bei gleichen festen Gewichten: 2,473594 → 2,347464.','math')
p('Dieser bedingte Mittelwert reagiert auf den Betrag der vollständigen Amplituden. Eine reine Änderung der relativen Phase würde ihn unverändert lassen. Die kohärente Ratio (3a₀+a₁)/(a₀+a₁) ist dagegen im Allgemeinen komplex und kein Born-Mittelwert. Beide Ausleseverträge dürfen nicht vermischt werden.','p')
p('<b>Grenze:</b> Exakte Komposition mit voller Vergangenheit ist noch keine abgeschlossene Evolution auf einem reduzierten physikalischen Randzustandsraum. Ein bevorzugtes Historienmaß, physische Zeit, Stabilität, Verfeinerung und vierdimensionale Staubball-Korrespondenz folgen daraus nicht.','small')

page();p('5  Fehlerkontrolle und präziser Restauftrag','h')
p('Die Dichteintegration und ihre Zerlegung in acht Strata sind exakt. Die drei Uhrintegrationen werden mit positiver normierter Gauß-Legendre-Tensorquadratur berechnet: n=64,96,128,160 pro Achse. Der komplexe Integrand ist in jeder Uhrvariablen ganz. Ein Chebyshev-Rest auf der Bernsteinellipse R=7/4 liefert eine unabhängige Trunkationsschranke.','p')
p('|I-Q<sub>n</sub><sup>⊗3</sup>| ≤ Σ<sub>k=1</sub><sup>3</sup>4 exp(L<sub>k</sub>) R⁻²ⁿ/(1-R⁻¹).','math')
p('Für 0≤ρ≤1/4 und n=160 beträgt die obere Schranke für W weniger als 1,2·10⁻²⁵ (Kette) bzw. 1,6·10⁻³² (Alternative). Die Dezimaloberschranken werden zusätzlich durch rationale Taylor-Abschätzungen zertifiziert. Die entsprechenden analytischen Schranken für W′ sind im Prüfpaket enthalten.','p')
p('<b>Wichtig:</b> Dies sind Grenzen des mathematischen Quadraturrests. Die tatsächliche Auswertung erfolgt mit Float64; Knoten-, Funktions- und Rundungsfehler sind nicht vollständig durch Intervallarithmetik eingeschlossen. n=128 und n=160 unterscheiden sich hier um etwa 10⁻¹⁵ bei W und 10⁻¹⁴ bei W′. Die angegebenen Zahlen sind reproduzierbar kontrollierte Näherungen, keine vollständigen Intervallzertifikate.','p')
table([['Was jetzt vorliegt','Was daraus noch nicht folgt'],['Volles inneres Uhr-/Dichtegewicht im gemeinsamen Vertrag','Ein ausgezeichnetes physikalisches Maß oder normierte äußere Staub-/Uhrpakete'],['Nichtverschwindender bedingter Randkontrast','Eine eindeutige physische Messkorrelation'],['Positive vollständige endliche Auslesemodelle','Welcher Detektorvertrag aus der Gesamtwirkung hervorgeht'],['Exakte Zusammensetzung mit vollständigem Gedächtnis','Eine reduzierte, kalibrierte vierdimensionale Geometriedynamik']],[245,245])
p('Der verbleibende entscheidende Auftrag ist die Ableitung eines gemeinsamen physikalischen Rand- und Auslesevertrags aus einer erweiterten oder präzisierten Theorie. Er muss Historiengewichte, Staub-/Uhr-Randpakete, Recordkopplung und konsistente Komposition gemeinsam festlegen. Mit dem jetzigen Paket lassen sich solche Kandidaten unmittelbar am vollständigen Kern prüfen. Ein bloßer weiterer Phasenvergleich kann diese Auswahl nicht ersetzen.','p')
p('Reproduktion: <b>python -m pip install -r requirements.txt</b>; danach <b>python -B verify.py</b>. Der Prüfer kontrolliert die Dateihashes, führt acht Programme in einer isolierten Kopie aus und vergleicht die Ergebnisse. Report-Erzeugung benötigt zusätzlich reportlab.','small')
p('Primärliteratur zur begrifflichen Einordnung: D. Giulini, <i>Group Averaging and Refined Algebraic Quantization</i> (2000), arxiv.org/abs/gr-qc/0003040. F. Dowker, S. Johnston, S. Surya, <i>On extending the Quantum Measure</i> (2010), arxiv.org/abs/1007.2725. Die neuen endlichen Rechnungen sind eigene Ableitungen im Prüfpaket; die Literatur wird nicht als Beweis dieser Ergebnisse ausgegeben.','small')

def footer(c,doc):
 c.saveState();c.setStrokeColor(teal);c.line(42,41,553,41);c.setFont('DV',7);c.setFillColor(muted)
 c.drawString(42,28,'CST-DUST · Vollständige innere Randamplitude · Physikalische Dynamik offen')
 c.drawRightString(553,28,str(doc.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=49,rightMargin=49,topMargin=46,bottomMargin=55,title='CST-DUST: Interferenz, Randantwort und Dynamikprüfung v0.1',author='Thomas Gfeller · Forschungsprogramm; KI-gestützte Ausarbeitung')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
