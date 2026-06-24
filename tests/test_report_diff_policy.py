import json

from braille_dotmatrix_engine.report_diff_policy import evaluate_report_diff_policy, main, write_report_diff_policy


def test_evaluate_report_diff_policy_passes_without_drift():
    policy = evaluate_report_diff_policy({'counts': {'added': 0, 'removed': 0, 'changed': 0, 'total': 0}, 'summary': 'reports match'})
    assert policy['status'] == 'pass'
    assert policy['drift_count'] == 0
    assert policy['policy'] == 'blocking'


def test_evaluate_report_diff_policy_fails_with_drift():
    policy = evaluate_report_diff_policy({'counts': {'added': 1, 'removed': 0, 'changed': 0, 'total': 1}, 'summary': 'reports differ'})
    assert policy['status'] == 'fail'
    assert policy['drift_count'] == 1


def test_write_report_diff_policy(tmp_path):
    diff = tmp_path / 'report_diff.json'
    output = tmp_path / 'drift_policy.json'
    diff.write_text(json.dumps({'counts': {'added': 0, 'removed': 0, 'changed': 0, 'total': 0}, 'summary': 'ok'}), encoding='utf-8')

    policy = write_report_diff_policy(diff, output)

    assert policy['status'] == 'pass'
    assert json.loads(output.read_text(encoding='utf-8')) == policy


def test_cli_enforce_passes_without_drift(tmp_path):
    diff = tmp_path / 'report_diff.json'
    output = tmp_path / 'drift_policy.json'
    diff.write_text(json.dumps({'counts': {'added': 0, 'removed': 0, 'changed': 0, 'total': 0}, 'summary': 'ok'}), encoding='utf-8')

    rc = main([str(diff), '--output', str(output), '--enforce'])

    assert rc == 0
    assert json.loads(output.read_text(encoding='utf-8'))['status'] == 'pass'


def test_cli_enforce_fails_with_drift(tmp_path):
    diff = tmp_path / 'report_diff.json'
    output = tmp_path / 'drift_policy.json'
    diff.write_text(json.dumps({'counts': {'added': 0, 'removed': 1, 'changed': 0, 'total': 1}, 'summary': 'drift'}), encoding='utf-8')

    rc = main([str(diff), '--output', str(output), '--enforce'])

    assert rc == 1
    assert json.loads(output.read_text(encoding='utf-8'))['status'] == 'fail'
