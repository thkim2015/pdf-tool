"""watermark 명령어 테스트: 텍스트/이미지 워터마크 적용을 검증한다."""

from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader, PdfWriter

from pdf_tool.commands.watermark import watermark_pdf
from pdf_tool.core.exceptions import FileValidationError, PDFProcessingError


@pytest.fixture()
def three_page_pdf(tmp_path: Path) -> Path:
    """3페이지짜리 PDF를 생성한다."""
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=595, height=842)
    path = tmp_path / "three_pages.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture()
def ten_page_pdf(tmp_path: Path) -> Path:
    """10페이지짜리 PDF를 생성한다."""
    writer = PdfWriter()
    for _ in range(10):
        writer.add_blank_page(width=595, height=842)
    path = tmp_path / "ten_pages.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture()
def sample_logo(tmp_path: Path) -> Path:
    """테스트용 PNG 이미지를 생성한다."""
    img = Image.new("RGBA", (200, 100), (255, 0, 0, 128))
    path = tmp_path / "logo.png"
    img.save(path)
    return path


class TestTextWatermark:
    """텍스트 워터마크 테스트."""

    def test_텍스트_워터마크를_적용한다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            three_page_pdf, output=output, text="DRAFT"
        )
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_투명도를_설정할_수_있다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            three_page_pdf,
            output=output,
            text="CONFIDENTIAL",
            opacity=0.5,
        )
        assert output.exists()

    def test_회전_각도를_설정할_수_있다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            three_page_pdf,
            output=output,
            text="SECRET",
            rotation=30,
        )
        assert output.exists()

    def test_위치를_설정할_수_있다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        for pos in ("center", "top", "bottom"):
            output = tmp_path / f"wm_{pos}.pdf"
            watermark_pdf(
                three_page_pdf,
                output=output,
                text="TEST",
                position=pos,
            )
            assert output.exists()

    def test_특정_페이지에만_적용할_수_있다(
        self, ten_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            ten_page_pdf,
            output=output,
            text="CONFIDENTIAL",
            pages="1,3",
        )
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_출력_경로_미지정시_자동_생성한다(
        self, three_page_pdf: Path
    ) -> None:
        result = watermark_pdf(
            three_page_pdf, text="DRAFT"
        )
        assert result.exists()
        assert "_watermarked" in result.stem


class TestImageWatermark:
    """이미지 워터마크 테스트."""

    def test_이미지_워터마크를_적용한다(
        self, three_page_pdf: Path, tmp_path: Path, sample_logo: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            three_page_pdf,
            output=output,
            image=sample_logo,
        )
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 3

    def test_위치를_설정할_수_있다(
        self, three_page_pdf: Path, tmp_path: Path, sample_logo: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        watermark_pdf(
            three_page_pdf,
            output=output,
            image=sample_logo,
            position="center",
        )
        assert output.exists()

    def test_존재하지_않는_이미지에_에러를_발생시킨다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        with pytest.raises(FileNotFoundError):
            watermark_pdf(
                three_page_pdf,
                output=output,
                image=tmp_path / "nonexistent.png",
            )


class TestWatermarkErrors:
    """워터마크 에러 처리 테스트."""

    def test_존재하지_않는_파일에_에러를_발생시킨다(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileValidationError):
            watermark_pdf(
                tmp_path / "not_exists.pdf", text="DRAFT"
            )

    def test_텍스트와_이미지_모두_없으면_에러를_발생시킨다(
        self, three_page_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "watermarked.pdf"
        with pytest.raises(PDFProcessingError, match="텍스트.*이미지"):
            watermark_pdf(three_page_pdf, output=output)
