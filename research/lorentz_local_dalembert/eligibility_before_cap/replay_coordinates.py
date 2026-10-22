"""Portable numeric replay backed by exact archived coordinate-byte fixtures.
SPDX-License-Identifier: Apache-2.0
"""
import gzip,hashlib
import numpy as np
from eb_common import HERE
TOLERANCE=2.0**-50  # absolute simulator-coordinate units; no count/gate tolerance

def compare_arrays(actual,reference):
    assert actual.dtype==reference.dtype==np.dtype('<f8')
    assert actual.shape==reference.shape and actual.ndim==2 and actual.shape[1]==3
    assert np.isfinite(actual).all() and np.isfinite(reference).all()
    delta=float(np.max(np.abs(actual-reference)))
    assert delta<=TOLERANCE,('coordinate replay differs beyond roundoff',delta,TOLERANCE)
    return delta

def invoke(fn,args,expected_hash):
    import simulation
    original_digest=simulation.digest;captured=[]
    def capture(a):
        if a.dtype==np.float64 and a.ndim==2 and a.shape[1]==3:captured.append(a)
        return original_digest(a)
    simulation.digest=capture
    try:result=fn(*args)
    finally:simulation.digest=original_digest
    assert len(captured)==1
    array=captured[0];record=result[0] if isinstance(result,tuple) else result
    actual_hash=original_digest(array)
    assert record['coordinates_sha256']==actual_hash
    raw=gzip.decompress((HERE/'coordinate_fixtures'/f'{expected_hash}.bin.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==expected_hash,'reference bytes changed'
    reference=np.frombuffer(raw,dtype='<f8').reshape(-1,3)
    delta=compare_arrays(array,reference)
    if actual_hash!=expected_hash:
        print('Coordinate numeric replay:',dict(reference_sha256=expected_hash,actual_sha256=actual_hash,
          maximum_absolute_difference=delta,tolerance=TOLERANCE,changed_components=int(np.count_nonzero(array!=reference))))
    # Only normalize the provenance field AFTER complete byte-reference and
    # coordinate comparison. Callers still require exact relation hashes,
    # interval bit hashes, all counts/overlaps and all scientific decisions.
    normalized={**record,'coordinates_sha256':expected_hash}
    return (normalized,result[1]) if isinstance(result,tuple) else normalized

def selection_cloud(seed,contract,expected_hash):
    import simulation
    return invoke(simulation.selection_cloud,(seed,contract),expected_hash)

def counting_cloud(private,packet,seed,replicate,contract,expected_hash):
    import simulation
    return invoke(simulation.counting_cloud,(private,packet,seed,replicate,contract),expected_hash)

def controls():
    reference=np.array([[0.,.25,-.5]],dtype='<f8')
    compare_arrays(reference+TOLERANCE/2,reference)
    for bad in [reference+2*TOLERANCE,np.array([[float('nan'),.25,-.5]]),reference.astype(np.float32),reference[:,:2]]:
        try:compare_arrays(bad,reference)
        except AssertionError:continue
        raise AssertionError('invalid coordinate replay accepted')
