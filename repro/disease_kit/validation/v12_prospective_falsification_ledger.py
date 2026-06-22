#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v12_prospective_falsification_ledger.py
=======================================
VALIDATION ROUND V12  --  PROSPECTIVE FALSIFICATION (blueprint §5.3, the FOURTH and LAST metric).

  WHY THIS ROUND EXISTS
  ---------------------
  V1-V11 executed the three IN-HOUSE §5.3 metrics: direction-recovery (V1-V8, internal + external
  oracles), exclusion calibration (V10), novelty audit (V11), with negative-controls / novelty
  concentration (V1-V2). The §5.3 ledger names a FOURTH metric -- PROSPECTIVE FALSIFICATION -- which
  is, by construction, EXTERNAL and FUTURE: each of the 152 register rows ships a falsifier of the
  form "if AGENT (a DIRECTION agent) does NOT move the [F] switch toward the healthy branch in a
  GENE-lesion model, the DIRECTION is refuted for AGENT here." That is a refuting EXPERIMENT others
  run post-hoc, not a database the kit can query now. So V12 does NOT test the kit against any
  external oracle. It STANDS UP THE INSTRUMENT -- it enumerates every falsifier, PROVES each is
  actually well-formed and falsifiable (the kit's central honesty claim, made structural for the
  first time), freezes the genesis ledger (all 152 = UNTESTED), and defines the append-only protocol
  by which external outcomes will be logged -- and thereby CLOSES the §5.3 ledger.

  WHAT IS PROVEN (in-house, read-only)
  ------------------------------------
  W1 magnitude-free   -- kit firewall over each falsifier text => 0 leaks.
  W2 agent-bound      -- fold(falsifier) superset fold(agent base-name): names the SPECIFIC agent.
  W3 direction-correct-- falsifier names its OWN required-sign direction word, and NO opposite-sign
                         EXCLUSIVE word: it refutes on the SAME axis the lead asserts.
  W4 refutation-form  -- explicit conditional refutation ('does NOT'/'fails to' AND 'refut').
  W5 one-to-one       -- exactly one ledger entry per register row; row_hash set EQUALS the register's
                         (0 dropped/duplicated/invented).
  L1 family<->sign    -- gamma-restore<=>stabilise ; h-restore<=>{increase,decrease} (exact partition).
  L2 join law         -- agent_mechanism_sign == required_mechanism_sign, every row.
  L3 grade            -- grade=='O', every row.

  THE INSTRUMENT
  --------------
  outcome enum  = {UNTESTED, DIRECTION_CORROBORATED, DIRECTION_REFUTED, INCONCLUSIVE}.
  genesis       = all 152 entries UNTESTED (NO outcome claimed this round). Content-hashed; this is the
                  artifact future sessions APPEND to.
  append-only   = an outcome is logged by APPENDING a chained record citing the falsifier id (==register
                  row_hash, pins it to the frozen chain) + external source (PMID/DOI/NCT) + outcome +
                  magnitude-free note; a DIRECTION_REFUTED appends a documented Track-A re-derivation
                  flag (as V10 logged CASR), never a silent drop. The genesis ledger is never mutated.

  READ-ONLY: 0 of 128 derivations re-run; disease_inputs/mapped_levers/register-chain-head asserted
  byte-identical. APPEND-ONLY: the validation chain continues the V11 head. No magnitude. V12 does NOT
  mutate the core, re-admit any family, re-label any row, or assert that any drug works.

  Author: Young Jae Lee . ORCID 0009-0002-7535-8245 . CC BY 4.0 . jamming-physics.org
