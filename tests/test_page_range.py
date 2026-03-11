"""page_range 모듈의 명세 테스트."""

import pytest

from pdf_tool.core.exceptions import PageRangeError
from pdf_tool.core.page_range import parse_page_range


class TestParsePageRange:
    """페이지 범위 파싱 기능을 검증한다."""

    def test_단일_페이지를_파싱한다(self):
        """단일 페이지 번호를 파싱한다."""
        result = parse_page_range("3", max_pages=10)
        assert result == [2]  # 0-indexed

    def test_쉼표로_구분된_개별_페이지를_파싱한다(self):
        """쉼표로 구분된 여러 페이지를 파싱한다."""
        result = parse_page_range("1,3,5", max_pages=10)
        assert result == [0, 2, 4]

    def test_연속_범위를_파싱한다(self):
        """하이픈으로 표시된 연속 범위를 파싱한다."""
        result = parse_page_range("3-7", max_pages=10)
        assert result == [2, 3, 4, 5, 6]

    def test_복합_범위를_파싱한다(self):
        """개별 페이지와 연속 범위가 혼합된 형식을 파싱한다."""
        result = parse_page_range("1,3,5-7", max_pages=10)
        assert result == [0, 2, 4, 5, 6]

    def test_중복_페이지를_제거하고_정렬한다(self):
        """중복된 페이지 번호를 제거하고 오름차순 정렬한다."""
        result = parse_page_range("3,1,3,5", max_pages=10)
        assert result == [0, 2, 4]

    def test_최대_페이지_초과시_에러를_발생시킨다(self):
        """페이지 번호가 최대 페이지 수를 초과하면 PageRangeError를 발생시킨다."""
        with pytest.raises(PageRangeError, match="페이지 범위 초과"):
            parse_page_range("3-10", max_pages=5)

    def test_0_이하의_페이지_번호에_에러를_발생시킨다(self):
        """0 이하의 페이지 번호는 유효하지 않다."""
        with pytest.raises(PageRangeError, match="유효하지 않은 페이지"):
            parse_page_range("0", max_pages=10)

    def test_빈_문자열에_에러를_발생시킨다(self):
        """빈 문자열은 유효하지 않다."""
        with pytest.raises(PageRangeError):
            parse_page_range("", max_pages=10)

    def test_잘못된_형식에_에러를_발생시킨다(self):
        """알 수 없는 형식의 문자열은 에러를 발생시킨다."""
        with pytest.raises(PageRangeError):
            parse_page_range("abc", max_pages=10)

    def test_역순_범위에_에러를_발생시킨다(self):
        """시작이 끝보다 큰 범위는 에러를 발생시킨다."""
        with pytest.raises(PageRangeError, match="유효하지 않은 범위"):
            parse_page_range("7-3", max_pages=10)

    def test_공백이_포함된_입력을_처리한다(self):
        """공백이 포함되어도 올바르게 파싱한다."""
        result = parse_page_range(" 1 , 3 , 5-7 ", max_pages=10)
        assert result == [0, 2, 4, 5, 6]
