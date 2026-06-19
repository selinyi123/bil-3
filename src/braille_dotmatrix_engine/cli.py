from __future__ import annotations
import argparse, json
from pathlib import Path
from .engine import BrailleArtConfig, create_demo_image, process_image
from .benchmark import run_benchmark_suite, write_benchmark_csv


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError('value must be a positive integer')
    return parsed


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Unicode Braille and ASCII visual-symbol renderer")
    p.add_argument("image", nargs="?")
    p.add_argument("--width-cells", type=_positive_int, default=80)
    p.add_argument("--mode", choices=["TACTILE", "SCREEN", "CHROMATIC", "ASCII_MONO", "ASCII_COLOR"], default="TACTILE")
    p.add_argument("--output-png", default="output_braille.png")
    p.add_argument("--output-txt", default="output_braille.txt")
    p.add_argument("--report-json", default="render_report.json")
    p.add_argument("--output-svg", default=None)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--no-invert", action="store_true")
    p.add_argument("--strict-tactile", action="store_true", help="fail tactile-mode export when tactile validation reports errors")
    p.add_argument("--ascii-charset", default=None)
    p.add_argument("--ascii-aspect", type=float, default=None)
    p.add_argument("--ascii-edge-weight", type=float, default=None)
    p.add_argument("--benchmark", action="store_true", help="run the benchmark suite instead of rendering one image")
    p.add_argument("--benchmark-csv", default="benchmark.csv")
    a = p.parse_args(argv)
    if a.benchmark:
        rows = run_benchmark_suite(output_dir=Path(a.benchmark_csv).parent or Path('.'))
        write_benchmark_csv(rows, a.benchmark_csv)
        print(json.dumps({'benchmark_csv': a.benchmark_csv, 'rows': rows}, indent=2, ensure_ascii=False))
        return 0
    for target in [a.output_png, a.output_txt, a.report_json, a.output_svg]:
        if target is not None:
            Path(target).parent.mkdir(parents=True, exist_ok=True)
    image = a.image or create_demo_image("test_input.png")
    cfg = BrailleArtConfig(
        output_width_cells=a.width_cells,
        mode=a.mode,
        seed=a.seed,
        invert_luminance=not a.no_invert,
        strict_tactile_validation=bool(a.strict_tactile),
    )
    if a.ascii_charset is not None:
        cfg.ascii_charset = a.ascii_charset
    if a.ascii_aspect is not None:
        cfg.ascii_aspect_ratio = a.ascii_aspect
    if a.ascii_edge_weight is not None:
        cfg.ascii_edge_weight = a.ascii_edge_weight
    report = process_image(image, cfg, a.output_png, a.output_txt, a.report_json, a.output_svg)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
