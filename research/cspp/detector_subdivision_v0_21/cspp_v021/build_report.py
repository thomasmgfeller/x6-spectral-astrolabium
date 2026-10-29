"""German research report; values generated from the certified 192-bit result."""
import json,math
from pathlib import Path
import numpy as np
from flint import arb,ctx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
HERE=Path(__file__).resolve().parent
def val(s):return float(arb(s).mid())
def up(s,d=9):
    n=int((arb(s).upper()*10**d).upper().ceil().unique_fmpz())
    return f'{n//10**d},{n%10**d:0{d}d}'
def main():
    ctx.prec=256
    r=json.loads((HERE/'results/DETECTOR_192.json').read_text())
    checks=json.loads((HERE/'results/CHECKS.json').read_text())
    replay=json.loads((HERE/'REPLAY.json').read_text())
    if checks['status']!='PASS' or replay['isolated_replay']!='PASS':raise ArithmeticError('checks not complete')
    navy='#18394a';teal='#087d86';amber='#ac761d';muted='#536a75'
    rows=[(a['key'],w) for a in r['archives'] for w in a['windows']]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,3),layout='constrained');x=np.arange(8)
    old=[val(w['v20']['patch_total_upper']) for _,w in rows];new=[val(w['levels'][-1]['patch_total_upper']) for _,w in rows]
    ax.bar(x-.17,old,.32,label='v0.20',color='#bbccd2');ax.bar(x+.17,new,.32,label='v0.21',color=teal)
    ax.axhline(.001,color=amber,linestyle='--',label='Vergleich 0,001; kein Patchbudget')
    ax.set_xticks(x,[f"r{k[-1]} / W{w['window']}" for k,w in rows]);ax.set_ylabel('Obere bedingte Erwartungswertschranke')
    ax.set_ylim(0,.007);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);ax.legend(frameon=False,fontsize=8,ncols=3,loc='upper left')
    fig.savefig(HERE/'results/comparison.png',dpi=180);fig.savefig(HERE/'results/comparison.svg');plt.close(fig)
    f='/usr/share/fonts/truetype/dejavu/DejaVuSans'
    pdfmetrics.registerFont(TTFont('DV',f+'.ttf'));pdfmetrics.registerFont(TTFont('DV-Bold',f+'-Bold.ttf'))
    pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
    styles=getSampleStyleSheet()
    for name,size,leading,color in [('Title21',24,29,navy),('H21',13,18,navy),('P21',9.6,14.4,navy),('Small21',8,11.5,muted),('Math21',10,16,teal)]:
        styles.add(ParagraphStyle(name=name,fontName='DV-Bold' if name in ['Title21','H21'] else 'DV',fontSize=size,leading=leading,textColor=HexColor(color),spaceAfter=10,spaceBefore=5 if name=='H21' else 0))
    flow=[]
    def P(t,s='P21'):return Paragraph(str(t),styles[s])
    def add(t,s='P21'):flow.append(P(t,s))
    def table(data,widths):
        t=Table([[P(v,'Small21') for v in row] for row in data],colWidths=widths,hAlign='LEFT',repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e2eff0')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.6,HexColor(teal)),('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#dbe3e7'))]))
        flow.append(t);flow.append(Spacer(1,9))
    add('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ v0.21','Small21')
    add('Unterteilter Detektor,<br/>schärfere Patchgrenze','Title21')
    add('Der nächste Schritt aus v0.20 ist ausgeführt.','H21')
    add('Für den unveränderten Historybereich <b>P = [-6,-5] × [-2,2]³</b> sinkt der direkte Detektorbeitrag um <b>54-74 %</b>. Die vollständige Patchschranke verbessert sich um <b>42-55 %</b> auf etwa <b>0,00221-0,00312</b>. Bekannter aktiver Transport und unbekannte aktive Außenpfade bleiben mit ihren bisherigen validierten Obergrenzen enthalten.')
    flow.append(Image(str(HERE/'results/comparison.png'),width=495,height=186))
    table([['Archiv','W0 · neue Grenze¹','W1 · neue Grenze¹']]+[[a['key']]+[up(w['levels'][-1]['patch_total_upper']) for w in a['windows']] for a in r['archives']],[165,165,165])
    add('¹ Nach oben gerundete Dezimaldarstellung. Vollständige Arb-Intervalle und die einzelnen Beiträge stehen im Prüfpaket. Prozentangaben beschreiben die Verbesserung der Obergrenzen, nicht die Änderung eines gemessenen Fehlers.','Small21')
    add('<b>METHOD_HOLD · G1 HOLD bleiben.</b> Alle acht Patchobergrenzen liegen weiterhin über dem unveränderten Vergleich 0,001. Der übrige äußere Historybereich ist nicht neu zertifiziert; es folgt keine globale Genauigkeitsaussage.')
    flow.append(PageBreak())
    add('1 · Eine fallende Kernhülle','Title21')
    add('Das bisherige breite Zellintervall fiel häufig auf die globale Gewichtsschranke κ zurück. Die neue Rechnung nutzt eine exakt abgeleitete Eigenschaft des unveränderten Schichtkerns: Nach seiner letzten Betrags-Spitze bei n=95 nimmt |w(n)| monoton ab.')
    add('H(n) = max<sub>k≥n</sub> |w(k)|<br/>M(n,μ) = E H(n + Poisson(μ))','Math21')
    add('H majorisiert den Betrag des ursprünglichen Kerns. Für n≤95 wird H endlich und exakt rational berechnet; für n≥95 gilt H(n)=-w(n). Zwei verschobene Polynome mit eindeutigem Koeffizientenvorzeichen beweisen die Monotonie für den gesamten unendlichen Rest.')
    add('M fällt sowohl mit der bekannten Punktzahl n als auch mit dem äußeren Poisson-Mittel μ. Für ein ganzes Wurzel-/Detektorzellpaar genügt deshalb die Auswertung an den eingeschlossenen unteren Grenzen n<sub>min</sub> und μ<sub>min</sub>. Die zugehörigen Maxima werden zur Kontrolle ebenfalls berechnet.')
    add('Exakte Zählungen und tatsächliche Überlappung','H21')
    add('Die vorhandenen Archivpunkte werden mit rationalen Koordinaten gegen die vollständigen Boxen geprüft. Die maximale Entfernung zu einer Boxecke liefert sichere Beziehungen für alle Zellpunkte; die minimale Entfernung liefert eine Obermenge möglicher Beziehungen. Keine Float-Toleranz entscheidet über Kausalität.')
    add('Für die Außenvolumina verwenden wir die unveränderte geschlossene Intervallüberlappung aus v0.20. Kausale Unter- und Oberintervalle schließen den tatsächlichen Wert über dem gleichen Produktgebiet ein. n und μ dürfen dabei voneinander abhängen; die monotone Majorante benötigt keine Unabhängigkeitsannahme.')
    table([['Stufe','Patchgrenzen, ungefähr'],['v0.20 · bisherige ganze Detektorhülle','0,00470 bis 0,00580'],['Neue monotone Hülle · ganze Kugel',f"{min(val(w['levels'][0]['patch_total_upper']) for _,w in rows):.5f} bis {max(val(w['levels'][0]['patch_total_upper']) for _,w in rows):.5f}".replace('.',',')],['16 Endpunktboxen je Fenster',f"{min(val(w['levels'][1]['patch_total_upper']) for _,w in rows):.5f} bis {max(val(w['levels'][1]['patch_total_upper']) for _,w in rows):.5f}".replace('.',',')],['256 Endpunktboxen je Fenster','0,00221 bis 0,00312']],[305,190])
    add('Jede feinere Zelle übernimmt zusätzlich die gültige Obergrenze ihrer Elternzelle. Dadurch kann eine ungünstigere einzelne Rundung oder Hülle die Verfeinerung nicht verschlechtern.','Small21')
    flow.append(PageBreak())
    add('2 · Der ganze Kugeldetektor','Title21')
    add('Der Detektor bleibt die normierte Kugel mit Radius 1/2 um (0,0,3/2), gemittelt über W0=[3/4,1] oder W1=[1,5/4]. Die Rechnung ersetzt ihn weder durch den umschließenden Würfel noch durch einzelne Detektorpunkte.')
    add('96,51 % sicher aufgelöste Masse; der Rest bleibt begrenzt','H21')
    add('Ein festes Gitter mit 128 Teilungen je Raumachse identifiziert Kleinstboxen, deren entfernteste Ecke innerhalb der Kugel liegt. Ihre disjunkten Volumina liefern eine exakte untere Grenze von <b>96,5100 %</b> der normierten Kugelmasse. Der verbleibende Randanteil von etwa <b>3,4900 %</b> erhält die gültige Hülle der ganzen Kugel.')
    add('K<sub>mittel</sub>(C) = K₀(C) - Σ<sub>E</sub> l<sub>E</sub> [K₀(C)-K<sub>E</sub>(C)]','Math21')
    add('Hier ist l<sub>E</sub> eine bewiesene untere Detektormasse und K<sub>E</sub>≤K₀ eine punktweise gültige Verbesserung. Abgezogen wird eine untere Grenze der Verbesserung. Das lässt den vollständigen Detektor eingeschlossen, ohne seine Teilmassen auf eins zu renormieren.')
    add('Die vollständige Pfadbilanz bleibt erhalten','H21')
    w=r['archives'][0]['windows'];table([['d0_r00 · Beitrag','W0¹','W1¹']]+[[label]+[up(q['levels'][-1][k]) for q in w] for label,k in [('Direkt zum Detektor','direct_detector_upper'),('Bekannter aktiver Transport','known_active_transport_upper'),('Unbekannte aktive Außenpfade','unknown_active_paths_upper'),('Gesamte Patchobergrenze','patch_total_upper')]],[245,125,125])
    add('¹ Alle Werte nach oben gerundet. Die beiden Transportbeiträge sind unveränderte Eingaben aus v0.20. Ihre Pfadzerlegung, kausale Konvexität und Mecke-Majorante werden weiterverwendet.','Small21')
    add('Daraus folgt eine schärfere obere bedingte Erwartungswertschranke für alle Pfade mit Wurzel in P. Der komplementäre Wurzelbereich bleibt offen. Insbesondere wird keine obere Patchgrenze von der bisherigen oberen Gesamtgrenze subtrahiert; die globale v0.19-Majorante bleibt unverändert.')
    flow.append(PageBreak())
    add('3 · Prüfung und nächster Schritt','Title21')
    c=checks['counters']
    table([['Prüfung','Ergebnis'],['Physikalische Volumenintervalle, 128 / 192 Bit',f"{c['physical_volume_overlaps']:,}".replace(',',' ')],['Zellmajoranten: Gültigkeitsbereich und Präzisionsstabilität',f"{c['kernel_majorants_checked']:,}".replace(',',' ')],['Separate Ganzzahl-Zählkontrollen',c['integer_box_count_checks']],['Kontrollpunkte unter der eingeschlossenen Zellhülle',c['point_kernel_dominance_checks']],['Direkte Poissonsummen mit rigorosem Rest',c['direct_poisson_controls']],['Gepinnte Eingabedateien gegen Main-Git-Blobs',c['source_blobs']],['Absichtlich falsche Kontrollen zurückgewiesen',c['negative_controls']],['Vollständiger isolierter Wiederholungslauf',f"PASS · {replay['byte_identical_result_files']} byteidentische Dateien"]],[350,145])
    add('Geprüft werden außerdem die vollständigen Zellinventare, die exakte Massenerhaltung zwischen Eltern und Kindern, der eingeschlossene Kugelrand, die unveränderten Transportbeiträge und die Verbesserung in allen acht Archiv-/Fensterfällen. Arithmetische Rechenradien sind keine Aussage über die Schärfe der tatsächlichen Fehlergrenze. Ein externes Fachreview wird nicht behauptet.')
    add('Weiterführung','H21')
    add('Der nächste offene Schritt ist die vollständige Überdeckung des übrigen endlichen äußeren Historybereichs, einschließlich der räumlichen Flanken außerhalb P. Dafür werden passende uniforme KG-Feldhüllen und gültige geometrische Teilbereiche benötigt. Erst mit einer vollständigen endlichen Bilanz und einem kompatiblen unendlichen Rest lässt sich das globale Fehlerziel neu bewerten.')
    add('Reproduktion und Quellen','H21')
    add('Basis: Main nach PR #152, Commit<br/>22eab46877dc03b1c0f1bee81c2d1d65bbf45d65.<br/>Laufzeit: Python 3.12, python-flint 0.8.0, NumPy 2.x.<br/>Vollständige Rechnung: <b>python3 reproduce.py</b>.<br/>Gespeicherte Ergebnisse prüfen: <b>python3 reproduce.py --quick</b>.','Small21')
    add('Die vollständige Herleitung steht in PROOF.md; die unveränderte v0.20-Herleitung liegt bei. PROVENANCE.json enthält die Quellenidentitäten. Die verwendete Ballarithmetik ist dokumentiert unter https://python-flint.readthedocs.io/en/latest/arb.html .','Small21')
    add('<b>29. Oktober 2026 · METHOD_HOLD · G1 HOLD · neue Bestätigung NOT_RUN.</b> Keine neuen Wolken, Seeds oder statistischen Schwellen.')
    out=HERE/'report/Detektor_Unterteilung_v0_21.pdf';out.parent.mkdir(exist_ok=True)
    def footer(c,doc):
        c.setStrokeColor(HexColor('#dbe3e7'));c.line(50,45,545,45);c.setFont('DV',8);c.setFillColor(HexColor(muted));c.drawString(50,30,'CSPP · v0.21 · 29. Oktober 2026');c.drawRightString(545,30,str(doc.page))
    SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50,topMargin=48,bottomMargin=62,title='CSPP v0.21 - Unterteilter Detektor',author='Thomas Gfeller / Codex').build(flow,onFirstPage=footer,onLaterPages=footer)
    print(out)
if __name__=='__main__':main()
