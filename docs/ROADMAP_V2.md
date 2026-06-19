# Roadmap V2

This roadmap moves the project from a Braille-only renderer into a multi-symbol visual encoding engine and then into a semantic tactile graphics engine.

## v1.8.0 — ASCII and Braille enhancement

- Add `ASCII_MONO` and `ASCII_COLOR` rendering modes.
- Add edge-aware Braille sampling enhancement before dithering.
- Add CLI smoke paths for ASCII output.
- Keep JSON reports explicit about `ascii_render` and `braille_enhancement`.

## v1.9.0 — Benchmark CI hardening

- Upload benchmark CSV as a GitHub Actions artifact.
- Add a small benchmark smoke job that runs only on synthetic images.
- Track runtime, RSS peak, occupancy, and basic quality metrics.
- Establish baseline thresholds to detect severe regressions.

## v1.10.0 — Rasterizer performance

- Replace PIL ellipse loops with an OpenCV or NumPy kernel rasterizer.
- Add a fast path for dense dot grids.
- Keep output determinism identical across Python versions.

## v2.0.0 — Semantic Braille Engine

- Introduce semantic region maps.
- Split text, line-art, natural-image, and background regions.
- Add region-specific rendering policies.
- Apply importance-weighted dot allocation.
- Report semantic coverage and per-region occupancy.

## v2.1.0 — Tactile graphics quality score

- Define a `Braille Quality Score` with separate tactile, semantic, compression, and manufacturability dimensions.
- Add failure categories for clutter, collision, poor edge continuity, and low subject preservation.

## v3.0.0 — Visual Semantic Encoding Layer

- Export a visual semantic graph alongside Braille/SVG/PNG/ASCII outputs.
- Treat Braille and ASCII as renderers of a general visual semantic runtime.
