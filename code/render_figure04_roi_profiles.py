"""Render ES&T Figure 4 using packaged regional summaries and map context."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import ACDL, AFTER, BEFORE, DPI, dem_cmap, draw_nan_segments, package_root, read, setup

def draw_profile(ax,h,stat,title,showx,showy,legend):
    for i,color,label,lw in [(0,ACDL,'ACDL',1.6),(1,BEFORE,r'wrfinput$_{noCorr}$',1.5),(2,AFTER,r'wrfinput$_{Corr}$',1.5)]:
        med,q25,q75=stat[i,:,0],stat[i,:,1],stat[i,:,2]; good=np.isfinite(med); ax.fill_betweenx(h[good],np.maximum(q25[good],1e-12),np.maximum(q75[good],1e-12),color=color,alpha=.20,lw=0);ax.semilogx(med[good],h[good],color=color,lw=lw,label=label)
    ax.set(xscale='log',xlim=(1e-4,.5),ylim=(-.5,16.5),title=title);ax.grid(True,which='both',color='#B8B8B8',lw=.4,alpha=.75);ax.tick_params(direction='in',width=.9,length=3.2,labelsize=13)
    if showx:ax.set_xlabel(r'Extinction (km$^{-1}$)',fontsize=14)
    else:ax.set_xticklabels([])
    if showy:ax.set_ylabel('Height (km)',fontsize=14)
    else:ax.set_yticklabels([])
    if legend:ax.legend(loc='lower left',fontsize=12,handlelength=3)

def render(output:Path)->None:
 setup();d=read(package_root()/"data"/"figure04_roi_profiles.nc");m=read(package_root()/"data"/"map_context_china.nc");h=d['height'];fig=plt.figure(figsize=(13.5,11.1));gs=fig.add_gridspec(3,4,left=.055,right=.978,bottom=.055,top=.965,wspace=.12,hspace=.18)
 mapax=fig.add_subplot(gs[:2,:3]);im=mapax.pcolormesh(m['dem_longitude'],m['dem_latitude'],np.where(m['china_mask'].astype(bool),m['dem_elevation'],np.nan),shading='auto',cmap=dem_cmap(),norm=Normalize(0,7000))
 for name,color,lw in [('world','#B8B8B8',.55),('country','#202020',.9),('province','#202020',.55)]:draw_nan_segments(mapax,m[f'{name}_longitude'],m[f'{name}_latitude'],color=color,lw=lw,zorder=3)
 draw_nan_segments(mapax,d['wrf_outline_longitude'],d['wrf_outline_latitude'],color='#E41A1C',lw=2.0,zorder=5)
 for k in range(1,6):mapax.text(float(d['region_label_longitude'][k]),float(d['region_label_latitude'][k]),f'G{k}',color='#E41A1C',fontsize=17,fontweight='bold',ha='center',va='center',bbox={'boxstyle':'round,pad=.18','facecolor':'white','edgecolor':'none','alpha':.72})
 mapax.set(xlim=(64,147),ylim=(10,60),xlabel='Longitude (°E)',ylabel='Latitude (°N)');mapax.grid(color='#B8B8B8',lw=.4,alpha=.7);mapax.tick_params(direction='in',labelsize=12)
 cax=fig.add_axes([.17,.965,.45,.026]);cb=fig.colorbar(im,cax=cax,orientation='horizontal');cax.xaxis.set_ticks_position('top');cax.xaxis.set_label_position('top');cb.set_label('Elevation (m)',fontsize=14,fontweight='bold');cb.ax.tick_params(labelsize=12)
 axes=[fig.add_subplot(gs[0,3]),fig.add_subplot(gs[1,3]),fig.add_subplot(gs[2,0]),fig.add_subplot(gs[2,1]),fig.add_subplot(gs[2,2]),fig.add_subplot(gs[2,3])]; labels=['All Test set','G1 Northwest','G2 Northeast','G3 Plateau','G4 North','G5 South']
 for i,ax in enumerate(axes):draw_profile(ax,h,d['statistics'][i],f'({chr(97+i)}) {labels[i]}',i not in(0,1),i in(0,1,2),i==0)
 output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(output,dpi=DPI,bbox_inches='tight',facecolor='white');plt.close(fig)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=package_root()/"generated_outputs"/"Figure_4_roi_profiles.png");a=p.parse_args();render(a.output)
