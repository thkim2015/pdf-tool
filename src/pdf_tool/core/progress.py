"""진행 상황 콜백 프레임워크.

# @MX:NOTE: SPEC-PDF-003 Phase 1 - ProgressCallback 타입 및 안전 호출 래퍼
# @MX:SPEC: SPEC-PDF-003

대용량 PDF 처리 시 진행 상황을 추적하기 위한 콜백 타입과
예외 안전 호출 래퍼를 제공한다.
"""

from collections.abc import Callable

# ProgressCallback 타입: (current_page, total_pages) -> None
# None이면 진행 상황을 추적하지 않는다.
ProgressCallback = Callable[[int, int], None] | None


def safe_callback(
    callback: ProgressCallback,
    current: int,
    total: int,
) -> None:
    """콜백을 예외 안전하게 호출한다.

    Args:
        callback: 진행 상황 콜백 (None이면 무시)
        current: 현재 처리된 항목 수
        total: 전체 항목 수

    Note:
        콜백이 예외를 발생시켜도 전파하지 않는다.
        단, KeyboardInterrupt는 전파한다.
    """
    if callback is None:
        return
    try:
        callback(current, total)
    except KeyboardInterrupt:
        raise
    except Exception:
        # 콜백 예외는 삼킨다 (R6: 콜백 예외 안전성)
        pass
