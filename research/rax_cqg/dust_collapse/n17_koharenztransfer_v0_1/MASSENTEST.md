# Zwei Randuhrfenster zur Ablesung der markierten Masse auf Typ 2324

Auf dem Weg $3\to4\to13\to7$ lässt sich die markierte Modellmasse aus zwei getrennten diagonalen Ladungsmittelwerten rekonstruieren, wenn die Präparation in beiden Randuhrfenstern denselben inneren Profilparameter $k$ verwendet. Der Leser benötigt den Wert von $k$ nicht. Lässt man eine Korrelation von Profil und Uhrfenster zu, gibt es zwei präzise angegebene Präparationen mit identischen beiden Ladungsmittelwerten und um 5 % verschiedener markierter Masse. Deshalb kommt es darauf an, ob die gewählte Präparation diese Korrelation physikalisch kontrolliert.

## Rechnung aus der Staubwirkung

Wir übernehmen aus der veröffentlichten Schnittmassenprüfung den Ordnungstyp 2324, die Massenzählung am markierten Weg und die Verweildauerregel. Die beiden inneren Uhren 4 und 13 liegen bei Anteilen $u_4=1/2-k$ und $u_{13}=k$ der Dauer $D=4\Delta-\delta$, mit $1/4<k<1/2$ und $\Delta^4=3/722$. Ihre Verweildichten sind $MD/4$ und $3MD/4$. Die übrigen inneren Dichten liegen auf dem Nullatom. Der markierte Fluss über den Anfangsschnitt ist $M$.

Der dimensionslose Uhrenoffset lautet $e=\delta/\Delta$. Die Differenz der Wirkungen bei entgegengesetzter gemeinsamer Verschiebung der vier Anfangsuhren ist bei festgehaltenen Dichten exakt linear in der Verschiebung. Die Schichtkoeffizienten von diesen Uhren zu Ereignis 4 sind $(-8,16,-9,1)$, zu Ereignis 13 sind sie $(0,-8,16,-9)$. Anfangs- und Zukunftskragen koppeln in dieser Ableitung mit Gewicht null. Einsetzen der beiden besetzten Dichten ergibt

$$76p(e)=M(4-e)\big[(1-23e)+3k(4-e)\big].$$

Als Gegenrechnung baut der Prüfer die vollständige 15-Ereignis-Ordnung aus dem Typenschlüssel auf, zählt alle offenen Intervalle und wertet beide verschobenen Wirkungen aus. Er rekonstruiert die drei Koeffizienten durch Interpolation und prüft zwei weitere rationale Uhrpunkte. Die Koeffizienten des Lesers folgen aus der analytischen Identität, unabhängig von den Prüfmassen.

## Sensor mit zwei getrennten Uhrfenstern

$L$ und $R$ sind die separat normierten Ladungsmittelwerte mit positivem diagonalem Gewicht für die feine Ladung auf $[-3/32,-1/32]$ und $[1/32,3/32]$ in $\delta$. In beiden Fenstern ist das Gewicht gleichförmig. Mit $\mu=1/(16\Delta)$ und $\nu=13/(3072\Delta^2)$ gilt $E[e\mid R]=\mu$, $E[e\mid L]=-\mu$ und $E[e^2]=\nu$ in jedem Fenster. Der Leser bildet $A=(L+R)/2$ und $B=(L-R)/(2\mu)$. Die zwei linearen Gleichungen lauten

$$76A=M[(4+23\nu)+(48+3\nu)k],\qquad 76B=M(93+24k).$$

Eliminiert man $Mk$, ergibt sich

$$\widehat M=\frac{76[(48+3\nu)B-24A]}{273(16-\nu)}.$$

Der Nenner ist strikt positiv. Numerisch hat der Leser die Form $1{,}500648\,L-1{,}919951\,R$. Je Test wurde der Marker allein in die Feldpräparation eingesetzt. Beide Eingaben des Lesers wurden anschliessend durch die symmetrische Differenz der vollständigen Wirkung berechnet. Das Verfahren reproduziert fünf markierte Dosen $0,1/4,1/2,19/20,1$ mit vier Profilen $1/3,3/8,2/5,11/24$. Der algebraische Nachweis umfasst alle gemeinsamen $k$ der angegebenen Familie mit zulässiger Dichte. Die exakten rationalen Einschliessungen der zwanzig Kontrollen haben Breite unter $10^{-34}$ beim rekonstruierten Marker. Die zwei Vakuumkontrollen, leeres Inneres mit positivem Kragen und vollständig staubfreie Belegung, liefern beide exakt null.

