"""GUI 3단 레이아웃 테스트.

BasePageWidget의 3단 레이아웃(툴바, 컨텐츠, 액션바) 구조를 검증한다.
GUI 위젯을 mock하여 레이아웃 구성 로직만 테스트한다.
"""

from __future__ import annotations

# ============================================================================
# 3단 레이아웃 상수 테스트
# ============================================================================


class Test_레이아웃_상수:
    """3단 레이아웃 관련 상수를 검증한다."""

    def test_툴바_높이(self):
        """툴바 높이는 52pt이다."""
        from pdf_tool.gui.pages.base_page_widget import TOOLBAR_HEIGHT

        assert TOOLBAR_HEIGHT == 52

    def test_액션바_높이(self):
        """액션 바 높이는 56pt이다."""
        from pdf_tool.gui.pages.base_page_widget import ACTION_BAR_HEIGHT

        assert ACTION_BAR_HEIGHT == 56

    def test_액션바_패딩(self):
        """액션 바 패딩은 8pt이다."""
        from pdf_tool.gui.pages.base_page_widget import ACTION_BAR_PADDING

        assert ACTION_BAR_PADDING == 8

    def test_분리선_높이(self):
        """분리선 높이는 1pt이다."""
        from pdf_tool.gui.pages.base_page_widget import SEPARATOR_HEIGHT

        assert SEPARATOR_HEIGHT == 1

    def test_컨텐츠_패딩(self):
        """컨텐츠 좌우 패딩은 24pt이다."""
        from pdf_tool.gui.pages.base_page_widget import CONTENT_PADX

        assert CONTENT_PADX == 24

    def test_컨텐츠_상단_여백(self):
        """컨텐츠 상단 여백은 20pt이다."""
        from pdf_tool.gui.pages.base_page_widget import CONTENT_TOP_MARGIN

        assert CONTENT_TOP_MARGIN == 20

    def test_툴바_패딩(self):
        """툴바 좌우 패딩은 24pt이다."""
        from pdf_tool.gui.pages.base_page_widget import TOOLBAR_PADX

        assert TOOLBAR_PADX == 24


# ============================================================================
# 툴바 스타일 테스트
# ============================================================================


class Test_툴바_스타일:
    """툴바 스타일 계산 로직을 검증한다."""

    def test_툴바_스타일_딕셔너리_키(self):
        """get_toolbar_style()은 height, title_font_size, title_weight를 포함한다."""
        from pdf_tool.gui.pages.base_page_widget import get_toolbar_style

        style = get_toolbar_style()
        assert "height" in style
        assert "title_font_size" in style
        assert "title_weight" in style

    def test_툴바_높이_52pt(self):
        """툴바 높이는 52pt이다."""
        from pdf_tool.gui.pages.base_page_widget import get_toolbar_style

        style = get_toolbar_style()
        assert style["height"] == 52

    def test_툴바_제목_폰트(self):
        """툴바 제목은 22pt Bold이다."""
        from pdf_tool.gui.pages.base_page_widget import get_toolbar_style

        style = get_toolbar_style()
        assert style["title_font_size"] == 22
        assert style["title_weight"] == "bold"


# ============================================================================
# 액션 바 스타일 테스트
# ============================================================================


class Test_액션바_스타일:
    """액션 바 스타일 계산 로직을 검증한다."""

    def test_액션바_스타일_키(self):
        """get_action_bar_style()은 height, separator_height, button_height를 포함한다."""
        from pdf_tool.gui.pages.base_page_widget import get_action_bar_style

        style = get_action_bar_style()
        assert "height" in style
        assert "separator_height" in style
        assert "button_height" in style

    def test_액션바_높이_56pt(self):
        """액션 바 높이는 56pt이다 (8pt 패딩 * 2 + 40pt 버튼)."""
        from pdf_tool.gui.pages.base_page_widget import get_action_bar_style

        style = get_action_bar_style()
        assert style["height"] == 56

    def test_액션바_분리선_1pt(self):
        """액션 바 상단 분리선은 1pt이다."""
        from pdf_tool.gui.pages.base_page_widget import get_action_bar_style

        style = get_action_bar_style()
        assert style["separator_height"] == 1

    def test_액션바_버튼_높이_40pt(self):
        """액션 바 버튼 높이는 40pt이다."""
        from pdf_tool.gui.pages.base_page_widget import get_action_bar_style

        style = get_action_bar_style()
        assert style["button_height"] == 40

    def test_액션바_분리선_색상(self):
        """분리선 색상은 systemGray3이다."""
        from pdf_tool.gui.pages.base_page_widget import get_action_bar_style

        style = get_action_bar_style()
        assert "separator_color" in style
        # systemGray3 색상값
        assert style["separator_color"] == "#48484A"


