"""Regenerate all ES&T main-text figures from the packaged NetCDF files."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "code"))
from render_figure01_scatter import render as figure01
from render_figure02_vertical_bins import render as figure02
from render_figure03_case_profiles import render_case
from render_figure04_roi_profiles import render as figure04
from render_figure05_extinction_maps import render as figure05

OUT = ROOT / "generated_outputs"
OUT.mkdir(exist_ok=True)
figure01(OUT / "Figure_1_Test40_scatter.png")
figure02(OUT / "Figure_2_Test40_vertical_bins.png")
render_case("day", OUT / "Figure_3a_day_profiles.png")
render_case("night", OUT / "Figure_3b_night_profiles.png")
figure04(OUT / "Figure_4_roi_profiles.png")
figure05(OUT / "Figure_5_extinction_maps.png")
print(f"Six PNG files written to: {OUT}")
