#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment A4 :  the FULL A4 anchor/loop/anchor-relative-phase deferred read.
                         Turns the FIREWALL's NAMED [O] from a flagged gap into a MADE measurement —
                         not by inventing numbers, but by fetching the two named inputs and running
                         the INHERITED grammar on them, then reporting honestly what is forced and
                         what stays open.

WHAT THIS BUILDS (FIREWALL §1 — the one NAMED, DEFERRED [O]).
  The seed reads each master-gene promoter as γ (LEVEL) + the promoter-scale A4 SHAPE. The firewall
  flags exactly ONE thing as deferred: "The FULL A4 anchor/loop/anchor-relative-phase needs the wider
  region + an NCBI feature table (rettype=ft) and is a named [O] deferred read — flagged, never
  invented." Two facts make this closable WITHOUT tuning: (1) the inherited grammar
  (inherited/dna_interpreter.py + inherited/key_pipeline_full.py) ALREADY contains every function the
  full read uses — run_key (the W=2000 wide-region shell map), build_anchors (shell-boundary anchors),
  parse_ft_motors (real motors from a feature table), build_loops (motors→anchors), helix_coord (the
  anchor-relative B-DNA phase); and (2) what was missing was the MEASUREMENT — the wider region and the
  feature table for each gene. tools/fetch_region_features.py fetched exactly those two inputs for all
  19 genes from NCBI; inherited/ear_regions.cache.json caches the raw bytes; THIS module recomputes the
  full A4 coordinate from those bytes OFFLINE, deterministically. So the deferred read is now MADE: the
  promise in the dna_interpreter docstring — "upgrades the COORDINATE read from anchors-only to real
  motors+loops" — is fulfilled on measured inputs, never on invented ones.

THE KEYSTONE (consistency, not tuning).
  The wide read provably sits ON TOP of the frozen promoter read with ZERO drift: with a symmetric
  genomic FLANK the cached promoter occupies offset FLANK in the strand-corrected region, so
  region[FLANK:FLANK+2501] == the frozen promoter byte-for-byte — asserted for all 19 genes. The same γ
  the seed has always read is the γ of the central 2501 bp of every wide region; the new A4 coordinate
  is read in the wide neighbourhood AROUND that unchanged centre.

WHAT THE READ ADDS, per gene (all from inherited grammar on measured inputs):
  • SHELL      — which stiffness shell (soft/mid/stiff) of the WIDE neighbourhood the TSS sits in (a real
                 A4 coordinate the promoter-only read cannot give), with its mean_z.
  • ANCHOR     — the nearest shell-boundary anchor: its kind, its strength = |Δmean_z| across the
                 boundary, and its distance.
  • MOTORS+LOOPS — the REAL neighbouring genes parsed from the NCBI feature table (parse_ft_motors),
                 joined to anchors as loops (build_loops, loop_k=2). EVERY gene carries ≥1 real motor.
  • HELICAL PHASE — the TSS↔nearest-anchor B-DNA phase (helix_coord; rise 3.4 Å, twist 34.29°/bp) →
                 contact-competent (same rotational face, ≲60°) or not.

HONEST RESULT (the E6/E7 discipline: existence/form forced, absolute magnitude [O]).
  FORCED [F]/[V]:  the keystone (19/19, exact); the EXISTENCE of a real shell coordinate, a real nearest
  anchor, real motors+loops (19/19 ≥1 motor), and a real anchor-relative phase for every gene; the
  QUALITATIVE read is mostly window-stable (under a 2× window shrink to the central sub-window of the
  SAME fetch: shell class stable 15/19, contact sign stable 16/19, motor-existence 19/19) — so it is not
  a FLANK artifact for the majority. Determinism (2×sha256), offline recompute from the FROZEN cache, and
  a live re-fetch that reproduces the cached bytes.
  OPEN [O] (each obstacle named below, N1–N7):  the absolute FLANK, the absolute anchor distances, and the
  absolute shell/motor/loop COUNTS are window-dependent — a single number would be tuning; the shell CLASS
  and contact SIGN are window-RELATIVE coordinates (the ~20% of genes nearest a tercile/face boundary flip
  under the window change — named, not hidden); "anchor" is a mechanical stiffness-boundary PROXY, not a
  measured CTCF/cohesin site; "loop" is a geometric motor↔anchor join, not a measured Hi-C contact; the
  phase uses IDEALISED constant twist; the loop CENSUS is window-truncated; Layer-2 (sign/fill/wiring) stays
  flagged. So this increment does not pretend to a clean numeric closure — it MAKES the measurement, fulfils
  the read's core promise, and reduces the [O] to its irreducible window-relative / wet-lab residue.

