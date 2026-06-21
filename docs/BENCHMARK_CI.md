# Benchmark CI

This document defines the v1.10.0 benchmark smoke layer.

## Purpose

The benchmark job is not a full performance lab. It is a CI safety gate that verifies the renderer still produces benchmarkable outputs with finite runtime, bounded memory, valid occupancy, and consistent schema metadata.

## CI job

The `benchmark-smoke` job runs on Python 3.11 and executes:

```bash
python -m braille_dotmatrix_engine.benchmark \
  --output-dir artifacts/benchmarks \
  --csv artifacts/benchmarks/benchmark.csv \
  --summary artifacts/benchmarks/benchmark_summary.json \
  --max-runtime-sec 120 \
  --max-rss-mb 4096
```

## Artifacts

The workflow uploads `artifacts/benchmarks` as the `benchmark-smoke` artifact. It contains benchmark CSV, benchmark summary JSON, per-case render reports, generated previews, and text outputs.

Generated benchmark artifacts are CI outputs and must not be committed to the repository.

## Validation

The benchmark validator checks:

- finite runtime
- bounded RSS peak memory
- occupancy in `[0, 1]`
- render report schema version
- benchmark row schema version

## Next use

Track B should use this artifact baseline before merging fast rasterizer changes.
