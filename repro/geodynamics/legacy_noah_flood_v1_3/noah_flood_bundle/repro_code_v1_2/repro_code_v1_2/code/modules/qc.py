import os, hashlib, pandas as pd

NEEDED = [
    "A_coastline/coast_line.csv",
    "B_isotopes/leafwax_dD_master.csv",
    "C_coal_geochem/raw_data.csv",
    "R6_IntCal_Marine/IntCal20_Marine20_full_raw.csv",
    "R7_DeltaR_Med/DeltaR_intake.csv",
    "R8_RSL/RSL_intake.csv",
    "R9_SPD/C14_intake.csv",
    "R10_Nile/seismic_profile_summary.csv",
    "R10_Nile/compaction_curve.csv",
    "R10_Nile/bulk_density_summary.csv",
    "PF_pack/human_pigment_variants.tsv",
    "DINO_THERM/bone_histology.csv",
    "PLANT_E1E2/leaf_cuticle_SI.csv",
]

def hash_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(1024*1024)
            if not b: break
            h.update(b)
    return h.hexdigest()

def hash_manifest(root):
    rows = []
    for dirpath, _, filenames in os.walk(root):
        for fn in sorted(filenames):
            fp = os.path.join(dirpath, fn)
            rows.append({
                "path": os.path.relpath(fp, root),
                "sha256": hash_file(fp),
                "bytes": os.path.getsize(fp)
            })
    return rows

def run(root):
    msgs = []
    # 존재 여부
    for rel in NEEDED:
        p = os.path.join(root, rel)
        msgs.append(f"[CHECK] {rel}: {'OK' if os.path.exists(p) else 'MISSING'}")
    # 간단 스키마 체크(열 포함 여부)
    def has_cols(csv_path, cols):
        try:
            df = pd.read_csv(os.path.join(root, csv_path))
            miss = [c for c in cols if c not in df.columns]
            return "OK" if not miss else f"MISSING COLUMNS: {miss}"
        except Exception as e:
            return f"READ ERROR: {e}"

    msgs.append("[SCHEMA] A_coastline: " + has_cols("A_coastline/coast_line.csv",
        ["id","age_Ma","shoreline_type","quality_flag","coastline_buffer_km"]))
    msgs.append("[SCHEMA] R8_RSL: " + has_cols("R8_RSL/RSL_intake.csv",
        ["basin","site","datum","Age_BP","RSL_m","tectonic_corr","GIA_model","QC_flag"]))
    msgs.append("[SCHEMA] R10_Nile seismic: " + has_cols("R10_Nile/seismic_profile_summary.csv",
        ["line_id","lat","lon","thickness_m","thickness_sigma_m","facies","method","QC_flag"]))
    return "\n".join(msgs)+"\n"
