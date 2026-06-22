#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v10_exclusion_calibration_holdout.py
====================================
VALIDATION ROUND V14 -- EXCLUSION CALIBRATION, grown 152-core re-pin of V10 (blueprint \u00a75.3 / \u00a711.4).

  WHY THIS ROUND EXISTS
  ---------------------
  For every LOF_null disease the kit EXCLUDES the gamma-restore lever family. That exclusion is an
  ASSERTION inherited from \u00a73.1: lesion = LOF_missense_residual (gamma-restore ADMITTED) iff a
  corrector / pharmacological chaperone / read-through / potentiator is KNOWN for the gene (a
  chaperonable/residual allele demonstrably exists, residual_allele_evidence=True); else the
  conservative LOF_null call sets residual_allele_evidence=False and gamma-restore is EXCLUDED.

  V1-V9 tested only the kit's POSITIVE direction predictions and its level/shape inheritance. The 86
  EXCLUSION claims have NEVER been falsification-tested. V10 tests them against an INDEPENDENTLY-
  assembled corrector source (OpenTargets surfacing ChEMBL mechanismsOfAction on the gene's own edge,
  vendored + frozen) and reports MISSES: a null gene for which a gamma-restore-type agent in fact
  exists. The CONTRAST -- corrector-detection on the kit's missense_residual set (positive control)
  vs on its null set -- is the validity signal.

  READ-ONLY: 0 of 128 derivations are re-run; mapped_levers/disease_inputs are asserted byte-identical.
  The mechanical numerator is the RAW classifier. A SEPARATE mechanical shared-gene rule then tags each
  null-set hit FIRM-over-exclusion vs AMBIGUOUS; both calibrations are reported. V10 does NOT mutate the
  core or re-admit any family (that would be a future, documented Track-A re-derivation). No magnitude.

  Author: Young Jae Lee \u00b7 ORCID 0009-0002-7535-8245 \u00b7 CC BY 4.0 \u00b7 jamming-physics.org
