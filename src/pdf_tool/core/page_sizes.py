"""용지 크기 상수: 표준 용지 규격과 mm-to-points 변환 기능을 제공한다."""

# 1인치 = 72포인트 = 25.4mm
_MM_TO_POINT_FACTOR = 72.0 / 25.4


def mm_to_points(mm: float) -> float:
    """밀리미터를 PDF 포인트 단위로 변환한다.

    Args:
        mm: 밀리미터 값

    Returns:
        포인트 단위 값 (1포인트 = 1/72인치)
    """
    return mm * _MM_TO_POINT_FACTOR


# 표준 용지 크기 정의 (너비, 높이) - 단위: 포인트
PAPER_SIZES: dict[str, tuple[float, float]] = {
    "A3": (mm_to_points(297), mm_to_points(420)),
    "A4": (mm_to_points(210), mm_to_points(297)),
    "A5": (mm_to_points(148), mm_to_points(210)),
    "Letter": (mm_to_points(216), mm_to_points(279)),
    "Legal": (mm_to_points(216), mm_to_points(356)),
}


def get_paper_size(name: str) -> tuple[float, float] | None:
    """용지 크기 이름으로 (너비, 높이) 포인트 값을 반환한다.

    대소문자를 구분하지 않는다.

    Args:
        name: 용지 크기 이름 (예: "A4", "letter")

    Returns:
        (너비, 높이) 포인트 튜플 또는 None
    """
    # 대소문자 무시 검색
    for key, value in PAPER_SIZES.items():
        if key.lower() == name.lower():
            return value
    return None


def get_supported_sizes() -> list[str]:
    """지원되는 용지 크기 이름 목록을 반환한다.

    Returns:
        용지 크기 이름 리스트
    """
    return list(PAPER_SIZES.keys())
