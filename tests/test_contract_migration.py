import json

from braille_dotmatrix_engine.contract_migration import main, propose_contract_migration, write_contract_migration


def test_propose_contract_migration_no_change_without_reason():
    current = {'aggregate': {'total_files': 1}, 'files': [{'name': 'a.txt', 'ok': True}]}

    migration = propose_contract_migration(current, current)

    assert migration['status'] == 'no_change'
    assert migration['requires_review'] is False
    assert migration['drift_count'] == 0
    assert migration['reason'] == ''
    assert migration['changed_paths'] == []


def test_propose_contract_migration_requires_reason_for_drift():
    current = {'summary': 'old'}
    proposed = {'summary': 'new'}

    try:
        propose_contract_migration(current, proposed)
    except ValueError as exc:
        assert 'reason is required' in str(exc)
    else:
        raise AssertionError('expected ValueError for drift without reason')


def test_propose_contract_migration_with_reason_records_review_metadata():
    migration = propose_contract_migration(
        {'summary': 'old'},
        {'summary': 'new'},
        reason='default BRF profile migration',
        author='ci',
        source='workflow run 123',
    )

    assert migration['status'] == 'migration_required'
    assert migration['requires_review'] is True
    assert migration['drift_count'] == 1
    assert migration['reason'] == 'default BRF profile migration'
    assert migration['author'] == 'ci'
    assert migration['source'] == 'workflow run 123'
    assert migration['changed_paths'] == ['summary']
    assert migration['counts']['changed'] == 1
    assert migration['review_checklist']
    assert migration['diff']['changed'][0]['old'] == 'old'
    assert migration['diff']['changed'][0]['new'] == 'new'


def test_write_contract_migration(tmp_path):
    current = tmp_path / 'current.json'
    proposed = tmp_path / 'proposed.json'
    output = tmp_path / 'migration.json'
    current.write_text(json.dumps({'summary': 'old'}), encoding='utf-8')
    proposed.write_text(json.dumps({'summary': 'new'}), encoding='utf-8')

    migration = write_contract_migration(current, proposed, output, reason='intentional update')

    assert migration['status'] == 'migration_required'
    assert json.loads(output.read_text(encoding='utf-8')) == migration


def test_cli_returns_two_when_drift_has_no_reason(tmp_path):
    current = tmp_path / 'current.json'
    proposed = tmp_path / 'proposed.json'
    output = tmp_path / 'migration.json'
    current.write_text(json.dumps({'summary': 'old'}), encoding='utf-8')
    proposed.write_text(json.dumps({'summary': 'new'}), encoding='utf-8')

    rc = main([str(current), str(proposed), '--output', str(output)])

    assert rc == 2
    assert not output.exists()


def test_cli_writes_migration_with_reason(tmp_path):
    current = tmp_path / 'current.json'
    proposed = tmp_path / 'proposed.json'
    output = tmp_path / 'migration.json'
    current.write_text(json.dumps({'summary': 'old'}), encoding='utf-8')
    proposed.write_text(json.dumps({'summary': 'new'}), encoding='utf-8')

    rc = main([str(current), str(proposed), '--output', str(output), '--reason', 'intentional update'])

    assert rc == 0
    assert json.loads(output.read_text(encoding='utf-8'))['reason'] == 'intentional update'
