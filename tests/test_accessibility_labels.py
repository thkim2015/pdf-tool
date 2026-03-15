"""Task 5.2: 접근성 레이블 테스트.

모든 인터랙티브 요소에 접근성 레이블이 존재하는지 검증한다.
상태 변경 알림 콜백 시스템을 검증한다.
"""

from __future__ import annotations

from unittest.mock import MagicMock


class Test_접근성_레이블_레지스트리:
    """AccessibilityLabelRegistry의 레이블 관리를 검증한다."""

    def test_레이블_등록(self):
        """위젯에 접근성 레이블을 등록할 수 있다."""
        from pdf_tool.gui.accessibility import AccessibilityLabelRegistry

        registry = AccessibilityLabelRegistry()
        widget = MagicMock()
        registry.register(widget, "파일 선택 버튼")

        assert registry.get_label(widget) == "파일 선택 버튼"

    def test_레이블_미등록_시_None(self):
        """미등록 위젯의 레이블은 None이다."""
        from pdf_tool.gui.accessibility import AccessibilityLabelRegistry

        registry = AccessibilityLabelRegistry()
        widget = MagicMock()

        assert registry.get_label(widget) is None

    def test_레이블_업데이트(self):
        """등록된 레이블을 업데이트할 수 있다."""
        from pdf_tool.gui.accessibility import AccessibilityLabelRegistry

        registry = AccessibilityLabelRegistry()
        widget = MagicMock()
        registry.register(widget, "이전 레이블")
        registry.register(widget, "새 레이블")

        assert registry.get_label(widget) == "새 레이블"

    def test_모든_레이블_조회(self):
        """등록된 모든 위젯-레이블 쌍을 조회할 수 있다."""
        from pdf_tool.gui.accessibility import AccessibilityLabelRegistry

        registry = AccessibilityLabelRegistry()
        w1 = MagicMock()
        w2 = MagicMock()
        registry.register(w1, "버튼 1")
        registry.register(w2, "버튼 2")

        all_labels = registry.get_all()
        assert len(all_labels) == 2

    def test_레이블_해제(self):
        """위젯의 접근성 레이블을 해제할 수 있다."""
        from pdf_tool.gui.accessibility import AccessibilityLabelRegistry

        registry = AccessibilityLabelRegistry()
        widget = MagicMock()
        registry.register(widget, "레이블")
        registry.unregister(widget)

        assert registry.get_label(widget) is None


class Test_상태_변경_알림:
    """StatusAnnouncer의 상태 변경 알림을 검증한다."""

    def test_상태_알림_콜백_등록(self):
        """상태 변경 알림 콜백을 등록할 수 있다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        callback = MagicMock()
        announcer.register_callback(callback)

        assert callback in announcer.callbacks

    def test_파일_로드_알림(self):
        """파일 로드 완료 시 알림이 발생한다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        callback = MagicMock()
        announcer.register_callback(callback)

        announcer.announce("파일 로드됨")
        callback.assert_called_once_with("파일 로드됨")

    def test_작업_시작_알림(self):
        """작업 시작 시 알림이 발생한다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        callback = MagicMock()
        announcer.register_callback(callback)

        announcer.announce("작업 시작")
        callback.assert_called_once_with("작업 시작")

    def test_작업_완료_알림(self):
        """작업 완료 시 알림이 발생한다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        callback = MagicMock()
        announcer.register_callback(callback)

        announcer.announce("작업 완료")
        callback.assert_called_once_with("작업 완료")

    def test_복수_콜백_호출(self):
        """여러 콜백이 등록되어 있으면 모두 호출된다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        cb1 = MagicMock()
        cb2 = MagicMock()
        announcer.register_callback(cb1)
        announcer.register_callback(cb2)

        announcer.announce("알림 메시지")
        cb1.assert_called_once_with("알림 메시지")
        cb2.assert_called_once_with("알림 메시지")

    def test_콜백_해제(self):
        """콜백을 해제하면 더 이상 호출되지 않는다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        callback = MagicMock()
        announcer.register_callback(callback)
        announcer.unregister_callback(callback)

        announcer.announce("알림")
        callback.assert_not_called()

    def test_콜백_예외_시_다른_콜백_계속_실행(self):
        """하나의 콜백이 예외를 발생시켜도 다른 콜백은 실행된다."""
        from pdf_tool.gui.accessibility import StatusAnnouncer

        announcer = StatusAnnouncer()
        failing_cb = MagicMock(side_effect=RuntimeError("fail"))
        normal_cb = MagicMock()
        announcer.register_callback(failing_cb)
        announcer.register_callback(normal_cb)

        announcer.announce("알림")
        normal_cb.assert_called_once_with("알림")
