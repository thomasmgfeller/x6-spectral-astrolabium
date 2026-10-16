"""Build the self-contained offline HTML from tracked template and JS sources."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
template=(ROOT/'web/lab_template.html').read_text()
for marker,name in [('/*__CORE__*/','rax_core.js'),('/*__UI__*/','lab_ui.js')]:
    assert template.count(marker)==1
    template=template.replace(marker,(ROOT/'web'/name).read_text())
(ROOT/'rax_cqg_lab.html').write_text(template)
print('Built rax_cqg_lab.html')
