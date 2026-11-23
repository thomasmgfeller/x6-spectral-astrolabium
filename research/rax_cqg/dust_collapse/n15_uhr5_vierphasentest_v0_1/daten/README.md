# Datenpilot für flaches ΛCDM mit DESI DR2 und Pantheon+

Der Pilot prüft, ob sich publizierte Referenzparameter aus reduzierten Messwerten und ihren Kovarianzen wiedergewinnen lassen. Die gemeinsame Analyse liefert einen Vergleichswert für künftige Tests einer separat herzuleitenden Staubball- oder Everpresent-Λ-Vorhersage.

## Ergebnisse

Die Parameter sind marginale Posteriormittel mit einer Standardabweichung. Die letzte Spalte zeigt das Minimum der quadratischen Residuen nach Anpassung der freien Parameter. $h=H_0/(100\,\mathrm{km\,s^{-1}\,Mpc^{-1}})$, $r_d$ ist der Schallhorizont an der baryonischen Entkopplung (drag epoch).

| Daten | Ωm | h r_d in Mpc | Korrelation | χ² am Minimum / nominale Freiheitsgrade |
| --- | ---: | ---: | ---: | ---: |
| DESI DR2 | 0,29783 ± 0,00863 | 101,523 ± 0,736 | −0,9239 | 10,271 / 11 |
| Pantheon+ allein | 0,33226 ± 0,01821 | — | — | 1402,919 / 1588 |
| DESI DR2 und Pantheon+ | 0,30447 ± 0,00795 | 101,003 ± 0,673 | −0,9094 | 1416,139 / 1600 |

DESI Gl. (17) gibt $0{,}2975\pm0{,}0086$, $101{,}54\pm0{,}73\,\mathrm{Mpc}$ und eine Korrelation von −0,92 an. Unsere Mittelwerte weichen um +0,038 bzw. −0,023 der jeweils publizierten Standardabweichung ab. Beide Rechnungen verwenden dieselben BAO-Messungen. Zum Vergleich liegt das Maximum unserer DESI-Likelihood bei 0,29746 und 101,540 Mpc. Brout et al. berichten aus Supernovae allein $0{,}334\pm0{,}018$. Unser SN-Mittel liegt um rund 0,10 ihrer Standardabweichung darunter. [DESI DR2, Gl. (17)](https://arxiv.org/html/2503.14738v3#S6.SS1) · [Pantheon+-Analyse](https://arxiv.org/abs/2202.04077)

## Physik und Messgrössen

Wir verwenden ein räumlich flaches Friedmann-Modell mit kalter Materie und kosmologischer Konstante. In der Hauptrechnung gilt $E(z)^2=[H(z)/H_0]^2=1+\Omega_m[(1+z)^3-1]$. Für die BAO-Einträge ergeben sich

$$
\frac{D_M(z)}{r_d}=\frac{c}{100\,h r_d}\int_0^z\frac{dz'}{E(z')},\qquad
\frac{D_H(z)}{r_d}=\frac{c}{100\,h r_d E(z)},\qquad
\frac{D_V(z)}{r_d}=\left[z\left(\frac{D_M(z)}{r_d}\right)^2\frac{D_H(z)}{r_d}\right]^{1/3}.
$$

Hier ist $c=299792{,}458\,\mathrm{km\,s^{-1}}$, und der Faktor 100 trägt die Einheit $\mathrm{km\,s^{-1}\,Mpc^{-1}}$. Die 13 Werte aus sieben Rotverschiebungsbereichen stehen mit ihren Originalzeilen und ihrer vollen 13 × 13-Kovarianz im Fit. Die Spalte mit der Messgrösse bestimmt die Zuordnung auch für die letzten beiden Zeilen, in denen $D_H$ vor $D_M$ steht. $hr_d$ bleibt frei. Die Rechnung bestimmt daher weder $H_0$ noch $r_d$ einzeln.

