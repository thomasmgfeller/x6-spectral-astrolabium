"""Propagate exclusions between identical free systems under implied clock inequalities."""
from collections import defaultdict
from ordnungen import EMPTY
from filter import FREE,Model

def fingerprint(model):
    return tuple((i,j,k) for j in range(23) if j not in EMPTY
                 for i,k,_ in model.inc[j] if i in FREE or j in FREE)

def propagate(full,rel):
    # Every new inequality used below relates 22 to a fixed collar clock strictly outside W.
    from ordnungen import as_relation
    forced={(a,22) for a in (0,1,2,3)}|{(22,b) for b in (7,8,9,10)}
    def group(s):return () if s=='∅' else tuple(map(int,s.split(',')))
    histories={};active=defaultdict(list)
    for i,row in enumerate(full):
        f,p=group(row[0]),group(row[1])
        if row[8]=='Kragenzeit':continue
        # Only compute fingerprints in the few families with any unfinished probe case.
        if row[4]=='OFFEN':active[f].append(i)
    for f in active:
        sets=defaultdict(list)
        for i,row in enumerate(full):
            if group(row[0])!=f or row[8]=='Kragenzeit':continue
            p=group(row[1])
            if p not in histories:
                histories[p]={ (a,22) for a in p}
            ext=as_relation(rel,p,f)
            sig=fingerprint(Model(ext))
            sets[row[2],sig].append((i,histories[p]))
        # Copy input states first to keep the transfer independent of record order.
        original={i:list(full[i]) for items in sets.values() for i,_ in items}
        for items in sets.values():
            for target,past in items:
                row=full[target]
                if row[4]!='OFFEN':continue
                allowed=None if row[7]=='–' else set(group(row[7]))
                reasons=[]
                for source,required in items:
                    if target==source or not required<=past|forced:continue
                    witness=original[source]
                    if witness[4]=='AUSGESCHLOSSEN':
                        row[4:8]=['AUSGESCHLOSSEN','AUSGESCHLOSSEN','AUSGESCHLOSSEN','–']
                        reasons.append(str(source+2));break
                    other=set() if witness[7]=='–' else set(group(witness[7]))
                    if allowed is not None and allowed-other:
                        allowed &= other
                        row[5]='OFFEN' if allowed else 'AUSGESCHLOSSEN'
                        row[7]=','.join(map(str,sorted(allowed))) or '–'
                        reasons.append(str(source+2))
                if reasons:row[8]+='|Freie_Gleichungen_Fallregister_Zeile_'+','.join(reasons)
