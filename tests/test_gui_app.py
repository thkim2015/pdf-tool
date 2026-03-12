"""GUI 메인 앱 테스트."""

from unittest.mock import MagicMock


class Test_네비게이션_버튼:
    """네비게이션 버튼 상수가 올바르게 정의되어 있는지 검증한다."""

    def test_네비게이션_버튼_목록(self):
        from pdf_tool.gui.app import NAV_BUTTONS

        expected = ["Cut", "Merge", "Split", "Rotate", "Resize", "Compress", "Watermark", "Info"]
        assert expected == NAV_BUTTONS

    def test_네비게이션_버튼_수(self):
        from pdf_tool.gui.app import NAV_BUTTONS

        assert len(NAV_BUTTONS) == 8


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
