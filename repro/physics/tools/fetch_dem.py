import urllib.request, urllib.parse, json, time, math, sys
import numpy as np

# 강한 기복 지역: Pikes Peak 정상 (동쪽으로 ~2km 급강하, 서쪽 산악)
LAT0, LON0, NAME = 38.8405, -105.0442, "Pikes Peak"
HALF_KM = 4.0          # ±4 km
STEP_M  = 250.0        # 250 m 격자
n = int(2*HALF_KM*1000/STEP_M)+1   # 33
print(f"중심={NAME} ({LAT0},{LON0}), 격자 {n}x{n}, 간격 {STEP_M}m, 범위 ±{HALF_KM}km")

m_per_deg_lat = 111320.0
m_per_deg_lon = 111320.0*math.cos(math.radians(LAT0))
xs = np.linspace(-HALF_KM*1000, HALF_KM*1000, n)   # meters east
ys = np.linspace(-HALF_KM*1000, HALF_KM*1000, n)   # meters north

pts=[]
for j,yy in enumerate(ys):
    for i,xx in enumerate(xs):
        lat = LAT0 + yy/m_per_deg_lat
        lon = LON0 + xx/m_per_deg_lon
        pts.append((j,i,lat,lon))

def fetch_batch(batch):
    locs="|".join(f"{lat:.6f},{lon:.6f}" for _,_,lat,lon in batch)
    url="https://api.opentopodata.org/v1/srtm30m?locations="+urllib.parse.quote(locs)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                d=json.load(r)
            if d.get("status")=="OK":
                return [res["elevation"] for res in d["results"]]
        except Exception as e:
            print(f"  재시도 {attempt+1}: {e}", file=sys.stderr); time.sleep(2)
    return [None]*len(batch)

Z=np.full((n,n), np.nan)
B=100
ok=0
for k in range(0,len(pts),B):
    batch=pts[k:k+B]
    elevs=fetch_batch(batch)
    for (j,i,_,_),e in zip(batch,elevs):
        if e is not None: Z[j,i]=e; ok+=1
    print(f"  배치 {k//B+1}/{(len(pts)+B-1)//B}  누적 {ok}/{len(pts)}")
    time.sleep(1.1)   # rate limit 1/sec

print(f"수집 완료: {ok}/{len(pts)} 유효, 결측 {np.isnan(Z).sum()}")
print(f"고도 범위: {np.nanmin(Z):.0f} ~ {np.nanmax(Z):.0f} m, 중심 z0={Z[n//2,n//2]:.0f} m")
np.save("dem_Z.npy", Z)
np.save("dem_xs.npy", xs); np.save("dem_ys.npy", ys)
with open("dem_meta.json","w") as f:
    json.dump(dict(name=NAME,lat0=LAT0,lon0=LON0,step_m=STEP_M,n=n,
                   zmin=float(np.nanmin(Z)),zmax=float(np.nanmax(Z)),
                   z0=float(Z[n//2,n//2])),f)
print("저장: dem_Z.npy")
