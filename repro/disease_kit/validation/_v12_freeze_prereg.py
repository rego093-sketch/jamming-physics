#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v12_freeze_prereg.py
=====================
Freeze V12_PREREGISTRATION.json BEFORE the prospective-falsification ledger is built, and stamp it
with a serialization-independent CONTENT hash (prereg_sha256), exactly as V11's fetcher froze its
prereg content hash before metrics. There is NO external snapshot this round (prospective
falsification is inherently external -- the "oracle" is future external testing, UNAVAILABLE at
freeze by definition), so this freezer only constructs and content-hashes the prereg; the genesis
ledger itself is built read-only from the already-frozen 152-row register by the holdout.

  Author: Young Jae Lee . ORCID 0009-0002-7535-8245 . CC BY 4.0 . jamming-physics.org
"""
import os, json, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
OUT    = os.path.join(HERE, "V12_PREREGISTRATION.json")


def canonical(o): return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def sha256_str(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()


prereg = {
    "programme": "jamming-physics.org / VP Disease Emergence Kit",
    "author": "Young Jae Lee",
    "orcid": "0009-0002-7535-8245",
    "licence": "CC BY 4.0",
    "release": "0.41.0-validation.v12",
    "round": "V12",
    "snapshot_date": "2026-06-21",
    "section": ("00_CONTINUATION_BLUEPRINT.md \u00a75.3 'Prospective falsification' -- the FOURTH and LAST "
                "validation metric: track which falsifiers were tested by others and the outcome "
                "(append-only log). The in-house four-metric ledger (direction-recovery V1-V8, exclusion "
                "calibration V10, novelty audit V11, negative-controls/novelty-concentration V1-V2) is "
                "already COMPLETE; prospective falsification is the only remaining item and is inherently "
                "EXTERNAL."),
    "axis": ("PROSPECTIVE FALSIFICATION tracking -- categorically distinct from every prior round. V1-V2 "
             "tested the kit's OWN direction recovery; V3-V7 tested the drug<->TARGET axis; V8 tested the "
             "approved-INDICATION axis; V10 tested the gamma-restore EXCLUSION (silence); V11 tested "
             "NOVELTY against an investigation registry. V12 does not test the kit against any external "
             "oracle at all -- it STANDS UP the instrument by which OTHERS will, over time, test the "
             "152 published [O] direction falsifiers, and freezes the genesis state. No outcome is "
             "claimed this round."),
    "why_no_external_oracle": ("prospective falsification is, by construction, future and external: each "
                               "of the 152 register rows ships a falsifier of the form 'if AGENT (a "
                               "DIRECTION agent) does NOT move the switch toward the healthy branch in a "
                               "GENE-lesion model, the DIRECTION is refuted for AGENT here' -- a refuting "
                               "EXPERIMENT others run post-hoc, not a database the kit can query now. So "
                               "the genesis ledger asserts every row UNTESTED; outcomes append later "
                               "(append-only), each citing the falsifier id + the external source. There "
                               "is therefore NO snapshot to vendor and NO external refetch -- the only "
                               "off-manifest audit is an INDEPENDENT RE-PARSE of the falsifiers (a "
                               "well-formedness re-derivation), confirming the ledger is reproducible "
                               "from the frozen register without trusting the in-run parse."),
    "target_set": {
        "label": "every candidate-register row's falsifier (a direction-only, falsifiable [O] hypothesis)",
        "n_rows": 152,
        "source": "outputs/candidate_register.json :: rows[*].falsifier",
        "pinned_by": "each ledger entry is keyed by the register row_hash, pinning it to the frozen "
                     "append-only register chain (head ca1796255c7c91db49cd28a11b15d49a649042c49a313649bcb63643d43c3fd3).",
    },
    # ---- the structural audit that EARNS 'every lead is refutable by its falsifier' -----------------
    "wellformedness_rules": {
        "W1_magnitude_free": "kit firewall magnitude_leak() over the falsifier text => 0 leaks (the "
                             "refutation criterion carries NO dose/efficacy/response/survival/p-value/"
                             "n-of-m token). Run with the kit's own _magnitude_leak verbatim.",
        "W2_agent_bound": "fold(falsifier) is a SUPERSET of fold(agent base-name) -- the falsifier names "
                          "the SPECIFIC agent, never a generic family stand-in. fold() inherited verbatim "
                          "from the V8/V11 holdout (lowercase; ae->e, oe->e; non-alnum->space; "
                          "singularize trailing-s if len>3; single-char-token drop).",
        "W3_direction_correct": "the falsifier carries the register generator's machine-emitted "
                                "self-declaration tag '<sign> agent' (e.g. 'a pathway decrease agent', 'a "
                                "broad stabilise agent', 'a gene-specific supply/increase agent') for its "
                                "OWN required_mechanism_sign, and carries NO conflicting '<other-sign> "
                                "agent' tag -- so the falsifier unambiguously states which direction it "
                                "would refute, and it is the RIGHT one (a falsifier declaring the wrong or "
                                "two signs is the defect class this catches).",
        "W3_rationale": "a fuzzy directional-verb lexicon was REJECTED as the W3 instrument: the lever "
                        "families are literally named `h-restore` / `gamma-restore`, so the token 'restore' "
                        "appears in every row's '...direction is refuted' clause AND legitimately belongs to "
                        "BOTH increase (h-restore=supply) and stabilise (restore thermostability) -- it is "
                        "not sign-discriminating. The deterministic '<sign> agent' tag the generator emits "
                        "is the unambiguous, non-tunable direction declaration; W3 tests THAT.",
        "W4_refutation_structure": "the falsifier is an explicit conditional refutation: it contains a "
                                   "negation of the predicted effect ('does NOT' / 'fails to') AND the word "
                                   "'refut' -- i.e. an 'if predicted-effect-absent => direction refuted' "
                                   "clause, not a bare assertion.",
        "W5_one_to_one": "exactly one ledger entry per register row; the ledger's row_hash set EQUALS the "
                         "register's row_hash set (0 dropped, 0 duplicated, 0 invented). No silent drop.",
    },
    "direction_self_declaration": {
        "tag_template": "<required_mechanism_sign> agent",
        "signs": ["increase", "decrease", "stabilise"],
        "match": "case-insensitive regex \\b<sign>\\s+agent\\b ; the 'supply/increase agent' compound is an "
                 "increase tag (\\bincrease\\b matches after the '/').",
        "pass_rule": "the falsifier matches the tag for its OWN sign and matches NEITHER other sign's tag.",
    },
    # ---- internal cross-laws the register must already satisfy (re-proven, not assumed) ------------
    "cross_laws": {
        "L1_family_sign": "gamma-restore <=> stabilise ; h-restore <=> {increase, decrease}. Exact "
                          "partition of all rows by (derived_family head, required_mechanism_sign).",
        "L2_join_law": "agent_mechanism_sign == required_mechanism_sign for EVERY row (an agent surfaces "
                       "only when its mechanism sign equals the family's required sign).",
        "L3_grade": "grade == 'O' for EVERY row (direction-only; magnitude-free).",
    },
    # ---- the prospective-falsification instrument itself ------------------------------------------
    "outcome_enum": ["UNTESTED", "DIRECTION_CORROBORATED", "DIRECTION_REFUTED", "INCONCLUSIVE"],
    "genesis_rule": ("every one of the 152 ledger entries is frozen at status UNTESTED. No external "
                     "prospective test has been logged; this round claims NO outcome. The genesis ledger "
                     "is content-hashed and is the artifact future sessions APPEND to."),
    "append_only_protocol": {
        "how_an_outcome_is_logged": "by APPENDING a new chained record -- never mutating genesis -- that "
                                    "cites (a) the falsifier id == the register row_hash (pins it to the "
                                    "frozen chain), (b) the external source (PMID/DOI/NCT), (c) the "
                                    "outcome enum, (d) a magnitude-free note.",
        "refuted_handling": "a DIRECTION_REFUTED outcome APPENDS a documented Track-A re-derivation flag "
                            "for the (gene, family, direction) -- the honest self-correction path, exactly "
                            "as V10 logged its CASR over-exclusion -- and is NEVER a silent drop.",
        "corroborated_handling": "a DIRECTION_CORROBORATED outcome is recorded as external support; it does "
                                 "NOT upgrade the lead to a treatment claim (direction != efficacy; the "
                                 "lead stays [O]).",
        "chain": "appended outcomes form their own append-only hash chain rooted at the genesis ledger "
                 "content hash, so the full falsification history is auditable end to end.",
    },
    "prospective_denominators": {
        "total_falsifiable_direction_hypotheses": 152,
        "open_novel": 69,
        "rediscovery_direction_corroborated_by_existing_practice": 83,
        "reading": "all 152 ship a refutable direction falsifier. The 69 `novel` rows are GENUINELY OPEN "
                   "-- their direction is an untested [O] lead and external falsification is the decisive "
                   "test. The 83 `rediscovery` rows have a direction already concordant with "
                   "established/approved practice (a consistency signal, V8-audited), so their falsifier "
                   "carries lower open-risk -- but each is still logged, because rediscovery corroborates "
                   "the DIRECTION, not a proof the geometry derived it for the right reason.",
    },
    "inheritance_discipline": {
        "inherits_invariants": "firewall PASS 0 leaks (kit _magnitude_leak verbatim); every string "
                               "magnitude-free; direction-only [O]; determinism 2x byte-identical; no "
                               "silent states; honest [V]/[F]/[O] grading.",
        "inherits_derivation_identity": "READ-ONLY over the frozen 128-core: 0 of 128 re-derived; "
                                        "disease_inputs e9003054... and mapped_levers 93ba3c89... asserted "
                                        "byte-identical (core-SUBSET invariance, 128-core root 7340874a...).",
        "inherits_register_chain": "the frozen 152-row register (chain head ca179625...) is unmutated and "
                                   "un-relabelled; the ledger is built from it read-only and keyed by its "
                                   "row hashes; the VALIDATION chain continues V11 (append-only).",
        "inherits_source_warrant": "no NEW external source is introduced (no snapshot to vendor); each "
                                   "falsifier's warrant is the already-source-verified register row it "
                                   "belongs to (Probe-8 AUDIT-PASS, 91/91, established upstream).",
        "inherits_novelty_warrant": "the V11 novelty pillar (in-disease 17/69, SPECIFIC 15/22 vs BROAD "
                                    "2/47, novel|approved=0) supplies the open/corroborated split this "
                                    "round freezes into the prospective-falsification denominator.",
    },
    "continues_from": {
        "round": "V11",
        "chain_head": "542971ddda3a801fdb19ef4bd1b1d861f5402d8e05d394e8948249f5a664c4c8",
        "results": "v11_results.json",
    },
    "verdict_rule": ("report the genesis ledger WITH its 1:1-correspondence proof (W5), the five "
                     "well-formedness checks (W1-W4) passing on every row, the three cross-laws (L1-L3) "
                     "re-proven, and the open/corroborated split. The genesis ledger asserts all 152 = "
                     "UNTESTED -- NO outcome is claimed. The instrument (outcome enum + append-only "
                     "protocol + Track-A refuted-flag path) is established and frozen, CLOSING the §5.3 "
                     "ledger: three in-house metrics executed (V10/V11 + V1-V8) plus the external "
                     "prospective-falsification instrument now stood up. No naked claim; no magnitude; "
                     "every lead stays [O]."),
    "expected": ("all 152 falsifiers pass W1-W5 and the register satisfies L1-L3 (the register is already "
                 "internally pristine -- 0 missing falsifiers, join law 152/152, family<->sign exact), so "
                 "the genesis ledger is a clean 152-entry UNTESTED instrument. If any falsifier FAILED a "
                 "well-formedness check, THAT is the finding -- a defect to fix at source, never papered "
                 "over. The audit biases toward finding defects, never toward declaring the kit clean."),
}

content_hash = sha256_str(canonical(prereg))
prereg["prereg_sha256"] = content_hash

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(prereg, fh, ensure_ascii=False, indent=1, sort_keys=True)

print(f"[V12] prereg frozen -> {os.path.basename(OUT)}")
print(f"[V12] prereg_sha256 (content) : {content_hash}")
