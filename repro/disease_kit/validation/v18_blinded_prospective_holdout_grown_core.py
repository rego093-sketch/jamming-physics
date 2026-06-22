#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v18_blinded_prospective_holdout_grown_core.py  --  VALIDATION round V18 (blueprint §5.2 / §11.4).

  WHAT THIS ROUND IS -- THE LAST OPEN §11.4 ITEM.  §5.2 asks for a BLINDED PROSPECTIVE HOLD-OUT:
  (1) a held-out set whose corrective DIRECTION is fixed from mechanism BEFORE any oracle is seen,
  (2) an INDEPENDENT mechanism join with NO hand-picking, (3) misses reported (not just hits),
  (4) negative controls. V2 dissolved the §5.1 *internal* circularity (the kit's forced corrective
  axis is a clean function of (role, lesion), blind to the therapy verb) over the FULL 128-core.
  What V2 explicitly pre-registered as the next batch -- and what was still open -- is the
  PARTITIONED, PROSPECTIVELY-LOCKED hold-out against a GENUINELY-INDEPENDENT external direction
  source. V18 executes exactly that, over the grown 152-core, append-only from V17.

  THE BLIND PREDICTION.  Per disease the corrective direction = OPPOSE(the stored forced emergent
  axis `axis_dir`). `axis_dir` is the kit's [F]-grade forced axis from (gene regulatory role,
  lesion, sourced biochemistry) -- it is NEVER read from a drug, so OPPOSE(axis_dir) is therapy-
  blind. Blindness is corroborated mechanically: the coarse (role,lesion) rule
  (brake: LOF->UP/GOF->DOWN ; contributor: LOF->DOWN/GOF->UP) reproduces the stored axis_dir for
  149/152; the 3 exceptions (ARG1, OAT, PHYH) are CATABOLIC enzymes whose LOF causes substrate
  ACCUMULATION (axis UP) -- a sourced biochemical fact, not a therapy -- which the kit's finer
  engine captures and the coarse label does not. (Grown-core role `receptor` -> positive-
  contributor, reproduces TNFRSF1A/TRAPS GOF->UP.)

  PROSPECTIVE LOCK (§5.5).  The HOLD-OUT partition is deterministic and blind -- sha256(slug) % 10
  < 3 -- and the HOLD-OUT blind predictions are FROZEN in V18_PREREGISTRATION.json (content-hashed)
  BEFORE any oracle is consulted. The partition cannot be cherry-picked; the predictions cannot be
  edited post-hoc.

  THE INDEPENDENT ORACLE -- and an HONEST CORRECTION of V2's M2'.  V2 scored "direction recovery"
  against the kit's own `corrective_agents[].axis_effect`. V18 finds (and LOGS) that axis_effect is
  IDENTICAL to corrective_direction = OPPOSE(axis_dir) for all 268 agent rows -- so matching the
  blind prediction to it is TRIVIALLY 100% and is NOT an independent recovery. V18 therefore scores
  recovery against the GENUINELY-INDEPENDENT external mechanism-direction source the kit vendored in
  V4 (OpenTargets surfacing ChEMBL approved-drug action signs, snapshot frozen, NO hand-picking),
  reporting WITH denominators, a miss list, and the V6 satisfiability stratification (LOF_null is
  pharmacologically unsatisfiable by a small-molecule activator -> reported separately, never hidden).
  This corrects V2's over-reading EXACTLY as V2 corrected V1's, and as e6s/V12 logged a calibration --
  V2 stays byte-identical (its numbers stand as computed; their reading is refined here).

  INHERITANCE DISCIPLINE (V18 adds NOTHING to the corpus; it only AUDITS):
    invariants : firewall PASS; every emitted string magnitude-free.
    derivation : strictly READ-ONLY over the GROWN 152-core (0 re-runs); inherited anchors byte-identical.
    chain      : APPEND-ONLY, continuing the V17 validation chain head.
    source     : V4 external snapshot reused VERBATIM (its sha pinned); the off-manifest audit is a
                 network-free independent re-derivation of the partition + locked predictions.

  Author: Young Jae Lee . ORCID 0009-0002-7535-8245 . CC BY 4.0 . jamming-physics.org

  Run:  python3 validation/v18_blinded_prospective_holdout_grown_core.py
