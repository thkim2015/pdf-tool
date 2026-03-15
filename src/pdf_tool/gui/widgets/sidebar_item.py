"""사이드바 항목 위젯 모듈.

macOS 스타일 사이드바 항목의 상태 관리 및 스타일 계산 로직이다.
아이콘 + 텍스트 가로 배열, 선택/호버/비활성 상태를 지원한다.
"""

from __future__ import annotations

from pdf_tool.gui.design_tokens import AccentColors, CornerRadius, Spacing

# 사이드바 아이콘 크기 (px)
SIDEBAR_ICON_SIZE: int = 24

# 아이콘-텍스트 간격 (pt)
SIDEBAR_TEXT_SPACING: int = 8

# 호버 배경색 (accent 10% opacity 시뮬레이션)
_HOVER_BG_COLOR: str = "#007AFF1A"


class SidebarItemState:
    """사이드바 항목의 상태를 관리하는 클래스.

    GUI 위젯과 분리된 순수 상태 관리 및 스타일 계산 로직이다.
    """

    def __init__(
        self,
        icon: str,
        label: str,
        value: str,
    ) -> None:
        """사이드바 항목 상태를 초기화한다.

        Args:
            icon: 유니코드 아이콘 문자열
            label: 표시할 텍스트
            value: 내부 식별 값
        """
        self.icon: str = icon
        self.label: str = label
        self.value: str = value
        self.selected: bool = False
        self.hovered: bool = False
        self.enabled: bool = True

    def set_selected(self, selected: bool) -> None:
        """선택 상태를 설정한다.

        비활성 상태에서는 선택이 무시된다.

        Args:
            selected: 선택 여부
        """
        if not self.enabled:
            return
        self.selected = selected

    def set_hovered(self, hovered: bool) -> None:
        """호버 상태를 설정한다.

        Args:
            hovered: 호버 여부
        """
        self.hovered = hovered

    def set_enabled(self, enabled: bool) -> None:
        """활성/비활성 상태를 설정한다.

        Args:
            enabled: 활성 여부
        """
        self.enabled = enabled

    def get_style(self) -> dict:
        """현재 상태에 맞는 스타일 딕셔너리를 반환한다.

        Returns:
            bg_color, corner_radius, padx, pady, opacity 키를 포함하는 스타일 딕셔너리
        """
        if not self.enabled:
            return {
                "bg_color": "transparent",
                "corner_radius": CornerRadius.SMALL,
                "padx": Spacing.XS,
                "pady": 4,
                "opacity": 0.5,
            }

        if self.selected:
            return {
                "bg_color": AccentColors.BLUE,
                "corner_radius": CornerRadius.SMALL,
                "padx": Spacing.XS,
                "pady": 4,
                "opacity": 1.0,
            }

        if self.hovered:
            return {
                "bg_color": _HOVER_BG_COLOR,
                "corner_radius": CornerRadius.SMALL,
                "padx": Spacing.XS,
                "pady": 4,
                "opacity": 1.0,
            }

        return {
            "bg_color": "transparent",
            "corner_radius": CornerRadius.SMALL,
            "padx": Spacing.XS,
            "pady": 4,
            "opacity": 1.0,
        }
