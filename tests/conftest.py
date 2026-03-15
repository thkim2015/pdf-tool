"""테스트 픽스처: 샘플 PDF를 동적으로 생성한다."""

from pathlib import Path

import pytest
from pypdf import PdfWriter


def _create_pdf(path: Path, num_pages: int) -> Path:
    """지정된 페이지 수를 가진 PDF 파일을 생성한다."""
    writer = PdfWriter()
    for _i in range(num_pages):
        # 빈 A4 페이지 추가 (595 x 842 포인트)
        writer.add_blank_page(width=595, height=842)
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture()
def sample_pdf(tmp_path: Path) -> Path:
    """10페이지짜리 샘플 PDF를 생성한다."""
    return _create_pdf(tmp_path / "sample.pdf", 10)


@pytest.fixture()
def small_pdf(tmp_path: Path) -> Path:
    """3페이지짜리 작은 PDF를 생성한다."""
    return _create_pdf(tmp_path / "small.pdf", 3)


@pytest.fixture()
def single_page_pdf(tmp_path: Path) -> Path:
    """1페이지짜리 PDF를 생성한다."""
    return _create_pdf(tmp_path / "single.pdf", 1)


@pytest.fixture()
def five_page_pdf(tmp_path: Path) -> Path:
    """5페이지짜리 PDF를 생성한다."""
    return _create_pdf(tmp_path / "five.pdf", 5)


@pytest.fixture()
def twelve_page_pdf(tmp_path: Path) -> Path:
    """12페이지짜리 PDF를 생성한다."""
    return _create_pdf(tmp_path / "twelve.pdf", 12)


@pytest.fixture()
def invalid_pdf(tmp_path: Path) -> Path:
    """유효하지 않은 PDF 파일 (텍스트 파일)을 생성한다."""
    path = tmp_path / "not_a_pdf.txt"
    path.write_text("이것은 PDF가 아닙니다", encoding="utf-8")
    return path


@pytest.fixture()
def create_pdf(tmp_path: Path):
    """임의의 페이지 수를 가진 PDF 생성 팩토리 픽스처."""

    def _factory(name: str, num_pages: int) -> Path:
        return _create_pdf(tmp_path / name, num_pages)

    return _factory
