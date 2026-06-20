#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_seam.py  --  Cross-package SEAM entry point (HANDOFF Section 5.3). Drop into a fresh chat and run:
    python repro/run_seam.py

Builds the package's single labelled SEAM manifest for the "one body" runner. This is NOT a new mechanism
and adds NO new constant: it (1) EXPOSES the already-internal pigment-loss -> oncology coupling (a
melanocyte-target T3 lesion removes the melanin screen and the shared oncology hazard rises) by
re-exporting the verified pathology layer's own numbers verbatim; (2) declares the INHERITED-IN seams the
package vendors read-only (circulatory dermal-perfusion magnitude, DNA organ identity + measured gamma,
the R19 substrate); and (3) declares the OUT contracts to sibling packages (gene-lesion -> disease_wp;
immune / rheumatology seams; out-of-class infections) honestly as DECLARED, not yet live wiring. Writes
reports/seam_manifest.json (the machine-readable manifest) and reports/seam_results.json (the gate
record), prints the seam map + the live coupling + the 2x sha256. This is a RESEARCH artifact (no HTML);
it does NOT touch the core run_all.py gate (the core battery and every disease layer are read, never
altered -- this layer carries its own independent hash).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_oncology", "_pathology", "_seam"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
S = importlib.import_module("seam_manifest")
W = importlib.import_module("seam_verify")


def main():
    print("=" * 96)
    print("Integumentary  --  CROSS-PACKAGE SEAMS (5.3): the labelled IN / INTERNAL-LIVE / OUT manifest")
    print("=" * 96)

    man = S.seam_manifest(); s, h = S._emit(man)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "seam_manifest.json"), "w", encoding="utf-8").write(s)

    print("\n[1] SCOPE (no new mechanism, no new constant -- this is the seam record for the 'one body' runner)")
    print("    inherited-IN seams : %d   internal-LIVE seams : %d   declared-OUT seams : %d"
          % (man["_counts"]["inherited_in"], man["_counts"]["internal_live"], man["_counts"]["declared_out"]))

    print("\n[2] INHERITED-IN (read-only inputs vendored from a sibling; never re-derived here)")
    for sm in man["inherited_in"]:
        print("    %-34s <- %-12s  %s" % (sm["seam_id"], sm["source_package"], sm["imported"][:54]))

    print("\n[3] INTERNAL-LIVE (the Section 5.3 headline: pigment-loss -> oncology, re-exported from pathology)")
    c = man["internal_live"][0]
    print("    %s  :  %s  ->  %s" % (c["seam_id"], c["from_target"], c["to_target"]))
    print("    SCC hazard RR (screen removed vs pigmented) : %.4f   [incidence RR %.4f]"
          % (c["scc_hazard_RR_screen_removed"], c["scc_incidence_RR_screen_removed"]))
    print("    SCC hazard RR WITH sunscreen (screen restored): %.4f   (screen is the causal lever: %s)"
          % (c["scc_hazard_RR_with_sunscreen"], c["screen_is_causal_lever"]))
    print("    melanoma BURST RR on pigment loss            : %.4f   (lesion delivered-UV attenuation %.2f = no screen)"
          % (c["melanoma_burst_RR_pigment_loss"], c["lesion_delivered_uv_attenuation"]))
    print("    coupling raises hazard (expected sign): %s" % c["coupling_sign_raises_hazard"])

    print("\n[4] DECLARED-OUT (contracts to sibling packages -- DECLARED, not yet live wiring)")
    for sm in man["declared_out"]:
        tgt = sm["target_package"] if sm["target_package"] else "(out-of-class)"
        print("    %-38s -> %-20s %s" % (sm["seam_id"], tgt, sm["status"]))

    print("\n[5] VERIFICATION (fidelity + sign + contracts + non-disturbance)")
    batt = W.run_battery(manifest=man)
    for key in ("reexport_fidelity", "coupling_sign", "provenance_and_contracts", "non_disturbance"):
        print("    %-26s [%-4s]  %s" % (key, batt[key]["status"], batt[key]["description"][:58]))
    print("    all pass: %s" % batt["all_pass"])

    g = W.seam_gate()
    out = {"manifest_counts": man["_counts"], "battery": batt, "seam_gate": g}
    open(os.path.join(reports, "seam_results.json"), "w", encoding="utf-8").write(
        __import__("json").dumps(out, ensure_ascii=False, indent=2))

    det, _ = W.determinism_ok()
    print("\n[6] DETERMINISM (VP-SPEC C1)")
    print("    seam manifest 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    print("    seam_gate all_green: %s  (the cross-package-seams section is written only when this is green)" % g["all_green"])
    print("\nGrades: internal coupling shape [V] / cited epidemiology [L] / absolute RR [O] (oncology obstacle); "
          "inherited + declared seams carry the owning package's grade.")
    print("Core battery + every disease layer UNTOUCHED: they are read, never altered (this layer's hash is its own).")
    print("Wrote: reports/seam_manifest.json, reports/seam_results.json")


if __name__ == "__main__":
    main()