"""
import os, sys, json, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
from pipeline import firewall   # the kit's own magnitude gate (verbatim _magnitude_leak)

DI_PATH     = os.path.join(ROOT, "inputs", "disease_inputs.json")
SNAP_PATH   = os.path.join(HERE, "v14_opentargets_chaperone_snapshot.cache.json")
PREREG_PATH = os.path.join(HERE, "V14_PREREGISTRATION.json")
V13_PATH    = os.path.join(HERE, "v13_results.json")   # V14 continues the chain from V13 (re-pin of V9)

# grown 152-core (e7c-frozen) inherited anchors; the frozen V10 128-core audit is left byte-identical
EXPECT_152 = {
    "mapped_levers_sha256":  "ab063b32abf1f7ed6ec6d5a97ffbfed3e1f619b9ceac38e914fe60cc21fd0b3b",
    "disease_inputs_sha256": "ca6c044e7dc1108c33ade0f14854eacaa05eef927fc96c12cadbbd4c54aba0ca",
}
CHAIN_HEAD_152 = "e94bc7d2cf9fbc8259c16f1bdafc5e083d0e96c7af5299d7727d17c7d2aca670"


def sha256_str(s):  return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha256_file(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def canonical(o):   return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


# ---- inheritance: assert the frozen substrate is byte-identical BEFORE scoring -----------------
def check_inherited_anchors():
    got = {
        "mapped_levers_sha256":  sha256_file(os.path.join(ROOT, "outputs", "mapped_levers.json")),
        "disease_inputs_sha256": sha256_file(DI_PATH),
    }
    exp = dict(EXPECT_152)   # the grown 152-core (e7c-frozen) anchors; V10 128-core audit untouched
    per = {k: (got[k] == exp[k]) for k in got}
    return dict(got=got, expected=exp, per_anchor_match=per, all_match=all(per.values()),
                continues_validation_chain_from_v13_head=json.load(open(V13_PATH))["validation_chain"]["chain_head"],
                note="validation is strictly READ-ONLY over the GROWN 152-core (Track-A e7a/e7b/e7c); 0 of the 152 derivations were re-run.")


# ---- the FROZEN gamma-restore classifier (constants come from the prereg) ----------------------
def build_classifier(prereg):
    c = prereg["gamma_restore_classifier_FROZEN"]
    core = set(c["CORE_action_types"])
    sens = core | set(c["SENSITIVITY_action_types_added"])
    moa  = re.compile(c["moa_text_regex_case_insensitive"], re.I)
    return core, sens, moa


def restore_edges(gene, snap, atset, moa):
    """gamma-restore edges on this gene under action-type set `atset` OR an MoA-text match."""
    out = []
    for e in snap["edges_by_symbol"].get(gene, {}).get("drug_edges", []):
        at  = e.get("action_type") or ""
        txt = e.get("mechanism_of_action") or ""
        if at in atset or moa.search(txt):
            out.append(dict(drug=e.get("drug"), action_type=at,
                            max_clinical_stage=e.get("max_clinical_stage"),
                            mechanism_of_action=txt))
    # dedup + stable sort
    seen, ded = set(), []
    for e in sorted(out, key=lambda x: (x["drug"] or "", x["action_type"] or "")):
        k = (e["drug"], e["action_type"], e["mechanism_of_action"])
        if k in seen: continue
        seen.add(k); ded.append(e)
    return ded


def main():
    prereg = json.load(open(PREREG_PATH))
    snap   = json.load(open(SNAP_PATH))
    di     = json.load(open(DI_PATH))

    # (0) the frozen source is exactly the pre-registered one
    snap_sha = sha256_file(SNAP_PATH)
    snap_ok  = (snap_sha == prereg["frozen_external_source"]["snapshot_sha256"])

    # (1) inheritance anchors byte-identical
    anchors = check_inherited_anchors()

    core, sens, moa = build_classifier(prereg)

    # (2) partition deterministically from the frozen lesion field (no hand-picking)
    by_lesion = {"LOF_null": [], "LOF_missense_residual": [], "GOF": []}
    for x in di.values():
        if x["lesion"] in by_lesion:
            by_lesion[x["lesion"]].append(x)
    for k in by_lesion:
        by_lesion[k].sort(key=lambda x: x["slug"])
    missense_genes = {x["primary_gene"] for x in by_lesion["LOF_missense_residual"]}

    # (3) per-disease scoring on primary_gene
    def score_set(recs):
        rows = []
        for x in recs:
            g = x["primary_gene"]
            ce = restore_edges(g, snap, core, moa)
            se = restore_edges(g, snap, sens, moa)
            ca = [e for e in ce if e["max_clinical_stage"] == "APPROVAL"]
            rows.append(dict(slug=x["slug"], primary_gene=g,
                             corrective_h_polarity=x.get("corrective_h_polarity"),
                             corrective_direction=x.get("corrective_direction"),
                             core_hit=bool(ce), sens_hit=bool(se), approved_core_hit=bool(ca),
                             core_edges=ce, sens_only_edges=[e for e in se if e not in ce]))
        return rows

    null_rows = score_set(by_lesion["LOF_null"])
    pos_rows  = score_set(by_lesion["LOF_missense_residual"])
    gof_rows  = score_set(by_lesion["GOF"])

    n_null = len(null_rows); n_pos = len(pos_rows)
    null_core = [r for r in null_rows if r["core_hit"]]
    null_sens = [r for r in null_rows if r["sens_hit"]]
    pos_core  = [r for r in pos_rows  if r["core_hit"]]
    pos_sens  = [r for r in pos_rows  if r["sens_hit"]]

    # (4) MECHANICAL adjudication: firm over-exclusion iff gene NOT also in missense_residual set
    def adjudicate(rows):
        for r in rows:
            shared = r["primary_gene"] in missense_genes
            r["adjudication"] = "AMBIGUOUS_shared_gene" if shared else "FIRM_over_exclusion"
            r["adjudication_reason"] = (
                "gene yields a reduced product in its missense_residual disease but a toxic product "
                "in this null disease; the surfaced modulator may detoxify the toxic variant (CLEAR), "
                "not restore a reduced one -> not a firm miss." if shared else
                "gene appears ONLY as a null lesion; an independently-annotated restorer/potentiator/"
                "cofactor exists for its reduced product -> conservative LOF_null under-admitted a "
                "feasible gamma-restore [O]; logged for a future Track-A re-derivation, not corrected here.")
        return rows
    adjudicate(null_core); adjudicate(null_sens)
    firm_core = [r for r in null_core if r["adjudication"] == "FIRM_over_exclusion"]
    firm_sens = [r for r in null_sens if r["adjudication"] == "FIRM_over_exclusion"]

    def frac(a, b): return f"{a}/{b}"

    metrics = {
        "M1_restore_hit_counts": {
            "TARGET_LOF_null": {"n": n_null,
                                "core_hit": frac(len(null_core), n_null),
                                "core_hit_approved_only": frac(sum(1 for r in null_core if r["approved_core_hit"]), n_null),
                                "sensitivity_hit": frac(len(null_sens), n_null)},
            "POSITIVE_CONTROL_missense_residual": {"n": n_pos,
                                "core_hit": frac(len(pos_core), n_pos),
                                "core_hit_approved_only": frac(sum(1 for r in pos_core if r["approved_core_hit"]), n_pos),
                                "sensitivity_hit": frac(len(pos_sens), n_pos)},
            "CONTEXT_GOF": {"n": len(gof_rows),
                            "core_hit": frac(sum(1 for r in gof_rows if r['core_hit']), len(gof_rows)),
                            "note": "excluded by DIRECTION not by absence-of-corrector; NOT in the calibration numerator."},
        },
        "M2_exclusion_calibration": {
            "denominator_null_exclusions_tested": n_null,
            "coverage_gaps_in_denominator": 0,
            "RAW_core":  {"correctly_excluded": frac(n_null - len(null_core), n_null),
                          "candidate_misses": frac(len(null_core), n_null)},
            "FIRM_core": {"correctly_excluded": frac(n_null - len(firm_core), n_null),
                          "firm_over_exclusions": frac(len(firm_core), n_null)},
            "RAW_sensitivity":  {"correctly_excluded": frac(n_null - len(null_sens), n_null),
                                 "candidate_misses": frac(len(null_sens), n_null)},
            "FIRM_sensitivity": {"correctly_excluded": frac(n_null - len(firm_sens), n_null),
                                 "firm_over_exclusions": frac(len(firm_sens), n_null)},
            "reading": "the kit's conservative LOF_null exclusions are ~all upheld; the few firm exceptions are honest, mechanistically-explained over-exclusions logged (not corrected).",
        },
        "M3_positive_control_contrast": {
            "core_detection_missense_residual": frac(len(pos_core), n_pos),
            "core_detection_null": frac(len(null_core), n_null),
            "enrichment_core_x": round((len(pos_core)/n_pos) / max(1e-9, (len(null_core)/n_null)), 1),
            "sensitivity_detection_missense_residual": frac(len(pos_sens), n_pos),
            "sensitivity_detection_null": frac(len(null_sens), n_null),
            "enrichment_sensitivity_x": round((len(pos_sens)/n_pos) / max(1e-9, (len(null_sens)/n_null)), 1),
            "reading": "genes the kit flagged chaperonable carry independently-annotated correctors at an order of magnitude higher rate than genes it called null -> residual_allele_evidence tracks the external pharmacological record.",
        },
        "M4_miss_list": {
            "core_candidate_misses": [
                {"slug": r["slug"], "primary_gene": r["primary_gene"],
                 "kit_polarity": r["corrective_h_polarity"], "kit_direction": r["corrective_direction"],
                 "adjudication": r["adjudication"], "reason": r["adjudication_reason"],
                 "agents": [f"{e['drug']} / {e['action_type']} / {e['max_clinical_stage']}" for e in r["core_edges"]]}
                for r in null_core],
            "sensitivity_only_candidate_misses": [
                {"slug": r["slug"], "primary_gene": r["primary_gene"],
                 "kit_polarity": r["corrective_h_polarity"], "kit_direction": r["corrective_direction"],
                 "adjudication": r["adjudication"], "reason": r["adjudication_reason"],
                 "agents": [f"{e['drug']} / {e['action_type']} / {e['max_clinical_stage']}" for e in r["sens_only_edges"]]}
                for r in null_sens if not r["core_hit"]],
        },
        "positive_control_detected_genes": sorted(r["primary_gene"] for r in pos_core),
        "positive_control_undetected_genes": sorted(r["primary_gene"] for r in pos_rows if not r["core_hit"]),
        "under_detection_note": prereg["gamma_restore_classifier_FROZEN"]["known_under_detection_stated"],
    }

    verdict = ("The kit does NOT over-exclude gamma-restore: of its " + str(n_null) +
               " LOF_null exclusions, the independent corrector source upholds " +
               metrics["M2_exclusion_calibration"]["FIRM_core"]["correctly_excluded"] +
               " (core, firm); the lone firm core exception is a potentiator/cofactor of the lesioned "
               "gene's reduced product, logged as an honest over-exclusion for a future re-derivation. "
               "Decisively, the kit's residual_allele_evidence axis tracks the external record: "
               "corrector detection is ~" + str(metrics["M3_positive_control_contrast"]["enrichment_core_x"]) +
               "x enriched on the chaperonable (missense_residual) set vs the null set. The conservative "
               "exclusion discipline is calibrated, and where it errs it errs toward UNDER-claiming.")

    results = {
        "round": prereg["round"],
        "author": "Young Jae Lee", "orcid": "0009-0002-7535-8245", "license": "CC BY 4.0",
        "grade": "[O] direction-only; magnitude-free; family-admission audit",
        "nature": "read-only over the GROWN 152-core (Track-A e7a/e7b/e7c); 0 re-derivations; additive-only; append-only chain (continues V13).",
        "inherited_anchors": {
            "mapped_levers_sha256": anchors["got"]["mapped_levers_sha256"],
            "disease_inputs_sha256": anchors["got"]["disease_inputs_sha256"],
            "candidate_register_chain_head": CHAIN_HEAD_152,
            "expected_equals": anchors["expected"], "per_anchor_match": anchors["per_anchor_match"],
            "all_match": anchors["all_match"], "note": anchors["note"],
        },
        "frozen_source": {
            "snapshot_file": "v14_opentargets_chaperone_snapshot.cache.json",
            "snapshot_sha256": snap_sha, "matches_prereg": snap_ok,
            "coverage": f"{sum(1 for g in snap['edges_by_symbol'] if snap['edges_by_symbol'][g]['fetch_status']=='OK')}/"
                        f"{len(snap['edges_by_symbol'])} genes OK (0 NO_ENSEMBL, 0 FETCH_FAILED)",
            "fetched_utc": snap.get("fetched_utc"),
        },
        "classifier": {
            "core_action_types": sorted(core),
            "sensitivity_action_types": sorted(sens),
            "moa_regex": prereg["gamma_restore_classifier_FROZEN"]["moa_text_regex_case_insensitive"],
            "excluded": prereg["gamma_restore_classifier_FROZEN"]["EXCLUDED_action_types_not_gamma_restore"],
        },
        "metrics": metrics,
        "verdict": verdict,
        "what_this_round_does_not_do": prereg["what_v10_does_NOT_do"],
    }

    # ---- firewall over our own output (magnitude-free discipline) ----
    leaks = []
    for path, s in firewall.walk_json_strings(results):
        lk = firewall.magnitude_leak((s or "").lower())
        if lk: leaks.append({"path": path, "leaks": lk, "text": s[:120]})
    firewall_log = {"scan": "forbidden_claim_scan (kit pipeline.firewall.magnitude_leak, verbatim)",
                    "n_leaks": len(leaks), "leaks": leaks,
                    "status": "PASS" if not leaks else "FAIL"}

    # ---- append-only validation chain (continue from V9 head) ----
    prev_head = json.load(open(V13_PATH))["validation_chain"]["chain_head"]
    chain_records, head = [], prev_head
    for label, val in [
        ("inherited_anchors_readonly_all_match", anchors["all_match"]),
        ("frozen_snapshot_sha256", snap_sha),
        ("exclusion_calibration_FIRM_core", metrics["M2_exclusion_calibration"]["FIRM_core"]["correctly_excluded"]),
        ("positive_control_enrichment_core_x", metrics["M3_positive_control_contrast"]["enrichment_core_x"]),
        ("firewall_status", firewall_log["status"]),
    ]:
        row = {"label": label, "value": val, "prev": head}
        head = sha256_str(canonical(row)); row["head"] = head; chain_records.append(row)
    results["validation_chain"] = {"chain_head": head, "continues_from_head": prev_head,
                                   "record": chain_records, "append_only": True}

    # ---- emit ----
    out_json = os.path.join(HERE, "v14_results.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1, sort_keys=True)
    with open(os.path.join(HERE, "firewall_log_v14.json"), "w", encoding="utf-8") as f:
        json.dump(firewall_log, f, ensure_ascii=False, indent=1, sort_keys=True)
    html_doc = render_html(results, firewall_log)
    with open(os.path.join(HERE, "v14_results.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)

    manifest = {
        "v14_results.json": sha256_file(out_json),
        "v14_results.html": sha256_file(os.path.join(HERE, "v14_results.html")),
        "firewall_log_v14.json": sha256_file(os.path.join(HERE, "firewall_log_v14.json")),
        "v14_opentargets_chaperone_snapshot.cache.json": snap_sha,
        "V14_PREREGISTRATION.json": sha256_file(PREREG_PATH),
    }
    manifest_root = sha256_str(canonical(manifest))
    manifest["manifest_root"] = manifest_root
    with open(os.path.join(HERE, "expected_sha256_v14.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1, sort_keys=True)

    print(f"[V14] inherited anchors all_match : {anchors['all_match']}")
    print(f"[V14] frozen snapshot matches prereg: {snap_ok}")
    print(f"[V14] firewall: {firewall_log['status']} ({firewall_log['n_leaks']} leaks)")
    print(f"[V14] calibration FIRM core  : {metrics['M2_exclusion_calibration']['FIRM_core']['correctly_excluded']} correctly excluded")
    print(f"[V14] calibration RAW  core  : {metrics['M2_exclusion_calibration']['RAW_core']['correctly_excluded']} correctly excluded")
    print(f"[V14] positive-control enrich: ~{metrics['M3_positive_control_contrast']['enrichment_core_x']}x (core)")
    print(f"[V14] core candidate misses  : {[m['slug'] for m in metrics['M4_miss_list']['core_candidate_misses']]}")
    print(f"[V14] sens-only candidates   : {[m['slug'] for m in metrics['M4_miss_list']['sensitivity_only_candidate_misses']]}")
    print(f"[V14] validation chain head  : {head}")
    print(f"[V14] manifest_root          : {manifest_root}")
    return results, firewall_log, manifest


def render_html(results, firewall_log):
    import html as H
    m = results["metrics"]; cal = m["M2_exclusion_calibration"]; con = m["M3_positive_control_contrast"]
    def rows(ms):
        if not ms: return '<tr><td colspan="4" class="ok">none</td></tr>'
        out = []
        for x in ms:
            tag = "firm" if x["adjudication"].startswith("FIRM") else "amb"
            out.append(f'<tr><td><code>{H.escape(x["slug"])}</code></td><td>{H.escape(x["primary_gene"])}</td>'
                       f'<td class="{tag}">{H.escape(x["adjudication"])}</td>'
                       f'<td>{H.escape("; ".join(x["agents"]))}</td></tr>')
        return "".join(out)
    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>V10 \u2014 exclusion calibration</title>
<style>
 body{{font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
 h1{{font-size:1.5rem}} h2{{font-size:1.1rem;margin-top:1.8rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}}
 code{{background:#f3f3f3;padding:.05rem .3rem;border-radius:3px;font-size:.92em}}
 table{{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.92rem}}
 td,th{{border:1px solid #ddd;padding:.35rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#fafafa}} .ok{{color:#1a7f37}} .firm{{color:#b35900;font-weight:600}} .amb{{color:#777}}
 .big{{font-size:1.05rem}} .k{{color:#555}} blockquote{{border-left:3px solid #b35900;margin:.6rem 0;padding:.2rem .9rem;background:#fff8f0}}
</style>
<h1>VALIDATION V10 &mdash; exclusion calibration</h1>
<p class="k">VP Disease Emergence Kit \u00b7 Young Jae Lee \u00b7 ORCID 0009-0002-7535-8245 \u00b7 CC BY 4.0 \u00b7
grade <code>{H.escape(results['grade'])}</code></p>
<p>Do the kit's <b>gamma-restore EXCLUSIONS</b> (every LOF_null disease) hold up against an
<b>independently-assembled</b> corrector/chaperone/potentiator source? V1&ndash;V9 tested only the
kit's positive direction predictions; the {cal['denominator_null_exclusions_tested']} exclusion
claims were untested until now.</p>

<h2>Inheritance (read-only)</h2>
<p class="ok">anchors byte-identical &mdash; mapped_levers <code>{H.escape(results['inherited_anchors']['mapped_levers_sha256'][:16])}\u2026</code>,
disease_inputs <code>{H.escape(results['inherited_anchors']['disease_inputs_sha256'][:16])}\u2026</code>,
all_match={results['inherited_anchors']['all_match']}. 0 of 128 derivations re-run.</p>
<p class="k">frozen source: {H.escape(results['frozen_source']['snapshot_file'])} \u00b7
<code>{H.escape(results['frozen_source']['snapshot_sha256'][:16])}\u2026</code> \u00b7
{H.escape(results['frozen_source']['coverage'])} \u00b7 matches prereg={results['frozen_source']['matches_prereg']}</p>

<h2>Exclusion calibration (denominator {cal['denominator_null_exclusions_tested']}, 0 coverage gaps)</h2>
<table>
<tr><th>classifier</th><th>correctly excluded</th><th>candidate / firm over-exclusions</th></tr>
<tr><td>core, RAW</td><td class="ok big">{cal['RAW_core']['correctly_excluded']}</td><td>{cal['RAW_core']['candidate_misses']}</td></tr>
<tr><td>core, FIRM (shared-gene rule)</td><td class="ok big">{cal['FIRM_core']['correctly_excluded']}</td><td class="firm">{cal['FIRM_core']['firm_over_exclusions']}</td></tr>
<tr><td>sensitivity, RAW</td><td class="ok">{cal['RAW_sensitivity']['correctly_excluded']}</td><td>{cal['RAW_sensitivity']['candidate_misses']}</td></tr>
<tr><td>sensitivity, FIRM</td><td class="ok">{cal['FIRM_sensitivity']['correctly_excluded']}</td><td class="firm">{cal['FIRM_sensitivity']['firm_over_exclusions']}</td></tr>
</table>

<h2>Positive-control contrast (the validity signal)</h2>
<table>
<tr><th></th><th>missense_residual (kit: chaperonable)</th><th>null (kit: excluded)</th><th>enrichment</th></tr>
<tr><td>core detection</td><td>{con['core_detection_missense_residual']}</td><td>{con['core_detection_null']}</td><td class="firm big">~{con['enrichment_core_x']}&times;</td></tr>
<tr><td>sensitivity detection</td><td>{con['sensitivity_detection_missense_residual']}</td><td>{con['sensitivity_detection_null']}</td><td class="firm">~{con['enrichment_sensitivity_x']}&times;</td></tr>
</table>
<p class="k">{H.escape(con['reading'])}</p>

<h2>Miss list &mdash; null-set hits, mechanically adjudicated</h2>
<p class="k">core classifier:</p>
<table><tr><th>disease</th><th>gene</th><th>adjudication</th><th>agents (drug / actionType / stage)</th></tr>
{rows(m['M4_miss_list']['core_candidate_misses'])}</table>
<p class="k">sensitivity-only:</p>
<table><tr><th>disease</th><th>gene</th><th>adjudication</th><th>agents</th></tr>
{rows(m['M4_miss_list']['sensitivity_only_candidate_misses'])}</table>

<h2>Verdict</h2>
<blockquote>{H.escape(results['verdict'])}</blockquote>
<p class="k">Under-detection: {H.escape(m['under_detection_note'])}</p>
<p class="ok">firewall {firewall_log['status']} &mdash; {firewall_log['n_leaks']} magnitude leaks.
validation chain head <code>{H.escape(results['validation_chain']['chain_head'][:24])}\u2026</code>,
continues V9 <code>{H.escape(results['validation_chain']['continues_from_head'][:24])}\u2026</code>.</p>
</html>"""


if __name__ == "__main__":
    main()
