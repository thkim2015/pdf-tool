"""GUI 테마 설정 모듈.

customtkinter의 외관 모드와 색상 팔레트를 관리한다.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pdf_tool.gui.colors import ColorPalette, get_palette

if TYPE_CHECKING:
    pass

# 테마 상수
DARK_MODE = "dark"
LIGHT_MODE = "light"

# 현재 테마 상태
_current_theme = DARK_MODE
_current_palette: ColorPalette | None = None


def _get_ctk():
    """customtkinter 모듈을 지연 로드한다."""
    import customtkinter as ctk

    return ctk


# 테스트에서 mock 가능하도록 모듈 수준 참조
ctk = None


def _ensure_ctk():
    """ctk 모듈이 로드되어 있는지 확인하고 반환한다."""
    global ctk
    if ctk is None:
        ctk = _get_ctk()
    return ctk


def apply_theme(mode: str) -> None:
    """지정된 테마 모드를 적용한다.

    Args:
        mode: 적용할 테마 모드 ("dark" 또는 "light")
    """
    global _current_theme, _current_palette
    _ensure_ctk().set_appearance_mode(mode)
    _current_theme = mode
    _current_palette = get_palette(mode)


def toggle_theme() -> str:
    """현재 테마를 반대 모드로 전환한다.

    Returns:
        전환된 테마 모드 문자열
    """
    global _current_theme
    new_theme = LIGHT_MODE if _current_theme == DARK_MODE else DARK_MODE
    apply_theme(new_theme)
    return new_theme


def get_current_theme() -> str:
    """현재 테마 모드를 반환한다.

    Returns:
        현재 테마 모드 문자열
    """
    return _current_theme


def get_current_palette() -> ColorPalette:
    """현재 테마의 색상 팔레트를 반환한다.

    Returns:
        현재 테마의 ColorPalette 객체
    """
    global _current_palette
    if _current_palette is None:
        _current_palette = get_palette(_current_theme)
    return _current_palette
