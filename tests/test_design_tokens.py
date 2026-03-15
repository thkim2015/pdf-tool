"""디자인 토큰 테스트.

Apple Human Interface Guidelines 기반 디자인 토큰 시스템을 검증한다.
"""

from __future__ import annotations

import pytest

# ============================================================================
# Apple 시스템 색상 테스트 (다크 모드)
# ============================================================================


class Test_다크모드_시스템_색상:
    """Apple 다크 모드 시스템 색상이 올바르게 정의되어 있는지 검증한다."""

    def test_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import DARK_COLORS

        assert DARK_COLORS.system_background in ("#000000", "#1C1C1E")

    def test_보조_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import DARK_COLORS

        assert DARK_COLORS.secondary_system_background == "#1C1C1E"

    def test_삼차_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import DARK_COLORS

        assert DARK_COLORS.tertiary_system_background == "#2C2C2E"

    def test_시스템_색상_불변(self):
        """시스템 색상은 불변이다 (frozen dataclass)."""
        from dataclasses import FrozenInstanceError

        from pdf_tool.gui.design_tokens import DARK_COLORS

        with pytest.raises(FrozenInstanceError):
            DARK_COLORS.system_background = "#FFFFFF"


# ============================================================================
# Apple 시스템 색상 테스트 (라이트 모드)
# ============================================================================


class Test_라이트모드_시스템_색상:
    """Apple 라이트 모드 시스템 색상이 올바르게 정의되어 있는지 검증한다."""

    def test_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import LIGHT_COLORS

        assert LIGHT_COLORS.system_background in ("#FFFFFF", "#F2F2F7")

    def test_보조_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import LIGHT_COLORS

        assert LIGHT_COLORS.secondary_system_background == "#F2F2F7"

    def test_삼차_시스템_배경색(self):
        from pdf_tool.gui.design_tokens import LIGHT_COLORS

        assert LIGHT_COLORS.tertiary_system_background == "#FFFFFF"


# ============================================================================
# Apple 액센트 컬러 테스트
# ============================================================================


class Test_액센트_컬러:
    """Apple 액센트 컬러가 올바르게 정의되어 있는지 검증한다."""

    def test_블루(self):
        from pdf_tool.gui.design_tokens import AccentColors

        assert AccentColors.BLUE == "#007AFF"

    def test_그린(self):
        from pdf_tool.gui.design_tokens import AccentColors

        assert AccentColors.GREEN == "#34C759"

    def test_레드(self):
        from pdf_tool.gui.design_tokens import AccentColors

        assert AccentColors.RED == "#FF3B30"

    def test_오렌지(self):
        from pdf_tool.gui.design_tokens import AccentColors

        assert AccentColors.ORANGE == "#FF9500"

    def test_옐로우(self):
        from pdf_tool.gui.design_tokens import AccentColors

        assert AccentColors.YELLOW == "#FFCC00"


# ============================================================================
# Typography (SF Pro) 테스트
# ============================================================================