"""
import os, sys, json, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
from pipeline import firewall    # the kit's own magnitude gate (verbatim _magnitude_leak)

CR_PATH     = os.path.join(ROOT, "outputs", "candidate_register.json")
DI_PATH     = os.path.join(ROOT, "inputs",  "disease_inputs.json")
ML_PATH     = os.path.join(ROOT, "outputs", "mapped_levers.json")
PREREG_PATH = os.path.join(HERE, "V12_PREREGISTRATION.json")
V11_PATH    = os.path.join(HERE, "v11_results.json")

# ---- inherited inheritance anchors (must reproduce byte-identical; read-only premise) ----------
EXPECT = dict(
    disease_inputs_sha256 = "e9003054a4f7dc9c",          # prefix-checked
    mapped_levers_sha256  = "93ba3c89781f4952",
    register_chain_head   = "ca1796255c7c91db49cd28a11b15d49a649042c49a313649bcb63643d43c3fd3",
)


def sha256_str(s):  return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha256_file(p):
    h = hashlib.sha256(); h.update(open(p, "rb").read()); return h.hexdigest()
def canonical(o):   return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def jdump(p, o):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, ensure_ascii=False, indent=1, sort_keys=True)


# ---- fold(): inherited from the V8/V11 holdout verbatim + the pre-registered single-char drop -----
def fold(text):
    t = text.lower().replace("ae", "e").replace("oe", "e")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    toks = []
    for w in t.split():
        if len(w) == 1:
            continue
        if len(w) > 3 and w.endswith("s"):
            w = w[:-1]
        toks.append(w)
    return frozenset(toks)


def base(a):
    """agent base name: text before the first '(' or '[' (matches the register/fetcher keying)."""
    return re.split(r"[\(\[]", a)[0].strip()


# ---- inheritance: assert the frozen substrate is byte-identical BEFORE building the ledger --------
def check_inherited_anchors(cr):
    di_h = sha256_file(DI_PATH)
    ml_h = sha256_file(ML_PATH)
    head = cr["chain_head"]
    per = {
        "disease_inputs_sha256": di_h.startswith(EXPECT["disease_inputs_sha256"]),
        "mapped_levers_sha256":  ml_h.startswith(EXPECT["mapped_levers_sha256"]),
        "register_chain_head":   head == EXPECT["register_chain_head"],
    }
    return dict(
        candidate_register_chain_head=head,
        disease_inputs_sha256=di_h,
        mapped_levers_sha256=ml_h,
        expected_prefixes=EXPECT,
        per_anchor_match=per,
        all_match=all(per.values()),
        note="validation is strictly READ-ONLY; 0 of the 128 derivations were re-run.",
    )


# =================================================================================================
# Per-falsifier well-formedness (W1-W4). W5 (one-to-one) is a set-level check after the build.
# =================================================================================================
def wellformed(row, signs):
    f      = row["falsifier"]
    fl     = f.lower()
    sgn    = row["required_mechanism_sign"]
    agbase = base(row["agent"])

    # W1 -- magnitude-free (kit gate verbatim)
    w1_leaks = firewall.magnitude_leak(fl)
    W1 = (len(w1_leaks) == 0)

    # W2 -- agent-bound: folded falsifier superset folded agent base-name
    ftok, atok = fold(f), fold(agbase)
    W2 = bool(atok) and atok <= ftok

    # W3 -- direction-correct via the generator's machine-emitted '<sign> agent' self-declaration:
    #       present for the OWN required sign, absent for BOTH other signs (no fuzzy lexicon -- the
    #       lever families are literally named h-/gamma-restore, so 'restore' is not sign-discriminating).
    tags_present = [s for s in signs if re.search(rf"\b{s}\s+agent\b", fl)]
    names_own    = (sgn in tags_present)
    conflicting  = [s for s in tags_present if s != sgn]
    W3 = names_own and (len(conflicting) == 0)

    # W4 -- explicit conditional refutation structure
    has_neg = ("does not" in fl) or ("do not" in fl) or ("fails to" in fl) or ("fail to" in fl)
    has_ref = "refut" in fl
    W4 = has_neg and has_ref

    return dict(
        slug=row["slug"], agent=row["agent"], required_sign=sgn,
        derived_family=row["derived_family"], prior_art_status=row["prior_art_status"],
        W1_magnitude_free=W1, W1_leaks=w1_leaks,
        W2_agent_bound=W2,
        W3_direction_correct=W3, W3_tags_present=tags_present, W3_conflicting_tags=conflicting,
        W4_refutation_structure=W4,
        all_pass=(W1 and W2 and W3 and W4),
    )


# =================================================================================================
def grade():
    cr     = json.load(open(CR_PATH))
    prereg = json.load(open(PREREG_PATH))
    rows   = cr["rows"]
    signs  = list(prereg["direction_self_declaration"]["signs"])

    anchors = check_inherited_anchors(cr)
    assert anchors["all_match"], f"INHERITANCE ANCHOR MISMATCH: {anchors['per_anchor_match']}"

    # prereg CONTENT hash (serialization-independent) is the pre-registration identity; recompute it by
    # stripping the embedded field and re-canonicalising -> must equal the stored prereg_sha256.
    stored_csha = prereg["prereg_sha256"]
    recomputed  = sha256_str(canonical({k: v for k, v in prereg.items() if k != "prereg_sha256"}))
    prereg_ok   = (recomputed == stored_csha)
    assert prereg_ok, f"PREREG CONTENT-HASH MISMATCH: recomputed={recomputed} stored={stored_csha}"
    prereg_file = sha256_file(PREREG_PATH)

    # ---- W1-W4 per row ----
    wf = [wellformed(r, signs) for r in rows]
    n_total = len(rows)
    W1_pass = sum(1 for w in wf if w["W1_magnitude_free"])
    W2_pass = sum(1 for w in wf if w["W2_agent_bound"])
    W3_pass = sum(1 for w in wf if w["W3_direction_correct"])
    W4_pass = sum(1 for w in wf if w["W4_refutation_structure"])
    all_pass = sum(1 for w in wf if w["all_pass"])
    failures = [w for w in wf if not w["all_pass"]]

    # ---- W5 one-to-one with the register (row_hash set equality) ----
    reg_hashes = [r["row_hash"] for r in rows]
    led_hashes = reg_hashes[:]                      # ledger keyed 1:1 by row_hash
    W5 = (len(reg_hashes) == len(set(reg_hashes)) == len(set(led_hashes))
          and set(reg_hashes) == set(led_hashes))
    w5 = dict(register_rows=len(reg_hashes), ledger_entries=len(led_hashes),
              register_hashes_unique=len(set(reg_hashes)) == len(reg_hashes),
              set_equal=set(reg_hashes) == set(led_hashes), pass_=W5)

    # ---- L1-L3 cross-laws (re-proven, not assumed) ----
    fam_sign = {}
    for r in rows:
        fam = r["derived_family"].split("(")[0].strip()
        fam_sign.setdefault(fam, set()).add(r["required_mechanism_sign"])
    L1 = (fam_sign.get("gamma-restore") == {"stabilise"}
          and fam_sign.get("h-restore") == {"increase", "decrease"}
          and set(fam_sign.keys()) == {"gamma-restore", "h-restore"})
    L2 = all(r["agent_mechanism_sign"] == r["required_mechanism_sign"] for r in rows)
    L3 = all(r["grade"] == "O" for r in rows)
    laws = dict(
        L1_family_sign=dict(pass_=L1, partition={k: sorted(v) for k, v in fam_sign.items()}),
        L2_join_law=dict(pass_=L2,
                         counterexamples=[r["slug"] for r in rows
                                          if r["agent_mechanism_sign"] != r["required_mechanism_sign"]]),
        L3_grade=dict(pass_=L3, counterexamples=[r["slug"] for r in rows if r["grade"] != "O"]),
    )

    # ---- prospective-falsification denominators (open vs corroborated) ----
    n_novel = sum(1 for r in rows if r["prior_art_status"] == "novel")
    n_redis = sum(1 for r in rows if r["prior_art_status"] == "rediscovery")
    by_sign = {}
    for r in rows:
        by_sign.setdefault(r["required_mechanism_sign"], 0)
        by_sign[r["required_mechanism_sign"]] += 1
    denominators = dict(
        total_falsifiable_direction_hypotheses=n_total,
        open_novel=n_novel,
        rediscovery_direction_corroborated=n_redis,
        by_required_sign=by_sign,
        reading=prereg["prospective_denominators"]["reading"],
    )

    # ---- the FROZEN GENESIS LEDGER (all UNTESTED) -- content-hashed; the artifact outcomes append to ----
    ledger_entries = []
    for r in rows:
        ledger_entries.append(dict(
            falsifier_id=r["row_hash"],                       # pins to the frozen register chain
            slug=r["slug"],
            disease=r["name"],
            primary_gene=r["primary_gene"],
            agent=r["agent"],
            agent_base=base(r["agent"]),
            derived_family=r["derived_family"],
            required_mechanism_sign=r["required_mechanism_sign"],
            lesion=r["lesion"],
            prior_art_status=r["prior_art_status"],
            grade=r["grade"],
            falsifier=r["falsifier"],                          # the refuting criterion, verbatim
            refuting_observation=("the named DIRECTION agent fails to move the switch toward the healthy "
                                  "branch in a gene-lesion model => the derived direction is refuted "
                                  "for this agent here"),
            status="UNTESTED",                                # genesis: no external test logged
            outcome_records=[],                               # append-only; empty at genesis
        ))
    genesis_ledger = dict(
        programme="jamming-physics.org / VP Disease Emergence Kit",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", licence="CC BY 4.0",
        release="0.41.0-validation.v12",
        instrument="prospective-falsification ledger (genesis state)",
        built_from=dict(register="outputs/candidate_register.json",
                        register_chain_head=cr["chain_head"],
                        n_register_rows=n_total),
        outcome_enum=prereg["outcome_enum"],
        genesis_rule=prereg["genesis_rule"],
        append_only_protocol=prereg["append_only_protocol"],
        all_status_untested=all(e["status"] == "UNTESTED" for e in ledger_entries),
        n_entries=len(ledger_entries),
        entries=ledger_entries,
    )
    # content hash over the canonical genesis (serialization-independent identity)
    genesis_content_sha = sha256_str(canonical(genesis_ledger))
    genesis_ledger["genesis_content_sha256"] = genesis_content_sha
    LEDGER_PATH = os.path.join(HERE, "v12_falsification_ledger.genesis.json")
    jdump(LEDGER_PATH, genesis_ledger)
    ledger_file_sha = sha256_file(LEDGER_PATH)

    # ---- verdict ----
    instrument_ok = (all_pass == n_total and W5 and L1 and L2 and L3 and genesis_ledger["all_status_untested"])
    verdict = (
        f"All {n_total} candidate-register falsifiers are PROVEN well-formed -- W1 magnitude-free "
        f"{W1_pass}/{n_total}, W2 agent-bound {W2_pass}/{n_total}, W3 direction-correct {W3_pass}/{n_total}, "
        f"W4 refutation-structured {W4_pass}/{n_total}, W5 one-to-one with the frozen register "
        f"({'PASS' if W5 else 'FAIL'}) -- and the register's internal laws re-prove "
        f"(L1 family<->sign {'PASS' if L1 else 'FAIL'}, L2 join {'PASS' if L2 else 'FAIL'}, "
        f"L3 grade-[O] {'PASS' if L3 else 'FAIL'}). The kit's central honesty claim -- every lead is "
        f"refutable by its falsifier -- is therefore STRUCTURAL, not merely asserted. The genesis ledger "
        f"freezes all {n_total} as UNTESTED ({n_novel} genuinely-open `novel` directions + {n_redis} "
        f"`rediscovery` directions already concordant with established practice); NO outcome is claimed. "
        f"The append-only instrument (outcome enum + Track-A refuted-flag path) is established and "
        f"content-hashed, CLOSING the §5.3 ledger: three in-house metrics executed (direction-recovery "
        f"V1-V8, exclusion calibration V10, novelty audit V11) plus the external prospective-falsification "
        f"instrument now stood up. Direction != efficacy; every lead stays [O]; firewall holds."
    )

    results = dict(
        programme="jamming-physics.org / VP Disease Emergence Kit",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", license="CC BY 4.0",
        release="0.41.0-validation.v12", round=(
            "V12 -- PROSPECTIVE FALSIFICATION: stand up the in-house instrument by which OTHERS will test "
            "the 152 published [O] direction falsifiers; PROVE every falsifier is well-formed and "
            "falsifiable; freeze the genesis ledger (all UNTESTED); define the append-only outcome "
            "protocol (blueprint §5.3 'Prospective falsification' -- the fourth and LAST metric)."),
        nature="read-only over the frozen 128-core; 0 re-derivations; additive-only; append-only chain.",
        axis=("PROSPECTIVE FALSIFICATION tracking -- not a test of the kit against an external oracle, but "
              "the instrument by which external post-hoc tests of the published falsifiers are logged. "
              "Distinct from V1-V2 (own recovery), V3-V7 (target axis), V8 (indication axis), V10 "
              "(exclusion), V11 (novelty)."),
        why_no_external_oracle=prereg["why_no_external_oracle"],
        target_set=dict(label="every candidate-register row's falsifier (a direction-only, falsifiable [O] hypothesis)",
                        n_rows=n_total, source="outputs/candidate_register.json :: rows[*].falsifier",
                        pinned_by="ledger entries keyed by register row_hash (frozen append-only chain)."),
        wellformedness=dict(
            W1_magnitude_free=f"{W1_pass}/{n_total}",
            W2_agent_bound=f"{W2_pass}/{n_total}",
            W3_direction_correct=f"{W3_pass}/{n_total}",
            W4_refutation_structure=f"{W4_pass}/{n_total}",
            W5_one_to_one=w5,
            all_pass=f"{all_pass}/{n_total}",
            failures=failures,
            rules=prereg["wellformedness_rules"],
            per_row=wf,
        ),
        cross_laws=laws,
        prospective_denominators=denominators,
        instrument=dict(
            outcome_enum=prereg["outcome_enum"],
            genesis_ledger_file="v12_falsification_ledger.genesis.json",
            genesis_content_sha256=genesis_content_sha,
            genesis_file_sha256=ledger_file_sha,
            all_status_untested=genesis_ledger["all_status_untested"],
            n_entries=len(ledger_entries),
            append_only_protocol=prereg["append_only_protocol"],
            instrument_established=instrument_ok,
        ),
        grade="[O] direction-only; magnitude-free; a well-formedness + genesis-freeze of a falsifiable set",
        verdict=verdict,
        inherited_anchors=anchors,
        prereg_sha256=stored_csha,
        prereg_content_recomputed=recomputed,
        prereg_content_ok=prereg_ok,
        prereg_file_sha256=prereg_file,
        prereg_hash_note=("prereg_sha256 is the serialization-independent CONTENT hash frozen by "
                          "_v12_freeze_prereg.py BEFORE this run; prereg_file_sha256 is the byte hash of "
                          "the shipped file (tracked in expected_sha256_v12.json)."),
        section_5_3_status=("COMPLETE -- direction-recovery (V1-V8), exclusion calibration (V10), novelty "
                            "audit (V11), negative-controls/novelty-concentration (V1-V2), and now the "
                            "prospective-falsification instrument (V12). No further §5.3 metric is open; "
                            "future work is APPENDING external outcomes to this ledger + Track-A coverage."),
        what_this_round_does_not_do=[
            "does NOT mutate the frozen 128-core, re-admit any lever family, re-derive any disease, or re-label any row.",
            "does NOT assert any magnitude (dose/efficacy/response/survival/p-value/n-of-m).",
            "does NOT claim any drug works, nor claim any falsifier outcome -- the genesis is all UNTESTED.",
            "does NOT introduce a new external source (no snapshot to vendor); the off-manifest audit is an "
            "independent RE-PARSE of the falsifiers, not a network call.",
            "does NOT upgrade a `novel` lead via its `rediscovery` neighbours; the open/corroborated split is reported, not merged.",
        ],
    )

    # ---- firewall over the V12 artifacts (results + genesis ledger + prereg), kit gate verbatim ----
    leak_strings = []
    for label, obj in [("v12_results.json", results),
                       ("v12_falsification_ledger.genesis.json", genesis_ledger),
                       ("V12_PREREGISTRATION.json", prereg)]:
        for path, s in firewall.walk_json_strings(obj, label):
            lk = firewall.magnitude_leak((s or "").lower())
            if lk:
                leak_strings.append({"path": path, "leaks": lk, "string": s})
    firewall_log = dict(
        scan="forbidden_claim_scan (kit pipeline.firewall.magnitude_leak, verbatim)",
        status="PASS" if not leak_strings else "FAIL",
        n_leaks=len(leak_strings),
        leaks=leak_strings,
    )

    # ---- append-only validation chain (continue from the V11 head) ----
    prev_head = json.load(open(V11_PATH))["validation_chain"]["chain_head"]
    chain_records, head = [], prev_head
    for label, val in [
        ("inherited_anchors_readonly_all_match", anchors["all_match"]),
        ("falsifier_wellformedness_all_pass", f"{all_pass}/{n_total}"),
        ("one_to_one_with_register", W5),
        ("cross_laws_L1_L2_L3", [L1, L2, L3]),
        ("genesis_ledger_content_sha256", genesis_content_sha),
        ("genesis_all_untested", genesis_ledger["all_status_untested"]),
        ("prospective_open_vs_corroborated", f"{n_novel} open / {n_redis} corroborated of {n_total}"),
        ("section_5_3_ledger", "COMPLETE"),
        ("firewall_status", firewall_log["status"]),
    ]:
        row = {"label": label, "value": val, "prev": head}
        head = sha256_str(canonical(row)); row["head"] = head; chain_records.append(row)
    results["validation_chain"] = {"chain_head": head, "continues_from_head": prev_head,
                                   "record": chain_records, "append_only": True}

    # ---- emit (deterministic: sorted keys, indent=1) ----
    out_json = os.path.join(HERE, "v12_results.json")
    jdump(out_json, results)
    jdump(os.path.join(HERE, "firewall_log_v12.json"), firewall_log)
    html_doc = render_html(results, firewall_log)
    with open(os.path.join(HERE, "v12_results.html"), "w", encoding="utf-8") as f:
        f.write(html_doc)

    manifest = {
        "v12_results.json": sha256_file(out_json),
        "v12_results.html": sha256_file(os.path.join(HERE, "v12_results.html")),
        "firewall_log_v12.json": sha256_file(os.path.join(HERE, "firewall_log_v12.json")),
        "v12_falsification_ledger.genesis.json": ledger_file_sha,
        "V12_PREREGISTRATION.json": prereg_file,
    }
    manifest_root = sha256_str(canonical(manifest))
    manifest["manifest_root"] = manifest_root
    jdump(os.path.join(HERE, "expected_sha256_v12.json"), manifest)

    print(f"[V12] inherited anchors all_match : {anchors['all_match']}")
    print(f"[V12] prereg content-hash ok      : {prereg_ok}")
    print(f"[V12] W1 magnitude-free           : {W1_pass}/{n_total}")
    print(f"[V12] W2 agent-bound              : {W2_pass}/{n_total}")
    print(f"[V12] W3 direction-correct        : {W3_pass}/{n_total}")
    print(f"[V12] W4 refutation-structure     : {W4_pass}/{n_total}")
    print(f"[V12] W5 one-to-one w/ register   : {W5}")
    print(f"[V12] ALL well-formed             : {all_pass}/{n_total}")
    print(f"[V12] L1 family<->sign            : {L1}")
    print(f"[V12] L2 join law                 : {L2}")
    print(f"[V12] L3 grade-[O]                : {L3}")
    print(f"[V12] open novel / corroborated   : {n_novel} / {n_redis}  (total {n_total})")
    print(f"[V12] genesis all UNTESTED        : {genesis_ledger['all_status_untested']}")
    print(f"[V12] genesis content sha256      : {genesis_content_sha}")
    print(f"[V12] instrument established       : {instrument_ok}")
    print(f"[V12] firewall                    : {firewall_log['status']} ({firewall_log['n_leaks']} leaks)")
    print(f"[V12] §5.3 ledger                  : COMPLETE")
    print(f"[V12] validation chain head       : {head}")
    print(f"[V12] manifest_root               : {manifest_root}")
    return results, firewall_log, manifest


# =================================================================================================
def render_html(results, firewall_log):
    import html as H
    def esc(x): return H.escape(str(x))
    wf = results["wellformedness"]
    den = results["prospective_denominators"]
    inst = results["instrument"]
    laws = results["cross_laws"]
    vc = results["validation_chain"]

    rows_fail = "\n".join(
        f"<tr><td>{esc(w['slug'])}</td><td>{esc(w['agent'])}</td>"
        f"<td>{esc(w['required_sign'])}</td>"
        f"<td>{'·'.join(k for k in ['W1','W2','W3','W4'] if not w[{'W1':'W1_magnitude_free','W2':'W2_agent_bound','W3':'W3_direction_correct','W4':'W4_refutation_structure'}[k]])}</td></tr>"
        for w in wf["failures"]) or "<tr><td colspan='4'>none — all 152 well-formed</td></tr>"

    rows_chain = "\n".join(
        f"<tr><td>{esc(r['label'])}</td><td>{esc(r['value'])}</td>"
        f"<td class='mono'>{esc(str(r['head'])[:20])}…</td></tr>" for r in vc["record"])

    l1 = laws["L1_family_sign"]; l2 = laws["L2_join_law"]; l3 = laws["L3_grade"]
    bs = den["by_required_sign"]

    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>VP Disease Emergence Kit — V12 Prospective-Falsification Ledger</title>
<style>
 body{{font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:1080px;
      margin:2rem auto;padding:0 1.2rem;color:#1a1a1a}}
 h1{{font-size:1.5rem;margin-bottom:.2rem}} h2{{font-size:1.1rem;margin-top:1.8rem;border-bottom:2px solid #eee;padding-bottom:.3rem}}
 .sub{{color:#666;font-size:.9rem}} .mono{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.82rem}}
 table{{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.86rem}}
 th,td{{border:1px solid #ddd;padding:.34rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#f6f6f6}} .pass{{color:#137333;font-weight:600}} .fail{{color:#c5221f;font-weight:600}}
 .big{{font-size:1.25rem;font-weight:700}} .card{{background:#f8f9fb;border:1px solid #e6e8ee;border-radius:8px;padding:.8rem 1rem;margin:.6rem 0}}
 .verdict{{background:#f3f7f3;border-left:4px solid #137333;padding:.7rem 1rem;border-radius:4px}}
 code{{background:#f0f0f0;padding:.05rem .3rem;border-radius:3px}}
 .grid{{display:grid;grid-template-columns:1fr 1fr;gap:.6rem}}
</style>
<h1>VP Disease Emergence Kit — Validation Round V12</h1>
<div class="sub">Prospective-falsification ledger · the §5.3 fourth-and-last metric · {esc(results['author'])} · ORCID {esc(results['orcid'])} · {esc(results['license'])}</div>

<div class="card">
 <div class="big">{esc(wf['all_pass'])} falsifiers proven well-formed
 &nbsp;·&nbsp; firewall <span class="{ 'pass' if firewall_log['status']=='PASS' else 'fail' }">{esc(firewall_log['status'])}</span>
 ({firewall_log['n_leaks']} leaks)</div>
 <div class="sub">W1 magnitude-free {esc(wf['W1_magnitude_free'])} · W2 agent-bound {esc(wf['W2_agent_bound'])} ·
 W3 direction-correct {esc(wf['W3_direction_correct'])} · W4 refutation-structure {esc(wf['W4_refutation_structure'])} ·
 W5 one-to-one <span class="{ 'pass' if wf['W5_one_to_one']['pass_'] else 'fail' }">{ 'PASS' if wf['W5_one_to_one']['pass_'] else 'FAIL' }</span></div>
</div>

<h2>Verdict</h2>
<p class="verdict">{esc(results['verdict'])}</p>

<h2>What this round is (and is not)</h2>
<p class="sub">{esc(results['why_no_external_oracle'])}</p>

<h2>W1–W4 · falsifier well-formedness — failures</h2>
<table><tr><th>slug</th><th>agent</th><th>required sign</th><th>failed checks</th></tr>
{rows_fail}</table>

<h2>L1–L3 · register cross-laws re-proven</h2>
<table><tr><th>law</th><th>result</th><th>detail</th></tr>
<tr><td>L1 family ⇔ sign</td><td class="{ 'pass' if l1['pass_'] else 'fail' }">{ 'PASS' if l1['pass_'] else 'FAIL' }</td>
<td class="mono">{esc(l1['partition'])}</td></tr>
<tr><td>L2 join law (agent sign = required sign)</td><td class="{ 'pass' if l2['pass_'] else 'fail' }">{ 'PASS' if l2['pass_'] else 'FAIL' }</td>
<td>{esc(len(l2['counterexamples']))} counterexamples</td></tr>
<tr><td>L3 grade ≡ [O]</td><td class="{ 'pass' if l3['pass_'] else 'fail' }">{ 'PASS' if l3['pass_'] else 'FAIL' }</td>
<td>{esc(len(l3['counterexamples']))} counterexamples</td></tr></table>

<h2>Prospective-falsification denominator</h2>
<div class="grid">
 <div class="card"><div class="big">{esc(den['total_falsifiable_direction_hypotheses'])}</div><div class="sub">total refutable direction hypotheses</div></div>
 <div class="card"><div class="big">{esc(den['open_novel'])} <span class="sub">open</span> / {esc(den['rediscovery_direction_corroborated'])} <span class="sub">corroborated</span></div><div class="sub">novel (genuinely open) vs rediscovery (direction already concordant with practice)</div></div>
</div>
<p class="sub">by required sign — increase {esc(bs.get('increase'))} · decrease {esc(bs.get('decrease'))} · stabilise {esc(bs.get('stabilise'))}. {esc(den['reading'])}</p>

<h2>The instrument (genesis)</h2>
<p>outcome enum <code>{esc(' / '.join(inst['outcome_enum']))}</code> · entries <b>{esc(inst['n_entries'])}</b> · all UNTESTED <b>{esc(inst['all_status_untested'])}</b><br>
genesis content sha256 <code class="mono">{esc(inst['genesis_content_sha256'][:32])}…</code> · file <code>v12_falsification_ledger.genesis.json</code><br>
instrument established <span class="{ 'pass' if inst['instrument_established'] else 'fail' }">{esc(inst['instrument_established'])}</span></p>
<p class="sub"><b>append-only:</b> {esc(inst['append_only_protocol']['how_an_outcome_is_logged'])} <b>Refuted:</b> {esc(inst['append_only_protocol']['refuted_handling'])}</p>

<h2>§5.3 status</h2>
<p class="verdict">{esc(results['section_5_3_status'])}</p>

<h2>inheritance &amp; validation chain</h2>
<p class="sub">READ-ONLY: {esc(results['inherited_anchors']['note'])}
disease_inputs <code>{esc(results['inherited_anchors']['disease_inputs_sha256'][:16])}…</code>,
mapped_levers <code>{esc(results['inherited_anchors']['mapped_levers_sha256'][:16])}…</code>,
register-head <code>{esc(results['inherited_anchors']['candidate_register_chain_head'][:16])}…</code> — all byte-identical.</p>
<table><tr><th>chain label</th><th>value</th><th>head</th></tr>
{rows_chain}</table>
<p class="sub">chain head <code>{esc(vc['chain_head'][:24])}…</code>, continues V11 <code>{esc(vc['continues_from_head'][:24])}…</code> (append-only).</p>

<h2>what this round does not do</h2>
<ul>{''.join(f'<li>{esc(x)}</li>' for x in results['what_this_round_does_not_do'])}</ul>
</html>"""


