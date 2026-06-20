#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seam_verify.py  --  Cross-package SEAM manifest verification + gate (the analogue of vasomotor_verify.py,
for the Section 5.3 seam-exposure layer rather than for a new disease mechanism).

The seam layer adds NO new mechanism and NO new constant, so the checks are about FIDELITY and HONESTY,
not about a physical sweep. Four layers of check, each auditable:

  (A) RE-EXPORT FIDELITY -- the INTERNAL-LIVE coupling values in the manifest must EQUAL the pathology
      layer's OWN return values, field by field. This is what makes "expose the already-internal link"
      truthful: the seam output IS the internal computation surfaced, not a parallel re-implementation.

  (B) COUPLING SIGN + CAUSAL LEVER -- the exposed coupling must carry the expected sign (screen removal
      RAISES the oncology hazard: every exposed RR > 1) AND the intervention must lower it (an exogenous
      sunscreen screen gives a smaller RR than the screen-removed state), demonstrating the screen is the
      causal lever, not a correlate.

  (C) PROVENANCE + CONTRACT VALIDITY -- every internal number must trace to a named pathology field (no
      orphan constant introduced by the seam), and every DECLARED-OUT seam must either point to a valid
      in-package dynamics-side target token (T1..T9 / oncology) or be explicitly flagged out-of-class
      with no target. No half-declared contract is allowed to pass silently.

  (D) NON-DISTURBANCE -- the seam READS the disease layers; it must not alter them. The pathology layer's
      own 2x-sha256 hash must still be the known value after the seam runs, and the seam has its own
      independent hash. (The core run_all.py battery is never imported here, so it is untouched a fortiori.)

seam_gate() is GREEN iff (A)-(D) all hold AND the manifest is bit-reproducible (2x sha256). It does NOT
touch the core gate (repro/_verify/gates.py): the core T1..T5+ONCO battery and the pathology, hair-cycle,
sebaceous, adhesion and vasomotor layers are all left frozen.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import seam_manifest as S

# the pathology layer's own determinism hash (frozen; the seam must not perturb it)
_PATHOLOGY_SHA = "0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8"
_VALID_TARGET_TOKENS = ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "oncology")


def _reexport_fidelity():
    """(A) the manifest's internal coupling must equal the pathology layer's own values, field by field."""
    import skin_pathology as PATHO
    man = S.pigment_loss_to_oncology()
    alb = PATHO.albinism(); can = PATHO.skin_cancer(); vit = PATHO.vitiligo()
    checks = {
        "scc_hazard_RR_screen_removed": man["scc_hazard_RR_screen_removed"] == alb["hazard_RR_albino_vs_pigmented"],
        "scc_incidence_RR_screen_removed": man["scc_incidence_RR_screen_removed"] == alb["incidence_RR_albino_vs_pigmented"],
        "scc_hazard_RR_with_sunscreen": man["scc_hazard_RR_with_sunscreen"] == alb["intervention_hazard_RR"],
        "melanoma_burst_RR_pigment_loss": man["melanoma_burst_RR_pigment_loss"] == can["pigment_loss_burst_RR"],
        "lesion_delivered_uv_attenuation": man["lesion_delivered_uv_attenuation"] == vit["disease_attenuation"],
    }
    return dict(status="PASS" if all(checks.values()) else "FAIL", field_matches=checks,
                description="every INTERNAL-LIVE coupling value equals the pathology layer's own return value "
                            "(the seam re-exports the internal link verbatim, it does not re-implement it)")


def _coupling_sign():
    """(B) screen removal raises the hazard (RR>1) and the intervention (sunscreen) lowers it again."""
    man = S.pigment_loss_to_oncology()
    raises = bool(man["scc_hazard_RR_screen_removed"] > 1.0 and man["melanoma_burst_RR_pigment_loss"] > 1.0)
    lever = bool(man["screen_is_causal_lever"]
                 and man["scc_hazard_RR_with_sunscreen"] < man["scc_hazard_RR_screen_removed"])
    full_screen_loss = bool(abs(man["lesion_delivered_uv_attenuation"] - 1.0) < 1e-9)
    ok = bool(raises and lever and full_screen_loss)
    return dict(status="PASS" if ok else "FAIL",
                hazard_rises_on_screen_loss=raises, sunscreen_lowers_hazard=lever,
                lesion_has_no_screen=full_screen_loss,
                description="the coupling carries the expected sign (a depigmenting lesion raises the oncology "
                            "hazard) and the screen is the causal lever (restoring it lowers the hazard)")