# ============================================================================
# 기존 기능 호환성 테스트
# ============================================================================


class Test_기존_인터페이스_호환성:
    """BasePageWidget의 기존 인터페이스가 유지됨을 검증한다."""

    def test_BasePage_로직_변경_없음(self):
        """BasePage의 generate_output_path는 변경되지 않는다."""
        from pathlib import Path

        from pdf_tool.gui.pages.base_page import generate_output_path

        result = generate_output_path(Path("/tmp/test.pdf"))
        assert result == Path("/tmp/test_output.pdf")

    def test_BasePage_would_overwrite_변경_없음(self):
        """BasePage의 would_overwrite는 변경되지 않는다."""
        from pathlib import Path

        from pdf_tool.gui.pages.base_page import would_overwrite

        assert would_overwrite(Path("/tmp/a.pdf"), Path("/tmp/a.pdf")) is True
        assert would_overwrite(Path("/tmp/a.pdf"), Path("/tmp/b.pdf")) is False

    def test_ExecutionState_변경_없음(self):
        """ExecutionState는 변경되지 않는다."""
        from pathlib import Path

        from pdf_tool.gui.pages.base_page import ExecutionState

        state = ExecutionState()
        assert state.is_executing is False
        state.start(Path("/tmp/test.pdf"))
        assert state.is_executing is True
        state.finish()
        assert state.is_executing is False


# ============================================================================
# 페이지 레이아웃 적용 검증 (각 페이지별)
# ============================================================================


class Test_페이지_레이아웃_상수_존재:
    """각 페이지가 3단 레이아웃 상수를 사용할 수 있는지 검증한다."""

    def test_레이아웃_상수_임포트(self):
        """레이아웃 상수가 base_page_widget에서 임포트 가능하다."""
        from pdf_tool.gui.pages.base_page_widget import (
            ACTION_BAR_HEIGHT,
            ACTION_BAR_PADDING,
            CONTENT_PADX,
            CONTENT_TOP_MARGIN,
            SEPARATOR_HEIGHT,
            TOOLBAR_HEIGHT,
            TOOLBAR_PADX,
        )

        assert TOOLBAR_HEIGHT > 0
        assert ACTION_BAR_HEIGHT > 0
        assert ACTION_BAR_PADDING > 0
        assert SEPARATOR_HEIGHT > 0
        assert CONTENT_PADX > 0
        assert CONTENT_TOP_MARGIN > 0
        assert TOOLBAR_PADX > 0

    def test_스타일_함수_임포트(self):
        """스타일 함수가 base_page_widget에서 임포트 가능하다."""
        from pdf_tool.gui.pages.base_page_widget import (
            get_action_bar_style,
            get_toolbar_style,
        )

        assert callable(get_toolbar_style)
        assert callable(get_action_bar_style)


# ============================================================================
# PdfPreviewWidget Quick Look 스타일 테스트
# ============================================================================


# ============================================================================
# 페이지별 page_title / action_button_text 테스트
# ============================================================================


