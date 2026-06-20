#!/usr/bin/env python3
"""
build_registry.py — VP_SPEC v1.8 §2 cross-volume DOI registry.

Single source for the 9-paper sibling table; emits registry/cross_volume_doi.csv
(machine index loaded by every work session) and .md (human notes incl. latest
resolved DOIs and site slugs). Transcribed from VP_SPEC_v1_8 §2; author and ORCID
are common to all volumes.
"""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "registry"
REG.mkdir(exist_ok=True)

AUTHOR = "Young Jae Lee"
ORCID = "0009-0002-7535-8245"

# paper_id, code, title_en, short, doi_concept, headline, relation, latest_doi, slug
ROWS = [
    ("physics", "phy", "The Vacuum as a Jammed Elastic Solid, and the Speed of Light as Its Elastic-Wave Speed",
     "VP Theory", "10.5281/zenodo.17932566",
     "c² = B/ρ ; m_p/m_e = 6π⁵ (−19 ppm)", "foundation", "", "/physics"),
    ("fluid-dynamics", "flu", "The Configured Continuum",
     "Configured Continuum", "10.5281/zenodo.17972568",
     "∂ρ/∂t + ∇·(ρu) = 0 ; ρ Du/Dt = ∇·T", "jamming branch", "", "/fluid-dynamics"),
    ("cosmology", "cos", "Gravity, Galaxies, and Cosmology as Vacuum Inflow",
     "Vacuum-Inflow Cosmology", "10.5281/zenodo.20568874",
     "a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻²", "inflow branch", "", "/cosmology"),
    ("geodynamics", "geo", "A Jamming–Unjamming Mechanism for Rapid Continental Break-up",
     "Jamming Geodynamics", "10.5281/zenodo.17978934",
     "Ψ_eff > Ψ_y", "convergence (jamming+chronology)", "", "/geodynamics"),
    ("dna", "dna", "A Deterministic Two-Layer Interpretation of DNA",
     "4D DNA Blueprint", "10.5281/zenodo.20471407",
     "form ← γ (Layer 1) ; quantity ← φ (Layer 2)", "jamming branch", "", "/dna"),
    ("geochronology", "chr", "Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit",
     "Cross-Chronometer Limit", "10.5281/zenodo.20568673",
     "foreign (old) incorporation ⇒ age-old bias", "methodology (supports convergence)", "", "/geochronology"),
    ("chemistry", "chm", "VP Chemistry & Electromagnetism: Derived from a Single Anchor on the Jamming-Lattice Substrate",
     "VP Chemistry & EM", "10.5281/zenodo.20680540",
     "c²=B/ρ (0.06% sim) ; arccos(−1/3) ; φ_RCP=0.7405 ; d-band catalysis",
     "jamming branch (cites physics Vol I)", "10.5281/zenodo.20680541", "(unconfirmed)"),
    ("neuro", "neu", "From Ion Channels to Behaviour: A Falsifiable Neural Emergence Chain",
     "Neural Emergence Chain", "10.5281/zenodo.17979015",
     "working-memory capacity ≈ θ/γ (7±2), tACS causal",
     "branch (self-contained chain)", "10.5281/zenodo.20694299", "/neuro"),
    ("mind", "mnd", "Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience",
     "Felt Cognition", "10.5281/zenodo.20694404",
     "stream = θ-frame serial selection ; hard problem OPEN",
     "frontier (cites neuro, one-way)", "10.5281/zenodo.20694405", "/mind"),
]

COLS = ["paper_id", "code", "title_en", "short", "doi_concept",
        "headline", "relation", "author", "orcid"]


def build_csv():
    with open(REG / "cross_volume_doi.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for r in ROWS:
            pid, code, title, short, doi, head, rel, latest, slug = r
            w.writerow([pid, code, title, short, doi, head, rel, AUTHOR, ORCID])
    return "registry/cross_volume_doi.csv"


def build_md():
    L = ["# Cross-Volume DOI Registry",
         "",
         f"Sibling white-papers of the Jamming Physics program. Common author: "
         f"**{AUTHOR}** (ORCID [{ORCID}](https://orcid.org/{ORCID})). "
         "Concept DOIs resolve to the latest version; this registry is the single "
         "table every work session consults (the original sites are not re-surveyed).",
         "",
         "| paper_id | code | short | concept DOI | latest DOI | site slug | relation |",
         "|---|---|---|---|---|---|---|"]
    for r in ROWS:
        pid, code, title, short, doi, head, rel, latest, slug = r
        latest_disp = latest if latest else doi.split("/")[-1] + " (= concept)"
        L.append(f"| `{pid}` | {code} | {short} | "
                 f"[{doi}](https://doi.org/{doi}) | {latest_disp} | `{slug}` | {rel} |")
    L += ["", "## Headline results", ""]
    for r in ROWS:
        pid, code, title, short, doi, head, rel, latest, slug = r
        L.append(f"- **{short}** — {title}. {head}")
    L += ["",
          "## Notes",
          "",
          "- The cosmology volume (`cos`) is the subject of this package; its "
          "headline locked result is a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻².",
          "- v1.7 added chemistry · neuro · mind; their latest-version DOIs "
          "(chemistry→20680541, neuro→20694299, mind→20694405) were confirmed "
          "on Zenodo 2026-06-15. Chemistry site slug is not yet confirmed.",
          "- All volumes share the no-tuning LOCK→derive→gate governance and "
          "CC BY 4.0 licensing.", ""]
    (REG / "cross_volume_doi.md").write_text("\n".join(L), encoding="utf-8")
    return "registry/cross_volume_doi.md"


if __name__ == "__main__":
    print(build_csv())
    print(build_md())
    print(f"rows: {len(ROWS)}")
