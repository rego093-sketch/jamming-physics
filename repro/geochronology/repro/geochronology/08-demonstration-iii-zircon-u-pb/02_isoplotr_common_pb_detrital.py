#!/usr/bin/env python3
"""02 - General case (Whitepaper Fig 4): common-Pb screening/correction + detrital inheritance.
DATA: IsoplotR example datasets (Vermeesch 2018, Geosci. Front. 9:1479; github.com/pvermees/IsoplotR).
Clones the repo into ./IsoplotR if absent (needs git+internet)."""
import os, subprocess, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
INST="IsoplotR/inst"
if not os.path.isdir(INST):
    subprocess.run(["git","clone","--depth","1","https://github.com/pvermees/IsoplotR"],check=True)
L8,L5,U=1.55125e-10,9.8485e-10,137.818
t6=lambda r: np.log1p(r)/L8/1e6; t7=lambda r: np.log1p(r)/L5/1e6
d1=pd.read_csv(INST+"/UPb1.csv"); d4=pd.read_csv(INST+"/UPb4.csv"); dz=pd.read_csv(INST+"/DZ.csv")
a6,a7=t6(d1.Pb206U238.values),t7(d1.Pb207U235.values)
print("clean UPb1: %.0f/%.0f Ma, disc %.1f%% -> concordant"%(a6.mean(),a7.mean(),100*np.mean(abs(1-a6/a7))))
r75,r68,r48=d4.Pb207U235.values,d4.Pb206U238.values,d4.Pb204U238.values
raw6,raw7=t6(r68),t7(r75); c64,c74=18.0,15.6   # ASSUMED Stacey-Kramers-type common Pb
cor6,cor7=t6(r68-r48*c64),t7(r75-r48*U*c74)
print("UPb4 RAW: %.0f/%.0f Ma, disc %.0f%%"%(raw6.mean(),raw7.mean(),100*np.mean(1-raw6/raw7)))
print("UPb4 204Pb-corrected: ~%.0f Ma, disc %.1f%% (concordant). NOTE depends on assumed common-Pb."%(cor6.mean(),100*np.mean(abs(1-cor6/cor7))))
ages=np.sort(dz["N1"].dropna().values)
print("detrital N1: n=%d %.0f-%.0f Ma; youngest %.0f, youngest-3 %.0f Ma = MAX depo age"%(len(ages),ages.min(),ages.max(),ages[0],ages[:3].mean()))
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13,5.2)); tt=np.linspace(1e6,1.5e9,400)
ax1.plot(np.expm1(L5*tt),np.expm1(L8*tt),'k-',lw=1.3)
ax1.scatter(d1.Pb207U235,d1.Pb206U238,c='#2c7fb8',s=42,label='clean (concordant)',edgecolor='k',lw=.4)
ax1.scatter(r75,r68,c='#d95f0e',s=42,marker='s',label='204Pb RAW (discordant)',edgecolor='k',lw=.4)
ax1.scatter(r75-r48*U*c74,r68-r48*c64,c='#31a354',s=42,marker='^',label='204Pb-corrected',edgecolor='k',lw=.4)
ax1.set_xlabel('207Pb/235U'); ax1.set_ylabel('206Pb/238U'); ax1.set_xlim(-.1,3.2); ax1.set_ylim(0,.09)
ax1.legend(fontsize=7.5); ax1.set_title('common-Pb screening & correction (real grains)')
ax2.hist(ages,bins=24,color='#bdbdbd',edgecolor='k',lw=.4); ax2.axvline(ages[0],color='#31a354',lw=2,label='youngest %.0f Ma'%ages[0])
ax2.axvline(ages[:3].mean(),color='#006d2c',lw=1.5,ls='--',label='youngest-3 (max depo age)')
ax2.set_xlabel('206Pb/238U age (Ma)'); ax2.set_ylabel('grains'); ax2.legend(fontsize=8); ax2.set_title('detrital inheritance (real)')
plt.tight_layout(); plt.savefig("fig4_isoplotr_common_pb_detrital.png",dpi=140); print("wrote fig4_isoplotr_common_pb_detrital.png")
