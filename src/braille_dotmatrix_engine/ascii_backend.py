from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

__all__ = ["render_ascii_text", "write_ascii_output"]

ANSI_RESET = "\x1b[0m"


def _normalize01(arr: np.ndarray) -> np.ndarray:
    a = np.asarray(arr, dtype=np.float32)
    lo = float(np.min(a)) if a.size else 0.0
    hi = float(np.max(a)) if a.size else 1.0
    if hi - lo < 1e-6:
        return np.clip(a, 0.0, 1.0)
    return np.clip((a - lo) / (hi - lo), 0.0, 1.0)


def _prepare_image(source_bgr, cols: int, cfg) -> tuple[np.ndarray, np.ndarray]:
    src = np.asarray(source_bgr)
    if src.ndim == 2:
        bgr = cv2.cvtColor(src.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    elif src.shape[2] == 4:
        bgr = src[:, :, :3].astype(np.uint8)
    else:
        bgr = src.astype(np.uint8)

    h, w = bgr.shape[:2]
    aspect = float(getattr(cfg, "ascii_aspect_ratio", 0.50))
    rows = max(1, int(round((h / max(w, 1)) * cols * aspect)))
    resized = cv2.resize(bgr, (cols, rows), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

    edge_weight = float(getattr(cfg, "ascii_edge_weight", 0.0))
    if edge_weight > 0 and min(gray.shape) >= 3:
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        edges = _normalize01(np.sqrt(gx * gx + gy * gy))
        gray = np.clip(gray + edges * edge_weight, 0.0, 1.0)

    if bool(getattr(cfg, "ascii_invert", False)):
        gray = 1.0 - gray
    return gray, resized


def _chars_from_luma(luma: np.ndarray, charset: str) -> np.ndarray:
    if not charset:
        raise ValueError("ascii_charset must not be empty")
    chars = np.array(list(charset), dtype="<U1")
    idx = np.clip(np.rint(luma * (len(chars) - 1)).astype(np.int32), 0, len(chars) - 1)
    return chars[idx]


def _ansi_color(ch: str, bgr) -> str:
    b, g, r = [int(x) for x in bgr]
    return f"\x1b[38;2;{r};{g};{b}m{ch}{ANSI_RESET}"


def render_ascii_text(source_bgr, cfg, color: bool | None = None) -> tuple[str, dict]:
    cols = int(getattr(cfg, "output_width_cells", 80))
    color = bool(getattr(cfg, "ascii_ansi", False)) if color is None else bool(color)
    luma, colors = _prepare_image(source_bgr, cols, cfg)
    matrix = _chars_from_luma(luma, str(getattr(cfg, "ascii_charset", " .:-=+*#%@")))

    lines: list[str] = []
    if color:
        for row_chars, row_colors in zip(matrix, colors):
            lines.append("".join(_ansi_color(ch, px) for ch, px in zip(row_chars.tolist(), row_colors)))
    else:
        lines = ["".join(row.tolist()) for row in matrix]

    text = "\n".join(lines) + "\n"
    report = {
        "backend": "ASCII_COLOR" if color else "ASCII_MONO",
        "rows": int(matrix.shape[0]),
        "cols": int(matrix.shape[1]),
        "charset_size": int(len(str(getattr(cfg, "ascii_charset", "")))),
        "aspect_ratio": float(getattr(cfg, "ascii_aspect_ratio", 0.50)),
        "edge_weight": float(getattr(cfg, "ascii_edge_weight", 0.0)),
        "ansi_color": bool(color),
        "monospace_required": True,
    }
    return text, report


def write_ascii_output(source_bgr, cfg, path, color: bool | None = None) -> dict:
    text, report = render_ascii_text(source_bgr, cfg, color=color)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return report
