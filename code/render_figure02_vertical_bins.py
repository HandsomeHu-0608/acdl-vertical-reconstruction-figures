"""Render ES&T Figure 2 from height-resolved summary data."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import AFTER, BEFORE, DPI, package_root, read, setup

def render(output: Path) -> None:
    setup(); d=read(package_root()/"data"/"figure02_vertical_bins.nc"); h=d['height']; s=d['summary']
    fig,axes=plt.subplots(1,3,figsize=(6.2,3.65),sharey=True)
    for ax,offset,label in zip(axes[:2],[0,3],['Bias\n'+r'$\log_{10}(\mathrm{Ext}_{\mathrm{WRF}}/\mathrm{Ext}_{\mathrm{ACDL}})$','RMSE\n'+r'$\log_{10}(\mathrm{Ext}_{\mathrm{WRF}}/\mathrm{Ext}_{\mathrm{ACDL}})$']):
        for i,color,name in [(0,BEFORE,'noCorr'),(1,AFTER,'Corr')]:
            med,q25,q75=s[i,:,offset:offset+3].T; good=np.isfinite(med)
            ax.fill_betweenx(h[good],q25[good],q75[good],color=color,alpha=.20,lw=0); ax.plot(med[good],h[good],color=color,lw=1.55,label=name)
        ax.set_xlabel(label,fontsize=12)
    ax=axes[2]
    for i,color,marker,name in [(0,BEFORE,'^','noCorr'),(1,AFTER,'s','Corr')]:
        r=s[i,:,6]; good=np.isfinite(r); ax.plot(r[good],h[good],'-'+marker,color=color,lw=1.45,ms=4.6,label=name)
    ax.set_xlabel('Pearson R',fontsize=13); ax.legend(loc='upper right',bbox_to_anchor=(1,.90),fontsize=11,handlelength=1.8)
    for ax in axes:
        ax.set_ylim(0,16); ax.set_yticks(np.arange(0,17,2)); ax.grid(axis='x',color='#C8C8C8',lw=.45,alpha=.65); ax.grid(axis='y',color='#E4E4E4',lw=.4,alpha=.75); ax.tick_params(width=.8,length=3,labelsize=12)
        for sp in ax.spines.values(): sp.set_linewidth(.75)
    axes[0].axvline(0,color='#202020',ls='--',lw=1); axes[0].set_xlim(-1,1); axes[1].set_xlim(0,1); axes[2].set_xlim(0,1); axes[0].set_ylabel('Height (km)',fontsize=13)
    for label,ax in zip(('a','b','c'),axes): ax.text(.97,.97,f'({label})',transform=ax.transAxes,fontsize=14,fontweight='bold',va='top',ha='right')
    fig.subplots_adjust(left=.095,right=.985,bottom=.22,top=.94,wspace=.18); output.parent.mkdir(parents=True,exist_ok=True); fig.savefig(output,dpi=DPI,bbox_inches='tight',facecolor='white');plt.close(fig)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=package_root()/"generated_outputs"/"Figure_2_Test40_vertical_bins.png");a=p.parse_args();render(a.output)
