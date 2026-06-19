from pathlib import Path
from braille_dotmatrix_engine.cli import main


def test_cli_generates_outputs(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(['--width-cells', '12', '--output-png', 'cli.png', '--output-txt', 'cli.txt', '--report-json', 'cli.json']) == 0
    assert (tmp_path / 'cli.png').exists()
    assert (tmp_path / 'cli.txt').exists()
    assert (tmp_path / 'cli.json').exists()


def test_cli_chromatic_mode_generates_outputs(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(['--width-cells', '12', '--mode', 'CHROMATIC', '--output-png', 'chromatic.png', '--output-txt', 'chromatic.txt', '--report-json', 'chromatic.json']) == 0
    assert (tmp_path / 'chromatic.png').exists()
    assert (tmp_path / 'chromatic.txt').exists()
    assert (tmp_path / 'chromatic.json').exists()


def test_cli_benchmark_generates_csv(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(['--benchmark', '--benchmark-csv', 'bench.csv']) == 0
    assert (tmp_path / 'bench.csv').exists()