Für Pantheon+ übernimmt der Pilot aus der offiziellen SN-only-Likelihood genau die Auswahl $z_{\rm HD}>0{,}01$ und die zugehörigen Zeilen **und Spalten** der STAT+SYS-Kovarianz. 1590 der 1701 Lichtkurven bleiben. Die zehn ausgewählten Kurven mit Kalibratorflag werden nach derselben $z$-Abstandsrelation behandelt wie die übrigen. Es werden weder Cepheiden-Distanzen noch die kalibrierte Spalte `MU_SH0ES` verwendet. Die dimensionslose Helligkeitsdistanz lautet $d_i=(1+z_{{\rm HEL},i})\int_0^{z_{{\rm HD},i}} dz/E(z)$. Das Modell für `m_b_corr` ist $5\log_{10} d_i+\mathcal M$, wobei der freie Helligkeitsnullpunkt $\mathcal M$ die absolute Supernovahelligkeit und die Hubble-Skala absorbiert. [Originalimplementierung von Pantheon+](https://github.com/PantheonPlusSH0ES/DataRelease/blob/c447f0fea703fcd0fff57de5000947b5ca81286b/Pantheon%2B_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon%2B_only_cosmosis_likelihood.py)

Bei $C=LL^T$, $v=L^{-1}(m_{\rm obs}-5\log_{10}d)$ und $u=L^{-1}\mathbf1$ hat der optimale Nullpunkt den Wert $\widehat{\mathcal M}=u^Tv/(u^Tu)$. Wir berechnen $\chi^2_{\rm SN}=\|v-u\widehat{\mathcal M}\|^2$. Die analytische Integration über einen konstanten, unbeschränkten Prior für $\mathcal M$ liefert zusätzlich den modellunabhängigen Faktor $\sqrt{2\pi/(u^Tu)}$. Er kürzt sich im normierten Parameterposterior. Die gemeinsame Rechnung nimmt für die veröffentlichten BAO- und SN-Residuen bedingte Unabhängigkeit bei festen kosmologischen Parametern an.

## Priors und numerische Kontrolle

* Die flachen Priors für $\Omega_m\in[0{,}01,0{,}99]$ und $hr_d\in[10,1000]\,\mathrm{Mpc}$ entsprechen der publizierten DESI-Parametrisierung für unkalibrierte Distanzen. Die Gauss-Quadratur integriert über $hr_d$ mit flachem Mass, auch wenn die Modellvorhersage linear in dessen Kehrwert ist. [DESI DR1, Tabelle 2](https://arxiv.org/html/2404.03002v3#S2.T2) · [DESI DR2, Methodik](https://arxiv.org/html/2503.14738v3#S4)
* Die Hauptrechnung vernachlässigt Strahlung über den beobachteten Rotverschiebungsbereich bis 2,33. Eine Variation bei festem $\Omega_r=0{,}00009$ ergänzt $E^2$ um $\Omega_r[(1+z)^4-1]$. DESI allein liefert dann 0,29751 ± 0,00863 und 101,532 ± 0,736 Mpc. Diese Variation misst den Einfluss eines kleinen Strahlungsbeitrags im Hintergrund. Der Pilot verwendet weder den vollständigen CAMB-Neutrinosektor noch die DESI-MCMC-Ketten. Die genaue Ursache kleiner Abweichungen lässt sich aus diesem Vergleich nicht isolieren.
* Die SN-Kovarianz ist positiv definit. Auf der tatsächlich ausgewählten Teilmatrix stimmen beide Dreieckshälften im gelieferten Text exakt überein. Für die Likelihood verwendet der Code eine Cholesky-Zerlegung und Dreieckslösungen.
* Für Distanzen nutzt der Hauptlauf 32-Punkt-Gauss-Legendre-Quadratur. Für die Posteriorintegrale wird der vollständige Prior in Intervalle unterteilt. Die Erhöhung der Ordnung von 24 auf 40 pro Intervall ändert sämtliche ausgewiesenen Momente um weniger als $10^{-11}$ in ihren jeweiligen Einheiten. Alle Grenzen sind in `datenpilot.py` angegeben.
* `gegenprobe.py` löst die Differentialgleichung für die komovierende Distanz mit DOP853. Der Kontrollfit passt die drei Parameter $\Omega_m,hr_d,\mathcal M$ gleichzeitig mit kleinsten Quadraten an. `gegenprobe.json` dokumentiert die Differenzen zum profilierten gemeinsamen Optimum. Die beiden Programme teilen sich den Bezug und die Prüfung der Eingabedateien.

## Reproduktion

Erforderlich sind Python ab 3.11, NumPy und SciPy. Die benutzten Paketversionen stehen in `ergebnis.json`. Die Programme laden beim ersten Aufruf vier öffentliche Dateien mit insgesamt rund 34 MB in den lokalen Ordner `cache/`. `quelldaten.json` enthält Dateinamen, vollständige Commit-URLs, Bytezahlen und SHA-256-Prüfsummen. Bereits verfügbare Originaldateien können mit `--cache PFAD` eingebunden werden. Ein Inhalt mit abweichender Prüfsumme beendet den Lauf.

```sh
python datenpilot.py
python gegenprobe.py
```

`ergebnis.json` enthält die publizierten DESI-Vergleichszahlen, die eigenen Mittelwerte, Standardabweichungen, Korrelationen und Minima, die Quadraturkontrolle und die Strahlungsvariation. `gegenprobe.json` hält die unabhängige numerische Prüfung des gemeinsamen Optimums fest.
