"""Animation Engine 테스트.

TAG-004 Task 4.1: Easing, Animation, Animator 클래스를 검증한다.
순수 Python 로직만 테스트 (CustomTkinter 의존성 없음).
"""

from __future__ import annotations

import pytest

# ============================================================================
# 1. Easing 함수 테스트
# ============================================================================


class Test_Easing_함수:
    """Easing 함수들이 올바른 보간 값을 반환하는지 검증한다."""

    def test_linear_시작(self):
        """linear(0) == 0."""
        from pdf_tool.gui.animation import Easing

        assert Easing.linear(0.0) == 0.0

    def test_linear_끝(self):
        """linear(1) == 1."""
        from pdf_tool.gui.animation import Easing

        assert Easing.linear(1.0) == 1.0

    def test_linear_중간(self):
        """linear(0.5) == 0.5."""
        from pdf_tool.gui.animation import Easing

        assert Easing.linear(0.5) == 0.5

    def test_ease_in_시작(self):
        """ease_in(0) == 0."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in(0.0) == 0.0

    def test_ease_in_끝(self):
        """ease_in(1) == 1."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in(1.0) == 1.0

    def test_ease_in_중간(self):
        """ease_in(0.5) == 0.25 (t^2)."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in(0.5) == pytest.approx(0.25)

    def test_ease_out_시작(self):
        """ease_out(0) == 0."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_out(0.0) == 0.0

    def test_ease_out_끝(self):
        """ease_out(1) == 1."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_out(1.0) == 1.0

    def test_ease_out_중간(self):
        """ease_out(0.5) == 0.75 (1 - (1-t)^2)."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_out(0.5) == pytest.approx(0.75)

    def test_ease_in_out_시작(self):
        """ease_in_out(0) == 0."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in_out(0.0) == 0.0

    def test_ease_in_out_끝(self):
        """ease_in_out(1) == 1."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in_out(1.0) == 1.0

    def test_ease_in_out_중간(self):
        """ease_in_out(0.5) == 0.5 (3t^2 - 2t^3)."""
        from pdf_tool.gui.animation import Easing

        assert Easing.ease_in_out(0.5) == pytest.approx(0.5)

    def test_ease_in_out_사분의일(self):
        """ease_in_out(0.25) = 3*(0.0625) - 2*(0.015625) = 0.15625."""
        from pdf_tool.gui.animation import Easing

        expected = 3 * 0.25**2 - 2 * 0.25**3
        assert Easing.ease_in_out(0.25) == pytest.approx(expected)

    def test_t_클램핑_음수(self):
        """t < 0 이면 0으로 클램핑된다."""
        from pdf_tool.gui.animation import Easing

        assert Easing.linear(-0.5) == 0.0
        assert Easing.ease_in(-1.0) == 0.0

    def test_t_클램핑_초과(self):
        """t > 1 이면 1로 클램핑된다."""
        from pdf_tool.gui.animation import Easing

        assert Easing.linear(1.5) == 1.0
        assert Easing.ease_out(2.0) == 1.0


# ============================================================================
# 2. Animation 클래스 테스트
# ============================================================================


