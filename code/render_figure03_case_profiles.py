"""Render ES&T Figure 3 day and night examples from packaged NetCDF data."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import DPI, package_root, read, setup

COLORS={'noCorr':'#C62828','Corr':'#1565C0','ACDL':'#202020'}

def curtain(ax,lat,alt,field,terrain,title,xlabel):
    mesh=ax.pcolormesh(lat,alt,np.clip(np.where(np.isfinite(field)&(field>0),field,1e-4),1e-4,.5),shading='auto',cmap='jet',norm=LogNorm(1e-4,.5))
    ax.imshow(np.where(terrain,1.,np.nan),origin='lower',extent=[lat.min(),lat.max(),alt.min(),alt.max()],aspect='auto',cmap='gray_r',vmin=0,vmax=1,zorder=3)
    ax.set(ylim=(0,18),xlim=(lat.min(),lat.max()),title=title); ax.set_ylabel('Height (km)',fontsize=17); ax.tick_params(direction='in',width=.9,length=3.5,labelsize=16)
    if xlabel: ax.set_xlabel('Latitude (°N)',fontsize=17)
    else: ax.set_xticklabels([])
    return mesh

def profile(ax,d,k,prefix,showx,legend):
    alt=d['altitude']; j=int(d['profile_index'][k]); acdl=d['profile_acdl_extinction'][:,k]; no=d['nocorr_extinction'][:,j]; co=d['corr_extinction'][:,j]
    for values,color,label,lw in [(no,COLORS['noCorr'],'noCorr',2.3),(co,COLORS['Corr'],'Corr',2.3),(acdl,COLORS['ACDL'],'ACDL',1.8)]: ax.semilogx(np.where(values>=1e-4,values,np.nan),alt,color=color,lw=lw,label=label)
    ax.set(xlim=(1e-4,.5),ylim=(0,18),title=f'({prefix}{k+4})  {d["profile_latitude"][k]:.2f}°N');ax.grid(True,which='both',color='#B8B8B8',lw=.45,alpha=.75);ax.tick_params(direction='in',width=.9,length=3.3,labelsize=16)
    if showx:ax.set_xlabel(r'Extinction (km$^{-1}$)',fontsize=17)
    else:ax.set_xticklabels([])
    if legend:ax.legend(loc='lower left',fontsize=14,handlelength=1.25,handletextpad=.35,labelspacing=.25,borderpad=.15)

def render_case(case:str,output:Path)->None:
    setup();d=read(package_root()/"data"/f"figure03_{case}_profiles.nc"); prefix='a' if case=='day' else 'b';title='Daytime example' if case=='day' else 'Nighttime example'
    fig=plt.figure(figsize=(11.42,11.52)); gs=fig.add_gridspec(3,2,left=.080,right=.965,bottom=.145,top=.925,width_ratios=[5.9,1.606],hspace=.11,wspace=.08);la=[fig.add_subplot(gs[i,0]) for i in range(3)];ra=[fig.add_subplot(gs[i,1]) for i in range(3)]
    mesh=curtain(la[0],d['acdl_map_latitude'],d['acdl_map_altitude'],d['acdl_map_extinction'],d['acdl_map_terrain'],f'({prefix}1) ACDL',False)
    curtain(la[1],d['latitude'],d['altitude'],d['nocorr_extinction'],d['terrain'],f'({prefix}2) noCorr',False);curtain(la[2],d['latitude'],d['altitude'],d['corr_extinction'],d['terrain'],f'({prefix}3) Corr',True)
    for ax in la:
        for x in d['profile_latitude']:ax.axvline(float(x),color='#D81B1B',ls='--',lw=1.9,zorder=6)
    for k,ax in enumerate(ra):profile(ax,d,k,prefix,k==2,k==0)
    fig.text(.080,.955,title,fontsize=21,fontweight='bold',ha='left',va='bottom');p=la[2].get_position();cx=p.x0+.14*p.width; cax=fig.add_axes([cx,.075,.72*p.width,.019]);cb=fig.colorbar(mesh,cax=cax,orientation='horizontal');cb.set_label(r'Extinction (km$^{-1}$)',fontsize=18,fontweight='bold');cb.ax.tick_params(labelsize=16)
    output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(output,dpi=DPI,bbox_inches='tight',facecolor='white');plt.close(fig)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--case',choices=['day','night'],required=True);p.add_argument('--output',type=Path);a=p.parse_args();out=a.output or package_root()/"generated_outputs"/f"Figure_3{'a' if a.case=='day' else 'b'}_{a.case}_profiles.png";render_case(a.case,out)