class Test_페이지_타이틀_속성:
    """각 페이지 위젯의 page_title과 action_button_text를 검증한다."""

    def test_cut_페이지_타이틀(self):
        """CutPageWidget의 page_title은 '자르기'이다."""
        from pdf_tool.gui.pages.cut_page_widget import CutPageWidget

        assert CutPageWidget.page_title == "자르기"
        assert CutPageWidget.action_button_text == "자르기"

    def test_split_페이지_타이틀(self):
        """SplitPageWidget의 page_title은 '분할'이다."""
        from pdf_tool.gui.pages.split_page_widget import SplitPageWidget

        assert SplitPageWidget.page_title == "분할"
        assert SplitPageWidget.action_button_text == "분할"

    def test_rotate_페이지_타이틀(self):
        """RotatePageWidget의 page_title은 '회전'이다."""
        from pdf_tool.gui.pages.rotate_page_widget import RotatePageWidget

        assert RotatePageWidget.page_title == "회전"
        assert RotatePageWidget.action_button_text == "회전"

    def test_resize_페이지_타이틀(self):
        """ResizePageWidget의 page_title은 '크기 조정'이다."""
        from pdf_tool.gui.pages.resize_page_widget import ResizePageWidget

        assert ResizePageWidget.page_title == "크기 조정"
        assert ResizePageWidget.action_button_text == "크기 조정"

    def test_compress_페이지_타이틀(self):
        """CompressPageWidget의 page_title은 '압축'이다."""
        from pdf_tool.gui.pages.compress_page_widget import CompressPageWidget

        assert CompressPageWidget.page_title == "압축"
        assert CompressPageWidget.action_button_text == "압축"

    def test_watermark_페이지_타이틀(self):
        """WatermarkPageWidget의 page_title은 '워터마크'이다."""
        from pdf_tool.gui.pages.watermark_page_widget import WatermarkPageWidget

        assert WatermarkPageWidget.page_title == "워터마크"
        assert WatermarkPageWidget.action_button_text == "추가"

    def test_image_to_pdf_페이지_타이틀(self):
        """ImageToPdfPageWidget의 page_title은 '이미지 -> PDF'이다."""
        from pdf_tool.gui.pages.image_to_pdf_page_widget import ImageToPdfPageWidget

        assert ImageToPdfPageWidget.page_title == "이미지 -> PDF"
        assert ImageToPdfPageWidget.action_button_text == "변환"


class Test_BasePageWidget_기본_속성:
    """BasePageWidget의 기본 속성을 검증한다."""

    def test_기본_page_title(self):
        """BasePageWidget의 기본 page_title은 빈 문자열이다."""
        from pdf_tool.gui.pages.base_page_widget import BasePageWidget

        assert BasePageWidget.page_title == ""

    def test_기본_action_button_text(self):
        """BasePageWidget의 기본 action_button_text는 '실행'이다."""
        from pdf_tool.gui.pages.base_page_widget import BasePageWidget

        assert BasePageWidget.action_button_text == "실행"


# ============================================================================
# PdfPreviewWidget Quick Look 스타일 테스트
# ============================================================================


class Test_MacOSButton_스타일_커버리지:
    """MacOSButtonStyle의 미커버 경로를 검증한다."""

    def test_unknown_style_fallback(self):
        """알 수 없는 스타일은 primary로 폴백한다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("unknown", "regular")
        primary = MacOSButtonStyle.get_style("primary", "regular")
        assert style["bg_color"] == primary["bg_color"]

    def test_unknown_size_fallback(self):
        """알 수 없는 크기는 regular로 폴백한다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "unknown")
        regular = MacOSButtonStyle.get_style("primary", "regular")
        assert style["height"] == regular["height"]

    def test_get_hover_color_unknown(self):
        """알 수 없는 스타일의 호버 색상은 primary로 폴백한다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        color = MacOSButtonStyle.get_hover_color("unknown")
        primary_hover = MacOSButtonStyle.get_hover_color("primary")
        assert color == primary_hover

    def test_get_disabled_style(self):
        """비활성 스타일은 opacity 키를 포함한다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_disabled_style()
        assert "opacity" in style
        assert style["opacity"] == 0.5


class Test_Quick_Look_스타일:
    """PdfPreviewWidget Quick Look 스타일 상수를 검증한다."""

    def test_코너_반지름_8pt(self):
        """Quick Look 코너 반지름은 8pt이다."""
        from pdf_tool.gui.widgets.pdf_preview_widget import QUICK_LOOK_CORNER_RADIUS

        assert QUICK_LOOK_CORNER_RADIUS == 8

    def test_그림자_스타일(self):
        """Quick Look 그림자 스타일을 검증한다."""
        from pdf_tool.gui.widgets.pdf_preview_widget import get_quick_look_style

        style = get_quick_look_style()
        assert "corner_radius" in style
        assert style["corner_radius"] == 8

    def test_스타일_딕셔너리(self):
        """get_quick_look_style()은 필요한 키를 포함한다."""
        from pdf_tool.gui.widgets.pdf_preview_widget import get_quick_look_style

        style = get_quick_look_style()
        assert "corner_radius" in style
        assert "shadow" in style