class Test_Animation_클래스:
    """Animation 클래스의 상태 관리와 값 보간을 검증한다."""

    def test_초기_상태(self):
        """Animation 생성 직후 상태는 idle이다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=0.3,
            easing_func=Easing.linear,
        )
        assert anim.is_complete is False
        assert anim.current_value == 0.0

    def test_update_중간값(self):
        """경과 시간에 따라 보간된 중간값을 반환한다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=0.0,
            end_value=100.0,
            duration=1.0,
            easing_func=Easing.linear,
        )
        anim.update(0.5)
        assert anim.current_value == pytest.approx(50.0)

    def test_update_완료(self):
        """duration 이상 경과 시 end_value에 도달하고 완료된다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=0.3,
            easing_func=Easing.linear,
        )
        anim.update(0.5)
        assert anim.is_complete is True
        assert anim.current_value == pytest.approx(1.0)

    def test_update_누적(self):
        """여러 번 update 호출 시 시간이 누적된다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=0.0,
            end_value=100.0,
            duration=1.0,
            easing_func=Easing.linear,
        )
        anim.update(0.3)
        assert anim.current_value == pytest.approx(30.0)
        anim.update(0.3)
        assert anim.current_value == pytest.approx(60.0)

    def test_on_complete_콜백(self):
        """완료 시 on_complete 콜백이 호출된다."""
        from pdf_tool.gui.animation import Animation, Easing

        completed = []
        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=0.1,
            easing_func=Easing.linear,
            on_complete=lambda: completed.append(True),
        )
        anim.update(0.2)
        assert len(completed) == 1

    def test_on_complete_한번만_호출(self):
        """on_complete 콜백은 한 번만 호출된다."""
        from pdf_tool.gui.animation import Animation, Easing

        call_count = []
        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=0.1,
            easing_func=Easing.linear,
            on_complete=lambda: call_count.append(1),
        )
        anim.update(0.2)
        anim.update(0.1)  # 이미 완료됨
        assert len(call_count) == 1

    def test_on_update_콜백(self):
        """매 update 마다 on_update 콜백이 호출된다."""
        from pdf_tool.gui.animation import Animation, Easing

        values = []
        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=1.0,
            easing_func=Easing.linear,
            on_update=lambda v: values.append(v),
        )
        anim.update(0.5)
        assert len(values) == 1
        assert values[0] == pytest.approx(0.5)

    def test_ease_in_보간(self):
        """ease_in 함수 사용 시 가속 곡선이 적용된다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=0.0,
            end_value=100.0,
            duration=1.0,
            easing_func=Easing.ease_in,
        )
        anim.update(0.5)
        # ease_in(0.5) = 0.25, value = 0 + 0.25 * 100 = 25
        assert anim.current_value == pytest.approx(25.0)

    def test_역방향_애니메이션(self):
        """start > end인 역방향 애니메이션도 동작한다."""
        from pdf_tool.gui.animation import Animation, Easing

        anim = Animation(
            start_value=1.0,
            end_value=0.0,
            duration=1.0,
            easing_func=Easing.linear,
        )
        anim.update(0.5)
        assert anim.current_value == pytest.approx(0.5)

    def test_animation_id_고유(self):
        """각 Animation은 고유한 id를 가진다."""
        from pdf_tool.gui.animation import Animation, Easing

        a1 = Animation(0, 1, 0.3, Easing.linear)
        a2 = Animation(0, 1, 0.3, Easing.linear)
        assert a1.animation_id != a2.animation_id

    def test_duration_0_즉시_완료(self):
        """duration이 0이면 즉시 완료된다."""
        from pdf_tool.gui.animation import Animation, Easing

        completed = []
        anim = Animation(
            start_value=0.0,
            end_value=1.0,
            duration=0.0,
            easing_func=Easing.linear,
            on_complete=lambda: completed.append(True),
        )
        anim.update(0.0)
        assert anim.is_complete is True
        assert anim.current_value == pytest.approx(1.0)
        assert len(completed) == 1


# ============================================================================
# 3. Animator 매니저 테스트
# ============================================================================


class Test_Animator_매니저:
    """Animator 싱글톤 매니저의 애니메이션 관리 로직을 검증한다."""

    def test_add_animation(self):
        """애니메이션을 추가할 수 있다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        anim = Animation(0, 1, 0.3, Easing.linear)
        animator.add_animation(anim)
        assert animator.is_animating() is True

    def test_remove_animation(self):
        """애니메이션을 제거할 수 있다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        anim = Animation(0, 1, 0.3, Easing.linear)
        animator.add_animation(anim)
        animator.remove_animation(anim.animation_id)
        assert animator.is_animating() is False

    def test_update_진행(self):
        """update(delta_time)으로 모든 애니메이션을 진행시킨다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        values = []
        anim = Animation(
            0.0, 1.0, 1.0, Easing.linear,
            on_update=lambda v: values.append(v),
        )
        animator.add_animation(anim)
        animator.update(0.5)
        assert len(values) == 1
        assert values[0] == pytest.approx(0.5)

    def test_완료된_애니메이션_자동_정리(self):
        """완료된 애니메이션은 자동으로 제거된다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        anim = Animation(0, 1, 0.1, Easing.linear)
        animator.add_animation(anim)
        animator.update(0.2)
        assert animator.is_animating() is False

    def test_is_animating_비어있을_때(self):
        """애니메이션이 없으면 is_animating()은 False이다."""
        from pdf_tool.gui.animation import Animator

        animator = Animator()
        assert animator.is_animating() is False

    def test_여러_애니메이션_동시_진행(self):
        """여러 애니메이션이 동시에 진행된다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        v1, v2 = [], []
        a1 = Animation(0, 100, 1.0, Easing.linear, on_update=lambda v: v1.append(v))
        a2 = Animation(0, 200, 1.0, Easing.linear, on_update=lambda v: v2.append(v))
        animator.add_animation(a1)
        animator.add_animation(a2)
        animator.update(0.5)
        assert v1[-1] == pytest.approx(50.0)
        assert v2[-1] == pytest.approx(100.0)

    def test_중복_add_방지(self):
        """같은 animation_id를 다시 추가하면 무시된다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        anim = Animation(0, 1, 0.3, Easing.linear)
        animator.add_animation(anim)
        animator.add_animation(anim)  # 중복
        assert animator.animation_count == 1

    def test_존재하지_않는_id_제거_무시(self):
        """존재하지 않는 animation_id 제거 시 예외 없이 무시된다."""
        from pdf_tool.gui.animation import Animator

        animator = Animator()
        animator.remove_animation("nonexistent")  # 예외 발생하지 않아야 함

    def test_clear_all(self):
        """clear_all()로 모든 애니메이션을 제거할 수 있다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        for _ in range(5):
            animator.add_animation(Animation(0, 1, 1.0, Easing.linear))
        animator.clear_all()
        assert animator.is_animating() is False
        assert animator.animation_count == 0


