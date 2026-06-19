from braille_dotmatrix_engine import BrailleArtConfig, create_demo_image, process_image

def test_process_image_creates_outputs(tmp_path):
    image = create_demo_image(tmp_path / 'demo.png', size=128)
    cfg = BrailleArtConfig(output_width_cells=16, tile_size_px=64, tile_overlap_px=16, render_spacing_px=6)
    report = process_image(image, cfg, tmp_path / 'out.png', tmp_path / 'out.txt', tmp_path / 'report.json')
    assert (tmp_path / 'out.png').exists()
    assert (tmp_path / 'out.txt').exists()
    assert (tmp_path / 'report.json').exists()
    assert report['validation']['unicode_roundtrip'] is True
    assert report['cells_shape'][1] == 16
