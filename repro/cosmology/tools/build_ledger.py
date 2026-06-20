#!/usr/bin/env python3
"""
build_ledger.py — VP_SPEC v1.8 Constitution C3 (irreproducibility ledger).

Aggregates, in one place, every quantity or result the cosmology volume does NOT
reproduce from first principles within its own scope, each marked [O] with a
reason and a canonical location.

Two tiers:
  A. Locked quantities held as input/anchor — derived from tools/cos_locks.json
     (badge ∈ {open, calibrated}); imported locks are listed separately as
     reproducible by cross-volume DOI.
  B. Documented open problems / out-of-scope empirical normalizations —
     transcribed from the canonical honest-ledger chapter (§16) and
     REMAINING_OPEN_PROBLEMS.md, each with its canonical chapter citation.

Every row's status is HYP / [INPUT] / degenerate, consistent with the volume's
discipline: these are gaps or conditionals, not contradictions.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCKS = json.load(open(ROOT / "tools" / "cos_locks.json", encoding="utf-8"))["locks"]
OUT = ROOT / "IRREPRODUCIBILITY_LEDGER.md"

CHAP = "https://jamming-physics.org/cosmology"

# Tier B — open problems documented in the canonical text (with locations).
OPEN_PROBLEMS = [
    ("absolute acoustic length L ≈ 150 Mpc (ℓ ≈ 220)",
     "[O] empirical normalization",
     "Mechanism closed without a Big Bang (HYP): one fixed inflow-shell length "
     "sets both the BAO real-space peak and the P(k) oscillation spacing, and 2 "
     "of 3 success conditions (1:2:3 standing-wave heights, harmless γ-ray "
     "dispersion) are met. The remaining condition — deriving the *absolute* "
     "150 Mpc from lattice/inflow constants — stays open: the needed factor "
     "≈28.6 of the Hubble length has no forced π-chain or geometric basis, so it "
     "is reclassified as an empirical normalization (same box as BBN, absolute "
     "g, absolute 2.725 K) rather than tuned.",
     "§14·15", "14-cmb-anisotropies-acoustic-scale",
     "repro/cosmology/14-cmb-anisotropies-acoustic-scale/derive_acoustic_length.py"),

    ("supernova Hubble-diagram fit vs ΛCDM",
     "[O] data-limited (degenerate)",
     "The static lattice-optics distance law d_L=(c/H₀)(1+z)ln(1+z) fits the SN "
     "Hubble diagram with a single marginalised offset at χ²/dof = 0.50, against "
     "0.44 for ΛCDM (Ω_Λ=0.7); the two laws differ by at most |Δμ| = 0.145 mag. "
     "The fit is statistically degenerate with ΛCDM, so present data cannot "
     "distinguish them — a data limitation, not a contradiction. No dark-energy "
     "term is used.",
     "§7 (cited §12)", "07-non-expanding-lattice-optics-cosmology",
     "repro/cosmology/07-non-expanding-lattice-optics-cosmology/"),

    ("absolute CMB temperature 2.725 K",
     "[O] empirical normalization",
     "Mechanism closed (a warm present lattice emits thermal radiation = light, "
     "§9); the absolute temperature is anchored to the observed radiation density "
     "(~80× starlight) and a full energy balance is still required. Out of scope, "
     "not contradicted.",
     "§9", "09-microwave-background-present-lattice-emission", ""),

    ("two length scales ratio D/a ≈ 7.7×10⁶",
     "[O] input (deferred to physics volume)",
     "The ratio of the angular scale D = 4.8526 pm to the cell size a = "
     "6.33×10⁻¹⁹ m is an imported absolute scale; its origin is a physics-volume "
     "question, left as input here.",
     "Appendix C", "axc-two-length-scales-d-versus", ""),

    ("post-Newtonian second-order coefficient β = 1",
     "[O] assumption (degenerate)",
     "β = 1 is assumed, making the sector fully degenerate with General "
     "Relativity at this order; the second-order coefficient is not independently "
     "derived.",
     "§10", "10-post-newtonian-sector", ""),

    ("gamma-ray vacuum dispersion",
     "[O] relaxed, not fully closed",
     "The sharpest tension of the lattice-light identification; relaxed but not "
     "fully closed, and mutually constrained with the acoustic-length program "
     "(§1 of the open-problems ledger).",
     "§2", "02-light-lattice-elastic-wave-sharpest", ""),
]

BADGE_NOTE = {
    "open": ("[O] input — open",
             "Held as a raw input; the mechanism behind its time-evolution is an "
             "explicit open question (E-COSMO), deferred to the physics volume "
             "§17.5."),
    "calibrated": ("[O] input — single absolute anchor",
                   "Fixed by one empirical anchor (the absolute surface-gravity / "
                   "G normalization, the 'four-wall' problem); the absolute scale "
                   "is deferred to the physics volume, not derived here."),
}


def main():
    L = []
    L.append("# Irreproducibility Ledger — Vacuum-Inflow Cosmology")
    L.append("")
    L.append("VP_SPEC v1.8 · Constitution **C3**. Every quantity or result that this "
             "volume does **not** reproduce from first principles within its own "
             "scope is collected here, marked `[O]` with a reason and a canonical "
             "location. Consistent with the volume's discipline (\"present facts in "
             "present physics; origins unclaimed; *exhibiting a mechanism ≠ "
             "deriving a value*\"), every entry is a **gap or a conditional, not a "
             "contradiction**. No parameter below is tuned to fit data.")
    L.append("")

    # Tier A
    L.append("## A. Locked quantities held as input or anchor")
    L.append("")
    L.append("Derived from the locked-quantity registry (`tools/cos_locks.json`).")
    L.append("")
    L.append("| quantity | mark | why irreproducible (in-scope) | canonical |")
    L.append("|---|---|---|---|")
    a_count = 0
    for lk in LOCKS:
        b = lk["badge"]
        if b in BADGE_NOTE:
            mark, why = BADGE_NOTE[b]
            loc = f"[{lk['canon_label']}]({CHAP}/{lk['canon_slug']}/)" \
                if lk.get("canon_label") else f"[{lk['canon_slug']}]({CHAP}/{lk['canon_slug']}/)"
            L.append(f"| {lk['display']} | `{mark}` | {why} | {loc} |")
            a_count += 1
    L.append("")
    imported = [lk for lk in LOCKS if lk["badge"] == "imported"]
    if imported:
        L.append("**Reproducible by cross-volume import (not irreproducible):** "
                 + "; ".join(f"{lk['display']}" for lk in imported)
                 + ". These come from the physics volume with their own DOI and "
                 "reproduction tree (see `registry/cross_volume_doi.csv`, "
                 "Appendix D).")
        L.append("")

    # Tier B
    L.append("## B. Documented open problems and out-of-scope normalizations")
    L.append("")
    L.append("Transcribed from the canonical honest-ledger chapter (§16) and "
             "`REMAINING_OPEN_PROBLEMS.md`.")
    L.append("")
    L.append("| item | mark | status | canonical | repro |")
    L.append("|---|---|---|---|---|")
    for name, mark, why, secs, slug, repro in OPEN_PROBLEMS:
        link = f"[{secs}]({CHAP}/{slug}/)"
        rep = f"`{repro}`" if repro else "—"
        # keep the table cell readable: status is the one-line reason
        L.append(f"| {name} | `{mark}` | {why} | {link} | {rep} |")
    L.append("")

    L.append("## Summary")
    L.append("")
    L.append(f"- Tier A: **{a_count}** locked quantities held as input/anchor "
             f"({len(imported)} further locks are reproducible by import).")
    L.append(f"- Tier B: **{len(OPEN_PROBLEMS)}** documented open problems / "
             f"empirical normalizations.")
    L.append("- The single largest open item is the **absolute** acoustic length "
             "150 Mpc; its mechanism is closed (Big-Bang-free) and only the "
             "absolute value remains an empirical normalization.")
    L.append("- Every item is in-scope-closed at the mechanism level, deferred to "
             "the physics volume, out of scope by the volume's own rule, or "
             "data-limited — none is a contradiction with observation.")
    L.append("")

    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote IRREPRODUCIBILITY_LEDGER.md  (Tier A {a_count}, "
          f"imported {len(imported)}, Tier B {len(OPEN_PROBLEMS)})")


if __name__ == "__main__":
    main()
