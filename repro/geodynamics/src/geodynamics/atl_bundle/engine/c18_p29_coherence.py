"""
c18_p29_coherence.py  --  P29 사건-창 일치도: 올바른 귀무 + look-elsewhere + N_eff + jackknife
================================================================================
목적 (신뢰도 강화, 옵션 ⓑ):
  r17 에서 P29 는 'PASS(evidence-eligible)'로 표기됐으나 (i) 번들에 엔진/데이터가
  없고, (ii) 본문이 정의한 귀무("t_i 를 proxy_class 보존하며 치환")는 *코히런스/군집*
  주장에 대해 잘못된 귀무를 검정한다 --- 관측된 시간들의 '퍼짐'을 고정한 채 짝만
  섞으므로, "이 군집이 우연보다 더 좁은가?"를 답하지 못한다. 또한 look-elsewhere
  (다중창 탐색) 보정과 proxy 비독립성(AR-32) 보정이 없다.

  이 엔진은 그것을 *올바르게* 구현한다:
   (1) RANGE NULL  : 각 t_i 를 사전등록된 허용 구간에서 균일추출 -> K 분포 -> p_raw.
   (2) LOOK-ELSEWHERE: p_LEE = 1-(1-p_raw)^{N_LEE}, N_LEE=range/window.
   (3) N_eff        : 같은 proxy_class/age-model 하향 -> 유효 독립 프록시 수 N_eff<N.
   (4) JACKKNIFE    : leave-one-proxy-out -> 최악(가장 비유의) p 로 '특정 모듈 의존' 검정.

판정: UNLOCK 은 (p_LEE<0.05) AND (N_classes>=3) AND (jackknife 최악 p<0.05) AND (부호일치 S>=0.8)
      AND (K<=K_unlock) 를 모두 만족할 때만. PASS 는 *데이터*가 정한다.
데이터: data/meta/event_window_estimates.csv 가 있으면 사용. 없으면 ILLUSTRATIVE(합성).
Pure numpy. Deterministic (seeded).
"""
import numpy as np, os, csv

rng = np.random.default_rng(20260605)
HERE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(HERE, "..", "data", "meta", "event_window_estimates.csv")

# ---- pre-registered constants (lock in config/constraints.yml) ----
RANGE_LO, RANGE_HI = 0.0, 11.7
WINDOW_W           = 0.5
K_UNLOCK           = 0.75
SIGN_MIN           = 0.80
NCLASS_MIN         = 3
R_WITHIN_CLASS     = 0.6
M_NULL             = 200000

# ---- illustrative dataset (CLEARLY SYNTHETIC; replace with prereg CSV) ----
ILLUSTRATIVE = [
    # module, proxy_class, t_center_ka, sigma_ka, sign
    # (realistic Holocene scatter so the look-elsewhere penalty is visible)
    ("P19_sealevel", "sea_level",   4.05, 0.45, +1),
    ("P16_d18O",     "isotope",     4.55, 0.50, +1),
    ("P16_AMOC",     "circulation", 3.75, 0.55, +1),
    ("P24_endorheic","hydrology",   4.80, 0.55, +1),
    ("P20_misfitR",  "hydrology",   3.95, 0.60, +1),  # shares class -> N_eff<N
    ("P20_delta",    "sediment",    4.45, 0.50, +1),
]

def load():
    if os.path.exists(CSV):
        rows=[]
        with open(CSV) as f:
            for r in csv.DictReader(f):
                if str(r.get("include","1")).strip() in ("1","true","True"):
                    rows.append((r["module"], r["proxy_class"], float(r["t_center_ka"]),
                                 float(r["sigma_ka"]), int(float(r.get("sign",0)))))
        return rows, False
    return ILLUSTRATIVE, True

def K_joint(t, sig):
    w = 1.0/np.asarray(sig)**2
    tb = np.sum(w*t)/np.sum(w)
    spread = np.sqrt(np.sum(w*(t-tb)**2)/np.sum(w))
    return spread/np.median(sig)

def neff(classes):
    out=0.0
    for c in set(classes):
        m=classes.count(c)
        out += 1.0 + (m-1)*(1.0-R_WITHIN_CLASS)
    return out

rows, illustrative = load()
mod   = [r[0] for r in rows]
cls   = [r[1] for r in rows]
t     = np.array([r[2] for r in rows], float)
sig   = np.array([r[3] for r in rows], float)
sign  = np.array([r[4] for r in rows], int)
N     = len(rows)

print("="*86)
print("C-18  P29 EVENT-WINDOW COHERENCE  (corrected null + look-elsewhere + N_eff + jackknife)")
print("="*86)
print(f"  DATA SOURCE: {'ILLUSTRATIVE synthetic set (NOT a real verdict)' if illustrative else CSV}")
print(f"  proxies N={N};  distinct proxy_class = {len(set(cls))} ({sorted(set(cls))})")

