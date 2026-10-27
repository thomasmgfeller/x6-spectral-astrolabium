"""Post-run descriptive diagnostics and an exportable scientific figure; no fits."""
import argparse
import json
from pathlib import Path
import numpy as np
from fields import rms
from scalar import HERE, volume

def main(metrics_only=False):
    from prepare_reference import prepare
    prepare()
    out=HERE/'results';doc=json.loads((out/'RESULTS.json').read_text())
    z=np.load(out/'metrics.npz');ref=np.load(out/'reference.npz')
    records=json.loads((out/'RUNS.json').read_text());clouds=np.load(out/'clouds.npz')
    rows=[]
    for row in doc['cells']:
        bias=np.array(row['operator_normalized_mean_bias_RMS_by_field'])
        sd=np.array(row['operator_normalized_sample_SD_RMS_by_field'])
        rmse=np.array(row['operator_normalized_RMSE_by_field'])
        if not np.allclose(rmse**2,bias**2+(15/16)*sd**2,atol=1e-10,rtol=1e-12):raise RuntimeError('bias variance identity failed')
        largest=int(np.argmax(rmse))
        rows.append({'nu':row['nu'],'epsilon':row['epsilon'],'largest_error_field':doc['field_order'][largest],
            'largest_field_RMSE':rmse[largest],'same_field_bias_RMS':bias[largest],
            'same_field_sample_SD_RMS':sd[largest],
            'ell_L0':float((row['nu']/volume(4))**(-.25)),
            'ell_k_L0':row['ell_k_L0'],'k8_ell_k':8*row['ell_k_L0']})
    source_difference=rms(ref['probes_fine']-ref['probes_coarse'])/rms(ref['probes_fine'])
    boundary=[]
    for d in [0,3]:
        recs=[r for r in records if r['density_index']==d and 'outer_metric_index' in r]
        for ei,e in enumerate([1,.25,.0625]):
            deltas=np.array([z['outer_operator'][r['outer_metric_index'],ei]-z['operator'][d,r['realization_index'],ei] for r in recs])
            denom=np.maximum(rms(z['exact_phi'][:21]),rms(z['exact_box'][:21]))
            boundary.append({'nu':[512,1024,2048,4096][d],'epsilon':e,'paired_runs':4,
                'maximum_field_normalized_RMS_change_inner':float(np.max(rms(deltas[:,:21].reshape(-1,10))/denom))})
    byprobe=[]
    for d,nu in enumerate([512,1024,2048,4096]):
        for ei,e in enumerate([1,.25,.0625]):
            for name,ids in [('inner',slice(0,21)),('detector',slice(21,28)),('boundary',slice(28,32))]:
                f,b=z['exact_phi'][ids],z['exact_box'][ids]
                denom=np.maximum(rms(f),rms(b));err=z['operator'][d,:,ei,ids]-b
                # Some groups have identically zero polynomial jets; do not divide by zero.
                good=denom>0;rr=rms(err.reshape(-1,10))
                byprobe.append({'nu':nu,'epsilon':e,'probe_group':name,
                    'absolute_RMSE_by_field':rr.tolist(),
                    'normalized_RMSE_by_field':[float(rr[j]/denom[j]) if good[j] else None for j in range(10)]})
    info={'status':'DESCRIPTIVE_DEVELOPMENT_DIAGNOSTICS','bias_variance_identity':'PASS',
        'largest_error_fields':rows,'fine_coarse_relative_RMS_by_mass':source_difference.tolist(),
        'paired_boundary_extension':boundary,'operator_by_probe_group':byprobe,
        'minimum_cell_worst_field_RMSE':min(r['maximum_field_RMSE'] for r in doc['cells']),
        'tolerance_screen_pass_cells':sum(r['draft_tolerance_screen']=='WITHIN_0.1' for r in doc['cells']),
        'outer_shell_empirical_mean_time':float(np.mean(np.concatenate([
            clouds[r['key']+'_outer'][np.abs(clouds[r['key']+'_outer'][:,0])+np.linalg.norm(clouds[r['key']+'_outer'][:,1:],axis=1)>=4,0]
            for r in records if 'outer_metric_index' in r])))}
    (out/'DIAGNOSTICS.json').write_text(json.dumps(info,indent=2,allow_nan=False)+'\n')
    if metrics_only:return
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
    for ei,e in enumerate([1,.25,.0625]):
        cells=[r for r in doc['cells'] if r['epsilon']==e];n=[r['nu'] for r in cells]
        color=['#d45b42','#397cb3','#279177'][ei]
        axes[0].plot(n,[r['maximum_field_RMSE'] for r in cells],'o-',label=f'epsilon = {e:g}',color=color)
        axes[1].plot(n,[max(r['manufactured_propagation_relative_RMSE_by_k']) for r in cells],'o-',color=color)
        axes[2].plot(n,[r['unit_history_response_max'] for r in cells],'o-',color=color)
    axes[0].axhline(.1,ls='--',color='#666666',label='draft tolerance 0.1')
    titles=['Operator: worst test-field RMSE','Propagation: worst manufactured wave','Unit-history response at probes']
    labels=['normalized RMS error','relative RMS error','maximum response magnitude']
    for ax,title,ylabel in zip(axes,titles,labels):
        ax.set(xscale='log',yscale='log',xlabel='expected points nu',ylabel=ylabel,title=title)
        ax.set_xticks([512,1024,2048,4096],labels=['512','1024','2048','4096'])
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(alpha=.18)
    axes[0].legend(fontsize=8,loc='lower right')
    fig.suptitle('CSPP scalar pilot: 16 independent clouds per density; descriptive results, HOLD',fontsize=13)
    fig.savefig(HERE/'scalar-pilot.png',dpi=160)
    fig.savefig(HERE/'scalar-pilot.svg')
    svg=HERE/'scalar-pilot.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--metrics-only',action='store_true')
    main(ap.parse_args().metrics_only)
