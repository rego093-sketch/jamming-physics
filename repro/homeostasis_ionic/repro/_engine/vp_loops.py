#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_loops.py  --  Mineral / Acid-Base / Electrolyte SETPOINT LOOPS on the R19 substrate.

This is the research core. Each homeostatic quantity (serum Ca, blood pH, bone reserve, Na/K, PO4) is a
DEFENDED ATTRACTOR of a multi-organ negative-feedback loop; no single organ owns it (loop quantity).

THE DEEP LAW (substrate -> control):  a homeostatic setpoint, linearized about its target, is an
Ornstein-Uhlenbeck process  dx/dt = -k (x - x*) + load + noise.  Its loop gain k sets:
   - disturbance-rejection error    err = load / k            (integral arm -> 0)
   - correction time-constant       tau = 1 / k
   - stationary variance            Var(x) = sigma^2 / (2 k)
and k is inherited from the node R19 switches: a deeper basin (barrier b(g)=g^2/4, MONOTONE in the
MEASURED gamma) holds the controlled state more firmly = larger disturbance-rejection stiffness. So the
setpoint VALUE is biology (cited [L]); the setpoint STABILITY (how tightly it is held, how fast a load is
cleared) is set by gamma. Disease = loop-gain DROP (k down: variance up, slow correction) / setpoint
DRIFT (x* moves: sensor mis-calibration) / ATTRACTOR-SHIFT (k below critical: regulation lost). [V].

