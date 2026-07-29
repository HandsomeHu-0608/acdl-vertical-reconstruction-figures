# ES&T Figure Code and Plotting Data Package

This standalone package reproduces the five main-text figure groups in the ES&T manuscript using only the included Python code and drawing-ready NetCDF files. It does not include raw DQ-1/ACDL observations, WRF-Chem input files, trained models, GIS shapefiles, or the original DEM files.

## Reproduce

Use Python 3.13 and install the pinned packages:

```bash
pip install -r requirements.txt
python reproduce_all.py
python qa_verify.py
```

The six output PNGs are written to `generated_outputs/` at 600 dpi:

| Manuscript figure | Output |
|---|---|
| Figure 1 | `Figure_1_Test40_scatter.png` |
| Figure 2 | `Figure_2_Test40_vertical_bins.png` |
| Figure 3 | `Figure_3a_day_profiles.png`, `Figure_3b_night_profiles.png` |
| Figure 4 | `Figure_4_roi_profiles.png` |
| Figure 5 | `Figure_5_extinction_maps.png` |

`reference_outputs/` contains the submitted PNGs used for visual regression. Run `qa_verify.py` before release and inspect any reported dimension or visual regression difference; platform-level font rasterization can also alter pixels.

## NetCDF contents

- `figure01_scatter.nc`: draw-ready hexagon centers/counts/classes plus the submitted statistical annotations. It intentionally stores binned display data rather than individual matched layers.
- `figure02_vertical_bins.nc`: height-resolved median, interquartile range, and Fisher-mean linear correlation used by the three panels.
- `figure03_day_profiles.nc` and `figure03_night_profiles.nc`: curtain grids, terrain/missing masks, and three selected profile arrays for the representative examples.
- `figure04_roi_profiles.nc`: six regional, height-resolved median/IQR profile summaries and map labels.
- `figure05_extinction_maps.nc`: three altitude levels of draw-ready 1° × 1° noCorr, Corr, and ACDL fields.
- `map_context_china.nc`: cropped DEM plus extracted line geometry for the map backgrounds. NaN values separate independent line segments.

All extinction variables are in km⁻¹; latitude and longitude coordinates are in degrees north/east. NetCDF files use CF-1.10 metadata, float32 drawing arrays, and lossless compression.

## Data-processing boundary

The package is designed for figure reproduction, not re-executing the full observation processing, WRF-Chem extinction calculation, or machine-learning vertical reconstruction. Inputs are the smallest processed values sufficient to redraw the submitted figures. Figure 1 retains its submitted `N = 315985` annotation and displayed statistics.

## License and attribution

Code is MIT-licensed; plotting data are CC BY 4.0. See `LICENSE-CODE`, `LICENSE-DATA`, and `THIRD_PARTY_NOTICES.md`.
