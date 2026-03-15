"""GUI 색상 팔레트 정의 모듈.

Apple Human Interface Guidelines 기반 다크모드/라이트모드 색상 체계를 정의한다.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """색상 팔레트.

    Apple HIG 시스템 색상 기반으로 정의한다.
    """

    # 기본 색상
    primary: str          # 주요 액션 (버튼, 링크) - Apple Blue
    secondary: str        # 보조 액션
    accent: str           # 강조 (하이라이트)

    # 배경색
    background: str       # 앱 배경 (Apple systemBackground)
    surface: str          # 카드, 패널 배경 (Apple secondarySystemBackground)
    surface_elevated: str # 상승된 표면 (Apple tertiarySystemBackground)

    # 텍스트 색상
    text_primary: str     # 주 텍스트
    text_secondary: str   # 보조 텍스트
    text_tertiary: str    # 터셔리 텍스트 (매우 연한)

    # 상태 색상 (Apple 액센트 컬러)
    success: str          # 성공 - Apple Green
    warning: str          # 경고 - Apple Orange
    error: str            # 에러 - Apple Red
    info: str             # 정보 - Apple Blue

    # 테두리/구분선
    border: str           # 테두리
    divider: str          # 구분선

    # 버튼 상태
    button_hover: str     # 버튼 hover
    button_active: str    # 버튼 active/pressed
    button_disabled: str  # 버튼 disabled

    # 사이드바 (macOS 스타일)
    sidebar_bg: str       # 사이드바 배경
    sidebar_hover: str    # 사이드바 항목 호버
    sidebar_selected: str # 사이드바 항목 선택

    # vibrancy (투명도 시뮬레이션)
    vibrancy_bg: str      # vibrancy 배경


# 다크모드 팔레트 (Apple HIG 기반)
DARK_PALETTE = ColorPalette(
    # 기본 색상 - Apple 시스템 색상
    primary="#007AFF",        # Apple Blue
    secondary="#5856D6",      # Apple Purple
    accent="#FF2D55",         # Apple Pink

    # 배경색 - Apple 다크 모드 시스템 배경
    background="#1C1C1E",     # systemBackground (다크)
    surface="#2C2C2E",        # secondarySystemBackground (다크)
    surface_elevated="#3A3A3C",  # tertiarySystemBackground (다크)

    # 텍스트 색상
    text_primary="#FFFFFF",   # label (다크)
    text_secondary="#EBEBF5",  # secondaryLabel (다크, 60% opacity 시뮬레이션)
    text_tertiary="#EBEBF5",  # tertiaryLabel (다크, 30% opacity 시뮬레이션)

    # 상태 색상 - Apple 액센트 컬러
    success="#34C759",        # Apple Green
    warning="#FF9500",        # Apple Orange
    error="#FF3B30",          # Apple Red
    info="#007AFF",           # Apple Blue

    # 테두리/구분선
    border="#38383A",         # separator (다크)
    divider="#48484A",        # opaqueSeparator (다크)

    # 버튼 상태
    button_hover="#0A84FF",   # Apple Blue (밝은 변형)
    button_active="#0071E3",  # Apple Blue (어두운 변형)
    button_disabled="#48484A",  # quaternaryLabel (다크)

    # 사이드바
    sidebar_bg="#1C1C1E",     # 사이드바 배경 (다크)
    sidebar_hover="#2C2C2E",  # 사이드바 호버
    sidebar_selected="#0A84FF",  # 사이드바 선택 (Apple Blue)

    # vibrancy
    vibrancy_bg="#1C1C1E",  # vibrancy 배경 (다크)
)

# 라이트모드 팔레트 (Apple HIG 기반)
LIGHT_PALETTE = ColorPalette(
    # 기본 색상 - Apple 시스템 색상
    primary="#007AFF",        # Apple Blue
    secondary="#5856D6",      # Apple Purple
    accent="#FF2D55",         # Apple Pink

    # 배경색 - Apple 라이트 모드 시스템 배경
    background="#F2F2F7",     # systemBackground (라이트)
    surface="#FFFFFF",        # secondarySystemBackground (라이트)
    surface_elevated="#F2F2F7",  # tertiarySystemBackground (라이트)

    # 텍스트 색상
    text_primary="#000000",   # label (라이트)
    text_secondary="#3C3C43",  # secondaryLabel (라이트, 60% opacity 시뮬레이션)
    text_tertiary="#3C3C43",  # tertiaryLabel (라이트, 30% opacity 시뮬레이션)

    # 상태 색상 - Apple 액센트 컬러
    success="#34C759",        # Apple Green
    warning="#FF9500",        # Apple Orange
    error="#FF3B30",          # Apple Red
    info="#007AFF",           # Apple Blue

    # 테두리/구분선
    border="#C6C6C8",         # separator (라이트)
    divider="#D1D1D6",        # opaqueSeparator (라이트)

    # 버튼 상태
    button_hover="#0A84FF",   # Apple Blue (밝은 변형)
    button_active="#0071E3",  # Apple Blue (어두운 변형)
    button_disabled="#D1D1D6",  # quaternaryLabel (라이트)

    # 사이드바
    sidebar_bg="#F2F2F7",     # 사이드바 배경 (라이트)
    sidebar_hover="#E5E5EA",  # 사이드바 호버
    sidebar_selected="#007AFF",  # 사이드바 선택 (Apple Blue)

    # vibrancy
    vibrancy_bg="#F2F2F7",  # vibrancy 배경 (라이트)
)


def get_palette(theme: str) -> ColorPalette:
    """테마에 따른 색상 팔레트를 반환한다.

    Args:
        theme: "dark" 또는 "light"

    Returns:
        해당 테마의 ColorPalette 객체
    """
    if theme == "dark":
        return DARK_PALETTE
    elif theme == "light":
        return LIGHT_PALETTE
    else:
        return DARK_PALETTE  # 기본값: 다크모드
