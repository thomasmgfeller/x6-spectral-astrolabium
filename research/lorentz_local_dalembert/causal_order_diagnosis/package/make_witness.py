"""Export the first archived B0 violated pair, a six-node diagnostic witness."""
import gzip,json
from diagnose import SRC,OUT,save,matrices
violated=json.loads((OUT/'violated_pairs.json').read_text())[0]
i=violated['index'];row=json.loads(gzip.decompress((SRC/f'results/cloud-{i:02d}.json.gz').read_bytes()))
t=json.loads((SRC/f'results/truth/cloud-{i:02d}.json').read_text())
pk=row['selection']['fourth']['packet'];ids=t['ids'];nodes=pk['landmarks']+[ids[violated['i']],ids[violated['j']]]
rep=row['replicates'][0];needed=set(nodes);measurements=[]
for k,(a,b) in enumerate(pk['pairs']):
    if a in needed and b in needed:
        measurements.append(dict(pair=[a,b],count=rep['observed']['counts'][k],q=rep['inference']['q'][k]))
assert len(measurements)==14
w=dict(scope='Post-hoc first mismatched B0 pair in index order; no population claim',
       original_cloud_index=i,replicate=0,rho=32768,scale=pk['scale'],landmarks=pk['landmarks'],
       support_pair=nodes[4:],nodes=nodes,truth_coordinates=[t['points'][ids.index(x)] for x in nodes],
       measurements=measurements,recorded_true_order=violated['true_order'],recorded_estimated_order=violated['estimated_order'],
       expected_true_s2=violated['true_s2'],expected_reconstructed_s2=violated['estimated_s2'])
save('minimal_counterexample.json',w)
