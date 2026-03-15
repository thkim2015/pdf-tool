"""macOS 스타일 위젯 테스트.

TAG-002: Sidebar + Core Components
SidebarItem, MacOSButton, SegmentedControl 위젯의 순수 로직을 검증한다.
"""

from __future__ import annotations

# ============================================================================
# Task 2.1: SidebarItem 테스트
# ============================================================================


class Test_SidebarItemState:
    """SidebarItem 위젯의 상태 관리 로직을 검증한다."""

    def test_초기_상태(self):
        """초기 상태는 선택되지 않고 호버되지 않은 상태이다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        assert state.icon == "\u2702"
        assert state.label == "Cut"
        assert state.value == "cut"
        assert state.selected is False
        assert state.hovered is False
        assert state.enabled is True

    def test_선택_상태_설정(self):
        """set_selected(True) 호출 시 선택 상태로 전환된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_selected(True)
        assert state.selected is True

    def test_선택_해제(self):
        """set_selected(False) 호출 시 선택 해제된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_selected(True)
        state.set_selected(False)
        assert state.selected is False

    def test_호버_상태_설정(self):
        """set_hovered(True) 호출 시 호버 상태로 전환된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_hovered(True)
        assert state.hovered is True

    def test_호버_해제(self):
        """set_hovered(False) 호출 시 호버 해제된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_hovered(True)
        state.set_hovered(False)
        assert state.hovered is False

    def test_비활성_상태(self):
        """set_enabled(False) 호출 시 비활성 상태가 된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_enabled(False)
        assert state.enabled is False

    def test_비활성_상태에서_선택_불가(self):
        """비활성 상태에서는 선택이 무시된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_enabled(False)
        state.set_selected(True)
        assert state.selected is False

    def test_스타일_기본_상태(self):
        """기본 상태의 스타일은 투명 배경이다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        style = state.get_style()
        assert style["bg_color"] == "transparent"
        assert style["opacity"] == 1.0

    def test_스타일_선택_상태(self):
        """선택 상태의 스타일은 accent 배경이다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_selected(True)
        style = state.get_style()
        assert style["bg_color"] == "#007AFF"
        assert style["corner_radius"] == 6
        assert style["padx"] == 8
        assert style["pady"] == 4

    def test_스타일_호버_상태(self):
        """호버 상태의 스타일은 미세한 배경 변화이다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_hovered(True)
        style = state.get_style()
        assert style["bg_color"] != "transparent"

    def test_스타일_비활성_상태(self):
        """비활성 상태의 스타일은 opacity 0.5이다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        state = SidebarItemState(icon="\u2702", label="Cut", value="cut")
        state.set_enabled(False)
        style = state.get_style()
        assert style["opacity"] == 0.5

    def test_아이콘_크기(self):
        """아이콘 크기는 24x24px이다."""
        from pdf_tool.gui.widgets.sidebar_item import SIDEBAR_ICON_SIZE

        assert SIDEBAR_ICON_SIZE == 24

    def test_텍스트_간격(self):
        """아이콘과 텍스트 간격은 8pt이다."""
        from pdf_tool.gui.widgets.sidebar_item import SIDEBAR_TEXT_SPACING

        assert SIDEBAR_TEXT_SPACING == 8


# ============================================================================
# Task 2.2: MacOSButton 테스트
# ============================================================================


class Test_MacOSButtonStyle:
    """MacOSButton 위젯의 스타일 계산 로직을 검증한다."""

    def test_primary_스타일(self):
        """Primary 스타일은 accent 배경과 흰색 텍스트이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "regular")
        assert style["bg_color"] == "#007AFF"
        assert style["text_color"] == "#FFFFFF"
        assert style["corner_radius"] == 6

    def test_secondary_스타일(self):
        """Secondary 스타일은 회색 배경이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("secondary", "regular")
        assert style["bg_color"] != "#007AFF"
        assert style["text_color"] != "#FFFFFF"

    def test_destructive_스타일(self):
        """Destructive 스타일은 빨강 배경과 흰색 텍스트이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("destructive", "regular")
        assert style["bg_color"] == "#FF3B30"
        assert style["text_color"] == "#FFFFFF"

    def test_regular_크기(self):
        """Regular 크기는 높이 28pt이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "regular")
        assert style["height"] == 28

    def test_mini_크기(self):
        """Mini 크기는 높이 22pt이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "mini")
        assert style["height"] == 22

    def test_large_크기(self):
        """Large 크기는 높이 36pt이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "large")
        assert style["height"] == 36

    def test_호버_색상_primary(self):
        """Primary 호버 시 배경색이 어두워진다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        hover = MacOSButtonStyle.get_hover_color("primary")
        assert hover != "#007AFF"
        assert isinstance(hover, str)

    def test_호버_색상_destructive(self):
        """Destructive 호버 시 배경색이 어두워진다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        hover = MacOSButtonStyle.get_hover_color("destructive")
        assert hover != "#FF3B30"

    def test_비활성_스타일(self):
        """비활성 상태에서 opacity는 0.5이다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_disabled_style()
        assert style["opacity"] == 0.5

    def test_유효하지_않은_스타일_기본값(self):
        """유효하지 않은 스타일은 primary로 기본 처리된다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("invalid", "regular")
        assert style["bg_color"] == "#007AFF"

    def test_유효하지_않은_크기_기본값(self):
        """유효하지 않은 크기는 regular로 기본 처리된다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        style = MacOSButtonStyle.get_style("primary", "invalid")
        assert style["height"] == 28


