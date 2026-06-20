#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_substrate.py  --  VENDORED shared substrate primitive (DO NOT re-derive).

The R19 jamming-lattice bistable switch + the FitzHugh-Nagumo relaxation oscillator (Neuron)
+ the organ-emergence helpers (Organ / spinodal / dwell). Single source of the substrate math
across the VP papers: byte-identical-in-spirit to vp_neuro_engine (neuro 02) and organism.core
(DNA). Vendored so this package reproduces offline without an upstream whitepaper. Do not rewrite
the math; report bugs to the neuro engine owner (VP-SPEC C1, primitive single-source).

Grades (VP-SPEC C3):  [F] forced  ./  [V] simulation-verified  ./  [O] open.
"""
import numpy as np
import math

SEED = 19
def seed_everything(seed=SEED):
    np.random.seed(seed)

# ===========================================================================
#  R19 — the shared bistable switch  (the jamming/DNA/neuron primitive)
#     ds/dt = g*s - s^3 + h     (double well; g sets the threshold SCALE)
# ===========================================================================
def sdot(s, g, h):
    return g * s - s ** 3 + h

def spinodal(g):
    """|h| past which the opposite basin disappears -> the flip is DISCONTINUOUS."""
    return 2.0 * (g / 3.0) ** 1.5

def barrier(g):
    """g^2/4 : energy barrier between the two basins (state stability)."""
    return g * g / 4.0

def settle(g, h, s0=None, n=1500, dt=0.02):
    """Integrate the R19 field from s0 to its steady state under fixed drive h."""
    s = (-math.sqrt(g) if g > 0 else 0.0) if s0 is None else s0
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s

def is_on(g, h, s0=None):
    return settle(g, h, s0) > 0.0


def dwell(g, brake, K=0.6):
    """DWELL: how long the switch runs ∝ γ^1.5 (DNA §5), throttled by a growth
    brake. Sets RELATIVE organ size — the order/direction is forced [F], the
    absolute magnitude is calibration [O]."""
    return (g ** 1.5) / (K + brake)


# ===========================================================================
#  Gate - a tonically-CLOSED R19 valve  (sphincter / LES / Oddi)
#     The gate is the R19 switch HELD in the closed (-s) basin by a tonic
#     closing bias -h_tone. A coordinated relaxation/pressure drive opens it iff
#     that drive clears the closing bias AND the R19 opening spinodal (bistable
#     hysteresis): open_drive > gate_resistance = h_tone + spinodal(g). Derived
#     entirely from the R19 double well ds/dt = g*s - s^3 + h; no new dynamics,
#     no fitted coefficient. (digestive_vp_site primitive.)
# ===========================================================================
def gate_resistance(h_tone, g=1.0):
    """Opening drive a coordinated signal must EXCEED to flip the gate open from
    its closed rest state: the tonic closing bias plus the R19 opening spinodal.
    Rises monotonically with gate tone."""
    return abs(h_tone) + spinodal(g)

def gate_open(h_tone, open_drive, g=1.0):
    """Gate = R19 switch biased CLOSED by -h_tone; True if a coordinated
    relaxation/pressure drive `open_drive` flips it to the OPEN (+s) basin,
    integrating from the closed basin s0=-sqrt(g). Opens iff
    open_drive > gate_resistance(h_tone, g). Low tone -> opens spuriously
    (incontinent, GERD direction); high tone / weak signal -> stuck closed
    (achalasia / Oddi direction)."""
    s_closed = -math.sqrt(g)
    return settle(g, -abs(h_tone) + open_drive, s0=s_closed) > 0.0


# ===========================================================================
#  Reservoir - a fundic COMPLIANCE / volume element  (gastric accommodation)
#     The fundic wall is the SAME R19 element, resting CONTRACTED at s = -sqrt(g).
#     A vagal accommodation drive h_acc >= 0 RELAXES it, sliding the contracted
#     operating point UP toward the barrier top -- toward the spinodal of the
#     contracted basin, where the wall YIELDS. The wall STIFFNESS (elastance) at
#     the accommodated operating point is the R19 restoring curvature
#         k(s*) = -d(sdot)/ds|_{s*} = 3*s*^2 - g
#     and the COMPLIANCE is its inverse C = 1/k; a fixed meal volume V raises
#     pressure P = V/C = V*k. Rising accommodation drives s* -> the yield point
#     s*^2 = g/3 where k -> 0 (maximal compliance) -- which is EXACTLY the R19
#     spinodal h_acc = spinodal(g) (an algebraic identity of the double well, the
#     marginal saddle-node). Lost accommodation (h_acc -> 0) leaves s* = -sqrt(g),
#     k = 2g (stiffest) -> premature pressure. Derived entirely from the R19 double
#     well ds/dt = g*s - s^3 + h; no new dynamics, no fitted coefficient. Readings
#     operate strictly BELOW yield (settle converges fast there; the marginal point
#     has critical slowing and is treated in closed form). (digestive_vp_site
#     primitive.)  [V] simulation-verified.
# ===========================================================================
def wall_stiffness(g, h_acc):
    """Fundic-wall elastance at the accommodated operating point: the R19 restoring
    curvature k = 3*s^2 - g (= -d(sdot)/ds) evaluated where a vagal relaxation drive
    h_acc>=0 settles the contracted wall (from s0=-sqrt(g)). Falls monotonically as
    accommodation rises (the wall slides toward its yield/spinodal point, k->0); k=2g
    at zero accommodation (stiffest)."""
    s_acc = settle(g, abs(h_acc), s0=-math.sqrt(g))
    return 3.0 * s_acc * s_acc - g

def reservoir_compliance(g, h_acc):
    """Fundic COMPLIANCE C = 1/k (inverse wall stiffness) at the accommodated
    operating point -- equivalently the meal volume tolerated per unit satiation
    pressure. Rises as the vagal accommodation drive h_acc relaxes the wall toward
    yield (diverges at the spinodal); defined while the wall is still stable (k>0)."""
    k = wall_stiffness(g, h_acc)
    return float("inf") if k <= 0.0 else 1.0 / k

def meal_pressure(g, h_acc, v_meal):
    """Intragastric pressure rise from a fixed meal volume v_meal on the accommodated
    reservoir: P = V/C = V*k. Low accommodation (small h_acc) -> stiff wall ->
    premature pressure rise (functional dyspepsia, post-prandial distress / early
    satiation); restored accommodation (large h_acc) -> compliant wall -> the meal is
    absorbed without a pressure spike. v_meal is a model volume unit (absolute scale [O])."""
    k = wall_stiffness(g, h_acc)
    return float(v_meal) * (k if k > 0.0 else 0.0)


# ===========================================================================
#  Afferent gain - a visceral mechanoreceptor SENSITIVITY element  (afferent gain)
#     A visceral afferent is the SAME R19 element resting QUIESCENT in the contracted
#     basin s = -sqrt(g). Its static SUSCEPTIBILITY to a wall-distension input h is the
#     slope of the settled state, ds*/dh, which by the implicit function theorem on the
#     fixed point g*s - s^3 + h = 0 is exactly the INVERSE of the same R19 restoring
#     curvature the reservoir uses:
#         chi(s*) = ds*/dh = 1 / (3*s*^2 - g) = 1 / k(s*)
#     -- i.e. the visceral-afferent GAIN and the fundic-wall COMPLIANCE (above) are the
#     IDENTICAL quantity 1/k evaluated at the operating point: one R19 curvature read two
#     ways (sensory gain here, mechanical compliance there). A peripheral SENSITIZATION
#     bias b >= 0 (inflammation / mediators / peripheral facilitation) slides the operating
#     point up toward yield, so chi RISES and DIVERGES at the R19 spinodal (b = spinodal(g))
#     -- visceral hypersensitivity / allodynia as a saddle-node CRITICAL GAIN, the same
#     marginal point as the reservoir yield. Baseline b=0 -> s*=-sqrt(g), k=2g, chi=1/(2g).
#     Derived entirely from the R19 double well ds/dt = g*s - s^3 + h; no new dynamics, no
#     fitted coefficient. PERIPHERAL afferent term ONLY -- the felt / affective interpretation
#     lives in `mind` (firewall kept). (digestive_vp_site primitive.)  [V]/[F].
# ===========================================================================
def afferent_gain(g, b):
    """Visceral-afferent SUSCEPTIBILITY chi = ds*/dh = 1/k at the operating point a peripheral
    sensitization bias b>=0 sets, integrating the afferent R19 element from its quiescent
    contracted rest s0=-sqrt(g). chi = 1/(3*s*^2 - g) -- the SAME restoring-curvature inverse as
    the fundic compliance reservoir_compliance(g,b) (an exact identity: gain == compliance, one
    R19 curvature). Baseline b=0 -> chi=1/(2g) (normal sensitivity); rising sensitization slides
    s* toward yield (k->0) so chi RISES and DIVERGES at the R19 spinodal -- allodynia/hyperalgesia
    as a saddle-node critical gain. Peripheral afferent term only; felt/affective reading is `mind`."""
    k = wall_stiffness(g, abs(b))
    return float("inf") if k <= 0.0 else 1.0 / k

def afferent_signal(g, b, stimulus):
    """Afferent OUTPUT for a wall-distension `stimulus` on the element sensitized by bias b>=0: the
    operating-point shift settle(g, b+stimulus) - settle(g, b) from the quiescent rest s0=-sqrt(g).
    For a FIXED sub-yield distension it rises monotonically with b (allodynia: the same stimulus
    yields a larger afferent signal as the gain 1/k amplifies); once b+stimulus crosses the R19
    spinodal the element flips DISCONTINUOUSLY to the firing basin (spontaneous/runaway afferent
    activity -- the un-provoked 'crisis' regime). Distension and signal are model units (absolute
    scale [O]); the felt/pain interpretation is `mind` (firewall kept)."""
    s_lo = settle(g, abs(b), s0=-math.sqrt(g))
    s_hi = settle(g, abs(b) + abs(stimulus), s0=-math.sqrt(g))
    return float(s_hi - s_lo)


# ===========================================================================
#  Metaplasia - a PRECURSOR fate-stability reduction  (Barrett's / intestinal metaplasia)
#     A metaplastic precursor (Barrett's oesophagus, gastric intestinal metaplasia) is the SAME R19
#     cell-fate switch with its stability SCALE reduced by sustained injury: chronic acid/bile reflux
#     or atrophic-gastritis inflammation lowers g to g_meta = g_healthy - drop -- the IDENTICAL
#     g-reduction the oncology kernel already uses for chronic H. pylori, now read as a discrete
#     precursor COMPARTMENT rather than a continuous background. A metaplastic cell therefore sits on
#     the SMALLER R19 fate barrier g_meta^2/4 < g_healthy^2/4, so the NEXT (malignant) crossing is
#     rate-limited on the precursor: carcinoma arises ~only from the metaplastic compartment, and
#     restoring g (removing the injury / ablating the metaplasia) collapses that next-step rate back
#     toward the healthy baseline. Derived entirely from the R19 double well ds/dt = g*s - s^3 + h;
#     no new dynamics, no fitted coefficient. (digestive_vp_site primitive.)  [V]/[F].
# ===========================================================================
def metaplastic_scale(g_healthy, drop):
    """Fate-stability SCALE of a METAPLASTIC cell: the healthy R19 scale reduced by a sustained-injury
    `drop` (0 < drop < g_healthy), g_meta = g_healthy - drop. The SAME g-reduction the oncology kernel
    applies for chronic H. pylori, read here as a discrete precursor (Barrett's / intestinal metaplasia).
    Clamped to a small positive floor so the barrier stays defined. R19-derived; no fitted coefficient."""
    g = float(g_healthy) - float(drop)
    return g if g > 1e-6 else 1e-6

def metaplasia_barrier_drop(g_healthy, drop):
    """Reduction in the unbiased R19 fate barrier produced by the metaplasia g-drop:
    barrier(g_healthy) - barrier(metaplastic_scale(g_healthy, drop)). This is the exponent gap (over the
    shared substrate noise) by which a metaplastic cell's next-transition rate exceeds a healthy cell's
    -- i.e. WHY the precursor compartment is rate-limiting for the malignant crossing. R19-derived."""
    return barrier(g_healthy) - barrier(metaplastic_scale(g_healthy, drop))


# ===========================================================================
#  Inflammation - a RELAPSING-REMITTING R19 element COUPLED to the barrier  (IBD)
#     Mucosal inflammation is the SAME R19 switch read as a relapsing element: a REMISSION (-s) basin and
#     a FLARE (+s) basin. The net pro-inflammatory drive is (antigen - suppression). From its current
#     basin (remission s0=-sqrt(g), or flare s0=+sqrt(g)), a drive past the R19 spinodal flips
#     remission->flare; the bistable HYSTERESIS makes a flare SELF-SUSTAINING after the antigen subsides
#     (the relapsing-remitting course) until suppression drives it back past the REVERSE spinodal. The
#     induction threshold (flip a flare to remission) is antigen + spinodal(g); the (lower) maintenance
#     threshold (hold remission) is antigen - spinodal(g) -- the induction-vs-maintenance dosing asymmetry,
#     an exact property of the double well. The FLARE AMPLITUDE is the barrier-lowering drive the section-7
#     oncology kernel consumes: a cumulative flare burden (extent x duration x activity) lowers the section-7
#     fate-stability scale g -> a higher malignant-crossing rate (the IBD->colorectal / Crohn's small-bowel
#     neoplasia continuity). Restoring remission restores g. Derived entirely from the R19 double well
#     ds/dt = g*s - s^3 + h; no new dynamics, no fitted coefficient. (digestive_vp_site primitive.)  [V]/[F].
# ===========================================================================
def flare_state(g, antigen, suppression=0.0, in_flare=False):
    """Relapsing-remitting inflammation as the R19 switch: settle the inflammation element under the net
    drive (antigen - suppression) from its current basin (remission s0=-sqrt(g), or flare s0=+sqrt(g) when
    in_flare). A drive past the R19 spinodal flips remission->flare; the bistable hysteresis keeps a flare
    self-sustaining after the antigen subsides (the relapsing course) until suppression past the reverse
    spinodal returns it to remission. Returns the settled state (>0 flare, <0 remission). R19-derived."""
    s0 = (math.sqrt(g) if in_flare else -math.sqrt(g))
    return settle(g, abs(antigen) - abs(suppression), s0=s0)

def flare_burden(g, antigen, suppression=0.0, in_flare=False):
    """Inflammatory burden = the FLARE AMPLITUDE (the positive part of flare_state): >0 in an active flare,
    ~0 in remission. This is the instantaneous barrier-lowering drive consumed by inflammatory_barrier_scale
    below (the section-7 oncology kernel). R19-derived."""
    return max(0.0, flare_state(g, antigen, suppression, in_flare))

def inflammatory_barrier_scale(g_barrier, cumulative_burden, kappa):
    """Barrier SCALE a relapsing-inflammation burden leaves for the section-7 barrier-Kramers kernel: the
    healthy fate-stability scale lowered in proportion to the CUMULATIVE inflammatory burden (extent x
    duration x activity), g_eff = g_barrier - kappa*cumulative_burden -- the IDENTICAL g-reduction the
    section-7 chronic-Hp / metaplasia step uses, now driven by inflammatory flares. Deeper/longer active
    disease lowers the dysplasia barrier -> a higher malignant-crossing rate (the IBD->colorectal /
    Crohn's small-bowel neoplasia continuity); suppression (remission -> burden 0) restores g. Clamped to a
    small positive floor. The single coupling kappa is calibrated by ONE bisection to a cited IBD-cancer RR
    (no curve-shape tuning). R19-derived. (digestive_vp_site primitive.)"""
    g = float(g_barrier) - float(kappa) * max(0.0, float(cumulative_burden))
    return g if g > 1e-6 else 1e-6


# ===========================================================================
#  Autocatalysis - an R19 zymogen switch in the RUNAWAY (latching) regime  (acute pancreatitis)
#     Pancreatic zymogen activation is the SAME R19 switch: an INACTIVE (-s) basin and an autocatalytic
#     ACTIVE (+s) basin. A protective inhibitor (SPINK1 / trypsin-inhibitor capacity) is a tonic CLOSING
#     bias -inhibitor; a transient insult (gallstone obstruction, alcohol metabolite, hypertriglyceridaemia)
#     is a trigger drive. The activation FORM is the gate's (tone -> inhibitor), but the question is the
#     OPPOSITE of a valve: a valve re-closes, whereas the disease IS the LATCH. The autocatalytic positive
#     feedback (the +g*s term: active trypsin activates more trypsinogen) makes the ACTIVE basin
#     SELF-SUSTAINING -- once a trigger past the threshold inhibitor + spinodal(g) flips the switch, removing
#     the trigger does NOT reverse it (R19 hysteresis): autodigestion runs on. This is WHY established acute
#     pancreatitis has no pharmacological 'off-switch' and intervention must be PRE-threshold. A strong
#     inhibitor > spinodal(g) abolishes the self-sustaining basin -> the activation becomes reversible (the
#     protective role of trypsin inhibitors). Derived entirely from the R19 double well ds/dt = g*s - s^3 + h;
#     no new dynamics, no fitted coefficient. (digestive_vp_site primitive.)  [V]/[F].
# ===========================================================================
def autoactivation_threshold(g, inhibitor=0.0):
    """Trigger drive a transient insult must EXCEED to flip the zymogen R19 switch from its inactive (-s)
    rest into the autocatalytic ACTIVE (+s) basin: the protective inhibitor bias plus the R19 opening
    spinodal. Rises with the inhibitor; a PRSS1 gain-of-function / SPINK1 loss LOWERS it (hereditary
    pancreatitis). Same FORM as gate_resistance (tone -> inhibitor); the active basin is self-sustaining
    (autodigestion_latched). R19-derived."""
    return abs(inhibitor) + spinodal(g)

def autodigestion_latched(g, trigger, inhibitor=0.0):
    """Acute pancreatitis: does a TRANSIENT activation trigger flip the zymogen R19 switch into the runaway
    ACTIVE basin AND STAY there after the trigger is removed? Two phases: (1) apply the trigger from the
    inactive rest s0=-sqrt(g); (2) REMOVE the trigger (drive -> the inhibitor bias only) and re-settle.
    Returns (flipped_under_trigger, latched_after_removal). LATCHED = irreversible autodigestion: the
    autocatalytic positive feedback makes the active state self-sustaining once over threshold, so removing
    the trigger does NOT reverse it (intervention must be PRE-threshold). A strong inhibitor > spinodal(g)
    abolishes the self-sustaining basin -> reversible (trypsin-inhibitor protection). R19-derived; no fit."""
    s_inactive = -math.sqrt(g)
    s_trig  = settle(g, -abs(inhibitor) + abs(trigger), s0=s_inactive)   # phase 1: trigger ON
    s_relax = settle(g, -abs(inhibitor),                s0=s_trig)        # phase 2: trigger OFF
    return (s_trig > 0.0), (s_relax > 0.0)


# ===========================================================================
#  Perfusion - a tissue-VIABILITY R19 switch SUSTAINED by blood flow  (mesenteric ischemia)
#     Tissue viability is the SAME R19 switch: a VIABLE (+s) basin held up by perfusion and a
#     NON-VIABLE / ischemic (-s) basin. The net sustaining drive is the perfusion minus the local
#     metabolic DEMAND, h = perfusion - demand (oxygen supply pushes +s viable; demand consumes the
#     margin). From the VIABLE basin s0=+sqrt(g) the tissue stays viable until the supply drops below
#     the lower spinodal (perfusion - demand < -spinodal(g)) -> it flips to the ischemic basin. From the
#     ischemic basin s0=-sqrt(g) it RECOVERS only once perfusion - demand > +spinodal(g) -- the
#     revascularization threshold. The hysteresis GAP between the two (width 2*spinodal) is the
#     ischemic RESERVE: a salvageable window in which re-perfusion still recovers the tissue. Rising
#     metabolic demand (post-prandial, the gut's work after a meal) RAISES the rescue threshold
#     demand + spinodal -- which is WHY chronic mesenteric ischemia presents as post-prandial pain
#     ('intestinal angina'): a fixed splanchnic supply meets the threshold at rest but not after a meal.
#     NB the model's basin flip is the REVERSIBLE ischemia<->viable transition; the IRREVERSIBLE
#     structural infarct (cell death) is a one-way tissue transition OUTSIDE the reversible double well
#     (graded [O], like the established-pancreatitis necrosis). Overlaps the `circulatory` sibling (the
#     perfusion FIELD itself) -- cited, not re-emerged. Derived entirely from the R19 double well
#     ds/dt = g*s - s^3 + h; no new dynamics, no fitted coefficient. (digestive_vp_site primitive.) [V]/[F].
# ===========================================================================
def perfusion_threshold(g, demand=0.0):
    """Perfusion a coordinated blood supply must EXCEED to keep/RESCUE viable tissue from the ischemic
    basin: the local metabolic demand plus the R19 opening spinodal. Rises with demand -- the post-
    prandial threshold rise behind chronic mesenteric 'intestinal angina'. Same FORM as gate_resistance
    / autoactivation_threshold (bias -> demand). R19-derived."""
    return abs(demand) + spinodal(g)

def viability_margin(g, perfusion, demand=0.0):
    """Reserve of perfusion ABOVE the rescue threshold: perfusion - perfusion_threshold(g, demand)
    = perfusion - demand - spinodal(g). Positive -> a viable margin; falls monotonically as perfusion
    drops OR metabolic demand rises (so it goes negative post-prandially in chronic mesenteric ischemia
    -- the 'intestinal angina' the model reads as a vanished reserve). R19-derived."""
    return float(perfusion) - perfusion_threshold(g, demand)

def tissue_viable(g, perfusion, demand=0.0, infarcted=False):
    """Settle the viability R19 element under the net sustaining drive (perfusion - demand) from its
    current basin (viable s0=+sqrt(g), or ischemic s0=-sqrt(g) when infarcted=True). Returns the settled
    state (>0 viable, <0 ischemic / non-viable). Dropping perfusion below demand - spinodal(g) flips
    viable->ischemic; restoring perfusion above demand + spinodal(g) recovers ischemic->viable
    (revascularization). The bistable gap between is the salvageable ischemic window. The basin flip is
    the REVERSIBLE ischemia transition; established structural infarction is out-of-model [O]. R19-derived."""
    s0 = (math.sqrt(g) if not infarcted else -math.sqrt(g))
    return settle(g, float(perfusion) - abs(demand), s0=s0)


# ===========================================================================
#  Supersaturation - an R19 CRYSTALLIZATION switch with a nucleation barrier  (cholesterol gallstones)
#     Cholesterol gallstone formation is the SAME R19 switch read as a phase change: a DISSOLVED (-s)
#     basin (cholesterol carried in micelles/vesicles) and a CRYSTAL / STONE (+s) basin. The drive is the
#     cholesterol SATURATION INDEX offset h = CSI - 1 (CSI>1 is supersaturated bile, tilting toward the
#     crystal basin). The R19 basin barrier g^2/4 IS the classical-nucleation-theory free-energy barrier
#     the metastable supersaturated bile must cross to nucleate a stone: below the spinodal (CSI - 1 <
#     spinodal(g)) the dissolved state PERSISTS even though supersaturated (the metastable zone, why
#     supersaturated bile need not stone), and only past CSI - 1 > spinodal(g) does it nucleate
#     spontaneously. The hysteresis is the clinically decisive part: once a STONE exists, lowering CSI back
#     below 1 does NOT redissolve it until CSI - 1 < -spinodal(g) -- which is WHY bile-acid (UDCA)
#     dissolution only works on small / early / non-calcified stones and cholecystectomy (removing the
#     supersaturated reservoir) is definitive. Biliary STASIS (impaired gallbladder emptying -- a B1-gate
#     problem; pregnancy / fasting / TPN) prolongs residence and promotes nucleation (the time-to-nucleate
#     magnitude is a Kramers-rate-over-this-barrier reading [O], as in the carcinogen kernel). Derived
#     entirely from the R19 double well ds/dt = g*s - s^3 + h; no new dynamics, no fitted coefficient.
#     SEAM to `circulatory` (lipid handling) and `mind` (the felt biliary pain). (digestive_vp_site
#     primitive.) [V]/[F].
# ===========================================================================
def nucleation_barrier(g):
    """Free-energy barrier separating supersaturated bile from the crystalline (stone) phase: the R19
    basin barrier g^2/4 read as the classical-nucleation-theory barrier. The exponent (over the shared
    substrate noise) that sets the time-to-nucleate -- the same barrier the carcinogen kernel reads as a
    crossing rate. R19-derived."""
    return barrier(g)

def supersaturation_drive(csi):
    """Thermodynamic crystallization tilt from the cholesterol saturation index: h = CSI - 1
    (>0 supersaturated, the metastable/labile regime; <0 undersaturated, dissolving). R19-derived."""
    return float(csi) - 1.0

def stone_nucleates(g, csi, seeded=False):
    """Settle the crystallization R19 element under the supersaturation drive (CSI - 1) from the dissolved
    rest s0=-sqrt(g) (or from an EXISTING nucleus s0=+sqrt(g) when seeded=True). Returns the settled state
    (>0 crystal/stone, <0 dissolved). From dissolved: nucleates only past CSI - 1 > spinodal(g)
    (supersaturated-but-metastable below it). Seeded: an existing stone PERSISTS until CSI - 1 < -spinodal(g)
    -- the dissolution hysteresis (UDCA works only on small/early stones; cholecystectomy is definitive).
    R19-derived; no fitted coefficient."""
    s0 = (-math.sqrt(g) if not seeded else math.sqrt(g))
    return settle(g, supersaturation_drive(csi), s0=s0)


# ===========================================================================
#  Wall mechanics - an R19 HERNIATION switch driven by Laplace pressure  (diverticular disease)
#     Colonic-wall integrity is the SAME R19 switch: an INTACT (-s) basin and a HERNIATED / out-pouched
#     (+s) basin. The drive is the segmental luminal PRESSURE; the R19 scale g_wall IS the wall's
#     structural strength (collagen / elastin / muscularis), so a weaker wall sits on a smaller barrier.
#     The geometry enters through LAPLACE's law P = tension / radius: a low-fibre diet makes small hard
#     stools that the colon grips with short high-pressure segmenting contractions -- a SMALL radius and a
#     HIGH segmenting tension both raise P. When the segmental pressure exceeds the wall's herniation
#     threshold spinodal(g_wall), the intact basin loses stability and the wall buckles out at its weak
#     points (the vascular penetrations) -> a diverticulum. Wall WEAKNESS (aging, Ehlers-Danlos / Marfan
#     collagen disorders) lowers g_wall -> a lower threshold (the age-rising prevalence). The treatment is
#     the geometry in reverse: dietary fibre bulks the stool (a LARGER radius) and softens the segmenting
#     pattern (LOWER tension), dropping Laplace P back below the threshold. Derived entirely from the R19
#     double well ds/dt = g*s - s^3 + h; no new dynamics, no fitted coefficient. The mechanical FIXED-block
#     obstructions (hernia / volvulus / intussusception / adhesions) are the counterpart the section-14
#     FUNCTIONAL (patent-lumen) motility module explicitly excludes; diverticulITIS reuses the C1
#     relapsing-inflammation flare (cited, not re-emerged). (digestive_vp_site primitive.) [V]/[F].
# ===========================================================================
def laplace_pressure(tension, radius):
    """Wall pressure from Laplace's law P = tension / radius. A low-fibre small-radius segment under a
    strong segmenting contraction -> high P; a bulky high-fibre large-radius segment -> low P. Rises
    monotonically as radius falls or segmenting tension rises. (Geometry feeding the herniation switch.)"""
    return float(tension) / float(radius)

def herniation_threshold(g_wall):
    """Segmental pressure past which the intact-wall R19 basin loses stability and the wall out-pouches:
    the R19 opening spinodal spinodal(g_wall). A weaker wall (lower g_wall -- aging / collagen disorder)
    lowers the threshold (the age-rising diverticulosis prevalence). R19-derived."""
    return spinodal(g_wall)

def wall_herniates(g_wall, pressure):
    """Settle the wall R19 element from its intact rest s0=-sqrt(g_wall) under the segmental-pressure
    drive; returns the settled state (>0 herniated/out-pouched, <0 intact). Herniation emerges monotonically
    as the Laplace pressure rises (low fibre) or the wall strength g_wall falls (aging / collagen disorder).
    Treatment lowers the pressure (fibre -> larger radius + softer segmenting) below the threshold. R19-derived."""
    return settle(g_wall, float(pressure), s0=-math.sqrt(g_wall))


class Organ:
    """An organ EMERGED from its master gene's measured γ (READ-ONLY). The R19
    switch sets a DISCONTINUOUS presence threshold (spinodal); STATE (the master
    cis drive) decides presence — an intact downstream pathway with the master
    OFF still yields ABSENCE ('parts present ≠ trait'). The functional spinodal
    orders organs in developmental time; DWELL ∝ γ^1.5 sets relative size.
    γ is measured and never fitted; only STATE and size move.  [F] form/order."""
    def __init__(self, name, gamma, master="", partners=(), layer=""):
        self.name, self.g = name, float(gamma)
        self.master, self.partners, self.layer = master, tuple(partners), layer
        self.spinodal = spinodal(self.g)
        self.barrier = barrier(self.g)
    def present(self, cis_drive):
        """Present only if the master cis drive clears the γ-set threshold."""
        return is_on(self.g, cis_drive)
    def functional_spinodal(self):
        """Drive needed to switch the organ ON — the developmental-order key."""
        return self.spinodal
    def size(self, brake=0.5):
        return dwell(self.g, brake)


# ===========================================================================
#  Neuron — R19 switch + SLOW recovery  (FitzHugh-Nagumo)  => low frequency
# ===========================================================================
class Neuron:
    """A neuron is the R19 switch (fast) with a slow recovery w. Because the
    recovery sets the period, the intrinsic rhythm is far slower than the switch
    timescale -> the substrate speaks at LOW FREQUENCY (neuro 02).  [F]/[V]"""
    def __init__(self, gamma=1.0, tau_f=1.0, tau_s=40.0, beta=0.5, name="neuron"):
        self.g, self.tau_f, self.tau_s, self.beta, self.name = gamma, tau_f, tau_s, beta, name

    def run(self, drive, E=1.0, I=1.0, T=4000.0, dt=0.05, s0=-1.0, w0=0.0):
        """drive: scalar bias h0 (or a length-T array). Returns membrane trace S."""
        n = int(T / dt)
        if np.isscalar(drive):
            drive = np.full(n, float(drive))
        else:
            drive = np.asarray(drive, float)
            n = len(drive)
        s, w = s0, w0
        S = np.empty(n)
        for i in range(n):
            s += dt * (E * (self.g * s - s ** 3) - I * w + drive[i]) / self.tau_f
            w += dt * (s - self.beta * w) / self.tau_s
            s = 12.0 if s > 12 else (-12.0 if s < -12 else s)
            S[i] = s
        return S, dt

    @staticmethod
    def spikes(S, thr=0.0):
        """Up-crossings of threshold = all-or-none spike times (indices)."""
        a = S > thr
        return np.where((~a[:-1]) & (a[1:]))[0] + 1

    @staticmethod
    def rate_hz(S, dt, thr=0.0):
        sp = Neuron.spikes(S, thr)
        dur = len(S) * dt
        return len(sp) / dur if dur > 0 else 0.0


def dominant_freq(S, dt):
    """Dominant rhythm (Hz) from the FFT of the membrane trace (DC removed)."""
    x = S - S.mean()
    n = len(x)
    f = np.fft.rfftfreq(n, d=dt)
    P = np.abs(np.fft.rfft(x)) ** 2
    P[0] = 0.0
    return float(f[np.argmax(P)])


__all__ = ["seed_everything","sdot","spinodal","barrier","settle","is_on","dwell",
           "gate_resistance","gate_open","wall_stiffness","reservoir_compliance","meal_pressure",
           "afferent_gain","afferent_signal","metaplastic_scale","metaplasia_barrier_drop",
           "flare_state","flare_burden","inflammatory_barrier_scale",
           "autoactivation_threshold","autodigestion_latched",
           "perfusion_threshold","viability_margin","tissue_viable",
           "nucleation_barrier","supersaturation_drive","stone_nucleates",
           "laplace_pressure","herniation_threshold","wall_herniates",
           "Organ","Neuron","dominant_freq","SEED"]
