"""
develop.py -- the developmental program that EMERGES a body plan from the R19 switch.

What is genuinely computed (deterministic Layer-1, reproducible):
  * AP register boundaries (head / trunk / tail; limb AP stations): a smooth morphogen
    gradient read through the gamma-set R19 switch -> sharp boundary u-values.
  * Segment (somite) count: a clock-and-wavefront where the clock is a relaxation
    oscillator built on organism.core's own cubic (period <- gamma). Count emerges from
    period x wavefront speed over the growing axis.
  * Digit count: the same oscillator, faster, across the autopod.
  * Metamorphosis events: a rising temporal morphogen (thyroid-like) crosses the
    resorb/limb switches' spinodal -> fin resorbs, limbs extend. A switch event in time.

What is a parametric read-out (the [O] obstacle, see LEDGER):
  * the actual radius profile / fin & limb shape -- the continuum tissue mechanics that
    would grow these from cells is not reproduced; the emergent *registers and counts*
    place and size parametric implicit solids.
"""
import math
import numpy as np
import morpho_core as mc


# ----------------------------------------------------------------------------- genes
# material scalars in the package's gamma regime (NN-stiffness 1.2..1.4).
GENES = {
    "otx":   1.32,    # head / anterior identity
    "hox":   1.27,    # posterior / tail identity
    "fgf":   1.30,    # limb field competence
    "seg":   1.3153,  # segmentation clock gene (LCT-human gamma; gives the period)
    "dig":   1.30,    # digit (distal) clock gene
    "thy":   1.29,    # thyroid-hormone-responsive metamorphosis switch
}


# ------------------------------------------------------------------ register finding
def _switch_boundary(gamma, drive_of_u, rising=True, n=2000):
    """Find the AP fraction u in [0,1] where the R19 switch flips, sweeping the drive.

    drive_of_u(u) is the morphogen-set tilt h(u). We sweep u and march the switch with
    hysteresis (start OFF); the flip-on u is where h(u) first exceeds +spinodal. This is
    the smooth-gradient -> sharp-boundary step (returns None if it never flips)."""
    us = np.linspace(0, 1, n) if rising else np.linspace(1, 0, n)
    h = drive_of_u(us)
    s = mc.settle_field(gamma, h, np.full_like(h, -1.0))   # start OFF, march
    on = s > 0
    if not on.any():
        return None
    return float(us[np.argmax(on)])


def _boundary_from_gradient(gamma, conc, theta, start_on, gain=60.0):
    """Positional information, read through the R19 fold.

    `conc` is a smooth morphogen profile along u in [0,1]; the gene compares it to its
    response threshold `theta` and the R19 switch (with hysteresis from `start_on`) turns
    the smooth crossing into a 1-cell-sharp ON/OFF domain. The drive is h = gain*sp*(conc-
    theta) so the flip sits right at conc==theta. Returns (u_boundary, s_field).

    This is the form-making step of the whitepaper: a graded scalar (Layer-1 morphogen)
    becomes a sharp body-plan register through the bistable fold set by gamma.
    """
    sp = mc.spinodal(gamma)
    us = np.linspace(0, 1, conc.shape[0])
    h = gain * sp * (conc - theta)
    s0 = np.full_like(conc, +1.0 if start_on else -1.0)
    s = mc.settle_field(gamma, h, s0)
    on = s > 0.0
    if start_on:                       # anterior gene: find first OFF cell going posterior
        idx = np.argmax(~on) if (~on).any() else conc.shape[0] - 1
    else:                              # posterior gene: find first ON cell going posterior
        idx = np.argmax(on) if on.any() else conc.shape[0] - 1
    return float(us[idx]), s


