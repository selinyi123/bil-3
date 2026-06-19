# API Usage

## Basic conversion

```python
from braille_dotmatrix_engine import BrailleArtConfig, process_image

cfg = BrailleArtConfig(output_width_cells=80, mode='TACTILE')
report = process_image('input.png', cfg, 'output.png', 'output.txt', 'report.json')
```

## Screen preview

```python
cfg = BrailleArtConfig(output_width_cells=100, mode='SCREEN')
process_image('input.png', cfg, 'screen.png', 'screen.txt', 'screen-report.json')
```

## Important fields

- `output_width_cells`: output width in Braille Unicode cells.
- `mode`: `TACTILE` or `SCREEN`.
- `invert_luminance`: dark source areas produce more dots when enabled.
- `tile_size_px`: tile size for memory-safe processing.
- `tile_overlap_px`: overlap used by feather-weighted blending.
- `render_spacing_px`: preview pixel spacing between dot centers.

## Report contract

The report dictionary includes image shape, dot shape, cell shape, dither method, occupancy ratio, runtime, mode, seed, validation results, and serialized config.
