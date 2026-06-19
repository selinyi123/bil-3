# Metrics

## Purpose

v1.2 adds a quality metrics layer to make each render report auditable.

## Report fields

`quality_metrics` contains:

- `mse`: mean squared error between sampled values and blurred binary reconstruction.
- `psnr`: peak signal-to-noise ratio derived from MSE.
- `edge_score`: similarity between source dot-value edges and binary-dot edges.
- `occupancy`: active dot count, total dot count, and active-dot ratio.
- `local_density_over_limit`: ratio of local areas above configured density limit.

## Design notes

The metrics do not replace tactile expert review. They provide deterministic engineering signals for regression testing, dither comparison, and later benchmark reports.