GRADES (VP-SPEC C3): loop mechanism + disturbance rejection [V]; cited setpoints (Ca 2.4 mM, pH 7.4,
Winters slope, Na/K) [L]; absolute fluxes / transport maxima [O] (obstacle stated). gamma MEASURED, never
fitted. Determinism (C1): fixed seed; deterministic Euler; round-before-hash.
"""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal, settle, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

def _gammas():
    g=json.load(open(_GAMMA, encoding="utf-8"))["genes"]
    return {k:g[k]["gamma"] for k in g}

# ===========================================================================
# 0. SUBSTRATE -> LOOP STIFFNESS:  R19 basin stability vs measured gamma
# ===========================================================================
def basin_displacement(g, pulse=0.25, n=400, dt=0.02):
    """Peak excursion of a SETTLED R19 switch under a fixed transient perturbation drive. A deeper basin
    (larger barrier b=g^2/4, monotone in measured gamma) is displaced LESS = stiffer disturbance rejection."""
    s = settle(g, 0.0); s0 = s; maxd = 0.0
    for _ in range(n):
        s += dt*(g*s - s**3 + pulse); maxd = max(maxd, abs(s - s0))
    return maxd

def gain_law():
    """gamma sets node STABILITY: barrier b=gamma^2/4 (monotone increasing) is the disturbance-rejection
    stiffness. Demonstrated: peak displacement under a fixed perturbation pulse DECREASES monotonically with
    measured gamma (stiffer basin = tighter hold); the OU loop stiffness k inherits this. [V] monotone
    (simulation); absolute k-scale [O]. Honest trade-off: small-signal comparator slope ~1/gamma moves
    oppositely, so gamma tunes the sensitivity/stability balance (stated, not hidden)."""
    seed_everything(); G=_gammas()
    rows=sorted(((sym, G[sym], round(barrier(G[sym]),6), round(basin_displacement(G[sym]),6)) for sym in G),
                key=lambda r: r[1])
    barr=[r[2] for r in rows]; disp=[r[3] for r in rows]
    barr_mono=all(barr[i] <= barr[i+1]+1e-12 for i in range(len(barr)-1))
    disp_mono=all(disp[i] >= disp[i+1]-1e-9 for i in range(len(disp)-1))
    return dict(by_gamma_ascending=[dict(master=r[0], gamma=r[1], barrier=r[2], pulse_displacement=r[3]) for r in rows],
                barrier_monotone_increasing_in_gamma=bool(barr_mono),
                displacement_monotone_decreasing_in_gamma=bool(disp_mono),
                claim="higher measured gamma -> deeper R19 basin (barrier g^2/4) -> smaller perturbation displacement -> larger loop stiffness k",
                grade_mechanism="[V]", grade_absolute="[O] (absolute gain scale needs calibration)")

# ===========================================================================
# 1. OU SETPOINT STATISTICS:  loop gain k controls tightness + correction speed
# ===========================================================================
def ou_setpoint(k, sigma=0.3, T=4000.0, dt=0.01, load=0.0, integral=0.0, seed=19):
    """Closed loop dx/dt = -k(x-x*) - I*z + load + noise ; dz/dt = x-x* (integral arm)."""
    rng=np.random.default_rng(seed); n=int(T/dt); x=0.0; z=0.0; xs=np.empty(n)
    for i in range(n):
        x += dt*(-k*x - integral*z + load) + sigma*math.sqrt(dt)*rng.standard_normal(); z += dt*x; xs[i]=x
    xss=xs[n//4:]
    return dict(mean_offset=round(float(np.mean(xss)),5), variance=round(float(np.var(xss)),6))

def ou_law():
    """Confirm the OU laws across a gain sweep: Var*2k/sigma^2 ~ 1 ; step error = load/k. [V]."""
    seed_everything(); sigma=0.3; sweep=[]
    for k in (0.5,1.0,2.0,4.0):
        st=ou_setpoint(k, sigma=sigma, load=0.0)
        var_law=st["variance"]*2*k/(sigma**2)
        det=ou_setpoint(k, sigma=0.0, load=1.0, integral=0.0)
        err_law=det["mean_offset"]*k
        sweep.append(dict(k=k, var_x=st["variance"], var_times_2k_over_sigma2=round(var_law,3),
                          step_error=det["mean_offset"], error_times_k=round(err_law,3)))
    var_ok=all(0.7 <= s["var_times_2k_over_sigma2"] <= 1.3 for s in sweep)
    err_ok=all(0.97 <= s["error_times_k"] <= 1.03 for s in sweep)
    integ=ou_setpoint(1.0, sigma=0.0, load=1.0, integral=0.5)
    return dict(sweep=sweep, variance_law_Var_eq_sigma2_over_2k=bool(var_ok),
                rejection_law_err_eq_load_over_k=bool(err_ok),
                integral_arm_zeroes_steady_error=bool(abs(integ["mean_offset"])<0.05),
                grade="[V] (OU control laws reproduced); setpoint VALUE cited [L]")

# ===========================================================================
# RI1  CALCIUM SETPOINT  (PTH<->vitD<->bone<->kidney<->gut; CaSR comparator)
# ===========================================================================
def pth_curve(ca, ca_sp=1.0, m=3.0, pmin=0.1, pmax=1.0):
    """Brown four-parameter inverse-sigmoid PTH(Ca). ca in units of the setpoint (ca_sp=1).
    m (Hill slope) is the CaSR comparator steepness; ca_sp is the defended setpoint (cited [L])."""
    return pmin + (pmax-pmin)/(1.0+(ca/ca_sp)**m)

def ri1_calcium():
    """Inject a Ca load (+) then a Ca deficit (-); the loop returns serum Ca to setpoint (=1). PTH
    suppressed by load, raised by deficit (the four-parameter curve). [V] correction; setpoint [L]."""
    seed_everything()
    ca_sp=1.0; m=3.0; g_eff=2.0; clr=2.0; tau_vd=40.0; P0=pth_curve(1.0,ca_sp,m)
    def run(load_fn, T=400.0, dt=0.02):
        ca=1.0; vd=0.0; n=int(T/dt); tr=[]
        for i in range(n):
            t=i*dt; P=pth_curve(ca, ca_sp, m)
            dca=g_eff*(P-P0)+0.5*vd-clr*(ca-1.0)+load_fn(t); dvd=((P-P0)-vd)/tau_vd
            ca+=dt*dca; vd+=dt*dvd; tr.append(ca)
        return np.array(tr)
    load=lambda t:(3.0 if 50<=t<80 else 0.0)+(-3.0 if 200<=t<230 else 0.0)
    tr=run(load); dt=0.02
    peak_hi=float(tr[int(50/dt):int(120/dt)].max()); peak_lo=float(tr[int(200/dt):int(280/dt)].min())
    recover=float(tr[-1]); corrected=abs(recover-1.0)<0.03 and peak_hi>1.0 and peak_lo<1.0
    return dict(setpoint=1.0, returns_to_setpoint=bool(corrected),
                ca_peak_on_load=round(peak_hi,4), ca_nadir_on_deficit=round(peak_lo,4), ca_final=round(recover,4),
                pth_when_high=round(pth_curve(peak_hi),4), pth_when_low=round(pth_curve(peak_lo),4),
                pth_suppressed_by_load=bool(pth_curve(peak_hi)<P0), pth_raised_by_deficit=bool(pth_curve(peak_lo)>P0),
                anchor="ionized Ca setpoint ~1.2 mM (total ~2.4 mM); Brown inverse-sigmoid PTH(Ca), Hill m~3 set by CaSR",
                grade="[V] load/deficit corrected to setpoint; setpoint + curve cited [L]")

# ===========================================================================
# RI2  ACID-BASE  (two-timescale: respiratory CO2 fast + renal HCO3 slow)
# ===========================================================================
def ph_hh(hco3, pco2):
    """Henderson-Hasselbalch: pH = 6.1 + log10(HCO3 / (0.03*pCO2))."""
    return 6.1 + math.log10(hco3/(0.03*pco2))

def ri2_acidbase():
    """Metabolic acid load (HCO3 24->14). FAST respiratory drop of pCO2 (partial; compensation slope ~
    Winters 1.2) then SLOW renal HCO3 regeneration restores pH to 7.4 with pCO2->40. Two-timescale buffer.
    The respiratory target pCO2 = 40*(HCO3/24)^0.6 gives Winters-like partial compensation acutely AND exact
    return to normal once HCO3 recovers. [V] two-timescale; pH 7.4 + Winters slope cited [L]."""
    seed_everything()
    HCO3_0=24.0; PCO2_0=40.0; pH_target=ph_hh(HCO3_0,PCO2_0); HCO3=14.0
    pH_acute=ph_hh(HCO3,PCO2_0)
    tau_resp=1.0; tau_renal=60.0; dt=0.05; T=800.0; n=int(T/dt)
    pco2=PCO2_0; hco3=HCO3; series=[]
    for i in range(n):
        pco2_star=40.0*(hco3/24.0)**0.6                 # respiratory controller (partial, Winters-like)
        pco2 += dt*(pco2_star-pco2)/tau_resp
        hco3 += dt*(HCO3_0-hco3)/tau_renal              # slow renal HCO3 regeneration toward 24
        series.append(ph_hh(hco3,pco2))
    pco2_comp=40.0*(HCO3/24.0)**0.6
    comp_slope=(PCO2_0-pco2_comp)/(HCO3_0-HCO3)
    pH_after_fast=ph_hh(HCO3, pco2_comp); pH_final=series[-1]
    two_timescale=(pH_acute < pH_after_fast < pH_final) and abs(pH_final-pH_target)<0.02
    return dict(pH_target=round(pH_target,3), pH_acute_acidemia=round(pH_acute,3),
                pH_after_fast_resp=round(pH_after_fast,3), pH_final=round(pH_final,3),
                respiratory_compensation_slope_dPCO2_dHCO3=round(comp_slope,3),
                winters_slope_match=bool(1.0 <= comp_slope <= 1.6), two_timescale_restored=bool(two_timescale),
                anchor="pH 7.4 = 6.1 + log10(24/(0.03*40)); Winters expected pCO2 = 1.5*HCO3 + 8 (slope ~1.2-1.5)",
                grade="[V] two-timescale correction; pH 7.4 + Winters slope cited [L]")

# ===========================================================================
# RI3  BONE RESERVOIR  (reservoir/setpoint trade-off -> osteoporosis mechanism)
# ===========================================================================
def ri3_bone_reservoir():
    """Sustained Ca demand: the loop HOLDS serum Ca at setpoint by WITHDRAWING from the bone reserve.
    Serum Ca stays ~setpoint while the reserve declines monotonically (the trade-off = osteoporosis
    substrate). [V] trade-off; absolute loss rate [O]/[L]."""
    seed_everything()
    m=3.0; g_eff=6.0; beta=2.0; clr=4.0; demand=0.3; formation=0.0008; kappa=0.05
    P0=pth_curve(1.0,1.0,m); ca=1.0; B=1.0; dt=0.05; T=2000.0; n=int(T/dt); tr_ca=[]; tr_B=[]
    for i in range(n):
        Pex=pth_curve(ca,1.0,m)-P0
        dca=g_eff*Pex + beta*Pex - clr*(ca-1.0) - demand        # PTH effector + bone release defend Ca
        resorption=kappa*max(Pex,0.0)                            # PTH-excess withdraws from reserve
        dB=formation - resorption
        ca+=dt*dca; B=max(B+dt*dB,0.0); tr_ca.append(ca); tr_B.append(B)
    ca=np.array(tr_ca); B=np.array(tr_B)
    ca_dev=float(np.max(np.abs(ca[int(200/dt):]-1.0)))
    B_depleted=bool(B[-1] < B[0]-0.1) and bool(np.all(np.diff(B[::400]) <= 1e-6))
    return dict(serum_ca_max_deviation=round(ca_dev,4), serum_ca_held_at_setpoint=bool(ca_dev<0.06),
                bone_reserve_start=round(float(B[0]),3), bone_reserve_end=round(float(B[-1]),3),
                reservoir_monotonically_depleted=B_depleted,
                interpretation="chronic demand is paid by the bone reservoir while serum Ca is defended = osteoporosis substrate",
                anchor="bone-density loss vs cited post-menopausal/age rates [L]; reservoir depletion [V]",
                grade="[V] reservoir/setpoint trade-off; absolute loss rate [O]/[L]")

# ===========================================================================
# RI4  ELECTROLYTE  (Na/K setpoints; Na<->volume<->pressure CITED to hemodynamic)
# ===========================================================================
def ri4_electrolyte():
    """Na and K loads corrected by renal handling. Na<->volume<->pressure coupling is a CITED seam to
    homeostasis_hemodynamic (NOT re-emerged here). [V] loops; setpoints (Na~140, K~4.2 mM) [L]."""
    seed_everything()
    def loop(setp, kgain, win, T=300.0, dt=0.05):
        x=setp; n=int(T/dt); tr=[]
        for i in range(n):
            t=i*dt; load=(0.3*setp if win[0]<=t<win[1] else 0.0); x+=dt*(-kgain*(x-setp)+load); tr.append(x)
        return np.array(tr)
    na=loop(140.0,0.5,(40,70)); k=loop(4.2,0.6,(40,70))
    na_ok=abs(na[-1]-140.0)<2.0 and na[int(50/0.05):].max()>140.0
    k_ok=abs(k[-1]-4.2)<0.2 and k[int(50/0.05):].max()>4.2
    return dict(na_setpoint=140.0, na_final=round(float(na[-1]),2), na_corrected=bool(na_ok),
                k_setpoint=4.2, k_final=round(float(k[-1]),3), k_corrected=bool(k_ok),
                volume_pressure_coupling="CITED seam -> homeostasis_hemodynamic (pressure natriuresis); not re-emerged here",
                anchor="serum Na ~140 mM, K ~4.2 mM (cited)",
                grade="[V] renal correction of Na/K loads; setpoints cited [L]; volume<->pressure = hemodynamic seam")

# ===========================================================================
# RI5  PHOSPHATE  (FGF23 lowering arm; Ca x PO4 product held below precipitation)
# ===========================================================================
def ri5_phosphate():
    """PO4 load raises FGF23 (osteocyte arm) -> phosphaturia -> PO4 falls (negative feedback); the FGF23
    arm keeps the Ca x PO4 product below a precipitation threshold. [V] mechanism; absolute TmP/GFR [O]."""
    seed_everything()
    po4=1.0; fgf=0.0; ca=1.0; dt=0.05; T=400.0; n=int(T/dt); tau_f=12.0; precip=1.6
    tr_po4=[]; tr_fgf=[]; prod=[]
    for i in range(n):
        t=i*dt; intake=(0.3 if 40<=t<120 else 0.0)
        excretion=0.6*po4 + 0.8*max(fgf,0.0)
        dpo4=intake - excretion + 0.6; dfgf=(0.9*(po4-1.0)-fgf)/tau_f
        po4+=dt*dpo4; fgf+=dt*dfgf; tr_po4.append(po4); tr_fgf.append(fgf); prod.append(ca*po4)
    po4=np.array(tr_po4); fgf=np.array(tr_fgf); prod=np.array(prod)
    return dict(po4_setpoint=1.0, po4_final=round(float(po4[-1]),4), po4_load_corrected=bool(abs(po4[-1]-1.0)<0.1),
                fgf23_rises_with_po4=bool(fgf[int(60/0.05):int(150/0.05)].max()>0.05),
                ca_po4_product_max=round(float(prod.max()),4), ca_po4_below_precipitation=bool(prod.max()<precip),
                anchor="Ca x PO4 product held below precipitation (vascular calcification / stone seam)",
                grade="[V] FGF23 negative-feedback lowering arm; absolute renal TmP/GFR now COMPUTED exactly "
                      "(Walton-Bijvoet, see renal_phosphate.py) -> residual [O] is only gamma->absolute-value (by design)")

# ===========================================================================
# battery wiring
# ===========================================================================
def run_loops():
    seed_everything()
    return {"gain_law":gain_law(), "ou_law":ou_law(), "RI1_calcium":ri1_calcium(),
            "RI2_acidbase":ri2_acidbase(), "RI3_bone_reservoir":ri3_bone_reservoir(),
            "RI4_electrolyte":ri4_electrolyte(), "RI5_phosphate":ri5_phosphate()}

def loop_pass():
    L=run_loops()
    checks={"gain_law":L["gain_law"]["barrier_monotone_increasing_in_gamma"] and L["gain_law"]["displacement_monotone_decreasing_in_gamma"],
            "ou_law":L["ou_law"]["variance_law_Var_eq_sigma2_over_2k"] and L["ou_law"]["rejection_law_err_eq_load_over_k"],
            "RI1":L["RI1_calcium"]["returns_to_setpoint"],
            "RI2":L["RI2_acidbase"]["two_timescale_restored"] and L["RI2_acidbase"]["winters_slope_match"],
            "RI3":L["RI3_bone_reservoir"]["serum_ca_held_at_setpoint"] and L["RI3_bone_reservoir"]["reservoir_monotonically_depleted"],
            "RI4":L["RI4_electrolyte"]["na_corrected"] and L["RI4_electrolyte"]["k_corrected"],
            "RI5":L["RI5_phosphate"]["po4_load_corrected"] and L["RI5_phosphate"]["fgf23_rises_with_po4"] and L["RI5_phosphate"]["ca_po4_below_precipitation"]}
    return checks, all(checks.values()), L

if __name__ == "__main__":
    checks, ok, L = loop_pass()
    print(json.dumps(L, ensure_ascii=False, indent=1)); print("\nchecks:", checks); print("ALL LOOPS PASS:", ok)
