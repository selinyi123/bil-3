from braille_dotmatrix_engine.cli import main

def test_cli_creates_nested_output_dirs(tmp_path):
    out_dir = tmp_path / 'nested' / 'outputs'
    code = main(['--width-cells', '8', '--output-png', str(out_dir / 'out.png'), '--output-txt', str(out_dir / 'out.txt'), '--report-json', str(out_dir / 'report.json')])
    assert code == 0
    assert (out_dir / 'out.png').exists()
    assert (out_dir / 'out.txt').exists()
    assert (out_dir / 'report.json').exists()
