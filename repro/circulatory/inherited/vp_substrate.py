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
           "Organ","Neuron","dominant_freq","SEED"]