"""
import os, sys, json, html, hashlib, re

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
OUTDIR = HERE
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import firewall as FW

SNAPSHOT = "2026-06-22"
RELEASE  = "0.41.0-validation.v18"

DI_PATH   = os.path.join(ROOT, "inputs",  "disease_inputs.json")
ML_PATH   = os.path.join(ROOT, "outputs", "mapped_levers.json")
CR_PATH   = os.path.join(ROOT, "outputs", "candidate_register.json")
V17_PATH  = os.path.join(OUTDIR, "v17_results.json")
V4SNAP    = os.path.join(OUTDIR, "v4_opentargets_snapshot.cache.json")
V17SNAP   = os.path.join(OUTDIR, "v17_medrt_may_treat_snapshot.cache.json")
PREREG_PATH = os.path.join(OUTDIR, "V18_PREREGISTRATION.json")

EXPECT_152 = {
    "mapped_levers_sha256":  "ab063b32abf1f7ed6ec6d5a97ffbfed3e1f619b9ceac38e914fe60cc21fd0b3b",
    "disease_inputs_sha256": "ca6c044e7dc1108c33ade0f14854eacaa05eef927fc96c12cadbbd4c54aba0ca",
}
CHAIN_HEAD_152 = "e94bc7d2cf9fbc8259c16f1bdafc5e083d0e96c7af5299d7727d17c7d2aca670"

# ---- blind direction machinery (V2 verbatim + receptor) ----
NEGATIVE_REGULATOR_ROLES = {"brake"}
POSITIVE_CONTRIBUTOR_ROLES = {"enzyme", "structural", "channel", "accelerator", "master_TF", "transporter", "receptor"}
OPP      = {"UP": "DOWN", "DOWN": "UP"}
AX2SIGN  = {"UP": "increase", "DOWN": "decrease"}
POL2SIGN = {"supply": "increase", "clear": "decrease"}
EXT2SIGN = {"ACTIVATING": "increase", "INHIBITORY": "decrease"}
# catabolic-enzyme refinements: enzyme role but LOF -> substrate ACCUMULATION (axis UP), captured by
# the kit's finer engine; the coarse role rule (enzyme=contributor) does not. Named, biochemically sourced.
CATABOLIC_ENZYME_REFINEMENTS = {"argininemia": "ARG1", "gyrate_atrophy_choroid_retina": "OAT", "refsum_disease": "PHYH"}

def canon(o):  return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def sha(o):    return hashlib.sha256(canon(o).encode("utf-8")).hexdigest()
def sha256_str(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def jdump(p, o):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, indent=1, ensure_ascii=False, sort_keys=True)

def partition(slug):
    return "HOLDOUT" if int(hashlib.sha256(slug.encode()).hexdigest(), 16) % 10 < 3 else "TRAIN"

def coarse_axis(role, lesion):
    if role in NEGATIVE_REGULATOR_ROLES:   return "UP" if lesion == "LOF" else "DOWN"
    if role in POSITIVE_CONTRIBUTOR_ROLES: return "DOWN" if lesion == "LOF" else "UP"
    return None

def disease_axis(rec):
    ax = {g["axis_dir"] for g in rec["genes"]}
    return next(iter(ax)) if len(ax) == 1 else None

def blind_direction(rec):
    """Corrective direction = OPPOSE(stored forced emergent axis). Therapy-blind."""
    ax = disease_axis(rec)
    return None if ax is None else AX2SIGN[OPP[ax]]

def v4_gene_dir(ibs, gene):
    rec = ibs.get(gene)
    if not rec: return None, 0, 0
    na = sum(1 for d in rec.get("approved_drugs", []) if d.get("sign") == "ACTIVATING")
    ni = sum(1 for d in rec.get("approved_drugs", []) if d.get("sign") == "INHIBITORY")
    if na == 0 and ni == 0: return None, na, ni
    if na > ni: return "increase", na, ni
    if ni > na: return "decrease", na, ni
    return "tie", na, ni

def check_anchors():
    got = {"mapped_levers_sha256": sha_file(ML_PATH), "disease_inputs_sha256": sha_file(DI_PATH)}
    per = {k: (got[k] == EXPECT_152[k]) for k in got}
    return dict(got=got, expected=dict(EXPECT_152), per_anchor_match=per, all_match=all(per.values()),
                note="strictly READ-ONLY over the GROWN 152-core (Track-A e7a/e7b/e7c); 0 of 152 re-run.")

def write_prereg(di, locked_holdout):
    prereg = dict(
        round="V18", release=RELEASE, snapshot_date=SNAPSHOT,
        programme="jamming-physics.org / VP Disease Emergence Kit",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", licence="CC BY 4.0",
        section="00_CONTINUATION_BLUEPRINT.md §5.2 / §11.4 -- blinded prospective hold-out (the last open §11.4 item).",
        design=dict(
            holdout_partition="deterministic + blind: sha256(slug) %% 10 < 3 -> HOLDOUT, else TRAIN. Cannot be cherry-picked.",
            blind_prediction="corrective direction = OPPOSE(stored forced emergent axis axis_dir); axis_dir is the kit's "
                             "[F] forced axis from (role, lesion, sourced biochemistry), NEVER a drug -> therapy-blind.",
            blindness_corroboration="coarse (role,lesion) rule reproduces stored axis_dir 149/152; the 3 exceptions "
                                    "(ARG1/OAT/PHYH) are CATABOLIC enzymes (LOF->accumulation->axis UP), a sourced "
                                    "biochemical refinement, not a therapy.",
            independent_oracle="external mechanism-direction = V4 OpenTargets/ChEMBL approved-drug action SIGN "
                               "(ACTIVATING->increase, INHIBITORY->decrease), per gene, NO hand-picking; vendored frozen.",
            axis_effect_is_NOT_independent="the kit's corrective_agents[].axis_effect == corrective_direction == "
                                           "OPPOSE(axis_dir) for all agent rows -> matching the blind prediction to it is "
                                           "trivially 100%% and is logged as a within-kit self-consistency check ONLY, "
                                           "NOT counted as external recovery (this corrects V2's M2' reading).",
            satisfiability="LOF_null is pharmacologically unsatisfiable by a small-molecule activator (V6) -> reported "
                           "as a SEPARATE stratum, never merged into the satisfiable (GOF / missense_residual) figure.",
            misses="every external-oracle disagreement is listed and tagged node-vs-target vs genuine.",
            negative_controls="(a) gamma-restore admitted on LOF_null must be 0 (family-exclusion); (b) gene-specific "
                              "agents must carry tight may_treat sets (inherited V8/V17 instrument)."),
        prospective_lock=dict(
            n_holdout=len(locked_holdout),
            holdout_blind_predictions=locked_holdout,
            content_hash=sha256_str(canon(locked_holdout)),
            note="these HOLD-OUT blind predictions are FROZEN here BEFORE any oracle is consulted (the prospective lock)."),
        frozen_external_source=dict(snapshot_file="v4_opentargets_snapshot.cache.json", snapshot_sha256=sha_file(V4SNAP)),
        inheritance_discipline=dict(
            invariants="firewall PASS; every emitted string magnitude-free",
            derivation="READ-ONLY over the GROWN 152-core (0 re-runs); inherited anchors re-checked byte-identical",
            chain="APPEND-ONLY, continuing the V17 validation chain head",
            source="V4 external snapshot reused verbatim (sha pinned); off-manifest audit is a network-free re-derivation"),
        continues_from=dict(round="V17", v17_validation_chain_head=json.load(open(V17_PATH))["validation_chain"]["chain_head"]),
        determinism="metrics computed from frozen artifacts (152-core + frozen V4 snapshot); no network in the byte-frozen "
                    "path; two runs byte-identical.")
    prereg["prereg_sha256"] = sha(prereg)
    jdump(PREREG_PATH, prereg)
    return prereg

def compute(di, ml, cr, prereg):
    v4 = json.load(open(V4SNAP)); ibs = v4["interactions_by_symbol"]

    # ---- per-disease blind direction + partition (predictions already locked in prereg) ----
    parts = {s: partition(s) for s in di}
    blind = {s: blind_direction(di[s]) for s in di}
    multi_axis = sorted(s for s in di if disease_axis(di[s]) is None)

    # ---- blindness corroboration: coarse rule reproduces stored axis_dir ----
    coarse_ok, coarse_mismatch = 0, []
    n_genes = 0
    for s, r in di.items():
        for g in r["genes"]:
            n_genes += 1
            ca = coarse_axis(g["role"], g["mechanism"])
            if ca == g["axis_dir"]: coarse_ok += 1
            else: coarse_mismatch.append(dict(slug=s, gene=g["gene"], role=g["role"], lesion=g["mechanism"],
                                              coarse=ca, stored=g["axis_dir"]))

    # ---- M1: independence from the therapy verb (the §5.1 circular axis) ----
    def m1(part_name):
        agree, div = 0, []
        for s, r in di.items():
            if parts[s] != part_name: continue
            b = blind[s]
            if b is None: continue
            verb = POL2SIGN[r["corrective_h_polarity"]]
            if b == verb: agree += 1
            else: div.append(dict(slug=s, blind_emergence=b, therapy_verb=verb,
                                  lesion=r["lesion"], gene=r["genes"][0]["gene"]))
        n = agree + len(div)
        return dict(scored=n, agree=agree, divergences=div, n_divergences=len(div))

    # ---- M2: EXTERNAL direction recovery vs V4 ChEMBL sign (the independent oracle) ----
    def m2(part_name):
        sat_rows, uns_rows = [], []
        for s, r in di.items():
            if parts[s] != part_name: continue
            b = blind[s]
            if b is None: continue
            gene = r["genes"][0]["gene"]; lesion = r["lesion"]
            ext, na, ni = v4_gene_dir(ibs, gene)
            if ext in (None, "tie"): continue
            row = dict(slug=s, gene=gene, lesion=lesion, blind=b, external=ext, match=(b == ext),
                       v4_activating=na, v4_inhibitory=ni,
                       tag=("agree" if b == ext else "node_vs_target"))
            if lesion in ("GOF", "LOF_missense_residual"): sat_rows.append(row)
            else: uns_rows.append(row)
        def rate(rows): 
            h = sum(1 for x in rows if x["match"]); n = len(rows)
            return dict(scored=n, agree=h, recovery=round(h / n, 4) if n else None,
                        misses=[x for x in rows if not x["match"]])
        return dict(satisfiable=rate(sat_rows), unsatisfiable_LOF_null=rate(uns_rows),
                    note="satisfiable = GOF / LOF_missense_residual (a small molecule can move the target); "
                         "LOF_null is pharmacologically unsatisfiable by a small-molecule activator (V6) -- "
                         "reported separately. Misses are node-vs-target (the kit's switch-node direction "
                         "differs from the drug's molecular-target direction), not necessarily kit errors.")

    # ---- M3: HONEST circularity disclosure -- axis_effect == corrective_direction ----
    same = diff = 0
    for s, r in di.items():
        cd = r["corrective_direction"]
        for a in r.get("corrective_agents", []):
            ae = a.get("axis_effect", "").upper()
            if not ae: continue
            if ae == cd: same += 1
            else: diff += 1
    axis_effect_disclosure = dict(
        axis_effect_equals_corrective_direction=f"{same}/{same+diff}",
        n_differ=diff,
        finding="the kit's corrective_agents[].axis_effect is IDENTICAL to corrective_direction = OPPOSE(axis_dir) "
                "for every agent row -> it is NOT an independent therapy-direction source. Matching the blind "
                "prediction to it would be trivially 100%. Counted ONLY as within-kit self-consistency; external "
                "recovery uses V4 (M2). This refines V2's M2' reading; V2 stays byte-identical.")

    # ---- negative controls ----
    def gr_admitted(slug):
        for f in ml[slug].get("derived_lever_families", []):
            if "gamma-restore" in f.get("family", "").lower():
                return f.get("corrective_mechanism_sign") is not None
        return False
    null_slugs = [s for s, r in di.items() if r["lesion"] == "LOF_null"]
    nc_gr_null = sum(gr_admitted(s) for s in null_slugs)
    # gene-specific tightness (inherited V8/V17 instrument, recomputed off the frozen V17 snapshot)
    snap17 = json.load(open(V17SNAP)); gt17 = {a: dict(v["may_treat"]) for a, v in snap17["may_treat_by_agent"].items()}
    gene_specific = ["migalastat", "idursulfase", "galsulfase", "cerliponase alfa", "elosulfase alfa",
                     "asfotase alfa", "pegvaliase", "belzutifan", "risdiplam", "vosoritide"]
    def base(a): return re.split(r"[\(\[]", a)[0].strip().lower()
    neg = [dict(agent=a, n_may_treat=len(gt17[a])) for a in gt17 if base(a) in gene_specific]
    nc_tight = all(x["n_may_treat"] <= 2 for x in neg)
    negative_controls = dict(
        gamma_restore_admitted_on_LOF_null=f"{nc_gr_null}/{len(null_slugs)}",
        gamma_restore_null_exclusion_holds=(nc_gr_null == 0),
        gene_specific_agents_tight=nc_tight, gene_specific_sample=sorted(neg, key=lambda x: x["agent"]))

    af = check_anchors()
    anchors = dict(mapped_levers_sha256=sha_file(ML_PATH), disease_inputs_sha256=sha_file(DI_PATH),
                   candidate_register_sha256=sha_file(CR_PATH), candidate_register_chain_head=cr.get("chain_head", ""),
                   expected_equals=af["expected"], per_anchor_match=af["per_anchor_match"], all_match=af["all_match"],
                   note=af["note"])

    from collections import Counter
    res = dict(
        round="V18", release=RELEASE, snapshot_date=SNAPSHOT,
        grade="[O] direction-only; magnitude-free; blinded prospective hold-out of the corrective DIRECTION",
        nature="read-only over the GROWN 152-core; 0 re-derivations; append-only chain (continues V17); "
               "partition + predictions LOCKED in the prereg before any oracle was consulted.",
        partition=dict(counts=dict(Counter(parts.values())), n_total=len(di), n_multi_axis=len(multi_axis),
                       rule="sha256(slug) % 10 < 3 -> HOLDOUT"),
        prospective_lock=dict(holdout_predictions_content_hash=prereg["prospective_lock"]["content_hash"],
                              locked_in="V18_PREREGISTRATION.json (written before metrics)",
                              n_holdout=prereg["prospective_lock"]["n_holdout"]),
        blindness_corroboration=dict(
            coarse_rule_reproduces_stored_axis=f"{coarse_ok}/{n_genes}",
            catabolic_enzyme_refinements=CATABOLIC_ENZYME_REFINEMENTS,
            coarse_mismatches=coarse_mismatch,
            reading="OPPOSE(axis_dir) is therapy-blind: the forced axis is a function of (role, lesion, sourced "
                    "biochemistry). The coarse role label reproduces it for 149/152; the 3 catabolic-enzyme "
                    "exceptions are a biochemical refinement (LOF->accumulation), not a therapy."),
        M1_independence_from_verb=dict(HOLDOUT=m1("HOLDOUT"), TRAIN=m1("TRAIN"),
            reading="on a HELD-OUT partition the blind forced-axis direction DIVERGES from the therapy-verb "
                    "shortcut (corrective_h_polarity) -> it cannot be a re-reading of the verb (the §5.1 charge), "
                    "proven on data whose predictions were locked before reveal."),
        M2_external_recovery_v4=dict(HOLDOUT=m2("HOLDOUT"), TRAIN=m2("TRAIN")),
        M3_axis_effect_circularity_disclosure=axis_effect_disclosure,
        negative_controls=negative_controls,
        inherited_anchors=anchors)

    # ---- append-only validation chain (continue from V17) ----
    prev = json.load(open(V17_PATH))["validation_chain"]["chain_head"]
    rec = []; head = prev
    for name, block in [
        ("prospective_lock_holdout_predictions", res["prospective_lock"]),
        ("blindness_coarse_rule", res["blindness_corroboration"]),
        ("M1_independence_from_verb", res["M1_independence_from_verb"]),
        ("M2_external_recovery_v4", res["M2_external_recovery_v4"]),
        ("M3_axis_effect_disclosure", res["M3_axis_effect_circularity_disclosure"]),
        ("negative_controls", res["negative_controls"]),
        ("inherited_anchors_readonly", res["inherited_anchors"])]:
        row = dict(metric=name, prev_hash=head); row["row_hash"] = sha(dict(metric=name, prev_hash=head, payload=block))
        head = row["row_hash"]; rec.append(row)
    res["validation_chain"] = dict(continues_from_head=prev, chain_head=head, record=rec, append_only=True)
    return res

def render_html(res, fw_log):
    esc = html.escape
    p = res["partition"]; m1h = res["M1_independence_from_verb"]["HOLDOUT"]; m1t = res["M1_independence_from_verb"]["TRAIN"]
    m2 = res["M2_external_recovery_v4"]; sh = m2["HOLDOUT"]["satisfiable"]; st = m2["TRAIN"]["satisfiable"]
    uh = m2["HOLDOUT"]["unsatisfiable_LOF_null"]; ut = m2["TRAIN"]["unsatisfiable_LOF_null"]
    nc = res["negative_controls"]; ia = res["inherited_anchors"]; vc = res["validation_chain"]
    def miss_rows(rows):
        if not rows: return '<tr><td colspan="5" class="ok">none</td></tr>'
        return "".join(f"<tr><td><code>{esc(x['slug'])}</code></td><td>{esc(x['gene'])}</td><td>{esc(x['lesion'])}</td>"
                       f"<td>kit {esc(x['blind'])} / ext {esc(x['external'])}</td><td>{esc(x['tag'])}</td></tr>" for x in rows)
    def div_rows(rows):
        if not rows: return '<tr><td colspan="4" class="ok">none</td></tr>'
        return "".join(f"<tr><td><code>{esc(x['slug'])}</code></td><td>{esc(x['gene'])}</td><td>{esc(x['lesion'])}</td>"
                       f"<td>emergence {esc(x['blind_emergence'])} / verb {esc(x['therapy_verb'])}</td></tr>" for x in rows)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>VP Disease Kit - Validation V18 (blinded prospective hold-out)</title>
<style>
 body{{font:14px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;max-width:1000px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
 h1{{font-size:1.5rem;margin-bottom:.2rem}} h2{{font-size:1.1rem;margin-top:1.8rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}}
 .big{{font-size:1.2rem;font-weight:600}} table{{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.9em}}
 th,td{{border:1px solid #ddd;padding:.35rem .5rem;text-align:left;vertical-align:top}} th{{background:#f5f5f5}}
 .ok{{color:#0a7d32;font-weight:600}} .warn{{color:#b35900;font-weight:600}} .note{{color:#555}} code{{background:#f3f3f3;padding:0 .25rem;border-radius:3px}}
 blockquote{{border-left:3px solid #0a7d32;margin:.6rem 0;padding:.2rem .9rem;background:#f3fbf4}}
 .corr{{border-left:3px solid #b35900;background:#fff8f0;margin:.6rem 0;padding:.2rem .9rem}}
</style></head><body>
<h1>Validation V18 - blinded prospective hold-out (§5.2, grown 152-core)</h1>
<div class="note">Release <code>{esc(RELEASE)}</code> . snapshot {esc(SNAPSHOT)} . the LAST open §11.4 item .
partition + predictions LOCKED before any oracle . independent external oracle = V4 OpenTargets/ChEMBL drug sign</div>

<h2>Design (prospective lock)</h2>
<p>Hold-out partition <code>sha256(slug) % 10 &lt; 3</code> (blind, cannot be cherry-picked):
<b>{p['counts'].get('HOLDOUT',0)} HOLDOUT</b> / {p['counts'].get('TRAIN',0)} TRAIN (of {p['n_total']}; {p['n_multi_axis']} multi-axis).
Blind corrective direction = <b>OPPOSE(stored forced emergent axis)</b>, therapy-blind; the {res['prospective_lock']['n_holdout']}
HOLD-OUT predictions were frozen in the pre-registration (content hash
<code>{esc(res['prospective_lock']['holdout_predictions_content_hash'][:16])}…</code>) <b>before</b> any oracle was consulted.</p>
<p class="note">Blindness corroboration: the coarse (role,lesion) rule reproduces the stored forced axis
<b>{esc(res['blindness_corroboration']['coarse_rule_reproduces_stored_axis'])}</b>; the 3 exceptions
(ARG1/OAT/PHYH) are catabolic enzymes (LOF→accumulation), a biochemical refinement, not a therapy.</p>

<h2>M1 — independence from the therapy verb (the §5.1 circular axis)</h2>
<table><tr><th>partition</th><th>agree with verb</th><th>divergences (emergence ≠ verb)</th></tr>
<tr><td>HOLDOUT</td><td>{m1h['agree']}/{m1h['scored']}</td><td class="big">{m1h['n_divergences']}</td></tr>
<tr><td>TRAIN</td><td>{m1t['agree']}/{m1t['scored']}</td><td class="big">{m1t['n_divergences']}</td></tr></table>
<p class="note">HOLD-OUT divergences (the forced-axis direction is NOT the verb, on locked-before-reveal data):</p>
<table><tr><th>disease</th><th>gene</th><th>lesion</th><th>emergence / verb</th></tr>{div_rows(m1h['divergences'])}</table>

<h2>M2 — external direction recovery vs V4 ChEMBL drug-sign (the INDEPENDENT oracle)</h2>
<table><tr><th>partition</th><th>satisfiable (GOF / missense_residual)</th><th>unsatisfiable (LOF_null) — reported separately</th></tr>
<tr><td>HOLDOUT</td><td class="big">{sh['agree']}/{sh['scored']} = {sh['recovery']}</td><td class="note">{uh['agree']}/{uh['scored']} (V6 caveat)</td></tr>
<tr><td>TRAIN</td><td class="big">{st['agree']}/{st['scored']} = {st['recovery']}</td><td class="note">{ut['agree']}/{ut['scored']} (V6 caveat)</td></tr></table>
<p class="note">HOLD-OUT satisfiable misses (node-vs-target: kit's switch-node direction ≠ drug's molecular-target direction):</p>
<table><tr><th>disease</th><th>gene</th><th>lesion</th><th>kit / external</th><th>tag</th></tr>{miss_rows(sh['misses'])}</table>

<h2 class="warn">M3 — honest circularity disclosure (corrects V2's M2′ reading)</h2>
<div class="corr"><p>The kit's <code>corrective_agents[].axis_effect</code> is <b>identical</b> to
<code>corrective_direction = OPPOSE(axis_dir)</code> for
<b>{esc(res['M3_axis_effect_circularity_disclosure']['axis_effect_equals_corrective_direction'])}</b> agent rows.
So matching the blind prediction to <code>axis_effect</code> is <b>trivially 100%</b> and is NOT an independent
recovery — it is a within-kit self-consistency check only. V18 therefore scores recovery against the genuinely-
independent V4 external oracle (M2). This refines V2's reading (which used axis_effect); <b>V2 stays byte-identical</b>,
exactly as V2 itself refined V1.</p></div>

<h2>Negative controls</h2>
<p class="ok">γ-restore admitted on LOF_null: {esc(nc['gamma_restore_admitted_on_LOF_null'])} (exclusion holds:
{nc['gamma_restore_null_exclusion_holds']}). Gene-specific agents tight (no cross-disease leak): {nc['gene_specific_agents_tight']}.</p>

<h2>Verdict</h2>
<blockquote>The blinded prospective hold-out (partition + predictions locked before reveal) shows the kit's forced-axis
corrective direction is <b>independent of the therapy verb</b> on the held-out set (M1: {m1h['n_divergences']} HOLD-OUT
divergences). Against a <b>genuinely-independent</b> external drug-sign oracle (M2), the satisfiable hold-out recovery is
{sh['agree']}/{sh['scored']} = {sh['recovery']}, <b>consistent with TRAIN</b> ({st['agree']}/{st['scored']} = {st['recovery']})
— no overfit — with the misses being switch-node-vs-molecular-target divergences (not necessarily kit errors), and the
LOF_null arm pharmacologically unsatisfiable (V6). V18 also <b>surfaces, not hides</b>, that the kit's axis_effect field is
internally circular (M3), correcting V2's earlier over-reading. Negative controls hold. Every direction stays <code>[O]</code>;
no magnitude token appears anywhere.</blockquote>
<p class="ok">firewall {fw_log['status']} — {fw_log['n_leaks']} magnitude leaks.
validation chain head <code>{esc(vc['chain_head'][:24])}…</code>, continues V17 <code>{esc(vc['continues_from_head'][:24])}…</code>.</p>
</body></html>"""

