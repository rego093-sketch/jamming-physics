#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_manifest.py
- scripts/make_manifest_sha256.py를 validation 폴더에서 호출할 수 있게 한 래퍼.
"""
import subprocess, sys
if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "scripts/make_manifest_sha256.py"]))
