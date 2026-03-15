"""프로그레스 바 위젯 모듈.

비결정적(indeterminate) 모드의 진행률 표시를 관리한다.
"""

from __future__ import annotations


class ProgressState:
    """프로그레스 바의 상태를 관리하는 클래스.

    GUI 위젯과 분리된 순수 상태 관리 로직이다.
    indeterminate 모드와 determinate 모드를 지원한다.
    """

    def __init__(self) -> None:
        self.is_running: bool = False
        self.message: str = ""
        self.mode: str = "indeterminate"
        self.current: int = 0
        self.total: int = 0

    def start(self, message: str = "") -> None:
        """indeterminate 모드로 진행률 표시를 시작한다.

        Args:
            message: 표시할 상태 메시지
        """
        self.is_running = True
        self.message = message
        self.mode = "indeterminate"

    def start_determinate(self, total: int, message: str = "") -> None:
        """determinate 모드로 진행률 표시를 시작한다.

        Args:
            total: 전체 항목 수
            message: 표시할 상태 메시지
        """
        self.is_running = True
        self.message = message
        self.mode = "determinate"
        self.total = total
        self.current = 0

    def update_progress(self, current: int, total: int) -> None:
        """determinate 모드에서 진행률을 갱신한다.

        Args:
            current: 현재 처리된 항목 수
            total: 전체 항목 수
        """
        self.current = current
        self.total = total

    @property
    def fraction(self) -> float:
        """0.0~1.0 범위의 진행 비율을 반환한다."""
        if self.total <= 0:
            return 0.0
        return min(self.current / self.total, 1.0)

    def stop(self) -> None:
        """진행률 표시를 정지한다."""
        self.is_running = False
        self.current = 0
        self.total = 0

    def reset(self) -> None:
        """초기 상태로 리셋한다."""
        self.is_running = False
        self.message = ""
        self.mode = "indeterminate"
        self.current = 0
        self.total = 0
