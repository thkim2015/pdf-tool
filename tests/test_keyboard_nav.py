"""Task 5.1: 키보드 네비게이션 테스트.

Tab/Shift-Tab 순환, Cmd/Ctrl+1~9 페이지 전환,
Enter/Space 버튼 활성화, Escape 대화상자 닫기를 검증한다.
"""

from __future__ import annotations

from unittest.mock import MagicMock

# ============================================================================
# 순수 로직 테스트 (GUI 불필요)
# ============================================================================


class Test_포커스_순서_관리:
    """FocusManager의 포커스 순서 관리 로직을 검증한다."""

    def test_포커스_순서_등록(self):
        """위젯을 포커스 순서에 등록할 수 있다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        widget = MagicMock()
        manager.register(widget)

        assert widget in manager.focus_order

    def test_포커스_순서_복수_등록(self):
        """여러 위젯을 순서대로 등록할 수 있다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        w1 = MagicMock()
        w2 = MagicMock()
        w3 = MagicMock()
        manager.register(w1)
        manager.register(w2)
        manager.register(w3)

        assert manager.focus_order == [w1, w2, w3]

    def test_포커스_다음_이동(self):
        """focus_next()로 다음 위젯으로 이동한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        w1 = MagicMock()
        w2 = MagicMock()
        manager.register(w1)
        manager.register(w2)
        manager.current_index = 0

        next_widget = manager.focus_next()
        assert next_widget is w2
        assert manager.current_index == 1

    def test_포커스_순환_마지막에서_첫_요소로(self):
        """마지막 요소에서 focus_next()하면 첫 요소로 순환한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        w1 = MagicMock()
        w2 = MagicMock()
        manager.register(w1)
        manager.register(w2)
        manager.current_index = 1

        next_widget = manager.focus_next()
        assert next_widget is w1
        assert manager.current_index == 0

    def test_포커스_이전_이동(self):
        """focus_prev()로 이전 위젯으로 이동한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        w1 = MagicMock()
        w2 = MagicMock()
        manager.register(w1)
        manager.register(w2)
        manager.current_index = 1

        prev_widget = manager.focus_prev()
        assert prev_widget is w1
        assert manager.current_index == 0

    def test_포커스_역순환_첫_요소에서_마지막으로(self):
        """첫 요소에서 focus_prev()하면 마지막 요소로 순환한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        w1 = MagicMock()
        w2 = MagicMock()
        w3 = MagicMock()
        manager.register(w1)
        manager.register(w2)
        manager.register(w3)
        manager.current_index = 0

        prev_widget = manager.focus_prev()
        assert prev_widget is w3
        assert manager.current_index == 2

    def test_빈_포커스_매니저_focus_next_None(self):
        """위젯이 없을 때 focus_next()는 None을 반환한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        assert manager.focus_next() is None

    def test_빈_포커스_매니저_focus_prev_None(self):
        """위젯이 없을 때 focus_prev()는 None을 반환한다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        assert manager.focus_prev() is None

    def test_포커스_순서_초기화(self):
        """clear()로 포커스 순서를 초기화할 수 있다."""
        from pdf_tool.gui.accessibility import FocusManager

        manager = FocusManager()
        manager.register(MagicMock())
        manager.clear()

        assert manager.focus_order == []
        assert manager.current_index == -1


class Test_키보드_단축키_매핑:
    """플랫폼별 키보드 단축키 매핑을 검증한다."""

    def test_macos_페이지_전환_키(self):
        """macOS에서 Command+1~9 키 매핑이 올바르다."""
        from pdf_tool.gui.accessibility import get_page_shortcut_keys

        keys = get_page_shortcut_keys("darwin")
        assert keys[1] == "<Command-Key-1>"
        assert keys[9] == "<Command-Key-9>"

    def test_windows_페이지_전환_키(self):
        """Windows에서 Ctrl+1~9 키 매핑이 올바르다."""
        from pdf_tool.gui.accessibility import get_page_shortcut_keys

        keys = get_page_shortcut_keys("win32")
        assert keys[1] == "<Control-Key-1>"
        assert keys[9] == "<Control-Key-9>"

    def test_linux_페이지_전환_키(self):
        """Linux에서 Ctrl+1~9 키 매핑이 올바르다."""
        from pdf_tool.gui.accessibility import get_page_shortcut_keys

        keys = get_page_shortcut_keys("linux")
        assert keys[1] == "<Control-Key-1>"
        assert keys[9] == "<Control-Key-9>"

    def test_페이지_전환_키_9개(self):
        """페이지 전환 키가 9개(1~9)이다."""
        from pdf_tool.gui.accessibility import get_page_shortcut_keys

        keys = get_page_shortcut_keys("darwin")
        assert len(keys) == 9

    def test_페이지_인덱스와_NAV_BUTTONS_매핑(self):
        """Cmd+N이 NAV_BUTTONS[N-1]에 매핑된다."""
        from pdf_tool.gui.accessibility import get_page_for_shortcut

        assert get_page_for_shortcut(1) == "Cut"
        assert get_page_for_shortcut(2) == "Merge"
        assert get_page_for_shortcut(9) == "Info"

    def test_범위_밖_인덱스_None(self):
        """0이나 10 등 범위 밖 인덱스는 None을 반환한다."""
        from pdf_tool.gui.accessibility import get_page_for_shortcut

        assert get_page_for_shortcut(0) is None
        assert get_page_for_shortcut(10) is None


class Test_Tab_네비게이션_키_이벤트:
    """Tab/Shift-Tab 키 이벤트 처리를 검증한다."""

    def test_tab_키_이벤트_이름(self):
        """Tab 키 이벤트 이름이 올바르다."""
        from pdf_tool.gui.accessibility import SHIFT_TAB_KEY, TAB_KEY

        assert TAB_KEY == "<Tab>"
        assert SHIFT_TAB_KEY == "<Shift-Tab>"

    def test_enter_space_키_이벤트_이름(self):
        """Enter/Space 키 이벤트 이름이 올바르다."""
        from pdf_tool.gui.accessibility import ENTER_KEY, SPACE_KEY

        assert ENTER_KEY == "<Return>"
        assert SPACE_KEY == "<space>"

    def test_escape_키_이벤트_이름(self):
        """Escape 키 이벤트 이름이 올바르다."""
        from pdf_tool.gui.accessibility import ESCAPE_KEY

        assert ESCAPE_KEY == "<Escape>"
