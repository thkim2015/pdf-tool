"""GUI 색상 팔레트 정의 모듈.

다크모드/라이트모드 색상 체계를 일관되게 정의한다.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """색상 팔레트."""

    # 기본 색상
    primary: str          # 주요 액션 (버튼, 링크)
    secondary: str        # 보조 액션
    accent: str           # 강조 (하이라이트)

    # 배경색
    background: str       # 앱 배경
    surface: str          # 카드, 패널 배경
    surface_elevated: str # 상승된 표면

    # 텍스트 색상
    text_primary: str     # 주 텍스트
    text_secondary: str   # 보조 텍스트
    text_tertiary: str    # 터셔리 텍스트 (매우 연한)

    # 상태 색상
    success: str          # 성공 (초록)
    warning: str          # 경고 (주황)
    error: str            # 에러 (빨강)
    info: str             # 정보 (파랑)

    # 테두리/구분선
    border: str           # 테두리
    divider: str          # 구분선

    # 버튼 상태
    button_hover: str     # 버튼 hover
    button_active: str    # 버튼 active/pressed
    button_disabled: str  # 버튼 disabled


# 다크모드 팔레트 (기본값)
DARK_PALETTE = ColorPalette(
    # 기본 색상 - Blue-Purple 체계
    primary="#3b82f6",        # Bright Blue
    secondary="#8b5cf6",      # Purple
    accent="#ec4899",         # Pink/Magenta

    # 배경색
    background="#0f172a",     # Navy Black (매우 어두운 파랑)
    surface="#1e293b",        # Dark Slate (어두운 회색-파랑)
    surface_elevated="#334155", # Slate (중간 회색-파랑)

    # 텍스트 색상
    text_primary="#f1f5f9",   # Light Slate (거의 흰색)
    text_secondary="#cbd5e1", # Medium Slate (밝은 회색)
    text_tertiary="#94a3b8",  # Dim Slate (중간 회색)

    # 상태 색상
    success="#10b981",        # Emerald (초록)
    warning="#f59e0b",        # Amber (주황)
    error="#ef4444",          # Red (빨강)
    info="#06b6d4",           # Cyan (시안)

    # 테두리/구분선
    border="#334155",         # Slate
    divider="#475569",        # Darker Slate

    # 버튼 상태
    button_hover="#4f46e5",   # Indigo (Blue보다 진함)
    button_active="#4338ca",  # Indigo (더 진함)
    button_disabled="#475569", # Slate (비활성)
)

# 라이트모드 팔레트
LIGHT_PALETTE = ColorPalette(
    # 기본 색상
    primary="#2563eb",        # Deep Blue
    secondary="#7c3aed",      # Deep Purple
    accent="#db2777",         # Deep Pink

    # 배경색
    background="#f8fafc",     # Very Light Slate
    surface="#ffffff",        # White
    surface_elevated="#f1f5f9", # Light Slate

    # 텍스트 색상
    text_primary="#0f172a",   # Navy Black
    text_secondary="#475569", # Slate
    text_tertiary="#94a3b8",  # Dim Slate

    # 상태 색상
    success="#059669",        # Deep Emerald
    warning="#d97706",        # Deep Amber
    error="#dc2626",          # Deep Red
    info="#0891b2",           # Deep Cyan

    # 테두리/구분선
    border="#e2e8f0",         # Light Gray
    divider="#cbd5e1",        # Medium Light Gray

    # 버튼 상태
    button_hover="#1d4ed8",   # Deeper Blue
    button_active="#1e40af",  # Very Deep Blue
    button_disabled="#cbd5e1", # Light Gray
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