HOW IT RELATES TO THE FOUNDATION (no-regression).
  This increment fetched NO new gene γ and folded nothing into the promoter atlas — it changes NOT ONE of
  the eight pre-existing inherited bytes and triggers NO re-freeze of them. It ADDS one new frozen artifact,
  inherited/ear_regions.cache.json (the measured wide-region + feature-table inputs), recorded deliberately
  in FROZEN_SHA256.json and the ledger. It consumes the INHERITED grammar by IMPORTING it (run_key /
  parse_ft_motors / build_loops / helix_coord) — inventing no new machinery and re-deriving no genome.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/cited · [O] open, obstacle named).
  [F]/[V] : the keystone (region ⊃ frozen promoter, 19/19, exact) ; the EXISTENCE, for every gene, of a real
            wide-neighbourhood shell coordinate + nearest shell-boundary anchor + real feature-table motors
            joined as loops (19/19 ≥1 motor) + a real anchor-relative B-DNA phase ; the window-stability of
            the qualitative read for the majority (class 15/19, contact 16/19, motors 19/19 under a 2× window
            change) ; determinism + offline recompute + live re-fetch byte-exact.
  [L]      : the wide region sequence + NCBI feature table per gene (NCBI-measured, cached, byte-exact,
            re-auditable via tools/fetch_region_features.py verify) ; the B-DNA geometry constants
            (rise 3.4 Å, twist 34.29°/bp) — cited, inherited LOCK.
  [O]      : absolute FLANK / anchor distances (bp) / shell-motor-loop COUNTS (window-dependent — a number =
            tuning) ; the shell CLASS + contact SIGN are window-RELATIVE (4/19 flip class, 3/19 flip contact
            under the window change — named) ; "anchor" = mechanical stiffness-boundary PROXY, not a measured
            CTCF/cohesin site (Hi-C/ChIP [O]) ; "loop" = geometric join, not a measured chromatin contact ;
            the phase uses IDEALISED constant twist (sequence-dependent twist / supercoiling / nucleosome
            phasing [O]) ; the loop CENSUS is window-truncated (neighbours beyond ±FLANK unseen) ; Layer-2
            (cascade sign / runtime fill / wiring) flagged, never assigned ; γ/A4 structure-only (firewall) ;
            felt percept → mind volume. Each names its obstacle below (N1–N7).

FIREWALL. γ/A4 read promoter STRUCTURE only — never a channel voltage, a transduction gain, a drug potency,
a dose, an in-vivo selectivity, or a clinical effect. This increment reads the wide-neighbourhood A4
COORDINATE (shell/anchor/loop/phase), still structure-only; it diagnoses, treats, prescribes nothing; it
designs no molecule. Layer-2 stays flagged. Identity/order are the DNA volume's [V], cited. Determinism:
2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))
for p in (os.path.join(ROOT, "inherited"),):
    if p not in sys.path:
        sys.path.insert(0, p)
import dna_interpreter as DI          # canonical grammar (run_key/parse_ft_motors/build_loops/helix_coord)
import vp_substrate as SUB            # SEED + seed_everything (determinism), consumed unedited

REGION_CACHE = os.path.join(ROOT, "inherited", "ear_regions.cache.json")
PROM_CACHE   = os.path.join(ROOT, "inherited", "ear_promoters.cache.json")


