#!/usr/bin/env python3
"""Recover JSON serialization only; do not regenerate any sample or change tests.

The frozen runner completed both arms but json.dumps rejected numpy.bool_.
Retain that runner unchanged and convert NumPy scalar values only here.
"""
import json, platform, subprocess
from datetime import datetime, timezone
import numpy as np
import scipy
from run_control import HERE, ROOT, digest, analyze

def main():
    out=HERE/'results/control';q=json.loads((HERE/'protocol.json').read_text())
    freeze='cfcea64a376d66f080130e29ecc04a0fe8d05c07'
    names=['protocol.json','run_control.py','trace.cjs','diagnose.py']
    for name in names:
        data=subprocess.check_output(['git','show',f'{freeze}:{(HERE/name).relative_to(ROOT)}'],cwd=ROOT)
        assert data==(HERE/name).read_bytes()
    before={p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file()}
    assert len(list(out.glob('*.bin.gz')))==64
    report=analyze(out,q)
    report['provenance']=dict(base_commit=q['base_commit'],freeze_commit=freeze,protocol_sha256=digest(HERE/'protocol.json'),
        source_sha256={name:digest(HERE/name) for name in names},core_sha256=digest(HERE.parent/'core.js'),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,node=subprocess.check_output(['node','--version'],text=True).strip()),
        public_preregistration_required=True)
    assert all(digest(out/name)==h for name,h in before.items())
    receipt=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),stage='POST_GENERATION_JSON_SERIALIZATION_RECOVERY',
        original_error='TypeError: Object of type bool is not JSON serializable (numpy.bool_)',
        completed_before_error=dict(arms=2,batches=64,points=4194304),
        action='Re-evaluate unchanged frozen analysis on preserved traces; JSON conversion np.generic.item only. No regenerated samples, seed changes, threshold changes, or discarded batches.',
        input_sha256=before,recovery_script_sha256=digest(HERE/'finalize.py'))
    report['serialization_recovery']=receipt
    normalize=lambda x:x.item() if isinstance(x,np.generic) else (_ for _ in ()).throw(TypeError(type(x).__name__))
    (out/'control_report.json').write_text(json.dumps(report,indent=2,default=normalize,allow_nan=False)+'\n')
    (out/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))
    print(json.dumps(dict(status=report['status'],arms={k:{f:a[f] for f in ['n','pooled_reconstructed','batch_rejections_at_005','batch_rejection_upper_tail_p','max_transform_error','historical_location_probe']} for k,a in report['arms'].items()}),indent=2,default=normalize))
if __name__=='__main__':main()
