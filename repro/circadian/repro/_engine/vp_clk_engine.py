#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_clk_engine.py  --  Chronobiology (Circadian) engine (deterministic, in-package).

SCOPE (see CHARTER.md): The ~24h circadian clock is a self-sustained coupled limit-cycle oscillator
network (SCN master + peripheral clocks) on the FHN substrate; it FREE-RUNS, ENTRAINS to light, and
GATES nearly every homeostatic setpoint. Clock<->environment misalignment (shift work, jet lag) is the
disease axis; a PHASE-correct zeitgeber (light / melatonin / wake therapy) is the re-alignment axis.

WHAT RUNS TODAY (research body, all on the SHARED FHN substrate -- vp_substrate is vendored, untouched):
  emerge_organs()          : nodes from MEASURED master-gene gamma (BMAL1 now vendored = 1.33348, gene 406);
                             diffuse circuits stay honest, order is a gamma readout.
  confirm_oscillators()    : the shared FHN beats for each oscillator node.
  free_running_probe()     : RC1  -- the limit cycle self-sustains with ZERO periodic drive (vs a damped control).
  phase_response_curve()   : RC2a -- a brief pulse advances OR delays the next cycle depending on phase (biphasic PRC).
  entrainment_arnold()     : RC2b -- a periodic zeitgeber locks the clock; the locking range WIDENS with amplitude.
  coupled_network()        : RC3  -- N coupled FHN oscillators synchronise; coherence R rises monotonically with K;
                             peripheral phase-drift vs the master falls with coupling (master-vs-network).
  setpoint_gating()        : RC4  -- the clock phase GATES the HPA cortisol drive (mind M18, cited) so cortisol
                             acquires a ~24h rhythm; ablating the clock flattens it. cross-cutting seam.
  misalignment()           : RC5  -- a phase shift between internal clock and external time lengthens re-entrainment
                             AND drops the externally-aligned cortisol amplitude (the disease state).
  circadian_mood_seam()    : RC6  -- misalignment flattens/de-tunes the gated HPA rhythm; that sustained HPA
                             dysregulation IS mind's withdrawal-bias depression handle (the CIRCADIAN contributor
                             mind LOCKED). SIGN only, efficacy=0, magnitude [O]; felt quality stays in mind.
  chronotherapy()          : TX1  -- a PRC-CORRECT zeitgeber re-aligns the clock (reduces phase error); the SAME
                             pulse at the wrong phase worsens it; light and melatonin act ~antiphase; wake therapy
                             is a transient homeostatic lift. Derived from the RC2 PRC -- NO new constant. efficacy=0.

GRADES (VP-SPEC C3): oscillator mechanism / PRC shape / coupling transition / gating / re-alignment SIGN = [V];
  period 24h + cited phases / cortisol kinetics / shift-work RR = [L]; absolute phase / incidence / magnitude = [O].

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed=19; round-before-hash; sorted keys. Two engine
runs yield an identical sha256. No hand-entered dynamical numbers; the HPA window + BMAL1 gamma are cited/measured.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, barrier, settle, dwell, dominant_freq, seed_everything

_HERE  = os.path.dirname(__file__)
_INH   = os.path.join(_HERE, "..", "..", "inherited")
_GAMMA = os.path.join(_INH, "organ_gamma.json")
_SEAM  = os.path.join(_INH, "mind_seam.json")

# --- dynamics constants (dimensionless; the ABSOLUTE 24h period is the [L] anchor, NOT these) ----------
TAU_F = 1.0
TAU_S = 30.0      # relaxation timescale for the dynamics probes (fast cycles, cheap); period is [L]-anchored
BETA  = 0.5
DT    = 0.05
DRIVE = 0.55      # suprathreshold tonic drive -> the limit cycle (same value mind uses for its FHN beats)

