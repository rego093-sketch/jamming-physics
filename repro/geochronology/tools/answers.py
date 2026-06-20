# -*- coding: utf-8 -*-
"""Authored answer-first blocks (VP-SPEC v1.8 §6-R.3) for geochronology.

Each value is a self-contained direct answer (entity + value/conclusion +
grade), 40-60 words, derived faithfully from that section's locked abstract/
body. Anti-writing invariant (§6-D.6 / §8): every numeric token here also
appears in that section's body — verified mechanically by vp_v18_gate.py.

These are gate-excluded metadata (like .abstract); injecting them does not
change body word count.
"""

# slug -> answer-first text (plain unicode; no eq-inline class, no figure/table)
ANSWER = {
"01-scope-premise":
 "This paper addresses sample-level dating accuracy, not whether decay clocks are "
 "correct. Laboratory-measured decay constants (A = \u03bbN) are environment-"
 "independent \u2014 Oklo and SN\u00a01987A bound fine-structure drift below 10\u207b\u2077 "
 "over two billion years. Accuracy is therefore set by event attribution and open-"
 "system exchange, not by the decay physics.",

"02-two-axes-dating-accuracy":
 "Every radiometric age splits into two independent axes: internal integrity (the "
 "clock) and event attribution (the sample). U\u2013Pb adds a self-check radiocarbon "
 "lacks \u2014 \u00b2\u00b3\u2078U\u2192\u00b2\u2070\u2076Pb and \u00b2\u00b3\u2075U\u2192\u00b2\u2070\u2077Pb must be concordant. Essentially all "
 "accuracy risk lies on the attribution axis: an interpretive and geochemical "
 "limit, not a precision one.",

"03-one-contamination-mechanism-two-detectabilities":
 "The dominant attribution failure is identical on both clocks: foreign older "
 "material in \u21d2 measured age biased old (radiocarbon reservoir / dead-carbon; "
 "zircon inheritance). They differ only in detectability \u2014 atomically homogeneous "
 "and self-concealing in radiocarbon, granular and separable in zircon. Daughter "
 "loss biases the other way, so screening must guard both directions.",

"04-shared-physics-closure-exchange-number":
 "Both clocks share one dimensionless group: the diffusion (Fourier) number "
 "N_D = D\u03c4/L\u00b2 \u2261 Fo. Dodson\u2019s closure temperature carries the same grouping "
 "A\u03c4D\u2080/a\u00b2 inside its logarithm, so a frozen system exchanging with a reservoir "
 "is formally the closure-temperature problem. The radiocarbon reservoir effect, "
 "isotopic closure and zircon retention are one physics, not an analogy.",

"05-unified-protocol":
 "One protocol runs on both clocks: screen \u2192 classify \u2192 correct-where-"
 "characterisable \u2192 cross-check \u2192 report honest uncertainty. The decisive move is "
 "Step\u00a02 for zircon \u2014 grains are classified on age-independent grounds (crystal "
 "position, texture, common-Pb f\u2082\u2080\u2086), never by picking the youngest age \u2014 which "
 "keeps the procedure non-circular. Radiocarbon implements the same steps via an "
 "external \u0394R offset.",

"06-demonstration-i-radiocarbon-homogeneous-case":
 "Leave-one-out cross-validation tests the reservoir correction out-of-sample on "
 "independently constrained radiocarbon pairs. On Elk Hills shell\u2013charcoal it cut "
 "RMSE 418 \u2192 141 yr (66%); on Lake Chichancanab leaf-wax / macrofossil pairs, "
 "739 \u2192 453 yr (39%). The smaller gain is the point: it flags the locality-"
 "dependent transferability that the protocol is designed to report.",

"07-demonstration-ii-zircon-u-pb":
 "Applied to the Lava Creek Tuff zircon dataset, the protocol splits grains by "
 "crystal position: faces give 626.5 \u00b1 2.9 ka, cores 668.8 \u00b1 3.2 ka. Faces "
 "reproduce the published rim age exactly and agree with two independent anchors "
 "(~631 ka eruption; MIS tephra ~630 ka) at the ~1% level; pooling biases the "
 "eruption age ~42 ka old.",

"08-demonstration-iii-zircon-u-pb":
 "On fully open IsoplotR datasets the screening steps run end-to-end. A \u00b2\u2070\u2074Pb-"
 "bearing suite is 67% discordant before correction (\u00b2\u2070\u2076Pb/\u00b2\u00b3\u2078U ~429 Ma vs "
 "\u00b2\u2070\u2077Pb/\u00b2\u00b3\u2075U ~1300 Ma) and concordant at ~312 Ma after a Stacey\u2013Kramers "
 "common-Pb correction; a clean suite sits at ~249 Ma untouched. A detrital "
 "population spanning ~129\u20132994 Ma yields only a maximum depositional age.",

"09-documented-cases-mechanism-real-chronologies":
 "The mechanism is the documented cause of named errors on both clocks, in both "
 "directions \u2014 none of them clock (Axis-A) failures. Older bias: living Nevada "
 "snails at ~27 ka; Bishop Tuff cores ~850\u2013892 ka vs ~767 ka eruption. Younger "
 "bias: Vindija bone climbing ~29 \u2192 32 \u2192 >48 ka. Each is fixed by an age-"
 "independent screen.",

"10-mitigation-strategies-current-practice":
 "Existing decontamination methods are unified, not replaced: each performs the same two "
 "moves \u2014 isolate the foreign component on age-independent grounds, then validate "
 "out-of-sample. Radiocarbon climbs ABA \u2192 ABOX-SC \u2192 ultrafiltration \u2192 "
 "hydroxyproline AMS; zircon climbs air abrasion \u2192 CA-ID-TIMS, CL-guided dating, "
 "\u00b2\u2070\u2074Pb common-Pb, concordance. Every rung has a stated ceiling; none converts an "
 "Axis-B problem into an Axis-A guarantee.",

"11-working-range-honest-limits":
 "U\u2013Pb has a working range like any measurement: at the young end, trace common Pb "
 "dominates; at the old end, \u00b2\u00b3\u2075U falls to ~1.3% by ~4.4 Ga. The deeper limit is "
 "epistemic \u2014 radiocarbon is checked against dendrochronology to 12,593 yr, but "
 "deep-time U\u2013Pb cannot be checked against any written record; its accuracy rests "
 "on consilience.",

"12-grading-attribution-severity-test-strength":
 "Grade a result not by its age or its \u00b1, but on one axis: what age-independent "
 "test would have failed had the attribution been wrong, and was it run? The scale "
 "runs A1 (reproduces an independent reference age) to A4 (untested and "
 "incentivised). Lava Creek 626 vs 658.8 \u00b1 6.6 ka shows selection alone moving the "
 "answer 32 kyr older.",

"13-validation-methodology":
 "Three rules govern the framework. Primary validation uses independently confirmed "
 "reference ages, not ages from the same model. Corrections are tested out-of-sample "
 "by leave-one-out, since a fit that only improves its own points is a curve fit, "
 "not a clock. Every claim is tagged [F]/[I]/[A], so confirmed facts are never "
 "merged with inference or assumption.",

"14-conclusion":
 "Neither clock is in question. Their shared bottleneck is foreign older material in "
 "\u21d2 age biased old, differing only in detectability (hidden in radiocarbon, "
 "separable in zircon), and both yield to one protocol: classify on age-independent "
 "grounds, validate out-of-sample. Demonstrated on radiocarbon pairs, Lava "
 "Creek, and open zircon data, it recovers correct ages where material permits.",
}

