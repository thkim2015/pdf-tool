"""Task 5.4: 고대비 모드 테스트 (Optional).

시스템 고대비 감지, WCAG AAA 대비 기준(7:1),
보더 두께 증가를 검증한다.
"""

from __future__ import annotations


class Test_고대비_감지:
    """시스템 고대비 모드 감지를 검증한다."""

    def test_고대비_모드_기본값_비활성(self):
        """고대비 모드의 기본값은 False이다."""
        from pdf_tool.gui.accessibility import is_high_contrast_enabled

        assert is_high_contrast_enabled() is False

    def test_고대비_모드_수동_활성화(self):
        """고대비 모드를 수동으로 활성화할 수 있다."""
        from pdf_tool.gui.accessibility import (
            is_high_contrast_enabled,
            set_high_contrast,
        )

        set_high_contrast(True)
        assert is_high_contrast_enabled() is True

        # 정리
        set_high_contrast(False)

    def test_고대비_모드_토글(self):
        """toggle_high_contrast()로 고대비를 토글할 수 있다."""
        from pdf_tool.gui.accessibility import (
            is_high_contrast_enabled,
            set_high_contrast,
            toggle_high_contrast,
        )

        set_high_contrast(False)
        toggle_high_contrast()
        assert is_high_contrast_enabled() is True

        toggle_high_contrast()
        assert is_high_contrast_enabled() is False


class Test_고대비_색상:
    """고대비 모드의 색상 강화를 검증한다."""

    def test_고대비_다크_배경_더_어두움(self):
        """고대비 다크 모드의 배경이 더 어둡다."""
        from pdf_tool.gui.accessibility import get_high_contrast_colors

        colors = get_high_contrast_colors("dark")
        # 일반 다크 배경은 #1C1C1E, 고대비는 더 어두움
        assert colors["background"] == "#000000"

    def test_고대비_라이트_배경_더_밝음(self):
        """고대비 라이트 모드의 배경이 더 밝다."""
        from pdf_tool.gui.accessibility import get_high_contrast_colors

        colors = get_high_contrast_colors("light")
        assert colors["background"] == "#FFFFFF"

    def test_고대비_텍스트_대비_강화(self):
        """고대비 모드에서 텍스트 대비가 강화된다."""
        from pdf_tool.gui.accessibility import get_high_contrast_colors

        dark_colors = get_high_contrast_colors("dark")
        assert dark_colors["text_primary"] == "#FFFFFF"

        light_colors = get_high_contrast_colors("light")
        assert light_colors["text_primary"] == "#000000"


class Test_고대비_보더:
    """고대비 모드의 보더 두께 조정을 검증한다."""

    def test_일반_모드_보더_1pt(self):
        """일반 모드 보더 두께는 1pt이다."""
        from pdf_tool.gui.accessibility import get_border_width

        assert get_border_width(high_contrast=False) == 1

    def test_고대비_모드_보더_2pt(self):
        """고대비 모드 보더 두께는 2pt이다."""
        from pdf_tool.gui.accessibility import get_border_width

        assert get_border_width(high_contrast=True) == 2


class Test_색상_대비_계산:
    """WCAG 색상 대비 비율 계산을 검증한다."""

    def test_흑백_최대_대비(self):
        """검정/흰색의 대비 비율은 21:1이다."""
        from pdf_tool.gui.accessibility import calculate_contrast_ratio

        ratio = calculate_contrast_ratio("#000000", "#FFFFFF")
        assert abs(ratio - 21.0) < 0.1

    def test_같은_색_대비_1(self):
        """같은 색의 대비 비율은 1:1이다."""
        from pdf_tool.gui.accessibility import calculate_contrast_ratio

        ratio = calculate_contrast_ratio("#FFFFFF", "#FFFFFF")
        assert abs(ratio - 1.0) < 0.1

    def test_WCAG_AAA_기준_7_1(self):
        """WCAG AAA 대비 기준은 7:1이다."""
        from pdf_tool.gui.accessibility import WCAG_AAA_CONTRAST_RATIO

        assert WCAG_AAA_CONTRAST_RATIO == 7.0

    def test_고대비_다크_텍스트_WCAG_AAA_충족(self):
        """고대비 다크 모드의 텍스트/배경 대비가 WCAG AAA를 충족한다."""
        from pdf_tool.gui.accessibility import (
            WCAG_AAA_CONTRAST_RATIO,
            calculate_contrast_ratio,
            get_high_contrast_colors,
        )

        colors = get_high_contrast_colors("dark")
        ratio = calculate_contrast_ratio(
            colors["text_primary"], colors["background"]
        )
        assert ratio >= WCAG_AAA_CONTRAST_RATIO
