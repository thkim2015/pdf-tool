"""cut 명령어의 명세 테스트."""

from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_tool.commands.cut import cut_pdf
from pdf_tool.core.exceptions import FileValidationError, PageRangeError


class TestCutPdf:
    """PDF 페이지 추출 기능을 검증한다."""

    def test_연속_페이지_범위를_추출한다(self, sample_pdf: Path, tmp_path: Path):
        """연속 범위(3-7)에서 5페이지를 추출한다."""
        output = tmp_path / "result.pdf"
        cut_pdf(sample_pdf, pages="3-7", output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_복합_페이지_범위를_추출한다(self, sample_pdf: Path, tmp_path: Path):
        """복합 범위(1,3,5-7)에서 5페이지를 추출한다."""
        output = tmp_path / "result.pdf"
        cut_pdf(sample_pdf, pages="1,3,5-7", output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 5

    def test_단일_페이지를_추출한다(self, sample_pdf: Path, tmp_path: Path):
        """단일 페이지(1)를 추출한다."""
        output = tmp_path / "result.pdf"
        cut_pdf(sample_pdf, pages="1", output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_원본_파일을_수정하지_않는다(self, sample_pdf: Path, tmp_path: Path):
        """추출 후 원본 PDF의 페이지 수가 변경되지 않는다."""
        original_reader = PdfReader(sample_pdf)
        original_count = len(original_reader.pages)

        output = tmp_path / "result.pdf"
        cut_pdf(sample_pdf, pages="1-3", output=output)

        after_reader = PdfReader(sample_pdf)
        assert len(after_reader.pages) == original_count

    def test_페이지_범위_초과시_에러를_발생시킨다(
        self, five_page_pdf: Path, tmp_path: Path
    ):
        """페이지 범위가 총 페이지를 초과하면 에러를 발생시킨다."""
        output = tmp_path / "result.pdf"
        with pytest.raises(PageRangeError, match="페이지 범위 초과"):
            cut_pdf(five_page_pdf, pages="3-10", output=output)
        # 출력 파일이 생성되지 않아야 한다
        assert not output.exists()

    def test_존재하지_않는_파일에_에러를_발생시킨다(self, tmp_path: Path):
        """존재하지 않는 입력 파일은 에러를 발생시킨다."""
        with pytest.raises(FileValidationError):
            cut_pdf(
                tmp_path / "nonexistent.pdf",
                pages="1",
                output=tmp_path / "output.pdf",
            )

    def test_출력_경로_미지정시_자동_생성한다(self, sample_pdf: Path):
        """output이 None이면 입력 파일명 기반으로 자동 생성한다."""
        result_path = cut_pdf(sample_pdf, pages="1-3", output=None)

        expected = sample_pdf.parent / "sample_cut.pdf"
        assert result_path == expected
        assert expected.exists()
        reader = PdfReader(expected)
        assert len(reader.pages) == 3
