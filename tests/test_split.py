"""split 명령어의 명세 테스트."""

from pathlib import Path

import pytest
from pypdf import PdfReader

from pdf_tool.commands.split import split_pdf
from pdf_tool.core.exceptions import FileValidationError


class TestSplitPdf:
    """PDF 분할 기능을 검증한다."""

    def test_페이지별_분할한다(self, five_page_pdf: Path, tmp_path: Path):
        """5페이지 PDF를 각각 1페이지씩 5개 파일로 분할한다."""
        output_dir = tmp_path / "pages"
        output_dir.mkdir()

        result_files = split_pdf(five_page_pdf, output_dir=output_dir)

        assert len(result_files) == 5
        for f in result_files:
            reader = PdfReader(f)
            assert len(reader.pages) == 1

    def test_파일명_패턴이_올바르다(self, five_page_pdf: Path, tmp_path: Path):
        """분할된 파일명이 _001, _002 형태를 따른다."""
        output_dir = tmp_path / "pages"
        output_dir.mkdir()

        result_files = split_pdf(five_page_pdf, output_dir=output_dir)

        expected_names = [f"five_{i:03d}.pdf" for i in range(1, 6)]
        actual_names = [f.name for f in result_files]
        assert actual_names == expected_names

    def test_단위별_분할한다(self, twelve_page_pdf: Path, tmp_path: Path):
        """12페이지 PDF를 5페이지 단위로 3개 파일(5p, 5p, 2p)로 분할한다."""
        output_dir = tmp_path / "parts"
        output_dir.mkdir()

        result_files = split_pdf(twelve_page_pdf, every=5, output_dir=output_dir)

        assert len(result_files) == 3
        assert len(PdfReader(result_files[0]).pages) == 5
        assert len(PdfReader(result_files[1]).pages) == 5
        assert len(PdfReader(result_files[2]).pages) == 2

    def test_분할_단위가_총_페이지_초과시_단일_파일을_생성한다(
        self, small_pdf: Path, tmp_path: Path
    ):
        """분할 단위(10)가 총 페이지(3)보다 크면 1개 파일을 생성한다."""
        output_dir = tmp_path / "parts"
        output_dir.mkdir()

        result_files = split_pdf(small_pdf, every=10, output_dir=output_dir)

        assert len(result_files) == 1
        assert len(PdfReader(result_files[0]).pages) == 3

    def test_존재하지_않는_파일에_에러를_발생시킨다(self, tmp_path: Path):
        """존재하지 않는 입력 파일은 에러를 발생시킨다."""
        output_dir = tmp_path / "out"
        output_dir.mkdir()

        with pytest.raises(FileValidationError):
            split_pdf(tmp_path / "nonexistent.pdf", output_dir=output_dir)

    def test_출력_디렉토리를_자동_생성한다(self, small_pdf: Path, tmp_path: Path):
        """출력 디렉토리가 존재하지 않으면 자동 생성한다."""
        output_dir = tmp_path / "new_dir"

        result_files = split_pdf(small_pdf, output_dir=output_dir)

        assert output_dir.exists()
        assert len(result_files) == 3