Kobs = K_joint(t, sig)
nz   = sign[sign!=0]
S    = np.mean(nz==np.sign(np.sum(nz))) if len(nz) else float('nan')
Neff = neff(cls)
print(f"\n[obs] K_joint = {Kobs:.3f}   sign-coherence S = {S:.2f}   N_eff = {Neff:.2f}")

# (1) RANGE NULL
sims = rng.uniform(RANGE_LO, RANGE_HI, size=(M_NULL, N))
w = 1.0/sig**2
tb = (sims*w).sum(1)/w.sum()
spread = np.sqrt(((w*(sims-tb[:,None])**2).sum(1))/w.sum())
Ksim = spread/np.median(sig)
p_raw = (Ksim <= Kobs).mean()
print(f"\n[1] RANGE NULL (draw t_i ~ U[{RANGE_LO},{RANGE_HI}] ka): p_raw = P(K_sim <= K_obs) = {p_raw:.4g}")
print(f"    (the paper's value-permutation null is INVALID here: permuting t_i preserves the")
print(f"     observed spread, so it cannot test clustering. This range null is the right test.)")

# (2) LOOK-ELSEWHERE
N_LEE = max(1.0, (RANGE_HI-RANGE_LO)/WINDOW_W)
p_LEE = 1.0-(1.0-p_raw)**N_LEE
print(f"\n[2] LOOK-ELSEWHERE: {int(N_LEE)} independent windows of width {WINDOW_W} ka over the range")
print(f"    p_LEE = 1-(1-p_raw)^{int(N_LEE)} = {p_LEE:.4g}   (penalty factor ~{p_LEE/max(p_raw,1e-12):.0f}x)")

# (3) N_eff gate
nclass = len(set(cls))
print(f"\n[3] INDEPENDENCE: distinct proxy_class = {nclass} (need >= {NCLASS_MIN}); "
      f"N_eff = {Neff:.2f} of N={N} (same-class down-weighted, r={R_WITHIN_CLASS})")

# (4) JACKKNIFE
worst_p = 0.0; worst_mod=None
for i in range(N):
    keep=[j for j in range(N) if j!=i]
    Kj=K_joint(t[keep], sig[keep])
    tbk=(sims[:,keep]*w[keep]).sum(1)/w[keep].sum()
    spk=np.sqrt(((w[keep]*(sims[:,keep]-tbk[:,None])**2).sum(1))/w[keep].sum())
    Ksk=spk/np.median(sig[keep])
    pj=(Ksk<=Kj).mean(); pj_lee=1.0-(1.0-pj)**N_LEE
    if pj_lee>worst_p: worst_p, worst_mod = pj_lee, mod[i]
print(f"\n[4] JACKKNIFE (leave-one-out): worst-case p_LEE = {worst_p:.4g} "
      f"(dropping '{worst_mod}')  -- tests dependence on any single module")

unlock = (p_LEE<0.05) and (nclass>=NCLASS_MIN) and (worst_p<0.05) and (S>=SIGN_MIN) and (Kobs<=K_UNLOCK)
verdict = "UNLOCK" if unlock else "HOLD"
print("\n[VERDICT]")
print("-"*86)
print(f"  UNLOCK requires ALL of: p_LEE<0.05 ({p_LEE<0.05}); proxy_class>=3 ({nclass>=NCLASS_MIN}); "
      f"jackknife worst p<0.05 ({worst_p<0.05}); S>={SIGN_MIN} ({S>=SIGN_MIN}); K<={K_UNLOCK} ({Kobs<=K_UNLOCK})")
print(f"  => P29 method verdict on THIS data: {verdict}")
if illustrative:
    print("  *** This is ILLUSTRATIVE data. The real P29 verdict is HOLD until the pre-registered")
    print("      data/meta/event_window_estimates.csv is supplied and run through this engine. ***")

np.savez("c18_p29_coherence_results.npz",
         K_obs=Kobs, S=S, N=N, N_eff=Neff, nclass=nclass,
         p_raw=p_raw, N_LEE=N_LEE, p_LEE=p_LEE, jackknife_worst_p=worst_p,
         illustrative=illustrative, unlock=unlock)
print("\nsaved -> c18_p29_coherence_results.npz")
print(f"  AUDIT: p_raw={p_raw:.3g} -> p_LEE={p_LEE:.3g} (LEE x{int(N_LEE)}); "
      f"N_eff={Neff:.2f}<=N={N}; jackknife worst p={worst_p:.3g}; illustrative={illustrative}")
