"""Local clock-pulse and central radar instrument. No density profile or reference boundary is an input."""
from fractions import Fraction as F

TICK_SCALE=10**10


def read(records,length,cut,inner,outer):
    # Values in integer units of 8*TICK_SCALE times the local density.
    bounds={}
    for send,receive,a,b,c,d in records:
        if send+receive!=2*cut or receive<send or (receive-send)%24:
            return {'state':'INVALID_RADAR'}
        j=(receive-send)//24
        if j in bounds:return {'state':'DUPLICATE'}
        center=a-b-c+d
        if center < -4:return {'state':'INVALID_PULSE'}
        bounds[j]=max(0,center-4),center+4
    grid=list(range(4,length-3))
    if set(bounds)!=set(grid):return {'state':'MISSING_EXPOSURE'}
    def mean(stations):
        return tuple(F(sum(bounds[j][k] for j in stations),len(stations)) for k in (0,1))
    il,ih=mean(inner);ol,oh=mean(outer)
    if il<=0:return {'state':'NO_POSITIVE_REFERENCE'}
    ratios=(ol/ih,oh/il)
    res={'state':'DEPLETED' if 100*oh<il else 'NOT_DEPLETED' if 100*ol>ih else 'UNRESOLVED',
         'outer_over_inner':list(map(str,ratios)),
         'inner_mean':[str(v/(8*TICK_SCALE)) for v in (il,ih)],
         'outer_mean':[str(v/(8*TICK_SCALE)) for v in (ol,oh)]}
    above=[j for j in grid if 100*bounds[j][0]>ih]
    below=[j for j in grid if 100*bounds[j][1]<il]
    if above and below and max(above)<min(below) and above==grid[:len(above)] and below==grid[-len(below):]:
        inside,outside=max(above),min(below)
        res['threshold_station_bracket']=[inside,outside]
        res['radar_half_delay_ticks']=[12*inside,12*outside]
    if res['state']=='DEPLETED':
        # Extra uniform density uncertainty beyond encoded quantization permitted by the ROI decision.
        res['additional_density_error_ceiling']=str((il-100*oh)/(101*8*TICK_SCALE))
    return res
