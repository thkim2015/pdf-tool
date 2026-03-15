"""Apple Human Interface Guidelines 기반 디자인 토큰 시스템.

macOS 스타일 UI를 위한 색상, 타이포그래피, 스페이싱, 애니메이션 상수를 정의한다.
모든 값은 Apple HIG (2024) 기준이다.
"""

from __future__ import annotations

from dataclasses import dataclass

# ============================================================================
# 시스템 색상 (Apple HIG)
# ============================================================================


@dataclass(frozen=True)
class SystemColors:
    """Apple 시스템 색상 정의.

    다크/라이트 모드별 배경, 텍스트 등 시스템 색상을 저장한다.
    불변 객체 (frozen=True)로 런타임 변경을 방지한다.
    """

    # 배경색 계층
    system_background: str
    secondary_system_background: str
    tertiary_system_background: str


# 다크 모드 시스템 색상
DARK_COLORS = SystemColors(
    system_background="#1C1C1E",
    secondary_system_background="#1C1C1E",
    tertiary_system_background="#2C2C2E",
)

# 라이트 모드 시스템 색상
LIGHT_COLORS = SystemColors(
    system_background="#F2F2F7",
    secondary_system_background="#F2F2F7",
    tertiary_system_background="#FFFFFF",
)


# ============================================================================
# 액센트 컬러 (Apple HIG)
# ============================================================================


class AccentColors:
    """Apple 시스템 액센트 컬러."""

    BLUE: str = "#007AFF"
    GREEN: str = "#34C759"
    RED: str = "#FF3B30"
    ORANGE: str = "#FF9500"
    YELLOW: str = "#FFCC00"


# ============================================================================
# Typography (Apple Dynamic Type)
# ============================================================================


class Typography:
    """Apple Dynamic Type 타이포그래피 스케일.

    SF Pro 폰트 기준 포인트 크기를 정의한다.
    """

    # 제목 크기 (pt)
    LARGE_TITLE: int = 34
    TITLE1: int = 28
    TITLE2: int = 22
    TITLE3: int = 20

    # 본문 크기 (pt)
    HEADLINE: int = 17
    HEADLINE_WEIGHT: str = "bold"
    BODY: int = 17
    CALLOUT: int = 16
    SUBHEADLINE: int = 15
    FOOTNOTE: int = 13
    CAPTION: int = 12


# ============================================================================
# Font Stacks (플랫폼별)
# ============================================================================


class FontStacks:
    """플랫폼별 폰트 스택 정의."""

    MACOS: tuple[str, ...] = ("SF Pro Text", "SF Pro Display", "Helvetica Neue", "Helvetica")
    MACOS_MONO: tuple[str, ...] = ("SF Mono", "Menlo", "Monaco")
    WINDOWS: tuple[str, ...] = ("Segoe UI", "Tahoma", "Arial")
    LINUX: tuple[str, ...] = ("Inter", "Cantarell", "Ubuntu", "Noto Sans")


# ============================================================================
# Spacing (8pt 그리드)
# ============================================================================


class Spacing:
    """8pt 그리드 기반 스페이싱 시스템."""

    UNIT: int = 8

    XS: int = 8    # 1 * UNIT
    SM: int = 16   # 2 * UNIT
    MD: int = 24   # 3 * UNIT
    LG: int = 32   # 4 * UNIT
    XL: int = 40   # 5 * UNIT


# ============================================================================
# Corner Radius (Apple HIG)
# ============================================================================


class CornerRadius:
    """Apple HIG 코너 반지름."""

    SMALL: int = 6
    MEDIUM: int = 10
    LARGE: int = 14


# ============================================================================
# Animation Timings
# ============================================================================


class AnimationTiming:
    """애니메이션 타이밍 상수 (초 단위)."""

    FAST: float = 0.1
    NORMAL: float = 0.15
    SLOW: float = 0.3


# ============================================================================
# 팩토리 함수
# ============================================================================


def get_tokens_for_mode(mode: str) -> SystemColors:
    """모드에 따른 시스템 색상을 반환한다.

    Args:
        mode: "dark" 또는 "light"

    Returns:
        해당 모드의 SystemColors 객체
    """
    if mode == "light":
        return LIGHT_COLORS
    return DARK_COLORS
