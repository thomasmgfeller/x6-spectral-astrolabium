# Strict and portable replays are different claims

The first GitHub job (39418799159, head 99bfa374ff4830944420c3286dfe60423253ed24)
passed all five controls but failed the strict regenerated-coordinate bytehash
check. This is retained as a failed strict platform replay, not reclassified
as a success. Local strict replay matched all 32 coordinate bytehashes.

The separate `verify_portable.py` records both coordinate hash matches and
mismatches. It still requires:

- exact archive/source SHA256, fixed seeds, event counts, observed root/support
  order, every used interval count, acceptance decisions and summary gates;
- independently checked moment/KKT witnesses and strict relation predicates;
- repeated projection/weights within the existing absolute 1e-8 plus relative
  1e-7 tolerance; field and covariance checks within the existing 1e-10 + 1e-10
  relative tolerance; summary floats within 1e-10 + 1e-9 relative tolerance.

The portable check is a new platform diagnostic added after the strict CI
failure. It does not change inference, calibration, data, estimator choice,
thresholds, or the CONDITIONAL_HOLD/HOLD_PHASE3 decisions. Strict `verify.py`
still rejects any coordinate-byte mismatch. GitHub runs the explicitly named
portable diagnostic; its logs report actual mismatch and maximum field/weight
difference counts.

Neither check repeats the full frame search. In portable mode, exact equality
of every full-cloud relation is not claimed: independently checked relations
cover the selected points, and interval counts cover all counted intervals.
The archived raw arrays are not stored, so no componentwise coordinate-error
bound against the original arrays is claimed. A portable PASS cannot establish
bitwise coordinates, external scientific replication or physical qualification.
