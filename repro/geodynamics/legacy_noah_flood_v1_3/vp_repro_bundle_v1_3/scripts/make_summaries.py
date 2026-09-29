from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path
from typing import List, Tuple

import pandas as pd

from common import repo_root

def _read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    if path.suffix.lower() == ".tsv":
        return pd.read_csv(path, sep="\t")
    raise ValueError(f"unsupported table type: {path}")

def summarize_dir(dir_path: Path, out_csv: Path) -> None:
    rows: List[Tuple[str, int, int, str]] = []
    for p in sorted(dir_path.rglob("*")):
        if p.is_file() and p.suffix.lower() in [".csv", ".tsv"]:
            df = _read_table(p)
            rows.append((p.relative_to(repo_root()).as_posix(), int(df.shape[0]), int(df.shape[1]), ",".join(map(str, df.columns))))

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "rows", "cols", "columns"])
        for r in rows:
            w.writerow(list(r))

def main() -> int:
    root = repo_root()
    summarize_dir(root / "data" / "mini", root / "outputs" / "mini" / "summary_tables.csv")
    summarize_dir(root / "data" / "full", root / "outputs" / "full" / "summary_tables.csv")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
