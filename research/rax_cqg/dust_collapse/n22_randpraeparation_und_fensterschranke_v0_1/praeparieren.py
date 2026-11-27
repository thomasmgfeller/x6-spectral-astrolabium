"""Reconstruct all simultaneous preparation cells using the pinned N21 model."""
import argparse
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
from randpraeparation import compute


def main():
    p=argparse.ArgumentParser()
    p.add_argument('archive',type=Path)
    p.add_argument('partitions',type=int)
    p.add_argument('output',type=Path)
    args=p.parse_args()
    assert __debug__ and args.partitions>0
    assert sha256(args.archive.read_bytes()).hexdigest()=='3b5ab2685aa41d00467c36be43832f8f16b82628536946e9c52d480c7929e06a'
    with TemporaryDirectory() as td,ZipFile(args.archive) as z:
        with ZipFile(BytesIO(z.read('basis/Ankerpaket.zip'))) as a:
            a.extractall(td)
        sys.path.insert(0,str(Path(td)/'basis'))
        from quellenpaket import model
        with model() as (_,__,previous,early):
            result=compute(previous,early,args.partitions)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
