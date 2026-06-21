from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Literal

EmbosserCellMode = Literal['SIX_DOT', 'EIGHT_DOT', 'GRAPHICS']


@dataclass(frozen=True)
class GenericEmbosserProfile:
    name: str = 'generic-embosser'
    cell_mode: EmbosserCellMode = 'SIX_DOT'
    page_width_mm: float = 210.0
    page_height_mm: float = 297.0
    margin_left_mm: float = 15.0
    margin_right_mm: float = 15.0
    margin_top_mm: float = 15.0
    margin_bottom_mm: float = 15.0
    cell_width_mm: float = 6.0
    cell_height_mm: float = 10.0
    dot_pitch_mm: float = 2.5
    dpi: int | None = None
    supports_interpoint: bool = False
    supports_graphics_mode: bool = False
    max_cols: int | None = None
    max_rows: int | None = None

    @property
    def printable_width_mm(self) -> float:
        return max(0.0, self.page_width_mm - self.margin_left_mm - self.margin_right_mm)

    @property
    def printable_height_mm(self) -> float:
        return max(0.0, self.page_height_mm - self.margin_top_mm - self.margin_bottom_mm)


EMBOSSER_PROFILE_PRESETS: dict[str, GenericEmbosserProfile] = {
    'a4-40x25': GenericEmbosserProfile(
        name='a4-40x25',
        page_width_mm=210.0,
        page_height_mm=297.0,
        margin_left_mm=10.0,
        margin_right_mm=10.0,
        margin_top_mm=12.0,
        margin_bottom_mm=12.0,
        cell_width_mm=4.7,
        cell_height_mm=10.0,
        max_cols=40,
        max_rows=25,
    ),
    'letter-40x25': GenericEmbosserProfile(
        name='letter-40x25',
        page_width_mm=215.9,
        page_height_mm=279.4,
        margin_left_mm=10.0,
        margin_right_mm=10.0,
        margin_top_mm=12.0,
        margin_bottom_mm=12.0,
        cell_width_mm=4.8,
        cell_height_mm=10.0,
        max_cols=40,
        max_rows=25,
    ),
    'portable-34x25': GenericEmbosserProfile(
        name='portable-34x25',
        page_width_mm=210.0,
        page_height_mm=297.0,
        margin_left_mm=18.0,
        margin_right_mm=18.0,
        margin_top_mm=12.0,
        margin_bottom_mm=12.0,
        cell_width_mm=5.0,
        cell_height_mm=10.0,
        max_cols=34,
        max_rows=25,
    ),
    'a4-interpoint-40x25': GenericEmbosserProfile(
        name='a4-interpoint-40x25',
        page_width_mm=210.0,
        page_height_mm=297.0,
        margin_left_mm=10.0,
        margin_right_mm=10.0,
        margin_top_mm=12.0,
        margin_bottom_mm=12.0,
        cell_width_mm=4.7,
        cell_height_mm=10.0,
        supports_interpoint=True,
        max_cols=40,
        max_rows=25,
    ),
}


def embosser_profile_names() -> list[str]:
    return sorted(EMBOSSER_PROFILE_PRESETS)


def get_embosser_profile_preset(name: str) -> GenericEmbosserProfile:
    try:
        return EMBOSSER_PROFILE_PRESETS[name]
    except KeyError as exc:
        known = ', '.join(embosser_profile_names())
        raise ValueError(f'unknown embosser profile preset: {name}; known presets: {known}') from exc


def build_embosser_profile(name: str = 'a4-40x25', *, max_cols: int | None = None, max_rows: int | None = None) -> GenericEmbosserProfile:
    profile = get_embosser_profile_preset(name)
    if max_cols is not None or max_rows is not None:
        profile = replace(
            profile,
            name=f'{profile.name}+override',
            max_cols=max_cols if max_cols is not None else profile.max_cols,
            max_rows=max_rows if max_rows is not None else profile.max_rows,
        )
    return profile


def _safe_int_capacity(available_mm: float, unit_mm: float) -> int:
    if available_mm <= 0 or unit_mm <= 0:
        return 0
    return int(available_mm // unit_mm)


def embosser_capacity(profile: GenericEmbosserProfile) -> dict[str, int | float | str | bool | None]:
    computed_cols = _safe_int_capacity(profile.printable_width_mm, profile.cell_width_mm)
    computed_rows = _safe_int_capacity(profile.printable_height_mm, profile.cell_height_mm)
    cols = min(computed_cols, profile.max_cols) if profile.max_cols is not None else computed_cols
    rows = min(computed_rows, profile.max_rows) if profile.max_rows is not None else computed_rows
    return {
        'profile': profile.name,
        'cell_mode': profile.cell_mode,
        'printable_width_mm': round(profile.printable_width_mm, 3),
        'printable_height_mm': round(profile.printable_height_mm, 3),
        'computed_cols': computed_cols,
        'computed_rows': computed_rows,
        'cols': cols,
        'rows': rows,
        'cells_per_page': cols * rows,
        'supports_interpoint': profile.supports_interpoint,
        'supports_graphics_mode': profile.supports_graphics_mode,
        'dpi': profile.dpi,
    }


def validate_embosser_profile(profile: GenericEmbosserProfile) -> list[str]:
    issues: list[str] = []
    if profile.page_width_mm <= 0 or profile.page_height_mm <= 0:
        issues.append('page dimensions must be positive')
    if profile.margin_left_mm < 0 or profile.margin_right_mm < 0 or profile.margin_top_mm < 0 or profile.margin_bottom_mm < 0:
        issues.append('margins must be non-negative')
    if profile.printable_width_mm <= 0 or profile.printable_height_mm <= 0:
        issues.append('printable area must be positive after margins')
    if profile.cell_width_mm <= 0 or profile.cell_height_mm <= 0:
        issues.append('cell dimensions must be positive')
    if profile.dot_pitch_mm <= 0:
        issues.append('dot pitch must be positive')
    if profile.cell_mode == 'GRAPHICS' and not profile.supports_graphics_mode:
        issues.append('GRAPHICS cell mode requires supports_graphics_mode=True')
    if profile.max_cols is not None and profile.max_cols <= 0:
        issues.append('max_cols must be positive when provided')
    if profile.max_rows is not None and profile.max_rows <= 0:
        issues.append('max_rows must be positive when provided')
    return issues


def embosser_encoding_family(profile: GenericEmbosserProfile) -> str:
    if profile.cell_mode == 'SIX_DOT':
        return 'BRF_OR_BRAILLE_ASCII'
    if profile.cell_mode == 'EIGHT_DOT':
        return 'UNICODE_BRAILLE_OR_DEVICE_SPECIFIC_8_DOT'
    return 'DEVICE_SPECIFIC_GRAPHICS_MODE'


def embosser_export_manifest(profile: GenericEmbosserProfile, *, output_path: str | None = None, source_artifact: str | None = None) -> dict:
    capacity = embosser_capacity(profile)
    issues = validate_embosser_profile(profile)
    return {
        'exporter': 'generic_embosser_boundary',
        'profile': asdict(profile),
        'encoding_family': embosser_encoding_family(profile),
        'capacity': capacity,
        'output_path': output_path,
        'source_artifact': source_artifact,
        'device_driver_required': profile.cell_mode == 'GRAPHICS' or profile.supports_graphics_mode,
        'portable_text_export': profile.cell_mode == 'SIX_DOT',
        'issues': issues,
        'ok': not issues,
    }


def assert_embosser_profile(profile: GenericEmbosserProfile) -> None:
    issues = validate_embosser_profile(profile)
    if issues:
        raise ValueError('; '.join(issues))
