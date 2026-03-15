"""프로그레스 바 스타일 모듈.

macOS 스타일 프로그레스 바의 크기, 색상, 백분율 계산 로직이다.
"""

from __future__ import annotations

from pdf_tool.gui.design_tokens import AccentColors


class ProgressBarStyle:
    """프로그레스 바의 스타일 계산 로직."""

    @staticmethod
    def get_style() -> dict:
        """프로그레스 바의 크기 스타일을 반환한다.

        Returns:
            height, corner_radius 키를 포함하는 딕셔너리
        """
        return {
            "height": 4,
            "corner_radius": 2,
        }

    @staticmethod
    def get_colors(mode: str) -> dict:
        """모드에 따른 프로그레스 바 색상을 반환한다.

        Args:
            mode: "dark" 또는 "light"

        Returns:
            progress_color, bg_color 키를 포함하는 딕셔너리
        """
        bg_color = "#3A3A3C" if mode == "dark" else "#E5E5EA"
        return {
            "progress_color": AccentColors.BLUE,
            "bg_color": bg_color,
        }

    @staticmethod
    def calculate_percentage(current: float, total: float) -> float:
        """백분율을 계산한다.

        Args:
            current: 현재 값
            total: 전체 값

        Returns:
            백분율 (0.0 ~ 100.0)
        """
        if total == 0:
            return 0.0
        return (current / total) * 100.0
