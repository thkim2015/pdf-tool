"""ETA 계산 모듈.

# @MX:NOTE: SPEC-PDF-003 Phase 2 - 작업 시간 추정 및 ETA 계산
# @MX:SPEC: SPEC-PDF-003

작업 시간 추정, 동적 ETA 계산, 포맷팅 기능을 제공한다.
"""

from __future__ import annotations

import time

# 작업별 페이지당 추정 처리 시간 (초/페이지)
_OPERATION_BENCHMARKS: dict[str, float] = {
    "cut": 0.02,
    "merge": 0.03,
    "split": 0.02,
    "rotate": 0.03,
    "resize": 0.05,
    "compress": 0.10,
    "watermark": 0.08,
    "info": 0.01,
}

# 기본 페이지당 처리 시간 (알 수 없는 작업용)
_DEFAULT_PER_PAGE = 0.05

# 파일 크기 보정 계수 (바이트 기준, MB당 추가 시간)
_SIZE_FACTOR_PER_MB = 0.01

# progress 표시 threshold (초)
PROGRESS_THRESHOLD_SECONDS = 2.0


def estimate_operation_time(
    page_count: int,
    operation: str,
    file_size_bytes: int = 0,
) -> float:
    """작업 예상 소요 시간을 추정한다.

    Args:
        page_count: 처리할 페이지 수
        operation: 작업 유형 (cut, merge, split, rotate 등)
        file_size_bytes: 파일 크기 (바이트). 0이면 무시한다.

    Returns:
        추정 소요 시간 (초)
    """
    per_page = _OPERATION_BENCHMARKS.get(operation, _DEFAULT_PER_PAGE)
    base_time = page_count * per_page

    # 파일 크기 보정
    if file_size_bytes > 0:
        size_mb = file_size_bytes / (1024 * 1024)
        base_time += size_mb * _SIZE_FACTOR_PER_MB

    return max(base_time, 0.001)


def should_show_progress(estimated_seconds: float) -> bool:
    """progress 표시 여부를 결정한다.

    Args:
        estimated_seconds: 추정 소요 시간 (초)

    Returns:
        2초 이상이면 True
    """
    return estimated_seconds >= PROGRESS_THRESHOLD_SECONDS


class ETACalculator:
    """동적 ETA 계산기.

    현재 진행률과 경과 시간을 기반으로 남은 시간을 동적으로 추정한다.
    """

    def __init__(self, total: int) -> None:
        """ETACalculator를 초기화한다.

        Args:
            total: 전체 항목 수
        """
        self.total = total
        self.current = 0
        self._start_time = time.monotonic()

    def update(self, current: int) -> None:
        """현재 진행률을 갱신한다.

        Args:
            current: 현재 처리된 항목 수
        """
        self.current = current

    @property
    def elapsed_seconds(self) -> float:
        """시작 이후 경과 시간을 반환한다."""
        return time.monotonic() - self._start_time

    @property
    def remaining_seconds(self) -> float | None:
        """남은 시간을 추정한다.

        Returns:
            남은 시간 (초). 진행률이 0이면 None.
        """
        if self.current <= 0:
            return None

        elapsed = self.elapsed_seconds
        rate = self.current / elapsed  # 항목/초
        remaining_items = self.total - self.current
        return max(remaining_items / rate, 0.0)

    @property
    def percentage(self) -> float:
        """진행 백분율을 반환한다.

        Returns:
            0.0 ~ 100.0 범위의 백분율
        """
        if self.total <= 0:
            return 0.0
        return min(self.current / self.total * 100.0, 100.0)


def format_eta(seconds: float | None) -> str:
    """남은 시간을 사람이 읽기 쉬운 포맷으로 변환한다.

    Args:
        seconds: 남은 시간 (초). None이면 빈 문자열.

    Returns:
        "ETA 2m 30s" 형식의 문자열
    """
    if seconds is None:
        return ""

    total_seconds = int(seconds)
    minutes = total_seconds // 60
    secs = total_seconds % 60

    if minutes > 0:
        return f"ETA {minutes}m {secs}s"
    return f"ETA {secs}s"
