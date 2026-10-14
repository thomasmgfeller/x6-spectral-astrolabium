#!/usr/bin/env python3
"""Common local entry point. Copyright 2026 Thomas Gfeller, Apache-2.0."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
environment = ROOT / '.venv'
python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
if len(sys.argv) > 1 and sys.argv[1] != 'setup' and python.is_file() and Path(sys.prefix).resolve() != environment.resolve():
    env = dict(os.environ, PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    os.execve(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]], env)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from tools.workflow.cli import main

if __name__ == '__main__':
    raise SystemExit(main())
