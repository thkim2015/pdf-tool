"""파일 피커 드롭 영역 스타일 모듈.

macOS 스타일 dashed border 드롭 영역의 스타일 계산 로직이다.
"""

from __future__ import annotations

from pdf_tool.gui.design_tokens import AccentColors


class FilePickerDropZoneStyle:
    """파일 피커 드롭 영역의 스타일 계산 로직."""

    @staticmethod
    def get_style(mode: str) -> dict:
        """모드에 따른 드롭 영역 스타일을 반환한다.

        Args:
            mode: "dark" 또는 "light"

        Returns:
            border_color, border_width, corner_radius, padding 키를 포함하는 딕셔너리
        """
        border_color = "#3A3A3C" if mode == "dark" else "#D1D1D6"
        return {
            "border_color": border_color,
            "border_width": 2,
            "corner_radius": 12,
            "padding": 20,
        }

    @staticmethod
    def get_drag_over_style() -> dict:
        """드래그 오버 상태의 스타일을 반환한다.

        Returns:
            border_color, bg_color 키를 포함하는 딕셔너리
        """
        return {
            "border_color": AccentColors.BLUE,
            "bg_color": "#007AFF1A",  # accent 10% opacity
        }
