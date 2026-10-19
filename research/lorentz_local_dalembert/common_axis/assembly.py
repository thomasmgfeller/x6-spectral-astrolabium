"""Rebuild unchanged balanced64 caps around externally selected references."""
import copy
from axis_common import estimator,weighting

def rebuild(g,base,references,rho,cfg):
    out=copy.deepcopy(base)
    out.pop('support',None);out.pop('weights',None)
    if references['status']!='ok':
        out['status']=references['status'];return out
    sides=[]
    for old,ref,reverse in zip(base['sides'],references['sides'],[False,True]):
        reference=ref['reference'];selected=[];distances=[];diagnostics=[]
        for x in old['shell']:
            d,info=estimator.spatial_distance(g,reference,x,rho,cfg,reverse)
            distances.append(d);diagnostics.append(info)
            if d is not None and d<=cfg['radius_over_tau_m']*base['tau_m']:selected.append(x)
        sides.append(dict(reference=reference,shell=old['shell'],selected=selected,distances=distances,diagnostics=diagnostics))
    out['sides']=sides
    if min(len(side['selected']) for side in sides)<cfg['minimum_neighborhood_population']:
        out['status']='insufficient_neighborhood';return out
    out['status']='ok'
    times={x:base['tau_m'] for side in sides for x in side['selected']}
    return weighting.assemble(out,g.marks,cfg['coefficient_C'],times)
