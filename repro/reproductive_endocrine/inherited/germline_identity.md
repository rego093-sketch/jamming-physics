# Germline / gamete-program identity (RECEIVED from DNA, then read-only)

The v0.4.x package emerged the reproductive **organs** and the HPG / germline **rhythms** but never opened
the germ cell itself. The gamete chapter (§11, module `repro/_germline/`) answers four questions — *how* a
gamete is made, *whether* gametes are identical, the *sperm* motility logic, the *egg* logic — each as a
discriminant against the shared substrate (R19 switch + FHN relaxation oscillator). The only NEW input is the
**measured promoter γ** of the gamete machinery, received through the identical DNA pipeline used for the
organ masters (NN-stacking ΔG37, SantaLucia 1998; promoter window TSS−2000…+500; GRCh38.p14 =
GCF_000001405.40). Sequences are cached in `inherited/germline_promoters.cache.json` for offline bit-for-bit
reproduction; γ values are read-only and **never fitted**.

The panel was declared **by function, before any γ was seen** (no cherry-picking), and the reception refuses
to persist unless BOTH vendored anchors reproduce exactly: SOX9 (1.4598) and the v0.4.x germline master
DAZL (1.3803).

| master gene | module | measured γ | role in the gamete program |
|---|---|---|---|
| TEKT1 | sperm | 1.3400 | tektin-1 flagellar structural filament |
| NLRP5 | oocyte | 1.3475 | maternal-effect (subcortical maternal complex) |
| MOS | oocyte | 1.3619 | c-Mos cytostatic factor (metaphase-II arrest) |
| **DAZL** | germline | **1.3803** | germline master (gametogenesis) — vendored v0.4.x anchor |
| CATSPER1 | sperm | 1.4019 | CatSper Ca²⁺ channel (hyperactivation gain switch) |
| DMC1 | meiosis | 1.4056 | meiotic recombinase (homolog strand invasion) |
| MLH1 | meiosis | 1.4085 | crossover maturation / resolution (MutLγ) |
| SPO11 | meiosis | 1.4105 | meiotic DSB catalyst (initiates recombination) |
| PRDM9 | meiosis | 1.4165 | recombination-hotspot designator (writes the CO map) |
| ZAR1 | oocyte | 1.4226 | zygote arrest 1 (oocyte-to-embryo transition) |
| DNAH1 | sperm | 1.4469 | axonemal dynein heavy chain (the 9+2 motor) |
| ZP3 | oocyte | 1.4486 | zona pellucida glycoprotein 3 (sperm receptor) |
| REC8 | meiosis | 1.4525 | meiotic cohesin (reductional vs equational release) |

> **What γ is used for, and what it is NOT.** γ enters the dynamics only where a measured master *names* a
> mechanism the substrate already owns: REC8 γ → the spinodal of the ordered two-stage cohesin release (G1);
> CATSPER1 γ → the CatSper gain context for hyperactivation (G3); MOS γ → the cytostatic hold of the
> metaphase-II switch (G4). The qualitative results (meiosis = one replication + two ordered divisions;
> assortment = 2²³; interference = the substrate refractory period mapped onto the chromosome axis;
> fertilisation = a one-way supra-spinodal flip; polyspermy block = past-spinodal irreversibility;
> sperm/egg = oscillator vs held switch) are **structural** and do not depend on the γ values.
>
> **Pre-registered γ test (G5), reported as it falls.** A permutation test of whether γ *separates* the three
> functional modules (meiosis / sperm / oocyte) is run against shuffled labels, with the null permitted and
> reported; a positive sub-test asks only whether the recombination CORE (SPO11/DMC1/MLH1/PRDM9, which
> clusters tightly ≈1.406–1.417) is tighter than random 4-gene subsets. No claim is graded **[V]** on the
> strength of γ separation unless the test supports it.
>
> **SSOT.** The gamete-program genes and their γ are RECEIVED from DNA and live here read-only. γ changes at
> the DNA source and propagates by re-vendoring — never edited locally. The reception was a measurement
> (cached), not a fit. Honest grades travel with each result in `gametogenesis.py` ([V] / [L] / [O]).
