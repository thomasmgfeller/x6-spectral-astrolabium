"""Export the registered six-bin laws and the alternative two-bin sign measurement."""
import csv
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent
joint=json.loads((BASE/'joint.json').read_text())
sensitivity=json.loads((BASE/'sensitivity.json').read_text())
with (BASE/'distribution.csv').open('w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['tagged_M','initial_density_center','one_edge_A_over_B','chain_extension','p_lt_minus1','minus1_le_p_lt_minus0.25','minus0.25_le_p_lt0','p_eq_0','0_lt_p_lt_0.25','0.25_le_p_lt_1','p_ge_1','positive_total_after_six_bin_register','positive_in_sign_only_register'])
    for k,ref in joint['rows'].items():
        m,r=k.split('/')
        for label in ('1:1','1:3'):
            d=ref[label];v=d['bin_probabilities']
            w.writerow([m,r,label,'primary',*v[:3],0,*v[3:],sum(v[3:]),d['positive_sign_record']])
        for tag,d in sensitivity.items():
            row=d['rows'][k];v=row['bins']
            w.writerow([m,r,'1:1',tag,*v[:3],0,*v[3:],sum(v[3:]),row['sign_positive']])
