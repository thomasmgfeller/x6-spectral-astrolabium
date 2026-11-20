"""Definitions and hash-pinned source loading for the independently selected prefix."""
from contextlib import contextmanager
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import os
import sys

HERE = Path(__file__).resolve().parent
SOURCE = 'CST_DUST_Praefix_1564_Neun_Richtungen_v0_1_Pruefpaket.zip'
SOURCE_HASH = '05968e2c6afeb263c66faa15255e1499b7cd6a90a6ff2b6510fd6b48cbc4c1c5'
TYPES = (623,662,718,726,751,760,764,767,5295,5307,26935)
DENSITIES = ('1/8','1/4')
REF_RADIUS = Fraction(1,60000)
TARGET_RADIUS = Fraction(1,50000)
for var in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[var] = '1'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def extract(path, expected, dest):
    if digest(path) != expected:
        raise ValueError('Unexpected input digest: '+path.name)
    with ZipFile(path) as z:
        z.extractall(dest)


@contextmanager
def source():
    with TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        nine, boundary_dir, rank, up = [tmp/p for p in ('nine','boundary','rank','up')]
        extract(HERE/SOURCE,SOURCE_HASH,nine)
        extract(nine/'CST_DUST_Randabbildung_1564_v0_1_Pruefpaket.zip',
                'ab2204236c27e8b804849d78889823927110e8fb41dabde3b8ab8e31018c325f',boundary_dir)
        extract(nine/'CST_DUST_Praefix_1564_Rangtest_v0_1.zip',
                '69447107966b781771b1bcdad6ae62875752b3bf103dc499a786a1002651cb44',rank)
        extract(boundary_dir/'CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip',
                '4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e',up)
        study = up/'prefix_1564_selection_v0_1'
        sys.path[:0]=list(map(str,(nine,boundary_dir,rank,study,study/'inputs')))
        try:
            yield study
        finally:
            del sys.path[:5]


def geometry(end_type,boundary):
    code=sum(1<<(6*i+j) for k,(i,j) in enumerate(combinations(range(6),2)) if end_type & (1<<k))
    _,coefficients,gravity = boundary.geometry_for(code,6)
    return coefficients,gravity


def encode(z):
    return [str(Fraction.from_float(float(x))) for x in (z.real,z.imag)]


def write_fresh(path,value):
    with path.open('x',encoding='utf-8') as stream:
        stream.write(json.dumps(value,indent=2,allow_nan=False)+'\n')