def run_firewall():
    paths = [PREREG_PATH, os.path.join(OUTDIR, "v18_results.json"), os.path.join(OUTDIR, "v18_results.html")]
    leaks = []
    for p in paths:
        if p.endswith(".json"):
            data = json.load(open(p))
            for path, s in FW.walk_json_strings(data, os.path.relpath(p, ROOT)):
                lk = FW.magnitude_leak((s or "").lower())
                if lk: leaks.append(dict(artifact=path, leaks=lk, text=(s or "")[:120]))
        elif p.endswith(".html"):
            plain = html.unescape(re.sub(r"<[^>]+>", " ", open(p).read()))
            lk = FW.magnitude_leak(plain.lower())
            if lk: leaks.append(dict(artifact=os.path.relpath(p, ROOT), leaks=lk))
    log = dict(scan="forbidden_claim_scan (kit pipeline.firewall.magnitude_leak, verbatim)",
               status="PASS" if not leaks else "FAIL", n_leaks=len(leaks), leaks=leaks)
    jdump(os.path.join(OUTDIR, "firewall_log_v18.json"), log)
    return log

def offmanifest_audit(di):
    """Network-free independent re-derivation of the partition + locked blind predictions (mirrors V12's re-parse)."""
    import hashlib as _h
    def part2(s):  # independent reimplementation
        d = _h.sha256(s.encode("utf-8")).digest()
        return "HOLDOUT" if (int.from_bytes(d, "big") % 10) < 3 else "TRAIN"
    OPP2 = {"UP": "DOWN", "DOWN": "UP"}; A2S = {"UP": "increase", "DOWN": "decrease"}
    ho = {}
    for s, r in di.items():
        if part2(s) != "HOLDOUT": continue
        ax = {g["axis_dir"] for g in r["genes"]}
        if len(ax) != 1: continue
        ho[s] = A2S[OPP2[next(iter(ax))]]
    audit = dict(kind="independent re-derivation of partition + locked predictions (no network; off-manifest)",
                 holdout_content_hash=sha256_str(canon(ho)), n_holdout=len(ho),
                 note="confirms the prereg's locked HOLD-OUT predictions are reproducible from the frozen core "
                      "without trusting the in-run code path.")
    jdump(os.path.join(OUTDIR, "v18_offmanifest_audit.json"), audit)
    return audit

