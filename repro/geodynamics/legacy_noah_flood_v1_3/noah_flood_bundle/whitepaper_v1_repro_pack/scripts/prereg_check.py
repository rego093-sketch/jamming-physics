#!/usr/bin/env python3
import sys, yaml, json
from pathlib import Path

def main(cfg_path: str):
    cfg = yaml.safe_load(Path(cfg_path).read_text(encoding='utf-8'))
    out = {"checked": [h["id"] for h in cfg["hypotheses"]],
           "status": "CONFIG_LOADED"}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prereg_check.py CONFIG_YAML", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
