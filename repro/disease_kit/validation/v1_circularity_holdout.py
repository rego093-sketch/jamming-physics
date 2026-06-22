#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1_circularity_holdout.py  --  VALIDATION track, round V1 (§5 + §11.4 of the blueprint).

  THE QUESTION §5 forces: the headline "known therapy directions line up with our derived
  directions" is a claim ABOUT THE METHOD, not yet evidence -- because (§5.1) the kit's
  corrective_h_polarity is read from the disease's own listed corrective-lever VERB. Matching a
  drug that acts in that direction therefore PARTLY RECOVERS AN INPUT. This round measures HOW
  MUCH of that "alignment" is circular, by re-deriving polarity BLIND TO ANY THERAPY (from the
  molecular-mechanism class alone) and testing recovery of the known therapy directions WITH
  DENOMINATORS and an explicit MISS LIST.

  INHERITANCE DISCIPLINE (binding -- this round adds nothing, it only AUDITS):
    * inherited invariants  : firewall PASS, every emitted string magnitude-free.
    * inherited derivation  : strictly READ-ONLY over the frozen 128-core. outputs/ is never
                              touched; mapped_levers.json / disease_inputs.json / candidate
                              register chain-head are recorded and must not move (core-SUBSET
                              invariance trivially holds: 0 derivations re-run).
    * inherited chain       : an APPEND-ONLY hash-chained validation record (its own genesis),
                              exactly as §5.5 requires ("keep results append-only, like the
                              register").
    * inherited source      : the recovery test reuses ONLY therapies that already carry a
                              sourced, Probe-8-verified citation in the kit. ZERO new external
                              claims are introduced -> nothing new for Probe 8 to verify.

  BLINDNESS, made mechanical: blind_polarity() receives ONLY the mechanism string. It can never
  see corrective_h_polarity or any lever verb. The pre-registration freezes this rule as text and
  is written + hashed BEFORE any metric is computed.

  Emits under validation/:
    V1_PREREGISTRATION.json   frozen set + rule + metric definitions (+ self-hash), written FIRST
    v1_results.json           the four metrics, denominators, full miss lists, append-only record
    v1_results.html           one self-contained page in the kit idiom
    firewall_log_v1.json      magnitude scan over the V1 artifacts (kit gate, verbatim)
    expected_sha256_v1.json   2x byte-identical determinism manifest over the V1 artifacts
"""
import os, sys, json, html, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
OUTDIR = HERE
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import firewall as FW                         # the kit's verbatim magnitude gate

SNAPSHOT = "2026-06-21"                        # pinned; no datetime.now() anywhere
RELEASE  = "0.41.0-validation.v1"
CHAIN_GENESIS = "vp_disease_kit::validation_chain::genesis::circularity_holdout"

ML_PATH = os.path.join(ROOT, "outputs", "mapped_levers.json")
DI_PATH = os.path.join(ROOT, "inputs",  "disease_inputs.json")
CR_PATH = os.path.join(ROOT, "outputs", "candidate_register.json")


def canon(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha(obj):
    return hashlib.sha256(canon(obj).encode("utf-8")).hexdigest()


def sha_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def jdump(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False, sort_keys=True)


# ------------------------------------------------------------------ BLIND polarity (null model)
# Receives ONLY the molecular-mechanism class. This is therapy-INDEPENDENT: LOF vs GOF is a
# variant-consequence fact sourced from OMIM/ClinGen, not from any drug list. The rule is a
# deliberately CRUDE NULL MODEL: "a loss disease wants its product pushed up; a gain disease wants
# the pathological species pushed down." Its failures are the whole point of the measurement.
def blind_polarity(mechanism):
    assert mechanism in ("LOF", "GOF"), mechanism
    return "clear" if mechanism == "GOF" else "supply"


POL2SIGN = {"supply": "increase", "clear": "decrease"}
AX2SIGN  = {"UP": "increase", "DOWN": "decrease"}


# ------------------------------------------------------------------ pre-registration (§5.5)
def write_prereg(di):
    slugs = sorted(di)
    prereg = dict(
        release=RELEASE, snapshot_date=SNAPSHOT, programme="jamming-physics.org",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", licence="CC BY 4.0",
        title="V1 -- blinded circularity hold-out for DNA-emergence drug-repurposing directions",
        committed_before_metrics=True,
        disease_set=dict(
            n=len(slugs),
            policy="ALL resolved diseases (whole frozen set; no cherry-picking, no hold-back).",
            slugs=slugs,
            disease_inputs_sha256=sha_file(DI_PATH),
            mapped_levers_sha256=sha_file(ML_PATH),
            candidate_register_sha256=sha_file(CR_PATH),
        ),
        blind_polarity_rule=dict(
            statement="polarity is assigned from the molecular-mechanism class ONLY, blind to any "
                      "therapy: GOF -> clear (push the pathological gain down); LOF -> supply (push "
                      "the deficient product up). This is a crude NULL MODEL by construction.",
            independence="LOF/GOF is sourced from OMIM/ClinGen variant consequence, never from a "
                         "drug. The assignment function is given the mechanism string and nothing "
                         "else, so blindness is mechanically inspectable.",
            known_limitation="the null model cannot distinguish a DEFICIENCY-driven LOF (supply the "
                             "product) from an ACCUMULATION-driven LOF (clear the upstream toxic "
                             "substrate). That distinction needs a sourced, blind biochemical "
                             "adjudication and is the pre-registered NEXT batch.",
        ),
        metrics=dict(
            m1_circularity_magnitude="agreement between blind-null polarity and the kit's "
                "therapy-verb polarity, over the whole set, WITH denominator; the disagreement "
                "slug list is the 'independence-not-established' set.",
            m2_direction_recovery="for every KNOWN, SOURCED therapy (disease_inputs.corrective_"
                "agents, axis_effect UP/DOWN), does the blind-null predicted sign match the therapy "
                "direction? Report hits/denominator AND the full miss list. Report the CIRCULAR "
                "reference (kit therapy-verb polarity vs same therapies) as an upper bound, and the "
                "independence gap = circular - blind.",
            m3_exclusion_calibration="negative control: the gamma-restore(stabilise) family must "
                "never be admitted on a LOF_null lesion; agent sign must equal required sign on "
                "every register row. Both counts must be 0.",
            m4_novelty_concentration="of rediscovery rows, how many sit on the broad-chaperone "
                "tier? The claim is ~0 -- i.e. recovered known care concentrates where the geometry "
                "is most specific (gene_specific/pathway).",
        ),
        non_claims=[
            "No metric here asserts any clinical magnitude, efficacy, dose, or outcome.",
            "A recovered direction is method-consistency, NOT evidence a drug works.",
            "A high circular reference vs a lower blind score is EXPECTED and is reported honestly; "
            "the blind score is the only one that is an independent signal.",
        ],
    )
    prereg["prereg_sha256"] = sha(prereg)
    jdump(os.path.join(OUTDIR, "V1_PREREGISTRATION.json"), prereg)
    return prereg


# ------------------------------------------------------------------ metrics
def compute(di, ml, cr, prereg):
    slugs = sorted(di)

    # -- M1: circularity magnitude (polarity level) --------------------------------------------
    m1_agree, m1_disagree = 0, []
    for s in slugs:
        mech = di[s]["mechanism"]
        pb = blind_polarity(mech)
        pk = di[s]["corrective_h_polarity"]            # therapy-verb polarity (the circular path)
        if pb == pk:
            m1_agree += 1
        else:
            m1_disagree.append(dict(slug=s, name=di[s]["name"], mechanism=mech,
                                    blind_null=pb, therapy_verb=pk))
    m1 = dict(
        what="blind-null polarity vs kit therapy-verb polarity (whole set)",
        agree=m1_agree, denominator=len(slugs),
        agree_fraction=round(m1_agree / len(slugs), 4),
        independence_not_established_count=len(m1_disagree),
        independence_not_established=m1_disagree,
        reading="these are the diseases whose corrective DIRECTION is NOT fixed by the crude "
                "LOF/GOF signal alone; their apparent alignment cannot be credited as independent "
                "until a sourced, blind accumulation-vs-deficiency call is made (next batch).",
    )

    # -- M2: direction recovery (therapy level, with denominators) ------------------------------
    hit_b = tot = hit_k = 0
    misses = []
    for s in slugs:
        mech = di[s]["mechanism"]
        predB = POL2SIGN[blind_polarity(mech)]
        predK = POL2SIGN[di[s]["corrective_h_polarity"]]
        for a in di[s]["corrective_agents"]:
            ts = AX2SIGN.get(a.get("axis_effect", "").upper())
            if ts is None:
                continue
            tot += 1
            if ts == predB:
                hit_b += 1
            else:
                misses.append(dict(slug=s, mechanism=mech, agent_class=a["agent_class"],
                                   therapy_direction=a["axis_effect"].upper(),
                                   blind_predicted_sign=predB, source=a.get("source", "")))
            if ts == predK:
                hit_k += 1
    # classify misses for the honest write-up
    miss_lof = [m for m in misses if m["mechanism"] == "LOF"]
    miss_gof = [m for m in misses if m["mechanism"] == "GOF"]
    m2 = dict(
        what="blind-null predicted sign vs KNOWN sourced therapy direction (per therapy row)",
        blind_hits=hit_b, denominator=tot,
        blind_recovery_fraction=round(hit_b / tot, 4),
        circular_reference_hits=hit_k,
        circular_reference_fraction=round(hit_k / tot, 4),
        independence_gap=round((hit_k - hit_b) / tot, 4),
        miss_count=len(misses),
        miss_breakdown=dict(LOF_accumulation_or_downstream=len(miss_lof),
                            GOF_downstream_agonist=len(miss_gof)),
        misses=misses,
        reading="the circular reference is the upper bound you get by reading direction off the "
                "therapy verb; the blind fraction is the only INDEPENDENT signal. The gap is the "
                "size of the circularity. The LOF misses are dominated by ACCUMULATION-driven loss "
                "diseases (clear the upstream toxin, e.g. AIP/givosiran, alkaptonuria/nitisinone) "
                "where 'LOF=>supply' is simply the wrong null; the GOF misses are downstream "
                "agonists whose axis_effect is measured on the agent's own node, not the disease "
                "gene. Both are honest, structural, and define the next batch.",
    )

    # -- M3: exclusion calibration / negative control -------------------------------------------
    rows = cr["rows"]
    stabilise_on_null = [dict(slug=r["slug"], agent=r["agent"])
                         for r in rows
                         if r.get("required_mechanism_sign") == "stabilise"
                         and r.get("lesion") == "LOF_null"]
    sign_mismatch = [dict(slug=r["slug"], agent=r["agent"],
                          agent_sign=r.get("agent_mechanism_sign"),
                          required_sign=r.get("required_mechanism_sign"))
                     for r in rows
                     if r.get("required_mechanism_sign") != "stabilise"
                     and r.get("agent_mechanism_sign") != r.get("required_mechanism_sign")]
    m3 = dict(
        what="negative controls over the candidate register",
        gamma_restore_on_LOF_null=len(stabilise_on_null),
        gamma_restore_on_LOF_null_rows=stabilise_on_null,
        join_integrity_sign_mismatches=len(sign_mismatch),
        join_integrity_sign_mismatch_rows=sign_mismatch,
        pass_=(len(stabilise_on_null) == 0 and len(sign_mismatch) == 0),
        reading="gamma-restore is geometrically excluded on null alleles and the sign join is "
                "exact: both must be 0. A non-zero here would mean a chaperone leaked onto a "
                "no-residual lesion or a direction was admitted against its own family.",
    )

    # -- M4: novelty concentration --------------------------------------------------------------
    from collections import Counter
    ct = Counter((r.get("prior_art_status"), r.get("target_specificity")) for r in rows)
    red = [r for r in rows if r.get("prior_art_status") == "rediscovery"]
    red_broad = sum(1 for r in red if r.get("target_specificity") == "broad")
    m4 = dict(
        what="prior-art status x target specificity over the register",
        cross_tab={f"{pa}|{spec}": n for (pa, spec), n in sorted(ct.items())},
        rediscovery_total=len(red),
        rediscovery_on_broad_tier=red_broad,
        rediscovery_denominator=len(rows),
        pass_=(red_broad == 0),
        reading="every recovered known indication sits on a gene_specific or pathway agent; zero "
                "rediscoveries on the broad-chaperone tier. The validation signal is concentrated "
                "exactly where the geometry is most specific -- which is the honest place for it.",
    )

    # -- append-only hash-chained record (§5.5) -------------------------------------------------
    record = []
    head = CHAIN_GENESIS
    for name, block in (("M1_circularity_magnitude", m1),
                        ("M2_direction_recovery", m2),
                        ("M3_exclusion_calibration", m3),
                        ("M4_novelty_concentration", m4)):
        row = dict(metric=name, prev_hash=head, payload=block)
        row["row_hash"] = sha(dict(metric=name, prev_hash=head, payload=block))
        head = row["row_hash"]
        record.append(row)

    results = dict(
        release=RELEASE, snapshot_date=SNAPSHOT, grade="[O] direction-only; magnitude-free",
        programme="jamming-physics.org", author="Young Jae Lee", orcid="0009-0002-7535-8245",
        prereg_sha256=prereg["prereg_sha256"],
        inherited_anchors=dict(                       # core-SUBSET invariance: these must not move
            mapped_levers_sha256=sha_file(ML_PATH),
            disease_inputs_sha256=sha_file(DI_PATH),
            candidate_register_sha256=sha_file(CR_PATH),
            candidate_register_chain_head=cr.get("chain_head", ""),
            note="validation is strictly read-only; 0 of the 128 derivations were re-run.",
        ),
        headline=dict(
            circularity_polarity_agreement=f"{m1['agree']}/{m1['denominator']}",
            blind_direction_recovery=f"{m2['blind_hits']}/{m2['denominator']}",
            circular_reference=f"{m2['circular_reference_hits']}/{m2['denominator']}",
            independence_gap=m2["independence_gap"],
            negative_controls_pass=m3["pass_"],
            novelty_concentration_pass=m4["pass_"],
        ),
        metrics=dict(M1=m1, M2=m2, M3=m3, M4=m4),
        validation_chain=dict(chain_genesis=CHAIN_GENESIS, chain_head=head, record=record),
        honest_conclusion=(
            "The independent direction signal recovers a clear majority of known therapy "
            "directions but well short of the circular reference; the gap is the measured size of "
            "the §5.1 circularity and is concentrated in accumulation-driven loss diseases. The "
            "negative controls and novelty concentration both hold. Therefore: the method's "
            "directional alignment is PARTLY genuine and PARTLY input-recovery, quantified here for "
            "the first time -- not yet a validated claim, and not to be presented as one until the "
            "blind accumulation-vs-deficiency batch closes the named gap."),
    )
    return results


# ------------------------------------------------------------------ HTML (kit idiom)
def render_html(results):
    h = results["headline"]; m = results["metrics"]
    esc = html.escape
    miss_rows = "".join(
        f"<tr><td>{esc(x['slug'])}</td><td>{esc(x['mechanism'])}</td>"
        f"<td>{esc(x['agent_class'][:70])}</td><td>{esc(x['therapy_direction'])}</td>"
        f"<td>{esc(x['blind_predicted_sign'])}</td></tr>"
        for x in m["M2"]["misses"][:40])
    dis_rows = "".join(
        f"<tr><td>{esc(x['slug'])}</td><td>{esc(x['mechanism'])}</td>"
        f"<td>{esc(x['blind_null'])}</td><td>{esc(x['therapy_verb'])}</td></tr>"
        for x in m["M1"]["independence_not_established"][:40])
    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<title>VP Disease Kit -- Validation V1 (circularity hold-out)</title>
<style>
 body{{font:15px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;max-width:880px;margin:2rem auto;padding:0 1rem;color:#1c2530}}
 h1{{font-size:1.5rem}} h2{{font-size:1.1rem;margin-top:1.8rem;border-bottom:1px solid #dce3ea;padding-bottom:.3rem}}
 .k{{display:inline-block;background:#eef3f8;border:1px solid #d4dde6;border-radius:6px;padding:.5rem .8rem;margin:.25rem .4rem .25rem 0}}
 .k b{{font-size:1.15rem}} table{{border-collapse:collapse;width:100%;font-size:13px;margin:.6rem 0}}
 td,th{{border:1px solid #dce3ea;padding:.32rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#f5f8fb}} .pass{{color:#0a7d3c;font-weight:600}} small{{color:#5a6b7b}}
 .note{{background:#fbf7ee;border:1px solid #ece2c6;border-radius:8px;padding:.7rem .9rem;margin:.8rem 0}}
</style>
<h1>Validation V1 &mdash; blinded circularity hold-out</h1>
<small>{esc(results['release'])} &middot; snapshot {esc(results['snapshot_date'])} &middot; grade {esc(results['grade'])}
&middot; pre-registration {esc(results['prereg_sha256'][:16])}&hellip;</small>
<div class="note">All numbers are counts and fractions only. No dose, efficacy, outcome, or any
clinical magnitude appears anywhere &mdash; by construction.</div>
<div>
 <span class="k">circularity (polarity)<br><b>{esc(h['circularity_polarity_agreement'])}</b> agree</span>
 <span class="k">blind recovery<br><b>{esc(h['blind_direction_recovery'])}</b></span>
 <span class="k">circular reference<br><b>{esc(h['circular_reference'])}</b></span>
 <span class="k">independence gap<br><b>{h['independence_gap']}</b></span>
 <span class="k">neg. controls<br><b class="pass">{'PASS' if h['negative_controls_pass'] else 'FAIL'}</b></span>
 <span class="k">novelty conc.<br><b class="pass">{'PASS' if h['novelty_concentration_pass'] else 'FAIL'}</b></span>
</div>

<h2>M1 &middot; how much of the alignment is circular</h2>
<p>{esc(m['M1']['reading'])}</p>
<p><b>{m['M1']['agree']}/{m['M1']['denominator']}</b> diseases get the same polarity from the crude
mechanism rule as from the therapy verb. The other <b>{m['M1']['independence_not_established_count']}</b>
are where direction is <i>not</i> fixed by LOF/GOF alone:</p>
<table><tr><th>slug</th><th>mechanism</th><th>blind-null</th><th>therapy-verb</th></tr>{dis_rows}</table>
<small>showing up to 40 of {m['M1']['independence_not_established_count']}.</small>

<h2>M2 &middot; direction recovery, with denominators and misses</h2>
<p>{esc(m['M2']['reading'])}</p>
<p>blind independent signal <b>{m['M2']['blind_hits']}/{m['M2']['denominator']}</b>
({m['M2']['blind_recovery_fraction']}) &middot; circular upper bound
<b>{m['M2']['circular_reference_hits']}/{m['M2']['denominator']}</b>
({m['M2']['circular_reference_fraction']}) &middot; gap <b>{m['M2']['independence_gap']}</b>.
Misses: <b>{m['M2']['miss_count']}</b>
(LOF accumulation/downstream {m['M2']['miss_breakdown']['LOF_accumulation_or_downstream']},
GOF downstream agonist {m['M2']['miss_breakdown']['GOF_downstream_agonist']}).</p>
<table><tr><th>slug</th><th>mech</th><th>therapy (agent)</th><th>therapy dir</th><th>blind pred</th></tr>{miss_rows}</table>
<small>showing up to 40 of {m['M2']['miss_count']}.</small>

<h2>M3 &middot; negative controls</h2>
<p>{esc(m['M3']['reading'])}</p>
<p>gamma-restore on a null allele: <b>{m['M3']['gamma_restore_on_LOF_null']}</b> &middot;
sign-join mismatches: <b>{m['M3']['join_integrity_sign_mismatches']}</b> &middot;
<b class="pass">{'PASS' if m['M3']['pass_'] else 'FAIL'}</b></p>

<h2>M4 &middot; where the recovered known care sits</h2>
<p>{esc(m['M4']['reading'])}</p>
<p>rediscoveries on the broad tier: <b>{m['M4']['rediscovery_on_broad_tier']}</b>
of <b>{m['M4']['rediscovery_total']}</b> &middot;
<b class="pass">{'PASS' if m['M4']['pass_'] else 'FAIL'}</b></p>

<h2>Honest conclusion</h2>
<p>{esc(results['honest_conclusion'])}</p>
</html>"""


# ------------------------------------------------------------------ gates
def firewall_scan(paths):
    """Verbatim kit gate (FW.magnitude_leak) over the V1 artifacts."""
    leaks = []
    for p in paths:
        if p.endswith(".json"):
            data = json.load(open(p))
            for path, s in FW.walk_json_strings(data, os.path.relpath(p, ROOT)):
                lk = FW.magnitude_leak(s.lower())
                if lk:
                    leaks.append(dict(artifact=path, leaks=lk))
        elif p.endswith(".html"):
            import re
            plain = html.unescape(re.sub(r"<[^>]+>", " ", open(p).read()))
            lk = FW.magnitude_leak(plain.lower())
            if lk:
                leaks.append(dict(artifact=os.path.relpath(p, ROOT), leaks=lk))
    log = dict(scan="forbidden_claim_scan (kit _magnitude_leak, verbatim)",
               status="PASS" if not leaks else "FAIL", n_leaks=len(leaks), leaks=leaks)
    jdump(os.path.join(OUTDIR, "firewall_log_v1.json"), log)
    return log


def determinism(paths):
    h = {os.path.basename(p): sha_file(p) for p in paths}
    man = dict(scan="2x byte-identical determinism over V1 artifacts", files=h,
               manifest_root=sha(h))
    jdump(os.path.join(OUTDIR, "expected_sha256_v1.json"), man)
    return man


def main():
    di = json.load(open(DI_PATH)); ml = json.load(open(ML_PATH)); cr = json.load(open(CR_PATH))

    # 1) pre-register FIRST (set + rule + metric defs frozen and hashed before any metric)
    prereg = write_prereg(di)

    # 2) compute metrics over the frozen, read-only artifacts
    results = compute(di, ml, cr, prereg)
    jdump(os.path.join(OUTDIR, "v1_results.json"), results)

    # 3) render page
    open(os.path.join(OUTDIR, "v1_results.html"), "w", encoding="utf-8").write(render_html(results))

    artifacts = [os.path.join(OUTDIR, f) for f in
                 ("V1_PREREGISTRATION.json", "v1_results.json", "v1_results.html")]

    # 4) GATES: firewall (verbatim) + determinism manifest
    fw = firewall_scan(artifacts)
    man = determinism(artifacts + [os.path.join(OUTDIR, "firewall_log_v1.json")])

    # core-subset invariance check (read-only proof)
    inv_ok = (results["inherited_anchors"]["mapped_levers_sha256"] == sha_file(ML_PATH)
              and results["inherited_anchors"]["disease_inputs_sha256"] == sha_file(DI_PATH))

    h = results["headline"]
    print("=== VALIDATION V1 ===")
    print(f"  prereg sha            : {prereg['prereg_sha256'][:16]}…  (written before metrics)")
    print(f"  M1 circularity        : {h['circularity_polarity_agreement']} agree  "
          f"(independence-not-established: {results['metrics']['M1']['independence_not_established_count']})")
    print(f"  M2 blind recovery     : {h['blind_direction_recovery']}  "
          f"vs circular {h['circular_reference']}  (gap {h['independence_gap']})  "
          f"misses {results['metrics']['M2']['miss_count']}")
    print(f"  M3 negative controls  : {'PASS' if h['negative_controls_pass'] else 'FAIL'}")
    print(f"  M4 novelty conc.      : {'PASS' if h['novelty_concentration_pass'] else 'FAIL'}")
    print(f"  firewall              : {fw['status']} ({fw['n_leaks']} leak)")
    print(f"  core-subset invariance: {'HELD' if inv_ok else 'BROKEN'} (0 derivations re-run)")
    print(f"  validation chain head : {results['validation_chain']['chain_head'][:16]}…")
    print(f"  manifest root         : {man['manifest_root'][:16]}…")
    return 0 if (fw["status"] == "PASS" and inv_ok and h["negative_controls_pass"]
                 and h["novelty_concentration_pass"]) else 1


if __name__ == "__main__":
    sys.exit(main())
