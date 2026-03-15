"""colors.py Apple HIG 색상 검증 테스트.

Apple 시스템 색상과의 일관성 및 확장 필드를 검증한다.
"""

from __future__ import annotations


class Test_다크팔레트_Apple_색상:
    """DARK_PALETTE이 Apple 다크 모드 색상을 사용하는지 검증한다."""

    def test_배경색이_Apple_다크(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        # Apple 다크 모드 시스템 배경색 기반
        assert DARK_PALETTE.background == "#1C1C1E"

    def test_표면색이_Apple_다크(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert DARK_PALETTE.surface == "#2C2C2E"

    def test_액센트_블루(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert DARK_PALETTE.primary == "#007AFF"


class Test_라이트팔레트_Apple_색상:
    """LIGHT_PALETTE이 Apple 라이트 모드 색상을 사용하는지 검증한다."""

    def test_배경색이_Apple_라이트(self):
        from pdf_tool.gui.colors import LIGHT_PALETTE

        assert LIGHT_PALETTE.background == "#F2F2F7"

    def test_표면색이_Apple_라이트(self):
        from pdf_tool.gui.colors import LIGHT_PALETTE

        assert LIGHT_PALETTE.surface == "#FFFFFF"

    def test_액센트_블루(self):
        from pdf_tool.gui.colors import LIGHT_PALETTE

        assert LIGHT_PALETTE.primary == "#007AFF"


class Test_팔레트_확장_필드:
    """ColorPalette에 사이드바, vibrancy 필드가 확장되었는지 검증한다."""

    def test_사이드바_배경색(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert hasattr(DARK_PALETTE, "sidebar_bg")
        assert isinstance(DARK_PALETTE.sidebar_bg, str)

    def test_사이드바_호버(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert hasattr(DARK_PALETTE, "sidebar_hover")

    def test_사이드바_선택(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert hasattr(DARK_PALETTE, "sidebar_selected")

    def test_vibrancy_배경(self):
        from pdf_tool.gui.colors import DARK_PALETTE

        assert hasattr(DARK_PALETTE, "vibrancy_bg")

    def test_라이트_사이드바_필드(self):
        from pdf_tool.gui.colors import LIGHT_PALETTE

        assert hasattr(LIGHT_PALETTE, "sidebar_bg")
        assert hasattr(LIGHT_PALETTE, "sidebar_hover")
        assert hasattr(LIGHT_PALETTE, "sidebar_selected")
        assert hasattr(LIGHT_PALETTE, "vibrancy_bg")


class Test_design_tokens_일관성:
    """get_palette()가 design_tokens.py와 일관되는지 검증한다."""

    def test_다크_배경색_일관성(self):
        from pdf_tool.gui.colors import get_palette
        from pdf_tool.gui.design_tokens import DARK_COLORS

        palette = get_palette("dark")
        assert palette.background == DARK_COLORS.system_background

    def test_라이트_배경색_일관성(self):
        from pdf_tool.gui.colors import get_palette
        from pdf_tool.gui.design_tokens import LIGHT_COLORS

        palette = get_palette("light")
        assert palette.background == LIGHT_COLORS.system_background
