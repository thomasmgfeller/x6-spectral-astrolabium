"""Descriptive report products; no fitted scaling exponent or confidence claim."""
import argparse
import json
import numpy as np
from common import HERE,write,exact_box

def main(metrics_only=False):
    out=HERE/'results';r=json.loads((out/'RESULTS.json').read_text())
    meta=json.loads((out/'MEAN.json').read_text());m=np.load(out/'mean.npz')['values'][:,-1]
    noise=[]
    for ell in [1,1.5,2]:
        cells=[x for x in r['cells'] if x['H']==8 and x['ell_k']==ell]
        noise.append({'ell_k':ell,'nu':[x['nu_equivalent_Omega4'] for x in cells],
            'worst_field_relative_SD':[max(x['relative_sample_SD']) for x in cells],
            'worst_field_relative_RMSE':[max(x['relative_RMSE']) for x in cells],
            'ratio_worst_SD_lowest_to_highest_density':max(cells[0]['relative_sample_SD'])/max(cells[-1]['relative_sample_SD']),
            'bias_floor_at_H8':max(cells[0]['relative_exact_mean_bias'])})
    mean=[]
    for i,row in enumerate(meta['rows']):
        mean.append({**row,'maximum_field_relative_mean_bias':float(np.max(np.abs(m[i]-exact_box(row['L']))/np.abs(exact_box(row['L']))))})
    source=r['source_reference'];maxnew=max(source['new_Fourier_relative_RMS_vs_Green_by_resolution'][-1])
    report={'status':'DESCRIPTIVE_CALIBRATION_NOT_G1','total_new_points':sum(x['N'] for x in json.loads((out/'RUNS.json').read_text())),
        'noise':noise,'mean_scan':mean,'quadrature_hold_count':sum(x['resolution_screen']=='QUADRATURE_HOLD' for x in meta['rows']),
        'best_cell_worst_field_RMSE':min(max(x['relative_RMSE']) for x in r['cells']),
        'source_max_relative_RMS_finest_Fourier':maxnew,'source_0_001_diagnostic_goal_met':maxnew<=.001,
        'old_finest_vs_new_finest_error_ratio_by_mass':(np.array(source['old_Fourier_relative_RMS_vs_Green_by_resolution'][-1])/np.array(source['new_Fourier_relative_RMS_vs_Green_by_resolution'][-1])).tolist(),
        'nonclaims':['no new G1 test substitution','no rigorously bounded reference remainder','no confirmed variance exponent']}
    write(out/'DIAGNOSTICS.json',report)
    if metrics_only:return
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    plt.rcParams.update({'font.size':9,'axes.spines.right':False,'axes.spines.top':False})
    fig,ax=plt.subplots(1,3,figsize=(13.4,4.2),layout='constrained')
    colors=['#c55b41','#397db1','#238974']
    for color,row in zip(colors,noise):
        ax[0].loglog(row['nu'],row['worst_field_relative_SD'],'o-',color=color,label=f'ell_k = {row["ell_k"]:g}')
    ax[0].set(xlabel='expected points in D8',ylabel='largest relative sample SD',title='Fluctuation at fixed nonlocality')
    ax[0].set_xticks([1024,4096,16384],labels=['1024','4096','16384']);ax[0].xaxis.set_minor_formatter(NullFormatter());ax[0].legend()
    selected=[x for x in mean if x['L']==2 and x['H']==64]
    ax[1].loglog([x['ell_k'] for x in selected],[x['maximum_field_relative_mean_bias'] for x in selected],'o-',color='#6655a8')
    ax[1].axhline(.1,color='#777777',ls='--',label='0.1 diagnostic line')
    ax[1].set(xlabel='nonlocality length ell_k / L0',ylabel='largest relative mean bias',title='Mean response only: L=2, H=64')
    ax[1].set_xticks([.125,.25,.5,1,2],labels=['.125','.25','.5','1','2']);ax[1].xaxis.set_minor_formatter(NullFormatter());ax[1].legend(loc='lower right')
    for j,color in enumerate(colors):
        ax[2].loglog([64,128,256],[x[j] for x in source['new_Fourier_relative_RMS_vs_Green_by_resolution']],'o-',color=color,label=f'm = {j}')
    ax[2].axhline(.001,color='#777777',ls='--',label='planned agreement goal')
    ax[2].set(xlabel='Fourier grid N, box length 8',ylabel='relative RMS vs real-space reference',title='Source reference at 28 fixed probes')
    ax[2].set_xticks([64,128,256],labels=['64','128','256']);ax[2].xaxis.set_minor_formatter(NullFormatter());ax[2].legend(loc='lower left',fontsize=8)
    for a in ax:a.grid(alpha=.2)
    fig.suptitle('CSPP v0.2: noise, mean bias and source-reference error separated; overall HOLD',fontsize=12)
    fig.savefig(HERE/'calibration.png',dpi=160)
    fig.savefig(HERE/'calibration.svg')
    svg=HERE/'calibration.svg';svg.write_text('\n'.join(x.rstrip() for x in svg.read_text().splitlines())+'\n')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--metrics-only',action='store_true');a=ap.parse_args();main(a.metrics_only)
