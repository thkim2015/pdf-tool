"""ETA 계산 모듈 명세 테스트.

SPEC-PDF-003 Phase 2: ETA 계산 및 작업 시간 추정
- AC-06: 2초 이상 작업만 progress 표시
- AC-08: ETA 계산 및 포맷
"""

import time

import pytest


# ============================================================================
# AC-08: ETA 초기 추정 테스트
# ============================================================================


class TestEstimateOperationTime:
    """작업 시간 추정 함수를 검증한다."""

    def test_estimate_operation_time이_정의되어_있다(self):
        """estimate_operation_time 함수가 core.eta에 정의되어 있다."""
        from pdf_tool.core.eta import estimate_operation_time

        assert callable(estimate_operation_time)

    def test_페이지_수가_많으면_추정_시간이_길다(self):
        """페이지 수가 많을수록 추정 시간이 증가한다."""
        from pdf_tool.core.eta import estimate_operation_time

        time_10 = estimate_operation_time(page_count=10, operation="cut")
        time_100 = estimate_operation_time(page_count=100, operation="cut")
        assert time_100 > time_10

    def test_파일_크기가_크면_추정_시간이_길다(self):
        """파일 크기가 클수록 추정 시간이 증가한다."""
        from pdf_tool.core.eta import estimate_operation_time

        time_small = estimate_operation_time(
            page_count=10, operation="compress", file_size_bytes=1_000_000
        )
        time_large = estimate_operation_time(
            page_count=10, operation="compress", file_size_bytes=100_000_000
        )
        assert time_large > time_small

    def test_지원하지_않는_operation도_기본값을_반환한다(self):
        """알 수 없는 operation에 대해서도 기본 추정값을 반환한다."""
        from pdf_tool.core.eta import estimate_operation_time

        result = estimate_operation_time(page_count=10, operation="unknown")
        assert result > 0

    def test_반환값은_초_단위_float이다(self):
        """반환값은 초 단위의 float이다."""
        from pdf_tool.core.eta import estimate_operation_time

        result = estimate_operation_time(page_count=10, operation="rotate")
        assert isinstance(result, float)
        assert result > 0


# ============================================================================
# AC-06: 2초 threshold 테스트
# ============================================================================


class TestShouldShowProgress:
    """2초 threshold 기반 progress 표시 여부를 검증한다."""

    def test_should_show_progress가_정의되어_있다(self):
        """should_show_progress 함수가 core.eta에 정의되어 있다."""
        from pdf_tool.core.eta import should_show_progress

        assert callable(should_show_progress)

    def test_2초_이상이면_True(self):
        """추정 시간이 2초 이상이면 progress를 표시한다."""
        from pdf_tool.core.eta import should_show_progress

        assert should_show_progress(estimated_seconds=2.0) is True
        assert should_show_progress(estimated_seconds=5.0) is True

    def test_2초_미만이면_False(self):
        """추정 시간이 2초 미만이면 progress를 표시하지 않는다."""
        from pdf_tool.core.eta import should_show_progress

        assert should_show_progress(estimated_seconds=0.5) is False
        assert should_show_progress(estimated_seconds=1.9) is False


# ============================================================================
# AC-08: 동적 ETA 조정 테스트
# ============================================================================


class TestETACalculator:
    """동적 ETA 계산기를 검증한다."""

    def test_ETACalculator가_정의되어_있다(self):
        """ETACalculator 클래스가 core.eta에 정의되어 있다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        assert calc is not None

    def test_update로_진행률을_갱신한다(self):
        """update 메서드로 현재 진행률을 갱신한다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        calc.update(current=10)
        assert calc.current == 10

    def test_elapsed_seconds는_경과_시간을_반환한다(self):
        """elapsed_seconds는 시작 이후 경과 시간을 반환한다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        time.sleep(0.05)
        assert calc.elapsed_seconds >= 0.04

    def test_remaining_seconds는_남은_시간을_추정한다(self):
        """remaining_seconds는 남은 시간을 추정한다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        time.sleep(0.05)
        calc.update(current=50)
        remaining = calc.remaining_seconds
        # 50% 완료했으므로 남은 시간은 경과 시간과 비슷해야 한다
        assert remaining is not None
        assert remaining >= 0

    def test_진행률_0일_때_remaining은_None(self):
        """진행률이 0이면 남은 시간을 추정할 수 없다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        assert calc.remaining_seconds is None

    def test_percentage는_진행_백분율을_반환한다(self):
        """percentage는 진행 백분율을 반환한다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        calc.update(current=25)
        assert calc.percentage == 25.0

    def test_percentage는_100을_초과하지_않는다(self):
        """percentage는 100%를 초과하지 않는다."""
        from pdf_tool.core.eta import ETACalculator

        calc = ETACalculator(total=100)
        calc.update(current=150)
        assert calc.percentage == 100.0


# ============================================================================
# AC-08: ETA 포맷 테스트
# ============================================================================


class TestFormatETA:
    """ETA 포맷 함수를 검증한다."""

    def test_format_eta가_정의되어_있다(self):
        """format_eta 함수가 core.eta에 정의되어 있다."""
        from pdf_tool.core.eta import format_eta

        assert callable(format_eta)

    def test_초_단위_포맷(self):
        """60초 미만이면 초 단위로 포맷한다."""
        from pdf_tool.core.eta import format_eta

        assert format_eta(30.0) == "ETA 30s"
        assert format_eta(5.5) == "ETA 5s"

    def test_분_초_단위_포맷(self):
        """60초 이상이면 분:초 단위로 포맷한다."""
        from pdf_tool.core.eta import format_eta

        assert format_eta(150.0) == "ETA 2m 30s"
        assert format_eta(90.0) == "ETA 1m 30s"

    def test_None이면_빈_문자열(self):
        """None이면 빈 문자열을 반환한다."""
        from pdf_tool.core.eta import format_eta

        assert format_eta(None) == ""

    def test_0이면_완료_표시(self):
        """0이면 완료 표시를 반환한다."""
        from pdf_tool.core.eta import format_eta

        assert format_eta(0.0) == "ETA 0s"
