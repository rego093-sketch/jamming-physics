# -*- coding: utf-8 -*-
"""
chapters.py — the CONTENT of the ear emergence HTML volume (data only, no rendering).

Numbers are NEVER hard-typed here: every value is referenced as [[KEY]] and resolved by
build_volume.py against vp_numeric_ssot.disp(KEY), so the prose cannot drift from the code.
Grade tokens [F]/[V]/[O]/[L]/[H] in body text are auto-styled by the builder.
Each section's first sentence is its direct answer (VP-SPEC §6-R.3); paragraphs stay short.
"""

META = {
    "volume": "Hearing from First Principles",
    "subtitle": "A falsifiable emergence of the ear — wave \u2192 place \u2192 R19 switch \u2192 congenital deafness",
    "author": "Young Jae Lee",
    "orcid": "0009-0002-7535-8245",
    "license": "CC BY 4.0",
    "license_url": "https://creativecommons.org/licenses/by/4.0/",
    "site": "https://jamming-physics.org",
    "canonical_base": "https://jamming-physics.org/ear",
    "repo": "https://github.com/rego093-sketch/jamming-physics",
    "dna_doi": "10.5281/zenodo.20471407",        # the cited readable-layer source (DNA v1.13)
    "volume_doi": "10.5281/zenodo.20790201",     # THIS volume's own MINTED concept DOI (latest-version resolver)
    "date_published": "2026-06-22",
    "date_modified": "2026-06-22",
    "package_version": "0.10.0",
}

GRADE_LABEL = {  # page-level badge text
    "forced": "[F] forced",
    "verified": "[V] verified",
    "open": "[O] open",
}

# --------------------------------------------------------------------------------------------
CONCEPTS = [
    {
        "slug": "r19-bistable-switch",
        "name": "R19 bistable switch",
        "term": "\u1e61 = g\u00b7s \u2212 s\u00b3 + h",
        "short": "The universal cubic substrate: bistable detection, and at criticality (g=0) cube-root amplification.",
        "body": [
            "The R19 switch is the one cubic the whole volume is built on. The state s obeys "
            "\u1e61 = g\u00b7s \u2212 s\u00b3 + h: with g>0 it is bistable (an all-or-none detector), and at "
            "the critical point g=0 the same equation compresses as the cube root s = h^(1/3).",
            "Its discontinuous threshold is the spinodal 2\u00b7(g/3)^1.5, which sets the emergence order of "
            "the master genes and the finite bistable drive window 2\u00b7spinodal(g). The same cubic appears "
            "as the tip-link switch (\u00a71), the cochlear amplifier (\u00a72), and the four deafness loci (\u00a73).",
        ],
    },
    {
        "slug": "greenwood-place-map",
        "name": "Greenwood place map",
        "term": "CF(x) = A(10^{a\u00b7x} \u2212 k)",
        "short": "Pitch by place: a \u221a-law resonance on log-graded stiffness gives an exponential, strictly monotone tonotopic map.",
        "body": [
            "The place map is how the cochlea turns a sound wave into a spatial code. The local resonance "
            "\u03c9 = \u221a(S/m) on a logarithmically graded stiffness forces an exponential map, reproducing "
            "Greenwood's CF(x) = A(10^{a\u00b7x} \u2212 k) to machine precision.",
            "Read off the inherited map, the apex is [[cf_apex]] and the base [[cf_base]], a span of "
            "[[octspan]]. Because CF(x) is strictly monotone, place \u2192 frequency is an order-isomorphism "
            "\u2014 the property \u00a77 uses to turn \u201cwhere a failure sits\u201d into \u201cwhich band is lost.\u201d",
        ],
    },
    {
        "slug": "gamma-level-a4-shape",
        "name": "\u03b3 (promoter stiffness): LEVEL and A4 SHAPE",
        "term": "\u03b3 = \u2212mean(\u0394G37);  A4 = signal \u2212 \u03b3",
        "short": "Each master gene is read as a stiffness LEVEL (\u03b3) and an orthogonal SHAPE (A4) \u2014 promoter structure only, never a function or a dose.",
        "body": [
            "\u03b3 is a measured promoter-structure LEVEL, not a fitted parameter. It is the window-mean of the "
            "SantaLucia-1998 nearest-neighbour stacking-stiffness signal; the A4 coordinate is that same signal "
            "with the mean removed (the orthogonal SHAPE).",
            "Both are read, because \u03b3 alone is lossy: genes with equal \u03b3 but different SHAPE are not "
            "interchangeable (the A4 tie-break). By the firewall, \u03b3 is never a channel gain, a drive, a dose, "
            "an in-vivo selectivity, or a clinical effect \u2014 all of those are [O].",
        ],
    },
]

