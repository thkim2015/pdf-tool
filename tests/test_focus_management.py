"""Task 5.3: 포커스 관리 시스템 테스트.

포커스 링 스타일, 초기 포커스 설정, 페이지 전환 시 포커스를 검증한다.
"""

from __future__ import annotations

from unittest.mock import MagicMock


class Test_포커스_링_스타일:
    """포커스 링의 시각적 스타일을 검증한다."""

    def test_포커스_링_색상_Apple_Blue(self):
        """포커스 링 색상이 Apple Blue (#007AFF)이다."""
        from pdf_tool.gui.accessibility import FOCUS_RING_COLOR

        assert FOCUS_RING_COLOR == "#007AFF"

    def test_포커스_링_두께_3pt(self):
        """포커스 링 두께가 3pt이다."""
        from pdf_tool.gui.accessibility import FOCUS_RING_THICKNESS

        assert FOCUS_RING_THICKNESS == 3

    def test_포커스_링_오프셋_3px(self):
        """포커스 링 오프셋이 3px이다."""
        from pdf_tool.gui.accessibility import FOCUS_RING_OFFSET

        assert FOCUS_RING_OFFSET == 3

    def test_포커스_링_스타일_딕셔너리(self):
        """get_focus_ring_style()이 올바른 스타일 딕셔너리를 반환한다."""
        from pdf_tool.gui.accessibility import get_focus_ring_style

        style = get_focus_ring_style()
        assert style["color"] == "#007AFF"
        assert style["thickness"] == 3
        assert style["offset"] == 3


class Test_초기_포커스:
    """앱 시작 시 및 페이지 전환 시 초기 포커스를 검증한다."""

    def test_초기_포커스_페이지_이름_반환(self):
        """get_initial_focus_page()가 첫 페이지 이름을 반환한다."""
        from pdf_tool.gui.accessibility import get_initial_focus_page

        assert get_initial_focus_page() == "Cut"

    def test_포커스_가능_위젯_우선순위(self):
        """포커스 가능 위젯 우선순위가 정의되어 있다."""
        from pdf_tool.gui.accessibility import FOCUSABLE_WIDGET_PRIORITY

        # 입력 필드가 버튼보다 우선
        assert "entry" in FOCUSABLE_WIDGET_PRIORITY
        assert "button" in FOCUSABLE_WIDGET_PRIORITY
        entry_idx = FOCUSABLE_WIDGET_PRIORITY.index("entry")
        button_idx = FOCUSABLE_WIDGET_PRIORITY.index("button")
        assert entry_idx < button_idx


class Test_포커스_트래핑:
    """모달 대화상자의 포커스 트래핑을 검증한다 (미래 확장)."""

    def test_포커스_트랩_활성화(self):
        """FocusTrap을 활성화하면 trapped=True 상태가 된다."""
        from pdf_tool.gui.accessibility import FocusTrap

        trap = FocusTrap()
        trap.activate([MagicMock(), MagicMock()])

        assert trap.is_active is True

    def test_포커스_트랩_비활성화(self):
        """FocusTrap을 비활성화하면 trapped=False 상태가 된다."""
        from pdf_tool.gui.accessibility import FocusTrap

        trap = FocusTrap()
        trap.activate([MagicMock()])
        trap.deactivate()

        assert trap.is_active is False

    def test_포커스_트랩_내부_순환(self):
        """트랩 활성화 시 트랩된 위젯 내에서만 순환한다."""
        from pdf_tool.gui.accessibility import FocusTrap

        trap = FocusTrap()
        w1 = MagicMock()
        w2 = MagicMock()
        trap.activate([w1, w2])
        trap.current_index = 1

        # 마지막에서 다음으로 가면 첫 번째로
        next_w = trap.next()
        assert next_w is w1

    def test_포커스_트랩_빈_리스트_비활성(self):
        """빈 리스트로 활성화하면 비활성 상태를 유지한다."""
        from pdf_tool.gui.accessibility import FocusTrap

        trap = FocusTrap()
        trap.activate([])

        assert trap.is_active is False
