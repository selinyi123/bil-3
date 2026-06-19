from __future__ import annotations

import csv
import os
import resource
import time
from pathlib import Path

import cv2
import numpy as np

from .config import BrailleArtConfig
from .pipeline import process_image

__all__ = ["create_synthetic_image", "run_one_benchmark", "run_benchmark_suite", "write_benchmark_csv"]


def _rss_mb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports KiB, macOS reports bytes. GitHub Actions is Linux, but keep
    # the fallback safe for local usage.
    if usage > 10_000_000:
        return float(usage / (1024 * 1024))
    return float(usage / 1024)


def create_synthetic_image(path, width: int = 256, height: int = 192) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0, 1, width, dtype=np.float32)
    y = np.linspace(0, 1, height, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    r = np.clip(255 * xx, 0, 255)
    g = np.clip(255 * yy, 0, 255)
    b = np.clip(255 * (0.55 + 0.45 * np.sin(8 * xx) * np.cos(6 * yy)), 0, 255)
    img = np.stack([b, g, r], axis=-1).astype(np.uint8)
    cv2.circle(img, (width // 2, height // 2), max(8, min(width, height) // 5), (245, 245, 245), -1)
    cv2.line(img, (0, height - 1), (width - 1, 0), (20, 20, 20), 3)
    cv2.imwrite(str(path), img)
    return str(path)


def run_one_benchmark(name: str, image_shape: tuple[int, int], mode: str, output_dir='artifacts/benchmarks') -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    height, width = image_shape
    image = create_synthetic_image(output_dir / f'{name}_{mode.lower()}_input.png', width=width, height=height)
    cfg = BrailleArtConfig(output_width_cells=max(12, min(96, width // 8)), mode=mode, render_spacing_px=6)
    before = _rss_mb()
    start = time.perf_counter()
    report = process_image(
        image,
        cfg,
        output_dir / f'{name}_{mode.lower()}.png',
        output_dir / f'{name}_{mode.lower()}.txt',
        output_dir / f'{name}_{mode.lower()}.json',
    )
    elapsed = time.perf_counter() - start
    after = _rss_mb()
    q = report.get('quality_metrics', {})
    return {
        'name': name,
        'mode': mode,
        'width': width,
        'height': height,
        'runtime_sec': round(float(elapsed), 6),
        'rss_delta_mb': round(float(max(0.0, after - before)), 3),
        'rss_peak_mb': round(float(after), 3),
        'occupancy_ratio': round(float(report.get('occupancy_ratio', 0.0)), 6),
        'tone_psnr': round(float(q.get('psnr', q.get('tone_psnr', 0.0)) or 0.0), 6),
        'edge_score': round(float(q.get('edge_score', 0.0) or 0.0), 6),
        'schema_version': report.get('schema_version'),
    }


def run_benchmark_suite(output_dir='artifacts/benchmarks') -> list[dict]:
    cases = [
        ('smoke_128', (96, 128)),
        ('smoke_256', (192, 256)),
    ]
    rows: list[dict] = []
    for name, shape in cases:
        rows.append(run_one_benchmark(name, shape, 'TACTILE', output_dir))
        rows.append(run_one_benchmark(name, shape, 'CHROMATIC', output_dir))
    return rows


def write_benchmark_csv(rows: list[dict], path='benchmark.csv') -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return str(path)
