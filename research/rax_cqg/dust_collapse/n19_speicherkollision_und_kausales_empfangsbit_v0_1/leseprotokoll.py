"""Emit one receiver bit, or consume it at site 7 from a separate local input."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from empfangsbit import CAL,receiver_bit,late_code,classify,valid


def checked(record):
    if record.get('kind') not in ('synthetic','measurement_records'):
        raise ValueError('unknown record kind')
    if not all(isinstance(record.get(k),str) and record[k].strip() for k in ('shot','device','baseline_id')):
        raise ValueError('missing association')
    if not valid(record.get('baseline_code')) or not 0<=F(record['baseline_error_q'])<=CAL:
        raise ValueError('missing or imprecise paired null calibration')
    if record.get('usable') is not True or record.get('saturated') is not False:
        raise ValueError('unusable reading')
    return {k:record[k] for k in ('kind','shot','device','baseline_id')}


def emit(record):
    packet=checked(record)
    bit=receiver_bit(record.get('receiver_clock'),record['baseline_code'])
    if bit is None:raise ValueError('invalid receiver digit')
    return {**packet,'bit':bit}


def read(record,packet):
    fields=checked(record)
    if not isinstance(packet,dict) or any(packet.get(k)!=v for k,v in fields.items()):
        raise ValueError('absent or mismatched receiver packet')
    late=late_code(record.get('clock7'),record.get('pointer7_t'),record.get('initial_t'),record['baseline_code'])
    j=classify(packet.get('bit'),late)
    return {'kind':record['kind'],'source_label':str(j) if j is not None else None,
            'status':'MODEL_CLASSIFICATION' if j is not None else 'UNRESOLVED','physical_P3':'60 NOT_RUN'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('senden','lesen'))
    p.add_argument('record',type=Path)
    p.add_argument('packet',nargs='?',type=Path)
    a=p.parse_args()
    try:
        record=json.loads(a.record.read_text())
        if a.mode=='senden':
            if a.packet:p.error('senden takes only a receiver record')
            result=emit(record)
        else:
            if not a.packet:p.error('lesen requires a receiver packet')
            result=read(record,json.loads(a.packet.read_text()))
    except (ValueError,TypeError,KeyError,ZeroDivisionError) as exc:
        p.exit(2,'UNRESOLVED: '+str(exc)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
