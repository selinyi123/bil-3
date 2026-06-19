import numpy as np
from braille_dotmatrix_engine import BrailleArtConfig, decode_braille_cell, encode_braille_cell, unicode_roundtrip_test
from braille_dotmatrix_engine.engine import build_dot_grid, gaussian_dot_sampling_grid, process_tiles

def test_unicode_roundtrip_all_patterns():
    assert unicode_roundtrip_test()

def test_cell_roundtrip():
    dots = np.array([1, 0, 1, 0, 0, 1, 0, 1], dtype=bool)
    assert np.array_equal(decode_braille_cell(encode_braille_cell(dots)), dots)

def test_tiled_sampling_close_to_full():
    rng = np.random.default_rng(123)
    img = rng.random((96, 128), dtype=np.float32)
    cfg = BrailleArtConfig(output_width_cells=16, tile_size_px=64, tile_overlap_px=16)
    coords, _, _, spacing = build_dot_grid(cfg, img.shape)
    full = gaussian_dot_sampling_grid(img, coords, spacing, cfg)
    tiled = process_tiles(img, coords, cfg)
    assert np.mean(np.abs(full - tiled)) < 0.05
