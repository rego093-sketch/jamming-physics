# START HERE — increment E5 (the READOUT substrate: otoferlin / auditory neuropathy)

**One-line goal.** Turn E4's honest **[O]** — the synaptic READOUT layer the transduction cubic cannot
see — into a **modelled** failure: emerge the downstream Ca²⁺-sensor (otoferlin / OTOF) as a substrate
**distinct from** the R19 cubic, compose it with the frozen switch, and reproduce **auditory neuropathy**.

## Why this increment exists
E4 decomposed congenital deafness into four classes (drive `h` / structure `g` / readout downstream /
amplifier `g→0`). Three were modelled; the **readout** class (OTOF) was left **[O]** — "the cubic is the
wrong layer." E5 supplies the right layer and shows the OTOF phenotype falls out of the cascade.

## What it delivers (all in this folder)
- `run.py` — the deterministic module (self-hashing, 2×sha256). Imports the **frozen** `vp_substrate`
  cubic + E1's `read_measured`; **edits no inherited byte** and triggers **no re-freeze**.
- `gate.py` — the standalone gate (G1–G7).
- `FINDINGS.md` — results + six honest negatives.
- `START_HERE.md` — this card.

## The result in one paragraph
The readout layer **cannot be the cubic** — release is non-negative, monotone, saturating, and
**non-bistable**, so the minimal form is a rectified saturating Ca²⁺ sensor (a different substrate). That
is the provable reason E4's cubic is blind to OTOF. Composing the sensor with the frozen switch:
**(1)** a sound flips the switch to **s=+1.3864 — identical in a hearing and an OTOF ear** — but the
removed sensor zeroes release (auditory neuropathy = normal switch, silent nerve); **(2)** the auditory-
nerve rate inherits the **composed exponent F^(m/3)** = E3 amplifier cube-root (1/3) × synaptic
cooperativity m (cited [L]); **(3)** the **OAE⁺/ABR⁻** clinical signature is forced because the amplifier
(E3, OHC) and the readout (E5, IHC synapse) are **separable stages**. The lever direction — left [O] by
E4 — is now forced: **restore the readout stage**, not the switch.

## How to run / verify
```
python3 research/E5-readout-synapse/run.py     # prints the emergence; ends with 'sha256: …'
python3 research/E5-readout-synapse/gate.py    # 'E5 GATE: PASS' iff all 7 hold
python3 tools/verify_seed.py                   # whole-seed gate; E5 is in the foundation list
```

## Firewall (binding)
γ reads promoter **structure only** — never a Ca²⁺-sensor affinity, a release rate, a dose, or an effect.
The disease layer is **proposal-only / direction-only**; no molecule, dose, or efficacy; nothing
diagnosed or treated. The cooperativity m is a **cited knob [L]**, never derived or tuned. The felt
percept of hearing is the **mind** volume's. Every magnitude is **[O]** with its obstacle named.
