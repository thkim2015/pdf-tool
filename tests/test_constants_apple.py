"""constants.py Apple HIG 호환 검증 테스트.

8pt 그리드, Apple Dynamic Type 스케일, 코너 반지름을 검증한다.
"""

from __future__ import annotations


class Test_8pt_그리드_패딩:
    """패딩 상수가 8pt 그리드를 사용하는지 검증한다."""

    def test_기본_단위_8pt(self):
        from pdf_tool.gui.constants import PADDING_UNIT

        assert PADDING_UNIT == 8

    def test_패딩이_8의_배수(self):
        from pdf_tool.gui.constants import (
            PADDING_LG,
            PADDING_MD,
            PADDING_SM,
            PADDING_XL,
            PADDING_XS,
        )

        for name, value in [
            ("XS", PADDING_XS),
            ("SM", PADDING_SM),
            ("MD", PADDING_MD),
            ("LG", PADDING_LG),
            ("XL", PADDING_XL),
        ]:
            assert value % 8 == 0, f"PADDING_{name}={value}는 8의 배수가 아닙니다"


class Test_Apple_Dynamic_Type_폰트:
    """폰트 크기가 Apple Dynamic Type 스케일을 사용하는지 검증한다."""

    def test_H1_라지타이틀(self):
        from pdf_tool.gui.constants import FONT_SIZE_H1

        assert FONT_SIZE_H1 == 34  # Apple Large Title

    def test_H2_타이틀1(self):
        from pdf_tool.gui.constants import FONT_SIZE_H2

        assert FONT_SIZE_H2 == 28  # Apple Title 1

    def test_H3_타이틀2(self):
        from pdf_tool.gui.constants import FONT_SIZE_H3

        assert FONT_SIZE_H3 == 22  # Apple Title 2

    def test_타이틀_타이틀3(self):
        from pdf_tool.gui.constants import FONT_SIZE_TITLE

        assert FONT_SIZE_TITLE == 20  # Apple Title 3

    def test_기본_바디(self):
        from pdf_tool.gui.constants import FONT_SIZE_BASE

        assert FONT_SIZE_BASE == 17  # Apple Body

    def test_SM_서브헤드라인(self):
        from pdf_tool.gui.constants import FONT_SIZE_SM

        assert FONT_SIZE_SM == 15  # Apple Subheadline

    def test_XS_각주(self):
        from pdf_tool.gui.constants import FONT_SIZE_XS

        assert FONT_SIZE_XS == 13  # Apple Footnote

    def test_LG_캘아웃(self):
        from pdf_tool.gui.constants import FONT_SIZE_LG

        assert FONT_SIZE_LG == 16  # Apple Callout


class Test_Apple_코너_반지름:
    """코너 반지름이 Apple HIG 스타일(6/10/14pt)인지 검증한다."""

    def test_스몰_6pt(self):
        from pdf_tool.gui.constants import BORDER_RADIUS_SM

        assert BORDER_RADIUS_SM == 6

    def test_미디엄_10pt(self):
        from pdf_tool.gui.constants import BORDER_RADIUS_MD

        assert BORDER_RADIUS_MD == 10

    def test_라지_14pt(self):
        from pdf_tool.gui.constants import BORDER_RADIUS_LG

        assert BORDER_RADIUS_LG == 14

    def test_기본값_미디엄(self):
        from pdf_tool.gui.constants import BORDER_RADIUS_DEFAULT, BORDER_RADIUS_MD

        assert BORDER_RADIUS_DEFAULT == BORDER_RADIUS_MD


class Test_design_tokens_일관성:
    """constants.py가 design_tokens.py와 일관되는지 검증한다."""

    def test_패딩_단위_일관성(self):
        from pdf_tool.gui.constants import PADDING_UNIT
        from pdf_tool.gui.design_tokens import Spacing

        assert PADDING_UNIT == Spacing.UNIT

    def test_코너_반지름_일관성(self):
        from pdf_tool.gui.constants import (
            BORDER_RADIUS_LG,
            BORDER_RADIUS_MD,
            BORDER_RADIUS_SM,
        )
        from pdf_tool.gui.design_tokens import CornerRadius

        assert BORDER_RADIUS_SM == CornerRadius.SMALL
        assert BORDER_RADIUS_MD == CornerRadius.MEDIUM
        assert BORDER_RADIUS_LG == CornerRadius.LARGE

    def test_폰트_크기_일관성(self):
        from pdf_tool.gui.constants import (
            FONT_SIZE_BASE,
            FONT_SIZE_H1,
            FONT_SIZE_H2,
            FONT_SIZE_H3,
        )
        from pdf_tool.gui.design_tokens import Typography

        assert FONT_SIZE_H1 == Typography.LARGE_TITLE
        assert FONT_SIZE_H2 == Typography.TITLE1
        assert FONT_SIZE_H3 == Typography.TITLE2
        assert FONT_SIZE_BASE == Typography.BODY
