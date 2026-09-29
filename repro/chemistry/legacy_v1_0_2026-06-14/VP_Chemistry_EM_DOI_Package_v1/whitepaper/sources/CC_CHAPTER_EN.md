# The Color of Molecules: From *d*-Orbitals to Paint Pigments

**VP Chemistry & Electromagnetism Whitepaper — Chapter CC**
DOI (reserved): 10.5281/zenodo.20680541 · Builds on Chapter EM (light), Chapter CH §CH.5
(crystal field), and Chapter CM. Numbers reproduced by `vp_molecular_color.py` (and
`vp_crystal_field.py`); deterministic, standard-library, self-checking.

> Color is a subtraction. White light arrives; the molecule removes the photons whose energy
> matches an electronic gap, and what is left — transmitted or reflected — is the color we see.
> Four different gaps give the four families of molecular color, but the rule is one: a gap the
> size of a visible photon makes a colored substance.


## CC.0 The question

Why is copper sulfate blue, a carrot orange, cadmium-yellow paint yellow, and titanium-white paint
white? This chapter derives the color of molecules and pigments from the electromagnetism of
Chapter EM: visible light is the transverse electromagnetic wave (§EM.6), and **color is which
visible photons a substance absorbs**, set by the size of an electronic energy gap.


## CC.1 The principle — color is selective absorption **[F]**

A substance has color when its electronic structure absorbs *part* of the visible spectrum
(400–700 nm). An absorbed photon (a transverse light quantum) lifts an electron across an electronic
**gap**; the gap size fixes which wavelength is absorbed, and the remaining light is the perceived
color. For dissolved molecules the eye sees the **complementary** of the absorbed band; for opaque
pigments it sees the **reflected** band. Two limits frame the rest: a gap *larger* than any visible
photon absorbs nothing (white or colorless), and a gap *smaller* than every visible photon absorbs
everything (black).


## CC.2 Energy and wavelength **[F]**

The bridge is the photon relation of Chapter EM,
$$ E = \frac{hc}{\lambda}, \qquad \lambda[\mathrm{nm}] = \frac{1240}{E[\mathrm{eV}]}. $$
Visible light spans $E = 1.77\ \mathrm{eV}$ (red, 700 nm) to $3.10\ \mathrm{eV}$ (violet, 400 nm).
A gap in this energy window produces color; outside it, the substance is white/colorless (gap too
large) or black (gap too small).


## CC.3 Mechanism 1 — *d*–*d* transitions (transition-metal complexes) **[F]/[CAL]/[O]**

In a transition-metal complex the ligands' electromagnetic $1/r^2$ field splits the geometric
$d$-orbitals by the crystal-field gap $\Delta$ (Chapter CH §CH.5). An electron absorbs a photon to
cross $\Delta$:
$$ \lambda_{\text{abs}}[\mathrm{nm}] = \frac{10^7}{\Delta[\mathrm{cm}^{-1}]}. $$
For $[\mathrm{Ti}(\mathrm H_2\mathrm O)_6]^{3+}$ ($d^1$, single transition), $\Delta = 20300\
\mathrm{cm^{-1}}$ gives $\lambda_{\text{abs}} = 493\ \mathrm{nm}$ (blue-green absorbed) → reddish
violet, matching observation (`vp_molecular_color.py`, §1). The mechanism — color *is* the $d$–$d$
gap — is forced by VP geometry **[F]**; the spectrochemical ordering of $\Delta$ is calibration
**[CAL]**; and for multi-electron ions ($d^9$ Cu²⁺, $d^8$ Ni²⁺) the single-$\Delta$ point model is
insufficient (broad multi-band absorption tails into the red, giving the real blue/green), an
honestly **[O]** limitation. Weak-field ligands give a small $\Delta$ (red absorption); strong-field
ligands a large $\Delta$ (blue absorption).


## CC.4 Mechanism 2 — conjugated $\pi$ systems (organic dyes) **[F]/[F?]**

In a conjugated polyene the $\pi$-electrons behave as a free electron gas in a one-dimensional box of
length $L$ (the conjugation length). The levels are $E_n = n^2 h^2/(8 m_e L^2)$; with $N = 2k$
electrons ($k$ double bonds) filling levels up to $k$, the HOMO→LUMO gap is
$$ \Delta E = \frac{h^2}{8 m_e L^2}\,(N+1). $$
Because $L$ grows with conjugation, **the gap shrinks and the absorption red-shifts** — the derived
trend (`vp_molecular_color.py`, §2): short polyenes (ethene, butadiene, hexatriene) absorb in the
ultraviolet and are colorless, while extended conjugation (β-carotene, 11 double bonds) absorbs in
the visible and is colored (orange; lycopene, red). The scaling $\Delta E \propto (N+1)/L^2$ and the
UV→visible crossover are forced **[F]**; the absolute wavelengths from the free-electron model
overestimate for long chains (bond alternation caps the gap), so the model's numbers are trend-only
**[F?]**. This is why carrots and tomatoes are colored: long $\pi$-conjugation pulls the gap down
into the visible.


## CC.5 Mechanism 3 — the band gap (inorganic pigments and paint) **[F]/[CAL]**

