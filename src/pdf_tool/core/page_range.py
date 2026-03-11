"""페이지 범위 파서: "1,3,5-10" 형식의 문자열을 0-indexed 페이지 목록으로 변환한다."""

from pdf_tool.core.exceptions import PageRangeError


def parse_page_range(page_range_str: str, *, max_pages: int) -> list[int]:
    """페이지 범위 문자열을 0-indexed 페이지 번호 리스트로 변환한다.

    Args:
        page_range_str: "1,3,5-10" 형식의 페이지 범위 문자열 (1-indexed)
        max_pages: PDF의 총 페이지 수

    Returns:
        0-indexed 페이지 번호 리스트 (정렬, 중복 제거)

    Raises:
        PageRangeError: 유효하지 않은 페이지 범위일 때
    """
    stripped = page_range_str.strip()
    if not stripped:
        raise PageRangeError("페이지 범위가 비어 있습니다")

    pages: set[int] = set()

    for part in stripped.split(","):
        part = part.strip()
        if not part:
            continue

        if "-" in part:
            # 범위 형식: "3-7"
            segments = part.split("-", maxsplit=1)
            try:
                start = int(segments[0].strip())
                end = int(segments[1].strip())
            except ValueError as exc:
                raise PageRangeError(
                    f"유효하지 않은 페이지 범위 형식입니다: '{part}'"
                ) from exc

            if start > end:
                raise PageRangeError(
                    f"유효하지 않은 범위: 시작({start})이 끝({end})보다 큽니다"
                )

            _validate_page_number(start, max_pages)
            _validate_page_number(end, max_pages)

            for page in range(start, end + 1):
                pages.add(page - 1)  # 0-indexed 변환
        else:
            # 단일 페이지: "3"
            try:
                page_num = int(part)
            except ValueError as exc:
                raise PageRangeError(
                    f"유효하지 않은 페이지 번호입니다: '{part}'"
                ) from exc

            _validate_page_number(page_num, max_pages)
            pages.add(page_num - 1)  # 0-indexed 변환

    if not pages:
        raise PageRangeError("파싱된 페이지가 없습니다")

    return sorted(pages)


def _validate_page_number(page: int, max_pages: int) -> None:
    """페이지 번호가 유효한 범위 내에 있는지 검증한다."""
    if page <= 0:
        raise PageRangeError(f"유효하지 않은 페이지 번호: {page} (1 이상이어야 합니다)")
    if page > max_pages:
        raise PageRangeError(
            f"페이지 범위 초과: {page} (최대 페이지는 {max_pages}입니다)"
        )