class Test_타이포그래피:
    """Apple Dynamic Type 스케일이 올바르게 정의되어 있는지 검증한다."""

    def test_라지_타이틀(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.LARGE_TITLE == 34

    def test_타이틀1(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.TITLE1 == 28

    def test_타이틀2(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.TITLE2 == 22

    def test_타이틀3(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.TITLE3 == 20

    def test_헤드라인(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.HEADLINE == 17

    def test_헤드라인_볼드(self):
        """헤드라인은 기본적으로 Bold이다."""
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.HEADLINE_WEIGHT == "bold"

    def test_바디(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.BODY == 17

    def test_캘아웃(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.CALLOUT == 16

    def test_서브헤드라인(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.SUBHEADLINE == 15

    def test_각주(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.FOOTNOTE == 13

    def test_캡션(self):
        from pdf_tool.gui.design_tokens import Typography

        assert Typography.CAPTION == 12


# ============================================================================
# Font Stacks 테스트
# ============================================================================


class Test_폰트_스택:
    """플랫폼별 폰트 스택이 올바르게 정의되어 있는지 검증한다."""

    def test_macOS_텍스트_폰트(self):
        from pdf_tool.gui.design_tokens import FontStacks

        assert "SF Pro Text" in FontStacks.MACOS

    def test_macOS_디스플레이_폰트(self):
        from pdf_tool.gui.design_tokens import FontStacks

        assert "SF Pro Display" in FontStacks.MACOS

    def test_macOS_모노_폰트(self):
        from pdf_tool.gui.design_tokens import FontStacks

        assert "SF Mono" in FontStacks.MACOS_MONO

    def test_Windows_폰트(self):
        from pdf_tool.gui.design_tokens import FontStacks

        assert "Segoe UI" in FontStacks.WINDOWS

    def test_Linux_폰트(self):
        from pdf_tool.gui.design_tokens import FontStacks

        assert "Inter" in FontStacks.LINUX
        assert "Cantarell" in FontStacks.LINUX


# ============================================================================
# Spacing (8pt 그리드) 테스트
# ============================================================================


class Test_스페이싱:
    """8pt 그리드 기반 스페이싱이 올바르게 정의되어 있는지 검증한다."""

    def test_기본_단위(self):
        from pdf_tool.gui.design_tokens import Spacing

        assert Spacing.UNIT == 8

    def test_스페이싱_값들(self):
        from pdf_tool.gui.design_tokens import Spacing

        assert Spacing.XS == 8    # 1 * 8
        assert Spacing.SM == 16   # 2 * 8
        assert Spacing.MD == 24   # 3 * 8
        assert Spacing.LG == 32   # 4 * 8
        assert Spacing.XL == 40   # 5 * 8

    def test_스페이싱이_8pt_배수(self):
        """모든 스페이싱 값이 8pt의 배수이다."""
        from pdf_tool.gui.design_tokens import Spacing

        for name in ("XS", "SM", "MD", "LG", "XL"):
            value = getattr(Spacing, name)
            assert value % 8 == 0, f"{name}={value}는 8의 배수가 아닙니다"


# ============================================================================
# Corner Radius 테스트
# ============================================================================


class Test_코너_반지름:
    """코너 반지름이 올바르게 정의되어 있는지 검증한다."""

    def test_스몰(self):
        from pdf_tool.gui.design_tokens import CornerRadius

        assert CornerRadius.SMALL == 6

    def test_미디엄(self):
        from pdf_tool.gui.design_tokens import CornerRadius

        assert CornerRadius.MEDIUM == 10

    def test_라지(self):
        from pdf_tool.gui.design_tokens import CornerRadius

        assert CornerRadius.LARGE == 14


# ============================================================================
# Animation Timings 테스트
# ============================================================================


class Test_애니메이션_타이밍:
    """애니메이션 타이밍이 올바르게 정의되어 있는지 검증한다."""

    def test_빠름(self):
        from pdf_tool.gui.design_tokens import AnimationTiming

        assert AnimationTiming.FAST == 0.1

    def test_보통(self):
        from pdf_tool.gui.design_tokens import AnimationTiming

        assert AnimationTiming.NORMAL == 0.15

    def test_느림(self):
        from pdf_tool.gui.design_tokens import AnimationTiming

        assert AnimationTiming.SLOW == 0.3


# ============================================================================
# 팩토리 함수 테스트
# ============================================================================


class Test_팩토리_함수:
    """get_tokens_for_mode 팩토리 함수를 검증한다."""

    def test_다크모드_토큰_반환(self):
        from pdf_tool.gui.design_tokens import DARK_COLORS, get_tokens_for_mode

        tokens = get_tokens_for_mode("dark")
        assert tokens is DARK_COLORS

    def test_라이트모드_토큰_반환(self):
        from pdf_tool.gui.design_tokens import LIGHT_COLORS, get_tokens_for_mode

        tokens = get_tokens_for_mode("light")
        assert tokens is LIGHT_COLORS

    def test_잘못된_모드_기본값(self):
        from pdf_tool.gui.design_tokens import DARK_COLORS, get_tokens_for_mode

        tokens = get_tokens_for_mode("invalid")
        assert tokens is DARK_COLORS


# ============================================================================
# DesignTokens 데이터클래스 테스트
# ============================================================================


class Test_디자인토큰_구조:
    """DesignTokens 데이터클래스 구조를 검증한다."""

    def test_데이터클래스_frozen(self):
        """SystemColors는 frozen dataclass이다."""
        from dataclasses import FrozenInstanceError

        from pdf_tool.gui.design_tokens import DARK_COLORS

        with pytest.raises(FrozenInstanceError):
            DARK_COLORS.system_background = "#000000"

    def test_다크_라이트_색상_차이(self):
        """다크와 라이트 색상이 서로 다르다."""
        from pdf_tool.gui.design_tokens import DARK_COLORS, LIGHT_COLORS

        assert DARK_COLORS.system_background != LIGHT_COLORS.system_background
