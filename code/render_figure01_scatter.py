"""Render ES&T Figure 1 from drawing-ready hexbin NetCDF data."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DPI, package_root, read, setup


def hexagon(x, y, rx, ry):
    angles = np.deg2rad(np.arange(0, 360, 60) + 30)
    return np.c_[x + rx*np.cos(angles), y + ry*np.sin(angles)]


def render(output: Path) -> None:
    setup(); d = read(package_root()/"data"/"figure01_scatter.nc")
    fig = plt.figure(figsize=(6.0, 2.58)); gs = fig.add_gridspec(1,3,width_ratios=[1,1,.048],left=.074,right=.928,bottom=.145,top=.912,wspace=.02)
    axes=[fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1])]
    dx=np.min(np.diff(np.unique(d['acdl_log10_center']))); dy=np.min(np.diff(np.unique(d['wrf_log10_center'])))
    cmap=plt.get_cmap('jet'); norm=Normalize(11,500,clip=True)
    labels=[r"(a) $\mathbf{wrfinput}_{\mathbf{noCorr}}$ vs. ACDL",r"(b) $\mathbf{wrfinput}_{\mathbf{Corr}}$ vs. ACDL"]
    notes=["N=315985\nR = 0.506\nRMSE = 0.111\nBias = -0.025","N=315985\nR = 0.708\nRMSE = 0.087\nBias = -0.014"]
    last=None
    for i,ax in enumerate(axes):
        m=d['condition']==i; x=d['acdl_log10_center'][m]; y=d['wrf_log10_center'][m]; c=d['count'][m]
        polys=np.asarray([hexagon(a,b,dx*.58,dy*.56) for a,b in zip(x,y)])
        colors=np.asarray([(.72,.72,.72,1) if q<=10 else cmap(norm(q)) for q in c])
        ax.add_collection(PolyCollection(polys, facecolors=colors, edgecolors='none', linewidths=0))
        ax.plot([-4,0],[-4,0],color='#202020',lw=1)
        ax.set(xlim=(-4,0),ylim=(-4,0),aspect='equal',title=labels[i])
        ax.set_xticks([-4,-3,-2,-1,0]); ax.set_yticks([-4,-3,-2,-1,0])
        ax.set_xticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$'])
        ax.set_yticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$'])
        ax.set_xlabel(r'ACDL extinction (km$^{-1}$)',fontsize=11); ax.tick_params(labelsize=10,width=.8,length=3)
        ax.set_title(labels[i],fontsize=12,pad=5,fontweight='bold'); ax.text(.04,.96,notes[i],transform=ax.transAxes,va='top',fontsize=10)
        for spine in ax.spines.values(): spine.set_linewidth(.8)
    axes[0].set_ylabel(r'WRF extinction (km$^{-1}$)',fontsize=11)
    sm=plt.cm.ScalarMappable(norm=norm,cmap=cmap); cbar=fig.colorbar(sm,cax=fig.add_subplot(gs[0,2])); cbar.set_label('Density',fontsize=11); cbar.set_ticks([11,100,200,300,400,500]); cbar.set_ticklabels(['0-10','100','200','300','400','500']); cbar.outline.set_visible(False)
    output.parent.mkdir(parents=True,exist_ok=True); fig.savefig(output,dpi=DPI,bbox_inches='tight',facecolor='white'); plt.close(fig)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=package_root()/"generated_outputs"/"Figure_1_Test40_scatter.png"); args=p.parse_args(); render(args.output)
