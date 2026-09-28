#!/usr/bin/env python3
"""Figure generation driver (stub for *no_images* bundle).

The whitepaper's artifact tree specifies a figure generation entry point:
  scripts/make_figures.(py|sh)

This DOI bundle variant is explicitly built as "no_images" to satisfy archive
policies and automated validators that forbid raster image artifacts.

Behavior:
  - Prints an explicit message describing that figure generation is disabled.
  - Creates derived/figures/README.md with the same explanation if missing.

If you later create an "images-enabled" bundle, you can replace this script
with a real figure pipeline (e.g., Matplotlib → PDF) while preserving the CLI.
"""

from __future__ import annotations

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    figs = root / 'derived' / 'figures'
    figs.mkdir(parents=True, exist_ok=True)
    readme = figs / 'README.md'
    if not readme.exists():
        readme.write_text(
            """# derived/figures

This bundle is a *no_images* artifact package.

Figure generation is intentionally disabled here to avoid producing
raster image artifacts (png/jpg/gif/svg/webp).

If you need figures, build an images-enabled variant where this directory
contains PDF figure outputs and the corresponding generator scripts.
""",
            encoding='utf-8',
        )
    print('[INFO] make_figures.py: disabled (no_images bundle).')
    print(f'[INFO] figures directory: {figs.as_posix()}')


if __name__ == '__main__':
    main()
