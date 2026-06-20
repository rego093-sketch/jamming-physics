# Demonstration II - zircon U-Pb, the canonical case (Lava Creek Tuff)

Reproduces the eruption age by classifying 183 SHRIMP-RG analyses strictly
by CRYSTAL POSITION (age-independent):
  faces (autocryst) n=70 -> 626.5 +/- 2.9 ka  (reproduces published rim age)
  cores (antecryst) n=62 -> 668.8 +/- 3.2 ka  (older; excluded)
  inter-zone        n=25 -> 649.8 ka
  EBT (other unit)  n=26 -> 769.3 ka          (excluded)

## Run
    pip install -r requirements.txt
    python 01_lava_creek_canonical.py [path/to/dss1.xls]

## Data (obtain from publisher; not redistributed)
Matthews, Vazquez & Calvert (2015), G-cubed 16:2508, doi:10.1002/2015GC005881,
Supporting Information Dataset S1 (`*dss1*.xls`). Place it in `data/`.