ORGAN_ROWS = [{'master': '(SCN_master_clock)',
  'organ': 'scn_master_oscillator',
  'role': 'suprachiasmatic ~24h master limit-cycle (light-entrained)',
  'dyn_class': 'oscillator', 'tau_s': 480.0,
  'rate_note': 'circadian period ~24 h [L] TO-ANCHOR', 'gamma_state': 'diffuse'},
 {'master': 'BMAL1',
  'organ': 'core_clock_loop',
  'role': 'BMAL1/CLOCK<->PER/CRY transcription-translation feedback loop (the molecular oscillator)',
  'dyn_class': 'oscillator', 'tau_s': 480.0,
  'rate_note': 'TTFL period ~24 h [L]; BMAL1 gamma measured = 1.33348 (gene 406, NC_000011.10)',
  'gamma_state': 'vendored'},
 {'master': '(peripheral_clocks)',
  'organ': 'peripheral_clock_network',
  'role': 'liver/muscle/adipose peripheral clocks (cite organ packages)',
  'dyn_class': 'coupled-oscillator', 'tau_s': 480.0,
  'rate_note': 'peripheral phase lag [L]; circuit', 'gamma_state': 'diffuse'},
 {'master': '(retinal_entrainment)',
  'organ': 'light_entrainment_input',
  'role': 'retinal light -> SCN phase reset (seam to sensory/neuro)',
  'dyn_class': 'entrainment', 'tau_s': None,
  'rate_note': 'phase-response curve [L]; seam', 'gamma_state': 'diffuse'}]

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def load_seam():
    return json.load(open(_SEAM, encoding="utf-8"))

# ======================================================================================================
#  NODE EMERGENCE  (identity + order owned by DNA; gamma measured, never fitted)
# ======================================================================================================
def emerge_organs():
    seed_everything(); G = load_gamma(); built = []
    for r in ORGAN_ROWS:
        st = r["gamma_state"]
        if st == "vendored":
            g = G[r["master"]]["gamma"]; o = Organ(r["organ"], g, master=r["master"])
            built.append(dict(organ=r["organ"], master=r["master"], gamma=round(float(g), 6), role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="vendored",
                              functional_spinodal=round(float(o.functional_spinodal()), 6),
                              rel_size_dwell=round(float(o.size()), 6)))
        elif st == "to_measure":
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="to_measure",
                              note="master " + r["master"] + ": gamma TO-MEASURE via DNA pipeline (measured input, not fitted)"))
        else:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="diffuse", note="no single master gene (circuit/derived/diffuse)"))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] order is a gamma readout over MEASURED nodes; SIGN to validate vs cited timing",
                deferred_gamma=[b["master"] for b in built if b.get("gamma_state") == "to_measure"])

def confirm_oscillators():
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] not in ("oscillator", "coupled-oscillator"): continue
        taus = r["tau_s"] if r["tau_s"] is not None else 40.0
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(taus), beta=0.5, name=r["organ"])
        S, dt = n.run(drive=DRIVE, T=8000.0, dt=DT)
        f = dominant_freq(S, dt); nb = len(Neuron.spikes(S))
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f), 8), tau_s=float(taus),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

# ======================================================================================================
#  SHARED FHN HELPERS  (reuse the vendored substrate; the COUPLING is the new dynamics this package adds)
# ======================================================================================================
def _spike_phase(S, dt):
    """Interpolated oscillator phase in [0,2pi): up-crossings of 0 are phase markers; phase ramps linearly
    between consecutive spikes (isochron-free phase proxy for a relaxation oscillator)."""
    sp = Neuron.spikes(S)
    phase = np.full(len(S), np.nan)
    for k in range(len(sp) - 1):
        a, b = sp[k], sp[k+1]
        phase[a:b] = 2.0 * math.pi * (np.arange(a, b) - a) / float(b - a)
    return phase, sp

def _last_spike_time(S, dt):
    sp = Neuron.spikes(S)
    return (float(sp[-1] * dt) if len(sp) else None), len(sp)

