"""Readable German report; all tables come from the certified 192-bit result."""
import json, math
from pathlib import Path
import numpy as np
from flint import arb,ctx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
def value(s):return float(arb(s).mid())
def main():
    ctx.prec=256
    d=json.loads((HERE/'results/LOCAL_192.json').read_text());checks=json.loads((HERE/'results/CHECKS.json').read_text())
    old=json.loads((HERE/'evidence/v19_BOUNDS_512.json').read_text())
    replay=json.loads((HERE/'REPLAY.json').read_text())
    navy='#18394a';teal='#087d86';amber='#b27319';muted='#536a75'
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,3.1),layout='constrained');x=np.arange(4)
    vals=[[value(r['levels'][-1]['windows'][wi]['patch_total_upper']) for r in d['archives']] for wi in [0,1]]
    ax.bar(x-.17,vals[0],.31,label='W0: 0,75 bis 1',color=teal);ax.bar(x+.17,vals[1],.31,label='W1: 1 bis 1,25',color=navy)
    ax.axhline(.001,color=amber,linestyle='--',label='Vergleich 0,001; kein eigenes Patchbudget')
    ax.set_xticks(x,[r['key'] for r in d['archives']]);ax.set_ylabel('Obere bedingte Erwartungswertschranke');ax.set_ylim(0,.0072)
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);ax.legend(frameon=False,fontsize=8,loc='upper left',ncols=2)
    fig.savefig(HERE/'results/patch_bounds.png',dpi=180);fig.savefig(HERE/'results/patch_bounds.svg');plt.close(fig)
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans'
    pdfmetrics.registerFont(TTFont('DV',font+'.ttf'));pdfmetrics.registerFont(TTFont('DV-Bold',font+'-Bold.ttf'))
    pdfmetrics.registerFontFamily('DV',normal='DV',bold='DV-Bold',italic='DV',boldItalic='DV-Bold')
    st=getSampleStyleSheet();st.add(ParagraphStyle(name='Title20',fontName='DV-Bold',fontSize=25,leading=30,textColor=HexColor(navy),spaceAfter=16))
    st.add(ParagraphStyle(name='H20',fontName='DV-Bold',fontSize=14,leading=18,textColor=HexColor(navy),spaceBefore=12,spaceAfter=8))
    st.add(ParagraphStyle(name='P20',fontName='DV',fontSize=9.8,leading=14.7,textColor=HexColor(navy),spaceAfter=10))
    st.add(ParagraphStyle(name='Small20',fontName='DV',fontSize=8,leading=11.5,textColor=HexColor(muted),spaceAfter=7))
    st.add(ParagraphStyle(name='Math20',fontName='DV',fontSize=10,leading=16,textColor=HexColor(teal),leftIndent=12,spaceBefore=6,spaceAfter=12))
    flow=[]
    def P(t,style='P20'):return Paragraph(t,st[style])
    def add(t,style='P20'):flow.append(P(t,style))
    def table(rows,widths):
        data=[[P(str(v),'Small20') for v in row] for row in rows]
        t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e2eff0')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.6,HexColor(teal)),('LINEBELOW',(0,1),(-1,-1),.25,HexColor('#dbe3e7'))]))
        flow.append(t);flow.append(Spacer(1,9))
    add('CSPP / EIGENZEIT · FORSCHUNGSNOTIZ v0.20','Small20')
    add('Lokale äußere History<br/>und exakte Überlappung','Title20')
    add('Ein endlicher Teilbereich ist vollständig eingeschlossen. Die globale Restzertifizierung bleibt offen.','H20')
    add('Für <b>P = [-6,-5] × [-2,2]³</b> ist der Beitrag aller Historywurzeln zum gemittelten Detektor nun einschließlich des diskreten Transports begrenzt. Die vier unveränderten Archive liefern in beiden Fenstern obere Schranken zwischen <b>0,004697 und 0,005799</b>.')
    flow.append(Image(str(HERE/'results/patch_bounds.png'),width=495,height=192))
    table([['Archiv','W0: obere Grenze¹','W1: obere Grenze¹']]+[[r['key']]+[f"{math.ceil(value(w['patch_total_upper'])*1e9)/1e9:.9f}" for w in r['levels'][-1]['windows']] for r in d['archives']],[165,165,165])
    add('¹ Dezimaldarstellung nach oben gerundet. Exakte Intervalle stehen im Prüfpaket. Die schmalen Rechenintervalle messen nur arithmetische Unsicherheit, nicht die Schärfe dieser Fehlermajoranten.','Small20')
    add('<b>METHOD_HOLD · G1 HOLD.</b> Der Vergleichsmaßstab 0,001 bleibt unverändert. Er ist weder erreicht noch ein nachträglich eingeführtes Teilbudget. Der komplementäre Außenbereich ist durch v0.20 nicht neu integriert. Es gibt kein neues Zufallsensemble und keine neue statistische Freigaberegel.')
    flow.append(PageBreak())
    add('1 · Tatsächliche Intervallgeometrie','Title20')
    add('Die universelle Kappe aus v0.19 wird für bekannte Endpunkte durch ein tatsächliches Überlappungsvolumen ersetzt. Im Ruhesystem des Diamanten zwischen b=(-5,0) und p wird das vierdimensionale Problem zu einer eindimensionalen Integration von Kugelschnitten.')
    add('v=p-b, w=y-b; h=√(v·v), u=(v·w)/h, d=√(u²-w·w).<br/>V<sub>über</sub> = π h(h-u-d)²(d²+dh-u²)/(24d)','Math20')
    add('Die Formel gilt im echten Linsenfall d&gt;|u| und h&gt;u+d. Verschachtelte oder nicht kausale Intervalle werden separat und exakt entschieden. Das Minkowski-Produkt hat Signatur (+---). Für p in Ω₅ gilt I(y,p) ∩ Ω₅ = J⁺(y) ∩ I(b,p).')
    add('Die drei Integrationsabschnitte reichen von (u+d)/2 bis h/2, von h/2 bis (h+u+d)/2 und von dort bis h. In den ersten beiden Abschnitten wird die Summe zweier Kugelkappen integriert; im dritten liegt die kleinere Kugel vollständig im Schnitt.')
    table([['Archiv','Aktive Punkte','Kausale Prüffälle','Echte Linsen']]+[[r['key'],len(r['active_archive_indices']),len(r['probes']),sum(q['branch']=='lens' for q in r['probes'])] for r in d['archives']],[135,100,135,125])
    add('Insgesamt werden <b>1.698 kausale Prüffälle</b> ausgewertet, davon <b>1.475 echte Linsen</b>. Die übrigen 86 der 1.784 möglichen Paare sind nicht kausal. Die acht Historypunkte sind feste mathematische Prüfstellen; sie erweitern das Zufallsarchiv nicht.')
    add('Archivbedingter Gewichtskern','H20')
    add('n₀ zählt exakt die bekannten Punkte im Intervall. Die restliche Punktzahl ist unter der Endpunkt-Palmverteilung Poisson-verteilt mit μ=ρ(V<sub>gesamt</sub>-V<sub>über</sub>). Ausgewertet wird F(n₀,μ)=E|w(n₀+Poisson(μ))|. Die endliche Formel aus v0.19 berücksichtigt die tatsächliche innere Zählung und ersetzt keine Geometrie durch eine Unabhängigkeitsannahme.')
    add('Für ganze Zellen werden n₀ und μ eingeschlossen. Eine nach oben gerundete Tabelle über geschlossene μ-Intervalle liefert zusätzliche Majoranten; die globale Schranke κ bleibt als gültige Rückfallgrenze erhalten. Im gesamten Rechenweg entscheiden exakte rationale Koordinaten über Kausalität.')
    flow.append(PageBreak())
    add('2 · KG-Feld und vollständige Zellen','Title20')
    add('Die lokale KG-Referenz wird bei 128 und 192 Bit erneut ausgeführt. Die Quelle exp(1-1/h)exp(4iz), Masse 1 und Anfangszeit -1 bleiben unverändert. Die analytischen Reste am glatten Quellenrand werden mitgeführt.')
    table([['Historypunkt (t; x,y,z)','|U|, ungefähr²','Radius, ungefähr']]+[[f"({'; '.join([r['point'][0], ', '.join(r['point'][1:])])})",f"{value(r['abs_upper']):.7g}",f"{max(float(arb(v).rad()) for v in r['KG']):.2e}"] for r in d['roots']],[235,130,130])
    add('² Gerundete Darstellung der eingeschlossenen Betragsobergrenze. Diese Punktwerte werden nicht als uniforme Schranken für ihre Umgebung ausgegeben.','Small20')
    add('Eine eigene Hülle deckt den ganzen Teilbereich ab','H20')
    add('Auf P gilt τ=|t+1|∈[4,5] und |x|≤√12. Daher liegt die gesamte Quelle strikt innerhalb des rückwärts betrachteten Lichtkegels. Der Kirchhoff- und der Oberflächenanteil verschwinden; es bleibt das massive Volumenintegral.')
    add('U(t,x)=τ/(32π) ∫ f(z) G(τ²-|x-z|²) d³z,<br/>G(A)=₀F₁(3;-A/4).','Math20')
    add(f"Die eingeschlossene L1-Quellnorm beträgt <b>{value(d['source_L1']):.15f}</b>. Ein expliziter alternierender Reihenrest beweist, dass G auf [0,25] positiv und fallend ist. Für jede Zelle folgt damit eine uniforme Feldhülle aus ihren äußeren Zeit- und Raumgrenzen.")
    add('Zwei vollständige Partitionen mit 16 beziehungsweise 256 Zellen werden berechnet. Kausale Unter- und Oberpunkte schließen für alle Zellpunkte die Intervallvolumina und Archivzählungen ein. Die feinere Partition verbessert die Schranke in allen acht Fällen. Es wird kein Integral durch einen Mittelpunktwert ersetzt.')
    flow.append(PageBreak())
    add('3 · Transport und Restbilanz','Title20')
    add('Alle Pfade von einer Historywurzel in P werden in zwei disjunkte Klassen zerlegt: ausschließlich bekannte aktive Punkte in Ω₅ oder mindestens ein unbekannter aktiver Außenpunkt. Der direkte Detektorbeitrag wird separat über das vollständige Raum-Zeit-Fenster eingeschlossen.')
    add('B<sub>P</sub> = D<sub>Fenster</sub> + Σ |aⱼ| Fⱼ + B<sub>Außenpfade</sub>','Math20')
    r=d['archives'][0];wins=r['levels'][-1]['windows']
    table([['Beitrag · d0_r00','W0','W1']]+[[label]+[f"{value(w[k]):.10g}" for w in wins] for label,k in [('Direkt zum Detektor','direct_detector_upper'),('Über bekannte aktive Punkte','known_active_transport_upper'),('Mit unbekannten aktiven Außenpunkten','unknown_active_paths_upper'),('Gesamte Patch-Obergrenze','patch_total_upper')]],[255,120,120])
    add('Die bekannten Kanten sind durch kausale Konvexität allein vom festen Archiv abhängig. Die adjungierten Koeffizienten werden aus den validierten Detektormitteln rückwärts berechnet und durch einen getrennten Vorwärtslauf kontrolliert. Erst danach wird ihr Betrag majorisiert.')
    add('Für Pfade mit aktiven Außenpunkten wird die globale Gewichtsschranke verwendet. Die multivariate Mecke-Formel und die zeitliche Ordnung liefern den Faktor (1+γ)ⁿ[exp(γ·29/512)-1]. Das berücksichtigt die Abhängigkeit von Intervallzählungen; ein Produkt unabhängiger zufälliger Verstärkungsfaktoren wird nicht angenommen.')
    add('Was die neue Grenze nicht leistet','H20')
    add('Die Summe aller Historywurzelbeiträge ist Δ=Δ<sub>P</sub>+Δ<sub>Rest</sub>. Für Δ<sub>P</sub> liegt nun eine integrierte obere Erwartungswertschranke vor. Für Δ<sub>Rest</sub> fehlt eine entsprechende neue Auswertung. Die globale v0.19-Grenze bleibt daher unverändert bei etwa 2,36·10¹⁴ bis 3,39·10¹⁴.')
    add('<b>Eine obere Patchgrenze darf nicht von einer oberen Gesamtgrenze subtrahiert werden.</b> Ebenso beweist eine große obere Schranke keinen großen tatsächlichen Fehler. Es bleibt eine offene Zertifizierungsaufgabe, keine Widerlegung der gesamten Operatorfamilie.')
    add('Der direkte Detektoranteil dominiert derzeit die Patchbilanz. Weitere Arbeit muss dort engere Raum-Zeit-Einschließungen mit den räumlichen Flanken und dem übrigen endlichen sowie unendlichen Historybereich verbinden.')
    flow.append(PageBreak())
    add('4 · Prüfung und Reproduktion','Title20')
    c=checks['counters'];ic=checks['internal_run_checks']
    table([['Prüfung','Ergebnis'],['Physikalische Intervallüberlappungen 128 / 192 Bit',c['physical_ball_overlaps']],['Archivzählungen mit separater Ganzzahldarstellung',c['integer_count_checks']],['Separate validierte Kugelkappen-Quadraturen',ic['cap_quadratures']],['Direkte Poissonsummen mit Chernoff-Rest',ic['direct_poisson_sums']],['Kontrollpunkte der oberen Kerntabelle',c['table_point_checks']],['Bewusst fehlerhafte Kontrollen korrekt zurückgewiesen',c['negative_controls']],['Isolierter vollständiger Wiederholungslauf',f"PASS · {replay['byte_identical_result_files']} identische Ergebnisdateien"]],[335,160])
    add('Zusätzlich: exakte verschachtelte Kontrollgeometrie aus v0.19, Lorentz- und Rotationsinvarianz, vollständige Zellpartitionen, positive Pfadzerlegung, unveränderte Quelldateien und Archividentitäten. Die symbolische Wolfram-Rechnung bestätigt die Überlappungsformel. Ein unabhängiges wissenschaftliches Review wird damit nicht behauptet.')
    add('Nachvollziehbarer Stand','H20')
    add('Basis: thomasmgfeller/x6-spectral-astrolabium, Main nach PR #151.<br/>Commit: b3e2c41bb32fec02a08432b40cc95acba013952a.<br/>Rechnung: Python 3.12, python-flint 0.8.0, Arb/Acb, 128 und 192 Bit.','Small20')
    add('Das Prüfpaket enthält Herleitung, festgelegtes Protokoll, exakte Archivarrays, Quellenidentitäten, sämtliche Zell- und Punktresultate, Prüfsummen und den isolierten Wiederholungslauf. Aufruf: <b>python reproduce.py</b>. Eine schnelle Prüfung der gespeicherten Ergebnisse ist mit <b>python reproduce.py --quick</b> möglich.')
    add('Quellen und Herleitung','H20')
    add('Projektquellen v0.3, v0.5, v0.16 und v0.19; Git-Identitäten im Prüfpaket.<br/>Wolfram MathWorld: Sphere-Sphere Intersection; Kugelkappenformel.<br/>https://mathworld.wolfram.com/Sphere-SphereIntersection.html<br/>Last/Penrose: Lectures on the Poisson Process, Theorem 4.4.<br/>https://www.math.kit.edu/stoch/~last/seite/lehrbuch_poissonp/media/lastpenrose2017.pdf<br/>FLINT/python-flint: Arb- und Acb-Arithmetik sowie validierte Quadratur.<br/>https://python-flint.readthedocs.io/','Small20')
    add('Status am 29. Oktober 2026: METHOD_HOLD · G1 HOLD · neue Bestätigung NOT_RUN.','H20')
    out=HERE/'report/Lokale_aeussere_History_v0_20.pdf';out.parent.mkdir(exist_ok=True)
    def footer(c,doc):
        c.setStrokeColor(HexColor('#dbe3e7'));c.line(50,45,545,45);c.setFont('DV',8);c.setFillColor(HexColor(muted));c.drawString(50,30,'CSPP · v0.20 · 29. Oktober 2026');c.drawRightString(545,30,str(doc.page))
    SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50,topMargin=48,bottomMargin=62,title='CSPP v0.20 - Lokale äußere History',author='Thomas Gfeller / Codex').build(flow,onFirstPage=footer,onLaterPages=footer)
    print(out)
if __name__=='__main__':main()
