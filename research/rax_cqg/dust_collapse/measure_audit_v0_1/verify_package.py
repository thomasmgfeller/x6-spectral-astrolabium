"""Check release integrity, frozen plan, and inherited Git blob identities."""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT = Path(__file__).resolve().parent
PLAN_SHA256 = 'fd9d00d4ce6ae7abd4d4b5b5588734e7220333a2ed1a26300688ad4f96411c15'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    require(manifest['schema'] == 'cst-dust-measure-audit-manifest-v0.1', 'Manifest schema')
    for name, entry in manifest['files'].items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts, 'Unsafe manifest path')
        data = (ROOT / name).read_bytes()
        require(len(data) == entry['size'], 'Size mismatch: ' + name)
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'SHA256 mismatch: ' + name)
    require(hashlib.sha256((ROOT / 'plan.json').read_bytes()).hexdigest() == PLAN_SHA256,
            'Frozen plan changed')
    require((ROOT / 'plan.sha256').read_text().split()[0] == PLAN_SHA256, 'Plan sidecar mismatch')
    provenance = json.loads((ROOT / 'provenance.json').read_text())
    require(provenance['source_main'] == '3177458a7f8545f845054e235cd3dcd7e829eff3',
            'Source revision changed')
    for name, entry in provenance['inputs'].items():
        data = (ROOT / name).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == entry['git_blob'], 'Inherited source mismatch: ' + name)
    gates = json.loads((ROOT / 'results/verification.json').read_text())['physical_gates']
    require(len(gates) == 8 and set(gates.values()) == {'HOLD'}, 'Physical claim boundary changed')
    result = {'status': 'PASS_PACKAGE_INTEGRITY', 'hashed_files': len(manifest['files']),
              'pinned_source_files': len(provenance['inputs']), 'frozen_plan': 'UNCHANGED',
              'physical_gates': gates,
              'limitation': 'Hashes establish internal consistency, not authorship or external replication.'}
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == '__main__':
    verify()
