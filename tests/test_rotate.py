"""rotate 명령어의 명세 테스트."""

from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_tool.commands.rotate import rotate_pdf
from pdf_tool.core.exceptions import PageRangeError, PDFToolError


class TestRotatePdf:
    """PDF 페이지 회전 기능을 검증한다."""

    def test_전체_페이지를_90도_회전한다(self, five_page_pdf: Path, tmp_path: Path):
        """모든 페이지를 시계 방향 90도 회전한다."""
        output = tmp_path / "rotated.pdf"
        rotate_pdf(five_page_pdf, angle=90, output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 5
        # 회전된 페이지는 /Rotate 속성이 90이어야 한다
        for page in reader.pages:
            rotation = page.get("/Rotate", 0)
            assert rotation == 90

    def test_전체_페이지를_180도_회전한다(self, five_page_pdf: Path, tmp_path: Path):
        """모든 페이지를 180도 회전한다."""
        output = tmp_path / "rotated.pdf"
        rotate_pdf(five_page_pdf, angle=180, output=output)

        reader = PdfReader(output)
        for page in reader.pages:
            rotation = page.get("/Rotate", 0)
            assert rotation == 180

    def test_특정_페이지만_회전한다(self, five_page_pdf: Path, tmp_path: Path):
        """2, 4페이지만 180도 회전하고 나머지는 원본 유지한다."""
        output = tmp_path / "rotated.pdf"
        rotate_pdf(five_page_pdf, angle=180, pages="2,4", output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 5
        # 2, 4페이지(0-indexed: 1, 3)만 회전
        for i, page in enumerate(reader.pages):
            rotation = page.get("/Rotate", 0)
            if i in (1, 3):
                assert rotation == 180, f"페이지 {i + 1}이 회전되지 않았다"
            else:
                assert rotation == 0, f"페이지 {i + 1}이 잘못 회전되었다"

    def test_잘못된_각도에_에러를_발생시킨다(self, five_page_pdf: Path, tmp_path: Path):
        """45도 같은 지원하지 않는 각도에 에러를 발생시킨다."""
        output = tmp_path / "rotated.pdf"
        with pytest.raises(PDFToolError, match="지원되지 않는 각도"):
            rotate_pdf(five_page_pdf, angle=45, output=output)

    def test_270도_회전을_지원한다(self, five_page_pdf: Path, tmp_path: Path):
        """270도 회전을 지원한다."""
        output = tmp_path / "rotated.pdf"
        rotate_pdf(five_page_pdf, angle=270, output=output)

        reader = PdfReader(output)
        for page in reader.pages:
            rotation = page.get("/Rotate", 0)
            assert rotation == 270

    def test_출력_경로_미지정시_자동_생성한다(self, five_page_pdf: Path):
        """output이 None이면 입력 파일명 기반으로 자동 생성한다."""
        result_path = rotate_pdf(five_page_pdf, angle=90, output=None)

        expected = five_page_pdf.parent / "five_rotated.pdf"
        assert result_path == expected
        assert expected.exists()

    def test_페이지_범위_초과시_에러를_발생시킨다(
        self, small_pdf: Path, tmp_path: Path
    ):
        """회전 대상 페이지가 총 페이지를 초과하면 에러를 발생시킨다."""
        output = tmp_path / "rotated.pdf"
        with pytest.raises(PageRangeError):
            rotate_pdf(small_pdf, angle=90, pages="5", output=output)
