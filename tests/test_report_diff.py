import json

from braille_dotmatrix_engine.cli import main
from braille_dotmatrix_engine.report_diff import diff_reports


def test_diff_reports_match():
    diff = diff_reports({'a': 1, 'b': {'c': 2}}, {'a': 1, 'b': {'c': 2}})
    assert diff['counts'] == {'added': 0, 'removed': 0, 'changed': 0, 'total': 0}
    assert diff['summary'] == 'reports match; added=0; removed=0; changed=0'


def test_diff_reports_added_removed_changed_nested_values():
    diff = diff_reports(
        {'a': 1, 'b': {'old': True, 'same': 2}, 'items': [1, 2]},
        {'a': 2, 'b': {'same': 2, 'new': True}, 'items': [1, 3, 4]},
    )
    assert diff['counts'] == {'added': 2, 'removed': 1, 'changed': 2, 'total': 5}
    assert {'path': 'b.new', 'value': True} in diff['added']
    assert {'path': 'items[2]', 'value': 4} in diff['added']
    assert {'path': 'b.old', 'value': True} in diff['removed']
    assert {'path': 'a', 'old': 1, 'new': 2} in diff['changed']
    assert {'path': 'items[1]', 'old': 2, 'new': 3} in diff['changed']
    assert diff['summary'] == 'reports differ; added=2; removed=1; changed=2'


def test_cli_report_diff_identical(tmp_path):
    old = tmp_path / 'old.json'
    new = tmp_path / 'new.json'
    out = tmp_path / 'diff.json'
    payload = {'brf_export': {'summary': 'BRF ok;', 'warning_count': 0}}
    old.write_text(json.dumps(payload), encoding='utf-8')
    new.write_text(json.dumps(payload), encoding='utf-8')

    rc = main(['--report-diff-old', str(old), '--report-diff-new', str(new), '--report-json', str(out)])

    assert rc == 0
    diff = json.loads(out.read_text(encoding='utf-8'))
    assert diff['counts']['total'] == 0


def test_cli_report_diff_changed(tmp_path):
    old = tmp_path / 'old.json'
    new = tmp_path / 'new.json'
    out = tmp_path / 'diff.json'
    old.write_text(json.dumps({'batch': {'aggregate': {'ok_files': 1}}}), encoding='utf-8')
    new.write_text(json.dumps({'batch': {'aggregate': {'ok_files': 2, 'issue_files': 1}}}), encoding='utf-8')

    rc = main(['--report-diff-old', str(old), '--report-diff-new', str(new), '--report-json', str(out)])

    assert rc == 1
    diff = json.loads(out.read_text(encoding='utf-8'))
    assert {'path': 'batch.aggregate.ok_files', 'old': 1, 'new': 2} in diff['changed']
    assert {'path': 'batch.aggregate.issue_files', 'value': 1} in diff['added']
