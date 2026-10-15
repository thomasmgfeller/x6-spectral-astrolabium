#!/usr/bin/env python3
"""Prove the scaling repair leaves other frames and research kernels unchanged."""
from pathlib import Path
import hashlib, importlib.util, json, re, zipfile

ROOT = Path(__file__).resolve().parents[2]
with zipfile.ZipFile(ROOT/'docs/numerics-v1/historical/check3-original.zip') as z:
    old = z.read('X6_Pruefung_3_v1/source/app/index.html').decode()
current = (ROOT/'app/index.html').read_text()
pattern = r'<iframe\b[^>]*\bid="spectrumFrame"[^>]*>'
assert len(re.findall(pattern, old)) == len(re.findall(pattern, current)) == 1
assert re.sub(pattern, '<SPECTRUM_FRAME>', old) == re.sub(pattern, '<SPECTRUM_FRAME>', current)
spec = importlib.util.spec_from_file_location('math_agent', ROOT/'agent/run_math_agent.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
before, after = module.core_functions(old), module.core_functions(current)
assert before == after, 'Research FFT/filter or graph mapping changed'
print(json.dumps({'status':'PASS', 'outside_spectrum_frame':'BYTE_IDENTICAL',
    'research_core_sha256':[hashlib.sha256(s.encode()).hexdigest() for s in after],
    'scope':'Unchanged research functions; no research agent is executed.'}, indent=2))
