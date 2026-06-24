from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .json_utils import dumps_json, write_json
from .report_diff import diff_reports

CONTRACT_MIGRATION_SCHEMA_VERSION = "1.0"
DEFAULT_REVIEW_CHECKLIST = (
    "Confirm that every changed field is intentional.",
    "Confirm that the proposed contract was generated from the documented CLI path.",
    "Confirm that tests and checked-in snapshots are updated together.",
    "Confirm that drift is not hiding an unintended renderer or profile default change.",
)

__all__ = ["CONTRACT_MIGRATION_SCHEMA_VERSION", "propose_contract_migration", "write_contract_migration"]


def _changed_paths(diff: dict[str, Any], *, limit: int = 100) -> tuple[list[str], bool]:
    paths: list[str] = []
    truncated = False
    for key in ("added", "removed", "changed"):
        for item in diff.get(key, []):
            path = str(item.get("path", ""))
            if not path:
                continue
            if len(paths) >= limit:
                truncated = True
                continue
            paths.append(path)
    return paths, truncated


def propose_contract_migration(
    current: Any,
    proposed: Any,
    *,
    reason: str = "",
    author: str | None = None,
    source: str | None = None,
    max_changed_paths: int = 100,
) -> dict[str, Any]:
    diff = diff_reports(current, proposed)
    drift_count = int(diff["counts"]["total"])
    normalized_reason = reason.strip()
    if drift_count > 0 and not normalized_reason:
        raise ValueError("contract migration reason is required when drift exists")
    changed_paths, changed_paths_truncated = _changed_paths(diff, limit=max_changed_paths)
    status = "no_change" if drift_count == 0 else "migration_required"
    return {
        "schema": "braille-dotmatrix-engine.contract_migration",
        "schema_version": CONTRACT_MIGRATION_SCHEMA_VERSION,
        "status": status,
        "requires_review": drift_count > 0,
        "reason": normalized_reason,
        "author": author,
        "source": source,
        "drift_count": drift_count,
        "summary": diff["summary"],
        "counts": diff["counts"],
        "changed_paths": changed_paths,
        "changed_paths_truncated": changed_paths_truncated,
        "review_checklist": list(DEFAULT_REVIEW_CHECKLIST),
        "diff": diff,
    }


def write_contract_migration(
    current_path: str | Path,
    proposed_path: str | Path,
    output_path: str | Path,
    *,
    reason: str = "",
    author: str | None = None,
    source: str | None = None,
) -> dict[str, Any]:
    current = json.loads(Path(current_path).read_text(encoding="utf-8"))
    proposed = json.loads(Path(proposed_path).read_text(encoding="utf-8"))
    result = propose_contract_migration(current, proposed, reason=reason, author=author, source=source)
    write_json(result, output_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a review record for an intentional JSON contract migration")
    parser.add_argument("current", help="current checked-in contract JSON path")
    parser.add_argument("proposed", help="proposed generated contract JSON path")
    parser.add_argument("--output", required=True, help="migration review JSON output path")
    parser.add_argument("--reason", default="", help="required when the proposed contract differs from the current contract")
    parser.add_argument("--author", default=None, help="optional author or actor recorded in the migration review JSON")
    parser.add_argument("--source", default=None, help="optional source command, artifact, PR, or workflow run")
    args = parser.parse_args(argv)
    try:
        result = write_contract_migration(args.current, args.proposed, args.output, reason=args.reason, author=args.author, source=args.source)
    except ValueError as exc:
        print(str(exc))
        return 2
    print(dumps_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
