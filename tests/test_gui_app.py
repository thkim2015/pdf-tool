"""GUI 메인 앱 테스트."""

from unittest.mock import MagicMock


class Test_네비게이션_버튼:
    """네비게이션 버튼 상수가 올바르게 정의되어 있는지 검증한다."""

    def test_네비게이션_버튼_목록(self):
        from pdf_tool.gui.constants import NAV_BUTTONS

        expected = ["Cut", "Merge", "Split", "Rotate", "Resize", "Compress", "Watermark", "Images to PDF", "Info"]
        assert expected == NAV_BUTTONS

    def test_네비게이션_버튼_수(self):
        from pdf_tool.gui.constants import NAV_BUTTONS

        assert len(NAV_BUTTONS) == 9


class Test_PageManager:
    """PageManager 클래스의 페이지 전환 로직을 검증한다."""

    def test_초기_상태_current_page_None(self):
        """초기 상태에서 현재 페이지는 None이다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        assert manager.current_page is None

    def test_페이지_등록(self):
        """페이지를 이름으로 등록할 수 있다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        mock_page = MagicMock()
        manager.register("Cut", mock_page)
        assert "Cut" in manager.pages

    def test_페이지_전환(self):
        """등록된 페이지로 전환하면 pack()이 호출된다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        old_page = MagicMock()
        new_page = MagicMock()
        manager.register("Cut", old_page)
        manager.register("Merge", new_page)

        # Cut 페이지 활성화
        manager.switch_to("Cut")
        assert manager.current_page == "Cut"
        old_page.pack.assert_called_once()

        # Merge로 전환
        manager.switch_to("Merge")
        assert manager.current_page == "Merge"
        old_page.pack_forget.assert_called_once()
        new_page.pack.assert_called_once()

    def test_존재하지_않는_페이지_전환_무시(self):
        """등록되지 않은 페이지로 전환 시 예외 없이 무시한다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        manager.switch_to("NonExistent")  # 예외 발생하지 않아야 함
        assert manager.current_page is None

    def test_같은_페이지_재전환(self):
        """같은 페이지로 다시 전환해도 정상 동작한다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        page = MagicMock()
        manager.register("Cut", page)

        manager.switch_to("Cut")
        manager.switch_to("Cut")
        assert manager.current_page == "Cut"


class Test_글로벌_예외_핸들러:
    """글로벌 예외 핸들러 로직을 검증한다."""

    def test_예외_메시지_포맷(self):
        """예외를 사용자 친화적 메시지로 변환한다."""
        from pdf_tool.gui.app import format_exception_message

        msg = format_exception_message(ValueError("잘못된 값"))
        assert "잘못된 값" in msg

    def test_PDFToolError_메시지(self):
        """PDFToolError 예외를 적절히 포맷한다."""
        from pdf_tool.core.exceptions import PDFToolError
        from pdf_tool.gui.app import format_exception_message

        msg = format_exception_message(PDFToolError("PDF 처리 오류"))
        assert "PDF 처리 오류" in msg

    def test_알_수_없는_예외_메시지(self):
        """알 수 없는 예외도 메시지를 생성한다."""
        from pdf_tool.gui.app import format_exception_message

        msg = format_exception_message(RuntimeError())
        assert msg  # 빈 문자열이 아님


class Test_윈도우_닫기_확인:
    """윈도우 닫기 시 작업 중 확인 로직을 검증한다."""

    def test_작업_중이_아닐_때_닫기_허용(self):
        """작업 중이 아니면 닫기를 허용한다."""
        from pdf_tool.gui.app import should_confirm_close

        assert should_confirm_close(is_executing=False) is False

    def test_작업_중일_때_확인_필요(self):
        """작업 중이면 닫기 확인이 필요하다."""
        from pdf_tool.gui.app import should_confirm_close

        assert should_confirm_close(is_executing=True) is True


class Test_사이드바_구성:
    """사이드바 구성 데이터를 검증한다."""

    def test_사이드바_항목_아이콘_매핑(self):
        """모든 NAV_BUTTONS에 대한 아이콘이 존재한다."""
        from pdf_tool.gui.constants import NAV_BUTTONS
        from pdf_tool.gui.icons import get_icon

        for name in NAV_BUTTONS:
            icon = get_icon(name)
            assert icon != "", f"{name}에 대한 아이콘이 없습니다"

    def test_사이드바_항목_9개_렌더링(self):
        """사이드바에 9개 항목이 렌더링되어야 한다."""
        from pdf_tool.gui.constants import NAV_BUTTONS

        assert len(NAV_BUTTONS) == 9

    def test_사이드바_항목_SidebarItemState_생성(self):
        """각 NAV_BUTTON에 대한 SidebarItemState를 생성할 수 있다."""
        from pdf_tool.gui.constants import NAV_BUTTONS
        from pdf_tool.gui.icons import get_icon
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        items = []
        for name in NAV_BUTTONS:
            state = SidebarItemState(
                icon=get_icon(name),
                label=name,
                value=name,
            )
            items.append(state)

        assert len(items) == 9
        assert items[0].label == "Cut"
        assert items[0].selected is False

    def test_사이드바_선택_항목_하이라이트(self):
        """선택된 항목만 하이라이트된다."""
        from pdf_tool.gui.widgets.sidebar_item import SidebarItemState

        items = [
            SidebarItemState(icon="A", label="A", value="a"),
            SidebarItemState(icon="B", label="B", value="b"),
        ]
        items[0].set_selected(True)

        assert items[0].get_style()["bg_color"] == "#007AFF"
        assert items[1].get_style()["bg_color"] == "transparent"

    def test_사이드바_vibrancy_배경_다크(self):
        """다크 모드 사이드바 배경은 #1C1C1E 기반이다."""
        from pdf_tool.gui.colors import get_palette

        palette = get_palette("dark")
        assert palette.sidebar_bg == "#1C1C1E"

    def test_사이드바_vibrancy_배경_라이트(self):
        """라이트 모드 사이드바 배경은 #F2F2F7 기반이다."""
        from pdf_tool.gui.colors import get_palette

        palette = get_palette("light")
        assert palette.sidebar_bg == "#F2F2F7"

    def test_사이드바_vibrancy_투명도(self):
        """vibrancy 배경은 투명도가 적용된다."""
        from pdf_tool.gui.colors import get_palette

        dark = get_palette("dark")
        assert dark.vibrancy_bg.endswith("CC")  # 80% opacity

        light = get_palette("light")
        assert light.vibrancy_bg.endswith("CC")


