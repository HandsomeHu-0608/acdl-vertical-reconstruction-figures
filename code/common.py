"""Package-local plotting helpers; no project-specific imports."""
from __future__ import annotations

from pathlib import Path

import h5py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

DPI = 600
BEFORE = "#C62828"
AFTER = "#1565C0"
ACDL = "#202020"


def setup() -> None:
    mpl.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "mathtext.fontset": "custom", "mathtext.rm": "Times New Roman",
        "mathtext.it": "Times New Roman:italic", "mathtext.bf": "Times New Roman:bold",
        "mathtext.default": "regular", "svg.fonttype": "none", "pdf.fonttype": 42,
        "axes.linewidth": 0.8,
    })


def read(path: Path) -> dict[str, np.ndarray]:
    with h5py.File(path, "r") as h:
        return {key: h[key][()] for key in h.keys()}


def jet():
    return plt.get_cmap("jet")


def dem_cmap() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list("dem", [(0.35, 0.78, 0.30), (0.96, 0.94, 0.70), (0.62, 0.50, 0.22), (0.95, 0.95, 0.95)], N=256)


def draw_nan_segments(ax, lon: np.ndarray, lat: np.ndarray, **kwargs) -> None:
    split = np.flatnonzero(~np.isfinite(lon) | ~np.isfinite(lat))
    start = 0
    for stop in np.r_[split, lon.size]:
        if stop - start >= 2:
            ax.plot(lon[start:stop], lat[start:stop], **kwargs)
        start = int(stop) + 1


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]
