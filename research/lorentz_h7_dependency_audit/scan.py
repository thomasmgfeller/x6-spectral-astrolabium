"""Read-only source inventory and bounded text search at a pinned Git revision.

This is a retrieval aid, NOT a semantic proof that dependencies are absent.
It never executes code from archives. Requires Git and Poppler pdftotext.
"""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

BASE='dc50ffb228e442a230a32e4437e8e452a90b39ad'
ROOT=Path(__file__).resolve().parents[2]
PATTERNS={
    'H7':r'H7|W_future|W_past|F0_W|bidirectional.moments',
    'identity':r'isomorph|canonical_key|canoni[cz]ation|dedup|EXACT_COLLISION|OBSERVATIONALLY_UNRESOLVED',
    'signature':r'fingerprint|spectral_key|signature|signatur',
    'reconstruction':r'(?:eindeutig|unique|complete|vollständig|injectiv|identity|identit|reconstruct|rekonstruk).{0,100}(?:spect|spektr|graph|order|ordnung|geometr)|(?:spect|spektr).{0,100}(?:eindeutig|unique|complete|vollständig|injectiv|identity|identit|reconstruct|rekonstruk)'
}
TEXT_SUFFIXES={'.py','.js','.mjs','.cjs','.md','.txt','.json','.html','.css','.yml','.yaml','.toml','.cff','.wl','.jl','.sh','.xml','.csv','.tsv','.rst','.tex','.v','.vhd','.hpp','.h','.cpp','.c'}


def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()


def scan(cache=None):
    regex={k:re.compile(v,re.I) for k,v in PATTERNS.items()}
    registry=json.loads(git('show',BASE+':MODULE_REGISTRY.json'))
    scopes=[{'name':'main','commit':BASE,'prefix':''}]
    for module in registry['modules']:
        s=module['source']
        if s['availability']=='BRANCH_ONLY':
            scopes.append({'name':module['id'],'commit':s['commit'],'prefix':str(PurePosixPath(s['path']).parent)+'/'})
    inventory=[];matches=[];gaps=[];consumed=0
    def inspect(data,location,depth=0):
        nonlocal consumed
        consumed+=len(data)
        if consumed>1024**3:raise ValueError('total scan budget exceeded')
        ext=PurePosixPath(location).suffix.lower()
        row={'location':location,'sha256':sha(data),'bytes':len(data)};inventory.append(row)
        text=None
        if ext=='.docx':
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                parts=[n for n in z.namelist() if n.startswith('word/') and n.endswith('.xml') and any(x in n for x in ['document','footnote','endnote','header','footer'])]
                text='\n'.join(' '.join(paragraph.itertext()) for n in sorted(parts) for paragraph in ET.fromstring(z.read(n)).iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))
            row['kind']='docx_text_xml'
        elif ext=='.pdf':
            p=subprocess.run(['pdftotext','-layout','-','-'],input=data,capture_output=True,timeout=30)
            if p.returncode:raise ValueError('PDF extraction failed: '+location)
            text=p.stdout.decode('utf8');row['kind']='pdf_text'
            if not text.strip():gaps.append({'location':location,'reason':'PDF has no extractable text; images not OCR-reviewed'})
        elif ext=='.zip':
            row['kind']='zip_container'
            if depth>=3:raise ValueError('archive nesting budget: '+location)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                infos=sorted((i for i in z.infolist() if not i.is_dir()),key=lambda i:i.filename)
                if len(infos)>10000 or sum(i.file_size for i in infos)>256*1024**2:raise ValueError('archive budget: '+location)
                for item in infos:
                    if item.file_size>64*1024**2:raise ValueError('member budget: '+location)
                    inspect(z.read(item),location+'!'+item.filename,depth+1)
        else:
            if ext in TEXT_SUFFIXES or (ext=='' and b'\0' not in data[:4096]):
                try:text=data.decode('utf8');row['kind']='utf8_text'
                except UnicodeDecodeError:row['kind']='binary_not_text_reviewed'
            else:row['kind']='binary_not_text_reviewed'
        if text is not None:
            row['text_sha256']=sha(text.encode());row['text_lines']=len(text.splitlines())
            if cache is not None:
                target=cache/(sha(location.encode())+'.txt');target.write_text(text)
            hits={}
            for label,pattern in regex.items():
                lines=[(i+1,line) for i,line in enumerate(text.splitlines()) if pattern.search(line)]
                if lines:hits[label]={'matching_lines':len(lines),'first_matches':[{'line':i,'text':line[:500]} for i,line in lines[:8]]}
            if hits:matches.append({'location':location,'hits':hits})
    for scope in scopes:
        entries=git('ls-tree','-r','--name-only',scope['commit'],'--',scope['prefix'] or '.').decode().splitlines()
        scope['files']=len(entries)
        for name in entries:inspect(git('show',scope['commit']+':'+name),scope['name']+'@'+scope['commit']+':'+name)
    # Branch components refer to these shared files outside their module roots.
    cross=[]
    for scope in scopes:
        prefixes=[]
        if scope['name'] in ('experiment-fabric','neutral-discovery'):prefixes+=['research/fingerprint_v1/']
        if scope['name']=='neutral-discovery':prefixes+=['experimental/experiment_fabric/']
        if scope['name'] in ('fingerprint','experiment-fabric','neutral-discovery'):prefixes+=['research/lorentz_n6/']
        if scope['name'] in ('lorentz-n6','fingerprint','experiment-fabric','neutral-discovery'):prefixes+=['agent/lorentz_spectral.py']
        for prefix in prefixes:
            names=git('ls-tree','-r','--name-only',scope['commit'],'--',prefix).decode().splitlines()
            for name in names:
                location=scope['name']+'@'+scope['commit']+':'+name
                inspect(git('show',scope['commit']+':'+name),location);cross.append(location)
    return {'schema':'x6.h7-dependency-scan/1','base_commit':BASE,'registered_modules':len(registry['modules']),
            'scopes':scopes,'cross_module_files':cross,'patterns':PATTERNS,
            'inventory':inventory,'matches':matches,'extraction_gaps':gaps,
            'counts':{'inventory_entries':len(inventory),'kinds':dict(sorted(Counter(r['kind'] for r in inventory).items())),
                      'files_with_matches':len(matches),'bytes_read_including_archive_members':consumed},
            'limits':['Text extraction and keyword retrieval are not semantic dependency proofs.',
                      'Raster images, binary datasets and unavailable archives are not source-reviewed.',
                      'Only the pinned main tree, registered branch module roots and listed cross-module files are included.',
                      'No claim about unrelated repositories, unpublished library files or all historical commits.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--text-cache',type=Path)
    a=p.parse_args()
    if a.text_cache:a.text_cache.mkdir(parents=True,exist_ok=True)
    result=scan(a.text_cache);a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'base_commit':BASE,**result['counts'],'extraction_gaps':result['extraction_gaps']}))
