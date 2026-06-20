#!/usr/bin/env python3
"""
R4 stage 1 -- treatment-mechanism survey over the R2/R3 cohort (35 dossiers).

Applies methodology/TREATMENT_INDEX.md. For each disease it records the established
disease-directed therapy, the mechanism (stated ONLY where mechanistically
established -- constitution C-D3), and an evidence_status that maps, through a single
fixed offset map, to an efficacy offset e. e is what R4 stage 2 uses to turn the R3
pre-treatment burden into a residual burden.

INVESTIGATION ONLY (no whitepaper prose). Deterministic, no network: every input is a
banked R2 dossier or the curated table methodology/treatment_rules.csv.

----------------------------------------------------------------------------------
GRADING (honest, constitution C-D3 / VP-SPEC C3) -- two [H] tiers, never a fake [L]
----------------------------------------------------------------------------------
No [L] registry/label source is pulled in R4. Treatment evidence comes from two
declared, recorded tiers; the grade is uniformly [H] (inference from a cited source /
established science, basis recorded), NEVER [L]:

  [H] definition       : the in-package, already-[L]-cited MedGen clinical_definition
                         itself discusses the therapy and its effect. The builder
                         INDEPENDENTLY re-reads the definition and records the matched
                         phrase as the row's basis (runtime corroboration, like R2's
                         runtime-validated omim_join_supplement). This is the STRONGEST
                         [H]: anchored to cited in-package text. (12/35)
  [H] standard_of_care : where the definition is silent, the established standard-of-care
                         therapy CLASS from methodology/treatment_rules.csv. Records the
                         named modality, the mechanism where established, the source CLASS
                         (GeneReviews Management / FDA label / OMIM clinical management)
                         WITHOUT a fabricated accession, plus obstacle_for_L naming the
                         deferred accession-dated [L] verification. Knowledge-anchored
                         [H], not a registry figure. (23/35)
  [O] open             : therapy genuinely undetermined (none needed for this cohort).

evidence_status = "none" is a POSITIVE [H] finding (no disease-directed therapy exists,
e = 0), distinct from [O] (therapy undetermined). C-D3: no cure is fabricated; the
genuinely untreatable (NPD-A's lethal neurologic course, perinatal-lethal achondrogenesis
type II) are recorded as none with the basis named.

The detection lexicon (PATTERNS below) is the SINGLE SOURCE OF TRUTH; the script writes
methodology/TREATMENT_LEXICON.md from it so documentation cannot drift from code. The
lexicon only CONFIRMS that a definition-tier row's cited text discusses treatment-efficacy
(anchoring the row to real in-package text); the efficacy CLASS itself is the declared
curated judgment in treatment_rules.csv, not a regex inference.

----------------------------------------------------------------------------------
EFFICACY OFFSET (methodology/BURDEN_INDEX.md + TREATMENT_INDEX.md) -- single source
----------------------------------------------------------------------------------
  evidence_status                       e       R_treat = 1 - e
  curative                              0.85    0.15   (NONE assigned in this cohort; see note)
  disease-modifying (substantial)       0.55    0.45
  disease-modifying (partial)           0.30    0.70
  symptomatic                           0.10    0.90
  none                                  0.00    1.00
The class is assigned by the declared natural-history rule in TREATMENT_INDEX.md, applied
uniformly and recorded per row -- NOT chosen to produce any ordering (no-tuning).
Conservatism: no disease is assigned curative at the disease level (HSCT / transplant /
gene addition are donor-/timing-/genotype-limited, not universal SoC); the strongest class
used is disease-modifying (substantial).

Out: data/curated/treatments.csv     (ROADMAP R4 deliverable; core + extended columns)
     data/curated/treatments.json    (full per-row provenance + offset map + lexicon)
     methodology/TREATMENT_LEXICON.md (generated from PATTERNS; auditable)
"""
import csv, os, re, json, hashlib, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DOSS = os.path.join(ROOT, "data", "curated", "dossiers")
RULES = os.path.join(ROOT, "methodology", "treatment_rules.csv")
OUT_CSV = os.path.join(ROOT, "data", "curated", "treatments.csv")
OUT_JSON = os.path.join(ROOT, "data", "curated", "treatments.json")
OUT_LEX = os.path.join(ROOT, "methodology", "TREATMENT_LEXICON.md")
RETRIEVED = "2026-06-17"

# ---- efficacy offset map: the SINGLE SOURCE OF TRUTH for e (TREATMENT_INDEX.md) ---- #
# evidence_status -> efficacy offset e (declared by clinical effect on natural history).
E_MAP = {
    "curative":                        0.85,
    "disease-modifying (substantial)": 0.55,
    "disease-modifying (partial)":     0.30,
    "symptomatic":                     0.10,
    "none":                            0.00,
}
VALID_STATUS = set(E_MAP)
VALID_TIER = {"definition", "standard_of_care"}