HUB_ANSWER = (
 "Radiocarbon and zircon U\u2013Pb are accepted clocks; their shared accuracy limit is "
 "sample-level: incorporating foreign older material biases ages old. The two "
 "differ only in detectability \u2014 homogeneous and hidden in radiocarbon, granular "
 "and separable in zircon. One protocol meets both: classify on age-independent "
 "grounds, then validate out-of-sample."
)

# ---- vp-card registry (§6-R.2): locked quantity N_D = D\u03c4/L\u00b2 \u2261 Fo, derived in \u00a74.
# Pages that USE the shared-physics result downstream carry a self-contained card.
FO_CARD = (
 '<aside class="vp-card" data-locked="fo">'
 '<b>N_D = D\u03c4/L\u00b2 \u2261 Fo</b> \u2014 the diffusion (Fourier) number: a characteristic '
 'diffusion length over system size, the dimensionless group that also sits inside '
 'Dodson\u2019s closure temperature. <b>[I]</b> inferential. '
 '<a href="/geochronology/04-shared-physics-closure-exchange-number/#fo">'
 'Canonical derivation \u00a74</a></aside>'
)
# slugs that invoke the matrix-exchange / diffusion-number screening from \u00a74
FO_CARD_ON = {"05-unified-protocol", "06-demonstration-i-radiocarbon-homogeneous-case"}
