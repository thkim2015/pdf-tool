"""merge 명령어의 명세 테스트."""

from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_tool.commands.merge import merge_pdfs
from pdf_tool.core.exceptions import FileValidationError


class TestMergePdfs:
    """PDF 병합 기능을 검증한다."""

    def test_여러_파일을_병합한다(self, create_pdf, tmp_path: Path):
        """3개 파일(3p + 5p + 2p = 10p)을 병합한다."""
        a = create_pdf("a.pdf", 3)
        b = create_pdf("b.pdf", 5)
        c = create_pdf("c.pdf", 2)
        output = tmp_path / "merged.pdf"

        merge_pdfs([a, b, c], output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 10

    def test_두_파일을_병합한다(self, create_pdf, tmp_path: Path):
        """2개 파일을 병합한다."""
        a = create_pdf("a.pdf", 3)
        b = create_pdf("b.pdf", 4)
        output = tmp_path / "merged.pdf"

        merge_pdfs([a, b], output=output)

        reader = PdfReader(output)
        assert len(reader.pages) == 7

    def test_존재하지_않는_파일_포함시_에러를_발생시킨다(
        self, create_pdf, tmp_path: Path
    ):
        """병합 대상 중 존재하지 않는 파일이 있으면 에러를 발생시킨다."""
        a = create_pdf("a.pdf", 3)
        missing = tmp_path / "missing.pdf"
        output = tmp_path / "merged.pdf"

        with pytest.raises(FileValidationError, match="파일을 찾을 수 없습니다"):
            merge_pdfs([a, missing], output=output)

    def test_유효하지_않은_PDF_포함시_에러를_발생시킨다(
        self, create_pdf, invalid_pdf: Path, tmp_path: Path
    ):
        """유효하지 않은 PDF가 포함되면 에러를 발생시킨다."""
        a = create_pdf("a.pdf", 3)
        output = tmp_path / "merged.pdf"

        with pytest.raises(FileValidationError, match="유효한 PDF 파일이 아닙니다"):
            merge_pdfs([a, invalid_pdf], output=output)

    def test_glob_패턴으로_파일을_병합한다(self, tmp_path: Path):
        """glob 패턴으로 매칭되는 파일을 알파벳 순서로 병합한다."""
        from pypdf import PdfWriter

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        for name, pages in [("01.pdf", 2), ("02.pdf", 3), ("03.pdf", 1)]:
            writer = PdfWriter()
            for _ in range(pages):
                writer.add_blank_page(width=595, height=842)
            with open(docs_dir / name, "wb") as f:
                writer.write(f)

        output = tmp_path / "all.pdf"
        merge_pdfs([docs_dir / "*.pdf"], output=output, use_glob=True)

        reader = PdfReader(output)
        assert len(reader.pages) == 6  # 2 + 3 + 1

    def test_출력_경로_미지정시_자동_생성한다(self, create_pdf):
        """output이 None이면 첫 번째 파일명 기반으로 자동 생성한다."""
        a = create_pdf("a.pdf", 2)
        b = create_pdf("b.pdf", 3)

        result_path = merge_pdfs([a, b], output=None)

        expected = a.parent / "a_merged.pdf"
        assert result_path == expected
        assert expected.exists()
