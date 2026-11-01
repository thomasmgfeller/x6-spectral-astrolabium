"""Load unchanged geometric and KL references under isolated module names."""
from pathlib import Path
import importlib.util
ROOT = Path(__file__).resolve().parents[2]
def load(name, relative):
    spec=importlib.util.spec_from_file_location(name, ROOT/relative)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
kl=load('variance_kl_reference','research/lorentz_de_sitter_kl/core.py')
reference=kl.reference
