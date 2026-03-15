"""macOS 스타일 버튼 위젯 모듈.

Primary, Secondary, Destructive 스타일과 Mini, Regular, Large 크기를 지원한다.
"""

from __future__ import annotations

from pdf_tool.gui.design_tokens import AccentColors, CornerRadius

# 호버 애니메이션 지속 시간 (초)
HOVER_ANIMATION_DURATION: float = 0.15

# 클릭 스케일 비율 (1.0 -> 이 값 -> 1.0)
CLICK_SCALE: float = 0.98

# 클릭 애니메이션 지속 시간 (초)
CLICK_ANIMATION_DURATION: float = 0.1

# 크기별 높이 (pt)
_SIZE_HEIGHT: dict[str, int] = {
    "mini": 22,
    "regular": 28,
    "large": 36,
}

# 스타일별 색상
_STYLE_COLORS: dict[str, dict[str, str]] = {
    "primary": {
        "bg_color": AccentColors.BLUE,
        "text_color": "#FFFFFF",
    },
    "secondary": {
        "bg_color": "#8E8E931A",  # systemGray 10% opacity
        "text_color": "#000000",
    },
    "destructive": {
        "bg_color": AccentColors.RED,
        "text_color": "#FFFFFF",
    },
}

# 스타일별 호버 색상 (20% 어두운 변형)
_HOVER_COLORS: dict[str, str] = {
    "primary": "#0066CC",
    "secondary": "#7A7A7F",
    "destructive": "#CC2F26",
}


class MacOSButtonStyle:
    """macOS 스타일 버튼의 스타일 계산 로직.

    스타일(primary/secondary/destructive)과 크기(mini/regular/large)에 따라
    적절한 스타일 딕셔너리를 반환한다.
    """

    @staticmethod
    def get_style(style: str, size: str) -> dict:
        """스타일과 크기에 맞는 스타일 딕셔너리를 반환한다.

        Args:
            style: "primary", "secondary", "destructive"
            size: "mini", "regular", "large"

        Returns:
            bg_color, text_color, height, corner_radius 키를 포함하는 딕셔너리
        """
        colors = _STYLE_COLORS.get(style, _STYLE_COLORS["primary"])
        height = _SIZE_HEIGHT.get(size, _SIZE_HEIGHT["regular"])

        return {
            "bg_color": colors["bg_color"],
            "text_color": colors["text_color"],
            "height": height,
            "corner_radius": CornerRadius.SMALL,
        }

    @staticmethod
    def get_hover_color(style: str) -> str:
        """스타일에 맞는 호버 색상을 반환한다.

        Args:
            style: "primary", "secondary", "destructive"

        Returns:
            호버 색상 hex 문자열
        """
        return _HOVER_COLORS.get(style, _HOVER_COLORS["primary"])

    @staticmethod
    def get_disabled_style() -> dict:
        """비활성 상태의 스타일을 반환한다.

        Returns:
            opacity 키를 포함하는 딕셔너리
        """
        return {"opacity": 0.5}
