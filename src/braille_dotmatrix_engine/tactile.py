from __future__ import annotations
from dataclasses import asdict
import numpy as np

def geometry_report(cfg) -> dict:
    gap = float(cfg.dot_spacing_mm - cfg.dot_diameter_mm)
    cell_width = float(cfg.dot_spacing_mm)
    cell_height = float(cfg.dot_spacing_mm * 3.0)
    issues = []
    if cfg.dot_diameter_mm <= 0:
        issues.append('dot_diameter_mm must be positive')
    if cfg.dot_spacing_mm <= 0:
        issues.append('dot_spacing_mm must be positive')
    if gap < cfg.safety_gap_mm:
        issues.append('dot edge gap below safety_gap_mm')
    if cfg.geometry.dot_height_mm <= 0:
        issues.append('dot_height_mm must be positive')
    return {
        'geometry': asdict(cfg.geometry),
        'material': asdict(cfg.material),
        'printer': asdict(cfg.printer),
        'edge_gap_mm': gap,
        'cell_width_mm': cell_width,
        'cell_height_mm': cell_height,
        'compliant': len(issues) == 0,
        'issues': issues,
    }

def binary_to_dot_positions_mm(binary, cfg):
    b = np.asarray(binary, dtype=bool)
    ys, xs = np.where(b)
    spacing = float(cfg.dot_spacing_mm)
    positions = []
    for y, x in zip(ys.tolist(), xs.tolist()):
        positions.append({'x_mm': float((x + 0.5) * spacing), 'y_mm': float((y + 0.5) * spacing)})
    return positions
