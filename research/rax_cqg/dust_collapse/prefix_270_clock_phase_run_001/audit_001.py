"""Standard-library audit of the archived output of the prefix 270 target run."""
import hashlib
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ARCHIVE = "CST_DUST_Praefix_270_Uhrphase_Vorregistrierung_v1_0.zip"
LOCK = "ea71c099519b99cd15dd079868d893dd20fbc7a51ef190b456246452848f5b44"
PACKAGE_SHA = "700a7fe72ab1d905b88f48179da213f7415b286aae253f3fc59e83e54346f732"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError(f"Duplicate key {k}")
        result[k] = v
    return result

def parse(data):
    return json.loads(data, object_pairs_hook=no_duplicates)

def bracket(squared):
    grid = 10**15
    k = isqrt(int(squared*grid**2))
    low = F(k, grid)
    high = low if low**2 == squared else F(k+1, grid)
    assert low**2 <= squared <= high**2
    return low, high

def run():
    package = HERE / ARCHIVE
    assert digest(package.read_bytes()) == PACKAGE_SHA
    with ZipFile(package) as z:
        raw_reg = z.read("registration.json")
        assert digest(raw_reg) == LOCK
        reg = parse(raw_reg)
        for name, hashed in reg["frozen_files_sha256"].items():
            assert digest(z.read(name)) == hashed
        ref = parse(z.read("reference.json"))
        gram = parse(z.read("gram/gram.json"))
        qual = parse(z.read("qualification.json"))
    raw = parse((HERE / "target_001.json").read_bytes())
    score = parse((HERE / "score_001.json").read_bytes())
    assert raw["registration_sha256"] == score["registration_sha256"] == LOCK
    assert reg["prefix"] == raw["prefix"] == score["prefix"] == 270
    assert reg["status_at_lock"] == "REGISTERED / NOT_RUN"
    rhos = reg["densities"]
    ids = {str(j) for j in reg["end_types"]}
    assert len(ids) == 11 and len(rhos) == 2
    assert set(raw["densities"]) == set(score["ratio_intervals"]) == set(rhos)
    g_lo, g_hi = map(F,(gram["gram_lower"],gram["gram_upper"]))
    assert 0 < g_lo <= 1 <= g_hi
    target_rad = F(reg["decision"]["target_disk_radius"])
    ref_rad = F(reg["decision"]["reference_disk_radius"])
    threshold = F(reg["decision"]["threshold_ratio"])
    assert F(qual["target_error_budget_upper"]) <= target_rad
    results = {}
    counts = 0
    for i, rho in enumerate(rhos):
        rows = raw["densities"][rho]
        assert set(rows) == ids
        lo_all, hi_all, max_dist_sq = F(0), F(0), F(0)
        for ident in sorted(ids, key=int):
            row = rows[ident]
            old = ref["packets"][ident]["densities"][i]
            assert old["density"] == rho
            assert F(row["complex_disk_radius"]) == target_rad
            re, im = map(F,row["complex_center"])
            a, b = map(F,row["unmodulated_split_center"])
            c, d = map(F,old["complex_center"])
            dist_sq = (a-c)**2 + (b-d)**2
            assert dist_sq <= (target_rad + ref_rad)**2
            max_dist_sq = max(max_dist_sq,dist_sq)
            zr_lo,zr_hi = bracket(c*c + d*d)
            m,M = map(F,old["modulus_interval"])
            assert (m,M) == (zr_lo-ref_rad,zr_hi+ref_rad) and 0<m<=M
            lo,hi = bracket(re*re + im*im)
            lo_all = max(lo_all, (max(F(0),lo-target_rad)/M)**2)
            hi_all = max(hi_all, g_hi*(hi+target_rad)**2/(g_lo*m*m))
            counts += 1
        assert (lo_all,hi_all) == tuple(map(F,score["ratio_intervals"][rho]))
        results[rho] = {"lower_ratio":str(lo_all),"upper_ratio":str(hi_all),
                        "qualified_control_count":len(rows),
                        "largest_squared_control_center_distance":str(max_dist_sq)}
    assert counts == score["qualified_controls"] == reg["decision"]["required_unmodulated_split_controls"]
    assert counts == reg["decision"]["required_target_rows"]
    if all(F(r["upper_ratio"])<=threshold for r in results.values()):
        verified = "PASS"
    elif any(F(r["lower_ratio"])>threshold for r in results.values()):
        verified = "FAIL"
    else:
        verified = "HOLD"
    assert score["status"] == verified
    return {"independently_checked_status":verified,"number_of_checked_target_rows":counts,
            "overlap_radius_limit":str(target_rad+ref_rad),"threshold_ratio":str(threshold),
            "checked_density_rows":results}

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O.")
    print(json.dumps(run(),indent=2))
