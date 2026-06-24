# v1.25.0 Report diff research

## Scope

This pass focuses on explaining report contract drift for BRF and batch JSON reports. It does not repeat earlier BRF fixture, batch preflight, or CI artifact research.

## External findings

- RFC 6902 JSON Patch is useful for machine-applied patches, but it is less readable as a user-facing explanation of report drift.
- Generic JSON diff libraries can add dependency and configuration surface.
- This repository only needs stable added, removed, and changed field reporting for small JSON reports.

## Decision

Add a small dependency-free report diff helper:

- recursively compare dictionaries,
- compare lists by index,
- emit `added`, `removed`, and `changed`,
- include aggregate counts and a compact summary,
- expose CLI report diff mode.

## Next slice

`v1.26.0` should evaluate CI artifact provenance or release attestation for wheel, benchmark, and BRF report artifacts.
