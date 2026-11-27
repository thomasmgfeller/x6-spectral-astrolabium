"""Necessary consequences of the two clock equations for an earlier empty twin."""
from fractions import Fraction as F
from intervall import I
from modell import WINDOW

def bounds(pair,side):
    d=pair[side]
    y,w=([I(*v) for v in d[k]] for k in ['clock_box','weight_box'])
    def linear(z,coeff):
        offset=sum((c*w[j]*y[j] for j,c in coeff),I())
        slope=sum((c*w[j] for j,c in coeff),I())
        return offset-z*slope
    C=16*w[7]-8*w[8]
    base=-9*w[7]+16*w[8]-8*w[9]
    lower=[];cap=[];target=[];slope=[]
    amp=16 if side=='light' else 1
    # All relevant positive clocks 18 satisfy Y22<Y18<Y7 for F18.
    # The original 18->7 device correction is included in its outgoing row.
    for t in [I(F('-.04')),y[7]]:
        K=[(7,1-F(1,10**11)),(8,-9),(9,16),(10,-8)]
        assert (amp*linear(t,K)).h<F('-.00865')
    for k in range(128):
        x=I(WINDOW[0]+k*(WINDOW[1]-WINDOW[0])/128,WINDOW[0]+(k+1)*(WINDOW[1]-WINDOW[0])/128)
        z=y[3]+x*(y[7]-y[3])
        h=linear(z,[(7,-65),(8,136),(9,-72)])
        l=linear(z,[(7,9),(8,-16),(9,8)])
        assert h.h<0<l.l and C.l>0
        # G_e - (-9 times the interior part of G22) is
        # H(z)+(z-Y_e)(C-9W)-eps*w18*(Y18-Y_e)=0, W=w18+w21.
        # The final term is zero if the ancestor is 20.
        if k==0: assert z.l>F('-.04')
        Wmax=(C+h/(z-y[0]))/9
        assert (-h/(z-y[0])).l*amp>F('.008')
        assert Wmax.h>0
        min21=z.l+l.l/Wmax.h
        assert min21>y[7].h # Y18<Y7, hence only Y21 can realize this lower bound.
        lower.append(min21);cap.append(Wmax.h);slope.append(Wmax.h+base.h)
        target.append((z+h/C).h)
    assert min(lower)>F('3.26') and max(target)<F('-1.15') and max(slope)<0
    amp=16 if side=='light' else 1
    assert max(cap)*amp<F('.00270') and max(slope)*amp<F('-.00228')
    # A_s deviations from the other twin are bounded by the positive device
    # contribution eps*w18*(Y18-Y17) with gap <8. This works even if both twins precede 22.
    assert F(8,10**11)*F('.00270')/min(F('.00228'),F('.008')) < F('.000001')
    assert F('-.00865')/F('.00270') < -3
    # The other twin, when incomparable to 22, has G_e=(z-Y_e)(W+base)
    # minus a possible device term of magnitude < eps*8*w18. With both earlier,
    # their common affine uncorrected G has slope magnitude C-9W >= -H/(z-Y0).
    return dict(terminal_min=str(min(lower)),ancestor_max=str(max(target)),weight_sum_max=str(max(cap)),
                unchanged_slope_max=str(max(slope)))