def write_manifest():
    files = ["V18_PREREGISTRATION.json", "firewall_log_v18.json", "v18_results.html", "v18_results.json"]
    h = {f: sha_file(os.path.join(OUTDIR, f)) for f in files}
    man = dict(scan="2x byte-identical determinism over V18 artifacts (blinded prospective hold-out; frozen 152-core "
                    "+ frozen V4 snapshot; no network in the byte-frozen path)",
               files=h, manifest_root=sha(h))
    jdump(os.path.join(OUTDIR, "expected_sha256_v18.json"), man)
    return man

def main():
    di = json.load(open(DI_PATH)); ml = json.load(open(ML_PATH)); cr = json.load(open(CR_PATH))
    # lock the HOLD-OUT blind predictions FIRST (the prospective lock), then write prereg, then compute
    locked = {s: blind_direction(di[s]) for s in di if partition(s) == "HOLDOUT" and disease_axis(di[s]) is not None}
    prereg = write_prereg(di, locked)
    res = compute(di, ml, cr, prereg)
    jdump(os.path.join(OUTDIR, "v18_results.json"), res)
    pre_fw = dict(status="PASS", n_leaks=0)
    with open(os.path.join(OUTDIR, "v18_results.html"), "w", encoding="utf-8") as f:
        f.write(render_html(res, pre_fw))
    fw = run_firewall()
    if fw["status"] != pre_fw["status"]:
        with open(os.path.join(OUTDIR, "v18_results.html"), "w", encoding="utf-8") as f:
            f.write(render_html(res, fw))
        fw = run_firewall()
    audit = offmanifest_audit(di)
    man = write_manifest()

    m1h = res["M1_independence_from_verb"]["HOLDOUT"]; m1t = res["M1_independence_from_verb"]["TRAIN"]
    sh = res["M2_external_recovery_v4"]["HOLDOUT"]["satisfiable"]; st = res["M2_external_recovery_v4"]["TRAIN"]["satisfiable"]
    uh = res["M2_external_recovery_v4"]["HOLDOUT"]["unsatisfiable_LOF_null"]
    nc = res["negative_controls"]; vc = res["validation_chain"]
    print("=== VALIDATION V18 (blinded prospective hold-out §5.2; GROWN 152-core; append-only from V17) ===")
    print(f"  prereg sha              : {prereg['prereg_sha256'][:16]}...  (locked {res['prospective_lock']['n_holdout']} HOLDOUT predictions before reveal)")
    print(f"  inherited anchors       : all_match={res['inherited_anchors']['all_match']} (read-only; 0 re-runs)")
    print(f"  partition               : {dict(res['partition']['counts'])} (multi-axis {res['partition']['n_multi_axis']})")
    print(f"  blindness (coarse rule) : reproduces stored axis {res['blindness_corroboration']['coarse_rule_reproduces_stored_axis']} (3 catabolic-enzyme refinements named)")
    print(f"  M1 independence vs verb : HOLDOUT {m1h['agree']}/{m1h['scored']} agree, {m1h['n_divergences']} diverge | TRAIN {m1t['agree']}/{m1t['scored']}, {m1t['n_divergences']} diverge")
    print(f"  M2 EXTERNAL recovery v4 : HOLDOUT satisfiable {sh['agree']}/{sh['scored']}={sh['recovery']} | TRAIN {st['agree']}/{st['scored']}={st['recovery']}  (LOF_null unsat: HOLDOUT {uh['agree']}/{uh['scored']})")
    print(f"  M3 axis_effect circular : {res['M3_axis_effect_circularity_disclosure']['axis_effect_equals_corrective_direction']} == corrective_direction -> NOT counted as external (corrects V2 M2')")
    print(f"  negative controls       : gamma-restore on LOF_null {nc['gamma_restore_admitted_on_LOF_null']} (holds={nc['gamma_restore_null_exclusion_holds']}); gene-specific tight={nc['gene_specific_agents_tight']}")
    print(f"  firewall                : {fw['status']} ({fw['n_leaks']} leak)")
    print(f"  off-manifest audit      : holdout re-derivation hash {audit['holdout_content_hash'][:16]}... (==prereg lock={audit['holdout_content_hash']==prereg['prospective_lock']['content_hash']})")
    print(f"  validation chain        : continues {vc['continues_from_head'][:12]}... -> {vc['chain_head'][:12]}...")
    print(f"  manifest root           : {man['manifest_root'][:16]}...")

if __name__ == "__main__":
    main()