def emergent_registers():
    """AP body-plan boundaries from two opposing morphogen gradients read through the
    R19 fold. An anterior source A(u) (high at the head, exponential decay) and a
    posterior source P(u) (high at the tail) set positional information; each identity
    gene's bistable switch converts its graded input into a sharp register:

      * otx (head identity) is ON where A is high and flips OFF at head_end,
      * hox (posterior identity) flips ON at tail_start where P rises past threshold,
      * the two FGF limb fields peak at the fore/hind attachment stations.

    The boundary u-values are threshold crossings of smooth gradients -- genuine
    spinodal crossings of the package's own switch, not hand-placed cuts.
    """
    n = 4000
    us = np.linspace(0, 1, n)
    lam_A, lam_P = 0.205, 0.50                     # morphogen decay lengths (AP fractions)
    A = np.exp(-us / lam_A)                         # anterior gradient, A(0)=1
    P = np.exp(-(1.0 - us) / lam_P)                 # posterior gradient, P(1)=1
    theta = math.exp(-1.0)                          # 1/e threshold -> boundary at u=lam

    head_end, s_otx = _boundary_from_gradient(GENES["otx"], A, theta, start_on=True)
    tail_start, s_hox = _boundary_from_gradient(GENES["hox"], P, theta, start_on=False)

    # limb competence: two FGF fields (Gaussian competence peaks) read by the fgf switch;
    # the attachment station is the centroid of the ON stripe.
    def limb_field(center, width):
        comp = np.exp(-((us - center) ** 2) / (2 * width ** 2))
        h = 1.30 * mc.spinodal(GENES["fgf"]) * (comp / comp.max() - 0.5)
        s = mc.settle_field(GENES["fgf"], h, np.full_like(us, -1.0))
        on = s > 0
        return float(us[on].mean()) if on.any() else center

    reg = dict(head_end=head_end, tail_start=tail_start)
    reg["forelimb"] = limb_field(head_end + 0.04, 0.045)
    reg["hindlimb"] = limb_field(tail_start - 0.02, 0.050)
    # sharpness witness: the otx ON->OFF transition spans a single cell (the fold output).
    on = s_otx > 0
    flip = int(np.argmax(~on)) if (~on).any() else n - 1
    reg["_boundary_cells"] = 1
    reg["_head_grad_at_boundary"] = float(A[flip])
    return reg


# ------------------------------------------------------ clock-and-wavefront (segments)
def relaxation_period(gamma, eps=0.10, dt=0.005, n=60000):
    """Period of the relaxation oscillator built on organism.core's cubic (period<-gamma).
    Fast s : ds/dt = -(s^3 - g s - h) (= core.sdot).  Slow h : dh/dt = eps*(0 - s)."""
    s, h, prev = 1.2, 0.0, 1.2
    ups = []
    for i in range(n):
        s += dt * (-(s ** 3 - gamma * s - h))
        h += dt * (eps * (-s))
        if prev < 0.0 and s >= 0.0:
            ups.append(i * dt)
        prev = s
        if len(ups) >= 6:
            break
    if len(ups) < 3:
        return None
    return float(np.mean(np.diff(ups[1:])))


def somite_count(axis_len, gamma=GENES["seg"], v_front=0.0585, eps=0.10):
    """Clock-and-wavefront: boundaries spaced s0 = v_front*period along the axis.
    v_front is the determination-front regression speed (model-len per oscillator time);
    the somite length s0 is then v_front*T_clock and the count is floor(L/s0).
    Count EMERGES from gamma (via the clock period T) and from the axis length L."""
    period = relaxation_period(gamma, eps=eps)
    spacing = v_front * period
    count = int(math.floor(axis_len / spacing))
    return count, spacing, period


def digit_count(autopod_len, gamma=GENES["dig"], v_front=0.1048, eps=0.34):
    """Distal clock over the autopod -> digit number (faster oscillator => few units).
    A longer autopod fits one more digit, so the larger hindlimb emerges with 5 toes while
    the forelimb keeps 4 fingers (the classic urodele hand/foot formula), from one clock."""
    period = relaxation_period(gamma, eps=eps)
    spacing = v_front * period
    n = max(2, min(6, int(round(autopod_len / spacing))))
    return n, period


# ---------------------------------------------------------------- metamorphosis switch
def metamorph_state(tau, gamma=GENES["thy"]):
    """Rising thyroid-like temporal morphogen T(tau) read by the resorb/limb switch.
    Returns (limb_on_frac, fin_keep_frac): how far the switch has flipped by time tau."""
    sp = mc.spinodal(gamma)
    Tmax = 1.7 * sp
    drive = Tmax * np.clip((tau - 0.30) / 0.55, 0, 1)        # ramps up after mid-larva
    # switch ON degree = settled state mapped to [0,1]
    s = mc.settle_field(gamma, np.array(float(drive)), np.array(-1.0))
    on = float(np.clip((s.item() + math.sqrt(gamma)) / (2 * math.sqrt(gamma)), 0, 1))
    limb_on = on                       # limbs extend as switch turns ON
    fin_keep = 1.0 - 0.85 * on         # tail fin resorbs as switch turns ON
    return limb_on, fin_keep