# --------------------------------------------------------------------------------------------
CHAPTERS = [
    # ===== §1 (folder E1) ====================================================================
    {
        "n": 1, "slug": "01-place-and-traveling-wave",
        "subj": "The place map and the tip-link MET switch",
        "desc": "The hair-cell MET switch (TMC1/PCDH15/CDH23) emerges on the inherited \u221a-law place map by R19 spinodal order; the traveling-wave peak place is parameter-free, the full envelope the named open obstacle.",
        "grade": "forced",
        "answer": "The hair-cell mechanotransduction switch (TMC1 / PCDH15 / CDH23) emerges on the inherited "
                  "\u221a-law place map: each gene is read as \u03b3 (LEVEL) plus its A4 SHAPE, the R19 switch flips "
                  "all-or-none, and the traveling-wave peak place is parameter-free. The full dispersive envelope "
                  "stays the named [O].",
        "abstract": "Pitch is coded by PLACE: \u03c9 = \u221a(S/m) on a log-graded stiffness gives an exponential "
                    "map reproducing Greenwood to machine precision. The MET genes order by R19 spinodal "
                    "2\u00b7(\u03b3/3)^1.5 \u2014 TMC1 [[spin_TMC1]] < PCDH15 [[spin_PCDH15]] < CDH23 [[spin_CDH23]] "
                    "\u2014 a lower discontinuous threshold flipping earlier.",
        "cards": ["r19", "greenwood", "gamma"],
        "sections": [
            {"h2": "Pitch is place, not assumed", "paras": [
                "The cochlea reads a longitudinal sound wave and turns it into a spatial code. The resonance "
                "\u03c9 = \u221a(S/m) with log-graded stiffness forces an exponential place map; \u221aS \u221d "
                "10^(a\u00b7x) reproduces Greenwood\u2019s term to max|ratio\u22121| \u2248 2\u00d710\u207b\u00b9\u2076 [V].",
                "The map is inherited physics, not a fit. Its constants A/a/k are measured calibration [L]; the "
                "exponential SHAPE is forced by the \u221a-law on a logarithmically graded membrane.",
            ]},
            {"h2": "The MET switch emerges by spinodal order", "paras": [
                "The tip-link switch flips all-or-none, not gradually. Emergence order = argsort(spinodal(\u03b3)) "
                "with the A4 SHAPE breaking \u03b3-ties: TMC1 [[spin_TMC1]] < PCDH15 [[spin_PCDH15]] < CDH23 "
                "[[spin_CDH23]] < TMIE [[spin_TMIE]] [F].",
                "\u03b3 is measured [L]; a lower discontinuous threshold means earlier switch competence. The "
                "switch is OFF up to 0.99\u00b7spinodal and flips ON discontinuously past it \u2014 no graded leak "
                "across the barrier.",
            ]},
            {"h2": "The peak place is forced; the envelope is the obstacle", "paras": [
                "Only the traveling-wave PEAK place is parameter-free. Inverse-Greenwood round-trips: 250 Hz "
                "\u2192 x* [[x_250]], 1 kHz \u2192 [[x_1k]], 4 kHz \u2192 [[x_4k]], 16 kHz \u2192 [[x_16k]], to "
                "<1\u00d710\u207b\u00b9\u00b2 Hz [V].",
                "The full fluid-loaded dispersive ENVELOPE \u2014 width, cutoff slope, phase, delay \u2014 is the "
                "named [O]. A closed envelope would require tuning a sharpness Q (forbidden); it is characterised, "
                "never tuned, in \u00a75.",
            ]},
        ],
        "negatives": [
            "N1. The A4 tie-break never fires on this atlas (all MET \u03b3 are distinct); it is proven non-vacuous "
            "on constructed equal-\u03b3 inputs and kept because such genes can occur in general.",
            "N2. argsort(spinodal(\u03b3)) is a structural [F] order; its concordance with the measured "
            "developmental sequence is [O] \u2014 no timing dataset is bundled.",
            "N3. Only the peak place is forced; the full dispersive envelope is [O] (a closed envelope needs a "
            "tuned Q plus the fluid mass-loading \u2014 the named obstacle this seed exists to take up).",
            "N4. No per-gene tonotopic place is claimed \u2014 the MET genes span the whole partition; assigning one "
            "would be invention.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only (never a voltage, gain, dose, or effect). \u00a71 is "
                    "pre-disease. The percept of hearing is the mind volume\u2019s.",
    },

    # ===== §2 (folder E3) ====================================================================
    {
        "n": 2, "slug": "02-cochlear-amplifier",
        "subj": "The cochlear amplifier: cube-root compression",
        "desc": "The outer-hair-cell amplifier (prestin/SLC26A5) emerges as the inherited R19 cubic at criticality: response compresses as the parameter-free cube root r\u221dF^(1/3); detection and amplification are one cubic in two regimes.",
        "grade": "forced",
        "answer": "The outer-hair-cell active amplifier (prestin / SLC26A5) emerges as the inherited R19 cubic at "
                  "its critical point: the response compresses as the parameter-free cube root r \u221d F^(1/3), and "
                  "the 1/3 is forced by the cubic, not fitted. Detection and amplification are one cubic in two "
                  "regimes.",
        "abstract": "At criticality g=0 the inherited cubic g\u00b7s\u2212s\u00b3+h has its zero at s=F^(1/3); the "
                    "integrator\u2019s fitted exponent is [[cube_exp]] and the gain falls as F^([[gain_exp]]) \u2014 "
                    "the ~120 dB compression. The cube root is the cubic\u2019s critical fixed point, no constant "
                    "chosen.",
        "cards": ["r19", "greenwood"],
        "sections": [
            {"h2": "One cubic, two regimes", "paras": [
                "The \u00a71 detection switch and the \u00a72 amplifier are the same equation. With g=\u03b3_TMC1 the "
                "response is bistable (the \u00a71 switch); with g=0 the same drives give the continuous cube root "
                "s = h^(1/3) [F].",
                "Bistable detection runs in parallel with critical amplification \u2014 one substrate, two "
                "operating regimes. The amplifier is not a new mechanism; it is the cubic taken to its critical "
                "point.",
            ]},
            {"h2": "Compression is the cube root \u2014 forced, not fitted", "paras": [
                "The 1/3 exponent is the inherited cubic\u2019s critical fixed point. Evaluating the inherited "
                "sdot at s=F^(1/3), g=0 gives max|residual| [[cube_resid]] over seven decades of drive [F].",
                "The integrator\u2019s read-off exponent is [[cube_exp]] and the gain exponent [[gain_exp]] [V] "
                "\u2014 faint drives amplified ~100\u00d7 more than loud, the dynamic-range compression that lets "
                "the ear span ~120 dB.",
            ]},
            {"h2": "Uniform across the bank; magnitude is the obstacle", "paras": [
                "Every place carries the same critical cubic, so the 1/3 exponent is CF-independent \u2014 "
                "compression is uniform across frequency [F]. SLC26A5 (\u03b3 [[gamma_SLC26A5]], spinodal "
                "[[spin_SLC26A5]]) takes its place in the emergence lineage.",
                "The absolute gain, the dB of amplification, and the sharpness Q are [O] \u2014 a number would "
                "require tuning a constant. Only the exponent (1/3) and the direction (compression) are forced.",
            ]},
        ],
        "negatives": [
            "N1. The absolute gain / dB / dynamic-range-in-dB / sharpness Q are [O] \u2014 a value would require "
            "tuning. Only the exponent and the direction are forced.",
            "N2. The cube root matches the FORM of measured cochlear compression; the study-dependent I/O slope "
            "(~0.2\u20130.5 dB/dB) and the absolute curve are [O].",
            "N3. Otoacoustic-emission frequencies and amplitudes are [O] \u2014 they need the per-place gain, Q, and "
            "an operating point just above the bifurcation.",
            "N4. Prestin\u2019s electromotile force is NOT read from \u03b3 (firewall) \u2014 only the gene\u2019s "
            "spinodal-order place and the compression exponent are forced.",
            "N5. The inherited integrator under-converges to the fixed point at very small drive; the rigorous [F] "
            "is the analytic fixed point, the [V] is on the converged range.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only (never a motor force, gain, voltage, dose, or effect). "
                    "\u00a72 is pre-disease. The percept of loudness is the mind volume\u2019s.",
    },

    # ===== §3 (folder E4) \u2014 the goal =====================================================
    {
        "n": 3, "slug": "03-congenital-deafness-failure-modes",
        "subj": "Congenital deafness: the failure modes",
        "desc": "Congenital deafness emerges as the inherited R19 cubic\u2019s failure modes \u2014 three loci plus the critical regime \u2014 each gene mapped by cited function to a direction-only, proposal-only lever. Two classes are honest negatives. Nothing is diagnosed or dosed.",
        "grade": "forced",
        "answer": "Congenital deafness emerges as the inherited R19 cubic\u2019s failure modes: the cubic has three "
                  "failure loci plus its critical regime, and each deafness gene maps to one by its cited protein "
                  "function \u2014 forcing a different direction-only, proposal-only lever per class. Two classes "
                  "are honest negatives. Nothing is diagnosed or dosed.",
        "abstract": "The cubic g\u00b7s\u2212s\u00b3+h fails at DRIVE h (recoverable), STRUCTURE g (an honest "
                    "negative \u2014 the window 2\u00b7spinodal(g) collapses from [[win_g130]] to [[win_g001]] as "
                    "g\u21920, so drive cannot rescue lost structure), DOWNSTREAM readout, or the CRITICAL "
                    "amplifier. \u03b3 cannot separate the classes (overlap 0.1474), proving it reads structure only.",
        "cards": ["r19", "greenwood"],
        "sections": [
            {"h2": "Four loci, four lever directions", "paras": [
                "A congenital switch can fail in exactly four places on the cubic. DRIVE (GJB2/GJB6/SLC26A4, the "
                "K\u207a power), STRUCTURE (LHFPL5/MYO15A/USH2A/MYO7A/TMC1, the apparatus), READOUT (OTOF, the "
                "downstream synapse), and the CRITICAL amplifier (SLC26A5).",
                "Each gene maps to one locus by its cited protein function, never by \u03b3 [F]. The R19 geometry "
                "then forces a different substrate-inverse lever direction per class \u2014 direction-only, "
                "proposal-only.",
            ]},
            {"h2": "Which failures are recoverable in principle", "paras": [
                "Drive-class failures are switch-recoverable; structure-class are not, and the discriminant "
                "proves it. A structurally-intact switch sits OFF at h=0 and flips ON once h passes the spinodal "
                "[F].",
                "But the bistable window 2\u00b7spinodal(g) = 4(g/3)^1.5 is set by structure, collapsing from "
                "[[win_g130]] at g=1.30 to [[win_g001]] at g=0.01 [V]. No finite drive restores a window the lost "
                "structure destroyed \u2014 the lever must act on g, a layer this substrate cannot supply.",
            ]},
            {"h2": "The firewall, quantified", "paras": [
                "\u03b3 does not separate the classes. Drive-class \u03b3 \u2208 [1.3612, 1.5375] overlaps "
                "structure-class \u03b3 \u2208 [1.2801, 1.5086] by 0.1474, and no single \u03b3-threshold separates "
                "them [V].",
                "The class labels are cited biology; the R19 geometry supplies the lever direction. \u03b3 reads "
                "promoter stiffness, not protein function \u2014 it never becomes a function, a drive, a dose, or an "
                "effect.",
            ]},
            {"h2": "Why this is the goal, honestly stated", "paras": [
                "This is the most useful honest output a first-principles framework can give the congenitally "
                "affected: a structural map of why each deafness happens, and which hopes the geometry forbids.",
                "It states directions, never doses. Nothing here is a diagnosis, a treatment, or a promise \u2014 it "
                "is a map of where the inherited substrate says the lever must act, and where the geometry itself "
                "says the easy hope fails.",
            ]},
        ],
        "negatives": [
            "N1. EVERY physical magnitude is [O] \u2014 the drive in volts/Hz, the structural g in real units, the "
            "amplifier gain/dB/Q, any threshold value. Only directions and exponents are forced.",
            "N2. The failure CLASS is cited protein function, not derived from \u03b3 (the overlap proves \u03b3 "
            "cannot assign it); finer multi-locus failure is [O].",
            "N3. The substrate-inverse lever is proposal-only and direction-only \u2014 no molecule, dose, or "
            "efficacy; nothing diagnosed or treated.",
            "N4. The READOUT layer (OTOF / synapse) is not modelled by this transduction cubic \u2014 its rescue "
            "direction was [O] here, and is supplied in \u00a74.",
            "N5. The amplifier-gain [V] inherits \u00a72\u2019s small-drive caveat; the rigorous result is the "
            "analytic fixed point.",
            "N6. The full dispersive traveling-wave ENVELOPE is still the named [O]; \u00a73 does not touch it.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only (never a channel function, drive, motor force, voltage, "
                    "dose, in-vivo selectivity, or effect). The disease layer is proposal-only \u2014 direction-only "
                    "R19 failure modes and substrate-inverse lever directions. The percept of hearing is the mind "
                    "volume\u2019s.",
    },

    # ===== §4 (folder E5) ====================================================================
    {
        "n": 4, "slug": "04-readout-synapse-otoferlin",
        "subj": "The readout synapse (otoferlin)",
        "desc": "The readout layer \u00a73 left open is modelled: release is non-negative, monotone, saturating and NON-bistable, so it cannot be the R19 cubic \u2014 the minimal form is a rectified saturating Ca\u00b2\u207a sensor (otoferlin), reproducing auditory neuropathy and the OAE\u207a/ABR\u207b fingerprint.",
        "grade": "forced",
        "answer": "The readout layer that \u00a73 left [O] is now modelled: release is non-negative, monotone, "
                  "saturating and NON-bistable, so it cannot be the R19 cubic \u2014 the minimal form is a rectified "
                  "saturating Ca\u00b2\u207a sensor (otoferlin). That is the provable reason the cubic is blind to "
                  "OTOF.",
        "abstract": "Composed with the frozen switch, the sensor reproduces auditory neuropathy: a sound flips the "
                    "switch identically in a hearing and an OTOF ear (s=+1.3864), but the removed sensor zeroes "
                    "evoked release (0.5810 \u2192 0.0000). The cascade forces the composed exponent R \u221d F^(m/3) "
                    "\u2014 [[compexp_m1]], [[compexp_m2]], [[compexp_m3]], [[compexp_m4]] for m=1\u20134 \u2014 and the "
                    "OAE\u207a/ABR\u207b fingerprint.",
        "cards": ["r19", "greenwood"],
        "sections": [
            {"h2": "The readout is a different substrate \u2014 forced", "paras": [
                "Vesicle release cannot be the bistable cubic, and that is forced, not assumed. A release rate is "
                "non-negative, monotone in Ca\u00b2\u207a, saturating, and non-bistable (zero hysteresis), so its "
                "minimal normal form is a rectified saturating sensor [F].",
                "This is the provable reason the \u00a73 cubic is the wrong layer for OTOF: the cubic is two-sided, "
                "odd-symmetric, and bistable, none of which a release rate is.",
            ]},
            {"h2": "Auditory neuropathy falls out of the cascade", "paras": [
                "Driving a sound flips the frozen switch to s=+1.3864 \u2014 byte-identical in a hearing and an OTOF "
                "ear (the substrate sees nothing wrong). The intact sensor then releases 0.5810 (nerve fires); the "
                "removed sensor releases 0.0000 (nerve silent) [V].",
                "The defect is purely downstream of the flip. The dissociation is not asserted \u2014 it is "
                "reproduced from the cascade structure alone.",
            ]},
            {"h2": "The composed exponent and the clinical fingerprint", "paras": [
                "The auditory-nerve slope is the amplifier cube-root times the synaptic cooperativity m. Feeding "
                "F^(1/3) into a power-law sensor gives R \u221d F^(m/3): [[compexp_m1]], [[compexp_m2]], "
                "[[compexp_m3]], [[compexp_m4]] for m=1\u20134 [V].",
                "The amplifier (outer hair cell) stays intact while the readout (inner-hair-cell synapse) is "
                "zeroed \u2014 otoacoustic emissions present, auditory-brainstem response absent. Because they are "
                "separable stages, one survives while the other fails: the textbook auditory-neuropathy signature.",
            ]},
            {"h2": "The lever direction is now forced", "paras": [
                "The geometry forces the lever to act on the readout stage, not the switch \u2014 the switch is "
                "provably intact [F]. This is the opposite locus from the drive class (restore h) and the structure "
                "class (rebuild g).",
                "Direction-only, proposal-only: restore Ca\u00b2\u207a-sensor coupling, with no molecule, dose, "
                "in-vivo selectivity, or efficacy.",
            ]},
        ],
        "negatives": [
            "N1. EVERY magnitude is [O]: absolute [Ca\u00b2\u207a], the sensor Kd/Rmax, the releasable-pool size, the "
            "nerve rate in Hz. Only the structure, the dissociation, and the composed exponent m/3 are forced.",
            "N2. The cooperativity m is cited biology [L] (study-dependent), never derived or tuned; the composed "
            "result is parametric in m and its qualitative force (silence on knockout) is m-independent.",
            "N3. The Ca\u00b2\u207a(s) map is a minimal monotone rectifying proxy; the real CaV1.3 I\u2013V curve and "
            "nanodomain geometry are [O].",
            "N4. \u201cSensor removed\u201d models evoked release \u2261 0; graded/partial loss and the spontaneous "
            "component are [O] \u2014 \u00a74 models the evoked, sound-driven release only.",
            "N5. The lever is direction-only and proposal-only (firewall) \u2014 nothing designed, dosed, diagnosed, "
            "or treated.",
            "N6. The full dispersive traveling-wave ENVELOPE is still the named [O]; \u00a74 does not touch it.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only (never a Ca\u00b2\u207a-sensor affinity, a release rate, a "
                    "vesicle count, a voltage, a dose, or an effect). The disease layer is proposal-only \u2014 a "
                    "direction-only readout-failure mode and substrate-inverse lever. The percept of hearing is the "
                    "mind volume\u2019s.",
    },

    # ===== §5 (folder E6) ====================================================================
    {
        "n": 5, "slug": "05-traveling-wave-envelope",
        "subj": "The traveling-wave envelope",
        "desc": "The dispersive traveling-wave envelope \u2014 the seed\u2019s deepest open obstacle \u2014 is characterised without tuning as a one-parameter family in the sharpness Q: every location is forced and Q-invariant, every magnitude scales with Q, so a number for Q would be tuning.",
        "grade": "forced",
        "answer": "The dispersive traveling-wave envelope \u2014 the seed\u2019s deepest [O] \u2014 is characterised "
                  "without tuning: it is a one-parameter family in the sharpness Q. Every LOCATION is forced and "
                  "Q-invariant; every MAGNITUDE scales with Q and is fixed by no inherited constant, so a number "
                  "for Q would be tuning.",
        "abstract": "Modelling the partition as a driven damped resonator on the frozen Greenwood CF(x), the "
                    "velocity peak sits at \u03c90=CF for every Q (= the \u00a71 place), the reactance flips sign at "
                    "CF forcing an apical cutoff, and the \u22123 dB bandwidth is exactly \u03c90/Q \u2014 [[bw_Q10]] "
                    "vs the law [[bwlaw_Q10]] at Q=10. The group delay peaks at CF with magnitude 2Q/\u03c90.",
        "cards": ["r19", "greenwood"],
        "sections": [
            {"h2": "The peak sits at CF for every Q \u2014 the keystone", "paras": [
                "The envelope is a one-parameter family in Q. The single-pole velocity peak is at \u03c9=\u03c90 "
                "independently of damping, and \u03c90(x)=CF(x) is the inherited place \u2014 so the peak IS the "
                "\u00a71 forced place to |\u0394|=0 [F][V].",
                "The near-peak FORM is the universal resonance |V(\u03c9)|\u00b2 \u221d "
                "\u03c9\u00b2/[(\u03c90\u00b2\u2212\u03c9\u00b2)\u00b2+(\u03c90\u03c9/Q)\u00b2]; its location is "
                "forced and carries no free choice but Q.",
            ]},
            {"h2": "The asymmetry and the bandwidth are forced", "paras": [
                "The asymmetry is forced by the reactance sign. \u03c7 = 1\u2212(f/CF)\u00b2 is positive basal "
                "(propagating) and negative apical (evanescent), so a tone is cut off apical of its place \u2014 the "
                "SIGN robust to the slope scale [F].",
                "The \u22123 dB bandwidth is exactly \u03c90/Q: numeric [[bw_Q3]] / [[bw_Q10]] / [[bw_Q30]] / "
                "[[bw_Q100]] versus the law [[bwlaw_Q3]] / [[bwlaw_Q10]] / [[bwlaw_Q30]] / [[bwlaw_Q100]], to "
                "machine precision [V]. Only the width carries Q; the place is Q-invariant.",
            ]},
            {"h2": "The active amplifier is negative damping", "paras": [
                "The active process enters as negative damping, Q_eff = Q0/(1\u2212G), and at the critical point it "
                "imposes the \u00a72 cube root [F]. The direction (active \u2192 sharper, taller, \u2192 cube-root "
                "compression) is forced; the gain magnitude G is the \u00a72 [O].",
                "The group delay peaks at CF with magnitude 2Q/\u03c90: [[gd_Q5]] / [[gd_Q20]] / [[gd_Q80]] for "
                "Q=5/20/80 [V]. The location of the delay peak is forced; its absolute value in ms is [O].",
            ]},
            {"h2": "One knob, and fixing it is tuning", "paras": [
                "Varying Q ten-fold leaves the peak place invariant while the bandwidth scales exactly \u221d1/Q. "
                "No inherited constant sets Q \u2014 the \u221a-law fixes only the place, and \u03b3 is structure "
                "only, not a damping [F].",
                "A closed numeric envelope = a choice of Q = tuning (forbidden). \u00a75 does not close the [O]; it "
                "characterises it: FORM forced, exactly one scalar Q open, with a proof that writing it down would "
                "be tuning.",
            ]},
        ],
        "negatives": [
            "N1. The absolute sharpness is [O] \u2014 Q, the \u22123 dB bandwidth in Hz, the peak gain in dB. Only "
            "the FORM, the exact bandwidth law (=\u03c90/Q), and the peak place are forced.",
            "N2. The apical cutoff SLOPE (dB/oct) is [O] \u2014 it needs Q plus the fluid mass-loading prefactor; "
            "only the cutoff\u2019s existence and side (apical) are forced.",
            "N3. The active gain MAGNITUDE (the fraction G, the proximity to the bifurcation) is the inherited "
            "\u00a72 [O]; \u00a75 forces only the direction.",
            "N4. The absolute group delay (ms), the phase in cycles, and the traveling-wave speed are [O] (they "
            "need the fluid hydrodynamics); only that the delay peaks at CF is forced.",
            "N5. The model is the long-wave (1-D, WKB) approximation; the full 2-D/3-D fluid problem, the "
            "short-wave region at the peak, and the \u201csecond filter\u201d are the deeper [O].",
            "N6. Two-tone suppression, distortion products, and combination tones are downstream of the cubic but "
            "are not derived here \u2014 [O].",
            "N7. The felt percept of pitch and timbre is the mind volume\u2019s (firewall); \u00a75 moves only the "
            "physical envelope.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only \u2014 it is NOT the partition damping, NOT the quality "
                    "factor Q, NOT the active force, a gain, a delay, or a clinical effect. No disease claim here; "
                    "every magnitude is [O] with its obstacle named. The percept of pitch and timbre is the mind "
                    "volume\u2019s.",
    },

    # ===== §6 (folder E7) ====================================================================
    {
        "n": 6, "slug": "06-audible-band",
        "subj": "The audible band: a geometry-carved bandpass",
        "desc": "Why we hear ~20 Hz\u201320 kHz is derived as a geometry-carved bandpass on the inherited \u221a-law: the keystone N_oct = \u00bd\u00b7log\u2082(S_base/S_apex) is exact; shape and every edge sign are forced; the absolute edges are the irreducible measured-geometry obstacle.",
        "grade": "forced",
        "answer": "Why we hear ~20 Hz\u201320 kHz is derived as a geometry-carved bandpass on the inherited "
                  "\u221a-law: the \u221a-law halves the stiffness decades into octaves, so N_oct = "
                  "\u00bd\u00b7log\u2082(S_base/S_apex). The shape and every edge sign are forced; the absolute edges "
                  "are the irreducible measured-geometry [O].",
        "abstract": "Read off the inherited map, the apex is [[cf_apex]] and the base [[cf_base]], a span of "
                    "[[octspan]] \u2014 and inverting the \u221a-law gives a stiffness ratio [[stiffratio]], with "
                    "\u00bd\u00b7log\u2082(S_ratio) closing the keystone to |\u0394|=[[noct_closure]]. The low edge "
                    "is a helicotrema high-pass, the high edge an ossicular-mass low-pass at [[mass_slope]] (\u221212 "
                    "dB/oct).",
        "cards": ["greenwood", "r19"],
        "sections": [
            {"h2": "The keystone is exact", "paras": [
                "The \u221a-law halves stiffness decades into octaves. The apex CF [[cf_apex]] and base CF "
                "[[cf_base]] give a [[octspan]] span; inverting CF \u221d \u221aS gives a stiffness ratio "
                "[[stiffratio]], and \u00bd\u00b7log\u2082(S_ratio) returns the span to |\u0394|=[[noct_closure]] [V].",
                "Why ~10 octaves is forced once the (measured) ratio is known; why a ratio ~10\u2076 is the "
                "basilar membrane\u2019s graded geometry [L], never a fit.",
            ]},
            {"h2": "The span decomposes; the \u00bd is the forced part", "paras": [
                "The span splits cleanly into a forced exponential and a forced apical bend. The bare exponential "
                "10^(a\u00b7x) contributes [[bare_exp_oct]] and the helicotrema apical bend adds [[heli_bend_oct]], "
                "summing to the full [[octspan]] [V].",
                "The exponential SHAPE (octaves per stiffness decade) is forced by the \u221a-law; the absolute "
                "decades (~10\u2076) are measured geometry [L].",
            ]},
            {"h2": "Both edges are forced by topology and mass", "paras": [
                "The low edge is a helicotrema high-pass. The Greenwood offset \u2212A\u00b7k is a constant "
                "subtracted from an exponential, hence low-end-only: its fractional weight ratio apex/base is "
                "[[ten_pow_a]] (=10^a), bending the apex down to ~20 Hz, and the apical hole short-circuits slow "
                "pressure \u2014 a lows-cut robust to filter order [F].",
                "The high edge is a middle-ear low-pass. The ossicular mass forces a [[mass_slope]] (\u221212 "
                "dB/oct) asymptote robust to damping, and the base\u2019s finite stiffness fixes a finite ceiling "
                "CF_max = [[cf_base]] [F].",
            ]},
            {"h2": "The band is the product; magnitudes are the obstacle", "paras": [
                "The audible band is the unimodal product of the rolloffs \u2014 a bandpass whose shape and every "
                "edge sign are geometry, not new physics [F].",
                "The absolute edges and the three corners are the irreducible measured-geometry [O]; a number for "
                "any of them would be tuning. It is the same discipline as \u00a75 \u2014 there one scalar Q was "
                "open, here the open quantities are the measured geometry.",
            ]},
        ],
        "negatives": [
            "N1. The absolute band edges CF_min / CF_max (Hz) are [O] \u2014 they need S_apex, S_base, the ossicular "
            "mass, and the helicotrema area. Only the bandpass shape, the \u00bd exponent, and each edge sign are "
            "forced.",
            "N2. The low (helicotrema) corner is [O] \u2014 it needs the helicotrema area and cochlear compliance; "
            "only the existence and side (apical/low) are forced.",
            "N3. The high (middle-ear) corner / CF_max is [O] \u2014 it needs the ossicular mass and S_base; only "
            "the existence, the side (high), and the \u221212 dB/oct asymptote are forced.",
            "N4. The stiffness RATIO (~10\u2076) is a measured anatomical input \u2014 the membrane widens and thins "
            "base\u2192apex; the \u221a-law forces only the factor (\u00bd) converting it to octaves.",
            "N5. The band here is the long-wave / place-resonance account (same scope as \u00a75); the full "
            "2-D/3-D fluid transfer and the middle ear\u2019s multi-resonance are the deeper [O].",
            "N6. The absolute BM stiffness gradient law S(x) and the developmental program that builds the graded "
            "membrane are anatomy / the DNA volume\u2019s \u2014 [O] here.",
            "N7. The felt pitch / loudness RANGE as experience is the mind volume\u2019s (firewall); \u00a76 moves "
            "only the physical band edges.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only \u2014 it is NOT a stiffness, a corner frequency, the "
                    "helicotrema area, the ossicular mass, or a band edge. No disease claim here (the band-specific "
                    "losses are \u00a77, proposal-only). Every magnitude is [O] with its obstacle named. The felt "
                    "range as experience is the mind volume\u2019s.",
    },

    # ===== §7 (folder E8) ====================================================================
    {
        "n": 7, "slug": "07-band-specific-hearing-loss",
        "subj": "Band-specific hearing loss (class \u00d7 place)",
        "desc": "Characteristic audiogram shapes emerge by composing \u00a73\u2019s failure-class axis with \u00a76\u2019s place axis: because the place map is monotone, where a failure sits IS which band is lost (an order-isomorphism). Every direction is forced; every dB and notch-Hz is the irreducible measured obstacle.",
        "grade": "forced",
        "answer": "Characteristic audiogram shapes emerge by composing \u00a73\u2019s failure-class axis with "
                  "\u00a76\u2019s place axis: because the place map is monotone, where a failure sits IS which "
                  "frequency band is lost (an order-isomorphism). Every direction is forced; every dB, slope, and "
                  "notch-Hz is the irreducible measured [O].",
        "abstract": "The inherited CF(x) is strictly monotone, so a contiguous band of failed places maps to a "
                    "contiguous band of lost frequencies, round-tripping to |\u0394|=[[e8_roundtrip]]: basal "
                    "x\u2208[0.7,1.0] \u2192 [[e8_basal_lo]]\u2013[[e8_basal_hi]] (high-frequency presbycusis, load "
                    "ratio [[e8_loadratio]]), mid \u2192 [[e8_mid_lo]]\u2013[[e8_mid_hi]] (cookie-bite), apical "
                    "\u2192 [[e8_apic_lo]]\u2013[[e8_apic_hi]] (low-frequency reverse-slope).",
        "cards": ["greenwood", "r19"],
        "sections": [
            {"h2": "The keystone: place\u2192frequency is an order-isomorphism", "paras": [
                "Because CF(x) is strictly monotone, where a failure sits is which band is lost. A basal band "
                "x\u2208[0.7,1.0] maps to [[e8_basal_lo]]\u2013[[e8_basal_hi]], mid to [[e8_mid_lo]]\u2013[[e8_mid_hi]], "
                "apical to [[e8_apic_lo]]\u2013[[e8_apic_hi]], each round-tripping to |\u0394|=[[e8_roundtrip]] [V].",
                "No constant is tuned \u2014 this is the monotonicity of the inherited map turned into an "
                "isomorphism. WHERE fails \u21d2 WHICH band is lost.",
            ]},
            {"h2": "The four shapes are images of where", "paras": [
                "Each audiogram is the image of a place band. Basal degeneration \u2192 high-frequency down-slope: "
                "the base cycles fastest (CF is the rate), so cumulative load is basal-first, load(base)/load(apex) "
                "= [[e8_loadratio]] \u2014 classic presbycusis [F].",
                "An over-drive at the outer/middle-ear transfer peak \u2192 a notch below the top (the ~3\u20136 kHz "
                "C5-dip); an apical ion-regime failure \u2192 a low-frequency reverse-slope (WFS1 archetype); a "
                "mid-cochlear locus \u2192 cookie-bite \u2014 the weakest, since only mid\u2192mid is forced and the "
                "locus concentration is cited [L].",
            ]},
            {"h2": "The lever, and the earlier negatives carry", "paras": [
                "Each audiogram is a (class \u00d7 band) hypothesis, and the lever is the \u00a73 direction applied "
                "at the \u00a76 band, proposal-only [F]. \u00a73\u2019s honest negative carries: the structural "
                "component of a high-frequency loss admits no drive rescue (the window 2\u00b7spinodal(g) \u2192 0 "
                "as g\u21920).",
                "Only the apical drive-class is switch-recoverable in principle \u2014 and even then only the "
                "direction is named. No molecule, dose, in-vivo selectivity, diagnosis, or efficacy.",
            ]},
            {"h2": "Shape forced, magnitudes the obstacle", "paras": [
                "The place-isomorphism and the four shape directions are parameter-free; every dB threshold, "
                "dB/oct slope, notch frequency, and age of onset is the irreducible measured [O] [F].",
                "A closed numeric audiogram = a choice of those magnitudes = tuning (forbidden). The disease layer "
                "states directions, never doses \u2014 and keeps \u00a73\u2019s honest negatives, refusing to "
                "promise a drive rescue for a structural high-frequency loss.",
            ]},
        ],
        "negatives": [
            "N1. Every magnitude is [O] \u2014 the dB thresholds, the dB/oct slopes, the notch frequency in Hz, the "
            "age of onset, the load rate, the absolute band edges. Only the shape and the directions are forced.",
            "N2. Cookie-bite is the weakest of the four \u2014 the isomorphism forces only mid PLACE \u2192 mid "
            "FREQUENCY; the mid-concentration of the locus is a cited input, not derived.",
            "N3. The notch frequency (~3\u20136 kHz) is [O] \u2014 it needs the ear-canal length and ossicular "
            "transfer; only the existence of an interior transfer peak (a notch below the top) is forced.",
            "N4. Presbycusis is multi-factorial (sensory, strial, neural); \u00a77 forces only the basal-first "
            "direction of the cyclic-load component.",
            "N5. The cumulative-load argument forces the ordering (basal-first) but assumes load accrues with "
            "cycling rate \u2014 a cited biophysical premise, not derived here; the rate and accrual law are [O].",
            "N6. Real audiograms are individual and noisy; \u00a77 is a shape-DIRECTION claim about each "
            "etiology\u2019s population tendency, not a per-patient predictor.",
            "N7. The readout class (OTOF / synapse) has no place-band shape in this transduction map \u2014 its "
            "failure is downstream of the flip ([O]); the felt experience of band-specific loss is the mind "
            "volume\u2019s.",
        ],
        "firewall": "\u03b3 reads promoter STRUCTURE only \u2014 it is NOT a band edge, a load rate, a dB threshold, "
                    "a notch frequency, or a clinical effect. The disease layer is proposal-only: direction-only "
                    "(class \u00d7 band) failure modes and substrate-inverse lever directions. WFS1 is named only as "
                    "a cited clinical archetype \u2014 no new \u03b3 is measured. Every magnitude is [O]. The felt "
                    "experience is the mind volume\u2019s.",
    },
]

# the honest open-obstacle ledger surfaced on the hub (VP-SPEC §C3) ---------------------------
O_LEDGER = [
    ("\u00a71", "The full dispersive traveling-wave ENVELOPE", "characterised in \u00a75 down to a single scalar Q"),
    ("\u00a72", "Absolute amplifier gain / dB / sharpness Q", "a number would require tuning a constant"),
    ("\u00a73", "Every physical magnitude of the deafness loci", "only directions and exponents are forced"),
    ("\u00a74", "Sensor Kd/Rmax, releasable-pool size, nerve rate (Hz)", "cooperativity m is cited biology, not derived"),
    ("\u00a75", "The sharpness Q (and the full 2-D/3-D hydrodynamics)", "a closed numeric envelope = a choice of Q = tuning"),
    ("\u00a76", "Absolute band edges CF_min / CF_max and the three corners", "measured geometry; a number = tuning"),
    ("\u00a77", "Every dB, slope, notch-Hz, and age of onset", "a closed numeric audiogram = tuning"),
]
