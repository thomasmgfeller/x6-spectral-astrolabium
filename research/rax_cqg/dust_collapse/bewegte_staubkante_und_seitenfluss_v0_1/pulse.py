"""Four-arm acquisition and signed cut/face readout on three observed sections."""
from fractions import Fraction as F
import sys


def edge_sets(n,j,stencil):
    # First form the full exposure. Each recorded edge is reused by both routes.
    routes = {route: {'Q':{}, 'F':{}} for route in ('receiver','emitter')}
    for d,s,_ in stencil:
        for route,columns in routes.items():
            emitter = j-s if route=='receiver' else j
            for v in range(n+1,n+d+1):
                columns['Q'][(v-d,emitter,v,emitter+s)] = 1
            first, last = sorted((j,j-s))
            for x in range(first+1,last+1):
                t = n if route=='receiver' else n-d
                columns['F'][(t,x,t+d,x+s)] = 1 if s>0 else -1
    return routes


def acquire(source,r,root,stencil):
    # Use the original acquisition code and its integer rounding convention.
    sys.path.insert(0,str(source))
    import dynamik
    import strom
    w = dynamik.weight_fn('profile',3072,r,root)
    frames = []
    for n,j in ((38400,2547),(46080,2547),(46080,2151)):
        routes = edge_sets(n,j,stencil)
        keys = set().union(*(group for route in routes.values() for group in route.values()))
        data = [strom.edge_record(w,3072,t,x,v-t,y-x) for t,x,v,y in sorted(keys)]
        frames.append({'tick':n,'station':j,'edges':data})
    return frames


def decode(frame,stencil):
    n,j = frame['tick'], frame['station']
    routes = edge_sets(n,j,stencil)
    required = set().union(*(group for route in routes.values() for group in route.values()))
    measured = {}
    for t,x,v,y,a,b,c,d in frame['edges']:
        key = (t,x,v,y)
        if key in measured:
            raise ValueError('Doppelte Kante')
        charge = -(v-t)*(a-b-c+d)
        error = 4*(v-t)
        measured[key] = charge-error,charge+error
    if measured.keys() != required:
        raise ValueError('Unvollständige Kantenaufnahme')
    result = {}
    for name,cols in routes.items():
        obs = {}
        for kind,weights in cols.items():
            low = high = 0
            for key,sign in weights.items():
                a,b = measured[key]
                low += a if sign==1 else -b
                high += b if sign==1 else -a
            obs[kind] = F(low,8*10**10), F(high,8*10**10)
        assert obs['Q'][0] > 0 and obs['F'][1] < 0
        obs['F_over_Q'] = obs['F'][0]/obs['Q'][0],obs['F'][1]/obs['Q'][1]
        result[name] = obs
    return result


def verify(frames,stencil,alloc):
    result = []
    for frame in frames:
        row = {'tick':frame['tick'],'station':frame['station'],'four_arm_records':len(frame['edges'])}
        for route,obs in decode(frame,stencil).items():
            a,b = obs['F_over_Q']
            expected = list(map(F,alloc[route]['fixed_face_flux_per_local_cell_charge']))
            assert a <= expected[0] <= expected[1] <= b
            row[route] = {k:list(map(str,v)) for k,v in obs.items()}
        result.append(row)
    for damaged in (frames[0]['edges'][:-1], frames[0]['edges']+frames[0]['edges'][:1]):
        try:
            decode({**frames[0], 'edges':damaged},stencil)
        except ValueError:
            continue
        raise AssertionError('Fehlende oder verdoppelte Aufnahme wurde akzeptiert.')
    return result
