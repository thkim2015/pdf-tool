"""resize 명령어 테스트: 페이지 크기 변경 및 DPI 리사이즈를 검증한다."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdf_tool.commands.resize import resize_pdf
from pdf_tool.core.exceptions import FileValidationError, PDFProcessingError
from pdf_tool.core.page_sizes import mm_to_points


@pytest.fixture()
def letter_pdf(tmp_path: Path) -> Path:
    """Letter 크기 PDF를 생성한다 (612x792 포인트)."""
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=612, height=792)
    path = tmp_path / "letter.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture()
def a4_pdf(tmp_path: Path) -> Path:
    """A4 크기 PDF를 생성한다 (595x842 포인트)."""
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    path = tmp_path / "a4.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


class TestResizePdfBySize:
    """용지 크기 리사이즈 테스트."""

    def test_A4_크기로_리사이즈한다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(letter_pdf, output=output, size="A4")
        assert output.exists()
        reader = PdfReader(output)
        page = reader.pages[0]
        target_w = mm_to_points(210)
        target_h = mm_to_points(297)
        # 페이지 크기가 A4에 근접해야 한다 (1포인트 오차 허용)
        assert float(page.mediabox.width) == pytest.approx(target_w, abs=1.0)
        assert float(page.mediabox.height) == pytest.approx(target_h, abs=1.0)

    def test_Letter_크기로_리사이즈한다(
        self, a4_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(a4_pdf, output=output, size="Letter")
        assert output.exists()
        reader = PdfReader(output)
        page = reader.pages[0]
        target_w = mm_to_points(216)
        target_h = mm_to_points(279)
        assert float(page.mediabox.width) == pytest.approx(target_w, abs=1.0)
        assert float(page.mediabox.height) == pytest.approx(target_h, abs=1.0)

    def test_커스텀_크기로_리사이즈한다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(
            letter_pdf,
            output=output,
            width_mm=150,
            height_mm=200,
        )
        reader = PdfReader(output)
        page = reader.pages[0]
        assert float(page.mediabox.width) == pytest.approx(
            mm_to_points(150), abs=1.0
        )
        assert float(page.mediabox.height) == pytest.approx(
            mm_to_points(200), abs=1.0
        )

    def test_모든_페이지가_리사이즈된다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(letter_pdf, output=output, size="A4")
        reader = PdfReader(output)
        assert len(reader.pages) == 3
        target_w = mm_to_points(210)
        for page in reader.pages:
            assert float(page.mediabox.width) == pytest.approx(target_w, abs=1.0)

    def test_지원되지_않는_크기에_에러를_발생시킨다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        with pytest.raises(PDFProcessingError, match="지원되지 않는 크기"):
            resize_pdf(letter_pdf, output=output, size="B7")

    def test_대소문자_무관하게_크기를_인식한다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(letter_pdf, output=output, size="a4")
        assert output.exists()

    def test_stretch_모드를_지원한다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(letter_pdf, output=output, size="A4", mode="stretch")
        assert output.exists()

    def test_fill_모드를_지원한다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        resize_pdf(letter_pdf, output=output, size="A4", mode="fill")
        assert output.exists()

    def test_출력_경로_미지정시_자동_생성한다(
        self, letter_pdf: Path
    ) -> None:
        result = resize_pdf(letter_pdf, size="A4")
        assert result.exists()
        assert "_resized" in result.stem

    def test_존재하지_않는_파일에_에러를_발생시킨다(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileValidationError):
            resize_pdf(tmp_path / "not_exists.pdf", size="A4")

    def test_크기_지정_없이_호출하면_에러를_발생시킨다(
        self, letter_pdf: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "resized.pdf"
        with pytest.raises(PDFProcessingError, match="크기.*지정"):
            resize_pdf(letter_pdf, output=output)
