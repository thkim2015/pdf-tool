"""프로그레스 바 위젯 모듈.

비결정적(indeterminate) 모드의 진행률 표시를 관리한다.
"""

from __future__ import annotations


class ProgressState:
    """프로그레스 바의 상태를 관리하는 클래스.

    GUI 위젯과 분리된 순수 상태 관리 로직이다.
    """

    def __init__(self) -> None:
        self.is_running: bool = False
        self.message: str = ""

    def start(self, message: str = "") -> None:
        """진행률 표시를 시작한다.

        Args:
            message: 표시할 상태 메시지
        """
        self.is_running = True
        self.message = message

    def stop(self) -> None:
        """진행률 표시를 정지한다."""
        self.is_running = False

    def reset(self) -> None:
        """초기 상태로 리셋한다."""
        self.is_running = False
        self.message = ""
