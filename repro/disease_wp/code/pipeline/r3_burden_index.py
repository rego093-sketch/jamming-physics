#!/usr/bin/env python3
"""
R3 stage 1 -- deterministic burden index ("suffering order") over the R2 cohort.

Applies methodology/BURDEN_INDEX.md to the 35 curated dossiers from R2. The index
is the package's *reproducible contribution* (VP-SPEC C1 / constitution C-D1): a
fixed, deterministic function of cited inputs. The clinical inputs themselves are
*observed* values, respected and cited -- never "reproduced".

INVESTIGATION ONLY (no whitepaper prose). Deterministic, no network: every input
is a banked dossier or the cached HPO ontology/annotations.

----------------------------------------------------------------------------------
SOURCING PRECEDENCE PER AXIS (honest grading, constitution C-D / VP-SPEC C3)
----------------------------------------------------------------------------------
The five burden components map to R2 fields. R2 structured ONE of them at registry
grade -- onset (HPO C-aspect onset annotations). The HPO "Clinical course" branch
*does* carry progression and mortality terms, but they are sparsely populated for
this cohort (progression 1/35, mortality 3/35 OMIMs). Severity and functional
status have no dedicated R2 registry source at all. So each axis is sourced by a
fixed precedence, and graded by what actually backs the value:

  [L] registry-stated : HPO annotation present (onset always; progression/mortality
                        where the Clinical-course branch is populated for the OMIM).
  [H] cited-text inference : value derived by a DECLARED, fixed lexicon over the
                        cited MedGen clinical_definition (an observed [L] source).
                        The matched phrase is recorded per row as the basis. This is
                        an inference from a cited source, not a guess.
  [O] open : neither HPO nor the definition states the axis -> value None, obstacle
                        named (a registry source -- Orphanet / OMIM clinical synopsis
                        / survival literature -- is deferred, NOT guessed).

The lexicon (PATTERNS below) is the single source of truth; the script writes
methodology/BURDEN_LEXICON.md from it so documentation cannot drift from code.

----------------------------------------------------------------------------------
COMPOSITE (BURDEN_INDEX.md)
----------------------------------------------------------------------------------
  raw_burden = (sum_present w_i * x_i) / (sum_present w_i)      # renormalised over
                                                                # the axes actually scored
Default weights are the declared equal prior w = 0.20 each. A [O] (missing) axis is
excluded from the mean (excluding is honest; substituting 0 would assert "no burden
on that axis", substituting 0.5 would guess). axes_scored records how many of 5 are
present so a sparse score is never silently compared with a complete one.

  R_treat = 1 - e ;  burden_score = raw_burden * R_treat
The treatability offset e comes from R4 treatments.csv, which does not exist yet, so
R_treat = 1.0 for every disease and is graded [O] (obstacle: R4 deferred). The
PRIMARY R3 ordering is therefore on raw_burden (pre-treatment burden); burden_score
is emitted but flagged provisional until R4.

  grade(raw_burden) = min-grade over the 5 axis grades, ordering O < H < L < V with
[O] weakest (BURDEN_INDEX floor rule). Any missing axis -> floor [O]. We also report
grade_present (floor over the axes actually scored) so the confidence of the computed
value is visible alongside the spec-faithful conservative floor.

Out: data/curated/burden_scores.csv     (flat ranking, gate- and human-readable)
     data/curated/burden_scores.json    (per-axis {value, grade, basis, source|obstacle}
                                          + weights + sensitivity + emergence links)
     methodology/BURDEN_LEXICON.md       (generated from PATTERNS; auditable)
"""
import csv, os, re, json, gzip, hashlib, collections, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DOSS = os.path.join(ROOT, "data", "curated", "dossiers")
HPOA = os.path.join(ROOT, "data", "raw", "hpo", "phenotype.hpoa.gz")
HPOBO = os.path.join(ROOT, "data", "raw", "hpo", "hp.obo.gz")
OUT_CSV = os.path.join(ROOT, "data", "curated", "burden_scores.csv")
OUT_JSON = os.path.join(ROOT, "data", "curated", "burden_scores.json")
OUT_LEX = os.path.join(ROOT, "methodology", "BURDEN_LEXICON.md")
HPOA_VERSION = "2026-06-06"
RETRIEVED = "2026-06-17"

# grade strength ordering (weakest -> strongest), BURDEN_INDEX floor rule
GRADE_RANK = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3}
def floor_grade(grades):
    gs = [g for g in grades if g in GRADE_RANK]
    return min(gs, key=lambda g: GRADE_RANK[g]) if gs else "[O]"

# default declared weights (equal prior); recorded in output
W = {"O": 0.20, "P": 0.20, "S": 0.20, "M": 0.20, "D": 0.20}

# Declared rankability threshold. raw_burden is a renormalised MEAN over the axes that are
# actually scored; a mean over fewer than a majority of the 5 axes is not a meaningful aggregate
# (e.g. a disease scored on onset alone would read 1.00 from a single axis and crowd the top of
# the order). We therefore place only diseases with a MAJORITY of axes scored (>= 3 of 5) into the
# ordered suffering-order; diseases with 1-2 scored axes are reported separately as "insufficient
# axis coverage - not placed" (rank = null). This is one fixed, declared threshold, not a tuned cut.
RANK_MIN_AXES = 3

# ----------------------------------------------------------------------------- #
# HPO ontology + annotations (mirrors r2_build_dossiers.py exactly)
# ----------------------------------------------------------------------------- #
def load_obo():
    txt = gzip.open(HPOBO, "rt", encoding="utf-8").read()
    name, parents, children = {}, {}, collections.defaultdict(list)
    for block in txt.split("\n[Term]\n"):
        mid = re.search(r"^id: (HP:\d+)", block, re.M)
        if not mid:
            continue
        tid = mid.group(1)
        mn = re.search(r"^name: (.+)$", block, re.M)
        name[tid] = mn.group(1).strip() if mn else tid
        parents[tid] = re.findall(r"^is_a: (HP:\d+)", block, re.M)
        for p in parents[tid]:
            children[p].append(tid)
    return name, parents, children