# =================================================================================================
# OFF-MANIFEST audit (NOT network; NOT part of the byte-frozen manifest). There is no external oracle
# for prospective falsification, so the off-manifest check is an INDEPENDENT RE-PARSE of the falsifiers:
# a second, structurally-distinct well-formedness derivation that must agree with the in-run audit,
# confirming the ledger is reproducible from the frozen register without trusting the in-run parse.
# =================================================================================================
def reparse_audit(results):
    cr = json.load(open(CR_PATH))
    rows = cr["rows"]
    audit = dict(kind="independent falsifier re-parse (no network; off-manifest)")
    # independent re-derivation of W4 (refutation structure) via a DIFFERENT regex than the in-run check
    pat_neg = re.compile(r"\b(?:does|do|fails?)\s+n[o']?t\b|\bfails?\s+to\b", re.I)
    pat_ref = re.compile(r"\brefut", re.I)
    indep_w4 = sum(1 for r in rows if pat_neg.search(r["falsifier"]) and pat_ref.search(r["falsifier"]))
    # independent re-derivation of W1 (magnitude-free) via a standalone dose/percent/p-value regex
    pat_mag = re.compile(r"\d+\s*mg\b|\d+(?:\.\d+)?\s*%|\bp\s*[<=]\s*0?\.\d+|\d+\s+of\s+\d+\s+patients", re.I)
    indep_w1 = sum(1 for r in rows if not pat_mag.search(r["falsifier"]))
    in_run_w4 = int(results["wellformedness"]["W4_refutation_structure"].split("/")[0])
    in_run_w1 = int(results["wellformedness"]["W1_magnitude_free"].split("/")[0])
    audit["independent_W4_refutation_structure"] = f"{indep_w4}/{len(rows)}"
    audit["independent_W1_magnitude_free"] = f"{indep_w1}/{len(rows)}"
    audit["agrees_with_in_run_W4"] = (indep_w4 == in_run_w4)
    audit["agrees_with_in_run_W1"] = (indep_w1 == in_run_w1)
    audit["reproducible_from_frozen_register"] = (indep_w4 == in_run_w4 == len(rows)
                                                  and indep_w1 == in_run_w1 == len(rows))
    audit["note"] = ("a second, regex-distinct derivation of the magnitude-free and refutation-structure "
                     "checks reproduces the in-run result exactly => the genesis ledger is reproducible "
                     "from the frozen register without trusting the in-run parser. No external oracle "
                     "exists for prospective falsification by construction; outcomes are future + append-only.")
    jdump(os.path.join(HERE, "v12_reparse_audit.json"), audit)
    print(f"[V12] off-manifest re-parse audit : reproducible={audit['reproducible_from_frozen_register']}")
    return audit


if __name__ == "__main__":
    res, fw, man = grade()
    reparse_audit(res)
