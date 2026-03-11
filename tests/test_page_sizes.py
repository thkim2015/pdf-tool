"""page_sizes 모듈 테스트: 용지 크기 상수 및 mm-to-points 변환을 검증한다."""

import pytest

from pdf_tool.core.page_sizes import (
    PAPER_SIZES,
    get_paper_size,
    get_supported_sizes,
    mm_to_points,
)


class TestMmToPoints:
    """mm -> points 변환 함수 테스트."""

    def test_0mm는_0포인트를_반환한다(self) -> None:
        assert mm_to_points(0) == 0

    def test_25_4mm는_72포인트를_반환한다(self) -> None:
        # 1인치 = 25.4mm = 72포인트
        assert mm_to_points(25.4) == pytest.approx(72.0, abs=0.01)

    def test_210mm를_정확히_변환한다(self) -> None:
        # A4 너비: 210mm -> 약 595.28포인트
        result = mm_to_points(210)
        assert result == pytest.approx(595.28, abs=0.1)

    def test_297mm를_정확히_변환한다(self) -> None:
        # A4 높이: 297mm -> 약 841.89포인트
        result = mm_to_points(297)
        assert result == pytest.approx(841.89, abs=0.1)


class TestPaperSizes:
    """용지 크기 상수 테스트."""

    def test_A4_크기가_정의되어_있다(self) -> None:
        assert "A4" in PAPER_SIZES
        width, height = PAPER_SIZES["A4"]
        assert width == pytest.approx(mm_to_points(210), abs=0.1)
        assert height == pytest.approx(mm_to_points(297), abs=0.1)

    def test_A3_크기가_정의되어_있다(self) -> None:
        assert "A3" in PAPER_SIZES
        width, height = PAPER_SIZES["A3"]
        assert width == pytest.approx(mm_to_points(297), abs=0.1)
        assert height == pytest.approx(mm_to_points(420), abs=0.1)

    def test_A5_크기가_정의되어_있다(self) -> None:
        assert "A5" in PAPER_SIZES
        width, height = PAPER_SIZES["A5"]
        assert width == pytest.approx(mm_to_points(148), abs=0.1)
        assert height == pytest.approx(mm_to_points(210), abs=0.1)

    def test_Letter_크기가_정의되어_있다(self) -> None:
        assert "Letter" in PAPER_SIZES
        width, height = PAPER_SIZES["Letter"]
        assert width == pytest.approx(mm_to_points(216), abs=0.1)
        assert height == pytest.approx(mm_to_points(279), abs=0.1)

    def test_Legal_크기가_정의되어_있다(self) -> None:
        assert "Legal" in PAPER_SIZES
        width, height = PAPER_SIZES["Legal"]
        assert width == pytest.approx(mm_to_points(216), abs=0.1)
        assert height == pytest.approx(mm_to_points(356), abs=0.1)

    def test_5개_표준_크기가_모두_정의되어_있다(self) -> None:
        expected = {"A3", "A4", "A5", "Letter", "Legal"}
        assert set(PAPER_SIZES.keys()) == expected


class TestGetPaperSize:
    """get_paper_size 함수 테스트."""

    def test_대소문자_구분없이_A4를_찾는다(self) -> None:
        result = get_paper_size("a4")
        assert result is not None
        assert result == PAPER_SIZES["A4"]

    def test_대소문자_구분없이_Letter를_찾는다(self) -> None:
        result = get_paper_size("letter")
        assert result is not None

    def test_존재하지_않는_크기는_None을_반환한다(self) -> None:
        result = get_paper_size("B7")
        assert result is None


class TestGetSupportedSizes:
    """get_supported_sizes 함수 테스트."""

    def test_지원_크기_목록을_반환한다(self) -> None:
        sizes = get_supported_sizes()
        assert "A3" in sizes
        assert "A4" in sizes
        assert "A5" in sizes
        assert "Letter" in sizes
        assert "Legal" in sizes
