"""Replay original frozen experiment and the disclosed follow-up coverage audit."""
import os,subprocess,sys
from pathlib import Path

root=Path(__file__).resolve().parent
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
subprocess.run([sys.executable,'-B','reproduce.py'],cwd=root,env=env,check=True)
subprocess.run([sys.executable,'-B','coverage_audit.py','--verify'],cwd=root,env=env,check=True)