# ============================================================================
# Task 2.7: SegmentedControl 테스트
# ============================================================================


class Test_SegmentedControlState:
    """SegmentedControl 위젯의 상태 관리 로직을 검증한다."""

    def test_초기_상태(self):
        """초기 상태에서 첫 번째 값이 선택된다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        assert state.get_value() == "A"
        assert state.values == ["A", "B", "C"]

    def test_값_설정(self):
        """set_value()로 선택 값을 변경할 수 있다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        state.set_value("B")
        assert state.get_value() == "B"

    def test_유효하지_않은_값_설정_무시(self):
        """values에 없는 값은 설정이 무시된다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        state.set_value("D")
        assert state.get_value() == "A"

    def test_선택_인덱스(self):
        """선택된 값의 인덱스를 반환한다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        state.set_value("B")
        assert state.get_selected_index() == 1

    def test_콜백_호출(self):
        """값 변경 시 on_change 콜백이 호출된다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        callback_values = []
        state = SegmentedControlState(
            values=["A", "B", "C"],
            on_change=lambda v: callback_values.append(v),
        )
        state.set_value("B")
        assert callback_values == ["B"]

    def test_같은_값_선택_시_콜백_미호출(self):
        """같은 값을 다시 선택하면 콜백이 호출되지 않는다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        callback_values = []
        state = SegmentedControlState(
            values=["A", "B", "C"],
            on_change=lambda v: callback_values.append(v),
        )
        state.set_value("A")  # 이미 A가 선택됨
        assert callback_values == []

    def test_빈_values_예외(self):
        """빈 values 리스트는 ValueError를 발생시킨다."""
        import pytest

        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        with pytest.raises(ValueError):
            SegmentedControlState(values=[])

    def test_스타일_캡슐_배경(self):
        """캡슐 형태의 배경 스타일을 반환한다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        style = state.get_container_style()
        assert style["corner_radius"] == 8

    def test_선택_인디케이터_스타일(self):
        """선택 인디케이터의 스타일을 반환한다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        style = state.get_indicator_style()
        assert style["bg_color"] == "#FFFFFF"
        assert style["corner_radius"] == 6

    def test_세그먼트_선택_텍스트_색상(self):
        """선택된 세그먼트의 텍스트 색상을 반환한다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        style = state.get_segment_style("A")
        assert style["selected"] is True
        assert style["text_color"] == "#000000"

    def test_세그먼트_미선택_텍스트_색상(self):
        """미선택된 세그먼트의 텍스트 색상을 반환한다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        style = state.get_segment_style("B")
        assert style["selected"] is False