def _load():
    reg = json.load(open(REGION_CACHE, encoding="utf-8"))["genes"]
    prom = json.load(open(PROM_CACHE, encoding="utf-8"))["genes"]
    return reg, prom


def full_a4(region_seq, tss_offset, prom_seq, ft_text):
    """The FULL A4 coordinate for one gene's TSS element, from the inherited grammar on measured inputs."""
    motors = DI.parse_ft_motors(ft_text)
    interp = DI.interpret_element(region_seq, tss_offset, prom_seq, motors=motors)
    return interp["coordinate"], len(motors)


def central_subwindow_read(region_seq, tss_offset, prom_seq, ft_text, flank):
    """Re-read the SAME fetch on its central sub-window (drop flank/2 each end) — the N-robustness probe.
       No network: this is the identical measured region, just a narrower observation window, so any change
       in the qualitative read is the window-relative residue, not new data."""
    half = flank // 2
    sub = region_seq[half:len(region_seq) - half]
    motors = DI.parse_ft_motors(ft_text)
    mots2 = [dict(id=i, pos=m["pos"] - half, strand=m["strand"])
             for i, m in enumerate(motors) if half <= m["pos"] < len(region_seq) - half]
    interp = DI.interpret_element(sub, tss_offset - half, prom_seq, motors=mots2)
    return interp["coordinate"]


