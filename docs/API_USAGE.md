# API Usage

## Basic usage

```python
from braille_dotmatrix_engine import BrailleArtConfig, process_image

cfg = BrailleArtConfig(output_width_cells=80, mode='TACTILE')
report = process_image('input.png', cfg, 'out.png', 'out.txt', 'report.json')
```

## Screen output

```python
cfg = BrailleArtConfig(output_width_cells=80, mode='SCREEN')
process_image('input.png', cfg, 'screen.png', 'screen.txt', 'screen.json')
```

## Important outputs

- `out.txt`: Unicode Braille text.
- `out.png`: tactile or screen preview.
- `report.json`: shape, dither method, occupancy, mode, and validation data.

## Current limitation

`TACTILE` mode supports raster roundtrip validation. `SCREEN` mode uses glow and RGB rendering, so raster roundtrip validation is skipped.