def _provenance_and_contracts(manifest):
    """(C) no orphan constant in the internal coupling; every OUT seam validly targeted or out-of-class."""
    internal = manifest["internal_live"][0]
    provenanced = all(k in internal["source_fields"] for k in (
        "scc_hazard_RR_screen_removed", "scc_incidence_RR_screen_removed", "scc_hazard_RR_with_sunscreen",
        "melanoma_burst_RR_pigment_loss", "lesion_delivered_uv_attenuation"))
    contract_ok = True
    contract_detail = []
    for seam in manifest["declared_out"]:
        if seam["kind"] == "out_of_class":
            ok = seam.get("target_package") is None
        elif seam["seam_id"] == "out__disease_wp__gene_lesion":
            ok = bool(seam.get("target_package")
                      and all(any(tok in e["dynamics_side"] for tok in _VALID_TARGET_TOKENS)
                              for e in seam["entities"]))
        else:
            ok = bool(seam.get("target_package") and seam.get("status"))
        contract_detail.append({seam["seam_id"]: ok}); contract_ok = contract_ok and ok
    in_ok = all(s.get("source_package") and s.get("grade") for s in manifest["inherited_in"])
    ok = bool(provenanced and contract_ok and in_ok and manifest.get("_no_new_constant") is True)
    return dict(status="PASS" if ok else "FAIL", internal_fully_provenanced=provenanced,
                out_contracts_valid=contract_ok, in_seams_sourced=in_ok,
                no_new_constant=manifest.get("_no_new_constant") is True, contract_detail=contract_detail,
                description="every internal number traces to a named pathology field (no orphan constant), "
                            "every declared-out seam is validly targeted or explicitly out-of-class, and every "
                            "inherited-in seam names its source package")


def _non_disturbance():
    """(D) the seam reads the pathology layer without altering it (its frozen hash is unchanged)."""
    import skin_pathology as PATHO
    _, patho_sha = PATHO._emit(PATHO.pathology_summary())
    ok = bool(patho_sha == _PATHOLOGY_SHA)
    return dict(status="PASS" if ok else "FAIL", pathology_sha_unchanged=ok,
                pathology_sha=patho_sha, expected=_PATHOLOGY_SHA,
                description="the pathology layer's own 2x-sha256 hash is unchanged after the seam runs "
                            "(the seam reads it, it does not perturb it); the core battery is never imported here")


def run_battery(manifest=None):
    man = manifest if manifest is not None else S.seam_manifest()
    a = _reexport_fidelity(); b = _coupling_sign(); c = _provenance_and_contracts(man); d = _non_disturbance()
    all_pass = all(x["status"] == "PASS" for x in (a, b, c, d))
    return dict(reexport_fidelity=a, coupling_sign=b, provenance_and_contracts=c, non_disturbance=d,
                counts=man["_counts"], all_pass=all_pass)


def determinism_ok():
    _, h1 = S._emit(S.seam_manifest()); _, h2 = S._emit(S.seam_manifest())
    return h1 == h2, h1


def seam_gate():
    """The seam layer's research-first gate (its analogue of vasomotor_gate())."""
    det, h = determinism_ok()
    b = run_battery()
    green = bool(det and b["all_pass"])
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "reexport_fidelity_ok": b["reexport_fidelity"]["status"] == "PASS",
            "coupling_sign_ok": b["coupling_sign"]["status"] == "PASS",
            "provenance_and_contracts_ok": b["provenance_and_contracts"]["status"] == "PASS",
            "non_disturbance_ok": b["non_disturbance"]["status"] == "PASS",
            "all_green": green}


if __name__ == "__main__":
    b = run_battery(); g = seam_gate()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\nseam_gate:", json.dumps(g, ensure_ascii=False))
    print("ALL PASS:", b["all_pass"], "(the cross-package-seams section is written only when this is green)")
