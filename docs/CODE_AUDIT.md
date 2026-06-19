# Code Audit

## Audit scope

This audit covers the current V1 Python package structure, with emphasis on Unicode Braille correctness, rendering pipeline stability, version consistency, tests, and documentation.

## Findings fixed in v1.4.0 branch

### 1. Unicode Braille physical layout bug

Severity: high.

The prior matrix encoder mapped the 4x2 physical matrix in row-major order into logical dots 1..8. That is incorrect for Unicode 8-dot Braille.

Correct layout:

```text
1 4
2 5
3 6
7 8
```

Correct bit layout:

```text
bit0 bit3
bit1 bit4
bit2 bit5
bit6 bit7
```

Fix:

- Added `BRAILLE_BIT_LAYOUT` and `BRAILLE_WEIGHTS`.
- Rewrote matrix encoding around the official layout.
- Added matrix decode support.
- Added regression tests for every physical dot position.

### 2. Version drift

Severity: medium.

`README.md` reported `v1.1.2`, while `pyproject.toml` reported `1.3.0`.

Fix:

- Bumped project version to `1.4.0`.
- Updated README to match.

### 3. Insufficient public positioning

Severity: medium.

The README described the repository as a simple Unicode Braille dot-matrix art renderer. That undersold the actual project direction and made it look like a generic converter.

Fix:

- Expanded README with current capabilities, CLI/API usage, validation layer, outputs, and roadmap direction.
- Added `ROADMAP.md`.
- Expanded `docs/PROJECT_DESIGN.md`.

## Remaining issues

### A. Sequential error-diffusion loops

`dither.py` uses nested loops. This is algorithmically normal for classic error diffusion, but performance can degrade on large dot grids.

Recommendation:

- Keep it for correctness in V1.
- Add optional fast ordered/blue-noise dithering in V1.6.
- Add benchmark gating before trying to optimize prematurely.

### B. PIL dot rendering loops

`raster.py` draws dots in Python loops. It is acceptable for current outputs, but will become a bottleneck for very large dot fields.

Recommendation:

- Replace with OpenCV vectorized rasterization or precomputed disk kernels in V1.5/V1.6.

### C. Tactile validation is not yet manufacturing-grade

Current validation checks basic geometry but not physical collisions, local tactile crowding, or device-specific embossing constraints.

Recommendation:

- Add dot collision detection.
- Add strict mode to block invalid tactile exports.
- Add material/printer acceptance profiles.

### D. Semantic-aware processing is not implemented yet

The code is still pixel-first. It does not yet distinguish text, line art, subject, and background regions.

Recommendation:

- Introduce `SemanticRegionMap` in V2.
- Allow per-region rendering policies.
