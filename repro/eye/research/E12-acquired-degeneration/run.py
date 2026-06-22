#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E12-acquired-degeneration/run.py — INCREMENT E12: acquired / degenerative disease.

  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
  │ SCOPE — THEORETICAL, NON-CLINICAL (read first; binding, FIREWALL.md / BLUEPRINT.md).           │
  │ E12 studies the MECHANISM LAYER of the common ACQUIRED, age/environment-related degenerative    │
  │ eye diseases (age-related macular degeneration, glaucoma, diabetic retinopathy) as a question   │
  │ in dynamical-systems theory — what the FROZEN R19 switch already FORCES about how a transducer   │
  │ that ONCE WORKED is lost. STRUCTURE-only and DIRECTION-only. It does NOT diagnose, treat,        │
  │ prescribe, screen, classify a person, stage, or triage; it designs no molecule, names no risk    │
  │ factor magnitude, and makes no prognosis. Every statement sits behind a machine-checked          │
  │ MAGNITUDE FIREWALL (main() asserts the entire output carries no quantitative clinical token — no │
  │ dose, potency, efficacy, pressure in mmHg, glycaemic value, length in mm, no '%'). The felt      │
  │ percept (and felt loss) of sight is deferred to the mind volume.                                │
  └──────────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E12 DOES (BLUEPRINT "beyond the ladder spine"; research/E12-acquired-degeneration/START_HERE.md).
  Four things, built ONLY on the FROZEN R19 substrate + the already-measured atlas — it adds NO new γ,
  fetches nothing, and re-derives nothing. The whole result is one structural distinction the substrate
  forces, and its consequences:

    The CONGENITAL chapter (E4) read the switch as a STATIC failure — loss-of-function is the R19 switch
    held with its drive frozen BELOW its own spinodal h*(γ), so the all-or-none flip never fires (it was
    born unable to flip). A DEGENERATIVE disease is categorically different: the switch STARTS in the
    healthy basin (s>0, it worked) and is carried OVER its own fold by a slowly-accumulating stress. On
    the FROZEN field ds/dt = γ·s − s³ + h, the upper (healthy) stable branch exists only while the drive
    stays above the lower fold h = −h*(γ); a stress that drives h down past −h* ANNIHILATES the healthy
    basin (a saddle-node), and the state drops discontinuously to the degenerate basin. SAME fold as
    E2/E4 — reached the other way (dynamically, from the ON side), which is exactly the difference between
    "never flipped" and "was lost".

    PART A — DEGENERATION IS A SLOW DRIFT ACROSS THE FOLD (dynamic), not a failure to be born (static).
      Hold a gene's measured γ; start ON (s>0); ramp a stress that lowers the drive h quasi-statically.
      The healthy state tracks the upper branch smoothly down through h=0 and stays ON — until h crosses
      the fold −h*(γ), where the upper basin disappears and the state COLLAPSES (s>0 → s<0) in one step.
      The collapse drive equals the analytic fold −h*(γ) to within the ramp resolution; it is independent
      of where the healthy point started. This is the tipping point: smooth, then sudden. [V]/[F]

    PART B — HYSTERESIS: WHY DEGENERATION IS HARD TO REVERSE (forced by the bistability).
      The signature of a fold-mediated collapse is HYSTERESIS. From the collapsed degenerate state, ramp
      the stress back DOWN (raise h). The state stays degenerate through the pre-collapse drive — merely
      undoing the stress to where the cell was still healthy does NOT restore it — and only re-flips when
      h is pushed all the way to the OPPOSITE fold +h*(γ). So the collapse fold (−h*) and the recovery
      fold (+h*) are different; the loop width is 2·h*(γ), the irreversibility margin. DIRECTION-only:
      acting BEFORE the fold (on the upper branch) is categorically unlike acting AFTER (recovery needs
      over-correction past +h*). The margin's clinical magnitude is the firewall-blocked [O]. [F]/[O-mag]

    PART C — ONE CATASTROPHE GEOMETRY, MANY ROUTES IN (the honest multifactorial unification).
      AMD (oxidative/RPE–photoreceptor), glaucoma (mechanical load on ganglion cells) and diabetic
      retinopathy (metabolic/ischaemic) have THREE DIFFERENT primary stresses. The substrate says any
      bistable transducer fails the SAME way — by a fold — regardless of WHICH parameter the stress rides.
      Show two distinct routes to the SAME saddle-node: (i) the LOAD route — raise an anti-drive (lower h)
      at fixed γ until h hits −h*(γ); (ii) the BASIN-SHALLOWING route — hold a fixed load and ERODE γ, so
      the fold itself h*(γ)=2(γ/3)^1.5 SHRINKS up to meet the operating point (collapse when h*(γ)=|load|).
      Both annihilate the healthy basin; both land on the ONE fold locus h=−h*(γ). The catastrophe geometry
      (a fold + hysteresis) is shared; the IDENTITY of the primary stress is exactly what the substrate
      does NOT determine — a named [O]. [F]/[O-route]

    PART D — γ READ-ONLY as a STRUCTURAL fragility offset; the genetics is even MORE open than E4.
      A shallower basin tips under a smaller stress: lower γ ⇒ smaller barrier γ²/4 AND smaller fold
      h*(γ). So the atlas genes carry a STRUCTURAL fragility ordering by spinodal(γ) — CNGB3 (shallowest)
      to PDE6B (deepest) — read READ-ONLY, byte-equal to the frozen atlas. This is NOT a clinical risk
      ranking (firewall-blocked), and — crucially — the map from a real degenerative-disease risk locus to
      a γ-shift is a named [O] that is even MORE open than the monogenic lesions of E4: these diseases are
      multifactorial, age- and environment-gated and polygenic (common variants of small effect, often
      outside a promoter), so the promoter-γ this package reads has essentially NO monogenic purchase here.
      The chapter's content is the dynamical-systems STRUCTURE (the distinction, the hysteresis, the
      one-geometry-many-routes), not a disease prediction. The felt loss of sight → mind volume. [F]/[O]

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E12 CONSUMES the FROZEN R19 substrate + the MEASURED atlas; it re-derives nothing and adds no γ.
    - the bistable field ds/dt=γ·s−s³+h, the spinodal h*(γ)=2(γ/3)^1.5, the barrier γ²/4, the settler
                                                        ← inherited/vp_substrate.py  (frozen, no-regression)
    - γ (LEVEL) of the retinal master genes (read-only) ← inherited/organ_gamma.json (MEASURED [L];
                                      re-proved by verify_seed [3] offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never a stress rate, a cell
  viability, a pressure, a metabolic level, or a clinical effect (FIREWALL #1). The stress drives and the
  ramps are INPUTS expressed as dimensionless multiples of the gene's OWN fold h*(γ) (never fitted targets
  and never a clinical magnitude). The disease layer is structure-only and proposal-only (FIREWALL #3); the
  felt percept belongs to the mind volume (FIREWALL #4). Nothing here diagnoses, treats, or prognoses.

GRADES (VP-SPEC C3): [F] forced · [V] verified (deterministic recomputation on the frozen field)
                     · [L] measured/calibrated · [O] open (obstacle named).
stdlib + numpy (the frozen substrate's dependency); no RNG (no seed_everything is called — every
trajectory is a deterministic integration). Deterministic: 2× run → identical sha256. Output passes the
machine-checked MAGNITUDE FIREWALL.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E12-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, barrier, settle   # FROZEN R19 field + fold + barrier + settler
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# ---- MAGNITUDE FIREWALL: forbidden quantitative clinical tokens (FIREWALL.md #1/#3) ----
# Mirrors E9/E11 and ADDS the magnitudes specific to this layer: glaucoma's intra-ocular pressure
# (mmhg, already blocked), diabetic-retinopathy glycaemic values (hba1c, mg/dl, mmol/l), and bare
# length units (mm) — so a pressure, a glucose level, a drusen/thickness length, or a visual-field
# loss can never leak. main() asserts the ENTIRE output contains none of them (case-insensitive),
# plus no "%": every fact is a dimensionless ratio (a multiple of the gene's OWN fold) or a sign.
MAGNITUDE_BLOCK = (
    "dose", "dosage", "mg/kg", "ic50", "ec50", "µmol", "nmol", "µg", "µm)", "nm)",
    "potency", "efficacy", "selectivity", "diopter", "dioptre", "mmhg",
    "milligram", "microgram", "micromolar", "nanomolar",
    "hba1c", "mg/dl", "mmol/l", "mmol/dl",
    " mm ", " mm.", " mm,", " mm)",
)

# ---- deterministic quasi-static integration helpers (no RNG; carry the state forward) ----
_DT, _RELAX = 0.01, 4000


def relax_to(s, g, h, dt=_DT, n=_RELAX):
    """Integrate the FROZEN field one quasi-static dwell from the current state s under fixed drive h."""
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s


def ramp_track(g, values, mode, fixed, s0):
    """Track the state along a quasi-static ramp of one parameter, carrying s forward (HYSTERESIS-aware).

    mode='h'     : sweep the drive h over `values` at fixed γ=`fixed` (the LOAD route).
    mode='gamma' : sweep γ over `values` at fixed drive h=`fixed` (the BASIN-SHALLOWING route).
    Returns (cross_value, last_same_sign_value, final_state) where cross_value is the first ramp point
    at which the state's sign flips from sign(s0). Deterministic.
    """
    s = s0
    started_on = (s0 > 0.0)
    last = None
    for x in values:
        g_use = x if mode == "gamma" else fixed
        h_use = x if mode == "h" else fixed
        s = relax_to(s, g_use, h_use)
        now_on = (s > 0.0)
        if now_on == started_on:
            last = x
        else:
            return x, last, s
    return None, last, s


def linspace(a, b, n):
    """Deterministic, dependency-free evenly-spaced ramp (endpoints inclusive)."""
    if n == 1:
        return [a]
    step = (b - a) / (n - 1)
    return [a + step * i for i in range(n)]


def run(P):
    P("=" * 80)
    P("E12 — ACQUIRED / DEGENERATIVE DISEASE   (the R19 switch carried OVER its fold, with hysteresis)")
    P("=" * 80)
    P("SCOPE: theoretical, NON-CLINICAL. Structure-only / direction-only behind the magnitude firewall.")
    P("consumes (frozen): the R19 field ds/dt=γ·s−s³+h, the fold h*(γ)=2(γ/3)^1.5, the barrier γ²/4.")
    P("re-derives: nothing; adds no γ. γ measured, never fitted; γ = promoter STRUCTURE only (firewall).")
    P("every stress is a dimensionless multiple of the gene's OWN fold h*(γ); no clinical magnitude, no percent sign.")
    P("DISTINCTION (vs E4): congenital = a switch born BELOW its fold (static, never flips); degenerative")
    P("                     = a switch that STARTED healthy (s>0) and is carried OVER its fold (dynamic).")

    # worked example: RHO (the rod photoreceptor opsin; the same fold E10 used). READ-ONLY.
    G = "RHO"
    g = ATLAS[G]["gamma"]
    hstar = spinodal(g)
    bar = barrier(g)
    s_root = math.sqrt(g)                                  # the symmetric ON/OFF roots at h=0 are ±√γ
    P(f"\nworked gene (READ-ONLY): {G}  γ = {g:.4f}   fold h*(γ) = {hstar:.6f}   barrier γ²/4 = {bar:.6f}")

    # ----------------------------------------------------------------------------------------
    # PART A — degeneration is a slow drift ACROSS the fold (dynamic), not a static failure
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — degeneration = a slow drift over the fold: start ON, lower the drive, COLLAPSE at −h*")
    P("-" * 80)
    # start comfortably ON at a healthy drive (a fraction of the fold), settled from the ON root
    h_health = 0.5 * hstar
    s_on = settle(g, h_health, s0=s_root)
    P(f"start healthy: drive h = +0.5·h* (a working operating point), state settles ON: s = {s_on:.6f} (s>0)")
    # quasi-static DOWN ramp of the drive (the accumulating stress) from +0.5h* to −1.3h*
    N = 320
    down = linspace(0.5 * hstar, -1.3 * hstar, N)
    h_collapse, h_last_on, s_after = ramp_track(g, down, "h", g, s_on)
    step = abs(down[0] - down[1])
    gap = abs(h_collapse - (-hstar))
    P(f"ramp a stress that lowers the drive quasi-statically (ramp step Δh = {step:.6f}):")
    P(f"   the healthy state tracks the upper branch DOWN through h=0 and stays ON, last ON at h = {h_last_on:.6f}")
    P(f"   then at h = {h_collapse:.6f} it COLLAPSES in one step to the degenerate basin: s = {s_after:.6f} (s<0)")
    P(f"   the collapse drive equals the analytic fold −h* = {-hstar:.6f}: gap = {gap:.6f} = {gap/step:.4f}× the ramp step. [V]")
    assert s_after < 0.0 and s_on > 0.0, "the state must start ON (s>0) and end degenerate (s<0)"
    assert gap < 2.0 * step, "the dynamic collapse must occur at the analytic fold −h* within the ramp resolution"
    # independence of the starting point: a different healthy start collapses at the SAME fold
    s_on_hi = settle(g, 0.9 * hstar, s0=s_root)
    h_collapse2, _, _ = ramp_track(g, linspace(0.9 * hstar, -1.3 * hstar, N), "h", g, s_on_hi)
    P(f"   independence: a DIFFERENT healthy start (h=+0.9·h*) collapses at h = {h_collapse2:.6f} — the same fold.")
    assert abs(h_collapse2 - h_collapse) < 3.0 * step, "the collapse fold must not depend on the healthy starting point"
    P("   smooth, then sudden: this is a TIPPING POINT, not a graded decline. The fold is E2/E4's spinodal,")
    P("   reached dynamically from the ON side — the difference between 'was lost' and 'never flipped'. [F]")

    # ----------------------------------------------------------------------------------------
    # PART B — hysteresis: why degeneration is hard to reverse (forced by the bistability)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — hysteresis: collapse at −h*, but recovery needs +h* — the loop width is the irreversibility")
    P("-" * 80)
    # from the collapsed degenerate state, ramp the stress back DOWN (raise h) toward +1.3h*
    up = linspace(-1.3 * hstar, 1.3 * hstar, N)
    h_recover, h_last_off, s_rec = ramp_track(g, up, "h", g, s_after)
    loop = h_recover - h_collapse
    P(f"from the collapsed state (s<0), ramp the stress back DOWN (raise the drive) from h = {up[0]:.6f}:")
    P(f"   the state stays degenerate through the PRE-COLLAPSE drive — last degenerate at h = {h_last_off:.6f} —")
    P(f"   and only re-flips ON (s = {s_rec:.6f}) at h = {h_recover:.6f}, the OPPOSITE fold +h* = {hstar:.6f}. [V]")
    P(f"   so collapse (−h*) and recovery (+h*) are DIFFERENT drives; the hysteresis loop width is")
    P(f"   h_recover − h_collapse = {loop:.6f}, the analytic 2·h*(γ) = {2*hstar:.6f}: the IRREVERSIBILITY margin.")
    assert h_recover > h_collapse + 0.5 * hstar, "recovery fold (+h*) must be well above the collapse fold (−h*)"
    assert s_rec > 0.0, "the up-ramp must eventually recover the healthy state"
    P("   DIRECTION-only: acting on the upper branch BEFORE the fold is categorically unlike acting AFTER —")
    P("   recovery requires over-correction past +h*, not merely undoing the stress. The margin's magnitude")
    P("   is the firewall-blocked [O]; only that the two folds DIFFER (early ≠ late) is stated. [F]/[O]")

    # ----------------------------------------------------------------------------------------
    # PART C — one catastrophe geometry, many routes in (the multifactorial unification)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — one geometry, many routes: a LOAD route (move h) and a BASIN-SHALLOWING route (erode γ)")
    P("-" * 80)
    P("AMD, glaucoma and diabetic retinopathy carry THREE DIFFERENT primary stresses; the substrate says")
    P("any bistable transducer fails the SAME way — by a fold — whichever parameter the stress rides.")
    # route (i): the LOAD route already shown in PART A — fixed γ, drive → −h*. restate its landing.
    P(f"\n[route i — LOAD] fixed γ={g:.4f}, raise an anti-drive (lower h): collapse at h = {h_collapse:.6f}")
    P(f"   ≈ the fold −h*(γ) = {-hstar:.6f} (PART A).")
    # route (ii): the BASIN-SHALLOWING route — hold a fixed load, erode γ until h*(γ) shrinks to meet it
    load = -0.30                                            # a fixed anti-drive (a constant load), |load| < h*(RHO)
    s_on_load = settle(g, load, s0=s_root)                 # still ON: the load alone hasn't crossed the fold
    P(f"\n[route ii — BASIN-SHALLOWING] hold a fixed load h = {load:.6f} (cell still ON: s = {s_on_load:.6f}, s>0);")
    P(f"   now ERODE γ. The fold itself h*(γ)=2(γ/3)^1.5 SHRINKS, rising up to meet the fixed load.")
    gseq = linspace(g, 0.5, N)
    g_collapse, g_last_on, s_after_g = ramp_track(g, gseq, "gamma", load, s_on_load)
    gcrit = 3.0 * (abs(load) / 2.0) ** (2.0 / 3.0)         # γ where h*(γ) = |load| exactly
    gstep = abs(gseq[0] - gseq[1])
    P(f"   eroding γ (ramp step Δγ = {gstep:.6f}): collapses at γ = {g_collapse:.6f} (last ON γ = {g_last_on:.6f}),")
    P(f"   where the shrinking fold h*(γ) = {spinodal(g_collapse):.6f} has met the load |h| = {abs(load):.6f}.")
    P(f"   the analytic crossing γ_crit (h*(γ)=|load|) = {gcrit:.6f}, and there h*(γ_crit) = {spinodal(gcrit):.6f}. [V]")
    assert s_after_g < 0.0, "the basin-shallowing route must also reach a collapse (s>0 → s<0)"
    assert abs(g_collapse - gcrit) < 3.0 * gstep, "the γ-erosion collapse must land where h*(γ)=|load|"
    # both routes land on the ONE fold locus h = −h*(γ): check the shallowing collapse lies on it
    on_locus = abs(load - (-spinodal(g_collapse)))
    P(f"   BOTH routes land on the ONE fold locus h = −h*(γ): at the γ-erosion collapse, the load {load:.6f}")
    P(f"   sits on −h*(γ) = {-spinodal(g_collapse):.6f} (gap {on_locus:.6f}). Same saddle-node, different parameter moved. [F]")
    assert on_locus < 0.05, "the basin-shallowing collapse must lie on the same fold locus h=−h*(γ)"
    P("   the catastrophe GEOMETRY (a fold + hysteresis) is shared; the IDENTITY of the primary stress —")
    P("   oxidative vs mechanical vs metabolic — is exactly what the substrate does NOT fix: a named [O].")

    # ----------------------------------------------------------------------------------------
    # PART D — γ READ-ONLY as a structural fragility offset; the genetics is even MORE open than E4
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART D — γ as STRUCTURAL fragility (shallower basin tips first); the disease-genetics map is [O]")
    P("-" * 80)
    P("a shallower basin tips under a smaller stress: lower γ ⇒ smaller barrier γ²/4 AND smaller fold h*(γ).")
    P("the atlas genes therefore carry a STRUCTURAL fragility ordering by spinodal(γ) (READ-ONLY, byte-equal):")
    ranked = sorted(ATLAS.items(), key=lambda kv: spinodal(kv[1]["gamma"]))
    # monotonicity: spinodal strictly increases with γ across the atlas
    mono = all(spinodal(ranked[i + 1][1]["gamma"]) > spinodal(ranked[i][1]["gamma"])
               for i in range(len(ranked) - 1))
    frail_sym, frail_g = ranked[0][0], ranked[0][1]["gamma"]
    stiff_sym, stiff_g = ranked[-1][0], ranked[-1][1]["gamma"]
    P(f"   most fragile (shallowest basin): {frail_sym:8s} γ = {frail_g:.4f}  fold h* = {spinodal(frail_g):.6f}")
    P(f"   stiffest    (deepest basin):     {stiff_sym:8s} γ = {stiff_g:.4f}  fold h* = {spinodal(stiff_g):.6f}")
    P(f"   structural fragility span (fold ratio stiffest/most-fragile) = {spinodal(stiff_g)/spinodal(frail_g):.6f}")
    P(f"   the ordering is MONOTONE in γ (lower γ ⇒ smaller fold ⇒ tips under less stress): {mono}. [F]")
    assert mono, "spinodal(γ) must be monotone in γ across the atlas (the structural fragility ordering)"
    # no-drift: every γ E12 reads is byte-equal to the frozen atlas (no fitting)
    no_drift = (ATLAS[frail_sym]["gamma"] == frail_g and ATLAS[stiff_sym]["gamma"] == stiff_g
                and ATLAS[G]["gamma"] == g)
    P(f"\n   [no-drift] every γ byte-equal to the frozen atlas (no fitting): {no_drift}")
    assert no_drift, "E12 must consume the frozen γ unchanged (no fitting)"
    P("   this is a STRUCTURAL ordering, NOT a clinical risk ranking (that would be firewall-blocked).")
    P("   BRUTAL CAVEAT (loudest in this chapter): the map from a real degenerative-disease risk locus to a")
    P("   γ-shift is a named [O] that is even MORE open than the monogenic lesions of E4 — these diseases are")
    P("   multifactorial, age- and environment-gated and polygenic (common variants of small effect, often")
    P("   outside a promoter), so the promoter-γ this package reads has essentially NO monogenic purchase here.")
    P("   the chapter's content is the dynamical-systems STRUCTURE (the distinction, the hysteresis, the")
    P("   one-geometry-many-routes), not a disease prediction. The felt loss of sight → mind volume. [O]")

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E12 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : degeneration is a switch carried OVER its fold (dynamic), categorically unlike the")
    P("                 congenital switch born below it (static, E4); a fold-mediated collapse has HYSTERESIS")
    P("                 (collapse at −h*, recovery at +h*, loop width 2·h*); any bistable transducer fails by")
    P("                 the SAME fold whatever parameter the stress rides (load route OR basin-shallowing")
    P("                 route, both on the one locus h=−h*(γ)); a shallower basin (lower γ) tips under less")
    P("                 stress (spinodal monotone in γ) — a STRUCTURAL fragility ordering, not a clinical one.")
    P("  [V] verified : on the frozen field, the down-ramp from ON collapses at −h* (within the ramp step) and")
    P("                 is independent of the healthy start; the up-ramp from the collapsed state recovers only")
    P("                 at +h*; the γ-erosion route collapses where h*(γ)=|load| and lands on h=−h*(γ); the")
    P("                 fragility ordering is monotone; every γ is byte-equal to the atlas. Firewall machine-checked.")
    P("  [L] measured : every retinal-master γ (NCBI promoters, cached, read-only); 'AMD/glaucoma/DR are")
    P("                 acquired, multifactorial degenerations' is the cited disease framing this matches.")
    P("  [O] open     : the IDENTITY and rate of the primary stress for any specific disease (oxidative vs")
    P("                 mechanical vs metabolic — the substrate fixes the geometry, not the route); the MAP")
    P("                 from a real risk locus to a γ-shift (even MORE open than E4 — polygenic, age/environment-")
    P("                 gated, mostly non-promoter common variants); the irreversibility-margin magnitude, the")
    P("                 absolute stress scale, any clinical staging/prognosis (all firewall-blocked — none")
    P("                 produced); the felt percept and felt LOSS of sight (→ mind volume). Each obstacle named.")
    P("\nLEARNED: a degenerative disease is not a switch born broken — it is a switch that worked and was")
    P("         carried over its own fold. On the frozen R19 field the healthy state lives in the upper basin")
    P("         and survives a slowly-rising stress right up to the spinodal −h*(γ), then collapses in one step:")
    P("         a TIPPING POINT, the same fold E4 read from the static side, reached here dynamically from the")
    P("         ON side. Because the transition is a fold it is HYSTERETIC — recovery demands pushing past the")
    P("         OPPOSITE fold +h*, not merely removing the stress — which is the substrate's account of why")
    P("         early and late are categorically different. And because ANY bistable transducer fails by a fold,")
    P("         the same catastrophe geometry is reached by many routes (load the switch, or shallow its basin)")
    P("         — so the shared late picture across AMD, glaucoma and diabetic retinopathy is FORCED while the")
    P("         identity of each primary stress, and the disease genetics, stay honestly and emphatically open.")
    P("         Foundation untouched; no γ added; nothing fitted; firewall intact and machine-checked.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    text = buf.getvalue()
    # --- MAGNITUDE FIREWALL (machine-checked, every run): no quantitative clinical token, no "%" ---
    low = text.lower()
    hits = [tok for tok in MAGNITUDE_BLOCK if tok in low]
    assert not hits, f"MAGNITUDE FIREWALL breached — forbidden clinical-magnitude token(s): {hits}"
    assert "%" not in text, "MAGNITUDE FIREWALL breached — a percent magnitude leaked into the output"
    return hashlib.sha256(text.encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
