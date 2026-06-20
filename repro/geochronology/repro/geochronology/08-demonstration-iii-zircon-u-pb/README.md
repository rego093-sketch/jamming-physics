# Demonstration III - zircon U-Pb, the general case (open data)

Common-Pb screening/correction and detrital inheritance on fully open
IsoplotR example datasets (Vermeesch 2018):
  clean suite (UPb1): concordant ~249 Ma
  204Pb suite (UPb4): RAW ~67% discordant -> 204Pb-corrected concordant ~312 Ma
    (correction depends on an ASSUMED common-Pb composition)
  detrital (DZ, N1): ~129-2994 Ma; only the youngest cluster bounds deposition

## Run
    pip install -r requirements.txt
    python 02_isoplotr_common_pb_detrital.py   # clones IsoplotR if absent (git+internet)
