"""Build the report with a full TeX Live installation; no global TeX changes."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
OUTPUT=ROOT/'CST_DUST_Basisunabhaengiger_Kopplungsbefund_v0_1.pdf'

def run(args,cwd,env):
    r=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if r.returncode:
        raise RuntimeError(r.stdout[-8000:])
    return r.stdout

def main():
    env=os.environ.copy()
    with tempfile.TemporaryDirectory() as tmp:
        # Some minimal images include TeX sources but no database/formats.
        found=subprocess.run(['kpsewhich','pdflatex.fmt'],env=env,stdout=subprocess.PIPE,text=True)
        if not found.stdout.strip():
            candidates=[Path('/usr/share/texmf'),Path('/usr/share/texlive/texmf-dist')]
            trees=[str(x) for x in candidates if x.is_dir()]
            if trees:
                env['TEXMF']='{'+','.join(trees)+'}'
            env['TEXFORMATS']=tmp
            run(['pdftex','-ini','-etex','-jobname=pdflatex','-progname=pdflatex',
                 '-interaction=nonstopmode','-halt-on-error','-output-directory='+tmp,'pdflatex.ini'],tmp,env)
        for _ in range(2):
            log=run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                     '-output-directory='+tmp,str(ROOT/'DERIVATION.tex')],ROOT,env)
        if 'Overfull' in log:
            lines=log.splitlines()
            details='\n'.join('\n'.join(lines[i:i+5]) for i,line in enumerate(lines) if 'Overfull' in line)
            raise RuntimeError('PDF layout contains an overfull box:\n'+details)
        shutil.copyfile(Path(tmp)/'DERIVATION.pdf',OUTPUT)
    print(OUTPUT)

if __name__=='__main__':
    main()
