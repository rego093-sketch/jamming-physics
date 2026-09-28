#!/usr/bin/env python3
"""
ch2_light.py  --  Reproduces Chapter 2 (light as the lattice elastic wave) -- INCLUDING the
framework's sharpest external CONFLICT (vacuum dispersion), made reproducible rather than hidden.

A) SPEED EMERGENCE (solid foundation).  A pulse on a mass-spring lattice moves at c=a*sqrt(K/m),
   exactly proportional to sqrt(K) (R^2=1) and independent of amplitude => c^2 = K/rho.

B) VACUUM DISPERSION (the conflict).  A lattice disperses: omega(k)=2 sqrt(K/m)|sin(ka/2)|,
   v_g = c cos(ka/2) (light slows at high k). The quadratic scale is E_QG = sqrt(2) h c /(pi ell).
   EXPECTED: E_QG = 1.15e5 eV (ell=D=4.854pm)  or  8.82e11 eV (ell=a=6.33e-19 m).
   Fermi GRB 090510 bound: E_QG,2 > 1.3e11 GeV = 1.3e20 eV.
   => predicted dispersion too STRONG by 15 orders (D) / 8 orders (a) => DECISIVE CONFLICT,
      unless light is effectively DISPERSIONLESS (open problem). GWs at c (GW170817) are fine.

C) ANGLE THEORY (exploratory).  sin(chi)=lambda/(mD), m=ceil(lambda/D): visible/radio ~transverse
   (= light), gamma longitudinal. D-INDEPENDENT test: at a COMMON order, sin(chi) ∝ lambda, so
   sin(chi_633)/sin(chi_532) = 633/532 = 1.190 regardless of D.

INPUTS: SI constants; D=4.854e-12 m, a=6.33e-19 m. No fitting.
DEPENDENCIES: numpy.
"""
import numpy as np

h = 6.62607015e-34; c_si = 2.99792458e8
hc_eVnm = 1239.84193
D = 4.854e-12; a_cell = 6.33e-19

# ---------- A) speed emergence ----------
def pulse_speed(K, m=1.0, a=1.0, N=8000, amp=1.0):
    j = N//4; idx = np.arange(N)
    x = amp*np.exp(-((idx-j)/12.0)**2)
    c = np.sqrt(K/m)*a
    dudx = (np.roll(x,-1)-np.roll(x,1))/(2*a)   # right-moving pulse: v = -c du/dx
    v = -c*dudx
    acc = lambda x: (K/m)*(np.roll(x,1)-2*x+np.roll(x,-1))
    A = acc(x); dt = 0.1*np.sqrt(m/K)
    com = lambda y: np.sum(idx*y**2)/np.sum(y**2)
    c0 = com(x); nstep = 1500
    for _ in range(nstep):
        v = v + 0.5*A*dt; x = x + v*dt; A = acc(x); v = v + 0.5*A*dt
    return (com(x)-c0)*a/(nstep*dt)

# ---------- B) dispersion / conflict ----------
def E_QG_eV(ell_m):
    return np.sqrt(2)*hc_eVnm/(np.pi*ell_m*1e9)

# ---------- C) angle theory ----------
def chi_deg(lam, D=D):
    m = np.ceil(lam/D); s = min(lam/(m*D), 1.0)
    return np.degrees(np.arcsin(s)), m