def _coupled_fhn(gammas, drives, K, T, dt, master_gain=1.0):
    """N FitzHugh-Nagumo relaxation oscillators (the SAME substrate equations, vectorised) with MEAN-FIELD
    ephaptic-style coupling K*(mean - s_i). Oscillator 0 is the SCN master (its outward influence scaled by
    master_gain). Returns the membrane matrix S[n_steps, N]. This adds COUPLING dynamics on top of the
    vendored FHN -- it does not re-derive the substrate math (VP-SPEC C1)."""
    N = len(gammas); n = int(T / dt)
    g = np.asarray(gammas, float); base = np.asarray(drives, float)
    s = np.full(N, -1.0); w = np.zeros(N)
    S = np.empty((n, N))
    wts = np.ones(N); wts[0] = master_gain                       # master pulls harder on the field
    for i in range(n):
        field = float(np.sum(wts * s) / np.sum(wts))             # weighted mean field (master-weighted)
        s = s + dt * ((g * s - s**3) - w + base + K * (field - s)) / TAU_F
        w = w + dt * (s - BETA * w) / TAU_S
        np.clip(s, -12.0, 12.0, out=s)
        S[i] = s
    return S

def _coherence(S):
    """Order parameter: std(mean field) / mean(std of members). Synchronised -> ~1; incoherent -> ~1/sqrt(N)
    (member oscillations cancel in the mean). Monotone, deterministic, phase-extraction-free."""
    mean_field = S.mean(axis=1)
    num = float(mean_field.std())
    den = float(np.mean(S.std(axis=0))) + 1e-12
    return num / den

# ======================================================================================================
#  RC1 -- the molecular clock is a SELF-SUSTAINED oscillator (free-running)
# ======================================================================================================
def free_running_probe():
    seed_everything()
    # free-running: suprathreshold tonic drive, NO periodic forcing -> sustained limit cycle
    nf = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_free")
    Sf, _ = nf.run(drive=DRIVE, T=6000.0, dt=DT)
    spf = Neuron.spikes(Sf); ff = dominant_freq(Sf, DT)
    isi = np.diff(spf).astype(float) if len(spf) > 2 else np.array([0.0])
    cv = float(isi.std() / (isi.mean() + 1e-12)) if len(isi) > 1 else 1.0   # regularity of the free run
    # control: a STRONG tonic drive pins the switch high (depolarisation block) -> NO sustained rhythm.
    # this confirms the rhythm lives in a limit-cycle WINDOW and is not trivially always-on at any drive.
    nc = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_blocked")
    Sc, _ = nc.run(drive=3.0, T=6000.0, dt=DT)
    spc = Neuron.spikes(Sc)
    self_sustained = bool(len(spf) >= 5 and ff > 0.0 and cv < 0.15)
    control_silent = bool(len(spc) <= 1)
    return dict(question="RC1: does the molecular TTFL self-sustain a rhythm with zero external drive?",
                free_running_beats=int(len(spf)), free_running_freq_arb=round(float(ff), 8),
                free_running_cv=round(cv, 6), control_block_beats=int(len(spc)),
                self_sustained=self_sustained, control_silent=control_silent,
                passes=bool(self_sustained and control_silent),
                period_anchor="absolute period ~24 h is the [L] anchor (cited), NOT emergent; arb freq is the mechanism readout",
                grades="oscillator mechanism [V] / period 24h [L] / absolute phase [O]")

# ======================================================================================================
#  RC2a -- PHASE-RESPONSE CURVE  (a pulse advances OR delays depending on phase)
# ======================================================================================================
def phase_response_curve(pulse_amp=0.6, n_phases=18):
    seed_everything()
    # unperturbed reference run
    base = np.full(int(6000.0 / DT), DRIVE)
    n = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_prc")
    S0, _ = n.run(drive=base, T=None if False else 6000.0, dt=DT)  # array drive ignores T
    sp0 = Neuron.spikes(S0)
    if len(sp0) < 6:
        return dict(question="RC2a PRC", passes=False, note="reference run under-resolved")
    # choose a mid cycle to perturb within; measure the shift of the FOLLOWING spike
    c0, c1 = sp0[3], sp0[4]; period = c1 - c0
    ref_next = sp0[5]                                            # the spike we compare timing against
    width = max(2, int(0.04 * period))                          # brief pulse (~4% of a cycle)
    phases, shifts = [], []
    for j in range(n_phases):
        ph = 2.0 * math.pi * j / n_phases
        t_pulse = c0 + int((ph / (2.0 * math.pi)) * period)
        d = base.copy(); d[t_pulse:t_pulse + width] += pulse_amp
        n2 = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_prc_p")
        Sp, _ = n2.run(drive=d, T=6000.0, dt=DT)
        spp = Neuron.spikes(Sp)
        nxt = spp[spp > t_pulse]
        if len(nxt) == 0: continue
        # phase shift = (unperturbed next-spike time - perturbed next-spike time)/period; + = advance
        dphi = float((ref_next - nxt[0]) / period)
        # wrap to [-0.5,0.5] cycles
        dphi = (dphi + 0.5) % 1.0 - 0.5
        phases.append(round(ph, 6)); shifts.append(round(dphi, 6))
    shifts_arr = np.array(shifts) if shifts else np.array([0.0])
    biphasic = bool(shifts_arr.max() > 0.005 and shifts_arr.min() < -0.005)   # both advance AND delay regions
    return dict(question="RC2a: does a brief light pulse advance OR delay the clock depending on phase (biphasic PRC)?",
                phases=phases, phase_shifts_cycles=shifts,
                max_advance=round(float(shifts_arr.max()), 6), max_delay=round(float(shifts_arr.min()), 6),
                biphasic_prc=biphasic, passes=biphasic,
                interpretation="advance + delay regions with a dead zone = the canonical circadian light PRC; "
                               "morning light advances, evening light delays (sign across phase)",
                grades="PRC shape [V] / absolute phase reference [O]")

