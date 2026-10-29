"""German summary of the complete infinite-tail and global remainder calculation."""
import json,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flint import arb,ctx
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
HERE=Path(__file__).resolve().parent
NAVY=colors.HexColor('#16304b');TEAL=colors.HexColor('#127b82');MUTED=colors.HexColor('#526173');LIGHT=colors.HexColor('#edf4f5')
def upper(x,d=6,scale=1):
    v=arb(x).upper()/scale;n=int((v*10**d).upper().ceil().unique_fmpz());assert arb(n)/10**d>=v
    return f'{n//10**d},{n%10**d:0{d}d}'
def scientific(x):
    v=arb(x).upper();exponent=int(float(v.log()/arb(10).log())//1)
    return upper(v,6,10**exponent)+f' × 10<super>{exponent}</super>'
def build():
    ctx.prec=192;data=json.loads((HERE/'results/GLOBAL_192.json').read_text());checks=json.loads((HERE/'results/CHECKS.json').read_text());replay=json.loads((HERE/'REPLAY.json').read_text())
    assert checks['status']=='PASS' and replay['isolated_replay']=='PASS';report=HERE/'report';report.mkdir(exist_ok=True)
    rows=[r for w in data['windows'] for r in w['archives']];labels=[f'r{i} / W{w}' for w in range(2) for i in range(4)]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'cspp-v023'})
    fig,ax=plt.subplots(figsize=(8,3.05));xx=np.arange(8)
    ax.bar(xx-.17,[float(arb(r['v019_global_upper'])) for r in rows],.32,color='#b7c4cf',label='v0.19: bisherige globale Grenze')
    ax.bar(xx+.17,[float(arb(r['complete_global_upper'])) for r in rows],.32,color='#127b82',label='v0.23: neue vollständige Bilanz')
    ax.set_yscale('log');ax.set_ylim(1e-4,1e16);ax.set_yticks([1e-3,1,1e4,1e8,1e12,1e16]);ax.axhline(1e-3,color='#ae6b2a',ls='--',lw=1,label='Unverändertes Ziel 0,001')
    ax.set_xticks(xx,labels);ax.set_ylabel('Obere Schranke (log)');ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
    ax.spines[['top','right']].set_visible(False);ax.legend(loc='upper center',bbox_to_anchor=(.5,1.22),frameon=False,fontsize=8,ncols=2)
    fig.tight_layout();fig.savefig(report/'global_comparison.png',dpi=180);fig.savefig(report/'global_comparison.svg',metadata={'Date':None});plt.close(fig)
    fonts=Path('/usr/share/fonts/truetype/dejavu');pdfmetrics.registerFont(TTFont('DV23',str(fonts/'DejaVuSans.ttf')));pdfmetrics.registerFont(TTFont('DV23-Bold',str(fonts/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DV23',normal='DV23',bold='DV23-Bold',italic='DV23',boldItalic='DV23-Bold')
    st=getSampleStyleSheet()
    for name in ['BodyText','Heading1','Heading2']:st[name].fontName='DV23';st[name].textColor=NAVY
    st['BodyText'].fontSize=9.8;st['BodyText'].leading=14.5;st['BodyText'].spaceAfter=8
    st['Heading1'].fontSize=22;st['Heading1'].leading=28;st['Heading1'].spaceAfter=14
    st['Heading2'].fontSize=12;st['Heading2'].leading=17;st['Heading2'].textColor=TEAL;st['Heading2'].spaceBefore=10;st['Heading2'].spaceAfter=7
    st.add(ParagraphStyle(name='Small23',fontName='DV23',fontSize=8.2,leading=11.8,textColor=MUTED,spaceAfter=7))
    st.add(ParagraphStyle(name='Math23',fontName='DV23',fontSize=10.2,leading=17,textColor=NAVY,backColor=LIGHT,borderPadding=9,spaceBefore=7,spaceAfter=14))
    story=[]
    def p(text,style='BodyText'):story.append(Paragraph(text,st[style]))
    def table(rows,widths):
        t=Table([[Paragraph(str(x),st['Small23']) for x in r] for r in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#d9e0e6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.extend([t,Spacer(1,8)])
    p('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ 0.23','Small23');p('Unendlicher Rest,<br/>vollständige globale Bilanz','Heading1')
    p('<b>Schritt 2 ist abgeschlossen.</b> Der gesamte Rest für t &lt; −6 ist jetzt mit der endlichen Außenhistory aus v0.22 verbunden. Die neue obere Grenze ist etwa <b>7.000 bis 9.100 Mal kleiner</b> als die bisherige globale Majorante aus v0.19.')
    story.append(Image(str(report/'global_comparison.png'),width=483,height=184))
    table([['Archiv','W0 · Grenze × 10¹⁰','W1 · Grenze × 10¹⁰']]+[[data['windows'][0]['archives'][k]['key']]+[upper(w['archives'][k]['complete_global_upper'],6,10**10) for w in data['windows']] for k in range(4)],[133,175,175])
    p('Tabellenwerte sind nach oben gerundet. Vergleichsgegenstand beider Versionen: E(|A∞ − A₅| | feste Konfiguration in Ω₅). Die Grafik zeigt obere Grenzen, keine beobachteten Fehler.','Small23')
    p('<b>Die Genauigkeit ist weiterhin nicht nachgewiesen.</b> Rund 3,17 bis 3,75 × 10¹⁰ liegen noch mehr als 13 Größenordnungen über 0,001. METHOD und G1 bleiben <b>HOLD</b>; eine frische Bestätigung wurde nicht ausgeführt.')
    p('Die Verbesserung betrifft das mathematische Beweisinstrument. Eine große obere Schranke belegt weder große physikalische Fluktuationen noch die Untauglichkeit der Operatorfamilie.','Small23')
    story.append(PageBreak())
    p('01 / Vollständige und disjunkte Zerlegung','Small23');p('Kein offener Wurzelbereich mehr','Heading1')
    p('Die physikalische History bleibt unverändert. Mit τ = −t − 1 werden ihre außerhalb Ω₅ liegenden Wurzeln an τ = 5 geteilt:')
    table([['Gebiet','Behandlung'],['0 ≤ τ ≤ 5','Vollständige endliche Grenze aus v0.22, unverändert übernommen. Für τ ≤ 7/4 ist der Außenbeitrag exakt null.'],['τ > 5','Neue unendliche Restgrenze auf dem gesamten KG-Träger und in allen Raumrichtungen.'],['τ = 5','Nullrand; keine positive Vierervolumenmasse und fast sicher keine äußeren Poissonpunkte.']],[115,368])
    p('E(|Δ| | Ω₅) ≤ B<sub>endlich, v0.22</sub> + B<sub>unendlich, v0.23</sub>','Math23')
    p('Der frühere Patch ist bereits einmal im endlichen Anteil enthalten. Die beiden Beiträge dürfen korreliert sein; die Dreiecksungleichung benötigt keine Unabhängigkeit. Es wird keine obere Schranke von einer anderen subtrahiert und der endliche Anteil nicht nochmals transportiert.')
    p('Eine engere nahe Konturhülle','Heading2')
    p('Die Fourierkontur wird um iδ verschoben. Eine positive radiale Integration liefert Potenzhüllen mit Exponenten <b>p = J − 3/4</b>. Die vorhandenen validierten Quellnormen werden wiederverwendet. Alle Hüllen gelten ab der festgelegten Grenze; ein unbekannter asymptotischer Übergang wird nicht vorausgesetzt.')
    p('Die Familie J = 1,…,34 und δ = j/16 für j = 1,…,15 wird über die vollständigen Zeitintervalle [5,8], [8,16], … und einen letzten analytischen Rest bis unendlich integriert. Gewählt werden gültige integrierte Obergrenzen, keine Mittelpunktwerte.')
    p('Eine neue L²-Grenze im fernen Teil','Heading2')
    p('Für s = (p<sub>t</sub> − y<sub>t</sub>)² − |p − y|² trennt s = √τ den nahen und fernen Teil. Im fernen Teil nutzt die Rechnung ||U(t)||₂ ≤ ||f||₂ und Cauchy-Schwarz in Raum und Zeit. Die verbleibenden positiven Kernmomente werden bis unendlich mit Gammafunktionen eingeschlossen.')
    p('Quelle, Masse, Dichte, Schichtkernel, Detektor, Wolken und statistische Regeln bleiben unverändert. δ, J und die Integrationszerlegung sind Hilfsgrößen des Beweises.','Small23')
    story.append(PageBreak())
    p('02 / Transport und dominierender Rest','Small23');p('Alle Pfadklassen bleiben enthalten','Heading1')
    p('Die Tail-Grenze wird für sämtliche <b>223 bekannten aktiven Endpunkte</b> einzeln eingeschlossen. Hinzu kommen je Fenster <b>128 Detektorzellen</b> mit exakt normierten Massen. Unbekannte aktive Außenpfade erhalten dieselbe Mecke-Pfadmajorante wie bisher.')
    p('B<sub>unendlich</sub> = B<sub>direkt</sub> + Σ |a<sub>j</sub>| F<sub>tail,j</sub> + B<sub>unbekannt</sub>','Math23')
    example=[w['archives'][2] for w in data['windows']]
    rr=[['d0_r02 · Beitrag','W0 · obere Grenze','W1 · obere Grenze']]
    for label,key in [('Endlich, v0.22','finite_v022_upper'),('Unendlich: direkt','direct_tail_upper'),('Unendlich: bekannte Pfade','known_active_tail_upper'),('Unendlich: unbekannte Pfade','unknown_active_tail_upper'),('Vollständige globale Bilanz','complete_global_upper')]:rr.append([label]+[scientific(r[key]) for r in example])
    table(rr,[185,149,149])
    p('Alle Werte nach oben gerundet. Einzelne gerundete Teilwerte müssen sich nicht exakt zum separat gerundeten Gesamtwert summieren. Die vollständigen Intervallzahlen liegen im Prüfpaket.','Small23')
    p('Der Engpass ist jetzt eindeutig','Heading2')
    p('Die Bilanz wird von der konservativen Hülle nahe dem Lichtkegel im unendlichen Bereich bestimmt. Der bereits eingeschlossene endliche Beitrag von etwa 0,48 bis 0,55 ist darin klein. Die neue L²-Methode verkleinert den fernen Teil deutlich; sie beseitigt die breite nahe Hülle noch nicht.')
    p('Für jeden Endpunkt bleibt der erste Schichtkernel durch eine gültige bedingte Hülle begrenzt. Die tatsächlichen archivabhängigen Zählkerne und Feldaufhebungen werden auf dem ganzen unendlichen Gebiet noch nicht exakt gemeinsam integriert.')
    p('Die ergänzende Tabelle für weiter entfernte Reste τ &gt; 2ʲ zeigt abfallende Obergrenzen. Sie ersetzt keinen Zwischenbereich: Die vollständige Bilanz verwendet immer den Rest ab τ = 5. Große ausreichende Grenzen sind keine Empfehlung für größere Poissonwolken.','Small23')
    story.append(PageBreak())
    p('03 / Prüfung und Anschlussentscheidung','Small23');p('Reproduziert, weiterhin HOLD','Heading1')
    c=checks['counts']
    table([['Prüfung','Ergebnis'],['Eingabeidentität',f'{c["source_files"]} unveränderte Dateien: SHA256 und Git-Blobs'],['Quellnormen','35 Intervalle: Überlappung der archivierten 384-/512-Bit-Läufe'],['Unabhängige Quadraturen','12 Fourier-, 12 Kernmoment-, 19 Potenz- und 6 Far-Polynomintegrale'],['Algebra und Poisson','34 Halbzahl-Gammaidentitäten; 12 direkte Poissonsummen mit Rest'],['Vollständige Bilanz',f'{c["endpoint_audits_checked"]} Endpunkt-Audits; {c["global_decompositions"]} globale Zerlegungen über beide Präzisionen'],['Isolierte Wiederholung',f'{replay["byte_identical_result_files"]} numerische Ergebnisdateien bytegenau identisch'],['Negativkontrollen','Fehlender Anfangsstreifen, Detektorschale, Außenpfade und falscher Fourierfaktor erkannt']],[158,325])
    p('Die Rechnung verwendet 128 und 192 Bit. Kleine arithmetische Radien beschreiben die Recheneinschließung, nicht die Schärfe der Fehlermajorante. Ein unabhängiges wissenschaftliches Review wurde nicht durchgeführt.','Small23')
    p('Was Schritt 3 jetzt berücksichtigen muss','Heading2')
    p('Die endliche und unendliche Außenhistory sind vollständig bilanziert. Für eine Genauigkeitsfreigabe bleibt die nahe Tail-Majorante viel zu grob. Eine gezielte Schärfung oder eine belastbare Fehlerdiagnose muss vor einer neuen Bestätigungsstichprobe kommen. Aus der jetzigen oberen Grenze folgt keine begründete Aufgabe der Operatorfamilie.')
    p('Reproduktion und Quellen','Heading2')
    p('Im entpackten Verzeichnis: <b>python3 reproduce.py</b><br/>Nur Prüfungen: <b>python3 reproduce.py --quick</b><br/>Python 3.12.14 · python-flint 0.8.0 · NumPy 2.3.5','Small23')
    p('Die vollständige Herleitung steht in PROOF.md. PROVENANCE.json, REPLAY.json und results/CHECKS.json dokumentieren Herkunft und Prüfung. Basis: Main fdf99cd95330 nach PR #154.','Small23')
    p('Primärgrundlagen: <link href="https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf" color="#127b82">Last/Penrose, Theorem 4.4</link>; <link href="https://dlmf.nist.gov/8.2#E2" color="#127b82">DLMF 8.2.2</link>; <link href="https://dlmf.nist.gov/13.4#E1" color="#127b82">DLMF 13.4.1</link>. Die neuen Schranken und die konkrete Bilanz sind eigene Herleitungen. Quellenstand: 29.10.2026.','Small23')
    def footer(can,doc):
        can.setStrokeColor(TEAL);can.line(56,49,539,49);can.setFont('DV23',8);can.setFillColor(MUTED);can.drawString(56,34,'CSPP v0.23 · Globale Außenhistory · METHOD / G1: HOLD');can.drawRightString(539,34,str(doc.page))
    class FixedCanvas(canvas.Canvas):
        def __init__(self,*a,**kw):kw['invariant']=1;super().__init__(*a,**kw)
    path=report/'Unendlicher_Rest_Globale_Bilanz_v0_23.pdf';doc=SimpleDocTemplate(str(path),pagesize=(595.276,841.89),leftMargin=56,rightMargin=56,topMargin=45,bottomMargin=65,title='CSPP v0.23 - Unendlicher Rest und globale Bilanz',author='CSPP research workflow')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=FixedCanvas)
    out=HERE.parent/'output/pdf';out.mkdir(parents=True,exist_ok=True);shutil.copy2(path,out/path.name);print(path)
if __name__=='__main__':build()
