"""페이지 범위 입력 위젯 모듈.

"1-3, 5, 8-10" 형식의 페이지 범위 입력을 지원한다.
"""

from __future__ import annotations

import re


def validate_page_range_input(value: str) -> bool:
    """페이지 범위 입력 문자열의 형식을 검증한다.

    빈 문자열은 선택적 입력으로 유효하게 처리한다.
    숫자, 쉼표, 하이픈, 공백만 허용하며,
    각 부분이 유효한 숫자 또는 범위인지 확인한다.

    Args:
        value: 페이지 범위 문자열

    Returns:
        유효한 형식이면 True
    """
    stripped = value.strip()
    if not stripped:
        return True

    # 허용 문자 검증: 숫자, 쉼표, 하이픈, 공백만 허용
    if not re.match(r"^[\d,\-\s]+$", stripped):
        return False

    # 각 부분을 파싱하여 유효성 검증
    for part in stripped.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            segments = part.split("-")
            # 하이픈이 2개 이상이면 유효하지 않음
            if len(segments) != 2:
                return False
            try:
                start = int(segments[0].strip())
                end = int(segments[1].strip())
                if start <= 0 or end <= 0 or start > end:
                    return False
            except ValueError:
                return False
        else:
            try:
                num = int(part)
                if num <= 0:
                    return False
            except ValueError:
                return False

    return True
