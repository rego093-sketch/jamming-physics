#!/usr/bin/env python3
"""Minimal deterministic chemistry support pipeline for VP whitepaper (Sec. 18).

This script:
- loads LOCK/chem_lock.json and the CSV inputs under data/chem/
- computes P_idx and r_eff for selected atoms/molecules
- computes r0 and ratios for the √2 table (Sec.18.3.2)
- computes Tb/Tm ratio for the 1.6 claim (Sec.18.8.3)
- writes JSON + LaTeX outputs into outputs/chem/
- emits a small run bundle into runs/run_CHEM_MINIMAL_0001/
- emits gate reports into bundle_root/gate/reports/

No non-std dependencies.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple


# ----------------------------
# Utilities
# ----------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Deterministic JSON (stable key ordering)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding='utf-8')


def protocol_created(bundle_root: Path) -> str:
    """Deterministic date for reproducibility (preferred over wall-clock time)."""
    p = bundle_root / "registry" / "protocol_lock.json"
    if p.exists():
        try:
            v = load_json(p).get("created")
            if v:
                return str(v)
        except Exception:
            pass
    return str(date.today())


def read_csv_dicts(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Strip whitespace from keys/values
            cleaned = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
            rows.append(cleaned)
    return rows


def parse_components(s: str) -> Dict[str, int]:
    """Parse 'H:2;O:1' into {'H': 2, 'O': 1}."""
    out: Dict[str, int] = {}
    if not s:
        return out
    for part in s.split(';'):
        part = part.strip()
        if not part:
            continue
        if ':' not in part:
            raise ValueError(f"Bad component token: {part}")
        k, v = part.split(':', 1)
        out[k.strip()] = int(v.strip())
    return out


def round_to(x: float, decimals: int) -> float:
    # Use Python round; stable enough for display use.
    return float(round(x, decimals))


@dataclass
class SpeciesRadius:
    species: str
    Z: int
    radius_pm: float
    radius_kind: str
    source_short: str
    source_detail: str


# ----------------------------
# Core computations
# ----------------------------

def compute_P_raw(Z: int, radius_pm: float) -> float:
    return float(Z) / (float(radius_pm) ** 2)


def compute_P_idx(P_raw_x: float, P_raw_ref: float) -> float:
    return P_raw_x / P_raw_ref


def compute_r_eff(r_vac_fm: float, P_idx_x: float) -> float:
    return r_vac_fm / math.sqrt(P_idx_x)


def stoichiometric_average(values: List[Tuple[float, int]]) -> float:
    """values is [(val_i, n_i), ...]."""
    num = 0.0
    den = 0
    for v, n in values:
        num += v * n
        den += n
    if den <= 0:
        raise ValueError("Empty stoichiometric average")
    return num / float(den)


# ----------------------------
# LaTeX generators
# ----------------------------

def latex_table_pressure_amplitude(rows: List[dict]) -> str:
    """Generate a LaTeX table matching the structure of Sec.18.2.3."""
    # Expect rows with keys: material, P_idx_display, r_eff_display, plus computed raw values.
    # The narrative columns are intentionally included (they are part of the whitepaper semantics).
    # This keeps the compiled PDF stable while guaranteeing that the numerical columns are generated
    # from locked inputs.
    ann = {
        "H": {
            "display": r"$H$ (수소)",
            "p_suffix": r" (기준)",
            "state": r"기준 상태",
            "chem": r"무결점 구조, 최대 이완",
        },
        "C": {
            "display": r"$C$ (탄소)",
            "p_suffix": r"",
            "state": r"완전 평형",
            "chem": r"유기 화합물의 뼈대, 구조적 안정",
        },
        "H2O": {
            "display": r"$H_2O$ (물)",
            "p_suffix": r" (평균)",
            "state": r"동적 안정",
            "chem": r"액체 상태 유지, 표면장력 우수",
            "r_eff_style": "approx_int",
        },
        "O": {
            "display": r"$O$ (산소)",
            "p_suffix": r"",
            "state": r"과압축",
            "chem": r"높은 반응성(산화력), 전자 탈취",
        },
        "Pt": {
            "display": r"$Pt$ (백금)",
            "p_suffix": r"",
            "state": r"초고밀도",
            "chem": r"\textbf{촉매 활성}, 접촉 물질 격자 왜곡",
        },
    }

    lines: List[str] = []
    lines.append(r"% Auto-generated by 04_vp_whitepaper/scripts/run_chem_minimal.py")
    lines.append(r"% Numerical columns are derived from locked inputs (LOCK/chem_lock.json + data/chem/*).")
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{|c|c|c|c|c|}")
    lines.append(r"\hline")
    lines.append(r"\textbf{물질} & \textbf{압력 지수 ($P_{\mathrm{idx}}$)} & \textbf{유효 진폭 ($r_{\mathrm{eff}}$)} & \textbf{상태 해석} & \textbf{화학적 특성}\\ \hline")

    for r in rows:
        key = r["material"]
        meta = ann.get(key, {
            "display": key,
            "p_suffix": "",
            "state": "",
            "chem": "",
        })

        # P_idx display: keep numeric rounded value, then optional suffix
        p_num = r["P_idx_display"]
        p_tex = f"{p_num:.2f}{meta.get('p_suffix','')}" if isinstance(p_num, (int, float)) else f"{p_num}{meta.get('p_suffix','')}"

        # r_eff display: by default show 1-decimal; for selected rows show an approximate integer.
        r_eff_val = float(r["r_eff_fm"]) if "r_eff_fm" in r else float(r["r_eff_display"])
        if meta.get("r_eff_style") == "approx_int":
            # Keep units in math mode to avoid \mathrm errors.
            r_eff_tex = rf"$\approx {int(round(r_eff_val))}\,\mathrm{{fm}}$"
        else:
            # Default: 1-decimal display in math mode.
            if isinstance(r.get("r_eff_display"), (int, float)):
                r_eff_tex = f"${float(r['r_eff_display']):.1f}\\,\\mathrm{{fm}}$"
            else:
                r_eff_tex = f"${r['r_eff_display']}\\,\\mathrm{{fm}}$"

        lines.append(
            f"{meta['display']} & {p_tex} & {r_eff_tex} & {meta.get('state','')} & {meta.get('chem','')}\\\\ \\hline"
        )

    lines.append(r"\end{tabular}")
    lines.append(r"\caption{표면 전하 밀도에 따른 동적 진폭 및 화학적 상태 정의}")
    lines.append(r"\label{tab:pressure_amplitude}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


def latex_table_sqrt2_validation(rows: List[dict]) -> str:
    """Generate a LaTeX table matching the structure of Sec.18.3.2."""
    ann = {
        "N2": {
            "display": r"\textbf{질소 ($N_2$)}",
            "verdict": r"임계 근접 (촉매 필요)",
        },
        "CO2": {
            "display": r"\textbf{이산화탄소}",
            "verdict": r"임계 초과 (완전 분해)",
        },
        "H2O": {
            "display": r"\textbf{물 ($H_2O$)}",
            "verdict": r"안전 (액체 유지)",
        },
        "Na+": {
            "display": r"\textbf{나트륨 이온}",
            "verdict": r"이온 팽창 (결합 아님)",
        },
    }

    src_tag_map = {
        "report": r"[보고서]",
        "device": r"[정수기]",
        "environment": r"[해수]",
    }

    lines: List[str] = []
    lines.append(r"% Auto-generated by 04_vp_whitepaper/scripts/run_chem_minimal.py")
    lines.append(r"% r0 is model-derived from locked inputs; observed amplitudes are locked extracts (see docs/chem/EXTRACTION_PROTOCOL.md).")
    lines.append(r"\begin{table}[h]")
    lines.append(r"\centering")
    lines.append(r"\begin{tabular}{|c|c|c|c|c|c|}")
    lines.append(r"\hline")
    lines.append(r"\textbf{대상} & \textbf{바닥 진폭 ($r_0$)} & \textbf{붕괴/활성 진폭 ($r_{\mathrm{break}}$)} & \textbf{확장비 ($\frac{r}{r_0}$)} & \textbf{이론값 ($\sqrt{2}$)} & \textbf{판정}\\ \hline")

    for r in rows:
        key = r["system"]
        meta = ann.get(key, {"display": key, "verdict": r.get("verdict", "")})

        r0 = int(r["r0_display"]) if isinstance(r.get("r0_display"), (int, float)) else r["r0_display"]
        ro = int(r["r_obs_display"]) if isinstance(r.get("r_obs_display"), (int, float)) else r["r_obs_display"]
        ratio = r["ratio_display"]
        sqrt2 = r["sqrt2_display"]

        # Observed amplitude formatting: show approx for report-like sources.
        tag = src_tag_map.get(r.get("source_tag", ""), "")
        if r.get("source_tag") == "report":
            ro_tex = rf"$\approx {ro}\,\mathrm{{fm}}$ {tag}"
        else:
            ro_tex = rf"${ro}\,\mathrm{{fm}}$ {tag}"

        r0_tex = rf"${r0}\,\mathrm{{fm}}$"

        lines.append(
            f"{meta['display']} & {r0_tex} & {ro_tex} & \\textbf{{{ratio}}} & {sqrt2} & {meta.get('verdict','')}\\\\ \\hline"
        )

    lines.append(r"\end{tabular}")
    lines.append(r"\caption{화학 결합 붕괴의 기하학적 임계값 검증 ($\sqrt{2}$ 법칙)}")
    lines.append(r"\label{tab:sqrt2_validation}")
    lines.append(r"\end{table}")
    return "\n".join(lines) + "\n"


# ----------------------------
# Gate helpers
# ----------------------------

def gate_compare_float(name: str, got: float, expected: float, tol: float) -> Tuple[bool, dict]:
    ok = abs(got - expected) <= tol
    return ok, {
        "name": name,
        "got": got,
        "expected": expected,
        "abs_err": abs(got - expected),
        "tol": tol,
        "pass": ok,
    }


def make_gate_report(
    gate_id: str,
    result: str,
    checks: List[dict],
    inputs: dict,
    outputs: dict,
    generator: str,
    created: str,
    notes: str = "",
) -> dict:
    # Deterministic stamp (no wall-clock time): key for reproducibility hashing.
    ts = f"{created}T00:00:00Z" if created else ""
    return {
        "gate_id": gate_id,
        "status": result,
        "created": created,
        "result": result,
        "fail_labels": [] if result == "PASS" else ["CHECK_FAILED"],
        "checks": checks,
        "inputs": inputs,
        "outputs": outputs,
        "generated_by": generator,
        "notes": notes,
        "timestamp_utc": ts,
    }


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    # Locate bundle root from this script location.
    script_path = Path(__file__).resolve()
    vp_root = script_path.parents[1]  # 04_vp_whitepaper/
    bundle_root = vp_root.parents[0]  # AQD_DOI_bundle_unified_v0.2.6_logic/

    created_date = protocol_created(bundle_root)
    stamp_utc = f"{created_date}T00:00:00Z" if created_date else ""

    lock_path = vp_root / "LOCK" / "chem_lock.json"
    lock = load_json(lock_path)

    # Inputs
    species_csv = bundle_root / lock["inputs"]["species_radius_csv"]
    mol_csv = bundle_root / lock["inputs"]["molecule_composition_csv"]
    obs_csv = bundle_root / lock["inputs"]["observed_amplitudes_csv"]
    thermo_csv = bundle_root / lock["inputs"]["thermo_phase_points_csv"]

    r_vac = float(lock["constants"]["r_vac_fm"])

    # Load species radii
    species_rows = read_csv_dicts(species_csv)
    species_map: Dict[str, SpeciesRadius] = {}
    for r in species_rows:
        s = SpeciesRadius(
            species=r["species"],
            Z=int(r["Z"]),
            radius_pm=float(r["radius_pm"]),
            radius_kind=r.get("radius_kind", ""),
            source_short=r.get("source_short", ""),
            source_detail=r.get("source_detail", ""),
        )
        species_map[s.species] = s

    # Reference species (H)
    ref = lock["constants"]["reference_species"]["species"]
    if ref not in species_map:
        raise SystemExit(f"Reference species {ref} not found in {species_csv}")
    P_raw_ref = compute_P_raw(species_map[ref].Z, species_map[ref].radius_pm)

    # Compute per-atom P_idx and r_eff
    atom_results: Dict[str, dict] = {}
    for sp, s in species_map.items():
        P_raw = compute_P_raw(s.Z, s.radius_pm)
        P_idx = compute_P_idx(P_raw, P_raw_ref)
        r_eff_fm = compute_r_eff(r_vac, P_idx)
        atom_results[sp] = {
            "species": sp,
            "Z": s.Z,
            "radius_pm": s.radius_pm,
            "radius_kind": s.radius_kind,
            "P_raw": P_raw,
            "P_idx": P_idx,
            "r_eff_fm": r_eff_fm,
        }

    # Load molecules
    mol_rows = read_csv_dicts(mol_csv)
    mol_results: Dict[str, dict] = {}
    for r in mol_rows:
        name = r["species"]
        comp = parse_components(r["components"])
        # Stoichiometric average of P_idx across atoms
        vals = []
        for atom, n in comp.items():
            if atom not in atom_results:
                raise SystemExit(f"Molecule {name} references unknown atom: {atom}")
            vals.append((atom_results[atom]["P_idx"], n))
        P_idx_m = stoichiometric_average(vals)
        r_eff_m = compute_r_eff(r_vac, P_idx_m)
        mol_results[name] = {
            "species": name,
            "components": comp,
            "P_idx": P_idx_m,
            "r_eff_fm": r_eff_m,
        }

    # ----------------
    # Outputs (Sec.18.2 table)
    # ----------------
    disp_p_dec = int(lock["display"]["table_pressure_amplitude"]["P_idx_round_decimals"])
    disp_r_dec = int(lock["display"]["table_pressure_amplitude"]["r_eff_round_decimals"])

    # Select rows to mirror the whitepaper table
    pressure_table_materials = ["H", "C", "H2O", "O", "Pt"]
    pressure_table_rows = []
    for m in pressure_table_materials:
        if m in atom_results:
            P = atom_results[m]["P_idx"]
            R = atom_results[m]["r_eff_fm"]
        elif m in mol_results:
            P = mol_results[m]["P_idx"]
            R = mol_results[m]["r_eff_fm"]
        else:
            raise SystemExit(f"Unknown material in pressure table: {m}")

        pressure_table_rows.append({
            "material": m,
            "P_idx": P,
            "r_eff_fm": R,
            "P_idx_display": round_to(P, disp_p_dec),
            "r_eff_display": round_to(R, disp_r_dec),
            "note": "" if m != "H2O" else "(avg)"
        })

    out_pressure_json = {
        "lock": lock["version"],
        "generated_utc": stamp_utc,
        "reference_species": ref,
        "r_vac_fm": r_vac,
        "atoms": atom_results,
        "molecules": mol_results,
        "table_rows": pressure_table_rows,
    }

    outdir = vp_root / "outputs" / "chem"
    outdir.mkdir(parents=True, exist_ok=True)

    pressure_json_path = outdir / "pressure_amplitude.json"
    write_json(pressure_json_path, out_pressure_json)

    pressure_tex_path = outdir / "table_pressure_amplitude.tex"
    pressure_tex_path.write_text(latex_table_pressure_amplitude(pressure_table_rows), encoding='utf-8')

    # ----------------
    # Outputs (Sec.18.3 √2 table)
    # ----------------
    obs_rows = read_csv_dicts(obs_csv)
    sqrt2 = float(lock["constants"]["sqrt2"])

    sqrt2_table_rows = []
    for r in obs_rows:
        sysname = r["system"]
        context = r["context"]
        r_obs = float(r["r_observed_fm"])

        # Define r0 by model: stoichiometric average of r_eff over constituent atoms.
        if sysname in mol_results:
            comp = mol_results[sysname]["components"]
            atom_r_eff_vals = []
            for atom, n in comp.items():
                atom_r_eff_vals.append((atom_results[atom]["r_eff_fm"], n))
            r0 = stoichiometric_average(atom_r_eff_vals)
        elif sysname in atom_results:
            r0 = atom_results[sysname]["r_eff_fm"]
        else:
            raise SystemExit(f"Observed system not found in molecules/atoms: {sysname}")

        ratio = r_obs / r0

        # Simple verdict rules (deterministic):
        if context == "bond_break":
            verdict = "break"
        elif context == "bond_break_or_activation":
            verdict = "near"
        else:
            verdict = "safe"

        sqrt2_table_rows.append({
            "system": sysname,
            "context": context,
            "r0_fm": r0,
            "r_obs_fm": r_obs,
            "ratio": ratio,
            "r0_display": int(round(r0)),
            "r_obs_display": int(round(r_obs)),
            "ratio_display": round_to(ratio, int(lock["display"]["table_sqrt2_validation"]["ratio_round_decimals"])),
            "sqrt2_display": round_to(sqrt2, 2),
            "verdict": verdict,
            "source_tag": r.get("source_tag", ""),
            "source_detail": r.get("source_detail", ""),
        })

    sqrt2_json_path = outdir / "sqrt2_validation.json"
    write_json(sqrt2_json_path, {
        "lock": lock["version"],
        "generated_utc": stamp_utc,
        "sqrt2": sqrt2,
        "rows": sqrt2_table_rows,
    })

    sqrt2_tex_path = outdir / "table_sqrt2_validation.tex"
    sqrt2_tex_path.write_text(latex_table_sqrt2_validation(sqrt2_table_rows), encoding='utf-8')

    # ----------------
    # Outputs (Sec.18.8 Tb/Tm)
    # ----------------
    thermo_rows = read_csv_dicts(thermo_csv)
    sqrt2p5 = float(lock["constants"]["sqrt2p5"])
    ratio_dec = int(lock["display"]["tb_tm_ratio"]["ratio_round_decimals"])

    tb_tm_rows = []
    for r in thermo_rows:
        mat = r["material"]
        Tm = float(r["Tm_K"])
        Tb = float(r["Tb_K"])
        ratio = Tb / Tm
        tb_tm_rows.append({
            "material": mat,
            "Tm_K": Tm,
            "Tb_K": Tb,
            "ratio": ratio,
            "ratio_display": round_to(ratio, ratio_dec),
            "theory": sqrt2p5,
            "theory_display": round_to(sqrt2p5, ratio_dec),
            "pressure_condition": r.get("pressure_condition", ""),
            "source_tag": r.get("source_tag", ""),
            "source_detail": r.get("source_detail", ""),
        })

    tb_tm_json_path = outdir / "tb_tm_ratio.json"
    write_json(tb_tm_json_path, {
        "lock": lock["version"],
        "generated_utc": stamp_utc,
        "theory": sqrt2p5,
        "rows": tb_tm_rows,
    })

    # ----------------
    # Gate checks (coherence with paper display values)
    # ----------------
    checks_pressure = []
    ok_pressure = True
    target_pressure = lock["targets_from_whitepaper"]["table_pressure_amplitude_expected_display"]

    # tolerances chosen to be conservative for displayed values
    tol_p = 0.03
    tol_r = 1.5

    for row in pressure_table_rows:
        mat = row["material"]
        exp = target_pressure.get(mat)
        if not exp:
            continue
        ok1, c1 = gate_compare_float(f"{mat}.P_idx", row["P_idx_display"], float(exp["P_idx"]), tol_p)
        ok2, c2 = gate_compare_float(f"{mat}.r_eff_fm", row["r_eff_display"], float(exp["r_eff_fm"]), tol_r)
        checks_pressure.extend([c1, c2])
        ok_pressure &= ok1 and ok2

    gate_pressure_result = "PASS" if ok_pressure else "FAIL"

    checks_sqrt2 = []
    ok_sqrt2 = True
    target_sqrt2 = lock["targets_from_whitepaper"]["table_sqrt2_validation_expected_display"]
    tol_r0 = 2.0
    tol_ratio = 0.03

    for row in sqrt2_table_rows:
        key = row["system"]
        exp = target_sqrt2.get(key)
        if not exp:
            continue
        ok1, c1 = gate_compare_float(f"{key}.r0_fm", float(row["r0_display"]), float(exp["r0_fm"]), tol_r0)
        ok2, c2 = gate_compare_float(f"{key}.ratio", float(row["ratio_display"]), float(exp["ratio"]), tol_ratio)
        checks_sqrt2.extend([c1, c2])
        ok_sqrt2 &= ok1 and ok2

    gate_sqrt2_result = "PASS" if ok_sqrt2 else "FAIL"

    checks_tb = []
    ok_tb = True
    target_tb = lock["targets_from_whitepaper"]["tb_tm_ratio_expected_display"]

    for row in tb_tm_rows:
        mat = row["material"]
        exp = target_tb.get(mat)
        if not exp:
            continue
        ok1, c1 = gate_compare_float(f"{mat}.ratio_display", float(row["ratio_display"]), float(exp["ratio"]), 0.01)
        ok2, c2 = gate_compare_float(f"{mat}.theory_display", float(row["theory_display"]), float(exp["theory"]), 0.01)
        checks_tb.extend([c1, c2])
        ok_tb &= ok1 and ok2

    gate_tb_result = "PASS" if ok_tb else "FAIL"

    # ----------------
    # Run bundle
    # ----------------
    run_dir = vp_root / "runs" / "run_CHEM_MINIMAL_0001"
    run_dir.mkdir(parents=True, exist_ok=True)

    run_meta = {
        "run_id": "CHEM_MINIMAL_0001",
        "generated_utc": stamp_utc,
        "created": created_date,
        "generator": str((vp_root / "scripts" / "run_chem_minimal.py").relative_to(bundle_root)),
        "lock_path": str(lock_path.relative_to(bundle_root)),
        "lock_sha256": sha256_file(lock_path),
        "inputs": {
            "species_radius_csv": str(species_csv.relative_to(bundle_root)),
            "molecule_composition_csv": str(mol_csv.relative_to(bundle_root)),
            "observed_amplitudes_csv": str(obs_csv.relative_to(bundle_root)),
            "thermo_phase_points_csv": str(thermo_csv.relative_to(bundle_root)),
        },
        "outputs": {
            "pressure_amplitude.json": str(pressure_json_path.relative_to(bundle_root)),
            "table_pressure_amplitude.tex": str(pressure_tex_path.relative_to(bundle_root)),
            "sqrt2_validation.json": str(sqrt2_json_path.relative_to(bundle_root)),
            "table_sqrt2_validation.tex": str(sqrt2_tex_path.relative_to(bundle_root)),
            "tb_tm_ratio.json": str(tb_tm_json_path.relative_to(bundle_root)),
        },
        "gate_results": {
            "pressure_amplitude": gate_pressure_result,
            "sqrt2_validation": gate_sqrt2_result,
            "tb_tm_ratio": gate_tb_result,
        },
    }
    write_json(run_dir / "run_meta.json", run_meta)

    # checksums (inputs + outputs + lock)
    checksum_paths = [
        lock_path, species_csv, mol_csv, obs_csv, thermo_csv,
        pressure_json_path, pressure_tex_path, sqrt2_json_path, sqrt2_tex_path, tb_tm_json_path,
    ]
    checksums = {str(p.relative_to(bundle_root)): sha256_file(p) for p in checksum_paths}
    write_json(run_dir / "checksums.json", checksums)

    # ----------------
    # Gate reports at bundle root
    # ----------------
    gate_dir = bundle_root / "gate" / "reports"
    gate_dir.mkdir(parents=True, exist_ok=True)

    gen = str((vp_root / "scripts" / "run_chem_minimal.py").relative_to(bundle_root))

    write_json(
        gate_dir / "gate_report_chem_pressure_amplitude.json",
        make_gate_report(
            gate_id="G-CHEM-PRESSURE-AMPLITUDE",
            result=gate_pressure_result,
            checks=checks_pressure,
            inputs={
                "chem_lock": str(lock_path.relative_to(bundle_root)),
                "species_radius_csv": str(species_csv.relative_to(bundle_root)),
                "molecule_composition_csv": str(mol_csv.relative_to(bundle_root)),
            },
            outputs={
                "pressure_amplitude.json": str(pressure_json_path.relative_to(bundle_root)),
                "table_pressure_amplitude.tex": str(pressure_tex_path.relative_to(bundle_root)),
            },
            generator=gen,
            created=created_date,
            notes="Coherence check: computed display values match the Sec.18.2.3 table (within conservative tolerances).",
        ),
    )

    write_json(
        gate_dir / "gate_report_chem_sqrt2_validation.json",
        make_gate_report(
            gate_id="G-CHEM-SQRT2-VALIDATION",
            result=gate_sqrt2_result,
            checks=checks_sqrt2,
            inputs={
                "chem_lock": str(lock_path.relative_to(bundle_root)),
                "observed_amplitudes_csv": str(obs_csv.relative_to(bundle_root)),
            },
            outputs={
                "sqrt2_validation.json": str(sqrt2_json_path.relative_to(bundle_root)),
                "table_sqrt2_validation.tex": str(sqrt2_tex_path.relative_to(bundle_root)),
            },
            generator=gen,
            created=created_date,
            notes="This gate validates the internal LOCK→derived connection for r0 and ratios. Primary-source PDFs are not bundled in this minimal run; see docs/chem/EXTRACTION_PROTOCOL.md.",
        ),
    )

    write_json(
        gate_dir / "gate_report_chem_tb_tm_ratio.json",
        make_gate_report(
            gate_id="G-CHEM-TB-TM-RATIO",
            result=gate_tb_result,
            checks=checks_tb,
            inputs={
                "chem_lock": str(lock_path.relative_to(bundle_root)),
                "thermo_phase_points_csv": str(thermo_csv.relative_to(bundle_root)),
            },
            outputs={
                "tb_tm_ratio.json": str(tb_tm_json_path.relative_to(bundle_root)),
            },
            generator=gen,
            created=created_date,
            notes="Tb/Tm ratio computed from locked thermodynamic points; compared to sqrt(2.5) display rounding.",
        ),
    )

    # Minimal console summary
    print("[CHEM_MINIMAL] Outputs written to:", outdir)
    print("[CHEM_MINIMAL] Gate:")
    print("  - pressure_amplitude:", gate_pressure_result)
    print("  - sqrt2_validation:", gate_sqrt2_result)
    print("  - tb_tm_ratio:", gate_tb_result)

    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
