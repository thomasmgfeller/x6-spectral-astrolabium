"""Independent enumeration, known controls, and replay of the cited predecessor certificates."""
from fractions import Fraction as Q
import csv
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
from shutil import copyfile
from subprocess import run,check_output
import json
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from ordnungen import ROOT,POS,EMPTY,LOW,HIGH,as_relation,closures,compatible,inputs,SOURCE
from pruefen import anchored,tsv
from zeugenvergleich import controls

def independent_order(r):
    # Branch in topological order. An ideal may add a point only after all its predecessors.
    topo=sorted(range(22),key=lambda j:sum((i,j) in r for i in range(22)))
    ideals=[frozenset()]
    for j in topo:
        pred={i for i in topo if (i,j) in r}
        ideals += [p|{j} for p in ideals if pred<=p]
    return {tuple(sorted(p)) for p in ideals}

def terminal(pair,pasts,rel):
    rows=[];counts={}
    for side in ('heavy','light'):
        case=pair[side];clocks=[[Q(k) for k in v] for v in case['normalized_clocks']]
        positive=set(range(22))-set(EMPTY)
        assert [q for q in sorted(positive) if LOW<=clocks[q][0]<=clocks[q][1]<=HIGH]==[18,19]
        assert {(pair_[0],pair_[1]) for pair_ in ((n,e) for n in (18,19) for e in (17,20))
                if anchored(rel,tuple(i for i in range(22) if (i,pair_[1]) in rel),
                            tuple(i for i in range(22) if (pair_[1],i) in rel),pair_[0])}=={(19,17),(19,20)}
        counts[side]={}
        for p in pasts:
            lo=max([LOW,*[clocks[i][1] for i in p]])
            if lo<HIGH:
                z=(lo+HIGH)/2
                assert LOW<=z<=HIGH and all(clocks[i][1]<z for i in p)
                state="ZEUGE"
            elif set(p)&{7,8,9,10}:z=None;state="KRAGEN_AUSSCHLUSS"
            else:z=None;state="OFFEN"
            counts[side][state]=counts[side].get(state,0)+1
            ext=as_relation(rel,p,())
            assert not any(a==22 for a,b in ext)
            assert {(a,b) for a,b in ext if a<22 and b<22}==rel
            assert all(not (a,22) in ext or not (22,b) in ext for a,b in rel)
            rows.append([','.join(map(str,p)) or '∅',side,state,str(z) if z is not None else '–','AUSGESCHLOSSEN'])
    return counts,tsv(['Vergangenheit','Praeparation','Sonde_und_Materie','x22_Zeuge','Verankerter_Kontakt'],rows)

def checked_archive(zipobj,work):
    zipobj.extractall(work)
    run(['sha256sum','--quiet','-c','SHA256SUMS'],cwd=work,check=True)

def main(write):
    pair,_,_=inputs()
    r=set(map(tuple,pair['relation']))
    fs,ps=closures(r)
    lhs=independent_order(r);rev=independent_order({(j,i) for i,j in r})
    assert lhs==set(ps) and rev-{()}==set(fs)
    pairs={(p,f) for p in lhs for f in rev if not set(p)&set(f)
           and all((i,j) in r for i in p for j in f)}
    assert len(pairs)==2657 and sum(bool(f) for p,f in pairs)==2320
    assert sum(compatible(r,p,f) for p in ps for f in fs)==2320
    counts,terminal_tsv=terminal(pair,ps,r)
    assert all(c=={'ZEUGE':279,'KRAGEN_AUSSCHLUSS':8,'OFFEN':50} for c in counts.values())
    pre=ROOT/'basis/N22_Vergleichspaar.zip'
    assert sha256(pre.read_bytes()).hexdigest()=='8ba8619785a8baed758c7cc425e8f79217c076bff7b3adbe6844b7db7f4a104c'
    with TemporaryDirectory() as d:
        base=Path(d);n22=base/'n22';n23=base/'n23';parent=base/'parent'
        with ZipFile(pre) as z:
            assert json.loads(z.read('Vergleichspaar.json'))==pair
            checked_archive(z,n22)
        run([sys.executable,'-B','pruefen.py'],cwd=n22,check=True)
        with ZipFile(ROOT/'basis/Fensterabstand.zip') as z:
            checked_archive(z,parent)
            with ZipFile(BytesIO(z.read('basis/Innenfelder.zip'))) as prev:
                checked_archive(prev,n23)
                controls(pair,r,json.loads(prev.read("Ergebnisse.json"))["solutions"])
        for name in ('pruefen.py','gegenprobe.py'):
            run([sys.executable,'-B',name],cwd=parent,check=True)
        copyfile(ROOT/'kontrollfelder.py',n23/'kontrollfelder.py')
        fields=check_output([sys.executable,'-B','kontrollfelder.py',str(ROOT/'Kontrollstartwerte.json')],cwd=n23)
    with (ROOT/'Fallregister.tsv').open(encoding='utf-8') as fp:
        combined=list(csv.reader(fp,delimiter='\t'))
    for row in csv.DictReader(StringIO(terminal_tsv),delimiter='\t'):
        status=row['Sonde_und_Materie']
        state='AUSGESCHLOSSEN' if status=='KRAGEN_AUSSCHLUSS' else status
        reason={'ZEUGE':'N22_Feld_und_terminale_freie_Uhr',
                'KRAGEN_AUSSCHLUSS':'Kragenzeit','OFFEN':'Terminal_ohne_Zukunftsanker'}[status]
        combined.append(['∅',row['Vergangenheit'],row['Praeparation'],'terminale_Sonde',
                         state,state,'AUSGESCHLOSSEN','nicht einzeln geprüft' if status=='OFFEN' else '–',reason])
    assert len(combined)==5315 and all(len(r)==9 for r in combined)
    products={'Terminalregister.tsv':terminal_tsv.encode(),'Kontrollfelder.json':fields,
              'Gesamtregister.tsv':tsv(combined[0],combined[1:]).encode()}
    for filename,content in products.items():
        if write:(ROOT/filename).write_bytes(content)
        else:assert (ROOT/filename).read_bytes()==content,filename
    print("2 657 Ordnungen unabhängig gezählt. Vier zusätzliche stationäre Lösungen und terminale Kontrollfamilie bestätigt.")

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen')
    assert sys.argv[1:] in ([],['--ausgabe'])
    main('--ausgabe' in sys.argv)
