"""결과 표시 카드 스타일 모듈.

macOS 스타일 성공/실패 결과 카드의 스타일 계산 로직이다.
"""

from __future__ import annotations

from pdf_tool.gui.design_tokens import AccentColors


class ResultCardStyle:
    """결과 카드의 스타일 계산 로직."""

    @staticmethod
    def get_success_style(mode: str) -> dict:
        """성공 카드 스타일을 반환한다.

        Args:
            mode: "dark" 또는 "light"

        Returns:
            bg_color, icon_color, corner_radius 키를 포함하는 딕셔너리
        """
        bg_color = "#2C2C2E" if mode == "dark" else "#F0F0F0"
        return {
            "bg_color": bg_color,
            "icon_color": AccentColors.GREEN,
            "text": "완료",
            "corner_radius": 12,
        }

    @staticmethod
    def get_error_style() -> dict:
        """실패 카드 스타일을 반환한다.

        Returns:
            icon_color 키를 포함하는 딕셔너리
        """
        return {
            "icon_color": AccentColors.RED,
            "corner_radius": 12,
        }

    @staticmethod
    def get_open_button_text(platform: str) -> str:
        """플랫폼에 따른 열기 버튼 텍스트를 반환한다.

        Args:
            platform: sys.platform 값 ("darwin", "win32", "linux")

        Returns:
            버튼에 표시할 텍스트
        """
        if platform == "darwin":
            return "Finder에서 보기"
        return "폴더 열기"
