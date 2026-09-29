"""Render the packaged scatter plot corresponding to manuscript Figure 2."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.collections import PolyCollection
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.transforms import AffineDeltaTransform
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DPI, package_root, read, setup


def density_palette():
    """Match the manuscript's gray 0-10 bins and density scale for 11-500."""
    gray = np.repeat(np.array(mcolors.to_rgba('#B8B8B8'))[None, :], 11, axis=0)
    colored = plt.get_cmap('jet')(np.linspace(0.05, 1.0, 490))
    cmap = ListedColormap(np.vstack([gray, colored]), name='gray_then_jet')
    return cmap, BoundaryNorm(np.arange(-0.5, 501.5, 1.0), cmap.N, clip=True)


def render(output: Path) -> None:
    setup()
    plt.rcParams['font.size'] = 10
    source = package_root() / 'data' / 'figure01_scatter.nc'
    data = read(source)
    with h5py.File(source, 'r') as h:
        gridsize = int(np.asarray(h.attrs['hex_gridsize']).item())
    # Match matplotlib's log-scale hexbin geometry, including its x padding.
    sx = (4.0 + 8.0e-9) / gridsize
    sy = 4.0 / int(gridsize / np.sqrt(3.0))
    polygon = np.array([[.5, -.5], [.5, .5], [0, 1],
                        [-.5, .5], [-.5, -.5], [0, -1]]) * [sx, sy / 3]
    polygon = 10.0 ** polygon
    fig = plt.figure(figsize=(6.0, 2.58))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, .048],
                          left=.074, right=.928, bottom=.145, top=.912, wspace=.02)
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
    axes[1].sharex(axes[0]); axes[1].sharey(axes[0])
    cmap, norm = density_palette()
    titles = [r'(a) $\mathbf{wrfinput}_{\mathbf{noCorr}}$ vs. ACDL',
              r'(b) $\mathbf{wrfinput}_{\mathbf{Corr}}$ vs. ACDL']
    for i, ax in enumerate(axes):
        selected = data['condition'] == i
        offsets = np.column_stack([data['acdl_log10_center'][selected],
                                   data['wrf_log10_center'][selected]])
        ax.set_xscale('log'); ax.set_yscale('log')
        collection = PolyCollection([polygon], offsets=offsets,
                                    offset_transform=AffineDeltaTransform(ax.transData), linewidths=0)
        collection.set_cmap(cmap); collection.set_norm(norm)
        collection.set_array(data['count'][selected].astype(float))
        ax.add_collection(collection, autolim=False)
        ax.plot([1e-4, 1], [1e-4, 1], color='#202020', lw=1.0, ls='-')
        ax.set_xlim(1e-4, 1); ax.set_ylim(1e-4, 1)
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(titles[i], fontsize=12, pad=5, fontweight='bold')
        ax.set_xlabel(r'ACDL extinction (km$^{-1}$)', fontsize=11)
        ax.tick_params(labelsize=10, width=.8, length=3)
        for spine in ax.spines.values():
            spine.set_visible(True); spine.set_linewidth(.8)
        # Full-sample metrics are supplied with the data, never inferred from bins.
        annotation = (f"N={int(data['metric_n'][i])}\n"
                      f"R = {data['metric_r'][i]:.3f}\n"
                      f"RMSE = {data['metric_rmse'][i]:.3f}\n"
                      f"Bias = {data['metric_bias'][i]:+.3f}")
        ax.text(.04, .96, annotation, transform=ax.transAxes, va='top', fontsize=10)
    axes[0].set_ylabel(r'WRF extinction (km$^{-1}$)', fontsize=11)
    cbar = fig.colorbar(collection, cax=fig.add_subplot(gs[0, 2]))
    cbar.set_label('Density', fontsize=11)
    cbar.set_ticks([5, 100, 200, 300, 400, 500])
    cbar.set_ticklabels(['0-10', '100', '200', '300', '400', '500'])
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(labelsize=10, width=.5, length=3)
    for spine in cbar.ax.spines.values():
        spine.set_visible(True); spine.set_linewidth(.55)
        spine.set_edgecolor(mcolors.to_rgba('#202020', .9))
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path,
                        default=package_root() / 'generated_outputs' / 'Figure_1_Test40_scatter.png')
    render(parser.parse_args().output)