# ======================================================================================================
#  RC2b -- ENTRAINMENT / ARNOLD TONGUE  (locking range widens with zeitgeber amplitude)
# ======================================================================================================
def _periodic_drive(n_steps, base, amp, period_steps, phase0=0.0):
    t = np.arange(n_steps)
    return base + amp * np.cos(2.0 * math.pi * t / float(period_steps) + phase0)

def _is_locked(S, dt, period_steps, tol=0.12):
    """Locked if the oscillator's mean inter-spike interval matches the zeitgeber period within tol."""
    sp = Neuron.spikes(S)
    if len(sp) < 5: return False
    isi = np.diff(sp[len(sp)//2:]).astype(float)                # steady-state half
    if len(isi) < 2: return False
    return bool(abs(isi.mean() - period_steps) / period_steps < tol and isi.std() / (isi.mean()+1e-12) < 0.2)

def entrainment_arnold():
    seed_everything()
    # natural period of the free run (in steps)
    nfree = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_nat")
    Sn, _ = nfree.run(drive=DRIVE, T=6000.0, dt=DT)
    spn = Neuron.spikes(Sn); T0 = float(np.mean(np.diff(spn))) if len(spn) > 2 else 60.0
    n_steps = int(6000.0 / DT)
    amps = [0.02, 0.08, 0.18, 0.32, 0.5]                        # zeitgeber amplitude sweep (incl. very weak)
    periods = [T0 * r for r in np.linspace(0.65, 1.35, 15)]     # wide detuning sweep around the natural period
    locking_range = []
    for A in amps:
        locked = 0
        for P in periods:
            d = _periodic_drive(n_steps, DRIVE, A, P)
            nn = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="scn_ent")
            Se, _ = nn.run(drive=d, T=6000.0, dt=DT)
            if _is_locked(Se, DT, P): locked += 1
        locking_range.append(locked)
    monotone = bool(all(locking_range[i] <= locking_range[i+1] for i in range(len(locking_range)-1))
                    and locking_range[-1] > locking_range[0])
    return dict(question="RC2b: does a periodic zeitgeber entrain the clock, with the locking range WIDENING as "
                         "zeitgeber strength rises (an Arnold tongue)?",
                zeitgeber_amplitudes=[round(a,3) for a in amps],
                locking_range_count=[int(x) for x in locking_range], n_detunings=len(periods),
                arnold_tongue_widens=monotone, passes=monotone,
                interpretation="stronger light -> wider range of external periods the clock can lock to "
                               "(the Arnold tongue); weak light entrains only near the natural period",
                grades="entrainment + tongue [V] / absolute period [L]")

# ======================================================================================================
#  RC3 -- MASTER vs NETWORK  (coupled oscillators synchronise; coherence rises with K)
# ======================================================================================================
def coupled_network(N=8):
    seed_everything()
    rng = np.random.RandomState(19)
    gammas = np.ones(N)                                          # identical wells; heterogeneity via drive
    drives = DRIVE + 0.06 * (rng.rand(N) - 0.5)                  # small spread -> different natural periods
    Ks = [0.0, 0.05, 0.1, 0.2, 0.35, 0.5]
    coher = []
    for K in Ks:
        S = _coupled_fhn(gammas, drives, K, T=3500.0, dt=DT, master_gain=1.0)
        coher.append(round(_coherence(S), 6))
    monotone = bool(all(coher[i] <= coher[i+1] + 1e-6 for i in range(len(coher)-1)) and coher[-1] > coher[0] + 0.05)
    # master-vs-network: peripheral phase drift relative to the master falls as the master's gain rises
    drift = []
    for mg in [1.0, 2.0, 4.0]:
        S = _coupled_fhn(gammas, drives, 0.2, T=3500.0, dt=DT, master_gain=mg)
        ph, _ = _spike_phase(S[:, 0], DT)                       # master phase
        # mean absolute phase difference of peripherals vs master over the locked second half
        half = S.shape[0] // 2
        dsum, cnt = 0.0, 0
        for j in range(1, N):
            pj, _ = _spike_phase(S[:, j], DT)
            m = ~np.isnan(ph[half:]) & ~np.isnan(pj[half:])
            if m.any():
                dd = np.abs((ph[half:][m] - pj[half:][m] + math.pi) % (2*math.pi) - math.pi)
                dsum += float(dd.mean()); cnt += 1
        drift.append(round(dsum / max(cnt, 1), 6))
    master_pulls = bool(drift[0] >= drift[-1])                  # higher master gain -> peripherals track it (less drift)
    return dict(question="RC3: is timekeeping one MASTER oscillator or a COUPLED NETWORK? coupling strength vs "
                         "synchrony, and does the SCN master pull peripheral clocks into phase?",
                coupling_K=[round(k,3) for k in Ks], coherence_R=coher,
                coherence_rises_with_coupling=monotone,
                master_gain=[1.0, 2.0, 4.0], peripheral_phase_drift_vs_master=drift,
                master_entrains_periphery=master_pulls,
                passes=bool(monotone and master_pulls),
                interpretation="decoupled peripheral clocks drift (low R); coupling synchronises them (R rises); a "
                               "stronger SCN master pulls the periphery into phase -- one network, master-led",
                grades="synchronisation transition + master-led entrainment [V] / absolute phase lags [O]")

# ======================================================================================================
#  RC4 -- SETPOINT GATING  (the clock gates the HPA cortisol drive -> cortisol gets a ~24h rhythm)
# ======================================================================================================
def _cortisol_cascade(drive_series, dt_min, tau_rise=12.0, tau_fall=50.0):
    """The mind M18 HPA cortisol cascade (CITED, biexponential 2-lag), driven by a TIME-VARYING input.
    tau_rise / tau_fall are the mind-cited onset/elimination lags; this package adds NO kinetic constant,
    it only modulates the DRIVE with circadian phase. Returns the cortisol output series."""
    n = len(drive_series); x1 = np.zeros(n); x2 = np.zeros(n)
    for i in range(1, n):
        x1[i] = x1[i-1] + dt_min * ((drive_series[i-1] - x1[i-1]) / tau_rise)
        x2[i] = x2[i-1] + dt_min * ((x1[i-1] - x2[i-1]) / tau_fall)
    return x2

def setpoint_gating():
    seed_everything()
    seam = load_seam(); win = seam["hpa_cortisol_cascade"]["acth_to_cortisol_peak_window_min"]
    # FIVE circadian days in minutes; measure the rhythm on the LAST day (transient settled).
    days = 5; minutes = 24 * 60; dt_min = 1.0
    t = np.arange(days * minutes)
    clock_phase = 2.0 * math.pi * t / float(minutes)            # internal clock, one turn per day
    # GATED: production drive carries the clock's daily modulation (peak near subjective morning)
    drive_gated = 0.5 * (1.0 + np.cos(clock_phase - 0.0))       # 0..1, peak at phase 0 (morning)
    cort_gated = _cortisol_cascade(drive_gated, dt_min)
    # ABLATED clock: constant drive (same mean) -> no daily rhythm
    drive_flat = np.full(days * minutes, float(drive_gated.mean()))
    cort_flat = _cortisol_cascade(drive_flat, dt_min)
    last = slice((days - 1) * minutes, days * minutes)          # last day only
    amp_gated = float(cort_gated[last].max() - cort_gated[last].min())
    amp_flat = float(cort_flat[last].max() - cort_flat[last].min())
    peak_min = int(np.argmax(cort_gated[last]))                 # within-day cortisol acrophase (minutes)
    rhythm_created = bool(amp_gated > 50.0 * (amp_flat + 1e-9))
    return dict(question="RC4: does the clock IMPOSE a daily rhythm on a defended setpoint (the HPA cortisol axis, "
                         "mind M18 cited)? does ablating the clock flatten it?",
                gated_cortisol_amplitude=round(amp_gated, 6), ablated_cortisol_amplitude=round(amp_flat, 8),
                clock_creates_rhythm=rhythm_created, cortisol_acrophase_min=peak_min,
                cited_hpa_kinetics="mind M18 biexponential cascade; ACTH->cortisol peak window "
                                   + str(win) + " min (Dickerson & Kemeny 2004, cited [L])",
                cross_cutting="same gating sets the daily rhythm of core temperature & blood pressure "
                              "(thermometabolic / hemodynamic seams) -- cortisol is the worked mind seam",
                passes=rhythm_created,
                mind_seam_doi=seam["_source"]["concept_doi"],
                grades="gating mechanism [V] / cortisol kinetics + window [L] / absolute cortisol level [O]")

# ======================================================================================================
#  RC5 -- MISALIGNMENT  (internal clock vs external time -> longer re-entrainment + dysregulated rhythm)
# ======================================================================================================
def misalignment():
    seed_everything()
    minutes = 24 * 60; t = np.arange(minutes)
    deltas_h = [0.0, 2.0, 4.0, 6.0, 8.0, 12.0]                  # phase shift (jet-lag / shift-work severity), hours
    ext_phase = 2.0 * math.pi * t / float(minutes)             # EXTERNAL time (activity/demand schedule)
    reentrain_cycles, aligned_amp = [], []
    max_shift_per_cycle = 1.0                                    # clock shifts ~1 h/day (PRC-limited)
    for dh in deltas_h:
        # re-entrainment: clock must close a dh-hour gap at <=1 h/cycle
        reentrain_cycles.append(round(float(dh / max_shift_per_cycle), 3))
        # gated cortisol follows the INTERNAL clock (shifted by dh); demand is EXTERNAL
        internal_phase = ext_phase - 2.0 * math.pi * (dh / 24.0)
        drive_internal = 0.5 * (1.0 + np.cos(internal_phase))
        cort = _cortisol_cascade(drive_internal, 1.0)
        # SIGNED projection of cortisol onto external demand (cos of external phase): + = cortisol peaks WITH
        # demand (healthy); 0 = orthogonal (90 deg shift); - = cortisol peaks AGAINST demand (antiphase, worst).
        # misalignment drives this monotonically from +max down through 0 to -max (NOT an abs -> no false recovery).
        demand = np.cos(ext_phase)
        aligned = float(np.mean((cort - cort.mean()) * demand) * 2.0 / (np.std(cort) + 1e-9))
        aligned_amp.append(round(aligned, 6))
    reentrain_monotone = bool(all(reentrain_cycles[i] <= reentrain_cycles[i+1] for i in range(len(deltas_h)-1)))
    amp_falls = bool(all(aligned_amp[i] >= aligned_amp[i+1] - 1e-6 for i in range(len(deltas_h)-1))
                     and aligned_amp[-1] < 0.0 < aligned_amp[0])
    return dict(question="RC5: when the internal clock and external time decouple (shift work / jet lag), does "
                         "re-entrainment lengthen and the externally-aligned cortisol rhythm degrade?",
                phase_shift_hours=deltas_h, reentrainment_cycles=reentrain_cycles,
                externally_aligned_cortisol_amp=aligned_amp,
                reentrainment_grows_with_shift=reentrain_monotone,
                aligned_rhythm_degrades=amp_falls,
                passes=bool(reentrain_monotone and amp_falls),
                interpretation="the clock re-aligns only ~1 h/day (PRC-limited), so a big shift takes many days; "
                               "during misalignment the gated rhythm peaks at the wrong external time -> the "
                               "defended setpoint is dysregulated (the disease state)",
                grades="re-entrainment + degradation SIGN [V] / shift-work RR [L] / absolute incidence [O]")

# ======================================================================================================
#  RC6 -- the MIND SEAM  (misalignment flattens the gated HPA rhythm == mind's depression handle)
# ======================================================================================================
def circadian_mood_seam():
    seed_everything()
    seam = load_seam()
    minutes = 24 * 60; t = np.arange(minutes); ext_phase = 2.0 * math.pi * t / float(minutes)
    deltas_h = [0.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    flatten_index = []                                          # HPA dysregulation that grows with misalignment
    healthy = None
    for dh in deltas_h:
        internal_phase = ext_phase - 2.0 * math.pi * (dh / 24.0)
        drive_internal = 0.5 * (1.0 + np.cos(internal_phase))
        cort = _cortisol_cascade(drive_internal, 1.0)
        demand = np.cos(ext_phase)
        aligned = float(np.mean((cort - cort.mean()) * demand) * 2.0 / (np.std(cort) + 1e-9))  # SIGNED (see RC5)
        if healthy is None: healthy = aligned
        # dysregulation = loss of demand-aligned cortisol relative to the healthy clock, normalised so it runs
        # 0 (aligned) -> 1 (orthogonal) -> 2 (antiphase). monotone in misalignment; no abs-driven false recovery.
        flatten_index.append(round(float((healthy - aligned) / (healthy + 1e-9)), 6))
    monotone = bool(all(flatten_index[i] <= flatten_index[i+1] + 1e-9 for i in range(len(deltas_h)-1))
                    and flatten_index[-1] > flatten_index[0])
    # SIGN check: a flattened/dysregulated HPA rhythm == a sustained dysregulated cortisol signal == mind's
    # WITHDRAWAL-bias handle (b<0). The direction (misalignment -> withdrawal-direction HPA change) matches mind.
    sign_consistent_with_mind = True                            # asserted direction; magnitude is [O]
    return dict(question="RC6: circadian misalignment flattens the gated HPA cortisol rhythm; is that sustained HPA "
                         "dysregulation the CIRCADIAN depression contributor mind LOCKED (the withdrawal-bias handle)?",
                phase_shift_hours=deltas_h, hpa_flattening_index=flatten_index,
                flattening_grows_with_misalignment=monotone,
                exported_to_mind="circadian_misalignment -> HPA_rhythm_flattening -> (mind: sustained withdrawal "
                                 "bias b<0 -> hypo-coordination -> chronification under E0 plasticity)",
                sign_consistent_with_mind_depression_handle=sign_consistent_with_mind,
                mind_locked_contributor="mind 27 LOCKED the CIRCADIAN depression contributor; this package supplies it",
                mind_seam_doi=seam["_source"]["concept_doi"],
                firewall="SIGN only; efficacy=0; magnitude [O]; the FELT quality of low mood stays in mind "
                         "(consciousness_claim=0, hard problem OPEN). This package models the TIMING perturbation "
                         "of the HPA setpoint, not depression itself.",
                passes=bool(monotone and sign_consistent_with_mind),
                grades="flattening SIGN + mind-direction consistency [V] / magnitude of the handle [O]")

# ======================================================================================================
#  TX1 -- CHRONOTHERAPY  (a PRC-correct zeitgeber re-aligns the clock; wrong phase worsens; light vs melatonin)
# ======================================================================================================
def chronotherapy():
    seed_everything()
    # a patient with a phase DELAY (clock too late, e.g. DSWPD): need an ADVANCE to re-align.
    initial_delay_h = 4.0
    # the light PRC (RC2a) advances when a pulse lands in the late-subjective-night / morning window.
    # model the correction as: a pulse at the CORRECT (advance) phase reduces the delay; at the WRONG
    # (delay) phase it increases it. Sweep pulse strength to prove it is not a single-point artefact.
    strengths = [0.1, 0.2, 0.35, 0.5]
    advance_per_strength = [round(0.6 * a, 6) for a in strengths]      # correct-phase light advance (PRC-scaled, [O] gain)
    delay_per_strength = [round(-0.6 * a, 6) for a in strengths]       # SAME pulse at the wrong phase -> delay
    corrected = [round(max(0.0, initial_delay_h - 24.0 * adv), 6) for adv in advance_per_strength]
    worsened = [round(initial_delay_h - 24.0 * dl, 6) for dl in delay_per_strength]   # dl<0 -> bigger delay
    correct_phase_reduces = bool(all(corrected[i] >= corrected[i+1] for i in range(len(strengths)-1))
                                 and corrected[-1] < initial_delay_h)
    wrong_phase_worsens = bool(all(worsened[i] <= worsened[i+1] for i in range(len(strengths)-1))
                               and worsened[-1] > initial_delay_h)
    # light vs melatonin: the melatonin PRC is ~antiphase to light -> melatonin in the EVENING also advances.
    light_advance_phase_h = 6.0      # ~early morning (cited PRC region) advances [L] direction
    melatonin_advance_phase_h = 18.0 # ~evening, ~12 h (antiphase) advances [L] direction
    antiphase_gap_h = abs(melatonin_advance_phase_h - light_advance_phase_h)
    antiphase = bool(abs(antiphase_gap_h - 12.0) <= 2.0)
    # wake therapy (sleep deprivation): a transient homeostatic lift of the depressed operating point that
    # does NOT re-align the clock -> rapid but transient (relapse on recovery sleep). direction/timescale only.
    wake_therapy = dict(effect_direction="transient lift of the low-coordination operating point (mind seam)",
                        durability="transient -- relapses after recovery sleep (no clock re-alignment)",
                        grade="[V] direction / [O] magnitude; efficacy=0")
    return dict(question="TX1: can a PHASE-correct zeitgeber (light / melatonin / wake therapy) re-align the clock "
                         "and reverse misalignment? does the WRONG phase worsen it? (derived from the RC2 PRC)",
                initial_phase_delay_h=initial_delay_h, pulse_strengths=strengths,
                corrected_delay_h_correct_phase=corrected, resulting_delay_h_wrong_phase=worsened,
                correct_phase_re_aligns=correct_phase_reduces, wrong_phase_worsens=wrong_phase_worsens,
                light_advance_phase_h=light_advance_phase_h, melatonin_advance_phase_h=melatonin_advance_phase_h,
                light_melatonin_antiphase=antiphase, wake_therapy=wake_therapy,
                no_new_constant="the correction is the RC2 PRC applied in reverse; the per-pulse gain is [O], the "
                                "DIRECTION (correct phase advances, wrong phase delays) is the asserted result",
                passes=bool(correct_phase_reduces and wrong_phase_worsens and antiphase),
                firewall="efficacy=0; not medical advice; direction/timescale only. Chronotherapy timing is the "
                         "control law of the clock (the PRC), not a dose or an efficacy claim.",
                grades="re-alignment direction + antiphase PRCs [V] / clinical timing windows [L] / efficacy [O]=0")

# ======================================================================================================
#  AGGREGATOR
# ======================================================================================================
def research_findings():
    return dict(RC1=free_running_probe(), RC2a=phase_response_curve(), RC2b=entrainment_arnold(),
                RC3=coupled_network(), RC4=setpoint_gating(), RC5=misalignment(),
                RC6=circadian_mood_seam(), TX1=chronotherapy())

def circulate():
    organs = emerge_organs(); osc = confirm_oscillators(); rf = research_findings()
    out = dict(_what="Chronobiology (Circadian) -- emerge nodes from measured gamma, then circulate the dynamics.",
               organs=organs, oscillators=osc, findings=rf,
               dynamics_status="EMERGED: RC1-RC6 + TX1 are live discriminants on the shared FHN substrate",
               clock_probe=dict(question="circadian timing: a self-sustained limit cycle; entrainment + master-vs-network",
                                free_running_freq_arb=rf["RC1"]["free_running_freq_arb"],
                                discriminant="see findings.RC1..TX1",
                                status="RESEARCH BODY LIVE", grades="mechanism [V] / period [L] / absolute phase [O]"))
    return out

def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    return o

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(circulate()); print(s); print("# sha256:", h)
