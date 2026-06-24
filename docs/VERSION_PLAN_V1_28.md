# v1.28.0 Version Plan — Blocking BRF contract drift policy

## Status

Implemented in `work-20260624-e`.

## Goals

- Convert BRF contract drift from observation-only to blocking policy.
- Keep diagnostic artifacts available before failing CI.
- Add a reusable report diff policy helper.
- Add tests for policy pass/fail behavior.
- Keep render, BRF, and benchmark schemas unchanged.

## Acceptance

- `report_diff_policy` can evaluate a diff result.
- CLI returns `0` for clean diff under `--enforce`.
- CLI returns `1` for drift under `--enforce`.
- CI writes `drift_policy.json`.
- CI uploads report, contract, diff, drift policy, and provenance.
- CI enforces drift only after artifact upload.

## Next version

`v1.29.0 — Intentional contract migration workflow`

Candidate goals:

- Add explicit contract update command or docs.
- Add PR review checklist for intentional snapshot changes.
- Optionally evaluate release-only signed attestations.