Bei exakt bekannten Fenstern und absoluten Lastfehlern $|\delta L|,|\delta R|\le\epsilon$ ist der dadurch induzierte Massenfehler kleiner als $3{,}420599\epsilon$. Diese Schranke deckt nur die zwei Ablesefehler. Unsicherheiten der Uhrskala, des Verweildauergesetzes und der Sektorpaarung erfordern eine eigene Begründung.

## Gegenbeispiel für unbekannte Fensterabhängigkeit

Als erste Kontrolle setze man $M=1$, $k_L=1/3$ und $k_R=11/24$. Alle Profile erfüllen die kausalen Schranken. Der unter der Annahme eines gemeinsamen Profils konstruierte Leser liefert rund $0{,}866459587137$.

Ein stärkerer Gegenversuch hält beide gemessenen Zahlen *exakt* fest. Die erste Präparation verwendet $M=1$ und $k=3/8$ in beiden Fenstern. Für die zweite wähle man $M'=19/20$ und definiere mit dem oberen Vorzeichen für links

$$a_\pm=4+23\nu\pm93\mu,\quad b_\pm=48+3\nu\pm24\mu,\quad
 k'_\pm=\frac{(a_\pm+b_\pm\,3/8)/M'-a_\pm}{b_\pm}.$$

Beide $b_\pm$ sind strikt positiv. Die zweite Präparation liefert nach direkter Substitution für jedes der beiden Fenster denselben Mittelwert wie die erste. Ihre inneren Profile liegen bei $k'_L\approx0{,}422367013589$ und $k'_R\approx0{,}373101422541$, jeweils strikt innerhalb des erlaubten Intervalls. Beide Profile können im unbeobachteten Zwischenraum stetig verbunden werden. Die ±2-%-Bänder der zwei markierten Massen sind disjunkt. Die Gleichheit beider Eingaben schliesst deshalb jeden Leser allein aus $(L,R)$ mit gleichzeitiger ±2-%-Garantie auf dieser erweiterten Klasse aus. Die einzelnen feinen Ladungsverteilungen können weitere Information enthalten.

## Physikalische Reichweite

Die positiven Modellmassen bis 1 haben auf diesem Einzelpfad für alle Offsetwerte $0<w_{13}\le 0{,}831984$. Bei $M=4$ liegt das grösste besetzte Dichtegewicht überall über $2{,}7654$ und verletzt $w<1$. Eine Einpfad-Extrapolation auf die grösste P3-Masse ist damit auf diesem Träger ausgeschlossen. Verteilte Pfade definieren eine andere Präparation und erfordern erneute Ableitung der Ladungsantwort.

Der Zweifenster-Leser verwendet zwei bedingte feine Ladungsmittel. Die früher veröffentlichte kohärente Quellantwort ist eine andere Auslese. Eine physikalische Paarung oder ein dynamisch begründetes Instrument müsste die beiden bedingten Mittel tatsächlich zugänglich machen und deren gemeinsame Präparationsvorschrift begründen. Der Marker im bekannten Hilfsmodell liefert weder eine unabhängige physikalische Eichmasse noch eine physikalische Vakuummessung. Der P3-Status bleibt bei 60 von 60 Prüfpunkten auf `NOT_RUN`. Die Ableitung und die zusätzlichen Fälle sind eine lokal ausgeführte Methodenprüfung.

## Nachrechnen

`python3 -B massentest.py` reproduziert `massentest.json` mit der Python-Standardbibliothek. Die JSON-Grenzen sind nach aussen gerundete rationale Zahlen. Die Eingaben stehen explizit im Skript.

[Markierte Schnittmasse, Wirkung und beide Uhrfenster](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/83b8a71bb96f2d794ecc35909f8102c20901f7f6/research/rax_cqg/dust_collapse/cut_mass_charge_vacuum_v0_1/README.md) · [Bisherige Einzelprofil-Kalibrierung und physikalischer Transfervertrag](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/83b8a71bb96f2d794ecc35909f8102c20901f7f6/research/rax_cqg/dust_collapse/n15_sector_norm_rest_mass_v0_1/README.md)