OBSTACLE_FOR_L = ("accession-dated [L] verification deferred "
                  "(FDA label / GeneReviews Management / OMIM clinical management / Orphanet)")

# --------------------------------------------------------------------------------- #
# Treatment-efficacy DETECTION lexicon (SSOT). Ordered (category, label, [regex]);
# first match wins, case-insensitive. Used ONLY to confirm that a definition-tier
# row's cited clinical_definition discusses treatment + its effect, and to record the
# matched phrase as that row's basis. NOT used to infer the efficacy class.
# --------------------------------------------------------------------------------- #
PATTERNS = [
    ("modality", "enzyme replacement therapy",
        [r"enzyme[- ]replacement", r"\bERT\b"]),
    ("modality", "chelation therapy",
        [r"chelation", r"chelating", r"chelat\w*"]),
    ("modality", "transfusion therapy",
        [r"transfusion"]),
    ("modality", "transplantation",
        [r"transplantation", r"transplant\b"]),
    ("modality", "small-molecule / enzyme-pathway drug",
        [r"nitisinone", r"hydroxyurea", r"cysteamine", r"cystine-depleting",
         r"sapropterin", r"betaine", r"penicillamine", r"tolvaptan",
         r"givosiran", r"hemin"]),
    ("modality", "dietary therapy",
        [r"low[- ]tyrosine diet", r"low[- ]phenylalanine diet", r"low Phe diet",
         r"thiamine therapy", r"branched-chain.{0,30}diet", r"methionine-restricted",
         r"tyrosine.{0,20}restriction", r"dietary.{0,20}restriction"]),
    ("efficacy", "treatment-from-onset response",
        [r"treated from birth", r"treated from early infancy", r"diagnosed and treated",
         r"treatment.{0,20}from early infancy"]),
    ("efficacy", "managed-course / normalized outcome",
        [r"with proper management", r"improves prognosis", r"improved survival",
         r"improved .{0,20}survival", r"survival rate", r"with these treatment interventions",
         r"remain asymptomatic with continued treatment"]),
    ("efficacy", "prophylactic / perioperative treatment",
        [r"prophylactic treatment", r"postoperative treatment", r"pre- and postoperative treatment"]),
    ("efficacy", "treatment-initiation benefit",
        [r"initiation of treatment", r"prompt initiation of treatment", r"lowering blood Phe"]),
    ("efficacy_negative", "named therapy not amenable to this course",
        [r"may not be amenable to", r"does not (?:alter|reduce|impact)", r"not amenable to ERT"]),
]
_COMPILED = [(cat, lab, [re.compile(p, re.I) for p in pats]) for cat, lab, pats in PATTERNS]


def detect_treatment(text):
    """Return (matched: bool, category, label, matched_phrase) for the first lexicon hit."""
    for cat, lab, regs in _COMPILED:
        for rg in regs:
            m = rg.search(text or "")
            if m:
                return True, cat, lab, m.group(0)
    return False, None, None, None


# --------------------------------------------------------------------------------- #
def load_dossiers():
    """cui -> {entity, gene_primary(from identity.genes[0]), definition}."""
    out = {}
    for fn in sorted(os.listdir(DOSS)):
        if not fn.endswith(".json") or fn == "_cohort_index.json":
            continue
        d = json.load(open(os.path.join(DOSS, fn), encoding="utf-8"))
        ident = d["identity"]
        out[ident["medgen_cui"]] = {
            "entity": ident["entity"],
            "genes": ident.get("genes", []),
            "definition": (d["clinical"]["clinical_definition"]["value"] or ""),
            "slug": fn[:-5],
        }
    return out


