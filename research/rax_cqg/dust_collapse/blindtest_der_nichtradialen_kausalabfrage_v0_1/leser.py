"""Lokale Blindwertung. Eingabe enthält ausschliesslich Kennung und Kausalantworten."""
import json
import sys
from pathlib import Path

def classify(hard, easy):
    answers={'JA','NEIN','UNBESTIMMT'}
    if hard not in answers or easy not in answers:
        raise ValueError('Unbekannte Kausalantwort')
    if hard=='JA' and easy=='NEIN':
        raise ValueError('Verletzte Ordnung der Fehlerquader')
    return hard if hard==easy and hard!='UNBESTIMMT' else 'OFFEN'

def read(frames):
    out={}
    for row in frames:
        if set(row)!={'id','antworten'} or row['id'] in out:
            raise ValueError('Ungültige Instrumentdaten')
        if set(row['antworten'])!={'0','1','4','8'}:
            raise ValueError('Fehlende Fehlerstufe')
        out[row['id']]={k:classify(*v) for k,v in row['antworten'].items()}
    return out

if __name__=='__main__':
    data=read(json.loads(Path(sys.argv[1]).read_bytes()))
    Path(sys.argv[2]).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