if __name__ == "__main__":
    print("=== A) SPEED EMERGENCE: c = a*sqrt(K/m), c ∝ sqrt(K), amplitude-independent ===")
    Ks = np.array([1., 4., 16.])
    cs = [pulse_speed(K) for K in Ks]
    for K, c in zip(Ks, cs):
        print(f"  K={K:5.1f}: simulated pulse speed ~ {c:.3f}  (theory a*sqrt(K/m)={np.sqrt(K):.3f})")
    R2 = np.corrcoef(np.sqrt(Ks), cs)[0,1]**2
    print(f"  c vs sqrt(K): R^2={R2:.4f} (analytic c=a*sqrt(K/m) is exact => c^2=K/rho).")
    print(f"  amplitude test: speed(amp=1)={pulse_speed(4.,amp=1.):.3f} vs speed(amp=3)={pulse_speed(4.,amp=3.):.3f} (same).\n")

    print("=== B) VACUUM DISPERSION — the decisive external conflict (reproduced, not hidden) ===")
    EQG_D = E_QG_eV(D); EQG_a = E_QG_eV(a_cell); Fermi = 1.3e20
    print(f"  lattice dispersion: v_g = c*cos(ka/2) (light slows at high k); quadratic correction.")
    print(f"  E_QG (ell=D=4.854pm)   = {EQG_D:.3e} eV = {EQG_D/1e3:.0f} keV")
    print(f"  E_QG (ell=a=6.33e-19m) = {EQG_a:.3e} eV = {EQG_a/1e9:.0f} GeV")
    print(f"  Fermi GRB 090510 bound: E_QG,2 > {Fermi:.2e} eV (=1.3e11 GeV)")
    print(f"  CONFLICT: predicted dispersion too strong by {np.log10(Fermi/EQG_D):.0f} orders (D) / "
          f"{np.log10(Fermi/EQG_a):.0f} orders (a).")
    print(f"  => survives ONLY if light is effectively dispersionless (open). GW170817: v_GW=c, |dv|/c<1e-15.\n")

    print("=== C) ANGLE THEORY (exploratory): sin(chi)=lambda/(mD) ===")
    for name, lam in [("gamma 1pm",1e-12),("green 532nm",532e-9),("red 633nm",633e-9),("radio 1m",1.0)]:
        chi, m = chi_deg(lam)
        kind = "longitudinal" if chi < 45 else "near-transverse (light)"
        print(f"  {name:12s}: chi={chi:6.2f} deg  ({kind})")
    print(f"  D-INDEPENDENT (common order): sin(chi_633)/sin(chi_532) = 633/532 = {633/532:.4f}")

    print("\n=== D) 3D fcc lattice (coordination 12): isotropy of the long-wavelength speed ===")
    nb = np.array(sorted({(a,b,0) for a in (1,-1) for b in (1,-1)} |
                         {(a,0,b) for a in (1,-1) for b in (1,-1)} |
                         {(0,a,b) for a in (1,-1) for b in (1,-1)}))
    Kf = mf = 1.0
    omega = lambda kv: np.sqrt((2*Kf/mf)*np.sum(np.sin(nb @ np.asarray(kv, float)/2.0)**2))
    ks = 1e-3
    print(f"  coordination number = {len(nb)}")
    for name, u in {'[100]':[1,0,0], '[110]':[1,1,0], '[111]':[1,1,1]}.items():
        u = np.array(u, float); u /= np.linalg.norm(u)
        print(f"  c along {name} = {omega(ks*u)/ks:.5f}")
    rng = np.random.default_rng(0)
    cs = np.array([omega(ks*(lambda v: v/np.linalg.norm(v))(rng.normal(size=3)))/ks for _ in range(2000)])
    print(f"  2000 random directions: c mean={cs.mean():.5f}, std/mean={cs.std()/cs.mean():.1e} "
          f"(ISOTROPIC; analytic 2*sqrt(K/m)=2)")

    print("\nSTATUS: speed emergence SOLID; vacuum dispersion is the clearest potential FALSIFICATION")
    print("        (8-15 orders vs Fermi) unless light is dispersionless; angle theory exploratory.")

    # ---------- figure: ch2_light.png  (A) speed emergence  (B) dispersion  (C) propagation angle ----------
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15.9, 4.7))
        Ks = np.array([1.,2.,4.,8.,16.]); cs=[pulse_speed(K) for K in Ks]
        a1.plot(np.sqrt(Ks), cs, "o", ms=8, color="#185FA5", label="simulated pulse")
        a1.plot(np.sqrt(Ks), np.sqrt(Ks), "--", color="#D85A30", lw=1.6, label=r"$c=a\sqrt{K/m}$")
        a1.set_xlabel(r"$\sqrt{K}$"); a1.set_ylabel("pulse speed"); a1.set_title(r"(1) speed emergence ($R^2=1$)")
        a1.legend(fontsize=8); a1.grid(alpha=.25)
        k = np.linspace(0, np.pi, 400)
        a2.plot(k, 2*np.abs(np.sin(k/2)), color="#185FA5", lw=2, label=r"$\omega=2\sqrt{K/m}\,|\sin(ka/2)|$")
        a2.plot(k, np.cos(k/2), color="#1C7C3B", lw=2, label=r"$v_g=c\cos(ka/2)$")
        a2.plot(k, k, ":", color="#888888", lw=1.2, label=r"non-dispersive $\omega=ck$")
        a2.set_ylim(0, np.pi); a2.set_xlabel(r"$ka$"); a2.set_ylabel("(units of $c$)")
        a2.set_title(r"(2) lattice dispersion: $v_g=c\cos(ka/2)$"); a2.legend(fontsize=7); a2.grid(alpha=.25)
        EQG_D = E_QG_eV(D); EQG_a = E_QG_eV(a_cell); Fermi = 1.3e20
        a3.bar([0,1,2], [EQG_D, EQG_a, Fermi], color=["#D85A30","#D85A30","#1C7C3B"], width=0.6)
        a3.set_yscale("log"); a3.set_ylim(1e3, 1e22)
        a3.set_xticks([0,1,2]); a3.set_xticklabels(["$E_{QG}$ ($\\ell{=}D$)\n115 keV","$E_{QG}$ ($\\ell{=}a$)\n882 GeV","Fermi bound\n$>$1.3e11 GeV"], fontsize=7.5)
        a3.annotate("", xy=(0,Fermi), xytext=(0,EQG_D), arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.2))
        a3.text(0.2, (EQG_D*Fermi)**0.5, "8-15 orders", rotation=90, va="center", fontsize=8, color="#555555")
        a3.set_ylabel("energy scale (eV)")
        a3.set_title("(3) the conflict (log scale): far below the Fermi bound"); a3.grid(alpha=.25, axis="y")
        plt.tight_layout(); plt.savefig("ch2_light.png", dpi=120, bbox_inches="tight"); plt.close()
        print("  [figure written: ch2_light.png]")
    except Exception as _exc:
        print(f"  [matplotlib unavailable: {_exc}] numbers above are the result.")
