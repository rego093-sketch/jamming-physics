#!/usr/bin/env python3
"""
M44 - DEGLACIATION RECENCY FROM ONGOING REBOUND  (present-tense; corrects M35 over-firewall)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

SELF-CORRECTION. M35 said "using GIA to date deglaciation = RECORD [O]." On reflection that
was hiding behind a symbol. The QUALITATIVE fact - the rebound is STILL GOING (not finished)
- is present-tense, and with the present-tense mantle relaxation time it forces a RECENCY
bound by pure physics, no assumed historical rate. The ORDER (recent, ~10^4 yr, NOT 10^8) is
[V]; only the exact calendar number keeps mild model dependence.

PHYSICS. A viscous mantle under a removed load relaxes with a characteristic time
  tau = 4*pi*eta / (rho * g * lambda)          (fundamental mode, load wavelength lambda)
After time t since unloading, the REMAINING uplift decays as exp(-t/tau). So:
  - if t ~ a few tau, uplift is STILL going (a few percent to tens of percent left)  -> OBSERVED
  - if t >> tau (e.g. 10^8 yr = many thousand tau), uplift is COMPLETE -> none left.
We measure ~1 cm/yr of uplift TODAY in the old ice centres. Ongoing uplift => unloading was
within ~1-2 tau. That is a PRESENT-TENSE clock on the deglaciation.

LOCK (present-tense quantities):
  eta = 1.0e21 Pa s      (upper-mantle viscosity from present GIA/post-seismic obs)
  rho = 3300 kg/m^3      g = 9.81 m/s^2      lambda = 3.0e6 m (continental load ~3000 km)
  uplift_now = 0.010 m/yr (Hudson Bay / Fennoscandia, present GPS)
  remaining_uplift = 100.0 m (order of rebound still to come in the centres)
SEED = 19. Double-SHA-256 self-gate.
"""
import os, math, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
ETA, RHO, G, LAM = 1.0e21, 3300.0, 9.81, 3.0e6
UPLIFT_NOW, REMAIN = 0.010, 100.0
SEC_PER_YR = 3.15576e7

tau_s = 4*math.pi*ETA/(RHO*G*LAM)
tau_yr = tau_s/SEC_PER_YR
# crude time-to-complete at present rate (lower bound on how much event-time is left)
t_complete = REMAIN/UPLIFT_NOW
# remaining fraction if the deglaciation were at various ages:
def remain_frac(t_yr): return math.exp(-t_yr/tau_yr)

out = []
out.append("M44  DEGLACIATION RECENCY FROM ONGOING REBOUND  (present-tense; SEED=19)")
out.append("")
out.append("[MANTLE RELAXATION TIME  (present-tense viscosity)]:")
out.append(f"  eta={ETA:.0e} Pa s, lambda={LAM/1e3:.0f} km  ->  tau = {tau_yr:,.0f} yr")
out.append("")
out.append("[REMAINING-UPLIFT TEST]  exp(-t/tau) for candidate deglaciation ages t:")
for t in [1e3, 5e3, 1e4, 5e4, 1e6, 1e8]:
    rf = remain_frac(t)
    tag = "ongoing uplift POSSIBLE" if rf > 1e-3 else "uplift COMPLETE - none left"
    out.append(f"   t = {t:>10,.0f} yr   remaining fraction = {rf:8.1e}   {tag}")
out.append("")
out.append("[OBSERVED]:")
out.append(f"  present uplift = {UPLIFT_NOW*1000:.0f} mm/yr in the old ice centres; ~{REMAIN:.0f} m still to come")
out.append(f"  (=> ~{t_complete:,.0f} yr of rebound REMAINS at the present rate).")
out.append("")
out.append("[VERDICT]  (present-tense physics, no assumed historical rate):")
out.append(f"  Rebound is STILL GOING. With tau ~ {tau_yr:,.0f} yr, that is only possible if the")
out.append("  ice was unloaded within ~1-2 tau, i.e. ~10^4 yr ago. Were it 10^8 yr ago")
out.append("  (~10^4 tau), the remaining fraction would be exp(-25000) ~ 0 - the land would")
out.append("  sit flat, no uplift. The fact that Hudson Bay and Fennoscandia are RISING TODAY")
out.append("  is a PRESENT-TENSE clock: the deglaciation was RECENT, order 10^4 yr. [V]")
out.append("  => This is exactly the author's 'last ice age' logic, and it needs NO calendar")
out.append("     date and NO assumed decay rate - just the ongoing springback we measure now.")
out.append("  => Correction to M35: the deglaciation's RECENCY (order 10^4 yr) is present-tense,")
out.append("     not [O]. Only the precise calendar number keeps mild viscosity-model dependence.")
out.append("")
out.append("[CONSEQUENCE for the cascade]:")
out.append("  The ICE event is provably recent. So 'when did the ice melt' is SETTLED (recent),")
out.append("  not an open [O] mystery. The only timing question left is whether the SOURCE/")
out.append("  SALT/RIFT belong to this SAME recent relaxation - the coupling question.")
out.append("")
out.append("[GRADE] deglaciation recency (order 10^4 yr) PRESENT-TENSE [V] from ongoing")
out.append("  rebound + present mantle viscosity; corrects the prior over-firewalling.")

body = "\n".join(out)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "d04347fe230f28bd21d396e887e28920ffe049efdf889f20cfd4494a67cf9487"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
