# BURDEN_LEXICON — declared clinical-definition inference rules (R3)

*Generated from `code/pipeline/r3_burden_index.py` `PATTERNS` — the single source of
truth. Do not hand-edit; re-run the builder to regenerate.*

Every value produced by these rules is graded **[H]** (inference from the cited MedGen
`clinical_definition`, an observed [L] source); the matched phrase is recorded per row as
the basis. A registry HPO annotation, where present, overrides the lexicon and is graded
**[L]**. Where neither fires, the axis is **[O]** with a named obstacle (never guessed).

Tiers are scanned in listed order; the first matching tier wins, except for the explicit
overrides noted below each table.

## P — progression (static 0.2 · slow 0.5 · rapid 0.8 · lethal-progressive 1.0)

| value | basis label | patterns (regex, case-insensitive) |
|---|---|---|
| 1.0 | progressive course with fatal outcome | `progressive[^.]*\b(?:fatal|lethal|death|demise|terminal)\b` · `\b(?:fatal|lethal|death|demise|terminal)\b[^.]*progressive` · `progressive\s+neurodegenerat` |
| 0.8 | rapidly progressive | `rapidly\s+progressive` · `rapid(?:ly)?\s+(?:deterioration|decline|progression)` · `fulminant` · `aggressive\s+(?:course|progression)` |
| 0.5 | progressive course | `slowly\s+progressive` · `\bprogressive\b` · `gradual(?:ly)?\s+(?:decline|deterioration|progression)` · `insidious` · `chronic[^.]*progress` |
| 0.2 | non-progressive / static course | `non-?progressive` · `\bstatic\b` · `does\s+not\s+progress` · `stable\s+course` |

## S — symptom/pain severity (mild 0.25 · moderate 0.5 · severe 0.75 · profound 1.0)

| value | basis label | patterns (regex, case-insensitive) |
|---|---|---|
| 1.0 | profound / devastating severity | `\bprofound\b` · `devastating` · `most\s+severe` · `extremely\s+severe` · `uniformly\s+(?:fatal|lethal)` |
| 0.75 | severe / debilitating | `(?<!more )(?<!most )(?<!other )(?<!less )\bsevere\b` · `debilitating` · `life-?threatening` · `disabling` · `significant\s+morbidity` · `serious` |
| 0.5 | moderate | `\bmoderate\b` |
| 0.25 | mild / asymptomatic | `\bmild\b` · `benign\s+(?:course|condition)` · `asymptomatic` |

Override: if the definition states BOTH a mild and a severe/lethal descriptor, or a `variable/spectrum/continuum/ranges from` phrase together with either, severity = 0.5 (variable spectrum) rather than an extreme.

## M — mortality (normal 0.0 · qualified-risk/near-normal 0.4 · severe-or-spectrum 0.7 · early-lethal 1.0)

Mortality is classified by `mortality_from_text()` (not a flat first-match table), because life-expectancy statements in the definitions are order-dependent and frequently describe a *range* rather than a single value. Natural-history read: treatment benefit is scored separately by `R_treat` (Phase R4), so an untreated lethal course is scored here even when the same definition also reports treated survival. Rules, in order:

1. **Variable spectrum -> 0.7.** An explicit range word (`range`/`ranges`/`continuum`/`spectrum`/`from X to Y`) spanning a lethal/severe end and a mild/normal end, OR a `(near-)normal lifespan` claim co-stated with a disease-defining `cause of (morbidity and) mortality`. Captures umbrella entities (e.g. perinatal-lethal-to-asymptomatic) without pinning them to either extreme.
2. **Near-normal with qualified risk -> 0.4 / normal -> 0.0.** A `(near-)normal lifespan` claim with NO disease-defining mortality: if only a *qualified* complication risk is present (`risk of death`, `can/may be fatal`, `predisposition`) -> 0.4; otherwise -> 0.0. This stops an isolated `risk of death in infancy` from over-stating a near-normal-lifespan disease.
3. **Early-life lethality -> 1.0.** Per sentence, a death/non-survival token (`death`, `die`, `do not survive`, `stillbirth`, `perinatal-lethal`, `lethal`, `fatal`) within the same sentence as an early-life marker (`infancy`, `childhood`, `neonatal`, `perinatal`, `in utero`, `hydrops fetalis`, `first N years/decade of life`, `before age <=ten>`), or a bare `perinatal-lethal`/`incompatible with life`/`stillbirth`, or a `lifespan ... less than ten years / first decade` phrase.
4. **Severely reduced / premature adult survival -> 0.7.** `reduced/shortened/decreased/limited lifespan|survival`, `premature death`, `early death/mortality`, `few survive`, `survive into the third/fourth/fifth decade`, `age of death in the forties/fifties/thirties`.
5. **Disease-defining mortality, timing unspecified -> 0.7.** A `cause of mortality/death` phrase or a bare `fatal`/`lethal` with no other timing signal.

Where none fire, M is **[O]** (survival not stated; registry survival source deferred, not guessed).

## D — functional disability (independent 0.2 · partial 0.5 · high 0.75 · dependent 1.0)

| value | basis label | patterns (regex, case-insensitive) |
|---|---|---|
| 1.0 | fully dependent | `bedridden` · `fully\s+dependent` · `complete(?:ly)?\s+dependent` · `vegetative` · `total\s+care` |
| 0.75 | high support need | `wheelchair` · `loss\s+of\s+(?:independent\s+)?ambulation` · `unable\s+to\s+walk` · `non-?ambulatory` · `requires?\s+(?:assistance|ventilation|ventilator|support)` · `intellectual\s+disability` · `severe\s+(?:developmental|cognitive|intellectual|motor)\s+(?:delay|disability|impairment)` |
| 0.5 | partial support need | `developmental\s+delay` · `(?:learning|cognitive)\s+(?:difficult|impair|disabilit)` · `mobility\s+(?:impair|limit)` · `motor\s+(?:delay|impair)` · `\bdisabilit` |
| 0.2 | functionally independent | `normal\s+(?:development|intelligence|cognition|psychomotor)` · `\bindependent\b` |

## O — onset (fallback only; HPO onset annotation preferred and graded [L])

| value | basis label | patterns (regex, case-insensitive) |
|---|---|---|
| 1.0 | congenital / neonatal onset | `congenital` · `at\s+birth` · `neonat\w*` · `prenatal` · `in\s+utero` · `antenatal` · `perinatal` |
| 0.85 | infantile onset | `infanc\w*` · `infantile` · `first\s+(?:year|months)\s+of\s+life` · `early\s+infancy` |
| 0.7 | childhood onset | `childhood` · `in\s+children` · `\bchildren\b` · `early\s+childhood` · `pediatric` · `paediatric` · `early[ -]onset` · `first\s+\w+\s+decades?\s+of\s+life` |
| 0.55 | juvenile / adolescent onset | `juvenile` · `adolescen` |
| 0.35 | adult onset | `adulthood` · `\badult\b` · `(?:second|third|fourth)\s+decade` · `middle\s+age` |
| 0.2 | late-adult onset | `late\s+onset` · `late\s+adulthood` · `elderly` · `older\s+adults` |