def run(P):
    reg, prom = _load()
    syms = list(reg.keys())
    flank = json.load(open(REGION_CACHE, encoding="utf-8"))["_flank"]

    P("=" * 92)
    P("FULL A4 READ — anchor / loop / anchor-relative-phase  (FIREWALL named [O], now MEASURED)")
    P("=" * 92)
    P(f"\nInputs: inherited/ear_regions.cache.json — {len(syms)} genes, wide region = frozen promoter")
    P(f"        TSS−2000..+500 EXTENDED by FLANK={flank} bp each genomic side (single, gene-independent).")
    P("        Grammar: inherited dna_interpreter + key_pipeline_full (run_key/parse_ft_motors/build_loops/")
    P("        helix_coord) — vendored byte-identical. This read invents NO new machinery and NO new number.")

    # -- KEYSTONE: the wide read sits on the FROZEN promoter, zero drift -------------------------------
    keyok = 0
    for s in syms:
        r = reg[s]
        if r["region_seq"][flank:flank + len(prom[s]["seq"])] == prom[s]["seq"]:
            keyok += 1
    P(f"\n[keystone] region[FLANK:FLANK+2501] == FROZEN promoter, byte-for-byte:  {keyok}/{len(syms)}  "
      f"(the wide A4 read is anchored to the unchanged γ layer — zero drift).")
    assert keyok == len(syms), "keystone failed: a wide region does not contain its frozen promoter"

    # -- the FULL A4 coordinate, per gene -------------------------------------------------------------
    P("\n[full A4 coordinate]  shell (wide-neighbourhood) · nearest shell-boundary anchor · real motors+loops ·")
    P("                      anchor-relative B-DNA phase (contact-competent = same rotational face, ≲60°):")
    P(f"  {'gene':9s} {'node':18s} {'shell':6s} {'mz':>6s} {'a.str':>6s} {'a.dist':>7s} "
      f"{'loops':>5s} {'face':>5s} {'contact':>7s} {'motors':>6s}")
    rows = {}
    nmot_pos = 0
    for s in syms:
        r = reg[s]
        c, nmot = full_a4(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"])
        rows[s] = c
        nmot_pos += (c["region_motor_count"] > 0)
        node = (r.get("node") or "")[:18]
        P(f"  {s:9s} {node:18s} {c['shell_class']:6s} {c['shell_mean_z']:>6.2f} "
          f"{c['anchor_strength']:>6.2f} {c['anchor_distance_bp']:>7d} {c['anchor_loops']:>5d} "
          f"{c['anchor_helical_face']:>5.3f} {str(c['contact_competent']):>7s} {c['region_motor_count']:>6d}")
    P(f"\n[motors+loops] genes carrying ≥1 REAL neighbouring-gene motor (feature table) joined as loops: "
      f"{nmot_pos}/{len(syms)}.")
    P("               This fulfils the dna_interpreter promise: anchors-only → real motors+loops, on")
    P("               MEASURED annotation — the core of the deferred read, and it holds for every gene.")
    assert nmot_pos == len(syms), "a gene has no real motor — feature-table read incomplete"

    # -- read-only structure: what the new coordinate reveals that γ-alone and promoter-A4 cannot ------
    stiff = [s for s in syms if rows[s]["shell_class"] == "stiff"]
    midsoft = [s for s in syms if rows[s]["shell_class"] != "stiff"]
    contact = [s for s in syms if rows[s]["contact_competent"]]
    P(f"\n[read-only] {len(stiff)}/{len(syms)} TSS sit in a STIFF wide-neighbourhood shell "
      f"(GC/CpG-island promoter neighbourhoods); the exception(s): {', '.join(midsoft) or '—'} "
      f"(e.g. the AT-rich low-γ structure gene). The promoter-only A4 cannot see this neighbourhood class.")
    P(f"            {len(contact)}/{len(syms)} TSS are contact-competent with their nearest anchor "
      f"(same B-DNA face): {', '.join(contact) or '—'}. (A read-only coordinate; Layer-2 sign stays flagged.)")

    # -- N-ROBUSTNESS: full region vs central sub-window of the SAME fetch (no new data) ---------------
    cls_stab = ctc_stab = mot_stab = 0
    flips_cls, flips_ctc = [], []
    for s in syms:
        r = reg[s]
        cf = rows[s]
        ch = central_subwindow_read(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"], flank)
        if cf["shell_class"] == ch["shell_class"]: cls_stab += 1
        else: flips_cls.append(s)
        if cf["contact_competent"] == ch["contact_competent"]: ctc_stab += 1
        else: flips_ctc.append(s)
        if (cf["region_motor_count"] > 0) == (ch["region_motor_count"] > 0): mot_stab += 1
    P(f"\n[N-robustness] re-read on the central sub-window (FLANK→FLANK/2, a 2× shrink of the SAME measured")
    P(f"               region — no new data). The qualitative read is mostly window-stable:")
    P(f"                 shell class stable : {cls_stab}/{len(syms)}   (flip near a tercile boundary: "
      f"{', '.join(flips_cls) or '—'})")
    P(f"                 contact sign stable: {ctc_stab}/{len(syms)}   (flip near the 60° face cutoff: "
      f"{', '.join(flips_ctc) or '—'})")
    P(f"                 motor existence    : {mot_stab}/{len(syms)}   (every gene keeps ≥1 real motor)")
    P("               So the read is NOT a FLANK artifact for the majority; the minority that flip are the")
    P("               window-RELATIVE residue — forced AWAY from a boundary, [O]-fragile near one (N5).")
    # guard against gross regression without overclaiming the fragile minority as forced
    assert mot_stab == len(syms), "motor existence not window-stable"
    assert cls_stab >= 12, "shell-class stability regressed below the documented majority"

    # -- DETERMINISM of the coordinate itself (independent of the stdout self-hash) --------------------
    h1 = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    rows2 = {}
    for s in syms:
        r = reg[s]
        c, _ = full_a4(r["region_seq"], r["tss_in_region"], prom[s]["seq"], r["ft_text"])
        rows2[s] = c
    h2 = hashlib.sha256(json.dumps(rows2, sort_keys=True).encode()).hexdigest()
    P(f"\n[determinism] full A4 coordinate recomputes identically (coordinate sha256 {h1[:16]}, 2× equal: {h1 == h2}).")
    assert h1 == h2

    # -- HONEST NEGATIVES (named obstacles; nothing tuned, nothing invented) ---------------------------
    P("\n[honest negatives — the [O] this read does NOT close, each obstacle named]")
    P("    N1  'anchor' is a MECHANICAL stiffness-shell BOUNDARY (|Δmean_z|), a proxy — NOT an")
    P("        experimentally mapped CTCF/cohesin site. A measured architectural anchor needs Hi-C/ChIP")
    P("        and is [O]; this read gives the framework's mechanical Layer-1 anchor, not a wet-lab one.")
    P("    N2  'loop' is a GEOMETRIC motor↔nearest-anchor join (build_loops, loop_k=2) — NOT a measured")
    P("        chromatin contact. The EXISTENCE of within-window motors→loops is forced; a real contact")
    P("        frequency (Hi-C/Micro-C) is [O].")
    P("    N3  the anchor-relative phase uses IDEALISED constant B-DNA twist (34.29°/bp, ~10.5 bp/turn).")
    P("        Sequence-dependent twist, supercoiling, and nucleosome phasing are [O]; only the helical")
    P("        FACE (same-side / opposite-side) is read, and only its sign is used.")
    P("    N4  absolute magnitudes are window-dependent [O]: the FLANK itself, the anchor distances in bp,")
    P("        and the shell/motor/loop COUNTS all scale with the observation window. A single absolute")
    P("        number for any of them would be TUNING (forbidden). Only the keystone + motor/loop")
    P("        EXISTENCE + the majority class/sign are window-stable.")
    P("    N5  the shell CLASS and the contact SIGN are window-RELATIVE coordinates (tercile thresholds and")
    P("        the 60° cutoff are referenced to the chosen window). Under a 2× window change "
      f"{len(flips_cls)}/{len(syms)} genes")
    P("        flip class and " + f"{len(flips_ctc)}/{len(syms)} flip contact — forced AWAY from a boundary,")
    P("        [O]-fragile near one. Named, not hidden: a clean per-gene class/sign would overclaim.")
    P("    N6  the loop CENSUS is window-TRUNCATED: neighbouring genes beyond ±FLANK are unseen, so the")
    P("        loop set is a lower bound. Within-window existence is forced; the COMPLETE census is [O].")
    P("    N7  Layer-2 stays flagged (firewall): the cascade SIGN (brake/accelerator), the runtime fill,")
    P("        and the wiring are NOT sequence-derivable and are never assigned. γ/A4 are STRUCTURE-ONLY —")
    P("        never a voltage, dose, selectivity, or effect; the felt percept of hearing is the mind")
    P("        volume's. Nothing here is diagnosed, treated, or prescribed; no molecule is designed.")

    # -- naming note (the seed's E-numbering slip, flagged not silently fixed) -------------------------
    P("\n[naming note] This increment ships in folder research/A4-anchor-loop-phase/ — a READING deepening")
    P("    (it closes the FIREWALL named [O]), NOT a wave E-chapter, so it does not enter the E-numbering")
    P("    map (verifier block [5] scans research/E*/ only) and introduces no new label inconsistency.")

    P("\nLEARNED (A4): the FIREWALL's named [O] — the FULL A4 anchor/loop/anchor-relative-phase — was a")
    P("  missing MEASUREMENT, not missing machinery. Fetching the two named inputs (wider region + NCBI")
    P("  feature table) for all 19 genes and running the INHERITED grammar MAKES the read: every TSS now")
    P("  carries a real wide-neighbourhood shell coordinate, a real nearest anchor, real feature-table")
    P("  motors joined as loops (19/19), and a real anchor-relative B-DNA phase — anchored to the frozen")
    P("  promoter with zero drift (keystone 19/19). The qualitative read is mostly window-stable (class")
    P("  15/19, contact 16/19, motors 19/19); the absolute magnitudes and the boundary-near class/sign are")
    P("  the irreducible window-relative [O], and the wet-lab contact map + sequence-dependent twist are a")
    P("  deeper [O] — both NAMED, never invented. No pre-existing inherited byte changed; one new frozen")
    P("  artifact (the measured region+feature-table cache) was added deliberately.")


def main():
    SUB.seed_everything(SUB.SEED)            # lock the seed (no RNG is used; determinism by construction)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
