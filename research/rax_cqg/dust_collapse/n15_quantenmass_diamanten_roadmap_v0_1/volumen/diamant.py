"""Synthetic FLRW causal diamonds, no observational inputs. Run in Python with mpmath."""
import json
from pathlib import Path
import mpmath as mp

DURATIONS = (4, 8, 16, 32)

def exterior(omega):
    """a(eta), proper time s(eta), spatial ball volume; a(0)=1, H(0)=1."""
    if omega == 1:
        return (lambda eta: (1 + eta/2)**2,
                lambda eta: eta + eta**2/2 + eta**3/12,
                lambda r: 4*mp.pi*r**3/3)
    k = 1-omega  # nonnegative Omega_k, spatial curvature K=-k
    beta = mp.sqrt(k)
    def scale(eta):
        x = beta*eta
        return mp.cosh(x) + mp.sinh(x)/beta + omega/(2*k)*(mp.cosh(x)-1)
    def time(eta):
        x = beta*eta
        return mp.sinh(x)/beta + (mp.cosh(x)-1)/k + omega/(2*k)*(mp.sinh(x)/beta-eta)
    def ball(r):
        return 4*mp.pi*(mp.sinh(2*beta*r)/(4*beta**3)-r/(2*k))
    return scale, time, ball

def four_volume(tau, functions):
    scale, time, ball = functions
    eta_lo = mp.findroot(lambda eta: time(eta)+tau/2, -tau/2)
    eta_hi = mp.findroot(lambda eta: time(eta)-tau/2, tau/2)
    if max(abs(time(eta_lo)+tau/2),abs(time(eta_hi)-tau/2)) > mp.mpf('1e-50'):
        raise ArithmeticError('Endpoint proper-time residual.')
    eta_cross = (eta_lo+eta_hi)/2
    left = mp.quad(lambda eta: scale(eta)**4*ball(eta-eta_lo), [eta_lo, eta_cross])
    right = mp.quad(lambda eta: scale(eta)**4*ball(eta_hi-eta), [eta_cross, eta_hi])
    return left+right

def run():
    mp.mp.dps = 60
    flat_control = (lambda eta: 1,lambda eta: eta,lambda r: 4*mp.pi*r**3/3)
    result = []
    for den in DURATIONS:
        tau = mp.mpf(1)/den
        v0 = mp.pi*tau**4/24
        control_err = abs(four_volume(tau, flat_control)/v0-1)
        if control_err > mp.mpf('1e-50'):
            raise ArithmeticError('Minkowski four-volume error')
        row = {'H0_tau_in_dust_models': '1/'+str(den), 'Minkowski_relative_error':mp.nstr(control_err,5)}
        for name,m in [('flat_dust',mp.mpf(1)),('open_dust',mp.mpf(64)/125)]:
            data = exterior(m)
            a, s, ball = data
            for eta in (-tau/2, tau/2):
                if abs(mp.diff(s, eta) - a(eta)) > mp.mpf('1e-49') or abs(mp.diff(a,eta)**2 - m*a(eta) - (1-m)*a(eta)**2) > mp.mpf('1e-49'):
                    raise ArithmeticError('Conformal dust Friedmann equation or lapse.')
            ratio = four_volume(tau,data)/v0
            estimate = (ratio-1)/tau**2
            # Gibbons & Solodukhin, Eq. (73), with R/H0²=3m and R_uu/H0²=3m/2.
            prediction = m/20 - m/60
            row[name] = {k:mp.nstr(v,25) for k,v in [
                ('ratio_to_Minkowski',ratio),('quadratic_coefficient',estimate),
                ('Ricci_prediction',prediction),('abs_difference',abs(estimate-prediction))]}
        result.append(row)
    for name in ('flat_dust','open_dust'):
        err = [mp.mpf(r[name]['abs_difference']) for r in result]
        if not all(b<a/3 for a,b in zip(err,err[1:])) or err[-1] > mp.mpf('5e-5'):
            raise ArithmeticError('Small-duration control did not converge to Ricci coefficient.')
    return result

if __name__ == '__main__':
    out = Path(__file__).with_name('diamant.json')
    out.write_text(json.dumps(run(),indent=2)+'\n',encoding='utf-8')