# ============================================================================
# Task 2.4: FilePickerWidget 스타일 테스트
# ============================================================================


class Test_FilePickerStyle:
    """FilePickerWidget의 macOS 드롭 영역 스타일을 검증한다."""

    def test_드롭_영역_스타일_라이트(self):
        """라이트 모드 드롭 영역 보더 색상이다."""
        from pdf_tool.gui.widgets.file_picker_style import FilePickerDropZoneStyle

        style = FilePickerDropZoneStyle.get_style("light")
        assert style["border_color"] == "#D1D1D6"
        assert style["border_width"] == 2
        assert style["corner_radius"] == 12
        assert style["padding"] == 20

    def test_드롭_영역_스타일_다크(self):
        """다크 모드 드롭 영역 보더 색상이다."""
        from pdf_tool.gui.widgets.file_picker_style import FilePickerDropZoneStyle

        style = FilePickerDropZoneStyle.get_style("dark")
        assert style["border_color"] == "#3A3A3C"

    def test_드래그_오버_스타일(self):
        """드래그 오버 상태의 보더 색상은 accent이다."""
        from pdf_tool.gui.widgets.file_picker_style import FilePickerDropZoneStyle

        style = FilePickerDropZoneStyle.get_drag_over_style()
        assert style["border_color"] == "#007AFF"


# ============================================================================
# Task 2.5: ProgressBarWidget 스타일 테스트
# ============================================================================


class Test_ProgressBarStyle:
    """ProgressBarWidget의 macOS 스타일을 검증한다."""

    def test_프로그레스_바_높이(self):
        """프로그레스 바 높이는 4pt이다."""
        from pdf_tool.gui.widgets.progress_bar_style import ProgressBarStyle

        style = ProgressBarStyle.get_style()
        assert style["height"] == 4
        assert style["corner_radius"] == 2

    def test_프로그레스_바_색상_라이트(self):
        """라이트 모드 프로그레스 바 색상이다."""
        from pdf_tool.gui.widgets.progress_bar_style import ProgressBarStyle

        style = ProgressBarStyle.get_colors("light")
        assert style["progress_color"] == "#007AFF"
        assert style["bg_color"] == "#E5E5EA"

    def test_프로그레스_바_색상_다크(self):
        """다크 모드 프로그레스 바 색상이다."""
        from pdf_tool.gui.widgets.progress_bar_style import ProgressBarStyle

        style = ProgressBarStyle.get_colors("dark")
        assert style["progress_color"] == "#007AFF"
        assert style["bg_color"] == "#3A3A3C"

    def test_백분율_계산(self):
        """백분율 계산이 올바르다."""
        from pdf_tool.gui.widgets.progress_bar_style import ProgressBarStyle

        assert ProgressBarStyle.calculate_percentage(50, 100) == 50.0
        assert ProgressBarStyle.calculate_percentage(0, 100) == 0.0
        assert ProgressBarStyle.calculate_percentage(100, 100) == 100.0

    def test_백분율_계산_0_나누기(self):
        """total이 0이면 0.0을 반환한다."""
        from pdf_tool.gui.widgets.progress_bar_style import ProgressBarStyle

        assert ProgressBarStyle.calculate_percentage(50, 0) == 0.0


# ============================================================================
# Task 2.6: ResultDisplayWidget 스타일 테스트
# ============================================================================


