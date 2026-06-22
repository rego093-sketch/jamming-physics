# START HERE — increment E9 (red-green colour vision; beyond the spine)

The first **mechanism extension beyond the down-conversion spine** (E0→E8 complete; see `BLUEPRINT.md`).
**BUILT (v0.13.0).**

**Scope — theoretical, NON-CLINICAL (binding, above the task).** Purely academic geometry and
dynamical-systems research. It does **not** diagnose, treat, prescribe, screen, classify a person, or
triage; it designs **no** molecule and states **no** dose, potency, selectivity, or efficacy. The
colour-vision layer is **structure-only** and **direction-only**, behind a **machine-checked magnitude
firewall** (`run.py`'s `main()` asserts the whole output carries no quantitative clinical token and no
`%`; `gate_E9.py` re-asserts it). The felt experience of colour — and of colour confusion — is deferred
to the **mind** volume.

**Task:** read the most common inherited colour-vision difference (**red-green**) off the **E1 angle
map** — the same three cone opsins **OPN1SW / OPN1MW / OPN1LW** placed at three propagation angles
χ(λmax) by their **measured** peaks (S 420 / M 530 / L 560 nm, literature [L]). E9 adds **no new γ**,
fetches nothing, and re-derives nothing — it is E1 read for **fragility**.

**Why this framing (the productive path):** colour is the propagation **angle** (E1), so the three
cones are three angle-**samples** and the three colour-discrimination axes are their pairwise angle
**margins**. Two facts then fall out of the frozen law with nothing fitted: (1) the **green-red (M-L)
margin is the smallest** of the three, so red-green is the structurally most fragile axis — matching the
epidemiology [L]; and (2) because χ is a function of λ **alone**, two opsins with the **same** λmax map
to the **same** angle, so the margin is **exactly 0** at coincidence — which unifies **dichromacy**
(remove one sample) and **anomalous trichromacy** (two samples converge) as one continuum whose endpoint
is coincidence.

**Deliverable (done):** a deterministic module `research/E9-red-green-dichromacy/run.py` that
(A) maps the three cones to three angles and shows the three pairwise **margins** (S-M 0.0509°, M-L
0.0421°, S-L 0.0931°), with the **green-red M-L margin the smallest** — forced by the measured λmax +
the frozen law, matching that red-green is the most common inherited colour-vision difference [L];
(B) proves the **coincidence collapse** (same λmax ⇒ margin **exactly 0**), then reads **dichromacy** as
removing one of the M/L angle-samples (the M-L axis vanishes; one chromatic axis survives) and
**anomalous trichromacy** as two peaks **converging** — shown **sawtooth-proof** inside one m-band where
χ is locally smooth-monotone, the margin falling **monotonically to 0** as the gap closes — stating the
**direction only** (peaks toward each other ⇒ margin shrinks), every magnitude a firewall-blocked **[O]**,
and naming the honest caveat that χ(λ) is hypersensitive and **distributional** (a sawtooth, inherited
E1/E6); (C) the **orthogonality** result — colour (angle, E1) is orthogonal to position (image, E3) and
brightness (the R19 switch, E2), so removing a cone costs **one colour axis** while spatial acuity and
the light/dark response stay intact (this is why it is *colour*-blindness, matching preserved acuity);
(D) reads the opsin γ (LEVEL) + A4 (SHAPE) **READ-ONLY** as a structural excitability offset (byte-equal
to the frozen atlas), with **no** claim that γ predicts λmax, and names the X-linked genomic
architecture (the OPN1LW/OPN1MW tandem array) as **[L]/[O]**, not γ. It prints every displayed number,
self-hashes (2× run → identical sha256), passes the magnitude firewall, and declares grades
[F]/[V]/[L]/[O] honestly. Plus `gate_E9.py` (`E9 GATE: PASS`, eight checks incl. the firewall), folded
into the verifier's foundation list and absorbed into the HTML volume as chapter **E9**.

**Provenance (this increment):** **nothing was fetched and no γ was added.** E9 consumes only the frozen
angle law (`vp_color_by_angle`), the frozen switch (`vp_substrate`), the already-measured cone λmax that
E1 placed, and the frozen atlas γ (read-only). `inherited/FROZEN_SHA256.json` is **unchanged** — the
foundation does not move for this increment. γ measured, never fitted.

**Firewall:** structure-only γ (never a channel voltage, gain, current, potency, dose, selectivity, or
clinical effect); the disease/condition layer is structure-only / direction-only and machine-checked;
the felt percept of colour and of colour confusion is the mind volume's.

**Next (same firewall, beyond the spine):** **light/dark adaptation** as gain control on the switch;
**accommodation + refractive error** (myopia/hyperopia) extending E3's optics; and — much harder,
multifactorial — an acquired/degenerative disease layer (AMD, glaucoma, diabetic retinopathy). Still
deferred: **SIX6** (eye-field TF), the one remaining gene in the atlas `_to_measure`, foldable by the
fetch→re-freeze discipline if a later increment needs it. The sibling **hearing** sense ships as its own
seed (`vp_ear_emergence_seed…`).
