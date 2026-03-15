"""GUI Progress Bar 통합 명세 테스트.

SPEC-PDF-003 Phase 2: GUI ProgressBar 실시간 업데이트
- AC-05: GUI ProgressBar determinate mode 전환
- AC-05: 100ms 간격 업데이트
- AC-05: 실행 중 진행값 정확성
"""

import pytest

# ============================================================================
# AC-05: ProgressState determinate mode 테스트
# ============================================================================


class TestProgressStateDeterminate:
    """ProgressState의 determinate mode 전환을 검증한다."""

    def test_start_determinate로_determinate_모드를_시작한다(self):
        """start_determinate 메서드로 determinate 모드를 시작한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=100, message="처리 중...")
        assert state.is_running is True
        assert state.mode == "determinate"
        assert state.total == 100
        assert state.current == 0

    def test_update_progress로_진행률을_갱신한다(self):
        """update_progress 메서드로 현재 진행률을 갱신한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=100)
        state.update_progress(current=50, total=100)
        assert state.current == 50
        assert state.total == 100

    def test_fraction은_진행_비율을_반환한다(self):
        """fraction 속성은 0.0~1.0 범위의 진행 비율을 반환한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=100)
        state.update_progress(current=25, total=100)
        assert state.fraction == pytest.approx(0.25)

    def test_fraction은_total_0일_때_0을_반환한다(self):
        """total이 0이면 fraction은 0.0을 반환한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=0)
        assert state.fraction == 0.0

    def test_기존_start는_indeterminate_모드를_유지한다(self):
        """기존 start 메서드는 indeterminate 모드를 유지한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start("처리 중...")
        assert state.mode == "indeterminate"
        assert state.is_running is True

    def test_stop은_모든_상태를_초기화한다(self):
        """stop은 모드에 관계없이 상태를 초기화한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=100)
        state.update_progress(current=50, total=100)
        state.stop()
        assert state.is_running is False
        assert state.current == 0
        assert state.total == 0

    def test_reset은_모드를_indeterminate로_초기화한다(self):
        """reset은 모드를 indeterminate로 초기화한다."""
        from pdf_tool.gui.widgets.progress_bar import ProgressState

        state = ProgressState()
        state.start_determinate(total=100)
        state.reset()
        assert state.mode == "indeterminate"
        assert state.current == 0
        assert state.total == 0


# ============================================================================
# AC-05: ProgressBarWidget determinate mode 테스트
# ============================================================================


class TestProgressBarWidgetDeterminate:
    """ProgressBarWidget의 determinate mode를 검증한다.

    NOTE: GUI 위젯 테스트는 customtkinter가 필요하므로
    ProgressState 로직만 단위 테스트한다.
    """

    def test_ProgressBarWidget에_start_determinate가_있다(self):
        """ProgressBarWidget에 start_determinate 메서드가 정의되어 있다."""
        from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget

        assert hasattr(ProgressBarWidget, "start_determinate")

    def test_ProgressBarWidget에_update_progress가_있다(self):
        """ProgressBarWidget에 update_progress 메서드가 정의되어 있다."""
        from pdf_tool.gui.widgets.progress_bar_widget import ProgressBarWidget

        assert hasattr(ProgressBarWidget, "update_progress")


# ============================================================================
# AC-05: BasePageWidget 콜백 전달 테스트
# ============================================================================


class TestBasePageWidgetCallback:
    """BasePageWidget이 execute_command에 콜백을 전달함을 검증한다."""

    def test_execute_command_시그니처에_callback이_있다(self):
        """execute_command에 callback 파라미터가 있다."""
        import inspect

        from pdf_tool.gui.pages.base_page_widget import BasePageWidget

        sig = inspect.signature(BasePageWidget.execute_command)
        params = list(sig.parameters.keys())
        assert "callback" in params

    def test_make_gui_callback이_정의되어_있다(self):
        """_make_gui_callback 메서드가 BasePageWidget에 정의되어 있다."""
        from pdf_tool.gui.pages.base_page_widget import BasePageWidget

        assert hasattr(BasePageWidget, "_make_gui_callback")
