"""Render ES&T Figure 5 one-degree extinction maps from packaged NetCDF."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import DPI, draw_nan_segments, package_root, read, setup

def render(output:Path)->None:
 setup();d=read(package_root()/"data"/"figure05_extinction_maps.nc");m=read(package_root()/"data"/"map_context_china.nc");fig,axes=plt.subplots(3,3,figsize=(9.2,6.75));fig.subplots_adjust(left=.05,right=.925,bottom=.06,top=.975,wspace=.035,hspace=.14);norm=LogNorm(1e-3,1); names=['noCorr','Corr','ACDL'];fields=[d['before'],d['after'],d['acdl']];last=None
 for r,level in enumerate(d['levels']):
  for c in range(3):
   ax=axes[r,c];last=ax.pcolormesh(d['lon'],d['lat'],fields[c][r],shading='auto',cmap='jet',norm=norm)
   for name,color,lw in [('world','#9A9A9A',.6),('country','#202020',1.0),('province','#8C8C8C',.7)]:draw_nan_segments(ax,m[f'{name}_longitude'],m[f'{name}_latitude'],color=color,lw=lw,zorder=3)
   ax.set(xlim=(72,137),ylim=(15,57));ax.set_xticks(np.arange(80,131,10));ax.set_yticks(np.arange(20,51,10));ax.tick_params(direction='in',width=.8,length=3,labelsize=12)
   if c==0:ax.set_ylabel('Latitude (°N)',fontsize=14)
   else:ax.set_yticklabels([])
   if r==2:ax.set_xlabel('Longitude (°E)',fontsize=14)
   else:ax.set_xticklabels([])
   ax.set_title(f'({chr(97+r)}{c+1}) {names[c]} {int(level)} km',fontsize=15,fontweight='bold',pad=2.5)
 cax=fig.add_axes([.94,.18,.018,.64]);cb=fig.colorbar(last,cax=cax);cb.set_label(r'Extinction (km$^{-1}$)',fontsize=13);cb.ax.tick_params(labelsize=11)
 output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(output,dpi=DPI,bbox_inches='tight',facecolor='white');plt.close(fig)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=package_root()/"generated_outputs"/"Figure_5_extinction_maps.png");a=p.parse_args();render(a.output)
