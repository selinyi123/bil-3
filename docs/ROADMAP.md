# Roadmap

## v1.1.x hardening

- Stabilize package layout, CLI, CI, tests, and README.
- Keep Unicode roundtrip and raster roundtrip as mandatory checks.
- Avoid logical-dot mutation for material compensation.

## v1.2 quality metrics

- Add MSE, PSNR, SSIM-style local metrics, occupancy reports, and edge-preservation metrics.
- Add benchmark fixtures for portrait, text, line art, and natural images.

## v1.3 tactile geometry

- Split tactile geometry into intra-cell spacing, inter-cell spacing, line spacing, dot height, and printer tolerance.
- Add SVG export for laser embossing and tactile graphics workflows.

## v1.4 acceleration

- Add optional Numba acceleration for dithering and raster analysis.
- Add serpentine error diffusion.

## v1.5 advanced rendering

- Add color-aware screen rendering.
- Add semantic region masks for text, line art, and natural image zones.

## v2.0 productization

- Build a local web UI.
- Add batch conversion, preset profiles, report dashboards, and export bundles.
