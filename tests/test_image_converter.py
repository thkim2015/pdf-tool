"""Image to PDF 변환 기능 테스트."""

import tempfile
from pathlib import Path

import pytest
from PIL import Image

from pdf_tool.core.exceptions import FileValidationError
from pdf_tool.core.image_converter import (
    image_to_pdf,
    validate_image_file,
)


@pytest.fixture
def temp_dir():
    """임시 디렉토리를 생성한다."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_image(temp_dir):
    """샘플 이미지를 생성한다."""
    img_path = temp_dir / "test_image.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_gray_image(temp_dir):
    """샘플 그레이스케일 이미지를 생성한다."""
    img_path = temp_dir / "test_gray.png"
    img = Image.new("L", (100, 100), color=128)
    img.save(img_path)
    return img_path


@pytest.fixture
def sample_rgba_image(temp_dir):
    """샘플 RGBA 이미지를 생성한다."""
    img_path = temp_dir / "test_rgba.png"
    img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))
    img.save(img_path)
    return img_path


class TestValidateImageFile:
    """validate_image_file 함수 테스트."""

    def test_valid_image_file(self, sample_image):
        """유효한 이미지 파일 검증."""
        # 예외가 발생하지 않아야 함
        validate_image_file(sample_image)

    def test_nonexistent_file(self, temp_dir):
        """존재하지 않는 파일 검증."""
        nonexistent = temp_dir / "nonexistent.png"
        with pytest.raises(FileValidationError, match="파일을 찾을 수 없습니다"):
            validate_image_file(nonexistent)

    def test_unsupported_format(self, temp_dir):
        """지원하지 않는 포맷 검증."""
        unsupported = temp_dir / "test.xyz"
        unsupported.touch()
        with pytest.raises(FileValidationError, match="지원하지 않는 이미지 포맷"):
            validate_image_file(unsupported)

    def test_invalid_image_file(self, temp_dir):
        """유효하지 않은 이미지 파일 검증."""
        invalid_img = temp_dir / "invalid.png"
        invalid_img.write_text("not an image")
        with pytest.raises(FileValidationError, match="유효한 이미지 파일이 아닙니다"):
            validate_image_file(invalid_img)


class TestImageToPDF:
    """image_to_pdf 함수 테스트."""

    def test_single_image_to_pdf(self, sample_image, temp_dir):
        """단일 이미지를 PDF로 변환."""
        output_pdf = temp_dir / "output.pdf"
        image_to_pdf(sample_image, output_pdf)

        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_multiple_images_to_pdf(self, sample_image, sample_gray_image, temp_dir):
        """여러 이미지를 PDF로 변환."""
        output_pdf = temp_dir / "output.pdf"
        image_to_pdf([sample_image, sample_gray_image], output_pdf)

        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_rgba_image_to_pdf(self, sample_rgba_image, temp_dir):
        """RGBA 이미지를 PDF로 변환 (투명도 처리)."""
        output_pdf = temp_dir / "output.pdf"
        image_to_pdf(sample_rgba_image, output_pdf)

        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_image_to_pdf_with_aspect_ratio(self, sample_image, temp_dir):
        """종횡비 유지하여 이미지를 PDF로 변환."""
        output_pdf = temp_dir / "output.pdf"
        image_to_pdf(sample_image, output_pdf, keep_aspect_ratio=True)

        assert output_pdf.exists()

    def test_image_to_pdf_without_aspect_ratio(self, sample_image, temp_dir):
        """종횡비 무시하여 이미지를 PDF로 변환."""
        output_pdf = temp_dir / "output.pdf"
        image_to_pdf(sample_image, output_pdf, keep_aspect_ratio=False)

        assert output_pdf.exists()

    def test_empty_image_list(self, temp_dir):
        """빈 이미지 리스트로 변환 시도."""
        output_pdf = temp_dir / "output.pdf"
        with pytest.raises(FileValidationError, match="변환할 이미지가 없습니다"):
            image_to_pdf([], output_pdf)

    def test_invalid_output_path(self, sample_image, temp_dir):
        """유효하지 않은 출력 경로."""
        invalid_output = temp_dir / "nonexistent_dir" / "output.pdf"
        with pytest.raises(FileValidationError, match="출력 디렉토리가 존재하지 않습니다"):
            image_to_pdf(sample_image, invalid_output)

    def test_all_supported_formats(self, temp_dir):
        """지원하는 모든 이미지 포맷 테스트."""
        temp_dir / "output.pdf"

        # PNG, JPG, BMP, TIFF 이미지 생성 및 변환 테스트
        test_formats = [
            ("png", "PNG"),
            ("jpg", "JPEG"),
            ("bmp", "BMP"),
            ("tiff", "TIFF"),
        ]

        for ext, format_name in test_formats:
            img_path = temp_dir / f"test.{ext}"
            img = Image.new("RGB", (50, 50), color="blue")
            img.save(img_path, format=format_name)

            output = temp_dir / f"output_{ext}.pdf"
            image_to_pdf(img_path, output)
            assert output.exists(), f"Failed to convert {ext} image"
