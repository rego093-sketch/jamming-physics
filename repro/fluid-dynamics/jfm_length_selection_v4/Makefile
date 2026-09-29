    .PHONY: all v3 dns analyze assert clean

    all: v3 dns analyze assert

    v3:
		@if [ ! -d v3 ]; then unzip -q JFM_DOI_FULLSTORY_v3.zip -d v3; else echo "v3 already unpacked"; fi

    dns:
		PYTHONPATH=code python scripts/run_dns_suite.py

    analyze:
		PYTHONPATH=code python scripts/analyze_dns_suite.py

    assert:
		PYTHONPATH=code python scripts/assert_reproduction.py --v3-root v3

    clean:
		rm -f data/dns_runs/*.npz data/dns_runs/dns_suite_with_Sb.csv data/dns_runs/slope.txt || true
