"""세그먼티드 컨트롤 위젯 모듈.

macOS 스타일 캡슐형 세그먼티드 컨트롤의 상태 관리 로직이다.
"""

from __future__ import annotations

from collections.abc import Callable


class SegmentedControlState:
    """세그먼티드 컨트롤의 상태를 관리하는 클래스.

    GUI 위젯과 분리된 순수 상태 관리 로직이다.
    """

    def __init__(
        self,
        values: list[str],
        on_change: Callable[[str], None] | None = None,
    ) -> None:
        """세그먼티드 컨트롤 상태를 초기화한다.

        Args:
            values: 세그먼트 값 목록
            on_change: 값 변경 시 호출될 콜백

        Raises:
            ValueError: values가 비어있을 때
        """
        if not values:
            msg = "values는 비어있을 수 없습니다"
            raise ValueError(msg)

        self.values: list[str] = values
        self._selected: str = values[0]
        self._on_change: Callable[[str], None] | None = on_change

    def get_value(self) -> str:
        """현재 선택된 값을 반환한다."""
        return self._selected

    def set_value(self, value: str) -> None:
        """선택 값을 변경한다.

        values에 없는 값은 무시된다.
        같은 값을 다시 선택하면 콜백이 호출되지 않는다.

        Args:
            value: 선택할 값
        """
        if value not in self.values:
            return
        if value == self._selected:
            return
        self._selected = value
        if self._on_change is not None:
            self._on_change(value)

    def get_selected_index(self) -> int:
        """선택된 값의 인덱스를 반환한다."""
        return self.values.index(self._selected)

    def get_container_style(self) -> dict:
        """컨테이너의 스타일을 반환한다.

        Returns:
            corner_radius, bg_color 키를 포함하는 딕셔너리
        """
        return {
            "corner_radius": 8,
            "bg_color": "#007AFF33",  # accent 20% opacity
        }

    def get_indicator_style(self) -> dict:
        """선택 인디케이터의 스타일을 반환한다.

        Returns:
            bg_color, corner_radius, animation_duration 키를 포함하는 딕셔너리
        """
        return {
            "bg_color": "#FFFFFF",
            "corner_radius": 6,
            "animation_duration": 0.2,
        }

    def get_segment_style(self, value: str) -> dict:
        """세그먼트의 스타일을 반환한다.

        Args:
            value: 세그먼트 값

        Returns:
            selected, text_color 키를 포함하는 딕셔너리
        """
        is_selected = value == self._selected
        return {
            "selected": is_selected,
            "text_color": "#000000" if is_selected else "#666666",
        }
