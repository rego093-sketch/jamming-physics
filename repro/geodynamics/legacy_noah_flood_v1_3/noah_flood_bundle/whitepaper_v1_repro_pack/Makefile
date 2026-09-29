.PHONY: prereg bio delta rsl all

prereg:
	python scripts/prereg_check.py config/prereg_omega_nogo.yml

bio:
	python scripts/bio_regression_stub.py data/PF_DataPack_v1.0/human_pigment_variants.tsv

delta:
	python scripts/delta_convert_stub.py data/RSL_Delta_BIO_Finalize/nile_core_map.csv

rsl:
	python scripts/rsl_fit_stub.py data/RSL_Delta_BIO_Finalize/RSL_all_sites.csv

all: prereg bio delta rsl
