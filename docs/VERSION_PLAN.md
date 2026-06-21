# Version Plan

## v1.10.2 — Hardening release

Status: implemented in `fix/v1.10.2-hardening`.

Goals:

- reject invalid public configuration before rendering,
- unify PNG and SVG physical radius semantics,
- expose package version in reports,
- add regression tests for validation and geometry consistency,
- document external research and next steps.

Acceptance:

- `pytest -q` passes,
- invalid render modes are rejected,
- invalid dither candidates are rejected,
- invalid geometry/material/chromatic parameters are rejected,
- SVG export uses the same compensated radius policy as PNG output.

## v1.10.3 — Mode-specific pipeline semantics

Goals:

- split ASCII mode into a fast path that does not require full Braille diagnostics by default,
- split CHROMATIC report semantics from tactile-only roundtrip validation,
- add explicit report sections: `input`, `renderer`, `artifacts`, `validation`, `diagnostics`,
- keep backward-compatible top-level fields for one minor cycle.

Acceptance:

- ASCII mode can render without Braille dither unless diagnostics are enabled,
- report clearly marks skipped diagnostics,
- benchmark includes at least one 1080p synthetic image.

## v1.11.0 — Renderer strategy architecture

Goals:

- introduce renderer strategy classes for TACTILE, SCREEN, CHROMATIC, ASCII_MONO, and ASCII_COLOR,
- add shared artifact writer,
- isolate geometry policy from renderer code,
- prepare a stable `RenderContext` and `RenderResult` internal API.

Acceptance:

- `process_image` becomes orchestration rather than per-mode branching,
- each renderer has independent unit tests,
- output artifacts remain compatible with v1.10 reports.

## v1.12.0 — Large-image benchmark and memory reporting

Goals:

- add synthetic 1080p and 4K benchmark profiles,
- add estimated peak-memory report,
- add optional stress benchmark profile for 8K images,
- compare tiled sampling behavior across image sizes.

Acceptance:

- medium benchmark runs in CI or scheduled benchmark workflow,
- stress benchmark is available but not mandatory in PR CI,
- render report includes memory-estimate fields.

## v2.0.0 — Semantic Braille Engine

Goals:

- introduce semantic region map schema,
- support text, line-art, natural-image, background, and chart-region labels,
- add region-specific tactile policy,
- apply importance-weighted dot allocation.

Acceptance:

- pipeline can consume a semantic map,
- report includes region coverage and per-region occupancy,
- semantic regions can change tactile output density and edge preservation.

## v2.1.0 — Tactile quality score

Goals:

- define tactile quality score dimensions: manufacturability, readability, semantic preservation, clutter, edge continuity,
- add failure categories,
- add quality snapshots for benchmark artifacts.

Acceptance:

- each render receives a structured quality score,
- reports include actionable failure categories,
- tests cover high-clutter and low-edge-continuity cases.
