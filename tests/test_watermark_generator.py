"""watermark_generator 모듈 테스트: 텍스트/이미지 워터마크 오버레이 PDF 생성을 검증한다."""

from pathlib import Path

import pytest
from PIL import Image
from pypdf import PdfReader

from pdf_tool.core.watermark_generator import (
    create_image_watermark,
    create_text_watermark,
)


@pytest.fixture()
def sample_logo(tmp_path: Path) -> Path:
    """테스트용 PNG 로고 이미지를 생성한다."""
    img = Image.new("RGBA", (200, 100), (255, 0, 0, 128))
    path = tmp_path / "logo.png"
    img.save(path)
    return path


class TestCreateTextWatermark:
    """텍스트 워터마크 PDF 생성 테스트."""

    def test_텍스트_워터마크_PDF를_생성한다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="DRAFT",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
        )
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_투명도를_설정할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        # 투명도 0.5로 워터마크 생성 - 에러 없이 완료되어야 한다
        create_text_watermark(
            text="CONFIDENTIAL",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            opacity=0.5,
        )
        assert output.exists()

    def test_회전_각도를_설정할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="SECRET",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            rotation=30,
        )
        assert output.exists()

    def test_위치를_center로_설정할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="DRAFT",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            position="center",
        )
        assert output.exists()

    def test_위치를_top으로_설정할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="DRAFT",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            position="top",
        )
        assert output.exists()

    def test_위치를_bottom으로_설정할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="DRAFT",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            position="bottom",
        )
        assert output.exists()

    def test_기본값으로_생성할_수_있다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        create_text_watermark(
            text="TEST",
            output_path=output,
            page_width=595.0,
            page_height=842.0,
        )
        assert output.exists()
        # 기본값: opacity=0.3, rotation=45, position="center"


class TestCreateImageWatermark:
    """이미지 워터마크 PDF 생성 테스트."""

    def test_이미지_워터마크_PDF를_생성한다(
        self, tmp_path: Path, sample_logo: Path
    ) -> None:
        output = tmp_path / "watermark.pdf"
        create_image_watermark(
            image_path=sample_logo,
            output_path=output,
            page_width=595.0,
            page_height=842.0,
        )
        assert output.exists()
        reader = PdfReader(output)
        assert len(reader.pages) == 1

    def test_투명도를_설정할_수_있다(
        self, tmp_path: Path, sample_logo: Path
    ) -> None:
        output = tmp_path / "watermark.pdf"
        create_image_watermark(
            image_path=sample_logo,
            output_path=output,
            page_width=595.0,
            page_height=842.0,
            opacity=0.5,
        )
        assert output.exists()

    def test_위치를_설정할_수_있다(
        self, tmp_path: Path, sample_logo: Path
    ) -> None:
        for pos in ("center", "top", "bottom"):
            output = tmp_path / f"watermark_{pos}.pdf"
            create_image_watermark(
                image_path=sample_logo,
                output_path=output,
                page_width=595.0,
                page_height=842.0,
                position=pos,
            )
            assert output.exists()

    def test_존재하지_않는_이미지에_에러를_발생시킨다(self, tmp_path: Path) -> None:
        output = tmp_path / "watermark.pdf"
        with pytest.raises(FileNotFoundError):
            create_image_watermark(
                image_path=tmp_path / "nonexistent.png",
                output_path=output,
                page_width=595.0,
                page_height=842.0,
            )
