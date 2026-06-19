from PIL import Image
from braille_dotmatrix_engine import BrailleArtConfig, create_demo_image, process_image

def test_screen_mode_outputs_rgb(tmp_path):
    image = create_demo_image(tmp_path / 'demo.png', size=96)
    cfg = BrailleArtConfig(output_width_cells=12, tile_size_px=48, tile_overlap_px=12, render_spacing_px=6, mode='SCREEN')
    process_image(image, cfg, tmp_path / 'screen.png', tmp_path / 'screen.txt', tmp_path / 'screen.json')
    assert Image.open(tmp_path / 'screen.png').mode == 'RGB'
