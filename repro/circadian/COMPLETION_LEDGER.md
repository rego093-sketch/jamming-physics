# COMPLETION LEDGER — Chronobiology (circadian_vp_site) · v0.3.0

A gate-by-gate record of what is complete at this version. Status vocabulary is the honest VP set —
`[V]` verified/done, `[L]` locked/cited anchor, `[O]` open (obstacle stated), `[F]` forced form.

## Phase gate
| gate | state | evidence |
|---|---|---|
| research stress battery | **GREEN 8/8** | `repro/_verify/stress_tests.py run_battery()` → all_targets_pass=True |
| research_complete artifact | **WRITTEN** | `reports/research_complete.json` all_green=true |
| PHASE | **writing** | `PHASE` file = `writing`; `gates.writing_locked()` = False |
| determinism | **PASS** | engine result sha256 `417823934d6e…` reproduces 2× identical (seed=19); **byte-identical to v0.2.0** |
| substrate integrity | **PASS** | `vp_substrate.py` byte-identical (vendored) |
| build idempotency | **PASS** | `tools/build_docs.py` re-emits `docs/` byte-identical across rebuilds |

## DOI + retrieval-readiness (v0.3.0 finalisation)
| item | state | note |
|---|---|---|
| concept DOI assigned | [V] | **10.5281/zenodo.20755413** (resolves to latest); v0.2.0 snapshot 10.5281/zenodo.20755414, CC BY 4.0 |
| DOI wired across site | [V] | JSON-LD identifier + isPartOf.sameAs on all 10 pages; claim-strip "DOI snapshot"; footers; hub note/footer; llms.txt (63 occurrences) |
| cross_volume_doi registry | [V] | `registry/cross_volume_doi.{csv,md}` — self entry (concept+version) + cited mind seam (SIGN-only firewall) |
| JSON-LD 6-R.4 chapter schema | [V] | ScholarlyArticle + identifier + datePublished/dateModified + isBasedOn + per-chapter knowsAbout; isPartOf=CreativeWorkSeries(sameAs DOI) |
| JSON-LD hub schema | [V] | CreativeWorkSeries + hasPart (9 chapters) + identifier/sameAs DOI + datePublished + inLanguage + BreadcrumbList |
| Google Scholar citation tags | [V] | hub Highwire citation_title/_author/_publication_date/_doi/_fulltext_html_url/_abstract_html_url/_language |
| SEO meta | [V] | per-page keywords (base + per-chapter), author, robots, link rel=license, Open Graph + Twitter card |
| JSON-LD validity | [V] | 20/20 blocks parse (2 per page × 10) |
| _meta.json (VP-SPEC §9) | [V] | `docs/circadian/_meta.json` — DOI, measured-input block, headline results, 9 chapters, totals (5539 words) |

## Writing deliverables (canonical site, 10 pages)
| item | state | note |
|---|---|---|
| hub `docs/circadian/index.html` | [V] | grounding callout + thesis + disease/treatment axis + mind seam + chapter list + citation tags |
| **§0 grounding (NEW)** | [V] | 975 words; measured-DNA emergence, determinism hash, 8 falsifiable discriminants, [V]/[L]/[O] triad — the "not a toy" page |
| §1 scope | [V] | 682 words; oscillator-not-timer; measured γ; period anchor |
| §2 free-running (RC1) | [V] | 478 words |
| §3 entrainment/PRC (RC2) | [V] | 561 words |
| §4 master-vs-network (RC3) | [V] | 475 words |
| §5 setpoint gating (RC4) | [V] | 509 words |
| §6 misalignment/disease (RC5) | [V] | 578 words; 3 named diseases |
| §7 circadian–mood seam (RC6) | [V] | 641 words; the inheritance keystone |
| §8 chronotherapy (TX1) | [V] | 640 words; efficacy=0 |
| answer-first / claim-strip / vp-cards | [V] | present in all 10 pages; claim-strip carries reproduce + DOI snapshot links |
| site.css vendored | [V] | 2723 bytes, verbatim |
| robots / sitemap / llms / llms-full | [V] | 8 crawlers; sitemap 10 URLs; grounding one-liner + DOI in llms |
| manifest CSV | [V] | 9 rows (consistent with _meta.json) |
| numbers pulled live from engine | [V] | build_docs reads research_findings(); no hand-typed values |
| page weight / DOM | [V] | every page <300KB and <3000 DOM nodes |

## Research deliverables (engine) — UNCHANGED from v0.2.0
| item | state | note |
|---|---|---|
| BMAL1 γ measured + vendored | [V] | γ=1.33348, gene 406, NC_000011.10, seq sha256 7293be92…; DNA NN pipeline, never fitted |
| RC1 free-running + block control | [V]/[L] | 76 cycles, cv=0.003691; block→1 beat |
| RC2 PRC + Arnold tongue | [V] | adv 0.185022 / delay −0.129012; locking range 5→15 |
| RC3 synchronisation + master-led | [V] | coherence 0.596→0.99993; drift 0.003823→0.002956 |
| RC4 HPA setpoint gating | [V]/[L] | gated 0.976237 vs ablated 0.0; mind-cited kinetics, no new constant |
| RC5 misalignment | [V] sign | signed amp 1.227923→−1.364039; reentrain 0→12 cyc |
| RC6 circadian–mood seam | [V] sign / [O] mag | flattening 0→2.11085; supplies mind's locked contributor |
| TX1 chronotherapy | [V] dir / eff=0 | corrected 2.56→0 h; worsened 5.44→11.2 h |
| 5 pathology failures wired | [V] | sleep-wake; shift-work metabolic/CV; IARC-2A cancer; misalignment depression; autism cross-ref |
| mind seam params (cited) | [L] | `inherited/mind_seam.json`; firewall SIGN-only, efficacy=0, magnitude [O], consciousness_claim=0 |

## Governance (four-document SSOT)
| doc | state |
|---|---|
| CHANGELOG.md | [V] written (v0.3.0 entry at top) |
| MASTER_MANUAL.md | [V] updated (v0.3.0) |
| COMPLETION_LEDGER.md | [V] this file |
| HANDOVER_v0_3_0_to_v0_4_0.md | [V] written (v0_2_0_to_v0_3_0 consumed) |
| VERSION 0.3.0 | [V] |
| CHARTER.md / START_HERE.md / docs/README.md | [V] DOI status updated (TBD → assigned) |
| IRREPRODUCIBILITY_LEDGER.md | [V] current (no new [O]; BMAL1 resolved, open items carry obstacles) |
| registry/cross_volume_doi.{csv,md} | [V] created |

## Open (carried forward — see HANDOVER + ledger)
- absolute circadian phase, inter-tissue SCN→periphery lags — [O], substrate has no wall-clock zero.
- absolute incidence / RR magnitude (sleep-wake, shift-work cardiometabolic, night-shift cancer) — [O], needs
  external epidemiological calibration.
- circadian→depression handle magnitude, per-pulse chronotherapy gain — [O], owned by mind / firewalled to
  efficacy=0.
- Author follow-ups (not blocking the site): enrich the Zenodo record metadata (human title/description/keywords
  to match the canonical title); add isDescribedBy → hub URL on the Zenodo record (VP-SPEC §12.B); PDF is a
  next-version deliverable (§12.C).
