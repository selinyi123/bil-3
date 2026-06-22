from __future__ import annotations

from pathlib import Path
from typing import Any

from .brf import validate_brf_text
from .embosser import GenericEmbosserProfile


def resolve_brf_input_paths(root: str | Path, pattern: str = '*.txt') -> list[Path]:
    root_path = Path(root)
    if root_path.is_file():
        return [root_path]
    if not root_path.exists():
        raise FileNotFoundError(str(root_path))
    files = sorted(path for path in root_path.glob(pattern) if path.is_file())
    if not files:
        raise FileNotFoundError(f'no files matched {pattern} under {root_path}')
    return files


def aggregate_brf_file_reports(file_reports: list[dict[str, Any]]) -> dict[str, Any]:
    by_reason: dict[str, int] = {}
    ok_files = 0
    warning_files = 0
    error_files = 0
    warning_count = 0
    error_count = 0
    for item in file_reports:
        brf = item['brf_export']
        diagnostics = brf['diagnostics']
        if diagnostics['total'] == 0:
            ok_files += 1
        if brf['warning_count'] > 0:
            warning_files += 1
        if brf['error_count'] > 0:
            error_files += 1
        warning_count += int(brf['warning_count'])
        error_count += int(brf['error_count'])
        for reason, count in diagnostics.get('by_reason', {}).items():
            by_reason[reason] = by_reason.get(reason, 0) + int(count)
    return {
        'total_files': len(file_reports),
        'ok_files': ok_files,
        'warning_files': warning_files,
        'error_files': error_files,
        'issue_files': len(file_reports) - ok_files,
        'warning_count': warning_count,
        'error_count': error_count,
        'by_reason': by_reason,
    }


def validate_brf_files(paths: list[Path], profile: GenericEmbosserProfile | None = None, *, strict: bool = False) -> dict[str, Any]:
    file_reports: list[dict[str, Any]] = []
    for path in paths:
        brf_report = validate_brf_text(path.read_text(encoding='utf-8'), profile, strict=strict)
        file_reports.append({
            'path': str(path),
            'summary': brf_report['summary'],
            'ok': brf_report['diagnostics']['total'] == 0,
            'warning_count': brf_report['warning_count'],
            'error_count': brf_report['error_count'],
            'brf_export': brf_report,
        })
    return {
        'aggregate': aggregate_brf_file_reports(file_reports),
        'files': file_reports,
    }
