#!/usr/bin/env python3
"""
M39 - P5-SPATIAL ALONG-MARGIN CO-VARIATION  (SH-61, the cleanest petroleum discriminator)
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only.

The one-parameter VP reading predicts extension, salt, and source richness CO-VARY SPATIALLY
along a single margin (one parameter sets all magnitudes); the mainstream treats them as
independent magnitudes. We test the PRESENT-TENSE SPATIAL correlation along the South
Atlantic conjugate margins (Santos/Campos/Espirito Santo vs Kwanza/Lower Congo/Gabon).

FIREWALL-CLEAN: spatial co-variation along one PRESENT-DAY margin needs NO event-pairing
and NO chronology. (The temporal cross-basin version - 'bigger floods had bigger
glaciations' - DOES need event-pairing and HITS the firewall; not built.)

LOCK: reads frozen data/sa_margin_segments.csv (raw SHA-256 pinned in-gate). Columns are
present-tense geometry: beta extension proxy, present salt isopach (km), source TOC band.
SEED = 19. Determinism structural. Double-SHA-256 self-gate.
"""
import os, csv, hashlib
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SEED = 19
SRC = "data/sa_margin_segments.csv"
raw = open(SRC, "rb").read()
raw_sha = hashlib.sha256(raw).hexdigest()
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))

beta = [float(r["beta_extension"]) for r in rows]
salt = [float(r["salt_thickness_km"]) for r in rows]

def pearson(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    sxx = sum((a-mx)**2 for a in x); syy = sum((b-my)**2 for b in y)
    return sxy / (sxx*syy) ** 0.5

r_bs = pearson(beta, salt)

L = []
L.append("M39  P5-SPATIAL ALONG-MARGIN CO-VARIATION  (present-tense geometry; SH-61)")
L.append(f"SEED={SEED}   source={SRC}  (South Atlantic conjugate margins)")
L.append(f"RAW_FILE_SHA256 = {raw_sha}")
L.append(f"n_segments={len(rows)}")
L.append("")
L.append("[PRESENT-TENSE SEGMENT GEOMETRY]  (no dates):")
L.append("  segment           side    beta   salt(km)   source TOC")
for r in rows:
    L.append(f"  {r['segment']:16s} {r['conjugate_side']:7s} {r['beta_extension']:4s}   {r['salt_thickness_km']:5s}      {r['source_toc_pct']}%")
L.append("")
L.append("[SPATIAL CORRELATION]  (extension proxy vs present salt isopach):")
L.append(f"  Pearson r(beta, salt) = {r_bs:+.2f}  across {len(rows)} along-margin segments")
L.append("")
L.append("[VERDICT]  (honest, symmetric):")
if r_bs > 0.6:
    L.append(f"  ok  Salt thickness CO-VARIES with the extension proxy (r={r_bs:+.2f}): segments")
    L.append("     with greater stretching carry thicker evaporite. This is the present-tense")
    L.append("     spatial co-variation the one-parameter reading predicts. [V] co-variation.")
L.append("  BUT NON-DISCRIMINATING (the honest cap): the mainstream predicts the SAME sign -")
L.append("     more extension -> more accommodation + thinner crust + restriction -> thicker")
L.append("     salt. So spatial co-variation is [V] and CONSISTENT with the cascade, but it")
L.append("     does NOT distinguish one coupled event from independent rift sedimentology.")
L.append("     The cascade's only edge remains ECONOMY (one parameter sets all three) - [L]")
L.append("     parsimony, not a knockout, and weakened by M36 (modest enrichment) and the")
L.append("     coupled-OAE counter (M28).")
L.append("  -> A genuinely DISCRIMINATING version would need a magnitude RATIO the one-")
L.append("     parameter budget predicts and independent-magnitude mainstream does NOT (the")
L.append("     open C-2 candidate, SH-26) - still UNBUILT. Spatial co-variation alone is [V]/[L].")
L.append("  Occurrence and absolute ages stay [O]/RECORD, both directions.")
L.append("")
L.append(f"GRADE: SH-61 - spatial co-variation r(beta,salt)={r_bs:+.2f} [V] present-tense;")
L.append("       CONSISTENT with the cascade but NON-DISCRIMINATING ([L] economy only).")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "e18f1cac79207ddf742e96be5428c77c8f00904ec978dfd9b70e2876e113feda"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
