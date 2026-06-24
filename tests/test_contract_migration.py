import json
from pathlib import Path

from braille_dotmatrix_engine.contract_migration import build_migration_plan


def test_migration_plan_detects_no_drift():
    old = {"counts": {"total": 0}}
    new = {"counts": {"total": 0}}

    plan = build_migration_plan(old, new)

    assert plan.should_migrate is False
    assert plan.drift_count == 0


def test_migration_plan_detects_drift():
    old = {"counts": {"total": 0}}
    new = {"counts": {"total": 3}}

    plan = build_migration_plan(old, new)

    assert plan.should_migrate is True
    assert plan.drift_count == 3
