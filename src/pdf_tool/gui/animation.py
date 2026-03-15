"""애니메이션 엔진 모듈.

TAG-004: 순수 Python 기반 애니메이션 시스템이다.
CustomTkinter 의존성 없이 Easing, Animation, Animator를 제공한다.
tkinter after()로 실제 GUI 루프와 통합된다.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable


def _clamp(value: float, min_val: float, max_val: float) -> float:
    """값을 min_val ~ max_val 범위로 클램핑한다."""
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value


class Easing:
    """이징 함수 모음.

    모든 함수는 t를 0.0~1.0으로 클램핑한 후 보간 값을 반환한다.
    """

    @staticmethod
    def linear(t: float) -> float:
        """선형 보간: f(t) = t."""
        t = _clamp(t, 0.0, 1.0)
        return t

    @staticmethod
    def ease_in(t: float) -> float:
        """가속 보간: f(t) = t^2."""
        t = _clamp(t, 0.0, 1.0)
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """감속 보간: f(t) = 1 - (1-t)^2."""
        t = _clamp(t, 0.0, 1.0)
        return 1.0 - (1.0 - t) ** 2

    @staticmethod
    def ease_in_out(t: float) -> float:
        """가감속 보간: f(t) = 3t^2 - 2t^3 (cubic smoothstep)."""
        t = _clamp(t, 0.0, 1.0)
        return 3.0 * t * t - 2.0 * t * t * t


class Animation:
    """단일 애니메이션 인스턴스.

    start_value에서 end_value로 duration 동안 easing_func에 따라 보간한다.

    Attributes:
        animation_id: 고유 식별자
        start_value: 시작 값
        end_value: 종료 값
        duration: 지속 시간 (초)
        current_value: 현재 보간된 값
        is_complete: 완료 여부
    """

    def __init__(
        self,
        start_value: float,
        end_value: float,
        duration: float,
        easing_func: Callable[[float], float],
        on_complete: Callable[[], None] | None = None,
        on_update: Callable[[float], None] | None = None,
    ) -> None:
        self.animation_id: str = str(uuid.uuid4())
        self.start_value: float = start_value
        self.end_value: float = end_value
        self.duration: float = max(duration, 0.0)
        self._easing_func: Callable[[float], float] = easing_func
        self._on_complete: Callable[[], None] | None = on_complete
        self._on_update: Callable[[float], None] | None = on_update
        self._elapsed: float = 0.0
        self.current_value: float = start_value
        self.is_complete: bool = False

    def update(self, delta_time: float) -> None:
        """경과 시간을 반영하여 현재 값을 갱신한다.

        Args:
            delta_time: 이전 프레임 이후 경과 시간 (초)
        """
        if self.is_complete:
            return

        self._elapsed += delta_time

        progress = 1.0 if self.duration <= 0.0 else min(self._elapsed / self.duration, 1.0)

        eased = self._easing_func(progress)
        self.current_value = self.start_value + (self.end_value - self.start_value) * eased

        if self._on_update is not None:
            self._on_update(self.current_value)

        if progress >= 1.0:
            self.is_complete = True
            self.current_value = self.end_value
            if self._on_complete is not None:
                self._on_complete()
            # 메모리 누수 방지: 콜백 참조 해제
            self._on_complete = None
            self._on_update = None


class Animator:
    """애니메이션 매니저.

    여러 Animation을 동시에 관리하고 update()로 일괄 진행시킨다.
    tkinter after()와 연동하여 GUI 메인 루프에서 사용한다.
    """

    def __init__(self) -> None:
        self._animations: dict[str, Animation] = {}

    @property
    def animation_count(self) -> int:
        """현재 관리 중인 애니메이션 수를 반환한다."""
        return len(self._animations)

    def add_animation(self, animation: Animation) -> None:
        """애니메이션을 추가한다. 같은 id는 무시된다.

        Args:
            animation: 추가할 Animation 인스턴스
        """
        if animation.animation_id in self._animations:
            return
        self._animations[animation.animation_id] = animation

    def remove_animation(self, animation_id: str) -> None:
        """애니메이션을 제거한다. 존재하지 않는 id는 무시된다.

        Args:
            animation_id: 제거할 애니메이션 식별자
        """
        self._animations.pop(animation_id, None)

    def update(self, delta_time: float) -> None:
        """모든 애니메이션을 delta_time만큼 진행시킨다.

        완료된 애니메이션은 자동으로 제거된다.

        Args:
            delta_time: 이전 프레임 이후 경과 시간 (초)
        """
        completed_ids: list[str] = []

        for anim_id, anim in self._animations.items():
            anim.update(delta_time)
            if anim.is_complete:
                completed_ids.append(anim_id)

        for anim_id in completed_ids:
            self._animations.pop(anim_id, None)

    def is_animating(self) -> bool:
        """현재 진행 중인 애니메이션이 있는지 반환한다."""
        return len(self._animations) > 0

    def clear_all(self) -> None:
        """모든 애니메이션을 즉시 제거한다."""
        self._animations.clear()


def opacity_animate(
    start: float,
    end: float,
    duration: float,
    easing_func: Callable[[float], float] | None = None,
    on_update: Callable[[float], None] | None = None,
    on_complete: Callable[[], None] | None = None,
) -> Animation:
    """Opacity 전용 애니메이션을 생성한다.

    start/end는 0.0 ~ 1.0 범위로 클램핑된다.

    Args:
        start: 시작 opacity (0.0 ~ 1.0)
        end: 종료 opacity (0.0 ~ 1.0)
        duration: 지속 시간 (초)
        easing_func: 이징 함수 (기본: ease_in_out)
        on_update: 값 갱신 콜백
        on_complete: 완료 콜백

    Returns:
        생성된 Animation 인스턴스
    """
    clamped_start = _clamp(start, 0.0, 1.0)
    clamped_end = _clamp(end, 0.0, 1.0)
    if easing_func is None:
        easing_func = Easing.ease_in_out

    return Animation(
        start_value=clamped_start,
        end_value=clamped_end,
        duration=duration,
        easing_func=easing_func,
        on_update=on_update,
        on_complete=on_complete,
    )
