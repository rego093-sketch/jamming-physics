#!/usr/bin/env bash
# Re-fetch offloaded large assets from Zenodo into their repo-relative paths.
# Fill ZENODO_BASE with the record's file base URL, then run from repo root.
set -euo pipefail
ZENODO_BASE="${ZENODO_BASE:?set ZENODO_BASE to the Zenodo record files URL}"

mkdir -p "$(dirname repro/disease_wp/data/raw/orphanet/en_product1.xml)"
curl -L "$ZENODO_BASE/en_product1.xml" -o "repro/disease_wp/data/raw/orphanet/en_product1.xml"
echo "fb2fbe8cc3f04c2ffb3fac3c498bce75e56cfc46b5475e3da30e97f8349140db  repro/disease_wp/data/raw/orphanet/en_product1.xml" | sha256sum -c -

mkdir -p "$(dirname repro/disease_wp/data/raw/orphanet/en_product4.xml)"
curl -L "$ZENODO_BASE/en_product4.xml" -o "repro/disease_wp/data/raw/orphanet/en_product4.xml"
echo "82079cfb9e6fdce0280001338618ecc8f4a5ae76d66f8e7c22e39fcdaebdebb7  repro/disease_wp/data/raw/orphanet/en_product4.xml" | sha256sum -c -

mkdir -p "$(dirname repro/disease_wp/data/raw/medgen/inscope_esummary.jsonl.gz)"
curl -L "$ZENODO_BASE/inscope_esummary.jsonl.gz" -o "repro/disease_wp/data/raw/medgen/inscope_esummary.jsonl.gz"
echo "0999599642614b8fe922bd82c294dfb9e5310ce22257b8e6de345c2fa4534e3c  repro/disease_wp/data/raw/medgen/inscope_esummary.jsonl.gz" | sha256sum -c -

