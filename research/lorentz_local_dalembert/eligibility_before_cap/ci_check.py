"""CI: immutable evidence, controls, published gates, algebra and two A/B replays.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import importlib.util
import shutil
import tempfile
from pathlib import Path
from eb_common import HERE,read,encode,frozen

def local_module(name):
    spec=importlib.util.spec_from_file_location('eligibility_audit_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def main():
    frozen()
    for line in (HERE/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    controls=local_module('controls'); analyze=local_module('analyze'); verify=local_module('verify')
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory); shutil.copy2(HERE/'contract.json',temp/'contract.json')
        controls.HERE=temp; controls.main()
        assert encode(read(temp/'controls.json'))==encode(read(HERE/'controls.json'))
        (temp/'results').symlink_to(HERE/'results',target_is_directory=True)
        analyze.HERE=temp; analyze.main()
        assert encode(read(temp/'analysis.json'))==encode(read(HERE/'analysis.json'))
    verify.main(write=False)
    print('CI PASS: technical reproducibility; scientific gate statuses unchanged.')

if __name__=='__main__':main()
