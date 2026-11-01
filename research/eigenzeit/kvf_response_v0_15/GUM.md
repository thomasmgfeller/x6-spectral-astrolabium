# Gemeinsame Unsicherheit des Antwortvektors

Grundlage: JCGM 100:2008 Abschnitt 8, Amd.1:2026 sowie JCGM 102:2011.
Die Zuordnung der Eingangsverteilungen ist Teil des synthetischen
Vertrags; sie ist kein Beleg realer Kalibrierwerte. Die Entscheidungsrisiken
werden getrennt im Rohdatenmodell begrenzt. Die frühere C01-Grenze
von 2 ppm wird nicht übernommen.

| GUM-Schritt | Ausführung in v0.15 |
|---|---|
| 1. Messmodell | R_s=(D_s-c_common-c_s)/K, s=1,...,4. |
| 2. Eingangsschätzwerte | Vier Mittelwerte der vollständigen ABBA-Blockkontraste; K=1, fünf Korrekturen mit Erwartungswert null. |
| 3. Standardunsicherheiten | Streuung der Blockvektoren; Rechteckverteilungen für gemeinsamen Rest (+/-0.0003), vier lokale Reste (je +/-0.0002) und K (+/-0.01). |
| 4. Kovarianzen | Alle vier Blockkomponenten gemeinsam auswerten; gemeinsame Korrektur und gemeinsamer Gain erzeugen zusätzliche Ausgangskovarianzen. |
| 5. Ausgangsschätzung | F(E[X]) und E[F(X)] getrennt ausweisen; der Quotient erlaubt exakte erste Momente. |
| 6. Fortpflanzung | U_R=J U_X J^T und exakte zweite Momente desselben zugewiesenen Modells vergleichen. |
| 7. Überdeckung | Gemeinsames Ellipsoid; Radius aus 500000 PDF-Ziehungen, unabhängige numerische Kontrollen. |
| 8. Bericht | Eingänge, vollständige Kovarianzen, Schätzwerte, Bereich, Einheiten, Verfahren, Datenbezug und Grenzen in JSON/PDF. |

## Typ-A-Verteilung und Kovarianz

Für n=2048 unabhängige gaußsche Blockvektoren der Dimension d=4 seien
bar D und die Stichprobenkovarianz S gegeben. U_A=S/n.
Die Verteilungszuordnung nach JCGM 102, 5.3.2 und 9.4.2.4-9.4.2.6
verwendet eine multivariate t-Verteilung mit nu=n-d und
Skalenmatrix (n-1)S/(nu*n). Ihre Kovarianz ist

$$U_T=\frac{n-1}{n-d-2}U_A.$$

Diese Korrektur wird auch in U_X für die Rechnung erster Ordnung
verwendet. Sie vermeidet einen Vergleich verschiedener Eingangsmodelle.
Die Eingangsreihenfolge, 10x10-Kovarianz und 4x10-Sensitivitätsmatrix
stehen in records/M0.json und records/M1.json.
Die Ableitungen sind dR_s/dD_j=delta_sj/K,
dR_s/dc_common=-1/K, dR_s/dc_j=-delta_sj/K,
dR_s/dK=-(D_s-c_common-c_s)/K^2.

## Exakte Momentenfortpflanzung

Sei Z=D-c_common*1-c_local. Dann

$$\mu_Z=\bar D,\quad
V_Z=U_T+\frac{0.0003^2}{3}\mathbf1\mathbf1^T
          +\frac{0.0002^2}{3}I.$$

K ist unabhängig und gleichverteilt auf [1-h,1+h], h=0.01. Mit

$$a=E[K^{-1}]=\frac{\log(1+h)-\log(1-h)}{2h},\quad
b=E[K^{-2}]=\frac1{1-h^2}$$

folgt ohne Linearisierungsfehler innerhalb dieser PDF-Zuordnung

$$E[R]=a\mu_Z,\qquad
\operatorname{Cov}(R)=b V_Z+(b-a^2)\mu_Z\mu_Z^T.$$

So wird die Nichtlinearität direkt berücksichtigt, wie es die
Nichtlinearitäts-Ergänzung 2026 verlangt. Die Auswertung erster Ordnung
bleibt als Vergleich sichtbar. Gemeinsame Kovarianzen werden nicht
durch vier unabhängige Fehlerbalken ersetzt.

## Gemeinsamer Bereich und offen ausgewiesene Kontrollen

Das Ellipsoid ist (R-mu_R)^T U_R^-1 (R-mu_R)<=q.
q ist die vorab festgelegte empirische 95-%-Quantile aus 500000 Ziehungen;
die Momente mu_R und U_R sind analytisch gegeben. Der Radius hat selbst
Monte-Carlo-Unsicherheit. Ein adaptiver JCGM-102-Algorithmus aus 7.8 wird
nicht beansprucht.

Die ersten unabhängigen 100000 Ziehungen ergaben 95056 Treffer für M0
und 94820 für M1. Das M1-Intervall mit 99 % Konfidenz liegt knapp unter
0.95. Daraufhin wurden AUDIT_PLAN.json und der separate Auditcode
fixiert: je eine Million neue Ziehungen, unveränderte Rohdaten und Radien,
keine Wiederholung bis zu einem gewünschten Ergebnis.

Der Audit verwendet SciPys multivariate t-Erzeugung statt der ursprünglichen
Normal-/Chi-Quadrat-Konstruktion. Er liefert 950014 beziehungsweise
950158 Treffer. Die beiden 99.5-%-Binomialintervalle sind gemeinsam mit
mindestens 99 % abgesichert und enthalten jeweils 0.95:
[0.94939928,0.95062368] und [0.94954412,0.95076685].
Das belegt numerische Verträglichkeit mit dem Zielwert unter den
zugeordneten PDFs; keine exakt garantierte 95-%-Überdeckung.

Die bekannte nominelle M1-Antwort liegt in der einen synthetischen
Rohdatenrealisation außerhalb des geschätzten Ellipsoids
(quadratischer Abstand 13.13249 gegenüber Radiusquadrat 9.29723).
Dieser Ausreißer bleibt erhalten. Eine PDF-Kontrolle ist keine
frequentistische Validierung über beliebige wahre Parameter oder
über wiederholte vollständige Laborexperimente.

## Einheiten und Grenzen

R und die additiven Korrekturen: ell0^-2; ihre Kovarianzen: ell0^-4.
K ist dimensionslos. Nulltests erhalten absolute Grenzen.
Unsichere geometrische Einstellungen begrenzen hier die Modellfamilie
über harte Intervalle; sie werden nicht zusätzlich als unabhängige
PDF-Beiträge zur gemessenen Antwort eingerechnet. Das würde eine weitere
Modellzuordnung benötigen. Numerische Integrationskontrollen sind
ebenfalls separat ausgewiesen.
