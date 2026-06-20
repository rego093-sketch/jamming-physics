# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL.

| item | grade | obstacle | location |
|---|---|---|---|
| absolute basal metabolic rate (endothermy cost) | [O] | the ~5–10× resting-rate ratio is reproduced/cited [V]/[L]; the absolute W/kg needs an external calorimetry calibration the R19 substrate (model units) does not contain | engine `endothermy_cost` / RT3 |
| Kleiber 3/4-power exponent | [O] | the substrate sets setpoint dynamics, not the transport-network (fractal distribution) geometry the 3/4 exponent is argued from; named open, not faked | engine `kleiber_status` / RT5 |
| absolute torpor metabolic-rate drop | [O] | the bistable SWITCH + hysteresis reproduces [V]; the absolute metabolic-rate drop needs species calibration | engine `torpor_hysteresis_sweep` / RH1 |
| silenced torpor-switch regulatory gating | [O] | the cross-species reads place the genes [V] (present-but-silenced); the regulatory gating circuitry is not derived from the promoter read | engine `null_pdk4…` / RH4, §11 |
| ADRB3 command absence across all ectotherms | [O] | symbol orthology across distant taxa is itself uncertain; the queried-assembly observation is [L], the universal claim is [O] | engine `gene_criterion` / §2 |
| absolute disease incidence rate | [O] | the attractor-shift / setpoint-drift SHAPE reproduces [V]; absolute incidence needs calibrating the model chronic-forcing axis to clinical (epidemiological) units | `_pathology/setpoint_failure.py` / §16–§18 |
| PDK4 co-upregulation in torpor & insulin resistance | [O] | the R19 framing (defended low setpoint vs chronic crossing) is [V]; the co-upregulation biology is CITED, not derived | `_engine hibernation_bridge` / RD4, §19 |
| no promoter γ marks hibernation across the 8-gene panel (the panel-level conclusion) | [O] | the reads and the GC confound are [V] (parameter-free: per-gene sign agreement + near-unit cross-gene slope r(Δγ,ΔGC)=0.9957); the CONCLUSION that no promoter marks hibernation is open — small n, species are not phylogenetically independent draws, and the regulatory gating that DOES carry the capability is cited biology, not derived from the promoter read | engine `null_torpor_panel_gamma_does_not_track_hibernation` / RH8, §11.1 |
| no STATIC promoter read marks hibernation (RH9 methylation-substrate panel-level conclusion) | [O] | the CpG-O/E reads, the γ↔CpG-O/E dissociation (cross-cell r=0.5601), and the GC-loading contrast (r(CpG O/E,GC)=0.4927 vs γ 0.9955) are [V] (parameter-free, re-derivable from the same cache); the CONCLUSION that NO static promoter read marks hibernation is open — small n, phylogenetic non-independence, and even a second GC-normalized static layer cannot see the gating, which is DYNAMIC and cited, not derived | engine `null_cpg_oe_does_not_track_hibernation` / RH9, §11.2 |
| the DYNAMIC torpor methylation/expression contrast (where the present-but-silenced gating is actually read) | [O] external | RH9 closes the STATIC sequence layers (γ and CpG-O/E); the genuine regulatory read is an in-vivo torpor↔euthermia differential expression / methylation contrast (cited: hibernation expression atlases and torpor methylation dynamics), which is Layer-2 and NOT a static promoter property. The package's offline-reproducibility invariant precludes vendoring processed in-vivo data in-package — this is the named honest next step, not a stub and not faked | engine `CITED_DYNAMIC_REGULATION` / RH9, §11.2 |
| all restoration clinical magnitudes (potency/dose/efficacy/safety) | [O] | γ reads promoter switch-threshold STRUCTURE only; every clinical magnitude is Layer-2, asserted nowhere (firewall); S3 mechanism link is [O] cited | `_pathology/restoration_levers.py` / §S1–§S3 |
| central appetite-axis (MC4R / hypothalamus) deliverability | [O] | the compartment is single and cited [F] (PRECISION routing), but REACHING it requires crossing the blood-brain barrier — a penetrance obstacle the routing geometry does not assert; routability ≠ deliverability | `_pathology/precision_routing.py` / §R, §RM |
| BAT-depot deliverability (UCP1 / ADRB3 brown-fat route) | [O] | the BAT compartment is cited [F] (the cleanest precision route), but adult-human brown-fat depot quantity is small and variable, so targeted delivery is an [O] obstacle, not a solved magnitude | `_pathology/precision_routing.py` / §RM |
| INSR distributed routability (the ubiquitous insulin receptor) | [O] | INSR is honestly SYSTEMIC (4 dominant compartments); restoration cannot be confined to one locus, so a single-compartment "precision" route does not exist for it — named, not oversold | `_pathology/precision_routing.py` / §RM |
| TNF distributed routability (a body-wide inflammatory program) | [O] | TNF is a distributed immune/stromal node with no single anatomical locus → SYSTEMIC by construction; there is no precision compartment to route to, and the routing map says so explicitly | `_pathology/precision_routing.py` / §RM |

> **Resolved at v0.3.0:** the torpor/hibernation master γ is no longer `[O]→[V]` deferred — PDK4 was
> fetched and promoted to **measured [V]** (γ=1.4112, NC_000007.14) via the identical DNA pipeline, and the
> cross-species panel re-derives offline bit-for-bit. No named master remains unmeasured.

> **v0.4.0 note:** no open item was newly resolved this version; instead the hibernation NULL (RH4, one
> gene) was GENERALIZED to the whole 8-gene torpor/BAT program across 14 species (RH8). The result is a new
> [O] conclusion (logged above): 0/8 promoter reads mark hibernation, and the group γ gaps ARE GC gaps. The
> firewall holds at panel scale — γ reads structure, not who can hibernate.

> **v0.5.0 note:** again no open item is newly resolved; instead the firewall is sharpened by closing a
> SECOND static sequence layer. RH9 reads the methylation SUBSTRATE (CpG observed/expected, GC-normalized)
> of the same panel and finds it ALSO fails to separate hibernators (0/8), while being a genuinely distinct
> read from γ (cross-cell r=0.5601). Two new [O] rows are logged (the RH9 panel-level conclusion, and the
> DYNAMIC torpor methylation/expression contrast as the named external next step). The cross-species panel
> and every read γ value are byte-identical — RH9 is computed from the cache already on disk, no fetch.

> **v0.6.0 note:** no open item is newly resolved; instead the precision-routing layer makes the restoration
> DELIVERABILITY obstacles explicit and graded. Four new [O] rows are logged — central (MC4R/BBB) access, the
> BAT-depot access, and the no-single-locus routability of the two distributed SYSTEMIC nodes (INSR, TNF). The
> routing geometry itself is [F] cited anatomy and parameter-free (specificity = 1/compartment-count), and the
> firewall is now PROVEN, not asserted: `gamma_independence_gate()` recomputes the whole map under a perturbed
> γ atlas and confirms the routing fields are byte-identical while only the carried γ-context moves. The
> engine, the panel, and every read γ value are byte-identical — the layer reads the γ atlas read-only and
> touches neither the panel nor the substrate.
