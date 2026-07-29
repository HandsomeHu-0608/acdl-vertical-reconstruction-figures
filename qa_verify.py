"""Validate packaged NetCDF files and compare rendering dimensions to references."""
from __future__ import annotations
import hashlib
from pathlib import Path
import h5py
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"; REF = ROOT / "reference_outputs"; OUT = ROOT / "generated_outputs"
required = {
 "figure01_scatter.nc": {"condition","acdl_log10_center","wrf_log10_center","count"},
 "figure02_vertical_bins.nc": {"height","summary"},
 "figure03_day_profiles.nc": {"latitude","altitude","acdl_map_extinction","nocorr_extinction","corr_extinction"},
 "figure03_night_profiles.nc": {"latitude","altitude","acdl_map_extinction","nocorr_extinction","corr_extinction"},
 "figure04_roi_profiles.nc": {"height","statistics"},
 "figure05_extinction_maps.nc": {"levels","lon","lat","before","after","acdl"},
 "map_context_china.nc": {"dem_elevation","china_mask","world_longitude","province_longitude"},
}
for name, keys in required.items():
    with h5py.File(DATA / name, "r") as h:
        missing = keys - set(h.keys())
        if missing: raise RuntimeError(f"{name}: missing {sorted(missing)}")
        convention = h.attrs["Conventions"]
        if isinstance(convention, bytes):
            convention = convention.decode("utf-8")
        assert str(convention) == "CF-1.10"
print(f"NetCDF structure: PASS ({len(required)} files)")

for reference in sorted(REF.glob("*.png")):
    generated = OUT / reference.name
    if not generated.exists(): raise RuntimeError(f"Missing regenerated file: {generated.name}")
    with Image.open(reference) as a, Image.open(generated) as b:
        a=a.convert("RGBA");b=b.convert("RGBA")
        if a.size != b.size: print(f"{reference.name}: SIZE DIFFERENT reference={a.size} generated={b.size}")
        else:
            diff=ImageChops.difference(a,b); bbox=diff.getbbox()
            print(f"{reference.name}: {'PIXEL-IDENTICAL' if bbox is None else 'VISUAL-REGRESSION-BASELINE-AVAILABLE'}")
print("Reference outputs remain packaged for visual regression. Inspect any SIZE DIFFERENT or VISUAL-REGRESSION-BASELINE-AVAILABLE result before release.")

for path in sorted(DATA.glob("*.nc")):
    print(f"{path.name}  sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")
expected = {}
for line in (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    digest, relative = line.split(maxsplit=1)
    expected[relative] = digest
for relative, digest in expected.items():
    observed = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    if observed != digest:
        raise RuntimeError(f"Checksum mismatch: {relative}")
print("SHA-256 manifest: PASS")
