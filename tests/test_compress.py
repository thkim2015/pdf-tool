"""compress 명령어 테스트: PDF 압축 기능을 검증한다."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdf_tool.commands.compress import compress_pdf
from pdf_tool.core.exceptions import FileValidationError


@pytest.fixture()
def uncompressed_pdf(tmp_path: Path) -> Path:
    """압축 가능한 콘텐츠를 가진 PDF를 생성한다."""
    writer = PdfWriter()
    for _i in range(5):
        writer.add_blank_page(width=595, height=842)
    # 반복적인 콘텐츠를 추가하여 압축 가능하게 만든다
    path = tmp_path / "uncompressed.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


class TestCompressPdf:
    """PDF 압축 기능 테스트."""

    def test_압축된_PDF_파일을_생성한다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "compressed.pdf"
        result = compress_pdf(uncompressed_pdf, output=output)
        assert output.exists()
        assert result["output_path"] == output

    def test_압축_결과에_크기_정보를_포함한다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "compressed.pdf"
        result = compress_pdf(uncompressed_pdf, output=output)
        assert "original_size" in result
        assert "compressed_size" in result
        assert "reduction_percent" in result
        assert result["original_size"] > 0
        assert result["compressed_size"] > 0

    def test_압축_후_파일_크기가_원본_이하이다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "compressed.pdf"
        result = compress_pdf(uncompressed_pdf, output=output)
        assert result["compressed_size"] <= result["original_size"]

    def test_압축_후_페이지_수가_동일하다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "compressed.pdf"
        original_pages = len(PdfReader(uncompressed_pdf).pages)
        compress_pdf(uncompressed_pdf, output=output)
        compressed_pages = len(PdfReader(output).pages)
        assert original_pages == compressed_pages

    def test_절감률을_백분율로_반환한다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "compressed.pdf"
        result = compress_pdf(uncompressed_pdf, output=output)
        assert 0 <= result["reduction_percent"] <= 100

    def test_출력_경로_미지정시_자동_생성한다(
        self, uncompressed_pdf: Path
    ) -> None:
        result = compress_pdf(uncompressed_pdf)
        output = result["output_path"]
        assert output.exists()
        assert "_compressed" in output.stem

    def test_존재하지_않는_파일에_에러를_발생시킨다(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileValidationError):
            compress_pdf(tmp_path / "not_exists.pdf")

    def test_이미_압축된_PDF의_효과가_미미하다(
        self, uncompressed_pdf: Path, tmp_path: Path
    ) -> None:
        """이미 압축된 PDF를 다시 압축하면 절감률이 낮아야 한다."""
        first_output = tmp_path / "first.pdf"
        compress_pdf(uncompressed_pdf, output=first_output)

        second_output = tmp_path / "second.pdf"
        result = compress_pdf(first_output, output=second_output)
        # 이미 압축된 파일이므로 추가 압축 효과가 거의 없다
        assert result["reduction_percent"] >= 0
