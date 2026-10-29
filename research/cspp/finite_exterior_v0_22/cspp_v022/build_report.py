"""Deterministic German report and scientific coverage figure."""
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
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
HERE=Path(__file__).resolve().parent
NAVY=colors.HexColor('#16304b');TEAL=colors.HexColor('#127b82');MUTED=colors.HexColor('#526173');LIGHT=colors.HexColor('#edf4f5')
def upper(x,d=6):
    value=arb(x).upper();integer=int((value*10**d).upper().ceil().unique_fmpz());assert arb(integer)/10**d>=value
    return f'{integer//10**d},{integer%10**d:0{d}d}'
def approximate(x,d=3):return f'{float(arb(x)):.{d}f}'.replace('.',',')
def build():
    ctx.prec=192;data=json.loads((HERE/'results/FINITE_192.json').read_text());checks=json.loads((HERE/'results/CHECKS.json').read_text());replay=json.loads((HERE/'REPLAY.json').read_text())
    assert checks['status']=='PASS' and replay['isolated_replay']=='PASS'
    fine=data['levels'][-1];report=HERE/'report';report.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'cspp-v022'})
    fig,ax=plt.subplots(figsize=(8,4.1));tau=np.linspace(1.75,5,700);low=np.maximum(0,4-tau);outer=tau+.5;inner=np.maximum(low,tau-.5)
    ax.fill_between(tau,low,inner,color='#b5d9db',label='Tiefes Inneres')
    ax.fill_between(tau,inner,outer,color='#efa264',label='Wellenfront')
    ax.plot(tau,outer,color='#16304b',lw=1.2);ax.plot(tau,low,color='#16304b',lw=1.2)
    ax.plot(tau,tau-.5,color='#b36a31',lw=1,ls='--');ax.axvline(4,color='#8a949d',lw=.8,ls=':')
    ax.set(xlim=(1.6,5.12),ylim=(0,5.8),xlabel='Historykoordinate τ = −t − 1',ylabel='Radius R = |x|')
    ax.text(2.15,1.0,'In Ω₅',color='#65758a');ax.text(4.3,2.1,'D₅',fontsize=17,color='#16304b')
    ax.text(2.7,4.7,'Außerhalb des KG-Trägers: U = 0',fontsize=9,color='#65758a')
    ax.legend(loc='upper left',frameon=False,ncol=2);ax.spines[['top','right']].set_visible(False)
    fig.tight_layout();fig.savefig(report/'coverage.png',dpi=180);fig.savefig(report/'coverage.svg',metadata={'Date':None});plt.close(fig)
    font=Path('/usr/share/fonts/truetype/dejavu');pdfmetrics.registerFont(TTFont('DejaVu',str(font/'DejaVuSans.ttf')));pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(font/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
    styles=getSampleStyleSheet()
    for name in ['Normal','BodyText','Heading1','Heading2','Title']:styles[name].fontName='DejaVu'
    styles['BodyText'].fontSize=10;styles['BodyText'].leading=15;styles['BodyText'].textColor=NAVY;styles['BodyText'].spaceAfter=8
    styles['Heading1'].fontSize=21;styles['Heading1'].leading=27;styles['Heading1'].textColor=NAVY;styles['Heading1'].spaceAfter=15
    styles['Heading2'].fontSize=12;styles['Heading2'].leading=17;styles['Heading2'].textColor=TEAL;styles['Heading2'].spaceBefore=12;styles['Heading2'].spaceAfter=7
    styles.add(ParagraphStyle(name='SmallCustom',fontName='DejaVu',fontSize=8.3,leading=12,textColor=MUTED,spaceAfter=7))
    styles.add(ParagraphStyle(name='FormulaCustom',fontName='DejaVu',fontSize=10,leading=16,textColor=NAVY,backColor=LIGHT,borderPadding=10,spaceBefore=8,spaceAfter=14))
    story=[]
    def p(t,style='BodyText'):story.append(Paragraph(t,styles[style]))
    def table(rows,widths):
        cooked=[[Paragraph(str(x),styles['SmallCustom']) for x in row] for row in rows]
        t=Table(cooked,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#d9e0e6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]));story.append(t);story.append(Spacer(1,9))
    p('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ 0.22','SmallCustom')
    p('Vollständige endliche<br/>Außenhistory','Heading1')
    p('<b>Schritt 1 ist abgeschlossen.</b> Die Rechnung erfasst die gesamte äußere History von t = −6 bis zur Anfangszeit −1, einschließlich aller räumlichen Flanken und der Wellenfront. Der ältere Patch ist darin genau einmal enthalten.')
    p('Ergebnis und Freigabestatus','Heading2')
    p('Die neuen oberen Grenzen liegen über beide Detektorfenster bei rund <b>0,477 bis 0,549</b>. Das unveränderte globale Ziel <b>0,001</b> ist damit nicht nachgewiesen. METHOD und G1 bleiben <b>HOLD</b>; eine frische Bestätigung wurde nicht ausgeführt.')
    rows=[['Archiv','Aktive Knoten','Fenster W0','Fenster W1']]
    for r in fine['archives']:rows.append([r['key'],r['active_count'],upper(r['windows'][0]['finite_total_upper']),upper(r['windows'][1]['finite_total_upper'])])
    table(rows,[130,100,127,126])
    p('Obere Grenzen für E(|Δ<sub>D5</sub>| | archivierte Konfiguration in Ω₅). Alle Tabellenwerte sind auf sechs Nachkommastellen nach oben gerundet. W0 = [3/4, 1], W1 = [1, 5/4]. Es sind Erwartungswertschranken, keine gemessenen Fehler und keine Garantie für eine einzelne Realisierung.','SmallCustom')
    p('Was diese Version leistet','Heading2')
    p('Die bisher offene endliche Gebietsergänzung ist mathematisch geschlossen. Der direkte Detektorbeitrag und sämtliche diskreten Transportpfade sind eingeschlossen, auch Pfade über noch unbekannte aktive Außenpunkte.')
    p('Der unendliche Wurzelbereich t &lt; −6 bleibt Gegenstand von Schritt 2. Die physikalische History wird durch die Rechengrenze nicht abgeschnitten. Die bisherige globale Majorante bleibt unverändert.')
    p('Stand: 29. Oktober 2026 · Basis: Main ff990b1ffe04 · Keine neuen Wolken, Zufallszahlen oder statistischen Regeln.','SmallCustom')
    story.append(PageBreak())
    p('01 / Lückenlose Gebietsabdeckung','SmallCustom');p('Alle Raumrichtungen sind erfasst','Heading1')
    p('Mit τ = −t − 1 und R = |x| liegt der KG-Träger innerhalb R ≤ τ + 1/2. Für τ ≤ 7/4 liegt dieser Träger vollständig in Ω₅: Der Außenbeitrag verschwindet dort exakt. Es bleibt das endliche Gebiet')
    p('D₅: 7/4 &lt; τ ≤ 5,<br/>max(0, 4 − τ) &lt; R &lt; τ + 1/2, alle Raumrichtungen.','FormulaCustom')
    story.append(Image(str(report/'coverage.png'),width=483,height=247.5))
    p('Die Grafik zeigt die radiale Geometrie; jede Fläche steht für sämtliche Raumrichtungen mit Volumenmaß 4πR² dR dτ. Die Grenze R = τ − 1/2 trennt tiefes Inneres und Wellenfront.','SmallCustom')
    table([['Teilgebiet','Exaktes Vierervolumen'],['Tiefes Inneres','(50087/384) π'],['Wellenfront','(315/2) π'],['Gesamtes D₅','(110567/384) π ≈ 904,574153']],[225,258])
    p('Die Zerlegung in 688, 2664 und 10480 rationale Zellen reproduziert diese Volumina exakt. Ein zusätzlicher Querschnittstest prüft, dass weder Lücken noch Überlappungen mit positivem Volumen auftreten.')
    p('P = [−6, −5] × [−2, 2]³ liegt vollständig in D₅. Seine alte v0.21-Schranke wird nicht nochmals addiert. Die Zahlen beider Versionen beziehen sich auf unterschiedliche Gebiete.','SmallCustom')
    story.append(PageBreak())
    p('02 / Feldschranken und diskreter Transport','SmallCustom');p('Die Wellenfront bestimmt die Breite','Heading1')
    p('Im tiefen Inneren verschwinden die Lichtkegeloberfläche und der Kirchhoff-Anteil. Auf der Wellenfront werden diese Terme ausdrücklich eingeschlossen. Dazu werden radiale Quellenmomente analytisch ausgewertet und durch unabhängige validierte Quadraturen kontrolliert.')
    p('Auf dem feinsten Gitter entfallen rund <b>93,1 %</b> der integrierten absoluten Feldhülle auf die Wellenfront. Die verbleibende Breite ist überwiegend eine Folge konservativer Betragsgrenzen; sie ist kein Nachweis großer physikalischer Fehler.')
    rows=[['Gitter 1/n','Zellen','∫ U<sub>Hülle</sub> d⁴x','Größte Grenze']]
    for l in data['levels']:
        mx=max(arb(w['finite_total_upper']).upper() for r in l['archives'] for w in r['windows'])
        rows.append([f'n = {l["grid_denominator"]}',l['cells'],upper(l['field_L1_integral_upper']),upper(mx)])
    table(rows,[95,75,165,148])
    p('Alle drei Stufen behandeln dasselbe vollständige Gebiet. Die beobachtete Verbesserung wird geprüft; eine asymptotische Konvergenzrate wird nicht behauptet.','SmallCustom')
    p('Vollständige Beitragszerlegung','Heading2')
    p('B<sub>D5</sub> = D<sub>Fenster</sub> + Σ |a<sub>j</sub>| F<sub>j</sub> + B<sub>unbekannt</sub>','FormulaCustom')
    table([['Beitrag','Bedeutung','Beispiel d0_r02 / W1'],['Direkt','Gesamte Detektorkugel und ganzes Zeitfenster',upper(fine['archives'][2]['windows'][1]['direct_upper'])],['Bekannte Pfade','Unveränderte adjungierte Koeffizienten',upper(fine['archives'][2]['windows'][1]['known_active_upper'])],['Unbekannte Pfade','Mecke-Grenze mit λ = 29/512',upper(fine['archives'][2]['windows'][1]['unknown_active_upper'])]],[100,235,148])
    p('Kausale Winkelkappen schließen alle Wurzelrichtungen ein. Die Detektormittelung verwendet 16 radiale und 8 zeitliche Teilintervalle mit exakt normierten Massen. Der erste Schichtkern wird punktweise durch κ majorisiert; die schärferen archivbedingten Zählkerne werden auf D₅ noch nicht neu integriert.','SmallCustom')
    p('Die vollständige Herleitung, einschließlich Quellenrandresten, Winkelkappen und Pfadzerlegung, steht in PROOF.md im Prüfpaket.','SmallCustom')
    story.append(PageBreak())
    p('03 / Prüfung und offener Rest','SmallCustom');p('Reproduzierbar, mit klarer Grenze','Heading1')
    table([['Prüfung','Ergebnis'],['Unveränderte Eingaben','11 Dateien: SHA256 und Git-Blob stimmen überein'],['Geometrie','Drei exakte Volumensummen; lückenlose radiale Querschnitte'],['Quellenintegrale','50 unabhängige Moment- und 6 Massenquadraturen'],['KG-Referenz','30 feste Kontrollpunkte je Präzision; alle eingeschlossen'],['Kausalität und Transport',f'{checks["rational_angular_box_probes"]} rationale Kappenproben; 48 Beitragszerlegungen'],['128 / 192 Bit','Physikalische Intervalle überlappen; größte Abweichung der Gesamtmajoranten < 5,9 × 10⁻¹³'],['Isolierte Wiederholung',f'{replay["byte_identical_result_files"]} numerische Ergebnisdateien bytegenau identisch']],[155,328])
    p('Gezielte Negativkontrollen erkennen eine ausgelassene Wellenfront, ein fehlendes Detektorintervall und veränderte Eingabebytes. Die Prüfungen sind Selbstkontrollen; ein unabhängiges wissenschaftliches Review wurde nicht durchgeführt.','SmallCustom')
    p('Nächster fachlicher Schritt','Heading2')
    p('Für t &lt; −6 wird eine dazu passende unendliche Restschranke benötigt. Sie muss dieselbe Konditionierung und Pfadzerlegung benutzen und D₅ ohne Doppelzählung ergänzen. Erst danach lässt sich ein neues vollständiges globales Budget bilden.')
    p('Auch eine sehr kleine Restschranke allein würde die derzeitige endliche Grenze nicht unter 0,001 bringen. Für eine Genauigkeitsfreigabe wären zusätzlich deutlich schärfere Abschätzungen erforderlich. METHOD_HOLD und G1 HOLD bleiben bestehen.')
    p('Reproduktion','Heading2')
    p('Python 3.12.14; python-flint 0.8.0; NumPy 2.3.5.<br/>Im entpackten Verzeichnis: <b>python3 reproduce.py</b><br/>Nur Prüfungen: <b>python3 reproduce.py --quick</b>','SmallCustom')
    p('Belege und Quellen','Heading2')
    p('PROOF.md, PROTOCOL.json, PROVENANCE.json, REPLAY.json und results/CHECKS.json dokumentieren Aussage, Eingaben und Prüfungen. Die Originalreferenz und alle benötigten numerischen Eingaben sind enthalten.','SmallCustom')
    p('DLMF 8.2.2: <link href="https://dlmf.nist.gov/8.2#E2" color="#127b82">dlmf.nist.gov/8.2#E2</link><br/>Arb-Dokumentation: <link href="https://python-flint.readthedocs.io/en/latest/arb.html" color="#127b82">python-flint.readthedocs.io/en/latest/arb.html</link><br/>Quellenstand 29.10.2026. Die Beweisschritte dieser Version sind im Paket explizit hergeleitet.','SmallCustom')
    def decorate(c,doc):
        c.setStrokeColor(TEAL);c.setLineWidth(.8);c.line(56,49,539,49);c.setFont('DejaVu',8);c.setFillColor(MUTED)
        c.drawString(56,34,'CSPP v0.22 · Endliche Außenhistory · METHOD / G1: HOLD');c.drawRightString(539,34,str(doc.page))
    class FixedCanvas(canvas.Canvas):
        def __init__(self,*a,**kw):kw['invariant']=1;super().__init__(*a,**kw)
    path=report/'Endliche_Aussenhistory_v0_22.pdf'
    doc=SimpleDocTemplate(str(path),pagesize=(595.276,841.89),rightMargin=56,leftMargin=56,topMargin=45,bottomMargin=65,title='CSPP v0.22 - Vollständige endliche Außenhistory',author='CSPP research workflow')
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate,canvasmaker=FixedCanvas)
    output=HERE.parent/'output/pdf';output.mkdir(parents=True,exist_ok=True);shutil.copy2(path,output/path.name)
    print(path)
if __name__=='__main__':build()