def subtree(root, children):
    seen, stack = set(), [root]
    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        stack.extend(children.get(t, []))
    return seen

def load_hpoa():
    ann = collections.defaultdict(list)
    with gzip.open(HPOA, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("database_id"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 12 or not f[0].startswith("OMIM:"):
                continue
            ann[f[0].split(":")[1]].append({
                "hpo_id": f[3], "reference": f[4], "onset": f[6],
                "frequency": f[7], "aspect": f[10],
            })
    return ann

# HPO term -> bin value maps (registry [L] sourcing)
ONSET_VAL = {  # earliness; more life-years affected = higher
    "HP:0030674": 1.0, "HP:0011460": 1.0, "HP:0011461": 1.0, "HP:0003577": 1.0,
    "HP:0003623": 1.0, "HP:0034197": 1.0, "HP:0034198": 1.0, "HP:0034199": 1.0,
    "HP:0003593": 0.85,
    "HP:0011463": 0.7, "HP:0410280": 0.7,
    "HP:0003621": 0.55,
    "HP:0011462": 0.35, "HP:0025708": 0.35, "HP:0025709": 0.35, "HP:0025710": 0.35,
    "HP:0003581": 0.35, "HP:0003596": 0.35,
    "HP:0003584": 0.2, "HP:0033765": 0.2,
}
PROG_VAL = {  # HPO Clinical-course progression terms
    "HP:0003678": 0.8,   # Rapidly progressive
    "HP:0003676": 0.5,   # Progressive
    "HP:0003677": 0.5,   # Slowly progressive
    "HP:0003682": 0.5,   # Variable progression rate
    "HP:0011010": 0.5,   # Chronic
    "HP:0003680": 0.2,   # Nonprogressive
    "HP:0031915": 0.2,   # Stable
}
MORT_VAL = {  # HPO Mortality/Aging terms
    "HP:0034241": 1.0, "HP:0003826": 1.0, "HP:0005268": 1.0,  # prenatal death / stillbirth / miscarriage
    "HP:0001522": 1.0, "HP:0003811": 1.0, "HP:0003819": 1.0,  # death infancy / neonatal / childhood
    "HP:0011421": 0.7, "HP:0100613": 0.7, "HP:0011420": 0.7,  # adolescence / early adulthood / age-of-death(unspec)
    "HP:0033763": 0.4, "HP:0033764": 0.4, "HP:0033765": 0.4,  # adulthood / middle / late
}

# ----------------------------------------------------------------------------- #
# DECLARED clinical-definition lexicon (cited-text inference -> grade [H])
#   each axis: ordered list of (value, basis_label, [regex...]).  Precedence is the
#   list order EXCEPT where a score_* function implements an explicit override
#   (documented in BURDEN_LEXICON.md and in the functions below).
# ----------------------------------------------------------------------------- #
PATTERNS = {
    "P_progression": [  # static .2 / slowly .5 / rapidly .8 / lethal-progressive 1.0
        (1.0, "progressive course with fatal outcome",
            # 'life-threatening' deliberately excluded here: it is a SEVERITY descriptor, not a
            # progression-to-death coupling. A genuine tier-1.0 requires progression explicitly
            # joined to a fatal/lethal/death/demise/terminal outcome in the same clause.
            [r"progressive[^.]*\b(?:fatal|lethal|death|demise|terminal)\b",
             r"\b(?:fatal|lethal|death|demise|terminal)\b[^.]*progressive",
             r"progressive\s+neurodegenerat"]),
        (0.8, "rapidly progressive",
            [r"rapidly\s+progressive", r"rapid(?:ly)?\s+(?:deterioration|decline|progression)",
             r"fulminant", r"aggressive\s+(?:course|progression)"]),
        (0.5, "progressive course",
            [r"slowly\s+progressive", r"\bprogressive\b",
             r"gradual(?:ly)?\s+(?:decline|deterioration|progression)",
             r"insidious", r"chronic[^.]*progress"]),
        (0.2, "non-progressive / static course",
            [r"non-?progressive", r"\bstatic\b", r"does\s+not\s+progress", r"stable\s+course"]),
    ],
    "S_severity": [  # mild .25 / moderate .5 / severe .75 / profound 1.0
        (1.0, "profound / devastating severity",
            [r"\bprofound\b", r"devastating", r"most\s+severe", r"extremely\s+severe",
             r"uniformly\s+(?:fatal|lethal)"]),
        (0.75, "severe / debilitating",
            # bare 'severe' excludes comparative references to OTHER forms ("more/most/other/less
            # severe forms of ..."), which describe related variants, not this entity. Non-comparative
            # uses ("severe anemia", "severe early-onset form") still match.
            [r"(?<!more )(?<!most )(?<!other )(?<!less )\bsevere\b",
             r"debilitating", r"life-?threatening", r"disabling",
             r"significant\s+morbidity", r"serious"]),
        (0.5, "moderate",
            [r"\bmoderate\b"]),
        (0.25, "mild / asymptomatic",
            [r"\bmild\b", r"benign\s+(?:course|condition)", r"asymptomatic"]),
    ],
    "M_mortality": [],  # mortality is classified by mortality_from_text() (sentence-level,
                        # spectrum/early-lethal/premature/qualified logic) — documented as prose
                        # in BURDEN_LEXICON.md, not as a flat first-match table.
    "D_disability": [  # independent .2 / partial .5 / high .75 / fully dependent 1.0
        (1.0, "fully dependent",
            [r"bedridden", r"fully\s+dependent", r"complete(?:ly)?\s+dependent", r"vegetative",
             r"total\s+care"]),
        (0.75, "high support need",
            [r"wheelchair", r"loss\s+of\s+(?:independent\s+)?ambulation", r"unable\s+to\s+walk",
             r"non-?ambulatory", r"requires?\s+(?:assistance|ventilation|ventilator|support)",
             r"intellectual\s+disability",
             r"severe\s+(?:developmental|cognitive|intellectual|motor)\s+(?:delay|disability|impairment)"]),
        (0.5, "partial support need",
            [r"developmental\s+delay", r"(?:learning|cognitive)\s+(?:difficult|impair|disabilit)",
             r"mobility\s+(?:impair|limit)", r"motor\s+(?:delay|impair)", r"\bdisabilit"]),
        (0.2, "functionally independent",
            # NB: deliberately excludes "normal life span" — that is a MORTALITY phrase
            # (handled by mortality_from_text), not a functional-independence signal.
            [r"normal\s+(?:development|intelligence|cognition|psychomotor)",
             r"\bindependent\b"]),
    ],
    "O_onset_text": [  # fallback only when HPO onset is absent
        (1.0, "congenital / neonatal onset",
            [r"congenital", r"at\s+birth", r"neonat\w*", r"prenatal", r"in\s+utero", r"antenatal",
             r"perinatal"]),
        (0.85, "infantile onset",
            [r"infanc\w*", r"infantile", r"first\s+(?:year|months)\s+of\s+life", r"early\s+infancy"]),
        (0.7, "childhood onset",
            [r"childhood", r"in\s+children", r"\bchildren\b", r"early\s+childhood",
             r"pediatric", r"paediatric", r"early[ -]onset",
             r"first\s+\w+\s+decades?\s+of\s+life"]),
        (0.55, "juvenile / adolescent onset",
            [r"juvenile", r"adolescen"]),
        (0.35, "adult onset",
            [r"adulthood", r"\badult\b", r"(?:second|third|fourth)\s+decade", r"middle\s+age"]),
        (0.2, "late-adult onset",
            [r"late\s+onset", r"late\s+adulthood", r"elderly", r"older\s+adults"]),
    ],
}

def first_match(text, tiers):
    """Return (value, basis_label, matched_phrase) for the first tier whose any
    pattern hits, scanning tiers in list order. None if nothing matches."""
    low = text.lower()
    for value, label, pats in tiers:
        for pat in pats:
            m = re.search(pat, low)
            if m:
                phrase = re.sub(r"\s+", " ", m.group(0)).strip()[:80]
                return value, label, phrase
    return None

# ----------------------------------------------------------------------------- #
# per-axis scorers -> (value, grade, basis, src_or_obstacle_dict)
# ----------------------------------------------------------------------------- #
def graded_axis(value, grade, basis, source=None, obstacle=None):
    o = {"value": value, "grade": grade, "basis": basis}
    if source:
        o["source"] = source
    if obstacle:
        o["obstacle"] = obstacle
    return o

def score_onset(dossier, defn, name):
    aoo = dossier["clinical"]["age_of_onset"]
    if aoo["grade"] == "[L]" and aoo["value"]:
        # earliest onset present (literal BURDEN_INDEX: more life-years affected)
        scored = [(ONSET_VAL[t["hpo_id"]], t) for t in aoo["value"] if t["hpo_id"] in ONSET_VAL]
        if scored:
            val = max(s[0] for s in scored)
            terms = ", ".join(f"{t['name']}" for _, t in scored)
            return graded_axis(val, "[L]", f"earliest of HPO onset annotations: {terms}",
                source=f"HPO phenotype.hpoa v{HPOA_VERSION} onset annotations (dossier age_of_onset)")
    # fallback: definition onset lexicon -> [H]
    hit = first_match(defn, PATTERNS["O_onset_text"]) if defn else None
    if hit:
        val, label, phrase = hit
        return graded_axis(val, "[H]", f"{label} (definition: '{phrase}')",
            source="cited-text inference over MedGen clinical_definition")
    return graded_axis(None, "[O]", "onset not stated",
        obstacle="age of onset not in HPO annotations or MedGen definition; registry onset (OMIM clinical synopsis) deferred, not guessed")

def score_progression(c_terms, defn, name):
    hpo = [(PROG_VAL[t], t) for t in c_terms if t in PROG_VAL]
    if hpo:
        val = max(v for v, _ in hpo)
        terms = ", ".join(name.get(t, t) for _, t in hpo)
        return graded_axis(val, "[L]", f"HPO clinical-course term(s): {terms}",
            source=f"HPO phenotype.hpoa v{HPOA_VERSION} Clinical-course (aspect C) annotations")
    if defn:
        low = defn.lower()
        # variable-progression spectrum: an explicit range/continuum framing that spans a
        # fast/fatal-progression end AND a slow/mild/normal end. Mirrors the severity-spectrum
        # rule. This pre-empts the tier-1.0 coupling, which otherwise mis-fires when a lethal
        # type and a progressive type are merely co-listed in one sentence (e.g. an umbrella
        # entity that runs perinatal-lethal -> attenuated). Recorded [H], value 0.5.
        prog_word = re.search(r"\bprogress", low)
        spectrum = re.search(r"continuum|ranges?\s+(?:from|over)|range\s+from|spectrum"
                             r"|from\s+[\w-]+[^.]*\bto\b|varying|variabilit", low)
        prog_fast = re.search(r"rapidly\s+progressive|fulminant|aggressive\s+(?:course|progression)"
                             r"|\b(?:fatal|lethal)\b|\bdeath\b|\bdie[sd]?\b|perinatal", low)
        prog_slow = re.search(r"slowly\s+progressive|non-?progressive|\bstatic\b|stable\s+course"
                             r"|attenuated|\bslight\b|normal\s+life|asymptomatic|\bmild\b", low)
        if prog_word and spectrum and prog_fast and prog_slow:
            return graded_axis(0.5, "[H]",
                "variable progression spectrum (fast/fatal-to-slow/mild range stated)",
                source="cited-text inference over MedGen clinical_definition")
    hit = first_match(defn, PATTERNS["P_progression"]) if defn else None
    if hit:
        val, label, phrase = hit
        return graded_axis(val, "[H]", f"{label} (definition: '{phrase}')",
            source="cited-text inference over MedGen clinical_definition")
    return graded_axis(None, "[O]", "progression not stated",
        obstacle="natural-history/progression not in HPO Clinical-course annotations or MedGen definition; registry natural-history (Orphanet) deferred, not guessed")

def score_severity(defn, name):
    if not defn:
        return graded_axis(None, "[O]", "severity not stated",
            obstacle="no MedGen definition; severity descriptor requires a registry source, deferred, not guessed")
    low = defn.lower()
    has_mild = re.search(r"\bmild\b|asymptomatic|benign", low)
    has_high = re.search(r"\bsevere\b|\bprofound\b|devastating|lethal|fatal", low)
    # A genuine within-entity severity range is signalled EITHER by both a mild-end and a high-end
    # descriptor (two ends stated), OR by variability explicitly predicated of THIS entity's
    # severity/phenotype/expression, OR an explicit "from X to Y" / "broad spectrum" range. A bare
    # "continuum"/"spectrum" word is NOT sufficient on its own: it frequently names a PARENT
    # classification (e.g. "ASMD occurs along a continuum" while the entity is its severe pole),
    # which must not be misread as within-entity variability.
    explicit_var = re.search(
        r"variabl[ey]\s+(?:severity|phenotyp|expressi|presentation|clinical|disease)"
        r"|(?:severity|phenotyp|expressi|presentation)[^.]{0,30}\bvariab"
        r"|variabilit\w*[^.]{0,20}(?:severity|phenotyp|expressi|presentation|disease)"
        r"|vary\s+widely|varies\s+widely|wide\s+(?:range|spectrum)\s+of\s+severit"
        r"|ranges?\s+from\s+[\w-]+[^.]*\bto\b"
        r"|broad\s+(?:phenotypic\s+|clinical\s+)?spectrum", low)
    if (has_mild and has_high) or (explicit_var and (has_mild or has_high)):
        return graded_axis(0.5, "[H]", "variable severity spectrum (mild-to-severe range stated)",
            source="cited-text inference over MedGen clinical_definition")
    hit = first_match(defn, PATTERNS["S_severity"])
    if hit:
        val, label, phrase = hit
        return graded_axis(val, "[H]", f"{label} (definition: '{phrase}')",
            source="cited-text inference over MedGen clinical_definition")
    return graded_axis(None, "[O]", "severity not stated",
        obstacle="severity descriptor not in MedGen definition; registry severity (OMIM clinical synopsis) deferred, not guessed")

def mortality_from_text(defn):
    """Classify life-expectancy impact from the cited definition. Returns
    (value, basis_label) or (None, None). Natural-history read: treatment benefit
    is handled separately by R_treat (R4), so untreated lethality is scored here."""
    low = defn.lower()
    LIFE = r"(?:life\s*span|lifespan|life\s+expectancy|survival)"
    sents = re.split(r"(?<=[.])\s+", low)
    range_word = re.search(r"\b(?:range|ranges|ranging|continuum|spectrum|encompass\w*)\b"
                           r"|from\s+[\w-]+[^.]*?\bto\b", low)
    has_lethal_end = re.search(r"lethal|fatal|\bdeath\b|\bdie[sd]?\b|do\s+not\s+survive|perinatal", low)
    has_mild_end = re.search(r"normal\s+life|near-?normal|asymptomatic|\bmild\b|\bslight\b", low)
    real_mortality = re.search(r"cause\s+of\s+(?:morbidity\s+and\s+)?mortality|cause\s+of\s+death|causes?\s+of\s+death", low)
    normal_claim = re.search(rf"\b(?:near[- ]?)?normal\b\s+{LIFE}"
                             rf"|{LIFE}\s+(?:is|are|remains?)?\s*(?:\w+\s+){{0,2}}?(?:near[- ]?)?normal\b"
                             rf"(?!\s+(?:growth|function|development|intelligence|cognition|stature|dentition|psychomotor))",
                             low)
    qualified_risk = re.search(r"(?:increases?\s+the\s+|increased\s+)?risk\s+of\s+death|can\s+be\s+fatal"
                               r"|may\s+be\s+fatal|rarely\s+fatal|predispos\w+\s+to\s+(?:death|fractures)"
                               r"|but\s+(?:can|may)\s+(?:also\s+)?develop[^.]*"
                               r"(?:disease|cancer|failure|cirrhosis|emphysema|copd|carcinoma)", low)

    # 1) explicit phenotypic range from a lethal/severe end to a mild/normal end -> variable spectrum
    if (range_word and has_lethal_end and has_mild_end) or (normal_claim and real_mortality):
        return 0.7, "variable mortality spectrum (lethal/severe-to-normal range stated)"
    # 2) near-normal lifespan with only a qualified complication risk (not a defining mortality)
    if normal_claim and not real_mortality:
        if qualified_risk:
            return 0.4, "near-normal lifespan with qualified mortality risk"
        return 0.0, "normal life expectancy stated"
    # 3) early-life lethality: a death/non-survival token tied to an early-life marker (per sentence)
    EARLY = (r"(?:infan|early\s+child|in\s+child|childhood|perinatal|neonat|in\s+utero|antenatal|"
             r"hydrops\s+fetalis|first\s+(?:year|two\s+years|ten\s+years|decade|few\s+years|months)|"
             r"before\s+age\s+(?:two|three|four|five|six|seven|eight|nine|ten)|"
             r"by\s+age\s+(?:one|two|three|four|five)|less\s+than\s+ten\s+years)")
    DEATH = r"(?:death|die[sd]?|dying|do\s+not\s+survive|stillbirth|perinatal-?lethal|\blethal\b|\bfatal\b)"
    for s in sents:
        if (re.search(rf"{DEATH}[^.]*{EARLY}", s) or re.search(rf"{EARLY}[^.]*{DEATH}", s)
                or re.search(r"perinatal-?lethal|incompatible\s+with\s+life|\bstillbirth\b", s)
                or re.search(rf"{LIFE}[^.]{{0,30}}(?:less\s+than\s+ten\s+years|first\s+decade)", s)):
            return 1.0, "early-life lethality stated"
    # 4) severely reduced / premature adult survival
    if re.search(rf"(?:reduced|shortened|decreased|poor|limited|diminished)\s+{LIFE}"
                 rf"|{LIFE}[^.]{{0,25}}(?:reduced|shortened|decreased|limited)"
                 r"|premature\s+death|die\s+prematurely|early\s+(?:death|mortality)"
                 r"|few\s+survive|do\s+not\s+survive\s+beyond"
                 r"|survive\s+(?:into|beyond|to)\s+(?:the\s+)?(?:third|fourth|fifth)\s+decade"
                 r"|(?:age\s+of\s+death|death)\s+(?:is\s+)?in\s+the\s+(?:mid-?|late\s+|early\s+)?(?:forties|fifties|thirties)", low):
        return 0.7, "severely reduced / premature survival stated"
    # 5) disease-defining mortality with no stated timing
    if real_mortality or re.search(r"\bfatal\b|\blethal\b", low):
        return 0.7, "disease-related mortality stated (timing unspecified)"
    return None, None

def score_mortality(m_terms, defn, name):
    hpo = [(MORT_VAL[t], t) for t in m_terms if t in MORT_VAL]
    hpo_val = max((v for v, _ in hpo), default=None)
    hpo_terms = ", ".join(name.get(t, t) for _, t in hpo) if hpo else None
    tval, tlabel = mortality_from_text(defn) if defn else (None, None)
    # An explicit lifespan-bounding statement in the definition (normal / qualified-risk / variable
    # spectrum) refines a coarse HPO mortality flag: HPO Mortality/Aging annotations encode phenotype
    # PRESENCE (often at low/uncertain frequency, e.g. "Death in infancy" 1/1), not lifespan MAGNITUDE.
    bounding = tlabel is not None and ("spectrum" in tlabel or "qualified" in tlabel
                                       or "normal life expectancy" in tlabel)
    if hpo_val is not None and bounding:
        return graded_axis(tval, "[H]",
            f"{tlabel}; refines HPO Mortality term(s) [{hpo_terms}] (presence flag, not lifespan magnitude)",
            source=f"cited-text inference over MedGen clinical_definition; HPO phenotype.hpoa v{HPOA_VERSION} corroborates presence")
    if hpo_val is not None:
        return graded_axis(hpo_val, "[L]", f"HPO Mortality/Aging term(s): {hpo_terms}",
            source=f"HPO phenotype.hpoa v{HPOA_VERSION} Mortality/Aging annotations")
    if not defn:
        return graded_axis(None, "[O]", "survival not stated",
            obstacle="no MedGen definition; survival data requires a registry source, deferred, not guessed")
    if tval is not None:
        return graded_axis(tval, "[H]", tlabel,
            source="cited-text inference over MedGen clinical_definition")
    return graded_axis(None, "[O]", "survival not stated",
        obstacle="life-expectancy impact not in HPO Mortality/Aging annotations or MedGen definition; survival literature deferred, not guessed")

def score_disability(defn, name):
    hit = first_match(defn, PATTERNS["D_disability"]) if defn else None
    if hit:
        val, label, phrase = hit
        return graded_axis(val, "[H]", f"{label} (definition: '{phrase}')",
            source="cited-text inference over MedGen clinical_definition")
    return graded_axis(None, "[O]", "functional status not stated",
        obstacle="functional/disability status not in MedGen definition; functional registry (Orphanet) deferred, not guessed")

# ----------------------------------------------------------------------------- #
# developmental/morphogenesis baseline links (optional, ROADMAP R3) -> [H]
#   which emergence-engine quantity the disease perturbs. Mechanistic mapping;
#   basis recorded; engine itself is the pinned read-only baseline (code/emergence_v2).
# ----------------------------------------------------------------------------- #
EMERGENCE = {
    "C0001080": ("achondroplasia",  # FGFR3 GoF -> growth-plate / length-scale lambda
        "FGFR3 constitutive activation suppresses chondrocyte proliferation at the growth plate; "
        "perturbs the morphogen length scale lambda = sqrt(D*tau) governing long-bone elongation"),
    "C0220685": ("achondrogenesis type II",  # COL2A1 -> cartilage matrix
        "COL2A1 loss disrupts cartilage extracellular-matrix assembly; perturbs the diffusion term D "
        "in the morphogen length scale lambda = sqrt(D*tau) for skeletal anlage"),
    "C0029434": ("osteogenesis imperfecta",  # COL1A1/2 -> bone matrix mechanics
        "COL1A1/COL1A2 defects alter type-I collagen matrix stiffness; perturbs the mechanical "
        "Layer-2 substrate on which the morphogenetic length scale acts"),
    "C0024796": ("marfan syndrome",  # FBN1 -> microfibril / TGF-beta
        "FBN1 microfibril defect dysregulates TGF-beta sequestration; perturbs the morphogen "
        "effective decay time tau in lambda = sqrt(D*tau) for connective-tissue patterning"),
    "C0268335": ("ehlers-danlos classic",  # COL5A1 -> collagen fibrillogenesis
        "COL5A1/COL1A1 defects impair collagen fibril nucleation; perturbs matrix diffusion D in the "
        "morphogenetic length scale for dermal/connective patterning"),
    "C0268338": ("ehlers-danlos type 4",  # COL3A1 -> vascular collagen
        "COL3A1 loss weakens type-III collagen in vessel/organ walls; perturbs the mechanical substrate "
        "term of the morphogenetic baseline"),
}

# ----------------------------------------------------------------------------- #
# Spearman rank correlation (no scipy dependency)
# ----------------------------------------------------------------------------- #
def rank(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = rank(a), rank(b)
    n = len(a)
    if n < 2:
        return 1.0
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    va = sum((x - ma) ** 2 for x in ra) ** 0.5
    vb = sum((x - mb) ** 2 for x in rb) ** 0.5
    return round(cov / (va * vb), 4) if va and vb else 1.0

def weighted_burden(axes, weights):
    """mean of present axis values under given weights (renormalised)."""
    num = den = 0.0
    for k, w in weights.items():
        ax = axes[k]
        if ax["value"] is not None:
            num += w * ax["value"]
            den += w
    return (num / den) if den else None

# ----------------------------------------------------------------------------- #
def write_lexicon_doc():
    lines = ["# BURDEN_LEXICON — declared clinical-definition inference rules (R3)",
             "",
             "*Generated from `code/pipeline/r3_burden_index.py` `PATTERNS` — the single source of",
             "truth. Do not hand-edit; re-run the builder to regenerate.*",
             "",
             "Every value produced by these rules is graded **[H]** (inference from the cited MedGen",
             "`clinical_definition`, an observed [L] source); the matched phrase is recorded per row as",
             "the basis. A registry HPO annotation, where present, overrides the lexicon and is graded",
             "**[L]**. Where neither fires, the axis is **[O]** with a named obstacle (never guessed).",
             "",
             "Tiers are scanned in listed order; the first matching tier wins, except for the explicit",
             "overrides noted below each table.",
             ""]
    titles = {
        "P_progression": "P — progression (static 0.2 · slow 0.5 · rapid 0.8 · lethal-progressive 1.0)",
        "S_severity": "S — symptom/pain severity (mild 0.25 · moderate 0.5 · severe 0.75 · profound 1.0)",
        "M_mortality": "M — mortality (normal 0.0 · qualified-risk/near-normal 0.4 · severe-or-spectrum 0.7 · early-lethal 1.0)",
        "D_disability": "D — functional disability (independent 0.2 · partial 0.5 · high 0.75 · dependent 1.0)",
        "O_onset_text": "O — onset (fallback only; HPO onset annotation preferred and graded [L])",
    }
    overrides = {
        "S_severity": "Override: if the definition states BOTH a mild and a severe/lethal descriptor, or a "
                      "`variable/spectrum/continuum/ranges from` phrase together with either, severity = 0.5 "
                      "(variable spectrum) rather than an extreme.",
    }
    # mortality is not a flat first-match table — describe its sentence-level classifier as prose
    M_PROSE = [
        "Mortality is classified by `mortality_from_text()` (not a flat first-match table), because "
        "life-expectancy statements in the definitions are order-dependent and frequently describe a "
        "*range* rather than a single value. Natural-history read: treatment benefit is scored "
        "separately by `R_treat` (Phase R4), so an untreated lethal course is scored here even when the "
        "same definition also reports treated survival. Rules, in order:",
        "",
        "1. **Variable spectrum -> 0.7.** An explicit range word (`range`/`ranges`/`continuum`/`spectrum`/"
        "`from X to Y`) spanning a lethal/severe end and a mild/normal end, OR a `(near-)normal lifespan` "
        "claim co-stated with a disease-defining `cause of (morbidity and) mortality`. Captures umbrella "
        "entities (e.g. perinatal-lethal-to-asymptomatic) without pinning them to either extreme.",
        "2. **Near-normal with qualified risk -> 0.4 / normal -> 0.0.** A `(near-)normal lifespan` claim "
        "with NO disease-defining mortality: if only a *qualified* complication risk is present "
        "(`risk of death`, `can/may be fatal`, `predisposition`) -> 0.4; otherwise -> 0.0. This stops an "
        "isolated `risk of death in infancy` from over-stating a near-normal-lifespan disease.",
        "3. **Early-life lethality -> 1.0.** Per sentence, a death/non-survival token (`death`, `die`, "
        "`do not survive`, `stillbirth`, `perinatal-lethal`, `lethal`, `fatal`) within the same sentence "
        "as an early-life marker (`infancy`, `childhood`, `neonatal`, `perinatal`, `in utero`, "
        "`hydrops fetalis`, `first N years/decade of life`, `before age <=ten>`), or a bare "
        "`perinatal-lethal`/`incompatible with life`/`stillbirth`, or a `lifespan ... less than ten "
        "years / first decade` phrase.",
        "4. **Severely reduced / premature adult survival -> 0.7.** `reduced/shortened/decreased/limited "
        "lifespan|survival`, `premature death`, `early death/mortality`, `few survive`, `survive into the "
        "third/fourth/fifth decade`, `age of death in the forties/fifties/thirties`.",
        "5. **Disease-defining mortality, timing unspecified -> 0.7.** A `cause of mortality/death` phrase "
        "or a bare `fatal`/`lethal` with no other timing signal.",
        "",
        "Where none fire, M is **[O]** (survival not stated; registry survival source deferred, not guessed).",
    ]
    for axis, tiers in PATTERNS.items():
        lines.append(f"## {titles[axis]}")
        lines.append("")
        if axis == "M_mortality":
            lines.extend(M_PROSE)
            lines.append("")
            continue
        lines.append("| value | basis label | patterns (regex, case-insensitive) |")
        lines.append("|---|---|---|")
        for value, label, pats in tiers:
            pat_txt = " · ".join(f"`{p}`" for p in pats)
            lines.append(f"| {value} | {label} | {pat_txt} |")
        if axis in overrides:
            lines.append("")
            lines.append(overrides[axis])
        lines.append("")
    open(OUT_LEX, "w").write("\n".join(lines))

# ----------------------------------------------------------------------------- #
def main():
    name, parents, children = load_obo()
    hpoa = load_hpoa()
    MORT_SET = subtree("HP:0040006", children)

    files = sorted(f for f in os.listdir(DOSS) if f.endswith(".json") and f != "_cohort_index.json")
    records = []
    for fn in files:
        d = json.load(open(os.path.join(DOSS, fn), encoding="utf-8"))
        ident = d["identity"]
        cui = ident["medgen_cui"]
        omims = ident["omim_codes"]
        defn = (d["clinical"]["clinical_definition"]["value"] or "")

        anns = [a for o in omims for a in hpoa.get(o, [])]
        c_terms = {a["hpo_id"] for a in anns if a["aspect"] == "C"}
        m_terms = {a["hpo_id"] for a in anns if a["hpo_id"] in MORT_SET}

        axes = {
            "O": score_onset(d, defn, name),
            "P": score_progression(c_terms, defn, name),
            "S": score_severity(defn, name),
            "M": score_mortality(m_terms, defn, name),
            "D": score_disability(defn, name),
        }
        present = [k for k in W if axes[k]["value"] is not None]
        axes_scored = len(present)
        rankable = axes_scored >= RANK_MIN_AXES

        raw_burden = weighted_burden(axes, W)
        grade_floor = floor_grade([axes[k]["grade"] for k in W])           # any [O] -> [O]
        grade_present = floor_grade([axes[k]["grade"] for k in present]) if present else "[O]"

        # treatability deferred to R4
        R_treat = {"value": 1.0, "grade": "[O]",
                   "basis": "no treatability offset applied (e = 0); R4 treatments.csv not yet built",
                   "obstacle": "treatability offset deferred to Phase R4 (treatments.csv); raw_burden is the pre-treatment burden"}
        burden_score = raw_burden  # * R_treat.value (==1.0)
        burden_grade = "[O]"       # floors to [O] because R_treat is [O]

        emr = EMERGENCE.get(cui)
        emergence_link = None
        if emr:
            emergence_link = {"value": emr[1], "grade": "[H]",
                              "basis": "developmental/morphogenesis mechanism mapped to the emergence baseline",
                              "source": "code/emergence_v2/ (pinned read-only baseline; morphogen_lengths.json, param_db.json)"}

        records.append({
            "entity": ident["entity"], "cui": cui, "tier": ident["tier"],
            "system_class": ident["system_class"], "genes": ident["genes"],
            "omim_codes": omims, "slug": fn[:-5],
            "axes": axes, "axes_scored": axes_scored, "rankable": rankable,
            "axes_present": present, "axes_missing": [k for k in W if k not in present],
            "raw_burden": raw_burden, "raw_burden_grade_floor": grade_floor,
            "raw_burden_grade_present": grade_present,
            "treatability": R_treat, "burden_score": burden_score, "burden_score_grade": burden_grade,
            "emergence_link": emergence_link,
        })

    # ---- primary ranking: only MAJORITY-COVERAGE diseases (>=3 axes) are placed in the order ----
    # rankable: raw_burden desc, then more-complete first, then name -> sequential ranks 1..N.
    # not-placed (1-2 axes): rank = null; ordered after, by axes_scored desc then name, for display.
    rankable = sorted([r for r in records if r["rankable"]],
                      key=lambda r: (-(r["raw_burden"] if r["raw_burden"] is not None else -1),
                                     -r["axes_scored"], r["entity"]))
    not_placed = sorted([r for r in records if not r["rankable"]],
                        key=lambda r: (-r["axes_scored"], r["entity"]))
    for i, r in enumerate(rankable, 1):
        r["rank"] = i
    for r in not_placed:
        r["rank"] = None
    records = rankable + not_placed

    # ---- sensitivity: alternative weightings vs default (Spearman over the PLACED order) ----
    default_vals = [r["raw_burden"] if r["raw_burden"] is not None else 0.0 for r in rankable]
    alt_weightings = {
        "equal_default": W,
        "onset_heavy":   {"O": 0.40, "P": 0.15, "S": 0.15, "M": 0.15, "D": 0.15},
        "mortality_heavy": {"O": 0.15, "P": 0.15, "S": 0.15, "M": 0.40, "D": 0.15},
        "severity_heavy": {"O": 0.15, "P": 0.15, "S": 0.40, "M": 0.15, "D": 0.15},
        "drop_disability_core4": {"O": 0.25, "P": 0.25, "S": 0.25, "M": 0.25, "D": 0.0},
    }
    sensitivity = {}
    for label, ww in alt_weightings.items():
        vals = [weighted_burden(r["axes"], ww) or 0.0 for r in rankable]
        sensitivity[label] = {"weights": ww, "spearman_vs_default": spearman(default_vals, vals)}

    # ---- CSV (flat, gate- and human-readable) ----
    cols = ["rank", "rankable", "entity", "cui", "tier", "system_class",
            "O_value", "O_grade", "P_value", "P_grade", "S_value", "S_grade",
            "M_value", "M_grade", "D_value", "D_grade",
            "axes_scored", "raw_burden", "raw_burden_grade_floor", "raw_burden_grade_present",
            "R_treat", "R_treat_grade", "burden_score", "burden_score_grade",
            "emergence_link"]
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in records:
            ax = r["axes"]
            def cell(v):
                return "" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)
            w.writerow([
                cell(r["rank"]), "yes" if r["rankable"] else "no",
                r["entity"], r["cui"], r["tier"], r["system_class"],
                cell(ax["O"]["value"]), ax["O"]["grade"], cell(ax["P"]["value"]), ax["P"]["grade"],
                cell(ax["S"]["value"]), ax["S"]["grade"], cell(ax["M"]["value"]), ax["M"]["grade"],
                cell(ax["D"]["value"]), ax["D"]["grade"],
                r["axes_scored"], cell(r["raw_burden"]),
                r["raw_burden_grade_floor"], r["raw_burden_grade_present"],
                cell(r["treatability"]["value"]), r["treatability"]["grade"],
                cell(r["burden_score"]), r["burden_score_grade"],
                "yes" if r["emergence_link"] else "",
            ])

    # ---- JSON (full provenance) ----
    payload = {
        "schema": "disease_wp.burden_scores/v1",
        "phase": "R3", "investigation_only": True, "generated": RETRIEVED,
        "method": "methodology/BURDEN_INDEX.md + methodology/BURDEN_LEXICON.md",
        "weights_default": W,
        "composite_rule": "raw_burden = mean of present axis values (renormalised); missing axis excluded, not imputed",
        "floor_rule": "raw_burden grade = min over 5 axis grades (O<H<L<V; any missing axis -> [O]); grade_present = floor over scored axes only",
        "treatability": "R_treat = 1 - e; e from R4 treatments.csv (not yet built) so R_treat = 1.0, [O]; primary ordering on raw_burden (pre-treatment)",
        "ranking_basis": "raw_burden desc, axes_scored desc, entity asc; only rankable (>=3 axes) placed",
        "rankability": {
            "min_axes": RANK_MIN_AXES,
            "rule": "rankable = axes_scored >= %d (majority of 5). Only rankable diseases are placed "
                    "in the ordered suffering-order; diseases with fewer scored axes are reported with "
                    "rank = null under 'not placed - insufficient axis coverage'." % RANK_MIN_AXES,
            "rationale": "raw_burden is a renormalised mean over scored axes; a mean over <3 of 5 axes "
                         "is not a meaningful aggregate and would let a single-axis disease crowd the top "
                         "of the order. One fixed declared threshold, not a tuned cut.",
            "placed": sum(1 for r in records if r["rankable"]),
            "not_placed": sum(1 for r in records if not r["rankable"]),
        },
        "cohort_size": len(records),
        "sensitivity": sensitivity,
        "axis_grade_coverage": {
            k: dict(collections.Counter(r["axes"][k]["grade"] for r in records)) for k in W
        },
        "records": [{
            "rank": r["rank"], "entity": r["entity"], "cui": r["cui"], "tier": r["tier"],
            "system_class": r["system_class"], "genes": r["genes"], "omim_codes": r["omim_codes"],
            "components": r["axes"],
            "axes_scored": r["axes_scored"], "rankable": r["rankable"],
            "axes_missing": r["axes_missing"],
            "raw_burden": r["raw_burden"],
            "raw_burden_grade_floor": r["raw_burden_grade_floor"],
            "raw_burden_grade_present": r["raw_burden_grade_present"],
            "treatability": r["treatability"],
            "burden_score": r["burden_score"], "burden_score_grade": r["burden_score_grade"],
            "emergence_link": r["emergence_link"],
        } for r in records],
        "grade_vocabulary": {
            "[L]": "registry-stated and cited (HPO annotation; observed input)",
            "[H]": "inference from the cited MedGen clinical_definition; matched phrase recorded as basis",
            "[V]": "derived from a quantitative published distribution (reserved; none used in R3)",
            "[O]": "open/unavailable; obstacle named; not guessed",
        },
    }
    json.dump(payload, open(OUT_JSON, "w"), indent=2, ensure_ascii=False)

    write_lexicon_doc()

    # ---- report ----
    print("--- R3 burden index built ---")
    print(f"  cohort: {len(records)}  ->  {os.path.relpath(OUT_CSV, ROOT)}")
    print("\n  axis grade coverage (over 35 diseases):")
    for k in W:
        print(f"    {k}: {dict(collections.Counter(r['axes'][k]['grade'] for r in records))}")
    print("\n  RANKING (raw_burden, pre-treatment; floor/present grades):")
    print(f"    {'#':>2} {'disease':40s} {'raw':>5s} {'flr':>4s} {'prs':>4s} {'ax':>2s}  O   P   S   M   D")
    def s(v): return f"{v:.2f}" if v is not None else "  · "
    placed = [r for r in records if r["rankable"]]
    unplaced = [r for r in records if not r["rankable"]]
    for r in placed:
        ax = r["axes"]
        rb = f"{r['raw_burden']:.3f}" if r["raw_burden"] is not None else "  ·  "
        print(f"    {r['rank']:2d} {r['entity'][:40]:40s} "
              f"{rb} {r['raw_burden_grade_floor']:>4s} {r['raw_burden_grade_present']:>4s} "
              f"{r['axes_scored']:2d}  {s(ax['O']['value'])} {s(ax['P']['value'])} {s(ax['S']['value'])} "
              f"{s(ax['M']['value'])} {s(ax['D']['value'])}")
    if unplaced:
        print(f"\n  NOT PLACED - insufficient axis coverage (<{RANK_MIN_AXES} of 5 axes; rank = null):")
        for r in unplaced:
            ax = r["axes"]
            rb = f"{r['raw_burden']:.3f}" if r["raw_burden"] is not None else "  ·  "
            print(f"     · {r['entity'][:40]:40s} "
                  f"{rb}  {'':>4s} {r['raw_burden_grade_present']:>4s} "
                  f"{r['axes_scored']:2d}  {s(ax['O']['value'])} {s(ax['P']['value'])} {s(ax['S']['value'])} "
                  f"{s(ax['M']['value'])} {s(ax['D']['value'])}")
    print("\n  sensitivity (Spearman rho of raw_burden ranking vs equal-weight default):")
    for label, sd in sensitivity.items():
        print(f"    {label:24s} rho = {sd['spearman_vs_default']}")

    # determinism digest over the two data artifacts (date-stamped, see note)
    h = hashlib.sha256()
    for p in (OUT_CSV, OUT_JSON):
        h.update(open(p, "rb").read())
    print(f"\n  burden-set sha256[:12]: {h.hexdigest()[:12]}")

if __name__ == "__main__":
    main()
