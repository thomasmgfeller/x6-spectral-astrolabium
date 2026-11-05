#!/usr/bin/env python3
"""Structural asset checks; does not claim Excel GUI or pixel-render validation."""
import json, pathlib, zipfile, xml.etree.ElementTree as ET, hashlib
root=pathlib.Path(__file__).resolve().parent
ns={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
with zipfile.ZipFile(root/"X6_Gaussian_Worksheet_v0_1.xlsx") as z:
    assert z.testzip() is None
    for name in z.namelist():
        if name.endswith((".xml",".rels")): ET.fromstring(z.read(name))
    wb=ET.fromstring(z.read("xl/workbook.xml"))
    assert len(wb.find("m:sheets",ns))==6
    calc=ET.fromstring(z.read("xl/worksheets/sheet3.xml"))
    assert len(calc.findall(".//m:f",ns))==88
    cells={x.attrib["r"]:x for x in calc.findall(".//m:c",ns)}
    ref=json.loads((root/"referenz.json").read_text())
    for col,row in zip("BCDE",ref["pump"]):
        for rn,key in [(17,"w0_um"),(18,"w_center_um"),(19,"waist_shift_local_mm"),(20,"zR_crystal_mm")]:
            assert abs(float(cells[f"{col}{rn}"].find("m:v",ns).text)-row[key])<1e-8
    measured=ET.fromstring(z.read("xl/worksheets/sheet6.xml"))
    assert not any(x.attrib["r"][0] in "BCD" and x.attrib["r"][1:]!="1" for x in measured.findall(".//m:c",ns))
svg=ET.fromstring((root/"X6_Sagnac_Layout_A2_1zu2.svg").read_bytes())
assert svg.attrib["width"]=="594mm" and svg.attrib["height"]=="420mm"
assert svg.attrib["viewBox"]=="0 0 1188 840"
for line in (root/"SHA256SUMS.txt").read_text().splitlines():
    digest,name=line.split("  ",1)
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
archive=root/"X6_Gaussian_Layout_v0_1_Pruefpaket.zip"
if archive.exists():
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist(): assert z.read(name)==(root/name).read_bytes(),name
else:
    print("Extracted package: archive absent; member hashes are verified.")
print("PASS: six sheets, 88 formulas, cached reference values, blank measurements, scale, hashes and archive.")