# ============================================================================
# 4. Opacity 애니메이션 헬퍼 테스트
# ============================================================================


class Test_opacity_animate:
    """opacity_animate() 헬퍼 함수를 검증한다."""

    def test_fade_in(self):
        """fade in 애니메이션은 0 -> 1 범위이다."""
        from pdf_tool.gui.animation import opacity_animate

        values = []
        anim = opacity_animate(
            start=0.0,
            end=1.0,
            duration=0.15,
            on_update=lambda v: values.append(v),
        )
        assert anim.start_value == 0.0
        assert anim.end_value == 1.0

    def test_fade_out(self):
        """fade out 애니메이션은 1 -> 0 범위이다."""
        from pdf_tool.gui.animation import opacity_animate

        anim = opacity_animate(start=1.0, end=0.0, duration=0.15)
        assert anim.start_value == 1.0
        assert anim.end_value == 0.0

    def test_범위_클램핑(self):
        """opacity 값은 0.0 ~ 1.0 범위로 클램핑된다."""
        from pdf_tool.gui.animation import opacity_animate

        anim = opacity_animate(start=-0.5, end=1.5, duration=0.15)
        assert anim.start_value == 0.0
        assert anim.end_value == 1.0

    def test_기본_easing은_ease_in_out(self):
        """기본 easing 함수는 ease_in_out이다."""
        from pdf_tool.gui.animation import opacity_animate

        anim = opacity_animate(start=0.0, end=1.0, duration=0.15)
        # 중간값 확인으로 easing 적용 검증
        anim.update(0.075)  # 절반 시점
        # ease_in_out(0.5) = 0.5 -> value = 0 + 0.5 * 1.0 = 0.5
        assert anim.current_value == pytest.approx(0.5)

    def test_on_complete_콜백_전달(self):
        """on_complete 콜백이 애니메이션 완료 시 호출된다."""
        from pdf_tool.gui.animation import opacity_animate

        completed = []
        anim = opacity_animate(
            start=0.0,
            end=1.0,
            duration=0.1,
            on_complete=lambda: completed.append(True),
        )
        anim.update(0.2)
        assert len(completed) == 1


# ============================================================================
# 5. 메모리 누수 방지 테스트
# ============================================================================


class Test_메모리_누수_방지:
    """애니메이션 완료 후 리소스가 올바르게 정리되는지 검증한다."""

    def test_완료_후_애니메이션_목록에서_제거(self):
        """완료된 애니메이션은 Animator에서 자동 제거된다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        anim = Animation(0, 1, 0.1, Easing.linear)
        animator.add_animation(anim)
        animator.update(0.2)
        assert animator.animation_count == 0

    def test_콜백_참조_해제(self):
        """완료된 애니메이션의 콜백 참조가 해제된다."""
        from pdf_tool.gui.animation import Animation, Easing

        callback_called = []
        anim = Animation(
            0, 1, 0.1, Easing.linear,
            on_complete=lambda: callback_called.append(True),
            on_update=lambda v: None,
        )
        anim.update(0.2)
        assert anim._on_complete is None
        assert anim._on_update is None

    def test_대량_애니메이션_생성_정리(self):
        """100개 애니메이션 생성 후 모두 완료되면 전부 정리된다."""
        from pdf_tool.gui.animation import Animation, Animator, Easing

        animator = Animator()
        for _i in range(100):
            animator.add_animation(Animation(0, 1, 0.05, Easing.linear))
        assert animator.animation_count == 100
        animator.update(0.1)
        assert animator.animation_count == 0
