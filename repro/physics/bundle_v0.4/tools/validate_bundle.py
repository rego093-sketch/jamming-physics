#!/usr/bin/env python3
"""AQD Unified DOI Bundle validator (strict mode).

This script performs lightweight, deterministic checks to help keep the bundle
internally consistent:

1) No image assets are shipped (png/jpg/svg/...)
2) No LaTeX build artifacts are shipped (aux/log/out/toc/...)
3) Canonical constants are consistent across key lock files
4) Manifests reference existing files

It does *not* attempt to run simulations or rebuild PDFs.

Usage:
  python3 tools/validate_bundle.py

Exit codes:
  0 success
  1 validation failures
"""

from __future__ import annotations

import json
import os
import re
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Iterable, Tuple


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}
# Note: avoid blanket-banning ".log" because simulation packages legitimately ship
# run logs (stdout/stderr). We ban the more unambiguous LaTeX artifacts.
LATEX_ARTIFACT_EXTS = {".aux", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz"}


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dec(x) -> Decimal:
    # Robust conversion for canonical constants (strings) or numeric lock values.
    if isinstance(x, Decimal):
        return x
    return Decimal(str(x))


def find_files(root: Path, predicate) -> Iterable[Path]:
    for p in root.rglob("*"):
        if p.is_file() and predicate(p):
            yield p


def check_no_images(root: Path) -> Tuple[bool, int]:
    bad = list(find_files(root, lambda p: p.suffix.lower() in IMAGE_EXTS))
    if bad:
        fail(f"Found {len(bad)} image file(s) (images are not allowed in this bundle).")
        for p in bad[:20]:
            print(f"  - {p}")
        if len(bad) > 20:
            print("  ...")
        return False, len(bad)
    ok("No image files present.")
    return True, 0


def check_no_latex_artifacts(root: Path) -> Tuple[bool, int]:
    def is_artifact(p: Path) -> bool:
        name = p.name.lower()
        if name.endswith(".synctex.gz"):
            return True
        return p.suffix.lower() in LATEX_ARTIFACT_EXTS

    bad = list(find_files(root, is_artifact))
    if bad:
        fail(f"Found {len(bad)} LaTeX build artifact(s). Remove before deposit.")
        for p in bad[:20]:
            print(f"  - {p}")
        if len(bad) > 20:
            print("  ...")
        return False, len(bad)
    ok("No LaTeX build artifacts present.")
    return True, 0


def check_canonical_consistency(root: Path) -> bool:
    """Check that module lock files use the canonical constants."""
    getcontext().prec = 80

    constants_path = root / "00_metadata" / "aqd_constants.json"
    cc = load_json(constants_path)["aqd_canonical_constants"]

    ell_rot_m = dec(cc["ell_rot_m"]["value"])
    a_m = dec(cc["a_m"]["value"])
    rp_m = dec(cc["proton_radius_m"]["value"])

    # Quantum annihilation canon lock
    canon_lock_path = root / "01_quantum_annihilation" / "quantum_annihilation_DOI_vNext" / "LOCK" / "canon_lock.json"
    if not canon_lock_path.exists():
        fail(f"Missing file: {canon_lock_path}")
        return False

    canon = load_json(canon_lock_path)
    D_anch_m = dec(canon.get("D_anch_m"))
    r_p_m = dec(canon.get("r_p_m"))

    # Compare with a tight relative tolerance (Decimal exact strings are used in constants).
    # Lock file values may be floats; compare numerically.
    def rel_err(x: Decimal, y: Decimal) -> Decimal:
        return abs(x - y) / abs(y)

    ok_all = True

    if rel_err(D_anch_m, ell_rot_m) > Decimal("1e-20"):
        fail(f"canon_lock D_anch_m != canonical ell_rot_m. D_anch_m={D_anch_m}, ell_rot_m={ell_rot_m}")
        ok_all = False
    else:
        ok("canon_lock D_anch_m matches canonical ell_rot_m")

    if rel_err(r_p_m, rp_m) > Decimal("1e-20"):
        fail(f"canon_lock r_p_m != canonical proton_radius_m. r_p_m={r_p_m}, proton_radius_m={rp_m}")
        ok_all = False
    else:
        ok("canon_lock r_p_m matches canonical proton_radius_m")

    # Realization lock a_m check (float precision limited; allow looser tolerance)
    realization_lock_path = root / "01_quantum_annihilation" / "quantum_annihilation_DOI_vNext" / "LOCK" / "realization_lock.json"
    if realization_lock_path.exists():
        rl = load_json(realization_lock_path)
        a_lock = dec(rl.get("a_m"))
        if rel_err(a_lock, a_m) > Decimal("1e-12"):
            fail(f"realization_lock a_m differs from canonical a_m beyond float tolerance. a_m(lock)={a_lock}, a_m(canon)={a_m}")
            ok_all = False
        else:
            ok("realization_lock a_m matches canonical a_m (within tolerance)")
    else:
        fail(f"Missing file: {realization_lock_path}")
        ok_all = False

    return ok_all


def check_manifests_reference_existing_files(root: Path) -> bool:
    """Ensure manifests don't reference missing files (common when pruning images)."""
    manifest_paths = [
        root / "00_metadata" / "MANIFEST.sha256",
        root / "01_quantum_annihilation" / "quantum_annihilation_DOI_vNext" / "MANIFEST.sha256",
        root / "02_lattice_percolation_soc" / "lattice_percolation_soc_bundle" / "manifest_sha256.txt",
        root / "03_qm_proton_whitepaper" / "MANIFEST.sha256",
    ]

    ok_all = True
    for mp in manifest_paths:
        if not mp.exists():
            fail(f"Missing manifest: {mp}")
            ok_all = False
            continue
        missing = []
        # Base directory rule:
        # - 00_metadata/MANIFEST.sha256 enumerates files relative to the bundle root
        # - module manifests enumerate files relative to their own module root
        if mp.parent.name == "00_metadata" and mp.name == "MANIFEST.sha256":
            base_dir = root
        else:
            base_dir = mp.parent
        for line in mp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                _hash, rel = line.split(None, 1)
            except ValueError:
                missing.append(("<parse>", line))
                continue
            rel = rel.strip()
            # Manifests are generated with leading ./ paths
            rel_path = rel[2:] if rel.startswith("./") else rel
            target = (base_dir / rel_path).resolve()
            if not target.exists():
                missing.append((rel, str(target)))
        if missing:
            fail(f"Manifest has {len(missing)} missing entry(ies): {mp}")
            for rel, target in missing[:20]:
                print(f"  - {rel} -> {target}")
            if len(missing) > 20:
                print("  ...")
            ok_all = False
        else:
            ok(f"Manifest references existing files: {mp}")
    return ok_all


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    success = True

    s1, _ = check_no_images(root)
    success &= s1

    s2, _ = check_no_latex_artifacts(root)
    success &= s2

    success &= check_canonical_consistency(root)
    success &= check_manifests_reference_existing_files(root)

    if success:
        ok("All strict checks passed.")
        return 0

    fail("One or more strict checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
