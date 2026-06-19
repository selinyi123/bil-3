import pytest
from braille_dotmatrix_engine.cli import main

def test_cli_rejects_zero_width():
    with pytest.raises(SystemExit):
        main(['--width-cells', '0'])
