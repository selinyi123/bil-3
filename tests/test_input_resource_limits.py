import cv2
import numpy as np
import pytest

from braille_dotmatrix_engine import BrailleArtConfig, process_image
from braille_dotmatrix_engine.validation import validate_config


def test_validate_config_rejects_invalid_input_resource_limits():
    cfg = BrailleArtConfig()
    cfg.max_input_pixels = 0
    with pytest.raises(ValueError, match='max_input_pixels'):
        validate_config(cfg)

    cfg = BrailleArtConfig()
    cfg.max_input_file_bytes = 0
    with pytest.raises(ValueError, match='max_input_file_bytes'):
        validate_config(cfg)

    cfg = BrailleArtConfig()
    cfg.max_input_pixels = 10.5
    with pytest.raises(ValueError, match='max_input_pixels'):
        validate_config(cfg)


def test_process_image_rejects_input_file_over_byte_limit(tmp_path):
    image = tmp_path / 'small.png'
    cv2.imwrite(str(image), np.zeros((8, 8, 3), dtype=np.uint8))
    cfg = BrailleArtConfig(output_width_cells=4, max_input_file_bytes=1)
    with pytest.raises(ValueError, match='max_input_file_bytes'):
        process_image(image, cfg, tmp_path / 'out.png', tmp_path / 'out.txt', tmp_path / 'report.json')


def test_process_image_rejects_input_over_pixel_limit(tmp_path):
    image = tmp_path / 'small.png'
    cv2.imwrite(str(image), np.zeros((16, 16, 3), dtype=np.uint8))
    cfg = BrailleArtConfig(output_width_cells=4, max_input_pixels=10)
    with pytest.raises(ValueError, match='max_input_pixels'):
        process_image(image, cfg, tmp_path / 'out.png', tmp_path / 'out.txt', tmp_path / 'report.json')
