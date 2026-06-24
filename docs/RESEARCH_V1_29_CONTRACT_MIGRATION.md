# v1.29.0 Intentional contract migration research

## Scope

This pass adds a controlled workflow for intentional JSON contract and snapshot updates after v1.28.0 made BRF contract drift blocking.

## External findings

- Snapshot testing workflows reduce regression noise by comparing generated output against checked-in expected output, but they create maintenance overhead when output changes intentionally.
- Golden-file and approval-style workflows generally require a human review step before accepting updated outputs.
- GitHub Actions workflow reliability research suggests keeping automation changes explicit and small, because complex workflow configurations increase maintenance load.
- Pull request templates are a lightweight way to force migration-specific checklist items without changing CI permissions or making workflow YAML more complex.

## Decision

Add a repository-local contract migration helper rather than weakening the v1.28 blocking gate.

The helper produces a JSON review record with:

- diff counts
- changed paths
- embedded diff
- review checklist
- required migration reason when drift exists

## Rationale

Blocking drift is correct for normal CI. Intentional drift still needs a governed update path. Requiring a migration reason and preserving the diff makes snapshot updates auditable without adding release signing or permissions complexity in this slice.

## Non-goals

- No automatic snapshot rewriting in CI.
- No automatic commit from workflow.
- No artifact attestation in this version.
- No schema version bump, because the render/BRF report contracts are unchanged.

## Next slice

`v1.30.0` should evaluate release-only artifact attestations or a stronger signed provenance path for release outputs.
