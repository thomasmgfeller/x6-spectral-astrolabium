"""Verify a copied X6 run, including partial/error captures, against its manifest."""
import argparse
import json
from pathlib import Path
import re
from drivers import digest

def verify(folder):
    folder=Path(folder)
    m=json.loads((folder/"manifest.json").read_bytes())
    if m.get("schema")!="x6.photonics.run.v1" or not isinstance(m.get("files"),dict):
        raise ValueError("Unbekanntes Manifest")
    actual={p.name for p in folder.iterdir() if p.name!="manifest.json"}
    if actual!=set(m["files"]):
        raise ValueError("Dateibestand stimmt nicht mit dem Manifest überein")
    for name,record in m["files"].items():
        p=folder/name
        if not re.fullmatch(r"[A-Za-z0-9_.-]+",name) or name in (".","..") or p.is_symlink() or not p.is_file():
            raise ValueError("Unerwarteter Archiveintrag")
        if p.stat().st_size!=record["bytes"] or digest(p)!=record["sha256"]:
            raise ValueError("Größe oder SHA-256 abweichend: "+name)
    return dict(files_verified=len(actual),run_state=m["final"]["state"],run_id=m["final"]["run_id"])
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder",type=Path)
    try: print(json.dumps(verify(parser.parse_args().folder),indent=2))
    except (OSError,ValueError,KeyError) as e:parser.exit(2,str(e)+"\n")
