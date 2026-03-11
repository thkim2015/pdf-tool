"""info 명령어 테스트: PDF 메타데이터 조회 및 수정을 검증한다."""

import json
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from pdf_tool.commands.info import get_metadata, set_metadata
from pdf_tool.core.exceptions import FileValidationError


@pytest.fixture()
def pdf_with_metadata(tmp_path: Path) -> Path:
    """메타데이터가 설정된 PDF를 생성한다."""
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    writer.add_metadata(
        {
            "/Title": "테스트 문서",
            "/Author": "테스트 작성자",
            "/Creator": "pytest",
        }
    )
    path = tmp_path / "with_meta.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


@pytest.fixture()
def pdf_without_metadata(tmp_path: Path) -> Path:
    """메타데이터가 없는 PDF를 생성한다."""
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    path = tmp_path / "no_meta.pdf"
    with open(path, "wb") as f:
        writer.write(f)
    return path


class TestGetMetadata:
    """메타데이터 조회 테스트."""

    def test_메타데이터를_딕셔너리로_반환한다(
        self, pdf_with_metadata: Path
    ) -> None:
        result = get_metadata(pdf_with_metadata)
        assert isinstance(result, dict)
        assert "title" in result
        assert "author" in result
        assert "pages" in result
        assert "file_size" in result

    def test_제목과_저자를_올바르게_반환한다(
        self, pdf_with_metadata: Path
    ) -> None:
        result = get_metadata(pdf_with_metadata)
        assert result["title"] == "테스트 문서"
        assert result["author"] == "테스트 작성자"

    def test_페이지_수를_올바르게_반환한다(
        self, pdf_with_metadata: Path
    ) -> None:
        result = get_metadata(pdf_with_metadata)
        assert result["pages"] == 1

    def test_파일_크기를_포함한다(self, pdf_with_metadata: Path) -> None:
        result = get_metadata(pdf_with_metadata)
        assert result["file_size"] > 0

    def test_메타데이터_없는_PDF도_처리한다(
        self, pdf_without_metadata: Path
    ) -> None:
        result = get_metadata(pdf_without_metadata)
        assert result["pages"] == 1
        # 메타데이터가 없으면 빈 문자열 또는 None
        assert result["title"] in ("", None)

    def test_존재하지_않는_파일에_에러를_발생시킨다(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileValidationError):
            get_metadata(tmp_path / "not_exists.pdf")

    def test_JSON_직렬화가_가능한_형태를_반환한다(
        self, pdf_with_metadata: Path
    ) -> None:
        result = get_metadata(pdf_with_metadata)
        # JSON 직렬화 가능해야 한다
        json_str = json.dumps(result, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["title"] == "테스트 문서"


class TestSetMetadata:
    """메타데이터 수정 테스트."""

    def test_제목을_수정할_수_있다(
        self, pdf_with_metadata: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "updated.pdf"
        set_metadata(
            pdf_with_metadata, output=output, title="새 제목"
        )
        assert output.exists()
        reader = PdfReader(output)
        assert reader.metadata is not None
        assert reader.metadata.title == "새 제목"

    def test_저자를_수정할_수_있다(
        self, pdf_with_metadata: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "updated.pdf"
        set_metadata(
            pdf_with_metadata, output=output, author="새 저자"
        )
        assert output.exists()
        reader = PdfReader(output)
        assert reader.metadata is not None
        assert reader.metadata.author == "새 저자"

    def test_제목과_저자를_동시에_수정할_수_있다(
        self, pdf_with_metadata: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "updated.pdf"
        set_metadata(
            pdf_with_metadata,
            output=output,
            title="새 제목",
            author="새 저자",
        )
        reader = PdfReader(output)
        assert reader.metadata is not None
        assert reader.metadata.title == "새 제목"
        assert reader.metadata.author == "새 저자"

    def test_기존_메타데이터를_유지하면서_일부만_수정한다(
        self, pdf_with_metadata: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "updated.pdf"
        set_metadata(
            pdf_with_metadata, output=output, title="변경된 제목"
        )
        reader = PdfReader(output)
        assert reader.metadata is not None
        assert reader.metadata.title == "변경된 제목"
        # 저자는 기존 값 유지
        assert reader.metadata.author == "테스트 작성자"

    def test_존재하지_않는_파일에_에러를_발생시킨다(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileValidationError):
            set_metadata(
                tmp_path / "not_exists.pdf",
                output=tmp_path / "out.pdf",
                title="test",
            )

    def test_페이지_내용이_보존된다(
        self, pdf_with_metadata: Path, tmp_path: Path
    ) -> None:
        output = tmp_path / "updated.pdf"
        original_pages = len(PdfReader(pdf_with_metadata).pages)
        set_metadata(
            pdf_with_metadata, output=output, title="제목"
        )
        updated_pages = len(PdfReader(output).pages)
        assert original_pages == updated_pages
