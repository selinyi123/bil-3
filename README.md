# Braille Dot-Matrix Engine

Corrected v1.1 implementation of a Unicode Braille dot-matrix art renderer.

This repository replaces the previous `bil-3` content with a focused runnable baseline.

## Pipeline

```text
image -> CLAHE -> Gaussian dot sampling -> dithering -> Unicode Braille text -> PNG render -> JSON report
```

## Fixed from the prototype

- `dataclass` mutable defaults use `field(default_factory=...)`.
- Tiled sampling no longer passes flat coordinates into grid-shaped samplers.
- Grayscale normalization is not applied twice.
- `invert_luminance=True` makes dark regions produce higher dot density by default.
- Fake Ostromoukhov support is removed from defaults.
- Material/printer compensation changes render radius, not the logical Braille mask.
- Added Unicode, physical, and raster roundtrip validation.

## Install

```bash
pip install -e ".[dev]"
```

## Run

```bash
braille-dotmatrix --width-cells 80 --mode TACTILE
braille-dotmatrix input.png --width-cells 100 --mode SCREEN --output-png out.png --output-txt out.txt
```
