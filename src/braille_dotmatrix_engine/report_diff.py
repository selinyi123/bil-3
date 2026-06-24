from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .json_utils import to_json_safe

__all__ = ["diff_reports", "summarize_diff"]


def _path_join(parent: str, key: str) -> str:
    return key if not parent else f"{parent}.{key}"


def _record_added(path: str, value: Any) -> dict[str, Any]:
    return {"path": path, "value": to_json_safe(value)}


def _record_removed(path: str, value: Any) -> dict[str, Any]:
    return {"path": path, "value": to_json_safe(value)}


def _record_changed(path: str, old: Any, new: Any) -> dict[str, Any]:
    return {"path": path, "old": to_json_safe(old), "new": to_json_safe(new)}


def _diff_values(old: Any, new: Any, path: str, result: dict[str, list[dict[str, Any]]]) -> None:
    if isinstance(old, Mapping) and isinstance(new, Mapping):
        old_keys = set(old.keys())
        new_keys = set(new.keys())
        for key in sorted(old_keys - new_keys, key=str):
            result["removed"].append(_record_removed(_path_join(path, str(key)), old[key]))
        for key in sorted(new_keys - old_keys, key=str):
            result["added"].append(_record_added(_path_join(path, str(key)), new[key]))
        for key in sorted(old_keys & new_keys, key=str):
            _diff_values(old[key], new[key], _path_join(path, str(key)), result)
        return

    if isinstance(old, list) and isinstance(new, list):
        common = min(len(old), len(new))
        for index in range(common):
            _diff_values(old[index], new[index], f"{path}[{index}]", result)
        for index in range(common, len(old)):
            result["removed"].append(_record_removed(f"{path}[{index}]", old[index]))
        for index in range(common, len(new)):
            result["added"].append(_record_added(f"{path}[{index}]", new[index]))
        return

    if old != new:
        result["changed"].append(_record_changed(path or "$", old, new))


def summarize_diff(result: dict[str, Any]) -> str:
    counts = result["counts"]
    total = counts["total"]
    if total == 0:
        return "reports match; added=0; removed=0; changed=0"
    return f"reports differ; added={counts['added']}; removed={counts['removed']}; changed={counts['changed']}"


def diff_reports(old: Any, new: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"added": [], "removed": [], "changed": []}
    _diff_values(to_json_safe(old), to_json_safe(new), "", result)
    result["counts"] = {
        "added": len(result["added"]),
        "removed": len(result["removed"]),
        "changed": len(result["changed"]),
    }
    result["counts"]["total"] = result["counts"]["added"] + result["counts"]["removed"] + result["counts"]["changed"]
    result["summary"] = summarize_diff(result)
    return result