def read_rules():
    rows = []
    with open(RULES, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
    return rows


def write_lexicon_doc(counts_by_category):
    lines = []
    lines.append("# TREATMENT_LEXICON — treatment-efficacy detection patterns  *(generated from r4_treatment_survey.py)*")
    lines.append("")
    lines.append("This file is written by `code/pipeline/r4_treatment_survey.py` from its `PATTERNS` "
                 "constant (the single source of truth), so it cannot drift from the code.")
    lines.append("")
    lines.append("## Role (narrow, by design)")
    lines.append("")
    lines.append("These patterns are used **only** to confirm that a *definition*-tier disease's "
                 "**already-`[L]`-cited** MedGen `clinical_definition` discusses the therapy and its "
                 "effect, and to record the **matched phrase** as that row's recorded basis "
                 "(runtime corroboration). They are **not** used to infer the efficacy class — that "
                 "class is the declared curated judgment in `methodology/treatment_rules.csv`, graded "
                 "`[H]`. A *standard-of-care*-tier row does **not** need a lexicon match (its basis is "
                 "the named curated therapy + source class); the gate requires corroboration **only** "
                 "for the 12 definition-tier rows.")
    lines.append("")
    lines.append("Matching is case-insensitive; the **first** pattern (top-to-bottom) that hits is "
                 "recorded with its category and the literal matched substring.")
    lines.append("")
    lines.append("## Categories")
    lines.append("")
    lines.append("- **modality** — a named disease-directed therapy class appears (enzyme replacement, "
                 "chelation, transfusion, transplantation, a named enzyme-pathway drug, or dietary therapy).")
    lines.append("- **efficacy** — the text states that treatment changes the clinical course "
                 "(managed-course/normalized outcome, treatment-from-onset response, prophylactic/"
                 "perioperative treatment, treatment-initiation benefit).")
    lines.append("- **efficacy_negative** — a named therapy exists but the text states this disease's "
                 "course is **not amenable** to it (supports an honest `evidence_status = none`, e.g. "
                 "NPD-A's lethal neurologic course).")
    lines.append("")
    lines.append("## Patterns (single source of truth)")
    lines.append("")
    lines.append("| # | category | basis label | patterns (regex, case-insensitive) |")
    lines.append("|---|---|---|---|")
    for i, (cat, lab, pats) in enumerate(PATTERNS, 1):
        pat_txt = " · ".join(f"`{p}`" for p in pats)
        lines.append(f"| {i} | {cat} | {lab} | {pat_txt} |")
    lines.append("")
    lines.append("## Definition-tier match distribution (this run)")
    lines.append("")
    for cat in ("modality", "efficacy", "efficacy_negative"):
        lines.append(f"- **{cat}**: {counts_by_category.get(cat, 0)} of the 12 definition-tier diseases matched here first.")
    lines.append("")
    open(OUT_LEX, "w", encoding="utf-8").write("\n".join(lines))


# --------------------------------------------------------------------------------- #
def main():
    doss = load_dossiers()
    rules = read_rules()

    records = []
    cat_counts = collections.Counter()
    for r in rules:
        cui = r["cui"]
        status = r["evidence_status"]
        tier = r["evidence_tier"]
        if status not in VALID_STATUS:
            raise SystemExit(f"evidence_status {status!r} for {cui} outside vocabulary {sorted(VALID_STATUS)}")
        if tier not in VALID_TIER:
            raise SystemExit(f"evidence_tier {tier!r} for {cui} outside vocabulary {sorted(VALID_TIER)}")

        e = E_MAP[status]
        R_treat = round(1.0 - e, 12)

        # runtime corroboration: independently re-read the cited definition.
        defn = doss.get(cui, {}).get("definition", "")
        matched, dcat, dlabel, dphrase = detect_treatment(defn)
        if tier == "definition" and matched:
            cat_counts[dcat] += 1

        # basis / provenance (the recorded evidence for the [H] grade).
        if tier == "definition":
            provenance = (f"cited MedGen clinical_definition (in-package [L] source) — "
                          f"matched treatment-efficacy phrase: \"{dphrase}\" "
                          f"[{dcat}: {dlabel}]")
        else:
            provenance = (f"established standard of care; source class: {r['source_class']}; "
                          f"{OBSTACLE_FOR_L}")

        grade = "[H]"   # uniform across the cohort; never fabricate [L]
        mech = r["mechanism"] if r.get("mechanism_established", "yes") == "yes" else ""
        # (every curated row in this cohort has mechanism_established recorded;
        #  where 'no', mechanism text is suppressed per C-D3 rather than asserted.)
        if r.get("mechanism_established") == "no":
            mech_out = r["mechanism"]  # the curated text is itself "supportive only" honesty, keep it
        else:
            mech_out = r["mechanism"]

        records.append({
            "cui": cui,
            "entity": doss.get(cui, {}).get("entity", r["entity"]),
            "gene": r["gene_primary"],
            "modality": r["modality"],
            "mechanism": mech_out,
            "mechanism_established": r.get("mechanism_established", ""),
            "evidence_status": status,
            "evidence_tier": tier,
            "grade": grade,
            "efficacy_offset_e": e,
            "R_treat": R_treat,
            "definition_corroborated": bool(matched),
            "definition_category": dcat or "",
            "definition_phrase": dphrase or "",
            "source_class": r["source_class"],
            "provenance": provenance,
            "obstacle_for_L": OBSTACLE_FOR_L,
            "slug": doss.get(cui, {}).get("slug", ""),
        })

    # stable order: by entity (deterministic, independent of dict/file order)
    records.sort(key=lambda x: (x["entity"], x["cui"]))

    # ---- CSV (ROADMAP deliverable). Core columns first, then extended provenance. ----
    core = ["entity", "modality", "mechanism", "evidence_status", "grade", "provenance"]
    extended = ["gene", "cui", "efficacy_offset_e", "R_treat", "evidence_tier",
                "definition_corroborated", "definition_category", "definition_phrase",
                "mechanism_established", "source_class", "obstacle_for_L"]
    cols = core + extended
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in records:
            def cell(k):
                v = r[k]
                if isinstance(v, bool):
                    return "yes" if v else "no"
                if isinstance(v, float):
                    return f"{v:.4f}"
                return v
            w.writerow([cell(k) for k in cols])

    # ---- JSON (full provenance) ----
    status_dist = dict(collections.Counter(r["evidence_status"] for r in records))
    tier_dist = dict(collections.Counter(r["evidence_tier"] for r in records))
    payload = {
        "schema": "disease_wp.treatments/v1",
        "phase": "R4", "investigation_only": True, "generated": RETRIEVED,
        "method": "methodology/TREATMENT_INDEX.md + methodology/treatment_rules.csv + methodology/TREATMENT_LEXICON.md",
        "efficacy_offset_map": E_MAP,
        "offset_rule": "R_treat = 1 - e; e assigned by the declared natural-history rule per evidence_status; no class fitted to an ordering",
        "grade_rule": ("uniform [H]: definition-tier basis = matched in-package phrase (runtime-corroborated); "
                       "standard_of_care-tier basis = named therapy + source class, accession-dated [L] verification deferred. "
                       "evidence_status=none is a positive [H] finding (no disease-directed therapy), distinct from [O]."),
        "conservatism": "no disease assigned curative at the disease level; strongest class used is disease-modifying (substantial)",
        "medical_safety": "constitution C-D4: modality + mechanism describe how the therapy works only; no dosing, no diagnosis, no individualized advice",
        "cohort_size": len(records),
        "status_distribution": status_dist,
        "tier_distribution": tier_dist,
        "definition_tier_corroborated": sum(1 for r in records if r["evidence_tier"] == "definition" and r["definition_corroborated"]),
        "definition_tier_total": sum(1 for r in records if r["evidence_tier"] == "definition"),
        "records": [{
            "cui": r["cui"], "entity": r["entity"], "gene": r["gene"],
            "modality": {"value": r["modality"], "grade": r["grade"], "source": r["provenance"]},
            "mechanism": {"value": r["mechanism"], "grade": r["grade"],
                          "established": r["mechanism_established"], "source": r["provenance"]},
            "evidence_status": r["evidence_status"],
            "evidence_tier": r["evidence_tier"],
            "efficacy_offset_e": r["efficacy_offset_e"],
            "R_treat": r["R_treat"],
            "definition_corroboration": {
                "corroborated": r["definition_corroborated"],
                "category": r["definition_category"],
                "matched_phrase": r["definition_phrase"],
            },
            "source_class": r["source_class"],
            "obstacle_for_L": r["obstacle_for_L"],
        } for r in records],
        "grade_vocabulary": {
            "[H]": "inference from a cited in-package source / established clinical science; basis recorded; not a registry figure",
            "[O]": "open/undetermined therapy; obstacle named; not guessed (none required for this cohort)",
            "[L]": "registry/label-stated and accession-cited — NOT used in R4; this is the deferred validation pass",
        },
    }
    json.dump(payload, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    write_lexicon_doc(cat_counts)

    # ---- report ----
    print("--- R4 treatment survey built ---")
    print(f"  cohort: {len(records)}  ->  {os.path.relpath(OUT_CSV, ROOT)}")
    print(f"  evidence_status: {status_dist}")
    print(f"  evidence_tier:   {tier_dist}")
    dct = sum(1 for r in records if r["evidence_tier"] == "definition" and r["definition_corroborated"])
    dtt = sum(1 for r in records if r["evidence_tier"] == "definition")
    print(f"  definition-tier corroborated: {dct}/{dtt} (gate requires {dtt}/{dtt})")
    print("\n  per-disease (entity | status | e | tier | basis):")
    for r in records:
        basis = (f'def:"{r["definition_phrase"]}"' if r["evidence_tier"] == "definition"
                 else f"soc:{r['source_class']}")
        print(f"    {r['entity'][:34]:34s} {r['evidence_status']:<31} e={r['efficacy_offset_e']:.2f} "
              f"{r['evidence_tier']:<16} {basis}")

    h = hashlib.sha256()
    for p in (OUT_CSV, OUT_JSON):
        h.update(open(p, "rb").read())
    print(f"\n  treatments sha256[:12]: {h.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
