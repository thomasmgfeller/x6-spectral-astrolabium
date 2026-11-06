#!/usr/bin/env python3
from pathlib import Path
import json,csv,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parent
FIG=ROOT/'figures';FIG.mkdir(exist_ok=True)
PDF=ROOT/'CST_Staubball_Regularitaet_Rand_Verfeinerung_v0_2.pdf'
font='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DV',font+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB',font+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
NAVY='#123443';TEAL='#007F86';RED='#AE4435';LIGHT='#EFF5F6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.labelcolor':NAVY,'text.color':NAVY,'axes.titleweight':'bold'})
def rows(name):
    with (ROOT/'results'/name).open() as f:return [{k:float(v) for k,v in r.items()} for r in csv.DictReader(f)]
cut=rows('cutoff.csv');spec=rows('spectral.csv');summary=json.loads((ROOT/'results/verification.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(9.6,3.25),layout='constrained')
t=np.linspace(0,.5,300);v=7/4-7*t+(79/5)*t*t
axs[0].plot(t,v,color=TEAL,lw=2);axs[0].scatter([35/158],[77/79],color=RED,zorder=4)
axs[0].set(xlabel='Zeit t',ylabel=r'$\langle V\rangle$',title='Positives mittleres Minimum')
axs[0].annotate('77/79',xy=(35/158,77/79),xytext=(.27,1.2),arrowprops={'arrowstyle':'-','color':RED})
axs[1].semilogy([r['j'] for r in cut],[r['inverse_second_cutoff'] for r in cut],marker='o',color=RED,label='Quadratur')
axs[1].semilogy([r['j'] for r in cut],[r['coefficient_squared']/r['q_cutoff'] for r in cut],ls='--',color=NAVY,label=r'$|s|^2/\epsilon$')
axs[1].set(xlabel=r'Cutoff $\epsilon=2^{-j}$: j',ylabel=r'$I_2(\epsilon,t_b)$',title='Divergenz am selben Minimum')
axs[1].legend(frameon=False,fontsize=8)
fig.savefig(FIG/'moments_cutoff.png',dpi=210);plt.close(fig)

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyDV',fontName='DV',fontSize=10.1,leading=14.5,textColor=colors.HexColor(NAVY),spaceAfter=8))
styles.add(ParagraphStyle(name='SmallDV',parent=styles['BodyDV'],fontSize=8.4,leading=11.7,spaceAfter=6))
styles.add(ParagraphStyle(name='H1DV',fontName='DVB',fontSize=23,leading=28,textColor=colors.HexColor(NAVY),spaceAfter=16))
styles.add(ParagraphStyle(name='H2DV',fontName='DVB',fontSize=12,leading=16,textColor=colors.HexColor(TEAL),spaceBefore=10,spaceAfter=8))
styles.add(ParagraphStyle(name='Kicker',fontName='DVB',fontSize=8.4,leading=12,textColor=colors.HexColor(TEAL),spaceAfter=11))
story=[];eqidx=0
def p(s,small=False):story.append(Paragraph(s,styles['SmallDV' if small else 'BodyDV']))
def h(s):story.append(Paragraph(s,styles['H2DV']))
def start(k,title):
    if story:story.append(PageBreak())
    story.append(Paragraph(k,styles['Kicker']));story.append(Paragraph(title,styles['H1DV']))
def eq(s,height=None):
    global eqidx
    eqidx+=1;path=FIG/f'eq_{eqidx:02d}.png'
    fig=plt.figure(figsize=(8,.45));fig.text(.5,.5,'$'+s+'$',ha='center',va='center',fontsize=15)
    fig.savefig(path,dpi=220,bbox_inches='tight',pad_inches=.08,transparent=True);plt.close(fig)
    from PIL import Image as PILImage
    with PILImage.open(path) as im:w,hh=im.size
    scale=min(1,490/(w*72/220));iw=w*72/220*scale;ih=hh*72/220*scale
    story.append(Image(str(path),width=iw,height=ih));story.append(Spacer(1,7))
def table(head,data,widths):
    ps=lambda s,b=False:Paragraph(('<b>'+str(s)+'</b>') if b else str(s),styles['SmallDV'])
    content=[[ps(v,True) for v in head]]+[[ps(v) for v in row] for row in data]
    tb=Table(content,colWidths=widths,hAlign='LEFT',repeatRows=1)
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(LIGHT)),('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor(TEAL)),
                           ('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#D7E2E5')),
                           ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
                           ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(tb);story.append(Spacer(1,9))

start('FORSCHUNGSPRÜFUNG · 6. NOVEMBER 2026 · v0.2','Singularitätsauflösung<br/>separat prüfen')
p('<b>Ergebnis: Die Singularitätsauflösung des CST-Staubballs bleibt unbewiesen.</b> Die Prüfung liefert eine begrenzte positive Aussage zum ersten inversen Volumenmoment, einen stärkeren Gegenbeweis zur Erhaltung des zweiten Moments und einen konkreten Hinderungsgrund am räumlichen Ballrand.')
table(['Bereich','Belastbare Aussage'],[
('Reduzierte Quantisierung','⟨V⁻¹⟩ ist bei endlicher Energie zeituniform beschränkt. Ein anfangs endliches ⟨V⁻²⟩ kann bei jeder späteren Zeit divergieren.'),
('Effektives homogenes Innere','Bei festem ν &gt; 0 sind Dichte und Krümmung begrenzt; ein lokaler Durchgang ist möglich. Für ν → 0 wächst Kmax wie ν⁻⁴.'),
('Endlicher Ball mit Außenraum','Der glatte Anschluss des geprüften Bounce-Inneren an konstante Schwarzschild-Masse scheitert unter den üblichen Einstein-Anschlussbedingungen.'),
('Dynamische vierdimensionale CST','Dichte-/Krümmungsoperator, uniforme Verfeinerung, konsistenter Außenraum und globale kausale Fortsetzung fehlen. Status: HOLD.')],[149,348])
h('Was dieser Schritt ergänzt')
p('Das neue Quantenbeispiel beginnt kontrahierend und mit endlichem zweiten inversen Moment. Damit entfällt die Einschränkung der vorherigen Gaußtests, die bereits anfänglich ein divergentes Moment hatten. Die Divergenz folgt analytisch; eine getrennte Sinusentwicklung kontrolliert die Wellenfunktion.')
p('Ein hinreichendes mathematisches Kriterium beschreibt, wie selten sehr kleine Volumina bei jeder Verfeinerung sein müssten. Die Randrechnung unterscheidet anschließend die periodische Modellzelle ausdrücklich von einem endlichen Staubball.')
h('Reichweite')
p('Inverse Volumenmomente sind hier definierte Volumenobservablen. Ihre Gleichsetzung mit physikalischer Dichte oder Krümmung ist nicht vorausgesetzt. Weder das neue Gegenbeispiel noch der Rand-Ausschluss widerlegt die gesamte CST. Horizonte und Schwarze Löcher erhalten aus diesen Rechnungen keine neue physikalische Freigabe.')
p('Analytische Untersuchung mit reproduzierbaren Referenzrechnungen; keine neuen CST-Ensembles und keine Messdaten. Vollständige Ableitungen: DERIVATION.md im Prüfpaket.',True)

start('01 · ZUSTAND UND DYNAMISCHE DOMÄNE','Anfangs endlich,<br/>später divergent')
p('Es gilt unverändert q = √V &gt; 0, H = κℏ²∂q², κ = 3πG/2, Maß dq und Dirichlet-Rand. Für E = ℏ²∫|ψ′|²dq liefert Hardy zusammen mit Energieerhaltung [P1]:')
eq(r'\langle V^{-1}\rangle_t\leq 4E/\hbar^2\qquad\mathrm{f\ddot ur\ alle}\ t')
p('Die Erwartungswerte werden als positive quadratische Formen verstanden: ⟨V⁻ᵖ⟩ = ‖q⁻ᵖψ‖². Unitarität erhält die Norm, aber nicht automatisch diese gewichteten Domänen.')
h('Neue kontrahierende Präparation')
eq(r'\psi_0=Nq^3e^{-zq^2},\quad z=\alpha-i\beta,\quad N^2=\frac{2(2\alpha)^{7/2}}{\Gamma(7/2)}')
p('Für α, β &gt; 0 ist die ungerade Fortsetzung eine Schwartz-Funktion. Anfangs sind ⟨V⁻¹⟩ = 4α/5 und ⟨V⁻²⟩ = 16α²/15 endlich. Der Anfangsstrom ist J = 7ℏβ/α &gt; 0, also d⟨V⟩/dt = −2κJ &lt; 0.')
eq(r'\psi(q,t)=ND^{-7/2}q(q^2-6i\tau D)e^{-zq^2/D},\quad D=1-4iz\tau,\ \tau=\kappa\hbar t')
p('Die Lösung folgt durch Ableitung der entwickelten Funktion q exp(−zq²) nach −z. Für reelle Zeiten ist D ≠ 0 und Re(z/D) = α/|D|² &gt; 0. Am Rand ergibt sich ψ = s(t)q + O(q³):')
eq(r'|s(t)|^2=36\tau^2N^2/|D|^5>0\quad(t\ne0)')
eq(r'\int_\epsilon^\infty\frac{|\psi(q,t)|^2}{q^4}\,dq=\frac{|s(t)|^2}{\epsilon}+O(1)')
p('<b>Folgerung:</b> ⟨V⁻²⟩ ist anfangs endlich und für jedes t &gt; 0 unendlich. Dennoch besitzt ⟨V⟩ ein positives Minimum. Für α = κ = ℏ = 1, β = 1/2 gilt exakt:')
eq(r'\langle V(t)\rangle=\frac{7}{4}-7t+\frac{79}{5}t^2,\quad t_b=\frac{35}{158},\quad V_b=\frac{77}{79}')
p('Das ist ein Gegenbeispiel zur Erhaltung des zweiten inversen Moments, kein Nachweis einer physikalischen Raumzeitsingularität. Die Masse M̂ = −H ist ein nicht mit V kommutierender Operator; ⟨M̂⟩⟨V⁻¹⟩ ist deshalb kein hergeleiteter Dichteerwartungswert.',True)

start('02 · AUSGEFÜHRTE RECHNUNGEN','Verfeinerung legt<br/>die Divergenz offen')
story.append(Image(str(FIG/'moments_cutoff.png'),width=497,height=168));story.append(Spacer(1,10))
p('Links das exakte mittlere Volumen des neuen Zustands. Rechts das regulierte zweite inverse Moment am selben Zeitpunkt t_b. Der endliche Wert auf jedem einzelnen Raster ist kein Regularitätsnachweis.',True)
table(['q-Cutoff ε','I₂(ε,t<sub>b</sub>)','ε I₂'],[[f'2<super>−{int(r["j"])}</super>',f'{r["inverse_second_cutoff"]:,.3f}'.replace(',',' ').replace('.',','),f'{r["scaled"]:.6f}'.replace('.',',')] for r in cut if r['j'] in [6,8,10,14]],[145,190,162])
p('Analytischer Grenzwert der letzten Spalte: |s(t_b)|² = 9,5788530104. Die Divergenz folgt aus dem linearen Randterm; die elf Quadraturen überprüfen die vorausgesagte Skalierung.')
h('Unabhängiger Entwicklungsweg')
p('Die Sinusentwicklung auf 0 &lt; q &lt; 16 mit 512 bis 8192 inneren Punkten verwendet die Eigenphasen desselben Operators. Maximaler diskreter L²-Abstand zur exakten Lösung: 9,43 · 10⁻¹⁶. Sechs Momentkontrollen bestätigen die Volumenformel; die Normabweichung bleibt unter 8,89 · 10⁻¹⁶.')
p('Kein Zeitschrittfehler und keine Intervallzertifizierung. Der direkte Vergleich mit der Halbgeradenlösung kontrolliert den endlichen oberen Rand für diese Fälle.',True)
h('Cutoff und Gitter sind verschiedene Regulatoren')
eq(r'h\sum_{j\geq1}\frac{|\psi(jh)|^2}{(jh)^4}\sim\frac{\pi^2|s|^2}{6h}')
p('Bei der Gittersumme ist der Vorfaktor π²/6 größer als beim Integralausschnitt. Auf den fünf Gittern steigt hI₂ von 14,8444 auf 15,6986; der vorausgesagte Grenzwert ist 15,7566. Eine genaue Wellenfunktion beseitigt das unbeschränkte Moment nicht.')

start('03 · HINREICHENDER REGULARITÄTSSATZ','Was bei Verfeinerung<br/>uniform gelten müsste')
p('Sei Vₙ(t) &gt; 0 eine positive Volumenobservable mit normierter Einzeitverteilung, n eine physikalisch abgeglichene Verfeinerung und I ein festes Zeitfenster. Eine hinreichende Voraussetzung lautet mit festen C, v₀ &gt; 0 und δ &gt; 0:')
eq(r'\sup_{n,t\in I}\Pr(V_n(t)\leq v)\leq Cv^{2+\delta}\quad(0<v\leq v_0)')
p('Aus der Schichtintegration folgt unmittelbar eine von n und t unabhängige Schranke:')
eq(r'\mathbb{E}[V_n^{-2}]=2\int_0^\infty\frac{F_n(v)}{v^3}\,dv\leq v_0^{-2}+\frac{2C}{\delta}v_0^\delta')
p('Der unbeobachtete kleine Volumenteil ist zusätzlich gleichmäßig kontrolliert:')
eq(r'\sup_{n,t}\mathbb{E}[V_n^{-2};V_n<\eta]\leq C(1+2/\delta)\eta^\delta\longrightarrow0')
p('Dies beweist uniforme Integrierbarkeit. Zusammen mit schwacher Verteilungskonvergenz folgen konvergierende inverse Momente zu jeder festen Zeit. Für eine zeituniforme Konvergenzaussage müssen auch die beschränkten abgeschnittenen Observablen zeituniform konvergieren.')
h('Warum ein endliches Maximum in einigen Läufen nicht genügt')
p('Setze P(Vₙ = εₙ) = εₙᵃ und P(Vₙ = 1) = 1 − εₙᵃ mit εₙ = 2⁻ⁿ. Das mittlere Volumen geht stets gegen eins. Trotzdem gilt:')
table(['Kleine-Volumen-Gewicht','Zweites inverses Moment'],[
('a = 1','Divergiert bei Verfeinerung.'),('a = 2','Bleibt beschränkt und geht gegen 2, während die Grenzverteilung das Moment 1 hat.'),('a = 3','Geht in dieser Kontrollfamilie korrekt gegen 1.')],[185,312])
p('24 exakte rationale Kontrollwerte sind enthalten. Ein endliches Ensemble ohne kleine-Volumen-Treffer kann den gesamten unbeobachteten Tail nicht ausschließen.')
h('Die physikalische Brücke bleibt offen')
p('Der neue Quantenzeuge besitzt für t ≠ 0 den Tail F(v) ∼ |s|²v³ᐟ²/3 und verfehlt das Kriterium. Eine Krümmungsschranke benötigt zusätzlich einen begründeten Operatorbezug, beispielsweise einen nachgewiesenen Formvergleich 0 ≤ K̂ ≤ a₀ + a₂V̂⁻². Ein solcher Vergleich ist hier nicht hergeleitet. Beschränkte skalare Momente allein beweisen keine kausale Vollständigkeit.')

start('04 · POSTULIERTE EFFEKTIVE METRIK','Reguläres Inneres<br/>bei fester Modellskala')
p('Dieser Abschnitt betrifft das gesonderte effektive Sinus-Modell [P1], nicht die zuvor entwickelte Wellenfunktion. Es setzt eine klassische Metrik mit a ∝ V¹ᐟ³ und fester Staubmasse M voraus:')
eq(r'V=b+ct^2,\quad b=M/\rho_B>0,\quad c=6\pi GM,\quad\rho_B=24\pi G\hbar^2/\nu^2')
p('Die Staubdichte bleibt durch ρ_B beschränkt. Für die räumlich flache Metrik folgt mit x = ct²/b:')
eq(r'K=\frac{16}{27}\frac{c^2}{b^2}\frac{9-6x+5x^2}{(1+x)^4}\leq192\pi^2G^2\rho_B^2')
p('Das Maximum liegt bei t = 0. Die Differenz der relevanten Zähler lautet 42x + 49x² + 36x³ + 9x⁴ ≥ 0. Bei festen b,c &gt; 0 ist die Innenmetrik glatt und erlaubt die lokale kausale Fortsetzung durch die Umkehr.')
h('Numerischer Schritt und physikalischer Parameter')
table(['Veränderung','Folge'],[
('Δt → 0, ν fest','Die Ablesung nähert sich einer festen endlichen Krümmungsspitze.'),
('ν halbiert, M,G,ℏ fest','Die Umkehrdichte steigt um Faktor 4; die maximale Krümmung um Faktor 16.'),
('CST-Verfeinerung','Benötigt eine eigene Zuordnung der Zustände und Observablen bei gleichen physikalischen Daten. Nicht durch Δt oder ν ersetzt.')],[185,312])
p('In Einheiten 6πG = M = ℏ = 1 ergeben sich folgende exakten Modellwerte:')
table(['ν','Vmin','ρ_B','Kmax'],[
('1','1/4','4','256/3'),('1/2','1/16','16','4096/3'),('1/4','1/64','64','65536/3'),('1/8','1/256','256','1048576/3')],[94,125,105,173])
p('<b>Keine uniforme Singularitätsauflösung für ν → 0.</b> Die Metrik nähert sich abseits der Umkehr der klassischen Lösung, aber nicht regulär durch t = 0. Soll ν fest physikalisch sein, muss seine Herkunft aus der mikroskopischen Theorie begründet werden.')
p('Eine vollständig homogene Fortsetzung auf ganz R³ und alle Zeiten ist bei a ≥ a_min &gt; 0 kausal vollständig. Dieser zusätzliche globale Modellansatz ist kein Nachweis für einen Ball, dessen Geodäten die Oberfläche und den Außenraum durchlaufen.',True)

start('05 · RÄUMLICHER RAND UND AUSSENRAUM','Der einfache Anschluss<br/>an Schwarzschild scheitert')
p('Nun wird die effektive flache Innenmetrik auf 0 ≤ r ≤ r<sub>b</sub> beschränkt: R<sub>b</sub> = ar<sub>b</sub> und V = 4πR<sub>b</sub>³/3. Diese Deutung als gesamtes Ballvolumen ist eine neue metrische Annahme. Die periodische Quantisierung liefert den Ballrand nicht automatisch.')
p('Ohne Oberflächenschicht verlangen die üblichen Einstein-Darmois-Israel-Bedingungen [h<sub>ab</sub>] = [K<sub>ab</sub>] = 0. Die Winkelkomponente der extrinsischen Krümmung erzwingt die Gleichheit der inneren Misner-Sharp-Masse mit der Schwarzschild-Masse [L4]:')
eq(r'm_- =\frac{H_a^2R_b^3}{2G}=\frac{\dot V^2}{24\pi GV}=M_+')
p('Innen gilt K<super>θ</super><sub>θ</sub> = 1/R<sub>b</sub>; außen K<super>θ</super><sub>θ</sub> = √(Ṙ<sub>b</sub>² + 1 − 2GM₊/R<sub>b</sub>)/R<sub>b</sub>. Gleichheit verlangt Ṙ<sub>b</sub>² = 2GM₊/R<sub>b</sub>. Die folgende Massenbedingung ist invariant und kein Artefakt der Schwarzschild-Zeitkoordinate.')
eq(r'V=b+6\pi GMt^2\quad\Longrightarrow\quad m_-=M\left(1-\frac{b}{V}\right)')
table(['x = ct²/b','0','1','4','9'],[['(M − m₋)/M','100 %','50 %','20 %','10 %']],[169,82,82,82,82])
p('<b>Am Bounce ist m₋ = 0 bei positiver Staubmasse M.</b> Der Wert ist zeitabhängig; auch eine andere konstante Außenmasse kann ihn nicht auf einem offenen Zeitintervall treffen. Für den klassischen Ast b = 0 erhält man dagegen m₋ = M.')
h('Derselbe Konflikt als effektiver Oberflächendruck')
eq(r'\rho_{\mathrm{eff}}=\frac{M}{V}\left(1-\frac{b}{V}\right),\qquad p_{\mathrm{eff}}=-\frac{Mb}{V^2}')
p('Der nichtverschwindende effektive Druck an der mitbewegten Oberfläche passt nicht zu einem schalenfreien Vakuumanschluss. Die Größen sind aus der angenommenen Metrik abgelesen; sie sind keine hergeleitete CST-Materie. 19 rationale Kontrollen bestätigen die algebraischen Identitäten.')
p('Ein geeigneter nichtvakuumartiger Außenraum, eine endliche Übergangszone oder modifizierte Anschlussgesetze müssten aus derselben Theorie bestimmt werden. Eine willkürlich eingesetzte dünne Schale löst die Regularitätsfrage nicht: Distributionelle Krümmung kann nicht naiv quadriert werden.')
p('Geltungsbereich: flaches homogenes Inneres, mitbewegte Oberfläche, Schwarzschild außen und die genannten Anschlussbedingungen. Kein allgemeiner Ausschluss regulärer Staubbälle. Ein bloßer endlicher Dichtesprung bei stetiger extrinsischer Krümmung ist im klassischen Modell nicht schon eine Singularität.',True)

start('06 · CST UND FREIGABE','Drei Ränder,<br/>drei unterschiedliche Prüfungen')
table(['Rand','Bedeutung'],[('q = 0','Rand des reduzierten Konfigurationsraums; Wahl der selbstadjungierten Quantendynamik.'),('r = r_b','Zeitartige materielle Oberfläche; Anschluss von Innen- und Außenraum.'),('Anfangs-/Endzeit','Begrenzung des beobachteten oder summierten Raumzeitgebiets.')],[123,374])
p('Die bisherigen Korrekturen endlicher Zeitfenster schließen den räumlichen Ballrand nicht. In einer vollständigen Raumzeit ist die Stauboberfläche außerdem kein Ende der Kausalordnung: Intervalle können aus dem Staub in den Vakuumaußenraum reichen.')
p('Schneidet man den Außenraum ab, entsteht ein künstlicher zeitartiger Gebietsrand. Für Minkowski-Teilgebiete stützen analytische und numerische Befunde einen mit ℓ⁻¹ divergierenden mittleren CST-Wirkungsbeitrag [L2]. Das ist eine dort gestützte Vermutung, kein hier bewiesener Satz über gekrümmte Staubbälle und keine Krümmungssingularität. Raumartige Randterme [L3] dürfen nicht ungeprüft übernommen werden.')
h('Mindestbedingungen für eine physikalische Freigabe')
table(['Prüfung','Stand nach diesem Schritt'],[
('Dichte-/Krümmungsoperator mit Domäne und Klassikbezug','HOLD'),
('Dynamischer CST-Kern mit regulären Anfangsdaten','HOLD'),
('Uniforme Tail- oder gleichwertige Operatorabschätzung','Kriterium formuliert; CST-Nachweis offen'),
('Verfeinerung bei gleicher Masse, Region, Präparation und physikalischer Glättung','NOT_RUN für CST'),
('Konsistente Oberfläche, Randwirkung und Außenraum','HOLD; einfacher Schwarzschild-Anschluss ausgeschlossen'),
('Kausale Fortsetzung im Inneren, durch die Oberfläche und außen','HOLD')],[322,175])
p('Bei nichtlokalen Operatoren braucht das Weglassen äußerer Intervalle eine quantitative Fehlerschranke. Den Randbereich bei jeder Verfeinerung auszuschließen beweist keine globale Regularität. Die materielle Grenzfläche muss einschließlich kreuzender Intervalle untersucht werden.')
p('<b>Freigabegrenze:</b> Erst nach diesen Nachweisen folgen Aussagen über eine reguläre globale Raumzeit. Horizontberechnungen auf vorgegebenen Metriken bleiben Referenzdiagnostik.',True)

start('07 · NACHVOLLZIEHBARKEIT','Beweise, Kontrollen<br/>und Quellen')
p('Das Prüfpaket enthält die vollständigen Ableitungen, ausführbaren Code, sieben Ergebnistabellen, die maschinenlesbare Entscheidung und Abbildungen. Die mathematischen Aussagen und numerischen Kontrollen sind getrennt gekennzeichnet.')
table(['Ausgeführt','Umfang'],[('Momente und Norm','6 Zeiten, zusätzlich Anfangsregularität'),('Cutoff-Skalierung','11 untere q-Grenzen'),('Getrennte Sinusentwicklung','5 räumliche Auflösungen'),('Effektive Randidentitäten','19 rationale Fälle plus allgemeine Ableitung'),('Seltene kleine Volumina','24 rationale Kontrollfälle'),('Skalenkontrolle','4 numerische und 4 physikalische Stufen')],[220,277])
p('<b>Wiederholung:</b> Im entpackten Ordner zunächst <font face="DVB">sha256sum -c SHA256SUMS</font>, dann <font face="DVB">python3 verify.py</font>. Python 3.10+, NumPy und SciPy genügen für die Rechnung. Die Erstellung des PDFs benötigt zusätzlich Matplotlib und ReportLab. Gleitkommawerte können in letzten Stellen abweichen.',True)
h('Gelesene Projektgrundlagen')
p('[P1] <b>Staubball_Bounce_Regularitaet</b>, 4.11.2026: Hardy-Schranke, Zeitintervall-Satz und effektive Innenmetrik. [P2] <b>Unabhängige Bounce-Vorhersage v0.1</b>, 5.11.2026: Gaußfälle und deren anfangs divergente Momente. [P3] <b>Klassik/Rückwirkung</b> und <b>Historiengewichtung v0.1</b>, 5.11.2026: Referenzoperator und Maß. [P4] Aktuelle Projektübersicht, gelesener Blob-SHA b77d3bbcd80f0ed9b4c8fcde3913c33ebbf1db6d. Links und Herkunft stehen vollständig in DERIVATION.md.',True)
h('Primärliteratur · am 6.11.2026 geprüft')
for s in [
'[L1] H. Maeda (2015), Unitary evolution of the quantum universe with a Brown-Kuchař dust. <link href="https://arxiv.org/abs/1502.06954" color="#007F86">arXiv:1502.06954</link>. Hintergrund zur reduzierten Staubquantisierung.',
'[L2] F. Dowker, R. Liu, D. Lloyd-Jones (2025), Timelike boundary and corner terms in the causal set action. <link href="https://arxiv.org/abs/2501.00139" color="#007F86">arXiv:2501.00139</link>. Zeitartige Randskalierung.',
'[L3] M. Buck, F. Dowker, I. Jubb, S. Surya (2015), Boundary Terms for Causal Sets. <link href="https://arxiv.org/abs/1502.05388" color="#007F86">arXiv:1502.05388</link>. Raumartige Randterme.',
'[L4] L. Buoninfante et al. (2025), Dust collapse and horizon formation in Quadratic Gravity. <link href="https://arxiv.org/html/2410.05941v2" color="#007F86">arXiv:2410.05941v2</link>, Abschn. 5.1-5.2. Hier nur für die üblichen geometrischen Anschlussbedingungen verwendet.',
'[L5] I. Jubb et al. (2016), Boundary and Corner Terms in the Action for General Relativity. <link href="https://arxiv.org/abs/1612.00149" color="#007F86">arXiv:1612.00149</link>. Variationsprinzip und Randtypen.']:
    p(s,True)
p('Die neuen Gegenbeispiel-, Tail- und Ballrandrechnungen sind eigene Ableitungen dieses Pakets. Literaturbefunde werden nicht als Nachweis einer bereits hergeleiteten CST-Singularitätsauflösung ausgegeben.',True)

def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#D7E2E5'));canvas.line(49,44,546,44)
    canvas.setFont('DV',8);canvas.setFillColor(colors.HexColor(NAVY))
    canvas.drawString(49,29,'X6 Astrolabium · Regularität, Rand und Verfeinerung v0.2')
    canvas.drawRightString(546,29,str(doc.page))
doc=SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),rightMargin=49,leftMargin=49,topMargin=44,bottomMargin=57,
                      title='CST-Staubball: Regularität, Rand und Verfeinerung v0.2',author='X6 Astrolabium - Forschungsprüfung')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(PDF)
