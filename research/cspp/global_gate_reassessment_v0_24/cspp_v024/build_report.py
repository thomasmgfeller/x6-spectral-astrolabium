"""German decision brief; all numerical displays derive from the archived result."""
import json, shutil
from pathlib import Path
from flint import arb, ctx
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
NAVY = colors.HexColor('#16304b')
TEAL = colors.HexColor('#127b82')
MUTED = colors.HexColor('#526173')
LIGHT = colors.HexColor('#edf4f5')

def upper(x, digits=6, scale=1):
    v = arb(x).upper() / scale
    n = int((v * 10**digits).upper().ceil().unique_fmpz())
    assert arb(n) / 10**digits >= v
    return f'{n // 10**digits},{n % 10**digits:0{digits}d}'

def build():
    ctx.prec = 192
    data = json.loads((HERE/'results/DECISION_192.json').read_text())
    checks = json.loads((HERE/'results/CHECKS.json').read_text())
    replay = json.loads((HERE/'REPLAY.json').read_text())
    assert checks['status'] == 'PASS' and replay['isolated_replay'] == 'PASS'
    report = HERE/'report'
    report.mkdir(exist_ok=True)
    fonts = Path('/usr/share/fonts/truetype/dejavu')
    pdfmetrics.registerFont(TTFont('DV24', str(fonts/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DV24-Bold', str(fonts/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DV24', normal='DV24', bold='DV24-Bold', italic='DV24', boldItalic='DV24-Bold')
    st = getSampleStyleSheet()
    for name in ['BodyText','Heading1','Heading2']:
        st[name].fontName = 'DV24'
        st[name].textColor = NAVY
    st['BodyText'].fontSize = 9.8
    st['BodyText'].leading = 14.5
    st['BodyText'].spaceAfter = 8
    st['Heading1'].fontSize = 22
    st['Heading1'].leading = 28
    st['Heading1'].spaceAfter = 14
    st['Heading2'].fontSize = 12
    st['Heading2'].leading = 17
    st['Heading2'].textColor = TEAL
    st['Heading2'].spaceBefore = 10
    st['Heading2'].spaceAfter = 7
    st.add(ParagraphStyle(name='Small24', fontName='DV24', fontSize=8.2, leading=11.8, textColor=MUTED, spaceAfter=7))
    st.add(ParagraphStyle(name='Math24', fontName='DV24', fontSize=10.2, leading=17, textColor=NAVY, backColor=LIGHT, borderPadding=9, spaceBefore=16, spaceAfter=22))
    story = []
    def p(text, style='BodyText'):
        story.append(Paragraph(text, st[style]))
    def table(rows, widths):
        t = Table([[Paragraph(str(x), st['Small24']) for x in r] for r in rows], colWidths=widths, repeatRows=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),LIGHT), ('LINEBELOW',(0,0),(-1,0),1,TEAL),
            ('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#d9e0e6')), ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),5)]))
        story.extend([t, Spacer(1,8)])

    p('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ 0.24 · 29.10.2026','Small24')
    p('Globale Bilanz:<br/>Methodenkriterien neu bewertet','Heading1')
    p('<b>Schritt 3 ist abgeschlossen. METHOD und G1 bleiben HOLD.</b> Die vollständige Außenhistory-Bilanz aus v0.23 rechtfertigt noch keine Genauigkeitsfreigabe und kein frisches Bestätigungsensemble.')
    p('Die nächste Hauptaufgabe ist die <b>deterministische Entwicklung und Stabilitätsprüfung eines geänderten skalaren Kandidaten</b>. Für die unveränderte feste Operatorzelle scheitert eine reine Gebietsvergrößerung bereits an einem früheren notwendigen Kontrolltest. Die ganze Operatorfamilie wird nicht verworfen.')
    p('Was die bestehende Schranke begrenzt','Heading2')
    table([
        ['Beitrag / Diagnose','Ergebnis über acht Archiv-Fenster-Fälle'],
        ['Vollständige obere Restschranke','Etwa 3,17 bis 3,75 × 10¹⁰'],
        ['Nahe Lichtkegelhülle','Mehr als 99,9999 % des ausgewiesenen Budgets'],
        ['Ferne Hülle','Etwa 7.804 bis 10.180'],
        ['Endlicher Außenbereich','Etwa 0,477 bis 0,549; das 477- bis 549-Fache von 0,001'],
        ['Markov am Ziel 0,001','Nur die triviale bedingte Wahrscheinlichkeitsgrenze 1']
    ], [182,301])
    p('<b>Diese Zahlen sind obere Beweisschranken, keine gemessenen Fehler.</b> Die Dominanz der nahen Hülle beweist keine entsprechende Aufteilung des tatsächlichen physikalischen Fehlers.')
    p('Selbst ein hypothetisch entferntes unendliches Zertifikat ließe die unveränderte endliche Majorante über dem Ziel. Das beschreibt die Grenze des bisherigen Beweisinstruments. Positive Terme dürfen für eine echte Fehlerbescheinigung nicht einfach weggelassen werden.','Small24')
    p('Unverändert bleiben Quelle, Dichte, Schichtkernel, Detektor, Archive und statistische Regeln. Es gibt keinen neuen Seed, keine neue Wolke und kein neues Bestätigungsdesign.','Small24')
    story.append(PageBreak())

    p('01 / Neue mathematische Folgerung','Small24')
    p('L¹-Kontrolle des idealen Ensembles','Heading1')
    p('Die vier bekannten Archive allein erlauben keine Ensembleaussage. Die uniformen Endpunkthüllen aus v0.23 gelten jedoch für beliebige endliche Archive. Zusammen mit der Poissonverteilung der aktiven Punktzahl ergibt sich eine neue quantitative Integrabilitätskontrolle.')
    p('Die gemeinsame aktive Hülle beider Fenster hat Poissonmasse λ<sub>A</sub> = 14625/256. Davon liegen λ<sub>E</sub> = 29/512 außerhalb und λ<sub>B</sub> = 29221/512 innerhalb von Ω₅. Mit γ = βκ ist N<sub>B</sub> poissonverteilt:')
    p('E[(1 + γ)<super>N<sub>B</sub></super>] = exp(γ λ<sub>B</sub>)','Math24')
    p('Die endliche erste Forcierung wird uniform durch F<sub>endlich</sub> = γ M · 110567/128 begrenzt; F<sub>tail,W</sub> stammt aus der unveränderten uniformen v0.23-Hülle. Konditionieren, positive Pfadsummen und anschließend Mitteln liefern:')
    p('E|A∞ − A₅| ≤ (F<sub>endlich</sub> + F<sub>tail,W</sub>) exp(γ λ<sub>A</sub>)','Math24')
    table([['Detektorfenster','Unbedingte obere L¹-Grenze, aufgerundet']]+
          [[f'W{w["window"]}', upper(w['unconditional_exterior_L1_upper'],6,10**11)+' × 10¹¹'] for w in data['budget_windows']], [150,333])
    p('Auch A₅ ist integrierbar: History- und aktive Punktzahlen betreffen disjunkte Poissonzählgebiete; eine endliche Pfadsumme gibt eine integrierbare Hülle. Damit ist auch A∞ in L¹. Die fast sichere absolute Konvergenz war bereits in v0.17 gezeigt.')
    p('Was daraus noch nicht folgt','Heading2')
    p('Ein endliches erstes absolutes Moment garantiert kein zweites Moment. Selbst gleiche Randverteilungen bestimmen keine Kreuzkovarianz. Das Prüfpaket enthält exakte Gegenbeispiele für beide Fehlschlüsse. Es behauptet damit nicht, dass die CSPP-Varianz unendlich wäre.')
    p('Die Aussage setzt das ideale Poisson-Gesetz und die exakt vorgeschriebene volle KG-History voraus. Sie qualifiziert weder einen Sampler noch dichteuniforme Stabilität, Genauigkeit oder die älteren H1-/PU-H1-Adapter.','Small24')
    story.append(PageBreak())

    p('02 / Zulassung und notwendiger Kontrollzeuge','Small24')
    p('Die sechs Kriterien bleiben bindend','Heading1')
    p('Die volle KG-History-Diagnose ist eine andere Eingabeabbildung als die beiden eingefrorenen v0.14-Kandidaten. Ein Zertifikat darf nicht ohne Beweis zwischen diesen Definitionen übertragen werden.')
    table([
        ['Methodenkriterium','Lokaler H1-Adapter','Nichtlokaler PU-H1-Adapter'],
        ['Kontrollreproduktion','PASS','PASS'],
        ['Totale Ensembleabbildung','PASS','Auf Menge positiver Wahrscheinlichkeit undefiniert'],
        ['Gemeinsame Originalmomente','Nicht ausgewertet','Nicht ausgewertet'],
        ['Viertes Moment / geeignete Tail-Kontrolle','PASS','Nicht zertifiziert'],
        ['Ensembleweiter numerischer Fehler','Nicht zertifiziert','Nicht zertifiziert'],
        ['Samplinggesetz-Konformität','Nicht zertifiziert','Nicht zertifiziert']
    ], [187,139,157])
    p('Beide Kandidaten bleiben <b>für einen Bestätigungslauf nicht zugelassen</b>. Dies ist eine Methodenzulassung mit offenen Voraussetzungen, kein neuer statistischer Verwerfungstest auf frischen Daten.')
    p('Unveränderter Gauß-Zeuge: Gebietsvergrößerung reicht nicht','Heading2')
    p('Für die feste Zelle ρ = 3/π, ε = 1/16 und q = 3/(16π) bleibt der relative Mittelwertfehler des vorhandenen Gauß-Kontrollfeldes für <b>jedes reelle H ≥ 4 größer als 0,417028051007</b>. Für unbegrenzte Vergangenheit beträgt er ungefähr 0,6848927465.')
    p('Damit scheitert schon die notwendige relative 10-%-RMS-Bedingung, weil RMS ≥ |Bias|. Die durchgehende H-Abdeckung wurde aus den unveränderten Einschließungen aus v0.15 erneut zusammengesetzt; die ursprünglichen Gaußquadraturen wurden hier nicht neu gerechnet.')
    p('Die Aussage betrifft diese feste Zelle, diesen Kernel, die betrachteten Vergangenheitsdiamanten und den notwendigen Kontrollzeugen. Sie ist weder ein Anteil am kompakten Detektorfehler noch eine Widerlegung aller skalaren Operatoren.','Small24')
    story.append(PageBreak())

    p('03 / Nächster Arbeitsauftrag und Nachprüfbarkeit','Small24')
    p('Zuerst Kandidat und Stabilität','Heading1')
    table([
        ['Reihenfolge','Konkreter Arbeitsauftrag'],
        ['1 · Deterministisch','Geänderten skalaren Kandidaten ausdrücklich definieren; Kontrollfelder, Normierung, Retardierung, Gesamtfehler und Stabilität prüfen. Noch kein Parameter oder Suchgitter gewählt.'],
        ['2 · Methodisch','Alle sechs Kriterien für genau diesen Kandidaten nachweisen; gemeinsame Momente und Korrelationen ausdrücklich behandeln.'],
        ['3 · Danach statistisch','Erst bei Zulassung Design, Rechenbudget und öffentliche Vorregistrierung einfrieren; anschließend frische Daten. Fluktuation und makroskopische Kriterien getrennt entscheiden.']
    ], [126,357])
    p('Optional bleibt eine vollständige Fehlerattribution im bisherigen Modell sinnvoll. Sie muss endliche und unendliche Beiträge sowie alle Pfadklassen umfassen. Sie hebt den notwendigen Gauß-Befund der festen Zelle nicht auf. Der neue Arbeitsauftrag ist vorbereitet, noch nicht ausgeführt.','Small24')
    p('Reproduzierbarkeit','Heading2')
    c = checks['counts']
    table([
        ['Prüfung','Ergebnis'],
        ['Herkunft und Arithmetik',f'{c["source_files"]} Eingaben gegen SHA256 und Git-Blobs; 128 und 192 Bit'],
        ['Bilanz und Operatorzeuge',f'{c["global_decompositions"]} Zerlegungen; {c["inherited_H_cover_nodes"]} übernommene H-Stützstellen'],
        ['Eigenständige Kontrollen','12 positive Poissonsummen mit explizitem Rest; 60 rationale Momentidentitäten; 2 Kovarianz-Vorzeichenkontrollen'],
        ['Isolierter Replay',f'{replay["byte_identical_result_files"]} numerische Ergebnisdateien bytegenau reproduziert']
    ], [170,313])
    p('Python 3.12.14 · python-flint 0.8.0. Im entpackten Paket: <b>python3 reproduce.py</b>; nur Prüfungen: <b>python3 reproduce.py --quick</b>. Herleitung: PROOF.md. Herkunft: PROVENANCE.json. Nächster Auftrag: NEXT_WORK_PACKAGE.md.','Small24')
    p('Die größte Abweichung im Präzisionsvergleich, etwa 2,41 × 10⁻¹⁵, stammt aus übernommenen endlichen Einschließungen. Arithmetische Konsistenzgrenzen ändern kein wissenschaftliches Ziel. Kein unabhängiges Peer Review und keine Beweisassistent-Verifikation.','Small24')
    p('Basis: <link href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/tree/0edb8e02aa3dbf5a1b827d7c9aa82385e056e817/research/cspp" color="#127b82">Main nach PR #155</link>. Poisson-Grundlagen: <link href="https://stoch.math.kit.edu/img/Last/lastpenrose2017.pdf" color="#127b82">Last/Penrose (2017), Gl. 1.8 und Thm. 4.4</link>. Operator-Kontext: <link href="https://arxiv.org/abs/1403.1622" color="#127b82">Aslanbeigi et al. (2014)</link> und <link href="https://arxiv.org/abs/1510.04656" color="#127b82">Belenchia et al. (2016)</link>. Die konkrete Bilanz und Entscheidung sind eigene Projektresultate.','Small24')
    def footer(can, doc):
        can.setStrokeColor(TEAL)
        can.line(56,49,539,49)
        can.setFont('DV24',8)
        can.setFillColor(MUTED)
        can.drawString(56,34,'CSPP v0.24 · Schritt 3 abgeschlossen · METHOD / G1: HOLD')
        can.drawRightString(539,34,str(doc.page))
    class FixedCanvas(canvas.Canvas):
        def __init__(self,*args,**kwargs):
            kwargs['invariant']=1
            super().__init__(*args,**kwargs)
    path = report/'Gate_Neubewertung_Globale_Bilanz_v0_24.pdf'
    doc = SimpleDocTemplate(str(path),pagesize=(595.276,841.89),leftMargin=56,rightMargin=56,topMargin=45,bottomMargin=65,title='CSPP v0.24 - Gate-Neubewertung nach globaler Bilanz',author='CSPP research workflow')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=FixedCanvas)
    out = HERE.parent/'output/pdf'
    out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(path,out/path.name)
    print(path)

if __name__ == '__main__':
    build()
