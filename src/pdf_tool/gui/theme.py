"""GUI 테마 설정 모듈.

customtkinter의 외관 모드와 색상 팔레트를 관리한다.
darkdetect를 통한 시스템 테마 자동 감지를 지원한다.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING

from pdf_tool.gui.colors import ColorPalette, get_palette

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

# 테마 상수
DARK_MODE = "dark"
LIGHT_MODE = "light"

# 현재 테마 상태
_current_theme = DARK_MODE
_current_palette: ColorPalette | None = None

# 테마 변경 콜백 목록
_theme_callbacks: list[Callable[[str], None]] = []


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


def _detect_system_theme() -> str:
    """시스템 테마를 감지한다.

    darkdetect를 사용하여 현재 시스템의 다크/라이트 모드를 감지한다.
    darkdetect를 사용할 수 없는 경우 다크 모드를 기본값으로 반환한다.

    Returns:
        "dark" 또는 "light"
    """
    try:
        import darkdetect

        theme = darkdetect.theme()
        if theme is not None:
            return theme.lower()
    except ImportError:
        logger.debug("darkdetect를 사용할 수 없습니다. 기본값(dark)을 사용합니다.")
    except Exception:
        logger.debug("시스템 테마 감지 실패. 기본값(dark)을 사용합니다.")
    return DARK_MODE


def apply_theme(mode: str) -> None:
    """지정된 테마 모드를 적용한다.

    Args:
        mode: 적용할 테마 모드 ("dark" 또는 "light")
    """
    global _current_theme, _current_palette
    _ensure_ctk().set_appearance_mode(mode)
    _current_theme = mode
    _current_palette = get_palette(mode)

    # 등록된 콜백에 테마 변경 알림
    for callback in _theme_callbacks:
        try:
            callback(mode)
        except Exception:
            logger.warning("테마 변경 콜백 실행 중 오류 발생", exc_info=True)


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


def register_theme_callback(callback: Callable[[str], None]) -> None:
    """테마 변경 콜백을 등록한다.

    테마가 변경될 때 호출될 콜백 함수를 등록한다.
    콜백은 새로운 테마 모드 문자열("dark" 또는 "light")을 인자로 받는다.

    Args:
        callback: 테마 변경 시 호출할 함수
    """
    if callback not in _theme_callbacks:
        _theme_callbacks.append(callback)


def unregister_theme_callback(callback: Callable[[str], None]) -> None:
    """테마 변경 콜백을 해제한다.

    Args:
        callback: 해제할 콜백 함수
    """
    if callback in _theme_callbacks:
        _theme_callbacks.remove(callback)