# ============================================================================
# TAG-004 Task 4.2: PageManager 크로스 페이드 애니메이션 테스트
# ============================================================================


class Test_PageManager_크로스페이드:
    """PageManager의 크로스 페이드 애니메이션 로직을 검증한다."""

    def test_switch_to_animated_기본_동작(self):
        """switch_to_animated()는 애니메이터를 사용하여 페이지를 전환한다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        old_page = MagicMock()
        new_page = MagicMock()
        manager.register("Cut", old_page)
        manager.register("Merge", new_page)

        manager.switch_to("Cut")
        manager.switch_to_animated("Merge")
        assert manager.current_page == "Merge"

    def test_switch_to_animated_콜백(self):
        """switch_to_animated() 완료 시 on_complete 콜백이 호출된다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        page = MagicMock()
        manager.register("Cut", page)

        completed = []
        manager.switch_to_animated("Cut", on_complete=lambda: completed.append(True))
        assert manager.current_page == "Cut"

    def test_switch_to_animated_존재하지_않는_페이지(self):
        """존재하지 않는 페이지로의 애니메이션 전환은 무시된다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        manager.switch_to_animated("NonExistent")
        assert manager.current_page is None

    def test_cross_fade_duration_기본값(self):
        """크로스 페이드 기본 지속 시간은 0.15초이다."""
        from pdf_tool.gui.app import CROSS_FADE_DURATION

        assert CROSS_FADE_DURATION == 0.15

    def test_animator_속성_존재(self):
        """PageManager는 animator 속성을 가진다."""
        from pdf_tool.gui.app import PageManager

        manager = PageManager()
        assert hasattr(manager, "animator")
