from .config import BrailleArtConfig, MaterialProfile, PrinterProfile, TactileGeometry
from .pipeline import create_demo_image, process_image
from .sampling import build_dot_grid, gaussian_dot_sampling_flat, gaussian_dot_sampling_grid, process_tiles
from .braille_unicode import BRAILLE_BASE, braille_matrix_to_text, decode_braille_cell, encode_braille_cell, encode_to_braille_matrix, unicode_roundtrip_test