class Test_ResultDisplayStyle:
    """ResultDisplayWidget의 macOS 카드 스타일을 검증한다."""

    def test_성공_카드_스타일_라이트(self):
        """라이트 모드 성공 카드 스타일이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        style = ResultCardStyle.get_success_style("light")
        assert style["bg_color"] == "#F0F0F0"
        assert style["icon_color"] == "#34C759"
        assert style["corner_radius"] == 12

    def test_성공_카드_스타일_다크(self):
        """다크 모드 성공 카드 스타일이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        style = ResultCardStyle.get_success_style("dark")
        assert style["bg_color"] == "#2C2C2E"
        assert style["icon_color"] == "#34C759"

    def test_실패_카드_스타일(self):
        """실패 카드 아이콘 색상은 빨강이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        style = ResultCardStyle.get_error_style()
        assert style["icon_color"] == "#FF3B30"

    def test_열기_버튼_텍스트_macos(self):
        """macOS에서 버튼 텍스트는 'Finder에서 보기'이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        text = ResultCardStyle.get_open_button_text("darwin")
        assert text == "Finder에서 보기"

    def test_열기_버튼_텍스트_windows(self):
        """Windows에서 버튼 텍스트는 '폴더 열기'이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        text = ResultCardStyle.get_open_button_text("win32")
        assert text == "폴더 열기"

    def test_열기_버튼_텍스트_linux(self):
        """Linux에서 버튼 텍스트는 '폴더 열기'이다."""
        from pdf_tool.gui.widgets.result_display_style import ResultCardStyle

        text = ResultCardStyle.get_open_button_text("linux")
        assert text == "폴더 열기"


# ============================================================================
# TAG-004 Task 4.3: 버튼/위젯 마이크로 인터랙션 테스트
# ============================================================================


class Test_MacOSButton_호버_효과:
    """버튼 호버 시 배경색 변화를 검증한다."""

    def test_호버_색상_primary_20퍼센트_어두움(self):
        """Primary 호버 색상은 기본 색상보다 어둡다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        base = MacOSButtonStyle.get_style("primary", "regular")["bg_color"]
        hover = MacOSButtonStyle.get_hover_color("primary")
        assert hover != base

    def test_호버_색상_secondary_20퍼센트_어두움(self):
        """Secondary 호버 색상은 정의되어 있다."""
        from pdf_tool.gui.widgets.macos_button import MacOSButtonStyle

        hover = MacOSButtonStyle.get_hover_color("secondary")
        assert isinstance(hover, str)
        assert hover.startswith("#")

    def test_호버_애니메이션_duration(self):
        """버튼 호버 애니메이션 시간은 0.15초이다."""
        from pdf_tool.gui.widgets.macos_button import HOVER_ANIMATION_DURATION

        assert HOVER_ANIMATION_DURATION == 0.15


class Test_MacOSButton_클릭_효과:
    """버튼 클릭 시 스케일 효과를 검증한다."""

    def test_클릭_스케일_값(self):
        """클릭 시 스케일은 0.98이다."""
        from pdf_tool.gui.widgets.macos_button import CLICK_SCALE

        assert CLICK_SCALE == 0.98

    def test_클릭_애니메이션_duration(self):
        """클릭 애니메이션 시간은 0.1초이다."""
        from pdf_tool.gui.widgets.macos_button import CLICK_ANIMATION_DURATION

        assert CLICK_ANIMATION_DURATION == 0.1


class Test_SegmentedControl_슬라이딩:
    """세그먼티드 컨트롤의 슬라이드 애니메이션을 검증한다."""

    def test_인디케이터_애니메이션_duration(self):
        """선택 인디케이터 슬라이드 애니메이션 시간은 0.2초이다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        style = state.get_indicator_style()
        assert style["animation_duration"] == 0.2

    def test_인디케이터_위치_계산(self):
        """선택 인덱스에 따른 인디케이터 위치를 계산할 수 있다."""
        from pdf_tool.gui.widgets.segmented_control import SegmentedControlState

        state = SegmentedControlState(values=["A", "B", "C"])
        assert state.get_selected_index() == 0
        state.set_value("C")
        assert state.get_selected_index() == 2
