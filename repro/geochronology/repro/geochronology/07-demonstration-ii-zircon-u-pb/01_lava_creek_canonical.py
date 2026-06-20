#!/usr/bin/env python3
"""01 - Canonical Lava Creek zircon result (Whitepaper Fig 3).
DATA: Matthews, Vazquez & Calvert (2015), G-cubed 16:2508, doi:10.1002/2015GC005881,
Supporting Information 'Dataset S1' zircon U-Pb file
ggge20775-sup-0002-2015gc005881-dss1.xls (free from publisher SI).
Put it in ./data/ (any *dss1*.xls) or pass its path as arg1.
Classification is by CRYSTAL POSITION (age-independent), not by age."""
import sys, glob, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
def find():
    if len(sys.argv)>1: return sys.argv[1]
    c=glob.glob("data/*dss1*.xls")+glob.glob("*dss1*.xls")
    if not c: sys.exit("ERROR: dss1 .xls not found (see README).")
    return c[0]
f=find(); raw=pd.read_excel(f,engine="xlrd",header=None)
D=raw.iloc[2:187].copy(); D.columns=range(raw.shape[1])
D["type"]=D[24].astype(str); D["date"]=pd.to_numeric(D[22],errors="coerce")
D["err"]=pd.to_numeric(D[23],errors="coerce"); D["fcom"]=pd.to_numeric(D[5],errors="coerce")
D=D.dropna(subset=["date","err"]); D=D[D.err>0]
def wm(s): w=1/s.err**2; return (s.date*w).sum()/w.sum(), np.sqrt(1/w.sum())
g=lambda rx: D[D.type.str.contains(rx,regex=True)]
rims,cores,iz,ebt=g("LCT-. zr xl face"),g("LCT-. zr core"),g("LCT-. zr inter zone"),g("EBT")
print("data:", f, "  median common-206Pb(LCT) = %.1f pct" % D[~D.type.str.contains("EBT")].fcom.median())
for n,gg in [("faces (autocryst)",rims),("cores (antecryst)",cores),("inter-zone",iz),("EBT [other]",ebt)]:
    m,se=wm(gg); print("  %-22s n=%3d  %6.1f +/- %.1f ka"%(n,len(gg),m,se))
mr,_=wm(rims); print("\nEruption (faces) = %.1f ka  [pub rim 626.5; eruption ~631; MIS16-15 ~630]"%mr)
assert abs(mr-626.5)<3; print("OK: reproduces published rim age.")
fig,ax=plt.subplots(figsize=(9.2,5)); b=np.arange(540,840,12)
ax.hist(cores.date,bins=b,color='#d95f0e',alpha=.75,label='cores/antecryst (n=%d)'%len(cores),edgecolor='k',lw=.3)
ax.hist(iz.date,bins=b,color='#fec44f',alpha=.7,label='inter-zone (n=%d)'%len(iz),edgecolor='k',lw=.3)
ax.hist(rims.date,bins=b,color='#2c7fb8',alpha=.8,label='faces/autocryst (n=%d)'%len(rims),edgecolor='k',lw=.3)
ax.hist(ebt.date,bins=b,color='#969696',alpha=.6,label='EBT-other unit (n=%d)'%len(ebt),edgecolor='k',lw=.3)
ax.axvline(mr,color='#2c7fb8',lw=2.2); ax.set_xlabel('230Th-corr 206Pb/238U date (ka)'); ax.set_ylabel('analyses')
ax.set_title('Lava Creek real grains: rims->eruption, cores->antecrysts (by position, not age)'); ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig("fig3_lava_creek_canonical.png",dpi=140); print("wrote fig3_lava_creek_canonical.png")