A solid pigment is a semiconductor with a band gap $E_g$. Photons with $E > E_g$ (wavelength below
the absorption edge $\lambda_{\text{edge}} = hc/E_g$) are absorbed; photons with $E < E_g$ (longer
wavelength) are reflected, and **the reflected band is the color**. As $E_g$ decreases, the edge
sweeps across the visible and the pigment runs **white → yellow → orange → red → black**
(`vp_molecular_color.py`, §3):

| pigment | $E_g$ (eV) | edge (nm) | reflected color |
|---|---|---|---|
| TiO₂ titanium white | 3.05 | 407 | white (all visible reflected) |
| ZnO zinc white | 3.20 | 387 | white |
| As₂S₃ orpiment | 2.70 | 459 | yellow (violet/blue absorbed) |
| CdS cadmium yellow | 2.42 | 512 | yellow |
| CdS·Se cadmium orange | 2.10 | 590 | orange/red |
| HgS vermilion (cinnabar) | 2.00 | 620 | red |
| Fe₂O₃ red ochre (hematite) | 2.10 | 590 | red |
| CdSe cadmium red | 1.73 | 717 | red (only deep red reflected) |
| carbon black | ~0.5 | — | black (all visible absorbed) |

The same single rule $\lambda_{\text{edge}} = hc/E_g$ orders the entire cadmium pigment series and
the historical mineral pigments (vermilion, orpiment, hematite) **[F]**, with $E_g$ a measured
material constant **[CAL]**. This is the physics of paint: **the band gap is the color knob.**
Titanium white reflects everything because its gap (3.05 eV) sits just past the violet edge; cadmium
red absorbs nearly all visible because its gap (1.73 eV) sits at the red edge.


## CC.6 Mechanism 4 — charge transfer (intense colors) **[F]/[CAL]**

When a photon moves an electron between a metal and a ligand (ligand-to-metal or metal-to-ligand
charge transfer), the transition is fully allowed and therefore **intense** — 100–1000× stronger than
a $d$–$d$ transition, so a trace gives a deep color. Permanganate $\mathrm{MnO_4^-}$ absorbs
$\sim 525\ \mathrm{nm}$ (O→Mn charge transfer) and is deep purple; dichromate
$\mathrm{Cr_2O_7^{2-}}$ is orange; Prussian blue is an Fe²⁺↔Fe³⁺ charge transfer
(`vp_molecular_color.py`, §4). The mechanism is the same electron-across-a-gap; only the gap's origin
(metal↔ligand) and its allowedness differ.


## CC.7 White, black, and everything between **[F]**

The two achromatic limits follow from the same rule and require no extra assumption:

- **White**: gap larger than any visible photon ($E_g > 3.1\ \mathrm{eV}$, edge in the ultraviolet).
  No visible light is absorbed; all is reflected. Titanium white, zinc white, table salt, snow.
- **Black**: gap smaller than every visible photon ($E_g < 1.8\ \mathrm{eV}$, edge in the infrared).
  All visible light is absorbed. Carbon black, graphite.
- **Color**: gap inside the visible window. The substance absorbs the short-wavelength side of the
  edge and shows the long-wavelength side.

So white and black are not "colors added" but the two ends of where the gap sits relative to the
visible band.


## CC.8 The unifying picture

All four families are one mechanism — **a transverse visible photon absorbed by lifting an electron
across an electronic gap** — differing only in what sets the gap:

- $d$–$d$: the crystal-field splitting $\Delta$ (ligand electromagnetic $1/r^2$ field).
- conjugated $\pi$: the HOMO–LUMO gap $\propto (N+1)/L^2$ (conjugation length).
- band gap: the semiconductor $E_g$ (the pigment's electronic structure).
- charge transfer: the metal↔ligand donor–acceptor gap.

The absorbing light is the transverse electromagnetic wave of Chapter EM ($\chi\to 90^\circ$); only a
photon whose energy matches the gap is absorbed (resonance), and the gap size determines the
wavelength and hence the color. One principle — gap-sized absorption — and four ways nature builds
the gap.


## CC.9 Falsification and reproducibility **[F]**

- If a transition-metal complex's color did not track its crystal-field $\Delta$ (weak-field red,
  strong-field blue absorption), the $d$–$d$ account fails.
- If extending $\pi$-conjugation did not red-shift absorption (UV for short, visible for long), the
  particle-in-a-box account fails.
- If a semiconductor pigment's color did not follow its band-gap edge $\lambda_{\text{edge}} =
  hc/E_g$ (large gap white, small gap black, intermediate colored), the band-gap account fails — this
  is tested across the cadmium series and historical pigments.

```
python3 code/foundation/vp_molecular_color.py    # complementary color, d-d, FEM, band-gap pigments
python3 code/foundation/vp_crystal_field.py      # crystal-field Δ and 4/9
```

Both modules are deterministic (stdout sha256 identical on re-run) and standard-library only.


*Color completes the optical arc of Chapter EM: light emerges from the lattice, refraction and the
rainbow split it by wavelength, and here matter *subtracts* selected wavelengths by lifting electrons
across gaps — crystal-field, conjugation, band-gap, and charge-transfer gaps — so that a carrot is
orange and titanium-white is white for the same reason, read through the size of a gap.*
