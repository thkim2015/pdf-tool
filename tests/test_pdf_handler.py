"""pdf_handler 모듈의 명세 테스트."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdf_tool.core.exceptions import FileValidationError
from pdf_tool.core.pdf_handler import load_pdf, save_pdf


class TestLoadPdf:
    """PDF 파일 로딩 기능을 검증한다."""

    def test_유효한_PDF를_로드한다(self, sample_pdf: Path):
        """유효한 PDF 파일을 PdfReader로 로드한다."""
        reader = load_pdf(sample_pdf)
        assert isinstance(reader, PdfReader)
        assert len(reader.pages) == 10

    def test_존재하지_않는_파일에_에러를_발생시킨다(self, tmp_path: Path):
        """존재하지 않는 파일 로드 시 에러를 발생시킨다."""
        with pytest.raises(FileValidationError):
            load_pdf(tmp_path / "nonexistent.pdf")

    def test_유효하지_않은_PDF에_에러를_발생시킨다(self, invalid_pdf: Path):
        """유효하지 않은 PDF 파일 로드 시 에러를 발생시킨다."""
        with pytest.raises(FileValidationError):
            load_pdf(invalid_pdf)


class TestSavePdf:
    """PDF 파일 저장 기능을 검증한다."""

    def test_PDF를_파일로_저장한다(self, tmp_path: Path):
        """PdfWriter의 내용을 파일로 저장한다."""
        writer = PdfWriter()
        writer.add_blank_page(width=595, height=842)
        output_path = tmp_path / "output.pdf"

        save_pdf(writer, output_path)

        assert output_path.exists()
        reader = PdfReader(output_path)
        assert len(reader.pages) == 1

    def test_존재하지_않는_디렉토리에_에러를_발생시킨다(self, tmp_path: Path):
        """출력 경로의 부모 디렉토리가 없으면 에러를 발생시킨다."""
        writer = PdfWriter()
        writer.add_blank_page(width=595, height=842)
        output_path = tmp_path / "nonexistent" / "output.pdf"

        with pytest.raises(FileValidationError):
            save_pdf(writer, output_path)
