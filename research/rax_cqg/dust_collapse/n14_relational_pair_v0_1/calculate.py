"""Reproduce the exact counting certificates, finite action sums and cut tests."""
import json
import os
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):
    os.environ[name] = '1'
from fractions import Fraction as Q
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import sympy as sp
import counting
from clock import BASE, MASKS, CUTS, native, packet, cartesian, ideals
from ideals import exact_count, rectangles, reference_transport
from record import occupancy_record

TOL = 5e-9
GRIDS = ((32,6),(48,8),(64,10))


def enc(z):
    return np.stack([z.real,z.imag],axis=-1).tolist()


def dec(z):
    a = np.asarray(z)
    return a[...,0]+1j*a[...,1]


def distance(a,b):
    return float(np.max(abs(a-b)))


def gram(amp, form):
    return amp.conj()[..., :,None]*form*amp[...,None,:]


def small_check(lib):
    worst = 0.
    for mask in MASKS:
        for cuts in ((),(0.,),(.25,),CUTS):
            fast = packet(mask,5,3,cuts,lib)
            slow = packet(mask,5,3,cuts,lib,cartesian)
            worst = max(worst,distance(fast,slow))
        for threshold in CUTS:
            for index,(_,members,frontier) in enumerate(ideals(mask)):
                box = {j:(-1.5,threshold) for j in members}
                box.update({j:(threshold,1.5) for j in frontier})
                fast = packet(mask,4,3,(),lib,bounds=box)
                slow = packet(mask,4,3,(),lib,cartesian,bounds=box,ideal_cut=threshold)
                worst = max(worst,distance(fast[:,0],slow[:,index]))
                assert np.max(abs(np.delete(slow,index,axis=1))) == 0
    assert worst < 2e-14
    return worst


def run_grid(n,m,lib):
    # Axes: density, geometry, class of the first release.
    joint = np.stack([packet(mask,n,m,CUTS,lib) for mask in MASKS],axis=1)
    direct = np.column_stack([packet(mask,n,m,(),lib)[:,0] for mask in MASKS])
    single,all_ideals = {}, {}
    by_cut = []
    for s in CUTS:
        single[s] = np.stack([packet(mask,n,m,(s,),lib) for mask in MASKS],axis=1)
        for mask in MASKS:
            all_ideals[mask,s] = rectangles(mask,n,m,s,lib)
        by_cut.append(np.column_stack([all_ideals[mask,s].sum(axis=1) for mask in MASKS]))
    return direct,joint,single,all_ideals,by_cut


def compare_grids(coarse,fine):
    return max(distance(a,b) for a,b in
               [(coarse[0],fine[0]),(coarse[1],fine[1])]
               + [(coarse[k][i],fine[k][i]) for k in (2,3) for i in fine[k]])


