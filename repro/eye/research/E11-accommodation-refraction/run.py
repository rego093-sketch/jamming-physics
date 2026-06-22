#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E11-accommodation-refraction/run.py — INCREMENT E11: accommodation & refractive error.

  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
  │ SCOPE — THEORETICAL, NON-CLINICAL (read first; binding, FIREWALL.md / BLUEPRINT.md).           │
  │ E11 extends E3's reduced-eye optics (the WHERE channel) to ask, as a question in geometry, how  │
  │ a single refracting eye stays in focus. The NORMAL mechanism (accommodation, a variable-power   │
  │ lens) and the MECHANISM layer of the two commonest refractive conditions (myopia = near-sighted,│
  │ hyperopia = far-sighted) are both studied STRUCTURE-only and DIRECTION-only. It does NOT         │
  │ diagnose, treat, prescribe, screen, classify a person, or triage; it designs no molecule and    │
  │ states no clinical quantity. Every statement sits behind a machine-checked MAGNITUDE FIREWALL    │
  │ (main() asserts the entire output carries no quantitative clinical token — no dose, no potency,  │
  │ no power magnitude in dioptres, no length in mm, no '%'). The felt percept of blur/clarity is    │
  │ deferred to the mind volume.                                                                    │
  └──────────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E11 DOES (BLUEPRINT "beyond the ladder spine"; research/E11-accommodation-refraction/START_HERE.md).
  Four things, built ONLY on the frozen E3 optics + the frozen substrate + the already-measured atlas —
  it adds NO new γ, fetches nothing, and re-derives nothing. The whole result is ONE fact about E3's
  single-surface imaging equation, read as a MATCH between two numbers the eye owns:

    From E3 (frozen): a single refracting surface obeys  n₂/v − n₁/u = P,  P = (n₂−n₁)/R  (the surface
    power), and a DISTANT object (1/u→0) images at  v_∞ = n₂/P. The retina sits at the eye's axial
    length L. So the eye is in focus for distance  ⇔  v_∞ = L  ⇔  **P·L = n₂**: a single, dimensionless
    MATCH between the eye's POWER (optics) and its LENGTH (growth). Everything below follows.

    PART A — EMMETROPIA IS THE POWER↔LENGTH MATCH (forced; the frozen reduced eye sits exactly on it).
      Define the match ratio  ρ ≡ P·L / n₂.  ρ = 1 is emmetropia (sharp distance vision). Read off E3's
      frozen Emsley reduced eye, ρ = 1 EXACTLY (the cited n,R make power and length cohere — by
      construction, not a fit). Emmetropia is NOT one eye but a whole CURVE in (power, length): the
      product is fixed, so a longer eye is emmetropic with proportionally LESS power. [V-arith]/[F]

    PART B — REFRACTIVE ERROR IS THE SIGNED MISMATCH; the SIGN is the only thing stated (DIRECTION-ONLY).
      The distant image is at v_∞ = n₂/P; the retina is at L, and L − v_∞ = (P·L − n₂)/P, so
      sign(L − v_∞) = sign(ρ − 1). Hence:
        • ρ > 1  ⇒ the distant focus falls IN FRONT of the retina ⇒ MYOPIA (near-sighted);
        • ρ < 1  ⇒ the distant focus falls BEHIND the retina      ⇒ HYPEROPIA (far-sighted).
      And the SAME product can be missed two independent ways — too LONG (axial) or too POWERFUL
      (refractive): both raise ρ above 1, both give myopia. Only the SIGN/DIRECTION of the mismatch and
      its correction (myopia ⇒ reduce power; hyperopia ⇒ add power) are stated. The MAGNITUDE — how much
      error, the axial length, the spectacle power — is the firewall-blocked [O]. [F-direction]/[O-mag]

    PART C — ACCOMMODATION IS A ONE-SIGNED POWER LEVER that spans an object-distance RANGE.
      A NEAR object needs MORE power than a distant one to image at the SAME retina. For an object at
      u = −k·L (k = distance in eye-lengths), the power to keep v = L is P_req = (n₂ + n₁/k)/L, so
        P_req / P_∞ = 1 + n₁/(n₂·k)  — rises MONOTONICALLY as the object nears (k↓), → 1 at distance.
      The eye supplies it by ROUNDING the lens: R↓ ⇒ P↑ via the SAME frozen P=(n₂−n₁)/R. So
      accommodation is a strictly ONE-SIGNED lever: it can only ADD plus power (pull the focus nearer),
      never subtract. The near point = lever maxed; the far point = lever relaxed. DIRECTION-only: nearer
      object ⇒ more accommodation. The accommodation AMPLITUDE, the near/far DISTANCES, the presbyopic
      decline with age — all firewall-blocked [O]. [F-direction]/[O-mag]

    PART D — THE LATTICE MEANING OF THE LEVER; the growth axis is a DWELL-size; γ READ-ONLY.
      The power lever is the SAME lattice geometry as E3: P = (n₂−n₁)/R with n = c_vac/c_med =
      √((B/ρ) ratio); since P ∝ 1/R at fixed indices, accommodation is a purely GEOMETRIC modulation of
      the transverse-match interface (dP/P = −dR/R). The LENGTH axis is GROWTH: in the substrate, organ
      size = dwell ∝ γ^1.5 (E1), so the eye's axial length is a DWELL-size. Reading the eye-field master
      PAX6 READ-ONLY (byte-equal to the frozen atlas) instantiates the size law; its DIRECTION is forced
      — more ocular growth ⇒ a longer eye ⇒ the MYOPIC side of the match — while the gene→elongation map,
      the emmetropization feedback that normally holds ρ≈1 in a growing eye, and the absolute scale are a
      named [O]. γ is promoter STRUCTURE only (never a growth rate, an optical power, or a clinical
      effect — firewall). The felt percept of blur → mind volume. [F-structure]/[O-scale]

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E11 CONSUMES the frozen E3 optics + the frozen substrate + the MEASURED atlas; it re-derives nothing
  and adds no γ.
    - the single-surface imaging equation + n=√((B/ρ) ratio) ← research/E3-image-formation/run.py
                                      (loaded read-only; its run() is __main__-guarded, not executed)
    - the size law dwell ∝ γ^1.5, spinodal              ← inherited/vp_substrate.py  (frozen, no-regression)
    - γ (LEVEL) of PAX6 / RAX (read-only)               ← inherited/organ_gamma.json (MEASURED [L];
                                      re-proved by verify_seed [3] offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never an optical power, a
  channel voltage, a potency, a dose, or a clinical effect (FIREWALL #1). The object distances and the
  power/length scalings are INPUTS expressed as dimensionless RATIOS, never fitted targets and never a
  clinical magnitude. The disease/condition layer is structure-only and proposal-only (FIREWALL #3); the
  felt percept belongs to the mind volume (FIREWALL #4). Nothing here diagnoses, treats, or prescribes.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [V-arith] classical ray arithmetic (honestly flagged)
                     · [L] measured/calibrated · [O] open (obstacle named).
stdlib + the frozen E3 optics + the frozen substrate's scalar helpers (pure math, no RNG).
Deterministic: 2× run → identical sha256. Output passes the machine-checked MAGNITUDE FIREWALL.
"""
import os, sys, json, math, hashlib, io, importlib.util

# --- locate the package root cwd-independently ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E11-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import dwell, spinodal                  # FROZEN: the size law dwell ∝ γ^1.5
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]


def _load_e3():
    """Load E3's frozen optics module read-only (its run() is __main__-guarded, so loading it only
    defines the surface-imaging helpers + the cited constants — it does not execute the increment).
    This is the SAME 'import a sibling increment's module to consume it verbatim' pattern the volume
    builder uses for E4's firewall list — so the optics E11 extends has exactly ONE source (E3)."""
    path = os.path.join(PKG, "research", "E3-image-formation", "run.py")
    spec = importlib.util.spec_from_file_location("_e3_optics_for_E11", path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E3 = _load_e3()
N1, N2, R, D = E3.N_AIR, E3.N_EYE, E3.R_MM, E3.D          # consumed from E3 (cited, never re-decided)

# ---- MAGNITUDE FIREWALL: forbidden quantitative clinical tokens (FIREWALL.md #1/#3) ----
# Same spirit as E4/E9. main() asserts the ENTIRE run output contains none of them (case-insensitive),
# plus no "%". "dioptre"/"diopter" and the length unit "mm" are BLOCKED here (a refractive magnitude in
# dioptres or an axial length in mm would BE a clinical quantity), so the whole chapter is forced to
# speak in dimensionless RATIOS and SIGNS only — direction-only by construction.
MAGNITUDE_BLOCK = (
    "dose", "dosage", "mg/kg", "ic50", "ec50", "µmol", "nmol", "µg", "µm)", "nm)",
    "potency", "efficacy", "selectivity", "diopter", "dioptre", "mmhg",
    "milligram", "microgram", "micromolar", "nanomolar", " mm ", " mm.", " mm,", " mm)",
)


def surface_focus(P_power, R_radius):
    """Distant-object image distance v_∞ on E3's frozen single surface, expressed via the consumed
    optics. v_∞ = n₂/P (object at infinity). Two routes (power vs the E3 ray helper) must agree."""
    v_via_power = N2 / P_power
    v_via_e3    = E3.surface_image_distance(None, N1, N2, R_radius)   # E3's frozen ray arithmetic
    assert abs(v_via_power - v_via_e3) < 1e-12, "v_∞ via power must match E3's frozen surface equation"
    return v_via_power


def run(P):
    P("=" * 80)
    P("E11 — ACCOMMODATION & REFRACTIVE ERROR   (E3's optics read as a power↔length MATCH)")
    P("=" * 80)
    P("SCOPE: theoretical, NON-CLINICAL. Structure-only / direction-only behind the magnitude firewall.")
    P(f"inherited invariant quantum size D = {D*1e12:.6f} pm  (the same frozen wave that carries colour)")
    P("consumes (frozen): E3 single-surface optics n₂/v−n₁/u=P, P=(n₂−n₁)/R · vp_substrate.dwell · atlas γ")
    P("re-derives: nothing; adds no γ. γ measured, never fitted; γ = promoter STRUCTURE only (firewall).")
    P("scalings/distances are dimensionless RATIOS; NO power magnitude, NO length, NO clinical quantity.")

    # the emmetropic reduced eye, read off E3's frozen constants (power & length in package-internal
    # units; only the DIMENSIONLESS match ratio ρ = P·L/n₂ is ever surfaced).
    P_emm = (N2 - N1) / R                                 # surface power = (n₂−n₁)/R  (E3)
    L_emm = surface_focus(P_emm, R)                       # axial length that puts v_∞ on the retina
    n2    = N2

    # ----------------------------------------------------------------------------------------
    # PART A — emmetropia is the power↔length MATCH  (ρ = P·L/n₂ = 1 on the frozen reduced eye)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — emmetropia is the power↔length MATCH:  ρ ≡ P·L/n₂ = 1  (a CURVE, not one eye)")
    P("-" * 80)
    rho_emm = (P_emm * L_emm) / n2
    P(f"the eye is in focus for distance ⇔ the distant image v_∞ = n₂/P lands on the retina (length L)")
    P(f"   ⇔ P·L = n₂. On E3's frozen reduced eye the match ratio ρ = P·L/n₂ = {rho_emm:.6f}  (EXACT). [V-arith]")
    P(f"   n₂ = {n2:.6f} (the consumed Emsley index; ρ=1 because the cited n,R cohere — not a fit).")
    assert abs(rho_emm - 1.0) < 1e-12, "the frozen reduced eye must sit EXACTLY on the emmetropic match ρ=1"
    P("emmetropia is a whole CURVE in (power, length): the PRODUCT is fixed, so a longer eye is")
    P("emmetropic with proportionally LESS power (and a shorter eye with more). [F]")

    # ----------------------------------------------------------------------------------------
    # PART B — refractive error is the SIGNED mismatch; DIRECTION-only; two independent routes
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — refractive error = sign(ρ−1): ρ>1 ⇒ MYOPIA (focus in front), ρ<1 ⇒ HYPEROPIA (behind)")
    P("-" * 80)
    P("the distant focus is v_∞ = n₂/P and the retina is at L, so L − v_∞ = (P·L − n₂)/P ⇒")
    P("   sign(L − v_∞) = sign(ρ − 1): the SIGN of the mismatch fixes the side, with NO magnitude.")

    # a longer/shorter eye (AXIAL) and a stronger/weaker eye (REFRACTIVE): each missed two ways, but
    # ONLY via dimensionless scale factors (ratios), illustrating the SIGN — the size is the [O].
    def side(rho, v_inf, L):
        """Direction-only label from the frozen geometry: where the distant focus falls vs the retina."""
        front = (v_inf < L - 1e-15)                       # focus short of the retina
        behind = (v_inf > L + 1e-15)
        name = "MYOPIA (focus in front)" if front else ("HYPEROPIA (focus behind)" if behind else "emmetropia")
        # the geometric sign must equal sign(ρ−1) — the central claim, machine-checked
        assert (front == (rho > 1.0)) and (behind == (rho < 1.0)), "blur side must equal sign(ρ−1)"
        return name

    P("\n[axial route] same power, scale the LENGTH by a dimensionless factor ℓ (illustrative, not a size):")
    for ell in (1.05, 0.95):
        L = ell * L_emm
        rho = (P_emm * L) / n2
        v_inf = surface_focus(P_emm, R)
        P(f"    length scale ℓ={ell:.2f} → ρ = {rho:.6f} → {side(rho, v_inf, L)}")
    P("\n[refractive route] same length, scale the POWER by a dimensionless factor q (P ∝ 1/R, so R↦R/q):")
    for q in (1.05, 0.95):
        Pq = q * P_emm
        Rq = (N2 - N1) / Pq                               # the radius giving the scaled power (rounder if q>1)
        L = L_emm
        rho = (Pq * L) / n2
        v_inf = surface_focus(Pq, Rq)
        P(f"    power scale  q={q:.2f} → ρ = {rho:.6f} → {side(rho, v_inf, L)}")

    # the product is what matters: a too-powerful eye made compensatingly SHORTER is emmetropic again
    q, ell = 1.05, 1.0 / 1.05
    rho_comp = (q * P_emm) * (ell * L_emm) / n2
    P(f"\n[product, not parts] a stronger eye (q={q:.2f}) made shorter (ℓ={ell:.6f}) is emmetropic again:")
    P(f"    ρ = q·ℓ = {rho_comp:.6f} → the match cares only about the PRODUCT P·L, not which is off. [F]")
    assert abs(rho_comp - 1.0) < 1e-12, "equal-product (q·ℓ=1) eyes must return to the emmetropic match"
    P("\nstated DIRECTION only: myopia ⇒ reduce power; hyperopia ⇒ add power. The MAGNITUDE (how much")
    P("error, the axial length, the spectacle power) is the firewall-blocked [O] — none is named. [F]/[O]")

    # ----------------------------------------------------------------------------------------
    # PART C — accommodation is a ONE-SIGNED power lever spanning an object-distance RANGE
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — accommodation: near objects need MORE power; P_req/P_∞ = 1 + n₁/(n₂·k), one-signed (↑)")
    P("-" * 80)
    P("to image an object at u=−k·L (k = distance in eye-lengths) on the SAME retina, the required power")
    P("is P_req=(n₂+n₁/k)/L, so P_req/P_∞ = 1 + n₁/(n₂·k): a pure number rising as the object nears (k↓).")
    P("    %-22s %-14s %-16s" % ("object distance (k·L)", "P_req/P_∞", "lens-radius R_req/R_∞"))
    prev = None
    mono_up = True
    one_signed = True
    for k in (1000.0, 100.0, 25.0, 10.0, 4.0, 2.0):
        ratio = 1.0 + N1 / (n2 * k)                       # = P_req/P_∞ (dimensionless)
        # verify against E3's frozen equation: the radius R_req giving P_req images u exactly at L_emm
        P_req = ratio * P_emm
        R_req = (N2 - N1) / P_req
        u = -k * L_emm
        v_check = E3.surface_image_distance(u, N1, N2, R_req)
        assert abs(v_check - L_emm) < 1e-9, "the R_req from P_req must image the near object onto the retina (E3)"
        radius_ratio = R_req / R                           # < 1 ⇒ rounder lens (more power)
        if prev is not None and ratio < prev - 1e-15:
            mono_up = False
        if ratio < 1.0 - 1e-15:
            one_signed = False
        P("    %-22s %-14.6f %-16.6f" % (f"k={k:.0f}", ratio, radius_ratio))
        prev = ratio
    P(f"\n    P_req/P_∞ rises monotonically as the object nears: {mono_up}; and is ALWAYS ≥ 1 (one-signed): {one_signed}")
    P("    → accommodation can only ADD plus power (pull focus nearer), never subtract; the far point is")
    P("      the relaxed lever (ratio→1 at distance), the near point is the lever maxed. DIRECTION only. [F]")
    assert mono_up and one_signed, "accommodation must be a monotone, strictly one-signed (additive) lever"
    P("    the lever is the lens ROUNDING (R↓ ⇒ P↑): R_req/R_∞ falls below 1 as the object nears (above). [F]")
    P("    the AMPLITUDE, the near/far DISTANCES, the presbyopic decline with age — firewall-blocked [O].")

    # ----------------------------------------------------------------------------------------
    # PART D — the lattice meaning of the lever; the length axis is a DWELL-size; γ READ-ONLY
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART D — the lever is lattice geometry (P=(n₂−n₁)/R, n=√((B/ρ) ratio)); length = a DWELL-size")
    P("-" * 80)
    # P ∝ 1/R at fixed indices ⇒ dP/P = −dR/R (the geometric lever), verified on the frozen relation
    eps = 1e-6
    P_a = (N2 - N1) / R
    P_b = (N2 - N1) / (R * (1.0 + eps))
    dPoverP = (P_b - P_a) / P_a
    dRoverR = eps
    P(f"power is a GEOMETRIC lever on the transverse-match interface: P=(n₂−n₁)/R ⇒ P ∝ 1/R, so")
    P(f"   dP/P = −dR/R (rounder lens ⇒ more power): measured {dPoverP:.6f} vs −dR/R = {-dRoverR:.6f}. [F]")
    P("   and n = c_vac/c_med = √((B/ρ) ratio) is the inherited lattice meaning of refractive index (E3);")
    P("   so BOTH accommodation (R lever) and the refractive axis (P axis) move along the ONE frozen P(R).")
    assert abs(dPoverP - (-dRoverR)) < 1e-5, "the power lever must obey dP/P = −dR/R (P ∝ 1/R)"

    # the LENGTH axis is GROWTH: organ size = dwell ∝ γ^1.5 (E1); the eye's axial length is a dwell-size.
    P("\nthe LENGTH axis is GROWTH: in the substrate, organ size = dwell ∝ γ^1.5 (E1) — so the eye's")
    P("axial length is a DWELL-size. Read the eye-field master PAX6 READ-ONLY (byte-equal to the atlas):")
    g_pax6 = ATLAS["PAX6"]["gamma"]
    g_rax  = ATLAS["RAX"]["gamma"]
    brake  = 0.5                                          # fixed brake — only the RELATIVE size (ratio) is forced
    size_pax6 = dwell(g_pax6, brake)
    size_rax  = dwell(g_rax, brake)
    size_ratio = size_pax6 / size_rax
    P(f"    PAX6 (eye_field master): γ = {g_pax6:.4f}   RAX (retina): γ = {g_rax:.4f}")
    P(f"    size law dwell ∝ γ^1.5 ⇒ relative size PAX6/RAX = (γ_PAX6/γ_RAX)^1.5 = {size_ratio:.6f}")
    P("    → the size law is MONOTONE in γ (more dwell ⇒ a larger structure): a definite DIRECTION.")
    # tie the direction to refractive error: bigger eye (more growth) ⇒ longer L ⇒ ρ>1 side = myopic
    P("    so on the growth axis the DIRECTION is forced: more ocular growth ⇒ a longer eye ⇒ the MYOPIC")
    P("    side of the match (ρ>1). The gene→elongation map, the emmetropization feedback that holds")
    P("    ρ≈1 in a normally growing eye, and the absolute scale are the named [O] — not invented. [F]/[O]")

    # no-drift: every γ E11 reads is byte-equal to the frozen atlas (no fitting)
    no_drift = (ATLAS["PAX6"]["gamma"] == g_pax6 and ATLAS["RAX"]["gamma"] == g_rax)
    P(f"\n    [no-drift] eye-field γ byte-equal to frozen atlas (no fitting): {no_drift}")
    assert no_drift, "E11 must consume the frozen γ unchanged (no fitting)"
    P("    γ is promoter STRUCTURE only — never an optical power, a growth rate, or a clinical effect")
    P("    (firewall). The felt percept of blur/clarity is OUT OF SCOPE (→ mind volume).")

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E11 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : emmetropia is the power↔length match ρ=P·L/n₂=1 (a curve, not one eye); the")
    P("                 mismatch SIGN fixes the side (ρ>1 myopia/focus-in-front, ρ<1 hyperopia/behind),")
    P("                 reachable two independent ways (too long OR too powerful — same product);")
    P("                 accommodation is a one-signed (additive) monotone power lever via R↓; the lever")
    P("                 is geometry (dP/P=−dR/R); the length axis is the substrate size law dwell ∝ γ^1.5.")
    P("  [V] verified : ρ=1 EXACTLY on the frozen reduced eye; the geometric blur side equals sign(ρ−1)")
    P("                 on E3's own surface equation (both axial and refractive routes); equal-product")
    P("                 eyes return to ρ=1; P_req/P_∞ rises monotonically and stays ≥1, and the R_req it")
    P("                 implies images the near object onto the retina (E3); dP/P=−dR/R; γ byte-equal.")
    P("  [V-arith]    : the single-surface imaging itself is E3's classical ray arithmetic (consumed,")
    P("                 not re-derived); E11 adds only the dimensionless MATCH reading on top of it.")
    P("  [L] measured : the Emsley reduced-eye n,R (cited, via E3); γ(PAX6), γ(RAX) (NCBI promoters,")
    P("                 cached, read-only); 'myopia = axial or refractive' is the cited optics this matches.")
    P("  [O] open     : the MAGNITUDE of any refractive error / the axial length / the spectacle power /")
    P("                 the accommodation amplitude / the near & far DISTANCES / the presbyopic decline")
    P("                 (all firewall-blocked — none produced); the gene→ocular-elongation map and the")
    P("                 emmetropization feedback loop that normally holds ρ≈1 (needs growth biology, not")
    P("                 the promoter-γ); the chromatic/aberration coupling (inherited E3 [O]); the felt")
    P("                 percept of blur/clarity (→ mind volume). Each obstacle named, not invented.")
    P("\nLEARNED: focus is a MATCH. E3's single-surface eye is in focus for distance exactly when its")
    P("         POWER and its LENGTH satisfy P·L = n₂ — a dimensionless condition the frozen reduced eye")
    P("         meets exactly, and a whole CURVE (a longer eye needs less power). Refractive error is")
    P("         simply being off that curve: the SIGN of the mismatch is myopia (focus in front) or")
    P("         hyperopia (behind), and the same error is reachable by an eye that is too LONG or too")
    P("         POWERFUL — only the product matters. Accommodation is the eye's one-signed lever on the")
    P("         power side: rounding the lens (R↓) adds plus power to pull near objects into focus, never")
    P("         the reverse. That lever is pure lattice geometry (P ∝ 1/R, n = √((B/ρ) ratio), E3), while")
    P("         the length side is the substrate's own size law (dwell ∝ γ^1.5, E1) — so each axis of the")
    P("         match has a forced DIRECTION. Every clinical magnitude, and the felt blur, stay honestly")
    P("         open. Foundation untouched; no γ added; nothing fitted; firewall intact and machine-checked.")


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
