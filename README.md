# Transformer-Based Aerosol Vertical Reconstruction: Figure Code and Plotting Data

This repository provides Python plotting code and drawing-ready NetCDF data for reproducing five figure groups from an ACDL-constrained, Transformer-based aerosol vertical reconstruction study.

The reconstruction framework uses a vertical-column Transformer to represent relationships across atmospheric layers. In the figures, `noCorr` denotes the uncorrected WRF-Chem fields, `Corr` denotes the corrected fields, and `ACDL` denotes the satellite lidar reference.

This package supports figure reproduction only. It does not include raw DQ-1/ACDL observations, WRF-Chem input files, model training code, trained checkpoints, GIS shapefiles, or original DEM files.

## Reproduce

Use Python 3.13 and install the pinned packages:

```bash
pip install -r requirements.txt
python reproduce_all.py
python qa_verify.py
```

The six output PNGs are written to `generated_outputs/` at 600 dpi:

| Figure | Output |
|---|---|
| Figure 1 | `Figure_1_Test40_scatter.png` |
| Figure 2 | `Figure_2_Test40_vertical_bins.png` |
| Figure 3 | `Figure_3a_day_profiles.png`, `Figure_3b_night_profiles.png` |
| Figure 4 | `Figure_4_roi_profiles.png` |
| Figure 5 | `Figure_5_extinction_maps.png` |

`reference_outputs/` contains the baseline PNGs used for visual comparison. Run `qa_verify.py` to check the NetCDF structure, data checksums, and output-image dimensions. Inspect any reported differences; font availability and rendering environments can affect image dimensions and pixels.

## NetCDF contents

- `figure01_scatter.nc`: drawing-ready hexagon centers, counts, classes, and statistical annotations. This file stores binned display data rather than individual matched layers.
- `figure02_vertical_bins.nc`: height-resolved medians, interquartile ranges, and Fisher-mean linear correlations used by the three panels.
- `figure03_day_profiles.nc` and `figure03_night_profiles.nc`: curtain grids, terrain and missing-data masks, and three selected profile arrays for each representative case.
- `figure04_roi_profiles.nc`: height-resolved median and interquartile-range profile summaries for six regions, together with map labels.
- `figure05_extinction_maps.nc`: drawing-ready 1° × 1° `noCorr`, `Corr`, and `ACDL` fields at three altitude levels.
- `map_context_china.nc`: cropped elevation data and extracted line geometry for the map backgrounds. NaN values separate independent line segments.

Extinction coefficients are expressed in km⁻¹. Latitude and longitude coordinates are expressed in degrees north and degrees east, respectively. NetCDF files use CF-1.10 metadata and lossless compression.

## Data-processing boundary

The included scripts render processed plotting data; they do not train or run the Transformer model. The package does not reproduce the upstream observation processing, WRF-Chem extinction calculation, or Transformer-based vertical reconstruction.

The plotting arrays and displayed statistics are retained from the reference figures. In particular, Figure 1 retains the `N = 315985` annotation and associated statistics; these annotations are not recalculated from the binned plotting data.

## License and attribution

Code is MIT-licensed; plotting data are licensed under CC BY 4.0. See `LICENSE-CODE`, `LICENSE-DATA`, and `THIRD_PARTY_NOTICES.md`.