def run():
    counts = counting.run()
    hist_a,ref_a = exact_count(MASKS[0])
    hist_b,ref_b = exact_count(MASKS[1])
    p=sp.Symbol('p')
    delta = [sp.factor(sum((a-b)*p**k*(1-p)**(6-k)
                           for k,(a,b) in enumerate(zip(ra,rb)))) for ra,rb in zip(hist_a,hist_b)]
    assert delta[:2] == [0,0] and sp.expand(delta[2]-p**3*(1-p)**2)==0
    assert Q(ref_a['0.0'][2])-Q(ref_b['0.0'][2])==Q(1,32)
    sector = json.loads((BASE/'inputs/sector.json').read_text())
    old = json.loads((BASE/'inputs/response.json').read_text())
    assert sector['order'] == old['order'] == list(MASKS)
    scalar = dec(sector['gram_scalar'])
    bins = dec(sector['pointer_effects_scalar'])
    assert distance(bins.sum(axis=0),scalar)<1e-14
    archive = old['production_grids'][-1]
    inherited = np.column_stack([dec(x['lobes']).sum(axis=1)/np.sqrt(2) for x in archive['packets']])
    assert np.min(abs(inherited))>.005
    with TemporaryDirectory() as tmp:
        lib = native(tmp)
        small = small_check(lib)
        rows,changes,last = [],[],None
        for n,m in GRIDS:
            data = run_grid(n,m,lib)
            direct,joint,single,all_ideals,by_cut = data
            alternatives = {'uncut':direct, 'both_first_release':joint.sum(axis=-1)}
            split_gap = max(distance(single[0.][...,0],joint[...,0]),
                            distance(single[0.][...,1],joint[...,1:].sum(axis=-1)),
                            distance(single[.25][...,0],joint[...,:2].sum(axis=-1)),
                            distance(single[.25][...,1],joint[...,2]))
            matched = []
            for k,s in enumerate(CUTS):
                alternatives['ideal_'+str(s)]=by_cut[k]
                empty = np.column_stack([all_ideals[mask,s][:,0] for mask in MASKS])
                matched.append(distance(empty,single[s][...,1]))
            amp_gap = max(distance(z,inherited) for z in alternatives.values())
            gram_gap = max(distance(gram(z,scalar),gram(inherited,scalar)) for z in alternatives.values())
            bin_gap = max(distance(gram(z,form),dec(archive['coherent_effects'])[:,idx])
                          for z in alternatives.values() for idx,form in enumerate(bins))
            rows.append({'grid':[n,m], 'max_complex_amplitude_error_vs_uncut_archive':amp_gap,
                         'max_complex_endpoint_gram_error_vs_uncut_archive':gram_gap,
                         'max_complex_bin_matrix_error_vs_uncut_archive':bin_gap,
                         'max_single_vs_two_cut_class_error':split_gap,
                         'max_empty_vs_full_ideal_partition_error':max(matched)})
            if last is not None:
                changes.append(compare_grids(last,data))
            last=data
            print(f'grid {n} x {m}, archive amplitude residual {amp_gap:.3g}',flush=True)
    assert max(changes[-1],amp_gap,gram_gap,bin_gap,split_gap,*matched)<TOL
    gram_direct = gram(direct,scalar)
    assert np.min(np.linalg.eigvalsh(gram_direct))>0
    ratios = direct[:,1]/direct[:,0]
    probes = {}
    for a,b in ((1,1),(1,3)):
        weights=np.array([a,b])/(a+b)
        success=(weights@gram_direct@weights).real
        ref=archive['pair_preparations'][1 if b==1 else 2]
        assert distance(success,1-np.asarray(ref)[:,3])<1e-13
        probes[f'{a}:{b}']={'amplitude_ratio_B_over_A':enc((b/a)*ratios),
                              'inclusive_q7_success':success.tolist()}
    rows_ideal = {}
    for s in CUTS:
        branches={}
        for mask in MASKS:
            cases=ideals(mask)
            amp=all_ideals[mask,s]
            branches[str(mask)]={'ideal_codes':[i for i,_,_ in cases],'amplitudes':enc(amp)}
        occ2=np.column_stack([all_ideals[mask,s][:,[k for k,(_,d,_) in enumerate(ideals(mask)) if len(d)==2]].sum(axis=1)
                              for mask in MASKS])
        rows_ideal[str(s)]={'branches':branches,'occupancy_two_amplitudes':enc(occ2),
                            'binary_count_record':occupancy_record(by_cut[CUTS.index(s)],occ2,scalar)}
    return {'contract':'contract.json','exact_counting':counts, 'reference_occupancy':{
                'probabilities_by_number_released':{'1790':ref_a,'5374':ref_b},
                'reference_transport':{str(mask):reference_transport(mask) for mask in MASKS},
                'difference_polynomials_A_minus_B':[str(x) for x in delta]},
            'small_cartesian_max_absolute_error':small,'refinements':rows,
            'max_change_in_any_branch_or_class_between_successive_grids':changes,
            'clock':{'densities':['1/8','1/4'],'branch_order':list(MASKS),'direct_amplitudes':enc(direct),
                     'endpoint_gram_by_density':enc(gram_direct),'first_release_classes':['by 0','(0,1/4]','above 1/4'],
                     'first_release_class_amplitudes':enc(joint),'full_ideals':rows_ideal,
                     'positive_coefficient_witnesses_within_selected_pair':probes}}


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    args.output.write_text(json.dumps(run(),indent=2,allow_nan=False)+'\n')
